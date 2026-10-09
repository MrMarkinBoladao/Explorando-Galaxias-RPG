# -*- coding: utf-8 -*-
"""
Aba Bestiário (R2, design §6.8, plano P7).

Filtro por faixa, tipo, Fraqueza, facção, ambiente (H8, lido da aba Tabelas), só com Resistência e só com
fases. Para cada ficha i: ordem_i = faixa·1000 + tipo·100 + i quando passa no filtro; N = SUMPRODUCT(ISNUMBER)*1
(sem COUNT); a k-ésima linha = INDEX(…, MATCH(SMALL(ordem, k), ordem, 0)) (sem FILTER/SORT).
Resultado em B1 (números) e B2 (dano, DT · TR, Fraquezas, Execução), blocos de 11/11/10 com cabeçalho
repetido, e a ficha completa com o texto do livro.
"""

import mestre_dados as D
from mestre import nucleo as N
from mestre.nucleo import T, ent, cal, rot, cabs, titulo, dcol, sugestao

NB = 32
B1 = [17, 30, 43]
B2 = [57, 70, 83]
NBLOCO = [11, 11, 10]
FICHA = 96
NOMES_LONGOS = [f["nome"] for f in D.bestiario()]
NLIN = 12


def montar(wb):
    ws = wb["Bestiário"]
    titulo(ws, 5, "Filtro (preencha; vazio = todas as fichas)")
    filtros = [("faixa", "Faixa", "lista.filtro_faixa", None), ("tipo", "Tipo", "lista.filtro_tipo", None),
               ("elemento", "Fraqueza (fase 1)", "lista.filtro_elemento", "C"),
               ("faccao", "Facção ou origem", "lista.filtro_faccao", "D"),
               ("ambiente", "Ambiente", "lista.filtro_ambiente", "D"),
               ("resistencia", "Só com Resistência?", "lista.sim_nao", None),
               ("fases", "Só com fases?", "lista.sim_nao", None)]
    for k, (ch, rot_, fonte, ate) in enumerate(filtros):
        r = 6 + k
        rot(ws, f"A{r}", rot_, negrito=True)
        ent(ws, f"B{r}", f"bestiario.filtro.{ch}", tipo="lista", fonte=fonte, ate=ate, rotulo=rot_, centro=True)
    sugestao(ws, "E10", "H8", "bestiario.h8.rotulo", ate="L", extra="o ambiente de cada facção vem da aba Tabelas.")
    rot(ws, "E6", "As Fraquezas sugeridas podem ser trocadas livremente para cumprir o contrato de encontro (28.2 "
                  "regra 7).", ate="L", italico=True)
    rot(ws, "A13", "Resultado", negrito=True)
    cal(ws, "B13", '=$O$5&" de 32 fichas"', nome="bestiario.resultado", ate="D")
    FF = {ch: T(f"bestiario.filtro.{ch}") for ch, *_ in filtros}
    blo = N.MAPA.blocos["dados.bestiario"]
    dl = lambda col, i: f"'Dados'!${blo['colunas'][col]}${blo['primeira_linha'] + i - 1}"  # noqa: E731
    fac, amb = T("tab.ambiente_por_faccao.valores"), T("tab.ambiente_por_faccao.ambientes")
    for i in range(1, NB + 1):
        rr = 10 + i
        fr = f"{dl('Fraqueza 1', i)}:{dl('Fraqueza 4', i)}"
        amb_ok = (f'OR(LEN({FF["ambiente"]})=0,{FF["ambiente"]}="Todos",COUNTIFS({fac},{dl("Facção ou origem", i)},'
                  f'{amb},{FF["ambiente"]})+IF(LEN({dl("Origem 2", i)})=0,0,COUNTIFS({fac},{dl("Origem 2", i)},{amb},'
                  f'{FF["ambiente"]}))>0)')
        passa = (f'AND(OR(LEN({FF["faixa"]})=0,{FF["faixa"]}="Todas",{FF["faixa"]}="Faixa "&{dl("Faixa", i)}),'
                 f'OR(LEN({FF["tipo"]})=0,{FF["tipo"]}="Todos",{FF["tipo"]}={dl("Tipo", i)}),'
                 f'OR(LEN({FF["elemento"]})=0,{FF["elemento"]}="Qualquer",COUNTIF({fr},{FF["elemento"]})>0),'
                 f'OR(LEN({FF["faccao"]})=0,{FF["faccao"]}="Todas",{FF["faccao"]}={dl("Facção ou origem", i)}),'
                 f'{amb_ok},OR({FF["resistencia"]}<>"Sim",LEN({dl("Resistência", i)})>0),'
                 f'OR({FF["fases"]}<>"Sim",{dl("Fases", i)}>1))')
        N.aux(ws, f"N{rr}", f'=IF({passa},{dl("Índice da faixa", i)}*1000+{dl("Índice do tipo", i)}*100+{i},"")',
              nome=f"bestiario.ordem{i}")
    N.aux(ws, "O5", "=SUMPRODUCT(ISNUMBER($N$11:$N$42)*1)", nome="bestiario.n")
    idx = {}
    k = 0
    titulo(ws, B1[0] - 2, "B1 · Números (automático, ordenado por faixa e tipo)")
    for b, r0 in enumerate(B1):
        cabs(ws, r0 - 1, {"A": "Nome", "B": "Tipo", "C": "Faixa", "D": "Facção ou origem", "E": "PV", "F": "Defesa",
                          "G": "RD", "H": "Tenacidade", "I": "VEL", "J": "Teste de Ataque"})
        for t in range(NBLOCO[b]):
            k += 1
            r = r0 + t
            N.aux(ws, f"P{r}", f'=IF({k}>$O$5,"",MATCH(SMALL($N$11:$N$42,{k}),$N$11:$N$42,0))',
                  nome=f"bestiario.idx{k}")
            ix = idx[k] = f"$P${r}"
            N.pior(ws, f"A{r}", NOMES_LONGOS)
            for col, coluna in (("A", "Nome"), ("B", "Tipo"), ("C", "Faixa"), ("D", "Facção ou origem"), ("E", "PV"),
                                ("F", "Defesa"), ("G", "RD"), ("H", "Tenacidade"), ("I", "VEL")):
                cal(ws, f"{col}{r}", f'=IF({ix}="","",INDEX({dcol("bestiario", coluna)},{ix}))',
                    nome=f"bestiario.b1.{k}.{col}", centro=col not in "AD", regra=col not in "AD")
            cal(ws, f"J{r}", f'=IF({ix}="","","+"&INDEX({dcol("bestiario", "Ataque")},{ix}))',
                nome=f"bestiario.b1.{k}.J", centro=True, regra=True)
    N.subtabela(ws, "B1", [r - 1 for r in B1], "A:J", NB)
    titulo(ws, B2[0] - 2, "B2 · Dano, Fraquezas e Execução (automático)")
    k = 0
    for b, r0 in enumerate(B2):
        cabs(ws, r0 - 1, {"A": "Nome", "B": ("Dano por acerto", "C"), "D": ("DT · Teste de Resistência", "E"),
                          "F": ("Fraquezas da fase 1", "G"), "H": "Resistência", "I": "Fases", "J": "Execução"})
        for t in range(NBLOCO[b]):
            k += 1
            r = r0 + t
            ix = idx[k]
            col = lambda c: f'INDEX({dcol("bestiario", c)},{ix})'  # noqa: E731
            cal(ws, f"A{r}", f'=IF({ix}="","",{col("Nome")})', nome=f"bestiario.b2.{k}.A")
            N.pior(ws, f"A{r}", NOMES_LONGOS)
            cal(ws, f"B{r}", f'=IF({ix}="","",{col("Dano por acerto")}&" · média "&{col("Média do dano")})',
                nome=f"bestiario.b2.{k}.B", ate="C", regra=True)
            cal(ws, f"D{r}", f'=IF({ix}="","","DT "&{col("DT dos efeitos")}&" · TR +"&{col("Teste de Resistência")})',
                nome=f"bestiario.b2.{k}.D", ate="E", centro=True, regra=True)
            cal(ws, f"F{r}", f'=IF({ix}="","",{col("Fraquezas (texto)")})', nome=f"bestiario.b2.{k}.F", ate="G",
                regra=True)
            cal(ws, f"H{r}", f'=IF({ix}="","",IF(LEN({col("Resistência")})>0,{col("Resistência")},"—"))',
                nome=f"bestiario.b2.{k}.H", centro=True, regra=True)
            cal(ws, f"I{r}", f'=IF({ix}="","",{col("Fases")})', nome=f"bestiario.b2.{k}.I", centro=True, regra=True)
            cal(ws, f"J{r}", f'=IF({ix}="","",{col("Execução")})', nome=f"bestiario.b2.{k}.J", centro=True, regra=True)
    N.subtabela(ws, "B2", [r - 1 for r in B2], "A:J", NB)
    _ficha(ws)
    r = FICHA + 7 + NLIN + 6       # +6: a linha +5 é a fase 3 da ficha (a nota escrevia por cima da fórmula)
    rot(ws, f"A{r}", "Os cinco inimigos com Resistência: Capataz Oco, Centurião Catafracto, Mestre de Cerimônias "
                     "Mascarado, Executora de Contrato, Arcanjo de Ferro-Vazio (28.11). As listas de Encontros e "
                     "Combate leem o Bestiário e os inimigos da campanha.", ate="L", italico=True)


