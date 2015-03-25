<h1> echolight </h1>
<h2> VERY WIP </h2>

Thing to control a light using the state of an echo360 recorder

<h2> Supported indicators </h2>
 - Delcom Gen2 Visual Indicator
 
<h2> Running </h2>
Running the code in the install file as root will install all dependencies and set PyLiteCo to run as a service. It can then be started with

<code>service pyliteco start</code>

Don't forget to copy config.json.example to config.json and set the username and password to the correct value for the echo box.

<h2> To-do </h2>
 - Not run as root
 - Nice .deb?
