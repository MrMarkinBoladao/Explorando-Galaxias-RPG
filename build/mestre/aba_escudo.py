# -*- coding: utf-8 -*-
"""
Aba Escudo do Mestre (R10; design §6.15): referência de mesa para imprimir em A4 paisagem, ajustada à largura, com a
área de impressão e as quebras de página gravadas (o Excel usa; o Google não, por isso cada página começa com a linha
"— Escudo do Mestre · página N de 5 —", o guia para as quebras personalizadas do diálogo de impressão do Google).

Todo número e todo trecho de regra é LIDO DA ABA DADOS por fórmula (fidelidade: a suíte dados confere o Escudo contra a
aba Dados e a aba Dados contra o .md). O mapa guarda, para cada célula, de que bloco/linha/coluna ela vem
(MAPA.extra["escudo"]). Páginas: 1 preparar (27.2–27.5, 28.2, 27.9 e o grupo agora); 2 inimigo e Tenacidade (28.3,
28.4, 20.2, 20.3); 3 combate (19.3–19.7, 20.4–20.6); 4 pessoas (21.5, 23.3–23.6); 5 mesa (17.2, 16.2, 29.12, 27.10).
O design pedia 3 páginas; com o corpo em 9 pt e a altura de uma A4 paisagem ajustada à largura, o conteúdo de §6.15
pede 5 (o gerador falha se uma página passar da altura: aba_escudo.paginas_altas).
"""

import re

from openpyxl.worksheet.pagebreak import Break, RowBreak
from openpyxl.worksheet.page import PageMargins

import gerar_ficha as G
from mestre import nucleo as N
from mestre.nucleo import T, q, cal, rot, cabs

PAGINAS = 5
LARG = {"A": 150, **{c: 130 for c in "BCDEFGHIJ"}, "K": 20, "L": 20}
MARGEM_LADO_POL, MARGEM_TOPO_POL = 0.3, 0.4
# A4 paisagem (297 × 210 mm) ajustada à largura: a área A:J (1320 px = 990 pt) ocupa a largura útil, então a altura
# útil, na escala da planilha, é (210 − 2 × topo) / (297 − 2 × lado) × 990 pt ≈ 666 pt; 5% de folga
ALTURA_PAGINA_PT = int(0.95 * (210 - 2 * 25.4 * MARGEM_TOPO_POL) / (297 - 2 * 25.4 * MARGEM_LADO_POL)
                       * sum(LARG[c] for c in "ABCDEFGHIJ") * 0.75)
FONTE_PT, LINHA_PT = 9, 13.5    # corpo do Escudo em 9 pt (o mínimo da casa) e a linha base de 13,5 pt
ESPEC = {}                      # nome lógico -> {"partes": [[bloco, coluna, i]], "formato": "{0} · {1}"}
PAGINAS_LINHAS = []             # [(primeira, última)] de cada página
# 27.10, a seleção que cabe (design §6.15): as 14 operações que a mesa mais consulta (linhas da tabela do livro)
CASOS_MESA = (1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)
_TEXTOS = []


def _formula(partes, formato):
    """Fórmula que monta `formato` ("+{0}", "{0} · {1}") com as células da aba Dados."""
    if formato == "{0}":
        return "=" + N.dcel(*partes[0])
    pecas = []
    for k, txt in enumerate(re.split(r"\{(\d+)\}", formato)):
        if k % 2:
            pecas.append(N.dcel(*partes[int(txt)]))
        elif txt:
            pecas.append(q(txt))
    return "=" + "&".join(pecas)


def dado(ws, cel, nome, partes, formato="{0}", ate=None, negrito=False, centro=False):
    """Célula do Escudo lida da aba Dados."""
    cal(ws, cel, _formula(partes, formato), nome=nome, ate=ate, negrito=negrito, centro=centro)
    ESPEC[nome] = {"partes": [list(p) for p in partes], "formato": formato}


def texto(ws, cel, nome, ids, ate="J", prefixo="", sufixo=""):
    """Trecho(s) de regra do bloco 'textos' (Dados), juntos por um espaço."""
    partes, fmt = [], prefixo
    for k, id_ in enumerate(ids):
        partes.append(("textos", "Texto", _TEXTOS.index(id_) + 1))
        fmt += ("" if k == 0 else " ") + "{" + str(k) + "}"
    dado(ws, cel, nome, partes, fmt + sufixo, ate=ate)


