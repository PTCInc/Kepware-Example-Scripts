# ******************************************************************************
# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for license information.Name:
#
#    - Export log items to CSV
#   
#   Purpose: 
#    - For a given Log Group, export all added log items to a CSV file
#
#   To use:
#    - Update 'csvs/logGroup.csv' with target Log Group name
#    - Update 'auth' with Kepware Config API username and password
#
#   Requirements: 
#    - Database table must be pre-created and Log Group must be configured to Log to Existing Table
#    - Kepware Configuration API must be enabled for HTTP 
#    - As necessary, edit the script's configuration to target correct Kepware Server IP address and Config API service port 
# ******************************************************************************/

Function Get-Auth {
    $csv1 = $PSScriptRoot + "/csvs/auth.csv"
    $auth = Import-Csv $csv1
    Return ($auth)
}

Function Get-Header ($param) {
    $username = $param.'Username'
    $password = $param.'Password'
    $credPair = "$($username):$($password)"
    $encodedCredentials = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes("$credPair"))
    $headers = @{ Authorization = "Basic $encodedCredentials" }
    Return ($headers)
}

Function Get-LogGroup {
    $csv1 = $PSScriptRoot + '\csvs\logGroup.csv'
    $obj = Import-Csv $csv1
    Return ($obj)
}

Function Get-LogItems ($param1) {
    $path = "http://127.0.0.1:57412/config/v1/project/_datalogger/log_groups/$($logGroup.Log_Group)/log_items/"
    $obj = Invoke-RestMethod -Uri $path -Method 'Get' -Headers $headers
    Return ($obj)
}

Function Export-LogItems ($param) {
    $path = $PSScriptRoot + "/csvs/exportedLogItems.csv"
    $param | Select-Object common.ALLTYPES_NAME, datalogger.LOG_ITEM_ID, datalogger.LOG_ITEM_NUMERIC_ID, datalogger.LOG_ITEM_DATA_TYPE, datalogger.LOG_ITEM_DEADBAND_TYPE, datalogger.LOG_ITEM_DEADBAND_VALUE, datalogger.LOG_ITEM_DEADBAND_LO_RANGE, datalogger.LOG_ITEM_DEADBAND_HI_RANGE | ConvertTo-csv > $path -NoTypeInformation
    $path = $PSScriptRoot + "/csvs/exportedLogItems.csv"
}

$auth = Get-Auth
$headers = Get-Header ($auth)
$logGroup = Get-LogGroup
$logItems = Get-LogItems ($headers)
Export-LogItems ($logItems)