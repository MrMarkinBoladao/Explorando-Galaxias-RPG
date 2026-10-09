# -*- coding: utf-8 -*-
"""Suítes dados e bestiario. O parser é o do teste (build\\oraculo_mestre_livro.py, que não importa
build\\mestre_dados.py nem build\\ficha_dados.py): a aba Dados e as listas "Livro" da aba Tabelas são
comparadas com o .md."""

import re

import openpyxl

import testar_ficha as TF
import oraculo_mestre_livro as L
from mestre import nucleo as N
from mestre import testes_comum as TC
from mestre.testes_regras import planilha

Resultado = TF.Resultado


def _bloco(wb, id_):
    b = TC.mapa()["blocos"][f"dados.{id_}"]
    ws = wb["Dados"]
    cols = b["colunas"]
    linhas = []
    for r in range(b["primeira_linha"], b["ultima_linha"] + 1):
        linhas.append({c: ws[f"{l}{r}"].value for c, l in cols.items()})
    return linhas


def _v(x):
    return "" if x is None else x


def suite_dados(args):
    r = Resultado("dados")
    wb = openpyxl.load_workbook(N.SAIDA_MODELO)
    # 28.3 — âncoras e dano em dados (relidos do .md pelo teste)
    md = L._md("28")
    i = next(k for k, l in enumerate(md) if l.startswith("## 28.3"))
    tab = [L._cels(l) for l in md[i:i + 40] if l.startswith("| **")]
    for row in _bloco(wb, "ancoras"):
        fx, t = row["Faixa"], TIPOS.index(row["Tipo"])
        lin = next(x for x in tab if x[0] == fx and len(x) == 13)
        tri = lambda c: [int(v) for v in re.findall(r"[+-]?\d+", lin[c])]  # noqa: E731
        esp = {"PV": int(lin[1 + t]), "Defesa": tri(4)[t], "RD": tri(5)[t], "Tenacidade": tri(6)[t], "VEL": tri(7)[t],
               "Ataque": int(lin[8].strip("+")), "Média do dano": tri(9)[t], "DT dos efeitos": tri(10)[t],
               "Teste de Resistência": tri(11)[t]}
        for c, v in esp.items():
            r.ok(row[c] == v, f"28.3 {fx} {row['Tipo']} {c}: Dados={row[c]!r} livro={v!r}")
        dd = next(x for x in tab if x[0] == fx and len(x) == 4)
        e, m = [s.strip() for s in dd[1 + t].split("·")]
        r.ok(row["Dano por acerto"] == e and row["Média do dano"] == int(m), f"28.3 dano em dados {fx} {row['Tipo']}")
    # H2 — dano especial: fonte "ficha" = a expressão está impressa na ficha citada; média = INT(1,5 × âncora)
    for row in _bloco(wb, "dano_especial"):
        fx, tp = row["Chave"].split("|")
        a = L.ancora(fx, tp)
        r.ok(row["Média"] == int(1.5 * a["dano_m"]), f"H2 {row['Chave']}: média {row['Média']} ≠ INT(1,5 × {a['dano_m']})")
        if row["Fonte"] == "ficha":
            f = L.ficha(row["Ficha"])
            achou = any(f"{row['Expressão']} · " in x["texto"] for x in f["acoes"])
            r.ok(achou, f"H2 {row['Chave']}: {row['Expressão']} não está impresso na ficha de {row['Ficha']}")
    # 28.6–28.11 — as 32 fichas
    fichas = {f["nome"]: f for f in L.bestiario_md()}
    linhas = _bloco(wb, "bestiario")
    r.ok(len(linhas) == 32, f"bestiário com {len(linhas)} fichas")
    for row in linhas:
        f = fichas.get(row["Nome"])
        if not r.ok(f is not None, f"ficha {row['Nome']} não está no .md"):
            continue
        for c, v in (("Tipo", f["tipo"]), ("Faixa", f["faixa"]), ("Facção ou origem", f["faccao"]), ("PV", f["pv"]),
                     ("Fases", f["fases"]), ("Resistência", f["res"]), ("Execução", f["execucao"]),
                     ("Frase", f["frase"]), ("Custo no orçamento", f["custo"])):
            r.ok(TF._igual(_v(row[c]), v), f"{row['Nome']} {c}: Dados={row[c]!r} livro={v!r}")
        fr = [_v(row[f"Fraqueza {k}"]) for k in range(1, 5)]
        r.ok(fr[:len(f["fraquezas"])] == f["fraquezas"] and not any(fr[len(f["fraquezas"]):]),
             f"{row['Nome']} Fraquezas: {fr} × {f['fraquezas']}")
    fases = _bloco(wb, "bestiario_fases")
    r.ok(len(fases) == 12, f"bestiario_fases com {len(fases)} linhas (esperado 12)")
    for row in fases:
        d = next(x for x in fichas[row["Criatura"]]["fases_d"] if x["fase"] == row["Fase"])
        r.ok((row["PV do topo"], row["PV do piso"], row["Tenacidade"], row["Ritmo"]) ==
             (d["topo"], d["piso"], d["ten"], d["ritmo"]) and [row[f"Fraqueza {k}"] for k in range(1, 5)] == d["fraq"],
             f"fase {row['Chave']}: {row} × {d}")
    # 27.4, 27.7, 27.2, 20.2, 20.5, 16.2, 24.5, 25.1
    for k, row in enumerate(_bloco(wb, "orcamento")):
        r.ok((row["Dano do grupo por Ciclo"], row["Orçamento"]) == L.ORC[k], f"27.4 {row}")
    comp = _bloco(wb, "composicoes")
    for row, (n, (b, e, c), s, d) in zip(comp, L.COMPOS):
        r.ok((row["Composição"], row["Boss"], row["Elite"], row["Comum"], row["Como ela se sente"],
              row["Duração esperada"]) == (n, b, e, c, s, d), f"27.4 composição {row['Composição']}")
    for k, row in enumerate(_bloco(wb, "attrition")):
        r.ok(row["O grupo termina com"] == L.ATTR[k], f"27.7 {row}")
    dt = {row["Dificuldade"]: row for row in _bloco(wb, "dt_faixa")}
    for nome, vals in L.DT.items():
        r.ok([dt[nome][fx] for fx in FAIXAS] == list(vals), f"27.2 {nome}")
    r.ok([x["DT"] for x in _bloco(wb, "dt_fraqueza")] == list(L.DT_FRAQ), "20.2 DT de Fraqueza")
    for row in _bloco(wb, "elementos"):
        r.ok((row["Nº de dados"], row["Faces"], row["Multiplicador da Eficiência"]) == L.QUEBRA[row["Elemento"]],
             f"20.5 {row['Elemento']}")
    for row in _bloco(wb, "tenacidade"):
        r.ok(L.REDUCAO.get(row["Fonte"]) == row["Redução bruta"], f"20.3 {row}")
    for row in _bloco(wb, "condicoes"):
        if row["Condição"] in L.CONDICOES:
            nd, fc, pa, se, pct, tef, atr, tac, dc = L.CONDICOES[row["Condição"]]
            r.ok((row["Nº de dados"], row["Faces"], row["% dos PV máximos"], row["Teto (× Eficiência)"],
                  row["Atrasa (casas)"], row["Teto de acúmulos"]) == (nd, fc, pct, tef, atr, tac), f"21.5 {row['Condição']}")
    for row in _bloco(wb, "ph"):
        mx = L.PH_MAX[row["Nº de jogadores"]]
        r.ok((row["Máximo 1-8"], row["Máximo 9-16"], row["Máximo 17-20"], row["Início 1-8"]) ==
             (mx[0], mx[1], mx[2], mx[0] - 2), f"16.2 {row}")
    r.ok([x["Verba de marco (Cr)"] for x in _bloco(wb, "verba")] == list(L.VERBA), "24.5 verba")
    r.ok([x["Relíquias"] for x in _bloco(wb, "faixas_equipamento")] == list(L.RELIQ), "25.1 Relíquias")
    # Listas "Livro" da aba Tabelas: 27.16 facções, 27.17 locais, 27.18 ganchos
    m27 = L._md("27")
    sec = lambda t: m27[next(k for k, l in enumerate(m27) if l.startswith(t)):]  # noqa: E731
    fac = []
    for l in sec("## 27.16")[1:]:
        if l.startswith("## "):
            break
        if l.startswith("### "):
            fac.append(l[4:].strip())
    loc = []
    for l in sec("## 27.17")[1:]:
        if l.startswith("## "):
            break
        if l.startswith("| **"):
            loc.append(L._cels(l)[0])
    gan = {}
    for l in sec("## 27.18")[1:]:
        if l.startswith("## "):
            break
        if l.startswith("| **"):
            c = L._cels(l)
            gan[c[0]] = [x.strip() for x in c[1].split(" · ")]
    ws = wb["Tabelas"]
    esperado = {"faccoes": fac, "locais": loc, **{f"ganchos_{k.replace('-', '_')}": v for k, v in gan.items()}}
    for id_, vals in esperado.items():
        t = TC.mapa()["tabelas"][f"tab.{id_}"]
        lidos = [ws[c].value for c in t["vagas"] if ws[c].value not in (None, "")]
        r.ok(lidos == vals, f"Tabelas {id_}: {lidos[:3]}… × livro {vals[:3]}…")
    r.ok(len(fac) == 8 and len(loc) == 6 and sum(len(v) for v in gan.values()) == 20,
         f"27.16–27.18: {len(fac)} facções, {len(loc)} locais, {sum(len(v) for v in gan.values())} ganchos")
    # H8: toda criatura com ≥ 1 ambiente; todo ambiente com criatura em ≥ 2 faixas
    amb = TC.mapa()["tabelas"]["tab.ambiente_por_faccao"]
    pares = list(zip([ws[c].value for c in amb["vagas"]], [ws[c].value for c in amb["ambientes"]]))
    for f in fichas.values():
        r.ok(any(fc in (f["faccao"], f["origem2"]) for fc, a in pares if fc), f"H8: {f['nome']} sem ambiente")
    uma = []
    for a in {a for _, a in pares if a}:
        fx = {f["faixa"] for f in fichas.values() if any(a2 == a and fc in (f["faccao"], f["origem2"]) for fc, a2 in pares)}
        r.ok(len(fx) >= 1, f"H8: ambiente {a} sem criatura")
        if len(fx) < 2:
            uma.append(f"{a} ({', '.join(sorted(fx))})")
    r.info("H8: ambientes com criatura numa faixa só (o livro dá às facções uma faixa; o encontro aleatório cai para "
           "'qualquer ambiente da faixa' e diz isso): " + "; ".join(sorted(uma)))
    from mestre import testes_hist
    testes_hist.dados_fase2(r, wb)     # equipamentos, Cones, Relíquias, Ressonâncias item a item (Fase 2)
    from mestre import testes_fase3
    testes_fase3.dados_fase3(r, wb)    # Escudo, loja, trechos de regra e os blocos novos (Fase 3)
    return r


