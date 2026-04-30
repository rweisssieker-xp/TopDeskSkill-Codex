param(
    [string]$PromptFile = "C:\tmp\topdeskskill\FORWARD_TEST_PROMPTS.md",
    [string]$OutFile = "C:\tmp\topdeskskill\FORWARD_TEST_RUN.md"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $PromptFile)) {
    throw "Prompt file not found: $PromptFile"
}

$content = Get-Content -Raw -LiteralPath $PromptFile
$skillMatches = [regex]::Matches($content, '### (topdesk-[a-z0-9-]+)')

$lines = @(
    "# Forward-Test Run",
    "",
    "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "",
    "| Skill | Status | Prompt copied | Notes |",
    "| --- | --- | --- | --- |"
)

foreach ($match in $skillMatches) {
    $skill = $match.Groups[1].Value
    $lines += "| `$skill` | Not run | Yes | Run in fresh agent context and paste result summary here. |"
}

Set-Content -LiteralPath $OutFile -Value ($lines -join "`r`n") -Encoding UTF8
Write-Host "Wrote $OutFile"
