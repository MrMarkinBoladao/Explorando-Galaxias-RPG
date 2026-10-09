# -*- coding: utf-8 -*-
"""
Aba Improviso (R8, R13; design §6.14): rumores e ganchos rápidos (G = 600), eventos e complicações de viagem, espaço e
cidade com a falha para frente (610; 02, 27.1), loja com estoque e preços do livro (620; 24.1–24.3, H15), bugigangas sem
efeito (630), oráculo sim/não (640, H10), rolador de dados com semente (650; média de 02) e DT rápida (27.2, 27.3).
O rolador também usa a semente da aba Início (D5): RAND recalcularia a cada edição em qualquer aba do Google e o
resultado não seria reproduzível.
"""

import mestre_dados as D
import mestre_dados3 as D3
from mestre import nucleo as N
from mestre import sorteio as S
from mestre import historia as H
from mestre.aba_mundos import rolagens, linha, vazia, cabecalho, M
from mestre.nucleo import T, q, ent, cal, av, rot, cabs, titulo, dcol, sugestao

GERADORES = [(600, "Rumores e ganchos"), (610, "Evento ou complicação"), (620, "Loja"), (630, "Bugigangas"),
             (640, "Oráculo sim/não"), (650, "Rolador de dados")]
NRUMOR, NBUG, NLOJA, NEXPR, NDADOS = 3, 3, 6, 3, 20


def montar(wb):
    ws = wb["Improviso"]
    # rolador: Faces (C) e Vantagem (E: "Desvantagem") são listas com a seta do Google
    N.larguras_grade(ws, {**N.GRADE_PX, "C": 110, "D": 110, "E": 130, "I": 90, "K": 135, "L": 135})
    r = rolagens(ws, 5, GERADORES, "improviso", "Rolar de novo = somar 1 na Rolagem nº do gerador (design §5).")
    g = lambda nome: T(f"improviso.g.{nome}")  # noqa: E731
    a = lambda rr, f, nome: N.aux(ws, f"N{rr}", f, nome=f"improviso.g.{nome}")  # noqa: E731
    xs, lin_aux = {}, 10
    params = {600: ["faixa do grupo (ganchos de 27.18)", "listas tab.*"], 610: ["onde", "listas tab.*"],
              620: ["tipo de loja", "blocos de 24.1–24.3 (Dados)"], 630: ["listas tab.*"],
              640: ["probabilidade", "tab.oraculo"], 650: ["as 3 expressões (N, F, M, Vantagem)"]}
    for gid, _ in GERADORES:
        xs[gid] = H.campos(ws, gid, f"improviso.r{gid}_ef", lin_aux, "AA", params[gid])
        lin_aux += len(N.MAPA.geradores[str(gid)]["campos"]) + 1
    aux_lin = [10]

    def a2(f, nome):
        """Auxiliar em N, numa linha nova (as linhas de u/y/x ficam em AA:AC)."""
        a(aux_lin[0], f, nome)
        aux_lin[0] += 1
        return g(nome)
    r = _rumores(ws, r + 1, xs[600], a2)
    r = _eventos(ws, r + 1, xs[610], a2)
    r = _loja(ws, r + 1, xs[620], a2)
    r = _bugigangas(ws, r + 1, xs[630], a2)
    r = _oraculo(ws, r + 1, xs[640], a2)
    r = _rolador(ws, r + 1, xs[650], a2)
    _dt_rapida(ws, r + 1)


def _seq(a2, id_, x, nome):
    n = a2(f"={H.n(id_)}", f"{nome}.n")
    p = a2("=" + S.passo(n), f"{nome}.passo")
    i0 = a2("=" + S.escolha(x, n), f"{nome}.i0")
    return n, p, i0


