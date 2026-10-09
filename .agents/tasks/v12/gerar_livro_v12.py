# -*- coding: utf-8 -*-
"""Emite as entradas de LIVRO_V12 (suíte google de testar_ficha.py) para o Haloviano.

A suíte google compara a ficha gerada com um export do Google feito pelo usuário em
04/10/2026, que não pode ser refeito. O export é da Raça **Haloviano**, então é nele
que toda mudança do capítulo 05 aparece célula por célula. Quando o livro muda, cada
divergência legítima entra em LIVRO_V12 como o par exato (o que o Google gravou, o
que a v1.2 traz).

O valor NOVO é lido do próprio módulo de dados e do gerador, para não haver erro de
transcrição. O valor ANTIGO é o da v1.1, que está escrito aqui porque o arquivo da
v1.1 não existe mais — ele é a verdade de referência do export.
"""
import sys
from pathlib import Path

#  .agents/tasks/v12/este-arquivo.py  ->  quatro níveis até a raiz do projeto
RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "build"))

import ficha_dados  # noqa: E402
import gerar_ficha  # noqa: E402

linha = next(r for r in ficha_dados.racas() if r["raca"] == "Haloviano")

# --- v1.1: o que o export do Google gravou -------------------------------------------------
B29_ANTIGO = "To na sua mente (2 vezes por dia, deixa o alvo Controlado)"
B30_ANTIGO = (
    "To na sua mente: 2 vezes por dia. Gaste a sua Ação Complementar. 1. Ativação. Se você "
    "segue o Caminho da Harmonia, não há teste de ativação. Caso contrário, faça um Teste de "
    "Sintonia contra DT 13; se falhar, você não pode usar este traço até o próximo Descanso "
    "Longo. 2. Resistência do alvo. Em ambos os casos, o alvo faz um Teste de Força de Vontade "
    "contra a sua DT (8 + Bônus do Atributo de Habilidade + Eficiência). 3. Na falha do alvo, "
    "ele fica Controlado (capítulo 21) por 2 turnos se for Comum, ou 1 turno se for Elite ou "
    "Boss. Não funciona em Boss em cena de clímax sem autorização do Mestre. Fora de combate, "
    "o Mestre define a duração pela cena — a referência é meia hora. A DT 13 da ativação é "
    "fixa em todas as faixas e é uma das cinco DTs de subsistema do livro (capítulo 02)."
)
EJ_ANTIGO = "—"

ENTRADAS = [
    ("'Criação'!C25", "Escolha onde vai o +2: Sincronia ou Presença",
     "Escolha onde vai o +2: Discernimento ou Presença"),
    ("'Criação'!N25", "Sincronia", "Discernimento"),
    ("'Criação'!O25", "Sincronia", "Discernimento"),
    ("'Criação'!B29", B29_ANTIGO, linha["tracos"]),
    ("'Criação'!B30", B30_ANTIGO, linha["texto_tracos"]),
    ("'Em Jogo'!B10", EJ_ANTIGO, gerar_ficha.EJ_VANTAGENS_CURTAS["Haloviano"]),
]


def bloco(texto, recuo, largura=104):
    """Quebra um literal longo em linhas de string adjacentes, como o arquivo já faz."""
    if len(texto) + len(recuo) + 2 <= largura:
        return repr(texto)
    partes, atual = [], ""
    for palavra in texto.split(" "):
        if atual and len(atual) + len(palavra) + 1 > largura - len(recuo) - 4:
            partes.append(atual + " ")
            atual = palavra
        else:
            atual = f"{atual} {palavra}".strip()
    partes.append(atual)
    sep = "\n" + recuo
    return sep.join(repr(p) for p in partes)


saida = []
for ref, antigo, novo in ENTRADAS:
    if antigo == novo:
        raise SystemExit(f"ERRO: {ref} não divergiu — não deve entrar em LIVRO_V12")
    chave = f'    {ref!r}: ('
    recuo = " " * len(chave)
    saida.append(f"{chave}{bloco(antigo, recuo)},\n{recuo}{bloco(novo, recuo)}),")

destino = Path(__file__).with_name("livro_v12_entradas.txt")
destino.write_text("\n".join(saida) + "\n", encoding="utf-8")
print(f"gravado: {destino}")
for ref, antigo, novo in ENTRADAS:
    print(f"  {ref}: {len(antigo)} -> {len(novo)} caracteres")
