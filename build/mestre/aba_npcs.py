# -*- coding: utf-8 -*-
"""
Aba NPCs — Criador de NPCs (R5, design §6.6).

Gerador G = 200 (semente da aba Início + Rolagem nº): nome por cultura (05), Raça, Caminho (06.3; "Nenhum" ×3, H11 —
27.12), ocupação, aparência (2 traços, H25), personalidade, motivação (por Caminho, 27.12, ou geral), segredo,
maneirismo e voz, atitude, gancho (50% livro 27.18 da faixa do grupo / 50% tabela, H20) e papel. Bloco de combate
opcional pelas âncoras de 28.3 (o mesmo bloco que o Criador de Inimigos usa no modo "Faixa do livro"), com o caminho
para levá-lo ao combate pela aba Inimigos. Linha de saída em 3 partes na ordem do Elenco (D6); Elenco de 30 NPCs em 4
sub-tabelas (D11, cabeçalho a cada 10); 4 cartões de NPC (R13).
"""

from openpyxl.utils import get_column_letter as L, column_index_from_string as CI

import mestre_dados as D
import mestre_sabor as SB
import mestre_sabor_nomes as NM
from mestre import nucleo as N
from mestre import sorteio as S
from mestre import historia as H
from mestre.nucleo import T, q, ent, cal, av, rot, cabs, titulo, dcol, sugestao, sugestao_formula

G_NPC = 200
NE = 30                     # NPCs no Elenco
NC = 4                      # cartões
R_SAIDA = 32
CAMPOS_RES = [("nome", "Nome completo"), ("raca", "Raça"), ("caminho", "Caminho"), ("ocupacao", "Ocupação"),
              ("aparencia", "Aparência"), ("personalidade", "Personalidade"), ("motivacao", "Motivação"),
              ("segredo", "Segredo"), ("maneirismo", "Maneirismo e voz"), ("atitude", "Atitude com o grupo"),
              ("gancho", "Gancho"), ("papel", "Papel na história")]
# Elenco (= ordem da linha de saída): sub-tabela -> [(campo, título, coluna inicial, coluna final, tipo, máximo)]
# Os campos curtos (Raça, Caminho, Atitude, Papel) são listas suspensas: o que a linha de saída cola já é uma opção
ELENCO = [
    ("E1", "Quem é", [("nome", "Nome completo", "A", None, "texto", 80),
                      ("raca", "Raça", "B", "C", "lista", "lista.racas"),
                      ("caminho", "Caminho", "D", "E", "lista", "lista.caminhos_elenco"),
                      ("papel", "Papel", "F", "G", "lista", "lista.papeis_elenco"),
                      ("ocupacao", "Ocupação", "H", "J", "texto", 120)]),
    ("E2", "Como é", [("aparencia", "Aparência", "B", "E", "texto", 200),
                      ("personalidade", "Personalidade", "F", "J", "texto", 200)]),
    ("E3", "Por dentro", [("motivacao", "Motivação", "B", "E", "texto", 200),
                          ("segredo", "Segredo", "F", "J", "texto", 200)]),
    ("E4", "Na mesa", [("maneirismo", "Maneirismo e voz", "B", "D", "texto", 200),
                       ("atitude", "Atitude", "E", "F", "lista", "atitude"),
                       ("gancho", "Gancho", "G", "J", "texto", 200)]),
    ("E5", "Registro", [("relacao", "Relação (−3 a +3)", "B", None, "inteiro", None),
                        ("vivo", "Vivo?", "C", None, "lista", "lista.sim_nao"),
                        ("sessao", "Sessão em que apareceu", "D", None, "inteiro", None),
                        ("onde", "Onde está", "E", "G", "texto", 120),
                        ("notas", "Notas", "H", "J", "texto", 200)]),
]
SAIDA_PARTES = 4            # E1 a E4 vêm do gerador; E5 é registro do Mestre
AUX_ELENCO = {"nome": "AG", "raca": "AH", "caminho": "AI", "ocupacao": "AJ", "aparencia": "AK", "maneirismo": "AL",
              "motivacao": "AM", "segredo": "AN", "atitude": "AO", "papel": "AP"}
