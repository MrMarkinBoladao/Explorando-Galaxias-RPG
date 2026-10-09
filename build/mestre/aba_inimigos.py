# -*- coding: utf-8 -*-
"""
Aba Inimigos — Criador de Inimigos (R1, design §6.7.1–6.7.2).

12 linhas em sub-tabelas I1, I1b, I2, I3, I4 e I5 (fases). Modos: "Faixa do livro" (copia a linha de 28.3,
28.4 passo 3), "Por nível — Sugestão" (H1: só o PV é interpolado entre os níveis de referência 3/7/11/15/19
de 29.1; o resto é a âncora da faixa do nível) e "Ajustar do bestiário" (âncoras da faixa nova; Fraquezas,
Resistência, Execução, fases e ações da base). Fraquezas vazias = sugeridas (G = 110, H12).
Colunas ocultas à direita de L: o CATÁLOGO (12 da campanha + 32 do bestiário) que alimenta Encontros e
Combate, e as auxiliares do Criador e do sorteio. Ações e ficha detalhada: aba_inimigos_acoes.py.
"""

from openpyxl.utils import get_column_letter as L, column_index_from_string as CI

import mestre_dados as D
from mestre import nucleo as N
from mestre import sorteio as S
from mestre.nucleo import T, q, ent, cal, av, rot, cabs, titulo, dcol, sugestao, sugestao_formula

NI = 12
NB = 32
NCAT = NI + NB
ELEM = D.ELEMENTOS
G_FRAQ = 110

I1, I1B, I2, I3, I4 = 11, 26, 42, 57, 72         # primeira linha de dados de cada sub-tabela
I5A, I5B = 88, 101                              # I5 em dois blocos de 12

CAT0 = 11                                       # catálogo: linhas 11..54, colunas a partir de N
CATC = ["nome", "tipo", "faixa", "pv", "defesa", "rd", "ten", "vel", "ataque", "dano_e", "dano_m", "dt", "tr",
        "f1", "f2", "f3", "f4", "res", "execucao", "fases", "acoes", "custo", "firmeza", "lim2", "lim3",
        "p2f1", "p2f2", "p2f3", "p2f4", "ten2", "p3f1", "p3f2", "p3f3", "p3f4", "ten3",
        "esp1", "rec1", "esp2", "rec2", "esp3", "rec3", "origem", "origem2", "ef", "faixa_idx", "fraq_txt",
        "origem_tipo"]
COLCAT = {c: L(N.PRIMEIRA_AUX + k) for k, c in enumerate(CATC)}
AUX0 = CI("BK")
AUXC = ["modo", "aj", "brow", "tipo", "tipo_idx", "nivel", "faixa", "fidx", "chave", "k", "pv", "fases", "nsug",
        "vazias", "w1", "w2", "w3", "w4", "res", "sug1", "sug2", "sug3", "sug4", "ten_orig", "pv_orig",
        "esp_e", "esp_m", "com_e", "com_m"]
AUXCOL = {c: L(AUX0 + k) for k, c in enumerate(AUXC)}
UYX0 = AUX0 + len(AUXC)                         # 7 × (u, y, x)
CHV0 = UYX0 + 21                                # 7 chaves contíguas (H12)


def _r(i):
    return I1 + i - 1


def A(nome, i):
    return f"${AUXCOL[nome]}${_r(i)}"


def ACOL(nome):
    return f"${AUXCOL[nome]}${I1}:${AUXCOL[nome]}${I1 + NI - 1}"


def anc(coluna, chave):
    return f'IFERROR(INDEX({dcol("ancoras", coluna)},MATCH({chave},{dcol("ancoras", "Chave")},0)),"")'


TEXTO_BES = {"Fraqueza 1", "Fraqueza 2", "Fraqueza 3", "Fraqueza 4", "Resistência", "Execução", "Origem 2",
             "Especial 1", "Especial 2", "Especial 3", "Facção ou origem",
             "Na Fila (resto)"}


def bes(coluna, linha):
    """Coluna do bestiário na linha dada; texto possivelmente vazio leva &"" (INDEX de vazio dá 0)."""
    s = '&""' if coluna in TEXTO_BES else ""
    return f'IFERROR(INDEX({dcol("bestiario", coluna)},{linha}){s},"")'


def rotulo(i):
    return f'=IF(LEN({T(f"inimigos.{i}.nome")})>0,"{i} · "&{T(f"inimigos.{i}.nome")},"{i} · (vazio)")'


