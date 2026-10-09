# -*- coding: utf-8 -*-
"""
gerar_pdf.py — Montagem do livro "Explorando Galáxias" v1.2 em PDF.

O QUE ELE FAZ
    Le todos os capitulos Markdown de `livro-v1.0/` na ordem do prefixo numerico
    de 2 digitos e monta um unico PDF (A4) com:
      - pagina de titulo com a capa (image11.png);
      - sumario com NUMEROS DE PAGINA REAIS (duas passadas do ReportLab:
        `multiBuild` + `afterFlowable` notificando cada titulo);
      - marcadores/outline navegaveis no PDF, hierarquicos (H1 > H2 > H3);
      - numero de pagina em todas as paginas e cabecalho corrido com o nome do
        capitulo atual;
      - cada capitulo comecando em pagina nova;
      - tabelas GFM como tabelas de verdade, com largura de coluna calculada
        pelo conteudo, cabecalho repetido na quebra de pagina e zebrado;
      - as imagens de `assets/imagens-v01/` onde o Markdown as referencia.

    O parser de Markdown e o MESMO de `build/gerar_docx.py` (mesmas expressoes
    regulares, mesma ordem de blocos, mesmas decisoes sobre regua horizontal,
    comentarios HTML, numeracao literal de lista e reuso da capa). A ideia e que
    o PDF e o .docx mostrem exatamente o mesmo conteudo — aqui so muda o
    back-end de desenho (ReportLab em vez de python-docx).

COMO USAR
    A partir da RAIZ do projeto (a pasta que contem `livro-v1.0/`):

        python "build\\gerar_pdf.py"

    Edite os .md quantas vezes quiser e rode de novo: o PDF e regerado por
    inteiro, sobrescrevendo o anterior.

SAIDA
    <raiz do projeto>\\Sistema de HSR by MC Filhos V1.2.pdf

REQUISITOS
    Python 3, reportlab e pillow (`python -m pip install reportlab pillow`).
"""

import io
import logging
import os
import re
import sys
import warnings

try:
    import reportlab
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable,
                                    Frame, HRFlowable, Image, NextPageTemplate,
                                    PageBreak, PageTemplate, Paragraph,
                                    Preformatted, Spacer, Table, TableStyle)
    from reportlab.platypus.tableofcontents import TableOfContents
except ImportError:  # pragma: no cover - ambiente sem a dependencia
    print("ERRO: reportlab nao esta instalado. Rode: python -m pip install reportlab pillow")
    sys.exit(1)

try:
    from PIL import Image as ImagemPIL
except ImportError:  # pragma: no cover
    print("ERRO: pillow nao esta instalado. Rode: python -m pip install pillow")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Configuracao (caminhos e constantes do livro) — espelha gerar_docx.py
# ---------------------------------------------------------------------------

# A raiz do projeto e a pasta ACIMA de build/ — assim o script funciona tanto
# chamado como `python "build\gerar_pdf.py"` quanto de dentro de build/.
DIR_BUILD = os.path.dirname(os.path.abspath(__file__))
DIR_RAIZ = os.path.dirname(DIR_BUILD)

DIR_CAPITULOS = os.path.join(DIR_RAIZ, "livro-v1.0")
DIR_IMAGENS = os.path.join(DIR_RAIZ, "assets", "imagens-v01")

# Caminho EXATO do arquivo final pedido pelo autor.
ARQUIVO_SAIDA = os.path.join(DIR_RAIZ, "Sistema de HSR by MC Filhos V1.2.pdf")

# Metadados da pagina de titulo.
TITULO_LIVRO = "Explorando Galáxias"
SUBTITULO_LIVRO = "Um sistema de RPG de mesa no universo de Honkai: Star Rail"
AUTOR_LIVRO = "by MC Filhos"
VERSAO_LIVRO = "Versão 1.2"

# Capa: definida no mapa de imagens do design (image11.png, 2048x2048).
ARQUIVO_CAPA = "image11.png"

# Geometria da pagina. Margens confortaveis de livro; o cabecalho e o rodape
# ficam FORA da area de texto (desenhados direto no canvas), por isso a margem
# de cima e a de baixo sao um pouco maiores que as do .docx.
PAGINA_RETRATO = A4                       # 21,0 x 29,7 cm
PAGINA_PAISAGEM = landscape(A4)           # 29,7 x 21,0 cm
MARGEM_LATERAL = 2.2 * cm
MARGEM_SUPERIOR = 2.4 * cm
MARGEM_INFERIOR = 2.2 * cm
MARGEM_LATERAL_PAISAGEM = 2.0 * cm

LARGURA_UTIL_RETRATO = PAGINA_RETRATO[0] - 2 * MARGEM_LATERAL
ALTURA_UTIL_RETRATO = PAGINA_RETRATO[1] - MARGEM_SUPERIOR - MARGEM_INFERIOR
LARGURA_UTIL_PAISAGEM = PAGINA_PAISAGEM[0] - 2 * MARGEM_LATERAL_PAISAGEM
ALTURA_UTIL_PAISAGEM = PAGINA_PAISAGEM[1] - MARGEM_SUPERIOR - MARGEM_INFERIOR
# A pagina de titulo usa quase a pagina inteira (nao tem cabecalho).
ALTURA_UTIL_CAPA = PAGINA_RETRATO[1] - MARGEM_INFERIOR - 1.6 * cm

# Limites de tamanho das imagens dentro da pagina (em pontos). Os mesmos do
# .docx (4,6 x 6,2 polegadas no corpo; 5,6 x 5,6 na capa), para as figuras
# sairem do mesmo tamanho nos dois formatos.
LARGURA_MAX_IMAGEM = 4.6 * 72
ALTURA_MAX_IMAGEM = 6.2 * 72
LARGURA_MAX_CAPA = 5.6 * 72
ALTURA_MAX_CAPA = 5.6 * 72

# Resolucao maxima com que uma imagem e embutida: acima disso ela e reduzida.
# 300 dpi no tamanho em que aparece impressa — qualidade de grafica sem inflar
# o arquivo (a capa tem 2048 px e seria embutida inteira sem isso).
DPI_MAXIMO_IMAGEM = 300

# Quanto a figura pode encolher para NAO deixar buraco no pe da pagina.
# Figura e legenda sao um bloco que nao se parte: quando o que resta na pagina
# e menor que esse bloco, ou a figura encolhe (proporcionalmente, sem distorcer)
# ou a pagina acaba ali com um terco em branco. Sao dois limites, e vale o mais
# apertado dos dois:
#   - a figura nunca sai com menos de metade do tamanho natural;
#   - a figura nunca sai com menos de 6 cm de altura.
# O segundo limite protege as figuras pequenas: uma arte de 4 cm nao encolhe,
# ela pula de pagina (e o buraco que ela deixa e pequeno de qualquer jeito).
ESCALA_MINIMA_FIGURA = 0.50
ALTURA_MINIMA_FIGURA = 6.0 * cm
# Rede de seguranca: figura maior que a moldura inteira (so aconteceria numa
# pagina em paisagem) encolhe ate caber, em vez de derrubar a montagem.
ESCALA_MINIMA_ABSOLUTA_FIGURA = 0.30

# Corpo do texto.
TAMANHO_CORPO = 10.5
ENTRELINHA_CORPO = 14.6

# Numero de pagina (folio) na pagina de titulo. Livro costuma suprimir: a pagina
# 1 conta na sequencia (a pagina 2 imprime "2"), mas nao leva numero debaixo da
# capa. Deixe True se quiser o folio impresso tambem na pagina de titulo.
FOLIO_NA_PAGINA_DE_TITULO = False

# Tabelas: escada de tamanhos de fonte e piso de legibilidade.
PISO_FONTE_TABELA = 6.0
ESCADA_FONTE_TABELA = (9.0, 8.5, 8.0, 7.5, 7.0, 6.5, 6.0)
# Abaixo de 7 pt a tabela ja fica desconfortavel; e o gatilho para tentar paisagem.
FONTE_TABELA_CONFORTAVEL = 7.0
RECHEIO_TABELA = 3.2          # padding lateral de cada celula
# Celula que e so numero com separadores ("13 / 15 / 16", "+1 / +2 / +3") conta
# como palavra UNICA no calculo da largura minima da coluna: valor partido em
# duas linhas ("0 / 2 /" + "4") nao se le. O limite de tamanho evita que uma
# celula comprida demais infle a coluna.
RE_CELULA_NUMERICA = re.compile(
    r"^[\s\+\-\(\u2212\u2192]*\d"
    r"[\d\s/,\.%\(\)\+\-x\u00d7\u2212\u2013\u2014\u2192\u2265\u2264]*$")
LIMITE_CELULA_NUMERICA = 20   # em caracteres

# Piso de fonte do bloco de codigo em arte ASCII (as fichas do capitulo 29).
PISO_FONTE_CODIGO = 6.0

# Niveis de titulo que entram no sumario (0 = H1, 1 = H2). O H3 fica de fora
# porque sao 329 entradas: elas estao todas nos marcadores do PDF, que e onde a
# navegacao fina se usa de verdade, e assim o sumario continua legivel.
NIVEL_MAX_SUMARIO = 1

# Paleta: azul-indigo de nave espacial + cinzas. Da hierarquia visual aos
# titulos, tabelas e citacoes sem pesar na impressao.
COR_ACENTO = colors.HexColor("#2F2A6B")
COR_ACENTO_CLARO = colors.HexColor("#5A54A8")
COR_TEXTO = colors.HexColor("#1A1A1A")
COR_TEXTO_FRACO = colors.HexColor("#6B6B78")
COR_GRADE = colors.HexColor("#C9C7DC")
COR_ZEBRA = colors.HexColor("#F2F1F8")
COR_FUNDO_CITACAO = colors.HexColor("#F4F3FA")
COR_FUNDO_CODIGO = colors.HexColor("#F1F1F4")


# ---------------------------------------------------------------------------
# Fontes
# ---------------------------------------------------------------------------

# O livro usa 5 caracteres fora do Latin-1 (→ ≥ ≈ ≤ −). As fontes nativas do
# PDF (Helvetica/Courier) nao os tem, entao registramos TrueType do sistema.
# Se nenhuma for encontrada, caimos para as nativas e trocamos esses 5
# caracteres por equivalentes ASCII — o livro sai inteiro de qualquer jeito.
PASTA_FONTES_WINDOWS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")

FAMILIAS_TEXTO = (
    # (nome registrado, normal, negrito, italico, negrito-italico)
    ("Calibri", "calibri.ttf", "calibrib.ttf", "calibrii.ttf", "calibriz.ttf"),
    ("Arial", "arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf"),
    ("DejaVuSans", "DejaVuSans.ttf", "DejaVuSans-Bold.ttf",
     "DejaVuSans-Oblique.ttf", "DejaVuSans-BoldOblique.ttf"),
)
FAMILIAS_MONO = (
    ("Consolas", "consola.ttf", "consolab.ttf", "consolai.ttf", "consolaz.ttf"),
    ("CourierNew", "cour.ttf", "courbd.ttf", "couri.ttf", "courbi.ttf"),
    ("DejaVuSansMono", "DejaVuSansMono.ttf", "DejaVuSansMono-Bold.ttf",
     "DejaVuSansMono-Oblique.ttf", "DejaVuSansMono-BoldOblique.ttf"),
)

SUBSTITUICOES_ASCII = {
    "\u2192": "->", "\u2265": ">=", "\u2264": "<=",
    "\u2248": "~", "\u2212": "-",
}