def tit(ws, r, s, c0="A", c1="J"):
    G.titulo(ws, f"{c0}{r}", s, ate=c1)
    if c0 != c1:
        ws.merge_cells(f"{c0}{r}:{c1}{r}")


def montar(wb):
    import mestre_dados3 as D3
    _TEXTOS[:] = [t[0] for t in D3.textos()]
    ESPEC.clear()
    PAGINAS_LINHAS.clear()
    ws = wb["Escudo do Mestre"]
    N.larguras_grade(ws, LARG)
    r = 5
    for k, pagina in enumerate((_pagina1, _pagina2, _pagina3, _pagina4, _pagina5), start=1):
        ini = 1 if k == 1 else r
        rot(ws, f"A{r}", f"— Escudo do Mestre · página {k} de {PAGINAS} · {pagina.__doc__.strip()} —", ate="J",
            negrito=True)
        N.reg(f"escudo.pagina{k}", ws, f"A{r}")
        r = pagina(ws, r + 1)
        PAGINAS_LINHAS.append((ini, r - 1))
    rot(ws, f"A{r}", f"Explorando Galáxias {N.VERSAO} · referência do Mestre · em dúvida, o capítulo vence", ate="J",
        italico=True)
    N.reg("escudo.rodape", ws, f"A{r}")
    PAGINAS_LINHAS[-1] = (PAGINAS_LINHAS[-1][0], r)
    # impressão: A4 paisagem, ajustada à largura, área A1:J, quebra no fim de cada página
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins = PageMargins(left=MARGEM_LADO_POL, right=MARGEM_LADO_POL, top=MARGEM_TOPO_POL,
                                  bottom=MARGEM_TOPO_POL, header=0.2, footer=0.2)
    ws.print_area = f"A1:J{r}"
    _compactar(ws, r)
    ws.row_breaks = RowBreak()
    for _, fim in PAGINAS_LINHAS[:-1]:
        ws.row_breaks.append(Break(id=fim))
    N.MAPA.extra["escudo"] = {"celulas": ESPEC, "paginas": PAGINAS_LINHAS, "altura_maxima_pt": ALTURA_PAGINA_PT}


def _compactar(ws, ultima):
    """Corpo em 9 pt e títulos de bloco em 10 pt (da linha 5 em diante), linha base de 13,5 pt: o ajuste de layout só
    aumenta a altura onde o texto quebra."""
    from copy import copy
    import renderizar_ficha as R
    for linha in ws.iter_rows(min_row=5, max_row=ultima):
        for c in linha:
            if c.value is None or c.font is None:
                continue
            f = copy(c.font)
            f.sz = 10 if R.cor_fundo(c) == R.COR_TITULO else FONTE_PT
            c.font = f
    for k in range(5, ultima + 1):
        ws.row_dimensions[k].height = LINHA_PT


def altura_pagina(ws, ini, fim):
    """Altura (pt) das linhas ini…fim, com a altura padrão de 15 pt nas que não foram ajustadas."""
    return sum((ws.row_dimensions[k].height or 15) for k in range(ini, fim + 1))


def paginas_altas(wb):
    ws = wb["Escudo do Mestre"]
    return [f"página {k}: linhas {a}–{b}, {altura_pagina(ws, a, b):.0f} pt (máximo {ALTURA_PAGINA_PT})"
            for k, (a, b) in enumerate(PAGINAS_LINHAS, start=1) if altura_pagina(ws, a, b) > ALTURA_PAGINA_PT]


# ---------------------------------------------------------------------------
# As páginas (a docstring é o nome da página)
# ---------------------------------------------------------------------------

