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
    
    # To use server class variable values in session module, return values have been passed.
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
    while True:
        process_incoming_sms()
        transaction.commit()
        #updating_status(sms_ids)
        time.sleep(5)


def process_incoming_sms():
    """
    This method is responsible for processing incoming smses.
    """

    sms_ids = ''
    smses = DBSession.query(Sms).filter_by(sms_type='incoming', status='recieved', target_network=None, user_id=None).all()
    if smses:
        for S in smses:
            sms_to = S.sms_to
            sms_from = S.sms_from
            mnp = DBSession.query(Mnp).filter_by(cell_number=sms_to).first()  # querying for mobile number conversion
            if mnp:
                target_network = mnp.target_network
                S.sms_type = 'outgoing'
                S.status = 'scheduled'
                S.validity_period = datetime.date.today()+datetime.timedelta(days=1)
            else:
                source_prefix = sms_from[0:6]  # extract prefix of sender number
                dest_prefix = sms_to[0:6]  # extract prefix of recipient
                s_network = DBSession.query(Prefix_Match).filter_by(prefix=source_prefix).first()
                source_network = s_network.network  # refers to sender network, getting the network of source from prefixes
                d_network = DBSession.query(Prefix_Match).filter_by(prefix=dest_prefix).first()
                dest_network = d_network.network   # refers to recipient network
                user = DBSession.query(User_Number).filter_by(cell_number=sms_to).first()  # user refers to normal user
                if user:
                    S.user_id = user.user_id
                    target_network = None
                else:
                    target_network = dest_network
                    S.sms_type = 'outgoing'
                    S.status = 'scheduled'
                    S.validity_period = datetime.date.today()+datetime.timedelta(days=1)
            S.target_network = target_network
            if target_network != source_network:
                connect_info(sms_to, S.msg, dest_network, S.id, sms_from)
                #sms_ids = sms_ids + str(S.id) + '\n'
        #return sms_ids


def updating_status(sms_ids):
    """
    This method is responsible to update status of messages from scheduled to delivered when messages are for server of
    other network.
    """

    if sms_ids:
        sms_ids = sms_ids.splitlines()
        print(sms_ids)
        for sms_id in sms_ids:
            smses = DBSession.query(Sms).filter_by(id=int(sms_id)).first()
            smses.status = 'delivered'
        transaction.commit()


def process_outgoing_sms(sender, user_id, recipient):
    """
    This method is responsible for processing outgoing smses.
    """
    if sender is not '':
            sender_number = sender
    else:
        user = DBSession.query(User_Number).filter_by(user_id=user_id).first()  # user refers to normal user
        sender_number = user.cell_number  # cell number of sender
    source_prefix = sender_number[0:6]  # extract prefix of sender number
    s_network = DBSession.query(Prefix_Match).filter_by(prefix=source_prefix).first()
    source_network = s_network.network  # refers to sender network, getting the network of source from prefixes
    dest_prefix = recipient[0:6]  # extract prefix of recipient
    d_network = DBSession.query(Prefix_Match).filter_by(prefix=dest_prefix).first()
    dest_network = d_network.network   # refers to recipient network
    mnp = DBSession.query(Mnp).filter_by(cell_number=recipient).first()  # querying for mobile number conversion
    if mnp:
        target_network = mnp.target_network
    elif(source_network == dest_network):
        target_network = dest_network
    else:
        target_network = dest_network
    return(dict(sender_number=sender_number, source_network=source_network, target_network=target_network))


def commit_db():
    """
    This method is used to commit database transaction
    """

    transaction.commit()


def connect_info(recipient, message, dest_network, sms_id, sender_number):
    """
    This method is responsible to get connection paramters from database to communicate with destination network
    server in case when sender sends a message to some other network.
    """

    # here we have to make client object
    server = DBSession.query(Network).filter_by(network=dest_network).first()
    if server:
        system_id = server.username
        password = server.password
        system_type = server.system_type
        ip = server.ip
        port = server.port

        background_thread3 = threading.Thread(target=connect_to_server,
                                              args=(ip, port, system_id, password, system_type, recipient, message,
                                                    sms_id, sender_number))
        background_thread3.start()
        background_thread3.join()


def connect_to_server(ip, port, system_id, password, system_type, recipient, message, sms_id, sender_number):
    """
    This method is responsible to create client instance to communicate with destination network server as client.
    """

    client = SMPPClient(ip, port, 'TX', system_id, password, system_type)
    connection = False
    notification = 0
    while connection is False:   # while connection is not established with server, try to connect.
        if client.connect():
            connection = True
            # this thread is checking the socket for getting responses from other server and save in dictionary.
            background_thread4 = threading.Thread(target=client.session.storing_recieved_pdus, args=())  # to recieve pdu response from other smpp server to whom it has sent the request.
            background_thread4.start()

    if client.login():  # if client successfully logins
        client.session.send_sms(recipient, message, sender_number)
        while notification == 0:
            notification = client.session.notifications_4_client()
        client.session.processing_recieved_pdus()
    smses = DBSession.query(Sms).filter_by(id=int(sms_id)).first()
    if smses:
        smses.status = 'delivered'
        transaction.commit()
    client.session.unbind()
    while client.session.state != SessionState.UNBOUND:
        client.session.processing_recieved_pdus()
    client.sc.close()
    background_thread4.join()