def _rumores(ws, r, x, a2):
    titulo(ws, r, f"Rumores (G = 600): {NRUMOR} por rolagem, sem repetir, cada um com a veracidade", ate="J")
    sugestao(ws, f"K{r}", "H25", "improviso.g600.h25", ate="L")
    cabs(ws, r + 1, {"A": "Rumor", "B": ("O que se diz (automático)", "H"), "I": ("Verdade? (automático)", "J"),
                     "K": ("Aviso", "L")})
    n, p, i0 = _seq(a2, "rumor", x[1], "rumor")
    for k in range(NRUMOR):
        rr = r + 2 + k
        rot(ws, f"A{rr}", f"Rumor {k + 1}", negrito=True)
        ix = a2("=" + S.kesimo_sem_repetir(i0, k, n, p), f"rumor.{k}.i")
        cal(ws, f"B{rr}", f'=IF({n}<=0,"",{H.k_esimo("rumor", ix)})', nome=f"improviso.rumor.{k + 1}", ate="H")
        cal(ws, f"I{rr}", "=" + H.sorteia("veracidade", x[2 + k]), nome=f"improviso.rumor.{k + 1}.verdade", ate="J",
            centro=True)
        if k == 0:
            av(ws, f"K{rr}", "improviso.rumor.aviso", vazia("rumor", "Rumor"), ate="L")
        elif k == 1:
            av(ws, f"K{rr}", "improviso.rumor.aviso2", vazia("veracidade", "Veracidade do rumor"), ate="L")
    rr = r + 2 + NRUMOR
    sugestao(ws, f"A{rr}", "H11", "improviso.g600.h11", ate="L",
             extra="a veracidade é Verdadeiro, Meia-verdade ou Falso com o mesmo peso; repita uma entrada na aba "
                   "Tabelas para mudar o peso")
    N.subtabela(ws, "improviso.rumores", [r + 1], "A:L", NRUMOR)
    rr += 1
    cabs(ws, rr, {"A": "Gancho rápido", "B": ("Gancho (automático)", "H"), "I": ("De onde vem", "J"), "K": ("Aviso", "L")})
    FI = T("campanha.faixa_idx")
    rot(ws, f"A{rr + 1}", "Do livro", negrito=True)
    cal(ws, f"B{rr + 1}", "=" + H.escolher(FI, [H.sorteia(f"ganchos_{fx.replace('-', '_')}", x[5]) for fx in D.FAIXAS]),
        nome="improviso.gancho.livro", ate="H")
    cal(ws, f"I{rr + 1}", f'="27.18, faixa "&{T("campanha.faixa")}', nome="improviso.gancho.livro.origem", ate="J")
    rot(ws, f"A{rr + 2}", "Da tabela", negrito=True)
    cal(ws, f"B{rr + 2}", "=" + H.sorteia("gancho", x[6]), nome="improviso.gancho.tabela", ate="H")
    rot(ws, f"I{rr + 2}", "Tabelas: Gancho de aventura", ate="J")
    av(ws, f"K{rr + 2}", "improviso.gancho.aviso", vazia("gancho", "Gancho de aventura"), ate="L")
    N.subtabela(ws, "improviso.ganchos", [rr], "A:L", 2)
    return rr + 3


