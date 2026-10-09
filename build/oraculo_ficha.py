# -*- coding: utf-8 -*-
"""
oraculo_ficha.py — Oráculo Python INDEPENDENTE da Ficha de Personagem
("Explorando Galáxias" v1.2).

O QUE ELE FAZ
    Implementa as regras de personagem do livro v1.2 direto em Python, com
    constantes próprias (cada uma com a seção do livro no comentário), para
    servir de gabarito ao teste diferencial da planilha (build/testar_ficha.py,
    suítes `ouro` e `oraculo`).

    Independência, de propósito:
      - NÃO importa build/gerar_ficha.py nem build/ficha_dados.py;
      - NÃO lê fórmula da planilha;
      - a única leitura do livro é o catálogo de NOMES das Bênçãos
        ("### N. Nome" nos capítulos 07 a 15); o tier sai do número pela regra
        de 06.7 (6 do Tier I, 4 do Tier II, 2 do Tier III), não da linha
        "**Tier …**" que o gerador lê.

    API:
        calcular(entradas: dict) -> dict
    `entradas` usa nomes lógicos (ver ENTRADAS_EXEMPLO); campo ausente = vazio.
    A saída traz as estatísticas do inventário 1.1–1.8 do plano e
    `avisos`: lista de códigos (ver AVISOS).

COMO USAR
    $env:PYTHONUTF8="1"; python "build\\oraculo_ficha.py"     (calcula a Nadir de 29.7)
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LIVRO = RAIZ / "livro-v1.0"          # nome histórico da pasta: o conteúdo é a v1.2

# ---------------------------------------------------------------------------
# Constantes do livro (seção no comentário)
# ---------------------------------------------------------------------------

ATRIBUTOS = ("Poder", "Agilidade", "Vigor", "Sincronia", "Discernimento", "Presença")  # 04.1

# 04.2 — Tabela de Bônus de Atributo
BONUS = {8: -1, 9: -1, 10: 0, 11: 0, 12: 1, 13: 1, 14: 2, 15: 3, 16: 3, 17: 4, 18: 4,
         19: 5, 20: 5}

ARRAY_OFICIAL = (15, 14, 13, 12, 10, 8)                       # 03 Passo 4, Método A
CUSTO_COMPRA = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 10}   # 03 Passo 4, Método B
VERBA_COMPRA = 28                                             # 03 Passo 4
TETO_CRIACAO, TETO_ATRIBUTO = 15, 20                          # 03 "Os dois tetos"
NIVEIS_AUMENTO = (3, 6, 9, 12, 15, 18)                         # 04.3

# 05 — bônus racial: opções do +2 (Humano: livre, +2 em um ou +1 em dois)
RACAS = {
    "Humano": None,
    "Xianzhouíta": ("Vigor", "Sincronia"),
    "Vidyadhara": ("Vigor", "Poder"),
    "Vulpes": ("Agilidade", "Discernimento"),
    "Haloviano": ("Discernimento", "Presença"),
    "Avginiano": ("Agilidade", "Presença"),
    "Intellitron": ("Sincronia", "Poder"),
}
# 05 (v1.2): os 6 Atributos redistribuídos para que cada um apareça em exatamente 2 Raças e
# nenhum par se repita. Antes, Poder e Agilidade eram concedidos por ZERO Raças — só o Humano
# os alcançava, pelo bônus livre, e isso tornava o Humano porta obrigatória de qualquer
# conceito que precisasse de um dos dois. Nenhuma Raça tem mais opção única.

# 04.4 — Perícias e atributo (Sintonia: Discernimento ou Sincronia, fixo na criação)
PERICIAS = (("Atletismo", "Poder"), ("Acrobacia", "Agilidade"), ("Furtividade", "Agilidade"),
            ("Pilotagem", "Agilidade"), ("Resistência", "Vigor"), ("Tecnologia", "Sincronia"),
            ("Pesquisa", "Sincronia"), ("Ciência", "Sincronia"), ("Mecânica", "Sincronia"),
            ("Percepção", "Discernimento"), ("Sobrevivência", "Discernimento"),
            ("Intuição", "Discernimento"), ("Investigação", "Discernimento"),
            ("Persuasão", "Presença"), ("Intimidação", "Presença"), ("Enganação", "Presença"),
            ("Liderança", "Presença"), ("Sintonia", None))

# 04.6 — Testes de Resistência
TESTES_RESISTENCIA = (("Potência Física", "Poder"), ("Reflexos", "Agilidade"),
                      ("Resistência Física", "Vigor"), ("Resistência Mental", "Sincronia"),
                      ("Percepção Mental", "Discernimento"), ("Força de Vontade", "Presença"))

# 06.3 — (atributos de Habilidade, 3 Perícias, N, Bônus de VEL)
CAMINHOS = {
    "A Destruição": (("Poder", "Vigor"), ("Atletismo", "Sobrevivência", "Resistência"), 6, 1),
    "A Inexistência": (("Discernimento", "Sincronia"), ("Percepção", "Pesquisa", "Furtividade"), 4, 2),
    "A Harmonia": (("Presença",), ("Liderança", "Sintonia", "Persuasão"), 3, 2),
    "A Abundância": (("Presença", "Sincronia"), ("Liderança", "Intuição", "Sobrevivência"), 5, 1),
    "A Recordação": (("Sincronia", "Discernimento"), ("Intimidação", "Investigação", "Ciência"), 3, 1),
    "A Erudição": (("Sincronia",), ("Ciência", "Pesquisa", "Tecnologia"), 3, 1),
    "A Euforia": (("Presença", "Discernimento"), ("Enganação", "Acrobacia", "Persuasão"), 3, 3),
    "A Caça": (("Agilidade",), ("Furtividade", "Percepção", "Acrobacia"), 2, 4),
    "A Preservação": (("Vigor", "Poder"), ("Resistência", "Atletismo", "Intuição"), 5, 0),
}
CAPITULO_CAMINHO = {"07": "A Destruição", "08": "A Inexistência", "09": "A Harmonia",
                    "10": "A Abundância", "11": "A Recordação", "12": "A Erudição",
                    "13": "A Euforia", "14": "A Caça", "15": "A Preservação"}

# 24.1 — Armaduras: (Defesa, VEL, RD, penalidade de Agilidade, Esquiva permitida, Espaço)
ARMADURAS = {"Leve": (3, 1, 0, 0, True, 1), "Média": (5, 0, 0, 0, True, 2),
             "Pesada": (6, -2, 2, -2, False, 3)}
PERICIAS_PENALIZADAS_PESADA = ("Acrobacia", "Furtividade", "Pilotagem")    # D4 (24.1)

# 24.2 / 18.5 — Armas: (face, dados extras iniciais, alcance, atributo, Espaço)
ARMAS = {"Leve": (8, 0, "Pessoal", "Agilidade", 0.5), "Média": (10, 0, "Pessoal", None, 1),
         "Pesada": (12, 0, "Pessoal", "Poder", 2), "Disparo curto": (8, 0, "Média", "Agilidade", 1),
         "Disparo longo": (10, 0, "Longa", "Agilidade", 2), "Energia": (8, 1, "Longa", "Sincronia", 2)}
ESCALA_DISTANCIA = ("Pessoal", "Curta", "Média", "Longa", "Extrema")        # 18.8

# 16.3 — Níveis de Habilidade: (dano n, face, cura n, face, PH, RT)
NIVEIS_HAB = {1: (6, 6, 5, 8, 1, 2), 2: (5, 10, 6, 10, 1, 2), 3: (6, 12, 8, 12, 2, 3),
              4: (6, 20, 7, 20, 3, 4), 5: (10, 20, 10, 20, 4, 5), 6: (14, 20, 14, 20, 5, 6),
              7: (18, 20, 18, 20, 6, 7)}
ALCANCE_MAX_HAB = {1: "Curta", 2: "Média", 3: "Longa"}                    # 16.3 (4+: Extrema)

# 26.2 — Habilidades conhecidas e Nível máximo por nível do personagem
HAB_CONHECIDAS = (1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 8, 8, 8, 8)
NIVEL_MAX_HAB = (1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7)
# 26.2 — slots de Eficácia (Perícias, Testes de Resistência)
SLOTS_EFICACIA = {1: (0, 0), 5: (1, 1), 8: (2, 1), 11: (2, 2), 14: (3, 2), 17: (4, 2), 20: (5, 3)}

# 17.3 — Ultimate por faixa: (Nível equivalente, dano n, face, cura n, face)
ULTIMATE = {1: (2, 5, 10, 6, 10), 2: (3, 6, 12, 8, 12), 3: (4, 6, 20, 7, 20),
            4: (5, 10, 20, 10, 20), 5: (6, 14, 20, 14, 20)}

# 20.5 — Dano de Quebra: (dados, face, multiplicador da Eficiência)
QUEBRA = {"Físico": (2, 6, 2), "Fogo": (2, 6, 2), "Raio": (1, 6, 1), "Vento": (1, 6, 1),
          "Gelo": (0, 0, 1), "Quântico": (0, 0, 1), "Imaginário": (0, 0, 1)}

# 25.2 — Cone de Luz: nível -> (bônus numérico, bônus de PV, "e"/"ou")
CONE = {1: (1, 10, "ou"), 2: (1, 10, "e"), 3: (2, 25, "ou"), 4: (2, 25, "e"), 5: (3, 50, "ou")}
TETO_CONE_NUM, TETO_CONE_PV = 3, 50                                          # 25.2 Sobreposição
SOBREPOSICAO_PV = 10                     # 25.2 (v1.1): cada Sobreposição soma +1 e +10 PV

# 25.3 — Relíquias: slot -> valores por Tier I..IV
RELIQUIAS = {"Cabeça": (10, 20, 35, 50), "Mãos": (2, 4, 6, 8), "Tronco": (1, 1, 2, 2),
             "Botas": (2, 3, 4, 5), "Esfera Planar": (2, 4, 6, 8),
             "Corda de Ligação": (10, 15, 20, 25)}

# 27.2 — DT por faixa
DT_FAIXA = {"Trivial": (8, 9, 10, 11, 12), "Fácil": (10, 12, 14, 16, 18),
            "Média": (13, 16, 19, 22, 25), "Difícil": (16, 19, 23, 27, 30),
            "Muito Difícil": (19, 23, 27, 31, 35), "Heroica": (22, 26, 31, 34, 38)}
DT_FRAQUEZA = (13, 14, 15, 16, 17)                                        # 20.2
VERBA_MARCO = (200, 500, 1200, 2500, 5000)                                 # 24.5

VANTAGEM_PERICIA = {"Vulpes": ("Persuasão", "Intimidação", "Enganação", "Liderança"),
                    "Intellitron": ("Tecnologia", "Mecânica")}               # 05
VANTAGEM_TR = {"Xianzhouíta": tuple(t for t, _ in TESTES_RESISTENCIA),
               "Avginiano": ("Resistência Mental", "Percepção Mental", "Força de Vontade"),
               "Vulpes": ("Força de Vontade",)}                               # 05, 22.6
# 05 (v1.2): vazio de propósito. O Corpo das Marés do Vidyadhara era a única Vantagem
# condicional em Teste de Resistência do livro (contra afogamento, frio e água) e virou
# regeneração + imunidade a afogamento, que não mexem em Teste de Resistência. A estrutura
# fica, porque 22.6 segue sendo o lugar onde uma Vantagem condicional nova entraria.
VANTAGEM_TR_CONDICIONAL = {}
VANTAGEM_MORRENDO = ("Xianzhouíta", "Vulpes", "Avginiano")                 # 23.5 (v1.1 nomeia as três)

AVISOS = {
    "NIVEL_FORA": "nível fora de 1–20 (conta com o valor limitado)",
    "JOGADORES_INVALIDO": "nº de jogadores fora de 1–6",
    "JOGADORES_FORA_DA_TABELA": "nº de jogadores fora de 3–6 (fora da tabela do livro)",
    "ATRIBUTO_FORA_8_20": "atributo fora de 8–20",
    "ATRIBUTO_ACIMA_15_NA_CRIACAO": "atributo acima de 15 antes da Raça",
    "ARRAY_INVALIDO": "array oficial: cada valor 15, 14, 13, 12, 10, 8 uma vez",
    "COMPRA_ACIMA_DE_28": "Compra de Pontos passou de 28",
    "BONUS_RACIAL_INVALIDO": "bônus racial fora das opções da Raça",
    "BONUS_RACIAL_MESMO_ATRIBUTO": "+1 em dois exige atributos diferentes",
    "AUMENTO_MESMO_ATRIBUTO": "aumento +1 em dois exige atributos diferentes",
    "AUMENTO_DESPERDICADO": "aumento passou do teto 20",
    "AUMENTO_ANTES_DO_NIVEL": "aumento de atributo de um marco que o nível ainda não alcançou",
    "RESSONANCIA_ANTES_DO_NIVEL": "Ressonância escolhida antes do nível 5/10/15/20",
    "RESSONANCIA_III_REPETIDA": "Ressonância III marcada em mais de uma Habilidade (vale só a primeira)",
    "ATRIBUTO_HABILIDADE_INVALIDO": "Atributo de Habilidade fora do que o Caminho permite",
    "PERICIAS_A_MAIS": "Perícias escolhidas acima do permitido",
    "PERICIA_DO_CAMINHO_ESCOLHIDA": "Perícia do Caminho já tem Eficiência: escolha outra",
    "EFICACIA_SEM_EFICIENCIA": "Eficácia só em Perícia com Eficiência",
    "EFICACIA_PERICIAS_A_MAIS": "slots de Eficácia em Perícias excedidos",
    "EFICACIA_TR_A_MAIS": "slots de Eficácia em Testes de Resistência excedidos",
    "HABILIDADES_A_MAIS": "Habilidades conhecidas acima do permitido",
    "HABILIDADE_NIVEL_ACIMA": "Habilidade acima do Nível máximo",
    "BENCAO_EM_SLOT_FUTURO": "Bênção num slot que o nível ainda não liberou",
    "BENCAO_TIER_ACIMA_DO_SLOT": "Bênção de tier acima do nível do slot",
    "BENCAO_REPETIDA": "Bênção repetida",
    "BENCAO_DE_OUTRO_CAMINHO": "Bênção de outro Caminho",
    "CONE_NIVEL_ACIMA": "Cone de Luz acima do Nível permitido",
    "SOBREPOSICOES_A_MAIS": "Sobreposições acima de uma por faixa",
    "SOBREPOSICOES_ACIMA_DO_TETO": "Sobreposições além do teto +3 do Cone (25.2)",
    "CONJUNTOS_DANO_ACIMA_DE_3": "bônus de Conjunto acima de +3 na mesma rolagem (25.3)",
    "ESQUIVA_PROIBIDA": "Esquiva proibida com Armadura Pesada",
    "RD_NO_TETO": "RD limitada ao teto",
    "VEL_FORA_7_25": "Velocidade fora de 7–25",
    "BONUS_TEMPORARIO_NO_TETO": "bônus temporário limitado ao teto da faixa",
    "SOBRECARGA": "acima da capacidade: Lentidão",
    "IMOVEL": "acima do dobro da capacidade: não se move",
    "MEMO_FORA_DA_RECORDACAO": "Memoespírito só na Recordação",
    "MEMO_ATRIBUTO_ACIMA_5": "Memoespírito: máximo 5 pontos por Atributo",
    "MEMO_PONTOS_A_MAIS": "Memoespírito: pontos acima do total",
    "MEMO_EVOLUCAO_ANTES_DO_NIVEL": "Evolução antes do nível 8/14/20",
    "MEMO_EVOLUCAO_REPETIDA": "Evolução repetida",
    "MEMO_BONUS_MENORES": "Memoespírito: escolha 3 Bônus menores diferentes",
}

# ---------------------------------------------------------------------------
# Regras por nível
# ---------------------------------------------------------------------------


def eficiencia(n):                       # 02.3 / 26.4
    return 2 + (n - 1) // 3


def faixa(n):                            # 26.3 (1-4, 5-8, 9-12, 13-16, 17-20)
    return (n - 1) // 4 + 1


def especializacao(n):                   # 26.5
    return 0 if n < 5 else 1 if n < 11 else 2 if n < 17 else 3


def slots_eficacia(n):                   # 26.4
    chave = max(k for k in SLOTS_EFICACIA if k <= n)
    return SLOTS_EFICACIA[chave]


def teto_bonus(n):                       # 26.6
    return 3 if n <= 9 else 4 if n <= 15 else 5


def dados_ab(n):                         # 18.5 / 26.2
    return 1 + (n - 1) // 4


def tier_reliquia(n):                    # 25.1 / 25.3
    return 1 if n <= 6 else 2 if n <= 12 else 3 if n <= 17 else 4


def ph_grupo(n, jogadores):              # 16.2 / 26.3
    extra = 1 if 9 <= n <= 16 else 2 if n >= 17 else 0
    mx = 1 + jogadores + extra
    return mx, mx - 2, 1 if n <= 8 else 2


def bonus(v):
    return BONUS[max(8, min(20, v))]


def media(n, face):                      # 02.5: média arredondada para baixo
    return (n * (face + 1)) // 2


def rolagem(b):
    return f"d20+{b}" if b >= 0 else f"d20{b}"


def texto_dano(n, face, fixo):
    if n <= 0:
        return str(fixo)
    s = f"{n}d{face}"
    return s + (f"+{fixo}" if fixo > 0 else f"{fixo}" if fixo < 0 else "")


# ---------------------------------------------------------------------------
# Catálogo de Bênçãos (só nomes; tier pelo número, regra de 06.7)
# ---------------------------------------------------------------------------

_CATALOGO = None


def catalogo_bencaos():
    """{nome: (caminho, número, tier, requisito)}."""
    global _CATALOGO
    if _CATALOGO is None:
        _CATALOGO = {}
        for cap, caminho in CAPITULO_CAMINHO.items():
            arq = next(LIVRO.glob(f"{cap}-*.md"))
            for m in re.finditer(r"(?m)^### (\d+)\. (.+?)\s*$", arq.read_text(encoding="utf-8")):
                n = int(m.group(1))
                tier, req = ("I", 1) if n <= 6 else ("II", 9) if n <= 10 else ("III", 17)
                _CATALOGO[m.group(2)] = (caminho, n, tier, req)
    return _CATALOGO


# ---------------------------------------------------------------------------
# Cálculo
# ---------------------------------------------------------------------------

ENTRADAS_EXEMPLO = {
    # A Nadir de 29.7, nível 1
    "nivel": 1, "jogadores": 4, "raca": "Humano", "caminho": "A Destruição",
    "metodo": "Array oficial",
    "atributos": {"Poder": 15, "Vigor": 14, "Agilidade": 13, "Discernimento": 12,
                  "Presença": 10, "Sincronia": 8},
    "bonus_racial": {"modo": "Um Atributo (+2)", "attr1": "Poder"},
    "aumentos": {},                      # {3: {"modo": "Um Atributo (+2)", "attr1": "Poder"}, ...}
    "atributo_habilidade": "Poder", "elemento": "Fogo", "sintonia": "Discernimento",
    "pericias_escolhidas": ["Intimidação", "Mecânica"],
    "eficacia_pericias": [], "eficacia_tr": [],
    "armadura": "Média",
    "arma": {"categoria": "Pesada", "atributo": None, "elemento": None, "propriedade": "Nenhuma"},
    "habilidades": [{"nome": "Rebarba", "tipo": "Dano", "nivel": 1, "area": False,
                     "resolucao": "Teste de Ataque", "ress3": False}],
    "ultimate": {"nome": "A Doca Inteira", "tipo": "Dano", "area": False},
    "bencaos": ["Pacto da Ruína"],       # slot k = nível 2k-1
    # 29.7 não declara o alvo do Bônus Maior do Cone da Nadir: sem alvo, não soma
    "cone": {"nivel": 1, "alvo": None, "escolha": "Numérico", "sobreposicoes": 0},
    "reliquias": {"Mãos": {"conjunto": "—"}, "Botas": {"conjunto": "—"}},
    "esfera_elemento": None,
    "conjuntos": {},                     # {"A": {"bonus2": "Velocidade +1"}}
    "ressonancias": {},                  # {"I": "Velocidade +1", ...}
    "inventario": [],                    # [{"espaco": 0.5, "qtd": 2}]
    "pv_atual": None, "memo_ativo": False, "forma_avatar": None,
    "acumulos": {},                      # {"Fúria": 1, "Marcas da Ruína": 2, ...}
    "memoespirito": None,
}


def calcular(e):
    av = []

    def aviso(cod):
        if cod not in av:
            av.append(cod)

    s = {}
    # --- Nível e mesa -------------------------------------------------------
    # Vazio = ficha em branco: conta como nível 1 e mesa de 4, sem aviso (decisão 8)
    nivel_in = e.get("nivel")
    L = nivel_in if isinstance(nivel_in, int) else 1
    if nivel_in is not None and (not isinstance(nivel_in, int) or not 1 <= nivel_in <= 20):
        aviso("NIVEL_FORA")
    L = max(1, min(20, L))
    jog_in = e.get("jogadores")
    jog = jog_in if isinstance(jog_in, int) else 4
    if jog_in is not None and (not isinstance(jog_in, int) or not 1 <= jog_in <= 6):
        aviso("JOGADORES_INVALIDO")
    jog = max(1, min(6, jog))
    if not 3 <= jog <= 6:
        aviso("JOGADORES_FORA_DA_TABELA")
    ef = eficiencia(L)
    fx = faixa(L)
    p_slots, tr_slots = slots_eficacia(L)
    s.update({"nivel": L, "faixa": fx, "eficiencia": ef, "eficacia": 2 * ef,
              "slots_eficacia_pericias": p_slots, "slots_eficacia_tr": tr_slots,
              "especializacao": especializacao(L), "teto_bonus": teto_bonus(L),
              "teto_penalidade": -teto_bonus(L), "teto_dados_adicionais": 3,
              "teto_rd": 2 + 2 * ef, "teto_temporarios": 3 * ef,
              "bencaos_possuidas": (L + 1) // 2, "habilidades_conhecidas": HAB_CONHECIDAS[L - 1],
              "reescreve": L >= 16, "nivel_max_habilidade": NIVEL_MAX_HAB[L - 1],
              "dados_ab": dados_ab(L), "aumento_neste_nivel": L in NIVEIS_AUMENTO,
              "tier_reliquia": tier_reliquia(L), "cone_maximo": fx,
              "ultimate_equivalente": ULTIMATE[fx][0], "pontos_memo": 12 + L // 2,
              "verba_marco": VERBA_MARCO[fx - 1], "dt_fraqueza": DT_FRAQUEZA[fx - 1],
              "dt_faixa": {k: v[fx - 1] for k, v in DT_FAIXA.items()},
              "ressonancias_liberadas": [r for r, n in (("I", 5), ("II", 10), ("III", 15),
                                                        ("IV", 20)) if L >= n]})
    s["ph_max"], s["ph_inicio"], s["ph_geracao"] = ph_grupo(L, jog)

    # --- Atributos ---------------------------------------------------------
    raca = e.get("raca")
    caminho = e.get("caminho")
    base = dict(e.get("atributos") or {})
    for a in ATRIBUTOS:
        base.setdefault(a, 8 if e.get("metodo") == "Compra de Pontos" else None)
    valores_base = [base[a] for a in ATRIBUTOS]
    if e.get("metodo") == "Array oficial" and all(isinstance(v, int) for v in valores_base):
        if sorted(valores_base, reverse=True) != list(ARRAY_OFICIAL):
            aviso("ARRAY_INVALIDO")
    if e.get("metodo") == "Compra de Pontos":
        gasto = sum(CUSTO_COMPRA.get(max(8, min(15, v)), 0) for v in valores_base if isinstance(v, int))
        s["compra_gasto"] = gasto
        if gasto > VERBA_COMPRA:
            aviso("COMPRA_ACIMA_DE_28")
    for v in valores_base:
        if isinstance(v, int) and v > TETO_CRIACAO:
            aviso("ATRIBUTO_ACIMA_15_NA_CRIACAO")
        if isinstance(v, int) and not 8 <= v <= 20:
            aviso("ATRIBUTO_FORA_8_20")
    racial = {a: 0 for a in ATRIBUTOS}
    br = e.get("bonus_racial") or {}
    if raca in RACAS:
        opcoes = RACAS[raca]
        # 05 (v1.2): o modo "+2 em um, ou +1 em cada" passou a valer para TODAS as Raças.
        # O que continua sendo só do Humano é a lista: ele escolhe entre os seis Atributos,
        # as outras escolhem dentro do par delas.
        dois = br.get("modo") == "Dois Atributos (+1 cada)"
        if opcoes is None:                                  # Humano: os seis Atributos
            if dois:
                a1, a2 = br.get("attr1"), br.get("attr2")
                if a1 in racial:
                    racial[a1] += 1
                if a2 in racial:
                    if a2 == a1:
                        aviso("BONUS_RACIAL_MESMO_ATRIBUTO")   # conta só um +1
                    else:
                        racial[a2] += 1
            elif br.get("attr1") in racial:
                racial[br["attr1"]] += 2
        elif dois:
            # "+1 em cada" é determinístico fora do Humano: os dois Atributos são o par da
            # Raça, então não há escolha a fazer e attr1/attr2 são ignorados de propósito
            for a in opcoes:
                racial[a] += 1
        else:
            escolhido = br.get("attr1") or (opcoes[0] if len(opcoes) == 1 else None)
            if escolhido in opcoes:
                racial[escolhido] += 2
            elif escolhido is not None:
                aviso("BONUS_RACIAL_INVALIDO")
    aumentos = {a: 0 for a in ATRIBUTOS}
    for nv, au in (e.get("aumentos") or {}).items():
        if nv in NIVEIS_AUMENTO and nv > L and au and (au.get("attr1") or au.get("attr2")):
            aviso("AUMENTO_ANTES_DO_NIVEL")       # 04.3: o aumento só vale a partir do nível do marco
        if nv not in NIVEIS_AUMENTO or nv > L or not au:
            continue
        if au.get("modo") == "Dois Atributos (+1 cada)":
            a1, a2 = au.get("attr1"), au.get("attr2")
            if a1 in aumentos:
                aumentos[a1] += 1
            if a2 in aumentos:
                if a2 == a1:
                    aviso("AUMENTO_MESMO_ATRIBUTO")
                else:
                    aumentos[a2] += 1
        elif au.get("attr1") in aumentos:
            aumentos[au["attr1"]] += 2
    attr, bon, criacao = {}, {}, {}
    for a in ATRIBUTOS:
        b0 = base[a] if isinstance(base[a], int) else 8
        b0 = max(8, min(20, b0))
        criacao[a] = min(TETO_ATRIBUTO, b0 + racial[a])
        bruto = b0 + racial[a] + aumentos[a]
        if bruto > TETO_ATRIBUTO and aumentos[a] > 0:
            aviso("AUMENTO_DESPERDICADO")
        attr[a] = min(TETO_ATRIBUTO, bruto)
        bon[a] = bonus(attr[a])
    s["atributos"] = attr
    s["bonus"] = bon
    s["atributos_criacao"] = criacao

    # --- Caminho -----------------------------------------------------------
    cam = CAMINHOS.get(caminho)
    attrs_hab, per_cam, N, vel_cam = cam if cam else ((), (), 0, 0)
    ah = e.get("atributo_habilidade")
    if cam and len(attrs_hab) == 1 and not ah:
        ah = attrs_hab[0]
    if cam and ah not in attrs_hab:
        aviso("ATRIBUTO_HABILIDADE_INVALIDO")
    bah = bon.get(ah, 0) if ah in attrs_hab else 0
    s.update({"N": N, "vel_caminho": vel_cam, "pericias_caminho": list(per_cam),
              "atributo_habilidade": ah})

    bencaos = list(e.get("bencaos") or [])
    tem = set(bencaos[:(L + 1) // 2])
    cat = catalogo_bencaos()
    acum = e.get("acumulos") or {}
    memo_ativo = bool(e.get("memo_ativo")) and caminho == "A Recordação"
    forma_sinc = "Avatar da Recordação" in tem and e.get("forma_avatar") == "Sincronizada"

    # --- Equipamento --------------------------------------------------------
    tier = tier_reliquia(L)
    rel = {slot: RELIQUIAS[slot][tier - 1] for slot in (e.get("reliquias") or {})}
    s["reliquias"] = rel
    conj_pecas = {}
    for slot, info in (e.get("reliquias") or {}).items():
        letra = (info or {}).get("conjunto")
        if letra in ("A", "B", "C"):
            conj_pecas[letra] = conj_pecas.get(letra, 0) + 1
    conj_bonus = {"vel": 0, "dano": 0, "rd": 0, "rolagem": 0}
    conj_rolagens = []                  # rolagens que recebem o +1 (uma por Conjunto ativo)
    conj_ativos = {}
    for letra, n_p in conj_pecas.items():
        info = (e.get("conjuntos") or {}).get(letra) or {}
        conj_ativos[letra] = 4 if n_p >= 4 else 2 if n_p >= 2 else 0
        if n_p >= 2:
            b2 = info.get("bonus2")
            if b2 == "Velocidade +1":
                conj_bonus["vel"] += 1
            elif b2 == "Dano +2":
                conj_bonus["dano"] += 2
            elif b2 == "RD +1":
                conj_bonus["rd"] += 1
            elif b2 == "Um tipo de rolagem +1":
                conj_bonus["rolagem"] += 1
                # 25.3: "Um tipo de rolagem +1" — vale na rolagem escolhida (Teste de
                # Ataque, um TR ou uma Perícia); sem escolha, não vale em nenhuma
                if info.get("rolagem"):
                    conj_rolagens.append(info["rolagem"])
    # 25.3: "Os bônus de conjunto não somam mais de +3 em uma mesma rolagem" — o dano do
    # Conjunto (+2 por Conjunto, no Ataque Básico) fica limitado a +3 (2+2+2 = 6 -> 3)
    if conj_bonus["dano"] > 3:
        aviso("CONJUNTOS_DANO_ACIMA_DE_3")
        conj_bonus["dano"] = 3
    s["conjuntos_rolagens"] = conj_rolagens
    s["conjuntos_pecas"] = conj_pecas
    s["conjuntos_ativos"] = conj_ativos
    s["conjuntos_bonus"] = conj_bonus

    cone_in = e.get("cone") or {}
    cone_b = {"alvo": None, "numerico": 0, "pv": 0}
    if cone_in.get("nivel"):
        nc = cone_in["nivel"]
        if nc > fx:
            aviso("CONE_NIVEL_ACIMA")
        nc = max(1, min(5, nc))
        num, pv, modo = CONE[nc]
        sob = cone_in.get("sobreposicoes") or 0
        if sob > fx:
            aviso("SOBREPOSICOES_A_MAIS")
            sob = fx
        # 25.2 (v1.1, D5): cada Sobreposição soma +1 no numérico e +10 no PV; o numérico para
        # em +3 e o PV para junto — 2 nos Níveis 1 e 2, 1 nos 3 e 4, nenhuma no 5
        cabem = TETO_CONE_NUM - num
        if sob > cabem:
            aviso("SOBREPOSICOES_ACIMA_DO_TETO")
            sob = cabem
        num += sob
        pv += SOBREPOSICAO_PV * sob
        alvo = cone_in.get("alvo")
        if alvo == "PV máximos":
            cone_b = {"alvo": alvo, "numerico": 0, "pv": pv}
        elif modo == "e":
            cone_b = {"alvo": alvo, "numerico": num, "pv": pv}
        elif cone_in.get("escolha") == "PV":
            cone_b = {"alvo": alvo, "numerico": 0, "pv": pv}
        else:
            cone_b = {"alvo": alvo, "numerico": num, "pv": 0}
    # 25.2: "Bônus em um tipo de Teste: Teste de Ataque, um Teste de Resistência, ou uma
    # Perícia" — nos dois últimos o jogador diz QUAL ("qual"); sem dizer, não vale em nenhum
    cone_b["qual"] = cone_in.get("qual") if cone_b["alvo"] in ("Um Teste de Resistência",
                                                               "Uma Perícia") else None
    s["cone"] = cone_b

    def cone_em(alvo, qual=None):
        if cone_b["alvo"] != alvo:
            return 0
        if alvo in ("Um Teste de Resistência", "Uma Perícia") and cone_b["qual"] != qual:
            return 0
        return cone_b["numerico"]

    ress = e.get("ressonancias") or {}
    ress_ok = {k: v for k, v in ress.items() if k in s["ressonancias_liberadas"] and v}
    if any(v and k not in s["ressonancias_liberadas"] for k, v in ress.items()):
        aviso("RESSONANCIA_ANTES_DO_NIVEL")       # 26.7: I no 5, II no 10, III no 15, IV no 20

    # --- Estatísticas ------------------------------------------------------
    V = bon["Vigor"]
    pv_max = 25 + 5 * N + 3 * V + (L - 1) * (5 + N + V)
    pv_max += rel.get("Cabeça", 0) + cone_b["pv"]
    if "Corpo Imortal" in tem:
        pv_max += 2 * L
    if forma_sinc:
        pv_max += 2 * L
    s["pv_max"] = pv_max
    s["pv_ganho_vigor"] = L + 2                                # 04.3
    s["descanso_curto"] = 2 * L + V                            # 23.6
    s["morrendo_bonus"] = bon["Presença"]                      # 23.4
    s["morrendo_vantagem"] = raca in VANTAGEM_MORRENDO         # D3
    s["morrendo_dt"] = 10
    s["pode_ser_executado"] = raca != "Xianzhouíta"
    s["esforco_max"] = 1 if raca == "Humano" else 0

    arm = ARMADURAS.get(e.get("armadura"))
    a_def, a_vel, a_rd, a_pen, a_esq, a_esp = arm if arm else (0, 0, 0, 0, True, 0)
    temp_def = 0
    if "Florescimento da Alma" in tem:
        temp_def += min(5, acum.get("Florescimento", 0))
    if "Fragmentos do Eu Perdido" in tem and memo_ativo and e.get("fragmento") == "Guarda":
        temp_def += ef
    defesa = 10 + bon["Agilidade"] + a_def + rel.get("Tronco", 0) + cone_em("Defesa") + \
        (1 if forma_sinc else 0)
    if temp_def > s["teto_bonus"]:
        aviso("BONUS_TEMPORARIO_NO_TETO")
    s["defesa"] = defesa
    s["defesa_com_temporarios"] = defesa + min(s["teto_bonus"], temp_def)
    if a_esq:
        s["esquiva"] = defesa + ef
    else:
        s["esquiva"] = None
        aviso("ESQUIVA_PROIBIDA")
    rd = a_rd + cone_em("RD") + conj_bonus["rd"]
    if "Pele de Pedra" in tem:
        rd += 2
    if "Corpo Imortal" in tem:
        rd += ef
    if rd > s["teto_rd"]:
        aviso("RD_NO_TETO")
    s["rd"] = min(rd, s["teto_rd"])
    vel = 10 + bon["Agilidade"] + vel_cam + a_vel + rel.get("Botas", 0) + cone_em("Velocidade") + \
        conj_bonus["vel"] + (1 if ress_ok.get("I") == "Velocidade +1" else 0) + \
        (2 if "Avatar da Caça" in tem else 0)
    if not 7 <= vel <= 25:
        aviso("VEL_FORA_7_25")
    s["velocidade"] = vel
    s["barreira_max"] = 3 * ef if caminho == "A Preservação" else None

    # --- Perícias -----------------------------------------------------------
    sinc_criacao = bonus(criacao["Sincronia"])
    permitidas = max(2, 2 + sinc_criacao)                     # 04.5 (v1.1): fixada na criação
    # 05 (v1.2): traço passivo Vocação Livre — o Humano escolhe 1 Perícia a mais. Entra depois
    # do piso de 2, e é fixada na criação como todas as outras (04.5)
    if raca == "Humano":
        permitidas += 1
    escolhidas = list(e.get("pericias_escolhidas") or [])
    s["pericias_permitidas"] = permitidas
    if len(escolhidas) > permitidas:
        aviso("PERICIAS_A_MAIS")
    if any(p in per_cam for p in escolhidas):
        aviso("PERICIA_DO_CAMINHO_ESCOLHIDA")
    efic_p = list(e.get("eficacia_pericias") or [])
    if len(efic_p) > p_slots:
        aviso("EFICACIA_PERICIAS_A_MAIS")
    pericias = {}
    com_ef = set(per_cam) | set(escolhidas[:permitidas])
    for nome, at in PERICIAS:
        at = at or e.get("sintonia") or "Discernimento"
        b = bon[at]
        tem_ef = nome in com_ef
        usa_efc = nome in efic_p[:p_slots] and tem_ef
        if nome in efic_p and not tem_ef:
            aviso("EFICACIA_SEM_EFICIENCIA")
        prof = 2 * ef if usa_efc else ef if tem_ef else 0
        pen = a_pen if nome in PERICIAS_PENALIZADAS_PESADA else 0
        # Cone "Uma Perícia" fora do teto (25.2); Conjunto "Um tipo de rolagem +1" dentro
        # do teto de bônus somado (25.3 / 26.6)
        extra = cone_em("Uma Perícia", nome) + min(s["teto_bonus"], conj_rolagens.count(nome))
        total = b + prof + pen + extra
        pericias[nome] = {"atributo": at, "bonus_atributo": b, "eficiencia": tem_ef,
                          "eficacia": usa_efc, "penalidade": pen, "total": total,
                          "rolagem": rolagem(total),
                          "vantagem": nome in VANTAGEM_PERICIA.get(raca, ())}
    s["pericias"] = pericias
    s["pericias_com_eficiencia"] = len([p for p in pericias.values() if p["eficiencia"]])

    # --- Testes de Resistência ------------------------------------------------
    efic_tr = list(e.get("eficacia_tr") or [])
    if len(efic_tr) > tr_slots:
        aviso("EFICACIA_TR_A_MAIS")
    trs = {}
    for nome, at in TESTES_RESISTENCIA:
        prof = 2 * ef if nome in efic_tr[:tr_slots] else ef
        pen = a_pen if nome == "Reflexos" else 0
        temp = 0
        if "Cicatriz da Destruição" in tem and nome in ("Força de Vontade", "Resistência Mental"):
            temp += min(5, acum.get("Marcas da Ruína", 0))
        if "Florescimento da Alma" in tem:
            temp += min(5, acum.get("Florescimento", 0))
        temp += conj_rolagens.count(nome)                   # Conjunto: dentro do teto (25.3)
        if temp > s["teto_bonus"]:
            aviso("BONUS_TEMPORARIO_NO_TETO")
        # Cone "Um Teste de Resistência" fica FORA do teto (25.2)
        total = bon[at] + prof + pen + min(s["teto_bonus"], temp) + cone_em("Um Teste de Resistência", nome)
        trs[nome] = {"atributo": at, "total": total, "rolagem": rolagem(total),
                     "vantagem": nome in VANTAGEM_TR.get(raca, ()),
                     "vantagem_condicional": nome in VANTAGEM_TR_CONDICIONAL.get(raca, ())}
    s["testes_resistencia"] = trs

    # --- DT, ataques ----------------------------------------------------------
    s["dt"] = 8 + bah + ef                                       # 02.2 / 22.3
    pv_atual = e.get("pv_atual")
    temp_atk = 0
    if "Instinto de Sobrevivência" in tem and isinstance(pv_atual, int) and pv_atual * 3 <= pv_max:
        temp_atk += 2
    if memo_ativo:
        memo = e.get("memoespirito") or {}
        if memo.get("funcao") == "Catalisador":
            temp_atk += 1
        if "Fusão de Memórias" in (memo.get("evolucoes") or []):
            temp_atk += 1
        if "Memória Compartilhada" in tem:
            temp_atk += 1
    temp_atk += conj_rolagens.count("Teste de Ataque")     # Conjunto: dentro do teto (25.3)
    if temp_atk > s["teto_bonus"]:
        aviso("BONUS_TEMPORARIO_NO_TETO")
    temp_atk = min(s["teto_bonus"], temp_atk)
    s["ataque_habilidade"] = bah + ef + especializacao(L) + cone_em("Teste de Ataque") + temp_atk
    arma = e.get("arma") or {}
    cat_arma = ARMAS.get(arma.get("categoria"))
    ab = None
    if cat_arma:
        face, extra, alcance, at_ab, esp_arma = cat_arma
        at_ab = at_ab or (arma.get("atributo") if arma.get("atributo") in ("Poder", "Agilidade")
                          else "Poder")
        n = dados_ab(L) + extra + (1 if forma_sinc else 0)
        if arma.get("propriedade") == "Alcance estendido":
            alcance = ESCALA_DISTANCIA[min(4, ESCALA_DISTANCIA.index(alcance) + 1)]
        fixo = bon[at_ab]
        equip = rel.get("Mãos", 0) + cone_em("Dano de Ataque Básico") + conj_bonus["dano"]
        ab = {"atributo": at_ab, "ataque": bon[at_ab] + ef + especializacao(L) +
              cone_em("Teste de Ataque") + temp_atk,
              "n": n, "face": face, "dados": f"{n}d{face}", "fixo": fixo,
              # 18.2 + 25.3: dano = dados + atributo + equipamento (Mãos, Cone, Conjuntos).
              # v1.1 (D1): 29.7 soma Mãos I (1d12 + 4 + 2 = 1d12 + 6); regra única
              "equip": equip, "fixo_total": fixo + equip,
              "texto": texto_dano(n, face, fixo + equip), "media": media(n, face) + fixo + equip,
              "fraqueza": f"{n + 2}d{face}", "texto_fraqueza": texto_dano(n + 2, face, fixo + equip),
              "resistencia": f"{max(1, n - 2)}d{face}",
              "rt": 1 + (1 if arma.get("propriedade") == "Peso de impacto" else 0),
              "alcance": alcance, "elemento": arma.get("elemento") or "Físico",
              "critico": "19-20" if "Olho de Lan" in tem else "20", "espaco": esp_arma}
        if arma.get("propriedade") == "Dissimulada":
            ab["espaco"] = 0.5
    s["ataque_basico"] = ab

    # --- Habilidades -------------------------------------------------------------
    elem = e.get("elemento")
    esfera = rel.get("Esfera Planar", 0) if e.get("esfera_elemento") and \
        e.get("esfera_elemento") == elem else 0
    habs = []
    lista_h = list(e.get("habilidades") or [])
    if len(lista_h) > HAB_CONHECIDAS[L - 1]:
        aviso("HABILIDADES_A_MAIS")
    nmax = NIVEL_MAX_HAB[L - 1]
    # 26.7: a Ressonância III escolhe "uma Habilidade" — só a PRIMEIRA marcada recebe o Nível
    ress3_usada = False
    for h in lista_h:
        nv = h.get("nivel") or 1
        if nv > nmax:
            aviso("HABILIDADE_NIVEL_ACIMA")
        nv = max(1, min(7, nv))
        if h.get("ress3") and ress_ok.get("III"):
            if ress3_usada:
                aviso("RESSONANCIA_III_REPETIDA")
            else:
                ress3_usada = True
                nv = min(nmax, nv + 1) if nv < nmax else nv
        dn, df, cn, cf, ph, rt = NIVEIS_HAB[nv]
        tipo = h.get("tipo")
        out = {"nivel_efetivo": nv, "ph": 0 if tipo == "Passiva" else ph,
               "rt": rt if tipo == "Dano" else 0,
               "alcance_max": ALCANCE_MAX_HAB.get(nv, "Extrema")}
        area = bool(h.get("area"))
        if tipo in ("Dano", "Cura"):
            n_, f_ = (dn, df) if tipo == "Dano" else (cn, cf)
            if area:
                n_ = max(1, n_ // 2)
            fixo = bah + ((esfera + cone_em("Dano de Habilidade")) if tipo == "Dano" else 0)
            out.update({"n": n_, "face": f_, "fixo": fixo, "texto": texto_dano(n_, f_, fixo),
                        "media": media(n_, f_) + fixo})
        out["alvos"] = (4 if nv >= 6 else 3) if area else 1
        out["rolagem"] = (rolagem(s["ataque_habilidade"]) if h.get("resolucao") == "Teste de Ataque"
                          else f"DT {s['dt']}" if h.get("resolucao") == "Teste de Resistência" else "")
        habs.append(out)
    s["habilidades"] = habs

    ult_in = e.get("ultimate") or {}
    eq, udn, udf, ucn, ucf = ULTIMATE[fx]
    ult = {"equivalente": eq, "rt": 5,
           "custo": 80 if ress_ok.get("IV") == "Ultimate com 80 de Energia" else 100}
    if ult_in.get("tipo") in ("Dano", "Cura"):
        n_, f_ = (udn, udf) if ult_in["tipo"] == "Dano" else (ucn, ucf)
        area = bool(ult_in.get("area"))
        if area:
            n_ = max(1, n_ // 2)
        fixo = bah + ((esfera + cone_em("Dano de Ultimate")) if ult_in["tipo"] == "Dano" else 0)
        ult.update({"n": n_, "face": f_, "dados": f"{n_}d{f_}", "fixo": fixo,
                    "texto": texto_dano(n_, f_, fixo), "media": media(n_, f_) + fixo,
                    "alvos": (4 if eq >= 6 else 3) if area else 1})
    s["ultimate"] = ult

    # --- Quebra ------------------------------------------------------------------
    if elem in QUEBRA:
        qn, qf, qm = QUEBRA[elem]
        s["quebra"] = {"texto": texto_dano(qn, qf, qm * ef), "media": media(qn, qf) + qm * ef}
    else:
        s["quebra"] = None

    # --- Bênçãos -------------------------------------------------------------------
    slots = []
    vistos = set()
    for k, nome in enumerate(bencaos[:10]):
        nivel_slot = 2 * k + 1
        info = {"nivel_slot": nivel_slot, "bencao": nome, "liberado": L >= nivel_slot}
        if nome:
            c = cat.get(nome)
            if L < nivel_slot:
                aviso("BENCAO_EM_SLOT_FUTURO")
            if c is None or c[0] != caminho:
                aviso("BENCAO_DE_OUTRO_CAMINHO")
            else:
                info.update({"tier": c[2], "requisito": c[3]})
                if c[3] > nivel_slot:
                    aviso("BENCAO_TIER_ACIMA_DO_SLOT")
            if nome in vistos:
                aviso("BENCAO_REPETIDA")
            vistos.add(nome)
        slots.append(info)
    s["bencoes_slots"] = slots
    if "Pacto da Ruína" in tem:
        s["pacto_da_ruina"] = {"custo_pv": 2 * L, "bonus": ef, "bonus_ferido": 2 * ef,
                               "limiar_pv": pv_max // 2}

    # --- Inventário ---------------------------------------------------------------------
    cap_inv = 10 + 2 * bon["Poder"] + (2 if "Peso do Juramento" in tem else 0)
    ocupado = (ab["espaco"] if ab else 0) + a_esp + \
        sum((i.get("espaco") or 0) * (1 if i.get("qtd") is None else i["qtd"])   # qtd vazia = 1
            for i in (e.get("inventario") or []))
    # 24.4: o Espaço conta o que você carrega, veste e empunha; 0 unidades = nada carregado,
    # então quantidade 0 ocupa 0 (antes o oráculo tratava 0 como 1 — corrigido na FEAT-004)
    s["capacidade"] = cap_inv
    s["ocupado"] = ocupado
    if ocupado > 2 * cap_inv:
        aviso("IMOVEL")
    elif ocupado > cap_inv:
        aviso("SOBRECARGA")

    # --- Memoespírito ----------------------------------------------------------------------
    memo = e.get("memoespirito")
    if memo:
        if caminho != "A Recordação":
            aviso("MEMO_FORA_DA_RECORDACAO")
        pts = {a: (memo.get("pontos") or {}).get(a, 0) or 0 for a in ATRIBUTOS}
        if any(v > 5 for v in pts.values()):
            aviso("MEMO_ATRIBUTO_ACIMA_5")
        total_pts = 12 + L // 2
        if sum(pts.values()) > total_pts:
            aviso("MEMO_PONTOS_A_MAIS")
        menores = list(memo.get("bonus_menores") or [])
        if len(menores) > 3 or len(set(menores)) != len(menores):
            aviso("MEMO_BONUS_MENORES")
        evol = list(memo.get("evolucoes") or [])
        if len(evol) > sum(1 for n in (8, 14, 20) if L >= n):
            aviso("MEMO_EVOLUCAO_ANTES_DO_NIVEL")
        if len(set(evol)) != len(evol):
            aviso("MEMO_EVOLUCAO_REPETIDA")
        p = {a: min(5, v) for a, v in pts.items()}
        atk = memo.get("atributo_ataque") or "Poder"
        pv_m = 8 * L + 3 * p["Vigor"]
        if memo.get("funcao") == "Guardião":
            pv_m += 3 * L
        if "Resistência Espiritual" in menores:
            pv_m += 2 * L
        if "Ecos do Passado" in tem:
            pv_m += 4 * L
        def_m = 10 + p["Agilidade"] + ef
        vel_m = 10 + p["Agilidade"] + vel_cam + (2 if "Velocidade Espiritual" in menores else 0)
        desperta = memo.get("memoria_desperta")
        if "Memória Desperta" in evol:
            if desperta == "Velocidade":
                vel_m += 2
            else:
                def_m += 2
        # 11.4 (v1.2, E17): a contagem de dados vem da arma do DONO, com a exceção da Energia
        # (18.5/24.2/26.2: começa em 2 e chega a 6). Só a quantidade vem do dono; a face é
        # sempre d6, do Memoespírito.
        n_m = dados_ab(L) + (cat_arma[1] if cat_arma else 0) + (1 if "Forma Completa" in evol else 0)
        fixo_m = p[atk] + (2 if "Força Espiritual" in menores else 0) + \
            (bah if "Ecos do Passado" in tem else 0)
        rt_m = (2 if L >= 11 else 1) + (1 if "Eternidade Recordada" in tem else 0)
        s["memo"] = {"pontos_total": total_pts, "pontos_gastos": sum(pts.values()),
                     "pv": pv_m, "defesa": def_m, "velocidade": vel_m,
                     "ataque": bah + p[atk] + ef, "n": n_m, "fixo": fixo_m,
                     "texto": texto_dano(n_m, 6, fixo_m), "media": media(n_m, 6) + fixo_m,
                     "media_fraqueza": media(n_m + 2, 6) + fixo_m,
                     "rt": rt_m, "rd": 1 if "Resistência Espiritual" in menores else 0,
                     "tr": {a: p[a] + ef for a in ATRIBUTOS},
                     "predador_d8": memo.get("funcao") == "Predador"}
    else:
        s["memo"] = None

    s["avisos"] = av
    return s


if __name__ == "__main__":
    r = calcular(ENTRADAS_EXEMPLO)
    print("Nadir nível 1 (29.7):")
    for k in ("atributos", "bonus", "pv_max", "defesa", "esquiva", "rd", "teto_rd", "velocidade",
              "dt", "ataque_basico", "habilidades", "ultimate", "ph_inicio", "ph_max",
              "capacidade", "pericias_com_eficiencia", "pacto_da_ruina", "avisos"):
        print(f"  {k}: {r[k]}")
