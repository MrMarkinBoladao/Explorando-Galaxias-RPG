# -*- coding: utf-8 -*-
"""Abas Campanha (só a Mesa e as calculadas, Fase 1) e Grupo (design §6.2, §6.3, D9, D11)."""

from mestre import nucleo as N
from mestre.nucleo import T, q, ent, cal, av, rot, cabs, titulo, dcol, dbusca, sugestao_formula

ELEMENTOS = ["Físico", "Fogo", "Gelo", "Raio", "Vento", "Quântico", "Imaginário"]
NPJ = 6
ROT2 = {"pv": "PV máx.", "def": "Defesa", "esq": "Esquiva", "rd": "RD", "vel": "VEL", "ag": "Bônus de Agilidade",
        "disc": "Bônus de Discernimento", "pres": "Bônus de Presença", "dt": "DT das Habilidades"}


def montar_campanha(wb):
    ws = wb["Campanha"]
    titulo(ws, 5, "Mesa (preencha uma vez: todas as abas leem daqui — D9)")
    cabs(ws, 6, {"A": "Campo", "B": ("Valor (preencha)", "D"), "E": ("O que a planilha usa (automático)", "J"),
                 "K": ("Aviso", "L")})
    linhas = [
        ("nome", "Nome da campanha", "texto", dict(maximo=60)),
        ("jogadores", "Nº de jogadores", "inteiro", dict(minimo=1, maximo=6)),
        ("nivel", "Nível do grupo", "inteiro", dict(minimo=1, maximo=20)),
        ("sessao", "Sessão atual", "inteiro", dict(minimo=1, maximo=999)),
        ("dia", "Dia de campanha", "inteiro", dict(minimo=1, maximo=9999)),
        ("metodo", "Método de atributos", "lista", dict(fonte='"Array oficial,Compra de Pontos"')),
        ("variantes", "Variantes da mesa", "texto", dict(maximo=200)),
    ]
    r = 7
    for chave, rotulo, tipo, kw in linhas:
        rot(ws, f"A{r}", rotulo, negrito=True)
        ent(ws, f"B{r}", f"campanha.{chave}", tipo=tipo, ate="D", rotulo=rotulo, **kw)
        r += 1
    NIV, JOG = T("campanha.nivel"), T("campanha.jogadores")
    # Calculadas (linhas 7..13, coluna E:J) — explicações curtas e efetivos
    cal(ws, "E7", '="A campanha aparece no título das abas de jogo."', ate="J")
    cal(ws, "E8", f'=IF(ISNUMBER({JOG}),"Jogadores na mesa: "&{T("campanha.jogadores_ef")}&".",'
                  f'"Vazio: usando o nº de PJs da aba Grupo ("&{T("campanha.jogadores_ef")}&").")', ate="J")
    cal(ws, "E9", f'=IF(ISNUMBER({NIV}),"Nível "&{T("campanha.nivel_ef")}&", faixa "&{T("campanha.faixa")}&".",'
                  f'"Vazio: as abas calculam com o nível 1 (faixa 1-4).")', ate="J")
    cal(ws, "E10", '="Lida pela aba Sessões (preparação e diário) e pela Início."', ate="J")
    cal(ws, "E11", '="Usado pela linha do tempo (nesta aba, mais abaixo)."', ate="J")
    cal(ws, "E12", '="Lembrete da Sessão Zero (capítulo 03)."', ate="J")
    cal(ws, "E13", '="Texto livre: média impressa, PV rolado, outra variante (06.4, 28.3)."', ate="J")
    av(ws, "K8", "campanha.aviso.jogadores",
       f'=IF(LEN({JOG})=0,"",IF(NOT(ISNUMBER({JOG})),"Nº de jogadores não é número: usando o nº de PJs do Grupo",'
       f'IF(OR({JOG}<1,{JOG}>6,INT({JOG})<>{JOG}),"Nº de jogadores fora de 1 a 6: usando o limite",'
       f'IF(OR({JOG}<3,{JOG}>6),"Fora da tabela de 16.2 (3 a 6): PH calculado com o limite 3 a 6",""))))',
       ate="L")
    av(ws, "K9", "campanha.aviso.nivel",
       f'=IF(LEN({NIV})=0,"",IF(NOT(ISNUMBER({NIV})),"Nível não é número: usando 1",'
       f'IF(OR({NIV}<1,{NIV}>20,INT({NIV})<>{NIV}),"Nível fora de 1 a 20: usando o limite","")))', ate="L")

    titulo(ws, 15, "Números do grupo (automático)")
    cabs(ws, 16, {"A": "Campo", "B": ("Valor", "C"), "D": ("Fonte no livro", "F"), "G": ("Observação", "L")})
    calcs = [
        ("nivel_ef", "Nível efetivo", f'=IF(ISNUMBER({NIV}),MIN(20,MAX(1,INT({NIV}))),1)', "26.1", "Vazio = 1."),
        ("faixa_idx", "Índice da faixa", f'=INT(({T("campanha.nivel_ef")}-1)/4)+1', "26.3", "1 a 5."),
        ("faixa", "Faixa do grupo", f'=INDEX({dcol("faixas", "Faixa")},{T("campanha.faixa_idx")})', "26.3",
         "A faixa do inimigo é a faixa do grupo (28.4 passo 1)."),
        ("ef", "Eficiência", f'=INDEX({dcol("eficiencia", "Eficiência")},{T("campanha.nivel_ef")})', "26.2 (02.3)",
         "Usada no Dano de Quebra e nas condições."),
        ("jogadores_ef", "Nº de jogadores efetivo",
         f'=IF(ISNUMBER({JOG}),MIN(6,MAX(1,INT({JOG}))),MAX(1,{T("grupo.npjs")}))', "16.2",
         "Vazio = nº de PJs da aba Grupo (mínimo 1)."),
        ("jogadores_ph", "Jogadores para o PH", f'=MIN(6,MAX(3,{T("campanha.jogadores_ef")}))', "16.2",
         "A tabela de 16.2 vai de 3 a 6 jogadores."),
        ("ph_degrau", "Degrau de PH", f'=IF({T("campanha.nivel_ef")}<=8,1,IF({T("campanha.nivel_ef")}<=16,2,3))',
         "16.2", "1 = níveis 1-8; 2 = 9-16; 3 = 17-20."),
        ("ph_max", "PH máximo do grupo", "=" + _ph("Máximo"), "16.2", "Degraus 1-8, 9-16 e 17-20."),
        ("ph_ini", "PH no início do combate", "=" + _ph("Início"), "16.2",
         "Começa cada combate com o máximo menos 2."),
    ]
    r = 17
    for chave, rotulo, f, fonte, obs in calcs:
        rot(ws, f"A{r}", rotulo, negrito=True)
        cal(ws, f"B{r}", f, nome=f"campanha.{chave}", ate="C", regra=True, centro=True)
        rot(ws, f"D{r}", fonte, ate="F")
        rot(ws, f"G{r}", obs, ate="L")
        r += 1
    # DTs da faixa (27.2, 20.2), equipamento e verba (25.1, 24.5)
    FX, FI = T("campanha.faixa"), T("campanha.faixa_idx")
    extras = [
        ("dt_media", "DT Média da faixa", "=" + _dt(FI, 3), "27.2",
         "Regra 1: a faixa é a do desafio, não a do personagem."),
        ("dt_dificil", "DT Difícil da faixa", "=" + _dt(FI, 4), "27.2", ""),
        ("dt_fraqueza", "DT para descobrir Fraqueza", "=" + dbusca("dt_fraqueza", "Faixa", FX, "DT"), "20.2",
         "Pela faixa do inimigo mais forte da cena."),
        ("cone", "Cone de Luz máximo", "=" + dbusca("faixas_equipamento", "Faixa", FX, "Cone de Luz máximo"), "25.1",
         ""),
        ("reliquias", "Relíquias", "=" + dbusca("faixas_equipamento", "Faixa", FX, "Relíquias"), "25.1", ""),
        ("verba", "Verba de marco (Cr)", "=" + dbusca("verba", "Faixa", FX, "Verba de marco (Cr)"), "24.5",
         "Por marco, para o grupo."),
    ]
    cabs(ws, r, {"A": "Campo", "B": ("Valor", "C"), "D": ("Fonte no livro", "F"), "G": ("Observação", "L")})
    r += 1
    for chave, rotulo, f, fonte, obs in extras:
        rot(ws, f"A{r}", rotulo, negrito=True)
        cal(ws, f"B{r}", f, nome=f"campanha.{chave}", ate="C", regra=True, centro=True)
        rot(ws, f"D{r}", fonte, ate="F")
        rot(ws, f"G{r}", obs, ate="L")
        r += 1
    rot(ws, f"A{r + 1}", "Não existe experiência por inimigo derrotado: a progressão é por marco narrativo (26.1).",
        ate="L", italico=True)
    N.subtabela(ws, "campanha.mesa", [6], "A:L", 7)


