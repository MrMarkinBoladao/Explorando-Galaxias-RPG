# -*- coding: utf-8 -*-
"""
oraculo_mestre_abas.py — o oráculo das abas Início, Campanha, Grupo, Inimigos e Bestiário.
Entrada: {nome lógico da entrada: valor} (a mesma que a bateria escreve na planilha). Saída: {nome lógico: valor
esperado}. Nenhuma fórmula é lida: as regras estão reimplementadas aqui a partir do livro (seções citadas).
"""
import oraculo_mestre as S
from oraculo_mestre_livro import (FAIXAS, TIPOS, ELEM, ancora, eficiencia, DT, DT_FRAQ, PH_MAX, VERBA, CONE, RELIQ,
                                  RACAS, MORRENDO_VANT, AMBIENTE, bestiario_md, ficha, reescrever, EF_INIMIGO)


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def tx(v):
    return "" if v is None else (str(int(v)) if num(v) and float(v).is_integer() else str(v))


def clamp(v, a, b):
    return min(b, max(a, v))


def campanha(E, out):
    nomes = [tx(E.get(f"grupo.pj{i}.nome")) for i in range(1, 7)]
    npjs = sum(1 for n in nomes if len(n) > 0)
    niv, jog = E.get("campanha.nivel"), E.get("campanha.jogadores")
    nv = clamp(int(niv), 1, 20) if num(niv) else 1
    fi = (nv - 1) // 4 + 1
    je = clamp(int(jog), 1, 6) if num(jog) else max(1, npjs)
    jp = clamp(je, 3, 6)
    deg = 1 if nv <= 8 else 2 if nv <= 16 else 3
    out.update({"campanha.nivel_ef": nv, "campanha.faixa_idx": fi, "campanha.faixa": FAIXAS[fi - 1],
                "campanha.ef": eficiencia(nv), "campanha.jogadores_ef": je, "campanha.jogadores_ph": jp,
                "campanha.ph_degrau": deg, "campanha.ph_max": PH_MAX[jp][deg - 1],
                "campanha.ph_ini": PH_MAX[jp][deg - 1] - 2, "campanha.dt_media": DT["Média"][fi - 1],
                "campanha.dt_dificil": DT["Difícil"][fi - 1], "campanha.dt_fraqueza": DT_FRAQ[fi - 1],
                "campanha.cone": CONE[fi - 1], "campanha.reliquias": RELIQ[fi - 1], "campanha.verba": VERBA[fi - 1],
                "grupo.npjs": npjs})
    s = E.get("inicio.semente")
    out["inicio.semente_ef"] = S.semente_efetiva(s)
    elems = [tx(E.get(f"grupo.pj{i}.elemento")) for i in range(1, 7)]
    for k, e in enumerate(ELEM, start=1):
        out[f"grupo.tem.{k}"] = "Sim" if e in elems else "Não"
    out["grupo.n_elementos"] = sum(1 for e in ELEM if e in elems)
    out["grupo.n_dobro"] = sum(1 for e in ELEM if elems.count(e) > 1)
    for i in range(1, 7):
        r = tx(E.get(f"grupo.pj{i}.raca"))
        ok = r in RACAS
        out[f"grupo.pj{i}.morrendo_vant"] = ("Sim" if r in MORRENDO_VANT else "Não") if ok else ""
        out[f"grupo.pj{i}.executavel"] = ("Não" if r == "Xianzhouíta" else "Sim") if ok else ""
        out[f"grupo.pj{i}.esforco"] = ("Sim" if r == "Humano" else "Não") if ok else ""
        out[f"grupo.pj{i}.descobre"] = ("Com Vantagem, 2 por sucesso" if r == "Intellitron" else "Normal") if ok else ""
    return elems


# ---------------------------------------------------------------------------
# Inimigos (6.7.1–6.7.3, H1, H3, H4, H12)
# ---------------------------------------------------------------------------

