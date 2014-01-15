from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import datetime
from time import strptime
from ..models import (
    DBSession, Sms, User_Number, Prefix_Match, Packages, Selected_package, Network, Mnp)
import hashlib
from ..auth import (User)


from ..forms import ContactForm
from ..forms import LoginForm, UserForm, PermissionForm, RoutePermissionForm
from ..models import DBSession, Permission, User, UserPermission, RoutePermission

from sqlalchemy import func


@view_config(route_name='home', renderer='home.mako')
def my_view(request):
    one = None
    return {'one': one, 'project': 'smpp5web'}


@view_config(route_name='contact', renderer="contact.mako")
def contact_form(request):

    f = ContactForm(request.POST)   # Empty form initializes if not a POST request

    if 'POST' == request.method and 'form.submitted' in request.params:
        if f.validate():
            #TODO: Do email sending here.

            request.session.flash("Your message has been sent!")
            return HTTPFound(location=request.route_url('home'))

    return {'contact_form': f}


@view_config(route_name='sms_in', renderer='sms.mako')
def say(request):
    if "POST" == request.method:
        try:
            sms_body = request.POST['body']
            sms_to = sms_body.splitlines()[0]
            if sms_to.isdigit() is True:
                if not sms_to.startswith('+'):
                    sms_to = '+92' + sms_to[1:]
            else:
                sms_to = ''
            sms_from = sms_body.splitlines()[1]
            if sms_from.isdigit() is True:
                if not sms_from.startswith('+'):
                    sms_from = '+92' + sms_from[1:]
            else:
                sms_from = ''
            try:
                message = ''
                messages = sms_body.splitlines()[2:]
                for m in messages:
                    message = message + m + "\n"
            except:
                messages = ''
            #Making Instance of Sms and Saving values in db
            if sms_to != '' and sms_from != '' and messages != '':
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
                S.client_type = 'mobile'
                DBSession.add(S)
                return{}
        except:
            return{}


@view_config(route_name='main_page', renderer='main_page.mako')
def mainpage(request):
    user = request.session['logged_in_user']  # Open page for logged in user 
    return{'user': user}


@view_config(route_name='sms_history', renderer='sms_history.mako')
def sms_history(request):
    user = request.session['logged_in_user']
    if "POST" == request.method:
        user = request.POST['user_id']
    smses = DBSession.query(Sms).filter_by(user_id=user, status='delivered').all()  # Query all delivered sms for logged in user
    return{'smses': smses}


@view_config(route_name='sms_history_admin', renderer='sms_history_admin.mako')
def admin_sms_history(request):
    if "POST" == request.method:
        user = request.POST['user_id']
        smses = DBSession.query(Sms).filter_by(user_id=user, status='delivered').all()  # Query smses of the user selected by admin
        return{'smses': smses}


@view_config(route_name='billing', renderer='billing.mako')
def billing(request): 
    'Calculate the billing information for the user.'
    
    user = request.session['logged_in_user']
    package_rates = 0.0
    smses_rates = 0.0
    selected_packages = DBSession.query(Selected_package).filter_by(user_id=user).all()  # Query the package selected by user
    # Calculate rates if user has selected some package
    if(selected_packages):
        for p in selected_packages:
            package_rates = package_rates+p.rates
            
    #  Query from sms table fetch the records
    # Calculate rates if no package has been selected
    smses = DBSession.query(Sms).filter_by(user_id=user, sms_type='outgoing', status='delivered').all()
    if(smses):
        for s in smses:
            smses_rates = smses_rates+s.rates
    
    # Calculate total bill i-e package and sms rates
    total_bill = package_rates+smses_rates

    return{'smses': smses, 'package_rates': package_rates, 'smses_rates': smses_rates, 'total_bill': total_bill}


