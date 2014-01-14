import socket
from smpp5.lib.session import SMPPSession, SessionState
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, message_state
from smpp5.lib.session.shared_connection import SharedConnection
import time


class SMPPClient(object):
    '''
    Client Class is responsible to send request to session to compose pdus. It just calls desired method in session.
    '''

    ip = None
    port = None
    system_id = None
    password = None
    system_type = None
    bind_mode = None
    session = None
    sc = None

    def __init__(self, ip, port, bind_mode, system_id, password, system_type):
        self.ip = ip
        self.port = port
        self.bind_mode = bind_mode
        self.system_id = system_id
        self.password = password
        self.system_type = system_type

    def connect(self):
        'Socket is created and passed to shared connection class object. Session class object has been created and called.'
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket created
            self.socket.connect((self.ip, self.port))  # Socket connected with the server via ip and port.
            self.sc = SharedConnection(self.socket)
            self.sc.is_open = True
            self.session = SMPPSession('client', self.sc)
        except:
            return False

        return True

    def login(self):
        ret = False
        if SessionState.OPEN == self.session.state:  # Check if session state is open
            self.session.bind(self.bind_mode, self.system_id, self.password, self.system_type)  # Bind with server via session method bind.
            time.sleep(2)  # Waiting for response of server for login because other actions can't be performed without login.
            self.session.processing_recieved_pdus()  # read pdu from dictionary, and change the status of pdu command status field accordingly if ack is positive.
            if self.session.state in [SessionState.BOUND_RX, SessionState.BOUND_TX, SessionState.BOUND_TRX]:
                return True  # Bind successful 

        return ret  # Bind failed because false has been returned


if __name__ == '__main__':
    pass