def _pagina1(ws, r):
    """Preparar a sessão e o encontro; descanso"""
    tit(ws, r, "DT por faixa — 27.2 (a única tabela de DT geral)", "A", "F")
    tit(ws, r, "As cinco DTs de subsistema — 27.3", "G", "J")
    cabs(ws, r + 1, {"A": "Dificuldade", "B": "1-4", "C": "5-8", "D": "9-12", "E": "13-16", "F": "17-20",
                     "G": ("Teste", "H"), "I": ("DT (capítulo)", "J")})
    for i in range(1, 7):
        rr = r + 1 + i
        dado(ws, f"A{rr}", f"escudo.dt.{i}.nome", [("dt_faixa", "Dificuldade", i)], negrito=True)
        for c, fx in zip("BCDEF", ("1-4", "5-8", "9-12", "13-16", "17-20")):
            dado(ws, f"{c}{rr}", f"escudo.dt.{i}.{N.slug(fx)}", [("dt_faixa", fx, i)], centro=True)
        if i <= 5:
            dado(ws, f"G{rr}", f"escudo.sub.{i}.teste", [("dt_subsistema", "Teste", i)], ate="H")
            dado(ws, f"I{rr}", f"escudo.sub.{i}.dt", [("dt_subsistema", "DT", i), ("dt_subsistema", "Capítulo", i)],
                 "{0} (capítulo {1})", ate="J")
    rot(ws, f"G{r + 7}", "Elas vencem a tabela de 27.2. Não existe uma sexta.", ate="J", italico=True)
    texto(ws, f"A{r + 8}", "escudo.dt.regras", ["dt.1", "dt.2", "dt.3"], prefixo="Três regras (27.2): ")
    r += 9
    tit(ws, r, "Orçamento do encontro — 27.4 (grupo de 4; o custo é o PV do inimigo)", "A", "F")
    tit(ws, r, "As quatro composições — 27.4", "G", "J")
    cabs(ws, r + 1, {"A": "Faixa", "B": "Dano por Ciclo", "C": "Orçamento", "D": "Comum", "E": "Elite", "F": "Boss",
                     "G": ("Composição", "H"), "I": ("Duração", "J")})
    for i in range(1, 6):
        rr = r + 1 + i
        dado(ws, f"A{rr}", f"escudo.orc.{i}.faixa", [("orcamento", "Faixa", i)], negrito=True)
        for c, col in zip("BCDEF", ("Dano do grupo por Ciclo", "Orçamento", "Custo Comum", "Custo Elite", "Custo Boss")):
            dado(ws, f"{c}{rr}", f"escudo.orc.{i}.{N.slug(col)}", [("orcamento", col, i)], centro=True)
        if i <= 4:
            dado(ws, f"G{rr}", f"escudo.comp.{i}.nome", [("composicoes", "Composição", i)], ate="H")
            dado(ws, f"I{rr}", f"escudo.comp.{i}.duracao", [("composicoes", "Duração esperada", i)], ate="J")
    rot(ws, f"G{r + 6}", "Metade do orçamento = cena de passagem, 2 Ciclos. Alvo: 3 a 5 Ciclos.", ate="J", italico=True)
    texto(ws, f"A{r + 7}", "escudo.contrato", ["contrato", "regra_irma"], prefixo="Contrato da Fraqueza (27.5): ")
    dado(ws, f"A{r + 8}", "escudo.acoes",
         [("acoes_tipo", "Tipo", 1), ("acoes_tipo", "Por turno", 1), ("acoes_tipo", "Tipo", 2),
          ("acoes_tipo", "Por turno", 2), ("acoes_tipo", "Tipo", 3), ("acoes_tipo", "Por turno", 3)],
         "Ações agressivas por turno (28.2 regra 5): {0}, {1} · {2}, {3} · {4}, {5}. Fraquezas: Comum 1 a 2, Elite 3, "
         "Boss 4 (28.2 regra 7).", ate="J")
    r += 9
    tit(ws, r, "Aprovar uma Ultimate — 27.9: ela lê o capítulo 16 no Nível equivalente da faixa", "A", "F")
    tit(ws, r, "Para o grupo agora (aba Campanha)", "G", "J")
    cabs(ws, r + 1, {"A": "Faixa", "B": "Nível equivalente", "C": ("Dano", "D"), "E": ("Cura", "F")})
    for i in range(1, 6):
        rr = r + 1 + i
        dado(ws, f"A{rr}", f"escudo.ult.{i}.faixa", [("ultimate_faixa", "Faixa", i)], negrito=True)
        dado(ws, f"B{rr}", f"escudo.ult.{i}.nivel", [("ultimate_faixa", "Nível equivalente", i)], centro=True)
        dado(ws, f"C{rr}", f"escudo.ult.{i}.dano", [("ultimate_faixa", "Dano", i), ("ultimate_faixa", "Média do dano", i)],
             "{0} ({1})", ate="D", centro=True)
        dado(ws, f"E{rr}", f"escudo.ult.{i}.cura", [("ultimate_faixa", "Cura", i), ("ultimate_faixa", "Média da cura", i)],
             "{0} ({1})", ate="F", centro=True)
    _grupo_agora(ws, r + 1)
    texto(ws, f"A{r + 7}", "escudo.ult.regras", ["ultimate.3", "ultimate.4"])
    return _descanso(ws, r + 8)


