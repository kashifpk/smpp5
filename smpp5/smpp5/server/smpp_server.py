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
from models import User, Sms, User_Number, Prefix_Match, Packages, Selected_package
from smpp5.lib.session import SMPPSession


def handle_client_connection(conn, addr):
    """
    Handle a client connection
    """
    print("Accepted connection from: " + repr(addr))
    server_session = SMPPSession('server', conn)
    #server_session.server_fetch_incoming_smses = SMPPServer.fetch_incoming_sms
    server_session.server_db_store = SMPPServer.db_storage
    server_session.server_validate_method = SMPPServer.validate
    server_session.server_query_result = SMPPServer.query_result
    server_session.server_cancel_result = SMPPServer.cancel_result
    server_session.server_replace_result = SMPPServer.replace_result
    #SMPPServer.multithread(server_session)
    #server_session.server_fetch_incoming_smses = SMPPServer.fetch_incoming_sms
    background_thread = threading.Thread(target=handle_client_requests, args=(server_session, conn))
    background_thread.start()

    while server_session.state != 5:
        server_session.handle_pdu()
    conn.close()
    time.sleep(1)
    background_thread.join()


def handle_client_requests(server_session, conn):
    while conn.is_open is True:
        server_session.close()


def fetch_incoming_sms():
        try:
            sms = DBSession.query(Sms).filter_by(sms_type='incoming',).first()
            return(sms)
        except (KeyboardInterrupt, SystemExit):
            print("Good bye!")
            sys.exit()


class SMPPServer(object):
    '''
    Server class is responsible for recieving PDUs from client & decode them and also for sending encoded PDUs response
    '''

    def __init__(self):
        self.socket = None
        self.session = None

    def start_serving(self, host, port):
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
        recipient = recipient.decode(encoding='ascii')
        #message = message.decode(encoding='ascii')
        user = DBSession.query(User_Number).filter_by(user_id=user_id).first()
        t_user = DBSession.query(Prefix_Match).filter_by(user_id=user_id).first()
        total_selected_package = DBSession.query(Selected_package).filter_by(user_id=user_id).count()
        if(total_selected_package > 0):
            selected_package = DBSession.query(Selected_package).filter_by(user_id=user_id)[-1]
        else:
            selected_package = None
        S = Sms()
        S.sms_type = 'outgoing'
        if(user is not None):
                S.sms_from = user.cell_number
        else:
                S.sms_from = t_user.prefix
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
            end_date = selected_package.end_date.strftime('%d')
            end_month = selected_package.end_date.strftime('%m')
            date = datetime.datetime.now()
            today_date = date.strftime('%d')
            today_month = date.strftime('%m')
            if(end_month > today_month or end_date >= today_date and int(selected_package.smses) > 0):
                S.package_name = selected_package.package_name
                S.rates = 0.0
                selected_package.smses = selected_package.smses-1
            else:
                S.rates = 1.5

        DBSession.add(S)
        transaction.commit()
        sms = DBSession.query(Sms)[-1]
        return(sms.id)

    def query_result(message_id):
        message_id = int(message_id.decode(encoding='ascii'))
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id).first()
    # if 22 returns then no such message_id exist
        if(smses is None):
            return(command_status.ESME_RINVMSGID)
        elif(smses.status == 'scheduled' and smses.validity_period >= datetime.datetime.now()):
            return(dict(state=message_state.SCHEDULED, final_date=smses.validity_period))
        elif(smses.status == 'scheduled' and smses.validity_period < datetime.datetime.now()):
            return(dict(state=message_state.EXPIRED, final_date=smses.validity_period))
        elif(smses.status == 'delivered'):
            return(dict(state=message_state.DELIVERED, final_date=smses.validity_period))

    def cancel_result(message_id):
        message_id = int(message_id.decode(encoding='ascii'))
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id).first()
        if(smses is None):
            return False
        elif(smses.status == 'delivered'):
            return command_status.ESME_RCANCELFAIL
        else:
            DBSession.delete(smses)
            transaction.commit()
            return True

    def replace_result(message_id, message):
        message_id = int(message_id.decode(encoding='ascii'))
        message = message.decode(encoding='ascii')
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id).first()
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


# surah toba verses 128 and 129