# Preenchidos por registrar_fontes().
FONTE_TEXTO = "Helvetica"
FONTE_TEXTO_NEGRITO = "Helvetica-Bold"
FONTE_TEXTO_ITALICO = "Helvetica-Oblique"
FONTE_MONO = "Courier"
FONTES_UNICODE = False


def _registrar_familia(candidatas):
    """Registra a primeira familia TrueType disponivel. Devolve o nome ou None."""
    for nome, normal, negrito, italico, negrito_italico in candidatas:
        caminhos = [os.path.join(PASTA_FONTES_WINDOWS, a)
                    for a in (normal, negrito, italico, negrito_italico)]
        if not all(os.path.isfile(c) for c in caminhos):
            continue
        try:
            pdfmetrics.registerFont(TTFont(nome, caminhos[0]))
            pdfmetrics.registerFont(TTFont(nome + "-Bold", caminhos[1]))
            pdfmetrics.registerFont(TTFont(nome + "-Italic", caminhos[2]))
            pdfmetrics.registerFont(TTFont(nome + "-BoldItalic", caminhos[3]))
            pdfmetrics.registerFontFamily(
                nome,
                normal=nome,
                bold=nome + "-Bold",
                italic=nome + "-Italic",
                boldItalic=nome + "-BoldItalic",
            )
            return nome
        except Exception as erro:  # fonte corrompida ou sem permissao de leitura
            print(f"  AVISO: nao deu para usar a fonte {nome}: {erro}")
    return None


def registrar_fontes():
    """Define as fontes do livro (TrueType com Unicode, ou as nativas do PDF)."""
    global FONTE_TEXTO, FONTE_TEXTO_NEGRITO, FONTE_TEXTO_ITALICO
    global FONTE_MONO, FONTES_UNICODE

    texto = _registrar_familia(FAMILIAS_TEXTO)
    mono = _registrar_familia(FAMILIAS_MONO)

    if texto:
        FONTE_TEXTO = texto
        FONTE_TEXTO_NEGRITO = texto + "-Bold"
        FONTE_TEXTO_ITALICO = texto + "-Italic"
    if mono:
        FONTE_MONO = mono

    FONTES_UNICODE = bool(texto and mono)
    if not FONTES_UNICODE:
        print("  AVISO: sem fontes TrueType completas; os sinais de seta e de"
              " comparacao saem em ASCII (->, >=, <=, ~, -).")
    return FONTE_TEXTO, FONTE_MONO


# ---------------------------------------------------------------------------
# Expressoes regulares do parser de Markdown — identicas as do gerar_docx.py
# ---------------------------------------------------------------------------

RE_TITULO = re.compile(r"^(#{1,6})\s+(.*)$")
RE_IMAGEM = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")
RE_REGUA = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")       # linha horizontal (---)
RE_CERCA = re.compile(r"^\s*(```|~~~)")                       # bloco de codigo
RE_CITACAO = re.compile(r"^\s*>\s?(.*)$")                     # blockquote
RE_LISTA_MARCADOR = re.compile(r"^(\s*)[-*+]\s+(.*)$")        # - item
RE_LISTA_NUMERO = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")      # 1. item
RE_COMENTARIO_HTML = re.compile(r"<!--.*?-->", re.DOTALL)
RE_SEPARADOR_TABELA = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")
RE_QUEBRA_HTML = re.compile(r"<br\s*/?>", re.IGNORECASE)

# Inline: ***forte+italico***, **forte**, *italico*, _italico_, `codigo`, [texto](url)
RE_INLINE = re.compile(
    r"(\*\*\*.+?\*\*\*"
    r"|\*\*.+?\*\*"
    r"|\*[^*\n]+?\*"
    r"|__.+?__"
    r"|_[^_\n]+?_"
    r"|`[^`]+?`"
    r"|\[[^\]]*\]\([^)]*\))",
    re.DOTALL,
)

MARCA_QUEBRA = "\x00br\x00"   # sentinela interna para o <br> do Markdown

# ---------------------------------------------------------------------------
# Leitura e ordenacao dos capitulos — identicas as do gerar_docx.py
# ---------------------------------------------------------------------------

def listar_capitulos(diretorio):
    """Devolve os .md do diretorio ordenados pelo prefixo numerico de 2 digitos.

    Empate de prefixo (ha dois arquivos `00-`) e resolvido pelo nome do arquivo,
    para a ordem ser sempre a mesma em qualquer maquina.
    """
    if not os.path.isdir(diretorio):
        raise SystemExit(f"ERRO: pasta de capitulos nao encontrada: {diretorio}")

    arquivos = [n for n in os.listdir(diretorio) if n.lower().endswith(".md")]

    def chave(nome):
        casamento = re.match(r"^(\d{2})", nome)
        # Arquivo sem prefixo numerico vai para o fim, nunca quebra o build.
        prefixo = int(casamento.group(1)) if casamento else 9999
        return (prefixo, nome.lower())

    arquivos.sort(key=chave)
    if not arquivos:
        raise SystemExit(f"ERRO: nenhum .md encontrado em {diretorio}")
    return [os.path.join(diretorio, n) for n in arquivos]


def ler_markdown(caminho):
    """Le um .md em UTF-8 (tolerando BOM) e devolve a lista de linhas."""
    with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
        texto = arquivo.read()
    # Remove comentarios HTML (ex.: <!-- ARTE PENDENTE: ... -->), que nao devem
    # aparecer no livro impresso.
    texto = RE_COMENTARIO_HTML.sub("", texto)
    return texto.replace("\r\n", "\n").replace("\r", "\n").split("\n")


# ---------------------------------------------------------------------------
# Avisos (nenhum problema de formatacao pode abortar o livro)
# ---------------------------------------------------------------------------

def avisar(estado, mensagem):
    """Registra um aviso no console e na lista do relatorio, sem abortar nada."""
    estado["avisos"].append(mensagem)
    if len(estado["avisos"]) <= 60:
        print(f"  AVISO: {mensagem}")


# ---------------------------------------------------------------------------
# Formatacao inline: Markdown -> mini-marcacao do ReportLab
# ---------------------------------------------------------------------------

def escapar(texto):
    """Escapa o que o parser de paragrafo do ReportLab leria como marcacao.

    `<br>` escrito no Markdown (ha varios dentro de celulas de tabela) vira a
    quebra de linha do ReportLab; o resto de `& < >` sai literal.
    """
    texto = RE_QUEBRA_HTML.sub(MARCA_QUEBRA, texto)
    if not FONTES_UNICODE:
        for original, trocado in SUBSTITUICOES_ASCII.items():
            texto = texto.replace(original, trocado)
    texto = (texto.replace("&", "&amp;")
                  .replace("<", "&lt;")
                  .replace(">", "&gt;"))
    texto = texto.replace("\n", MARCA_QUEBRA)
    return texto.replace(MARCA_QUEBRA, "<br/>")


def aplicar_inline(texto, tamanho_base=TAMANHO_CORPO):
    """Converte a marcacao inline do Markdown na marcacao do ReportLab.

    Mesma gramatica do gerar_docx.py: ***forte+italico***, **forte**, *italico*,
    __forte__, _italico_, `codigo` e [rotulo](destino) — do link fica so o
    rotulo, porque os links do livro apontam para outros capitulos do proprio
    livro.
    """
    if not texto:
        return ""
    partes = []
    for pedaco in RE_INLINE.split(texto):
        if not pedaco:
            continue
        if pedaco.startswith("***") and pedaco.endswith("***") and len(pedaco) > 6:
            partes.append("<b><i>%s</i></b>" % aplicar_inline(pedaco[3:-3], tamanho_base))
        elif pedaco.startswith("**") and pedaco.endswith("**") and len(pedaco) > 4:
            partes.append("<b>%s</b>" % aplicar_inline(pedaco[2:-2], tamanho_base))
        elif pedaco.startswith("__") and pedaco.endswith("__") and len(pedaco) > 4:
            partes.append("<b>%s</b>" % aplicar_inline(pedaco[2:-2], tamanho_base))
        elif pedaco.startswith("`") and pedaco.endswith("`") and len(pedaco) > 2:
            # Dentro de ` ` nao ha marcacao: e codigo literal.
            partes.append('<font face="%s" size="%.2f">%s</font>'
                          % (FONTE_MONO, tamanho_base * 0.92, escapar(pedaco[1:-1])))
        elif pedaco.startswith("*") and pedaco.endswith("*") and len(pedaco) > 2:
            partes.append("<i>%s</i>" % aplicar_inline(pedaco[1:-1], tamanho_base))
        elif pedaco.startswith("_") and pedaco.endswith("_") and len(pedaco) > 2:
            partes.append("<i>%s</i>" % aplicar_inline(pedaco[1:-1], tamanho_base))
        elif pedaco.startswith("[") and "](" in pedaco and pedaco.endswith(")"):
            rotulo = pedaco[1:pedaco.index("](")]
            partes.append(aplicar_inline(rotulo, tamanho_base))
        else:
            partes.append(escapar(pedaco))
    return "".join(partes)


def texto_puro(texto):
    """Mesmo texto sem marcacao nenhuma.

    Serve para tres coisas: medir a largura das colunas de tabela, escrever os
    marcadores do PDF e montar as entradas do sumario.
    """
    if not texto:
        return ""
    partes = []
    for pedaco in RE_INLINE.split(texto):
        if not pedaco:
            continue
        if pedaco.startswith("***") and pedaco.endswith("***") and len(pedaco) > 6:
            partes.append(texto_puro(pedaco[3:-3]))
        elif pedaco.startswith("**") and pedaco.endswith("**") and len(pedaco) > 4:
            partes.append(texto_puro(pedaco[2:-2]))
        elif pedaco.startswith("__") and pedaco.endswith("__") and len(pedaco) > 4:
            partes.append(texto_puro(pedaco[2:-2]))
        elif pedaco.startswith("`") and pedaco.endswith("`") and len(pedaco) > 2:
            partes.append(pedaco[1:-1])
        elif pedaco.startswith("*") and pedaco.endswith("*") and len(pedaco) > 2:
            partes.append(texto_puro(pedaco[1:-1]))
        elif pedaco.startswith("_") and pedaco.endswith("_") and len(pedaco) > 2:
            partes.append(texto_puro(pedaco[1:-1]))
        elif pedaco.startswith("[") and "](" in pedaco and pedaco.endswith(")"):
            partes.append(texto_puro(pedaco[1:pedaco.index("](")]))
        else:
            partes.append(pedaco)
    resultado = RE_QUEBRA_HTML.sub("\n", "".join(partes))
    if not FONTES_UNICODE:
        for original, trocado in SUBSTITUICOES_ASCII.items():
            resultado = resultado.replace(original, trocado)
    return resultado


# ---------------------------------------------------------------------------
# Flowables com comportamento proprio
# ---------------------------------------------------------------------------

def folgas_de_decoracao(flowable, recheio):
    """Quanto a decoracao de um flowable pode avancar para fora da caixa dele.

    Citacao e bloco de codigo desenham fundo e barra lateral um pouco PARA FORA
    do retangulo que o ReportLab reservou para o paragrafo — e o que da o ar de
    caixa, em vez de tinta colada na letra. O problema e a borda da moldura: um
    paragrafo que cai rente ao pe (ou ao topo) da area de texto levava a tinta
    para dentro da margem.

    Aqui a folga e cortada no espaco que realmente existe entre o paragrafo e a
    moldura, de modo que a decoracao para exatamente na borda da area de texto.
    Devolve (folga de baixo, folga de cima), em pontos.
    """
    baixo = alto = float(recheio)
    moldura = getattr(flowable, "_frame", None)
    base = getattr(flowable, "_base_y", None)
    if moldura is None or base is None:
        return baixo, alto
    try:
        pe_da_moldura = moldura._y1p
        topo_da_moldura = moldura._y2 - moldura._topPadding
    except AttributeError:      # moldura de outro tipo: mantem a folga cheia
        return baixo, alto
    baixo = max(0.0, min(baixo, base - pe_da_moldura))
    alto = max(0.0, min(alto, topo_da_moldura - (base + flowable.height)))
    return baixo, alto


