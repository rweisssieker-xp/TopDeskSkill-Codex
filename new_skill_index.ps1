param(
    [string]$Manifest = "C:\tmp\topdeskskill\skills.manifest.json",
    [string]$OutFile = "C:\tmp\topdeskskill\SKILL_INDEX.generated.md"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Manifest)) {
    throw "Manifest not found: $Manifest"
}

$data = Get-Content -Raw -LiteralPath $Manifest | ConvertFrom-Json

$lines = @(
    "# Generated TOPdesk Skill Index",
    "",
    "Generated: $($data.generated_at)",
    "",
    "| Skill | Folder | Description |",
    "| --- | --- | --- |"
)

foreach ($skill in $data.skills) {
    $description = $skill.description -replace '\|', '/'
    $lines += "| `$($skill.name)` | `$($skill.folder)` | $description |"
}

Set-Content -LiteralPath $OutFile -Value ($lines -join "`r`n") -Encoding UTF8
Write-Host "Wrote $OutFile"
