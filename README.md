<h1> PyLiteCo </h1>

Thing to control a light using the state of an echo360 recorder

<h2> Supported indicators </h2>
 - Delcom Gen2 Visual Indicator


<h2> Windows service</h2>

This will run pyliteco as a Windows service, logging to the Event Log, starting on automatically on boot.

 - Run the installer (pyliteco-setup.exe).
 - After driver install, the service is installed and starts automatically.
 - Modify the generated pyliteco.json or copy a pre-made version into "C:\Program Files (x86)\pyliteco\" to provide credentials for connecting to the Echo box.
 - The service should recover from most issues (network problems, disconnected indicator, etc) automatically. If not, please file a bug report as mentioned below.


<h2> Configuration Server </h2>

 - Ensure the entry on the webserver data file has the correct IPs for both the box hosting the indicator and the echo box.
 - Also ensure the server has port 80 accessable from each client you will install the service on to.
 
 
<h2> Building from source </h2>
 
PyLiteCo requires Python3, Pywinusb and Pywin32 to run. To additionally build the exe andinstaller, py2exe and NSIS are required. 
If just running the Python script, run <code>python3 \_\_main\_\_.py <path_to_local_config_file></code>
 
<h2> Bug reporting </h2>
Please use the <a href="https://github.com/rrah/PyLiteCo/issues">Github repo issues feature</a>, making sure to include the log file generated. If running as a service, the log entries will appear in the Windows Event Log.
