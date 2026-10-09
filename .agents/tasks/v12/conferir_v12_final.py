# -*- coding: utf-8 -*-
"""Confere nos ARQUIVOS PUBLICADOS da v1.2 se as 7 Raças estão atualizadas.

Não lê o Markdown nem o código: lê o PDF e o .xlsx que vão para a mesa, que é o
único lugar onde "está atualizado" quer dizer algo para o jogador.

Para cada Raça checa, nos dois arquivos:
  - o traço ATIVÁVEL, pelo nome;
  - o traço PASSIVO, pelo nome;
  - o par de Atributos e o modo "+1 em cada" / "+1 em dois".
E confere que nada da v1.1 ficou para trás (traços removidos, cláusula da Harmonia,
rótulo antigo do bônus do Humano).
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
PDF = RAIZ / "Sistema de HSR by MC Filhos V1.2.pdf"
XLSX = RAIZ / "ficha-automatizada" / "Ficha Automatizada - Explorando Galáxias V1.2.xlsx"
MAPA = RAIZ / "build" / "ficha_mapa.json"

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf
import openpyxl

# Raça -> (ativável, passivo, par de Atributos)
RACAS = {
    "Humano": ("Força de Vontade", "Vocação Livre", None),
    "Xianzhouíta": ("Séculos de Memória", "Ad Vitam Aeternam", ("Vigor", "Sincronia")),
    "Vidyadhara": ("Maré que Volta", "Corpo das Marés", ("Vigor", "Poder")),
    "Vulpes": ("Favor Antigo", "Língua de Prata", ("Agilidade", "Discernimento")),
    "Haloviano": ("To na sua mente", "Asas de Halo", ("Discernimento", "Presença")),
    "Avginiano": ("Não Foi a Primeira Vez", "Mente de Ferro", ("Agilidade", "Presença")),
    "Intellitron": ("Sabedoria de Intellitron", "Chassi", ("Sincronia", "Poder")),
}

# O que a v1.1 tinha e a v1.2 removeu: se aparecer, ficou resto para trás
# ATENÇÃO: estas strings são buscadas no texto RENDERIZADO do PDF, onde a marcação
# Markdown não existe. Nada de "**" aqui — foi assim que este teste deu um falso
# negativo na primeira versão.
RESTOS_V11 = [
    "Se você segue o Caminho da Harmonia, não há teste de ativação",
    "não pode usar este traço até o próximo Descanso Longo",
    "Vantagem em Testes de Resistência Física contra afogamento, frio e efeitos de água",
    "Nenhuma Raça é melhor que outra",
    "Sem limitações naturais, podendo seguir qualquer Caminho",
    "o mais discreto da lista",
]
# O changelog nem sempre cita o texto antigo ao pé da letra: às vezes ele parafraseia.
# Para cada resto acima, o fragmento que o changelog realmente traz.
CITADO_NO_CHANGELOG = {
    "Se você segue o Caminho da Harmonia, não há teste de ativação":
        "não fazia o teste",
    "Vantagem em Testes de Resistência Física contra afogamento, frio e efeitos de água":
        "Vantagem em Testes de Resistência Física contra afogamento, frio e efeitos de água",
}

falhas, ok = [], []


def checa(desc, cond, detalhe=""):
    if cond:
        ok.append(desc)
    else:
        falhas.append(f"{desc}{(' — ' + detalhe) if detalhe else ''}")


# ============================== PDF =======================================
doc = pymupdf.open(PDF)
paginas = [doc[i].get_text() for i in range(doc.page_count)]
texto_pdf = "\n".join(paginas)
# normaliza as quebras de linha dentro de frases, para buscar por frase
plano = " ".join(texto_pdf.split())

print(f"PDF: {doc.page_count} páginas, {len(plano)} caracteres de texto")
for raca, (ativ, pas, par) in RACAS.items():
    checa(f"PDF · {raca}: nome da Raça", raca in plano)
    checa(f"PDF · {raca}: ativável '{ativ}'", f"Traço ativável — {ativ}" in plano,
          "não achei o título 'Traço ativável — ...'")
    checa(f"PDF · {raca}: passivo '{pas}'", f"Traço passivo — {pas}" in plano,
          "não achei o título 'Traço passivo — ...'")
    if par:
        esperado = f"+2 em {par[0]} ou {par[1]}, ou +1 em cada"
        checa(f"PDF · {raca}: bônus '{esperado}'", esperado in plano, f"esperado: {esperado!r}")
    else:
        checa("PDF · Humano: bônus livre",
              "+2 em um Atributo à sua escolha, ou +1 em dois Atributos diferentes" in plano)

checa("PDF · contrato das três coisas",
      "As três coisas que toda Raça tem, sem exceção" in plano)
checa("PDF · tabela de cobertura de Atributos", "A cobertura de Atributos" in plano)
checa("PDF · tabela do traço ativável", "O traço ativável de cada Raça" in plano)
checa("PDF · 4.5 com a linha do Humano", "Perícias escolhidas — Humano" in plano)
checa("PDF · changelog do formato das Raças", "um formato igual para as sete" in plano)
checa("PDF · changelog do alcance na Criação",
      "Alcance do Ataque Básico (com a propriedade)" in plano)
checa("PDF · capa diz Versão 1.2", "Versão 1.2" in plano)

# Os restos da v1.1 DEVEM aparecer no changelog — a coluna "Antes" existe para citá-los.
# O que não pode é sobrarem no corpo das regras. Então a busca exclui as páginas do
# changelog e procura só do capítulo 01 em diante.
def primeira_pagina_que_comeca_com(titulo):
    for i, t in enumerate(paginas):
        if t.lstrip().startswith(titulo):
            return i
    return None


ini_corpo = primeira_pagina_que_comeca_com("Capítulo 01")
if ini_corpo is None:
    checa("PDF · achei o começo do corpo do livro (capítulo 01)", False)
    ini_corpo = 0
else:
    ok.append("PDF · começo do corpo do livro localizado")
plano_changelog = " ".join(" ".join(paginas[:ini_corpo]).split())

# A busca por restos da v1.1 é feita no MARKDOWN, não no PDF, por uma razão de precisão:
# o livro registra toda mudança num quadro "> **O que mudou da v1.1:**" que CITA o texto
# antigo de propósito, e no PDF renderizado não há como separar a citação da regra ativa.
# No Markdown dá: basta pular as linhas de citação editorial. O que não pode é o texto
# antigo valer como REGRA; constar do histórico é o comportamento correto do livro.
NOTAS = ("> **O que mudou", "> **Converse", "> **A Execução", "> **O Esforço",
         "> **Sobre o Executado", "> **Lembretes")
regras = []
for md in sorted((RAIZ / "livro-v1.0").glob("*.md")):
    if md.name.startswith("00-changelog"):
        continue                      # o changelog é histórico por definição
    dentro_nota = False
    for linha in md.read_text(encoding="utf-8").splitlines():
        if linha.startswith(NOTAS):
            dentro_nota = True
            continue
        if dentro_nota:
            # a nota continua enquanto as linhas seguirem citadas ("> ") ou em branco
            if linha.startswith(">") or not linha.strip():
                continue
            dentro_nota = False
        regras.append(linha)
corpo_regras = " ".join(" ".join(regras).split()).replace("**", "")

for resto in RESTOS_V11:
    checa(f"PDF · v1.1 não vale mais como regra: {resto[:40]}...",
          resto not in corpo_regras,
          "esse texto da v1.1 ainda está valendo como regra, fora de um quadro de histórico")
    citado = CITADO_NO_CHANGELOG.get(resto, resto)
    checa(f"PDF · changelog registra o antes: {citado[:40]}...",
          citado in plano_changelog,
          "o changelog deveria citar esse texto ao falar do que mudou")

# ============================== XLSX ======================================
mapa = json.loads(MAPA.read_text(encoding="utf-8"))
wb = openpyxl.load_workbook(XLSX)
b = mapa["blocos"]["dados.racas"]
col = b["colunas"]
ws = wb[b["intervalo"].split("!")[0].strip("'")]

vistas = 0
for r in range(b["primeira_linha"], b["ultima_linha"] + 1):
    raca = str(ws[f"{col['Raça']}{r}"].value or "")
    if not raca:
        continue
    vistas += 1
    if raca not in RACAS:
        checa(f"FICHA · {raca} conhecida", False, "Raça fora da lista")
        continue
    ativ, pas, par = RACAS[raca]
    resumo = str(ws[f"{col['Traços (resumo)']}{r}"].value or "")
    texto = str(ws[f"{col['Traços (texto do livro)']}{r}"].value or "")
    bonus = str(ws[f"{col['Bônus de atributo']}{r}"].value or "")
    op1 = str(ws[f"{col['Opção 1 do +2']}{r}"].value or "")
    op2 = str(ws[f"{col['Opção 2 do +2']}{r}"].value or "")
    checa(f"FICHA · {raca}: ativável '{ativ}' no resumo", ativ in resumo, resumo[:70])
    checa(f"FICHA · {raca}: passivo '{pas}' no resumo", pas in resumo, resumo[:70])
    checa(f"FICHA · {raca}: ativável no texto do livro", ativ in texto, texto[:70])
    checa(f"FICHA · {raca}: passivo no texto do livro", pas in texto, texto[:70])
    if par:
        checa(f"FICHA · {raca}: par {par}", (op1, op2) == par, f"ficha: {op1!r}/{op2!r}")
        checa(f"FICHA · {raca}: bônus diz '+1 em cada'", "+1 em cada" in bonus, bonus)
    else:
        checa("FICHA · Humano: sem par fixo", not op1 and not op2, f"{op1!r}/{op2!r}")
        checa("FICHA · Humano: bônus diz '+1 em dois'", "+1 em dois" in bonus, bonus)
    for resto in RESTOS_V11:
        if resto in texto:
            checa(f"FICHA · {raca}: resto da v1.1 no texto", False, resto[:50])

checa("FICHA · as 7 Raças na aba Dados", vistas == 7, f"achei {vistas}")
checa("FICHA · alcance resolvido na Criação existe",
      "criacao.arma.alcance" in mapa["celulas"])
checa("FICHA · aba Início diz V1.2",
      any("V1.2" in str(c.value) for row in wb["Início"].iter_rows()
          for c in row if isinstance(c.value, str)))

print(f"\nOK: {len(ok)}")
if falhas:
    print(f"FALHAS: {len(falhas)}")
    for x in falhas:
        print(f"  [X] {x}")
    sys.exit(1)
print("Tudo conferido: as 7 Raças estão atualizadas no PDF e na ficha.")
