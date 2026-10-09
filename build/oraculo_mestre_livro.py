# -*- coding: utf-8 -*-
"""
oraculo_mestre_livro.py — tabelas do livro TRANSCRITAS para o oráculo (com a seção ao lado) e um parser
PRÓPRIO das 32 fichas do capítulo 28 (não importa build\\mestre_dados.py nem build\\ficha_dados.py).
Usado por build\\oraculo_mestre*.py e pelas suítes dados/bestiario.
"""
import re
from functools import lru_cache
from pathlib import Path

LIVRO = Path(__file__).resolve().parent.parent / "livro-v1.0"
FAIXAS = ["1-4", "5-8", "9-12", "13-16", "17-20"]
TIPOS = ["Comum", "Elite", "Boss"]
ELEM = ["Físico", "Fogo", "Gelo", "Raio", "Vento", "Quântico", "Imaginário"]                 # 20.1

# 28.3 — por faixa: (PV C/E/B, Defesa, RD, Tenacidade, VEL, Ataque, Dano em dados, DT, TR)
ANC = {
    "1-4": ((50, 120, 305), (13, 15, 16), (0, 2, 4), (3, 5, 10), (11, 12, 13), 7,
            (("1d6", 3), ("2d6", 7), ("3d6", 10)), (12, 13, 14), (1, 2, 3)),
    "5-8": ((70, 160, 410), (16, 18, 19), (0, 2, 4), (3, 6, 11), (12, 13, 15), 9,
            (("2d6", 7), ("3d8", 13), ("4d8 + 2", 20)), (14, 15, 16), (3, 4, 5)),
    "9-12": ((95, 225, 580), (19, 21, 22), (0, 3, 6), (4, 7, 12), (13, 15, 16), 11,
             (("2d8", 9), ("4d8 + 1", 19), ("5d10 + 1", 28)), (16, 17, 18), (4, 5, 6)),
    "13-16": ((125, 295, 750), (20, 22, 23), (0, 3, 6), (4, 6, 12), (14, 16, 18), 12,
              (("3d6 + 2", 12), ("4d10 + 2", 24), ("6d10 + 3", 36)), (17, 18, 19), (5, 6, 7)),
    "17-20": ((155, 365, 935), (24, 26, 27), (0, 4, 8), (4, 7, 13), (15, 17, 19), 13,
              (("3d8 + 3", 16), ("5d12", 32), ("7d12 + 3", 48)), (19, 20, 21), (7, 8, 9)),
}
# 28.4 regra 5 / H2 (ficha do livro ou Sugestão) — por faixa: Comum, Elite, Boss
ESPECIAL = {"1-4": (("1d6 + 1", 4), ("3d6", 10), ("3d8 + 2", 15)),
            "5-8": (("2d6 + 3", 10), ("4d8 + 1", 19), ("4d8 + 12", 30)),
            "9-12": (("2d8 + 4", 13), ("5d10 + 1", 28), ("7d10 + 4", 42)),
            "13-16": (("3d6 + 8", 18), ("6d10 + 3", 36), ("9d10 + 5", 54)),
            "17-20": (("3d8 + 11", 24), ("7d12 + 3", 48), ("10d12 + 7", 72))}
NFRAQ = {"Comum": "1-2", "Elite": "3", "Boss": "4"}                                       # 28.2 regra 7
NSUG = {"Comum": 2, "Elite": 3, "Boss": 4}                                                 # H12
ACOES = {"Comum": 1, "Elite": 1.5, "Boss": 2}                                              # 28.2 regra 5
EF_INIMIGO = (2, 4, 5, 6, 8)                    # 28.3: TR do Elite = Eficiência da faixa
ORC = ((88, 352), (119, 476), (168, 672), (218, 872), (271, 1084))                       # 27.4
DT_FRAQ = (13, 14, 15, 16, 17)                                                             # 20.2
DT = {"Média": (13, 16, 19, 22, 25), "Difícil": (16, 19, 23, 27, 30)}                      # 27.2
PH_MAX = {3: (4, 5, 6), 4: (5, 6, 7), 5: (6, 7, 8), 6: (7, 8, 9)}                          # 16.2 (início = −2)
VERBA = (200, 500, 1200, 2500, 5000)                                                       # 24.5
CONE = ("Nível 1", "Nível 2", "Nível 3", "Nível 4", "Nível 5")                              # 25.1
RELIQ = ("Tier I", "Tier I, virando Tier II no nível 7", "Tier II", "Tier III",
         "Tier III, virando Tier IV no nível 18")                                         # 25.1
