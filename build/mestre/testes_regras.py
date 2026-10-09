# -*- coding: utf-8 -*-
"""Suítes oraculo (oráculo independente × planilha, cobertura medida — plano P10), ouro (números impressos no
livro calculados NA planilha) e determinismo (propriedades (a)–(g) do sorteio, design §5)."""

import random
import time

import testar_ficha as TF
import oraculo_mestre as O
import oraculo_mestre_abas as OA
from oraculo_mestre_livro import FAIXAS, TIPOS, ELEM, bestiario_md, ancora
from mestre import testes_comum as TC

Resultado = TF.Resultado
COMPARADOS = set()


def _norm(v):
    return "" if v is None else v


def planilha(E, nomes):
    refs = [TC.C(n) for n in nomes if n in TC.mapa()["celulas"]]
    sol = TC.modelo().calcular(TC.entradas(E), refs)
    inv = {TC.C(n): n for n in nomes if n in TC.mapa()["celulas"]}
    return {inv[k]: _norm(v) for k, v in sol.items()}


def progresso(msg):
    print(f"  … {time.strftime('%H:%M:%S')} {msg}", flush=True)


def comparar(r, E, rotulo, prefixos=None, limite=8):
    """Oráculo × planilha nas células de regra (e nas demais que o oráculo calcula) com os prefixos dados."""
    esp = O.calcular(E)
    regra = TC.mapa()["numeros_de_regra"]
    nomes = [n for n in esp if n in TC.mapa()["celulas"] and (prefixos is None or n.startswith(tuple(prefixos)))]
    obt = planilha(E, nomes)
    ruins = 0
    for n in nomes:
        ok = TF._igual(obt.get(n), esp[n]) or (esp[n] == "" and obt.get(n) in ("", None))
        if n in regra:
            COMPARADOS.add(n)
        if not r.ok(ok, f"[{rotulo}] {n}: planilha={obt.get(n)!r} oráculo={esp[n]!r}"):
            ruins += 1
            if ruins >= limite:
                break
    return obt, esp


def _grupo(rng, n=4, repetir=False):
    gr = []
    els = rng.sample(ELEM, n) if not repetir else [rng.choice(ELEM) for _ in range(n)]
    for i in range(n):
        gr.append({"nome": f"PJ{i + 1}", "raca": rng.choice(OA.RACAS), "elemento": els[i], "pv": rng.randint(20, 200),
                   "vel": rng.randint(7, 25), "ag": rng.randint(-1, 5), "disc": rng.randint(-1, 5),
                   "pres": rng.randint(-1, 5), "caminho": "A Caça"})
    return TC.entradas_grupo(gr)


GRUPOS = [{"Fogo", "Vento", "Gelo", "Quântico"}, {"Físico", "Raio", "Imaginário"}, {"Fogo", "Fogo", "Gelo", "Raio"}]


def _grupo_fixo(k):
    els = [["Fogo", "Vento", "Gelo", "Quântico"], ["Físico", "Raio", "Imaginário"], ["Fogo", "Fogo", "Gelo", "Raio"]][k]
    return TC.entradas_grupo([{"nome": f"PJ{i + 1}", "elemento": e, "raca": "Humano", "pv": 60, "vel": 12 + i,
                               "ag": 1, "disc": 1, "pres": 0} for i, e in enumerate(els)])


# ---------------------------------------------------------------------------

TAREFAS = []


def _t(E, rotulo, prefixos=None, limite=8, modo=None, var=None, peso=None):
    """Registra um caso oráculo × planilha (calculado depois, em paralelo — mestre\\paralelo.py; modo "bloco" =
    cálculo incremental sobre a base do bloco, para séries que só mudam as entradas `var`; peso = custo relativo
    medido, para repartir os casos caros entre os processos)."""
    TAREFAS.append({"tipo": "comparar", "rot": rotulo, "E": dict(E), "pref": prefixos, "lim": limite, "modo": modo,
                    "var": var, "peso": peso})


VAR_CALC = ["combate.calc.alvo", "combate.calc.fonte", "combate.calc.n", "combate.calc.f", "combate.calc.fixo",
            "combate.calc.elem", "combate.calc.crit", "combate.calc.extra", "combate.calc.rolado"]


