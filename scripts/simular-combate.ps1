<#
    simular-combate.ps1
    Verificador do passe de balanceamento de "Explorando Galáxias" v1.0.

    O QUE ELE FAZ (design 23, item 34 do plano de escrita)
        Recebe as premissas de 18.1 como parâmetros, reproduz o DPC de 18.2
        PARCELA POR PARCELA nas cinco faixas e compara com o publicado. Imprime,
        por faixa:
          - o DPC de referência (acerto e RD de Elite, cadência de Quebra de Boss);
          - o DPC puro de Elite (Quebra todo Ciclo);
          - o DPC puro de Boss (acerto 55%, RD de Boss, 4 Fraquezas);
          - os Ciclos até a resolução contra o PV de Boss de 18.3;
          - a attrition do grupo por combate e no terceiro combate do dia;
          - a parcela do Memoespírito (13.1).

    ELE REPROVA (código 1) SE
        - alguma faixa sair da janela de 3 a 5 Ciclos;
        - o DPC de referência divergir do publicado em mais de 5%;
        - a attrition de um combate sair de 70% a 85% restantes;
        - a attrition do terceiro combate do dia sair de 45% a 70%;
        - o Memoespírito sair de 15% a 25% do dano do dono na faixa 17-20.

    UMA ESCOLHA DECLARADA SOBRE O MEMOESPÍRITO
        O design abre a conta do Memoespírito em UMA faixa, a 17-20 (13.1:
        `5d6 + 5` ≈ 22, cerca de 25% do dano do dono). Nas faixas baixas os
        pontos fixos da ficha dele pesam mais do que os dados — um Memoespírito
        de nível 3 tem os mesmos "até 5 pontos por atributo" e só 1 dado de
        Ataque Básico —, então a razão sobe. O script imprime a razão nas cinco
        faixas e REPROVA na faixa que o design fecha; nas outras quatro a linha
        é informativa, e está escrita assim de propósito em vez de inventar
        número que o design não publicou.

    COMO USAR
        powershell -File "scripts\simular-combate.ps1"
        powershell -File "scripts\simular-combate.ps1" -Verboso
        powershell -File "scripts\simular-combate.ps1" -TaxaAcertoElite 0.55

    CÓDIGO DE SAÍDA
        0 = todas as janelas publicadas reproduzidas     1 = fora de janela
#>
[CmdletBinding()]
param(
    # --- Premissas de 18.1, todas parametrizadas ---
    [double]$TaxaAcertoComum = 0.70,
    [double]$TaxaAcertoElite = 0.60,
    [double]$TaxaAcertoBoss  = 0.55,
    [double]$TaxaCritico     = 0.05,
    # Bônus de Atributo do atacante de referência (satura em +5 por 5.1).
    [int]$AtributoAtacante   = 5,
    # Esquiva: dos ataques inimigos de um Ciclo, quantos são Esquivados e com
    # que acerto efetivo.
    [int]$AtaquesInimigosPorCiclo = 3,
    [int]$AtaquesEsquivadosPorCiclo = 1,
    [double]$AcertoInimigo = 0.60,
    [double]$AcertoNoEsquivado = 0.20,
    # Ritmo do combate e do dia.
    [int]$CiclosPorCombate = 4,
    [int]$CombatesPorDia = 3,
    [int]$DescansosCurtosPorDia = 2,
    [int]$BonusVigorTipico = 2,
    [int]$TamanhoDoGrupo = 4,
    # Área: alvos de uma Habilidade em área (10.1).
    [int]$AlvosEmArea = 3,
    # Memoespírito: pontos no atributo de ataque. 0 = proporcional aos pontos
    # disponíveis no nível (um quarto deles, teto de 5, como em 13.1).
    [int]$PontosAtaqueMemo = 0,
    # Tolerância de divergência do DPC contra o publicado.
    [double]$ToleranciaDPC = 0.05,
    [switch]$Verboso
)

$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Tabelas do design (16.1, 17.3, 18.2 e 18.3)
# ---------------------------------------------------------------------------

