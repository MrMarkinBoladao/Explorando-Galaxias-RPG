# -*- coding: utf-8 -*-
"""
gerar_docx.py — Script de montagem do livro "Explorando Galáxias" v1.2.

O QUE ELE FAZ
    Le todos os capitulos Markdown de `livro-v1.0/` na ordem do prefixo numerico
    de 2 digitos e monta um unico arquivo .docx com:
      - pagina de titulo (com a imagem de capa image11.png);
      - sumario (campo TOC de verdade do Word);
      - estilos Heading 1/2/3 REAIS do Word (# / ## / ###), para o sumario e o
        painel de navegacao funcionarem;
      - tabelas como OBJETOS TABELA do Word (as tabelas GFM dos .md sao
        parseadas de verdade — na v0.1 elas viravam linhas soltas de texto);
      - imagens posicionadas onde o Markdown as referencia (mapa de imagens do
        documento de design), lidas de `assets/imagens-v01/`.

COMO USAR
    A partir da RAIZ do projeto (a pasta que contem `livro-v1.0/`):

        python "build\\gerar_docx.py"

    Edite os .md quantas vezes quiser e rode de novo: o .docx e regerado por
    inteiro, sobrescrevendo o anterior.

SAIDA
    <raiz do projeto>\\Sistema de HSR by MC Filhos V1.2.docx

REQUISITOS
    Python 3 e python-docx (`python -m pip install python-docx`).

OBSERVACAO SOBRE O SUMARIO
    O Word so calcula as paginas do sumario quando o campo e atualizado. Ao
    abrir o arquivo, o Word costuma perguntar se deve atualizar os campos:
    responda SIM. Se nao perguntar, clique no sumario e pressione F9.
"""

import os
import re
import sys

try:
    import docx
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from docx.shared import Emu, Inches, Pt, Cm
except ImportError:  # pragma: no cover - ambiente sem a dependencia
    print("ERRO: python-docx nao esta instalado. Rode: python -m pip install python-docx")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Configuracao (caminhos e constantes do livro)
# ---------------------------------------------------------------------------

# A raiz do projeto e a pasta ACIMA de build/ — assim o script funciona tanto
# chamado como `python "build\gerar_docx.py"` quanto de dentro de build/.
DIR_BUILD = os.path.dirname(os.path.abspath(__file__))
DIR_RAIZ = os.path.dirname(DIR_BUILD)

DIR_CAPITULOS = os.path.join(DIR_RAIZ, "livro-v1.0")
DIR_IMAGENS = os.path.join(DIR_RAIZ, "assets", "imagens-v01")

# Caminho EXATO do arquivo final pedido pelo autor.
ARQUIVO_SAIDA = os.path.join(DIR_RAIZ, "Sistema de HSR by MC Filhos V1.2.docx")

# Metadados da pagina de titulo.
TITULO_LIVRO = "Explorando Galáxias"
SUBTITULO_LIVRO = "Um sistema de RPG de mesa no universo de Honkai: Star Rail"
AUTOR_LIVRO = "by MC Filhos"
VERSAO_LIVRO = "Versão 1.2"

# Capa: definida no mapa de imagens do design (image11.png, 2048x2048).
ARQUIVO_CAPA = "image11.png"

# Limites de tamanho das imagens dentro da pagina (em polegadas).
LARGURA_MAX_IMAGEM = Inches(4.6)
ALTURA_MAX_IMAGEM = Inches(6.2)
LARGURA_MAX_CAPA = Inches(5.6)
ALTURA_MAX_CAPA = Inches(5.6)


# ---------------------------------------------------------------------------
# Expressoes regulares do parser de Markdown
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


# ---------------------------------------------------------------------------
# Leitura e ordenacao dos capitulos
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
# Formatacao inline (negrito, italico, codigo, links)
# ---------------------------------------------------------------------------

