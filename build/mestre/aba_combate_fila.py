# -*- coding: utf-8 -*-
"""
Aba Combate — tabela de estado (oculta), Fila de Ação C8/C9 (19.3–19.6, H13), painel de consulta rápida das condições
C9b, condições por combatente C7 (21.5) e calculadora C10 (23.1, 20.2, 20.3). Ver o cabeçalho de aba_combate.py.

Fase 4 (pedido do usuário depois de jogar em mesa): 22 combatentes (os 6 Memoespíritos entram na Fila pela VEL deles,
11.5 e 19.7); cada combatente tem 4 condições ao mesmo tempo, com turnos restantes (C7); a condição com 0 turnos
fica marcada como EXPIRADA e sai da conta; o painel C9b mostra todas as ativas de uma vez, em quem, por quantos
turnos e o que cada uma faz (21.5).
"""

from mestre import nucleo as N
from mestre.nucleo import T, ent, cal, av, rot, cabs, titulo, dcol
from mestre.aba_combate_base import (NPJ, NIN, NC, MI0, NSLOT, NPAINEL, ST0, SC, CC, R_C3, R_C7, R_C7_TIT, R_C8, R_C9,
                                     R_C9B, R_C9B_TIT, R_PEND, R_C10, EC, s, srng, e_, cat, linha_bloco, slot,
                                     linha_slot)


# o rótulo mais comprido de um Memoespírito: nome (30) + " (de " + nome do PJ (30) + ")" — mede a altura das linhas
PIOR_MEMO = "Lembrança Antiga do Porto Sete (de Personagem com Nome Bem Comprido)"


def montar(ws):
    _estado(ws)
    _fila(ws)
    _condicoes(ws)
    _painel(ws)
    _calculadora(ws)


def _slots_rng(c):
    """Coluna auxiliar `c` da C7 inteira (inclui as linhas de cabeçalho, onde fica vazia)."""
    return f"${CC[c]}${R_C7[0]}:${CC[c]}${linha_slot(NC * NSLOT)}"


