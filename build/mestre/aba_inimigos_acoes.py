# -*- coding: utf-8 -*-
"""
Aba Inimigos — ações dos inimigos criados (régua de 28.4) e ficha detalhada no formato do cartão de 28.1
(design §6.7.3). No modo "Ajustar do bestiário" as ações são as da base, reescritas pelo texto-modelo de
Dados.bestiario_acoes: pedaços literais p0…p4 intercalados com marcadores m1…m4 (tipo) e n1…n4 (parâmetro),
montados com & (sem SUBSTITUTE/MID, fora da lista branca). {PV:n} = INT(n × PV novo ÷ PV original) (H3).
"""

import mestre_dados as D
from mestre import nucleo as N
from mestre import aba_inimigos as I
from mestre.nucleo import T, q, ent, cal, av, rot, cabs, titulo, dcol

AC1 = [116, 129, 142]       # ações — entradas (3 blocos de 12)
AC2 = [157, 170, 183]       # ações — texto pronto
FICHA = 196
NLIN = 12                   # linhas de ação na ficha detalhada


def montar(ws):
    _acoes(ws)
    _ficha(ws)


def _acoes(ws):
    titulo(ws, AC1[0] - 2, "Ações dos inimigos criados — entradas (régua de 28.4; modo Ajustar usa as da base)")
    fim = AC1[-1] + 11
    for b, r0 in enumerate(AC1):
        cabs(ws, r0 - 1, {"A": ("Inimigo", "B"), "C": ("Tipo de ação", "D"), "E": ("Nome da ação", "F"),
                          "G": "Alcance", "H": "Elemento", "I": "Recarga (Ciclos)", "J": "Duração (turnos)",
                          "K": ("Aviso", "L")})
        for k in range(12):
            r, n = r0 + k, b * 12 + k + 1
            p = f"inimigos.acao{n}"
            ent(ws, f"A{r}", f"{p}.inimigo", tipo="lista", fonte=T("inimigos.col.nome"), ate="B", rotulo="Inimigo",
                opcoes=[])
            ent(ws, f"C{r}", f"{p}.tipo", tipo="lista", fonte="lista.tipos_acao", ate="D", rotulo="Tipo de ação")
            ent(ws, f"E{r}", f"{p}.nome", ate="F", maximo=40, rotulo="Nome da ação")
            ent(ws, f"G{r}", f"{p}.alcance", tipo="lista", fonte="lista.alcances", rotulo="Alcance", centro=True)
            ent(ws, f"H{r}", f"{p}.elemento", tipo="lista", fonte="lista.elementos", rotulo="Elemento", centro=True)
            ent(ws, f"I{r}", f"{p}.recarga", tipo="inteiro", minimo=2, maximo=3, rotulo="Recarga", centro=True)
            ent(ws, f"J{r}", f"{p}.duracao", tipo="inteiro", minimo=1, maximo=5, rotulo="Duração", centro=True)
            INIM, TP = T(f"{p}.inimigo"), T(f"{p}.tipo")
            p0 = AC1[0]
            N.aux(ws, f"N{r}", f'=IF(AND(LEN({INIM})>0,LEN({TP})>0),1,0)', nome=f"{p}.tem")
            N.aux(ws, f"O{r}", f'=IF(AND($N${r}=1,{TP}<>"Ataque normal"),1,0)', nome=f"{p}.esp")
            N.aux(ws, f"P{r}", f'=IF($N${r}=1,{INIM}&"|"&COUNTIFS($A${p0}:A{r},{INIM},$N${p0}:N{r},1),"")',
                  nome=f"{p}.chave")
            N.aux(ws, f"Q{r}", f'=IF($O${r}=1,{INIM}&"|"&COUNTIFS($A${p0}:A{r},{INIM},$O${p0}:O{r},1),"")',
                  nome=f"{p}.chave_esp")
            N.aux(ws, f"R{r}", f'=IFERROR(MATCH({INIM},{T("inimigos.col.nome")},0),"")', nome=f"{p}.linha")
            N.aux(ws, f"S{r}", f'={T(f"{p}.texto")}', nome=f"{p}.texto_aux")
            esp_total = f'COUNTIFS($A${p0}:$A${fim},{INIM},$O${p0}:$O${fim},1)'
            av(ws, f"K{r}", f"{p}.aviso1",
               f'=IF(LEN({INIM})=0,"",IF(NOT(ISNUMBER($R${r})),"Inimigo fora da tabela I1",'
               f'IF(AND($O${r}=1,{TP}<>"Reação",NOT(ISNUMBER({T(f"{p}.recarga")}))),'
               f'"Ação especial precisa de recarga de 2 ou 3 Ciclos (28.4)",'
               f'IF({esp_total}>3,"Mais de 3 ações especiais neste inimigo (28.1: de 1 a 3)",'
               f'IF(AND({TP}="Especial de dano 1 alvo (até 1,5×)",INDEX({T("inimigos.col.tipo")},$R${r})="Comum"),'
               f'"Pico de dano: ocupa a ação do turno (28.4)","")))))', ate="L")
        N.subtabela(ws, f"AÇ1.{b + 1}", [r0 - 1], "A:L", 12)
    N.reg("inimigos.ac.chave", ws, f"P{AC1[0]}:P{fim}")
    N.reg("inimigos.ac.chave_esp", ws, f"Q{AC1[0]}:Q{fim}")
    N.reg("inimigos.ac.nome", ws, f"E{AC1[0]}:E{fim}")
    N.reg("inimigos.ac.recarga", ws, f"I{AC1[0]}:I{fim}")
    N.reg("inimigos.ac.texto", ws, f"S{AC1[0]}:S{fim}")
    titulo(ws, AC2[0] - 2, "Ações — texto pronto (automático, com o dano e a DT da ficha do inimigo)")
    for b, r0 in enumerate(AC2):
        cabs(ws, r0 - 1, {"A": "Ação", "B": ("Condição (capítulo 21)", "C"), "D": ("Teste de Resistência do alvo", "E"),
                          "F": ("Texto pronto", "J"), "K": ("Aviso", "L")})
        for k in range(12):
            r, n = r0 + k, b * 12 + k + 1
            p = f"inimigos.acao{n}"
            cal(ws, f"A{r}", f'=IF(LEN({T(f"{p}.inimigo")})>0,"{n} · "&{T(f"{p}.inimigo")},"{n} · (vazia)")',
                nome=f"{p}.rotulo")
            ent(ws, f"B{r}", f"{p}.condicao", tipo="lista", fonte="lista.condicoes_acao", ate="C", rotulo="Condição")
            ent(ws, f"D{r}", f"{p}.tr", tipo="lista", fonte="lista.tr", ate="E", rotulo="Teste de Resistência")
            cal(ws, f"F{r}", "=" + texto_pronto(p, AC1[b] + k), nome=f"{p}.texto", ate="J")
            N.pior(ws, f"F{r}", PIOR_TEXTO)
            CO, TR_, TP = T(f"{p}.condicao"), T(f"{p}.tr"), T(f"{p}.tipo")
            av(ws, f"K{r}", f"{p}.aviso2",
               f'=IF(LEN({T(f"{p}.inimigo")})=0,"",IF(AND({TP}="Especial de controle",LEN({CO})=0),'
               f'"Ação de controle aplica uma condição do capítulo 21 (28.4)",'
               f'IF(AND({TP}="Especial de controle",LEN({TR_})=0),"Diga o Teste de Resistência do alvo",'
               f'IF({CO}="Congelado","Inimigo não aplica Congelamento em personagem (28.2 regra 9)",'
               f'IF(AND(LEN({CO})>0,COUNTIF({N.dlista("condicoes_acao")},{CO})=0),'
               f'"Condição fora do capítulo 21: nada de condição nova (28.4)","")))))', ate="L")
        N.subtabela(ws, f"AÇ2.{b + 1}", [r0 - 1], "A:L", 12)


