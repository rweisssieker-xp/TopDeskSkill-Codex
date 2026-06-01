param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path,
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$Version = "0.1.3",
    [int]$FileCountLimit = 128
)

$ErrorActionPreference = "Stop"

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path
$dist = Join-Path $resolvedRoot "dist"
$stage = Join-Path $dist "marketplace-topdesk-skill-suite"
$zip = Join-Path $dist "topdesk-skill-suite-marketplace-$Version.zip"

if (-not ($resolvedPluginRoot.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase))) {
    throw "PluginRoot must be inside Root. Root=$resolvedRoot PluginRoot=$resolvedPluginRoot"
}

if (Test-Path -LiteralPath $stage) {
    $resolvedStage = (Resolve-Path -LiteralPath $stage).Path
    if (-not ($resolvedStage.StartsWith($dist, [System.StringComparison]::OrdinalIgnoreCase))) {
        throw "Refusing to remove staging directory outside dist: $resolvedStage"
    }
    Remove-Item -LiteralPath $resolvedStage -Recurse -Force
}

if (Test-Path -LiteralPath $zip) {
    Remove-Item -LiteralPath $zip -Force
}

New-Item -ItemType Directory -Force -Path $stage | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $stage ".codex-plugin") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $stage "assets") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $stage "docs") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $stage "scripts") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $stage "skills") | Out-Null

Copy-Item -LiteralPath (Join-Path $resolvedPluginRoot ".codex-plugin\plugin.json") -Destination (Join-Path $stage ".codex-plugin\plugin.json")
Copy-Item -LiteralPath (Join-Path $resolvedPluginRoot ".mcp.json") -Destination (Join-Path $stage ".mcp.json")

foreach ($file in @("README.md", "CHANGELOG.md", "LICENSE", "RELEASE_CHECKLIST.md")) {
    $source = Join-Path $resolvedPluginRoot $file
    if ($file -eq "LICENSE" -and -not (Test-Path -LiteralPath $source)) {
        $source = Join-Path $resolvedRoot "LICENSE"
    }
    if (Test-Path -LiteralPath $source) {
        Copy-Item -LiteralPath $source -Destination (Join-Path $stage $file)
    }
}

foreach ($asset in @("icon.png", "logo.png", "screenshot-overview.png", "screenshot-powerbi.png", "screenshot-ai-governance.png")) {
    Copy-Item -LiteralPath (Join-Path $resolvedPluginRoot "assets\$asset") -Destination (Join-Path $stage "assets\$asset")
}

$docs = @(
    "INSTALLATION_AND_RELEASE.md",
    "COMMERCIAL_MODEL.md",
    "DEMO_DASHBOARD_STORYBOARD.md",
    "SECURITY_PRIVACY_AI.md",
    "ONE_PAGER.md",
    "PRIVACY_POLICY.md",
    "TERMS_OF_SERVICE.md",
    "PRODUCTION_READINESS.md",
    "MARKETPLACE_SUBMISSION.md",
    "FEATURE_MATRIX.md",
    "SERVICE_INTELLIGENCE_RUNTIME.md",
    "LOCALIZATION.md",
    "DOCUMENTATION_COVERAGE.md"
)
foreach ($doc in $docs) {
    Copy-Item -LiteralPath (Join-Path $resolvedPluginRoot "docs\$doc") -Destination (Join-Path $stage "docs\$doc")
}

$scripts = @(
    "topdesk_mcp_server.py",
    "test_mcp_server.py",
    "validate_marketplace_readiness.ps1",
    "validate_plugin.ps1"
)
foreach ($script in $scripts) {
    Copy-Item -LiteralPath (Join-Path $resolvedPluginRoot "scripts\$script") -Destination (Join-Path $stage "scripts\$script")
}

$skillDirs = Get-ChildItem -LiteralPath (Join-Path $resolvedPluginRoot "skills") -Directory | Sort-Object Name
foreach ($skill in $skillDirs) {
    $target = Join-Path $stage "skills\$($skill.Name)"
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    Copy-Item -LiteralPath (Join-Path $skill.FullName "SKILL.md") -Destination (Join-Path $target "SKILL.md")
}

$skillFiles = @(
    "topdesk-ai-adoption-ledger\scripts\build_ai_adoption_ledger.py",
    "topdesk-api-test-lab\scripts\smoke_topdesk_api.py",
    "topdesk-automation-sandbox\scripts\review_automation_risk.py",
    "topdesk-compliance-pii\scripts\scan_pii_catalog.py",
    "topdesk-decision-findings\scripts\build_decision_findings.py",
    "topdesk-digital-twin-light\scripts\run_digital_twin_light.py",
    "topdesk-executive-narrative\scripts\build_executive_narrative.py",
    "topdesk-odata\scripts\generate_data_quality_findings.py",
    "topdesk-odata\scripts\generate_field_catalog.py",
    "topdesk-odata\scripts\parse_odata_metadata.py",
    "topdesk-odata\scripts\profile_topdesk_export.py",
    "topdesk-powerbi-dax\scripts\new_dax_measure_pack.py",
    "topdesk-powerbi\scripts\build_demo_powerbi_report_pack.py",
    "topdesk-powerbi\scripts\build_topdesk_pbir_report.py",
    "topdesk-process-debt\scripts\analyze_process_debt.py",
    "topdesk-readiness-scoring\scripts\score_readiness.py",
    "topdesk-service-intelligence-runtime\assets\runtime-config.example.json",
    "topdesk-service-intelligence-runtime\scripts\Register-ServiceIntelligenceSchedule.ps1",
    "topdesk-service-intelligence-runtime\scripts\run_service_intelligence.py",
    "topdesk-service-intelligence-runtime\scripts\service_intelligence_server.py",
    "topdesk-service-intelligence-runtime\scripts\topdesk_live_connector.py",
    "topdesk-service-intelligence-runtime\scripts\topdesk_secret_store.py",
    "topdesk-sla-optimizer\scripts\analyze_sla_backlog.py",
    "topdesk-tenant-drift\scripts\compare_tenant_drift.py",
    "topdesk-tenant-mapping\scripts\profile_topdesk_rest.py"
)
foreach ($relative in $skillFiles) {
    $source = Join-Path (Join-Path $resolvedPluginRoot "skills") $relative
    $target = Join-Path (Join-Path $stage "skills") $relative
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
    Copy-Item -LiteralPath $source -Destination $target
}

$fileCount = @(Get-ChildItem -LiteralPath $stage -Recurse -File).Count
if ($fileCount -gt $FileCountLimit) {
    throw "Marketplace package has $fileCount files, above limit $FileCountLimit"
}

Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $zip -Force

if (-not (Test-Path -LiteralPath $zip)) {
    throw "Marketplace package was not created: $zip"
}

Write-Host "Wrote $zip with $fileCount files"
