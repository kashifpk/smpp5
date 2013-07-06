import socket
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.constants import *
from smpp5.lib.constants import NPI, TON, esm_class, command_id, command_status, tlv_tag
from smpp5.lib.constants.command_status import *
from smpp5.lib.pdu.session_management import BindTransmitter, BindTransmitterResp, BindReceiver, BindReceiverResp, BindTransceiver, BindTransceiverResp, OutBind, UnBind, UnBindResp, EnquireLink, EnquireLinkResp, AlertNotification, GenericNack
from smpp5.lib.pdu.pdu import PDU
import db
from db import DBSession
from models import User
import hashlib
import transaction

class Server(object):
    '''Server class is responsible for recieving PDUs from client and decode them and also for sending encoded PDUs response'''
    status='CLOSED'
    decode_pdu='' 
    PORT = 50007
    pdu_status=''

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), self.PORT))
        self.server.listen(1)
        print(b'Server is listening')
        self.status='OPEN'
        (self.conn, addr) = self.server.accept()
        print('Connected by' + str(addr))
        while(self.status in ['OPEN', 'BOUND_TX', 'BOUND_TRX', 'BOUND_RX', 'ERROR']):
         decode_pdu = self.recieve()         #calling recieve method
         resp_pdu=self.send_resp()           #calling send_resp method
         self.conn.sendall(resp_pdu)
         print("Response encoded and sent to Client is: ")
         print(resp_pdu)
        self.conn.close()

    def recieve(self):
        '''This method is responsible for recieving encoded PDUs from Client and decode them'''
        length = self.conn.recv(4)
        while len(length) < 4:
            #time.sleep(1)   # if bytes received from client are less than 4
            length += self.conn.recv(4-len(length))
        pdu_length = Integer.decode(length).value
        print(pdu_length)
        pdu_str = length
        while len(pdu_str) != pdu_length:
            pdu_str += self.conn.recv(pdu_length-len(pdu_str))
        P = PDU.decode(pdu_str)
        if(P.command_id.value==2):
         P=BindTransmitter.decode(pdu_str)
         self.status='BOUND_TX'
        elif(P.command_id.value==1):
         P=BindReceiver.decode(pdu_str)
         self.status='BOUND_RX'
        elif(P.command_id.value==9):
         P=BindTransceiver.decode(pdu_str)
         self.status='BOUND_TRX'
        elif(P.command_id.value==6):
         P=UnBind.decode(pdu_str)   
        self.status='UNBIND'

        if type(P) in [BindTransmitter, BindReceiver, BindTransceiver]:
         db.bind_session()
         system_id=P.system_id.value.decode(encoding='ascii')
         password=P.password.value.decode(encoding='ascii')
         system_type=P.system_type.value.decode(encoding='ascii')
         #print(P.system_id.value)
         for R in DBSession.query(User):
          if(R.user_id==system_id and R.password==password and R.system_type==system_type):
           self.pdu_status='accept'
         if(self.pdu_status=='accept'):
          pass
         else:
          self.status="ERROR"
        print("Encoded PDU sent from client and decoded is:  "+hex_convert(P.encode()))
        return P

    def send_resp(self):
        '''This method is responsible for encoding response PDUs'''
        if(self.status=='BOUND_TX'):
            P = BindTransmitterResp()
            P.system_id = CString("SMPP3TEST")
            return P.encode()

        elif(self.status=='BOUND_RX'):
    
            P = BindReceiverResp()
            P.system_id = CString("SMPP3TEST")
            return P.encode()

        elif(self.status=='BOUND_TRX'):
    
            P = BindTransceiverResp()
            P.system_id = CString("SMPP3TEST")
            return P.encode()
        
        elif(self.status=='UNBIND'):
    
            P = UnBindResp()
            return P.encode()
            self.status='CLOSED'
    
        elif(self.status=='ERROR'):
         P=GenericNack()
         P.command_status= Integer(command_status.ESME_RBINDFAIL, 4)
         return P.encode()
    


if __name__ == '__main__':
    #testing server
    servr=Server()
    
    
    
    
    
