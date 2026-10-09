# -*- coding: utf-8 -*-
"""
Aba Recompensas — Gerador de Recompensas (R7, design §6.12).

1. Entrega de marco, REGRA sem sorteio (24.5, 25.1–25.3, 26.1, 26.7, 27.8): verba de marco do nível, Cone de Luz
   máximo e Tier de Relíquia (viradas no 7, 13 e 18), Bônus Maior do Cone, Ressonância, Sobreposição (≤ 1 por faixa,
   e o teto do Cone pelo Nível, contando as de faixas anteriores) com as do grupo (aba Grupo, G3), slot novo, o que
   não dar e os preços de referência.
2. Achados de encontro, G = 400: créditos (5/10/15% da verba, H18), 0 a 2 consumíveis de 24.3 pela faixa (H9),
   bugiganga e pista; linha de saída na ordem do Tesouro (D6).
3. Sabor de Cone de Luz (G = 410) e de Conjunto de Relíquias (G = 420), com os números de 25.2/25.3.
4. Tesouro do grupo: 25 linhas e o saldo de Créditos.
"""

import mestre_dados as D
from mestre import nucleo as N
from mestre import sorteio as S
from mestre import historia as H
from mestre.nucleo import T, q, ent, cal, av, rot, cabs, titulo, dcol, sugestao, sugestao_formula

NPJ = 6
NT = 25          # linhas do Tesouro
R_ACHADOS = 80


def montar(wb):
    ws = wb["Recompensas"]
    _marco(ws)
    r = _sobreposicao(ws, 23)
    r = _nao_dar(ws, r + 1)
    r = _precos(ws, r + 1)
    r = _achados(ws, max(r + 1, R_ACHADOS))
    r = _cone(ws, r + 1)
    r = _conjunto(ws, r + 1)
    _tesouro(ws, r + 1)


def _ne(col, ef):
    return f'INDEX({dcol("nivel_equipamento", col)},{ef})'


