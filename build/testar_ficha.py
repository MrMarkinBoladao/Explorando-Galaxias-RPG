# -*- coding: utf-8 -*-
"""
testar_ficha.py — Bateria de testes da Ficha de Personagem automatizada
("Explorando Galáxias" v1.2, para importar no Google Planilhas).

O QUE ELE FAZ
    Roda suítes independentes contra o .xlsx gerado por `build/gerar_ficha.py`
    (ficha-automatizada/Ficha Automatizada - Explorando Galáxias V1.2.xlsx e a
    Ficha Exemplo - Nadir.xlsx),
    contra os capítulos .md do livro (fonte de verdade) e contra o oráculo
    Python independente (`build/oraculo_ficha.py`). As fórmulas da planilha
    são CALCULADAS de verdade com a biblioteca `formulas` (nunca se valida
    lendo o texto da fórmula). Sai com código 1 em qualquer falha.

    Suítes:
      spike      compatibilidade da biblioteca `formulas` com a lista branca
                 de funções e com nomes de aba com espaço e acento; grava
                 build/ficha_funcoes_ok.json (lista efetiva + veredito).
      protegidos SHA-256 do livro (livro-v1.0/ — nome histórico da pasta, o
                 conteúdo é a v1.2 —, .docx/.pdf V1.2, gerar_docx.py,
                 gerar_pdf.py): grava build/ficha_protegidos.json na primeira
                 vez e compara nas seguintes. Os .docx/.pdf V1.0 ficam na raiz
                 como registro, fora da lista.
      dados      parser PRÓPRIO deste arquivo relê os .md e compara, célula a
                 célula, com a aba Dados; confere as âncoras do módulo
                 transcrito de build/ficha_dados.py.
      ouro       números de ouro impressos no livro (casos a–m), no oráculo e
                 na PLANILHA calculada (entradas lógicas -> células do mapa).
                 Com --so-oraculo, só o oráculo é conferido (sem planilha).
      oraculo    teste diferencial planilha × oráculo: matriz 7 Raças × 9 Caminhos ×
                 níveis {1, 20} (cenários válidos por semente fixa), 3 varreduras
                 1->20 e casos-limite; ~45+ saídas por caso e avisos nos dois
                 sentidos (código do oráculo <-> célula de aviso). Meta: zero.
      extremos   calcula TODAS as células com fórmula na ficha em branco, em
                 estados parciais (só Raça, só Caminho, um campo por vez com
                 valor válido e inválido), em entradas inválidas (com o aviso
                 esperado na coluna certa) e em fichas completas: nenhum valor
                 de erro; ficha em branco sem aviso. Os cenários rodam em
                 paralelo (até 8 processos, cada um carrega a planilha uma vez).
      lint       compatibilidade Google Planilhas de toda fórmula, validação e
                 formatação condicional, fontes, proteção, nomes definidos; layout
                 da Em Jogo (A:L <= 1360 px, Resumo em A1, tela nas linhas 1-40).
      texto      texto visível (valores, literais de fórmula, validações, nomes de
                 aba): 25 strings proibidas + termos aposentados de 30.2, grafia
                 do glossário 30.1, ortografia pelo léxico (livro +
                 build/ficha_lexico_extra.txt) e formas sem acento.
      preview    build/renderizar_ficha.py desenha as 10 abas em PNG em 3 estados
                 (.agents/tasks/ficha-preview/), falha com texto cortado e confere
                 a Em Jogo dentro de 1360 × 768 px.
      tudo       todas as anteriores.

COMO USAR
    $env:PYTHONUTF8="1"; python "build\\testar_ficha.py" --suite spike
    $env:PYTHONUTF8="1"; python "build\\testar_ficha.py" --suite ouro --so-oraculo
    $env:PYTHONUTF8="1"; python "build\\testar_ficha.py" --suite tudo

REQUISITOS
    Python 3, openpyxl 3.1.5, formulas 1.3.4, pillow 12.1.0 — versões exatas em
    build/requirements-ficha.txt.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BUILD = RAIZ / "build"
LIVRO = RAIZ / "livro-v1.0"          # nome histórico: o conteúdo é a v1.2 (00-changelog-v11-para-v12.md)
ENTREGA = RAIZ / "ficha-automatizada"
XLSX = ENTREGA / "Ficha Automatizada - Explorando Galáxias V1.2.xlsx"
XLSX_NADIR = ENTREGA / "Ficha Exemplo - Nadir.xlsx"
MAPA_JSON = BUILD / "ficha_mapa.json"
FUNCOES_OK_JSON = BUILD / "ficha_funcoes_ok.json"
PROTEGIDOS_JSON = BUILD / "ficha_protegidos.json"

ABAS_ESPERADAS = ["Início", "Criação", "Em Jogo", "Testes", "Habilidades",
                  "Caminho", "Equipamento", "Progressão", "Regras Rápidas", "Dados"]

LISTA_BRANCA = ["IF", "IFERROR", "AND", "OR", "NOT", "SUM", "SUMIF", "SUMPRODUCT",
                "COUNTIF", "COUNTIFS", "COUNTA", "COUNTBLANK", "INDEX", "MATCH",
                "VLOOKUP", "HLOOKUP", "CHOOSE", "MIN", "MAX", "ROUNDUP", "ROUND",
                "INT", "MOD", "ABS", "LEN", "TRIM", "CONCATENATE", "REPT",
                "ISBLANK", "ISNUMBER", "ISERROR", "ROWS", "LARGE", "SMALL"]

PROIBIDAS = ["LET", "LAMBDA", "XLOOKUP", "FILTER", "UNIQUE", "SORT", "SEQUENCE",
             "TEXTJOIN", "IFS", "SWITCH", "ARRAYFORMULA", "QUERY", "IMPORTRANGE",
             "TEXT", "INDIRECT", "OFFSET", "ROUNDDOWN"]


# ---------------------------------------------------------------------------
# Infraestrutura
# ---------------------------------------------------------------------------

class Resultado:
    """Acumula falhas e informações de uma suíte."""

    def __init__(self, nome):
        self.nome = nome
        self.falhas = []
        self.infos = []
        self.checagens = 0

    def ok(self, condicao, mensagem):
        self.checagens += 1
        if not condicao:
            self.falhas.append(mensagem)
        return condicao

    def falha(self, mensagem):
        self.checagens += 1
        self.falhas.append(mensagem)

    def info(self, mensagem):
        self.infos.append(mensagem)

    def imprimir(self):
        situacao = "OK" if not self.falhas else "FALHOU"
        print(f"\n=== Suíte {self.nome}: {situacao} — {self.checagens} checagens, "
              f"{len(self.falhas)} falha(s)")
        for i in self.infos:
            print("  ·", i)
        for f in self.falhas[:200]:
            print("  ✗", f)
        if len(self.falhas) > 200:
            print(f"  … mais {len(self.falhas) - 200} falha(s)")


def normalizar_valor(v):
    """Converte o valor devolvido pela `formulas` para tipo Python simples."""
    import numpy as np
    import schedula as sh
    if hasattr(v, "value"):
        v = v.value
    if isinstance(v, np.ndarray):
        if v.size == 1:
            v = v.reshape(-1)[0]
        else:
            return [normalizar_valor(x) for x in v.reshape(-1)]
    if v is sh.EMPTY:
        return None
    if type(v).__name__ == "XlError":
        return str(v)
    if isinstance(v, np.generic):
        v = v.item()
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def eh_erro(v):
    return isinstance(v, str) and v in ("#N/A", "#VALUE!", "#REF!", "#DIV/0!",
                                        "#NAME?", "#NUM!", "#NULL!")


def separar_ref(ref):
    """'Em Jogo'!A1 -> ('Em Jogo', 'A1')."""
    aba, cel = ref.rsplit("!", 1)
    aba = aba.strip("'")
    return aba, cel.replace("$", "").upper()


class Modelo:
    """Carrega o .xlsx uma vez com `formulas` e calcula cenários por inputs."""

    def __init__(self, caminho):
        import formulas
        self.caminho = Path(caminho)
        t0 = time.time()
        self.modelo = formulas.ExcelModel().loads(str(self.caminho)).finish()
        self.tempo_carga = time.time() - t0
        self._chaves = {k.upper(): k for k in self.modelo.cells}

    def chave(self, ref):
        aba, cel = separar_ref(ref)
        bruta = f"'[{self.caminho.name}]{aba}'!{cel}".upper()
        return self._chaves.get(bruta, f"'[{self.caminho.name}]{aba.upper()}'!{cel}")

    def calcular(self, entradas=None, saidas=None):
        """entradas: {"'Aba'!A1": valor (None = célula vazia)}; saidas: lista de refs.
        Devolve {ref: valor normalizado}."""
        ins = {}
        for ref, v in (entradas or {}).items():
            # None = célula vazia: omite a entrada (toda entrada sai vazia no .xlsx)
            if v is not None:
                ins[self.chave(ref)] = v
        outs = None
        if saidas is not None:
            outs = [self.chave(r) for r in saidas if self.chave(r) in self.modelo.cells]
        if outs == []:
            sol = {}
        elif outs is not None and len(outs) <= 60:
            # Revisão 2: com o contador de erros da Início, todo dispatch da `formulas` custa uns
            # 2 s mesmo para uma saída só. Para poucas saídas, o grafo reduzido às entradas e
            # saídas pedidas (shrink_dsp, guardado por chaves de entrada + saídas) dá o mesmo
            # resultado em centésimos; para muitas saídas, reduzir custa mais que calcular tudo.
            chave_ = (frozenset(ins), tuple(outs))
            cache = self.__dict__.setdefault("_reduzidos", {})
            if chave_ not in cache:
                if len(cache) > 256:
                    cache.clear()
                cache[chave_] = self.modelo.dsp.shrink_dsp(inputs=list(ins), outputs=outs)
            sol = cache[chave_].dispatch(inputs=ins, outputs=outs)
        elif outs is not None:
            sol = self.modelo.calculate(inputs=ins, outputs=outs)
        elif ins:
            sol = self.modelo.calculate(inputs=ins)
        else:
            sol = self.modelo.calculate()
        resultado = {}
        alvo = saidas if saidas is not None else None
        if alvo is None:
            for k, v in sol.items():
                resultado[k] = normalizar_valor(v)
            return resultado
        for r in alvo:
            k = self.chave(r)
            resultado[r] = normalizar_valor(sol[k]) if k in sol else None
        return resultado


def ler_mapa():
    if not MAPA_JSON.exists():
        return None
    return json.loads(MAPA_JSON.read_text(encoding="utf-8"))


def ler_funcoes_ok():
    if not FUNCOES_OK_JSON.exists():
        return None
    return json.loads(FUNCOES_OK_JSON.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Suíte spike
# ---------------------------------------------------------------------------

def suite_spike(args):
    import openpyxl
    r = Resultado("spike")
    pasta = Path(tempfile.mkdtemp(prefix="spike_ficha_"))
    arq = pasta / "Spike Ficha.xlsx"
    try:
        wb = openpyxl.Workbook()
        cr = wb.active
        cr.title = "Criação"
        ej = wb.create_sheet("Em Jogo")
        rr = wb.create_sheet("Regras Rápidas")
        da = wb.create_sheet("Dados")
        # Entradas
        cr["A1"] = 5
        cr["A2"] = "Humano"
        # A3 fica vazia de propósito
        cr["A4"] = -7
        cr["A5"] = 3.7
        cr["A6"] = "Vulpes"
        cr["A7"] = 12
        cr["A8"] = 15
        cr["B1"] = "Leve"
        cr["B2"] = "Pesada"
        cr["B3"] = "Média"
        rr["A1"] = 4
        for i, (n, v) in enumerate([("Humano", 1), ("Vulpes", 2), ("Intellitron", 3)], 1):
            da.cell(i, 1, n)
            da.cell(i, 2, v)
        for j, (n, v) in enumerate([("a", 10), ("b", 20), ("c", 30)], 4):
            da.cell(1, j, n)
            da.cell(2, j, v)
        C = "'Criação'!"
        casos = [
            # (funções testadas, fórmula, esperado)
            (["IF"], f'=IF({C}A1>3,"sim","não")', "sim"),
            (["IF"], f'=IF({C}A3="","",{C}A3*2)', ""),
            (["IFERROR"], '=IFERROR(1/0,"x")', "x"),
            (["IFERROR", "MATCH"], f'=IFERROR(MATCH("Zé",Dados!A1:A3,0),"nao")', "nao"),
            (["AND"], f"=AND({C}A1>1,{C}A7=12)", True),
            (["OR"], f"=OR(FALSE,{C}A1=5)", True),
            (["NOT"], f"=NOT({C}A1=5)", False),
            (["SUM"], f"=SUM({C}A1,{C}A7,{C}A3)", 17),
            (["SUM"], f"=SUM({C}A1:A3)", 5),
            (["SUMIF"], '=SUMIF(Dados!A1:A3,"Vulpes",Dados!B1:B3)', 2),
            (["SUMPRODUCT", "LEN"], "=SUMPRODUCT((LEN(Dados!A1:A3)>6)*1)", 1),
            (["SUMPRODUCT"], "=SUMPRODUCT(Dados!B1:B3,Dados!B1:B3)", 14),
            (["SUMPRODUCT", "LEN"], f"=SUMPRODUCT((LEN({C}A1:A3)>0)*1)", 2),
            (["SUMPRODUCT"], f'=SUMPRODUCT(({C}B1:B3="Média")*1)', 1),
            (["COUNTIF"], '=COUNTIF(Dados!A1:A3,"Humano")', 1),
            (["COUNTIF"], '=COUNTIF(Dados!A1:A3,"humano")', 1),
            (["COUNTIF"], f'=COUNTIF({C}A7:A8,">=12")', 2),
            (["COUNTIF"], f"=COUNTIF({C}A7:A8,{C}A1+7)", 1),
            (["COUNTIF"], '=COUNTIF(Dados!A1:A3,"?*")', 3),
            (["COUNTIFS"], '=COUNTIFS(Dados!A1:A3,"<>Humano",Dados!B1:B3,">1")', 2),
            (["COUNTA"], f"=COUNTA({C}A1:A3)", 2),
            (["COUNTBLANK"], f"=COUNTBLANK({C}A1:A3)", 1),
            (["INDEX"], "=INDEX(Dados!B1:B3,2)", 2),
            (["INDEX"], "=INDEX(Dados!A1:B3,3,2)", 3),
            (["MATCH"], '=MATCH("Intellitron",Dados!A1:A3,0)', 3),
            (["INDEX", "MATCH"], f"=INDEX(Dados!B1:B3,MATCH({C}A6,Dados!A1:A3,0))", 2),
            (["VLOOKUP"], '=VLOOKUP("Intellitron",Dados!A1:B3,2,FALSE)', 3),
            (["HLOOKUP"], '=HLOOKUP("b",Dados!D1:F2,2,FALSE)', 20),
            (["CHOOSE"], '=CHOOSE(2,"x","y","z")', "y"),
            (["MIN"], f"=MIN({C}A1,{C}A4)", -7),
            (["MIN"], f"=MIN({C}A3,{C}A1)", 5),
            (["MAX"], f"=MAX({C}A1,{C}A4)", 5),
            (["MAX"], f"=MAX(2,MIN(7,{C}A7))", 7),
            (["ROUNDUP"], f"=ROUNDUP({C}A5,0)", 4),
            (["ROUNDUP"], "=ROUNDUP(-3.2,0)", -4),
            (["ROUND"], "=ROUND(2.5,0)", 3),
            (["ROUND"], "=ROUND(-2.5,0)", -3),
            (["INT"], "=INT(-3.5)", -4),
            (["INT"], "=INT(7/2)", 3),
            (["INT"], f"=INT(({C}A8-15)/2)+3", 3),
            (["MOD"], "=MOD(-7,3)", 2),
            (["ABS"], f"=ABS({C}A4)", 7),
            (["LEN"], f"=LEN({C}A2)", 6),
            (["LEN"], f"=LEN({C}A3)", 0),
            (["TRIM"], '=TRIM("  a  b ")', "a b"),
            (["TRIM"], '=TRIM("  ab ")', "ab"),
            (["CONCATENATE"], f'=CONCATENATE("PV ",{C}A1)', "PV 5"),
            (["REPT"], '=REPT("*",3)', "***"),
            (["ISBLANK"], f"=ISBLANK({C}A3)", True),
            (["ISBLANK"], f"=ISBLANK({C}A1)", False),
            (["ISNUMBER"], f"=ISNUMBER({C}A2)", False),
            (["ISNUMBER"], f"=ISNUMBER({C}A1)", True),
            (["ISERROR"], "=ISERROR(1/0)", True),
            (["ROWS"], "=ROWS(Dados!A1:A3)", 3),
            (["LARGE"], "=LARGE(Dados!B1:B3,1)", 3),
            (["SMALL"], "=SMALL(Dados!B1:B3,1)", 1),
            (["&"], f'="d20+"&{C}A1', "d20+5"),
            (["&"], f'="d20+"&({C}A1+1)', "d20+6"),
            (["&", "INT"], '="média "&INT(5*(10+1)/2)', "média 27"),
            (["&", "IF"], f'=IF({C}A4>=0,"+"&{C}A4,{C}A4)', -7),
            (["&", "IF"], f'=IF({C}A1>=0,"+"&{C}A1,""&{C}A1)', "+5"),
            (["&"], f'=""&{C}A4', "-7"),
            # Célula vazia em conta e em comparação
            (["vazio"], f"={C}A3+1", 1),
            (["vazio"], f'={C}A3=""', True),
            (["vazio"], f"={C}A3=0", True),
            (["vazio"], f'=IF({C}A3="","vazio","cheio")', "vazio"),
            # Comparação de texto sem caixa
            (["texto"], f'={C}A2="humano"', True),
            # Aba com espaço e acento (referência e cálculo encadeado)
            (["acento"], "='Regras Rápidas'!A1*2", 8),
            (["acento"], f"={C}A1+'Regras Rápidas'!A1", 9),
            (["acento", "COUNTIF"], f'=COUNTIF({C}B1:B3,"Média")', 1),
        ]
        # Comportamentos documentados (não decidem a lista; viram regra do lint/projeto)
        comportamentos = [
            ("duplo menos unário (--)", f"=SUMPRODUCT(--(LEN({C}A1:A3)>0))", 2),
            ("COUNTIF \"?*\" em intervalo com número e texto",
             f'=COUNTIF({C}A1:A3,"?*")', 1),
            ("TRIM com espaço duplo interno", '=TRIM("a  b")', "a b"),
            ("divisão por zero sem proteção", "=1/0", "#DIV/0!"),
            ("MATCH sem achado", '=MATCH("Zé",Dados!A1:A3,0)', "#N/A"),
            # revisão 2 (Google real): texto vazio em conta, referência a célula vazia, ISBLANK("")
            ('texto vazio em conta (""+1)', '=""+1', "#VALUE!"),
            ("referência a célula vazia (=A3)", f"={C}A3", ""),
            ('ISBLANK("") (texto vazio não é célula vazia)', '=ISBLANK("")', False),
        ]
        # Revisão 2: a camada de leitura protegida e o contador de erros precisam se comportar
        # como no Google (vazio explícito, erro vira vazio, ISERROR conta a célula com erro)
        camada = [
            ("leitura protegida de célula vazia", f'=IF(ISERROR({C}A3),"",IF(ISBLANK({C}A3),"",{C}A3))', "", None),
            ("leitura protegida de número", f'=IF(ISERROR({C}A1),"",IF(ISBLANK({C}A1),"",{C}A1))', 5, None),
            ("leitura protegida de texto", f'=IF(ISERROR({C}A2),"",IF(ISBLANK({C}A2),"",{C}A2))', "Humano", None),
            ("leitura protegida de entrada com erro", f'=IF(ISERROR({C}A2),"",IF(ISBLANK({C}A2),"",{C}A2))', "",
             "#VALUE!"),
            ("contador sem erro", f"=SUMPRODUCT(ISERROR({C}A1:B8)*1)", 0, None),
            ("contador com uma entrada em erro", f"=SUMPRODUCT(ISERROR({C}A1:B8)*1)", 1, "#VALUE!"),
            ("contador com #N/A", f"=SUMPRODUCT(ISERROR({C}A1:B8)*1)", 1, "#N/A"),
            ("sinal de erro da linha", f"=ISERROR({C}A2)*1+ISERROR({C}B2)*1", 1, "#N/A"),
            ("vazio da camada em ISNUMBER", f'=ISNUMBER(IF(ISBLANK({C}A3),"",{C}A3))', False, None),
        ]
        refs_camada = []
        for i, (_, formula, _, _) in enumerate(camada, 1):
            ej.cell(i, 5, formula)
            refs_camada.append(f"'Em Jogo'!E{i}")
        refs = []
        for i, (_, formula, _) in enumerate(casos, 1):
            ej.cell(i, 1, formula)
            refs.append(f"'Em Jogo'!A{i}")
        refs_comp = []
        for i, (_, formula, _) in enumerate(comportamentos, 1):
            ej.cell(i, 3, formula)
            refs_comp.append(f"'Em Jogo'!C{i}")
        por_formula = {formula: ref for (_, formula, _), ref in zip(casos, refs)}
        ref_index = por_formula["=INDEX(Dados!B1:B3,2)"]
        # Encadeamento entre abas: Regras Rápidas lê Em Jogo
        rr["B1"] = f"={ref_index}*10"     # INDEX(Dados!B1:B3,2) = 2 -> 20
        wb.save(arq)

        modelo = Modelo(arq)
        r.info(f"carga do modelo: {modelo.tempo_carga:.2f} s")
        t0 = time.time()
        res = modelo.calcular(saidas=refs + ["'Regras Rápidas'!B1"])
        t_calc = time.time() - t0
        r.info(f"calculate (todas as saídas): {t_calc:.4f} s")

        aprovadas, reprovadas = {}, {}
        for (funcs, formula, esperado), ref in zip(casos, refs):
            obtido = res.get(ref)
            ok = _igual(obtido, esperado)
            for f in funcs:
                aprovadas.setdefault(f, True)
                if not ok:
                    aprovadas[f] = False
                    reprovadas.setdefault(f, []).append(
                        f"{formula} → obtido {obtido!r}, esperado {esperado!r}")
        ok_cadeia = _igual(res.get("'Regras Rápidas'!B1"), 20)
        aprovadas["acento"] = aprovadas.get("acento", True) and ok_cadeia
        if not ok_cadeia:
            reprovadas.setdefault("acento", []).append(
                f"{ref_index}*10 → {res.get(chr(39) + 'Regras Rápidas' + chr(39) + '!B1')!r}")

        # Cenário por inputs: muda entradas e confere propagação (inclusive vazio)
        esperado_cenario = {
            f'=IF({C}A1>3,"sim","não")': "sim",
            f"=COUNTA({C}A1:A3)": 3,
            f"=COUNTBLANK({C}A1:A3)": 0,
            f"=SUM({C}A1:A3)": 13,
            f"={C}A3+1": 5,
            f'=IF({C}A3="","vazio","cheio")': "cheio",
            f"=LEN({C}A2)": 6,
            f'="d20+"&({C}A1+1)': "d20+10",
        }
        saidas_cen = [por_formula[f] for f in esperado_cenario]
        t0 = time.time()
        res2 = modelo.calcular(entradas={f"{C}A1": 9, f"{C}A3": 4}, saidas=saidas_cen)
        t_calc2 = time.time() - t0
        r.info(f"calculate (cenário com 3 entradas, {len(saidas_cen)} saídas): {t_calc2:.4f} s")
        for f, esp in esperado_cenario.items():
            r.ok(_igual(res2[por_formula[f]], esp),
                 f"cenário por inputs: {f} → {res2[por_formula[f]]!r}, esperado {esp!r}")
        # o modelo volta ao estado original depois do cenário
        res3 = modelo.calcular(saidas=[por_formula[f"=SUM({C}A1:A3)"]])
        r.ok(_igual(res3[por_formula[f"=SUM({C}A1:A3)"]], 5),
             "cenário contaminou o cálculo seguinte (estado não volta ao original)")
        # None = "deixar vazia": a entrada é omitida e vale o vazio do arquivo
        res4 = modelo.calcular(entradas={f"{C}A3": None},
                               saidas=[por_formula[f"={C}A3+1"]])
        r.ok(_igual(res4[por_formula[f"={C}A3+1"]], 1),
             "entrada None não reproduziu a célula vazia do arquivo")

        # Comportamentos documentados
        res_comp = modelo.calcular(saidas=refs_comp)
        comp_json = []
        for (desc, formula, google), ref in zip(comportamentos, refs_comp):
            obtido = res_comp.get(ref)
            igual = _igual(obtido, google)
            comp_json.append({"caso": desc, "formula": formula, "google": google,
                              "formulas_1_3_4": obtido, "igual_ao_google": igual})
            r.info(f"comportamento — {desc}: formulas={obtido!r}, Google={google!r}"
                   f"{'' if igual else '  (DIVERGE)'}")

        # Revisão 2: camada de leitura protegida e contador (com erro injetado como input)
        from formulas.functions import Error as _Erro
        for (desc, formula, esperado, erro), ref in zip(camada, refs_camada):
            ins = {f"{C}A2": _Erro.errors[erro]} if erro else {}
            obtido = modelo.calcular(entradas=ins, saidas=[ref])[ref]
            r.ok(_igual("" if obtido is None else obtido, esperado),
                 f"revisão 2 — {desc}: {formula} (A2 = {erro or 'Humano'}) → {obtido!r}, esperado {esperado!r}")
        r.info(f"revisão 2: {len(camada)} checagens da leitura protegida e do contador de erros")

        for f, msgs in reprovadas.items():
            for m in msgs:
                r.info(f"REPROVADA [{f}] {m}")
        efetiva = [f for f in LISTA_BRANCA if aprovadas.get(f, False)]
        nao_testadas = [f for f in LISTA_BRANCA if f not in aprovadas]
        for f in nao_testadas:
            r.falha(f"função da lista branca sem caso no spike: {f}")
        for f in ("&", "vazio", "texto"):
            r.ok(aprovadas.get(f, False), f"comportamento básico reprovado: {f}")
        veredito_acento = "ok" if aprovadas.get("acento") else "falhou"
        observacoes = [
            "Duplo menos unário (--) devolve 0 na formulas 1.3.4: contar condição com "
            "SUMPRODUCT((condição)*1); o lint proíbe '--'.",
            "COUNTIF(intervalo,\"?*\") na formulas 1.3.4 conta também NÚMEROS (o Google "
            "conta só texto): usar \"?*\" só em intervalo de texto, ou "
            "SUMPRODUCT((LEN(intervalo)>0)*1).",
            "TRIM da formulas 1.3.4 não reduz espaço duplo interno: TRIM sai da lista "
            "efetiva (não é necessário na ficha).",
            "Entrada em cenário: só VALOR. 'Deixar vazia' = omitir a entrada (Modelo.calcular "
            "trata None assim); por isso TODA célula de entrada deve sair VAZIA no .xlsx "
            "gerado. schedula.EMPTY como input não reproduz célula vazia.",
            "Célula vazia que nenhuma fórmula referencia isoladamente não vira nó em "
            "model.cells, mas aceita input normalmente (o utilitário não filtra).",
            "Chave da formulas: \"'[Nome Do Arquivo.xlsx]ABA'!A1\" — o nome do arquivo "
            "mantém a caixa original e só a aba vai em maiúsculas; Modelo.chave() resolve "
            "sem diferenciar caixa.",
            "Número concatenado com & sai sem '.0' (\"d20+\"&(A1+1) = \"d20+6\").",
            "Revisão 2: referência a célula vazia (=A3) devolve vazio no Google e 0 no Excel e na "
            "formulas. A ficha não depende disso: toda entrada é lida pela camada de leitura protegida "
            "(IF(ISERROR(X),\"\",IF(ISBLANK(X),\"\",X))) e o lint proíbe ler uma entrada fora dela.",
            "Revisão 2: \"\"+1 dá #VALUE! (Google e formulas): o vazio da camada só entra em conta "
            "depois de ISNUMBER/LEN.",
        ]
        saida = {
            "gerado_por": "build/testar_ficha.py --suite spike",
            "biblioteca": "formulas 1.3.4",
            "funcoes": efetiva,
            "operadores": ["&", "+", "-", "*", "/", "=", "<>", "<", ">", "<=", ">="],
            "operadores_proibidos": ["--"],
            "reprovadas": reprovadas,
            "comportamentos": comp_json,
            "acento_em_nome_de_aba": veredito_acento,
            "abas_testadas": ["Criação", "Em Jogo", "Regras Rápidas", "Dados"],
            "tempo_carga_s": round(modelo.tempo_carga, 3),
            "tempo_calculate_s": round(t_calc, 4),
            "tempo_calculate_cenario_s": round(t_calc2, 4),
            "observacoes": observacoes,
        }
        FUNCOES_OK_JSON.write_text(json.dumps(saida, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
        r.info(f"lista efetiva ({len(efetiva)}): {', '.join(efetiva)} + operador &")
        r.info(f"veredito acento em nome de aba: {veredito_acento}")
        r.info(f"gravado {FUNCOES_OK_JSON}")
    finally:
        shutil.rmtree(pasta, ignore_errors=True)
    r.ok(not pasta.exists(), f"temporário não foi apagado: {pasta}")
    return r


def _igual(obtido, esperado):
    if isinstance(esperado, bool):
        return obtido is esperado or obtido == esperado and isinstance(obtido, bool)
    if isinstance(esperado, (int, float)) and not isinstance(esperado, bool):
        return isinstance(obtido, (int, float)) and not isinstance(obtido, bool) \
            and abs(obtido - esperado) < 1e-9
    return obtido == esperado


# ---------------------------------------------------------------------------
# Suíte protegidos
# ---------------------------------------------------------------------------

def _arquivos_protegidos():
    arquivos = sorted(p for p in LIVRO.rglob("*") if p.is_file())
    arquivos += [RAIZ / "Sistema de HSR by MC Filhos V1.2.docx",
                 RAIZ / "Sistema de HSR by MC Filhos V1.2.pdf",
                 BUILD / "gerar_docx.py",
                 BUILD / "gerar_pdf.py"]
    return arquivos


def _sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def suite_protegidos(args):
    r = Resultado("protegidos")
    atuais = {}
    for p in _arquivos_protegidos():
        rel = p.relative_to(RAIZ).as_posix()
        if not p.exists():
            r.falha(f"arquivo protegido ausente: {rel}")
            continue
        atuais[rel] = _sha256(p)
    if not PROTEGIDOS_JSON.exists():
        PROTEGIDOS_JSON.write_text(json.dumps(
            {"gerado_por": "build/testar_ficha.py --suite protegidos",
             "sha256": atuais}, ensure_ascii=False, indent=2), encoding="utf-8")
        r.info(f"primeira execução: gravados {len(atuais)} hashes em {PROTEGIDOS_JSON}")
        r.ok(True, "")
        return r
    gravados = json.loads(PROTEGIDOS_JSON.read_text(encoding="utf-8"))["sha256"]
    for rel, h in gravados.items():
        if rel not in atuais:
            r.falha(f"arquivo protegido sumiu: {rel}")
        else:
            r.ok(atuais[rel] == h, f"arquivo protegido ALTERADO: {rel}")
    for rel in atuais:
        r.ok(rel in gravados, f"arquivo novo em área protegida: {rel}")
    r.info(f"{len(gravados)} arquivos conferidos")
    return r


# ---------------------------------------------------------------------------
# Suíte lint
# ---------------------------------------------------------------------------

def _tem_emoji(s):
    for ch in s:
        o = ord(ch)
        if o > 0xFFFF or 0x2600 <= o <= 0x27BF or 0x1F000 <= o or \
                unicodedata.category(ch) == "So":
            return True
    return False


def _checar_formula(r, texto, onde, permitidas, permite_exclamacao=True):
    """Confere uma fórmula pelos tokens do openpyxl.formula.Tokenizer."""
    from openpyxl.formula import Tokenizer
    try:
        tok = Tokenizer(texto if texto.startswith("=") else "=" + texto)
    except Exception as e:
        r.falha(f"{onde}: fórmula que o Tokenizer não entende ({e}): {texto}")
        return
    fora_de_texto = []
    for t in tok.items:
        if t.type == "OPERAND" and t.subtype == "TEXT":
            continue
        fora_de_texto.append(t.value)
        if t.type == "FUNC" and t.subtype == "OPEN":
            nome = t.value[:-1].upper().replace("_XLFN.", "").replace("_XLWS.", "")
            if nome in PROIBIDAS or nome.startswith("REGEX"):
                r.falha(f"{onde}: função PROIBIDA {nome}: {texto}")
            elif nome not in permitidas:
                r.falha(f"{onde}: função fora da lista efetiva {nome}: {texto}")
        if t.type == "OPERAND" and t.subtype == "RANGE" and "[" in t.value:
            r.falha(f"{onde}: link externo ou referência estruturada '[': {texto}")
    resto = "".join(fora_de_texto)
    r.ok(";" not in resto, f"{onde}: ';' fora de string: {texto}")
    r.ok(not re.search(r"-\s*-", resto), f"{onde}: duplo menos unário '--' (formulas devolve 0): {texto}")
    if not permite_exclamacao:
        r.ok("!" not in resto, f"{onde}: referência a outra aba ('!') em CF/validação personalizada: {texto}")


# --- Revisão 2: riscos de digitação no Google e leitura protegida das entradas --------------

_RE_REF_T = re.compile(r"^(?:(?P<aba>'(?:[^']|'')+'|[^'!]+)!)?(?P<c1>\$?[A-Z]{1,3}\$?\d+)"
                       r"(?::(?P<c2>\$?[A-Z]{1,3}\$?\d+))?$")


def _intervalos_da_formula(texto, aba):
    """[(aba, linha0, col0, linha1, col1)] de cada referência da fórmula (implementação do teste)."""
    from openpyxl.formula import Tokenizer
    from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
    saida = []
    for t in Tokenizer(texto if texto.startswith("=") else "=" + texto).items:
        if t.type != "OPERAND" or t.subtype != "RANGE":
            continue
        m = _RE_REF_T.match(t.value)
        if not m:
            continue
        a = m.group("aba").strip("'").replace("''", "'") if m.group("aba") else aba
        l1, r1 = coordinate_from_string(m.group("c1").replace("$", ""))
        l2, r2 = coordinate_from_string((m.group("c2") or m.group("c1")).replace("$", ""))
        c1, c2 = column_index_from_string(l1), column_index_from_string(l2)
        saida.append((a, min(r1, r2), min(c1, c2), max(r1, r2), max(c1, c2)))
    return saida


def risco_google(v):
    """Motivo pelo qual o Google NÃO leria a opção de lista `v` como o texto que ela é (ou None).
    Número de verdade (int/float) é aceito: a lista numérica tem de vir de célula com número."""
    if v is None or isinstance(v, bool):
        return None if v is None else "booleano"
    if isinstance(v, (int, float)):
        return None
    s = str(v)
    if not s:
        return None
    if s[0] in "=+-@":
        return f"começa com {s[0]!r} (o Google lê como fórmula)"
    t = s.strip()
    if t.upper() in ("VERDADEIRO", "FALSO", "TRUE", "FALSE"):
        return "vira booleano"
    if re.fullmatch(r"\d{1,4}\s*[-/.]\s*\d{1,2}(\s*[-/.]\s*\d{1,4})?", t):
        return "parece data"
    if re.fullmatch(r"\d{1,2}:\d{2}(:\d{2})?(\s*[AaPp][Mm])?", t):
        return "parece hora"
    if re.fullmatch(r"[-+]?(\d+[.,]?\d*|[.,]\d+)\s*%?", t) or re.fullmatch(r"R?\$\s*\d+([.,]\d+)?", t):
        return "parece número (texto que o Google converte)"
    return None


def _opcoes_da_validacao(wb, ws, formula1):
    """Valores que a lista suspensa pode oferecer: literal "a,b", intervalo da aba Dados ou
    intervalo local (inclusive das listas dependentes: os textos literais das fórmulas
    auxiliares e todas as células da aba Dados que elas leem — um superconjunto)."""
    f = (formula1 or "").strip()
    if f.startswith('"'):
        return [x for x in f.strip('"').split(",")]
    vistos, valores = set(), []

    def celula(aba, r_, c_, prof=0):
        if (aba, r_, c_) in vistos or aba not in wb.sheetnames:
            return
        vistos.add((aba, r_, c_))
        v = wb[aba].cell(r_, c_).value
        if isinstance(v, str) and v.startswith("="):
            if prof > 3:
                return
            from openpyxl.formula import Tokenizer
            for t in Tokenizer(v).items:
                if t.type == "OPERAND" and t.subtype == "TEXT":
                    valores.append(t.value[1:-1].replace('""', '"'))
            for a, r0, c0, r1, c1 in _intervalos_da_formula(v, aba):
                if a == "Dados" or (r1 - r0 + 1) * (c1 - c0 + 1) <= 60:
                    for rr in range(r0, r1 + 1):
                        for cc in range(c0, c1 + 1):
                            celula(a, rr, cc, prof + 1)
        elif type(v).__name__ != "ArrayFormula":
            valores.append(v)

    for a, r0, c0, r1, c1 in _intervalos_da_formula(f, ws.title):
        for rr in range(r0, r1 + 1):
            for cc in range(c0, c1 + 1):
                celula(a, rr, cc)
    return valores


def _lint_google(r, wb):
    """(1) Nenhuma opção de lista suspensa que o Google leia como fórmula, data, hora, número ou
    booleano. (2) Nenhuma fórmula lê uma entrada fora da camada de leitura protegida."""
    mapa = ler_mapa() or {}
    n_opcoes = n_listas = 0
    for ws in wb.worksheets:
        for dv in ws.data_validations.dataValidation:
            if dv.type != "list":
                continue
            n_listas += 1
            for v in _opcoes_da_validacao(wb, ws, dv.formula1):
                n_opcoes += 1
                motivo = risco_google(v)
                r.ok(motivo is None, f"'{ws.title}' lista {dv.sqref}: opção {v!r} {motivo}")
    # autoteste do verificador
    for ruim in ("+2 em um", "-1", "=A1", "@x", "1-4", "3/7", "1:30", "2.5", "07", "50%", "TRUE", "Falso"):
        r.ok(risco_google(ruim) is not None, f"autoteste do lint: {ruim!r} deveria ser risco no Google")
    for bom in ("Um Atributo (+2)", "—", "A", "Dano +2", "Nível 3", 5, "1d6"):
        r.ok(risco_google(bom) is None, f"autoteste do lint: {bom!r} não é risco ({risco_google(bom)})")
    r.info(f"revisão 2: {n_listas} listas suspensas, {n_opcoes} opções conferidas (=, +, -, @, data, hora, "
           f"número em texto, booleano)")
    # (2) leitura protegida
    leitura, sinais, contador = mapa.get("leitura", {}), mapa.get("sinais", {}), mapa.get("contador", {})
    r.ok(bool(leitura) and bool(sinais) and bool(contador), "mapa sem camada de leitura protegida/sinais/contador")
    entradas = {}
    for nome in mapa.get("entradas", {}):
        aba, cel = separar_ref(mapa["celulas"][nome])
        from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
        l, rr = coordinate_from_string(cel.split(":")[0])
        entradas.setdefault(aba, set()).add((rr, column_index_from_string(l)))
    isentas = set(leitura) | set(sinais) | set(contador)
    n_diretas = n_conf = 0
    for ws in wb.worksheets:
        for linha in ws.iter_rows():
            for c in linha:
                v = c.value
                if not (isinstance(v, str) and v.startswith("=")):
                    continue
                ref = f"'{ws.title}'!{c.coordinate}"
                n_conf += 1
                if ref in leitura:
                    alvo = leitura[ref]
                    a_, cel_ = separar_ref(alvo)
                    pref = "" if a_ == ws.title else f"'{a_}'!"
                    x = f"{pref}${re.match(r'[A-Z]+', cel_).group(0)}${re.search(r'\d+', cel_).group(0)}"
                    r.ok(v == f'=IF(ISERROR({x}),"",IF(ISBLANK({x}),"",{x}))',
                         f"{ref}: camada de leitura protegida fora do formato: {v}")
                    continue
                if ref in isentas:
                    continue
                for a, r0, c0, r1, c1 in _intervalos_da_formula(v, ws.title):
                    toca = [(rr, cc) for rr, cc in entradas.get(a, ()) if r0 <= rr <= r1 and c0 <= cc <= c1]
                    if toca:
                        n_diretas += 1
                        r.falha(f"{ref}: lê a entrada '{a}'!{toca[0]} fora da camada de leitura protegida: {v[:160]}")
    from openpyxl.utils import get_column_letter
    todas = {f"'{a}'!{get_column_letter(cc)}{rr}" for a, s in entradas.items() for rr, cc in s}
    com_sinal = {x for xs in sinais.values() for x in xs}
    r.ok(todas <= com_sinal, f"entradas sem sinal de erro na linha: {sorted(todas - com_sinal)[:8]}")
    # cada sinal aparece no aviso da linha (que mostra o que fazer)
    avisos = {f"'{a}'!{c}" for a, cs in mapa.get("avisos", {}).items() for c in cs}
    usos = {s: 0 for s in sinais}
    for ref in avisos:
        a, cel = separar_ref(ref)
        v = wb[a][cel].value or ""
        for s in sinais:
            if separar_ref(s)[0] == a and f"IF({separar_ref(s)[1]}>0," in v:
                usos[s] += 1
    sem = [s for s, n in usos.items() if n != 1]
    r.ok(not sem, f"sinal de erro sem aviso (ou em mais de um): {sem[:8]}")
    r.info(f"revisão 2: {n_conf} fórmulas conferidas, {n_diretas} leitura(s) direta(s) de entrada; "
           f"{len(leitura)} células na camada de leitura protegida, {len(com_sinal)} entradas com sinal "
           f"de erro em {len(sinais)} linhas; {len(contador)} células do contador da Início")


def suite_lint(args):
    import openpyxl
    r = Resultado("lint")
    ok = ler_funcoes_ok()
    if ok is None:
        r.falha("build/ficha_funcoes_ok.json não existe: rode a suíte spike antes")
        return r
    permitidas = set(ok["funcoes"])
    # Autoteste do verificador: cada fórmula ruim precisa gerar achado
    for ruim, exc in [('=TEXT(A1,"0")', True), ("=SUM(A1;A2)", True), ("=SUMPRODUCT(--(A1:A3>0))", True),
                      ("=ROUNDDOWN(A1,0)", True), ("=TRIM(A1)", True), ("=[Outro.xlsx]Aba!A1", True),
                      ("='Dados'!A1>0", False), ('=IF(A1="a;b","x","y")', True)]:
        sonda = Resultado("sonda")
        _checar_formula(sonda, ruim, "sonda", permitidas, permite_exclamacao=exc)
        esperado_falha = ruim != '=IF(A1="a;b","x","y")'
        r.ok(bool(sonda.falhas) == esperado_falha,
             f"autoteste do lint: {ruim} → achados {sonda.falhas}")
    if not XLSX.exists():
        r.falha(f"planilha não encontrada: {XLSX}")
        return r
    wb = openpyxl.load_workbook(XLSX)
    r.ok(wb.sheetnames == ABAS_ESPERADAS,
         f"abas fora do plano: {wb.sheetnames} (esperado {ABAS_ESPERADAS})")
    for nome in wb.sheetnames:
        r.ok(not _tem_emoji(nome), f"nome de aba com emoji/símbolo: {nome!r}")
    r.ok(len(wb.defined_names) == 0, f"nomes definidos no arquivo: {list(wb.defined_names)}")
    r.ok(bool(wb.calculation.fullCalcOnLoad), "wb.calculation.fullCalcOnLoad não está ligado")
    sec = wb.security
    r.ok(sec is None or not (sec.lockStructure or sec.lockWindows),
         "proteção de pasta de trabalho ligada")
    for f in wb._fonts:
        r.ok(f.name == "Arial", f"fonte no arquivo diferente de Arial: {f.name}")
    n_formulas = n_dv = n_cf = 0
    fontes_ruins = 0
    for ws in wb.worksheets:
        r.ok(not ws.protection.sheet, f"aba '{ws.title}' com proteção do Excel")
        r.ok(not ws.tables, f"aba '{ws.title}' com Tabela do Excel: {list(ws.tables)}")
        for linha in ws.iter_rows():
            for c in linha:
                if c.has_style and c.font is not None and c.font.name != "Arial":
                    fontes_ruins += 1
                    if fontes_ruins <= 20:
                        r.falha(f"'{ws.title}'!{c.coordinate}: fonte {c.font.name}")
                v = c.value
                if isinstance(v, bool):
                    r.falha(f"'{ws.title}'!{c.coordinate}: valor booleano (vira caixa de seleção?)")
                if isinstance(v, str) and v.startswith("="):
                    n_formulas += 1
                    _checar_formula(r, v, f"'{ws.title}'!{c.coordinate}", permitidas)
        for dv in ws.data_validations.dataValidation:
            n_dv += 1
            onde = f"'{ws.title}' validação {dv.sqref}"
            for fx in (dv.formula1, dv.formula2):
                if not fx:
                    continue
                if dv.type == "custom":
                    _checar_formula(r, fx, onde, permitidas, permite_exclamacao=False)
                elif dv.type == "list":
                    r.ok("[" not in fx, f"{onde}: link externo em lista: {fx}")
                    r.ok(fx.upper() not in ('"TRUE,FALSE"', '"FALSE,TRUE"'),
                         f"{onde}: lista TRUE/FALSE (caixa de seleção)")
                else:
                    _checar_formula(r, fx, onde, permitidas)
        for cf in ws.conditional_formatting:
            for regra in cf.rules:
                n_cf += 1
                onde = f"'{ws.title}' formatação condicional {cf.sqref}"
                for fx in regra.formula or []:
                    _checar_formula(r, fx, onde, permitidas, permite_exclamacao=False)
                if regra.dxf is not None and regra.dxf.font is not None and \
                        regra.dxf.font.name not in (None, "Arial"):
                    r.falha(f"{onde}: fonte {regra.dxf.font.name} na formatação condicional")
    r.ok(fontes_ruins == 0, f"{fontes_ruins} célula(s) com fonte diferente de Arial")
    # Layout da Em Jogo (plano 2.2): uma tela A:L × linhas 1-40, largura somada <= 1360 px
    ej = wb["Em Jogo"]
    larg = sum(int((ej.column_dimensions[chr(65 + i)].width or 8.43) * 7 + 5) for i in range(12))
    r.ok(larg <= 1360, f"Em Jogo: largura de A:L = {larg} px (máximo 1360)")
    r.ok(ej["A1"].value == "Resumo para o Jogador", f"Em Jogo: A1 deveria abrir o Resumo para o Jogador, "
                                                    f"veio {ej['A1'].value!r}")
    # Pedido do usuário (v1.1): a ficha é dos jogadores. O texto antigo não pode voltar em
    # lugar nenhum do arquivo (valores, fórmulas, validações e notas)
    antigo = "resumo para o mestre"
    achados = [f"'{ws.title}'!{c.coordinate}" for ws in wb.worksheets for linha in ws.iter_rows() for c in linha
               if isinstance(c.value, str) and antigo in c.value.lower()]
    for ws in wb.worksheets:
        for dv in ws.data_validations.dataValidation:
            for s in (dv.prompt, dv.promptTitle, dv.error, dv.errorTitle, dv.formula1):
                if s and antigo in str(s).lower():
                    achados.append(f"'{ws.title}' validação {dv.sqref}")
        for linha in ws.iter_rows():
            for c in linha:
                if c.comment is not None and antigo in c.comment.text.lower():
                    achados.append(f"'{ws.title}'!{c.coordinate} (nota)")
    r.ok(not achados, f"'Resumo para o Mestre' ainda aparece no .xlsx: {achados[:8]}")
    # Pedido do usuário (v1.1): nenhuma aba com painel congelado nem dividido
    for ws in wb.worksheets:
        sv = ws.sheet_view
        r.ok(ws.freeze_panes is None, f"'{ws.title}': painel congelado em {ws.freeze_panes}")
        r.ok(sv.pane is None, f"'{ws.title}': painel dividido/congelado no sheet_view ({sv.pane})")
    fora = [c.coordinate for linha in ej.iter_rows(min_row=41, max_col=12) for c in linha
            if c.value is not None and c.row < 42]
    r.ok(not fora, f"Em Jogo: conteúdo na linha 41 (a tela vai até a 40): {fora}")
    _lint_google(r, wb)
    r.info(f"Em Jogo: A:L soma {larg} px; tela nas linhas 1-40; título e legenda a partir da linha 42")
    r.info(f"{n_formulas} fórmulas, {n_dv} validações, {n_cf} regras de formatação condicional "
           f"conferidas em {len(wb.worksheets)} abas")
    return r


# ---------------------------------------------------------------------------
# Suíte dados — parser PRÓPRIO (não importa build/ficha_dados.py)
# ---------------------------------------------------------------------------

_md_cache = {}


def _md(cap):
    if cap not in _md_cache:
        arq = next(p for p in sorted(LIVRO.iterdir()) if p.name.startswith(cap + "-"))
        _md_cache[cap] = arq.read_text(encoding="utf-8")
    return _md_cache[cap]


def _sem_md(s):
    """Remove negrito/itálico/código e normaliza espaços (implementação do teste)."""
    s = re.sub(r"\*\*|`", "", s)
    s = re.sub(r"(^|[^\w*])\*([^*\s][^*]*?)\*(?=$|[^\w*])", r"\1\2", s)
    return " ".join(s.split())


def _trecho(cap, cabecalho):
    """Texto da seção que começa na linha `cabecalho` até o próximo cabeçalho
    com o mesmo número de '#' ou menos."""
    linhas = _md(cap).split("\n")
    n = len(cabecalho.split(" ")[0])
    for i, l in enumerate(linhas):
        if l.startswith(cabecalho):
            fim = len(linhas)
            for j in range(i + 1, len(linhas)):
                mm = re.match(r"(#+) ", linhas[j])
                if mm and len(mm.group(1)) <= n:
                    fim = j
                    break
            return linhas[i:fim]
    raise ValueError(f"[teste] seção {cabecalho!r} não achada em {cap}")


def _tabs(linhas):
    """Tabelas markdown: lista de linhas (cada linha = lista de células limpas);
    a primeira linha é o cabeçalho; a linha '|---|' é descartada."""
    achadas, atual = [], None
    for l in linhas:
        s = re.sub(r"^>\s?", "", l).strip()
        if s.startswith("|") and s.endswith("|"):
            if re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", s):
                continue
            cel = [_sem_md(x) for x in s.strip("|").split("|")]
            if atual is None:
                atual = []
                achadas.append(atual)
            atual.append(cel)
        else:
            atual = None
    return achadas


def _tab(cap, cabecalho, primeira):
    for t in _tabs(_trecho(cap, cabecalho)):
        if t[0][0].startswith(primeira):
            return t[0], t[1:]
    raise ValueError(f"[teste] tabela {primeira!r} não achada em {cap} {cabecalho}")


def _n(s):
    s = _sem_md(str(s)).replace(" Cr", "").replace("Cr", "").strip()
    if s in ("", "—", "-"):
        return None
    if re.fullmatch(r"[+-]?\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    s = s.replace(",", ".")
    m = re.match(r"[+-]?\d+(?:\.\d+)?", s)
    if not m:
        return None
    x = float(m.group(0))
    return int(x) if x == int(x) else x


def _dd(s):
    m = re.search(r"(\d+)d(\d+)", s)
    return [int(m.group(1)), int(m.group(2))] if m else [0, 0]


_ATR = ["Poder", "Agilidade", "Vigor", "Sincronia", "Discernimento", "Presença"]


def _atrs(texto):
    return sorted([a for a in _ATR if a in texto], key=texto.index)


def _transcrito():
    """Lê o dicionário TRANSCRITO de ficha_dados.py por AST (sem importar)."""
    import ast
    arvore = ast.parse((BUILD / "ficha_dados.py").read_text(encoding="utf-8"))
    for no in arvore.body:
        if isinstance(no, ast.Assign) and any(getattr(t, "id", "") == "TRANSCRITO"
                                              for t in no.targets):
            return ast.literal_eval(no.value)
    raise ValueError("TRANSCRITO não achado em ficha_dados.py")


_RE_FREQ_T = re.compile(r"\b(uma|1) vez por (turno|ciclo|combate|descanso longo|descanso curto|"
                        r"cena|sessão|dia)( por alvo)?|\b(duas|2) vezes por (dia|combate|ciclo|"
                        r"descanso longo)", re.I)


def _bencaos_teste():
    caps = [("07", "A Destruição"), ("08", "A Inexistência"), ("09", "A Harmonia"),
            ("10", "A Abundância"), ("11", "A Recordação"), ("12", "A Erudição"),
            ("13", "A Euforia"), ("14", "A Caça"), ("15", "A Preservação")]
    saida = []
    for cap, caminho in caps:
        txt = _md(cap)
        resumo = {}
        for t in _tabs(_trecho(cap, "## Resumo do capítulo")):
            if t[0][:2] == ["#", "Bênção"]:
                resumo = {int(l[0]): l[3] for l in t[1:]}
        partes = re.split(r"(?m)^### (?=\d+\. )", txt)[1:]
        for p in partes:
            cab, _, resto = p.partition("\n")
            n, nome = cab.split(". ", 1)
            tier_l, _, corpo = resto.partition("\n")
            m = re.match(r"\*\*Tier (III|II|I) — (sem requisito de nível|requisito: nível (\d+))", tier_l)
            corpo = re.split(r"(?m)^(?:## |---\s*$)", corpo)[0]
            freq = []
            for linha in corpo.split("\n"):
                if linha.strip().startswith(">"):
                    continue
                for mm in _RE_FREQ_T.finditer(_sem_md(linha)):
                    f = mm.group(0)
                    f = re.sub(r"^1 vez", "uma vez", f, flags=re.I)
                    f = re.sub(r"^2 vezes", "duas vezes", f, flags=re.I)
                    f = f[0].upper() + f[1:]
                    if f.lower() not in (x.lower() for x in freq):
                        freq.append(f)
            saida.append([caminho, int(n), nome.strip(), m.group(1) if m else "?",
                          int(m.group(3)) if m and m.group(3) else 1, resumo.get(int(n), "?"),
                          " · ".join(freq) if freq else "Sem limite declarado",
                          "Sim" if "Bênção nova da v1.0" in tier_l else "Não"])
    return saida


def _reescreve_desde(corpo_mestra):
    """Nível a partir do qual se reescreve 1 Habilidade por nível: a marca
    '(reescreve…)' de 26.2 e a frase 'A partir do nível N' de 16.6 têm de bater."""
    marca = next(_n(l[0]) for l in corpo_mestra if "reescreve" in l[4])
    frase = re.search(r"A partir do nível (\d+)\*\*, em vez de aprender", _md("16"))
    if frase is None or int(frase.group(1)) != marca:
        raise ValueError(f"[teste] 26.2 marca reescrita no {marca}, 16.6 diz "
                         f"{frase.group(1) if frase else '?'}")
    # v1.1 (N1): a célula de 26.2 escreve o intervalo inteiro, "do 16 ao 20"
    faixa = next((re.search(r"do (\d+) ao (\d+)", l[4]) for l in corpo_mestra if "reescreve" in l[4]), None)
    if faixa is None or (int(faixa.group(1)), int(faixa.group(2))) != (marca, 20):
        raise ValueError(f"[teste] 26.2 não diz 'do {marca} ao 20' na célula da reescrita")
    return marca


def _so_inimigos(linha_21_5):
    """Linha da tabela de 21.5 que só vale para inimigos: '(só inimigos)' no nome
    (Quebrado) ou o Efeito começando por 'Só inimigos.' (Congelado, v1.1 — 21.2)."""
    return "só inimigos" in linha_21_5[0] or linha_21_5[1].lower().startswith("só inimigos")


def _esperados_dados():
    """Linhas esperadas de cada bloco da aba Dados, montadas pelo teste."""
    tr_ = _transcrito()
    E = {}
    cab, rs = _tab("05", "## Tabela de consulta rápida", "Raça")
    linhas = []
    for l in rs:
        op = _atrs(l[1])
        linhas.append([l[0], l[1], "Não" if op else "Sim", op[0] if op else "",
                       op[1] if len(op) > 1 else "", l[2], None])   # texto: checagem à parte
    E["racas"] = linhas
    E["vantagens_raciais"] = [[v["raca"], v["onde"]] for v in tr_["vantagens_raciais"]]
    cab, c = _tab("04", "## 4.2", "Valor")
    E["bonus_atributo"] = [[_n(a), _n(b)] for a, b in zip(cab[1:], c[0][1:])]
    cab, c = _tab("03", "### Método B", "Valor")
    E["compra"] = [[_n(a), _n(b)] for a, b in zip(cab[1:], c[0][1:])]
    per, atual = [], None
    for l in _trecho("04", "## 4.4"):
        if l.startswith("### "):
            atual = l[len("### Perícias de "):] if l.startswith("### Perícias de ") else \
                l[len("### Perícia de "):] if l.startswith("### Perícia de ") else \
                "Discernimento ou Sincronia"
        s = l.strip()
        if s.startswith("| **"):
            cel = [_sem_md(x) for x in s.strip("|").split("|")]
            per.append([re.sub(r" \(.*\)$", "", cel[0]), atual, cel[1]])
    E["pericias"] = per
    E["tr"] = [l[:2] for l in _tab("04", "## 4.6", "Teste de Resistência")[1]]
    _, aeon = _tab("06", "## 6.2", "Caminho")
    _, col = _tab("06", "## 6.3", "Caminho")
    rec = {x["caminho"]: x["recurso"] for x in tr_["recurso_proprio"]}
    ae = {l[0]: l for l in aeon}
    E["caminhos"] = []
    for l in col:
        a = _atrs(l[1])
        p = [x.strip() for x in l[2].split(",")]
        E["caminhos"].append([l[0], ae[l[0]][1], ae[l[0]][2], l[1], a[0],
                              a[1] if len(a) > 1 else "", p[0], p[1], p[2], _n(l[3]), _n(l[4]),
                              rec[l[0]]])
    E["pv"] = [[_n(x) for x in l] for l in _tab("06", "## 6.4", "Nível")[1]]
    E["bencaos"] = _bencaos_teste()
    E["acumulos"] = [[a["caminho"], a["bencao"], a["recurso"], a["maximo"]] for a in tr_["acumulos"]]
    E["efeitos_automaticos"] = [[e["caminho"], e["bencao"], e["efeito"]]
                                for e in tr_["efeitos_automaticos"]]
    mestra = []
    corpo_m = _tab("26", "## 26.2", "Nível")[1]
    desde = _reescreve_desde(corpo_m)
    for l in corpo_m:
        m = re.search(r"(\d+) P / (\d+) TR", l[2])
        mestra.append([_n(l[0]), _n(l[1]), int(m.group(1)) if m else 0,
                       int(m.group(2)) if m else 0, _n(l[3]), _n(l[4]),
                       "Sim" if _n(l[0]) >= desde else "Não", _n(l[5]),
                       "Não" if _n(l[6]) is None else "Sim", _n(l[7]), _n(l[8]) or 0, _n(l[9])])
    E["mestra"] = mestra
    E["faixas"] = _tab("26", "## 26.3", "Faixa")[1]
    E["ressonancias"] = [[l[0], _n(l[1]), l[2]] for l in _tab("26", "## 26.7", "Ressonância")[1]]
    E["habilidades"] = [[_n(l[0]), l[1]] + _dd(l[1]) + [_n(l[2]), l[3]] + _dd(l[3]) +
                        [_n(l[4]), _n(l[5]), _n(l[6]), l[7]]
                        for l in _tab("16", "## 16.3", "Nível")[1]]
    E["buff"] = [[_n(l[0])] + l[1:4] for l in _tab("16", "### Buff e Debuff", "Nível")[1]]
    E["passivas"] = [[_n(l[0]), l[1]] for l in _tab("16", "### Passivas", "Nível")[1]]
    E["ultimate"] = [[l[0], _n(l[1]), l[2]] + _dd(l[2]) + [_n(l[3]), l[4]] + _dd(l[4]) +
                     [_n(l[5]), _n(l[6])] for l in _tab("17", "## 17.3", "Faixa de nível")[1]]
    E["ph"] = [[_n(l[0])] + [int(x) for x in re.findall(r"\d+", l[1])] +
               [int(x) for x in re.findall(r"\d+", l[2])]
               for l in _tab("16", "## 16.2", "Nº de jogadores")[1]]
    cab, c = _tab("16", "## 16.2", "Nível da Habilidade")
    E["custo_ph"] = [[_n(a), _n(b)] for a, b in zip(cab[1:], c[0][1:])]
    E["energia"] = [l[:3] for l in _tab("17", "## 17.2", "Fonte")[1]]
    E["tenacidade"] = [l[:2] for l in _tab("20", "## 20.3", "Fonte")[1]]
    q = {l[0]: l for l in _tab("20", "## 20.5", "Elemento")[1]}
    els = []
    for l in _tab("20", "## 20.1", "Elemento")[1]:
        dq = q[l[0]][1]
        mm = re.search(r"(\d+) × Eficiência", dq)
        els.append([l[0], l[1], l[2], dq] + _dd(dq) + [int(mm.group(1)) if mm else 1, q[l[0]][2]])
    E["elementos"] = els
    E["fraqueza"] = [l[:3] for l in _tab("20", "## 20.2", "Situação")[1]]
    cab, c = _tab("20", "## 20.2", "Faixa de nível do inimigo")
    E["dt_fraqueza"] = [[a, _n(b)] for a, b in zip(cab[1:], c[0][1:])]
    # 21.5 (v1.1): "só inimigos" vem no nome (Quebrado) ou abre o Efeito (Congelado: "Só inimigos.")
    E["condicoes"] = [[l[0].replace(" (só inimigos)", ""), l[1], l[2], l[3],
                       "Sim" if _so_inimigos(l) else "Não"]
                      for l in _tab("21", "## 21.5", "Condição")[1]]
    E["dt_faixa"] = [[l[0]] + [_n(x) for x in l[1:]] for l in _tab("27", "## 27.2", "Dificuldade")[1]]
    E["dt_subsistema"] = [l[:3] for l in _tab("27", "## 27.3", "Teste")[1]]
    E["dt_fonte"] = [l[:2] for l in _tab("22", "## 22.3", "A fonte é")[1]]
    ini = [t for t in _tabs(_trecho("22", "## 22.3")) if t[0][0] == "Faixa do inimigo"]
    E["dt_inimigo"] = [[l[0]] + [_n(x) for x in l[1:]] for l in ini[0][1:]]
    E["tr_inimigo"] = [[l[0]] + [_n(x) for x in l[1:]] for l in ini[1][1:]]
    E["armas"] = [[l[0].replace(" (2 mãos)", ""), l[1]] + _dd(l[1]) +
                  [l[2], l[3], _n(l[4]), _n(l[5]), _n(l[6]), "Sim" if "(2 mãos)" in l[0] else "Não"]
                  for l in _tab("24", "## 24.2", "Categoria")[1]]
    E["propriedades"] = [l[:2] for l in _tab("24", "## 24.2", "Propriedade")[1]]
    arm = []
    for l in _tab("24", "## 24.1", "Tipo")[1]:
        o = l[2]
        v = re.search(r"([+-]\d+) de Velocidade", o)
        rd = re.search(r"(\d+) RD", o)
        pe = re.search(r"([+-]\d+) em Reflexos e nas Perícias de Agilidade", o)   # 24.1 (v1.1)
        arm.append([l[0], _n(l[1]), o, l[3], _n(l[4]), _n(l[5]), int(v.group(1)) if v else 0,
                    int(rd.group(1)) if rd else 0, int(pe.group(1)) if pe else 0])
    E["armaduras"] = arm
    E["pocoes"] = [[l[0]] + [_n(x) for x in l[1:4]] for l in _tab("24", "## 24.3", "Poção")[1]]
    E["itens"] = [[l[0], _n(l[1]), _n(l[2]), l[3]] for l in _tab("24", "## 24.3", "Item")[1]]
    E["inventario"] = [l[:2] for l in _tab("24", "## 24.4", "Situação")[1]]
    E["verba"] = [[l[0], _n(l[1]), l[2]] for l in _tab("24", "## 24.5", "Faixa de nível")[1]]
    E["faixas_equipamento"] = [l[:3] for l in _tab("25", "## 25.1", "Faixa de nível")[1]]
    cones = []
    for l in _tab("25", "## 25.2", "Nível do Cone")[1]:
        mm = re.match(r"\+(\d+) (ou|e) \+(\d+) PV", l[2])
        cones.append([_n(l[0]), _n(l[1]), l[2], int(mm.group(1)), mm.group(2), int(mm.group(3)), l[3]])
    E["cone"] = cones
    E["reliquias"] = [[l[0], l[1]] + [_n(x) for x in l[2:6]] for l in _tab("25", "## 25.3", "Slot")[1]]
    E["conjuntos"] = [l[:2] for l in _tab("25", "## 25.3", "Peças do mesmo Conjunto")[1]]
    for id_, prim in [("memo_conceito", "Conceito"), ("memo_funcao", "Função"),
                      ("memo_bonus", "Bônus menor"), ("memo_evolucoes", "Evolução")]:
        E[id_] = [l[:2] for l in _tab("11", "## 11.3", prim)[1]]
    mod = [t for t in _tabs(_trecho("11", "### Passo 5")) if t[0][0] == "Modelo da v0.1"]
    E["memo_principal"] = [l[:2] for l in mod[0][1:]]
    E["memo_auxiliar"] = [l[:2] for l in mod[1][1:]]
    E["memo_ficha"] = [l[:2] for l in _tab("11", "## 11.4", "Estatística")[1]]
    return E


def _listas_esperadas():
    tr_ = _transcrito()
    L = {}
    L["racas"] = [l[0] for l in _tab("05", "## Tabela de consulta rápida", "Raça")[1]]
    L["caminhos"] = [l[0] for l in _tab("06", "## 6.3", "Caminho")[1]]
    L["atributos"] = re.findall(r"(?m)^\*\*(\w+)\*\* — ", "\n".join(_trecho("04", "## 4.1")))
    L["elementos"] = [l[0] for l in _tab("20", "## 20.1", "Elemento")[1]]
    L["armaduras"] = [l[0] for l in _tab("24", "## 24.1", "Tipo")[1]]
    L["armas"] = [l[0].replace(" (2 mãos)", "") for l in _tab("24", "## 24.2", "Categoria")[1]]
    media = next(l for l in _tab("24", "## 24.2", "Categoria")[1] if l[0] == "Média")
    L["atributo_media"] = _atrs(media[3])
    L["propriedades"] = ["Nenhuma"] + [l[0] for l in _tab("24", "## 24.2", "Propriedade")[1]]
    tipo = next(l for l in _tab("16", "## 16.1", "Campo")[1] if l[0] == "Tipo")[1]
    L["tipos_habilidade"] = [x.strip() for x in re.split(r", | ou ", tipo)]
    escala = next(l for l in _md("18").split("\n") if "Pessoal → Curta" in l)
    L["alcances"] = [_sem_md(x.replace(">", "")) for x in escala.split("→")]
    L["condicoes"] = [l[0] for l in _tab("21", "## 21.5", "Condição")[1]
                      if not _so_inimigos(l) and l[0] != "Morrendo"]
    L["pericias"] = re.findall(r"(?m)^\| \*\*([^*]+)\*\*", "\n".join(_trecho("04", "## 4.4")))
    L["tr"] = [l[0] for l in _tab("04", "## 4.6", "Teste de Resistência")[1]]
    L["slots"] = [l[0] for l in _tab("25", "## 25.3", "Slot")[1]]
    L["memo_conceito"] = [l[0] for l in _tab("11", "## 11.3", "Conceito")[1]]
    L["memo_funcao"] = [l[0] for l in _tab("11", "## 11.3", "Função")[1]]
    L["memo_bonus"] = [l[0] for l in _tab("11", "## 11.3", "Bônus menor")[1]]
    L["memo_evolucoes"] = [l[0] for l in _tab("11", "## 11.3", "Evolução")[1]]
    for k, v in tr_["listas"].items():
        L[k] = v["valores"]
    return L


def _igual_celula(a, b):
    a = "" if a is None else a
    b = "" if b is None else b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) < 1e-9
    return a == b


def _ler_intervalo(ws, intervalo):
    from openpyxl.utils.cell import range_boundaries
    _, rng = separar_ref(intervalo)
    c1, r1, c2, r2 = range_boundaries(rng)
    return [[ws.cell(i, j).value for j in range(c1, c2 + 1)] for i in range(r1, r2 + 1)]


def suite_dados(args):
    import openpyxl
    r = Resultado("dados")
    mapa = ler_mapa()
    if mapa is None or not XLSX.exists():
        r.falha("rode build/gerar_ficha.py antes (falta o .xlsx ou o ficha_mapa.json)")
        return r
    wb = openpyxl.load_workbook(XLSX)
    ws = wb["Dados"]
    esperados = _esperados_dados()
    blocos = mapa["blocos"]
    for id_, esp in esperados.items():
        chave = f"dados.{id_}"
        if chave not in blocos:
            r.falha(f"bloco {chave} ausente no mapa")
            continue
        b = blocos[chave]
        real = _ler_intervalo(ws, b["intervalo"])
        r.ok(len(real) == len(esp), f"{chave}: {len(real)} linhas na aba, {len(esp)} no livro")
        tit = ws[separar_ref(b["titulo"])[1]].value
        r.ok(bool(tit) and "—" in tit, f"{chave}: título sem fonte: {tit!r}")
        for i, (lr, le) in enumerate(zip(real, esp)):
            r.ok(len(lr) == len(le), f"{chave} linha {i + 1}: {len(lr)} colunas, esperado {len(le)}")
            for j, (vr, ve) in enumerate(zip(lr, le)):
                if ve is None and id_ == "racas" and j == 6:
                    continue
                r.ok(_igual_celula(vr, ve),
                     f"{chave} linha {i + 1} coluna {b['colunas'] and list(b['colunas'])[j]}: "
                     f"aba={vr!r} livro={ve!r}")
    for chave in blocos:
        r.ok(chave[len("dados."):] in esperados, f"bloco {chave} na aba sem conferência no teste")

    # Texto dos traços: cada frase existe no capítulo 05 (sem marcação) e
    # todo traço '### Traço — X' da Raça aparece
    md05 = _sem_md(_md("05").replace("\n", " "))
    md05 = md05.replace("> ", " ")
    md05 = " ".join(md05.split())
    racas_b = blocos["dados.racas"]
    for lr in _ler_intervalo(ws, racas_b["intervalo"]):
        raca, txt = lr[0], lr[6] or ""
        bloco_md = re.split(r"(?m)^## ", _md("05"))
        sec = next((s for s in bloco_md if s.startswith(raca + "\n")), "")
        # v1.2: o capítulo 05 passou a marcar o tipo no próprio título — "### Traço ativável —"
        # e "### Traço passivo —", porque toda Raça tem exatamente um de cada. O formato antigo
        # ("### Traço —") continua aceito para não quebrar a leitura de um capítulo mais velho.
        nomes = re.findall(r"(?m)^### Traço(?: ativável| passivo)? — (.+)$", sec)
        r.ok(bool(nomes), f"Raça {raca}: nenhum traço no capítulo 05")
        # o contrato da v1.2: toda Raça tem exatamente um ativável e um passivo
        r.ok(len(nomes) >= 2, f"Raça {raca}: esperado um traço ativável e um passivo, achei {len(nomes)}")
        for nome in nomes:
            r.ok(f"{nome.strip()}:" in txt, f"Raça {raca}: traço '{nome}' ausente do texto da aba")
        for frase in re.split(r"(?<=[.:])\s+|•\s*", txt):
            frase = frase.strip()
            if len(frase) < 12 or frase.endswith(":") and len(frase) < 40:
                continue
            r.ok(frase in md05, f"Raça {raca}: trecho do texto dos traços não está no livro: {frase[:80]!r}")

    # Listas de validação
    listas = _listas_esperadas()
    for id_, valores in listas.items():
        chave = f"lista.{id_}"
        if chave not in mapa["listas"]:
            r.falha(f"lista {chave} ausente no mapa")
            continue
        real = [x[0] for x in _ler_intervalo(ws, mapa["listas"][chave])]
        r.ok(real == valores, f"{chave}: aba={real} livro={valores}")
    for chave in mapa["listas"]:
        r.ok(chave[len("lista."):] in listas, f"lista {chave} sem conferência no teste")

    # Contagens do livro
    bs = esperados["bencaos"]
    r.ok(len(bs) == 108, f"{len(bs)} Bênçãos (esperado 108)")
    from collections import Counter
    por_cam = Counter(b[0] for b in bs)
    r.ok(len(por_cam) == 9 and all(v == 12 for v in por_cam.values()),
         f"Bênçãos por Caminho: {dict(por_cam)}")
    for cam in por_cam:
        tiers = Counter(b[3] for b in bs if b[0] == cam)
        r.ok(tiers == Counter({"I": 6, "II": 4, "III": 2}), f"{cam}: tiers {dict(tiers)}")
        nums = [b[1] for b in bs if b[0] == cam]
        r.ok(nums == list(range(1, 13)), f"{cam}: numeração {nums}")
    req = {(b[3], b[4]) for b in bs}
    r.ok(req == {("I", 1), ("II", 9), ("III", 17)}, f"requisitos por tier: {sorted(req)}")
    r.ok(all(b[5] != "?" for b in bs), "Bênção sem resumo de uma linha no 'Resumo do capítulo'")
    # 12 contíguas por Caminho na aba
    reais = _ler_intervalo(ws, blocos["dados.bencaos"]["intervalo"])
    for k in range(9):
        grupo = {x[0] for x in reais[12 * k:12 * k + 12]}
        r.ok(len(grupo) == 1, f"Bênçãos {12 * k + 1}–{12 * k + 12} da aba misturam Caminhos: {grupo}")
    for id_, n in [("racas", 7), ("pericias", 18), ("tr", 6), ("caminhos", 9), ("mestra", 20),
                   ("condicoes", 16), ("elementos", 7), ("habilidades", 7)]:
        r.ok(len(esperados[id_]) == n, f"{id_}: {len(esperados[id_])} linhas no livro (esperado {n})")
        r.ok(blocos[f"dados.{id_}"]["linhas"] == n, f"{id_}: {blocos[f'dados.{id_}']['linhas']} na aba")

    # Âncoras do módulo transcrito
    tr_ = _transcrito()
    n_anc = 0
    for grupo in ("acumulos", "efeitos_automaticos", "recurso_proprio", "vantagens_raciais"):
        for item in tr_[grupo]:
            n_anc += 1
            r.ok(item["ancora"] in _md(item["cap"]),
                 f"âncora não encontrada no capítulo {item['cap']} ({grupo}): {item['ancora']!r}")
    for id_, item in tr_["listas"].items():
        if item["ancora"]:
            n_anc += 1
            r.ok(item["ancora"] in _md(item["cap"]),
                 f"âncora não encontrada no capítulo {item['cap']} (lista {id_}): {item['ancora']!r}")
    # cada acúmulo/efeito cita Bênção que existe no Caminho indicado
    nomes_b = {(b[0], b[2]) for b in bs}
    for item in tr_["acumulos"]:
        r.ok((item["caminho"], item["bencao"]) in nomes_b,
             f"acúmulo cita Bênção inexistente: {item['caminho']} · {item['bencao']}")
    r.info(f"{len(esperados)} blocos e {len(listas)} listas conferidos célula a célula; "
           f"{n_anc} âncoras; {len(bs)} Bênçãos")
    return r


# ---------------------------------------------------------------------------
# Suíte ouro — números impressos no livro (casos a–m da seção 5 do plano)
# ---------------------------------------------------------------------------

def _oraculo():
    sys.path.insert(0, str(BUILD))
    import oraculo_ficha
    return oraculo_ficha


def _nadir(**mudancas):
    """A Nadir de 29.7 (Humana, A Destruição, array oficial, Média, marreta Pesada)."""
    import copy
    e = {
        "nivel": 1, "jogadores": 4, "raca": "Humano", "caminho": "A Destruição",
        "metodo": "Array oficial",
        "atributos": {"Poder": 15, "Vigor": 14, "Agilidade": 13, "Discernimento": 12,
                      "Presença": 10, "Sincronia": 8},
        "bonus_racial": {"modo": "Um Atributo (+2)", "attr1": "Poder"},
        "atributo_habilidade": "Poder", "elemento": "Fogo", "sintonia": "Discernimento",
        "pericias_escolhidas": ["Intimidação", "Mecânica"], "armadura": "Média",
        "arma": {"categoria": "Pesada", "propriedade": "Nenhuma"},
        "habilidades": [{"nome": "Rebarba", "tipo": "Dano", "nivel": 1, "area": False,
                         "resolucao": "Teste de Ataque"}],
        "ultimate": {"nome": "A Doca Inteira", "tipo": "Dano", "area": False},
        "bencaos": ["Pacto da Ruína"], "cone": {"nivel": 1, "alvo": None},
        "reliquias": {"Mãos": {"conjunto": "—"}, "Botas": {"conjunto": "—"}},
    }
    e = copy.deepcopy(e)
    e.update(mudancas)
    return e


def _casos_sobreposicao_25_2():
    """Casos de ouro da Sobreposição (25.2, v1.1): '**2 Sobreposições** num Cone de Nível 1 ou 2
    (... **+3**; a de PV, a **+30**), **1** num de Nível 3 ou 4 (**+3**; PV **+35**) e **nenhuma**
    num de Nível 5 (**+3** ou **+50 PV**)'. Devolve [(rótulo, cone, (numérico, PV), aviso de teto?)]."""
    md = _md("25")
    m = re.search(r"\*\*(\d) Sobreposições\*\* num Cone de Nível 1 ou 2 \(a parte numérica chega a "
                  r"\*\*\+(\d)\*\*; a de PV, a \*\*\+(\d+)\*\*\), \*\*(\d)\*\* num de Nível 3 ou 4 "
                  r"\(\*\*\+(\d)\*\*; PV \*\*\+(\d+)\*\*\) e \*\*nenhuma\*\* num de Nível 5, que já está no "
                  r"teto absoluto \(\*\*\+(\d)\*\* ou \*\*\+(\d+) PV\*\*\)", md)
    if m is None:
        raise ValueError("[teste] 25.2: frase do teto da Sobreposição não encontrada")
    s12, n12, pv12, s34, n34, pv34, n5, pv5 = (int(x) for x in m.groups())
    d = "Defesa"
    return [
        ("Cone 1 (ou, numérico) + 2", {"nivel": 1, "alvo": d, "escolha": "Numérico", "sobreposicoes": s12},
         (n12, 0), False),
        ("Cone 1 (ou, PV) + 2", {"nivel": 1, "alvo": d, "escolha": "PV", "sobreposicoes": s12}, (0, pv12), False),
        ("Cone 2 (e) + 2", {"nivel": 2, "alvo": d, "sobreposicoes": s12}, (n12, pv12), False),
        ("Cone 3 (ou, PV) + 1", {"nivel": 3, "alvo": d, "escolha": "PV", "sobreposicoes": s34}, (0, pv34), False),
        ("Cone 4 (e) + 1", {"nivel": 4, "alvo": d, "sobreposicoes": s34}, (n34, pv34), False),
        ("Cone 5 (ou, numérico) + 0", {"nivel": 5, "alvo": d, "escolha": "Numérico", "sobreposicoes": 0},
         (n5, 0), False),
        ("Cone 5 (ou, PV) + 0", {"nivel": 5, "alvo": d, "escolha": "PV", "sobreposicoes": 0}, (0, pv5), False),
        ("Cone 2 (e) + 3: além do teto", {"nivel": 2, "alvo": d, "sobreposicoes": s12 + 1}, (n12, pv12), True),
        ("Cone 4 (e) + 2: além do teto", {"nivel": 4, "alvo": d, "sobreposicoes": s34 + 1}, (n34, pv34), True),
        ("Cone 5 (ou, PV) + 1: além do teto", {"nivel": 5, "alvo": d, "escolha": "PV", "sobreposicoes": 1},
         (0, pv5), True),
    ]


