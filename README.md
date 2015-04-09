<h1> PyLiteCo </h1>

Thing to control a light using the state of an echo360 recorder

<h2> Supported indicators </h2>
 - Delcom Gen2 Visual Indicator
 
 
<h2> Linux </h2>
Running the code in the install file as root will install all dependencies and set PyLiteCo to run as a service. It can then be started with

<code>service pyliteco start</code>

Don't forget to copy config.json.example to config.json and set the username and password to the correct value for the echo box.


<h2> Windows service</h2>

This will run pyliteco as a Windows service, logging to the Event Log, starting on automatically on boot.

 - Run the installer (pyliteco-setup.exe).
 - During installation you'll be prompted to install the LibUSB drivers for the Delcom indicators. Ensure an indicator is connected during this process.
 - After driver install, the service is installed and starts automatically.
 - Modify the generated pyliteco.json or copy a pre-made version into "C:\Program Files (x86)\pyliteco\" to provide credentials for connecting to the Echo box.


<h2> Configuration Server </h2>

 - Ensure the entry on the webserver data file has the correct IPs for both the box hosting the indicator and the echo box.


<h2> To-do </h2>
 - Not run as root
 - Nice .deb?
 - Document server side
 - Silent install
 - Uninstaller