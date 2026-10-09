# -*- coding: utf-8 -*-
"""
Aba Encontros — Construtor de Encontros (R3, design §6.9).

Orçamento de 27.4 (H5 para grupo ≠ 4), três encontros salvos (A, B, C) em sub-tabelas E1/E2 de 8 linhas,
custo (= PV; Escória 1,5 × PV, 28.10), % do orçamento, Ciclos estimados (H7), leitura de dificuldade (H6),
composição reconhecida (27.4), contrato da Fraqueza e regra irmã (27.5), DT para descobrir Fraqueza (20.2),
avisos de ficha (28.7, 28.8, 28.11), attrition (27.7) e "sem XP" (26.1). Encontro aleatório G = 100 por
ambiente (H8) e faixa, com a troca de Fraqueza sugerida (H19). Linha de saída = colunas de E1 (D6).
"""

from openpyxl.utils import get_column_letter as L, column_index_from_string as CI

import mestre_dados as D
from mestre import nucleo as N
from mestre import sorteio as S
from mestre.nucleo import T, q, ent, cal, av, rot, cabs, titulo, dcol, sugestao, sugestao_formula

ELEM = D.ELEMENTOS
NL = 8
ENC = {"A": 18, "B": 46, "C": 74}         # linha do título de cada encontro salvo
ALE = 103                                 # título do encontro aleatório
G_ENC = 100
CAUX = {k: L(CI("N") + i) for i, k in enumerate(
    ["idx", "q", "w1", "w2", "w3", "w4", "res", "tipo", "fidx", "custo", "acoes", "cum", "resbad", "solo", "germe",
     "fdif", "fidxq", "nome", "nesc", "peso"])}


def cat(c, idx):
    s = '&""' if c in ("f1", "f2", "f3", "f4", "res", "nome", "execucao", "tipo", "faixa") else ""
    return f'INDEX({T("inimigos.cat." + c)},{idx}){s}'


def montar(wb):
    ws = wb["Encontros"]
    _parametros(ws)
    for X, r0 in ENC.items():
        _encontro(ws, X, r0)
    _aleatorio(ws)


def _parametros(ws):
    titulo(ws, 5, "Parâmetros e orçamento (27.4)")
    cabs(ws, 6, {"A": "Campo", "B": ("Valor", "C"), "D": ("Troca opcional (preencha)", "E"),
                 "F": ("De onde vem", "J"), "K": ("Aviso", "L")})
    rot(ws, "A7", "Nº de PJs", negrito=True)
    ent(ws, "D7", "encontros.npj_troca", tipo="inteiro", minimo=1, maximo=6, ate="E", rotulo="Nº de PJs", centro=True)
    cal(ws, "B7", f'=IF(ISNUMBER({T("encontros.npj_troca")}),MIN(6,MAX(1,INT({T("encontros.npj_troca")}))),'
                  f'{T("campanha.jogadores_ef")})', nome="encontros.npj", ate="C", centro=True, regra=True)
    rot(ws, "F7", "Aba Campanha (nº de jogadores; vazio = nº de PJs do Grupo).", ate="J")
    rot(ws, "A8", "Faixa do encontro", negrito=True)
    ent(ws, "D8", "encontros.faixa_troca", tipo="lista", fonte="lista.faixas", ate="E", rotulo="Faixa", centro=True)
    fx = dcol("faixas", "Faixa")
    ft = N.faixa_da_lista(T("encontros.faixa_troca"))
    cal(ws, "B8", f'=IF(LEN({ft})>0,{ft},{T("campanha.faixa")})', nome="encontros.faixa", ate="C", centro=True,
        regra=True)
    N.aux(ws, "N8", f'=MATCH({T("encontros.faixa")},{fx},0)', nome="encontros.fidx")
    rot(ws, "F8", "A faixa do inimigo é a faixa do grupo (28.4 passo 1).", ate="J")
    FI = T("encontros.fidx")
    rot(ws, "A9", "Orçamento (grupo de 4)", negrito=True)
    cal(ws, "B9", f'=INDEX({dcol("orcamento", "Orçamento")},{FI})', nome="encontros.orc4", ate="C", centro=True,
        regra=True)
    rot(ws, "F9", "27.4: orçamento = o dano que o grupo entrega em 4 Ciclos.", ate="J")
    rot(ws, "A10", "Dano do grupo por Ciclo (4)", negrito=True)
    cal(ws, "B10", f'=INDEX({dcol("orcamento", "Dano do grupo por Ciclo")},{FI})', nome="encontros.dpc4", ate="C",
        centro=True, regra=True)
    rot(ws, "F10", "27.4 (mesa de 4 personagens, 29.1).", ate="J")
    rot(ws, "A11", "Orçamento deste grupo", negrito=True)
    NP = T("encontros.npj")
    cal(ws, "B11", f'=IF({NP}=4,{T("encontros.orc4")},INT({T("encontros.orc4")}*{NP}/4))', nome="encontros.orc",
        ate="C", centro=True, regra=True)
    rot(ws, "A12", "Dano por Ciclo deste grupo", negrito=True)
    cal(ws, "B12", f'=IF({NP}=4,{T("encontros.dpc4")},INT({T("encontros.dpc4")}*{NP}/4))', nome="encontros.dpc",
        ate="C", centro=True, regra=True)
    cal(ws, "F11", f'=IF({NP}=4,"Igual a 27.4 (4 personagens).","Grupo de "&{NP}&": 27.4 × "&{NP}&"/4 — '
                   f'{N.ROTULO_SUGESTAO} (H5)")', nome="encontros.h5", ate="J")
    sugestao_formula("encontros.h5", "H5", ["B11", "B12"])
    rot(ws, "A14", "Montar em quatro passos (27.4): (1) leia a faixa; (2) gaste o orçamento escolhendo tipos; (3) "
                   "escolha as Fraquezas cumprindo o contrato de 27.5; (4) confira as ações agressivas por Ciclo.",
        ate="L", italico=True)
    rot(ws, "A15", "Criatura: inimigos da campanha (aba Inimigos) e as 32 do Bestiário; a lista procura primeiro os "
                   "da campanha. Quantidade vazia = 1. Fraquezas nesta cena vazias = as da ficha.", ate="L",
        italico=True)
    av(ws, "K7", "encontros.aviso.npj", f'=IF(AND(ISNUMBER({T("encontros.npj_troca")}),OR({T("encontros.npj_troca")}<1,'
                                        f'{T("encontros.npj_troca")}>6)),"Nº de PJs fora de 1 a 6: usando o limite","")',
       ate="L")


