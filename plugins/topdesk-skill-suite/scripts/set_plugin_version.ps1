param(
    [Parameter(Mandatory = $true)]
    [string]$Version,
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

if ($Version -notmatch '^\d+\.\d+\.\d+(-[A-Za-z0-9.-]+)?$') {
    throw "Version must be semantic version format, for example 0.1.0 or 0.2.0-beta.1"
}

$manifestPath = Join-Path (Resolve-Path -LiteralPath $PluginRoot).Path ".codex-plugin\plugin.json"
$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
$manifest.version = $Version
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

Write-Host "Set plugin version to $Version"

