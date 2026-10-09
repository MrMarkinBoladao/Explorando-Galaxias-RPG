# -*- coding: utf-8 -*-
"""Aba Tabelas — listas dos geradores, editáveis (design §4.2, §6.16).

Bloco 1 (Fase 1): listas do livro (27.16–27.18) e ambiente por facção (H8). Blocos 2 a 6 (Fase 2): as tabelas de
sabor de build\\mestre_sabor.py (nomes por cultura, NPC, aventura, recompensa). Cada bloco tem até 9 colunas
visíveis (B…J; K:L ficam para o aviso da linha, como na Fase 1); as tabelas de duas colunas (chave + valor) ocupam duas.
Cada lista tem 100 vagas em 8 faixas de 13 (a última com 9), cada faixa com o cabeçalho repetido; ao lado (coluna
oculta) o contador corrido: vaga = anterior + IF(LEN(valor)>0,1,0); cabeçalho = anterior. "Tamanho da lista" = último
contador. O k-ésimo valor não vazio = INDEX(coluna, MATCH(k, contador, 0)).
"""

from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

import mestre_dados as D
import mestre_sabor as SB
from mestre import nucleo as N
from mestre.nucleo import cal, av, rot, cab, titulo

VAGAS = 100
FAIXA = 13
PX_LISTA = 210
BLOCOS = [("nomes", "Nomes por cultura (05) — Sugestão da planilha; ficam fora da ortografia"),
          ("sobrenomes", "Sobrenomes, epítetos, clãs e nomes escolhidos (05) — Sugestão da planilha"),
          ("npc", "Gerador de NPCs (aba NPCs) — Sugestão da planilha (H11)"),
          ("aventura", "Gerador de aventuras (aba Aventuras) — Sugestão da planilha (H11)"),
          ("recompensa", "Achados, Cones de Luz e Conjuntos (aba Recompensas) — Sugestão da planilha (H11)"),
          ("mundos", "Planetas, estações, naves, facções e nomes (aba Mundos) — Sugestão da planilha (H11)"),
          ("improviso", "Rumores, eventos, loja e oráculo (aba Improviso) — Sugestão da planilha (H10, H11)")]


def _listas():
    g = D.ganchos()
    L_ = [("faccoes", "Facções", "Livro 27.16", D.faccoes(), None),
          ("locais", "Locais", "Livro 27.17", [x["lugar"] for x in D.locais()], None)]
    for fx in D.FAIXAS:
        L_.append((f"ganchos_{fx.replace('-', '_')}", f"Ganchos {fx}", "Livro 27.18", g[fx], None))
    return L_


def _linhas(r0):
    """Linhas das 8 faixas de vagas a partir de r0 (a 1ª linha é um cabeçalho repetido)."""
    vagas, cabs_ = [], []
    r = r0
    for b in range(8):
        cabs_.append(r)
        r += 1
        for _ in range(FAIXA if b < 7 else VAGAS - 7 * FAIXA):
            vagas.append(r)
            r += 1
    return vagas, cabs_, r - 1


def _dv_texto(ws, cels, tit):
    dv = DataValidation(type="textLength", operator="lessThanOrEqual", formula1="200", allow_blank=True,
                        showErrorMessage=True, errorStyle="warning", errorTitle="Texto longo",
                        error=f"{tit}: até 200 caracteres (o sorteio usa o texto mesmo assim).")
    for c in cels:
        dv.add(c)
    ws.add_data_validation(dv)