def _niveis_referencia_22_3():
    """Níveis em que 22.3 conta a DT típica (v1.1, N4): '... nível de referência de cada uma:
    **3, 7, 11, 15 e 19**'."""
    m = re.search(r"nível de referência de cada uma: \*\*([\d, e]+)\*\*", _md("22"))
    if m is None:
        raise ValueError("[teste] 22.3: níveis de referência da DT típica não encontrados")
    return tuple(int(x) for x in re.findall(r"\d+", m.group(1)))


def _nadir_ab_livro():
    """Dano do Ataque Básico da Nadir lido de 29.7 (v1.1, D1): o Passo 12 escreve
    `1d12 + 4 + 2` = `1d12 + 6` = **12** médio, e a ficha fechada repete '1d12 + 6 (com Mãos I)'.
    Devolve (texto, média, fixo do atributo, fixo do equipamento)."""
    md = _md("29")
    m = re.search(r"Dano: `(\d+d\d+) \+ (\d+) \+ (\d+)` = `(\d+d\d+) \+ (\d+)` = \*\*(\d+)\*\* médio", md)
    f = re.search(r"marreta de doca — Pesada, (\d+d\d+) \+ (\d+) \(com Mãos I\)", md)
    if m is None or f is None:
        raise ValueError("[teste] 29.7: dano da marreta da Nadir não encontrado no Passo 12 ou na ficha fechada")
    if int(m.group(2)) + int(m.group(3)) != int(m.group(5)) or (f.group(1), f.group(2)) != (m.group(4), m.group(5)):
        raise ValueError("[teste] 29.7: Passo 12 e ficha fechada dão danos diferentes para a marreta")
    return f"{m.group(4)}+{m.group(5)}", int(m.group(6)), int(m.group(2)), int(m.group(3))


