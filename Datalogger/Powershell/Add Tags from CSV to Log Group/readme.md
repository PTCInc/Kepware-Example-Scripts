## This is script is for example and instructional purposes only.

# Add tags from CSV to Log Group

## Purpose: 
- Add a set of tags within a CSV file to a target Log Group

## To use:
- Update 'csvs/deviceItems.csv' with desired set of tag paths and tag names (see Notes section below)
- Update 'csvs/logGroup.csv' with target Log Group
- Update 'csvs/auth.csv' with Kepware Username and Password for use with the Config API

## Notes:
- To quickly get started, export a device or folder's tag set to a CSV file using the GUI or via an API script and add a column called "Tag Path"; 
       within the Tag Path column, place the tag's location within the server project with the following format: 'channel.device.<folders>.'

## Requirements: 
- Log Group must be pre-created in DataLogger
- If not already enabled, enable Kepware Server Configuration API service (consult Kepware Server documentation for details)
- As necessary, edit the script's configuration to target correct Kepware Server IP address and Config API service port 