def _eventos(ws, r, x, a2):
    cabecalho(ws, r, "Evento ou complicação: viagem, espaço ou cidade", 610)
    rr = r + 2
    rot(ws, f"A{rr}", "Onde (preencha)", negrito=True)
    ent(ws, f"B{rr}", "improviso.evento.onde", tipo="lista", fonte="lista.onde_evento", ate="C", rotulo="Onde")
    ON = T("improviso.evento.onde")
    ok = f'OR({ON}="Viagem",{ON}="Espaço",{ON}="Cidade")'
    sort = H.escolher(S.escolha(x[1], 3), ['"Viagem"', '"Espaço"', '"Cidade"'])
    oe = a2(f"=IF({ok},{ON},{sort})", "evento.onde")
    cal(ws, f"D{rr}", f'=IF({ok},"Escolhido: ","Sorteado: ")&{oe}', nome="improviso.evento.onde_ef", ate="J")
    av(ws, f"K{rr}", "improviso.evento.aviso.onde",
       f'=IF(AND(LEN({ON})>0,{ON}<>"Sortear",NOT({ok})),"Fora da lista: sorteando entre viagem, espaço e cidade","")',
       ate="L")
    ev = (f'IF({oe}="Viagem",{H.sorteia("evento_viagem", x[2])},IF({oe}="Espaço",{H.sorteia("evento_espaco", x[2])},'
          f'{H.sorteia("evento_cidade", x[2])}))')
    linha(ws, rr + 1, "Evento", "=" + ev, "improviso.evento.evento", f'="Tabelas: Evento ("&{oe}&")"',
          f'=IF(LEN({T("improviso.evento.evento")})=0,"Lista de eventos vazia (aba Tabelas)","")')
    linha(ws, rr + 2, "Complicação", "=" + H.sorteia("complicacao", x[3]), "improviso.evento.complicacao",
          '="Tabelas: Complicação"', vazia("complicacao", "Complicação"))
    linha(ws, rr + 3, "Se um teste falhar", "=" + H.sorteia("custo_falha", x[4]), "improviso.evento.custo",
          '="Tabelas: Falhe para frente (02, 27.1)"', vazia("custo_falha", "Falhe para frente: o custo"))
    cal(ws, f"A{rr + 4}", "=" + N.dtexto("falhe") + '&" Ela cobra: tempo, ruído, recurso, '
                                                                                 'informação incompleta, uma '
                                                                                 'complicação nova (27.1)."',
        nome="improviso.evento.falhe", ate="L")
    N.subtabela(ws, "improviso.eventos", [r + 1], "A:L", 4)
    return rr + 5


