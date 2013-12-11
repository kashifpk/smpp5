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
#package #package-2
{
	background: #d0dafd;
	border-bottom: 1px solid #c8d4fd;
}
#package #package-1, #package #package-3
{
	background: #dce4ff;
	border-bottom: 1px solid #d6dfff;
        }
p {color:#369;}
</style>
</head>
    
    <body>
    <h1><font color = "#039">&nbsp&nbsp&nbspPackages Detail</h1></ font>
    <br />
    <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#c8d4fd"></ div><br /><br />
 % for p in packages:
    <table id="package">
    <colgroup>
    	<col class="package-odd" />
    </colgroup>
    <thead>
    	<tr>
            <th scope="col" id="package-1"><center>${p.package_name} Package</center></th>
            <td></td>
            </tr>
     </thead>
     </table>
      <table id="package">
    <colgroup>
    	<col class="package-odd" />
    	<col class="package-even" />
    	<col class="package-odd" />
    </colgroup>
    <thead>
    	<tr>
            <th scope="col" id="package-1">TOTAL SMSES</th>
            <td>${p.smses}</td>
        </tr>
        <tr>
            <th scope="col" id="package-2">DURATION</th>
            <td>${p.duration}</td>
        </tr>
        <tr>
            <th scope="col" id="package-3">RATES</th>
            <td>${p.rates}</td>
        </tr>
    </thead>
    </table>
  <br /><br />
 % endfor
        <br /><br />
    <h1><font color = "#039">&nbsp&nbsp&nbspPackage Selection</h1></ font><br />
    <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#c8d4fd"></ div><br /><br />
        <form action="${request.route_url('select_packages')}" method="POST">
        <select id='package_name' name="package_name">
        <option value="Select package">------Select package------</option>
    % for p in packages:
        <option value="${p.package_name}">${p.package_name}</option>
    % endfor
        </select>
        <input type="submit" value="Apply Package" /></form>
        <br />
        <a href= ${request.route_url('main_page')}><p><center>BACK TO MAIN PAGE</center></p></a>
   <br /><br /><br />
   </ body>
   </html>
