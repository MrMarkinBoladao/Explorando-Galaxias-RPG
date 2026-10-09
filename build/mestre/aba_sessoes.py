# -*- coding: utf-8 -*-
"""
Abas Sessões e Missões (design §6.4, §6.5; R9).

Sessões: preparar a próxima sessão (5 cenas com encontro ligado e a DT da faixa do desafio, 27.2 regra 1; segredos e
pistas; recompensas planejadas; ganchos de Propósito de Vida), checklist de preparo (27.4, 27.5, 27.7, 25.1) e o diário
de 30 sessões (sessões desde o último marco). Missões: 20 linhas com as colunas de "missão" a "recompensa" na ordem da
linha de saída da aba Aventuras (D6), contagem por estado e o aviso H23 (mais de 3 Ativas).
"""

import mestre_sabor as SB
import mestre_dados3 as D3
from mestre import nucleo as N
from mestre import historia as H
from mestre.nucleo import T, q, ent, cal, av, rot, cabs, titulo, dcol, sugestao

NCENAS, NPISTAS, NDIARIO, NMISSOES = 5, 10, 30, 20
ENCONTROS = ("A", "B", "C")


def montar(wb):
    _sessoes(wb["Sessões"])
    _missoes(wb["Missões"])


def _dt(dif, fx_lista):
    """DT da dificuldade `dif` (linha de 27.2) na faixa do desafio (lista "Faixa 9-12"; vazia = a do grupo)."""
    lin = f'MATCH({dif},{dcol("dt_faixa", "Dificuldade")},0)'
    fi = (f'IF(LEN({fx_lista})=0,{T("campanha.faixa_idx")},IFERROR(MATCH({fx_lista},{N.dlista("faixas")},0),'
          f'{T("campanha.faixa_idx")}))')
    return (f'IF(LEN({dif})=0,"",IFERROR(' +
            H.escolher(fi, [f"INDEX({dcol('dt_faixa', fx)},{lin})" for fx in D3.FAIXAS]) + ',""))')


