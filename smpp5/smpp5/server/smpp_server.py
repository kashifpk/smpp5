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
    This method is responsible to Handle a client connection and creating two background threads...One for handling
    client request pdus and other for delivering smses to client..
    """

    print("Accepted connection from: " + repr(addr))
    server_session = SMPPSession('server', conn)
    server_session.server_db_store = SMPPServer.db_storage
    server_session.server_validate_method = SMPPServer.validate
    server_session.server_query_result = SMPPServer.query_result
    server_session.server_cancel_result = SMPPServer.cancel_result
    server_session.server_replace_result = SMPPServer.replace_result
    server_session.sever_fetch_sms = fetch_incoming_sms
    server_session.commit_db = commit_db

    # background thread 1 to handle clients request pdus by recieving them from socket and storing them in dictionary
    background_thread = threading.Thread(target=handle_client_requests, args=(server_session, conn))
    background_thread.start()

    # background thread 2 to check database for messages after every 5secs and deliever smses to client if any

    background_thread2 = threading.Thread(target=deliver_sms, args=(server_session, conn))
    background_thread2.start()

    # background thread 3 to process incoming smses after login
    # current thread for receiving responses from client and storing them in dict
    while server_session.state != SessionState.UNBOUND:
        server_session.handle_pdu()

    conn.close()
    #time.sleep(1)
    background_thread.join()
    background_thread2.join()


def handle_client_requests(server_session, conn):
    """
    This method handles client request/response pdus by receiving them from socket and storing them in dictionary
    till Unbound state.
    """

    while conn.is_open is True:
        server_session.process_request()


def deliver_sms(server_session, conn):
    """
    This method checks database for smses every 5 seconds and deliver sms to client if any.
    """
    while conn.is_open is True:
        if server_session.state in [SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            time.sleep(5)
            server_session.deliver_sms()
            transaction.commit()


def fetch_incoming_sms(user_id):
    """
    This method query database to retrieve pending incoming smses for logged in client..
    """

    smses = DBSession.query(Sms).filter_by(sms_type='incoming', user_id=user_id, status='recieved').first()
    if smses:
        smses.status = 'delivered'
    return(smses)


def thread_4_incoming_sms():
    while True:
        process_incoming_sms()
        transaction.commit()
        time.sleep(5)


def process_incoming_sms():
    """
    This method is responsible for processing incoming smses
    """

    smses = DBSession.query(Sms).filter_by(sms_type='incoming', status='recieved', target_network=None, user_id=None).all()
    if smses:
        for S in smses:
            sms_to = S.sms_to
            sms_from = S.sms_from
            mnp = DBSession.query(Mnp).filter_by(cell_number=sms_to).first()  # querying for mobile number conversion
            if mnp:
                target_network = mnp.target_network
                S.sms_type = 'outgoing'
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
                    S.validity_period = datetime.date.today()+datetime.timedelta(days=1)
            S.target_network = target_network
            if target_network != source_network:
                connect_info(sms_to, S.msg, dest_network, S.id, sms_from)


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
        # Hard coded values to check.....
        #system_id = 'KIRAN'
        #password = 'secret08'
        #system_type = 'SUBMIT1'
        #ip = '127.0.0.3'
        #port = 1339
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

    if client.login():
        client.session.send_sms(recipient, message, sender_number)
        while notification == 0:
            notification = client.session.notifications_4_client()
        client.session.processing_recieved_pdus()
        smses = DBSession.query(Sms).filter_by(id=sms_id).first()
        smses.status = 'delivered'
        commit_db()
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
        date = datetime.datetime.now()
        today_date = int(date.strftime('%d'))
        today_month = int(date.strftime('%m'))
        if(end_month > today_month and int(selected_package.smses) > 0):  # check if package is expired
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
                print("listening......")
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

        sms_ids = ''
        sender = sender.decode(encoding='ascii')
        recipients = recipients.decode(encoding='ascii').splitlines()
        selected_package = selected_packages(user_id)
        for i in range(len(recipients)):
            recipient = recipients[i]
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
            # storing to database
            DBSession.add(S)
            sms = DBSession.query(Sms)[-1]  # to send id to the client for ancilliary operations and querying.
            sms_ids = sms_ids + str(sms.id) + '\n'
            if processed_fields['target_network'] != processed_fields['source_network']:  # if destination and source network is different 
                connect_info(recipient, message, processed_fields['target_network'], sms.id,
                             processed_fields['sender_number'])  # connect to the destination's smpp server.
        transaction.commit()
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
    S.start_serving('192.168.1.3', 1337)

