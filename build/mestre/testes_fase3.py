# -*- coding: utf-8 -*-
"""Suítes e casos da Fase 3 (Campanha, Grupo, Sessões, Missões, Mundos, Improviso, Escudo, Minhas Tabelas — R8–R11,
R13; design §6.1–6.5, §6.13–6.17).

  dados_fase3          parser PRÓPRIO do teste (lê o .md) × aba Dados para os blocos novos (27.3, 27.9, 17.2, 19.4,
                       19.7, 20.2, 20.3, 23.3, 23.4, 23.6, 26.1, 27.10, 27.16, 27.17, 28.2, 29.12, loja de 24.1–24.3) e
                       cada trecho de regra do bloco 'textos' achado na seção citada; e cada célula do Escudo do Mestre
                       igual à aba Dados (MAPA["escudo"])
  ouro_fase3           números do livro calculados NA planilha: 27.9 nível a nível, 23.6, 23.3, 27.2 (DT rápida, 30
                       casos), 26.1, 26.7, preços da loja (24.1–24.3), H16 (45 casos), H17 (7 rótulos), H23 (3 × 4)
  casos_oraculo        oráculo × planilha: G = 510…650 e 701…710 em 300 Rolagens nº × 3 sementes, estados de campanha
  validar_heuristicas  H10, H15, H16, H25, Minhas Tabelas sem repetir, toda entrada de toda lista alcançável (d)
  lint_fase3 / texto_fase3   Escudo em A4 paisagem com as quebras e a altura das páginas; nenhum "Em construção";
                       H24: cada item da Sessão Zero cita uma seção que existe e tem a palavra-chave
"""

import random
import re

import testar_ficha as TF
import oraculo_mestre as O
import oraculo_mestre_hist as OH
import oraculo_mestre_ger as OG
import oraculo_mestre_camp as OC
import oraculo_mestre_livro as L
from mestre import nucleo as N
from mestre import testes_comum as TC
from mestre.testes_hist import _tab, _secao, _n, _bloco

Resultado = TF.Resultado
PESO = 9


def _md_linhas(cap, sec):
    return [L.limpo(re.sub(r"^\s*(>\s*)+", "", l)) for l in _secao(cap, sec)]


def livro_fase3():
    """O que o .md diz (parser do teste) para os blocos novos da aba Dados."""
    d = {}
    _, c = _tab("27", "## 27.3", "Teste")
    d["dt_subsistema"] = [(x[0], x[1], x[2]) for x in c]
    _, c = _tab("27", "### Aprovar uma Ultimate", "Faixa")
    d["ultimate_faixa"] = []
    for x in c:
        a, b = re.fullmatch(r"(\S+) \((\d+)\)", x[2]).groups(), re.fullmatch(r"(\S+) \((\d+)\)", x[3]).groups()
        d["ultimate_faixa"].append((x[0], int(x[1]), a[0], int(a[1]), b[0], int(b[1])))
    _, c = _tab("17", "## 17.2", "Fonte")
    d["energia"] = [tuple(x[:3]) for x in c]
    _, c = _tab("19", "## 19.4", "Tipo de alvo")
    d["teto_atraso"] = [tuple(x[:3]) for x in c]
    _, c = _tab("19", "## 19.7", "Situação")
    d["casos_fila"] = [tuple(x[:2]) for x in c]
    _, c = _tab("20", "## 20.2", "Situação")
    d["fraqueza_resistencia"] = [tuple(x[:3]) for x in c]
    _, c = _tab("20", "## 20.3", "Fonte")
    d["tenacidade_livro"] = [tuple(x[:2]) for x in c]
    _, c = _tab("23", "## 23.4", "Resultado")
    d["morrendo"] = [tuple(x[:2]) for x in c]
    _, c = _tab("23", "## 23.6", "Tipo")
    d["descanso"] = [tuple(x[:4]) for x in c]
    cab, c = _tab("23", "## 23.6", "Nível")
    d["descanso_curto"] = [(int(a), int(b)) for a, b in zip(cab[1:], c[0][1:])]
    cab, c = _tab("23", "## 23.3", "Nível")
    d["pv_temp"] = [(a, int(a.split("-")[0]), int(a.split("-")[1]), int(b)) for a, b in zip(cab[1:], c[0][1:])]
    _, c = _tab("27", "## 27.10", "Operação")
    d["casos_mesa"] = [tuple(x[:3]) for x in c]
    _, c = _tab("28", "## 28.2", "Tipo")
    d["acoes_tipo"] = [tuple(x[:3]) for x in c]
    t = next(l for l in _md_linhas("29", "## 29.12") if l.startswith("Tetos que a mesa esquece:"))
    d["tetos"] = [(x.strip().rstrip("."),) for x in t.split(":", 1)[1].split("·")]
    t = " ".join(_md_linhas("26", "## 26.1"))
    m = re.search(r"(\d+) a (\d+) sessões por nível nos níveis 1 a (\d+); (\d+) a (\d+) sessões por nível", t)
    a, b, ate, c2, d2 = (int(v) for v in m.groups())
    d["ritmo"] = [(1, ate, a, b, f"{a} a {b} sessões por nível (níveis 1 a {ate})"),
                  (ate + 1, 20, c2, d2, f"{c2} a {d2} sessões por nível (do nível {ate + 1} em diante)")]
    fac, atual = [], None
    for l in _secao("27", "## 27.16"):
        if l.startswith("### "):
            atual = l[4:].strip()
        t = L.limpo(l)
        if t.startswith("Como usar:"):
            fac.append((atual, t[len("Como usar:"):].strip()))
    d["faccoes_uso"] = fac
    _, c = _tab("27", "## 27.17", "Lugar")
    d["locais_livro"] = [tuple(x[:3]) for x in c]
    return d