def montar(wb):
    ws = wb["Inimigos"]
    titulo(ws, 5, "Criador de Inimigos — uma linha por inimigo da campanha (28.1, 28.3, 28.4)")
    rot(ws, "A6", "Modo vazio = Faixa do livro; Faixa vazia = faixa do grupo; Tipo vazio = Comum (no modo Ajustar, "
                  "o da base). A tabela já alimenta as listas de Encontros e Combate: não precisa copiar nada.",
        ate="L", italico=True)
    rot(ws, "A7", "Rolagem nº (Fraquezas sugeridas)", negrito=True)
    ent(ws, "B7", "inimigos.rolagem", tipo="inteiro", minimo=1, maximo=1000000, rotulo="Rolagem nº", centro=True,
        amostra=7)
    cal(ws, "C7", S.rolagem_efetiva(T("inimigos.rolagem")), nome="inimigos.rolagem_ef", centro=True)
    rot(ws, "D7", "Some 1 para sortear outra ordem de Fraquezas sugeridas.", ate="J", italico=True)
    av(ws, "K7", "inimigos.aviso.rolagem", S.aviso_rolagem(T("inimigos.rolagem")), ate="L")
    _i1(ws)
    _i1b(ws)
    _i2(ws)
    _aux(ws)
    _i3_i4(ws)
    _i5(ws)
    _catalogo(ws)
    from mestre import aba_inimigos_acoes
    aba_inimigos_acoes.montar(ws)


def _i1(ws):
    titulo(ws, I1 - 2, "I1 · Conceito (preencha)")
    cabs(ws, I1 - 1, {"A": "Nome", "B": ("Modo", "C"), "D": ("Base do bestiário (modo Ajustar)", "F"),
                      "G": "Faixa", "H": "Nível (modo Por nível)", "I": "Tipo", "J": "Fases (Boss, 1 a 3)",
                      "K": ("Aviso", "L")})
    for i in range(1, NI + 1):
        r, p = _r(i), f"inimigos.{i}"
        ent(ws, f"A{r}", f"{p}.nome", maximo=30, rotulo="Nome do inimigo")
        ent(ws, f"B{r}", f"{p}.modo", tipo="lista", fonte="lista.modos", ate="C", rotulo="Modo")
        ent(ws, f"D{r}", f"{p}.base", tipo="lista", fonte="lista.criaturas", ate="F", rotulo="Base do bestiário")
        ent(ws, f"G{r}", f"{p}.faixa", tipo="lista", fonte="lista.faixas", rotulo="Faixa", centro=True)
        ent(ws, f"H{r}", f"{p}.nivel", tipo="inteiro", minimo=1, maximo=20, rotulo="Nível", centro=True)
        ent(ws, f"I{r}", f"{p}.tipo", tipo="lista", fonte="lista.tipos", rotulo="Tipo", centro=True)
        ent(ws, f"J{r}", f"{p}.fases", tipo="inteiro", minimo=1, maximo=3, rotulo="Fases", centro=True, amostra=2)
        NOME = T(f"{p}.nome")
        av(ws, f"K{r}", f"{p}.aviso1",
           f'=IF(LEN({NOME})=0,IF(LEN({T(f"{p}.modo")}&{T(f"{p}.base")}&{T(f"{p}.tipo")})>0,'
           f'"Linha sem nome: o inimigo não entra nas listas",""),'
           f'IF(COUNTIF({T("inimigos.col.nome")},{NOME})>1,"Nome repetido na tabela",'
           f'IF(COUNTIF({dcol("bestiario", "Nome")},{NOME})>0,"Nome igual a uma criatura do bestiário: dê outro nome",'
           f'IF(AND({A("modo", i)}="Ajustar do bestiário",{A("aj", i)}=0),"Modo Ajustar sem base do bestiário válida",'
           f'IF(AND(LEN({T(f"{p}.fases")})>0,{A("tipo", i)}<>"Boss"),"Fases só valem para Boss (28.5)",'
           f'IF(AND(ISNUMBER({T(f"{p}.nivel")}),OR({T(f"{p}.nivel")}<1,{T(f"{p}.nivel")}>20)),'
           f'"Nível fora de 1 a 20: usando o limite",'
           f'IF(AND(LEN({T(f"{p}.tipo")})>0,COUNTIF({N.dlista("tipos")},{T(f"{p}.tipo")})=0),'
           f'"Tipo fora da lista: usando Comum","")))))))', ate="L")
    N.reg("inimigos.col.nome", ws, f"A{I1}:A{I1 + NI - 1}")
    N.reg("inimigos.col.base", ws, f"D{I1}:D{I1 + NI - 1}")
    N.subtabela(ws, "I1", [I1 - 1], "A:L", NI)


def _i1b(ws):
    titulo(ws, I1B - 2, "I1b · Origem e comportamento (preencha)")
    cabs(ws, I1B - 1, {"A": "Inimigo", "B": ("Facção ou origem", "D"), "E": "Elemento dos ataques",
                       "F": "Pode Executar? (ser racional)", "G": ("Comportamento na Fila (28.4 passo 6)", "J"),
                       "K": ("Aviso", "L")})
    for i in range(1, NI + 1):
        r, p = I1B + i - 1, f"inimigos.{i}"
        cal(ws, f"A{r}", rotulo(i), nome=f"{p}.rot1b")
        ent(ws, f"B{r}", f"{p}.faccao", tipo="lista", fonte="lista.faccoes_criador", ate="D", rotulo="Facção")
        ent(ws, f"E{r}", f"{p}.elemento", tipo="lista", fonte="lista.elementos", rotulo="Elemento", centro=True)
        ent(ws, f"F{r}", f"{p}.racional", tipo="lista", fonte="lista.sim_nao", rotulo="Pode Executar?", centro=True)
        ent(ws, f"G{r}", f"{p}.comportamento", ate="J", maximo=120, rotulo="Comportamento na Fila")
        av(ws, f"K{r}", f"{p}.aviso1b",
           f'=IF(AND(LEN({T(f"{p}.nome")})>0,LEN({T(f"{p}.racional")})=0,{A("aj", i)}=0),'
           f'"Diga se ele é ser racional (só ser racional Executa, 23.5)","")', ate="L")
    N.reg("inimigos.col.comp", ws, f"G{I1B}:G{I1B + NI - 1}")
    N.subtabela(ws, "I1b", [I1B - 1], "A:L", NI)