def _estado(ws):
    """Uma linha por combatente: a Fila inteira é calculada aqui (colunas ocultas)."""
    CIC = T("combate.ciclo_ef")
    comb, cond, turn = T("combate.cond.col.comb"), T("combate.cond.col.cond"), T("combate.cond.col.turnos")
    for i in range(1, NC + 1):
        r = ST0 + i - 1
        put = lambda c, f, r=r, i=i: N.aux(ws, f"{SC[c]}{r}", f, nome=f"combate.st{i}.{c}")  # noqa: E731
        c8 = f"combate.f{i}"
        if i <= NPJ:
            g, p = f"grupo.pj{i}", f"combate.pj{i}"
            put("lab", f'=IF(LEN({T(g + ".nome")})>0,{T(g + ".nome")},"")')
            put("tipo", '="PJ"')
            put("ex", f'=IF(AND(LEN({T(g + ".nome")})>0,{T(p + ".participa")}<>"Não"),1,0)')
            put("pvmax", f'=IF(ISNUMBER({T(g + ".pv")}),MAX(1,{T(g + ".pv")}),1)')
            PV = T(p + ".pv")
            put("pvat", f'=IF(ISNUMBER({PV}),MIN({s("pvmax", i)},MAX(0,INT({PV}))),{s("pvmax", i)})')
            FA = T(p + ".fal")
            put("vivo", f'=IF(AND({s("ex", i)}=1,NOT(AND(ISNUMBER({FA}),{FA}>=3))),1,0)')
            put("velb", f'=IF(ISNUMBER({T(g + ".vel")}),{T(g + ".vel")},10)')
            AJ = T(p + ".ajvel")
            ag, di = T(g + ".ag"), T(g + ".disc")
            put("tag", f'=MIN(30,MAX(15,IF(ISNUMBER({ag}),{ag},0)+20))')
            put("tdisc", f'=MIN(30,MAX(15,IF(ISNUMBER({di}),{di},0)+20))')
            E = T(c8 + ".ordem")
            put("ttipo", f'=5+(5-IF(ISNUMBER({E}),MIN(5,MAX(1,INT({E}))),5))')
            put("tlin", f"={(10 - i) / 100}")
            put("ef", f'={T("campanha.ef")}')
            put("cong", "=0")
        elif i <= MI0:
            e, p = i - NPJ, f"combate.in{i - NPJ}"
            IX = e_("idx", e)
            nm = e_("nome", e)
            put("lab", f'=IF(LEN({nm})=0,"",{nm}&IF(COUNTIF({erng_nome()},{nm})>1," "&COUNTIF(${EC["nome"]}${R_C3}:'
                       f'{nm},{nm}),""))')
            put("tipo", f'=IF(ISNUMBER({IX}),{cat("tipo", IX)},"")')
            put("ex", f'=IF(ISNUMBER({IX}),1,0)')
            put("pvmax", f'=IF(ISNUMBER({IX}),{cat("pv", IX)},1)')
            PV = T(p + ".pv")
            put("pvat", f'=IF(ISNUMBER({PV}),MIN({s("pvmax", i)},MAX(0,INT({PV}))),{s("pvmax", i)})')
            put("vivo", f'=IF(AND({s("ex", i)}=1,{s("pvat", i)}>0),1,0)')
            put("velb", f'=IF(ISNUMBER({IX}),{cat("vel", IX)},0)')
            AJ = T(p + ".ajvel")
            put("tag", "=0")
            put("tdisc", "=0")
            put("ttipo", "=0")
            put("tlin", f"={(20 - e) / 100}")
            put("ef", f'=IF(ISNUMBER({IX}),{cat("ef", IX)},0)')
            put("cong", f'=IF(LEN({s("lab", i)})=0,0,IF(COUNTIFS({comb},{s("lab", i)},{cond},"Congelado")-'
                        f'COUNTIFS({comb},{s("lab", i)},{cond},"Congelado",{turn},0)>0,1,0))')
        else:
            # Memoespírito do PJ m (11.5): casa própria na Fila pela VEL dele; sem Tenacidade, nunca Congelado (21.2)
            m = i - MI0
            g, p = f"grupo.pj{m}", f"combate.memo{m}"
            NOME, MN = T(g + ".nome"), T(g + ".memo.nome")
            put("lab", f'=IF(AND(LEN({NOME})>0,{T(g + ".memo.tem")}="Sim"),IF(LEN({MN})>0,{MN}&" (de "&{NOME}&")",'
                       f'"Memoespírito de "&{NOME}),"")')
            put("tipo", '="Memoespírito"')
            put("ex", f'=IF(AND(LEN({s("lab", i)})>0,{s("ex", m)}=1,{T(p + ".invocado")}="Sim"),1,0)')
            put("pvmax", f'=IF(ISNUMBER({T(g + ".memo.pv_ef")}),MAX(1,{T(g + ".memo.pv_ef")}),1)')
            PV = T(p + ".pv")
            put("pvat", f'=IF(ISNUMBER({PV}),MIN({s("pvmax", i)},MAX(0,INT({PV}))),{s("pvmax", i)})')
            put("vivo", f'=IF(AND({s("ex", i)}=1,{s("pvat", i)}>0),1,0)')
            put("velb", f'=IF(ISNUMBER({T(g + ".memo.vel_ef")}),{T(g + ".memo.vel_ef")},10)')
            AJ = T(p + ".ajvel")
            ag, di = T(g + ".memo.agi"), T(g + ".memo.disc")
            put("tag", f'=MIN(30,MAX(15,IF(ISNUMBER({ag}),{ag},0)+20))')
            put("tdisc", f'=MIN(30,MAX(15,IF(ISNUMBER({di}),{di},0)+20))')
            put("ttipo", "=5")                                                   # lado dos jogadores (H27)
            put("tlin", f"={(30 - m) / 1000}")                                   # depois dos PJs (H27)
            put("ef", f'={T("campanha.ef")}')
            put("cong", "=0")
        put("vel", f'=MIN(40,MAX(0,{s("velb", i)}+IF(ISNUMBER({AJ}),MIN(10,MAX(-10,INT({AJ}))),0)))')
        put("chave", f'={s("vel", i)}*100000+{s("tag", i)}*1000+{s("tdisc", i)}*10+{s("ttipo", i)}+{s("tlin", i)}')
        congc = f'AND({s("cong", i)}=1,{s("tipo", i)}="Comum")'
        put("ativo", f'=IF(AND({s("vivo", i)}=1,NOT({congc})),1,0)')
        put("ativon", f'={s("vivo", i)}')
        put("surp", f'=IF(AND({CIC}=1,LEN({s("lab", i)})>0),IF(COUNTIFS({comb},{s("lab", i)},{cond},"Surpreso")-'
                    f'COUNTIFS({comb},{s("lab", i)},{cond},"Surpreso",{turn},0)>0,1,0),0)')
        AT, PE, AV, JA, MA = (T(c8 + ".atraso"), T(c8 + ".pend"), T(c8 + ".avancar"), T(c8 + ".ja"),
                              T(c8 + ".manual"))
        put("bruto", f'=IF(ISNUMBER({AT}),MAX(0,INT({AT})),0)')
        B = s("bruto", i)
        put("firm", f'=IF(AND({s("cong", i)}=1,{s("tipo", i)}<>"Comum"),2,IF({s("tipo", i)}="Comum",MIN(3,{B}),'
                    f'IF(OR({s("tipo", i)}="Elite",{s("tipo", i)}="Boss"),IF({B}=0,0,MIN(2,MAX(1,INT({B}/2)))),{B})))')
        teto = f'IF({s("tipo", i)}="Comum",3,IF(OR({s("tipo", i)}="PJ",{s("tipo", i)}="Memoespírito"),999,2))'
        put("pendp", f'=IF({congc},0,MIN({teto},IF(ISNUMBER({PE}),MAX(0,INT({PE})),0)))')
        put("ja", f'=IF({JA}="Sim",1,0)')
        put("avc", f'=IF({s("ja", i)}=1,0,IF(ISNUMBER({AV}),MAX(0,INT({AV})),0))')
        put("man", f'=IF(ISNUMBER({MA}),{MA},"")')
        put("base", f'=IF({s("ativo", i)}=1,1+COUNTIFS({srng("ativo")},1,{srng("chave")},">"&{s("chave", i)}),"")')
        d = f'({s("pendp", i)}+IF({s("ja", i)}=1,0,{s("firm", i)}))'
        put("posr", f'=IF({s("ativo", i)}=1,{s("base", i)}+{d},"")')
        put("posc", f'=IF({s("ativo", i)}=1,MIN({T("combate.n")},{s("posr", i)}),"")')
        put("exc", f'=IF({s("ativo", i)}=1,{s("posr", i)}-{s("posc", i)},0)')
        put("ch2", f'=IF({s("ativo", i)}=0,"",IF(ISNUMBER({s("man", i)}),{s("man", i)}-0.7+{i}/1000,{s("posc", i)}+'
                   f'IF({d}>0,0.5,0)-{s("avc", i)}-IF({s("avc", i)}>0,0.5,0)+{i}/1000))')
        put("pendn", f'=IF(OR({s("vivo", i)}=0,{congc}),0,MIN({teto},IF({s("ja", i)}=1,{s("firm", i)},0)+{s("exc", i)}))')
        put("basen", f'=IF({s("ativon", i)}=1,1+COUNTIFS({srng("ativon")},1,{srng("chave")},">"&{s("chave", i)}),"")')
        put("chn", f'=IF({s("ativon", i)}=1,{s("basen", i)}+{s("pendn", i)}+IF({s("pendn", i)}>0,0.5,0)+{i}/1000,"")')
        put("flag", f'=IF(AND({s("ativo", i)}=1,{s("ja", i)}=0,{s("surp", i)}=0),1,0)')
        put("avt", f'=IF({T(c8 + ".avtotal")}="Sim",1,0)')
        put("ncond", "=" + "+".join(f'${CC["ativa"]}${linha_slot(slot(i, k))}' for k in range(1, NSLOT + 1)))
    N.reg("combate.lista.todos", ws, f"{SC['lab']}{ST0}:{SC['lab']}{ST0 + NC - 1}")
    N.reg("combate.lista.pjs", ws, f"{SC['lab']}{ST0}:{SC['lab']}{ST0 + NPJ - 1}")
    N.reg("combate.lista.inimigos", ws, f"{SC['lab']}{ST0 + NPJ}:{SC['lab']}{ST0 + MI0 - 1}")
    for k, v, sec in (("firmeza.divisor", 2, "19.4"), ("firmeza.minimo", 1, "19.4"), ("teto.atraso.comum", 3, "19.4"),
                      ("teto.atraso.elite_boss", 2, "19.4"), ("congelamento.atraso", 2, "19.6"),
                      ("chave.termo_pj", 20, "19.3 passo 2 (H13)"), ("quebrado.defesa", -2, "20.4"),
                      ("sangramento.pct", 5, "21.2"), ("sangramento.teto_ef", 3, "21.2"),
                      ("fraqueza.dados", 2, "20.2"), ("resistencia.dados", -2, "20.2"), ("teto.dados_extra", 3, "16.9"),
                      ("energia.ultimate", 100, "17.2"), ("morrendo.dt", 10, "23.4"), ("dano.minimo", 1, "23.1"),
                      ("memo.vel_caminho", 1, "19.1 e 11.4"), ("condicoes.por_combatente", NSLOT, "pedido do usuário")):
        N.constante(k, v, sec)