def _marco(ws):
    titulo(ws, 5, "Entrega de marco (regra do livro, sem sorteio: 25.1 e 27.8)")
    cabs(ws, 6, {"A": "Campo", "B": ("Valor (preencha)", "C"), "D": ("O que a planilha usa (automático)", "J"),
                 "K": ("Aviso", "L")})
    rot(ws, "A7", "Nível novo do grupo", negrito=True)
    ent(ws, "B7", "recompensas.nivel", tipo="inteiro", minimo=1, maximo=20, ate="C", rotulo="Nível novo",
        centro=True, amostra=2)
    NV = T("recompensas.nivel")
    a = lambda r, f, nome: N.aux(ws, f"N{r}", f, nome=f"recompensas.g.{nome}")  # noqa: E731
    g = lambda nome: T(f"recompensas.g.{nome}")  # noqa: E731
    a(7, f'=IF(ISNUMBER({NV}),MIN(20,MAX(1,INT({NV}))),{T("campanha.nivel_ef")})', "ef")
    EF = g("ef")
    cal(ws, "D7", f'=IF(ISNUMBER({NV}),"Nível "&{EF}&".","Vazio: o nível da aba Campanha ("&{EF}&").")', ate="J")
    av(ws, "K7", "recompensas.aviso.nivel",
       f'=IF(LEN({NV})=0,"",IF(NOT(ISNUMBER({NV})),"Nível não é número: usando o da aba Campanha",'
       f'IF(OR({NV}<1,{NV}>20,INT({NV})<>{NV}),"Nível fora de 1 a 20: usando o limite","")))', ate="L")
    rot(ws, "A8", "O que aconteceu", negrito=True)
    ent(ws, "B8", "recompensas.marco", tipo="lista", fonte="lista.marco", ate="C", rotulo="O que aconteceu")
    MC = T("recompensas.marco")
    cal(ws, "D8", f'=IF({MC}="Fim de arco","Fim de arco: o grupo sobe de nível junto, ao concluir um arco (26.1).",'
                  f'IF({MC}="Entrou em faixa nova","Faixa nova: Cone e Tier da faixa entram agora (25.1).",'
                  f'"Subir de nível acontece fora de combate, num momento de respiro (26.1)."))', ate="J")
    av(ws, "K8", "recompensas.aviso.marco",
       f'=IF(AND(LEN({MC})>0,COUNTIF({N.dlista("marco")},{MC})=0),"Fora da lista: escolha o que aconteceu",'
       f'IF(AND({MC}="Entrou em faixa nova",{_ne("Primeiro nível da faixa", EF)}="Não"),"O nível "&{EF}&" não é o '
       f'primeiro de uma faixa (1, 5, 9, 13, 17)",""))', ate="L")
    titulo(ws, 10, "O que entra neste marco (automático)")
    cabs(ws, 11, {"A": "Campo", "B": ("Valor", "C"), "D": ("Regra e fonte", "J"), "K": ("Aviso", "L")})
    a(8, "=" + _ne("Faixa", EF), "fx")
    a(9, "=" + _ne("Cone de Luz máximo (Nível)", EF), "cone")
    a(10, "=" + _ne("Tier de Relíquia", EF), "tier")
    a(11, "=" + _ne("Ressonância", EF), "res")
    a(12, f'=OR({_ne("Primeiro nível da faixa", EF)}="Sim",{MC}="Entrou em faixa nova")', "faixa_nova")
    CONE = g("cone")
    linhas = [
        ("nivel_ef", "Nível efetivo", f"={EF}", f'="Vazio = nível da aba Campanha (D9). Sem experiência: a progressão '
                                                f'é por marco narrativo (26.1)."'),
        ("faixa", "Faixa", f'={g("fx")}', '="26.3"'),
        ("verba", "Verba de marco (Cr)", "=" + _ne("Verba de marco (Cr)", EF),
         f'="Para o grupo, por nível ganho (24.5). O que ela compra: "&'
         f'{N.dbusca("verba", "Faixa", g("fx"), "O que ela compra")}&"."'),
        ("cone", "Cone de Luz máximo", f'="Nível "&{CONE}',
         f'=IF({g("faixa_nova")},"Faixa nova: cada personagem pode trocar o Cone pelo Nível "&{CONE}&" (25.1). '
         f'Trocar é opcional: Nível maior não é automaticamente melhor (25.2).","Mesmo Cone máximo da faixa (25.1).")'),
        ("bonus", "Bônus Maior do Cone", f'=INDEX({dcol("cone", "Bônus Maior")},{CONE})',
         f'="Efeito Condicional: "&INDEX({dcol("cone", "Efeito Condicional")},{CONE})&" (25.2)."'),
        ("tier", "Tier de Relíquia", f'={g("tier")}',
         f'=IF({_ne("Tier novo neste nível", EF)}="Sim","Tier novo: cada personagem recebe o "&{g("tier")}&" nos slots '
         f'que já possui (25.1).","Mesmo Tier (viradas nos níveis 7, 13 e 18; 25.1 e 25.3).")'),
        ("ressonancia", "Ressonância", f'={g("res")}',
         f'=IF({g("res")}="—","Só nos níveis 5, 10, 15 e 20 (26.7).",INDEX({dcol("ressonancias", "O que ela dá")},'
         f'MATCH({g("res")},{dcol("ressonancias", "Ressonância")},0))&". Marco de história, escolhida na hora com o '
         f'Mestre, e não muda (26.7).")'),
        ("sobreposicao", "Sobreposição", '="No máximo 1 por faixa"',
         '="Decisão sua, como marco narrativo; o teto é do Cone e conta as de faixas anteriores: Nível 1 ou 2, 2; '
         'Nível 3 ou 4, 1; Nível 5, nenhuma (25.2, 27.8)."'),
        ("slot", "Slot de Relíquia novo", '="Quando a história entrega"', '="Decisão sua (25.1, 27.8)."'),
        ("ritmo", "Ritmo de sessões", f'=IF({EF}<=8,"2 a 4 sessões por nível","4 a 6 sessões por nível")',
         '="Ritmo sugerido pelo livro: 2 a 4 sessões por nível nos níveis 1 a 8; 4 a 6 daí em diante (26.1)."'),
    ]
    for k, (campo, rotulo, valor, regra) in enumerate(linhas):
        r = 12 + k
        rot(ws, f"A{r}", rotulo, negrito=True)
        cal(ws, f"B{r}", valor, nome=f"recompensas.marco.{campo}", ate="C", centro=True,
            regra=campo not in ("sobreposicao", "slot"))
        cal(ws, f"D{r}", regra, nome=f"recompensas.marco.{campo}.regra", ate="J", regra=campo in ("cone", "tier",
                                                                                                 "ressonancia", "bonus"))
    N.subtabela(ws, "recompensas.marco", [11], "A:L", len(linhas))


