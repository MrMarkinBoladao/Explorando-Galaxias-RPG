# -*- coding: utf-8 -*-
"""
gerar_site.py — Gera os dados do site (ficha online + livro de consulta).

O QUE ELE FAZ
    Lê os capítulos de `livro-v1.0/` (a fonte de verdade das regras) e as
    tabelas que `build/ficha_dados.py` já sabe extrair deles, e grava:

      site/dados/livro.js     o livro inteiro, dividido em blocos por título
                              (é o que a aba Regras mostra e pesquisa)
      site/dados/catalogo.js  Raças, Caminhos, Bênçãos, condições, armas...
                              (é o que a ficha usa nas listas e nos textos)
      site/img/               as imagens do livro, em versão leve para a web

    Os dados vão em arquivos .js (e não .json) para o site funcionar também
    abrindo o index.html direto do computador, sem servidor.

    Os números das fórmulas (PV, Defesa, dano...) moram em site/js/motor.js,
    que é uma tradução do build/oraculo_ficha.py para JavaScript.

COMO USAR (na pasta raiz do projeto)
    python site/gerar_site.py

    Rode de novo sempre que mudar algum capítulo do livro. No GitHub, o site
    publicado roda este script sozinho a cada envio (.github/workflows/site.yml).
"""

import json
import re
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
LIVRO = RAIZ / "livro-v1.0"
DADOS = AQUI / "dados"
IMG = AQUI / "img"
LARGURA_IMG = 900

sys.path.insert(0, str(RAIZ / "build"))
import ficha_dados as fd  # noqa: E402  (precisa do sys.path acima)

RE_TITULO = re.compile(r"^(#{1,3}) +(.+?)\s*$")
RE_IMAGEM = re.compile(r"\]\(\.\./assets/imagens-v01/([^)]+)\)")


# ---------------------------------------------------------------------------
# Livro
# ---------------------------------------------------------------------------

def limpar_titulo(t):
    return re.sub(r"[*`]", "", t).strip()


def blocos_do_capitulo(texto):
    """Divide o capítulo nos títulos de nível 1 a 3 (fora de bloco de código e de
    citação). Cada bloco leva o próprio título e o texto até o próximo título."""
    blocos, atual, cerca = [], None, False
    for linha in texto.splitlines():
        if linha.lstrip().startswith("```"):
            cerca = not cerca
        m = None if cerca else RE_TITULO.match(linha)
        if m:
            atual = {"nivel": len(m.group(1)), "titulo": limpar_titulo(m.group(2)), "linhas": [linha]}
            blocos.append(atual)
            continue
        if atual is None:
            atual = {"nivel": 1, "titulo": "", "linhas": []}
            blocos.append(atual)
        atual["linhas"].append(linha)

    saida, pai = [], ""
    for i, b in enumerate(blocos):
        linhas = b["linhas"]
        # o "---" entre seções é só separador visual do livro
        while linhas and linhas[-1].strip() in ("", "---"):
            linhas.pop()
        if b["nivel"] <= 2:
            pai = b["titulo"]
        saida.append({
            "id": "s%d" % i,
            "nivel": b["nivel"],
            "titulo": b["titulo"],
            "pai": pai if b["nivel"] == 3 else "",
            "md": "\n".join(linhas),
        })
    return saida


def imagem_web(nome):
    """Caminho (relativo ao site) da versão web da imagem `nome` do livro."""
    origem = RAIZ / "assets" / "imagens-v01" / nome
    IMG.mkdir(exist_ok=True)
    pronta = sorted(IMG.glob(Path(nome).stem + ".*"))
    if pronta:
        return "img/" + pronta[0].name
    if not origem.exists():
        print("  aviso: imagem não encontrada:", origem)
        return "../assets/imagens-v01/" + nome
    try:
        from PIL import Image
        with Image.open(origem) as im:
            if im.width > LARGURA_IMG:
                im = im.resize((LARGURA_IMG, round(im.height * LARGURA_IMG / im.width)))
            destino = IMG / (origem.stem + ".webp")
            im.save(destino, "WEBP", quality=80, method=6)
    except ImportError:
        # sem Pillow, vai a imagem original (mais pesada, mas funciona)
        destino = IMG / origem.name
        shutil.copyfile(origem, destino)
    return "img/" + destino.name


def versao_do_livro():
    capa = next(LIVRO.glob("00-capa*.md")).read_text(encoding="utf-8")
    m = re.search(r"\*\*Versão ([\d.]+)\*\*", capa)
    return m.group(1) if m else "?"


def livro():
    capitulos = []
    for arq in sorted(LIVRO.glob("*.md")):
        if arq.name.startswith("00-changelog"):
            continue                       # histórico de versões não é regra
        texto = arq.read_text(encoding="utf-8")
        texto = RE_IMAGEM.sub(lambda m: "](" + imagem_web(m.group(1)) + ")", texto)
        blocos = blocos_do_capitulo(texto)
        titulo = next((b["titulo"] for b in blocos if b["nivel"] == 1 and b["titulo"]), arq.stem)
        m = re.match(r"Capítulo (\d+)\s*[—-]\s*(.+)", titulo)
        capitulos.append({
            "id": arq.stem,
            "num": m.group(1) if m else arq.stem[:2],
            "titulo": m.group(2) if m else titulo,
            "blocos": blocos,
        })
    return {"versao": versao_do_livro(), "capitulos": capitulos}


