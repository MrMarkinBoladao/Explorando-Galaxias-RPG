# -*- coding: utf-8 -*-
"""
mestre_dados3.py — Dados do livro para a Fase 3 da Planilha do Mestre (design §4.1, §6.2–6.5, §6.13–6.15).

Escudo do Mestre (16.2, 17.2, 19.3–19.7, 20.2–20.6, 21.5, 23.3–23.6, 27.2–27.5, 27.9, 27.10, 28.2–28.4, 29.12),
Improviso (24.1–24.3 na loja, 27.2 na DT rápida), Campanha (26.1, 26.7) e Mundos (27.16, 27.17). Reaproveita os
parsers de build\\ficha_dados.py por import (a ficha não é editada). Toda leitura falha alto, com capítulo e seção.
mestre_dados.blocos()/listas() chamam blocos3()/listas3() no fim (o arquivo de lá já passa de 50 KB).
"""

import re
from functools import lru_cache

import ficha_dados as F

FAIXAS = ["1-4", "5-8", "9-12", "13-16", "17-20"]


def _erro(cap, sec, msg):
    raise ValueError(f"cap {cap}, seção {sec}: {msg}")


def _tab(cap, sec, primeira, colunas=None):
    try:
        cab, corpo = F.tabela(cap, sec, primeira)
    except ValueError as e:
        _erro(cap, sec, str(e))
    if colunas is not None and cab[:len(colunas)] != colunas:
        _erro(cap, sec, f"tabela '{primeira}' com colunas {cab} (esperado {colunas})")
    if not corpo:
        _erro(cap, sec, f"tabela '{primeira}' vazia")
    return cab, corpo


def _numerada(cap, sec, n):
    """Os n itens da primeira lista numerada (1. 2. …) da seção, sem a marcação."""
    itens = []
    for l in F.secao(cap, sec):
        m = re.match(r"^(\d+)\. (.+)$", l)
        if m and int(m.group(1)) == len(itens) + 1:
            itens.append(F.limpar(m.group(2)))
            if len(itens) == n:
                return itens
        elif itens and l.strip() and not m:
            break
    _erro(cap, sec, f"lista numerada com {len(itens)} itens (esperado {n})")


def _marcadores(cap, sec, n, ate=None):
    """Os n primeiros itens de lista com '- ' da seção (para antes de uma linha que começa com `ate`)."""
    itens = []
    for l in F.secao(cap, sec):
        if ate and l.startswith(ate):
            break
        if l.startswith("- "):
            itens.append(F.limpar(l[2:]))
    if len(itens) < n:
        _erro(cap, sec, f"{len(itens)} itens de lista (esperado {n})")
    return itens[:n]


def _citacao(cap, sec, comeca):
    """O parágrafo de citação ('> ') da seção que começa com `comeca` (depois de limpar)."""
    for l in F.secao(cap, sec):
        if l.startswith(">"):
            t = F.limpar(l.lstrip("> "))
            if t.startswith(comeca):
                return t
    _erro(cap, sec, f"citação '{comeca}' não encontrada")


def _frase(cap, sec, contem):
    """A frase (até o ponto) de um parágrafo da seção que contém `contem`."""
    for l in F.secao(cap, sec):
        t = F.limpar(l.lstrip("> "))
        if t.startswith("- "):
            t = t[2:]
        i = t.find(contem)
        if i >= 0:
            ini = t.rfind(". ", 0, i)
            ini = ini + 2 if ini >= 0 else 0
            prof, fim = 0, len(t)
            for k in range(i + len(contem) - 1, len(t)):      # o ponto final fora de parênteses
                if t[k] == "(":
                    prof += 1
                elif t[k] == ")":
                    prof -= 1
                elif t[k] == "." and prof <= 0 and (k + 1 == len(t) or t[k + 1] == " "):
                    fim = k + 1
                    break
            return t[ini:fim].strip()
    _erro(cap, sec, f"frase com '{contem}' não encontrada")


# ---------------------------------------------------------------------------
# Tabelas
# ---------------------------------------------------------------------------