def _novo_run(paragrafo, texto, negrito, italico, codigo):
    """Cria um run com a formatacao pedida, tratando quebras de linha."""
    run = paragrafo.add_run()
    if negrito:
        run.bold = True
    if italico:
        run.italic = True
    if codigo:
        run.font.name = "Consolas"
        run.font.size = Pt(9.5)
    # <br> do GFM e quebras reais dentro de uma celula viram quebra de linha.
    partes = re.split(r"<br\s*/?>|\n", texto)
    for indice, parte in enumerate(partes):
        if indice:
            run.add_break()
        run.add_text(parte)
    return run


def aplicar_inline(paragrafo, texto, negrito=False, italico=False):
    """Escreve `texto` no paragrafo convertendo a marcacao inline do Markdown.

    `negrito` e `italico` servem de base herdada (usado nos cabecalhos de tabela,
    que ja saem em negrito).
    """
    if texto is None:
        return
    for pedaco in RE_INLINE.split(texto):
        if not pedaco:
            continue
        if pedaco.startswith("***") and pedaco.endswith("***") and len(pedaco) > 6:
            _novo_run(paragrafo, pedaco[3:-3], True, True, False)
        elif pedaco.startswith("**") and pedaco.endswith("**") and len(pedaco) > 4:
            _novo_run(paragrafo, pedaco[2:-2], True, italico, False)
        elif pedaco.startswith("__") and pedaco.endswith("__") and len(pedaco) > 4:
            _novo_run(paragrafo, pedaco[2:-2], True, italico, False)
        elif pedaco.startswith("`") and pedaco.endswith("`") and len(pedaco) > 2:
            _novo_run(paragrafo, pedaco[1:-1], negrito, italico, True)
        elif pedaco.startswith("*") and pedaco.endswith("*") and len(pedaco) > 2:
            _novo_run(paragrafo, pedaco[1:-1], negrito, True, False)
        elif pedaco.startswith("_") and pedaco.endswith("_") and len(pedaco) > 2:
            _novo_run(paragrafo, pedaco[1:-1], negrito, True, False)
        elif pedaco.startswith("[") and "](" in pedaco and pedaco.endswith(")"):
            # Links do livro apontam para outros capitulos; mantemos so o rotulo.
            rotulo = pedaco[1:pedaco.index("](")]
            aplicar_inline(paragrafo, rotulo, negrito, italico)
        else:
            _novo_run(paragrafo, pedaco, negrito, italico, False)


# ---------------------------------------------------------------------------
# Peças do documento: estilos, pagina de titulo, sumario
# ---------------------------------------------------------------------------

def preparar_documento():
    """Cria o Document, configura pagina A4, margens e a fonte padrao."""
    documento = Document()

    secao = documento.sections[0]
    secao.page_width = Cm(21.0)      # A4 retrato
    secao.page_height = Cm(29.7)
    secao.left_margin = Cm(2.2)
    secao.right_margin = Cm(2.2)
    secao.top_margin = Cm(2.0)
    secao.bottom_margin = Cm(2.0)

    estilo_normal = documento.styles["Normal"]
    estilo_normal.font.name = "Calibri"
    estilo_normal.font.size = Pt(10.5)
    # Garante a fonte tambem para os scripts de Asia Oriental/complexos, senao o
    # Word pode ignorar o nome escolhido.
    rpr = estilo_normal.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:eastAsia"), "Calibri")
    estilo_normal.paragraph_format.space_after = Pt(6)

    documento.core_properties.title = TITULO_LIVRO
    documento.core_properties.author = "MC Filhos"
    documento.core_properties.comments = "Explorando Galáxias v1.2 — gerado por build/gerar_docx.py"
    return documento


def largura_util(documento):
    """Largura disponivel entre as margens, em EMU."""
    secao = documento.sections[0]
    return secao.page_width - secao.left_margin - secao.right_margin


