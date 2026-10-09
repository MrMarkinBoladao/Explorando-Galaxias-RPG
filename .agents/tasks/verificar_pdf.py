# -*- coding: utf-8 -*-
"""
verificar_pdf.py — Conferencia do livro gerado por build/gerar_pdf.py.

O que ele faz, nesta ordem:
  1. abre o PDF com pypdf e relata paginas, marcadores, metadados e tamanho;
  2. conta as imagens embutidas (XObjects de imagem) pagina por pagina;
  3. procura conteudo fora das margens (tabela estourada ou texto cortado),
     comparando a caixa de cada bloco de texto e de cada vetor desenhado com a
     MOLDURA DE TEXTO de verdade (2,4 cm no topo, 2,2 cm nos outros tres
     lados), e nao com uma faixa folgada;
  4. confere cada imagem: se a caixa dela cabe na moldura e se a proporcao na
     pagina e a mesma do arquivo de origem (imagem esticada);
  5. confere se o sumario mostra numeros de pagina de verdade, comparando a
     pagina impressa no sumario com a pagina onde o titulo realmente esta;
  6. confere se os marcadores do outline levam ao capitulo certo e se os links
     do sumario apontam para paginas que existem;
  7. rasteriza as paginas pedidas em .agents/tasks/pdf-paginas/ para inspecao
     visual.

Uso (a partir da raiz do projeto):
    python ".agents\\tasks\\verificar_pdf.py"
"""

import os
import re
import sys

import fitz          # pymupdf
from pypdf import PdfReader

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDF = os.path.join(RAIZ, "Sistema de HSR by MC Filhos V1.0.pdf")
PASTA_PAGINAS = os.path.join(RAIZ, ".agents", "tasks", "pdf-paginas")

CM = 28.3465

# A moldura de texto do livro, igual a de build/gerar_pdf.py.
MARGEM_RETRATO = 2.2 * CM
MARGEM_PAISAGEM = 2.0 * CM
MARGEM_TOPO = 2.4 * CM
MARGEM_PE = 2.2 * CM

# O cabecalho corrido (regua em 1,74 cm do topo) e o numero de pagina (1,25 cm
# do pe) sao desenhados de proposito FORA da moldura de texto. Um bloco que
# vive inteiro dentro de uma dessas duas faixas nao e estouro de margem.
BANDA_CABECALHO = 1.95 * CM
BANDA_RODAPE = 1.6 * CM

# Vetor e geometria exata: meio ponto de folga ja pega qualquer fundo de
# citacao ou grade de tabela vazando. A caixa que o pymupdf devolve para um
# bloco de TEXTO justificado inclui a sobra lateral do glifo, que chega a ~0,3
# pt sem haver tinta fora da margem — por isso o texto usa 1 pt.
TOLERANCIA_VETOR = 0.5
TOLERANCIA_TEXTO = 1.0

# Desvio maximo aceito entre a proporcao da imagem na pagina e a do arquivo.
DESVIO_PROPORCAO = 1.0           # em %

# Vazio no pe da pagina que conta como buraco. Cinco centimetros e mais ou
# menos um quinto da moldura de texto: abaixo disso o olho le como respiro de
# fim de secao, acima disso le como pagina inacabada.
LIMITE_BURACO = 5.0 * CM


def contar_imagens(leitor):
    """Conta as imagens embutidas, por pagina e no total (sem repetir XObject)."""
    total = 0
    por_pagina = []
    nomes = set()
    for numero, pagina in enumerate(leitor.pages, start=1):
        try:
            imagens = pagina.images
        except Exception:
            imagens = []
        if imagens:
            por_pagina.append((numero, len(imagens)))
            total += len(imagens)
            for imagem in imagens:
                nomes.add((numero, imagem.name))
    return total, por_pagina, nomes


def listar_marcadores(leitor):
    """Devolve (quantidade, profundidade maxima, primeiros marcadores)."""
    quantidade = 0
    profundidade = 0
    amostra = []

    def andar(itens, nivel):
        nonlocal quantidade, profundidade
        profundidade = max(profundidade, nivel + 1)
        for item in itens:
            if isinstance(item, list):
                andar(item, nivel + 1)
                continue
            quantidade += 1
            if len(amostra) < 12:
                amostra.append((nivel, str(item.title)))

    try:
        andar(leitor.outline, 0)
    except Exception as erro:
        print(f"  ERRO ao ler o outline: {erro}")
    return quantidade, profundidade, amostra