@lru_cache(None)
def ultimate_faixa():
    """27.9 'Aprovar uma Ultimate': faixa, Nível equivalente, Dano e Cura (expressão e média)."""
    _, corpo = _tab("27", "### Aprovar uma Ultimate", "Faixa", ["Faixa", "Nível equivalente", "Dano", "Cura"])
    saida = []
    for l in corpo:
        dm = re.fullmatch(r"(\d+d\d+) \((\d+)\)", l[2])
        cm = re.fullmatch(r"(\d+d\d+) \((\d+)\)", l[3])
        if not dm or not cm:
            _erro("27", "27.9", f"linha da Ultimate fora do formato: {l}")
        saida.append({"faixa": l[0], "nivel": int(l[1]), "dano_e": dm.group(1), "dano_m": int(dm.group(2)),
                      "cura_e": cm.group(1), "cura_m": int(cm.group(2))})
    if [x["faixa"] for x in saida] != FAIXAS:
        _erro("27", "27.9", "faixas da Ultimate fora da ordem 1-4 … 17-20")
    return saida


@lru_cache(None)
def descanso_curto():
    """23.6: PV por Descanso Curto (Vigor +2) nos níveis 3, 7, 11, 15, 19."""
    cab, corpo = _tab("23", "## 23.6", "Nível")
    return [(int(n), int(v)) for n, v in zip(cab[1:], corpo[0][1:])]


@lru_cache(None)
def pv_temporarios():
    """23.3: teto de PV temporários por faixa de níveis."""
    cab, corpo = _tab("23", "## 23.3", "Nível")
    saida = []
    for faixa, v in zip(cab[1:], corpo[0][1:]):
        a, b = (int(x) for x in faixa.split("-"))
        saida.append((faixa, a, b, int(v)))
    return saida


def ritmo():
    """26.1: 'Ritmo sugerido: 2 a 4 sessões por nível nos níveis 1 a 8; 4 a 6 sessões por nível daí em diante.'"""
    t = " ".join(F.limpar(l) for l in F.secao("26", "## 26.1"))
    m = re.search(r"Ritmo sugerido: (\d+) a (\d+) sessões por nível nos níveis 1 a (\d+); (\d+) a (\d+) sessões por "
                  r"nível daí em diante", t)
    if not m:
        _erro("26", "26.1", "ritmo sugerido não encontrado")
    a, b, ate, c, d = (int(x) for x in m.groups())
    return [(1, ate, a, b, f"{a} a {b} sessões por nível (níveis 1 a {ate})"),
            (ate + 1, 20, c, d, f"{c} a {d} sessões por nível (do nível {ate + 1} em diante)")]


def tetos():
    """29.12 'Tetos que a mesa esquece' (itens separados por ·)."""
    for l in F.secao("29", "## 29.12"):
        t = F.limpar(l)
        if t.startswith("Tetos que a mesa esquece:"):
            itens = [x.strip().rstrip(".") for x in t.split(":", 1)[1].split("·")]
            if len(itens) != 7:
                _erro("29", "29.12", f"{len(itens)} tetos (esperado 7)")
            return itens
    _erro("29", "29.12", "linha 'Tetos que a mesa esquece' não encontrada")


@lru_cache(None)
def faccoes_uso():
    """27.16: cada facção e o seu 'Como usar'."""
    saida, atual = [], None
    for l in F.secao("27", "## 27.16"):
        if l.startswith("### "):
            atual = l[4:].strip()
        t = F.limpar(l)
        if atual and t.startswith("Como usar:"):
            saida.append((atual, t[len("Como usar:"):].strip()))
    if len(saida) != 8:
        _erro("27", "27.16", f"{len(saida)} facções com 'Como usar' (esperado 8)")
    return saida


def exemplos_armas():
    """24.2 'Exemplos de cada categoria'."""
    for cab, corpo in F.tabelas(F.secao("24", "## 24.2")):
        if cab[:2] == ["Categoria", "Exemplos"]:
            return {l[0]: l[1] for l in corpo}
    _erro("24", "24.2", "tabela de exemplos das armas não encontrada")


# Loja (G = 620): tipos de loja e o estoque de cada um, só com linhas do livro (24.1 armaduras, 24.2 armas, 24.3 poções
# e itens) e o preço do livro. Que linhas cabem em cada tipo de loja é Sugestão da planilha (H15).
TIPOS_LOJA = ["Armas", "Armaduras", "Suprimentos", "Farmácia", "Mercado geral", "Mercado da Frota de Jade"]
_LOJA_ITENS = {
    "Armaduras": ["Kit de ferramentas", "Traje de vedação", "Munição ou célula de reserva"],
    "Farmácia": ["Kit de primeiros socorros (3 usos)", "Kit de pesquisa de campo", "Ração de viagem (3 dias)"],
    "Armas": ["Munição ou célula de reserva"],
}


