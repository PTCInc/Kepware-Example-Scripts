# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
$Cert = New-SelfSignedCertificate -CertStoreLocation "Cert:\LocalMachine\My" -HashAlgorithm "SHA256" -KeyAlgorithm RSA -KeyLength 2048 -KeyUsage DigitalSignature -Subject "CN=unused"

$WORK_DIR = 'C:\Users\ttosun\Documents\GoogleTest' #Specify a folder for temporary files

Export-Certificate -Cert $Cert -Type CERT -FilePath "$WORK_DIR\rsa_cert.cer"

certutil.exe -encode "$WORK_DIR\rsa_cert.cer" "$WORK_DIR\rsa_cert.pem"

gcloud config set project coastal-throne-266515 # project_ID here
gcloud pubsub topics create kepware-msg #create a topic for your google device
gcloud iot registries create kepware-devices ` #create a registry
--region europe-west1 `
--event-notification-config=topic=kepware-msg

gcloud iot devices create kepware-device ` #create a device with the cert file created earlier
--region=europe-west1 `
--registry=kepware-devices `
--public-key=path="$WORK_DIR\rsa_cert.pem",type=rsa-x509-pem


#create a folder to store jwt updater powershell script
$iotJwtRefresherFolder ="$Env:ProgramData\iotjwtre" 

New-Item -ItemType directory -Path $iotJwtRefresherFolder
 
&icacls "$iotJwtRefresherFolder" /inheritance:r 

&icacls "$iotJwtRefresherFolder" /grant:r "CREATOR OWNER:(OI)(CI)F" /T 
&icacls "$iotJwtRefresherFolder" /grant "BUILTIN\Administrators:(OI)(CI)F" /T 
&icacls "$iotJwtRefresherFolder" /grant "LOCAL SERVICE:(OI)(CI)F" /T

$configdata = @"
gcp.project=coastal-throne-266515
cert.path=Cert:\\LocalMachine\\My\\$($Cert.Thumbprint)
"@
$configdata > "$Env:ProgramData\iotjwtre\config.txt"

#JWT creation and preliminary functions
function ConvertTo-Base64-FromString ([parameter(ValueFromPipeline)] $StringInput ) {
Write-Output([Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($StringInput)))}

function Replace-Chars ([parameter(ValueFromPipeline)] $StringInput ) {
Write-Output ($StringInput -replace '\+' , '-' -replace '/' , '_' -replace '=' )}

function New-IotCoreJwt ($Algorithm ='RS256', $ValidSeconds=7200 ) {
$ConfigProps = convertfrom-stringdata ( get-content "$Env:ProgramData\iotjwtre\config.txt" -raw)
$Header = '{{"alg":"{0}","typ":"JWT"}}' -f $Algorithm
$Now = [Math]::Floor([decimal]( Get-Date ( Get-Date ).ToUniversalTime() -UFormat '%s'))
$Exp = $Now + $ValidSeconds
$Claim = '{{"aud":"{0}","iat":{1},"exp":{2}}}' -f $ConfigProps.'gcp.project', $Now, $Exp
$EncodedHeader = $Header | ConvertTo-Base64-FromString | Replace-Chars
$EncodedClaim = $Claim | ConvertTo-Base64-FromString | Replace-Chars
$ToSign = $EncodedHeader + '.' + $EncodedClaim
$EncodedToSign = [System.Text.Encoding]::UTF8.GetBytes($ToSign)
$Cert = (Get-ChildItem -Path $ConfigProps.'cert.path')
$Key = [System.Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($Cert)
$Signature = $Key.SignData($EncodedToSign, [Security.Cryptography.HashAlgorithmName]::SHA256, [Security.Cryptography.RSASignaturePadding]::Pkcs1)
$EncodedSignature = [Convert]::ToBase64String($Signature) | Replace-Chars
Write-Output($ToSign + '.' + $EncodedSignature)}

#create JWT
$Jwt = New-IotCoreJwt

#create functions for MQTT Agent on IOT Gateway Plugin through Config API
function Get-AdminHeader() {
$EncodedCred = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes('Administrator:'))
Write-Output (@{ Authorization = "Basic $EncodedCred " })}

function Create-IoTGatewayAgent ( $Jwt , $AgentName = 'IoTCore' , $Region = 'europe-west1' , $Registry = 'kepware-devices' , $Device = 'kepware-device' ) {
$ConfigProps = convertfrom-stringdata ( get-content "$Env:ProgramData\iotjwtre\config.txt" -raw)
$Uri = 'http://127.0.0.1:57412/config/v1/project/_iot_gateway/mqtt_clients'
$EventsTopic = '/devices/{0}/events' -f $Device
$ClientId = 'projects/{0}/locations/{1}/registries/{2}/devices/{3}' -f $ConfigProps. 'gcp.project' , $Region , $Registry , $Device
$Body = @{
"common.ALLTYPES_NAME" = $AgentName ;
"iot_gateway.MQTT_CLIENT_URL" = "ssl://mqtt.googleapis.com:8883" ;
"iot_gateway.MQTT_CLIENT_TOPIC" = $EventsTopic ;
"iot_gateway.MQTT_CLIENT_CLIENT_ID" = $ClientId ;
"iot_gateway.MQTT_CLIENT_USERNAME" = "unused" ;
"iot_gateway.MQTT_CLIENT_PASSWORD" = $Jwt
}
$Payload = ConvertTo-Json $Body
Invoke-RestMethod -Uri $Uri -Method Post -Headers (Get-AdminHeader) -Body $Payload}

#create MQTT client with password field filled with JWT
Create-IoTGatewayAgent $Jwt

#add a tag to MQTT Agent
function Create-ServerTag( $AgentName = 'IoTCore' ) {
$Uri = 'http://127.0.0.1:57412/config/v1/project/_iot_gateway/mqtt_clients/{0}/iot_items' -f $AgentName
$Body = @{
"iot_gateway.IOT_ITEM_SERVER_TAG" = "Channel1.Device1.Random1" ;
"iot_gateway.IOT_ITEM_USE_SCAN_RATE" = $true ;
"iot_gateway.IOT_ITEM_SCAN_RATE_MS" = 20000 ;
"iot_gateway.IOT_ITEM_SEND_EVERY_SCAN" = $true ;
"iot_gateway.IOT_ITEM_ENABLED" = $true
}
$Payload = ConvertTo-Json $Body
Invoke-RestMethod -Uri $Uri -Method Post -Headers (Get-AdminHeader) -Body $Payload}

#create a subscription for visualizing the data flow
gcloud pubsub subscriptions create verify-kepware-msg `
--topic=kepware-msg

#pull data from the subscription
gcloud pubsub subscriptions pull verify-kepware-msg --auto-ack --limit 10