def selected_packages(user_id):
    """
    This method is used by server to ensure if logged in user has selected any package or not.
    """

    total_selected_package = DBSession.query(Selected_package).filter_by(user_id=user_id).count()
    if(total_selected_package > 0):
        selected_package = DBSession.query(Selected_package).filter_by(user_id=user_id)[-1]  # retrieve last selected package
    else:
        selected_package = None
    if(selected_package is None):
            package_name = None
            rates = 1.5
    else:
        end_date = int(selected_package.end_date.strftime('%d'))
        end_month = int(selected_package.end_date.strftime('%m'))
        end_year = int(selected_package.end_date.strftime('%y'))
        date = datetime.datetime.now()
        today_date = int(date.strftime('%d'))
        today_month = int(date.strftime('%m'))
        today_year = int(date.strftime('%y'))
        if(end_year > today_year and int(selected_package.smses) > 0):
            package_name = selected_package.package_name
            rates = 0.0
            selected_package.smses = selected_package.smses-1
        elif(end_year == today_year and end_month > today_month and int(selected_package.smses) > 0):
            package_name = selected_package.package_name
            rates = 0.0
            selected_package.smses = selected_package.smses-1
        elif(end_month == today_month):
            if(end_date >= today_date and int(selected_package.smses) > 0):
                package_name = selected_package.package_name
                rates = 0.0
                selected_package.smses = selected_package.smses-1
        else:
            package_name = None
            rates = 1.5
    return(dict(package_name=package_name, rates=rates))


class SMPPServer(object):
    '''
    Server class is responsible for performing database related activities as requested by client like retrieving,
    deleting, updating database etc
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

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))  # built-in method
        db.bind_session()
        background_thread1 = threading.Thread(target=thread_4_incoming_sms, args=())
        background_thread1.start()

        try:
            while True:
                self.socket.listen(1)  # listening for connections
                print("Ufone server listening......")
                conn, addr = self.socket.accept()  # accept connections and return ip and port
                sc = SharedConnection(conn)
                sc.is_open = True

                P = multiprocessing.Process(target=handle_client_connection, args=(sc, addr))
                P.start()

                active_conns = multiprocessing.active_children()
                print("Active connections: %i" % len(active_conns))

        except (KeyboardInterrupt, SystemExit):
            print("Good bye!")

    def validate(system_id, password, system_type):
        """
        This method is used by server to validate credentials provided by client against database
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
        This method is responsible to store Sms and related fields provided by client in database
        """

        sms_ids = ''    # contains all message ids that are sended by client to recipient of same or different network.
        #smses_ids = ''  # contains only message ids that are sended by client to recipient of some other network.
        sender = sender.decode(encoding='ascii')
        recipients = recipients.decode(encoding='ascii').splitlines()
        selected_package = selected_packages(user_id)
        for recipient in recipients:
            processed_fields = process_outgoing_sms(sender, user_id, recipient)

        # storing vaues to database

            S = Sms()
            S.sms_type = 'outgoing'
            S.sms_from = processed_fields['sender_number']
            S.sms_to = recipient
            S.schedule_delivery_time = datetime.date.today()
            S.validity_period = datetime.date.today()+datetime.timedelta(days=1)
            S.msg = message
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
            sms = DBSession.query(Sms)[-1]  # to send id to the client for ancilliary operations and querying.
            sms_ids = sms_ids + str(sms.id) + '\n'
            if processed_fields['target_network'] != processed_fields['source_network']:  # if destination and source network is different 
                connect_info(recipient, message, processed_fields['target_network'], sms.id,
                             processed_fields['sender_number'])  # connect to the destination's smpp server.
                #smses_ids = smses_ids + str(s) + '\n'
        #updating_status(smses_ids)
        return(sms_ids)

    def query_result(message_id, user_id):
        """
        This method is responsible to query database for provided message id to view the status of Sms
        """

        message_id = int(message_id.decode(encoding='ascii'))
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id, user_id=user_id).first()  #check for all outgoing sms
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
        This method is responsible to cancel sending particular sms if it is not yet delivered.
        """

        message_id = int(message_id.decode(encoding='ascii'))
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id, user_id=user_id).first()
        if(smses is None):
            return False
        elif(smses.status == 'delivered'):
            return command_status.ESME_RCANCELFAIL
        else:
            DBSession.delete(smses)
            transaction.commit()
            return True

    def replace_result(message_id, message, user_id):
        """
        This method is responsible to replace particular message which is not yet delivered.
        """

        message_id = int(message_id.decode(encoding='ascii'))
        message = message.decode(encoding='ascii')
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id, user_id=user_id).first()
        if(smses is None):
            return False
        elif(smses.status == 'delievered'):
            return(command_status.ESME_RREPLACEFAIL)
        elif(smses.status == 'scheduled'):
            smses.schedule_delivery_time = datetime.datetime.now()
            smses. validity_period = datetime.datetime.now()+datetime.timedelta(days=1)
            smses.msg = message
            transaction.commit()
            return True


if __name__ == '__main__':
    #testing server
    S = SMPPServer()
    S.start_serving('192.168.5.35', 1337)

