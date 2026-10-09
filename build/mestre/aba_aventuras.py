# -*- coding: utf-8 -*-
"""
Aba Aventuras — Criador de Aventuras (R6, design §6.11).

Gerador G = 300: tipo, gancho (50% os 4 de 27.18 da faixa da aventura / 50% tabela, H20), contratante (facção de
27.16 diferente da do conflito, ocupação e nome pela cultura de 05), objetivo (por tipo), local (50% os lugares de
27.17 que servem à faixa / 50% tabela, H26), facção do conflito, antagonista (Boss da facção na faixa → Elite da
facção → Boss da faixa, H22, pelas fichas de 27.16), complicação, reviravolta, prazo (27.7 abre a lista) e
recompensa (verba de marco 24.5 da faixa da aventura, equipamento de faixa 25.1, 1 consumível de 24.3 pela faixa —
H9 — e 1 pista). Não lê a aba Recompensas (§5). Estrutura de 5 cenas (H14) pelas réguas de 27.4 e 27.7, com a DT
da faixa do desafio (27.2) e o orçamento (27.4, H5 para grupo ≠ 4). Linha de saída na ordem de Missões (6.5, D6).
"""

from openpyxl.utils import column_index_from_string as CI

import mestre_dados as D
from mestre import nucleo as N
from mestre import sorteio as S
from mestre import historia as H
from mestre.nucleo import T, q, ent, cal, av, rot, cabs, titulo, dcol, sugestao, sugestao_formula

G_AV = 300
M = 2147483647


def _dt(fi, linha):
    return H.escolher(fi, [f"INDEX({dcol('dt_faixa', fx)},{linha})" for fx in D.FAIXAS])