def _encontro(ws, X, r0):
    p = f"encontros.{X}"
    titulo(ws, r0, f"Encontro {X}")
    rot(ws, f"A{r0 + 1}", "Nome do encontro", negrito=True)
    ent(ws, f"B{r0 + 1}", f"{p}.nome", ate="E", maximo=60, rotulo="Nome do encontro")
    rot(ws, f"F{r0 + 1}", "Ambiente", negrito=True)
    ent(ws, f"G{r0 + 1}", f"{p}.ambiente", ate="J", maximo=80, rotulo="Ambiente")
    e1, e2 = r0 + 3, r0 + 12
    cabs(ws, e1 - 1, {"A": ("Criatura (preencha)", "B"), "C": "Quantidade", "D": "Fraqueza nesta cena 1",
                      "E": "Fraqueza nesta cena 2", "F": "Fraqueza nesta cena 3", "G": "Fraqueza nesta cena 4",
                      "H": "Tipo", "I": "PV", "J": "Custo", "K": ("Aviso", "L")})
    cabs(ws, e2 - 1, {"A": "Criatura", "B": "Faixa", "C": ("Fraquezas efetivas", "F"), "G": "Resistência",
                      "H": "Ações agressivas", "I": ("Execução", "J"), "K": ("Aviso", "L")})
    a = lambda c, r: f"${CAUX[c]}${r}"  # noqa: E731
    rng = lambda c: f"${CAUX[c]}${e1}:${CAUX[c]}${e1 + NL - 1}"  # noqa: E731
    for j in range(1, NL + 1):
        r, r2 = e1 + j - 1, e2 + j - 1
        pj = f"{p}.{j}"
        ent(ws, f"A{r}", f"{pj}.criatura", tipo="lista", fonte=T("inimigos.cat.nome"), ate="B", rotulo="Criatura",
            opcoes=[f["nome"] for f in D.bestiario()])
        ent(ws, f"C{r}", f"{pj}.qtd", tipo="inteiro", minimo=0, maximo=10, rotulo="Quantidade", centro=True,
            amostra=2)
        for k, col in enumerate("DEFG", start=1):
            ent(ws, f"{col}{r}", f"{pj}.f{k}", tipo="lista", fonte="lista.elementos", rotulo=f"Fraqueza {k}",
                centro=True)
        CR, QT = T(f"{pj}.criatura"), T(f"{pj}.qtd")
        idx = a("idx", r)
        put = lambda c, f, rr=r, pj=pj: N.aux(ws, f"{CAUX[c]}{rr}", f, nome=f"{pj}.aux.{c}")  # noqa: E731
        put("idx", f'=IF(LEN({CR})=0,"",IFERROR(MATCH({CR},{T("inimigos.cat.nome")},0),""))')
        put("q", f'=IF(ISNUMBER({idx}),IF(ISNUMBER({QT}),MIN(10,MAX(0,INT({QT}))),1),0)')
        cena = " ,".join([])
        F = [T(f"{pj}.f{k}") for k in range(1, 5)]
        algum = "OR(" + ",".join(f"LEN({x})>0" for x in F) + ")"
        for k in range(1, 5):
            put(f"w{k}", f'=IF({a("q", r)}=0,"",IF({algum},{F[k - 1]}&"",{cat(f"f{k}", idx)}))')
        put("res", f'=IF({a("q", r)}=0,"",{cat("res", idx)})')
        put("tipo", f'=IF(ISNUMBER({idx}),{cat("tipo", idx)},"")')
        put("fidx", f'=IF(ISNUMBER({idx}),{cat("faixa_idx", idx)},"")')
        put("custo", f'=IF({a("q", r)}=0,0,{cat("custo", idx)}*{a("q", r)})')
        put("acoes", f'=IF({a("q", r)}=0,0,{cat("acoes", idx)}*{a("q", r)})')
        put("cum", f'={a("q", r)}' if j == 1 else f'={a("cum", r - 1)}+{a("q", r)}')
        put("resbad", f'=IF(AND({a("q", r)}>0,LEN({a("res", r)})>0),IF(COUNTIF({T("grupo.col.elemento")},'
                      f'{a("res", r)})>=2,1,0),0)')
        put("nome", f'=IF(ISNUMBER({idx}),{cat("nome", idx)},"")')
        put("solo", f'=IF(AND({a("q", r)}>0,OR({a("nome", r)}="Pretor Vazio-Nove",'
                    f'{a("nome", r)}="O Dramaturgo de Mil Faces")),1,0)')
        put("germe", f'=IF(AND({a("q", r)}>0,{a("nome", r)}="O Germe de Pavor"),1,0)')
        put("fdif", f'=IF(AND({a("q", r)}>0,{a("fidx", r)}<>{T("encontros.fidx")}),1,0)')
        put("fidxq", f'=IF({a("q", r)}>0,{a("fidx", r)},0)')
        put("peso", f'={a("q", r)}*IF({a("nome", r)}="Escória de Stellaron",1.5,1)')
        put("nesc", "=" + "+".join(f"IF(LEN({x})>0,1,0)" for x in F))
        cal(ws, f"H{r}", f'=IF(ISNUMBER({idx}),{cat("tipo", idx)},"")', nome=f"{pj}.tipo", centro=True, regra=True)
        cal(ws, f"I{r}", f'=IF(ISNUMBER({idx}),{cat("pv", idx)},"")', nome=f"{pj}.pv", centro=True, regra=True)
        cal(ws, f"J{r}", f'=IF(ISNUMBER({idx}),{a("custo", r)},"")', nome=f"{pj}.custo", centro=True, regra=True)
        nf_cat = "+".join(f'IF(LEN({cat(f"f{k}", idx)})>0,1,0)' for k in range(1, 5))
        rep = "+".join(f'IF(AND(LEN({F[x]})>0,{F[x]}={F[y]}),1,0)' for x in range(4) for y in range(x + 1, 4))
        av(ws, f"K{r}", f"{pj}.aviso1",
           f'=IF(LEN({CR})=0,"",IF(NOT(ISNUMBER({idx})),"Criatura fora da lista (Inimigos e Bestiário)",'
           f'IF(AND(ISNUMBER({QT}),OR({QT}<0,{QT}>10)),"Quantidade fora de 0 a 10: usando o limite",'
           f'IF(({rep})>0,"Fraqueza repetida nesta cena",IF(AND({a("nesc", r)}>0,{a("nesc", r)}<>({nf_cat})),'
           f'"O nº de Fraquezas é regra (28.2 regra 7): troque, não acrescente nem tire",'
           f'IF(AND(LEN({a("res", r)})>0,COUNTIF({a("w1", r)}:{a("w4", r)},{a("res", r)})>0),'
           f'"Fraqueza igual à Resistência da ficha",""))))))', ate="L")
        cal(ws, f"A{r2}", f'=IF(LEN({CR})>0,{CR},"{j} · (vazia)")', nome=f"{pj}.rot2")
        cal(ws, f"B{r2}", f'=IF(ISNUMBER({idx}),{cat("faixa", idx)},"")', nome=f"{pj}.faixa", centro=True, regra=True)
        w = [a(f"w{k}", r) for k in range(1, 5)]
        cal(ws, f"C{r2}", f'={w[0]}' + "".join(f'&IF(LEN({x})>0,", "&{x},"")' for x in w[1:]),
            nome=f"{pj}.fraq", ate="F", regra=True)
        cal(ws, f"G{r2}", f'=IF(ISNUMBER({idx}),IF(LEN({a("res", r)})>0,{a("res", r)},"—"),"")', nome=f"{pj}.res",
            centro=True, regra=True)
        cal(ws, f"H{r2}", f'=IF(ISNUMBER({idx}),{a("acoes", r)},"")', nome=f"{pj}.acoes", centro=True, regra=True)
        cal(ws, f"I{r2}", f'=IF(ISNUMBER({idx}),IF({cat("execucao", idx)}="Pode","Pode Executar (ser racional)",'
                          f'IF({cat("execucao", idx)}="Não","Não Executa","Execução não declarada")),"")',
            nome=f"{pj}.execucao", ate="J")
        av(ws, f"K{r2}", f"{pj}.aviso2",
           f'=IF({a("q", r)}=0,"",IF({a("fdif", r)}=1,"Faixa diferente da do grupo (28.4 passo 1: a faixa do '
           f'inimigo é a do grupo)",IF({a("resbad", r)}=1,"Resistência no Elemento de dois personagens (27.5)","")))',
           ate="L")
    for c in ("nome", "q", "cum", "w1", "w2", "w3", "w4", "idx"):
        N.reg(f"{p}.col.{c}", ws, f"{CAUX[c]}{e1}:{CAUX[c]}{e1 + NL - 1}")
    N.subtabela(ws, f"{X}.E1", [e1 - 1], "A:L", NL)
    N.subtabela(ws, f"{X}.E2", [e2 - 1], "A:L", NL)
    rl = e2 + NL
    _leitura(ws, X, p, rl, rng)


