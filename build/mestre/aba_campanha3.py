# -*- coding: utf-8 -*-
"""
Aba Campanha, Fase 3 (design §6.2; R9): marcos e progressão (26.1, 26.7), facções e reputação (H17), relógios de
progresso (H16), linha do tempo com os próximos eventos, Ficha de Decisões da Mesa (27.11, 29.11) e Sessão Zero (as
cinco perguntas de 03 e os itens do livro; tom, limites e véus e expectativas são H24).
A Mesa e os números do grupo (Fase 1) continuam em aba_campanha.py; este módulo escreve abaixo deles.
"""

import mestre_dados as D
from mestre import nucleo as N
from mestre import historia as H
from mestre.nucleo import T, q, ent, cal, av, rot, cab, cabs, titulo, dcol, dcel, sugestao

NFAC, NREL, NTL, NPROX = 12, 10, 30, 5
NHAB, NREGRA, NITEM, NNOME = 10, 10, 8, 10


def _texto(id_):
    """Trecho do livro guardado na aba Dados (bloco 'textos')."""
    return N.dtexto(id_)


def montar_gestao(wb):
    ws = wb["Campanha"]
    r = ws.max_row + 2
    r = _marcos(ws, r)
    r = _faccoes(ws, r + 1)
    r = _relogios(ws, r + 1)
    r = _linha_do_tempo(ws, r + 1)
    r = _decisoes(ws, r + 1)
    _sessao_zero(ws, r + 1)


# ---------------------------------------------------------------------------
# Marcos e progressão (26.1, 26.7)
# ---------------------------------------------------------------------------

def _marcos(ws, r):
    NV = T("campanha.nivel_ef")
    titulo(ws, r, "Marcos e progressão (26.1): o grupo sobe de nível junto, por marco narrativo")
    cabs(ws, r + 1, {"A": "Campo", "B": ("Valor", "D"), "E": ("O que a planilha usa (automático)", "J"),
                     "K": ("Aviso", "L")})
    rr = r + 2
    rot(ws, f"A{rr}", "Sessões jogadas no nível atual", negrito=True)
    ent(ws, f"B{rr}", "campanha.sessoes_nivel", tipo="inteiro", minimo=0, maximo=99, ate="D",
        rotulo="Sessões no nível atual", centro=True, amostra=3)
    ate1 = dcel("ritmo", "Ao nível", 1)
    cal(ws, f"E{rr}", f'="Ritmo sugerido: "&IF({NV}<={ate1},{dcel("ritmo", "Texto", 1)},{dcel("ritmo", "Texto", 2)})'
                      f'&" (26.1)."', nome="campanha.ritmo", ate="J", regra=True)
    S = T("campanha.sessoes_nivel")
    mx = f'IF({NV}<={ate1},{dcel("ritmo", "Máximo", 1)},{dcel("ritmo", "Máximo", 2)})'
    av(ws, f"K{rr}", "campanha.aviso.ritmo",
       f'=IF(LEN({S})=0,"",IF(NOT(ISNUMBER({S})),"Sessões não é número",IF(OR({S}<0,{S}>99,INT({S})<>{S}),'
       f'"Sessões fora de 0 a 99",IF({S}>{mx},"Ritmo acima do sugerido (26.1): mais de "&{mx}&" sessões no nível",'
       f'""))))', ate="L")
    rr += 1
    rot(ws, f"A{rr}", "Próxima Ressonância", negrito=True)
    k = f'(COUNTIF({dcol("ressonancias", "Nível")},"<="&{NV})+1)'
    cal(ws, f"B{rr}", f'=IF({k}>4,"Todas (nível 20)","Ressonância "&INDEX({dcol("ressonancias", "Ressonância")},'
                      f'MIN(4,{k}))&" no nível "&INDEX({dcol("ressonancias", "Nível")},MIN(4,{k})))',
        nome="campanha.prox_ress", ate="D", regra=True, centro=True)
    rot(ws, f"E{rr}", "Sempre um marco de história, escolhida com o Mestre na hora (26.1, 26.7). É o lugar natural "
                      "para fechar um capítulo do Propósito de Vida de alguém.", ate="J")
    rr += 1
    rot(ws, f"A{rr}", "Marcos concluídos", negrito=True)
    cal(ws, f"B{rr}", f'=COUNTIFS({T("missoes.col.estado")},"Concluída",{T("missoes.col.marco")},"Sim")',
        nome="campanha.marcos", ate="D", centro=True)
    rot(ws, f"E{rr}", "Missões concluídas que eram marco de nível (aba Missões).", ate="J")
    rr += 1
    rot(ws, f"A{rr}", "Dia de campanha efetivo", negrito=True)
    DIA = T("campanha.dia")
    cal(ws, f"B{rr}", f"=IF(ISNUMBER({DIA}),MAX(1,INT({DIA})),1)", nome="campanha.dia_ef", ate="D", centro=True)
    rot(ws, f"E{rr}", "Vazio = dia 1. A linha do tempo mostra os próximos eventos a partir deste dia.", ate="J")
    rr += 1
    cal(ws, f"A{rr}", "=" + _texto("marco"), nome="campanha.marco.texto", ate="L")
    rr += 1
    rot(ws, f"A{rr}", "Na virada de nível entram o Tier de Relíquia, o Cone de Luz e a verba de marco (26.1): veja a "
                      "entrega de marco na aba Recompensas.", ate="L", italico=True)
    N.subtabela(ws, "campanha.marcos", [r + 1], "A:L", 4)
    return rr + 1