def _sobreposicao(ws, r0):
    # 25.2 fixa dois limites independentes: no máximo 1 por faixa e o teto do Cone (2 no Nível 1–2, 1 no 3–4, 0 no
    # 5), que conta as Sobreposições de faixas anteriores (trocar de Cone é opcional, E14)
    titulo(ws, r0, "Sobreposições do grupo (25.2: no máximo 1 por faixa; o teto é do Cone; números da aba Grupo, G3)")
    cabs(ws, r0 + 1, {"A": "PJ", "B": "Nível do Cone", "C": "Nesta faixa (máx. 1)", "D": "No Cone (total)",
                      "E": ("Teto do Cone", "F"), "G": ("Situação", "J"), "K": ("Aviso", "L")})
    for i in range(1, NPJ + 1):
        r = r0 + 1 + i
        p, pr = f"grupo.pj{i}", f"recompensas.sob.{i}"
        NM, C, SO, TO = T(f"{p}.nome"), T(f"{p}.cone"), T(f"{p}.sobrep"), T(f"{p}.sobrep_total")
        cal(ws, f"A{r}", f'=IF(LEN({NM})>0,{NM},"PJ {i}")', nome=f"{pr}.pj")
        cal(ws, f"B{r}", f'=IF(ISNUMBER({C}),{C},"")', nome=f"{pr}.cone", centro=True)
        cal(ws, f"C{r}", f'=IF(ISNUMBER({SO}),{SO},IF(LEN({NM})>0,0,""))', nome=f"{pr}.sobrep", centro=True)
        # total no Cone: o informado, e nunca menos que as desta faixa
        cal(ws, f"D{r}", f'=IF(OR(LEN({NM})>0,ISNUMBER({TO}),ISNUMBER({SO})),MAX(IF(ISNUMBER({TO}),{TO},0),'
                         f'IF(ISNUMBER({SO}),{SO},0)),"")', nome=f"{pr}.total", centro=True)
        teto = f'IF(AND(ISNUMBER({C}),{C}>=1,{C}<=5),INDEX({dcol("cone", "Sobreposições até o teto")},INT({C})),"")'
        cal(ws, f"E{r}", "=" + teto, nome=f"{pr}.teto", ate="F", centro=True, regra=True)
        TT, TOT = T(f"{pr}.teto"), T(f"{pr}.total")
        cal(ws, f"G{r}", f'=IF(LEN({NM})=0,"",IF(NOT(ISNUMBER({TT})),"Preencha o Nível do Cone (1 a 5) na aba Grupo",'
                         f'IF({TT}=0,"Cone no teto (+3): nenhuma Sobreposição (25.2)",IF({TOT}>={TT},'
                         f'"Cone no teto (+3) com as que já tem: nenhuma a mais (25.2)",IF(AND(ISNUMBER({SO}),{SO}>=1),'
                         f'"Já recebeu a desta faixa (máximo 1 por faixa, 25.2)","Pode receber 1 nesta faixa, se a '
                         f'história entregar (25.2)")))))', nome=f"{pr}.situacao", ate="J", regra=True)
        resto = (f'IF(AND(ISNUMBER({SO}),{SO}>1),"Mais de 1 Sobreposição nesta faixa (25.2)",'
                 f'IF(AND(ISNUMBER({TO}),ISNUMBER({SO}),{TO}<{SO}),"Total no Cone menor que as desta faixa: confira '
                 f'na aba Grupo",""))')
        av(ws, f"K{r}", f"{pr}.aviso",
           f'=IF(AND(ISNUMBER({TT}),ISNUMBER({TOT})),IF({TOT}>{TT},"Acima do teto do Cone: o Nível "&INT({C})&'
           f'" aceita até "&{TT}&" (25.2)",{resto}),{resto})', ate="L")
    r = r0 + NPJ + 2
    rot(ws, f"A{r}", "Total do grupo", negrito=True)
    cal(ws, f"B{r}", "=" + "+".join(f'IF(ISNUMBER({T(f"recompensas.sob.{i}.sobrep")}),'
                                    f'{T(f"recompensas.sob.{i}.sobrep")},0)' for i in range(1, NPJ + 1)),
        nome="recompensas.sob.total", ate="C", centro=True, regra=True)
    rot(ws, f"D{r}", "Sobreposições já recebidas nesta faixa (Sobreposição não é comprada nem sorteada, 25.2).",
        ate="J")
    N.subtabela(ws, "recompensas.sob", [r0 + 1], "A:L", NPJ)
    return r + 1


def _nao_dar(ws, r0):
    titulo(ws, r0, "O que não dar, por mais tentador que pareça (27.8)")
    for k, item in enumerate(D.nao_dar()):
        rot(ws, f"A{r0 + 1 + k}", "• " + item, ate="L")
    r = r0 + 1 + len(D.nao_dar())
    rot(ws, f"A{r}", "Não existe compra de Relíquia, não existe sorteio e não existe economia de equipamento (25.1, "
                     "27.8). Amarre cada entrega ao Propósito de Vida de alguém: o Cone novo é uma memória que alguém "
                     "confia a um personagem; o Tier novo é a oficina da nave recalibrando as peças (27.8).", ate="L",
        italico=True)
    return r + 1