# Dano de Habilidade por Nível (capítulo 16): dados e lados.
$DadosPorNivelHabilidade = @{
    1 = @{ Dados = 6;  Lados = 6  }
    2 = @{ Dados = 5;  Lados = 10 }
    3 = @{ Dados = 6;  Lados = 12 }
    4 = @{ Dados = 6;  Lados = 20 }
    5 = @{ Dados = 10; Lados = 20 }
    6 = @{ Dados = 14; Lados = 20 }
    7 = @{ Dados = 18; Lados = 20 }
}

# As cinco faixas. Tudo aqui é do design: 18.2 (personagem de referência) e
# 18.3 (âncoras de inimigo e attrition publicada).
$Faixas = @(
    [pscustomobject]@{
        Nome = '1-4';   NivelRef = 3;  Eficiencia = 2; DadosArma = 1; Maos = 2; Esfera = 2
        RdElite = 2;    RdBoss = 4;    NivelEqUltimate = 2
        MixHabilidade = @(@{ Nivel = 2; Peso = 1.00 })
        PvBoss = 305;   PvGrupo = 292; DanoBoss = 10
        DpcRefPub = 88; DpcElitePub = 100; DpcBossPub = 82
    },
    [pscustomobject]@{
        Nome = '5-8';   NivelRef = 7;  Eficiencia = 4; DadosArma = 2; Maos = 4; Esfera = 4
        RdElite = 2;    RdBoss = 4;    NivelEqUltimate = 3
        MixHabilidade = @(@{ Nivel = 3; Peso = 0.75 }, @{ Nivel = 2; Peso = 0.25 })
        PvBoss = 410;   PvGrupo = 468; DanoBoss = 20
        DpcRefPub = 119; DpcElitePub = 137; DpcBossPub = 112
    },
    [pscustomobject]@{
        Nome = '9-12';  NivelRef = 11; Eficiencia = 5; DadosArma = 3; Maos = 4; Esfera = 4
        RdElite = 3;    RdBoss = 6;    NivelEqUltimate = 4
        MixHabilidade = @(@{ Nivel = 4; Peso = 1.00 })
        PvBoss = 580;   PvGrupo = 644; DanoBoss = 28
        DpcRefPub = 168; DpcElitePub = 187; DpcBossPub = 154
    },
    [pscustomobject]@{
        Nome = '13-16'; NivelRef = 15; Eficiencia = 6; DadosArma = 4; Maos = 6; Esfera = 6
        RdElite = 3;    RdBoss = 6;    NivelEqUltimate = 5
        MixHabilidade = @(@{ Nivel = 6; Peso = 0.50 }, @{ Nivel = 3; Peso = 0.25 })
        PvBoss = 750;   PvGrupo = 820; DanoBoss = 36
        DpcRefPub = 218; DpcElitePub = 238; DpcBossPub = 200
    },
    [pscustomobject]@{
        Nome = '17-20'; NivelRef = 19; Eficiencia = 8; DadosArma = 5; Maos = 8; Esfera = 8
        RdElite = 4;    RdBoss = 8;    NivelEqUltimate = 6
        MixHabilidade = @(@{ Nivel = 7; Peso = 0.50 }, @{ Nivel = 3; Peso = 0.25 })
        PvBoss = 935;   PvGrupo = 996; DanoBoss = 48
        DpcRefPub = 271; DpcElitePub = 295; DpcBossPub = 247
    }
)

# ---------------------------------------------------------------------------
# Aritmética do capítulo 02: média de NdM, arredondada para baixo
# ---------------------------------------------------------------------------

function Get-Media {
    param([int]$Dados, [int]$Lados)
    return [math]::Floor($Dados * ($Lados + 1) / 2.0)
}

# Os +2 dados de Fraqueza são do MESMO tipo dos dados da parcela (9.3).
function Get-ExtraFraqueza {
    param([int]$Lados)
    return (Get-Media -Dados 2 -Lados $Lados)
}