PIOR_TEXTO = ("Nome da ação com quarenta caracteres aqui (recarga 3 Ciclos): até 3 alvos a até uma Distância um do "
              "outro fazem Teste de Resistência Mental contra DT 21. Quem falha recebe 7d12 + 3 · média 48 de dano "
              "Imaginário e Cisalhamento de Vento por 5 turnos; quem passa recebe metade do dano.")


def texto_pronto(p, ra):
    """Texto da ação pela régua de 28.4, com o dano (normal, 1,5× ou cheio por alvo) e a DT da ficha."""
    INIM, TP, NOME = T(f"{p}.inimigo"), T(f"{p}.tipo"), T(f"{p}.nome")
    AL, EL, REC, DUR = T(f"{p}.alcance"), T(f"{p}.elemento"), T(f"{p}.recarga"), T(f"{p}.duracao")
    CO, TR_ = T(f"{p}.condicao"), T(f"{p}.tr")
    lin = f"$R${ra}"
    cat = lambda c: f'INDEX({T("inimigos.col." + c)},{lin})'  # noqa: E731
    dano = f'{cat("dano_e")}&" · média "&{cat("dano_m")}'
    esp = f'{cat("esp_e")}&" · média "&{cat("esp_m")}'
    dt = cat("dt")
    el = f'IF(LEN({EL})>0,{EL},"Físico")'
    rec = f'IF(ISNUMBER({REC})," (recarga "&{REC}&" Ciclos)","")'
    dur = f'IF(ISNUMBER({DUR}),{DUR},1)&IF(AND(ISNUMBER({DUR}),{DUR}>1)," turnos"," turno")'
    cond = f'IF(LEN({CO})>0," e "&{CO}&" por "&{dur},"")'
    nome = f'IF(LEN({NOME})>0,{NOME},"Ação")'
    alc = f'IF(LEN({AL})>0,{AL},"Pessoal")'
    teste = f'"Teste de "&{TR_}&" contra DT "&{dt}'
    qualquer = f'IF(LEN({TR_})>0,{teste},"Teste de Resistência contra DT "&{dt})'
    ataque = f'{nome}&" ("&{alc}&", "&{el}&"): "&{dano}&IF(LEN({CO})>0,", e o alvo recebe "&{CO}&" por "&{dur},"")'
    um = (f'{nome}&{rec}&": um alvo a até Distância "&{alc}&IF(LEN({TR_})>0," faz "&{teste}&"; se falhar, recebe ",'
          f'" recebe ")&{esp}&" de dano "&{el}&{cond}&"."')
    area = (f'{nome}&{rec}&": até 3 alvos a até uma Distância um do outro "&IF(LEN({TR_})>0,"fazem "&{teste}&'
            f'". Quem falha recebe "&{dano}&" de dano "&{el}&{cond}&"; quem passa recebe metade do dano.",'
            f'"recebem, cada um, "&{dano}&" de dano "&{el}&{cond}&".")')
    controle = (f'{nome}&{rec}&": o alvo faz "&{qualquer}&"; se falhar, recebe "&IF(LEN({CO})>0,{CO},'
                f'"(escolha a condição)")&" por "&{dur}&"."')
    reacao = (f'{nome}&" (Reação"&IF(ISNUMBER({REC}),", recarga "&{REC}&" Ciclos","")&")"&IF(LEN({CO})>0,'
              f'": o alvo faz "&{qualquer}&"; se falhar, recebe "&{CO}&" por "&{dur}&".",".")')
    return (f'IF(OR(LEN({INIM})=0,NOT(ISNUMBER({lin}))),"",IF({TP}="Ataque normal",{ataque},IF({TP}='
            f'"Especial de dano 1 alvo (até 1,5×)",{um},IF({TP}="Especial de dano 2–3 alvos (dano cheio por alvo)",{area},IF({TP}="Especial de controle",'
            f'{controle},IF({TP}="Reação",{reacao},""))))))')