class ReservaDeEspaco(CondPageBreak):
    """Quebra condicional de pagina com altura MEDIDA, nao chutada.

    O `CondPageBreak(3 cm)` fixo que vinha antes de cada titulo de secao dava
    conta de um titulo seguido de paragrafo, mas nao de um titulo seguido de
    figura: a figura e um bloco que nao se parte e pode pedir 16 cm, entao ela
    pulava de pagina e deixava o titulo sozinho no pe (titulo orfao).

    Esta classe e so um CondPageBreak que o gerador consegue achar depois de
    montar o livro inteiro, para trocar a altura pela que o bloco seguinte
    realmente precisa (ver `amarrar_titulos_aos_blocos`). Os dois sinalizadores
    dizem o que a reserva protege:

      `de_titulo`  — reserva de um titulo de secao (H2/H3);
      `de_bloco`   — reserva do proprio bloco de codigo, que nao quer ser
                     partido no meio.
    """

    def __init__(self, altura, de_titulo=False, de_bloco=False):
        CondPageBreak.__init__(self, altura)
        self.de_titulo = de_titulo
        self.de_bloco = de_bloco


class GrupoDeFigura(Flowable):
    """Figura com legenda: um bloco so, que nunca se parte e que ENCOLHE.

    A legenda nunca se separa da figura. Quando o espaco que resta na pagina e
    menor do que o bloco pede, a figura e reduzida PROPORCIONALMENTE — ate o
    limite de `ESCALA_MINIMA_FIGURA` / `ALTURA_MINIMA_FIGURA` — para o bloco
    caber onde o texto o chamou, em vez de pular de pagina e deixar um terco de
    pagina vazio no pe. Se nem com a reducao couber, o bloco inteiro vai para a
    pagina seguinte (o ReportLab faz isso sozinho quando `wrap` devolve altura
    maior que a disponivel) e la a figura sai no tamanho cheio.

    A reducao e sempre proporcional: largura e altura caem pelo mesmo fator,
    entao a figura nunca distorce.
    """

    def __init__(self, figura, legenda=None, espaco_antes=4.0,
                 espaco_depois=10.0):
        Flowable.__init__(self)
        self.figura = figura
        self.legenda = legenda
        self.largura_figura = float(figura.drawWidth)
        self.altura_figura = float(figura.drawHeight)
        self.spaceBefore = espaco_antes
        self.spaceAfter = espaco_depois
        self.escala = 1.0
        self._altura_legenda = 0.0
        self._largura = self.largura_figura
        self._altura = self.altura_figura
        # Diagnostico (relatorio do fim da montagem): a maior escala que algum
        # pe de pagina chegou a pedir desta figura, e se ela aceitou encolher.
        self.escala_pedida = None
        self.encolheu = False
        self.nome = "figura"

    # -- medidas (usadas tambem pela reserva do titulo) ---------------------

    def _medir_legenda(self, largura, canv=None):
        """Altura da legenda (texto + o espaco que ela pede antes de si)."""
        if self.legenda is None:
            return 0.0
        _, altura = self.legenda.wrapOn(canv or getattr(self, "canv", None),
                                        largura, 0xfffffff)
        return altura + self.legenda.getSpaceBefore()

    def escala_minima(self):
        """Menor reducao aceita para esta figura (vale o limite mais apertado)."""
        if self.altura_figura <= 0:
            return 1.0
        por_altura = min(1.0, ALTURA_MINIMA_FIGURA / self.altura_figura)
        return max(ESCALA_MINIMA_FIGURA, por_altura)

    def altura_natural(self, largura, canv=None):
        """Altura do bloco com a figura no tamanho cheio."""
        return self.altura_figura + self._medir_legenda(largura, canv)

    def altura_minima(self, largura, canv=None):
        """Altura do bloco com a figura no menor tamanho aceito."""
        return (self.altura_figura * self.escala_minima()
                + self._medir_legenda(largura, canv))

    # -- fluxo -------------------------------------------------------------

    def wrap(self, largura_disponivel, altura_disponivel):
        self._largura = largura_disponivel
        self._altura_legenda = self._medir_legenda(largura_disponivel)
        natural = self.altura_figura + self._altura_legenda
        self.escala = 1.0
        self._altura = natural

        if altura_disponivel < natural and self.altura_figura > 0:
            # No topo da moldura nao ha para onde pular: se a figura nao cabe
            # nem numa pagina inteira (so aconteceria em paisagem), ela encolhe
            # o quanto for preciso em vez de derrubar a montagem.
            no_topo = getattr(getattr(self, "_frame", None), "_atTop", False)
            piso = (ESCALA_MINIMA_ABSOLUTA_FIGURA if no_topo
                    else self.escala_minima())
            escala = ((altura_disponivel - self._altura_legenda)
                      / self.altura_figura)
            if self.escala_pedida is None or escala > self.escala_pedida:
                self.escala_pedida = escala
            if escala >= piso:
                self.escala = escala
                self._altura = altura_disponivel
                self.encolheu = True

        self.width, self.height = self._largura, self._altura
        return self._largura, self._altura

    def draw(self):
        largura = self.largura_figura * self.escala
        altura = self.altura_figura * self.escala
        self.figura.drawWidth = largura
        self.figura.drawHeight = altura
        # A figura encosta no topo do bloco e fica centrada na coluna; a legenda
        # vem logo abaixo, na largura toda (por isso ela sai centrada no texto,
        # e nao na figura).
        self.figura.drawOn(self.canv, max(0.0, (self._largura - largura) / 2.0),
                           self._altura - altura)
        if self.legenda is not None:
            self.legenda.drawOn(self.canv, 0.0,
                                self._altura - altura - self._altura_legenda)

    def identity(self, maxLen=None):
        nome = getattr(self.figura, "filename", "figura")
        if not isinstance(nome, str):
            nome = "figura"
        return "<GrupoDeFigura %s %.0fx%.0fpt>" % (
            os.path.basename(nome), self.largura_figura, self.altura_figura)


class Titulo(Paragraph):
    """Titulo de capitulo ou secao.

    Carrega o nivel, o texto puro e a chave do marcador: e por esses atributos
    que o `afterFlowable` do documento registra a entrada do sumario e o
    marcador (outline) do PDF. A regua, quando existe, e desenhada pelo proprio
    flowable — assim ela nunca se separa do titulo numa quebra de pagina.
    """

    # Os parametros `bulletText` e `frags` existem porque `Paragraph.split()`
    # recria o objeto com a propria classe quando um paragrafo quebra no meio.
    # Nesse caso nao vem nivel: o pedaco continuado nao registra marcador nem
    # entrada de sumario de novo (o `afterFlowable` ignora nivel None).
    def __init__(self, markup, estilo, nivel=None, texto="", chave=None,
                 regua=0.0, cor_regua=None, fora_do_sumario=False,
                 bulletText=None, frags=None):
        Paragraph.__init__(self, markup, estilo, bulletText=bulletText,
                           frags=frags)
        self.nivel_titulo = nivel
        self.texto_titulo = texto
        self.chave_marcador = chave
        self.fora_do_sumario = fora_do_sumario
        self._regua = regua
        self._cor_regua = cor_regua or COR_ACENTO

    def draw(self):
        Paragraph.draw(self)
        if self._regua > 0:
            canv = self.canv
            canv.saveState()
            canv.setStrokeColor(self._cor_regua)
            canv.setLineWidth(self._regua)
            altura = -2.0 - self._regua
            canv.line(0, altura, self.width, altura)
            canv.restoreState()


class ParagrafoCitacao(Paragraph):
    """Citacao do Markdown (>): fundo claro e barra lateral de destaque.

    O desenho fica dentro do flowable porque `Paragraph.split()` devolve objetos
    da mesma classe — quando a citacao quebra de pagina, o fundo e a barra
    continuam na pagina seguinte.
    """

    RECHEIO = 5.0
    _base_y = None      # y absoluto da ultima vez que o flowable foi desenhado

    def drawOn(self, canv, x, y, _sW=0):
        # Guardado para `folgas_de_decoracao` saber a que distancia da borda da
        # moldura este paragrafo caiu.
        self._base_y = y
        Paragraph.drawOn(self, canv, x, y, _sW)

    def drawPara(self, debug=0):
        estilo = self.style
        canv = self.canv
        recheio = self.RECHEIO
        baixo, alto = folgas_de_decoracao(self, recheio)
        # A faixa horizontal tambem e presa na largura do flowable: a decoracao
        # nunca passa da coluna de texto.
        x0 = max(0.0, estilo.leftIndent - recheio)
        x1 = min(self.width, self.width - estilo.rightIndent + recheio)
        altura = self.height + baixo + alto
        canv.saveState()
        canv.setFillColor(COR_FUNDO_CITACAO)
        canv.rect(x0, -baixo, x1 - x0, altura, stroke=0, fill=1)
        canv.setFillColor(COR_ACENTO_CLARO)
        canv.rect(x0, -baixo, 2.2, altura, stroke=0, fill=1)
        canv.restoreState()
        Paragraph.drawPara(self, debug)


class BlocoDeCodigo(Preformatted):
    """Bloco cercado (```) em fonte monoespacada, com fundo e barra lateral.

    As fichas em arte ASCII do capitulo 29 sao blocos destes: o alinhamento
    delas depende de fonte de largura fixa e de nao reflui-las.
    """

    RECHEIO = 4.0
    _base_y = None      # y absoluto da ultima vez que o flowable foi desenhado
    # Altura que o bloco vai ocupar, preenchida por `inserir_bloco_de_codigo`.
    # Fica em zero nos pedacos que o proprio ReportLab cria quando um bloco
    # grande e partido entre duas paginas.
    altura_estimada = 0.0

    def split(self, largura_disponivel, altura_disponivel):
        # Preformatted.split devolve Preformatted puro; refazemos como
        # BlocoDeCodigo para o fundo acompanhar a continuacao na outra pagina.
        partes = Preformatted.split(self, largura_disponivel, altura_disponivel)
        return [BlocoDeCodigo("\n".join(parte.lines), parte.style)
                for parte in partes]

    def drawOn(self, canv, x, y, _sW=0):
        self._base_y = y
        Preformatted.drawOn(self, canv, x, y, _sW)

    def draw(self):
        canv = self.canv
        estilo = self.style
        recheio = self.RECHEIO
        baixo, alto = folgas_de_decoracao(self, recheio)
        # `rightIndent` do estilo de codigo e menor que o recheio, por isso o
        # limite da direita e preso na largura do flowable: sem isso o fundo
        # passava 1 pt da margem.
        x0 = max(0.0, estilo.leftIndent - recheio - 1.0)
        x1 = min(self.width, self.width - estilo.rightIndent + recheio + 1.0)
        altura = self.height + baixo + alto
        canv.saveState()
        canv.setFillColor(COR_FUNDO_CODIGO)
        canv.rect(x0, -baixo, x1 - x0, altura, stroke=0, fill=1)
        canv.setFillColor(COR_ACENTO_CLARO)
        canv.rect(x0, -baixo, 2.0, altura, stroke=0, fill=1)
        canv.restoreState()
        Preformatted.draw(self)


# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------

def criar_estilos():
    """Monta o dicionario de estilos do livro."""
    corpo = ParagraphStyle(
        "corpo",
        fontName=FONTE_TEXTO,
        fontSize=TAMANHO_CORPO,
        leading=ENTRELINHA_CORPO,
        textColor=COR_TEXTO,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        splitLongWords=1,     # rede de seguranca: nada vaza a margem
    )

    estilos = {"corpo": corpo}

    estilos["titulo1"] = ParagraphStyle(
        "titulo1", parent=corpo, fontName=FONTE_TEXTO_NEGRITO, fontSize=23,
        leading=27, textColor=COR_ACENTO, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=18,
    )
    estilos["titulo2"] = ParagraphStyle(
        "titulo2", parent=corpo, fontName=FONTE_TEXTO_NEGRITO, fontSize=15,
        leading=18.5, textColor=COR_ACENTO, alignment=TA_LEFT,
        spaceBefore=16, spaceAfter=9,
    )
    estilos["titulo3"] = ParagraphStyle(
        "titulo3", parent=corpo, fontName=FONTE_TEXTO_NEGRITO, fontSize=12,
        leading=15, textColor=COR_ACENTO_CLARO, alignment=TA_LEFT,
        spaceBefore=12, spaceAfter=5,
    )

    estilos["citacao"] = ParagraphStyle(
        "citacao", parent=corpo, fontSize=10, leading=13.6,
        leftIndent=14, rightIndent=8, spaceBefore=9, spaceAfter=10,
        alignment=TA_LEFT,
    )

    estilos["lista"] = ParagraphStyle(
        "lista", parent=corpo, leftIndent=22, bulletIndent=7,
        spaceAfter=4, alignment=TA_LEFT,
        bulletFontName=FONTE_TEXTO_NEGRITO, bulletFontSize=TAMANHO_CORPO,
    )
    estilos["lista2"] = ParagraphStyle(
        "lista2", parent=estilos["lista"], leftIndent=38, bulletIndent=23,
    )
    estilos["lista_citacao"] = ParagraphStyle(
        "lista_citacao", parent=estilos["lista"], fontSize=10, leading=13.6,
        leftIndent=36, bulletIndent=21, rightIndent=8, bulletFontSize=10,
    )
    estilos["lista2_citacao"] = ParagraphStyle(
        "lista2_citacao", parent=estilos["lista_citacao"],
        leftIndent=48, bulletIndent=36,
    )

    estilos["legenda"] = ParagraphStyle(
        "legenda", parent=corpo, fontName=FONTE_TEXTO_ITALICO, fontSize=9,
        leading=11.5, textColor=COR_TEXTO_FRACO, alignment=TA_CENTER,
        spaceBefore=3, spaceAfter=10,
    )

    estilos["codigo"] = ParagraphStyle(
        "codigo", parent=corpo, fontName=FONTE_MONO, fontSize=8, leading=9.8,
        leftIndent=10, rightIndent=4, spaceBefore=10, spaceAfter=12,
        alignment=TA_LEFT,
    )

    # Pagina de titulo.
    estilos["capa_titulo"] = ParagraphStyle(
        "capa_titulo", parent=corpo, fontName=FONTE_TEXTO_NEGRITO, fontSize=34,
        leading=40, textColor=COR_ACENTO, alignment=TA_CENTER,
        spaceBefore=16, spaceAfter=4,
    )
    estilos["capa_subtitulo"] = ParagraphStyle(
        "capa_subtitulo", parent=corpo, fontName=FONTE_TEXTO_ITALICO,
        fontSize=13, leading=17, textColor=COR_TEXTO, alignment=TA_CENTER,
        spaceBefore=8, spaceAfter=4,
    )
    estilos["capa_autor"] = ParagraphStyle(
        "capa_autor", parent=corpo, fontName=FONTE_TEXTO_NEGRITO, fontSize=15,
        leading=19, textColor=COR_TEXTO, alignment=TA_CENTER,
        spaceBefore=26, spaceAfter=2,
    )
    estilos["capa_versao"] = ParagraphStyle(
        "capa_versao", parent=corpo, fontSize=11, leading=14,
        textColor=COR_TEXTO_FRACO, alignment=TA_CENTER, spaceAfter=0,
    )

    # Sumario (as duas colunas de numero de pagina sao desenhadas pelo proprio
    # TableOfContents; o rightIndent abre espaco para elas).
    estilos["sumario_nivel0"] = ParagraphStyle(
        "sumario_nivel0", parent=corpo, fontName=FONTE_TEXTO_NEGRITO,
        fontSize=11, leading=15.5, textColor=COR_ACENTO, alignment=TA_LEFT,
        spaceBefore=7, leftIndent=0, rightIndent=30, firstLineIndent=0,
    )
    estilos["sumario_nivel1"] = ParagraphStyle(
        "sumario_nivel1", parent=corpo, fontSize=9.5, leading=12.8,
        textColor=COR_TEXTO, alignment=TA_LEFT, spaceBefore=0,
        leftIndent=16, rightIndent=30, firstLineIndent=0,
    )
    return estilos


_CACHE_ESTILO_CELULA = {}


def estilo_celula(tamanho, alinhamento, cabecalho):
    """Estilo do paragrafo de uma celula de tabela (em cache: sao ~295 tabelas)."""
    chave = (round(tamanho, 2), alinhamento, bool(cabecalho))
    if chave not in _CACHE_ESTILO_CELULA:
        _CACHE_ESTILO_CELULA[chave] = ParagraphStyle(
            "celula_%s_%s_%s" % chave,
            fontName=FONTE_TEXTO_NEGRITO if cabecalho else FONTE_TEXTO,
            fontSize=tamanho,
            leading=tamanho * 1.22,
            textColor=colors.white if cabecalho else COR_TEXTO,
            alignment=alinhamento,
            spaceBefore=0,
            spaceAfter=0,
            splitLongWords=1,
        )
    return _CACHE_ESTILO_CELULA[chave]


# ---------------------------------------------------------------------------
# Imagens
# ---------------------------------------------------------------------------

_CACHE_IMAGENS = {}


def preparar_imagem(caminho, largura_max, altura_max, estado):
    """Devolve um Image do ReportLab pronto para a pagina, ou None.

    Regras (as mesmas do .docx): a imagem entra no tamanho natural dela, lida a
    96 dpi, e e reduzida proporcionalmente ate caber na largura util e na altura
    maxima. Nunca e ampliada e nunca e distorcida.
    """
    chave = (caminho, round(largura_max, 2), round(altura_max, 2))
    if chave in _CACHE_IMAGENS:
        return _CACHE_IMAGENS[chave]

    if not os.path.isfile(caminho):
        avisar(estado, f"imagem nao encontrada, ignorada: {caminho}")
        return None

    try:
        with ImagemPIL.open(caminho) as origem:
            origem.load()
            if origem.mode in ("RGBA", "LA", "P", "PA"):
                # Compoe sobre branco: a pagina do livro e branca e o PDF nao
                # precisa carregar canal alfa.
                origem = origem.convert("RGBA")
                fundo = ImagemPIL.new("RGB", origem.size, (255, 255, 255))
                fundo.paste(origem, mask=origem.split()[-1])
                imagem = fundo
            else:
                imagem = origem.convert("RGB")

        pixels_largura, pixels_altura = imagem.size
        largura = pixels_largura / 96.0 * 72.0
        altura = pixels_altura / 96.0 * 72.0
        if largura > largura_max:
            altura *= largura_max / largura
            largura = largura_max
        if altura > altura_max:
            largura *= altura_max / altura
            altura = altura_max

        # Reamostra se a imagem tiver mais pixels do que 300 dpi no tamanho
        # final — mantem a nitidez de grafica e evita um PDF inflado.
        teto_pixels = max(1, int(largura / 72.0 * DPI_MAXIMO_IMAGEM))
        if pixels_largura > teto_pixels * 1.05:
            nova_altura = max(1, int(pixels_altura * teto_pixels / pixels_largura))
            imagem = imagem.resize((teto_pixels, nova_altura),
                                   ImagemPIL.LANCZOS)

        buffer_png = io.BytesIO()
        imagem.save(buffer_png, format="PNG", optimize=True)
        buffer_png.seek(0)
        figura = Image(buffer_png, width=largura, height=altura)
        figura.hAlign = "CENTER"
    except Exception as erro:
        avisar(estado, f"nao deu para preparar a imagem {caminho}: {erro}")
        return None

    _CACHE_IMAGENS[chave] = figura
    return figura


# ---------------------------------------------------------------------------
# Tabelas GFM -> tabelas do ReportLab
# ---------------------------------------------------------------------------

def dividir_celulas(linha):
    """Quebra uma linha `| a | b |` na lista de celulas, sem as bordas."""
    conteudo = linha.strip()
    if conteudo.startswith("|"):
        conteudo = conteudo[1:]
    if conteudo.endswith("|"):
        conteudo = conteudo[:-1]
    return [celula.strip() for celula in conteudo.split("|")]


def ler_alinhamentos(linha_separadora):
    """Traduz `|:---|---:|:---:|` para os alinhamentos de cada coluna."""
    alinhamentos = []
    for marca in dividir_celulas(linha_separadora):
        esquerda = marca.startswith(":")
        direita = marca.endswith(":")
        if esquerda and direita:
            alinhamentos.append(TA_CENTER)
        elif direita:
            alinhamentos.append(TA_RIGHT)
        else:
            alinhamentos.append(TA_LEFT)
    return alinhamentos


def eh_inicio_de_tabela(linhas, indice):
    """Verdadeiro se em `indice` comeca uma tabela GFM (cabecalho + separador)."""
    if indice + 1 >= len(linhas):
        return False
    atual = linhas[indice].strip()
    proxima = linhas[indice + 1].strip()
    if not atual.startswith("|"):
        return False
    return bool(RE_SEPARADOR_TABELA.match(proxima)) and "|" in proxima


