param(
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$OutFile = ""
)

$ErrorActionPreference = "Stop"

function Get-FrontmatterValue {
    param(
        [string]$Content,
        [string]$Key
    )
    $match = [regex]::Match($Content, "(?m)^$Key\s*:\s*(.+)$")
    if ($match.Success) {
        return $match.Groups[1].Value.Trim().Trim('"')
    }
    return ""
}

$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path
$skillsRoot = Join-Path $resolvedPluginRoot "skills"

if ([string]::IsNullOrWhiteSpace($OutFile)) {
    $OutFile = Join-Path $resolvedPluginRoot "plugin-skills.manifest.json"
}

if (-not (Test-Path -LiteralPath $skillsRoot)) {
    throw "Plugin skills directory not found: $skillsRoot"
}

$skills = @()

Get-ChildItem -LiteralPath $skillsRoot -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
} | Sort-Object Name | ForEach-Object {
    $skillMd = Join-Path $_.FullName "SKILL.md"
    $content = Get-Content -Raw -LiteralPath $skillMd

    $refs = @()
    $scripts = @()
    $assets = @()

    $refDir = Join-Path $_.FullName "references"
    if (Test-Path -LiteralPath $refDir) {
        $refs = @(Get-ChildItem -LiteralPath $refDir -File | Sort-Object Name | ForEach-Object { "references/$($_.Name)" })
    }

    $scriptDir = Join-Path $_.FullName "scripts"
    if (Test-Path -LiteralPath $scriptDir) {
        $scripts = @(Get-ChildItem -LiteralPath $scriptDir -File | Sort-Object Name | ForEach-Object { "scripts/$($_.Name)" })
    }

    $assetDir = Join-Path $_.FullName "assets"
    if (Test-Path -LiteralPath $assetDir) {
        $assets = @(Get-ChildItem -LiteralPath $assetDir -File | Sort-Object Name | ForEach-Object { "assets/$($_.Name)" })
    }

    $skills += [ordered]@{
        name = Get-FrontmatterValue -Content $content -Key "name"
        folder = $_.Name
        description = Get-FrontmatterValue -Content $content -Key "description"
        references = $refs
        scripts = $scripts
        assets = $assets
    }
}

$manifest = [ordered]@{
    generated_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK")
    plugin = "topdesk-skill-suite"
    skill_count = $skills.Count
    skills = $skills
}

$json = $manifest | ConvertTo-Json -Depth 8
[System.IO.File]::WriteAllText($OutFile, ($json + [Environment]::NewLine), [System.Text.UTF8Encoding]::new($false))
Write-Host "Wrote $OutFile"
