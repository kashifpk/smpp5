   <%inherit file="base.mako"/>
   <html>
   <head>
<style>
#billing
{
	font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
	font-size: 12px;
	width: 100%;
	text-align: left;
	border-collapse: collapse;
}
#billing th
{
	font-size: 14px;
	font-weight: normal;
	padding: 12px 15px;
	border-right: 1px solid #fff;
	border-left: 1px solid #fff;
	color: #039;
}
#billing td
{
	padding: 8px 15px;
	border-right: 1px solid #fff;
	border-left: 1px solid #fff;
	color: #669;
}
.billing-odd
{
	background: #eff2ff;
}
.billing-even
{
	background: #e8edff;
}
#billing #billing-2, #billing #billing-4
{
	background: #d0dafd;
	border-bottom: 1px solid #c8d4fd;
}
#billing #billing-1, #billing #billing-3, #billing #billing-5
{
	background: #dce4ff;
	border-bottom: 1px solid #d6dfff;
        }
p {color:#369;}
.billings { height: 16em; overflow: auto; }

</style>
</head>
   <body>
   <h1><font color = "#039">&nbsp&nbsp&nbspSms Bills</h1></font>
   <br />
   <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#c8d4fd"> </div><br /><br />
   <div class = "billings">
   
   <table id="billing">
    <colgroup>
    	<col class="billing-odd" />
    	<col class="billing-even" />
    	<col class="billing-odd" />
    </colgroup>
    <thead>
    	<tr>
            <th scope="col" id="billing-1">SMS TO</th>
            <th scope="col" id="billing-2">DELIVERY DATE</th>
            <th scope="col" id="billing-3">RATES</th>
        </tr>
    </thead>
   <tbody>
   % for s in smses:
     <tr>
       <td>${s.sms_to}</td>
       <td>${s.timestamp}</td>
       <td>${s.rates}</td>
     </tr>
     </tbody>
   % endfor
   </table></div>
   <br /><br /><br />
   <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#c8d4fd"></ div><br /><br />
   <table id="billing">
    <colgroup>
    	<col class="billing-odd" />
    	<col class="billing-even" />
    	<col class="billing-odd" />
    </colgroup>
    <thead>
    	<tr>
            <th scope="col" id="billing-1">TOTAL PACKAGE RATES</th>
            <td>Rs.${package_rates}/-</td>
            </tr>
         <tr>
            <th scope="col" id="billing-2">TOTAL SMS RATES</th>
            <td>Rs.${smses_rates}/-</td>
         </tr>
         <tr>
            <th scope="col" id="billing-3">TOTAL BILL</th>
            <td>Rs.${total_bill}/-</td>
        </tr>
      </thead>
      </table>
   <br />
 <a href= ${request.route_url('main_page')}><p><center>BACK TO MAIN PAGE</center></p></a>
   <br /><br /><br />
   </ body>
   </html>
