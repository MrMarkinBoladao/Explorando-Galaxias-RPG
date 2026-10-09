# -*- coding: utf-8 -*-
"""
Aba Combate — Rastreador de combate (R4, design §6.10, D7). Sem macro: todo estado é entrada do Mestre.

22 combatentes (6 PJs da aba Grupo + 10 inimigos do encontro carregado ou escolhidos na lista: o inimigo escolhido
preenche os próprios dados a partir do catálogo da aba Inimigos + os 6 Memoespíritos dos PJs, Fase 4). Sub-tabelas
C0…C10, C2b e C9b (D11).
- C0 e PJs (C1, C2): este arquivo. Memoespíritos (C2b): aba_memo.py.
- Inimigos C3–C6, fases do Boss (28.5) e Quebra (20.4, 20.5): aba_combate_inimigos.py.
- Fila de Ação C8/C9 (19.3–19.6, H13), condições C7 (21.5) e calculadora C10: aba_combate_fila.py.
"""

from mestre import nucleo as N
from mestre import aba_combate_fila, aba_combate_inimigos, aba_memo
from mestre.nucleo import T, ent, cal, av, rot, cabs, titulo
from mestre.aba_combate_base import NPJ, R_C1, R_C2, s, srng, erng


def montar(wb):
    ws = wb["Combate"]
    N.larguras_grade(ws, {**N.GRADE_PX, "C": 120, "K": 145, "L": 145})     # C: listas de nomes longos (Trocar por)
    _c0(ws)
    _pjs(ws)
    aba_memo.combate(ws)
    aba_combate_inimigos.montar(ws)
    aba_combate_fila.montar(ws)


def _c0(ws):
    titulo(ws, 5, "C0 · Controle do combate")
    cabs(ws, 6, {"A": "Combate", "B": "Ciclo atual", "C": ("Carregar encontro", "D"), "E": ("Surpresa", "F"),
                 "G": "PH atual", "H": "PH máx.", "I": "PH no início", "J": "Na Fila agora", "K": ("Aviso", "L")})
    rot(ws, "A7", "Estado", negrito=True)
    ent(ws, "B7", "combate.ciclo", tipo="inteiro", minimo=1, maximo=99, rotulo="Ciclo atual", centro=True, amostra=2)
    ent(ws, "C7", "combate.carregar", tipo="lista", fonte="lista.carregar", ate="D", rotulo="Carregar encontro")
    ent(ws, "E7", "combate.surpresa", tipo="lista", fonte="lista.surpresa", ate="F", rotulo="Surpresa")
    ent(ws, "G7", "combate.ph", tipo="inteiro", minimo=0, maximo=9, rotulo="PH atual", centro=True)
    cal(ws, "H7", f'={T("campanha.ph_max")}', nome="combate.ph_max", centro=True, regra=True)
    cal(ws, "I7", f'={T("campanha.ph_ini")}', nome="combate.ph_ini", centro=True, regra=True)
    cal(ws, "J7", f'=SUM({srng("ativo")})', nome="combate.n", centro=True, regra=True)
    N.aux(ws, "N8", f'=IF(ISNUMBER({T("combate.ciclo")}),MAX(1,INT({T("combate.ciclo")})),1)', nome="combate.ciclo_ef")
    N.aux(ws, "O8", f'=IF(ISNUMBER({T("combate.ph")}),{T("combate.ph")},{T("combate.ph_ini")})', nome="combate.ph_ef")
    N.aux(ws, "P8", f'=IFERROR(MATCH({T("combate.carregar")},{N.dlista("carregar")},0)-1,0)', nome="combate.src")
    PH = T("combate.ph")
    av(ws, "K7", "combate.aviso.c0",
       f'=IF(AND(ISNUMBER({PH}),{PH}<0),"Não existe PH negativo (27.10)",IF(AND(ISNUMBER({PH}),{PH}>{T("combate.ph_max")}),'
       f'"PH acima do máximo do grupo (16.2)",IF(AND({T("combate.surpresa")}<>"",{T("combate.surpresa")}<>"Ninguém",'
       f'{T("combate.ciclo_ef")}=1),"Surpresa: cada um do lado surpreendido faz Percepção Mental DT 13; quem falha '
       f'recebe Surpreso em C7 (19.3)","")))', ate="L")
    passos = ["Avançar o Ciclo (4 passos, como a Trilha de Ação de 29.10): (1) some 1 em Ciclo atual;",
              "(2) copie a coluna 'Pendente para o Ciclo seguinte' (C8) e cole como valores em 'Atraso pendente do "
              "Ciclo anterior';",
              "(3) apague 'Atraso deste Ciclo', 'Avançar', 'Já agiu?', 'Avanço Total' e 'Ultimate usada';",
              "(4) desconte 1 turno das condições de quem agiu (C7; com 0 ela expira e sai do painel C9b). PV: digite "
              "o 'PV depois' no 'PV atual'."]
    for k, t in enumerate(passos):
        rot(ws, f"A{8 + k}", t, ate="L", italico=k > 0)
    rot(ws, "A12", "PH: começa cada combate com o máximo menos 2 (vazio = início); gera +1 por Ataque Básico que "
                   "acerta (níveis 1–8) ou +2 (9–20), 16.2.", ate="L", italico=True)
    N.subtabela(ws, "C0", [6], "A:L", 1)