MODOS = ["Faixa do livro", "Por nível — Sugestão", "Ajustar do bestiário"]


def pv_h1(tipo, L):
    """H1: só o PV, interpolado entre os níveis de referência 3/7/11/15/19 (29.1)."""
    a = [ancora(fx, tipo)["pv"] for fx in FAIXAS]
    if L <= 3:
        return a[0]
    if L >= 19:
        return a[4]
    k = min(4, max(1, (L - 3) // 4 + 1))
    return (a[k - 1] * 4 + (a[k] - a[k - 1]) * (L - (4 * k - 1))) // 4


def inimigos(E, out, elems):
    camp = out["campanha.nivel_ef"], out["campanha.faixa"]
    sem, rol = out["inicio.semente_ef"], S.rolagem_efetiva(E.get("inimigos.rolagem"))
    tem = [e in elems for e in ELEM]
    linhas, ws_ant = [], []
    for i in range(1, 13):
        g = lambda k: E.get(f"inimigos.{i}.{k}")  # noqa: E731
        nome = tx(g("nome"))
        modo = g("modo") if g("modo") in MODOS else "Faixa do livro"
        base = ficha(g("base")) if g("base") else None
        aj = modo == "Ajustar do bestiário" and base is not None
        tipo = g("tipo") if g("tipo") in TIPOS else (base["tipo"] if aj else "Comum")
        nivel = clamp(int(g("nivel")), 1, 20) if num(g("nivel")) else camp[0]
        if modo == "Por nível — Sugestão":
            fx = FAIXAS[(nivel - 1) // 4]
        else:
            fx = g("faixa") if g("faixa") in FAIXAS else camp[1]
        a = ancora(fx, tipo)
        pv = pv_h1(tipo, nivel) if modo == "Por nível — Sugestão" else a["pv"]
        fv = g("fases")
        fases = 1 if tipo != "Boss" else (int(fv) if num(fv) and 1 <= fv <= 3 else (max(1, base["fases"]) if aj else 1))
        F = [tx(g(f"f{j}")) for j in range(1, 5)]
        vazias = all(len(x) == 0 for x in F)
        res = tx(g("res")) if tx(g("res")) else (base["res"] if aj else "")
        # H12: chave de preferência e a ordem sugerida (G = 110, C = 10·i + e)
        chaves = []
        for e in range(1, 8):
            x = S.valor(sem, 110, rol, 10 * i + e)
            coberto = any(ELEM[e - 1] in w for w in ws_ant)
            pref = 9000000000 if res == ELEM[e - 1] else (0 if tem[e - 1] and not coberto else 2147483647)
            chaves.append((pref + x + e / 10, e))
        sug = [ELEM[e - 1] for _, e in sorted(chaves)]
        w = []
        for j in range(4):
            if not nome:
                w.append("")
            elif not vazias:
                w.append(F[j])
            elif aj:
                w.append(base["fraquezas"][j] if j < len(base["fraquezas"]) else "")
            else:
                w.append(sug[j] if j + 1 <= a["nsug"] else "")
        ws_ant.append(w)
        rac = g("racional")
        execu = "Pode" if rac == "Sim" else "Não" if rac == "Não" else (base["execucao"] if aj else "Não declarado")
        custo = (1.5 if aj and base["nome"] == "Escória de Stellaron" else 1) * pv
        lim2 = (pv // 2 if fases == 2 else (2 * pv) // 3 if fases == 3 else "")
        lim3 = pv // 3 if fases == 3 else ""
        txt = "" if not nome else (w[0] + "".join(", " + x for x in w[1:] if x) +
                                   (" (sugeridas)" if vazias and not aj else " (da base)" if vazias and aj else ""))
        L_ = {"nome": nome, "tipo": tipo, "faixa": fx, "pv": pv, "aj": aj, "base": base, "a": a, "fases": fases,
              "w": w, "res": res, "execucao": execu, "custo": custo, "lim2": lim2, "lim3": lim3, "fraq_txt": txt,
              "fidx": FAIXAS.index(fx) + 1, "ef": EF_INIMIGO[FAIXAS.index(fx)]}
        linhas.append(L_)
        p = f"inimigos.{i}"
        if not nome:
            for k in ("faixa_ef", "pv", "defesa", "rd", "ten", "vel", "dt", "ataque", "tr", "dano", "nfraq", "nafila",
                      "acoes", "custo", "execucao"):
                out[f"{p}.{k}"] = ""
            continue
        out.update({f"{p}.faixa_ef": fx, f"{p}.pv": pv, f"{p}.defesa": a["defesa"], f"{p}.rd": a["rd"],
                    f"{p}.ten": a["ten"], f"{p}.vel": a["vel"], f"{p}.dt": a["dt"], f"{p}.ataque": f"+{a['ataque']}",
                    f"{p}.tr": f"+{a['tr']}", f"{p}.dano": f"{a['dano_e']} · média {a['dano_m']}",
                    f"{p}.nfraq": a["nfraq"], f"{p}.nafila": f"VEL {a['vel']}, {a['firmeza']}",
                    f"{p}.acoes": a["acoes"], f"{p}.custo": custo, f"{p}.execucao": execu})
    _fases_cat(E, linhas)
    _acoes(E, out, linhas)
    _ficha_inimigo(E, out, linhas)
    return linhas


def _fases_cat(E, linhas):
    i5 = {}
    for n in range(1, 25):
        inim, fz = tx(E.get(f"inimigos.fase{n}.inimigo")), E.get(f"inimigos.fase{n}.fase")
        if inim:
            chave = f"{inim}|{tx(fz)}"
            if chave not in i5:
                i5[chave] = n
    for L_ in linhas:
        ten_new = L_["a"]["ten"]
        for f in (2, 3):
            fr, ten = [""] * 4, ""
            if L_["nome"] and L_["fases"] >= f:
                n = i5.get(f"{L_['nome']}|{f}")
                bf = None
                if L_["aj"]:
                    bf = next((x for x in L_["base"]["fases_d"] if x["fase"] == f), None)
                if n:
                    fr = [tx(E.get(f"inimigos.fase{n}.f{j}")) for j in range(1, 5)]
                    t5 = E.get(f"inimigos.fase{n}.ten")
                    ten = min(ten_new, t5) if num(t5) else ten_new
                elif bf:
                    fr = list(bf["fraq"]) + [""] * (4 - len(bf["fraq"]))
                    ten = min(ten_new, bf["ten"] * ten_new // L_["base"]["ten"])
                else:
                    ten = ten_new
            L_[f"p{f}"], L_[f"ten{f}"] = fr, ten


def texto_pronto(E, n, linhas):
    g = lambda k: E.get(f"inimigos.acao{n}.{k}")  # noqa: E731
    inim = tx(g("inimigo"))
    lin = next((L_ for L_ in linhas if L_["nome"] == inim and inim), None)
    nomes_i1 = [tx(E.get(f"inimigos.{i}.nome")) for i in range(1, 13)]
    if not inim or inim not in nomes_i1:
        return ""
    lin = linhas[nomes_i1.index(inim)]
    a = lin["a"]
    tp = g("tipo")
    dano = f"{a['dano_e']} · média {a['dano_m']}" if lin["nome"] else " · média "
    esp = f"{a['esp_e']} · média {a['esp_m']}"
    dt = a["dt"] if lin["nome"] else ""
    el = tx(g("elemento")) or "Físico"
    rec = f" (recarga {tx(g('recarga'))} Ciclos)" if num(g("recarga")) else ""
    D = g("duracao")
    dur = (tx(D) if num(D) else "1") + (" turnos" if num(D) and D > 1 else " turno")
    co, tr = tx(g("condicao")), tx(g("tr"))
    cond = f" e {co} por {dur}" if co else ""
    nome = tx(g("nome")) or "Ação"
    alc = tx(g("alcance")) or "Pessoal"
    teste = f"Teste de {tr} contra DT {dt}"
    qualquer = teste if tr else f"Teste de Resistência contra DT {dt}"
    if tp == "Ataque normal":
        return f"{nome} ({alc}, {el}): {dano}" + (f", e o alvo recebe {co} por {dur}" if co else "")
    if tp == "Especial de dano 1 alvo (até 1,5×)":
        return (f"{nome}{rec}: um alvo a até Distância {alc}" + (f" faz {teste}; se falhar, recebe " if tr else
                " recebe ") + f"{esp} de dano {el}{cond}.")
    if tp == "Especial de dano 2–3 alvos (dano cheio por alvo)":
        return (f"{nome}{rec}: até 3 alvos a até uma Distância um do outro " + (
            f"fazem {teste}. Quem falha recebe {dano} de dano {el}{cond}; quem passa recebe metade do dano." if tr
            else f"recebem, cada um, {dano} de dano {el}{cond}."))
    if tp == "Especial de controle":
        return f"{nome}{rec}: o alvo faz {qualquer}; se falhar, recebe {co or '(escolha a condição)'} por {dur}."
    if tp == "Reação":
        return (f"{nome} (Reação" + (f", recarga {tx(g('recarga'))} Ciclos" if num(g("recarga")) else "") + ")" +
                (f": o alvo faz {qualquer}; se falhar, recebe {co} por {dur}." if co else "."))
    return ""


def _acoes(E, out, linhas):
    """Texto pronto (36 linhas) e as especiais criadas (para C6 do Combate)."""
    cont, esp = {}, {}
    for n in range(1, 37):
        out[f"inimigos.acao{n}.texto"] = t = texto_pronto(E, n, linhas)
        inim, tp = tx(E.get(f"inimigos.acao{n}.inimigo")), tx(E.get(f"inimigos.acao{n}.tipo"))
        if inim and tp:
            cont.setdefault(inim, []).append(t)
            if tp != "Ataque normal":
                esp.setdefault(inim, []).append((tx(E.get(f"inimigos.acao{n}.nome")), E.get(f"inimigos.acao{n}.recarga")))
    for L_ in linhas:
        L_["criadas"] = cont.get(L_["nome"], [])
        if L_["aj"]:
            L_["esp"] = [(nm, rc) for nm, rc in L_["base"]["esp"]]
        else:
            L_["esp"] = [(nm, rc if num(rc) else 0) for nm, rc in esp.get(L_["nome"], [])[:3]]


def _ficha_inimigo(E, out, linhas):
    nomes = [tx(E.get(f"inimigos.{i}.nome")) for i in range(1, 13)]
    ver = tx(E.get("inimigos.ver"))
    keys = ["l2", "l3"] + [f"acao{k}" for k in range(1, 13)] + ["fase1", "fase2", "fase3"]
    if not ver or ver not in nomes:
        for k in keys:
            out[f"inimigos.ficha.{k}"] = ""
        return
    L_ = linhas[nomes.index(ver)]
    a = L_["a"]
    if not L_["nome"]:
        return
    out["inimigos.ficha.l2"] = (f"PV {tx(L_['pv'])}   Defesa {a['defesa']}   RD {a['rd']}   Tenacidade {a['ten']}   "
                                f"VEL {a['vel']}")
    out["inimigos.ficha.l3"] = (f"Ataque +{a['ataque']}    DT dos efeitos {a['dt']}    Teste de Resistência +{a['tr']}"
                                f"    Dano por acerto {a['dano_e']} · média {a['dano_m']}")
    for k in range(1, 13):
        if L_["aj"]:
            b = L_["base"]["acoes"]
            t = reescrever(b[k - 1]["texto"], L_["base"], L_["faixa"], L_["tipo"], L_["pv"]) if k <= len(b) else ""
        else:
            t = L_["criadas"][k - 1] if k <= len(L_["criadas"]) else ""
        out[f"inimigos.ficha.acao{k}"] = t
    nf = L_["fases"]
    for f in (1, 2, 3):
        if nf >= f and nf > 1:
            if f == 1:
                topo, piso, fq, ten = L_["pv"], L_["lim2"] + 1 if nf >= 2 else 0, L_["fraq_txt"], a["ten"]
            else:
                pf = L_[f"p{f}"]
                fq = pf[0] + "".join(", " + x for x in pf[1:] if x)
                topo, ten = L_[f"lim{f}"], L_[f"ten{f}"]
                piso = (L_["lim3"] + 1 if nf > 2 else 0) if f == 2 else 0
            out[f"inimigos.ficha.fase{f}"] = (f"Fase {f} ({tx(topo)} a {tx(piso)} PV): Fraquezas {fq}; Tenacidade "
                                              f"{tx(ten)} (volta ao máximo na virada)")
        else:
            out[f"inimigos.ficha.fase{f}"] = ""


# ---------------------------------------------------------------------------
# Bestiário (6.8)
# ---------------------------------------------------------------------------

def bestiario(E, out):
    g = lambda k: tx(E.get(f"bestiario.filtro.{k}"))  # noqa: E731
    fichas = bestiario_md()
    ordem = []
    for i, f in enumerate(fichas, start=1):
        amb = g("ambiente")
        ok_amb = (not amb or amb == "Todos" or any(a == amb and (fc == f["faccao"] or (f["origem2"] and fc == f["origem2"]))
                                                    for fc, a in AMBIENTE))
        passa = ((not g("faixa") or g("faixa") == "Todas" or g("faixa") == f["faixa"]) and
                 (not g("tipo") or g("tipo") == "Todos" or g("tipo") == f["tipo"]) and
                 (not g("elemento") or g("elemento") == "Qualquer" or g("elemento") in f["fraquezas"]) and
                 (not g("faccao") or g("faccao") == "Todas" or g("faccao") == f["faccao"]) and ok_amb and
                 (g("resistencia") != "Sim" or bool(f["res"])) and (g("fases") != "Sim" or f["fases"] > 1))
        if passa:
            ordem.append((FAIXAS.index(f["faixa"]) * 1000 + 1000 + (TIPOS.index(f["tipo"]) + 1) * 100 + i, f))
    ordem.sort(key=lambda t: t[0])
    for k in range(1, 33):
        f = ordem[k - 1][1] if k <= len(ordem) else None
        a = ancora(f["faixa"], f["tipo"]) if f else None
        v1 = dict(zip("ABCDEFGHIJ", [f["nome"], f["tipo"], f["faixa"], f["faccao"], f["pv"], a["defesa"], a["rd"],
                                     a["ten"], a["vel"], f"+{a['ataque']}"])) if f else {c: "" for c in "ABCDEFGHIJ"}
        for c, v in v1.items():
            out[f"bestiario.b1.{k}.{c}"] = v
        v2 = {"B": f"{a['dano_e']} · média {a['dano_m']}", "D": f"DT {a['dt']} · TR +{a['tr']}",
              "F": ", ".join(f["fraquezas"]), "H": f["res"] or "—", "I": f["fases"], "J": f["execucao"]} if f else \
            {c: "" for c in "BDFHIJ"}
        for c, v in v2.items():
            out[f"bestiario.b2.{k}.{c}"] = v
    out["bestiario.resultado"] = f"{len(ordem)} de 32 fichas"
    f = ficha(E.get("bestiario.ver")) if E.get("bestiario.ver") else None
    keys = ["l3", "l4", "l5", "nafila"] + [f"acao{k}" for k in range(1, 13)] + ["fase1", "fase2", "fase3"]
    if not f:
        for k in keys:
            out[f"bestiario.ficha.{k}"] = ""
        return
    a = ancora(f["faixa"], f["tipo"])
    out["bestiario.ficha.l3"] = f"PV {f['pv']}   Defesa {a['defesa']}   RD {a['rd']}   Tenacidade {a['ten']}   VEL {a['vel']}"
    out["bestiario.ficha.l4"] = f"Ataque +{a['ataque']}    DT dos efeitos {a['dt']}    Teste de Resistência +{a['tr']}"
    out["bestiario.ficha.l5"] = f"Fraquezas: {', '.join(f['fraquezas'])}    Resistências: {f['res'] or '—'}"
    out["bestiario.ficha.nafila"] = f"Na Fila: {f['nafila']}"
    for k in range(1, 13):
        out[f"bestiario.ficha.acao{k}"] = f["acoes"][k - 1]["texto"] if k <= len(f["acoes"]) else ""
    for fz in (1, 2, 3):
        d = next((x for x in f["fases_d"] if x["fase"] == fz), None)
        out[f"bestiario.ficha.fase{fz}"] = (f"Fase {fz} — {d['nome']} ({d['topo']} a {d['piso']} PV): Fraquezas "
                                            f"{', '.join(d['fraq'])}; Tenacidade {d['ten']}; {d['ritmo']}") if d else ""


def catalogo(linhas):
    """As 44 entradas (12 da campanha + 32 do bestiário) que alimentam Encontros e Combate."""
    cat = []
    for L_ in linhas:
        a = L_["a"]
        cat.append({"nome": L_["nome"], "tipo": L_["tipo"], "faixa": L_["faixa"], "pv": L_["pv"], "ten": a["ten"],
                    "defesa": a["defesa"], "rd": a["rd"], "vel": a["vel"], "ataque": a["ataque"], "dano_e": a["dano_e"],
                    "dano_m": a["dano_m"], "dt": a["dt"], "tr": a["tr"], "f": L_["w"], "res": L_["res"],
                    "execucao": L_["execucao"], "fases": L_["fases"], "acoes": a["acoes"], "custo": L_["custo"],
                    "firmeza": a["firmeza"], "lim2": L_["lim2"], "lim3": L_["lim3"], "p2": L_["p2"], "p3": L_["p3"],
                    "ten2": L_["ten2"], "ten3": L_["ten3"], "esp": L_["esp"], "ef": L_["ef"], "fidx": L_["fidx"],
                    "campanha": True})
    for f in bestiario_md():
        a = ancora(f["faixa"], f["tipo"])
        fd = {x["fase"]: x for x in f["fases_d"]}
        fr = f["fraquezas"] + [""] * (4 - len(f["fraquezas"]))
        cat.append({"nome": f["nome"], "tipo": f["tipo"], "faixa": f["faixa"], "pv": f["pv"], "ten": a["ten"],
                    "defesa": a["defesa"], "rd": a["rd"], "vel": a["vel"], "ataque": a["ataque"], "dano_e": a["dano_e"],
                    "dano_m": a["dano_m"], "dt": a["dt"], "tr": a["tr"], "f": fr, "res": f["res"],
                    "execucao": f["execucao"], "fases": f["fases"], "acoes": a["acoes"], "custo": f["custo"],
                    "firmeza": a["firmeza"], "lim2": f["lim2"], "lim3": f["lim3"],
                    "p2": fd[2]["fraq"] if 2 in fd else [""] * 4, "p3": fd[3]["fraq"] if 3 in fd else [""] * 4,
                    "ten2": fd[2]["ten"] if 2 in fd else "", "ten3": fd[3]["ten"] if 3 in fd else "",
                    "esp": f["esp"], "ef": EF_INIMIGO[FAIXAS.index(f["faixa"])], "fidx": FAIXAS.index(f["faixa"]) + 1,
                    "campanha": False})
    return cat


def achar(cat, nome):
    if not nome:
        return None
    for k, c in enumerate(cat):
        if c["nome"] == nome:
            return k
    return None
