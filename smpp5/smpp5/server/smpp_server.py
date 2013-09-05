"""
SMPP Server
"""

import time
import socket
import hashlib
import transaction
import multiprocessing
import datetime

from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, message_state

import db
from db import DBSession
from models import User, Sms, User_Number, Prefix_Match
from smpp5.server.database_file import Database


from smpp5.lib.session import SMPPSession


def handle_client_connection(conn, addr):
    """
    Handle a client connection
    """
    print("Accepted connection from: " + repr(addr))
    server_session = SMPPSession('server', conn)
    server_session.handle_bind(SMPPServer.validate)  # passing validate function name to handle_bind method to let the session instance call it 
    server_session.server_db_store = SMPPServer.db_storage
    server_session.server_query_result = SMPPServer.query_result
    server_session.server_cancel_result = SMPPServer.cancel_result
    server_session.server_replace_result = SMPPServer.replace_result
    server_session.close()
    time.sleep(5)
    conn.close()


class SMPPServer(object):
    '''
    Server class is responsible for recieving PDUs from client and decode them and also for sending encoded PDUs response
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

                P = multiprocessing.Process(target=handle_client_connection, args=(conn, addr))
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
        message = message.decode(encoding='ascii')
        user = DBSession.query(User_Number).filter_by(user_id=user_id).first()
        t_user = DBSession.query(Prefix_Match).filter_by(user_id=user_id).first()
        S = Sms()
        S.sms_type = 'outgoing'
        if(user is not None):
            S.sms_from = user.cell_number
        else:
            S.sms_from = t_user.prefix
        S.sms_to = recipient
        S.msg = message
        S.timestamp = datetime.datetime.now()
        S.status = 'scheduled'
        S.msg_type = 'text'
        S.user_id = user_id
        DBSession.add(S)
        transaction.commit()
        sms = DBSession.query(Sms)[-1]
        return(sms.id)

    def query_result(message_id):
        message_id = int(message_id.decode(encoding='ascii'))
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id).first()
        if(smses is None):
            return(command_status.ESME_RQUERYFAIL)
        elif(smses.status == 'scheduled'):
            return(message_state.SCHEDULED)
        elif(smses.status == 'delivered'):
            return(message_state.DELIVERED)

    def cancel_result(message_id):
        message_id = int(message_id.decode(encoding='ascii'))
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id, status='scheduled').first()
        if(smses is None):
            return False
        else:
            DBSession.delete(smses)
            transaction.commit()
            return True

    def replace_result(message_id, message):
        message_id = int(message_id.decode(encoding='ascii'))
        message = message.decode(encoding='ascii')
        smses = DBSession.query(Sms).filter_by(sms_type='outgoing', id=message_id, status='scheduled').first()
        if(smses is None):
            return False
        else:
            smses.msg = message
            transaction.commit()
            return True


if __name__ == '__main__':
    #testing server
    S = SMPPServer()
    S.start_serving('127.0.0.1', 1337)