def montar(wb):
    ws = wb["Aventuras"]
    titulo(ws, 5, "Gerador de aventuras (G = 300): vazio = Sortear; faixa vazia = a do grupo")
    cabs(ws, 6, {"A": "Rolagem nº", "B": ("Tipo", "D"), "E": "Faixa", "F": ("Facção do conflito", "H"),
                 "I": ("Rolagem efetiva", "J"), "K": ("Aviso", "L")})
    fonte_tipo = H.lista_com_sortear(ws, "AH", 10, "tipo_aventura", "aventuras.lista.tipo")
    fonte_fac = H.lista_com_sortear(ws, "AI", 10, "faccoes", "aventuras.lista.faccao")
    ent(ws, "A7", "aventuras.rolagem", tipo="inteiro", minimo=1, maximo=1000000, rotulo="Rolagem nº", centro=True,
        amostra=3)
    import mestre_sabor as SB
    ent(ws, "B7", "aventuras.tipo", tipo="lista", fonte=fonte_tipo, ate="D", rotulo="Tipo",
        opcoes=["Sortear"] + SB.TIPO_AVENTURA)
    ent(ws, "E7", "aventuras.faixa", tipo="lista", fonte="lista.faixas", rotulo="Faixa", centro=True)
    ent(ws, "F7", "aventuras.faccao", tipo="lista", fonte=fonte_fac, ate="H", rotulo="Facção do conflito",
        opcoes=["Sortear"] + D.faccoes())
    cal(ws, "I7", S.rolagem_efetiva(T("aventuras.rolagem")), nome="aventuras.rolagem_ef", ate="J", centro=True)
    xs = H.campos(ws, G_AV, "aventuras.rolagem_ef", 10, "AA",
                  ["tipo", "faixa (vazia = do grupo: ganchos, local, antagonista, DTs, orçamento, recompensa)",
                   "facção", "listas tab.* da aventura", "bestiário e 27.16 (Dados)"])
    TP, FA, FC = T("aventuras.tipo"), T("aventuras.faixa"), T("aventuras.faccao")
    a = lambda r, f, nome: N.aux(ws, f"N{r}", f, nome=f"aventuras.g.{nome}")  # noqa: E731
    g = lambda nome: T(f"aventuras.g.{nome}")  # noqa: E731
    LT, LF = T("aventuras.lista.tipo"), T("aventuras.lista.faccao")
    a(10, f'=IF(AND(LEN({TP})>0,{TP}<>"Sortear",COUNTIF({LT},{TP})>0),{TP},{H.sorteia("tipo_aventura", xs[1])})',
      "tipo")
    fl = N.faixa_da_lista(FA)
    a(11, f'=IF(LEN({fl})>0,{fl},{T("campanha.faixa")})', "fx")
    a(12, f'=MATCH({g("fx")},{dcol("faixas", "Faixa")},0)', "fi")
    a(13, f'=IF(AND(LEN({FC})>0,{FC}<>"Sortear",COUNTIF({LF},{FC})>0),{FC},{H.sorteia("faccoes", xs[20])})', "fc")
    # contratante: facção ≠ a do conflito (H26), Raça, ocupação e nome pela cultura (05)
    a(14, f'=IFERROR(INDEX({T("tab.faccoes.contador")},MATCH({g("fc")},{T("tab.faccoes.valores")},0)),0)', "fc_k")
    nf = H.n("faccoes")
    kfc = g("fc_k")
    k_contr = f"IF({kfc}>0,{S.segundo_sem_repetir(xs[3], nf, kfc)},{S.escolha(xs[3], nf)})"
    a(15, f'=IF({nf}<=0,"",{H.k_esimo("faccoes", k_contr)})', "c_fac")
    rac = dcol("racas", "Raça")
    a(16, f'=INDEX({rac},INT({xs[4]}*7/2147483647)+1)', "c_raca")
    a(17, "=" + H.ridx(g("c_raca")), "c_ri")
    nome, sob = H.nome_cultura(g("c_ri"), xs[17], xs[21])
    a(18, "=" + nome, "c_nome")
    a(19, "=" + sob, "c_sob")
    a(20, "=" + H.montar_nome(g("c_ri"), g("c_nome"), g("c_sob")), "c_nome_completo")
    a(21, "=" + H.sorteia("ocupacao", xs[16]), "c_ocup")
    a(22, f'={g("c_nome_completo")}&IF(LEN({g("c_ocup")})>0,", "&{g("c_ocup")},"")&IF(LEN({g("c_fac")})>0," ("&'
          f'{g("c_fac")}&")","")', "contratante")
    # objetivo por tipo (contador corrido em AE sobre a tabela de duas colunas)
    vals = T("tab.objetivo.valores2")
    tot, _ = H.contador_chave(ws, "AE", 10, "objetivo", g("tipo"), "aventuras.g.ob_col")
    a(23, f"={tot}", "ob_n")
    a(24, f'=IF({g("ob_n")}=0,"",IFERROR(INDEX({vals},MATCH(INT({xs[5]}*{g("ob_n")}/2147483647)+1,'
          f'{T("aventuras.g.ob_col")},0))&"",""))', "objetivo")
    # local: lugares de 27.17 que servem à faixa (AF = serve?, AG = contador) ou a tabela de sabor (H26)
    lv = T("tab.locais.valores")
    lug, fmin, fmax = dcol("locais_faixa", "Lugar"), dcol("locais_faixa", "Faixa mínima"), dcol("locais_faixa",
                                                                                              "Faixa máxima")
    linhas = H.linhas_do_intervalo("locais")
    for i, eh_cab in linhas:
        nm = f'INDEX({lv},{i})&""'
        m = f"MATCH({nm},{lug},0)"
        # o cabeçalho repetido entre as faixas de vagas não é lugar: 0
        N.aux(ws, f"AF{9 + i}", "=0" if eh_cab else
              f'=IF(LEN({nm})=0,0,IF(ISNUMBER({m}),IF(AND(INDEX({fmin},{m})<={g("fi")},'
              f'INDEX({fmax},{m})>={g("fi")}),1,0),1))', nome=f"aventuras.g.ls{i}")
        prev = "0" if i == 1 else f"$AG${9 + i - 1}"
        N.aux(ws, f"AG{9 + i}", f"={prev}+$AF${9 + i}", nome=f"aventuras.g.lc{i}")
    nlin = len(linhas)
    N.reg("aventuras.g.lc_col", ws, f"AG10:AG{9 + nlin}")
    a(25, f"=$AG${9 + nlin}", "ll_n")
    a(26, f'=IF({g("ll_n")}=0,"",IFERROR(INDEX({lv},MATCH(INT({xs[6]}*{g("ll_n")}/2147483647)+1,'
          f'{T("aventuras.g.lc_col")},0))&"",""))', "local_livro")
    a(27, "=" + H.sorteia("local", xs[6]), "local_tab")
    a(28, "=" + S.inteiro(xs[18], 1, 2), "fonte_local")
    a(29, f'=IF({g("fonte_local")}=1,IF(LEN({g("local_livro")})>0,{g("local_livro")},{g("local_tab")}),'
          f'IF(LEN({g("local_tab")})>0,{g("local_tab")},{g("local_livro")}))', "local")
    _antagonista(ws, xs, a, g)
    a(33, "=" + H.sorteia("complicacao", xs[8]), "complicacao")
    a(34, "=" + H.sorteia("reviravolta", xs[9]), "reviravolta")
    a(35, "=" + H.sorteia("prazo", xs[10]), "prazo")
    a(36, f'=INDEX({dcol("composicoes", "Composição")},{S.escolha(xs[11], 4)})', "comp")
    a(37, "=" + S.inteiro(xs[12], 1, 2), "cena4")
    a(38, f'=INDEX({dcol("sem_matar", "Objetivo")},{S.escolha(xs[19], 3)})', "sem_matar")
    # consumível da faixa da aventura (24.3, H9)
    FI = g("fi")
    ncf = f'INDEX({dcol("consumiveis_faixa", "Nº de consumíveis")},{FI})'
    a(39, f"={S.escolha(xs[13], ncf)}", "cons_j")
    a(40, "=" + H.escolher(FI, [f'MATCH({g("cons_j")},{dcol("consumiveis", f"Ordem {fx}")},0)' for fx in D.FAIXAS]),
      "cons_l")
    a(41, f'=INDEX({dcol("consumiveis", "Item")},{g("cons_l")})', "cons_item")
    a(42, f'=INDEX({dcol("consumiveis", "Preço (Cr)")},{g("cons_l")})', "cons_preco")
    a(43, "=" + H.sorteia("pista", xs[14]), "pista")
    a(44, "=" + S.inteiro(xs[15], 1, 2), "fonte_gancho")
    a(45, "=" + H.escolher(FI, [H.sorteia(f"ganchos_{fx.replace('-', '_')}", xs[2]) for fx in D.FAIXAS]),
      "gancho_livro")
    a(46, "=" + H.sorteia("gancho", xs[2]), "gancho_tab")
    a(47, f'=IF({g("fonte_gancho")}=1,IF(LEN({g("gancho_livro")})>0,{g("gancho_livro")},{g("gancho_tab")}),'
          f'IF(LEN({g("gancho_tab")})>0,{g("gancho_tab")},{g("gancho_livro")}))', "gancho")
    a(48, f'=INDEX({dcol("orcamento", "Orçamento")},{FI})', "orc4")
    NP = T("campanha.jogadores_ef")
    a(49, f'=IF({NP}=4,{g("orc4")},INT({g("orc4")}*{NP}/4))', "orc")
    a(50, "=" + _dt(FI, 3), "dt_media")
    a(51, "=" + _dt(FI, 4), "dt_dificil")
    a(52, f'=INDEX({dcol("verba", "Verba de marco (Cr)")},{FI})', "verba")
    av(ws, "K7", "aventuras.aviso.entradas",
       f'=IF(LEN({S.aviso_rolagem(T("aventuras.rolagem"))[1:]})>0,{S.aviso_rolagem(T("aventuras.rolagem"))[1:]},'
       f'IF(AND(LEN({TP})>0,{TP}<>"Sortear",COUNTIF({LT},{TP})=0),"Tipo fora da lista (aba Tabelas): sorteando",'
       f'IF(AND(LEN({FA})>0,LEN({fl})=0),"Faixa fora da lista: usando a do grupo",'
       f'IF(AND(LEN({FC})>0,{FC}<>"Sortear",COUNTIF({LF},{FC})=0),"Facção fora da lista (aba Tabelas): sorteando",'
       f'""))))', ate="L")
    _resultado(ws, g)
    _cenas(ws, g)
    _saida(ws, g)


