# -*- coding: utf-8 -*-
"""Confere, lendo o .xlsx publicado, se as mudanças da v1.2 chegaram à ficha do jogador.

Lê o arquivo gerado (não o código que o gera), pelo mapa de nomes lógicos, e checa:
  - E35: a linha nova do alcance resolvido na aba Criação, que olha a propriedade;
  - E30: o rótulo do modo de bônus, que deixou de ser "do Humano";
  - E20: os pares de Atributo das 7 Raças na aba Dados;
  - E34: o resumo dos traços, com um ativável e um passivo em cada Raça;
  - E31: a contagem de Perícias permitidas, com o +1 do Humano.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
XLSX = RAIZ / "ficha-automatizada" / "Ficha Automatizada - Explorando Galáxias V1.2.xlsx"
MAPA = RAIZ / "build" / "ficha_mapa.json"

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl não está instalado")

mapa = json.loads(MAPA.read_text(encoding="utf-8"))
celulas = mapa["celulas"]
wb = openpyxl.load_workbook(XLSX)

falhas, ok = [], []


def checa(desc, cond, detalhe=""):
    """O detalhe só entra quando a checagem FALHA: anexá-lo também no sucesso fazia o
    registro ler como falha ('[ok] ... — não achei o rótulo'), o que é pior que não ter
    detalhe nenhum."""
    if cond:
        ok.append(desc)
    else:
        falhas.append(f"{desc}{(' — ' + detalhe) if detalhe else ''}")


def partir(ref):
    aba, cel = ref.split("!")
    return aba.strip("'").replace("''", "'"), cel.replace("$", "")


def valor(nome):
    aba, cel = partir(celulas[nome])
    return aba, str(wb[aba][cel].value or "")


# --- E35: alcance resolvido na aba Criação -------------------------------------------------
if "criacao.arma.alcance" not in celulas:
    checa("E35 alcance resolvido", False, "nome lógico 'criacao.arma.alcance' não está no mapa")
else:
    aba, f = valor("criacao.arma.alcance")
    checa("E35 a célula está na aba Criação", aba == "Criação", f"está em {aba!r}")
    checa("E35 a fórmula olha a propriedade especial", "Alcance estendido" in f, f[:110])
    checa("E35 a fórmula tem teto na escala de Distâncias", "MIN(5" in f.replace(" ", ""),
          "sem MIN(5,...) o alcance passaria de Extrema")

# --- E30: o rótulo do modo não é mais exclusivo do Humano ----------------------------------
ws_c = wb["Criação"]
textos_criacao = [str(c.value) for row in ws_c.iter_rows() for c in row if isinstance(c.value, str)]
checa("E30 rótulo novo do modo de bônus",
      any("Bônus racial: +2 em um, ou +1 em cada" in t for t in textos_criacao),
      "não achei o rótulo 'Bônus racial: +2 em um, ou +1 em cada' na aba Criação")
checa("E30 rótulo antigo removido",
      not any(t.startswith("Bônus do Humano:") for t in textos_criacao),
      "ainda existe um rótulo 'Bônus do Humano:'")

# --- E20 e E34: pares de Atributo e traços das 7 Raças, na aba Dados -----------------------
b = mapa["blocos"]["dados.racas"]
aba_d, intervalo = partir(b["intervalo"])
col = b["colunas"]
ws_d = wb[aba_d]
primeira, ultima = b["primeira_linha"], b["ultima_linha"]

ESPERADO = {
    "Humano": (("", ""), ("Força de Vontade", "Vocação Livre")),
    "Xianzhouíta": (("Vigor", "Sincronia"), ("Séculos de Memória", "Ad Vitam Aeternam")),
    "Vidyadhara": (("Vigor", "Poder"), ("Maré que Volta", "Corpo das Marés")),
    "Vulpes": (("Agilidade", "Discernimento"), ("Favor Antigo", "Língua de Prata")),
    "Haloviano": (("Discernimento", "Presença"), ("To na sua mente", "Asas de Halo")),
    "Avginiano": (("Agilidade", "Presença"), ("Não Foi a Primeira Vez", "Mente de Ferro")),
    "Intellitron": (("Sincronia", "Poder"), ("Sabedoria de Intellitron", "Chassi")),
}

vistas = []
for r in range(primeira, ultima + 1):
    raca = str(ws_d[f"{col['Raça']}{r}"].value or "")
    if not raca:
        continue
    vistas.append(raca)
    if raca not in ESPERADO:
        checa(f"Raça {raca} conhecida", False, "nome fora do esperado")
        continue
    (op1_e, op2_e), (ativ, pas) = ESPERADO[raca]
    op1 = str(ws_d[f"{col['Opção 1 do +2']}{r}"].value or "")
    op2 = str(ws_d[f"{col['Opção 2 do +2']}{r}"].value or "")
    bonus = str(ws_d[f"{col['Bônus de atributo']}{r}"].value or "")
    resumo = str(ws_d[f"{col['Traços (resumo)']}{r}"].value or "")
    if op1_e:
        checa(f"{raca}: par de Atributos", (op1, op2) == (op1_e, op2_e),
              f"ficha: {op1!r}/{op2!r}, esperado {op1_e!r}/{op2_e!r}")
    else:
        checa(f"{raca}: bônus livre, sem par fixo", not op1 and not op2,
              f"ficha: {op1!r}/{op2!r}")
    checa(f"{raca}: bônus diz '+1 em cada' ou '+1 em dois'",
          re.search(r"\+1 em (cada|dois)", bonus) is not None, f"bônus: {bonus!r}")
    checa(f"{raca}: ativável '{ativ}' no resumo", ativ in resumo, f"resumo: {resumo[:80]!r}")
    checa(f"{raca}: passivo '{pas}' no resumo", pas in resumo, f"resumo: {resumo[:80]!r}")
    checa(f"{raca}: resumo marca os dois tipos",
          "ativável" in resumo and "passivo" in resumo, f"resumo: {resumo[:80]!r}")

checa("as 7 Raças estão na aba Dados", len(vistas) == 7, f"achei {len(vistas)}: {vistas}")

# --- E31: Perícias permitidas somam o +1 do Humano -----------------------------------------
_, fp = valor("criacao.pericias.permitidas")
checa("E31 Perícias permitidas somam o +1 do Humano",
      '"Humano",1,0' in fp.replace(" ", ""), f"fórmula: {fp[:120]}")

print(f"OK: {len(ok)}")
for x in ok:
    print(f"  [ok] {x}")
if falhas:
    print(f"\nFALHAS: {len(falhas)}")
    for x in falhas:
        print(f"  [X] {x}")
    sys.exit(1)
print("\nTodas as checagens passaram.")
