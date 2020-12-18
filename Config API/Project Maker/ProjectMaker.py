# ******************************************************************************
# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
#  Description: 
#    Creates a standardized project file for hardware testing  
#    		     
#  Revision 1.1
#
# ******************************************************************************/

import json
import requests
import os
import csv
import time
import copy

channelList = []

def get_parameters(path):
	try:
		print("Loading settings from {}".format(path))
		with open(path) as j:
			data = json.load(j)
		return data
	except Exception as e:
		print("[Exception] Load failed - {}".format(e))
		return False

def get_template(path):
    try:
        print("Loading template from {}".format(path))
        template = open(path)
        item = json.load(template)
        return item
    except Exception as e:
        print("[Exception] Loading failed - '{}'".format(e))
        return False

def get_channel_list(path):
    try:
        print("Getting channel list from {}".format(path))
        for file in os.listdir(path):
            if file.endswith(".json"):
                channelList.append(os.path.splitext(file)[0])
        return channelList
    except Exception as e:
        print("[Exception] Unable to get channel list - '{}'".format(e))
        return False

def get_tag_list(path):
    try:
        print("Getting tag list from {}".format(path))
        csv_file = open(path, 'r', encoding="utf-8-sig") #Seems to work with ANSI and UTF-8 
        reader = csv.DictReader(csv_file)
        out = json.dumps([row for row in reader])
        json_from_csv = json.loads(out)
        return json_from_csv
    except Exception as e:
        print("[Exception] Unable to get tag list - '{}'".format (e))
        return False

def delete_channels():
    try:
        # get all channel properties
        url = "http://{}:{}/config/v1/project/channels".format(host,port)
        response = requests.get(url, auth=(apiUsername, apiPassword))
        channelProps = json.loads(response.text)
    
        # delete each channel
        for each in channelProps:
            channelName = (each['common.ALLTYPES_NAME'])
            url = "http://{}:{}/config/v1/project/channels/{}".format(host,port,channelName)
            response = requests.delete(url, auth=(apiUsername, apiPassword))

            message = "Deleting channel {} - ".format(channelName)
            if response:
                message = message + "Success"
            else:
                message = message + "An error has occurred: " + str(response.text)
            print(message)
    except Exception as e:
        print("[Exception] Deleting channel - '{}'".format(e))
        return False

def create_channel(cTemplate,tTemplate,thisChannel):
    try:
        channelData = get_parameters("./Channels/" + thisChannel + ".json")

        url = "http://{}:{}/config/v1/project/channels".format(host,port)

        cTemplate[0]['common.ALLTYPES_NAME'] = thisChannel
        cTemplate[0]['servermain.MULTIPLE_TYPES_DEVICE_DRIVER'] = channelData['driver']
        cTemplate[0]['devices'][0]['common.ALLTYPES_NAME'] = channelData['deviceName']
        cTemplate[0]['devices'][0]['servermain.DEVICE_ID_STRING'] = channelData['deviceID']
        cTemplate[0]['devices'][0]['servermain.DEVICE_MODEL'] = int(channelData['deviceModel'])
        cTemplate[0]['devices'][0]['servermain.MULTIPLE_TYPES_DEVICE_DRIVER'] = channelData['driver']

        # create tag list
        tagList = get_tag_list(channelData['tagPath'])
        tagCount = len(tagList)
        tagPayload = []
        for each in tagList:
            tTemplate['common.ALLTYPES_NAME'] = each['Tag Name']
            tTemplate['common.ALLTYPES_DESCRIPTION'] = each['Description']
            tTemplate['servermain.TAG_ADDRESS'] = each['Address']
            try: 
                tTemplate['servermain.TAG_DATA_TYPE'] = int(tagEnumeration[each['Data Type']])
            except:
                print("Datatype not supported.  Reverting tag {} with type {} to Default".format(each['Tag Name'],each['Data Type']))
                tTemplate['servermain.TAG_DATA_TYPE'] = -1

            tagPayload.append(tTemplate.copy())
        
        cTemplate[0]['devices'][0]['tags'] = tagPayload
        payload = json.dumps(cTemplate)

        # send request
        response = requests.post(url, auth=(apiUsername, apiPassword), data=(payload))

        message = "Creating channel {} and device {} with {} tags - ".format(cTemplate[0]['common.ALLTYPES_NAME'],cTemplate[0]['devices'][0]['common.ALLTYPES_NAME'],tagCount)
        if response:
            message = message + "Success"
        else:
            message = message + "An error has occurred: " + str(response.text)
        print(message)

    except Exception as e:
        print("[Exception] Creating channel - '{}'".format(e))

def delete_mqtt_agents():
    try:
        # get all channel properties
        url = "http://{}:{}/config/v1/project/_iot_gateway/mqtt_clients".format(host,port)
        response = requests.get(url, auth=(apiUsername, apiPassword))
        agentProps = json.loads(response.text)
    
        # delete each channel
        for each in agentProps:
            agentName = (each['common.ALLTYPES_NAME'])
            url = "http://{}:{}/config/v1/project/_iot_gateway/mqtt_clients/{}".format(host,port,agentName)
            response = requests.delete(url, auth=(apiUsername, apiPassword))

            message = "Deleting agent {} - ".format(agentName)
            if response:
                message = message + "Success"
            else:
                message = message + "An error has occurred: " + str(response.text)
            print(message)
    except Exception as e:
        print("[Exception] Deleting agent - '{}'".format(e))
        return False