ATTR = ("81%", "76%", "76%", "75%", "73%")                                                 # 27.7
COMPOS = [("1 Boss + 1 Comum", (1, 0, 1), "uma ameaça com nome, um estorvo. O combate é um duelo com interrupção",
           "3 a 5 Ciclos"),
          ("1 Elite + 4 Comuns", (0, 1, 4), "um comandante e a tropa dele. O grupo escolhe entre limpar os lados ou "
                                            "ir no chefe", "3 a 4 Ciclos"),
          ("3 Elites", (0, 3, 0), "três problemas simultâneos. É a mais pesada das quatro em dano recebido",
           "3 a 4 Ciclos"),
          ("7 Comuns", (0, 0, 7), "pelotão. Morre rápido e ainda assim morde", "2 a 3 Ciclos")]      # 27.4
# 20.5 — Elemento: (nº de dados, faces, multiplicador da Eficiência)
QUEBRA = {"Físico": (2, 6, 2), "Fogo": (2, 6, 2), "Raio": (1, 6, 1), "Vento": (1, 6, 1), "Gelo": (0, 0, 1),
          "Quântico": (0, 0, 1), "Imaginário": (0, 0, 1)}
# 20.3 — Redução de Tenacidade bruta por fonte
REDUCAO = {"Ataque Básico": 1, **{f"Habilidade de Nível {k}": max(2, k) for k in range(1, 8)}, "Ultimate": 5,
           "Dano Contínuo": 0}
# 21.5 — condição: (dados, faces, por acúmulo, soma Eficiência, % PV, teto ×Ef, atrasa, teto de acúmulos, DC)
CONDICOES = {
    "Sangramento": (0, 0, 0, 0, 5, 3, 0, 5, 1), "Queimadura": (2, 6, 0, 1, 0, 0, 0, 5, 1),
    "Choque": (1, 6, 0, 1, 0, 0, 0, 5, 1), "Cisalhamento de Vento": (1, 6, 1, 0, 0, 0, 0, 5, 1),
    "Embaraço": (1, 6, 1, 0, 0, 0, 1, 5, 0), "Aprisionamento": (1, 6, 0, 1, 0, 0, 2, 5, 0),
    "Congelado": (0, 0, 0, 0, 0, 0, 0, 1, 0), "Lentidão": (0, 0, 0, 0, 0, 0, 0, 1, 0),
    "Marcado": (0, 0, 0, 0, 0, 0, 0, 3, 0), "Silenciado": (0, 0, 0, 0, 0, 0, 0, 1, 0),
    "Vulnerável": (0, 0, 0, 0, 0, 0, 0, 5, 0), "Controlado": (0, 0, 0, 0, 0, 0, 0, 1, 0),
    "Corrupção": (0, 0, 0, 0, 0, 0, 0, 5, 0), "Surpreso": (0, 0, 0, 0, 0, 0, 0, 1, 0)}
# 21.5 — efeito e duração, como o livro escreve (sem o negrito e a crase): o painel C9b mostra os dois (Fase 4)
TEXTO_21_5 = {
    "Sangramento": ("Dano Contínuo = 5% dos PV máximos, teto 3 × Eficiência", "2 turnos"),
    "Queimadura": ("Dano Contínuo 2d6 + Eficiência (Fogo)", "2 turnos"),
    "Choque": ("Dano Contínuo 1d6 + Eficiência (Raio)", "3 turnos"),
    "Cisalhamento de Vento": ("Dano Contínuo 1d6 por acúmulo (Vento), 1 acúmulo por ataque seu de Vento", "2 turnos"),
    "Embaraço": ("1d6 por acúmulo (só por ataques) e Atrasa 1 casa", "1 turno"),
    "Aprisionamento": ("1d6 + Eficiência e Atrasa 2 casas", "1 turno"),
    "Congelado": ("Só inimigos. Comum perde o turno; Elite e Boss são Atrasados 2 casas e perdem a ação especial",
                  "1 turno"),
    "Lentidão": ("Ação de Movimento não muda a Distância; só sai do lugar com Esforço Total", "fonte"),
    "Marcado": ("+1 em Testes de Ataque de quem marcou", "fonte"),
    "Silenciado": ("não pode usar Habilidade de Nível 4 ou maior", "1 turno"),
    "Vulnerável": ("+1 dado de dano da fonte indicada", "fonte"),
    "Controlado": ("quem aplicou decide as ações do alvo, sem Habilidade, Ultimate nem recursos", "fonte"),
    "Corrupção": ("+1 no dano de cada Dano Contínuo seu no alvo", "fim do combate"),
    "Surpreso": ("casa pulada no primeiro Ciclo", "1 Ciclo")}
