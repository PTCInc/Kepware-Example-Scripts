# ******************************************************************************
# ------------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for license information.
# ------------------------------------------------------------------------------
# 
# Description: 
# This script is to be run on the secondary Kepware server and will disable or enable all 
# supported features including devices, DataLogger groups, IoT Gateway Agents, 
# Schedules and EFM Exporters when the primary server goes offline.  The health 
# of the primary is determined by verifying the port for the Configuration API is open, but a 
# ping can also be used.
# 
# Requires:
# Python on secondary Kepware server PC with Kepconfig package
# 
# Update History:
# 0.2.0:    Updated to leverage Kepconfig package 
#           Added HTTPS support
#           Use API call instead of port check for status validation
#
# Version:  0.2.0
# ******************************************************************************/

import json
import time
import datetime
import socket
from kepconfig.connection import server
from kepconfig.connectivity import channel, device
from kepconfig.datalogger import log_group
from kepconfig.iot_gateway import agent, MQTT_CLIENT_AGENT, REST_CLIENT_AGENT, REST_SERVER_AGENT

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

# Checks network path of Kepware host on the network. Only provides status of network path, not running of 
# runtime or Config API service (since no port or data collection from API is done.)
def check_ping(server: server):
    host = server.host
    try:
        print("Pinging {}".format(host))
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', host]
        return subprocess.call(command) == 0
    except:
        return False

# Checks Socket of Config API service. Only provides status of port open, not running of 
# runtime or Config API service (since any app can open the port)
def check_socket(server: server):
    host = server.host
    port = server.port
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

# Check server status via API call, any non 200 response will throw an 
# KepHTTPerror or KepURLerror exception and is a sign that the config API service
# or runtime service is not running
# 
# Supported in Kepware v6.13 or later. Use check_socket() for older versions.
def check_state(server: server):
    try:
        r = server.get_info()
        return True
    except:
        return False

def objects(server: server, sState):
    #Check for Channels
    enableProperty = "servermain.DEVICE_DATA_COLLECTION"
    try:
        channelProperties = channel.get_all_channels(server)
    except:
            channelProperties = []

    for eachChannel in channelProperties:
        thisChannel = eachChannel['common.ALLTYPES_NAME']

        #Check for Devices within Channel
        try:
            deviceProperties = device.get_all_devices(server, thisChannel)
        except:
            deviceProperties = []

        for eachDevice in deviceProperties:
            thisDevice = eachDevice['common.ALLTYPES_NAME']
            try:
                result = device.modify_device(server, f'{thisChannel}.{thisDevice}', DATA={enableProperty: sState}, force=True)
            except Exception as e:
                print("[Exception] Failed to set property - {}".format(e))

    #Check for DataLogger groups
    enableProperty = "datalogger.LOG_GROUP_ENABLED"
    try:
        logGroupProperties = log_group.get_all_log_groups(server)
    except:
        logGroupProperties = []

    for eachLogGroup in logGroupProperties:
        eachLogGroup[enableProperty] = sState
        try:
            result = log_group.modify_log_group(server, DATA= eachLogGroup, force= True)
        except Exception as e:
            print("[Exception] Failed to set property - {}".format(e))
    
    #Check for MQTT clients
    enableProperty = "iot_gateway.AGENTTYPES_ENABLED"
    try:
        agentProperties = agent.get_all_iot_agents(server, MQTT_CLIENT_AGENT)
        agentProperties.extend(agent.get_all_iot_agents(server, REST_CLIENT_AGENT))
        agentProperties.extend(agent.get_all_iot_agents(server, REST_SERVER_AGENT))
    except:
        agentProperties = []
    
    for eachAgent in agentProperties:
        eachAgent[enableProperty] = sState
        try:
            result = agent.modify_iot_agent(server,eachAgent, force= True)
        except Exception as e:
            print("[Exception] Failed to set property - {}".format(e))
    
    #Check for Schedules
    url = f"{server.url}/project/_scheduler/schedules"
    enableProperty = "scheduler.SCHEDULE_ENABLED"
    try:
        result = server._config_get(url)
        schedProperties = result.payload
    except:
        schedProperties = []
    
    for eachSched in schedProperties:
        eachSched[enableProperty] = sState
        eachSched['FORCE_UPDATE'] = True
        try:
            result = server._config_update(f'{url}/{eachSched["common.ALLTYPES_NAME"]}', DATA= eachSched)
        except Exception as e:
            print("[Exception] Failed to set property - {}".format(e))
    
    #Check for EFM exporters
    url = f"{server.url}/project/_efmexporter/poll_groups"
    enableProperty = "efm_exporter.POLLGROUP_ENABLED"

    try:
        result = server._config_get(url)
        pollGroupProperties = result.payload
    except:
        pollGroupProperties = []
    
    for eachPollGroup in pollGroupProperties:
        eachPollGroup[enableProperty] = sState
        eachPollGroup['FORCE_UPDATE'] = True
        try:
            result = server._config_update(f'{url}/{eachPollGroup["common.ALLTYPES_NAME"]}', DATA= eachPollGroup)
        except Exception as e:
            print("[Exception] Failed to set property - {}".format(e))

    return True