def conferir_margens(documento):
    """Procura texto ou vetor fora da moldura de texto.

    A conferencia e feita contra a moldura de verdade (2,4 cm no topo, 2,2 cm
    nos outros lados), tirando da conta so o cabecalho corrido e o numero de
    pagina, que sao desenhados fora dela de proposito.
    """
    problemas = []
    for indice, pagina in enumerate(documento, start=1):
        largura, altura = pagina.rect.width, pagina.rect.height
        margem = MARGEM_RETRATO if largura <= altura else MARGEM_PAISAGEM

        caixas = []
        for bloco in pagina.get_text("blocks"):
            if not str(bloco[4]).strip():
                continue
            caixas.append(("texto", bloco[:4], TOLERANCIA_TEXTO,
                           str(bloco[4])[:48].replace("\n", " ")))
        for desenho in pagina.get_drawings():
            caixa = desenho["rect"]
            caixas.append(("vetor", (caixa.x0, caixa.y0, caixa.x1, caixa.y1),
                           TOLERANCIA_VETOR, str(desenho.get("fill"))))

        for tipo, (x0, y0, x1, y1), folga, amostra in caixas:
            if x1 - x0 <= 0 or y1 - y0 < 0:
                continue
            # Cabecalho e rodape: ficam fora da moldura por desenho do livro.
            if y1 < BANDA_CABECALHO or y0 > altura - BANDA_RODAPE:
                continue
            fora = []
            if margem - x0 > folga:
                fora.append(f"esquerda {x0:.1f} < {margem:.1f}")
            if x1 - (largura - margem) > folga:
                fora.append(f"direita {x1:.1f} > {largura - margem:.1f}")
            if MARGEM_TOPO - y0 > folga:
                fora.append(f"topo {y0:.1f} < {MARGEM_TOPO:.1f}")
            if y1 - (altura - MARGEM_PE) > folga:
                fora.append(f"pe {y1:.1f} > {altura - MARGEM_PE:.1f}")
            if fora:
                problemas.append((indice, tipo, "; ".join(fora), amostra))
    return problemas


def conferir_imagens(documento):
    """Confere caixa e proporcao de cada imagem desenhada.

    Duas perguntas: a imagem cabe na moldura de texto e a proporcao dela na
    pagina e a mesma do arquivo de origem (ou seja, ela nao foi esticada)?
    """
    linhas = []
    problemas = []
    for indice, pagina in enumerate(documento, start=1):
        largura, altura = pagina.rect.width, pagina.rect.height
        margem = MARGEM_RETRATO if largura <= altura else MARGEM_PAISAGEM
        for info in pagina.get_image_info(xrefs=True):
            caixa = fitz.Rect(info["bbox"])
            if caixa.height <= 0 or info["height"] <= 0:
                continue
            proporcao_origem = info["width"] / info["height"]
            proporcao_pagina = caixa.width / caixa.height
            desvio = abs(proporcao_pagina - proporcao_origem) / proporcao_origem * 100
            fora = []
            if margem - caixa.x0 > TOLERANCIA_VETOR:
                fora.append("passa a esquerda")
            if caixa.x1 - (largura - margem) > TOLERANCIA_VETOR:
                fora.append("passa a direita")
            if MARGEM_TOPO - caixa.y0 > TOLERANCIA_VETOR:
                fora.append("passa o topo")
            if caixa.y1 - (altura - MARGEM_PE) > TOLERANCIA_VETOR:
                fora.append("passa o pe")
            if desvio > DESVIO_PROPORCAO:
                fora.append(f"esticada ({desvio:.1f}%)")
            linhas.append((indice, info["width"], info["height"],
                           caixa.width, caixa.height, desvio,
                           "; ".join(fora) or "ok"))
            if fora:
                problemas.append((indice, "; ".join(fora)))
    return linhas, problemas


