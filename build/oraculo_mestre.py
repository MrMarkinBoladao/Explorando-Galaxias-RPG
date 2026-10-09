# -*- coding: utf-8 -*-
"""
oraculo_mestre.py — Oráculo INDEPENDENTE da Planilha do Mestre (design §12.2).

Não importa build\\mestre_dados.py nem build\\mestre\\*, e não lê fórmula nenhuma: as tabelas do
livro que ele usa estão TRANSCRITAS aqui, com a seção ao lado, e as regras estão reimplementadas
em Python puro. A bateria (build\\testar_mestre.py) compara cada número de regra da planilha
calculada (biblioteca formulas 1.3.4) com o que este módulo devolve: 0 divergência é a meta.

Partes da Fase 1: sorteio (§5), âncoras e Criador de Inimigos (28.3, 28.4, H1, H12), orçamento
e encontros (27.4, 27.5, H5–H7, H19), Fila de Ação (19.3–19.6, H13), Quebra e Dano de Quebra
(20.3–20.5), condições (21.2, 21.5), Morrendo (23.4) e PH (16.2).
Fase 2 (oraculo_mestre_hist.py): NPCs (G = 200), Aventuras (G = 300; H14, H20, H22, H26), Recompensas (24.5, 25.1–25.3,
26.7; G = 400/410/420, H9, H18).
Fase 3 (oraculo_mestre_camp.py, oraculo_mestre_ger.py): Campanha (26.1, 26.7, H16, H17), Grupo (25.3, 19.3, 20.2),
Sessões (27.2, 27.7), Missões (H23), Início; Mundos (G = 510…560), Improviso (G = 600…650: 24.1–24.3 e H15 na loja,
H10 no oráculo, 02 no rolador, 27.2 na DT rápida), Minhas Tabelas (G = 701…710) e o Escudo (27.9, 23.6, 23.3).
"""

M = 2147483647
LIMITE_EXATO = 2 ** 53

# ---------------------------------------------------------------------------
# Sorteio (design §5) — com assert de limites < 2^53 em todo intermediário
# ---------------------------------------------------------------------------

_maior = [0]


def _chk(v):
    if v > _maior[0]:
        _maior[0] = v
    assert 0 <= v < LIMITE_EXATO, f"intermediário fora de 2^53: {v}"
    return v


def maior_intermediario():
    return _maior[0]


def l3(z):
    for _ in range(3):
        z = _chk(z * 16807) % M
    return z


def q(z):
    a = _chk((z // 65536) * z) % M
    return _chk(_chk(a * 65536) + _chk((z % 65536) * z)) % M


def x_mix(z):
    return _chk(z + _chk((z // 65536) * (z % 65536))) % 2147483646 + 1


def h(s, g, r, c):
    return _chk(s + 7919 * g + 104729 * r + 1299709 * c) % 2147483646 + 1


def uyx(s, g, r, c):
    """As três auxiliares (u, y, x) do campo C do gerador G, semente S e Rolagem nº R."""
    u = l3(h(s, g, r, c))
    y = l3(q(u))
    x = l3(x_mix(y))
    return u, y, x


def valor(s, g, r, c):
    return uyx(s, g, r, c)[2]


def semente_efetiva(s):
    if isinstance(s, (int, float)) and not isinstance(s, bool) and 1 <= s <= 2147483646 and int(s) == s:
        return int(s)
    return 12345


def rolagem_efetiva(r):
    if isinstance(r, (int, float)) and not isinstance(r, bool) and 1 <= r <= 1000000 and int(r) == r:
        return int(r)
    return 1


def escolha(x, n):
    return 0 if n <= 0 else (x * n) // M + 1


def inteiro(x, a, b):
    return a + (x * (b - a + 1)) // M


def dado(x, faces):
    return (x * faces) // M + 1


# ---------------------------------------------------------------------------
# A planilha inteira (números de regra): {nome lógico da entrada: valor} -> {nome lógico: esperado}
# ---------------------------------------------------------------------------

def calcular(E):
    """Reimplementa as regras das abas da Fase 1 (Início, Campanha, Grupo, Inimigos, Bestiário, Encontros,
    Combate). Não lê a planilha nem importa o gerador: as tabelas estão em oraculo_mestre_livro.py."""
    import oraculo_mestre_abas as AB
    import oraculo_mestre_cmb as CB
    out = {}
    elems = AB.campanha(E, out)
    linhas = AB.inimigos(E, out, elems)
    AB.bestiario(E, out)
    cat = AB.catalogo(linhas)
    racas = [AB.tx(E.get(f"grupo.pj{i}.raca")) for i in range(1, 7)]
    salvos = CB.encontros(E, out, cat, elems, racas)
    grupo = [{k: E.get(f"grupo.pj{i}.{k}") for k in ("nome", "pv", "vel", "ag", "disc", "pres")} for i in range(1, 7)]
    CB.combate(E, out, cat, salvos, grupo)
    import oraculo_mestre_hist as HI           # Fase 2: NPCs, Aventuras, Recompensas
    HI.calcular(E, out)
    import oraculo_mestre_camp as CP           # Fase 3: Campanha, Grupo, Sessões, Missões, Início
    CP.calcular(E, out)
    import oraculo_mestre_ger as GR            # Fase 3: Mundos, Improviso, Minhas Tabelas, Escudo
    GR.calcular(E, out)
    return out
