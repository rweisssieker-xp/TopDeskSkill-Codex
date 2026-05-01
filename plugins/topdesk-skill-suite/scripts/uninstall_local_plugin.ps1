param(
    [string]$HomeRoot = $HOME
)

$ErrorActionPreference = "Stop"

$targetParent = Join-Path $HomeRoot "plugins"
$target = Join-Path $targetParent "topdesk-skill-suite"
$marketplacePath = Join-Path $HomeRoot ".agents\plugins\marketplace.json"

if (Test-Path -LiteralPath $target) {
    $resolvedTarget = (Resolve-Path -LiteralPath $target).Path
    if (-not ($resolvedTarget.StartsWith((Resolve-Path -LiteralPath $targetParent).Path, [System.StringComparison]::OrdinalIgnoreCase))) {
        throw "Refusing to remove target outside plugin parent: $resolvedTarget"
    }
    Remove-Item -LiteralPath $resolvedTarget -Recurse -Force
    Write-Host "Removed plugin from $target"
}

if (Test-Path -LiteralPath $marketplacePath) {
    $marketplace = Get-Content -Raw -LiteralPath $marketplacePath | ConvertFrom-Json
    $marketplace.plugins = @($marketplace.plugins | Where-Object { $_.name -ne "topdesk-skill-suite" })
    $marketplace | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $marketplacePath -Encoding UTF8
    Write-Host "Removed marketplace entry from $marketplacePath"
}

