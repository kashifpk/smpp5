import socket
from smpp5.lib.session import SMPPSession, SessionState
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, message_state
from smpp5.client.cli_background_thread import client_thread
from smpp5.client import cli_background_thread
from smpp5.lib.session.shared_connection import SharedConnection
import time


class SMPPClient(object):

    ip = None
    port = None
    system_id = None
    password = None
    system_type = None
    bind_mode = None
    session = None
    sc = None

    def __init__(self, ip, port, bind_mode, system_id, password, system_type):
        "This constructor is responsible for initializing the credentials got via parameters."
        self.ip = ip
        self.port = port
        self.bind_mode = bind_mode
        self.system_id = system_id
        self.password = password
        self.system_type = system_type

    def connect(self):
        "This method is responsible for creating the socket, connecting to it, passing socket object to shared connection class, and passing shared connection class object to session  "
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            self.sc = SharedConnection(self.socket)
            self.sc.is_open = True
            self.session = SMPPSession('client', self.sc)
        except:
            return False

        return True

    def login(self):
        "This method is responsible for binding the client with session on the basis of state of session, if state of session is open, client binds with session via credentials."
        ret = False
        if SessionState.OPEN == self.session.state:
            self.session.bind(self.bind_mode, self.system_id, self.password, self.system_type)
            time.sleep(1)
            self.session.processing_recieved_pdus()
            if self.session.state in [SessionState.BOUND_RX, SessionState.BOUND_TX, SessionState.BOUND_TRX]:
                return True

        return ret


if __name__ == '__main__':
    pass
    #Testing client
    #client = SMPPClient()
    #client.connect('127.0.0.1', 1337)
    #client.login('TX', 'UFONE', 'secret08', 'SUBMIT3')
    #client.send_sms('+923005381993', 'hello cutomers :-)')
    #client.query_status(1)
    #client.send_sms('+923005381993', 'hello to kiran :-)')
    #client.query_status(70)
    #client.query_status(15)
    #client.replace_sms(1, 'asma')
    #client.cancel_sms(107)
    #client.logout()
    #client.disconnect()
