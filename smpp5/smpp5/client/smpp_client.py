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
    status = None

    def __init__(self):
        pass

    def connect(self, host, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.session = SMPPSession('client', self.socket)
            print("Connection established successfully\n")
            self.status = 'success'
        except:
            print("Connection Refused...Try Again\n")

    def disconnect(self):
        #TODO: close SMPPSession if not already closed
        self.socket.close()

    def login(self, mode, system_id, password, system_type):
        self.session.bind(mode, system_id, password, system_type)
        self.status = self.session.status
        #self.session.handle_response()

    def logout(self):
        if(self.status == 'success'):
            self.session.close()

    #def logoff(self):
        #self.session.unbind()
        #self.session.handle_unbind_response()
        #self.session.close_session()


if __name__ == '__main__':
    #Testing client
    client = SMPPClient()
    client.connect('127.0.0.1', 1337)
    client.login('TX', '3TEST', 'secret0', 'SUBMIT1')
    client.logout()
    client.disconnect()
