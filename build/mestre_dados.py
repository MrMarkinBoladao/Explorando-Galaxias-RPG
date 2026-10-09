# -*- coding: utf-8 -*-
"""
mestre_dados.py — Dados do livro para a Planilha do Mestre (design §3.1, §4.1).

Parsers dos capítulos 28 (28.3 âncoras e dano em dados; 28.6–28.10 as 32 fichas com campos, fases e
ações; 28.11 índice e composições) e 27 (27.4 orçamento e composições, 27.7 attrition, 27.16 facções,
27.17 locais, 27.18 ganchos), mais o que reaproveita de build\\ficha_dados.py (19–25) por import.
Toda leitura falha alto (ValueError com capítulo e seção). Número de ficha que não bate com a âncora
de 28.3 é FATAL (plano P13), salvo as entradas de DIVERGENCIAS_DOCUMENTADAS.

Expõe: ancoras(), dano_dados(), dano_especial(), bestiario(), fases(), acoes(), orcamento(),
composicoes(), attrition(), faccoes(), locais(), ganchos(), blocos(), listas(), GERADORES.
"""

import re
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ficha_dados as F  # noqa: E402

FAIXAS = ["1-4", "5-8", "9-12", "13-16", "17-20"]
ROTULOS_FAIXA = [f"Faixa {fx}" for fx in FAIXAS]     # opções das listas suspensas (o Google lê "1-4" como data)
TIPOS = ["Comum", "Elite", "Boss"]
NIVEL_REFERENCIA = {"1-4": 3, "5-8": 7, "9-12": 11, "13-16": 15, "17-20": 19}     # 29.1 / 27.7
ELEMENTOS = ["Físico", "Fogo", "Gelo", "Raio", "Vento", "Quântico", "Imaginário"]      # 20.1

# Ids estáveis dos geradores e campos (design §5). Nunca reaproveitar um G.
GERADORES = {
    100: {"nome": "Encontro aleatório", "aba": "Encontros",
          "campos": {1: "composição", **{1 + k: f"vaga {k}" for k in range(1, 8)}}},
    110: {"nome": "Fraquezas sugeridas (Criador de Inimigos)", "aba": "Inimigos",
          "campos": {10 * i + e: f"linha {i}, Elemento {e}" for i in range(1, 13) for e in range(1, 8)}},
    # Fase 2 (design §5, §6.6, §6.11, §6.12)
    200: {"nome": "NPC", "aba": "NPCs",
          "campos": {1: "Raça", 2: "nome", 3: "sobrenome", 4: "Caminho", 5: "ocupação", 6: "aparência 1",
                     7: "aparência 2", 8: "personalidade", 9: "motivação", 10: "segredo", 11: "maneirismo",
                     12: "atitude", 13: "gancho", 14: "fonte do gancho (H20)", 15: "papel"}},
    300: {"nome": "Aventura", "aba": "Aventuras",
          "campos": {1: "tipo", 2: "gancho", 3: "facção do contratante", 4: "Raça do contratante", 5: "objetivo",
                     6: "local", 7: "antagonista (H22)", 8: "complicação", 9: "reviravolta", 10: "prazo",
                     11: "composição da cena 3", 12: "cena 4: encontro ou objetivo", 13: "consumível (H9)",
                     14: "pista", 15: "fonte do gancho (H20)", 16: "ocupação do contratante",
                     17: "nome do contratante", 18: "fonte do local (H26)", 19: "objetivo sem matar (27.7)",
                     20: "facção do conflito", 21: "sobrenome do contratante"}},
    400: {"nome": "Recompensa de encontro", "aba": "Recompensas",
          "campos": {1: "quantidade de consumíveis (H9)", 2: "consumível 1", 3: "consumível 2", 4: "bugiganga",
                     5: "pista"}},
    410: {"nome": "Cone de Luz (sabor)", "aba": "Recompensas",
          "campos": {1: "nome (início)", 2: "nome (fim)", 3: "memória", 4: "Bônus Maior", 5: "gatilho 1",
                     6: "gatilho 2"}},
    420: {"nome": "Conjunto de Relíquias (sabor)", "aba": "Recompensas",
          "campos": {1: "nome", 2: "origem", 3: "bônus de 2 peças", 4: "efeito de 4 peças"}},
}
import mestre_dados3 as _D3  # noqa: E402  (Fase 3: G = 510…650 e 701…710)
GERADORES.update(_D3.GERADORES3)

# Divergências entre fichas e âncoras de 28.3 — registradas, não corrigidas (o livro não se edita).
# (seção, criatura, campo, valor do livro, o que a planilha mostra)
DIVERGENCIAS_DOCUMENTADAS = [
    ("28.8", "O Dramaturgo de Mil Faces", "Tenacidade da fase 2", 9,
     "9 (abaixo da âncora 12; 28.5 regra 3 permite cair)"),
    ("28.10", "O Germe de Pavor", "Tenacidade da fase 3", 10,
     "10 (abaixo da âncora 13; 28.5 regra 3 permite cair)"),
    ("28.10", "Vazia Coroada", "Tenacidade da fase 2", 12,
     "12 (abaixo da âncora 13; 28.5 regra 3 permite cair)"),
    ("28.10", "Vazia Coroada", "Tenacidade da fase 3", 10,
     "10 (abaixo da âncora 13; 28.5 regra 3 permite cair)"),
]


def _erro(sec, msg):
    raise ValueError(f"cap 28, seção {sec}: {msg}")


def _num(s):
    v = F.num(s)
    if v is None:
        raise ValueError(f"número esperado, veio {s!r}")
    return v


def dados_de(expr):
    """'4d8 + 2' -> (4, 8, 2); '1d6' -> (1, 6, 0)."""
    m = re.fullmatch(r"(\d+)d(\d+)(?: \+ (\d+))?", expr.strip())
    if not m:
        raise ValueError(f"expressão de dano fora do formato: {expr!r}")
    return int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)


def media(n, f, fixo):
    """Capítulo 02 / 28.3: n × (lados + 1) ÷ 2, arredondado para baixo, + fixo."""
    return (n * (f + 1)) // 2 + fixo


# ---------------------------------------------------------------------------
# 28.3 — âncoras e dano em dados
# ---------------------------------------------------------------------------

@lru_cache(None)
def ancoras():
    tabs = F.tabelas(F.secao("28", "## 28.3"))
    if len(tabs) < 2:
        _erro("28.3", "as duas tabelas (âncoras e dano em dados) não foram encontradas")
    cab, corpo = tabs[0]
    esperado = ["Faixa", "PV Comum", "PV Elite", "PV Boss", "Defesa C / E / B", "RD C / E / B",
                "Tenacidade C / E / B", "VEL C / E / B", "Ataque", "Dano por acerto C / E / B",
                "DT dos efeitos C / E / B", "Teste de Resistência C / E / B", "Fraquezas C / E / B"]
    if cab != esperado:
        _erro("28.3", f"colunas da tabela de âncoras diferentes do esperado: {cab}")
    _, dd = tabs[1]
    dano = {}
    for l in dd:
        for j, tipo in enumerate(TIPOS, start=1):
            expr, med = [x.strip() for x in l[j].split("·")]
            n, f, fixo = dados_de(expr)
            if media(n, f, fixo) != _num(med):
                _erro("28.3", f"média impressa {med} ≠ {n}d{f}+{fixo} na faixa {l[0]} {tipo}")
            dano[(l[0], tipo)] = (expr, n, f, fixo, _num(med))
    saida = []
    for l in corpo:
        fx = l[0]
        if fx not in FAIXAS:
            _erro("28.3", f"faixa desconhecida {fx}")
        tri = {k: [x.strip() for x in l[i].split("/")] for k, i in
               (("def", 4), ("rd", 5), ("ten", 6), ("vel", 7), ("dano", 9), ("dt", 10), ("tr", 11), ("fr", 12))}
        for j, tipo in enumerate(TIPOS):
            expr, n, f, fixo, med = dano[(fx, tipo)]
            if med != _num(tri["dano"][j]):
                _erro("28.3", f"Dano por acerto {tri['dano'][j]} ≠ média em dados {med} ({fx} {tipo})")
            saida.append({
                "faixa": fx, "tipo": tipo, "chave": f"{fx}|{tipo}", "pv": _num(l[1 + j]),
                "defesa": _num(tri["def"][j]), "rd": _num(tri["rd"][j]), "ten": _num(tri["ten"][j]),
                "vel": _num(tri["vel"][j]), "ataque": _num(l[8]), "dano_expr": expr, "dano_n": n, "dano_f": f,
                "dano_fixo": fixo, "dano_media": med, "dt": _num(tri["dt"][j]), "tr": _num(tri["tr"][j]),
                "nfraq": tri["fr"][j], "nfraq_sug": {"Comum": 2, "Elite": 3, "Boss": 4}[tipo],
                "firmeza": "sem Firmeza" if tipo == "Comum" else "com Firmeza",          # 28.2 regra 3
                "acoes": {"Comum": 1, "Elite": 1.5, "Boss": 2}[tipo],                      # 28.2 regra 5
                "teto_atraso": 3 if tipo == "Comum" else 2,                                # 19.4
            })
    if len(saida) != 15:
        _erro("28.3", f"esperava 15 âncoras, vieram {len(saida)}")
    return saida


