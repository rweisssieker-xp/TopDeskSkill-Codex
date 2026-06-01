param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path,
    [string]$Version = "0.1.3",
    [int]$FileCountLimit = 128
)

$ErrorActionPreference = "Stop"

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$dist = Join-Path $resolvedRoot "dist"
$zip = Join-Path $dist "topdesk-skill-suite-marketplace-$Version.zip"
$extractRoot = Join-Path $dist "marketplace-package-test-topdesk-skill-suite"

if (-not (Test-Path -LiteralPath $zip)) {
    throw "Marketplace package not found: $zip"
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

$fileCount = @(Get-ChildItem -LiteralPath $extractRoot -Recurse -File).Count
if ($fileCount -gt $FileCountLimit) {
    throw "Extracted marketplace package has $fileCount files, above limit $FileCountLimit"
}

$manifest = Join-Path $extractRoot ".codex-plugin\plugin.json"
if (-not (Test-Path -LiteralPath $manifest)) {
    throw "Marketplace package is missing .codex-plugin/plugin.json at artifact root"
}

$manifestJson = Get-Content -LiteralPath $manifest -Raw | ConvertFrom-Json
if (-not ($manifestJson.author.email -match "^[^@\s]+@[^@\s]+\.[^@\s]+$")) {
    throw "Manifest author.email is not valid: $($manifestJson.author.email)"
}

$skillCount = @(Get-ChildItem -LiteralPath (Join-Path $extractRoot "skills") -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}).Count
if ($skillCount -ne 48) {
    throw "Expected 48 marketplace skill entry points, found $skillCount"
}

foreach ($required in @(
    "docs\FEATURE_MATRIX.md",
    "docs\MARKETPLACE_SUBMISSION.md",
    "docs\PRIVACY_POLICY.md",
    "docs\TERMS_OF_SERVICE.md",
    "assets\icon.png",
    "assets\logo.png",
    "scripts\topdesk_mcp_server.py",
    "skills\topdesk-service-intelligence-runtime\scripts\run_service_intelligence.py",
    "skills\topdesk-service-intelligence-runtime\scripts\service_intelligence_server.py",
    "skills\topdesk-tenant-drift\scripts\compare_tenant_drift.py",
    "skills\topdesk-process-debt\scripts\analyze_process_debt.py",
    ".mcp.json"
)) {
    if (-not (Test-Path -LiteralPath (Join-Path $extractRoot $required))) {
        throw "Marketplace package is missing $required"
    }
}

Write-Host "Marketplace package test passed for $zip with $fileCount files and $skillCount skills"
