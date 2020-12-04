# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# --------------------------------------------------------------------------
# ******************************************************************************
# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
#  Description: 
#       This script creates a JWT based on the parameters specified such as 
#       Google Cloud project ID and private key file and then updates the
#       password field of desired MQTT Agent.
#
#  Procedure:
#       Create a JWT
#       Update MQTT AGent with creted JWT
#
# ******************************************************************************/

from kepconfig import connection, error
import kepconfig.iot_gateway as IoT
from kepconfig.iot_gateway import agent, iot_items
import datetime
import jwt

# Agent name and Type to be used - constants from kepconfig.iotgateway 
# can be used to identify the type of agent
agent_name = 'IoTCore'
agent_type = IoT.MQTT_CLIENT_AGENT

# JWT specific variables, Google Cloud Project ID, private key file location and name
project_id='coastal-throne-266515'
private_key_file='rsa_private.pem'

# [START iot_mqtt_jwt]
def create_jwt(project_id, private_key_file, algorithm):
    
    token = {
            # The time that the token was issued at
            'iat': datetime.datetime.utcnow(),
            # The time the token expires.
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)
# [END iot_mqtt_jwt]

# Create JWT and Convert into String
jwt=create_jwt(project_id, private_key_file, algorithm='RS256').decode("utf-8") 

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

# This creates a server reference that is used to target all modifications of 
# the Kepware configuration
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')

# Modify the password of the Agent
agent_data = {
}
agent_data['iot_gateway.MQTT_CLIENT_PASSWORD'] = jwt
try:
    print("{} - {}".format("Modify the password in the MQTT Agent", agent.modify_iot_agent(server,agent_data, agent_name, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)
