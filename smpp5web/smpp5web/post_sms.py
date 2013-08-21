 
from bottle import *
from models.db import get_db_session
from models.models import Sms, User
 
@post('/send_sms')
def send_sms():
    '''this method has to read the pending status sms from databasepost sms to url 
    '''
    try:
        db_session = get_db_session()
        smses = db_session.query(Sms).filter(Sms.status=='pending').filter(Sms.sms_type=='outgoing').all()
        
        for sms in smses:
            post_args = dict(sms_id=sms[u'sms_id'], sms_type=sms[u'sms_from'], sms_from=sms[u'sms_from'], sms_to=sms[u'sms_to'], msg=sms[u'msg'], timestamp=sms[u'timestamp'], status=sms[u'status'], user_id=sms[u'user_id'])
            post_data = urllib.urlencode(post_args)
        
    except Exception, e:
        return "Error posting sms\n" + str(e)
   
