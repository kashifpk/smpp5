import db
from db import DBSession
from models import User
import hashlib
import transaction
from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.session_management import *
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.pdu.session_management import BindTransmitter, BindTransmitterResp, BindReceiver, BindReceiverResp, BindTransceiver, BindTransceiverResp, OutBind, UnBind, UnBindResp, EnquireLink, EnquireLinkResp, AlertNotification, GenericNack
from smpp5.lib.constants import *

if '__main__' == __name__:
    db.bind_session()
    data = b'\x00\x00\x00/\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
      b'SUBMIT1\x00P\x01\x01\x00'
    P = BindTransmitter.decode(data)
    print(DBSession.query(User).count())
    system=P.system_id.value.decode(encoding='ascii')
    for U in DBSession.query(User).all():
      if(U.user_id==system):
         print(U.user_id)
         print(U.password)
         print(U.system_type)
         print("yessssss! it works :-) ")
         #TODO: Initially uncomment below given comments if you have already inserted record for username = SMPP3TEST, password = secret08,system_type = SUBMIT1 and after running below given statements again put these statements into comments 
         #if('SMPP3TEST'==u.user_id):
         # DBSession.delete(u)
         # transaction.commit()

      
       
    #Insert records in database
    
    #U = User()
    #U.user_id='system'
    #password='system123'
    #passhash = hashlib.sha1(bytes(password, encoding="utf8")).hexdigest()
    #U.password=passhash
    #U.system_type='SUBMIT1'
    #DBSession.add(U)
    #transaction.commit()
        