def _loja(ws, r, x, a2):
    titulo(ws, r, "Loja (G = 620): estoque de 6 itens do livro, com o preço do livro", ate="J")
    sugestao(ws, f"K{r}", "H15", "improviso.g620.h15", ate="L")
    rr = r + 1
    cabs(ws, rr, {"A": "Campo", "B": ("Valor", "J"), "K": ("Aviso", "L")})
    rot(ws, f"A{rr + 1}", "Tipo de loja (preencha)", negrito=True)
    ent(ws, f"B{rr + 1}", "improviso.loja.tipo", tipo="lista", fonte="lista.tipo_loja", ate="D", rotulo="Tipo de loja")
    TL = T("improviso.loja.tipo")
    tipos = dcol("loja_tipos", "Tipo de loja")
    te = a2(f"=IF(COUNTIF({tipos},{TL})>0,{TL},INDEX({tipos},{S.escolha(x[1], 6)}))", "loja.tipo")
    cal(ws, f"E{rr + 1}", f'=IF(COUNTIF({tipos},{TL})>0,"Escolhida: ","Sorteada: ")&{te}', nome="improviso.loja.tipo_ef",
        ate="J")
    av(ws, f"K{rr + 1}", "improviso.loja.aviso.tipo",
       f'=IF(AND(LEN({TL})>0,{TL}<>"Sortear",COUNTIF({tipos},{TL})=0),"Tipo de loja fora da lista: sorteando","")',
       ate="L")
    rac = dcol("racas", "Raça")
    raca = a2(f"=INDEX({rac},INT({x[9]}*7/{M})+1)", "loja.raca")
    ri = a2("=" + H.ridx(raca), "loja.ri")
    nm, sb = H.nome_cultura(ri, x[10], x[11])
    nome = a2("=" + nm, "loja.nome")
    sob = a2("=" + sb, "loja.sob")
    rot(ws, f"A{rr + 2}", "Quem atende", negrito=True)
    cal(ws, f"B{rr + 2}", f'={H.montar_nome(ri, nome, sob)}&" ("&{raca}&"): "&{H.sorteia("maneirismo", x[12])}',
        nome="improviso.loja.lojista", ate="J")
    N.subtabela(ws, "improviso.loja.cab", [rr], "A:L", 2)
    rr += 3
    cabs(ws, rr, {"A": "Item", "B": ("No estoque (automático)", "D"), "E": ("O que é", "H"), "I": "Preço (Cr)",
                  "J": "Quantidade", "K": ("Aviso", "L")})
    n = a2(f'=IFERROR(INDEX({dcol("loja_tipos", "Nº de itens")},MATCH({te},{tipos},0)),0)', "loja.n")
    p = a2("=" + S.passo(n), "loja.passo")
    i0 = a2("=" + S.escolha(x[2], n), "loja.i0")
    for k in range(NLOJA):
        rl = rr + 1 + k
        ix = a2("=" + S.kesimo_sem_repetir(i0, k, n, p), f"loja.{k}.i")
        ch = a2(f'={te}&"|"&{ix}', f"loja.{k}.chave")
        rot(ws, f"A{rl}", f"Item {k + 1}", negrito=True)
        cal(ws, f"B{rl}", "=" + N.dbusca("loja", "Chave", ch, "Item"), nome=f"improviso.loja.{k + 1}.item", ate="D")
        cal(ws, f"E{rl}", "=" + N.dbusca("loja", "Chave", ch, "O que é"), nome=f"improviso.loja.{k + 1}.oque", ate="H")
        cal(ws, f"I{rl}", "=" + N.dbusca("loja", "Chave", ch, "Preço (Cr)"), nome=f"improviso.loja.{k + 1}.preco",
            regra=True, centro=True)
        cal(ws, f"J{rl}", "=" + S.inteiro(x[3 + k], 1, 3), nome=f"improviso.loja.{k + 1}.qtd", centro=True)
    rl = rr + 1 + NLOJA
    rot(ws, f"A{rl}", "Fora do comum", negrito=True)
    cal(ws, f"B{rl}", "=" + H.sorteia("item_raro", x[13]), nome="improviso.loja.raro", ate="D")
    cal(ws, f"E{rl}", '="Sem efeito no jogo até o Mestre decidir (27.9)."', nome="improviso.loja.raro.oque", ate="H")
    cal(ws, f"I{rl}", '="O que o Mestre disser (24.5)"', nome="improviso.loja.raro.preco", ate="J")
    av(ws, f"K{rl}", "improviso.loja.aviso.raro", vazia("item_raro", "Item fora do comum"), ate="L")
    N.subtabela(ws, "improviso.loja", [rr], "A:L", NLOJA + 1)
    rl += 1
    cal(ws, f"A{rl}", "=" + N.dtexto("precos") + '&" "&' +
        N.dtexto("sem_reliquia") + '&" (24.5)"', nome="improviso.loja.regra", ate="L")
    cal(ws, f"A{rl + 1}", "=" + N.dtexto("servicos") + '&" (24.5)"',
        nome="improviso.loja.servicos", ate="L")
    return rl + 2


def _bugigangas(ws, r, x, a2):
    titulo(ws, r, f"Bugigangas sem efeito (G = 630): {NBUG} por rolagem, sem repetir", ate="J")
    sugestao(ws, f"K{r}", "H25", "improviso.g630.h25", ate="L")
    cabs(ws, r + 1, {"A": "Bugiganga", "B": ("O que o grupo acha (automático)", "J"), "K": ("Aviso", "L")})
    n, p, i0 = _seq(a2, "bugiganga", x[1], "bug")
    for k in range(NBUG):
        rr = r + 2 + k
        rot(ws, f"A{rr}", f"Bugiganga {k + 1}", negrito=True)
        ix = a2("=" + S.kesimo_sem_repetir(i0, k, n, p), f"bug.{k}.i")
        cal(ws, f"B{rr}", f'=IF({n}<=0,"",{H.k_esimo("bugiganga", ix)})', nome=f"improviso.bug.{k + 1}", ate="J")
        if k == 0:
            av(ws, f"K{rr}", "improviso.bug.aviso", vazia("bugiganga", "Bugiganga"), ate="L")
    N.subtabela(ws, "improviso.bugigangas", [r + 1], "A:L", NBUG)
    return r + 2 + NBUG


