param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path,
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$Version = "0.1.0"
)

$ErrorActionPreference = "Stop"

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path
$dist = Join-Path $resolvedRoot "dist"
$zip = Join-Path $dist "topdesk-skill-suite-plugin-$Version.zip"

if (-not ($resolvedPluginRoot.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase))) {
    throw "PluginRoot must be inside Root. Root=$resolvedRoot PluginRoot=$resolvedPluginRoot"
}

if (-not (Test-Path -LiteralPath (Join-Path $resolvedPluginRoot ".codex-plugin\plugin.json"))) {
    throw "Plugin manifest not found under PluginRoot: $resolvedPluginRoot"
}

New-Item -ItemType Directory -Force -Path $dist | Out-Null

if (Test-Path -LiteralPath $zip) {
    Remove-Item -LiteralPath $zip -Force
}

Get-ChildItem -LiteralPath $resolvedPluginRoot -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force

$cleanupExtensions = @(".pyc", ".tmp", ".bak", ".log")
Get-ChildItem -LiteralPath $resolvedPluginRoot -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $cleanupExtensions -contains $_.Extension.ToLowerInvariant() } |
    Remove-Item -Force

Compress-Archive -Path (Join-Path $resolvedPluginRoot "*") -DestinationPath $zip -Force

if (-not (Test-Path -LiteralPath $zip)) {
    throw "Package was not created: $zip"
}

Write-Host "Wrote $zip"

