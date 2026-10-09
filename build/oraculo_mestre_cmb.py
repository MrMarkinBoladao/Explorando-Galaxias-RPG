# -*- coding: utf-8 -*-
"""
oraculo_mestre_cmb.py — o oráculo das abas Encontros (27.4, 27.5, 20.2, H5–H7, H19) e Combate (19.3–19.6, 20.2–20.5,
21.5, 23.1–23.5, 28.5, H13). Mesma convenção de oraculo_mestre_abas.py.
"""
from decimal import Decimal, ROUND_HALF_UP

import oraculo_mestre as S
from oraculo_mestre_abas import num, tx, clamp, achar
from oraculo_mestre_livro import (FAIXAS, ELEM, ORC, DT_FRAQ, ATTR, COMPOS, QUEBRA, REDUCAO, CONDICOES, AMBIENTE,
                                  TEXTO_21_5, bestiario_md, ancora)


def xround(x, d):
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))


def junta(w):
    return w[0] + "".join(", " + x for x in w[1:] if x)


def encontros(E, out, cat, elems, racas):
    t = E.get("encontros.npj_troca")
    npj = clamp(int(t), 1, 6) if num(t) else out["campanha.jogadores_ef"]
    fx = E.get("encontros.faixa_troca") if E.get("encontros.faixa_troca") in FAIXAS else out["campanha.faixa"]
    fi = FAIXAS.index(fx) + 1
    dpc4, orc4 = ORC[fi - 1]
    orc = orc4 if npj == 4 else orc4 * npj // 4
    dpc = dpc4 if npj == 4 else dpc4 * npj // 4
    out.update({"encontros.npj": npj, "encontros.faixa": fx, "encontros.orc4": orc4, "encontros.dpc4": dpc4,
                "encontros.orc": orc, "encontros.dpc": dpc,
                "encontros.attrition": f"Attrition de referência (27.7), faixa {fx}: o grupo termina um combate típico "
                                       f"com {ATTR[fi - 1]} dos PV. Dois combates por dia é um dia tranquilo, três é um "
                                       f"dia de verdade, quatro é emergência."})
    salvos = {}
    for X in "ABC":
        p = f"encontros.{X}"
        L = []
        for j in range(1, 9):
            g = lambda k: E.get(f"{p}.{j}.{k}")  # noqa: E731
            idx = achar(cat, tx(g("criatura")))
            c = cat[idx] if idx is not None else None
            q = (clamp(int(g("qtd")), 0, 10) if num(g("qtd")) else 1) if c else 0
            F = [tx(g(f"f{k}")) for k in range(1, 5)]
            w = ["" if q == 0 else (F[k] if any(F) else c["f"][k]) for k in range(4)]
            res = "" if q == 0 else c["res"]
            L.append({"c": c, "q": q, "w": w, "res": res, "nome": c["nome"] if c else ""})
            pj = f"{p}.{j}"
            out.update({f"{pj}.tipo": c["tipo"] if c else "", f"{pj}.pv": c["pv"] if c else "",
                        f"{pj}.custo": c["custo"] * q if c else "", f"{pj}.faixa": c["faixa"] if c else "",
                        f"{pj}.fraq": junta(w), f"{pj}.res": (res or "—") if c else "",
                        f"{pj}.acoes": c["acoes"] * q if c else ""})
        custo = sum(x["c"]["custo"] * x["q"] for x in L if x["c"])
        todas = [w for x in L for w in x["w"]]
        cn = 0
        for k, e in enumerate(ELEM, start=1):
            v = ("Sim" if e in todas else "Não") if e in elems else "—"
            cn += v == "Sim"
            out[f"{p}.contrato.{k}"] = v
        nb = sum(x["q"] for x in L if x["c"] and x["c"]["tipo"] == "Boss")
        ne = sum(x["q"] for x in L if x["c"] and x["c"]["tipo"] == "Elite")
        nc = sum(x["q"] * (1.5 if x["nome"] == "Escória de Stellaron" else 1) for x in L
                 if x["c"] and x["c"]["tipo"] == "Comum")                         # Escória = 1,5 Comum (28.10)
        comp = next((f"{n} — {s} ({d}, 27.4)" for n, (b, e_, c_), s, d in COMPOS if (b, e_, c_) == (nb, ne, nc)), "")
        r = custo / orc if orc else 0
        dif = ("Cena de passagem — cerca de 2 Ciclos (27.4)" if r <= 0.6 else "Encontro típico — 3 a 5 Ciclos (27.4)"
               if r <= 1.15 else "Pesado" if r <= 1.6 else "Dois orçamentos num só encontro: passa de 6 Ciclos (27.4)")
        bad = any(x["q"] > 0 and x["res"] and elems.count(x["res"]) >= 2 for x in L)
        mf = max([x["c"]["fidx"] for x in L if x["q"] > 0] + [0])
        z = custo == 0
        out.update({
            f"{p}.custo": custo, f"{p}.pct": xround(custo * 100 / orc, 0) if orc > 0 else "",
            f"{p}.ciclos": "" if z or dpc == 0 else xround(custo / dpc + (1 if cn < 3 else 0), 1),
            f"{p}.dificuldade": "" if z else dif, f"{p}.contrato_n": cn,
            f"{p}.contrato": "" if z else ("Cumprido" if cn >= 3 else "Não cumprido"),
            f"{p}.composicao": "" if z else (comp or f"{nb} Boss, {ne} Elite, {tx(nc)} Comum: não é uma das quatro "
                                                      f"composições de 27.4"),
            f"{p}.irma": "" if z else ("Há Resistência no Elemento de dois personagens: troque-a (27.5)" if bad else
                                       "Nenhuma Resistência aponta para o Elemento de dois personagens (27.5)"),
            f"{p}.dt": "" if z else (f"DT para descobrir Fraqueza: {DT_FRAQ[max(1, mf) - 1]} (20.2, faixa do mais forte)"
                                     + ("; Intellitron: Vantagem e 2 por sucesso" if "Intellitron" in racas else ""))})
        salvos[X] = L
    salvos["R"] = aleatorio(E, out, elems)
    return salvos


