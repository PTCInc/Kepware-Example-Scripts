# Convert Tags from Config API to Kepware formatted CSV for Importing

This script reads all tags and tag groups from a device via Config API and exports the Kepware formatted CSV for Tag importing through the Config GUI

## Install Python

1. Download [Python](https://www.python.org/downloads/)
2. During the install, check Add Python 3.x to PATH
3. Install the [Kepware Config API SDK](https://github.com/PTCInc/Kepware-ConfigAPI-SDK-Python) library

## Enable the Configuration API

1. Right-Click on the Administration Tool (green icon in the system tray) and select Settings
2. Set Enable and Enable HTTP to Yes
3. Set CORS Allowed Origins to *
4. Set Enable Documentation to Yes

## Prepare Script

1. View [tag_export.py](tag_export.py) in a text editor
2. Set Kepware Server connection information in the "connection.server" method
3. Set output_file to the csv location
4. Set device_path to the channel.device location in the Kepware configuration

## Run the Script

1. Open a CMD and cd to the [tag_export.py](tag_export.py) location before launching the script or double-click on [tag_export.py](tag_export.py) from File Explorer