def inserir_imagem(documento, caminho_imagem, largura_max, altura_max):
    """Insere a imagem centralizada, reduzindo-a para caber nos limites dados.

    python-docx le as dimensoes nativas do PNG, entao nao precisamos de Pillow:
    inserimos, medimos e reescalamos proporcionalmente se passar do limite.
    """
    if not os.path.isfile(caminho_imagem):
        print(f"  AVISO: imagem nao encontrada, ignorada: {caminho_imagem}")
        return None

    paragrafo = documento.add_paragraph()
    paragrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragrafo.add_run()
    figura = run.add_picture(caminho_imagem)

    largura, altura = figura.width, figura.height
    # Nunca passar da largura util da pagina.
    teto_largura = min(int(largura_max), int(largura_util(documento)))

    if largura > teto_largura:
        altura = int(altura * teto_largura / largura)
        largura = teto_largura
    if altura > int(altura_max):
        largura = int(largura * int(altura_max) / altura)
        altura = int(altura_max)

    figura.width = Emu(largura)
    figura.height = Emu(altura)
    return paragrafo


def montar_pagina_titulo(documento):
    """Pagina de titulo: capa, nome do sistema, autor e versao."""
    # Capa (image11.png, conforme o mapa de imagens do design).
    inserir_imagem(
        documento,
        os.path.join(DIR_IMAGENS, ARQUIVO_CAPA),
        LARGURA_MAX_CAPA,
        ALTURA_MAX_CAPA,
    )

    def linha(texto, tamanho, negrito=False, italico=False, espaco_antes=0):
        paragrafo = documento.add_paragraph()
        paragrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragrafo.paragraph_format.space_before = Pt(espaco_antes)
        paragrafo.paragraph_format.space_after = Pt(6)
        run = paragrafo.add_run(texto)
        run.font.size = Pt(tamanho)
        run.bold = negrito
        run.italic = italico
        return paragrafo

    linha(TITULO_LIVRO, 40, negrito=True, espaco_antes=18)
    linha(SUBTITULO_LIVRO, 14, italico=True)
    linha(AUTOR_LIVRO, 16, negrito=True, espaco_antes=18)
    linha(VERSAO_LIVRO, 13)

    quebrar_pagina(documento)


def montar_sumario(documento):
    """Insere o titulo 'Sumário' e um campo TOC nativo do Word (niveis 1-3)."""
    documento.add_heading("Sumário", level=1)

    aviso = documento.add_paragraph()
    aviso.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_aviso = aviso.add_run(
        "Se o Word perguntar se deve atualizar os campos ao abrir, responda Sim. "
        "Para atualizar manualmente: clique no sumário e pressione F9."
    )
    run_aviso.italic = True
    run_aviso.font.size = Pt(9)

    paragrafo = documento.add_paragraph()
    run = paragrafo.add_run()

    # Campo: { TOC \o "1-3" \h \z \u }
    inicio = OxmlElement("w:fldChar")
    inicio.set(qn("w:fldCharType"), "begin")
    inicio.set(qn("w:dirty"), "true")   # faz o Word recalcular na abertura

    instrucao = OxmlElement("w:instrText")
    instrucao.set(qn("xml:space"), "preserve")
    instrucao.text = r'TOC \o "1-3" \h \z \u'

    separador = OxmlElement("w:fldChar")
    separador.set(qn("w:fldCharType"), "separate")

    # Texto exibido enquanto o campo nao for atualizado.
    texto_provisorio = OxmlElement("w:t")
    texto_provisorio.text = "O sumário será montado quando os campos forem atualizados (F9)."

    fim = OxmlElement("w:fldChar")
    fim.set(qn("w:fldCharType"), "end")

    run._r.append(inicio)
    run._r.append(instrucao)
    run._r.append(separador)
    run._r.append(texto_provisorio)
    run._r.append(fim)

    quebrar_pagina(documento)


def quebrar_pagina(documento):
    """Adiciona uma quebra de pagina."""
    paragrafo = documento.add_paragraph()
    paragrafo.add_run().add_break(WD_BREAK.PAGE)


