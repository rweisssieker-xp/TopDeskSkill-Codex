param(
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$Validator = "C:\Users\weiss\.codex\skills\.system\skill-creator\scripts\quick_validate.py"
)

$ErrorActionPreference = "Stop"
$failed = $false

$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path
$manifest = Join-Path $resolvedPluginRoot ".codex-plugin\plugin.json"
$skillsRoot = Join-Path $resolvedPluginRoot "skills"

if (-not (Test-Path -LiteralPath $manifest)) {
    throw "Plugin manifest not found: $manifest"
}

if (-not (Test-Path -LiteralPath $skillsRoot)) {
    throw "Plugin skills directory not found: $skillsRoot"
}

Write-Host "Checking plugin manifest JSON..."
python -m json.tool "$manifest" | Out-Null
if ($LASTEXITCODE -ne 0) { $failed = $true }

if (-not (Test-Path -LiteralPath $Validator)) {
    throw "Skill validator not found: $Validator"
}

$skillDirs = Get-ChildItem -LiteralPath $skillsRoot -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}

Write-Host "Validating $($skillDirs.Count) bundled skills..."
foreach ($skill in $skillDirs) {
    Write-Host "==> $($skill.Name)"
    & python $Validator $skill.FullName
    if ($LASTEXITCODE -ne 0) { $failed = $true }
}

Write-Host "Compiling bundled Python scripts..."
$pythonFiles = Get-ChildItem -LiteralPath $skillsRoot -Recurse -File -Filter *.py
if ($pythonFiles.Count -gt 0) {
    & python -m py_compile @($pythonFiles.FullName)
    if ($LASTEXITCODE -ne 0) { $failed = $true }
}

$pycacheDirs = Get-ChildItem -LiteralPath $skillsRoot -Recurse -Directory -Filter __pycache__ -ErrorAction SilentlyContinue
if ($pycacheDirs) {
    $pycacheDirs | Remove-Item -Recurse -Force
}

if ($failed) {
    Write-Host "Plugin validation failed." -ForegroundColor Red
    exit 1
}

Write-Host "Plugin validation succeeded." -ForegroundColor Green