def _precos(ws, r0):
    titulo(ws, r0, "Preços de referência (24.1 a 24.3): os preços não escalam (24.5)")
    tabelas = [
        ("Armaduras e armas", [("armaduras", "Tipo", lambda i: f'"Armadura "&INDEX({dcol("armaduras", "Tipo")},{i})',
                                lambda i: f'"Defesa +"&INDEX({dcol("armaduras", "Defesa")},{i})&IF(INDEX('
                                          f'{dcol("armaduras", "Outros efeitos")},{i})="—","","; "&INDEX('
                                          f'{dcol("armaduras", "Outros efeitos")},{i}))', "24.1"),
                               ("armas", "Categoria", lambda i: f'"Arma "&INDEX({dcol("armas", "Categoria")},{i})',
                                lambda i: f'INDEX({dcol("armas", "Dados base")},{i})&", "&INDEX({dcol("armas", "Alcance")},'
                                          f'{i})&", "&INDEX({dcol("armas", "Atributo de Ataque")},{i})', "24.2")]),
        ("Poções de Vida", [("pocoes", "Poção", lambda i: f'"Poção "&INDEX({dcol("pocoes", "Poção")},{i})',
                             lambda i: f'"Cura "&INDEX({dcol("pocoes", "Cura")},{i})&" (fixa)"', "24.3")]),
        ("Itens comuns", [("itens", "Item", lambda i: f'INDEX({dcol("itens", "Item")},{i})',
                           lambda i: f'INDEX({dcol("itens", "Para quê")},{i})', "24.3")]),
    ]
    r = r0 + 1
    for tit, partes in tabelas:
        cabs(ws, r, {"A": (tit, "B"), "C": ("O que é", "H"), "I": "Espaço", "J": "Preço (Cr)"})
        cab0 = r
        r += 1
        n = 0
        for bloco, chave, fnome, fdesc, sec in partes:
            nb = N.MAPA.blocos[f"dados.{bloco}"]["linhas"]
            for i in range(1, nb + 1):
                cal(ws, f"A{r}", "=" + fnome(i), nome=f"recompensas.preco.{bloco}.{i}.item", ate="B")
                cal(ws, f"C{r}", "=" + fdesc(i), nome=f"recompensas.preco.{bloco}.{i}.desc", ate="H")
                cal(ws, f"I{r}", f'=INDEX({dcol(bloco, "Espaço")},{i})', nome=f"recompensas.preco.{bloco}.{i}.espaco",
                    centro=True, regra=True)
                cal(ws, f"J{r}", f'=INDEX({dcol(bloco, "Preço (Cr)")},{i})',
                    nome=f"recompensas.preco.{bloco}.{i}.preco", centro=True, regra=True)
                r += 1
                n += 1
        N.subtabela(ws, f"recompensas.precos.{tit}", [cab0], "A:L", n)
        r += 1
    return r