def _descanso(ws, r):
    tit(ws, r, "Descanso — 23.6", "A", "F")
    tit(ws, r, "PV por Descanso Curto (Vigor +2) — 23.6", "G", "J")
    cabs(ws, r + 1, {"A": "Tipo", "B": "Tempo", "C": "Quantas", "D": ("Recupera", "F"), "G": ("Nível", "H"),
                     "I": ("PV", "J")})
    for i in range(1, 3):
        dado(ws, f"A{r + 1 + i}", f"escudo.desc.{i}.tipo", [("descanso", "Tipo", i)], negrito=True)
        dado(ws, f"B{r + 1 + i}", f"escudo.desc.{i}.tempo", [("descanso", "Tempo", i)], centro=True)
        dado(ws, f"C{r + 1 + i}", f"escudo.desc.{i}.quantas", [("descanso", "Quantas", i)], centro=True)
        dado(ws, f"D{r + 1 + i}", f"escudo.desc.{i}.recupera", [("descanso", "Recupera", i)], ate="F")
    for i in range(1, 6):
        dado(ws, f"G{r + 1 + i}", f"escudo.dcurto.{i}.nivel", [("descanso_curto", "Nível", i)], ate="H", centro=True)
        dado(ws, f"I{r + 1 + i}", f"escudo.dcurto.{i}.pv", [("descanso_curto", "PV", i)], ate="J", centro=True)
    return r + 7


def _grupo_agora(ws, r):
    """Os números da faixa do grupo: Ultimate (27.9), Descanso Curto com Vigor +2 (23.6) e teto de PV temporários
    (23.3) — calculados a partir do nível da aba Campanha, números de regra (o oráculo e o ouro conferem)."""
    NV, FX, EF = T("campanha.nivel_ef"), T("campanha.faixa"), T("campanha.ef")
    k = f"MATCH({FX},{N.dcol('ultimate_faixa', 'Faixa')},0)"
    vals = {}
    for j, (nome, f) in enumerate((("ult_nivel", f"=INDEX({N.dcol('ultimate_faixa', 'Nível equivalente')},{k})"),
                                   ("ult_dano", f"=INDEX({N.dcol('ultimate_faixa', 'Média do dano')},{k})"),
                                   ("ult_cura", f"=INDEX({N.dcol('ultimate_faixa', 'Média da cura')},{k})"),
                                   ("descanso", f"=2*{NV}+2"), ("pv_temp", f"=3*{EF}"))):
        N.aux(ws, f"N{r + j}", f, nome=f"escudo.grupo.{nome}")
        N.MAPA.numeros_de_regra[f"escudo.grupo.{nome}"] = N.MAPA.celulas[f"escudo.grupo.{nome}"]
        vals[nome] = T(f"escudo.grupo.{nome}")
    linhas = [("nivel", f'="Nível "&{NV}&", faixa "&{FX}&", Eficiência +"&{EF}'),
              ("ultimate", f'="Ultimate: Nível equivalente "&{vals["ult_nivel"]}&"; dano médio "&{vals["ult_dano"]}&'
                           f'", cura média "&{vals["ult_cura"]}&" (27.9)"'),
              ("descanso", f'="Descanso Curto: "&{vals["descanso"]}&" PV com Vigor +2 (23.6)"'),
              ("pv_temp", f'="Teto de PV temporários: "&{vals["pv_temp"]}&" (23.3)"'),
              ("ph", f'="PH do grupo: máximo "&{T("campanha.ph_max")}&", início "&{T("campanha.ph_ini")}&" (16.2)"')]
    for j, (nome, f) in enumerate(linhas):
        cal(ws, f"G{r + j}", f, nome=f"escudo.grupo.{nome}.texto", ate="J")
    N.constante("descanso_curto", "2 × nível + Bônus de Vigor (Vigor +2 na tabela)", "23.6")
    N.constante("pv_temp", "3 × Eficiência", "23.3")


