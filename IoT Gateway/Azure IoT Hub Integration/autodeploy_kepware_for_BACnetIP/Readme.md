# Build BACnet/IP devices and Deploy and Map IoT Agents to devices with Azure IoT Hub

This script automatically creates a complete Kepware project file based on a list of BACnet data points and integrates the BACnet/IP channel and all devices to Azure IoT Hub. The created project file will contain one BACnet channel, up to 128 BACnet devices below that channel, an IoT Gateway MQTT agent, and any number of tags/MQTT agent IoT item references. The IoT Gateway MQTT agent serves as an integration point to a single IoT Device created within an Azure IoT Hub.

## Dependencies

- [Azure CLI 2.x.x](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure CLI IoT Extension](https://github.com/Azure/azure-iot-cli-extension) (use the CLI to run 'az extension add --name azure-iot')
- [Python 3.7 or above](https://www.python.org/downloads/)
- Python [Requests](https://pypi.org/project/requests/) library

## Instructions

After installing Python and the 'requests' library, navigate to the 'autodeploy_kepware_for_BACnetIP' folder and double-click the Python script "auto_deploy.py". To observe verbose script output in a command prompt, call the script via the command line via "python auto_deploy.py"

## Notes

Review [auto_deploy.py](auto_deploy.py) for procedural details

- Assignment of user parameters is conducted through [setup.json](setup.json)
- BACnet device and point parameters are defined in [/csvs/source.csv](csvs/source.csv)
- Currently only the following BACnet data point types (called "object types") are supported: Analog Inputs, Analog Outputs, Analog Values, Binary Inputs, Binary Outputs, and Binary Values
- Azure connectivity (MQTT agent configuration) is controlled by / modified via the JSON object file at [/objs/agent.json](objs/agent.json). This JSON object file also includes a configuration of desired message format.
- BACnet network number is assumed (and thus hard-coded) to be "1", which yields Device Instance addresses like "1.1210100".
- BACnet device discovery is assumed (and thus hard-coded) to be "automatic via WhoIs/IAm", which means no IP address information is required, but that the devices need to support this BACnet service. Otherwise, the script should be run first and then the IP addresses / discovery type modified afterwards either manually via the Kepware Configuration Tool or via the Configuration API
- If more than 128 BACnet devices are identified in the source CSV file, only 128 will be created. The value of '128' is the "device" limit per single channel for Kepware.
