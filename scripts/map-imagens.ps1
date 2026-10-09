# Mapeia cada imagem do .docx v0.1 para o texto que a cerca, em ordem de documento.
# Uso: pwsh -File scripts/map-imagens.ps1 -Extraido <pasta do docx expandido>
param(
    [string]$Extraido = "C:\Users\marco\AppData\Local\Temp\eg_docx\x"
)

$rels = [xml](Get-Content (Join-Path $Extraido "word\_rels\document.xml.rels") -Raw)
$map = @{}
foreach ($r in $rels.Relationships.Relationship) {
    if ($r.Target -like "media/*") { $map[$r.Id] = ($r.Target -replace 'media/', '') }
}

$doc = Get-Content (Join-Path $Extraido "word\document.xml") -Raw
$rx = [regex]'(?:<w:t[^>]*>(?<t>[^<]*)</w:t>)|(?:r:embed="(?<id>rId\d+)")'

$itens = New-Object System.Collections.Generic.List[object]
$buf = ""
foreach ($m in $rx.Matches($doc)) {
    if ($m.Groups['t'].Success) {
        $buf = $buf + $m.Groups['t'].Value
    }
    else {
        $itens.Add([pscustomobject]@{ Img = $map[$m.Groups['id'].Value]; Antes = $buf })
        $buf = ""
    }
}

for ($i = 0; $i -lt $itens.Count; $i++) {
    $antes = $itens[$i].Antes
    if ($antes.Length -gt 110) { $antes = $antes.Substring($antes.Length - 110) }
    $depois = if ($i -lt $itens.Count - 1) { $itens[$i + 1].Antes } else { $buf }
    if ($depois.Length -gt 110) { $depois = $depois.Substring(0, 110) }
    "=== $($itens[$i].Img)"
    "   ANTES : ...$antes"
    "   DEPOIS: $depois..."
}
