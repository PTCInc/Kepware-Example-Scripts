# ******************************************************************************
# ------------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for license information.
# ------------------------------------------------------------------------------
# 
# Description: 
# This script is to be run on the secondary server and will disable or enable all 
# supported features including devices, DataLogger groups, IoT Gateway Agents, 
# Schedules and EFM Exporters when the primary server goes offline.  The health 
# of the primary is determined by connecting to the Configuration API port, but a 
# ping can also be used.
# 
# Requires:
# Python on Primary PC with Requests library
#
# Todo:
#
# ******************************************************************************/

import json
import requests
import time
import datetime
import socket

import platform
import subprocess

def get_setup_parameters(path):
    try:
        print("Loading settings from {}".format(path))
        with open(path) as j:
            data = json.load(j)
        return data
    except Exception as e:
        print("[Exception] Load failed - {}".format(e))
        return False

def check_ping(host):
    try:
        print("Pinging {}".format(host))
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', host]
        return subprocess.call(command) == 0
    except:
        return False

def check_socket(host,port):
    s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

def objects(host,port,state):
    baseUrl = "http://{}:{}/config/v1/project".format(host, port)
    
    #convert a bool to a string
    sState = str(state).lower()
    
    try:
        #Check for Channels
        url = baseUrl + "/channels"
        enableProperty = "servermain.DEVICE_DATA_COLLECTION"

        channelProperties = get_properties(url,host,port)
        
        for eachChannel in channelProperties:
            thisChannel = (eachChannel['common.ALLTYPES_NAME'])

            #Check for Devices within Channel
            deviceUrl = url + "/" + thisChannel + "/devices"
            deviceProperties = get_properties(deviceUrl,host,port) 

            if deviceProperties: set_properties(deviceProperties,deviceUrl,enableProperty,sState)

        #Check for DataLogger groups
        url = baseUrl + "/_datalogger/log_groups"
        enableProperty = "datalogger.LOG_GROUP_ENABLED"

        properties = get_properties(url,host,port)
        if properties: set_properties(properties,url,enableProperty,sState)
      
        #Check for MQTT clients
        url = baseUrl + "/_iot_gateway/mqtt_clients"
        enableProperty = "iot_gateway.AGENTTYPES_ENABLED"

        properties = get_properties(url,host,port)
        if properties: set_properties(properties,url,enableProperty,sState)

        #Check for REST clients
        url = baseUrl + "/_iot_gateway/rest_clients"
        enableProperty = "iot_gateway.AGENTTYPES_ENABLED"

        properties = get_properties(url,host,port)
        if properties: set_properties(properties,url,enableProperty,sState)
        
        #Check for REST servers
        url = baseUrl + "/_iot_gateway/rest_servers"
        enableProperty = "iot_gateway.AGENTTYPES_ENABLED"

        properties = get_properties(url,host,port)
        if properties: set_properties(properties,url,enableProperty,sState)
        
        #Check for Schedules
        url = baseUrl + "/_scheduler/schedules"
        enableProperty = "scheduler.SCHEDULE_ENABLED"

        properties = get_properties(url,host,port)
        if properties: set_properties(properties,url,enableProperty,sState)
        
        #Check for EFM exporters
        url = baseUrl + "/_efmexporter/poll_groups"
        enableProperty = "efm_exporter.POLLGROUP_ENABLED"

        properties = get_properties(url,host,port)
        if properties: set_properties(properties,url,enableProperty,sState)

        return True

    except Exception as e:
        print("[Exception] Failed - {}".format(e))
        return False

def get_properties(url,host,port):
    try:
        response = requests.get(url, auth=(apiUsername, apiPassword))
        if response:
            return json.loads(response.text)
        else:
            return False        
    except:
        empty = {}
        return empty

def set_properties(properties,url,enableProperty,sState):
    try:
        for each in properties:
            name = (each['common.ALLTYPES_NAME'])
            setUrl = url + "/" + name
            payload = "{{\"FORCE_UPDATE\": true,\"{}\": {}}}".format(enableProperty,sState)
            response = requests.put(setUrl, auth=(apiUsername, apiPassword), data=(payload))

            message = "- {} - ".format(name)
            if not response:
                message = message + "An error has occurred: " + str(response.text)
                print(message)        

    except Exception as e:
        print("[Exception] Failed to set property - {}".format(e))
        return False

# load setup parameters
setupData = get_setup_parameters('./setup.json')

# assign global variables
primaryHost = setupData['primaryHost']
primaryPort = setupData['primaryPort']
secondaryHost = setupData['secondaryHost']
secondaryPort = setupData['secondaryPort']
apiUsername = setupData['apiUsername']
apiPassword = setupData['apiPassword']

# be sure to use explicit operators (== or !=) to compare values since this is somewhat of a tri-state bool
# none = unknown, true = objects are enabled, false = objects are disabled
primaryState = None
secondaryState = None

while True:
    # check health by connecting to the Configuration API's port
    primaryAvailable = check_socket(primaryHost,primaryPort)
    secondaryAvailable = check_socket(secondaryHost,secondaryPort)

    if not secondaryAvailable:
        print("{} - [Warning] Secondary not available - Please ensure Configuration API is enabled".format(datetime.datetime.now()))

    # or use a ping
    #primaryAvailable = check_ping(primaryHost)
    #secondaryAvailable = check_ping(secondaryHost)

    # if connection is lost, assume state is unknown
    if not primaryAvailable: primaryState = None
    if not secondaryAvailable: secondaryState = None

    if primaryAvailable:
        # enable primary if needed
        if primaryState != True:
            result = objects(primaryHost,primaryPort,True)
            if result: 
                primaryState = True
                print("{} - Primary has been enabled".format(datetime.datetime.now()))
        # only attempt to disable the secondary when it's available to avoid errors
        if secondaryAvailable and secondaryState != False:
            result = objects(secondaryHost,secondaryPort,False)
            if result: 
                secondaryState = False 
                print("{} - Secondary has been disabled".format(datetime.datetime.now()))
    else:
        # enable secondary if needed. not necessary to disable primary since it's unavailabe 
        if secondaryAvailable and secondaryState != True:
            result = objects(secondaryHost,secondaryPort,True)
            if result: 
                secondaryState = True
                print("{} - Secondary has been enabled".format(datetime.datetime.now()))

    time.sleep(1)