param(
    [string]$Root = "C:\tmp\topdeskskill"
)

$ErrorActionPreference = "Stop"
$failed = $false

$skillDirs = Get-ChildItem -LiteralPath $Root -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}

foreach ($skill in $skillDirs) {
    $skillPath = Join-Path $skill.FullName "SKILL.md"
    $content = Get-Content -Raw -LiteralPath $skillPath
    $matches = [regex]::Matches($content, '`((references|scripts|assets)/[^`]+)`')

    foreach ($match in $matches) {
        $relative = $match.Groups[1].Value -replace '/', '\'
        if ($relative -match '[\*\?]') {
            $pattern = Join-Path $skill.FullName $relative
            $found = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
            if (-not $found) {
                $failed = $true
                Write-Host "Missing glob reference in $($skill.Name): $($match.Groups[1].Value)" -ForegroundColor Red
            }
            continue
        }
        $target = Join-Path $skill.FullName $relative
        if (-not (Test-Path -LiteralPath $target)) {
            $failed = $true
            Write-Host "Missing reference in $($skill.Name): $($match.Groups[1].Value)" -ForegroundColor Red
        }
    }
}

$badPathMatches = Get-ChildItem -LiteralPath $Root -Recurse -File |
    Where-Object { $_.Name -ne "check_skill_references.ps1" } |
    Select-String -Pattern "topdeskill" -CaseSensitive -ErrorAction SilentlyContinue
if ($badPathMatches) {
    $failed = $true
    $badPathMatches | ForEach-Object {
        Write-Host "Suspicious path typo: $($_.Path):$($_.LineNumber): $($_.Line)" -ForegroundColor Red
    }
}

if ($failed) {
    exit 1
}

Write-Host "All referenced skill files exist and no topdeskill typo was found." -ForegroundColor Green