def _antagonista(ws, xs, a, g):
    """H22: Boss da facção do conflito na faixa → Elite da facção na faixa → Boss da faixa (27.16 + 28.11)."""
    b = N.MAPA.blocos["dados.bestiario"]
    dl = lambda col, i: f"'Dados'!${b['colunas'][col]}${b['primeira_linha'] + i - 1}"  # noqa: E731
    ff, fc_ = dcol("faccao_fichas", "Facção"), dcol("faccao_fichas", "Criatura")
    FX, FC = g("fx"), g("fc")
    cols = {"bf": "AK", "ef": "AL", "ba": "AM"}
    for i in range(1, 33):
        rr = 10 + i
        da = f'COUNTIFS({ff},{FC},{fc_},{dl("Nome", i)})>0'
        cond = {"bf": f'AND({dl("Tipo", i)}="Boss",{dl("Faixa", i)}={FX},{da})',
                "ef": f'AND({dl("Tipo", i)}="Elite",{dl("Faixa", i)}={FX},{da})',
                "ba": f'AND({dl("Tipo", i)}="Boss",{dl("Faixa", i)}={FX})'}
        for k, col in cols.items():
            prev = "0" if i == 1 else f"${col}${rr - 1}"
            N.aux(ws, f"{col}{rr}", f"={prev}+IF({cond[k]},1,0)", nome=f"aventuras.g.{k}{i}")
    rng = {k: f"${c}$11:${c}$42" for k, c in cols.items()}
    a(30, f'=IF($AK$42>0,1,IF($AL$42>0,2,IF($AM$42>0,3,0)))', "an_degrau")
    a(31, f'=IF({g("an_degrau")}=0,"",IFERROR(MATCH(INT({xs[7]}*IF({g("an_degrau")}=1,$AK$42,IF({g("an_degrau")}=2,'
          f'$AL$42,$AM$42))/2147483647)+1,IF({g("an_degrau")}=1,{rng["bf"]},IF({g("an_degrau")}=2,{rng["ef"]},'
          f'{rng["ba"]})),0),""))', "an_linha")
    LN = g("an_linha")
    bx = lambda col: f'INDEX({dcol("bestiario", col)},{LN})'  # noqa: E731
    a(32, f'=IF(ISNUMBER({LN}),{bx("Nome")}&" ("&{bx("Tipo")}&", faixa "&{bx("Faixa")}&", "&'
          f'{bx("Facção ou origem")}&")","")', "antagonista")
    N.aux(ws, "O30", f'=IF(ISNUMBER({LN}),{bx("Nome")},"")', nome="aventuras.g.an_nome")