# ---------------------------------------------------------------------------
# Facções e reputação (H17)
# ---------------------------------------------------------------------------

def _faccoes(ws, r):
    titulo(ws, r, f"Facções e reputação ({NFAC} linhas): atitude com o grupo de −3 a +3", ate="J")
    sugestao(ws, f"K{r}", "H17", "campanha.fac.h17", ate="L")
    cabs(ws, r + 1, {"A": "Facção (preencha)", "B": "Atitude (−3 a +3)", "C": ("Leitura (automático)", "D"),
                     "E": ("Relógio ligado", "F"), "G": ("Notas", "I"), "J": "Último contato (sessão)",
                     "K": ("Aviso", "L")})
    fonte = H.lista_com_sortear(ws, "AA", 5, "faccoes", "campanha.lista.faccoes", sortear=False)
    r0 = r + 2
    for i in range(1, NFAC + 1):
        rr = r0 + i - 1
        p = f"campanha.fac.{i}"
        ent(ws, f"A{rr}", f"{p}.nome", tipo="lista", fonte=fonte, opcoes=D.faccoes(), rotulo="Facção")
        ent(ws, f"B{rr}", f"{p}.atitude", tipo="lista", fonte="lista.reputacao", rotulo="Atitude (−3 a +3)",
            centro=True, amostra=1)
        AT = T(f"{p}.atitude")
        cal(ws, f"C{rr}", f'=IF(LEN({AT})=0,"",IF(ISNUMBER({AT}),IFERROR(INDEX({dcol("reputacao", "Leitura")},'
                          f'MATCH({AT},{dcol("reputacao", "Atitude")},0)),""),""))', nome=f"{p}.leitura", ate="D",
            centro=True)
        ent(ws, f"E{rr}", f"{p}.relogio", maximo=60, ate="F", rotulo="Relógio ligado")
        ent(ws, f"G{rr}", f"{p}.notas", maximo=200, ate="I", rotulo="Notas")
        ent(ws, f"J{rr}", f"{p}.ultimo", tipo="inteiro", minimo=1, maximo=999, rotulo="Último contato", centro=True)
        NOME = T(f"{p}.nome")
        av(ws, f"K{rr}", f"{p}.aviso",
           f'=IF(LEN({NOME})=0,IF(LEN({AT}&{T(f"{p}.relogio")}&{T(f"{p}.notas")}&{T(f"{p}.ultimo")})>0,'
           f'"Linha sem facção: preencha a facção",""),IF(COUNTIF({T("campanha.col.fac")},{NOME})>1,'
           f'"Facção repetida: use uma linha por facção (H17)",IF(AND(LEN({AT})>0,LEN({T(f"{p}.leitura")})=0),'
           f'"Atitude fora de −3 a +3 (H17)","")))', ate="L")
    N.reg("campanha.col.fac", ws, f"A{r0}:A{r0 + NFAC - 1}")
    N.subtabela(ws, "campanha.faccoes", [r + 1], "A:L", NFAC)
    return r0 + NFAC


