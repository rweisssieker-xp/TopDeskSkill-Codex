param(
    [string]$Version = "0.1.0",
    [string]$Tag = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Tag)) {
    $Tag = "v$Version"
}

git status --short
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if (git tag --list $Tag) {
    Write-Host "Tag already exists: $Tag"
} else {
    git tag -a $Tag -m "Release $Tag"
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
    Write-Host "Created local tag $Tag"
}

Write-Host "Review changes, then push explicitly when ready:"
Write-Host "git push origin HEAD"
Write-Host "git push origin $Tag"

