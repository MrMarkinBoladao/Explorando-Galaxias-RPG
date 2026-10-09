# -*- coding: utf-8 -*-
"""
teste_paisagem.py — Prova que o plano B das tabelas largas funciona.

Nenhuma tabela do livro v1.0 precisa de pagina deitada: a maior (13 colunas,
a de ancoras do bestiario) cabe no retrato com 7 pt. Este teste forca o caso
apertando o piso de fonte do gerador, para garantir que o caminho de PAISAGEM
nao esta quebrado — se um dia o autor escrever uma tabela mais larga, o livro
continua saindo.

Ele gera um PDF pequeno em .agents/tasks/ e rasteriza a pagina deitada em
.agents/tasks/pdf-paginas/paisagem-fallback.png.

Uso (a partir da raiz do projeto):
    python ".agents\\tasks\\teste_paisagem.py"
"""

import importlib.util
import os

import pymupdf

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PASTA_TAREFAS = os.path.join(RAIZ, ".agents", "tasks")
SAIDA = os.path.join(PASTA_TAREFAS, "_teste-paisagem.pdf")

spec = importlib.util.spec_from_file_location(
    "gerar_pdf", os.path.join(RAIZ, "build", "gerar_pdf.py"))
gerar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gerar)

# Bloco de tabela GFM com 13 colunas, igual ao do capitulo 28.
TABELA = [
    "| Faixa | PV Comum | PV Elite | PV Boss | Defesa C / E / B | RD C / E / B |"
    " Tenacidade C / E / B | VEL C / E / B | Ataque | Dano por acerto C / E / B |"
    " DT dos efeitos C / E / B | Teste de Resistência C / E / B | Fraquezas C / E / B |",
    "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    "| **1-4** | **50** | **120** | **305** | 13 / 15 / 16 | 0 / 2 / 4 |"
    " 3 / 5 / 10 | 11 / 12 / 13 | **+7** | **3 / 7 / 10** | 12 / 13 / 14 |"
    " +1 / +2 / +3 | 1-2 / 3 / 4 |",
    "| **17-20** | **155** | **365** | **935** | 24 / 26 / 27 | 0 / 4 / 8 |"
    " 4 / 7 / 13 | 15 / 17 / 19 | **+13** | **16 / 32 / 48** | 19 / 20 / 21 |"
    " +7 / +8 / +9 | 1-2 / 3 / 4 |",
]


def main():
    gerar.registrar_fontes()

    # Aperta o gerador: com piso de 8,5 pt nada tao largo cabe no retrato, e o
    # plano B (pagina deitada) tem de entrar.
    gerar.FONTE_TABELA_CONFORTAVEL = 9.0
    gerar.PISO_FONTE_TABELA = 8.5

    estado = {
        "estilos": gerar.criar_estilos(),
        "imagens": 0, "tabelas": 0, "tabelas_paisagem": 0,
        "marcadores": 0, "capa_usada": True, "avisos": [],
    }

    historia = []
    gerar.renderizar_blocos(historia, [
        "# Teste do plano B",
        "",
        "Texto antes da tabela, em retrato.",
        "",
    ] + TABELA + [
        "",
        "Texto depois da tabela: tem de voltar ao retrato.",
    ], estado)

    documento = gerar.DocumentoLivro(
        SAIDA, pagesize=gerar.PAGINA_RETRATO,
        pageTemplates=gerar.criar_modelos_de_pagina(),
        title="Teste do plano B", author="MC Filhos",
    )
    documento.multiBuild(historia)

    print(f"tabelas: {estado['tabelas']} | em paisagem: "
          f"{estado['tabelas_paisagem']} | avisos: {len(estado['avisos'])}")

    doc = pymupdf.open(SAIDA)
    print(f"paginas: {doc.page_count}")
    deitadas = []
    for indice, pagina in enumerate(doc, start=1):
        orientacao = ("paisagem" if pagina.rect.width > pagina.rect.height
                      else "retrato")
        caixas = [b[:4] for b in pagina.get_text("blocks")]
        esquerda = min((c[0] for c in caixas), default=0)
        direita = max((c[2] for c in caixas), default=0)
        print(f"  pagina {indice}: {orientacao:8s} "
              f"{pagina.rect.width:.0f}x{pagina.rect.height:.0f} "
              f"texto de x={esquerda:.1f} a x={direita:.1f}")
        if orientacao == "paisagem":
            deitadas.append(indice)

    if deitadas:
        destino = os.path.join(PASTA_TAREFAS, "pdf-paginas",
                               "paisagem-fallback.png")
        pagina = doc[deitadas[0] - 1]
        pagina.get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6)).save(destino)
        print(f"pagina deitada rasterizada em {destino}")
    else:
        print("ATENCAO: nenhuma pagina em paisagem foi gerada")
    doc.close()


if __name__ == "__main__":
    main()
