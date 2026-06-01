param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path,
    [string]$Version = "0.1.3",
    [string]$OutFile = ""
)

$ErrorActionPreference = "Stop"

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$dist = Join-Path $resolvedRoot "dist"
$zip = Join-Path $dist "topdesk-skill-suite-plugin-$Version.zip"

if ([string]::IsNullOrWhiteSpace($OutFile)) {
    $OutFile = Join-Path $dist "topdesk-skill-suite-plugin-$Version.sha256"
}

if (-not (Test-Path -LiteralPath $zip)) {
    throw "Package not found: $zip"
}

$hash = Get-FileHash -LiteralPath $zip -Algorithm SHA256
"$($hash.Hash.ToLowerInvariant())  $(Split-Path -Leaf $zip)" | Set-Content -LiteralPath $OutFile -Encoding ASCII
Write-Host "Wrote $OutFile"

$marketplaceZip = Join-Path $dist "topdesk-skill-suite-marketplace-$Version.zip"
if (Test-Path -LiteralPath $marketplaceZip) {
    $marketplaceOutFile = Join-Path $dist "topdesk-skill-suite-marketplace-$Version.sha256"
    $marketplaceHash = Get-FileHash -LiteralPath $marketplaceZip -Algorithm SHA256
    "$($marketplaceHash.Hash.ToLowerInvariant())  $(Split-Path -Leaf $marketplaceZip)" | Set-Content -LiteralPath $marketplaceOutFile -Encoding ASCII
    Write-Host "Wrote $marketplaceOutFile"
}
