# -*- coding: utf-8 -*-
"""Utilitários das suítes da Mestre: planilha calculada (formulas 1.3.4 via testar_ficha.Modelo), mapa e
entradas por nome lógico, e o grupo do Exemplo."""

import json

import testar_ficha as TF
from mestre import nucleo as N

_MAPA = None
_MODELOS = {}


def mapa():
    global _MAPA
    if _MAPA is None:
        _MAPA = json.loads(N.SAIDA_MAPA.read_text(encoding="utf-8"))
    return _MAPA


def C(nome):
    return mapa()["celulas"][nome]


def modelo(caminho=None):
    caminho = str(caminho or N.SAIDA_MODELO)
    if caminho not in _MODELOS:
        _MODELOS[caminho] = TF.Modelo(caminho)
    return _MODELOS[caminho]


def refs(prefixos):
    return [v for k, v in mapa()["celulas"].items() if k.startswith(tuple(prefixos)) and ":" not in v]


FAIXAS = ("1-4", "5-8", "9-12", "13-16", "17-20")


def digitado(nome, v):
    """O que o mestre escolhe na lista para o valor lógico v: a faixa "9-12" aparece na lista como "Faixa 9-12"
    (o Google leria "9-12" como data — requisito do Google, revisão 2 da ficha). O oráculo continua com "9-12"."""
    fonte = (mapa()["entradas"].get(nome) or {}).get("fonte") or ""
    if isinstance(v, str) and v in FAIXAS and fonte in ("lista.faixas", "lista.filtro_faixa", "lista.faixa_bloco"):
        return f"Faixa {v}"
    return v


def entradas(d):
    """{nome lógico: valor} -> {"'Aba'!A1": valor}."""
    return {C(k): digitado(k, v) for k, v in d.items()}


def calcular(ent_nomes, prefixos=None, saidas=None, caminho=None):
    """Calcula e devolve {nome lógico: valor} para os nomes com os prefixos dados (ou as refs `saidas`)."""
    m = modelo(caminho)
    inv = {v: k for k, v in mapa()["celulas"].items()}
    outs = saidas if saidas is not None else refs(prefixos or [""])
    sol = m.calcular(entradas(ent_nomes), outs)
    return {inv.get(k, k): v for k, v in sol.items()}


def todas_formulas(caminho=None):
    """Refs de todas as células com fórmula das abas (para conferir erros)."""
    import openpyxl
    wb = openpyxl.load_workbook(caminho or N.SAIDA_MODELO)
    saida = []
    for ws in wb.worksheets:
        for linha in ws.iter_rows():
            for c in linha:
                if isinstance(c.value, str) and c.value.startswith("="):
                    saida.append(f"'{ws.title}'!{c.coordinate}")
    return saida


from mestre.aba_combate_base import NC, slot  # noqa: E402,F401  (22 combatentes; condição k do combatente i na C7)


def grupo_exemplo():
    from mestre import exemplo
    return exemplo.grupo()


def entradas_grupo(grupo):
    d = {}
    for i, pj in enumerate(grupo, start=1):
        for k, v in pj.items():
            if v is not None:
                d[f"grupo.pj{i}.{k}"] = v
    return d
