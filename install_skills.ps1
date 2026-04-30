param(
    [string]$SourceRoot = "C:\tmp\topdeskskill",
    [string]$TargetRoot = "$env:USERPROFILE\.codex\skills",
    [string[]]$SkillNames = @(),
    [switch]$WhatIfOnly
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $SourceRoot)) {
    throw "Source root not found: $SourceRoot"
}

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

$skills = Get-ChildItem -LiteralPath $SourceRoot -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}

if ($SkillNames.Count -gt 0) {
    $wanted = @{}
    $SkillNames | ForEach-Object { $wanted[$_] = $true }
    $skills = $skills | Where-Object { $wanted.ContainsKey($_.Name) }
}

if ($skills.Count -eq 0) {
    throw "No matching skills found."
}

$backupRoot = Join-Path $TargetRoot ("_backup_topdesk_" + (Get-Date -Format "yyyyMMdd_HHmmss"))

foreach ($skill in $skills) {
    $target = Join-Path $TargetRoot $skill.Name
    Write-Host "Installing $($skill.Name) -> $target"

    if ($WhatIfOnly) {
        continue
    }

    if (Test-Path -LiteralPath $target) {
        New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
        $backupTarget = Join-Path $backupRoot $skill.Name
        Write-Host "Backing up existing skill to $backupTarget"
        Copy-Item -LiteralPath $target -Destination $backupTarget -Recurse -Force
        Remove-Item -LiteralPath $target -Recurse -Force
    }

    Copy-Item -LiteralPath $skill.FullName -Destination $target -Recurse -Force
}

Write-Host "Installed $($skills.Count) skill(s)."
if (-not $WhatIfOnly -and (Test-Path -LiteralPath $backupRoot)) {
    Write-Host "Backups written to $backupRoot"
}
