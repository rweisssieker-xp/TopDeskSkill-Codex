param(
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$Manifest = "",
    [string]$OutFile = ""
)

$ErrorActionPreference = "Stop"

$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path

if ([string]::IsNullOrWhiteSpace($Manifest)) {
    $Manifest = Join-Path $resolvedPluginRoot "plugin-skills.manifest.json"
}

if ([string]::IsNullOrWhiteSpace($OutFile)) {
    $OutFile = Join-Path $resolvedPluginRoot "PLUGIN_INVENTORY.md"
}

if (-not (Test-Path -LiteralPath $Manifest)) {
    & powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "new_plugin_manifest.ps1") -PluginRoot $resolvedPluginRoot -OutFile $Manifest
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to generate manifest: $Manifest"
    }
}

$data = Get-Content -Raw -LiteralPath $Manifest | ConvertFrom-Json

$lines = @(
    "# TOPdesk Skill Suite Plugin Inventory",
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

$lines += @("", "## Skills", "")

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