RACAS = ["Humano", "Xianzhouíta", "Vidyadhara", "Vulpes", "Haloviano", "Avginiano", "Intellitron"]      # 05
MORRENDO_VANT = ("Xianzhouíta", "Vulpes", "Avginiano")                                    # 23.5
# H8 — ambiente por facção (padrão da aba Tabelas)
AMBIENTE = [("Fragmentum", "Colônia ou mina abandonada"), ("Fragmentum", "Ruína"),
            ("Legião da Antimatéria", "Frente de guerra"), ("Legião da Antimatéria", "Lua-forja"),
            ("Corporação da Paz Interastral", "Estação"), ("Corporação da Paz Interastral", "Cidade corporativa"),
            ("Aliança Xianzhou", "Nave-cidade"), ("Xianzhou", "Nave-cidade"),
            ("Tolos Mascarados", "Teatro, festa ou multidão"), ("Cavaleiros da Beleza", "Clínica ou ateliê"),
            ("Caçadores de Stellaron", "Qualquer lugar onde o grupo esteja"),
            ("Culto da Inexistência", "Lugar esvaziado"), ("Autômato", "Instalação antiga"),
            ("Autômato de guerra", "Instalação antiga"), ("Stellaron", "Mundo com Stellaron"),
            ("Emanadora da Inexistência", "Mundo com Stellaron"), ("Emanador", "Mundo com Stellaron")]
DESDE = {"criaturas": "28.11", "fases": "28.5–28.10"}


def ancora(fx, tipo):
    t = TIPOS.index(tipo)
    a = ANC[fx]
    e, m = a[6][t]
    return {"pv": a[0][t], "defesa": a[1][t], "rd": a[2][t], "ten": a[3][t], "vel": a[4][t], "ataque": a[5],
            "dano_e": e, "dano_m": m, "dt": a[7][t], "tr": a[8][t], "esp_e": ESPECIAL[fx][t][0],
            "esp_m": ESPECIAL[fx][t][1], "firmeza": "sem Firmeza" if tipo == "Comum" else "com Firmeza",
            "acoes": ACOES[tipo], "nfraq": NFRAQ[tipo], "nsug": NSUG[tipo]}


def eficiencia(n):                                                                         # 26.2
    return 2 + (n - 1) // 3


# ---------------------------------------------------------------------------
# Parser próprio das fichas (28.6–28.11)
# ---------------------------------------------------------------------------

def limpo(s):
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def _md(cap):
    return sorted(LIVRO.glob(f"{cap}-*.md"))[0].read_text(encoding="utf-8").splitlines()


def _cels(linha):
    return [limpo(x) for x in linha.strip().strip("|").split("|")]