# o teste guarda a sua própria cópia de H15 (que linha do livro cabe em cada loja) e dos exemplos de 24.2
LOJA_H15 = {"Armas": ("armas", ["Munição ou célula de reserva"]),
            "Armaduras": ("armaduras", ["Kit de ferramentas", "Traje de vedação", "Munição ou célula de reserva"]),
            "Suprimentos": ("itens", []),
            "Farmácia": ("pocoes", ["Kit de primeiros socorros (3 usos)", "Kit de pesquisa de campo",
                                    "Ração de viagem (3 dias)"]),
            "Mercado geral": ("tudo", []), "Mercado da Frota de Jade": ("tudo", [])}


def _loja_livro():
    from mestre.testes_hist import livro_fase2
    lv = livro_fase2()
    ex = {}
    for l in _secao("24", "## 24.2"):
        cs = L._cels(l) if l.startswith("|") else []
        if len(cs) == 2 and cs[0] in ("Leve", "Média", "Pesada", "Disparo curto", "Disparo longo", "Energia") and \
                not cs[1].startswith("1d") and "," in cs[1]:
            ex[cs[0]] = cs[1]
    armas = [(f"Arma {c}", pr, f"{dd}, {al}, {at}; ex.: {ex[c]}", e) for c, dd, al, at, e, pr in lv["armas"]]
    armad = [(f"Armadura {t}", pr, f"Defesa +{df}" + ("" if o == "—" else f"; {o}"), e)
             for t, df, o, _, e, pr in lv["armaduras"]]
    poc = [(f"Poção {nm}", pr, f"Cura {cu}", e) for nm, cu, e, pr in lv["pocoes"]]
    itens = [(nm, pr, uso, e) for nm, e, pr, uso in lv["itens"]]
    por = {x[0]: x for x in armas + armad + poc + itens}
    base = {"armas": armas, "armaduras": armad, "itens": itens, "pocoes": poc, "tudo": armas + armad + poc + itens}
    return {t: base[b] + [por[n] for n in extra] for t, (b, extra) in LOJA_H15.items()}, ex


def dados_fase3(r, wb):
    """Parser do teste × aba Dados (blocos novos) e Escudo do Mestre × aba Dados."""
    n0 = r.checagens
    lv = livro_fase3()
    for id_, linhas in lv.items():
        rows = _bloco(wb, id_)
        cols = list(TC.mapa()["blocos"][f"dados.{id_}"]["colunas"])
        r.ok(len(rows) == len(linhas), f"{id_}: {len(rows)} linhas na aba Dados, {len(linhas)} no livro")
        for k, (row, esp) in enumerate(zip(rows, linhas), start=1):
            got = tuple(row[c] for c in cols[:len(esp)])
            r.ok(all(TF._igual(a, b) or str(a) == str(b) for a, b in zip(got, esp)),
                 f"{id_} linha {k}: aba Dados={got!r} livro={esp!r}")
    # trechos de regra (bloco 'textos'): cada um está, inteiro, numa linha da seção citada
    secoes = {"19.3": ("19", "## 19.3"), "19.4": ("19", "## 19.4"), "19.5": ("19", "## 19.5"), "19.6": ("19", "## 19.6"),
              "20.3": ("20", "## 20.3"), "20.4": ("20", "## 20.4"), "20.6": ("20", "## 20.6"), "27.5": ("27", "## 27.5"),
              "28.4": ("28", "## 28.4"), "23.4": ("23", "## 23.4"), "23.5": ("23", "## 23.5"), "23.3": ("23", "## 23.3"),
              "16.2": ("16", "## 16.2"), "17.2": ("17", "## 17.2"), "27.9": ("27", "### Aprovar uma Ultimate"),
              "29.12": ("29", "## 29.12"), "27.1": ("27", "## 27.1"), "27.17": ("27", "## 27.17"),
              "27.15": ("27", "## 27.15"), "24.5": ("24", "## 24.5"), "03": ("03", "## Antes de jogar"),
              "26.1": ("26", "## 26.1"), "27.8": ("27", "## 27.8"), "27.2": ("27", "## 27.2")}
    for row in _bloco(wb, "textos"):
        cap, sec = secoes[str(row["Seção"])]
        lin = _md_linhas(cap, sec)
        t = row["Texto"]
        r.ok(any(t in re.sub(r"^(- |\d+\. )", "", x) for x in lin), f"textos {row['Chave']}: trecho fora de {sec}: {t[:80]!r}")
    # loja (24.1–24.3 e H15): cada item, preço e descrição iguais ao livro; o estoque de cada tipo é o do H15
    pools, _ = _loja_livro()
    lj = _bloco(wb, "loja")
    for t, pool in pools.items():
        got = [(x["Item"], x["Preço (Cr)"], x["O que é"], x["Espaço"]) for x in lj if x["Tipo de loja"] == t]
        r.ok(got == pool, f"loja {t}: aba Dados ≠ livro ({got[:2]} × {pool[:2]})")
        r.ok(len(pool) >= 6, f"H15: a loja {t} tem só {len(pool)} itens (estoque de 6 sem repetir)")
        r.ok([x for x in OG.LOJA[t]] == [p[:3] for p in pool], f"loja {t}: oráculo ≠ livro")
    for row in _bloco(wb, "loja_tipos"):
        r.ok(row["Nº de itens"] == len(pools[row["Tipo de loja"]]), f"loja_tipos {row['Tipo de loja']}")
    # transcrições do oráculo × livro (o oráculo não lê o .md em tempo de execução)
    r.ok([(f, n, dm, cm) for f, n, _, dm, _, cm in lv["ultimate_faixa"]] ==
         [(f, *OG.ULTIMATE[f]) for f in L.FAIXAS], "oráculo 27.9 ≠ livro")
    r.ok({k: v for k, v in OC.DT27.items()} == {x[0]: tuple(x[1:]) for x in _dt27()}, "oráculo 27.2 ≠ livro")
    r.ok([x[4] for x in lv["ritmo"]] == [t for _, _, t in OC.RITMO] and
         [x[3] for x in lv["ritmo"]] == [m for _, m, _ in OC.RITMO], "oráculo 26.1 ≠ livro")
    _, c = _tab("06", "## 6.3", "Caminho")
    r.ok([x[0] for x in c] == OG.CAMINHOS, f"oráculo 06.3 (ordem dos Caminhos) ≠ livro: {[x[0] for x in c]}")
    _escudo_x_dados(r, wb)
    r.info(f"Fase 3: {r.checagens - n0} checagens (blocos 27.3, 27.9, 17.2, 19.4, 19.7, 20.2, 20.3, 23.3, 23.4, 23.6, "
           f"26.1, 27.10, 27.16, 27.17, 28.2, 29.12; {len(_bloco(wb, 'textos'))} trechos de regra; loja de 24.1–24.3; "
           f"Escudo × Dados)")


