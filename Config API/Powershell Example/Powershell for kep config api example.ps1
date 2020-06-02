# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Global vars to use with testing.

$Global:username = 'Administrator'
$Global:password = ''
$Global:uri = 'http://127.0.0.1:57412/config/v1/'
$Global:headder =  @{ Authorization = "Basic {0}" -f [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $Global:username,$Global:password)))}



# Simple config get api funtions

function Verb-Noun {
    [CmdletBinding()]
    param (
        
    )
    
    begin {
        
    }
    
    process {
        
    }
    
    end {
        
    }
}


function Get-Admin {
    # This function will pull in the server admin info
    $uri = $Global:uri+'admin'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-ServerUserGroup{
    # This function will pull in the server user groups 
    $uri = $Global:uri+'admin/server_usergroups'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-EventLog{
    # This function will pull in the server log
    $uri = $Global:uri+'event_log'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-Transaction_log{
    # This function will get the config API transaction log.
    $uri = $Global:uri+'transaction_log'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-Schediler{
    # Funtion to get schediler
    $uri = $Global:uri+'project/_scheduler'
    Write-Host $uri
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-SchedilerPriorities{
    # Funtion to get schediler
    $uri = $Global:uri+'project/_scheduler/priorities'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-IotGateway{
    # Funtion to Get the IotGateway 
    $uri = $Global:uri+'project/_iot_gateway'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-ServerUserGroup{
    # This Function will read the server user groups.
    $uri = $Global:uri+'admin/server_usergroups'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-Project{
    # Function to get the project properties.
    $uri = $Global:uri+'project'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-ServerUser{
    # Function to get the server users.
    $uri = $Global:uri+'admin/server_users'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-Channel{
    # Function to get the server channels.
    $uri = $Global:uri+'project/channels'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-ClinetInterface{
    # Function to get the client interfaces.
    $uri = $Global:uri+'project/client_interfaces'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-ServerService{
    # Function to get services
    $uri = $Global:uri+'project/services'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-UconGlobalData{
    # Function to get the ucon global data.
    $uri = $Global:uri+'project/uconglobaldata'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-Datalogger{
    # Function to get the the Datalogger data
    $uri = $Global:uri+'project/_datalogger'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-DataloggerLogGroup{
    #Function to get LogGroups
    $uri = $Global:uri+'project/_datalogger/log_groups'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-DataloggerTag{
    # Function that gets the data logger tags.
    $uri = $Global:uri+'project/_datalogger/tags'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder

}

Function Get-EfmExporter{
    # Function to get the the EFM exporter.
    $uri = $Global:uri+'project/_efmexporter'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder

}

Function Get-EfmPollGroup{
    # Function to get the efm poll groups.
    $uri = $Global:uri+'project/_efmexporter/poll_groups'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-IotGatewayMqttClient{
    # Function to get the MQTT Clients
    $uri = $Global:uri+'project/_iot_gateway/mqtt_clients'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-IotGatewayRestClient{
    # Function to get the REST cleint config.
    $uri = $Global:uri+'project/_iot_gateway/rest_clients'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder
}

Function Get-IotGatewayRestServer{
    # Function to get the REST Server.
    $uri = $Global:uri+'project/_iot_gateway/rest_servers'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder 
}

Function Get-Alias{
    # Function to get the Aliases Server.
    $uri = $Global:uri+'project/aliases'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder     
}

function Get-IotGateWayThingWorxClient{
    # Function to get the ThingWorx Clients.
    $uri = $Global:uri+'project/_iot_gateway/thingworx_clients'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder 
}

Function Get-SchedulerPriority{
    # Function to get the scheduler priorites Clients.
    $uri = $Global:uri+'project/_scheduler/priorities'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder      

}

Function Get-SchedulerSchedule{
    # Function to get the scheduler schedules Clients.
    $uri = $Global:uri+'project/_scheduler/schedules'
    Invoke-RestMethod -Uri $uri -Headers $Global:headder   
}


# Congig API functions that require 1 input.

Function Get-ServerUserGroupByName{
    param ($name)
    $a = $uri + "admin/server_usergroups/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder    
}

Function Get-ServerUserGroupProjectPermByName{
    param ($name)
    $a = $uri + "admin/server_usergroups/" + $name + "/project_permissions"
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-ServerUserByName {
    param ($name)
    $a = $uri + "admin/server_users/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-ServerAliasesByName {
    param ($name)
    $a = $uri + "project/aliases/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-ServerChannelByName {
    param ($name)
    $a = $uri + "project/channels/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-ServerDevicesByChannelName {
    param ($name)
    $a = $uri + "project/channels/" + $name + "/devices"
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-ServerPhoneBookByChannelName {
    param ($name)
    $a = $uri + "project/channels/" + $name + "/phonebooks"
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-ClientInterfaceByName {
    param ($name)
    $a = $uri + "project/client_interfaces/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-ServerServiceByName {
    param ($name)
    $a = $uri + "project/services/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-ServerServiceJobsByName {
    param ($name)
    $a = $uri + "project/services/" + $name + "/jobs"
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-UconGlobalDataByName {
    param ($name)
    $a = $uri + "project/uconglobaldata/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-DataloggerLogGroupByName {
    param ($name)
    $a = $uri + "project/_datalogger/log_groups/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-DataloggerLogGroupServicesByName {
    param ($name)
    $a = $uri + "project/_datalogger/log_groups/" + $name + "/services"
    Invoke-RestMethod -Uri $a -Headers $headder     
}
Function Get-DataloggerLogGroupColumnMappingByName {
    param ($name)
    $a = $uri + "project/_datalogger/log_groups/" + $name + "/column_mappings"
    Invoke-RestMethod -Uri $a -Headers $headder     
}

Function Get-DataloggerLogGroupLogItemsByName{
    param ($name)
    $a = $uri + "project/_datalogger/log_groups/" + $name + "/log_items"
    Invoke-RestMethod -Uri $a -Headers $headder    
}

Function Get-DataloggerLogGroupTagsByName{
    param ($name)
    $a = $uri + "project/_datalogger/log_groups/" + $name + "/tags"
    Invoke-RestMethod -Uri $a -Headers $headder    
}

Function Get-DataloggerLogGroupTriggerByName{
    param ($name)
    $a = $uri + "project/_datalogger/log_groups/" + $name + "/triggers"
    Invoke-RestMethod -Uri $a -Headers $headder    
}

Function Get-DataloggerTagByName{
    param ($name)
    $a = $uri + "project/_datalogger/tags/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder 
}

function Get-EfmPollGroupByName{
    param ($name)
    $a = $uri + "project/_efmexporter/poll_groups/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder
}

Function Get-IotGatewayMqttClientByName{
    param ($name)
    $a = $uri + "project/_iot_gateway/mqtt_clients/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder

}

Function Get-IotGatewayMqttClientItemsByName{
    param ($name)
    $a = $uri + "project/_iot_gateway/mqtt_clients/" + $name + "/iot_items"
    Invoke-RestMethod -Uri $a -Headers $headder

}

Function Get-IotGatewayMRestClientByName{
    param ($name)
    $a = $uri + "project/_iot_gateway/rest_clients/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder

}

Function Get-IotGatewayRestClientItemsByName{
    param ($name)
    $a = $uri + "project/_iot_gateway/rest_clients/" + $name + "/iot_items"
    Invoke-RestMethod -Uri $a -Headers $headder

}

Function Get-IotGatewayRestServerByName{
    param ($name)
    $a = $uri + "project/_iot_gateway/rest_servers/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder

}

Function Get-IotGatewayRestServerItemsByName{
    param ($name)
    $a = $uri + "project/_iot_gateway/rest_servers/" + $name + "/iot_items"
    Invoke-RestMethod -Uri $a -Headers $headder

}

Function Get-IotGatewayThingWorxClientByName{
    param ($name)
    $a = $uri + "project/_iot_gateway/thingworx_clients/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder

}

Function Get-IotGatewayThingWorxClientItemsByName{
    param ($name)
    $a = $uri + "project/_iot_gateway/thingworx_clients/" + $name + "/iot_items"
    Invoke-RestMethod -Uri $a -Headers $headder

}

Function Get-SchedulerPriorityByName{
    param ($name)
    $a = $uri + "project/_scheduler/priorities/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder   
}

Function Get-SchedulerScheduleByName{
    param ($name)
    $a = $uri + "project/_scheduler/schedules/" + $name
    Invoke-RestMethod -Uri $a -Headers $headder   
}

Function Get-SchedulerScheduleRealTimeObjectsByName{
    param ($name)
    $a = $uri + "project/_scheduler/schedules/" + $name + "/real_time_objects"
    Invoke-RestMethod -Uri $a -Headers $headder    
}

Function Get-SchedulerScheduleRecurrenceGroupsByName{
    param ($name)
    $a = $uri + "project/_scheduler/schedules/" + $name + "/recurrence_groups"
    Invoke-RestMethod -Uri $a -Headers $headder

}

Get-EventLog | Format-Table





# Congig API functions that require 2 inputs.




<# Mis Tools
Function Get-APICRED{
# This Funtion will collect the Server Config API username and password.
    $username = Read-Host -Prompt Enter the config API username:
    $password = Read-Host -Prompt Enter the config API password, cannot be null:
    $secpassword = ConvertTo-SecureString $password -AsPlainText -Force
    $credential = New-Object System.Management.Automation.PSCredential($username, $secpassword)
}

Function Get-SERVERIP{
    # Small funtion to get the server's IP
    $ip = Read-Host -Prompt Enter the server IP address:
}

Function Get-SERVERPORT{
    # Small funtion to get the server's port number.
    $port = read-host -prompt Enter the server port number:
}

Function Test-CONNECT{
    # Test TCP connection
    $ip = '127.0.0.1'
    $port = '57415'
    $result = Test-Connection $ip -TCPport $port    
    if ($result -eq 'True'){
        Write-host 'Connected'
    }
    Else {
        Write-host 'Connect Failed'
    }
}

Function Get-ADMIN {
    #This function will retrive the admin setting.
    $username = 'Administrator'
    $password = ''
    $uri = 'http://127.0.0.1:57412/config/v1/admin'
    $headder = @{ Authorization = "Basic {0}" -f [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $username,$password)))}
    Invoke-RestMethod -Uri $uri -Headers $headder
}

#>