def _i2(ws):
    titulo(ws, I2 - 3, "I2 · Fraquezas e Resistência (preencha; vazias = sugeridas pela planilha)")
    sugestao(ws, f"A{I2 - 2}", "H12", "inimigos.h12.rotulo", ate="L",
             extra="Fraquezas vazias são sugeridas primeiro com os Elementos do grupo que ainda faltam no contrato "
                   "(27.5), depois em ordem sorteada; Comum recebe 2. Quantas é regra; quais, decisão sua (28.1).")
    cabs(ws, I2 - 1, {"A": "Inimigo", "B": "Fraqueza 1", "C": "Fraqueza 2", "D": "Fraqueza 3", "E": "Fraqueza 4",
                      "F": "Resistência", "G": ("Fraquezas efetivas", "J"), "K": ("Aviso", "L")})
    celulas = []
    for i in range(1, NI + 1):
        r, p = I2 + i - 1, f"inimigos.{i}"
        cal(ws, f"A{r}", rotulo(i), nome=f"{p}.rot2")
        for j, col in enumerate("BCDE", start=1):
            ent(ws, f"{col}{r}", f"{p}.f{j}", tipo="lista", fonte="lista.elementos", rotulo=f"Fraqueza {j}",
                centro=True)
        ent(ws, f"F{r}", f"{p}.res", tipo="lista", fonte="lista.elementos", rotulo="Resistência", centro=True)
        w = [A(f"w{j}", i) for j in range(1, 5)]
        corpo = w[0] + "".join(f'&IF(LEN({x})>0,", "&{x},"")' for x in w[1:])
        cal(ws, f"G{r}", f'=IF(LEN({T(f"{p}.nome")})=0,"",{corpo}&IF(AND({A("vazias", i)}=1,{A("aj", i)}=0),'
                         f'" (sugeridas)",IF(AND({A("vazias", i)}=1,{A("aj", i)}=1)," (da base)","")))',
            nome=f"{p}.fraq_txt", ate="J")
        celulas.append(f"G{r}")
        F = [T(f"{p}.f{j}") for j in range(1, 5)]
        nf = "+".join(f"IF(LEN({x})>0,1,0)" for x in F)
        rep = "+".join(f'IF(AND(LEN({F[a]})>0,{F[a]}={F[b]}),1,0)' for a in range(4) for b in range(a + 1, 4))
        av(ws, f"K{r}", f"{p}.aviso2",
           f'=IF(LEN({T(f"{p}.nome")})=0,"",IF(({rep})>0,"Fraqueza repetida",'
           f'IF(AND(LEN({A("res", i)})>0,COUNTIF({A("w1", i)}:{A("w4", i)},{A("res", i)})>0),'
           f'"Resistência igual a uma Fraqueza",'
           f'IF(AND({A("tipo", i)}="Comum",({nf})>2),"Comum tem 1 a 2 Fraquezas (20.2)",'
           f'IF(AND({A("tipo", i)}="Elite",({nf})>3),"Elite tem 3 Fraquezas (20.2)",'
           f'IF(AND(LEN({A("res", i)})>0,COUNTIF({T("grupo.col.elemento")},{A("res", i)})>=2),'
           f'"Nunca aponte uma Resistência para o Elemento de dois personagens (27.5)",""))))))', ate="L")
    N.MAPA.sugestoes[-1]["celulas"] = [N.MapaMestre.ref("Inimigos", c) for c in celulas]
    N.subtabela(ws, "I2", [I2 - 1], "A:L", NI)