def _bloco(ws, r0, titulo_bloco, listas):
    """listas: [(id, título, fonte, valores, segunda | None, sem_ortografia)] — segunda = (título, valores)."""
    ncols = sum(2 if x[4] else 1 for x in listas)
    if ncols > 9:
        raise ValueError(f"aba Tabelas: bloco '{titulo_bloco}' com {ncols} colunas (máximo 9: K:L ficam para o "
                         f"aviso da linha)")
    titulo(ws, r0, titulo_bloco + " — 100 vagas por lista", ate=L(1 + max(ncols, 1)))
    rot(ws, f"A{r0 + 1}", "Apague para trocar, use as vagas vazias para ampliar. Não insira linhas: o contador corrido "
                          "pularia a linha nova.", ate=L(1 + max(ncols, 1)), italico=True)
    cab(ws, f"A{r0 + 2}", "Lista")
    rot(ws, f"A{r0 + 3}", "Fonte", negrito=True)
    rot(ws, f"A{r0 + 4}", "Tamanho da lista", negrito=True)
    rot(ws, f"A{r0 + 5}", "Aviso", negrito=True)
    vagas, cabs_, ultima = _linhas(r0 + 6)
    j = 0
    for id_, tit, fonte, vals, segunda, sem_orto in listas:
        c, cc = L(2 + j), L(N.PRIMEIRA_AUX + j)
        cab(ws, f"{c}{r0 + 2}", tit)
        rot(ws, f"{c}{r0 + 3}", fonte)
        for rc in cabs_:
            cab(ws, f"{c}{rc}", tit)
            N.aux(ws, f"{cc}{rc}", f"={cc}{rc - 1}" if rc != r0 + 6 else "=0")
        for k, rv in enumerate(vagas):
            v = vals[k] if k < len(vals) else None
            cel = N.G.entrada(ws, f"{c}{rv}", v)
            cel.alignment = N.Alignment(vertical="center", wrap_text=True)
            N.aux(ws, f"{cc}{rv}", f"={cc}{rv - 1}+IF(LEN({c}{rv})>0,1,0)")
        _dv_texto(ws, [f"{c}{rv}" for rv in vagas], tit)
        cal(ws, f"{c}{r0 + 4}", f"={cc}{ultima}", nome=f"tab.{id_}.tamanho", centro=True)
        av(ws, f"{c}{r0 + 5}", f"tab.{id_}.aviso",
           f'=IF({cc}{ultima}>={VAGAS},"Lista cheia (100): use Minhas Tabelas para uma lista maior","")')
        N.reg(f"tab.{id_}.valores", ws, f"{c}{vagas[0]}:{c}{ultima}")
        N.reg(f"tab.{id_}.contador", ws, f"{cc}{vagas[0]}:{cc}{ultima}")
        N.MAPA.tabelas[f"tab.{id_}"] = {
            "titulo": tit, "fonte": fonte, "valores": N.MapaMestre.ref("Tabelas", f"{c}{r0 + 6}:{c}{ultima}"),
            "vagas": [f"{c}{x}" for x in vagas], "cabecalhos": [f"{c}{x}" for x in cabs_],
            "auxiliar": N.MapaMestre.ref("Tabelas", f"{cc}{r0 + 6}:{cc}{ultima}"),
            "tamanho": N.MapaMestre.ref("Tabelas", f"{c}{r0 + 4}"), "sem_ortografia": bool(sem_orto),
            "livro": list(vals) if fonte.startswith("Livro") else None, "padrao": list(vals)}
        j += 1
        if segunda:
            tit2, vals2 = segunda
            c2 = L(2 + j)
            cab(ws, f"{c2}{r0 + 2}", tit2)
            rot(ws, f"{c2}{r0 + 3}", fonte)
            for rc in cabs_:
                cab(ws, f"{c2}{rc}", tit2)
            for k, rv in enumerate(vagas):
                v = vals2[k] if k < len(vals2) else None
                cel = N.G.entrada(ws, f"{c2}{rv}", v)
                cel.alignment = N.Alignment(vertical="center", wrap_text=True)
            _dv_texto(ws, [f"{c2}{rv}" for rv in vagas], tit2)
            N.reg(f"tab.{id_}.valores2", ws, f"{c2}{vagas[0]}:{c2}{ultima}")
            N.MAPA.tabelas[f"tab.{id_}"]["segunda"] = [f"{c2}{x}" for x in vagas]
            N.MAPA.tabelas[f"tab.{id_}"]["padrao_segunda"] = list(vals2)
            N.MAPA.tabelas[f"tab.{id_}"]["titulo_segunda"] = tit2
            j += 1
    for rv in vagas + cabs_:
        ws.row_dimensions[rv].height = 15
    return {"linhas_vaga": vagas, "linhas_cab": cabs_, "ultima": ultima}


