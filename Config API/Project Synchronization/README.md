# Save, Transfer and Load Project File Between Two Kepware Servers

This script is run on the primary server to copy the entire project file to a secondary server.  The Python Paramiko library is used to SFTP the project file over OpenSSH, but the script can be edited to use other file transfer mechanisms instead.

## Install Python

1. Download [Python](https://www.python.org/downloads/)
2. During the install, check Add Python 3.x to PATH
3. From a CMD, type ‘pip install kepconfig’ to install the [Kepware Config API SDK](https://github.com/PTCInc/Kepware-ConfigAPI-SDK-Python) library
4. From a CMD, type ‘pip install paramiko' to install the [Paramiko](https://www.paramiko.org/) library

## Enable the Configuration API on the Primary and Secondary servers

1. Right-Click on the Administration Tool (green icon in the system tray) and select Settings
2. Set Enable and Enable HTTP to Yes - script can be modified as necessary if HTTPS is desired

## Enable File Transfers on Secondary server

1. Install or Enable OpenSSH
2. Create a folder to receive the file transfer.  For example, C:\Projects
3. Enable sharing to this folder

## Prepare Script

1. View [setup.json](setup.json) in a text editor
2. Set source, destination, ports and folder locations
3. Set username and password for the API and SSH users

## Run the Script

1. Open a CMD and cd to the [ProjectSync.py](ProjectSync.py) location before launching the script or double-click on [ProjectSync.py](ProjectSync.py) from File Explorer
