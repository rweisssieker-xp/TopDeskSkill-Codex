param(
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [switch]$CheckExternalUrls
)

$ErrorActionPreference = "Stop"

$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path
$manifestPath = Join-Path $resolvedPluginRoot ".codex-plugin\plugin.json"
$configPath = Join-Path $resolvedPluginRoot "plugin.config.json"
$submissionDoc = Join-Path $resolvedPluginRoot "docs\MARKETPLACE_SUBMISSION.md"
$readinessDoc = Join-Path $resolvedPluginRoot "docs\PRODUCTION_READINESS.md"

if (-not (Test-Path -LiteralPath $manifestPath)) {
    throw "Plugin manifest not found: $manifestPath"
}

if (-not (Test-Path -LiteralPath $configPath)) {
    throw "Plugin config not found: $configPath"
}

if (-not (Test-Path -LiteralPath $submissionDoc)) {
    throw "Marketplace submission guide missing: docs/MARKETPLACE_SUBMISSION.md"
}

if (-not (Test-Path -LiteralPath $readinessDoc)) {
    throw "Production readiness guide missing: docs/PRODUCTION_READINESS.md"
}

$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
$config = Get-Content -Raw -LiteralPath $configPath | ConvertFrom-Json

$requiredTextFields = @(
    @{ Name = "name"; Value = $manifest.name },
    @{ Name = "version"; Value = $manifest.version },
    @{ Name = "description"; Value = $manifest.description },
    @{ Name = "license"; Value = $manifest.license },
    @{ Name = "homepage"; Value = $manifest.homepage },
    @{ Name = "repository"; Value = $manifest.repository },
    @{ Name = "interface.displayName"; Value = $manifest.interface.displayName },
    @{ Name = "interface.shortDescription"; Value = $manifest.interface.shortDescription },
    @{ Name = "interface.longDescription"; Value = $manifest.interface.longDescription },
    @{ Name = "interface.developerName"; Value = $manifest.interface.developerName },
    @{ Name = "interface.category"; Value = $manifest.interface.category },
    @{ Name = "interface.websiteURL"; Value = $manifest.interface.websiteURL },
    @{ Name = "interface.privacyPolicyURL"; Value = $manifest.interface.privacyPolicyURL },
    @{ Name = "interface.termsOfServiceURL"; Value = $manifest.interface.termsOfServiceURL }
)

foreach ($field in $requiredTextFields) {
    if ([string]::IsNullOrWhiteSpace([string]$field.Value)) {
        throw "Required marketplace field is empty: $($field.Name)"
    }
}

foreach ($urlField in @("homepage", "repository")) {
    $url = [string]$manifest.$urlField
    if (-not $url.StartsWith("https://")) {
        throw "Marketplace URL must use https: $urlField"
    }
}

foreach ($urlField in @("websiteURL", "privacyPolicyURL", "termsOfServiceURL")) {
    $url = [string]$manifest.interface.$urlField
    if (-not $url.StartsWith("https://")) {
        throw "Marketplace interface URL must use https: $urlField"
    }
}

if ($CheckExternalUrls) {
    $urls = @(
        [string]$manifest.homepage,
        [string]$manifest.repository,
        [string]$manifest.interface.websiteURL,
        [string]$manifest.interface.privacyPolicyURL,
        [string]$manifest.interface.termsOfServiceURL
    ) | Select-Object -Unique

    foreach ($url in $urls) {
        try {
            $response = Invoke-WebRequest -Uri $url -Method Head -UseBasicParsing -TimeoutSec 20
            if ([int]$response.StatusCode -ge 400) {
                throw "HTTP $($response.StatusCode)"
            }
        } catch {
            throw "External marketplace URL is not reachable: $url ($($_.Exception.Message))"
        }
    }
}

if (@($manifest.interface.screenshots).Count -lt 3) {
    throw "At least three marketplace screenshots are expected."
}

foreach ($asset in $config.requiredAssets) {
    $assetPath = Join-Path $resolvedPluginRoot $asset
    if (-not (Test-Path -LiteralPath $assetPath)) {
        throw "Required marketplace asset missing: $asset"
    }

    $length = (Get-Item -LiteralPath $assetPath).Length
    if ($length -lt 1024) {
        throw "Marketplace asset appears too small or empty: $asset"
    }
}

$submissionText = Get-Content -Raw -LiteralPath $submissionDoc
foreach ($requiredPhrase in @("Screenshot Policy", "Submission Evidence", "Localized prompt examples")) {
    if ($submissionText -notmatch [regex]::Escape($requiredPhrase)) {
        throw "Marketplace submission guide missing section: $requiredPhrase"
    }
}

$readinessText = Get-Content -Raw -LiteralPath $readinessDoc
foreach ($requiredPhrase in @("Tenant Access", "Real Data Mapping", "Privacy And AI", "Operations", "Commercial Boundary")) {
    if ($readinessText -notmatch [regex]::Escape($requiredPhrase)) {
        throw "Production readiness guide missing section: $requiredPhrase"
    }
}

Write-Host "Marketplace readiness validation succeeded."