def _sessoes(ws):
    # listas com a seta do Google: "Exploração" (B), "Muito Difícil" (I) e "Faixa 13-16" (J) pedem colunas mais largas
    N.larguras_grade(ws, {**N.GRADE_PX, "B": 125, "C": 95, "D": 95, "E": 95, "I": 125, "J": 115, "K": 130, "L": 130})
    titulo(ws, 5, "Preparar a próxima sessão (preencha)")
    cabs(ws, 6, {"A": "Campo", "B": ("Valor (preencha)", "J"), "K": ("Aviso", "L")})
    rot(ws, "A7", "Sessão nº", negrito=True)
    ent(ws, "B7", "sessoes.prep.n", tipo="inteiro", minimo=1, maximo=999, rotulo="Sessão nº", centro=True, amostra=2)
    cal(ws, "C7", f'="Sessão atual na Mesa: "&IF(ISNUMBER({T("campanha.sessao")}),{T("campanha.sessao")},'
                  f'"(vazia)")&"."', nome="sessoes.prep.atual", ate="J")
    rot(ws, "A8", "Data real", negrito=True)
    ent(ws, "B8", "sessoes.prep.data", maximo=20, ate="D", rotulo="Data real")
    rot(ws, "A9", "Título", negrito=True)
    ent(ws, "B9", "sessoes.prep.titulo", maximo=80, ate="J", rotulo="Título")
    rot(ws, "A10", "Objetivo da sessão", negrito=True)
    ent(ws, "B10", "sessoes.prep.objetivo", maximo=200, ate="J", rotulo="Objetivo da sessão")
    av(ws, "K7", "sessoes.aviso.prep",
       f'=IF(AND(ISNUMBER({T("sessoes.prep.n")}),ISNUMBER({T("campanha.sessao")})),IF({T("sessoes.prep.n")}<'
       f'{T("campanha.sessao")},"Sessão preparada anterior à sessão atual da Mesa",""),"")', ate="L")
    N.subtabela(ws, "sessoes.prep", [6], "A:L", 4)
    # cenas
    titulo(ws, 12, f"{NCENAS} cenas planejadas (a DT usa a faixa do desafio, não a do grupo: 27.2 regra 1)")
    cabs(ws, 13, {"A": "Cena", "B": "Tipo", "C": ("Descrição", "E"), "F": ("NPCs presentes", "G"),
                  "H": "Encontro ligado", "I": "Dificuldade", "J": "Faixa do desafio", "K": ("Aviso", "L")})
    for k in range(1, NCENAS + 1):
        r = 13 + k
        p = f"sessoes.cena.{k}"
        rot(ws, f"A{r}", f"Cena {k}", negrito=True)
        ent(ws, f"B{r}", f"{p}.tipo", tipo="lista", fonte="lista.tipo_cena", rotulo="Tipo de cena")
        ent(ws, f"C{r}", f"{p}.descricao", maximo=200, ate="E", rotulo="Descrição")
        ent(ws, f"F{r}", f"{p}.npcs", maximo=120, ate="G", rotulo="NPCs presentes")
        ent(ws, f"H{r}", f"{p}.encontro", tipo="lista", fonte="lista.encontro_ligado", rotulo="Encontro ligado",
            centro=True)
        ent(ws, f"I{r}", f"{p}.dificuldade", tipo="lista", fonte="lista.dificuldades", rotulo="Dificuldade")
        ent(ws, f"J{r}", f"{p}.faixa", tipo="lista", fonte="lista.faixas", rotulo="Faixa do desafio")
        DIF, FX, EN = T(f"{p}.dificuldade"), T(f"{p}.faixa"), T(f"{p}.encontro")
        av(ws, f"K{r}", f"{p}.aviso",
           f'=IF(AND(LEN({DIF})>0,COUNTIF({dcol("dt_faixa", "Dificuldade")},{DIF})=0),"Dificuldade fora da lista '
           f'(27.2)",IF(AND(LEN({FX})>0,COUNTIF({N.dlista("faixas")},{FX})=0),"Faixa fora da lista: usando a do grupo",'
           f'IF(AND(LEN({EN})>0,{EN}<>"Nenhum",{EN}<>"A",{EN}<>"B",{EN}<>"C"),"Encontro fora da lista (A, B ou C)",'
           f'"")))', ate="L")
    N.reg("sessoes.col.tipo", ws, f"B14:B{13 + NCENAS}")
    N.reg("sessoes.col.encontro", ws, f"H14:H{13 + NCENAS}")
    N.subtabela(ws, "sessoes.cenas", [13], "A:L", NCENAS)
    r0 = 14 + NCENAS
    cabs(ws, r0, {"A": "Cena", "B": "DT (automático)", "C": ("Encontro ligado (aba Encontros)", "F"),
                  "G": ("Contrato da Fraqueza (27.5)", "J"), "K": ("Aviso", "L")})
    for k in range(1, NCENAS + 1):
        r = r0 + k
        p = f"sessoes.cena.{k}"
        rot(ws, f"A{r}", f"Cena {k}", negrito=True)
        cal(ws, f"B{r}", "=" + _dt(T(f"{p}.dificuldade"), T(f"{p}.faixa")), nome=f"{p}.dt", regra=True, centro=True)
        EN = T(f"{p}.encontro")
        enc = "".join(f'IF({EN}="{X}",IF(LEN({T(f"encontros.{X}.nome")}&"")>0,{T(f"encontros.{X}.nome")}&": ",'
                      f'"Encontro {X}: ")&"custo "&{T(f"encontros.{X}.custo")}&" · "&{T(f"encontros.{X}.dificuldade")},'
                      for X in ENCONTROS) + '""' + ")" * 3
        cal(ws, f"C{r}", "=" + enc, nome=f"{p}.encontro_txt", ate="F")
        con = "".join(f'IF({EN}="{X}",{T(f"encontros.{X}.contrato")},' for X in ENCONTROS) + '""' + ")" * 3
        cal(ws, f"G{r}", "=" + con, nome=f"{p}.contrato", ate="J")
    N.subtabela(ws, "sessoes.cenas2", [r0], "A:L", NCENAS)
    # segredos e pistas
    r = r0 + NCENAS + 2
    titulo(ws, r, f"Segredos e pistas ({NPISTAS} linhas)")
    cabs(ws, r + 1, {"A": "Pista", "B": ("Segredo ou pista", "I"), "J": "Revelada?", "K": ("Aviso", "L")})
    for k in range(1, NPISTAS + 1):
        rr = r + 1 + k
        rot(ws, f"A{rr}", f"Pista {k}", negrito=True)
        ent(ws, f"B{rr}", f"sessoes.pista.{k}.texto", maximo=200, ate="I", rotulo="Pista")
        ent(ws, f"J{rr}", f"sessoes.pista.{k}.revelada", tipo="lista", fonte="lista.sim_nao", rotulo="Revelada?",
            centro=True)
    N.reg("sessoes.col.pista", ws, f"B{r + 2}:B{r + 1 + NPISTAS}")
    N.reg("sessoes.col.revelada", ws, f"J{r + 2}:J{r + 1 + NPISTAS}")
    N.subtabela(ws, "sessoes.pistas", [r + 1], "A:L", NPISTAS)
    rr = r + 2 + NPISTAS
    cal(ws, f"A{rr}", f'="Pistas: "&SUMPRODUCT((LEN({T("sessoes.col.pista")})>0)*1)&" · reveladas: "&'
                      f'COUNTIF({T("sessoes.col.revelada")},"Sim")', nome="sessoes.pistas.resumo", ate="L")
    # recompensas planejadas
    rr += 2
    titulo(ws, rr, "Recompensas planejadas")
    rot(ws, f"A{rr + 1}", "Recompensas", negrito=True)
    ent(ws, f"B{rr + 1}", "sessoes.recompensas", maximo=200, ate="J", rotulo="Recompensas planejadas")
    rot(ws, f"A{rr + 2}", "A entrega de marco (verba, Cone, Tier, Ressonância) e os achados de encontro estão na aba "
                          "Recompensas. Amarre cada entrega ao Propósito de Vida de alguém (27.8).", ate="L",
        italico=True)
    # ganchos de Propósito de Vida
    rr += 4
    titulo(ws, rr, "Ganchos de Propósito de Vida (um por PJ; o gancho com nome de personagem inicia um arco, 27.18)")
    cabs(ws, rr + 1, {"A": "PJ (aba Grupo)", "B": ("Propósito de Vida (aba Grupo)", "E"),
                      "F": ("Gancho desta sessão (preencha)", "J"), "K": ("Aviso", "L")})
    for i in range(1, 7):
        r2 = rr + 1 + i
        NM = T(f"grupo.pj{i}.nome")
        cal(ws, f"A{r2}", f'=IF(LEN({NM})>0,{NM},"PJ {i}")', nome=f"sessoes.gancho.{i}.pj")
        PR = T(f"grupo.pj{i}.proposito")
        cal(ws, f"B{r2}", f'=IF(LEN({PR})>0,{PR},"")', nome=f"sessoes.gancho.{i}.proposito", ate="E")
        ent(ws, f"F{r2}", f"sessoes.gancho.{i}.texto", maximo=200, ate="J", rotulo="Gancho")
        av(ws, f"K{r2}", f"sessoes.gancho.{i}.aviso",
           f'=IF(AND(LEN({T(f"sessoes.gancho.{i}.texto")})>0,LEN({NM})=0),"PJ {i} sem nome na aba Grupo","")', ate="L")
    N.subtabela(ws, "sessoes.ganchos", [rr + 1], "A:L", 6)
    rr += 8
    rr = _checklist(ws, rr + 1)
    _diario(ws, rr + 1)


