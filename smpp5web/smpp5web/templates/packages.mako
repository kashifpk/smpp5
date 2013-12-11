    <%inherit file="base.mako"/>
    <html>
    <head>
<style>
#package
{
	font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
	font-size: 12px;
	width: 100%;
	text-align: left;
	border-collapse: collapse;
}
#package th
{
	font-size: 14px;
	font-weight: normal;
	padding: 12px 15px;
	border-right: 1px solid #fff;
	border-left: 1px solid #fff;
	color: #039;
}
#package td
{
	padding: 8px 15px;
	border-right: 1px solid #fff;
	border-left: 1px solid #fff;
	color: #669;
}
.package-odd
{
	background: #eff2ff;
}
.package-even
{
	background: #e8edff;
}
#package #package-2, #package #package-4
{
	background: #d0dafd;
	border-bottom: 1px solid #c8d4fd;
}
#package #package-1, #package #package-3, #package #package-5
{
	background: #dce4ff;
	border-bottom: 1px solid #d6dfff;
        }
p {color:#369;}
</style>
</head>
    
    <body>
    <h1><font color = "#039">&nbsp&nbsp&nbspCurrent Package Detail</h1></ font>
    <br />
    <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#c8d4fd"></ div><br /><br />
    % if selected_package is None:
        <center>No package has been selected yet </center>
    % elif end_month<today_month:
        <center>Your Package has been expired or there are not remaining sms.. </center>
        <center>Resubscribe the package <a href= ${request.route_url('select_packages')}>here</a></center>
    % elif end_month==today_month:
        % if end_date > today_date and int(selected_package.smses) > 0:
            <center>Your Package has been expired or there are not remaining sms.. </center>
            <center>Resubscribe the package <a href= ${request.route_url('select_packages')}>here</a></center>
        % elif end_date < today_date and int(selected_package.smses) == 0:
            <center>Your Package has been expired or there are not remaining sms.. </center>
            <center>Resubscribe the package <a href= ${request.route_url('select_packages')}>here</a></center>
        % endif
    % else:
    
    <table id="package">
    <colgroup>
    	<col class="package-odd" />
    	<col class="package-even" />
    	<col class="package-odd" />
        <col class="package-even" />
    </colgroup>
    <thead>
    	<tr>
            <th scope="col" id="package-1">Current Package</th>
            <td>${selected_package.package_name}</td>
            </tr>
         <tr>
            <th scope="col" id="package-2">Applied Date</th>
            <td>${selected_package.start_date}</td>
         </tr>
         <tr>
            <th scope="col" id="package-3"> Expiry Date </th>
            <td>${selected_package.end_date}</td>
        </tr>
        <tr>
            <th scope="col" id="package-4"> Remaining Sms</th>
            <td>${selected_package.smses}</td>
        </tr>
      </thead>
      </table>
    % endif
    <br />
        <a href= ${request.route_url('main_page')}><p><center>BACK TO MAIN PAGE</center></p></a>
   <br /><br /><br />
    </ body>
    </html>
