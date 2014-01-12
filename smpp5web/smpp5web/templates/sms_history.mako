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
#history #history-2, #history #history-4, #history #history-6, #history #history-8
{
	background: #d0dafd;
	border-bottom: 1px solid #c8d4fd;
}
#history #history-1, #history #history-3, #history #history-5, #history #history-7, #history #history-9
{
	background: #dce4ff;
	border-bottom: 1px solid #d6dfff;
        }
p {color:#369;}
.historry { height: 16em; overflow: auto; }
</style>
</head>
   <body>
   <h1><font color = "#039">&nbsp&nbsp&nbspSms History</h1></ font>
   <br />
   <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#c8d4fd"></ div><br /><br />
   <div class="historry">
   <table id="history">
    <colgroup>
    	<col class="history-odd" />
    	<col class="history-even" />
    	<col class="history-odd" />
        <col class="history-even" />
        <col class="history-odd" />
    </colgroup>
    <thead>
    	<tr>
            <th scope="col" id="history-1"><center>USER</center></th>
            <th scope="col" id="history-2"><center>SMS TO</center></th>
            <th scope="col" id="history-3"><center>MESSAGE</center></th>
            <th scope="col" id="history-4"><center>SMS STATUS</center></th>
            <th scope="col" id="history-5"><center>DELIVERED DATE</center></th>
        </tr>
    </thead>
   <tbody>
   % for s in smses:
     <tr>
       <td><center>${s.user_id}</center></td>
       <td><center>${s.sms_to}</center></td>
       <td><center>${s.msg}</center></td>
       <td><center>${s.status}</center></td>
       <td><center>${s.timestamp}</center></td>

     </tr>
     </tbody>
   % endfor
   </table></div><br /><br />
   <h1><font color = "#039">&nbsp&nbsp&nbspSms Traffic Graphs</h1></font>
   <br />
   <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#c8d4fd"></div><br /><br />
    <a href= ${request.route_url('dailygraphs')}><p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspDaily Sms Traffic</p></a>
    <a href= ${request.route_url('weeklygraphs')}><p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspWeekly Sms Traffic</p></a>
    <a href= ${request.route_url('monthlygraphs')}><p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspMonthly Sms Traffic</p></a>
  <br />
 <br />
 <a href= ${request.route_url('main_page')}><p><center>BACK TO MAIN PAGE</center></p></a>
   <br /><br /><br />
   </ body>
   </html>