def _leitura(ws, X, p, rl, rng):
    ORC, DPC = T("encontros.orc"), T("encontros.dpc")
    rot(ws, f"A{rl}", "Custo total", negrito=True)
    cal(ws, f"B{rl}", f'=SUM({rng("custo")})', nome=f"{p}.custo", centro=True, regra=True)
    rot(ws, f"C{rl}", "% do orçamento", negrito=True)
    # D1: arredondamento só com INT. Meio para cima em aritmética inteira (custo e orçamento/DPC são inteiros):
    # INT((2·x·b + b) / (2·b)) = x arredondado (revisão da Fase 1, F7; mesmo valor do ROUND de antes)
    C_ = T(f"{p}.custo")
    cal(ws, f"D{rl}", f'=IF({ORC}>0,INT((200*{C_}+{ORC})/(2*{ORC})),"")', nome=f"{p}.pct", centro=True, regra=True)
    rot(ws, f"E{rl}", "Ciclos estimados", negrito=True)
    cal(ws, f"F{rl}", f'=IF(OR({C_}=0,{DPC}=0),"",INT((20*{C_}+20*IF({T(f"{p}.contrato_n")}<3,1,0)*{DPC}+{DPC})'
                      f'/(2*{DPC}))/10)', nome=f"{p}.ciclos", centro=True, regra=True)
    pct = f'({T(f"{p}.custo")}/{ORC})'
    cal(ws, f"G{rl}", f'=IF({T(f"{p}.custo")}=0,"",IF({pct}<=0.6,"Cena de passagem — cerca de 2 Ciclos (27.4)",'
                      f'IF({pct}<=1.15,"Encontro típico — 3 a 5 Ciclos (27.4)",IF({pct}<=1.6,"Pesado",'
                      f'"Dois orçamentos num só encontro: passa de 6 Ciclos (27.4)"))))', nome=f"{p}.dificuldade",
        ate="J", regra=True)
    cal(ws, f"K{rl}", f'=IF({T(f"{p}.custo")}=0,"","Ciclos e leitura: {N.ROTULO_SUGESTAO} (H6, H7)")',
        nome=f"{p}.h6", ate="L")
    sugestao_formula(f"{p}.h6", "H6", [f"G{rl}"])
    N.MAPA.sugestoes.append({"h": "H7", "rotulo": N.MapaMestre.ref("Encontros", f"K{rl}"), "nome": f"{p}.h6",
                             "na_formula": True, "celulas": [N.MapaMestre.ref("Encontros", f"F{rl}")]})
    r = rl + 1
    nb = f'SUMIF({rng("tipo")},"Boss",{rng("q")})'
    ne = f'SUMIF({rng("tipo")},"Elite",{rng("q")})'
    nc = f'SUMIF({rng("tipo")},"Comum",{rng("peso")})'   # Escória = 1,5 Comum (28.10)
    rot(ws, f"A{r}", "Composição", negrito=True)
    comps = D.composicoes()
    s = '""'
    for c in reversed(comps):
        s = (f'IF(AND({nb}={c["boss"]},{ne}={c["elite"]},{nc}={c["comum"]}),{q(c["composicao"] + " — " + c["sensacao"] + " (" + c["duracao"] + ", 27.4)")},{s})')
    cal(ws, f"B{r}", f'=IF({T(f"{p}.custo")}=0,"",IF({s}="",{nb}&" Boss, "&{ne}&" Elite, "&{nc}&" Comum: '
                     f'não é uma das quatro composições de 27.4",{s}))', nome=f"{p}.composicao", ate="L", regra=True)
    N.pior(ws, f"B{r}", max((c["composicao"] + " — " + c["sensacao"] + " (" + c["duracao"] + ", 27.4)" for c in comps),
                            key=len))
    r += 1
    cabs(ws, r, {"A": "Contrato (27.5)", **{L(2 + k): e for k, e in enumerate(ELEM)}, "I": "Cobertos",
                 "J": "Contrato", "K": ("Aviso", "L")})
    r += 1
    rot(ws, f"A{r}", "Fraqueza na cena?", negrito=True)
    reg_w = f"${CAUX['w1']}${rl - 2 * NL - 1 - 0}:${CAUX['w4']}${rl - NL - 2}"
    e1 = rl - 2 * NL - 1
    reg_w = f"${CAUX['w1']}${e1}:${CAUX['w4']}${e1 + NL - 1}"
    for k, e in enumerate(ELEM):
        cal(ws, f"{L(2 + k)}{r}", f'=IF({T(f"grupo.tem.{k + 1}")}="Sim",IF(COUNTIF({reg_w},{q(e)})>0,"Sim","Não"),"—")',
            nome=f"{p}.contrato.{k + 1}", centro=True, regra=True)
    cal(ws, f"I{r}", f'=COUNTIF(B{r}:H{r},"Sim")', nome=f"{p}.contrato_n", centro=True, regra=True)
    cal(ws, f"J{r}", f'=IF({T(f"{p}.custo")}=0,"",IF({T(f"{p}.contrato_n")}>=3,"Cumprido","Não cumprido"))',
        nome=f"{p}.contrato", centro=True, regra=True)
    av(ws, f"K{r}", f"{p}.aviso.contrato",
       f'=IF(OR({T(f"{p}.custo")}=0,{T(f"{p}.contrato_n")}>=3),"","Contrato não cumprido: encontro deliberadamente '
       f'mais duro, cerca de 1 Ciclo a mais (27.5)")', ate="L")
    r += 1
    rot(ws, f"A{r}", "Se não cumprir", negrito=True)
    cal(ws, f"B{r}", f'=IF(OR({T(f"{p}.custo")}=0,{T(f"{p}.contrato_n")}>=3),"","Três saídas (27.5): distribua as '
                     f'Fraquezas entre vários inimigos; deixe o grupo criar a Fraqueza (Implante de Fraqueza, 08); '
                     f'aceite o Ciclo extra e avise a mesa.")', nome=f"{p}.saidas", ate="L")
    r += 1
    rot(ws, f"A{r}", "Regra irmã e DT", negrito=True)
    cal(ws, f"B{r}", f'=IF({T(f"{p}.custo")}=0,"",IF(SUM({rng("resbad")})>0,"Há Resistência no Elemento de dois '
                     f'personagens: troque-a (27.5)","Nenhuma Resistência aponta para o Elemento de dois personagens '
                     f'(27.5)"))', nome=f"{p}.irma", ate="F", regra=True)
    cal(ws, f"G{r}", f'=IF({T(f"{p}.custo")}=0,"","DT para descobrir Fraqueza: "&INDEX({dcol("dt_fraqueza", "DT")},'
                     f'MAX(1,MAX({rng("fidxq")})))&" (20.2, faixa do mais forte)"&IF(COUNTIF({T("grupo.col.raca")},'
                     f'"Intellitron")>0,"; Intellitron: Vantagem e 2 por sucesso",""))', nome=f"{p}.dt", ate="L",
        regra=True)
    N.pior(ws, f"G{r}", "DT para descobrir Fraqueza: 17 (20.2, faixa do mais forte); Intellitron: Vantagem e 2 por "
                        "sucesso")
    r += 1
    rot(ws, f"A{r}", "Avisos de ficha", negrito=True)
    ntot = f'SUM({rng("q")})'
    av(ws, f"B{r}", f"{p}.aviso.ficha",
       f'=IF(AND(SUM({rng("solo")})>0,{ntot}>1),"Pretor Vazio-Nove e Dramaturgo: monte sozinho, os reforços são o que '
       f'ele tem em vez de acompanhantes (28.7, 28.8)",IF(AND(SUM({rng("germe")})>0,{nc}>0),"O Germe de Pavor vem '
       f'sozinho: o Parto falso traz os Comuns (28.11)",""))', ate="L")