def suite_ouro(args):
    r = Resultado("ouro")
    o = _oraculo()
    calc = o.calcular

    def conf(rotulo, obtido, esperado):
        r.ok(obtido == esperado, f"{rotulo}: oráculo={obtido!r} livro={esperado!r}")

    # (a) Nadir nível 1 — 29.7 (passos 4 a 12 e a ficha fechada)
    s = calc(_nadir())
    for a, (v, b) in {"Poder": (17, 4), "Vigor": (14, 2), "Agilidade": (13, 1),
                      "Discernimento": (12, 1), "Presença": (10, 0), "Sincronia": (8, -1)}.items():
        conf(f"(a) {a}", (s["atributos"][a], s["bonus"][a]), (v, b))
    conf("(a) PV", s["pv_max"], 61)
    conf("(a) Defesa", s["defesa"], 16)
    conf("(a) Esquiva", s["esquiva"], 18)
    conf("(a) RD", s["rd"], 0)
    conf("(a) teto de RD", s["teto_rd"], 6)
    conf("(a) VEL com Botas I", s["velocidade"], 14)
    conf("(a) VEL sem Relíquias (passo 8)", calc(_nadir(reliquias={}))["velocidade"], 12)
    conf("(a) DT das Habilidades", s["dt"], 14)
    conf("(a) Teste de Ataque das Habilidades", s["ataque_habilidade"], 6)
    ab = s["ataque_basico"]
    conf("(a) Teste de Ataque do básico", ab["ataque"], 6)
    ab_txt, ab_med, ab_atr, ab_eq = _nadir_ab_livro()
    conf("(a) AB dano com Mãos I (29.7 v1.1)", (ab["texto"], ab["media"]), (ab_txt, ab_med))
    conf("(a) AB fixo: atributo + Mãos I", (ab["fixo"], ab["equip"]), (ab_atr, ab_eq))
    conf("(a) AB elemento", ab["elemento"], "Físico")
    h = s["habilidades"][0]
    conf("(a) Rebarba", (h["texto"], h["media"], h["ph"], h["rt"]), ("6d6+4", 25, 1, 2))
    u = s["ultimate"]
    conf("(a) A Doca Inteira", (u["texto"], u["media"], u["rt"], u["custo"]), ("5d10+4", 31, 5, 100))
    conf("(a) PH do grupo (início/máximo, mesa de 4)", (s["ph_inicio"], s["ph_max"]), (3, 5))
    conf("(a) Espaço", s["capacidade"], 18)
    conf("(a) Perícias com Eficiência", s["pericias_com_eficiencia"], 5)
    # v1.2: a Nadir é Humana, e o traço passivo Vocação Livre (05) dá +1 Perícia escolhida na
    # criação, então o permitido dela passou de 2 para 3 (04.5)
    conf("(a) Perícias escolhidas permitidas", s["pericias_permitidas"], 3)
    conf("(a) Pacto da Ruína", (s["pacto_da_ruina"]["custo_pv"], s["pacto_da_ruina"]["bonus"],
                                s["pacto_da_ruina"]["bonus_ferido"], s["pacto_da_ruina"]["limiar_pv"]),
         (2, 2, 4, 30))
    conf("(a) Esforço", s["esforco_max"], 1)
    conf("(a) sem avisos", s["avisos"], [])
    for tr_, b in {"Potência Física": 6, "Reflexos": 3, "Resistência Física": 4,
                   "Resistência Mental": 1, "Percepção Mental": 3, "Força de Vontade": 2}.items():
        conf(f"(a) TR {tr_} (d20 + Bônus + 2)", s["testes_resistencia"][tr_]["total"], b)

    # (b) Atletismo +6 no nível 3 — 02.1
    s3 = calc(_nadir(nivel=3))
    conf("(b) Atletismo nível 3", (s3["pericias"]["Atletismo"]["total"],
                                   s3["pericias"]["Atletismo"]["rolagem"]), (6, "d20+6"))

    # (c) Tabela de PV de 06.4 (20 níveis × 5 índices N, Bônus de Vigor +2)
    cab, linhas = _tab("06", "## 6.4", "Nível")
    por_n = {6: "A Destruição", 5: "A Preservação", 4: "A Inexistência", 3: "A Harmonia", 2: "A Caça"}
    for j, col in enumerate(cab[1:], start=1):
        n_ = int(re.search(r"N=(\d)", col).group(1))
        for lin in linhas:
            nv = _n(lin[0])
            sv = calc(_nadir(nivel=nv, caminho=por_n[n_], bencaos=[], atributo_habilidade=None))
            conf(f"(c) PV N={n_} nível {nv}", sv["pv_max"], _n(lin[j]))

    # (d) Lin Hai: aumento de Vigor no nível 9 (+2 -> +3) dá +11 PV na hora — 04.3
    sem = calc(_nadir(nivel=9))
    com = calc(_nadir(nivel=9, aumentos={9: {"modo": "Um Atributo (+2)", "attr1": "Vigor"}}))
    conf("(d) bônus de Vigor 9", (sem["bonus"]["Vigor"], com["bonus"]["Vigor"]), (2, 3))
    conf("(d) ganho de PV na hora", com["pv_max"] - sem["pv_max"], 11)
    conf("(d) nível + 2", com["pv_ganho_vigor"], 11)

    # (e) Memoespírito nível 17 — 11.4
    recorda = _nadir(
        nivel=17, raca="Intellitron", caminho="A Recordação", bonus_racial={"attr1": "Sincronia"},
        atributos={"Sincronia": 15, "Poder": 14, "Agilidade": 13, "Vigor": 12, "Discernimento": 10,
                   "Presença": 8},
        aumentos={3: {"modo": "Um Atributo (+2)", "attr1": "Sincronia"},
                  6: {"modo": "Dois Atributos (+1 cada)", "attr1": "Sincronia", "attr2": "Vigor"}},
        atributo_habilidade="Sincronia", bencaos=[], pericias_escolhidas=[],
        memoespirito={"pontos": {"Sincronia": 5, "Agilidade": 4, "Vigor": 5},
                      "atributo_ataque": "Sincronia", "funcao": "Controlador",
                      "bonus_menores": ["Memória Afiada", "Vínculo Profundo", "Forma Mutável"],
                      "evolucoes": []})
    sm = calc(recorda)
    m = sm["memo"]
    conf("(e) dono: Sincronia/Bônus/Eficiência", (sm["atributos"]["Sincronia"], sm["bonus"]["Sincronia"],
                                                  sm["eficiencia"]), (20, 5, 7))
    conf("(e) PV", m["pv"], 151)
    conf("(e) Defesa", m["defesa"], 21)
    conf("(e) Velocidade", m["velocidade"], 15)
    conf("(e) Teste de Ataque", m["ataque"], 17)
    conf("(e) Dano", (m["texto"], m["media"]), ("5d6+5", 22))
    conf("(e) Dano contra Fraqueza", m["media_fraqueza"], 29)
    conf("(e) Redução de Tenacidade", m["rt"], 2)

    # (e2) Memoespírito de quem usa arma de ENERGIA — 11.4 (v1.2, E17). A escada de 26.2 vale
    # 1/2/3/4/5, mas a arma de Energia começa em 2 e chega a 6 (18.5 e 24.2), e o Memoespírito
    # herda a QUANTIDADE do dono: 2d6 no nível 1 e 6d6 no 17. A face continua d6, nunca d8.
    import copy as _copy
    en17 = _copy.deepcopy(recorda)
    en17["arma"] = {"categoria": "Energia", "propriedade": "Nenhuma"}
    m_en17 = calc(en17)["memo"]
    conf("(e2) Energia, nível 17: 6 dados", (m_en17["texto"], m_en17["media"]), ("6d6+5", 26))
    conf("(e2) Energia, nível 17: contra Fraqueza", m_en17["media_fraqueza"], 33)
    en1 = _copy.deepcopy(en17)
    en1["nivel"] = 1
    en1.pop("aumentos", None)
    conf("(e2) Energia, nível 1: 2 dados", calc(en1)["memo"]["texto"], "2d6+5")
    nao_en1 = _copy.deepcopy(en1)
    nao_en1["arma"] = {"categoria": "Média", "atributo": "Poder", "propriedade": "Nenhuma"}
    conf("(e2) arma Média, nível 1: 1 dado", calc(nao_en1)["memo"]["texto"], "1d6+5")

    # (f) Barreira no 13 = 18 (15.2); teto de PV temporários no 11 = 15 (23.3)
    conf("(f) Barreira nível 13", calc(_nadir(nivel=13, caminho="A Preservação", bencaos=[],
                                              atributo_habilidade="Vigor"))["barreira_max"], 18)
    conf("(f) teto temporário nível 11", calc(_nadir(nivel=11))["teto_temporarios"], 15)

    # (g) Descanso Curto (Vigor +2) — tabela de 23.6
    t = [x for x in _tabs(_trecho("23", "## 23.6")) if x[0][0] == "Nível"][0]
    for nv, esperado in zip(t[0][1:], t[1][1:]):
        conf(f"(g) Descanso Curto nível {nv}", calc(_nadir(nivel=int(nv)))["descanso_curto"], _n(esperado))

    # (h) Dano de Quebra — 20.5 (Eficiência +2 no 3, +8 no 19)
    q3 = calc(_nadir(nivel=3, elemento="Físico"))["quebra"]
    q19 = calc(_nadir(nivel=19, elemento="Físico"))["quebra"]
    conf("(h) Físico nível 3", (q3["texto"], q3["media"]), ("2d6+4", 11))
    conf("(h) Físico nível 19", (q19["texto"], q19["media"]), ("2d6+16", 23))
    conf("(h) Gelo nível 3 e 19", (calc(_nadir(nivel=3, elemento="Gelo"))["quebra"]["texto"],
                                   calc(_nadir(nivel=19, elemento="Gelo"))["quebra"]["texto"]), ("2", "8"))

    # (i) Vesper nível 11, rifle (Disparo longo), Agilidade +5, Mãos +4 — 18.5; Ultimate — 17.4
    vesper = _nadir(
        nivel=11, caminho="A Caça", elemento="Vento", atributo_habilidade="Agilidade",
        atributos={"Agilidade": 15, "Vigor": 14, "Discernimento": 13, "Poder": 12, "Presença": 10,
                   "Sincronia": 8},
        bonus_racial={"modo": "Um Atributo (+2)", "attr1": "Agilidade"},
        aumentos={3: {"modo": "Um Atributo (+2)", "attr1": "Agilidade"},
                  6: {"modo": "Dois Atributos (+1 cada)", "attr1": "Agilidade", "attr2": "Vigor"}},
        arma={"categoria": "Disparo longo", "propriedade": "Nenhuma"}, bencaos=[],
        pericias_escolhidas=[], reliquias={"Mãos": {"conjunto": "—"}},
        ultimate={"tipo": "Dano", "area": False})
    sv = calc(vesper)
    conf("(i) bônus de Agilidade", sv["bonus"]["Agilidade"], 5)
    conf("(i) rifle no nível 11", sv["ataque_basico"]["texto"], "3d10+9")
    conf("(i) rifle contra Fraqueza", sv["ataque_basico"]["texto_fraqueza"], "5d10+9")
    conf("(i) Ultimate nível 11", sv["ultimate"]["dados"], "6d20")
    conf("(i) Ultimate nível 13", calc(dict(vesper, nivel=13))["ultimate"]["dados"], "10d20")

    # (j) Nadir nível 15, Tier III, Conjuntos 4+2 — 25.3
    rel = {"Cabeça": {"conjunto": "A"}, "Mãos": {"conjunto": "A"}, "Tronco": {"conjunto": "A"},
           "Botas": {"conjunto": "A"}, "Esfera Planar": {"conjunto": "B"},
           "Corda de Ligação": {"conjunto": "B"}}
    base15 = calc(_nadir(nivel=15, reliquias={}))
    n15 = calc(_nadir(nivel=15, reliquias=rel, esfera_elemento="Fogo",
                      conjuntos={"A": {"bonus2": "Um tipo de rolagem +1"},
                                 "B": {"bonus2": "Velocidade +1"}}))
    conf("(j) Tier", n15["tier_reliquia"], 3)
    conf("(j) +PV", n15["pv_max"] - base15["pv_max"], 35)
    conf("(j) +Defesa", n15["defesa"] - base15["defesa"], 2)
    conf("(j) +VEL (Botas +4, Nó de Ferro +1)", n15["velocidade"] - base15["velocidade"], 5)
    conf("(j) +dano de Ataque Básico", n15["ataque_basico"]["fixo_total"] - n15["ataque_basico"]["fixo"], 6)
    conf("(j) +dano de Fogo (Esfera Planar)", n15["habilidades"][0]["fixo"] - n15["bonus"]["Poder"], 6)
    conf("(j) Corda de Ligação", n15["reliquias"]["Corda de Ligação"], 20)
    conf("(j) Conjuntos ativos", n15["conjuntos_ativos"], {"A": 4, "B": 2})

    # (k) DT típica 8 + 5 + Eficiência — 22.3
    tipica = re.search(r"ou seja \*\*([\d / ]+)\*\*", _md("22")).group(1)
    esperado = [int(x) for x in tipica.split("/")]
    dts = []
    niveis = _niveis_referencia_22_3()
    for nv in niveis:
        # Poder 15 + 2 (Raça) + 2 (aumento do nível 3) = 19 -> Bônus +5
        sx = calc(_nadir(nivel=nv, aumentos={3: {"modo": "Um Atributo (+2)", "attr1": "Poder"}}))
        conf(f"(k) Bônus do Atributo de Habilidade no nível {nv}", sx["bonus"]["Poder"], 5)
        dts.append(sx["dt"])
    conf(f"(k) DT típica nas cinco faixas (níveis de referência {niveis}, 22.3 v1.1)", dts, esperado)

    # (l) PH de 16.2 (3 a 6 jogadores × 3 degraus)
    for lin in _tab("16", "## 16.2", "Nº de jogadores")[1]:
        jg = _n(lin[0])
        mx = [int(x) for x in re.findall(r"\d+", lin[1])]
        ini = [int(x) for x in re.findall(r"\d+", lin[2])]
        for k, nv in enumerate((1, 9, 17)):
            sx = calc(_nadir(nivel=nv, jogadores=jg))
            conf(f"(l) PH {jg} jogadores nível {nv}", (sx["ph_max"], sx["ph_inicio"]), (mx[k], ini[k]))

    # (m) Progressão = 26.2 linha a linha (reescrita: do nível marcado em diante, 16.6)
    corpo_m = _tab("26", "## 26.2", "Nível")[1]
    desde = _reescreve_desde(corpo_m)
    for lin in corpo_m:
        nv = _n(lin[0])
        sx = calc(_nadir(nivel=nv))
        mm = re.search(r"(\d+) P / (\d+) TR", lin[2])
        esperado = (_n(lin[1]), (int(mm.group(1)), int(mm.group(2))) if mm else (0, 0), _n(lin[3]),
                    _n(lin[4]), nv >= desde, _n(lin[5]), _n(lin[6]) is not None, _n(lin[7]),
                    _n(lin[8]) or 0, _n(lin[9]))
        obtido = (sx["eficiencia"], (sx["slots_eficacia_pericias"], sx["slots_eficacia_tr"]),
                  sx["bencaos_possuidas"], sx["habilidades_conhecidas"], sx["reescreve"],
                  sx["nivel_max_habilidade"], sx["aumento_neste_nivel"], sx["dados_ab"],
                  sx["especializacao"], sx["teto_rd"])
        conf(f"(m) tabela mestra nível {nv}", obtido, esperado)
    # 26.4: Eficácia = 2 × Eficiência
    cab, c = _tab("26", "## 26.4", "Nível")
    for faixa_txt, efi, efc in zip(cab[1:], c[0][1:], c[1][1:]):
        nv = int(faixa_txt.split("-")[0])
        sx = calc(_nadir(nivel=nv))
        conf(f"(m) Eficiência/Eficácia {faixa_txt}", (sx["eficiencia"], sx["eficacia"]), (_n(efi), _n(efc)))

    # (o) Sobreposição — 25.2 (v1.1, D5): +1 e +10 PV por cópia, até a parte numérica chegar a +3
    for rotulo, cone, esperado, acima in _casos_sobreposicao_25_2():
        sx = calc(_nadir(nivel=20, cone=cone))
        conf(f"(o) {rotulo}", (sx["cone"]["numerico"], sx["cone"]["pv"],
                               "SOBREPOSICOES_ACIMA_DO_TETO" in sx["avisos"]), esperado + (acima,))

    if not args.so_oraculo:
        _ouro_planilha(r)
    r.info("modo --so-oraculo: só o oráculo foi conferido" if args.so_oraculo else
           "modo completo: oráculo e PLANILHA (calculada pela biblioteca formulas)")
    return r


# ---------------------------------------------------------------------------
# Planilha: entradas lógicas do oráculo -> células do mapa
# ---------------------------------------------------------------------------

