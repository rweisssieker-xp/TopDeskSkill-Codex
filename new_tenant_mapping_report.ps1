param(
    [Parameter(Mandatory = $true)]
    [string]$TenantName,

    [string]$MetadataXml,
    [string[]]$CsvExports = @(),
    [string]$OutRoot = "C:\tmp\topdeskskill\tenant-output"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$odataScripts = Join-Path $repoRoot "topdesk-odata\scripts"
$tenantSlug = ($TenantName.ToLowerInvariant() -replace '[^a-z0-9]+', '-').Trim('-')
if (-not $tenantSlug) {
    throw "TenantName must contain at least one alphanumeric character."
}

$outDir = Join-Path $OutRoot $tenantSlug
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$catalogDir = Join-Path $outDir "odata_catalog"
$profileDir = Join-Path $outDir "export_profiles"
New-Item -ItemType Directory -Force -Path $profileDir | Out-Null

$report = @(
    "# TOPdesk Tenant Mapping Report",
    "",
    "Tenant: $TenantName",
    "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "",
    "## Inputs",
    ""
)

if ($MetadataXml) {
    if (-not (Test-Path -LiteralPath $MetadataXml)) {
        throw "Metadata XML not found: $MetadataXml"
    }

    New-Item -ItemType Directory -Force -Path $catalogDir | Out-Null
    python (Join-Path $odataScripts "parse_odata_metadata.py") $MetadataXml --out $catalogDir
    python (Join-Path $odataScripts "generate_field_catalog.py") `
        --entity-sets (Join-Path $catalogDir "entity_sets.csv") `
        --properties (Join-Path $catalogDir "properties.csv") `
        --navigation (Join-Path $catalogDir "navigation_properties.csv") `
        --out (Join-Path $outDir "field_catalog.md")

    $report += "- Metadata XML: $MetadataXml"
    $report += "- Field catalog: field_catalog.md"
} else {
    $report += "- Metadata XML: not provided"
}

if ($CsvExports.Count -gt 0) {
    $report += "- CSV exports:"
    foreach ($csv in $CsvExports) {
        if (-not (Test-Path -LiteralPath $csv)) {
            throw "CSV export not found: $csv"
        }

        $name = [IO.Path]::GetFileNameWithoutExtension($csv)
        $safeName = ($name -replace '[^a-zA-Z0-9_-]+', '_')
        $csvOut = Join-Path $profileDir $safeName
        New-Item -ItemType Directory -Force -Path $csvOut | Out-Null
        python (Join-Path $odataScripts "profile_topdesk_export.py") $csv --out $csvOut
        python (Join-Path $odataScripts "generate_data_quality_findings.py") `
            (Join-Path $csvOut "column_profile.csv") `
            --out (Join-Path $csvOut "data_quality_findings.csv")
        $report += "  - $csv -> export_profiles/$safeName"
    }
} else {
    $report += "- CSV exports: not provided"
}

$report += @(
    "",
    "## Outputs",
    "",
    "- OData catalog CSVs in odata_catalog/ when metadata was provided.",
    "- Markdown field catalog in field_catalog.md when metadata was provided.",
    "- CSV export profiles and data-quality findings in export_profiles/ when exports were provided.",
    "",
    "## Next Steps",
    "",
    "1. Review field catalog business concepts and model fields.",
    "2. Confirm relationship/navigation semantics with TOPdesk admin.",
    "3. Map facts and dimensions for Power BI.",
    "4. Review data-quality findings and assign cleanup owners.",
    "5. Define tenant-specific RLS and KPI rules."
)

Set-Content -LiteralPath (Join-Path $outDir "tenant_mapping_report.md") -Value ($report -join "`r`n") -Encoding UTF8
Write-Host "Wrote tenant mapping output to $outDir"
