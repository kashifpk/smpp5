import db
from db import DBSession
from models import User, Sms, Selected_package, User_Number, Prefix_Match
import hashlib
import transaction
from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.session_management import *
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.pdu.session_management import BindTransmitter, BindTransmitterResp, BindReceiver, BindReceiverResp, BindTransceiver, BindTransceiverResp, OutBind, UnBind, UnBindResp, EnquireLink, EnquireLinkResp, AlertNotification, GenericNack
from smpp5.lib.constants import *
from sqlalchemy import func
import datetime

if '__main__' == __name__:
    db.bind_session()
    d = datetime.date.today()
    S = Sms()
    S.sms_type = 'outgoing'
    S.sms_from = '+9233365195924'
    S.sms_to = '+923366767999'
    S.schedule_delivery_time = d   # give date 2nd december
    S.validity_period = d+datetime.timedelta(days=1)
    S.msg = "dont disturb.."
    S.timestamp = d
    S.status = 'delivered'
    S.msg_type = 'text'
    S.user_id = 'ASMA'
    S.package_name = 'iyashi'
    S.rates = 0.0
    S.target_network = 'ufone'  # process sms file would use it to send to respective network of which server is.
    S.client_type = 'smpp'
    DBSession.add(S)
    #user = DBSession.query(User_Number).filter_by(user_id='ASMA').first()  # user refers to normal user
    #cell_number = user.cell_number
    #source_prefix = cell_number[0:6]
    #dest_prefix = '+92300'
    #source_network = DBSession.query(Prefix_Match).filter_by(prefix=source_prefix).first()  # t_user refers to network
    #dest_network = DBSession.query(Prefix_Match).filter_by(prefix=dest_prefix).first()  # t_user refers to network
    #print(source_network.network)
    #print(dest_network.network)
    transaction.commit()
    #data = b'\x00\x00\x00/\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
      #b'SUBMIT1\x00P\x01\x01\x00'
    #P = BindTransmitter.decode(data)
    #print(DBSession.query(User).count())
    #system=P.system_id.value.decode(encoding='ascii')
    #for U in DBSession.query(User).all():
      #if(U.user_id==system):
         #print(U.user_id)
         #print(U.password)
         #print(U.system_type)
         #print("yessssss! it works :-) ")
         #TODO: Initially uncomment below given comments if you have already inserted record for username = SMPP3TEST, password = secret08,system_type = SUBMIT1 and after running below given statements again put these statements into comments 
         #if('SMPP3TEST'==u.user_id):
         # DBSession.delete(u)
         # transaction.commit()
    #date = datetime.date.today()
    #month = date.month
    ##date2 = date-datetime.timedelta(days=7)
    #smses = DBSession.query(Sms.timestamp, func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(user_id='ASMA', sms_type='outgoing').filter(func.MONTH(Sms.timestamp) == month).all()
    ##print(smses.timestamp.month)
    #print(smses)
    #sms = []
    #date = []
    #smses = DBSession.query(Sms.timestamp, func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(user_id='ASMA', sms_type='outgoing').all()
    #print(smses[3][1])
    #print(len(smses[0]))
    #for row in range(len(smses)):
    #    for col in range(len(smses[row])):
    #        if col == 1:
    #            sms.append(smses[row][col])
    #        else:
    #            date.append(int(smses[row][col].strftime('%d')))
    #print(sms)
    #print(date)
    #  
    #   
    #Insert records in database

    #U = User()
    #U.user_id='UFONE'
    #password='secret08'
    #passhash = hashlib.sha1(bytes(password, encoding="utf8")).hexdigest()
    #U.password=passhash
    #U.system_type='SUBMIT1'
    #U.bind_account_type = 'telecom'
    #DBSession.add(U)
    #transaction.commit()
    #sms = []
    #date = []
    #smses = DBSession.query(Sms.timestamp, func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(user_id='ASMA', sms_type='outgoing').all()
    #for row in range(len(smses)):
    #    for col in range(len(smses[row])):
    #        if col == 1:
    #            sms.append(smses[row][col])
    #        else:
    #            date.append(smses[row][col].strftime("%Y-%m-%d"))
    #print(sms)
    #print(date)