# -*- coding: utf-8 -*-
"""
gerar_mestre.py — Gera a Planilha do Mestre do RPG "Explorando Galáxias" v1.2 (.xlsx para o Google Planilhas).

O QUE ELE FAZ
    Monta, com openpyxl, um único .xlsx com as 18 abas de D3 (design .agents\\tasks\\mestre\\design.md):
    Fase 1 = Início, Campanha (Mesa), Grupo, Inimigos, Bestiário, Encontros, Combate, Tabelas e Dados; as
    demais abas existem na ordem final com título, legenda e "Em construção". As tabelas do livro vêm de
    build\\mestre_dados.py (que reaproveita build\\ficha_dados.py por import); os estilos vêm de
    build\\gerar_ficha.py por import. Nenhum arquivo da ficha é alterado.
    Fórmulas em inglês com vírgula, só funções de build\\ficha_funcoes_ok.json, sem macro, sem _xlfn, sem
    INDIRECT; toda entrada sai VAZIA no modelo; fullCalcOnLoad ligado.

COMO USAR
    $env:PYTHONUTF8="1"; python "build\\gerar_mestre.py"

SAÍDA
    Mestre\\Planilha do Mestre - Explorando Galáxias V1.2.xlsx   (modelo em branco)
    Mestre\\Planilha do Mestre - Exemplo.xlsx                   (o mesmo modelo com a campanha de exemplo)
    build\\mestre_mapa.json                                     (contrato gerador × testes)
"""

import json
import os
import sys
import time
from pathlib import Path

BUILD = Path(__file__).resolve().parent
sys.path.insert(0, str(BUILD))

import mestre_dados as D  # noqa: E402
from mestre import nucleo as N  # noqa: E402


def montar():
    """Monta o workbook do modelo (sem gravar). Devolve wb."""
    from mestre import (aba_inicio, aba_campanha, aba_tabelas, aba_inimigos, aba_bestiario, aba_encontros,
                        aba_combate, aba_npcs, aba_aventuras, aba_recompensas, aba_campanha3, aba_sessoes, aba_mundos,
                        aba_improviso, aba_escudo, aba_minhas)
    import gerar_ficha as G
    from mestre import protecao
    N.iniciar()
    protecao.iniciar()
    wb = N.novo_workbook()
    for ws in wb.worksheets:
        N.cabecalho_aba(ws)
    N.escrever_dados(wb["Dados"], D.blocos(), D.listas())
    aba_tabelas.montar(wb)
    aba_inicio.montar(wb)
    aba_campanha.montar_campanha(wb)
    aba_campanha.montar_grupo(wb)
    aba_inimigos.montar(wb)
    aba_bestiario.montar(wb)
    aba_encontros.montar(wb)
    aba_combate.montar(wb)
    aba_npcs.montar(wb)              # Fase 2 (R5, R6, R7)
    aba_aventuras.montar(wb)
    aba_recompensas.montar(wb)
    aba_campanha3.montar_gestao(wb)  # Fase 3 (R8–R11, R13)
    aba_sessoes.montar(wb)
    aba_mundos.montar(wb)
    aba_improviso.montar(wb)
    aba_escudo.montar(wb)
    aba_minhas.montar(wb)
    for nome in N.ABAS:
        if nome not in N.ABAS_PRONTAS:
            N.aba_em_construcao(wb[nome])
    N.resolver_marcadores(wb)
    prot = protecao.proteger(wb)     # requisito do Google (revisão 2 da ficha): leitura protegida + contador
    aba_inicio.preencher_alertas(wb)  # avisos por aba (depois da camada, que também cria avisos)
    N.ocultar_auxiliares(wb)
    for ws in wb.worksheets:
        G.legenda(ws, 2)
        ws.sheet_view.showGridLines = True
    G.marcar_tabelas(wb)
    N.formatar_avisos(wb)
    # listas de nomes calculados (inimigos da campanha, combatentes): o pior caso é o nome mais longo do bestiário
    # ou um nome digitado no tamanho máximo (os mesmos textos de pior caso da suíte visual)
    import re
    import renderizar_ficha as R
    ordem = sorted(N.MAPA.entradas.items())
    nomes = [N.texto_pior(int(i.get("maximo") or 40), 7 * k) for k, (n, i) in enumerate(ordem)
             if re.fullmatch(r"(inimigos\.\d+|grupo\.pj\d)\.nome", n)]
    for n, i in N.MAPA.entradas.items():
        if i["tipo"] == "lista" and not i.get("opcoes"):
            N.MAPA.pior[N.MAPA.celulas[n]] = nomes + ["Operativo de Campo dos Caçadores 10"]
        elif i["tipo"] == "lista" and "«inimigos.cat.nome»" in str(i.get("fonte")):
            # catálogo (Combate C3 "Trocar por"): bestiário + inimigos da campanha com o nome digitado no máximo
            N.MAPA.pior[N.MAPA.celulas[n]] = nomes + list(i["opcoes"])
    problemas = N.ajustar_layout(wb, pior_caso_entradas())
    if problemas:
        raise ValueError("texto que não cabe na largura (área fixa de 1360 px):\n  " + "\n  ".join(problemas[:30]))
    altas = aba_escudo.paginas_altas(wb)
    if altas:
        raise ValueError("Escudo do Mestre: página mais alta que A4 paisagem (40 linhas de 15 pt):\n  " +
                         "\n  ".join(altas))
    print(f"Leitura protegida: {prot['leitura']} células da camada, {prot['sinais']} sinais de linha")
    return wb