def ancora(faixa, tipo):
    for a in ancoras():
        if a["faixa"] == faixa and a["tipo"] == tipo:
            return a
    raise KeyError((faixa, tipo))


# H2: dano de ação especial 1,5× (28.4 regra 5). "ficha" = expressão impressa numa ficha do livro
# (conferida no .md pela suíte bestiario); "Sugestão" = dados normais do tipo + fixo até INT(1,5 × média).
DANO_ESPECIAL = {
    ("1-4", "Comum"): ("1d6 + 1", "Sugestão da planilha (H2)", ""),
    ("5-8", "Comum"): ("2d6 + 3", "Sugestão da planilha (H2)", ""),
    ("9-12", "Comum"): ("2d8 + 4", "Sugestão da planilha (H2)", ""),
    ("13-16", "Comum"): ("3d6 + 8", "Sugestão da planilha (H2)", ""),
    ("17-20", "Comum"): ("3d8 + 11", "Sugestão da planilha (H2)", ""),
    ("1-4", "Elite"): ("3d6", "ficha", "Capataz Oco"),
    ("5-8", "Elite"): ("4d8 + 1", "ficha", "Centurião Catafracto"),
    ("9-12", "Elite"): ("5d10 + 1", "ficha", "Oficial-Lâmina da Frota de Jade"),
    ("13-16", "Elite"): ("6d10 + 3", "ficha", "Escultor de Carne"),
    ("17-20", "Elite"): ("7d12 + 3", "ficha", "Arcanjo de Ferro-Vazio"),
    ("1-4", "Boss"): ("3d8 + 2", "ficha", "O Afogado do Poço Sete"),
    ("5-8", "Boss"): ("4d8 + 12", "Sugestão da planilha (H2)", ""),
    ("9-12", "Boss"): ("7d10 + 4", "ficha", "O Dramaturgo de Mil Faces"),
    ("13-16", "Boss"): ("9d10 + 5", "ficha", "Vênia, a Primeira Obra"),
    ("17-20", "Boss"): ("10d12 + 7", "ficha", "O Germe de Pavor"),
}


@lru_cache(None)
def dano_especial():
    saida = []
    for fx in FAIXAS:
        for tipo in TIPOS:
            expr, fonte, ficha = DANO_ESPECIAL[(fx, tipo)]
            n, f, fixo = dados_de(expr)
            med = media(n, f, fixo)
            alvo = int(1.5 * ancora(fx, tipo)["dano_media"])
            if med != alvo:
                _erro("28.4", f"dano especial {expr} (média {med}) ≠ INT(1,5 × âncora) = {alvo} em {fx} {tipo}")
            saida.append({"faixa": fx, "tipo": tipo, "chave": f"{fx}|{tipo}", "expr": expr, "media": med,
                          "fonte": fonte, "ficha": ficha})
    return saida


# ---------------------------------------------------------------------------
# 28.6–28.11 — as 32 fichas
# ---------------------------------------------------------------------------

_RE_DANO = re.compile(r"(\d+d\d+(?: \+ \d+)?) · (média )?(\d+)")
_ALCANCES = ["Pessoal", "Curta", "Média", "Longa", "Extrema"]


def _indice():
    _, corpo = F.tabela("28", "## 28.11", "#")
    saida = []
    for l in corpo:
        tipo_fases = l[2]
        tipo = tipo_fases.split(",")[0].strip()
        m = re.search(r"(\d) fases", tipo_fases)
        saida.append({"n": _num(l[0]), "nome": l[1], "tipo": tipo, "fases": int(m.group(1)) if m else 1,
                      "faixa": l[3], "faccao": l[4], "pv": _num(l[5]),
                      "fraquezas": [x.strip() for x in l[6].split(",")]})
    if len(saida) != 32:
        _erro("28.11", f"índice com {len(saida)} fichas (esperado 32)")
    return saida


def _linhas_cap28():
    return F.capitulo("28")


def _blocos_fichas():
    """{título do ### : linhas do cartão} para as seções 28.6 a 28.10."""
    linhas = _linhas_cap28()
    saida, atual, dentro = {}, None, False
    for l in linhas:
        if l.startswith("## "):
            dentro = bool(re.match(r"## 28\.(6|7|8|9|10) ", l))
            atual = None
            continue
        if not dentro:
            continue
        if l.startswith("### "):
            atual = l[4:].strip()
            saida[atual] = []
            continue
        if atual is not None:
            saida[atual].append(l)
    return saida


def _tipo_acao(grupo, parenteses, nome_parenteses_ok):
    p = parenteses or ""
    if "Reação" in p:
        return "Reação"
    if "1 vez por combate" in p or "cai a 0 PV" in p:
        return "Gatilho"
    if grupo == "ataques":
        return "Ataque"
    if grupo == "especiais":
        return "Especial"
    # grupo misto (fases 2 e 3): ataque = "(Alcance, Elemento)" e nada mais
    return "Ataque" if nome_parenteses_ok else "Especial"


def _acao(bullet, grupo, fase, ordem, criatura):
    texto = F.limpar(bullet[2:])
    m = re.match(r"^(.+?) \((.+?)\)(:|\s)", texto)
    if not m:
        raise ValueError(f"cap 28: ação fora do formato em {criatura}: {texto[:60]!r}")
    nome, par = m.group(1), m.group(2)
    partes = [x.strip() for x in par.split(",")]
    ataque_puro = len(partes) == 2 and partes[0] in _ALCANCES and partes[1] in ELEMENTOS
    tipo = _tipo_acao(grupo, par, ataque_puro)
    rec = re.search(r"recarga (\d) Ciclos", par)
    recarga = int(rec.group(1)) if rec else (0 if "sem recarga" in par else "")
    alcance = partes[0] if partes[0] in _ALCANCES else ""
    elemento = next((x for x in partes if x in ELEMENTOS), "")
    return {"criatura": criatura, "fase": fase, "ordem": ordem, "tipo": tipo, "nome": nome, "alcance": alcance,
            "elemento": elemento, "recarga": recarga, "texto": texto}


def _fraquezas(s):
    s = F.limpar(s)
    return [] if s in ("—", "-", "") else [x.strip() for x in s.split(",")]