if __name__ == "__main__":
    # load setup parameters
    setupData = get_setup_parameters('./Config API/Enable Secondary Server/setup.json')

    # assign global variables
    primaryHost = setupData['primaryHost']
    primaryPort = setupData['primaryPort']
    secondaryHost = setupData['secondaryHost']
    secondaryPort = setupData['secondaryPort']
    apiUsername = setupData['apiUsername']
    apiPassword = setupData['apiPassword']
    useHttps = setupData['HTTPS']
    monitorInterval = setupData['monitorInterval']

    # Create Server connection references to use
    primaryServer =  server(primaryHost, primaryPort, apiUsername, apiPassword, https= useHttps)
    secondaryServer = server(secondaryHost, secondaryPort, apiUsername, apiPassword, https= useHttps)

    # Handle self-signed certs if needed
    if setupData['trustAllCerts']:
        primaryServer.SSL_trust_all_certs = True
        secondaryServer.SSL_trust_all_certs = True

    # be sure to use explicit operators (== or !=) to compare values since this is somewhat of a tri-state bool
    # none = unknown, true = objects are enabled, false = objects are disabled
    primaryState = None
    secondaryState = None
    primaryAvailable = None
    secondaryAvailable = None

    while True:
        # check health by connecting to the Configuration API's port and querying project properties
        # can be substituted with check_socket() if desired.
        # check_state() is supported in Kepware v6.13 or later. Use check_socket() for older versions.
        if check_state(primaryServer):
            if not primaryAvailable:
                print(f"{datetime.datetime.now()} - Primary is available")
            primaryAvailable = True
        else: 
            if primaryAvailable:
                print(f"{datetime.datetime.now()} - [Warning] Primary is unavailable")
            primaryAvailable = False

        if check_state(secondaryServer):
            if not secondaryAvailable:
                print(f"{datetime.datetime.now()} - Secondary is available")
            secondaryAvailable = True
        else: 
            if secondaryAvailable:
                print(f"{datetime.datetime.now()} - [Warning] Secondary not available - Please ensure Configuration API is enabled")
            secondaryAvailable = False

        # or use a ping
        #primaryAvailable = check_ping(primaryHost)
        #secondaryAvailable = check_ping(secondaryHost)

        # if connection is lost, assume state is unknown
        if not primaryAvailable: primaryState = None
        if not secondaryAvailable: secondaryState = None

        if primaryAvailable:
            # enable primary if needed
            if primaryState != True:
                result = objects(primaryServer,True)
                if result: 
                    primaryState = True
                    print("{} - Primary has been enabled".format(datetime.datetime.now()))
            # only attempt to disable the secondary when it's available to avoid errors
            if secondaryAvailable and secondaryState != False:
                result = objects(secondaryServer,False)
                if result: 
                    secondaryState = False 
                    print("{} - Secondary has been disabled".format(datetime.datetime.now()))
        else:
            # enable secondary if needed. not necessary to disable primary since it's unavailabe 
            if secondaryAvailable and secondaryState != True:
                result = objects(secondaryServer,True)
                if result: 
                    secondaryState = True
                    print("{} - Secondary has been enabled".format(datetime.datetime.now()))
            pass

        time.sleep(monitorInterval)