<%inherit file="base.mako"/>

<%def name="title()">
smpp5web - Authentication Manager
</%def>

<%def name="main_menu()">
<p>
 %if request.session.get('logged_in_user', None) == 'admin':
  <a href="${request.route_url('pyckauth_users')}">Users</a> |
  <a href="${request.route_url('pyckauth_permissions')}">Permissions</a> |
  <a href="${request.route_url('pyckauth_routes')}">Routes</a>
 %endif
</p>
</%def>

${self.body()}

<%def name="footer()">
  
</%def>