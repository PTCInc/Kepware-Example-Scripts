# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
$scriptContent = @'
function ConvertTo-Base64-FromString ([parameter(ValueFromPipeline)] $StringInput) {
Write-Output([Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($StringInput)))
}

function Replace-Chars ([parameter(ValueFromPipeline)] $StringInput) {
Write-Output($StringInput -replace '\+','-' -replace '/','_' -replace '=')
}

function New-IotCoreJwt ($Algorithm='RS256', $ValidSeconds=7200) {
$ConfigProps = convertfrom-stringdata (get-content "$Env:ProgramData\iotjwtre\config.txt" -raw)
$Header = '{{"alg":"{0}","typ":"JWT"}}' -f $Algorithm
$Now = [Math]::Floor([decimal](Get-Date (Get-Date).ToUniversalTime() -UFormat '%s'))
$Exp = $Now + $ValidSeconds
$Claim = '{{"aud":"{0}","iat":{1},"exp":{2}}}' -f
$ConfigProps.'gcp.project', $Now, $Exp
$EncodedHeader = $Header | ConvertTo-Base64-FromString | Replace-Chars
$EncodedClaim = $Claim | ConvertTo-Base64-FromString | Replace-Chars
$ToSign = $EncodedHeader + '.' + $EncodedClaim
$EncodedToSign = [System.Text.Encoding]::UTF8.GetBytes($ToSign)
$Cert = (Get-ChildItem -Path $ConfigProps.'cert.path')
$Key = [System.Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($Cert)
$Signature = $Key.SignData($EncodedToSign, [Security.Cryptography.HashAlgorithmName]::SHA256, [Security.Cryptography.RSASignaturePadding]::Pkcs1)
$EncodedSignature = [Convert]::ToBase64String($Signature) | Replace-Chars
Write-Output($ToSign + '.' + $EncodedSignature)
}

function Get-AdminHeader() {
$EncodedCred = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes('Administrator:'))
Write-Output(@{ Authorization = "Basic $EncodedCred" })
}

function Update-AgentJWT ($AgentName='IoTCore') {
$Uri = 'http://127.0.0.1:57412/config/v1/project/_iot_gateway/mqtt_clients/{0}' -f $AgentName
$AgentObj = Invoke-RestMethod -Uri $Uri -Method Get -Headers (Get-AdminHeader)
$Jwt = (New-IotCoreJwt)
$Body = @{
"PROJECT_ID" = $AgentObj.PROJECT_ID;
"iot_gateway.MQTT_CLIENT_USERNAME" = "unused";
"iot_gateway.MQTT_CLIENT_PASSWORD" = $Jwt
}
$Payload = ConvertTo-Json $Body
Invoke-RestMethod -Uri $Uri -Method Put -Headers (Get-AdminHeader) -Body $Payload
}
Update-AgentJWT
'@
$scriptContent > "$Env:ProgramData\iotjwtre\updateJWT.ps1"

