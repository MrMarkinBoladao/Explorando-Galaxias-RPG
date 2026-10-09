# -*- coding: utf-8 -*-
"""Aba Combate — inimigos (C3 quem é, C4 PV e fase, C5 Tenacidade, C5b Quebra, C6 recargas). 28.5, 20.2–20.5."""

import mestre_dados as D
from mestre import nucleo as N
from mestre.nucleo import T, ent, cal, av, rot, cabs, titulo, dcol
from mestre.aba_combate_base import NPJ, NIN, R_C3, R_C4, R_C5, R_C5B, R_C6, EC, s, e_, cat

CABS = [
    (R_C3, "C3 · Inimigos — quem é (o inimigo escolhido preenche os próprios dados)",
     {"A": "Inimigo", "B": "Do encontro", "C": "Trocar por (preencha)", "D": "Tipo · faixa", "E": "Teste de Ataque",
      "F": ("Dano por acerto", "G"), "H": "DT · TR", "I": "Firmeza", "J": "Execução"}),
    (R_C4, "C4 · Inimigos — PV e fase do Boss (28.5)",
     {"A": "Inimigo", "B": "Ajuste de VEL", "C": "VEL efetiva", "D": "PV máx.", "E": "PV atual",
      "F": "Dano agora (− = cura)", "G": "PV depois", "H": "Fase da barra", "I": "Fase em vigor", "J": "Defesa atual"}),
    (R_C5, "C5 · Inimigos — Tenacidade e Fraquezas em vigor (20.2–20.4)",
     {"A": "Inimigo", "B": "Tenacidade máx. (fase em vigor)", "C": "Redução acumulada", "D": "Tenacidade atual",
      "E": ("Fraquezas em vigor", "G"), "H": "Resistência", "I": "RD", "J": "Quebrado?"}),
    (R_C5B, "C5b · Quebra: Dano de Quebra e efeito do Elemento (20.4, 20.5)",
     {"A": "Inimigo", "B": "Elemento que quebrou", "C": "Quem quebrou",
      "D": ("Dano de Quebra e efeito (com a Eficiência do grupo)", "J")}),
    (R_C6, "C6 · Inimigos — recargas das ações especiais (28.4)",
     {"A": "Inimigo", "B": "Especial 1", "C": "Usada no Ciclo", "D": "Disponível?", "E": "Especial 2",
      "F": "Usada no Ciclo", "G": "Disponível?", "H": "Especial 3", "I": "Usada no Ciclo", "J": "Disponível?"})]
FONTES = {1: "A", 2: "B", 3: "C", 4: "R"}


def montar(ws):
    for r, t, c in CABS:
        titulo(ws, r - 2, t)
        cabs(ws, r - 1, {**c, "K": ("Aviso", "L")})
        N.subtabela(ws, t.split(" ")[0], [r - 1], "A:L", NIN)
    for e in range(1, NIN + 1):
        _aux(ws, e)
        _linhas(ws, e)
    for k in range(1, 5):
        N.reg(f"combate.col.v{k}", ws, f"{EC[f'v{k}']}{R_C3}:{EC[f'v{k}']}{R_C3 + NIN - 1}")
    for c in ("res", "rd", "tenat", "rot", "nome", "pode"):
        N.reg(f"combate.col.{c}", ws, f"{EC[c]}{R_C3}:{EC[c]}{R_C3 + NIN - 1}")
    r = R_C4 + NIN
    for k, t in enumerate(["Virar a fase do Boss (no fim do turno dele, quando o aviso 'a barra cruzou o limiar' "
                           "acender): (1) digite a fase nova em 'Fase em vigor';",
                           "(2) apague a 'Redução acumulada' dele em C5: a Tenacidade volta ao máximo da fase nova;",
                           "(3) leia em voz alta as Fraquezas novas (C5). A virada não gasta a ação dele (28.5 regra "
                           "5)."]):
        rot(ws, f"A{r + k}", t, ate="L", italico=True)
    rot(ws, f"A{R_C5B + NIN}", "Quebra em 5 passos (20.4): Dano de Quebra + efeito; Atrasa 1 casa (em C8, entra na "
                               "Firmeza); Quebrado até o fim do próximo turno dele (−2 de Defesa, +1 dado de qualquer "
                               "fonte); quem quebrou +10 de Energia (1 por Ciclo); Tenacidade volta ao máximo no fim do "
                               "próximo turno dele (apague a Redução acumulada).", ate="L", italico=True)