AUX_L0 = 10                 # 1ª linha das colunas auxiliares contíguas do Elenco (cartões e listas)


def montar(wb):
    ws = wb["NPCs"]
    x = _gerador(ws)
    _saida(ws)
    r = _elenco(ws, R_SAIDA + 11)
    _cartoes(ws, r + 1)
    return x


def _gerador(ws):
    titulo(ws, 5, "Gerador de NPCs (G = 200): vazio = Sortear; a semente é a da aba Início")
    cabs(ws, 6, {"A": "Rolagem nº", "B": ("Raça", "C"), "D": ("Caminho", "E"), "F": ("Papel na história", "G"),
                 "H": ("Bloco de combate", "I"), "J": "Tipo do bloco", "K": ("Aviso", "L")})
    ent(ws, "A7", "npcs.rolagem", tipo="inteiro", minimo=1, maximo=1000000, rotulo="Rolagem nº", centro=True,
        amostra=3)
    ent(ws, "B7", "npcs.raca", tipo="lista", fonte="lista.racas_sortear", ate="C", rotulo="Raça")
    ent(ws, "D7", "npcs.caminho", tipo="lista", fonte="lista.caminhos_npc", ate="E", rotulo="Caminho")
    ent(ws, "F7", "npcs.papel", tipo="lista", fonte="lista.papeis", ate="G", rotulo="Papel na história")
    ent(ws, "H7", "npcs.bloco_faixa", tipo="lista", fonte="lista.faixa_bloco", ate="I", rotulo="Bloco de combate")
    ent(ws, "J7", "npcs.bloco_tipo", tipo="lista", fonte="lista.tipo_bloco", rotulo="Tipo do bloco", centro=True)
    rot(ws, "A8", "Rolagem efetiva", negrito=True)
    cal(ws, "B8", S.rolagem_efetiva(T("npcs.rolagem")), nome="npcs.rolagem_ef", centro=True)
    rot(ws, "C8", "Mesma semente e mesma Rolagem nº dão o mesmo NPC; para outro, some 1 na Rolagem nº. Bloco de "
                  "combate vazio = Nenhum; tipo vazio = Comum.", ate="J", italico=True)
    xs = H.campos(ws, G_NPC, "npcs.rolagem_ef", 10, "AA",
                  ["Raça", "Caminho", "papel", "faixa e tipo do bloco", "faixa do grupo (ganchos de 27.18, H20)",
                   "listas tab.* do NPC"])
    RA, CA, PA = T("npcs.raca"), T("npcs.caminho"), T("npcs.papel")
    FB, TB = T("npcs.bloco_faixa"), T("npcs.bloco_tipo")
    rac, cam, pap = dcol("racas", "Raça"), dcol("caminhos", "Caminho"), dcol("papeis", "Papel")
    a = lambda r, f, nome: N.aux(ws, f"N{r}", f, nome=f"npcs.g.{nome}")  # noqa: E731
    g = lambda nome: T(f"npcs.g.{nome}")  # noqa: E731
    a(10, f'=IF(COUNTIF({rac},{RA})>0,{RA},INDEX({rac},INT({xs[1]}*7/2147483647)+1))', "raca")
    a(11, "=" + H.ridx(g("raca")), "ri")
    nome, sob = H.nome_cultura(g("ri"), xs[2], xs[3])
    a(12, "=" + nome, "nome")
    a(13, "=" + sob, "sobrenome")
    a(14, "=" + H.montar_nome(g("ri"), g("nome"), g("sobrenome")), "nome_completo")
    a(15, f'=IF(OR({CA}="Nenhum",COUNTIF({cam},{CA})>0),{CA},{H.sorteia("caminho_npc", xs[4])})', "caminho")
    a(16, "=" + H.sorteia("ocupacao", xs[5]), "ocupacao")
    a(17, "=" + S.escolha(xs[6], H.n("aparencia_traco")), "ap_i1")
    a(18, f'=IF({H.n("aparencia_traco")}<=0,"",{H.k_esimo("aparencia_traco", g("ap_i1"))})', "ap1")
    a(19, "=" + H.sorteia_sem_repetir("aparencia_traco", xs[7], g("ap_i1")), "ap2")
    a(20, f'=IF(LEN({g("ap1")})=0,"",IF(OR({g("ap2")}={g("ap1")},LEN({g("ap2")})=0),{g("ap1")},'
          f'{g("ap1")}&"; "&{g("ap2")}))', "aparencia")
    a(21, "=" + H.sorteia("personalidade", xs[8]), "personalidade")
    # motivação: k-ésima linha de "Motivação por Caminho" cujo Caminho é o do NPC (contador corrido em AE)
    vals = T("tab.motivacao_caminho.valores2")
    mc, _ = H.contador_chave(ws, "AE", 10, "motivacao_caminho", g("caminho"), "npcs.g.mc_col")
    a(22, f"={mc}", "mc_n")
    a(23, f'=IF(OR({g("caminho")}="Nenhum",LEN({g("caminho")})=0,{g("mc_n")}=0),{H.sorteia("motivacao", xs[9])},'
          f'IFERROR(INDEX({vals},MATCH(INT({xs[9]}*{g("mc_n")}/2147483647)+1,{T("npcs.g.mc_col")},0))&"",""))',
      "motivacao")
    a(24, "=" + H.sorteia("segredo", xs[10]), "segredo")
    a(25, "=" + H.sorteia("maneirismo", xs[11]), "maneirismo")
    a(26, "=" + H.sorteia("atitude", xs[12]), "atitude")
    a(27, "=" + S.inteiro(xs[14], 1, 2), "fonte_gancho")
    FI = T("campanha.faixa_idx")
    a(28, "=" + H.escolher(FI, [H.sorteia(f"ganchos_{fx.replace('-', '_')}", xs[13]) for fx in D.FAIXAS]),
      "gancho_livro")
    a(29, "=" + H.sorteia("gancho_npc", xs[13]), "gancho_tab")
    a(30, f'=IF({g("fonte_gancho")}=1,IF(LEN({g("gancho_livro")})>0,{g("gancho_livro")},{g("gancho_tab")}),'
          f'IF(LEN({g("gancho_tab")})>0,{g("gancho_tab")},{g("gancho_livro")}))', "gancho")
    a(31, f'=IF(COUNTIF({pap},{PA})>0,{PA},INDEX({pap},INT({xs[15]}*7/2147483647)+1))', "papel")
    a(33, f'=IF({FB}="Do grupo",{T("campanha.faixa")},{N.faixa_da_lista(FB)})', "bfx")
    a(34, f'=IF({TB}="Elite","Elite","Comum")', "btipo")
    a(35, f'=IF(LEN({g("bfx")})=0,"",{g("bfx")}&"|"&{g("btipo")})', "chave")
    av(ws, "K7", "npcs.aviso.entradas",
       f'=IF(LEN({S.aviso_rolagem(T("npcs.rolagem"))[1:]})>0,{S.aviso_rolagem(T("npcs.rolagem"))[1:]},'
       f'IF(AND(LEN({RA})>0,{RA}<>"Sortear",COUNTIF({rac},{RA})=0),"Raça fora da lista do capítulo 05: sorteando",'
       f'IF(AND(LEN({CA})>0,{CA}<>"Sortear",{CA}<>"Nenhum",COUNTIF({cam},{CA})=0),"Caminho fora da lista: sorteando",'
       f'IF(AND(LEN({PA})>0,{PA}<>"Sortear",COUNTIF({pap},{PA})=0),"Papel fora da lista: sorteando",'
       f'IF(AND(LEN({FB})>0,{FB}<>"Nenhum",{FB}<>"Do grupo",LEN({N.faixa_da_lista(FB)})=0),'
       f'"Bloco de combate fora da lista: sem bloco",IF(AND(LEN({TB})>0,{TB}<>"Comum",{TB}<>"Elite"),'
       f'"Tipo do bloco fora da lista: usando Comum",""))))))', ate="L")
    # resultado
    titulo(ws, 10, "NPC sorteado (automático)")
    cabs(ws, 11, {"A": "Campo", "B": ("Sorteado", "H"), "I": ("De onde vem", "J"), "K": ("Aviso", "L")})
    origem = {
        "nome": f'="Tabelas: nome e sobrenome da cultura "&{g("raca")}&" (estilo de 05)"',
        "raca": f'=IF(COUNTIF({rac},{RA})>0,"Escolhida","Sorteada entre as 7 Raças de 05")',
        "caminho": f'=IF(OR({CA}="Nenhum",COUNTIF({cam},{CA})>0),"Escolhido","Tabelas: Caminho do NPC (06.3; Nenhum ×3, '
                   f'27.12) · {N.ROTULO_SUGESTAO} (H11)")',
        "ocupacao": '="Tabelas: Ocupação (NPC)"',
        "motivacao": f'=IF(OR({g("caminho")}="Nenhum",LEN({g("caminho")})=0,{g("mc_n")}=0),"Tabelas: Motivação (sem '
                     f'Caminho)","Tabelas: Motivação por Caminho (27.12)")',
        "personalidade": '="Tabelas: Personalidade"', "segredo": '="Tabelas: Segredo"',
        "maneirismo": '="Tabelas: Maneirismo e voz"',
        "atitude": f'="Tabelas: Atitude com o grupo · {N.ROTULO_SUGESTAO} (H11)"',
        "papel": f'=IF(COUNTIF({pap},{PA})>0,"Escolhido","Sorteado entre os 7 papéis")',
    }
    vazias = {"ocupacao": ("ocupacao", "Ocupação (NPC)"), "aparencia": ("aparencia_traco", "Traço de aparência"),
              "personalidade": ("personalidade", "Personalidade"), "segredo": ("segredo", "Segredo"),
              "maneirismo": ("maneirismo", "Maneirismo e voz"), "atitude": ("atitude", "Atitude com o grupo")}
    for k, (campo, rotulo) in enumerate(CAMPOS_RES):
        r = 12 + k
        rot(ws, f"A{r}", rotulo, negrito=True)
        src = {"nome": "nome_completo"}.get(campo, campo)
        cal(ws, f"B{r}", f"={g(src)}", nome=f"npcs.res.{campo}", ate="H", negrito=campo == "nome")
        if campo in origem:
            cal(ws, f"I{r}", origem[campo], nome=f"npcs.res.{campo}.origem", ate="J")
        if campo in vazias:
            id_, tit = vazias[campo]
            av(ws, f"K{r}", f"npcs.aviso.{campo}",
               f'=IF({H.n(id_)}<=0,"Lista \'{tit}\' está vazia (aba Tabelas)","")', ate="L")
    rn = 12
    av(ws, f"K{rn}", "npcs.aviso.nome",
       "=" + H.escolher(g("ri"), [f'IF({H.n("nome." + NM.SLUG[c])}+{H.n("sobrenome." + NM.SLUG[c])}<=0,'
                                  f'"Listas de nome da cultura {c} vazias (aba Tabelas)","")' for c in NM.CULTURAS]),
       ate="L")
    ra = 12 + [c for c, _ in CAMPOS_RES].index("aparencia")
    sugestao(ws, f"I{ra}", "H25", "npcs.h25", celulas=[f"B{ra}"], ate="J", extra="2 traços")
    rm = 12 + [c for c, _ in CAMPOS_RES].index("motivacao")
    av(ws, f"K{rm}", "npcs.aviso.motivacao",
       f'=IF(AND({g("mc_n")}=0,{H.n("motivacao")}<=0),"Listas de motivação vazias (aba Tabelas)","")', ate="L")
    rg = 12 + [c for c, _ in CAMPOS_RES].index("gancho")
    cal(ws, f"I{rg}", f'=IF({g("fonte_gancho")}=1,"27.18, faixa "&{T("campanha.faixa")},"Tabelas: Gancho do NPC")&'
                      f'" · {N.ROTULO_SUGESTAO} (H20)"', nome="npcs.res.gancho.origem", ate="J")
    sugestao_formula("npcs.res.gancho.origem", "H20", [f"B{rg}"])
    av(ws, f"K{rg}", "npcs.aviso.gancho",
       f'=IF(LEN({g("gancho")})=0,"Listas de gancho vazias (aba Tabelas)","")', ate="L")
    rc = 12 + [c for c, _ in CAMPOS_RES].index("caminho")
    sugestao_formula("npcs.res.caminho.origem", "H11", [f"B{rc}"])
    rt = 12 + [c for c, _ in CAMPOS_RES].index("atitude")
    sugestao_formula("npcs.res.atitude.origem", "H11", [f"B{rt}"])
    _bloco(ws, g)