def _slug(s):
    """Mesma convenção de nomes do mapa (implementação do teste)."""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def _entradas_planilha(e, mapa):
    """Converte as entradas lógicas do oráculo (ENTRADAS_EXEMPLO) em {ref: valor}, nas
    10 abas: Criação, Progressão, Testes, Caminho, Habilidades, Equipamento e Em Jogo.
    Acúmulos: 'Marcas da Ruína' vai no campo B da Em Jogo; os outros no campo A."""
    C = mapa["celulas"]
    E = {}

    def put(nome, v):
        if v is None:
            return
        if nome not in C:
            raise KeyError(f"[teste] entrada sem célula no mapa: {nome}")
        E[C[nome]] = v

    put("criacao.nivel", e.get("nivel"))
    put("criacao.jogadores", e.get("jogadores"))
    put("criacao.raca", e.get("raca"))
    put("criacao.caminho", e.get("caminho"))
    put("criacao.metodo", e.get("metodo"))
    for a, v in (e.get("atributos") or {}).items():
        put(f"criacao.atributo.{_slug(a)}.distribuido", v)
    br = e.get("bonus_racial") or {}
    put("criacao.raca.modo", br.get("modo"))
    put("criacao.raca.atributo1", br.get("attr1"))
    put("criacao.raca.atributo2", br.get("attr2"))
    for nv, au in (e.get("aumentos") or {}).items():
        put(f"progressao.aumento.{nv}.modo", au.get("modo"))
        put(f"progressao.aumento.{nv}.atributo1", au.get("attr1"))
        put(f"progressao.aumento.{nv}.atributo2", au.get("attr2"))
    put("criacao.atributo_habilidade", e.get("atributo_habilidade"))
    put("criacao.elemento", e.get("elemento"))
    put("criacao.sintonia", e.get("sintonia"))
    for p in e.get("pericias_escolhidas") or []:
        put(f"criacao.pericia.{_slug(p)}.escolhida", "Sim")
    for p in e.get("eficacia_pericias") or []:
        put(f"testes.pericia.{_slug(p)}.eficacia", "Sim")
    for t in e.get("eficacia_tr") or []:
        put(f"testes.tr.{_slug(t)}.eficacia", "Sim")
    put("criacao.armadura", e.get("armadura"))
    arma = e.get("arma") or {}
    put("criacao.arma.categoria", arma.get("categoria"))
    put("criacao.arma.atributo_media", arma.get("atributo"))
    put("criacao.arma.elemento_proprio", arma.get("elemento"))
    put("criacao.arma.propriedade", arma.get("propriedade"))
    for k, nome in enumerate(e.get("bencaos") or [], start=1):
        put(f"caminho.bencao.slot{k}.nome", nome)
    for rn, opcao in (e.get("ressonancias") or {}).items():
        put(f"progressao.ressonancia.{rn}.opcao", opcao)
    memo = e.get("memoespirito")
    if memo:
        for a, v in (memo.get("pontos") or {}).items():
            put(f"memo.pontos.{_slug(a)}", v)
        put("memo.atributo_ataque", memo.get("atributo_ataque"))
        put("memo.funcao", memo.get("funcao"))
        for k, b in enumerate(memo.get("bonus_menores") or [], start=1):
            put(f"memo.bonus_menor.{k}", b)
        for k, ev in enumerate(memo.get("evolucoes") or [], start=1):
            put(f"memo.evolucao.{k}", ev)
        put("memo.memoria_desperta", memo.get("memoria_desperta"))
    # --- abas de jogo (FEAT-003): Habilidades, Equipamento, Em Jogo, escolhas de Bênção
    sim = lambda b: None if b is None else ("Sim" if b else "Não")  # noqa: E731
    for k, h in enumerate(e.get("habilidades") or [], start=1):
        b = f"habilidades.{k}"
        put(f"{b}.nome", h.get("nome"))
        put(f"{b}.tipo", h.get("tipo"))
        put(f"{b}.nivel", h.get("nivel"))
        put(f"{b}.area", sim(h.get("area")))
        put(f"{b}.resolucao", h.get("resolucao"))
        put(f"{b}.alcance", h.get("alcance"))
        if h.get("ress3"):
            put(f"{b}.ress3", "Sim")
    ult = e.get("ultimate") or {}
    put("habilidades.ultimate.nome", ult.get("nome"))
    put("habilidades.ultimate.tipo", ult.get("tipo"))
    put("habilidades.ultimate.area", sim(ult.get("area")))
    put("habilidades.ultimate.resolucao", ult.get("resolucao"))
    cone = e.get("cone") or {}
    put("equipamento.cone.nivel", cone.get("nivel"))
    put("equipamento.cone.alvo", cone.get("alvo"))
    put("equipamento.cone.escolha", cone.get("escolha"))
    put("equipamento.cone.qual", cone.get("qual"))
    put("equipamento.cone.sobreposicoes", cone.get("sobreposicoes"))
    for slot, info in (e.get("reliquias") or {}).items():
        put(f"equipamento.reliquia.{_slug(slot)}.possui", "Sim")
        put(f"equipamento.reliquia.{_slug(slot)}.conjunto", (info or {}).get("conjunto"))
    put("equipamento.esfera.elemento", e.get("esfera_elemento"))
    for letra, info in (e.get("conjuntos") or {}).items():
        put(f"equipamento.conjunto.{letra.lower()}.bonus2", (info or {}).get("bonus2"))
        put(f"equipamento.conjunto.{letra.lower()}.rolagem", (info or {}).get("rolagem"))
    for k, it in enumerate(e.get("inventario") or [], start=1):
        put(f"equipamento.inventario.{k}.item", it.get("item") or f"Item {k}")
        put(f"equipamento.inventario.{k}.espaco_manual", it.get("espaco"))
        put(f"equipamento.inventario.{k}.qtd", it.get("qtd"))
    put("em_jogo.pv_atual", e.get("pv_atual"))
    if e.get("memo_ativo"):
        put("em_jogo.memo_ativo", "Sim")
    put("caminho.escolha.avatar", e.get("forma_avatar"))
    put("caminho.escolha.fragmentos", e.get("fragmento"))
    for nome, v in (e.get("acumulos") or {}).items():
        put("em_jogo.acumulo.b" if nome == "Marcas da Ruína" else "em_jogo.acumulo.a", v)
    return E


class Planilha:
    """Modelo da planilha + mapa: calcula cenários pelos nomes lógicos."""

    def __init__(self):
        self.mapa = ler_mapa()
        if self.mapa is None:
            raise RuntimeError("build/ficha_mapa.json não existe: rode gerar_ficha.py")
        self.modelo = Modelo(XLSX)
        self.C = self.mapa["celulas"]

    def avisos(self):
        return [f"'{aba}'!{c}" for aba, cs in self.mapa.get("avisos", {}).items() for c in cs]

    def calcular(self, entradas_oraculo=None, nomes=(), refs_entrada=None, extras=()):
        ins = dict(refs_entrada or {})
        if entradas_oraculo is not None:
            ins.update(_entradas_planilha(entradas_oraculo, self.mapa))
        refs = [self.C[n] for n in nomes] + list(extras)
        res = self.modelo.calcular(entradas=ins, saidas=refs)
        saida = {n: res[self.C[n]] for n in nomes}
        saida.update({x: res[x] for x in extras})
        return saida


def _ouro_planilha(r):
    """Números de ouro calculados NA PLANILHA: casos (a)–(m) da seção 5 do plano (com o dano
    da marreta lido de 29.7 v1.1), (n) cobertura de 100% dos campos das fichas 29.8 e 29.9 no
    mapa e (o) Sobreposição de 25.2 (v1.1)."""
    pl = Planilha()
    r.info(f"planilha carregada em {pl.modelo.tempo_carga:.1f} s")

    def conf(rotulo, obtido, esperado):
        r.ok(obtido == esperado, f"[planilha] {rotulo}: planilha={obtido!r} livro={esperado!r}")

    # (a) Nadir nível 1 — 29.7
    nomes = []
    for a in _ATR:
        nomes += [f"criacao.atributo.{_slug(a)}.atual", f"criacao.atributo.{_slug(a)}.bonus"]
    nomes += ["criacao.pv", "criacao.defesa", "criacao.esquiva", "criacao.rd", "nucleo.teto_rd",
              "criacao.velocidade", "criacao.dt", "criacao.ataque_habilidade",
              "criacao.ataque_habilidade.rolagem", "nucleo.ph_inicio", "nucleo.ph_max",
              "criacao.pericias.com_eficiencia", "testes.pericias_com_eficiencia",
              "criacao.pericias.permitidas", "caminho.pacto.custo_pv", "caminho.pacto.bonus",
              "caminho.pacto.bonus_ferido", "caminho.pacto.limiar_pv"]
    nomes_tr = {"Potência Física": 6, "Reflexos": 3, "Resistência Física": 4, "Resistência Mental": 1,
                "Percepção Mental": 3, "Força de Vontade": 2}
    nomes += [f"testes.tr.{_slug(t)}.total" for t in nomes_tr]
    s = pl.calcular(_nadir(), nomes, extras=pl.avisos())
    for a, (v, b) in {"Poder": (17, 4), "Vigor": (14, 2), "Agilidade": (13, 1),
                      "Discernimento": (12, 1), "Presença": (10, 0), "Sincronia": (8, -1)}.items():
        conf(f"(a) {a}", (s[f"criacao.atributo.{_slug(a)}.atual"], s[f"criacao.atributo.{_slug(a)}.bonus"]),
             (v, b))
    conf("(a) PV", s["criacao.pv"], 61)
    conf("(a) Defesa", s["criacao.defesa"], 16)
    conf("(a) Esquiva", s["criacao.esquiva"], 18)
    conf("(a) RD", s["criacao.rd"], 0)
    conf("(a) teto de RD", s["nucleo.teto_rd"], 6)
    conf("(a) VEL com Botas I (passo 12 de 29.7)", s["criacao.velocidade"], 14)
    conf("(a) VEL sem Relíquias (passo 8 do capítulo 03)",
         pl.calcular(_nadir(reliquias={}), ["criacao.velocidade"])["criacao.velocidade"], 12)
    conf("(a) DT das Habilidades", s["criacao.dt"], 14)
    conf("(a) Teste de Ataque das Habilidades", (s["criacao.ataque_habilidade"],
                                                 s["criacao.ataque_habilidade.rolagem"]), (6, "d20+6"))
    conf("(a) PH do grupo (início/máximo, mesa de 4)", (s["nucleo.ph_inicio"], s["nucleo.ph_max"]), (3, 5))
    conf("(a) Perícias com Eficiência", (s["criacao.pericias.com_eficiencia"],
                                         s["testes.pericias_com_eficiencia"]), (5, 5))
    # v1.2: Vocação Livre (05) dá +1 Perícia ao Humano, e a Nadir é Humana — de 2 para 3 (04.5)
    conf("(a) Perícias escolhidas permitidas", s["criacao.pericias.permitidas"], 3)
    conf("(a) Pacto da Ruína", (s["caminho.pacto.custo_pv"], s["caminho.pacto.bonus"],
                                s["caminho.pacto.bonus_ferido"], s["caminho.pacto.limiar_pv"]), (2, 2, 4, 30))
    for t, b in nomes_tr.items():
        conf(f"(a) TR {t}", s[f"testes.tr.{_slug(t)}.total"], b)
    ligados = [f"{x} = {s[x]!r}" for x in pl.avisos() if s[x] not in (None, "")]
    conf("(a) sem avisos na ficha da Nadir", ligados, [])
    # (a) equipamento, Habilidade e Ultimate (29.7 passos 9, 10 e 12) — dano da regra, lido de 29.7 (v1.1, D1)
    nm = ["equipamento.ab.principal.rolagem", "equipamento.ab.principal.texto", "equipamento.ab.principal.media",
          "equipamento.ab.principal.do_atributo", "equipamento.ab.principal.do_equipamento",
          "equipamento.ab.principal.elemento", "em_jogo.ab.principal.texto", "em_jogo.ab.principal.media",
          "em_jogo.ab.principal.do_atributo", "em_jogo.ab.principal.do_equipamento", "em_jogo.resumo.ataque",
          "habilidades.1.total", "habilidades.1.media", "habilidades.1.ph", "habilidades.1.rt",
          "habilidades.1.rolagem", "habilidades.ultimate.total", "habilidades.ultimate.media",
          "habilidades.ultimate.rt", "habilidades.ultimate.custo", "habilidades.ultimate.equivalente",
          "equipamento.inventario.capacidade", "criacao.status.habilidade", "criacao.status.ultimate",
          "em_jogo.resumo.pv", "inicio.painel.total"]
    s = pl.calcular(_nadir(), nm)
    conf("(a) Teste de Ataque do básico", s["equipamento.ab.principal.rolagem"], "d20+6")
    ab_txt, ab_med, ab_atr, ab_eq = _nadir_ab_livro()
    conf("(a) AB dano com Mãos I (29.7 v1.1)",
         (s["equipamento.ab.principal.texto"], s["equipamento.ab.principal.media"]), (ab_txt, ab_med))
    conf("(a) AB fixo: atributo + Mãos I",
         (s["equipamento.ab.principal.do_atributo"], s["equipamento.ab.principal.do_equipamento"]), (ab_atr, ab_eq))
    conf("(a) AB na Em Jogo",
         (s["em_jogo.ab.principal.texto"], s["em_jogo.ab.principal.media"], s["em_jogo.ab.principal.do_atributo"],
          s["em_jogo.ab.principal.do_equipamento"]), (ab_txt, ab_med, ab_atr, ab_eq))
    conf("(a) Melhor ataque no Resumo para o Jogador", s["em_jogo.resumo.ataque"],
         f"Ataque Básico d20+6 · {ab_txt} (média {ab_med})")
    conf("(a) AB Elemento", s["equipamento.ab.principal.elemento"], "Físico")
    conf("(a) Rebarba", (s["habilidades.1.total"], s["habilidades.1.media"], s["habilidades.1.ph"],
                         s["habilidades.1.rt"], s["habilidades.1.rolagem"]), ("6d6+4", 25, 1, 2, "d20+6"))
    conf("(a) A Doca Inteira", (s["habilidades.ultimate.total"], s["habilidades.ultimate.media"],
                                s["habilidades.ultimate.rt"], s["habilidades.ultimate.custo"],
                                s["habilidades.ultimate.equivalente"]), ("5d10+4", 31, 5, 100, 2))
    conf("(a) Espaço", s["equipamento.inventario.capacidade"], 18)
    conf("(a) passos 9 e 10 ligados à aba Habilidades",
         (s["criacao.status.habilidade"], s["criacao.status.ultimate"]), ("OK: Rebarba", "OK: A Doca Inteira"))
    conf("(a) PV no Resumo para o Jogador", s["em_jogo.resumo.pv"], "61 / 61")
    conf("(a) Painel de avisos zerado", s["inicio.painel.total"], 0)

    # (f) Barreira no 13 = 18 (15.2); teto de PV temporários no 11 = 15 (23.3)
    conf("(f) Barreira nível 13", pl.calcular(_nadir(nivel=13, caminho="A Preservação", bencaos=[],
                                                     atributo_habilidade="Vigor"),
                                              ["em_jogo.barreira_max"])["em_jogo.barreira_max"], 18)
    conf("(f) teto temporário nível 11",
         pl.calcular(_nadir(nivel=11), ["nucleo.teto_temporarios"])["nucleo.teto_temporarios"], 15)

    # (g) Descanso Curto (Vigor +2) — tabela de 23.6
    t = [x for x in _tabs(_trecho("23", "## 23.6")) if x[0][0] == "Nível"][0]
    for nv, esp in zip(t[0][1:], t[1][1:]):
        conf(f"(g) Descanso Curto nível {nv}",
             pl.calcular(_nadir(nivel=int(nv)), ["em_jogo.descanso_curto"])["em_jogo.descanso_curto"], _n(esp))

    # (h) Dano de Quebra — 20.5
    nq = ["criacao.quebra.texto", "criacao.quebra.media"]
    q3 = pl.calcular(_nadir(nivel=3, elemento="Físico"), nq)
    q19 = pl.calcular(_nadir(nivel=19, elemento="Físico"), nq)
    conf("(h) Físico nível 3", (q3["criacao.quebra.texto"], q3["criacao.quebra.media"]), ("2d6+4", 11))
    conf("(h) Físico nível 19", (q19["criacao.quebra.texto"], q19["criacao.quebra.media"]), ("2d6+16", 23))
    conf("(h) Gelo nível 3 e 19",
         (pl.calcular(_nadir(nivel=3, elemento="Gelo"), nq)["criacao.quebra.texto"],
          pl.calcular(_nadir(nivel=19, elemento="Gelo"), nq)["criacao.quebra.texto"]), ("2", "8"))

    # (i) Vesper nível 11, rifle (Disparo longo), Agilidade +5, Mãos Tier II — 18.5; Ultimate — 17.4
    vesper = _nadir(
        nivel=11, caminho="A Caça", elemento="Vento", atributo_habilidade="Agilidade",
        atributos={"Agilidade": 15, "Vigor": 14, "Discernimento": 13, "Poder": 12, "Presença": 10, "Sincronia": 8},
        bonus_racial={"modo": "Um Atributo (+2)", "attr1": "Agilidade"},
        aumentos={3: {"modo": "Um Atributo (+2)", "attr1": "Agilidade"},
                  6: {"modo": "Dois Atributos (+1 cada)", "attr1": "Agilidade", "attr2": "Vigor"}},
        arma={"categoria": "Disparo longo", "propriedade": "Nenhuma"}, bencaos=[],
        pericias_escolhidas=[], reliquias={"Mãos": {"conjunto": "—"}},
        ultimate={"tipo": "Dano", "area": False})
    nm = ["criacao.atributo.agilidade.bonus", "equipamento.ab.principal.texto", "equipamento.ab.principal.fraqueza",
          "habilidades.ultimate.dados", "equipamento.ab.principal.alcance"]
    sv = pl.calcular(vesper, nm)
    conf("(i) bônus de Agilidade", sv["criacao.atributo.agilidade.bonus"], 5)
    conf("(i) rifle no nível 11", sv["equipamento.ab.principal.texto"], "3d10+9")
    conf("(i) rifle contra Fraqueza", sv["equipamento.ab.principal.fraqueza"], "5d10+9")
    conf("(i) rifle: alcance", sv["equipamento.ab.principal.alcance"], "Longa")
    conf("(i) Ultimate nível 11", sv["habilidades.ultimate.dados"], "6d20")
    conf("(i) Ultimate nível 13", pl.calcular(dict(vesper, nivel=13), ["habilidades.ultimate.dados"])
         ["habilidades.ultimate.dados"], "10d20")

    # (j) Nadir nível 15, Tier III, Conjuntos 4+2 — 25.3
    rel = {"Cabeça": {"conjunto": "A"}, "Mãos": {"conjunto": "A"}, "Tronco": {"conjunto": "A"},
           "Botas": {"conjunto": "A"}, "Esfera Planar": {"conjunto": "B"}, "Corda de Ligação": {"conjunto": "B"}}
    nm = ["criacao.pv", "criacao.defesa", "criacao.velocidade", "equipamento.ab.principal.equip",
          "habilidades.1.fixo", "criacao.atributo.poder.bonus", "equipamento.reliquia.corda_de_ligacao.bonus",
          "equipamento.conjunto.a.ativo", "equipamento.conjunto.b.ativo", "equipamento.tier",
          "em_jogo.energia_equipamento"]
    b15 = pl.calcular(_nadir(nivel=15, reliquias={}), nm)
    n15 = pl.calcular(_nadir(nivel=15, reliquias=rel, esfera_elemento="Fogo",
                             conjuntos={"A": {"bonus2": "Um tipo de rolagem +1"},
                                        "B": {"bonus2": "Velocidade +1"}}), nm)
    conf("(j) Tier", n15["equipamento.tier"], "III")
    conf("(j) +PV", n15["criacao.pv"] - b15["criacao.pv"], 35)
    conf("(j) +Defesa", n15["criacao.defesa"] - b15["criacao.defesa"], 2)
    conf("(j) +VEL (Botas +4, Nó de Ferro +1)", n15["criacao.velocidade"] - b15["criacao.velocidade"], 5)
    conf("(j) +dano de Ataque Básico", n15["equipamento.ab.principal.equip"], 6)
    conf("(j) +dano de Fogo (Esfera Planar)", n15["habilidades.1.fixo"] - n15["criacao.atributo.poder.bonus"], 6)
    conf("(j) Corda de Ligação", n15["equipamento.reliquia.corda_de_ligacao.bonus"], 20)
    conf("(j) Conjuntos ativos", (n15["equipamento.conjunto.a.ativo"], n15["equipamento.conjunto.b.ativo"]),
         ("4 peças", "2 peças"))

    # (l) PH de 16.2 (3 a 6 jogadores × 3 degraus)
    for lin in _tab("16", "## 16.2", "Nº de jogadores")[1]:
        jg = _n(lin[0])
        mx = [int(x) for x in re.findall(r"\d+", lin[1])]
        ini = [int(x) for x in re.findall(r"\d+", lin[2])]
        for k, nv in enumerate((1, 9, 17)):
            sx = pl.calcular(_nadir(nivel=nv, jogadores=jg), ["nucleo.ph_max", "nucleo.ph_inicio"])
            conf(f"(l) PH {jg} jogadores nível {nv}", (sx["nucleo.ph_max"], sx["nucleo.ph_inicio"]), (mx[k], ini[k]))

    # (n) cobertura: todo campo das fichas 29.8 e 29.9 tem célula no mapa
    faltam = [f"{campo} -> {nome}" for campo, nomes in _campos_fichas_oficiais().items() for nome in nomes
              if nome not in pl.C]
    r.ok(not faltam, f"[planilha] (n) campos das fichas 29.8/29.9 sem célula no mapa: {faltam[:20]}")
    r.info(f"(n) cobertura: {len(_campos_fichas_oficiais())} campos das fichas 29.8 e 29.9, "
           f"{sum(len(v) for v in _campos_fichas_oficiais().values())} células conferidas no mapa")

    # (b) Atletismo +6 no nível 3 — 02.1
    s3 = pl.calcular(_nadir(nivel=3), ["testes.pericia.atletismo.total", "testes.pericia.atletismo.rolagem"])
    conf("(b) Atletismo nível 3", (s3["testes.pericia.atletismo.total"], s3["testes.pericia.atletismo.rolagem"]),
         (6, "d20+6"))

    # (c) Tabela de PV de 06.4 (20 níveis × 5 índices N, Bônus de Vigor +2)
    cab, linhas = _tab("06", "## 6.4", "Nível")
    por_n = {6: "A Destruição", 5: "A Preservação", 4: "A Inexistência", 3: "A Harmonia", 2: "A Caça"}
    for j, col in enumerate(cab[1:], start=1):
        n_ = int(re.search(r"N=(\d)", col).group(1))
        for lin in linhas:
            nv = _n(lin[0])
            sv = pl.calcular(_nadir(nivel=nv, caminho=por_n[n_], bencaos=[], atributo_habilidade=None),
                             ["criacao.pv"])
            conf(f"(c) PV N={n_} nível {nv}", sv["criacao.pv"], _n(lin[j]))

    # (d) Lin Hai: aumento de Vigor no nível 9 (+2 -> +3) dá +11 PV na hora — 04.3
    nm = ["criacao.atributo.vigor.bonus", "criacao.pv", "progressao.pv_ganho_vigor"]
    sem = pl.calcular(_nadir(nivel=9), nm)
    com = pl.calcular(_nadir(nivel=9, aumentos={9: {"modo": "Um Atributo (+2)", "attr1": "Vigor"}}), nm)
    conf("(d) bônus de Vigor 9", (sem["criacao.atributo.vigor.bonus"], com["criacao.atributo.vigor.bonus"]),
         (2, 3))
    conf("(d) ganho de PV na hora", com["criacao.pv"] - sem["criacao.pv"], 11)
    conf("(d) nível + 2", com["progressao.pv_ganho_vigor"], 11)

    # (e) Memoespírito nível 17 — 11.4 (mesma ficha do caso de oráculo)
    recorda = _nadir(
        nivel=17, raca="Intellitron", caminho="A Recordação", bonus_racial={"attr1": "Sincronia"},
        atributos={"Sincronia": 15, "Poder": 14, "Agilidade": 13, "Vigor": 12, "Discernimento": 10,
                   "Presença": 8},
        aumentos={3: {"modo": "Um Atributo (+2)", "attr1": "Sincronia"},
                  6: {"modo": "Dois Atributos (+1 cada)", "attr1": "Sincronia", "attr2": "Vigor"}},
        atributo_habilidade="Sincronia", bencaos=[], pericias_escolhidas=[],
        memoespirito={"pontos": {"Sincronia": 5, "Agilidade": 4, "Vigor": 5},
                      "atributo_ataque": "Sincronia", "funcao": "Controlador",
                      "bonus_menores": ["Memória Afiada", "Vínculo Profundo", "Forma Mutável"],
                      "evolucoes": []})
    nm = ["criacao.atributo.sincronia.atual", "criacao.atributo.sincronia.bonus", "nucleo.eficiencia",
          "memo.pv", "memo.defesa", "memo.velocidade", "memo.ataque", "memo.ataque.rolagem", "memo.dano",
          "memo.media", "memo.media_fraqueza", "memo.rt"]
    sm = pl.calcular(recorda, nm)
    conf("(e) dono: Sincronia/Bônus/Eficiência", (sm["criacao.atributo.sincronia.atual"],
                                                  sm["criacao.atributo.sincronia.bonus"],
                                                  sm["nucleo.eficiencia"]), (20, 5, 7))
    conf("(e) PV", sm["memo.pv"], 151)
    conf("(e) Defesa", sm["memo.defesa"], 21)
    conf("(e) Velocidade", sm["memo.velocidade"], 15)
    conf("(e) Teste de Ataque", (sm["memo.ataque"], sm["memo.ataque.rolagem"]), (17, "d20+17"))
    conf("(e) Dano", (sm["memo.dano"], sm["memo.media"]), ("5d6+5", 22))
    conf("(e) Dano contra Fraqueza", sm["memo.media_fraqueza"], 29)
    conf("(e) Redução de Tenacidade", sm["memo.rt"], 2)

    # (e2) a mesma ficha com arma de ENERGIA — 11.4 (v1.2, E17): 6 dados no 17, não 5, porque a
    # arma de Energia começa em 2 (18.5 e 24.2). A face continua d6
    import copy as _copy
    en17 = _copy.deepcopy(recorda)
    en17["arma"] = {"categoria": "Energia", "propriedade": "Nenhuma"}
    se = pl.calcular(en17, ["memo.n", "memo.dano", "memo.media", "memo.media_fraqueza"])
    conf("(e2) Energia, nível 17: 6 dados", (se["memo.n"], se["memo.dano"], se["memo.media"]),
         (6, "6d6+5", 26))
    conf("(e2) Energia, nível 17: contra Fraqueza", se["memo.media_fraqueza"], 33)

    # (k) DT típica 8 + 5 + Eficiência — 22.3
    tipica = re.search(r"ou seja \*\*([\d / ]+)\*\*", _md("22")).group(1)
    esperado = [int(x) for x in tipica.split("/")]
    dts = []
    niveis = _niveis_referencia_22_3()
    for nv in niveis:
        sx = pl.calcular(_nadir(nivel=nv, aumentos={3: {"modo": "Um Atributo (+2)", "attr1": "Poder"}}),
                         ["criacao.atributo.poder.bonus", "criacao.dt"])
        conf(f"(k) Bônus do Atributo de Habilidade no nível {nv}", sx["criacao.atributo.poder.bonus"], 5)
        dts.append(sx["criacao.dt"])
    conf(f"(k) DT típica nas cinco faixas (níveis de referência {niveis}, 22.3 v1.1)", dts, esperado)

    # (m) Progressão = 26.2 linha a linha: a tabela da aba Progressão e os números do nível
    corpo_m = _tab("26", "## 26.2", "Nível")[1]
    desde = _reescreve_desde(corpo_m)
    campos = ["eficiencia", "eficacia_pericias", "eficacia_tr", "bencaos", "habilidades", "reescreve",
              "nivel_max_habilidade", "aumento", "dados_ab", "especializacao", "teto_rd"]
    tabela = pl.calcular(None, [f"progressao.mestra.{n}.{c}" for n in range(1, 21) for c in campos])
    nucleo = ["nucleo.eficiencia", "nucleo.slots_eficacia_pericias", "nucleo.slots_eficacia_tr",
              "nucleo.bencaos", "nucleo.habilidades_conhecidas", "nucleo.reescreve",
              "nucleo.nivel_max_habilidade", "nucleo.aumento_neste_nivel", "nucleo.dados_ab",
              "nucleo.especializacao", "nucleo.teto_rd", "nucleo.eficacia"]
    for lin in corpo_m:
        nv = _n(lin[0])
        mm = re.search(r"(\d+) P / (\d+) TR", lin[2])
        p_, t_ = (int(mm.group(1)), int(mm.group(2))) if mm else (0, 0)
        esperado = (_n(lin[1]), p_, t_, _n(lin[3]), _n(lin[4]), "Sim" if nv >= desde else "Não", _n(lin[5]),
                    "Sim" if _n(lin[6]) is not None else "Não", _n(lin[7]), _n(lin[8]) or 0, _n(lin[9]))
        conf(f"(m) aba Progressão, linha do nível {nv}",
             tuple(tabela[f"progressao.mestra.{nv}.{c}"] for c in campos), esperado)
        sx = pl.calcular(_nadir(nivel=nv), nucleo)
        conf(f"(m) números do nível {nv} (Criação)", tuple(sx[x] for x in nucleo[:-1]), esperado)
        conf(f"(m) Eficácia = 2 × Eficiência no nível {nv}", sx["nucleo.eficacia"], 2 * esperado[0])

    # (o) Sobreposição — 25.2 (v1.1, D5), na aba Equipamento
    for rotulo, cone, esperado, acima in _casos_sobreposicao_25_2():
        sx = pl.calcular(_nadir(nivel=20, cone=cone), ["equipamento.cone.numerico", "equipamento.cone.pv",
                                                         "equipamento.aviso.cone.sobreposicoes"])
        conf(f"(o) {rotulo}", (sx["equipamento.cone.numerico"], sx["equipamento.cone.pv"],
                               "teto" in (sx["equipamento.aviso.cone.sobreposicoes"] or "")), esperado + (acima,))
    r.info("planilha: casos (a)–(o) comparados, calculados na planilha pela biblioteca formulas")
    _ouro_exemplo_nadir(r, pl)


def _ouro_exemplo_nadir(r, pl):
    """(p) O entregável 'Ficha Exemplo - Nadir.xlsx': fullCalcOnLoad ligado, as entradas
    gravadas são as da Nadir de 29.7 e TODA célula com fórmula, calculada a partir do próprio
    arquivo, dá o mesmo valor que o modelo em branco com as entradas da Nadir. Sem aviso."""
    import openpyxl
    if not XLSX_NADIR.exists():
        r.falha(f"(p) exemplo não encontrado: {XLSX_NADIR}")
        return
    wb = openpyxl.load_workbook(XLSX_NADIR)
    r.ok(bool(wb.calculation.fullCalcOnLoad), "(p) Ficha Exemplo - Nadir: fullCalcOnLoad desligado")
    entradas = entradas_nadir_exemplo(pl.mapa)
    for ref, v in entradas.items():
        aba, cel = separar_ref(ref)
        r.ok(wb[aba][cel].value == v, f"(p) entrada {ref}: arquivo={wb[aba][cel].value!r} Nadir={v!r}")
    refs, _ = _formulas_da_planilha()
    ex = Modelo(XLSX_NADIR).calcular(entradas={}, saidas=refs)
    mod = pl.modelo.calcular(entradas=entradas, saidas=refs)
    difs = [f"{k}: exemplo={ex[k]!r} modelo={mod[k]!r}" for k in refs if ex[k] != mod[k]]
    r.ok(not difs, f"(p) {len(difs)} célula(s) do exemplo diferem do modelo com a Nadir: {difs[:5]}")
    ligados = [f"{x} = {ex[x]!r}" for x in pl.avisos() if ex.get(x) not in (None, "")]
    r.ok(not ligados, f"(p) avisos acesos na Ficha Exemplo - Nadir: {ligados[:5]}")
    ab = ex[pl.C["em_jogo.ab.principal.texto"]], ex[pl.C["em_jogo.ab.principal.media"]]
    r.ok(ab == _nadir_ab_livro()[:2], f"(p) marreta na Em Jogo do exemplo: {ab!r}")
    r.info(f"(p) Ficha Exemplo - Nadir: {len(entradas)} entradas, {len(refs)} células com fórmula iguais ao "
           f"modelo, {len(difs)} diferença(s), {len(ligados)} aviso(s)")


