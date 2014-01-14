"""
SMPP Server
"""

import time
import socket
import hashlib
import transaction
import multiprocessing
import datetime
import threading

from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, message_state
from smpp5.lib.session.shared_connection import SharedConnection

import db
from db import DBSession
from models import User, Sms, User_Number, Prefix_Match, Packages, Selected_package, Network, Mnp
from smpp5.lib.session import SMPPSession, SessionState
from smpp5.client.smpp_client import SMPPClient


def handle_client_connection(conn, addr):
    """
    This method is responsible to handle a client connection and creating two background threads...One for handling
    client request pdus and other for delivering smses to client..
    """

    print("Accepted connection from: " + repr(addr))
    server_session = SMPPSession('server', conn)  # SMPPSession class object has been created.
    
    # Server class has session object so its methods are easily accessible here, return values have been passed.
    # These variables in session have been assigned methods of server class.so that these variables act as methods in session. 
    server_session.server_db_store = SMPPServer.db_storage  # sms_ids have been passed to variable in SMPP Session.
    server_session.server_validate_method = SMPPServer.validate 
    server_session.server_query_result = SMPPServer.query_result
    server_session.server_cancel_result = SMPPServer.cancel_result
    server_session.server_replace_result = SMPPServer.replace_result
    server_session.sever_fetch_sms = fetch_incoming_sms
    server_session.commit_db = commit_db

    # Background thread 1 is to handle client request pdus by recieving them from socket and storing them in dictionary.
    background_thread = threading.Thread(target=handle_client_requests, args=(server_session, conn))
    background_thread.start()

    # Background thread 2 to check database for incoming messages every 5secs and deliever smses to client if any.
    background_thread2 = threading.Thread(target=deliver_sms, args=(server_session, conn))
    background_thread2.start()

    # Main/ Parent thread is responsible for receiving deliver sms requests and all pdu responses from client and storing them in dict.
    while server_session.state != SessionState.UNBOUND:
        server_session.handle_pdu()

    conn.close()
    #time.sleep(1)
    background_thread.join()  # Joining the threads means to terminate them at the point where all the threads have finished their work.
    background_thread2.join()


def handle_client_requests(server_session, conn):
    """
    This method called by thread handles client request/response pdus by reading them from socket and storing them in dictionary
    till Unbound state.
    """

    while conn.is_open is True:
        server_session.process_request()  # Accessing session class method


