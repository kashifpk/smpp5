import time
import socket
from smpp5.lib.session import SMPPSession


class SMPPClient(object):
    '''
    Client Class is responsible to encode PDUs and send them to Server and also decode the response get from Server
    '''

    ip = None
    port = None
    system_id = None
    password = None
    system_type = None
    session = None

    def __init__(self):
        pass

    def connect(self, host, port):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.session = SMPPSession('client', self.socket)

    def disconnect(self):
        #TODO: close SMPPSession if not already closed
        self.session.close()
        self.socket.close()
        

    def login(self, mode, system_id, password, system_type):
        self.session.bind(mode, system_id, password, system_type)
        self.session.handle_response()

    def logoff(self):
        self.session.unbind()
        #self.session.handle_unbind_response()
        #self.session.close_session()
        time.sleep(1)


if __name__ == '__main__':
    #Testing client
    client = SMPPClient()
    client.connect('127.0.0.1', 1337)
    client.login('TX', '3TEST', 'secret08', 'SUBMIT1')
    client.logoff()
    client.disconnect()