@lru_cache(None)
def loja():
    """[(tipo de loja, ordem, item, preço, o que é, espaço)] na ordem de 24.1, 24.2, 24.3."""
    ex = exemplos_armas()
    armas = [(f"Arma {a['categoria']}", a["preco"], f"{a['dados']}, {a['alcance']}, {a['atributo']}; ex.: "
              f"{ex[a['categoria']]}", a["espaco"]) for a in F.armas()]
    armaduras = [(f"Armadura {a['tipo']}", a["preco"], f"Defesa +{a['defesa']}" +
                  ("" if a["outros"] in ("—", "") else f"; {a['outros']}"), a["espaco"]) for a in F.armaduras()]
    pocoes = [(f"Poção {p['pocao']}", p["preco"], f"Cura {p['cura']}", p["espaco"]) for p in F.pocoes()]
    itens = [(i["item"], i["preco"], i["uso"], i["espaco"]) for i in F.itens()]
    por_nome = {x[0]: x for x in armas + armaduras + pocoes + itens}
    pools = {
        "Armas": armas + [por_nome[n] for n in _LOJA_ITENS["Armas"]],
        "Armaduras": armaduras + [por_nome[n] for n in _LOJA_ITENS["Armaduras"]],
        "Suprimentos": itens,
        "Farmácia": pocoes + [por_nome[n] for n in _LOJA_ITENS["Farmácia"]],
        "Mercado geral": armas + armaduras + pocoes + itens,
        "Mercado da Frota de Jade": armas + armaduras + pocoes + itens,
    }
    saida = []
    for t in TIPOS_LOJA:
        if len(pools[t]) < 6:
            raise ValueError(f"H15: a loja '{t}' tem {len(pools[t])} itens (mínimo 6 para o estoque)")
        for k, (item, preco, oque, esp) in enumerate(pools[t], start=1):
            saida.append((t, k, f"{t}|{k}", item, preco, oque, esp))
    return saida


ORACULO_PROB = [("Quase impossível", -6), ("Improvável", -3), ("Meio a meio", 0), ("Provável", 3),
                ("Quase certo", 6)]                                                   # H10 (sem "50/50": o Google lê data)
REPUTACAO = [(-3, "−3 Inimiga declarada"), (-2, "−2 Hostil"), (-1, "−1 Desconfiada"), (0, "0 Neutra"),
             (1, "+1 Simpática"), (2, "+2 Amiga"), (3, "+3 Aliada")]                 # H17
SEGMENTOS = [4, 6, 8, 10, 12]                                                         # H16
FACES = [2, 4, 6, 8, 10, 12, 20, 100]                                                 # 02 (dados do livro)
TIPOS_CENA = ["Social", "Exploração", "Combate", "Viagem", "Descanso"]                # 6.4
ESTADOS_MISSAO = ["Oferecida", "Ativa", "Concluída", "Falhou", "Abandonada"]          # 6.5
ONDE_EVENTO = ["Viagem", "Espaço", "Cidade"]                                          # 6.14


