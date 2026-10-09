<#
    verificar-livro-final.ps1
    Protocolo de verificação final de "Explorando Galáxias" v1.0
    (item 39 do plano de escrita, seção 12 do handoff).

    O QUE ELE FAZ
        1. Roda os quatro scripts de checagem e coleta o código de saída de
           cada um: nomenclatura, tabelas, completude e simulação de combate.
        2. Confere o .docx: existe, passa de 1 MB e é mais novo que o .md mais
           recente (se não for, o livro compilado está atrasado em relação ao
           texto e precisa de `python "build\gerar_docx.py"`).
        3. REABRE o .docx com python-docx e conta parágrafos, tabelas (mais de
           15), presença de Heading 1/2/3, tabelas vazias e imagens realmente
           embutidas.
        4. Varredura de referência cruzada: toda citação de `capítulo NN`
           aponta para um capítulo que existe, e todo termo oficial do sistema
           tem verbete no glossário. Citar subsistema que o livro não define foi
           o defeito central da v0.1.
        5. Confirma em texto que o livro é de nível 1 a 20.

    COMO USAR
        powershell -File "scripts\verificar-livro-final.ps1"

    CÓDIGO DE SAÍDA
        0 = relatório inteiro verde     1 = qualquer item reprovado

    Nunca relate "pronto" porque um script rodou sem erro: relate com este
    relatório em mãos.
#>
[CmdletBinding()]
param(
    [switch]$PularSimulacao
)

$ErrorActionPreference = 'Stop'

$RaizProjeto   = Split-Path -Parent $PSScriptRoot
$PastaLivro    = Join-Path $RaizProjeto 'livro-v1.0'
$PastaScripts  = $PSScriptRoot
$ArquivoDocx   = Join-Path $RaizProjeto 'Sistema de HSR by MC Filhos V1.2.docx'

$falhas   = New-Object System.Collections.ArrayList
$relatorio = New-Object System.Collections.ArrayList

function Add-Linha {
    param([string]$Item, [string]$Valor, [bool]$Passou)
    [void]$relatorio.Add([pscustomobject]@{
        Item      = $Item
        Resultado = $Valor
        Situacao  = if ($Passou) { 'passa' } else { 'REPROVA' }
    })
    if (-not $Passou) { [void]$falhas.Add(('{0}: {1}' -f $Item, $Valor)) }
}

Write-Host ''
Write-Host '============================================================'
Write-Host ' VERIFICAÇÃO FINAL — Explorando Galáxias v1.2'
Write-Host '============================================================'

# ---------------------------------------------------------------------------
# 1. Os quatro scripts de checagem
# ---------------------------------------------------------------------------

$scripts = @(
    @{ Nome = 'checar-nomenclatura'; Arquivo = 'checar-nomenclatura.ps1' },
    @{ Nome = 'checar-tabelas';      Arquivo = 'checar-tabelas.ps1' },
    @{ Nome = 'checar-completude';   Arquivo = 'checar-completude.ps1' }
)
if (-not $PularSimulacao) {
    $scripts += @{ Nome = 'simular-combate'; Arquivo = 'simular-combate.ps1' }
}

foreach ($script in $scripts) {
    $caminho = Join-Path $PastaScripts $script.Arquivo
    if (-not (Test-Path -LiteralPath $caminho)) {
        Add-Linha -Item $script.Nome -Valor 'script ausente' -Passou $false
        continue
    }
    Write-Host ''
    Write-Host ('>>> {0}' -f $script.Nome)
    & powershell -NoProfile -ExecutionPolicy Bypass -File $caminho | Write-Host
    $codigo = $LASTEXITCODE
    Add-Linha -Item $script.Nome -Valor ('código de saída {0}' -f $codigo) -Passou ($codigo -eq 0)
}

# ---------------------------------------------------------------------------
# 2. O .docx existe, passa de 1 MB e está em dia com os .md
# ---------------------------------------------------------------------------

Write-Host ''
Write-Host '>>> arquivo compilado'