# ---------------------------------------------------------------------------
# Relógios de progresso (H16)
# ---------------------------------------------------------------------------

def _relogios(ws, r):
    titulo(ws, r, f"Relógios de progresso ({NREL} linhas): 4, 6, 8, 10 ou 12 segmentos", ate="J")
    sugestao(ws, f"K{r}", "H16", "campanha.rel.h16", ate="L")
    cabs(ws, r + 1, {"A": "Relógio (preencha)", "B": "Segmentos", "C": "Preenchidos", "D": ("Barra (automático)", "F"),
                     "G": ("Situação (automático)", "H"), "I": ("O que acontece ao encher", "J"), "K": ("Aviso", "L")})
    r0 = r + 2
    for i in range(1, NREL + 1):
        rr = r0 + i - 1
        p = f"campanha.rel.{i}"
        ent(ws, f"A{rr}", f"{p}.nome", maximo=60, rotulo="Relógio")
        ent(ws, f"B{rr}", f"{p}.seg", tipo="lista", fonte="lista.segmentos", rotulo="Segmentos", centro=True, amostra=6)
        ent(ws, f"C{rr}", f"{p}.n", tipo="inteiro", minimo=0, maximo=12, rotulo="Preenchidos", centro=True, amostra=2)
        ent(ws, f"I{rr}", f"{p}.ao_encher", maximo=200, ate="J", rotulo="O que acontece ao encher")
        S, NN = T(f"{p}.seg"), T(f"{p}.n")
        N.aux(ws, f"N{rr}", f"=IF(ISNUMBER({S}),IF(OR({S}=4,{S}=6,{S}=8,{S}=10,{S}=12),1,0),0)", nome=f"{p}.s_ok")
        N.aux(ws, f"O{rr}", f'=IF(LEN({NN})=0,0,{NN})', nome=f"{p}.n_ef")
        SOK, NE = T(f"{p}.s_ok"), T(f"{p}.n_ef")
        N.aux(ws, f"P{rr}", f"=IF({SOK}=1,IF(ISNUMBER({NE}),IF(AND({NE}>=0,INT({NE})={NE},{NE}<={S}),1,0),0),0)",
              nome=f"{p}.ok")
        OK = T(f"{p}.ok")
        cal(ws, f"D{rr}", f'=IF({OK}=1,REPT("●",{NE})&REPT("○",{S}-{NE})&" "&{NE}&"/"&{S},"")', nome=f"{p}.barra",
            ate="F", centro=True)
        cal(ws, f"G{rr}", f'=IF({OK}=1,IF({NE}={S},"Cheio — aconteceu",IF({NE}={S}-1,"Falta 1","")),"")',
            nome=f"{p}.situacao", ate="H", centro=True)
        av(ws, f"K{rr}", f"{p}.aviso",
           f'=IF(LEN({T(f"{p}.nome")}&{S}&{NN})=0,"",IF({SOK}=0,IF(LEN({S})=0,"Escolha os segmentos: 4, 6, 8, 10 ou 12 '
           f'(H16)","Segmentos fora de 4, 6, 8, 10 ou 12 (H16)"),IF(NOT(ISNUMBER({NE})),"Preenchidos não é número '
           f'(H16)",IF(OR({NE}<0,INT({NE})<>{NE}),"Preenchidos fora de 0 a "&{S}&" (H16)",IF({NE}>{S},'
           f'"Preenchidos acima dos segmentos: confira (H16)","")))))', ate="L")
    N.reg("campanha.col.rel_sit", ws, f"G{r0}:G{r0 + NREL - 1}")
    N.reg("campanha.col.rel_nome", ws, f"A{r0}:A{r0 + NREL - 1}")
    N.subtabela(ws, "campanha.relogios", [r + 1], "A:L", NREL)
    rr = r0 + NREL
    cal(ws, f"A{rr}", f'="Relógios a 1 segmento de encher: "&COUNTIF({T("campanha.col.rel_sit")},"Falta 1")&" · cheios: "'
                      f'&COUNTIF({T("campanha.col.rel_sit")},"Cheio — aconteceu")&". O livro pede relógio na ficção '
                      f'para o Descanso Longo (27.7): a nave parte ao amanhecer, o lacre não aguenta mais um dia."',
        nome="campanha.rel.resumo", ate="L")
    return rr + 1