def _pagina2(ws, r):
    """O inimigo, a Tenacidade e o PH"""
    tit(ws, r, "Âncoras do inimigo — 28.3: copie a linha (o dano em dados · a média)")
    hdr = {"A": "Faixa · tipo", "B": "PV", "C": "Defesa", "D": "RD", "E": "Tenacidade", "F": "VEL", "G": "Ataque",
           "H": "Dano por acerto", "I": "DT dos efeitos", "J": "Teste de Resistência"}
    rr = r + 1
    for i in range(1, 16):
        if i in (1, 10):
            cabs(ws, rr, hdr)
            rr += 1
        p = f"escudo.anc.{i}"
        dado(ws, f"A{rr}", f"{p}.rotulo", [("ancoras", "Faixa", i), ("ancoras", "Tipo", i)], "{0} · {1}", negrito=True)
        for c, col, fmt in (("B", "PV", "{0}"), ("C", "Defesa", "{0}"), ("D", "RD", "{0}"), ("E", "Tenacidade", "{0}"),
                            ("F", "VEL", "{0}"), ("G", "Ataque", "+{0}"), ("I", "DT dos efeitos", "{0}"),
                            ("J", "Teste de Resistência", "+{0}")):
            dado(ws, f"{c}{rr}", f"{p}.{N.slug(col)}", [("ancoras", col, i)], fmt, centro=True)
        dado(ws, f"H{rr}", f"{p}.dano", [("ancoras", "Dano por acerto", i), ("ancoras", "Média do dano", i)],
             "{0} · {1}", centro=True)
        rr += 1
    texto(ws, f"A{rr}", "escudo.regua", ["regua.normal", "regua.dano", "regua.controle"],
          prefixo="Régua das ações (28.4): ")
    r = rr + 1
    tit(ws, r, "Fraqueza e Resistência — 20.2", "A", "F")
    tit(ws, r, "Redução de Tenacidade — 20.3", "G", "J")
    cabs(ws, r + 1, {"A": ("Situação", "B"), "C": ("Dano", "D"), "E": ("Redução de Tenacidade", "F"),
                     "G": ("Fonte", "I"), "J": "Redução"})
    for i in range(1, 4):
        dado(ws, f"A{r + 1 + i}", f"escudo.fr.{i}.situacao", [("fraqueza_resistencia", "Situação", i)], ate="B")
        dado(ws, f"C{r + 1 + i}", f"escudo.fr.{i}.dano", [("fraqueza_resistencia", "Dano", i)], ate="D")
        dado(ws, f"E{r + 1 + i}", f"escudo.fr.{i}.rt", [("fraqueza_resistencia", "Redução de Tenacidade", i)], ate="F")
    for i in range(1, 10):
        dado(ws, f"G{r + 1 + i}", f"escudo.ten.{i}.fonte", [("tenacidade_livro", "Fonte", i)], ate="I")
        dado(ws, f"J{r + 1 + i}", f"escudo.ten.{i}.rt", [("tenacidade_livro", "Redução de Tenacidade", i)], centro=True)
    texto(ws, f"A{r + 5}", "escudo.tenacidade_acerto", ["tenacidade.acerto"], ate="F")
    r += 11
    tit(ws, r, "Pontos de Habilidade do grupo — 16.2 (máximo · início do combate)", "A", "F")
    tit(ws, r, "O que o PH é", "G", "J")
    cabs(ws, r + 1, {"A": "Nº de jogadores", "B": ("Níveis 1-8", "C"), "D": "Níveis 9-16", "E": ("Níveis 17-20", "F")})
    for i in range(1, 5):
        rr = r + 1 + i
        dado(ws, f"A{rr}", f"escudo.ph.{i}.jogadores", [("ph", "Nº de jogadores", i)], centro=True, negrito=True)
        for c, fx, ate in (("B", "1-8", "C"), ("D", "9-16", None), ("E", "17-20", "F")):
            dado(ws, f"{c}{rr}", f"escudo.ph.{i}.{N.slug(fx)}", [("ph", f"Máximo {fx}", i), ("ph", f"Início {fx}", i)],
                 "{0} · {1}", ate=ate, centro=True)
    texto(ws, f"G{r + 1}", "escudo.ph.regra", ["ph", "ph_ganho"], ate="J")
    return r + 6


