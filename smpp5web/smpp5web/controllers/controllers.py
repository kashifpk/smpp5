from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import datetime

from ..models import (
    DBSession, Sms, User_Number, Prefix_Match)

from ..auth import (User)


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
        sms_body = request.POST['body']
        sms_to = sms_body.splitlines()[0]
        sms_from = request.POST['address']
        message = sms_body.splitlines()[1]
        #Making Instance of Sms and Saving values in db
        S = Sms()
        S.sms_type = 'incoming'
        S.sms_from = sms_from
        S.sms_to = sms_to
        S.msg = message
        user_number = DBSession.query(User_Number).filter_by(cell_number=sms_to).first()
        # if number in sms_to is not present in user_number table then find number in telecom table
        if(user_number is None):
            prefix = '0'+sms_to[3:6]
            telecom_number = DBSession.query(Prefix_Match).filter_by(prefix=prefix).first()
            if(telecom_number is not None):
                users = DBSession.query(User).filter_by(user_id=telecom_number.user_id).first()
                if(users.bind_account_type == 'telecom'):
                    S.user_id = telecom_number.user_id
        else:
            S.user_id = user_number.user_id
        S.timestamp = datetime.datetime.now()
        S.status = 'pending'
        S.msg_type = 'text'
        if(user_number or telecom_number is not None):
            DBSession.add(S)
        return{}



    