# ---------------------------------------------------------------------------
# Linha do tempo e próximos eventos
# ---------------------------------------------------------------------------

def _linha_do_tempo(ws, r):
    titulo(ws, r, f"Linha do tempo ({NTL} eventos): a ordem e os próximos eventos são automáticos")
    rr = r + 1
    cab_linhas, dados = [], []
    hoje = T("campanha.dia_ef")
    for i in range(1, NTL + 1):
        if (i - 1) % 10 == 0:
            cabs(ws, rr, {"A": "Dia de campanha (preencha)", "B": "Nº na ordem (automático)", "C": "Sessão",
                          "D": ("Evento", "F"), "G": "Quem (facção ou NPC)", "H": ("Consequência", "I"),
                          "J": "Público?", "K": ("Aviso", "L")})
            cab_linhas.append(rr)
            rr += 1
        p = f"campanha.tl.{i}"
        ent(ws, f"A{rr}", f"{p}.dia", tipo="inteiro", minimo=1, maximo=9999, rotulo="Dia de campanha", centro=True,
            amostra=3)
        ent(ws, f"C{rr}", f"{p}.sessao", tipo="inteiro", minimo=1, maximo=999, rotulo="Sessão", centro=True)
        ent(ws, f"D{rr}", f"{p}.evento", maximo=200, ate="F", rotulo="Evento")
        ent(ws, f"G{rr}", f"{p}.quem", maximo=80, rotulo="Quem")
        ent(ws, f"H{rr}", f"{p}.consequencia", maximo=200, ate="I", rotulo="Consequência")
        ent(ws, f"J{rr}", f"{p}.publico", tipo="lista", fonte="lista.sim_nao", rotulo="Público?", centro=True)
        DI = T(f"{p}.dia")
        N.aux(ws, f"Q{rr}", f'=IF(ISNUMBER({DI}),IF(AND({DI}>=1,{DI}<=9999,INT({DI})={DI}),{DI}+{i}/100,""),"")',
              nome=f"{p}.chave")
        K = T(f"{p}.chave")
        N.aux(ws, f"R{rr}", f'=IF(ISNUMBER({K}),IF(INT({K})>={hoje},{K},""),"")', nome=f"{p}.fut")
        cal(ws, f"B{rr}", f'=IF(ISNUMBER({K}),COUNTIF({T("campanha.tl.chaves")},"<"&{K})+1,"")', nome=f"{p}.ordem",
            centro=True)
        av(ws, f"K{rr}", f"{p}.aviso",
           f'=IF(LEN({DI})=0,IF(LEN({T(f"{p}.evento")}&{T(f"{p}.quem")}&{T(f"{p}.consequencia")}&'
           f'{T(f"{p}.sessao")})>0,"Sem dia: o evento fica fora da ordem",""),IF(ISNUMBER({K}),"",'
           f'"Dia fora de 1 a 9.999 (inteiro)"))', ate="L")
        dados.append(rr)
        rr += 1
    a, b = dados[0], dados[-1]
    for nome, col in (("chaves", "Q"), ("futs", "R"), ("dias", "A"), ("sessoes", "C"), ("eventos", "D"),
                      ("quem", "G"), ("consequencias", "H"), ("publicos", "J")):
        N.reg(f"campanha.tl.{nome}", ws, f"{col}{a}:{col}{b}")
    N.subtabela(ws, "campanha.linha_do_tempo", cab_linhas, "A:L", NTL)
    # próximos eventos (SMALL + MATCH sobre as chaves dia + linha/100, só as de hoje em diante)
    titulo(ws, rr, f"Próximos eventos agendados (os {NPROX} primeiros a partir do dia de hoje)")
    rr += 1
    cal(ws, f"A{rr}", f'="A partir do dia "&{hoje}&" (Dia de campanha, na Mesa). "&IF(SUMPRODUCT(ISNUMBER('
                      f'{T("campanha.tl.futs")})*1)=0,"Nenhum evento agendado de hoje em diante.",'
                      f'SUMPRODUCT(ISNUMBER({T("campanha.tl.futs")})*1)&" evento(s) de hoje em diante.")',
        nome="campanha.prox.resumo", ate="L")
    rr += 1
    cabs(ws, rr, {"A": "Dia", "B": "Faltam (dias)", "C": "Sessão", "D": ("Evento", "F"), "G": "Quem",
                  "H": ("Consequência", "I"), "J": "Público?"})
    c0 = rr
    rr += 1
    for k in range(1, NPROX + 1):
        p = f"campanha.prox.{k}"
        N.aux(ws, f"S{rr}", f'=IFERROR(SMALL({T("campanha.tl.futs")},{k}),"")', nome=f"{p}.chave")
        N.aux(ws, f"T{rr}", f'=IF(ISNUMBER({T(f"{p}.chave")}),IFERROR(MATCH({T(f"{p}.chave")},'
                            f'{T("campanha.tl.futs")},0),""),"")', nome=f"{p}.idx")
        IX = T(f"{p}.idx")
        for col, campo, ate in (("A", "dias", None), ("C", "sessoes", None), ("D", "eventos", "F"), ("G", "quem", None),
                                ("H", "consequencias", "I"), ("J", "publicos", None)):
            cal(ws, f"{col}{rr}", f'=IF(ISNUMBER({IX}),INDEX({T(f"campanha.tl.{campo}")},{IX}),"")',
                nome=f"{p}.{campo}", ate=ate, centro=col in ("A", "C", "J"))
        cal(ws, f"B{rr}", f'=IF(ISNUMBER({T(f"{p}.dias")}),{T(f"{p}.dias")}-{hoje},"")', nome=f"{p}.faltam",
            centro=True)
        rr += 1
    N.subtabela(ws, "campanha.proximos", [c0], "A:J", NPROX)
    return rr