def _pagina3(ws, r):
    """Combate: a Fila, a Quebra e o Dano Contínuo"""
    tit(ws, r, "A Fila — 19.3 (nada é rolado) e a Surpresa")
    texto(ws, f"A{r + 1}", "escudo.fila.a", ["fila.1", "fila.2"], prefixo="1-2. ")
    texto(ws, f"A{r + 2}", "escudo.fila.b", ["fila.3", "fila.4"], prefixo="3-4. ")
    texto(ws, f"A{r + 3}", "escudo.surpresa", ["surpresa.1", "surpresa.2"], prefixo="Surpresa: ")
    r += 4
    tit(ws, r, "Firmeza — 19.4 (Elite e Boss), nesta ordem", "A", "F")
    tit(ws, r, "Teto de Atraso por alvo, por Ciclo — 19.4", "G", "J")
    cabs(ws, r + 1, {"G": ("Tipo de alvo", "H"), "I": "Teto", "J": "Firmeza"})
    for k in range(1, 5):
        texto(ws, f"A{r + k}", f"escudo.firmeza.{k}", [f"firmeza.{k}"], ate="F", prefixo=f"{k}. ")
    for i in range(1, 3):
        dado(ws, f"G{r + 1 + i}", f"escudo.teto.{i}.tipo", [("teto_atraso", "Tipo de alvo", i)], ate="H")
        dado(ws, f"I{r + 1 + i}", f"escudo.teto.{i}.teto", [("teto_atraso", "Teto", i)], centro=True)
        dado(ws, f"J{r + 1 + i}", f"escudo.teto.{i}.firmeza", [("teto_atraso", "Firmeza", i)], centro=True)
    rot(ws, f"G{r + 4}", "Já agiu, ou sem casas atrás: vira Atraso pendente do próximo Ciclo.", ate="J", italico=True)
    r += 5
    texto(ws, f"A{r}", "escudo.avancar", ["avancar", "avanco_total"], prefixo="Avançar (19.5): ")
    texto(ws, f"A{r + 1}", "escudo.congelamento", ["congelamento.comum", "congelamento.elite"],
          prefixo="Congelamento (19.6), Comum: ")
    r += 2
    tit(ws, r, "Casos-limite da Fila — 19.7")
    cabs(ws, r + 1, {"A": ("Situação", "C"), "D": ("Resolução", "J")})
    for i in range(1, 10):
        dado(ws, f"A{r + 1 + i}", f"escudo.casos_fila.{i}.situacao", [("casos_fila", "Situação", i)], ate="C")
        dado(ws, f"D{r + 1 + i}", f"escudo.casos_fila.{i}.resolucao", [("casos_fila", "Resolução", i)], ate="J")
    r += 11
    tit(ws, r, "Quebra — 20.4, nesta ordem", "A", "F")
    tit(ws, r, "Dano Contínuo — 20.6", "G", "J")
    for k in range(1, 6):
        texto(ws, f"A{r + k}", f"escudo.quebra.{k}", [f"quebra.{k}"], ate="F", prefixo=f"{k}. ")
        texto(ws, f"G{r + k}", f"escudo.dc.{k}", [f"dc.{k}"], ate="J", prefixo="• ")
    r += 6
    tit(ws, r, "Dano de Quebra — 20.5 (a Eficiência é de quem quebrou)")
    cabs(ws, r + 1, {"A": "Elemento", "B": ("Dano de Quebra", "D"), "E": ("Efeito de Quebra", "G"),
                     "H": "Elemento", "I": "Dano de Quebra", "J": "Efeito de Quebra"})
    for i in range(1, 8):            # 4 à esquerda, 3 à direita
        rr = r + 1 + (i if i <= 4 else i - 4)
        if i <= 4:
            cs = ("A", "B", "D", "E", "G")
        else:
            cs = ("H", "I", None, "J", None)
        dado(ws, f"{cs[0]}{rr}", f"escudo.quebra_dano.{i}.elemento", [("elementos", "Elemento", i)], negrito=True)
        dado(ws, f"{cs[1]}{rr}", f"escudo.quebra_dano.{i}.dano", [("elementos", "Dano de Quebra", i)], ate=cs[2])
        dado(ws, f"{cs[3]}{rr}", f"escudo.quebra_dano.{i}.efeito", [("elementos", "Efeito de Quebra", i)], ate=cs[4])
    return r + 6


