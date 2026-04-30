param(
    [string]$Manifest = "C:\tmp\topdeskskill\skills.manifest.json",
    [string]$OutFile = "C:\tmp\topdeskskill\SKILL_INVENTORY_REPORT.md"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Manifest)) {
    throw "Manifest not found: $Manifest"
}

$data = Get-Content -Raw -LiteralPath $Manifest | ConvertFrom-Json

$lines = @(
    "# Skill Inventory Report",
    "",
    "Generated: $($data.generated_at)",
    "",
    "Skill count: $($data.skill_count)",
    "",
    "| Skill | References | Scripts | Assets |",
    "| --- | ---: | ---: | ---: |"
)

foreach ($skill in $data.skills) {
    $lines += "| ``$($skill.name)`` | $($skill.references.Count) | $($skill.scripts.Count) | $($skill.assets.Count) |"
}

$lines += @(
    "",
    "## Skills",
    ""
)

foreach ($skill in $data.skills) {
    $lines += "### ``$($skill.name)``"
    $lines += ""
    $lines += $skill.description
    $lines += ""

    if ($skill.references.Count -gt 0) {
        $lines += "References:"
        foreach ($ref in $skill.references) {
            $lines += "- ``$ref``"
        }
        $lines += ""
    }

    if ($skill.scripts.Count -gt 0) {
        $lines += "Scripts:"
        foreach ($script in $skill.scripts) {
            $lines += "- ``$script``"
        }
        $lines += ""
    }

    if ($skill.assets.Count -gt 0) {
        $lines += "Assets:"
        foreach ($asset in $skill.assets) {
            $lines += "- ``$asset``"
        }
        $lines += ""
    }
}

Set-Content -LiteralPath $OutFile -Value ($lines -join "`r`n") -Encoding UTF8
Write-Host "Wrote $OutFile"
