# -*- coding: utf-8 -*-
"""Suítes extremos (recálculo sem célula de erro), preview (recortes ≤ 1800 px, 0 texto cortado — plano P6) e
visual (régua da ficha: cabe na célula, listas com a seta, contraste, fonte, 15 linhas, 1360 px)."""

import random
import shutil
import tempfile
import time
from pathlib import Path

import openpyxl

import testar_ficha as TF
import renderizar_ficha as R
from mestre import nucleo as N
from mestre import testes_comum as TC

Resultado = TF.Resultado
PREVIEW = N.RAIZ / ".agents" / "tasks" / "mestre" / "preview"


def _erros(sol):
    return [k for k, v in sol.items() if TF.eh_erro(v)]


def _formulas_por_aba(wb):
    d = {}
    for ws in wb.worksheets:
        for linha in ws.iter_rows():
            for c in linha:
                if isinstance(c.value, str) and c.value.startswith("="):
                    d.setdefault(ws.title, []).append(f"'{ws.title}'!{c.coordinate}")
    return d


def _tabelas(valor):
    """Todas as vagas da aba Tabelas vazias ("") ou cheias (valor)."""
    d = {}
    for t in TC.mapa()["tabelas"].values():
        for c in t["vagas"] + t.get("ambientes", []) + t.get("segunda", []):
            d[f"'Tabelas'!{c}"] = "" if valor == "" else f"{valor} {c}"
    return d


def _combate_cheio():
    E = TC.entradas_grupo([{"nome": f"PJ{i}", "pv": 30 + i, "vel": 10 + i, "ag": i % 3, "disc": 1, "pres": 1,
                            "raca": "Xianzhouíta" if i == 2 else "Humano", "elemento": "Fogo"} for i in range(1, 7)])
    E.update({"campanha.nivel": 20, "combate.carregar": "A", "combate.ciclo": 1, "combate.surpresa": "Grupo surpreendido"})
    for j, (nm, q) in enumerate([("O Germe de Pavor", 1), ("Escória de Stellaron", 4), ("Arcanjo de Ferro-Vazio", 2),
                                 ("Guarda Pretoriano da Antimatéria", 3)], start=1):
        E.update({f"encontros.A.{j}.criatura": nm, f"encontros.A.{j}.qtd": q})
    for i in range(1, 7):                     # os 6 Memoespíritos ligados e invocados (Fase 4): 22 combatentes
        E.update({f"grupo.pj{i}.memo.tem": "Sim", f"grupo.pj{i}.memo.nome": f"Lembrança Antiga Número {i}",
                  f"grupo.pj{i}.memo.vel": 10 + i, f"grupo.pj{i}.memo.agi": 5, f"combate.memo{i}.invocado": "Sim",
                  f"combate.memo{i}.dano": -50 if i == 1 else 3})
    E["combate.memo2.pv"] = 0
    for i in range(1, TC.NC + 1):
        E.update({f"combate.f{i}.atraso": i % 5, f"combate.f{i}.pend": i % 3, f"combate.f{i}.avancar": i % 2,
                  f"combate.f{i}.ja": "Sim" if i % 4 == 0 else None, f"combate.f{i}.avtotal": "Sim" if i == 3 else None})
    E.update({"combate.pj1.pv": 0, "combate.pj1.fal": 2, "combate.pj2.pv": 0, "combate.pj3.pv": 0, "combate.pj3.fal": 3,
              "combate.in1.pv": 300, "combate.in1.fase": 3, "combate.in2.pv": 0, "combate.in1.reducao": 99,
              "combate.in1.elemq": "Gelo", "combate.in3.elemq": "Físico", "combate.in1.usada1": 1})
    labs = ["Escória de Stellaron 1", "Arcanjo de Ferro-Vazio 1", "PJ4", "O Germe de Pavor", "PJ5",
            "Lembrança Antiga Número 3 (de PJ3)"]
    for n in range(1, TC.NC * 4 + 1):         # as 88 condições da C7 ocupadas (4 por combatente)
        E.update({f"combate.c{n}.cond": ["Congelado", "Surpreso", "Sangramento", "Embaraço", "Aprisionamento",
                                         "Marcado", "Cisalhamento de Vento"][n % 7],
                  f"combate.c{n}.turnos": n % 3, f"combate.c{n}.acum": n % 7, f"combate.c{n}.quem": labs[(n + 1) % 6]})
    E.update({"combate.calc.alvo": "O Germe de Pavor", "combate.calc.fonte": "Ultimate", "combate.calc.n": 6,
              "combate.calc.f": 10, "combate.calc.elem": "Gelo", "combate.calc.crit": "Sim", "combate.calc.extra": 5})
    return E


