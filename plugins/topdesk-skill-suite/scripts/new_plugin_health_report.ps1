param(
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$OutFile = ""
)

$ErrorActionPreference = "Stop"

$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path
$manifestPath = Join-Path $resolvedPluginRoot ".codex-plugin\plugin.json"
$skillsRoot = Join-Path $resolvedPluginRoot "skills"

if ([string]::IsNullOrWhiteSpace($OutFile)) {
    $OutFile = Join-Path $resolvedPluginRoot "PLUGIN_HEALTH.md"
}

$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
$skillDirs = @(Get-ChildItem -LiteralPath $skillsRoot -Directory | Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md") })
$pngAssets = @(Get-ChildItem -LiteralPath (Join-Path $resolvedPluginRoot "assets") -File -Filter "*.png" -ErrorAction SilentlyContinue)
$scripts = @(Get-ChildItem -LiteralPath (Join-Path $resolvedPluginRoot "scripts") -File -Filter "*.ps1" -ErrorAction SilentlyContinue)

$missing = @()
foreach ($path in @($manifest.interface.composerIcon, $manifest.interface.logo)) {
    if (-not [string]::IsNullOrWhiteSpace($path)) {
        $local = Join-Path $resolvedPluginRoot ($path -replace "^\.\/", "")
        if (-not (Test-Path -LiteralPath $local)) {
            $missing += $path
        }
    }
}

$lines = @(
    "# Plugin Health Report",
    "",
    "Generated: $((Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK"))",
    "",
    "| Check | Result |",
    "| --- | --- |",
    "| Plugin name | $($manifest.name) |",
    "| Version | $($manifest.version) |",
    "| Bundled skills | $($skillDirs.Count) |",
    "| PowerShell scripts | $($scripts.Count) |",
    "| PNG assets | $($pngAssets.Count) |",
    "| Missing referenced assets | $(if ($missing.Count -eq 0) { "none" } else { $missing -join ", " }) |"
)

Set-Content -LiteralPath $OutFile -Value ($lines -join "`r`n") -Encoding UTF8
Write-Host "Wrote $OutFile"