def _campos_fichas_oficiais():
    """Campos das fichas em branco de 29.8 (personagem) e 29.9 (Memoespírito) -> nomes
    lógicos do mapa que os guardam. A suíte ouro (n) exige cobertura de 100%."""
    atr = ["Poder", "Agilidade", "Vigor", "Sincronia", "Discernimento", "Presença"]
    tr_ = ["Potência Física", "Reflexos", "Resistência Física", "Resistência Mental", "Percepção Mental",
           "Força de Vontade"]
    slots = ["Cabeça", "Mãos", "Tronco", "Botas", "Esfera Planar", "Corda de Ligação"]
    c = {
        "29.8 Nome": ["criacao.nome"], "29.8 Jogador": ["criacao.jogador"], "29.8 Nível": ["criacao.nivel"],
        "29.8 Raça": ["criacao.raca"], "29.8 Caminho": ["criacao.caminho"], "29.8 Elemento": ["criacao.elemento"],
        "29.8 Atributo de Habilidade": ["criacao.atributo_habilidade", "criacao.atributo_habilidade.usado"],
        "29.8 Propósito de Vida": ["criacao.proposito"],
        "29.8 Eficiência": ["nucleo.eficiencia"],
        "29.8 Eficácia P / TR": ["nucleo.eficacia", "nucleo.slots_eficacia_pericias", "nucleo.slots_eficacia_tr"],
        "29.8 Especialização": ["nucleo.especializacao"],
        "29.8 Bênçãos ___/10": ["caminho.bencoes.possuidas", "nucleo.bencaos"],
        "29.8 Habilidades ___/8": ["habilidades.preenchidas", "nucleo.habilidades_conhecidas"],
        "29.8 Nível máx. de Habilidade": ["nucleo.nivel_max_habilidade"],
        "29.8 PV ___/___": ["em_jogo.pv_atual", "criacao.pv"],
        "29.8 PV temporários (teto)": ["em_jogo.temporarios", "nucleo.teto_temporarios"],
        "29.8 Defesa": ["criacao.defesa"], "29.8 Esquiva": ["criacao.esquiva"],
        "29.8 RD (teto)": ["criacao.rd", "nucleo.teto_rd"], "29.8 Velocidade": ["criacao.velocidade"],
        "29.8 Energia ___/100": ["em_jogo.energia"], "29.8 PH do grupo ___/___": ["em_jogo.ph", "nucleo.ph_max"],
        "29.8 Esforço": ["em_jogo.esforco"],
        "29.8 Perícias com Eficiência (8 linhas)": [f"em_jogo.pericia.{k}.nome" for k in range(1, 9)],
        "29.8 Ultimate: Nome / Nível equivalente / Efeito": ["habilidades.ultimate.nome",
                                                             "habilidades.ultimate.equivalente",
                                                             "habilidades.ultimate.efeito"],
        "29.8 Bênçãos N1 a N19": [f"caminho.bencao.slot{k}.nome" for k in range(1, 11)],
        "29.8 Traços de Raça": ["criacao.raca.tracos_texto"],
        "29.8 Arma / Categoria / Dados / Elem": ["criacao.arma.nome", "criacao.arma.categoria",
                                                "equipamento.ab.principal.texto", "criacao.arma.elemento"],
        "29.8 Armadura / Defesa / RD": ["criacao.armadura", "criacao.armadura.defesa", "criacao.armadura.rd"],
        "29.8 Cone de Luz / Nível / Sobreposição": ["equipamento.cone.nome", "equipamento.cone.nivel",
                                                    "equipamento.cone.sobreposicoes"],
        "29.8 Conjuntos": [f"equipamento.conjunto.{x}.nome" for x in "abc"],
        "29.8 Inventário: Espaço": ["equipamento.inventario.capacidade", "equipamento.inventario.ocupado"]
                                   + [f"equipamento.inventario.{k}.item" for k in range(1, 21)],
        "29.8 Condições ativas": [f"em_jogo.condicao.{k}.nome" for k in range(1, 5)] + ["em_jogo.resumo.condicoes"],
        "29.8 Ressonâncias I a IV": [f"progressao.ressonancia.{x}.opcao" for x in ("I", "II", "III", "IV")],
        "29.9 Nome": ["memo.nome"], "29.9 Dono / Nível do dono": ["criacao.nome", "nucleo.nivel"],
        "29.9 Conceito": ["memo.conceito"], "29.9 Função": ["memo.funcao"], "29.9 Elemento": ["memo.elemento"],
        "29.9 Total disponível / Gastos": ["memo.pontos_total", "memo.pontos_gastos"],
        "29.9 Pontos: Ataque / Agilidade / Vigor / Outros": ["memo.atributo_ataque"]
                                                            + [f"memo.pontos.{_slug(a)}" for a in atr],
        "29.9 PV ___/___": ["em_jogo.memo_pv", "memo.pv"], "29.9 Defesa": ["memo.defesa"],
        "29.9 Velocidade": ["memo.velocidade"], "29.9 Teste de Ataque": ["memo.ataque", "memo.ataque.rolagem"],
        "29.9 Dano": ["memo.dano"], "29.9 Redução de Tenacidade": ["memo.rt"],
        "29.9 Testes de Resistência": [f"memo.tr.{_slug(a)}" for a in atr], "29.9 RD": ["memo.rd"],
        "29.9 3 Bônus menores": [f"memo.bonus_menor.{k}" for k in (1, 2, 3)],
        "29.9 Habilidade ofensiva / auxiliar": ["memo.tecnica_principal.nome", "memo.tecnica_principal.texto",
                                                "memo.tecnica_auxiliar.nome", "memo.tecnica_auxiliar.texto"],
        "29.9 Evoluções": [f"memo.evolucao.{k}" for k in (1, 2, 3)],
    }
    for a in atr:
        c[f"29.8 Atributo {a} (valor e bônus)"] = [f"criacao.atributo.{_slug(a)}.atual",
                                                   f"criacao.atributo.{_slug(a)}.bonus"]
    for t in tr_:
        c[f"29.8 Teste de Resistência {t}"] = [f"testes.tr.{_slug(t)}.total", f"testes.tr.{_slug(t)}.rolagem"]
    for k in range(1, 9):
        c[f"29.8 Habilidade {k}: Nome / Nível / Tipo / Dados + atrib. / PH / Alcance / Ten."] = [
            f"habilidades.{k}.{x}" for x in ("nome", "nivel", "tipo", "total", "ph", "alcance", "rt")]
    for s_ in slots:
        c[f"29.8 Relíquia {s_}"] = [f"equipamento.reliquia.{_slug(s_)}.possui",
                                    f"equipamento.reliquia.{_slug(s_)}.bonus"]
    return c


# ---------------------------------------------------------------------------
# Suíte extremos — nenhum valor de erro em estado algum
# ---------------------------------------------------------------------------

def _formulas_da_planilha():
    import openpyxl
    wb = openpyxl.load_workbook(XLSX)
    refs = []
    for ws in wb.worksheets:
        for linha in ws.iter_rows():
            for c in linha:
                if isinstance(c.value, str) and c.value.startswith("="):
                    refs.append(f"'{ws.title}'!{c.coordinate}")
    valores_lista = {}
    dados = wb["Dados"]
    for nome, intervalo in (ler_mapa() or {}).get("listas", {}).items():
        valores_lista[nome] = [linha[0] for linha in _ler_intervalo(dados, intervalo)
                               if linha[0] not in (None, "")]
    return refs, valores_lista


_EXT = {}          # estado de cada processo de trabalho da suíte extremos


def _extremos_iniciar():
    """Inicializa um processo de trabalho: carrega a planilha uma vez."""
    pl = Planilha()
    refs, _ = _formulas_da_planilha()
    _EXT.update(pl=pl, refs=refs, avisos=pl.avisos())


def _valor_de_erro(codigo):
    """Valor de erro do mesmo tipo que a `formulas` produz (#VALUE!, #N/A...), para injetar
    numa entrada: é o que o Google mostra quando lê como fórmula o que o jogador digitou."""
    from formulas.functions import Error
    return Error.errors[codigo]


def _extremos_trabalhar(cenario):
    """Calcula TODAS as células com fórmula de um cenário e devolve só o resumo."""
    rotulo, entradas, esperados, sem_aviso = cenario
    pl, refs, avisos = _EXT["pl"], _EXT["refs"], _EXT["avisos"]
    entradas = {k: (_valor_de_erro(v[1]) if isinstance(v, tuple) and v[0] == "ERRO" else v)
                for k, v in entradas.items()}
    res = pl.modelo.calcular(entradas=entradas, saidas=refs + avisos)
    erros = [f"{k} = {v}" for k, v in res.items() if eh_erro(v)]
    ligados = [f"{k} = {res[k]!r}" for k in avisos if res.get(k) not in (None, "")] if sem_aviso else []
    faltando = [(nome, ref, res.get(ref)) for nome, ref in esperados if res.get(ref) in (None, "")]
    total = res.get(pl.C["inicio.erros.total"])
    return rotulo, len(erros), erros[:8], ligados[:8], faltando, total


def suite_extremos(args):
    import multiprocessing as mp
    r = Resultado("extremos")
    if not XLSX.exists():
        r.falha(f"planilha não encontrada: {XLSX}")
        return r
    mapa = ler_mapa()
    C, ent = mapa["celulas"], mapa.get("entradas", {})
    refs, listas = _formulas_da_planilha()
    avisos = [f"'{aba}'!{c}" for aba, cs in mapa.get("avisos", {}).items() for c in cs]
    r.info(f"{len(refs)} células com fórmula; {len(ent)} entradas; {len(avisos)} células de aviso")

    class _Pl:  # o processo principal só precisa do mapa
        pass
    pl = _Pl()
    pl.mapa = mapa

    cenarios = []

    def rodar(rotulo, entradas, avisos_esperados=(), sem_aviso=False):
        """Guarda o cenário; todos rodam no fim, em paralelo (_extremos_trabalhar)."""
        cenarios.append((rotulo, entradas, [(n, C[n]) for n in avisos_esperados], sem_aviso))

    def e(**pares):
        return {C[k.replace("__", ".")]: v for k, v in pares.items()}

    t0 = time.time()
    rodar("ficha em branco", {}, sem_aviso=True)
    rodar("só nome", {C["criacao.nome"]: "Nadir"}, sem_aviso=True)
    for raca in listas.get("lista.racas", []):
        rodar(f"só Raça = {raca}", {C["criacao.raca"]: raca})
    for cam in listas.get("lista.caminhos", []):
        rodar(f"só Caminho = {cam}", {C["criacao.caminho"]: cam})
    # Um campo por vez: valor válido de amostra e valor inválido
    n_campos = 0
    for nome, info in ent.items():
        for tipo_valor in ("amostra", "invalido"):
            v = info.get(tipo_valor)
            if v is None:
                continue
            rodar(f"só {nome} = {v!r}", {C[nome]: v})
            n_campos += 1
    r.info(f"{n_campos} cenários de um campo por vez")

    # Inválidos com aviso esperado na coluna certa
    casos = [
        ("nível 0", e(criacao__nivel=0), ["criacao.aviso.nivel"]),
        ("nível 21", e(criacao__nivel=21), ["criacao.aviso.nivel"]),
        ("nível 'abc'", e(criacao__nivel="abc"), ["criacao.aviso.nivel"]),
        ("nível 2,5", e(criacao__nivel=2.5), ["criacao.aviso.nivel"]),
        ("jogadores 0", e(criacao__jogadores=0), ["criacao.aviso.jogadores"]),
        ("jogadores 2", e(criacao__jogadores=2), ["criacao.aviso.jogadores"]),
        ("jogadores 'x'", e(criacao__jogadores="x"), ["criacao.aviso.jogadores"]),
        ("atributo 3", e(criacao__atributo__poder__distribuido=3), ["criacao.aviso.atributo.poder"]),
        ("atributo 25", e(criacao__atributo__poder__distribuido=25), ["criacao.aviso.atributo.poder"]),
        ("atributo 'abc'", e(criacao__atributo__vigor__distribuido="abc"), ["criacao.aviso.atributo.vigor"]),
        ("Raça inventada", e(criacao__raca="Marciano"), ["criacao.aviso.raca"]),
        ("Caminho inventado", e(criacao__caminho="A Ordem"), ["criacao.aviso.caminho"]),
        ("Bênção de outro Caminho colada",
         e(criacao__caminho="A Destruição", caminho__bencao__slot1__nome="Olho de Lan"),
         ["caminho.aviso.slot1"]),
        ("Bênção fora do catálogo",
         e(criacao__caminho="A Caça", caminho__bencao__slot1__nome="Bênção Inventada"), ["caminho.aviso.slot1"]),
        ("Bênção Tier II no slot do nível 1",
         e(criacao__nivel=20, criacao__caminho="A Caça", caminho__bencao__slot1__nome="Perseguição"),
         ["caminho.aviso.slot1"]),
        ("Bênção repetida",
         e(criacao__nivel=3, criacao__caminho="A Caça", caminho__bencao__slot1__nome="Olho de Lan",
           caminho__bencao__slot2__nome="Olho de Lan"), ["caminho.aviso.slot1", "caminho.aviso.slot2"]),
        ("Bênção em slot futuro",
         e(criacao__caminho="A Caça", caminho__bencao__slot3__nome="Olho de Lan"), ["caminho.aviso.slot3"]),
        ("array com valor repetido",
         {**e(criacao__metodo="Array oficial"),
          **{C[f"criacao.atributo.{_slug(a)}.distribuido"]: 15 for a in _ATR}}, ["criacao.aviso.array"]),
        ("Compra de Pontos acima de 28",
         {**e(criacao__metodo="Compra de Pontos"),
          **{C[f"criacao.atributo.{_slug(a)}.distribuido"]: 14 for a in _ATR}},
         ["criacao.aviso.compra"]),
        ("Humano +1/+1 no mesmo atributo",
         e(criacao__raca="Humano", criacao__raca__modo="Dois Atributos (+1 cada)", criacao__raca__atributo1="Poder",
           criacao__raca__atributo2="Poder"), ["criacao.aviso.raca_atributo1"]),
        # v1.2: o Vidyadhara passou a oferecer "Vigor ou Poder", então Poder deixou de ser
        # inválido para ele e o caso precisou de outro atributo fora do par (05)
        ("bônus racial fora das opções",
         e(criacao__raca="Vidyadhara", criacao__raca__atributo1="Presença"), ["criacao.aviso.raca_atributo1"]),
        ("aumento antes do nível", e(progressao__aumento__9__atributo1="Poder"), ["progressao.aviso.aumento.9"]),
        ("aumento +1/+1 no mesmo atributo",
         e(criacao__nivel=6, progressao__aumento__6__modo="Dois Atributos (+1 cada)", progressao__aumento__6__atributo1="Vigor",
           progressao__aumento__6__atributo2="Vigor"), ["progressao.aviso.aumento.6"]),
        ("aumento desperdiçado acima de 20",
         {**e(criacao__nivel=20, criacao__raca="Humano", criacao__raca__atributo1="Poder",
              criacao__atributo__poder__distribuido=15),
          **{C[f"progressao.aumento.{n}.atributo1"]: "Poder" for n in (3, 6, 9)}},
         ["criacao.aviso.atributo.poder"]),
        ("Perícia do Caminho escolhida",
         e(criacao__caminho="A Destruição", criacao__pericia__atletismo__escolhida="Sim"),
         ["criacao.aviso.pericia.atletismo"]),
        ("Perícias escolhidas a mais",
         e(criacao__pericia__tecnologia__escolhida="Sim", criacao__pericia__pesquisa__escolhida="Sim",
           criacao__pericia__ciencia__escolhida="Sim"), ["criacao.aviso.pericias", "criacao.aviso.pericia.ciencia"]),
        ("Eficácia sem Eficiência", e(criacao__nivel=5, testes__pericia__furtividade__eficacia="Sim"),
         ["testes.aviso.pericia.furtividade"]),
        ("Eficácia em TR acima dos slots", e(testes__tr__reflexos__eficacia="Sim"), ["testes.aviso.tr.reflexos"]),
        ("Esquiva com Pesada", e(criacao__armadura="Pesada"), ["criacao.aviso.esquiva"]),
        ("Atributo de Habilidade fora do Caminho",
         e(criacao__caminho="A Caça", criacao__atributo_habilidade="Poder"), ["criacao.aviso.atributo_habilidade"]),
        ("Memoespírito fora da Recordação", e(criacao__caminho="A Caça", memo__pontos__vigor=3),
         ["memo.aviso.fora_da_recordacao"]),
        ("Memoespírito com 6 pontos num Atributo",
         e(criacao__caminho="A Recordação", memo__pontos__vigor=6), ["memo.aviso.pontos.vigor"]),
        ("Memoespírito: pontos acima do total",
         {**e(criacao__caminho="A Recordação"), **{C[f"memo.pontos.{_slug(a)}"]: 5 for a in _ATR}},
         ["memo.aviso.pontos_total"]),
        ("Evolução antes do nível", e(criacao__caminho="A Recordação", memo__evolucao__1="Forma Completa"),
         ["memo.aviso.evolucao.1"]),
        ("Ressonância antes do nível", e(progressao__ressonancia__I__opcao="Velocidade +1"),
         ["progressao.aviso.ressonancia.I"]),
        ("propriedade de arma dupla", e(criacao__arma__propriedade="Arremessável, Dissimulada"),
         ["criacao.aviso.arma_propriedade"]),
        # --- abas de jogo (FEAT-003) ---------------------------------------------------
        ("Cone acima da faixa", e(equipamento__cone__nivel=3), ["equipamento.aviso.cone.nivel"]),
        ("Cone com texto no Nível", e(equipamento__cone__nivel="abc"), ["equipamento.aviso.cone.nivel"]),
        ("Sobreposições acima de uma por faixa", e(equipamento__cone__nivel=1, equipamento__cone__sobreposicoes=2),
         ["equipamento.aviso.cone.sobreposicoes"]),
        ("Cone em TR sem dizer qual", e(equipamento__cone__nivel=1, equipamento__cone__alvo="Um Teste de Resistência"),
         ["equipamento.aviso.cone.alvo"]),
        ("Cone: escolha no Nível 2 (e)", e(criacao__nivel=5, equipamento__cone__nivel=2, equipamento__cone__escolha="PV"),
         ["equipamento.aviso.cone.escolha"]),
        ("Cone: qual sem alvo de TR/Perícia", e(equipamento__cone__qual="Reflexos"), ["equipamento.aviso.cone.qual"]),
        ("Relíquia em Conjunto sem possuir", e(equipamento__reliquia__cabeca__conjunto="A"),
         ["equipamento.aviso.reliquia.cabeca"]),
        ("Conjuntos 2+2+2 com +2 de dano",
         {**{C[f"equipamento.reliquia.{s}.possui"]: "Sim" for s in
             ("cabeca", "maos", "tronco", "botas", "esfera_planar", "corda_de_ligacao")},
          **{C[f"equipamento.reliquia.{s}.conjunto"]: x for s, x in
             (("cabeca", "A"), ("maos", "A"), ("tronco", "B"), ("botas", "B"), ("esfera_planar", "C"),
              ("corda_de_ligacao", "C"))},
          **{C[f"equipamento.conjunto.{x}.bonus2"]: "Dano +2" for x in "abc"}}, ["equipamento.aviso.conjuntos"]),
        ("Conjunto: rolagem sem o bônus de rolagem",
         e(equipamento__conjunto__a__rolagem="Reflexos", equipamento__conjunto__a__bonus2="RD +1"),
         ["equipamento.aviso.conjunto.a"]),
        ("Esfera Planar com Elemento inventado", e(equipamento__esfera__elemento="Plasma"),
         ["equipamento.aviso.reliquia.esfera_planar"]),
        ("Arma secundária Média sem atributo", e(equipamento__arma2__categoria="Média"), ["equipamento.aviso.arma2"]),
        ("Arma secundária sem categoria", e(equipamento__arma2__nome="Faca"), ["equipamento.aviso.arma2"]),
        ("inventário acima da capacidade", e(equipamento__inventario__1__item="Traje de vedação",
                                             equipamento__inventario__1__qtd=5), ["equipamento.aviso.inventario"]),
        ("inventário acima do dobro", e(equipamento__inventario__1__item="Traje de vedação",
                                        equipamento__inventario__1__qtd=9), ["equipamento.aviso.inventario"]),
        ("item fora do catálogo sem Espaço", e(equipamento__inventario__1__item="Coisa"),
         ["equipamento.aviso.inventario.1"]),
        ("quantidade sem item", e(equipamento__inventario__2__qtd=3), ["equipamento.aviso.inventario.2"]),
        ("Créditos com texto", e(equipamento__creditos__lancamento__1__valor="abc"), ["equipamento.aviso.creditos.1"]),
        ("saldo negativo", e(equipamento__creditos__inicial=10, equipamento__creditos__lancamento__1__valor=-50),
         ["equipamento.aviso.creditos.saldo"]),
        ("Habilidade acima do Nível máximo", e(habilidades__1__tipo="Dano", habilidades__1__nivel=3),
         ["habilidades.aviso.1"]),
        ("Habilidade sem Tipo", e(habilidades__1__nome="Golpe"), ["habilidades.aviso.1"]),
        ("Nível de Habilidade 9 no nível 20", e(criacao__nivel=20, habilidades__1__tipo="Dano", habilidades__1__nivel=9),
         ["habilidades.aviso.1"]),
        ("Nível de Habilidade 'abc'", e(habilidades__1__tipo="Dano", habilidades__1__nivel="abc"),
         ["habilidades.aviso.1"]),
        ("Nível de Habilidade 0", e(habilidades__1__tipo="Cura", habilidades__1__nivel=0), ["habilidades.aviso.1"]),
        ("Habilidades a mais", e(habilidades__1__tipo="Dano", habilidades__2__tipo="Cura"),
         ["habilidades.aviso.2", "habilidades.aviso.contagem"]),
        ("alcance acima do Nível", e(habilidades__1__tipo="Dano", habilidades__1__alcance="Longa"),
         ["habilidades.aviso.1"]),
        ("Ressonância III em duas Habilidades",
         e(criacao__nivel=15, progressao__ressonancia__III__opcao="Uma Habilidade sobe 1 Nível de efeito",
           habilidades__1__tipo="Dano", habilidades__1__ress3="Sim", habilidades__2__tipo="Dano",
           habilidades__2__ress3="Sim"), ["habilidades.aviso.ress3", "habilidades.aviso.2"]),
        ("Ressonância III antes do nível", e(habilidades__1__tipo="Dano", habilidades__1__ress3="Sim"),
         ["habilidades.aviso.1"]),
        ("Ultimate com Tipo inventado", e(habilidades__ultimate__tipo="Ataque"), ["habilidades.aviso.ultimate"]),
        ("PV atual acima do máximo", e(em_jogo__pv_atual=999), ["em_jogo.aviso.pv"]),
        ("PV atual com texto", e(em_jogo__pv_atual="cheio"), ["em_jogo.aviso.pv"]),
        ("PV temporários acima do teto", e(em_jogo__temporarios=50), ["em_jogo.aviso.temporarios"]),
        ("Energia acima de 100", e(em_jogo__energia=130), ["em_jogo.aviso.energia"]),
        ("PH acima do máximo", e(em_jogo__ph=9), ["em_jogo.aviso.ph"]),
        ("Esforço fora do Humano", e(criacao__raca="Vulpes", em_jogo__esforco=1), ["em_jogo.aviso.esforco"]),
        ("Memoespírito ativo fora da Recordação", e(criacao__caminho="A Caça", em_jogo__memo_ativo="Sim"),
         ["em_jogo.aviso.memo"]),
        ("PV do Memoespírito acima do máximo", e(criacao__caminho="A Recordação", em_jogo__memo_pv=999),
         ["em_jogo.aviso.memo"]),
        ("acúmulo sem Bênção", e(em_jogo__acumulo__a=2), ["em_jogo.aviso.acumulo.a"]),
        ("Fúria acima do máximo", e(criacao__caminho="A Destruição", caminho__bencao__slot1__nome="Sacrifício Desesperado",
                                    em_jogo__acumulo__a=3), ["em_jogo.aviso.acumulo.a"]),
        ("Marcas sem Bênção", e(em_jogo__acumulo__b=1), ["em_jogo.aviso.acumulo.b"]),
        ("Florescimento acima do teto (Defesa e TR)",
         e(criacao__caminho="A Abundância", caminho__bencao__slot1__nome="Florescimento da Alma", em_jogo__acumulo__a=5),
         ["em_jogo.aviso.temporarios_teto", "testes.aviso.tr.reflexos"]),
        ("condição Quebrado", e(em_jogo__condicao__1__nome="Quebrado"), ["em_jogo.aviso.condicao.1"]),
        ("condição inventada", e(em_jogo__condicao__2__nome="Tonto"), ["em_jogo.aviso.condicao.2"]),
        ("Surpreso", e(em_jogo__condicao__1__nome="Surpreso"), ["em_jogo.aviso.surpreso"]),
        ("contador de Morrendo com PV", e(em_jogo__morrendo__sucessos=1), ["em_jogo.aviso.morrendo"]),
        ("Descanso Curto 3 vezes", e(em_jogo__uso__1__usados=3), ["em_jogo.aviso.descanso"]),
        ("dano com texto", e(em_jogo__dano__bruto="muito"), ["em_jogo.aviso.dano"]),
        ("cura com texto", e(em_jogo__cura="muita"), ["em_jogo.aviso.cura"]),
        ("Forma do Avatar sem a Bênção", e(caminho__escolha__avatar="Sincronizada"),
         ["caminho.aviso.escolha.avatar"]),
        ("Memória sem a Bênção", e(caminho__escolha__fragmentos="Guarda"), ["caminho.aviso.escolha.fragmentos"]),
    ]
    for rotulo, entradas, esperados in casos:
        rodar(rotulo, entradas, esperados)
    # Em Jogo cheia: Silenciado + Controlado + Lentidão, Morrendo, dano e cura
    rodar("Em Jogo com condições e Morrendo",
          {**_entradas_planilha(_nadir(nivel=9, habilidades=[
              {"nome": "Rebarba", "tipo": "Dano", "nivel": 4, "area": True, "resolucao": "Teste de Ataque"}]),
              pl.mapa),
           **e(em_jogo__pv_atual=0, em_jogo__dano__bruto=12, em_jogo__dano__continuo="Sim", em_jogo__cura=5,
               em_jogo__condicao__1__nome="Silenciado", em_jogo__condicao__2__nome="Controlado",
               em_jogo__condicao__3__nome="Lentidão", em_jogo__condicao__4__nome="Sangramento",
               em_jogo__condicao__4__eficiencia=4, em_jogo__morrendo__sucessos=2, em_jogo__morrendo__falhas=1,
               em_jogo__energia=100, em_jogo__temporarios=4)})

    # Fichas completas
    o = _oraculo()
    rodar("Nadir completa (29.7)", _entradas_planilha(_nadir(), pl.mapa), sem_aviso=True)
    completo = _nadir(
        nivel=20, raca="Xianzhouíta", caminho="A Recordação", bonus_racial={"attr1": "Sincronia"},
        atributo_habilidade="Sincronia", eficacia_pericias=["Intimidação", "Investigação", "Ciência"],
        eficacia_tr=["Reflexos", "Força de Vontade", "Resistência Mental"],
        aumentos={n: {"modo": "Dois Atributos (+1 cada)", "attr1": "Sincronia", "attr2": "Agilidade"} for n in (3, 6, 9, 12, 15, 18)},
        bencaos=[b for b, info in o.catalogo_bencaos().items() if info[0] == "A Recordação"][:10],
        ressonancias={"I": "Velocidade +1", "II": "Ultimate com efeito extra",
                      "III": "Uma Habilidade sobe 1 Nível de efeito", "IV": "Ultimate com 80 de Energia"},
        memoespirito={"pontos": {"Sincronia": 5, "Agilidade": 5, "Vigor": 5, "Poder": 5, "Presença": 2},
                      "atributo_ataque": "Sincronia", "funcao": "Guardião",
                      "bonus_menores": ["Força Espiritual", "Resistência Espiritual", "Velocidade Espiritual"],
                      "evolucoes": ["Forma Completa", "Fusão de Memórias", "Memória Desperta"],
                      "memoria_desperta": "Velocidade"},
        # abas de jogo no máximo: 8 Habilidades (uma com Ressonância III), Cone 5 (já no teto, 25.2),
        # Tier IV com Conjuntos 4+2, inventário, Memoespírito ativo, Forma Sincronizada
        habilidades=[{"nome": f"H{k}", "tipo": t, "nivel": 7, "area": k % 2 == 0, "ress3": k == 1,
                      "resolucao": "Teste de Ataque" if k % 2 else "Teste de Resistência", "alcance": "Extrema"}
                     for k, t in enumerate(["Dano", "Cura", "Buff", "Debuff", "Passiva", "Dano", "Cura", "Dano"],
                                           start=1)],
        ultimate={"nome": "Fim", "tipo": "Controle", "area": True, "resolucao": "Teste de Resistência"},
        cone={"nivel": 5, "alvo": "Teste de Ataque", "escolha": "Numérico", "sobreposicoes": 0},  # 25.2: o 5 já está no teto
        reliquias={"Cabeça": {"conjunto": "A"}, "Mãos": {"conjunto": "A"}, "Tronco": {"conjunto": "A"},
                   "Botas": {"conjunto": "A"}, "Esfera Planar": {"conjunto": "B"},
                   "Corda de Ligação": {"conjunto": "B"}},
        esfera_elemento="Fogo", conjuntos={"A": {"bonus2": "Um tipo de rolagem +1", "rolagem": "Teste de Ataque"},
                                           "B": {"bonus2": "Dano +2"}},
        inventario=[{"item": "Poção de Vida Média", "qtd": 3}, {"item": "Bastão", "espaco": 1.5, "qtd": 1}],
        pv_atual=40, memo_ativo=True, forma_avatar="Sincronizada", fragmento="Guarda",
        acumulos={"Fragmentos de Memória": 4})
    rodar("Recordação nível 20 completa", _entradas_planilha(completo, pl.mapa))
    caca = _nadir(nivel=20, raca="Intellitron", caminho="A Caça", bonus_racial={"attr1": "Sincronia"},
                  armadura="Pesada", atributo_habilidade="Agilidade",
                  bencaos=["Olho de Lan", "Presa Escolhida", "Tiro Certeiro", "Caçador Incansável",
                           "Passos de Sombra", "Perseguição", "Dois Alvos, Uma Flecha", "Golpe no Ponto Cego",
                           "Avatar da Caça", "A Última Flecha"],
                  cone={"nivel": 4, "alvo": "Uma Perícia", "qual": "Furtividade"},
                  arma={"categoria": "Disparo longo", "propriedade": "Alcance estendido"})
    rodar("Caça nível 20 com Olho de Lan e Pesada", _entradas_planilha(caca, pl.mapa))
    destr = _nadir(nivel=12, bencaos=["Pacto da Ruína", "Sacrifício Desesperado", "Instinto de Sobrevivência",
                                      "Impacto Devastador", "Cicatriz da Destruição"],
                   pv_atual=20, acumulos={"Fúria": 2, "Marcas da Ruína": 5},
                   cone={"nivel": 3, "alvo": "Um Teste de Resistência", "qual": "Força de Vontade", "escolha": "PV"})
    rodar("Destruição nível 12 com acúmulos e Instinto", _entradas_planilha(destr, pl.mapa))

    # --- Revisão 2: valor de erro em cada entrada (o Google leu como fórmula o que se digitou) --
    # Todas as entradas (listas, texto livre e números), cada uma sozinha e também por cima da
    # Nadir completa nas entradas da Raça e do Nível: o erro fica na própria célula (contador = 1),
    # nenhuma outra célula fica com erro e o aviso da linha diz o que fazer.
    com_erro = set()
    sinal_aviso = {}
    wb_ = __import__("openpyxl").load_workbook(XLSX)
    av_set = set(avisos)
    for s, ents in mapa.get("sinais", {}).items():
        a, cel = separar_ref(s)
        alvo = [x for x in av_set if separar_ref(x)[0] == a
                and f"IF({cel}>0," in str(wb_[a][separar_ref(x)[1]].value or "")]
        for e_ in ents:
            sinal_aviso[e_] = alvo[0] if alvo else None
    n_tipo = {}
    codigos = ("#VALUE!", "#N/A")
    for k, (nome, info) in enumerate(sorted(ent.items())):
        ref = C[nome]
        codigo = codigos[k % 2]
        rot_ = f"[erro {codigo}] {nome}"
        com_erro.add(rot_)
        n_tipo[info["tipo"]] = n_tipo.get(info["tipo"], 0) + 1
        aviso_ = sinal_aviso.get(f"'{separar_ref(ref)[0]}'!{separar_ref(ref)[1]}")
        rodar(rot_, {ref: ("ERRO", codigo)})
        if aviso_:
            cenarios[-1] = (rot_, {ref: ("ERRO", codigo)}, [(aviso_, aviso_)], False)
        else:
            r.falha(f"{nome}: entrada sem aviso de erro na linha")
    nadir_ = _entradas_planilha(_nadir(), mapa)
    for nome in ("criacao.raca", "criacao.raca.modo", "criacao.raca.atributo1", "criacao.raca.atributo2",
                 "criacao.nivel", "criacao.atributo.poder.distribuido", "criacao.caminho"):
        rot_ = f"[erro #VALUE!] Nadir com {nome}"
        com_erro.add(rot_)
        rodar(rot_, {**nadir_, C[nome]: ("ERRO", "#VALUE!")})
    # o caso do usuário (Criação!B25:B28): Humano + bônus em erro + Poder + Agilidade
    rot_ = "[erro #VALUE!] caso do usuário: Humano, B26 em erro, Poder, Agilidade"
    com_erro.add(rot_)
    rodar(rot_, e(criacao__raca="Humano", criacao__raca__modo=("ERRO", "#VALUE!"), criacao__raca__atributo1="Poder",
                  criacao__raca__atributo2="Agilidade"), ["criacao.aviso.raca_modo"] if "criacao.aviso.raca_modo" in C
          else [])
    r.info(f"revisão 2: {len(com_erro)} cenários com valor de erro numa entrada ({len(ent)} entradas: "
           + ", ".join(f"{n} {t}" for t, n in sorted(n_tipo.items())) + "; mais 7 por cima da Nadir e o caso do usuário)")

    # --- Execução em paralelo: cada processo carrega a planilha uma vez -------------------
    n_proc = max(1, min(8, (os.cpu_count() or 2) - 1, len(cenarios)))
    r.info(f"{len(cenarios)} cenários em {n_proc} processo(s)")
    with mp.get_context("spawn").Pool(n_proc, initializer=_extremos_iniciar) as pool:
        por_rotulo = {c_[0]: c_ for c_ in cenarios}
        for rotulo, n_erros, erros, ligados, faltando, total in pool.imap_unordered(
                _extremos_trabalhar, cenarios, chunksize=4):
            r.ok(n_erros == 0, f"[{rotulo}] {n_erros} valor(es) de erro: {erros}")
            # revisão 2: o contador da Início mostra só a própria entrada com erro (1) ou nenhuma (0)
            r.ok(total == (1 if rotulo in com_erro else 0),
                 f"[{rotulo}] contador de erros da Início = {total!r}, esperado {1 if rotulo in com_erro else 0}")
            if por_rotulo[rotulo][3]:
                r.ok(not ligados, f"[{rotulo}] aviso falso na ficha sem erro: {ligados}")
            sem = {n for n, _, _ in faltando}
            for nome, ref in por_rotulo[rotulo][2]:
                r.ok(nome not in sem, f"[{rotulo}] esperava aviso em {nome} ({ref}), veio vazio")
    r.info(f"tempo dos cenários: {time.time() - t0:.0f} s")
    return r


# ---------------------------------------------------------------------------
# Suíte oraculo — teste diferencial planilha × oráculo
# ---------------------------------------------------------------------------

# Listas das escolhas (as mesmas opções que o jogador vê nos menus; o oráculo as entende
# pelo texto). Ficam aqui, no teste, para o gerador de cenários não depender da planilha.
_OR_ELEMENTOS = ["Físico", "Fogo", "Gelo", "Raio", "Vento", "Quântico", "Imaginário"]
_OR_ARMAS = ["Leve", "Média", "Pesada", "Disparo curto", "Disparo longo", "Energia"]
_OR_PROPRIEDADES = ["Nenhuma", "Arremessável", "Alcance estendido", "Peso de impacto", "Dissimulada"]
_OR_TIPOS = ["Dano", "Cura", "Buff", "Debuff", "Passiva"]
_OR_ULT_TIPOS = ["Dano", "Cura", "Buff", "Debuff", "Controle"]
_OR_RESOLUCAO = ["Teste de Ataque", "Teste de Resistência"]
_OR_ALCANCES = ["Pessoal", "Curta", "Média", "Longa", "Extrema"]
_OR_ALVO_CONE = ["PV máximos", "Defesa", "Velocidade", "Dano de Ataque Básico", "Dano de Habilidade",
                 "Dano de Ultimate", "RD", "Teste de Ataque", "Um Teste de Resistência", "Uma Perícia"]