def aleatorio(E, out, elems):
    sem, rol = out["inicio.semente_ef"], S.rolagem_efetiva(E.get("encontros.ale.rolagem"))
    x = {c: S.valor(sem, 100, rol, c) for c in range(1, 9)}
    nomes_c = ["Sortear"] + [n for n, *_ in COMPOS]
    cp = E.get("encontros.ale.composicao")
    comp = nomes_c.index(cp) if cp in nomes_c and cp != "Sortear" else S.escolha(x[1], 4)
    fx = E.get("encontros.ale.faixa") if E.get("encontros.ale.faixa") in FAIXAS else out["campanha.faixa"]
    amb = tx(E.get("encontros.ale.ambiente"))
    fichas = bestiario_md()

    def ok_amb(f):
        return (not amb or amb == "Qualquer" or
                any(a == amb and (fc == f["faccao"] or (f["origem2"] and fc == f["origem2"])) for fc, a in AMBIENTE))
    tipos = {1: ["Boss", "Comum"], 2: ["Elite"] + ["Comum"] * 4, 3: ["Elite"] * 3, 4: ["Comum"] * 7}[comp]
    vagas = []
    for k in range(1, 8):
        tp = tipos[k - 1] if k <= len(tipos) else ""
        f = None
        if tp:
            ca = [f_ for f_ in fichas if f_["tipo"] == tp and f_["faixa"] == fx and ok_amb(f_)]
            cf = [f_ for f_ in fichas if f_["tipo"] == tp and f_["faixa"] == fx]
            lista = ca if ca else cf
            j = S.escolha(x[k + 1], len(lista))
            f = lista[j - 1] if j >= 1 else None
        vagas.append(f)
    # H19: varredura vaga 1…7 × Fraqueza 1…4; faltantes na ordem de 20.1; nunca igual à Resistência
    pos = [(k, j, (f["fraquezas"][j] if f and j < len(f["fraquezas"]) else ""), (f["res"] if f else ""))
           for k, f in enumerate(vagas) for j in range(4)]
    orig = [v for _, _, v, _ in pos]
    M = [e for e in ELEM if e in elems and e not in orig]
    c0 = sum(1 for e in ELEM if e in elems and e in orig)
    need = min(max(0, 3 - c0), len(M))
    kk, novo = 0, {}
    for k, j, v, r in pos:
        s_ = 1 if v and v not in elems else 0
        if s_ and kk < need and M[kk] != r:
            kk += 1
            novo[(k, j)] = M[kk - 1]
        else:
            novo[(k, j)] = v
    total = 0
    for k, f in enumerate(vagas, start=1):
        p = f"encontros.ale.v{k}"
        out.update({f"{p}.criatura": f["nome"] if f else "", f"{p}.qtd": 1 if f else "",
                    f"{p}.tipo_v": f["tipo"] if f else "", f"{p}.pv": f["pv"] if f else "",
                    f"{p}.custo": f["custo"] if f else ""})
        for j in range(4):
            out[f"{p}.f{j + 1}"] = novo[(k - 1, j)]
        total += f["custo"] if f else 0
    out["encontros.ale.leitura"] = "" if not vagas[0] else (
        f"Custo {tx(total)} de {out['encontros.orc']} · contrato: {c0 + kk} Elemento(s) do grupo como Fraqueza" +
        (" (cumprido)" if c0 + kk >= 3 else " (não cumprido)") + f" · composição: {nomes_c[comp]}")
    return [{"nome": f["nome"] if f else "", "q": 1 if f else 0, "w": [novo[(k, j)] for j in range(4)]}
            for k, f in enumerate(vagas)]


