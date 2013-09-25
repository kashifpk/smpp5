import socket
from smpp5.lib.session import SMPPSession
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, message_state


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
            self.validation_status = self.session.validation_status
            if(self.validation_status != 'success'):
                print("Oops!!validation failed")

    def send_sms(self, recipient, message):
        if(self.conn_status == 'connected'):
            message_id = self.session.send_sms(recipient, message)
            if(message_id is not None):
                print("\nMessage id of Message U have just sent is  "+str(message_id) + "\n")

    def query_status(self, message_id):
        message_status = self.session.query_status(message_id)
        if(message_status == message_state.DELIVERED):
            print("\nYour Message having Message_id  "+str(message_id)+"  has been successfully Delievered\n")
        elif(message_status == message_state.SCHEDULED):
            print("\nYour Message having Message_id  "+str(message_id)+"  is scheduled and ready to deliever\n")
        else:
            print("\nSorry.....Try Again\n")

    def cancel_sms(self, message_id):
        cancel_status = self.session.cancel_sms(message_id)
        if(cancel_status is False):
            print("Message cancelling Failed Because Message has been already Delivered")
        else:
            print("Message with Message_id  "+str(message_id)+"  has been cancelled successfully")

    def replace_sms(self, message_id, message):
        replace_status = self.session.replace_sms(message_id, message)
        if(replace_status is False):
            print("Message replacement Failed Because Message has been already Delivered")
        else:
            print("Message with Message_id  "+str(message_id)+"  has been replaced successfully")

    def logout(self):
        if(self.conn_status == 'connected'):
            self.session.unbind()


if __name__ == '__main__':
    #Testing client
    client = SMPPClient()
    client.connect('127.0.0.1', 1337)
    client.login('TX', 'UFONE', 'secret08', 'SUBMIT3')
    client.send_sms('+923005381993', 'hello cutomers :-)')
    #client.query_status(1)
    #client.send_sms('+923005381993', 'hello to kiran :-)')
    #client.query_status(70)
    #client.query_status(15)
    #client.replace_sms(1, 'asma')
    #client.cancel_sms(107)
    client.logout()
    client.disconnect()