def _ficha(ws):
    r0 = FICHA
    titulo(ws, r0, "Ficha detalhada (formato do cartão de 28.1)")
    rot(ws, f"A{r0 + 1}", "Ver ficha de", negrito=True)
    ent(ws, f"B{r0 + 1}", "inimigos.ver", tipo="lista", fonte=T("inimigos.col.nome"), ate="D", rotulo="Ver ficha de",
        opcoes=[])
    rot(ws, f"E{r0 + 1}", "Números sem marcador são os do livro, na faixa original. Limiares de PV reescritos: "
                          f"{N.ROTULO_SUGESTAO} (H3).", ate="L", italico=True)
    N.reg("inimigos.h3.rotulo", ws, f"E{r0 + 1}")
    N.MAPA.sugestoes.append({"h": "H3", "rotulo": N.MapaMestre.ref("Inimigos", f"E{r0 + 1}"),
                             "nome": "inimigos.h3.rotulo", "celulas": []})
    sel = f"$N${r0 + 1}"
    # LEN(ver)=0: a camada de leitura protegida devolve "" para a entrada vazia, e MATCH("") acharia uma linha sem nome
    N.aux(ws, sel, f'=IF(LEN({T("inimigos.ver")})=0,"",IFERROR(MATCH({T("inimigos.ver")},{T("inimigos.col.nome")},0),'
                   f'""))', nome="inimigos.ver.linha")
    c = lambda campo: f'INDEX({T("inimigos.cat." + campo)},{sel})'  # noqa: E731
    a = lambda nome: f'INDEX({T("inimigos.col." + nome)},{sel})'  # noqa: E731
    ok = f"ISNUMBER({sel})"
    linhas = [
        f'=IF({ok},{c("nome")}&"  ·  "&{c("tipo")}&" · "&IF(LEN({c("origem")})>0,{c("origem")}&" · ","")&'
        f'"faixa "&{c("faixa")}&IF({c("fases")}>1," · "&{c("fases")}&" fases",""),"")',
        f'=IF({ok},"PV "&{c("pv")}&"   Defesa "&{c("defesa")}&"   RD "&{c("rd")}&"   Tenacidade "&{c("ten")}&'
        f'"   VEL "&{c("vel")},"")',
        f'=IF({ok},"Ataque +"&{c("ataque")}&"    DT dos efeitos "&{c("dt")}&"    Teste de Resistência +"&{c("tr")}&'
        f'"    Dano por acerto "&{c("dano_e")}&" · média "&{c("dano_m")},"")',
        f'=IF({ok},"Fraquezas: "&{c("fraq_txt")}&"    Resistências: "&IF(LEN({c("res")})>0,{c("res")},"—"),"")',
    ]
    for k, f in enumerate(linhas):
        cal(ws, f"A{r0 + 2 + k}", f, nome=f"inimigos.ficha.l{k + 1}", ate="L", regra=k in (1, 2))
    ra = r0 + 6
    N.cab(ws, f"A{ra}", "Ataques e ações")
    N.cab(ws, f"B{ra}", "Texto (modo Ajustar: ações da base reescritas para a faixa nova)", ate="L")
    for k in range(1, NLIN + 1):
        r = ra + k
        base = f'INDEX({T("inimigos.col.base")},{sel})'
        idx = f"$O${r}"
        N.aux(ws, idx, f'=IF({ok},IFERROR(IF({a("aj")}=1,MATCH({base}&"|{k}",{dcol("bestiario_acoes", "Chave")},'
                       f'0),""),""),"")', nome=f"inimigos.ficha.idx{k}")
        pec = lambda col: f'INDEX({dcol("bestiario_acoes", col)},{idx})'  # noqa: E731
        txt = pec("p0")
        for j in range(1, D.MAX_MARCADORES + 1):
            m, n = pec(f"m{j}"), pec(f"n{j}")
            val = (f'IF({m}="","",IF({m}="DANO.e",{c("dano_e")},IF({m}="DANO.m",{c("dano_m")},IF({m}="DANO15.e",'
                   f'{a("esp_e")},IF({m}="DANO15.m",{a("esp_m")},IF({m}="COMUM.e",{a("com_e")},IF({m}="COMUM.m",'
                   f'{a("com_m")},IF({m}="DT",{c("dt")},IF({m}="PV",INT({n}*{c("pv")}/{a("pv_orig")}),"")))))))))')
            txt += f"&{val}&{pec(f'p{j}')}"
        criado = f'IFERROR(INDEX({T("inimigos.ac.texto")},MATCH({c("nome")}&"|{k}",{T("inimigos.ac.chave")},0)),"")'
        fase_txt = f'IF({pec("Fase")}=0,{pec("Tipo")},"Fase "&{pec("Fase")}&" · "&{pec("Tipo")})'
        cal(ws, f"A{r}", f'=IF(NOT({ok}),"",IF({a("aj")}=1,IF(ISNUMBER({idx}),{fase_txt},""),IF(LEN({criado})>0,'
                         f'"Ação {k}","")))', nome=f"inimigos.ficha.tipo{k}")
        cal(ws, f"B{r}", f'=IF(NOT({ok}),"",IF({a("aj")}=1,IF(ISNUMBER({idx}),{txt},""),{criado}))',
            nome=f"inimigos.ficha.acao{k}", ate="L", regra=True)
        N.pior(ws, f"B{r}", max((x["texto"] for x in D.acoes()), key=len))
    N.subtabela(ws, "inimigos.ficha.acoes", [ra], "A:L", NLIN)
    r = ra + NLIN + 2
    resto = max((f["na_fila_resto"] for f in D.bestiario()), key=len)
    cal(ws, f"A{r}", f'=IF({ok},"Na Fila: VEL "&{c("vel")}&", "&{c("firmeza")}&"."&IF(LEN(INDEX({T("inimigos.col.comp")},'
                     f'{sel}))>0," "&INDEX({T("inimigos.col.comp")},{sel}),IF({a("aj")}=1," "&'
                     f'{I.bes("Na Fila (resto)", a("brow"))},""))&IF({c("execucao")}="Pode",'
                     f'" Pode Executar (ser racional, 23.5).",IF({c("execucao")}="Não"," Não Executa (23.5).","")),"")',
        nome="inimigos.ficha.nafila", ate="L")
    N.pior(ws, f"A{r}", f"Na Fila: VEL 19, com Firmeza. {resto} Pode Executar (ser racional, 23.5).")
    for f_ in (1, 2, 3):
        rr = r + f_
        if f_ == 1:
            fq, ten, topo = c("fraq_txt"), c("ten"), c("pv")
            piso = f'IF({c("fases")}>=2,{c("lim2")}+1,0)'
        else:
            fq = (f'{c(f"p{f_}f1")}&IF(LEN({c(f"p{f_}f2")})>0,", "&{c(f"p{f_}f2")},"")&IF(LEN({c(f"p{f_}f3")})>0,'
                  f'", "&{c(f"p{f_}f3")},"")&IF(LEN({c(f"p{f_}f4")})>0,", "&{c(f"p{f_}f4")},"")')
            ten, topo = c(f"ten{f_}"), c(f"lim{f_}")
            piso = f'IF({c("fases")}>2,{c("lim3")}+1,0)' if f_ == 2 else "0"
        cal(ws, f"A{rr}", f'=IF(NOT({ok}),"",IFERROR(IF(AND({c("fases")}>={f_},{c("fases")}>1),"Fase {f_} ("&{topo}&" a "&{piso}&'
                          f'" PV): Fraquezas "&{fq}&"; Tenacidade "&{ten}&" (volta ao máximo na virada)",""),""))',
            nome=f"inimigos.ficha.fase{f_}", ate="L", regra=True)
