# Count the number of channels and devices in a Kepware Server Project

## Install Python and the Kepware Config API Python SDK

1. Download [Python](https://www.python.org/downloads/)
2. During the install, check Add Python 3.x to PATH
3. Download and extract Kepware Config API Python SDK from https://github.com/PTCInc/Kepware-ConfigAPI-SDK-Python
4. Within the extracted contents, run setup.py to install Kepware Config API Python SDK

## Enable the Kepware Server Configuration API

1. Right-Click on the Administration Tool (green icon in the system tray) and select Settings
2. Set Enable and Enable HTTP to Yes
3. Set CORS Allowed Origins to *
4. Set Enable Documentation to Yes

## Run the Script

1. Open a CMD and navigate to the location of [count_channels_and_devices.py](count_channels_and_devices.py)
2. Run the script (type 'python count_channels_and_devices.py' and hit enter)
