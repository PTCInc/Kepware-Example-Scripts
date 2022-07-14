# Activate secodary server when primary is no longer responding

This script is to be run on the secondary server and will disable or enable all supported features including devices, DataLogger groups, IoT Gateway Agents, Schedules and EFM Exporters when the primary server goes offline.  The health of the primary is determined by connecting to the Configuration API port, but a ping can also be used.

## Install Python

1. Download [Python](https://www.python.org/downloads/)
2. During the install, check Add Python 3.x to PATH
3. From a CMD, type ‘pip install requests’ to install the Requests library
4. From a CMD, type ‘pip install paramiko' to install the Paramiko library

## Enable the Configuration API on the Primary and Secondary servers

1. Right-Click on the Administration Tool (green icon in the system tray) and select Settings
2. Set Enable and Enable HTTP to Yes
3. Set CORS Allowed Origins to *

## Enable File Transfers on Secondary server

1. Install or Enable OpenSSH
2. Create a folder to receive the file transfer.  For example, C:\Projects
3. Enable sharing to this folder

## Prepare Script

1. View [setup.json](setup.json) in a text editor
2. Set source, destination, and folder locations
3. Set username and password for the API and SSH users

## Run the Script

1. Open a CMD and cd to the [ProjectSync.py](ProjectSync.py) location before launching the script or double-click on [ProjectSync.py](ProjectSync.py) from File Explorer