def _aux(ws):
    """Auxiliares por linha: modo, base, tipo, faixa, PV (H1), Fraquezas efetivas e a ordem sugerida (H12)."""
    faixas = dcol("faixas", "Faixa")
    N.MAPA.geradores[str(G_FRAQ)] = {"nome": D.GERADORES[G_FRAQ]["nome"], "aba": "Inimigos", "campos": {},
                                     "rolagem": "inimigos.rolagem_ef",
                                     "parametros": ["tipo da linha", "Elementos do grupo",
                                                    "Fraquezas das linhas anteriores", "Resistência da linha"]}
    for i in range(1, NI + 1):
        r, p = _r(i), f"inimigos.{i}"
        MODO, BASE, TIPO, FX, NIV = (T(f"{p}.modo"), T(f"{p}.base"), T(f"{p}.tipo"), T(f"{p}.faixa"),
                                     T(f"{p}.nivel"))

        def put(nome, f):
            N.aux(ws, f"{AUXCOL[nome]}{r}", f, nome=f"{p}.aux.{nome}")
        put("modo", f'=IF(COUNTIF({N.dlista("modos")},{MODO})>0,{MODO},"Faixa do livro")')
        put("brow", f'=IFERROR(MATCH({BASE},{dcol("bestiario", "Nome")},0),"")')
        put("aj", f'=IF(AND({A("modo", i)}="Ajustar do bestiário",ISNUMBER({A("brow", i)})),1,0)')
        put("tipo", f'=IF(COUNTIF({N.dlista("tipos")},{TIPO})>0,{TIPO},IF({A("aj", i)}=1,'
                    f'{bes("Tipo", A("brow", i))},"Comum"))')
        put("tipo_idx", f'=MATCH({A("tipo", i)},{N.dlista("tipos")},0)')
        put("nivel", f'=IF(ISNUMBER({NIV}),MIN(20,MAX(1,INT({NIV}))),{T("campanha.nivel_ef")})')
        put("faixa", f'=IF({A("modo", i)}="Por nível — Sugestão",INDEX({faixas},INT(({A("nivel", i)}-1)/4)+1),'
                     f'IF(LEN({N.faixa_da_lista(FX)})>0,{N.faixa_da_lista(FX)},{T("campanha.faixa")}))')
        put("fidx", f'=MATCH({A("faixa", i)},{faixas},0)')
        put("chave", f'={A("faixa", i)}&"|"&{A("tipo", i)}')
        put("k", f'=MIN(4,MAX(1,INT(({A("nivel", i)}-3)/4)+1))')
        PVc = dcol("ancoras", "PV")
        ak = f'INDEX({PVc},({A("k", i)}-1)*3+{A("tipo_idx", i)})'
        ak1 = f'INDEX({PVc},{A("k", i)}*3+{A("tipo_idx", i)})'
        a1 = f'INDEX({PVc},{A("tipo_idx", i)})'
        a5 = f'INDEX({PVc},12+{A("tipo_idx", i)})'
        lv = A("nivel", i)
        h1 = f'INT(IF({lv}<=3,{a1},IF({lv}>=19,{a5},{ak}+({ak1}-{ak})*({lv}-(4*{A("k", i)}-1))/4)))'
        put("pv", f'=IF({A("modo", i)}="Por nível — Sugestão",{h1},{anc("PV", A("chave", i))})')
        put("fases", f'=IF({A("tipo", i)}<>"Boss",1,IF(AND(ISNUMBER({T(f"{p}.fases")}),{T(f"{p}.fases")}>=1,'
                     f'{T(f"{p}.fases")}<=3),INT({T(f"{p}.fases")}),IF({A("aj", i)}=1,'
                     f'MAX(1,{bes("Fases", A("brow", i))}),1)))')
        put("nsug", f'={anc("Fraquezas sugeridas", A("chave", i))}')
        F = [T(f"{p}.f{j}") for j in range(1, 5)]
        put("vazias", f'=IF(AND({",".join(f"LEN({x})=0" for x in F)}),1,0)')
        for j in range(1, 5):
            put(f"w{j}", f'=IF(LEN({T(f"{p}.nome")})=0,"",IF({A("vazias", i)}=0,{F[j - 1]}&"",IF({A("aj", i)}=1,'
                         f'{bes(f"Fraqueza {j}", A("brow", i))},IF({j}<={A("nsug", i)},{A(f"sug{j}", i)},""))))')
        put("res", f'=IF(LEN({T(f"{p}.res")})>0,{T(f"{p}.res")},IF({A("aj", i)}=1,'
                   f'{bes("Resistência", A("brow", i))},""))')
        put("ten_orig", f'=IF({A("aj", i)}=1,{bes("Tenacidade", A("brow", i))},"")')
        put("pv_orig", f'=IF({A("aj", i)}=1,{bes("PV", A("brow", i))},"")')
        put("esp_e", f'={anc("Dano especial 1,5×", A("chave", i))}')
        put("esp_m", f'={anc("Média do especial", A("chave", i))}')
        put("com_e", f'={anc("Dano por acerto", A("faixa", i) + "&" + q("|Comum"))}')
        put("com_m", f'={anc("Média do dano", A("faixa", i) + "&" + q("|Comum"))}')
        # H12: x por Elemento (G = 110, C = 10·i + e) e a chave de preferência (7 colunas contíguas)
        chaves = []
        for e in range(1, 8):
            campo = S.Campo(ws, r, UYX0 + (e - 1) * 3, T("inicio.semente_ef"), T("inimigos.rolagem_ef"), G_FRAQ,
                            10 * i + e, f"{p}.h12.e{e}", lambda w, cel, f, nome: N.aux(w, cel, f, nome=nome))
            N.MAPA.geradores[str(G_FRAQ)]["campos"][str(10 * i + e)] = {
                "u": N.MapaMestre.ref("Inimigos", campo.u), "y": N.MapaMestre.ref("Inimigos", campo.y),
                "x": N.MapaMestre.ref("Inimigos", campo.x)}
            elem = q(ELEM[e - 1])
            cob = "0" if i == 1 else f'COUNTIF(${AUXCOL["w1"]}${I1}:${AUXCOL["w4"]}${r - 1},{elem})'
            ch = L(CHV0 + e - 1)
            N.aux(ws, f"{ch}{r}", f'=IF({A("res", i)}={elem},9000000000,IF(AND({T(f"grupo.tem.{e}")}="Sim",'
                                  f'{cob}=0),0,2147483647))+{campo.xref}+{e}/10', nome=f"{p}.h12.chave{e}")
            chaves.append(f"${ch}${r}")
        faixa_ch = f"{chaves[0]}:{chaves[-1]}"
        for j in range(1, 5):
            put(f"sug{j}", f'=INDEX({dcol("elementos", "Elemento")},MATCH(SMALL({faixa_ch},{j}),{faixa_ch},0))')