def _via(fn):
    out = '""'
    for k in (4, 3, 2, 1):
        out = f'IF({T("combate.src")}={k},{fn(FONTES[k])},{out})'
    return out


def _aux(ws, e):
    r3, p, i = R_C3 + e - 1, f"combate.in{e}", NPJ + e
    put = lambda c, f: N.aux(ws, f"{EC[c]}{r3}", f, nome=f"{p}.aux.{c}")  # noqa: E731
    cum = lambda X: T(f"encontros.{X}.col.cum")  # noqa: E731
    put("dj", "=" + _via(lambda X: f'IF(MAX({cum(X)})>={e},COUNTIF({cum(X)},"<"&{e})+1,"")'))
    DJ = e_("dj", e)
    put("dnome", "=" + _via(lambda X: f'IF(ISNUMBER({DJ}),INDEX({T(f"encontros.{X}.col.nome")},{DJ})&"","")'))
    TROCA = T(f"{p}.troca")
    put("nome", f'=IF(LEN({TROCA})>0,{TROCA},{e_("dnome", e)})')
    put("idx", f'=IF(LEN({e_("nome", e)})=0,"",IFERROR(MATCH({e_("nome", e)},{T("inimigos.cat.nome")},0),""))')
    IX = e_("idx", e)
    ok = f"ISNUMBER({IX})"
    for k in range(1, 5):
        put(f"w{k}", f'=IF(NOT({ok}),"",IF(AND(LEN({TROCA})=0,ISNUMBER({DJ})),'
                     + _via(lambda X: f'INDEX({T(f"encontros.{X}.col.w{k}")},{DJ})&""') + f',{cat(f"f{k}", IX)}))')
    put("fases", f'=IF({ok},MAX(1,{cat("fases", IX)}),1)')
    put("tipo", f'=IF({ok},{cat("tipo", IX)},"")')
    PVA = s("pvat", i)
    put("fb", f'=IF(NOT({ok}),"",IF(AND({e_("fases", e)}>=3,{PVA}<={cat("lim3", IX)}),3,IF(AND({e_("fases", e)}>=2,'
              f'{PVA}<={cat("lim2", IX)}),2,1)))')
    FV = T(f"{p}.fase")
    put("fv", f'=IF(NOT({ok}),"",IF(ISNUMBER({FV}),MIN({e_("fases", e)},MAX(1,INT({FV}))),1))')
    V = e_("fv", e)
    for k in range(1, 5):
        put(f"v{k}", f'=IF(NOT({ok}),"",IF({V}=3,{cat(f"p3f{k}", IX)},IF({V}=2,{cat(f"p2f{k}", IX)},{e_(f"w{k}", e)})))')
    put("res", f'=IF({ok},{cat("res", IX)},"")')
    put("tenmax", f'=IF(NOT({ok}),"",MIN({cat("ten", IX)},IF({V}=3,{cat("ten3", IX)},IF({V}=2,{cat("ten2", IX)},'
                  f'{cat("ten", IX)}))))')
    RED = T(f"{p}.reducao")
    put("tenat", f'=IF(NOT({ok}),"",MAX(0,{e_("tenmax", e)}-IF(ISNUMBER({RED}),MAX(0,INT({RED})),0)))')
    put("quebr", f'=IF(NOT({ok}),0,IF({e_("tenat", e)}=0,1,0))')
    put("defat", f'=IF({ok},{cat("defesa", IX)}-2*{e_("quebr", e)},"")')
    put("rd", f'=IF({ok},{cat("rd", IX)},"")')
    put("ef", f'=IF({ok},{cat("ef", IX)},"")')
    put("exec", f'=IF({ok},{cat("execucao", IX)},"")')
    put("pode", f'=IF(AND({ok},{PVA}>0,{e_("exec", e)}="Pode"),1,0)')
    put("rot", f'={s("lab", i)}')