def _medir_colunas(matriz, total_colunas, tamanho, tem_cabecalho):
    """Mede, por coluna, a maior palavra e a maior linha de texto (em pontos).

    A maior PALAVRA e o minimo absoluto da coluna: o ReportLab quebra a linha
    nos espacos, nao no meio da palavra. A maior LINHA e a largura ideal, a que
    faria a celula nao quebrar em nenhuma linha.

    Excecao: celula que e so numero com separadores ("13 / 15 / 16",
    "+1 / +2 / +3", "0 / 2 / 4") conta como UMA palavra, ou seja, a linha
    inteira entra no minimo. Numero partido em duas linhas nao se le, e o
    espaco em branco ganho apertando essa coluna nao vale o estrago.
    """
    minimos = []
    desejadas = []
    for coluna in range(total_colunas):
        maior_palavra = 0.0
        maior_linha = 0.0
        for indice_linha, linha in enumerate(matriz):
            bruto = linha[coluna] if coluna < len(linha) else ""
            # v1.2: a celula do CORPO era sempre medida com a fonte REGULAR, mesmo quando
            # o Markdown dela pede **negrito** ou `mono` -- e as duas sao mais largas que
            # a regular no mesmo tamanho. A coluna saia subestimada e o ReportLab quebrava
            # a palavra no meio. Dois casos reais na tabela de consulta rapida do capitulo
            # 05, que apareceram quando a coluna de tracos cresceu e tirou a folga que
            # mascarava o erro: "Xianzhouit/a" (negrito) e "image12.pn/g" (mono).
            #
            # A celula e medida com a MAIS LARGA das fontes que ela pode usar. E
            # conservador de proposito -- uma celula meio negrito e medida inteira em
            # negrito --, porque errar para o lado da folga nao estraga a pagina e errar
            # para o lado de menos parte palavra.
            if tem_cabecalho and indice_linha == 0:
                fontes = (FONTE_TEXTO_NEGRITO,)
            else:
                fontes = [FONTE_TEXTO]
                if "**" in (bruto or ""):
                    fontes.append(FONTE_TEXTO_NEGRITO)
                if "`" in (bruto or ""):
                    fontes.append(FONTE_MONO)
                fontes = tuple(fontes)

            def _largura(txt, _fontes=fontes, _tam=tamanho):
                return max(stringWidth(txt, f, _tam) for f in _fontes)

            for pedaco in texto_puro(bruto).split("\n"):
                largura_pedaco = _largura(pedaco)
                maior_linha = max(maior_linha, largura_pedaco)
                limpo = pedaco.strip()
                if (len(limpo) <= LIMITE_CELULA_NUMERICA
                        and RE_CELULA_NUMERICA.match(limpo)):
                    maior_palavra = max(maior_palavra, largura_pedaco)
                    continue
                for palavra in pedaco.split():
                    maior_palavra = max(maior_palavra, _largura(palavra))
        minimos.append(maior_palavra + 2 * RECHEIO_TABELA + 1.0)
        desejadas.append(max(maior_linha + 2 * RECHEIO_TABELA + 1.0, minimos[-1]))
    return minimos, desejadas


def _distribuir_larguras(minimos, desejadas, largura_disponivel):
    """Reparte a faixa util entre as colunas. Devolve None se nem o minimo cabe.

    O resultado SEMPRE soma no maximo `largura_disponivel` — e isso que garante
    que nenhuma tabela do livro vaze a margem.

    O reparto e "max-min": existe um nivel de agua L tal que toda coluna que
    quer MENOS que L recebe exatamente o que quer, e as colunas que querem mais
    recebem L. Isso e muito melhor que repartir proporcionalmente: as colunas
    estreitas (`Faixa`, `PV`, `+12`) ficam numa linha so, e quem aperta e apenas
    a coluna de texto comprido, que ia quebrar linha de qualquer jeito.
    """
    if sum(minimos) > largura_disponivel:
        return None

    if sum(desejadas) <= largura_disponivel:
        # Cabe inteira: estica proporcionalmente para ocupar a faixa (tabela de
        # livro ocupando a largura do texto fica melhor que tabela encolhida).
        fator = largura_disponivel / sum(desejadas)
        return [desejada * fator for desejada in desejadas]

    def soma_com_nivel(nivel):
        return sum(max(minimo, min(desejada, nivel))
                   for minimo, desejada in zip(minimos, desejadas))

    baixo, alto = 0.0, max(desejadas)
    for _ in range(60):      # busca binaria do nivel de agua
        meio = (baixo + alto) / 2.0
        if soma_com_nivel(meio) > largura_disponivel:
            alto = meio
        else:
            baixo = meio

    larguras = [max(minimo, min(desejada, baixo))
                for minimo, desejada in zip(minimos, desejadas)]

    # A sobra (por causa das colunas presas no minimo) vai para quem ainda
    # queria mais largura.
    folga = largura_disponivel - sum(larguras)
    if folga > 0.5:
        famintas = [indice for indice, (largura, desejada)
                    in enumerate(zip(larguras, desejadas))
                    if desejada > largura + 0.5]
        if famintas:
            parte = folga / len(famintas)
            for indice in famintas:
                larguras[indice] += parte
    return larguras


def escolher_layout_tabela(matriz, total_colunas, tem_cabecalho,
                           largura_retrato, largura_paisagem):
    """Escolhe tamanho de fonte, larguras de coluna e orientacao da tabela.

    ESTRATEGIA PARA TABELAS LARGAS (decisao documentada):

      1. a fonte comeca num tamanho que depende do numero de colunas (9 pt ate
         4 colunas, caindo ate 7 pt com 11 ou mais);
      2. se a soma das larguras minimas nao couber na faixa util, a fonte desce
         um degrau por vez (9 > 8,5 > ... > 6 pt), com piso de 6 pt — abaixo
         disso a tabela deixaria de ser legivel;
      3. se a tabela nao couber no RETRATO com pelo menos 7 pt, ela sai sozinha
         numa pagina em PAISAGEM (A4 deitado, 25,7 cm de faixa util) e o texto
         volta ao retrato na pagina seguinte. Preferi paisagem a quebrar a
         tabela em blocos de colunas porque a tabela de ancoras do bestiario
         (13 colunas) so se le inteira: cada linha e um orcamento completo de
         inimigo, e partir as colunas obrigaria o mestre a juntar duas metades
         de cabeca;
      4. se nem em paisagem couber com 7 pt, volta ao retrato no menor tamanho
         que couber (ate 6 pt), e depois tenta paisagem no mesmo piso;
      5. ultimo recurso: as larguras minimas sao reduzidas na proporcao para
         somar exatamente a faixa util e fica registrado um AVISO. Nesse caso o
         ReportLab quebra palavra no meio (splitLongWords=1): fica apertado, mas
         nao vaza a margem.
    """
    if total_colunas <= 4:
        inicial = 9.0
    elif total_colunas <= 6:
        inicial = 8.5
    elif total_colunas <= 8:
        inicial = 8.0
    elif total_colunas <= 10:
        inicial = 7.5
    else:
        inicial = 7.0

    escada = [t for t in ESCADA_FONTE_TABELA if t <= inicial]

    def tentar(largura, piso):
        for tamanho in escada:
            if tamanho < piso:
                break
            minimos, desejadas = _medir_colunas(matriz, total_colunas, tamanho,
                                                tem_cabecalho)
            larguras = _distribuir_larguras(minimos, desejadas, largura)
            if larguras is not None:
                return tamanho, larguras
        return None

    tem_paisagem = largura_paisagem > largura_retrato + 1

    # 1) retrato, em tamanho confortavel
    resultado = tentar(largura_retrato, FONTE_TABELA_CONFORTAVEL)
    if resultado:
        return resultado[0], resultado[1], False

    # 2) paisagem, em tamanho confortavel
    if tem_paisagem:
        resultado = tentar(largura_paisagem, FONTE_TABELA_CONFORTAVEL)
        if resultado:
            return resultado[0], resultado[1], True

    # 3) retrato, descendo ate o piso
    resultado = tentar(largura_retrato, PISO_FONTE_TABELA)
    if resultado:
        return resultado[0], resultado[1], False

    # 4) paisagem, descendo ate o piso
    if tem_paisagem:
        resultado = tentar(largura_paisagem, PISO_FONTE_TABELA)
        if resultado:
            return resultado[0], resultado[1], True

    # 5) ultimo recurso
    largura_final = largura_paisagem if tem_paisagem else largura_retrato
    minimos, _ = _medir_colunas(matriz, total_colunas, PISO_FONTE_TABELA,
                                tem_cabecalho)
    fator = largura_final / sum(minimos)
    return PISO_FONTE_TABELA, [minimo * fator for minimo in minimos], tem_paisagem


def construir_tabela(linhas_tabela, largura_disponivel, estado):
    """Converte um bloco de tabela GFM nos flowables correspondentes.

    Primeira linha = cabecalho, segunda = separador de alinhamento, demais =
    dados. Devolve a lista de flowables, ja com as quebras de pagina se a tabela
    precisar sair em paisagem.
    """
    cabecalho = dividir_celulas(linhas_tabela[0])
    alinhamentos = ler_alinhamentos(linhas_tabela[1])
    corpo = [dividir_celulas(linha) for linha in linhas_tabela[2:]]

    total_colunas = max([len(cabecalho)] + [len(linha) for linha in corpo])
    if total_colunas < 1:
        return []

    # Tabela de duas colunas no estilo "ficha" vem com cabecalho vazio (`| | |`):
    # nesse caso nao ha faixa de cabecalho nem linha repetida, so pares
    # rotulo/valor.
    tem_cabecalho = any(celula.strip() for celula in cabecalho)
    matriz = ([cabecalho] if tem_cabecalho else []) + corpo
    if not matriz:
        return []

    # Paisagem so e opcao para tabela que esta no fluxo normal do texto: dentro
    # de uma citacao a largura disponivel ja e menor e a tabela fica no lugar.
    no_fluxo_principal = abs(largura_disponivel - LARGURA_UTIL_RETRATO) < 1
    tamanho, larguras, paisagem = escolher_layout_tabela(
        matriz, total_colunas, tem_cabecalho, largura_disponivel,
        LARGURA_UTIL_PAISAGEM if no_fluxo_principal else largura_disponivel,
    )

    # Trava de seguranca: a soma das larguras nunca pode passar da faixa util.
    faixa = LARGURA_UTIL_PAISAGEM if paisagem else largura_disponivel
    soma = sum(larguras)
    if soma > faixa + 0.5:
        fator = faixa / soma
        larguras = [largura * fator for largura in larguras]
        avisar(estado, "tabela mais larga que a pagina foi comprimida "
                       f"(colunas={total_colunas}, soma={soma:.0f}pt, "
                       f"faixa={faixa:.0f}pt)")

    dados = []
    for indice_linha, linha in enumerate(matriz):
        linha_flowables = []
        for coluna in range(total_colunas):
            bruto = linha[coluna] if coluna < len(linha) else ""
            alinhamento = (alinhamentos[coluna]
                           if coluna < len(alinhamentos) else TA_LEFT)
            e_cabecalho = tem_cabecalho and indice_linha == 0
            estilo = estilo_celula(tamanho, alinhamento, e_cabecalho)
            try:
                linha_flowables.append(
                    Paragraph(aplicar_inline(bruto, tamanho), estilo))
            except Exception as erro:
                # Degrada para texto simples: uma celula estranha nao pode
                # derrubar o livro.
                avisar(estado, f"celula de tabela sem formatacao ({erro})")
                linha_flowables.append(
                    Paragraph(escapar(texto_puro(bruto)), estilo))
        dados.append(linha_flowables)

    comandos = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), RECHEIO_TABELA),
        ("RIGHTPADDING", (0, 0), (-1, -1), RECHEIO_TABELA),
        ("TOPPADDING", (0, 0), (-1, -1), 2.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.8),
        ("GRID", (0, 0), (-1, -1), 0.25, COR_GRADE),
        ("BOX", (0, 0), (-1, -1), 0.7, COR_ACENTO_CLARO),
    ]
    if tem_cabecalho:
        comandos += [
            ("BACKGROUND", (0, 0), (-1, 0), COR_ACENTO),
            ("LINEBELOW", (0, 0), (-1, 0), 0.7, COR_ACENTO),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COR_ZEBRA]),
        ]
    else:
        comandos.append(
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, COR_ZEBRA]))

    tabela = Table(
        dados,
        colWidths=larguras,
        repeatRows=1 if tem_cabecalho else 0,   # cabecalho repete na quebra
        style=TableStyle(comandos),
        hAlign="CENTER",
        splitByRow=1,
        splitInRow=1,   # linha mais alta que a pagina ainda consegue dividir
    )

    estado["tabelas"] += 1
    if paisagem:
        estado["tabelas_paisagem"] += 1
        return [
            NextPageTemplate("paisagem"), PageBreak(),
            tabela,
            NextPageTemplate("retrato"), PageBreak(),
        ]
    return [tabela, Spacer(0, 6)]


