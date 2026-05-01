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

New-Bitmap -Path (Join-Path $assets "screenshot-powerbi.png") -Width 1440 -Height 900 -Draw {
    param($g, $w, $h)
    $panel = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(248, 250, 252))
    $dark = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(15, 23, 42))
    $blueBrush = New-Object System.Drawing.SolidBrush $blue
    $green = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(15, 118, 110))
    $amber = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(245, 158, 11))
    $titleFont = New-Object System.Drawing.Font "Segoe UI", 42, ([System.Drawing.FontStyle]::Bold)
    $kpiFont = New-Object System.Drawing.Font "Segoe UI", 36, ([System.Drawing.FontStyle]::Bold)
    $bodyFont = New-Object System.Drawing.Font "Segoe UI", 20, ([System.Drawing.FontStyle]::Regular)
    $g.FillRectangle($panel, 0, 0, $w, $h)
    $g.DrawString("TOPdesk Power BI Foundation", $titleFont, $dark, 60, 44)
    $kpis = @("Created", "Closed", "Backlog", "SLA Met %")
    for ($i = 0; $i -lt $kpis.Count; $i++) {
        $x = 60 + ($i * 330)
        $g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)), $x, 130, 280, 120)
        $g.DrawString($kpis[$i], $bodyFont, $dark, $x + 24, 152)
        $g.DrawString(@("1,248", "1,197", "312", "91.4%")[$i], $kpiFont, $blueBrush, $x + 24, 184)
    }
    $g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)), 60, 300, 820, 430)
    $g.DrawString("Created vs Closed Trend", $bodyFont, $dark, 90, 325)
    for ($i = 0; $i -lt 12; $i++) {
        $x = 120 + ($i * 55)
        $g.FillRectangle($blueBrush, $x, 650 - ($i % 5) * 35, 22, 60 + ($i % 5) * 35)
        $g.FillRectangle($green, $x + 25, 650 - (($i + 2) % 5) * 30, 22, 60 + (($i + 2) % 5) * 30)
    }
    $g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)), 930, 300, 420, 430)
    $g.DrawString("SLA Risk Queue", $bodyFont, $dark, 960, 325)
    for ($i = 0; $i -lt 6; $i++) {
        $g.FillRectangle(@($amber, $blueBrush)[$i % 2], 965, 380 + ($i * 48), 300 - ($i * 25), 26)
    }
}

New-Bitmap -Path (Join-Path $assets "screenshot-ai-governance.png") -Width 1440 -Height 900 -Draw {
    param($g, $w, $h)
    $panel = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 255, 255))
    $dark = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(17, 24, 39))
    $red = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(220, 38, 38))
    $green = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(22, 163, 74))
    $amber = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(245, 158, 11))
    $titleFont = New-Object System.Drawing.Font "Segoe UI", 42, ([System.Drawing.FontStyle]::Bold)
    $bodyFont = New-Object System.Drawing.Font "Segoe UI", 21, ([System.Drawing.FontStyle]::Regular)
    $g.FillRectangle($panel, 0, 0, $w, $h)
    $g.DrawString("AI Governance Cockpit", $titleFont, $dark, 60, 44)
    $labels = @("Acceptance Rate", "Eval Pass Rate", "PII Findings", "Cost / Accepted")
    $values = @("76.2%", "94.8%", "3", "0.18")
    for ($i = 0; $i -lt $labels.Count; $i++) {
        $x = 60 + ($i * 330)
        $g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(248, 250, 252))), $x, 130, 280, 120)
        $g.DrawString($labels[$i], $bodyFont, $dark, $x + 22, 152)
        $g.DrawString($values[$i], (New-Object System.Drawing.Font "Segoe UI", 34, ([System.Drawing.FontStyle]::Bold)), @($green, $green, $red, (New-Object System.Drawing.SolidBrush $blue))[$i], $x + 22, 188)
    }
    $g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(248, 250, 252))), 60, 300, 600, 430)
    $g.DrawString("Prompt / Model Quality", $bodyFont, $dark, 90, 325)
    for ($i = 0; $i -lt 7; $i++) {
        $g.FillEllipse((New-Object System.Drawing.SolidBrush $blue), 110 + ($i * 70), 610 - ($i % 4) * 55, 24, 24)
    }
    $g.FillRectangle((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(248, 250, 252))), 720, 300, 620, 430)
    $g.DrawString("Risk Findings", $bodyFont, $dark, 750, 325)
    $risks = @("PII", "Permission", "Stale source", "Low confidence")
    for ($i = 0; $i -lt $risks.Count; $i++) {
        $g.FillRectangle(@($red, $amber, $green, (New-Object System.Drawing.SolidBrush $blue))[$i], 760, 390 + ($i * 72), 360 - ($i * 55), 34)
        $g.DrawString($risks[$i], $bodyFont, $dark, 1140, 384 + ($i * 72))
    }
}

Write-Host "Generated plugin PNG assets in $assets"
