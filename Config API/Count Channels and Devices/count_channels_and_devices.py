# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------------

# Uses a target Kepware Server's Configuration API to count the number channels, 
# devices, and channels per driver type

from collections import Counter
from kepconfig import connection, error
from kepconfig.connectivity import channel, device


def discover_devices (channel):
    # Count all devices on a given channel
    devices_in_channel = 0
    try:
        # Use KepConfigAPI to get list of all devices for specified channel
        device_list = device.get_all_devices(server,channel)
        for i in device_list:
            devices_in_channel += 1
        return devices_in_channel
    except Exception as err:
        HTTPErrorHandler(err)            


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

# Define variables
channel_count = 0
device_count = 0
idriver = []

# Use KepConfigAPI to get list of all channels in server project
try:
    channel_list = channel.get_all_channels(server)
except Exception as err:
    HTTPErrorHandler(err)

for i in channel_list:
        channel_count += 1
        channel_name = i['common.ALLTYPES_NAME']
        # Add the driver type for this channel into our list
        idriver.append(i['servermain.MULTIPLE_TYPES_DEVICE_DRIVER'])
        # Call local discover_devices() to return counted devices per channel name and add to device counter
        try:
            device_count = device_count + discover_devices(channel_name)
        except Exception as err:
            HTTPErrorHandler(err)

# Use Python Counter type to identify channel counts by driver
driver_counts = Counter(idriver)

# Format into Python dictionary type (json)
driver_counts = dict(driver_counts)

print("{} {} {} {} {} {}".format("Channel Count:", channel_count, ", Device Count:", device_count, ", Channel Count by Driver:", driver_counts))