def _historia_cheia():
    """Fase 2: os 30 NPCs do Elenco com texto no máximo, os 4 cartões, as 25 linhas do Tesouro (saldo negativo) e os
    geradores com parâmetros nos extremos."""
    import renderizar_ficha as R_
    E = {"campanha.nivel": 20, "campanha.jogadores": 6, "npcs.rolagem": 1000000, "npcs.raca": "Intellitron",
         "npcs.caminho": "Nenhum", "npcs.bloco_faixa": "Do grupo", "npcs.bloco_tipo": "Elite",
         "aventuras.rolagem": 999999, "aventuras.faixa": "17-20", "aventuras.faccao": "Autômatos",
         "recompensas.nivel": 20, "recompensas.marco": "Fim de arco", "recompensas.ach.leitura": "Pesado",
         "recompensas.cone.faixa": "17-20"}
    ent = TC.mapa()["entradas"]
    for i in range(1, 31):
        for c in ("nome", "ocupacao", "aparencia", "personalidade", "motivacao", "segredo", "maneirismo", "gancho",
                  "onde", "notas"):
            n = f"npcs.elenco.{i}.{c}"
            E[n] = N.texto_pior(int(ent[n].get("maximo") or 40), 3 * i) if c != "nome" else f"NPC número {i}"
        E.update({f"npcs.elenco.{i}.raca": "Xianzhouíta", f"npcs.elenco.{i}.caminho": "A Inexistência",
                  f"npcs.elenco.{i}.papel": "Antagonista", f"npcs.elenco.{i}.atitude": "Desconfiado",
                  f"npcs.elenco.{i}.relacao": -3, f"npcs.elenco.{i}.vivo": "Não", f"npcs.elenco.{i}.sessao": 999})
    for c in range(1, 5):
        E[f"npcs.cartao{c}.npc"] = f"NPC número {c}"
    for i in range(1, 26):
        E.update({f"recompensas.tes.{i}.sessao": 999, f"recompensas.tes.{i}.item": N.texto_pior(80, i),
                  f"recompensas.tes.{i}.qtd": 999, f"recompensas.tes.{i}.cr": -99999,
                  f"recompensas.tes.{i}.quem": N.texto_pior(40, i),
                  f"recompensas.tes.{i}.notas": N.texto_pior(200, i)})
    return E