def _dt27():
    _, c = _tab("27", "## 27.2", "Dificuldade")
    return [(x[0], *[int(v) for v in x[1:6]]) for x in c]


def _escudo_x_dados(r, wb):
    """Toda célula do Escudo do Mestre é a(s) célula(s) da aba Dados que o mapa diz, no formato dito."""
    esc = TC.mapa()["escudo"]
    cel = TC.mapa()["celulas"]
    nomes = sorted(esc["celulas"])
    sol = TC.modelo().calcular({}, [cel[n] for n in nomes])
    blocos = {}
    for n in nomes:
        spec = esc["celulas"][n]
        vals = []
        for bloco, col, i in spec["partes"]:
            if bloco not in blocos:
                blocos[bloco] = _bloco(wb, bloco)
            vals.append(blocos[bloco][i - 1][col])
        esp = vals[0] if spec["formato"] == "{0}" else spec["formato"].format(*[O_tx(v) for v in vals])
        got = sol.get(cel[n])
        r.ok(TF._igual(got, esp), f"Escudo {n}: planilha={got!r} aba Dados={esp!r}")
    r.info(f"Escudo do Mestre: {len(nomes)} células lidas da aba Dados conferidas; páginas {esc['paginas']}")


def O_tx(v):
    return str(int(v)) if isinstance(v, float) and v.is_integer() else str(v)


# ---------------------------------------------------------------------------
# ouro — números do livro calculados NA planilha
# ---------------------------------------------------------------------------