def _oraculo(ws, r, x, a2):
    titulo(ws, r, "Oráculo sim/não (G = 640): d20 + modificador da probabilidade", ate="J")
    sugestao(ws, f"K{r}", "H10", "improviso.g640.h10", ate="L")
    cabs(ws, r + 1, {"A": "Campo", "B": ("Valor", "J"), "K": ("Aviso", "L")})
    rr = r + 2
    rot(ws, f"A{rr}", "Pergunta (preencha)", negrito=True)
    ent(ws, f"B{rr}", "improviso.oraculo.pergunta", maximo=200, ate="J", rotulo="Pergunta")
    rot(ws, f"A{rr + 1}", "Probabilidade", negrito=True)
    ent(ws, f"B{rr + 1}", "improviso.oraculo.prob", tipo="lista", fonte="lista.probabilidade", ate="D",
        rotulo="Probabilidade")
    PR = T("improviso.oraculo.prob")
    probs, mods = dcol("oraculo_prob", "Probabilidade"), dcol("oraculo_prob", "Modificador")
    mod = a2(f"=IFERROR(INDEX({mods},MATCH({PR},{probs},0)),0)", "oraculo.mod")
    cal(ws, f"E{rr + 1}", f'=IF(COUNTIF({probs},{PR})>0,"","Vazio = Meio a meio. ")&"Modificador "&IF({mod}>0,"+","")&'
                          f'{mod}', nome="improviso.oraculo.mod_txt", ate="J")
    av(ws, f"K{rr + 1}", "improviso.oraculo.aviso.prob",
       f'=IF(AND(LEN({PR})>0,COUNTIF({probs},{PR})=0),"Probabilidade fora da lista: usando Meio a meio","")', ate="L")
    d20 = a2("=" + S.dado(x[1], 20), "oraculo.d20")
    tot = a2(f"={d20}+{mod}", "oraculo.total")
    n = H.n("oraculo")
    k = a2(f'=IF({n}<=0,0,MIN({n},1+COUNTIF({T("tab.oraculo.valores2")},"<"&{tot})))', "oraculo.k")
    rot(ws, f"A{rr + 2}", "d20 rolado", negrito=True)
    cal(ws, f"B{rr + 2}", f'={d20}&IF({mod}=0,""," "&IF({mod}>0,"+","−")&" "&ABS({mod}))&" = "&{tot}',
        nome="improviso.oraculo.rolagem", ate="D")
    rot(ws, f"A{rr + 3}", "Resposta", negrito=True)
    cal(ws, f"B{rr + 3}", f'=IF({k}<=0,"",{H.k_esimo("oraculo", k)})', nome="improviso.oraculo.resposta", ate="D",
        negrito=True)
    rot(ws, f"E{rr + 3}", "Faixas (aba Tabelas, editáveis): até 3 Não, e… · 4 a 7 Não · 8 a 10 Não, mas… · 11 a 13 Sim, "
                          "mas… · 14 a 17 Sim · 18 ou mais Sim, e…", ate="J")
    av(ws, f"K{rr + 3}", "improviso.oraculo.aviso", vazia("oraculo", "Oráculo: resposta"), ate="L")
    N.subtabela(ws, "improviso.oraculo", [r + 1], "A:L", 4)
    return rr + 4