def _pagina4(ws, r):
    """Pessoas: condições, Morrendo e PV temporários"""
    tit(ws, r, "Condições — 21.5 (cura não remove condição; acúmulos no máximo 5)")
    hdr = {"A": "Condição", "B": ("Efeito", "H"), "I": "Duração", "J": "Acúmulo"}
    rr = r + 1
    for i in range(1, 17):
        if i in (1, 9):
            cabs(ws, rr, hdr)
            rr += 1
        dado(ws, f"A{rr}", f"escudo.cond.{i}.nome", [("condicoes", "Condição", i)], negrito=True)
        dado(ws, f"B{rr}", f"escudo.cond.{i}.efeito", [("condicoes", "Efeito", i)], ate="H")
        dado(ws, f"I{rr}", f"escudo.cond.{i}.duracao", [("condicoes", "Duração", i)], centro=True)
        dado(ws, f"J{rr}", f"escudo.cond.{i}.acumulo", [("condicoes", "Acúmulo", i)], centro=True)
        rr += 1
    r = rr
    tit(ws, r, "Morrendo — 23.4", "A", "F")
    tit(ws, r, "Executado — 23.5", "G", "J")
    texto(ws, f"A{r + 1}", "escudo.morrendo", ["morrendo"], ate="F")
    texto(ws, f"G{r + 1}", "escudo.executado", ["executado", "intervir"], ate="J")
    cabs(ws, r + 2, {"A": "Resultado", "B": ("Efeito", "F")})
    for i in range(1, 7):
        dado(ws, f"A{r + 2 + i}", f"escudo.morr.{i}.resultado", [("morrendo", "Resultado", i)])
        dado(ws, f"B{r + 2 + i}", f"escudo.morr.{i}.efeito", [("morrendo", "Efeito", i)], ate="F")
    texto(ws, f"G{r + 4}", "escudo.executado.4", ["executado.4"], ate="J")
    r += 9
    tit(ws, r, "Teto de PV temporários — 23.3", "A", "F")
    rot(ws, f"A{r + 1}", "Níveis", negrito=True)
    for i in range(1, 8):
        c = "BCDEFGH"[i - 1]
        dado(ws, f"{c}{r + 1}", f"escudo.pvt.{i}.niveis", [("pv_temp", "Níveis", i)], centro=True)
        dado(ws, f"{c}{r + 2}", f"escudo.pvt.{i}.teto", [("pv_temp", "Teto", i)], centro=True)
    rot(ws, f"A{r + 2}", "Teto", negrito=True)
    texto(ws, f"A{r + 3}", "escudo.pv_temp", ["pv_temp"])
    return r + 4


def _pagina5(ws, r):
    """Mesa: Energia, tetos e casos-limite"""
    tit(ws, r, "De onde vem a Energia — 17.2", "A", "F")
    tit(ws, r, "Tetos que a mesa esquece — 29.12", "G", "J")
    cabs(ws, r + 1, {"A": ("Fonte", "C"), "D": "Energia", "E": ("Limite", "F")})
    for i in range(1, 9):
        dado(ws, f"A{r + 1 + i}", f"escudo.energia.{i}.fonte", [("energia", "Fonte", i)], ate="C")
        dado(ws, f"D{r + 1 + i}", f"escudo.energia.{i}.energia", [("energia", "Energia", i)], centro=True)
        dado(ws, f"E{r + 1 + i}", f"escudo.energia.{i}.limite", [("energia", "Limite", i)], ate="F")
    for i in range(1, 8):
        dado(ws, f"G{r + i}", f"escudo.teto.{i}", [("tetos", "Teto", i)], ate="J")
    texto(ws, f"G{r + 8}", "escudo.rolagem", ["rolagem", "falhe"], ate="J")
    texto(ws, f"A{r + 10}", "escudo.energia.regra", ["energia"])
    r += 11
    tit(ws, r, "Casos-limite de mesa — 27.10 (a seleção que cabe; a tabela inteira está na aba Dados)")
    hdr = {"A": ("Operação", "B"), "C": ("Quando falha", "D"), "E": ("O que acontece", "J")}
    rr = r + 1
    for n, i in enumerate(CASOS_MESA):
        if n in (0, 12):
            cabs(ws, rr, hdr)
            rr += 1
        dado(ws, f"A{rr}", f"escudo.casos_mesa.{i}.operacao", [("casos_mesa", "Operação", i)], ate="B", negrito=True)
        dado(ws, f"C{rr}", f"escudo.casos_mesa.{i}.falha", [("casos_mesa", "Quando falha", i)], ate="D")
        dado(ws, f"E{rr}", f"escudo.casos_mesa.{i}.acontece", [("casos_mesa", "O que acontece", i)], ate="J")
        rr += 1
    return rr
