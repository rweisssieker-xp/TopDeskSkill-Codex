<#
.SYNOPSIS
TOPdesk automation script template.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-RequiredPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Path not found: $Path"
    }
    return (Resolve-Path -LiteralPath $Path).Path
}

$resolvedInput = Resolve-RequiredPath -Path $InputPath
$resolvedOutputParent = Split-Path -Parent $OutputPath
if (-not [string]::IsNullOrWhiteSpace($resolvedOutputParent)) {
    New-Item -ItemType Directory -Force -Path $resolvedOutputParent | Out-Null
}

if ($PSCmdlet.ShouldProcess($OutputPath, "Write TOPdesk automation output")) {
    [pscustomobject]@{
        input = $resolvedInput
        generated_at = (Get-Date).ToString("o")
    } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
}