def _achados(ws, r0):
    titulo(ws, r0, "Achados de encontro (G = 400): faixa vazia = a do grupo; leitura vazia = Típico")
    cabs(ws, r0 + 1, {"A": "Rolagem nº", "B": "Faixa", "C": ("Leitura do encontro", "D"),
                      "E": ("Rolagem efetiva", "F"), "G": ("Quando usar", "J"), "K": ("Aviso", "L")})
    re_ = r0 + 2
    ent(ws, f"A{re_}", "recompensas.ach.rolagem", tipo="inteiro", minimo=1, maximo=1000000, rotulo="Rolagem nº",
        centro=True, amostra=3)
    ent(ws, f"B{re_}", "recompensas.ach.faixa", tipo="lista", fonte="lista.faixas", rotulo="Faixa", centro=True)
    ent(ws, f"C{re_}", "recompensas.ach.leitura", tipo="lista", fonte="lista.leitura", ate="D",
        rotulo="Leitura do encontro")
    cal(ws, f"E{re_}", S.rolagem_efetiva(T("recompensas.ach.rolagem")), nome="recompensas.ach.rolagem_ef", ate="F",
        centro=True)
    rot(ws, f"G{re_}", "Depois de um encontro, se a cena pedir algo no chão. A leitura é a da aba Encontros (H6).",
        ate="J", italico=True)
    FA, LE = T("recompensas.ach.faixa"), T("recompensas.ach.leitura")
    av(ws, f"K{re_}", "recompensas.ach.aviso",
       f'=IF(LEN({S.aviso_rolagem(T("recompensas.ach.rolagem"))[1:]})>0,'
       f'{S.aviso_rolagem(T("recompensas.ach.rolagem"))[1:]},IF(AND(LEN({FA})>0,LEN({N.faixa_da_lista(FA)})=0),'
       f'"Faixa fora da lista: usando a do grupo",IF(AND(LEN({LE})>0,COUNTIF({N.dlista("leitura")},{LE})=0),'
       f'"Leitura fora da lista: usando Típico","")))', ate="L")
    xs = H.campos(ws, 400, "recompensas.ach.rolagem_ef", 10, "AA", ["faixa (vazia = do grupo)",
                                                                  "leitura de dificuldade (vazia = Típico)"])
    a = lambda r, f, nome: N.aux(ws, f"O{r}", f, nome=f"recompensas.ach.g.{nome}")  # noqa: E731
    g = lambda nome: T(f"recompensas.ach.g.{nome}")  # noqa: E731
    fl = N.faixa_da_lista(FA)
    a(10, f'=IF(LEN({fl})>0,{fl},{T("campanha.faixa")})', "fx")
    a(11, f'=MATCH({g("fx")},{dcol("faixas", "Faixa")},0)', "fi")
    a(12, f'=IF({LE}="Passagem",5,IF({LE}="Pesado",15,10))', "fator")
    a(13, f'=INDEX({dcol("verba", "Verba de marco (Cr)")},{g("fi")})', "verba")
    a(14, f'=INT({g("verba")}*{g("fator")}/100)', "creditos")
    a(15, "=" + S.inteiro(xs[1], 0, 2), "qtd")
    ncf = f'INDEX({dcol("consumiveis_faixa", "Nº de consumíveis")},{g("fi")})'
    a(16, f"={ncf}", "nc")
    a(17, "=" + S.escolha(xs[2], g("nc")), "j1")
    a(18, "=" + S.segundo_sem_repetir(xs[3], g("nc"), g("j1")), "j2")
    for k in (1, 2):
        a(18 + k, "=" + H.escolher(g("fi"), [f'MATCH({g(f"j{k}")},{dcol("consumiveis", f"Ordem {fx}")},0)'
                                            for fx in D.FAIXAS]), f"l{k}")
        a(20 + k, f'=IF({g("qtd")}>={k},INDEX({dcol("consumiveis", "Item")},{g(f"l{k}")}),"")', f"item{k}")
        a(22 + k, f'=IF({g("qtd")}>={k},INDEX({dcol("consumiveis", "Preço (Cr)")},{g(f"l{k}")}),"")', f"preco{k}")
    a(25, "=" + H.sorteia("bugiganga", xs[4]), "bugiganga")
    a(26, "=" + H.sorteia("pista", xs[5]), "pista")
    r = re_ + 2
    cabs(ws, r, {"A": "Achado", "B": ("O quê", "F"), "G": "Quantidade", "H": "Valor (Cr)", "I": ("De onde vem", "J"),
                 "K": ("Aviso", "L")})
    S_ = N.ROTULO_SUGESTAO
    linhas = [
        ("creditos", "Créditos", '="Créditos achados"', "=1", f'={g("creditos")}',
         f'={g("fator")}&"% da verba de marco da faixa "&{g("fx")}&" (24.5) · {S_} (H18)"'),
        ("qtd", "Consumíveis", '="Quantos consumíveis o encontro deixa"', f'={g("qtd")}', '=""',
         f'="0 a 2, uniforme · {S_} (H9)"'),
        ("item1", "Consumível 1", f'={g("item1")}', f'=IF(LEN({g("item1")})>0,1,"")', f'={g("preco1")}',
         f'=IF(LEN({g("item1")})>0,"24.3 (preço de referência), faixa "&{g("fx")},"")'),
        ("item2", "Consumível 2", f'={g("item2")}', f'=IF(LEN({g("item2")})>0,1,"")', f'={g("preco2")}',
         f'=IF(LEN({g("item2")})>0,"24.3 (preço de referência), faixa "&{g("fx")},"")'),
        ("bugiganga", "Bugiganga", f'={g("bugiganga")}', f'=IF(LEN({g("bugiganga")})>0,1,"")', '="—"',
         '="Tabelas: Bugiganga"'),
        ("pista", "Pista ou informação", f'={g("pista")}', '=""', '="—"', '="Tabelas: Pista"'),
    ]
    for k, (campo, rotulo, oque, qt, valor, origem) in enumerate(linhas):
        rr = r + 1 + k
        rot(ws, f"A{rr}", rotulo, negrito=True)
        cal(ws, f"B{rr}", oque, nome=f"recompensas.ach.{campo}", ate="F")
        cal(ws, f"G{rr}", qt, nome=f"recompensas.ach.{campo}.qtd", centro=True, regra=campo == "qtd")
        cal(ws, f"H{rr}", valor, nome=f"recompensas.ach.{campo}.valor", centro=True, regra=campo in (
            "creditos", "item1", "item2"))
        cal(ws, f"I{rr}", origem, nome=f"recompensas.ach.{campo}.origem", ate="J")
        if "(H" in origem:
            sugestao_formula(f"recompensas.ach.{campo}.origem", "H18" if campo == "creditos" else "H9",
                             [f"H{rr}" if campo == "creditos" else f"G{rr}"])
    av(ws, f"K{r + 5}", "recompensas.ach.aviso.bugiganga",
       f'=IF({H.n("bugiganga")}<=0,"Lista \'Bugiganga\' está vazia (aba Tabelas)","")', ate="L")
    av(ws, f"K{r + 6}", "recompensas.ach.aviso.pista",
       f'=IF({H.n("pista")}<=0,"Lista \'Pista\' está vazia (aba Tabelas)","")', ate="L")
    rr = r + 1 + len(linhas)
    rot(ws, f"A{rr}", "Créditos são preço de referência, não economia; nada no balanceamento depende deles (24.5). "
                      "Equipamento de faixa (Cone, Tier) só por marco (25.1).", ate="L", italico=True)
    # linha de saída na ordem do Tesouro (D6)
    rr += 2
    titulo(ws, rr, "Linha de saída: copie A:J e cole como valores no Tesouro (Colar especial → Somente valores)")
    rr += 1
    _cab_tesouro(ws, rr)
    SES = T("campanha.sessao")
    saidas = [("creditos", '"Créditos (achados)"', "1", g("creditos"), '"Achado de encontro (24.5; H18)"'),
              ("item1", g("item1"), f'IF(LEN({g("item1")})>0,1,"")', '""',
               f'IF(LEN({g("item1")})>0,"Preço de referência "&{g("preco1")}&" Cr (24.3)","")'),
              ("item2", g("item2"), f'IF(LEN({g("item2")})>0,1,"")', '""',
               f'IF(LEN({g("item2")})>0,"Preço de referência "&{g("preco2")}&" Cr (24.3)","")'),
              ("bugiganga", g("bugiganga"), f'IF(LEN({g("bugiganga")})>0,1,"")', '""', '"Bugiganga, sem preço"')]
    for k, (campo, item, qt, valor, nota) in enumerate(saidas):
        x = rr + 1 + k
        cal(ws, f"A{x}", f'=IF(ISNUMBER({SES}),{SES},"")', nome=f"recompensas.ach.saida{k + 1}.sessao", centro=True)
        cal(ws, f"B{x}", "=" + item, nome=f"recompensas.ach.saida{k + 1}.item", ate="D")
        cal(ws, f"E{x}", "=" + qt, nome=f"recompensas.ach.saida{k + 1}.qtd", centro=True)
        cal(ws, f"F{x}", "=" + valor, nome=f"recompensas.ach.saida{k + 1}.valor", centro=True, regra=campo == "creditos")
        cal(ws, f"G{x}", '="Grupo"', nome=f"recompensas.ach.saida{k + 1}.quem", ate="H")
        cal(ws, f"I{x}", "=" + nota, nome=f"recompensas.ach.saida{k + 1}.notas", ate="J")
    return rr + len(saidas) + 1