def _campanha_cheia():
    """Fase 3: todas as tabelas da Campanha, Sessões e Missões cheias (texto no máximo), valores nos extremos e
    inválidos, 20 missões Ativas, 30 eventos, 10 relógios, 12 facções, o Grupo G5/G6 inteiro e os geradores de Mundos e
    Improviso nos extremos."""
    import mestre_dados3 as D3
    ent = TC.mapa()["entradas"]
    E = {"campanha.nivel": 20, "campanha.jogadores": 6, "campanha.dia": 9999, "campanha.sessao": 999,
         "campanha.sessoes_nivel": 99, "mundos.nomes.cultura": "Intellitron", "improviso.evento.onde": "Cidade",
         "improviso.loja.tipo": "Mercado da Frota de Jade", "improviso.oraculo.prob": "Quase certo",
         "improviso.dt.dificuldade": "Heroica", "improviso.dt.faixa": "17-20"}
    for k, (nome, info) in enumerate(sorted(ent.items())):
        if not nome.startswith(("campanha.fac.", "campanha.rel.", "campanha.tl.", "campanha.dec.", "campanha.sz.",
                                "sessoes.", "missoes.", "grupo.pj")) or info["tipo"] != "texto":
            continue
        E[nome] = N.texto_pior(int(info.get("maximo") or 40), 5 * k)
    for i in range(1, 13):
        E.update({f"campanha.fac.{i}.nome": "Corporação da Paz Interastral" if i < 3 else f"Facção {i}",
                  f"campanha.fac.{i}.atitude": [-3, 3, 4][i % 3], f"campanha.fac.{i}.ultimo": 999})
    for i in range(1, 11):
        E.update({f"campanha.rel.{i}.seg": [4, 12, 5][i % 3], f"campanha.rel.{i}.n": [3, 12, 13][i % 3]})
    for i in range(1, 31):
        E.update({f"campanha.tl.{i}.dia": [9999, 1, 0][i % 3], f"campanha.tl.{i}.sessao": 999,
                  f"campanha.tl.{i}.publico": "Sim"})
    for i in range(1, 7):
        for c in ("tr_pot", "tr_ref", "tr_rfis", "tr_rmen", "tr_pm", "tr_fv", "per_perc", "per_int", "per_furt",
                  "per_pesq", "per_cien", "per_sint", "per_pers"):
            E[f"grupo.pj{i}.{c}"] = 41 if i % 2 else -5
        E.update({f"grupo.pj{i}.nome": f"PJ{i}", f"grupo.pj{i}.raca": "Intellitron", f"grupo.pj{i}.tier": 1})
    for i in range(1, 21):
        E.update({f"missoes.{i}.estado": "Ativa" if i % 2 else "Concluída", f"missoes.{i}.marco": "Sim",
                  f"missoes.{i}.inicio": 999, f"missoes.{i}.fim": 1})
    for k in range(1, 6):
        E.update({f"sessoes.cena.{k}.tipo": "Combate", f"sessoes.cena.{k}.encontro": "ABC"[k % 3],
                  f"sessoes.cena.{k}.dificuldade": "Muito Difícil", f"sessoes.cena.{k}.faixa": "13-16"})
    for i in range(1, 31):
        E.update({f"sessoes.diario.{i}.n": 999, f"sessoes.diario.{i}.dia": 9999,
                  f"sessoes.diario.{i}.marco": ["Sim", "Não", "Talvez"][i % 3]})
    E.update({"sessoes.prep.n": 1, "sessoes.check.combates.n": 9})
    for k in range(1, 11):
        E[f"sessoes.pista.{k}.revelada"] = "Sim"
    for e in range(1, 4):
        E.update({f"improviso.rol.{e}.n": 20, f"improviso.rol.{e}.f": 100, f"improviso.rol.{e}.m": -50})
    E.update({"improviso.rol.1.n": 1, "improviso.rol.1.f": 20, "improviso.rol.1.v": "Desvantagem",
              "improviso.rol.3.v": "Vantagem"})
    return E


def _minhas(valor, nome=False):
    """Minhas Tabelas: as 1 000 vagas com texto no máximo (cheias) ou vazias com o nome e 'quantos' preenchidos."""
    E = {}
    for t in range(1, 11):
        if valor:
            for k in range(1, 101):
                E[f"minhas.{t}.vaga{k}"] = N.texto_pior(200, 13 * k + t)
        if nome:
            E.update({f"minhas.{t}.nome": f"Tabela do Mestre número {t}", f"minhas.{t}.quantos": 5,
                      f"minhas.{t}.rolagem": 1000000})
    return E


