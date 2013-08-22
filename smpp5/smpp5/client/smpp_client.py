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
    validation_status = None
    conn_status = 'noconn'

    def __init__(self):
        pass

    def connect(self, host, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.session = SMPPSession('client', self.socket)
            print("Connection established successfully\n")
            self.conn_status = 'connected'
        except:
            print("Connection Refused...Try Again\n")

    def disconnect(self):
        #TODO: close SMPPSession if not already closed
        if(self.conn_status == 'connected'):
            self.socket.close()

    def login(self, mode, system_id, password, system_type):
        if(self.conn_status == 'connected'):
            self.session.bind(mode, system_id, password, system_type)
            self.validation_status = self.session.status
            if(self.validation_status != 'success'):
                print("Oops!!validation failed")
        #self.session.handle_response()

    def send_sms(self, recipient, message, system_id):
        if(self.conn_status == 'connected'):
            message_id = self.session.send_sms(recipient, message, system_id)
            print("Message id of Message U have just sent is "+message_id)

    def query_status(self, message_id):
        self.session.query_status(message_id)

    def logout(self):
        if(self.conn_status == 'connected'):
            self.session.close()

    #def logoff(self):
        #self.session.unbind()
        #self.session.handle_unbind_response()
        #self.session.close_session()


if __name__ == '__main__':
    #Testing client
    client = SMPPClient()
    client.connect('127.0.0.1', 1337)
    client.login('TX', '3TEST', 'secret08', 'SUBMIT1')
    client.send_sms('+923005381993', 'hello from asma project yessssss :-)', '3TEST')
    client.logout()
    client.disconnect()
