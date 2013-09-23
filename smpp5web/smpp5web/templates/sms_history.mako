<%inherit file="base.mako"/>
<html>
<body>
<h1><font color = "#EE872A">&nbsp&nbsp&nbspSms History Data</h1></ font>
<br /><br />
<div style="font-family:verdana;border-radius:4px;height:5px;background-color:#EE872A"></ div><br /><br />
<table border=1px>
   <tr>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp<B>MSISDN</B></th>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<B>MESSAGE</B></th>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<B>SMS TYPE</B></th>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<B>SMS FROM</B></th>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<B>SMS TO</B></th>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<B>DATE</B></th></ div>
  </tr>
% for s in smses:
  <tr>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp${s.user_id}</td>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${s.msg}</td>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${s.sms_type}</td>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${s.sms_from}</td>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${s.sms_to}</td>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${s.timestamp}</td>
  </tr>
% endfor
</table>
<p>
<br /><br /><br /><br /><br /><br /><br />


<a href= ${request.route_url('main_page')}><h2>BACK TO MAIN PAGE<h2></a><p>
</ body>
</html>