def suite_extremos(args):
    """Monta todos os casos e calcula em paralelo (mestre\\paralelo.py, plano §10 item 8)."""
    from mestre import paralelo
    r = Resultado("extremos")
    wb = openpyxl.load_workbook(N.SAIDA_MODELO)
    porab = _formulas_por_aba(wb)
    todas = [x for v in porab.values() for x in v]
    from mestre import exemplo
    tarefas = []
    avisos = [TC.C(n) for n in TC.mapa()["celulas"] if ".aviso" in n]

    def erros(rot, E, outs, **kw):
        tarefas.append({"tipo": "erros", "rot": rot, "E": E, "outs": outs, **kw})
    estados = {
        "em branco": {}, "Exemplo": TC.entradas(exemplo.entradas_nomes()),
        "grupo com 1 PJ": TC.entradas({"grupo.pj1.nome": "Só", "grupo.pj1.pv": 40, "grupo.pj1.elemento": "Fogo"}),
        "grupo cheio (6)": TC.entradas(TC.entradas_grupo([{"nome": f"P{i}", "pv": 50, "elemento": "Gelo"} for i in range(6)])),
        "nº de jogadores 8 (fora de 1–6)": TC.entradas({"campanha.jogadores": 8}),
        "nível 1, 1 jogador": TC.entradas({"campanha.nivel": 1, "campanha.jogadores": 1}),
        "nível 20, 6 jogadores": TC.entradas({"campanha.nivel": 20, "campanha.jogadores": 6}),
        "Tabelas vazias": _tabelas(""), "Tabelas cheias (100)": _tabelas("Item"),
        "Combate cheio (22, com os 6 Memoespíritos) e todos os estados": TC.entradas(_combate_cheio()),
        "Elenco (30), cartões e Tesouro (25) cheios": TC.entradas(_historia_cheia()),
        # Fase 3
        "Campanha, Grupo, Sessões e Missões cheias": TC.entradas(_campanha_cheia()),
        "Minhas Tabelas cheias (10 × 100)": TC.entradas(_minhas(True, nome=True)),
        "Minhas Tabelas vazias, com nome e quantos": TC.entradas(_minhas(False, nome=True)),
    }
    for nome, E in estados.items():
        kw = {}
        if nome == "em branco":
            kw = {"vazios": avisos, "msg_v": "modelo em branco com aviso aceso"}
        if nome.startswith("nº de jogadores 8"):
            kw = {"cheios": [TC.C("campanha.aviso.jogadores")], "msg_c": "jogadores = 8 sem aviso na Campanha (K8)"}
        if nome.startswith("Tabelas cheias"):
            kw = {"cheios": [TC.C(f"tab.{k}.aviso") for k in ("faccoes", "locais", "ocupacao", "nome.humano",
                                                               "objetivo", "rumor", "lugar_a", "oraculo")],
                  "msg_c": "lista cheia sem aviso"}
        if nome.startswith("Tabelas vazias"):
            kw = {"cheios": [TC.C(n) for n in ("npcs.aviso.ocupacao", "npcs.aviso.nome", "npcs.aviso.gancho",
                                               "aventuras.aviso.objetivo", "recompensas.ach.aviso.bugiganga",
                                               "recompensas.cone.aviso.nome", "mundos.planeta.tipo.aviso",
                                               "mundos.org.nome.aviso", "improviso.rumor.aviso",
                                               "improviso.oraculo.aviso", "improviso.bug.aviso",
                                               "improviso.loja.aviso.raro", "mundos.nomes.aviso.vazia")],
                  "msg_c": "lista vazia sem aviso"}
        if nome.startswith("Elenco (30)"):
            kw = {"cheios": [TC.C("recompensas.tes.aviso.saldo")], "msg_c": "Tesouro negativo sem aviso"}
        if nome.startswith("Campanha, Grupo"):
            kw = {"cheios": [TC.C(n) for n in ("missoes.aviso.ativas", "campanha.rel.2.aviso", "campanha.fac.1.aviso",
                                               "campanha.fac.5.aviso", "campanha.aviso.ritmo", "missoes.2.aviso2",
                                               "sessoes.check.combates.aviso", "sessoes.diario.2.aviso",
                                               "grupo.pj1.aviso5", "grupo.pj1.aviso4", "improviso.rol.3.aviso")],
                  "msg_c": "estado cheio sem o aviso esperado"}
        if nome.startswith("Minhas Tabelas cheias"):
            kw = {"cheios": [TC.C(f"minhas.{t}.aviso") for t in range(1, 11)], "msg_c": "lista cheia (100) sem aviso"}
        if nome.startswith("Minhas Tabelas vazias"):
            kw = {"cheios": [TC.C(f"minhas.{t}.aviso") for t in range(1, 11)], "msg_c": "tabela vazia sem aviso"}
        erros(nome, E, "@todas", **kw)
    r.info(f"{len(estados)} estados com as {len(todas)} fórmulas")
    # ~200 sementes × Rolagem nº 1 e 1 000 000 (P15): as fórmulas que dependem do sorteio (Inimigos, Encontros)
    # as células que dependem do sorteio: u/y/x, as sugestões (H12) e o encontro aleatório inteiro
    alvo = [v for k, v in TC.mapa()["celulas"].items() if ":" not in v and (k.startswith("encontros.ale.") or
            ".h12." in k or ".aux.sug" in k or ".aux.w" in k or k.endswith(".fraq_txt") or k.startswith(
                ("npcs.g", "npcs.res.", "npcs.saida.", "npcs.bloco.", "aventuras.", "recompensas.ach.",
                 "recompensas.cone.", "recompensas.conj.", "mundos.", "improviso.", "minhas.")))]
    rng = random.Random(15)
    sementes = [1, 12345, 2026, 2147483646] + [rng.randint(1, 2147483646) for _ in range(196)]
    base = TC.entradas(TC.entradas_grupo([{"nome": "A", "elemento": "Fogo"}, {"nome": "B", "elemento": "Gelo"}]))
    base.update(TC.entradas({"inimigos.1.nome": "X", "inimigos.2.nome": "Y", "inimigos.2.tipo": "Boss",
                             "improviso.rol.1.n": 20, "improviso.rol.2.n": 1, "improviso.rol.2.v": "Vantagem",
                             **{f"minhas.1.vaga{k}": f"Entrada {k}" for k in range(1, 8)}, "minhas.1.quantos": 5}))
    for s in sementes:
        for R_ in (1, 1000000):
            from mestre.testes_fase3 import ROLAGENS
            E = dict(base, **TC.entradas({"inicio.semente": s, "encontros.ale.rolagem": R_, "inimigos.rolagem": R_,
                                          "npcs.rolagem": R_, "aventuras.rolagem": R_, "recompensas.ach.rolagem": R_,
                                          "recompensas.cone.rolagem": R_, "recompensas.conj.rolagem": R_,
                                          **{k: R_ for k in ROLAGENS}}))
            erros(f"semente {s}, rolagem {R_}", E, "@alvo")
    r.info(f"{len(sementes)} sementes × 2 rolagens nas {len(alvo)} células que dependem do sorteio")
    # um campo por vez, válido e inválido (amostra de 150 entradas do mapa): avisos e números de regra da aba
    porab_leve = {}
    for k, v in list(TC.mapa()["numeros_de_regra"].items()) + [(a, N.MapaMestre.ref(a, c)) for a, cs in
                                                                 TC.mapa()["avisos"].items() for c in cs]:
        porab_leve.setdefault(TF.separar_ref(v)[0], []).append(v)
    ent = TC.mapa()["entradas"]
    for nome in rng.sample(sorted(ent), 150):
        aba = TF.separar_ref(TC.C(nome))[0]
        for v in (ent[nome]["amostra"], ent[nome]["invalido"]):
            if v is None:
                continue
            erros(f"{nome} = {v!r}", {TC.C(nome): v}, "@leve:" + aba if aba in porab_leve else "@aba:" + aba)
    n_inj = _injecoes(wb, erros, rng)
    r.info(f"requisito do Google: erro injetado em {n_inj} entradas, uma por vez (contador da Início = 1, aviso da "
           f"linha aceso, nenhuma outra célula com erro), e em todas ao mesmo tempo")
    listas = {"todas": todas, "alvo": alvo, **{f"leve:{a}": v for a, v in porab_leve.items()},
              **{f"aba:{a}": v for a, v in porab.items()}}
    paralelo.executar(r, tarefas, listas, progresso=lambda m: print(f"  … {time.strftime('%H:%M:%S')} {m}",
                                                                    flush=True))
    r.info("150 entradas × (válido, inválido); referência circular: o modelo do formulas carrega sem ciclo "
           "(finish() sem circular=True)")
    return r


