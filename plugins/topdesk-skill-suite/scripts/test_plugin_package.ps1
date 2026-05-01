param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path,
    [string]$Version = "0.1.0"
)

$ErrorActionPreference = "Stop"

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$dist = Join-Path $resolvedRoot "dist"
$zip = Join-Path $dist "topdesk-skill-suite-plugin-$Version.zip"
$extractRoot = Join-Path $dist "package-test-topdesk-skill-suite"

if (-not (Test-Path -LiteralPath $zip)) {
    throw "Package not found: $zip"
}

if (Test-Path -LiteralPath $extractRoot) {
    $resolvedExtractRoot = (Resolve-Path -LiteralPath $extractRoot).Path
    if (-not ($resolvedExtractRoot.StartsWith($dist, [System.StringComparison]::OrdinalIgnoreCase))) {
        throw "Refusing to remove extract directory outside dist: $resolvedExtractRoot"
    }
    Remove-Item -LiteralPath $resolvedExtractRoot -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $extractRoot | Out-Null
Expand-Archive -LiteralPath $zip -DestinationPath $extractRoot -Force

$manifest = Join-Path $extractRoot ".codex-plugin\plugin.json"
$skillsRoot = Join-Path $extractRoot "skills"

if (-not (Test-Path -LiteralPath $manifest)) {
    throw "Extracted package is missing .codex-plugin/plugin.json"
}

python -m json.tool "$manifest" | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Extracted plugin manifest is invalid JSON"
}

$skillCount = @(Get-ChildItem -LiteralPath $skillsRoot -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}).Count

if ($skillCount -lt 1) {
    throw "Extracted package has no bundled skills"
}

foreach ($asset in @("assets\icon.png", "assets\logo.png", "assets\screenshot-overview.png")) {
    if (-not (Test-Path -LiteralPath (Join-Path $extractRoot $asset))) {
        throw "Extracted package is missing $asset"
    }
}

Write-Host "Package test passed for $zip with $skillCount skills"

