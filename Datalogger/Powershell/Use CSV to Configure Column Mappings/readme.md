## This is script is for example and instructional purposes only.

# Use a CSV file to configure wide format column mappings
   
## Purpose: 
- For a given Log Group, automatically configure tag-to-column mappings using a source CSV file

## To use:
- Add desired tags to Log Group using GUI or API
- Update 'csvs/logGroup.csv' with target Log Group
- Update 'csvs/columnMappings.csv' with desired tag mapping scheme, data types and lengths
- Update 'auth' with Kepware Config API username and password

## Notes:
- To quickly and easily source full tag paths (chan.dev.<folders>.name) of log items with column mappings desired for custom configuration, run the helper script "exportLogItemsToCsv.ps1" and copy the "datalogger.LOG_ITEM_ID" column from the exported CSV into the "Log_Item_ID" column of the columnMappings.csv file.
- SQL Data Type Enumerations and (Lengths) 
--- Integer = 7 (4)
--- Real = 4 (4)
--- Char = 1 (64)
--- Timestamp = 11 (16)
--- Smallint = 5 (2) 

## Requirements: 
- Database table must be pre-created and Log Group must be configured to Log to Existing Table
- Wide Format must be used
- If not already enabled, enable Kepware Server Configuration API service (consult Kepware Server documentation for details)
- As necessary, edit the script's configuration to target correct Kepware Server IP address and Config API service port 