def erng_nome():
    return f"${EC['nome']}${R_C3}:${EC['nome']}${R_C3 + NIN - 1}"


def _fila(ws):
    titulo(ws, R_C8[0] - 2, "C8 · Fila — entradas do Ciclo (19.3–19.6)")
    for r0 in R_C8:
        cabs(ws, r0 - 1, {"A": "Combatente", "B": "VEL efetiva", "C": "Ordem entre empatados (PJ, 1–5)",
                          "D": "Atraso deste Ciclo (casas)", "E": "Atraso pendente do Ciclo anterior", "F": "Avançar",
                          "G": "Avanço Total", "H": "Já agiu?", "I": "Casa manual",
                          "J": "Pendente para o Ciclo seguinte", "K": ("Aviso", "L")})
    for i in range(1, NC + 1):
        r = linha_bloco(R_C8, i)
        p = f"combate.f{i}"
        cal(ws, f"A{r}", f'=IF(LEN({s("lab", i)})>0,{s("lab", i)},"{i} · (vazio)")', nome=f"{p}.rot")
        if i > MI0:
            N.pior(ws, f"A{r}", PIOR_MEMO)
        cal(ws, f"B{r}", f'=IF({s("ex", i)}=1,{s("vel", i)},"")', nome=f"{p}.vel", centro=True, regra=True)
        if i <= NPJ:
            ent(ws, f"C{r}", f"{p}.ordem", tipo="inteiro", minimo=1, maximo=5, rotulo="Ordem entre empatados",
                centro=True, amostra=1)
        else:
            cal(ws, f"C{r}", '="—"', centro=True)
        ent(ws, f"D{r}", f"{p}.atraso", tipo="inteiro", minimo=0, maximo=20, rotulo="Atraso", centro=True, amostra=3)
        ent(ws, f"E{r}", f"{p}.pend", tipo="inteiro", minimo=0, maximo=20, rotulo="Atraso pendente", centro=True,
            amostra=1)
        ent(ws, f"F{r}", f"{p}.avancar", tipo="inteiro", minimo=0, maximo=20, rotulo="Avançar", centro=True, amostra=1)
        ent(ws, f"G{r}", f"{p}.avtotal", tipo="lista", fonte="lista.sim_nao", rotulo="Avanço Total", centro=True)
        ent(ws, f"H{r}", f"{p}.ja", tipo="lista", fonte="lista.sim_nao", rotulo="Já agiu?", centro=True)
        ent(ws, f"I{r}", f"{p}.manual", tipo="inteiro", minimo=1, maximo=NC, rotulo="Casa manual", centro=True)
        cal(ws, f"J{r}", f'=IF({s("ex", i)}=1,{s("pendn", i)},"")', nome=f"{p}.pendn", centro=True, regra=True)
        AV = T(p + ".avancar")
        av(ws, f"K{r}", f"{p}.aviso",
           f'=IF({s("ex", i)}=0,"",IF(AND({s("cong", i)}=1,{s("tipo", i)}="Comum"),"Congelado: fora da Fila neste '
           f'Ciclo; pendentes descartados (19.6)",IF(AND({s("cong", i)}=1,{s("bruto", i)}>0),"Congelado: o Atraso 2 já '
           f'é o teto; nada mais soma (19.6)",IF(AND(ISNUMBER({AV}),{AV}>0,{s("ja", i)}=1),"Avançar não vale em quem '
           f'já agiu (19.5)",IF({s("firm", i)}<{s("bruto", i)},"Teto/Firmeza: "&{s("bruto", i)}&" casa(s) viram "&'
           f'{s("firm", i)}&" (19.4)",IF({s("avt", i)}=1,"Avanço Total: age logo após o turno atual, 1 por Ciclo '
           f'(19.5); use Casa manual se quiser fixar",""))))))', ate="L")
    N.subtabela(ws, "C8", [r - 1 for r in R_C8], "A:L", NC)
    titulo(ws, R_C9[0] - 2, "C9 · Fila do Ciclo atual (à esquerda) e Fila prevista do Ciclo seguinte (à direita)")
    for r0 in R_C9:
        cabs(ws, r0 - 1, {"A": "Casa", "B": ("Combatente", "C"), "D": "VEL", "E": "Situação",
                          "F": ("Ciclo seguinte: combatente", "H"), "I": "VEL", "J": "Pendente aplicado"})
    for k in range(1, NC + 1):
        r = linha_bloco(R_C9, k)
        p = f"combate.fila{k}"
        N.aux(ws, f"N{r}", f'=IF({k}>{T("combate.n")},"",MATCH(SMALL({srng("ch2")},{k}),{srng("ch2")},0))',
              nome=f"{p}.c")
        C = f"$N${r}"
        N.aux(ws, f"O{r}", f'=IF({C}="",0,INDEX({srng("flag")},{C}))', nome=f"{p}.flag")
        prev = "0" if k == 1 else f"$P${linha_bloco(R_C9, k - 1)}"
        N.aux(ws, f"P{r}", f"={prev}+$O${r}", nome=f"{p}.cum")
        nn = f'SUM({srng("ativon")})'
        N.aux(ws, f"Q{r}", f'=IF({k}>{nn},"",MATCH(SMALL({srng("chn")},{k}),{srng("chn")},0))', nome=f"{p}.cn")
        CN = f"$Q${r}"
        ix = lambda c, x=C: f'INDEX({srng(c)},{x})'  # noqa: E731
        cal(ws, f"A{r}", f'=IF({C}="","",{k})', nome=f"{p}.casa", centro=True, regra=True)
        cal(ws, f"B{r}", f'=IF({C}="","",{ix("lab")})', nome=f"{p}.nome", ate="C", regra=True)
        N.pior(ws, f"B{r}", PIOR_MEMO)
        cal(ws, f"D{r}", f'=IF({C}="","",{ix("vel")})', nome=f"{p}.vel", centro=True, regra=True)
        cal(ws, f"E{r}", f'=IF({C}="","",IF({ix("surp")}=1,"Surpreso: casa pulada",IF({ix("ja")}=1,"Já agiu",'
                         f'IF(AND($O${r}=1,$P${r}=1),"Agindo agora",""))))', nome=f"{p}.situacao", regra=True)
        cal(ws, f"F{r}", f'=IF({CN}="","",{ix("lab", CN)})', nome=f"{p}.nome_n", ate="H", regra=True)
        cal(ws, f"I{r}", f'=IF({CN}="","",{ix("vel", CN)})', nome=f"{p}.vel_n", centro=True, regra=True)
        cal(ws, f"J{r}", f'=IF({CN}="","",{ix("pendn", CN)})', nome=f"{p}.pend_n", centro=True, regra=True)
    N.subtabela(ws, "C9", [r - 1 for r in R_C9], "A:J", NC)
    r = R_PEND
    pend = "&".join(f'IF(AND({s("ex", i)}=1,{s("pendn", i)}>0),{s("lab", i)}&" −"&{s("pendn", i)}&" casa(s); ","")'
                    for i in range(1, NC + 1))
    cong = "&".join(f'IF(AND({s("cong", i)}=1,{s("tipo", i)}="Comum",{s("vivo", i)}=1),{s("lab", i)}&": CONGELADO; ","")'
                    for i in range(NPJ + 1, MI0 + 1))
    rot(ws, f"A{r}", "PENDENTES", negrito=True)
    cal(ws, f"B{r}", f'={pend}&{cong}', nome="combate.pendentes", ate="L")
    N.pior(ws, f"B{r}", "".join(f"Nome de Personagem Bem Comprido {k} −20 casa(s); " for k in range(1, 7)) +
           "".join(f"Operativo de Campo dos Caçadores {k} −3 casa(s); " for k in range(1, 11)) +
           "".join(f"{PIOR_MEMO} −20 casa(s); " for _ in range(6)) +
           "".join(f"Operativo de Campo dos Caçadores {k}: CONGELADO; " for k in range(1, 11)))
    # CONDIÇÕES: a contagem e os Quebrados; o detalhe de cada condição ficou no painel C9b (Fase 4)
    rot(ws, f"A{r + 1}", "CONDIÇÕES", negrito=True)
    queb = "&".join(f'IF({e_("quebr", e)}=1,{s("lab", NPJ + e)}&": Quebrado; ","")' for e in range(1, NIN + 1))
    TOT = f"SUM({_slots_rng('ativa')})"
    N.aux(ws, f"N{r + 1}", f"={queb}", nome="combate.quebrados_txt")
    Q = f"$N${r + 1}"
    cal(ws, f"B{r + 1}", f'=IF({TOT}=0,"Nenhuma ativa",{TOT}&IF({TOT}=1," ativa"," ativas")&": veja o painel C9b, '
                         f'logo abaixo")&IF(LEN({Q})>0,"; "&{Q},"")', nome="combate.condicoes_txt", ate="L")
    N.pior(ws, f"B{r + 1}", "88 ativas: veja o painel C9b, logo abaixo; " +
           "".join(f"Operativo de Campo dos Caçadores {k}: Quebrado; " for k in range(1, 11)))
    rot(ws, f"A{r + 2}", "A Fila não usa medidor de tempo (19.2): a prevista é a remontagem pelas VEL atuais mais os "
                         "pendentes. Quando dois combatentes são movidos no mesmo Ciclo, a ordem segue a chave 2 "
                         f"(casa + Atraso − Avanço): {N.ROTULO_SUGESTAO} (H13); 'Casa manual' vence a calculada.",
        ate="L", italico=True)
    N.reg("combate.h13.rotulo", ws, f"A{r + 2}")
    N.MAPA.sugestoes.append({"h": "H13", "rotulo": N.MapaMestre.ref("Combate", f"A{r + 2}"),
                             "nome": "combate.h13.rotulo", "celulas": []})


