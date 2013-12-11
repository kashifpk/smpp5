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
    till Unbound state
    """

    while conn.is_open is True:
        server_session.process_request()


def deliver_sms(server_session, conn):
    """
    This method checks database for smses every 5 seconds and deliver sms to client if any
    """
    while conn.is_open is True:
        if server_session.state in [SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            time.sleep(5)
            server_session.deliver_sms()


def fetch_incoming_sms(user_id):
    """
    This method query database to retrieve pending incoming smses for logged in client..
    """

    smses = DBSession.query(Sms).filter_by(sms_type='incoming', user_id=user_id, status='received').first()
    sms = smses
    if smses:
        smses.status = 'delivered'
    return(smses)


def commit_db():
    """
    This method is used to commit database transaction
    """

    transaction.commit()


def connect_info(recipient, message, dest_network, sms_id):
    """
    This method is responsible to get connection paramters from database to communicate with destination network
    server in case when sender sends a message to some other network.
    """

    # here we have to make client object
    server = DBSession.query(Network).filter_by(network=dest_network).first()
    if server:
        username = server.username
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
                                                    sms_id))
        background_thread3.start()
        background_thread3.join()


def connect_to_server(ip, port, system_id, password, system_type, recipient, message, sms_id):
    """
    This method is tesponsible to create client instance to communicate with destination network server as client.
    """

    client = SMPPClient(ip, port, 'TX', system_id, password, system_type)
    connection = False
    notification = 0
    while connection is False:   # while connection is not established with server, try to connect.
        if client.connect():
            connection = True
            background_thread4 = threading.Thread(target=client.session.storing_recieved_pdus, args=())
            background_thread4.start()

    if client.login():
        client.session.send_sms(recipient, message)
        while notification == 0:
            notification = client.session.notifications_4_client()
        client.session.processing_recieved_pdus()
        smses = DBSession.query(Sms).filter_by(id=sms_id).first()
        smses.status = 'delivered'
    client.sc.close()
    commit_db()
    background_thread4.join()


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

        db.bind_session()
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

    def db_storage(recipient, message, user_id):
        """
        This method is responsible to store Sms and related fields provided by client in database
        """

        recipient = recipient.decode(encoding='ascii')  # recipient refers to destination address
        user = DBSession.query(User_Number).filter_by(user_id=user_id).first()  # user refers to normal user
        cell_number = user.cell_number  # cell number of sender
        source_prefix = cell_number[0:6]  # extract prefix of sender number
        dest_prefix = recipient[0:6]  # extract prefix of recipient
        s_network = DBSession.query(Prefix_Match).filter_by(prefix=source_prefix).first()
        source_network = s_network.network  # refers to sender network
        d_network = DBSession.query(Prefix_Match).filter_by(prefix=dest_prefix).first()
        dest_network = d_network.network   # refers to recipient network
        if(source_network == dest_network):
            mnp = DBSession.query(Mnp).filter_by(cell_number=recipient).first()
            if mnp:
                target_network = mnp.target_network
            else:
                target_network = dest_network
        else:
            target_network = dest_network

        # Now check if logged in user selected any package
        total_selected_package = DBSession.query(Selected_package).filter_by(user_id=user_id).count()
        if(total_selected_package > 0):
            selected_package = DBSession.query(Selected_package).filter_by(user_id=user_id)[-1]  # retrieve last selected package
        else:
            selected_package = None
        S = Sms()
        S.sms_type = 'outgoing'
        S.sms_from = cell_number
        S.sms_to = recipient
        S.schedule_delivery_time = datetime.date.today()
        S.validity_period = datetime.date.today()+datetime.timedelta(days=1)
        S.msg = message
        S.timestamp = datetime.date.today()
        S.status = 'scheduled'
        S.msg_type = 'text'
        S.user_id = user_id
        if(selected_package is None):
            S.package_name = None
            S.rates = 1.5
        else:
            end_date = int(selected_package.end_date.strftime('%d'))
            end_month = int(selected_package.end_date.strftime('%m'))
            date = datetime.datetime.now()
            today_date = int(date.strftime('%d'))
            today_month = int(date.strftime('%m'))
            if(end_month > today_month and int(selected_package.smses) > 0):  # check if package is expired
                S.package_name = selected_package.package_name
                S.rates = 0.0
                selected_package.smses = selected_package.smses-1
            elif(end_month == today_month):
                if(end_date >= today_date and int(selected_package.smses) > 0):
                    S.package_name = selected_package.package_name
                    S.rates = 0.0
                    selected_package.smses = selected_package.smses-1
            else:
                S.package_name = None
                S.rates = 1.5
        S.target_network = target_network
        # storing to database
        DBSession.add(S)
        transaction.commit()
        sms = DBSession.query(Sms)[-1]
        if target_network != source_network:
            connect_info(recipient, message, dest_network, sms.id)
        return(sms.id)

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
    S.start_serving('127.0.0.1', 1337)

