from bottle import *
import android

@post('/sendsms')
def read_sms():
    number = request.forms.number
    message = request.forms.message 
    droid = android.Android()
    droid.smsSend(number,message)
    return "Message sent successfully"


run(host='192.168.1.2', port=50111)
