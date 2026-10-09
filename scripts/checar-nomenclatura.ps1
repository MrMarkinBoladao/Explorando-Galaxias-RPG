<#
    checar-nomenclatura.ps1
    Gate de nomenclatura do livro "Explorando Galáxias" v1.0.

    O QUE ELE FAZ
        Varre os .md de `livro-v1.0/` procurando SÓ as 25 strings proibidas da
        Coluna A do documento de design (seção 3.1) — palavras que não existem
        no vocabulário do sistema. Uma ocorrência em capítulo de regra é falha
        fatal: o script sai com código 1 e imprime arquivo, linha e termo.

        Ele NÃO verifica a Coluna B (3.2). A Coluna B lista palavras que o livro
        USA como termo oficial em outro contexto ("vida" em Propósito de Vida,
        "ação" em Ação Complementar, "resistência" nos 6 Testes de Resistência),
        e procurá-las reprovaria os 28 capítulos de uma vez. Uso incorreto de
        termo é revisão humana, por decisão de design.

    VÁLVULA (design 23)
        As strings proibidas são IGNORADAS em `00-*`, `01-*` e `30-*` — a capa,
        a introdução com o changelog e o glossário precisam citar os termos
        aposentados da v0.1 — e em qualquer linha marcada com
        `<!-- termo-historico -->`.

    COMO USAR
        powershell -File "scripts\checar-nomenclatura.ps1"
        powershell -File "scripts\checar-nomenclatura.ps1" -Pasta "C:\outra\pasta"

    CÓDIGO DE SAÍDA
        0 = nenhuma ocorrência (ou pasta sem .md)   1 = ocorrência encontrada
#>
[CmdletBinding()]
param(
    # Pasta a varrer. Vazio = `livro-v1.0` na raiz do projeto.
    [string]$Pasta = ''
)

$ErrorActionPreference = 'Stop'

# A raiz do projeto é a pasta acima de scripts/, para o script funcionar
# chamado de qualquer lugar.
$RaizProjeto = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($Pasta)) {
    $Pasta = Join-Path $RaizProjeto 'livro-v1.0'
}

# As 25 strings da Coluna A (design 3.1). Lista fechada.
$TermosProibidos = @(
    'HP', 'DoT', 'iniciativa', 'ação bônus', 'ação menor', 'ação comum',
    'ação completa', 'rodada', 'round', 'stagger', 'poise', 'break',
    'skill points', 'SP', 'mana', 'memosprite', 'CD', 'salvaguarda', 'save',
    'proficiência', 'ult charge', 'push back', 'action advance',
    'provavelmente vou mudar o nome', 'nível 1 a 10'
)

Write-Host ''
Write-Host '== checar-nomenclatura =='
Write-Host ("Pasta: {0}" -f $Pasta)

if (-not (Test-Path -LiteralPath $Pasta)) {
    Write-Host ('ERRO: pasta não encontrada: {0}' -f $Pasta) -ForegroundColor Red
    exit 1
}

# Arquivos isentos por prefixo (capa/creditos, introdução/changelog, glossário).
$arquivos = @(
    Get-ChildItem -LiteralPath $Pasta -Filter '*.md' -File |
        Where-Object { $_.Name -notmatch '^(00|01|30)' } |
        Sort-Object Name
)

$achados = New-Object System.Collections.ArrayList

foreach ($arquivo in $arquivos) {
    $linhas = @(Get-Content -LiteralPath $arquivo.FullName -Encoding UTF8)
    for ($i = 0; $i -lt $linhas.Count; $i++) {
        $linha = $linhas[$i]
        # Válvula de linha: termo citado como histórico é legítimo.
        if ($linha -match '<!--\s*termo-historico\s*-->') { continue }
        foreach ($termo in $TermosProibidos) {
            # Casamento insensível a maiúsculas e delimitado por fronteira de
            # palavra: `break` não casa dentro de "Quebra", `SP` não casa dentro
            # de outra palavra.
            $padrao = '\b' + [regex]::Escape($termo) + '\b'
            if ([regex]::IsMatch($linha, $padrao, 'IgnoreCase')) {
                [void]$achados.Add([pscustomobject]@{
                    Arquivo = $arquivo.Name
                    Linha   = $i + 1
                    Termo   = $termo
                    Texto   = $linha.Trim()
                })
            }
        }
    }
}

Write-Host ("Arquivos varridos: {0} (00-*, 01-* e 30-* isentos por design 23)" -f $arquivos.Count)

if ($achados.Count -eq 0) {
    Write-Host 'OK: nenhuma das 25 strings proibidas da Coluna A aparece nos capítulos de regra.' -ForegroundColor Green
    exit 0
}

Write-Host ('FALHA: {0} ocorrência(s) de termo proibido.' -f $achados.Count) -ForegroundColor Red
foreach ($achado in $achados) {
    $trecho = $achado.Texto
    if ($trecho.Length -gt 110) { $trecho = $trecho.Substring(0, 110) + '...' }
    Write-Host ('  {0}:{1}  [{2}]  {3}' -f $achado.Arquivo, $achado.Linha, $achado.Termo, $trecho)
}
exit 1
