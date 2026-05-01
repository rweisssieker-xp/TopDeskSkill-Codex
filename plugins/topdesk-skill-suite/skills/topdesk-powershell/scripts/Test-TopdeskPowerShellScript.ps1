param(
    [Parameter(Mandatory = $true)]
    [string]$Path
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Path)) {
    throw "Script not found: $Path"
}

$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path -LiteralPath $Path).Path, [ref]$tokens, [ref]$errors)
if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error "$($_.Extent.Text): $($_.Message)" }
    exit 1
}

$content = Get-Content -Raw -LiteralPath $Path
$required = @(
    '$ErrorActionPreference = "Stop"',
    'Set-StrictMode -Version Latest'
)

foreach ($needle in $required) {
    if ($content -notlike "*$needle*") {
        throw "Recommended pattern missing: $needle"
    }
}

Write-Host "PowerShell script validation succeeded: $Path"

