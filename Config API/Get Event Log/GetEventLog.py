# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------------
#
# Name: GetEventLog.py
#
# Description:  This script reads Kepware's Event Log through the Config API 
#               and exports it to a .txt file in a desired folder.    
#
# Dependencies:  KepConfig package
#                Kepware Config API enabled 
#
############################################################################


from kepconfig import connection, error
import json
from contextlib import redirect_stdout
import datetime


# This creates a server reference that is used to target all modifications of the Kepware configuration
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')

# Global Variables - Update as needed

# FiletoPath should include: an absolute path like "C:/Users/testUser/Destop" if file needs to be saved on the local machine
#                            an UNC path "//servername/path" if the file needs to be saved on a different shared network drive 
DIR = "PathToFile"

# length of time to look back in request - in Minutes
INTERVAL = 30

# Generic Handler for exception errors
def HTTPErrorHandler(err):
    if err.__class__ is error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    elif err.__class__ is error.KepURLError:
        print(err.url)
        print(err.reason)
    else:
        print('Different Exception Received: {}'.format(err))

# Calculate a 30 minutes polling interval for the Event Log retrieval
currentDate = datetime.datetime.utcnow()
hoursSubstracted = datetime.timedelta(minutes = INTERVAL)
previousDate = currentDate - hoursSubstracted

# Create a TKS Event Log file with date appended to the name
fileName='TKS Log ' + datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
filePath = DIR + fileName

# This is needed so the script can be executed as a scheduled task 


# Write the content of the Event Log into a certain .txt file 
try:
	with open(filePath + '.txt', 'w') as f:
		with redirect_stdout(f):
		#Get the events from the past half hour - max number of events is 1000
			print('Event Log Poll Start Date (UTC):',previousDate,'---- Event Log Poll End Date (UTC):',currentDate)
			print("\n")
			print("{} - {}".format("Thingworx Kepware Server Event Log", json.dumps(server.get_event_log(1000, previousDate, datetime.datetime.utcnow()), indent=4)))		                                                                                                                             
except Exception as err:
    HTTPErrorHandler(err)