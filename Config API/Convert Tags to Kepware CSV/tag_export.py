# ******************************************************************************
# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------------
#  Name:
#       tag_export.py
# 
#  Description: 
#		This script reads all tags and tag groups from a device via Config API and exports
#		the Kepware formatted CSV for Tag importing through the Config GUI
#		
#  Procedure:
#       1- Setup csv output and delete if previously existed
#       2- iterates through all tag groups and exports the tags found in every tag group.
#  Dependencies:
#       Uses KepConfig package
# 
# ******************************************************************************/

import kepconfig
from kepconfig import connection, error
from kepconfig.connectivity import channel, device, tag
import json
import csv
import os
import time

# output file
output_file = "MyDevice.csv"

# device path
device_path = "Channel1.Device1"

# csv header and JSON mapping
fields = ['Tag Name','Address','Data Type','Respect Data Type',
    'Client Access','Scan Rate','Scaling','Raw Low','Raw High',
    'Scaled Low','Scaled High','Scaled Data Type','Clamp Low',
    'Clamp High','Eng Units','Description','Negate Value']
mapping = {        
    "common.ALLTYPES_NAME": "Tag Name",
    "common.ALLTYPES_DESCRIPTION": "Description",
    "servermain.TAG_ADDRESS": "Address",
    "servermain.TAG_DATA_TYPE": {
        "id": "Data Type",
        "enumeration": {
			"Default": -1,
			"String": 0,
			"Boolean": 1,
			"Char": 2,
			"Byte": 3,
			"Short": 4,
			"Word": 5,
			"Long": 6,
			"DWord": 7,
			"Float": 8,
			"Double": 9,
			"BCD": 10,
			"LBCD": 11,
			"Date": 12,
			"LLong": 13,
			"QWord": 14,
			"String Array": 20,
			"Boolean Array": 21,
			"Char Array": 22,
			"Byte Array": 23,
			"Short Array": 24,
			"Word Array": 25,
			"Long Array": 26,
			"DWord Array": 27,
			"Float Array": 28,
			"Double Array": 29,
			"BCD Array": 30,
			"LBCD Array": 31,
			"Date Array": 32,
			"LLong Array": 33,
			"QWord Array": 34
		}
    },
    "servermain.TAG_READ_WRITE_ACCESS": {
        "id":"Client Access",
        "enumeration": {
			"RO": 0,
			"R/W": 1
		}
    },
    "servermain.TAG_SCAN_RATE_MILLISECONDS": "Scan Rate",
    "servermain.TAG_SCALING_TYPE": {
        "id": "Scaling",
        "enumeration": {
			"None": 0,
			"Linear": 1,
			"Square Root": 2
		}
    }
}
scaling_sub_mapping = {
    "servermain.TAG_SCALING_RAW_LOW": "Raw Low",
    "servermain.TAG_SCALING_RAW_HIGH": "Raw High",
    "servermain.TAG_SCALING_SCALED_DATA_TYPE": {
        "id":"Scaled Data Type",
        "enumeration": {
            "Char": 2,
            "Byte": 3,
            "Short": 4,
            "Word": 5,
            "Long": 6,
            "DWord": 7,
            "Float": 8,
            "Double": 9
        }
    },
    "servermain.TAG_SCALING_SCALED_LOW": "Scaled Low",
    "servermain.TAG_SCALING_SCALED_HIGH": "Scaled High",
    "servermain.TAG_SCALING_CLAMP_LOW": "Clamp Low",
    "servermain.TAG_SCALING_CLAMP_HIGH": "Clamp High",
    "servermain.TAG_SCALING_NEGATE_VALUE": "Negate Value",
    "servermain.TAG_SCALING_UNITS": "Eng Units"
}

def HTTPErrorHandler(err):
    # Generic Handler for exception errors
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


class CsvFormatter():
    def __init__(self):
        self.output = open(output_file, mode= 'x', newline='')
        self.writer = csv.DictWriter(self.output, fields)

    def add_header(self):
        self.writer.writeheader()

    def write(self, record):
        self.writer.writerows(record)
    
    def close(self):
        return self.output.close()

def logger_setup():
    # delete file if exists
    try:
        os.remove(output_file)
    except OSError:
        pass
    
    logger = CsvFormatter()
    logger.add_header()
    return logger