@lru_cache(None)
def bestiario():
    """As 32 fichas, na ordem do índice de 28.11, com campos, fases e ações."""
    idx = _indice()
    blocos = _blocos_fichas()
    saida = []
    for it in idx:
        titulo = next((t for t in blocos if t == it["nome"] or t.startswith(it["nome"] + ",")), None)
        if titulo is None:
            _erro("28.6–28.10", f"ficha de {it['nome']} não encontrada")
        ls = blocos[titulo]
        linha_tipo = next((F.limpar(l) for l in ls if l.startswith("*") and "faixa" in l), None)
        if not linha_tipo:
            _erro("28.6–28.10", f"{it['nome']}: linha de tipo não encontrada")
        partes = [x.strip() for x in linha_tipo.split("·")]
        tipo_card, faixa_card = partes[0], next(x.replace("faixa ", "") for x in partes if x.startswith("faixa "))
        origem_card = " · ".join(x for x in partes[1:] if not x.startswith("faixa ") and "fase" not in x)
        frase = next((F.limpar(l.lstrip("> ")) for l in ls if l.startswith('> *"')), "")
        tabs = F.tabelas(ls)
        campos = {c[0]: c[1] for c in tabs[0][1]} if tabs and tabs[0][0][:2] == ["Campo", "Valor"] else None
        if campos is None:
            _erro("28.6–28.10", f"{it['nome']}: tabela Campo/Valor não encontrada")
        ficha = {"n": it["n"], "nome": it["nome"], "titulo": titulo, "tipo": it["tipo"], "faixa": it["faixa"],
                 "faccao": it["faccao"], "origem_card": origem_card, "fases": it["fases"], "frase": frase,
                 "tipo_card": tipo_card, "faixa_card": faixa_card}
        ficha["pv"] = _num(campos["PV"].split("(")[0])
        for k, c in (("defesa", "Defesa"), ("rd", "RD"), ("vel", "Velocidade"), ("ataque", "Teste de Ataque"),
                     ("dt", "DT dos efeitos"), ("tr", "Teste de Resistência")):
            ficha[k] = _num(campos[c])
        ficha["ten"] = _num(re.match(r"\d+", campos["Tenacidade"]).group(0))
        ficha["ten_texto"] = campos["Tenacidade"]
        ficha["pv_texto"] = campos["PV"]
        # fases, ações e Fraquezas
        acoes, fases, grupo, fase, ordem = [], [], None, 0, 0
        fase_atual = None
        na_fila = ""
        i = 0
        while i < len(ls):
            l = ls[i]
            mf = re.match(r"^\*\*Fase (\d) — (.+?) \((\d+) a (\d+) PV\)\*\*", l)
            if mf:
                fase = int(mf.group(1))
                fase_atual = {"criatura": it["nome"], "fase": fase, "nome_fase": mf.group(2),
                              "topo": int(mf.group(3)), "piso": int(mf.group(4)), "fraquezas": None,
                              "ten": None, "ritmo": ""}
                fases.append(fase_atual)
                grupo = None
                i += 1
                continue
            if l.startswith("**Ataques**"):
                grupo = "ataques"
                if fase_atual is not None and "—" in l:
                    fase_atual["ritmo"] = F.limpar(l.split("—", 1)[1]).rstrip(":")
            elif l.startswith("**Ações especiais**") or l.startswith("**Ação especial**"):
                grupo = "especiais"
            elif re.match(r"^\*\*(Ataques e ações|Ação) da fase (\d)\*\*", l):
                grupo = "misto"
                if fase_atual is not None and "—" in l:
                    fase_atual["ritmo"] = F.limpar(l.split("—", 1)[1]).rstrip(":")
            elif l.startswith("**Na Fila:**"):
                na_fila = F.limpar(l[len("**Na Fila:**"):])
                grupo = None
            elif l.startswith("- **") and grupo:
                ordem += 1
                acoes.append(_acao(l, grupo, fase, ordem, it["nome"]))
            i += 1
        # Fraquezas e Tenacidade por fase
        if fases:
            for t_cab, t_corpo in tabs[1:]:
                if t_cab[:2] == ["Campo", "Valor"]:
                    d = {c[0]: c[1] for c in t_corpo}
                    alvo = next((f for f in fases if f["fraquezas"] is None), None)
                    if alvo is not None and "Fraquezas" in d:
                        alvo["fraquezas"] = _fraquezas(d["Fraquezas"])
                        alvo["ten"] = _num(d["Tenacidade"])
                elif t_cab[:3] == ["O que muda", "De", "Para"]:
                    d = {c[0]: (c[1], c[2]) for c in t_corpo}
                    alvo = next((f for f in fases if f["fraquezas"] is None), None)
                    if alvo is None:
                        _erro("28.5", f"{it['nome']}: tabela 'O que muda' sem fase")
                    alvo["fraquezas"] = _fraquezas(d["Fraquezas"][1])
                    alvo["ten"] = _num(re.match(r"\d+", F.limpar(d["Tenacidade"][1])).group(0))
            if any(f["fraquezas"] is None for f in fases):
                _erro("28.5", f"{it['nome']}: fase sem Fraquezas")
            ficha["fraquezas"] = fases[0]["fraquezas"]
        else:
            ficha["fraquezas"] = _fraquezas(campos["Fraquezas"])
        ficha["resistencias"] = _fraquezas(campos.get("Resistências", "—"))
        ficha["fases_detalhe"] = fases
        ficha["acoes"] = acoes
        ficha["na_fila"] = na_fila
        nf = na_fila.lower()
        ficha["execucao"] = ("Não" if ("não pode executar" in nf or "não executa" in nf)
                             else "Pode" if "pode executar" in nf else "Não declarado")
        mv = re.match(r"VEL (\d+), (com|sem) Firmeza\. ?(.*)$", na_fila)
        if not mv:
            _erro("28.6–28.10", f"{it['nome']}: linha Na Fila fora do formato: {na_fila[:60]!r}")
        ficha["na_fila_vel"], ficha["na_fila_firmeza"] = int(mv.group(1)), f"{mv.group(2)} Firmeza"
        ficha["na_fila_resto"] = mv.group(3)
        _conferir(ficha, it)
        saida.append(ficha)
    return saida


def _conferir(fi, it):
    """Número da ficha × âncora de 28.3 e × índice de 28.11 (P13: divergência nova é fatal)."""
    a = ancora(fi["faixa"], fi["tipo"])
    doc = {(d[1], d[2]) for d in DIVERGENCIAS_DOCUMENTADAS}
    for k in ("pv", "defesa", "rd", "ten", "vel", "ataque", "dt", "tr"):
        if fi[k] != a[k]:
            _erro("28.6–28.10", f"{fi['nome']}: {k} = {fi[k]} ≠ âncora {a[k]} ({fi['faixa']} {fi['tipo']})")
    if fi["na_fila_vel"] != a["vel"] or fi["na_fila_firmeza"] != a["firmeza"]:
        _erro("28.6–28.10", f"{fi['nome']}: Na Fila diferente da âncora")
    n = len(fi["fraquezas"])
    ok = (1 <= n <= 2) if fi["tipo"] == "Comum" else n == {"Elite": 3, "Boss": 4}[fi["tipo"]]
    if not ok:
        _erro("28.2", f"{fi['nome']}: {n} Fraquezas para {fi['tipo']}")
    for f in fi["fases_detalhe"]:
        if f["ten"] > a["ten"]:
            _erro("28.5", f"{fi['nome']}: Tenacidade da fase {f['fase']} acima da âncora")
        if f["ten"] != a["ten"] and (fi["nome"], f"Tenacidade da fase {f['fase']}") not in doc:
            _erro("28.5", f"{fi['nome']}: Tenacidade da fase {f['fase']} = {f['ten']} ≠ âncora {a['ten']} "
                          f"(registre em DIVERGENCIAS_DOCUMENTADAS)")
        if len(f["fraquezas"]) != 4:
            _erro("28.5", f"{fi['nome']}: fase {f['fase']} com {len(f['fraquezas'])} Fraquezas")
    if fi["pv"] != it["pv"] or fi["fraquezas"] != it["fraquezas"]:
        _erro("28.11", f"{fi['nome']}: PV ou Fraquezas diferentes do índice")
    if fi["tipo_card"] != fi["tipo"] or fi["faixa_card"] != fi["faixa"]:
        _erro("28.11", f"{fi['nome']}: tipo/faixa do cartão diferentes do índice")
    if len(fi["fases_detalhe"]) not in (0, fi["fases"]) or (fi["fases"] > 1 and not fi["fases_detalhe"]):
        _erro("28.5", f"{fi['nome']}: nº de fases diferente do índice")


def fases():
    return [f for fi in bestiario() for f in fi["fases_detalhe"]]