def conferir_links(documento):
    """Confere os links internos (as entradas clicaveis do sumario)."""
    total = 0
    quebrados = []
    paginas_com_link = set()
    for indice in range(documento.page_count):
        for link in documento[indice].get_links():
            total += 1
            paginas_com_link.add(indice + 1)
            destino = link.get("page", -1)
            if link["kind"] != fitz.LINK_GOTO or not (
                    0 <= destino < documento.page_count):
                quebrados.append((indice + 1, link.get("kind")))
    return total, quebrados, sorted(paginas_com_link)


def menores_fontes(documento, quantas=5):
    """Os menores tamanhos de fonte do livro, para conferir o piso de 6 pt."""
    tamanhos = {}
    for indice in range(documento.page_count):
        for bloco in documento[indice].get_text("dict")["blocks"]:
            for linha in bloco.get("lines", []):
                for trecho in linha["spans"]:
                    tamanho = round(trecho["size"], 1)
                    if tamanho not in tamanhos:
                        tamanhos[tamanho] = (indice + 1, trecho["text"][:24])
    return [(t, ) + tamanhos[t] for t in sorted(tamanhos)[:quantas]]


def paginas_quase_vazias(documento):
    """Paginas com cabecalho e rodape e quase mais nada (quebra sobrando)."""
    suspeitas = []
    for indice, pagina in enumerate(documento, start=1):
        altura = pagina.rect.height
        caracteres = 0
        for bloco in pagina.get_text("blocks"):
            if bloco[1] < 50 or bloco[1] > altura - 40:
                continue      # cabecalho corrido e numero de pagina
            caracteres += len(bloco[4].strip())
        if caracteres < 40 and not pagina.get_images():
            suspeitas.append((indice, caracteres))
    return suspeitas


def paginas_de_capitulo(documento):
    """Paginas em que um capitulo (titulo de nivel 1 do outline) abre."""
    return {pagina for nivel, _, pagina in documento.get_toc(simple=True)
            if nivel == 1}


def paginas_de_secao(documento):
    """Paginas em que uma secao (titulo de nivel 2) abre."""
    return {pagina for nivel, _, pagina in documento.get_toc(simple=True)
            if nivel == 2}


def vazio_no_pe(documento):
    """Mede, pagina por pagina, o vazio entre o ultimo conteudo e o pe.

    E a medida que faltava na conferencia: margem em ordem e sumario certo nao
    dizem nada sobre um terco de pagina em branco no meio de um capitulo, que e
    o que acontece quando um bloco que nao se parte (figura, ficha em arte
    ASCII) nao cabe no que restou e pula de pagina.

    A conta e contra a moldura de texto de verdade (pe em 2,2 cm), somando
    texto, vetores e imagens e tirando da conta as faixas do cabecalho corrido
    e do numero de pagina. Devolve uma lista de dicionarios, um por pagina, com
    o vazio em pontos e a classificacao:

      `fim de capitulo`  — a pagina seguinte abre capitulo novo, ou e a ultima
                           do livro: capitulo acaba onde acaba, vazio normal;
      `meio de capitulo` — a pagina seguinte continua o mesmo capitulo: vazio
                           grande aqui e defeito de paginacao.
    """
    capitulos = paginas_de_capitulo(documento)
    secoes = paginas_de_secao(documento)
    medidas = []
    for indice, pagina in enumerate(documento, start=1):
        altura = pagina.rect.height
        pe_da_moldura = altura - MARGEM_PE
        ultimo = MARGEM_TOPO          # nada impresso: vazio = moldura inteira

        caixas = [bloco[:4] for bloco in pagina.get_text("blocks")
                  if str(bloco[4]).strip()]
        caixas += [(d["rect"].x0, d["rect"].y0, d["rect"].x1, d["rect"].y1)
                   for d in pagina.get_drawings()]
        caixas += [tuple(info["bbox"]) for info in pagina.get_image_info()]
        for _, y0, _, y1 in caixas:
            if y1 < BANDA_CABECALHO or y0 > altura - BANDA_RODAPE:
                continue              # cabecalho corrido e folio
            ultimo = max(ultimo, min(y1, pe_da_moldura))

        seguinte = indice + 1
        fim_de_capitulo = (seguinte > documento.page_count
                           or seguinte in capitulos)
        medidas.append({
            "pagina": indice,
            "vazio": max(0.0, pe_da_moldura - ultimo),
            "fim_de_capitulo": fim_de_capitulo,
            "abre_secao_depois": seguinte in secoes,
        })
    return medidas