def _cab_tesouro(ws, r):
    cabs(ws, r, {"A": "Sessão", "B": ("Item ou Créditos", "D"), "E": "Quantidade",
                 "F": "Créditos (+ entra, − sai)", "G": ("Com quem", "H"), "I": ("Notas", "J"), "K": ("Aviso", "L")})


def _cone(ws, r0):
    titulo(ws, r0, "Sabor de Cone de Luz (G = 410): faixa vazia = a do grupo", ate="J")
    sugestao(ws, f"K{r0}", "H11", "recompensas.cone.h11", ate="L")
    cabs(ws, r0 + 1, {"A": "Rolagem nº", "B": "Faixa", "C": ("Rolagem efetiva", "D"), "E": ("Como usar", "J"),
                      "K": ("Aviso", "L")})
    re_ = r0 + 2
    ent(ws, f"A{re_}", "recompensas.cone.rolagem", tipo="inteiro", minimo=1, maximo=1000000, rotulo="Rolagem nº",
        centro=True, amostra=3)
    ent(ws, f"B{re_}", "recompensas.cone.faixa", tipo="lista", fonte="lista.faixas", rotulo="Faixa", centro=True)
    cal(ws, f"C{re_}", S.rolagem_efetiva(T("recompensas.cone.rolagem")), nome="recompensas.cone.rolagem_ef", ate="D",
        centro=True)
    rot(ws, f"E{re_}", "Sabor sorteado; o Cone é recompensa de marco escrita com o jogador (25.1, 25.2).", ate="J",
        italico=True)
    FA = T("recompensas.cone.faixa")
    av(ws, f"K{re_}", "recompensas.cone.aviso",
       f'=IF(LEN({S.aviso_rolagem(T("recompensas.cone.rolagem"))[1:]})>0,'
       f'{S.aviso_rolagem(T("recompensas.cone.rolagem"))[1:]},IF(AND(LEN({FA})>0,LEN({N.faixa_da_lista(FA)})=0),'
       f'"Faixa fora da lista: usando a do grupo",""))', ate="L")
    xs = H.campos(ws, 410, "recompensas.cone.rolagem_ef", 20, "AA", ["faixa (vazia = do grupo)",
                                                                   "listas tab.cone_*"])
    a = lambda r, f, nome: N.aux(ws, f"O{r}", f, nome=f"recompensas.cone.g.{nome}")  # noqa: E731
    g = lambda nome: T(f"recompensas.cone.g.{nome}")  # noqa: E731
    fl = N.faixa_da_lista(FA)
    a(30, f'=IF(LEN({fl})>0,{fl},{T("campanha.faixa")})', "fx")
    a(31, f'=MATCH({g("fx")},{dcol("faixas", "Faixa")},0)', "nivel")
    a(32, "=" + H.sorteia("cone_nome_a", xs[1]), "a")
    a(33, "=" + H.sorteia("cone_nome_b", xs[2]), "b")
    a(34, f'=IF(LEN({g("b")})=0,{g("a")},{g("a")}&" "&{g("b")})', "nome")
    a(35, "=" + H.sorteia("cone_memoria", xs[3]), "memoria")
    a(36, f'=INDEX({dcol("bonus_maior", "Bônus Maior")},{S.escolha(xs[4], 10)})', "bm")
    a(37, "=" + S.escolha(xs[5], H.n("cone_gatilho")), "i1")
    a(38, f'=IF({H.n("cone_gatilho")}<=0,"",{H.k_esimo("cone_gatilho", g("i1"))})', "g1")
    a(39, "=" + H.sorteia_sem_repetir("cone_gatilho", xs[6], g("i1")), "g2")
    NV = g("nivel")
    linhas = [
        ("nome", "Nome do Cone", f'={g("nome")}', '="Tabelas: Nome do Cone (início + fim)"'),
        ("nivel", "Nível do Cone", f'="Nível "&{NV}', f'="Cone de Luz máximo da faixa "&{g("fx")}&" (25.1)"'),
        ("memoria", "Memória que carrega", f'={g("memoria")}', '="Tabelas: Memória do Cone"'),
        ("bonus", "Bônus Maior", f'={g("bm")}&": "&INDEX({dcol("cone", "Bônus Maior")},{NV})',
         '="Escolha de 25.2; número pela tabela de 25.2. Permanente e fora do teto (25.2)."'),
        ("efeito", "Efeito Condicional", f'=IF({NV}>=4,"Dois efeitos: "&{g("g1")}&"; "&{g("g2")},{g("g1")})&" — "&'
                                         f'INDEX({dcol("cone", "Efeito Condicional")},{NV})',
         '="Gatilho: Tabelas (os 6 primeiros são os de 25.2). Temporário, entra no teto (25.2)."'),
        ("sobreposicao", "Sobreposição", f'="Até "&INDEX({dcol("cone", "Sobreposições até o teto")},{NV})&'
                                         f'" neste Nível (parte numérica até +3; PV até +"&'
                                         f'INDEX({dcol("cone", "PV no teto")},{NV})&"); no máximo 1 por faixa"',
         '="25.2: cada Sobreposição soma +1 e +10 PV ao Bônus Maior."'),
    ]
    return _tabela_res(ws, re_ + 2, "recompensas.cone", linhas, {"nome": ("cone_nome_a", "Nome do Cone (início)"),
                                                                 "memoria": ("cone_memoria", "Memória do Cone"),
                                                                 "efeito": ("cone_gatilho", "Gatilho")},
                       regra=("nivel", "bonus", "sobreposicao"))