def montar(wb):
    ws = wb["Tabelas"]
    ws.column_dimensions["A"].width = N.G._px_largura(110)
    for j in range(10):          # B…J listas; K = aviso da linha (camada do Google) com a mesma largura
        ws.column_dimensions[L(2 + j)].width = N.G._px_largura(PX_LISTA)
    ws.column_dimensions["L"].width = N.G._px_largura(60)
    # bloco 1 (Fase 1): listas do livro e ambiente por facção (H8)
    amb = D.AMBIENTE_POR_FACCAO
    b1 = _listas() + [("ambiente_por_faccao", "Facção ou origem (H8)", "Sugestão da planilha (H8)",
                       [f for f, _ in amb], None)]
    info = _bloco(ws, 5, "Listas do livro (editáveis) e ambiente por facção",
                  [(i, t, f, v, s, False) for i, t, f, v, s in b1])
    vagas, cabs_, ultima = info["linhas_vaga"], info["linhas_cab"], info["ultima"]
    col_amb = L(2 + len(b1))
    cab(ws, f"{col_amb}7", "Ambiente (H8)")
    rot(ws, f"{col_amb}8", "Sugestão da planilha — não é regra do livro (H8)")
    N.reg("tabelas.h8.rotulo", ws, f"{col_amb}8")
    N.MAPA.sugestoes.append({"h": "H8", "rotulo": N.MapaMestre.ref("Tabelas", f"{col_amb}8"),
                             "nome": "tabelas.h8.rotulo", "celulas": []})
    for rc in cabs_:
        cab(ws, f"{col_amb}{rc}", "Ambiente (H8)")
    dv = DataValidation(type="list", formula1=N.dlista("ambiente_aleatorio"), allow_blank=True,
                        showErrorMessage=True, errorStyle="warning", errorTitle="Fora da lista",
                        error="Ambiente: escolha um da lista, ou digite um novo (o filtro do Bestiário usa o texto).")
    for k, rv in enumerate(vagas):
        v = amb[k][1] if k < len(amb) else None
        cel = N.G.entrada(ws, f"{col_amb}{rv}", v)
        cel.alignment = N.Alignment(vertical="center", wrap_text=True)
        dv.add(f"{col_amb}{rv}")
    ws.add_data_validation(dv)
    N.reg("tab.ambiente_por_faccao.ambientes", ws, f"{col_amb}{vagas[0]}:{col_amb}{ultima}")
    N.MAPA.tabelas["tab.ambiente_por_faccao"]["ambientes"] = [f"{col_amb}{x}" for x in vagas]
    N.MAPA.tabelas["tab.ambiente_por_faccao"]["padrao_ambientes"] = [a for _, a in amb]
    # blocos 2 a 6 (Fase 2): tabelas de sabor
    SB.conferir()
    por_bloco = {}
    for t in SB.tabelas():
        por_bloco.setdefault(t["bloco"], []).append(t)
    r = ultima + 2
    for id_b, tit_b in BLOCOS:
        ts = por_bloco.pop(id_b)
        # um bloco com mais de 9 colunas se divide em partes (mesma ordem)
        partes, atual, n = [], [], 0
        for t in ts:
            w = 2 if t["segunda"] else 1
            if n + w > 9:
                partes.append(atual)
                atual, n = [], 0
            atual.append(t)
            n += w
        partes.append(atual)
        for k, parte in enumerate(partes):
            info = _bloco(ws, r, tit_b + (f" (parte {k + 1})" if len(partes) > 1 else ""),
                          [(t["id"], t["titulo"], t["fonte"], t["valores"], t["segunda"], t["sem_ortografia"])
                           for t in parte])
            r = info["ultima"] + 2
    if por_bloco:
        raise ValueError(f"aba Tabelas: tabelas de sabor sem bloco: {sorted(por_bloco)}")
    return {"linhas_vaga": vagas, "linhas_cab": cabs_}