_OR_SLOTS = ["Cabeça", "Mãos", "Tronco", "Botas", "Esfera Planar", "Corda de Ligação"]
_OR_BONUS2 = ["Um tipo de rolagem +1", "Velocidade +1", "Dano +2", "RD +1"]
_OR_RESS = {"I": ["Habilidade de Nível 3 ou menor sem PH (1 por combate)", "Velocidade +1"],
            "II": ["Ultimate com efeito extra"], "III": ["Uma Habilidade sobe 1 Nível de efeito"],
            "IV": ["Ultimate com 80 de Energia", "Avatar afeta um alvo adicional"]}
_OR_MEMO_FUNCAO = ["Predador", "Guardião", "Catalisador", "Controlador"]
_OR_MEMO_BONUS = ["Força Espiritual", "Resistência Espiritual", "Velocidade Espiritual", "Memória Afiada",
                  "Vínculo Profundo", "Forma Mutável"]
_OR_MEMO_EVOL = ["Forma Completa", "Fusão de Memórias", "Memória Desperta"]
_OR_PERICIAS = ["Atletismo", "Acrobacia", "Furtividade", "Pilotagem", "Resistência", "Tecnologia", "Pesquisa",
                "Ciência", "Mecânica", "Percepção", "Sobrevivência", "Intuição", "Investigação", "Persuasão",
                "Intimidação", "Enganação", "Liderança", "Sintonia"]
_OR_TR = ["Potência Física", "Reflexos", "Resistência Física", "Resistência Mental", "Percepção Mental",
          "Força de Vontade"]
_OR_NIVEL_MAX_HAB = (1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7)
_OR_ALCANCE_MAX = {1: 1, 2: 2, 3: 3}                       # índice em _OR_ALCANCES (4+: Extrema)

# Aviso da planilha (nome lógico, '*' = qualquer sufixo) -> códigos do oráculo que o explicam.
# Mão dupla: (1) todo aviso aceso na planilha precisa de um código do oráculo que o explique;
# (2) todo código do oráculo precisa acender pelo menos uma célula que o explique.
_OR_AVISOS = [
    ("criacao.aviso.nivel", {"NIVEL_FORA"}),
    ("criacao.aviso.jogadores", {"JOGADORES_INVALIDO", "JOGADORES_FORA_DA_TABELA"}),
    ("criacao.aviso.raca_atributo1", {"BONUS_RACIAL_INVALIDO", "BONUS_RACIAL_MESMO_ATRIBUTO"}),
    ("criacao.aviso.raca_atributo2", {"BONUS_RACIAL_INVALIDO", "BONUS_RACIAL_MESMO_ATRIBUTO"}),
    ("criacao.aviso.atributo.*", {"ATRIBUTO_FORA_8_20", "ATRIBUTO_ACIMA_15_NA_CRIACAO", "AUMENTO_DESPERDICADO"}),
    ("criacao.aviso.array", {"ARRAY_INVALIDO"}),
    ("criacao.aviso.compra", {"COMPRA_ACIMA_DE_28"}),
    ("criacao.aviso.atributo_habilidade", {"ATRIBUTO_HABILIDADE_INVALIDO"}),
    ("criacao.aviso.pericia.*", {"PERICIA_DO_CAMINHO_ESCOLHIDA", "PERICIAS_A_MAIS"}),
    ("criacao.aviso.pericias", {"PERICIAS_A_MAIS"}),
    ("criacao.aviso.esquiva", {"ESQUIVA_PROIBIDA"}),
    ("criacao.aviso.rd", {"RD_NO_TETO"}),
    ("criacao.aviso.velocidade", {"VEL_FORA_7_25"}),
    ("progressao.aviso.aumento.*", {"AUMENTO_MESMO_ATRIBUTO", "AUMENTO_ANTES_DO_NIVEL"}),
    ("progressao.aviso.ressonancia.*", {"RESSONANCIA_ANTES_DO_NIVEL"}),
    ("testes.aviso.pericia.*", {"EFICACIA_SEM_EFICIENCIA", "EFICACIA_PERICIAS_A_MAIS"}),
    ("testes.aviso.tr.*", {"EFICACIA_TR_A_MAIS", "BONUS_TEMPORARIO_NO_TETO"}),
    ("caminho.aviso.slot*", {"BENCAO_EM_SLOT_FUTURO", "BENCAO_TIER_ACIMA_DO_SLOT", "BENCAO_REPETIDA",
                             "BENCAO_DE_OUTRO_CAMINHO"}),
    ("memo.aviso.pontos.*", {"MEMO_ATRIBUTO_ACIMA_5"}),
    ("memo.aviso.pontos_total", {"MEMO_PONTOS_A_MAIS"}),
    ("memo.aviso.bonus_menor.*", {"MEMO_BONUS_MENORES"}),
    ("memo.aviso.evolucao.*", {"MEMO_EVOLUCAO_ANTES_DO_NIVEL", "MEMO_EVOLUCAO_REPETIDA"}),
    ("memo.aviso.fora_da_recordacao", {"MEMO_FORA_DA_RECORDACAO"}),
    ("equipamento.aviso.cone.nivel", {"CONE_NIVEL_ACIMA"}),
    ("equipamento.aviso.cone.sobreposicoes", {"SOBREPOSICOES_A_MAIS", "SOBREPOSICOES_ACIMA_DO_TETO"}),
    ("equipamento.aviso.conjuntos", {"CONJUNTOS_DANO_ACIMA_DE_3"}),
    ("equipamento.aviso.inventario", {"SOBRECARGA", "IMOVEL"}),
    ("habilidades.aviso.contagem", {"HABILIDADES_A_MAIS"}),
    ("habilidades.aviso.ress3", {"RESSONANCIA_III_REPETIDA"}),
    ("habilidades.aviso.*", {"HABILIDADE_NIVEL_ACIMA", "HABILIDADES_A_MAIS", "RESSONANCIA_III_REPETIDA"}),
    ("em_jogo.aviso.temporarios_teto", {"BONUS_TEMPORARIO_NO_TETO"}),
]


# Avisos que a planilha mostra por limite de LAYOUT, não por regra do livro: o oráculo não
# os calcula (precisaria da frequência de cada Bênção, que é leitura do texto, N3).
#   em_jogo.aviso.usos — a tabela de Usos da Em Jogo tem 8 linhas (v1.1); um nível alto com muitas
#   Bênçãos de frequência declarada passa disso e o aviso manda ver a aba Caminho.
_OR_INFORMATIVOS = ("em_jogo.aviso.usos",)


def _or_explica(nome_aviso):
    """Códigos do oráculo que explicam um aviso da planilha (primeiro padrão que casa);
    None = aviso que só a planilha tem (não pode acender num cenário válido)."""
    for padrao, codigos in _OR_AVISOS:
        if padrao.endswith("*") and nome_aviso.startswith(padrao[:-1]) or nome_aviso == padrao:
            return codigos
    return None