def limiares(pv, nfases):
    """H4: 2 fases → topo da fase 2 = INT(PV/2); 3 fases → INT(2PV/3) e INT(PV/3). Devolve [(topo, piso)]."""
    if nfases == 2:
        t2 = pv // 2
        return [(pv, t2 + 1), (t2, 0)]
    if nfases == 3:
        t2, t3 = (2 * pv) // 3, pv // 3
        return [(pv, t2 + 1), (t2, t3 + 1), (t3, 0)]
    return [(pv, 0)]


# ---------------------------------------------------------------------------
# Texto-modelo das ações (design §6.7.3): pedaços literais + marcadores (tipo, parâmetro)
# ---------------------------------------------------------------------------

MAX_MARCADORES = 4


def modelo_acao(texto, ficha):
    """Parte o texto em [p0, (t1, n1), p1, …]. Marcadores: DANO.e/DANO.m, DANO15.e/.m, DANOC.e/.m, DT, PV(n)."""
    a = ancora(ficha["faixa"], ficha["tipo"])
    esp = next(d for d in dano_especial() if d["faixa"] == ficha["faixa"] and d["tipo"] == ficha["tipo"])
    comum = ancora(ficha["faixa"], "Comum")
    achados = []          # (início, fim, tipo, parâmetro)
    for m in _RE_DANO.finditer(texto):
        expr, med = m.group(1), int(m.group(3))
        fam = None
        if expr == a["dano_expr"] and med == a["dano_media"]:
            fam = "DANO"
        elif expr == esp["expr"] and med == esp["media"]:
            fam = "DANO15"
        elif expr == comum["dano_expr"] and med == comum["dano_media"]:
            fam = "COMUM"
        if fam:
            achados.append((m.start(1), m.end(1), f"{fam}.e", ""))
            achados.append((m.start(3), m.end(3), f"{fam}.m", ""))
    for m in re.finditer(r"DT (\d+)", texto):
        if int(m.group(1)) == ficha["dt"]:
            achados.append((m.start(1), m.end(1), "DT", ""))
    for m in re.finditer(r"(\d+) PV ou menos|metade dos PV \((\d+)\)", texto):
        g = 1 if m.group(1) else 2
        achados.append((m.start(g), m.end(g), "PV", int(m.group(g))))
    achados.sort()
    if len(achados) > MAX_MARCADORES:
        raise ValueError(f"cap 28: {ficha['nome']}: ação com {len(achados)} marcadores (máximo {MAX_MARCADORES})")
    pecas, pos = [], 0
    for ini, fim, tipo, par in achados:
        pecas.append(texto[pos:ini])
        pecas.append((tipo, par))
        pos = fim
    pecas.append(texto[pos:])
    return pecas


def renderizar_modelo(pecas, valores):
    """Inverso de modelo_acao (usado para conferir na faixa original)."""
    s = ""
    for p in pecas:
        if isinstance(p, tuple):
            tipo, par = p
            s += str(valores[tipo](par) if callable(valores[tipo]) else valores[tipo])
        else:
            s += p
    return s


def acoes():
    saida = []
    for fi in bestiario():
        a = ancora(fi["faixa"], fi["tipo"])
        esp = next(d for d in dano_especial() if d["faixa"] == fi["faixa"] and d["tipo"] == fi["tipo"])
        com = ancora(fi["faixa"], "Comum")
        vals = {"DANO.e": a["dano_expr"], "DANO.m": a["dano_media"], "DANO15.e": esp["expr"],
                "DANO15.m": esp["media"], "COMUM.e": com["dano_expr"], "COMUM.m": com["dano_media"],
                "DT": fi["dt"], "PV": lambda n: n}
        for k, ac in enumerate(fi["acoes"], start=1):
            pecas = modelo_acao(ac["texto"], fi)
            if renderizar_modelo(pecas, vals) != ac["texto"]:
                raise ValueError(f"cap 28: {fi['nome']}: texto-modelo não reproduz a ação {ac['nome']}")
            saida.append({**ac, "k": k, "pecas": pecas})
    return saida


# ---------------------------------------------------------------------------
# Capítulo 27
# ---------------------------------------------------------------------------

@lru_cache(None)
def orcamento():
    cab, corpo = F.tabela("27", "## 27.4", "Faixa")
    if cab[:3] != ["Faixa", "Dano do grupo por Ciclo", "Orçamento do encontro"]:
        raise ValueError(f"cap 27, seção 27.4: colunas inesperadas {cab}")
    saida = []
    for l in corpo:
        saida.append({"faixa": l[0], "dpc": _num(l[1]), "orcamento": _num(l[2]),
                      "comum": _num(l[3].split("(")[0]), "elite": _num(l[4].split("(")[0]),
                      "boss": _num(l[5].split("(")[0])})
        if saida[-1]["orcamento"] != 4 * saida[-1]["dpc"]:
            raise ValueError(f"cap 27, seção 27.4: orçamento ≠ 4 × dano por Ciclo em {l[0]}")
    return saida


COMPOSICOES_TIPOS = {"1 Boss + 1 Comum": (1, 0, 1), "1 Elite + 4 Comuns": (0, 1, 4), "3 Elites": (0, 3, 0),
                     "7 Comuns": (0, 0, 7)}


@lru_cache(None)
def composicoes():
    _, corpo = F.tabela("27", "## 27.4", "Composição")
    saida = []
    for l in corpo:
        if l[0] not in COMPOSICOES_TIPOS:
            raise ValueError(f"cap 27, seção 27.4: composição desconhecida {l[0]}")
        b, e, c = COMPOSICOES_TIPOS[l[0]]
        saida.append({"composicao": l[0], "sensacao": l[1], "duracao": l[2], "boss": b, "elite": e, "comum": c})
    _, ex = F.tabela("28", "## 28.11", "Composição")
    exemplos = {l[0]: (l[1], l[2]) for l in ex}
    for s in saida:
        s["exemplo_1_4"], s["exemplo_17_20"] = exemplos[s["composicao"]]
    return saida


@lru_cache(None)
def attrition():
    _, corpo = F.tabela("27", "## 27.7", "Faixa")
    return [{"faixa": l[0], "nivel": _num(l[1]), "pv_grupo": _num(l[2]), "dano_4": _num(l[3]),
             "termina": l[4]} for l in corpo]


@lru_cache(None)
def faccoes():
    linhas = F.secao("27", "## 27.16")
    nomes = [l[4:].strip() for l in linhas if l.startswith("### ")]
    if len(nomes) != 8:
        raise ValueError(f"cap 27, seção 27.16: {len(nomes)} facções (esperado 8)")
    return nomes


@lru_cache(None)
def locais():
    _, corpo = F.tabela("27", "## 27.17", "Lugar")
    if len(corpo) != 6:
        raise ValueError("cap 27, seção 27.17: esperado 6 locais")
    return [{"lugar": l[0], "o_que_e": l[1], "cena": l[2]} for l in corpo]


@lru_cache(None)
def ganchos():
    _, corpo = F.tabela("27", "## 27.18", "Faixa")
    saida = {}
    for l in corpo:
        g = [x.strip() for x in l[1].split(" · ")]
        if len(g) != 4:
            raise ValueError(f"cap 27, seção 27.18: faixa {l[0]} com {len(g)} ganchos")
        saida[l[0]] = g
    return saida


# H8: ambiente por facção/origem (lida de 27.16–27.17); editável na aba Tabelas
AMBIENTE_POR_FACCAO = [
    ("Fragmentum", "Colônia ou mina abandonada"), ("Fragmentum", "Ruína"),
    ("Legião da Antimatéria", "Frente de guerra"), ("Legião da Antimatéria", "Lua-forja"),
    ("Corporação da Paz Interastral", "Estação"), ("Corporação da Paz Interastral", "Cidade corporativa"),
    ("Aliança Xianzhou", "Nave-cidade"), ("Xianzhou", "Nave-cidade"),
    ("Tolos Mascarados", "Teatro, festa ou multidão"), ("Cavaleiros da Beleza", "Clínica ou ateliê"),
    ("Caçadores de Stellaron", "Qualquer lugar onde o grupo esteja"),
    ("Culto da Inexistência", "Lugar esvaziado"), ("Autômato", "Instalação antiga"),
    ("Autômato de guerra", "Instalação antiga"), ("Stellaron", "Mundo com Stellaron"),
    ("Emanadora da Inexistência", "Mundo com Stellaron"), ("Emanador", "Mundo com Stellaron"),
]
AMBIENTES = list(dict.fromkeys(a for _, a in AMBIENTE_POR_FACCAO))
FACCOES_CRIADOR_EXTRA = ["Fragmentum", "Stellaron", "Emanador", "Outra"]


