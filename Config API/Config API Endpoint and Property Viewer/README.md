# Kepware Configuration API Endpoint and Property Viewer

This provides a simple UI application to help navigate the documentation endpoints included in the Kepware Configuration API. The doc endpoints provide the API uri mapping and property definitions for all configuration items in Kepware.

## Install Python

1. Download [Python](https://www.python.org/downloads/)
2. During the install
    • Check box "Add python.exe to PATH" (can also be added later under "Advanced Options", check "Add Python to environment variables")
    • Select "Customized Installation"
    • Under "Optional Features", select "pip"
3. From a CMD, type ‘pip install kepconfig’ to install the [Kepconfig](https://github.com/PTCInc/Kepware-ConfigAPI-SDK-Python) package

## Enable the Configuration API on Kepware Server

1. Right-Click on the Administration Tool (green icon in the system tray) and select Settings
2. Set Enable and Enable HTTP to Yes

## Use the Application

1. Open a CMD and cd to the [API_gui.py](API_gui.py) location before launching the script or double-click on [API_gui.py](API_gui.py) from File Explorer. This will launch the UI.
2. Provide the correct parameters to connect to the Kepware Server instance and click the *Connect* button.
3. Once connected navigate the components in the tree by double clicking on each item. If there are children of the object, they will appear.
4. Search is available for the text within the property definition window.
