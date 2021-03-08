# ******************************************************************************
# ------------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for license information.
# ------------------------------------------------------------------------------
# 
# Description: 
# This script is run on the primary server to copy the entire project file to 
# a secondary server. The Python Paramiko library is used to SFTP the project 
# file over OpenSSH, but the script can be edited to use other file transfer 
# mechanisms instead.
# 
# Requires:
# -Python on Primary PC with Requests and Paramiko
# -OpenSSH on Secondary PC (or other mechanism to copy a project from from the 
#  Primary to the Secondary PC)
#
# Todo:
# -Fix JSON so that destinationFolder doesn't require 4 backslashes.  Current 
#  workaround is to use "(repr(destinationFolder).replace('\'','')" 
# -Maybe check the registry for the correct location of ProgramData
# -Add options for scheduling and/or project change detection 
#
# ******************************************************************************/

import json
import requests
import time
import paramiko
import os 

print(os.environ["ProgramData"])

def get_parameters(setup_file):
	try:
		print("Loading 'setup.json' from local directory")
		with open(setup_file) as j:
			setup_data = json.load(j)
			print("-- Setup load successful")
		return setup_data
	except Exception as e:
		print("-- Setup data failed to load - '{}'".format(e))
		return False

def save_source_project():
	try:
		print("Saving project file on '{}'".format(source))
		
		unixTime = str(time.time()).replace('.', '') #Use UNIX time to generate a unique filename
		fileName = "Project_{}.opf".format (unixTime)
		url = "http://{}:57412/config/v1/project/services/ProjectSave".format (source)
		payload = "{{\"servermain.PROJECT_FILENAME\": \"{}\\\\{}\"}}".format (sourceFolder,fileName)
		response = requests.put(url, auth=(apiUsername, apiPassword), data=(payload))
		
		if response:
			print("-- Project save successful - '<ProgramData>\Kepware\KEPServerEX\V6\{}\\{}'".format(sourceFolder,fileName))
		else:
			print("-- An error has occurred: " + str(response.text))
			
		return fileName
	except Exception as e:
		print("-- Project failed to save - '{}'".format(e))
		return False
		
def move_source_project():
	
	try:
		print("Moving project file to '{}'".format(destination))
		
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=destination, username=sshUsername, password=sshPassword, port=22)
		sftp_client=ssh.open_sftp()
	
		#Probably should check the registry for the correct location of ProgramData
		fileIn = os.environ["ProgramData"] + "\\Kepware\\KEPServerEX\\V6\\{}\\{}".format (sourceFolder,projectName)
	
		fileOut = "{}\\{}".format (destinationFolder,projectName)

		sftp_client.put(fileIn,fileOut)
		sftp_client.close()
		ssh.close()
		
		print("-- Project move successful - '{}'".format(fileOut))
			
	except Exception as e:
		print("-- Project move failed - '{}'".format(e))
		return False

def load_destination_project():
	try:
		print("Loading project file on '{}'".format(destination))
		
		url = "http://{}:57412/config/v1/project/services/ProjectLoad".format (destination)
		payload = "{{\"servermain.PROJECT_FILENAME\": \"{}\\\\{}\"}}".format (repr(destinationFolder).replace('\'',''),projectName)

		#print(payload)
		response = requests.put(url, auth=(apiUsername, apiPassword), data=(payload))
		
		if response:
			print("-- Project load succeeded")
		else:
			print("-- An error has occurred: " + str(response.text))
			
		return
	except Exception as e:
		print("-- Project load failed - '{}'".format(e))
		return False

# load setup parameters
setupFilePath = 'setup.json'
setupData = get_parameters(setupFilePath)

# assign global variables
source = setupData['source']
sourceFolder = setupData['sourceFolder']
destination = setupData['destination']
destinationFolder = setupData ['destinationFolder']
apiUsername = setupData['apiUser']
apiPassword = setupData['apiPassword']
sshUsername = setupData['sshUser']
sshPassword = setupData['sshPassword']

# save source project
projectName = save_source_project()

# move project using sftc over ssh
move_source_project()

# load destination project
load_destination_project()

print()
print("Press any key...")
input()
