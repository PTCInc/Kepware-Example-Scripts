# ******************************************************************************
#  
#  Description: 
#		Created as a replacement for DataLogger's CSV Export.  This script uses
#		the Configuration API to export a the specified log group to a CSV file
#		that can be edited and re-imported using the CSVtoDataLogger script.
#		exports a log group to CSV where it can be edited and re-imported.  
#
#  Procedure:
#       Read in setup file
#       Get log group items
#       Write log items to CSV
#
# ******************************************************************************/

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

def get_log_group_items(groupName):
	
	try:
		print("Getting log group items for '{}'".format(groupName))
		
		url = "http://127.0.0.1:57412/config/v1/project/_datalogger/log_groups/{}/log_items".format (group)
		response = requests.get(url, auth=(username, password))
		data = json.loads(response.text)
		print("-- Get succeeded")
		return data
	except Exception as e:
		print("-- Get failed - '{}'".format (e))
		return False

def write_to_csv(data,path):
	try:
		print("Writing CSV to '{}'".format(path))
		
		file = open(path, 'w')
		file.write("Item_Name,Item_ID,Numeric_Alias,Data_Type,Deadband_Type,Deadband,Range_Low,Range_High,Description")
		file.write("\n")
		
		for each in data:
			file.write(each['common.ALLTYPES_NAME'] 
			+ "," + each['datalogger.LOG_ITEM_ID'] + "," 
			+ str(each['datalogger.LOG_ITEM_NUMERIC_ID']) + "," 
			+ str(each['datalogger.LOG_ITEM_DATA_TYPE']) + "," 
			+ str(each['datalogger.LOG_ITEM_DEADBAND_TYPE']) + "," 
			+ str(each['datalogger.LOG_ITEM_DEADBAND_VALUE']) + "," 
			+ str(each['datalogger.LOG_ITEM_DEADBAND_LO_RANGE']) + "," 
			+ str(each['datalogger.LOG_ITEM_DEADBAND_HI_RANGE']) + "," 
			+ each['common.ALLTYPES_DESCRIPTION'])
			#must handle last row here
			file.write("\n") #must handle last row here
		print("-- Write succeeded")

	except Exception as e:
		print("-- Write failed - '{}'".format (e))
		return False	
	finally:
		file.close()		

# load setup parameters
setupFilePath = 'setup.json'
setupData = get_parameters(setupFilePath)

# assign global variables
group = setupData['logGroupName']
path = setupData['exportPath']
username = setupData['apiUser']
password = setupData['apiPassword']

# get log group items
logItemData = get_log_group_items(group)

# write to CSV
write_to_csv(logItemData,path)

print()
print("Press any key...")
input()