def _pjs(ws):
    titulo(ws, R_C1 - 2, "C1 · PJs — PV e Energia (os números vêm da aba Grupo)")
    cabs(ws, R_C1 - 1, {"A": "PJ", "B": "Participa?", "C": "Ajuste de VEL", "D": "VEL efetiva", "E": "PV máx.",
                        "F": "PV atual", "G": "Dano agora (− = cura)", "H": "PV depois", "I": "Energia",
                        "J": "Ultimate pronta?", "K": ("Aviso", "L")})
    titulo(ws, R_C2 - 2, "C2 · PJs — Morrendo e recursos (23.4, 23.5)")
    cabs(ws, R_C2 - 1, {"A": "PJ", "B": "Ultimate usada neste Ciclo", "C": "Esforço disponível", "D": "Sucessos",
                        "E": "Falhas", "F": ("Situação", "H"), "I": "PV temporário", "J": "Pode ser Executado?",
                        "K": ("Aviso", "L")})
    EF = T("campanha.ef")
    for i in range(1, NPJ + 1):
        r, r2, p, g = R_C1 + i - 1, R_C2 + i - 1, f"combate.pj{i}", f"grupo.pj{i}"
        lab = f'=IF(LEN({s("lab", i)})>0,{s("lab", i)},"PJ {i}")'
        cal(ws, f"A{r}", lab, nome=f"{p}.rot1")
        ent(ws, f"B{r}", f"{p}.participa", tipo="lista", fonte="lista.sim_nao", rotulo="Participa?", centro=True)
        ent(ws, f"C{r}", f"{p}.ajvel", tipo="inteiro", minimo=-10, maximo=10, rotulo="Ajuste de VEL", centro=True,
            amostra=2)
        cal(ws, f"D{r}", f'=IF({s("ex", i)}=1,{s("vel", i)},"")', nome=f"{p}.vel", centro=True, regra=True)
        cal(ws, f"E{r}", f'=IF({s("ex", i)}=1,{s("pvmax", i)},"")', nome=f"{p}.pvmax", centro=True, regra=True)
        ent(ws, f"F{r}", f"{p}.pv", tipo="inteiro", minimo=0, maximo=999, rotulo="PV atual", centro=True, amostra=10)
        ent(ws, f"G{r}", f"{p}.dano", tipo="inteiro", minimo=-999, maximo=999, rotulo="Dano agora", centro=True,
            amostra=5)
        TEMP, DANO = T(f"{p}.temp"), T(f"{p}.dano")
        tmp = f'IF(ISNUMBER({TEMP}),MAX(0,{TEMP}),0)'
        dano = f'IF(ISNUMBER({DANO}),INT({DANO}),0)'
        cal(ws, f"H{r}", f'=IF({s("ex", i)}=0,"",IF({dano}>=0,MAX(0,{s("pvat", i)}-MAX(0,{dano}-{tmp})),'
                         f'MIN({s("pvmax", i)},{s("pvat", i)}-{dano})))', nome=f"{p}.pvdepois", centro=True, regra=True)
        ent(ws, f"I{r}", f"{p}.energia", tipo="inteiro", minimo=0, maximo=100, rotulo="Energia", centro=True)
        EN = T(f"{p}.energia")
        cal(ws, f"J{r}", f'=IF({s("ex", i)}=0,"",IF(AND(ISNUMBER({EN}),{EN}>=100),"Sim","Não"))', nome=f"{p}.ult",
            centro=True, regra=True)
        PVE = T(f"{p}.pv")
        av(ws, f"K{r}", f"{p}.aviso1",
           f'=IF({s("ex", i)}=0,"",IF(AND(ISNUMBER({PVE}),{PVE}>{s("pvmax", i)}),"PV acima do máximo: usando o máximo",'
           f'IF(AND({dano}<0,{s("pvat", i)}-{dano}>{s("pvmax", i)}),"Cura acima do máximo: "&({s("pvat", i)}-{dano}-'
           f'{s("pvmax", i)})&" perdida (23.2)",IF(AND(ISNUMBER({EN}),OR({EN}>100,{EN}<0)),'
           f'"Energia de 0 a 100: o excedente é perdido (17)",IF(NOT(ISNUMBER({T(g + ".vel")})),'
           f'"VEL vazia na aba Grupo: usando 10","")))))', ate="L")
        cal(ws, f"A{r2}", lab, nome=f"{p}.rot2")
        ent(ws, f"B{r2}", f"{p}.ultusada", tipo="lista", fonte="lista.sim_nao", rotulo="Ultimate usada", centro=True)
        ent(ws, f"C{r2}", f"{p}.esforco", tipo="lista", fonte="lista.sim_nao", rotulo="Esforço", centro=True)
        ent(ws, f"D{r2}", f"{p}.suc", tipo="inteiro", minimo=0, maximo=3, rotulo="Sucessos", centro=True)
        ent(ws, f"E{r2}", f"{p}.fal", tipo="inteiro", minimo=0, maximo=3, rotulo="Falhas", centro=True)
        SU, FA = T(f"{p}.suc"), T(f"{p}.fal")
        pres = f'IF(ISNUMBER({T(g + ".pres")}),{T(g + ".pres")},0)'
        vant = f'{T(g + ".morrendo_vant")}="Sim"'
        cal(ws, f"F{r2}", f'=IF({s("ex", i)}=0,"",IF({s("pvat", i)}>0,"De pé",IF(AND(ISNUMBER({FA}),{FA}>=3),'
                          f'"Morre (3 falhas, 23.4)",IF(AND(ISNUMBER({SU}),{SU}>=3),"Estabiliza com 1 PV: digite 1 '
                          f'em PV atual","Morrendo: d20"&IF({pres}>=0,"+","")&{pres}&", sem Eficiência"&IF({vant},'
                          f'", com Vantagem","")&" contra DT 10. Dano recebido = +1 falha (2 se crítico ou Habilidade '
                          f'de Nível 5+)"))))', nome=f"{p}.situacao", ate="H", regra=True)
        N.pior(ws, f"F{r2}", "Morrendo: d20+5, sem Eficiência, com Vantagem contra DT 10. Dano recebido = +1 falha (2 "
                             "se crítico ou Habilidade de Nível 5+)")
        ent(ws, f"I{r2}", f"{p}.temp", tipo="inteiro", minimo=0, maximo=24, rotulo="PV temporário", centro=True)
        cal(ws, f"J{r2}", f'=IF({s("ex", i)}=0,"",IF(LEN({T(g + ".executavel")})>0,{T(g + ".executavel")},"Sim"))',
            nome=f"{p}.executavel", centro=True, regra=True)
        primeiro = f'IFERROR(INDEX({erng("rot")},MATCH(1,{erng("pode")},0)),"")'
        av(ws, f"K{r2}", f"{p}.aviso2",
           f'=IF({s("ex", i)}=0,"",IF(AND({s("pvat", i)}=0,{T(p + ".executavel")}="Sim",LEN({primeiro})>0,'
           f'NOT(AND(ISNUMBER({FA}),{FA}>=3))),"PV 0 e Morrendo: "&{primeiro}&" pode Executar (23.5); Intervir '
           f'cancela",IF(AND(ISNUMBER({TEMP}),{TEMP}>3*{EF}),"PV temporário acima do teto 3 × Eficiência (23.3)",'
           f'IF(AND({T(p + ".esforco")}="Sim",{T(g + ".esforco")}<>"Sim"),"Esforço é traço do Humano (05)",""))))',
           ate="L")
    N.subtabela(ws, "C1", [R_C1 - 1], "A:L", NPJ)
    N.subtabela(ws, "C2", [R_C2 - 1], "A:L", NPJ)
