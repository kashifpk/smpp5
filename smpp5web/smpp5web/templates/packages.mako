    <%inherit file="base.mako"/>
    <html>
    <body>
    <h1><font color = "#EE872A">&nbsp&nbsp&nbspCurrent Package Detail</h1></ font>
    <br />
    <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#EE872A"></ div><br /><br />
    % if selected_package is None:
        No package has been selected yet 
    % else:
        <table>
        <tr>
        <th>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        Current Package : ${selected_package.package_name}</ th>
        </ tr>
        <tr>
        <th>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        Applied Date    :  ${selected_package.start_date}</ th>
        </ tr>
        <tr>
        <th>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        Expiry Date     :  ${selected_package.end_date}</ th>
        </ tr>
        </ table>
    % endif
    <br />
    <h1><font color = "#EE872A">&nbsp&nbsp&nbspPackages Detail</h1></ font>
    <br />
    <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#EE872A"></ div><br /><br />
    % for p in packages:
    
        <table>
        <tr>
        <th>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        <B>${p.package_name} Package</B></ th><br />
        </ tr>
        <tr><br />
        <th>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        Total Smses&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${p.smses}                                                        </ th>
        </tr>
        <tr><br />
        <th>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        Duration&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${p.duration}                                                        </ th>
        </tr>
        <tr><br />
        <th>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        Rates&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp${p.rates}                                                        </ th>
        </tr>
        <tr></ tr><br />
        <tr>
        <th>
        </ th>
        </ tr>
        </table
        <br />
    % endfor
        <br /><br />
    <h1><font color = "#EE872A">&nbsp&nbsp&nbspPackage Selection</h1></ font><br />
    <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#EE872A"></ div><br /><br />
        <form action="${request.route_url('packages')}" method="POST">
        <select id='package_name' name="package_name">
        <option value="Select package">------Select package------</option>
    % for p in packages:
        <option value="${p.package_name}">${p.package_name}</option>
    % endfor
        </select>
        <input type="submit" value="Apply Package" /></ form>
        <br /><br /><br /><br />
        <U><a href= ${request.route_url('main_page')} ><h2><font color = "#EE872A">&nbsp&nbspBACK TO MAIN PAGE</font><h2></a><p></U>
        <br /><br />
    </ body>
    </html>
