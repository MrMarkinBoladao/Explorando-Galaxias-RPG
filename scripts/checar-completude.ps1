<#
    checar-completude.ps1
    Gate dos dois invariantes de contrato do livro "Explorando Galáxias" v1.0.

    O QUE ELE CONFERE
        1. Os 31 capítulos esperados existem em `livro-v1.0/`, mais o changelog
           `00-changelog-v01-para-v10.md`.
        2. Cada um dos 9 arquivos de Caminho (`07-*` a `15-*`) tem 12 Bênçãos
           nomeadas — o invariante que fecha as 108 Bênçãos. Na v0.1, 4 Caminhos
           tinham ZERO.
        3. Nenhum marcador de pendência no livro: `TBD`, `a definir`,
           `farão juntamente`, `sujeito a mudanças`, `futuramente`,
           `provavelmente vou mudar o nome`. O marcador `ARTE PENDENTE` é aceito
           SÓ nos quatro Caminhos novos (`12-*` a `15-*`), que não têm arte
           na v0.1 (design 20.3).
        4. O bestiário tem 30 ou mais fichas nominais e 3 ou mais Bosses com
           fases declaradas.
        5. O livro declara em texto a faixa de nível 1 a 20.

    COMO USAR
        powershell -File "scripts\checar-completude.ps1"
        powershell -File "scripts\checar-completude.ps1" -Pasta "C:\outra\pasta"

    CÓDIGO DE SAÍDA
        0 = livro completo     1 = falta coisa (ou pasta vazia, o que é o
                                   comportamento correto antes da escrita)
#>
[CmdletBinding()]
param(
    # Pasta a varrer. Vazio = `livro-v1.0` na raiz do projeto.
    [string]$Pasta = ''
)

$ErrorActionPreference = 'Stop'

$RaizProjeto = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($Pasta)) {
    $Pasta = Join-Path $RaizProjeto 'livro-v1.0'
}

# Os 31 capítulos, na ordem de montagem do .docx.
$CapitulosEsperados = @(
    '00-capa-e-creditos.md',
    '01-introducao.md',
    '02-como-jogar.md',
    '03-criacao-de-personagem.md',
    '04-atributos-e-pericias.md',
    '05-racas.md',
    '06-caminhos-visao-geral.md',
    '07-caminho-destruicao.md',
    '08-caminho-inexistencia.md',
    '09-caminho-harmonia.md',
    '10-caminho-abundancia.md',
    '11-caminho-recordacao.md',
    '12-caminho-erudicao.md',
    '13-caminho-euforia.md',
    '14-caminho-caca.md',
    '15-caminho-preservacao.md',
    '16-habilidades.md',
    '17-ultimate-e-energia.md',
    '18-combate.md',
    '19-fila-de-acao-e-velocidade.md',
    '20-elementos-tenacidade-e-quebra.md',
    '21-condicoes.md',
    '22-testes-de-resistencia.md',
    '23-dano-cura-e-morte.md',
    '24-equipamentos.md',
    '25-cones-de-luz-e-reliquias.md',
    '26-progressao-e-ressonancias.md',
    '27-guia-do-mestre.md',
    '28-bestiario.md',
    '29-apendices-e-fichas.md',
    '30-glossario.md'
)

$ArquivoChangelog = '00-changelog-v01-para-v10.md'

# Marcadores de rascunho que não podem sobreviver na v1.0.
$MarcadoresPendencia = @(
    'TBD', 'a definir', 'farão juntamente', 'sujeito a mudanças',
    'futuramente', 'provavelmente vou mudar o nome'
)

Write-Host ''
Write-Host '== checar-completude =='
Write-Host ("Pasta: {0}" -f $Pasta)

$erros = New-Object System.Collections.ArrayList

if (-not (Test-Path -LiteralPath $Pasta)) {
    Write-Host ('ERRO: pasta não encontrada: {0}' -f $Pasta) -ForegroundColor Red
    exit 1
}

# ---------------------------------------------------------------------------
# 1. Os 31 capítulos + o changelog
# ---------------------------------------------------------------------------

$presentes = @{}
foreach ($arquivo in Get-ChildItem -LiteralPath $Pasta -Filter '*.md' -File) {
    $presentes[$arquivo.Name] = $arquivo.FullName
}

$ausentes = @($CapitulosEsperados | Where-Object { -not $presentes.ContainsKey($_) })
if ($ausentes.Count -gt 0) {
    [void]$erros.Add(('{0} capítulo(s) ausente(s): {1}' -f $ausentes.Count, ($ausentes -join ', ')))
} else {
    Write-Host ("Capítulos: {0} de {0} presentes." -f $CapitulosEsperados.Count)
}

if (-not $presentes.ContainsKey($ArquivoChangelog)) {
    [void]$erros.Add(('changelog ausente: {0}' -f $ArquivoChangelog))
} else {
    Write-Host 'Changelog: presente.'
}

# ---------------------------------------------------------------------------
# 2. 12 Bênçãos por Caminho (invariante das 108)
# ---------------------------------------------------------------------------

$arquivosCaminho = @(
    Get-ChildItem -LiteralPath $Pasta -Filter '*.md' -File |
        Where-Object { $_.Name -match '^(0[7-9]|1[0-5])-' } |
        Sort-Object Name
)