def deliver_sms(server_session, conn):
    """
    This method  called by thread checks database for incoming smses every 5 seconds and deliver sms to the client periodically.
    """
    _thread_lock = None
    # Thread lock to lock the shared access of data.
    _thread_lock = threading.Lock()
    while conn.is_open is True:
        # If state is receiver or transceiver
        if server_session.state in [SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            # Periodically checks for incoming smses.
            time.sleep(5)
            _thread_lock.acquire()  # Acquire the thread lock.
            server_session.deliver_sms()  # Accessing session class method
            transaction.commit()  # Changes in sms status has been committed to database.
            _thread_lock.release()  # Release the thread lock so that shared can be used by any other entity.


def fetch_incoming_sms(user_id):
    """
    This method query database to retrieve pending incoming smses for logged in client..
    """

    smses = DBSession.query(Sms).filter_by(sms_type='incoming', user_id=user_id, status='recieved').first()
    # If there are incoming smses for the client.
    if smses:
        smses.status = 'delivered'  # Set the status of incoming sms in database as delieverd in place of received.
    return(smses)  # Return all these incoming pending smses to the deliver sms method in session.


def thread_4_incoming_sms():
    'This method will infinitely process incoming sms till server terminates.'
    while True:
        process_incoming_sms()
        transaction.commit()
        #updating_status(sms_ids)
        time.sleep(5)


def process_incoming_sms():
    """
    This method is responsible for processing incoming smses into the database.
    """

    sms_ids = ''
    # Fetch smses from database whose type is incoming, status is received, target netwrok is none because its been sent to smpp client
    # since user id is none.
    smses = DBSession.query(Sms).filter_by(sms_type='incoming', status='recieved', target_network=None, user_id=None).all()
    if smses:
        for S in smses:
            sms_to = S.sms_to  # Get the destination
            sms_from = S.sms_from  # Set the sender
            mnp = DBSession.query(Mnp).filter_by(cell_number=sms_to).first()  # Querying for converted mobile numbers.
            if mnp: #  If destination is some no. from mnp table
                target_network = mnp.target_network  # Get the target number into a variable.
                S.sms_type = 'outgoing'  # Set the sms type in database as outgoing because now it would be sent to the destination.
                S.status = 'scheduled'  # Set status in database as scheduled.  
                S.validity_period = datetime.date.today()+datetime.timedelta(days=1)  # Set validity period of 1 day.
            else:
                source_prefix = sms_from[0:6]  # Extract prefix of sender number.
                dest_prefix = sms_to[0:6]  # Extract prefix of recipient.
                s_network = DBSession.query(Prefix_Match).filter_by(prefix=source_prefix).first()  # Query the database in prefix match table  to find the source network.
                source_network = s_network.network  # Refers to sender network.
                d_network = DBSession.query(Prefix_Match).filter_by(prefix=dest_prefix).first()  # Query the database in prefix match table  to find the destination network.
                dest_network = d_network.network   # Refers to recipient network.
                user = DBSession.query(User_Number).filter_by(cell_number=sms_to).first()  # User refers to normal user.
                if user:  # If user is a client
                    S.user_id = user.user_id
                    target_network = None
                else:  # If destination is of the same network
                    target_network = dest_network
                    S.sms_type = 'outgoing'
                    S.status = 'scheduled'
                    S.validity_period = datetime.date.today()+datetime.timedelta(days=1)
            S.target_network = target_network  # Set the target network in database.
            if target_network != source_network:  # If source and destination network are different
                connect_info(sms_to, S.msg, dest_network, S.id, sms_from)  # Call connection info method.
                

def process_outgoing_sms(sender, user_id, recipient):
    """
    This method is responsible for processing outgoing smses.
    """
    if sender is not '':
            sender_number = sender  # Get the sender number.
    else:
        user = DBSession.query(User_Number).filter_by(user_id=user_id).first()  # User refers to client.
        sender_number = user.cell_number  # Cell number of sender
    source_prefix = sender_number[0:6]  # Extract prefix of sender number
    s_network = DBSession.query(Prefix_Match).filter_by(prefix=source_prefix).first()  #  Getting the network of source from prefixes.
    source_network = s_network.network  # Refers to sender network
    dest_prefix = recipient[0:6]  # Extract prefix of recipient
    d_network = DBSession.query(Prefix_Match).filter_by(prefix=dest_prefix).first()  #  Getting the network of destination from prefixes.
    dest_network = d_network.network   # Refers to recipient network
    mnp = DBSession.query(Mnp).filter_by(cell_number=recipient).first()  # Querying for mobile number conversion
    if mnp:
        target_network = mnp.target_network
    elif(source_network == dest_network):
        target_network = dest_network
    else:
        target_network = dest_network
        
    return(dict(sender_number=sender_number, source_network=source_network, target_network=target_network))  # Returning the dict.


def commit_db():
    """
    This method is used to commit database transaction
    """

    transaction.commit()


def connect_info(recipient, message, dest_network, sms_id, sender_number):
    """
    This method is responsible to get sms fields and connection parameters from process incoming sms method to communicate with destination network
    server in case when sender sends a message to some other network.
    """

    # here we have to make client object
    server = DBSession.query(Network).filter_by(network=dest_network).first()  # Query the Network table to get the ip and port of other smpp server.
    if server:
        system_id = server.username
        password = server.password
        system_type = server.system_type
        ip = server.ip
        port = server.port

        # Background thread3 is responible to send sms to the other server.
        background_thread3 = threading.Thread(target=connect_to_server,
                                              args=(ip, port, system_id, password, system_type, recipient, message,
                                                    sms_id, sender_number))
        background_thread3.start() # Start the thread
        background_thread3.join()  # Join thread so that when all threads will finish their work then the process will terminate.


def connect_to_server(ip, port, system_id, password, system_type, recipient, message, sms_id, sender_number):
    """
    In this method server creates client instance to communicate with the destination network server,
    current server will connect with other server as client.
    """

    client = SMPPClient(ip, port, 'TX', system_id, password, system_type)  # Creates client instance,connect with other server via these paramaters this server will bind with nother server as transmitter.
    connection = False
    notification = 0
    while connection is False:   # While connection is not established with server, try to connect.
        if client.connect():  # Call the connect method of client class.
            connection = True  
            # This thread is checking the socket for receiving responses from other server and saves in the dictionary.
            background_thread4 = threading.Thread(target=client.session.storing_recieved_pdus, args=())  # To recieve pdu response from other smpp server to whom it has sent the request.
            background_thread4.start()  # Start the thread

    if client.login():  # If client successfully logins
        client.session.send_sms(recipient, message, sender_number)
        while notification == 0:
            notification = client.session.notifications_4_client()  
        client.session.processing_recieved_pdus()
    smses = DBSession.query(Sms).filter_by(id=int(sms_id)).first()  # Read sms from database that is delivered to other smpp server.
    if smses:
        smses.status = 'delivered'  # Mark status of that message as delivered in database.
        transaction.commit()  # Commit in database.
    client.session.unbind()
    while client.session.state != SessionState.UNBOUND:  # If session state is not set as unbind.
        client.session.processing_recieved_pdus()  # Again call this method.
    client.sc.close()  # Close the shared socket connection.
    background_thread4.join()  # Terminate the program unless all threads finish their work.


def selected_packages(user_id):
    """
    This method is used by server to ensure if logged in user has selected any package or not so thst he will be charged normally or on package rate.
    """

    total_selected_package = DBSession.query(Selected_package).filter_by(user_id=user_id).count()  # Queries for number of selected packages.
    if(total_selected_package > 0):
        selected_package = DBSession.query(Selected_package).filter_by(user_id=user_id)[-1]  # Retrieve last selected package.
    else:
        selected_package = None
    if(selected_package is None):
            package_name = None
            rates = 1.5
    else:
        end_date = int(selected_package.end_date.strftime('%d'))  # Get the package end date and convert to integer.
        end_month = int(selected_package.end_date.strftime('%m'))  # Get the package end month and convert to integer.
        end_year = int(selected_package.end_date.strftime('%y'))  # Get package end year and convert to integer.
        date = datetime.datetime.now()  # Get today's date.
        today_date = int(date.strftime('%d'))  # Get today's date and convert to integer.
        today_month = int(date.strftime('%m'))  # Get current month and convert to integer.
        today_year = int(date.strftime('%y'))  # # Get current year and convert to integer.
        if(end_year > today_year and int(selected_package.smses) > 0):  # If package is not expired and number of sent smses are greater than zero.
            package_name = selected_package.package_name  # Get the selected package name
            rates = 0.0  
            selected_package.smses = selected_package.smses-1  # Subtract 1 sms from total smses. 
        elif(end_year == today_year and end_month > today_month and int(selected_package.smses) > 0):  # iF PACKAGE IS NOT EXPIRED.
            package_name = selected_package.package_name
            rates = 0.0
            selected_package.smses = selected_package.smses-1
        elif(end_month == today_month):  # # iF PACKAGE IS NOT EXPIRED.
            if(end_date >= today_date and int(selected_package.smses) > 0):
                package_name = selected_package.package_name
                rates = 0.0
                selected_package.smses = selected_package.smses-1
        else:  #  Charge sms on normal rate.
            package_name = None
            rates = 1.5
            
    return(dict(package_name=package_name, rates=rates))  # Return dict


class SMPPServer(object):
    '''
    Server class is responsible for performing database related activities as requested by client like retrieving,
    deleting, updating database etc.
    '''

    def __init__(self):
        self.socket = None
        self.session = None

    def start_serving(self, host, port):
        """
        This method is used by server to accept binding request of client on ip address on which server is listening
        and also creating seperate process to handle each client..
        """
        print("*** Seving on {host}:{port}".format(host=host, port=port))

        if '0.0.0.0' == host:  # translating all available ips to socket convention
            host = ''

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating socket.
        self.socket.bind((host, port))  # built-in method, socket binds with server.
        db.bind_session()  # Models bind with database engine.
        background_thread1 = threading.Thread(target=thread_4_incoming_sms, args=())  # Thread for incoming smses processing.
        background_thread1.start()  # Start the thread.

        try:
            while True:
                self.socket.listen(1)  # Socket listening for connections.
                print("ZONG server listening......")
                conn, addr = self.socket.accept()  # Socket accept connections and return ip and port.
                sc = SharedConnection(conn)  # Make shared connection class object and pass it the socket object.
                sc.is_open = True

                P = multiprocessing.Process(target=handle_client_connection, args=(sc, addr))  # For every client request a process would be made to handle it.
                P.start()  # Start the process.

                active_conns = multiprocessing.active_children()  # Tell count of active clients.
                print("Active connections: %i" % len(active_conns))

        except (KeyboardInterrupt, SystemExit):
            print("Good bye!")

    def validate(system_id, password, system_type):
        """
        This method is used by server when it receives the bind tx, rx, trx request it validates the credentials provided by the client against database.
        """

        system_id = system_id.decode(encoding='ascii')
        passhash = hashlib.sha1(bytes(password.decode(encoding='ascii'), encoding="utf8")).hexdigest()
        system_type = system_type.decode(encoding='ascii')
        record = DBSession.query(User).filter_by(user_id=system_id, password=passhash, system_type=system_type).first()
        if(record):
            print("Credentials Validated successfully!!!")
            return 'True'
        else:
            print("Validation failed")
            return 'false'

    def db_storage(recipients, message, user_id, sender):
        """
        This method is responsible to store Sms and related fields provided by the client in the database.
        """
        
        # Contains all message ids that are sent by client to recipient of same or different network.
        sms_ids = ''    
        sender = sender.decode(encoding='ascii')
        recipients = recipients.decode(encoding='ascii').splitlines()  # A list is made.
        selected_package = selected_packages(user_id)
        for recipient in recipients:
            processed_fields = process_outgoing_sms(sender, user_id, recipient)  # Dict returns in proccessed fields.

        # Storing vaues to database

            S = Sms()  # Make instance of sms class 
            S.sms_type = 'outgoing'
            S.sms_from = processed_fields['sender_number']
            S.sms_to = recipient
            S.schedule_delivery_time = datetime.date.today()  # It should be delivered now
            S.validity_period = datetime.date.today()+datetime.timedelta(days=1)  # It is of one day
            S.timestamp = datetime.date.today()
            S.status = 'scheduled'
            S.msg_type = 'text'
            S.user_id = user_id
            S.package_name = selected_package['package_name']
            S.rates = selected_package['rates']
            S.target_network = processed_fields['target_network']  # process sms file would use it to send to respective network of which server is.
            S.client_type = 'smpp'
            DBSession.add(S)
            transaction.commit()
            sms = DBSession.query(Sms)[-1]  # Picks last record to send id to the client for ancilliary operations and querying.
            sms_ids = sms_ids + str(sms.id) + '\n'  # Server stores all sms ids. Server will notify client about the sms id of the message sent by client.
            if processed_fields['target_network'] != processed_fields['source_network']:  # If destination and source network is different 
                connect_info(recipient, message, processed_fields['target_network'], sms.id,
                             processed_fields['sender_number'])  # Connect to the destination's smpp server.
               
        return(sms_ids)

    def query_result(message_id, user_id):
        """
        This method is responsible to query database for provided message id to view the status of Sms and returns message state.
        """

        message_id = int(message_id.decode(encoding='ascii'))
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id, user_id=user_id).first()  # Check for all outgoing sms
        if(smses is None):
            return(command_status.ESME_RINVMSGID)
        elif(smses.status == 'scheduled' and smses.validity_period >= datetime.datetime.now()):
            return(dict(state=message_state.SCHEDULED, final_date=smses.validity_period))
        elif(smses.status == 'scheduled' and smses.validity_period < datetime.datetime.now()):
            return(dict(state=message_state.EXPIRED, final_date=smses.validity_period))
        elif(smses.status == 'delivered'):
            return(dict(state=message_state.DELIVERED, final_date=smses.validity_period))

    def cancel_result(message_id, user_id):
        """
        This method is responsible to cancel sending particular scheduled sms i-e if it is not yet delivered.
        """

        message_id = int(message_id.decode(encoding='ascii'))
        # This message id has been provided by user.
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id, user_id=user_id).first()
        if(smses is None):
            return False
        elif(smses.status == 'delivered'):
            return command_status.ESME_RCANCELFAIL  # Cancellation failed because message has been delievered.
        else:
            DBSession.delete(smses)  # Delete sms from database.
            transaction.commit()  # Commit in database.
            return True

    def replace_result(message_id, message, user_id):
        """
        This method is responsible to replace particular scheduled message i-e it is not yet delivered.
        """

        message_id = int(message_id.decode(encoding='ascii'))  # convert message if from byte to int.
        message = message.decode(encoding='ascii')
        # User id of logged in user.
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id, user_id=user_id).first()
        if(smses is None):
            return False  # No such sms.
        elif(smses.status == 'delievered'):
            return(command_status.ESME_RREPLACEFAIL)  # Relacement failed because message has been delivered.
        elif(smses.status == 'scheduled'):
            smses.schedule_delivery_time = datetime.datetime.now()  # It has be delivered now.
            smses. validity_period = datetime.datetime.now()+datetime.timedelta(days=1)  # Set validity period after replacement.
            smses.msg = message  # New message body in database.
            transaction.commit()  # Changes committed.
            return True


if __name__ == '__main__':
    #testing server
    S = SMPPServer()
    S.start_serving('127.0.0.1', 1337)