def textos():
    """Trechos de regra do livro que o Escudo do Mestre mostra (id, seção, texto limpo)."""
    T = []
    for k, t in enumerate(_numerada("19", "## 19.3", 4), start=1):
        T.append((f"fila.{k}", "19.3", t))
    for k, t in enumerate(_numerada("19", "### Surpresa", 2), start=1):
        T.append((f"surpresa.{k}", "19.3", t))
    for k, t in enumerate(_numerada("19", "## 19.4", 4), start=1):
        T.append((f"firmeza.{k}", "19.4", t))
    T.append(("avancar", "19.5", _citacao("19", "## 19.5", "Avançar em N casas:")))
    T.append(("avanco_total", "19.5", _citacao("19", "## 19.5", "Avanço Total:")))
    T.append(("congelamento.elite", "19.6", _citacao("19", "## 19.6", "Elite e Boss não perdem o turno")))
    for k, t in enumerate(_numerada("20", "## 20.4", 5), start=1):
        T.append((f"quebra.{k}", "20.4", t))
    for k, t in enumerate(_marcadores("20", "## 20.6", 5, ate="*Por quê"), start=1):
        T.append((f"dc.{k}", "20.6", t))
    T.append(("tenacidade.acerto", "20.3", _citacao("20", "## 20.3", "A Redução de Tenacidade é condicionada")))
    T.append(("contrato", "27.5", _citacao("27", "## 27.5", "Monte o encontro")))
    T.append(("regra_irma", "27.5", _frase("27", "## 27.5", "nunca aponte uma Resistência")))
    for nome in ("Ataque normal:", "Ação especial de dano:", "Ação especial de controle:"):
        T.append((f"regua.{nome.split()[-1].rstrip(':')}", "28.4", _citacao("28", "## 28.4", nome)))
    T.append(("morrendo", "23.4", _citacao("23", "## 23.4", "Este Teste soma só")))
    T.append(("executado", "23.5", _citacao("23", "## 23.5", "Executado:")))
    for k, t in enumerate(_numerada("23", "## 23.5", 4), start=1):
        T.append((f"executado.{k}", "23.5", t))
    T.append(("pv_temp", "23.3", _citacao("23", "## 23.3", "Teto global de PV temporários")))
    T.append(("ph", "16.2", _citacao("16", "## 16.2", "Máximo de PH")))
    T.append(("ph_ganho", "16.2", _citacao("16", "## 16.2", "Cada Ataque Básico que acerta gera")))
    T.append(("energia", "17.2", _citacao("17", "## 17.2", "A Energia é da ação, não do acerto.")))
    for k, t in enumerate(_marcadores("27", "### Aprovar uma Ultimate", 4), start=1):
        T.append((f"ultimate.{k}", "27.9", t))
    T.append(("rolagem", "29.12", _frase("29", "## 29.12", "A rolagem única:")))
    T.append(("falhe", "27.1", _frase("27", "## 27.1", "falha em Teste de Perícia nunca trava a cena")))
    T.append(("regra_ouro", "27.1", _frase("27", "## 27.1", "Se uma regra deste livro estiver atrapalhando")))
    T.append(("perguntas", "27.17", _frase("27", "## 27.17", "Montar um lugar seu, em três perguntas:")))
    T.append(("viagem", "27.15", _frase("27", "## 27.15", "Regras de nave, rota e viagem interestelar não estão")))
    T.append(("viagem_cena", "27.15", _frase("27", "## 27.15", "Se a sua mesa quiser fazer da viagem um desafio")))
    T.append(("servicos", "24.5", _frase("24", "## 24.5", "Serviços e ficção")))
    T.append(("precos", "24.5", _frase("24", "## 24.5", "Uma pistola custa 250 Cr")))
    T.append(("sem_reliquia", "24.5", _frase("24", "## 24.5", "Cones de Luz e Relíquias são recompensas de marco")))
    for k, t in enumerate(_numerada("03", "## Antes de jogar", 5), start=1):     # a base da Sessão Zero
        T.append((f"mesa.{k}", "03", t))
    T.append(("marco", "26.1", _citacao("26", "## 26.1", "Progressão por marco narrativo.")))
    T.append(("expresso", "27.15", _numerada("27", "## 27.15", 3)[0]))
    for l in F.secao("27", "## 27.2"):                   # as três regras que acompanham a tabela de DT
        m = re.match(r"^\*\*([123])\. (.+?)\*\*", l)
        if m:
            T.append((f"dt.{m.group(1)}", "27.2", F.limpar(m.group(2))))
    if sum(1 for t in T if t[0].startswith("dt.")) != 3:
        _erro("27", "27.2", "as três regras da tabela de DT não foram encontradas")
    T.append(("congelamento.comum", "19.6", _marcadores("19", "## 19.6", 1)[0]))
    T.append(("intervir", "23.5", _frase("23", "## 23.5", "Intervir cancela a Execução")))
    T.append(("sem_compra", "27.8", _citacao("27", "## 27.8", "Não existe compra de Relíquia")))
    return T


# ---------------------------------------------------------------------------
# Blocos da aba Dados e listas de validação (chamados por mestre_dados.blocos()/listas())
# ---------------------------------------------------------------------------