def create_mqtt_agent(mTemplate):
    try:
        mqttPayload = []
        agentName = "MQTT Client"

        url = "http://{}:{}/config/v1/project/_iot_gateway/mqtt_clients".format(host,port)

        mTemplate['common.ALLTYPES_NAME'] = mqttAgentName
        mTemplate['iot_gateway.AGENTTYPES_TYPE'] = agentName
        mTemplate['iot_gateway.MQTT_CLIENT_URL'] = mqttUrl
        mTemplate['iot_gateway.MQTT_CLIENT_TOPIC'] = mqttTopic
        mTemplate['iot_gateway.AGENTTYPES_RATE_MS'] = int(mqttPublishRate)
        mTemplate['iot_gateway.MQTT_CLIENT_CLIENT_ID'] = mqttClientID
        mTemplate['iot_gateway.MQTT_CLIENT_USERNAME'] = mqttUsername
        mTemplate['iot_gateway.MQTT_CLIENT_PASSWORD'] = mqttPassword
        
        mqttPayload.append(mTemplate)
        payload = json.dumps(mqttPayload)

        # send request
        response = requests.post(url, auth=(apiUsername, apiPassword), data=(payload))

        message = "Creating MQTT Agent {} - ".format(agentName)
        if response:
            message = message + "Success"
        else:
            message = message + "An error has occurred: " + str(response.text)
        print(message)

    except Exception as e:
        print("[Exception] Creating MQTT agent - '{}'".format(e))

def create_mqtt_items(iTemplate,thisChannel):
    try:
        # get channel data from file
        channelData = get_parameters("./Channels/" + thisChannel + ".json")
        
        channelName = thisChannel
        deviceName = channelData['deviceName']

        url = "http://{}:{}/config/v1/project/_iot_gateway/mqtt_clients/{}/iot_items".format(host,port,mqttAgentName)

        # create tag list from file
        tagList = get_tag_list(channelData['tagPath'])
        tagCount = len(tagList)
        itemPayload = []

        for each in tagList:
            tagName = each['Tag Name']
            fullTagName = "{}.{}.{}".format(channelName,deviceName,tagName)
            iTemplate['common.ALLTYPES_NAME'] = fullTagName.replace(".","_")
            iTemplate['common.ALLTYPES_DESCRIPTION'] = each['Description'] 
            iTemplate['iot_gateway.IOT_ITEM_SERVER_TAG'] = fullTagName
            iTemplate['iot_gateway.IOT_ITEM_SCAN_RATE_MS'] = 1000 
            try: 
                iTemplate['iot_gateway.IOT_ITEM_DATA_TYPE'] = int(tagEnumeration[each['Data Type']])
            except:
                print("Datatype not supported.  Reverting tag {} with type {} to Default".format(each['Tag Name'],each['Data Type']))
                iTemplate['iot_gateway.IOT_ITEM_DATA_TYPE'] = -1

            itemPayload.append(iTemplate.copy())
        
        payload = json.dumps(itemPayload)

        # send request
        response = requests.post(url, auth=(apiUsername, apiPassword), data=(payload))

        message = "Adding tags to agent {} - ".format(mqttAgentName)
        if response:
            message = message + "Success"
        else:
            message = message + "An error has occurred: " + str(response.text)
        print(message)

    except Exception as e:
        print("[Exception] Adding items to agent - '{}'".format(e))
            
print()

# load setup parameters
setupData = get_parameters('./setup.json')

# assign global variables
host = setupData['api'][0]['host']
port = setupData['api'][0]['port']
apiUsername = setupData['api'][0]['apiUsername']
apiPassword = setupData['api'][0]['apiPassword']

try:
    mqttAgentName = "MQTT Agent"
    mqttUrl = setupData['mqtt'][0]["url"]
    mqttTopic = setupData['mqtt'][0]["topic"]
    mqttPublishRate = setupData['mqtt'][0]["publishRate"]
    mqttClientID = setupData['mqtt'][0]["ClientID"]
    mqttUsername = setupData['mqtt'][0]["mqttUsername"]
    mqttPassword = setupData['mqtt'][0]["mqttPassword"]
    usingMQTT = True
except:
    usingMQTT = False
    print("No MQTT Configuration Found")

# load channel template
channelTemplate = get_template('./Objects/ChannelTemplate.json')

# load tag template
tagTemplate = get_template('./Objects/TagTemplate.json')

# load tag enumeration
tagEnumeration = get_template('./Objects/TagEnumeration.json')

# find files in channels directory
channelList = get_channel_list('./Channels')

# delete all mqtt agents
delete_mqtt_agents()

# give time for server to drop tag references?
time.sleep(5) 

# delete all channels.  maybe make this into a project replacement 
delete_channels()

# create channels
if channelList:
    for each in channelList:
        create_channel(channelTemplate,tagTemplate,each)
else:
    print("No channels to create!")

# create mqtt agent
if usingMQTT:
    mqttAgentTemplate = get_template('./Objects/MqttAgentTemplate.json')
    create_mqtt_agent(mqttAgentTemplate)
# add all tags to agent
    mqttItemTemplate = get_template('./Objects/MqttItemTemplate.json')
    if channelList:
        for each in channelList:
            create_mqtt_items(mqttItemTemplate,each)


#print("Press any key...")
#input()