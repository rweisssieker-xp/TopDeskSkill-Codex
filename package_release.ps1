param(
    [string]$Root = "C:\tmp\topdeskskill",
    [string]$Version = "v0.1.0"
)

$ErrorActionPreference = "Stop"

$dist = Join-Path $Root "dist"
$staging = Join-Path $dist "topdesk-skills-$Version"
$zip = Join-Path $dist "topdesk-skills-$Version.zip"

if (Test-Path -LiteralPath $staging) {
    Remove-Item -LiteralPath $staging -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $staging | Out-Null

$excludeDirs = @(".git", "dist")
$items = Get-ChildItem -LiteralPath $Root -Force | Where-Object {
    $excludeDirs -notcontains $_.Name
}

foreach ($item in $items) {
    Copy-Item -LiteralPath $item.FullName -Destination (Join-Path $staging $item.Name) -Recurse -Force
}

Get-ChildItem -LiteralPath $staging -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -LiteralPath $staging -Recurse -File -Include "*.pyc","*.tmp","*.bak","*.log" | Remove-Item -Force

if (Test-Path -LiteralPath $zip) {
    Remove-Item -LiteralPath $zip -Force
}

Compress-Archive -LiteralPath (Join-Path $staging "*") -DestinationPath $zip -Force
Write-Host "Wrote $zip"
