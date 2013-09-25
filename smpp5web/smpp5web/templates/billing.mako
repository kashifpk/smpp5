<%inherit file="base.mako"/>
<html>
<body>
<h1><font color = "#EE872A">&nbsp&nbsp&nbspSms Bills</h1></ font>
<br /><br />
<div style="font-family:verdana;border-radius:4px;height:5px;background-color:#EE872A"></ div><br /><br />
<table border=1px>
   <tr>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp<B>MSISDN</B></th>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<B>MESSAGE</B></th>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<B>SMS TO</B></th>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<B>DATE</B></th>
    <th>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<B>RATES</B></th>
  </tr>
% for s in smses:
  <tr>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp${s.sms_from}</td>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${s.msg}</td>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${s.sms_to}</td>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${s.timestamp}</td>
    <td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${s.rates}</td>
  </tr>
% endfor
</table>
<br /><br /><br /><br /><br />
<div style="font-family:verdana;border-radius:4px;height:5px;background-color:#EE872A"></ div><br /><br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
&nbsp&nbsp&nbsp&nbsp
TOTAL PACKAGES PRICE = Rs.${package_rates}<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
&nbsp&nbsp&nbsp&nbsp
TOTAL SMS PRICES&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp= Rs.${smses_rates}<br />
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
&nbsp&nbsp&nbsp&nbsp
TOTAL BILL&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp= Rs.${total_bill}<br />
<p>
<br /><br /><br /><br /><br />
<a href= ${request.route_url('main_page')}><h2>BACK TO MAIN PAGE<h2></a><p>
</ body>
</html>