def _injecoes(wb, erros, rng):
    """Requisito do Google (revisão 2 da ficha): o mestre digita "+1 em dois" e o Google mostra #ERROR! na célula.
    Injeta um valor de erro (#VALUE!/#N/A, como a formulas os produz) em cada entrada que alguma fórmula lê: todas as
    de lista, a semente, o nível e o nº de jogadores, um combatente do Combate, 10 vagas das listas editáveis, 10 de
    texto livre e 10 numéricas. Esperado: contador da Início = exatamente 1 (total e na aba), o aviso da linha aceso
    e nenhuma outra célula com erro (o contador soma ISERROR de todas as abas). Depois, todas ao mesmo tempo."""
    m = TC.mapa()
    cel, ent = m["celulas"], m["entradas"]
    camada_de = {}
    for cam, alvo in m["leitura"].items():
        camada_de.setdefault(alvo, []).append(cam)
    lidas = set(camada_de)          # entradas que alguma fórmula lê (pela camada de leitura protegida)
    # sinal -> aviso que o mostra (o mesmo critério do lint da ficha: "IF(<sinal>>0," no aviso da mesma aba)
    aviso_do = {}
    for aba, cs in m["avisos"].items():
        for c in cs:
            v = wb[aba][c].value or ""
            for s in m["sinais"]:
                a_, sc = TF.separar_ref(s)
                if a_ == aba and f"IF({sc}>0," in v:
                    aviso_do[s] = f"'{aba}'!{c}"
    sinal_de = {e: s for s, es in m["sinais"].items() for e in es}
    cont = {a: cel[f"inicio.erros.{N.SLUG[a]}"] for a in N.ABAS}
    tot = cel["inicio.erros.total"]
    # amostra representativa (decisão do orquestrador, iteração 2: 40 a 60 entradas; a prova de que TODA entrada passa
    # pela camada é a checagem estática do lint): uma entrada de cada lista distinta, em cada aba da Fase 1
    por_lista = {}
    for nm in sorted(ent):
        if ent[nm]["tipo"] == "lista" and cel[nm] in lidas:
            por_lista.setdefault((TF.separar_ref(cel[nm])[0], str(ent[nm].get("fonte"))), nm)
    escolha = list(por_lista.values())
    escolha += ["inicio.semente", "campanha.nivel", "campanha.jogadores", "combate.in1.troca", "combate.in1.pv"]
    escolha += rng.sample(sorted(n for n in ent if ent[n]["tipo"] == "texto" and cel[n] in lidas), 10)
    escolha += rng.sample(sorted(n for n in ent if ent[n]["tipo"] == "inteiro" and cel[n] in lidas
                                 and n not in escolha), 10)
    refs = list(dict.fromkeys(cel[n] for n in escolha))
    vagas = [f"'Tabelas'!{c}" for t in m["tabelas"].values()
             for c in t["vagas"] + t.get("ambientes", []) + t.get("segunda", [])]
    refs += rng.sample(sorted(v for v in vagas if v in lidas), 10)
    n = 0
    for k, ref in enumerate(refs):
        if ref not in lidas:
            continue
        aba = TF.separar_ref(ref)[0]
        codigo = "#VALUE!" if k % 2 == 0 else "#N/A"
        erros(f"erro {codigo} em {ref}", {ref: ["ERRO", codigo]}, [], cheios=[aviso_do[sinal_de[ref]]],
              msg_c="entrada com erro sem aviso na linha", iguais={tot: 1, cont[aba]: 1}, nao_erro=[])
        n += 1
    # todas as entradas e vagas ao mesmo tempo: cada aba conta exatamente as suas, nenhuma fórmula com erro
    todas_ent = sorted(lidas)
    por_aba = {}
    for x in todas_ent:
        por_aba[TF.separar_ref(x)[0]] = por_aba.get(TF.separar_ref(x)[0], 0) + 1
    iguais = {tot: len(todas_ent), **{cont[a]: por_aba.get(a, 0) for a in N.ABAS}}
    erros(f"erro em todas as {len(todas_ent)} entradas", {x: ["ERRO", "#VALUE!"] for x in todas_ent}, "@todas",
          iguais=iguais)
    return n