def _resultado(ws, g):
    r0 = 9
    titulo(ws, r0, "Aventura sorteada (automático)")
    cabs(ws, r0 + 1, {"A": "Campo", "B": ("Sorteado", "H"), "I": ("De onde vem", "J"), "K": ("Aviso", "L")})
    S_ = N.ROTULO_SUGESTAO
    linhas = [
        ("tipo", "Tipo", g("tipo"), f'=IF(AND(LEN({T("aventuras.tipo")})>0,{T("aventuras.tipo")}<>"Sortear"),'
                                    f'"Escolhido","Tabelas: Tipo de aventura")'),
        ("gancho", "Gancho", g("gancho"), f'=IF({g("fonte_gancho")}=1,"27.18, faixa "&{g("fx")},"Tabelas: Gancho de '
                                          f'aventura")&" · {S_} (H20)"'),
        ("contratante", "Contratante", g("contratante"),
         '="Facção de 27.16 diferente da do conflito; nome pela cultura (05) · ' + S_ + ' (H26)"'),
        ("objetivo", "Objetivo", g("objetivo"), '="Tabelas: Objetivo por tipo"'),
        ("local", "Local", g("local"), f'=IF(AND({g("fonte_local")}=1,LEN({g("local_livro")})>0),"27.17 (lugar que '
                                       f'serve à faixa)","Tabelas: Local")&" · {S_} (H26)"'),
        ("faccao", "Facção do conflito", g("fc"), f'=IF(AND(LEN({T("aventuras.faccao")})>0,'
                                                 f'{T("aventuras.faccao")}<>"Sortear"),"Escolhida","Sorteada (27.16)")'),
        ("antagonista", "Antagonista", g("antagonista"),
         f'=CHOOSE(MAX(1,{g("an_degrau")}),"Boss da facção na faixa","Elite da facção na faixa","Boss da faixa")&'
         f'" (28.11, 27.16) · {S_} (H22)"'),
        ("complicacao", "Complicação", g("complicacao"), '="Tabelas: Complicação (falhe para frente, 02)"'),
        ("reviravolta", "Reviravolta", g("reviravolta"), '="Tabelas: Reviravolta"'),
        ("prazo", "Prazo ou risco", g("prazo"), '="Tabelas: Prazo (27.7: ponha relógio na ficção)"'),
        ("recompensa", "Recompensa", f'"Verba de marco: "&{g("verba")}&" Cr para o grupo ao subir de nível (24.5) · '
                                     f'equipamento de faixa se esta aventura fechar o arco (25.1) · 1 "&'
                                     f'{g("cons_item")}&" ("&{g("cons_preco")}&" Cr, 24.3) · pista: "&{g("pista")}',
         f'="Faixa "&{g("fx")}&"; o consumível é {S_} (H9)"'),
    ]
    vazias = {"objetivo": f'IF({g("ob_n")}=0,"Sem objetivo para o tipo "&{g("tipo")}&" na aba Tabelas","")',
              "tipo": f'IF({H.n("tipo_aventura")}<=0,"Lista \'Tipo de aventura\' está vazia (aba Tabelas)","")',
              "gancho": f'IF(LEN({g("gancho")})=0,"Listas de gancho vazias (aba Tabelas)","")',
              "local": f'IF(LEN({g("local")})=0,"Listas de local vazias (aba Tabelas)","")',
              "complicacao": f'IF({H.n("complicacao")}<=0,"Lista \'Complicação\' está vazia (aba Tabelas)","")',
              "reviravolta": f'IF({H.n("reviravolta")}<=0,"Lista \'Reviravolta\' está vazia (aba Tabelas)","")',
              "prazo": f'IF({H.n("prazo")}<=0,"Lista \'Prazo ou risco\' está vazia (aba Tabelas)","")',
              "faccao": f'IF({H.n("faccoes")}<=0,"Lista \'Facções\' está vazia (aba Tabelas)","")'}
    for k, (campo, rotulo, valor, origem) in enumerate(linhas):
        r = r0 + 2 + k
        rot(ws, f"A{r}", rotulo, negrito=True)
        cal(ws, f"B{r}", "=" + valor, nome=f"aventuras.res.{campo}", ate="H", regra=campo == "recompensa")
        cal(ws, f"I{r}", origem, nome=f"aventuras.res.{campo}.origem", ate="J")
        if "(H" in origem:
            h = origem.split("(H")[-1].split(")")[0]
            sugestao_formula(f"aventuras.res.{campo}.origem", f"H{h}", [f"B{r}"])
        if campo in vazias:
            av(ws, f"K{r}", f"aventuras.aviso.{campo}", "=" + vazias[campo], ate="L")


