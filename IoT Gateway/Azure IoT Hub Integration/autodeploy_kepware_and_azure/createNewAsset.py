# ******************************************************************************  
# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
#  Name:
#        Create_new_asset
#   Parameters:
#        Setup parameters defined in setup.json:
#           Sas key length in seconds
#           Path for kepware mqtt json snippet
#           Config api username
#           Config api password
#           Iot hub name
#           Iot device name
#        Iot gateway agent parameters defined in mqtt json snippet
#           One or an array of JSON objects of iot gateway mqtt agent in kepware server v6.7 with default settings
#
#   Returns:
#         True - if both creating both agent and device are successful
#         False - if creating with agent or device fails
#
#   Procedure:
#       Check if Azure user is logged in
#       Load setup parameters from file (or uncomment code for user input)
#           Handle file I/O errors
#           Check for required keys
#           Check to make sure certain required keys aren't empty
#       Load MQTT agent JSON object from file
#           Handle I/O errors
#           Check for required keys
#           !! To add: check to make sure certain required keys aren't empty
#       For each agent in JSON array
#           Create iot hub device
#           Generate SAS key
#           Modify JSON with required fields based on name and SAS key
#           Delete iot devices if device creation or sas key generation error
#       Post modified JSON object to kepware and handle errors
#           Delete devices from iot hub if HTTP post generates server response error
#
# *****************************************************************************/