if (-not (Test-Path -LiteralPath $ArquivoDocx)) {
    Add-Linha -Item 'docx existe' -Valor 'não encontrado' -Passou $false
} else {
    $info = Get-Item -LiteralPath $ArquivoDocx
    $mb = [math]::Round($info.Length / 1MB, 2)
    Add-Linha -Item 'docx existe' -Valor ('{0} MB' -f $mb) -Passou ($info.Length -gt 1MB)

    $mdMaisNovo = Get-ChildItem -LiteralPath $PastaLivro -Filter '*.md' -File |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
    $emDia = $info.LastWriteTime -ge $mdMaisNovo.LastWriteTime
    Add-Linha -Item 'docx em dia com os .md' `
        -Valor ('docx {0:dd/MM HH:mm} contra {1} {2:dd/MM HH:mm}' -f $info.LastWriteTime, $mdMaisNovo.Name, $mdMaisNovo.LastWriteTime) `
        -Passou $emDia

    # -----------------------------------------------------------------------
    # 3. Reabrir o .docx com python-docx
    # -----------------------------------------------------------------------
    $codigoPython = @'
# -*- coding: utf-8 -*-
# Reabre o .docx compilado e imprime as contagens do protocolo de verificacao.
import sys
from docx import Document

caminho = sys.argv[1]
doc = Document(caminho)

paragrafos = len(doc.paragraphs)
tabelas = len(doc.tables)

estilos = set()
contagem_estilos = {}
for p in doc.paragraphs:
    if p.style is not None and p.style.name:
        estilos.add(p.style.name)
        contagem_estilos[p.style.name] = contagem_estilos.get(p.style.name, 0) + 1

tabelas_vazias = 0
celulas = 0
for t in doc.tables:
    texto_total = 0
    for linha in t.rows:
        for celula in linha.cells:
            celulas += 1
            if celula.text.strip():
                texto_total += 1
    if texto_total == 0:
        tabelas_vazias += 1

# Imagens realmente embutidas: partes de imagem do pacote.
imagens = 0
for parte in doc.part.package.parts:
    tipo = str(getattr(parte, "content_type", ""))
    if tipo.startswith("image/"):
        imagens += 1

inline = len(doc.inline_shapes)

# Contagem, nao presenca: um .docx com um unico titulo nao pode passar neste teste.
n_h1 = contagem_estilos.get("Heading 1", 0)
n_h2 = contagem_estilos.get("Heading 2", 0)
n_h3 = contagem_estilos.get("Heading 3", 0)
tem_toc = any("TOC" in e or "Sumario" in e or "Sumário" in e for e in estilos)

print("PARAGRAFOS=%d" % paragrafos)
print("TABELAS=%d" % tabelas)
print("CELULAS=%d" % celulas)
print("TABELAS_VAZIAS=%d" % tabelas_vazias)
print("IMAGENS=%d" % imagens)
print("INLINE_SHAPES=%d" % inline)
print("H1=%d" % n_h1)
print("H2=%d" % n_h2)
print("H3=%d" % n_h3)
print("TOC=%s" % ("1" if tem_toc else "0"))
'@

    $arquivoPython = Join-Path $env:TEMP 'eg-inspecionar-docx.py'
    [System.IO.File]::WriteAllText($arquivoPython, $codigoPython, (New-Object System.Text.UTF8Encoding $false))

    $saida = & python $arquivoPython $ArquivoDocx 2>&1
    $codigoPy = $LASTEXITCODE
    Remove-Item -LiteralPath $arquivoPython -ErrorAction SilentlyContinue

    if ($codigoPy -ne 0) {
        Add-Linha -Item 'reabrir o docx' -Valor ('python-docx falhou: {0}' -f ($saida -join ' ')) -Passou $false
    } else {
        $dados = @{}
        foreach ($linha in $saida) {
            if ($linha -match '^([A-Z0-9_]+)=(.+)$') { $dados[$Matches[1]] = $Matches[2].Trim() }
        }

        $paragrafos     = [int]$dados['PARAGRAFOS']
        $tabelas        = [int]$dados['TABELAS']
        $celulas        = [int]$dados['CELULAS']
        $tabelasVazias  = [int]$dados['TABELAS_VAZIAS']
        $imagens        = [int]$dados['IMAGENS']
        $inlineShapes   = [int]$dados['INLINE_SHAPES']

        Add-Linha -Item 'docx: parágrafos'        -Valor ('{0}' -f $paragrafos)    -Passou ($paragrafos -gt 1000)
        Add-Linha -Item 'docx: tabelas (mais de 15)' -Valor ('{0} tabelas, {1} células' -f $tabelas, $celulas) -Passou ($tabelas -gt 15)
        Add-Linha -Item 'docx: nenhuma tabela vazia' -Valor ('{0} vazias' -f $tabelasVazias) -Passou ($tabelasVazias -eq 0)
        # Contagem minima, nao presenca: o rotulo promete quantidade, entao o teste mede
        # quantidade. Um .docx com um unico titulo de cada nivel deve REPROVAR aqui.
        $h1 = [int]$dados['H1']; $h2 = [int]$dados['H2']; $h3 = [int]$dados['H3']
        Add-Linha -Item 'docx: Heading 1/2/3 (contagem)' -Valor ('H1={0} H2={1} H3={2}' -f $h1, $h2, $h3) `
            -Passou ($h1 -ge 30 -and $h2 -ge 100 -and $h3 -ge 100)
        Add-Linha -Item 'docx: imagens embutidas' -Valor ('{0} partes de imagem, {1} inline shapes' -f $imagens, $inlineShapes) `
            -Passou ($imagens -gt 0 -and $inlineShapes -gt 0)
    }
}