def _tabela_res(ws, r, prefixo, linhas, vazias, regra=()):
    cabs(ws, r, {"A": "Campo", "B": ("Sorteado", "H"), "I": ("De onde vem", "J"), "K": ("Aviso", "L")})
    for k, (campo, rotulo, valor, origem) in enumerate(linhas):
        rr = r + 1 + k
        rot(ws, f"A{rr}", rotulo, negrito=True)
        cal(ws, f"B{rr}", valor, nome=f"{prefixo}.{campo}", ate="H", regra=campo in regra)
        cal(ws, f"I{rr}", origem, nome=f"{prefixo}.{campo}.origem", ate="J")
        if campo in vazias:
            id_, tit = vazias[campo]
            av(ws, f"K{rr}", f"{prefixo}.aviso.{campo}",
               f'=IF({H.n(id_)}<=0,"Lista \'{tit}\' está vazia (aba Tabelas)","")', ate="L")
    return r + len(linhas) + 1


def _conjunto(ws, r0):
    titulo(ws, r0, "Sabor de Conjunto de Relíquias (G = 420)", ate="J")
    sugestao(ws, f"K{r0}", "H11", "recompensas.conj.h11", ate="L")
    cabs(ws, r0 + 1, {"A": "Rolagem nº", "B": ("Rolagem efetiva", "C"), "D": ("Como usar", "J"), "K": ("Aviso", "L")})
    re_ = r0 + 2
    ent(ws, f"A{re_}", "recompensas.conj.rolagem", tipo="inteiro", minimo=1, maximo=1000000, rotulo="Rolagem nº",
        centro=True, amostra=3)
    cal(ws, f"B{re_}", S.rolagem_efetiva(T("recompensas.conj.rolagem")), nome="recompensas.conj.rolagem_ef", ate="C",
        centro=True)
    rot(ws, f"D{re_}", "Seis fragmentos de um mesmo lugar, de uma mesma catástrofe, de um mesmo morto ilustre (25.3).",
        ate="J", italico=True)
    av(ws, f"K{re_}", "recompensas.conj.aviso", S.aviso_rolagem(T("recompensas.conj.rolagem")), ate="L")
    xs = H.campos(ws, 420, "recompensas.conj.rolagem_ef", 30, "AA", ["listas tab.conjunto_*"])
    linhas = [
        ("nome", "Nome do Conjunto", "=" + H.sorteia("conjunto_nome", xs[1]), '="Tabelas: Nome do Conjunto"'),
        ("origem", "Origem", "=" + H.sorteia("conjunto_origem", xs[2]), '="Tabelas: Origem do Conjunto (25.3)"'),
        ("p2", "2 peças", f'=INDEX({dcol("conjunto_2", "Bônus de 2 peças")},{S.escolha(xs[3], 4)})',
         '="Uma das 4 opções de 25.3 (bônus pequeno e fixo)."'),
        ("p4", "4 peças", "=" + H.sorteia("conjunto_4", xs[4]),
         '="Tabelas (as 2 primeiras são as de 25.3): efeito condicional por Ciclo."'),
        ("teto", "Teto", '="Os bônus de Conjunto não somam mais de +3 numa mesma rolagem e entram no teto global '
                         '(25.3, 26.6)."', '="25.3"'),
    ]
    r = _tabela_res(ws, re_ + 2, "recompensas.conj", linhas, {"nome": ("conjunto_nome", "Nome do Conjunto"),
                                                              "origem": ("conjunto_origem", "Origem do Conjunto"),
                                                              "p4": ("conjunto_4", "Efeito de 4 peças")},
                    regra=("p2",))
    # Relíquias por Tier (25.3) e o Tier do grupo agora
    cabs(ws, r, {"A": "Slot (25.3)", "B": ("O que dá", "E"), "F": "Tier I (1-6)", "G": "Tier II (7-12)",
                 "H": "Tier III (13-17)", "I": "Tier IV (18-20)", "J": "Grupo agora", "K": ("Aviso", "L")})
    TG = f'INDEX({dcol("nivel_equipamento", "Tier de Relíquia")},{T("campanha.nivel_ef")})'
    for i in range(1, 7):
        rr = r + i
        cal(ws, f"A{rr}", f'=INDEX({dcol("reliquias", "Slot")},{i})', nome=f"recompensas.rel.{i}.slot")
        cal(ws, f"B{rr}", f'=INDEX({dcol("reliquias", "O que dá")},{i})', nome=f"recompensas.rel.{i}.da", ate="E")
        for j, (col, tier) in enumerate(zip("FGHI", ("Tier I", "Tier II", "Tier III", "Tier IV"))):
            cal(ws, f"{col}{rr}", f'="+"&INDEX({dcol("reliquias", tier)},{i})', nome=f"recompensas.rel.{i}.t{j + 1}",
                centro=True, regra=True)
        agora = (f'="+"&IF({TG}="Tier I",INDEX({dcol("reliquias", "Tier I")},{i}),IF({TG}="Tier II",'
                 f'INDEX({dcol("reliquias", "Tier II")},{i}),IF({TG}="Tier III",'
                 f'INDEX({dcol("reliquias", "Tier III")},{i}),INDEX({dcol("reliquias", "Tier IV")},{i}))))')
        cal(ws, f"J{rr}", agora, nome=f"recompensas.rel.{i}.agora", centro=True, regra=True)
    N.subtabela(ws, "recompensas.reliquias", [r], "A:L", 6)
    rr = r + 7
    cal(ws, f"A{rr}", f'="Tier do grupo agora: "&{TG}&" (nível "&{T("campanha.nivel_ef")}&"). Bônus de slot são '
                      f'permanentes e ficam fora do teto; Mãos e Esfera Planar nunca somam na mesma rolagem (25.3)."',
        nome="recompensas.rel.tier_grupo", ate="L", regra=True)
    return rr + 1