def _bloco(ws, g):
    r0 = 25
    titulo(ws, r0, "Bloco de combate (âncoras de 28.3; o mesmo número do Criador de Inimigos no modo Faixa do livro)")
    cabs(ws, r0 + 1, {"A": "Faixa · tipo", "B": "PV", "C": "Defesa", "D": "RD", "E": "Tenacidade", "F": "VEL",
                      "G": "Ataque", "H": "DT dos efeitos", "I": "Teste de Resistência", "J": "Nº de Fraquezas",
                      "K": ("Aviso", "L")})
    CH = g("chave")
    r = r0 + 2
    cal(ws, f"A{r}", f'=IF(LEN({CH})=0,"Sem bloco",{g("bfx")}&" · "&{g("btipo")})', nome="npcs.bloco.rotulo")
    for col, campo, nome, fmt in (("B", "PV", "pv", None), ("C", "Defesa", "defesa", None), ("D", "RD", "rd", None),
                                  ("E", "Tenacidade", "ten", None), ("F", "VEL", "vel", None),
                                  ("G", "Ataque", "ataque", "+"), ("H", "DT dos efeitos", "dt", None),
                                  ("I", "Teste de Resistência", "tr", "+"), ("J", "Nº de Fraquezas", "nfraq", None)):
        v = H.ancora(campo, CH)
        f = f'=IF(LEN({CH})=0,"",{"" if not fmt else chr(34) + "+" + chr(34) + "&"}{v})'
        cal(ws, f"{col}{r}", f, nome=f"npcs.bloco.{nome}", centro=True, regra=True)
    r += 1
    rot(ws, f"A{r}", "Dano por acerto", negrito=True)
    cal(ws, f"B{r}", f'=IF(LEN({CH})=0,"",{H.ancora("Dano por acerto", CH)}&" · média "&'
                     f'{H.ancora("Média do dano", CH)})', nome="npcs.bloco.dano", ate="E", regra=True)
    rot(ws, f"F{r}", "Na Fila", negrito=True)
    cal(ws, f"G{r}", f'=IF(LEN({CH})=0,"","VEL "&{H.ancora("VEL", CH)}&", "&{H.ancora("Firmeza", CH)})',
        nome="npcs.bloco.nafila", ate="J", regra=True)
    r += 1
    cal(ws, f"A{r}", f'=IF(LEN({CH})=0,"Escolha a faixa do bloco (ou Do grupo) para ver os números.","NPC aliado '
                     f'também usa as âncoras de 28.3 (sem Esquiva, PH, Energia nem Ultimate, 28.2); Execução: ser '
                     f'racional pode Executar (23.5).")', nome="npcs.bloco.regra", ate="L")
    r += 1
    cal(ws, f"A{r}", f'=IF(LEN({CH})=0,"","Para levar ao combate: na aba Inimigos, crie uma linha com o nome "&'
                     f'{g("nome_completo")}&", tipo "&{g("btipo")}&" e faixa "&{g("bfx")}&" (modo Faixa do livro); ele '
                     f'entra nas listas de Encontros e Combate.")', nome="npcs.bloco.combate", ate="L")