def escolher(k, exprs):
    """IF encadeado: exprs[0] se k=1, exprs[1] se k=2, … (sem CHOOSE sobre intervalos)."""
    s = exprs[-1]
    for j in range(len(exprs) - 2, -1, -1):
        s = f"IF({k}={j + 1},{exprs[j]},{s})"
    return s


def _dt(fi, linha):
    """DT da linha `linha` (1 = Trivial … 6 = Heroica) da tabela 27.2 na faixa de índice fi."""
    return escolher(fi, [f"INDEX({dcol('dt_faixa', fx)},{linha})" for fx in ("1-4", "5-8", "9-12", "13-16", "17-20")])


def _ph(qual):
    m = f'MATCH({T("campanha.jogadores_ph")},{dcol("ph", "Nº de jogadores")},0)'
    return escolher(T("campanha.ph_degrau"),
                    [f'INDEX({dcol("ph", f"{qual} {d}")},{m})' for d in ("1-8", "9-16", "17-20")])


def montar_grupo(wb):
    ws = wb["Grupo"]
    # "Discernimento" e "Sobreposições" (cabeçalhos em negrito) pedem 115 px; K:L cedem 30 px (soma 1360)
    N.larguras_grade(ws, {**N.GRADE_PX, "C": 120, "D": 125, "E": 115, "H": 115, "K": 118, "L": 116})
    r0 = 5
    # G1 — quem é
    titulo(ws, r0, "G1 · Quem é (preencha, da ficha de cada jogador)")
    cabs(ws, r0 + 1, {"A": "Nome do PJ", "B": "Jogador", "C": "Raça", "D": "Caminho", "E": "Elemento",
                      "F": ("Propósito de Vida", "H"), "I": ("Crença do Esforço (Humano)", "J"), "K": ("Aviso", "L")})
    g1 = r0 + 2
    for i in range(1, NPJ + 1):
        r = g1 + i - 1
        p = f"grupo.pj{i}"
        ent(ws, f"A{r}", f"{p}.nome", maximo=30, rotulo="Nome do PJ")
        ent(ws, f"B{r}", f"{p}.jogador", maximo=30, rotulo="Jogador")
        ent(ws, f"C{r}", f"{p}.raca", tipo="lista", fonte="lista.racas", rotulo="Raça")
        ent(ws, f"D{r}", f"{p}.caminho", tipo="lista", fonte="lista.caminhos", rotulo="Caminho")
        ent(ws, f"E{r}", f"{p}.elemento", tipo="lista", fonte="lista.elementos", rotulo="Elemento")
        ent(ws, f"F{r}", f"{p}.proposito", ate="H", maximo=200, rotulo="Propósito de Vida")
        ent(ws, f"I{r}", f"{p}.crenca", ate="J", maximo=80, rotulo="Crença do Esforço")
        E = T(f"{p}.elemento")
        av(ws, f"K{r}", f"{p}.aviso1",
           f'=IF(AND(LEN({T(f"{p}.raca")})>0,COUNTIF({dcol("racas", "Raça")},{T(f"{p}.raca")})=0),'
           f'"Raça fora da lista do capítulo 05",IF(AND(LEN({E})>0,COUNTIF({T("grupo.col.elemento")},{E})>1),'
           f'"Elemento repetido no grupo: cuidado com a Resistência (regra irmã, 27.5)",'
           f'IF(AND(LEN({T(f"{p}.nome")})=0,LEN({T(f"{p}.raca")}&{E}&{T(f"{p}.caminho")})>0),'
           f'"Linha sem nome: o PJ não entra na contagem","")))', ate="L")
    N.reg("grupo.col.nome", ws, f"A{g1}:A{g1 + NPJ - 1}")
    N.reg("grupo.col.elemento", ws, f"E{g1}:E{g1 + NPJ - 1}")
    N.reg("grupo.col.raca", ws, f"C{g1}:C{g1 + NPJ - 1}")
    N.subtabela(ws, "G1", [r0 + 1], "A:L", NPJ)

    def rotulo_pj(i):
        return f'=IF(LEN({T(f"grupo.pj{i}.nome")})>0,{T(f"grupo.pj{i}.nome")},"PJ {i}")'

    # G2 — números de combate
    r0 = g1 + NPJ + 1
    titulo(ws, r0, "G2 · Números de combate (preencha, da aba Em Jogo da ficha)")
    cabs(ws, r0 + 1, {"A": "PJ", "B": "PV máx.", "C": "Defesa", "D": "Esquiva", "E": "RD", "F": "VEL",
                      "G": "Bônus de Agilidade", "H": "Bônus de Discernimento", "I": "Bônus de Presença",
                      "J": "DT das Habilidades", "K": ("Aviso", "L")})
    g2 = r0 + 2
    campos2 = [("pv", "B", 1, 999), ("def", "C", 5, 40), ("esq", "D", 0, 40), ("rd", "E", 0, 30),
               ("vel", "F", 5, 30), ("ag", "G", -1, 5), ("disc", "H", -1, 5), ("pres", "I", -1, 5),
               ("dt", "J", 5, 40)]
    for i in range(1, NPJ + 1):
        r = g2 + i - 1
        p = f"grupo.pj{i}"
        cal(ws, f"A{r}", rotulo_pj(i), nome=f"{p}.rotulo2")
        for k, col, mn, mx in campos2:
            ent(ws, f"{col}{r}", f"{p}.{k}", tipo="inteiro", minimo=mn, maximo=mx, rotulo=ROT2[k], centro=True,
                amostra=max(mn, 1) if k not in ("ag", "disc", "pres") else 2)
        V = T(f"{p}.vel")
        av(ws, f"K{r}", f"{p}.aviso2",
           f'=IF(AND(ISNUMBER({V}),OR({V}<7,{V}>25)),"VEL fora dos extremos 7 a 25 da fórmula: confira na ficha (19.1)",'
           + "IF(OR(" + ",".join(f'AND(ISNUMBER({T(f"{p}.{k}")}),OR({T(f"{p}.{k}")}<-1,{T(f"{p}.{k}")}>5))'
                                for k in ("ag", "disc", "pres"))
           + '),"Bônus de Atributo fora de -1 a +5: confira na ficha",'
           + f'IF(AND(ISNUMBER({T(f"{p}.pv")}),OR({T(f"{p}.pv")}<1,{T(f"{p}.pv")}>999)),"PV fora de 1 a 999: confira na ficha","")))',
           ate="L")
    N.subtabela(ws, "G2", [r0 + 1], "A:L", NPJ)

    # G3 — equipamento de faixa
    r0 = g2 + NPJ + 1
    titulo(ws, r0, "G3 · Equipamento de faixa (preencha)")
    cabs(ws, r0 + 1, {"A": "PJ", "B": "Nível do Cone", "C": "Tier de Relíquias", "D": "Slots de Relíquia",
                      "E": "Sobreposições nesta faixa", "F": "Total no Cone", "G": ("Ressonâncias escolhidas", "J"),
                      "K": ("Aviso", "L")})
    g3 = r0 + 2
    for i in range(1, NPJ + 1):
        r = g3 + i - 1
        p = f"grupo.pj{i}"
        cal(ws, f"A{r}", rotulo_pj(i), nome=f"{p}.rotulo3")
        ent(ws, f"B{r}", f"{p}.cone", tipo="inteiro", minimo=1, maximo=5, rotulo="Nível do Cone", centro=True)
        ent(ws, f"C{r}", f"{p}.tier", tipo="inteiro", minimo=1, maximo=4, rotulo="Tier de Relíquias", centro=True)
        ent(ws, f"D{r}", f"{p}.slots", tipo="inteiro", minimo=0, maximo=6, rotulo="Slots", centro=True)
        ent(ws, f"E{r}", f"{p}.sobrep", tipo="inteiro", minimo=0, maximo=2, rotulo="Sobreposições", centro=True)
        # 25.2: o teto é do Cone (2 no Nível 1–2, 1 no 3–4, 0 no 5), contando as de faixas anteriores (trocar é
        # opcional, E14): o total no Cone atual, com as desta faixa
        ent(ws, f"F{r}", f"{p}.sobrep_total", tipo="inteiro", minimo=0, maximo=5, rotulo="Sobreposições no Cone",
            centro=True)
        ent(ws, f"G{r}", f"{p}.ress", ate="J", maximo=200, rotulo="Ressonâncias")
        C, S, TO = T(f"{p}.cone"), T(f"{p}.sobrep"), T(f"{p}.sobrep_total")
        TETO = f'INDEX({dcol("cone", "Sobreposições até o teto")},INT({C}))'
        TE = f'MAX(IF(ISNUMBER({TO}),{TO},0),IF(ISNUMBER({S}),{S},0))'
        menor = f'IF(AND(ISNUMBER({TO}),ISNUMBER({S}),{TO}<{S}),"Total no Cone menor que as desta faixa","")'
        av(ws, f"K{r}", f"{p}.aviso3",
           f'=IF(AND(ISNUMBER({C}),{C}>{T("campanha.faixa_idx")}),"Cone acima do máximo da faixa (25.1)",'
           f'IF(AND(ISNUMBER({S}),{S}>1),"Mais de 1 Sobreposição nesta faixa (25.2)",'
           f'IF(AND(ISNUMBER({C}),{C}>=1,{C}<=5),IF({TE}>{TETO},"Acima do teto do Cone (25.2): o Nível "&INT({C})&'
           f'" aceita até "&{TETO},{menor}),{menor})))', ate="L")
    N.subtabela(ws, "G3", [r0 + 1], "A:L", NPJ)

    # G4 — o que a Raça e o equipamento mudam (calculada)
    r0 = g3 + NPJ + 1
    titulo(ws, r0, "G4 · O que a Raça muda no combate (automático)")
    cabs(ws, r0 + 1, {"A": "PJ", "B": "Morrendo com Vantagem?", "C": "Pode ser Executado?", "D": "Esforço?",
                      "E": ("Descobre Fraqueza", "F"), "G": ("Lembrete da Raça", "J"), "K": ("Aviso", "L")})
    g4 = r0 + 2
    for i in range(1, NPJ + 1):
        r = g4 + i - 1
        p = f"grupo.pj{i}"
        RA = T(f"{p}.raca")
        cal(ws, f"A{r}", rotulo_pj(i), nome=f"{p}.rotulo4")
        cal(ws, f"B{r}", "=" + dbusca("racas", "Raça", RA, "Morrendo com Vantagem"), nome=f"{p}.morrendo_vant",
            regra=True, centro=True)
        cal(ws, f"C{r}", "=" + dbusca("racas", "Raça", RA, "Pode ser Executado"), nome=f"{p}.executavel",
            regra=True, centro=True)
        cal(ws, f"D{r}", "=" + dbusca("racas", "Raça", RA, "Esforço"), nome=f"{p}.esforco", regra=True, centro=True)
        cal(ws, f"E{r}", "=" + dbusca("racas", "Raça", RA, "Descobre Fraqueza"), nome=f"{p}.descobre", ate="F",
            regra=True)
        # v1.2 (05 reescrito, E21–E34): o traço que pesa no combate de cada Raça
        cal(ws, f"G{r}", f'=IF({RA}="Vulpes","Raposa Astuta: segunda chance contra a Surpresa (DT 10, 19.3 e 27.3)",'
                         f'IF({RA}="Haloviano","To na sua mente: DT 13 de ativação; a falha gasta o uso (05, 27.3)",'
                         f'IF({RA}="Xianzhouíta","Não pode ser Executado (05, 23.5)",'
                         f'IF({RA}="Intellitron","Descobre Fraqueza com Vantagem e 2 por sucesso (20.2)",'
                         f'IF({RA}="Vidyadhara","Maré que Volta: 1 por Descanso Curto, nível + Vigor PV em si (05)",'
                         f'IF({RA}="Avginiano","Não Foi a Primeira Vez: 1 por combate, metade da duração na falha (05)",'
                         f'IF({RA}="Humano","Esforço: no máximo 1 ponto (05)","")))))))', ate="J")
        # 25.1/25.3 (Fase 3: "Cone ou Tier abaixo do esperado"): Tier I nos níveis 1-6, II 7-12, III 13-17, IV 18-20
        TI, NV = T(f"{p}.tier"), T("campanha.nivel_ef")
        TE = f"IF({NV}<=6,1,IF({NV}<=12,2,IF({NV}<=17,3,4)))"
        av(ws, f"K{r}", f"{p}.aviso4",
           f'=IF(AND(ISNUMBER({T(f"{p}.cone")}),{T(f"{p}.cone")}<{T("campanha.faixa_idx")}),'
           f'"Cone abaixo do esperado: encontros ficam mais duros (27.8)",IF(AND(ISNUMBER({TI}),{TI}<{TE}),'
           f'"Tier abaixo do esperado: encontros ficam mais duros (27.8)",IF(AND(ISNUMBER({TI}),{TI}>{TE}),'
           f'"Tier acima do Tier do nível do grupo (25.1, 25.3)","")))', ate="L")
    N.constante("tier.niveis", [6, 12, 17], "25.3")
    N.subtabela(ws, "G4", [r0 + 1], "A:L", NPJ)

    g5, g6 = _testes(ws, g4 + NPJ + 1, rotulo_pj)
    # Fase 4 (pedido do usuário): o Memoespírito de cada PJ (G7 e G8)
    from mestre import aba_memo
    r_memo = aba_memo.grupo(ws, g6 + NPJ + 1, rotulo_pj)

    # Resumo do grupo
    r0 = r_memo
    titulo(ws, r0, "Resumo do grupo (automático)")
    rot(ws, f"A{r0 + 1}", "Nº de PJs", negrito=True)
    cal(ws, f"B{r0 + 1}", f'=SUMPRODUCT((LEN({T("grupo.col.nome")})>0)*1)', nome="grupo.npjs", regra=True,
        centro=True)
    av(ws, f"C{r0 + 1}", "grupo.aviso.npjs",
       f'=IF(AND(ISNUMBER({T("campanha.jogadores")}),{T("grupo.npjs")}>0,{T("grupo.npjs")}<>{T("campanha.jogadores")}),'
       f'"Nº de PJs diferente do nº de jogadores da aba Campanha","")', ate="L")
    cabs(ws, r0 + 2, {"A": "Elemento", **{chr(66 + k): e for k, e in enumerate(ELEMENTOS)}, "I": "Distintos",
                      "J": "Em dobro"})
    rot(ws, f"A{r0 + 3}", "No grupo?", negrito=True)
    for k, e in enumerate(ELEMENTOS):
        col = chr(66 + k)
        cal(ws, f"{col}{r0 + 3}", f'=IF(COUNTIF({T("grupo.col.elemento")},{q(e)})>0,"Sim","Não")',
            nome=f"grupo.tem.{k + 1}", regra=True, centro=True)
    cal(ws, f"I{r0 + 3}", "=" + "+".join(f'IF({T(f"grupo.tem.{k + 1}")}="Sim",1,0)' for k in range(7)),
        nome="grupo.n_elementos", regra=True, centro=True)
    cal(ws, f"J{r0 + 3}", "=" + "+".join(f'IF(COUNTIF({T("grupo.col.elemento")},{q(e)})>1,1,0)' for e in ELEMENTOS),
        nome="grupo.n_dobro", regra=True, centro=True)
    N.reg("grupo.tem.linha", ws, f"B{r0 + 3}:H{r0 + 3}")
    rot(ws, f"A{r0 + 4}", "Presenças", negrito=True)
    cal(ws, f"B{r0 + 4}",
        f'=IF(COUNTIF({T("grupo.col.raca")},"Intellitron")>0,"Intellitron no grupo: descobre Fraqueza com Vantagem '
        f'e 2 por sucesso (20.2). ","")&IF(COUNTIF({T("grupo.col.raca")},"Humano")>0,"Humano no grupo: Esforço (05). ",'
        f'"")&IF(COUNTIF({T("grupo.col.caminho")},"A Preservação")+COUNTIF({T("grupo.col.caminho")},"A Abundância")>0,'
        f'"Há Caminho de sustentação (27.7).","Sem Preservação nem Abundância: cuidado com o dia de jogo (27.7).")',
        nome="grupo.presencas", ate="L")
    N.reg("grupo.col.caminho", ws, f"D{g1}:D{g1 + NPJ - 1}")
    N.reg("grupo.col.vel", ws, f"F{g2}:F{g2 + NPJ - 1}")
    # Fase 3: os testes que o Mestre pede (G5 e G6)
    PM, NM_ = T("grupo.col.pm"), T("grupo.col.nome")
    rot(ws, f"A{r0 + 5}", "Surpresa", negrito=True)
    cal(ws, f"B{r0 + 5}", f'=IF(SUMPRODUCT(ISNUMBER({PM})*1)=0,"Preencha a Percepção Mental na G5.","Menor Percepção '
                          f'Mental do grupo: "&MIN({PM})&" ("&INDEX({NM_},MATCH(MIN({PM}),{PM},0))&"). Surpresa: Teste '
                          f'de Percepção Mental contra DT 13, fixa em todas as faixas (19.3, 27.3).")',
        nome="grupo.surpresa", ate="L")
    MF = T("grupo.col.fraq")
    rot(ws, f"A{r0 + 6}", "Descobrir Fraqueza", negrito=True)
    cal(ws, f"B{r0 + 6}", f'=IF(SUMPRODUCT(ISNUMBER({MF})*1)=0,"Preencha Pesquisa, Ciência ou Sintonia na G6.",'
                          f'"Melhor total de Pesquisa, Ciência ou Sintonia: "&MAX({MF})&" ("&INDEX({NM_},MATCH(MAX({MF}),'
                          f'{MF},0))&"), contra DT "&{T("campanha.dt_fraqueza")}&" na faixa do grupo (20.2)'
                          f'"&IF(COUNTIF({T("grupo.col.raca")},"Intellitron")>0,"; o Intellitron rola com Vantagem e '
                          f'descobre duas por sucesso (20.2).","."))', nome="grupo.fraqueza", ate="L")
    rot(ws, f"A{r0 + 7}", "VEL esperada", negrito=True)
    rot(ws, f"B{r0 + 7}", "Faixa esperada de VEL (19.1): 10 a 19 no nível 1; 12 a 21 no nível 10; 13 a 24 no nível 20 "
                          "com equipamento. Extremos absolutos da fórmula: 7 e 25.", ate="L")
    return {"g1": g1, "g2": g2, "g3": g3, "g4": g4, "g5": g5, "g6": g6}