def pior_caso_entradas():
    """Texto de pior caso de cada entrada ("'Aba'!A1" -> texto) para medir a altura das linhas."""
    import renderizar_ficha as R
    saida = {}
    for k, (nome, info) in enumerate(sorted(N.MAPA.entradas.items())):
        ref = N.MAPA.celulas[nome]
        if info["tipo"] == "lista":
            op = info.get("opcoes") or []
            # lista de nomes calculados (inimigos, combatentes): o nome mais longo do bestiário com o número
            saida[ref] = str(max(op, key=lambda s: len(str(s)))) if op else "Operativo de Campo dos Caçadores 10"
        elif info["tipo"] == "inteiro":
            saida[ref] = str(info.get("maximo"))
        else:
            saida[ref] = N.texto_pior(int(info.get("maximo") or 40), 7 * k)
    return saida


def gravar(wb, destino):
    """Grava num temporário na mesma pasta e só então troca (nunca deixa .xlsx pela metade)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_name(destino.stem + ".tmp.xlsx")
    try:
        wb.save(tmp)
        os.replace(tmp, destino)
    except PermissionError:
        if tmp.exists():
            tmp.unlink()
        raise SystemExit(f"Não foi possível gravar {destino}: feche o arquivo no Excel/Drive e rode de novo.")


def main():
    t0 = time.time()
    wb = montar()
    gravar(wb, N.SAIDA_MODELO)
    N.MAPA.salvar()
    nf = sum(1 for ws in wb.worksheets for linha in ws.iter_rows() for c in linha
             if isinstance(c.value, str) and c.value.startswith("="))
    ndv = sum(len(ws.data_validations.dataValidation) for ws in wb.worksheets)
    print(f"Modelo:  {N.SAIDA_MODELO} ({len(wb.sheetnames)} abas, {nf} fórmulas, {ndv} validações, "
          f"{len(N.MAPA.entradas)} entradas)")
    from mestre import exemplo
    wb2 = exemplo.preencher(wb)
    gravar(wb2, N.SAIDA_EXEMPLO)
    print(f"Exemplo: {N.SAIDA_EXEMPLO} ({exemplo.N_ENTRADAS} entradas preenchidas)")
    print(f"Mapa:    {N.SAIDA_MAPA} ({len(N.MAPA.celulas)} nomes lógicos, {len(N.MAPA.blocos)} blocos, "
          f"{len(N.MAPA.listas)} listas, {len(N.MAPA.numeros_de_regra)} números de regra)")
    print(f"Tempo:   {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
