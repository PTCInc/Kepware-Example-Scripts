# Export Datalogger Log Items to CSV using the Configuration API

## Install Python

1. Download [Python](https://www.python.org/downloads/)
2. During the install, check Add Python 3.x to PATH
3. From a CMD, type ‘pip install requests’ to install the [Requests](https://2.python-requests.org/en/master/) library

## Enable the Configuration API

1. Right-Click on the Administration Tool (green icon in the system tray) and select Settings
2. Set Enable and Enable HTTP to Yes
3. Set CORS Allowed Origins to *
4. Set Enable Documentation to Yes

## Prepare Script

1. View [setup.json](setup.json) in a text editor
2. Set logGroupName to the name of the Log Group in KEPServerEX
3. Set exportPath to the csv location and filename
4. Set apiUser and apiPassword to the user and password.  If an Administrator password was created during the KEPServerEX install, enter it here

## Run the Script

1. Open a CMD and cd to the [DataLoggerToCSV.py](DataLoggerToCSV.py) location before launching the script or double-click on [DataLoggerToCSV.py](DataLoggerToCSV.py) from File Explorer
2. Once complete, a csv will appear in the location specified in the [setup.json](setup.json) file