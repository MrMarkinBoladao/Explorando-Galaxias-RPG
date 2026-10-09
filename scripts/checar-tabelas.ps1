<#
    checar-tabelas.ps1
    Gate de aritmética das tabelas do livro "Explorando Galáxias" v1.0.

    O QUE ELE CONFERE (design 23)
        1. Toda média impressa de dano, cura e Ultimate é
           `floor(nº de dados × (lados + 1) / 2)`. Casos de referência:
           6d6 = 21, 5d10 = 27, 5d8 = 22, 7d20 = 73, 18d20 = 189.
           Foi o erro que atravessava a v0.1 inteira (lá 6d6 valia 18).
        2. A tabela de Bônus de Atributo é monotônica não-decrescente
           (na v0.1, 13 e 14 davam os dois +2).
        3. A tabela mestra de progressão cobre os 20 níveis, sem nível vazio.
        4. A coluna de Nível equivalente da Ultimate aponta para Níveis de
           Habilidade que existem (1 a 7, capítulo 16).
        5. Nenhuma tabela de progressão ficou presa no nível 10.

    ONDE ELE PROCURA CADA COISA
        Médias: em todos os .md de `livro-v1.0/`, nos três formatos que o livro
        usa — célula de tabela seguida da média, linha de derivação
        (`6d6 = 6 × 3,5 | 21 | 21`) e prosa (`6d20 (média 63)`).

    COMO USAR
        powershell -File "scripts\checar-tabelas.ps1"
        powershell -File "scripts\checar-tabelas.ps1" -Pasta "C:\outra\pasta"

    CÓDIGO DE SAÍDA
        0 = aritmética conferida     1 = divergência encontrada
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

Write-Host ''
Write-Host '== checar-tabelas =='
Write-Host ("Pasta: {0}" -f $Pasta)

if (-not (Test-Path -LiteralPath $Pasta)) {
    Write-Host ('ERRO: pasta não encontrada: {0}' -f $Pasta) -ForegroundColor Red
    exit 1
}

$erros  = New-Object System.Collections.ArrayList
$avisos = New-Object System.Collections.ArrayList

# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

# Média oficial de uma expressão NdM, pela regra global de arredondamento
# para baixo do capítulo 02.
function Get-MediaOficial {
    param([int]$Dados, [int]$Lados)
    return [math]::Floor($Dados * ($Lados + 1) / 2.0)
}

# Limpa uma célula de tabela: negrito, crase, espaço e espaço fino.
function Format-Celula {
    param([string]$Texto)
    if ($null -eq $Texto) { return '' }
    $limpo = $Texto -replace '\*\*', '' -replace '`', ''
    return $limpo.Trim()
}

# Quebra uma linha de tabela GFM em células.
function Split-LinhaTabela {
    param([string]$Linha)
    $corte = $Linha.Trim()
    $corte = $corte -replace '^\|', '' -replace '\|$', ''
    return @($corte -split '\|' | ForEach-Object { Format-Celula $_ })
}

# ---------------------------------------------------------------------------
# 1. Médias de dados
#
#    Os três formatos que o livro usa para imprimir uma média:
#      prosa/ficha   `4d8 + 1` · média **19**   ou   `2d6` · **7**
#      parênteses    **6d20** (média 63)
#      derivação     | 6d6 = 6 × 3,5 | 21,0 | **21** |
#      tabela        | **1** | 6d6 | **21** | 5d8 | **22** | ...
#
#    Regras do casamento, para não gerar falso positivo:
#      - o modificador fixo (`+ 1`) entra na média esperada;
#      - um `+ N ×` (como `2d6 + 2 × Eficiência`) NÃO é modificador fixo e a
#        média impressa é então um valor de mesa, não a média dos dados: a
#        ocorrência é ignorada;
#      - vale a expressão de dados MAIS PRÓXIMA à esquerda do número impresso
#        (em `6d12 viram 3d12 (média 19)`, a média é a de 3d12);
#      - `00-*`, `01-*` e `30-*` são isentos, pela mesma razão do checador de
#        nomenclatura (design 23): changelog, introdução e glossário citam de
#        propósito os números ERRADOS da v0.1 (`6d6` "valia" 18);
#      - uma linha marcada com `<!-- media-livre -->` é ignorada.
# ---------------------------------------------------------------------------

$arquivos = @(Get-ChildItem -LiteralPath $Pasta -Filter '*.md' -File | Sort-Object Name)
$arquivosMedia = @($arquivos | Where-Object { $_.Name -notmatch '^(00|01|30)' })
$mediasConferidas = 0