def _rolador(ws, r, x, a2):
    titulo(ws, r, f"Rolador de dados (G = 650): até {NEXPR} expressões N d F + M, com a média impressa de 02")
    cabs(ws, r + 1, {"A": "Expressão", "B": "Nº de dados (N)", "C": "Faces (F; vazio = 20)", "D": "Modificador (M)",
                     "E": "Vantagem (só 1d20)", "F": ("Dados rolados (automático)", "H"), "I": "Total",
                     "J": "Média (02)", "K": ("Aviso", "L")})
    for e in range(1, NEXPR + 1):
        rr = r + 1 + e
        p = f"improviso.rol.{e}"
        rot(ws, f"A{rr}", f"Expressão {e}", negrito=True)
        ent(ws, f"B{rr}", f"{p}.n", tipo="inteiro", minimo=1, maximo=NDADOS, rotulo="Nº de dados", centro=True,
            amostra=3)
        ent(ws, f"C{rr}", f"{p}.f", tipo="lista", fonte="lista.faces", rotulo="Faces", centro=True, amostra=6)
        ent(ws, f"D{rr}", f"{p}.m", tipo="inteiro", minimo=-50, maximo=50, rotulo="Modificador", centro=True, amostra=2)
        ent(ws, f"E{rr}", f"{p}.v", tipo="lista", fonte="lista.vantagem", rotulo="Vantagem", centro=True)
        NN, FF, MM, VV = (T(f"{p}.{k}") for k in "nfmv")
        ne = a2(f"=IF(ISNUMBER({NN}),MIN({NDADOS},MAX(1,INT({NN}))),0)", f"rol.{e}.n")
        fok = "OR(" + ",".join(f"{FF}={f}" for f in D3.FACES) + ")"
        fe = a2(f"=IF(ISNUMBER({FF}),IF({fok},{FF},20),20)", f"rol.{e}.f")
        me = a2(f"=IF(ISNUMBER({MM}),MIN(50,MAX(-50,INT({MM}))),0)", f"rol.{e}.m")
        va = a2(f'=IF(AND({ne}=1,{fe}=20),IF({VV}="Vantagem",1,IF({VV}="Desvantagem",-1,0)),0)', f"rol.{e}.va")
        ds = []
        for d in range(1, NDADOS + 1):
            c = 20 * (e - 1) + d
            cond = f"OR({d}<={ne},AND({d}=2,{va}<>0))" if d == 2 else f"{d}<={ne}"
            ds.append(a2(f'=IF({cond},{S.dado(x[c], fe)},"")', f"rol.{e}.d{d}"))
        kept = a2(f'=IF({va}=1,MAX({ds[0]},{ds[1]}),IF({va}=-1,MIN({ds[0]},{ds[1]}),{ds[0]}))', f"rol.{e}.mantido")
        lista_txt = f"{ds[0]}" + "".join(f'&IF({ne}>={d},", "&{ds[d - 1]},"")' for d in range(2, NDADOS + 1))
        cal(ws, f"F{rr}", f'=IF({ne}=0,"",IF({va}<>0,{ds[0]}&" e "&{ds[1]}&" (fica o "&{kept}&")",{lista_txt}))',
            nome=f"{p}.dados", ate="H")
        soma = "+".join(f'IF({d}<={ne},{ds[d - 1]},0)' for d in range(1, NDADOS + 1))
        cal(ws, f"I{rr}", f'=IF({ne}=0,"",IF({va}<>0,{kept},{soma})+{me})', nome=f"{p}.total", centro=True, negrito=True)
        cal(ws, f"J{rr}", f'=IF({ne}=0,"",INT({ne}*({fe}+1)/2)+{me})', nome=f"{p}.media", centro=True, regra=True)
        av(ws, f"K{rr}", f"{p}.aviso",
           f'=IF(IF(ISNUMBER({NN}),OR({NN}<1,{NN}>{NDADOS},INT({NN})<>{NN}),FALSE),"Nº de dados fora de 1 a {NDADOS}: '
           f'usando o limite",IF(AND(LEN({NN})=0,LEN({FF}&{MM}&{VV})>0),"Preencha o nº de dados",IF(AND(LEN({FF})>0,'
           f'NOT(AND(ISNUMBER({FF}),{fok}))),"Faces fora da lista: usando 20",IF(IF(ISNUMBER({MM}),OR({MM}<-50,'
           f'{MM}>50,INT({MM})<>{MM}),FALSE),"Modificador fora de −50 a +50: usando o limite",IF(AND(OR({VV}="Vantagem",'
           f'{VV}="Desvantagem"),{va}=0,{ne}>0),"Vantagem só vale para 1d20: rolando normal","")))))', ate="L")
    N.subtabela(ws, "improviso.rolador", [r + 1], "A:L", NEXPR)
    rr = r + 2 + NEXPR
    rot(ws, f"A{rr}", "Média impressa: número de dados × (faces + 1) ÷ 2, para baixo, + modificador (02, 28.3). Vantagem: "
                      "rola dois d20 e fica o maior; Desvantagem, o menor. Cada dado tem o próprio sorteio (a semente da "
                      "Início e a Rolagem nº do rolador).", ate="L", italico=True)
    N.constante("rolador.media", "INT(N*(F+1)/2)+M", "02")
    return rr + 1