# ---------------------------------------------------------------------------
# estados da prévia
# ---------------------------------------------------------------------------

def _pior_caso(wb):
    import renderizar_ficha as R_
    mapa = TC.mapa()
    E = {}
    for k, (nome, info) in enumerate(sorted(mapa["entradas"].items())):
        ref = mapa["celulas"][nome]
        aba, cel = TF.separar_ref(ref)
        f = R_.fonte_da_celula(wb[aba][cel])
        if info["tipo"] == "lista":
            op = info.get("opcoes") or []
            if op:
                E[ref] = max(op, key=lambda s: f.getlength(str(s)))
        elif info["tipo"] == "inteiro":
            E[ref] = info["maximo"]
        else:
            E[ref] = N.texto_pior(int(info.get("maximo") or 40), 7 * k)
    return E


def estados(wb):
    from mestre import exemplo
    return {"em-branco": {}, "exemplo": TC.entradas(exemplo.entradas_nomes()), "pior-caso": _pior_caso(wb)}


def suite_preview(args):
    r = Resultado("preview")
    from PIL import Image
    wb = openpyxl.load_workbook(N.SAIDA_MODELO)
    for nome in list(wb.sheetnames):
        if nome not in N.ABAS_PRONTAS:
            del wb[nome]
    avisos = {N.MapaMestre.ref(a, c) for a, cs in TC.mapa()["avisos"].items() for c in cs}
    todas = [x for v in _formulas_por_aba(wb).values() for x in v]
    tmp = Path(tempfile.mkdtemp(prefix="mestre-preview-", dir=N.TEMP))
    try:
        saidas, cortes = {}, 0
        for est, E in estados(openpyxl.load_workbook(N.SAIDA_MODELO)).items():
            vals = TC.modelo().calcular(E, todas)
            r.ok(not _erros(vals), f"[{est}] erros: {_erros(vals)[:5]}")
            vals.update(E)
            s = R.renderizar_estado(wb, vals, avisos, tmp, est)
            saidas[est] = s
            for aba, (png, w, h, cts, partes) in s.items():
                cortes += len(cts)
                for ref, txt, motivo in cts[:30]:
                    r.falha(f"[{est}] texto cortado em {ref}: {motivo} — {txt[:70]!r}")
        PREVIEW.mkdir(parents=True, exist_ok=True)
        for antigo in list(PREVIEW.glob("*.png")) + list(PREVIEW.glob("indice-recortes.txt")):
            antigo.unlink()
        n = 0
        for est, s in saidas.items():
            for aba, (png, w, h, cts, partes) in s.items():
                for p, pw, ph, _ in partes:
                    with Image.open(p) as im:
                        r.ok(max(im.size) <= R.LADO_RECORTE, f"recorte maior que 1800 px: {p.name} {im.size}")
                    shutil.copy2(p, PREVIEW / p.name)
                    n += 1
        linhas = [f"Recortes 1:1 da prévia da Planilha do Mestre (≤ {R.LADO_RECORTE} px). arquivo · largura × altura · "
                  "intervalo", ""]
        for est, s in saidas.items():
            for aba, (png, w, h, cts, partes) in s.items():
                for p, pw, ph, iv in partes:
                    linhas.append(f"[{est}] {aba}: {p.name} · {pw} × {ph} · {iv}")
        (PREVIEW / "indice-recortes.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
        grandes = [p.name for p in PREVIEW.glob("*.png") if max(Image.open(p).size) > R.LADO_RECORTE]
        r.ok(not grandes and not list(PREVIEW.glob("*[!0-9].png")), f"PNG inteiro ou grande na pasta: {grandes[:4]}")
        r.info(f"{n} recortes (≤ 1800 px) de {len(N.ABAS_PRONTAS)} abas × 3 estados em {PREVIEW}; {cortes} texto(s) "
               f"cortado(s)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return r


def suite_visual(args):
    r = Resultado("visual")
    from openpyxl.utils import get_column_letter
    from openpyxl.utils.cell import range_boundaries
    wb = openpyxl.load_workbook(N.SAIDA_MODELO)
    todas = [x for v in _formulas_por_aba(wb).values() for x in v]
    mescla = {ws.title: R._mesclas(ws) for ws in wb.worksheets}
    oculta = lambda ws, rr, cc: bool(ws.column_dimensions[get_column_letter(cc)].hidden)  # noqa: E731
    ests = estados(wb)
    valores = {}
    nao, n = {}, 0
    for est, E in ests.items():
        v = TC.modelo().calcular(E, todas)
        v.update(E)
        valores[est] = v
        for ws in wb.worksheets:
            if ws.title not in N.ABAS_PRONTAS:
                continue
            topo, cob = mescla[ws.title]
            for linha in ws.iter_rows():
                for c in linha:
                    if (c.row, c.column) in cob or oculta(ws, c.row, c.column):
                        continue
                    ref = f"'{ws.title}'!{c.coordinate}"
                    x = c.value
                    if x is None or (isinstance(x, str) and x.startswith("=")):
                        x = v.get(ref)
                    s = R.texto_exibido(x)
                    if not s:
                        continue
                    n += 1
                    mot = R.medir(ws, c.row, c.column, s, topo)
                    if mot and ref not in nao:
                        nao[ref] = (est, s, mot)
    for ref, (est, s, mot) in sorted(nao.items())[:60]:
        r.falha(f"[{est}] não cabe em {ref}: {mot} — {s[:60]!r}")
    r.checagens += n
    r.info(f"(1) {n} textos medidos em 3 estados; {len(nao)} não couberam")
    # (2) listas: largura ≥ opção mais longa + 24 px
    nl = 0
    for ws in wb.worksheets:
        if ws.title not in N.ABAS_PRONTAS or ws.title == "Tabelas":
            continue
        topo, _ = mescla[ws.title]
        for dv in ws.data_validations.dataValidation:
            if dv.type != "list":
                continue
            fx = dv.formula1
            op = set()
            if fx.startswith('"'):
                op = set(fx.strip('"').split(","))
            else:
                aba, faixa = fx.rsplit("!", 1) if "!" in fx else (ws.title, fx)
                aba = aba.strip("'")
                c0, r0, c1, r1 = range_boundaries(faixa.replace("$", ""))
                for rr in range(r0, r1 + 1):
                    for cc in range(c0, c1 + 1):
                        k = f"'{aba}'!{wb[aba].cell(rr, cc).coordinate}"
                        for vv in valores.values():
                            s = R.texto_exibido(vv.get(k, wb[aba].cell(rr, cc).value if not str(
                                wb[aba].cell(rr, cc).value or "").startswith("=") else None))
                            if s:
                                op.add(s)
            for faixa in str(dv.sqref).split():
                c0, r0, c1, r1 = range_boundaries(faixa)
                for rr in range(r0, r1 + 1):
                    for cc in range(c0, c1 + 1):
                        cel = ws.cell(rr, cc)
                        f = R.fonte_da_celula(cel)
                        w, _ = R.area_px(ws, rr, cc, topo)
                        maior = max(op, key=f.getlength, default="")
                        nl += 1
                        if cel.alignment is not None and cel.alignment.wrap_text:
                            # com quebra de linha: o texto quebra na largura que sobra ao lado da seta e cabe na altura
                            util = w - R.RESERVA - R.SETA_LISTA
                            pior = max(op, key=lambda s: len(R.quebrar(s, f, util / R.FOLGA)), default="")
                            lin = R.quebrar(pior, f, util / R.FOLGA)
                            asc, desc = f.getmetrics()
                            h = R.area_px(ws, rr, cc, topo)[1]
                            ok = all(f.getlength(x) * R.FOLGA <= util for x in lin) and len(lin) * (asc + desc) + 2 <= h
                            r.ok(ok, f"lista em '{ws.title}'!{cel.coordinate}: {pior[:40]!r} não cabe ao lado da seta "
                                     f"({w} × {h} px)")
                        else:
                            r.ok(w >= f.getlength(maior) * R.FOLGA + R.SETA_LISTA,
                                 f"lista em '{ws.title}'!{cel.coordinate}: {w} px para {maior[:40]!r} + seta")
    r.info(f"(2) {nl} células com lista suspensa conferidas")
    # (4) avisos pela mensagem mais longa
    est = R.PiorTexto(wb, entradas_texto={k: R.texto_exibido(v) for k, v in ests["pior-caso"].items()})
    na = 0
    for aba, cels in TC.mapa()["avisos"].items():
        ws = wb[aba]
        topo, _ = mescla[aba]
        for cel in cels:
            s = est.formula(ws[cel].value, aba)
            if s:
                na += 1
                mot = R.medir(ws, ws[cel].row, ws[cel].column, s, topo)
                r.ok(mot is None, f"aviso mais longo não cabe em '{aba}'!{cel}: {mot} — {s[:60]!r}")
    r.info(f"(4) {na} avisos medidos pela mensagem mais longa")
    # (6) fonte ≥ 9 pt, (7) contraste ≥ 4,5:1, (8) ≤ 15 linhas do cabeçalho, (9) área ≤ 1360 px
    combos, peq = {}, []
    for ws in wb.worksheets:
        for linha in ws.iter_rows():
            for c in linha:
                if c.value is None and not R.eh_entrada(c):
                    continue
                if (c.font.sz or 10) < 9:
                    peq.append(f"{ws.title}!{c.coordinate}")
                fundo = R._rgb(c.fill.fgColor) if R.cor_fundo(c) else (255, 255, 255)
                cor = R._rgb(c.font.color, (0, 0, 0)) if c.font.color is not None else (0, 0, 0)
                combos.setdefault((cor, fundo), f"{ws.title}!{c.coordinate}")
    combos.setdefault(((0x9C, 0, 6), (0xFF, 0xC7, 0xCE)), "avisos")
    r.ok(not peq, f"fonte < 9 pt: {peq[:5]}")
    for (cor, fundo), onde in combos.items():
        r.ok(R.contraste(cor, fundo) >= 4.5, f"contraste {R.contraste(cor, fundo):.2f} em {onde}")
    for ws in wb.worksheets:
        if ws.title in ("Dados",):
            continue
        for t in R.tabelas(ws):
            if t["linhas"]:
                r.ok(t["linhas"][-1] - t["cab"] <= 15, f"{ws.title}: tabela da linha {t['cab']} vai até "
                                                        f"{t['linhas'][-1]}")
        if ws.title not in ("Tabelas",):
            r.ok(sum(R.px_coluna(ws, k) for k in range(1, 13)) <= N.LARGURA_TELA, f"{ws.title}: A:L > 1360 px")
    r.info(f"(6)(7) {len(combos)} combinações de cor com contraste ≥ 4,5:1 (menor "
           f"{min(R.contraste(a, b) for a, b in combos):.2f}:1); (8) tabelas a ≤ 15 linhas do cabeçalho; (9) A:L ≤ 1360 px")
    return r
