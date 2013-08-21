from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ..models import (
    DBSession,
    )

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
    
@view_config(route_name='send_sms', renderer='send_sms.mako')
def send_sms(request):
    
    f = request.POST   # empty form initializes if not a POST request
    return {'send_sms': f, 'project': 'smpp5web'}


@view_config(route_name='incoming_sms', renderer='incoming_sms.mako')
def incoming_sms(request):
    
    f = request.POST   # empty form initializes if not a POST request
    return {'incoming_sms': f, 'project': 'smpp5web'}