# ---------------------------------------------------------------------------
# Tabelas reaproveitadas da ficha (caps. 16, 17, 19–25)
# ---------------------------------------------------------------------------

def fontes_tenacidade():
    """Fontes da calculadora com a Redução de Tenacidade bruta (20.3), uma linha por nível."""
    saida = []
    for t in F.tenacidade():
        f, v = t["fonte"], t["rt"]
        n = _num(re.match(r"\d+", v).group(0))
        m = re.match(r"Habilidade de Nível (\d)-(\d)", f)
        if m:
            for k in range(int(m.group(1)), int(m.group(2)) + 1):
                saida.append((f"Habilidade de Nível {k}", n))
        else:
            saida.append((f, n))
    return saida


def condicoes_mestre():
    """21.5 com os números de dano e teto de acúmulo lidos do texto do efeito."""
    saida = []
    for c in F.condicoes():
        ef = c["efeito"]
        m = re.search(r"(\d+)d(\d+)", ef)
        n, f = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        por_ac = "Sim" if "por acúmulo" in ef else "Não"
        soma_ef = "Sim" if re.search(r"\d+d\d+ \+ Eficiência", ef) else "Não"
        pct = re.search(r"(\d+)% dos PV máximos, teto (\d+) × Eficiência", ef)
        atr = re.search(r"Atrasa (\d+) casa", ef)
        ac = c["acumulo"]
        mt = re.search(r"\d+", ac)
        teto = int(mt.group(0)) if mt else 1
        saida.append({**c, "n": n, "f": f, "por_acumulo": por_ac, "soma_ef": soma_ef,
                      "pct": int(pct.group(1)) if pct else 0, "teto_ef": int(pct.group(2)) if pct else 0,
                      "atrasa": int(atr.group(1)) if atr else 0, "teto_acumulo": teto,
                      "dano_continuo": "Sim" if "Dano Contínuo" in ef else "Não"})
    return saida


def eficiencias():
    return [(m["nivel"], m["eficiencia"]) for m in F.tabela_mestra()]


# ---------------------------------------------------------------------------
# Fase 2 — NPCs, aventuras e recompensas (05, 24, 25, 26, 27.7, 27.8, 27.16, 27.17)
# ---------------------------------------------------------------------------

@lru_cache(None)
def faccao_fichas():
    """27.16: cada facção lista as fichas do capítulo 28 ("*Fichas: …*"). Devolve [(facção, criatura)]."""
    saida, atual = [], None
    nomes = {f["nome"] for f in bestiario()}
    for l in F.secao("27", "## 27.16"):
        if l.startswith("### "):
            atual = l[4:].strip()
        m = re.search(r"\*Fichas: (.+?)\.\*", l)
        if m and atual:
            for c in _separar_fichas(m.group(1), nomes):
                saida.append((atual, c))
    if len({f for f, _ in saida}) != 8:
        raise ValueError("cap 27, seção 27.16: esperava fichas nas 8 facções")
    return saida


def _separar_fichas(s, nomes):
    """'A, B, Vênia, a Primeira Obra' → nomes do bestiário (o nome pode ter vírgula)."""
    partes = [x.strip() for x in s.split(",")]
    saida, i = [], 0
    while i < len(partes):
        if i + 1 < len(partes) and f"{partes[i]}, {partes[i + 1]}" in nomes:
            saida.append(f"{partes[i]}, {partes[i + 1]}")
            i += 2
            continue
        if partes[i] not in nomes:
            raise ValueError(f"cap 27, seção 27.16: ficha '{partes[i]}' não está no bestiário (28.11)")
        saida.append(partes[i])
        i += 1
    return saida


# H26: "Faixa alta" (Ferro-Vazio, 27.17) = as duas faixas do topo; sem faixa dita, o lugar serve em qualquer faixa
FAIXA_ALTA = (4, 5)


@lru_cache(None)
def locais_faixa():
    """27.17: a faixa que o livro diz para cada lugar (coluna 'A cena que ele entrega')."""
    saida = []
    for x in locais():
        m = re.match(r"Faixa (\d+-\d+)\.", x["cena"])
        if m:
            k = FAIXAS.index(m.group(1)) + 1
            saida.append((x["lugar"], k, k, f"Faixa {m.group(1)} (27.17)"))
        elif x["cena"].startswith("Faixa alta."):
            saida.append((x["lugar"], FAIXA_ALTA[0], FAIXA_ALTA[1], "Faixa alta (27.17): 13-16 e 17-20 — "
                                                                   "Sugestão da planilha (H26)"))
        else:
            saida.append((x["lugar"], 1, 5, "Sem faixa no livro: qualquer faixa"))
    return saida


@lru_cache(None)
def sem_matar():
    """27.7: '…dar à cena um objetivo que não seja matar todo mundo (fugir com a carga, aguentar 3 Ciclos, chegar
    ao console)'."""
    txt = "\n".join(F.secao("27", "## 27.7"))
    m = re.search(r"objetivo que não seja matar todo mundo \((.+?)\)", F.limpar(txt))
    if not m:
        raise ValueError("cap 27, seção 27.7: objetivos 'que não seja matar todo mundo' não encontrados")
    return [x.strip() for x in m.group(1).split(",")]


@lru_cache(None)
def nao_dar():
    """27.8: 'O que você não deve dar, por mais tentador que pareça' (lista)."""
    ls = F.secao("27", "## 27.8")
    i = next((k for k, l in enumerate(ls) if "O que você não deve dar" in l), None)
    if i is None:
        raise ValueError("cap 27, seção 27.8: lista 'O que você não deve dar' não encontrada")
    saida = []
    for l in ls[i + 1:]:
        if l.startswith("- "):
            saida.append(F.limpar(l[2:]))
        elif saida and l.strip():
            break
    if len(saida) != 5:
        raise ValueError(f"cap 27, seção 27.8: esperava 5 itens em 'o que não dar', vieram {len(saida)}")
    return saida


@lru_cache(None)
def bonus_maior():
    """25.2 'O Bônus Maior': a lista de escolhas (o Dano e o Teste abertos nas suas opções)."""
    ls = F.secao("25", "### O Bônus Maior")
    itens = [F.limpar(l[2:]) for l in ls if l.startswith("- ")]
    if len(itens) != 6:
        raise ValueError(f"cap 25, seção 25.2: esperava 6 itens no Bônus Maior, vieram {len(itens)}")
    return ["PV máximos", "Defesa", "Velocidade", "Dano de Ataque Básico", "Dano de Habilidade", "Dano de Ultimate",
            "RD, dentro do teto de 2 + (2 × Eficiência)", "Bônus em Teste de Ataque",
            "Bônus em um Teste de Resistência", "Bônus em uma Perícia"]


@lru_cache(None)
def conjunto_2():
    """25.3: as opções do bônus de 2 peças ('+1 em um tipo de rolagem, +1 de Velocidade, +2 de dano ou +1 RD')."""
    g = next(c["ganho"] for c in F.conjuntos() if c["pecas"].startswith("2"))
    m = re.search(r": (.+)$", g)
    partes = re.split(r", | ou ", m.group(1))
    if len(partes) != 4:
        raise ValueError(f"cap 25, seção 25.3: esperava 4 opções de 2 peças, vieram {partes}")
    return partes


def tier_do_nivel(n):
    """25.3: Tier I (1-6), II (7-12), III (13-17), IV (18-20)."""
    return "Tier I" if n <= 6 else "Tier II" if n <= 12 else "Tier III" if n <= 17 else "Tier IV"


def consumiveis():
    """24.3 (poções e itens comuns) com a faixa de cada poção (H9: Pequena 1-8, Média 5-16, Grande 13-20)."""
    faixas_pocao = {"Pequena": (1, 2), "Média": (2, 4), "Grande": (4, 5)}
    saida = []
    for p in F.pocoes():
        a, b = faixas_pocao[p["pocao"]]
        saida.append((f"Poção {p['pocao']}", p["preco"], "Poção de Vida", a, b))
    for it in F.itens():
        saida.append((it["item"], it["preco"], "Item comum", 1, 5))
    return saida


