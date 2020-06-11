Enable the Configuration API:
1.	Right-Click on the green EX icon in the system tray and select Settings
2.	Set Enable and Enable HTTP to Yes
3.	Set CORS Allowed Origins to *
4.	Set Enable Documentation to Yes

Install Python:
1.	Download https://www.python.org/downloads/
2.	During the install, check Add Python 3.x to PATH
3.	From a CMD, type ‘pip install requests’ to install the Requests library 

Prepare Script:
1.	Extract DataLoggerToCSV.zip 
2.	View ..\setup.json in a text editor
3.	Set logGroupName to the name of the Log Group in KEPServerEX
4.	Set exportPath to the csv location
5.	Set apiUser and apiPassword to the user and password.  If an Administrator password was created during the KEPServerEX install, enter it here
6.	View ..\csvs\logitems_example.csv in a text editor
7.	Edit Log Items as needed.  Tags must exist on the server

Run the Script
1.	Open a CMD and cd to the CSVtoDataLogger.py location before launching the script or double-click on ..\CSVtoDataLogger.py from File Explorer
2.	If an item fails to get added, a 400 error will appear