def create_new_asset():
    import json
    import requests
    import subprocess

    # make variables
    checkLoginCmd = "az ad signed-in-user show"
    azureIotHubName = "myCloudHub1"
    azureMqttClientUrl = "ssl://{}.azure-devices.net:8883".format(azureIotHubName)
    createdDeviceCount = 0

    # check if user is logged in, alert and end if not
    try:
        print ("\nChecking Azure account login status")
        returned_value = subprocess.check_output(checkLoginCmd, shell=True)
        print ("-- Login status OK")
    except subprocess.CalledProcessError as e:
        print ("-- No user logged in - Please run 'az login' using Azure CLI\n")
        print(e.output.decode("utf-8"))
        return False

    # grab config api U/P, device name, iot hub name, JSON file path from file
    setupFile = 'setup.json'
    try:
        print ("Loading 'setup.json' from local directory")
        with open (setupFile) as j:
            setupData = json.load (j)
        try:
            try:
                azureIotHubName = setupData['hubName']
                deviceName = setupData['name']
                configUsername = setupData.get('configApiUsername')
                configPassword = setupData['configApiPassword']
                sasKeyLength = setupData['sasLen']
                readFile = setupData['agentFile']
                if azureIotHubName == '' or deviceName == '' or configUsername == '' or sasKeyLength == '' or readFile == '':
                    print ("-- Load setup failed - missing parameters from setup file")
                    return False
            except Exception as e:
                print ("-- Load setup failed - '{}'".format (e))
                return False
        except KeyError as e:
            print ("-- Load setup failed - '{}'".format (e))
            return False
    except Exception as e:
        print ("-- Load setup failed - '{}'".format (e))
        return False

    # ******* User input for setup parameters ***********************************************************************
    """ 
    # grab username from user
    i = 0
    while i == 0:
        configUsername = str(input ("Enter username for config API: ") or "administrator")
        if re.search (r'[\s]', configUsername):
            print ("No spaces please")
        else:
            print ("-- Accepted")
            i += 1

    #grab password from user
    i = 0
    while i == 0:
        configPassword = str(input("Enter password for config API (press enter for no password): ") or "")
        if re.search (r'[\s]', configPassword):
            print ("No spaces please")
        else:
            print ("-- Accepted")
            i += 1
     
    # ask user for iot hub name and base name for iot hub devices and mqtt agents
    i = 0
    while i == 0:
        azureIotHubName = str(input("Enter Azure IoT Hub name: ") or "myCloudHub1")
        if re.search (r'[\s]', azureIotHubName):
            print("No spaces please")
        else:
           print("-- Accepted")
           i += 1
    i = 0
    while i == 0:
        deviceName = str(input("Enter a base name (myDevice becomes myDevice1) for Azure IoT Hub devices and IoT Gateway MQTT agents:") or "myDevice")
        if re.search (r'[\s]', deviceName):
            print ("-- No spaces please")
        else:
            print ("-- Accepted")
            i += 1

    # grab file name
    readFile = str (input ("Enter full file path of JSON MQTT agents snippet including file name: ") or "kepware_object_snippets/arrayOfMqttAgents.json")
    print ("-- Accepted")
    """
    # ******************************************************************************

    # read in kepware iot gateway mqtt json template
    try:
        print ("Loading JSON snippet at '{}'".format (readFile))
        with open (readFile) as j:
            jsonData = json.load(j)

    except IOError as e:
        print ("File load failed - '{}'".format(e))
        return False;

    # check if keys are present in file
    agentNameKey = 'common.ALLTYPES_NAME'
    agentTypeKey = 'iot_gateway.AGENTTYPES_TYPE'
    agentEnabledKey = 'iot_gateway.AGENTTYPES_ENABLED'
    agentUrlKey = 'iot_gateway.MQTT_CLIENT_URL'
    agentTopicKey = 'iot_gateway.MQTT_CLIENT_TOPIC'
    agentQosKey = 'iot_gateway.MQTT_CLIENT_QOS'
    agentPubRateKey = 'iot_gateway.AGENTTYPES_RATE_MS'
    agentPubFormat = 'iot_gateway.AGENTTYPES_PUBLISH_FORMAT'
    agentMaxEvents = 'iot_gateway.AGENTTYPES_MAX_EVENTS'
    agentTimeoutKey = 'iot_gateway.AGENTTYPES_TIMEOUT_S'
    agentFormatKey = 'iot_gateway.AGENTTYPES_MESSAGE_FORMAT'
    agentStanTempKey = 'iot_gateway.AGENTTYPES_STANDARD_TEMPLATE'
    agentExpansionKey = 'iot_gateway.AGENTTYPES_EXPANSION_OF_VALUES'
    agentAdvTempKey = 'iot_gateway.AGENTTYPES_ADVANCED_TEMPLATE'
    agentClientIdKey = 'iot_gateway.MQTT_CLIENT_CLIENT_ID'
    agentUserNameKey = 'iot_gateway.MQTT_CLIENT_USERNAME'
    agentPasswordKey = 'iot_gateway.MQTT_CLIENT_PASSWORD'
    agentTlsKey = 'iot_gateway.MQTT_TLS_VERSION'
    agentCertificateKey = 'iot_gateway.MQTT_CLIENT_CERTIFICATE'
    agentWillKey = 'iot_gateway.MQTT_CLIENT_ENABLE_LAST_WILL'
    agentWillMessKey = 'iot_gateway.MQTT_CLIENT_LAST_WILL_MESSAGE'
    agentWriteEnableKey = 'iot_gateway.MQTT_CLIENT_ENABLE_WRITE_TOPIC'
    agentWriteTopicKey = 'iot_gateway.MQTT_CLIENT_WRITE_TOPIC'
    try:
        for r in jsonData:
            x = r[agentNameKey]
            x = r[agentTypeKey]
            x = r[agentEnabledKey]
            x = r[agentEnabledKey]
            x = r[agentUrlKey]
            x = r[agentTopicKey]
            x = r[agentQosKey]
            x = r[agentPubRateKey]
            x = r[agentPubFormat]
            x = r[agentMaxEvents]
            x = r[agentTimeoutKey]
            x = r[agentFormatKey]
            x = r[agentStanTempKey]
            x = r[agentExpansionKey]
            x = r[agentAdvTempKey]
            x = r[agentClientIdKey]
            x = r[agentUserNameKey]
            x = r[agentPasswordKey]
            x = r[agentTlsKey]
            x = r[agentCertificateKey]
            x = r[agentCertificateKey]
            x = r[agentWillKey]
            x = r[agentWillMessKey]
            x = r[agentWriteEnableKey]
            x = r[agentWriteTopicKey]
    except KeyError:
        print("-- Load failed, missing keys")
        return False
    print("-- Load succeeded")

    # create all iot devices using information from setup file
    try:
        i = 0
        if isinstance (jsonData, dict):
            nameNum = i + 1
            azureDeviceName = deviceName + "{}".format (nameNum)
            print ("Creating Azure IoT device with name '{}' on hub '{}'".format (azureDeviceName, azureIotHubName))
            createDeviceCmd = "az iot hub device-identity create -n {} -d {}".format (azureIotHubName, azureDeviceName)
            returned_value = subprocess.check_output (createDeviceCmd, shell=True)
            print ("-- '{}' successfully created".format (azureDeviceName))
            createdDeviceCount += 1
        else:
            while i < len (jsonData):
                nameNum = i + 1
                azureDeviceName = deviceName + "{}".format (nameNum)
                print("Creating Azure IoT device with name '{}' on hub '{}'".format(azureDeviceName, azureIotHubName))
                createDeviceCmd = "az iot hub device-identity create -n {} -d {}".format(azureIotHubName, azureDeviceName)
                returned_value = subprocess.check_output(createDeviceCmd, shell=True)
                print ("-- '{}' successfully created".format (azureDeviceName))
                azureDeviceName = deviceName
                i += 1
                createdDeviceCount += 1
    except subprocess.CalledProcessError as e:
        print(e.output.decode("utf-8"))
        if createdDeviceCount == 0:
            return False
        else:
            try:
                i = 0
                while i < createdDeviceCount:
                        nameNum = i + 1
                        azureDeviceName = deviceName + "{}".format (nameNum)
                        print ("Deleting {} from {}".format (azureDeviceName, azureIotHubName))
                        deleteDeviceCmd = "az iot hub device-identity delete --hub-name {} --device-id {}".format (azureIotHubName, azureDeviceName)
                        returned_value = subprocess.check_output (deleteDeviceCmd, shell=True)
                        print ("-- {} successfully deleted".format (azureDeviceName))
                        i += 1
                return False
            except subprocess.CalledProcessError as e:
                print("Error deleting device: " + (e.output.decode ("utf-8")))
                return False

    # generate SAS token for devices and update JSON data object with SAS token, device name and IoT Hub name
    i = 0
    if createdDeviceCount == 1:
        nameNum = i + 1
        azureDeviceName = deviceName + "{}".format (nameNum)
        print ("Generating SAS token for {}".format (azureDeviceName))
        createDeviceSasCmd = "az iot hub generate-sas-token --hub-name {} --device-id {} --du {}".format (
            azureIotHubName, azureDeviceName, sasKeyLength)
        sasToken = subprocess.check_output (createDeviceSasCmd, shell=True)
        utfToken = sasToken.decode ("utf-8")
        Token = utfToken.split ('}', 1)[0].rstrip () + '\n' + "}"
        jsonToken = json.loads (Token)
        print ("-- SAS Token:\n\n{}\n".format (jsonToken))
        azureTopicName = "devices/{}/messages/events/".format (azureDeviceName)
        try:
            jsonData[i]['iot_gateway.MQTT_CLIENT_URL'] = azureMqttClientUrl
            jsonData[i]['common.ALLTYPES_NAME'] = azureDeviceName
            jsonData[i]['iot_gateway.MQTT_CLIENT_CLIENT_ID'] = azureDeviceName
            jsonData[i]['iot_gateway.MQTT_CLIENT_TOPIC'] = azureTopicName
            jsonData[i]['iot_gateway.MQTT_CLIENT_USERNAME'] = "{}.azure-devices.net/{}".format (azureIotHubName,
                                                                                                azureDeviceName)
            jsonData[i]['iot_gateway.MQTT_CLIENT_PASSWORD'] = jsonToken['sas']
        except KeyError:
            print ('-- Error editing JSON object - check keys\n')
    else:
        while i < createdDeviceCount:
            generatedSas = 0
            try:
                nameNum = i + 1
                azureDeviceName = deviceName + "{}".format (nameNum)
                print ("Generating SAS token for {}".format (azureDeviceName))
                createDeviceSasCmd = "az iot hub generate-sas-token --hub-name {} --device-id {} --du {}".format(azureIotHubName, azureDeviceName, sasKeyLength)
                sasToken = subprocess.check_output(createDeviceSasCmd, shell=True)
                utfToken = sasToken.decode("utf-8")
                Token = utfToken.split ('}', 1)[0].rstrip() + '\n' + "}"
                jsonToken = json.loads(Token)
                print ("-- SAS Token:\n\n{}\n".format (jsonToken))
                generatedSas += 1
                azureTopicName = "devices/{}/messages/events/".format (azureDeviceName)
                try:
                    jsonData[i]['iot_gateway.MQTT_CLIENT_URL'] = azureMqttClientUrl
                    jsonData[i]['common.ALLTYPES_NAME'] = azureDeviceName
                    jsonData[i]['iot_gateway.MQTT_CLIENT_CLIENT_ID'] = azureDeviceName
                    jsonData[i]['iot_gateway.MQTT_CLIENT_TOPIC'] = azureTopicName
                    jsonData[i]['iot_gateway.MQTT_CLIENT_USERNAME'] = "{}.azure-devices.net/{}".format (azureIotHubName, azureDeviceName)
                    jsonData[i]['iot_gateway.MQTT_CLIENT_PASSWORD'] = jsonToken['sas']
                except KeyError:
                    print ('-- Error editing JSON object - check keys\n')
                    try:
                        while i <= generatedSas and i < createdDeviceCount:
                            nameNum = i + 1
                            azureDeviceName = deviceName + "{}".format (nameNum)
                            print ("Deleting {} from {}".format (azureDeviceName, azureIotHubName))
                            deleteDeviceCmd = "az iot hub device-identity delete --hub-name {} --device-id {}".format (
                                azureIotHubName, azureDeviceName)
                            returned_value = subprocess.check_output (deleteDeviceCmd, shell=True)
                            print ("-- {} successfully deleted".format (azureDeviceName))
                            azureDeviceName = deviceName
                            i += 1
                        return False
                    except subprocess.CalledProcessError as e:
                        print (e.output.decode ("utf-8"))
                        return False
                i += 1
                azureDeviceName = deviceName
            except subprocess.CalledProcessError as e:
                print (e.output.decode ("utf-8"))
                try:
                    while i <= generatedSas and i < createdDeviceCount:
                        nameNum = i + 1
                        azureDeviceName = deviceName + "{}".format (nameNum)
                        print ("Deleting {} from {}".format (azureDeviceName, azureIotHubName))
                        deleteDeviceCmd = "az iot hub device-identity delete --hub-name {} --device-id {}".format (azureIotHubName, azureDeviceName)
                        returned_value = subprocess.check_output (deleteDeviceCmd, shell=True)
                        print ("-- {} successfully deleted".format (azureDeviceName))
                        azureDeviceName = deviceName
                        i += 1
                    return False
                except subprocess.CalledProcessError as e:
                    print (e.output.decode ("utf-8"))
                    return False

    # post mqtt agent to kepware
    try:
        iotGatewayEndpoint = 'http://{}:{}@127.0.0.1:57412/config/v1/project/_iot_gateway/mqtt_clients'''.format (configUsername, configPassword)
        print ("Creating MQTT Client Agents at URL '{}'".format(iotGatewayEndpoint))
        print ("-- Posting JSON".format (azureDeviceName))
        r = requests.post (url=iotGatewayEndpoint, json=jsonData)
        r.raise_for_status ()
        print ("-- Agents created")
        print ("\nExiting\n".format(azureDeviceName))
        return True
    except requests.exceptions.HTTPError as err:
        response = r.content
        print("-- Received error response from REST Config API: '{}".format(err, response))
        print("Response content: {}".format(response))
        try:
            i = 0
            while i < createdDeviceCount:
                nameNum = i + 1
                azureDeviceName = deviceName + "{}".format (nameNum)
                print ("Deleting {} from {}".format (azureDeviceName, azureIotHubName))
                deleteDeviceCmd = "az iot hub device-identity delete --hub-name {} --device-id {}".format (
                    azureIotHubName, azureDeviceName)
                returned_value = subprocess.check_output (deleteDeviceCmd, shell=True)
                print ("-- {} successfully deleted".format (azureDeviceName))
                azureDeviceName = deviceName
                i += 1
            return False
        except subprocess.CalledProcessError as e:
            print ("Error deleting device: " + (e.output.decode ("utf-8")))
            return False


        """
        if isinstance(jsonData, dict):
            print("---- {}".format(response))
            try:
                i = 0
                if isinstance (jsonData, dict):
                    nameNum = i + 1
                    azureDeviceName = deviceName + "{}".format (nameNum)
                    deleteDeviceCmd = "az iot hub device-identity delete --hub-name {} --device-id {}".format (
                        azureIotHubName, azureDeviceName)
                    print ("Deleting '{}' from IoT Hub".format (azureDeviceName))
                    returned_value = subprocess.check_output (deleteDeviceCmd, shell=True)
                    print ("-- '{}' successfully deleted from IoT Hub".format (azureDeviceName))
                    azureDeviceName = deviceName
                else:
                    while i < len (jsonData):
                        nameNum = i + 1
                        azureDeviceName = deviceName + "{}".format (nameNum)
                        deleteDeviceCmd = "az iot hub device-identity delete --hub-name {} --device-id {}".format (
                            azureIotHubName, azureDeviceName)
                        print ("Deleting '{}' from IoT Hub".format (azureDeviceName))
                        returned_value = subprocess.check_output (deleteDeviceCmd, shell=True)
                        print ("-- '{}' successfully deleted from IoT Hub".format (azureDeviceName))
                        azureDeviceName = deviceName
                        i += 1
                return False
            except subprocess.CalledProcessError as e:
                print (e.output.decode ("utf-8"))
                return False
        else:
            for m in response:
                resp = m['message']
                print ("---- {}".format (resp))
                try:
                    i = 0
                    while i < len(jsonData):
                        nameNum = i + 1
                        azureDeviceName = deviceName + "{}".format (nameNum)
                        deleteDeviceCmd = "az iot hub device-identity delete --hub-name {} --device-id {}".format (azureIotHubName, azureDeviceName)
                        print("Deleting '{}' from IoT Hub".format(azureDeviceName))
                        returned_value = subprocess.check_output (deleteDeviceCmd, shell=True)
                        print("-- '{}' successfully deleted from IoT Hub".format(azureDeviceName))
                        azureDeviceName = deviceName
                        i += 1
                    return False
                except subprocess.CalledProcessError as e:
                    print (e.output.decode ("utf-8"))
                    return False
        """

returnCode = create_new_asset()
print("Return Code: {}".format(returnCode))