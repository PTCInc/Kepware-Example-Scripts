# Create a JSON Web Token (JWT) and Update MQTT Agent

This script creates a JWT based on the parameters satisfied in the code and then updates the password field of MQTT Agent with created JWT according to parameters of Configuration API.

## Dependencies

- [Kepware Configuration API SDK for Python](https://github.com/PTCInc/Kepware-ConfigAPI-SDK-Python)
- [PyJWT library](https://pyjwt.readthedocs.io/en/stable/)


## Notes

- This script is here to support [Kepware MQTT Agent and Google Cloud IoT Core](https://www.kepware.com/getattachment/f927bc2c-8a2b-459e-90ed-c85b29fdfffd/Kepware-MQTT-Agent-and-Google-IoT-Core.pdf) connectivity guide.
- The private key file that is used to create JWT should be created prior the use of this script.
- MQTT Agent should be created prior the use of this script according to connectivity guide.
- Configuration API should be enabled and available for connections in order to use this script.