def _cenas(ws, g):
    r0 = 23
    titulo(ws, r0, "Estrutura em 5 cenas (27.4 e 27.7; a DT é a da faixa do desafio, 27.2)", ate="J")
    sugestao(ws, f"K{r0}", "H14", "aventuras.h14", ate="L")
    cabs(ws, r0 + 1, {"A": "Cena", "B": "Tipo", "C": ("O que acontece", "H"), "I": "DT", "J": "Orçamento (PV)",
                      "K": ("Aviso", "L")})
    ORC, C4 = g("orc"), g("cena4")
    cenas = [
        ("1 · Gancho", '"Social ou descoberta"', g("gancho"), g("dt_media"), '"—"'),
        ("2 · Investigação ou viagem", '"Exploração"',
         '"Um Teste de Perícia da faixa do desafio (DT Média, 27.2); falhe para frente: chegar tarde, sem recurso ou '
         'devendo um favor (02, 27.15)."', g("dt_media"), '"—"'),
        ("3 · Primeiro encontro", '"Combate"', f'"Composição "&{g("comp")}&" a 50% do orçamento: cena de passagem, '
                                                f'cerca de 2 Ciclos (27.4)."', '"—"', f"INT({ORC}/2)"),
        ("4 · Complicação", f'IF({C4}=1,"Combate","Objetivo")',
         f'{g("complicacao")}&" — "&IF({C4}=1,"e um encontro típico (27.4).","e um objetivo que não seja matar todo '
         f'mundo: "&{g("sem_matar")}&" (27.7).")', g("dt_dificil"), f'IF({C4}=1,{ORC},"—")'),
        ("5 · Clímax", '"Combate"', f'"Antagonista: "&{g("antagonista")}&". Cumpra o contrato da Fraqueza (27.5); três '
                                    f'combates no dia é um dia de verdade, quatro é emergência (27.7)."',
         g("dt_dificil"), ORC),
    ]
    for k, (nome, tipo, txt, dt, orc) in enumerate(cenas, start=1):
        r = r0 + 1 + k
        rot(ws, f"A{r}", nome, negrito=True)
        cal(ws, f"B{r}", "=" + tipo, nome=f"aventuras.cena{k}.tipo", centro=True)
        cal(ws, f"C{r}", "=" + txt, nome=f"aventuras.cena{k}.texto", ate="H")
        cal(ws, f"I{r}", "=" + dt, nome=f"aventuras.cena{k}.dt", centro=True, regra=True)
        cal(ws, f"J{r}", "=" + orc, nome=f"aventuras.cena{k}.orc", centro=True, regra=True)
    r = r0 + 7
    cal(ws, f"A{r}", f'="Orçamento da faixa "&{g("fx")}&" para "&{T("campanha.jogadores_ef")}&" jogadores: "&{ORC}&'
                     f'" PV (27.4"&IF({T("campanha.jogadores_ef")}=4,")","; grupo diferente de 4: {N.ROTULO_SUGESTAO}'
                     f' (H5))")&". DT Média "&{g("dt_media")}&", Difícil "&{g("dt_dificil")}&" (27.2)."',
        nome="aventuras.cenas.resumo", ate="L", regra=True)
    sugestao_formula("aventuras.cenas.resumo", "H5", [])
    N.subtabela(ws, "aventuras.cenas", [r0 + 1], "A:L", 5)


