'''This background process is responsible for reading the outgoing smses from database sent by client
and post them to the url on bottle server
'''
import urllib2
import urllib
import db
import transaction
from db import DBSession
from models import Sms, User

try:
    db.bind_session()
    smses = DBSession.query(Sms).filter_by(status='scheduled', sms_type='outgoing').count()
    if(smses == 0):
        print("\nYou have no pending messages to sent.......Thanks\n")
    else:
        smses = DBSession.query(Sms).filter_by(status='scheduled', sms_type='outgoing').all()
        for S in smses:
            sms_to = S.sms_to
            sms_from = S.sms_from
            message = S.msg
            post_data = {'sms_to': sms_to, 'sms_from': sms_from, 'message': message}
            post_str = urllib.urlencode(post_data)    
            # urlencode converts the dict to a string suitable for POST
            # Note when some data is specified in urlopen then HTTP request type 
            # POST is used instead of GET request type
            result = urllib2.urlopen("http://192.168.1.2:50111/" + 'sendsms', post_str).read()
            S.status = 'delivered'
            print(result)
        transaction.commit()

except Exception, e:
    print(e.__class__.__name__, e.message)