def _layout_parte(ws, r, parte, saida):
    """Cabeçalho + uma linha (saída) com as colunas da sub-tabela `parte` do Elenco."""
    _, tit, cols = ELENCO[parte]
    d = {"A": "Nome completo" if parte == 0 else f"Parte {parte + 1}"}
    for campo, t, c0, c1, tipo, mx in cols:
        if saida and campo == "relacao":
            continue
        d[c0] = (t, c1) if c1 else t
    cabs(ws, r, d)


def _saida(ws):
    r = R_SAIDA
    titulo(ws, r, "Linha de saída: copie e cole como valores no Elenco (Colar especial → Somente valores)")
    g = lambda nome: T(f"npcs.g.{nome}")  # noqa: E731
    src = {"nome": "nome_completo"}
    for p in range(SAIDA_PARTES):
        _layout_parte(ws, r + 1 + 2 * p, p, True)
        rr = r + 2 + 2 * p
        if p > 0:
            cal(ws, f"A{rr}", f'="Parte {p + 1} de {SAIDA_PARTES}"', nome=f"npcs.saida.p{p + 1}")
        for campo, t, c0, c1, tipo, mx in ELENCO[p][2]:
            if campo == "relacao":
                continue
            cal(ws, f"{c0}{rr}", f"={g(src.get(campo, campo))}", nome=f"npcs.saida.{campo}", ate=c1)
    rot(ws, f"A{r + 9}", "Parte 1: copie A:J e cole em A:J da linha do Elenco E1. Partes 2 a 4: B:J em E2, E3 e E4 "
                         "(a mesma ordem de colunas, D6). Depois, preencha a relação e o registro (E5).", ate="L",
        italico=True)