# Fase 3 (R9: "os números de cada PJ que o mestre consulta"): os 6 Testes de Resistência (22.1) e as Perícias que o
# Mestre pede na mesa (Percepção, Intuição, Furtividade; Pesquisa, Ciência e Sintonia para descobrir Fraqueza, 20.2),
# com o total que o jogador soma ao d20 (Atributo + Eficiência, ficha do jogador)
TR6 = [("tr_pot", "Potência Física"), ("tr_ref", "Reflexos"), ("tr_rfis", "Resistência Física"),
       ("tr_rmen", "Resistência Mental"), ("tr_pm", "Percepção Mental"), ("tr_fv", "Força de Vontade"),
       ("per_perc", "Percepção"), ("per_int", "Intuição"), ("per_furt", "Furtividade")]
PER6 = [("per_pesq", "Pesquisa"), ("per_cien", "Ciência"), ("per_sint", "Sintonia"), ("per_pers", "Persuasão")]


def _testes(ws, r0, rotulo_pj):
    titulo(ws, r0, "G5 · Testes de Resistência e Perícias de mesa (preencha o total da ficha: o que soma ao d20)")
    cabs(ws, r0 + 1, {"A": "PJ", **{chr(66 + k): t for k, (_, t) in enumerate(TR6)}, "K": ("Aviso", "L")})
    g5 = r0 + 2
    for i in range(1, NPJ + 1):
        r = g5 + i - 1
        p = f"grupo.pj{i}"
        cal(ws, f"A{r}", rotulo_pj(i), nome=f"{p}.rotulo5")
        for k, (c, t) in enumerate(TR6):
            ent(ws, f"{chr(66 + k)}{r}", f"{p}.{c}", tipo="inteiro", minimo=-5, maximo=40, rotulo=t, centro=True,
                amostra=4)
        av(ws, f"K{r}", f"{p}.aviso5", "=IF(OR(" + ",".join(
            f'AND(ISNUMBER({T(f"{p}.{c}")}),OR({T(f"{p}.{c}")}<-5,{T(f"{p}.{c}")}>40))' for c, _ in TR6) +
            '),"Total fora de −5 a +40: confira na ficha","")', ate="L")
    N.reg("grupo.col.pm", ws, f"F{g5}:F{g5 + NPJ - 1}")
    N.subtabela(ws, "G5", [r0 + 1], "A:L", NPJ)
    r0 = g5 + NPJ + 1
    titulo(ws, r0, "G6 · Descobrir Fraqueza (20.2), conversar e o que o Mestre lembra (preencha)")
    cabs(ws, r0 + 1, {"A": "PJ", **{chr(66 + k): t for k, (_, t) in enumerate(PER6)},
                      "F": ("Traços e passivas que o Mestre lembra", "J"), "K": ("Aviso", "L")})
    g6 = r0 + 2
    for i in range(1, NPJ + 1):
        r = g6 + i - 1
        p = f"grupo.pj{i}"
        cal(ws, f"A{r}", rotulo_pj(i), nome=f"{p}.rotulo6")
        for k, (c, t) in enumerate(PER6):
            ent(ws, f"{chr(66 + k)}{r}", f"{p}.{c}", tipo="inteiro", minimo=-5, maximo=40, rotulo=t, centro=True,
                amostra=4)
        ent(ws, f"F{r}", f"{p}.passivas", maximo=200, ate="J", rotulo="Traços e passivas")
        X = [T(f"{p}.{c}") for c, _ in PER6[:3]]
        N.aux(ws, f"N{r}", f'=IF(SUMPRODUCT(ISNUMBER({T(f"{p}.faixa_fraq")})*1)=0,"",MAX({T(f"{p}.faixa_fraq")}))',
              nome=f"{p}.melhor_fraq")
        N.reg(f"{p}.faixa_fraq", ws, f"B{r}:D{r}")
        av(ws, f"K{r}", f"{p}.aviso6", "=IF(OR(" + ",".join(
            f'AND(ISNUMBER({x}),OR({x}<-5,{x}>40))' for x in X + [T(f"{p}.per_pers")]) +
            '),"Total fora de −5 a +40: confira na ficha","")', ate="L")
    N.reg("grupo.col.fraq", ws, f"N{g6}:N{g6 + NPJ - 1}")
    N.subtabela(ws, "G6", [r0 + 1], "A:L", NPJ)
    return g5, g6