def _blocos_fase2(bloco):
    import mestre_sabor_nomes as NM
    bloco("culturas", "Culturas e montagem do nome — 05 (nomes: Sugestão da planilha)",
          ["Raça", "Ordem", "Separador", "Índice"],
          [[c, NM.MONTAGEM[c][0], NM.MONTAGEM[c][1], k + 1] for k, c in enumerate(NM.CULTURAS)], "05")
    bloco("papeis", "Papel do NPC na história — Sugestão da planilha (H11)", ["Papel", "Índice"],
          [[p, k + 1] for k, p in enumerate(PAPEIS)], "6.6")
    bloco("pocoes", "Poções de Vida — 24.3", ["Poção", "Cura", "Espaço", "Preço (Cr)"],
          [[p["pocao"], p["cura"], p["espaco"], p["preco"]] for p in F.pocoes()], "24.3")
    bloco("itens", "Itens comuns — 24.3", ["Item", "Espaço", "Preço (Cr)", "Para quê"],
          [[i["item"], i["espaco"], i["preco"], i["uso"]] for i in F.itens()], "24.3")
    bloco("armaduras", "Armaduras e Vestimentas — 24.1", ["Tipo", "Defesa", "Outros efeitos", "Esquiva", "Espaço",
                                                         "Preço (Cr)"],
          [[a["tipo"], a["defesa"], a["outros"], a["esquiva"], a["espaco"], a["preco"]] for a in F.armaduras()], "24.1")
    bloco("armas", "Armas — 24.2", ["Categoria", "Dados base", "Alcance", "Atributo de Ataque", "Espaço",
                                   "Preço (Cr)"],
          [[a["categoria"], a["dados"], a["alcance"], a["atributo"], a["espaco"], a["preco"]] for a in F.armas()],
          "24.2")
    cons = consumiveis()
    linhas = []
    cont = [0] * 5
    for nome, preco, tipo, a, b in cons:
        ordem = []
        for k in range(1, 6):
            if a <= k <= b:
                cont[k - 1] += 1
                ordem.append(cont[k - 1])
            else:
                ordem.append("")
        linhas.append([nome, preco, tipo, f"{FAIXAS[a - 1].split('-')[0]}-{FAIXAS[b - 1].split('-')[1]}"] + ordem)
    bloco("consumiveis", "Consumíveis dos achados — 24.3 (faixa da poção: Sugestão da planilha, H9)",
          ["Item", "Preço (Cr)", "Tipo", "Faixas", "Ordem 1-4", "Ordem 5-8", "Ordem 9-12", "Ordem 13-16",
           "Ordem 17-20"], linhas, "24.3")
    bloco("consumiveis_faixa", "Consumíveis por faixa — 24.3 e H9", ["Faixa", "Nº de consumíveis"],
          [[fx, cont[k]] for k, fx in enumerate(FAIXAS)], "24.3")
    cone = F.cone()
    bloco("cone", "Cone de Luz por Nível — 25.2 (Sobreposição até o teto +3)",
          ["Nível do Cone", "Nível do personagem", "Bônus Maior", "Efeito Condicional", "Parte numérica", "Modo",
           "PV", "Sobreposições até o teto", "PV no teto"],
          [[c["nivel"], c["nivel_personagem"], c["bonus"], c["condicional"], c["numerico"], c["modo"], c["pv"],
            3 - c["numerico"], c["pv"] + 10 * (3 - c["numerico"])] for c in cone], "25.2")
    bloco("reliquias", "Relíquias: 6 slots por Tier — 25.3", ["Slot", "O que dá", "Tier I", "Tier II", "Tier III",
                                                              "Tier IV"],
          [[r["slot"], r["da"], r["t1"], r["t2"], r["t3"], r["t4"]] for r in F.reliquias()], "25.3")
    bloco("conjuntos", "Conjuntos de Relíquias — 25.3", ["Peças", "O que você ganha"],
          [[c["pecas"], c["ganho"]] for c in F.conjuntos()], "25.3")
    bloco("ressonancias", "Ressonâncias — 26.7", ["Ressonância", "Nível", "O que ela dá"],
          [[r["ressonancia"], r["nivel"], r["opcao"]] for r in F.ressonancias()], "26.7")
    fe = {f["faixa"]: f for f in F.faixas_equipamento()}
    ress = {r["nivel"]: r["ressonancia"] for r in F.ressonancias()}
    verba = {v["faixa"]: v["verba"] for v in F.verba()}
    niv = []
    for n in range(1, 21):
        fx = FAIXAS[(n - 1) // 4]
        cone_n = int(re.search(r"\d", fe[fx]["cone"]).group(0))
        niv.append([n, fx, cone_n, tier_do_nivel(n), "Sim" if n in (1, 5, 9, 13, 17) else "Não",
                    "Sim" if n in (1, 7, 13, 18) else "Não", ress.get(n, "—"), verba[fx]])
    bloco("nivel_equipamento", "Equipamento e marcos por nível — 25.1, 25.3, 26.7, 24.5",
          ["Nível", "Faixa", "Cone de Luz máximo (Nível)", "Tier de Relíquia", "Primeiro nível da faixa",
           "Tier novo neste nível", "Ressonância", "Verba de marco (Cr)"], niv, "25.1")
    bloco("faccao_fichas", "Facções e as suas fichas — 27.16", ["Facção", "Criatura"],
          [list(x) for x in faccao_fichas()], "27.16")
    bloco("locais_faixa", "Locais do livro e a faixa da cena — 27.17 (Faixa alta: Sugestão da planilha, H26)",
          ["Lugar", "Faixa mínima", "Faixa máxima", "De onde vem"], [list(x) for x in locais_faixa()], "27.17")
    bloco("sem_matar", "Objetivo que não seja matar todo mundo — 27.7", ["Objetivo", "Índice"],
          [[x, k + 1] for k, x in enumerate(sem_matar())], "27.7")
    bloco("bonus_maior", "Bônus Maior: escolha um — 25.2", ["Bônus Maior", "Índice"],
          [[x, k + 1] for k, x in enumerate(bonus_maior())], "25.2")
    bloco("conjunto_2", "Bônus de 2 peças: um bônus pequeno e fixo — 25.3", ["Bônus de 2 peças", "Índice"],
          [[x, k + 1] for k, x in enumerate(conjunto_2())], "25.3")
    bloco("nao_dar", "O que não dar como recompensa — 27.8", ["O que não dar"], [[x] for x in nao_dar()], "27.8")


PAPEIS = ["Aliado", "Contratante", "Rival", "Neutro", "Informante", "Vítima", "Antagonista"]       # 6.6 (H11)


# ---------------------------------------------------------------------------
# Blocos da aba Dados e listas de validação
# ---------------------------------------------------------------------------

def _fq(lista, k):
    return lista[k] if k < len(lista) else ""


def blocos():
    B = []

    def bloco(id_, titulo, cab, linhas, fonte=""):
        B.append({"id": id_, "titulo": titulo, "cabecalho": list(cab), "linhas": [list(x) for x in linhas],
                  "fonte": fonte})

    bloco("faixas", "Faixas de nível — 26.3, 29.1 (nível de referência) e 28.3 (Eficiência do inimigo)",
          ["Índice", "Faixa", "Nível de referência", "Primeiro nível", "Último nível", "Eficiência do inimigo"],
          [[i + 1, fx, NIVEL_REFERENCIA[fx], 4 * i + 1, 4 * i + 4, ancora(fx, "Elite")["tr"]]
           for i, fx in enumerate(FAIXAS)], "26.3")
    bloco("eficiencia", "Eficiência por nível — 26.2 (02.3)", ["Nível", "Eficiência"], eficiencias(), "26.2")
    bloco("ancoras", "Âncoras do inimigo — 28.3 (com 28.2 regras 3 e 5 e 19.4)",
          ["Chave", "Faixa", "Tipo", "PV", "Defesa", "RD", "Tenacidade", "VEL", "Ataque", "Dano por acerto",
           "Média do dano", "DT dos efeitos", "Teste de Resistência", "Nº de Fraquezas", "Fraquezas sugeridas",
           "Firmeza", "Ações agressivas", "Teto de Atraso", "Dano especial 1,5×", "Média do especial",
           "Fonte do especial"],
          [[a["chave"], a["faixa"], a["tipo"], a["pv"], a["defesa"], a["rd"], a["ten"], a["vel"], a["ataque"],
            a["dano_expr"], a["dano_media"], a["dt"], a["tr"], a["nfraq"], a["nfraq_sug"], a["firmeza"],
            a["acoes"], a["teto_atraso"], e["expr"], e["media"], e["fonte"]]
           for a, e in zip(ancoras(), dano_especial())], "28.3")
    bloco("dano_dados", "Dano por acerto, convertido em dados — 28.3",
          ["Chave", "Expressão", "Nº de dados", "Faces", "Fixo", "Média"],
          [[a["chave"], a["dano_expr"], a["dano_n"], a["dano_f"], a["dano_fixo"], a["dano_media"]]
           for a in ancoras()], "28.3")
    bloco("dano_especial", "Dano de ação especial 1,5× — 28.4 regra 5 (fonte: ficha do livro ou Sugestão H2)",
          ["Chave", "Expressão", "Média", "Fonte", "Ficha"],
          [[d["chave"], d["expr"], d["media"], d["fonte"], d["ficha"]] for d in dano_especial()], "28.4")
    fichas = bestiario()
    bloco("bestiario", "Bestiário: as 32 fichas — 28.6 a 28.11 (ambiente: Sugestão da planilha, H8)",
          ["Nº", "Nome", "Tipo", "Faixa", "Facção ou origem", "Fases", "PV", "Defesa", "RD", "Tenacidade", "VEL",
           "Ataque", "Dano por acerto", "Média do dano", "DT dos efeitos", "Teste de Resistência", "Fraqueza 1",
           "Fraqueza 2", "Fraqueza 3", "Fraqueza 4", "Resistência", "Execução", "Firmeza", "Na Fila (resto)",
           "Frase", "Ações agressivas", "Custo no orçamento", "Índice da faixa", "Índice do tipo", "Origem 2",
           "Fraquezas (texto)", "Especial 1", "Recarga 1", "Especial 2", "Recarga 2",
           "Especial 3", "Recarga 3", "Origem no cartão"],
          [_linha_bestiario(fi) for fi in fichas], "28")
    bloco("bestiario_fases", "Bosses com fases — 28.5 a 28.10 (12 linhas)",
          ["Chave", "Criatura", "Fase", "Nome da fase", "PV do topo", "PV do piso", "Fraqueza 1", "Fraqueza 2",
           "Fraqueza 3", "Fraqueza 4", "Tenacidade", "Ritmo"],
          [[f"{f['criatura']}|{f['fase']}", f["criatura"], f["fase"], f["nome_fase"], f["topo"], f["piso"]]
           + [_fq(f["fraquezas"], k) for k in range(4)] + [f["ten"], f["ritmo"]] for f in fases()], "28.5")
    linhas_acoes = []
    for ac in acoes():
        pecas = ac["pecas"]
        lit = [p for p in pecas if not isinstance(p, tuple)]
        mk = [p for p in pecas if isinstance(p, tuple)]
        row = [f"{ac['criatura']}|{ac['k']}", ac["criatura"], ac["fase"], ac["k"], ac["tipo"], ac["nome"],
               ac["recarga"], ac["texto"], lit[0]]
        for j in range(MAX_MARCADORES):
            t, n = mk[j] if j < len(mk) else ("", "")
            row += [t, n, lit[j + 1] if j + 1 < len(lit) else ""]
        linhas_acoes.append(row)
    cab_ac = ["Chave", "Criatura", "Fase", "Ordem", "Tipo", "Nome", "Recarga", "Texto do livro", "p0"]
    for j in range(1, MAX_MARCADORES + 1):
        cab_ac += [f"m{j}", f"n{j}", f"p{j}"]
    bloco("bestiario_acoes", "Ataques e ações das 32 fichas — 28.6 a 28.10 (texto-modelo com marcadores, 6.7.3)",
          cab_ac, linhas_acoes, "28")
    bloco("orcamento", "Orçamento do encontro (grupo de 4) — 27.4",
          ["Faixa", "Dano do grupo por Ciclo", "Orçamento", "Custo Comum", "Custo Elite", "Custo Boss"],
          [[o["faixa"], o["dpc"], o["orcamento"], o["comum"], o["elite"], o["boss"]] for o in orcamento()], "27.4")
    bloco("composicoes", "As quatro composições — 27.4 e 28.11",
          ["Composição", "Como ela se sente", "Duração esperada", "Boss", "Elite", "Comum", "Exemplo 1-4",
           "Exemplo 17-20"],
          [[c["composicao"], c["sensacao"], c["duracao"], c["boss"], c["elite"], c["comum"], c["exemplo_1_4"],
            c["exemplo_17_20"]] for c in composicoes()], "27.4")
    bloco("attrition", "O dia de jogo (attrition) — 27.7",
          ["Faixa", "Nível de referência", "PV do grupo", "Dano recebido em 4 Ciclos", "O grupo termina com"],
          [[a["faixa"], a["nivel"], a["pv_grupo"], a["dano_4"], a["termina"]] for a in attrition()], "27.7")
    cab_dt, corpo_dt = F.dt_faixa()
    bloco("dt_faixa", "DT por faixa — 27.2", cab_dt, corpo_dt, "27.2")
    bloco("dt_fraqueza", "DT para descobrir uma Fraqueza — 20.2",
          ["Faixa", "DT"], [[d["faixa"], d["dt"]] for d in F.dt_fraqueza()], "20.2")
    bloco("elementos", "Elementos, Dano de Quebra e efeito de Quebra — 20.1 e 20.5",
          ["Elemento", "Dano de Quebra", "Nº de dados", "Faces", "Multiplicador da Eficiência", "Efeito de Quebra",
           "Ordem"],
          [[e["elemento"], e["dano_quebra"], e["quebra_n"], e["quebra_f"], e["quebra_mult_ef"], e["efeito_quebra"],
            k + 1] for k, e in enumerate(F.elementos())], "20.5")
    bloco("tenacidade", "Redução de Tenacidade por fonte — 20.3",
          ["Fonte", "Redução bruta"], fontes_tenacidade(), "20.3")
    bloco("condicoes", "Condições — 21.5 (com os números de dano lidos do efeito)",
          ["Condição", "Efeito", "Duração", "Acúmulo", "Só inimigos", "Nº de dados", "Faces", "Por acúmulo",
           "Soma Eficiência", "% dos PV máximos", "Teto (× Eficiência)", "Atrasa (casas)", "Teto de acúmulos",
           "Dano Contínuo"],
          [[c["condicao"], c["efeito"], c["duracao"], c["acumulo"], c["so_inimigos"], c["n"], c["f"],
            c["por_acumulo"], c["soma_ef"], c["pct"], c["teto_ef"], c["atrasa"], c["teto_acumulo"],
            c["dano_continuo"]] for c in condicoes_mestre()], "21.5")
    bloco("ph", "Pontos de Habilidade do grupo — 16.2",
          ["Nº de jogadores", "Máximo 1-8", "Máximo 9-16", "Máximo 17-20", "Início 1-8", "Início 9-16",
           "Início 17-20"], [[p["jogadores"]] + p["max"] + p["ini"] for p in F.ph()], "16.2")
    bloco("racas", "Raças — 05 (o que importa no combate: 23.5, 05, 20.2)",
          ["Raça", "Morrendo com Vantagem", "Pode ser Executado", "Esforço", "Descobre Fraqueza"],
          [[r["raca"], "Sim" if r["raca"] in F.racas_morrendo_vantagem() else "Não",
            "Não" if r["raca"] == "Xianzhouíta" else "Sim", "Sim" if r["raca"] == "Humano" else "Não",
            "Com Vantagem, 2 por sucesso" if r["raca"] == "Intellitron" else "Normal"] for r in F.racas()], "05")
    bloco("caminhos", "Caminhos e Bônus de VEL — 19.1", ["Caminho", "Bônus de VEL"],
          [[c["caminho"], c["vel"]] for c in F.caminhos()], "19.1")
    bloco("verba", "Verba de marco do grupo — 24.5", ["Faixa", "Verba de marco (Cr)", "O que ela compra"],
          [[v["faixa"], v["verba"], v["compra"]] for v in F.verba()], "24.5")
    bloco("faixas_equipamento", "Cone de Luz e Relíquias por faixa — 25.1",
          ["Faixa", "Cone de Luz máximo", "Relíquias"],
          [[f["faixa"], f["cone"], f["reliquias"]] for f in F.faixas_equipamento()], "25.1")
    _blocos_fase2(bloco)
    import mestre_dados3 as D3          # Fase 3: Escudo, Improviso, Campanha, Mundos
    D3.blocos3(bloco)
    return B


def _linha_bestiario(fi):
    fr = fi["fraquezas"]
    esp = [a for a in fi["acoes"] if a["tipo"] in ("Especial", "Reação", "Gatilho") and a["recarga"] not in ("", 0)]
    origens = [x.strip() for x in fi["origem_card"].split("·")]
    origem2 = next((x for x in origens if x != fi["faccao"] and x not in fi["faccao"]), "")
    custo = fi["pv"] * 1.5 if fi["nome"] == "Escória de Stellaron" else fi["pv"]       # 28.10 (Divisão)
    linha = [fi["n"], fi["nome"], fi["tipo"], fi["faixa"], fi["faccao"], fi["fases"], fi["pv"], fi["defesa"],
             fi["rd"], fi["ten"], fi["vel"], fi["ataque"], ancora(fi["faixa"], fi["tipo"])["dano_expr"],
             ancora(fi["faixa"], fi["tipo"])["dano_media"], fi["dt"], fi["tr"], _fq(fr, 0), _fq(fr, 1), _fq(fr, 2),
             _fq(fr, 3), ", ".join(fi["resistencias"]) if fi["resistencias"] else "", fi["execucao"],
             fi["na_fila_firmeza"], fi["na_fila_resto"], fi["frase"], ancora(fi["faixa"], fi["tipo"])["acoes"],
             custo, FAIXAS.index(fi["faixa"]) + 1, TIPOS.index(fi["tipo"]) + 1, origem2,
             ", ".join(fr)]
    for k in range(3):
        linha += [esp[k]["nome"], esp[k]["recarga"]] if k < len(esp) else ["", ""]
    linha.append(fi["origem_card"])
    return linha


def listas():
    L = []

    def lista(id_, titulo, fonte, valores):
        L.append({"id": id_, "titulo": titulo, "fonte": fonte, "valores": list(valores)})

    fichas = bestiario()
    lista("elementos", "Elementos", "20.1", ELEMENTOS)
    lista("tipos", "Tipos de inimigo", "28.1", TIPOS)
    # requisito do Google (revisão 2 da ficha): "1-4" escolhido numa lista vira data no Google; a lista mostra
    # "Faixa 1-4" e as fórmulas convertem pela posição na lista (ROTULOS_FAIXA, mesma ordem de FAIXAS)
    lista("faixas", "Faixas", "28.1", ROTULOS_FAIXA)
    lista("modos", "Modo do Criador", "6.7.1", ["Faixa do livro", "Por nível — Sugestão", "Ajustar do bestiário"])
    lista("racas", "Raças", "05", [r["raca"] for r in F.racas()])
    lista("caminhos", "Caminhos", "06.3", [c["caminho"] for c in F.caminhos()])
    lista("sim_nao", "Sim/Não", "convenção da planilha", ["Sim", "Não"])
    lista("execucao", "Ser racional?", "23.5", ["Pode Executar", "Não Executa"])
    lista("faccoes_criador", "Facção ou origem", "27.16", faccoes() + FACCOES_CRIADOR_EXTRA)
    lista("criaturas", "Criaturas do bestiário", "28.11", [f["nome"] for f in fichas])
    lista("filtro_faixa", "Faixa (filtro)", "28.1", ["Todas"] + ROTULOS_FAIXA)
    lista("filtro_tipo", "Tipo (filtro)", "28.1", ["Todos"] + TIPOS)
    lista("filtro_elemento", "Fraqueza (filtro)", "20.1", ["Qualquer"] + ELEMENTOS)
    lista("filtro_faccao", "Facção (filtro)", "28.11", ["Todas"] + list(dict.fromkeys(f["faccao"] for f in fichas)))
    lista("filtro_ambiente", "Ambiente (filtro)", "Sugestão da planilha (H8)", ["Todos"] + AMBIENTES)
    lista("ambiente_aleatorio", "Ambiente (encontro aleatório)", "Sugestão da planilha (H8)",
          ["Qualquer"] + AMBIENTES)
    lista("composicoes", "Composição", "27.4", ["Sortear"] + [c["composicao"] for c in composicoes()])
    lista("carregar", "Carregar encontro", "6.10", ["Nenhum", "A", "B", "C", "Aleatório"])
    lista("surpresa", "Surpresa", "19.3", ["Ninguém", "Grupo surpreendido", "Inimigos surpreendidos"])
    conds = [c["condicao"] for c in F.condicoes()]
    lista("condicoes_combate", "Condição (Combate)", "21.5", [c for c in conds if c not in ("Quebrado", "Morrendo")])
    lista("condicoes_acao", "Condição (ação de inimigo)", "21.5 e 28.4",
          [c for c in conds if c not in ("Quebrado", "Surpreso", "Morrendo")])
    lista("fontes", "Fonte do dano", "20.3", [f for f, _ in fontes_tenacidade()])
    lista("tipos_acao", "Tipo de ação", "28.4",
          ["Ataque normal", "Especial de dano 1 alvo (até 1,5×)", "Especial de dano 2–3 alvos (dano cheio por alvo)",
           "Especial de controle", "Reação"])
    lista("alcances", "Alcances", "18.3", F.alcances())
    lista("tr", "Testes de Resistência", "04.6", [t["tr"] for t in F.testes_resistencia()])
    # Fase 2 (6.6, 6.11, 6.12)
    lista("racas_sortear", "Raça (NPC)", "05", ["Sortear"] + [r["raca"] for r in F.racas()])
    lista("caminhos_npc", "Caminho (NPC)", "06.3 e 27.12", ["Sortear"] + [c["caminho"] for c in F.caminhos()]
          + ["Nenhum"])
    lista("papeis", "Papel do NPC", "6.6", ["Sortear"] + PAPEIS)
    lista("caminhos_elenco", "Caminho (Elenco)", "06.3 e 27.12", [c["caminho"] for c in F.caminhos()] + ["Nenhum"])
    lista("papeis_elenco", "Papel (Elenco)", "6.6", PAPEIS)
    lista("faixa_bloco", "Bloco de combate do NPC", "28.3", ["Nenhum"] + ROTULOS_FAIXA + ["Do grupo"])
    lista("tipo_bloco", "Tipo do bloco", "28.1", ["Comum", "Elite"])
    lista("leitura", "Leitura do encontro", "27.4 (H6)", ["Passagem", "Típico", "Pesado"])
    lista("marco", "O que aconteceu", "26.1 e 27.8", ["Subiu de nível", "Entrou em faixa nova", "Fim de arco"])
    import mestre_dados3 as D3          # Fase 3 (6.2–6.5, 6.13–6.15)
    D3.listas3(lista)
    return L


if __name__ == "__main__":
    for b in blocos():
        print(f"{b['id']:<20} {len(b['linhas']):>4} linhas × {len(b['cabecalho'])} colunas — {b['titulo']}")
    for l in listas():
        print(f"lista {l['id']:<20} {len(l['valores']):>3} valores")
    fi = bestiario()
    print(sum(1 for f in fi if f["execucao"] == "Não declarado"), "fichas sem Execução declarada")
    print(len(acoes()), "ações;", max(sum(isinstance(p, tuple) for p in a["pecas"]) for a in acoes()),
          "marcadores no máximo")