def _elenco(ws, r0):
    # lista suspensa da Atitude: as vagas da tabela tab.atitude (coluna oculta AT), sem "Sortear"
    fonte_atitude = H.lista_com_sortear(ws, "AT", 10, "atitude", "npcs.lista.atitude", sortear=False)
    titulo(ws, r0, f"Elenco da campanha ({NE} NPCs; preencha ou cole a linha de saída)")
    r = r0 + 1
    for s, (sid, tit, cols) in enumerate(ELENCO):
        if sid == "E5":
            titulo(ws, r, f"{sid} · {tit} (a relação usa a escala −3 a +3 da planilha)", ate="J")
            sugestao(ws, f"K{r}", "H17", "npcs.elenco.h17", ate="L")
        else:
            titulo(ws, r, f"{sid} · {tit}")
        r += 1
        cabecalhos = []
        for i in range(1, NE + 1):
            if (i - 1) % 10 == 0:
                d = {"A": "Nome completo (preencha)" if s == 0 else "NPC"}
                for campo, t, c0, c1, tipo, mx in cols:
                    d[c0] = (t, c1) if c1 else t
                d["K"] = ("Aviso", "L")
                cabs(ws, r, d)
                cabecalhos.append(r)
                r += 1
            p = f"npcs.elenco.{i}"
            if s > 0:
                cal(ws, f"A{r}", f'=IF(LEN({T(f"{p}.nome")})>0,{T(f"{p}.nome")},"NPC {i}")', nome=f"{p}.rot{s + 1}")
            for campo, t, c0, c1, tipo, mx in cols:
                kw = {"maximo": mx} if tipo == "texto" else {}
                if tipo == "inteiro":
                    kw = {"minimo": -3, "maximo": 3, "amostra": 1} if campo == "relacao" else {"minimo": 1,
                                                                                                "maximo": 999}
                if tipo == "lista":
                    if mx == "atitude":
                        kw = {"fonte": fonte_atitude, "opcoes": list(SB.ATITUDE)}
                    else:
                        kw = {"fonte": mx}
                ent(ws, f"{c0}{r}", f"{p}.{campo}", tipo=tipo, ate=c1, rotulo=t, centro=tipo not in ("texto", "lista"),
                    **kw)
            if s == 0:
                NOME = T(f"{p}.nome")
                av(ws, f"K{r}", f"{p}.aviso",
                   f'=IF(LEN({NOME})=0,"",IF(COUNTIF({T("npcs.aux.nome")},{NOME})>1,"Nome repetido no elenco",'
                   f'IF(COUNTIF({dcol("bestiario", "Nome")},{NOME})>0,"Nome igual a uma criatura do Bestiário","")))',
                   ate="L")
            elif sid == "E5":
                REL = T(f"{p}.relacao")
                av(ws, f"K{r}", f"{p}.aviso_rel",
                   f'=IF(LEN({REL})=0,"",IF(NOT(ISNUMBER({REL})),"Relação não é número (−3 a +3)",'
                   f'IF(OR({REL}<-3,{REL}>3,INT({REL})<>{REL}),"Relação fora de −3 a +3","")))', ate="L")
            else:
                av(ws, f"K{r}", f"{p}.aviso{s + 1}", '=""', ate="L")
            r += 1
        N.subtabela(ws, f"elenco.{sid}", cabecalhos, "A:L", NE)
    # colunas auxiliares contíguas (cartões e lista dos cartões)
    for campo, col in AUX_ELENCO.items():
        for i in range(1, NE + 1):
            N.aux(ws, f"{col}{AUX_L0 + i - 1}", f'={T(f"npcs.elenco.{i}.{campo}")}&""', nome=f"npcs.aux.{campo}.{i}")
        N.reg(f"npcs.aux.{campo}", ws, f"{col}{AUX_L0}:{col}{AUX_L0 + NE - 1}")
    return r


