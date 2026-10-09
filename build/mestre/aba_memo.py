# -*- coding: utf-8 -*-
"""
Memoespírito (Fase 4, pedido do usuário depois de jogar em mesa; capítulo 11, 11.3–11.5, e 19.7).

- Aba Grupo, G7 e G8 (M1): cada PJ pode ter um Memoespírito ligado a ele, com os números da ficha do jogador (29.9) e,
  no que ficar vazio, os de 11.4 sem Bênção nem Bônus menor.
- Aba Combate, C2b (M2): "Memoespírito invocado?" Sim/Não; com Sim ele entra na Fila de Ação pela VEL dele (combatentes
  17–22 da tabela de estado, aba_combate_fila.py), com PV e condições próprias (C7), e aparece como "<nome> (de <PJ>)".
  Não tem Tenacidade e nunca fica Quebrado (20.1, 11.5).
"""

from mestre import nucleo as N
from mestre.nucleo import T, ent, cal, av, rot, cabs, titulo
from mestre.aba_combate_base import NPJ, MI0, R_C2B, s

CAMINHO = "A Recordação"


def grupo(ws, r0, rotulo_pj):
    """G7 (preencha) e G8 (automático). Devolve a próxima linha livre."""
    NV, EF, FI = T("campanha.nivel_ef"), T("campanha.ef"), T("campanha.faixa_idx")
    titulo(ws, r0, "G7 · Memoespírito ligado a cada PJ (Recordação, capítulo 11; preencha, da ficha do jogador, 29.9)")
    cabs(ws, r0 + 1, {"A": "PJ dono", "B": "Tem? (Sim/Não)", "C": "Nome dele", "D": "PV máx.", "E": "Defesa",
                      "F": "VEL", "G": "RD", "H": "Pontos em Discernimento", "I": "Pontos em Agilidade",
                      "J": "Pontos em Vigor", "K": ("Aviso", "L")})
    g7 = r0 + 2
    for i in range(1, NPJ + 1):
        r, p, g = g7 + i - 1, f"grupo.pj{i}.memo", f"grupo.pj{i}"
        cal(ws, f"A{r}", rotulo_pj(i), nome=f"{p}.rot7")
        ent(ws, f"B{r}", f"{p}.tem", tipo="lista", fonte="lista.sim_nao", rotulo="Tem Memoespírito", centro=True)
        ent(ws, f"C{r}", f"{p}.nome", maximo=30, rotulo="Nome do Memoespírito")
        for k, col, mx, rt in (("pv", "D", 999, "PV máx. do Memoespírito"), ("def", "E", 40, "Defesa do Memoespírito"),
                               ("vel", "F", 30, "VEL do Memoespírito"), ("rd", "G", 10, "RD do Memoespírito")):
            ent(ws, f"{col}{r}", f"{p}.{k}", tipo="inteiro", minimo=0, maximo=mx, rotulo=rt, centro=True,
                amostra=min(mx, 15))
        for k, col, rt in (("disc", "H", "Pontos em Discernimento"), ("agi", "I", "Pontos em Agilidade"),
                           ("vigor", "J", "Pontos em Vigor")):
            ent(ws, f"{col}{r}", f"{p}.{k}", tipo="inteiro", minimo=0, maximo=5, rotulo=rt, centro=True, amostra=3)
        TEM, CAM, NOME = T(f"{p}.tem"), T(f"{g}.caminho"), T(f"{g}.nome")
        PV, DF, VL = T(f"{p}.pv"), T(f"{p}.def"), T(f"{p}.vel")
        num = lambda k: f'IF(ISNUMBER({T(f"{p}.{k}")}),{T(f"{p}.{k}")},0)'  # noqa: E731
        algum = "&".join(T(f"{p}.{k}") for k in ("nome", "pv", "def", "vel", "rd", "agi", "disc", "vigor"))
        av(ws, f"K{r}", f"{p}.aviso1",
           f'=IF({TEM}="Sim",IF(LEN({NOME})=0,"PJ sem nome em G1: o Memoespírito não entra no Combate",'
           f'IF(AND(LEN({CAM})>0,{CAM}<>"{CAMINHO}"),"O Memoespírito é da Recordação (11.1); este PJ é de outro '
           f'Caminho",IF(AND(ISNUMBER({VL}),{VL}<10+{num("agi")}+1),"VEL abaixo de 10 + Agilidade + 1 (11.4): '
           f'confira na ficha",IF(AND(ISNUMBER({DF}),{DF}<10+{num("agi")}+{EF}),"Defesa abaixo de 10 + Agilidade + '
           f'Eficiência (11.4): confira na ficha",IF(AND(ISNUMBER({PV}),{PV}<8*{NV}+3*{num("vigor")}),"PV abaixo de '
           f'8 × nível + 3 × Vigor (11.4): confira na ficha",IF({num("agi")}+{num("disc")}+{num("vigor")}>12+INT({NV}/2),'
           f'"Pontos acima de 12 + 1 a cada 2 níveis (11.3)","")))))),IF(LEN({algum})>0,"Marque Sim em Tem? para o '
           f'Memoespírito aparecer no Combate",""))', ate="L")
    N.subtabela(ws, "G7", [r0 + 1], "A:L", NPJ)
    r0 = g7 + NPJ + 1
    titulo(ws, r0, "G8 · Memoespírito: os números que o Combate usa (automático; vazio em G7 = 11.4 sem Bênção)")
    cabs(ws, r0 + 1, {"A": "PJ dono", "B": ("Memoespírito", "C"), "D": "PV máx.", "E": "Defesa", "F": "VEL", "G": "RD",
                      "H": ("Dano do ataque (11.4)", "I"), "J": "Redução de Tenacidade", "K": ("Aviso", "L")})
    g8 = r0 + 2
    for i in range(1, NPJ + 1):
        r, p = g8 + i - 1, f"grupo.pj{i}.memo"
        TEM = T(f"{p}.tem")
        on = f'{TEM}="Sim"'
        num = lambda k: f'IF(ISNUMBER({T(f"{p}.{k}")}),{T(f"{p}.{k}")},0)'  # noqa: E731
        usa = lambda k, livro: f'=IF({on},IF(ISNUMBER({T(f"{p}.{k}")}),{T(f"{p}.{k}")},{livro}),"")'  # noqa: E731
        cal(ws, f"A{r}", rotulo_pj(i), nome=f"{p}.rot8")
        cal(ws, f"B{r}", f'=IF({on},IF(LEN({T(f"{p}.nome")})>0,{T(f"{p}.nome")},"(sem nome)"),"—")', nome=f"{p}.nome_v",
            ate="C")
        cal(ws, f"D{r}", usa("pv", f'8*{NV}+3*{num("vigor")}'), nome=f"{p}.pv_ef", centro=True, regra=True)
        cal(ws, f"E{r}", usa("def", f'10+{num("agi")}+{EF}'), nome=f"{p}.def_ef", centro=True, regra=True)
        cal(ws, f"F{r}", usa("vel", f'10+{num("agi")}+1'), nome=f"{p}.vel_ef", centro=True, regra=True)
        cal(ws, f"G{r}", usa("rd", "0"), nome=f"{p}.rd_ef", centro=True, regra=True)
        cal(ws, f"H{r}", f'=IF({on},{FI}&"d6 + pontos no Atributo de ataque ("&({FI}+1)&"d6 se a arma do dono for de '
                         f'Energia)","")', nome=f"{p}.dano", ate="I", regra=True)
        cal(ws, f"J{r}", f'=IF({on},IF({NV}>=11,2,1),"")', nome=f"{p}.rt", centro=True, regra=True)
        vazios = f'OR(NOT(ISNUMBER({T(f"{p}.pv")})),NOT(ISNUMBER({T(f"{p}.def")})),NOT(ISNUMBER({T(f"{p}.vel")})))'
        av(ws, f"K{r}", f"{p}.aviso2", f'=IF(AND({on},{vazios}),"Campo vazio em G7: usando 11.4 sem Bênção nem Bônus '
                                       f'menor; digite o da ficha","")', ate="L")
    N.subtabela(ws, "G8", [r0 + 1], "A:L", NPJ)
    N.constante("memo.pv_por_nivel", 8, "11.4")
    N.constante("memo.pv_por_vigor", 3, "11.4")
    N.constante("memo.base", 10, "11.4")
    N.constante("memo.rt_nivel11", 2, "11.4")
    r = g8 + NPJ
    rot(ws, f"A{r}", "Na mesa (11.5): invocar custa a Ação Complementar do dono e 1 PH; ele tem casa própria na Fila pela "
                     "VEL dele e faz 1 ação por turno (Ataque Básico, uma das 2 Habilidades dele ou Movimento) mais 1 "
                     "Reação; gera metade da Energia para o dono (17); fica até o dono dispensá-lo ou ele cair a 0 PV, "
                     "e então só volta depois do próximo Descanso Curto (23.6). Não tem Tenacidade nem fica Quebrado "
                     "(20.1).", ate="L", italico=True)
    return r + 2


