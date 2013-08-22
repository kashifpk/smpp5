from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import datetime

from ..models import (
    DBSession, Sms)

from ..forms import ContactForm


@view_config(route_name='home', renderer='home.mako')
def my_view(request):
    one = None
    return {'one': one, 'project': 'smpp5web'}


@view_config(route_name='contact', renderer="contact.mako")
def contact_form(request):

    f = ContactForm(request.POST)   # empty form initializes if not a POST request

    if 'POST' == request.method and 'form.submitted' in request.params:
        if f.validate():
            #TODO: Do email sending here.

            request.session.flash("Your message has been sent!")
            return HTTPFound(location=request.route_url('home'))

    return {'contact_form': f}


@view_config(route_name='sms_in', renderer='sms.mako')
def say(request):
    if "POST" == request.method:
        S = Sms()
        S.sms_type = 'incoming'
        S.sms_from = request.POST['address']
        S.sms_to = 'None'
        S.msg = request.POST['body']
        S.timestamp = datetime.datetime.now()
        S.status = 'pending'
        S.msg_type = 'text'
        S.user_id = '3TEST'
        DBSession.add(S)
        return{}



    
