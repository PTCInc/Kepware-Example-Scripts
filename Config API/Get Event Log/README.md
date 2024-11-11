# Query Kepware's Event log for a certain period of time

This script reads the Kepware event log via Config API and exports the last 30 minutes (default) of events to a text file.

## Install Python

1. Download [Python](https://www.python.org/downloads/)
2. During the install
    • Check box "Add python.exe to PATH" (can also be added later under "Advanced Options", check "Add Python to environment variables")
    • Select "Customized Installation"
    • Under "Optional Features", select "pip"
3. Install the [Kepware Config API SDK](https://github.com/PTCInc/Kepware-ConfigAPI-SDK-Python) library

## Enable the Configuration API

1. Right-Click on the Administration Tool (green icon in the system tray) and select Settings
2. Set Enable and Enable HTTP to Yes
3. Set Enable Documentation to Yes

## Prepare Script

1. View [GetEventLog.py](GetEventLog.py) in a text editor
2. Set Kepware Server connection information in the "connection.server" method
3. Set DIR variable to the directory location to output log files
4. Set INTERVAL variable to be the time to look back in the event log query.

## Run the Script

1. Open a CMD and cd to the [GetEventLog.py](GetEventLog.py) location before launching the script or double-click on [GetEventLog.py](GetEventLog.py) from File Explorer

## Optionally

1. Set up a scheduled task so the event log can be retrieved periodically based on the defined poll interval