# ---------------------------------------------------------------------------
# Ficha de Decisões da Mesa (27.11, 29.11)
# ---------------------------------------------------------------------------

def _decisoes(ws, r):
    titulo(ws, r, "Ficha de Decisões da Mesa (27.11, 29.11): a decisão de hoje é precedente amanhã")
    rot(ws, f"A{r + 1}", "Vai para a ficha: método de atributos, variantes em uso, toda Habilidade aprovada com ajuste, "
                         "todo caso-limite decidido, todo nome criado pela mesa. Não vai: resultado de rolagem, dano "
                         "sofrido, condição ativa; isso é ficha de personagem e Trilha de Ação (29.11).", ate="L",
        italico=True)
    MET, VAR = T("campanha.metodo"), T("campanha.variantes")
    cal(ws, f"A{r + 2}", f'="Método de atributos: "&IF(LEN({MET})>0,{MET},"(preencha na Mesa)")&" · Tamanho da mesa: "&'
                         f'{T("campanha.jogadores_ef")}&" jogadores → PH máximo "&{T("campanha.ph_max")}&" / início "&'
                         f'{T("campanha.ph_ini")}&" (16.2) · Variantes em uso: "&IF(LEN({VAR})>0,{VAR},'
                         f'"nenhuma anotada")', nome="campanha.dec.mesa", ate="L")
    rr = r + 3
    # Habilidades e Ultimates aprovadas com ajuste
    N.titulo(ws, rr, "Habilidades e Ultimates aprovadas com ajuste")
    cabs(ws, rr + 1, {"A": "Quem", "B": ("Nome", "C"), "D": ("O que foi ajustado", "G"), "H": ("Por quê", "J"),
                      "K": ("Aviso", "L")})
    c0 = rr + 1
    rr += 2
    for i in range(1, NHAB + 1):
        p = f"campanha.dec.hab.{i}"
        ent(ws, f"A{rr}", f"{p}.quem", maximo=40, rotulo="Quem")
        ent(ws, f"B{rr}", f"{p}.nome", maximo=80, ate="C", rotulo="Nome")
        ent(ws, f"D{rr}", f"{p}.ajuste", maximo=200, ate="G", rotulo="O que foi ajustado")
        ent(ws, f"H{rr}", f"{p}.porque", maximo=200, ate="J", rotulo="Por quê")
        rr += 1
    N.subtabela(ws, "campanha.dec.hab", [c0], "A:L", NHAB)
    for chave, tit, cab_a, cab_b, n in (("regra", "Regras decididas na mesa (casos-limite que o livro não cobriu)",
                                         "Regra", "O que foi decidido", NREGRA),
                                        ("item", "Armas, itens e efeitos caseiros aceitos", "Item",
                                         "O que foi aceito, e como", NITEM)):
        N.titulo(ws, rr, tit)
        cabs(ws, rr + 1, {"A": cab_a, "B": (cab_b, "J"), "K": ("Aviso", "L")})
        c0 = rr + 1
        rr += 2
        for i in range(1, n + 1):
            rot(ws, f"A{rr}", f"{cab_a} {i}", negrito=True)
            ent(ws, f"B{rr}", f"campanha.dec.{chave}.{i}", maximo=200, ate="J", rotulo=cab_b)
            rr += 1
        N.subtabela(ws, f"campanha.dec.{chave}", [c0], "A:L", n)
    N.titulo(ws, rr, "Nomes que a mesa criou (facções, lugares, pessoas)")
    cabs(ws, rr + 1, {"A": "Nome", "B": ("Tipo", "C"), "D": ("Notas", "J"), "K": ("Aviso", "L")})
    c0 = rr + 1
    rr += 2
    for i in range(1, NNOME + 1):
        p = f"campanha.dec.nome.{i}"
        ent(ws, f"A{rr}", f"{p}.nome", maximo=60, rotulo="Nome")
        ent(ws, f"B{rr}", f"{p}.tipo", tipo="lista", fonte="lista.tipo_nome", ate="C", rotulo="Tipo")
        ent(ws, f"D{rr}", f"{p}.notas", maximo=200, ate="J", rotulo="Notas")
        rr += 1
    N.subtabela(ws, "campanha.dec.nomes", [c0], "A:L", NNOME)
    return rr