def _checklist(ws, r):
    titulo(ws, r, "Checklist de preparo")
    cabs(ws, r + 1, {"A": "Item", "B": ("O que conferir", "F"), "G": "Feito?", "H": ("Automático", "J"),
                     "K": ("Aviso", "L")})
    TIPOS, ENC = T("sessoes.col.tipo"), T("sessoes.col.encontro")
    NV = T("campanha.nivel_ef")
    itens = [
        ("orcamento", "Orçamento", "O encontro gasta o orçamento da faixa (27.4); metade dele é cena de passagem.",
         f'="Orçamento da faixa para o grupo: "&{T("encontros.orc")}&" PV (aba Encontros)."'),
        ("contrato", "Contrato da Fraqueza", "Pelo menos 3 dos Elementos do grupo como Fraqueza na cena (27.5).",
         "=" + "&".join(f'IF(COUNTIF({ENC},"{X}")>0,"{X}: "&{T(f"encontros.{X}.contrato")}&". ","")'
                        for X in ENCONTROS) + f'&IF(COUNTIF({ENC},"A")+COUNTIF({ENC},"B")+COUNTIF({ENC},"C")=0,'
                                              f'"Nenhum encontro ligado às cenas.","")'),
        ("relogio", "Relógio na ficção", "Um prazo na história para o Descanso Longo não ser um botão (27.7).",
         f'="Relógios a 1 de encher: "&COUNTIF({T("campanha.col.rel_sit")},"Falta 1")&" (aba Campanha)."'),
        ("combates", "Combates do dia", "Dois combates por dia é um dia tranquilo; três é um dia de verdade; quatro "
                                        "é uma emergência (27.7). Vazio = os combates das cenas.", None),
        ("equipamento", "Equipamento de faixa", "Se houve virada de faixa ou de Tier, o Cone e o Tier novos entram "
                                                "(25.1, 27.8).",
         f'=IF(OR({NV}=1,{NV}=5,{NV}=9,{NV}=13,{NV}=17),"Nível "&{NV}&": faixa nova (Cone e Tier)",IF(OR({NV}=7,'
         f'{NV}=18),"Nível "&{NV}&": Tier novo","Nível "&{NV}&": sem virada"))'),
    ]
    rr = r + 2
    for chave, item, texto, auto in itens:
        p = f"sessoes.check.{chave}"
        rot(ws, f"A{rr}", item, negrito=True)
        rot(ws, f"B{rr}", texto, ate="F")
        if chave == "combates":
            ent(ws, f"G{rr}", f"{p}.n", tipo="inteiro", minimo=0, maximo=9, rotulo="Combates do dia", centro=True,
                amostra=3)
            NN = T(f"{p}.n")
            NE = f'IF(ISNUMBER({NN}),{NN},COUNTIF({TIPOS},"Combate"))'
            N.aux(ws, f"N{rr}", f"={NE}", nome=f"{p}.ef")
            E_ = T(f"{p}.ef")
            cal(ws, f"H{rr}", f'=IF({E_}<=0,"Nenhum combate previsto",{E_}&" combate(s): "&IF({E_}<=2,"dia tranquilo",'
                              f'IF({E_}=3,"dia de verdade","emergência, e o grupo deve sentir que é"))&" (27.7)")',
                nome=f"{p}.auto", ate="J")
            av(ws, f"K{rr}", f"{p}.aviso",
               f'=IF(IF(ISNUMBER({NN}),OR({NN}<0,{NN}>9,INT({NN})<>{NN}),FALSE),"Combates fora de 0 a 9",IF({E_}>=4,'
               f'"Quatro combates ou mais no dia é emergência (27.7)",""))', ate="L")
        else:
            ent(ws, f"G{rr}", f"{p}.feito", tipo="lista", fonte="lista.sim_nao", rotulo="Feito?", centro=True)
            cal(ws, f"H{rr}", auto, nome=f"{p}.auto", ate="J")
        rr += 1
    N.subtabela(ws, "sessoes.checklist", [r + 1], "A:L", len(itens))
    return rr