# ---------------------------------------------------------------------------
# Blocos de Markdown -> flowables
# ---------------------------------------------------------------------------

def proxima_chave(estado):
    """Chave unica de marcador, usada no outline e nos links do sumario."""
    estado["marcadores"] += 1
    return "secao%04d" % estado["marcadores"]


def inserir_titulo(flowables, nivel, texto_md, estado):
    """Titulo de nivel 1, 2 ou 3. O de nivel 1 sempre abre pagina nova."""
    estilos = estado["estilos"]
    puro = texto_puro(texto_md).strip()
    chave = proxima_chave(estado)

    if nivel <= 1:
        # Cada capitulo comeca em pagina nova (requisito do livro). A lista de
        # flowables e a do livro inteiro, por isso basta olhar o ultimo item.
        if flowables and not isinstance(flowables[-1], PageBreak):
            flowables.append(PageBreak())
        estilo = estilos["titulo1"]
        flowables.append(Titulo(aplicar_inline(texto_md, estilo.fontSize), estilo,
                                0, puro, chave, regua=1.6, cor_regua=COR_ACENTO))
    elif nivel == 2:
        # Reserva MINIMA contra titulo orfao no pe da pagina. Depois de montar
        # o livro, `amarrar_titulos_aos_blocos` troca esta altura pela que o
        # bloco seguinte realmente precisa (uma figura pede muito mais que 3 cm).
        flowables.append(ReservaDeEspaco(3.0 * cm, de_titulo=True))
        estilo = estilos["titulo2"]
        flowables.append(Titulo(aplicar_inline(texto_md, estilo.fontSize), estilo,
                                1, puro, chave, regua=0.6, cor_regua=COR_GRADE))
    else:
        flowables.append(ReservaDeEspaco(2.2 * cm, de_titulo=True))
        estilo = estilos["titulo3"]
        flowables.append(Titulo(aplicar_inline(texto_md, estilo.fontSize), estilo,
                                2, puro, chave))


def inserir_paragrafo(flowables, texto, estado, citacao=False):
    """Paragrafo comum ou de citacao (a citacao sai com fundo e barra lateral)."""
    estilos = estado["estilos"]
    estilo = estilos["citacao"] if citacao else estilos["corpo"]
    classe = ParagrafoCitacao if citacao else Paragraph
    try:
        flowables.append(classe(aplicar_inline(texto, estilo.fontSize), estilo))
    except Exception as erro:
        # Degrada para texto simples e segue o baile.
        avisar(estado, f"paragrafo sem formatacao ({erro}): {texto[:60]!r}")
        flowables.append(classe(escapar(texto_puro(texto)), estilo))


def dimensionar_codigo(linhas_codigo, estilo_base, largura_texto, altura_maxima,
                       estado, piso=PISO_FONTE_CODIGO):
    """Escolhe a fonte do bloco de codigo. Devolve (estilo, linhas, altura).

    Duas pressoes: a linha mais longa tem de caber na faixa util e, quando da,
    o bloco inteiro tem de caber de uma vez em `altura_maxima` — as fichas em
    arte ASCII do capitulo 29 so se leem inteiras. O piso de fonte impede que a
    busca por um encaixe deixe a ficha ilegivel.
    """
    referencia = max(stringWidth(linha, FONTE_MONO, 10.0)
                     for linha in linhas_codigo) or 1.0
    tamanho = min(estilo_base.fontSize, 10.0 * largura_texto / referencia)
    total_linhas = len(linhas_codigo)
    if total_linhas * 1.22 * tamanho > altura_maxima and total_linhas <= 90:
        tamanho = min(tamanho, (altura_maxima - 16) / (total_linhas * 1.23))
    tamanho = max(round(tamanho, 2), piso)

    estilo = ParagraphStyle("codigo_%.2f" % tamanho, parent=estilo_base,
                            fontSize=tamanho, leading=tamanho * 1.22)
    largura_caractere = stringWidth("M", FONTE_MONO, tamanho) or 1.0

    # Rede de seguranca: se mesmo no piso uma linha nao couber, ela e cortada em
    # pedacos (nenhum bloco do livro chega nisso hoje, mas o script nao pode
    # vazar a margem se um dia chegar).
    ajustadas = []
    for linha in linhas_codigo:
        if stringWidth(linha, FONTE_MONO, tamanho) <= largura_texto:
            ajustadas.append(linha)
            continue
        maximo = max(10, int(largura_texto / largura_caractere))
        avisar(estado, f"linha de bloco de codigo cortada em {maximo} colunas")
        while len(linha) > maximo:
            ajustadas.append(linha[:maximo])
            linha = linha[maximo:]
        ajustadas.append(linha)

    return estilo, ajustadas, len(ajustadas) * estilo.leading + 16


def inserir_bloco_de_codigo(flowables, linhas_codigo, largura_disponivel, estado):
    """Bloco cercado (```): fonte monoespacada, sem refluir as linhas."""
    if not linhas_codigo:
        return
    estilo_base = estado["estilos"]["codigo"]
    largura_texto = (largura_disponivel - estilo_base.leftIndent
                     - estilo_base.rightIndent - 12)
    estilo, ajustadas, altura_estimada = dimensionar_codigo(
        linhas_codigo, estilo_base, largura_texto, ALTURA_UTIL_RETRATO, estado)

    bloco = BlocoDeCodigo("\n".join(ajustadas), estilo)
    # Guardada para a amarracao do titulo: se este bloco for o primeiro da
    # secao, o titulo so e impresso onde o bloco tambem couber.
    bloco.altura_estimada = altura_estimada

    # Se o bloco cabe inteiro numa pagina, ele nao e partido no meio: as fichas
    # em arte ASCII perdem sentido divididas em duas paginas.
    if altura_estimada <= ALTURA_UTIL_RETRATO:
        flowables.append(ReservaDeEspaco(
            min(altura_estimada, ALTURA_UTIL_RETRATO - 2), de_bloco=True))

    flowables.append(bloco)


def inserir_item_de_lista(flowables, texto, numerado, marcador, nivel, citacao,
                          estado):
    """Item de lista. Listas numeradas preservam o numero escrito no Markdown.

    Mesma decisao do gerar_docx.py: o numero vai literal, porque o livro tem
    dezenas de listas independentes e qualquer numeracao automatica continuaria
    contando de uma lista para a outra.
    """
    estilos = estado["estilos"]
    if citacao:
        estilo = estilos["lista2_citacao"] if nivel else estilos["lista_citacao"]
    else:
        estilo = estilos["lista2"] if nivel else estilos["lista"]

    if numerado:
        marca = f"{marcador}."
    else:
        marca = "\u2013" if nivel else "\u2022"

    try:
        markup = aplicar_inline(texto, estilo.fontSize)
        flowables.append(Paragraph(markup, estilo, bulletText=marca))
    except Exception as erro:
        avisar(estado, f"item de lista sem formatacao ({erro})")
        flowables.append(Paragraph(escapar(texto_puro(texto)), estilo,
                                   bulletText=marca))


def inserir_imagem(flowables, referencia, legenda, largura_disponivel, estado):
    """Imagem referenciada no Markdown, com a legenda logo abaixo."""
    nome_arquivo = os.path.basename(referencia)

    # A capa ja foi usada na pagina de titulo: nao repete.
    if nome_arquivo.lower() == ARQUIVO_CAPA.lower() and estado.get("capa_usada"):
        return

    caminho = os.path.join(DIR_IMAGENS, nome_arquivo)
    if not os.path.isfile(caminho):
        # Fallback: resolve o caminho relativo escrito no .md.
        caminho = os.path.normpath(os.path.join(DIR_CAPITULOS, referencia))

    figura = preparar_imagem(caminho,
                             min(LARGURA_MAX_IMAGEM, largura_disponivel),
                             ALTURA_MAX_IMAGEM, estado)
    if figura is None:
        return

    estado["imagens"] += 1
    paragrafo_legenda = None
    if legenda:
        paragrafo_legenda = Paragraph(escapar(legenda),
                                      estado["estilos"]["legenda"])
    # Figura e legenda andam juntas na mesma pagina, e o grupo encolhe um pouco
    # se for o que falta para ele nao pular de pagina (ver GrupoDeFigura).
    grupo = GrupoDeFigura(figura, paragrafo_legenda)
    grupo.nome = nome_arquivo
    flowables.append(grupo)


def renderizar_blocos(flowables, linhas, estado, citacao=False,
                      largura_disponivel=None):
    """Varre as linhas do Markdown e vai acrescentando flowables em `flowables`.

    Mesma ordem de decisao do gerar_docx.py (linha vazia, cerca de codigo,
    titulo, imagem, regua, tabela, citacao, lista numerada, lista com marcador,
    paragrafo). `citacao=True` e usado na recursao dos blockquotes, de modo que
    uma tabela dentro de um `>` continue virando tabela de verdade.

    A lista e a MESMA do livro inteiro (nao uma por capitulo): e assim que
    `inserir_titulo` consegue olhar o ultimo flowable e decidir se precisa de
    quebra de pagina antes do titulo de capitulo.
    """
    if largura_disponivel is None:
        largura_disponivel = LARGURA_UTIL_RETRATO

    indice = 0
    total = len(linhas)

    while indice < total:
        linha = linhas[indice]
        sem_espacos = linha.strip()

        # 1) Linha vazia: nada a fazer.
        if not sem_espacos:
            indice += 1
            continue

        # 2) Bloco de codigo cercado por ``` ou ~~~.
        if RE_CERCA.match(linha):
            cerca = RE_CERCA.match(linha).group(1)
            indice += 1
            codigo = []
            while indice < total and not linhas[indice].strip().startswith(cerca):
                codigo.append(linhas[indice])
                indice += 1
            indice += 1  # consome a cerca de fechamento
            inserir_bloco_de_codigo(flowables, codigo, largura_disponivel, estado)
            continue

        # 3) Titulos: # -> nivel 1, ## -> nivel 2, ### -> nivel 3.
        casamento_titulo = RE_TITULO.match(sem_espacos)
        if casamento_titulo:
            nivel = min(len(casamento_titulo.group(1)), 3)
            inserir_titulo(flowables, nivel, casamento_titulo.group(2).strip(),
                           estado)
            indice += 1
            continue

        # 4) Imagem em linha propria: ![alt](caminho)
        casamento_imagem = RE_IMAGEM.match(sem_espacos)
        if casamento_imagem:
            legenda = casamento_imagem.group(1).strip()
            referencia = casamento_imagem.group(2).strip().split(" ")[0].strip("<>")
            inserir_imagem(flowables, referencia, legenda, largura_disponivel,
                           estado)
            indice += 1
            continue

        # 5) Regua horizontal (---): e separador visual do Markdown; aqui a
        #    hierarquia de titulos ja separa as secoes, entao ela nao e impressa
        #    (mesma decisao do .docx, para os dois arquivos baterem).
        if RE_REGUA.match(linha):
            indice += 1
            continue

        # 6) Tabela GFM.
        if eh_inicio_de_tabela(linhas, indice):
            bloco = []
            while indice < total and linhas[indice].strip().startswith("|"):
                bloco.append(linhas[indice])
                indice += 1
            try:
                flowables.extend(construir_tabela(bloco, largura_disponivel,
                                                  estado))
            except Exception as erro:
                # Degrada para texto: a tabela sai como linhas, mas sai.
                avisar(estado, f"tabela convertida em texto simples ({erro})")
                for linha_tabela in bloco:
                    if RE_SEPARADOR_TABELA.match(linha_tabela.strip()):
                        continue
                    inserir_paragrafo(flowables,
                                      " · ".join(dividir_celulas(linha_tabela)),
                                      estado, citacao=citacao)
            continue

        # 7) Blockquote: junta as linhas do bloco, tira o '>' e renderiza por
        #    recursao (preserva tabelas e listas dentro da citacao).
        if RE_CITACAO.match(linha):
            internas = []
            while indice < total and (
                RE_CITACAO.match(linhas[indice])
                or (internas and linhas[indice].strip() == "")
            ):
                if linhas[indice].strip() == "":
                    # Linha vazia encerra a citacao se o proximo nao for '>'.
                    if indice + 1 < total and RE_CITACAO.match(linhas[indice + 1]):
                        internas.append("")
                        indice += 1
                        continue
                    break
                internas.append(RE_CITACAO.match(linhas[indice]).group(1))
                indice += 1
            renderizar_blocos(flowables, internas, estado, citacao=True,
                              largura_disponivel=largura_disponivel - 26)
            continue

        # 8) Lista numerada.
        casamento_numero = RE_LISTA_NUMERO.match(linha)
        if casamento_numero:
            recuo = len(casamento_numero.group(1))
            inserir_item_de_lista(flowables, casamento_numero.group(3),
                                  numerado=True,
                                  marcador=casamento_numero.group(2),
                                  nivel=1 if recuo >= 2 else 0,
                                  citacao=citacao, estado=estado)
            indice += 1
            continue

        # 9) Lista com marcador.
        casamento_marcador = RE_LISTA_MARCADOR.match(linha)
        if casamento_marcador:
            recuo = len(casamento_marcador.group(1))
            inserir_item_de_lista(flowables, casamento_marcador.group(2),
                                  numerado=False, marcador=None,
                                  nivel=1 if recuo >= 2 else 0,
                                  citacao=citacao, estado=estado)
            indice += 1
            continue

        # 10) Paragrafo comum: junta as linhas seguidas em um unico paragrafo.
        pedacos = [sem_espacos]
        indice += 1
        while indice < total:
            proxima = linhas[indice]
            if (
                not proxima.strip()
                or RE_TITULO.match(proxima.strip())
                or RE_IMAGEM.match(proxima.strip())
                or RE_REGUA.match(proxima)
                or RE_CERCA.match(proxima)
                or RE_CITACAO.match(proxima)
                or RE_LISTA_MARCADOR.match(proxima)
                or RE_LISTA_NUMERO.match(proxima)
                or proxima.strip().startswith("|")
            ):
                break
            pedacos.append(proxima.strip())
            indice += 1
        inserir_paragrafo(flowables, " ".join(pedacos), estado, citacao=citacao)

    return flowables


