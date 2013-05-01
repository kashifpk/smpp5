import socket
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
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
            
    def recieve(self):
        '''This method is responsible for recieving response PDUs and decoding them'''
        pdu = self.conn.recv(1024)
        if(self.state=='BOUND_TX'): 
            P = BindTransceiverResp()
            P = BindTransceiverResp.decode(pdu)
            print("the response that is recieved and decoded is : "+hex_convert(P.encode(), 150))
            
    
            
    def Bindtransmitter(self):
        '''This method is specifically for Bind Transmitter which encode PDU and sent it to Server'''
        if self.state in ['CLOSED']:
            self.connection()
        if self.state in ['OPEN']:
            P = BindTransmitter() 
            P.system_id = CString("SMPP3TEST")
            P.password = CString("secret08")
            P.system_type = CString("SUBMIT1") 
            pdu = P.encode()
            self.conn.send(pdu)
            print("PDU that is encoded and sent to server is:  ")
            print(pdu)
            self.state = 'BOUND_TX'
            self.recieve()
           
        
if __name__ == '__main__':
    #Testing client
    client=Client()
    client.connection()
    client.Bindtransmitter()
    
    
    
            