# Localiza a expressão de dados mais próxima à esquerda de uma posição.
# Devolve $null quando não há nenhuma na janela, ou quando o modificador é
# multiplicativo (`+ 2 × Eficiência`).
function Get-DadosAEsquerda {
    param([string]$Linha, [int]$Posicao, [int]$Janela = 42)

    $inicio = [math]::Max(0, $Posicao - $Janela)
    $trecho = $Linha.Substring($inicio, $Posicao - $inicio)
    # Não atravessa separador de célula.
    $pipe = $trecho.LastIndexOf('|')
    if ($pipe -ge 0) { $trecho = $trecho.Substring($pipe + 1) }

    $ms = [regex]::Matches($trecho, '(\d+)\s*[dD](\d+)((?:\s*\+\s*\d+)?)')
    if ($ms.Count -eq 0) { return $null }
    $m = $ms[$ms.Count - 1]

    $modificador = 0
    if ($m.Groups[3].Value -match '\+\s*(\d+)') {
        # `+ 2 × Eficiência` não é modificador fixo.
        $depois = $trecho.Substring($m.Index + $m.Length)
        if ($depois -match '^\s*[×xX]') { return $null }
        $modificador = [int]$Matches[1]
    }

    return [pscustomobject]@{
        Dados       = [int]$m.Groups[1].Value
        Lados       = [int]$m.Groups[2].Value
        Modificador = $modificador
    }
}