# ---------------------------------------------------------------------------
# 4. Varredura de referência cruzada
# ---------------------------------------------------------------------------

Write-Host ''
Write-Host '>>> referência cruzada'

$arquivosMd = @(Get-ChildItem -LiteralPath $PastaLivro -Filter '*.md' -File | Sort-Object Name)

# 4a. `capítulo NN` aponta para capítulo que existe.
$prefixosExistentes = New-Object System.Collections.Generic.HashSet[string]
foreach ($arquivo in $arquivosMd) {
    if ($arquivo.Name -match '^(\d{2})-') { [void]$prefixosExistentes.Add($Matches[1]) }
}

$refsQuebradas = New-Object System.Collections.ArrayList
$refsTotais = 0
foreach ($arquivo in $arquivosMd) {
    $linhas = @(Get-Content -LiteralPath $arquivo.FullName -Encoding UTF8)
    for ($i = 0; $i -lt $linhas.Count; $i++) {
        foreach ($m in [regex]::Matches($linhas[$i], 'cap[íi]tulos?\s+(\d{1,2})(?:\s*(?:,|e|a)\s*(\d{1,2}))*')) {
            foreach ($numero in [regex]::Matches($m.Value, '\d{1,2}')) {
                $refsTotais++
                $prefixo = ([int]$numero.Value).ToString('00')
                if (-not $prefixosExistentes.Contains($prefixo)) {
                    [void]$refsQuebradas.Add(('{0}:{1} → capítulo {2}' -f $arquivo.Name, ($i + 1), $prefixo))
                }
            }
        }
    }
}

Add-Linha -Item 'referências a capítulo resolvem' `
    -Valor ('{0} citações, {1} quebrada(s)' -f $refsTotais, $refsQuebradas.Count) `
    -Passou ($refsQuebradas.Count -eq 0)
foreach ($ref in $refsQuebradas) { Write-Host ('  referência quebrada: {0}' -f $ref) }

# 4b. Todo termo oficial tem verbete no glossário.
$TermosOficiais = @(
    'Ação Complementar', 'Ação de Movimento', 'Ataque Básico', 'Atrasar', 'Avançar',
    'Avanço Total', 'Barreira', 'Bênção', 'Ciclo', 'Dano Contínuo', 'Dano de Quebra',
    'Distância', 'DT', 'Eficácia', 'Eficiência', 'Energia', 'Esforço', 'Esforço Total',
    'Especialização de Combate', 'Executado', 'Falhe para frente', 'Fila de Ação',
    'Memoespírito', 'Nível equivalente', 'PH', 'Propósito de Vida', 'PV', 'Quebra',
    'RD', 'Reação', 'Tenacidade', 'Teste de Ataque', 'Teste de Perícia',
    'Teste de Resistência', 'Turno', 'Velocidade'
)

