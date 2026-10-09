# -*- coding: utf-8 -*-
"""Constantes de leiaute e utilitários da aba Combate (compartilhados por aba_combate*.py).

Combatentes (tabela de estado oculta, uma linha cada): 1–6 os PJs, 7–16 os inimigos e 17–22 os Memoespíritos
dos PJs 1–6 (Fase 4, pedido do usuário: casa própria na Fila pela VEL dele, 11.5 e 19.7).
"""

from openpyxl.utils import get_column_letter as L, column_index_from_string as CI

from mestre.nucleo import T

NPJ, NIN, NMEMO = 6, 10, 6
NC = NPJ + NIN + NMEMO            # 22
MI0 = NPJ + NIN                   # o Memoespírito do PJ m é o combatente MI0 + m
NSLOT = 4                         # condições por combatente (C7: o pedido pede de 4 a 6)
NPAINEL = 30                      # linhas do painel de consulta rápida (C9b)

R_C1, R_C2 = 15, 24
R_C2B = 33                        # C2b · Memoespíritos (6 linhas) + 3 linhas de regra
R_C3, R_C4, R_C5, R_C5B, R_C6 = 45, 58, 74, 87, 101
R_C8 = (114, 125, 136)            # 22 linhas em blocos de 10 (D11)
R_C9 = (141, 152, 163)
R_PEND = 166                      # PENDENTES, CONDIÇÕES, nota H13
R_C9B_TIT = 170
R_C9B = (173, 184, 195)           # painel: 30 linhas em blocos de 10
R_C7_TIT = 207
R_C7 = tuple(209 + 13 * b for b in range(8))     # 88 linhas (22 × 4) em blocos de 12
R_C10 = 308
ST0 = 11

STC = ["lab", "tipo", "ex", "vivo", "ativo", "ativon", "velb", "vel", "tag", "tdisc", "ttipo", "tlin", "chave", "cong",
       "surp", "bruto", "firm", "pendp", "ja", "avc", "man", "base", "posr", "posc", "exc", "ch2", "pendn", "basen",
       "chn", "pvmax", "pvat", "ef", "flag", "avt", "ncond"]
SC = {c: L(CI("N") + k) for k, c in enumerate(STC)}
ENC_ = ["dj", "dnome", "nome", "idx", "w1", "w2", "w3", "w4", "fb", "fv", "v1", "v2", "v3", "v4", "res", "tenmax",
        "tenat", "quebr", "defat", "rd", "ef", "exec", "pode", "tipo", "fases", "rot"]
EC = {c: L(CI("AZ") + k) for k, c in enumerate(ENC_)}
CC = {c: L(CI("N") + k) for k, c in enumerate(["ia", "it", "ef", "pvm", "cnd", "nd", "fc", "pa", "se", "pct", "tef",
                                                "atr", "tac", "dc", "acu", "efe", "ativa", "ord", "dur", "txt",
                                                "expi"])}
TEXTO_CAT = {"f1", "f2", "f3", "f4", "res", "nome", "execucao", "tipo", "faixa", "p2f1", "p2f2", "p2f3", "p2f4",
             "p3f1", "p3f2", "p3f3", "p3f4", "esp1", "esp2", "esp3", "dano_e", "firmeza"}


def linha_bloco(inicios, k, n=10):
    """Linha do k-ésimo item (1-based) numa tabela em blocos de n linhas que começam em `inicios`."""
    return inicios[(k - 1) // n] + (k - 1) % n


def slot(i, k):
    """Número da condição k (1…NSLOT) do combatente i (1…NC) na C7."""
    return (i - 1) * NSLOT + k


def linha_slot(n):
    return linha_bloco(R_C7, n, 12)


def s(c, i):
    return f"${SC[c]}${ST0 + i - 1}"


def srng(c):
    return f"${SC[c]}${ST0}:${SC[c]}${ST0 + NC - 1}"


def e_(c, e):
    return f"${EC[c]}${R_C3 + e - 1}"


def erng(c):
    return f"${EC[c]}${R_C3}:${EC[c]}${R_C3 + NIN - 1}"


def cat(c, idx):
    t = '&""' if c in TEXTO_CAT else ""
    return f'INDEX({T("inimigos.cat." + c)},{idx}){t}'