def _diario(ws, r):
    titulo(ws, r, f"Diário de campanha ({NDIARIO} sessões; uma linha por sessão jogada, na ordem)")
    rr = r + 1
    cabs_d1, cabs_d2 = [], []
    linhas = []
    N.titulo(ws, rr, "D1 · A sessão")
    rr += 1
    for i in range(1, NDIARIO + 1):
        if (i - 1) % 10 == 0:
            cabs(ws, rr, {"A": "Sessão nº (preencha)", "B": "Data real", "C": "Dia de campanha", "D": "Marco atingido?",
                          "E": ("Resumo (até 300 caracteres)", "J"), "K": ("Aviso", "L")})
            cabs_d1.append(rr)
            rr += 1
        p = f"sessoes.diario.{i}"
        ent(ws, f"A{rr}", f"{p}.n", tipo="inteiro", minimo=1, maximo=999, rotulo="Sessão nº", centro=True)
        ent(ws, f"B{rr}", f"{p}.data", maximo=20, rotulo="Data real")
        ent(ws, f"C{rr}", f"{p}.dia", tipo="inteiro", minimo=1, maximo=9999, rotulo="Dia de campanha", centro=True)
        ent(ws, f"D{rr}", f"{p}.marco", tipo="lista", fonte="lista.sim_nao", rotulo="Marco atingido?", centro=True)
        ent(ws, f"E{rr}", f"{p}.resumo", maximo=300, ate="J", rotulo="Resumo")
        linhas.append(rr)
        rr += 1
    N.subtabela(ws, "sessoes.diario.d1", cabs_d1, "A:L", NDIARIO)
    N.titulo(ws, rr, "D2 · O que ficou")
    rr += 1
    for i in range(1, NDIARIO + 1):
        if (i - 1) % 10 == 0:
            cabs(ws, rr, {"A": "Sessão", "B": ("Decisões importantes", "D"), "E": ("Ganchos abertos", "G"),
                          "H": ("NPCs que apareceram", "J"), "K": ("Aviso", "L")})
            cabs_d2.append(rr)
            rr += 1
        p = f"sessoes.diario.{i}"
        NN = T(f"{p}.n")
        cal(ws, f"A{rr}", f'=IF(ISNUMBER({NN}),"Sessão "&{NN},"Linha {i}")', nome=f"{p}.rot2")
        ent(ws, f"B{rr}", f"{p}.decisoes", maximo=200, ate="D", rotulo="Decisões importantes")
        ent(ws, f"E{rr}", f"{p}.ganchos", maximo=200, ate="G", rotulo="Ganchos abertos")
        ent(ws, f"H{rr}", f"{p}.npcs", maximo=200, ate="J", rotulo="NPCs que apareceram")
        rr += 1
    N.subtabela(ws, "sessoes.diario.d2", cabs_d2, "A:L", NDIARIO)
    # contadores corridos (colunas ocultas, nas linhas do D1): sessões registradas e "Não" desde o último "Sim"
    for k, (i, lin) in enumerate(zip(range(1, NDIARIO + 1), linhas)):
        p = f"sessoes.diario.{i}"
        MC = T(f"{p}.marco")
        tem = (f'IF(LEN({T(f"{p}.n")}&{T(f"{p}.resumo")}&{T(f"{p}.data")}&{T(f"{p}.dia")}&{MC})>0,1,0)')
        ant_c = "0" if k == 0 else T(f"sessoes.diario.{i - 1}.cont")
        ant_d = "0" if k == 0 else T(f"sessoes.diario.{i - 1}.desde")
        N.aux(ws, f"N{lin}", f"={ant_c}+{tem}", nome=f"{p}.cont")
        N.aux(ws, f"O{lin}", f'=IF({MC}="Sim",0,{ant_d}+IF({MC}="Não",1,0))', nome=f"{p}.desde")
        av(ws, f"K{lin}", f"{p}.aviso",
           f'=IF(AND(LEN({MC})>0,{MC}<>"Sim",{MC}<>"Não"),"Marco: escolha Sim ou Não","")', ate="L")
    ult = NDIARIO
    titulo(ws, rr, "Resumo do diário (automático)")
    cal(ws, f"A{rr + 1}", f'="Sessões registradas: "&{T(f"sessoes.diario.{ult}.cont")}&" · sessões desde o último marco: "'
                          f'&{T(f"sessoes.diario.{ult}.desde")}&" (conta os Não desde o último Sim). Ritmo sugerido: '
                          f'veja Marcos e progressão na aba Campanha (26.1)."', nome="sessoes.diario.resumo", ate="L")
    N.reg("sessoes.diario.total", ws, N.REFS[f"sessoes.diario.{ult}.cont"][1])
    return rr + 2


