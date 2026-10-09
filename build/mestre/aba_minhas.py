# -*- coding: utf-8 -*-
"""
Aba Minhas Tabelas (R11; design §6.17): 10 tabelas do Mestre (G = 701…710), cada uma com nome, 100 vagas (o mesmo
contador corrido da aba Tabelas, 4.2), Rolagem nº e "quantos sortear" (1 a 5). Os resultados saem em sequência sem
repetir: o k-ésimo é MOD(i₀ − 1 + k·passo, n) + 1, com i₀ = escolha(x) e o passo o primeiro de 7, 11, 13, 17, 19, 23
que não divide n (sorteio.passo). Com n menor que "quantos", a lista repete e o aviso diz quantas entradas ela tem.
"""

from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

from mestre import nucleo as N
from mestre import sorteio as S
from mestre import historia as H
from mestre.nucleo import T, ent, cal, av, rot, cab, cabs, titulo

NT, VAGAS, FAIXA, QMAX = 10, 100, 13, 5
GRUPOS = [("B", "D"), ("E", "G"), ("H", "J")]        # 3 tabelas por faixa de linhas (4 faixas: 3 + 3 + 3 + 1)


def montar(wb):
    ws = wb["Minhas Tabelas"]
    N.larguras_grade(ws, {**N.GRADE_PX, "A": 110, "B": 104, "C": 104, "D": 104, "E": 104, "F": 104, "G": 104, "H": 104,
                          "I": 104, "J": 104, "K": 147, "L": 147})
    lin_sorteio = 7
    lin_res = lin_sorteio + NT + 3
    r_listas = lin_res + NT + 2
    vagas = _listas(ws, r_listas)
    titulo(ws, 5, "Sorteio (G = 701 a 710): a semente é a da aba Início; cada tabela tem a sua Rolagem nº")
    cabs(ws, 6, {"A": "Tabela", "B": ("Nome da tabela (preencha)", "E"), "F": "Rolagem nº", "G": "Quantos sortear",
                 "H": "Tamanho da lista", "I": "Rolagem efetiva", "J": "Quantos (efetivo)", "K": ("Aviso", "L")})
    for t in range(1, NT + 1):
        r = lin_sorteio + t - 1
        p = f"minhas.{t}"
        rot(ws, f"A{r}", f"Tabela {t}", negrito=True)
        ent(ws, f"B{r}", f"{p}.nome", maximo=40, ate="E", rotulo="Nome da tabela")
        ent(ws, f"F{r}", f"{p}.rolagem", tipo="inteiro", minimo=1, maximo=1000000, rotulo="Rolagem nº", centro=True,
            amostra=2)
        ent(ws, f"G{r}", f"{p}.quantos", tipo="inteiro", minimo=1, maximo=QMAX, rotulo="Quantos sortear", centro=True,
            amostra=3)
        cont = vagas[t]["contador"]
        cal(ws, f"H{r}", f"={cont[-1]}", nome=f"{p}.tamanho", centro=True)
        cal(ws, f"I{r}", S.rolagem_efetiva(T(f"{p}.rolagem")), nome=f"{p}.rol_ef", centro=True)
        Q = T(f"{p}.quantos")
        cal(ws, f"J{r}", f"=IF(ISNUMBER({Q}),MIN({QMAX},MAX(1,INT({Q}))),1)", nome=f"{p}.quantos_ef", centro=True)
    for t in range(1, NT + 1):
        p = f"minhas.{t}"
        xs = H.campos(ws, 700 + t, f"{p}.rol_ef", 10 + 2 * (t - 1), "AA", ["a própria tabela", "quantos sortear"])
        x = xs[1]
        n, qe = T(f"{p}.tamanho"), T(f"{p}.quantos_ef")
        r = lin_sorteio + t - 1
        N.aux(ws, f"N{r}", "=" + S.passo(n), nome=f"{p}.passo")
        N.aux(ws, f"O{r}", "=" + S.escolha(x, n), nome=f"{p}.i0")
        val, cnt = vagas[t]["valores"], vagas[t]["intervalo_contador"]
        res = []
        for k in range(QMAX):
            ix = S.kesimo_sem_repetir(T(f"{p}.i0"), k, n, T(f"{p}.passo"))
            N.aux(ws, f"{L(16 + k)}{r}", f'=IF({k}<{qe},IF({n}<=0,"",IFERROR(INDEX({val},MATCH({ix},{cnt},0))&"","")),"")',
                  nome=f"{p}.res.{k + 1}")
            res.append(T(f"{p}.res.{k + 1}"))
        rr = lin_res + t - 1
        cal(ws, f"A{rr}", f'=IF(LEN({T(f"{p}.nome")})>0,{T(f"{p}.nome")},"Tabela {t}")', nome=f"{p}.rotulo")
        junta = f'"1. "&{res[0]}' + "".join(f'&IF(LEN({res[k]})>0," · {k + 1}. "&{res[k]},"")' for k in range(1, QMAX))
        cal(ws, f"B{rr}", f'=IF(LEN({res[0]})=0,"",{junta})', nome=f"{p}.resultado", ate="J")
        R_, NM_ = T(f"{p}.rolagem"), T(f"{p}.nome")
        av(ws, f"K{lin_sorteio + t - 1}", f"{p}.aviso",
           f'=IF(LEN({S.aviso_rolagem(R_)[1:]})>0,{S.aviso_rolagem(R_)[1:]},IF(IF(ISNUMBER({T(f"{p}.quantos")}),'
           f'OR({T(f"{p}.quantos")}<1,{T(f"{p}.quantos")}>{QMAX},INT({T(f"{p}.quantos")})<>{T(f"{p}.quantos")}),FALSE),'
           f'"Quantos fora de 1 a {QMAX}: usando o limite",IF(AND({n}<=0,LEN({NM_}&{T(f"{p}.quantos")}&{R_})>0),'
           f'"Tabela vazia: preencha as vagas abaixo",IF(AND({n}>0,{n}<{qe}),"A lista tem só "&{n}&'
           f'" entrada(s): os resultados se repetem",IF({n}>={VAGAS},"Lista cheia (100)","")))))', ate="L")
    N.subtabela(ws, "minhas.sorteio", [6], "A:L", NT)
    titulo(ws, lin_res - 2, "Resultados (automático): copie e cole como valores onde precisar")
    cabs(ws, lin_res - 1, {"A": "Tabela", "B": ("Resultados da rolagem, na ordem (sem repetir)", "J")})
    N.subtabela(ws, "minhas.resultados", [lin_res - 1], "A:J", NT)
    rot(ws, f"A{lin_res + NT}", "Com n entradas, os resultados de uma rolagem não se repetem enquanto 'quantos' ≤ n "
                                "(passo primo, 6.17). Editar a lista muda o sorteio: o resultado é função da semente, da "
                                "Rolagem nº e da lista.", ate="L", italico=True)
    N.MAPA.extra["minhas"] = {str(t): {"vagas": vagas[t]["vagas"], "cabecalhos": vagas[t]["cabecalhos"]}
                              for t in range(1, NT + 1)}


