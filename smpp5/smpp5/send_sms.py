'''This module is responsible for physicaly routing the smses.
'''
from bottle import *
import android, socket, struct

def return_ip():
  '''This method is responsible for getting ip address
    '''
    droid = android.Android()
    ipdec = droid.wifiGetConnectionInfo().result['ip_address']
    ipstr = socket.inet_ntoa(struct.pack('L', ipdec))
    return ipstr


@post('/sendsms')
'''This method is responsible for reading sms from url to which smpp server has posted and send to the particular recipient
    '''
def read_sms():
    sms_to = request.forms.sms_to
    sms_from = request.forms.sms_from
    message = request.forms.message 
    sms_body = "Sms To :"+sms_to +"\nSms From :"+sms_from +"\nMessage :" +message
    droid = android.Android()
    droid.smsSend(sms_to,sms_body)
    return "Message sent successfully"

#Running at this host and port on android
run(host= return_ip(), port=50111)