# Os 6 nomes fechados dos Testes de Resistência moram DENTRO do verbete
# "Teste de Resistência" (é um termo só, com seis nomes), então para eles basta
# aparecer no corpo do glossário.
$NomesTestesResistencia = @(
    'Potência Física', 'Reflexos', 'Resistência Física', 'Resistência Mental',
    'Percepção Mental', 'Força de Vontade'
)

$arqGlossario = Join-Path $PastaLivro '30-glossario.md'
if (-not (Test-Path -LiteralPath $arqGlossario)) {
    Add-Linha -Item 'glossário cobre os termos oficiais' -Valor '30-glossario.md ausente' -Passou $false
} else {
    $linhasGlossario = @(Get-Content -LiteralPath $arqGlossario -Encoding UTF8 | Where-Object { $_ -match '^\|' })
    $semVerbete = New-Object System.Collections.ArrayList

    foreach ($termo in $TermosOficiais) {
        $padrao = '^\|\s*\*{0,2}' + [regex]::Escape($termo) + '\b'
        $achou = $false
        foreach ($linha in $linhasGlossario) {
            if ([regex]::IsMatch($linha, $padrao, 'IgnoreCase')) { $achou = $true; break }
        }
        if (-not $achou) { [void]$semVerbete.Add($termo) }
    }

    foreach ($nome in $NomesTestesResistencia) {
        $padrao = [regex]::Escape($nome)
        $achou = $false
        foreach ($linha in $linhasGlossario) {
            if ([regex]::IsMatch($linha, $padrao, 'IgnoreCase')) { $achou = $true; break }
        }
        if (-not $achou) { [void]$semVerbete.Add($nome) }
    }

    $totalTermos = $TermosOficiais.Count + $NomesTestesResistencia.Count
    Add-Linha -Item 'glossário cobre os termos oficiais' `
        -Valor ('{0} de {1} cobertos' -f ($totalTermos - $semVerbete.Count), $totalTermos) `
        -Passou ($semVerbete.Count -eq 0)
    foreach ($termo in $semVerbete) { Write-Host ('  termo sem verbete: {0}' -f $termo) }
}

# ---------------------------------------------------------------------------
# 5. A faixa 1 a 20 declarada em texto
# ---------------------------------------------------------------------------

$declaraFaixa = $false
foreach ($arquivo in $arquivosMd) {
    $texto = Get-Content -LiteralPath $arquivo.FullName -Encoding UTF8 -Raw
    if ($texto -match 'n[íi]vel\s+1\s+a[oò]?\s*20|n[íi]veis\s+1\s+a\s+20|do\s+n[íi]vel\s+1\s+ao\s+20') {
        $declaraFaixa = $true
        break
    }
}
$valorFaixa = 'não encontrada'
if ($declaraFaixa) { $valorFaixa = 'declarada' }
Add-Linha -Item 'faixa de nível 1 a 20 em texto' -Valor $valorFaixa -Passou $declaraFaixa

# ---------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------

Write-Host ''
Write-Host '============================================================'
Write-Host ' RELATÓRIO'
Write-Host '============================================================'
$relatorio | Format-Table -AutoSize | Out-String -Width 160 | Write-Host

if ($falhas.Count -eq 0) {
    Write-Host 'LIVRO VERIFICADO: todos os itens do protocolo passaram.' -ForegroundColor Green
    exit 0
}

Write-Host ('VERIFICAÇÃO REPROVADA: {0} item(ns).' -f $falhas.Count) -ForegroundColor Red
foreach ($falha in $falhas) { Write-Host ('  {0}' -f $falha) }
exit 1
