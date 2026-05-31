param(
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path
$configPath = Join-Path $resolvedPluginRoot "plugin.config.json"
$manifestPath = Join-Path $resolvedPluginRoot ".codex-plugin\plugin.json"

if (-not (Test-Path -LiteralPath $configPath)) {
    throw "Plugin config not found: $configPath"
}

$config = Get-Content -Raw -LiteralPath $configPath | ConvertFrom-Json
$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json

if ($config.name -ne $manifest.name) {
    throw "Config name '$($config.name)' does not match manifest name '$($manifest.name)'"
}

if ($config.version -ne $manifest.version) {
    throw "Config version '$($config.version)' does not match manifest version '$($manifest.version)'"
}

$skillCount = @(Get-ChildItem -LiteralPath (Join-Path $resolvedPluginRoot "skills") -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}).Count

if ($skillCount -ne [int]$config.expectedSkillCount) {
    throw "Expected $($config.expectedSkillCount) skills, found $skillCount"
}

foreach ($asset in $config.requiredAssets) {
    if (-not (Test-Path -LiteralPath (Join-Path $resolvedPluginRoot $asset))) {
        throw "Required asset missing: $asset"
    }
}

if ($config.PSObject.Properties.Name -contains "requiredDocs") {
    foreach ($doc in $config.requiredDocs) {
        if (-not (Test-Path -LiteralPath (Join-Path $resolvedPluginRoot $doc))) {
            throw "Required doc missing: $doc"
        }
    }
}

foreach ($script in $config.requiredScripts) {
    if (-not (Test-Path -LiteralPath (Join-Path $resolvedPluginRoot $script))) {
        throw "Required script missing: $script"
    }
}

Write-Host "Plugin config validation succeeded."
