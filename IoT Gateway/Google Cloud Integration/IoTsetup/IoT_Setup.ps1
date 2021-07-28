param([switch]$Elevated) #lines 1-15: Verify script is being run as administrator to ensure sufficient privileges. If not run as admin, restart as such

function Test-Admin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent())
    $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

if ((Test-Admin) -eq $false)  {
    if ($elevated) {
        # tried to elevate, did not work, aborting
    } else {
        Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
    }
    exit
}

$global:terminateScript = $false;
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Application]::EnableVisualStyles()

################## Functions #######################

Function Get-Filename($initialDirectory) {
	[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null
	$OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog
	$OpenFileDialog.initialDirectory = $initialDirectory
	$OpenFileDialog.filter = "JSON (*.json) | *.json"
	$OpenFileDialog.ShowDialog() | Out-Null
	return $OpenFileDialog.filename
}
	
Function Test-IsUuid
{
	[OutputType([bool])]
	param
	(
	   [Parameter(Mandatory = $true)]
	   [string]$ObjectUuid
	)
	# Define verification regex; what the UUID format should look like
	[regex]$uuidRegex = '(?im)^[{(]?[0-9A-F]{8}[-]?(?:[0-9A-F]{4}[-]?){3}[0-9A-F]{12}[)}]?$'
	# Check uuid against regex
	return $ObjectUuid -match $uuidRegex
}

Function Set-Refresh($agent) {
    $taskName = "Kepware IoTGateway JWT Refresh - " + $agent
    $jwtReDir = "$Env:ProgramData\iotjwtre_" + $agent
    $action = New-ScheduledTaskAction -Execute 'PowerShell.exe' `
    -Argument "-ExecutionPolicy Bypass -NoProfile $jwtReDir\updateJWT.ps1" `
    -WorkingDirectory $jwtReDir
    $trigger = New-ScheduledTaskTrigger `
    -Once `
    -At ( Get-Date ) `
    -RepetitionInterval (New-TimeSpan -Hours 1 -Minutes 30) `
    -RepetitionDuration (New-TimeSpan -Days (365 * 20))
    $principal = New-ScheduledTaskPrincipal -UserID "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount 
    Register-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -TaskName $taskName
    $task = Get-ScheduledTask -TaskName "$taskName"
    $task.Settings.ExecutionTimeLimit = "PT1M"
    Set-ScheduledTask $task
}
    
Function Cert-Check ($SelectedPath){
	$certFolderReady=$false
    if (-Not ([string]::IsNullorEmpty($SelectedPath))){
		Write-Host ( Get-ChildItem $SelectedPath -Include *.cer, *.pem -Force | Measure-Object ).Count " certificate count before check"
		if (( Get-ChildItem $SelectedPath -Include *.cer, *.pem -Force | Measure-Object ).Count -gt 0){
			Write-Host "Must delete pre-existing files in selected folder"
			[void] [System.Reflection.Assembly]::LoadWithPartialName("Microsoft.VisualBasic") 
			$ccmsgBoxInput = [Microsoft.VisualBasic.Interaction]::MsgBox("Certificates already present in chosen folder: `n`nWould you like to overwrite these certificates? `n`nClick Yes to overwrite, No to select a different folder or Cancel to Exit", "YesNoCancel,SystemModal,Information,DefaultButton2", "Certificates already present in chosen folder")
			switch ($ccmsgBoxInput){
				'Yes' {
					Remove-Item -Path $SelectedPath -Include *.cer, *.pem -Force
					$certFolderReady=$true
				}
				'No' {
					$certFolderReady=$false
				}
				'Cancel' {
					Exit
					$global:terminateScript = $true
				}
			}
			Write-Host ( Get-ChildItem $SelectedPath -Include *.cer, *.pem | Measure-Object ).Count " certificate count after check"
		}
		else{
			$certFolderReady=$true
		}
	}
		return $certFolderReady
}

Function Get-Folder ($initialDirectory) {
	$certFolderReady=$false
	Write-Host $initialDirectory " is the initial directory"
    while ($certFolderReady -eq $false){###loop here to force reselection of new folder for ceritifcates if there is an issue with initial selection
		[void] [System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms')
		$FolderBrowserDialog = New-Object System.Windows.Forms.FolderBrowserDialog
		$FolderBrowserDialog.RootFolder = 'MyComputer'
		$FolderBrowserDialog.Description = "Select location for certificates"
		
		if ($initialDirectory) { $FolderBrowserDialog.SelectedPath = $initialDirectory }
		$Result = $FolderBrowserDialog.ShowDialog()
		if ($Result -eq "OK"){
						Write-Host $FolderBrowserDialog.SelectedPath "is path passed to SelectedPath below"
						$SelectedPath = $FolderBrowserDialog.SelectedPath+'\*'###+'\*' concatenation required for Cert-Check to check for certificates
						$certFolderReady = Cert-Check $SelectedPath
		}
		elseif ($Result -eq "Cancel"){
						$certFolderReady=$true
						$global:terminateScript = $true;
						Write-Host "Exit triggered by Cancel button"
						Exit
		}
	}
	return $FolderBrowserDialog.SelectedPath
}

################## Form #######################

$Form                            = New-Object system.Windows.Forms.Form
$Form.ClientSize                 = New-Object System.Drawing.Point(400,500)
$Form.text                       = "Oden Technologies -  MQTT Client Setup v3"
$Form.TopMost                    = $true

$AdminLogin                      = New-Object system.Windows.Forms.TextBox
$AdminLogin.multiline            = $false
$AdminLogin.width                = 125
$AdminLogin.height               = 20
$AdminLogin.visible              = $true
$AdminLogin.location             = New-Object System.Drawing.Point(25,73)
$AdminLogin.Font                 = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$AdminPass                       = New-Object system.Windows.Forms.MaskedTextBox
$AdminPass.multiline             = $false
$AdminPass.width                 = 125
$AdminPass.height                = 20
$AdminPass.PasswordChar          = "*"
$AdminPass.location              = New-Object System.Drawing.Point(25,119)
$AdminPass.Font                  = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$IoTAgentName                    = New-Object system.Windows.Forms.TextBox
$IoTAgentName.multiline          = $false
$IoTAgentName.width              = 256
$IoTAgentName.height             = 20
$IoTAgentName.location           = New-Object System.Drawing.Point(25,200)
$IoTAgentName.Font               = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$DeviceID                       = New-Object system.Windows.Forms.TextBox
$DeviceID.multiline             = $false
$DeviceID.width                 = 256
$DeviceID.height                = 20
$DeviceID.location              = New-Object System.Drawing.Point(25,250)
$DeviceID.Font                  = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$Subfolder                       = New-Object system.Windows.Forms.TextBox
$Subfolder.multiline             = $false
$Subfolder.width                 = 256
$Subfolder.height                = 20
$Subfolder.location              = New-Object System.Drawing.Point(25,300)
$Subfolder.Font                  = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$RegistryID                        = New-Object system.Windows.Forms.TextBox
$RegistryID.multiline              = $false
$RegistryID.width                  = 256
$RegistryID.height                 = 20
$RegistryID.location               = New-Object System.Drawing.Point(25,350)
$RegistryID.Font                   = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$GCP_proj                       = New-Object system.Windows.Forms.TextBox
$GCP_proj.multiline             = $false
$GCP_proj.width                 = 256
$GCP_proj.height                = 20
$GCP_proj.location              = New-Object System.Drawing.Point(25,400)
$GCP_proj.Font                  = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$WinForm1                        = New-Object system.Windows.Forms.Form
$WinForm1.ClientSize             = New-Object System.Drawing.Point(400,400)
$WinForm1.text                   = "Form"
$WinForm1.TopMost                = $false

$Label1                          = New-Object system.Windows.Forms.Label
$Label1.text                     = "Username"
$Label1.AutoSize                 = $true
$Label1.width                    = 25
$Label1.height                   = 10
$Label1.location                 = New-Object System.Drawing.Point(25,54)
$Label1.Font                     = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$Label2                          = New-Object system.Windows.Forms.Label
$Label2.text                     = "Password"
$Label2.AutoSize                 = $true
$Label2.width                    = 25
$Label2.height                   = 10
$Label2.location                 = New-Object System.Drawing.Point(25,102)
$Label2.Font                     = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$Label3                          = New-Object system.Windows.Forms.Label
$Label3.text                     = "Device ID"
$Label3.AutoSize                 = $true
$Label3.width                    = 25
$Label3.height                   = 10
$Label3.location                 = New-Object System.Drawing.Point(25,230)
$Label3.Font                     = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$Label4                          = New-Object system.Windows.Forms.Label
$Label4.text                     = "Subfolder"
$Label4.AutoSize                 = $true
$Label4.width                    = 25
$Label4.height                   = 10
$Label4.location                 = New-Object System.Drawing.Point(25,280)
$Label4.Font                     = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$Label5                          = New-Object system.Windows.Forms.Label
$Label5.text                     = "Connection Name"
$Label5.AutoSize                 = $true
$Label5.width                    = 25
$Label5.height                   = 10
$Label5.location                 = New-Object System.Drawing.Point(25,180)
$Label5.Font                     = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$Label6                          = New-Object system.Windows.Forms.Label
$Label6.text                     = "Kepware IoT Gateway"
$Label6.AutoSize                 = $true
$Label6.width                    = 25
$Label6.height                   = 10
$Label6.location                 = New-Object System.Drawing.Point(25,155)
$Label6.Font                     = New-Object System.Drawing.Font('Microsoft Sans Serif',10,[System.Drawing.FontStyle]([System.Drawing.FontStyle]::Underline))

$Label7                          = New-Object system.Windows.Forms.Label
$Label7.text                     = "KEPServerEX Credentials"
$Label7.AutoSize                 = $true
$Label7.width                    = 25
$Label7.height                   = 10
$Label7.location                 = New-Object System.Drawing.Point(25,29)
$Label7.Font                     = New-Object System.Drawing.Font('Microsoft Sans Serif',10,[System.Drawing.FontStyle]([System.Drawing.FontStyle]::Underline))

$Label8                          = New-Object system.Windows.Forms.Label
$Label8.text                     = "Registry"
$Label8.AutoSize                 = $true
$Label8.width                    = 25
$Label8.height                   = 10
$Label8.location                 = New-Object System.Drawing.Point(25,330)
$Label8.Font                     = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$Label9                          = New-Object system.Windows.Forms.Label
$Label9.text                     = "(default: `"Administrator`")"
$Label9.AutoSize                 = $true
$Label9.width                    = 25
$Label9.height                   = 10
$Label9.location                 = New-Object System.Drawing.Point(161,77)
$Label9.Font                     = New-Object System.Drawing.Font('Microsoft Sans Serif',10,[System.Drawing.FontStyle]([System.Drawing.FontStyle]::Italic))

$Label10                         = New-Object system.Windows.Forms.Label
$Label10.text                    = "(default: password required)"
$Label10.AutoSize                = $true
$Label10.width                   = 25
$Label10.height                  = 10
$Label10.location                = New-Object System.Drawing.Point(161,121)
$Label10.Font                    = New-Object System.Drawing.Font('Microsoft Sans Serif',10,[System.Drawing.FontStyle]([System.Drawing.FontStyle]::Italic))

$Label11                          = New-Object system.Windows.Forms.Label
$Label11.text                     = "GCP Project"
$Label11.AutoSize                 = $true
$Label11.width                    = 25
$Label11.height                   = 10
$Label11.location                 = New-Object System.Drawing.Point(25,380)
$Label11.Font                     = New-Object System.Drawing.Font('Microsoft Sans Serif',10)

$Button1                         = New-Object system.Windows.Forms.Button
$Button1.text                    = "Submit"
$Button1.width                   = 60
$Button1.height                  = 30
$Button1.location                = New-Object System.Drawing.Point(25,450)
$Button1.Font                    = New-Object System.Drawing.Font('Microsoft Sans Serif',10)
$Button1.DialogResult =  [System.Windows.Forms.DialogResult]::None

$Button2                         = New-Object system.Windows.Forms.Button
$Button2.text                    = "Cancel"
$Button2.width                   = 60
$Button2.height                  = 30
$Button2.location                = New-Object System.Drawing.Point(123,450)
$Button2.Font                    = New-Object System.Drawing.Font('Microsoft Sans Serif',10)
$Button2.DialogResult =  [System.Windows.Forms.DialogResult]::Cancel

$Button3                         = New-Object system.Windows.Forms.Button
$Button3.text                    = "Upload Config File"
$Button3.width                   = 140
$Button3.height                  = 30
$Button3.location                = New-Object System.Drawing.Point(221,450)
$Button3.Font                    = New-Object System.Drawing.Font('Microsoft Sans Serif',10)
$Button3.DialogResult =  [System.Windows.Forms.DialogResult]::None

$Form.AcceptButton = $Button1
$Form.CancelButton = $Button2
$Form.controls.AddRange(@($AdminLogin,$AdminPass,$IoTAgentName,$DeviceID,$Subfolder,$RegistryID,$GCP_proj,$Label1,$Label2,$Label3,$Label4,$Label5,$Label6,$Label7,$Label8,$Label9,$Label10, $Label11, $Button1,$Button2,$Button3))

####Submit button
$Button1.Add_Click(
{
	#check all values are not length zero
	if (($IoTAgentName.text.length -lt 1) -or ($DeviceID.Text.length -lt 1) -or ($Subfolder.Text.length -lt 1) -or ($RegistryID.Text.length -lt 1) -or ($AdminLogin.Text.length -lt 1) -or ($AdminPass.Text.length -lt 1) -or ($GCP_proj.Text.length -lt 1)){
		Write-Host "Testing form fields are empty"
		[void] [System.Reflection.Assembly]::LoadWithPartialName("Microsoft.VisualBasic") 
		[Microsoft.VisualBasic.Interaction]::MsgBox("One or more required form fields are missing. Please retry.", "OKOnly,SystemModal,Exclamation,DefaultButton1", "Validation Failed")
		}
	# validate UUID is valid type
	elseif (-Not(Test-IsUuid -ObjectUuid $DeviceID.Text)){
		Write-Host "Missing valid UUID"
		[void] [System.Reflection.Assembly]::LoadWithPartialName("Microsoft.VisualBasic") 
		[Microsoft.VisualBasic.Interaction]::MsgBox("Invalid UUID. Please check format and retry.", "OKOnly,SystemModal,Exclamation,DefaultButton1", "Validation Failed")
	}else{
		Write-Host "Fields populated, valid UUID: Ready to Go!"
		$Form.close()
	}
})

####Cancel button
$Button2.Add_Click({
	Write-Host "User Canceled" -BackgroundColor Red -ForegroundColor White
	$form.Close()
	$form.Dispose()
	$global:terminateScript=$true
})

####Select File button
$Button3.Add_Click({
		$upload_config = Get-Filename C:\Users
		Write-Host "File path is "$upload_config 

		# 1. Validate JSON file contents
		if (-Not ([string]::IsNullorEmpty($upload_config))){
			$jsonText = Get-Content $upload_config -Raw
			$powershellRepresentation = ConvertFrom-Json $jsonText -ErrorAction SilentlyContinue -ErrorVariable ProcessError
				If ($ProcessError) {
					[void] [System.Reflection.Assembly]::LoadWithPartialName("Microsoft.VisualBasic") 
					[Microsoft.VisualBasic.Interaction]::MsgBox("JSON Validation Failed: `n`nAt lease part of selected .json has a format issue. `n`nPlease check and retry.", "OKOnly,SystemModal,Exclamation,DefaultButton1", "Validation Conflict")
					Write-Host "Provided text is not a valid JSON string"
				}else{
					Write-Host "JSON PASSED"
				}
		}		
		if (-Not ([string]::IsNullorEmpty($jsonID.DeviceID))){
				Test-IsUuid -ObjectUuid $DeviceID.Text #Test-IsUuid -ObjectUuid '123e4567-e89b-12d3-a456-426614174000'
				Write-Host "UUID looks good"
				if (-Not (Test-IsUuid -ObjectUuid $DeviceID.Text)){
					[void] [System.Reflection.Assembly]::LoadWithPartialName("Microsoft.VisualBasic") 
					[Microsoft.VisualBasic.Interaction]::MsgBox("UUID validation failed: Bad UUID format.", "OKOnly,SystemModal,Exclamation,DefaultButton1", "Validation Conflict")
					Write-Host "UUID has an issue"
				}
		}
				#fill in the form fields/assign values
		if (-Not ([string]::IsNullorEmpty($upload_config))){		
				$jsonID = Get-Content -Raw $upload_config -ErrorAction SilentlyContinue | ConvertFrom-Json
				if (-Not ([string]::IsNullorEmpty($jsonID.DeviceID))){Write-Host $jsonID.DeviceID " obtained from JSON"}
				if (-Not ([string]::IsNullorEmpty($jsonID.Subfolder))){Write-Host $jsonID.Subfolder " obtained from JSON"}
				if (-Not ([string]::IsNullorEmpty($jsonID.RegistryID))){Write-Host $jsonID.RegistryID " obtained from JSON"}
				$DeviceID.Text=$jsonID.DeviceID
				$Subfolder.Text=$jsonID.Subfolder
				$RegistryID.Text=$jsonID.RegistryID
		}})

[void]$Form.ShowDialog()
###END of form code

###If user hit cancel button on form this will end remainder of script
if ( $global:terminateScript -eq $true ){
	Write-Host "terminateScript was changed to 'true' by the user" -BackgroundColor Red -ForegroundColor White
	Exit
}

Write-Host 	$IoTAgentName.Text " obtained from form"
Write-Host 	$DeviceID.Text " obtained from form"
Write-Host 	$Subfolder.Text " obtained from form"
Write-Host 	$RegistryID.Text " obtained from form"

$WORK_DIR = Get-Folder C:\Users\$ENV:UserName\Documents
Write-Host $WORK_DIR "after Get-Folder loop"

#Write-Host $AdminLogin.text
#Write-Host $AdminPass.text
#$IoTAgentName.text
#$DeviceID.text  # UUID
#$FactoryID.text     # Subfolder
#$ClientId.text      # Registry

$IoTjwtreTaskName = "iotjwtre_"+$IoTAgentName.text

$Cert = New-SelfSignedCertificate -CertStoreLocation "Cert:\LocalMachine\My" -HashAlgorithm "SHA256" -KeyAlgorithm RSA -KeyLength 2048 -KeyUsage DigitalSignature -Subject "CN=unused"
Export-Certificate -Cert $Cert -Type CERT -FilePath "$WORK_DIR\rsa_cert.cer"
certutil.exe -encode "$WORK_DIR\rsa_cert.cer" "$WORK_DIR\rsa_cert.pem"

############### FIRST TIME RUN #########################################
#create a folder to store jwt updater powershell script

$iotJwtRefresherFolder ="$Env:ProgramData\"+"$IoTjwtreTaskName"
Write-Host $iotJwtRefresherFolder
if (-Not(Test-Path $iotJwtRefresherFolder)){
	New-Item -ItemType directory -Path C:\ProgramData\ -Name $iotJwtreTaskName
}
else{
	Write-Host "Device Folder already exists!"
	[void] [System.Reflection.Assembly]::LoadWithPartialName("Microsoft.VisualBasic") 
	[Microsoft.VisualBasic.Interaction]::MsgBox("Device Folder already exists! `n`nPlease delete old devices.", "OKOnly,SystemModal,Exclamation,DefaultButton1", "Folder already exists")
	Exit
}

&icacls "$iotJwtRefresherFolder" /inheritance:r 

&icacls "$iotJwtRefresherFolder" /grant:r "CREATOR OWNER:(OI)(CI)F" /T 
&icacls "$iotJwtRefresherFolder" /grant "BUILTIN\Administrators:(OI)(CI)F" /T 
&icacls "$iotJwtRefresherFolder" /grant "LOCAL SERVICE:(OI)(CI)F" /T
#######################################################################
$gcpProject = $GCP_proj.text
$configdata = @"
gcp.project=$gcpProject
cert.path=Cert:\\LocalMachine\\My\\$($Cert.Thumbprint)
"@
$configdata > "$iotJwtRefresherFolder\config.txt"

#JWT creation and preliminary functions
function ConvertTo-Base64-FromString ([parameter(ValueFromPipeline)] $StringInput ) {
    Write-Output([Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($StringInput)))
}

function Replace-Chars ([parameter(ValueFromPipeline)] $StringInput ) {
    Write-Output ($StringInput -replace '\+' , '-' -replace '/' , '_' -replace '=' )
}

function New-IotCoreJwt ($Algorithm ='RS256', $ValidSeconds=7200 ) {
    $ConfigProps = convertfrom-stringdata ( get-content "$Env:ProgramData\$IoTjwtreTaskName\config.txt" -raw)
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
    Write-Output($ToSign + '.' + $EncodedSignature)
}

#create JWT
$Jwt = New-IotCoreJwt

#create functions for MQTT Agent on IOT Gateway Plugin through Config API
function Get-AdminHeader() {
    $EncodedCred = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes($AdminLogin.text + ":" + $AdminPass.text))
    Write-Output (@{ Authorization = "Basic $EncodedCred " })
}

function Create-IoTGatewayAgent ( $Jwt , $AgentName = $IoTAgentName.text , $Region = 'us-central1' , $Registry = $RegistryID.text , $Device = $DeviceID.text ) {
    $ConfigProps = convertfrom-stringdata ( get-content "$Env:ProgramData\$IoTjwtreTaskName\config.txt" -raw)
    $Uri = 'http://127.0.0.1:57412/config/v1/project/_iot_gateway/mqtt_clients'
    $EventsTopic = '/devices/{0}/events/{1}' -f $Device , $Subfolder.text
    $RegistryID = 'projects/{0}/locations/{1}/registries/{2}/devices/{3}' -f $ConfigProps. 'gcp.project' , $Region , $Registry , $Device
    $Body = @{
    "common.ALLTYPES_NAME" = $AgentName ;
    "iot_gateway.MQTT_CLIENT_URL" = "ssl://mqtt.googleapis.com:8883" ;
    "iot_gateway.MQTT_CLIENT_TOPIC" = $EventsTopic ;
    "iot_gateway.MQTT_CLIENT_CLIENT_ID" = $RegistryID ;
    "iot_gateway.MQTT_CLIENT_USERNAME" = "unused" ;
    "iot_gateway.MQTT_CLIENT_PASSWORD" = $Jwt ;
    "iot_gateway.MQTT_CLIENT_QOS" = 1 ;
    "iot_gateway.AGENTTYPES_RATE_MS" = 1000 ;
    "iot_gateway.AGENTTYPES_PUBLISH_FORMAT" = 1
    }
    $Payload = ConvertTo-Json $Body
    Invoke-RestMethod -Uri $Uri -Method Post -Headers (Get-AdminHeader) -Body $Payload
}

#create MQTT client with password field filled with JWT
Create-IoTGatewayAgent $Jwt

#create Scheduled Task to refresh JWT
Set-Refresh $IoTAgentName.text

$scriptContent = @'
function ConvertTo-Base64-FromString ([parameter(ValueFromPipeline)] $StringInput) {
Write-Output([Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($StringInput)))
}

function Replace-Chars ([parameter(ValueFromPipeline)] $StringInput) {
Write-Output($StringInput -replace '\+','-' -replace '/','_' -replace '=')
}

function New-IotCoreJwt ($Algorithm='RS256', $ValidSeconds=7200) {
$ConfigProps = convertfrom-stringdata (get-content "$Env:ProgramData\REPLACE_1\config.txt" -raw)
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
$EncodedCred = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes('AdminLogin.text:AdminPass.text'))
Write-Output(@{ Authorization = "Basic $EncodedCred" })
}

function Update-AgentJWT ($AgentName='REPLACE_2') {
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
$scriptContent > "$Env:ProgramData\$IoTjwtreTaskName\updateJWT.ps1"

$content = Get-Content -Path "$Env:ProgramData\$IoTjwtreTaskName\updateJWT.ps1"
$newContent = $content -replace 'REPLACE_1', $IoTjwtreTaskName
$newContent = $newContent -replace 'REPLACE_2', $IoTAgentName.text
$newContent = $newContent -replace 'AdminLogin.text', $AdminLogin.text
$newContent = $newContent -replace 'AdminPass.text', $AdminPass.text
$newContent | Set-Content -Path "$Env:ProgramData\$IoTjwtreTaskName\updateJWT.ps1"