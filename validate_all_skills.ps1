param(
    [string]$Root = "C:\tmp\topdeskskill",
    [string]$Validator = "C:\Users\weiss\.codex\skills\.system\skill-creator\scripts\quick_validate.py"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Root)) {
    throw "Root not found: $Root"
}

if (-not (Test-Path -LiteralPath $Validator)) {
    throw "Validator not found: $Validator"
}

$failed = $false
$skillDirs = Get-ChildItem -LiteralPath $Root -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}

Write-Host "Validating $($skillDirs.Count) skills..."

foreach ($skill in $skillDirs) {
    Write-Host "==> $($skill.Name)"
    & python $Validator $skill.FullName
    if ($LASTEXITCODE -ne 0) {
        $failed = $true
    }
}

Write-Host ""
Write-Host "Compiling Python scripts..."
$pythonFiles = Get-ChildItem -LiteralPath $Root -Recurse -File -Filter *.py
if ($pythonFiles.Count -gt 0) {
    & python -m py_compile @($pythonFiles.FullName)
    if ($LASTEXITCODE -ne 0) {
        $failed = $true
    }
}

Write-Host ""
Write-Host "Checking for open markers..."
$searchFiles = Get-ChildItem -LiteralPath $Root -Recurse -File | Where-Object {
    $_.FullName -match "\\topdesk-[^\\]+\\"
}
$openMarker = [string]::Concat("TO", "DO")
$markers = $searchFiles | Select-String -Pattern "$openMarker|\[$openMarker|FIXME|TBD" -CaseSensitive -ErrorAction SilentlyContinue
if ($markers) {
    $failed = $true
    $markers | ForEach-Object { Write-Host "$($_.Path):$($_.LineNumber): $($_.Line)" }
}

Write-Host ""
Write-Host "Cleaning __pycache__ directories..."
$pycacheDirs = Get-ChildItem -LiteralPath $Root -Recurse -Directory -Filter __pycache__
if ($pycacheDirs) {
    $pycacheDirs | ForEach-Object {
        Write-Host "Removing __pycache__: $($_.FullName)"
        Remove-Item -LiteralPath $_.FullName -Recurse -Force
    }
}

Write-Host ""
Write-Host "Checking skill references..."
$referenceChecker = Join-Path $Root "check_skill_references.ps1"
if (Test-Path -LiteralPath $referenceChecker) {
    & powershell -ExecutionPolicy Bypass -File $referenceChecker -Root $Root
    if ($LASTEXITCODE -ne 0) {
        $failed = $true
    }
}

if ($failed) {
    Write-Host "Validation failed." -ForegroundColor Red
    exit 1
}

Write-Host "All skills validated successfully." -ForegroundColor Green
