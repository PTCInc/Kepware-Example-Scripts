Get Kepware's Event log for a certain period of time 

Install Python and the Kepware Config API Python SDK

    Download Python
    During the install, check Add Python 3.x to PATH
    Download and install the Kepware Config API Python SDK

Enable the Kepware Server Configuration API

    Right-Click on the Administration Tool (green icon in the system tray) and select Settings
    Set Enable and Enable HTTP to Yes
    Set CORS Allowed Origins to *
    Set Enable Documentation to Yes

Run the Script

    Open a CMD and navigate to the location of GetEventLog.py
    Run the script (type 'GetEventLog.py' and hit enter)

Optionally

    Set up a scheduled task so the event log can be retrieved periodically based on the defined poll interval 