# ---------------------------------------------------------------------------
# Tabelas GFM -> tabelas de verdade do Word
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
            alinhamentos.append(WD_ALIGN_PARAGRAPH.CENTER)
        elif direita:
            alinhamentos.append(WD_ALIGN_PARAGRAPH.RIGHT)
        else:
            alinhamentos.append(WD_ALIGN_PARAGRAPH.LEFT)
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


def inserir_tabela(documento, linhas_tabela):
    """Cria uma tabela do Word a partir das linhas GFM coletadas.

    Primeira linha = cabecalho (negrito e repetido no topo de cada pagina),
    segunda linha = separador de alinhamento, demais = dados.
    """
    cabecalho = dividir_celulas(linhas_tabela[0])
    alinhamentos = ler_alinhamentos(linhas_tabela[1])
    corpo = [dividir_celulas(linha) for linha in linhas_tabela[2:]]

    # A tabela usa a maior largura encontrada; linhas curtas sao completadas com
    # celulas vazias, para o Word nunca receber uma linha torta.
    total_colunas = max([len(cabecalho)] + [len(linha) for linha in corpo])
    if total_colunas < 1:
        return

    tabela = documento.add_table(rows=1, cols=total_colunas)
    # 'Table Grid' existe no template padrao do python-docx e desenha as bordas.
    try:
        tabela.style = documento.styles["Table Grid"]
    except KeyError:
        pass
    tabela.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabela.autofit = True

    def preencher(celulas_word, valores, negrito):
        for coluna in range(total_colunas):
            texto = valores[coluna] if coluna < len(valores) else ""
            celula = celulas_word[coluna]
            paragrafo = celula.paragraphs[0]
            paragrafo.paragraph_format.space_before = Pt(2)
            paragrafo.paragraph_format.space_after = Pt(2)
            if coluna < len(alinhamentos):
                paragrafo.alignment = alinhamentos[coluna]
            aplicar_inline(paragrafo, texto, negrito=negrito)
            if negrito:
                for run in paragrafo.runs:
                    run.bold = True

    preencher(tabela.rows[0].cells, cabecalho, negrito=True)
    marcar_linha_de_cabecalho(tabela.rows[0])

    for valores in corpo:
        preencher(tabela.add_row().cells, valores, negrito=False)

    # Respiro depois da tabela, para o texto seguinte nao colar nela.
    documento.add_paragraph().paragraph_format.space_after = Pt(4)


def marcar_linha_de_cabecalho(linha):
    """Marca a linha como cabecalho (repete no topo de cada pagina impressa)."""
    propriedades = linha._tr.get_or_add_trPr()
    repetir = OxmlElement("w:tblHeader")
    repetir.set(qn("w:val"), "true")
    propriedades.append(repetir)


# ---------------------------------------------------------------------------
# Renderizacao dos blocos de Markdown
# ---------------------------------------------------------------------------

def estilo_existe(documento, nome):
    """Checa se um estilo existe no template, para nunca estourar KeyError."""
    try:
        documento.styles[nome]
        return True
    except KeyError:
        return False


def inserir_paragrafo(documento, texto, estilo=None, citacao=False):
    """Paragrafo comum (ou de citacao, com o estilo 'Quote' do Word)."""
    nome_estilo = estilo
    if citacao and nome_estilo is None:
        nome_estilo = "Quote" if estilo_existe(documento, "Quote") else None

    paragrafo = documento.add_paragraph(style=nome_estilo)
    if citacao and nome_estilo is None:
        # Sem o estilo 'Quote' no template, simula a citacao com recuo + italico.
        paragrafo.paragraph_format.left_indent = Cm(1.0)
    aplicar_inline(paragrafo, texto)
    return paragrafo


