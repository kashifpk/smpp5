    <%inherit file="base.mako"/>
    <html>
    <head>
    <script>
 var arraySer1 = [1, 2, 0.5, 1.5, 1, 2.8, 0.4];
var arraySer2 = [2.6, 1.8, 2, 1, 1.4, 0.7, 2];
var arraySer3 = [6.3, 1.8, 3, 0.5, 4.4, 2.7, 2];

 require(["dojox/charting/Chart", "dojox/charting/axis2d/Default", "dojox/charting/plot2d/Columns", "dojox/charting/themes/Wetland" , "dojo/ready"],
          function(Chart, Default, Columns, Wetland, ready){
            ready(function(){
	    data = []
	    chartData = [
	     { x: "0", y: "0" },
    { x: "1", y: "10" },
    { x: "2", y: "20" },
    { x: "3", y: "30" },
    { x: "4", y: "40" },
    { x: "5", y: "50" },
    { x: "6", y: "60" },
    { x: "7", y: "70" }
];
              var c = new Chart("chartOne");
              c.addPlot("default", {type: Columns, gap:8})
                c.addAxis("x")
c.addAxis("y", {
		vertical: true})
                .setTheme(Wetland)
                .addSeries("Series A",chartData)

            .render();
        });
    });
    </script>
    </head>
    <body>
    <div id="chartOne" style="width: 400px; height: 240px; margin: 10px auto 0px auto;"></div>
    </body>