def pagina_nova_se_preciso(flowables):
    """Garante uma quebra de pagina sem criar pagina em branco."""
    if flowables and not isinstance(flowables[-1], PageBreak):
        flowables.append(PageBreak())


# ---------------------------------------------------------------------------
# Amarracao do titulo ao bloco que vem depois dele
# ---------------------------------------------------------------------------

# Quanto de prosa o titulo arrasta consigo quando NAO ha bloco alto na frente:
# so as duas primeiras linhas do paragrafo, o bastante para o titulo nunca
# ficar sozinho no pe da pagina.
LINHAS_PRESAS_AO_TITULO = 2.2
# Prosa curta (um paragrafo de abertura) pode ficar entre o titulo e o bloco
# alto da secao e ser levada junto; prosa comprida nao.
PROSA_MAXIMA_ANTES_DO_BLOCO = 4.0 * cm
BLOCOS_DE_PROSA_ANTES_DO_BLOCO = 2
# Teto da amarracao. Se o conjunto titulo + bloco pede quase a pagina inteira,
# amarrar PIORA a pagina anterior: o bloco ia comecar em pagina nova de
# qualquer jeito, e levar o titulo junto so aumenta o vazio que fica atras. E o
# caso das fichas em arte ASCII de 71 linhas, que ocupam uma pagina inteira.
TETO_DA_AMARRACAO = 0.85 * ALTURA_UTIL_RETRATO


def _altura_de(flowable, largura, canv):
    """Altura que o flowable ocupa na coluna, incluindo o espaco que pede antes."""
    _, altura = flowable.wrapOn(canv, largura, 0xfffffff)
    return flowable.getSpaceBefore() + altura


def amarrar_titulos_aos_blocos(historia, estado):
    """Troca a reserva fixa de cada titulo de secao pela altura MEDIDA do bloco.

    O PROBLEMA. `inserir_titulo` reservava 3 cm antes de um H2. Isso basta
    quando o que vem depois e paragrafo, mas a arte de raca e de Caminho e um
    bloco que nao se parte e pede ate 16 cm: o titulo passava no teste dos 3 cm
    e era impresso, a figura nao cabia e pulava de pagina, e o titulo ficava
    sozinho no pe (titulo orfao, com um terco de pagina vazio embaixo).

    O CONSERTO. Depois de o livro inteiro estar montado, cada reserva de titulo
    e recalculada com o que precisa ficar junto do titulo:

      - titulo + figura  -> titulo + a figura no MENOR tamanho que ela aceita
        (ver `GrupoDeFigura.escala_minima`). Se couber, o titulo e impresso e a
        propria figura encolhe para fechar o espaco; se nao couber, titulo e
        figura vao juntos para a pagina seguinte, e a figura sai cheia;
      - titulo + paragrafo de abertura + bloco de codigo -> os tres juntos,
        desde que o conjunto nao passe de `TETO_DA_AMARRACAO`;
      - titulo + paragrafo -> titulo + as duas primeiras linhas do paragrafo,
        que e o minimo contra titulo orfao;
      - titulo + tabela -> a reserva minima de sempre, porque tabela se parte
        entre paginas repetindo o cabecalho, e forcar quebra ali abriria buraco
        em vez de fechar.

    A reserva nunca fica menor que a de antes e nunca passa de
    `TETO_DA_AMARRACAO`: amarrar o titulo a um bloco que ocupa a pagina inteira
    (as fichas em arte ASCII) nao fecharia buraco nenhum, so aumentaria o vazio
    da pagina anterior. Devolve quantos titulos ganharam reserva maior.
    """
    canv = Canvas(io.BytesIO())      # so para medir; nada e escrito nele
    largura = LARGURA_UTIL_RETRATO
    teto = ALTURA_UTIL_RETRATO - 2.0
    amarrados = 0
    recusadas = []

    for indice, item in enumerate(historia):
        if not (isinstance(item, ReservaDeEspaco) and item.de_titulo):
            continue
        titulo = historia[indice + 1] if indice + 1 < len(historia) else None
        if not isinstance(titulo, Titulo):
            continue

        base = item.height
        necessario = _altura_de(titulo, largura, canv) + titulo.getSpaceAfter()

        # Caminha pelos flowables seguintes atras do primeiro bloco alto da
        # secao, atravessando no maximo um ou dois paragrafos curtos.
        prosa = 0.0
        blocos_de_prosa = 0
        extra = 0.0
        posicao = indice + 2
        while posicao < len(historia):
            seguinte = historia[posicao]

            if isinstance(seguinte, ReservaDeEspaco) and seguinte.de_bloco:
                posicao += 1          # a reserva do proprio bloco seguinte
                continue

            if isinstance(seguinte, GrupoDeFigura):
                extra = (seguinte.getSpaceBefore()
                         + seguinte.altura_minima(largura, canv))
                break

            if isinstance(seguinte, BlocoDeCodigo):
                extra = seguinte.getSpaceBefore() + seguinte.altura_estimada
                break

            if (isinstance(seguinte, Paragraph)
                    and not isinstance(seguinte, Titulo)):
                altura = _altura_de(seguinte, largura, canv)
                prosa += altura
                blocos_de_prosa += 1
                if (prosa > PROSA_MAXIMA_ANTES_DO_BLOCO
                        or blocos_de_prosa > BLOCOS_DE_PROSA_ANTES_DO_BLOCO):
                    break
                posicao += 1
                continue

            break                     # tabela, outro titulo, fim do capitulo

        minimo_contra_orfao = (necessario
                               + min(prosa, LINHAS_PRESAS_AO_TITULO
                                     * ENTRELINHA_CORPO))
        amarracao_cheia = necessario + prosa + extra
        if extra > 0 and amarracao_cheia <= TETO_DA_AMARRACAO:
            necessario = amarracao_cheia
        else:
            # Sem bloco alto na frente (ou bloco que toma a pagina inteira):
            # leva so o comeco do paragrafo, que e o minimo contra orfao.
            necessario = minimo_contra_orfao
            if extra > 0:
                recusadas.append(round(amarracao_cheia, 1))

        altura = max(base, min(necessario + 2.0, teto))
        if altura > base + 0.5:
            amarrados += 1
        item.height = altura

    estado["titulos_amarrados"] = amarrados
    estado["amarracoes_recusadas"] = len(recusadas)
    return amarrados


# ---------------------------------------------------------------------------
# Documento: cabecalho, rodape, marcadores e sumario
# ---------------------------------------------------------------------------

def _encurtar(texto, largura_maxima, fonte, tamanho):
    """Corta o texto com reticencias se ele nao couber na largura dada."""
    if stringWidth(texto, fonte, tamanho) <= largura_maxima:
        return texto
    while texto and stringWidth(texto + "\u2026", fonte, tamanho) > largura_maxima:
        texto = texto[:-1]
    return texto.rstrip() + "\u2026"


def desenhar_moldura(canv, doc, com_cabecalho=True, com_folio=True):
    """Cabecalho corrido (livro | capitulo) e numero de pagina.

    Desenhado em `onPageEnd`, ou seja, depois de a pagina ter sido montada:
    assim o nome do capitulo que aparece no alto e sempre o do conteudo que
    esta na propria pagina.

    A pagina de titulo nao leva cabecalho e, por convencao de livro, tambem nao
    leva folio (ver `FOLIO_NA_PAGINA_DE_TITULO`) — ela continua contando na
    sequencia, so nao imprime o numero debaixo da capa.
    """
    largura, altura = canv._pagesize
    margem = MARGEM_LATERAL if largura <= altura else MARGEM_LATERAL_PAISAGEM
    canv.saveState()
    if com_cabecalho:
        canv.setFont(FONTE_TEXTO, 8.2)
        canv.setFillColor(COR_TEXTO_FRACO)
        canv.drawString(margem, altura - 1.52 * cm, TITULO_LIVRO)
        capitulo = getattr(doc, "capitulo_atual", "") or ""
        if capitulo:
            disponivel = (largura - 2 * margem
                          - stringWidth(TITULO_LIVRO, FONTE_TEXTO, 8.2) - 18)
            canv.drawRightString(largura - margem, altura - 1.52 * cm,
                                 _encurtar(capitulo, disponivel, FONTE_TEXTO, 8.2))
        canv.setStrokeColor(COR_GRADE)
        canv.setLineWidth(0.5)
        canv.line(margem, altura - 1.74 * cm, largura - margem, altura - 1.74 * cm)
    if com_folio:
        canv.setFont(FONTE_TEXTO, 9)
        canv.setFillColor(COR_TEXTO_FRACO)
        canv.drawCentredString(largura / 2.0, 1.25 * cm,
                               str(canv.getPageNumber()))
    canv.restoreState()