# ---------------------------------------------------------------------------
# Sessão Zero
# ---------------------------------------------------------------------------

# (chave, item, texto ou None = trecho do livro / fórmula, seções citadas, palavra que a seção tem) — a suíte texto
# confere que cada seção citada existe e contém a palavra (H24: nenhum item cita regra fora da seção indicada)
SESSAO_ZERO = [
    ("tom", "Tom e temas", "o clima da campanha (aventura, intriga, horror educado) e os temas que a mesa quer "
                           "explorar", None, None),
    ("limites", "Limites e véus", "o que não entra em jogo de jeito nenhum (linhas) e o que acontece fora de cena "
                                  "(véus); qualquer pessoa pode pedir para parar uma cena", None, None),
    ("expectativas", "Expectativas", "frequência e duração das sessões, quanto de combate e quanto de história, quem "
                                     "aprova o conteúdo escrito pelos jogadores", None, None),
    ("mesa1", "Pergunta 1 da mesa", None, ("03",), "Compra de Pontos"),
    ("mesa2", "Pergunta 2 da mesa", None, ("03", "27.5"), "Elementos"),
    ("mesa3", "Pergunta 3 da mesa", None, ("03", "27.7"), "cuidando do grupo"),
    ("mesa4", "Pergunta 4 da mesa", None, ("03", "19.1"), "VEL"),
    ("mesa5", "Pergunta 5 da mesa", None, ("03",), "Propósitos de Vida"),
    ("ph", "Tamanho da mesa", None, ("16.2",), "Máximo de PH"),
    ("variantes", "Variantes", "PV rolado ou valor fixo (06.4); usar a média do dano dos inimigos em vez de rolar "
                               "(28.3)", ("06.4", "28.3"), "PV rolado"),
    ("ouro", "Regra de Ouro", None, ("27.1",), "Regra de Ouro"),
    ("falhe", "Falhe para frente", None, ("27.1", "02"), "Falhe para frente"),
    ("expresso", "A casa do grupo", None, ("27.15",), "casa do grupo"),
    ("nao_cobre", "O que o livro não cobre", "nave e viagem, economia detalhada, grade, duelos entre personagens e "
                                             "níveis acima de 20 ficam fora; o que a mesa inventar vai para a Ficha "
                                             "de Decisões (27.19)", ("27.19",), "não cobre"),
    ("marco", "Como se sobe de nível", None, ("26.1",), "Não existe experiência por inimigo derrotado"),
    ("recompensa", "Recompensa de marco", None, ("27.8", "25.1"), "Não existe compra de Relíquia"),
]
_TEXTO_DO_LIVRO = {"mesa1": "mesa.1", "mesa2": "mesa.2", "mesa3": "mesa.3", "mesa4": "mesa.4", "mesa5": "mesa.5",
                   "ouro": "regra_ouro", "falhe": "falhe", "expresso": "expresso", "marco": "marco",
                   "recompensa": "sem_compra"}
