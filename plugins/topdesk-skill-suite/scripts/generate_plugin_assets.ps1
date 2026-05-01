param(
    [string]$PluginRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

$resolvedPluginRoot = (Resolve-Path -LiteralPath $PluginRoot).Path
$assets = Join-Path $resolvedPluginRoot "assets"
New-Item -ItemType Directory -Force -Path $assets | Out-Null

Add-Type -AssemblyName System.Drawing

function New-Bitmap {
    param(
        [string]$Path,
        [int]$Width,
        [int]$Height,
        [scriptblock]$Draw
    )

    $bitmap = New-Object System.Drawing.Bitmap $Width, $Height
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.Clear([System.Drawing.Color]::FromArgb(15, 23, 42))
    & $Draw $graphics $Width $Height
    $bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
}

$blue = [System.Drawing.Color]::FromArgb(37, 99, 235)
$lightBlue = [System.Drawing.Color]::FromArgb(147, 197, 253)
$white = [System.Drawing.Color]::White

New-Bitmap -Path (Join-Path $assets "icon.png") -Width 512 -Height 512 -Draw {
    param($g, $w, $h)
    $g.FillRectangle((New-Object System.Drawing.SolidBrush $blue), 0, 0, $w, $h)
    $font = New-Object System.Drawing.Font "Segoe UI", 168, ([System.Drawing.FontStyle]::Bold)
    $brush = New-Object System.Drawing.SolidBrush $white
    $g.DrawString("TD", $font, $brush, 88, 140)
    $g.FillRectangle((New-Object System.Drawing.SolidBrush $lightBlue), 96, 390, 320, 34)
}

New-Bitmap -Path (Join-Path $assets "logo.png") -Width 1200 -Height 360 -Draw {
    param($g, $w, $h)
    $g.FillRectangle((New-Object System.Drawing.SolidBrush $blue), 54, 54, 220, 220)
    $fontIcon = New-Object System.Drawing.Font "Segoe UI", 80, ([System.Drawing.FontStyle]::Bold)
    $fontTitle = New-Object System.Drawing.Font "Segoe UI", 72, ([System.Drawing.FontStyle]::Bold)
    $fontSub = New-Object System.Drawing.Font "Segoe UI", 44, ([System.Drawing.FontStyle]::Regular)
    $g.DrawString("TD", $fontIcon, (New-Object System.Drawing.SolidBrush $white), 91, 113)
    $g.DrawString("TOPdesk Skill Suite", $fontTitle, (New-Object System.Drawing.SolidBrush $white), 330, 88)
    $g.DrawString("Service management, OData, Power BI, AI, migration", $fontSub, (New-Object System.Drawing.SolidBrush $lightBlue), 335, 190)
}

New-Bitmap -Path (Join-Path $assets "screenshot-overview.png") -Width 1440 -Height 900 -Draw {
    param($g, $w, $h)
    $panel = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(30, 41, 59))
    $card = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(248, 250, 252))
    $muted = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(71, 85, 105))
    $titleFont = New-Object System.Drawing.Font "Segoe UI", 46, ([System.Drawing.FontStyle]::Bold)
    $headingFont = New-Object System.Drawing.Font "Segoe UI", 26, ([System.Drawing.FontStyle]::Bold)
    $bodyFont = New-Object System.Drawing.Font "Segoe UI", 21, ([System.Drawing.FontStyle]::Regular)
    $g.FillRectangle($panel, 0, 0, $w, 150)
    $g.DrawString("TOPdesk Skill Suite", $titleFont, (New-Object System.Drawing.SolidBrush $white), 70, 42)
    $labels = @("TOPdesk Expert", "OData Mapping", "Power BI", "AI Governance", "Migration", "Testing")
    for ($i = 0; $i -lt $labels.Count; $i++) {
        $x = 70 + (($i % 3) * 430)
        $y = 220 + ([math]::Floor($i / 3) * 230)
        $g.FillRectangle($card, $x, $y, 360, 160)
        $g.DrawString($labels[$i], $headingFont, (New-Object System.Drawing.SolidBrush $blue), $x + 28, $y + 26)
        $g.DrawString("Bundled skill with references, scripts, and reusable delivery guidance.", $bodyFont, $muted, (New-Object System.Drawing.RectangleF ($x + 28), ($y + 78), 300, 70))
    }
}

Write-Host "Generated plugin PNG assets in $assets"