def _condicoes(ws):
    titulo(ws, R_C7_TIT, f"C7 · Condições de cada combatente (21.5): {NSLOT} ao mesmo tempo, com os turnos que faltam, "
                         "os acúmulos e o dano pela Eficiência de quem aplicou")
    todos = T("combate.lista.todos")
    for b, r0 in enumerate(R_C7):
        cabs(ws, r0 - 1, {"A": "Combatente", "B": ("Condição", "C"), "D": "Turnos restantes", "E": "Acúmulos",
                          "F": ("Quem aplicou", "G"), "H": ("Efeito e dano", "J"), "K": ("Aviso", "L")})
    for i in range(1, NC + 1):
        LAB = s("lab", i)
        for k in range(1, NSLOT + 1):
            n = slot(i, k)
            r, p = linha_slot(n), f"combate.c{n}"
            cal(ws, f"A{r}", f'=IF(LEN({LAB})>0,{LAB},"{i} · (vazio)")', nome=f"{p}.comb")
            if i > MI0:
                N.pior(ws, f"A{r}", PIOR_MEMO)
            ent(ws, f"B{r}", f"{p}.cond", tipo="lista", fonte="lista.condicoes_combate", ate="C", rotulo="Condição")
            ent(ws, f"D{r}", f"{p}.turnos", tipo="inteiro", minimo=0, maximo=20, rotulo="Turnos", centro=True,
                amostra=2)
            ent(ws, f"E{r}", f"{p}.acum", tipo="inteiro", minimo=0, maximo=5, rotulo="Acúmulos", centro=True, amostra=2)
            ent(ws, f"F{r}", f"{p}.quem", tipo="lista", fonte=todos, ate="G", rotulo="Quem aplicou", opcoes=[])
            CO, QU, AC, TU = T(p + ".cond"), T(p + ".quem"), T(p + ".acum"), T(p + ".turnos")
            put = lambda c, f, r=r, p=p: N.aux(ws, f"{CC[c]}{r}", f, nome=f"{p}.aux.{c}")  # noqa: E731
            a = lambda c, r=r: f"${CC[c]}${r}"  # noqa: E731
            put("ia", f'=IF(LEN({LAB})=0,"",{i})')
            put("it", f'=IF(LEN({QU})=0,"",IFERROR(MATCH({QU},{todos},0),""))')
            put("ef", f'=IF(ISNUMBER({a("it")}),INDEX({srng("ef")},{a("it")}),{T("campanha.ef")})')
            put("pvm", f'=IF(ISNUMBER({a("ia")}),{s("pvmax", i)},0)')
            put("cnd", f'=IF(LEN({CO})=0,"",IFERROR(MATCH({CO},{dcol("condicoes", "Condição")},0),""))')
            for c, col in (("nd", "Nº de dados"), ("fc", "Faces"), ("pa", "Por acúmulo"), ("se", "Soma Eficiência"),
                           ("pct", "% dos PV máximos"), ("tef", "Teto (× Eficiência)"), ("atr", "Atrasa (casas)"),
                           ("tac", "Teto de acúmulos"), ("dc", "Dano Contínuo"), ("efe", "Efeito"),
                           ("dur", "Duração")):
                put(c, f'=IF(ISNUMBER({a("cnd")}),INDEX({dcol("condicoes", col)},{a("cnd")}),"")')
            put("acu", f'=IF(ISNUMBER({AC}),MIN({a("tac")},MAX(1,INT({AC}))),1)')
            ok = f'ISNUMBER({a("cnd")})'
            exp = f'IF(ISNUMBER({TU}),{TU}=0,FALSE)'
            put("ativa", f'=IF(AND({ok},LEN({LAB})>0,{s("vivo", i)}=1,NOT({exp})),1,0)')
            put("ord", f'=IF({a("ativa")}=1,{n},"")')
            dados = f'IF({a("pa")}="Sim",{a("acu")}*{a("nd")},{a("nd")})'
            efx = f'IF({a("se")}="Sim",{a("ef")},0)'
            dano = (f'IF({a("pct")}>0,"Dano Contínuo: "&MIN(INT({a("pct")}*{a("pvm")}/100),{a("tef")}*{a("ef")})&'
                    f'" por turno",IF({a("nd")}>0,IF({a("dc")}="Sim","Dano Contínuo: ","Dano: ")&{dados}&"d"&{a("fc")}&'
                    f'IF({a("se")}="Sim"," + "&{a("ef")},"")&" · média "&(INT({dados}*({a("fc")}+1)/2)+{efx}),'
                    f'{a("efe")}))')
            atr = f'IF({a("atr")}>0,"; Atrasa "&{a("atr")}&" casa(s): some em Atraso deste Ciclo do alvo (C8)","")'
            cal(ws, f"H{r}", f'=IF(NOT({ok}),"",IF({exp},"EXPIRADA (0 turnos): já não vale; apague a condição",'
                             f'{dano}&{atr}))', nome=f"{p}.efeito", ate="J", regra=True)
            N.pior(ws, f"H{r}", "Quem aplicou decide as ações do alvo, sem Habilidade, Ultimate nem recursos; Atrasa 2 "
                                "casa(s): some em Atraso deste Ciclo do alvo (C8)")
            # o texto do painel C9b: o que a condição faz (21.5), o número de agora e a duração do livro
            put("txt", f'=IF({a("ativa")}=0,"",{a("efe")}&IF($H${r}<>{a("efe")}," · Agora: "&$H${r},"")&'
                       f'" (duração: "&{a("dur")}&")")')
            put("expi", f'=IF(AND({ok},LEN({LAB})>0),IF({exp},1,0),0)')
            so_inimigo = i <= NPJ or i > MI0
            cong = (f'IF({CO}="Congelado","Congelado só em inimigo (21.2)",' if so_inimigo else "IF(FALSE,\"\",")
            av(ws, f"K{r}", f"{p}.aviso",
               f'=IF(LEN({CO})=0,"",IF(LEN({LAB})=0,"Combatente vazio: a condição não conta",IF(NOT({ok}),'
               f'"Condição fora do capítulo 21",{cong}IF({exp},"Expirou: os turnos chegaram a 0 e ela saiu do painel",'
               f'IF(AND(ISNUMBER({AC}),{AC}>{a("tac")}),"Acima do teto de "&{a("tac")}&" acúmulo(s) (21.5): usando o '
               f'teto",IF({a("dc")}="Sim","Dano Contínuo: início do turno do alvo; ignora RD, não crita, sem dados de '
               f'Fraqueza (20.6)","")))))))', ate="L")
    for b, r0 in enumerate(R_C7):
        itens = min(12, NC * NSLOT - 12 * b)
        N.subtabela(ws, f"C7.{b + 1}", [r0 - 1], "A:L", itens)
    fim = linha_slot(NC * NSLOT)
    for nome, col in (("comb", "A"), ("cond", "B"), ("turnos", "D"), ("quem", "F")):
        N.reg(f"combate.cond.col.{nome}", ws, f"{col}{R_C7[0]}:{col}{fim}")
    rot(ws, f"A{fim + 1}", "Cura não remove condição (21.1). Duração em turnos do alvo (19.2): no fim do turno do alvo, "
                           "desconte 1 em Turnos restantes; com 0, a condição fica EXPIRADA e sai do painel C9b. Vazio = "
                           "sem contador (dura o que a fonte disser). Quebrado e Morrendo são automáticos (C5 e C2). "
                           "Nenhum alvo acumula mais de 5 instâncias da mesma condição (21.1).", ate="L", italico=True)