def buracos_no_meio(medidas, limite=5.0 * CM):
    """So os vazios grandes que caem no meio de um capitulo (os defeitos)."""
    return [m for m in medidas
            if not m["fim_de_capitulo"] and m["vazio"] > limite]


def titulos_orfaos(documento, tamanho_minimo=12.0):
    """Paginas que terminam com um TITULO como ultimo elemento impresso.

    Titulo orfao: o H2 (15 pt) ou H3 (12 pt) e a ultima coisa da pagina e o
    corpo da secao comeca na pagina seguinte. O filtro e o tamanho da fonte —
    corpo tem 10,5 pt, legenda 9 pt, celula de tabela no maximo 9 pt — mais o
    negrito, que todo titulo do livro tem.
    """
    orfaos = []
    for indice, pagina in enumerate(documento, start=1):
        altura = pagina.rect.height
        ultimo = None
        for bloco in pagina.get_text("dict")["blocks"]:
            for linha in bloco.get("lines", []):
                for trecho in linha["spans"]:
                    if not trecho["text"].strip():
                        continue
                    y1 = trecho["bbox"][3]
                    if y1 < BANDA_CABECALHO or trecho["bbox"][1] > altura - BANDA_RODAPE:
                        continue
                    if ultimo is None or y1 > ultimo[0]:
                        ultimo = (y1, trecho)
        if ultimo is None:
            continue
        trecho = ultimo[1]
        negrito = "bold" in trecho["font"].lower()
        if trecho["size"] >= tamanho_minimo and negrito:
            orfaos.append((indice, round(trecho["size"], 1),
                           trecho["text"][:46]))
    return orfaos


def achar_pagina(documento, trecho, inicio=0):
    """Numero (1-based) da primeira pagina que contem o trecho, ou None."""
    for indice in range(inicio, documento.page_count):
        if trecho in documento[indice].get_text():
            return indice + 1
    return None


def pagina_do_marcador(documento, titulo):
    """Pagina do marcador com este titulo exato (a pagina em que ele esta)."""
    for _, texto, pagina in documento.get_toc(simple=True):
        if texto.strip() == titulo:
            return pagina
    return None


def paginas_do_sumario(documento):
    """Faixa de paginas ocupada pelo sumario, lida do proprio outline."""
    toc = documento.get_toc(simple=True)
    inicio = next((p for n, t, p in toc if t.strip() == "Sumário"), 2)
    seguintes = [p for n, t, p in toc if n == 1 and p > inicio]
    fim = (min(seguintes) - 1) if seguintes else inicio
    return list(range(inicio, fim + 1))


def entradas_impressas(documento, paginas):
    """Le o sumario por coordenada: [(rotulo, numero de pagina impresso)].

    O numero de pagina do sumario e desenhado em outro objeto de texto (e o
    ReportLab que preenche os pontinhos), por isso a leitura e feita agrupando
    as palavras pela mesma linha e tomando a ultima palavra, que e o numero.
    """
    entradas = []
    for numero in paginas:
        pagina = documento[numero - 1]
        linhas = {}
        for palavra in pagina.get_text("words"):
            linhas.setdefault(round(palavra[1] / 3.0), []).append(palavra)
        for chave in sorted(linhas):
            palavras = sorted(linhas[chave], key=lambda p: p[0])
            if len(palavras) < 3 or not palavras[-1][4].isdigit():
                continue    # linha de cabecalho/rodape, nao entrada de sumario
            rotulo = " ".join(p[4] for p in palavras[:-1])
            rotulo = re.sub(r"[\s.]+$", "", rotulo).strip()
            if rotulo:
                entradas.append((" ".join(rotulo.split()),
                                 int(palavras[-1][4])))
    return entradas