# DPC de um perfil: $Acerto, $Rd, se os DOIS Ataques Básicos acertam Fraqueza
# (4 Fraquezas do Boss) e se a Quebra sai todo Ciclo (Elite) ou a cada 2 (Boss).
function Get-Dpc {
    param(
        [pscustomobject]$Faixa,
        [double]$Acerto,
        [int]$Rd,
        [bool]$DoisAtaquesComFraqueza,
        [double]$CiclosPorQuebra
    )

    $mediaArma   = Get-Media -Dados $Faixa.DadosArma -Lados 10
    $extraArma   = Get-ExtraFraqueza -Lados 10
    $baseAtaque  = $mediaArma + $AtributoAtacante + $Faixa.Maos

    # Ataque Básico: um com Fraqueza sempre; o segundo só contra Boss (4 Fraquezas).
    $ab1 = $baseAtaque + $extraArma - $Rd
    $ab2 = if ($DoisAtaquesComFraqueza) { $baseAtaque + $extraArma - $Rd } else { $baseAtaque - $Rd }
    $parcelaAtaques = ($ab1 + $ab2) * $Acerto

    # Habilidade: mix de Níveis que a geração de PH sustenta (8.2).
    $parcelaHabilidade = 0.0
    $dadosBaseHabilidade = 0.0
    foreach ($entrada in $Faixa.MixHabilidade) {
        $d = $DadosPorNivelHabilidade[[int]$entrada.Nivel]
        $media = Get-Media -Dados $d.Dados -Lados $d.Lados
        $instancia = $media + $AtributoAtacante + $Faixa.Esfera + (Get-ExtraFraqueza -Lados $d.Lados) - $Rd
        $parcelaHabilidade += [double]$entrada.Peso * $instancia
        $dadosBaseHabilidade += [double]$entrada.Peso * $media
    }
    $parcelaHabilidade = $parcelaHabilidade * $Acerto

    # Ultimate: 1 por Ciclo no grupo, no Nível equivalente da faixa (8.5).
    $du = $DadosPorNivelHabilidade[[int]$Faixa.NivelEqUltimate]
    $mediaUltimate = Get-Media -Dados $du.Dados -Lados $du.Lados
    $parcelaUltimate = ($mediaUltimate + $AtributoAtacante + $Faixa.Esfera + (Get-ExtraFraqueza -Lados $du.Lados) - $Rd) * $Acerto

    # Crítico: 5% das rolagens dobrando SÓ os dados base (4.6).
    $dadosBaseNoCiclo = (2 * $mediaArma) + $dadosBaseHabilidade + $mediaUltimate
    $parcelaCritico = $dadosBaseNoCiclo * $TaxaCritico

    # Quebra: Dano de Quebra sofre RD; o Dano Contínuo (2 turnos) ignora RD.
    $danoDeQuebra = (Get-Media -Dados 2 -Lados 6) + (2 * $Faixa.Eficiencia) - $Rd
    $contínuo = ((Get-Media -Dados 2 -Lados 6) + $Faixa.Eficiencia) * 2
    $parcelaQuebra = ($danoDeQuebra + $contínuo) / $CiclosPorQuebra

    return [pscustomobject]@{
        Ataques    = $parcelaAtaques
        Habilidade = $parcelaHabilidade
        Ultimate   = $parcelaUltimate
        Critico    = $parcelaCritico
        Quebra     = $parcelaQuebra
        Total      = $parcelaAtaques + $parcelaHabilidade + $parcelaUltimate + $parcelaCritico + $parcelaQuebra
    }
}

# ---------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------

Write-Host ''
Write-Host '== simular-combate =='
Write-Host ("Premissas: acerto {0:P0}/{1:P0}/{2:P0} (Comum/Elite/Boss) · crítico {3:P0} · {4} ataques inimigos por Ciclo, {5} Esquivado · combate de {6} Ciclos" -f `
    $TaxaAcertoComum, $TaxaAcertoElite, $TaxaAcertoBoss, $TaxaCritico, `
    $AtaquesInimigosPorCiclo, $AtaquesEsquivadosPorCiclo, $CiclosPorCombate)
Write-Host ''

$reprovas = New-Object System.Collections.ArrayList
$linhasResumo = New-Object System.Collections.ArrayList

