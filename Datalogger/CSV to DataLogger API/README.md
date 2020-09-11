# Import Datalogger Log Items from CSV using the Configuration API

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

1. View [..\setup.json](setup.json) in a text editor
2. Set logGroupName to the name of the Log Group in KEPServerEX
3. Set importPath to the csv location
4. Set apiUser and apiPassword to the user and password.  If an Administrator password was created during the KEPServerEX install, enter it here
5. View [..\csvs\logitems_example.csv](\csvs\logitems_example.csv) in a text editor
6. Edit Log Items as needed.  Tags must exist on the server

## Run the Script

1. Open a CMD and cd to the [CSVtoDataLogger.py](CSVtoDataLogger.py) location before launching the script or double-click on [..\CSVtoDataLogger.py](CSVtoDataLogger.py) from File Explorer
2. If an item fails to get added, a HTTP 400 error will appear