def _linhas(ws, e):
    r3, r4, r5, r5b, r6 = (R_C3 + e - 1, R_C4 + e - 1, R_C5 + e - 1, R_C5B + e - 1, R_C6 + e - 1)
    p, i = f"combate.in{e}", NPJ + e
    IX = e_("idx", e)
    ok = f"ISNUMBER({IX})"
    PVA, V, FV, RED = s("pvat", i), e_("fv", e), T(f"{p}.fase"), T(f"{p}.reducao")
    lab = f'=IF(LEN({s("lab", i)})>0,{s("lab", i)},"Inimigo {e}")'
    for col, r in (("3", r3), ("4", r4), ("5", r5), ("5b", r5b), ("6", r6)):
        cal(ws, f"A{r}", lab, nome=f"{p}.rot{col}")
    # C3
    cal(ws, f"B{r3}", f'={e_("dnome", e)}', nome=f"{p}.doencontro")
    ent(ws, f"C{r3}", f"{p}.troca", tipo="lista", fonte=T("inimigos.cat.nome"), rotulo="Trocar por",
        opcoes=[f["nome"] for f in D.bestiario()])
    cal(ws, f"D{r3}", f'=IF({ok},{cat("tipo", IX)}&" · "&{cat("faixa", IX)},"")', nome=f"{p}.tipo", centro=True,
        regra=True)
    cal(ws, f"E{r3}", f'=IF({ok},"+"&{cat("ataque", IX)},"")', nome=f"{p}.ataque", centro=True, regra=True)
    cal(ws, f"F{r3}", f'=IF({ok},{cat("dano_e", IX)}&" · média "&{cat("dano_m", IX)},"")', nome=f"{p}.dano_acerto", ate="G",
        regra=True)
    cal(ws, f"H{r3}", f'=IF({ok},"DT "&{cat("dt", IX)}&" · TR +"&{cat("tr", IX)},"")', nome=f"{p}.dt", centro=True,
        regra=True)
    cal(ws, f"I{r3}", f'=IF({ok},{cat("firmeza", IX)},"")', nome=f"{p}.firmeza", centro=True, regra=True)
    cal(ws, f"J{r3}", f'=IF({ok},{e_("exec", e)},"")', nome=f"{p}.execucao", centro=True, regra=True)
    av(ws, f"K{r3}", f"{p}.aviso3",
       f'=IF(AND(LEN({e_("nome", e)})>0,NOT({ok})),"Inimigo fora da lista (Inimigos e Bestiário)",IF(AND({ok},'
       f'{e_("exec", e)}="Não declarado"),"Execução não declarada na ficha: só ser racional Executa (23.5)",""))',
       ate="L")
    # C4
    ent(ws, f"B{r4}", f"{p}.ajvel", tipo="inteiro", minimo=-10, maximo=10, rotulo="Ajuste de VEL", centro=True,
        amostra=2)
    cal(ws, f"C{r4}", f'=IF({ok},{s("vel", i)},"")', nome=f"{p}.vel", centro=True, regra=True)
    cal(ws, f"D{r4}", f'=IF({ok},{s("pvmax", i)},"")', nome=f"{p}.pvmax", centro=True, regra=True)
    ent(ws, f"E{r4}", f"{p}.pv", tipo="inteiro", minimo=0, maximo=999, rotulo="PV atual", centro=True, amostra=10)
    ent(ws, f"F{r4}", f"{p}.dano", tipo="inteiro", minimo=-999, maximo=999, rotulo="Dano agora", centro=True,
        amostra=5)
    DN = T(f"{p}.dano")
    dano = f'IF(ISNUMBER({DN}),INT({DN}),0)'
    cal(ws, f"G{r4}", f'=IF({ok},MIN({s("pvmax", i)},MAX(0,{PVA}-{dano})),"")', nome=f"{p}.pvdepois", centro=True,
        regra=True)
    cal(ws, f"H{r4}", f'=IF({ok},{e_("fb", e)},"")', nome=f"{p}.fasebarra", centro=True, regra=True)
    ent(ws, f"I{r4}", f"{p}.fase", tipo="inteiro", minimo=1, maximo=3, rotulo="Fase em vigor", centro=True)
    cal(ws, f"J{r4}", f'=IF({ok},{e_("defat", e)},"")', nome=f"{p}.defesa", centro=True, regra=True)
    FB, NF = e_("fb", e), e_("fases", e)
    av(ws, f"K{r4}", f"{p}.aviso4",
       f'=IF(NOT({ok}),"",IF({PVA}=0,"Derrotado: remova a casa (19.7)",IF(AND(ISNUMBER({FV}),OR({FV}<1,{FV}>{NF})),'
       f'IF({e_("tipo", e)}="Boss","Fase em vigor fora de 1 a "&{NF}&": usando o limite","Comum e Elite não têm fases '
       f'(28.5)"),IF({V}>{FB},"Fase adiantada: a barra ainda não cruzou o limiar",IF({FB}>{V},"A barra cruzou o limiar '
       f'da fase "&{FB}&". No fim do turno do Boss: digite "&{FB}&" em Fase em vigor, apague a Redução acumulada (a '
       f'Tenacidade volta ao máximo, 28.5 regra 3) e anuncie as Fraquezas novas; a virada não gasta a ação dele",'
       f'"")))))', ate="L")
    # C5
    cal(ws, f"B{r5}", f'=IF({ok},{e_("tenmax", e)},"")', nome=f"{p}.tenmax", centro=True, regra=True)
    ent(ws, f"C{r5}", f"{p}.reducao", tipo="inteiro", minimo=0, maximo=99, rotulo="Redução acumulada", centro=True,
        amostra=2)
    cal(ws, f"D{r5}", f'=IF({ok},{e_("tenat", e)},"")', nome=f"{p}.tenat", centro=True, regra=True)
    vs = [e_(f"v{k}", e) for k in range(1, 5)]
    cal(ws, f"E{r5}", f'=IF({ok},{vs[0]}' + "".join(f'&IF(LEN({x})>0,", "&{x},"")' for x in vs[1:]) + ',"")',
        nome=f"{p}.fraquezas", ate="G", regra=True)
    cal(ws, f"H{r5}", f'=IF({ok},IF(LEN({e_("res", e)})>0,{e_("res", e)},"—"),"")', nome=f"{p}.res", centro=True,
        regra=True)
    cal(ws, f"I{r5}", f'=IF({ok},{e_("rd", e)},"")', nome=f"{p}.rd", centro=True, regra=True)
    cal(ws, f"J{r5}", f'=IF({ok},IF({e_("quebr", e)}=1,"Sim","Não"),"")', nome=f"{p}.quebrado", centro=True, regra=True)
    av(ws, f"K{r5}", f"{p}.aviso5",
       f'=IF(NOT({ok}),"",IF(AND(ISNUMBER({RED}),{RED}<0),"Redução negativa: usando 0",IF({e_("quebr", e)}=1,'
       f'"Quebra! Dano de Quebra em C5b; Atrasa 1 casa; Quebrado até o fim do próximo turno dele; +10 de Energia para '
       f'quem quebrou (20.4)","")))', ate="L")
    # C5b
    ent(ws, f"B{r5b}", f"{p}.elemq", tipo="lista", fonte="lista.elementos", rotulo="Elemento que quebrou", centro=True)
    ent(ws, f"C{r5b}", f"{p}.quemq", tipo="lista", fonte=T("combate.lista.pjs"), rotulo="Quem quebrou", opcoes=[])
    cal(ws, f"D{r5b}", "=" + quebra(T(f"{p}.elemq"), e, ok), nome=f"{p}.danoquebra", ate="J", regra=True)
    N.pior(ws, f"D{r5b}", "Físico: 2d6 + 16 · média 23 (menos RD 8 = 15) + Sangramento (24 por turno, 2 turnos, ignora "
                          "RD). Quebrado até o fim do próximo turno dele: −2 de Defesa e +1 dado; Atrasa 1 casa.")
    av(ws, f"K{r5b}", f"{p}.aviso5b",
       f'=IF(AND({ok},{e_("quebr", e)}=1,LEN({T(f"{p}.elemq")})=0),"Diga o Elemento que quebrou (20.5)","")', ate="L")
    # C6
    CIC = T("combate.ciclo_ef")
    for k, (cn, cu, cd) in enumerate((("B", "C", "D"), ("E", "F", "G"), ("H", "I", "J")), start=1):
        nm = cat(f"esp{k}", IX)
        cal(ws, f"{cn}{r6}", f'=IF({ok},{nm},"")', nome=f"{p}.esp{k}", regra=True)
        ent(ws, f"{cu}{r6}", f"{p}.usada{k}", tipo="inteiro", minimo=1, maximo=99, rotulo="Usada no Ciclo", centro=True)
        U, RC = T(f"{p}.usada{k}"), cat(f"rec{k}", IX)
        cal(ws, f"{cd}{r6}", f'=IF(NOT({ok}),"",IFERROR(IF(LEN({nm})=0,"",IF(NOT(ISNUMBER({U})),"Sim",IF(NOT(ISNUMBER({RC})),'
                             f'"Usada",IF({CIC}>={U}+{RC},"Sim","No Ciclo "&({U}+{RC}))))),""))', nome=f"{p}.disp{k}",
            centro=True, regra=True)
    av(ws, f"K{r6}", f"{p}.aviso6",
       f'=IF(AND({ok},{s("cong", i)}=1,{e_("tipo", e)}<>"Comum"),"Congelado: sem ação especial no turno seguinte '
       f'(19.6)","")', ate="L")