$totalBencaos = 0
foreach ($arquivo in $arquivosCaminho) {
    $linhas = @(Get-Content -LiteralPath $arquivo.FullName -Encoding UTF8)
    # Uma Bênção é um cabeçalho `### N. Nome`, numerado de 1 a 12.
    $nomes = @($linhas | Where-Object { $_ -match '^###\s+\d+\.\s+\S' })
    $totalBencaos += $nomes.Count
    if ($nomes.Count -lt 12) {
        [void]$erros.Add(('{0}: {1} Bênção(ãos) nomeada(s), esperado 12.' -f $arquivo.Name, $nomes.Count))
    } else {
        Write-Host ("{0}: {1} Bênçãos." -f $arquivo.Name, $nomes.Count)
    }
}

if ($arquivosCaminho.Count -ne 9 -and $arquivosCaminho.Count -gt 0) {
    [void]$erros.Add(('arquivos de Caminho encontrados: {0}, esperado 9.' -f $arquivosCaminho.Count))
}
if ($arquivosCaminho.Count -eq 9) {
    Write-Host ("Total de Bênçãos nos 9 Caminhos: {0} (contrato: 108)." -f $totalBencaos)
    if ($totalBencaos -lt 108) {
        [void]$erros.Add(('total de Bênçãos {0}, esperado 108.' -f $totalBencaos))
    }
}

# ---------------------------------------------------------------------------
# 3. Marcadores de pendência
# ---------------------------------------------------------------------------

$arquivosTodos = @(Get-ChildItem -LiteralPath $Pasta -Filter '*.md' -File | Sort-Object Name)
$ocorrenciasPendencia = 0

foreach ($arquivo in $arquivosTodos) {
    $linhas = @(Get-Content -LiteralPath $arquivo.FullName -Encoding UTF8)
    $caminhoNovo = $arquivo.Name -match '^(1[2-5])-'

    for ($i = 0; $i -lt $linhas.Count; $i++) {
        $linha = $linhas[$i]

        foreach ($marcador in $MarcadoresPendencia) {
            # O changelog, a introdução e o glossário citam os rascunhos da v0.1
            # de propósito (mesma válvula do checador de nomenclatura).
            if ($arquivo.Name -match '^(00|01|30)' ) { continue }
            if ([regex]::IsMatch($linha, '\b' + [regex]::Escape($marcador) + '\b', 'IgnoreCase')) {
                $ocorrenciasPendencia++
                [void]$erros.Add(('{0}:{1}  marcador de pendência "{2}".' -f $arquivo.Name, ($i + 1), $marcador))
            }
        }

        if ($linha -match 'ARTE PENDENTE' -and -not $caminhoNovo) {
            $ocorrenciasPendencia++
            [void]$erros.Add(('{0}:{1}  "ARTE PENDENTE" só é aceito nos Caminhos novos (12-* a 15-*).' -f $arquivo.Name, ($i + 1)))
        }
    }
}

if ($ocorrenciasPendencia -eq 0 -and $arquivosTodos.Count -gt 0) {
    Write-Host 'Pendências: nenhum marcador de rascunho fora das exceções previstas.'
}

# ---------------------------------------------------------------------------
# 4. Bestiário: 30+ fichas, 3+ Bosses com fases
# ---------------------------------------------------------------------------

$arqBestiario = Join-Path $Pasta '28-bestiario.md'
if (Test-Path -LiteralPath $arqBestiario) {
    $linhasBest = @(Get-Content -LiteralPath $arqBestiario -Encoding UTF8)

    # Cada ficha abre com a linha de tipo: *Comum · Facção · faixa X-Y*
    $fichas = @($linhasBest | Where-Object { $_ -match '^\*(Comum|Elite|Boss)\s*·' })
    $fichasBoss = @($linhasBest | Where-Object { $_ -match '^\*Boss\s*·' })
    $fases = @($linhasBest | Where-Object { $_ -match '^\*\*Fase\s*2' })

    Write-Host ("Bestiário: {0} fichas nominais, {1} Bosses, {2} com fase 2 declarada." -f `
        $fichas.Count, $fichasBoss.Count, $fases.Count)

    if ($fichas.Count -lt 30) { [void]$erros.Add(('bestiário com {0} fichas, esperado 30 ou mais.' -f $fichas.Count)) }
    if ($fases.Count -lt 3)   { [void]$erros.Add(('bestiário com {0} Bosses com fases, esperado 3 ou mais.' -f $fases.Count)) }
} else {
    [void]$erros.Add('28-bestiario.md ausente: contagem de fichas impossível.')
}

# ---------------------------------------------------------------------------
# 5. A faixa 1 a 20 declarada em texto
# ---------------------------------------------------------------------------

$arqIntroducao = Join-Path $Pasta '01-introducao.md'
if (Test-Path -LiteralPath $arqIntroducao) {
    $textoIntro = Get-Content -LiteralPath $arqIntroducao -Encoding UTF8 -Raw
    if ($textoIntro -match 'n[íi]vel\s+1\s+a[oò]?\s*20|n[íi]veis\s+1\s+a\s+20|do\s+n[íi]vel\s+1\s+ao\s+20') {
        Write-Host 'Faixa de níveis: 1 a 20 declarada na introdução.'
    } else {
        [void]$erros.Add('01-introducao.md não declara em texto a faixa de nível 1 a 20.')
    }
} else {
    [void]$erros.Add('01-introducao.md ausente: faixa de níveis não verificável.')
}

# ---------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------

if ($erros.Count -eq 0) {
    Write-Host 'OK: livro completo pelos dois invariantes de contrato.' -ForegroundColor Green
    exit 0
}

Write-Host ('FALHA: {0} problema(s) de completude.' -f $erros.Count) -ForegroundColor Red
foreach ($erro in $erros) { Write-Host ('  {0}' -f $erro) }
exit 1
