import socket
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.constants import *
from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.pdu.session_management import BindTransmitter, BindTransmitterResp, BindReceiver, BindReceiverResp, BindTransceiver, BindTransceiverResp, OutBind, UnBind, UnBindResp, EnquireLink, EnquireLinkResp, AlertNotification, GenericNack
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.pdu.login_check import LoginInfo
from smpp5.lib.constants import NPI, TON, esm_class, command_id, command_status, tlv_tag



class Client(object):
    '''Client Class is responsible to encode PDUs and send them to Server and also decode the response get from Server'''
    state=''
    conn=''
    PORT=''
    bind_pdu = ''
    seq_num = 0
    smpplogin= LoginInfo()
    def __init__(self):
        self.state = 'CLOSED'
        self.conn = None
        #self.HOST = '127.0.0.1' 
        self.PORT = 50007
        self.sequence_inc()
        
        
    def connection(self):
        '''This method is responsible for creating socket and connecting to server'''
        if self.state in ['CLOSED']:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((socket.gethostname(), self.PORT))
            self.state = 'OPEN'
            
    def disconnection(self):
        '''This method is responsible for ending session by calling Unbind PDU'''
        print("*************Disconnecting The Session***************************")
        if self.state in ['BOUND_TX', 'BOUND_RX', 'BOUND_TRX']:
            self.Unbind()
            self.state='OPEN'
            self.state = 'CLOSED'
            self.conn.close()
            
    def sequence_inc(self):
        self.seq_num=self.seq_num+1
            
            
    def recieve(self):
        '''This method is responsible for recieving response PDUs and decoding them'''
        length = self.conn.recv(4)
        while len(length) < 4:
            #time.sleep(1)   # if bytes received from client are less than 4
            length += self.conn.recv(4-len(length))
        pdu_length = Integer.decode(length).value
        pdu_str = length
        while len(pdu_str) != pdu_length:
            pdu_str += self.conn.recv(pdu_length-len(pdu_str))
        print()
        P = PDU.decode(pdu_str)
        print("the response that is recieved and decoded is : "+hex_convert(P.encode(), 150))
        
    def send_pdu(self,pdu):
        '''This method is responsible for sending encoded Bind PDUs'''
        self.conn.send(pdu)
        print("PDU that is encoded and sent to server is:  ")
        print(pdu)
        if(self.bind_pdu == 'BindTransmitter'):
         self.state = 'BOUND_TX'
        elif(self.bind_pdu == 'BindReceiver'):
         self.state = 'BOUND_RX'
        elif(self.bind_pdu == 'BindTransceiver'):
         self.state = 'BOUND_TRX'
        
            
    def bind(self, bind_type, system_id, password, system_type):
        ''' This method is responsible for getting parameters from user and encode required bind PDU'''
        if self.state in ['CLOSED']:
            self.connection()
        print("****************"+bind_type+"*********************** ")
        pdu_name = bind_type
        pdu_name = eval(pdu_name)
        P = pdu_name()
        P.sequence_number = Integer(self.seq_num,4)
        P.system_id = CString(system_id)
        P.password = CString(password)
        P.system_type = CString(system_type)
        self.bind_pdu = bind_type
        pdu = P.encode()
        self.send_pdu(pdu)
        if(self.state in ['BOUND_TX','BOUND_RX', 'BOUND_TRX']):
         if(self.smpplogin.logged_in=='true'):
            print()
            print("Successfully login")
            print()
         else:
            print("Oops! Login Failed.....")
        self.recieve()
        self.sequence_inc()
        
            
    def Unbind(self):
        ''' this method is for sending UNBIND PDU to server by encoding it'''
        if self.state in ['CLOSED']:
            self.connection()
        elif self.state in ['BOUND_TX', 'BOUND_RX', 'BOUND_TRX']:
            P = UnBind()
            P.sequence_number = Integer(self.seq_num,4)
            pdu = P.encode()
            self.send_pdu(pdu)
            self.recieve()
            self.state = 'UNBIND'
            self.sequence_inc()
                  
        
if __name__ == '__main__':
    #Testing client
    client=Client()
    client.connection()
    client.bind('BindTransceiver','SMPP3TEST','secret08','SUBMIT1') 
    #client.Bindreceiver()
    #client.Bindtransceiver()
    #client.Unbind()
    client.disconnection()
    
    
    
            
