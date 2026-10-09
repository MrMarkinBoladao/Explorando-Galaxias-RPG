# -*- coding: utf-8 -*-
"""
gerar_ficha.py — Gera a Ficha de Personagem automatizada do RPG
"Explorando Galáxias" v1.2 (.xlsx para importar no Google Planilhas).

O QUE ELE FAZ
    Monta, com openpyxl, um único .xlsx com as 10 abas, nesta ordem:
    Início, Criação, Em Jogo, Testes, Habilidades, Caminho, Equipamento,
    Progressão, Regras Rápidas e Dados. A aba Dados é preenchida a partir dos
    capítulos do livro por `build/ficha_dados.py` (parser dos .md + módulo
    transcrito com âncoras), em blocos com título e fonte.

    Regras de projeto (plano .agents/tasks/plano-ficha.md, seções 2–4):
      - estilos da seção 2.1 (só Arial): entrada, calculada, aviso, título,
        não se aplica — com legenda no topo de cada aba;
      - fórmulas em inglês, separador ',', só funções da lista efetiva
        (build/ficha_funcoes_ok.json), sem nome definido: referência direta;
      - toda célula de ENTRADA sai VAZIA no arquivo (a bateria de testes
        simula "deixar vazio" omitindo a entrada);
      - wb.calculation.fullCalcOnLoad = True.

    Abas de construção (FEAT-002): Criação (os 12 passos do capítulo 03 e os
    números do nível, 'nucleo.*'), Progressão (tabela mestra 1-20, aumentos,
    Ressonâncias, próximo nível), Testes (18 Perícias, 6 Testes de
    Resistência, Morrendo, DT da faixa) e Caminho (ficha, recurso próprio,
    10 slots de Bênção, catálogo, Memoespírito). As fórmulas são escritas com
    marcadores «nome.logico» e resolvidas no fim para a célula do mapa.

    Abas de jogo (FEAT-003): Equipamento (armas e Ataque Básico com o dano
    da regra, Cone de Luz com Sobreposição, Relíquias por Tier, Conjuntos A/B/C,
    inventário com catálogo, Créditos), Habilidades (8 linhas + Ressonância III
    + Ultimate), Em Jogo (uma tela A:L × 1-40: Resumo para o Jogador, recursos,
    calculadora de dano, ações, Testes de Resistência, Perícias, condições e
    usos; avisos fora da tela na coluna N com resumo na linha 13), Regras
    Rápidas (29.12, tabelas lidas da aba Dados) e Início (guia, importação,
    proteção nativa e Painel de avisos). Elas preenchem as células reservadas
    da Criação (criacao.extra.*, criacao.reserva.*) e os extras dos Testes.

    Também grava `build/ficha_mapa.json`, o contrato entre o gerador e os
    testes: nome lógico -> célula ('Aba'!A1), blocos da aba Dados e listas de
    validação. Convenção de nomes: "<aba>.<campo>" com a aba em minúsculas sem
    acento (inicio, criacao, em_jogo, testes, habilidades, caminho,
    equipamento, progressao, regras, dados); blocos "dados.<id>"; listas
    "lista.<id>".

COMO USAR
    $env:PYTHONUTF8="1"; python "build\\gerar_ficha.py"

SAÍDA
    <raiz>\\ficha-automatizada\\Ficha Automatizada - Explorando Galáxias V1.2.xlsx  (modelo em branco)
    <raiz>\\ficha-automatizada\\Ficha Exemplo - Nadir.xlsx  (o mesmo modelo com a Nadir de 29.7)
    <raiz>\\build\\ficha_mapa.json

REQUISITOS
    Python 3, openpyxl 3.1.5 (versões exatas em build\\requirements-ficha.txt).
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils.indexed_list import IndexedList
from openpyxl.workbook.properties import CalcProperties

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ficha_dados  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
BUILD = RAIZ / "build"
VERSAO = "v1.2"                 # versão do livro (capa, 00-capa-e-creditos.md)
ENTREGA = RAIZ / "ficha-automatizada"
SAIDA_XLSX = ENTREGA / "Ficha Automatizada - Explorando Galáxias V1.2.xlsx"
SAIDA_NADIR = ENTREGA / "Ficha Exemplo - Nadir.xlsx"
SAIDA_MAPA = BUILD / "ficha_mapa.json"

ABAS = ["Início", "Criação", "Em Jogo", "Testes", "Habilidades", "Caminho",
        "Equipamento", "Progressão", "Regras Rápidas", "Dados"]
SLUG = {"Início": "inicio", "Criação": "criacao", "Em Jogo": "em_jogo", "Testes": "testes",
        "Habilidades": "habilidades", "Caminho": "caminho", "Equipamento": "equipamento",
        "Progressão": "progressao", "Regras Rápidas": "regras", "Dados": "dados"}

# ---------------------------------------------------------------------------
# Estilos (seção 2.1 do plano) — só Arial
# ---------------------------------------------------------------------------

FONTE = "Arial"
COR_ENTRADA = "FFF2CC"
COR_ENTRADA_BORDA = "BF9000"
COR_CALCULADA = "E8EEF7"
COR_CALCULADA_TEXTO = "1F1F1F"
COR_AVISO_TEXTO = "9C0006"
COR_AVISO_FUNDO = "FFC7CE"          # só via formatação condicional LEN(célula)>0
COR_TITULO = "1F3864"
COR_TITULO_TEXTO = "FFFFFF"
COR_NA = "D9D9D9"
COR_NA_TEXTO = "595959"
TAM_CORPO = 10
TAM_TITULO_BLOCO = 12
TAM_TITULO_ABA = 16
# Ajustes pedidos pelo usuário (v1.1): sem linhas congeladas; no lugar, células visualmente
# diferentes. Cabeçalho de coluna ≠ título de bloco ≠ linha de dados; rótulo da linha em
# negrito com borda direita média; zebra (dois tons da mesma cor) nas tabelas.
COR_CAB_COLUNA = "B4C6E7"           # cabeçalho de coluna de tabela (texto #1F3864, 6,7:1)
COR_CAB_COLUNA_TEXTO = "1F3864"
COR_ZEBRA = {COR_CALCULADA: "D6E0F0", COR_ENTRADA: "FFE9B0", None: "F2F2F2"}   # 2º tom de cada tipo
COR_SEPARADOR = "1F3864"            # borda média: embaixo do cabeçalho e à direita do rótulo da linha

_fino = Side(style="thin", color=COR_ENTRADA_BORDA)
_medio = Side(style="medium", color=COR_SEPARADOR)
BORDA_ENTRADA = Border(left=_fino, right=_fino, top=_fino, bottom=_fino)
BORDA_CABECALHO = Border(bottom=_medio)


def fonte(tamanho=TAM_CORPO, negrito=False, cor="000000", italico=False):
    return Font(name=FONTE, size=tamanho, bold=negrito, italic=italico, color=cor)


def _pos(ws, cel, valor):
    c = ws[cel]
    if valor is not None:
        c.value = valor
    return c


def entrada(ws, cel, valor=None):
    """Célula que o jogador preenche. Sai vazia no arquivo (valor só em exemplo)."""
    c = _pos(ws, cel, valor)
    c.fill = PatternFill("solid", fgColor=COR_ENTRADA)
    c.border = BORDA_ENTRADA
    c.font = fonte()
    c.alignment = Alignment(vertical="center")
    return c


def calculada(ws, cel, valor=None, negrito=False):
    """Célula automática (fórmula ou texto fixo de consulta)."""
    c = _pos(ws, cel, valor)
    c.fill = PatternFill("solid", fgColor=COR_CALCULADA)
    c.font = fonte(negrito=negrito, cor=COR_CALCULADA_TEXTO)
    c.alignment = Alignment(vertical="center")
    return c


def aviso(ws, cel, valor=None):
    """Célula de aviso: texto vermelho escuro negrito; o fundo rosa entra por
    formatação condicional (LEN>0) aplicada pelo chamador na mesma aba."""
    c = _pos(ws, cel, valor)
    c.font = fonte(negrito=True, cor=COR_AVISO_TEXTO)
    c.alignment = Alignment(vertical="center", wrap_text=True)
    return c


def titulo(ws, cel, texto, tamanho=TAM_TITULO_BLOCO, ate=None):
    """Título de bloco: fundo azul-escuro, texto branco negrito. `ate` = última
    coluna (letra) para pintar a faixa inteira (sem mesclar)."""
    c = _pos(ws, cel, texto)
    estilo = PatternFill("solid", fgColor=COR_TITULO)
    c.fill = estilo
    c.font = fonte(tamanho, negrito=True, cor=COR_TITULO_TEXTO)
    c.alignment = Alignment(vertical="center")
    if ate:
        linha = c.row
        for col in range(c.column + 1, _col(ate) + 1):
            o = ws.cell(linha, col)
            o.fill = estilo
            o.font = fonte(tamanho, negrito=True, cor=COR_TITULO_TEXTO)
    return c


def nao_se_aplica(ws, cel, valor=None):
    c = _pos(ws, cel, valor)
    c.fill = PatternFill("solid", fgColor=COR_NA)
    c.font = fonte(cor=COR_NA_TEXTO)
    c.alignment = Alignment(vertical="center")
    return c


def cabecalho(ws, cel, texto):
    """Cabeçalho de coluna de tabela: azul-médio, texto azul-escuro em negrito, borda
    inferior média (diferente do título de bloco e das linhas de dados)."""
    c = _pos(ws, cel, texto)
    c.font = fonte(negrito=True, cor=COR_CAB_COLUNA_TEXTO)
    c.fill = PatternFill("solid", fgColor=COR_CAB_COLUNA)
    c.border = BORDA_CABECALHO
    c.alignment = Alignment(vertical="center", wrap_text=True)
    return c


def texto(ws, cel, valor, negrito=False, italico=False, tamanho=TAM_CORPO):
    c = _pos(ws, cel, valor)
    c.font = fonte(tamanho, negrito=negrito, italico=italico)
    # centro vertical como as entradas e as calculadas: rótulo e valor ficam na mesma altura
    # nas linhas altas (auditoria visual, FEAT-004)
    c.alignment = Alignment(vertical="center")
    return c


def _col(letra):
    from openpyxl.utils import column_index_from_string
    return column_index_from_string(letra)


LEGENDA = [
    (entrada, "Entrada (preencha)"),
    (calculada, "Calculada (automático)"),
    (None, "Aviso (texto em vermelho)"),
    (None, "Título de bloco"),
    (None, "Cabeçalho de coluna"),
    (None, "Rótulo da linha"),
    (None, "Linha alternada (outro tom)"),
    (nao_se_aplica, "Não se aplica"),
]


def legenda(ws, linha, coluna=1, limite=1360):
    """Legenda das cores numa linha (cor nunca é o único sinal: o texto diz). Cada item ocupa
    as colunas que precisar (mescladas) para o texto caber em até 2 linhas, sem passar de
    `limite` px; a altura da linha cresce no ajuste do layout."""
    import renderizar_ficha as R
    texto(ws, ws.cell(linha, coluna).coordinate, "Legenda:", negrito=True)
    c = coluna + 1
    x = sum(R.px_coluna(ws, k) for k in range(1, c))
    for fn, rotulo in LEGENDA:
        negrito = rotulo.startswith(("Aviso", "Título", "Cabeçalho", "Rótulo"))
        f = R.fonte(round(TAM_CORPO * 4 / 3), negrito)
        palavra = max(f.getlength(p) for p in rotulo.split()) * R.FOLGA + R.RESERVA
        inteira = f.getlength(rotulo) * R.FOLGA + R.RESERVA
        k, w = c, R.px_coluna(ws, c)
        while (w < palavra or w * 2 < inteira) and x + w < limite and \
                x + w + R.px_coluna(ws, k + 1) <= limite:
            k += 1
            w += R.px_coluna(ws, k)
        _legenda_item(ws, ws.cell(linha, c).coordinate, fn, rotulo)
        if k > c:
            ws.merge_cells(start_row=linha, start_column=c, end_row=linha, end_column=k)
        x += w
        c = k + 1
    return linha


def _legenda_item(ws, cel, fn, rotulo):
    if rotulo.startswith("Aviso"):
        c = aviso(ws, cel, rotulo)
        c.fill = PatternFill("solid", fgColor=COR_AVISO_FUNDO)
    elif rotulo.startswith("Título"):
        titulo(ws, cel, rotulo, tamanho=TAM_CORPO)
    elif rotulo.startswith("Cabeçalho"):
        cabecalho(ws, cel, rotulo)
    elif rotulo.startswith("Rótulo"):
        estilo_rotulo_linha(texto(ws, cel, rotulo))
    elif rotulo.startswith("Linha alternada"):
        calculada(ws, cel, rotulo).fill = PatternFill("solid", fgColor=COR_ZEBRA[COR_CALCULADA])
    else:
        fn(ws, cel, rotulo)
    ws[cel].alignment = Alignment(vertical="center", wrap_text=True)


def montar_legendas(wb):
    """Legenda no topo de cada aba (linha 2; na Em Jogo, linha 43), com as larguras finais."""
    for nome in ABAS:
        ws = wb[nome]
        legenda(ws, 43 if nome == "Em Jogo" else 2)


def estilo_rotulo_linha(c):
    """Rótulo da linha (1ª coluna que identifica a linha): negrito e borda direita média."""
    f = c.font
    c.font = Font(name=FONTE, size=f.sz or TAM_CORPO, bold=True, italic=f.i, color=f.color)
    b = c.border
    c.border = Border(left=b.left, top=b.top, bottom=b.bottom, right=_medio)
    return c


# ---------------------------------------------------------------------------
# Mapa lógico -> célula (contrato com os testes)
# ---------------------------------------------------------------------------

class Mapa:
    def __init__(self):
        self.celulas = {}
        self.blocos = {}
        self.listas = {}
        self.entradas = {}      # nome lógico -> {tipo, fonte, amostra, invalido}
        self.avisos = {}        # aba -> [células de aviso]

    @staticmethod
    def ref(aba, cel):
        return f"'{aba}'!{cel}"

    def celula(self, nome, aba, cel):
        if nome in self.celulas:
            raise ValueError(f"nome lógico repetido no mapa: {nome}")
        self.celulas[nome] = self.ref(aba, cel)

    def salvar(self, abas):
        dados = {"gerado_por": "build/gerar_ficha.py", "arquivo": SAIDA_XLSX.name,
                 "abas": abas,
                 "convencao": "celulas: '<aba>.<campo>' -> \"'Aba'!A1\" (aba em minúsculas sem "
                              "acento); blocos: 'dados.<id>'; listas: 'lista.<id>' -> "
                              "\"'Dados'!$X$1:$X$9\"; 'nucleo.*' = números do nível (aba Criação); "
                              "entradas: nome lógico das células que o jogador preenche (tipo, "
                              "valor de amostra válido e inválido para a suíte extremos); "
                              "avisos: células de aviso por aba (painel de avisos)",
                 "celulas": self.celulas, "blocos": self.blocos, "listas": self.listas,
                 "entradas": self.entradas, "avisos": self.avisos,
                 # revisão 2: camada de leitura protegida (célula da camada -> célula lida), sinais
                 # de erro por linha (sinal -> entradas da linha) e contador de erros da Início
                 "leitura": LEITURA, "sinais": SINAIS, "contador": CONTADOR}
        SAIDA_MAPA.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


MAPA = Mapa()


# ---------------------------------------------------------------------------
# Workbook
# ---------------------------------------------------------------------------

def novo_workbook():
    wb = Workbook()
    # Fonte padrão do arquivo = Arial (o openpyxl nasce com Calibri)
    arial = Font(name=FONTE, size=TAM_CORPO)
    wb._fonts = IndexedList([arial])
    wb._named_styles["Normal"].font = arial
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
    primeira = wb.active
    primeira.title = ABAS[0]
    for nome in ABAS[1:]:
        wb.create_sheet(nome)
    return wb


def cabecalho_aba(ws, subtitulo, linha=1):
    """Linha 1: título da aba; linha 2: legenda; linha 3: subtítulo. A aba Em Jogo
    usa `linha` = 42 (o Resumo para o Jogador ocupa A1:D12 e a tela vai até a linha 40)."""
    titulo(ws, f"A{linha}", f"{ws.title} — Explorando Galáxias {VERSAO}", tamanho=TAM_TITULO_ABA, ate="L")
    ws.row_dimensions[linha].height = 24
    # a legenda é montada no fim (montar_legendas), quando as larguras das colunas já existem
    texto(ws, f"A{linha + 1}", "Legenda:", negrito=True)
    texto(ws, f"A{linha + 2}", subtitulo, italico=True).alignment = Alignment(vertical="center", wrap_text=True)
    _mesclar(ws, f"A{linha + 2}", "L")
    MAPA.celula(f"{SLUG[ws.title]}.titulo", ws.title, f"A{linha}")
    MAPA.celula(f"{SLUG[ws.title]}.legenda", ws.title, f"A{linha + 1}")


SUBTITULOS = {
    "Início": "Comece por aqui: como usar a ficha, importar no Google Planilhas e o painel de avisos.",
    "Criação": "Os 12 passos do capítulo 03, de cima para baixo.",
    "Em Jogo": "Tudo que se usa na mesa, numa tela só.",
    "Testes": "As 18 Perícias e os 6 Testes de Resistência com a rolagem pronta.",
    "Habilidades": "As suas Habilidades (até 8) e a Ultimate.",
    "Caminho": "O seu Caminho, as Bênçãos adquiridas e o Memoespírito.",
    "Equipamento": "Arma, armadura, Cone de Luz, Relíquias, inventário e Créditos.",
    "Progressão": "A tabela mestra do nível 1 ao 20, aumentos de Atributo e Ressonâncias.",
    "Regras Rápidas": "Referência de uma página (29.12), condições, Quebra, Energia e tetos.",
    "Dados": "Tabelas do livro usadas pelas fórmulas. Não edite: o gerador reescreve esta aba.",
}


# ---------------------------------------------------------------------------
# Aba Dados
# ---------------------------------------------------------------------------

LINHA_INICIAL_DADOS = 5
COLUNA_LISTAS = 15          # O: listas de validação, uma por coluna
LARGURA_MAX_BLOCO = 12      # A:L


def escrever_dados(ws):
    linha = LINHA_INICIAL_DADOS
    for b in ficha_dados.blocos():
        ncol = len(b["cabecalho"])
        if ncol > LARGURA_MAX_BLOCO:
            raise ValueError(f"bloco {b['id']} com {ncol} colunas (máximo {LARGURA_MAX_BLOCO})")
        ultima = get_column_letter(ncol)
        titulo(ws, f"A{linha}", b["titulo"], ate=ultima)
        lin_titulo = linha
        linha += 1
        for j, nome in enumerate(b["cabecalho"], start=1):
            cabecalho(ws, ws.cell(linha, j).coordinate, nome)
        lin_cab = linha
        linha += 1
        primeira = linha
        for registro in b["linhas"]:
            for j, v in enumerate(registro, start=1):
                calculada(ws, ws.cell(linha, j).coordinate, v if v is not None else "")
            linha += 1
        ultima_linha = linha - 1
        MAPA.blocos[f"dados.{b['id']}"] = {
            "titulo_texto": b["titulo"],
            "titulo": Mapa.ref("Dados", f"A{lin_titulo}"),
            "cabecalho": Mapa.ref("Dados", f"A{lin_cab}:{ultima}{lin_cab}"),
            "intervalo": Mapa.ref("Dados", f"$A${primeira}:${ultima}${ultima_linha}"),
            "primeira_linha": primeira, "ultima_linha": ultima_linha,
            "linhas": len(b["linhas"]),
            "colunas": {nome: get_column_letter(j) for j, nome in enumerate(b["cabecalho"], 1)},
        }
        linha += 1      # linha em branco entre blocos

    # Listas de validação: uma por coluna, a partir de O
    lin_tit = LINHA_INICIAL_DADOS
    titulo(ws, ws.cell(lin_tit - 1, COLUNA_LISTAS).coordinate,
           "Listas de validação (uma por coluna; a fonte está no título)",
           ate=get_column_letter(COLUNA_LISTAS + len(ficha_dados.listas()) - 1))
    for k, l in enumerate(ficha_dados.listas()):
        col = COLUNA_LISTAS + k
        letra = get_column_letter(col)
        fonte_txt = l["fonte"] if not l["fonte"][:1].isdigit() else f"cap. {l['fonte']}"
        cabecalho(ws, f"{letra}{lin_tit}", f"{l['titulo']} — {fonte_txt}")
        for i, v in enumerate(l["valores"], start=1):
            calculada(ws, f"{letra}{lin_tit + i}", v)
        MAPA.listas[f"lista.{l['id']}"] = Mapa.ref(
            "Dados", f"${letra}${lin_tit + 1}:${letra}${lin_tit + len(l['valores'])}")
        ws.column_dimensions[letra].width = 24

    # F e G largos: traços das Raças e resumo das Bênçãos (texto longo do livro) sem linhas gigantes
    larguras = [26, 20, 20, 18, 18, 40, 80, 16, 16, 14, 14, 18]
    for j, w in enumerate(larguras, start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.column_dimensions["M"].width = 3
    ws.column_dimensions["N"].width = 3


# ---------------------------------------------------------------------------
# Infraestrutura das abas de jogo: referências por nome lógico
# ---------------------------------------------------------------------------
#
# As fórmulas são escritas com marcadores «nome.logico». Depois que todas as
# abas estão montadas, resolver_marcadores() troca cada marcador pela célula
# registrada no MAPA: referência local ($B$5) na própria aba e 'Aba'!$B$5 nas
# outras. Assim a ordem de montagem das abas não importa.

REFS = {}                   # nome lógico -> (aba, célula ou intervalo sem $)
_MARCADOR = re.compile(r"«([^»]+)»")
AV = "L"                    # coluna de avisos das abas de construção
DISTANCIA_CABECALHO = 15    # nenhuma linha de dados a mais de 15 linhas do cabeçalho da tabela
COR_DESTAQUE = "FFE699"     # linha do nível atual na Progressão


def T(nome):
    """Marcador de referência para usar dentro de uma fórmula."""
    return f"«{nome}»"


def q(s):
    """Literal de texto numa fórmula (aspas dobradas)."""
    return '"' + str(s).replace('"', '""') + '"'


def slug(s):
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def _abs(cel):
    partes = []
    for p in cel.replace("$", "").split(":"):
        m = re.fullmatch(r"([A-Z]+)(\d+)", p)
        partes.append(f"${m.group(1)}${m.group(2)}")
    return ":".join(partes)


def reg(nome, ws, cel):
    MAPA.celula(nome, ws.title, cel)
    REFS[nome] = (ws.title, cel)
    return cel


def ref(nome, aba):
    a, cel = REFS[nome]
    return _abs(cel) if a == aba else f"'{a}'!{_abs(cel)}"


def resolver_marcadores(wb):
    faltando = set()
    for ws in wb.worksheets:
        for linha in ws.iter_rows():
            for c in linha:
                if isinstance(c.value, str) and "«" in c.value:
                    def troca(m, aba=ws.title):
                        if m.group(1) not in REFS:
                            faltando.add(m.group(1))
                            return "#REF!"
                        return ref(m.group(1), aba)
                    c.value = _MARCADOR.sub(troca, c.value)
    if faltando:
        raise ValueError(f"marcadores sem célula no mapa: {sorted(faltando)}")


def dcol(bloco, coluna):
    """Coluna de um bloco da aba Dados ('Dados'!$X$a:$X$b), pelo nome do cabeçalho."""
    b = MAPA.blocos[f"dados.{bloco}"]
    letra = b["colunas"][coluna]
    return f"'Dados'!${letra}${b['primeira_linha']}:${letra}${b['ultima_linha']}"


def dtab(bloco):
    return MAPA.blocos[f"dados.{bloco}"]["intervalo"]


def dlista(id_):
    return MAPA.listas[f"lista.{id_}"]


def _valores_lista(id_):
    for l in ficha_dados.listas():
        if l["id"] == id_:
            return l["valores"]
    raise KeyError(id_)


def rolagem(expr):
    """'d20+X' / 'd20-X' com o sinal montado por IF (sem TEXT)."""
    return f'"d20"&IF({expr}>=0,"+","")&{expr}'


def sinal(expr):
    return f'IF({expr}>=0,"+","")&{expr}'


def texto_dano(n, face, fixo):
    """'6d6+4', '1d12', '4' (sem dados) — mesma regra do oráculo."""
    return (f'IF({n}<=0,""&{fixo},{n}&"d"&{face}&IF({fixo}>0,"+"&{fixo},'
            f'IF({fixo}<0,""&{fixo},"")))')


def _mesclar(ws, cel, ate):
    if ate:
        linha = ws[cel].row
        ws.merge_cells(f"{cel}:{ate}{linha}")


def _validacao(ws, cel, dv):
    dv.add(cel)
    ws.add_data_validation(dv)


def _dv_lista(ws, cel, fonte, rotulo):
    _validacao(ws, cel, DataValidation(
        type="list", formula1=fonte, allow_blank=True, showErrorMessage=True,
        errorStyle="warning", errorTitle="Fora da lista",
        error=f"{rotulo}: escolha um valor da lista. A ficha pode não reconhecer outro valor."))


def _dv_numero(ws, cel, minimo, maximo, rotulo):
    _validacao(ws, cel, DataValidation(
        type="whole", operator="between", formula1=str(minimo), formula2=str(maximo),
        allow_blank=True, showErrorMessage=True, errorStyle="warning",
        errorTitle="Valor fora da faixa",
        error=f"{rotulo}: use um número inteiro de {minimo} a {maximo}."))


def ent(ws, cel, nome, tipo="texto", fonte=None, amostra=None, invalido=None, rotulo="",
        ate=None, minimo=None, maximo=None):
    """Entrada (fica VAZIA no arquivo). tipo: texto | inteiro | lista (fonte = id de lista
    da aba Dados, ou intervalo local '$N$5:$N$10', ou literal '"a,b"')."""
    entrada(ws, cel)
    _mesclar(ws, cel, ate)
    reg(nome, ws, cel)
    rotulo = rotulo or nome
    info = {"tipo": tipo}
    if tipo == "lista":
        if fonte.startswith('"') or fonte.startswith("$"):
            formula = fonte
            info["fonte"] = fonte
        else:
            formula = dlista(fonte)
            info["fonte"] = f"lista.{fonte}"
            if amostra is None:
                amostra = _valores_lista(fonte)[0]
        _dv_lista(ws, cel, formula, rotulo)
        if invalido is None:
            invalido = "Valor inventado"
    elif tipo in ("inteiro", "decimal"):
        if tipo == "inteiro":
            _dv_numero(ws, cel, minimo, maximo, rotulo)
        else:
            _validacao(ws, cel, DataValidation(
                type="decimal", operator="between", formula1=str(minimo), formula2=str(maximo),
                allow_blank=True, showErrorMessage=True, errorStyle="warning",
                errorTitle="Valor fora da faixa",
                error=f"{rotulo}: use um número de {minimo} a {maximo}."))
        info["minimo"], info["maximo"] = minimo, maximo
        if amostra is None:
            amostra = maximo
        if invalido is None:
            invalido = "abc"
    else:
        if amostra is None:
            amostra = "Teste"
    info["amostra"] = amostra
    info["invalido"] = invalido
    MAPA.entradas[nome] = info
    return cel


def cal(ws, cel, valor, nome=None, negrito=False, ate=None, quebra=False):
    c = calculada(ws, cel, valor, negrito=negrito)
    if quebra:
        # centro vertical: o texto quebrado fica na mesma altura dos números da linha (auditoria visual)
        c.alignment = Alignment(vertical="center", wrap_text=True)
    _mesclar(ws, cel, ate)
    if nome:
        reg(nome, ws, cel)
    return c


def av(ws, cel, nome, formula, ate=None):
    aviso(ws, cel, formula)
    _mesclar(ws, cel, ate)
    reg(nome, ws, cel)
    MAPA.avisos.setdefault(ws.title, []).append(cel)


def aux(ws, cel, formula, nome=None):
    """Célula auxiliar de lista dependente (cinza, à direita)."""
    c = nao_se_aplica(ws, cel, formula)
    if nome:
        reg(nome, ws, cel)
    return c


def rot(ws, cel, s, negrito=False):
    c = texto(ws, cel, s, negrito=negrito)
    c.alignment = Alignment(vertical="center", wrap_text=True)
    return c


def cabecalhos(ws, linha, nomes, coluna=1, altura=40):
    for j, nome in enumerate(nomes, start=coluna):
        if nome:
            cabecalho(ws, f"{get_column_letter(j)}{linha}", nome)
    if altura:
        ws.row_dimensions[linha].height = altura


def formatar_avisos(ws):
    """Fundo rosa nos avisos via formatação condicional LEN>0 (mesma aba, sem '!')."""
    fundo = PatternFill(start_color=COR_AVISO_FUNDO, end_color=COR_AVISO_FUNDO, fill_type="solid")
    for cel in MAPA.avisos.get(ws.title, []):
        ws.conditional_formatting.add(cel, FormulaRule(formula=[f"LEN({cel})>0"], fill=fundo))


def alargar_avisos(ws, de="L", para="K"):
    """Auditoria visual final: aviso na coluna L estreita (152 px) obriga a linha a crescer
    até 95 px pelo aviso mais longo possível (atributos, nível, crença). Onde a coluna K da
    mesma linha está livre, o aviso (e o cabeçalho "Aviso") passa para K e é mesclado K:L,
    o dobro da largura e metade da altura. Chamar antes de resolver os marcadores e de
    formatar os avisos: o nome lógico e a lista de avisos seguem a célula nova."""
    from copy import copy
    import renderizar_ficha as R
    usadas = {cel for aba, cel in REFS.values() if aba == ws.title}
    mescladas = {c for m in ws.merged_cells.ranges for linha in ws.iter_rows(
        min_row=m.min_row, max_row=m.max_row, min_col=m.min_col, max_col=m.max_col) for c in
        (x.coordinate for x in linha)}
    nomes = {cel: n for n, (aba, cel) in REFS.items() if aba == ws.title}
    avisos = MAPA.avisos.get(ws.title, [])

    def pode(r):
        origem, destino = ws[f"{de}{r}"], ws[f"{para}{r}"]
        return not (destino.value is not None or destino.coordinate in usadas
                    or destino.coordinate in mescladas or origem.coordinate in mescladas
                    or _cor(destino) == COR_ENTRADA)

    # numa tabela, ou todas as linhas (e o cabeçalho) mudam, ou nenhuma: a coluna fica alinhada
    travadas = set()
    for tab in R.tabelas(ws):
        grupo = [tab["cab"]] + [r for r in tab["linhas"] if f"{de}{r}" in avisos]
        if ws[f"{de}{tab['cab']}"].value == "Aviso" and not all(pode(r) for r in grupo):
            travadas.update(grupo + list(tab["linhas"]))
    for r in range(1, ws.max_row + 1):
        origem, destino = ws[f"{de}{r}"], ws[f"{para}{r}"]
        eh_aviso = origem.coordinate in avisos
        eh_cab = origem.value == "Aviso" and _cor(origem) == COR_CAB_COLUNA
        if not (eh_aviso or eh_cab) or r in travadas or not pode(r):
            continue
        destino.value = origem.value
        destino._style = copy(origem._style)
        origem.value = None
        ws.merge_cells(f"{para}{r}:{de}{r}")
        if eh_aviso:
            nome = nomes[origem.coordinate]
            REFS[nome] = (ws.title, destino.coordinate)
            MAPA.celulas[nome] = Mapa.ref(ws.title, destino.coordinate)
            avisos[avisos.index(origem.coordinate)] = destino.coordinate


def larguras(ws, mapa_larg):
    for letra, w in mapa_larg.items():
        ws.column_dimensions[letra].width = w


def tem_bencao(nome_bencao):
    """Expressão: a Bênção está num slot já liberado (decisão 2; conta como o oráculo)."""
    return f'(COUNTIF({T("caminho.bencoes.ativas")},{q(nome_bencao)})>0)'


ATRS = list(ficha_dados.ATRIBUTOS)
LV, EF, FX = T("nucleo.nivel"), T("nucleo.eficiencia"), T("nucleo.faixa")
RACA, CAM = T("criacao.raca"), T("criacao.caminho")


def _vantagens_raciais():
    """Vantagens raciais por Perícia/TR a partir do texto transcrito do capítulo 05.
    Devolve (pericias, tr, tr_condicional, morrendo) com listas de Raças."""
    nomes_tr = _valores_lista("tr")
    nomes_per = _valores_lista("pericias")
    per, tr, cond, morr = {}, {}, {}, []
    for v in ficha_dados.TRANSCRITO["vantagens_raciais"]:
        onde, raca = v["onde"], v["raca"]
        if "todos os 6 Testes de Resistência" in onde:
            for t in nomes_tr:
                tr.setdefault(t, []).append(raca)
            if "Morrendo" in onde:
                morr.append((raca, "23.5"))
            continue
        tokens = [x.strip() for x in re.split(r",| e ", onde)]
        for t in nomes_tr:
            for tok in tokens:
                if tok == t:
                    tr.setdefault(t, []).append(raca)
                elif tok.startswith(t + " ") and "(condicional)" in onde:
                    cond.setdefault(t, []).append(raca)
        for p in nomes_per:
            if p in tokens:
                per.setdefault(p, []).append(raca)
    # 23.5 (v1.1, D3): o quadro "Quem rola o Teste de Morrendo com Vantagem" nomeia as três
    # Raças (Xianzhouíta, Vulpes e Avginiano); lido do livro, não deduzido
    for raca in ficha_dados.racas_morrendo_vantagem():
        if raca not in [m[0] for m in morr]:
            morr.append((raca, "23.5"))
    return per, tr, cond, morr


def _ou_raca(racas):
    return "OR(" + ",".join(f"{RACA}={q(x)}" for x in racas) + ")"


# ---------------------------------------------------------------------------
# Aba Criação — os 12 passos do capítulo 03
# ---------------------------------------------------------------------------

class Cursor:
    """Linha corrente de uma aba montada de cima para baixo."""

    def __init__(self, ws, linha=5):
        self.ws = ws
        self.r = linha

    def titulo(self, texto_titulo, ate=AV):
        titulo(self.ws, f"A{self.r}", texto_titulo, ate=ate)
        self.r += 1

    def passo(self, texto_titulo, ate=AV):
        self.r += 1
        self.titulo(texto_titulo, ate=ate)


def criacao_cabecalho(c):
    ws = c.ws
    c.titulo("Personagem")
    r = c.r
    rot(ws, f"A{r}", "Nome do personagem")
    ent(ws, f"B{r}", "criacao.nome", ate="J", rotulo="Nome")
    r += 1
    rot(ws, f"A{r}", "Jogador")
    ent(ws, f"B{r}", "criacao.jogador", ate="J", rotulo="Jogador")
    r += 1
    rot(ws, f"A{r}", "Nível atual (1 a 20)")
    ent(ws, f"B{r}", "criacao.nivel", "inteiro", minimo=1, maximo=20, amostra=5, rotulo="Nível")
    niv = T("criacao.nivel")
    cal(ws, f"C{r}", f'="Usado nas contas: nível "&{LV}', ate="J")
    av(ws, f"{AV}{r}", "criacao.aviso.nivel",
       f'=IF({niv}="","",IF(ISNUMBER({niv}),IF(OR({niv}<1,{niv}>20),'
       f'"Nível fora de 1 a 20: a ficha conta com o nível "&{LV},'
       f'IF({niv}<>INT({niv}),"Nível precisa ser inteiro: a ficha conta com o nível "&{LV},"")),'
       f'"Nível precisa ser um número de 1 a 20: a ficha conta com o nível 1"))')
    r += 1
    rot(ws, f"A{r}", "Nº de jogadores na mesa")
    ent(ws, f"B{r}", "criacao.jogadores", "inteiro", minimo=1, maximo=6, amostra=4, invalido=0,
        rotulo="Nº de jogadores")
    jg = T("criacao.jogadores")
    cal(ws, f"C{r}", f'="PH do grupo: máximo "&{T("nucleo.ph_max")}&", começa o combate com "'
                     f'&{T("nucleo.ph_inicio")}', ate="J")
    av(ws, f"{AV}{r}", "criacao.aviso.jogadores",
       f'=IF({jg}="","",IF(ISNUMBER({jg}),IF(OR({jg}<1,{jg}>6),'
       f'"Nº de jogadores fora de 1 a 6: a ficha conta com "&{T("nucleo.jogadores")},'
       f'IF(OR({jg}<3,{jg}>6),"Fora da tabela do livro (3 a 6 jogadores): o PH segue a mesma regra",'
       f'"")),"Nº de jogadores precisa ser um número de 1 a 6"))')
    r += 1
    rot(ws, f"A{r}", "Método de atributos (o Mestre escolhe)")
    ent(ws, f"B{r}", "criacao.metodo", "lista", "metodo", rotulo="Método de atributos")
    met = T("criacao.metodo")
    cal(ws, f"C{r}", f'=IF({met}="","Array oficial (15, 14, 13, 12, 10, 8) ou Compra de Pontos (28)",'
                     f'IF({met}="Array oficial","Distribua 15, 14, 13, 12, 10 e 8, um em cada Atributo",'
                     f'"Todos começam em 8; gaste até 28 pontos"))', ate="J")
    av(ws, f"{AV}{r}", "criacao.aviso.metodo",
       f'=IF({met}="","",IF(COUNTIF({dlista("metodo")},{met})=0,"Método fora da lista",""))')
    r += 1
    c.r = r


def criacao_nucleo(c):
    """Números do nível usados por todas as abas (registrados como 'nucleo.*')."""
    ws = c.ws
    niv, jg = T("criacao.nivel"), T("criacao.jogadores")
    c.passo("Números do seu nível (automático) — 26.2 a 26.6")
    r = c.r

    def mestra(col):
        return dcol("mestra", col)

    grade = [
        [("nivel", "Nível usado", f'=IF(ISNUMBER({niv}),MAX(1,MIN(20,INT({niv}))),1)'),
         ("faixa", "Faixa (1 a 5)", f"=INT(({LV}-1)/4)+1"),
         ("eficiencia", "Eficiência", f"=2+INT(({LV}-1)/3)"),
         ("eficacia", "Eficácia", f"=2*{EF}"),
         ("slots_eficacia_pericias", "Slots de Eficácia em Perícias",
          f"=INDEX({mestra('Eficácia: Perícias')},{LV})"),
         ("slots_eficacia_tr", "Slots de Eficácia em Testes de Resistência",
          f"=INDEX({mestra('Eficácia: Testes de Resistência')},{LV})"),
         ("especializacao", "Especialização de Combate", f"=INDEX({mestra('Especialização')},{LV})"),
         ("teto_rd", "Teto de RD", f"=INDEX({mestra('Teto de RD')},{LV})"),
         ("teto_temporarios", "Teto de PV temporários", f"=3*{EF}"),
         ("teto_bonus", "Teto de bônus somado", f"=IF({LV}<=9,3,IF({LV}<=15,4,5))"),
         ("teto_penalidade", "Teto de penalidade somada", f"=-{T('nucleo.teto_bonus')}"),
         ("bencaos", "Bênçãos possuídas", f"=INDEX({mestra('Bênçãos')},{LV})")],
        [("habilidades_conhecidas", "Habilidades conhecidas",
          f"=INDEX({mestra('Habilidades conhecidas')},{LV})"),
         ("nivel_max_habilidade", "Nível máx. de Habilidade",
          f"=INDEX({mestra('Nível máx. de Habilidade')},{LV})"),
         ("reescreve", "Reescreve 1 Habilidade por nível",
          f"=INDEX({mestra('Reescreve 1 por nível')},{LV})"),
         ("dados_ab", "Dados de Ataque Básico", f"=INDEX({mestra('Dados de Ataque Básico')},{LV})"),
         ("ph_max", "PH do grupo: máximo",
          f"=1+{T('nucleo.jogadores')}+IF({LV}>=17,2,IF({LV}>=9,1,0))"),
         ("ph_inicio", "PH do grupo: início", f"={T('nucleo.ph_max')}-2"),
         ("ph_geracao", "PH por Ataque Básico que acerta", f"=IF({LV}<=8,1,2)"),
         ("ultimate_equivalente", "Ultimate: Nível equivalente",
          f"=INDEX({dcol('ultimate', 'Nível equivalente')},{FX})"),
         ("cone_maximo", "Cone de Luz: Nível máximo", f"={FX}"),
         ("tier_reliquia", "Tier de Relíquia (1 a 4)",
          f"=IF({LV}<=6,1,IF({LV}<=12,2,IF({LV}<=17,3,4)))"),
         ("pontos_memo", "Pontos do Memoespírito", f"=12+INT({LV}/2)"),
         ("dt_fraqueza", "DT para descobrir Fraqueza",
          f"=INDEX({dcol('dt_fraqueza', 'DT')},{FX})")],
    ]
    for grupo in grade:
        cabecalhos(ws, r, [g[1] for g in grupo])
        for j, (campo, _, formula) in enumerate(grupo, start=1):
            v = cal(ws, f"{get_column_letter(j)}{r + 1}", formula, nome=f"nucleo.{campo}", negrito=True)
            # grade de consulta: cabeçalho e número centrados na mesma coluna (auditoria visual)
            v.alignment = Alignment(horizontal="center", vertical="center")
            ws.cell(r, j).alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        r += 2
    rot(ws, f"A{r}", "Nº de jogadores usado (vazio = 4)")
    cal(ws, f"B{r}", f'=IF(ISNUMBER({jg}),MAX(1,MIN(6,INT({jg}))),4)', nome="nucleo.jogadores",
        negrito=True)
    rot(ws, f"C{r}", "Aumento de Atributo neste nível?")
    _mesclar(ws, f"C{r}", "D")
    cal(ws, f"E{r}", f"=INDEX({mestra('Aumento de Atributo')},{LV})",
        nome="nucleo.aumento_neste_nivel", negrito=True)
    c.r = r + 1


def criacao_passos_1_a_3(c):
    ws = c.ws
    c.passo("Passo 1 — Conceito e Propósito de Vida")
    r = c.r
    rot(ws, f"A{r}", "Quem é esse sujeito? (conceito em uma frase)")
    ent(ws, f"B{r}", "criacao.conceito", ate="J", rotulo="Conceito")
    r += 1
    rot(ws, f"A{r}", "Propósito de Vida (objetivo de longo prazo)")
    ent(ws, f"B{r}", "criacao.proposito", ate="J", rotulo="Propósito de Vida")
    r += 1
    rot(ws, f"A{r}", "Em que você acredita (recarrega o Esforço; só Humano)")
    ent(ws, f"B{r}", "criacao.crenca_esforco", ate="J", rotulo="Crença do Esforço")
    av(ws, f"{AV}{r}", "criacao.aviso.crenca_esforco",
       f'=IF(AND({RACA}<>"Humano",LEN({T("criacao.crenca_esforco")})>0),'
       f'"O Esforço é traço do Humano: esta linha só vale para Humano","")')
    c.r = r + 1

    # --- Passo 2 ------------------------------------------------------------------
    c.passo("Passo 2 — Raça (capítulo 05)")
    r = c.r
    modo, a1, a2 = T("criacao.raca.modo"), T("criacao.raca.atributo1"), T("criacao.raca.atributo2")
    op1, op2, esc = T("criacao.raca.opcao1"), T("criacao.raca.opcao2"), T("criacao.raca.escolhido")
    m_raca = f"MATCH({RACA},{dcol('racas', 'Raça')},0)"
    rot(ws, f"A{r}", "Raça")
    ent(ws, f"B{r}", "criacao.raca", "lista", "racas", invalido="Marciano", rotulo="Raça")
    # ""& força texto: a Opção 2 vazia (Raça de opção única) vira "" e não 0
    aux(ws, f"O{r}", f'=IF({RACA}="","",IFERROR(""&INDEX({dcol("racas", "Opção 1 do +2")},{m_raca}),""))',
        nome="criacao.raca.opcao1")
    aux(ws, f"O{r + 1}", f'=IF({RACA}="","",IFERROR(""&INDEX({dcol("racas", "Opção 2 do +2")},{m_raca}),""))',
        nome="criacao.raca.opcao2")
    aux(ws, f"O{r + 2}", f'=IF(OR({RACA}="",{RACA}="Humano"),"",IF({op2}="",IF(OR({a1}="",{a1}={op1}),'
                         f'{op1},""),IF(OR({a1}={op1},{a1}={op2}),{a1},"")))', nome="criacao.raca.escolhido")
    for k in range(6):
        outro = op1 if k == 0 else op2 if k == 1 else '""'
        aux(ws, f"N{r + k}", f'=IF({RACA}="Humano",INDEX({dlista("atributos")},{k + 1}),{outro})')
    lista_raca = f"$N${r}:$N${r + 5}"
    # 05 (v1.2): o modo "+2 em um, ou +1 em cada" vale para todas as Raças. Fora do Humano, o
    # "+1 em cada" é determinístico (os dois são o par da Raça), então nem pede escolha
    cal(ws, f"C{r}", f'=IF({RACA}="","Escolha a Raça",IF({RACA}="Humano",IF({modo}="Dois Atributos (+1 cada)",'
                     f'"Bônus racial: +1 em "&IF({a1}="","?",{a1})&" e +1 em "&IF({a2}="","?",{a2}),'
                     f'IF({a1}="","Escolha onde vai o +2 (qualquer Atributo)","Bônus racial: +2 em "&{a1})),'
                     f'IF({op1}="","Raça fora da lista do capítulo 05",'
                     f'IF({modo}="Dois Atributos (+1 cada)","Bônus racial: +1 em "&{op1}&" e +1 em "&{op2},'
                     f'IF({esc}="","Escolha onde vai o +2: "&{op1}&" ou "&{op2},'
                     f'"Bônus racial: +2 em "&{esc})))))',
        nome="criacao.raca.status", ate="J")
    av(ws, f"{AV}{r}", "criacao.aviso.raca",
       f'=IF({RACA}="","",IF(COUNTIF({dlista("racas")},{RACA})=0,"Raça fora da lista do capítulo 05",""))')
    r += 1
    rot(ws, f"A{r}", "Bônus racial: +2 em um, ou +1 em cada")
    ent(ws, f"B{r}", "criacao.raca.modo", "lista", "modo_humano", rotulo="Bônus racial")
    rot(ws, f"C{r}", "Vale para todas as Raças. Com +1 em cada, os dois Atributos são os da sua "
                     "Raça — o Humano escolhe entre os seis.")
    _mesclar(ws, f"C{r}", "J")
    # 05 (v1.2): o modo deixou de ser exclusivo do Humano, então o aviso trocou de assunto —
    # fora do Humano, "+1 em cada" não pede escolha, e um atributo digitado ali é ignorado
    av(ws, f"{AV}{r}", "criacao.aviso.raca_modo",
       f'=IF(AND({modo}="Dois Atributos (+1 cada)",{RACA}<>"",{RACA}<>"Humano",OR({a1}<>"",{a2}<>"")),'
       f'"Com +1 em cada, os dois Atributos são os da sua Raça: não precisa escolher","")')
    r += 1
    rot(ws, f"A{r}", "Atributo do +2 (Humano com Dois Atributos: o 1º)")
    ent(ws, f"B{r}", "criacao.raca.atributo1", "lista", lista_raca, amostra="Poder",
        rotulo="Atributo do bônus racial")
    rot(ws, f"C{r}", "A lista mostra só as opções da sua Raça.")
    _mesclar(ws, f"C{r}", "J")
    av(ws, f"{AV}{r}", "criacao.aviso.raca_atributo1",
       f'=IF(AND({RACA}="Humano",{modo}="Dois Atributos (+1 cada)",{a1}<>"",{a1}={a2}),'
       f'"+1 em dois exige atributos diferentes: contou só um +1",'
       f'IF(AND({RACA}<>"",{RACA}<>"Humano",{op1}<>"",{a1}<>"",{esc}=""),'
       f'"Bônus fora das opções da Raça: "&{op1}&IF({op2}="",""," ou "&{op2}),""))')
    r += 1
    rot(ws, f"A{r}", "Atributo 2 (só Humano com Dois Atributos)")
    ent(ws, f"B{r}", "criacao.raca.atributo2", "lista", "atributos", rotulo="Atributo 2")
    av(ws, f"{AV}{r}", "criacao.aviso.raca_atributo2",
       f'=IF(AND({a2}<>"",OR({RACA}<>"Humano",{modo}<>"Dois Atributos (+1 cada)")),'
       f'"Atributo 2 só vale para Humano com Dois Atributos (+1 cada)","")')
    r += 1
    rot(ws, f"A{r}", "Traços (resumo)")
    cal(ws, f"B{r}", f'=IF({RACA}="","",IFERROR(INDEX({dcol("racas", "Traços (resumo)")},{m_raca}),""))',
        nome="criacao.raca.tracos", ate="J", quebra=True)
    ws.row_dimensions[r].height = 30
    r += 1
    rot(ws, f"A{r}", "Traços (texto inteiro do livro)")
    cal(ws, f"B{r}", f'=IF({RACA}="","",IFERROR(INDEX({dcol("racas", "Traços (texto do livro)")},'
                     f'{m_raca}),""))', nome="criacao.raca.tracos_texto", ate="J", quebra=True)
    ws.row_dimensions[r].height = 30   # ajustar_layout cresce até o texto de Raça mais longo caber
    c.r = r + 1

    # --- Passo 3 ------------------------------------------------------------------
    c.passo("Passo 3 — Caminho (capítulo 06)")
    r = c.r
    rot(ws, f"A{r}", "Caminho")
    ent(ws, f"B{r}", "criacao.caminho", "lista", "caminhos", invalido="A Ordem", rotulo="Caminho")
    cal(ws, f"C{r}", f'=IF({CAM}="","Escolha o Caminho","Aeon: "&{do_caminho("Aeon")})', ate="J")
    av(ws, f"{AV}{r}", "criacao.aviso.caminho",
       f'=IF({CAM}="","",IF(COUNTIF({dlista("caminhos")},{CAM})=0,"Caminho fora da lista do capítulo 06",""))')
    r += 1
    rot(ws, f"A{r}", "Aeon")
    cal(ws, f"B{r}", f"={do_caminho('Aeon')}", nome="criacao.caminho.aeon", ate="D")
    r += 1
    rot(ws, f"A{r}", "A ideia, em uma frase")
    cal(ws, f"B{r}", f"={do_caminho('A ideia, em uma frase')}", nome="criacao.caminho.ideia", ate="J")
    r += 1
    rot(ws, f"A{r}", "Índice de vitalidade N (entra no PV)")
    cal(ws, f"B{r}", f"={do_caminho('N', '0')}", nome="criacao.caminho.n", negrito=True)
    r += 1
    rot(ws, f"A{r}", "Bônus de Velocidade do Caminho")
    cal(ws, f"B{r}", f"={do_caminho('Bônus de VEL', '0')}", nome="criacao.caminho.vel", negrito=True)
    r += 1
    rot(ws, f"A{r}", "As 3 Perícias do Caminho (Eficiência de graça)")
    for k, (col, ate) in enumerate((("B", "C"), ("D", "E"), ("F", "G")), start=1):
        cal(ws, f"{col}{r}", f"={do_caminho(f'Perícia {k}')}", nome=f"criacao.caminho.pericia{k}", ate=ate)
    r += 1
    rot(ws, f"A{r}", "Atributo de Habilidade que o Caminho permite")
    cal(ws, f"B{r}", f"={do_caminho('Atributo de Habilidade')}", ate="J")
    r += 1
    rot(ws, f"A{r}", "Recurso próprio (detalhes na aba Caminho)")
    cal(ws, f"B{r}", f"={do_caminho('Recurso próprio')}", nome="criacao.caminho.recurso", ate="J")
    c.r = r + 1


def do_caminho(coluna, vazio='""'):
    """INDEX/MATCH de uma coluna do bloco Caminhos (Dados) pelo Caminho escolhido."""
    m_cam = f"MATCH({CAM},{dcol('caminhos', 'Caminho')},0)"
    return f'IF({CAM}="",{vazio},IFERROR(INDEX({dcol("caminhos", coluna)},{m_cam}),{vazio}))'


def bonus_de(atributo):
    return T(f"criacao.atributo.{slug(atributo)}.bonus")


def criacao_passo_4(c):
    ws = c.ws
    met = T("criacao.metodo")
    modo, a1, a2 = T("criacao.raca.modo"), T("criacao.raca.atributo1"), T("criacao.raca.atributo2")
    esc = T("criacao.raca.escolhido")
    # v1.2: o "+1 em cada" das Raças não-Humanas soma nos dois Atributos do par delas
    op1, op2 = T("criacao.raca.opcao1"), T("criacao.raca.opcao2")
    c.passo("Passo 4 — Atributos (teto 15 antes da Raça; teto 20 sempre)")
    r = c.r
    cabecalhos(ws, r, ["Atributo", "Distribuído (preencha)", "Raça (automático)",
                       "Aumentos (aba Progressão)", "Valor atual", "Bônus atual",
                       "Valor na criação (com Raça)", "Bônus na criação", "Custo na Compra de Pontos",
                       "Valor usado (8 a 20)"])
    cabecalho(ws, f"{AV}{r}", "Aviso")
    r += 1
    p_a1, p_s1 = T("progressao.aumentos.atributo1"), T("progressao.aumentos.soma1")
    p_a2, p_s2 = T("progressao.aumentos.atributo2"), T("progressao.aumentos.soma2")
    r0 = r
    for a in ATRS:
        s = slug(a)
        base = f"criacao.atributo.{s}"
        texto(ws, f"A{r}", a, negrito=True)
        ent(ws, f"B{r}", f"{base}.distribuido", "inteiro", minimo=8, maximo=15, amostra=15,
            invalido=25, rotulo=a)
        B, Cr, D, J = (T(f"{base}.distribuido"), T(f"{base}.raca"), T(f"{base}.aumentos"),
                       T(f"{base}.base"))
        E, G = T(f"{base}.atual"), T(f"{base}.criacao")
        # 05 (v1.2): "+1 em cada" vale para todas. No Humano os dois Atributos são escolhidos;
        # nas outras Raças são o par delas (op1 e op2), que já são diferentes por construção
        cal(ws, f"C{r}", f'=IF({RACA}="Humano",IF({modo}="Dois Atributos (+1 cada)",({a1}={q(a)})*1+'
                         f'AND({a2}={q(a)},{a2}<>{a1})*1,({a1}={q(a)})*2),'
                         f'IF({modo}="Dois Atributos (+1 cada)",({op1}={q(a)})*1+({op2}={q(a)})*1,'
                         f'IF({esc}={q(a)},2,0)))',
            nome=f"{base}.raca")
        cal(ws, f"D{r}", f"=SUMIF({p_a1},{q(a)},{p_s1})+SUMIF({p_a2},{q(a)},{p_s2})",
            nome=f"{base}.aumentos")
        cal(ws, f"E{r}", f"=MIN(20,{J}+{Cr}+{D})", nome=f"{base}.atual", negrito=True)
        cal(ws, f"F{r}", f"=IF({E}<15,VLOOKUP({E},{dtab('bonus_atributo')},2,FALSE),INT(({E}-15)/2)+3)",
            nome=f"{base}.bonus", negrito=True)
        cal(ws, f"G{r}", f"=MIN(20,{J}+{Cr})", nome=f"{base}.criacao")
        cal(ws, f"H{r}", f"=IF({G}<15,VLOOKUP({G},{dtab('bonus_atributo')},2,FALSE),INT(({G}-15)/2)+3)",
            nome=f"{base}.bonus_criacao")
        cal(ws, f"I{r}", f'=IF({met}="Compra de Pontos",VLOOKUP(MAX(8,MIN(15,{J})),'
                         f'{dtab("compra")},2,FALSE),"")', nome=f"{base}.custo")
        cal(ws, f"J{r}", f"=IF(ISNUMBER({B}),MAX(8,MIN(20,INT({B}))),8)", nome=f"{base}.base")
        av(ws, f"{AV}{r}", f"criacao.aviso.atributo.{s}",
           f'=IF({B}="","",IF(ISNUMBER({B}),IF(OR({B}<8,{B}>20),"Fora de 8 a 20: a ficha conta com "'
           f'&{J}&". ","")&IF({B}>15,"Acima de 15 antes da Raça. ",""),"Precisa ser um número. "))'
           f'&IF(AND({D}>0,{J}+{Cr}+{D}>20),"Aumento desperdiçado: passou do teto 20.","")')
        r += 1
    for nome, col in (("nomes", "A"), ("distribuido", "B"), ("atual", "E"), ("bonus", "F"),
                      ("custo", "I")):
        reg(f"criacao.atributos.{nome}", ws, f"{col}{r0}:{col}{r - 1}")
    dist, custos = T("criacao.atributos.distribuido"), T("criacao.atributos.custo")
    preenchidos = "(" + "+".join(f"ISNUMBER({T(f'criacao.atributo.{slug(a)}.distribuido')})*1"
                                 for a in ATRS) + ")"
    array = (15, 14, 13, 12, 10, 8)
    ok_array = "AND(" + ",".join(f"COUNTIF({dist},{v})=1" for v in array) + ")"
    faltando = "&".join(f'IF(COUNTIF({dist},{v})=0,"{v} ","")' for v in array)
    repetido = "&".join(f'IF(COUNTIF({dist},{v})>1,"{v} ","")' for v in array)
    rot(ws, f"A{r}", "Conferência do array oficial")
    cal(ws, f"B{r}", f'=IF({met}<>"Array oficial","",IF({preenchidos}<6,"Valores que faltam para fechar o array: "'
                     f'&(6-{preenchidos}),IF({ok_array},"OK: cada valor usado uma vez",'
                     f'"Confira o aviso ao lado")))', nome="criacao.array.status", ate="J")
    av(ws, f"{AV}{r}", "criacao.aviso.array",
       f'=IF(AND({met}="Array oficial",{preenchidos}=6),IF({ok_array},"",'
       f'"Array oficial: use 15, 14, 13, 12, 10 e 8 uma vez cada. Falta: "&{faltando}&"· Repetido: "'
       f'&{repetido}),"")')
    r += 1
    rot(ws, f"A{r}", "Compra de Pontos: gastos de 28")
    cal(ws, f"B{r}", f'=IF({met}="Compra de Pontos",SUM({custos}),"")', nome="criacao.compra.gasto",
        negrito=True)
    rot(ws, f"C{r}", "Sobram:")
    cal(ws, f"D{r}", f'=IF({met}="Compra de Pontos",28-SUM({custos}),"")', nome="criacao.compra.sobram",
        negrito=True)
    av(ws, f"{AV}{r}", "criacao.aviso.compra",
       f'=IF(AND({met}="Compra de Pontos",SUM({custos})>28),"Compra de Pontos passou de 28 ("'
       f'&SUM({custos})&" pontos)","")')
    c.r = r + 1


def criacao_passos_5_6(c):
    ws = c.ws
    c.passo("Passo 5 — Atributo de Habilidade (fixo pela campanha)")
    r = c.r
    oph1, oph2 = T("criacao.atributo_habilidade.opcao1"), T("criacao.atributo_habilidade.opcao2")
    # ""& força texto: a célula vazia da Dados (Caminho de opção única) vira "" e não 0
    m_cam = f"MATCH({CAM},{dcol('caminhos', 'Caminho')},0)"
    for k in (1, 2):
        aux(ws, f"N{r + k - 1}", f'=IF({CAM}="","",IFERROR(""&INDEX({dcol("caminhos", f"Opção {k}")},{m_cam}),""))',
            nome=f"criacao.atributo_habilidade.opcao{k}")
    rot(ws, f"A{r}", "Atributo de Habilidade")
    ent(ws, f"B{r}", "criacao.atributo_habilidade", "lista", f"$N${r}:$N${r + 1}", amostra="Poder",
        rotulo="Atributo de Habilidade")
    ah = T("criacao.atributo_habilidade")
    rot(ws, f"C{r}", "Usado:")
    cal(ws, f"D{r}", f'=IF({oph1}="","",IF(AND({ah}="",{oph2}=""),{oph1},IF(AND({ah}<>"",'
                     f'OR({ah}={oph1},{ah}={oph2})),{ah},"")))', nome="criacao.atributo_habilidade.usado",
        negrito=True, ate="E")
    ahu = T("criacao.atributo_habilidade.usado")
    av(ws, f"{AV}{r}", "criacao.aviso.atributo_habilidade",
       f'=IF(AND({oph1}<>"",{ahu}=""),IF({ah}="","Escolha o Atributo de Habilidade: "&{oph1}&" ou "'
       f'&{oph2},"Fora do que o Caminho permite: "&{oph1}&IF({oph2}="",""," ou "&{oph2})),"")')
    r += 1
    rot(ws, f"A{r}", "Bônus do Atributo de Habilidade")
    cal(ws, f"B{r}", f'=IF({ahu}="",0,IFERROR(INDEX({T("criacao.atributos.bonus")},'
                     f'MATCH({ahu},{T("criacao.atributos.nomes")},0)),0))', nome="criacao.bonus_habilidade",
        negrito=True)
    bah = T("criacao.bonus_habilidade")
    r += 1
    rot(ws, f"A{r}", "DT das suas Habilidades (8 + Bônus + Eficiência)")
    cal(ws, f"B{r}", f"=8+{bah}+{EF}", nome="criacao.dt", negrito=True)
    r += 1
    rot(ws, f"A{r}", "Teste de Ataque das Habilidades e da Ultimate")
    cal(ws, f"B{r}", f"={bah}+{EF}+{T('nucleo.especializacao')}+{T('criacao.extra.ataque')}",
        nome="criacao.ataque_habilidade", negrito=True)
    cal(ws, f"C{r}", "=" + rolagem(T("criacao.ataque_habilidade")),
        nome="criacao.ataque_habilidade.rolagem", negrito=True)
    rot(ws, f"D{r}", "Bônus + Eficiência + Especialização + equipamento (aba Equipamento)")
    _mesclar(ws, f"D{r}", "J")
    c.r = r + 1

    c.passo("Passo 6 — Elemento (capítulo 20)")
    r = c.r
    el = T("criacao.elemento")
    m_el = f"MATCH({el},{dcol('elementos', 'Elemento')},0)"
    rot(ws, f"A{r}", "Elemento")
    ent(ws, f"B{r}", "criacao.elemento", "lista", "elementos", amostra="Fogo", invalido="Plasma",
        rotulo="Elemento")
    rot(ws, f"C{r}", "Suas Habilidades e a Ultimate causam dano deste Elemento.")
    _mesclar(ws, f"C{r}", "J")
    av(ws, f"{AV}{r}", "criacao.aviso.elemento",
       f'=IF({el}="","",IF(COUNTIF({dlista("elementos")},{el})=0,"Elemento fora da lista do capítulo 20",""))')
    r += 1
    nq = f"INDEX({dcol('elementos', 'Dados do Dano de Quebra')},{m_el})"
    fq = f"INDEX({dcol('elementos', 'Face')},{m_el})"
    mq = f"INDEX({dcol('elementos', 'Multiplicador da Eficiência')},{m_el})"
    rot(ws, f"A{r}", "Efeito de Quebra")
    cal(ws, f"B{r}", f'=IF({el}="","",IFERROR(INDEX({dcol("elementos", "Efeito de Quebra")},{m_el}),""))',
        nome="criacao.quebra.efeito", ate="D")
    r += 1
    rot(ws, f"A{r}", "Dano de Quebra (20.5)")
    cal(ws, f"B{r}", f'=IF({el}="","",IFERROR({texto_dano(nq, fq, f"{mq}*{EF}")},""))',
        nome="criacao.quebra.texto", negrito=True)
    rot(ws, f"C{r}", "média")
    cal(ws, f"D{r}", f'=IF({el}="","",IFERROR(INT({nq}*({fq}+1)/2)+{mq}*{EF},""))',
        nome="criacao.quebra.media", negrito=True)
    c.r = r + 1


def criacao_passo_7(c):
    ws = c.ws
    c.passo("Passo 7 — Perícias (3 do Caminho + 2 + Bônus de Sincronia escolhidas, mínimo 2)")
    r = c.r
    rot(ws, f"A{r}", "Sintonia usa (fixo na criação)")
    ent(ws, f"B{r}", "criacao.sintonia", "lista", "sintonia", amostra="Sincronia", rotulo="Sintonia")
    sint = T("criacao.sintonia")
    rot(ws, f"C{r}", "Usado:")
    cal(ws, f"D{r}", f'=IF({sint}="Sincronia","Sincronia","Discernimento")', nome="criacao.sintonia.usada",
        ate="E")
    r += 1
    rot(ws, f"A{r}", "Perícias escolhidas permitidas (Sincronia da criação; Humano +1)")
    # 04.5 + 05 (v1.2): piso de 2, e o traço passivo Vocação Livre dá ao Humano 1 Perícia a mais
    cal(ws, f"B{r}", f"=MAX(2,2+{T('criacao.atributo.sincronia.bonus_criacao')})"
                     f'+IF({RACA}="Humano",1,0)',
        nome="criacao.pericias.permitidas", negrito=True)
    perm = T("criacao.pericias.permitidas")
    r += 1
    r_cont = r
    r += 1
    nomes_cab = ["Perícia", "Atributo", "Do Caminho?", "Escolhida (preencha Sim)", "Eficiência (automático)",
                 "Origem"]
    r0 = r + 1
    per1, per2, per3 = (T(f"criacao.caminho.pericia{k}") for k in (1, 2, 3))
    for k, p in enumerate(_valores_lista("pericias"), start=1):
        if k - 1 in GRUPOS_PERICIAS:
            # cabeçalho repetido a cada grupo de Atributos (sem linhas congeladas)
            cabecalhos(ws, r, [f"Perícia ({GRUPOS_PERICIAS[k - 1]})"] + nomes_cab[1:], altura=30)
            cabecalho(ws, f"{AV}{r}", "Aviso")
            r += 1
        base = f"criacao.pericia.{slug(p)}"
        texto(ws, f"A{r}", p, negrito=True)
        if p == "Sintonia":
            cal(ws, f"B{r}", f"={T('criacao.sintonia.usada')}", nome=f"{base}.atributo")
        else:
            cal(ws, f"B{r}", f"=INDEX({dcol('pericias', 'Atributo')},{k})", nome=f"{base}.atributo")
        cal(ws, f"C{r}", f'=IF(OR({per1}={q(p)},{per2}={q(p)},{per3}={q(p)}),"Sim","Não")',
            nome=f"{base}.caminho")
        ent(ws, f"D{r}", f"{base}.escolhida", "lista", "sim_nao", rotulo=p)
        Cc, D = T(f"{base}.caminho"), T(f"{base}.escolhida")
        cal(ws, f"E{r}", f'=IF(OR({Cc}="Sim",AND({D}="Sim",COUNTIF($D${r0}:D{r},"Sim")<={perm})),"Sim","Não")',
            nome=f"{base}.eficiencia", negrito=True)
        E = T(f"{base}.eficiencia")
        cal(ws, f"F{r}", f'=IF({Cc}="Sim","Caminho",IF({E}="Sim","Escolhida",""))', nome=f"{base}.origem")
        av(ws, f"{AV}{r}", f"criacao.aviso.pericia.{slug(p)}",
           f'=IF({D}<>"Sim","",IF({Cc}="Sim","Já vem do Caminho: escolha outra",'
           f'IF({E}="Não","Acima do permitido ("&{perm}&"): esta fica sem Eficiência","")))')
        r += 1
    reg("criacao.pericias.escolhida", ws, f"D{r0}:D{r - 1}")
    reg("criacao.pericias.eficiencia", ws, f"E{r0}:E{r - 1}")
    rot(ws, f"A{r_cont}", "Escolhidas / com Eficiência no total")
    cal(ws, f"B{r_cont}", f'=COUNTIF({T("criacao.pericias.escolhida")},"Sim")',
        nome="criacao.pericias.escolhidas", negrito=True)
    rot(ws, f"C{r_cont}", "com Eficiência:")
    cal(ws, f"D{r_cont}", f'=COUNTIF({T("criacao.pericias.eficiencia")},"Sim")',
        nome="criacao.pericias.com_eficiencia", negrito=True)
    av(ws, f"{AV}{r_cont}", "criacao.aviso.pericias",
       f'=IF({T("criacao.pericias.escolhidas")}>{perm},"Perícias escolhidas acima do permitido ("'
       f'&{perm}&"): as últimas ficam sem Eficiência","")')
    c.r = r


def criacao_passo_8(c):
    ws = c.ws
    c.passo("Passo 8 — As cinco estatísticas: PV, Defesa, Esquiva, RD e Velocidade")
    r = c.r
    arm = T("criacao.armadura")
    rot(ws, f"A{r}", "Armadura ou Vestimenta")
    ent(ws, f"B{r}", "criacao.armadura", "lista", "armaduras", amostra="Média", invalido="Couro",
        rotulo="Armadura")
    cal(ws, f"C{r}", f'=IF({arm}="","Sem armadura: Defesa +0",IFERROR("Defesa +"&VLOOKUP({arm},'
                     f'{dtab("armaduras")},2,FALSE)&" · "&VLOOKUP({arm},{dtab("armaduras")},3,FALSE),""))',
        ate="J")
    av(ws, f"{AV}{r}", "criacao.aviso.armadura",
       f'=IF({arm}="","",IF(COUNTIF({dlista("armaduras")},{arm})=0,"Armadura fora da lista do capítulo 24",""))')
    r += 1
    cabecalhos(ws, r, ["Números da armadura", "Defesa", "Velocidade", "RD",
                       "Penalidade em Reflexos e Perícias de Agilidade", "Esquiva"], altura=45)
    r += 1
    texto(ws, f"A{r}", "(automático, 24.1)")
    for col, campo, k, vazio in (("B", "defesa", 2, "0"), ("C", "vel", 7, "0"), ("D", "rd", 8, "0"),
                                 ("E", "penalidade", 9, "0"), ("F", "esquiva", 4, '"Permitida"')):
        cal(ws, f"{col}{r}", f"=IFERROR(VLOOKUP({arm},{dtab('armaduras')},{k},FALSE),{vazio})",
            nome=f"criacao.armadura.{campo}")
    r += 1
    cabecalhos(ws, r, ["Estatística", "Base", "Extra (equipamento e Bênçãos)", "Total",
                       "Como se calcula"], altura=30)
    _mesclar(ws, f"E{r}", "J")
    cabecalho(ws, f"{AV}{r}", "Aviso")
    r += 1
    N, V = T("criacao.caminho.n"), bonus_de("Vigor")
    bag = bonus_de("Agilidade")
    linhas = [
        ("pv", "PV máximos", f"=25+5*{N}+3*{V}+({LV}-1)*(5+{N}+{V})", "pv",
         "25 + 5 × N + 3 × Bônus de Vigor + (nível - 1) × (5 + N + Bônus de Vigor) — 06.4"),
        ("defesa", "Defesa", f"=10+{bag}+{T('criacao.armadura.defesa')}", "defesa",
         "10 + Bônus de Agilidade + armadura — 18.4"),
        ("esquiva", "Esquiva (Reação)", None, None, "Defesa + Eficiência; proibida com Armadura Pesada"),
        ("rd", "RD", f"={T('criacao.armadura.rd')}", "rd", None),
        ("velocidade", "Velocidade (VEL)", f"=10+{bag}+{T('criacao.caminho.vel')}+{T('criacao.armadura.vel')}",
         "vel", "10 + Bônus de Agilidade + Bônus do Caminho + armadura — 19.1"),
    ]
    for campo, rotulo, base, extra, como in linhas:
        texto(ws, f"A{r}", rotulo, negrito=True)
        if campo == "esquiva":
            cal(ws, f"D{r}", f'=IF({T("criacao.armadura.esquiva")}="Proibida","Proibida (Armadura Pesada)",'
                             f'{T("criacao.defesa")}+{EF})', nome="criacao.esquiva", negrito=True, quebra=True)
            av(ws, f"{AV}{r}", "criacao.aviso.esquiva",
               f'=IF({T("criacao.armadura.esquiva")}="Proibida","Armadura Pesada não permite Esquiva","")')
        else:
            cal(ws, f"B{r}", base, nome=f"criacao.{campo}.base")
            cal(ws, f"C{r}", f"={T(f'criacao.extra.{extra}')}")
            b, x = T(f"criacao.{campo}.base"), T(f"criacao.extra.{extra}")
            if campo == "rd":
                cal(ws, f"D{r}", f"=MIN({T('nucleo.teto_rd')},{b}+{x})", nome="criacao.rd", negrito=True)
                como = f'="Armadura + Bênçãos + equipamento, até o teto de RD ("&{T("nucleo.teto_rd")}&") — 18.4"'
                av(ws, f"{AV}{r}", "criacao.aviso.rd",
                   f'=IF({b}+{x}>{T("nucleo.teto_rd")},"RD limitada ao teto ("&{T("nucleo.teto_rd")}&")","")')
            else:
                cal(ws, f"D{r}", f"={b}+{x}", nome=f"criacao.{campo}", negrito=True)
            if campo == "velocidade":
                vel = T("criacao.velocidade")
                av(ws, f"{AV}{r}", "criacao.aviso.velocidade",
                   f'=IF(OR({vel}<7,{vel}>25),"Velocidade fora de 7 a 25 (19.1)","")')
        cal(ws, f"E{r}", como, ate="J")
        r += 1
    c.r = r


def criacao_passos_9_a_12(c):
    ws = c.ws
    c.passo("Passos 9 a 11 — Habilidade, Ultimate e Bênção")
    r = c.r
    for campo, rotulo, alvo, falta in (
            ("habilidade", "Passo 9 — Sua primeira Habilidade", "criacao.reserva.habilidade1",
             "Preencha a Habilidade 1 na aba Habilidades"),
            ("ultimate", "Passo 10 — Sua Ultimate", "criacao.reserva.ultimate",
             "Preencha a Ultimate na aba Habilidades"),
            ("bencao", "Passo 11 — Sua primeira Bênção", "caminho.bencao.slot1.nome",
             "Preencha a Bênção do nível 1 na aba Caminho")):
        rot(ws, f"A{r}", rotulo, negrito=True)
        cal(ws, f"B{r}", f'=IF(LEN({T(alvo)})=0,{q(falta)},"OK: "&{T(alvo)})', nome=f"criacao.status.{campo}",
            ate="J")
        r += 1
    c.r = r

    c.passo("Passo 12 — Equipamento, nome e acabamento")
    r = c.r
    cat, atr, ela, prop = (T("criacao.arma.categoria"), T("criacao.arma.atributo_media"),
                           T("criacao.arma.elemento_proprio"), T("criacao.arma.propriedade"))
    rot(ws, f"A{r}", "Arma: nome e descrição")
    ent(ws, f"B{r}", "criacao.arma.nome", ate="J", rotulo="Arma")
    r += 1
    rot(ws, f"A{r}", "Categoria da arma (capítulo 18)")
    ent(ws, f"B{r}", "criacao.arma.categoria", "lista", "armas", amostra="Pesada", invalido="Laser",
        rotulo="Categoria da arma")
    arma = dtab("armas")
    cal(ws, f"C{r}", f'=IF({cat}="","",IFERROR(VLOOKUP({cat},{arma},2,FALSE)&" · alcance "&'
                     f'VLOOKUP({cat},{arma},5,FALSE)&" · "&VLOOKUP({cat},{arma},6,FALSE)&'
                     f'IF(VLOOKUP({cat},{arma},10,FALSE)="Sim"," · duas mãos",""),""))', ate="J")
    av(ws, f"{AV}{r}", "criacao.aviso.arma_categoria",
       f'=IF({cat}="","",IF(COUNTIF({dlista("armas")},{cat})=0,"Categoria fora da lista do capítulo 24",""))')
    r += 1
    rot(ws, f"A{r}", "Atributo (só arma Média: Poder ou Agilidade)")
    ent(ws, f"B{r}", "criacao.arma.atributo_media", "lista", "atributo_media", rotulo="Atributo da arma")
    rot(ws, f"C{r}", "Atributo de ataque:")
    cal(ws, f"D{r}", f'=IF({cat}="","",IF({cat}="Média",IF(OR({atr}="Poder",{atr}="Agilidade"),{atr},'
                     f'"Poder"),IFERROR(VLOOKUP({cat},{arma},6,FALSE),"")))', nome="criacao.arma.atributo",
        negrito=True, ate="E")
    av(ws, f"{AV}{r}", "criacao.aviso.arma_atributo",
       f'=IF(AND({atr}<>"",{cat}<>"Média"),"O atributo só se escolhe na arma Média",'
       f'IF(AND({cat}="Média",{atr}=""),"Arma Média: escolha Poder ou Agilidade (contando Poder)",""))')
    r += 1
    rot(ws, f"A{r}", "Elemento próprio da arma (vazio = Físico)")
    ent(ws, f"B{r}", "criacao.arma.elemento_proprio", "lista", "elementos", rotulo="Elemento da arma")
    rot(ws, f"C{r}", "Elemento do Ataque Básico:")
    cal(ws, f"D{r}", f'=IF({ela}="","Físico",{ela})', nome="criacao.arma.elemento", negrito=True, ate="E")
    av(ws, f"{AV}{r}", "criacao.aviso.arma_elemento",
       f'=IF({ela}="","",IF(COUNTIF({dlista("elementos")},{ela})=0,"Elemento fora da lista do capítulo 20",""))')
    r += 1
    rot(ws, f"A{r}", "Propriedade especial (no máximo 1)")
    ent(ws, f"B{r}", "criacao.arma.propriedade", "lista", "propriedades", amostra="Alcance estendido",
        invalido="Arremessável, Dissimulada", rotulo="Propriedade especial")
    cal(ws, f"C{r}", f'=IF(OR({prop}="",{prop}="Nenhuma"),"",IFERROR(VLOOKUP({prop},'
                     f'{dtab("propriedades")},2,FALSE),""))', ate="J", quebra=True)
    ws.row_dimensions[r].height = 30
    av(ws, f"{AV}{r}", "criacao.aviso.arma_propriedade",
       f'=IF({prop}="","",IF(COUNTIF({dlista("propriedades")},{prop})=0,'
       f'"Só uma propriedade especial por arma (24.2): escolha uma da lista",""))')
    r += 1
    # v1.2: a aba resolve em negrito o valor final de cada escolha (atributo, elemento, Espaço),
    # e o Espaço já honrava a propriedade (Dissimulada). O alcance não tinha linha resolvida: o
    # único que aparecia era o da categoria, lido direto da tabela de armas, então quem escolhia
    # "Alcance estendido" lia o alcance antigo aqui e o novo na aba Equipamento. Mesma fórmula
    # de lá: um passo acima na escala de 18.6, com teto em Extrema
    alc_arma = dlista("alcances")
    rot(ws, f"A{r}", "Alcance do Ataque Básico (com a propriedade)")
    cal(ws, f"B{r}", f'=IF({cat}="","",IFERROR(INDEX({alc_arma},MIN(5,'
                     f'MATCH(VLOOKUP({cat},{arma},5,FALSE),{alc_arma},0)'
                     f'+IF({prop}="Alcance estendido",1,0))),""))',
        nome="criacao.arma.alcance", negrito=True, ate="C")
    rot(ws, f"D{r}", "Arremessável não muda este alcance: é um arremesso só, e depois você está sem a arma (24.2).")
    _mesclar(ws, f"D{r}", "J")
    r += 1
    rot(ws, f"A{r}", "Espaço da arma no inventário")
    cal(ws, f"B{r}", f'=IF({prop}="Dissimulada",0.5,IFERROR(VLOOKUP({cat},{arma},8,FALSE),0))',
        nome="criacao.arma.espaco", negrito=True)
    r += 1
    rot(ws, f"A{r}", "Técnica (24.6): nome")
    ent(ws, f"B{r}", "criacao.tecnica.nome", ate="J", rotulo="Técnica")
    r += 1
    rot(ws, f"A{r}", "Técnica: o que ela faz")
    ent(ws, f"B{r}", "criacao.tecnica.texto", ate="J", rotulo="Técnica")
    r += 1
    rot(ws, f"A{r}", "Técnica: usos")
    cal(ws, f"B{r}", "2 usos por Descanso Longo, fora de combate (24.6)", ate="J")
    r += 1
    rot(ws, f"A{r}", "Aparência e de onde você veio")
    ent(ws, f"B{r}", "criacao.aparencia", ate="J", rotulo="Aparência")
    r += 1
    rot(ws, f"A{r}", "Uma coisa que você carrega e não serve para nada")
    ent(ws, f"B{r}", "criacao.coisa_inutil", ate="J", rotulo="A coisa que não serve para nada")
    c.r = r + 1


def _forma_sincronizada():
    """Avatar da Recordação com a Forma Sincronizada escolhida (decisão 2; 11, nº 11)."""
    return f'AND({tem_bencao("Avatar da Recordação")},{T("caminho.escolha.avatar")}="Sincronizada")'


def criacao_ligacoes(c):
    """Células que juntam o que vem das abas Equipamento, Caminho, Em Jogo e Habilidades
    (decisão 2 do plano: Bênçãos de efeito fixo entram nos números)."""
    ws = c.ws
    c.passo("Ligações com outras abas (automático; não editar)")
    r = c.r
    L2 = f"2*{LV}"
    fs = _forma_sincronizada()
    ligacoes = (
        ("criacao.extra.pv", "PV extra (Relíquia Cabeça, Cone de Luz, Corpo Imortal, Forma Sincronizada)",
         f'={T("equipamento.reliquia.cabeca.bonus")}+{T("equipamento.cone.em.pv")}'
         f'+IF({tem_bencao("Corpo Imortal")},{L2},0)+IF({fs},{L2},0)'),
        ("criacao.extra.defesa", "Defesa extra (Relíquia Tronco, Cone de Luz, Forma Sincronizada)",
         f'={T("equipamento.reliquia.tronco.bonus")}+{T("equipamento.cone.em.defesa")}+IF({fs},1,0)'),
        ("criacao.extra.rd", "RD extra (Cone de Luz, Conjunto, Pele de Pedra, Corpo Imortal)",
         f'={T("equipamento.cone.em.rd")}+{T("equipamento.conjuntos.rd")}'
         f'+IF({tem_bencao("Pele de Pedra")},2,0)+IF({tem_bencao("Corpo Imortal")},{EF},0)'),
        ("criacao.extra.vel", "Velocidade extra (Botas, Cone de Luz, Conjunto, Ressonância I, Avatar da Caça)",
         f'={T("equipamento.reliquia.botas.bonus")}+{T("equipamento.cone.em.velocidade")}'
         f'+{T("equipamento.conjuntos.vel")}+IF({T("progressao.ressonancia.I.efetiva")}="Velocidade +1",1,0)'
         f'+IF({tem_bencao("Avatar da Caça")},2,0)'),
        ("criacao.extra.ataque", "Teste de Ataque extra (Cone de Luz + bônus temporários no teto, aba Em Jogo)",
         f'={T("equipamento.cone.em.ataque")}+{T("em_jogo.temp_ataque")}'),
        ("criacao.reserva.habilidade1", "Nome da Habilidade 1 (aba Habilidades)",
         f'=IF(LEN({T("habilidades.1.nome")})=0,"",""&{T("habilidades.1.nome")})'),
        ("criacao.reserva.ultimate", "Nome da Ultimate (aba Habilidades)",
         f'=IF(LEN({T("habilidades.ultimate.nome")})=0,"",""&{T("habilidades.ultimate.nome")})'),
    )
    for nome, rotulo, valor in ligacoes:
        rot(ws, f"A{r}", rotulo)
        # nomes (até 40 caracteres) ocupam B:F; números ficam só em B
        cal(ws, f"B{r}", valor, nome=nome, ate="F" if nome.startswith("criacao.reserva.") else None)
        r += 1
    c.r = r


def aba_criacao(ws):
    # K tem números do nível (linhas 13-16): largura normal, não espaçador (auditoria visual)
    # A:L = 1355 px (área do jogador em 1360 px; M:O são auxiliares ocultas)
    # B = 25 (180 px): cabe "Dois Atributos (+1 cada)" + a seta da lista (revisão 2)
    larguras(ws, {"A": 30, "B": 25, **{get_column_letter(j): 11 for j in range(3, 12)}, "L": 36,
                  "M": 2, "N": 16, "O": 16})
    texto(ws, "N4", "Listas auxiliares", negrito=True)
    c = Cursor(ws, 5)
    criacao_cabecalho(c)
    criacao_nucleo(c)
    criacao_passos_1_a_3(c)
    criacao_passo_4(c)
    criacao_passos_5_6(c)
    criacao_passo_7(c)
    criacao_passo_8(c)
    criacao_passos_9_a_12(c)
    criacao_ligacoes(c)


# ---------------------------------------------------------------------------
# Aba Progressão — tabela mestra, aumentos, Ressonâncias, próximo nível
# ---------------------------------------------------------------------------

MESTRA_CAMPOS = [  # (campo no mapa, coluna da Dados ou None, cabeçalho)
    ("nivel", "Nível", "Nível"),
    ("eficiencia", "Eficiência", "Eficiência"),
    ("eficacia_pericias", "Eficácia: Perícias", "Eficácia: slots em Perícias"),
    ("eficacia_tr", "Eficácia: Testes de Resistência", "Eficácia: slots em Testes de Resistência"),
    ("bencaos", "Bênçãos", "Bênçãos"),
    ("habilidades", "Habilidades conhecidas", "Habilidades conhecidas"),
    ("reescreve", "Reescreve 1 por nível", "Reescreve 1 por nível"),
    ("nivel_max_habilidade", "Nível máx. de Habilidade", "Nível máx. de Habilidade"),
    ("aumento", "Aumento de Atributo", "Aumento de Atributo"),
    ("dados_ab", "Dados de Ataque Básico", "Dados de Ataque Básico"),
    ("especializacao", "Especialização", "Especialização de Combate"),
    ("teto_rd", "Teto de RD", "Teto de RD"),
    ("ph_max", None, "PH do grupo: máximo"),
    ("ph_inicio", None, "PH do grupo: início"),
    ("ultimate", None, "Ultimate: Nível equivalente"),
    ("cone", None, "Cone de Luz máximo"),
    ("tier", None, "Tier de Relíquia"),
]
NIVEIS_AUMENTO = (3, 6, 9, 12, 15, 18)


def aba_progressao(ws):
    # A:I = 1356 px (área do jogador em 1360 px; R é auxiliar oculta)
    # C = 180 px: cabe "Dois Atributos (+1 cada)" + a seta da lista (revisão 2); I cede a diferença
    larguras(ws, {"A": _px_largura(68), **{get_column_letter(j): _px_largura(161) for j in range(2, 10)},
                  "C": _px_largura(180), "I": _px_largura(142)})
    PL = T("progressao.nivel")
    rot(ws, "A5", "Nível atual")
    _mesclar(ws, "A5", "B")
    cal(ws, "C5", f"={LV}", nome="progressao.nivel", negrito=True)
    rot(ws, "D5", "Jogadores")
    cal(ws, "E5", f"={T('nucleo.jogadores')}", nome="progressao.jogadores", negrito=True)
    rot(ws, "F5", "A linha do seu nível fica destacada em amarelo e negrito.")
    _mesclar(ws, "F5", "I")
    # 16 colunas não cabem em 1360 px: a tabela mestra vem em 2 partes de 8 colunas (cada uma
    # repete o Nível) e cada parte em 2 blocos de 10 níveis, com o cabeçalho repetido
    destaque = PatternFill(start_color=COR_DESTAQUE, end_color=COR_DESTAQUE, fill_type="solid")
    partes = [("Tabela mestra, nível 1 a 20 — 26.2: Eficiência, Eficácia, Bênçãos e Habilidades",
               MESTRA_CAMPOS[1:9]),
              ("Tabela mestra (continuação) — 26.2, PH do grupo 16.2, Ultimate 17.3, Cone de Luz e Relíquias 25.1",
               MESTRA_CAMPOS[9:])]
    r = 7
    cabs = []
    for k_parte, (titulo_parte, campos) in enumerate(partes):
        if k_parte:
            r += 1
        titulo(ws, f"A{r}", titulo_parte, ate="I")
        r += 1
        r0 = r + 1
        for n in range(1, 21):
            if n in (1, 11):
                cabecalhos(ws, r, [f"Nível ({n} a {n + 9})"] + [c[2] for c in campos], altura=None)
                cabs.append(r)
                r += 1
            nn = f"$A{r}"
            cal(ws, f"A{r}", f"=INDEX({dcol('mestra', 'Nível')},{n})",
                nome=f"progressao.mestra.{n}.nivel" if not k_parte else None, negrito=True).alignment = \
                Alignment(horizontal="center", vertical="center")
            for j, (campo, col_dados, _) in enumerate(campos, start=2):
                letra = get_column_letter(j)
                if col_dados:
                    f = f"=INDEX({dcol('mestra', col_dados)},{n})"
                elif campo == "ph_max":
                    f = f"=1+{T('progressao.jogadores')}+IF({nn}>=17,2,IF({nn}>=9,1,0))"
                elif campo == "ph_inicio":
                    f = f"={T(f'progressao.mestra.{n}.ph_max')}-2"
                elif campo == "ultimate":
                    f = f"=INDEX({dcol('ultimate', 'Nível equivalente')},INT(({nn}-1)/4)+1)"
                elif campo == "cone":
                    f = f'="Nível "&(INT(({nn}-1)/4)+1)'
                else:
                    f = f'=CHOOSE(IF({nn}<=6,1,IF({nn}<=12,2,IF({nn}<=17,3,4))),"I","II","III","IV")'
                cal(ws, f"{letra}{r}", f, nome=f"progressao.mestra.{n}.{campo}").alignment = \
                    Alignment(horizontal="center", vertical="center")    # número embaixo do cabeçalho
            r += 1
        ws.conditional_formatting.add(f"A{r0}:I{r - 1}", FormulaRule(
            formula=[f"$A{r0}=$C$5"], fill=destaque, font=Font(bold=True, color="000000")))
    for rc in cabs:
        for j in range(1, 10):
            ws.cell(rc, j).alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # --- Aumentos de Atributo ---------------------------------------------------------
    r += 1
    titulo(ws, f"A{r}", "Aumentos de Atributo — níveis 3, 6, 9, 12, 15 e 18 (04.3): +2 em um ou "
                        "+1 em dois diferentes, teto 20", ate="I")
    r += 1
    cabecalhos(ws, r, ["Nível", "Situação", "Modo (preencha)", "Atributo 1 (preencha)",
                       "Atributo 2 (só Dois Atributos)", "Soma no Atributo 1", "Soma no Atributo 2", "Aviso"],
               altura=None)
    _mesclar(ws, f"H{r}", "I")
    r += 1
    r0 = r
    for n in NIVEIS_AUMENTO:
        base = f"progressao.aumento.{n}"
        texto(ws, f"A{r}", n, negrito=True)
        cal(ws, f"B{r}", f'=IF({PL}>={n},"Liberado","Libera no nível {n}")', nome=f"{base}.situacao")
        ent(ws, f"C{r}", f"{base}.modo", "lista", "modo_aumento", rotulo=f"Aumento do nível {n}")
        ent(ws, f"D{r}", f"{base}.atributo1", "lista", "atributos", rotulo="Atributo 1")
        ent(ws, f"E{r}", f"{base}.atributo2", "lista", "atributos", amostra="Vigor", rotulo="Atributo 2")
        md, x1, x2 = T(f"{base}.modo"), T(f"{base}.atributo1"), T(f"{base}.atributo2")
        cal(ws, f"F{r}", f'=IF(AND({n}<={PL},{x1}<>""),IF({md}="Dois Atributos (+1 cada)",1,2),0)', nome=f"{base}.soma1")
        cal(ws, f"G{r}", f'=IF(AND({n}<={PL},{md}="Dois Atributos (+1 cada)",{x2}<>"",{x2}<>{x1}),1,0)',
            nome=f"{base}.soma2")
        av(ws, f"H{r}", f"progressao.aviso.aumento.{n}",
           f'=IF(AND(OR({md}<>"",{x1}<>"",{x2}<>""),{n}>{PL}),"Ainda não liberado (nível {n})",'
           f'IF(AND({md}="Dois Atributos (+1 cada)",{x1}<>"",{x1}={x2}),"+1 em dois exige atributos diferentes: '
           f'contou só um +1",IF(AND({x2}<>"",{md}<>"Dois Atributos (+1 cada)"),"Atributo 2 só vale no modo Dois Atributos (+1 cada)",'
           f'IF(AND({md}="Dois Atributos (+1 cada)",{x1}<>"",{x2}=""),"Falta o Atributo 2",""))))', ate="I")
        r += 1
    for nome, col in (("atributo1", "D"), ("atributo2", "E"), ("soma1", "F"), ("soma2", "G")):
        reg(f"progressao.aumentos.{nome}", ws, f"{col}{r0}:{col}{r - 1}")
    rot(ws, f"A{r}", "Bônus de Vigor subiu? Os PV sobem na hora: nível + 2 =")
    _mesclar(ws, f"A{r}", "D")
    cal(ws, f"E{r}", f"={PL}+2", nome="progressao.pv_ganho_vigor", negrito=True)
    rot(ws, f"F{r}", "PV (04.3; a aba Criação já soma tudo)")
    _mesclar(ws, f"F{r}", "I")
    r += 2

    # --- Ressonâncias --------------------------------------------------------------------
    titulo(ws, f"A{r}", "Ressonâncias — 26.7 (níveis 5, 10, 15 e 20)", ate="I")
    r += 1
    cabecalhos(ws, r, ["Ressonância", "Nível", "Opção (preencha)", None, None, "Situação",
                       "O que o livro diz", None, "Aviso"], altura=None)
    _mesclar(ws, f"C{r}", "E")
    _mesclar(ws, f"G{r}", "H")
    r += 1
    for k, rn in enumerate(("I", "II", "III", "IV"), start=1):
        base = f"progressao.ressonancia.{rn}"
        texto(ws, f"A{r}", rn, negrito=True)
        cal(ws, f"B{r}", f"=INDEX({dcol('ressonancias', 'Nível')},{k})", nome=f"{base}.nivel")
        nr = T(f"{base}.nivel")
        # C:E: a opção mais longa de 26.7 + a seta da lista cabem numa linha
        ent(ws, f"C{r}", f"{base}.opcao", "lista", f"ress{k}", ate="E", rotulo=f"Ressonância {rn}")
        op = T(f"{base}.opcao")
        cal(ws, f"F{r}", f'=IF({PL}>={nr},IF({op}="","Liberada: escolha a opção","Ativa"),'
                         f'"Libera no nível "&{nr})', nome=f"{base}.situacao", quebra=True)
        cal(ws, f"G{r}", f"=INDEX({dcol('ressonancias', 'O que ela dá')},{k})", ate="H", quebra=True)
        av(ws, f"I{r}", f"progressao.aviso.ressonancia.{rn}",
           f'=IF(AND({op}<>"",{PL}<{nr}),"Ainda não liberada (nível "&{nr}&")","")')
        # opção que vale nos números (vazia antes do nível) — coluna auxiliar cinza
        aux(ws, f"R{r}", f'=IF({PL}>={nr},{op},"")', nome=f"{base}.efetiva")
        r += 1
    ws.column_dimensions["R"].width = 4
    r += 1

    # --- No próximo nível -----------------------------------------------------------------
    titulo(ws, f"A{r}", "No próximo nível você ganha", ate="I")
    r += 1
    rot(ws, f"A{r}", "Próximo nível:")
    _mesclar(ws, f"A{r}", "B")
    cal(ws, f"C{r}", f"=MIN(20,{PL}+1)", nome="progressao.proximo.nivel", negrito=True)
    r += 1
    nx = T("progressao.proximo.nivel")
    fim = f"{PL}<20"

    def m(col, idx):
        return f"INDEX({dcol('mestra', col)},{idx})"

    N, V = T("criacao.caminho.n"), bonus_de("Vigor")
    linhas = [
        f'=IF({PL}>=20,"Você está no nível 20, o máximo do jogo.","Nível "&{nx}&":")',
        f'=IF(AND({fim},{m("Eficiência", nx)}>{m("Eficiência", PL)}),"Eficiência sobe para +"&'
        f'{m("Eficiência", nx)}&" (Eficácia +"&2*{m("Eficiência", nx)}&")","")',
        f'=IF(AND({fim},MOD({nx},2)=1),"Nova Bênção (slot do nível "&{nx}&", aba Caminho)","")',
        f'=IF(AND({fim},{m("Habilidades conhecidas", nx)}>{m("Habilidades conhecidas", PL)}),'
        f'"Mais 1 Habilidade conhecida (total "&{m("Habilidades conhecidas", nx)}&")",'
        f'IF(AND({fim},{m("Reescreve 1 por nível", nx)}="Sim"),"Reescreva 1 Habilidade (16.6)",""))',
        f'=IF(AND({fim},{m("Nível máx. de Habilidade", nx)}>{m("Nível máx. de Habilidade", PL)}),'
        f'"Habilidades até o Nível "&{m("Nível máx. de Habilidade", nx)},"")',
        f'=IF(AND({fim},{m("Aumento de Atributo", nx)}="Sim"),"Aumento de Atributo: +2 em um ou +1 em dois '
        f'(tabela acima)","")',
        f'=IF(AND({fim},{m("Dados de Ataque Básico", nx)}>{m("Dados de Ataque Básico", PL)}),'
        f'"Ataque Básico com "&{m("Dados de Ataque Básico", nx)}&" dados","")',
        f'=IF(AND({fim},{m("Especialização", nx)}>{m("Especialização", PL)}),"Especialização de Combate +"'
        f'&{m("Especialização", nx)},"")',
        f'=IF(AND({fim},OR({m("Eficácia: Perícias", nx)}>{m("Eficácia: Perícias", PL)},'
        f'{m("Eficácia: Testes de Resistência", nx)}>{m("Eficácia: Testes de Resistência", PL)})),'
        f'"Slots de Eficácia: "&{m("Eficácia: Perícias", nx)}&" em Perícias e "&'
        f'{m("Eficácia: Testes de Resistência", nx)}&" em Testes de Resistência","")',
        f'=IF({fim},"PV máximos +"&(5+{N}+{V})&" (5 + N + Bônus de Vigor)","")',
        f'=IF(AND({fim},MOD({PL},4)=0),"Nova faixa de nível: Ultimate de Nível equivalente "&'
        f'INDEX({dcol("ultimate", "Nível equivalente")},INT(({nx}-1)/4)+1)&" e Cone de Luz até o Nível "&'
        f'(INT(({nx}-1)/4)+1),"")',
        f'=IF(AND({fim},MOD({nx},5)=0),"Ressonância "&CHOOSE(INT({nx}/5),"I","II","III","IV")&'
        f'" (tabela acima)","")',
        f'=IF(AND({fim},OR({nx}=7,{nx}=13,{nx}=18)),"Relíquias sobem para o Tier "&'
        f'CHOOSE(IF({nx}=7,1,IF({nx}=13,2,3)),"II","III","IV"),"")',
        f'=IF(AND({fim},OR({nx}=9,{nx}=17)),"PH do grupo: máximo +1","")',
        f'=IF(AND({fim},{CAM}="A Recordação"),IF(MOD({nx},2)=0,"Memoespírito: +1 ponto de atributo. ","")'
        f'&IF(OR({nx}=8,{nx}=14,{nx}=20),"Memoespírito: nova Evolução.",""),"")',
    ]
    for k, f in enumerate(linhas, start=1):
        cal(ws, f"A{r}", f, nome=f"progressao.proximo.linha{k}", ate="I")
        r += 1


# ---------------------------------------------------------------------------
# Aba Testes — 18 Perícias, 6 Testes de Resistência, Morrendo, DT da faixa
# ---------------------------------------------------------------------------

DIFICULDADES = ["Trivial", "Fácil", "Média", "Difícil", "Muito Difícil", "Heroica"]
# Perícias em 3 grupos de Atributos (índice da 1ª Perícia do grupo na lista de 04.4): o
# cabeçalho se repete em cada grupo, e nenhuma linha fica longe dele
GRUPOS_PERICIAS = {0: "Poder, Agilidade e Vigor", 5: "Sincronia e Discernimento", 13: "Presença e Sintonia"}


def aba_testes(ws):
    # A:L = 1306 px (área do jogador em 1360 px): Vantagem racial e Aviso quebram em linhas
    larguras(ws, {"A": 22, "B": 14, "C": 7, "D": 15, "E": 12, "F": 8, "G": 8, "H": 7, "I": 11,
                  "J": 30, "K": 16, "L": 30})
    van_per, van_tr, van_cond, van_morr = _vantagens_raciais()
    arm_pen = T("criacao.armadura.penalidade")
    sp, st = T("nucleo.slots_eficacia_pericias"), T("nucleo.slots_eficacia_tr")
    nomes, bon = T("criacao.atributos.nomes"), T("criacao.atributos.bonus")

    # DT da faixa primeiro (as Perícias consultam esta tabela)
    r_dt = 5
    titulo(ws, f"A{r_dt}", "DT por faixa — 27.2 (a sua faixa)", ate="D")
    rot(ws, f"F{r_dt}", "DT das suas Habilidades:")
    _mesclar(ws, f"F{r_dt}", "H")
    cal(ws, f"I{r_dt}", f"={T('criacao.dt')}", nome="testes.dt_habilidades", negrito=True)
    rot(ws, f"J{r_dt}", "Sucesso Automático: bônus total ≥ DT → não rola (só Perícia, 27.2)")
    _mesclar(ws, f"J{r_dt}", AV)
    r = r_dt + 1
    cabecalhos(ws, r, ["Dificuldade", "DT"], altura=None)
    r += 1
    for k, d in enumerate(DIFICULDADES, start=1):
        cal(ws, f"A{r}", f"=INDEX({dcol('dt_faixa', 'Dificuldade')},{k})")
        cal(ws, f"B{r}", f"=INDEX({dtab('dt_faixa')},{k},{FX}+1)", nome=f"testes.dt.{slug(d)}", negrito=True)
        r += 1

    def sucesso(total):
        f = '"—"'
        for d in DIFICULDADES:
            dt_ = T(f"testes.dt.{slug(d)}")
            f = f'IF({total}>={dt_},"{d} ("&{dt_}&")",{f})'
        return "=" + f

    def vantagem(nome, mapa, cond=None):
        partes = []
        if mapa.get(nome):
            partes.append(f'IF({_ou_raca(mapa[nome])},"Vantagem ("&{RACA}&")","")')
        if cond and cond.get(nome):
            partes.append(f'IF({_ou_raca(cond[nome])},"Vantagem condicional ("&{RACA}&'
                          f'": água, frio e afogamento)","")')
        return "=" + ("&".join(partes) if partes else '""')

    # --- Perícias ---------------------------------------------------------------
    r += 1
    titulo(ws, f"A{r}", "Perícias — 04.4 (rolagem pronta: d20 + Bônus + Eficiência)", ate=AV)
    r += 1
    cab_per = ["Atributo", "Bônus", "Eficiência (origem)", "Eficácia (preencha Sim)",
               "Penalidade (Armadura Pesada)", "Extra (equipamento)", "Total", "Rolagem",
               "Vantagem racial", "Sucesso Automático até", "Aviso"]
    r0 = r + 1
    for i_p, p in enumerate(_valores_lista("pericias")):
        if i_p in GRUPOS_PERICIAS:
            # cabeçalho repetido em cada grupo de Atributos (sem linhas congeladas)
            cabecalhos(ws, r, [f"Perícia ({GRUPOS_PERICIAS[i_p]})"] + cab_per)
            r += 1
        s = slug(p)
        base, cri = f"testes.pericia.{s}", f"criacao.pericia.{s}"
        texto(ws, f"A{r}", p, negrito=True)
        cal(ws, f"B{r}", f"={T(cri + '.atributo')}", nome=f"{base}.atributo")
        B = T(f"{base}.atributo")
        cal(ws, f"C{r}", f"=IFERROR(INDEX({bon},MATCH({B},{nomes},0)),0)", nome=f"{base}.bonus")
        efi, orig = T(cri + ".eficiencia"), T(cri + ".origem")
        cal(ws, f"D{r}", f'=IF({efi}="Sim","Sim ("&{orig}&")","Não")', nome=f"{base}.eficiencia")
        ent(ws, f"E{r}", f"{base}.eficacia", "lista", "sim_nao", rotulo=p)
        E = T(f"{base}.eficacia")
        cal(ws, f"F{r}", f'=IF({B}="Agilidade",{arm_pen},0)', nome=f"{base}.penalidade")
        # Cone de Luz "Uma Perícia" (permanente, fora do teto) + Conjunto "+1 em um tipo de
        # rolagem" (temporário, dentro do teto de bônus somado) — 25.2, 25.3, 25.4
        cal(ws, f"G{r}", f'=IF({T("equipamento.cone.em.pericia_nome")}={q(p)},{T("equipamento.cone.em.pericia")},0)'
                         f'+MIN({T("nucleo.teto_bonus")},COUNTIF({T("equipamento.conjuntos.rolagens")},{q(p)}))',
            nome=f"{base}.extra")
        usa = f'AND({E}="Sim",{efi}="Sim",COUNTIF($E${r0}:E{r},"Sim")<={sp})'
        cal(ws, f"H{r}", f'={T(base + ".bonus")}+IF({efi}="Sim",IF({usa},2*{EF},{EF}),0)+'
                         f'{T(base + ".penalidade")}+{T(base + ".extra")}', nome=f"{base}.total", negrito=True)
        tot = T(f"{base}.total")
        cal(ws, f"I{r}", "=" + rolagem(tot), nome=f"{base}.rolagem", negrito=True)
        cal(ws, f"J{r}", vantagem(p, van_per), nome=f"{base}.vantagem", quebra=True)
        cal(ws, f"K{r}", sucesso(tot), nome=f"{base}.sucesso_automatico", quebra=True)
        av(ws, f"{AV}{r}", f"testes.aviso.pericia.{s}",
           f'=IF({E}<>"Sim","",IF({efi}<>"Sim","Eficácia exige Eficiência nesta Perícia",'
           f'IF(COUNTIF($E${r0}:E{r},"Sim")>{sp},"Acima dos slots de Eficácia em Perícias ("&{sp}&")","")))')
        r += 1
    reg("testes.pericias.eficacia", ws, f"E{r0}:E{r - 1}")
    rot(ws, f"A{r}", "Slots de Eficácia em Perícias: marcados / permitidos")
    cal(ws, f"B{r}", f'=COUNTIF({T("testes.pericias.eficacia")},"Sim")', nome="testes.eficacia_pericias.usados",
        negrito=True)
    cal(ws, f"C{r}", f"={sp}", nome="testes.eficacia_pericias.permitidos", negrito=True)
    rot(ws, f"D{r}", "Perícias com Eficiência:")
    cal(ws, f"E{r}", f"={T('criacao.pericias.com_eficiencia')}", nome="testes.pericias_com_eficiencia",
        negrito=True)
    r += 2

    # --- Testes de Resistência ------------------------------------------------------
    titulo(ws, f"A{r}", "Testes de Resistência — 04.6 e 22 (Eficiência em todos desde o nível 1; "
                        "sem crítico, sempre rolado)", ate=AV)
    r += 1
    cabecalhos(ws, r, ["Teste de Resistência", "Atributo", "Bônus", "Eficiência", "Eficácia (preencha Sim)",
                       "Penalidade (Armadura Pesada)", "Extra (Bênçãos)", "Total", "Rolagem",
                       "Vantagem racial", "Aviso"])
    _mesclar(ws, f"K{r}", "L")         # TR não tem Sucesso Automático: o aviso ganha K:L
    r += 1
    r0 = r
    for k, t in enumerate(_valores_lista("tr"), start=1):
        s = slug(t)
        base = f"testes.tr.{s}"
        texto(ws, f"A{r}", t, negrito=True)
        cal(ws, f"B{r}", f"=INDEX({dcol('tr', 'Atributo')},{k})", nome=f"{base}.atributo")
        B = T(f"{base}.atributo")
        cal(ws, f"C{r}", f"=IFERROR(INDEX({bon},MATCH({B},{nomes},0)),0)", nome=f"{base}.bonus")
        cal(ws, f"D{r}", f'="+"&{EF}', nome=f"{base}.eficiencia")
        ent(ws, f"E{r}", f"{base}.eficacia", "lista", "sim_nao", rotulo=t)
        E = T(f"{base}.eficacia")
        cal(ws, f"F{r}", f'=IF({B}="Agilidade",{arm_pen},0)', nome=f"{base}.penalidade")
        # Cone de Luz "Um Teste de Resistência" (fora do teto) + temporários no teto de bônus
        # somado: Conjunto, Cicatriz da Destruição (FV e RM), Florescimento da Alma (decisão 2)
        temp_tr = f'COUNTIF({T("equipamento.conjuntos.rolagens")},{q(t)})+{T("em_jogo.florescimento")}'
        if t in ("Força de Vontade", "Resistência Mental"):
            temp_tr += f'+{T("em_jogo.marcas")}'
        cal(ws, f"G{r}", f'=IF({T("equipamento.cone.em.tr_nome")}={q(t)},{T("equipamento.cone.em.tr")},0)'
                         f'+MIN({T("nucleo.teto_bonus")},{temp_tr})', nome=f"{base}.extra")
        usa = f'AND({E}="Sim",COUNTIF($E${r0}:E{r},"Sim")<={st})'
        cal(ws, f"H{r}", f'={T(base + ".bonus")}+IF({usa},2*{EF},{EF})+{T(base + ".penalidade")}+'
                         f'{T(base + ".extra")}', nome=f"{base}.total", negrito=True)
        cal(ws, f"I{r}", "=" + rolagem(T(f"{base}.total")), nome=f"{base}.rolagem", negrito=True)
        cal(ws, f"J{r}", vantagem(t, van_tr, van_cond), nome=f"{base}.vantagem", quebra=True)
        av(ws, f"K{r}", f"testes.aviso.tr.{s}", ate="L", formula=
           f'=IF(AND({E}="Sim",COUNTIF($E${r0}:E{r},"Sim")>{st}),'
           f'"Acima dos slots de Eficácia em Testes de Resistência ("&{st}&"). ","")'
           f'&IF(({temp_tr})>{T("nucleo.teto_bonus")},"Bônus temporário acima do teto (+"&'
           f'{T("nucleo.teto_bonus")}&"): conta só o teto (26.6).","")')
        r += 1
    reg("testes.tr.eficacia_marcadas", ws, f"E{r0}:E{r - 1}")
    # Morrendo (23.4): d20 + Presença, sem Eficiência, DT 10
    texto(ws, f"A{r}", "Teste de Morrendo (sem Eficiência, DT 10)", negrito=True)
    cal(ws, f"B{r}", "Presença")
    cal(ws, f"C{r}", f"={bonus_de('Presença')}", nome="testes.morrendo.bonus")
    cal(ws, f"D{r}", "Não usa")
    cal(ws, f"H{r}", f"={T('testes.morrendo.bonus')}", nome="testes.morrendo.total", negrito=True)
    cal(ws, f"I{r}", "=" + rolagem(T("testes.morrendo.total")) + '&" ≥ 10"', nome="testes.morrendo.rolagem",
        negrito=True)
    direta = [x for x, _ in van_morr]          # 23.5 nomeia as três Raças (v1.1)
    f_morr = f'IF({_ou_raca(direta)},"Vantagem ("&{RACA}&", 23.5)","")' if direta else '""'
    cal(ws, f"J{r}", "=" + f_morr, nome="testes.morrendo.vantagem")
    rot(ws, f"K{r}", "3 sucessos: 1 PV · 3 falhas: morre (23.4)")
    _mesclar(ws, f"K{r}", AV)
    r += 1
    rot(ws, f"A{r}", "Slots de Eficácia em Testes de Resistência: marcados / permitidos")
    cal(ws, f"B{r}", f'=COUNTIF({T("testes.tr.eficacia_marcadas")},"Sim")', nome="testes.eficacia_tr.usados",
        negrito=True)
    cal(ws, f"C{r}", f"={st}", nome="testes.eficacia_tr.permitidos", negrito=True)


# ---------------------------------------------------------------------------
# Aba Caminho — ficha do Caminho, recurso próprio, 10 slots, catálogo, Memoespírito
# ---------------------------------------------------------------------------

def _linhas_recurso():
    """Linhas do recurso próprio por Caminho (D2): expressões de texto da fórmula."""
    L2, EF3 = f"2*{LV}", f"3*{EF}"
    riso = []
    _, corpo = ficha_dados.tabela("13", "## 13.2", "d6")
    for d6, efeito in corpo:
        riso.append(q(f"{ficha_dados.limpar(d6)}: {ficha_dados.limpar(efeito)}"))
    # 08.1, 09.1 e 10.1 (v1.1): "Nenhum além dos acúmulos das Bênçãos" — a linha nomeia os acúmulos
    def so_bencaos(cap, acumulos):
        return [q(f"Nenhum recurso além dos acúmulos das Bênçãos ({cap}.1): {acumulos}."),
                q("Use a frequência e os acúmulos das Bênçãos adquiridas, nos slots abaixo.")]
    return {
        "A Destruição": [
            f'"PV como moeda (7.2): ativação ou acúmulo de Bênção de custo = 2 × nível = "&{L2}&" PV"',
            f'"Dado base comprado no Avatar = 5 × nível = "&(5*{LV})&" PV"',
            q("Você escolhe pagar e não pode pagar se o custo for igual ou maior que os seus PV atuais."),
            q("PV gastos assim não são dano: não geram Energia, não passam por RD e contam para as Marcas."),
        ],
        "A Inexistência": so_bencaos("8", "Marca do Vazio (até 3) e Corrupção (até 5)"),
        "A Harmonia": so_bencaos("9", "Eco da Vitória (até 3)"),
        "A Abundância": so_bencaos("10", "Florescimento (até 5)"),
        "A Recordação": [
            q("Memoespírito (11.3 a 11.5): monte a ficha dele no bloco abaixo."),
            q("Invocar: Ação Complementar + 1 PH. A Energia das ações dele vale metade para você."),
        ],
        "A Erudição": [
            f'"Acúmulos de Cálculo (12.2): máximo "&IF({tem_bencao("Teto Rompido")},7,5)&" por combate"',
            q("Ganha 1 acúmulo por inimigo atingido por um mesmo ataque, Habilidade ou Ultimate sua."),
            q("Gastar 1 acúmulo: +1 alvo para a ação em curso. Gastar 2: +1 dado base no dano."),
            q("Gastar não consome ação. Os acúmulos zeram no fim do combate."),
        ],
        "A Euforia": [q("Tabela do Riso (13.2): role 1d6 quando uma Bênção mandar.")] + riso,
        "A Caça": [
            q("Marcação de Presa (14.2): Ação Complementar, 1 inimigo por vez, +1 dado base contra ele."),
            q("A marca dura até o fim do combate e migra de graça quando o alvo é derrotado."),
            f'"Faixa de crítico: "&IF({tem_bencao("Olho de Lan")},"19-20 (Olho de Lan)","20")',
        ],
        "A Preservação": [
            f'"Teto de Barreira (15.2) = 3 × Eficiência = "&{EF3}',
            q("Barreira não acumula com outro PV temporário: fica o maior valor."),
            q("Cura não repõe Barreira. O dano passa pela RD antes da Barreira."),
        ],
    }


def caminho_ficha(c):
    ws = c.ws
    c.titulo("Ficha do Caminho (escolha o Caminho na aba Criação, Passo 3)")
    r = c.r
    rot(ws, f"A{r}", "Caminho")
    cal(ws, f"B{r}", f'=IF({CAM}="","Escolha na aba Criação",{CAM})', nome="caminho.caminho", negrito=True,
        ate="C")
    rot(ws, f"D{r}", "Aeon")
    cal(ws, f"E{r}", f"={T('criacao.caminho.aeon')}", ate="F")
    rot(ws, f"G{r}", "Atributo de Habilidade usado")
    cal(ws, f"H{r}", f"={T('criacao.atributo_habilidade.usado')}", negrito=True)
    r += 1
    rot(ws, f"A{r}", "A ideia")
    cal(ws, f"B{r}", f"={T('criacao.caminho.ideia')}", ate="H")
    r += 1
    rot(ws, f"A{r}", "N (PV)")
    cal(ws, f"B{r}", f"={T('criacao.caminho.n')}", negrito=True)
    rot(ws, f"C{r}", "Bônus de Velocidade")
    cal(ws, f"D{r}", f"={T('criacao.caminho.vel')}", negrito=True)
    rot(ws, f"E{r}", "Perícias do Caminho")
    _mesclar(ws, f"E{r}", "F")
    cal(ws, f"G{r}", f'={T("criacao.caminho.pericia1")}&IF({CAM}="",""," · ")&{T("criacao.caminho.pericia2")}'
                     f'&IF({CAM}="",""," · ")&{T("criacao.caminho.pericia3")}', ate="H")
    r += 1
    rot(ws, f"A{r}", "Recurso próprio")
    cal(ws, f"B{r}", f"={T('criacao.caminho.recurso')}", ate="H")
    c.r = r + 1

    c.passo("Recurso próprio do Caminho (capítulos 07 a 15)")
    r = c.r
    textos = _linhas_recurso()
    for k in range(7):
        f = q("Escolha o Caminho na aba Criação (Passo 3).") if k == 0 else '""'
        for caminho, linhas in textos.items():
            if k < len(linhas):
                f = f"IF({CAM}={q(caminho)},{linhas[k]},{f})"
        cal(ws, f"A{r}", "=" + f, nome=f"caminho.recurso.linha{k + 1}", ate="H")
        r += 1
    c.r = r

    c.passo("Bênçãos com número na ficha")
    r = c.r
    cabecalhos(ws, r, ["Bênção", None, "Custo em PV", "Bônus de dano", "Bônus ferido",
                       "Ferido com PV até", "Como funciona"], altura=30)
    _mesclar(ws, f"A{r}", "B")
    _mesclar(ws, f"G{r}", "H")
    r += 1
    tem_pacto = tem_bencao("Pacto da Ruína")
    rot(ws, f"A{r}", "Pacto da Ruína (7.3, nº 1)")
    _mesclar(ws, f"A{r}", "B")
    cal(ws, f"C{r}", f'=IF({tem_pacto},2*{LV},"")', nome="caminho.pacto.custo_pv", negrito=True)
    cal(ws, f"D{r}", f'=IF({tem_pacto},{EF},"")', nome="caminho.pacto.bonus", negrito=True)
    cal(ws, f"E{r}", f'=IF({tem_pacto},2*{EF},"")', nome="caminho.pacto.bonus_ferido", negrito=True)
    cal(ws, f"F{r}", f'=IF({tem_pacto},INT({T("criacao.pv")}/2),"")', nome="caminho.pacto.limiar_pv",
        negrito=True)
    cal(ws, f"G{r}", f'=IF({tem_pacto},"Uma vez por turno: pague o custo e some o bônus ao dano; '
                     f'dobra com metade dos PV ou menos","Só com a Bênção Pacto da Ruína")', ate="H", quebra=True)
    ws.row_dimensions[r].height = 30
    c.r = r + 1


def caminho_slots(c):
    ws = c.ws
    c.passo("Bênçãos adquiridas — uma por nível ímpar (06.7); o Tier I cabe em qualquer slot")
    r = c.r
    rot(ws, f"A{r}", "Possuídas / permitidas no nível")
    r_cont = r
    r += 1
    cabecalhos(ws, r, ["Slot", "Nível do slot", "Bênção (preencha)", "Tier", "Requisito (nível)",
                       "Liberado?", "Em uma linha", "Frequência", "Conta na ficha", None, None, "Aviso"])
    r += 1
    bc, bn, bt, br_ = (dcol("bencaos", "Caminho"), dcol("bencaos", "Bênção"), dcol("bencaos", "Tier"),
                       dcol("bencaos", "Requisito (nível)"))
    r0 = r
    # lista dependente: as 12 Bênçãos do Caminho, na coluna N
    texto(ws, f"N{r - 1}", "Lista auxiliar: Bênçãos do Caminho", negrito=True)
    for k in range(12):
        aux(ws, f"N{r0 + k}", f'=IF({CAM}="","",IFERROR(INDEX({bn},MATCH({CAM},{bc},0)+{k}),""))',
            nome=f"caminho.lista_bencaos.{k + 1}")
    lista = f"$N${r0}:$N${r0 + 11}"
    for k in range(1, 11):
        nivel_slot = 2 * k - 1
        base = f"caminho.bencao.slot{k}"
        texto(ws, f"A{r}", f"Slot {k}", negrito=True)
        cal(ws, f"B{r}", nivel_slot, nome=f"{base}.nivel")
        ent(ws, f"C{r}", f"{base}.nome", "lista", lista, amostra="Pacto da Ruína",
            invalido="Bênção Inventada", rotulo=f"Bênção do slot {k}")
        C = T(f"{base}.nome")
        m = f"MATCH({C},{bn},0)"
        cal(ws, f"D{r}", f'=IF({C}="","",IFERROR(INDEX({bt},{m}),"—"))', nome=f"{base}.tier")
        cal(ws, f"E{r}", f'=IF({C}="","",IFERROR(INDEX({br_},{m}),""))', nome=f"{base}.requisito")
        cal(ws, f"F{r}", f'=IF({LV}>={nivel_slot},"Sim","Não (nível {nivel_slot})")', nome=f"{base}.liberado")
        cal(ws, f"G{r}", f'=IF({C}="","",IFERROR(INDEX({dcol("bencaos", "Em uma linha")},{m}),'
                         f'"Fora do catálogo dos capítulos 07 a 15"))', nome=f"{base}.resumo", quebra=True)
        cal(ws, f"H{r}", f'=IF({C}="","",IFERROR(INDEX({dcol("bencaos", "Frequência")},{m}),""))',
            nome=f"{base}.frequencia")
        cal(ws, f"I{r}", f'=IF(AND({C}<>"",{LV}>={nivel_slot}),{C},"")', nome=f"{base}.ativa", quebra=True)
        av(ws, f"{AV}{r}", f"caminho.aviso.slot{k}",
           f'=IF({C}="","",IF({LV}<{nivel_slot},"Slot ainda não liberado (nível {nivel_slot}). ","")&'
           f'IF(ISERROR({m}),"Bênção fora do catálogo dos capítulos 07 a 15. ",'
           f'IF(INDEX({bc},{m})<>{CAM},"Bênção de outro Caminho ("&INDEX({bc},{m})&"). ",'
           f'IF(INDEX({br_},{m})>{nivel_slot},"Tier "&INDEX({bt},{m})&" exige slot de nível "&'
           f'INDEX({br_},{m})&" ou mais. ","")))&IF(COUNTIF($C${r0}:$C${r0 + 9},{C})>1,"Bênção repetida.",""))')
        ws.row_dimensions[r].height = 30
        r += 1
    reg("caminho.bencoes.nomes", ws, f"C{r0}:C{r - 1}")
    reg("caminho.bencoes.ativas", ws, f"I{r0}:I{r - 1}")
    cal(ws, f"B{r_cont}", f'=SUMPRODUCT((LEN({T("caminho.bencoes.ativas")})>0)*1)',
        nome="caminho.bencoes.possuidas", negrito=True)
    cal(ws, f"C{r_cont}", f'="de "&{T("nucleo.bencaos")}&" permitidas no nível "&{LV}', ate="E")
    c.r = r

    c.passo("Catálogo das 12 Bênçãos do seu Caminho")
    r = c.r
    cabecalhos(ws, r, ["Nº", None, "Bênção", "Tier", "Requisito (nível)", "Pode escolher agora?",
                       "Em uma linha", "Frequência"], altura=30)
    r += 1
    for k in range(1, 13):
        nome = T(f"caminho.lista_bencaos.{k}")
        m = f"MATCH({nome},{bn},0)"
        base = f"caminho.catalogo.{k}"
        texto(ws, f"A{r}", k, negrito=True)
        cal(ws, f"C{r}", f"={nome}", nome=f"{base}.nome")
        cal(ws, f"D{r}", f'=IF({nome}="","",IFERROR(INDEX({bt},{m}),""))')
        cal(ws, f"E{r}", f'=IF({nome}="","",IFERROR(INDEX({br_},{m}),""))', nome=f"{base}.requisito")
        req = T(f"{base}.requisito")
        cal(ws, f"F{r}", f'=IF({nome}="","",IF(COUNTIF({T("caminho.bencoes.nomes")},{nome})>0,"Já escolhida",'
                         f'IF({LV}>={req},"Sim","A partir do nível "&{req})))', nome=f"{base}.pode", quebra=True)
        cal(ws, f"G{r}", f'=IF({nome}="","",IFERROR(INDEX({dcol("bencaos", "Em uma linha")},{m}),""))',
            quebra=True)
        cal(ws, f"H{r}", f'=IF({nome}="","",IFERROR(INDEX({dcol("bencaos", "Frequência")},{m}),""))')
        ws.row_dimensions[r].height = 30
        r += 1
    c.r = r


def caminho_memoespirito(c):
    """Bloco do Memoespírito (11.3 a 11.5); cinza e vazio fora da Recordação."""
    ws = c.ws
    c.r += 1
    r_ini = c.r
    cal(ws, f"A{r_ini}", f'=IF({CAM}="A Recordação","Memoespírito — 11.3 a 11.5",'
                         f'"Memoespírito — só para A Recordação")')
    titulo(ws, f"A{r_ini}", ws[f"A{r_ini}"].value, ate=AV)
    reg("memo.titulo", ws, f"A{r_ini}")
    r = r_ini + 1
    rot(ws, f"A{r}", "Só para A Recordação?")
    cal(ws, f"B{r}", f'=IF({CAM}="A Recordação","Sim","Não")', nome="memo.ativo", negrito=True)
    ativo_cel = f"$B${r}"
    rec = f'({T("memo.ativo")}="Sim")'
    r_aviso_geral = r
    r += 1
    campos_texto = []
    for nome, rotulo, tipo, fonte in (("nome", "Nome do Memoespírito", "texto", None),
                                      ("conceito", "Conceito (11.3 Passo 2)", "lista", "memo_conceito"),
                                      ("funcao", "Função (11.3 Passo 3)", "lista", "memo_funcao"),
                                      ("elemento", "Elemento dele", "lista", "elementos")):
        rot(ws, f"A{r}", rotulo)
        if tipo == "texto":
            ent(ws, f"B{r}", f"memo.{nome}", ate="E", rotulo=rotulo)
        else:
            ent(ws, f"B{r}", f"memo.{nome}", "lista", fonte, ate="C", rotulo=rotulo)
        campos_texto.append(T(f"memo.{nome}"))
        if nome == "funcao":
            fn = T("memo.funcao")
            cal(ws, f"D{r}", f'=IF(OR(NOT({rec}),{fn}=""),"",IFERROR(VLOOKUP({fn},{dtab("memo_funcao")},2,FALSE),""))',
                ate="H", quebra=True)
            ws.row_dimensions[r].height = 30
        if nome == "conceito":
            cn = T("memo.conceito")
            cal(ws, f"D{r}", f'=IF(OR(NOT({rec}),{cn}=""),"",IFERROR(VLOOKUP({cn},{dtab("memo_conceito")},2,FALSE),""))',
                ate="H")
        r += 1

    # Pontos por atributo
    cabecalhos(ws, r, ["Atributo", "Pontos (preencha, máx. 5)", "Pontos usados", "Teste de Resistência dele"],
               altura=30)
    cabecalho(ws, f"{AV}{r}", "Aviso")
    r += 1
    r0 = r
    for a in ATRS:
        s = slug(a)
        texto(ws, f"A{r}", a, negrito=True)
        ent(ws, f"B{r}", f"memo.pontos.{s}", "inteiro", minimo=0, maximo=5, amostra=3, invalido=9,
            rotulo=f"Pontos em {a}")
        P = T(f"memo.pontos.{s}")
        campos_texto.append(P)
        cal(ws, f"C{r}", f"=IF(ISNUMBER({P}),MAX(0,MIN(5,INT({P}))),0)", nome=f"memo.usado.{s}")
        U = T(f"memo.usado.{s}")
        cal(ws, f"D{r}", f'=IF({rec},{rolagem(f"({U}+{EF})")},"")', nome=f"memo.tr.{s}")
        av(ws, f"{AV}{r}", f"memo.aviso.pontos.{s}",
           f'=IF({P}="","",IF(ISNUMBER({P}),IF({P}>5,"Máximo 5 pontos por Atributo","")&'
           f'IF({P}<0,"Pontos não podem ser negativos",""),"Precisa ser um número"))')
        r += 1
    reg("memo.pontos", ws, f"B{r0}:B{r - 1}")
    reg("memo.usados", ws, f"C{r0}:C{r - 1}")
    reg("memo.nomes", ws, f"A{r0}:A{r - 1}")
    rot(ws, f"A{r}", "Pontos totais (12 + metade do nível) / gastos")
    cal(ws, f"B{r}", f'=IF({rec},{T("nucleo.pontos_memo")},"")', nome="memo.pontos_total", negrito=True)
    cal(ws, f"C{r}", f"=SUM({T('memo.pontos')})", nome="memo.pontos_gastos", negrito=True)
    av(ws, f"{AV}{r}", "memo.aviso.pontos_total",
       f'=IF(AND({rec},{T("memo.pontos_gastos")}>{T("nucleo.pontos_memo")}),"Pontos acima do total ("&'
       f'{T("nucleo.pontos_memo")}&")","")')
    r += 1
    rot(ws, f"A{r}", "Atributo de ataque dele (vazio = Poder)")
    ent(ws, f"B{r}", "memo.atributo_ataque", "lista", "atributos", ate="C", rotulo="Atributo de ataque")
    campos_texto.append(T("memo.atributo_ataque"))
    atk = T("memo.atributo_ataque")
    cal(ws, f"D{r}", f'=IF({atk}="","Poder",{atk})', nome="memo.atributo_ataque.usado", ate="E")
    r += 1

    # Bônus menores
    cabecalhos(ws, r, ["Bônus menor (11.3 Passo 4)", "Escolha (preencha)", None, "Efeito"], altura=None)
    r += 1
    r0 = r
    for k in range(1, 4):
        texto(ws, f"A{r}", f"Bônus menor {k}", negrito=True)
        ent(ws, f"B{r}", f"memo.bonus_menor.{k}", "lista", "memo_bonus", ate="C", rotulo=f"Bônus menor {k}")
        bm = T(f"memo.bonus_menor.{k}")
        campos_texto.append(bm)
        cal(ws, f"D{r}", f'=IF({bm}="","",IFERROR(VLOOKUP({bm},{dtab("memo_bonus")},2,FALSE),""))', ate="H",
            quebra=True)
        ws.row_dimensions[r].height = 30
        av(ws, f"{AV}{r}", f"memo.aviso.bonus_menor.{k}",
           f'=IF({bm}="","",IF(COUNTIF($B${r0}:$B${r0 + 2},{bm})>1,"Bônus menor repetido: escolha 3 diferentes",'
           f'IF(COUNTIF({dlista("memo_bonus")},{bm})=0,"Fora da lista de 11.3","")))')
        r += 1
    reg("memo.bonus_menores", ws, f"B{r0}:B{r - 1}")

    # Técnicas
    for nome, rotulo in (("principal", "Técnica Principal"), ("auxiliar", "Técnica Auxiliar")):
        rot(ws, f"A{r}", f"{rotulo}: nome")
        ent(ws, f"B{r}", f"memo.tecnica_{nome}.nome", ate="C", rotulo=rotulo)
        rot(ws, f"D{r}", "o que faz")
        ent(ws, f"E{r}", f"memo.tecnica_{nome}.texto", ate="H", rotulo=rotulo)
        campos_texto += [T(f"memo.tecnica_{nome}.nome"), T(f"memo.tecnica_{nome}.texto")]
        r += 1

    # Evoluções
    cabecalhos(ws, r, ["Evolução (11.3)", "Nível", "Escolha (preencha)", "Efeito"], altura=None)
    r += 1
    r0 = r
    for k, nv in enumerate((8, 14, 20), start=1):
        texto(ws, f"A{r}", f"Evolução {k}", negrito=True)
        cal(ws, f"B{r}", nv)
        ent(ws, f"C{r}", f"memo.evolucao.{k}", "lista", "memo_evolucoes", rotulo=f"Evolução do nível {nv}")
        ev = T(f"memo.evolucao.{k}")
        campos_texto.append(ev)
        cal(ws, f"D{r}", f'=IF({ev}="","",IFERROR(VLOOKUP({ev},{dtab("memo_evolucoes")},2,FALSE),""))', ate="H",
            quebra=True)
        ws.row_dimensions[r].height = 30
        av(ws, f"{AV}{r}", f"memo.aviso.evolucao.{k}",
           f'=IF({ev}="","",IF({LV}<{nv},"Só a partir do nível {nv}. ","")&'
           f'IF(COUNTIF($C${r0}:$C${r0 + 2},{ev})>1,"Evolução repetida: cada uma só uma vez.",""))')
        r += 1
    reg("memo.evolucoes", ws, f"C{r0}:C{r - 1}")
    rot(ws, f"A{r}", "Memória Desperta: +2 em")
    ent(ws, f"B{r}", "memo.memoria_desperta", "lista", '"Defesa,Velocidade"', amostra="Velocidade",
        rotulo="Memória Desperta", ate="C")
    campos_texto.append(T("memo.memoria_desperta"))
    r += 1

    # Estatísticas (11.4)
    titulo(ws, f"A{r}", "Estatísticas do Memoespírito (11.4, com Função, Bônus menores, Evoluções e Bênçãos)",
           ate=AV)
    r += 1
    usado = lambda a: T(f"memo.usado.{slug(a)}")  # noqa: E731
    fn = T("memo.funcao")
    menor = lambda x: f'(COUNTIF({T("memo.bonus_menores")},{q(x)})>0)'  # noqa: E731
    evol = lambda x: f'(COUNTIF({T("memo.evolucoes")},{q(x)})>0)'  # noqa: E731
    desp = T("memo.memoria_desperta")
    p_atk = (f'IFERROR(INDEX({T("memo.usados")},MATCH({T("memo.atributo_ataque.usado")},'
             f'{T("memo.nomes")},0)),0)')
    bah = T("criacao.bonus_habilidade")
    ecos = tem_bencao("Ecos do Passado")
    stats = [
        ("pv", "PV", f'=IF({rec},8*{LV}+3*{usado("Vigor")}+IF({fn}="Guardião",3*{LV},0)+'
                     f'IF({menor("Resistência Espiritual")},2*{LV},0)+IF({ecos},4*{LV},0),"")'),
        ("defesa", "Defesa", f'=IF({rec},10+{usado("Agilidade")}+{EF}+IF(AND({evol("Memória Desperta")},'
                             f'{desp}<>"Velocidade"),2,0),"")'),
        ("velocidade", "Velocidade", f'=IF({rec},10+{usado("Agilidade")}+{T("criacao.caminho.vel")}+'
                                     f'IF({menor("Velocidade Espiritual")},2,0)+IF(AND({evol("Memória Desperta")},'
                                     f'{desp}="Velocidade"),2,0),"")'),
        ("ataque", "Teste de Ataque (número)", f'=IF({rec},{bah}+{p_atk}+{EF},"")'),
        ("ataque.rolagem", "Teste de Ataque", f'=IF({rec},{rolagem(T("memo.ataque"))},"")'),
        # fora da Recordação o bloco fica vazio como as outras contas (auditoria visual)
        # 11.4 (v1.2, E17): a quantidade de dados é a da arma do dono, incluindo o dado extra da
        # categoria Energia (coluna 3 da tabela de armas de 24.2, que vale 2 nela e 1 nas outras).
        # A face é sempre d6, do Memoespírito, nunca a da arma.
        ("n", "Dados de dano (d6)", f'=IF({rec},{T("nucleo.dados_ab")}'
                                    f'+IF({T("criacao.arma.categoria")}="",0,'
                                    f'IFERROR(VLOOKUP({T("criacao.arma.categoria")},{dtab("armas")},3,FALSE),1)-1)'
                                    f'+IF({evol("Forma Completa")},1,0),"")'),
        ("fixo", "Dano fixo", f'=IF({rec},{p_atk}+IF({menor("Força Espiritual")},2,0)+IF({ecos},{bah},0),"")'),
        ("dano", "Dano do ataque", f'=IF({rec},{texto_dano(T("memo.n"), 6, T("memo.fixo"))},"")'),
        ("media", "Média do dano", f'=IF({rec},INT({T("memo.n")}*7/2)+{T("memo.fixo")},"")'),
        ("media_fraqueza", "Média contra Fraqueza (+2 dados)",
         f'=IF({rec},INT(({T("memo.n")}+2)*7/2)+{T("memo.fixo")},"")'),
        ("rt", "Redução de Tenacidade", f'=IF({rec},IF({LV}>=11,2,1)+IF({tem_bencao("Eternidade Recordada")},1,0),"")'),
        ("rd", "RD", f'=IF({rec},IF({menor("Resistência Espiritual")},1,0),"")'),
        ("predador", "Função Predador", f'=IF(AND({rec},{fn}="Predador"),"+1d8 de dano nos ataques dele","")'),
    ]
    for campo, rotulo, formula in stats:
        rot(ws, f"A{r}", rotulo)
        cal(ws, f"B{r}", formula, nome=f"memo.{campo}", negrito=True, ate="C")
        r += 1
    rot(ws, f"D{r_ini + 1}", "Fora da Recordação o bloco fica cinza e as contas ficam vazias.")
    _mesclar(ws, f"D{r_ini + 1}", "H")
    av(ws, f"{AV}{r_aviso_geral}", "memo.aviso.fora_da_recordacao",
       f'=IF(AND(NOT({rec}),({"+".join(f"LEN({x})" for x in campos_texto)})>0),'
       f'"Memoespírito só na Recordação: estes campos não contam","")')
    cinza = PatternFill(start_color=COR_NA, end_color=COR_NA, fill_type="solid")
    ws.conditional_formatting.add(f"A{r_ini + 1}:K{r - 1}", FormulaRule(
        formula=[f'{ativo_cel}="Não"'], fill=cinza, font=Font(color=COR_NA_TEXTO)))
    c.r = r


def caminho_escolhas(c):
    """Escolhas permanentes feitas ao adquirir uma Bênção (11, nº 5 e nº 11). Entram nos
    números pela decisão 2 (Memória da Guarda, Forma Sincronizada)."""
    ws = c.ws
    c.passo("Escolhas permanentes de Bênção (só vale com a Bênção adquirida)")
    r = c.r
    for nome, bencao, rotulo, opcoes, efeito in (
            ("fragmentos", "Fragmentos do Eu Perdido", "Fragmentos do Eu Perdido: Memória escolhida",
             "Fúria,Guarda,Sabedoria",
             '"Fúria: +1d8 nos ataques dele e nos seus com ele ativo · Guarda: +Eficiência de Defesa com '
             'ele ativo · Sabedoria: Eficácia em um Teste de Perícia, 2 vezes por dia"'),
            ("avatar", "Avatar da Recordação", "Avatar da Recordação: Forma escolhida",
             "Manifestada,Sincronizada",
             '"Manifestada: o Memoespírito ganha +1 Distância e +2 dados · Sincronizada: você ganha PV '
             '+2 × nível, +1 de Defesa e +1 dado base nos seus ataques"')):
        rot(ws, f"A{r}", rotulo)
        ent(ws, f"B{r}", f"caminho.escolha.{nome}", "lista", q(opcoes), amostra=opcoes.split(",")[-1],
            rotulo=rotulo, ate="C")
        cal(ws, f"D{r}", "=" + efeito, ate="I", quebra=True)
        ws.row_dimensions[r].height = 30
        esc = T(f"caminho.escolha.{nome}")
        av(ws, f"{AV}{r}", f"caminho.aviso.escolha.{nome}",
           f'=IF({esc}="","",IF(OR({",".join(f"{esc}={q(o)}" for o in opcoes.split(","))}),"",'
           f'"Escolha uma opção da lista. ")&IF({tem_bencao(bencao)},"",{q("Só vale com a Bênção " + bencao + " num slot liberado.")}))')
        r += 1
    c.r = r


def aba_caminho(ws):
    # A:L = 1359 px (área do jogador em 1360 px; M:N são auxiliares ocultas)
    # E só tem números curtos e H/I quebram em 2 linhas (auditoria visual final): o espaço vai
    # para o aviso dos slots (K:L), que
    # encaixar_na_tela apara se a área passar de 1360 px. B fica em 12 para a legenda caber
    larguras(ws, {"A": 24, "B": 12, "C": 29, "D": 9, "E": 10, "F": 17, "G": 26.7, "H": 13.6, "I": 14,
                  "J": 1, "K": 1, "L": 30, "M": 2, "N": 30})
    c = Cursor(ws, 5)
    caminho_ficha(c)
    caminho_slots(c)
    caminho_memoespirito(c)
    caminho_escolhas(c)


# ---------------------------------------------------------------------------
# Aba Equipamento — armas, Cone de Luz, Relíquias, Conjuntos, inventário, Créditos
# ---------------------------------------------------------------------------

CONE_TR, CONE_PERICIA = "Um Teste de Resistência", "Uma Perícia"
CONE_ALVOS = [  # (campo no mapa, texto do alvo na lista alvo_cone, cabeçalho)
    ("defesa", "Defesa", "Defesa"), ("velocidade", "Velocidade", "Velocidade"),
    ("dano_ab", "Dano de Ataque Básico", "Dano de Ataque Básico"),
    ("dano_habilidade", "Dano de Habilidade", "Dano de Habilidade"),
    ("dano_ultimate", "Dano de Ultimate", "Dano de Ultimate"), ("rd", "RD", "RD"),
    ("ataque", "Teste de Ataque", "Teste de Ataque"),
]


def _bonus_do_atributo(atr):
    """Bônus atual do Atributo cujo nome está na expressão `atr` (0 se vazio)."""
    return (f'IFERROR(INDEX({T("criacao.atributos.bonus")},MATCH({atr},'
            f'{T("criacao.atributos.nomes")},0)),0)')


def _ab_resultados(ws, r, base, cat, atr, prop, elem):
    """Linha do Ataque Básico de uma arma (18.2 e 18.5). Auxiliares em P:T."""
    arma = dtab("armas")
    alc = dlista("alcances")
    n_, f_, fx_, eq_, atk = (T(f"{base}.{x}") for x in ("n", "face", "fixo", "equip", "ataque"))
    aux(ws, f"P{r}", f'=IF({cat}="",0,{T("nucleo.dados_ab")}+IFERROR(VLOOKUP({cat},{arma},3,FALSE),1)-1'
                     f'+IF({_forma_sincronizada()},1,0))', nome=f"{base}.n")
    aux(ws, f"Q{r}", f"=IFERROR(VLOOKUP({cat},{arma},4,FALSE),0)", nome=f"{base}.face")
    aux(ws, f"R{r}", f"={_bonus_do_atributo(atr)}", nome=f"{base}.fixo")
    aux(ws, f"S{r}", f'={T("equipamento.reliquia.maos.bonus")}+{T("equipamento.cone.em.dano_ab")}'
                     f'+{T("equipamento.conjuntos.dano")}', nome=f"{base}.equip")
    aux(ws, f"T{r}", f'={_bonus_do_atributo(atr)}+{EF}+{T("nucleo.especializacao")}+{T("criacao.extra.ataque")}',
        nome=f"{base}.ataque")
    vz = f'{cat}=""'
    total = f"({fx_}+{eq_})"
    cal(ws, f"B{r}", f'=IF({vz},"—",{rolagem(atk)})', nome=f"{base}.rolagem", negrito=True)
    # Dano = dados + atributo + equipamento (18.2, 25.3 Mãos). Regra única desde a v1.1: o exemplo
    # de 29.7 passou a somar Mãos I (1d12 + 4 + 2 = 1d12 + 6), então a coluna "como no livro" saiu (D1)
    cal(ws, f"C{r}", f'=IF({vz},"",{texto_dano(n_, f_, total)})', nome=f"{base}.texto", negrito=True)
    cal(ws, f"D{r}", f'=IF({vz},"",INT({n_}*({f_}+1)/2)+{total})', nome=f"{base}.media", negrito=True)
    cal(ws, f"E{r}", f'=IF({vz},"",{fx_})', nome=f"{base}.do_atributo")
    cal(ws, f"F{r}", f'=IF({vz},"",{eq_})', nome=f"{base}.do_equipamento")
    cal(ws, f"G{r}", f'=IF({vz},"",{texto_dano(f"({n_}+2)", f_, total)})', nome=f"{base}.fraqueza")
    cal(ws, f"H{r}", f'=IF({vz},"",INT(({n_}+2)*({f_}+1)/2)+{total})', nome=f"{base}.media_fraqueza")
    cal(ws, f"I{r}", f'=IF({vz},"",IF({tem_bencao("Olho de Lan")},"19-20","20"))', nome=f"{base}.critico")
    cal(ws, f"J{r}", f'=IF({vz},"",1+IF({prop}="Peso de impacto",1,0))', nome=f"{base}.rt")
    cal(ws, f"K{r}", f'=IF({vz},"",IFERROR(INDEX({alc},MIN(5,MATCH(VLOOKUP({cat},{arma},5,FALSE),{alc},0)'
                     f'+IF({prop}="Alcance estendido",1,0))),""))', nome=f"{base}.alcance")
    cal(ws, f"L{r}", f'=IF({vz},"",{elem})', nome=f"{base}.elemento")


def equip_armas(c):
    ws = c.ws
    arma = dtab("armas")
    c.titulo("Armas e armadura — a arma principal e a armadura vêm da aba Criação (Passos 8 e 12)")
    r = c.r
    cabecalhos(ws, r, ["Arma", "Nome", "Categoria", "Atributo (só arma Média)", "Elemento próprio",
                       "Propriedade especial", "Espaço", "Dados base", "Atributo de ataque",
                       "Elemento do Ataque Básico", None, "Aviso"], altura=30)
    r += 1
    # Principal: espelho da Criação (nenhuma entrada em dois lugares — decisão 12)
    texto(ws, f"A{r}", "Principal (edite na aba Criação)", negrito=True)
    for col, nome in (("B", "criacao.arma.nome"), ("C", "criacao.arma.categoria"),
                      ("D", "criacao.arma.atributo_media"), ("E", "criacao.arma.elemento_proprio")):
        x = T(nome)
        cal(ws, f"{col}{r}", f'=IF(LEN({x})=0,"—",""&{x})', quebra=True)
    prop1 = T("criacao.arma.propriedade")
    cal(ws, f"F{r}", f'=IF(LEN({prop1})=0,"Nenhuma",""&{prop1})')
    cal(ws, f"G{r}", f'={T("criacao.arma.espaco")}', nome="equipamento.arma1.espaco")
    cat1 = T("criacao.arma.categoria")
    cal(ws, f"H{r}", f'=IF({cat1}="","",IFERROR(VLOOKUP({cat1},{arma},2,FALSE),""))')
    cal(ws, f"I{r}", f'={T("criacao.arma.atributo")}')
    cal(ws, f"J{r}", f'=IF({cat1}="","",{T("criacao.arma.elemento")})')
    r += 1
    # Secundária: entrada desta aba
    texto(ws, f"A{r}", "Secundária (preencha)", negrito=True)
    ent(ws, f"B{r}", "equipamento.arma2.nome", rotulo="Arma secundária")
    ent(ws, f"C{r}", "equipamento.arma2.categoria", "lista", "armas", amostra="Disparo longo", invalido="Laser",
        rotulo="Categoria da arma secundária")
    ent(ws, f"D{r}", "equipamento.arma2.atributo_media", "lista", "atributo_media",
        rotulo="Atributo da arma secundária")
    ent(ws, f"E{r}", "equipamento.arma2.elemento_proprio", "lista", "elementos", invalido="Plasma",
        rotulo="Elemento da arma secundária")
    ent(ws, f"F{r}", "equipamento.arma2.propriedade", "lista", "propriedades", amostra="Dissimulada",
        invalido="Arremessável, Dissimulada", rotulo="Propriedade da arma secundária")
    cat2, atr2, ela2, prop2 = (T(f"equipamento.arma2.{x}") for x in
                               ("categoria", "atributo_media", "elemento_proprio", "propriedade"))
    cal(ws, f"G{r}", f'=IF({cat2}="",0,IF({prop2}="Dissimulada",0.5,IFERROR(VLOOKUP({cat2},{arma},8,FALSE),0)))',
        nome="equipamento.arma2.espaco")
    cal(ws, f"H{r}", f'=IF({cat2}="","",IFERROR(VLOOKUP({cat2},{arma},2,FALSE),""))')
    cal(ws, f"I{r}", f'=IF({cat2}="","",IF({cat2}="Média",IF(OR({atr2}="Poder",{atr2}="Agilidade"),{atr2},'
                     f'"Poder"),IFERROR(VLOOKUP({cat2},{arma},6,FALSE),"")))', nome="equipamento.arma2.atributo")
    cal(ws, f"J{r}", f'=IF({cat2}="","",IF({ela2}="","Físico",{ela2}))', nome="equipamento.arma2.elemento")
    av(ws, f"{AV}{r}", "equipamento.aviso.arma2",
       f'=IF(AND({cat2}<>"",COUNTIF({dlista("armas")},{cat2})=0),"Categoria fora da lista do capítulo 24. ","")'
       f'&IF(AND({atr2}<>"",{cat2}<>"Média"),"O atributo só se escolhe na arma Média. ","")'
       f'&IF(AND({cat2}="Média",{atr2}=""),"Arma Média: escolha Poder ou Agilidade (contando Poder). ","")'
       f'&IF(AND({ela2}<>"",COUNTIF({dlista("elementos")},{ela2})=0),"Elemento fora da lista do capítulo 20. ","")'
       f'&IF(AND({prop2}<>"",COUNTIF({dlista("propriedades")},{prop2})=0),'
       f'"Só uma propriedade especial por arma (24.2): escolha uma da lista. ","")'
       f'&IF(AND({cat2}="",OR(LEN({T("equipamento.arma2.nome")})>0,{atr2}<>"",{ela2}<>"",{prop2}<>"")),'
       f'"Escolha a categoria da arma secundária.","")')
    r += 1
    texto(ws, f"A{r}", "Armadura (edite na aba Criação)", negrito=True)
    arm = T("criacao.armadura")
    cal(ws, f"B{r}", f'=IF(LEN({arm})=0,"Sem armadura",""&{arm})')
    cal(ws, f"C{r}", f'="Defesa +"&{T("criacao.armadura.defesa")}')
    cal(ws, f"D{r}", f'="RD "&{T("criacao.armadura.rd")}')
    cal(ws, f"E{r}", f'="Velocidade "&{sinal(T("criacao.armadura.vel"))}')
    cal(ws, f"F{r}", f'="Esquiva: "&{T("criacao.armadura.esquiva")}')
    cal(ws, f"G{r}", f'=IFERROR(VLOOKUP({arm},{dtab("armaduras")},5,FALSE),0)', nome="equipamento.armadura.espaco")
    c.r = r + 1

    c.passo("Ataque Básico — 18.2 e 18.5 (dano = dados + atributo + equipamento: Mãos, Cone e Conjuntos, 25.3)")
    r = c.r
    cabecalhos(ws, r, ["Arma", "Teste de Ataque", "Dano", "Média", "Fixo do atributo",
                       "Fixo do equipamento", "Contra Fraqueza (+2 dados)", "Média", "Crítico", "Redução de Tenacidade",
                       "Alcance", "Elemento"], altura=40)
    cabecalhos(ws, r, ["nº de dados", "face", "dano fixo", "equipamento", "ataque"], coluna=16, altura=None)
    r += 1
    for base, rotulo, cat, atr, prop, elem in (
            ("equipamento.ab.principal", "Principal", cat1, T("criacao.arma.atributo"), prop1,
             T("criacao.arma.elemento")),
            ("equipamento.ab.secundaria", "Secundária", cat2, T("equipamento.arma2.atributo"), prop2,
             T("equipamento.arma2.elemento"))):
        texto(ws, f"A{r}", rotulo, negrito=True)
        _ab_resultados(ws, r, base, cat, atr, prop, elem)
        r += 1
    rot(ws, f"A{r}", "Mãos (Relíquia) soma no Ataque Básico; a Esfera Planar nunca (25.3). Fraqueza: +2 dados "
                     "que não critam; o crítico dobra só os dados base (18.3).")
    _mesclar(ws, f"A{r}", "L")
    c.r = r + 1


def equip_cone(c):
    ws = c.ws
    c.passo("Cone de Luz — 25.2 (Bônus Maior permanente, fora do teto; Efeito Condicional temporário)")
    r = c.r
    NV, ALVO, QUAL, ESC, SOB = (T(f"equipamento.cone.{x}") for x in
                                ("nivel", "alvo", "qual", "escolha", "sobreposicoes"))
    nu, modo, sobu = (T(f"equipamento.cone.{x}") for x in ("nivel_usado", "modo", "sobreposicoes_usadas"))
    ntot, pvtot = T("equipamento.cone.numerico_tabela"), T("equipamento.cone.pv_tabela")
    num, pv = T("equipamento.cone.numerico"), T("equipamento.cone.pv")
    cone = lambda col: dcol("cone", col)  # noqa: E731
    # Sobreposições que ainda cabem no Cone até o numérico chegar a +3 (25.2, v1.1)
    cabem = f'(3-INDEX({cone("Bônus numérico")},{nu}))'
    rot(ws, f"A{r}", "Nome do Cone de Luz")
    ent(ws, f"B{r}", "equipamento.cone.nome", ate="F", rotulo="Cone de Luz")
    r += 1
    rot(ws, f"A{r}", "Nível do Cone (1 a 5)")
    ent(ws, f"B{r}", "equipamento.cone.nivel", "inteiro", minimo=1, maximo=5, amostra=1, rotulo="Nível do Cone")
    cal(ws, f"C{r}", f'="Máximo na sua faixa: Nível "&{FX}&IF({nu}>0," · Bônus Maior da tabela: "&'
                     f'INDEX({cone("Bônus Maior")},{nu}),"")', ate="K")
    av(ws, f"{AV}{r}", "equipamento.aviso.cone.nivel",
       f'=IF(LEN({NV})=0,"",IF(ISNUMBER({NV}),IF(OR({NV}<1,{NV}>5),"O Nível do Cone vai de 1 a 5. ","")&'
       f'IF({nu}>{FX},"Cone de Nível "&{nu}&" acima do máximo da sua faixa (Nível "&{FX}&").",""),'
       f'"Nível precisa ser um número de 1 a 5."))')
    r += 1
    r_qual = r + 1
    lista_qual = f"$Y${r_qual}:$Y${r_qual + 17}"
    rot(ws, f"A{r}", "Alvo do Bônus Maior (escolha um)")
    ent(ws, f"B{r}", "equipamento.cone.alvo", "lista", "alvo_cone", amostra="Defesa", invalido="Sorte", ate="C",
        rotulo="Alvo do Bônus Maior")
    cal(ws, f"D{r}", f'=IF({ALVO}="","Sem alvo, o bônus numérico não conta (o +PV dos Níveis 2 e 4 conta sempre)",'
                     f'"O bônus vai para: "&{ALVO}&IF(LEN({QUAL})>0," ("&{QUAL}&")",""))', ate="K")
    av(ws, f"{AV}{r}", "equipamento.aviso.cone.alvo",
       f'=IF({ALVO}="","",IF(COUNTIF({dlista("alvo_cone")},{ALVO})=0,"Alvo fora da lista de 25.2. ",'
       f'IF(AND(OR({ALVO}={q(CONE_TR)},{ALVO}={q(CONE_PERICIA)}),LEN({QUAL})=0),"Escolha qual "&'
       f'IF({ALVO}={q(CONE_TR)},"Teste de Resistência","Perícia")&" recebe o bônus. ",""))&'
       f'IF({nu}=0,"Preencha o Nível do Cone para o bônus contar.",""))')
    r += 1
    texto(ws, f"Y{r_qual - 1}", "Lista: Teste de Resistência ou Perícia do Cone", negrito=True)
    tr_l, per_l = dlista("tr"), dlista("pericias")
    for k in range(1, 19):
        aux(ws, f"Y{r_qual + k - 1}", f'=IF({ALVO}={q(CONE_TR)},IFERROR(INDEX({tr_l},{k}),""),'
                                      f'IF({ALVO}={q(CONE_PERICIA)},IFERROR(INDEX({per_l},{k}),""),""))')
    rot(ws, f"A{r}", "Qual Teste de Resistência ou Perícia (se o alvo pedir)")
    ent(ws, f"B{r}", "equipamento.cone.qual", "lista", lista_qual, amostra="Reflexos", invalido="Sorte", ate="C",
        rotulo="Teste de Resistência ou Perícia do Cone")
    av(ws, f"{AV}{r}", "equipamento.aviso.cone.qual",
       f'=IF(LEN({QUAL})=0,"",IF(AND({ALVO}<>{q(CONE_TR)},{ALVO}<>{q(CONE_PERICIA)}),'
       f'"Só vale com o alvo Um Teste de Resistência ou Uma Perícia.",'
       f'IF(COUNTIF({lista_qual},{QUAL})=0,"Escolha um nome da lista.","")))')
    r += 1
    rot(ws, f"A{r}", "Numérico ou PV (só nos Níveis 1, 3 e 5)")
    ent(ws, f"B{r}", "equipamento.cone.escolha", "lista", "cone_escolha", amostra="PV", invalido="Os dois",
        rotulo="Numérico ou PV")
    cal(ws, f"C{r}", f'=IF({nu}=0,"",IF({modo}="e","No Nível "&{nu}&" o Cone dá os dois: +"&{ntot}&" e +"&{pvtot}&'
                     f'" PV",IF({ESC}="PV","Vale o PV: +"&{pvtot}&" PV","Vale o numérico: +"&{ntot}&'
                     f'IF({ESC}=""," (vazio = Numérico)",""))))', ate="K")
    av(ws, f"{AV}{r}", "equipamento.aviso.cone.escolha",
       f'=IF({ESC}="","",IF(COUNTIF({dlista("cone_escolha")},{ESC})=0,"Escolha Numérico ou PV.",'
       f'IF({modo}="e","No Nível "&{nu}&" o Cone dá os dois: a escolha não se aplica.","")))')
    r += 1
    rot(ws, f"A{r}", "Sobreposições (cópias extras do mesmo Cone)")
    ent(ws, f"B{r}", "equipamento.cone.sobreposicoes", "inteiro", minimo=0, maximo=5, amostra=1,
        rotulo="Sobreposições")
    cal(ws, f"C{r}", f'="Cada uma: +1 e +10 PV, até o numérico chegar a +3 · no máximo 1 por faixa alcançada ("&'
                     f'{FX}&")"&IF({nu}>0," · este Cone aceita até "&{cabem},"")&" (25.2)"', ate="K")
    av(ws, f"{AV}{r}", "equipamento.aviso.cone.sobreposicoes",
       f'=IF(LEN({SOB})=0,"",IF(ISNUMBER({SOB}),IF({SOB}>{FX},"Sobreposições acima de uma por faixa alcançada '
       f'(máximo "&{FX}&"). ","")&IF({SOB}<0,"Não pode ser negativo. ","")&IF({nu}=0,"Sem Cone: preencha o Nível.",'
       f'IF({sobu}>{cabem},"Acima do teto: o Cone de Nível "&{nu}&" aceita no máximo "&{cabem}&'
       f'" (o numérico para em +3 e o PV para junto, 25.2).","")),"Precisa ser um número."))')
    r += 1
    rot(ws, f"A{r}", "Efeito Condicional (escreva com o Mestre)")
    ent(ws, f"B{r}", "equipamento.cone.efeito", ate="K", rotulo="Efeito Condicional")
    r += 1
    rot(ws, f"A{r}", "Frequência do Efeito Condicional")
    cal(ws, f"B{r}", f'=IF({nu}=0,"",IF({nu}=1,"1 vez por combate","1 vez por Ciclo")&'
                     f'" · temporário: entra no teto de bônus somado (25.4)")', nome="equipamento.cone.frequencia",
        ate="K")
    r += 1
    rot(ws, f"A{r}", "Energia do Cone (17.2)")
    cal(ws, f"B{r}", f'=IF({nu}>=3,"Sim: +5 de Energia, no máximo 1 vez por Ciclo (Efeito Condicional)",'
                     f'IF({nu}=0,"","Não: só no Nível 3 ou maior"))', nome="equipamento.cone.energia", ate="K")
    r += 1
    cabecalhos(ws, r, [None, "Numérico que vale", "PV que vale", "Resumo do Bônus Maior"], altura=30)
    cabecalhos(ws, r, ["nível", "e/ou", "cópias", "numérico", "PV"], coluna=16, altura=None)
    r += 1
    aux(ws, f"P{r}", f'=IF(ISNUMBER({NV}),IF({NV}<1,0,MIN(5,INT({NV}))),0)', nome="equipamento.cone.nivel_usado")
    aux(ws, f"Q{r}", f'=IF({nu}=0,"",INDEX({cone("e/ou")},{nu}))', nome="equipamento.cone.modo")
    aux(ws, f"R{r}", f"=IF(ISNUMBER({SOB}),MAX(0,MIN({FX},INT({SOB}))),0)", nome="equipamento.cone.sobreposicoes_usadas")
    # 25.2 (v1.1, D5): cada Sobreposição soma +1 no numérico e +10 no PV; o numérico para em +3 e o
    # PV para junto (2 Sobreposições nos Níveis 1 e 2, 1 nos 3 e 4, nenhuma no 5)
    aux(ws, f"S{r}", f'=IF({nu}=0,0,INDEX({cone("Bônus numérico")},{nu})+MIN({sobu},{cabem}))',
        nome="equipamento.cone.numerico_tabela")
    aux(ws, f"T{r}", f'=IF({nu}=0,0,INDEX({cone("Bônus de PV")},{nu})+10*MIN({sobu},{cabem}))',
        nome="equipamento.cone.pv_tabela")
    rot(ws, f"A{r}", "Numérico / PV que valem")
    cal(ws, f"B{r}", f'=IF({nu}=0,0,IF({ALVO}="PV máximos",0,IF({modo}="e",{ntot},IF({ESC}="PV",0,{ntot}))))',
        nome="equipamento.cone.numerico", negrito=True)
    cal(ws, f"C{r}", f'=IF({nu}=0,0,IF(OR({ALVO}="PV máximos",{modo}="e",{ESC}="PV"),{pvtot},0))',
        nome="equipamento.cone.pv", negrito=True)
    cal(ws, f"D{r}", f'=IF({nu}=0,"Sem Cone","+"&{num}&IF({ALVO}=""," (sem alvo)"," em "&{ALVO})&'
                     f'IF({pv}>0," · +"&{pv}&" PV máximos",""))', ate="K")
    r += 1
    texto(ws, f"A{r}", "Onde o Bônus Maior entra (automático)", negrito=True)
    r += 1
    cabecalhos(ws, r, ["PV máximos"] + [x[2] for x in CONE_ALVOS] + ["Teste de Resistência", "Perícia"],
               altura=30)
    r += 1
    cal(ws, f"A{r}", f"={pv}", nome="equipamento.cone.em.pv", negrito=True)
    for j, (campo, alvo, _) in enumerate(CONE_ALVOS, start=2):
        cal(ws, f"{get_column_letter(j)}{r}", f'=IF({ALVO}={q(alvo)},{num},0)', nome=f"equipamento.cone.em.{campo}",
            negrito=True)
    cal(ws, f"I{r}", f'=IF(AND({ALVO}={q(CONE_TR)},LEN({QUAL})>0),{num},0)', nome="equipamento.cone.em.tr",
        negrito=True)
    cal(ws, f"J{r}", f'=IF({ALVO}={q(CONE_TR)},""&{QUAL},"")', nome="equipamento.cone.em.tr_nome", quebra=True)
    cal(ws, f"K{r}", f'=IF(AND({ALVO}={q(CONE_PERICIA)},LEN({QUAL})>0),{num},0)', nome="equipamento.cone.em.pericia",
        negrito=True)
    cal(ws, f"L{r}", f'=IF({ALVO}={q(CONE_PERICIA)},""&{QUAL},"")', nome="equipamento.cone.em.pericia_nome",
        quebra=True)
    cabecalho(ws, f"J{r - 1}", "Qual Teste de Resistência")
    cabecalho(ws, f"I{r - 1}", "Teste de Resistência")
    cabecalho(ws, f"K{r - 1}", "Perícia")
    cabecalho(ws, f"L{r - 1}", "Qual Perícia")
    c.r = r + 1


def equip_reliquias(c):
    ws = c.ws
    c.passo("Relíquias — 25.3 (6 slots; o Tier sobe sozinho com o nível; bônus de slot fora do teto)")
    r = c.r
    rot(ws, f"A{r}", "Tier da sua faixa")
    cal(ws, f"B{r}", f'=CHOOSE({T("nucleo.tier_reliquia")},"I","II","III","IV")', nome="equipamento.tier", negrito=True)
    rot(ws, f"C{r}", "Tier I (níveis 1-6) · II (7-12) · III (13-17) · IV (18-20) — recompensa de marco (25.1)")
    _mesclar(ws, f"C{r}", "K")
    r += 1
    cabecalhos(ws, r, ["Slot", "Possui? (Sim)", "Nome da peça", None, "Conjunto (A, B, C ou —)", "Tier", "Bônus",
                       "O que dá", None, "Elemento (só Esfera Planar)", "Vale no seu dano?", "Aviso"], altura=30)
    _mesclar(ws, f"C{r}", "D")
    _mesclar(ws, f"H{r}", "I")
    r += 1
    r0 = r
    tier = T("nucleo.tier_reliquia")
    for k, slot in enumerate(_valores_lista("slots"), start=1):
        base = f"equipamento.reliquia.{slug(slot)}"
        texto(ws, f"A{r}", slot, negrito=True)
        ent(ws, f"B{r}", f"{base}.possui", "lista", "sim_nao", rotulo=f"Possui {slot}")
        ent(ws, f"C{r}", f"{base}.nome", ate="D", rotulo=f"Nome da peça ({slot})")
        ent(ws, f"E{r}", f"{base}.conjunto", "lista", "conjunto", invalido="Z", rotulo=f"Conjunto ({slot})")
        P, CJ, B = T(f"{base}.possui"), T(f"{base}.conjunto"), T(f"{base}.bonus")
        cal(ws, f"F{r}", f'=IF({P}="Sim",{T("equipamento.tier")},"—")', nome=f"{base}.tier")
        cal(ws, f"G{r}", f'=IF({P}="Sim",INDEX({dtab("reliquias")},{k},2+{tier}),0)', nome=f"{base}.bonus",
            negrito=True)
        oque = f'INDEX({dcol("reliquias", "O que dá")},{k})'
        cal(ws, f"H{r}", f'=IF({P}="Sim",{oque}&": +"&{B},{oque})', ate="I")
        extra_av = ""
        if slot == "Esfera Planar":
            ent(ws, f"J{r}", "equipamento.esfera.elemento", "lista", "elementos", amostra="Fogo", invalido="Plasma",
                rotulo="Elemento da Esfera Planar")
            EL, ELP = T("equipamento.esfera.elemento"), T("criacao.elemento")
            cal(ws, f"K{r}", f'=IF({P}<>"Sim","",IF({EL}="","Escolha o Elemento",IF({EL}={ELP},'
                             f'"Sim: +"&{B}&" nas Habilidades e na Ultimate","Não: o seu Elemento é "&'
                             f'IF(LEN({ELP})=0,"(vazio)",{ELP}))))', quebra=True)
            aux(ws, f"P{r}", f'=IF(AND({P}="Sim",{EL}<>"",{EL}={ELP}),{B},0)', nome="equipamento.esfera.vale")
            extra_av = (f'&IF(AND({EL}<>"",COUNTIF({dlista("elementos")},{EL})=0),'
                        f'"Elemento fora da lista do capítulo 20.","")')
        else:
            nao_se_aplica(ws, f"J{r}", "—")
            nao_se_aplica(ws, f"K{r}", "—")
        if slot == "Corda de Ligação":
            cal(ws, f"K{r}", f'=IF({P}="Sim","+"&{B}&" de Energia ao entrar na Fila, 1 vez por combate","")',
                quebra=True)
        av(ws, f"{AV}{r}", f"equipamento.aviso.reliquia.{slug(slot)}",
           f'=IF(AND({CJ}<>"",{CJ}<>"—",{P}<>"Sim"),"A peça só conta para o Conjunto com Possui = Sim. ","")'
           f'&IF(AND({CJ}<>"",COUNTIF({dlista("conjunto")},{CJ})=0),"Conjunto: use A, B, C ou —. ","")'
           f'&IF(AND({P}<>"",{P}<>"Sim",{P}<>"Não"),"Possui: use Sim ou Não. ","")' + extra_av)
        ws.row_dimensions[r].height = 38          # K: até 3 linhas ("+25 de Energia ao entrar na Fila...")
        r += 1
    reg("equipamento.reliquias.possui", ws, f"B{r0}:B{r - 1}")
    reg("equipamento.reliquias.conjunto", ws, f"E{r0}:E{r - 1}")
    c.r = r


def equip_conjuntos(c):
    ws = c.ws
    c.passo("Conjuntos de Relíquias — 25.3 (2 peças: bônus pequeno; 4 peças: efeito por Ciclo; "
            "teto +3, dentro do teto global)")
    r = c.r
    # o Efeito de 4 peças (texto longo) ganhou uma tabela própria logo abaixo, com a largura toda
    cabecalhos(ws, r, ["Conjunto", "Nome do Conjunto (preencha)", "Bônus de 2 peças (preencha)", None,
                       "Qual rolagem (só no Um tipo de rolagem +1)", None, "Peças", "Ativo", "Aviso"], altura=40)
    for a, b in (("C", "D"), ("E", "F"), ("I", "L")):
        _mesclar(ws, f"{a}{r}", b)
    cabecalhos(ws, r, ["rolagem", "VEL", "RD", "dano"], coluna=16, altura=None)
    # lista auxiliar das rolagens: Teste de Ataque, 6 TR e 18 Perícias
    rolagens = ["Teste de Ataque"] + _valores_lista("tr") + _valores_lista("pericias")
    texto(ws, f"AA{r}", "Lista: rolagens do Conjunto", negrito=True)
    for k, nome in enumerate(rolagens, start=1):
        aux(ws, f"AA{r + k}", nome)
    lista_rol = f"$AA${r + 1}:$AA${r + len(rolagens)}"
    r += 1
    r0 = r
    for letra in "ABC":
        base = f"equipamento.conjunto.{letra.lower()}"
        texto(ws, f"A{r}", letra, negrito=True)
        ent(ws, f"B{r}", f"{base}.nome", rotulo=f"Nome do Conjunto {letra}")
        ent(ws, f"C{r}", f"{base}.bonus2", "lista", "bonus_conjunto2", invalido="+5 em tudo", ate="D",
            rotulo=f"Bônus de 2 peças do Conjunto {letra}")
        ent(ws, f"E{r}", f"{base}.rolagem", "lista", lista_rol, amostra="Teste de Ataque", invalido="Sorte", ate="F",
            rotulo=f"Rolagem do Conjunto {letra}")
        B2, RL, PC = T(f"{base}.bonus2"), T(f"{base}.rolagem"), T(f"{base}.pecas")
        cal(ws, f"G{r}", f'=COUNTIFS({T("equipamento.reliquias.conjunto")},{q(letra)},'
                         f'{T("equipamento.reliquias.possui")},"Sim")', nome=f"{base}.pecas", negrito=True)
        cal(ws, f"H{r}", f'=IF({PC}>=4,"4 peças",IF({PC}>=2,"2 peças","—"))', nome=f"{base}.ativo", negrito=True)
        aux(ws, f"P{r}", f'=IF(AND({PC}>=2,{B2}="Um tipo de rolagem +1",LEN({RL})>0),""&{RL},"")',
            nome=f"{base}.vale_rolagem")
        aux(ws, f"Q{r}", f'=IF(AND({PC}>=2,{B2}="Velocidade +1"),1,0)', nome=f"{base}.vel")
        aux(ws, f"R{r}", f'=IF(AND({PC}>=2,{B2}="RD +1"),1,0)', nome=f"{base}.rd")
        aux(ws, f"S{r}", f'=IF(AND({PC}>=2,{B2}="Dano +2"),2,0)', nome=f"{base}.dano")
        av(ws, f"I{r}", f"equipamento.aviso.conjunto.{letra.lower()}", ate="L", formula=
           f'=IF(AND({B2}<>"",COUNTIF({dlista("bonus_conjunto2")},{B2})=0),"Bônus fora da lista de 25.3. ","")'
           f'&IF(AND(LEN({RL})>0,{B2}<>"Um tipo de rolagem +1"),'
           f'"Qual rolagem só vale com o bônus Um tipo de rolagem +1. ","")'
           f'&IF(AND(LEN({RL})>0,COUNTIF({lista_rol},{RL})=0),"Rolagem fora da lista. ","")'
           f'&IF(AND({PC}>=2,{B2}="Um tipo de rolagem +1",LEN({RL})=0),"Escolha qual rolagem recebe o +1.","")')
        r += 1
    reg("equipamento.conjuntos.rolagens", ws, f"P{r0}:P{r - 1}")
    r_soma = r
    r += 2
    # Efeito de 4 peças: texto longo, largura toda
    cabecalhos(ws, r, ["Conjunto", "Nome (automático)", "Efeito de 4 peças (escreva)"], altura=None)
    _mesclar(ws, f"C{r}", "L")
    r += 1
    for letra in "ABC":
        base = f"equipamento.conjunto.{letra.lower()}"
        texto(ws, f"A{r}", letra, negrito=True)
        nm = T(f"{base}.nome")
        cal(ws, f"B{r}", f'=IF(LEN({nm})=0,"Conjunto {letra}",""&{nm})', quebra=True)
        ent(ws, f"C{r}", f"{base}.efeito4", ate="L", rotulo=f"Efeito de 4 peças do Conjunto {letra}")
        r += 1
    r_fim = r
    r = r_soma
    rot(ws, f"A{r}", "Bônus de Conjunto somados")
    rot(ws, f"B{r}", "Velocidade")
    cal(ws, f"C{r}", f"=SUM(Q{r0}:Q{r - 1})", nome="equipamento.conjuntos.vel", negrito=True)
    rot(ws, f"D{r}", "RD")
    cal(ws, f"E{r}", f"=SUM(R{r0}:R{r - 1})", nome="equipamento.conjuntos.rd", negrito=True)
    rot(ws, f"F{r}", "Dano do Ataque Básico (teto +3)")
    aux(ws, f"S{r}", f"=SUM(S{r0}:S{r - 1})", nome="equipamento.conjuntos.dano_bruto")
    cal(ws, f"G{r}", f'=MIN(3,{T("equipamento.conjuntos.dano_bruto")})', nome="equipamento.conjuntos.dano",
        negrito=True)
    rot(ws, f"H{r}", "Rolagens com +1:")
    cal(ws, f"I{r}", f'=IF(SUMPRODUCT((LEN({T("equipamento.conjuntos.rolagens")})>0)*1)=0,"nenhuma",'
                     f'{_juntar([f"P{r0}", f"P{r0 + 1}", f"P{r0 + 2}"])})', ate="K")
    av(ws, f"{AV}{r}", "equipamento.aviso.conjuntos",
       f'=IF({T("equipamento.conjuntos.dano_bruto")}>3,"Os Conjuntos somam +"&'
       f'{T("equipamento.conjuntos.dano_bruto")}&" de dano: o teto é +3 por rolagem (25.3).","")')
    c.r = r_fim


def equip_inventario(c):
    ws = c.ws
    c.passo("Inventário e Espaço — 24.4 (capacidade = 10 + 2 × Bônus de Poder; vestido e empunhado contam)")
    r = c.r
    # Catálogo auxiliar (V:W): poções, itens, armas e armaduras, lidos da aba Dados
    texto(ws, f"V{r}", "Catálogo (24.1 a 24.3)", negrito=True)
    texto(ws, f"W{r}", "Espaço", negrito=True)
    k = r + 1
    for bloco, col_nome, col_esp, prefixo in (("pocoes", "Poção", "Espaço", "Poção de Vida "),
                                             ("itens", "Item", "Espaço", ""),
                                             ("armas", "Categoria", "Espaço", "Arma "),
                                             ("armaduras", "Tipo", "Espaço", "Armadura ")):
        for i in range(1, MAPA.blocos[f"dados.{bloco}"]["linhas"] + 1):
            pre = f'{q(prefixo)}&' if prefixo else ""
            aux(ws, f"V{k}", f"={pre}INDEX({dcol(bloco, col_nome)},{i})")
            aux(ws, f"W{k}", f"=INDEX({dcol(bloco, col_esp)},{i})")
            k += 1
    catalogo, nomes_cat = f"$V${r + 1}:$W${k - 1}", f"$V${r + 1}:$V${k - 1}"
    cap, ocu = T("equipamento.inventario.capacidade"), T("equipamento.inventario.ocupado")
    rot(ws, f"A{r}", "Capacidade (Espaço)")
    cal(ws, f"B{r}", f'=10+2*{bonus_de("Poder")}+IF({tem_bencao("Peso do Juramento")},2,0)',
        nome="equipamento.inventario.capacidade", negrito=True)
    rot(ws, f"C{r}", "10 + 2 × Bônus de Poder (+2 com a Bênção Peso do Juramento)")
    _mesclar(ws, f"C{r}", "K")
    r += 1
    itens = T("equipamento.inventario.itens")
    armas_esp = f'{T("equipamento.arma1.espaco")}+{T("equipamento.arma2.espaco")}'
    rot(ws, f"A{r}", "Ocupado (itens + armas + armadura)")
    cal(ws, f"B{r}", f'={itens}+{armas_esp}+{T("equipamento.armadura.espaco")}',
        nome="equipamento.inventario.ocupado", negrito=True)
    cal(ws, f"C{r}", f'="itens "&{itens}&" · armas "&({armas_esp})&" · armadura "&'
                     f'{T("equipamento.armadura.espaco")}', ate="K")
    r += 1
    rot(ws, f"A{r}", "Estado")
    cal(ws, f"B{r}", f'=IF({ocu}>2*{cap},"Não consegue se mover",IF({ocu}>{cap},"Lentidão","Normal"))',
        nome="equipamento.inventario.estado", negrito=True, ate="D")
    av(ws, f"{AV}{r}", "equipamento.aviso.inventario",
       f'=IF({ocu}>2*{cap},"Acima do dobro da capacidade: você não consegue se mover, nem com Esforço Total (24.4).",'
       f'IF({ocu}>{cap},"Acima da capacidade: Lentidão (24.4). Largar carga é Ação Complementar.",""))')
    r += 1
    r0 = r + 1
    for i in range(1, 21):
        if i in (1, 11):
            # 20 itens em 2 blocos de 10, com o cabeçalho repetido (sem linhas congeladas)
            cabecalhos(ws, r, [f"Item {i} a {i + 9} (escolha do catálogo ou escreva)", None,
                               "Espaço (só fora do catálogo)", "Espaço por unidade", "Quantidade (vazio = 1)",
                               "Espaço total", "Do catálogo?", None, None, None, None, "Aviso"], altura=40)
            _mesclar(ws, f"A{r}", "B")
            _mesclar(ws, f"G{r}", "J")      # K fica para o aviso (K:L, auditoria visual final)
            r += 1
        base = f"equipamento.inventario.{i}"
        ent(ws, f"A{r}", f"{base}.item", "lista", nomes_cat, amostra="Poção de Vida Pequena",
            invalido="Coisa sem catálogo", ate="B", rotulo=f"Item {i}")
        ent(ws, f"C{r}", f"{base}.espaco_manual", "decimal", minimo=0, maximo=50, amostra=0.5,
            rotulo=f"Espaço do item {i}")
        ent(ws, f"E{r}", f"{base}.qtd", "inteiro", minimo=0, maximo=999, amostra=2, rotulo=f"Quantidade do item {i}")
        IT, EM, QT = (T(f"{base}.{x}") for x in ("item", "espaco_manual", "qtd"))
        unid = f"IFERROR(VLOOKUP({IT},{catalogo},2,FALSE),IF(ISNUMBER({EM}),{EM},0))"
        cal(ws, f"D{r}", f'=IF(LEN({IT})=0,"",{unid})', nome=f"{base}.espaco")
        cal(ws, f"F{r}", f"=IF(LEN({IT})=0,0,{unid}*IF(ISNUMBER({QT}),{QT},1))", nome=f"{base}.total", negrito=True)
        cal(ws, f"G{r}", f'=IF(LEN({IT})=0,"",IF(ISERROR(MATCH({IT},{nomes_cat},0)),'
                         f'"Texto livre: use o Espaço que o Mestre aprovar","Sim (capítulo 24)"))', ate="J")
        av(ws, f"{AV}{r}", f"equipamento.aviso.inventario.{i}",
           f'=IF(LEN({IT})=0,IF(OR(LEN({EM})>0,LEN({QT})>0),"Falta o nome do item.",""),'
           f'IF(AND(ISERROR(MATCH({IT},{nomes_cat},0)),LEN({EM})=0),"Fora do catálogo: preencha o Espaço. ","")&'
           f'IF(AND(LEN({EM})>0,NOT(ISNUMBER({EM}))),"Espaço precisa ser um número. ","")&'
           f'IF(AND(LEN({QT})>0,NOT(ISNUMBER({QT}))),"Quantidade precisa ser um número.",""))')
        r += 1
    reg("equipamento.inventario.totais", ws, f"F{r0}:F{r - 1}")
    rot(ws, f"A{r}", "Soma dos itens")
    cal(ws, f"F{r}", f'=SUM({T("equipamento.inventario.totais")})', nome="equipamento.inventario.itens", negrito=True)
    c.r = r + 1


def equip_creditos(c):
    ws = c.ws
    c.passo("Créditos — 24.5 (não ocupam Espaço; os preços não escalam)")
    r = c.r
    ini = T("equipamento.creditos.inicial")
    rot(ws, f"A{r}", "Saldo inicial (Cr)")
    ent(ws, f"B{r}", "equipamento.creditos.inicial", "inteiro", minimo=-10000000, maximo=10000000, amostra=500,
        rotulo="Saldo inicial")
    av(ws, f"{AV}{r}", "equipamento.aviso.creditos.inicial",
       f'=IF(AND(LEN({ini})>0,NOT(ISNUMBER({ini}))),"Precisa ser um número.","")')
    r += 1
    cabecalhos(ws, r, ["Lançamento", "Descrição (preencha)", None, None, None, None,
                       "Valor (+ ganho, - gasto)", None, None, None, None, "Aviso"], altura=30)
    _mesclar(ws, f"B{r}", "F")
    r += 1
    r0 = r
    for i in range(1, 11):
        base = f"equipamento.creditos.lancamento.{i}"
        texto(ws, f"A{r}", i, negrito=True)
        ent(ws, f"B{r}", f"{base}.descricao", ate="F", rotulo=f"Lançamento {i}")
        ent(ws, f"G{r}", f"{base}.valor", "inteiro", minimo=-10000000, maximo=10000000, amostra=-150,
            rotulo=f"Valor do lançamento {i}")
        D, V = T(f"{base}.descricao"), T(f"{base}.valor")
        av(ws, f"{AV}{r}", f"equipamento.aviso.creditos.{i}",
           f'=IF(AND(LEN({V})>0,NOT(ISNUMBER({V}))),"Valor precisa ser um número.",'
           f'IF(AND(LEN({V})=0,LEN({D})>0),"Falta o valor.",""))')
        r += 1
    reg("equipamento.creditos.valores", ws, f"G{r0}:G{r - 1}")
    rot(ws, f"A{r}", "Saldo atual (Cr)")
    cal(ws, f"B{r}", f'=IF(ISNUMBER({ini}),{ini},0)+SUMIF({T("equipamento.creditos.valores")},">-100000000")',
        nome="equipamento.creditos.saldo", negrito=True)
    av(ws, f"{AV}{r}", "equipamento.aviso.creditos.saldo",
       f'=IF({T("equipamento.creditos.saldo")}<0,"Saldo negativo.","")')
    r += 1
    rot(ws, f"A{r}", "Verba de marco do grupo (sua faixa)")
    cal(ws, f"B{r}", f'=INDEX({dcol("verba", "Verba de marco (Cr)")},{FX})', nome="equipamento.creditos.verba",
        negrito=True)
    cal(ws, f"C{r}", f'="Cr por nível ganho, para o grupo (24.5): "&INDEX({dcol("verba", "O que ela compra")},{FX})',
        ate="K")
    c.r = r + 1


def aba_equipamento(ws):
    # A:L = 1355 px (área do jogador em 1360 px; M:AA são auxiliares ocultas)
    larguras(ws, {"A": 20, "B": 18, "C": 16, "D": 13, "E": 14, "F": 20, "G": 11, "H": 10, "I": 9, "J": 13,
                  "K": 12, "L": 30, "M": 2, "N": 2, "O": 2, "P": 16, "Q": 8, "R": 8, "S": 10, "T": 10, "U": 2,
                  "V": 30, "W": 8, "X": 2, "Y": 22, "Z": 2, "AA": 22})
    c = Cursor(ws, 5)
    equip_armas(c)
    equip_cone(c)
    equip_reliquias(c)
    equip_conjuntos(c)
    equip_inventario(c)
    equip_creditos(c)


# ---------------------------------------------------------------------------
# Aba Habilidades — 8 Habilidades (16.3 a 16.6), Ressonância III e a Ultimate (17)
# ---------------------------------------------------------------------------

TIPOS_ULTIMATE = "Dano,Cura,Buff,Debuff,Controle"     # 17.4 passo 2


def _valores_dados(wb, bloco, coluna):
    """Valores de uma coluna de um bloco da aba Dados (já escrita), na ordem das linhas."""
    b = MAPA.blocos[f"dados.{bloco}"]
    letra = b["colunas"][coluna]
    return ["" if wb["Dados"][f"{letra}{k}"].value is None else str(wb["Dados"][f"{letra}{k}"].value)
            for k in range(b["primeira_linha"], b["ultima_linha"] + 1)]


def _altura_texto(textos, ws, coluna, pt=TAM_CORPO):
    """Altura (pt) para o texto mais longo da lista caber com quebra de linha na coluna."""
    import math
    import renderizar_ficha as R
    f = R.fonte(round(pt * 4 / 3))
    asc, desc = f.getmetrics()
    util = int((ws.column_dimensions[coluna].width or 8.43) * 7 + 5) - 2 * R.MARGEM
    n = max(len(R.quebrar(t, f, util)) for t in textos)
    return math.ceil((n * (asc + desc) + 4) * 3 / 4)


def _guias_habilidade(wb):
    """Todos os textos que o guia de 16.5 pode mostrar numa linha de Habilidade."""
    o, d, a = (_valores_dados(wb, "buff", x) for x in ("O que você pode escrever", "Duração", "Alvos"))
    p = _valores_dados(wb, "passivas", "O que você pode escrever")
    return ([f"{x} · {y} · alvos: {z}" for x, y, z in zip(o, d, a)] + [f"{x} · não custa PH" for x in p]
            + ["Dados da tabela 16.3 + Bônus do Atributo de Habilidade, uma vez"])


def _guias_ultimate(wb):
    o, d = _valores_dados(wb, "buff", "O que você pode escrever"), _valores_dados(wb, "buff", "Duração")
    return [f"Nível equivalente {k + 1}: {x} · {y}" for k, (x, y) in enumerate(zip(o, d))] + \
        ["Dados da linha da sua faixa (17.3) + Bônus do Atributo de Habilidade, uma vez"]


def aba_habilidades(ws):
    # A:L = 1355 px (área do jogador em 1360 px; O:W são auxiliares ocultas). F e G cabem a
    # opção mais longa da lista + a seta do Google
    larguras(ws, {"A": 6, "B": 27, "C": 12, "D": 13, "E": 11, "F": 23, "G": 11, "H": 13, "I": 14, "J": 10,
                  "K": 12, "L": 34, "M": 2, "N": 2, "O": 2, "P": 8, "Q": 8, "R": 8, "S": 8, "T": 8, "U": 8,
                  "V": 8, "W": 8})
    nmax, conh = T("nucleo.nivel_max_habilidade"), T("nucleo.habilidades_conhecidas")
    bah, III = T("criacao.bonus_habilidade"), T("progressao.ressonancia.III.efetiva")
    esfera = T("equipamento.esfera.vale")
    hab = lambda col: dcol("habilidades", col)  # noqa: E731
    buff = lambda col: dcol("buff", col)  # noqa: E731
    atk_rol, dt = T("criacao.ataque_habilidade.rolagem"), T("criacao.dt")
    c = Cursor(ws, 5)
    c.titulo("Seus números de Habilidade (automático) — 16.3, 16.6 e 26.2")
    r = c.r
    rot(ws, f"A{r}", "Teste de Ataque (Habilidades e Ultimate)")
    _mesclar(ws, f"A{r}", "B")
    cal(ws, f"C{r}", f"={atk_rol}", nome="habilidades.ataque", negrito=True)
    rot(ws, f"D{r}", "DT das Habilidades")
    _mesclar(ws, f"D{r}", "E")
    cal(ws, f"F{r}", f"={dt}", nome="habilidades.dt", negrito=True)
    rot(ws, f"G{r}", "Nível máximo")
    _mesclar(ws, f"G{r}", "H")
    cal(ws, f"I{r}", f"={nmax}", nome="habilidades.nivel_max", negrito=True)
    r += 1
    rot(ws, f"A{r}", "Habilidades preenchidas / conhecidas")
    _mesclar(ws, f"A{r}", "B")
    pre = T("habilidades.preenchidas")
    cal(ws, f"C{r}", f'=SUM({T("habilidades.preenchida")})', nome="habilidades.preenchidas", negrito=True)
    cal(ws, f"D{r}", f'="de "&{conh}', nome="habilidades.conhecidas")
    cal(ws, f"E{r}", f'=IF({T("nucleo.reescreve")}="Sim","A partir do nível 16: em vez de aprender, reescreva 1 '
                     f'Habilidade conhecida por nível (16.6)","Passivas contam no teto de 8 (16.6)")',
        nome="habilidades.reescreve", ate="K")
    av(ws, f"{AV}{r}", "habilidades.aviso.contagem",
       f'=IF({pre}>{conh},"Habilidades acima das conhecidas no seu nível ("&{conh}&"): confira as linhas abaixo.","")')
    r += 1
    rot(ws, f"A{r}", "Ressonância III (26.7)")
    _mesclar(ws, f"A{r}", "B")
    cal(ws, f"C{r}", f'=IF({III}="","Ainda não ativa: libera no nível 15 (aba Progressão)",'
                     f'"Ativa: marque Sim em uma Habilidade para ela subir 1 Nível de efeito, até o Nível máximo")',
        ate="K")
    av(ws, f"{AV}{r}", "habilidades.aviso.ress3",
       f'=IF(COUNTIF({T("habilidades.ress3")},"Sim")>1,"Ressonância III marcada em mais de uma Habilidade: '
       f'vale só a primeira.","")')
    c.r = r + 1

    # --- Entradas ------------------------------------------------------------------
    c.passo("Suas Habilidades (preencha) — até 8; escreva pelos sete passos de 16.7")
    r = c.r
    # o Efeito (texto longo) ganhou uma tabela própria logo abaixo, com a largura toda
    cabecalhos(ws, r, ["Nº", "Nome (preencha)", "Tipo", "Nível (1 a 7)", "Em área?", "Resolução", "Alcance",
                       "Ressonância III aqui?", "Aviso"], altura=40)
    _mesclar(ws, f"I{r}", "L")
    cabecalhos(ws, r, ["preenchida", "Nível usado", "Ress. III vale", "Nível efetivo", "dados (tabela)",
                       "nº de dados", "face", "fixo"], coluna=16, altura=None)
    r += 1
    r0 = r
    linhas_entrada = {}
    for k in range(1, 9):
        base = f"habilidades.{k}"
        texto(ws, f"A{r}", k, negrito=True)
        ent(ws, f"B{r}", f"{base}.nome", amostra="Rebarba", rotulo=f"Habilidade {k}")
        ent(ws, f"C{r}", f"{base}.tipo", "lista", "tipos_habilidade", invalido="Ataque", rotulo="Tipo")
        ent(ws, f"D{r}", f"{base}.nivel", "inteiro", minimo=1, maximo=7, rotulo="Nível da Habilidade")
        ent(ws, f"E{r}", f"{base}.area", "lista", "sim_nao", rotulo="Em área")
        ent(ws, f"F{r}", f"{base}.resolucao", "lista", "resolucao", rotulo="Resolução")
        ent(ws, f"G{r}", f"{base}.alcance", "lista", "alcances", amostra="Extrema", invalido="Longe", rotulo="Alcance")
        ent(ws, f"H{r}", f"{base}.ress3", "lista", "sim_nao", rotulo="Ressonância III")
        NOME, TIPO, NIV, AREA, RES, ALC, R3, EFE = (T(f"{base}.{x}") for x in (
            "nome", "tipo", "nivel", "area", "resolucao", "alcance", "ress3", "efeito"))
        PR, NU, R3V, NE, NB, N_, F_, FX_ = (T(f"{base}.{x}") for x in (
            "preenchida", "nivel_usado", "ress3_vale", "nivel_efetivo", "n_tabela", "n", "face", "fixo"))
        campos = (NOME, TIPO, NIV, AREA, RES, ALC, R3, EFE)
        aux(ws, f"P{r}", "=IF(OR(" + ",".join(f"LEN({x})>0" for x in campos) + "),1,0)", nome=f"{base}.preenchida")
        aux(ws, f"Q{r}", f"=IF(ISNUMBER({NIV}),MAX(1,MIN(7,INT({NIV}))),1)", nome=f"{base}.nivel_usado")
        aux(ws, f"R{r}", f'=IF(AND({R3}="Sim",{III}<>"",COUNTIF($H${r0}:H{r},"Sim")=1),1,0)', nome=f"{base}.ress3_vale")
        aux(ws, f"S{r}", f"=IF(AND({R3V}=1,{NU}<{nmax}),MIN({nmax},{NU}+1),{NU})", nome=f"{base}.nivel_efetivo")
        aux(ws, f"T{r}", f'=IF({TIPO}="Dano",INDEX({hab("Dados de dano")},{NE}),IF({TIPO}="Cura",'
                         f'INDEX({hab("Dados de cura")},{NE}),0))', nome=f"{base}.n_tabela")
        aux(ws, f"U{r}", f'=IF(AND({AREA}="Sim",{NB}>0),MAX(1,INT({NB}/2)),{NB})', nome=f"{base}.n")
        aux(ws, f"V{r}", f'=IF({TIPO}="Dano",INDEX({hab("Face do dano")},{NE}),IF({TIPO}="Cura",'
                         f'INDEX({hab("Face da cura")},{NE}),0))', nome=f"{base}.face")
        aux(ws, f"W{r}", f'=IF(OR({TIPO}="Dano",{TIPO}="Cura"),{bah}+IF({TIPO}="Dano",{esfera}+'
                         f'{T("equipamento.cone.em.dano_habilidade")},0),0)', nome=f"{base}.fixo")
        alc_l = dlista("alcances")
        AMAX = T(f"{base}.alcance_max")
        av(ws, f"I{r}", f"habilidades.aviso.{k}", ate="L", formula=
           f'=IF({PR}=0,"",IF({TIPO}="","Escolha o Tipo. ",IF(COUNTIF({dlista("tipos_habilidade")},{TIPO})=0,'
           f'"Tipo fora da lista (16.5). ",""))'
           f'&IF(LEN({NIV})=0,"",IF(ISNUMBER({NIV}),IF(OR({NIV}<1,{NIV}>7),"O Nível vai de 1 a 7. ","")&'
           f'IF({NIV}>{nmax},"Acima do Nível máximo do seu nível ("&{nmax}&"). ",""),'
           f'"Nível precisa ser um número de 1 a 7. "))'
           f'&IF(LEN({ALC})=0,"",IF(ISERROR(MATCH({ALC},{alc_l},0)),"Alcance fora da lista. ",'
           f'IF(MATCH({ALC},{alc_l},0)>MATCH({AMAX},{alc_l},0),"Alcance acima do que o Nível "&{NE}&'
           f'" permite (até "&{AMAX}&"). ","")))'
           f'&IF(SUM($P${r0}:P{r})>{conh},"Acima das "&{conh}&" Habilidades conhecidas do seu nível. ","")'
           f'&IF({R3}="Sim",IF({III}="","Ressonância III ainda não está ativa. ",'
           f'IF(COUNTIF($H${r0}:H{r},"Sim")>1,"Ressonância III só vale numa Habilidade. ","")),""))')
        linhas_entrada[k] = r
        r += 1
    reg("habilidades.preenchida", ws, f"P{r0}:P{r - 1}")
    reg("habilidades.ress3", ws, f"H{r0}:H{r - 1}")
    c.r = r

    # --- Efeito de cada Habilidade (texto longo, largura toda) ------------------------
    c.passo("Efeito de cada Habilidade (preencha) — o que ela faz, em uma ou duas frases")
    r = c.r
    cabecalhos(ws, r, ["Nº", "Nome (automático)", "Efeito (preencha)"], altura=None)
    _mesclar(ws, f"C{r}", "L")
    r += 1
    for k in range(1, 9):
        texto(ws, f"A{r}", k, negrito=True)
        nm = T(f"habilidades.{k}.nome")
        cal(ws, f"B{r}", f'=IF(LEN({nm})=0,"Habilidade {k}",""&{nm})', quebra=True)
        ent(ws, f"C{r}", f"habilidades.{k}.efeito", ate="L", rotulo="Efeito")
        r += 1
    c.r = r

    # --- Saídas -----------------------------------------------------------------------
    c.passo("Números das Habilidades (automático) — 16.3, 16.4 e 16.5")
    r = c.r
    cabecalhos(ws, r, ["Nº", "Nome", "Nível efetivo", "Dano ou cura", "Média", "Rolagem ou DT", "PH",
                       "Redução de Tenacidade", "Alcance máximo", "Alvos", "Dados da tabela",
                       "Média dos dados"], altura=40)
    r += 1
    r_guia = r + 8 + 2          # tabela do guia de 16.5 e do bônus fixo, logo abaixo
    for k in range(1, 9):
        base = f"habilidades.{k}"
        NOME, TIPO, AREA, RES = (T(f"{base}.{x}") for x in ("nome", "tipo", "area", "resolucao"))
        PR, NE, N_, F_, FX_ = (T(f"{base}.{x}") for x in ("preenchida", "nivel_efetivo", "n", "face", "fixo"))
        semd = f"OR({PR}=0,{N_}=0)"
        texto(ws, f"A{r}", k, negrito=True)
        cal(ws, f"B{r}", f'=IF({PR}=0,"",IF(LEN({NOME})=0,"Habilidade {k}",""&{NOME}))', nome=f"{base}.nome_exibido",
            quebra=True)
        cal(ws, f"C{r}", f'=IF({PR}=0,"",{NE})', nome=f"{base}.nivel_exibido", negrito=True)
        cal(ws, f"D{r}", f'=IF({semd},"",{texto_dano(N_, F_, FX_)})', nome=f"{base}.total", negrito=True)
        cal(ws, f"E{r}", f'=IF({semd},"",INT({N_}*({F_}+1)/2)+{FX_})', nome=f"{base}.media", negrito=True)
        cal(ws, f"F{r}", f'=IF({PR}=0,"",IF({RES}="Teste de Ataque",{atk_rol},IF({RES}="Teste de Resistência",'
                         f'"DT "&{dt},"")))', nome=f"{base}.rolagem", negrito=True)
        cal(ws, f"G{r}", f'=IF({PR}=0,"",IF({TIPO}="Passiva",0,INDEX({hab("Custo (PH)")},{NE})))', nome=f"{base}.ph")
        cal(ws, f"H{r}", f'=IF({PR}=0,"",IF({TIPO}="Dano",INDEX({hab("Redução de Tenacidade")},{NE}),0))',
            nome=f"{base}.rt")
        cal(ws, f"I{r}", f'=IF({PR}=0,"",CHOOSE(MIN(4,{NE}),"Curta","Média","Longa","Extrema"))',
            nome=f"{base}.alcance_max")
        cal(ws, f"J{r}", f'=IF({PR}=0,"",IF({AREA}="Sim",IF({NE}>=6,4,3),1))', nome=f"{base}.alvos")
        cal(ws, f"K{r}", f'=IF({semd},"",{N_}&"d"&{F_})', nome=f"{base}.dados")
        cal(ws, f"L{r}", f'=IF({semd},"",INT({N_}*({F_}+1)/2))', nome=f"{base}.media_dados")
        rg = r_guia + k - 1
        texto(ws, f"A{rg}", k, negrito=True)
        cal(ws, f"B{rg}", f'=IF({PR}=0,"",IF(LEN({NOME})=0,"Habilidade {k}",""&{NOME}))', quebra=True)
        cal(ws, f"C{rg}", f'=IF({PR}=0,"",{FX_})', nome=f"{base}.fixo_exibido")
        cal(ws, f"D{rg}", f'=IF({PR}=0,"",IF(OR({TIPO}="Buff",{TIPO}="Debuff"),INDEX({buff("O que você pode escrever")},'
                         f'{NE})&" · "&INDEX({buff("Duração")},{NE})&" · alvos: "&INDEX({buff("Alvos")},{NE}),'
                         f'IF({TIPO}="Passiva",INDEX({dcol("passivas", "O que você pode escrever")},{NE})&'
                         f'" · não custa PH",IF(OR({TIPO}="Dano",{TIPO}="Cura"),"Dados da tabela 16.3 + Bônus do '
                         f'Atributo de Habilidade, uma vez","Escolha o Tipo"))))', nome=f"{base}.guia", quebra=True,
            ate="L")
        r += 1
    # guia de 16.5 e bônus fixo: tabela própria (o texto do guia ganha a largura D:L)
    r += 1
    cabecalhos(ws, r, ["Nº", "Nome", "Bônus fixo", "Guia de 16.5 (o que o efeito pode fazer)"], altura=None)
    _mesclar(ws, f"D{r}", "L")
    c.r = r + 9

    # --- Ultimate -------------------------------------------------------------------
    c.passo("Ultimate — 17 (100 de Energia, não gasta ação, 1 por Ciclo; potência pela faixa)")
    r = c.r
    U = lambda x: T(f"habilidades.ultimate.{x}")  # noqa: E731
    ult = lambda col: dcol("ultimate", col)  # noqa: E731
    for nome, rotulo, tipo, fonte, ate, amostra, invalido in (
            ("nome", "Nome (diga em voz alta)", "texto", None, "F", "A Doca Inteira", None),
            ("frase", "A frase que você diz", "texto", None, "K", None, None),
            # C:D mesclada: "Teste de Resistência" cabe dentro da caixa amarela (auditoria visual)
            ("tipo", "Tipo", "lista", q(TIPOS_ULTIMATE), "D", "Dano", "Ataque"),
            ("area", "Em área?", "lista", "sim_nao", "D", None, None),
            ("resolucao", "Resolução", "lista", "resolucao", "D", None, None),
            ("efeito", "Efeito (o que ela faz)", "texto", None, "K", None, None)):
        rot(ws, f"A{r}", rotulo)
        _mesclar(ws, f"A{r}", "B")
        ent(ws, f"C{r}", f"habilidades.ultimate.{nome}", tipo, fonte, amostra=amostra, invalido=invalido, ate=ate,
            rotulo=f"Ultimate: {rotulo}")
        if nome == "tipo":
            tip, res_ = U("tipo"), U("resolucao")
            ok_tipo = "OR(" + ",".join(f"{tip}={q(x)}" for x in TIPOS_ULTIMATE.split(",")) + ")"
            av(ws, f"{AV}{r}", "habilidades.aviso.ultimate",
               f'=IF({tip}="",IF({U("preenchida")}=1,"Escolha o Tipo da Ultimate.",""),'
               f'IF({ok_tipo},"","Tipo fora da lista (17.4)."))&IF(AND(LEN({res_})>0,'
               f'COUNTIF({dlista("resolucao")},{res_})=0)," Resolução fora da lista.","")')
        r += 1
    TIPO, AREA, RES = U("tipo"), U("area"), U("resolucao")
    EQ, N_, F_, FX_ = U("equivalente"), U("n"), U("face"), U("fixo")
    campos = [U(x) for x in ("nome", "frase", "tipo", "area", "resolucao", "efeito")]
    cabecalhos(ws, r, ["Ultimate", "", "Nível equivalente", "Dano ou cura", "Média", "Rolagem ou DT",
                       "Custo (Energia)", "Redução de Tenacidade", "Alvos", "Dados da tabela", "Média dos dados",
                       "Bônus fixo"], altura=40)
    _mesclar(ws, f"A{r}", "B")
    cabecalhos(ws, r, ["preenchida", "nº tabela", "nº de dados", "face"], coluna=16, altura=None)
    r += 1
    aux(ws, f"P{r}", "=IF(OR(" + ",".join(f"LEN({x})>0" for x in campos) + "),1,0)",
        nome="habilidades.ultimate.preenchida")
    aux(ws, f"Q{r}", f'=IF({TIPO}="Dano",INDEX({ult("Dados de dano")},{FX}),IF({TIPO}="Cura",'
                     f'INDEX({ult("Dados de cura")},{FX}),0))', nome="habilidades.ultimate.n_tabela")
    aux(ws, f"R{r}", f'=IF(AND({AREA}="Sim",{U("n_tabela")}>0),MAX(1,INT({U("n_tabela")}/2)),{U("n_tabela")})',
        nome="habilidades.ultimate.n")
    aux(ws, f"S{r}", f'=IF({TIPO}="Dano",INDEX({ult("Face do dano")},{FX}),IF({TIPO}="Cura",'
                     f'INDEX({ult("Face da cura")},{FX}),0))', nome="habilidades.ultimate.face")
    semd = f"{N_}=0"
    rot(ws, f"A{r}", "Números da Ultimate")
    _mesclar(ws, f"A{r}", "B")
    cal(ws, f"C{r}", f"={T('nucleo.ultimate_equivalente')}", nome="habilidades.ultimate.equivalente", negrito=True)
    cal(ws, f"L{r}", f'=IF(OR({TIPO}="Dano",{TIPO}="Cura"),{bah}+IF({TIPO}="Dano",{esfera}+'
                     f'{T("equipamento.cone.em.dano_ultimate")},0),0)', nome="habilidades.ultimate.fixo")
    cal(ws, f"D{r}", f'=IF({semd},"",{texto_dano(N_, F_, FX_)})', nome="habilidades.ultimate.total", negrito=True)
    cal(ws, f"E{r}", f'=IF({semd},"",INT({N_}*({F_}+1)/2)+{FX_})', nome="habilidades.ultimate.media", negrito=True)
    cal(ws, f"F{r}", f'=IF({RES}="Teste de Ataque",{atk_rol},IF({RES}="Teste de Resistência","DT "&{dt},""))',
        nome="habilidades.ultimate.rolagem", negrito=True)
    cal(ws, f"G{r}", f'=IF({T("progressao.ressonancia.IV.efetiva")}="Ultimate com 80 de Energia",80,100)',
        nome="habilidades.ultimate.custo", negrito=True)
    cal(ws, f"H{r}", f"=INDEX({ult('Redução de Tenacidade')},{FX})", nome="habilidades.ultimate.rt")
    cal(ws, f"I{r}", f'=IF({AREA}="Sim",IF({EQ}>=6,4,3),1)', nome="habilidades.ultimate.alvos")
    cal(ws, f"J{r}", f'=IF({semd},"",{N_}&"d"&{F_})', nome="habilidades.ultimate.dados")
    cal(ws, f"K{r}", f'=IF({semd},"",INT({N_}*({F_}+1)/2))', nome="habilidades.ultimate.media_dados")
    r += 1
    rot(ws, f"A{r}", "Guia de 16.5 (efeito)")
    _mesclar(ws, f"A{r}", "B")
    cal(ws, f"C{r}", f'=IF(OR({TIPO}="Buff",{TIPO}="Debuff",{TIPO}="Controle"),"Nível equivalente "&{EQ}&": "&'
                     f'INDEX({buff("O que você pode escrever")},{EQ})&" · "&INDEX({buff("Duração")},{EQ}),'
                     f'IF(OR({TIPO}="Dano",{TIPO}="Cura"),"Dados da linha da sua faixa (17.3) + Bônus do Atributo '
                     f'de Habilidade, uma vez","Escolha o Tipo"))', nome="habilidades.ultimate.guia", quebra=True,
        ate="L")
    r += 1
    rot(ws, f"A{r}", "A Ultimate sobe sozinha ao mudar de faixa (níveis 5, 9, 13 e 17). Ressonância II: efeito extra; "
                     "Ressonância IV: pode custar 80 de Energia (26.7).")
    _mesclar(ws, f"A{r}", "L")
    c.r = r + 1


# ---------------------------------------------------------------------------
# Aba Em Jogo — uma tela (A:L × 1-40): Resumo para o Jogador, recursos, calculadora de
# dano, ações, Testes de Resistência, Perícias, condições e usos
# ---------------------------------------------------------------------------

# Soma A:L = 1360 px (o limite da tela), em px: A 150 · B 140 · C 95 · D 105 · E 90 · F 90 | G 156 ·
# H 134 · I 105 · J 105 · K 126 · L 64. A:B e G:H (290 px) levam o nome de 40 caracteres das
# Habilidades e das armas; G:I (395 px) o "Bênção · frequência" dos Usos (v1.1, ajustes pedidos
# pelo usuário: tudo cabe na própria célula, sem transbordar)
def _px_largura(px):
    """Largura de coluna (caracteres) que dá exatamente `px` pela conversão int(largura × 7 + 5)."""
    return round((px - 5 + 0.5) / 7, 3)


EJ_PX = {"A": 150, "B": 140, "C": 95, "D": 105, "E": 90, "F": 90, "G": 156, "H": 134, "I": 105, "J": 105,
         "K": 126, "L": 64}
EJ_LARGURAS = {k: _px_largura(v) for k, v in EJ_PX.items()}
EJ_FONTE_CORPO = 9   # pt do corpo da tela (títulos de bloco continuam com 12)
# Resumo para o Jogador: versão curta de onde valem as Vantagens raciais (o texto inteiro, com
# a regra, está na aba Testes e nos traços da Criação; aqui precisa caber em B:D numa linha)
EJ_VANTAGENS_CURTAS = {
    "Humano": "Esforço (1 ponto) e +1 Perícia na criação",
    "Xianzhouíta": "todo Teste de Resistência; 1 pergunta por cena",
    "Vidyadhara": "recupera PV 1× por descanso; respira na água",
    "Vulpes": "Presença e Força de Vontade; 1 favor por descanso",
    "Haloviano": "Controlado 2× por dia; sem dano de queda",
    "Avginiano": "Testes mentais; metade da duração ao falhar",
    "Intellitron": "Tecnologia, Mecânica, Fraqueza; imune a doença",
}
# Efeito curto das condições do personagem (resumo de 21.5 para caber em C:D da Em Jogo)
EJ_EFEITO_CURTO = [
    ("Sangramento", "5% dos PV máx. por turno"), ("Queimadura", "Contínuo 2d6 + Eficiência"),
    ("Choque", "Contínuo 1d6 + Eficiência"), ("Cisalhamento de Vento", "Contínuo 1d6 por acúmulo"),
    ("Embaraço", "1d6/acúmulo · Atrasa 1 casa"), ("Aprisionamento", "1d6 + Ef. · Atrasa 2 casas"),
    # Congelado saiu da lista do personagem na v1.1: "só existe em inimigo" (21.2 e 21.5, D6)
    ("Lentidão", "só move com Esforço Total"),
    ("Marcado", "+1 Ataque de quem marcou"), ("Silenciado", "sem Habilidade de Nível 4+"),
    ("Vulnerável", "+1 dado de dano da fonte"), ("Controlado", "quem aplicou decide ações"),
    ("Corrupção", "+1 em toda DC do aplicador"), ("Surpreso", "casa pulada no 1º Ciclo"),
]
# Frequência curta dos Usos (a frequência inteira está na aba Caminho)
EJ_FREQ_CURTA = [("Uma vez por turno", "1/turno"), ("Uma vez por Ciclo", "1/Ciclo"),
                 ("Uma vez por combate por alvo", "1/combate/alvo"), ("Uma vez por combate", "1/combate"),
                 ("Uma vez por Descanso Longo", "1/Desc. Longo"), ("Uma vez por sessão", "1/sessão"),
                 ("Duas vezes por dia", "2/dia")]
EJ_AV = "N"          # avisos fora da tela (o resumo deles aparece na linha 13)
AVISOS_EM_JOGO = []  # células de aviso da coluna N (o resumo da linha 13 conta todas)


def _resumo_avisos_em_jogo(avisos_ej):
    """Linha 13 da Em Jogo: quantos avisos e o primeiro deles (a lista inteira fica na coluna N,
    fora da tela): cabe numa linha de A:L mesmo no pior caso (v1.1)."""
    n_av = "+".join(f"IF(LEN({c_})>0,1,0)" for c_ in avisos_ej)
    prim_av = '""'
    for c_ in reversed(avisos_ej):
        prim_av = f"IF(LEN({c_})>0,{c_},{prim_av})"
    return (f'=IF(({n_av})=0,"","Avisos ("&({n_av})&"): "&{prim_av}&IF(({n_av})>1,'
            f'" · os outros estão na coluna N",""))')
EJ_USOS = 8          # linhas de Usos por combate e descanso (G33:J40)


def _juntar(exprs, sep=" · "):
    """Concatena expressões de texto (cada uma "" ou texto) com separador só entre as
    não vazias, sem LEFT/MID (fora da lista branca)."""
    partes = [exprs[0]]
    for i, x in enumerate(exprs[1:], start=1):
        antes = "&".join(exprs[:i])
        partes.append(f'IF(LEN({x})>0,IF(LEN({antes})>0,{q(sep)},"")&{x},"")')
    return "&".join(partes)


def _ej_bloqueio(k_nivel=None, ultimate=False):
    """Texto de bloqueio por condição (decisão 1): Controlado bloqueia tudo; Silenciado,
    Habilidade de Nível 4 ou maior."""
    ctl, sil = T("em_jogo.controlado"), T("em_jogo.silenciado")
    # na coluna de rolagem cabe só a palavra; o motivo aparece nas condições ativas (e na
    # situação da Ultimate)
    if ultimate:
        return f'IF({ctl}=1,"BLOQUEADA","")'
    return f'IF({ctl}=1,"BLOQUEADA",IF(AND({sil}=1,{k_nivel}>=4),"BLOQUEADA",""))'


def aba_em_jogo(ws):
    # N: avisos fora da tela, numa linha só (o resumo deles aparece na linha 13)
    larguras(ws, {**EJ_LARGURAS, "M": 2, "N": 150, "O": 2, "P": 48, "Q": 10, "R": 2, "S": 34, "T": 30, "U": 6,
                  "V": 6, "W": 16, "X": 6, "Y": 6, "Z": 12, "AA": 30, "AB": 13})
    for lin in range(1, 41):
        ws.row_dimensions[lin].height = 14.25
    PVMAX, TETO_T, EFV = T("criacao.pv"), T("nucleo.teto_temporarios"), EF
    PV, TMP, EN, PH, ESF, MEMO = (T(f"em_jogo.{x}") for x in
                                  ("pv_atual", "temporarios", "energia", "ph", "esforco", "memo_ativo"))
    PVU, TMPU, ENU = T("em_jogo.pv_usado"), T("em_jogo.temporarios_usado"), T("em_jogo.energia_usada")
    MORR = T("em_jogo.morrendo")
    memo_on = f'({T("em_jogo.memo_ativo.usado")}="Sim")'
    teto_b = T("nucleo.teto_bonus")
    avisos_ej = []

    def avj(linha, nome, formula):
        av(ws, f"{EJ_AV}{linha}", nome, formula)
        avisos_ej.append(f"{EJ_AV}{linha}")

    def num(linha, nome, rotulo, formula):
        texto(ws, f"P{linha}", rotulo)
        aux(ws, f"Q{linha}", formula, nome=nome)

    # --- Valores auxiliares (P:Q, fora da tela) ---------------------------------------
    texto(ws, "P1", "Valores auxiliares (automático)", negrito=True)
    texto(ws, f"{EJ_AV}1", "Avisos desta aba (automático; o resumo aparece na linha 13)", negrito=True)
    num(2, "em_jogo.pv_usado", "PV atual usado (vazio = cheio)", f"=IF(ISNUMBER({PV}),MAX(0,INT({PV})),{PVMAX})")
    num(3, "em_jogo.morrendo", "Morrendo (PV 0)", f'=IF({PVU}=0,"Sim","Não")')
    num(4, "em_jogo.temporarios_usado", "PV temporários usados (teto)",
        f"=IF(ISNUMBER({TMP}),MAX(0,MIN({TETO_T},INT({TMP}))),0)")
    num(5, "em_jogo.energia_usada", "Energia usada (0 a 100)", f"=IF(ISNUMBER({EN}),MAX(0,MIN(100,INT({EN}))),0)")
    num(6, "em_jogo.memo_ativo.usado", "Memoespírito ativo (só A Recordação)",
        f'=IF(AND({MEMO}="Sim",{CAM}="A Recordação"),"Sim","Não")')
    ACA, ACB = T("em_jogo.acumulo.a"), T("em_jogo.acumulo.b")
    NA, NB_ = T("em_jogo.acumulo.a.nome"), T("em_jogo.acumulo.b.nome")
    acA = f"IF(ISNUMBER({ACA}),MAX(0,INT({ACA})),0)"
    acB = f"IF(ISNUMBER({ACB}),MAX(0,INT({ACB})),0)"
    teto_calc = f'IF({tem_bencao("Teto Rompido")},7,5)'
    num(7, "em_jogo.furia", "Fúria (Sacrifício Desesperado, máx. 2)", f'=IF({NA}="Fúria",MIN(2,{acA}),0)')
    num(8, "em_jogo.florescimento", "Florescimento (máx. 5)", f'=IF({NA}="Florescimento",MIN(5,{acA}),0)')
    num(9, "em_jogo.fragmentos", "Fragmentos de Memória (máx. 5)",
        f'=IF({NA}="Fragmentos de Memória",MIN(5,{acA}),0)')
    num(10, "em_jogo.calculo", "Acúmulos de Cálculo (máx. 5 ou 7)",
        f'=IF({NA}="Acúmulos de Cálculo",MIN({teto_calc},{acA}),0)')
    num(11, "em_jogo.marcas", "Marcas da Ruína (máx. 5)", f'=IF({NB_}="Marcas da Ruína",MIN(5,{acB}),0)')
    num(12, "em_jogo.instinto", "Instinto de Sobrevivência ligado (PV ≤ 1/3)",
        f'=IF(AND({tem_bencao("Instinto de Sobrevivência")},ISNUMBER({PV}),{PVU}*3<={PVMAX}),1,0)')
    num(13, "em_jogo.temp_ataque.bruto", "Bônus temporário no Teste de Ataque (antes do teto)",
        f'=2*{T("em_jogo.instinto")}+IF(AND({memo_on},{T("memo.funcao")}="Catalisador"),1,0)'
        f'+IF(AND({memo_on},COUNTIF({T("memo.evolucoes")},"Fusão de Memórias")>0),1,0)'
        f'+IF(AND({memo_on},{tem_bencao("Memória Compartilhada")}),1,0)'
        f'+COUNTIF({T("equipamento.conjuntos.rolagens")},"Teste de Ataque")')
    num(14, "em_jogo.temp_ataque", "Bônus temporário no Teste de Ataque (no teto)",
        f'=MIN({teto_b},{T("em_jogo.temp_ataque.bruto")})')
    num(15, "em_jogo.temp_defesa.bruto", "Defesa temporária (Florescimento, Memória da Guarda)",
        f'={T("em_jogo.florescimento")}+IF(AND({tem_bencao("Fragmentos do Eu Perdido")},{memo_on},'
        f'{T("caminho.escolha.fragmentos")}="Guarda"),{EFV},0)')
    num(16, "em_jogo.defesa_com_temporarios", "Defesa com temporários",
        f'={T("criacao.defesa")}+MIN({teto_b},{T("em_jogo.temp_defesa.bruto")})')
    num(17, "em_jogo.barreira_max", "Teto de Barreira (Preservação)", f'=IF({CAM}="A Preservação",3*{EFV},"")')
    COND = T("em_jogo.condicoes")
    num(18, "em_jogo.silenciado", "Silenciado", f'=IF(COUNTIF({COND},"Silenciado")>0,1,0)')
    num(19, "em_jogo.controlado", "Controlado", f'=IF(COUNTIF({COND},"Controlado")>0,1,0)')
    num(20, "em_jogo.lentidao", "Lentidão (condição ou carga)",
        f'=IF(OR(COUNTIF({COND},"Lentidão")>0,{T("equipamento.inventario.estado")}="Lentidão"),1,0)')
    num(21, "em_jogo.surpreso", "Surpreso", f'=IF(COUNTIF({COND},"Surpreso")>0,1,0)')
    num(22, "em_jogo.ultimate_pronta", "Ultimate pronta",
        f'=IF({ENU}>={T("habilidades.ultimate.custo")},"Sim","Não")')

    # --- Resumo para o Jogador (A1:D12) ----------------------------------------------
    titulo(ws, "A1", "Resumo para o Jogador", ate="D")
    nome_ = T("criacao.nome")
    ab = lambda x: T(f"equipamento.ab.principal.{x}")  # noqa: E731
    van_txt = {}
    for v in ficha_dados.TRANSCRITO["vantagens_raciais"]:
        van_txt.setdefault(v["raca"], []).append(v["onde"])
    f_van = '"—"'
    for raca in van_txt:
        f_van = f'IF({RACA}={q(raca)},{q(EJ_VANTAGENS_CURTAS[raca])},{f_van})'
    conds_txt = T("em_jogo.condicoes_texto")
    resumo = [
        ("Nome", f'=IF(LEN({nome_})=0,"(sem nome)",""&{nome_})', "em_jogo.resumo.nome"),
        ("Raça · Caminho", f'=IF({RACA}="","Raça?",{RACA})&" · "&IF({CAM}="","Caminho?",{CAM})&" · nível "&{LV}',
         "em_jogo.resumo.identidade"),
        ("Elemento", f'=IF({T("criacao.elemento")}="","—",{T("criacao.elemento")})&" (Ataque Básico: "&'
                     f'{T("criacao.arma.elemento")}&")"', "em_jogo.resumo.elemento"),
        ("PV", f'={PVU}&" / "&{PVMAX}&IF({TMPU}>0," (+"&{TMPU}&" temporários)","")&IF({MORR}="Sim"," · Morrendo","")',
         "em_jogo.resumo.pv"),
        ("Defesa · Esquiva", f'={T("criacao.defesa")}&IF({T("em_jogo.defesa_com_temporarios")}>{T("criacao.defesa")},'
                             f'" ("&{T("em_jogo.defesa_com_temporarios")}&" com temporários)","")&" · Esquiva "&'
                             f'IF(ISNUMBER({T("criacao.esquiva")}),{T("criacao.esquiva")},"proibida")',
         "em_jogo.resumo.defesa"),
        ("RD · Velocidade", f'="RD "&{T("criacao.rd")}&" · VEL "&{T("criacao.velocidade")}', "em_jogo.resumo.rd_vel"),
        ("DT das Habilidades", f'={T("criacao.dt")}&" · ataque de Habilidade "&{T("criacao.ataque_habilidade.rolagem")}',
         "em_jogo.resumo.dt"),
        ("Melhor ataque", f'=IF({T("criacao.arma.categoria")}="","Habilidades "&{T("criacao.ataque_habilidade.rolagem")},'
                          f'"Ataque Básico "&{ab("rolagem")}&" · "&{ab("texto")}&" (média "&{ab("media")}&")")',
         "em_jogo.resumo.ataque"),
        ("Vantagens raciais", "=" + f_van, "em_jogo.resumo.vantagens"),
        # a 1ª condição e quantas mais (a lista inteira está nas linhas 37 a 40 e cabe em B:D)
        ("Condições ativas", f'=IF({T("em_jogo.condicoes_n")}=0,"Nenhuma",{T("em_jogo.condicoes_primeira")}&'
                             f'IF({T("em_jogo.condicoes_n")}>1," + "&({T("em_jogo.condicoes_n")}-1)&" (linhas 37-40)",""))',
         "em_jogo.resumo.condicoes"),
        ("Pode ser Executado?", f'=IF({RACA}="Xianzhouíta","Não (Xianzhouíta, 23.5)",IF({MORR}="Sim",'
                                f'"Sim: está Morrendo (23.5)","Só se estiver Morrendo (23.5)"))',
         "em_jogo.resumo.executado"),
    ]
    for i, (rotulo, formula, nome) in enumerate(resumo, start=2):
        rot(ws, f"A{i}", rotulo, negrito=True)
        cal(ws, f"B{i}", formula, nome=nome, ate="D")

    # --- Recursos (E1:H12) ----------------------------------------------------------------
    titulo(ws, "E1", "Recursos (preencha os amarelos)", ate="H")
    CUSTO = T("habilidades.ultimate.custo")
    rot(ws, "E2", "PV atual")
    ent(ws, "F2", "em_jogo.pv_atual", "inteiro", minimo=0, maximo=9999, amostra=1, rotulo="PV atual")
    cal(ws, "G2", f'="de "&{PVMAX}&IF({MORR}="Sim"," · Morrendo"," · vazio = cheio")', ate="H")
    avj(2, "em_jogo.aviso.pv", f'=IF(LEN({PV})=0,"",IF(ISNUMBER({PV}),IF({PV}>{PVMAX},"PV atual acima do máximo ("&'
                               f'{PVMAX}&"). ","")&IF({PV}<0,"PV não fica abaixo de 0 (23.4). ",""),'
                               f'"PV atual precisa ser um número."))')
    rot(ws, "E3", "Temporários")
    ent(ws, "F3", "em_jogo.temporarios", "inteiro", minimo=0, maximo=99, amostra=5, rotulo="PV temporários")
    cal(ws, "G3", f'="ou Barreira · teto "&{TETO_T}&" · não acumulam"', ate="H")
    avj(3, "em_jogo.aviso.temporarios",
        f'=IF(LEN({TMP})=0,"",IF(ISNUMBER({TMP}),IF({TMP}>{TETO_T},"PV temporários acima do teto ("&{TETO_T}&'
        f'", 23.3): conta o teto.",""),"PV temporários precisa ser um número."))')
    rot(ws, "E4", "Energia")
    ent(ws, "F4", "em_jogo.energia", "inteiro", minimo=0, maximo=100, amostra=100, invalido=130, rotulo="Energia")
    cal(ws, "G4", f'="0 a 100 · Ultimate pronta: "&IF({T("em_jogo.ultimate_pronta")}="Sim","Sim","Não ("&{CUSTO}&")")',
        ate="H")
    avj(4, "em_jogo.aviso.energia",
        f'=IF(LEN({EN})=0,"",IF(ISNUMBER({EN}),IF({EN}>100,"Energia acima de 100 é perdida (17.1).","")&'
        f'IF({EN}<0,"Energia não fica abaixo de 0.",""),"Energia precisa ser um número."))')
    rot(ws, "E5", "PH do grupo")
    ent(ws, "F5", "em_jogo.ph", "inteiro", minimo=0, maximo=20, amostra=3, invalido=50, rotulo="PH do grupo")
    cal(ws, "G5", f'="máx "&{T("nucleo.ph_max")}&" · início "&{T("nucleo.ph_inicio")}&" · +"&{T("nucleo.ph_geracao")}&'
                  f'" por acerto"', ate="H")
    avj(5, "em_jogo.aviso.ph", f'=IF(LEN({PH})=0,"",IF(ISNUMBER({PH}),IF({PH}>{T("nucleo.ph_max")},'
                               f'"PH acima do máximo do grupo ("&{T("nucleo.ph_max")}&", 16.2).",""),'
                               f'"PH precisa ser um número."))')
    rot(ws, "E6", "Esforço")
    ent(ws, "F6", "em_jogo.esforco", "inteiro", minimo=0, maximo=1, amostra=1, invalido=2, rotulo="Esforço")
    cal(ws, "G6", f'=IF({RACA}="Humano","máx 1 · volta no Descanso Longo","só para Humano")', ate="H")
    avj(6, "em_jogo.aviso.esforco",
        f'=IF(LEN({ESF})=0,"",IF(ISNUMBER({ESF}),IF({RACA}<>"Humano","O Esforço é traço do Humano (05). ","")&'
        f'IF({ESF}>1,"Esforço máximo 1 (05).",""),"Esforço precisa ser um número."))')
    rot(ws, "E7", "Memoespírito")
    ent(ws, "F7", "em_jogo.memo_ativo", "lista", "sim_nao", amostra="Sim", rotulo="Memoespírito ativo")
    MPV, MPVMAX = T("em_jogo.memo_pv"), T("memo.pv")
    # rótulo do PV dele à esquerda da entrada (G7), com o máximo; a entrada fica em H7
    cal(ws, "G7", f'=IF({CAM}="A Recordação","PV dele (máx "&{MPVMAX}&")","só A Recordação")',
        nome="em_jogo.memo_pv_max")
    ent(ws, "H7", "em_jogo.memo_pv", "inteiro", minimo=0, maximo=999, amostra=10, rotulo="PV atual do Memoespírito")
    avj(7, "em_jogo.aviso.memo",
        f'=IF(AND(OR({MEMO}="Sim",LEN({MPV})>0),{CAM}<>"A Recordação"),"Memoespírito só na Recordação: não conta. ",'
        f'"")&IF(LEN({MPV})=0,"",IF(ISNUMBER({MPV}),IF(AND({CAM}="A Recordação",{MPV}>{MPVMAX}),'
        f'"PV do Memoespírito acima do máximo ("&{MPVMAX}&"). ",""),"PV do Memoespírito precisa ser um número."))')
    # Acúmulos das Bênçãos (rótulo pela Bênção adquirida)
    lab_a = (f'=IF({tem_bencao("Sacrifício Desesperado")},"Fúria",IF({tem_bencao("Florescimento da Alma")},'
             f'"Florescimento",IF({tem_bencao("Memória Devastadora")},"Fragmentos de Memória",'
             f'IF({CAM}="A Erudição","Acúmulos de Cálculo","—"))))')
    lab_b = f'=IF({tem_bencao("Cicatriz da Destruição")},"Marcas da Ruína","—")'
    max_a = (f'IF({NA}="Fúria",2,IF({NA}="Acúmulos de Cálculo",{teto_calc},IF({NA}="—",0,5)))')
    # o nome do acúmulo (até "Fragmentos de Memória") vai em G, ao lado do máximo em H
    rot(ws, "E8", "Acúmulos")
    ent(ws, "F8", "em_jogo.acumulo.a", "inteiro", minimo=0, maximo=7, amostra=1, rotulo="Acúmulos")
    cal(ws, "G8", lab_a, nome="em_jogo.acumulo.a.nome")
    cal(ws, "H8", f'=IF({NA}="—","sem acúmulo","máx "&{max_a})')
    avj(8, "em_jogo.aviso.acumulo.a",
        f'=IF(LEN({ACA})=0,"",IF(ISNUMBER({ACA}),IF({NA}="—","Nenhuma Bênção sua tem acúmulo neste campo.",'
        f'IF({ACA}>{max_a},"Máximo "&{max_a}&" acúmulos de "&{NA}&".","")),"Acúmulos precisa ser um número."))')
    rot(ws, "E9", "Marcas")
    ent(ws, "F9", "em_jogo.acumulo.b", "inteiro", minimo=0, maximo=5, amostra=1, rotulo="Marcas da Ruína")
    cal(ws, "G9", lab_b, nome="em_jogo.acumulo.b.nome")
    cal(ws, "H9", f'=IF({NB_}="—","sem acúmulo","máx 5")')
    avj(9, "em_jogo.aviso.acumulo.b",
        f'=IF(LEN({ACB})=0,"",IF(ISNUMBER({ACB}),IF({NB_}="—","Nenhuma Bênção sua tem acúmulo neste campo.",'
        f'IF({ACB}>5,"Máximo 5 Marcas da Ruína.","")),"Acúmulos precisa ser um número."))')
    cal(ws, "E10", f'=IF({CAM}="","Recurso do Caminho: escolha o Caminho",'
                   f'IF({CAM}="A Destruição","PV como moeda: "&(2*{LV})&" PV por ativação",'
                   f'IF({CAM}="A Preservação","Barreira: teto "&{T("em_jogo.barreira_max")},'
                   f'IF({CAM}="A Erudição","Acúmulos de Cálculo: máx "&{teto_calc},'
                   f'IF({CAM}="A Caça","Marcação de Presa: 1 alvo · crítico "&IF({tem_bencao("Olho de Lan")},"19-20","20"),'
                   f'IF({CAM}="A Euforia","Tabela do Riso: 1d6 (aba Caminho)",'
                   f'IF({CAM}="A Recordação","Memoespírito: ficha na aba Caminho",'
                   f'IF({CAM}="A Inexistência","Recurso: acúmulos de Marca do Vazio e Corrupção",'
                   f'IF({CAM}="A Harmonia","Recurso: acúmulos de Eco da Vitória (máx 3)",'
                   f'IF({CAM}="A Abundância","Recurso: acúmulos de Florescimento (máx 5)",'
                   f'"Recurso do Caminho: escolha um Caminho da lista"' + ")" * 10, nome="em_jogo.recurso", ate="H")
    corda = T("equipamento.reliquia.corda_de_ligacao.bonus")
    cal(ws, "E11", f'="Energia de equipamento: "&IF({corda}>0,"Corda +"&{corda}&" ao entrar na Fila","sem Corda")&'
                   f'IF({T("equipamento.cone.nivel_usado")}>=3," · Cone +5 por Ciclo","")', nome="em_jogo.energia_equipamento",
        ate="H")
    cal(ws, "E12", f'=IF({T("equipamento.inventario.estado")}="Não consegue se mover","Movimento: não se move (carga)",'
                   f'IF({T("em_jogo.lentidao")}=1,"Movimento: Lentidão, só Esforço Total move 1 passo",'
                   f'"Movimento: 1 Distância por ação · Esforço Total: 2"))', nome="em_jogo.movimento", ate="H")

    # --- Calculadora de dano (I1:L12) — decisão 5, ordem de 23.1 e 23.3 --------------------
    titulo(ws, "I1", "Calculadora de dano (23.1 e 23.3)", ate="L")
    DB, DC, CURA = T("em_jogo.dano.bruto"), T("em_jogo.dano.continuo"), T("em_jogo.cura")
    rot(ws, "I2", "Dano recebido")
    ent(ws, "J2", "em_jogo.dano.bruto", "inteiro", minimo=0, maximo=9999, amostra=20, rotulo="Dano recebido")
    rot(ws, "K2", "depois de dados e bônus")
    _mesclar(ws, "K2", "L")
    avj(10, "em_jogo.aviso.dano",
        f'=IF(LEN({DB})=0,"",IF(ISNUMBER({DB}),IF({DB}<0,"Dano não é negativo: use a cura.",""),'
        f'"Dano recebido precisa ser um número."))')
    rot(ws, "I3", "Contínuo?")
    ent(ws, "J3", "em_jogo.dano.continuo", "lista", "sim_nao", amostra="Sim", rotulo="Dano Contínuo")
    rot(ws, "K3", "Contínuo ignora a RD")
    _mesclar(ws, "K3", "L")
    RDA, APOS, ABS_, PERD = (T(f"em_jogo.dano.{x}") for x in ("rd", "apos_rd", "absorvido", "pv_perdidos"))
    rot(ws, "I4", "RD aplicada")
    cal(ws, "J4", f'=IF({DC}="Sim",0,{T("criacao.rd")})', nome="em_jogo.dano.rd", negrito=True)
    rot(ws, "K5", "mínimo 1")
    _mesclar(ws, "K5", "L")
    rot(ws, "K6", "pelos temporários")
    _mesclar(ws, "K6", "L")
    rot(ws, "I5", "Após a RD")
    cal(ws, "J5", f"=IF(ISNUMBER({DB}),IF({DB}<=0,0,MAX(1,{DB}-{RDA})),0)", nome="em_jogo.dano.apos_rd", negrito=True)
    rot(ws, "I6", "Absorvido")
    cal(ws, "J6", f"=MIN({TMPU},{APOS})", nome="em_jogo.dano.absorvido", negrito=True)
    rot(ws, "I7", "PV perdidos")
    cal(ws, "J7", f"={APOS}-{ABS_}", nome="em_jogo.dano.pv_perdidos", negrito=True)
    rot(ws, "I8", "PV novo")
    cal(ws, "J8", f"=MAX(0,{PVU}-{PERD})", nome="em_jogo.dano.pv_novo", negrito=True)
    cal(ws, "K8", f'="PV novo: "&{T("em_jogo.dano.pv_novo")}&" · temp. "&({TMPU}-{ABS_})', nome="em_jogo.dano.texto",
        ate="L")
    cal(ws, "I9", f'=IF({APOS}=0,"Preencha o dano para ver o resultado",IF({MORR}="Sim",'
                  f'"Já Morrendo: 1 falha (2 se crítico ou Nível 5+)",'
                  f'IF({T("em_jogo.dano.pv_novo")}=0,"Cai a 0 PV: fica Morrendo (23.4)","Continua de pé")))',
        nome="em_jogo.dano.situacao", ate="L")
    rot(ws, "I10", "Cura recebida")
    ent(ws, "J10", "em_jogo.cura", "inteiro", minimo=0, maximo=9999, amostra=10, rotulo="Cura recebida")
    cal(ws, "K10", f'="PV depois: "&IF(ISNUMBER({CURA}),MIN({PVMAX},{PVU}+MAX(0,{CURA})),{PVU})',
        nome="em_jogo.cura.texto", ate="L")
    avj(11, "em_jogo.aviso.cura", f'=IF(AND(LEN({CURA})>0,NOT(ISNUMBER({CURA}))),"Cura precisa ser um número.","")')
    rot(ws, "I11", "Descanso Curto")
    cal(ws, "J11", f"=2*{LV}+{bonus_de('Vigor')}", nome="em_jogo.descanso_curto", negrito=True)
    cal(ws, "K11", f'="PV depois: "&MIN({PVMAX},{PVU}+{T("em_jogo.descanso_curto")})', ate="L")
    cal(ws, "I12", '="Descanso Longo: PV cheios, sem condições, Esforço de volta"', ate="L")

    # --- Linha 13: resumo dos avisos desta aba -------------------------------------------
    # (preenchida no fim, quando todos os avisos da aba já existem)

    # --- Ações (A14:L24) --------------------------------------------------------------------
    titulo(ws, "A14", "Ações — Ataque Básico (18), Habilidades (16) e Ultimate (17)", ate="L")
    # Nome da arma em A:B (até 40 caracteres); "Contra Fraqueza" leva a média junto e Alcance ·
    # Elemento dividem K:L, para tudo caber na própria célula (v1.1)
    cabecalhos(ws, 15, ["Ataque Básico", None, "Ataque", "Dano", "Média", "Do atributo", "Equipamento",
                        "Contra Fraqueza", "Crítico", "RT", "Alcance · Elemento"], altura=None)
    _mesclar(ws, "A15", "B")
    _mesclar(ws, "K15", "L")
    campos_ab = [("C", "rolagem"), ("D", "texto"), ("E", "media"), ("F", "do_atributo"), ("G", "do_equipamento"),
                 ("I", "critico"), ("J", "rt")]
    for linha, base, rotulo_vazio, nome_arma in (
            (16, "principal", "Arma principal", T("criacao.arma.nome")),
            (17, "secundaria", "Arma secundária", T("equipamento.arma2.nome"))):
        cat = T("criacao.arma.categoria") if base == "principal" else T("equipamento.arma2.categoria")
        eb = lambda x: T(f"equipamento.ab.{base}.{x}")  # noqa: E731
        cal(ws, f"A{linha}", f'=IF({cat}="","{rotulo_vazio}: —",IF(LEN({nome_arma})=0,"Arma "&{cat},""&{nome_arma}))',
            nome=f"em_jogo.ab.{base}.nome", ate="B")
        for col, campo in campos_ab:
            cal(ws, f"{col}{linha}", f'={eb(campo)}', nome=f"em_jogo.ab.{base}.{campo}",
                negrito=campo in ("rolagem", "texto"))
        cal(ws, f"H{linha}", f'=IF(LEN({eb("fraqueza")})=0,"",{eb("fraqueza")}&" ("&{eb("media_fraqueza")}&")")',
            nome=f"em_jogo.ab.{base}.fraqueza")
        cal(ws, f"K{linha}", f'=IF(LEN({eb("alcance")})=0,"",{eb("alcance")}&" · "&{eb("elemento")})',
            nome=f"em_jogo.ab.{base}.alcance_elemento", ate="L")
    # Habilidades: 2 colunas de 4. Nome em A:B / G:H (até 40 caracteres); dano e média juntos;
    # Nível, PH, RT e alvos juntos em E:F / K:L
    for c0 in (1, 7):
        cabecalhos(ws, 18, ["Habilidade", None, "Rolagem", "Dano · média", "Nível · PH · RT · alvos"],
                   coluna=c0, altura=None)
        _mesclar(ws, f"{get_column_letter(c0)}18", get_column_letter(c0 + 1))
        _mesclar(ws, f"{get_column_letter(c0 + 4)}18", get_column_letter(c0 + 5))
    for k in range(1, 9):
        linha = 19 + (k - 1) % 4
        c0 = 1 if k <= 4 else 7
        col = lambda d: get_column_letter(c0 + d)  # noqa: E731
        h = lambda x: T(f"habilidades.{k}.{x}")  # noqa: E731
        PR, NE = h("preenchida"), h("nivel_efetivo")
        cal(ws, f"{col(0)}{linha}", f'=IF({PR}=0,"—",{h("nome_exibido")})', nome=f"em_jogo.habilidade.{k}.nome",
            ate=col(1))
        bloq = _ej_bloqueio(NE)
        cal(ws, f"{col(2)}{linha}", f'=IF({PR}=0,"",IF(LEN({bloq})>0,{bloq},IF(LEN({h("rolagem")})=0,'
                                     f'IF({h("tipo")}="Passiva","Passiva","—"),{h("rolagem")})))',
            nome=f"em_jogo.habilidade.{k}.rolagem", negrito=True)
        cal(ws, f"{col(3)}{linha}", f'=IF(LEN({h("total")})=0,"",{h("total")}&" ("&{h("media")}&")")',
            nome=f"em_jogo.habilidade.{k}.total")
        cal(ws, f"{col(4)}{linha}", f'=IF({PR}=0,"",{NE}&" · "&{h("ph")}&" PH · RT "&{h("rt")}&" · "&'
                                     f'{h("alvos")}&IF({h("alvos")}=1," alvo"," alvos"))',
            nome=f"em_jogo.habilidade.{k}.nivel_ph", ate=col(5))
    u = lambda x: T(f"habilidades.ultimate.{x}")  # noqa: E731
    bl_u = _ej_bloqueio(ultimate=True)
    cal(ws, "A23", f'=IF(LEN({u("nome")})=0,"Ultimate: —",""&{u("nome")})', nome="em_jogo.ultimate.nome",
        ate="B")
    cal(ws, "C23", f'=IF(LEN({bl_u})>0,{bl_u},IF(LEN({u("rolagem")})=0,"—",{u("rolagem")}))',
        nome="em_jogo.ultimate.rolagem", negrito=True)
    cal(ws, "D23", f'=IF(LEN({u("total")})=0,"",{u("total")}&" ("&{u("media")}&")")', nome="em_jogo.ultimate.total")
    cal(ws, "E23", f'="RT "&{u("rt")}&" · "&{u("alvos")}&IF({u("alvos")}=1," alvo"," alvos")',
        nome="em_jogo.ultimate.rt_alvos", ate="F")
    # a situação leva a Energia; o efeito (texto longo) fica na aba Habilidades
    cal(ws, "G23", f'="Ultimate ("&{ENU}&"/"&{CUSTO}&" de Energia): "&IF(LEN({bl_u})>0,"BLOQUEADA (Controlado)",'
                   f'IF({T("em_jogo.ultimate_pronta")}="Sim","pronta, diga o nome em voz alta",'
                   f'"faltam "&({CUSTO}-{ENU})))',
        nome="em_jogo.ultimate.situacao", ate="L")
    fur, mar = T("em_jogo.furia"), T("em_jogo.marcas")
    cal(ws, "A24", f'="Neste ataque: "&IF(AND({memo_on},{tem_bencao("Memória Compartilhada")}),'
                   f'"+1d6 (Memória Compartilhada) · ","")&IF(AND({memo_on},'
                   f'{tem_bencao("Fragmentos do Eu Perdido")},{T("caminho.escolha.fragmentos")}="Fúria"),'
                   f'"+1d8 (Memória da Fúria) · ","")&IF({fur}>0,"+"&{fur}&"d6 (Fúria) · ","")'
                   f'&IF({mar}>0,"+"&MIN({teto_b},{mar})&" de dano (Cicatriz) · ","")'
                   f'&IF({T("em_jogo.instinto")}=1,"+2 no ataque, já somado (Instinto) · ","")'
                   f'&"temporários: no máximo +3 por rolagem, fora a Fraqueza (26.6)"',
        nome="em_jogo.extras", ate="L")

    # --- Testes de Resistência e Morrendo (A26:F33) ------------------------------------------
    titulo(ws, "A26", "Testes de Resistência (d20 + Bônus + Eficiência)", ate="F")
    _, van_tr, van_cond, _ = _vantagens_raciais()
    for i, t in enumerate(_valores_lista("tr"), start=27):
        s = slug(t)
        tb = f"testes.tr.{s}"
        rot(ws, f"A{i}", t, negrito=True)
        cal(ws, f"B{i}", f'={T(tb + ".rolagem")}', nome=f"em_jogo.tr.{s}.rolagem", negrito=True)
        # versão curta da Vantagem racial (a frase inteira, com a condição, está na aba Testes)
        f_v = '""'
        if van_cond.get(t):
            f_v = f'IF({_ou_raca(van_cond[t])},"Vantagem condicional",{f_v})'
        if van_tr.get(t):
            f_v = f'IF({_ou_raca(van_tr[t])},"Vantagem ("&{RACA}&")",{f_v})'
        cal(ws, f"C{i}", "=" + f_v, nome=f"em_jogo.tr.{s}.vantagem", ate="D")
        cal(ws, f"E{i}", f'=IF({T(tb + ".extra")}=0,"",{sinal(T(tb + ".extra"))}&" de equipamento/Bênção")',
            ate="F")
    SUC, FAL = T("em_jogo.morrendo.sucessos"), T("em_jogo.morrendo.falhas")
    # Morrendo: cada entrada com o rótulo logo à esquerda; a situação na linha de baixo
    rot(ws, "A33", "Morrendo (DT 10)", negrito=True)
    cal(ws, "B33", f'={T("testes.morrendo.rolagem")}', nome="em_jogo.morrendo.rolagem", negrito=True)
    rot(ws, "C33", "Sucessos")
    ent(ws, "D33", "em_jogo.morrendo.sucessos", "inteiro", minimo=0, maximo=3, amostra=1, invalido=5,
        rotulo="Sucessos no Teste de Morrendo")
    rot(ws, "E33", "Falhas")
    ent(ws, "F33", "em_jogo.morrendo.falhas", "inteiro", minimo=0, maximo=3, amostra=1, invalido=5,
        rotulo="Falhas no Teste de Morrendo")
    sucn = f"IF(ISNUMBER({SUC}),{SUC},0)"
    faln = f"IF(ISNUMBER({FAL}),{FAL},0)"
    rot(ws, "A34", "Morrendo agora", negrito=True)
    cal(ws, "B34", f'=IF({sucn}>=3,"Estabiliza com 1 PV",IF({faln}>=3,"Morre",IF({MORR}="Sim",'
                   f'{sucn}&" sucesso(s), "&{faln}&" falha(s) (0 a 3 cada)","Não está Morrendo")))'
                   f'&IF(LEN({T("testes.morrendo.vantagem")})>0," · Vantagem","")', nome="em_jogo.morrendo.estado",
        ate="F")
    avj(12, "em_jogo.aviso.morrendo",
        f'=IF(OR(AND(LEN({SUC})>0,NOT(ISNUMBER({SUC}))),AND(LEN({FAL})>0,NOT(ISNUMBER({FAL})))),'
        f'"Sucessos e falhas precisam ser números de 0 a 3. ",IF(OR({sucn}>3,{faln}>3),"Sucessos e falhas vão de 0 a 3. ",""))'
        f'&IF(AND({MORR}="Não",{sucn}+{faln}>0),"Contador de Morrendo preenchido com PV acima de 0: a cura zera o '
        f'contador (23.4).","")')

    # --- Perícias com Eficiência (G26:L33) ----------------------------------------------------
    # 10 vagas (5 linhas × 2): 3 do Caminho + 2 + Bônus de Sincronia nunca passam disso
    titulo(ws, "G26", "Perícias com Eficiência (rolagem pronta)", ate="L")
    texto(ws, "W1", "Perícias (auxiliar)", negrito=True)
    pericias = _valores_lista("pericias")
    for i, p in enumerate(pericias, start=2):
        s = slug(p)
        aux(ws, f"W{i}", p)
        efi = T(f"criacao.pericia.{s}.eficiencia")
        ant = "0" if i == 2 else f"X{i - 1}"
        aux(ws, f"X{i}", f'={ant}+IF({efi}="Sim",1,0)')
        aux(ws, f"Y{i}", f'=IF({efi}="Sim",X{i},0)')
        aux(ws, f"Z{i}", f'={T(f"testes.pericia.{s}.rolagem")}')
        aux(ws, f"AA{i}", f'=IF(LEN({T(f"testes.pericia.{s}.vantagem")})>0,"Vantagem","")')
    n_p = len(pericias)
    idx = f"$Y$2:$Y${n_p + 1}"
    for j in range(1, 11):
        linha = 27 + (j - 1) % 5
        c0 = 7 if j <= 5 else 10
        m = f"MATCH({j},{idx},0)"
        # nome (com "· Vantagem" quando houver) em G:H / J:K e a rolagem ao lado
        aux(ws, f"AB{j + 1}", f'=IFERROR(INDEX($AA$2:$AA${n_p + 1},{m}),"")', nome=f"em_jogo.pericia.{j}.vantagem")
        vt = T(f"em_jogo.pericia.{j}.vantagem")
        cal(ws, f"{get_column_letter(c0)}{linha}", f'=IFERROR(INDEX($W$2:$W${n_p + 1},{m})&'
                                                   f'IF(LEN({vt})>0," · Vantagem",""),"")',
            nome=f"em_jogo.pericia.{j}.nome", negrito=True, ate=get_column_letter(c0 + 1))
        cal(ws, f"{get_column_letter(c0 + 2)}{linha}", f'=IFERROR(INDEX($Z$2:$Z${n_p + 1},{m}),"")',
            nome=f"em_jogo.pericia.{j}.rolagem", negrito=True)

    # --- Condições ativas (A35:F40) — decisão 1 --------------------------------------------
    titulo(ws, "A35", "Condições ativas (21.5) — Quebrado é só de inimigos", ate="F")
    # Condição em A:B (a opção mais longa + a seta da lista cabem); o efeito curto vira o tique
    # pronto quando a Eficiência de quem aplicou está preenchida (o tique fica em AD, oculta)
    cabecalhos(ws, 36, ["Condição (preencha)", None, "Turnos", "Ef. aplicador", "Efeito (tique por turno)"],
               altura=None)
    _mesclar(ws, "A36", "B")
    _mesclar(ws, "E36", "F")
    cond_l = dlista("condicoes")
    for k, linha in enumerate(range(37, 41), start=1):
        base = f"em_jogo.condicao.{k}"
        ent(ws, f"A{linha}", f"{base}.nome", "lista", "condicoes", amostra="Lentidão", invalido="Quebrado",
            rotulo=f"Condição {k}", ate="B")
        ent(ws, f"C{linha}", f"{base}.turnos", "inteiro", minimo=0, maximo=99, amostra=2, rotulo="Turnos")
        ent(ws, f"D{linha}", f"{base}.eficiencia", "inteiro", minimo=2, maximo=8, amostra=4,
            rotulo="Eficiência de quem aplicou")
        CN, CE = T(f"{base}.nome"), T(f"{base}.eficiencia")
        # Efeito curto (cabe em E:F numa linha); o verbete inteiro de 21.5 está em Regras Rápidas
        ef_curto = '"veja Regras Rápidas (21.5)"'
        for nome_c, curto in reversed(EJ_EFEITO_CURTO):
            ef_curto = f'IF({CN}={q(nome_c)},{q(curto)},{ef_curto})'
        efa = f"IF(ISNUMBER({CE}),{CE},0)"
        tem_ef = f"ISNUMBER({CE})"
        aux(ws, f"AD{k + 1}", f'=IF({CN}="","",IF({CN}="Sangramento",IF({tem_ef},MIN(INT({PVMAX}*5/100),3*{efa})&'
                              f'" por turno","5% PV, teto 3×Ef"),IF({CN}="Queimadura","2d6+"&IF({tem_ef},{efa},"Ef"),'
                              f'IF(OR({CN}="Choque",{CN}="Aprisionamento"),"1d6+"&IF({tem_ef},{efa},"Ef"),'
                              f'IF(OR({CN}="Cisalhamento de Vento",{CN}="Embaraço"),"1d6 por acúmulo",'
                              f'IF({CN}="Surpreso","casa pulada no 1º Ciclo","—"))))))', nome=f"{base}.tique")
        dot = f'AND({tem_ef},OR({CN}="Sangramento",{CN}="Queimadura",{CN}="Choque",{CN}="Aprisionamento"))'
        tq = T(f"{base}.tique")
        cal(ws, f"E{linha}", f'=IF({CN}="","",IF({dot},IF({CN}="Sangramento",{tq},{tq}&" por turno")'
                             f'&IF({CN}="Aprisionamento"," · Atrasa 2",""),{ef_curto}))', nome=f"{base}.efeito",
            ate="F")
        avj(12 + k, f"em_jogo.aviso.condicao.{k}",
            f'=IF({CN}="","",IF({CN}="Quebrado","Quebrado é só de inimigos (20.3).",IF({CN}="Morrendo",'
            f'"Morrendo liga sozinho com PV 0.",IF(COUNTIF({cond_l},{CN})=0,"Condição fora da lista de 21.5.",""))))')
    reg("em_jogo.condicoes", ws, "A37:A40")
    lista_cond = ['""&A37', '""&A38', '""&A39', '""&A40', f'IF({MORR}="Sim","Morrendo","")',
                  f'IF({T("equipamento.inventario.estado")}<>"Normal","Lentidão (carga)","")']
    num(23, "em_jogo.condicoes_texto", "Condições ativas (texto inteiro)", "=" + _juntar(lista_cond))
    num(24, "em_jogo.condicoes_n", "Condições ativas (quantas)",
        "=" + "+".join(f"IF(LEN({x})>0,1,0)" for x in lista_cond))
    prim = '""'
    for x in reversed(lista_cond):
        prim = f"IF(LEN({x})>0,{x},{prim})"
    num(25, "em_jogo.condicoes_primeira", "Condições ativas (a primeira)", "=" + prim)

    # --- Usos por combate e descanso (G35:L40) ------------------------------------------------
    # 8 usos, um por linha (G:I nome · frequência curta, J usados): o "Bênção · frequência" mais
    # longo (Bênção da Harmonia (Reação) · 1/Desc. Longo) cabe numa linha
    titulo(ws, "G32", "Usos por combate e descanso (preencha os usados)", ate="L")
    texto(ws, "S1", "Usos (auxiliar): nome", negrito=True)
    texto(ws, "T1", "frequência", negrito=True)
    texto(ws, "U1", "entra?", negrito=True)
    texto(ws, "V1", "ordem", negrito=True)
    tec = T("criacao.tecnica.nome")
    nu_cone = T("equipamento.cone.nivel_usado")
    # Frequência curta (cabe ao lado do nome numa linha; a inteira está na aba Caminho e em 23.6/24.6/05)
    itens_uso = [
        ('"Descanso Curto"', '"2/dia"', "1"),
        # o nome da Técnica (até 40 caracteres) está na Criação; aqui cabe só a palavra
        ('"Técnica"', '"2/Desc. Longo"', "1"),
        ('"To na sua mente"', '"2/dia"', f'IF({RACA}="Haloviano",1,0)'),
        ('"Efeito do Cone de Luz"', f'IF({nu_cone}=1,"1/combate","1/Ciclo")', f"IF({nu_cone}>0,1,0)"),
        ('"Corda de Ligação"', '"1/combate"', f'IF({corda}>0,1,0)'),
    ]
    for k in range(1, 11):
        at, fr = T(f"caminho.bencao.slot{k}.ativa"), T(f"caminho.bencao.slot{k}.frequencia")
        curta = f'""&{fr}'
        for longa, c_ in reversed(EJ_FREQ_CURTA):
            curta = f'IF({fr}={q(longa)},{q(c_)},{curta})'
        itens_uso.append((f'""&{at}', curta, f'IF(AND(LEN({at})>0,LEN({fr})>0,{fr}<>"Sem limite declarado"),1,0)'))
    for i, (nome_f, freq_f, inclui) in enumerate(itens_uso, start=2):
        aux(ws, f"S{i}", "=" + nome_f)
        aux(ws, f"T{i}", "=" + freq_f)
        aux(ws, f"U{i}", "=" + inclui)
        ant = "0" if i == 2 else f"MAX($V$2:V{i - 1})"
        aux(ws, f"V{i}", f"=IF(U{i}=1,{ant}+1,0)")
    n_u = len(itens_uso)
    ordem = f"$V$2:$V${n_u + 1}"
    texto(ws, "AC1", "Usos (auxiliar): frequência por linha", negrito=True)
    for j in range(1, EJ_USOS + 1):
        linha = 32 + j
        c0 = 7
        m = f"MATCH({j},{ordem},0)"
        # nome · frequência curta numa célula mesclada de 2 colunas (9 pt), usados na 3ª; linha
        # vazia mostra "—" (é o rótulo da entrada de usados ao lado)
        aux(ws, f"AC{j + 1}", f'=IFERROR(INDEX($T$2:$T${n_u + 1},{m}),"")', nome=f"em_jogo.uso.{j}.frequencia")
        fq = T(f"em_jogo.uso.{j}.frequencia")
        cal(ws, f"{get_column_letter(c0)}{linha}",
            f'=IFERROR(INDEX($S$2:$S${n_u + 1},{m})&IF(LEN({fq})>0," · "&{fq},""),"—")',
            nome=f"em_jogo.uso.{j}.nome", ate=get_column_letter(c0 + 2))
        ent(ws, f"{get_column_letter(c0 + 3)}{linha}", f"em_jogo.uso.{j}.usados", "inteiro", minimo=0, maximo=9,
            amostra=1, rotulo="Usados")
    avj(17, "em_jogo.aviso.usos",
        f'=IF(MAX({ordem})>{EJ_USOS},"Mais usos do que cabem aqui: veja a frequência das Bênçãos na aba Caminho.","")')
    du = T("em_jogo.uso.1.usados")
    avj(18, "em_jogo.aviso.descanso",
        f'=IF(AND(ISNUMBER({du}),{du}>2),"Descanso Curto: até 2 por dia (23.6).","")')
    avj(19, "em_jogo.aviso.temporarios_teto",
        f'=IF({T("em_jogo.temp_ataque.bruto")}>{teto_b},"Bônus temporário no Teste de Ataque acima do teto (+"&{teto_b}&'
        f'"): conta só o teto (26.6). ","")&IF({T("em_jogo.temp_defesa.bruto")}>{teto_b},'
        f'"Defesa temporária acima do teto (+"&{teto_b}&"): conta só o teto (26.6).","")')
    avj(20, "em_jogo.aviso.surpreso", f'=IF({T("em_jogo.surpreso")}=1,"Surpreso: a sua casa é pulada no primeiro Ciclo.","")')

    # --- Linha 13: resumo dos avisos desta aba --------------------------------------------------
    # quantos avisos e o primeiro deles (a lista inteira fica na coluna N, fora da tela): cabe
    # numa linha de A:L mesmo no pior caso (v1.1)
    AVISOS_EM_JOGO[:] = avisos_ej
    cal(ws, "A13", _resumo_avisos_em_jogo(avisos_ej), nome="em_jogo.avisos_resumo", ate="L")
    aviso(ws, "A13")
    fundo = PatternFill(start_color=COR_AVISO_FUNDO, end_color=COR_AVISO_FUNDO, fill_type="solid")
    ws.conditional_formatting.add("A13", FormulaRule(formula=["LEN(A13)>0"], fill=fundo))
    ws.freeze_panes = None
    # Corpo da tela em 9 pt: a tela inteira (A:L × 1-40) tem linhas fixas de 14,25 pt e o
    # texto precisa caber numa linha (auditoria visual, FEAT-004)
    for linha in ws.iter_rows(min_row=1, max_row=40, max_col=12):
        for cel in linha:
            f = cel.font
            if f is not None and f.sz == TAM_CORPO:
                cel.font = Font(name=f.name, size=EJ_FONTE_CORPO, bold=f.b, italic=f.i, color=f.color)


# ---------------------------------------------------------------------------
# Aba Regras Rápidas — referência de uma página (29.12), tabelas lidas da aba Dados
# ---------------------------------------------------------------------------

def _paragrafo(c, s, altura=30):
    ws = c.ws
    if s.startswith("="):
        cal(ws, f"A{c.r}", s, ate="L", quebra=True)
    else:
        rot(ws, f"A{c.r}", s)
        _mesclar(ws, f"A{c.r}", "L")
    ws.row_dimensions[c.r].height = altura
    c.r += 1


def _copiar_bloco(c, bloco, colunas, titulo_txt, altura=None):
    """Copia colunas de um bloco da aba Dados por referência (a aba Dados é a fonte).
    colunas: [(cabeçalho no bloco, nº de colunas mescladas)]."""
    ws = c.ws
    b = MAPA.blocos[f"dados.{bloco}"]
    c.passo(titulo_txt)
    r = c.r

    def alinhar(col, span):
        # 1ª coluna e colunas mescladas (texto) à esquerda; coluna simples (número curto) no centro,
        # para o número ficar embaixo do próprio cabeçalho (auditoria visual, FEAT-004)
        h = "left" if col == 1 or span > 1 else "center"
        return Alignment(horizontal=h, vertical="center", wrap_text=True)

    def cab(r):
        col = 1
        for nome, span in colunas:
            letra = get_column_letter(col)
            cabecalho(ws, f"{letra}{r}", nome).alignment = alinhar(col, span)
            if span > 1:
                _mesclar(ws, f"{letra}{r}", get_column_letter(col + span - 1))
            col += span
        ws.row_dimensions[r].height = 30

    cab(r)
    r += 1
    for i in range(b["linhas"]):
        if i and i % 10 == 0 and b["linhas"] > DISTANCIA_CABECALHO:
            cab(r)                 # tabela longa: o cabeçalho se repete a cada 10 linhas (sem congelar)
            r += 1
        lin = b["primeira_linha"] + i
        col = 1
        for nome, span in colunas:
            letra = get_column_letter(col)
            src = f"'Dados'!${b['colunas'][nome]}${lin}"
            cal(ws, f"{letra}{r}", f'=IF(LEN({src})=0,"",{src})',
                ate=get_column_letter(col + span - 1) if span > 1 else None, quebra=True).alignment = \
                alinhar(col, span)
            col += span
        if altura:
            ws.row_dimensions[r].height = altura
        r += 1
    c.r = r


def aba_regras(ws):
    larguras(ws, {"A": 26, **{get_column_letter(j): 13 for j in range(2, 13)}})
    c = Cursor(ws, 5)
    c.titulo("A rolagem única — 29.12 e 02")
    _paragrafo(c, "d20 + Bônus de Atributo + Eficiência (se treinado) ≥ DT. Arredonde para baixo. Toda instância de "
                  "dano causa no mínimo 1. A Eficácia (2 × Eficiência) nunca entra em Teste de Ataque; a Esquiva soma "
                  "sempre a Eficiência. Vantagem: 2d20, fica o maior; Desvantagem: o menor; não acumulam (02.4).")
    c.passo("Eficiência e Eficácia por nível — 26.4")
    r = c.r
    cabecalhos(ws, r, ["Níveis", "Eficiência", "Eficácia"], altura=None)
    r += 1
    efi = dcol("mestra", "Eficiência")
    for txt, nv in (("1-3", 1), ("4-6", 4), ("7-9", 7), ("10-12", 10), ("13-15", 13), ("16-18", 16), ("19-20", 19)):
        texto(ws, f"A{r}", txt, negrito=True)
        cal(ws, f"B{r}", f'="+"&INDEX({efi},{nv})')
        cal(ws, f"C{r}", f'="+"&(2*INDEX({efi},{nv}))')
        r += 1
    cal(ws, f"D{c.r + 1}", f'="Você agora: nível "&{LV}&", Eficiência +"&{EF}&", Eficácia +"&(2*{EF})', ate="I")
    c.r = r
    c.passo("Bônus de Atributo — 04.2")
    r = c.r
    grupos = (("8-9", 8), ("10-11", 10), ("12-13", 12), ("14", 14), ("15-16", 15), ("17-18", 17), ("19-20", 19))
    cabecalhos(ws, r, ["Valor"] + [g[0] for g in grupos], altura=None)
    r += 1
    texto(ws, f"A{r}", "Bônus", negrito=True)
    for j, (_, v) in enumerate(grupos, start=2):
        b = f"VLOOKUP({v},{dtab('bonus_atributo')},2,FALSE)"
        cal(ws, f"{get_column_letter(j)}{r}", f"={sinal(b)}", negrito=True)
    c.r = r + 1
    _copiar_bloco(c, "dt_faixa", [("Dificuldade", 1), ("1-4", 1), ("5-8", 1), ("9-12", 1), ("13-16", 1),
                                  ("17-20", 1)], "DT por faixa — 27.2")
    _paragrafo(c, f'="A sua faixa agora: "&CHOOSE({FX},"1-4","5-8","9-12","13-16","17-20")&'
                  f'" · Sucesso Automático: bônus total da Perícia ≥ DT, não rola (27.2)"', altura=None)
    _copiar_bloco(c, "dt_subsistema", [("Teste", 4), ("DT", 4), ("Capítulo", 1)],
                  "As cinco DTs de subsistema — 27.3 (vencem a tabela acima e não escalam)")
    c.passo("O turno, as Distâncias e o Teste de Ataque — 18 e 29.12")
    _paragrafo(c, "O turno: 1 Ataque Básico + 1 Ação Complementar + 1 Ação de Movimento, mais a Ultimate (não gasta "
                  "ação) e 1 Reação. Habilidade ocupa o espaço do Ataque Básico. Esforço Total troca Ataque Básico + "
                  "Ação Complementar por 2 Distâncias. Máximo de 1 Ação Extra por criatura por Ciclo.")
    _paragrafo(c, "Distâncias: Pessoal → Curta → Média → Longa → Extrema. Um passo por Ação de Movimento.",
               altura=None)
    _paragrafo(c, "Teste de Ataque: d20 + Atributo de Ataque + Eficiência + Especialização + equipamento ± temporários "
                  "≥ Defesa. 20 natural é crítico (dobra só os dados base); 1 natural erra e não gera Energia. A faixa "
                  "19-20 é exclusiva da Caça (Olho de Lan).")
    _copiar_bloco(c, "habilidades", [("Nível", 1), ("Dano", 1), ("Média do dano", 1), ("Cura", 1),
                                     ("Média da cura", 1), ("Custo (PH)", 1), ("Redução de Tenacidade", 1),
                                     ("Alcance (cumulativo)", 2)], "Habilidades por Nível — 16.3")
    _paragrafo(c, "Mais o Bônus do Atributo de Habilidade, uma vez. Em área: metade dos dados (mínimo 1), até 3 alvos "
                  "(4 nos Níveis 6 e 7), teto absoluto 6, mesmo custo (16.4). Passiva não custa PH e conta no teto de 8.")
    _copiar_bloco(c, "ultimate", [("Faixa de nível", 1), ("Nível equivalente", 1), ("Dano", 1), ("Média do dano", 1),
                                  ("Cura", 1), ("Média da cura", 1), ("Redução de Tenacidade", 1)],
                  "Ultimate por faixa — 17.3 (100 de Energia, 1 por Ciclo)")
    _copiar_bloco(c, "energia", [("Fonte", 3), ("Energia", 5), ("Limite", 3)], "Energia — 17.2", altura=30)
    _copiar_bloco(c, "fraqueza", [("Situação", 3), ("Dano", 4), ("Redução de Tenacidade", 4)],
                  "Fraqueza e Resistência — 20.2 (Redução de Tenacidade só se o ataque acertar)")
    _copiar_bloco(c, "elementos", [("Elemento", 2), ("Dano de Quebra", 3), ("Efeito de Quebra", 3)],
                  "Dano de Quebra — 20.5 (Quebra: dano + efeito + Atrasa 1 casa + Quebrado + 10 de Energia)")
    c.passo("Tetos que a mesa esquece — 26.6, 18.4 e 23.3")
    _paragrafo(c, "Bônus somado +3 (níveis 1-9) / +4 (10-15) / +5 (16-20) · penalidade somada -3 / -4 / -5 (somatórios "
                  "separados) · dados adicionais +3 por rolagem, sem contar a Fraqueza · RD 2 + (2 × Eficiência) · PV "
                  "temporários 3 × Eficiência (não acumulam: fica o maior) · acúmulos de uma condição 5 · Habilidades "
                  "conhecidas 8. Bônus Maior do Cone e bônus de slot de Relíquia ficam fora do teto; Conjuntos e "
                  "Efeito Condicional entram (25.4).", altura=45)
    _paragrafo(c, f'="Os seus tetos agora: bônus +"&{T("nucleo.teto_bonus")}&" · penalidade "&'
                  f'{T("nucleo.teto_penalidade")}&" · RD "&{T("nucleo.teto_rd")}&" · PV temporários "&'
                  f'{T("nucleo.teto_temporarios")}', altura=None)
    _copiar_bloco(c, "condicoes", [("Condição", 2), ("Efeito", 5), ("Duração", 2), ("Acúmulo", 2), ("Só inimigos", 1)],
                  "Condições — 21.5 (no máximo 5 instâncias; cura não remove; Descanso Longo remove todas)",
                  altura=30)
    c.passo("Morrendo, Descanso e variantes — 23.4, 23.6 e 06.4")
    _paragrafo(c, "Morrendo: 0 PV, mantém a casa na Fila, Teste de Força de Vontade DT 10 com d20 + Presença apenas "
                  "(sem Eficiência). 3 sucessos: estabiliza com 1 PV · 3 falhas: morre · 20 natural levanta · 1 natural "
                  "vale 2 falhas · dano é 1 falha (2 se crítico ou Habilidade de Nível 5+) · qualquer cura levanta.",
               altura=45)
    _paragrafo(c, f'="Descanso Curto: 1 hora, até 2 por dia, (2 × nível) + Bônus de Vigor = "&'
                  f'{T("em_jogo.descanso_curto")}&" PV para você. Descanso Longo: 8 horas, 1 por dia, todos os PV, '
                  f'remove todas as condições e devolve o Esforço. A Energia não zera; o PH volta no começo de cada '
                  f'combate."', altura=30)
    _paragrafo(c, "Variante oficial — PV rolado (06.4): role 1d20 no lugar do valor fixo de cada nível, com piso no valor "
                  "fixo menos 3 e teto no valor fixo mais 5. A ficha calcula só o valor fixo: com a variante, "
                  "o Mestre ajusta os PV à mão.", altura=30)
    _paragrafo(c, "Falhe para frente: uma falha em Teste de Perícia nunca trava a cena. A cena avança com custo.",
               altura=None)


# ---------------------------------------------------------------------------
# Aba Início — guia, importação, proteção nativa e Painel de avisos
# ---------------------------------------------------------------------------

def _faixas_de_aviso(celulas):
    """Agrupa células de aviso em faixas contíguas da mesma coluna ('L8:L10', 'L22')."""
    por_col = {}
    for cel in celulas:
        m = re.fullmatch(r"([A-Z]+)(\d+)", cel)
        por_col.setdefault(m.group(1), []).append(int(m.group(2)))
    faixas = []
    for col in sorted(por_col, key=lambda x: (len(x), x)):
        linhas = sorted(por_col[col])
        ini = ant = linhas[0]
        for n in linhas[1:] + [None]:
            if n is not None and n == ant + 1:
                ant = n
                continue
            faixas.append(f"${col}${ini}" if ini == ant else f"${col}${ini}:${col}${ant}")
            if n is not None:
                ini = ant = n
    return faixas


def _painel(aba, celulas):
    """(contagem, primeiro aviso) de uma aba, por faixas exatas de aviso."""
    faixas = _faixas_de_aviso(celulas)
    if not faixas:
        return "=0", '=""'
    refs = [f"'{aba}'!{f}" for f in faixas]
    conta = "+".join(f"SUMPRODUCT((LEN({x})>0)*1)" if ":" in x else f"(LEN({x})>0)*1" for x in refs)
    primeiro = '""'
    for x in reversed(refs):
        primeiro = f'IFERROR(INDEX({x},MATCH("?*",{x},0)),{primeiro})'
    return "=" + conta, "=" + primeiro


def aba_inicio(ws):
    larguras(ws, {"A": 30, "B": 12, **{get_column_letter(j): 13 for j in range(3, 13)}})
    c = Cursor(ws, 5)
    titulo(ws, f"A{c.r}", f"Ficha de Personagem — Explorando Galáxias {VERSAO}", tamanho=TAM_TITULO_ABA, ate="L")
    ws.row_dimensions[c.r].height = 24
    c.r += 1
    _paragrafo(c, f"Sistema de RPG de mesa no universo de Honkai: Star Rail · autoria: MC Filhos · versão {VERSAO} · "
                  "níveis 1 a 20. Ficha automatizada para o Google Planilhas: preencha as células amarelas e o resto "
                  "se calcula sozinho. Ficha V1.2 · revisão 1.", altura=30)
    reg("inicio.autoria", ws, f"A{c.r - 1}")
    # Revisão 2: o Google lê como fórmula o texto que começa com +, - ou =
    _paragrafo(c, "Não comece um texto com +, - ou =: o Google entende como fórmula. Se precisar, digite um "
                  "apóstrofo (') antes.", altura=None)
    reg("inicio.dica_formula", ws, f"A{c.r - 1}")
    ws[f"A{c.r - 1}"].font = fonte(negrito=True, cor=COR_AVISO_TEXTO)

    c.passo("Painel de avisos (automático) — uma linha por aba; zero avisos = ficha conferida")
    r = c.r
    cabecalhos(ws, r, ["Aba", "Avisos", "Primeiro aviso"], altura=None)
    _mesclar(ws, f"C{r}", "L")
    r += 1
    r0 = r
    for aba in ("Criação", "Em Jogo", "Testes", "Habilidades", "Caminho", "Equipamento", "Progressão"):
        conta, primeiro = _painel(aba, MAPA.avisos.get(aba, []))
        texto(ws, f"A{r}", aba, negrito=True)
        cal(ws, f"B{r}", conta, nome=f"inicio.painel.{SLUG[aba]}.contagem", negrito=True)
        # estilo de aviso, mas fora de MAPA.avisos: o painel repete avisos, não conta os seus
        aviso(ws, f"C{r}", primeiro)
        _mesclar(ws, f"C{r}", "L")
        reg(f"inicio.painel.{SLUG[aba]}.primeiro", ws, f"C{r}")
        ws.conditional_formatting.add(f"C{r}", FormulaRule(
            formula=[f"LEN(C{r})>0"], fill=PatternFill(start_color=COR_AVISO_FUNDO, end_color=COR_AVISO_FUNDO,
                                                       fill_type="solid")))
        ws.row_dimensions[r].height = 30
        r += 1
    texto(ws, f"A{r}", "Total", negrito=True)
    cal(ws, f"B{r}", f"=SUM(B{r0}:B{r - 1})", nome="inicio.painel.total", negrito=True)
    cal(ws, f"C{r}", f'=IF(B{r}=0,"Nenhum aviso: a ficha está conferida.","Abra a aba indicada e leia a coluna Aviso '
                     f'(na Em Jogo, a linha 13).")', ate="L", nome="inicio.painel.total.texto")
    # Revisão 2: contador de células com erro. As fórmulas entram em proteger_entradas(), que
    # conhece a área final de cada aba; estas linhas ficam fora da contagem da própria Início.
    r += 1
    r_erros = r
    texto(ws, f"A{r}", "Células com erro na ficha", negrito=True)
    cal(ws, f"B{r}", "=0", nome="inicio.erros.total", negrito=True)
    cal(ws, f"C{r}", '=""', nome="inicio.erros.explicacao", ate="L", quebra=True)
    r += 1
    cabecalhos(ws, r, ["Erros por aba"] + ABAS, altura=30)
    r += 1
    texto(ws, f"A{r}", "Células com erro", negrito=True)
    for j, aba in enumerate(ABAS):
        cal(ws, f"{get_column_letter(2 + j)}{r}", "=0", nome=f"inicio.erros.{SLUG[aba]}")
    LINHAS_CONTADOR.update(inicio=r_erros, fim=r)
    c.r = r + 1

    c.passo("Como usar em 6 passos")
    for s in ("1. Criação: preencha as células amarelas de cima para baixo — são os 12 passos do capítulo 03.",
              "2. Caminho: escolha as Bênçãos nos slots liberados (e monte o Memoespírito, se for A Recordação).",
              "3. Habilidades: escreva as suas Habilidades e a Ultimate; a ficha calcula dados, média, PH e rolagem.",
              "4. Equipamento: Cone de Luz, Relíquias, Conjuntos, arma secundária, inventário e Créditos.",
              "5. Progressão: a cada nível, mude o Nível atual na Criação e preencha os aumentos e as Ressonâncias.",
              "6. Em Jogo: na mesa, use só esta aba — PV, Energia, PH, condições, usos e a calculadora de dano."):
        _paragrafo(c, s, altura=None)

    c.passo("Legenda de cores (a cor nunca é o único sinal: o texto diz)")
    r = c.r
    entrada(ws, f"A{r}", "Entrada (preencha)")
    rot(ws, f"B{r}", "Fundo amarelo com borda: é você quem preenche. Toda entrada sai vazia no arquivo.")
    _mesclar(ws, f"B{r}", "L")
    calculada(ws, f"A{r + 1}", "Calculada (automático)")
    rot(ws, f"B{r + 1}", "Fundo azul-claro: fórmula. Não edite (veja a proteção abaixo).")
    _mesclar(ws, f"B{r + 1}", "L")
    av_ = aviso(ws, f"A{r + 2}", "Aviso")
    av_.fill = PatternFill("solid", fgColor=COR_AVISO_FUNDO)
    rot(ws, f"B{r + 2}", "Texto vermelho em fundo rosa: alguma regra do livro não fechou. O texto diz o quê.")
    _mesclar(ws, f"B{r + 2}", "L")
    titulo(ws, f"A{r + 3}", "Título de bloco", tamanho=TAM_CORPO)
    rot(ws, f"B{r + 3}", "Faixa azul-escura: começo de um bloco, com o capítulo do livro.")
    _mesclar(ws, f"B{r + 3}", "L")
    nao_se_aplica(ws, f"A{r + 4}", "Não se aplica")
    rot(ws, f"B{r + 4}", "Cinza: não vale para o seu personagem (ou é coluna auxiliar).")
    _mesclar(ws, f"B{r + 4}", "L")
    c.r = r + 5

    c.passo("Como importar no Google Planilhas")
    for s in ("1. Envie o arquivo .xlsx para o seu Google Drive.",
              "2. Clique com o botão direito no arquivo → Abrir com → Planilhas Google.",
              "3. No Planilhas: Arquivo → Salvar como Planilhas Google. Use essa cópia (a original continua .xlsx).",
              "4. Confira o Painel de avisos acima: com a ficha em branco ele mostra zero avisos.",
              "5. Para esconder a aba Dados: clique com o botão direito na aba Dados → Ocultar página. "
              "Não apague a aba Dados: as fórmulas leem dela."):
        _paragrafo(c, s, altura=None)

    c.passo("Como proteger as fórmulas (proteção nativa do Google, sem senha)")
    for s in ("1. Dados → Proteger páginas e intervalos → Adicionar uma página ou um intervalo.",
              "2. Escolha a aba (ou os intervalos calculados) e marque Exceto certas células para deixar as amarelas "
              "livres.",
              "3. Definir permissões → Mostrar um aviso ao editar este intervalo → Concluído.",
              "Assim ninguém apaga uma fórmula sem querer: o Google avisa antes de editar."):
        _paragrafo(c, s, altura=None)

    c.passo("O que a ficha não faz (de propósito)")
    # (decisões 4, 5 e 9 do plano; o número da decisão não aparece para o jogador)
    _paragrafo(c, "Não rola dados: ela entrega a rolagem pronta, como d20+6 ou 6d6+4 · média 25, e a mesa "
                  f"rola os dados físicos. Não tem macro nem script: tudo é fórmula, e cada fórmula lê o livro {VERSAO} "
                  "pela aba Dados.", altura=30)
    _paragrafo(c, "PV atual é entrada direta: use a calculadora de dano da aba Em Jogo e copie o PV novo. "
                  "A variante de PV rolado não é calculada (veja Regras Rápidas).", altura=30)


def montar_abas_de_jogo(wb):
    aba_equipamento(wb["Equipamento"])
    alargar_avisos(wb["Equipamento"])   # antes do Início: o painel lê a lista de avisos
    aba_habilidades(wb["Habilidades"])
    aba_em_jogo(wb["Em Jogo"])
    aba_regras(wb["Regras Rápidas"])
    aba_inicio(wb["Início"])        # por último: o painel lê os avisos de todas as abas


def montar_abas_de_construcao(wb):
    aba_criacao(wb["Criação"])
    aba_progressao(wb["Progressão"])
    aba_testes(wb["Testes"])
    aba_caminho(wb["Caminho"])
    for aba in ("Criação", "Caminho"):
        alargar_avisos(wb[aba])      # avisos em K:L onde K está livre (auditoria visual final)
    montar_abas_de_jogo(wb)
    resolver_marcadores(wb)
    proteger_entradas(wb)
    for nome in ABAS:
        formatar_avisos(wb[nome])


# ---------------------------------------------------------------------------
# Revisão 2 — leitura protegida das entradas e contador de erros (Google Planilhas)
# ---------------------------------------------------------------------------
#
# O Google lê como FÓRMULA o que o jogador digita (ou escolhe numa lista) começando com =, +, -
# ou @: "+1d6 de Fogo" vira #ERROR! na própria célula. Para o erro não se espalhar, nenhuma
# fórmula lê uma entrada diretamente: ela lê uma célula da camada de leitura protegida (colunas
# ocultas à direita de cada aba), que devolve "" se a entrada estiver vazia ou com erro e o
# valor da entrada nos outros casos. O vazio é escrito de forma explícita (ISBLANK/ISERROR):
# no Google a referência a célula vazia é vazia, no Excel e na `formulas` é 0.
# Uma coluna de sinal por aba marca as linhas com entrada em erro; o aviso da linha mostra o
# que fazer. O contador da aba Início soma as células com erro de cada aba.

LINHAS_CONTADOR = {}        # {"inicio": linha, "fim": linha} do bloco do contador na Início
LEITURA = {}                # "'Aba'!X5" (camada) -> "'Aba'!B5" (célula lida)
SINAIS = {}                 # "'Aba'!Y5" (sinal da linha) -> ["'Aba'!B5", ...] (entradas da linha)
CONTADOR = {}               # "'Aba'!B12" (célula do contador) -> intervalos contados
# campo de texto longo mesclado até a coluna de aviso: o erro aparece no aviso do mesmo item
AVISO_DO_CAMPO = {
    r"habilidades\.\d\.efeito": lambda n: f"habilidades.aviso.{n.split('.')[1]}",
    r"equipamento\.conjunto\.[abc]\.efeito4": lambda n: f"equipamento.aviso.conjunto.{n.split('.')[2]}",
}
MSG_ERRO_LISTA = "O Google leu como fórmula: escolha de novo na lista."
MSG_ERRO_TEXTO = "O Google leu como fórmula: digite de novo com ' na frente."
MSG_ERRO_GERAL = "O Google leu como fórmula: escolha de novo ou digite com ' na frente."
_RE_REF = re.compile(r"^(?:(?P<aba>'(?:[^']|'')+'|[^'!]+)!)?(?P<c1>\$?[A-Z]{1,3}\$?\d+)"
                     r"(?::(?P<c2>\$?[A-Z]{1,3}\$?\d+))?$")


def _limites(c1, c2):
    from openpyxl.utils.cell import coordinate_from_string
    l1, r1 = coordinate_from_string(c1.replace("$", ""))
    l2, r2 = coordinate_from_string((c2 or c1).replace("$", ""))
    a, b = _col(l1), _col(l2)
    return min(r1, r2), min(a, b), max(r1, r2), max(a, b)


def _tokens(formula):
    from openpyxl.formula import Tokenizer
    tok = Tokenizer(formula)
    if "=" + "".join(t.value for t in tok.items) != formula:
        raise ValueError(f"fórmula que o Tokenizer não reconstrói: {formula}")
    return tok.items


def proteger_entradas(wb):
    """Camada de leitura protegida + sinais de erro por linha + contador da Início."""
    entradas = {}                                   # aba -> {(linha, coluna): nome}
    for nome, info in MAPA.entradas.items():
        aba, cel = REFS[nome]
        r1, c1, _, _ = _limites(cel.split(":")[0], None)
        entradas.setdefault(aba, {})[(r1, c1)] = nome
    # 1) referências (célula ou intervalo) que tocam uma entrada
    pedidos = {}                                    # aba -> set((r, c)) a espelhar
    achados = []                                    # (ws, célula, índice do token, aba alvo, limites)
    for ws in wb.worksheets:
        for linha in ws.iter_rows():
            for cel in linha:
                v = cel.value
                if not (isinstance(v, str) and v.startswith("=")):
                    continue
                for k, t in enumerate(_tokens(v)):
                    if t.type != "OPERAND" or t.subtype != "RANGE":
                        continue
                    m = _RE_REF.match(t.value)
                    if not m:
                        continue
                    alvo = m.group("aba").strip("'").replace("''", "'") if m.group("aba") else ws.title
                    if alvo not in entradas:
                        continue
                    lim = _limites(m.group("c1"), m.group("c2"))
                    r0, c0, r1, c1 = lim
                    if not any(r0 <= r <= r1 and c0 <= c <= c1 for r, c in entradas[alvo]):
                        continue
                    achados.append((ws, cel.coordinate, k, alvo, lim, m.group("aba")))
                    pedidos.setdefault(alvo, set()).update(
                        (r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1))
    # 2) colunas da camada: à direita de tudo, mesma linha, colunas contíguas (intervalo vira
    #    intervalo); depois delas, a coluna de sinal de erro da aba
    base, cmin, sinal_col = {}, {}, {}
    for aba in ABAS:
        if aba not in entradas:
            continue
        ws = wb[aba]
        cols = [c for _, c in pedidos.get(aba, ())]
        base[aba] = ws.max_column + 2
        cmin[aba] = min(cols) if cols else 1
        largura_ = (max(cols) - cmin[aba] + 1) if cols else 0
        sinal_col[aba] = base[aba] + largura_
        COLUNAS_OCULTAS.setdefault(aba, [])
        COLUNAS_OCULTAS[aba] += [get_column_letter(k) for k in range(base[aba], sinal_col[aba] + 1)]
    for aba, cels in pedidos.items():
        ws = wb[aba]
        for r, c in sorted(cels):
            orig = f"${get_column_letter(c)}${r}"
            espelho = f"{get_column_letter(base[aba] + c - cmin[aba])}{r}"
            ws[espelho].value = f'=IF(ISERROR({orig}),"",IF(ISBLANK({orig}),"",{orig}))'
            LEITURA[Mapa.ref(aba, espelho)] = Mapa.ref(aba, orig.replace("$", ""))
    # 3) reescreve as referências para a camada
    por_celula = {}
    for ws, coord, k, alvo, lim, prefixo in achados:
        por_celula.setdefault((ws.title, coord), []).append((k, alvo, lim, prefixo))
    for (aba_f, coord), trocas in por_celula.items():
        cel = wb[aba_f][coord]
        toks = _tokens(cel.value)
        for k, alvo, (r0, c0, r1, c1), prefixo in trocas:
            a = f"${get_column_letter(base[alvo] + c0 - cmin[alvo])}${r0}"
            b = f"${get_column_letter(base[alvo] + c1 - cmin[alvo])}${r1}"
            nova = a if (r0, c0) == (r1, c1) else f"{a}:{b}"
            toks[k].value = f"{prefixo}!{nova}" if prefixo else nova
        cel.value = "=" + "".join(t.value for t in toks)
    # 4) sinal de erro por linha e aviso da linha
    avisos_linha = {}
    for aba, cels in MAPA.avisos.items():
        for x in cels:
            r1, c1, _, _ = _limites(x, None)
            avisos_linha.setdefault((aba, r1), []).append((c1, x))
    import renderizar_ficha as R
    por_aviso = {}                                  # (aba, célula do aviso) -> [(sinal, tipos, rótulo)]
    novos = {}                                      # aba -> nº de avisos novos
    sem_aviso = []
    for aba, ents in entradas.items():
        ws = wb[aba]
        topo, coberta = R._mesclas(ws)
        por_linha = {}
        for (r, c), nome in ents.items():
            por_linha.setdefault(r, []).append((c, nome))
        for r, itens in sorted(por_linha.items()):
            itens.sort()
            sinal_ = f"{get_column_letter(sinal_col[aba])}{r}"
            refs_ = [f"${get_column_letter(c)}${r}" for c, _ in itens]
            ws[sinal_].value = "=" + "+".join(f"ISERROR({x})*1" for x in refs_)
            SINAIS[Mapa.ref(aba, sinal_)] = [Mapa.ref(aba, x.replace("$", "")) for x in refs_]
            tipos = {MAPA.entradas[n]["tipo"] == "lista" and not n.endswith(".item") for _, n in itens}
            rotulo_ = ""
            alvo = avisos_linha.get((aba, r))
            if alvo:
                _, cel_av = max(alvo)                   # o aviso mais à direita da linha
            else:
                # sem aviso na linha: um aviso novo na coluna de aviso da aba (K:L se K estiver
                # livre; na Em Jogo, a coluna N, fora da tela); se a coluna estiver ocupada (texto
                # longo mesclado até L), o aviso da mesma Habilidade/Conjunto, com a linha
                col = EJ_AV if aba == "Em Jogo" else AV
                livre = lambda k: (r, k) not in coberta and (r, k) not in topo and ws.cell(r, k).value is None  # noqa: E731
                if livre(_col(col)):
                    cel_av = f"{col}{r}"
                    nome_av = f"{SLUG[aba]}.aviso.erro.{r}"
                    aviso(ws, cel_av, '=""')
                    if aba != "Em Jogo" and livre(_col(col) - 1):
                        cel_av = f"{get_column_letter(_col(col) - 1)}{r}"
                        ws[cel_av].value, ws[f"{col}{r}"].value = '=""', None
                        aviso(ws, cel_av, '=""')
                        _mesclar(ws, cel_av, col)
                    reg(nome_av, ws, cel_av)
                    MAPA.avisos.setdefault(aba, []).append(cel_av)
                    if aba == "Em Jogo":
                        AVISOS_EM_JOGO.append(cel_av)
                    novos[aba] = novos.get(aba, 0) + 1
                else:
                    nome_av = next((AVISO_DO_CAMPO[p](n) for _, n in itens for p in AVISO_DO_CAMPO
                                    if re.fullmatch(p, n)), None)
                    if nome_av is None or REFS[nome_av][0] != aba:
                        sem_aviso.append((aba, r, [n for _, n in itens]))
                        continue
                    cel_av = REFS[nome_av][1]
                    rotulo_ = f"Linha {r}: "
            por_aviso.setdefault((aba, cel_av), []).append((sinal_, tipos, rotulo_))
    if sem_aviso:
        raise ValueError(f"linhas com entrada e sem célula de aviso: {sem_aviso}")
    for (aba, cel_av), lista in por_aviso.items():
        ws = wb[aba]
        expr = ws[cel_av].value[1:]
        for sinal_, tipos, rotulo_ in reversed(lista):
            msg = MSG_ERRO_GERAL if len(tipos) > 1 else (MSG_ERRO_LISTA if tipos == {True} else MSG_ERRO_TEXTO)
            expr = f"IF({sinal_}>0,{q(rotulo_ + msg)},{expr})"
        ws[cel_av].value = "=" + expr
    if novos:
        # o painel da Início e o resumo da Em Jogo (linha 13) passam a contar os avisos novos
        ini = wb["Início"]
        for aba in novos:
            conta, primeiro = _painel(aba, MAPA.avisos.get(aba, []))
            ini[REFS[f"inicio.painel.{SLUG[aba]}.contagem"][1]].value = conta
            ini[REFS[f"inicio.painel.{SLUG[aba]}.primeiro"][1]].value = primeiro
        if "Em Jogo" in novos:
            wb["Em Jogo"]["A13"].value = _resumo_avisos_em_jogo(AVISOS_EM_JOGO)
    # 5) contador da Início: ISERROR sobre a área usada de cada aba (sem as linhas do contador)
    ini = wb["Início"]
    for aba in ABAS:
        ws = wb[aba]
        fim_col = get_column_letter(ws.max_column)
        if aba == "Início":
            a, b = LINHAS_CONTADOR["inicio"], LINHAS_CONTADOR["fim"]
            faixas = [f"$A$1:${fim_col}${a - 1}"]
            if ws.max_row > b:
                faixas.append(f"$A${b + 1}:${fim_col}${ws.max_row}")
        else:
            faixas = [f"'{aba}'!$A$1:${fim_col}${ws.max_row}"]
        _, cel = REFS[f"inicio.erros.{SLUG[aba]}"]
        ini[cel].value = "=" + "+".join(f"SUMPRODUCT(ISERROR({x})*1)" for x in faixas)
        CONTADOR[Mapa.ref("Início", cel)] = faixas
    _, tot = REFS["inicio.erros.total"]
    primeira = REFS[f"inicio.erros.{SLUG[ABAS[0]]}"][1]
    ultima = REFS[f"inicio.erros.{SLUG[ABAS[-1]]}"][1]
    ini[tot].value = f"=SUM({_abs(primeira)}:{_abs(ultima)})"
    CONTADOR[Mapa.ref("Início", tot)] = [f"{primeira}:{ultima}"]
    _, exp = REFS["inicio.erros.explicacao"]
    ini[exp].value = (f'=IF({_abs(tot)}=0,"Nenhuma célula com erro.","O Google leu como fórmula um texto que começa '
                      f'com +, - ou =. Procure a célula com erro na aba indicada abaixo (o aviso da linha diz o '
                      f'que fazer), apague e escreva de novo com um apóstrofo (\') na frente, ou escolha de novo '
                      f'na lista.")')
    CONTADOR[Mapa.ref("Início", exp)] = [tot]
    print(f"Leitura protegida: {len(LEITURA)} células da camada, {len(SINAIS)} sinais de linha, "
          f"{sum(len(v) for v in SINAIS.values())} entradas com sinal")


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------

def ajustar_layout(wb):
    """Texto fixo que não cabe na célula (auditoria visual, FEAT-004): mede com a mesma
    régua da suíte preview (build/renderizar_ficha.py, Arial) e, quando o texto não pode
    transbordar para células vazias à direita, liga a quebra de linha, alarga a coluna se
    uma palavra sozinha não cabe e aumenta a altura da linha até as linhas caberem. Não
    mexe na tela da Em Jogo (A:L × 1-40, linhas fixas). Células com fórmula não são medidas
    aqui (o valor só existe no cálculo): a suíte preview confere essas em 3 estados."""
    import math
    from copy import copy
    import renderizar_ficha as R

    estima = R.PiorTexto(wb, entradas_texto=_textos_pior_caso())
    # listas dependentes (intervalo local): a opção mais longa que as fórmulas auxiliares podem dar
    for nome, info in MAPA.entradas.items():
        fonte_ = info.get("fonte") or ""
        if info["tipo"] == "lista" and fonte_.startswith("$") and not nome.endswith(".item"):
            aba, cel = REFS[nome]
            estima.textos[Mapa.ref(aba, cel)] = estima.intervalo(aba, fonte_.replace("$", ""))
    estender_titulos(wb)
    # alargar uma coluna muda as medidas: 2 passadas que podem alargar; depois a coluna
    # flexível de cada aba encolhe para a área do jogador caber em 1360 px, e uma última
    # passada só acerta as alturas
    for alargar in (True, True, None, False):
        if alargar is None:
            encaixar_na_tela(wb)
            continue
        for ws in wb.worksheets:
            topo, coberta = R._mesclas(ws)
            em_jogo = ws.title == "Em Jogo"
            avisos_aba = set(MAPA.avisos.get(ws.title, []))
            livres = {REFS[n][1]: n for n, i in MAPA.entradas.items()
                      if (i["tipo"] == "texto" or n.endswith(".item")) and REFS[n][0] == ws.title}
            for linha in ws.iter_rows():
                for cel in linha:
                    s = cel.value
                    r, c = cel.row, cel.column
                    if s is None and cel.coordinate in livres and (r, c) not in coberta:
                        # entrada livre: o texto de pior caso quebra em linhas e a linha cresce
                        s = estima.textos.get(Mapa.ref(ws.title, cel.coordinate), "")
                        if not (cel.alignment and cel.alignment.wrap_text):
                            novo = copy(cel.alignment)
                            novo.wrap_text = True
                            novo.vertical = "top"
                            cel.alignment = novo
                    if not isinstance(s, str) or not s.strip() or (r, c) in coberta:
                        continue
                    if em_jogo and r <= 40:
                        continue
                    if s.startswith("="):
                        # fórmula: aviso, texto buscado na aba Dados e calculada com quebra de
                        # linha, pelo texto mais longo que ela pode mostrar
                        quebra = bool(cel.alignment and cel.alignment.wrap_text)
                        if cel.coordinate not in avisos_aba and not R.busca_dados(s) and not quebra:
                            continue
                        s = estima.formula(s, ws.title)
                        if not s or ws.column_dimensions[get_column_letter(c)].hidden:
                            continue
                    if _cor(cel) == COR_TITULO and not (cel.alignment and cel.alignment.wrap_text):
                        continue                       # título de bloco: a faixa vira mescla (mesclar_titulos)
                    if R.medir(ws, r, c, s, topo) is None:
                        continue
                    r2, c2 = topo.get((r, c), (r, c))
                    f = R.fonte_da_celula(cel)
                    asc, desc = f.getmetrics()
                    lh = asc + desc
                    util = sum(R.px_coluna(ws, k) for k in range(c, c2 + 1)) - R.RESERVA
                    al = cel.alignment
                    if not al.wrap_text:
                        novo = copy(al)
                        novo.wrap_text = True
                        cel.alignment = novo
                    linhas = R.quebrar(s, f, util / R.FOLGA)
                    larga = max(f.getlength(x) for x in linhas) * R.FOLGA
                    if larga > util and not em_jogo and alargar:
                        letra = get_column_letter(c2)
                        atual = R.px_coluna(ws, c2)
                        ws.column_dimensions[letra].width = math.ceil((atual + larga - util + 1 - 5) / 7 * 10) / 10
                        util = sum(R.px_coluna(ws, k) for k in range(c, c2 + 1)) - R.RESERVA
                        linhas = R.quebrar(s, f, util / R.FOLGA)
                    precisa = len(linhas) * lh + 4
                    tem = sum(R.px_linha(ws, k) for k in range(r, r2 + 1))
                    if precisa > tem:
                        dim = ws.row_dimensions[r2]
                        atual_pt = dim.height or ws.sheet_format.defaultRowHeight or 15
                        dim.height = math.ceil(atual_pt + (precisa - tem) * 3 / 4)


# Colunas que encolhem (na ordem) quando o ajuste alargou outras e a área do jogador passou
# de 1360 px: avisos e textos que quebram em linhas. Mínimo de 130 px cada.
COLUNAS_FLEXIVEIS = {"Criação": ["L", "A"], "Testes": ["L", "J"], "Habilidades": ["L"], "Caminho": ["L", "G"],
                     "Equipamento": ["L"], "Progressão": ["I", "H"], "Início": [], "Regras Rápidas": ["A"]}
LARGURA_TELA = 1360


def encaixar_na_tela(wb):
    import renderizar_ficha as R
    for aba, flex in COLUNAS_FLEXIVEIS.items():
        ws = wb[aba]
        ultima = 9 if aba == "Progressão" else 12
        excesso = sum(R.px_coluna(ws, c) for c in range(1, ultima + 1)) - LARGURA_TELA
        for letra in flex:
            if excesso <= 0:
                break
            atual = R.px_coluna(ws, _col(letra))
            novo = max(130, atual - excesso)
            ws.column_dimensions[letra].width = _px_largura(novo)
            excesso -= atual - R.px_coluna(ws, _col(letra))


def _textos_pior_caso():
    """Texto de pior caso de cada entrada ({"'Aba'!A1": texto}) para medir avisos que citam
    o que o jogador digitou: opção mais longa da lista, texto longo do livro ou o máximo."""
    import renderizar_ficha as R
    listas = {l["id"]: l["valores"] for l in ficha_dados.listas()}
    saida = {}
    for k, (nome, info) in enumerate(sorted(MAPA.entradas.items())):
        aba, cel = REFS[nome]
        ref = Mapa.ref(aba, cel)
        fonte_ = info.get("fonte") or ""
        if info["tipo"] == "lista":
            if nome.endswith(".item"):           # inventário: texto livre (como no estado pior-caso)
                saida[ref] = R.texto_pior_caso(40, 7 * k)
            elif fonte_.startswith("lista."):
                saida[ref] = max((str(v) for v in listas[fonte_[6:]]), key=len, default="")
            elif fonte_.startswith('"'):
                saida[ref] = max(fonte_.strip('"').split(","), key=len)
        elif info["tipo"] in ("inteiro", "decimal"):
            saida[ref] = str(info.get("maximo"))
        else:
            saida[ref] = R.texto_pior_caso(R.tamanho_pior_caso(nome), 7 * k)
    return saida


def estender_titulos(wb):
    """Título de bloco é texto branco: se ele passa da faixa azul, o pedaço que transborda
    cai em fundo branco e some (no Google também). A faixa cresce para a direita, só sobre
    células vazias e sem mescla, até o texto caber (auditoria visual, FEAT-004)."""
    import renderizar_ficha as R

    def azul(cel):
        return (cel.fill is not None and cel.fill.patternType == "solid"
                and str(cel.fill.fgColor.rgb or "")[-6:].upper() == COR_TITULO)

    for ws in wb.worksheets:
        topo, coberta = R._mesclas(ws)
        for linha in ws.iter_rows():
            for cel in linha:
                s = cel.value
                if not isinstance(s, str) or not s.strip() or s.startswith("=") or not azul(cel):
                    continue
                r, c = cel.row, cel.column
                if (r, c) in coberta or (r, c) in topo:
                    continue
                ft = cel.font
                f = R.fonte(round((ft.sz or TAM_CORPO) * 4 / 3), ft.b, ft.i)
                precisa = f.getlength(s) * R.FOLGA + R.RESERVA
                k, tem = c, R.px_coluna(ws, c)
                while k + 1 <= ws.max_column and azul(ws.cell(r, k + 1)):
                    k += 1
                    tem += R.px_coluna(ws, k)
                while tem < precisa:
                    k += 1
                    viz = ws.cell(r, k)
                    if (r, k) in coberta or (r, k) in topo or viz.value is not None:
                        break                  # bloqueado: a suíte preview acusa
                    viz.fill = PatternFill("solid", fgColor=COR_TITULO)
                    viz.font = fonte(ft.sz or TAM_TITULO_BLOCO, negrito=True, cor=COR_TITULO_TEXTO)
                    tem += R.px_coluna(ws, k)


# Colunas auxiliares (só guardam valores de apoio das listas dependentes e das contas): ficam
# OCULTAS. A validação de dados pode apontar para elas. Colunas de aviso nunca entram aqui.
COLUNAS_OCULTAS = {
    "Criação": ["M", "N", "O"],
    "Em Jogo": ["O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD"],
    "Habilidades": ["O", "P", "Q", "R", "S", "T", "U", "V", "W"],
    "Caminho": ["M", "N"],
    "Equipamento": ["M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA"],
    "Progressão": ["R"],
}


def ocultar_auxiliares(wb):
    for aba, cols in COLUNAS_OCULTAS.items():
        for letra in cols:
            wb[aba].column_dimensions[letra].hidden = True


def _cor(cel):
    f = cel.fill
    if f is None or f.patternType != "solid":
        return None
    return str(f.fgColor.rgb or "")[-6:].upper() or None


def marcar_tabelas(wb):
    """Zebra e rótulo da linha nas tabelas (cabeçalho de coluna + linhas de dados até a
    linha em branco, o próximo título ou o próximo cabeçalho), e rótulo da linha nos
    formulários (texto fixo na coluna A seguido de valor na mesma linha)."""
    import renderizar_ficha as R
    for ws in wb.worksheets:
        topo, coberta = R._mesclas(ws)
        for tab in R.tabelas(ws):
            for i, r in enumerate(tab["linhas"]):
                prim = None
                for c in range(tab["c0"], tab["c1"] + 1):
                    if (r, c) in coberta:
                        continue
                    cel = ws.cell(r, c)
                    if prim is None and (cel.value is not None or _cor(cel) == COR_ENTRADA):
                        prim = cel
                    if i % 2 == 1:
                        cor = _cor(cel)
                        if cor in (COR_CALCULADA, COR_ENTRADA):
                            cel.fill = PatternFill("solid", fgColor=COR_ZEBRA[cor])
                        elif cor is None:
                            cel.fill = PatternFill("solid", fgColor=COR_ZEBRA[None])
                if prim is not None:
                    estilo_rotulo_linha(prim)
        if ws.title in ("Dados", "Início", "Regras Rápidas"):
            continue
        em_tabela = {r for tab in R.tabelas(ws) for r in [tab["cab"]] + tab["linhas"]}
        for r in range(4, ws.max_row + 1):
            a = ws.cell(r, 1)
            if r in em_tabela or (r, 1) in coberta or not isinstance(a.value, str) or a.value.startswith("=") \
                    or _cor(a) is not None:
                continue
            c2 = topo.get((r, 1), (r, 1))[1]
            depois = [ws.cell(r, c) for c in range(c2 + 1, min(ws.max_column, 12) + 1) if (r, c) not in coberta]
            if any(x.value is not None or _cor(x) == COR_ENTRADA for x in depois):
                estilo_rotulo_linha(a)


def mesclar_titulos(wb):
    """Título de bloco: a faixa azul vira uma mescla só, para o texto caber na própria
    célula (sem transbordar para as vizinhas)."""
    import renderizar_ficha as R
    for ws in wb.worksheets:
        topo, coberta = R._mesclas(ws)
        for linha in ws.iter_rows():
            for cel in linha:
                r, c = cel.row, cel.column
                if (r, c) in coberta or (r, c) in topo or not isinstance(cel.value, str) \
                        or _cor(cel) != COR_TITULO:
                    continue
                k = c
                while k + 1 <= ws.max_column and (r, k + 1) not in coberta and (r, k + 1) not in topo \
                        and ws.cell(r, k + 1).value is None and _cor(ws.cell(r, k + 1)) == COR_TITULO:
                    k += 1
                if k > c:
                    ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=k)


def gerar():
    wb = novo_workbook()
    for nome in ABAS:
        ws = wb[nome]
        cabecalho_aba(ws, SUBTITULOS[nome], linha=42 if nome == "Em Jogo" else 1)
        ws.column_dimensions["A"].width = max(ws.column_dimensions["A"].width or 0, 26)
        ws.sheet_view.showGridLines = True
    escrever_dados(wb["Dados"])
    montar_abas_de_construcao(wb)
    ocultar_auxiliares(wb)
    montar_legendas(wb)
    marcar_tabelas(wb)
    ajustar_layout(wb)
    mesclar_titulos(wb)
    ENTREGA.mkdir(parents=True, exist_ok=True)
    wb.save(SAIDA_XLSX)
    MAPA.salvar(ABAS)
    print(f"Gerado: {SAIDA_XLSX}")
    print(f"Mapa:   {SAIDA_MAPA} ({len(MAPA.celulas)} células, {len(MAPA.blocos)} blocos, "
          f"{len(MAPA.listas)} listas)")
    gravar_exemplo_nadir(wb)


def gravar_exemplo_nadir(wb):
    """O mesmo modelo preenchido com a Nadir de 29.7 (entradas de build/testar_ficha.py,
    as mesmas que a suíte ouro e a prévia usam). Só as células de entrada mudam; as fórmulas
    se calculam ao abrir (fullCalcOnLoad)."""
    import testar_ficha
    mapa = json.loads(SAIDA_MAPA.read_text(encoding="utf-8"))
    entradas = testar_ficha.entradas_nadir_exemplo(mapa)
    for ref, valor in entradas.items():
        if valor is None:
            continue
        aba, cel = ref.rsplit("!", 1)
        wb[aba.strip("'")][cel].value = valor
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
    wb.save(SAIDA_NADIR)
    print(f"Exemplo: {SAIDA_NADIR} ({sum(v is not None for v in entradas.values())} entradas da Nadir, 29.7)")


if __name__ == "__main__":
    gerar()
