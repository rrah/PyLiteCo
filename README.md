<h1> PyLiteCo </h1>

Thing to control a light using the state of an echo360 recorder

<h2> Supported indicators </h2>
 - Delcom Gen2 Visual Indicator


<h2> Windows service</h2>

This will run pyliteco as a Windows service, logging to the Event Log, starting on automatically on boot.

 - Run the installer (pyliteco-setup.exe).
 - During installation you'll be prompted to install the LibUSB drivers for the Delcom indicators. Ensure an indicator is connected during this process.
 - After driver install, the service is installed and starts automatically.
 - Modify the generated pyliteco.json or copy a pre-made version into "C:\Program Files (x86)\pyliteco\" to provide credentials for connecting to the Echo box.
 - You may need to restart the service for it to work


<h2> Configuration Server </h2>

 - Ensure the entry on the webserver data file has the correct IPs for both the box hosting the indicator and the echo box.


<h2> To-do </h2>
 - Document server side
 - Silent install
 - ~~Uninstaller~~