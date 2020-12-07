# ******************************************************************************
#   This is script is for example and instructional purposes only.
#
#   Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
#   See License.txt in the project root for license information.
#
#   Name:
#    - Add tags to Log Group
#   
#   Purpose: 
#    - Add a set of tags within a CSV file to a target Log Group
#
#   To use:
#    - Update 'csvs/deviceItems.csv' with desired set of tag paths and tag names (see Notes section below)
#    - Update 'csvs/logGroup.csv' with target Log Group
#    - Update 'csvs/auth.csv' with Kepware Username and Password for use with the Config API
#
#   Notes:
#   - To quickly get started, export a device or folder's tag set to a CSV file using the GUI or via an API script and add a column called "Tag Path"; 
#       within the Tag Path column, place the tag's location within the server project with the following format: 'channel.device.<folders>.'
#
#   Requirements: 
#    - Log Group must be pre-created in DataLogger
#    - If not already enabled, enable Kepware Server Configuration API service (consult Kepware Server documentation for details)
#    - As necessary, edit the script's configuration to target correct Kepware Server IP address and Config API service port 
# ******************************************************************************/

Function Get-Header {
    $csv1 = $PSScriptRoot + "/csvs/auth.csv"
    $auth = Import-Csv $csv1
    $username = $auth.'Username'
    $password = $auth.'Password'
    $credPair = "$($username):$($password)"
    $encodedCredentials = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes("$credPair"))
    $headers = @{ Authorization = "Basic $encodedCredentials" }
    Write-Output ($headers)
}

Function Get-DeviceItems {
    $csv = $PSScriptRoot + '\csvs\deviceItems.csv'
    $obj = Import-Csv $csv
    Return ($obj)
}
Function Get-LogGroup{
    $csv1 = $PSScriptRoot + '\csvs\logGroup.csv'
    $obj = Import-Csv $csv1
    Return ($obj)
}

Function Get-LogItemTemplate {
    $lItem = @'
    {
        "common.ALLTYPES_NAME": "",
        "common.ALLTYPES_DESCRIPTION": "",
        "datalogger.LOG_ITEM_ID": "",
        "datalogger.LOG_ITEM_NUMERIC_ID": "0",
        "datalogger.LOG_ITEM_DATA_TYPE": "",
        "datalogger.LOG_ITEM_DEADBAND_TYPE": 0,
        "datalogger.LOG_ITEM_DEADBAND_VALUE": 0,
        "datalogger.LOG_ITEM_DEADBAND_LO_RANGE": 0,
        "datalogger.LOG_ITEM_DEADBAND_HI_RANGE": 0
    }
'@ | ConvertFrom-Json

    Return $lItem
}
Function Add-LogItems ($param1) {
    $logGroup = Get-LogGroup
    $logItemJson = ConvertTo-Json $param1
    $uriLogItems = "http://127.0.0.1:57412/config/v1/project/_datalogger/log_groups/$($logGroup.Log_Group)/log_items"
    Invoke-RestMethod -Uri $uriLogItems -Method 'Post' -Headers (Get-Header) -Body $logItemJson 
}

Function Get-LogItemArray {
    $deviceItems = Get-DeviceItems
    $logItemObj = @()
    $logItem = Get-LogItemTemplate
    foreach ($i in $deviceItems) {
            $_itemPath = $i.'Tag Path' -replace '\.', '-' 
            $logItem.'common.ALLTYPES_NAME' = $_itemPath + $i."Tag Name"
            $logItem."datalogger.LOG_ITEM_ID" = $i.'Tag Path' + $i.'Tag Name'
            $logItem."datalogger.LOG_ITEM_DATA_TYPE" = $i.'Data Type'
            $logItemObj += $logItem.psobject.copy()   
    }
    Return $logItemObj
}

$logItemArray = Get-LogItemArray
Add-LogItems ($logItemArray)

