# Deploy and Map IoT Agents to devices with Azure IoT Hub

This script automatically creates IoT devices within Azure IoT Hub and deploys corresponding MQTT agents to Kepware with appropriate connection settings.

## Dependencies

- [Azure CLI 2.x.x](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure CLI IoT Extension](https://docs.microsoft.com/en-us/azure/iot-pnp/howto-install-pnp-cli) (use the CLI to run 'az extension add --name azure-cli-iot-ext')
- [Python 3.7 or above](https://www.python.org/downloads/)
- Python [Requests](https://2.python-requests.org/en/master/) library

## Notes

- Returns True is all operations succeed
- Returns False if any operation fails
- Assignment of user parameters is conducted through [setup.json](setup.json)
- IoT device and MQTT agent quantity along with MQTT agent definition of custom, non-required properties is controlled through MQTT agent object file

Review [createNewAsset.py](createNewAsset.py) for procedural details
