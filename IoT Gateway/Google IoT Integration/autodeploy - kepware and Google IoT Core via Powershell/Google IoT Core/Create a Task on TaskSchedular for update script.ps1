# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
$taskName = "Kepware IoTGateway JWT Refresh"
$jwtReDir = "$Env:ProgramData\iotjwtre"
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