foreach ($faixa in $Faixas) {

    # Os três DPCs de 18.2.
    $dpcRef   = Get-Dpc -Faixa $faixa -Acerto $TaxaAcertoElite -Rd $faixa.RdElite -DoisAtaquesComFraqueza $false -CiclosPorQuebra 2.0
    $dpcElite = Get-Dpc -Faixa $faixa -Acerto $TaxaAcertoElite -Rd $faixa.RdElite -DoisAtaquesComFraqueza $false -CiclosPorQuebra 1.0
    $dpcBoss  = Get-Dpc -Faixa $faixa -Acerto $TaxaAcertoBoss  -Rd $faixa.RdBoss  -DoisAtaquesComFraqueza $true  -CiclosPorQuebra 2.0

    $divergencia = [math]::Abs($dpcRef.Total - $faixa.DpcRefPub) / $faixa.DpcRefPub

    # Ciclos até a resolução: é o DPC puro de Boss que mede isso (18.3).
    $ciclos = $faixa.PvBoss / $dpcBoss.Total

    # Attrition: a Esquiva entra no modelo (18.1).
    $acertosPorCiclo = (($AtaquesInimigosPorCiclo - $AtaquesEsquivadosPorCiclo) * $AcertoInimigo) + ($AtaquesEsquivadosPorCiclo * $AcertoNoEsquivado)
    $danoRecebidoCombate = $acertosPorCiclo * $faixa.DanoBoss * $CiclosPorCombate
    $restanteCombate = ($faixa.PvGrupo - $danoRecebidoCombate) / $faixa.PvGrupo

    # O dia: três combates e dois Descansos Curtos de `(2 × nível) + Bônus de Vigor`.
    $descansoGrupo = ((2 * $faixa.NivelRef) + $BonusVigorTipico) * $TamanhoDoGrupo
    $pvNoFimDoDia = $faixa.PvGrupo - ($CombatesPorDia * $danoRecebidoCombate) + ($DescansosCurtosPorDia * $descansoGrupo)
    $restanteTerceiro = $pvNoFimDoDia / $faixa.PvGrupo

    # Memoespírito (13.1): dados de Ataque Básico do dono em d6, + pontos.
    $pontosDisponiveis = 12 + [math]::Floor($faixa.NivelRef / 2)
    $pontosAtaque = if ($PontosAtaqueMemo -gt 0) { $PontosAtaqueMemo } else {
        [math]::Min(5, [math]::Round($pontosDisponiveis * 0.25))
    }
    $danoMemo = (Get-Media -Dados $faixa.DadosArma -Lados 6) + $pontosAtaque
    $danoMemoComFraqueza = $danoMemo + (Get-ExtraFraqueza -Lados 6)
    $memoPorCiclo = ($danoMemoComFraqueza - $faixa.RdElite) * $TaxaAcertoElite
    $razaoMemo = $memoPorCiclo / $dpcRef.Habilidade
    $efeitoMemoNoDpc = $memoPorCiclo / $dpcRef.Total

    # Área: metade dos dados, teto de alvos (10.1).
    $dTopo = $DadosPorNivelHabilidade[[int]($faixa.MixHabilidade[0].Nivel)]
    $dadosArea = [math]::Max(1, [math]::Floor($dTopo.Dados / 2))
    $danoArea = (Get-Media -Dados $dadosArea -Lados $dTopo.Lados) + $AtributoAtacante + $faixa.Esfera
    $danoAlvoUnico = (Get-Media -Dados $dTopo.Dados -Lados $dTopo.Lados) + $AtributoAtacante + $faixa.Esfera + (Get-ExtraFraqueza -Lados $dTopo.Lados) - $faixa.RdElite
    $multiplicadorArea = ($danoArea * $AlvosEmArea) / $danoAlvoUnico

    Write-Host ("--- Faixa {0} (nível {1} · Eficiência +{2} · arma {3}d10 · Mãos e Esfera +{4} · RD de Elite {5}) ---" -f `
        $faixa.Nome, $faixa.NivelRef, $faixa.Eficiencia, $faixa.DadosArma, $faixa.Maos, $faixa.RdElite)

    if ($Verboso) {
        Write-Host ("  2 Ataques Básicos {0,8:N1}   Habilidade {1,8:N1}   Ultimate {2,8:N1}   Crítico {3,6:N1}   Quebra/2 {4,6:N1}" -f `
            $dpcRef.Ataques, $dpcRef.Habilidade, $dpcRef.Ultimate, $dpcRef.Critico, $dpcRef.Quebra)
    }

    Write-Host ("  DPC de referência {0,7:N1}  (publicado {1}, divergência {2:P1})" -f $dpcRef.Total, $faixa.DpcRefPub, $divergencia)
    Write-Host ("  DPC puro de Elite {0,7:N1}  (publicado {1})" -f $dpcElite.Total, $faixa.DpcElitePub)
    Write-Host ("  DPC puro de Boss  {0,7:N1}  (publicado {1})" -f $dpcBoss.Total, $faixa.DpcBossPub)
    Write-Host ("  Ciclos até a resolução {0,5:N1}  ({1} PV de Boss)" -f $ciclos, $faixa.PvBoss)
    Write-Host ("  Attrition: {0:P0} dos PV no fim do combate · {1:P0} no fim do terceiro combate do dia" -f $restanteCombate, $restanteTerceiro)
    Write-Host ("  Memoespírito: {0:N1} por Ciclo = {1:P0} do dano do dono · efeito no DPC do grupo {2:P1}" -f $memoPorCiclo, $razaoMemo, $efeitoMemoNoDpc)
    Write-Host ("  Área: {0} alvos a {1:N0} cada = {2:N0} contra {3:N0} de alvo único ({4:N2} ×)" -f `
        $AlvosEmArea, $danoArea, ($danoArea * $AlvosEmArea), $danoAlvoUnico, $multiplicadorArea)
    Write-Host ''

    # --- Janelas que reprovam ---
    if ($ciclos -lt 3.0 -or $ciclos -gt 5.0) {
        [void]$reprovas.Add(('faixa {0}: combate em {1:N1} Ciclos, fora da janela de 3 a 5.' -f $faixa.Nome, $ciclos))
    }
    if ($divergencia -gt $ToleranciaDPC) {
        [void]$reprovas.Add(('faixa {0}: DPC {1:N1} contra {2} publicado, divergência {3:P1} acima da tolerância de {4:P0}.' -f `
            $faixa.Nome, $dpcRef.Total, $faixa.DpcRefPub, $divergencia, $ToleranciaDPC))
    }
    if ($restanteCombate -lt 0.70 -or $restanteCombate -gt 0.85) {
        [void]$reprovas.Add(('faixa {0}: grupo termina o combate com {1:P0} dos PV, fora de 70% a 85%.' -f $faixa.Nome, $restanteCombate))
    }
    if ($restanteTerceiro -lt 0.45 -or $restanteTerceiro -gt 0.70) {
        [void]$reprovas.Add(('faixa {0}: grupo termina o terceiro combate com {1:P0} dos PV, fora de 45% a 70%.' -f $faixa.Nome, $restanteTerceiro))
    }
    # A janela do Memoespírito é verificada na faixa que o design abre (13.1).
    if ($faixa.Nome -eq '17-20' -and ($razaoMemo -lt 0.15 -or $razaoMemo -gt 0.25)) {
        [void]$reprovas.Add(('faixa {0}: Memoespírito em {1:P0} do dano do dono, fora de 15% a 25%.' -f $faixa.Nome, $razaoMemo))
    }

    [void]$linhasResumo.Add([pscustomobject]@{
        Faixa          = $faixa.Nome
        DPC            = [math]::Round($dpcRef.Total, 1)
        Publicado      = $faixa.DpcRefPub
        Divergencia    = ('{0:P1}' -f $divergencia)
        ElitePuro      = [math]::Round($dpcElite.Total, 1)
        BossPuro       = [math]::Round($dpcBoss.Total, 1)
        Ciclos         = [math]::Round($ciclos, 2)
        FimDoCombate   = ('{0:P0}' -f $restanteCombate)
        TerceiroCombate= ('{0:P0}' -f $restanteTerceiro)
        Memoespirito   = ('{0:P0}' -f $razaoMemo)
    })
}

Write-Host '== Resumo das cinco faixas =='
$linhasResumo | Format-Table -AutoSize | Out-String | Write-Host

if ($reprovas.Count -eq 0) {
    Write-Host 'OK: as cinco faixas reproduzem as janelas publicadas (3 a 5 Ciclos, DPC dentro de 5%, attrition 70-85% e 45-70%).' -ForegroundColor Green
    exit 0
}

Write-Host ('FALHA: {0} janela(s) fora do publicado.' -f $reprovas.Count) -ForegroundColor Red
foreach ($reprova in $reprovas) { Write-Host ('  {0}' -f $reprova) }
exit 1
