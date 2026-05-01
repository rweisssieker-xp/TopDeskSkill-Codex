param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path,
    [string]$Version = "0.1.0",
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