def _listas(ws, r0):
    """As 10 listas em faixas de 3 (B:D, E:G, H:J), 100 vagas cada em 8 blocos de 13 (o último com 9) com o
    cabeçalho repetido; contador corrido em coluna oculta. Devolve {t: {...}}."""
    saida = {}
    r = r0
    for banda in range((NT + 2) // 3):
        ts = list(range(3 * banda + 1, min(NT, 3 * banda + 3) + 1))
        ult = GRUPOS[len(ts) - 1][1]
        titulo(ws, r, f"Listas {ts[0]} a {ts[-1]} (100 vagas cada): apague para trocar, use as vagas vazias para ampliar; "
                      f"não insira linhas" if len(ts) > 1 else f"Lista {ts[0]} (100 vagas): apague para trocar, use as "
                                                             f"vagas vazias para ampliar; não insira linhas", ate=ult)
        r += 1
        cabs_lin, vag_lin = [], []
        for b in range(8):
            cabs_lin.append(r)
            r += 1
            for _ in range(FAIXA if b < 7 else VAGAS - 7 * FAIXA):
                vag_lin.append(r)
                r += 1
        for j, t in enumerate(ts):
            c0, c1 = GRUPOS[j]
            cc = L(40 + 3 * banda + j)                # contador (coluna oculta, uma por tabela)
            dv = DataValidation(type="textLength", operator="lessThanOrEqual", formula1="200", allow_blank=True,
                                showErrorMessage=True, errorStyle="warning", errorTitle="Texto longo",
                                error="Vaga: até 200 caracteres (o sorteio usa o texto mesmo assim).")
            for k, rc in enumerate(cabs_lin):
                cab(ws, f"{c0}{rc}", f"Tabela {t}", ate=c1)
                N.aux(ws, f"{cc}{rc}", "=0" if k == 0 else f"={cc}{rc - 1}")
                if j == 0:
                    a, b_ = 13 * k + 1, min(VAGAS, 13 * k + (FAIXA if k < 7 else VAGAS - 7 * FAIXA))
                    cab(ws, f"A{rc}", f"Vagas {a}–{b_}")
            vagas = []
            for k, rv in enumerate(vag_lin, start=1):
                N.vaga(ws, f"{c0}{rv}", f"minhas.{t}.vaga{k}", ate=c1)
                dv.add(f"{c0}{rv}")
                N.aux(ws, f"{cc}{rv}", f"={cc}{rv - 1}+IF(LEN({c0}{rv})>0,1,0)")
                vagas.append(f"{c0}{rv}")
                if j == 0:
                    rot(ws, f"A{rv}", str(k))
            ws.add_data_validation(dv)
            saida[t] = {"vagas": vagas, "cabecalhos": [f"{c0}{x}" for x in cabs_lin],
                        "valores": f"${c0}${vag_lin[0]}:${c0}${vag_lin[-1]}",
                        "intervalo_contador": f"${cc}${vag_lin[0]}:${cc}${vag_lin[-1]}",
                        "contador": [f"${cc}${vag_lin[-1]}"]}
            N.reg(f"minhas.{t}.valores", ws, f"{c0}{vag_lin[0]}:{c0}{vag_lin[-1]}")
        for rv in vag_lin:
            ws.row_dimensions[rv].height = 15
        N.subtabela(ws, f"minhas.listas.{banda + 1}", cabs_lin, "A:J", VAGAS)
        r += 1
    return saida
