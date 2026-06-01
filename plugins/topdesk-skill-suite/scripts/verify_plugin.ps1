param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path,
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$Version = "0.1.3"
)

$ErrorActionPreference = "Stop"

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "sync_skills.ps1") -Root $resolvedRoot -PluginRoot $resolvedPluginRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "generate_plugin_assets.ps1") -PluginRoot $resolvedPluginRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "new_plugin_manifest.ps1") -PluginRoot $resolvedPluginRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "new_plugin_inventory.ps1") -PluginRoot $resolvedPluginRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "new_plugin_health_report.ps1") -PluginRoot $resolvedPluginRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "validate_plugin_config.ps1") -PluginRoot $resolvedPluginRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "validate_marketplace_readiness.ps1") -PluginRoot $resolvedPluginRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python (Join-Path $PSScriptRoot "test_mcp_server.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "validate_plugin.ps1") -PluginRoot $resolvedPluginRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "package_plugin.ps1") -Root $resolvedRoot -PluginRoot $resolvedPluginRoot -Version $Version
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "test_plugin_package.ps1") -Root $resolvedRoot -Version $Version
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "new_plugin_checksums.ps1") -Root $resolvedRoot -Version $Version
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Plugin verification completed." -ForegroundColor Green