def _dt_rapida(ws, r):
    titulo(ws, r, "DT rápida (27.2): a faixa é a do desafio, não a do personagem")
    cabs(ws, r + 1, {"A": "Dificuldade", "B": ("Faixa do desafio (vazio = do grupo)", "C"), "D": "DT (automático)",
                     "E": ("Lembrete", "J"), "K": ("Aviso", "L")})
    rr = r + 2
    ent(ws, f"A{rr}", "improviso.dt.dificuldade", tipo="lista", fonte="lista.dificuldades", rotulo="Dificuldade")
    ent(ws, f"B{rr}", "improviso.dt.faixa", tipo="lista", fonte="lista.faixas", ate="C", rotulo="Faixa do desafio")
    from mestre.aba_sessoes import _dt
    DIF, FX = T("improviso.dt.dificuldade"), T("improviso.dt.faixa")
    cal(ws, f"D{rr}", "=" + _dt(DIF, FX), nome="improviso.dt.valor", regra=True, centro=True, negrito=True)
    rot(ws, f"E{rr}", "Um muro é um muro: escalar continua DT 13 no nível 20. Sucesso Automático só em Teste de Perícia "
                      "(bônus ≥ DT); Teste de Ataque e de Resistência sempre se rolam. Sem Eficiência contra faixa alta, "
                      "conceda Vantagem (27.2).", ate="J")
    av(ws, f"K{rr}", "improviso.dt.aviso",
       f'=IF(AND(LEN({DIF})>0,COUNTIF({dcol("dt_faixa", "Dificuldade")},{DIF})=0),"Dificuldade fora da lista (27.2)",'
       f'IF(AND(LEN({FX})>0,COUNTIF({N.dlista("faixas")},{FX})=0),"Faixa fora da lista: usando a do grupo",""))',
       ate="L")
    N.subtabela(ws, "improviso.dt", [r + 1], "A:L", 1)
    rr += 2
    titulo(ws, rr, "As cinco DTs de subsistema (27.3): vencem a tabela de 27.2, e não existe uma sexta")
    cabs(ws, rr + 1, {"A": ("Teste", "F"), "G": "DT", "H": ("Capítulo", "I")})
    for k in range(1, 6):
        rl = rr + 1 + k
        cal(ws, f"A{rl}", "=" + N.dcel("dt_subsistema", "Teste", k), nome=f"improviso.sub.{k}.teste", ate="F")
        cal(ws, f"G{rl}", "=" + N.dcel("dt_subsistema", "DT", k), nome=f"improviso.sub.{k}.dt", centro=True)
        cal(ws, f"H{rl}", "=" + N.dcel("dt_subsistema", "Capítulo", k), nome=f"improviso.sub.{k}.cap", ate="I",
            centro=True)
    return rr + 7
