# -*- coding: utf-8 -*-
"""Peças comuns dos geradores da Fase 2 (NPCs, Aventuras, Recompensas): campos sorteados (u/y/x de §5 pelo
mestre\\sorteio.py), k-ésimo valor de uma lista da aba Tabelas, nome por cultura e listas suspensas com "Sortear"
lidas da aba Tabelas (coluna auxiliar oculta da própria aba)."""

from openpyxl.utils import get_column_letter as L, column_index_from_string as CI

import mestre_dados as D
import mestre_sabor_nomes as NM
from mestre import nucleo as N
from mestre import sorteio as S
from mestre.nucleo import T, q

M = "2147483647"


def campos(ws, g, rolagem_nome, linha0, col, parametros):
    """Cria as células u/y/x de todos os campos do gerador g (uma linha por campo, colunas ocultas `col`…) e
    registra o gerador no mapa. Devolve {C: referência absoluta de x}."""
    SEM, ROL = T("inicio.semente_ef"), T(rolagem_nome)
    info = D.GERADORES[g]
    N.MAPA.geradores[str(g)] = {"nome": info["nome"], "aba": ws.title, "campos": {}, "rolagem": rolagem_nome,
                                "parametros": list(parametros)}
    xs = {}
    for k, c in enumerate(sorted(info["campos"])):
        cp = S.Campo(ws, linha0 + k, CI(col), SEM, ROL, g, c, f"{N.SLUG[ws.title]}.g{g}.c{c}",
                     lambda w, cel, f, nome: N.aux(w, cel, f, nome=nome))
        xs[c] = cp.xref
        N.MAPA.geradores[str(g)]["campos"][str(c)] = {k2: N.MapaMestre.ref(ws.title, getattr(cp, k2))
                                                     for k2 in ("u", "y", "x")}
    return xs


def n(id_):
    return T(f"tab.{id_}.tamanho")


def k_esimo(id_, k):
    """O k-ésimo valor não vazio da lista tab.<id> ("" se não houver)."""
    return f'IFERROR(INDEX({T(f"tab.{id_}.valores")},MATCH({k},{T(f"tab.{id_}.contador")},0))&"","")'


def sorteia(id_, x):
    """Valor sorteado da lista tab.<id> com o x do campo ("" com a lista vazia)."""
    return f'IF({n(id_)}<=0,"",{k_esimo(id_, S.escolha(x, n(id_)))})'


def sorteia_sem_repetir(id_, x2, i1):
    return f'IF({n(id_)}<=0,"",{k_esimo(id_, S.segundo_sem_repetir(x2, n(id_), i1))})'


def escolher(k, exprs):
    """IF encadeado: exprs[0] se k=1, exprs[1] se k=2, … (sem CHOOSE sobre intervalos)."""
    s = exprs[-1]
    for j in range(len(exprs) - 2, -1, -1):
        s = f"IF({k}={j + 1},{exprs[j]},{s})"
    return s


def ridx(raca):
    """Índice da Raça (1 a 7) na ordem de 05; 1 se não achar (a Raça efetiva sempre está na lista)."""
    return f'IFERROR(MATCH({raca},{N.dcol("culturas", "Raça")},0),1)'


def nome_cultura(ri, x_nome, x_sob):
    """Nome completo pela cultura de índice `ri` (05): nome e sobrenome sorteados nas listas da cultura e montados
    na ordem da cultura (Xianzhouíta: família primeiro)."""
    nomes = [sorteia(f"nome.{NM.SLUG[c]}", x_nome) for c in NM.CULTURAS]
    sobs = [sorteia(f"sobrenome.{NM.SLUG[c]}", x_sob) for c in NM.CULTURAS]
    return escolher(ri, nomes), escolher(ri, sobs)


def montar_nome(ri, nome, sob):
    ordem = f'INDEX({N.dcol("culturas", "Ordem")},{ri})'
    sep = f'INDEX({N.dcol("culturas", "Separador")},{ri})'
    return (f'IF(LEN({sob})=0,{nome},IF(LEN({nome})=0,{sob},IF({ordem}=2,{sob}&{sep}&{nome},'
            f'{nome}&{sep}&{sob})))')


def lista_com_sortear(ws, col, linha0, id_, nome, sortear=True):
    """Coluna auxiliar oculta: "Sortear" (opcional) + os 100 valores da lista tab.<id> (fonte de uma lista suspensa).
    Devolve a fonte da validação (intervalo absoluto da própria aba)."""
    import re
    d = 0
    if sortear:
        N.aux(ws, f"{col}{linha0}", '="Sortear"')
        d = 1
    t = N.MAPA.tabelas[f"tab.{id_}"]
    for k, cel in enumerate(t["vagas"]):
        c, r = re.match(r"([A-Z]+)(\d+)", cel).groups()
        N.aux(ws, f"{col}{linha0 + d + k}", f"='Tabelas'!${c}${r}&\"\"")
    fim = linha0 + d + len(t["vagas"]) - 1
    N.reg(nome, ws, f"{col}{linha0}:{col}{fim}")
    return f"${col}${linha0}:${col}${fim}"


def linhas_do_intervalo(id_):
    """[(i, é_cabeçalho)] para i = 1…n do intervalo tab.<id>.valores (da 1ª vaga à última linha; os cabeçalhos
    repetidos entre as faixas de vagas ficam dentro do intervalo)."""
    import re
    t = N.MAPA.tabelas[f"tab.{id_}"]
    num = lambda c: int(re.search(r"\d+", c).group(0))  # noqa: E731
    vagas = [num(c) for c in t["vagas"]]
    cabs_ = {num(c) for c in t["cabecalhos"]}
    return [(k + 1, r in cabs_) for k, r in enumerate(range(vagas[0], vagas[-1] + 1))]


def contador_chave(ws, col, linha0, id_, chave, nome):
    """Contador corrido (coluna oculta `col`, a partir de `linha0`) das linhas da tabela de duas colunas tab.<id> cuja
    1ª coluna é igual a `chave` e cuja 2ª coluna não está vazia. Devolve (célula do total, nome do intervalo)."""
    keys, vals = T(f"tab.{id_}.valores"), T(f"tab.{id_}.valores2")
    linhas = linhas_do_intervalo(id_)
    for i, cab in linhas:
        r = linha0 + i - 1
        prev = "0" if i == 1 else f"${col}${r - 1}"
        f = f"={prev}" if cab else (f'={prev}+IF(AND(LEN({chave})>0,INDEX({keys},{i})&""={chave},'
                                    f'LEN(INDEX({vals},{i})&"")>0),1,0)')
        N.aux(ws, f"{col}{r}", f, nome=f"{nome}.{i}")
    fim = linha0 + len(linhas) - 1
    N.reg(nome, ws, f"{col}{linha0}:{col}{fim}")
    return f"${col}${fim}", T(nome)


def ancora(campo, chave):
    """Número da âncora de 28.3 (bloco Dados 'ancoras') para a chave 'faixa|tipo'."""
    return N.dbusca("ancoras", "Chave", chave, campo)


def sinal(x):
    return f'IF(LEN({x}&"")=0,"","+"&{x})'
