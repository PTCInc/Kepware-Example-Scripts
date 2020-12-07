# ******************************************************************************
#   This is script is for example and instructional purposes only.
#
#   Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
#   See License.txt in the project root for license information.
#
#   Name:
#       Configure wide format column mappings
#   
#   Purpose: 
#    - For a given Log Group, automatically configure tag-to-column mappings using a source CSV file
#
#   To use:
#    - Add desired tags to Log Group using GUI or API
#    - Update 'csvs/logGroup.csv' with target Log Group
#    - Update 'csvs/columnMappings.csv' with desired tag mapping scheme, data types and lengths
#    - Update 'auth' with Kepware Config API username and password
#
#   Notes:
#    - To quickly and easily source full tag paths (chan.dev.<folders>.name) of log items with column mappings desired for custom configuration, run the helper script "exportLogItemsToCsv.ps1" and copy the "datalogger.LOG_ITEM_ID" column from the exported CSV into the "Log_Item_ID" column of the columnMappings.csv file.
#    - SQL Data Type Enumerations and (Lengths) 
#    --- Integer = 7 (4)
#    --- Real = 4 (4)
#    --- Char = 1 (64)
#    --- Timestamp = 11 (16)
#    --- Smallint = 5 (2) 
#
#   Requirements: 
#    - Database table must be pre-created and Log Group must be configured to Log to Existing Table
#    - Wide Format must be used
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

Function Get-LogGroup{ 
    $csv1 = $PSScriptRoot + '\csvs\logGroup.csv'
    $obj = Import-Csv $csv1
    Return ($obj)
}

Function Get-ColumnMappings {
    $csv1 = $PSScriptRoot + '\csvs\columnMappings.csv'
    $obj = Import-Csv $csv1
    Return ($obj)
}

Function Get-KepColumnMappingDefaults ($param1) {
    $uri = "http://127.0.0.1:57412/config/v1/project/_datalogger/log_groups/$($param1.Log_Group)/column_mappings/"
    $obj = Invoke-RestMethod -Uri $uri -Method 'Get' -Headers (Get-Header)
    Return ($obj)
}

Function Get-ProjectID {
    $uri = 'http://127.0.0.1:57412/config/v1/project/'
    $obj = Invoke-RestMethod -Uri $uri -Method 'Get' -Headers (Get-Header)
    $objProjID = $obj.'PROJECT_ID'
    Write-Output ($objProjID)
}

$logGroup = Get-LogGroup
$columnMappings = Get-ColumnMappings
$returnedColumnMappings = Get-KepColumnMappingDefaults ($logGroup)

foreach ($x in $columnMappings) {
    foreach ($n in $returnedColumnMappings) {
        if ($n.'datalogger.TABLE_ALIAS_LOG_ITEM_ID' -eq $x.'LOG_ITEM_ID') {
                $n.'datalogger.TABLE_ALIAS_DATABASE_FIELD_NAME_VALUE' = $x.'Value_DBColumn'
                $n.'datalogger.TABLE_ALIAS_SQL_DATA_TYPE_VALUE' = [int]$x.'Value_Datatype'
                $n.'datalogger.TABLE_ALIAS_SQL_LENGTH_VALUE' = [int]$x.'Value_Length'
                $n."datalogger.TABLE_ALIAS_DATABASE_FIELD_NAME_NUMERIC" = $x.'NumericID_DBColumn'
                $n."datalogger.TABLE_ALIAS_SQL_DATA_TYPE_NUMERIC" = [int]$x.'NumericID_Datatype'
                $n."datalogger.TABLE_ALIAS_SQL_LENGTH_NUMERIC" = [int]$x.'NumericID_Length'
                $n."datalogger.TABLE_ALIAS_DATABASE_FIELD_NAME_QUALITY" = $x.'Quality_DBColumn'
                $n."datalogger.TABLE_ALIAS_SQL_DATA_TYPE_QUALITY" = [int]$x.'Quality_Datatype'
                $n."datalogger.TABLE_ALIAS_SQL_LENGTH_QUALITY" = [int]$x.'Quality_Length'
                $n."datalogger.TABLE_ALIAS_DATABASE_FIELD_NAME_TIMESTAMP" = $x.'Timestamp_DBColumn'
                $n."datalogger.TABLE_ALIAS_SQL_DATA_TYPE_TIMESTAMP" = [int]$x.'Timestamp_Datatype'
                $n."datalogger.TABLE_ALIAS_SQL_LENGTH_TIMESTAMP" = [int]$x.'Timestamp_Length'
                $n."datalogger.TABLE_ALIAS_DATABASE_FIELD_NAME_BATCHID" = $x.'BatchID_DBColumn'
                $n."datalogger.TABLE_ALIAS_SQL_DATA_TYPE_BATCHID" = [int]$x.'BatchID_Datatype'
                $n."datalogger.TABLE_ALIAS_SQL_LENGTH_BATCHID" = [int]$x.'BatchID_Length'
                $n.PROJECT_ID = Get-ProjectID
                $column = $n.'common.ALLTYPES_NAME'
                $uriColumnNumber = "http://127.0.0.1:57412/config/v1/project/_datalogger/log_groups/$($logGroup.Log_Group)/column_mappings/$($column)"
                $body = ConvertTo-Json $n
                Invoke-RestMethod -Uri $uriColumnNumber -Method 'PUT' -Headers $headers -Body $body
        }
    }
}