def combate(ws):
    """C2b · Memoespíritos (M2): a chave "Memoespírito invocado?" e PV; a Fila e as condições ficam em C8/C9/C7."""
    r0 = R_C2B
    titulo(ws, r0 - 2, "C2b · Memoespíritos (11.5): Memoespírito invocado? Sim/Não; com Sim ele entra na Fila pela "
                       "VEL dele")
    cabs(ws, r0 - 1, {"A": "Memoespírito (dono)", "B": "Invocado? (Sim/Não)", "C": "Ajuste de VEL",
                      "D": "VEL efetiva", "E": "PV máx.", "F": "PV atual", "G": "Dano agora (− = cura)",
                      "H": "PV depois", "I": "Defesa", "J": "Na Fila?", "K": ("Aviso", "L")})
    for m in range(1, NPJ + 1):
        r, p, i = r0 + m - 1, f"combate.memo{m}", MI0 + m
        g = f"grupo.pj{m}"
        cal(ws, f"A{r}", f'=IF(LEN({s("lab", i)})>0,{s("lab", i)},"Do PJ {m}: nenhum")', nome=f"{p}.rot")
        N.pior(ws, f"A{r}", "Lembrança Antiga do Porto Sete (de Personagem com Nome Bem Comprido)")
        ent(ws, f"B{r}", f"{p}.invocado", tipo="lista", fonte="lista.sim_nao", rotulo="Memoespírito invocado?",
            centro=True)
        ent(ws, f"C{r}", f"{p}.ajvel", tipo="inteiro", minimo=-10, maximo=10, rotulo="Ajuste de VEL", centro=True,
            amostra=2)
        cal(ws, f"D{r}", f'=IF({s("ex", i)}=1,{s("vel", i)},"")', nome=f"{p}.vel", centro=True, regra=True)
        cal(ws, f"E{r}", f'=IF(LEN({s("lab", i)})>0,{s("pvmax", i)},"")', nome=f"{p}.pvmax", centro=True, regra=True)
        ent(ws, f"F{r}", f"{p}.pv", tipo="inteiro", minimo=0, maximo=999, rotulo="PV atual", centro=True, amostra=10)
        ent(ws, f"G{r}", f"{p}.dano", tipo="inteiro", minimo=-999, maximo=999, rotulo="Dano agora", centro=True,
            amostra=5)
        DANO = T(f"{p}.dano")
        dano = f'IF(ISNUMBER({DANO}),INT({DANO}),0)'
        cal(ws, f"H{r}", f'=IF({s("ex", i)}=0,"",IF({dano}>=0,MAX(0,{s("pvat", i)}-{dano}),MIN({s("pvmax", i)},'
                         f'{s("pvat", i)}-{dano})))', nome=f"{p}.pvdepois", centro=True, regra=True)
        cal(ws, f"I{r}", f'=IF(LEN({s("lab", i)})>0,{T(g + ".memo.def_ef")},"")', nome=f"{p}.defesa", centro=True,
            regra=True)
        cal(ws, f"J{r}", f'=IF(LEN({s("lab", i)})=0,"",IF({s("ativo", i)}=1,"Sim",IF({s("ex", i)}=0,"Não",'
                         f'"Não: caiu")))', nome=f"{p}.nafila", centro=True, regra=True)
        INV, PVE = T(f"{p}.invocado"), T(f"{p}.pv")
        av(ws, f"K{r}", f"{p}.aviso",
           f'=IF({INV}<>"Sim","",IF(LEN({s("lab", i)})=0,"Nenhum Memoespírito ligado a este PJ na aba Grupo (G7)",'
           f'IF({s("ex", m)}=0,"O dono não participa deste combate (C1)",IF({s("pvat", i)}=0,"A 0 PV ele some: só '
           f'volta depois do próximo Descanso Curto (11.5)",IF(AND(ISNUMBER({PVE}),{PVE}>{s("pvmax", i)}),'
           f'"PV acima do máximo: usando o máximo",IF({s("pvat", m)}=0,"Dono a 0 PV: a planilha o mantém na Fila '
           f'(H27)",IF(AND({dano}<0,{s("pvat", i)}-{dano}>{s("pvmax", i)}),"Cura acima do máximo: '
           f'"&({s("pvat", i)}-{dano}-{s("pvmax", i)})&" perdida (23.2)","")))))))', ate="L")
    N.subtabela(ws, "C2b", [r0 - 1], "A:L", NPJ)
    r = r0 + NPJ
    rot(ws, f"A{r}", "Invocar (11.5): Ação Complementar do dono e 1 PH (desconte em PH atual, C0); invocado no meio do "
                     "Ciclo, ele entra nas casas restantes, e se a VEL dele passaria de quem está agindo, age logo "
                     "depois (19.7): use Casa manual (C8). Ele não tem Tenacidade, não fica Quebrado nem Congelado "
                     "(20.1, 21.2). Dispensar: Não em invocado.", ate="L", italico=True)
    rot(ws, f"A{r + 1}", "Condições dele vão na C7, nas linhas dele (combatentes 17 a 22); a Energia que ele gera é "
                         "metade da ação, para o dono (17): some na Energia do dono (C1).", ate="L", italico=True)
    N.sugestao(ws, f"A{r + 2}", "H27", "combate.h27.rotulo", ate="L",
               extra="o livro não diz o que acontece com o Memoespírito quando o dono cai a 0 PV nem como ele desempata "
                     "na Fila; a planilha o mantém em campo (11.5 só o tira dispensado ou a 0 PV) e, em empate total de "
                     "VEL, Agilidade e Discernimento, o põe do lado dos jogadores, logo depois dos PJs (19.3 passo 2).")