def _aleatorio(ws):
    r0 = ALE
    titulo(ws, r0, "Encontro aleatório (G = 100): por ambiente e faixa, com a troca de Fraqueza sugerida")
    cabs(ws, r0 + 1, {"A": "Rolagem nº", "B": ("Ambiente", "D"), "E": "Faixa", "F": ("Composição", "G"),
                      "H": ("Rolagem efetiva", "I"), "K": ("Aviso", "L")})
    ri = r0 + 2
    ent(ws, f"A{ri}", "encontros.ale.rolagem", tipo="inteiro", minimo=1, maximo=1000000, rotulo="Rolagem nº",
        centro=True, amostra=3)
    ent(ws, f"B{ri}", "encontros.ale.ambiente", tipo="lista", fonte="lista.ambiente_aleatorio", ate="D",
        rotulo="Ambiente")
    ent(ws, f"E{ri}", "encontros.ale.faixa", tipo="lista", fonte="lista.faixas", rotulo="Faixa", centro=True)
    ent(ws, f"F{ri}", "encontros.ale.composicao", tipo="lista", fonte="lista.composicoes", ate="G",
        rotulo="Composição")
    cal(ws, f"H{ri}", S.rolagem_efetiva(T("encontros.ale.rolagem")), nome="encontros.ale.rolagem_ef", ate="I",
        centro=True)
    av(ws, f"K{ri}", "encontros.ale.aviso", S.aviso_rolagem(T("encontros.ale.rolagem")), ate="L")
    SEM, ROL = T("inicio.semente_ef"), T("encontros.ale.rolagem_ef")
    fx = dcol("faixas", "Faixa")
    # parâmetros efetivos e sorteio (colunas ocultas N…, linhas da seção)
    ra = ri
    fa = N.faixa_da_lista(T("encontros.ale.faixa"))
    N.aux(ws, f"N{ra}", f'=IF(LEN({fa})>0,{fa},{T("campanha.faixa")})', nome="encontros.ale.faixa_ef")
    N.MAPA.geradores[str(G_ENC)] = {"nome": D.GERADORES[G_ENC]["nome"], "aba": "Encontros", "campos": {},
                                    "rolagem": "encontros.ale.rolagem_ef",
                                    "parametros": ["ambiente", "faixa", "composição", "bestiário (Dados)",
                                                   "tab.ambiente_por_faccao", "Elementos do grupo (H19)"]}
    xs = {}
    for c in range(1, 9):
        rr = r0 + 4 + c
        cp = S.Campo(ws, rr, CI("AH"), SEM, ROL, G_ENC, c, f"encontros.ale.c{c}",
                     lambda w, cel, f, nome: N.aux(w, cel, f, nome=nome))
        xs[c] = cp.xref
        N.MAPA.geradores[str(G_ENC)]["campos"][str(c)] = {k: N.MapaMestre.ref("Encontros", getattr(cp, k))
                                                          for k in ("u", "y", "x")}
    comp_lista = N.dlista("composicoes")
    CP = T("encontros.ale.composicao")
    N.aux(ws, f"O{ra}", f'=IF(AND(COUNTIF({comp_lista},{CP})>0,{CP}<>"Sortear"),MATCH({CP},{comp_lista},0)-1,'
                        f'{S.escolha(xs[1], 4)})', nome="encontros.ale.comp")
    COMP, FXE = T("encontros.ale.comp"), T("encontros.ale.faixa_ef")
    # candidatos: 32 linhas do bestiário (linhas 11..42, colunas AK..AR)
    blo = N.MAPA.blocos["dados.bestiario"]
    dl = lambda col, i: f"'Dados'!${blo['colunas'][col]}${blo['primeira_linha'] + i - 1}"  # noqa: E731
    AMB = T("encontros.ale.ambiente")
    fac, amb = T("tab.ambiente_por_faccao.valores"), T("tab.ambiente_por_faccao.ambientes")
    cols = {"amb": "AK", "aC": "AL", "aE": "AM", "aB": "AN", "fC": "AO", "fE": "AP", "fB": "AQ"}
    for i in range(1, 33):
        rr = 10 + i
        ok_amb = (f'IF(OR(LEN({AMB})=0,{AMB}="Qualquer"),1,IF(COUNTIFS({fac},{dl("Facção ou origem", i)},{amb},{AMB})+'
                  f'IF(LEN({dl("Origem 2", i)})=0,0,COUNTIFS({fac},{dl("Origem 2", i)},{amb},{AMB}))>0,1,0))')
        N.aux(ws, f"AK{rr}", "=" + ok_amb, nome=f"encontros.ale.amb{i}")
        for t, tipo in (("C", "Comum"), ("E", "Elite"), ("B", "Boss")):
            base = f'IF(AND({dl("Tipo", i)}="{tipo}",{dl("Faixa", i)}={FXE}),1,0)'
            for pre, cond in (("a", f"*$AK${rr}"), ("f", "")):
                col = cols[pre + t]
                prev = "0" if i == 1 else f"${col}${rr - 1}"
                N.aux(ws, f"{col}{rr}", f"={prev}+{base}{cond}", nome=f"encontros.ale.{pre}{t}{i}")
    rng = {k: f"${v}$11:${v}$42" for k, v in cols.items()}
    # saída: 7 vagas (linhas da tabela), com a linha de saída nas colunas de E1
    rs = r0 + 5
    cabs(ws, rs - 1, {"A": ("Criatura", "B"), "C": "Quantidade", "D": "Fraqueza nesta cena 1",
                      "E": "Fraqueza nesta cena 2", "F": "Fraqueza nesta cena 3", "G": "Fraqueza nesta cena 4",
                      "H": "Tipo", "I": "PV", "J": "Custo", "K": ("Aviso", "L")})
    ordem = []
    for k in range(1, 8):
        r = rs + k - 1
        pk = f"encontros.ale.v{k}"
        tipo = (f'IF({COMP}=1,IF({k}=1,"Boss",IF({k}=2,"Comum","")),IF({COMP}=2,IF({k}=1,"Elite",IF({k}<=5,"Comum","")),'
                f'IF({COMP}=3,IF({k}<=3,"Elite",""),"Comum")))')
        N.aux(ws, f"N{r}", "=" + tipo, nome=f"{pk}.tipo")
        TP = f"$N${r}"
        na = f'IF({TP}="Comum",INDEX({rng["aC"]},32),IF({TP}="Elite",INDEX({rng["aE"]},32),INDEX({rng["aB"]},32)))'
        nfx = f'IF({TP}="Comum",INDEX({rng["fC"]},32),IF({TP}="Elite",INDEX({rng["fE"]},32),INDEX({rng["fB"]},32)))'
        N.aux(ws, f"O{r}", f'=IF({TP}="","",{na})', nome=f"{pk}.na")
        N.aux(ws, f"P{r}", f'=IF({TP}="","",IF($O${r}>0,$O${r},{nfx}))', nome=f"{pk}.n")
        N.aux(ws, f"Q{r}", f'=IF({TP}="","",{S.escolha(xs[k + 1], f"$P${r}")})', nome=f"{pk}.j")
        J = f"$Q${r}"
        m = lambda t: (f'IF($O${r}>0,MATCH({J},{rng["a" + t]},0),MATCH({J},{rng["f" + t]},0))')  # noqa: E731
        N.aux(ws, f"R{r}", f'=IF({TP}="","",IFERROR(IF({TP}="Comum",{m("C")},IF({TP}="Elite",{m("E")},{m("B")})),""))',
              nome=f"{pk}.linha")
        LN = f"$R${r}"
        bx = lambda col: f'INDEX({dcol("bestiario", col)},{LN})'  # noqa: E731
        N.aux(ws, f"S{r}", f'=IF(ISNUMBER({LN}),{bx("Nome")},"")', nome=f"{pk}.nome")
        cal(ws, f"A{r}", f"=$S${r}", nome=f"{pk}.criatura", ate="B")
        cal(ws, f"C{r}", f'=IF(ISNUMBER({LN}),1,"")', nome=f"{pk}.qtd", centro=True)
        cal(ws, f"H{r}", f'=IF(ISNUMBER({LN}),{bx("Tipo")},"")', nome=f"{pk}.tipo_v", centro=True, regra=True)
        cal(ws, f"I{r}", f'=IF(ISNUMBER({LN}),{bx("PV")},"")', nome=f"{pk}.pv", centro=True, regra=True)
        cal(ws, f"J{r}", f'=IF(ISNUMBER({LN}),{bx("Custo no orçamento")},"")', nome=f"{pk}.custo", centro=True,
            regra=True)
        av(ws, f"K{r}", f"{pk}.aviso", f'=IF(AND(ISNUMBER({LN}),$O${r}=0),"Sem criatura deste tipo no ambiente: '
                                       f'qualquer ambiente da faixa","")', ate="L")
        ordem.append((r, LN))
    N.reg("encontros.R.col.nome", ws, f"S{rs}:S{rs + 7}")
    N.subtabela(ws, "aleatorio", [rs - 1], "A:L", 7)
    # H19: 28 posições (vaga × Fraqueza), colunas AT…AZ nas linhas 11..38; faltantes em BA..BC (linhas 11..17)
    grp = T("grupo.col.elemento")
    for e in range(1, 8):
        rr = 10 + e
        el = q(ELEM[e - 1])
        N.aux(ws, f"BA{rr}", f'=IF(AND({T(f"grupo.tem.{e}")}="Sim",COUNTIF($AT$11:$AT$38,{el})=0),1,0)',
              nome=f"encontros.h19.miss{e}")
        N.aux(ws, f"BB{rr}", f"=$BA${rr}" if e == 1 else f"=$BB${rr - 1}+$BA${rr}", nome=f"encontros.h19.cum{e}")
        N.aux(ws, f"BC{rr}", f'=IFERROR(INDEX({dcol("elementos", "Elemento")},MATCH({e},$BB$11:$BB$17,0)),"")',
              nome=f"encontros.h19.M{e}")
        N.aux(ws, f"BD{rr}", f'=IF(AND({T(f"grupo.tem.{e}")}="Sim",COUNTIF($AT$11:$AT$38,{el})>0),1,0)',
              nome=f"encontros.h19.cob{e}")
    N.aux(ws, "BE11", "=SUM($BD$11:$BD$17)", nome="encontros.h19.c0")
    N.aux(ws, "BE12", "=MIN(MAX(0,3-$BE$11),$BB$17)", nome="encontros.h19.need")
    for p_ in range(1, 29):
        rr = 10 + p_
        k, j = (p_ - 1) // 4 + 1, (p_ - 1) % 4 + 1
        r_out, LN = ordem[k - 1]
        N.aux(ws, f"AT{rr}", f'=IF(ISNUMBER({LN}),INDEX({dcol("bestiario", f"Fraqueza {j}")},{LN})&"","")',
              nome=f"encontros.h19.v{p_}")
        N.aux(ws, f"AU{rr}", f'=IF(ISNUMBER({LN}),INDEX({dcol("bestiario", "Resistência")},{LN})&"","")',
              nome=f"encontros.h19.r{p_}")
        N.aux(ws, f"AV{rr}", f'=IF(LEN($AT${rr})=0,0,IF(COUNTIF({grp},$AT${rr})>0,0,1))', nome=f"encontros.h19.s{p_}")
        prev = "0" if p_ == 1 else f"$AW${rr - 1}"
        N.aux(ws, f"AW{rr}", f'={prev}+IF(AND($AV${rr}=1,{prev}<$BE$12),IF(INDEX($BC$11:$BC$17,{prev}+1)<>$AU${rr},1,0),0)',
              nome=f"encontros.h19.k{p_}")
        N.aux(ws, f"AX{rr}", f'=IF($AW${rr}>{prev},INDEX($BC$11:$BC$17,$AW${rr}),$AT${rr})', nome=f"encontros.h19.n{p_}")
        N.aux(ws, f"AY{rr}", f'=IF($AW${rr}>{prev},$S${r_out}&": "&$AT${rr}&" → "&$AX${rr}&"; ","")',
              nome=f"encontros.h19.t{p_}")
        col = "DEFG"[j - 1]
        cal(ws, f"{col}{r_out}", f"=$AX${rr}", nome=f"encontros.ale.v{k}.f{j}", centro=True, regra=True)
    for k in range(1, 9):
        rr = rs + k - 1
        if k <= 7:
            for j in range(1, 5):
                N.aux(ws, f"{L(CI('U') + j - 1)}{rr}", f"={'DEFG'[j - 1]}{rr}", nome=f"encontros.ale.v{k}.w{j}")
            N.aux(ws, f"Y{rr}", f'=IF(LEN($S${rr})>0,1,0)' if k == 1 else f'=$Y${rr - 1}+IF(LEN($S${rr})>0,1,0)',
                  nome=f"encontros.ale.v{k}.cum")
    for j in range(1, 5):
        c = L(CI("U") + j - 1)
        N.reg(f"encontros.R.col.w{j}", ws, f"{c}{rs}:{c}{rs + 7}")
    N.reg("encontros.R.col.cum", ws, f"Y{rs}:Y{rs + 7}")
    r = rs + 8
    rot(ws, f"A{r}", "Trocas sugeridas", negrito=True)
    cal(ws, f"B{r}", '=IF(ISNUMBER($R$' + str(rs) + '),IF(LEN(' + "&".join(f"$AY${10 + p_}" for p_ in range(1, 29)) +
        ')=0,"Nenhuma troca necessária",' + "&".join(f"$AY${10 + p_}" for p_ in range(1, 29)) + '),"")',
        nome="encontros.ale.trocas", ate="J")
    N.pior(ws, f"B{r}", "Larva Fuliginosa: Vento → Quântico; Casco Oco: Físico → Imaginário; "
                        "Sargento de Trincheira: Raio → Gelo; ")
    cal(ws, f"K{r}", f'="{N.ROTULO_SUGESTAO} (H19)"', nome="encontros.ale.h19", ate="L")
    sugestao_formula("encontros.ale.h19", "H19", [f"B{r}"])
    r += 1
    rot(ws, f"A{r}", "Leitura", negrito=True)
    cal(ws, f"B{r}", f'=IF(ISNUMBER($R${rs}),"Custo "&SUM(J{rs}:J{rs + 6})&" de "&{T("encontros.orc")}&'
                     f'" · contrato: "&($BE$11+$AW$38)&" Elemento(s) do grupo como Fraqueza"&IF($BE$11+$AW$38>=3,'
                     f'" (cumprido)"," (não cumprido)")&" · composição: "&INDEX({comp_lista},{COMP}+1),"")',
        nome="encontros.ale.leitura", ate="J", regra=True)
    N.reg("encontros.ale.contrato_n", ws, "BE13")
    N.aux(ws, "BE13", "=$BE$11+$AW$38")
    cal(ws, f"K{r}", f'="Composição sorteada com peso igual: {N.ROTULO_SUGESTAO} (H11)"', nome="encontros.ale.h11",
        ate="L")
    sugestao_formula("encontros.ale.h11", "H11", [])
    rot(ws, f"A{r + 1}", "Copie A:G da linha de saída e cole como valores (Colar especial → Somente valores) em A, B "
                         "ou C: as colunas estão na mesma ordem (D6).", ate="L", italico=True)
    r += 3
    titulo(ws, r, "O dia de jogo e as recompensas")
    cal(ws, f"A{r + 1}", f'="Attrition de referência (27.7), faixa "&{T("encontros.faixa")}&": o grupo termina um '
                         f'combate típico com "&INDEX({dcol("attrition", "O grupo termina com")},{T("encontros.fidx")})'
                         f'&" dos PV. Dois combates por dia é um dia tranquilo, três é um dia de verdade, quatro é '
                         f'emergência."', nome="encontros.attrition", ate="L", regra=True)
    rot(ws, f"A{r + 2}", "Progressão por marco narrativo; não existe experiência por inimigo derrotado (26.1). "
                         "Recompensas: aba Recompensas.", ate="L", italico=True)