def _painel(ws):
    """C9b: todas as condições ativas de uma vez (C3 do pedido): em quem, qual, turnos, acúmulos, quem aplicou e o que
    faz. As ativas são as da C7 com condição do capítulo 21, combatente presente e vivo, e turnos ≠ 0."""
    titulo(ws, R_C9B_TIT, "C9b · Painel de consulta rápida: todas as condições ativas agora e o que cada uma faz (21.5)")
    ORD, ATIVA = _slots_rng("ord"), _slots_rng("ativa")
    ncond = srng("ncond")
    rot(ws, f"A{R_C9B_TIT + 1}", "Agora", negrito=True)
    TOT = f"SUM({ATIVA})"
    NCB = f'COUNTIF({ncond},">0")'
    N.aux(ws, f"N{R_C9B_TIT + 1}", f'=SUM({_slots_rng("expi")})', nome="combate.painel.expiradas")
    EXP = f"$N${R_C9B_TIT + 1}"
    cal(ws, f"B{R_C9B_TIT + 1}",
        f'=IF({TOT}=0,"Nenhuma condição ativa: lance as condições na C7, na linha de cada combatente",{TOT}&IF({TOT}=1,'
        f'" condição ativa"," condições ativas")&" em "&{NCB}&IF({NCB}=1," combatente"," combatentes")&". Cada uma '
        f'está na C7, na linha do combatente")&IF({EXP}>0,". Expirada(s) para apagar na C7: "&{EXP},"")&"."',
        nome="combate.painel.resumo", ate="L", regra=True)
    for r0 in R_C9B:
        cabs(ws, r0 - 1, {"A": "Em quem", "B": ("Condição", "C"), "D": "Turnos restantes", "E": "Acúmulos",
                          "F": ("Quem aplicou", "G"), "H": ("O que faz (21.5) e o número de agora", "L")})
    col = lambda c: T(f"combate.cond.col.{c}")  # noqa: E731
    for k in range(1, NPAINEL + 1):
        r, p = linha_bloco(R_C9B, k), f"combate.painel{k}"
        N.aux(ws, f"N{r}", f'=IF({k}>{TOT},"",MATCH(SMALL({ORD},{k}),{ORD},0))', nome=f"{p}.pos")
        P = f"$N${r}"
        ix = lambda rng, P=P: f"INDEX({rng},{P})"  # noqa: E731
        cal(ws, f"A{r}", f'=IF({P}="","",{ix(col("comb"))})', nome=f"{p}.quem", regra=True)
        cal(ws, f"B{r}", f'=IF({P}="","",{ix(col("cond"))})', nome=f"{p}.cond", ate="C", regra=True)
        cal(ws, f"D{r}", f'=IF({P}="","",IF(ISNUMBER({ix(col("turnos"))}),{ix(col("turnos"))},"sem contador"))',
            nome=f"{p}.turnos", centro=True, regra=True)
        cal(ws, f"E{r}", f'=IF({P}="","",IF({ix(_slots_rng("tac"))}>1,{ix(_slots_rng("acu"))},"—"))',
            nome=f"{p}.acum", centro=True, regra=True)
        cal(ws, f"F{r}", f'=IF({P}="","",IF(LEN({ix(col("quem"))})>0,{ix(col("quem"))},"—"))', nome=f"{p}.aplicou",
            ate="G", regra=True)
        cal(ws, f"H{r}", f'=IF({P}="","",{ix(_slots_rng("txt"))})', nome=f"{p}.efeito", ate="L", regra=True)
        N.pior(ws, f"H{r}", "Só inimigos. Comum perde o turno; Elite e Boss são Atrasados 2 casas e perdem a ação "
                            "especial · Agora: Dano Contínuo: 5d6 + 8 · média 25; Atrasa 2 casa(s): some em Atraso deste "
                            "Ciclo do alvo (C8) (duração: até o fim do próximo turno dele)")
        N.pior(ws, f"A{r}", PIOR_MEMO)
        N.pior(ws, f"F{r}", PIOR_MEMO)
    N.subtabela(ws, "C9b", [r0 - 1 for r0 in R_C9B], "A:L", NPAINEL)
    r = linha_bloco(R_C9B, NPAINEL) + 1
    cal(ws, f"A{r}", f'=IF({TOT}>{NPAINEL},"Mais "&({TOT}-{NPAINEL})&IF({TOT}-{NPAINEL}=1," condição ativa"," '
                     f'condições ativas")&" além destas {NPAINEL}: veja a C7.","")', nome="combate.painel.mais", ate="L",
        regra=True)


