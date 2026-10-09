# -*- coding: utf-8 -*-
"""Renderiza em PNG as páginas do capítulo 05 do PDF V1.2, para conferência visual.

Buscar por trecho de texto não serve: o changelog fica na frente do livro e cita os
mesmos nomes, então a primeira página com "Asas de Halo" é a do changelog, não a da
Raça. Aqui o capítulo é localizado pelo título e renderizado inteiro, do início até
o título do capítulo seguinte.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
PDF = RAIZ / "Sistema de HSR by MC Filhos V1.2.pdf"
SAIDA = Path(__file__).parent / "paginas"
SAIDA.mkdir(parents=True, exist_ok=True)

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        sys.exit("PyMuPDF não está instalado: pip install pymupdf")

doc = pymupdf.open(PDF)
print(f"PDF com {doc.page_count} páginas")


def achar(titulo, inicio=0):
    """Primeira página, a partir de `inicio`, cujo texto começa pelo título do capítulo."""
    for i in range(inicio, doc.page_count):
        t = doc[i].get_text().lstrip()
        if t.startswith(titulo):
            return i
    return None


# O capítulo 05 de verdade: o título abre a página. O changelog cita os nomes, mas não
# tem uma página que comece com "Capítulo 05".
ini = achar("Capítulo 05")
if ini is None:
    sys.exit("não achei a página de abertura do capítulo 05")
fim = achar("Capítulo 06", ini + 1)
if fim is None:
    fim = min(ini + 12, doc.page_count)
print(f"Capítulo 05: páginas {ini + 1} a {fim} (o 06 começa em {fim + 1})")

for i in range(ini, fim):
    doc[i].get_pixmap(dpi=130).save(SAIDA / f"cap05-p{i + 1:03d}.png")
print(f"  {fim - ini} páginas do capítulo 05 renderizadas")

# A tabela de Perícias de 4.5, que ganhou a linha do Humano
ini4 = achar("Capítulo 04")
alvo4 = None
for i in range(ini4 or 0, (ini4 or 0) + 14):
    if i < doc.page_count and doc[i].search_for("Perícias escolhidas — Humano"):
        alvo4 = i
        break
if alvo4 is not None:
    doc[alvo4].get_pixmap(dpi=130).save(SAIDA / f"cap04-pericias-p{alvo4 + 1:03d}.png")
    print(f"  4.5 com a linha do Humano: página {alvo4 + 1}")
else:
    print("  AVISO: não achei a tabela de Perícias de 4.5 dentro do capítulo 04")

print(f"\nPNGs em {SAIDA}")