def _tesouro(ws, r0):
    titulo(ws, r0, f"Tesouro do grupo ({NT} linhas; cole aqui a linha de saída dos achados)")
    r = r0 + 1
    cabecalhos = []
    for i in range(1, NT + 1):
        if (i - 1) % 13 == 0:
            _cab_tesouro(ws, r)
            cabecalhos.append(r)
            r += 1
        p = f"recompensas.tes.{i}"
        ent(ws, f"A{r}", f"{p}.sessao", tipo="inteiro", minimo=1, maximo=999, rotulo="Sessão", centro=True)
        ent(ws, f"B{r}", f"{p}.item", ate="D", maximo=80, rotulo="Item ou Créditos")
        ent(ws, f"E{r}", f"{p}.qtd", tipo="inteiro", minimo=0, maximo=999, rotulo="Quantidade", centro=True)
        ent(ws, f"F{r}", f"{p}.cr", tipo="inteiro", minimo=-99999, maximo=99999, rotulo="Créditos", centro=True,
            amostra=200)
        ent(ws, f"G{r}", f"{p}.quem", ate="H", maximo=40, rotulo="Com quem")
        ent(ws, f"I{r}", f"{p}.notas", ate="J", maximo=200, rotulo="Notas")
        CR = T(f"{p}.cr")
        av(ws, f"K{r}", f"{p}.aviso", f'=IF(AND(LEN({CR})>0,NOT(ISNUMBER({CR}))),"Créditos não é número: a linha não '
                                      f'entra no saldo","")', ate="L")
        r += 1
    N.subtabela(ws, "recompensas.tesouro", cabecalhos, "A:L", NT)
    rot(ws, f"A{r}", "Saldo de Créditos", negrito=True)
    cal(ws, f"B{r}", "=" + "+".join(f'IF(ISNUMBER({T(f"recompensas.tes.{i}.cr")}),{T(f"recompensas.tes.{i}.cr")},0)'
                                    for i in range(1, NT + 1)), nome="recompensas.tes.saldo", centro=True, regra=True)
    rot(ws, f"C{r}", "Soma da coluna Créditos (+ entra, − sai). Itens sem Créditos não mexem no saldo.", ate="J")
    av(ws, f"K{r}", "recompensas.tes.aviso.saldo", f'=IF({T("recompensas.tes.saldo")}<0,"Saldo de Créditos negativo",'
                                                    f'"")', ate="L")