@view_config(route_name='dailygraphs', renderer='graphs.mako')
def dailygraph(request):
    user = request.session['logged_in_user']
    sms = []
    date = []
    smses = DBSession.query(Sms.timestamp, func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(user_id=user, sms_type='outgoing', status='delivered').all()
    for row in range(len(smses)):
        for col in range(len(smses[row])):
            if col == 1:
                sms.append(smses[row][col])
            else:
                date.append(smses[row][col].strftime("%Y-%m-%d"))

    return{'sms': sms, 'date': date, 'name': '', 'traffic': 'Daily'}


@view_config(route_name='weeklygraphs', renderer='graphs.mako')
def weeklygraph(request):
    user = request.session['logged_in_user']
    sms = []
    date = []
    todaydate = datetime.date.today()
    previousdate = todaydate-datetime.timedelta(days=7)
    smses = DBSession.query(Sms.timestamp,
                            func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(user_id=user,
                                                                                        sms_type='outgoing', status='delivered').filter(Sms.timestamp >= previousdate).all()
    for row in range(len(smses)):
        for col in range(len(smses[row])):
            if col == 1:
                sms.append(smses[row][col])
            else:
                date.append(smses[row][col].strftime("%Y-%m-%d"))

    return{'sms': sms, 'date': date, 'name': '', 'traffic': 'Weekly'}


@view_config(route_name='monthlygraphs', renderer='graphs.mako')
def monthlygraph(request):
    user = request.session['logged_in_user']
    sms = []
    date = []
    todaydate = datetime.date.today()
    currentmonth = todaydate.month
    month_name = todaydate.strftime('%B')
    smses = DBSession.query(Sms.timestamp, func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(user_id=user, sms_type='outgoing', status='delivered').filter(func.MONTH(Sms.timestamp) == currentmonth).all()
    for row in range(len(smses)):
        for col in range(len(smses[row])):
            if col == 1:
                sms.append(smses[row][col])
            else:
                date.append(smses[row][col].strftime("%Y-%m-%d"))

    return{'sms': sms, 'date': date, 'name': month_name, 'traffic': 'Monthly'}


@view_config(route_name='usermonthlygraphs', renderer='usergraphs.mako')
def usermonthlygraph(request):
    if "POST" == request.method:
        month = request.POST['month']
        sms = []
        date = []
        currentmonth = strptime(month[0:3], '%b').tm_mon
        month_name = request.POST['month']
        smses = DBSession.query(Sms.timestamp, func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(sms_type='outgoing', status='delivered').filter(func.MONTH(Sms.timestamp) == currentmonth).all()
        for row in range(len(smses)):
            for col in range(len(smses[row])):
                if col == 1:
                    sms.append(smses[row][col])
                else:
                    date.append(smses[row][col].strftime("%Y-%m-%d"))

        return{'sms': sms, 'date': date, 'name': month, 'traffic': 'Monthly'}


@view_config(route_name='useryearlygraphs', renderer='usergraphs.mako')
def useryearlygraph(request):
    if "POST" == request.method:
        year = request.POST['year']
        sms = []
        date = []
        todaydate = datetime.date.today()
        smses = DBSession.query(Sms.timestamp, func.count(Sms.sms_type)).group_by(Sms.timestamp).filter_by(sms_type='outgoing', status='delivered').filter(func.YEAR(Sms.timestamp) == year).all()
        for row in range(len(smses)):
            for col in range(len(smses[row])):
                if col == 1:
                    sms.append(smses[row][col])
                else:
                    date.append(smses[row][col].strftime("%Y-%m-%d"))

        return{'sms': sms, 'date': date, 'name': year, 'traffic': 'Yearly'}


@view_config(route_name='packages', renderer='packages.mako')
def packages(request):
    user = request.session['logged_in_user']
    total_selected_package = DBSession.query(Selected_package).filter_by(user_id=user).count()
    if(total_selected_package > 0):
        selected_package = DBSession.query(Selected_package).filter_by(user_id=user)[-1]
        end_date = int(selected_package.end_date.strftime('%d'))
        end_month = int(selected_package.end_date.strftime('%m'))
        end_year = int(selected_package.end_date.strftime('%y'))
    else:
        selected_package = None
        end_date = None
        end_month = None
        end_month = None
        end_year = None
    date = datetime.datetime.now()
    today_date = int(date.strftime('%d'))
    today_month = int(date.strftime('%m'))
    today_year = int(date.strftime('%y'))
    return{'selected_package': selected_package, 'today_date': today_date, 'today_month': today_month,
           'today_year': today_year, 'end_date': end_date, 'end_month': end_month,  'end_year': end_year}


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


@view_config(route_name='admin_page', renderer='admin_page.mako')
def adminpage(request):
    return{}


@view_config(route_name='reset_password', renderer='reset_password.mako')
def reset_password(request):
    action = request.GET.get('action', 'add')
    user = request.session['logged_in_user']
    U = None

    if 'edit' == action:
        U = DBSession.query(User).filter_by(user_id=request.GET['id']).first()

    f = UserForm(request.POST, U)

    if 'POST' == request.method:
        if f.validate():
            if 'add' == action:
                U = User()
                f.populate_obj(U)
                U.password = hashlib.sha1(f.password.data).hexdigest()
                DBSession.add(U)

                # Add user permissions here.
                for key in request.POST.keys():
                    if key.startswith('chk_perm_'):
                        permission = request.POST[key]
                        UP = UserPermission(f.user_id.data, permission)
                        DBSession.add(UP)

                request.session.flash("User created!")
                return HTTPFound(location=request.current_route_url())

            elif 'edit' == action:
                DBSession.query(UserPermission).filter_by(user_id=request.GET['id']).delete()
                for key in request.POST.keys():
                    if key.startswith('chk_perm_'):
                        permission = request.POST[key]
                        UP = UserPermission(f.user_id.data, permission)
                        DBSession.add(UP)

                f.populate_obj(U)
                U.password = hashlib.sha1(f.password.data).hexdigest()
                request.session.flash("User updated!")
                return HTTPFound(location=request.route_url('main_page'))

    permissions = DBSession.query(Permission).order_by('permission')
    users = DBSession.query(User).order_by('user_id').filter_by(user_id=user)

    return dict(action=action, user_form=f, users=users, user=U)


@view_config(route_name='display_users', renderer='display_users.mako')
def display_users(request):
    users = DBSession.query(User).order_by('user_id')
    months_choices = []
    months = []
    years = []
    for i in range(1, 13):
        months_choices.append((i, datetime.date(2008, i, 1).strftime('%B')))
    for m in months_choices:
        months.append(m[1])
    for y in range(1995, datetime.datetime.now().year + 1):
        years.append(y)
    return{'users': users, 'months': months, 'years': years}




