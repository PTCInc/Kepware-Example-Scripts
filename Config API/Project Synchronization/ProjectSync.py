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
# -Python on Primary PC with Kepconfig SDK and Paramiko packages
# -OpenSSH on Secondary PC (or other mechanism to copy a project from from the 
#  Primary to the Secondary PC)
#
# Todo:
# -Maybe check the registry for the correct location of ProgramData
# -Add options for scheduling and/or project change detection 
# 
# Change History:
#  v0.0.2 - Updated to kepconfig SDK package for Config API handling and 
# 		removed Requests as requirement
#
#  v0.0.2
# ******************************************************************************/

import json
import time
import paramiko
import os 
import kepconfig
import kepconfig.error as error

print(os.environ["ProgramData"])

def ErrorHandler(err):
	print("-- An error has occurred: ")
    # Generic Handler for exception errors
	if err.__class__ is error.KepError:
		print(err.msg)
	elif err.__class__ is error.KepHTTPError:
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

def save_source_project(server: kepconfig.connection.server):
	try:
		print("Saving project file on '{}'".format(server.host))
		
		unixTime = str(time.time()).replace('.', '') #Use UNIX time to generate a unique filename
		fileName = "Project_{}.opf".format (unixTime)
		
		job = server.save_project('{}\\{}'.format(sourceFolder,fileName))
		
		# check job status for completion
		while True:
			time.sleep(1)
			status = server.service_status(job)
			if (status.complete == True): break
		print("-- Project save successful - '<ProgramData>\Kepware\KEPServerEX\V6\{}\\{}'".format(sourceFolder,fileName))
		return fileName
	except Exception as e:
		print("-- Project failed to save --")
		ErrorHandler(e)
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

def load_destination_project(server: kepconfig.connection.server):
	try:
		print("Loading project file on '{}'".format(destination))
		
		job = server.load_project('{}\\{}'.format(destinationFolder,projectName))
		
		# check job status for completion
		while True:
			time.sleep(1)
			status = server.service_status(job)
			if (status.complete == True): break
		print("-- Project load successful - '{}\\{}'".format(destinationFolder,projectName))
		return
	except Exception as e:
		print("-- Project load failed --")
		ErrorHandler(e)
		return False

# load setup parameters
setupFilePath = './Config API/Project Synchronization/setup.json'
setupData = get_parameters(setupFilePath)

# assign global variables
source = setupData['source']
sourcePort = setupData['sourcePort']
sourceFolder = setupData['sourceFolder']
destination = setupData['destination']
destinationPort = setupData['destinationPort']
destinationFolder = setupData ['destinationFolder']
apiUsername = setupData['apiUser']
apiPassword = setupData['apiPassword']
sshUsername = setupData['sshUser']
sshPassword = setupData['sshPassword']

server_source = kepconfig.connection.server(source, sourcePort, apiUsername, apiPassword, https=False)
server_dest = kepconfig.connection.server(destination, destinationPort, apiUsername, apiPassword, https=False)

# save source project
projectName = save_source_project(server_source)
if projectName is False:
	# TODO Failures
	pass

# move project using sftc over ssh
move_source_project()

# load destination project
load_destination_project(server_dest)

print()
print("Press any key...")
input()