def _i3_i4(ws):
    titulo(ws, I3 - 2, "I3 · Ficha — números (automático: a linha de 28.3 da faixa e do tipo)")
    cabs(ws, I3 - 1, {"A": "Inimigo", "B": "Faixa efetiva", "C": "PV", "D": "Defesa", "E": "RD", "F": "Tenacidade",
                      "G": "VEL", "H": "Teste de Ataque", "I": "DT dos efeitos", "J": "Teste de Resistência",
                      "K": ("Observação", "L")})
    for i in range(1, NI + 1):
        r, p = I3 + i - 1, f"inimigos.{i}"
        cal(ws, f"A{r}", rotulo(i), nome=f"{p}.rot3")
        vazio = f'LEN({T(f"{p}.nome")})=0'
        ch = A("chave", i)
        cal(ws, f"B{r}", f'=IF({vazio},"",{A("faixa", i)})', nome=f"{p}.faixa_ef", centro=True, regra=True)
        cal(ws, f"C{r}", f'=IF({vazio},"",{A("pv", i)})', nome=f"{p}.pv", centro=True, regra=True)
        for col, campo, coluna in (("D", "defesa", "Defesa"), ("E", "rd", "RD"), ("F", "ten", "Tenacidade"),
                                   ("G", "vel", "VEL"), ("I", "dt", "DT dos efeitos")):
            cal(ws, f"{col}{r}", f'=IF({vazio},"",{anc(coluna, ch)})', nome=f"{p}.{campo}", centro=True, regra=True)
        cal(ws, f"H{r}", f'=IF({vazio},"","+"&{anc("Ataque", ch)})', nome=f"{p}.ataque", centro=True, regra=True)
        cal(ws, f"J{r}", f'=IF({vazio},"","+"&{anc("Teste de Resistência", ch)})', nome=f"{p}.tr", centro=True,
            regra=True)
        cal(ws, f"K{r}", f'=IF({vazio},"",IF({A("modo", i)}="Por nível — Sugestão","PV do nível "&{A("nivel", i)}&'
                         f'": {N.ROTULO_SUGESTAO} (H1)",IF({A("aj", i)}=1,"Ajustado de "&{T(f"{p}.base")}&'
                         f'" (28.4 passo 3)","")))', nome=f"{p}.obs3", ate="L")
        sugestao_formula(f"{p}.obs3", "H1", [f"C{r}"])
    N.subtabela(ws, "I3", [I3 - 1], "A:L", NI)
    titulo(ws, I4 - 2, "I4 · Ficha — dano e regras (automático: 28.2, 28.3, 27.4)")
    cabs(ws, I4 - 1, {"A": "Inimigo", "B": ("Dano por acerto", "D"), "E": "Nº de Fraquezas (regra)",
                      "F": ("Na Fila", "G"), "H": "Ações agressivas por Ciclo", "I": "Custo no orçamento",
                      "J": "Execução", "K": ("Aviso", "L")})
    for i in range(1, NI + 1):
        r, p = I4 + i - 1, f"inimigos.{i}"
        cal(ws, f"A{r}", rotulo(i), nome=f"{p}.rot4")
        vazio = f'LEN({T(f"{p}.nome")})=0'
        ch = A("chave", i)
        cal(ws, f"B{r}", f'=IF({vazio},"",{anc("Dano por acerto", ch)}&" · média "&{anc("Média do dano", ch)})',
            nome=f"{p}.dano", ate="D", regra=True)
        cal(ws, f"E{r}", f'=IF({vazio},"",{anc("Nº de Fraquezas", ch)})', nome=f"{p}.nfraq", centro=True, regra=True)
        cal(ws, f"F{r}", f'=IF({vazio},"","VEL "&{anc("VEL", ch)}&", "&{anc("Firmeza", ch)})', nome=f"{p}.nafila",
            ate="G", regra=True)
        cal(ws, f"H{r}", f'=IF({vazio},"",{anc("Ações agressivas", ch)})', nome=f"{p}.acoes", centro=True, regra=True)
        cal(ws, f"I{r}", f'=IF({vazio},"",{cat_linha("custo", i)})', nome=f"{p}.custo", centro=True, regra=True)
        cal(ws, f"J{r}", f'=IF({vazio},"",{cat_linha("execucao", i)})', nome=f"{p}.execucao", centro=True, regra=True)
        nf = "+".join(f'IF(LEN({A(f"w{j}", i)})>0,1,0)' for j in range(1, 5))
        av(ws, f"K{r}", f"{p}.aviso4",
           f'=IF({vazio},"",IF(AND({A("tipo", i)}="Boss",({nf})<4),"Boss tem 4 Fraquezas (20.2): faltam "&(4-({nf})),'
           f'IF(AND({A("tipo", i)}="Elite",({nf})<3),"Elite tem 3 Fraquezas (20.2): faltam "&(3-({nf})),'
           f'IF(({nf})=0,"Sem Fraqueza: todo inimigo tem pelo menos 1 (20.2)",""))))', ate="L")
    N.subtabela(ws, "I4", [I4 - 1], "A:L", NI)