def log_tags(tags, current_path = ''):
    # Processes Tags list and logs to CSV
    ls = []
    for tag in tags:
        output = {}
        # Filter out keys from Tag that are not related to scaling (General property group)
        s = set(mapping.keys())
        non_scale_keys = [v for v in tag.keys() if v in s]

        for k in non_scale_keys:
            if k == 'common.ALLTYPES_NAME':
                name = tag[k]
                if current_path == '':
                    output[mapping[k]] = name
                else:
                    output[mapping[k]] = current_path + '.' + name
            elif k in ['servermain.TAG_DATA_TYPE','servermain.TAG_READ_WRITE_ACCESS']:
                key_list = list(mapping[k]['enumeration'].keys())
                val_list = list(mapping[k]['enumeration'].values())
                output[mapping[k]['id']] = key_list[val_list.index(tag[k])]
            elif k == 'servermain.TAG_SCALING_TYPE':
                if tag[k] == 0:
                    output[mapping[k]['id']] = ""
                    # Map all the scaling related properties to '' for no scaling configuration
                    for scale in scaling_sub_mapping.keys():
                        if scale == 'servermain.TAG_SCALING_SCALED_DATA_TYPE':
                            output[scaling_sub_mapping[scale]['id']] = ""
                        else:
                            output[scaling_sub_mapping[scale]] = ""
                else:
                    # Map all the scaling related properties
                    key_list = list(mapping[k]['enumeration'].keys())
                    val_list = list(mapping[k]['enumeration'].values())
                    output[mapping[k]['id']] = key_list[val_list.index(tag[k])]
                    
                    # Filter out keys from Tag that are related to scaling (Scaling property group)
                    s_scale = set(scaling_sub_mapping.keys())
                    scale_keys = [v for v in tag.keys() if v in s_scale]
                    for l in scale_keys:
                        if l == 'servermain.TAG_SCALING_SCALED_DATA_TYPE':
                            key_list = list(scaling_sub_mapping[l]['enumeration'].keys())
                            val_list = list(scaling_sub_mapping[l]['enumeration'].values())
                            output[scaling_sub_mapping[l]['id']] = key_list[val_list.index(tag[l])]
                        elif l in ["servermain.TAG_SCALING_CLAMP_LOW","servermain.TAG_SCALING_CLAMP_HIGH", 
                                    "servermain.TAG_SCALING_NEGATE_VALUE"]:
                            output[scaling_sub_mapping[l]] = int(tag[l])
                        else:
                             output[scaling_sub_mapping[l]] = tag[l]
            else:
                output[mapping[k]] = tag[k]
        # Append to list of CSV output
        ls.append(output)
    # Write to CSV file
    server_output.write(ls)

def process_tags(current_path):
    tag_path = ''
    path_parts = kepconfig.path_split(current_path)
    try:
        for item in  kepconfig.path_split(current_path)['tag_path']:
            tag_path = tag_path + '.' + item
    except KeyError:
        pass
    except:
        print('Other Error')
    
    try:
        tags = tag.get_all_tags(server, current_path)
    except Exception as err:
        # Retry if call fails
        HTTPErrorHandler(err)
        success = False
        retry = 1
        while retry != 3:
            time.sleep(1)
            try:
                tags = tag.get_all_tags(server, current_path)
                retry = 3
                success = True
            except Exception as err:
                retry = retry + 1
                HTTPErrorHandler(err)
        # If fails three times, move on
        if success == False:
            return False
    log_tags(tags, tag_path)

    try:
        tag_group = tag.get_all_tag_groups(server, current_path)
    except Exception as err:
        # Retry if call fails
        HTTPErrorHandler(err)
        success = False
        retry = 1
        while retry != 3:
            time.sleep(1)
            try:
                tag_group = tag.get_all_tag_groups(server, current_path)
                retry = 3
                success = True
            except Exception as err:
                retry = retry + 1
                HTTPErrorHandler(err)
        # If fails three times, move on
        if success == False:
            return False
    for group in tag_group:
        process_tags(current_path + '.' + group['common.ALLTYPES_NAME'])
    return True

# Create output
server_output = logger_setup()

# Configure Kepware Server API connection
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '', https=False)

dev = kepconfig.path_split(device_path)
# output = {}
current_path = ''
time_start = time.perf_counter()

process_tags(device_path)

server_output.close()

time_end = time.perf_counter()
print('Complete {}! {} - Took {} seconds'.format(os.path.basename(__file__),time.asctime(), time_end - time_start))

