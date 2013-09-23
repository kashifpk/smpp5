from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import datetime

from ..models import (
    DBSession, Sms, User_Number, Prefix_Match, Packages, Selected_package, Rates)

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


@view_config(route_name='main_page', renderer='main_page.mako')
def mainpage(request):
    user = request.session['logged_in_user']
    return{'user': user}


@view_config(route_name='sms_history', renderer='sms_history.mako')
def sms_history(request):
    user = request.session['logged_in_user']
    smses = DBSession.query(Sms).filter_by(user_id=user).all()
    return{'smses': smses}


@view_config(route_name='billing', renderer='billing.mako')
def billing(request):
    user = request.session['logged_in_user']
    package_rates = 0.0
    smses_rates = 0.0
    selected_packages = DBSession.query(Selected_package).filter_by(user_id=user).all()
    if(selected_packages):
        for p in selected_packages:
            package_rates = package_rates+p.rates
    smses = DBSession.query(Sms).filter_by(user_id=user, sms_type='outgoing').all()
    if(smses):
        for s in smses:
            smses_rates = smses_rates+s.rates
    total_bill = package_rates+smses_rates

    return{'smses': smses, 'package_rates': package_rates, 'smses_rates': smses_rates, 'total_bill': total_bill}


