   <%inherit file="base.mako"/>
   <html>
    <head>
<style>
#history
{
	font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
	font-size: 12px;
	width: 100%;
	text-align: left;
	border-collapse: collapse;
}
#history th
{
	font-size: 14px;
	font-weight: normal;
	padding: 12px 15px;
	border-right: 1px solid #fff;
	border-left: 1px solid #fff;
	color: #039;
}
#history td
{
	padding: 8px 15px;
	border-right: 1px solid #fff;
	border-left: 1px solid #fff;
	color: #669;
}
.history-odd
{
	background: #eff2ff;
}
.history-even
{
	background: #e8edff;
}
#history #history-2, #history #history-4, #history #history-6
{
	background: #d0dafd;
	border-bottom: 1px solid #c8d4fd;
}
#history #history-1, #history #history-3, #history #history-5, #history #history-7
{
	background: #dce4ff;
	border-bottom: 1px solid #d6dfff;
        }
p {color:#369;}
</style>
</head>
   <body>
   <h1><font color = "#039">&nbsp&nbsp&nbspSms History</h1></ font>
   <br />
   <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#c8d4fd"></ div><br /><br />
   
   <table id="history">
    <colgroup>
    	<col class="history-odd" />
    	<col class="history-even" />
    	<col class="history-odd" />
        <col class="history-even" />
        <col class="history-odd" />
        <col class="history-even" />
        <col class="history-odd" />
    </colgroup>
    <thead>
    	<tr>
            <th scope="col" id="history-1">USER</th>
            <th scope="col" id="history-2">MESSAGE</th>
            <th scope="col" id="history-3">SMS TO</th>
            <th scope="col" id="history-4">SMS FROM</th>
            <th scope="col" id="history-5">SMS TYPE</th>
            <th scope="col" id="history-6">DATE</th>
            <th scope="col" id="history-7">RATES</th>
        </tr>
    </thead>
   <tbody>
   % for s in smses:
     <tr>
       <td>${s.user_id}</td>
       <td>${s.msg}</td>
       <td>${s.sms_to}</td>
       <td>${s.sms_from}</td>
       <td>${s.sms_type}</td>
       <td>${s.timestamp}</td>
       <td>${s.rates}</td>
     </tr>
     </tbody>
   % endfor
   </table>
  <br />
 <br />
 <a href= ${request.route_url('main_page')}><p><center>BACK TO MAIN PAGE</center></p></a>
   <br /><br /><br />
   </ body>
   </html>
