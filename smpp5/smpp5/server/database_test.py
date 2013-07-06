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
    #data = b'\x00\x00\x00/\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
     #       b'SUBMIT1\x00P\x01\x01\x00'
    #P = BindTransmitter.decode(data)
    #print(DBSession.query(User).count())
    #system=P.system_id.value.decode(encoding='ascii')
    #for R in DBSession.query(User):
     # if(R.user_id==system):
      #print(R.user_id)
       #print("yessssss! it works  :-) ")
      
       
    #Insert records in database
    
    U = User()
    U.user_id='SMPP3TEST'
    password='secret08'
    passhash = hashlib.sha1(bytes(password, encoding="utf8")).hexdigest()
    U.password=passhash
    U.system_type='SUBMIT1'
    DBSession.add(U)
    transaction.commit()
    #DBSession.query(User).filter_by(user_id=system_id, system_type=system_type, password=passhash).first()
    #passhash = hashlib.sha1(bytes(password, encoding="utf8")).hexdigest()
    for u in  DBSession.query(User).all():
        print(u.user_id)
        print(u.password)
        print(u.system_type)
        #if('SMPP3TEST'==u.user_id):
         #   DBSession.delete(u)
          #  transaction.commit()

    #S=User()
    #S.user_id='SMPP3TEST'
    #S.password='secret08'
    #S.system_type='SUBMIT1'
    #DBSession.add(S)
    #transaction.commit()
    #

