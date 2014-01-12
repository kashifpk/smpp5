import socket
from smpp5.lib.session import SMPPSession, SessionState
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, message_state
from smpp5.lib.session.shared_connection import SharedConnection
import time


# Note: This whole module seems mostly unnecessary. We either need this or client_cli module, not both.
# We can keep this one but should remove most of the methods here as they are implemented in session

class SMPPClient(object):
    '''
    Client Class is responsible to encode PDUs and send them to Server and also decode the response get from Server
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
        ret = False
        if SessionState.OPEN == self.session.state:
            self.session.bind(self.bind_mode, self.system_id, self.password, self.system_type)
            time.sleep(2)  # waiting for response for login because other actions can't be performed without login.
            self.session.processing_recieved_pdus()  # read pdu from dictionary, and change the status accordingly if ack is positive.
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
