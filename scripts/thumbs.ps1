# Gera miniaturas JPEG leves das imagens da v0.1 para inspecao rapida.
# Uso: powershell -File scripts/thumbs.ps1 -Nomes image11,image9 -Largura 300
param(
    [string[]]$Nomes,
    [int]$Largura = 300,
    [string]$Origem = "assets\imagens-v01",
    [string]$Destino = "$env:TEMP\eg_thumbs"
)

Add-Type -AssemblyName System.Drawing
if (-not (Test-Path $Destino)) { New-Item -ItemType Directory -Path $Destino | Out-Null }

$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$params = New-Object System.Drawing.Imaging.EncoderParameters 1
$params.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality, 50)

foreach ($n in $Nomes) {
    $src = Join-Path $Origem "$n.png"
    if (-not (Test-Path $src)) { "FALTA: $src"; continue }
    $img = [System.Drawing.Image]::FromFile((Resolve-Path $src))
    $h = [int]($img.Height * ($Largura / $img.Width))
    $bmp = New-Object System.Drawing.Bitmap $Largura, $h
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.Clear([System.Drawing.Color]::White)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.DrawImage($img, 0, 0, $Largura, $h)
    $out = Join-Path $Destino "$n.jpg"
    $bmp.Save($out, $codec, $params)
    $g.Dispose(); $bmp.Dispose(); $img.Dispose()
    "{0} -> {1} KB" -f $out, [math]::Round((Get-Item $out).Length / 1KB, 0)
}