TIPOS = L.TIPOS
FAIXAS = L.FAIXAS


def suite_bestiario(args):
    r = Resultado("bestiario")
    fichas = L.bestiario_md()
    import mestre_dados as D
    doc = {(d[1], d[2]): d for d in D.DIVERGENCIAS_DOCUMENTADAS}
    linhas = []
    for f in fichas:
        a = L.ancora(f["faixa"], f["tipo"])
        prob = []
        c = f["campos"]
        for campo, k in (("Defesa", "defesa"), ("RD", "rd"), ("Velocidade", "vel"), ("DT dos efeitos", "dt")):
            if int(c[campo]) != a[k]:
                prob.append(f"{campo} {c[campo]} ≠ âncora {a[k]}")
        if int(c["Teste de Ataque"].strip("+")) != a["ataque"] or int(c["Teste de Resistência"].strip("+")) != a["tr"]:
            prob.append("Ataque/TR ≠ âncora")
        if int(re.match(r"\d+", c["PV"]).group(0)) != a["pv"]:
            prob.append("PV ≠ âncora")
        n = len(f["fraquezas"])
        if not ((1 <= n <= 2) if f["tipo"] == "Comum" else n == {"Elite": 3, "Boss": 4}[f["tipo"]]):
            prob.append(f"{n} Fraquezas")
        for d in f["fases_d"]:
            if d["ten"] != a["ten"] and (f["nome"], f"Tenacidade da fase {d['fase']}") not in doc:
                prob.append(f"Tenacidade da fase {d['fase']} {d['ten']} não documentada")
            if d["ten"] > a["ten"]:
                prob.append("Tenacidade de fase acima da âncora (28.5 regra 3)")
        # H4: limiares em partes iguais reproduzem a barra
        if f["fases"] == 2:
            ok4 = f["fases_d"][1]["topo"] == f["pv"] // 2 and f["fases_d"][0]["piso"] == f["pv"] // 2 + 1
        elif f["fases"] == 3:
            ok4 = (f["fases_d"][1]["topo"], f["fases_d"][2]["topo"]) == ((2 * f["pv"]) // 3, f["pv"] // 3)
        else:
            ok4 = True
        if not ok4:
            prob.append("H4 não reproduz a barra")
        # ficha completa na planilha (texto do livro) e Ajustar na própria faixa (H3: 0 diferença)
        E = {"bestiario.ver": f["nome"], "inimigos.1.nome": "Teste", "inimigos.1.modo": "Ajustar do bestiário",
             "inimigos.1.base": f["nome"], "inimigos.1.faixa": f["faixa"], "inimigos.ver": "Teste"}
        nomes = [f"bestiario.ficha.acao{k}" for k in range(1, 13)] + [f"inimigos.ficha.acao{k}" for k in range(1, 13)]
        got = planilha(E, nomes)
        for k, ac in enumerate(f["acoes"], start=1):
            if got[f"bestiario.ficha.acao{k}"] != ac["texto"]:
                prob.append(f"ação {k} (Bestiário) ≠ livro")
            if got[f"inimigos.ficha.acao{k}"] != ac["texto"]:
                prob.append(f"ação {k} (Ajustar na faixa original) ≠ livro: {got[f'inimigos.ficha.acao{k}'][:60]!r}")
        if len(f["acoes"]) > 12:
            prob.append("mais de 12 ações (a ficha mostra 12)")
        r.ok(not prob, f"✗ {f['n']} {f['nome']}: {'; '.join(prob)}")
        linhas.append(f"{'OK' if not prob else '✗'} {f['n']:>2} {f['nome']}: 15 campos, {f['fases']} fase(s), "
                      f"{len(f['acoes'])} ações" + (f" — {'; '.join(prob)}" if prob else ""))
    for l in linhas:
        r.info(l)
    r.ok(sum(1 for f in fichas if f["res"]) == 5, "28.11: cinco inimigos com Resistência")
    r.ok(sum(f["fases"] > 1 for f in fichas) == 5 and sum(len(f["fases_d"]) for f in fichas) == 12,
         "28.5: 5 Bosses com fases, 12 linhas de fase")
    sem = sum(1 for f in fichas if f["execucao"] == "Não declarado")
    r.info(f"L1: {sem} fichas sem Execução declarada ('Não declarado'); {32 - sem} declaram (Pode/Não)")
    for d in D.DIVERGENCIAS_DOCUMENTADAS:
        r.info(f"divergência documentada (o livro não muda): {d[0]} {d[1]} — {d[2]} = {d[3]}; a planilha mostra {d[4]}")
    r.info(f"{sum(len(f['acoes']) for f in fichas)} ataques e ações renderizados na faixa original, 0 diferença exigida")
    return r