# ---------------------------------------------------------------------------
# Missões (6.5)
# ---------------------------------------------------------------------------

def _missoes(ws):
    # Tipo (B: "Contenção de Fragmentum") e Estado (I: "Abandonada") são listas: a seta do Google pede largura
    N.larguras_grade(ws, {**N.GRADE_PX, "B": 140, "C": 90, "D": 90, "E": 95, "F": 95, "G": 115, "H": 115, "I": 120,
                          "J": 130, "K": 110, "L": 110})
    titulo(ws, 5, f"Missões ({NMISSOES} linhas): cole a linha de saída da aba Aventuras em A:J da M1 (Colar especial → "
                  f"Somente valores)")
    fonte_tipo = H.lista_com_sortear(ws, "AA", 5, "tipo_aventura", "missoes.lista.tipo", sortear=False)
    rr = 6
    N.titulo(ws, rr, "M1 · A missão (mesma ordem de colunas da linha de saída da aba Aventuras, D6)")
    rr += 1
    cabs1, cabs2, lin1 = [], [], []
    for i in range(1, NMISSOES + 1):
        if (i - 1) % 10 == 0:
            cabs(ws, rr, {"A": "Missão (preencha)", "B": "Tipo", "C": ("Contratante", "D"), "E": ("Objetivo", "F"),
                          "G": "Local", "H": "Prazo", "I": "Estado", "J": "Recompensa combinada", "K": ("Aviso", "L")})
            cabs1.append(rr)
            rr += 1
        p = f"missoes.{i}"
        ent(ws, f"A{rr}", f"{p}.missao", maximo=160, rotulo="Missão")
        ent(ws, f"B{rr}", f"{p}.tipo", tipo="lista", fonte=fonte_tipo, opcoes=list(SB.TIPO_AVENTURA), rotulo="Tipo")
        ent(ws, f"C{rr}", f"{p}.contratante", maximo=200, ate="D", rotulo="Contratante")
        ent(ws, f"E{rr}", f"{p}.objetivo", maximo=200, ate="F", rotulo="Objetivo")
        ent(ws, f"G{rr}", f"{p}.local", maximo=120, rotulo="Local")
        ent(ws, f"H{rr}", f"{p}.prazo", maximo=120, rotulo="Prazo")
        ent(ws, f"I{rr}", f"{p}.estado", tipo="lista", fonte="lista.estado_missao", rotulo="Estado", centro=True)
        ent(ws, f"J{rr}", f"{p}.recompensa", maximo=200, rotulo="Recompensa combinada")
        ES = T(f"{p}.estado")
        av(ws, f"K{rr}", f"{p}.aviso",
           f'=IF(AND(LEN({ES})>0,COUNTIF({N.dlista("estado_missao")},{ES})=0),"Estado fora da lista",'
           f'IF(AND(LEN({T(f"{p}.missao")})=0,LEN({ES}&{T(f"{p}.objetivo")})>0),"Linha sem o nome da missão",""))',
           ate="L")
        lin1.append(rr)
        rr += 1
    N.reg("missoes.col.estado", ws, f"I{lin1[0]}:I{lin1[-1]}")
    N.subtabela(ws, "missoes.m1", cabs1, "A:L", NMISSOES)
    N.titulo(ws, rr, "M2 · O registro (preencha)")
    rr += 1
    lin2 = []
    for i in range(1, NMISSOES + 1):
        if (i - 1) % 10 == 0:
            cabs(ws, rr, {"A": "Missão", "B": "É marco de nível?", "C": "Sessão de início", "D": "Sessão de fim",
                          "E": ("Notas", "J"), "K": ("Aviso", "L")})
            cabs2.append(rr)
            rr += 1
        p = f"missoes.{i}"
        MI = T(f"{p}.missao")
        cal(ws, f"A{rr}", f'=IF(LEN({MI})>0,{MI},"Missão {i}")', nome=f"{p}.rot2")
        ent(ws, f"B{rr}", f"{p}.marco", tipo="lista", fonte="lista.sim_nao", rotulo="É marco de nível?", centro=True)
        ent(ws, f"C{rr}", f"{p}.inicio", tipo="inteiro", minimo=1, maximo=999, rotulo="Sessão de início", centro=True)
        ent(ws, f"D{rr}", f"{p}.fim", tipo="inteiro", minimo=1, maximo=999, rotulo="Sessão de fim", centro=True)
        ent(ws, f"E{rr}", f"{p}.notas", maximo=200, ate="J", rotulo="Notas")
        ES, INI, FIM = T(f"{p}.estado"), T(f"{p}.inicio"), T(f"{p}.fim")
        av(ws, f"K{rr}", f"{p}.aviso2",
           f'=IF(AND({ES}="Concluída",LEN({FIM})=0),"Concluída sem sessão de fim",IF(AND(ISNUMBER({INI}),'
           f'ISNUMBER({FIM})),IF({FIM}<{INI},"Sessão de fim antes da de início",""),""))', ate="L")
        lin2.append(rr)
        rr += 1
    N.reg("missoes.col.marco", ws, f"B{lin2[0]}:B{lin2[-1]}")
    N.subtabela(ws, "missoes.m2", cabs2, "A:L", NMISSOES)
    # contagem por estado e H23
    titulo(ws, rr, "Missões por estado (automático)", ate="J")
    sugestao(ws, f"K{rr}", "H23", "missoes.h23", ate="L")
    cabs(ws, rr + 1, {"A": "Estado", **{chr(66 + k): e for k, e in enumerate(D3.ESTADOS_MISSAO)}, "G": "Total",
                      "H": ("Marcos concluídos", "I")})
    rot(ws, f"A{rr + 2}", "Missões", negrito=True)
    ESC = T("missoes.col.estado")
    for k, e in enumerate(D3.ESTADOS_MISSAO):
        cal(ws, f"{chr(66 + k)}{rr + 2}", f'=COUNTIF({ESC},{q(e)})', nome=f"missoes.n.{N.slug(e)}", centro=True)
    cal(ws, f"G{rr + 2}", "=" + "+".join(T(f"missoes.n.{N.slug(e)}") for e in D3.ESTADOS_MISSAO), nome="missoes.n.total",
        centro=True)
    cal(ws, f"H{rr + 2}", f'=COUNTIFS({ESC},"Concluída",{T("missoes.col.marco")},"Sim")', nome="missoes.n.marcos",
        ate="I", centro=True)
    av(ws, f"A{rr + 3}", "missoes.aviso.ativas",
       f'=IF({T("missoes.n.ativa")}>3,"Mais de 3 missões Ativas: o grupo pode perder o fio — Sugestão da planilha '
       f'(H23)","")', ate="L")
    N.subtabela(ws, "missoes.contagem", [rr + 1], "A:I", 1)
