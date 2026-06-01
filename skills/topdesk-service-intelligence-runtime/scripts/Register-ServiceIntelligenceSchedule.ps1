param(
    [Parameter(Mandatory = $true)]
    [string]$ConfigPath,
    [Parameter(Mandatory = $true)]
    [string]$OutDir,
    [string]$TaskName = "TOPdesk Service Intelligence Runtime",
    [string]$StateDb = "",
    [string]$MonitoringJson = "",
    [string]$Python = "python",
    [string]$At = "06:30",
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "run_service_intelligence.py"
$resolvedScript = (Resolve-Path -LiteralPath $scriptPath).Path
$resolvedConfig = (Resolve-Path -LiteralPath $ConfigPath).Path
$resolvedOutDir = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutDir)

$arguments = @(
    "`"$resolvedScript`"",
    "--config", "`"$resolvedConfig`"",
    "--out-dir", "`"$resolvedOutDir`""
)

if (-not [string]::IsNullOrWhiteSpace($StateDb)) {
    $resolvedStateDb = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($StateDb)
    $arguments += @("--state-db", "`"$resolvedStateDb`"")
}

if (-not [string]::IsNullOrWhiteSpace($MonitoringJson)) {
    $resolvedMonitoringJson = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($MonitoringJson)
    $arguments += @("--monitoring-json", "`"$resolvedMonitoringJson`"")
}

$action = New-ScheduledTaskAction -Execute $Python -Argument ($arguments -join " ")
$trigger = New-ScheduledTaskTrigger -Daily -At $At
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 2) -MultipleInstances IgnoreNew -StartWhenAvailable

if ($WhatIf) {
    [pscustomobject]@{
        TaskName = $TaskName
        Execute = $Python
        Arguments = $arguments -join " "
        Trigger = "Daily at $At"
    } | Format-List
    exit 0
}

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null
Write-Host "Registered scheduled task: $TaskName"

