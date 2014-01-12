<%inherit file="base.mako"/>

<%def name="title()">
PyCK Web Development Framework
</%def>

<%def name="header()">
  <div id="top" style="text-align: center">
    <br /><br /><br />
    <img src="${request.static_url('smpp5web:static/smpp.png')}"  alt="pyck"/>
  </div>
  ${self.main_menu()}
</%def>
<center>
     <img src="${request.static_url('smpp5web:static/smpp1.jpg')}"  alt="pyck"/></center>
    <div>
      <div class="middle align-center">
        <p class="app-welcome">
          Welcome to Short Message Peer To Peer Protocol Web Interface,<br/>
          developed using PyCK web application development framework.
        </p>
      </div>
    </div>
    
