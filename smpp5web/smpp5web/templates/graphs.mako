    <%inherit file="base.mako"/>
    <html>
    <head>
    <script>
 
 require(["dojox/charting/Chart", "dojox/charting/axis2d/Default", "dojox/charting/plot2d/Columns", "dojox/charting/themes/Wetland" , "dojo/ready"],
          function(Chart, Default, Columns, Wetland, ready){
            ready(function(){

            chartData = [
            %for i in sms:
            ${i},
            %endfor 
            ];
            
            var c = new Chart("chartOne");
            c.addPlot("default", {type: "Columns", gap: 3});
            c.addAxis("x", {labels: [
            %for i in date:
            {value: ${loop.index+1}, text: "${i}"},
            %endfor 
            ]});
           c.addAxis("y", {vertical: true, min:0});
                c.setTheme(Wetland);
                c.addSeries("Daily SMS Traffic",chartData, {stroke: {color:"#039"}, fill: "#c8d4fd"});

            c.render();
        });
    });
    </script>
    </head>
    <body><br />
    <h1><font color = "#039">&nbsp&nbsp&nbsp${traffic} Sms Traffic     ${name}</h1></ font>
    <br />
    <div style="font-family:verdana;border-radius:4px;height:5px;background-color:#c8d4fd"></ div><br /><br />
    <div id="chartOne" style="width: 400px; height: 240px; margin: 10px auto 0px auto;"></div>
    <br />
    <a href= ${request.route_url('sms_history')}><p><center>BACK</center></p></a>
   <br /><br /><br />
    </body>
