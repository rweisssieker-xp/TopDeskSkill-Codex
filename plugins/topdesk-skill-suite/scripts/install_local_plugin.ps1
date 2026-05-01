param(
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$HomeRoot = $HOME
)

$ErrorActionPreference = "Stop"

$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path
$targetParent = Join-Path $HomeRoot "plugins"
$target = Join-Path $targetParent "topdesk-skill-suite"
$marketplacePath = Join-Path $HomeRoot ".agents\plugins\marketplace.json"

if (-not (Test-Path -LiteralPath (Join-Path $resolvedPluginRoot ".codex-plugin\plugin.json"))) {
    throw "Plugin manifest not found: $resolvedPluginRoot"
}

New-Item -ItemType Directory -Force -Path $targetParent | Out-Null

if (Test-Path -LiteralPath $target) {
    $resolvedTarget = (Resolve-Path -LiteralPath $target).Path
    if (-not ($resolvedTarget.StartsWith((Resolve-Path -LiteralPath $targetParent).Path, [System.StringComparison]::OrdinalIgnoreCase))) {
        throw "Refusing to replace target outside plugin parent: $resolvedTarget"
    }
    Remove-Item -LiteralPath $resolvedTarget -Recurse -Force
}

Copy-Item -LiteralPath $resolvedPluginRoot -Destination $targetParent -Recurse -Force

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $marketplacePath) | Out-Null

if (Test-Path -LiteralPath $marketplacePath) {
    $marketplace = Get-Content -Raw -LiteralPath $marketplacePath | ConvertFrom-Json
} else {
    $marketplace = [pscustomobject]@{
        name = "topdesk-local"
        interface = [pscustomobject]@{ displayName = "TOPdesk Local Plugins" }
        plugins = @()
    }
}

$entry = [pscustomobject]@{
    name = "topdesk-skill-suite"
    source = [pscustomobject]@{
        source = "local"
        path = "./plugins/topdesk-skill-suite"
    }
    policy = [pscustomobject]@{
        installation = "AVAILABLE"
        authentication = "ON_INSTALL"
    }
    category = "Productivity"
}

$plugins = @($marketplace.plugins | Where-Object { $_.name -ne "topdesk-skill-suite" })
$plugins += $entry
$marketplace.plugins = $plugins
$marketplace | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $marketplacePath -Encoding UTF8

Write-Host "Installed plugin to $target"
Write-Host "Updated marketplace $marketplacePath"