def blocos3(bloco):
    bloco("dt_subsistema", "As cinco DTs de subsistema — 27.3", ["Teste", "DT", "Capítulo"],
          [[d["teste"], d["dt"], d["capitulo"]] for d in F.dt_subsistema()], "27.3")
    bloco("ultimate_faixa", "Aprovar uma Ultimate: o Nível equivalente da faixa — 27.9",
          ["Faixa", "Nível equivalente", "Dano", "Média do dano", "Cura", "Média da cura"],
          [[u["faixa"], u["nivel"], u["dano_e"], u["dano_m"], u["cura_e"], u["cura_m"]] for u in ultimate_faixa()],
          "27.9")
    bloco("energia", "De onde vem a Energia — 17.2", ["Fonte", "Energia", "Limite"],
          [[e["fonte"], e["energia"], e["limite"]] for e in F.energia()], "17.2")
    _, c = _tab("19", "## 19.4", "Tipo de alvo", ["Tipo de alvo", "Teto", "Firmeza"])
    bloco("teto_atraso", "Teto de Atraso por alvo, por Ciclo — 19.4", ["Tipo de alvo", "Teto", "Firmeza"], c, "19.4")
    _, c = _tab("19", "## 19.7", "Situação", ["Situação", "Resolução"])
    bloco("casos_fila", "Casos-limite da Fila — 19.7", ["Situação", "Resolução"], c, "19.7")
    bloco("fraqueza_resistencia", "Fraqueza, neutro e Resistência — 20.2", ["Situação", "Dano", "Redução de Tenacidade"],
          [[f["situacao"], f["dano"], f["rt"]] for f in F.fraqueza_resistencia()], "20.2")
    bloco("tenacidade_livro", "Redução de Tenacidade por fonte — 20.3 (a tabela do livro)",
          ["Fonte", "Redução de Tenacidade"], [[t["fonte"], t["rt"]] for t in F.tenacidade()], "20.3")
    _, c = _tab("23", "## 23.4", "Resultado", ["Resultado", "Efeito"])
    bloco("morrendo", "O contador do Morrendo — 23.4", ["Resultado", "Efeito"], c, "23.4")
    _, c = _tab("23", "## 23.6", "Tipo", ["Tipo", "Tempo", "Quantas", "Recupera"])
    bloco("descanso", "Descanso — 23.6", ["Tipo", "Tempo", "Quantas", "Recupera"], c, "23.6")
    bloco("descanso_curto", "PV por Descanso Curto (Vigor +2) — 23.6", ["Nível", "PV"], descanso_curto(), "23.6")
    bloco("pv_temp", "Teto de PV temporários — 23.3", ["Níveis", "Do nível", "Ao nível", "Teto"], pv_temporarios(),
          "23.3")
    _, c = _tab("27", "## 27.10", "Operação", ["Operação", "Quando falha", "O que acontece"])
    bloco("casos_mesa", "Casos-limite de mesa — 27.10", ["Operação", "Quando falha", "O que acontece"], c, "27.10")
    _, c = _tab("28", "## 28.2", "Tipo", ["Tipo", "Por turno", "Por Ciclo, na prática"])
    bloco("acoes_tipo", "Ações agressivas por tipo — 28.2 regra 5", ["Tipo", "Por turno", "Por Ciclo, na prática"], c,
          "28.2")
    bloco("tetos", "Tetos que a mesa esquece — 29.12", ["Teto"], [[t] for t in tetos()], "29.12")
    bloco("ritmo", "Ritmo sugerido de sessões por nível — 26.1", ["Do nível", "Ao nível", "Mínimo", "Máximo", "Texto"],
          ritmo(), "26.1")
    bloco("faccoes_uso", "Facções: como usar — 27.16", ["Facção", "Como usar"], [list(x) for x in faccoes_uso()],
          "27.16")
    _, c = _tab("27", "## 27.17", "Lugar", ["Lugar", "O que é", "A cena que ele entrega"])
    bloco("locais_livro", "Locais — 27.17", ["Lugar", "O que é", "A cena que ele entrega"], c, "27.17")
    bloco("textos", "Trechos de regra que o Escudo do Mestre mostra — vários capítulos", ["Chave", "Seção", "Texto"],
          [[f"T{k:02d}", s, t] for k, (_, s, t) in enumerate(textos(), start=1)], "Escudo")
    lj = loja()
    bloco("loja", "Estoque das lojas — 24.1 a 24.3 (que linha cabe em cada loja: Sugestão da planilha, H15)",
          ["Tipo de loja", "Ordem", "Chave", "Item", "Preço (Cr)", "O que é", "Espaço"], [list(x) for x in lj], "24.1")
    bloco("loja_tipos", "Tipos de loja — H15 (Sugestão da planilha)", ["Tipo de loja", "Nº de itens", "Índice"],
          [[t, sum(1 for x in lj if x[0] == t), k + 1] for k, t in enumerate(TIPOS_LOJA)], "H15")
    bloco("oraculo_prob", "Oráculo sim/não: modificador do d20 — H10 (Sugestão da planilha)",
          ["Probabilidade", "Modificador"], [list(x) for x in ORACULO_PROB], "H10")
    bloco("reputacao", "Reputação −3 a +3 — H17 (Sugestão da planilha)", ["Atitude", "Leitura"],
          [list(x) for x in REPUTACAO], "H17")