def quebra(EL, e, ok):
    """Texto do Dano de Quebra (20.5) com a Eficiência do grupo e o efeito de Quebra (21.2)."""
    EF = T("campanha.ef")
    lin = f'MATCH({EL},{dcol("elementos", "Elemento")},0)'
    n = f'INDEX({dcol("elementos", "Nº de dados")},{lin})'
    f = f'INDEX({dcol("elementos", "Faces")},{lin})'
    mu = f'INDEX({dcol("elementos", "Multiplicador da Eficiência")},{lin})'
    fixo = f"({mu}*{EF})"
    med = f"(INT({n}*({f}+1)/2)+{fixo})"
    rd = e_("rd", e)
    expr = f'IF({n}>0,{n}&"d"&{f}&" + "&{fixo}&" · média "&{med},{fixo}&"")'
    final = f'" (menos RD "&{rd}&" = "&MAX(1,{med}-{rd})&")"'
    sang = f'MIN(INT(5*{s("pvmax", NPJ + e)}/100),3*{EF})'
    efeito = (f'IF({EL}="Físico"," + Sangramento ("&{sang}&" por turno, 2 turnos, ignora RD)",'
              f'IF({EL}="Fogo"," + Queimadura (2d6 + "&{EF}&" por turno, 2 turnos, ignora RD)",'
              f'IF({EL}="Raio"," + Choque (1d6 + "&{EF}&" por turno, 3 turnos, ignora RD)",'
              f'IF({EL}="Vento"," + Cisalhamento de Vento (1d6 por acúmulo por turno, até 5, 2 turnos)",'
              f'IF({EL}="Gelo",IF({e_("tipo", e)}="Comum"," + Congelamento: perde o turno (19.6)",'
              f'" + Congelamento: Atrasado 2 casas e sem ação especial no turno seguinte (19.6)"),'
              f'IF({EL}="Quântico"," + Embaraço (1d6 por acúmulo, Atrasa 1 casa)",'
              f'IF({EL}="Imaginário"," + Aprisionamento (1d6 + "&{EF}&", Atrasa 2 casas)","")))))))')
    return (f'IF(OR(NOT({ok}),LEN({EL})=0),"",IFERROR({EL}&": "&{expr}&{final}&{efeito}&". Quebrado até o fim do '
            f'próximo turno dele: −2 de Defesa e +1 dado; Atrasa 1 casa.",""))')