def cat_linha(campo, i):
    return f"${COLCAT[campo]}${CAT0 + i - 1}"


def _i5(ws):
    titulo(ws, I5A - 3, "I5 · Fases dos Bosses criados (28.5: a fase troca, não soma; Tenacidade ≤ âncora)")
    sugestao(ws, f"A{I5A - 2}", "H4", "inimigos.h4.rotulo", ate="L",
             extra="limiares em partes iguais: 2 fases → topo da fase 2 = metade dos PV; 3 fases → 2/3 e 1/3. "
                   "No modo Ajustar, as fases vêm da base (a I5 vence se preenchida).")
    for b, r0 in enumerate((I5A, I5B)):
        cabs(ws, r0 - 1, {"A": ("Inimigo", "B"), "C": "Fase (2 ou 3)", "D": "Fraqueza 1", "E": "Fraqueza 2",
                          "F": "Fraqueza 3", "G": "Fraqueza 4", "H": "Tenacidade da fase", "I": ("Ritmo", "J"),
                          "K": ("Aviso", "L")})
        for k in range(12):
            r = r0 + k
            n = b * 12 + k + 1
            p = f"inimigos.fase{n}"
            ent(ws, f"A{r}", f"{p}.inimigo", tipo="lista", fonte=T("inimigos.col.nome"), ate="B", rotulo="Inimigo",
                opcoes=[])
            ent(ws, f"C{r}", f"{p}.fase", tipo="inteiro", minimo=2, maximo=3, rotulo="Fase", centro=True)
            for j, col in enumerate("DEFG", start=1):
                ent(ws, f"{col}{r}", f"{p}.f{j}", tipo="lista", fonte="lista.elementos", rotulo=f"Fraqueza {j}",
                    centro=True)
            ent(ws, f"H{r}", f"{p}.ten", tipo="inteiro", minimo=0, maximo=13, rotulo="Tenacidade", centro=True)
            ent(ws, f"I{r}", f"{p}.ritmo", ate="J", maximo=80, rotulo="Ritmo")
            INIM = T(f"{p}.inimigo")
            N.aux(ws, f"N{r}", f'=IF(LEN({INIM})>0,{INIM}&"|"&{T(f"{p}.fase")},"")', nome=f"{p}.chave")
            N.aux(ws, f"O{r}", f'=IFERROR(MATCH({INIM},{T("inimigos.col.nome")},0),"")', nome=f"{p}.linha")
            lin = f"$O${r}"
            ten_anc = f'INDEX({T("inimigos.col.ten")},{lin})'
            fases_i = f'INDEX({ACOL("fases")},{lin})'
            nfq = "+".join(f'IF(LEN({T(f"{p}.f{j}")})>0,1,0)' for j in range(1, 5))
            av(ws, f"K{r}", f"{p}.aviso",
               f'=IF(LEN({INIM})=0,"",IF(NOT(ISNUMBER({lin})),"Inimigo fora da tabela I1",'
               f'IF(NOT(ISNUMBER({T(f"{p}.fase")})),"Diga a fase (2 ou 3)",'
               f'IF({T(f"{p}.fase")}>{fases_i},"Fase para inimigo sem essa fase: confira Fases na I1",'
               f'IF(AND(ISNUMBER({T(f"{p}.ten")}),{T(f"{p}.ten")}>{ten_anc}),'
               f'"Tenacidade acima da âncora: a planilha usa a âncora (28.5 regra 3)",'
               f'IF(({nfq})<4,"Boss tem 4 Fraquezas em cada fase (28.5 regra 4)",""))))))', ate="L")
        N.subtabela(ws, f"I5.{b + 1}", [r0 - 1], "A:L", 12)
    fim = I5B + 11
    N.reg("inimigos.i5.chaves", ws, f"N{I5A}:N{fim}")
    for j, col in enumerate("DEFG", start=1):
        N.reg(f"inimigos.i5.f{j}", ws, f"{col}{I5A}:{col}{fim}")
    N.reg("inimigos.i5.ten", ws, f"H{I5A}:H{fim}")