# ---------------------------------------------------------------------------
# Combate
# ---------------------------------------------------------------------------

def combate(E, out, cat, salvos, grupo_raw):
    g = E.get
    cic = max(1, int(g("combate.ciclo"))) if num(g("combate.ciclo")) else 1
    src = ["Nenhum", "A", "B", "C", "Aleatório"]
    s_ = src.index(g("combate.carregar")) if g("combate.carregar") in src else 0
    enc = salvos[{1: "A", 2: "B", 3: "C", 4: "R"}[s_]] if s_ else []
    cum, acc = [], 0
    for L in enc:
        acc += L["q"]
        cum.append(acc)
    C = []
    for i in range(1, 7):
        pj = grupo_raw[i - 1]
        nome = tx(pj.get("nome"))
        ex = 1 if nome and g(f"combate.pj{i}.participa") != "Não" else 0
        pvmax = max(1, pj["pv"]) if num(pj.get("pv")) else 1
        pv = g(f"combate.pj{i}.pv")
        fal = g(f"combate.pj{i}.fal")
        c = {"lab": nome, "tipo": "PJ", "ex": ex, "pvmax": pvmax,
             "pvat": clamp(int(pv), 0, pvmax) if num(pv) else pvmax,
             "velb": pj["vel"] if num(pj.get("vel")) else 10, "aj": g(f"combate.pj{i}.ajvel"),
             "tag": clamp((pj["ag"] if num(pj.get("ag")) else 0) + 20, 15, 30),
             "tdisc": clamp((pj["disc"] if num(pj.get("disc")) else 0) + 20, 15, 30),
             "ttipo": 5 + (5 - (clamp(int(g(f"combate.f{i}.ordem")), 1, 5) if num(g(f"combate.f{i}.ordem")) else 5)),
             "tlin": (10 - i) / 100, "ef": out["campanha.ef"], "cong": 0}
        c["vivo"] = 1 if ex and not (num(fal) and fal >= 3) else 0
        C.append(c)
    nomes_in = []
    for e in range(1, 11):
        dj = sum(1 for v in cum if v < e) + 1 if cum and max(cum) >= e else None
        dn = enc[dj - 1]["nome"] if dj else ""
        troca = tx(g(f"combate.in{e}.troca"))
        nm = troca or dn
        nomes_in.append((nm, dj, troca, dn))
    for e, (nm, dj, troca, dn) in enumerate(nomes_in, start=1):
        idx = achar(cat, nm)
        k = cat[idx] if idx is not None else None
        rep = sum(1 for x in nomes_in if x[0] == nm)
        lab = "" if not nm else nm + (f" {sum(1 for x in nomes_in[:e] if x[0] == nm)}" if rep > 1 else "")
        pvmax = k["pv"] if k else 1
        pv = g(f"combate.in{e}.pv")
        c = {"lab": lab, "tipo": k["tipo"] if k else "", "ex": 1 if k else 0, "pvmax": pvmax,
             "pvat": clamp(int(pv), 0, pvmax) if num(pv) else pvmax, "velb": k["vel"] if k else 0,
             "aj": g(f"combate.in{e}.ajvel"), "tag": 0, "tdisc": 0, "ttipo": 0, "tlin": (20 - e) / 100,
             "ef": k["ef"] if k else 0, "k": k, "dj": dj, "troca": troca, "dn": dn, "e": e}
        c["vivo"] = 1 if k and c["pvat"] > 0 else 0
        C.append(c)
    grupo_memo(E, out)
    for m in range(1, 7):                                    # os Memoespíritos dos PJs 1–6 (11.5, 19.7)
        dono, p = C[m - 1], f"grupo.pj{m}.memo"
        nm, mn = tx(grupo_raw[m - 1].get("nome")), tx(g(f"{p}.nome"))
        lab = ((f"{mn} (de {nm})" if mn else f"Memoespírito de {nm}") if nm and g(f"{p}.tem") == "Sim" else "")
        pv_ef, vel_ef = out[f"{p}.pv_ef"], out[f"{p}.vel_ef"]
        pvmax = max(1, pv_ef) if num(pv_ef) else 1
        pv = g(f"combate.memo{m}.pv")
        agi, di = g(f"{p}.agi"), g(f"{p}.disc")
        c = {"lab": lab, "tipo": "Memoespírito", "pvmax": pvmax,
             "ex": 1 if lab and dono["ex"] and g(f"combate.memo{m}.invocado") == "Sim" else 0,
             "pvat": clamp(int(pv), 0, pvmax) if num(pv) else pvmax, "velb": vel_ef if num(vel_ef) else 10,
             "aj": g(f"combate.memo{m}.ajvel"), "tag": clamp((agi if num(agi) else 0) + 20, 15, 30),
             "tdisc": clamp((di if num(di) else 0) + 20, 15, 30), "ttipo": 5, "tlin": (30 - m) / 1000,
             "ef": out["campanha.ef"], "cong": 0, "m": m}
        c["vivo"] = 1 if c["ex"] and c["pvat"] > 0 else 0
        C.append(c)
    # C7: 4 condições por combatente, com o rótulo fixo da linha (como a planilha, que conta pelo rótulo)
    conds = []
    for n in range(1, len(C) * NSLOT + 1):
        i = (n - 1) // NSLOT
        rotulo = C[i]["lab"] or f"{i + 1} · (vazio)"
        conds.append((rotulo, tx(g(f"combate.c{n}.cond")), g(f"combate.c{n}.turnos"), i))
    for c in C[6:16]:
        c["cong"] = 1 if c["lab"] and any(cb == c["lab"] and co == "Congelado" and not (num(t) and t == 0)
                                          for cb, co, t, _ in conds) else 0
    for i, c in enumerate(C, start=1):
        aj = c["aj"]
        c["vel"] = clamp(c["velb"] + (clamp(int(aj), -10, 10) if num(aj) else 0), 0, 40)
        c["chave"] = c["vel"] * 100000 + c["tag"] * 1000 + c["tdisc"] * 10 + c["ttipo"] + c["tlin"]
        c["congc"] = c["cong"] == 1 and c["tipo"] == "Comum"
        c["ativo"] = 1 if c["vivo"] and not c["congc"] else 0
        c["surp"] = 1 if cic == 1 and c["lab"] and any(cb == c["lab"] and co == "Surpreso" and not (num(t) and t == 0)
                                                       for cb, co, t, _ in conds) else 0
        f = lambda k, i=i: g(f"combate.f{i}.{k}")  # noqa: E731
        b = max(0, int(f("atraso"))) if num(f("atraso")) else 0
        t = c["tipo"]
        c["bruto"] = b
        c["firm"] = 2 if (c["cong"] and t != "Comum") else min(3, b) if t == "Comum" else \
            ((0 if b == 0 else min(2, max(1, b // 2))) if t in ("Elite", "Boss") else b)
        teto = 3 if t == "Comum" else 999 if t in ("PJ", "Memoespírito") else 2
        c["pendp"] = 0 if c["congc"] else min(teto, max(0, int(f("pend"))) if num(f("pend")) else 0)
        c["ja"] = 1 if f("ja") == "Sim" else 0
        c["avc"] = 0 if c["ja"] else (max(0, int(f("avancar"))) if num(f("avancar")) else 0)
        c["man"] = f("manual") if num(f("manual")) else None
        c["teto"] = teto
    n = sum(c["ativo"] for c in C)
    for i, c in enumerate(C, start=1):
        if c["ativo"]:
            c["base"] = 1 + sum(1 for o in C if o["ativo"] and o["chave"] > c["chave"])
            d = c["pendp"] + (0 if c["ja"] else c["firm"])
            c["posr"] = c["base"] + d
            c["exc"] = c["posr"] - min(n, c["posr"])
            c["ch2"] = (c["man"] - 0.7 + i / 1000) if c["man"] is not None else \
                (min(n, c["posr"]) + (0.5 if d > 0 else 0) - c["avc"] - (0.5 if c["avc"] > 0 else 0) + i / 1000)
        else:
            c["exc"] = 0
        c["pendn"] = 0 if (not c["vivo"] or c["congc"]) else min(c["teto"], (c["firm"] if c["ja"] else 0) + c["exc"])
    for i, c in enumerate(C, start=1):
        if c["vivo"]:
            c["chn"] = 1 + sum(1 for o in C if o["vivo"] and o["chave"] > c["chave"]) + c["pendn"] + \
                (0.5 if c["pendn"] > 0 else 0) + i / 1000
        c["flag"] = 1 if c["ativo"] and not c["ja"] and not c["surp"] else 0
        out[f"combate.f{i}.vel"] = c["vel"] if c["ex"] else ""
        out[f"combate.f{i}.pendn"] = c["pendn"] if c["ex"] else ""
    atual = sorted([c for c in C if c["ativo"]], key=lambda c: c["ch2"])
    prox = sorted([c for c in C if c["vivo"]], key=lambda c: c["chn"])
    vistos = 0
    for k in range(1, len(C) + 1):
        p = f"combate.fila{k}"
        c = atual[k - 1] if k <= len(atual) else None
        if c:
            vistos += c["flag"]
            sit = "Surpreso: casa pulada" if c["surp"] else "Já agiu" if c["ja"] else \
                ("Agindo agora" if c["flag"] and vistos == 1 else "")
        out.update({f"{p}.casa": k if c else "", f"{p}.nome": c["lab"] if c else "", f"{p}.vel": c["vel"] if c else "",
                    f"{p}.situacao": sit if c else ""})
        cn = prox[k - 1] if k <= len(prox) else None
        out.update({f"{p}.nome_n": cn["lab"] if cn else "", f"{p}.vel_n": cn["vel"] if cn else "",
                    f"{p}.pend_n": cn["pendn"] if cn else ""})
    out.update({"combate.ph_max": out["campanha.ph_max"], "combate.ph_ini": out["campanha.ph_ini"], "combate.n": n})
    _pjs(E, out, C, grupo_raw)
    _inimigos(E, out, C, enc, cic)
    _memos(E, out, C)
    _condicoes(E, out, C, conds)
    _calc(E, out, C)


NSLOT, NPAINEL = 4, 30


def grupo_memo(E, out):
    """Aba Grupo, G7 e G8 (11.3, 11.4): os números que o Combate usa e os avisos."""
    g = E.get
    nv, ef, fi = out["campanha.nivel_ef"], out["campanha.ef"], out["campanha.faixa_idx"]
    for i in range(1, 7):
        p = f"grupo.pj{i}.memo"
        on = g(f"{p}.tem") == "Sim"
        v = {k: g(f"{p}.{k}") for k in ("pv", "def", "vel", "rd", "agi", "disc", "vigor")}
        n0 = {k: (x if num(x) else 0) for k, x in v.items()}
        livro = {"pv": 8 * nv + 3 * n0["vigor"], "def": 10 + n0["agi"] + ef, "vel": 10 + n0["agi"] + 1, "rd": 0}
        for k in ("pv", "def", "vel", "rd"):
            out[f"{p}.{k}_ef"] = (v[k] if num(v[k]) else livro[k]) if on else ""
        out[f"{p}.dano"] = (f"{fi}d6 + pontos no Atributo de ataque ({fi + 1}d6 se a arma do dono for de Energia)"
                            if on else "")
        out[f"{p}.rt"] = (2 if nv >= 11 else 1) if on else ""
        out[f"{p}.nome_v"] = (tx(g(f"{p}.nome")) or "(sem nome)") if on else "—"
        out[f"{p}.aviso2"] = ("Campo vazio em G7: usando 11.4 sem Bênção nem Bônus menor; digite o da ficha"
                              if on and not all(num(v[k]) for k in ("pv", "def", "vel")) else "")
        nome, cam = tx(g(f"grupo.pj{i}.nome")), tx(g(f"grupo.pj{i}.caminho"))
        if on:
            a = ("PJ sem nome em G1: o Memoespírito não entra no Combate" if not nome else
                 "O Memoespírito é da Recordação (11.1); este PJ é de outro Caminho" if cam and cam != "A Recordação"
                 else "VEL abaixo de 10 + Agilidade + 1 (11.4): confira na ficha" if num(v["vel"]) and
                 v["vel"] < 10 + n0["agi"] + 1 else
                 "Defesa abaixo de 10 + Agilidade + Eficiência (11.4): confira na ficha" if num(v["def"]) and
                 v["def"] < 10 + n0["agi"] + ef else
                 "PV abaixo de 8 × nível + 3 × Vigor (11.4): confira na ficha" if num(v["pv"]) and
                 v["pv"] < 8 * nv + 3 * n0["vigor"] else
                 "Pontos acima de 12 + 1 a cada 2 níveis (11.3)" if n0["agi"] + n0["disc"] + n0["vigor"] > 12 + nv // 2
                 else "")
        else:
            algum = tx(g(f"{p}.nome")) + "".join(tx(x) for x in v.values())
            a = "Marque Sim em Tem? para o Memoespírito aparecer no Combate" if algum else ""
        out[f"{p}.aviso1"] = a


def _memos(E, out, C):
    """Aba Combate, C2b (11.5): VEL, PV, Defesa, "Na Fila?" e o aviso de cada Memoespírito."""
    g = E.get
    for c in C[16:]:
        m, p = c["m"], f"combate.memo{c['m']}"
        dono = C[m - 1]
        dn = int(g(f"{p}.dano")) if num(g(f"{p}.dano")) else 0
        lab = c["lab"]
        out.update({f"{p}.vel": c["vel"] if c["ex"] else "", f"{p}.pvmax": c["pvmax"] if lab else "",
                    f"{p}.pvdepois": "" if not c["ex"] else (max(0, c["pvat"] - dn) if dn >= 0 else
                                                             min(c["pvmax"], c["pvat"] - dn)),
                    f"{p}.defesa": out[f"grupo.pj{m}.memo.def_ef"] if lab else "",
                    f"{p}.nafila": "" if not lab else "Sim" if c["ativo"] else "Não" if not c["ex"] else "Não: caiu"})
        pve, da = g(f"{p}.pv"), g(f"{p}.dano")
        if g(f"{p}.invocado") != "Sim":
            a = ""
        elif not lab:
            a = "Nenhum Memoespírito ligado a este PJ na aba Grupo (G7)"
        elif not dono["ex"]:
            a = "O dono não participa deste combate (C1)"
        elif c["pvat"] == 0:
            a = "A 0 PV ele some: só volta depois do próximo Descanso Curto (11.5)"
        elif num(pve) and pve > c["pvmax"]:
            a = "PV acima do máximo: usando o máximo"
        elif dono["pvat"] == 0:
            a = "Dono a 0 PV: a planilha o mantém na Fila (H27)"
        elif dn < 0 and c["pvat"] - dn > c["pvmax"]:
            a = f"Cura acima do máximo: {tx(c['pvat'] - dn - c['pvmax'])} perdida (23.2)"
        else:
            a = ""
        out[f"{p}.aviso"] = a


def _pjs(E, out, C, grupo_raw):
    g = E.get
    for i in range(1, 7):
        c, pj, p = C[i - 1], grupo_raw[i - 1], f"combate.pj{i}"
        if not c["ex"]:
            for k in ("vel", "pvmax", "pvdepois", "ult", "situacao", "executavel"):
                out[f"{p}.{k}"] = ""
            continue
        dn = int(g(f"{p}.dano")) if num(g(f"{p}.dano")) else 0
        tmp = max(0, g(f"{p}.temp")) if num(g(f"{p}.temp")) else 0
        pvd = max(0, c["pvat"] - max(0, dn - tmp)) if dn >= 0 else min(c["pvmax"], c["pvat"] - dn)
        en = g(f"{p}.energia")
        su, fa = g(f"{p}.suc"), g(f"{p}.fal")
        pres = pj["pres"] if num(pj.get("pres")) else 0
        vant = out.get(f"grupo.pj{i}.morrendo_vant") == "Sim"
        if c["pvat"] > 0:
            sit = "De pé"
        elif num(fa) and fa >= 3:
            sit = "Morre (3 falhas, 23.4)"
        elif num(su) and su >= 3:
            sit = "Estabiliza com 1 PV: digite 1 em PV atual"
        else:
            sit = (f"Morrendo: d20{'+' if pres >= 0 else ''}{pres}, sem Eficiência" + (", com Vantagem" if vant else "")
                   + " contra DT 10. Dano recebido = +1 falha (2 se crítico ou Habilidade de Nível 5+)")
        out.update({f"{p}.vel": c["vel"], f"{p}.pvmax": c["pvmax"], f"{p}.pvdepois": pvd,
                    f"{p}.ult": "Sim" if num(en) and en >= 100 else "Não", f"{p}.situacao": sit,
                    f"{p}.executavel": out.get(f"grupo.pj{i}.executavel") or "Sim"})


def _inimigos(E, out, C, enc, cic):
    g = E.get
    ef = out["campanha.ef"]
    for c in C[6:16]:
        e, k, p = c["e"], c["k"], f"combate.in{c['e']}"
        keys = ["tipo", "ataque", "dano_acerto", "dt", "firmeza", "execucao", "vel", "pvmax", "pvdepois", "fasebarra",
                "defesa", "tenmax", "tenat", "fraquezas", "res", "rd", "quebrado", "danoquebra"] + \
               [f"{x}{j}" for x in ("esp", "disp") for j in (1, 2, 3)]
        if not k:
            for x in keys:
                out[f"{p}.{x}"] = ""
            c["v"], c["res"], c["rd"], c["tenat"], c["quebr"] = [""] * 4, "", "", "", 0
            continue
        w = enc[c["dj"] - 1]["w"] if (not c["troca"] and c["dj"]) else k["f"]
        fases = max(1, k["fases"])
        pva = c["pvat"]
        fb = 3 if fases >= 3 and pva <= k["lim3"] else 2 if fases >= 2 and pva <= k["lim2"] else 1
        fv_ = g(f"{p}.fase")
        fv = clamp(int(fv_), 1, fases) if num(fv_) else 1
        v = k["p3"] if fv == 3 else k["p2"] if fv == 2 else w
        tf = k["ten3"] if fv == 3 else k["ten2"] if fv == 2 else k["ten"]
        tenmax = min(k["ten"], tf)
        red = g(f"{p}.reducao")
        tenat = max(0, tenmax - (max(0, int(red)) if num(red) else 0))
        quebr = 1 if tenat == 0 else 0
        dn = int(g(f"{p}.dano")) if num(g(f"{p}.dano")) else 0
        c.update({"v": list(v), "res": k["res"], "rd": k["rd"], "tenat": tenat, "quebr": quebr})
        out.update({f"{p}.tipo": f"{k['tipo']} · {k['faixa']}", f"{p}.ataque": f"+{k['ataque']}",
                    f"{p}.dano_acerto": f"{k['dano_e']} · média {k['dano_m']}", f"{p}.dt": f"DT {k['dt']} · TR +{k['tr']}",
                    f"{p}.firmeza": k["firmeza"], f"{p}.execucao": k["execucao"], f"{p}.vel": c["vel"],
                    f"{p}.pvmax": c["pvmax"], f"{p}.pvdepois": min(c["pvmax"], max(0, pva - dn)), f"{p}.fasebarra": fb,
                    f"{p}.defesa": k["defesa"] - 2 * quebr, f"{p}.tenmax": tenmax, f"{p}.tenat": tenat,
                    f"{p}.fraquezas": junta(list(v)), f"{p}.res": k["res"] or "—", f"{p}.rd": k["rd"],
                    f"{p}.quebrado": "Sim" if quebr else "Não"})
        EL = tx(g(f"{p}.elemq"))
        if EL in QUEBRA:
            nd, fc, mu = QUEBRA[EL]
            fixo = mu * ef
            med = nd * (fc + 1) // 2 + fixo
            expr = f"{nd}d{fc} + {fixo} · média {med}" if nd > 0 else f"{fixo}"
            sang = min(5 * c["pvmax"] // 100, 3 * ef)
            efe = {"Físico": f" + Sangramento ({sang} por turno, 2 turnos, ignora RD)",
                   "Fogo": f" + Queimadura (2d6 + {ef} por turno, 2 turnos, ignora RD)",
                   "Raio": f" + Choque (1d6 + {ef} por turno, 3 turnos, ignora RD)",
                   "Vento": " + Cisalhamento de Vento (1d6 por acúmulo por turno, até 5, 2 turnos)",
                   "Gelo": " + Congelamento: perde o turno (19.6)" if k["tipo"] == "Comum" else
                   " + Congelamento: Atrasado 2 casas e sem ação especial no turno seguinte (19.6)",
                   "Quântico": " + Embaraço (1d6 por acúmulo, Atrasa 1 casa)",
                   "Imaginário": f" + Aprisionamento (1d6 + {ef}, Atrasa 2 casas)"}[EL]
            out[f"{p}.danoquebra"] = (f"{EL}: {expr} (menos RD {k['rd']} = {max(1, med - k['rd'])}){efe}. Quebrado até o "
                                      f"fim do próximo turno dele: −2 de Defesa e +1 dado; Atrasa 1 casa.")
        else:
            out[f"{p}.danoquebra"] = ""
        for j in (1, 2, 3):
            nm, rc = k["esp"][j - 1] if j <= len(k["esp"]) else ("", "")
            u = g(f"{p}.usada{j}")
            out[f"{p}.esp{j}"] = nm
            out[f"{p}.disp{j}"] = "" if not nm else ("Sim" if not num(u) else "Usada" if not num(rc) else
                                                     "Sim" if cic >= u + rc else f"No Ciclo {tx(u + rc)}")


def _condicoes(E, out, C, conds):
    """C7 (4 por combatente; 0 turnos = expirada, C6 do pedido) e o painel C9b (todas as ativas e o que fazem)."""
    g = E.get
    labs = [c["lab"] for c in C]
    ativas, nexp = [], 0
    for n in range(1, len(conds) + 1):
        rotulo, co, tu, i = conds[n - 1]
        out[f"combate.c{n}.comb"] = rotulo
        quem = tx(g(f"combate.c{n}.quem"))
        lab = C[i]["lab"]
        it = labs.index(quem) if quem and quem in labs else None
        ef = C[it]["ef"] if it is not None else out["campanha.ef"]
        pvm = C[i]["pvmax"] if lab else 0
        if co not in CONDICOES:
            out[f"combate.c{n}.efeito"] = ""
            continue
        expirada = num(tu) and tu == 0
        nexp += 1 if lab and expirada else 0
        nd, fc, pa, se, pct, tef, atr, tac, dc = CONDICOES[co]
        ac = g(f"combate.c{n}.acum")
        acu = min(tac, max(1, int(ac))) if num(ac) else 1
        dados = acu * nd if pa else nd
        if pct > 0:
            s = f"Dano Contínuo: {min(pct * pvm // 100, tef * ef)} por turno"
        elif nd > 0:
            s = (("Dano Contínuo: " if dc else "Dano: ") + f"{dados}d{fc}" + (f" + {ef}" if se else "") +
                 f" · média {dados * (fc + 1) // 2 + (ef if se else 0)}")
        else:
            s = EFEITO_TXT[co]
        if atr:
            s += f"; Atrasa {atr} casa(s): some em Atraso deste Ciclo do alvo (C8)"
        out[f"combate.c{n}.efeito"] = "EXPIRADA (0 turnos): já não vale; apague a condição" if expirada else s
        if lab and C[i]["vivo"] and not expirada:
            efe, dur = TEXTO_21_5[co]
            ativas.append({"quem": rotulo, "cond": co, "turnos": tu if num(tu) else "sem contador",
                           "acum": acu if tac > 1 else "—", "aplicou": quem or "—", "i": i,
                           "efeito": efe + (f" · Agora: {s}" if s != efe else "") + f" (duração: {dur})"})
    tot = len(ativas)
    ncb = len({a["i"] for a in ativas})
    out["combate.painel.resumo"] = (
        ("Nenhuma condição ativa: lance as condições na C7, na linha de cada combatente" if tot == 0 else
         f"{tot} {'condição ativa' if tot == 1 else 'condições ativas'} em {ncb} "
         f"{'combatente' if ncb == 1 else 'combatentes'}. Cada uma está na C7, na linha do combatente") +
        (f". Expirada(s) para apagar na C7: {nexp}" if nexp > 0 else "") + ".")
    for k in range(1, NPAINEL + 1):
        a = ativas[k - 1] if k <= tot else None
        for c in ("quem", "cond", "turnos", "acum", "aplicou", "efeito"):
            out[f"combate.painel{k}.{c}"] = a[c] if a else ""
    out["combate.painel.mais"] = (f"Mais {tot - NPAINEL} {'condição ativa' if tot - NPAINEL == 1 else 'condições ativas'}"
                                  f" além destas {NPAINEL}: veja a C7." if tot > NPAINEL else "")


EFEITO_TXT = {"Congelado": "Só inimigos. Comum perde o turno; Elite e Boss são Atrasados 2 casas e perdem a ação especial",
              "Lentidão": "Ação de Movimento não muda a Distância; só sai do lugar com Esforço Total",
              "Marcado": "+1 em Testes de Ataque de quem marcou",
              "Silenciado": "não pode usar Habilidade de Nível 4 ou maior",
              "Vulnerável": "+1 dado de dano da fonte indicada",
              "Controlado": "quem aplicou decide as ações do alvo, sem Habilidade, Ultimate nem recursos",
              "Corrupção": "+1 no dano de cada Dano Contínuo seu no alvo",
              "Surpreso": "casa pulada no primeiro Ciclo"}                                  # 21.5


def _calc(E, out, C):
    g = lambda k: E.get(f"combate.calc.{k}")  # noqa: E731
    labs = [c["lab"] for c in C[6:16]]
    al, fo, el = tx(g("alvo")), tx(g("fonte")), tx(g("elem"))
    ia = labs.index(al) if al and al in labs else None
    keys = ["situacao", "ndados", "expr", "media_v", "rd_v", "final", "reducao", "tendepois"]
    if ia is None or not C[6 + ia]["ex"] or not fo:
        for k in keys:
            out[f"combate.calc.{k}"] = ""
        return
    c = C[6 + ia]
    sit = "neutro" if not el else ("Fraqueza" if el in c["v"] else "Resistência" if c["res"] == el else "neutro")
    dc = fo == "Dano Contínuo"
    base = max(1, int(g("n"))) if num(g("n")) else 1
    ex = min(3, max(0, int(g("extra")))) if num(g("extra")) else 0
    dados = base if dc else max(1, base * (2 if g("crit") == "Sim" else 1) + (2 if sit == "Fraqueza" else 0) -
                                (2 if sit == "Resistência" else 0)) + ex
    fa = max(2, int(g("f"))) if num(g("f")) else 6
    fx = int(g("fixo")) if num(g("fixo")) else 0
    med = dados * (fa + 1) // 2 + fx
    rd = 0 if dc else c["rd"]
    br = REDUCAO.get(fo, 0)
    red = 0 if br == 0 else br if sit == "Fraqueza" else 1 if sit == "Resistência" else max(1, br // 2)
    ro = g("rolado")
    out.update({"combate.calc.situacao": "Dano Contínuo" if dc else sit, "combate.calc.ndados": dados,
                "combate.calc.expr": f"{dados}d{fa}" + (f" + {fx}" if fx > 0 else f" − {abs(fx)}" if fx < 0 else ""),
                "combate.calc.media_v": med, "combate.calc.rd_v": rd,
                "combate.calc.final": max(1, (ro if num(ro) else med) - rd), "combate.calc.reducao": red,
                "combate.calc.tendepois": max(0, c["tenat"] - red)})
