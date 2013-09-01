from bottle import *
import android, socket, struct

def return_ip():
    droid = android.Android()
    ipdec = droid.wifiGetConnectionInfo().result['ip_address']
    ipstr = socket.inet_ntoa(struct.pack('L', ipdec))
    return ipstr


@post('/sendsms')
def read_sms():
    '''This method is responsible for reading sms from url to which smpp server has posted and send to the particular recipient
    '''
    
    number = request.forms.number
    message = request.forms.message 
    droid = android.Android()
    droid.smsSend(number,message)
    return "Message sent successfully"


run(host= return_ip(), port=50111)
