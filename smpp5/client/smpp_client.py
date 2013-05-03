import socket
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.constants import *
from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.pdu.session_management import BindTransmitter, BindTransmitterResp, BindReceiver, BindReceiverResp, BindTransceiver, BindTransceiverResp, OutBind, UnBind, UnBindResp, EnquireLink, EnquireLinkResp, AlertNotification, GenericNack
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, esm_class, command_id, command_status, tlv_tag

class Client(object):
    '''Client Class is responsible to encode PDUs and send them to Server and also decode the response get from Server'''
    state=''
    conn=''
    PORT=''
    def __init__(self):
        self.state = 'CLOSED'
        self.conn = None
        #self.HOST = '127.0.0.1' 
        self.PORT = 50007
        
    def connection(self):
        '''This method is responsible for creating socket and connecting to server'''
        if self.state in ['CLOSED']:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((socket.gethostname(), self.PORT))
            self.state = 'OPEN'
            
    def disconnection(self,):
        if self.state in ['BOUND_TX', 'BOUND_RX', 'BOUND_TRX']:
            self.Unbind()
            self.state='OPEN'
            self.conn.close()
            self.state = 'CLOSED'
    
            
    def recieve(self):
        '''This method is responsible for recieving response PDUs and decoding them'''
        pdu = self.conn.recv(1024)
        P= ''
        if(self.state=='BOUND_TX'): 
            P = BindTransceiverResp()
            P = BindTransceiverResp.decode(pdu)
            #print("the response that is recieved and decoded is : "+hex_convert(P.encode(), 150))
            
        elif(self.state=='BOUND_RX'): 
            P = BindReceiverResp()
            P = BindReceiverResp.decode(pdu)
            #print("the response that is recieved and decoded is : "+hex_convert(P.encode(), 150))
            
        elif(self.state=='BOUND_TRX'): 
            P = BindTransceiverResp()
            P = BindTransceiverResp.decode(pdu)
            #print("the response that is recieved and decoded is : "+hex_convert(P.encode(), 150))
            
        elif(self.state=='UNBIND'): 
            P = UnBindResp()
            P = UnBindResp.decode(pdu)
        print("the response that is recieved and decoded is : "+hex_convert(P.encode(), 150))
            
               
    def Bindtransmitter(self):
        '''This method is specifically for Bind Transmitter which encode this PDU and sent it to Server'''
        if self.state in ['CLOSED']:
            self.connection()
        if self.state in ['OPEN', 'BOUND_RX', 'BOUND_TRX']:
            P = BindTransmitter() 
            P.system_id = CString("SMPP3TEST")
            P.password = CString("secret08")
            P.system_type = CString("SUBMIT1") 
            pdu = P.encode()
            self.conn.send(pdu)
            print("****************BIND TRANSMITTER*********************** ")
            print("PDU that is encoded and sent to server is:  ")
            print(pdu)
            self.state = 'BOUND_TX'
            self.recieve()
            print()
            
    def Bindreceiver(self):
        '''This method is specifically for Bind Receiver which encode this PDU and sent it to Server'''
        if self.state in ['CLOSED']:
            self.connection()
        if self.state in ['OPEN', 'BOUND_TX', 'BOUND_TRX']:
            P = BindReceiver()
            P.system_id = CString("SMPP3TEST")
            P.password = CString("secret08")
            P.system_type = CString("SUBMIT1")
            pdu = P.encode()
            self.conn.send(pdu)
            print("******************BIND RECEIVER*************************  ")
            print("PDU that is encoded and sent to server is:  ")
            print(pdu)
            self.state = 'BOUND_RX'
            self.recieve()
            print()
            
    def Bindtransceiver(self):
        '''This method is specifically for Bind Transceiver which encode this PDU and sent it to Server'''
        if self.state in ['CLOSED']:
            self.connection()
        elif self.state in ['OPEN', 'BOUND_TX', 'BOUND_RX']:
            P = BindTransceiver()
            P.system_id = CString("SMPP3TEST")
            P.password = CString("secret08")
            P.system_type = CString("SUBMIT1")
            pdu = P.encode()
            self.conn.send(pdu)
            print("******************BIND TRANSCEIVER************************ ")
            print("PDU that is encoded and sent to server is:  ")
            print(pdu)
            print()
            self.state = 'BOUND_TRX'
            self.recieve()
            print()
            
    def Unbind(self):
        ''' this method is for sending UNBIND PDU to server by encoding it'''
        if self.state in ['CLOSED']:
            self.connection()
        elif self.state in ['BOUND_TX', 'BOUND_RX', 'BOUND_TRX']:
            P = UnBind()
            pdu = P.encode()
            self.conn.send(pdu)
            print("****************UNBIND************************ ")
            print("PDU that is encoded and sent to server is:  ")
            print(pdu)
            print()
            self.state = 'UNBIND'
            self.recieve()
            
        pass
    
            
           
        
if __name__ == '__main__':
    #Testing client
    client=Client()
    client.connection()
    client.Bindtransmitter() 
    client.Bindreceiver()
    client.Bindtransceiver()
    client.disconnection()
    
    
    
            