_SECAO_DO_TEXTO = {"mesa1": "03", "mesa2": "03", "mesa3": "03", "mesa4": "03", "mesa5": "03", "ouro": "27.1",
                   "falhe": "27.1", "expresso": "27.15", "marco": "26.1", "recompensa": "27.8"}
COMBINADOS = [("tom", "Tom"), ("temas", "Temas"), ("linhas", "Linhas (não entram em jogo)"),
              ("veus", "Véus (acontecem fora de cena)"), ("expectativas", "Expectativas da mesa")]


def _sessao_zero(ws, r):
    titulo(ws, r, "Sessão Zero (antes da primeira sessão): o que combinar com a mesa")
    cabs(ws, r + 1, {"A": "Item", "B": ("O que combinar (e onde está no livro)", "G"), "H": "Feito?",
                     "I": ("Nota", "J"), "K": ("Aviso", "L")})
    rr = r + 2
    for chave, item, texto, secoes, _ in SESSAO_ZERO:
        rot(ws, f"A{rr}", item, negrito=True)
        nome = f"campanha.sz.{chave}"
        if secoes is None:                   # H24: prática geral de RPG que o livro não traz
            sugestao(ws, f"B{rr}", "H24", f"{nome}.h24", ate="G", extra=texto)
        elif chave in _TEXTO_DO_LIVRO:
            cal(ws, f"B{rr}", f'={_texto(_TEXTO_DO_LIVRO[chave])}&" ({_SECAO_DO_TEXTO[chave]})"', nome=f"{nome}.texto",
                ate="G")
        elif chave == "ph":
            cal(ws, f"B{rr}", f'="Máximo de PH = 1 + número de personagens jogadores: com "&{T("campanha.jogadores_ef")}'
                              f'&" jogadores, PH máximo "&{T("campanha.ph_max")}&" e início "&{T("campanha.ph_ini")}&'
                              f'" nesta faixa (16.2)."', nome=f"{nome}.texto", ate="G")
        else:
            rot(ws, f"B{rr}", texto[0].upper() + texto[1:] + ("." if not texto.endswith(")") else "."), ate="G")
            N.reg(f"{nome}.texto", ws, f"B{rr}")
        ent(ws, f"H{rr}", f"{nome}.feito", tipo="lista", fonte="lista.sim_nao", rotulo="Feito?", centro=True)
        ent(ws, f"I{rr}", f"{nome}.nota", maximo=200, ate="J", rotulo="Nota")
        rr += 1
        if rr - (r + 2) == 13 and chave != SESSAO_ZERO[-1][0]:      # cabeçalho repetido (D11: 13 linhas)
            cabs(ws, rr, {"A": "Item", "B": ("O que combinar (e onde está no livro)", "G"), "H": "Feito?",
                          "I": ("Nota", "J"), "K": ("Aviso", "L")})
            rr += 1
    N.titulo(ws, rr, "Combinados da mesa (anote o que foi decidido)", ate="J")
    sugestao(ws, f"K{rr}", "H24", "campanha.sz.combinados.h24", ate="L")
    cabs(ws, rr + 1, {"A": "Combinado", "B": ("O que a mesa decidiu", "J"), "K": ("Aviso", "L")})
    rr += 2
    for chave, rotulo in COMBINADOS:
        rot(ws, f"A{rr}", rotulo, negrito=True)
        ent(ws, f"B{rr}", f"campanha.sz.comb.{chave}", maximo=200, ate="J", rotulo=rotulo)
        rr += 1
    return rr