def suite_oraculo(args):
    from mestre import paralelo
    r = Resultado("oraculo")
    COMPARADOS.clear()
    TAREFAS.clear()
    rng = random.Random(2026)
    from mestre import exemplo
    _t({}, "em branco")
    _t(exemplo.entradas_nomes(), "Exemplo")
    # Criador: 3 modos × 20 níveis × 3 tipos × 4 Elementos de ataque (12 linhas por cenário)
    combos = [(m, L, t) for m in ("Faixa do livro", "Por nível — Sugestão") for L in range(1, 21) for t in TIPOS]
    n_cri = 0
    for k in range(0, len(combos), 12):
        E = _grupo_fixo(k // 12 % 3)
        E["inimigos.rolagem"] = 1 + k
        for i, (m, L, t) in enumerate(combos[k:k + 12], start=1):
            E.update({f"inimigos.{i}.nome": f"I{k + i}", f"inimigos.{i}.modo": m, f"inimigos.{i}.tipo": t,
                      f"inimigos.{i}.elemento": ELEM[(k + i) % 4], f"inimigos.{i}.racional": rng.choice(["Sim", "Não", None])})
            if m == "Faixa do livro":
                E[f"inimigos.{i}.faixa"] = FAIXAS[(L - 1) // 4]
            else:
                E[f"inimigos.{i}.nivel"] = L
            if rng.random() < 0.3:
                E[f"inimigos.{i}.f1"] = rng.choice(ELEM)
            if rng.random() < 0.2:
                E[f"inimigos.{i}.res"] = rng.choice(ELEM)
        E["inimigos.ver"] = f"I{k + 1}"
        _t(E, f"Criador {k // 12 + 1}", ["inimigos."])
        n_cri += 1
    # Ajustar do bestiário: 32 × 5 faixas
    fichas = bestiario_md()
    aj = [(f["nome"], fx) for f in fichas for fx in FAIXAS]
    for k in range(0, len(aj), 12):
        E = _grupo_fixo(k // 12 % 3)
        for i, (b, fx) in enumerate(aj[k:k + 12], start=1):
            E.update({f"inimigos.{i}.nome": f"A{k + i}", f"inimigos.{i}.modo": "Ajustar do bestiário",
                      f"inimigos.{i}.base": b, f"inimigos.{i}.faixa": fx})
        E["inimigos.ver"] = f"A{k + rng.randint(1, len(aj[k:k + 12]))}"
        _t(E, f"Ajustar {k // 12 + 1}", ["inimigos."])
        n_cri += 1
    # ficha detalhada de cada base no Ajustar (ações reescritas, H3) e Boss criado com fases (I5, H4)
    for b in [f["nome"] for f in fichas if f["fases"] > 1] + ["Capataz Oco", "Pretor Vazio-Nove", "Escória de Stellaron"]:
        E = {"inimigos.1.nome": "X", "inimigos.1.modo": "Ajustar do bestiário", "inimigos.1.base": b,
             "inimigos.1.faixa": rng.choice(FAIXAS), "inimigos.ver": "X"}
        _t(E, f"ficha Ajustar {b}", ["inimigos."])
    for nf in (2, 3):
        E = {"inimigos.1.nome": "Chefe", "inimigos.1.tipo": "Boss", "inimigos.1.fases": nf, "inimigos.1.faixa": "13-16",
             "inimigos.ver": "Chefe", "inimigos.fase1.inimigo": "Chefe", "inimigos.fase1.fase": 2,
             "inimigos.fase1.f1": "Gelo", "inimigos.fase1.f2": "Raio", "inimigos.fase1.f3": "Vento",
             "inimigos.fase1.f4": "Físico", "inimigos.fase1.ten": 20 if nf == 2 else 9}
        for n in range(1, 13):
            E.update({f"inimigos.acao{n}.inimigo": "Chefe", f"inimigos.acao{n}.tipo": rng.choice(
                ["Ataque normal", "Especial de dano 1 alvo (até 1,5×)", "Especial de dano 2–3 alvos (dano cheio por alvo)",
                 "Especial de controle", "Reação"]), f"inimigos.acao{n}.nome": f"Golpe {n}",
                f"inimigos.acao{n}.recarga": rng.choice([2, 3, None]), f"inimigos.acao{n}.duracao": rng.choice([1, 2, None]),
                f"inimigos.acao{n}.condicao": rng.choice(["Lentidão", "Marcado", None]),
                f"inimigos.acao{n}.tr": rng.choice(["Reflexos", None]), f"inimigos.acao{n}.elemento": rng.choice(ELEM)})
        _t(E, f"Boss criado {nf} fases", ["inimigos.", "combate."])
    r.info(f"Criador: {len(combos)} combinações modo × nível × tipo, {len(aj)} Ajustar (32 × 5) em {n_cri} cenários")
    # H1 — desvio do PV por nível contra a âncora da própria faixa (só o PV é interpolado)
    linhas = []
    for t in TIPOS:
        pior = max(((abs(OA.pv_h1(t, L) - ancora(FAIXAS[(L - 1) // 4], t)["pv"]) /
                     ancora(FAIXAS[(L - 1) // 4], t)["pv"], L) for L in range(1, 21)))
        r.ok(pior[0] <= 0.20, f"H1: desvio do PV de {t} {pior[0]:.1%} > 20% (nível {pior[1]})")
        for L in (3, 7, 11, 15, 19):
            r.ok(OA.pv_h1(t, L) == ancora(FAIXAS[(L - 1) // 4], t)["pv"], f"H1: PV de {t} no nível {L} ≠ 28.3")
        linhas.append(f"{t} {pior[0]:.1%} (nível {pior[1]})")
    r.info("H1, desvio máximo do PV por tipo: " + "; ".join(linhas))
    # Bestiário: filtros
    for k in range(12):
        E = {"bestiario.filtro.faixa": rng.choice([None, "Todas"] + FAIXAS),
             "bestiario.filtro.tipo": rng.choice([None, "Todos"] + TIPOS),
             "bestiario.filtro.elemento": rng.choice([None, "Qualquer"] + ELEM),
             "bestiario.filtro.ambiente": rng.choice([None, "Todos", "Ruína", "Nave-cidade", "Instalação antiga",
                                                      "Mundo com Stellaron"]),
             "bestiario.filtro.resistencia": rng.choice([None, "Sim", "Não"]), "bestiario.filtro.fases": rng.choice(
                 [None, "Sim"]), "bestiario.ver": rng.choice(fichas)["nome"]}
        if k == 0:
            E = {"bestiario.ver": "Vazia Coroada"}
        _t(E, f"Bestiário {k + 1}", ["bestiario."])
    # Encontros salvos
    nomes = [f["nome"] for f in fichas]
    for k in range(30):
        E = _grupo(rng, rng.randint(1, 6), repetir=k % 3 == 2)
        E["campanha.nivel"] = rng.randint(1, 20)
        if k % 4 == 0:
            E["encontros.npj_troca"] = rng.randint(1, 6)
        E.update({"inimigos.1.nome": "Criado", "inimigos.1.tipo": rng.choice(TIPOS)})
        for X in "ABC":
            for j in range(1, rng.randint(1, 8) + 1):
                E[f"encontros.{X}.{j}.criatura"] = rng.choice(nomes + ["Criado"])
                if rng.random() < 0.7:
                    E[f"encontros.{X}.{j}.qtd"] = rng.randint(0, 4)
                if rng.random() < 0.2:
                    E[f"encontros.{X}.{j}.f1"] = rng.choice(ELEM)
        _t(E, f"Encontros {k + 1}", ["encontros."])
    # Composições de 28.11 e 27.4 (as quatro na faixa caem em "típico", H6)
    # Encontro aleatório (G = 100) × 3 grupos
    n_ale = 0
    for g in range(3):
        for k in range(int(getattr(args, "n_aleatorio", 0) or 167)):
            E = _grupo_fixo(g)
            E.update({"encontros.ale.rolagem": rng.randint(1, 1000000), "inicio.semente": rng.randint(1, 2147483646),
                      "encontros.ale.ambiente": rng.choice([None, "Qualquer"] + [a for _, a in OA.AMBIENTE[:12]]),
                      "encontros.ale.faixa": rng.choice([None] + FAIXAS),
                      "encontros.ale.composicao": rng.choice([None, "Sortear", "1 Boss + 1 Comum", "1 Elite + 4 Comuns",
                                                              "3 Elites", "7 Comuns"])})
            _t(E, f"aleatório g{g} {k}", ["encontros.ale.", "encontros.orc"], limite=3)
            n_ale += 1
    r.info(f"encontro aleatório: {n_ale} encontros (3 grupos)")
    # Fila: 4 empates fixos + 300 estados aleatórios
    _fila(r, rng)
    # Calculadora (2 000 casos) e condições
    _calc(r, rng)
    # Fase 2: NPCs, Aventuras, Recompensas (G = 200, 300, 400, 410, 420) e as heurísticas H9, H14, H18, H20, H22, H25
    from mestre import testes_hist
    testes_hist.casos_oraculo(r, rng, _t)
    # Fase 3: Mundos, Improviso, Minhas Tabelas (G = 510…650, 701…710), campanha, H10, H15, H16, H25, (d)
    from mestre import testes_fase3
    testes_fase3.casos_oraculo(r, rng, _t)
    COMPARADOS.update(paralelo.executar(r, TAREFAS, progresso=progresso))
    regra = set(TC.mapa()["numeros_de_regra"])
    falta = sorted(regra - COMPARADOS)
    r.ok(not falta, f"cobertura P10: {len(falta)} número(s) de regra sem comparação: {falta[:20]}")
    r.info(f"cobertura P10: {len(regra & COMPARADOS)} de {len(regra)} números de regra comparados")
    return r


def _estado_fila(rng, E):
    E.update(_grupo(rng, rng.randint(1, 6)))
    for X in ("A",):
        for j in range(1, rng.randint(1, 5) + 1):
            E[f"encontros.A.{j}.criatura"] = rng.choice([f["nome"] for f in bestiario_md()])
            E[f"encontros.A.{j}.qtd"] = rng.randint(1, 3)
    E["combate.carregar"] = "A"
    E["combate.ciclo"] = rng.choice([1, 2, 3])
    memos_aleatorios(rng, E)
    for i in range(1, TC.NC + 1):
        if rng.random() < 0.3:
            E[f"combate.f{i}.atraso"] = rng.randint(0, 8)
        if rng.random() < 0.15:
            E[f"combate.f{i}.pend"] = rng.randint(0, 4)
        if rng.random() < 0.2:
            E[f"combate.f{i}.avancar"] = rng.randint(0, 3)
        if rng.random() < 0.3:
            E[f"combate.f{i}.ja"] = "Sim"
        if i <= 6 and rng.random() < 0.3:
            E[f"combate.f{i}.ordem"] = rng.randint(1, 5)
        if rng.random() < 0.05:
            E[f"combate.f{i}.manual"] = rng.randint(1, TC.NC)
    for e in range(1, 11):
        if rng.random() < 0.15:
            E[f"combate.in{e}.pv"] = 0
        if rng.random() < 0.2:
            E[f"combate.in{e}.ajvel"] = rng.randint(-3, 3)
    for i in range(1, 7):
        if rng.random() < 0.1:
            E[f"combate.pj{i}.pv"] = 0
            E[f"combate.pj{i}.fal"] = rng.choice([1, 3])
    # condições na C7 (até 4 por combatente): Congelado tira o Comum da Fila, Surpreso pula a casa; 0 turnos = expirada
    for _ in range(rng.randint(0, 6)):
        n = TC.slot(rng.randint(1, TC.NC), rng.randint(1, 4))
        E.update({f"combate.c{n}.cond": rng.choice(["Congelado", "Surpreso", "Queimadura"]),
                  f"combate.c{n}.turnos": rng.choice([0, 1, 2, None])})
    return E


def memos_aleatorios(rng, E, p=0.45):
    """Memoespíritos ligados a PJs (G7) e invocados ou não (C2b), com números digitados ou vazios (11.4)."""
    for i in range(1, 7):
        if rng.random() >= p:
            continue
        g = f"grupo.pj{i}.memo"
        E[f"{g}.tem"] = rng.choice(["Sim", "Sim", "Sim", "Não", None])
        if rng.random() < 0.6:
            E[f"{g}.nome"] = rng.choice(["Eco", "Lembrança Antiga", "Sombra do Pai"])
        for k, a, b in (("pv", 5, 300), ("def", 8, 30), ("vel", 8, 26), ("rd", 0, 3), ("agi", 0, 5), ("disc", 0, 5),
                        ("vigor", 0, 5)):
            if rng.random() < 0.6:
                E[f"{g}.{k}"] = rng.randint(a, b)
        E[f"combate.memo{i}.invocado"] = rng.choice(["Sim", "Sim", "Não", None])
        if rng.random() < 0.3:
            E[f"combate.memo{i}.pv"] = rng.choice([0, 1, 10, 999])
        if rng.random() < 0.2:
            E[f"combate.memo{i}.ajvel"] = rng.randint(-3, 3)
        if rng.random() < 0.2:
            E[f"combate.memo{i}.dano"] = rng.choice([-30, -5, 4, 40])
        if rng.random() < 0.15:
            E[f"grupo.pj{i}.caminho"] = rng.choice(["A Recordação", "A Caça"])
    return E


def ouro_memo(conf, planilha, r):
    """11.4 (o exemplo do livro: nível 17, 5 pontos em Vigor e 4 em Agilidade, Eficiência +7, Caminho +1) e 11.5/19.7
    (casa própria na Fila pela VEL dele; Não = fora; a 0 PV some), calculados NA planilha."""
    E = {"campanha.nivel": 17, "grupo.pj1.nome": "Dona", "grupo.pj1.caminho": "A Recordação", "grupo.pj1.vel": 14,
         "grupo.pj1.pv": 200, "grupo.pj1.memo.tem": "Sim", "grupo.pj1.memo.vigor": 5, "grupo.pj1.memo.agi": 4}
    for nome, v in (("pv_ef", 151), ("def_ef", 21), ("vel_ef", 15), ("rt", 2),
                    ("dano", "5d6 + pontos no Atributo de ataque (6d6 se a arma do dono for de Energia)")):
        conf(f"11.4 exemplo do nível 17: {nome}", E, f"grupo.pj1.memo.{nome}", v)
    conf("11.4 RT 1 antes do nível 11", dict(E, **{"campanha.nivel": 10}), "grupo.pj1.memo.rt", 1)
    conf("11.4 PV no nível 1 com 4 em Vigor", dict(E, **{"campanha.nivel": 1, "grupo.pj1.memo.vigor": 4}),
         "grupo.pj1.memo.pv_ef", 20)
    E2 = dict(E, **{"combate.memo1.invocado": "Sim"})
    got = planilha(E2, ["combate.fila1.nome", "combate.fila2.nome", "combate.n", "combate.memo1.nafila"])
    r.ok(got == {"combate.fila1.nome": "Memoespírito de Dona", "combate.fila2.nome": "Dona", "combate.n": 2,
                 "combate.memo1.nafila": "Sim"}, f"11.5/19.7 casa própria pela VEL 15 antes da dona (VEL 14): {got}")
    got = planilha(dict(E2, **{"combate.memo1.invocado": "Não"}), ["combate.n", "combate.memo1.nafila"])
    r.ok(got == {"combate.n": 1, "combate.memo1.nafila": "Não"}, f"11.5 dispensado sai da Fila: {got}")
    got = planilha(dict(E2, **{"combate.memo1.pv": 0}), ["combate.n", "combate.memo1.nafila", "combate.memo1.aviso"])
    r.ok(got["combate.n"] == 1 and got["combate.memo1.nafila"] == "Não: caiu" and
         "Descanso Curto" in str(got["combate.memo1.aviso"]), f"11.5 a 0 PV ele some: {got}")
    E3 = dict(E2, **{"grupo.pj1.memo.vel": 14, "grupo.pj1.ag": 1, "grupo.pj1.memo.agi": 1, "grupo.pj1.disc": 0})
    got = planilha(E3, ["combate.fila1.nome", "combate.fila2.nome"])
    r.ok(got == {"combate.fila1.nome": "Dona", "combate.fila2.nome": "Memoespírito de Dona"},
         f"H27 empate total: a dona antes do Memoespírito: {got}")
    # 20.1/21.2: Congelado não vale no Memoespírito (aviso) e ele não fica Quebrado (não tem Tenacidade)
    n = TC.slot(17, 1)
    got = planilha(dict(E2, **{f"combate.c{n}.cond": "Congelado", f"combate.c{n}.turnos": 1}),
                   [f"combate.c{n}.aviso", "combate.n"])
    r.ok(got == {f"combate.c{n}.aviso": "Congelado só em inimigo (21.2)", "combate.n": 2}, f"21.2 Memoespírito: {got}")


def _empate(r, E, rotulo, pref, esperado, msg):
    """Caso de empate fixo: planilha × oráculo (em paralelo) e o oráculo contra a regra do livro (aqui)."""
    _t(E, rotulo, pref)
    r.ok(O.calcular(dict(E))["combate.fila1.nome"] == esperado, msg)


def _fila(r, rng):
    pref = ["combate.f", "combate.fila", "combate.n"]
    # 4 empates fixos (6.10): PJ Ag −1 VEL 13 × Boss VEL 13; PJs decididos por Discernimento; por E; inimigos pela linha
    base = {"grupo.pj1.nome": "Lento", "grupo.pj1.vel": 13, "grupo.pj1.ag": -1, "grupo.pj1.pv": 50,
            "combate.in1.troca": "O Afogado do Poço Sete"}
    _empate(r, base, "empate PJ × Boss", pref, "Lento", "empate de VEL: o PJ vem antes do inimigo (19.3 passo 2)")
    E = {"grupo.pj1.nome": "A", "grupo.pj1.vel": 14, "grupo.pj1.ag": 2, "grupo.pj1.disc": 1,
         "grupo.pj2.nome": "B", "grupo.pj2.vel": 14, "grupo.pj2.ag": 2, "grupo.pj2.disc": 3}
    _empate(r, E, "empate por Discernimento", pref, "B", "empate de VEL e Agilidade: decide o Discernimento")
    E.update({"grupo.pj2.disc": 1, "combate.f1.ordem": 2, "combate.f2.ordem": 1})
    _empate(r, E, "empate por escolha dos jogadores", pref, "B",
            "empate total: a ordem escolhida pelos jogadores (E = 1 primeiro)")
    E = {"combate.in1.troca": "Casco Oco", "combate.in2.troca": "Casco Oco"}
    _empate(r, E, "empate entre inimigos", pref, "Casco Oco 1", "inimigos iguais: decide a linha (H13)")
    for k in range(300):
        _t(_estado_fila(rng, {}), f"Fila {k + 1}", pref + ["combate.pendentes"], limite=3)
    r.info("Fila: 4 empates fixos + 300 estados aleatórios")
    # fases dos 5 Bosses do bestiário: barra × fase em vigor
    for f in [x for x in bestiario_md() if x["fases"] > 1]:
        for pv, fv in ((f["pv"], None), (f["lim2"], None), (f["lim2"], 2), (f["lim2"] + 1, 2), (1, 3), (1, None)):
            E = {"combate.in1.troca": f["nome"], "combate.in1.pv": pv, "combate.in1.fase": fv,
                 "combate.in1.reducao": rng.randint(0, 14), "combate.in1.elemq": rng.choice(ELEM),
                 "campanha.nivel": rng.randint(1, 20), "combate.in1.usada1": rng.choice([None, 1, 2]),
                 "combate.ciclo": rng.randint(1, 5)}
            _t(E, f"fases {f['nome']} pv={pv} fv={fv}", ["combate.in1."])


def _calc(r, rng):
    fontes = list(O and __import__("oraculo_mestre_livro").REDUCAO)
    fichas = bestiario_md()
    for k in range(2000):
        if k % 40 == 0:
            alvo = rng.choice(fichas)["nome"]
            base = {"combate.in1.troca": alvo, "combate.in1.reducao": rng.randint(0, 6),
                    "campanha.nivel": rng.randint(1, 20)}
        E = dict(base)
        E.update({"combate.calc.alvo": alvo if rng.random() < 0.95 else "Ninguém",
                  "combate.calc.fonte": rng.choice(fontes), "combate.calc.n": rng.choice([None, 1, 2, 4, 7]),
                  "combate.calc.f": rng.choice([None, 4, 6, 8, 10, 12]), "combate.calc.fixo": rng.randint(-3, 10),
                  "combate.calc.elem": rng.choice([None] + ELEM), "combate.calc.crit": rng.choice([None, "Sim", "Não"]),
                  "combate.calc.extra": rng.choice([None, 0, 1, 3, 5]),
                  "combate.calc.rolado": rng.choice([None, None, rng.randint(0, 60)])})
        _t(E, f"calculadora {k + 1}", ["combate.calc."], limite=2, modo="bloco", var=VAR_CALC)
    # condições (dano pela Eficiência de quem aplicou, Sangramento com teto, Embaraço e Aprisionamento), várias por
    # combatente (C1/C4 do pedido), expiradas (C6), e o painel C9b (C3) — também com mais de 30 ativas
    conds = list(__import__("oraculo_mestre_livro").CONDICOES)
    pref = ["combate.c", "combate.painel", "combate.pj", "combate.memo", "combate.fila", "combate.f"]
    for k in range(120):
        E = _grupo(rng, 4)
        E.update({"campanha.nivel": rng.randint(1, 20), "combate.in1.troca": rng.choice(fichas)["nome"],
                  "grupo.pj1.memo.tem": "Sim", "combate.memo1.invocado": rng.choice(["Sim", "Não"])})
        if rng.random() < 0.3:
            E["combate.in1.pv"] = 0
        quem = [None, "PJ1", "PJ2", E["combate.in1.troca"], "Memoespírito de PJ1"]
        alvos = [1, 2, 7, 17] if k % 10 else list(range(1, TC.NC + 1))
        for i in alvos:
            for j in range(1, rng.randint(1, 4) + 1 if k % 10 else 5):
                n = TC.slot(i, j)
                E.update({f"combate.c{n}.cond": rng.choice(conds), f"combate.c{n}.acum": rng.choice([None, 1, 3, 7]),
                          f"combate.c{n}.quem": rng.choice(quem),
                          f"combate.c{n}.turnos": rng.choice([None, 0, 1, 2, 3])})
        _t(E, f"condições {k + 1}", pref, peso=2)
    r.info("calculadora: 2 000 casos; condições: 120 estados (4 por combatente, expiradas, painel; 12 com as 88 cheias)")
    _memo_casos(r, rng)


def _memo_casos(r, rng):
    """Memoespírito (pedido do usuário, 11.3–11.5, 19.7): G7/G8 e C2b em 150 estados, na Fila com os PJs e inimigos."""
    pref = ["grupo.pj", "combate.memo", "combate.f", "combate.fila", "combate.n", "combate.st"]
    for k in range(150):
        E = _grupo(rng, rng.randint(1, 6))
        E["campanha.nivel"] = rng.randint(1, 20)
        if k % 3 == 0:
            E.update({"encontros.A.1.criatura": rng.choice([f["nome"] for f in bestiario_md()]),
                      "combate.carregar": "A"})
        memos_aleatorios(rng, E, p=0.8)
        _t(E, f"Memoespírito {k + 1}", pref, limite=4)
    r.info("Memoespírito: 150 estados (G7, G8, C2b, Fila)")


# ---------------------------------------------------------------------------
# ouro — números impressos no livro, calculados NA planilha
# ---------------------------------------------------------------------------

def suite_ouro(args):
    r = Resultado("ouro")

    def conf(rot, E, nome, esperado):
        v = planilha(E, [nome]).get(nome)
        r.ok(TF._igual(v, esperado), f"{rot}: planilha={v!r} livro={esperado!r}")
    # 28.4 — o carcereiro de prisão orbital (Elite, 9-12)
    E = {"inimigos.1.nome": "Carcereiro", "inimigos.1.tipo": "Elite", "inimigos.1.faixa": "9-12",
         "inimigos.acao1.inimigo": "Carcereiro", "inimigos.acao1.tipo": "Especial de controle",
         "inimigos.acao1.nome": "Trancafiar", "inimigos.acao1.recarga": 2, "inimigos.acao1.duracao": 2,
         "inimigos.acao1.condicao": "Lentidão", "inimigos.acao1.tr": "Reflexos"}
    for k, v in {"pv": 225, "defesa": 21, "rd": 3, "ten": 7, "vel": 15, "ataque": "+11", "dano": "4d8 + 1 · média 19",
                 "dt": 17, "tr": "+5", "nfraq": "3", "nafila": "VEL 15, com Firmeza"}.items():
        conf(f"28.4 carcereiro {k}", E, f"inimigos.1.{k}", v)
    conf("28.4 Trancafiar", E, "inimigos.acao1.texto", "Trancafiar (recarga 2 Ciclos): o alvo faz Teste de Reflexos "
                                                       "contra DT 17; se falhar, recebe Lentidão por 2 turnos.")
    # 28.3 / 29.4 — as 15 linhas no modo Faixa (cartões de referência)
    for fx in FAIXAS:
        for t in TIPOS:
            a = ancora(fx, t)
            E = {"inimigos.1.nome": "R", "inimigos.1.tipo": t, "inimigos.1.faixa": fx}
            got = planilha(E, ["inimigos.1.pv", "inimigos.1.dano", "inimigos.1.ten"])
            r.ok(got["inimigos.1.pv"] == a["pv"] and got["inimigos.1.ten"] == a["ten"] and
                 got["inimigos.1.dano"] == f"{a['dano_e']} · média {a['dano_m']}", f"28.3 {fx} {t}: {got}")
    # 27.4 — orçamento nas 5 faixas (grupo de 4) e 16.2 — PH (3–6 jogadores × 3 degraus)
    orc = [(88, 352), (119, 476), (168, 672), (218, 872), (271, 1084)]
    for k, fx in enumerate(FAIXAS):
        got = planilha({"campanha.nivel": 4 * k + 1, "campanha.jogadores": 4}, ["encontros.orc", "encontros.dpc"])
        r.ok((got["encontros.dpc"], got["encontros.orc"]) == orc[k], f"27.4 orçamento {fx}: {got}")
    ph = {3: (4, 5, 6), 4: (5, 6, 7), 5: (6, 7, 8), 6: (7, 8, 9)}
    for j, v in ph.items():
        for d, niv in enumerate((1, 9, 17)):
            got = planilha({"campanha.nivel": niv, "campanha.jogadores": j}, ["campanha.ph_max", "campanha.ph_ini"])
            r.ok((got["campanha.ph_max"], got["campanha.ph_ini"]) == (v[d], v[d] - 2), f"16.2 PH {j} jog. nível {niv}: {got}")
    # 28.11 — as composições prontas: custo, composição reconhecida e "típico" (H6)
    prontos = [("1-4", [("O Afogado do Poço Sete", 1), ("Casco Oco", 1)], 355, "1 Boss + 1 Comum"),
               ("1-4", [("Sargento de Trincheira", 1), ("Peão da Antimatéria", 4)], 320, "1 Elite + 4 Comuns"),
               ("1-4", [("Capataz Oco", 1), ("Sargento de Trincheira", 2)], 360, "3 Elites"),
               ("1-4", [("Larva Fuliginosa", 4), ("Casco Oco", 3)], 350, "7 Comuns"),
               ("17-20", [("Arcanjo de Ferro-Vazio", 1), ("Guarda Pretoriano da Antimatéria", 4)], 985,
                "1 Elite + 4 Comuns"),
               ("17-20", [("Arcanjo de Ferro-Vazio", 2), ("Arauto da Tempestade Vazia", 1)], 1095, "3 Elites"),
               ("17-20", [("Guarda Pretoriano da Antimatéria", 4), ("Escória de Stellaron", 2)], 1085, "7 Comuns")]
    for fx, itens, custo, comp in prontos:
        E = {"campanha.nivel": 1 if fx == "1-4" else 17, "campanha.jogadores": 4}
        for j, (nm, q) in enumerate(itens, start=1):
            E.update({f"encontros.A.{j}.criatura": nm, f"encontros.A.{j}.qtd": q})
        got = planilha(E, ["encontros.A.custo", "encontros.A.composicao", "encontros.A.dificuldade"])
        r.ok(got["encontros.A.custo"] == custo and str(got["encontros.A.composicao"]).startswith(comp) and
             str(got["encontros.A.dificuldade"]).startswith("Encontro típico"), f"28.11 {fx} {comp}: {got}")
    # H7 — Combate A de 29.5: 305 + 50 contra 88 = 4,0 Ciclos (o livro publica 3,7 com o DPC puro de Boss: L3)
    E = {"campanha.nivel": 3, "campanha.jogadores": 4, "encontros.A.1.criatura": "O Afogado do Poço Sete",
         "encontros.A.2.criatura": "Casco Oco", **TC.entradas_grupo([{"nome": f"P{i}", "elemento": e} for i, e in
                                                                   enumerate(["Fogo", "Raio", "Vento", "Gelo"])])}
    conf("H7 Combate A (29.5)", E, "encontros.A.ciclos", 4.0)
    # 19.4 — Firmeza: 7 casas → 2; 1 casa → 1
    conf("19.4 Firmeza 7 → 2", {"combate.in1.troca": "O Afogado do Poço Sete", "combate.f7.atraso": 7},
         "combate.f7.aviso", "Teto/Firmeza: 7 casa(s) viram 2 (19.4)")
    E = {"combate.in1.troca": "O Afogado do Poço Sete", "combate.in2.troca": "Casco Oco", "combate.f7.atraso": 1}
    conf("19.4 Firmeza 1 → 1 (o Boss cai uma casa)", E, "combate.fila1.nome", "Casco Oco")
    # 21.2 — Sangramento: 365 → 18 e 935 → 24 com Eficiência 8
    n1 = TC.slot(7, 1)            # a primeira condição do inimigo 1 (combatente 7) na C7
    for nm, v in (("Arcanjo de Ferro-Vazio", 18), ("O Germe de Pavor", 24)):
        E = {"campanha.nivel": 19, "combate.in1.troca": nm, f"combate.c{n1}.cond": "Sangramento"}
        conf(f"21.2 Sangramento {nm}", E, f"combate.c{n1}.efeito", f"Dano Contínuo: {v} por turno")
    ouro_memo(conf, planilha, r)
    # 20.5 — Dano de Quebra: Fogo 2d6 + 4 · 11 (nível 3) e 2d6 + 16 · 23 (nível 19); Gelo 2 e 8
    for niv, el, ini in ((3, "Fogo", "Fogo: 2d6 + 4 · média 11"), (19, "Fogo", "Fogo: 2d6 + 16 · média 23"),
                         (3, "Gelo", "Gelo: 2 ("), (19, "Gelo", "Gelo: 8 (")):
        E = {"campanha.nivel": niv, "combate.in1.troca": "Casco Oco", "combate.in1.elemq": el}
        v = planilha(E, ["combate.in1.danoquebra"])["combate.in1.danoquebra"]
        r.ok(str(v).startswith(ini), f"20.5 {el} nível {niv}: {v!r}")
    # 20.4 — Ciclo com Quebra: 12 − 4 − 1 − 1 − 2 = 4; depois −4 (Fogo, Fraqueza) = Quebra
    E = {"inimigos.1.nome": "Boss912", "inimigos.1.tipo": "Boss", "inimigos.1.faixa": "9-12", "inimigos.1.f1": "Fogo",
         "inimigos.1.f2": "Gelo", "inimigos.1.f3": "Raio", "inimigos.1.f4": "Físico", "combate.in1.troca": "Boss912",
         "combate.calc.alvo": "Boss912"}
    passos = [("Habilidade de Nível 4", "Fogo", 4), ("Ataque Básico", "Vento", 1), ("Ataque Básico", "Quântico", 1),
              ("Ultimate", "Vento", 2)]
    red = 0
    for fonte, el, v in passos:
        E2 = dict(E, **{"combate.calc.fonte": fonte, "combate.calc.elem": el, "combate.in1.reducao": red})
        got = planilha(E2, ["combate.calc.reducao"])["combate.calc.reducao"]
        r.ok(got == v, f"20.4 {fonte} {el}: redução {got!r} (livro {v})")
        red += v
    conf("20.4 Tenacidade no fim do Ciclo 1", dict(E, **{"combate.in1.reducao": red}), "combate.in1.tenat", 4)
    conf("20.4 Ciclo 2: Quebra", dict(E, **{"combate.in1.reducao": red + 4}), "combate.in1.quebrado", "Sim")
    # 23.4 — Vesper (Presença +0): 1 sucesso, 2 falhas, ainda Morrendo; 3 falhas, morre
    E = {"grupo.pj1.nome": "Vesper", "grupo.pj1.pv": 40, "grupo.pj1.pres": 0, "combate.pj1.pv": 0,
         "combate.pj1.suc": 1, "combate.pj1.fal": 2}
    conf("23.4 Vesper", E, "combate.pj1.situacao", "Morrendo: d20+0, sem Eficiência contra DT 10. Dano recebido = +1 "
                                                   "falha (2 se crítico ou Habilidade de Nível 5+)")
    conf("23.4 três falhas", dict(E, **{"combate.pj1.fal": 3}), "combate.pj1.situacao", "Morre (3 falhas, 23.4)")
    # 27.2 / 20.2 — DT Média e DT de Fraqueza por faixa
    for k, (m, f) in enumerate(zip((13, 16, 19, 22, 25), (13, 14, 15, 16, 17))):
        got = planilha({"campanha.nivel": 4 * k + 2}, ["campanha.dt_media", "campanha.dt_fraqueza"])
        r.ok((got["campanha.dt_media"], got["campanha.dt_fraqueza"]) == (m, f), f"27.2/20.2 faixa {k + 1}: {got}")
    from mestre import testes_hist
    testes_hist.ouro_fase2(r)          # 24.3, 24.5, 25.1, 25.2, 25.3, 26.7 na aba Recompensas
    from mestre import testes_fase3
    testes_fase3.ouro_fase3(r)         # 27.9, 23.3, 23.6, 27.2, 26.1, 26.7, loja, H16, H17, H23 (Fase 3)
    return r


# ---------------------------------------------------------------------------
# determinismo — propriedades (a)–(g) da seção 5
# ---------------------------------------------------------------------------

def _chi2(cont, n, total):
    e = total / n
    return sum((cont.get(k, 0) - e) ** 2 / e for k in range(n))


def suite_determinismo(args):
    r = Resultado("determinismo")
    S0 = 12345
    idx = lambda s, g, rr, c, n: O.escolha(O.valor(s, g, rr, c), n)  # noqa: E731
    for g in (100, 110, 200, 300, 400, 410, 420, 510, 520, 530, 540, 550, 560, 600, 610, 620, 630, 640, 650, 701, 710):
        # (c) trocar R muda ≥ 90% (lista de 30, 200 rolagens)
        muda = sum(idx(S0, g, R, 2, 30) != idx(S0, g, R + 1, 2, 30) for R in range(1, 201))
        r.ok(muda >= 180, f"(c) G={g}: só {muda}/200 rolagens mudaram")
        # (d) toda entrada aparece em 2 000 rolagens; (e) ±25% em 100 000 (lista de 100). Com 20 000 (média 200,
        # desvio 14) a tolerância é de 3,5 desvios: com 21 G, um sorteio uniforme falha em cerca de metade das
        # rodadas (G = 540 deu 254 com χ² = 98 em 99 graus); com 100 000 (média 1 000) ela é de 7,9 desvios
        for n in (6, 30, 100):
            vistos = {idx(S0, g, R, 3, n) for R in range(1, 2001)}
            r.ok(len(vistos) == n, f"(d) G={g} lista {n}: {len(vistos)} entradas em 2 000 rolagens")
        cont = {}
        for R in range(1, 100001):
            k = idx(S0, g, R, 4, 100)
            cont[k] = cont.get(k, 0) + 1
        r.ok(len(cont) == 100 and min(cont.values()) >= 750 and max(cont.values()) <= 1250,
             f"(e) G={g}: frequências {min(cont.values())}–{max(cont.values())} (esperado 1 000 ± 25%)")
        # (f) pares C=8 × C=10, listas de 30
        pares = {(idx(S0, g, R, 8, 30), idx(S0, g, R, 10, 30)) for R in range(1, 2001)}
        r.ok(len(pares) >= 540, f"(f) G={g}: {len(pares)}/900 pares")
        # (g) correlação serial: χ² das diferenças 1ª a 5ª, entre rolagens e entre campos
        for n, crit in ((6, 20.5), (30, 58.3)):
            for modo in ("R", "C"):
                seq = [idx(S0, g, R, 5, n) if modo == "R" else idx(S0, g, 1 + R // 20, 1 + R % 20, n)
                       for R in range(1, 4001)]
                for d in range(1, 6):
                    dif = seq
                    for _ in range(d):
                        dif = [(b - a) % n for a, b in zip(dif, dif[1:])]
                    cont = {}
                    for v in dif:
                        cont[v] = cont.get(v, 0) + 1
                    c2 = _chi2(cont, n, len(dif))
                    r.ok(c2 < crit, f"(g) G={g} n={n} {modo} diferença {d}: χ² {c2:.1f} ≥ {crit}")
        trip = {(O.dado(O.valor(S0, g, R, 1, ), 6), O.dado(O.valor(S0, g, R, 2), 6), O.dado(O.valor(S0, g, R, 3), 6))
                for R in range(1, 2001)}
        r.ok(len(trip) == 216, f"(g) G={g}: {len(trip)}/216 triplas de d6")
    # limites < 2^53 nos extremos (o oráculo faz assert em cada intermediário)
    for s in (1, 2147483646):
        for g in (100, 710):
            for R in (1, 1000000):
                for c in (1, 400):
                    O.uyx(s, g, R, c)
    r.info(f"maior intermediário nos extremos: {O.maior_intermediario():.3e} (< 2^53)")
    # planilha = oráculo em u, y, x: G = 100 (8 campos) e G = 110 (84 campos), 300 rolagens × 3 sementes
    ger = TC.mapa()["geradores"]
    t0 = time.time()
    for s in (1, 2026, 2147483646):
        for R in range(1, 301):
            E = {"inicio.semente": s, "encontros.ale.rolagem": R, "inimigos.rolagem": R, "npcs.rolagem": R,
                 "aventuras.rolagem": R, "recompensas.ach.rolagem": R, "recompensas.cone.rolagem": R,
                 "recompensas.conj.rolagem": R}
            from mestre.testes_fase3 import ROLAGENS
            E.update({k: R for k in ROLAGENS})          # Fase 3: G = 510…650 e 701…710
            refs, esp = [], {}
            for g in ("100", "110", "200", "300", "400", "410", "420", "510", "520", "530", "540", "550", "560",
                      "600", "610", "620", "630", "640", "650", *[str(700 + t) for t in range(1, 11)]):
                campos = ger[g]["campos"]
                passo_c = max(1, len(campos) // (8 if int(g) < 500 else 3))     # Fase 3: 3 campos por gerador
                for c in (campos if R % 50 == 1 else list(campos)[::passo_c]):
                    u, y, x = O.uyx(s, int(g), R, int(c))
                    for k, v in zip("uyx", (u, y, x)):
                        refs.append(campos[c][k])
                        esp[campos[c][k]] = v
            # em blocos de até 60 saídas: testar_ficha.Modelo guarda o grafo reduzido (shrink) só até 60 saídas; com
            # mais, recalcula o modelo inteiro a cada rolagem (a Fase 2 triplicou o modelo)
            sol = {}
            for k0 in range(0, len(refs), 60):
                sol.update(TC.modelo().calcular(TC.entradas(E), refs[k0:k0 + 60]))
            for ref in refs:
                r.ok(sol.get(ref) == esp[ref], f"(a) S={s} R={R} {ref}: planilha={sol.get(ref)} oráculo={esp[ref]}")
    r.info(f"u/y/x da planilha = oráculo: G = 100, 110, 200, 300, 400, 410, 420, 510…560, 600…650 e 701…710, 300 "
           f"rolagens × 3 sementes ({time.time() - t0:.0f} s)")
    # (a) recalcular duas vezes dá o mesmo; (b) entradas fora da tabela de parâmetros não mudam o sorteio
    outs = [TC.C(f"encontros.ale.v{k}.criatura") for k in range(1, 8)] + \
           [ger["110"]["campos"][c]["x"] for c in list(ger["110"]["campos"])[:12]] + \
           [v for k, v in TC.mapa()["celulas"].items() if ":" not in v and (
               k.startswith(("npcs.res.", "aventuras.res.")) or k in ("recompensas.ach.item1", "recompensas.ach.item2",
                                                                     "recompensas.ach.creditos.valor",
                                                                     "recompensas.ach.bugiganga", "recompensas.cone.nome",
                                                                     "recompensas.cone.efeito", "recompensas.conj.nome",
                                                                     "recompensas.conj.p4")) and not k.endswith(".origem")]
    # Fase 3: um campo de cada gerador novo
    outs += [TC.C(n) for n in ("mundos.planeta.nome", "mundos.estacao.funcao", "mundos.nave.nome", "mundos.faccao.nome",
                               "mundos.org.nome", "mundos.nomes.1.pessoa", "improviso.rumor.1", "improviso.evento.evento",
                               "improviso.loja.1.item", "improviso.bug.1", "improviso.oraculo.resposta",
                               "improviso.rol.1.dados", "minhas.1.resultado", "mundos.nomes.cultura_ef",
                               "improviso.evento.onde_ef", "improviso.loja.tipo_ef", "improviso.oraculo.rolagem")]
    base = {"inicio.semente": 777, "encontros.ale.rolagem": 9, **_grupo_fixo(0), "improviso.rol.1.n": 3,
            **{f"minhas.1.vaga{k}": f"Entrada {k}" for k in range(1, 13)}, "minhas.1.quantos": 3}
    a1 = TC.modelo().calcular(TC.entradas(base), outs)
    a2 = TC.modelo().calcular(TC.entradas(base), outs)
    r.ok(a1 == a2, "(a) recalcular duas vezes mudou o resultado")
    rng = random.Random(5)
    params = {"inicio.semente", "encontros.ale.rolagem", "encontros.ale.ambiente", "encontros.ale.faixa",
              "encontros.ale.composicao", "inimigos.rolagem", "campanha.nivel", "encontros.faixa_troca",
              "campanha.jogadores"}     # jogadores: o orçamento das cenas da aventura (27.4), não o sorteio
    from mestre.testes_fase3 import ROLAGENS
    params |= set(ROLAGENS) | {"mundos.nomes.cultura", "improviso.evento.onde", "improviso.loja.tipo",
                               "improviso.oraculo.prob"}
    alheias = [n for n in TC.mapa()["entradas"] if n.split(".")[0] in ("combate", "bestiario", "campanha")
               and n not in params and not n.startswith(("campanha.nivel",))]
    for nome in rng.sample(alheias, 50):
        info = TC.mapa()["entradas"][nome]
        a3 = TC.modelo().calcular(TC.entradas(dict(base, **{nome: info["amostra"]})), outs)
        r.ok(a3 == a1, f"(b) mudar {nome} (fora dos parâmetros) mudou o sorteio")
    for nome, v in (("encontros.ale.ambiente", "Ruína"), ("encontros.ale.faixa", "17-20"),
                    ("encontros.ale.composicao", "3 Elites"), ("inicio.semente", 778), ("encontros.ale.rolagem", 10),
                    ("npcs.rolagem", 2), ("npcs.raca", "Vulpes"), ("npcs.caminho", "A Caça"), ("aventuras.rolagem", 2),
                    ("aventuras.tipo", "Fuga"), ("aventuras.faixa", "17-20"), ("aventuras.faccao", "Autômatos"),
                    ("recompensas.ach.rolagem", 2), ("recompensas.ach.faixa", "13-16"), ("recompensas.cone.rolagem", 2),
                    ("recompensas.conj.rolagem", 2),
                    # Fase 3 (§5: 510–560 só a cultura no 560; 610 onde; 620 tipo de loja; 640 probabilidade; 650 as
                    # expressões; 701–710 a própria tabela e "quantos")
                    ("mundos.r510", 2), ("mundos.r520", 2), ("mundos.r530", 2), ("mundos.r540", 2), ("mundos.r550", 2),
                    ("mundos.r560", 2), ("mundos.nomes.cultura", "Vulpes"), ("improviso.r600", 2),
                    ("improviso.r610", 2), ("improviso.evento.onde", "Espaço"), ("improviso.r620", 2),
                    ("improviso.loja.tipo", "Farmácia"), ("improviso.r630", 2), ("improviso.r640", 2),
                    ("improviso.oraculo.prob", "Quase impossível"), ("improviso.r650", 2), ("improviso.rol.1.n", 5),
                    ("minhas.1.rolagem", 2), ("minhas.1.quantos", 5), ("minhas.1.vaga50", "Nova entrada")):
        a4 = TC.modelo().calcular(TC.entradas(dict(base, **{nome: v})), outs)
        r.ok(a4 != a1, f"(b) o parâmetro {nome} não mudou nenhum campo")
    # (b) ambiente (revisão da Fase 1, F5): o caso discrimina (no oráculo, o ambiente muda as criaturas sorteadas),
    # a planilha segue o oráculo, e toda criatura sorteada é de uma facção daquele ambiente (H8)
    from oraculo_mestre_livro import AMBIENTE
    fac = {f["nome"]: (f["faccao"], f["origem2"]) for f in bestiario_md()}
    nv = [f"encontros.ale.v{k}.criatura" for k in range(1, 8)]
    esp0 = O.calcular(dict(base))
    for amb in ("Ruína", "Frente de guerra"):
        Ea = dict(base, **{"encontros.ale.ambiente": amb})
        esp = O.calcular(dict(Ea))
        r.ok([esp[n] for n in nv] != [esp0[n] for n in nv], f"(b) o caso de teste não discrimina o ambiente {amb}")
        sol = planilha(Ea, nv)
        r.ok([sol[n] for n in nv] == [esp[n] for n in nv],
             f"(b) ambiente {amb}: planilha={[sol[n] for n in nv]} oráculo={[esp[n] for n in nv]}")
        fora = [v for v in (sol[n] for n in nv) if v and not any(a == amb and fc in fac[v] for fc, a in AMBIENTE)]
        r.ok(not fora, f"(b) ambiente {amb}: criatura de outra facção sorteada: {fora}")
    r.info("(b) ambiente: 'Ruína' e 'Frente de guerra' mudam as criaturas sorteadas no caso base (semente 777, "
           "rolagem 9), e a planilha segue o oráculo")
    return r
