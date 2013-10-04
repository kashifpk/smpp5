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
            c.addPlot("default", {type: "Columns", gap: 5});
            c.addAxis("x", {labels: [
            %for i in date:
            {value: ${loop.index+1}, text: "${i}"},
            %endfor 
            ]});
           c.addAxis("y", {vertical: true, min:0});
                c.setTheme(Wetland);
                c.addSeries("Daily SMS Traffic",chartData);

            c.render();
        });
    });
    </script>
    </head>
    <body>
    <div id="chartOne" style="width: 400px; height: 240px; margin: 10px auto 0px auto;"></div>
    </body>