def _catalogo(ws):
    blo = N.MAPA.blocos["dados.bestiario"]
    fblk = N.MAPA.blocos["dados.bestiario_fases"]
    fichas = D.bestiario()
    fase_linha = {(f["criatura"], f["fase"]): k for k, f in enumerate(D.fases())}

    def dcel(coluna, ib):
        return f"'Dados'!${blo['colunas'][coluna]}${blo['primeira_linha'] + ib}"

    def fcel(coluna, criatura, fase):
        k = fase_linha.get((criatura, fase))
        return '""' if k is None else f"'Dados'!${fblk['colunas'][coluna]}${fblk['primeira_linha'] + k}"

    for k in range(NCAT):
        r = CAT0 + k
        if k < NI:
            v = _cat_campanha(k + 1)
        else:
            ib = k - NI
            fi = fichas[ib]
            dc = lambda c: f"={dcel(c, ib)}" + ('&""' if c in TEXTO_BES else "")  # noqa: E731
            v = {"nome": dc("Nome"), "tipo": dc("Tipo"), "faixa": dc("Faixa"), "pv": dc("PV"), "defesa": dc("Defesa"),
                 "rd": dc("RD"), "ten": dc("Tenacidade"), "vel": dc("VEL"), "ataque": dc("Ataque"),
                 "dano_e": dc("Dano por acerto"), "dano_m": dc("Média do dano"), "dt": dc("DT dos efeitos"),
                 "tr": dc("Teste de Resistência"), "f1": dc("Fraqueza 1"), "f2": dc("Fraqueza 2"),
                 "f3": dc("Fraqueza 3"), "f4": dc("Fraqueza 4"), "res": dc("Resistência"), "execucao": dc("Execução"),
                 "fases": dc("Fases"), "acoes": dc("Ações agressivas"), "custo": dc("Custo no orçamento"),
                 "firmeza": dc("Firmeza"), "origem": dc("Facção ou origem"), "origem2": dc("Origem 2"),
                 "faixa_idx": dc("Índice da faixa"), "fraq_txt": dc("Fraquezas (texto)"),
                 "ef": f"=INDEX({dcol('faixas', 'Eficiência do inimigo')},{dcel('Índice da faixa', ib)})",
                 "origem_tipo": '="Bestiário"'}
            v["lim2"] = f"={fcel('PV do topo', fi['nome'], 2)}"
            v["lim3"] = f"={fcel('PV do topo', fi['nome'], 3)}"
            for f_ in (2, 3):
                for j in range(1, 5):
                    v[f"p{f_}f{j}"] = f"={fcel(f'Fraqueza {j}', fi['nome'], f_)}"
                v[f"ten{f_}"] = f"={fcel('Tenacidade', fi['nome'], f_)}"
            for e in range(1, 4):
                v[f"esp{e}"] = dc(f"Especial {e}")
                rc = dcel(f"Recarga {e}", ib)
                v[f"rec{e}"] = f'=IF(ISNUMBER({rc}),IF({rc}>0,{rc},""),"")'
        for c in CATC:
            N.aux(ws, f"{COLCAT[c]}{r}", v[c])
    for c in CATC:
        N.reg(f"inimigos.cat.{c}", ws, f"{COLCAT[c]}{CAT0}:{COLCAT[c]}{CAT0 + NCAT - 1}")
    for c in ("tipo", "dano_e", "dano_m", "dt", "ten", "pv", "nome", "fases", "execucao", "vel", "firmeza", "origem",
              "res", "fraq_txt", "lim2", "lim3"):
        N.reg(f"inimigos.col.{c}" if c not in ("nome",) else "inimigos.col.nome_cat", ws,
              f"{COLCAT[c]}{CAT0}:{COLCAT[c]}{CAT0 + NI - 1}")
    for c in ("esp_e", "esp_m", "com_e", "com_m", "aj", "pv_orig", "brow"):
        N.reg(f"inimigos.col.{c}", ws, f"{AUXCOL[c]}{I1}:{AUXCOL[c]}{I1 + NI - 1}")