def _ficha(ws):
    r0 = FICHA
    titulo(ws, r0, "Ficha completa (texto do livro)")
    rot(ws, f"A{r0 + 1}", "Ver criatura", negrito=True)
    ent(ws, f"B{r0 + 1}", "bestiario.ver", tipo="lista", fonte="lista.criaturas", ate="D", rotulo="Ver criatura")
    sel = f"$N${r0 + 1}"
    N.aux(ws, sel, f'=IFERROR(MATCH({T("bestiario.ver")},{dcol("bestiario", "Nome")},0),"")',
          nome="bestiario.ver.linha")
    ok = f"ISNUMBER({sel})"
    c = lambda col: f'INDEX({dcol("bestiario", col)},{sel})'  # noqa: E731
    linhas = [
        f'=IF({ok},{c("Nome")}&"  ·  "&{c("Tipo")}&" · "&{c("Origem no cartão")}&" · faixa "&{c("Faixa")}&'
        f'IF({c("Fases")}>1," · "&{c("Fases")}&" fases",IF({c("Tipo")}="Boss"," · fase única","")),"")',
        f'=IF({ok},{c("Frase")},"")',
        f'=IF({ok},"PV "&{c("PV")}&"   Defesa "&{c("Defesa")}&"   RD "&{c("RD")}&"   Tenacidade "&{c("Tenacidade")}&'
        f'"   VEL "&{c("VEL")},"")',
        f'=IF({ok},"Ataque +"&{c("Ataque")}&"    DT dos efeitos "&{c("DT dos efeitos")}&"    Teste de Resistência +"&'
        f'{c("Teste de Resistência")},"")',
        f'=IF({ok},"Fraquezas: "&{c("Fraquezas (texto)")}&"    Resistências: "&IF(LEN({c("Resistência")})>0,'
        f'{c("Resistência")},"—"),"")',
    ]
    for k, f in enumerate(linhas):
        cal(ws, f"A{r0 + 2 + k}", f, nome=f"bestiario.ficha.l{k + 1}", ate="L", regra=k in (2, 3, 4))
    N.pior(ws, f"A{r0 + 3}", max((f["frase"] for f in D.bestiario()), key=len))
    ra = r0 + 7
    N.cab(ws, f"A{ra}", "Fase · tipo")
    N.cab(ws, f"B{ra}", "Ataques e ações (texto do livro)", ate="L")
    nome = c("Nome")
    for k in range(1, NLIN + 1):
        r = ra + k
        ix = f"$O${r}"
        N.aux(ws, ix, f'=IF({ok},IFERROR(MATCH({nome}&"|{k}",{dcol("bestiario_acoes", "Chave")},0),""),"")',
              nome=f"bestiario.ficha.idx{k}")
        pec = lambda col: f'INDEX({dcol("bestiario_acoes", col)},{ix})'  # noqa: E731
        cal(ws, f"A{r}", f'=IF(ISNUMBER({ix}),IF({pec("Fase")}=0,{pec("Tipo")},"Fase "&{pec("Fase")}&" · "&'
                         f'{pec("Tipo")}),"")', nome=f"bestiario.ficha.tipo{k}")
        cal(ws, f"B{r}", f'=IF(ISNUMBER({ix}),{pec("Texto do livro")},"")', nome=f"bestiario.ficha.acao{k}",
            ate="L", regra=True)
        N.pior(ws, f"B{r}", max((x["texto"] for x in D.acoes()), key=len))
    N.subtabela(ws, "bestiario.ficha.acoes", [ra], "A:L", NLIN)
    r = ra + NLIN + 2
    cal(ws, f"A{r}", f'=IF({ok},"Na Fila: VEL "&{c("VEL")}&", "&{c("Firmeza")}&". "&{c("Na Fila (resto)")},"")',
        nome="bestiario.ficha.nafila", ate="L", regra=True)
    N.pior(ws, f"A{r}", "Na Fila: VEL 19, com Firmeza. " + max((f["na_fila_resto"] for f in D.bestiario()), key=len))
    fk = dcol("bestiario_fases", "Chave")
    for f_ in (1, 2, 3):
        rr = r + f_
        m = f'MATCH({nome}&"|{f_}",{fk},0)'
        fc = lambda col: f'INDEX({dcol("bestiario_fases", col)},{m})'  # noqa: E731
        fq = (f'{fc("Fraqueza 1")}&", "&{fc("Fraqueza 2")}&", "&{fc("Fraqueza 3")}&", "&{fc("Fraqueza 4")}')
        cal(ws, f"A{rr}", f'=IF({ok},IFERROR("Fase {f_} — "&{fc("Nome da fase")}&" ("&{fc("PV do topo")}&" a "&'
                          f'{fc("PV do piso")}&" PV): Fraquezas "&{fq}&"; Tenacidade "&{fc("Tenacidade")}&"; "&'
                          f'{fc("Ritmo")},""),"")', nome=f"bestiario.ficha.fase{f_}", ate="L", regra=True)