foreach ($arquivo in $arquivosMedia) {
    $linhas = @(Get-Content -LiteralPath $arquivo.FullName -Encoding UTF8)
    for ($i = 0; $i -lt $linhas.Count; $i++) {
        $linha = $linhas[$i]
        if ($linha -match '<!--\s*media-livre\s*-->') { continue }

        # (a) Número impresso logo depois de "média" ou de um `·`.
        $marcadores = [regex]::Matches($linha, '(?:m[éeÉE]dia|·)[^0-9|\r\n]{0,10}?(\d+)')
        foreach ($mk in $marcadores) {
            $expr = Get-DadosAEsquerda -Linha $linha -Posicao $mk.Index
            if ($null -eq $expr) { continue }
            $impressa = [int]$mk.Groups[1].Value
            $esperada = (Get-MediaOficial -Dados $expr.Dados -Lados $expr.Lados) + $expr.Modificador
            $mediasConferidas++
            if ($impressa -ne $esperada) {
                $assinatura = if ($expr.Modificador -gt 0) { '{0}d{1} + {2}' -f $expr.Dados, $expr.Lados, $expr.Modificador } else { '{0}d{1}' -f $expr.Dados, $expr.Lados }
                [void]$erros.Add(('{0}:{1}  {2} impresso como média {3}, esperado {4}' -f `
                    $arquivo.Name, ($i + 1), $assinatura, $impressa, $esperada))
            }
        }

        if ($linha.TrimStart().StartsWith('|')) {
            $celulas = Split-LinhaTabela -Linha $linha

            # (b) Linha de derivação: `6d6 = 6 × 3,5 | 21,0 | **21** |`
            #     A última célula inteira da linha é a média arredondada.
            if ($celulas.Count -ge 2 -and $celulas[0] -match '^(\d+)\s*[dD](\d+)\s*=') {
                $dados = [int]$Matches[1]
                $lados = [int]$Matches[2]
                $ultima = $null
                for ($c = $celulas.Count - 1; $c -ge 1; $c--) {
                    if ($celulas[$c] -match '^\d+$') { $ultima = [int]$celulas[$c]; break }
                }
                if ($null -ne $ultima) {
                    $esperada = Get-MediaOficial -Dados $dados -Lados $lados
                    $mediasConferidas++
                    if ($ultima -ne $esperada) {
                        [void]$erros.Add(('{0}:{1}  derivação {2}d{3} fecha em {4}, esperado {5}' -f `
                            $arquivo.Name, ($i + 1), $dados, $lados, $ultima, $esperada))
                    }
                }
                continue
            }

            # (c) Célula que é só a expressão de dados, seguida de célula que é
            #     só um número: é o par (dados, média) das tabelas de 16.1 e 17.3.
            for ($c = 0; $c -lt $celulas.Count - 1; $c++) {
                if ($celulas[$c] -notmatch '^(\d+)\s*[dD](\d+)(?:\s*\+\s*(\d+))?$') { continue }
                $dados = [int]$Matches[1]
                $lados = [int]$Matches[2]
                $modificador = if ($Matches[3]) { [int]$Matches[3] } else { 0 }
                if ($celulas[$c + 1] -notmatch '^\d+$') { continue }
                $impressa = [int]$celulas[$c + 1]
                $esperada = (Get-MediaOficial -Dados $dados -Lados $lados) + $modificador
                $mediasConferidas++
                if ($impressa -ne $esperada) {
                    [void]$erros.Add(('{0}:{1}  {2}d{3} na tabela com média {4}, esperado {5}' -f `
                        $arquivo.Name, ($i + 1), $dados, $lados, $impressa, $esperada))
                }
            }
        }
    }
}

Write-Host ("Médias de dados conferidas: {0}" -f $mediasConferidas)
if ($mediasConferidas -lt 20 -and $arquivos.Count -ge 20) {
    [void]$avisos.Add('Poucas médias encontradas para um livro completo — confira se o formato das tabelas mudou.')
}

# ---------------------------------------------------------------------------
# 2. Bônus de Atributo monotônico
# ---------------------------------------------------------------------------

$arqAtributos = Join-Path $Pasta '04-atributos-e-pericias.md'
if (Test-Path -LiteralPath $arqAtributos) {
    $linhasAtr = @(Get-Content -LiteralPath $arqAtributos -Encoding UTF8)
    $achouLinha = $false
    foreach ($linha in $linhasAtr) {
        if ($linha -notmatch '^\|') { continue }
        $celulas = Split-LinhaTabela -Linha $linha
        if ($celulas.Count -lt 3) { continue }
        if ($celulas[0] -notmatch '^B[ôo]nus$') { continue }

        $achouLinha = $true
        $valores = New-Object System.Collections.ArrayList
        for ($c = 1; $c -lt $celulas.Count; $c++) {
            if ($celulas[$c] -match '^([+-]?\d+)$') { [void]$valores.Add([int]$Matches[1]) }
        }
        if ($valores.Count -lt 5) {
            [void]$erros.Add('04-atributos-e-pericias.md: a linha de Bônus de Atributo tem menos de 5 valores legíveis.')
            break
        }
        for ($v = 1; $v -lt $valores.Count; $v++) {
            if ($valores[$v] -lt $valores[$v - 1]) {
                [void]$erros.Add(('04-atributos-e-pericias.md: Bônus de Atributo não monotônico ({0} depois de {1}).' -f `
                    $valores[$v], $valores[$v - 1]))
            }
        }
        Write-Host ("Bônus de Atributo: {0} degraus, de {1} a {2} — monotonicidade verificada." -f `
            $valores.Count, $valores[0], $valores[$valores.Count - 1])
        break
    }
    if (-not $achouLinha) {
        [void]$erros.Add('04-atributos-e-pericias.md: linha de Bônus de Atributo não encontrada.')
    }
} else {
    [void]$avisos.Add('04-atributos-e-pericias.md ausente: checagem de Bônus de Atributo pulada.')
}

# ---------------------------------------------------------------------------
# 3. Progressão 1-20 sem nível vazio
# ---------------------------------------------------------------------------

$arqProgressao = Join-Path $Pasta '26-progressao-e-ressonancias.md'
if (Test-Path -LiteralPath $arqProgressao) {
    $linhasProg = @(Get-Content -LiteralPath $arqProgressao -Encoding UTF8)
    $niveis = New-Object System.Collections.Generic.HashSet[int]
    foreach ($linha in $linhasProg) {
        if ($linha -notmatch '^\|') { continue }
        $celulas = Split-LinhaTabela -Linha $linha
        if ($celulas.Count -lt 8) { continue }   # a tabela mestra tem 10 colunas
        if ($celulas[0] -match '^(\d+)$') {
            $n = [int]$Matches[1]
            if ($n -ge 1 -and $n -le 20) { [void]$niveis.Add($n) }
        }
    }
    $faltando = @(1..20 | Where-Object { -not $niveis.Contains($_) })
    if ($faltando.Count -gt 0) {
        [void]$erros.Add(('26-progressao-e-ressonancias.md: tabela mestra sem os níveis {0}.' -f ($faltando -join ', ')))
    } else {
        Write-Host 'Progressão: os 20 níveis presentes na tabela mestra.'
    }
} else {
    [void]$avisos.Add('26-progressao-e-ressonancias.md ausente: checagem de progressão pulada.')
}

# ---------------------------------------------------------------------------
# 4. Nível equivalente da Ultimate aponta para Nível de Habilidade existente
# ---------------------------------------------------------------------------

$arqUltimate = Join-Path $Pasta '17-ultimate-e-energia.md'
if (Test-Path -LiteralPath $arqUltimate) {
    $linhasUlt = @(Get-Content -LiteralPath $arqUltimate -Encoding UTF8)
    $dentroTabela = $false
    $colunaNivel = -1
    $equivalentes = New-Object System.Collections.ArrayList

    foreach ($linha in $linhasUlt) {
        if ($linha -notmatch '^\|') { $dentroTabela = $false; continue }
        $celulas = Split-LinhaTabela -Linha $linha

        if (-not $dentroTabela) {
            for ($c = 0; $c -lt $celulas.Count; $c++) {
                if ($celulas[$c] -match 'N[íi]vel equivalente') { $colunaNivel = $c; $dentroTabela = $true }
            }
            continue
        }
        if ($celulas[0] -match '^-+$') { continue }   # separador
        if ($colunaNivel -ge 0 -and $colunaNivel -lt $celulas.Count) {
            if ($celulas[$colunaNivel] -match '^(\d+)$') { [void]$equivalentes.Add([int]$Matches[1]) }
        }
    }

    if ($equivalentes.Count -eq 0) {
        [void]$erros.Add('17-ultimate-e-energia.md: coluna de Nível equivalente não encontrada ou vazia.')
    } else {
        foreach ($eq in $equivalentes) {
            if ($eq -lt 1 -or $eq -gt 7) {
                [void]$erros.Add(('17-ultimate-e-energia.md: Nível equivalente {0} não existe nas tabelas de Habilidade (1 a 7).' -f $eq))
            }
        }
        Write-Host ("Ultimate: Níveis equivalentes {0} — todos dentro de 1 a 7." -f ($equivalentes -join ' / '))
    }
} else {
    [void]$avisos.Add('17-ultimate-e-energia.md ausente: checagem de Nível equivalente pulada.')
}

# ---------------------------------------------------------------------------
# 5. Nenhuma tabela de progressão presa no nível 10
# ---------------------------------------------------------------------------

foreach ($arquivo in $arquivos) {
    $linhas = @(Get-Content -LiteralPath $arquivo.FullName -Encoding UTF8)
    $cabecalhoNivel = $false
    $linhaCabecalho = 0
    $niveisTabela = New-Object System.Collections.Generic.HashSet[int]

    for ($i = 0; $i -le $linhas.Count; $i++) {
        $linha = if ($i -lt $linhas.Count) { $linhas[$i] } else { '' }
        $eTabela = $linha.TrimStart().StartsWith('|')

        if ($eTabela) {
            $celulas = Split-LinhaTabela -Linha $linha
            if ($celulas.Count -ge 2 -and $celulas[0] -match '^N[íi]vel') {
                $cabecalhoNivel = $true
                $linhaCabecalho = $i + 1
                $niveisTabela.Clear()
                continue
            }
            if ($cabecalhoNivel -and $celulas[0] -match '^(\d+)$') {
                [void]$niveisTabela.Add([int]$Matches[1])
            }
            continue
        }

        # Fim da tabela: avalia se ela ficou presa no 10.
        if ($cabecalhoNivel) {
            $temAte10 = $true
            foreach ($n in 1..10) { if (-not $niveisTabela.Contains($n)) { $temAte10 = $false; break } }
            $maior = 0
            foreach ($n in $niveisTabela) { if ($n -gt $maior) { $maior = $n } }
            if ($temAte10 -and $maior -eq 10) {
                [void]$erros.Add(('{0}:{1}  tabela de Nível presa no 10 (o livro é de 1 a 20).' -f $arquivo.Name, $linhaCabecalho))
            }
            $cabecalhoNivel = $false
            $niveisTabela.Clear()
        }
    }
}

# ---------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------

foreach ($aviso in $avisos) { Write-Host ('AVISO: {0}' -f $aviso) -ForegroundColor Yellow }

if ($erros.Count -eq 0) {
    Write-Host 'OK: aritmética das tabelas conferida.' -ForegroundColor Green
    exit 0
}

Write-Host ('FALHA: {0} divergência(s).' -f $erros.Count) -ForegroundColor Red
foreach ($erro in $erros) { Write-Host ('  {0}' -f $erro) }
exit 1