def _cartoes(ws, r0):
    titulo(ws, r0, "Cartões de NPC (escolha um NPC do Elenco; imprima em A4 paisagem)")
    r = r0 + 1
    lado = [("A", "B", "E"), ("F", "G", "J")]
    for banda in range(NC // 2):
        idxs = []
        for k in range(2):
            c = banda * 2 + k + 1
            c_rot, c_ent, c_fim = lado[k]
            rot(ws, f"{c_rot}{r}", f"Cartão {c}: NPC", negrito=True)
            ent(ws, f"{c_ent}{r}", f"npcs.cartao{c}.npc", tipo="lista", fonte=T("npcs.aux.nome"), ate=c_fim,
                rotulo="NPC do Elenco", opcoes=[])
            idx = f"npcs.cartao{c}.idx"
            N.aux(ws, f"AR{r0 + c}", f'=IF(LEN({T(f"npcs.cartao{c}.npc")})=0,"",IFERROR(MATCH('
                                     f'{T(f"npcs.cartao{c}.npc")},{T("npcs.aux.nome")},0),""))', nome=idx)
            idxs.append((c, T(idx)))
        av(ws, f"K{r}", f"npcs.cartoes.aviso{banda + 1}",
           "=" + "".join(f'IF(AND(LEN({T(f"npcs.cartao{c}.npc")})>0,NOT(ISNUMBER({ix}))),"Cartão {c}: NPC fora do '
                         f'Elenco",' for c, ix in idxs) + '""' + ")" * len(idxs), ate="L")
        linhas = [("nome", lambda ix: f'INDEX({T("npcs.aux.nome")},{ix})'),
                  ("quem", lambda ix: f'INDEX({T("npcs.aux.raca")},{ix})&" · "&INDEX({T("npcs.aux.caminho")},{ix})&'
                                      f'" · "&INDEX({T("npcs.aux.ocupacao")},{ix})'),
                  ("aparencia", lambda ix: f'"Aparência: "&INDEX({T("npcs.aux.aparencia")},{ix})'),
                  ("voz", lambda ix: f'"Voz: "&INDEX({T("npcs.aux.maneirismo")},{ix})'),
                  ("quer", lambda ix: f'"Quer: "&INDEX({T("npcs.aux.motivacao")},{ix})'),
                  ("esconde", lambda ix: f'"Esconde: "&INDEX({T("npcs.aux.segredo")},{ix})'),
                  ("atitude", lambda ix: f'"Atitude: "&INDEX({T("npcs.aux.atitude")},{ix})&" · Papel: "&'
                                         f'INDEX({T("npcs.aux.papel")},{ix})')]
        for j, (campo, f) in enumerate(linhas, start=1):
            for k, (c, ix) in enumerate(idxs):
                c_rot, _, c_fim = lado[k]
                cal(ws, f"{c_rot}{r + j}", f'=IF(ISNUMBER({ix}),{f(ix)},"")', nome=f"npcs.cartao{c}.{campo}",
                    ate=c_fim, negrito=campo == "nome")
        r += len(linhas) + 2
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.print_area = f"A{r0}:J{r - 1}"
    return r