@lru_cache(None)
def bestiario_md():
    linhas = _md("28")
    ini = next(i for i, l in enumerate(linhas) if l.startswith("## 28.11"))
    idx = []
    for l in linhas[ini:]:
        c = _cels(l) if l.startswith("|") else []
        if len(c) == 7 and c[0].isdigit():
            m = re.search(r"(\d) fases", c[2])
            idx.append({"n": int(c[0]), "nome": c[1], "tipo": c[2].split(",")[0], "faixa": c[3], "faccao": c[4],
                        "pv": int(c[5]), "fraquezas": [x.strip() for x in c[6].split(",")],
                        "fases": int(m.group(1)) if m else 1})
    blocos, atual, dentro = {}, None, False
    for l in linhas:
        if l.startswith("## "):
            dentro = bool(re.match(r"## 28\.(6|7|8|9|10) ", l))
            atual = None
        elif dentro and l.startswith("### "):
            atual = l[4:].strip()
            blocos[atual] = []
        elif dentro and atual:
            blocos[atual].append(l)
    for f in idx:
        ls = blocos[next(t for t in blocos if t == f["nome"] or t.startswith(f["nome"] + ","))]
        tl = limpo(next(l for l in ls if l.startswith("*") and "faixa" in l))
        partes = [x.strip() for x in tl.split("·")]
        f["origem_card"] = " · ".join(x for x in partes[1:] if not x.startswith("faixa") and "fase" not in x)
        f["frase"] = next((limpo(l[2:]) for l in ls if l.startswith('> *"')), "")
        campos, acoes, fases, fase, ritmo_de = {}, [], [], 0, None
        tab = None
        for l in ls:
            if l.startswith("| **") and tab is None:
                c = _cels(l)
                campos[c[0]] = c[1]
            m = re.match(r"^\*\*Fase (\d) — (.+?) \((\d+) a (\d+) PV\)\*\*", l)
            if m:
                fase = int(m.group(1))
                fases.append({"fase": fase, "nome": m.group(2), "topo": int(m.group(3)), "piso": int(m.group(4)),
                              "fraq": None, "ten": None, "ritmo": ""})
                tab = "fase"
            elif l.startswith("**") and "—" in l and fases and not l.startswith("**Na Fila"):
                if l.startswith(("**Ataques", "**Ação da fase")):
                    fases[-1]["ritmo"] = limpo(l.split("—", 1)[1]).rstrip(":")
            elif l.startswith("| ") and fases and tab == "fase":
                c = _cels(l)
                if c[0] == "Fraquezas" and fases[-1]["fraq"] is None:
                    fases[-1]["fraq"] = [x.strip() for x in c[-1].split(",")]
                if c[0] == "Tenacidade" and fases[-1]["ten"] is None:
                    fases[-1]["ten"] = int(re.match(r"\d+", c[-1]).group(0))
            elif l.startswith("- **"):
                acoes.append({"fase": fase, "texto": limpo(l[2:])})
            elif l.startswith("**Na Fila:**"):
                f["nafila"] = limpo(l[len("**Na Fila:**"):])
        f["campos"] = campos
        f["fases_d"] = fases
        f["acoes"] = acoes
        f["res"] = "" if campos.get("Resistências", "—") == "—" else campos["Resistências"]
        nf = f["nafila"].lower()
        f["execucao"] = "Não" if ("não pode executar" in nf or "não executa" in nf) else \
            "Pode" if "pode executar" in nf else "Não declarado"
        f["esp"] = []
        for a in acoes:
            m = re.match(r"^.+? \((.+?)\)", a["texto"])
            r = re.search(r"recarga (\d) Ciclos", m.group(1)) if m else None
            if r and len(f["esp"]) < 3:
                f["esp"].append((a["texto"].split(" (")[0], int(r.group(1))))
        f["ten"] = ancora(f["faixa"], f["tipo"])["ten"]
        f["custo"] = f["pv"] * 1.5 if f["nome"] == "Escória de Stellaron" else f["pv"]     # 28.10
        ori = [x.strip() for x in f["origem_card"].split("·")]
        f["origem2"] = next((x for x in ori if x != f["faccao"] and x not in f["faccao"]), "")
        if f["fases"] == 2:
            f["lim2"], f["lim3"] = fases[1]["topo"], ""
        elif f["fases"] == 3:
            f["lim2"], f["lim3"] = fases[1]["topo"], fases[2]["topo"]
        else:
            f["lim2"] = f["lim3"] = ""
    return idx


def ficha(nome):
    for f in bestiario_md():
        if f["nome"] == nome:
            return f
    return None


def reescrever(texto, f_orig, fx_nova, tipo, pv_novo):
    """Ação da base reescrita para a faixa nova (H3): dano normal, 1,5×, de Comum, DT e limiares de PV."""
    a0, a1 = ancora(f_orig["faixa"], f_orig["tipo"]), ancora(fx_nova, tipo)
    c0, c1 = ancora(f_orig["faixa"], "Comum"), ancora(fx_nova, "Comum")

    def dano(m):
        e, med = m.group(1), int(m.group(3))
        pre = m.group(2) or ""
        for (oe, om), (ne, nm) in (((a0["dano_e"], a0["dano_m"]), (a1["dano_e"], a1["dano_m"])),
                                   ((a0["esp_e"], a0["esp_m"]), (a1["esp_e"], a1["esp_m"])),
                                   ((c0["dano_e"], c0["dano_m"]), (c1["dano_e"], c1["dano_m"]))):
            if e == oe and med == om:
                return f"{ne} · {pre}{nm}"
        return m.group(0)
    s = re.sub(r"(\d+d\d+(?: \+ \d+)?) · (média )?(\d+)", dano, texto)
    s = re.sub(r"DT (\d+)", lambda m: f"DT {a1['dt']}" if int(m.group(1)) == a0["dt"] else m.group(0), s)
    s = re.sub(r"(\d+)( PV ou menos)", lambda m: f"{int(m.group(1)) * pv_novo // f_orig['pv']}{m.group(2)}", s)
    s = re.sub(r"(metade dos PV \()(\d+)\)", lambda m: f"{m.group(1)}{int(m.group(2)) * pv_novo // f_orig['pv']})", s)
    return s