def conferir_sumario(documento):
    """Compara, na ordem, cada numero impresso no sumario com o do marcador.

    A comparacao e por ORDEM, nao por titulo: o livro tem titulos repetidos
    ("Resumo do capitulo" aparece em quase todo capitulo) e comparar por nome
    daria falso negativo.
    """
    paginas = paginas_do_sumario(documento)
    impressas = entradas_impressas(documento, paginas)
    esperadas = [(" ".join(titulo.split()), pagina)
                 for nivel, titulo, pagina in documento.get_toc(simple=True)
                 if nivel <= 2 and titulo.strip() != "Sumário"]

    iguais, divergentes = [], []
    for (rotulo, numero), (titulo, pagina) in zip(impressas, esperadas):
        mesmo_titulo = titulo.startswith(rotulo[:28]) or rotulo.startswith(titulo[:28])
        if numero == pagina and mesmo_titulo:
            iguais.append((rotulo, numero, pagina))
        else:
            divergentes.append((rotulo, numero, f"{titulo[:40]} p.{pagina}"))
    sobras = abs(len(impressas) - len(esperadas))
    return paginas, iguais, divergentes, sobras


def conferir_outline(documento, quantos=8):
    """Confere se o destino de cada marcador cai na pagina do proprio titulo."""
    saida = []
    toc = documento.get_toc(simple=True)
    passo = max(1, len(toc) // quantos)
    for nivel, titulo, pagina in toc[::passo][:quantos]:
        if pagina < 1 or pagina > documento.page_count:
            saida.append((nivel, titulo, pagina, "pagina invalida"))
            continue
        texto = documento[pagina - 1].get_text().replace("\n", " ")
        alvo = " ".join(titulo.split())
        saida.append((nivel, titulo, pagina,
                      "ok" if alvo[:40] in texto else "titulo nao encontrado"))
    return saida


COR_FUNDO_CITACAO = (0.9568629860877991, 0.9529410004615784, 0.9803919792175293)


def paginas_de_borda_de_citacao(documento):
    """Acha a citacao que abre uma pagina e a que fecha uma pagina.

    Sao os dois casos em que o fundo da citacao chega rente a moldura — os que
    antes levavam a tinta para dentro da margem. Devolve (pagina do topo,
    pagina do pe) para a inspecao visual mirar neles.
    """
    melhor_topo = (1e9, None)
    melhor_pe = (1e9, None)
    for indice in range(documento.page_count):
        pagina = documento[indice]
        altura = pagina.rect.height
        for desenho in pagina.get_drawings():
            cor = desenho.get("fill")
            if cor is None or max(abs(a - b) for a, b in
                                  zip(cor, COR_FUNDO_CITACAO)) > 0.01:
                continue
            caixa = desenho["rect"]
            if caixa.width < 100:      # a barra lateral, nao o fundo
                continue
            distancia_topo = abs(caixa.y0 - MARGEM_TOPO)
            distancia_pe = abs((altura - MARGEM_PE) - caixa.y1)
            if distancia_topo < melhor_topo[0]:
                melhor_topo = (distancia_topo, indice + 1)
            if distancia_pe < melhor_pe[0]:
                melhor_pe = (distancia_pe, indice + 1)
    return melhor_topo[1], melhor_pe[1]


def rasterizar(documento, pedidos, zoom=1.6):
    """Salva as paginas pedidas como PNG para inspecao visual."""
    os.makedirs(PASTA_PAGINAS, exist_ok=True)
    matriz = fitz.Matrix(zoom, zoom)
    salvos = []
    for nome, numero in pedidos:
        if not numero or numero < 1 or numero > documento.page_count:
            print(f"  AVISO: pagina de '{nome}' nao encontrada ({numero})")
            continue
        pagina = documento[numero - 1]
        pixmap = pagina.get_pixmap(matrix=matriz)
        destino = os.path.join(PASTA_PAGINAS, f"{nome}.png")
        pixmap.save(destino)
        salvos.append((nome, numero, destino, pixmap.width, pixmap.height))
    return salvos


def main():
    if not os.path.isfile(PDF):
        raise SystemExit(f"ERRO: PDF nao encontrado: {PDF}")

    tamanho = os.path.getsize(PDF)
    print("=" * 78)
    print("CONFERENCIA DO PDF")
    print("=" * 78)
    print(f"arquivo : {PDF}")
    print(f"tamanho : {tamanho/1024/1024:.2f} MB ({tamanho} bytes)")

    leitor = PdfReader(PDF)
    print(f"paginas : {len(leitor.pages)}")
    print(f"titulo  : {leitor.metadata.get('/Title')}")
    print(f"autor   : {leitor.metadata.get('/Author')}")

    quantidade, profundidade, amostra = listar_marcadores(leitor)
    print(f"outline : {quantidade} marcadores, profundidade {profundidade}")
    for nivel, titulo in amostra:
        print(f"          {'  ' * nivel}- {titulo}")

    total_imagens, por_pagina, _ = contar_imagens(leitor)
    print(f"imagens : {total_imagens} embutidas em {len(por_pagina)} paginas")
    print(f"          paginas com imagem: {[p for p, _ in por_pagina]}")

    documento = fitz.open(PDF)

    print("")
    print(f"-- conteudo fora da moldura de texto (topo {MARGEM_TOPO:.1f}pt,"
          f" lados {MARGEM_RETRATO:.1f}pt, pe {MARGEM_PE:.1f}pt;"
          f" folga vetor {TOLERANCIA_VETOR}pt / texto {TOLERANCIA_TEXTO}pt) --")
    problemas = conferir_margens(documento)
    if not problemas:
        print("nenhum: todo texto e todo vetor estao dentro da moldura")
    else:
        print(f"{len(problemas)} ocorrencia(s):")
        for pagina, tipo, detalhe, trecho in problemas[:40]:
            print(f"  pagina {pagina:4d} {tipo:6s} {detalhe} | {trecho}")
        if len(problemas) > 40:
            print(f"  ... e mais {len(problemas) - 40}")

    print("")
    print("-- imagens: caixa na moldura e proporcao do arquivo de origem --")
    linhas_imagem, problemas_imagem = conferir_imagens(documento)
    for (pagina, px_l, px_a, pt_l, pt_a, desvio, estado) in linhas_imagem:
        print(f"  pagina {pagina:4d} {px_l:5d}x{px_a:<5d}px ->"
              f" {pt_l:6.1f}x{pt_a:6.1f}pt  desvio de proporcao"
              f" {desvio:4.2f}%  {estado}")
    print(f"  {len(linhas_imagem)} imagem(ns), {len(problemas_imagem)}"
          f" com problema")

    print("")
    print("-- links internos (sumario clicavel) --")
    total_links, links_quebrados, paginas_com_link = conferir_links(documento)
    print(f"{total_links} link(ns) interno(s), {len(links_quebrados)} quebrado(s)")
    print(f"  paginas que tem link: {paginas_com_link}")

    print("")
    print("-- menores tamanhos de fonte (piso de 6 pt nas tabelas) --")
    for tamanho, pagina, amostra in menores_fontes(documento):
        print(f"  {tamanho:5.1f} pt  1a ocorrencia p{pagina:<4d} {amostra!r}")

    print("")
    print("-- paginas quase vazias --")
    vazias = paginas_quase_vazias(documento)
    if not vazias:
        print("nenhuma: toda pagina tem conteudo")
    else:
        print(f"{len(vazias)}: {vazias}")

    print("")
    print(f"-- vazio no pe da pagina (limite de {LIMITE_BURACO/CM:.0f} cm,"
          f" moldura de texto com pe em {MARGEM_PE/CM:.1f} cm) --")
    medidas = vazio_no_pe(documento)
    buracos = buracos_no_meio(medidas, LIMITE_BURACO)
    fins = [m for m in medidas
            if m["fim_de_capitulo"] and m["vazio"] > LIMITE_BURACO]
    if not buracos:
        print("nenhum buraco no MEIO de capitulo")
    else:
        print(f"{len(buracos)} pagina(s) com buraco no MEIO de capitulo:")
        for medida in buracos:
            marca = ("(a pagina seguinte abre secao)"
                     if medida["abre_secao_depois"] else "")
            print(f"  pagina {medida['pagina']:4d}  {medida['vazio']/CM:5.1f} cm"
                  f"  {marca}")
    print(f"{len(fins)} pagina(s) com vazio no FIM de capitulo (normal):"
          f" {[m['pagina'] for m in fins]}")
    maior = max(medidas, key=lambda m: m["vazio"] if not m["fim_de_capitulo"]
                else -1)
    print(f"maior vazio no meio de capitulo: pagina {maior['pagina']}"
          f" com {maior['vazio']/CM:.1f} cm")

    print("")
    print("-- titulo orfao (pagina que termina com um titulo) --")
    orfaos = titulos_orfaos(documento)
    if not orfaos:
        print("nenhum: nenhuma pagina termina com titulo")
    else:
        for pagina, tamanho, texto in orfaos:
            print(f"  pagina {pagina:4d} {tamanho:4.1f} pt  {texto!r}")

    print("")
    print("-- aberturas de capitulo (titulo de nivel 1 do outline) --")
    aberturas = sorted(paginas_de_capitulo(documento))
    print(f"{len(aberturas)} paginas: {aberturas}")

    print("")
    print("-- sumario com paginas reais --")
    paginas_sumario, iguais, divergentes, sobras = conferir_sumario(documento)
    print(f"paginas do sumario : {paginas_sumario[0]} a {paginas_sumario[-1]}")
    print(f"entradas conferidas: {len(iguais)} com a pagina certa, "
          f"{len(divergentes)} divergentes, diferenca de contagem: {sobras}")
    for rotulo, impresso, esperado in divergentes[:10]:
        print(f"  DIVERGE {rotulo[:50]:52s} sumario={impresso} | {esperado}")
    for rotulo, impresso, _ in iguais[:4] + iguais[-4:]:
        print(f"  ok      {rotulo[:50]:52s} pagina {impresso}")

    # Paginas de interesse, localizadas pelo texto depois do sumario.
    depois = paginas_sumario[-1]
    pagina_bestiario = achar_pagina(documento, "Capítulo 28", depois)
    pagina_ancoras = achar_pagina(documento, "Âncoras", depois)
    pagina_destruicao = achar_pagina(documento, "7.1 A ficha do Caminho", depois)
    pagina_ficha = achar_pagina(documento, "FICHA DE PERSONAGEM", depois)
    pagina_texto = achar_pagina(documento, "18.1", depois)
    pagina_fichas15 = achar_pagina(documento, "Fichas de inimigo de referência",
                                   depois)
    pagina_progressao = achar_pagina(documento, "A tabela mestra", depois)
    citacao_topo, citacao_pe = paginas_de_borda_de_citacao(documento)

    print("")
    print("-- marcadores apontando para o lugar certo --")
    for nivel, titulo, pagina, estado in conferir_outline(documento):
        print(f"  nivel {nivel} pagina {pagina:4d} {estado:24s} {titulo[:50]}")

    print("")
    print("-- paginas rasterizadas --")
    pedidos = [
        ("titulo", 1),
        ("sumario", paginas_sumario[0] if paginas_sumario else 2),
        ("sumario-2", paginas_sumario[1] if len(paginas_sumario) > 1 else None),
        ("tabela-bestiario-13-colunas", pagina_ancoras),
        ("tabela-fichas-12-colunas", pagina_fichas15),
        ("caminho-ficha", pagina_destruicao),
        ("texto", pagina_texto),
        ("ficha-ascii", pagina_ficha),
        ("tabela-progressao", pagina_progressao),
        ("tabela-progressao-continuacao",
         pagina_progressao + 1 if pagina_progressao else None),
        ("bestiario-abertura", pagina_bestiario),
        # As duas bordas em que o fundo da citacao chega rente a moldura.
        ("citacao-no-topo-da-pagina", citacao_topo),
        ("citacao-no-pe-da-pagina", citacao_pe),
    ]
    # As aberturas de Caminho (as duas artes na mesma pagina, sem buraco), a
    # secao de raca cujo titulo ficava orfao, e o que sobrou de buraco no meio
    # de capitulo.
    pedidos += [
        ("caminho-abertura", achar_pagina(documento, "Capítulo 07", depois)),
        ("caminho-abertura-2", achar_pagina(documento, "Capítulo 09", depois)),
        # A secao de raca cujo titulo ficava orfao no pe da pagina: a pagina
        # vem do proprio marcador, que e exatamente onde o titulo esta.
        ("raca-titulo-com-arte", pagina_do_marcador(documento, "Vulpes")),
    ]
    for ordem, medida in enumerate(buracos[:4], start=1):
        pedidos.append((f"buraco-{ordem}-p{medida['pagina']:03d}",
                        medida["pagina"]))
    for nome, numero, destino, largura, altura in rasterizar(documento, pedidos):
        print(f"  {nome:28s} pagina {numero:4d} -> {os.path.basename(destino)}"
              f" ({largura}x{altura}px)")

    documento.close()
    print("")
    print("=" * 78)


if __name__ == "__main__":
    main()