def _calculadora(ws):
    r0 = R_C10
    titulo(ws, r0 - 2, "C10 · Calculadora de dano e Tenacidade (23.1, 20.2, 20.3; teto de +3 dados, 16.9/26.6)")
    cabs(ws, r0 - 1, {"A": "Entradas", "B": "Fonte", "C": "Alvo", "D": "Nº de dados base", "E": "Faces",
                      "F": "Bônus fixo", "G": "Elemento", "H": "Crítico?", "I": "Dados extras (0–5)",
                      "J": "Resultado rolado", "K": ("Aviso", "L")})
    rot(ws, f"A{r0}", "Preencha", negrito=True)
    p = "combate.calc"
    ent(ws, f"C{r0}", f"{p}.alvo", tipo="lista", fonte=T("combate.lista.inimigos"), rotulo="Alvo", opcoes=[])
    ent(ws, f"B{r0}", f"{p}.fonte", tipo="lista", fonte="lista.fontes", rotulo="Fonte")
    ent(ws, f"D{r0}", f"{p}.n", tipo="inteiro", minimo=1, maximo=20, rotulo="Nº de dados", centro=True, amostra=2)
    ent(ws, f"E{r0}", f"{p}.f", tipo="inteiro", minimo=2, maximo=20, rotulo="Faces", centro=True, amostra=6)
    ent(ws, f"F{r0}", f"{p}.fixo", tipo="inteiro", minimo=-20, maximo=99, rotulo="Bônus fixo", centro=True, amostra=4)
    ent(ws, f"G{r0}", f"{p}.elem", tipo="lista", fonte="lista.elementos", rotulo="Elemento", centro=True)
    ent(ws, f"H{r0}", f"{p}.crit", tipo="lista", fonte="lista.sim_nao", rotulo="Crítico?", centro=True)
    ent(ws, f"I{r0}", f"{p}.extra", tipo="inteiro", minimo=0, maximo=5, rotulo="Dados extras", centro=True, amostra=1)
    ent(ws, f"J{r0}", f"{p}.rolado", tipo="inteiro", minimo=0, maximo=999, rotulo="Resultado rolado", centro=True,
        amostra=15)
    AL, FO, NN, FF, FX, EL, CR, EX, RO = (T(f"{p}.{k}") for k in ("alvo", "fonte", "n", "f", "fixo", "elem", "crit",
                                                                   "extra", "rolado"))
    a = lambda c: f"${c}${r0 + 1}"  # noqa: E731
    N.aux(ws, a("N"), f'=IF(LEN({AL})=0,"",IFERROR(MATCH({AL},{T("combate.col.rot")},0),""))', nome=f"{p}.ia")
    IA = a("N")
    ok = f"ISNUMBER({IA})"
    vig = "+".join(f'IF(INDEX({T(f"combate.col.v{k}")},{IA})={EL},1,0)' for k in range(1, 5))
    N.aux(ws, a("O"), f'=IF(OR(NOT({ok}),LEN({EL})=0),"neutro",IF(({vig})>0,"Fraqueza",IF(INDEX({T("combate.col.res")},'
                      f'{IA})={EL},"Resistência","neutro")))', nome=f"{p}.sit")
    SIT = a("O")
    N.aux(ws, a("P"), f'=IF({FO}="Dano Contínuo",1,0)', nome=f"{p}.dc")
    DC = a("P")
    base = f'IF(ISNUMBER({NN}),MAX(1,INT({NN})),1)'
    N.aux(ws, a("Q"), f'=IF({DC}=1,{base},MAX(1,{base}*IF({CR}="Sim",2,1)+IF({SIT}="Fraqueza",2,0)-'
                      f'IF({SIT}="Resistência",2,0))+MIN(3,IF(ISNUMBER({EX}),MAX(0,INT({EX})),0)))', nome=f"{p}.dados")
    faces = f'IF(ISNUMBER({FF}),MAX(2,INT({FF})),6)'
    fixo = f'IF(ISNUMBER({FX}),INT({FX}),0)'
    N.aux(ws, a("R"), f'=INT({a("Q")}*({faces}+1)/2)+{fixo}', nome=f"{p}.media")
    N.aux(ws, a("S"), f'=IF(OR(NOT({ok}),{DC}=1),0,INDEX({T("combate.col.rd")},{IA}))', nome=f"{p}.rd")
    N.aux(ws, a("T"), f'=IFERROR(INDEX({dcol("tenacidade", "Redução bruta")},MATCH({FO},{dcol("tenacidade", "Fonte")},'
                      f'0)),0)', nome=f"{p}.bruto")
    BR = a("T")
    N.aux(ws, a("U"), f'=IF({BR}=0,0,IF({SIT}="Fraqueza",{BR},IF({SIT}="Resistência",1,MAX(1,INT({BR}/2)))))',
          nome=f"{p}.red")
    rs = r0 + 2
    cabs(ws, rs - 1, {"A": "Resultado", "B": "Situação", "C": "Dados finais", "D": ("Expressão", "E"),
                      "F": "Média", "G": "RD do alvo", "H": "Dano final", "I": "Redução de Tenacidade",
                      "J": "Tenacidade depois", "K": ("Aviso", "L")})
    rot(ws, f"A{rs}", "Automático", negrito=True)
    vazio = f"OR(NOT({ok}),LEN({FO})=0)"
    cal(ws, f"B{rs}", f'=IF({vazio},"",IF({DC}=1,"Dano Contínuo",{SIT}))', nome=f"{p}.situacao", centro=True,
        regra=True)
    cal(ws, f"C{rs}", f'=IF({vazio},"",{a("Q")})', nome=f"{p}.ndados", centro=True, regra=True)
    cal(ws, f"D{rs}", f'=IF({vazio},"",{a("Q")}&"d"&{faces}&IF({fixo}>0," + "&{fixo},IF({fixo}<0," − "&ABS({fixo}),"")))',
        nome=f"{p}.expr", ate="E", centro=True, regra=True)
    cal(ws, f"F{rs}", f'=IF({vazio},"",{a("R")})', nome=f"{p}.media_v", centro=True, regra=True)
    cal(ws, f"G{rs}", f'=IF({vazio},"",{a("S")})', nome=f"{p}.rd_v", centro=True, regra=True)
    cal(ws, f"H{rs}", f'=IF({vazio},"",MAX(1,IF(ISNUMBER({RO}),{RO},{a("R")})-{a("S")}))', nome=f"{p}.final",
        centro=True, regra=True)
    cal(ws, f"I{rs}", f'=IF({vazio},"",{a("U")})', nome=f"{p}.reducao", centro=True, regra=True)
    cal(ws, f"J{rs}", f'=IF({vazio},"",MAX(0,INDEX({T("combate.col.tenat")},{IA})-{a("U")}))', nome=f"{p}.tendepois",
        centro=True, regra=True)
    av(ws, f"K{rs}", f"{p}.aviso",
       f'=IF({vazio},"",IF(AND(ISNUMBER({EX}),{EX}>3),"Teto de +3 dados adicionais (16.9, 26.6): usando 3",'
       f'IF(AND({DC}=1,OR({CR}="Sim",{SIT}<>"neutro")),"Dano Contínuo não crita, sem dados de Fraqueza e ignora RD '
       f'(20.6)","Só reduz Tenacidade se acertou (20.3)")))', ate="L")
    rot(ws, f"A{rs + 1}", "Ordem de 23.1: dados base; +2 dados por Fraqueza ou −2 por Resistência (mínimo 1 dado); o "
                          "crítico dobra só os dados base; soma o fixo; tira a RD (não em Dano Contínuo); mínimo 1. "
                          "Os dados da Fraqueza ficam fora do teto de +3.", ate="L", italico=True)
    N.subtabela(ws, "C10", [r0 - 1, rs - 1], "A:L", 1)