def inserir_bloco_de_codigo(documento, linhas_codigo):
    """Bloco cercado (```) vira um paragrafo monoespacado, preservando as linhas."""
    estilo = "No Spacing" if estilo_existe(documento, "No Spacing") else None
    paragrafo = documento.add_paragraph(style=estilo)
    formato = paragrafo.paragraph_format
    formato.left_indent = Cm(0.6)
    formato.space_before = Pt(6)
    formato.space_after = Pt(6)
    run = paragrafo.add_run()
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    for indice, linha in enumerate(linhas_codigo):
        if indice:
            run.add_break()
        run.add_text(linha)
    return paragrafo


def inserir_item_de_lista(documento, texto, numerado, marcador, nivel, citacao):
    """Item de lista. Listas numeradas preservam o numero escrito no Markdown.

    Por que o numero vai no texto: o estilo 'List Number' do Word numera de forma
    continua ao longo do documento inteiro, e o livro tem dezenas de listas
    independentes — a numeracao do autor sairia errada. Com o numero literal, o
    que esta no .md e o que aparece no .docx.
    """
    if numerado:
        estilo = "List Paragraph" if estilo_existe(documento, "List Paragraph") else None
        paragrafo = documento.add_paragraph(style=estilo)
        paragrafo.paragraph_format.left_indent = Cm(0.75 + 0.6 * nivel)
        run = paragrafo.add_run(f"{marcador}. ")
        run.bold = True
        aplicar_inline(paragrafo, texto)
    else:
        nome = "List Bullet 2" if nivel else "List Bullet"
        if not estilo_existe(documento, nome):
            nome = "List Bullet" if estilo_existe(documento, "List Bullet") else None
        paragrafo = documento.add_paragraph(style=nome)
        if nome is None:
            paragrafo.paragraph_format.left_indent = Cm(0.75 + 0.6 * nivel)
            aplicar_inline(paragrafo, "• " + texto)
            return paragrafo
        aplicar_inline(paragrafo, texto)

    if citacao:
        paragrafo.paragraph_format.left_indent = Cm(1.6 + 0.6 * nivel)
    return paragrafo