def listas3(lista):
    lista("estado_missao", "Estado da missão", "6.5", ESTADOS_MISSAO)
    lista("tipo_cena", "Tipo de cena", "6.4", TIPOS_CENA)
    lista("encontro_ligado", "Encontro ligado", "6.4", ["Nenhum", "A", "B", "C"])
    lista("dificuldades", "Dificuldade", "27.2", [l[0] for l in F.dt_faixa()[1]])
    lista("segmentos", "Segmentos do relógio", "Sugestão da planilha (H16)", SEGMENTOS)
    lista("reputacao", "Atitude (−3 a +3)", "Sugestão da planilha (H17)", [v for v, _ in REPUTACAO])
    lista("tipo_nome", "Tipo de nome", "29.11", ["Facção", "Lugar", "Pessoa", "Outro"])
    lista("onde_evento", "Onde (evento)", "6.14", ["Sortear"] + ONDE_EVENTO)
    lista("tipo_loja", "Tipo de loja", "Sugestão da planilha (H15)", ["Sortear"] + TIPOS_LOJA)
    lista("probabilidade", "Probabilidade", "Sugestão da planilha (H10)", [p for p, _ in ORACULO_PROB])
    lista("faces", "Faces do dado", "02", FACES)
    lista("vantagem", "Vantagem", "02", ["Normal", "Vantagem", "Desvantagem"])


# Ids estáveis dos geradores da Fase 3 (design §5). Nunca reaproveitar um G.
GERADORES3 = {
    510: {"nome": "Planeta ou local", "aba": "Mundos",
          "campos": {1: "tipo", 2: "condição", 3: "Caminho que vence", 4: "manhã", 5: "o que pararam",
                     6: "presença", 7: "facção presente", 8: "nome (início)", 9: "nome (fim)"}},
    520: {"nome": "Estação", "aba": "Mundos",
          "campos": {1: "função", 2: "dono", 3: "problema", 4: "nome (início)", 5: "nome (fim)"}},
    530: {"nome": "Nave", "aba": "Mundos",
          "campos": {1: "nome (início)", 2: "nome (fim)", 3: "classe", 4: "peculiaridade", 5: "tripulação",
                     6: "ocupação a bordo"}},
    540: {"nome": "Facção nova", "aba": "Mundos",
          "campos": {1: "nome (início)", 2: "nome (fim)", 3: "Caminho", 4: "o que quer", 5: "método", 6: "recurso",
                     7: "como usar"}},
    550: {"nome": "Organização", "aba": "Mundos",
          "campos": {1: "organização", 2: "Raça do líder", 3: "nome do líder", 4: "sobrenome do líder", 5: "oferece",
                     6: "cobra", 7: "sede (início)", 8: "sede (fim)"}},
    560: {"nome": "Nomes avulsos", "aba": "Mundos",
          "campos": {1: "cultura", 2: "nome", 3: "sobrenome", 4: "lugar (início)", 5: "lugar (fim)", 6: "nave (início)",
                     7: "nave (fim)", 8: "organização"}},
    600: {"nome": "Rumor", "aba": "Improviso",
          "campos": {1: "rumores (início da sequência)", 2: "veracidade 1", 3: "veracidade 2", 4: "veracidade 3",
                     5: "gancho do livro", 6: "gancho da tabela"}},
    610: {"nome": "Evento ou complicação", "aba": "Improviso",
          "campos": {1: "onde", 2: "evento", 3: "complicação", 4: "custo da falha"}},
    620: {"nome": "Loja", "aba": "Improviso",
          "campos": {1: "tipo de loja", 2: "estoque (início da sequência)", **{2 + k: f"quantidade {k}" for k in
                                                                               range(1, 7)},
                     9: "Raça do lojista", 10: "nome do lojista", 11: "sobrenome do lojista", 12: "maneirismo",
                     13: "item fora do comum"}},
    630: {"nome": "Bugiganga", "aba": "Improviso", "campos": {1: "bugigangas (início da sequência)"}},
    640: {"nome": "Oráculo sim/não", "aba": "Improviso", "campos": {1: "d20"}},
    650: {"nome": "Rolador de dados", "aba": "Improviso",
          "campos": {20 * (e - 1) + d: f"expressão {e}, dado {d}" for e in range(1, 4) for d in range(1, 21)}},
    **{700 + t: {"nome": f"Minhas Tabelas {t}", "aba": "Minhas Tabelas", "campos": {1: "início da sequência"}}
       for t in range(1, 11)},
}