def _or_cenario(raca, caminho, nivel, semente, fixo=None):
    """Monta entradas VÁLIDAS do oráculo, determinísticas pela semente. A parte de criação
    (método, atributos, Raça, Atributo de Habilidade, Elemento, Sintonia, armadura, arma)
    usa só a semente; a parte que depende do nível usa semente + nível — assim a varredura
    1->20 é o MESMO personagem subindo de nível."""
    import random
    o = _oraculo()
    fixo = dict(fixo or {})
    rb = random.Random(semente)
    rn = random.Random(semente * 1000 + nivel)
    L = nivel
    fx = (L - 1) // 4 + 1
    e = {"nivel": L, "jogadores": rb.choice([1, 2, 3, 4, 4, 5, 6]), "raca": raca, "caminho": caminho}
    # Método e atributos (03 Passo 4)
    if rb.random() < 0.6:
        e["metodo"] = "Array oficial"
        vals = [15, 14, 13, 12, 10, 8]
        rb.shuffle(vals)
        e["atributos"] = dict(zip(_ATR, vals))
    else:
        e["metodo"] = "Compra de Pontos"
        custo = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 10}
        at = {a: 8 for a in _ATR}
        gasto = 0
        for _ in range(200):
            a = rb.choice(_ATR)
            if at[a] < 15 and gasto - custo[at[a]] + custo[at[a] + 1] <= 28:
                gasto += custo[at[a] + 1] - custo[at[a]]
                at[a] += 1
        e["atributos"] = at
    # Bônus racial (05)
    opcoes = o.RACAS[raca]
    if opcoes is None:
        if rb.random() < 0.5:
            e["bonus_racial"] = {"modo": "Um Atributo (+2)", "attr1": rb.choice(_ATR)}
        else:
            a1, a2 = rb.sample(_ATR, 2)
            e["bonus_racial"] = {"modo": "Dois Atributos (+1 cada)", "attr1": a1, "attr2": a2}
    elif len(opcoes) == 1 and rb.random() < 0.5:
        e["bonus_racial"] = {}                       # a Raça de opção única aplica sozinha
    else:
        e["bonus_racial"] = {"attr1": rb.choice(opcoes)}
    attrs_hab = o.CAMINHOS[caminho][0]
    e["atributo_habilidade"] = None if len(attrs_hab) == 1 and rb.random() < 0.5 else rb.choice(attrs_hab)
    e["elemento"] = rb.choice(_OR_ELEMENTOS)
    e["sintonia"] = rb.choice(["Discernimento", "Sincronia"])
    e["armadura"] = rb.choice([None, "Leve", "Média", "Média", "Pesada"])
    cat = rb.choice([None] + _OR_ARMAS * 2)
    if cat:
        e["arma"] = {"categoria": cat, "atributo": rb.choice(["Poder", "Agilidade"]) if cat == "Média" else None,
                     "elemento": rb.choice([None, None] + _OR_ELEMENTOS), "propriedade": rb.choice(_OR_PROPRIEDADES)}
    else:
        e["arma"] = {}
    for k in ("armadura", "arma", "atributo_habilidade", "elemento"):
        if k in fixo:
            e[k] = fixo.pop(k)
    # Aumentos de atributo nos marcos já alcançados, sem passar de 20 (04.3)
    atual = {a: e["atributos"][a] for a in _ATR}
    br = e["bonus_racial"]
    if opcoes is None:
        if br.get("modo") == "Dois Atributos (+1 cada)":
            atual[br["attr1"]] += 1
            atual[br["attr2"]] += 1
        else:
            atual[br["attr1"]] += 2
    else:
        atual[br.get("attr1") or opcoes[0]] += 2
    e["aumentos"] = {}
    for nv in (3, 6, 9, 12, 15, 18):
        if nv > L:
            break
        ra = random.Random(semente * 7 + nv)            # mesmo aumento em toda a varredura
        if ra.random() < 0.5:
            livres = [a for a in _ATR if atual[a] <= 18]
            if livres:
                a = ra.choice(livres)
                atual[a] += 2
                e["aumentos"][nv] = {"modo": "Um Atributo (+2)", "attr1": a}
        else:
            livres = [a for a in _ATR if atual[a] <= 19]
            if len(livres) >= 2:
                a1, a2 = ra.sample(livres, 2)
                atual[a1] += 1
                atual[a2] += 1
                e["aumentos"][nv] = {"modo": "Dois Atributos (+1 cada)", "attr1": a1, "attr2": a2}
    # Bênçãos válidas por slot (06.7): slot k = nível 2k-1; tier pelo requisito
    catalogo = [(n, info) for n, info in o.catalogo_bencaos().items() if info[0] == caminho]
    usadas, bencaos = set(), []
    forcadas = fixo.pop("bencaos_primeiras", [])
    for k in range((L + 1) // 2):
        nivel_slot = 2 * k + 1
        if k < len(forcadas):
            nome = forcadas[k]
        else:
            cand = [n for n, info in catalogo if info[3] <= nivel_slot and n not in usadas and n not in forcadas]
            nome = rn.choice(cand) if cand and rn.random() < 0.9 else None
        bencaos.append(nome)
        if nome:
            usadas.add(nome)
    while bencaos and bencaos[-1] is None:
        bencaos.pop()
    e["bencaos"] = bencaos
    tem = set(b for b in bencaos if b)
    # Ressonâncias liberadas
    e["ressonancias"] = {}
    for rn_, marco in (("I", 5), ("II", 10), ("III", 15), ("IV", 20)):
        if L >= marco and rn.random() < 0.8:
            e["ressonancias"][rn_] = rn.choice(_OR_RESS[rn_])
    # Habilidades até o limite, Nível até o máximo (26.2), alcance dentro do Nível (16.3)
    conhecidas = o.HAB_CONHECIDAS[L - 1]
    nmax = _OR_NIVEL_MAX_HAB[L - 1]
    habs = []
    ress3_livre = "III" in e["ressonancias"]
    for k in range(rn.randint(0, conhecidas)):
        nv = rn.randint(1, nmax)
        h = {"nome": f"Habilidade {k + 1}", "tipo": rn.choice(_OR_TIPOS), "nivel": nv,
             "area": rn.random() < 0.4, "resolucao": rn.choice(_OR_RESOLUCAO + [None])}
        if rn.random() < 0.5:
            h["alcance"] = rn.choice(_OR_ALCANCES[:_OR_ALCANCE_MAX.get(nv, 4) + 1])
        if ress3_livre and rn.random() < 0.5:
            h["ress3"] = True
            ress3_livre = False
        habs.append(h)
    e["habilidades"] = habs
    e["ultimate"] = {"nome": "Ultimate", "tipo": rn.choice(_OR_ULT_TIPOS), "area": rn.random() < 0.4,
                     "resolucao": rn.choice(_OR_RESOLUCAO + [None])} if rn.random() < 0.85 else {}
    # Perícias escolhidas no limite (04.5), fora das do Caminho; Eficácia nos slots (26.4)
    s0 = o.calcular(dict(e, pericias_escolhidas=[]))
    per_cam = set(o.CAMINHOS[caminho][1])
    livres = [p for p in _OR_PERICIAS if p not in per_cam]
    escolhidas = rn.sample(livres, min(len(livres), rn.randint(max(0, s0["pericias_permitidas"] - 1),
                                                                s0["pericias_permitidas"])))
    e["pericias_escolhidas"] = [p for p in _OR_PERICIAS if p in escolhidas]   # ordem das linhas
    com_ef = [p for p in _OR_PERICIAS if p in per_cam or p in escolhidas]
    e["eficacia_pericias"] = [p for p in _OR_PERICIAS
                              if p in rn.sample(com_ef, min(len(com_ef), s0["slots_eficacia_pericias"]))]
    e["eficacia_tr"] = [t for t in _OR_TR if t in rn.sample(_OR_TR, s0["slots_eficacia_tr"])]
    # Cone de Luz da faixa (25.2)
    if rn.random() < 0.8:
        nc = rn.randint(1, fx)
        # 25.2 (v1.1): uma por faixa e só até a parte numérica chegar a +3
        cone = {"nivel": nc, "alvo": rn.choice(_OR_ALVO_CONE + [None]),
                "sobreposicoes": rn.randint(0, min(fx, o.TETO_CONE_NUM - o.CONE[nc][0]))}
        if nc in (1, 3, 5):
            cone["escolha"] = rn.choice(["Numérico", "PV", None])
        if cone["alvo"] == "Um Teste de Resistência":
            cone["qual"] = rn.choice(_OR_TR)
        elif cone["alvo"] == "Uma Perícia":
            cone["qual"] = rn.choice(_OR_PERICIAS)
        e["cone"] = cone
    else:
        e["cone"] = {}
    # Relíquias da faixa (Tier pelo nível) e Conjuntos (25.3)
    rel = {}
    for slot in _OR_SLOTS:
        if rn.random() < 0.7:
            rel[slot] = {"conjunto": rn.choice(["A", "B", "C", "—", "A", "B"])}
    e["reliquias"] = rel
    e["esfera_elemento"] = rn.choice([e["elemento"], rn.choice(_OR_ELEMENTOS)]) if "Esfera Planar" in rel else None
    pecas = {}
    for info in rel.values():
        pecas[info["conjunto"]] = pecas.get(info["conjunto"], 0) + 1
    conj = {}
    for letra in "ABC":
        if pecas.get(letra, 0) >= 1 and rn.random() < 0.9:
            b2 = rn.choice(_OR_BONUS2)
            conj[letra] = {"bonus2": b2}
            if b2 == "Um tipo de rolagem +1":
                conj[letra]["rolagem"] = rn.choice(["Teste de Ataque"] + _OR_TR + _OR_PERICIAS)
    e["conjuntos"] = conj
    # Inventário em texto livre (Espaço manual)
    e["inventario"] = [{"espaco": rn.choice([0.5, 1, 1.5, 2]), "qtd": rn.choice([None, 0, 1, 2, 3])}
                       for _ in range(rn.randint(0, 3))]
    # Estado de jogo coerente com as Bênçãos
    if caminho == "A Recordação":
        total = 12 + L // 2
        pts = {a: 0 for a in _ATR}
        for _ in range(rn.randint(total - 4, total)):
            a = rn.choice([x for x in _ATR if pts[x] < 5] or _ATR)
            if pts[a] < 5:
                pts[a] += 1
        n_evol = sum(1 for n in (8, 14, 20) if L >= n)
        evol = rn.sample(_OR_MEMO_EVOL, rn.randint(0, n_evol))
        memo = {"pontos": {a: v for a, v in pts.items() if v}, "atributo_ataque": rn.choice(_ATR),
                "funcao": rn.choice(_OR_MEMO_FUNCAO), "bonus_menores": rn.sample(_OR_MEMO_BONUS, 3),
                "evolucoes": evol}
        if "Memória Desperta" in evol:
            memo["memoria_desperta"] = rn.choice(["Defesa", "Velocidade"])
        e["memoespirito"] = memo
        e["memo_ativo"] = rn.random() < 0.5
    if "Avatar da Recordação" in tem:
        e["forma_avatar"] = rn.choice(["Manifestada", "Sincronizada"])
    if "Fragmentos do Eu Perdido" in tem:
        e["fragmento"] = rn.choice(["Fúria", "Guarda", "Sabedoria"])
    acum = {}
    if "Sacrifício Desesperado" in tem:
        acum["Fúria"] = rn.randint(0, 2)
    elif "Florescimento da Alma" in tem:
        acum["Florescimento"] = rn.randint(0, 5)
    if "Cicatriz da Destruição" in tem:
        acum["Marcas da Ruína"] = rn.randint(0, 5)
    e["acumulos"] = acum
    e.update(fixo)
    if rn.random() < 0.6:
        e["pv_atual"] = rn.randint(1, o.calcular(e)["pv_max"])
    return e


def _or_pares(s, e):
    """(nome lógico na planilha, valor esperado pelo oráculo) — as saídas comparadas."""
    P = []

    def add(nome, v):
        P.append((nome, v))
    sn = lambda b: "Sim" if b else "Não"  # noqa: E731
    for a in _ATR:
        add(f"criacao.atributo.{_slug(a)}.atual", s["atributos"][a])
        add(f"criacao.atributo.{_slug(a)}.bonus", s["bonus"][a])
    for chave, nome in (("eficiencia", "eficiencia"), ("eficacia", "eficacia"),
                        ("slots_eficacia_pericias", "slots_eficacia_pericias"),
                        ("slots_eficacia_tr", "slots_eficacia_tr"), ("especializacao", "especializacao"),
                        ("teto_rd", "teto_rd"), ("teto_temporarios", "teto_temporarios"),
                        ("teto_bonus", "teto_bonus"), ("bencaos_possuidas", "bencaos"),
                        ("habilidades_conhecidas", "habilidades_conhecidas"),
                        ("nivel_max_habilidade", "nivel_max_habilidade"), ("dados_ab", "dados_ab"),
                        ("tier_reliquia", "tier_reliquia"), ("cone_maximo", "cone_maximo"),
                        ("ultimate_equivalente", "ultimate_equivalente"), ("pontos_memo", "pontos_memo"),
                        ("dt_fraqueza", "dt_fraqueza"), ("ph_max", "ph_max"), ("ph_inicio", "ph_inicio"),
                        ("ph_geracao", "ph_geracao")):
        add(f"nucleo.{nome}", s[chave])
    add("nucleo.reescreve", sn(s["reescreve"]))
    add("criacao.pv", s["pv_max"])
    add("criacao.defesa", s["defesa"])
    add("criacao.esquiva", s["esquiva"] if s["esquiva"] is not None else "Proibida (Armadura Pesada)")
    add("criacao.rd", s["rd"])
    add("criacao.velocidade", s["velocidade"])
    add("criacao.dt", s["dt"])
    add("criacao.ataque_habilidade", s["ataque_habilidade"])
    add("criacao.pericias.permitidas", s["pericias_permitidas"])
    add("criacao.pericias.com_eficiencia", s["pericias_com_eficiencia"])
    add("progressao.pv_ganho_vigor", s["pv_ganho_vigor"])
    add("em_jogo.descanso_curto", s["descanso_curto"])
    if s["quebra"]:
        add("criacao.quebra.texto", s["quebra"]["texto"])
        add("criacao.quebra.media", s["quebra"]["media"])
    for p, info in s["pericias"].items():
        add(f"testes.pericia.{_slug(p)}.total", info["total"])
        add(f"testes.pericia.{_slug(p)}.rolagem", info["rolagem"])
        add(f"testes.pericia.{_slug(p)}.vantagem?", info["vantagem"])
    for t, info in s["testes_resistencia"].items():
        add(f"testes.tr.{_slug(t)}.total", info["total"])
        add(f"testes.tr.{_slug(t)}.rolagem", info["rolagem"])
        add(f"testes.tr.{_slug(t)}.vantagem?", info["vantagem"] or info["vantagem_condicional"])
    add("testes.morrendo.bonus", s["morrendo_bonus"])
    add("testes.morrendo.vantagem?", s["morrendo_vantagem"])
    ab = s["ataque_basico"]
    if ab:
        b = "equipamento.ab.principal"
        add(f"{b}.ataque", ab["ataque"])
        add(f"{b}.rolagem", _oraculo().rolagem(ab["ataque"]))
        for k in ("texto", "media", "rt", "alcance", "elemento"):
            add(f"{b}.{k}", ab[k])
        add(f"{b}.do_atributo", ab["fixo"])
        add(f"{b}.do_equipamento", ab["equip"])
        add(f"{b}.fraqueza", ab["texto_fraqueza"])
        add(f"{b}.critico", ab["critico"])
        add("equipamento.arma1.espaco", ab["espaco"])
    for k, h in enumerate(s["habilidades"], start=1):
        b = f"habilidades.{k}"
        tipo = e["habilidades"][k - 1].get("tipo")
        for x in ("nivel_efetivo", "ph", "rt", "alcance_max", "alvos", "rolagem"):
            add(f"{b}.{x}", h[x])
        if tipo in ("Dano", "Cura"):
            add(f"{b}.total", h["texto"])
            add(f"{b}.media", h["media"])
    u = s["ultimate"]
    add("habilidades.ultimate.equivalente", u["equivalente"])
    add("habilidades.ultimate.custo", u["custo"])
    add("habilidades.ultimate.rt", u["rt"])
    if "texto" in u:
        add("habilidades.ultimate.total", u["texto"])
        add("habilidades.ultimate.media", u["media"])
        add("habilidades.ultimate.dados", u["dados"])
        add("habilidades.ultimate.alvos", u["alvos"])
    for k, sl in enumerate(s["bencoes_slots"], start=1):
        add(f"caminho.bencao.slot{k}.liberado^", sn(sl["liberado"]))   # 'Não (nível 3)' = Não
        if "tier" in sl:
            add(f"caminho.bencao.slot{k}.tier", sl["tier"])
            add(f"caminho.bencao.slot{k}.requisito", sl["requisito"])
    if "pacto_da_ruina" in s:
        p = s["pacto_da_ruina"]
        for k in ("custo_pv", "bonus", "bonus_ferido", "limiar_pv"):
            add(f"caminho.pacto.{k}", p[k])
    add("equipamento.inventario.capacidade", s["capacidade"])
    add("equipamento.inventario.ocupado", s["ocupado"])
    for slot, v in s["reliquias"].items():
        add(f"equipamento.reliquia.{_slug(slot)}.bonus", v)
    for letra in "ABC":
        n_ = s["conjuntos_pecas"].get(letra, 0)
        add(f"equipamento.conjunto.{letra.lower()}.ativo", "4 peças" if n_ >= 4 else "2 peças" if n_ >= 2 else "—")
    add("equipamento.conjuntos.dano", s["conjuntos_bonus"]["dano"])
    if s["barreira_max"] is not None:
        add("em_jogo.barreira_max", s["barreira_max"])
    m = s["memo"]
    if m and e.get("caminho") == "A Recordação":
        for k in ("pontos_total", "pontos_gastos", "pv", "defesa", "velocidade", "ataque", "media",
                  "media_fraqueza", "rt", "rd"):
            add(f"memo.{k}", m[k])
        add("memo.dano", m["texto"])
        for a in _ATR:
            add(f"memo.tr.{_slug(a)}", _oraculo().rolagem(m["tr"][a]))
    return P


def _or_nome(n):
    """Tira o marcador de comparação do fim do nome: '?' = Sim/Não pelo texto não vazio,
    '^' = a primeira palavra do texto da planilha."""
    return n.rstrip("?^")


def _or_igual(obtido, esperado, nome):
    if nome.endswith("?"):                       # Vantagem: texto não vazio na planilha = Sim
        return bool(obtido not in (None, "")) == bool(esperado)
    if nome.endswith("^"):
        return str(obtido or "").split(" ")[0] == str(esperado)
    if isinstance(esperado, (int, float)) and not isinstance(esperado, bool):
        return isinstance(obtido, (int, float)) and abs(obtido - esperado) < 1e-9
    if esperado is None:
        return obtido in (None, "")
    return str(obtido) == str(esperado) if obtido is not None else esperado == ""


_ORC = {}          # estado de cada processo de trabalho da suíte oraculo


def _oraculo_iniciar():
    pl = Planilha()
    C = pl.C
    nome_de = {ref: n for n, ref in C.items()}
    avisos = [(nome_de[ref], ref) for ref in pl.avisos() if ref in nome_de]
    _ORC.update(pl=pl, o=_oraculo(), avisos=avisos)


def _oraculo_trabalhar(caso):
    """Calcula um caso no oráculo e na planilha e devolve as divergências."""
    rotulo, e, ignorar = caso
    pl, o, avisos = _ORC["pl"], _ORC["o"], _ORC["avisos"]
    s = o.calcular(e)
    pares = _or_pares(s, e)
    nomes = sorted({_or_nome(n) for n, _ in pares})
    res = pl.calcular(e, nomes, extras=[ref for _, ref in avisos])
    div = []
    for n, esperado in pares:
        obtido = res[_or_nome(n)]
        if not _or_igual(obtido, esperado, n):
            div.append(f"{_or_nome(n)}: planilha={obtido!r} oráculo={esperado!r}")
    acesos = {n for n, ref in avisos if res[ref] not in (None, "")}
    codigos = set(s["avisos"])
    for n in sorted(acesos):
        if any(n == x or (x.endswith("*") and n.startswith(x[:-1])) for x in ignorar + _OR_INFORMATIVOS):
            continue
        exp = _or_explica(n)
        if exp is None or not (exp & codigos):
            div.append(f"aviso só na planilha: {n} = {res[dict(avisos)[n]]!r} (oráculo: {sorted(codigos)})")
    for cod in sorted(codigos):
        cel = [n for n in acesos if cod in (_or_explica(n) or set())]
        if not cel:
            div.append(f"aviso só no oráculo: {cod} (planilha acesa: {sorted(acesos)})")
    return rotulo, len(pares), len(codigos), div


def _or_casos_limite():
    """Casos-limite da seção 5 do plano (e mais os que a auditoria pediu)."""
    o = _oraculo()
    rec = [b for b, info in o.catalogo_bencaos().items() if info[0] == "A Recordação"]
    C = []

    def caso(rotulo, e, ignorar=()):
        C.append((f"limite: {rotulo}", e, tuple(ignorar)))
    caso("Humano +1/+1 em atributos diferentes",
         _nadir(bonus_racial={"modo": "Dois Atributos (+1 cada)", "attr1": "Poder", "attr2": "Vigor"}))
    caso("Humano +1/+1 no mesmo atributo",
         _nadir(bonus_racial={"modo": "Dois Atributos (+1 cada)", "attr1": "Poder", "attr2": "Poder"}))
    caso("atributo acima de 15 antes da Raça", _nadir(metodo=None, atributos={"Poder": 17, "Vigor": 14}))
    caso("aumentos até 20 e além", _nadir(nivel=20, aumentos={n: {"modo": "Um Atributo (+2)", "attr1": "Poder"}
                                                              for n in (3, 6, 9, 12, 15, 18)}))
    caso("aumento +1/+1 no mesmo atributo",
         _nadir(nivel=6, aumentos={6: {"modo": "Dois Atributos (+1 cada)", "attr1": "Vigor", "attr2": "Vigor"}}))
    caso("aumento antes do nível", _nadir(nivel=5, aumentos={6: {"modo": "Um Atributo (+2)", "attr1": "Vigor"}}))
    caso("atributo 3 e 25", _nadir(metodo=None, atributos={"Poder": 25, "Vigor": 3}))
    caso("nível 0", _nadir(nivel=0))
    caso("nível 21", _nadir(nivel=21))
    caso("jogadores 0", _nadir(jogadores=0))
    caso("jogadores 2", _nadir(jogadores=2))
    caso("jogadores 7", _nadir(jogadores=7))
    caso("array com valor repetido", _nadir(atributos={a: 13 for a in _ATR}))
    caso("Compra de Pontos acima de 28", _nadir(metodo="Compra de Pontos", atributos={a: 13 for a in _ATR}))
    caso("Compra de Pontos exata", _nadir(metodo="Compra de Pontos",
                                          atributos={"Poder": 15, "Vigor": 15, "Agilidade": 12, "Discernimento": 10,
                                                     "Presença": 8, "Sincronia": 8}))
    # v1.2: Poder entrou no par do Vidyadhara (05); o atributo inválido virou Presença
    caso("bônus racial fora das opções", _nadir(raca="Vidyadhara", bonus_racial={"attr1": "Presença"}))
    caso("Atributo de Habilidade fora do Caminho", _nadir(atributo_habilidade="Presença"))
    caso("Perícias escolhidas a mais", _nadir(pericias_escolhidas=["Tecnologia", "Mecânica", "Percepção",
                                                                    "Intimidação"]))
    caso("Perícia do Caminho escolhida", _nadir(pericias_escolhidas=["Atletismo", "Mecânica"]))
    caso("Eficácia sem Eficiência", _nadir(nivel=5, eficacia_pericias=["Furtividade"]))
    caso("Eficácia em Perícias acima dos slots", _nadir(nivel=5, eficacia_pericias=["Atletismo", "Mecânica"]))
    caso("Eficácia em TR acima dos slots", _nadir(nivel=5, eficacia_tr=["Reflexos", "Força de Vontade"]))
    caso("Esquiva com Pesada", _nadir(armadura="Pesada"))
    caso("Habilidades a mais", _nadir(habilidades=[{"nome": "A", "tipo": "Dano", "nivel": 1},
                                                   {"nome": "B", "tipo": "Cura", "nivel": 1}]))
    caso("Nível de Habilidade acima do máximo",
         _nadir(nivel=3, habilidades=[{"nome": "A", "tipo": "Dano", "nivel": 4, "resolucao": "Teste de Ataque"}]))
    caso("Nível de Habilidade 9 (fora de 1-7)",
         _nadir(nivel=20, habilidades=[{"nome": "A", "tipo": "Dano", "nivel": 9, "resolucao": "Teste de Ataque"}]))
    caso("Ressonância III em duas Habilidades",
         _nadir(nivel=15, ressonancias={"III": "Uma Habilidade sobe 1 Nível de efeito"},
                habilidades=[{"nome": "A", "tipo": "Dano", "nivel": 5, "ress3": True},
                             {"nome": "B", "tipo": "Cura", "nivel": 5, "area": True, "ress3": True}]))
    caso("Ressonância III no Nível máximo",
         _nadir(nivel=15, ressonancias={"III": "Uma Habilidade sobe 1 Nível de efeito"},
                habilidades=[{"nome": "A", "tipo": "Dano", "nivel": 6, "ress3": True}]))
    caso("Ressonância antes do nível", _nadir(nivel=4, ressonancias={"I": "Velocidade +1"}))
    caso("Bênção de tier acima do slot", _nadir(nivel=20, bencaos=["Impacto Devastador"]))
    caso("Bênção repetida", _nadir(nivel=3, bencaos=["Pacto da Ruína", "Pacto da Ruína"]))
    caso("Bênção de outro Caminho", _nadir(bencaos=["Olho de Lan"]))
    caso("Bênção em slot futuro", _nadir(bencaos=["Pacto da Ruína", "Sacrifício Desesperado"]))
    caso("Cone acima da faixa", _nadir(cone={"nivel": 3, "alvo": "Defesa"}))
    caso("Sobreposições acima de uma por faixa", _nadir(cone={"nivel": 1, "alvo": "Defesa", "sobreposicoes": 2}))
    caso("Cone 5 com Sobreposições no teto", _nadir(nivel=20, cone={"nivel": 5, "alvo": "PV máximos",
                                                                     "escolha": "PV", "sobreposicoes": 5}))
    # 25.2 (v1.1): além do teto +3 — o PV para junto com o numérico
    caso("Sobreposições além do teto (Cone 1 + 3)", _nadir(nivel=20, cone={"nivel": 1, "alvo": "Defesa",
                                                                           "escolha": "PV", "sobreposicoes": 3}))
    caso("Sobreposições além do teto (Cone 4 + 2)", _nadir(nivel=20, cone={"nivel": 4, "alvo": "Defesa",
                                                                           "sobreposicoes": 2}))
    caso("Cone num TR", _nadir(nivel=9, cone={"nivel": 3, "alvo": "Um Teste de Resistência", "qual": "Reflexos"}))
    caso("Cone numa Perícia", _nadir(nivel=13, cone={"nivel": 4, "alvo": "Uma Perícia", "qual": "Sintonia"}))
    caso("Conjunto +1 em TR, Perícia e Teste de Ataque",
         _nadir(nivel=20, reliquias={s_: {"conjunto": x} for s_, x in zip(_OR_SLOTS, "AABBCC")},
                conjuntos={x: {"bonus2": "Um tipo de rolagem +1", "rolagem": r_}
                           for x, r_ in zip("ABC", ("Reflexos", "Furtividade", "Teste de Ataque"))}))
    caso("Conjuntos 2+2+2 com +2 de dano",
         _nadir(nivel=20, reliquias={s_: {"conjunto": x} for s_, x in zip(_OR_SLOTS, "AABBCC")},
                conjuntos={x: {"bonus2": "Dano +2"} for x in "ABC"}))
    caso("RD no teto (Preservação, Pesada, Pele de Pedra, Cone RD, Conjunto)",
         _nadir(caminho="A Preservação", atributo_habilidade="Vigor", armadura="Pesada", nivel=9,
                bencaos=["Pele de Pedra"], cone={"nivel": 3, "alvo": "RD"},
                reliquias={"Cabeça": {"conjunto": "A"}, "Mãos": {"conjunto": "A"}},
                conjuntos={"A": {"bonus2": "RD +1"}}, pericias_escolhidas=["Mecânica", "Intimidação"]))
    caso("Velocidade acima de 25",
         _nadir(nivel=20, caminho="A Caça", atributo_habilidade="Agilidade", armadura="Leve",
                atributos={"Agilidade": 15, "Poder": 14, "Vigor": 13, "Discernimento": 12, "Presença": 10,
                           "Sincronia": 8}, bonus_racial={"modo": "Um Atributo (+2)", "attr1": "Agilidade"},
                aumentos={3: {"modo": "Um Atributo (+2)", "attr1": "Agilidade"}, 6: {"modo": "Dois Atributos (+1 cada)", "attr1": "Agilidade",
                                                                           "attr2": "Poder"}},
                bencaos=["Olho de Lan", "Presa Escolhida", "Tiro Certeiro", "Caçador Incansável", "Passos de Sombra",
                         "Perseguição", "Dois Alvos, Uma Flecha", "Golpe no Ponto Cego", "Avatar da Caça"],
                ressonancias={"I": "Velocidade +1"}, cone={"nivel": 5, "alvo": "Velocidade"},
                reliquias={"Botas": {"conjunto": "A"}, "Tronco": {"conjunto": "A"}},
                conjuntos={"A": {"bonus2": "Velocidade +1"}}, pericias_escolhidas=["Mecânica", "Intimidação"]))
    caso("inventário com quantidade 0", _nadir(inventario=[{"espaco": 2, "qtd": 0}, {"espaco": 1}]))
    caso("inventário acima da capacidade", _nadir(inventario=[{"espaco": 2, "qtd": 3}]))
    caso("inventário acima do dobro", _nadir(inventario=[{"espaco": 5, "qtd": 5}]))
    caso("Florescimento acima do teto (Defesa e TR)",
         _nadir(caminho="A Abundância", atributo_habilidade="Presença", bencaos=["Florescimento da Alma"],
                acumulos={"Florescimento": 5}, pericias_escolhidas=["Mecânica", "Intimidação"]))
    caso("Instinto de Sobrevivência ligado", _nadir(nivel=5, bencaos=["Pacto da Ruína", "Sacrifício Desesperado",
                                                                      "Instinto de Sobrevivência"], pv_atual=20))
    caso("Cicatriz com 5 Marcas", _nadir(nivel=12, bencaos=["Pacto da Ruína", "Sacrifício Desesperado",
                                                            "Instinto de Sobrevivência", "Impacto Devastador",
                                                            "Cicatriz da Destruição"],
                                         acumulos={"Fúria": 2, "Marcas da Ruína": 5}))
    caso("Corpo Imortal (Abundância)", _nadir(caminho="A Abundância", atributo_habilidade="Presença", nivel=13,
                                              bencaos=[b for b, i in o.catalogo_bencaos().items()
                                                       if i[0] == "A Abundância" and i[1] in (1, 2, 3, 4, 5, 6, 7)],
                                              pericias_escolhidas=["Mecânica", "Intimidação"]))
    memo_ok = {"pontos": {"Sincronia": 5, "Agilidade": 5, "Vigor": 5, "Poder": 5, "Presença": 2},
               "atributo_ataque": "Sincronia", "funcao": "Catalisador",
               "bonus_menores": ["Força Espiritual", "Resistência Espiritual", "Velocidade Espiritual"],
               "evolucoes": ["Forma Completa", "Fusão de Memórias", "Memória Desperta"], "memoria_desperta": "Defesa"}
    recorda = dict(caminho="A Recordação", raca="Xianzhouíta", bonus_racial={"attr1": "Sincronia"},
                   atributo_habilidade="Sincronia", pericias_escolhidas=["Mecânica", "Persuasão"])
    rec_avatar = rec[:9] + ["Avatar da Recordação"]              # slot 10 = nível 19 (Tier III)
    caso("Recordação nível 20 completa com Memoespírito ativo",
         _nadir(nivel=20, bencaos=rec_avatar, memoespirito=memo_ok, memo_ativo=True, forma_avatar="Sincronizada",
                fragmento="Guarda", **recorda))
    caso("Recordação nível 20, Forma Manifestada e Memoespírito inativo",
         _nadir(nivel=20, bencaos=rec[:8] + ["Eternidade Recordada", "Avatar da Recordação"],
                memoespirito=memo_ok, forma_avatar="Manifestada", fragmento="Fúria", **recorda))
    caso("Memoespírito com 6 pontos num Atributo",
         _nadir(nivel=5, memoespirito=dict(memo_ok, pontos={"Vigor": 6}, evolucoes=[]), bencaos=[], **recorda))
    caso("Memoespírito: pontos acima do total",
         _nadir(nivel=1, memoespirito=dict(memo_ok, pontos={a: 3 for a in _ATR}, evolucoes=[]), bencaos=[],
                **recorda))
    caso("Evolução antes do nível", _nadir(nivel=7, memoespirito=dict(memo_ok, evolucoes=["Forma Completa"]),
                                           bencaos=[], **recorda))
    caso("Evolução repetida", _nadir(nivel=14, memoespirito=dict(memo_ok, evolucoes=["Forma Completa",
                                                                                     "Forma Completa"]),
                                     bencaos=[], **recorda))
    caso("Bônus menores repetidos",
         _nadir(nivel=3, memoespirito=dict(memo_ok, evolucoes=[], bonus_menores=["Força Espiritual",
                                                                                 "Força Espiritual"]),
                bencaos=[], **recorda))
    caso("Memoespírito fora da Recordação", _nadir(memoespirito=dict(memo_ok, pontos={"Vigor": 3}, evolucoes=[])))
    nivel20 = _nadir(
        nivel=20, raca="Xianzhouíta", caminho="A Recordação", bonus_racial={"attr1": "Sincronia"},
        atributo_habilidade="Sincronia", eficacia_pericias=["Intimidação", "Investigação", "Ciência"],
        eficacia_tr=["Reflexos", "Força de Vontade", "Resistência Mental"],
        aumentos={n: {"modo": "Dois Atributos (+1 cada)", "attr1": "Sincronia", "attr2": "Agilidade"} for n in (3, 6, 9, 12, 15, 18)},
        pericias_escolhidas=["Mecânica", "Persuasão"],
        bencaos=rec_avatar, ressonancias={"I": "Velocidade +1", "II": "Ultimate com efeito extra",
                                        "III": "Uma Habilidade sobe 1 Nível de efeito",
                                        "IV": "Ultimate com 80 de Energia"},
        memoespirito=dict(memo_ok, funcao="Guardião", memoria_desperta="Velocidade"),
        habilidades=[{"nome": f"H{k}", "tipo": t, "nivel": 7, "area": k % 2 == 0, "ress3": k == 1,
                      "resolucao": "Teste de Ataque" if k % 2 else "Teste de Resistência", "alcance": "Extrema"}
                     for k, t in enumerate(["Dano", "Cura", "Buff", "Debuff", "Passiva", "Dano", "Cura", "Dano"],
                                           start=1)],
        ultimate={"nome": "Fim", "tipo": "Dano", "area": True, "resolucao": "Teste de Resistência"},
        cone={"nivel": 5, "alvo": "Teste de Ataque", "escolha": "Numérico", "sobreposicoes": 0},  # 25.2: o 5 já está no teto
        reliquias={"Cabeça": {"conjunto": "A"}, "Mãos": {"conjunto": "A"}, "Tronco": {"conjunto": "A"},
                   "Botas": {"conjunto": "A"}, "Esfera Planar": {"conjunto": "B"}, "Corda de Ligação": {"conjunto": "B"}},
        esfera_elemento="Fogo", conjuntos={"A": {"bonus2": "Um tipo de rolagem +1", "rolagem": "Teste de Ataque"},
                                           "B": {"bonus2": "Dano +2"}},
        inventario=[{"espaco": 1, "qtd": 3}, {"espaco": 1.5, "qtd": 1}],
        pv_atual=40, memo_ativo=True, forma_avatar="Sincronizada", fragmento="Guarda",
        acumulos={"Fragmentos de Memória": 4})
    caso("nível 20 tudo no máximo (Cone 5 no teto, Tier IV, Conjuntos, 4 Ressonâncias)", nivel20)
    caca = _nadir(nivel=20, raca="Intellitron", caminho="A Caça", bonus_racial={"attr1": "Sincronia"},
                  armadura="Pesada", atributo_habilidade="Agilidade",
                  bencaos=["Olho de Lan", "Presa Escolhida", "Tiro Certeiro", "Caçador Incansável",
                           "Passos de Sombra", "Perseguição", "Dois Alvos, Uma Flecha", "Golpe no Ponto Cego",
                           "Avatar da Caça", "A Última Flecha"],
                  cone={"nivel": 4, "alvo": "Uma Perícia", "qual": "Furtividade"},
                  arma={"categoria": "Disparo longo", "propriedade": "Alcance estendido"},
                  pericias_escolhidas=["Mecânica", "Intimidação"])
    caso("Caça nível 20 com Olho de Lan, Pesada e Alcance estendido", caca)
    return C


def suite_oraculo(args):
    import multiprocessing as mp
    r = Resultado("oraculo")
    if not XLSX.exists():
        r.falha(f"planilha não encontrada: {XLSX}")
        return r
    o = _oraculo()
    casos = []
    # (1) Matriz 7 Raças × 9 Caminhos × níveis {1, 20}: 126 casos, semente fixa por combinação
    for i, raca in enumerate(o.RACAS):
        for j, caminho in enumerate(o.CAMINHOS):
            for nivel in (1, 20):
                semente = 1000 + 10 * i + j
                casos.append((f"matriz: {raca} / {caminho} / nível {nivel}",
                              _or_cenario(raca, caminho, nivel, semente), ()))
    n_matriz = len(casos)
    # (2) Varreduras 1 -> 20 (o mesmo personagem subindo de nível)
    varreduras = [("Humano", "A Destruição", 7001, {}),
                  ("Xianzhouíta", "A Recordação", 7002, {"memo_ativo": True}),
                  ("Intellitron", "A Caça", 7003, {"armadura": "Pesada", "bencaos_primeiras": ["Olho de Lan"]})]
    for raca, caminho, semente, fixo in varreduras:
        for nivel in range(1, 21):
            casos.append((f"varredura: {raca} / {caminho} / nível {nivel}",
                          _or_cenario(raca, caminho, nivel, semente, fixo), ()))
    n_varr = len(casos) - n_matriz
    # (3) Casos-limite
    limites = _or_casos_limite()
    casos += limites
    r.info(f"{n_matriz} casos da matriz, {n_varr} da varredura (3 × 20), {len(limites)} casos-limite")
    t0 = time.time()
    n_proc = max(1, min(8, (os.cpu_count() or 2) - 1, len(casos)))
    total_saidas = total_codigos = n_div = 0
    with mp.get_context("spawn").Pool(n_proc, initializer=_oraculo_iniciar) as pool:
        for rotulo, n_saidas, n_cod, div in pool.imap_unordered(_oraculo_trabalhar, casos, chunksize=2):
            total_saidas += n_saidas
            total_codigos += n_cod
            n_div += len(div)
            r.ok(not div, f"[{rotulo}] {len(div)} divergência(s): " + " | ".join(div[:12]))
    r.info(f"{len(casos)} casos, {total_saidas} saídas comparadas, {total_codigos} códigos de aviso do oráculo "
           f"conferidos na planilha; {n_div} divergência(s); {n_proc} processo(s), {time.time() - t0:.0f} s")
    return r


# ---------------------------------------------------------------------------
# Suíte texto — nomenclatura, glossário, ortografia e acentuação
# ---------------------------------------------------------------------------

LEXICO_EXTRA = BUILD / "ficha_lexico_extra.txt"
NOMENCLATURA_PS1 = RAIZ / "scripts" / "checar-nomenclatura.ps1"

# Termos aposentados da tabela 30.2 (coluna da esquerda, sem aspas e sem o comentário entre
# parênteses). A suíte confere que cada um está escrito em 30.2, para a lista não inventar nada.
_APOSENTADOS_30_2 = ["HP", "DoT", "ação bônus", "ação comum", "rodada", "turno do grupo", "derrubar o turno",
                     "adiantar", "iniciativa", "barra de resistência", "+1 de distância", "Aumento na velocidade",
                     "Teste de Atenção", "Cura toda a Vida", "ação adicional limitada", "dados de vida",
                     "a defesa inimiga conta como -10", "provavelmente vou mudar o nome"]

# Formas sem acento proibidas (palavra inteira, sem distinção de caixa)
_SEM_ACENTO = ["Criacao", "Progressao", "Inicio", "Pericia", "Pericias", "Bencao", "Bencaos", "Bencoes",
               "Eficiencia", "Eficacia", "Nivel", "Niveis", "Forca", "Acao", "Acoes", "Raca", "Racas",
               "Rapidas", "Regras Rapidas", "Memoespirito", "Resistencia", "Distancia", "Tecnica", "Pocao",
               "Pocoes", "Reliquia", "Reliquias", "Presenca", "Ciencia", "Mecanica", "Percepcao",
               "Sobrevivencia", "Intuicao", "Investigacao", "Persuasao", "Intimidacao", "Enganacao", "Lideranca",
               "Potencia", "Fisica", "Fisico", "Lentidao", "Corrupcao", "Condicao", "Condicoes", "Opcao",
               "Sobreposicao", "Ressonancia", "Ressonancias", "Especializacao", "Quantico", "Imaginario",
               "Credito", "Creditos", "Espaco", "Media", "Basico", "Ultima", "Codigo", "Xianzhouita",
               "Destruicao", "Inexistencia", "Abundancia", "Recordacao", "Erudicao", "Caca", "Preservacao",
               "Avancar", "Avanco", "Critico", "Reacao", "Vulneravel", "Proposito", "Bonus", "Nao", "Voce",
               "Tambem", "Ate", "Atraves", "Unico", "Proximo", "Calculo", "Acumulos", "Inventario", "Saida"]

_RE_PALAVRA = re.compile(r"[^\W\d_]+")


def _sem_acento_mesmo_tamanho(s):
    """Tira acentos letra a letra, sem mudar o tamanho (para mapear posições)."""
    return "".join(unicodedata.normalize("NFD", ch)[0] for ch in s).lower()


def _proibidas_ps1():
    texto = NOMENCLATURA_PS1.read_text(encoding="utf-8")
    bloco = re.search(r"\$TermosProibidos\s*=\s*@\((.*?)\)", texto, re.S).group(1)
    return re.findall(r"'([^']*)'", bloco)


def _glossario_30_1():
    sec = _md("30").split("## 30.1")[1].split("## 30.2")[0]
    termos = []
    for m in re.finditer(r"(?m)^\| \*\*(.+?)\*\*", sec):
        termos += [t.strip() for t in m.group(1).split("/")]
    return termos


def _lexico():
    palavras = set()
    for p in sorted(LIVRO.glob("*.md")):
        palavras.update(w.lower() for w in _RE_PALAVRA.findall(p.read_text(encoding="utf-8")))
    extra = set()
    if LEXICO_EXTRA.exists():
        for linha in LEXICO_EXTRA.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if linha and not linha.startswith("#"):
                extra.add(linha.lower())
    return palavras, extra


def _textos_visiveis(caminho=None):
    """Texto que o jogador vê: valores literais, literais de string dentro das fórmulas
    (Tokenizer, nunca nomes de função), títulos e mensagens das validações, listas literais
    das validações e nomes de aba. Devolve [(onde, texto)]."""
    import openpyxl
    from openpyxl.formula import Tokenizer
    wb = openpyxl.load_workbook(caminho or XLSX)
    itens = []
    for ws in wb.worksheets:
        itens.append((f"nome da aba '{ws.title}'", ws.title))
        for linha in ws.iter_rows():
            for c in linha:
                v = c.value
                if not isinstance(v, str) or not v.strip():
                    continue
                onde = f"'{ws.title}'!{c.coordinate}"
                if v.startswith("="):
                    for tok in Tokenizer(v).items:
                        if tok.type == "OPERAND" and tok.subtype == "TEXT":
                            s = tok.value[1:-1].replace('""', '"')
                            if s.strip():
                                itens.append((onde + " (fórmula)", s))
                else:
                    itens.append((onde, v))
        for dv in ws.data_validations.dataValidation:
            onde = f"'{ws.title}'!{str(dv.sqref).split()[0]} (validação)"
            for campo in (dv.promptTitle, dv.prompt, dv.errorTitle, dv.error):
                if campo:
                    itens.append((onde, campo))
            if dv.type == "list" and dv.formula1 and dv.formula1.startswith('"'):
                itens.append((onde + " (lista)", dv.formula1.strip('"')))
    return itens


def suite_texto(args):
    r = Resultado("texto")
    if not XLSX.exists():
        r.falha(f"planilha não encontrada: {XLSX}")
        return r
    itens = _textos_visiveis()
    r.info(f"{len(itens)} trechos de texto visível extraídos (valores, literais de fórmula, validações, abas)")
    # (1) 25 strings proibidas (mesma regra do checar-nomenclatura.ps1) + termos aposentados de 30.2
    proibidas = _proibidas_ps1()
    r.ok(len(proibidas) == 25, f"checar-nomenclatura.ps1 deveria ter 25 strings proibidas, tem {len(proibidas)}")
    sec_30_2 = _md("30").split("## 30.2")[1].lower()
    for t in _APOSENTADOS_30_2:
        r.ok(t.lower() in sec_30_2, f"termo aposentado '{t}' não está escrito em 30.2 (lista do teste errada)")
    padroes = [(t, re.compile(r"\b" + re.escape(t) + r"\b", re.I), "string proibida (checar-nomenclatura.ps1)")
               for t in proibidas]
    padroes += [(t, re.compile(r"(?<!\w)" + re.escape(t) + r"(?!\w)", re.I), "termo aposentado (30.2)")
                for t in _APOSENTADOS_30_2]
    n1 = 0
    for onde, s in itens:
        for termo, rx, tipo in padroes:
            n1 += 1
            if rx.search(s):
                r.falha(f"(1) {tipo} '{termo}' em {onde}: {s[:120]!r}")
    # (2) grafia exata dos termos oficiais do glossário 30.1
    termos = _glossario_30_1()
    r.ok(len(termos) >= 90, f"glossário 30.1 com poucos termos lidos: {len(termos)}")
    # Citação literal do livro (o livro é a fonte de verdade e não se edita): um trecho que
    # aparece igual num capítulo (sem a marcação **, *, `) não é achado de grafia — é o livro.
    corpo_livro = "\n".join(re.sub(r"\*\*|\*|`", "", p.read_text(encoding="utf-8"))
                            for p in sorted(LIVRO.glob("*.md")))
    citacoes = set()
    n2 = 0
    for termo in termos:
        chave = _sem_acento_mesmo_tamanho(termo)
        rx = re.compile(r"(?<!\w)" + re.escape(chave) + r"(?!\w)")
        palavras_t = termo.split()
        for onde, s in itens:
            for m in rx.finditer(_sem_acento_mesmo_tamanho(s)):
                n2 += 1
                orig = s[m.start():m.end()]
                acento_errado = orig.lower() != termo.lower()
                caixa_errada = len(palavras_t) > 1 and orig.split()[1:] != palavras_t[1:]
                if (acento_errado or caixa_errada) and s.strip() in corpo_livro:
                    citacoes.add(f"'{orig}' em {onde}")
                elif acento_errado or caixa_errada:
                    r.falha(f"(2) termo do glossário '{termo}' escrito '{orig}' em {onde}: {s[:120]!r}")
    if citacoes:
        r.info(f"(2) {len(citacoes)} grafia(s) fora do glossário que são citação literal do livro (aceitas): "
               + "; ".join(sorted(citacoes)))
    # (3) ortografia: toda palavra no léxico (livro + ficha_lexico_extra.txt)
    livro, extra = _lexico()
    r.ok(LEXICO_EXTRA.exists(), f"léxico extra não encontrado: {LEXICO_EXTRA}")
    sobra_extra = sorted(w for w in extra if w in livro)
    r.ok(not sobra_extra, f"ficha_lexico_extra.txt repete palavras que o livro já tem: {sobra_extra[:20]}")
    lexico = livro | extra
    fora = {}
    n3 = 0
    usadas_extra = set()
    for onde, s in itens:
        for w in _RE_PALAVRA.findall(s):
            n3 += 1
            if w.lower() in extra:
                usadas_extra.add(w.lower())
            if w.lower() not in lexico:
                fora.setdefault(w, onde)
    for w, onde in sorted(fora.items()):
        r.falha(f"(3) palavra fora do léxico: '{w}' (primeira vez em {onde})")
    nao_usadas = sorted(extra - usadas_extra)
    r.ok(not nao_usadas, f"ficha_lexico_extra.txt tem palavras que a planilha não usa: {nao_usadas[:20]}")
    # (4) acentuação: formas sem acento proibidas
    n4 = 0
    for forma in _SEM_ACENTO:
        rx = re.compile(r"(?<!\w)" + re.escape(forma) + r"(?!\w)", re.I)
        for onde, s in itens:
            n4 += 1
            if rx.search(s):
                r.falha(f"(4) forma sem acento '{forma}' em {onde}: {s[:120]!r}")
    r.checagens += n1 + n2 + n3 + n4
    r.info(f"(1) {len(proibidas)} strings proibidas + {len(_APOSENTADOS_30_2)} aposentadas × trechos = {n1} buscas; "
           f"(2) {len(termos)} termos do glossário, {n2} ocorrências conferidas; (3) {n3} palavras, léxico de "
           f"{len(livro)} palavras do livro + {len(extra)} extras; (4) {len(_SEM_ACENTO)} formas sem acento, "
           f"{n4} buscas")
    return r


# ---------------------------------------------------------------------------
# Suíte preview — PNG de cada aba em 3 estados e texto cortado
# ---------------------------------------------------------------------------

PREVIEW = RAIZ / ".agents" / "tasks" / "ficha-preview"


def entradas_nadir_exemplo(mapa):
    """Entradas da Nadir de 29.7 ({"'Aba'!A1": valor}), com nome, conceito e acabamento do
    Passo 12. Usada pela prévia e por build/gerar_ficha.py para gravar 'Ficha Exemplo - Nadir.xlsx'."""
    C = mapa["celulas"]
    nadir = _entradas_planilha(_nadir(), mapa)
    nadir.update({C["criacao.nome"]: "Nadir", C["criacao.jogador"]: "Jogadora da mesa",
                  C["criacao.conceito"]: "Mecânica de doca orbital expulsa da Aliança por consertar a nave errada",
                  C["criacao.proposito"]: "Provar que o acidente não foi culpa dela",
                  C["criacao.crenca_esforco"]: "Eu não assino nada que eu não consertei",
                  C["criacao.arma.nome"]: "Marreta de doca", C["criacao.coisa_inutil"]:
                  "O crachá cortado ao meio da doca que a expulsou"})
    return nadir


def _estados_preview(mapa, pl=None, wb=None):
    """Os 4 estados da prévia: ficha em branco, Nadir nível 1 (29.7), nível 20 completo e o
    pior caso (renderizar_ficha.estado_pior_caso: listas na opção mais longa, números no
    máximo e textos longos do livro). Sem `pl` e `wb`, só os 3 primeiros."""
    estados = _estados_basicos(mapa)
    if pl is not None and wb is not None:
        sys.path.insert(0, str(BUILD))
        import renderizar_ficha
        refs, _ = _formulas_da_planilha()
        estados["pior-caso"] = renderizar_ficha.estado_pior_caso(
            wb, mapa, lambda e: pl.modelo.calcular(entradas=e, saidas=refs))
    return estados


def _estados_basicos(mapa):
    """Os 3 estados fixos da prévia: ficha em branco, Nadir nível 1 (29.7) e nível 20 completo."""
    C = mapa["celulas"]
    o = _oraculo()
    nadir = entradas_nadir_exemplo(mapa)
    rec = [b for b, info in o.catalogo_bencaos().items() if info[0] == "A Recordação"]
    completo = _nadir(
        nivel=20, raca="Xianzhouíta", caminho="A Recordação", bonus_racial={"attr1": "Sincronia"},
        atributo_habilidade="Sincronia", pericias_escolhidas=["Mecânica", "Persuasão"],
        eficacia_pericias=["Intimidação", "Investigação", "Ciência", "Mecânica", "Persuasão"],
        eficacia_tr=["Reflexos", "Força de Vontade", "Resistência Mental"],
        aumentos={n: {"modo": "Dois Atributos (+1 cada)", "attr1": "Sincronia", "attr2": "Agilidade"} for n in (3, 6, 9, 12, 15, 18)},
        bencaos=rec[:9] + ["Avatar da Recordação"],
        ressonancias={"I": "Velocidade +1", "II": "Ultimate com efeito extra",
                      "III": "Uma Habilidade sobe 1 Nível de efeito", "IV": "Ultimate com 80 de Energia"},
        memoespirito={"pontos": {"Sincronia": 5, "Agilidade": 5, "Vigor": 5, "Poder": 5, "Presença": 2},
                      "atributo_ataque": "Sincronia", "funcao": "Guardião",
                      "bonus_menores": ["Força Espiritual", "Resistência Espiritual", "Velocidade Espiritual"],
                      "evolucoes": ["Forma Completa", "Fusão de Memórias", "Memória Desperta"],
                      "memoria_desperta": "Velocidade"},
        habilidades=[{"nome": n, "tipo": t, "nivel": 7, "area": k % 2 == 0, "ress3": k == 1,
                      "resolucao": "Teste de Ataque" if k % 2 else "Teste de Resistência", "alcance": "Extrema"}
                     for k, (n, t) in enumerate([("Lança da Memória", "Dano"), ("Abraço do Passado", "Cura"),
                                                 ("Eco Firme", "Buff"), ("Névoa do Esquecimento", "Debuff"),
                                                 ("Guarda Lembrada", "Passiva"), ("Chuva de Fragmentos", "Dano"),
                                                 ("Luz que Fica", "Cura"), ("Último Retrato", "Dano")], start=1)],
        ultimate={"nome": "O Fim Lembrado", "tipo": "Dano", "area": True, "resolucao": "Teste de Resistência"},
        cone={"nivel": 5, "alvo": "Teste de Ataque", "escolha": "Numérico", "sobreposicoes": 0},  # 25.2: o 5 já está no teto
        reliquias={"Cabeça": {"conjunto": "A"}, "Mãos": {"conjunto": "A"}, "Tronco": {"conjunto": "A"},
                   "Botas": {"conjunto": "A"}, "Esfera Planar": {"conjunto": "B"}, "Corda de Ligação": {"conjunto": "B"}},
        esfera_elemento="Fogo", conjuntos={"A": {"bonus2": "Um tipo de rolagem +1", "rolagem": "Teste de Ataque"},
                                           "B": {"bonus2": "Dano +2"}},
        inventario=[{"item": "Poção de Vida Média", "qtd": 3}, {"item": "Bastão retrátil", "espaco": 1.5, "qtd": 1}],
        pv_atual=40, memo_ativo=True, forma_avatar="Sincronizada", fragmento="Guarda",
        acumulos={"Fragmentos de Memória": 4})
    nv20 = _entradas_planilha(completo, mapa)
    nv20.update({C["criacao.nome"]: "Lin Qiu", C["criacao.jogador"]: "Jogador da mesa",
                 C["criacao.conceito"]: "Arquivista que guarda as memórias de um mundo que acabou",
                 C["criacao.proposito"]: "Devolver a cada sobrevivente a lembrança que ele perdeu",
                 C["criacao.arma.nome"]: "Pena de jade", C["memo.nome"]: "Sombra de Jade",
                 C["criacao.tecnica.nome"]: "Leitura de arquivo", C["equipamento.cone.nome"]: "O Que Restou",
                 C["equipamento.conjunto.a.nome"]: "Arquivo Eterno", C["equipamento.conjunto.b.nome"]: "Nó de Ferro",
                 C["em_jogo.energia"]: 100, C["em_jogo.ph"]: 5,
                 C["em_jogo.condicao.1.nome"]: "Marcado", C["em_jogo.condicao.1.turnos"]: 2,
                 C["em_jogo.condicao.2.nome"]: "Queimadura", C["em_jogo.condicao.2.eficiencia"]: 6,
                 C["em_jogo.dano.bruto"]: 30})
    return {"em-branco": {}, "nadir-nivel-1": nadir, "nivel-20-completo": nv20}


def suite_preview(args):
    import openpyxl
    sys.path.insert(0, str(BUILD))
    import renderizar_ficha
    r = Resultado("preview")
    if not XLSX.exists():
        r.falha(f"planilha não encontrada: {XLSX}")
        return r
    pl = Planilha()
    refs, _ = _formulas_da_planilha()
    avisos = set(pl.avisos())
    wb = openpyxl.load_workbook(XLSX)
    PREVIEW.mkdir(parents=True, exist_ok=True)
    for antigo in list(PREVIEW.glob("*.png")) + list(PREVIEW.glob("indice-recortes.txt")):
        antigo.unlink()
    total_cortes = 0
    pngs, recortes, saidas = [], [], {}
    lado = renderizar_ficha.LADO_RECORTE
    for estado, entradas in _estados_preview(pl.mapa, pl, wb).items():
        valores = pl.modelo.calcular(entradas=entradas, saidas=refs)
        erros = [k for k, v in valores.items() if eh_erro(v)]
        valores.update(entradas)          # o que o jogador digitou aparece na própria célula de entrada
        r.ok(not erros, f"[{estado}] {len(erros)} valor(es) de erro: {erros[:8]}")
        saida = renderizar_ficha.renderizar_estado(wb, valores, avisos, PREVIEW, estado)
        saidas[estado] = saida
        for aba, (png, w, h, cortes, partes) in saida.items():
            pngs.append(png)
            r.ok(png.exists(), f"[{estado}] PNG não gerado: {png}")
            # Recortes 1:1: todos existem, nenhum passa de LADO_RECORTE e juntos cobrem a aba sem reduzir
            r.ok(bool(partes) and all(p.exists() for p, *_ in partes), f"[{estado}] {aba}: recortes não gerados")
            grandes = [(p.name, pw, ph) for p, pw, ph, _ in partes if pw > lado or ph > lado]
            r.ok(not grandes, f"[{estado}] {aba}: recorte maior que {lado} px: {grandes[:3]}")
            area = sum((pw - renderizar_ficha.CAB_LIN) * (ph - renderizar_ficha.CAB_COL) for _, pw, ph, _ in partes)
            r.ok(area == w * h, f"[{estado}] {aba}: recortes cobrem {area} px², a aba tem {w * h} px² (escala ≠ 1:1?)")
            recortes.extend(partes)
            total_cortes += len(cortes)
            for ref, s, motivo in cortes[:40]:
                r.falha(f"[{estado}] texto cortado em {ref}: {motivo} — {s[:90]!r}")
            if len(cortes) > 40:
                r.falha(f"[{estado}] {aba}: mais {len(cortes) - 40} texto(s) cortado(s)")
            r.checagens += 1
    # Em Jogo, pior caso dos textos curtos (não dependem do estado): todo efeito de condição,
    # toda Vantagem racial e todo "Bênção · frequência" dos Usos cabem numa linha
    import gerar_ficha as G
    ej = wb["Em Jogo"]
    util = lambda c0, c1: sum(renderizar_ficha.px_coluna(ej, c) for c in range(c0, c1 + 1)) - 2 * renderizar_ficha.MARGEM  # noqa: E731,E501
    f9 = renderizar_ficha.fonte(round(G.EJ_FONTE_CORPO * 4 / 3))
    for cond, t in G.EJ_EFEITO_CURTO:
        r.ok(f9.getlength(t) <= util(5, 6), f"Em Jogo: efeito curto de {cond} não cabe em E:F: {t!r}")
    for raca, t in G.EJ_VANTAGENS_CURTAS.items():
        r.ok(f9.getlength(t) <= util(2, 4), f"Em Jogo: Vantagem curta de {raca} não cabe em B:D: {t!r}")
    curta = dict(G.EJ_FREQ_CURTA)
    bl = pl.mapa["blocos"]["dados.bencaos"]
    dados = wb["Dados"]
    n_usos = 0
    for k in range(bl["primeira_linha"], bl["ultima_linha"] + 1):
        nome = dados[f"{bl['colunas']['Bênção']}{k}"].value
        fr = dados[f"{bl['colunas']['Frequência']}{k}"].value
        if fr == "Sem limite declarado":
            continue
        t = f"{nome} · {curta.get(fr, fr)}"
        n_usos += 1
        r.ok(f9.getlength(t) <= util(7, 9), f"Em Jogo: uso '{t}' não cabe em G:I")
    r.info(f"Em Jogo, pior caso: {len(G.EJ_EFEITO_CURTO)} efeitos de condição, {len(G.EJ_VANTAGENS_CURTAS)} "
           f"Vantagens raciais e {n_usos} Bênçãos com frequência medidos (cabem numa linha)")
    # Em Jogo cabe numa tela de 1360 × 768 (A:L × linhas 1-40)
    larg = sum(renderizar_ficha.px_coluna(ej, c) for c in range(1, 13))
    alt = sum(renderizar_ficha.px_linha(ej, k) for k in range(1, 41))
    r.ok(larg <= 1360 and alt <= 768, f"Em Jogo: A:L × 1-40 = {larg} × {alt} px (máximo 1360 × 768)")
    r.ok(len(pngs) == 40, f"esperava 40 PNGs (10 abas × 4 estados), vieram {len(pngs)}")
    indice = renderizar_ficha.gravar_indice(PREVIEW, saidas)
    r.info(f"{len(pngs)} PNGs inteiros + {len(recortes)} recortes 1:1 (≤ {lado} × {lado} px) em {PREVIEW}; "
           f"índice em {indice.name}; {total_cortes} texto(s) cortado(s); Em Jogo A:L × 1-40 = {larg} × {alt} px")
    return r


# ---------------------------------------------------------------------------
# Suíte visual — tamanhos das células (pedido do usuário, v1.1): tudo cabe na própria
# célula, listas com espaço para a seta, rótulos visíveis, fonte >= 9 pt, contraste
# >= 4,5:1, tabelas a no máximo 15 linhas do cabeçalho e área do jogador em 1360 px
# ---------------------------------------------------------------------------

LARGURA_TELA = 1360
DISTANCIA_MAX_CABECALHO = 15


def suite_visual(args):
    import openpyxl
    from openpyxl.utils import get_column_letter
    from openpyxl.utils.cell import range_boundaries
    sys.path.insert(0, str(BUILD))
    import renderizar_ficha as R
    r = Resultado("visual")
    if not XLSX.exists():
        r.falha(f"planilha não encontrada: {XLSX}")
        return r
    wb = openpyxl.load_workbook(XLSX)
    pl = Planilha()
    refs, _ = _formulas_da_planilha()
    C = pl.mapa["celulas"]
    avisos = set(pl.avisos())
    mescla = {ws.title: R._mesclas(ws) for ws in wb.worksheets}

    def oculta(ws, rr, cc):
        return bool(ws.column_dimensions[get_column_letter(cc)].hidden or ws.row_dimensions[rr].hidden)

    def separar(ref):
        aba, cel = separar_ref(ref)
        ws = wb[aba]
        return ws, ws[cel].row, ws[cel].column

    # (1) Cada célula com conteúdo cabe nela mesma, nos 4 estados ------------------------------
    estados = _estados_preview(pl.mapa, pl, wb)
    nao_cabe = {}                       # ref -> (estado, texto, motivo): a 1ª vez que não coube
    larg_conteudo = {}                  # (aba, coluna) -> maior conteúdo em px (aviso de desperdício)
    valores_por_estado = {}
    n_medidas = 0
    por_estado = {}                     # estado -> textos medidos (relatório da auditoria visual final)
    for estado, ent in estados.items():
        valores = pl.modelo.calcular(entradas=ent, saidas=refs)
        erros = [k for k, v in valores.items() if eh_erro(v)]
        r.ok(not erros, f"[{estado}] {len(erros)} valor(es) de erro: {erros[:8]}")
        valores.update(ent)
        valores_por_estado[estado] = valores
        for ws in wb.worksheets:
            topo, coberta = mescla[ws.title]
            for linha in ws.iter_rows():
                for cel in linha:
                    rr, cc = cel.row, cel.column
                    if (rr, cc) in coberta or oculta(ws, rr, cc):
                        continue
                    ref = f"'{ws.title}'!{cel.coordinate}"
                    v = cel.value
                    if (isinstance(v, str) and v.startswith("=")) or v is None:
                        v = valores.get(ref)
                    s = R.texto_exibido(v)
                    if not s:
                        continue
                    n_medidas += 1
                    por_estado[estado] = por_estado.get(estado, 0) + 1
                    motivo = R.medir(ws, rr, cc, s, topo)
                    if motivo and ref not in nao_cabe:
                        nao_cabe[ref] = (estado, s, motivo)
                    al = cel.alignment
                    if (rr, cc) not in topo and not (al is not None and al.wrap_text):
                        px = R.fonte_da_celula(cel).getlength(s.split("\n")[0]) * R.FOLGA + R.RESERVA
                        k = (ws.title, cc)
                        larg_conteudo[k] = max(larg_conteudo.get(k, 0), px)
    for ref, (estado, s, motivo) in sorted(nao_cabe.items()):
        r.falha(f"[{estado}] não cabe em {ref}: {motivo} — {s[:70]!r}")
    r.checagens += n_medidas - len(nao_cabe)
    r.info(f"(1) {n_medidas} textos medidos em 4 estados ("
           f"{', '.join(f'{e} {por_estado.get(e, 0)}' for e in estados)}); {len(nao_cabe)} não couberam")

    # (2) Listas suspensas: largura >= opção mais longa + 24 px (seta do Google) -----------------
    n_listas = 0
    for ws in wb.worksheets:
        topo, _ = mescla[ws.title]
        for dv in ws.data_validations.dataValidation:
            if dv.type != "list" or not dv.formula1:
                continue
            fx = dv.formula1
            opcoes = set()
            if fx.startswith('"'):
                opcoes = {x for x in fx.strip('"').split(",") if x}
            else:
                aba = ws.title
                faixa = fx
                if "!" in fx:
                    aba, faixa = fx.rsplit("!", 1)
                    aba = aba.strip("'")
                c0, r0, c1, r1 = range_boundaries(faixa.replace("$", ""))
                alvo = wb[aba]
                for rr in range(r0, r1 + 1):
                    for cc in range(c0, c1 + 1):
                        k = f"'{aba}'!{alvo.cell(rr, cc).coordinate}"
                        bruto = alvo.cell(rr, cc).value
                        if isinstance(bruto, str) and bruto.startswith("="):
                            for vals in valores_por_estado.values():
                                s = R.texto_exibido(vals.get(k))
                                if s:
                                    opcoes.add(s)
                        elif bruto not in (None, ""):
                            opcoes.add(R.texto_exibido(bruto))
            for faixa in str(dv.sqref).split():
                c0, r0, c1, r1 = range_boundaries(faixa)
                for rr in range(r0, r1 + 1):
                    for cc in range(c0, c1 + 1):
                        cel = ws.cell(rr, cc)
                        f = R.fonte_da_celula(cel)
                        w, _ = R.area_px(ws, rr, cc, topo)
                        maior = max(opcoes, key=f.getlength, default="")
                        precisa = f.getlength(maior) * R.FOLGA + R.SETA_LISTA
                        n_listas += 1
                        r.ok(w >= precisa, f"lista em '{ws.title}'!{cel.coordinate}: {w} px < {int(precisa)} px "
                                           f"(opção mais longa {maior[:50]!r} + seta)")
    r.info(f"(2) {n_listas} células com lista suspensa conferidas (opção mais longa + {R.SETA_LISTA} px)")

    # (3) e (4) Texto buscado na aba Dados e mensagem mais longa de cada aviso --------------------
    pior_caso = {k: R.texto_exibido(v) for k, v in estados.get("pior-caso", {}).items()}
    estima = R.PiorTexto(wb, entradas_texto=pior_caso)
    n_busca = n_av = 0
    for ws in wb.worksheets:
        if ws.title == "Dados":
            continue
        topo, coberta = mescla[ws.title]
        for linha in ws.iter_rows():
            for cel in linha:
                f = cel.value
                if not (isinstance(f, str) and f.startswith("=")) or oculta(ws, cel.row, cel.column):
                    continue
                ref = f"'{ws.title}'!{cel.coordinate}"
                eh_aviso = ref in avisos
                if not eh_aviso and not R.busca_dados(f):
                    continue
                s = estima.formula(f, ws.title)
                if not s:
                    continue
                if eh_aviso:
                    n_av += 1
                else:
                    n_busca += 1
                motivo = R.medir(ws, cel.row, cel.column, s, topo)
                r.ok(motivo is None, f"{'aviso' if eh_aviso else 'texto buscado na Dados'} mais longo não cabe "
                                     f"em {ref}: {motivo} — {s[:70]!r}")
    r.info(f"(3) {n_busca} células com texto buscado na aba Dados e (4) {n_av} avisos medidos com o texto mais "
           f"longo que a fórmula pode mostrar")

    # (5) Entradas: rótulo visível à esquerda ou no cabeçalho acima, sem linha/coluna oculta ----------
    tabs = {ws.title: R.tabelas(ws) for ws in wb.worksheets}
    sem_rotulo = []
    for nome in pl.mapa["entradas"]:
        ws, rr, cc = separar(C[nome])
        topo, coberta = mescla[ws.title]
        r.ok(not oculta(ws, rr, cc), f"entrada {nome} ({C[nome]}) em linha ou coluna oculta")
        ok_rot = False
        k = cc - 1
        while k >= 1 and (rr, k) in coberta:
            k -= 1
        if k >= 1:
            esq = ws.cell(rr, k)
            v = esq.value
            if isinstance(v, str) and v.startswith("="):
                v = valores_por_estado["em-branco"].get(f"'{ws.title}'!{esq.coordinate}")
            ok_rot = isinstance(v, str) and bool(v.strip()) and not R.eh_entrada(esq)
        if not ok_rot:
            for t in tabs[ws.title]:
                if rr in t["linhas"] and t["c0"] <= cc <= t["c1"]:
                    kk = cc
                    while kk >= 1 and (t["cab"], kk) in coberta:
                        kk -= 1
                    ok_rot = bool(str(ws.cell(t["cab"], kk).value or "").strip())
        if not ok_rot:
            sem_rotulo.append(f"{nome} ({C[nome]})")
    r.ok(not sem_rotulo, f"{len(sem_rotulo)} entrada(s) sem rótulo visível à esquerda ou no cabeçalho: "
                         f"{sem_rotulo[:12]}")

    # (6) Fonte mínima 9 pt e (7) contraste >= 4,5:1 -------------------------------------------------
    pequenas, combos = [], {}
    branco = (255, 255, 255)
    for ws in wb.worksheets:
        for linha in ws.iter_rows():
            for cel in linha:
                if cel.value is None and not R.eh_entrada(cel):
                    continue
                ft = cel.font
                if (ft.sz or 10) < 9:
                    pequenas.append(f"'{ws.title}'!{cel.coordinate} ({ft.sz} pt)")
                fundo = R._rgb(cel.fill.fgColor) if R.cor_fundo(cel) else branco
                cor = R._rgb(ft.color, (0, 0, 0)) if ft.color is not None else (0, 0, 0)
                combos.setdefault((cor, fundo), f"'{ws.title}'!{cel.coordinate}")
    combos.setdefault(((0x9C, 0, 6), (0xFF, 0xC7, 0xCE)), "avisos (formatação condicional)")
    combos.setdefault(((0, 0, 0), (0xFF, 0xE6, 0x99)), "nível atual na Progressão (formatação condicional)")
    r.ok(not pequenas, f"{len(pequenas)} célula(s) com fonte menor que 9 pt: {pequenas[:10]}")
    for (cor, fundo), onde in sorted(combos.items()):
        cr = R.contraste(cor, fundo)
        r.ok(cr >= 4.5, f"contraste {cr:.2f}:1 < 4,5:1 (texto #{'%02X%02X%02X' % cor} em #{'%02X%02X%02X' % fundo}), "
                        f"por exemplo {onde}")
    r.info(f"(6) fonte >= 9 pt em todas as abas; (7) {len(combos)} combinações de texto e fundo com contraste "
           f">= 4,5:1 (menor: {min(R.contraste(a, b) for a, b in combos):.2f}:1)")

    # (8) C2: nenhuma linha de dados a mais de 15 linhas do cabeçalho da própria tabela -------------
    n_tab = 0
    for ws in wb.worksheets:
        if ws.title == "Dados":
            continue
        for t in tabs[ws.title]:
            n_tab += 1
            if t["linhas"]:
                d = t["linhas"][-1] - t["cab"]
                r.ok(d <= DISTANCIA_MAX_CABECALHO, f"'{ws.title}': tabela com cabeçalho na linha {t['cab']} vai até a "
                                                   f"linha {t['linhas'][-1]} ({d} > {DISTANCIA_MAX_CABECALHO} linhas)")
    r.info(f"(8) {n_tab} tabelas fora da aba Dados: toda linha de dados a até {DISTANCIA_MAX_CABECALHO} linhas "
           f"do cabeçalho")

    # (9) C3: a área do jogador cabe em 1360 px (Dados fora; avisos da Em Jogo em N com resumo em A13) ----
    resumo_ej = C.get("em_jogo.avisos_resumo")
    for ws in wb.worksheets:
        if ws.title == "Dados":
            continue
        x, borda = 0, {}
        for cc in range(1, ws.max_column + 1):
            x += R.px_coluna(ws, cc)
            borda[cc] = x
        fora = []
        for linha in ws.iter_rows():
            for cel in linha:
                if (cel.row, cel.column) in mescla[ws.title][1] or oculta(ws, cel.row, cel.column):
                    continue
                if cel.value is None and not R.eh_entrada(cel):
                    continue
                if borda[cel.column] <= LARGURA_TELA:
                    continue
                ref = f"'{ws.title}'!{cel.coordinate}"
                if ws.title == "Em Jogo" and cel.column_letter == "N" and resumo_ej:
                    continue          # avisos da Em Jogo: resumo visível em A13 (conferido abaixo)
                fora.append(cel.coordinate)
        r.ok(not fora, f"'{ws.title}': {len(fora)} célula(s) além de {LARGURA_TELA} px: {fora[:10]}")
    ws_ej = wb["Em Jogo"]
    if resumo_ej:
        _, rr, cc = separar(resumo_ej)
        r.ok(sum(R.px_coluna(ws_ej, k) for k in range(1, cc + 1)) <= LARGURA_TELA and rr <= 40,
             f"Em Jogo: o resumo dos avisos ({resumo_ej}) precisa ficar dentro da tela")
    larg = sum(R.px_coluna(ws_ej, k) for k in range(1, 13))
    alt = sum(R.px_linha(ws_ej, k) for k in range(1, 41))
    r.ok(larg <= LARGURA_TELA and alt <= 768, f"Em Jogo: A:L × 1-40 = {larg} × {alt} px (máximo 1360 × 768)")
    r.info(f"(9) área do jogador em até {LARGURA_TELA} px em 9 abas (colunas auxiliares ocultas); "
           f"Em Jogo A:L × 1-40 = {larg} × {alt} px")

    # (10) Aviso não bloqueante: coluna com mais que o dobro da largura do maior conteúdo -----------
    largas = []
    for (aba, cc), px in sorted(larg_conteudo.items()):
        ws = wb[aba]
        w = R.px_coluna(ws, cc)
        if px > 0 and w > 2 * px and w - px > 40:
            largas.append(f"'{aba}'!{get_column_letter(cc)} ({w} px, maior conteúdo {int(px)} px)")
    r.info(f"(10) aviso, não bloqueia: {len(largas)} coluna(s) com mais que o dobro do maior conteúdo"
           + (f": {'; '.join(largas[:12])}" if largas else ""))
    return r


# ---------------------------------------------------------------------------
# Suíte google — fidelidade com o Google Planilhas real (revisão 2)
# ---------------------------------------------------------------------------
# Verdade de referência: dois exports do Google feitos pelo usuário em 04/10/2026, guardados em
# build/google_rev1 (não alterar). O export "haloviano" (Raça Haloviano, 0 erros) traz os 2.363
# valores que o Google calculou para a ficha da revisão 1; o export "humano" traz os 261 #ERROR!
# do "+1 em dois". A revisão 1 também fica em build/google_rev1 (arquivo + mapa).

GOOGLE_REF = BUILD / "google_rev1"
GOOGLE_COPIA = GOOGLE_REF / "export-google-haloviano-0-erros.xlsx"
GOOGLE_ERRO = GOOGLE_REF / "export-google-humano-261-erros.xlsx"
REV1_XLSX = BUILD / "google_rev1" / "Ficha rev1.xlsx"
REV1_MAPA = BUILD / "google_rev1" / "ficha_mapa_rev1.json"
# rótulos que mudaram de propósito na revisão 2 (o Google lia os antigos como fórmula)
ROTULOS_REV2 = {"+2 em um": "Um Atributo (+2)", "+1 em dois": "Dois Atributos (+1 cada)",
                "+1 em um tipo de rolagem": "Um tipo de rolagem +1", "+1 de Velocidade": "Velocidade +1",
                "+2 de dano": "Dano +2", "+1 RD": "RD +1"}
# Células em que o LIVRO mudou da v1.1 para a v1.2 (auditoria de dominância): o export do Google é
# de 04/10/2026 e não pode ser refeito, então aqui fica, célula por célula, o que ele gravou e o que
# a v1.2 tem de trazer. Só este par exato é aceito; qualquer outro valor continua falhando.
# E3 = Espaço da arma Leve (24.2); E7 = duração do Choque (21.5); E9 = acúmulo do Cisalhamento de
# Vento (21.5); E16 = Ressonância IV condicionada à Bênção Avatar (26.7).
# E20 e E25 = o redesenho das Raças: o bônus do Haloviano foi de "Sincronia ou Presença" para
# "Discernimento ou Presença" (a redistribuição que deu a Poder e a Agilidade duas Raças cada),
# e o traço "To na sua mente" deixou de queimar o dia na falha de ativação e perdeu a cláusula
# que isentava o Caminho da Harmonia. O export do Google é da Raça Haloviano, então é nele que
# o redesenho aparece célula por célula; as outras seis Raças não têm células no export.
LIVRO_V12 = {
    "'Equipamento'!W71": (1, 0.5),
    "'Criação'!C25": ('Escolha onde vai o +2: Sincronia ou Presença',
                      'Escolha onde vai o +2: Discernimento ou Presença'),
    "'Criação'!N25": ('Sincronia',
                      'Discernimento'),
    "'Criação'!O25": ('Sincronia',
                      'Discernimento'),
    "'Criação'!B29": ('To na sua mente (2 vezes por dia, deixa o alvo Controlado)',
                      'To na sua mente (ativável: 2 vezes por dia, deixa o alvo Controlado) · Asas de '
                      'Halo (passivo: não sofre dano de queda)'),
    "'Criação'!B30": ('To na sua mente: 2 vezes por dia. Gaste a sua Ação Complementar. 1. Ativação. '
                      'Se você segue o Caminho da Harmonia, não há teste de ativação. Caso contrário, '
                      'faça um Teste de Sintonia contra DT 13; se falhar, você não pode usar este '
                      'traço até o próximo Descanso Longo. 2. Resistência do alvo. Em ambos os casos, '
                      'o alvo faz um Teste de Força de Vontade contra a sua DT (8 + Bônus do Atributo '
                      'de Habilidade + Eficiência). 3. Na falha do alvo, ele fica Controlado '
                      '(capítulo 21) por 2 turnos se for Comum, ou 1 turno se for Elite ou Boss. Não '
                      'funciona em Boss em cena de clímax sem autorização do Mestre. Fora de combate, '
                      'o Mestre define a duração pela cena — a referência é meia hora. A DT 13 da '
                      'ativação é fixa em todas as faixas e é uma das cinco DTs de subsistema do '
                      'livro (capítulo 02).',
                      'To na sua mente: 2 vezes por dia. Gaste a sua Ação Complementar. 1. Ativação. '
                      'Faça um Teste de Sintonia contra DT 13. Se falhar, este uso é gasto e nada '
                      'acontece. 2. Resistência do alvo. Se você passar, o alvo faz um Teste de Força '
                      'de Vontade contra a sua DT (8 + Bônus do Atributo de Habilidade + Eficiência). '
                      '3. Na falha do alvo, ele fica Controlado (capítulo 21) por 2 turnos se for '
                      'Comum, ou 1 turno se for Elite ou Boss. Não funciona em Boss em cena de clímax '
                      'sem autorização do Mestre. Fora de combate, o Mestre define a duração pela '
                      'cena — a referência é meia hora. A DT 13 da ativação é fixa em todas as faixas '
                      'e é uma das cinco DTs de subsistema do livro (capítulo 02). Asas de Halo: As '
                      'asas não levam o seu peso para cima, mas não deixam você cair. • Você não '
                      'sofre dano de queda, de nenhuma altura, e não faz Teste de Reflexos por cair '
                      '(capítulo 22). • Você desce planando: ao cair, ou ao pular de propósito, você '
                      'chega ao chão de pé, no ponto que escolher dentro de uma Distância do lugar de '
                      'onde saiu (capítulo 18). • Não é voo. Você não ganha altura, não ignora '
                      'terreno em combate, e isso não muda a sua Velocidade, a sua Ação de Movimento '
                      'nem a sua casa na Fila (capítulo 19).'),
    "'Em Jogo'!B10": ('—',
                      'Controlado 2× por dia; sem dano de queda'),
    "'Regras Rápidas'!H99": ("2 turnos", "3 turnos"),
    "'Regras Rápidas'!C100": ("Dano Contínuo 1d6 por acúmulo (Vento)",
                              "Dano Contínuo 1d6 por acúmulo (Vento), 1 acúmulo por ataque seu de Vento"),
    "'Progressão'!G70": ("Sua Ultimate ativa com 80 de Energia e consome 80 (o teto do medidor "
                         "continua 100); ou sua Bênção Avatar afeta um alvo adicional",
                         "Sua Ultimate ativa com 80 de Energia e consome 80 (o teto do medidor "
                         "continua 100); ou, se você tiver a Bênção Avatar do seu Caminho, ela "
                         "afeta um alvo adicional"),
}
# células da Início sem nome lógico na revisão 1 que desceram de linha na revisão 2
SEM_NOME_REV1 = {"'Início'!C17": "inicio.painel.total.texto"}


def _g_norm(v):
    if v is None or v == "":
        return ""
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return float(v)
    return v


def _g_igual(a, b):
    a, b = _g_norm(a), _g_norm(b)
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a is b
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) <= 1e-9
    return a == b


