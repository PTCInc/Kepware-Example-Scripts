# Count the number of channels, devices, and channels by driver type in a running Kepware Server project

## Install Python and the Kepware Config API Python SDK

1. Download [Python](https://www.python.org/downloads/)
2. During the install
    • Check box "Add python.exe to PATH" (can also be added later under "Advanced Options", check "Add Python to environment variables")
    • Select "Customized Installation"
    • Under "Optional Features", select "pip"
3. Install the [Kepware Config API Python SDK](https://github.com/PTCInc/Kepware-ConfigAPI-SDK-Python)

## Enable the Kepware Server Configuration API

1. Right-Click on the Administration Tool (green icon in the system tray) and select Settings
2. Set Enable and Enable HTTP to Yes
3. Set CORS Allowed Origins to *
4. Set Enable Documentation to Yes

## Run the Script

1. Open a CMD and navigate to the location of [count_channels_and_devices.py](count_channels_and_devices.py)
2. Run the script (type 'python count_channels_and_devices.py' and hit enter)