def criar_modelos_de_pagina():
    """Os tres modelos de pagina: capa, retrato e paisagem.

    O modelo `paisagem` NAO tem `autoNextPageTemplate`: se uma tabela larga
    precisar de mais de uma pagina deitada, ela continua deitada; o retorno ao
    retrato e feito pelo `NextPageTemplate` que acompanha a tabela.
    """
    moldura_capa = Frame(
        MARGEM_LATERAL, MARGEM_INFERIOR,
        LARGURA_UTIL_RETRATO, ALTURA_UTIL_CAPA,
        id="capa", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    moldura_retrato = Frame(
        MARGEM_LATERAL, MARGEM_INFERIOR,
        LARGURA_UTIL_RETRATO, ALTURA_UTIL_RETRATO,
        id="retrato", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    moldura_paisagem = Frame(
        MARGEM_LATERAL_PAISAGEM, MARGEM_INFERIOR,
        LARGURA_UTIL_PAISAGEM, ALTURA_UTIL_PAISAGEM,
        id="paisagem", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    return [
        PageTemplate(id="capa", frames=[moldura_capa], pagesize=PAGINA_RETRATO,
                     onPageEnd=lambda canv, doc: desenhar_moldura(
                         canv, doc, False, FOLIO_NA_PAGINA_DE_TITULO),
                     autoNextPageTemplate="retrato"),
        PageTemplate(id="retrato", frames=[moldura_retrato],
                     pagesize=PAGINA_RETRATO,
                     onPageEnd=lambda canv, doc: desenhar_moldura(canv, doc, True)),
        PageTemplate(id="paisagem", frames=[moldura_paisagem],
                     pagesize=PAGINA_PAISAGEM,
                     onPageEnd=lambda canv, doc: desenhar_moldura(canv, doc, True)),
    ]


class DocumentoLivro(BaseDocTemplate):
    """Documento do livro: registra sumario e marcadores a cada titulo.

    O sumario com paginas de verdade sai das DUAS PASSADAS do `multiBuild`: na
    primeira, cada titulo notifica `TOCEntry` com a pagina onde caiu; na
    segunda, o `TableOfContents` ja sabe os numeros e se imprime com eles.
    """

    def __init__(self, caminho, **kwargs):
        BaseDocTemplate.__init__(self, caminho, **kwargs)
        self.capitulo_atual = ""
        self.total_marcadores = 0
        self._ultimo_nivel = -1

    def beforeDocument(self):
        # multiBuild roda o documento mais de uma vez: o que e por passada
        # precisa ser zerado aqui.
        self.capitulo_atual = ""
        self.total_marcadores = 0
        self._ultimo_nivel = -1
        self.canv.showOutline()   # abre o painel de marcadores no leitor

    def afterFlowable(self, flowable):
        nivel = getattr(flowable, "nivel_titulo", None)
        if nivel is None:
            return
        texto = getattr(flowable, "texto_titulo", "") or ""
        chave = getattr(flowable, "chave_marcador", None)
        if not texto or not chave:
            return

        if nivel == 0:
            self.capitulo_atual = texto

        self.canv.bookmarkPage(chave)
        # O outline do PDF nao aceita pular nivel (um H3 logo apos um H1).
        nivel_outline = min(nivel, self._ultimo_nivel + 1)
        self.canv.addOutlineEntry(texto, chave, level=nivel_outline,
                                  closed=(nivel_outline == 0))
        self._ultimo_nivel = nivel_outline
        self.total_marcadores += 1

        if (nivel <= NIVEL_MAX_SUMARIO
                and not getattr(flowable, "fora_do_sumario", False)):
            self.notify("TOCEntry", (nivel, escapar(texto), self.page, chave))


def montar_pagina_titulo(estado):
    """Pagina de titulo: capa, nome do sistema, subtitulo, autor e versao."""
    estilos = estado["estilos"]
    capa = preparar_imagem(os.path.join(DIR_IMAGENS, ARQUIVO_CAPA),
                           LARGURA_MAX_CAPA, ALTURA_MAX_CAPA, estado)

    # Centraliza o conjunto (capa + titulo + autor) na vertical: o bloco de
    # texto da pagina de titulo mede cerca de 170 pt com estes estilos.
    altura_do_bloco = (capa.drawHeight if capa is not None else 0) + 170
    flowables = [Spacer(0, max(0.4 * cm, (ALTURA_UTIL_CAPA - altura_do_bloco) / 2.0))]

    if capa is not None:
        flowables.append(capa)
        estado["imagens"] += 1
        estado["capa_usada"] = True

    flowables += [
        Paragraph(escapar(TITULO_LIVRO), estilos["capa_titulo"]),
        HRFlowable(width="52%", thickness=1.4, color=COR_ACENTO_CLARO,
                   spaceBefore=2, spaceAfter=9, hAlign="CENTER"),
        Paragraph(escapar(SUBTITULO_LIVRO), estilos["capa_subtitulo"]),
        Paragraph(escapar(AUTOR_LIVRO), estilos["capa_autor"]),
        Paragraph(escapar(VERSAO_LIVRO), estilos["capa_versao"]),
        NextPageTemplate("retrato"),
        PageBreak(),
    ]
    return flowables


def montar_sumario(estado):
    """Sumario de verdade: niveis 1 e 2 com o numero da pagina e link clicavel."""
    estilos = estado["estilos"]
    titulo = Titulo(escapar("Sumário"), estilos["titulo1"], 0, "Sumário",
                    proxima_chave(estado), regua=1.6, cor_regua=COR_ACENTO,
                    fora_do_sumario=True)
    sumario = TableOfContents(
        rightColumnWidth=34,
        levelStyles=[estilos["sumario_nivel0"], estilos["sumario_nivel1"]],
        dotsMinLevel=0,
    )
    return [titulo, sumario, PageBreak()]


# ---------------------------------------------------------------------------
# Captura de avisos (o livro nunca aborta por um aviso, mas ele e registrado)
# ---------------------------------------------------------------------------

class ColetorDeAvisos(logging.Handler):
    """Manda para o relatorio tudo que o ReportLab registrar como aviso."""

    def __init__(self, estado):
        logging.Handler.__init__(self, level=logging.WARNING)
        self.estado = estado

    def emit(self, registro):
        try:
            mensagem = registro.getMessage()
        except Exception:
            mensagem = str(registro.msg)
        avisar(self.estado, f"reportlab[{registro.name}]: {mensagem}")


def instalar_captura_de_avisos(estado):
    """Liga a captura de `logging` e de `warnings` durante a montagem."""
    coletor = ColetorDeAvisos(estado)
    raiz = logging.getLogger()
    if raiz.level > logging.WARNING or raiz.level == logging.NOTSET:
        raiz.setLevel(logging.WARNING)
    raiz.addHandler(coletor)

    warnings.simplefilter("always")

    def mostrar(mensagem, categoria, arquivo, linha, file=None, line=None):
        avisar(estado, f"{categoria.__name__}: {mensagem}")

    warnings.showwarning = mostrar
    return coletor


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    print("Explorando Galáxias — montagem do livro v1.2 em PDF")
    fonte_texto, fonte_mono = registrar_fontes()
    print(f"  raiz do projeto : {DIR_RAIZ}")
    print(f"  capitulos       : {DIR_CAPITULOS}")
    print(f"  imagens         : {DIR_IMAGENS}")
    print(f"  reportlab       : {reportlab.Version}")
    print(f"  fontes          : {fonte_texto} + {fonte_mono}")
    print("")

    estado = {
        "estilos": criar_estilos(),
        "imagens": 0,
        "tabelas": 0,
        "tabelas_paisagem": 0,
        "marcadores": 0,
        "capa_usada": False,
        "titulos_amarrados": 0,
        "amarracoes_recusadas": 0,
        "avisos": [],
    }
    instalar_captura_de_avisos(estado)

    capitulos = listar_capitulos(DIR_CAPITULOS)

    historia = montar_pagina_titulo(estado)
    historia += montar_sumario(estado)

    for numero, caminho in enumerate(capitulos, start=1):
        nome = os.path.basename(caminho)
        print(f"  [{numero:02d}/{len(capitulos)}] {nome}")
        linhas = ler_markdown(caminho)
        # O titulo de nivel 1 ja abre pagina nova; se um capitulo comecar sem
        # titulo, a quebra e forcada aqui para nao emendar com o anterior.
        primeira = next((l.strip() for l in linhas if l.strip()), "")
        if not re.match(r"^#\s+", primeira):
            pagina_nova_se_preciso(historia)
        renderizar_blocos(historia, linhas, estado)

    # Com o livro montado, cada titulo de secao passa a reservar o espaco do
    # bloco que vem depois dele (nada de titulo orfao no pe da pagina).
    amarrar_titulos_aos_blocos(historia, estado)

    documento = DocumentoLivro(
        ARQUIVO_SAIDA,
        pagesize=PAGINA_RETRATO,
        pageTemplates=criar_modelos_de_pagina(),
        title=f"{TITULO_LIVRO} — {VERSAO_LIVRO}",
        author="MC Filhos",
        subject=SUBTITULO_LIVRO,
        creator="build/gerar_pdf.py",
        lang="pt-BR",
        displayDocTitle=1,
    )

    print("")
    print("  montando o PDF (duas passadas, para o sumario sair com as paginas"
          " certas)...")
    try:
        documento.multiBuild(historia)
    except PermissionError:
        raise SystemExit(
            "ERRO: nao foi possivel escrever o PDF. Feche o arquivo no leitor e"
            " rode de novo:\n"
            f"  {ARQUIVO_SAIDA}"
        )

    tamanho_mb = os.path.getsize(ARQUIVO_SAIDA) / (1024 * 1024)
    print("")
    print("Pronto.")
    print(f"  capitulos  : {len(capitulos)}")
    print(f"  paginas    : {documento.page}")
    print(f"  tabelas    : {estado['tabelas']}"
          f" (em paisagem: {estado['tabelas_paisagem']})")
    print(f"  imagens    : {estado['imagens']}")
    print(f"  marcadores : {documento.total_marcadores}")
    print(f"  titulos amarrados ao bloco seguinte: "
          f"{estado['titulos_amarrados']}")
    print(f"  amarracoes recusadas (bloco maior que a pagina): "
          f"{estado['amarracoes_recusadas']}")
    print(f"  avisos     : {len(estado['avisos'])}")

    figuras = [f for f in historia if isinstance(f, GrupoDeFigura)]
    apertadas = [f for f in figuras if f.escala_pedida is not None]
    if apertadas:
        print("")
        print("  Figuras que chegaram ao pe de uma pagina"
              " (pedido / piso / resultado):")
        for figura in apertadas:
            print(f"    - {figura.nome:14s} altura natural"
                  f" {figura.altura_figura/cm:5.2f} cm,"
                  f" pedida {figura.escala_pedida*100:5.1f}%,"
                  f" piso {figura.escala_minima()*100:5.1f}%,"
                  f" {'encolheu para %.1f%%' % (figura.escala * 100) if figura.encolheu else 'foi para a pagina seguinte'}")
    print(f"  arquivo    : {ARQUIVO_SAIDA} ({tamanho_mb:.1f} MB)")
    if estado["avisos"]:
        print("")
        print("  Avisos registrados (nenhum derrubou a montagem):")
        for mensagem in estado["avisos"][:60]:
            print(f"    - {mensagem}")
        if len(estado["avisos"]) > 60:
            print(f"    ... e mais {len(estado['avisos']) - 60}")


if __name__ == "__main__":
    main()