# ---------------------------------------------------------------------------
# Catálogo da ficha (tudo vem do parser de build/ficha_dados.py)
# ---------------------------------------------------------------------------

def tabela_do_riso():
    _, corpo = fd.tabela("13", "## 13.2", "d6")
    return [{"d6": fd.num(l[0]), "efeito": l[1]} for l in corpo]


def mesa_do_mestre():
    """As tabelas que a Área do Mestre usa: âncoras de inimigo (28.3), orçamento de
    encontro (27.4), DTs (27.2, 27.3, 20.2), Tenacidade (20.3), Atraso (19.4) e
    recompensas (27.8)."""
    cab, dt = fd.dt_faixa()
    return {
        "ancoras": fd.ancoras_inimigo(),
        "orcamento": fd.orcamento_encontro(),
        "composicoes": fd.composicoes_encontro(),
        "acoes_tipo": fd.acoes_por_tipo(),
        "fraquezas_tipo": fd.fraquezas_por_tipo(),
        "atraso_tipo": fd.atraso_por_tipo(),
        "dt_faixa": {"faixas": cab[1:], "linhas": [{"dificuldade": l[0], "dt": l[1:]} for l in dt]},
        "dt_subsistema": fd.dt_subsistema(),
        "dt_fraqueza": fd.dt_fraqueza(),
        "fraqueza_resistencia": fd.fraqueza_resistencia(),
        "reducao_tenacidade": fd.tenacidade(),
        "recompensas": fd.recompensas_calendario(),
        "equipamento_faixa": fd.equipamento_por_faixa(),
        "verba": fd.verba(),
    }


def catalogo():
    recurso = {x["caminho"]: x["recurso"] for x in fd.TRANSCRITO["recurso_proprio"]}
    caminhos = fd.caminhos()
    for c in caminhos:
        c["recurso"] = recurso[c["caminho"]]
    sem_ancora = lambda itens: [{k: v for k, v in i.items() if k not in ("ancora", "cap")} for i in itens]
    acumulos = sem_ancora(fd.TRANSCRITO["acumulos"])
    # 09: "Recurso próprio | Nenhum além dos acúmulos das Bênçãos: Eco da Vitória (até 3)"
    acumulos.append({"caminho": "A Harmonia", "bencao": "Eco da Vitória",
                     "recurso": "Eco da Vitória", "maximo": 3})
    return {
        "versao": versao_do_livro(),
        "racas": fd.racas(),
        "caminhos": caminhos,
        "bencaos": fd.bencaos(),
        "acumulos": acumulos,
        "pericias": fd.pericias(),
        "testes_resistencia": fd.testes_resistencia(),
        "condicoes": fd.condicoes(),
        "elementos": fd.elementos(),
        "armas": fd.armas(),
        "armaduras": fd.armaduras(),
        "propriedades": fd.propriedades(),
        "pocoes": fd.pocoes(),
        "itens": fd.itens(),
        "buff_debuff": fd.buff_debuff(),
        "passivas": fd.passivas(),
        "energia": fd.energia(),
        "tabela_do_riso": tabela_do_riso(),
        "bestiario": fd.bestiario(),
        "mestre": mesa_do_mestre(),
        "memo": {
            "conceitos": [{"nome": a, "texto": b} for a, b in fd.memo_tabela("Conceito")],
            "funcoes": [{"nome": a, "texto": b} for a, b in fd.memo_tabela("Função")],
            "bonus_menores": [{"nome": a, "texto": b} for a, b in fd.memo_tabela("Bônus menor")],
            "evolucoes": [{"nome": a, "texto": b} for a, b in fd.memo_tabela("Evolução")],
        },
        "listas": {k: v["valores"] for k, v in fd.TRANSCRITO["listas"].items()},
    }


# ---------------------------------------------------------------------------

def gravar(nome, variavel, dados):
    DADOS.mkdir(exist_ok=True)
    corpo = json.dumps(dados, ensure_ascii=False, separators=(",", ":"))
    texto = ("// Gerado por site/gerar_site.py a partir de livro-v1.0/. Não edite à mão.\n"
             "window.%s = %s;\n" % (variavel, corpo))
    (DADOS / nome).write_text(texto, encoding="utf-8")
    print("  %-14s %6.0f KB" % (nome, len(texto.encode("utf-8")) / 1024))


def main():
    print("Gerando o site a partir de", LIVRO)
    L = livro()
    gravar("livro.js", "LIVRO", L)
    gravar("catalogo.js", "CATALOGO", catalogo())
    n = sum(len(c["blocos"]) for c in L["capitulos"])
    print("  %d capítulos, %d blocos de regra · livro v%s" % (len(L["capitulos"]), n, L["versao"]))


if __name__ == "__main__":
    main()
