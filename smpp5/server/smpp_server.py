import socket
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.constants import *
from smpp5.lib.pdu.session_management import BindTransmitter, BindTransmitterResp, BindReceiver, BindReceiverResp, BindTransceiver, BindTransceiverResp, OutBind, UnBind, UnBindResp, EnquireLink, EnquireLinkResp, AlertNotification, GenericNack
from smpp5.lib.pdu.pdu import PDU

class Server(object):
    '''Server class is responsible for recieving PDUs from client and decode them and also for sending encoded PDUs response'''
   
    status='CLOSED'
    decode_pdu='' 
    PORT = 50007

    def __init__(self):
   
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), self.PORT))
        self.server.listen(1)
        print(b'Server is listening')
        self.conn, addr = self.server.accept()
        print('Connected by' + str(addr))
        decode_pdu = self.receive()         #calling recieve method
        resp_pdu = self.send_resp()           #calling send_resp method
        self.conn.sendall(resp_pdu)
        print("Response encoded and sent to Client is: ")
        print(resp_pdu)
        self.conn.close()
        
    def receive(self):
        '''This method is responsible for recieving encoded PDUs from Client and decode them'''
        
        length = self.conn.recv(4)
        
        if(len(length) == 4):
        
            command_length = Integer.decode(length).value
            print("Length of PDU send by client is : ")
            print(command_length)
            cid = self.conn.recv(4)
            command_id = Integer.decode(cid).value
            #print(command_id)
            
            if(command_id == 2):
            
                self.status = 'BOUND_TX'
                print("BIND TRANSMITTER PDU")
            
            elif(command_id == 1):
            
                self.status = 'BOUND_RX'
                print("BIND RECEIVER PDU")
            
            elif(command_id == 9):
            
                self.status = 'BOUND_TRX'
                print("BIND TRANCEIVER PDU")
            
            pdu = self.conn.recv(command_length-4)
            rec = BindTransmitter.decode(length+cid+pdu)
            print("Encoded PDU sent from client and decoded is:  "+hex_convert(rec.encode()))
            return rec
    
    def send_resp(self):
        '''This method is responsible for encoding response PDUs'''
        
        if( self.status == 'BOUND_TX' ):
        
            P = BindTransmitterResp()
            P.system_id = CString("SMPP3TEST")
            return P.encode()

        elif( self.status == 'BOUND_RX' ):
    
            P = BindReceiverResp()
            P.system_id = CString("SMPP3TEST")
            return P.encode()

        elif( self.status=='BOUND_TRX' ):
    
            P = BindTransceiverResp()
            P.system_id = CString("SMPP3TEST")
            return P.encode()


if __name__ == '__main__':
    #testing server
    servr = Server()
    
    
    
    
    