def _cat_campanha(i):
    p = f"inimigos.{i}"
    vazio = f'LEN({T(f"{p}.nome")})=0'
    ch = A("chave", i)
    v = {
        "nome": f'=IF({vazio},"",{T(f"{p}.nome")})',
        "tipo": f'=IF({vazio},"",{A("tipo", i)})', "faixa": f'=IF({vazio},"",{A("faixa", i)})',
        "pv": f'=IF({vazio},"",{A("pv", i)})',
        "defesa": f'=IF({vazio},"",{anc("Defesa", ch)})', "rd": f'=IF({vazio},"",{anc("RD", ch)})',
        "ten": f'=IF({vazio},"",{anc("Tenacidade", ch)})', "vel": f'=IF({vazio},"",{anc("VEL", ch)})',
        "ataque": f'=IF({vazio},"",{anc("Ataque", ch)})', "dano_e": f'=IF({vazio},"",{anc("Dano por acerto", ch)})',
        "dano_m": f'=IF({vazio},"",{anc("Média do dano", ch)})', "dt": f'=IF({vazio},"",{anc("DT dos efeitos", ch)})',
        "tr": f'=IF({vazio},"",{anc("Teste de Resistência", ch)})',
        "res": f'=IF({vazio},"",{A("res", i)})',
        "execucao": f'=IF({vazio},"",IF({T(f"{p}.racional")}="Sim","Pode",IF({T(f"{p}.racional")}="Não","Não",'
                    f'IF({A("aj", i)}=1,{bes("Execução", A("brow", i))},"Não declarado"))))',
        "fases": f'=IF({vazio},"",{A("fases", i)})', "acoes": f'=IF({vazio},"",{anc("Ações agressivas", ch)})',
        "custo": f'=IF({vazio},"",IF(AND({A("aj", i)}=1,{T(f"{p}.base")}="Escória de Stellaron"),1.5,1)*{A("pv", i)})',
        "firmeza": f'=IF({vazio},"",{anc("Firmeza", ch)})',
        "lim2": f'=IF({vazio},"",IF({A("fases", i)}=2,INT({A("pv", i)}/2),IF({A("fases", i)}=3,'
                f'INT(2*{A("pv", i)}/3),"")))',
        "lim3": f'=IF({vazio},"",IF({A("fases", i)}=3,INT({A("pv", i)}/3),""))',
        "origem": f'=IF({vazio},"",IF(LEN({T(f"{p}.faccao")})>0,{T(f"{p}.faccao")},IF({A("aj", i)}=1,'
                  f'{bes("Facção ou origem", A("brow", i))},"")))',
        "origem2": f'=IF(AND(LEN({T(f"{p}.faccao")})=0,{A("aj", i)}=1),{bes("Origem 2", A("brow", i))},"")',
        "ef": f'=IF({vazio},"",INDEX({dcol("faixas", "Eficiência do inimigo")},{A("fidx", i)}))',
        "faixa_idx": f'=IF({vazio},"",{A("fidx", i)})', "fraq_txt": f'={T(f"{p}.fraq_txt")}',
        "origem_tipo": '="Campanha"',
    }
    for j in range(1, 5):
        v[f"f{j}"] = f'=IF({vazio},"",{A(f"w{j}", i)})'
    ten_new = anc("Tenacidade", ch)
    for f_ in (2, 3):
        i5 = f'MATCH({T(f"{p}.nome")}&"|{f_}",{T("inimigos.i5.chaves")},0)'
        bk = f'MATCH({T(f"{p}.base")}&"|{f_}",{dcol("bestiario_fases", "Chave")},0)'
        semfase = f'OR({vazio},{A("fases", i)}<{f_})'
        for j in range(1, 5):
            v[f"p{f_}f{j}"] = (f'=IF({semfase},"",IFERROR(INDEX({T(f"inimigos.i5.f{j}")},{i5})&"",IF({A("aj", i)}=1,'
                               f'IFERROR(INDEX({dcol("bestiario_fases", f"Fraqueza {j}")},{bk}),""),"")))')
        t5 = f'INDEX({T("inimigos.i5.ten")},{i5})'
        # sem linha em I5: no Ajustar, a Tenacidade da fase da base reescalada (28.5 regra 3: ≤ âncora). O teste é
        # ISNUMBER(MATCH): ISNUMBER(INDEX(…, #N/A)) dá FALSE, não erro, e o IFERROR antigo nunca chegava ao Ajustar
        v[f"ten{f_}"] = (f'=IF({semfase},"",IF(ISNUMBER({i5}),IF(ISNUMBER({t5}),MIN({ten_new},{t5}),{ten_new}),'
                         f'IF({A("aj", i)}=1,IFERROR(MIN({ten_new},INT(INDEX({dcol("bestiario_fases", "Tenacidade")},'
                         f'{bk})*{ten_new}/{A("ten_orig", i)})),{ten_new}),{ten_new})))')
    for e in range(1, 4):
        kb = q(f"|{e}")
        v[f"esp{e}"] = (f'=IF({vazio},"",IF({A("aj", i)}=1,{bes(f"Especial {e}", A("brow", i))},'
                        f'IFERROR(INDEX({T("inimigos.ac.nome")},MATCH({T(f"{p}.nome")}&{kb},'
                        f'{T("inimigos.ac.chave_esp")},0))&"","")))')
        rb = bes(f"Recarga {e}", A("brow", i))
        v[f"rec{e}"] = (f'=IF({vazio},"",IF({A("aj", i)}=1,IF(ISNUMBER({rb}),IF({rb}>0,{rb},""),""),'
                        f'IFERROR(INDEX({T("inimigos.ac.recarga")},MATCH({T(f"{p}.nome")}&{kb},'
                        f'{T("inimigos.ac.chave_esp")},0))+0,"")))')
    return v