def _g_formulas(wb):
    return {f"'{ws.title}'!{c.coordinate}": c.value for ws in wb.worksheets for linha in ws.iter_rows()
            for c in linha if isinstance(c.value, str) and c.value.startswith("=")}


def _g_entradas(wv, mapa):
    """Entradas preenchidas no export do Google, pelo nome lógico do mapa dado."""
    saida = {}
    for nome in mapa["entradas"]:
        aba, cel = separar_ref(mapa["celulas"][nome])
        v = wv[aba][cel].value
        if v is not None:
            saida[nome] = v
    return saida


def suite_google(args):
    import collections
    import openpyxl
    r = Resultado("google")
    for p in (GOOGLE_COPIA, GOOGLE_ERRO, REV1_XLSX, REV1_MAPA, XLSX, MAPA_JSON):
        if not p.exists():
            r.falha(f"arquivo não encontrado: {p}")
            return r
    mapa1 = json.loads(REV1_MAPA.read_text(encoding="utf-8"))
    mapa2 = ler_mapa()
    wv_g = openpyxl.load_workbook(GOOGLE_COPIA, data_only=True)
    f_rev1 = _g_formulas(openpyxl.load_workbook(REV1_XLSX))
    ent_nomes = _g_entradas(wv_g, mapa1)
    r.info(f"export do Google (Cópia): {len(ent_nomes)} entradas preenchidas: "
           + ", ".join(f"{k} = {v!r}" for k, v in sorted(ent_nomes.items())))

    def google(ref):
        aba, cel = separar_ref(ref)
        return wv_g[aba][cel].value

    # (a) revisão 1 calculada pela formulas × o que o Google gravou ------------------------------
    m1 = Modelo(REV1_XLSX)
    res1 = m1.calcular(entradas={mapa1["celulas"][n]: v for n, v in ent_nomes.items()}, saidas=list(f_rev1))
    div1 = collections.Counter()
    for ref in f_rev1:
        if not r.ok(_g_igual(res1.get(ref), google(ref)),
                    f"(a) {ref}: formulas={res1.get(ref)!r} Google={google(ref)!r}"):
            div1[(type(_g_norm(res1.get(ref))).__name__, type(_g_norm(google(ref))).__name__)] += 1
    r.ok(len(f_rev1) == 2363, f"(a) a revisão 1 tinha 2363 fórmulas, veio {len(f_rev1)}")
    r.info(f"(a) revisão 1 × Google: {len(f_rev1) - sum(div1.values())} de {len(f_rev1)} células iguais; "
           f"divergências por tipo (formulas, Google): {dict(div1) or 'nenhuma'}")

    # (b) revisão 2 com as mesmas entradas × o que o Google gravou, ligadas pelo nome lógico ------
    wb2 = openpyxl.load_workbook(XLSX)
    f_rev2 = _g_formulas(wb2)
    nome_de1 = {v: k for k, v in mapa1["celulas"].items()}
    ligacao, sem_par = {}, []
    por_texto = collections.defaultdict(list)
    for ref, fx in f_rev2.items():
        por_texto[(separar_ref(ref)[0], fx)].append(ref)
    for ref in f_rev1:
        nome = nome_de1.get(ref)
        aba, cel = separar_ref(ref)
        nome = nome or SEM_NOME_REV1.get(ref)
        if nome and nome in mapa2["celulas"]:
            ligacao[ref] = mapa2["celulas"][nome]
        elif aba != "Início" and ref in f_rev2:
            ligacao[ref] = ref                      # mesma célula (as abas só ganharam colunas à direita)
        elif len(por_texto[(aba, f_rev1[ref])]) == 1:
            ligacao[ref] = por_texto[(aba, f_rev1[ref])][0]
        else:
            sem_par.append(ref)
    r.ok(not sem_par, f"(b) {len(sem_par)} célula(s) da revisão 1 sem par na revisão 2: {sem_par[:10]}")
    m2 = Modelo(XLSX)
    ins2 = {mapa2["celulas"][n]: v for n, v in ent_nomes.items()}
    res2 = m2.calcular(entradas=ins2, saidas=list(f_rev2))
    iguais, aceitas, aceitas_v12 = 0, [], []
    for ref1, ref2 in ligacao.items():
        g, l = google(ref1), res2.get(ref2)
        if _g_igual(l, g):
            iguais += 1
            r.ok(True, "")
            continue
        g_novo = g
        if isinstance(g, str):
            for a, b in ROTULOS_REV2.items():
                g_novo = g_novo.replace(a, b)
        if g_novo != g and _g_igual(l, g_novo):
            aceitas.append(f"{ref1} → {ref2}: Google={g!r}, revisão 2={l!r}")
            r.ok(True, "")
            continue
        par = LIVRO_V12.get(ref1)
        if par and _g_igual(g, par[0]) and _g_igual(l, par[1]):
            aceitas_v12.append(f"{ref1} → {ref2}: Google (v1.1)={g!r}, v1.2={l!r}")
            r.ok(True, "")
            continue
        r.falha(f"(b) {ref1} → {ref2}: revisão 2={l!r} Google={g!r} ({f_rev2.get(ref2, '')[:140]})")
    for x in aceitas:
        r.info(f"(b) divergência aceita (rótulo novo): {x}")
    for x in aceitas_v12:
        r.info(f"(b) divergência aceita (livro v1.2): {x}")
    sobra_v12 = sorted(set(LIVRO_V12) - {x.split(" → ")[0] for x in aceitas_v12})
    r.ok(not sobra_v12, f"(b) LIVRO_V12 lista célula que não divergiu mais: {sobra_v12}")
    r.info(f"(b) revisão 2 × Google: {iguais} de {len(f_rev1)} células iguais pelo nome lógico, "
           f"{len(aceitas)} divergência(s) aceita(s) por rótulo novo, {len(sem_par)} sem par; "
           f"{len(f_rev2) - len(set(ligacao.values()))} fórmulas novas da revisão 2 (camada, sinais, contador)")
    # as fórmulas novas, no mesmo estado, não podem dar erro e o contador fica em 0
    erros2 = [f"{k} = {v}" for k, v in res2.items() if eh_erro(v)]
    r.ok(not erros2, f"(b) revisão 2 no estado do Google com erro: {erros2[:8]}")
    r.ok(res2.get(mapa2["celulas"]["inicio.erros.total"]) == 0,
         f"(b) contador de erros = {res2.get(mapa2['celulas']['inicio.erros.total'])!r}, esperado 0")

    # evidência: o export com erro tem 261 #ERROR! e a única entrada diferente é Criação!B26 --------
    wv_e = openpyxl.load_workbook(GOOGLE_ERRO, data_only=True)
    n_err = sum(1 for ref in f_rev1 if str(wv_e[separar_ref(ref)[0]][separar_ref(ref)[1]].value).startswith("#ERROR"))
    ent_e = _g_entradas(wv_e, mapa1)
    dif = sorted(n for n in set(ent_e) | set(ent_nomes) if ent_e.get(n) != ent_nomes.get(n))
    r.info(f"evidência: export com erro tem {n_err} fórmula(s) com #ERROR!; entradas diferentes da Cópia: "
           + ", ".join(f"{n} = {ent_e.get(n)!r}" for n in dif))
    r.ok(str(ent_e.get("criacao.raca.modo")).startswith("#ERROR"),
         f"evidência: Criação!B26 deveria estar com #ERROR! no export, veio {ent_e.get('criacao.raca.modo')!r}")

    # (c) o caso do usuário: Humano + "Dois Atributos (+1 cada)" + Poder + Agilidade --------------
    caso = dict(ent_nomes)
    caso.update({"criacao.raca": "Humano", "criacao.raca.modo": "Dois Atributos (+1 cada)",
                 "criacao.raca.atributo1": "Poder", "criacao.raca.atributo2": "Agilidade"})
    res3 = m2.calcular(entradas={mapa2["celulas"][n]: v for n, v in caso.items()}, saidas=list(f_rev2))
    erros3 = [f"{k} = {v}" for k, v in res3.items() if eh_erro(v)]
    r.ok(not erros3, f"(c) caso do usuário com {len(erros3)} erro(s): {erros3[:8]}")
    tot3 = res3.get(mapa2["celulas"]["inicio.erros.total"])
    r.ok(tot3 == 0, f"(c) contador de erros = {tot3!r}, esperado 0")
    racial = {a: res3.get(mapa2["celulas"][f"criacao.atributo.{_slug(a)}.raca"]) for a in _ATR}
    r.ok(racial == {"Poder": 1, "Agilidade": 1, "Vigor": 0, "Sincronia": 0, "Discernimento": 0, "Presença": 0},
         f"(c) bônus racial (05: +1 em dois Atributos diferentes): {racial}")
    status = res3.get(mapa2["celulas"].get("criacao.raca.resumo", ""), None)
    r.info(f"(c) Humano + Dois Atributos (+1 cada) + Poder + Agilidade: {len(erros3)} erro(s), contador {tot3}, "
           f"bônus racial {racial}" + (f", resumo {status!r}" if status else ""))
    return r


# ---------------------------------------------------------------------------
# Registro das suítes
# ---------------------------------------------------------------------------

SUITES = {
    "spike": suite_spike,
    "protegidos": suite_protegidos,
    "dados": suite_dados,
    "ouro": suite_ouro,
    "oraculo": suite_oraculo,
    "extremos": suite_extremos,
    "lint": suite_lint,
    "texto": suite_texto,
    "preview": suite_preview,
    "visual": suite_visual,
    "google": suite_google,
}


def main():
    ap = argparse.ArgumentParser(description="Bateria de testes da ficha automatizada.")
    ap.add_argument("--suite", required=True, choices=list(SUITES) + ["tudo"])
    ap.add_argument("--so-oraculo", action="store_true",
                    help="na suíte ouro, confere só o oráculo (sem planilha)")
    args = ap.parse_args()
    nomes = list(SUITES) if args.suite == "tudo" else [args.suite]
    resultados = []
    for n in nomes:
        t0 = time.time()
        try:
            res = SUITES[n](args)
        except Exception as e:  # falha inesperada conta como falha da suíte
            import traceback
            res = Resultado(n)
            res.falha(f"exceção: {type(e).__name__}: {e}\n{traceback.format_exc()}")
        res.info(f"tempo da suíte: {time.time() - t0:.1f} s")
        res.imprimir()
        resultados.append(res)
    total_falhas = sum(len(x.falhas) for x in resultados)
    print("\n=== RESUMO")
    for x in resultados:
        print(f"  {x.nome:<11} {'OK' if not x.falhas else 'FALHOU':<7} "
              f"{x.checagens} checagens, {len(x.falhas)} falha(s)")
    sys.exit(1 if total_falhas else 0)


if __name__ == "__main__":
    main()
