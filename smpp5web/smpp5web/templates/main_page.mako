    <%inherit file="base.mako"/>
    <html>
    <head>
    <script>
    function bigImg(x)
    {
    x.style.height="64px";
    x.style.width="64px";
    }
    
    function normalImg(x)
    {
    x.style.height="42px";
    x.style.width="42px";
    }
    </script>
    </head>
    <body>
    <%def name="title()">Welcome</%def>
    <br />
    
    <div><h1><font color="#EE872A">Welcome To Customer Self Care</ font></ h1></div><br />
    Dear ${user},<br /><br />
    <font color="grey">
    You can now select from a wide range of products offered. You can find out or change any information required.
    From viewing history to package coversion, from switching tariffs to Calculate billing,
    every thing is now just a click away. Please select from the options below.</ font>
    <br /><br />
    <div style="font-family:verdana;border-radius:0px;solid #EE872A; background-color:#EE872A">
    <font color="white" size="2">BILLING SERVICES:</ font>
    </div>
    <div><br />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    <a href= ${request.route_url('billing')}><img onmouseover="bigImg(this)" onmouseout="normalImg(this)" border="0" src="${request.static_url('smpp5web:static/pencil.jpeg')}"  alt="pyck" width="42" height="42"/></ a>
    </ div><br /><br />
    <div style="font-family:verdana;position:absolute;left:10px;padding:5px;width:130px;border-radius:3px;border:5px solid #EE872A">
    <font color="#EE872A" size="2">Transactions details</ font>
    </div>
    <br /><br /><br /><br /><br /><br /><br /><br />
    <div style="font-family:verdana;border-radius:0px;solid #EE872A; background-color:#EE872A">
    <font color="white" size="2">PACKAGE SERVICES:</ font>
    </div>
    
    <div><br />&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    <a href = ${request.route_url('packages')}><img onmouseover="bigImg(this)" onmouseout="normalImg(this)" border="0" src="${request.static_url('smpp5web:static/notes.jpg')}"  alt="pyck" width="42" height="42"/></ a>
    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    <a href = ${request.route_url('sms_history')}><img onmouseover="bigImg(this)" onmouseout="normalImg(this)" border="0" src="${request.static_url('smpp5web:static/sms.jpeg')}"  alt="pyck" width="42" height="42"/></a>
    </ div>
    <br /><br />
    
    <div style="font-family:verdana;position:absolute;left:10px;padding:5px;width:130px;border-radius:3px;border:5px solid #EE872A">
    <font color="#EE872A" size="3">Package Selection</ font>
    </div>
    <div style="font-family:verdana;position:absolute;left:300px;padding:5px;width:130px;border-radius:3px;border:5px solid #EE872A">
    <font color="#EE872A" size="3">Sms History</ font>
    </div>
    
    
    <br /><br /><br /><br /><br /><br /><br /><br />
    
    
    
    
    </ html></ body>