def renderizar_blocos(documento, linhas, estado, citacao=False):
    """Varre as linhas do Markdown e escreve os blocos no documento.

    `estado` guarda o que atravessa arquivos (ex.: imagens ja usadas, para a capa
    nao sair duas vezes). `citacao=True` e usado na recursao dos blockquotes, de
    modo que uma tabela dentro de um `>` continue virando tabela de verdade.
    """
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
            inserir_bloco_de_codigo(documento, codigo)
            continue

        # 3) Titulos: # -> Heading 1, ## -> Heading 2, ### -> Heading 3.
        casamento_titulo = RE_TITULO.match(sem_espacos)
        if casamento_titulo:
            nivel = min(len(casamento_titulo.group(1)), 3)
            texto = casamento_titulo.group(2).strip()
            titulo = documento.add_heading(level=nivel)
            # add_heading ja cria o run; usamos o paragrafo vazio e aplicamos a
            # formatacao inline (ha titulos com ** e * no livro).
            aplicar_inline(titulo, texto)
            indice += 1
            continue

        # 4) Imagem em linha propria: ![alt](caminho)
        casamento_imagem = RE_IMAGEM.match(sem_espacos)
        if casamento_imagem:
            legenda = casamento_imagem.group(1).strip()
            referencia = casamento_imagem.group(2).strip().split(" ")[0].strip("<>")
            nome_arquivo = os.path.basename(referencia)

            # A capa ja foi usada na pagina de titulo: nao repete.
            if nome_arquivo.lower() == ARQUIVO_CAPA.lower() and estado.get("capa_usada"):
                indice += 1
                continue

            caminho = os.path.join(DIR_IMAGENS, nome_arquivo)
            if not os.path.isfile(caminho):
                # Fallback: resolve o caminho relativo escrito no .md.
                caminho = os.path.normpath(os.path.join(DIR_CAPITULOS, referencia))

            if inserir_imagem(documento, caminho, LARGURA_MAX_IMAGEM, ALTURA_MAX_IMAGEM):
                estado["imagens"] += 1
                if legenda:
                    paragrafo = documento.add_paragraph()
                    paragrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = paragrafo.add_run(legenda)
                    run.italic = True
                    run.font.size = Pt(9)
            indice += 1
            continue

        # 5) Regua horizontal (---): e separador visual do Markdown; no .docx a
        #    hierarquia de titulos ja separa as secoes, entao ela nao e impressa.
        if RE_REGUA.match(linha):
            indice += 1
            continue

        # 6) Tabela GFM.
        if eh_inicio_de_tabela(linhas, indice):
            bloco = []
            while indice < total and linhas[indice].strip().startswith("|"):
                bloco.append(linhas[indice])
                indice += 1
            inserir_tabela(documento, bloco)
            estado["tabelas"] += 1
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
            renderizar_blocos(documento, internas, estado, citacao=True)
            continue

        # 8) Lista numerada.
        casamento_numero = RE_LISTA_NUMERO.match(linha)
        if casamento_numero:
            recuo = len(casamento_numero.group(1))
            inserir_item_de_lista(
                documento,
                casamento_numero.group(3),
                numerado=True,
                marcador=casamento_numero.group(2),
                nivel=1 if recuo >= 2 else 0,
                citacao=citacao,
            )
            indice += 1
            continue

        # 9) Lista com marcador.
        casamento_marcador = RE_LISTA_MARCADOR.match(linha)
        if casamento_marcador:
            recuo = len(casamento_marcador.group(1))
            inserir_item_de_lista(
                documento,
                casamento_marcador.group(2),
                numerado=False,
                marcador=None,
                nivel=1 if recuo >= 2 else 0,
                citacao=citacao,
            )
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
        inserir_paragrafo(documento, " ".join(pedacos), citacao=citacao)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    print("Explorando Galáxias — montagem do livro v1.2")
    print(f"  raiz do projeto : {DIR_RAIZ}")
    print(f"  capitulos       : {DIR_CAPITULOS}")
    print(f"  imagens         : {DIR_IMAGENS}")
    print(f"  python-docx     : {docx.__version__}")
    print("")

    capitulos = listar_capitulos(DIR_CAPITULOS)
    documento = preparar_documento()

    # Pagina de titulo (com a capa) e sumario.
    montar_pagina_titulo(documento)
    estado = {"imagens": 1, "tabelas": 0, "capa_usada": True}
    montar_sumario(documento)

    # Capitulos, na ordem do prefixo numerico.
    for numero, caminho in enumerate(capitulos, start=1):
        nome = os.path.basename(caminho)
        print(f"  [{numero:02d}/{len(capitulos)}] {nome}")
        if numero > 1:
            quebrar_pagina(documento)   # cada capitulo comeca em pagina nova
        renderizar_blocos(documento, ler_markdown(caminho), estado)

    try:
        documento.save(ARQUIVO_SAIDA)
    except PermissionError:
        raise SystemExit(
            "ERRO: nao foi possivel escrever o .docx. Feche o arquivo no Word e rode de novo:\n"
            f"  {ARQUIVO_SAIDA}"
        )

    tamanho_mb = os.path.getsize(ARQUIVO_SAIDA) / (1024 * 1024)
    print("")
    print("Pronto.")
    print(f"  capitulos : {len(capitulos)}")
    print(f"  tabelas   : {estado['tabelas']}")
    print(f"  imagens   : {estado['imagens']}")
    print(f"  arquivo   : {ARQUIVO_SAIDA} ({tamanho_mb:.1f} MB)")
    print("")
    print("Lembrete: ao abrir no Word, aceite atualizar os campos (ou pressione F9 no sumário)")
    print("para o sumário ser preenchido com os títulos e as páginas.")


if __name__ == "__main__":
    main()
