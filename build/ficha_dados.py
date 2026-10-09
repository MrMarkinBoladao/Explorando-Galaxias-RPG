# -*- coding: utf-8 -*-
"""
ficha_dados.py — Camada de dados da Ficha de Personagem automatizada
("Explorando Galáxias" v1.2).

O QUE ELE FAZ
    Lê os capítulos .md de `livro-v1.0/` (fonte de verdade, somente leitura; o
    nome da pasta é histórico, o conteúdo é a v1.2 — 00-changelog-v11-para-v12) e
    devolve as tabelas que a aba Dados da planilha usa: Raças, Perícias, Testes
    de Resistência, Caminhos, PV, as 108 Bênçãos, armas, armaduras, poções,
    itens, Cone de Luz, Relíquias, Ressonâncias, tabela mestra, Habilidades,
    Buff/Debuff/Passivas, Ultimate, PH, Energia, Tenacidade, Dano de Quebra,
    condições, DTs e Memoespírito.

    Duas camadas, de propósito:
      1. PARSER — tudo que é tabela ou estrutura fixa do livro é lido do .md na
         hora de gerar (tabela markdown "| a | b |" com linha "|---|"; Bênçãos
         por "### N. Nome" + linha "**Tier …**" + tabela "Resumo do capítulo";
         frequência da Bênção = expressões "uma vez por …" do corpo do Efeito,
         fora das citações).
      2. MÓDULO TRANSCRITO (`TRANSCRITO`) — só o que é interpretação: acúmulos
         por Bênção, efeitos automáticos (decisão 2 do plano), recurso próprio
         por Caminho, vantagens raciais e listas de validação que o livro
         escreve em prosa. CADA item tem `ancora` = trecho literal do capítulo
         citado em `cap`; a suíte `dados` de `build/testar_ficha.py` confere que
         a âncora existe no .md.

    Não escreve nada: é importado por `build/gerar_ficha.py`.

COMO USAR
    $env:PYTHONUTF8="1"; python "build\\ficha_dados.py"     (imprime um resumo)
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LIVRO = RAIZ / "livro-v1.0"

ATRIBUTOS = ["Poder", "Agilidade", "Vigor", "Sincronia", "Discernimento", "Presença"]
CAMINHOS_CAPITULO = [("07", "A Destruição"), ("08", "A Inexistência"), ("09", "A Harmonia"),
                     ("10", "A Abundância"), ("11", "A Recordação"), ("12", "A Erudição"),
                     ("13", "A Euforia"), ("14", "A Caça"), ("15", "A Preservação")]


# ---------------------------------------------------------------------------
# Leitura e utilitários de markdown
# ---------------------------------------------------------------------------

_cache = {}


def capitulo(prefixo):
    """Linhas do capítulo cujo arquivo começa com `prefixo` (ex.: '05')."""
    if prefixo not in _cache:
        arq = sorted(LIVRO.glob(f"{prefixo}-*.md"))[0]
        _cache[prefixo] = arq.read_text(encoding="utf-8").splitlines()
    return _cache[prefixo]


def texto_capitulo(prefixo):
    return "\n".join(capitulo(prefixo))


def limpar(celula):
    """Tira marcação markdown (negrito, itálico, código) e espaços extras."""
    s = celula.replace("**", "").replace("`", "")
    s = re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"\1", s)
    s = s.replace("\\|", "|")
    return re.sub(r"\s+", " ", s).strip()


def secao(prefixo, titulo):
    """Linhas da seção cujo cabeçalho começa com `titulo` (ex.: '## 4.4'),
    até o próximo cabeçalho de mesmo nível ou superior."""
    linhas = capitulo(prefixo)
    nivel = len(titulo) - len(titulo.lstrip("#"))
    ini = None
    for i, l in enumerate(linhas):
        if ini is None:
            if l.startswith(titulo):
                ini = i
        else:
            m = re.match(r"^(#+) ", l)
            if m and len(m.group(1)) <= nivel:
                return linhas[ini:i]
    if ini is None:
        raise ValueError(f"seção '{titulo}' não encontrada no capítulo {prefixo}")
    return linhas[ini:]


def tabelas(linhas):
    """Todas as tabelas markdown de `linhas`: lista de (cabecalho, linhas).
    Aceita tabela dentro de citação ('> | a | b |')."""
    saida = []
    i = 0
    while i < len(linhas):
        l = linhas[i].lstrip("> ").rstrip()
        prox = linhas[i + 1].lstrip("> ").rstrip() if i + 1 < len(linhas) else ""
        if l.startswith("|") and re.match(r"^\|(\s*:?-{3,}:?\s*\|)+$", prox):
            cab = _celulas(l)
            corpo = []
            j = i + 2
            while j < len(linhas) and linhas[j].lstrip("> ").startswith("|"):
                corpo.append(_celulas(linhas[j].lstrip("> ").rstrip()))
                j += 1
            saida.append((cab, corpo))
            i = j
        else:
            i += 1
    return saida


def _celulas(linha):
    linha = linha.strip()
    if linha.startswith("|"):
        linha = linha[1:]
    if linha.endswith("|"):
        linha = linha[:-1]
    return [limpar(p) for p in re.split(r"(?<!\\)\|", linha)]


def tabela(prefixo, titulo_secao, primeira_coluna):
    """A tabela da seção cujo cabeçalho começa por `primeira_coluna`."""
    for cab, corpo in tabelas(secao(prefixo, titulo_secao)):
        if cab and cab[0].startswith(primeira_coluna):
            return cab, corpo
    raise ValueError(f"tabela '{primeira_coluna}' não achada em {prefixo} {titulo_secao}")


def num(s):
    """'+3' -> 3; '-1' -> -1; '1.200 Cr' -> 1200; '0,5' -> 0.5; '—' -> None."""
    s = limpar(str(s)).replace("Cr", "").strip()
    if s in ("—", "-", ""):
        return None
    if re.match(r"^[+-]?\d{1,3}(\.\d{3})+$", s):
        s = s.replace(".", "")
    s = s.replace(",", ".")
    m = re.match(r"^[+-]?\d+(\.\d+)?", s)
    if not m:
        return None
    v = float(m.group(0))
    return int(v) if v.is_integer() else v


def dados(s):
    """'6d20' -> (6, 20)."""
    m = re.search(r"(\d+)d(\d+)", s)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def atributos_em(texto):
    """Atributos citados em `texto`, na ordem em que aparecem."""
    achados = [(texto.find(a), a) for a in ATRIBUTOS if texto.find(a) >= 0]
    return [a for _, a in sorted(achados)]


# ---------------------------------------------------------------------------
# Extratores por capítulo
# ---------------------------------------------------------------------------

def racas():
    _, corpo = tabela("05", "## Tabela de consulta rápida", "Raça")
    textos = _textos_tracos()
    saida = []
    for lin in corpo:
        nome, bonus, tracos = lin[0], lin[1], lin[2]
        opcoes = atributos_em(bonus)
        livre = not opcoes
        saida.append({
            "raca": nome, "bonus": bonus, "livre": livre,
            "opcao1": opcoes[0] if opcoes else "",
            "opcao2": opcoes[1] if len(opcoes) > 1 else "",
            "tracos": tracos, "texto_tracos": textos.get(nome, ""),
        })
    return saida


_NOTAS_TRACO = ("> **O que mudou", "> **Converse", "> **A Execução", "> **O Esforço")


def _textos_tracos():
    """Texto inteiro dos traços de cada Raça ('### Traço — Nome' em diante),
    sem as notas editoriais ('O que mudou', etc.)."""
    saida, raca, dentro, nota = {}, None, False, False
    for l in capitulo("05"):
        if l.startswith("## "):
            raca, dentro = l[3:].strip(), False
            continue
        if l.startswith("### Traço"):
            dentro, nota = True, False
            saida.setdefault(raca, []).append(l.split("—", 1)[1].strip() + ":")
            continue
        if l.startswith("### ") or l.strip() == "---":
            dentro = False
            continue
        if not dentro:
            continue
        if l.startswith(_NOTAS_TRACO):
            nota = True
        if nota:
            if not l.strip():
                nota = False
            continue
        t = limpar(l.lstrip("> ").strip())
        if not t:
            continue
        if t.startswith("- "):
            t = "• " + t[2:]
        saida[raca].append(t)
    return {k: " ".join(v) for k, v in saida.items()}


def pericias():
    saida, atual, bloco = [], None, []

    def fecha():
        for _, corpo in tabelas(bloco):
            for lin in corpo:
                nome = re.sub(r"\s*\(.*\)$", "", lin[0]).strip()
                saida.append({"pericia": nome, "atributo": atual, "resolve": lin[1]})

    for l in secao("04", "## 4.4"):
        if l.startswith("### "):
            fecha()
            bloco = []
            m = re.match(r"^### Perícias? de (\w+)$", l)
            atual = m.group(1) if m else "Discernimento ou Sincronia"
        else:
            bloco.append(l)
    fecha()
    return saida


def testes_resistencia():
    _, corpo = tabela("04", "## 4.6", "Teste de Resistência")
    return [{"tr": l[0], "atributo": l[1]} for l in corpo]


def caminhos():
    _, aeons = tabela("06", "## 6.2", "Caminho")
    _, colunas = tabela("06", "## 6.3", "Caminho")
    frase = {l[0]: (l[1], l[2]) for l in aeons}
    saida = []
    for l in colunas:
        nome = l[0]
        attrs = atributos_em(l[1])
        per = [p.strip() for p in l[2].split(",")]
        saida.append({
            "caminho": nome, "aeon": frase[nome][0], "ideia": frase[nome][1],
            "atributo_habilidade": l[1], "attr1": attrs[0],
            "attr2": attrs[1] if len(attrs) > 1 else "",
            "pericia1": per[0], "pericia2": per[1], "pericia3": per[2],
            "n": num(l[3]), "vel": num(l[4]),
        })
    return saida


def tabela_pv():
    cab, corpo = tabela("06", "## 6.4", "Nível")
    return cab, [[num(c) for c in l] for l in corpo]


_RE_FREQ = re.compile(
    r"\b(?:uma|1) vez por (?:turno|Ciclo|combate|Descanso Longo|Descanso Curto|cena|sessão|dia)"
    r"(?: por alvo)?|\b(?:duas|2) vezes por (?:dia|combate|Ciclo|Descanso Longo)",
    re.IGNORECASE)


def frequencias(linhas_corpo):
    """Frequências declaradas no corpo da Bênção, fora das citações (> …)."""
    achadas = []
    for l in linhas_corpo:
        if l.lstrip().startswith(">"):
            continue
        for m in _RE_FREQ.finditer(limpar(l)):
            f = m.group(0)
            f = re.sub(r"^1 vez", "uma vez", f, flags=re.IGNORECASE)
            f = re.sub(r"^2 vezes", "duas vezes", f, flags=re.IGNORECASE)
            f = f[0].upper() + f[1:]
            if f.lower() not in [a.lower() for a in achadas]:
                achadas.append(f)
    return achadas


def bencaos():
    """As 108 Bênçãos, 12 por Caminho, na ordem dos capítulos 07 a 15."""
    saida = []
    for cap, caminho in CAMINHOS_CAPITULO:
        linhas = capitulo(cap)
        _, resumo = tabela(cap, "## Resumo do capítulo", "#")
        resumo_por_n = {int(l[0]): l[3] for l in resumo if l[0].isdigit()}
        i = 0
        while i < len(linhas):
            m = re.match(r"^### (\d+)\. (.+?)\s*$", linhas[i])
            if not m:
                i += 1
                continue
            n, nome = int(m.group(1)), m.group(2).strip()
            linha_tier = linhas[i + 1]
            mt = re.match(r"^\*\*Tier (I{1,3}) — (?:sem requisito de nível|requisito: nível (\d+))\*\*",
                          linha_tier)
            if not mt:
                raise ValueError(f"linha de Tier inesperada em {cap} #{n}: {linha_tier!r}")
            j = i + 2
            corpo = []
            while j < len(linhas) and not re.match(r"^(### |## |---\s*$)", linhas[j]):
                corpo.append(linhas[j])
                j += 1
            freq = frequencias(corpo)
            saida.append({
                "caminho": caminho, "n": n, "bencao": nome, "tier": mt.group(1),
                "requisito": int(mt.group(2)) if mt.group(2) else 1,
                "resumo": resumo_por_n.get(n, ""),
                "frequencia": " · ".join(freq) if freq else "Sem limite declarado",
                "nova": "Sim" if "Bênção nova da v1.0" in linha_tier else "Não",
            })
            i = j
    return saida


def armas():
    _, corpo = tabela("24", "## 24.2", "Categoria")
    saida = []
    for l in corpo:
        n, f = dados(l[1])
        saida.append({
            "categoria": re.sub(r"\s*\(2 mãos\)", "", l[0]).strip(), "dados": l[1],
            "n": n, "face": f, "alcance": l[2], "atributo": l[3], "rt": num(l[4]),
            "espaco": num(l[5]), "preco": num(l[6]),
            "duas_maos": "Sim" if "2 mãos" in l[0] else "Não",
        })
    return saida


def armaduras():
    _, corpo = tabela("24", "## 24.1", "Tipo")
    saida = []
    for l in corpo:
        outros = l[2]
        vel = re.search(r"([+-]\d+) de Velocidade", outros)
        rd = re.search(r"(\d+) RD", outros)
        # 24.1 (v1.1, D4): "-2 em Reflexos e nas Perícias de Agilidade" — não no Teste de Ataque
        pen = re.search(r"([+-]\d+) em Reflexos e nas Perícias de Agilidade", outros)
        saida.append({
            "tipo": l[0], "defesa": num(l[1]), "outros": outros, "esquiva": l[3],
            "espaco": num(l[4]), "preco": num(l[5]),
            "vel": int(vel.group(1)) if vel else 0, "rd": int(rd.group(1)) if rd else 0,
            "pen_agilidade": int(pen.group(1)) if pen else 0,
        })
    return saida


def propriedades():
    _, corpo = tabela("24", "## 24.2", "Propriedade")
    return [{"propriedade": l[0], "efeito": l[1]} for l in corpo]


def pocoes():
    _, corpo = tabela("24", "## 24.3", "Poção")
    return [{"pocao": l[0], "cura": num(l[1]), "espaco": num(l[2]), "preco": num(l[3])}
            for l in corpo]


def itens():
    _, corpo = tabela("24", "## 24.3", "Item")
    return [{"item": l[0], "espaco": num(l[1]), "preco": num(l[2]), "uso": l[3]} for l in corpo]


def inventario():
    _, corpo = tabela("24", "## 24.4", "Situação")
    return [{"situacao": l[0], "efeito": l[1]} for l in corpo]


def verba():
    _, corpo = tabela("24", "## 24.5", "Faixa de nível")
    return [{"faixa": l[0], "verba": num(l[1]), "compra": l[2]} for l in corpo]


def cone():
    _, corpo = tabela("25", "## 25.2", "Nível do Cone")
    saida = []
    for l in corpo:
        m = re.match(r"\+(\d+) (ou|e) \+(\d+) PV", l[2])
        saida.append({"nivel": num(l[0]), "nivel_personagem": num(l[1]), "bonus": l[2],
                      "numerico": int(m.group(1)), "modo": m.group(2),
                      "pv": int(m.group(3)), "condicional": l[3]})
    return saida


def faixas_equipamento():
    _, corpo = tabela("25", "## 25.1", "Faixa de nível")
    return [{"faixa": l[0], "cone": l[1], "reliquias": l[2]} for l in corpo]


def reliquias():
    _, corpo = tabela("25", "## 25.3", "Slot")
    return [{"slot": l[0], "da": l[1], "t1": num(l[2]), "t2": num(l[3]), "t3": num(l[4]),
             "t4": num(l[5])} for l in corpo]


def conjuntos():
    _, corpo = tabela("25", "## 25.3", "Peças do mesmo Conjunto")
    return [{"pecas": l[0], "ganho": l[1]} for l in corpo]


def ressonancias():
    _, corpo = tabela("26", "## 26.7", "Ressonância")
    return [{"ressonancia": l[0], "nivel": num(l[1]), "opcao": l[2]} for l in corpo]


def tabela_mestra():
    _, corpo = tabela("26", "## 26.2", "Nível")
    saida = []
    # 26.2 (v1.1, N1): "8 (reescreve 1 por nível, do 16 ao 20)" — o intervalo vem da
    # própria célula; sem ele, vale da linha marcada em diante (16.6: "A partir do nível 16")
    marca = next(l[4] for l in corpo if "reescreve" in l[4])
    faixa = re.search(r"do (\d+) ao (\d+)", marca)
    desde = int(faixa.group(1)) if faixa else min(num(l[0]) for l in corpo if "reescreve" in l[4])
    ate = int(faixa.group(2)) if faixa else 20
    for l in corpo:
        m = re.match(r"(\d+) P / (\d+) TR", l[2])
        saida.append({
            "nivel": num(l[0]), "eficiencia": num(l[1]),
            "eficacia_p": int(m.group(1)) if m else 0, "eficacia_tr": int(m.group(2)) if m else 0,
            "bencaos": num(l[3]), "habilidades": num(l[4]),
            "reescreve": "Sim" if desde <= num(l[0]) <= ate else "Não",
            "nivel_max_hab": num(l[5]), "aumento": "Sim" if num(l[6]) else "Não",
            "dados_ab": num(l[7]), "especializacao": num(l[8]) or 0, "teto_rd": num(l[9]),
        })
    return saida


def recursos_por_faixa():
    return tabela("26", "## 26.3", "Faixa")


def habilidades():
    _, corpo = tabela("16", "## 16.3", "Nível")
    saida = []
    for l in corpo:
        dn, df = dados(l[1])
        cn, cf = dados(l[3])
        saida.append({"nivel": num(l[0]), "dano": l[1], "dano_n": dn, "dano_f": df,
                      "dano_media": num(l[2]), "cura": l[3], "cura_n": cn, "cura_f": cf,
                      "cura_media": num(l[4]), "ph": num(l[5]), "rt": num(l[6]),
                      "alcance": l[7]})
    return saida


def buff_debuff():
    _, corpo = tabela("16", "### Buff e Debuff", "Nível")
    return [{"nivel": num(l[0]), "texto": l[1], "duracao": l[2], "alvos": l[3]} for l in corpo]


def passivas():
    _, corpo = tabela("16", "### Passivas", "Nível")
    return [{"nivel": num(l[0]), "texto": l[1]} for l in corpo]


def ultimate():
    _, corpo = tabela("17", "## 17.3", "Faixa de nível")
    saida = []
    for l in corpo:
        dn, df = dados(l[2])
        cn, cf = dados(l[4])
        saida.append({"faixa": l[0], "nivel_equivalente": num(l[1]), "dano": l[2],
                      "dano_n": dn, "dano_f": df, "dano_media": num(l[3]), "cura": l[4],
                      "cura_n": cn, "cura_f": cf, "cura_media": num(l[5]), "rt": num(l[6])})
    return saida


def ph():
    _, corpo = tabela("16", "## 16.2", "Nº de jogadores")
    saida = []
    for l in corpo:
        mx = [int(x) for x in re.findall(r"\d+", l[1])]
        ini = [int(x) for x in re.findall(r"\d+", l[2])]
        saida.append({"jogadores": num(l[0]), "max": mx, "ini": ini})
    return saida


def custo_ph():
    cab, corpo = tabela("16", "## 16.2", "Nível da Habilidade")
    return [{"nivel": num(n), "ph": num(c)} for n, c in zip(cab[1:], corpo[0][1:])]


def energia():
    _, corpo = tabela("17", "## 17.2", "Fonte")
    return [{"fonte": l[0], "energia": l[1], "limite": l[2]} for l in corpo]


def tenacidade():
    _, corpo = tabela("20", "## 20.3", "Fonte")
    return [{"fonte": l[0], "rt": l[1]} for l in corpo]


def elementos():
    _, corpo = tabela("20", "## 20.1", "Elemento")
    _, quebra = tabela("20", "## 20.5", "Elemento")
    q = {l[0]: l for l in quebra}
    saida = []
    for l in corpo:
        dq = q[l[0]][1]
        n, f = dados(dq)
        mult = re.search(r"(\d+) × Eficiência", dq)
        saida.append({"elemento": l[0], "tematica": l[1], "entrega": l[2],
                      "dano_quebra": dq, "quebra_n": n, "quebra_f": f,
                      "quebra_mult_ef": int(mult.group(1)) if mult else 1,
                      "efeito_quebra": q[l[0]][2]})
    return saida


def fraqueza_resistencia():
    _, corpo = tabela("20", "## 20.2", "Situação")
    return [{"situacao": l[0], "dano": l[1], "rt": l[2]} for l in corpo]


def dt_fraqueza():
    cab, corpo = tabela("20", "## 20.2", "Faixa de nível do inimigo")
    return [{"faixa": c, "dt": num(v)} for c, v in zip(cab[1:], corpo[0][1:])]


def condicoes():
    _, corpo = tabela("21", "## 21.5", "Condição")
    saida = []
    for l in corpo:
        # "só inimigos" no nome (Quebrado) ou abrindo o Efeito (Congelado, v1.1: 21.2 e 21.5, D6)
        so = "só inimigos" in l[0] or limpar(l[1]).lower().startswith("só inimigos")
        saida.append({"condicao": re.sub(r"\s*\(só inimigos\)", "", l[0]).strip(),
                      "efeito": l[1], "duracao": l[2], "acumulo": l[3],
                      "so_inimigos": "Sim" if so else "Não"})
    return saida


def racas_morrendo_vantagem():
    """Raças que rolam o Teste de Morrendo com Vantagem: o quadro de 23.5 (v1.1, D3)
    'Quem rola o Teste de Morrendo com Vantagem.' nomeia as três em negrito."""
    linha = next(l for l in secao("23", "## 23.5") if "Quem rola o Teste de Morrendo com Vantagem" in l)
    nomes = {r["raca"] for r in racas()}
    return [x for x in re.findall(r"\*\*([^*]+)\*\*", linha) if x in nomes]


def dt_faixa():
    cab, corpo = tabela("27", "## 27.2", "Dificuldade")
    return cab, [[l[0]] + [num(c) for c in l[1:]] for l in corpo]


def dt_subsistema():
    _, corpo = tabela("27", "## 27.3", "Teste")
    return [{"teste": l[0], "dt": l[1], "capitulo": l[2]} for l in corpo]


def dt_fonte():
    _, corpo = tabela("22", "## 22.3", "A fonte é")
    return [{"fonte": l[0], "dt": l[1]} for l in corpo]


def dt_inimigo():
    """[DT dos efeitos de inimigo, Teste de Resistência do inimigo] — 22.3."""
    tabs = [t for t in tabelas(secao("22", "## 22.3")) if t[0][0].startswith("Faixa do inimigo")]
    return [[[l[0]] + [num(c) for c in l[1:]] for l in t[1]] for t in tabs]


def compra_pontos():
    cab, corpo = tabela("03", "### Método B", "Valor")
    return [{"valor": num(v), "custo": num(c)} for v, c in zip(cab[1:], corpo[0][1:])]


def bonus_atributo():
    cab, corpo = tabela("04", "## 4.2", "Valor")
    return [{"valor": num(v), "bonus": num(b)} for v, b in zip(cab[1:], corpo[0][1:])]


def memo_tabela(primeira):
    _, corpo = tabela("11", "## 11.3", primeira)
    return corpo


def memo_ficha():
    _, corpo = tabela("11", "## 11.4", "Estatística")
    return corpo


def alcances():
    for l in capitulo("18"):
        if "Pessoal → Curta" in l:
            return [limpar(x) for x in l.lstrip("> ").replace("**", "").split("→")]
    raise ValueError("escala de Distâncias não achada no capítulo 18")


def tipos_habilidade():
    _, corpo = tabela("16", "## 16.1", "Campo")
    for l in corpo:
        if l[0] == "Tipo":
            return [t.strip() for t in re.split(r",| ou ", l[1]) if t.strip()]
    raise ValueError("linha Tipo não achada em 16.1")


# ---------------------------------------------------------------------------
# Mesa do Mestre: âncoras de inimigo, orçamento de encontro e recompensas
# ---------------------------------------------------------------------------

TIPOS_INIMIGO = ["Comum", "Elite", "Boss"]


def _por_tipo(celula):
    """'13 / 15 / 16' -> {'Comum': 13, 'Elite': 15, 'Boss': 16}."""
    partes = [p.strip() for p in limpar(celula).split("/")]
    return {t: num(p) for t, p in zip(TIPOS_INIMIGO, partes)}


def _tabela_por_tamanho(prefixo, titulo, primeira_coluna, colunas):
    """A tabela da seção que começa por `primeira_coluna` e tem `colunas` colunas.
    Duas tabelas da mesma seção podem abrir pela mesma palavra (28.2 e 28.3)."""
    for cab, corpo in tabelas(secao(prefixo, titulo)):
        if cab and cab[0].startswith(primeira_coluna) and len(cab) == colunas:
            return cab, corpo
    raise ValueError(f"tabela '{primeira_coluna}' de {colunas} colunas não achada "
                     f"em {prefixo} {titulo}")


def ancoras_inimigo():
    """28.3 — a tabela mestra do bestiário: uma linha por faixa, 13 campos por tipo."""
    _, corpo = _tabela_por_tamanho("28", "## 28.3", "Faixa", 13)
    _, dados_ = _tabela_por_tamanho("28", "## 28.3", "Faixa", 4)
    dano = {}
    for l in dados_:
        dano[l[0]] = {t: {"texto": limpar(v).split("·")[0].strip(),
                          "media": num(limpar(v).split("·")[-1])}
                      for t, v in zip(TIPOS_INIMIGO, l[1:])}
    saida = []
    for i, l in enumerate(corpo):
        faixa = l[0]
        saida.append({
            "faixa": faixa, "n": i + 1,
            "pv": {t: num(v) for t, v in zip(TIPOS_INIMIGO, l[1:4])},
            "defesa": _por_tipo(l[4]), "rd": _por_tipo(l[5]),
            "tenacidade": _por_tipo(l[6]), "vel": _por_tipo(l[7]),
            "ataque": num(l[8]),
            "dano_media": _por_tipo(l[9]), "dt": _por_tipo(l[10]), "tr": _por_tipo(l[11]),
            "fraquezas": {t: p.strip() for t, p in zip(TIPOS_INIMIGO, l[12].split("/"))},
            "dano": dano.get(faixa, {}),
        })
    return saida


def orcamento_encontro():
    """27.4 — orçamento de PV por faixa e o custo de cada tipo de inimigo."""
    _, corpo = tabela("27", "## 27.4", "Faixa")
    return [{"faixa": l[0], "n": i + 1, "dano_ciclo": num(l[1]), "orcamento": num(l[2]),
             "custo": {t: num(v) for t, v in zip(TIPOS_INIMIGO, l[3:6])}}
            for i, l in enumerate(corpo)]


def composicoes_encontro():
    """27.4 — as quatro composições que gastam o orçamento inteiro."""
    _, corpo = tabela("27", "## 27.4", "Composição")
    return [{"composicao": l[0], "sensacao": l[1], "duracao": l[2]} for l in corpo]


def acoes_por_tipo():
    """28.2 regra 5 — ações agressivas por turno e por Ciclo."""
    _, corpo = _tabela_por_tamanho("28", "## 28.2", "Tipo", 3)
    return [{"tipo": l[0], "por_turno": l[1], "por_ciclo": l[2]} for l in corpo]


def fraquezas_por_tipo():
    """28.2 regra 7 — quantas Fraquezas cada tipo tem."""
    _, corpo = _tabela_por_tamanho("28", "## 28.2", "Tipo", 2)
    return [{"tipo": l[0], "fraquezas": l[1]} for l in corpo]


def atraso_por_tipo():
    """19.4 — teto de Atraso por Ciclo e quem tem Firmeza."""
    _, corpo = tabela("19", "## 19.4", "Tipo de alvo")
    saida = []
    for l in corpo:
        for tipo in re.split(r",| e ", l[0]):
            tipo = tipo.strip()
            if tipo in TIPOS_INIMIGO:
                saida.append({"tipo": tipo, "teto": num(l[1]),
                              "firmeza": "Sim" if l[2].lower().startswith("tem") else "Não"})
    return saida


def recompensas_calendario():
    """27.8 — quando entra cada recompensa e quem decide."""
    _, corpo = tabela("27", "## 27.8", "Recompensa")
    return [{"recompensa": l[0], "quando": l[1], "quem": l[2]} for l in corpo]


def equipamento_por_faixa():
    """27.8 — Cone de Luz máximo e Tier de Relíquia por faixa."""
    _, corpo = tabela("27", "## 27.8", "Faixa")
    return [{"faixa": l[0], "n": i + 1, "cone": l[1], "reliquias": l[2]}
            for i, l in enumerate(corpo)]


# ---------------------------------------------------------------------------
# Bestiário: as 32 fichas nominais de 28.6 a 28.10
# ---------------------------------------------------------------------------

# O subtítulo da ficha, já sem o itálico que `limpar` tira:
# "Comum · Fragmentum · faixa 1-4" (com " · 2 fases" nos Bosses de fase)
RE_SUBTITULO = re.compile(r"^(Comum|Elite|Boss) · (.+?) · faixa ([\d-]+)(.*)$")
RE_ATAQUE = re.compile(r"^- \*\*(.+?)\*\*\s*\((.+?)\)\s*:\s*(.*)$")


def _blocos_do_bestiario():
    """(título, linhas) de cada '### ' do capítulo 28 que tenha ficha de inimigo."""
    blocos, atual = [], None
    for linha in capitulo("28"):
        if linha.startswith("### "):
            atual = (limpar(linha[4:]), [])
            blocos.append(atual)
        elif atual is not None:
            atual[1].append(linha)
    marca = "| Campo | Valor |"
    return [b for b in blocos if any(l.strip().startswith(marca) for l in b[1])]


def _campos_do_bloco(linhas):
    """Junta as tabelas 'Campo | Valor' do bloco. A primeira ocorrência vence:
    o quadro principal manda, e o quadro da fase 1 só completa o que falta."""
    campos = {}
    for cab, corpo in tabelas(linhas):
        if len(cab) != 2 or cab[0] != "Campo":
            continue
        for l in corpo:
            campos.setdefault(l[0], l[1])
    return campos


def _lista_marcada(celula):
    """'**Físico**, **Fogo**' -> ['Físico', 'Fogo']; '—' -> []."""
    celula = limpar(celula or "")
    if celula in ("—", "-", "", "nenhuma", "Nenhuma"):
        return []
    return [p.strip() for p in celula.split(",") if p.strip() and p.strip() != "—"]


def _itens_da_secao(linhas, titulos):
    """Os itens de lista ('- ...') do primeiro bloco em negrito cujo texto está em `titulos`."""
    dentro = False
    itens = []
    for l in linhas:
        t = l.strip()
        if t.startswith("**"):
            rotulo = limpar(t).split("—")[0].split(":")[0].strip().rstrip(".")
            if rotulo in titulos:
                if "nenhuma" in limpar(t).lower():
                    return []
                dentro = True
                continue
            if dentro:
                break
        if dentro and t.startswith("- "):
            itens.append(t)
        elif dentro and itens and t and not t.startswith(("-", ">", "|")):
            itens[-1] += " " + t
    return itens


def bestiario():
    """As fichas nominais do capítulo 28, com os números estruturados.
    O texto completo de cada ficha já está em LIVRO (o bloco '### Nome' do capítulo 28)."""
    faixas = [a["faixa"] for a in ancoras_inimigo()]
    saida = []
    for nome, linhas in _blocos_do_bestiario():
        sub = next((limpar(l) for l in linhas
                    if l.startswith("*") and RE_SUBTITULO.match(limpar(l))), "")
        m = RE_SUBTITULO.match(sub)
        if not m:
            raise ValueError(f"bestiário: subtítulo não reconhecido em '{nome}': {sub!r}")
        tipo, faccao, faixa, resto = m.group(1), m.group(2), m.group(3), m.group(4)
        campos = _campos_do_bloco(linhas)
        fases = num(re.search(r"(\d+) fases", resto).group(1)) if "fases" in resto else 1
        frase = next((limpar(l).strip('>" ') for l in linhas if l.startswith("> *")), "")
        ataques = []
        for item in _itens_da_secao(linhas, ("Ataques", "Ataque")):
            ma = RE_ATAQUE.match(item.strip())
            if not ma:
                continue
            partes = [p.strip() for p in limpar(ma.group(2)).split(",")]
            corpo = limpar(ma.group(3))
            md = re.search(r"`([^`]+)`", ma.group(3))
            ataques.append({
                "nome": limpar(ma.group(1)),
                "alcance": partes[0] if partes else "",
                "elemento": partes[1] if len(partes) > 1 else "",
                "nota": ", ".join(partes[2:]),
                "dados": md.group(1) if md else "",
                "media": num(corpo.split("média")[-1]) if "média" in corpo else None,
                "texto": corpo,
            })
        especiais = []
        for item in _itens_da_secao(linhas, ("Ações especiais", "Ação especial")):
            ma = re.match(r"^- \*\*(.+?)\*\*\s*(\((.+?)\))?\s*:?\s*(.*)$", item.strip())
            if not ma:
                continue
            especiais.append({"nome": limpar(ma.group(1)), "recarga": limpar(ma.group(3) or ""),
                              "efeito": limpar(ma.group(4))})
        fila = next((limpar(l).replace("Na Fila:", "").strip()
                     for l in linhas if l.strip().startswith("**Na Fila:**")), "")
        saida.append({
            "nome": nome, "tipo": tipo, "faccao": faccao, "faixa": faixa,
            "faixa_n": faixas.index(faixa) + 1 if faixa in faixas else None,
            "fases": fases, "frase": frase,
            "pv": num(campos.get("PV")), "defesa": num(campos.get("Defesa")),
            "rd": num(campos.get("RD")), "tenacidade": num(campos.get("Tenacidade")),
            "vel": num(campos.get("Velocidade")), "ataque": num(campos.get("Teste de Ataque")),
            "dt": num(campos.get("DT dos efeitos")),
            "tr": num(campos.get("Teste de Resistência")),
            "fraquezas": _lista_marcada(campos.get("Fraquezas")),
            "resistencias": _lista_marcada(campos.get("Resistências")),
            "ataques": ataques, "especiais": especiais,
            "fila": fila, "firmeza": "Não" if "sem Firmeza" in fila else "Sim",
            "pv_nota": limpar(campos.get("PV", "")),
        })
    return saida


# ---------------------------------------------------------------------------
# Módulo transcrito (interpretação), com âncora literal no .md
# ---------------------------------------------------------------------------

TRANSCRITO = {
    "acumulos": [
        {"caminho": "A Destruição", "bencao": "Sacrifício Desesperado", "recurso": "Fúria",
         "maximo": 2, "cap": "07", "ancora": "Máximo de **2 acúmulos por combate**"},
        {"caminho": "A Destruição", "bencao": "Cicatriz da Destruição",
         "recurso": "Marcas da Ruína", "maximo": 5, "cap": "07",
         "ancora": "Máximo de **5 Marcas**, e elas zeram no fim do combate"},
        {"caminho": "A Inexistência", "bencao": "Marca do Vazio", "recurso": "Marca do Vazio",
         "maximo": 3, "cap": "08", "ancora": "A marca **acumula até 3 vezes**"},
        {"caminho": "A Inexistência", "bencao": "Corrupção Progressiva", "recurso": "Corrupção",
         "maximo": 5, "cap": "08",
         "ancora": "ela ganha **1 acúmulo de Corrupção** (capítulo 21). Máximo de **5**"},
        {"caminho": "A Abundância", "bencao": "Florescimento da Alma",
         "recurso": "Florescimento", "maximo": 5, "cap": "10",
         "ancora": "ganhe **1 acúmulo de Florescimento**. Máximo de **5**"},
        {"caminho": "A Recordação", "bencao": "Memória Devastadora",
         "recurso": "Fragmentos de Memória", "maximo": 5, "cap": "11",
         "ancora": "ele ganha **1 Fragmento de Memória**. Máximo de **5**"},
        {"caminho": "A Recordação", "bencao": "Ataque Espiritual",
         "recurso": "Lembranças Passadas", "maximo": 3, "cap": "11",
         "ancora": "Acumula até **3 vezes**; cada acúmulo além do primeiro soma **+1d6** ao tique"},
    ],
    # Decisão 2 do plano: Bênçãos (e escolhas do Memoespírito) com efeito fixo
    # aplicado nos números da ficha.
    "efeitos_automaticos": [
        {"caminho": "A Abundância", "bencao": "Corpo Imortal", "efeito": "PV máximo +2 × nível",
         "cap": "10", "ancora": "- **+PV máximo igual a `2 × seu nível`**. No nível 9 são 18 PV; no 20, 40."},
        {"caminho": "A Abundância", "bencao": "Corpo Imortal", "efeito": "RD = Eficiência (teto de RD)",
         "cap": "10", "ancora": "- Você tem **RD igual à sua Eficiência** (dentro do teto de RD)."},
        {"caminho": "A Preservação", "bencao": "Pele de Pedra", "efeito": "RD +2 permanente",
         "cap": "15", "ancora": "- **+2 RD**, permanentemente (dentro do teto de RD)."},
        {"caminho": "A Caça", "bencao": "Olho de Lan", "efeito": "faixa de crítico 19-20",
         "cap": "14", "ancora": "A sua **faixa de crítico** passa a ser **19-20** em todos os seus Testes de Ataque."},
        {"caminho": "A Caça", "bencao": "Avatar da Caça", "efeito": "Velocidade +2 permanente",
         "cap": "14", "ancora": "- Você ganha **+2 de Velocidade**, permanentemente."},
        {"caminho": "A Recordação", "bencao": "Avatar da Recordação",
         "efeito": "Forma Sincronizada: PV máximo +2 × nível, Defesa +1, +1 dado base",
         "cap": "11", "ancora": "- **Você** ganha **+PV máximo igual a `2 × seu nível`**, **+1 de Defesa** e **+1 dado base** nos seus ataques."},
        {"caminho": "A Destruição", "bencao": "Instinto de Sobrevivência",
         "efeito": "+2 em Testes de Ataque com PV ≤ 1/3 do máximo (teto de bônus)",
         "cap": "07", "ancora": "- **+2** em Testes de Ataque (dentro do teto de bônus somado)."},
        {"caminho": "A Destruição", "bencao": "Sacrifício Desesperado",
         "efeito": "+1d6 de dano por acúmulo de Fúria (teto de dados adicionais)",
         "cap": "07", "ancora": "- Cada acúmulo dá **+1d6** de dano do seu Elemento em todos os seus ataques, até o fim do combate."},
        {"caminho": "A Destruição", "bencao": "Cicatriz da Destruição",
         "efeito": "+1 dano, +1 Força de Vontade e Resistência Mental por Marca (teto de bônus)",
         "cap": "07", "ancora": "- Cada Marca dá **+1 de dano** nos seus ataques e **+1** em Testes de **Força de Vontade** e de **Resistência Mental**."},
        {"caminho": "A Abundância", "bencao": "Florescimento da Alma",
         "efeito": "+1 em Testes de Resistência e +1 de Defesa por acúmulo (teto de bônus)",
         "cap": "10", "ancora": "- Cada acúmulo dá **+1** em Testes de Resistência e **+1 de Defesa**, respeitando o **teto de bônus somado** da sua faixa."},
        {"caminho": "A Recordação", "bencao": "Memória Compartilhada",
         "efeito": "com o Memoespírito ativo: +1 em ataques e +1d6 de dano",
         "cap": "11", "ancora": "| 6 | **Memória Compartilhada** | I | Com ele em campo: +1 em ataques, +1d6 de dano, +1 Distância |"},
        {"caminho": "A Recordação", "bencao": "Fragmentos do Eu Perdido",
         "efeito": "Memória da Guarda: +Eficiência de Defesa com o Memoespírito ativo",
         "cap": "11", "ancora": "- Você ganha **+Eficiência de Defesa** enquanto o Memoespírito estiver ativo."},
        {"caminho": "A Recordação", "bencao": "Ecos do Passado",
         "efeito": "Memoespírito: PV máximo +4 × nível e +Bônus do Atributo de Habilidade no dano",
         "cap": "11", "ancora": "- O Memoespírito ganha **+PV máximo igual a `4 × seu nível`**. No nível 1 são 4 PV; no nível 20, 80."},
        {"caminho": "A Recordação", "bencao": "Função Catalisador",
         "efeito": "você ganha +1 em Testes de Ataque com o Memoespírito ativo",
         "cap": "11", "ancora": "| **Catalisador** | **Você** ganha **+1** em Testes de Ataque enquanto ele estiver ativo"},
        {"caminho": "A Recordação", "bencao": "Evolução Fusão de Memórias",
         "efeito": "você ganha +1 em Testes de Ataque com o Memoespírito ativo",
         "cap": "11", "ancora": "| **Fusão de Memórias** | **Você** ganha **+1** em Testes de Ataque enquanto ele estiver ativo"},
    ],
    "recurso_proprio": [
        # 07 a 11: linha "Recurso próprio" da ficha do Caminho, nova na v1.1 (D2)
        {"caminho": "A Destruição", "recurso": "Os seus PV, gastos como moeda: 2 × nível por ativação; 5 × nível por dado base do Avatar",
         "cap": "07", "ancora": "| **Recurso próprio** | **Os seus PV**, gastos como moeda (7.2) |"},
        {"caminho": "A Inexistência", "recurso": "Nenhum além dos acúmulos das Bênçãos: Marca do Vazio (até 3) e Corrupção (até 5)",
         "cap": "08", "ancora": "| **Recurso próprio** | Nenhum além dos acúmulos das Bênçãos: **Marca do Vazio** (até 3) e **Corrupção** (até 5) |"},
        {"caminho": "A Harmonia", "recurso": "Nenhum além dos acúmulos das Bênçãos: Eco da Vitória (até 3)",
         "cap": "09", "ancora": "| **Recurso próprio** | Nenhum além dos acúmulos das Bênçãos: **Eco da Vitória** (até 3) |"},
        {"caminho": "A Abundância", "recurso": "Nenhum além dos acúmulos das Bênçãos: Florescimento (até 5)",
         "cap": "10", "ancora": "| **Recurso próprio** | Nenhum além dos acúmulos das Bênçãos: **Florescimento** (até 5) |"},
        {"caminho": "A Recordação", "recurso": "Memoespírito (11.3 a 11.5)",
         "cap": "11", "ancora": "| **Recurso próprio** | **Memoespírito** (11.3 a 11.5) |"},
        {"caminho": "A Erudição", "recurso": "Acúmulos de Cálculo (máximo 5)",
         "cap": "12", "ancora": "**Máximo de 5 acúmulos.**"},
        {"caminho": "A Euforia", "recurso": "Tabela do Riso (1d6)",
         "cap": "13", "ancora": "| **Recurso próprio** | **Tabela do Riso** (1d6) |"},
        {"caminho": "A Caça", "recurso": "Marcação de Presa (1 alvo) + faixa de crítico 19-20 com Olho de Lan",
         "cap": "14", "ancora": "| **Recurso próprio** | **Marcação de Presa** + **faixa de crítico 19-20** |"},
        {"caminho": "A Preservação", "recurso": "Barreira (teto 3 × Eficiência)",
         "cap": "15", "ancora": "| **Teto** | **`3 × Eficiência`**, o mesmo teto global de PV temporários do livro (capítulo 23) |"},
    ],
    "vantagens_raciais": [
        {"raca": "Xianzhouíta", "onde": "todos os 6 Testes de Resistência (inclusive Morrendo)",
         "cap": "05", "ancora": "**Você tem Vantagem em qualquer Teste de Resistência.**"},
        {"raca": "Xianzhouíta", "onde": "não pode ser Executado",
         "cap": "05", "ancora": "**Você não pode ser Executado por ninguém.**"},
        {"raca": "Xianzhouíta", "onde": "1 pergunta verdadeira por cena sobre o que tem passado",
         "cap": "05", "ancora": "Faça ao Mestre **uma pergunta concreta** sobre o que você apontou"},
        {"raca": "Vidyadhara", "onde": "1 por Descanso Curto: recupera PV; respira debaixo d'água",
         "cap": "05", "ancora": "**Uma vez por Descanso Curto**, gaste a sua **Ação Complementar** para recuperar"},
        {"raca": "Vulpes", "onde": "Persuasão, Intimidação, Enganação, Liderança e Força de Vontade",
         "cap": "05", "ancora": "Persuasão, Intimidação, Enganação, Liderança e o Teste de Força de Vontade"},
        {"raca": "Haloviano", "onde": "2 por dia: Ação Complementar deixa o alvo Controlado",
         "cap": "05", "ancora": "**2 vezes por dia.** Gaste a sua **Ação Complementar**."},
        {"raca": "Avginiano", "onde": "Resistência Mental, Percepção Mental e Força de Vontade",
         "cap": "05", "ancora": "Você tem **Vantagem** em três dos seis Testes de Resistência:"},
        {"raca": "Avginiano", "onde": "1 por combate: metade da duração ao falhar num Teste",
         "cap": "05", "ancora": "**Uma vez por combate**, quando você **falha** em um Teste de Resistência"},
        {"raca": "Intellitron", "onde": "Tecnologia, Mecânica e teste de descobrir Fraqueza",
         "cap": "05", "ancora": "Você tem **Vantagem em Testes de Tecnologia e de Mecânica**."},
        {"raca": "Intellitron", "onde": "imune a doença natural e a veneno de origem biológica",
         "cap": "05", "ancora": "Você é **imune a doença natural** e a **veneno de origem biológica**."},
        {"raca": "Humano", "onde": "Esforço (máximo 1 ponto)",
         "cap": "05", "ancora": "Você carrega **no máximo 1 ponto** de Esforço."},
        {"raca": "Humano", "onde": "1 Perícia escolhida a mais, fixada na criação",
         "cap": "05", "ancora": "Na criação, você escolhe **1 Perícia a mais**"},
        {"raca": "Vulpes", "onde": "1 por Descanso Longo: alguém daquele lugar lhe deve um favor",
         "cap": "05", "ancora": "você declara que alguém naquele lugar lhe deve um favor antigo"},
        {"raca": "Haloviano", "onde": "não sofre dano de queda e desce planando",
         "cap": "05", "ancora": "Você **não sofre dano de queda**, de nenhuma altura"},
    ],
    # Listas de validação que o livro escreve em prosa (não em tabela)
    "listas": {
        "sim_nao": {"titulo": "Sim/Não", "valores": ["Sim", "Não"], "cap": None, "ancora": None},
        "metodo": {"titulo": "Método de atributos", "valores": ["Array oficial", "Compra de Pontos"],
                   "cap": "03", "ancora": "### Método A — o array oficial"},
        # v1.2: a chave continua "modo_humano" (ela é referência de fórmula e de mapa), mas o
        # modo passou a valer para todas as Raças — o que é só do Humano é a lista de Atributos
        "modo_humano": {"titulo": "Bônus racial: +2 em um, ou +1 em cada",
                        "valores": ["Um Atributo (+2)", "Dois Atributos (+1 cada)"],
                        "cap": "05", "ancora": "**+2 em um** dos dois Atributos dela, **ou +1 em cada**"},
        "modo_aumento": {"titulo": "Aumento de Atributo", "valores": ["Um Atributo (+2)", "Dois Atributos (+1 cada)"],
                         "cap": "04", "ancora": "> **+2 em um Atributo**, ou **+1 em dois Atributos diferentes** — respeitando o teto 20."},
        "resolucao": {"titulo": "Resolução", "valores": ["Teste de Ataque", "Teste de Resistência"],
                      "cap": "16", "ancora": "| **Resolução** | **Teste de Ataque** ou **Teste de Resistência do alvo** — nunca os dois |"},
        "sintonia": {"titulo": "Atributo da Sintonia", "valores": ["Discernimento", "Sincronia"],
                     "cap": "04", "ancora": "**Sintonia** (+Discernimento **ou** +Sincronia)"},
        "alvo_cone": {"titulo": "Alvo do Bônus Maior",
                      "valores": ["PV máximos", "Defesa", "Velocidade", "Dano de Ataque Básico",
                                  "Dano de Habilidade", "Dano de Ultimate", "RD", "Teste de Ataque",
                                  "Um Teste de Resistência", "Uma Perícia"],
                      "cap": "25", "ancora": "- **Dano** de uma das três categorias: Ataque Básico, Habilidade ou Ultimate (capítulo 18)"},
        "cone_escolha": {"titulo": "Cone: numérico ou PV", "valores": ["Numérico", "PV"],
                         "cap": "25", "ancora": "| **1** | 1 | +1 **ou** +10 PV |"},
        "conjunto": {"titulo": "Conjunto", "valores": ["A", "B", "C", "—"],
                     "cap": "25", "ancora": "Você pode usar dois Conjuntos ao mesmo tempo: **4 + 2**, **2 + 2 + 2**"},
        "bonus_conjunto2": {"titulo": "Bônus de 2 peças",
                            "valores": ["Um tipo de rolagem +1", "Velocidade +1", "Dano +2", "RD +1"],
                            "cap": "25", "ancora": "**+1** em um tipo de rolagem, **+1 de Velocidade**, **+2 de dano** ou **+1 RD**"},
        "ress1": {"titulo": "Ressonância I",
                  "valores": ["Habilidade de Nível 3 ou menor sem PH (1 por combate)", "Velocidade +1"],
                  "cap": "26", "ancora": "**1 uso por combate de uma Habilidade de Nível 3 ou menor sem custo de PH**; **ou** **+1 de Velocidade** permanente"},
        "ress2": {"titulo": "Ressonância II", "valores": ["Ultimate com efeito extra"],
                  "cap": "26", "ancora": "Sua **Ultimate ganha um efeito extra**"},
        "ress3": {"titulo": "Ressonância III", "valores": ["Uma Habilidade sobe 1 Nível de efeito"],
                  "cap": "26", "ancora": "Uma Habilidade sua **sobe 1 Nível de efeito e passa a custar o PH do Nível novo**"},
        "ress4": {"titulo": "Ressonância IV",
                  "valores": ["Ultimate com 80 de Energia", "Avatar afeta um alvo adicional"],
                  "cap": "26", "ancora": "Sua Ultimate **ativa com 80 de Energia e consome 80**"},
    },
}

# ---------------------------------------------------------------------------
# Blocos da aba Dados (a ordem desta lista é a ordem/posição na aba)
# ---------------------------------------------------------------------------

def blocos():
    """Blocos de tabela da aba Dados: dict(id, titulo, cabecalho, linhas).
    O título já traz a fonte (capítulo/seção)."""
    B = []

    def bloco(id_, titulo, cab, linhas):
        B.append({"id": id_, "titulo": titulo, "cabecalho": list(cab),
                  "linhas": [list(x) for x in linhas]})

    bloco("racas", "Raças — capítulo 05 (tabela de consulta rápida e traços)",
          ["Raça", "Bônus de atributo", "Bônus livre (+2 em um ou +1 em dois)", "Opção 1 do +2",
           "Opção 2 do +2", "Traços (resumo)", "Traços (texto do livro)"],
          [[r["raca"], r["bonus"], "Sim" if r["livre"] else "Não", r["opcao1"], r["opcao2"],
            r["tracos"], r["texto_tracos"]] for r in racas()])
    bloco("vantagens_raciais", "Vantagens e traços automáticos por Raça — capítulo 05 (transcrito)",
          ["Raça", "Onde vale"],
          [[v["raca"], v["onde"]] for v in TRANSCRITO["vantagens_raciais"]])
    bloco("bonus_atributo", "Bônus de Atributo — 04.2",
          ["Valor", "Bônus"], [[b["valor"], b["bonus"]] for b in bonus_atributo()])
    bloco("compra", "Compra de Pontos — 03 Passo 4 (Método B)",
          ["Valor", "Custo acumulado"], [[c["valor"], c["custo"]] for c in compra_pontos()])
    bloco("pericias", "Perícias — 04.4",
          ["Perícia", "Atributo", "O que resolve"],
          [[p["pericia"], p["atributo"], p["resolve"]] for p in pericias()])
    bloco("tr", "Testes de Resistência — 04.6",
          ["Teste de Resistência", "Atributo"],
          [[t["tr"], t["atributo"]] for t in testes_resistencia()])
    rec = {x["caminho"]: x["recurso"] for x in TRANSCRITO["recurso_proprio"]}
    bloco("caminhos", "Caminhos — 06.2 e 06.3 (recurso próprio: capítulos 07 a 15)",
          ["Caminho", "Aeon", "A ideia, em uma frase", "Atributo de Habilidade", "Opção 1",
           "Opção 2", "Perícia 1", "Perícia 2", "Perícia 3", "N", "Bônus de VEL",
           "Recurso próprio"],
          [[c["caminho"], c["aeon"], c["ideia"], c["atributo_habilidade"], c["attr1"],
            c["attr2"], c["pericia1"], c["pericia2"], c["pericia3"], c["n"], c["vel"],
            rec[c["caminho"]]] for c in caminhos()])
    cab_pv, pv = tabela_pv()
    bloco("pv", "PV com Bônus de Vigor +2 — 06.4", cab_pv, pv)
    bloco("bencaos", "Bênçãos — capítulos 07 a 15 (12 por Caminho)",
          ["Caminho", "Nº", "Bênção", "Tier", "Requisito (nível)", "Em uma linha",
           "Frequência", "Nova da v1.0"],
          [[b["caminho"], b["n"], b["bencao"], b["tier"], b["requisito"], b["resumo"],
            b["frequencia"], b["nova"]] for b in bencaos()])
    bloco("acumulos", "Acúmulos das Bênçãos — capítulos 07 a 15 (transcrito)",
          ["Caminho", "Bênção", "Acúmulo", "Máximo"],
          [[a["caminho"], a["bencao"], a["recurso"], a["maximo"]]
           for a in TRANSCRITO["acumulos"]])
    bloco("efeitos_automaticos", "Efeitos aplicados nos números — decisão 2 do plano (transcrito)",
          ["Caminho", "Bênção ou escolha", "Efeito"],
          [[e["caminho"], e["bencao"], e["efeito"]] for e in TRANSCRITO["efeitos_automaticos"]])
    bloco("mestra", "Tabela mestra, nível 1 a 20 — 26.2",
          ["Nível", "Eficiência", "Eficácia: Perícias", "Eficácia: Testes de Resistência",
           "Bênçãos", "Habilidades conhecidas", "Reescreve 1 por nível",
           "Nível máx. de Habilidade", "Aumento de Atributo", "Dados de Ataque Básico",
           "Especialização", "Teto de RD"],
          [[m["nivel"], m["eficiencia"], m["eficacia_p"], m["eficacia_tr"], m["bencaos"],
            m["habilidades"], m["reescreve"], m["nivel_max_hab"], m["aumento"], m["dados_ab"],
            m["especializacao"], m["teto_rd"]] for m in tabela_mestra()])
    cab_rf, corpo_rf = recursos_por_faixa()
    bloco("faixas", "Recursos do grupo e equipamento por faixa (mesa de 4) — 26.3",
          cab_rf, corpo_rf)
    bloco("ressonancias", "Ressonâncias — 26.7",
          ["Ressonância", "Nível", "O que ela dá"],      # 26.7 (v1.2, E15): só I e IV têm duas opções
          [[r["ressonancia"], r["nivel"], r["opcao"]] for r in ressonancias()])
    bloco("habilidades", "Níveis de Habilidade — 16.3",
          ["Nível", "Dano", "Dados de dano", "Face do dano", "Média do dano", "Cura",
           "Dados de cura", "Face da cura", "Média da cura", "Custo (PH)",
           "Redução de Tenacidade", "Alcance (cumulativo)"],
          [[h["nivel"], h["dano"], h["dano_n"], h["dano_f"], h["dano_media"], h["cura"],
            h["cura_n"], h["cura_f"], h["cura_media"], h["ph"], h["rt"], h["alcance"]]
           for h in habilidades()])
    bloco("buff", "Buff e Debuff — 16.5",
          ["Nível", "O que você pode escrever", "Duração", "Alvos"],
          [[b["nivel"], b["texto"], b["duracao"], b["alvos"]] for b in buff_debuff()])
    bloco("passivas", "Passivas — 16.5",
          ["Nível", "O que você pode escrever"], [[p["nivel"], p["texto"]] for p in passivas()])
    bloco("ultimate", "Ultimate: Nível equivalente por faixa — 17.3",
          ["Faixa de nível", "Nível equivalente", "Dano", "Dados de dano", "Face do dano",
           "Média do dano", "Cura", "Dados de cura", "Face da cura", "Média da cura",
           "Redução de Tenacidade"],
          [[u["faixa"], u["nivel_equivalente"], u["dano"], u["dano_n"], u["dano_f"],
            u["dano_media"], u["cura"], u["cura_n"], u["cura_f"], u["cura_media"], u["rt"]]
           for u in ultimate()])
    bloco("ph", "Pontos de Habilidade do grupo — 16.2",
          ["Nº de jogadores", "Máximo 1-8", "Máximo 9-16", "Máximo 17-20",
           "Início 1-8", "Início 9-16", "Início 17-20"],
          [[p["jogadores"]] + p["max"] + p["ini"] for p in ph()])
    bloco("custo_ph", "Custo em PH por Nível de Habilidade — 16.2",
          ["Nível da Habilidade", "Custo (PH)"], [[c["nivel"], c["ph"]] for c in custo_ph()])
    bloco("energia", "Energia — 17.2",
          ["Fonte", "Energia", "Limite"],
          [[e["fonte"], e["energia"], e["limite"]] for e in energia()])
    bloco("tenacidade", "Redução de Tenacidade — 20.3",
          ["Fonte", "Redução de Tenacidade"], [[t["fonte"], t["rt"]] for t in tenacidade()])
    bloco("elementos", "Elementos e Dano de Quebra — 20.1 e 20.5",
          ["Elemento", "Temática", "O que ele entrega na Quebra", "Dano de Quebra",
           "Dados do Dano de Quebra", "Face", "Multiplicador da Eficiência", "Efeito de Quebra"],
          [[e["elemento"], e["tematica"], e["entrega"], e["dano_quebra"], e["quebra_n"],
            e["quebra_f"], e["quebra_mult_ef"], e["efeito_quebra"]] for e in elementos()])
    bloco("fraqueza", "Fraqueza e Resistência — 20.2",
          ["Situação", "Dano", "Redução de Tenacidade"],
          [[f["situacao"], f["dano"], f["rt"]] for f in fraqueza_resistencia()])
    bloco("dt_fraqueza", "DT para descobrir uma Fraqueza — 20.2",
          ["Faixa de nível do inimigo", "DT"], [[d["faixa"], d["dt"]] for d in dt_fraqueza()])
    bloco("condicoes", "Condições — 21.5",
          ["Condição", "Efeito", "Duração", "Acúmulo", "Só inimigos"],
          [[c["condicao"], c["efeito"], c["duracao"], c["acumulo"], c["so_inimigos"]]
           for c in condicoes()])
    cab_dt, corpo_dt = dt_faixa()
    bloco("dt_faixa", "DT por faixa — 27.2", cab_dt, corpo_dt)
    bloco("dt_subsistema", "As cinco DTs de subsistema — 27.3",
          ["Teste", "DT", "Capítulo"],
          [[d["teste"], d["dt"], d["capitulo"]] for d in dt_subsistema()])
    bloco("dt_fonte", "Contra qual DT você rola — 22.3",
          ["A fonte é...", "A DT é..."], [[d["fonte"], d["dt"]] for d in dt_fonte()])
    dti, tri = dt_inimigo()
    bloco("dt_inimigo", "DT dos efeitos de inimigo — 22.3",
          ["Faixa do inimigo", "Comum", "Elite", "Boss"], dti)
    bloco("tr_inimigo", "Teste de Resistência do inimigo — 22.3",
          ["Faixa do inimigo", "Comum", "Elite", "Boss"], tri)
    bloco("armas", "Armas — 24.2",
          ["Categoria", "Dados base", "Nº de dados", "Face", "Alcance", "Atributo de Ataque",
           "Redução de Tenacidade", "Espaço", "Preço (Cr)", "Duas mãos"],
          [[a["categoria"], a["dados"], a["n"], a["face"], a["alcance"], a["atributo"],
            a["rt"], a["espaco"], a["preco"], a["duas_maos"]] for a in armas()])
    bloco("propriedades", "Propriedade especial de arma — 24.2",
          ["Propriedade", "O que faz"], [[p["propriedade"], p["efeito"]] for p in propriedades()])
    bloco("armaduras", "Armaduras — 24.1",
          ["Tipo", "Defesa", "Outros efeitos", "Esquiva", "Espaço", "Preço (Cr)",
           "Velocidade", "RD", "Penalidade em Reflexos e Perícias de Agilidade"],
          [[a["tipo"], a["defesa"], a["outros"], a["esquiva"], a["espaco"], a["preco"],
            a["vel"], a["rd"], a["pen_agilidade"]] for a in armaduras()])
    bloco("pocoes", "Poções de Vida — 24.3",
          ["Poção", "Cura", "Espaço", "Preço (Cr)"],
          [[p["pocao"], p["cura"], p["espaco"], p["preco"]] for p in pocoes()])
    bloco("itens", "Itens comuns — 24.3",
          ["Item", "Espaço", "Preço (Cr)", "Para quê"],
          [[i["item"], i["espaco"], i["preco"], i["uso"]] for i in itens()])
    bloco("inventario", "Inventário e Espaço — 24.4",
          ["Situação", "Efeito"], [[i["situacao"], i["efeito"]] for i in inventario()])
    bloco("verba", "Verba de marco do grupo — 24.5",
          ["Faixa de nível", "Verba de marco (Cr)", "O que ela compra"],
          [[v["faixa"], v["verba"], v["compra"]] for v in verba()])
    bloco("faixas_equipamento", "Cone de Luz e Relíquias por faixa — 25.1",
          ["Faixa de nível", "Cone de Luz máximo", "Relíquias"],
          [[f["faixa"], f["cone"], f["reliquias"]] for f in faixas_equipamento()])
    bloco("cone", "Cone de Luz — 25.2",
          ["Nível do Cone", "Nível do personagem", "Bônus Maior", "Bônus numérico",
           "e/ou", "Bônus de PV", "Efeito Condicional"],
          [[c["nivel"], c["nivel_personagem"], c["bonus"], c["numerico"], c["modo"], c["pv"],
            c["condicional"]] for c in cone()])
    bloco("reliquias", "Relíquias — 25.3",
          ["Slot", "O que dá", "Tier I", "Tier II", "Tier III", "Tier IV"],
          [[r["slot"], r["da"], r["t1"], r["t2"], r["t3"], r["t4"]] for r in reliquias()])
    bloco("conjuntos", "Conjuntos de Relíquias — 25.3",
          ["Peças do mesmo Conjunto", "O que você ganha"],
          [[c["pecas"], c["ganho"]] for c in conjuntos()])
    bloco("memo_conceito", "Memoespírito: Conceito — 11.3 Passo 2",
          ["Conceito", "O que é"], memo_tabela("Conceito"))
    bloco("memo_funcao", "Memoespírito: Função — 11.3 Passo 3",
          ["Função", "Bônus"], memo_tabela("Função"))
    bloco("memo_bonus", "Memoespírito: Bônus menores — 11.3 Passo 4",
          ["Bônus menor", "Efeito"], memo_tabela("Bônus menor"))
    principal, auxiliar = [t for t in tabelas(secao("11", "### Passo 5"))
                           if t[0][0].startswith("Modelo da v0.1")]
    bloco("memo_principal", "Memoespírito: Técnica Principal — 11.3 Passo 5",
          ["Modelo da v0.1", "Acréscimo"], principal[1])
    bloco("memo_auxiliar", "Memoespírito: Técnica Auxiliar — 11.3 Passo 5",
          ["Modelo da v0.1", "Efeito"], auxiliar[1])
    bloco("memo_evolucoes", "Memoespírito: Evoluções (níveis 8, 14 e 20) — 11.3",
          ["Evolução", "Efeito"], memo_tabela("Evolução"))
    bloco("memo_ficha", "Ficha do Memoespírito — 11.4",
          ["Estatística", "Fórmula"], memo_ficha())
    return B


def listas():
    """Listas de validação (uma coluna cada): dict(id, titulo, fonte, valores)."""
    L = []

    def lista(id_, titulo, fonte, valores):
        L.append({"id": id_, "titulo": titulo, "fonte": fonte, "valores": list(valores)})

    lista("racas", "Raças", "05", [r["raca"] for r in racas()])
    lista("caminhos", "Caminhos", "06.3", [c["caminho"] for c in caminhos()])
    lista("atributos", "Atributos", "04.1", ATRIBUTOS)
    lista("elementos", "Elementos", "20.1", [e["elemento"] for e in elementos()])
    lista("armaduras", "Armaduras", "24.1", [a["tipo"] for a in armaduras()])
    lista("armas", "Categorias de arma", "24.2", [a["categoria"] for a in armas()])
    lista("atributo_media", "Atributo da arma Média", "24.2",
          atributos_em(next(a["atributo"] for a in armas() if a["categoria"] == "Média")))
    lista("propriedades", "Propriedade especial", "24.2",
          ["Nenhuma"] + [p["propriedade"] for p in propriedades()])
    lista("tipos_habilidade", "Tipos de Habilidade", "16.1", tipos_habilidade())
    lista("alcances", "Alcances", "18", alcances())
    lista("condicoes", "Condições do personagem", "21.5",
          [c["condicao"] for c in condicoes()
           if c["so_inimigos"] == "Não" and c["condicao"] != "Morrendo"])
    lista("pericias", "Perícias", "04.4", [p["pericia"] for p in pericias()])
    lista("tr", "Testes de Resistência", "04.6", [t["tr"] for t in testes_resistencia()])
    lista("slots", "Slots de Relíquia", "25.3", [r["slot"] for r in reliquias()])
    lista("memo_conceito", "Conceitos do Memoespírito", "11.3",
          [l[0] for l in memo_tabela("Conceito")])
    lista("memo_funcao", "Funções do Memoespírito", "11.3", [l[0] for l in memo_tabela("Função")])
    lista("memo_bonus", "Bônus menores do Memoespírito", "11.3",
          [l[0] for l in memo_tabela("Bônus menor")])
    lista("memo_evolucoes", "Evoluções do Memoespírito", "11.3",
          [l[0] for l in memo_tabela("Evolução")])
    for id_, item in TRANSCRITO["listas"].items():
        lista(id_, item["titulo"], item["cap"] or "convenção da planilha", item["valores"])
    return L


def ancoras():
    """Todas as âncoras do módulo transcrito: lista de (cap, ancora, descrição)."""
    saida = []
    for chave in ("acumulos", "efeitos_automaticos", "recurso_proprio", "vantagens_raciais"):
        for item in TRANSCRITO[chave]:
            desc = f"{chave}: {item.get('bencao') or item.get('caminho') or item.get('raca')}"
            saida.append((item["cap"], item["ancora"], desc))
    for id_, item in TRANSCRITO["listas"].items():
        if item["ancora"]:
            saida.append((item["cap"], item["ancora"], f"listas: {id_}"))
    return saida


if __name__ == "__main__":
    for b in blocos():
        print(f"{b['id']:<20} {len(b['linhas']):>4} linhas × {len(b['cabecalho'])} colunas — {b['titulo']}")
    for l in listas():
        print(f"lista {l['id']:<16} {len(l['valores']):>3} valores")
    falta = [a for a in ancoras() if a[1] not in texto_capitulo(a[0])]
    print(f"âncoras: {len(ancoras())}, não encontradas: {len(falta)}")
    for f in falta:
        print("  ✗", f)
