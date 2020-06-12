# ******************************************************************************
#  Name:
#       GetAzureIoTDevicesandTags
#  parameters:
#             path - [[optional] location for csv files
#             name - [optional]  name of iot gateway agent you want to get tags for
#             KepwareIP - address to find kepware at
#
#   Returns:
#         True - if file or files was created successful
#         False - if error in some way
#
# 1. Confirm the all the parameters are not null or undefined, other than optional ones
# 2. Check if name parameters is a valid name of a Iot gateway agent connected to IoT Hub
#     2a. If No - get list of IoT gateway agents connected to IoT Hub
#     2b. If Yes - place single agent name in to list and move on to next step
# 3. Get all items associated with each IoT Gateway Agent in the list
# 4. Write out each agent in the list items as it own CSV file, include date timestamp in file name
# ******************************************************************************/

def GetAzureIoTDeviceandTags():
    import csv
    import datetime
    import json
    import requests
    import subprocess

    setupFilePath = 'setup.json'
    def get_parameters(setupFile):
        try:
            print ("Loading 'setup.json' from local directory")
            with open (setupFile) as j:
                setupData = json.load (j)
                print ("-- Load succeeded")
            try:
                try:
                    optionalPath = setupData['path']
                    name = setupData['agentName']
                    kepwareIp = setupData['kepwareIp']
                    hubName = setupData['hubName']
                    configUsername = setupData['configUsername']
                    if kepwareIp == '' or hubName == '' or configUsername == '':
                        print ("-- Load setup failed - missing parameters from setup file")
                        return False
                except Exception as e:
                    print ("-- Load setup failed - '{}'".format (e))
                    return False
            except KeyError as e:
                print ("-- Load setup failed '{}'".format (e))
                return False
            return setupData
        except Exception as e:
            print ("-- Load setup failed - '{}'".format (e))
            return False

    def check_name_with_azure(agentName, hubName):
        checkDeviceNameCmd = "az iot hub device-identity show --device-id {} --hub-name {}".format(agentName, hubName)
        try:
            print ("Checking device presence for '{}' within Azure IoT Hub".format(agentName))
            returned_value = subprocess.check_output (checkDeviceNameCmd, shell=True)
            print ("-- Device presence OK")
            return True
        except subprocess.CalledProcessError as e:
            print ("-- Device '{}' does not exist".format(agentName))
            print (e.output.decode ("utf-8"))
            return False

    def get_agent_tags(agentName, kepwareIp, configUsername, configPassword):
        try:
            mqttEndpoint = 'http://{}:{}@{}:57412/config/v1/project/_iot_gateway/mqtt_clients/{}/iot_items'.format (
                configUsername, configPassword, kepwareIp, agentName)
            print ("GET-ing MQTT Client agent at URL '{}'".format (mqttEndpoint))
            r = requests.get (url=mqttEndpoint)
            r.raise_for_status ()
            response = r.json()
            if len(response) == 0:
                print ("-- No IoT items found")
                return False
            print ("-- Agent found, sourcing tags")
            return response
        except requests.exceptions.HTTPError as err:
            response = r.content
            print ("-- Received error response from REST Config API: '{}".format (err, response))
            print ("Response content: {}".format (response))
            return False

    def export_single(agentName, items, optionalPath):
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            with open ('{}{}_items_{}.csv'.format(optionalPath, agentName, now), 'w', newline='') as csvfile:
                filewriter = csv.writer (csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow (['Item List for {}'.format(agentName)])
                for m in items:
                    rName = m['common.ALLTYPES_NAME']
                    filewriter.writerow ([rName])
                return True
        except Exception as e:
            print('-- Error encountered while creating CSV file')
            print(e)
            return False

    def get_all_agents(kepwareIp, configUsername, configPassword):
        try:
            mqttEndpoint = 'http://{}:{}@{}:57412/config/v1/project/_iot_gateway/mqtt_clients'.format (
                configUsername, configPassword, kepwareIp)
            print ("GET-ing all MQTT client agents at URL '{}'".format (mqttEndpoint))
            r = requests.get (url=mqttEndpoint)
            r.raise_for_status ()
            response = r.json ()
            if len(response) == 0:
                print ("-- No agents found")
                return False
            print ("-- Agents found, sourcing agent list")
            return response
        except requests.exceptions.HTTPError as err:
            response = r.content
            print ("-- Received error response from REST Config API: '{}".format (err, response))
            print ("Response content: {}".format (response))
            return False

    # load setup parameters
    setupList = get_parameters(setupFilePath)

    # assign variables from retrieved setup parameters
    agentName = setupList['agentName']
    hubName = setupList['hubName']
    configUsername = setupList['configUsername']
    configPassword = setupList['configPassword']
    kepwareIp = setupList['kepwareIp']

    # handle empty path key
    optionalPath = setupList['path']
    if optionalPath == '':
        optionalPath = "csv_exports/"
    else:
        pass

    # if no device name is present get all agents from kepware and export tags to CSV
    # else check single device name with azure and export tags to CSV
    if agentName == '':
        allAgents = get_all_agents(kepwareIp, configUsername, configPassword)
        if allAgents == False:
            return False
        for a in allAgents:
            agentName = a['common.ALLTYPES_NAME']
            items = get_agent_tags (agentName, kepwareIp, configUsername, configPassword)
            if items == False:
                return False
            export_single (agentName, items, optionalPath)
        return True
    else:
        nameStatus = check_name_with_azure(agentName, hubName)
        if nameStatus == True:
            items = get_agent_tags (agentName, kepwareIp, configUsername, configPassword)
            if items == False:
                return False
            export_single (agentName, items, optionalPath)
            return True
        else:
            print("-- Device not present in Azure")
            return False
results = GetAzureIoTDeviceandTags()
print(results)