def ouro_fase3(r):
    from mestre.testes_regras import planilha
    lv = livro_fase3()
    # 27.9: a Ultimate no Nível equivalente da faixa do grupo, nível a nível (adiado da Fase 2, item 2.4)
    ult = {x[0]: x for x in lv["ultimate_faixa"]}
    pvt = lv["pv_temp"]
    dcur = dict(lv["descanso_curto"])
    for n in range(1, 21):
        fx = L.FAIXAS[(n - 1) // 4]
        got = planilha({"campanha.nivel": n}, ["escudo.grupo.ult_nivel", "escudo.grupo.ult_dano", "escudo.grupo.ult_cura",
                                               "escudo.grupo.descanso", "escudo.grupo.pv_temp"])
        _, niv, _, dm, _, cm = ult[fx]
        teto = next(t for _, a, b, t in pvt if a <= n <= b)
        r.ok((got["escudo.grupo.ult_nivel"], got["escudo.grupo.ult_dano"], got["escudo.grupo.ult_cura"]) == (niv, dm, cm),
             f"27.9 nível {n}: {got}")
        r.ok(got["escudo.grupo.pv_temp"] == teto, f"23.3 teto de PV temporários no nível {n}: {got} (livro {teto})")
        if n in dcur:     # 23.6: PV por Descanso Curto com Vigor +2
            r.ok(got["escudo.grupo.descanso"] == dcur[n], f"23.6 Descanso Curto no nível {n}: {got} (livro {dcur[n]})")
    # 27.2: DT rápida e DT das cenas — as 6 dificuldades × 5 faixas do desafio
    for dif, *dts in _dt27():
        for k, fx in enumerate(L.FAIXAS):
            got = planilha({"improviso.dt.dificuldade": dif, "improviso.dt.faixa": fx, "sessoes.cena.1.dificuldade": dif,
                            "sessoes.cena.1.faixa": fx}, ["improviso.dt.valor", "sessoes.cena.1.dt"])
            r.ok(got["improviso.dt.valor"] == dts[k] == got["sessoes.cena.1.dt"], f"27.2 {dif} {fx}: {got}")
    # 27.2 regra 1: faixa do desafio vazia = a do grupo (nível 11 → 9-12: Média 19)
    got = planilha({"campanha.nivel": 11, "improviso.dt.dificuldade": "Média"}, ["improviso.dt.valor"])
    r.ok(got["improviso.dt.valor"] == 19, f"27.2 exemplo de leitura (nível 11, Média 9-12 = 19): {got}")
    # 26.1 ritmo e 26.7 próxima Ressonância
    for n, esp in ((8, lv["ritmo"][0][4]), (9, lv["ritmo"][1][4])):
        got = planilha({"campanha.nivel": n}, ["campanha.ritmo"])["campanha.ritmo"]
        r.ok(got == f"Ritmo sugerido: {esp} (26.1).", f"26.1 nível {n}: {got!r}")
    _, c = _tab("26", "## 26.7", "Ressonância")
    res = [(x[0], int(_n(x[1]))) for x in c]
    for n in (1, 4, 5, 9, 10, 14, 15, 19, 20):
        prox = next(((nm, lv_) for nm, lv_ in res if lv_ > n), None)
        esp = f"Ressonância {prox[0]} no nível {prox[1]}" if prox else "Todas (nível 20)"
        got = planilha({"campanha.nivel": n}, ["campanha.prox_ress"])["campanha.prox_ress"]
        r.ok(got == esp, f"26.7 próxima Ressonância no nível {n}: {got!r} (esperado {esp!r})")
    # 24.1–24.3: na loja, todo preço é o do livro (6 tipos × 4 rolagens)
    pools, _ = _loja_livro()
    preco = {x[0]: x[1] for p in pools.values() for x in p}
    for t in pools:
        for rol in (1, 2, 3, 4):
            nomes = [f"improviso.loja.{k}.{c}" for k in range(1, 7) for c in ("item", "preco")]
            got = planilha({"improviso.loja.tipo": t, "improviso.r620": rol}, nomes)
            itens = [got[f"improviso.loja.{k}.item"] for k in range(1, 7)]
            r.ok(all(got[f"improviso.loja.{k}.preco"] == preco.get(itens[k - 1]) for k in range(1, 7)) and
                 all(i in [x[0] for x in pools[t]] for i in itens) and len(set(itens)) == 6,
                 f"24.1–24.3 / H15 loja {t} rolagem {rol}: {got}")
    _ouro_h16_h17_h23(r, planilha)
    r.info("Fase 3: 27.9 (Ultimate por faixa, adiado da Fase 2), 23.3, 23.6, 27.2 (30 casos e o exemplo de leitura), "
           "26.1, 26.7, preços da loja (24.1–24.3), H16 (45 casos), H17 (7 rótulos), H23 (3 e 4 Ativas) na planilha")


def _ouro_h16_h17_h23(r, planilha):
    # H16: todo par segmentos × preenchidos (45 casos), 10 relógios por cálculo
    casos = [(s, n) for s in (4, 6, 8, 10, 12) for n in range(0, s + 1)]
    r.ok(len(casos) == 45, "H16: 45 casos")
    for k in range(0, len(casos), 10):
        E, esp = {}, {}
        for i, (s, n) in enumerate(casos[k:k + 10], start=1):
            E.update({f"campanha.rel.{i}.nome": f"R{i}", f"campanha.rel.{i}.seg": s, f"campanha.rel.{i}.n": n})
            esp[i] = ("●" * n + "○" * (s - n) + f" {n}/{s}", "Cheio — aconteceu" if n == s else "Falta 1" if n == s - 1
                      else "")
        nomes = [f"campanha.rel.{i}.{c}" for i in esp for c in ("barra", "situacao", "aviso")] + ["inicio.painel.relogios"]
        got = planilha(E, nomes)
        for i, (b, s_) in esp.items():
            r.ok((got[f"campanha.rel.{i}.barra"], got[f"campanha.rel.{i}.situacao"], got[f"campanha.rel.{i}.aviso"]) ==
                 (b, s_, ""), f"H16 {casos[k + i - 1]}: {got}")
        r.ok(got["inicio.painel.relogios"] == sum(1 for _, s_ in esp.values() if s_ == "Falta 1"),
             f"H16 painel da Início: {got['inicio.painel.relogios']}")
    # inválidos: n > s, n < 0, n não inteiro, s fora da lista, n sem s — aviso e nenhum erro
    E = {"campanha.rel.1.seg": 4, "campanha.rel.1.n": 5, "campanha.rel.2.seg": 6, "campanha.rel.2.n": -1,
         "campanha.rel.3.seg": 8, "campanha.rel.3.n": 2.5, "campanha.rel.4.seg": 5, "campanha.rel.4.n": 1,
         "campanha.rel.5.nome": "Sem segmentos", "campanha.rel.6.seg": 6, "campanha.rel.6.n": "três"}
    got = planilha(E, [f"campanha.rel.{i}.{c}" for i in range(1, 7) for c in ("aviso", "barra")])
    esp = ["Preenchidos acima dos segmentos: confira (H16)", "Preenchidos fora de 0 a 6 (H16)",
           "Preenchidos fora de 0 a 8 (H16)", "Segmentos fora de 4, 6, 8, 10 ou 12 (H16)",
           "Escolha os segmentos: 4, 6, 8, 10 ou 12 (H16)", "Preenchidos não é número (H16)"]
    for i, a in enumerate(esp, start=1):
        r.ok(got[f"campanha.rel.{i}.aviso"] == a and got[f"campanha.rel.{i}.barra"] == "", f"H16 inválido {i}: {got}")
    # H17: os 7 rótulos, vazio, fora da faixa, não inteiro, facção repetida
    rot = {-3: "−3 Inimiga declarada", -2: "−2 Hostil", -1: "−1 Desconfiada", 0: "0 Neutra", 1: "+1 Simpática",
           2: "+2 Amiga", 3: "+3 Aliada"}
    E = {f"campanha.fac.{i}.nome": f"Facção {i}" for i in range(1, 12)}
    E.update({f"campanha.fac.{i}.atitude": v for i, v in enumerate(range(-3, 4), start=1)})
    E.update({"campanha.fac.9.atitude": 4, "campanha.fac.10.atitude": 1.5, "campanha.fac.11.nome": "Facção 1"})
    got = planilha(E, [f"campanha.fac.{i}.{c}" for i in range(1, 12) for c in ("leitura", "aviso")])
    for i, v in enumerate(range(-3, 4), start=1):
        r.ok((got[f"campanha.fac.{i}.leitura"], got[f"campanha.fac.{i}.aviso"]) ==
             (rot[v], "Facção repetida: use uma linha por facção (H17)" if i == 1 else ""), f"H17 {v}: {got}")
    r.ok(got["campanha.fac.8.leitura"] == "" and got["campanha.fac.8.aviso"] == "", "H17 vazio")
    for i in (9, 10):
        r.ok(got[f"campanha.fac.{i}.leitura"] == "" and got[f"campanha.fac.{i}.aviso"] == "Atitude fora de −3 a +3 (H17)",
             f"H17 fora da faixa / não inteiro {i}: {got}")
    r.ok(got["campanha.fac.11.aviso"] == "Facção repetida: use uma linha por facção (H17)", "H17 facção repetida")
    # H23: com 3 Ativas, nenhum aviso; com 4, o aviso rotulado
    for n_at, esp in ((3, ""), (4, "Mais de 3 missões Ativas: o grupo pode perder o fio — Sugestão da planilha (H23)")):
        E = {f"missoes.{i}.missao": f"M{i}" for i in range(1, 6)}
        E.update({f"missoes.{i}.estado": "Ativa" for i in range(1, n_at + 1)})
        E["missoes.5.estado"] = "Oferecida"
        got = planilha(E, ["missoes.aviso.ativas", "missoes.n.ativa", "inicio.painel.missoes"])
        r.ok(got["missoes.aviso.ativas"] == esp and got["missoes.n.ativa"] == n_at, f"H23 com {n_at} Ativas: {got}")


# ---------------------------------------------------------------------------
# oráculo — casos da Fase 3 (calculados em paralelo com os da Fase 1 e 2)
# ---------------------------------------------------------------------------

PREF_GER = ["mundos.", "improviso.", "minhas.", "escudo.grupo"]
PREF_CAMP = ["campanha.", "grupo.", "sessoes.", "missoes.", "inicio.painel"]
ROLAGENS = [f"mundos.r{g}" for g in (510, 520, 530, 540, 550, 560)] + \
           [f"improviso.r{g}" for g in (600, 610, 620, 630, 640, 650)] + [f"minhas.{t}.rolagem" for t in range(1, 11)]


def _minhas(rng, E):
    """Minhas Tabelas com listas de tamanhos variados (vagas vazias no meio) e 'quantos' de 1 a 5 (e inválidos)."""
    for t in rng.sample(range(1, 11), rng.randint(1, 4)):
        n = rng.choice([0, 1, 2, 3, 5, 7, 11, 13, 30, 77, 100])
        vagas = sorted(rng.sample(range(1, 101), n))
        for k, v in enumerate(vagas):
            E[f"minhas.{t}.vaga{v}"] = f"Entrada {t}.{k + 1}"
        E[f"minhas.{t}.quantos"] = rng.choice([None, 1, 2, 3, 4, 5, 0, 6, 2.5, "três"])
        if rng.random() < 0.5:
            E[f"minhas.{t}.nome"] = f"Tabela do Mestre {t}"


def _rolador(rng, E):
    for e in range(1, 4):
        if rng.random() < 0.8:
            E[f"improviso.rol.{e}.n"] = rng.choice([1, 1, 2, 3, 6, 10, 20, 0, 21, 2.5, "dois"])
        if rng.random() < 0.7:
            E[f"improviso.rol.{e}.f"] = rng.choice([2, 4, 6, 8, 10, 12, 20, 100, 7, "d6"])
        if rng.random() < 0.5:
            E[f"improviso.rol.{e}.m"] = rng.choice([-50, -3, 0, 2, 50, 51, -60, 1.5])
        if rng.random() < 0.4:
            E[f"improviso.rol.{e}.v"] = rng.choice(["Normal", "Vantagem", "Desvantagem", "Sorte"])


def casos_oraculo(r, rng, _t):
    import mestre_dados3 as D3
    for s in (1, 2026, 2147483646):
        for R in range(1, 301):
            E = {"inicio.semente": s, **{k: R for k in ROLAGENS}}
            if rng.random() < 0.6:
                E["campanha.nivel"] = rng.randint(1, 20)
            par = {"mundos.nomes.cultura": [None, "Sortear"] + L.RACAS,
                   "improviso.evento.onde": [None, "Sortear", "Viagem", "Espaço", "Cidade"],
                   "improviso.loja.tipo": [None, "Sortear"] + D3.TIPOS_LOJA,
                   "improviso.oraculo.prob": [None] + [p for p, _ in D3.ORACULO_PROB],
                   "improviso.dt.dificuldade": [None] + list(OC.DT27), "improviso.dt.faixa": [None] + L.FAIXAS}
            for k, op in par.items():
                if rng.random() < 0.6:
                    v = rng.choice(op)
                    if v is not None:
                        E[k] = v
            _rolador(rng, E)
            if R % 3 == 0:
                _minhas(rng, E)
            if R % 25 == 0:        # entradas inválidas (avisos nos dois sentidos)
                E.update({"mundos.r510": rng.choice([0, 2000000, "abc"]), "mundos.nomes.cultura": "Elfo",
                          "improviso.evento.onde": "Lua", "improviso.loja.tipo": "Padaria",
                          "improviso.oraculo.prob": "Talvez", "improviso.dt.dificuldade": "Impossível",
                          "improviso.dt.faixa": "21-24", "minhas.1.rolagem": -5})
            _t(E, f"Fase 3 S={s} R={R}", PREF_GER, limite=4, peso=PESO)
    r.info("Fase 3: G = 510…650 e 701…710 em 300 Rolagens nº × 3 sementes (900 casos), parâmetros de §5 sorteados, "
           "rolador e Minhas Tabelas com entradas inválidas")
    for k in range(60):
        _t(estado_campanha(rng, k), f"campanha {k + 1}", PREF_CAMP, limite=6, peso=PESO)
    r.info("Fase 3: 60 estados de campanha (facções, relógios, linha do tempo, Grupo G4–G6, Sessões, Missões, painel)")
    validar_heuristicas(r)


def estado_campanha(rng, k):
    """Um estado de campanha com entradas válidas, inválidas e vazias em todas as tabelas da Fase 3."""
    E = {"campanha.nivel": rng.randint(1, 20), "campanha.jogadores": rng.choice([None, 1, 3, 4, 6, 8]),
         "campanha.dia": rng.choice([None, 1, 3, 7, 12, 0, "x"]), "campanha.sessao": rng.choice([None, 1, 2, 5]),
         "campanha.sessoes_nivel": rng.choice([None, 0, 2, 4, 5, 7, 100, -1, "x"]),
         "campanha.metodo": rng.choice([None, "Array oficial", "Compra de Pontos"]),
         "campanha.nome": rng.choice([None, "Campanha de teste"])}
    facs = list(OH.FACCAO_FICHAS) + ["Guilda dos Relojoeiros"]
    for i in range(1, 13):
        if rng.random() < 0.6:
            E[f"campanha.fac.{i}.nome"] = rng.choice(facs)
        if rng.random() < 0.6:
            E[f"campanha.fac.{i}.atitude"] = rng.choice([-3, -2, -1, 0, 1, 2, 3, 4, -4, 0.5])
        if rng.random() < 0.2:
            E[f"campanha.fac.{i}.notas"] = "nota"
    for i in range(1, 11):
        if rng.random() < 0.7:
            E[f"campanha.rel.{i}.seg"] = rng.choice([4, 6, 8, 10, 12, 5, 0])
        if rng.random() < 0.7:
            E[f"campanha.rel.{i}.n"] = rng.choice([0, 1, 2, 3, 5, 7, 9, 11, 12, 13, -1, 1.5, "x"])
        if rng.random() < 0.4:
            E[f"campanha.rel.{i}.nome"] = f"Relógio {i}"
    for i in range(1, 31):
        if rng.random() < 0.5:
            E[f"campanha.tl.{i}.dia"] = rng.choice([1, 2, 3, 3, 5, 8, 13, 20, 0, 10000, 2.5, "x"])
        if rng.random() < 0.4:
            E[f"campanha.tl.{i}.evento"] = f"Evento {i}"
        if rng.random() < 0.2:
            E[f"campanha.tl.{i}.sessao"] = rng.randint(1, 9)
    for i in range(1, 7):
        if rng.random() < 0.8:
            E[f"grupo.pj{i}.nome"] = f"PJ{i}"
        for c in OC.TR6 + OC.PER6:
            if rng.random() < 0.4:
                E[f"grupo.pj{i}.{c}"] = rng.choice([-1, 0, 2, 3, 5, 8, 41, -6])
        E[f"grupo.pj{i}.raca"] = rng.choice(L.RACAS)
        if rng.random() < 0.5:
            E[f"grupo.pj{i}.cone"] = rng.choice([1, 2, 3, 4, 5])
        if rng.random() < 0.5:
            E[f"grupo.pj{i}.tier"] = rng.choice([1, 2, 3, 4])
    for i in range(1, 21):
        if rng.random() < 0.5:
            E[f"missoes.{i}.missao"] = f"Missão {i}"
        if rng.random() < 0.6:
            E[f"missoes.{i}.estado"] = rng.choice(OC.ESTADOS + ["Perdida", "ativa"])
        if rng.random() < 0.3:
            E[f"missoes.{i}.marco"] = rng.choice(["Sim", "Não"])
        for c in ("inicio", "fim"):
            if rng.random() < 0.3:
                E[f"missoes.{i}.{c}"] = rng.randint(1, 9)
    for k_ in range(1, 6):
        E.update({f"sessoes.cena.{k_}.tipo": rng.choice([None, "Social", "Combate", "Viagem"]),
                  f"sessoes.cena.{k_}.dificuldade": rng.choice([None] + list(OC.DT27) + ["Impossível"]),
                  f"sessoes.cena.{k_}.faixa": rng.choice([None] + L.FAIXAS),
                  f"sessoes.cena.{k_}.encontro": rng.choice([None, "Nenhum", "A", "B", "C", "D"])})
    if k % 3 == 0:
        for j in range(1, rng.randint(1, 4)):
            E[f"encontros.A.{j}.criatura"] = rng.choice([f["nome"] for f in L.bestiario_md()])
    E["sessoes.check.combates.n"] = rng.choice([None, 0, 2, 3, 4, 10, "x"])
    for i in range(1, 31):
        if rng.random() < 0.4:
            E[f"sessoes.diario.{i}.marco"] = rng.choice(["Sim", "Não", "Não", "Talvez"])
        if rng.random() < 0.3:
            E[f"sessoes.diario.{i}.n"] = i
    for k_ in range(1, 11):
        if rng.random() < 0.4:
            E[f"sessoes.pista.{k_}.texto"] = f"Pista {k_}"
            E[f"sessoes.pista.{k_}.revelada"] = rng.choice(["Sim", "Não"])
    E.update({"sessoes.prep.n": rng.choice([None, 1, 3]), "sessoes.prep.titulo": rng.choice([None, "Título"]),
              "sessoes.gancho.2.texto": rng.choice([None, "Gancho"])})
    return {a: b for a, b in E.items() if b is not None}


# ---------------------------------------------------------------------------
# heurísticas e propriedades no oráculo (o oráculo é conferido contra a planilha nos casos acima)
# ---------------------------------------------------------------------------

# campo sorteado -> lista que ele indexa (para a propriedade (d): toda entrada de toda lista alcançável)
CAMPOS_LISTA = {(510, 1): "mundo_tipo", (510, 2): "mundo_condicao", (510, 4): "manha", (510, 5): "pararam",
                (510, 6): "ameaca", (510, 7): "faccoes", (510, 8): "lugar_a", (510, 9): "lugar_b",
                (520, 1): "estacao_funcao", (520, 3): "estacao_problema", (530, 1): "nave_a", (530, 2): "nave_b",
                (530, 3): "nave_classe", (530, 4): "nave_peculiaridade", (530, 6): "ocupacao", (540, 1): "faccao_a",
                (540, 2): "faccao_b", (540, 4): "faccao_quer", (540, 5): "faccao_metodo", (540, 6): "faccao_recurso",
                (540, 7): "faccao_uso", (550, 1): "organizacao", (550, 5): "org_oferece", (550, 6): "org_cobra",
                (560, 8): "organizacao", (600, 1): "rumor", (600, 2): "veracidade", (600, 6): "gancho",
                (610, 2): "evento_cidade", (610, 3): "complicacao", (610, 4): "custo_falha", (620, 12): "maneirismo",
                (620, 13): "item_raro", (630, 1): "bugiganga"}


def validar_heuristicas(r):
    S0 = 12345
    # (d) toda entrada de toda lista da Fase 3 é alcançável em 2 000 rolagens
    n_d = 0
    for (g, c), id_ in CAMPOS_LISTA.items():
        n = len(OH.lista(id_))
        vistos = {O.escolha(O.valor(S0, g, R, c), n) for R in range(1, 2001)}
        r.ok(len(vistos) == n, f"(d) G={g} C={c} ({id_}): {len(vistos)} de {n} entradas em 2 000 rolagens")
        n_d += n
    for t, n in ((6, 6), (6, 23), (4, 9)):         # a loja (estoques do H15) e os 9 Caminhos
        vistos = {O.escolha(O.valor(S0, 620, R, 2), n) for R in range(1, 2001)}
        r.ok(len(vistos) == n, f"(d) loja / Caminhos, lista de {n}: {len(vistos)}")
    r.info(f"(d) {len(CAMPOS_LISTA)} campos da Fase 3, {n_d} entradas, todas alcançadas em 2 000 rolagens")
    # H10: Meio a meio = 50% de "Sim…" (d20 + 0 ≥ 11); a probabilidade cresce com o modificador
    resp = OH.lista("oraculo")
    lim = [OG._n(b) for _, b in OH.pares("oraculo") if OG._n(b) is not None]
    sims = {}
    for p, mod in OG.PROB.items():
        res = [resp[min(len(resp), 1 + sum(1 for b in lim if b < d + mod)) - 1] for d in range(1, 21)]
        sims[p] = sum(1 for x in res if x.startswith("Sim")) / 20
    r.ok(sims["Meio a meio"] == 0.5, f"H10: Meio a meio dá {sims['Meio a meio']:.0%} de Sim")
    ordem = [sims[p] for p in ("Quase impossível", "Improvável", "Meio a meio", "Provável", "Quase certo")]
    r.ok(ordem == sorted(ordem) and ordem[0] < ordem[-1], f"H10: probabilidade fora de ordem {ordem}")
    r.info("H10, chance de 'Sim…' por probabilidade: " + "; ".join(f"{p} {v:.0%}" for p, v in sims.items()))
    # H15 e H25: estoque de 6 sem repetir, quantidade 1 a 3, preço do livro; 3 rumores e 3 bugigangas sem repetir;
    # 10 nomes de cada sem repetir (listas ≥ 10)
    pools, _ = _loja_livro()
    preco = {x[0]: x[1] for p in pools.values() for x in p}
    for R in range(1, 301):
        out = O.calcular({"improviso.r620": R, "improviso.r600": R, "improviso.r630": R, "mundos.r560": R,
                          "improviso.loja.tipo": OG.TIPOS_LOJA[R % 6]})
        it = [out[f"improviso.loja.{k}.item"] for k in range(1, 7)]
        r.ok(len(set(it)) == 6 and all(out[f"improviso.loja.{k}.preco"] == preco[it[k - 1]] and
                                       1 <= out[f"improviso.loja.{k}.qtd"] <= 3 for k in range(1, 7)),
             f"H15 rolagem {R}: {it}")
        for pref, n in (("improviso.rumor.", 3), ("improviso.bug.", 3)):
            vs = [out[f"{pref}{k}"] for k in range(1, n + 1)]
            r.ok(len(set(vs)) == n and all(vs), f"H25 {pref} rolagem {R}: {vs}")
        for c in ("pessoa", "lugar", "nave", "org"):
            vs = [out[f"mundos.nomes.{j}.{c}"] for j in range(1, 11)]
            r.ok(len(set(vs)) == 10, f"H25 nomes avulsos ({c}) rolagem {R}: repetidos")
    # Minhas Tabelas: sem repetir enquanto 'quantos' ≤ n, para n de 1 a 100
    rng = random.Random(710)
    for n in range(1, 101):
        E = {f"minhas.1.vaga{v}": f"e{v}" for v in rng.sample(range(1, 101), n)}
        for q in range(1, 6):
            E.update({"minhas.1.quantos": q, "minhas.1.rolagem": rng.randint(1, 10 ** 6)})
            out = {"inicio.semente_ef": 12345}
            OG.minhas(E, out)
            res = [out[f"minhas.1.res.{k}"] for k in range(1, q + 1)]
            r.ok(len(set(res)) == min(q, n) and all(res), f"Minhas Tabelas n={n} quantos={q}: {res}")
    r.info("H15: 300 lojas (6 itens distintos, preço do livro, 1 a 3 de cada); H25: rumores, bugigangas e os 10 nomes "
           "avulsos de cada tipo sem repetir em 300 rolagens; Minhas Tabelas sem repetir com n = 1…100 e quantos = 1…5")
    # H16: os 45 casos e o painel no oráculo (a planilha é conferida no ouro)
    for s in (4, 6, 8, 10, 12):
        for n in range(0, s + 1):
            out = {"campanha.nivel_ef": 1, "campanha.dia_ef": 1}
            out.update({"campanha.jogadores_ef": 4, "campanha.ph_max": 5, "campanha.ph_ini": 3})
            OC._relogios({"campanha.rel.1.seg": s, "campanha.rel.1.n": n}, out)
            r.ok(out["campanha.rel.1.barra"].count("●") == n and out["campanha.rel.1.barra"].count("○") == s - n and
                 out["campanha._falta1"] == (1 if n == s - 1 else 0), f"H16 oráculo {s}/{n}")


# ---------------------------------------------------------------------------
# lint e texto da Fase 3
# ---------------------------------------------------------------------------

def lint_fase3(r, wb):
    """Nenhuma aba "Em construção"; Escudo do Mestre em A4 paisagem ajustado à largura, área de impressão, quebras no
    fim de cada página, linha-guia "— página N de M —" e altura de cada página dentro de uma A4 paisagem."""
    provisorio = ("em construção", "próxima fase", "proxima fase")     # revisão da Fase 3, F1
    for ws in wb.worksheets:
        achou = [c.coordinate for ln in ws.iter_rows() for c in ln if c.value == N.EM_CONSTRUCAO]
        r.ok(not achou, f"{ws.title}: ainda diz 'Em construção' ({achou[:3]})")
        achou = [c.coordinate for ln in ws.iter_rows() for c in ln
                 if isinstance(c.value, str) and any(p in c.value.lower() for p in provisorio)]
        r.ok(not achou, f"{ws.title}: texto provisório ('Em construção' / 'próxima fase') em {achou[:3]}")
    ws = wb["Escudo do Mestre"]
    esc = TC.mapa()["escudo"]
    r.ok(ws.page_setup.orientation == "landscape", f"Escudo: orientação {ws.page_setup.orientation}")
    r.ok(str(ws.page_setup.paperSize) == "9", f"Escudo: papel {ws.page_setup.paperSize} (A4 = 9)")
    r.ok(ws.page_setup.fitToWidth in (1, "1") and ws.sheet_properties.pageSetUpPr.fitToPage, "Escudo: ajuste à largura")
    pag = esc["paginas"]
    r.ok(str(ws.print_area).replace("$", "").endswith(f"A1:J{pag[-1][1]}"), f"Escudo: área de impressão {ws.print_area}")
    quebras = [b.id for b in ws.row_breaks.brk]
    r.ok(quebras == [b for _, b in pag[:-1]], f"Escudo: quebras {quebras} × páginas {pag}")
    for k, (a, b) in enumerate(pag, start=1):
        h = sum((ws.row_dimensions[x].height or 15) for x in range(a, b + 1))
        r.ok(h <= esc["altura_maxima_pt"], f"Escudo página {k}: {h} pt > {esc['altura_maxima_pt']} pt")
        guia = ws[TC.mapa()["celulas"][f"escudo.pagina{k}"].split("!")[1]].value or ""
        r.ok(guia.startswith(f"— Escudo do Mestre · página {k} de {len(pag)}"), f"Escudo: linha-guia da página {k}: "
                                                                                  f"{guia!r}")
    r.info(f"Escudo do Mestre: A4 paisagem, {len(pag)} páginas, alturas "
           f"{[sum((ws.row_dimensions[x].height or 15) for x in range(a, b + 1)) for a, b in pag]} pt "
           f"(máximo {esc['altura_maxima_pt']})")


def texto_fase3(r):
    """H24: cada item da Sessão Zero que cita o livro cita uma seção que existe e que tem a palavra-chave; os itens sem
    seção são os três da H24, rotulados. Os 5 custos da falha (02, 27.1) abrem a tabela custo_falha, na ordem."""
    from mestre.aba_campanha3 import SESSAO_ZERO
    import mestre_sabor_mundo as MU
    secs = {"03": ("03", "## Antes de jogar"), "27.5": ("27", "## 27.5"), "27.7": ("27", "## 27.7"),
            "19.1": ("19", "## 19.1"), "16.2": ("16", "## 16.2"), "06.4": ("06", "## 6.4"), "28.3": ("28", "## 28.3"),
            "27.1": ("27", "## 27.1"), "02": ("02", "# "), "27.15": ("27", "## 27.15"), "27.19": ("27", "## 27.19"),
            "26.1": ("26", "## 26.1"), "27.8": ("27", "## 27.8"), "25.1": ("25", "## 25.1")}
    sem = 0
    for chave, item_, texto, secoes, palavra in SESSAO_ZERO:
        if secoes is None:
            sem += 1
            continue
        texto_livro = " ".join(L.limpo(" ".join(_secao(*secs[s]))) for s in secoes)
        r.ok(palavra.lower() in texto_livro.lower(), f"H24: '{item_}' cita {secoes} e a seção não tem '{palavra}'")
    r.ok(sem == 3, f"H24: {sem} itens sem seção do livro (esperado 3: tom e temas, limites e véus, expectativas)")
    mapa = TC.mapa()
    h24 = [s for s in mapa["sugestoes"] if s["h"] == "H24"]
    r.ok(len(h24) == 4, f"H24: {len(h24)} rótulos (os 3 itens e os combinados)")
    t = " ".join(L.limpo(l) for l in _secao("27", "## 27.1"))
    r.ok("tempo, ruído, recurso, informação incompleta, uma complicação nova" in t, "27.1: os 5 custos da falha")
    pos = [next((k for k, v in enumerate(MU.CUSTO_FALHA) if c in v), -1) for c in MU.CUSTO_FALHA_LIVRO]
    r.ok(pos == [0, 1, 2, 3, 4], f"custo_falha: os 5 custos do livro abrem a tabela, na ordem ({pos})")
