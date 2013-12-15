from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import datetime

from ..models import (
    DBSession, Sms, User_Number, Prefix_Match, Packages, Selected_package, Network, Mnp)

from ..auth import (User)


from ..forms import ContactForm
from sqlalchemy import func


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
        sms_from = sms_body.splitlines()[1]
        try:
            message = sms_body.splitlines()[2]
        except:
            message = ''
        #Making Instance of Sms and Saving values in db
        S = Sms()
        S.sms_type = 'incoming'
        S.sms_from = sms_from
        S.sms_to = sms_to
        S.status = 'recieved'
        S.schedule_delivery_time = datetime.date.today()
        S.validity_period = None
        S.msg = message
        S.user_id = None
        S.timestamp = datetime.datetime.now()
        S.msg_type = 'text'
        S.rates = 0.0
        S.target_network = None
        DBSession.add(S)
        return{}


@view_config(route_name='main_page', renderer='main_page.mako')
def mainpage(request):
    user = request.session['logged_in_user']
    return{'user': user}


@view_config(route_name='sms_history', renderer='sms_history.mako')
def sms_history(request):
    user = request.session['logged_in_user']
    smses = DBSession.query(Sms).filter_by(user_id=user, status='delivered').all()
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
    smses = DBSession.query(Sms).filter_by(user_id=user, sms_type='outgoing', status='delivered').all()
    if(smses):
        for s in smses:
            smses_rates = smses_rates+s.rates
    total_bill = package_rates+smses_rates

    return{'smses': smses, 'package_rates': package_rates, 'smses_rates': smses_rates, 'total_bill': total_bill}


@view_config(route_name='weeklygraphs', renderer='graphs.mako')
def weeklygraph(request):
    user = request.session['logged_in_user']
    sms = []
    date = []
    todaydate = datetime.date.today()
    previousdate = todaydate-datetime.timedelta(days=7)
    smses = DBSession.query(Sms.timestamp,
                            func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(user_id='ASMA',
                                                                                        sms_type='outgoing', status='delivered').filter(Sms.timestamp >= previousdate).all()
    for row in range(len(smses)):
        for col in range(len(smses[row])):
            if col == 1:
                sms.append(smses[row][col])
            else:
                date.append(smses[row][col].strftime("%Y-%m-%d"))

    return{'sms': sms, 'date': date, 'name': 'Week', 'traffic': 'Weekly'}


@view_config(route_name='monthlygraphs', renderer='graphs.mako')
def monthlygraph(request):
    user = request.session['logged_in_user']
    sms = []
    date = []
    todaydate = datetime.date.today()
    currentmonth = todaydate.month
    month_name = todaydate.strftime('%B')
    smses = DBSession.query(Sms.timestamp, func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(user_id='ASMA', sms_type='outgoing', status='delivered').filter(func.MONTH(Sms.timestamp) == currentmonth).all()
    for row in range(len(smses)):
        for col in range(len(smses[row])):
            if col == 1:
                sms.append(smses[row][col])
            else:
                date.append(smses[row][col].strftime("%Y-%m-%d"))

    return{'sms': sms, 'date': date, 'name': month_name, 'traffic': 'Monthly'}


@view_config(route_name='dailygraphs', renderer='graphs.mako')
def dailygraph(request):
    user = request.session['logged_in_user']
    sms = []
    date = []
    smses = DBSession.query(Sms.timestamp, func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(user_id='ASMA', sms_type='outgoing', status='delivered').all()
    for row in range(len(smses)):
        for col in range(len(smses[row])):
            if col == 1:
                sms.append(smses[row][col])
            else:
                date.append(smses[row][col].strftime("%Y-%m-%d"))

    return{'sms': sms, 'date': date, 'name': '', 'traffic': 'Daily'}


@view_config(route_name='packages', renderer='packages.mako')
def packages(request):
    user = request.session['logged_in_user']
    total_selected_package = DBSession.query(Selected_package).filter_by(user_id=user).count()
    if(total_selected_package > 0):
        selected_package = DBSession.query(Selected_package).filter_by(user_id=user)[-1]
        end_date = int(selected_package.end_date.strftime('%d'))
        end_month = int(selected_package.end_date.strftime('%m'))
    else:
        selected_package = None
        end_date = None
        end_month = None
    date = datetime.datetime.now()
    today_date = int(date.strftime('%d'))
    today_month = int(date.strftime('%m'))
    return{'selected_package': selected_package, 'today_date': today_date, 'today_month': today_month,
           'end_date': end_date, 'end_month': end_month}


@view_config(route_name='select_packages', renderer='select_packages.mako')
def select_packages(request):
    user = request.session['logged_in_user']
    if "POST" == request.method:
        package_name = request.POST['package_name']
        package = DBSession.query(Packages).filter_by(package_name=package_name).first()
        duration = int(package.duration)
        S = Selected_package()
        S.user_id = user
        S.package_name = package_name
        S.smses = package.smses
        S.rates = package.rates
        S.start_date = datetime.date.today()
        S.end_date = S.start_date+datetime.timedelta(days=duration)
        S.status = 'unpaid'
        DBSession.add(S)

        request.session.flash("Your package has been activated!")
        return HTTPFound(location=request.route_url('main_page'))

    packages = DBSession.query(Packages).all()
    return{'packages': packages}


