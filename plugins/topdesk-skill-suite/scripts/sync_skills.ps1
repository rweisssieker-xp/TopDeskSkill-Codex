param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path,
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path
$skillsTarget = Join-Path $resolvedPluginRoot "skills"

if (-not ($resolvedPluginRoot.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase))) {
    throw "PluginRoot must be inside Root. Root=$resolvedRoot PluginRoot=$resolvedPluginRoot"
}

if (-not (Test-Path -LiteralPath (Join-Path $resolvedPluginRoot ".codex-plugin\plugin.json"))) {
    throw "Plugin manifest not found under PluginRoot: $resolvedPluginRoot"
}

if (Test-Path -LiteralPath $skillsTarget) {
    $resolvedSkillsTarget = (Resolve-Path -LiteralPath $skillsTarget).Path
    if (-not ($resolvedSkillsTarget.StartsWith($resolvedPluginRoot, [System.StringComparison]::OrdinalIgnoreCase))) {
        throw "Refusing to remove skills target outside plugin root: $resolvedSkillsTarget"
    }
    Remove-Item -LiteralPath $resolvedSkillsTarget -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $skillsTarget | Out-Null

$skillDirs = Get-ChildItem -LiteralPath $resolvedRoot -Directory -Filter "topdesk-*" | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}

foreach ($skill in $skillDirs) {
    $destination = Join-Path $skillsTarget $skill.Name
    New-Item -ItemType Directory -Force -Path $destination | Out-Null
    Copy-Item -Path (Join-Path $skill.FullName "*") -Destination $destination -Recurse -Force
}

Get-ChildItem -LiteralPath $skillsTarget -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force

Write-Host "Synced $($skillDirs.Count) skills to $skillsTarget"

