# ******************************************************************************
# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
#  Description: 
#		Created as a replacement for DataLogger's CSV Export/Import.  This script 
#		imports a CSV containing log items and POSTs them to the specified Log  
#		Group using the Configuration API      
#
#  Procedure:
#       Read in setup file
#       Read in log item template
#       Read in CSV, convert to json
#       Create log items
#
# ******************************************************************************/

import csv
import json
import requests


def get_parameters(setup_file):
	try:
		print("Loading 'setup.json' from local directory")
		with open(setup_file) as j:
			setup_data = json.load(j)
			print("-- Load succeeded")
		return setup_data
	except Exception as e:
		print("-- Load setup failed - '{}'".format(e))
		return False
		
def get_templates():
	try:
		print("Loading Item JSON template from local directory")
		i_template = open('./objs/logitem.json')
		item = json.load(i_template)
		print("-- Load succeeded")
		return item
	except Exception as e:
		print("-- Load failed - '{}'".format(e))
		return False
		
def convert_csv_to_json(path):
	try:
		print("Converting CSV at '{}' into JSON".format(path))
		csv_file = open(path, 'r')
		reader = csv.DictReader(csv_file)
		out = json.dumps([row for row in reader])
		json_from_csv = json.loads(out)
		print("-- Conversion succeeded")
		return json_from_csv
	except Exception as e:
		print("-- Conversion failed - '{}'".format (e))
		return False

def log_group_enabled(state):
	try:
		print("Changing state of {} to Enabled = {}".format(group,state))
		
		url = "http://127.0.0.1:57412/config/v1/project/_datalogger/log_groups/{}".format (group)
		payload = "{{\"FORCE_UPDATE\": true,\"datalogger.LOG_GROUP_ENABLED\": {}}}".format (state)
		response = requests.put(url, auth=(username, password), data=(payload))

		if response:
			print("-- State change succeeded")
		else:
			print("-- An error has occurred: " + str(response.status_code))
		
	except Exception as e:
		print("-- State change failed - '{}'".format (e))
		return False	
	
def add_items_to_loggroup(list,template):
	try:
		print()
		print("Attempting to add {} items to {}".format ((len(list)),group))
		url = "http://127.0.0.1:57412/config/v1/project/_datalogger/log_groups/{}/log_items".format (group)

		for item in list:
			template['common.ALLTYPES_NAME'] = item['Item_Name']
			template['common.ALLTYPES_DESCRIPTION'] = item['Description']
			template['datalogger.LOG_ITEM_ID'] = item['Item_ID']
			template['datalogger.LOG_ITEM_NUMERIC_ID'] = item['Numeric_Alias']
			template['datalogger.LOG_ITEM_DATA_TYPE'] = item['Data_Type']
			template['datalogger.LOG_ITEM_DEADBAND_TYPE'] = int(item['Deadband_Type'])
			template['datalogger.LOG_ITEM_DEADBAND_VALUE'] = int(item['Deadband'])
			template['datalogger.LOG_ITEM_DEADBAND_LO_RANGE'] = int(item['Range_Low'])
			template['datalogger.LOG_ITEM_DEADBAND_HI_RANGE'] = int(item['Range_High'])
			payload = json.dumps(template)
			
			response = requests.post(url, auth=(username, password), data=(payload))
			
			message = item['Item_Name'] + " = " 
			if response:
				message = message + "Success"
			else:
				message = message + "An error has occurred: " + str(response.status_code)
			print(message)
	except Exception as e:
		print("-- Add failed - '{}'".format (e))
		return False	

# load setup parameters
setupFilePath = 'setup.json'
setupData = get_parameters(setupFilePath)

# assign global variables
group = setupData['logGroupName']
path = setupData['importPath']
username = setupData['apiUser']
password = setupData['apiPassword']

# get json template for item
itemTemplate = get_templates()

# convert CSV file to JSON
itemList = convert_csv_to_json(path)

# disable log group. items can be added to an enabled log group via the API, but let's disable the group anyway 
log_group_enabled('false')

# add tags to log group 
add_items_to_loggroup(itemList,itemTemplate)

# enable log group
print()
log_group_enabled('true')

print()
print("Press any key...")
input()