def _saida(ws, g):
    r0 = 32
    titulo(ws, r0, "Linha de saída: copie A:J e cole como valores em Missões (Colar especial → Somente valores)")
    cabs(ws, r0 + 1, {"A": "Missão", "B": "Tipo", "C": ("Contratante", "D"), "E": ("Objetivo", "F"), "G": "Local",
                      "H": "Prazo", "I": "Estado", "J": "Recompensa combinada"})
    r = r0 + 2
    cal(ws, f"A{r}", f'={g("tipo")}&" — "&{g("local")}', nome="aventuras.saida.missao")
    cal(ws, f"B{r}", f'={g("tipo")}', nome="aventuras.saida.tipo")
    cal(ws, f"C{r}", f'={g("contratante")}', nome="aventuras.saida.contratante", ate="D")
    cal(ws, f"E{r}", f'={g("objetivo")}', nome="aventuras.saida.objetivo", ate="F")
    cal(ws, f"G{r}", f'={g("local")}', nome="aventuras.saida.local")
    cal(ws, f"H{r}", f'={g("prazo")}', nome="aventuras.saida.prazo")
    cal(ws, f"I{r}", '="Oferecida"', nome="aventuras.saida.estado", centro=True)
    cal(ws, f"J{r}", f'={g("verba")}&" Cr · "&{g("cons_item")}&" · equipamento de faixa se fechar o arco"',
        nome="aventuras.saida.recompensa", regra=True)
    rot(ws, f"A{r + 1}", "As colunas estão na ordem da aba Missões (missão, tipo, contratante, objetivo, local, prazo, "
                         "estado, recompensa; D6). A recompensa usa a faixa da aventura e não lê a aba Recompensas.",
        ate="L", italico=True)
