# -*- coding: utf-8 -*-
"""Execução paralela das suítes de volume (oraculo, extremos) — plano §10 item 8 ("paralelizar, até 8
processos, antes de reduzir casos"); revisão da Fase 1, F2 (as suítes não terminavam).

Como funciona
    A suíte monta a lista COMPLETA de casos (as mesmas quantidades do plano, a mesma semente de random) sem
    calcular nada. `executar` reparte os casos entre N processos `testar_mestre.py --trabalhador`; cada um carrega
    o modelo (formulas 1.3.4) uma vez, calcula a sua parte e grava um JSON com checagens, falhas e os números de
    regra comparados (cobertura P10). O processo principal junta tudo num `Resultado` só.

Por que é rápido
    O custo da `formulas` está em reduzir o grafo às entradas e saídas do caso (shrink_dsp, uns 5 s); o cálculo
    reduzido leva centésimos. Dentro de um grupo de casos com as mesmas saídas, toda entrada que algum caso preenche
    e outro não é passada como "" (texto vazio) nos casos que não a preenchem: o conjunto de entradas fica igual e a
    redução é feita uma vez só. Isso é exato porque nenhuma fórmula lê uma entrada diretamente (lint, requisito do
    Google): a leitura passa pela camada protegida IF(ISERROR(X),"",IF(ISBLANK(X),"",X)), que dá "" tanto para a
    célula vazia quanto para "" — e o sinal/contador usam ISERROR, que dá 0 nos dois. As vagas da aba Tabelas já
    vêm preenchidas no arquivo: para elas o preenchimento é o próprio valor do arquivo (Fase 2: sem isso, o estado
    "em branco" herdava as listas vazias de outro caso do mesmo grupo). O oráculo recebe o caso sem o preenchimento.

Tipos de caso
    {"tipo": "comparar", "rot", "E" (nomes lógicos), "pref", "lim"}     oráculo × planilha (como testes_regras.comparar)
    {"tipo": "erros", "rot", "E" (refs; ["ERRO", "#VALUE!"] = valor de erro injetado), "outs" (lista ou "@nome"),
     "vazios", "cheios", "msg_v", "msg_c", "iguais" ({ref: valor esperado}), "nao_erro" (refs que podem ter erro)}

Processos: variável de ambiente MESTRE_PROCESSOS (padrão 8, o teto do plano).
"""

import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import testar_ficha as TF
from mestre import nucleo as N

PROCESSOS = max(1, min(8, int(os.environ.get("MESTRE_PROCESSOS", "8"))))
CLI = Path(__file__).resolve().parent.parent / "testar_mestre.py"
PESADO = 1500          # acima disso, cálculo completo (reduzir o grafo custaria mais que calcular tudo)


def _grupo(t):
    saida = t.get("pref") if t["tipo"] == "comparar" else t.get("outs")
    return json.dumps([t["tipo"], saida, sorted(t.get("iguais", {}))], ensure_ascii=False)


def _peso(t, listas):
    if t.get("peso"):
        return float(t["peso"])
    if t.get("modo") == "bloco":
        return 0.7
    outs = t.get("outs")
    n = len(listas.get(outs[1:], [])) if isinstance(outs, str) else len(outs or [])
    return 14.0 if n > PESADO else 1.0


def repartir(tarefas, n, listas):
    """Grupos (mesmas saídas) partidos em pedaços de peso ≤ total/n, e cada pedaço para o processo menos carregado.
    Cada pedaço custa uma redução do grafo (+ 6)."""
    grupos = {}
    for t in tarefas:
        grupos.setdefault(_grupo(t), []).append(t)
    total = sum(_peso(t, listas) for t in tarefas) + 6 * len(grupos)
    teto = max(1.0, total / n)
    pedacos = []
    for g in grupos.values():
        atual, peso = [], 6.0
        for t in g:
            if atual and peso + _peso(t, listas) > teto:
                pedacos.append((peso, atual))
                atual, peso = [], 6.0
            atual.append(t)
            peso += _peso(t, listas)
        pedacos.append((peso, atual))
    partes, carga = [[] for _ in range(n)], [0.0] * n
    for peso, p in sorted(pedacos, key=lambda x: -x[0]):
        k = carga.index(min(carga))
        partes[k].append(p)
        carga[k] += peso
    return [p for p in partes if p]


def executar(r, tarefas, listas=None, progresso=print):
    """Roda as tarefas em paralelo e soma checagens/falhas em `r`. Devolve os números de regra comparados (P10)."""
    listas = listas or {}
    t0 = time.time()
    partes = repartir(tarefas, min(PROCESSOS, max(1, len(tarefas))), listas)
    tmp = Path(tempfile.mkdtemp(prefix="mestre-par-", dir=N.TEMP))
    comparados = set()
    try:
        procs = []
        env = dict(os.environ, PYTHONUTF8="1")
        for i, p in enumerate(partes):
            arq = tmp / f"parte{i}.json"
            arq.write_text(json.dumps({"listas": listas, "pedacos": p}, ensure_ascii=False), encoding="utf-8")
            log = open(tmp / f"parte{i}.log", "w", encoding="utf-8")
            procs.append((i, subprocess.Popen([sys.executable, str(CLI), "--trabalhador", str(arq)], stdout=log,
                                              stderr=subprocess.STDOUT, cwd=str(N.RAIZ), env=env), log))
        for i, pr, log in procs:
            pr.wait()
            log.close()
            res = tmp / f"parte{i}.res.json"
            if pr.returncode != 0 or not res.exists():
                cauda = (tmp / f"parte{i}.log").read_text(encoding="utf-8", errors="replace")[-1500:]
                r.falha(f"processo {i} terminou com código {pr.returncode} sem resultado: {cauda}")
                continue
            d = json.loads(res.read_text(encoding="utf-8"))
            r.checagens += d["checagens"]
            r.falhas.extend(d["falhas"])
            comparados.update(d["comparados"])
            progresso(f"processo {i + 1}/{len(partes)}: {d['casos']} casos em {d['tempo']:.0f} s "
                      f"({len(d['falhas'])} falha(s))")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    r.info(f"{len(tarefas)} casos em {len(partes)} processos: {time.time() - t0:.0f} s")
    return comparados


# ---------------------------------------------------------------------------
# processo filho
# ---------------------------------------------------------------------------

_REDUZIDOS = {}


def _valor(v):
    if isinstance(v, list) and len(v) == 2 and v[0] == "ERRO":
        return TF._valor_de_erro(v[1])
    return v


def calcular(ins_refs, outs_refs):
    """{ref: valor} × [refs] -> {ref: valor normalizado}; grafo reduzido guardado por (entradas, saídas)."""
    from mestre import testes_comum as TC
    m = TC.modelo()
    # None (entrada vazia) vira "" — a camada de leitura protegida dá o mesmo resultado para os dois
    ins = {m.chave(k): ("" if v is None else _valor(v)) for k, v in ins_refs.items()}
    outs = [o for o in dict.fromkeys(m.chave(x) for x in outs_refs) if o in m.modelo.cells]
    if not outs:
        sol = {}
    elif len(outs) > PESADO:
        sol = m.modelo.calculate(inputs=ins, outputs=outs)
    else:
        chave = (frozenset(ins), tuple(outs))
        if chave not in _REDUZIDOS:
            if len(_REDUZIDOS) > 16:
                _REDUZIDOS.clear()
            _REDUZIDOS[chave] = m.modelo.dsp.shrink_dsp(inputs=list(ins), outputs=outs)
        sol = _REDUZIDOS[chave].dispatch(inputs=ins, outputs=outs)
    return {x: (TF.normalizar_valor(sol[m.chave(x)]) if m.chave(x) in sol else None) for x in outs_refs}


class Fronteira:
    """Cálculo incremental exato para uma série de casos que só muda um conjunto FIXO de entradas V (modo "bloco":
    a calculadora do Combate, 40 casos por alvo, V = as entradas da calculadora).
    A base B é o cálculo completo do primeiro caso do bloco. Só os nós que descendem de V podem mudar; os dados que
    alimentam esses nós sem descender de V (a fronteira) têm em B o mesmo valor que teriam no caso e entram como
    entrada do grafo reduzido (V + fronteira), que é construído uma vez por processo (só depende da estrutura) e
    calcula um caso em ~0,35 s em vez de ~4 s. Se o caso muda alguma entrada fora de V (outro alvo), a base é
    refeita. A exatidão é conferida pela própria suíte: cada caso é comparado com o oráculo independente."""

    def __init__(self):
        from mestre import testes_comum as TC
        self.m = TC.modelo()
        self.dsp = self.m.modelo.dsp
        self.B, self.IB = None, None
        self.red = {}

    def _base(self, ins):
        self.B = self.m.modelo.calculate(inputs=ins)
        self.IB = dict(ins)

    def _desc(self, D):
        g = self.dsp.dmap
        desc, pilha = set(D), list(D)
        while pilha:
            for y in g.succ.get(pilha.pop(), {}):
                if y not in desc:
                    desc.add(y)
                    pilha.append(y)
        return desc

    def calcular(self, ins, outs, V):
        if self.B is None:
            self._base(ins)
        D = {k for k in set(ins) | set(self.IB) if ins.get(k, "") != self.IB.get(k, "")}
        if not D:
            return {o: self.B[o] for o in outs if o in self.B}
        if not D <= V:
            self._base(ins)
            return {o: self.B[o] for o in outs if o in self.B}
        Vg = sorted(V)
        chave = (tuple(Vg), tuple(outs))
        if chave not in self.red:
            desc = self._desc(Vg)
            nos = self.dsp.nodes
            fr = {p for f in desc if nos.get(f, {}).get("type") == "function" for p in self.dsp.dmap.pred.get(f, {})
                  if p not in desc}
            alvo = [o for o in outs if o in desc]
            self.red[chave] = (desc, fr, alvo, self.dsp.shrink_dsp(inputs=Vg + sorted(fr), outputs=alvo)
                               if alvo else None)
        desc, fr, alvo, red = self.red[chave]
        sol = {o: self.B[o] for o in outs if o not in desc and o in self.B}
        if red is not None:
            entrada = {k: self.B[k] for k in fr if k in self.B}
            entrada.update({k: ins.get(k, "") for k in Vg})
            s = red.dispatch(inputs=entrada, outputs=alvo)
            sol.update({o: s[o] for o in alvo if o in s})
        return sol


_FRONTEIRA = {}


def _calc_caso(t, ins_refs, outs_refs, gid):
    if t.get("modo") != "bloco":
        return calcular(ins_refs, outs_refs)
    from mestre import testes_comum as TC
    m = TC.modelo()
    ins = {m.chave(k): ("" if v is None else _valor(v)) for k, v in ins_refs.items()}
    outs = [o for o in dict.fromkeys(m.chave(x) for x in outs_refs) if o in m.modelo.cells]
    V = {m.chave(TC.C(n)) for n in t["var"]}
    for k in V:
        ins.setdefault(k, "")
    sol = _FRONTEIRA.setdefault(gid, Fronteira()).calcular(ins, outs, V)
    return {x: (TF.normalizar_valor(sol[m.chave(x)]) if m.chave(x) in sol else None) for x in outs_refs}


def _comparar(r, t, pad, comparados, gid=None):
    import oraculo_mestre as O
    from mestre import testes_comum as TC
    E = t["E"]
    esp = O.calcular(dict(E))
    cel, regra = TC.mapa()["celulas"], TC.mapa()["numeros_de_regra"]
    pref = t.get("pref")
    nomes = [n for n in esp if n in cel and (pref is None or n.startswith(tuple(pref)))]
    ins = {**pad, **TC.entradas(E)}
    sol = _calc_caso(t, ins, [cel[n] for n in nomes], gid)
    ruins = 0
    for n in nomes:
        v = sol.get(cel[n])
        v = "" if v is None else v
        ok = TF._igual(v, esp[n]) or (esp[n] == "" and v in ("", None))
        if n in regra:
            comparados.add(n)
        if not r.ok(ok, f"[{t['rot']}] {n}: planilha={v!r} oráculo={esp[n]!r}"):
            ruins += 1
            if ruins >= t.get("lim", 8):
                break


def _erros(r, t, pad, listas, gid=None):
    outs = listas[t["outs"][1:]] if isinstance(t["outs"], str) else list(t["outs"])
    extra = t.get("vazios", []) + t.get("cheios", []) + list(t.get("iguais", {}))
    sol = _calc_caso(t, {**pad, **t["E"]}, outs + [x for x in extra if x not in outs], gid)
    pode = set(t.get("nao_erro", []))
    er = [k for k, v in sol.items() if TF.eh_erro(v) and k not in pode]
    r.ok(not er, f"[{t['rot']}] {len(er)} célula(s) de erro: {er[:40]}")
    if t.get("vazios"):
        acesos = [a for a in t["vazios"] if sol.get(a) not in ("", None)]
        r.ok(not acesos, f"[{t['rot']}] {t.get('msg_v', 'aviso aceso')}: {acesos[:6]}")
    if t.get("cheios"):
        apagados = [a for a in t["cheios"] if sol.get(a) in ("", None, 0)]
        r.ok(not apagados, f"[{t['rot']}] {t.get('msg_c', 'sem aviso')}: {apagados[:6]}")
    for ref, esperado in t.get("iguais", {}).items():
        r.ok(TF._igual(sol.get(ref), esperado), f"[{t['rot']}] {ref} = {sol.get(ref)!r}, esperado {esperado!r}")


_ORIG = {}


def _original(ref):
    """Valor da célula no modelo gravado ("" se vazia) — só a aba Tabelas tem entradas que já vêm preenchidas."""
    aba, cel = TF.separar_ref(ref)
    if aba != "Tabelas":
        return ""
    if not _ORIG:
        import openpyxl
        ws = openpyxl.load_workbook(N.SAIDA_MODELO)["Tabelas"]
        for linha in ws.iter_rows():
            for c in linha:
                if c.value is not None and not (isinstance(c.value, str) and c.value.startswith("=")):
                    _ORIG[c.coordinate] = c.value
        _ORIG.setdefault("__carregado__", True)
    return _ORIG.get(cel.replace("$", ""), "")


def trabalhador(arquivo):
    """Ponto de entrada do processo filho (testar_mestre.py --trabalhador <parte.json>)."""
    from mestre import testes_comum as TC
    t0 = time.time()
    d = json.loads(Path(arquivo).read_text(encoding="utf-8"))
    listas = d["listas"]
    r = TF.Resultado("parte")
    comparados = set()
    n = 0
    for gid, pedaco in enumerate(d["pedacos"]):
        # preenchimento com "" (ver o cabeçalho): a união das entradas do pedaço
        chaves = set()
        for t in pedaco:
            chaves.update(TC.entradas(t["E"]) if t["tipo"] == "comparar" else t["E"])
        # a célula que já vem preenchida no arquivo (as vagas da aba Tabelas, com o texto do livro e das tabelas de
        # sabor) é preenchida com o próprio valor do arquivo, não com "": só a célula vazia no arquivo equivale a ""
        pad = {k: _original(k) for k in chaves}
        for t in pedaco:
            if n % 25 == 0:
                print(f"{time.strftime('%H:%M:%S')} caso {n}: {t['rot']}", flush=True)
            n += 1
            if t["tipo"] == "comparar":
                _comparar(r, t, pad, comparados, gid)
            else:
                _erros(r, t, pad, listas, gid)
        _FRONTEIRA.pop(gid, None)
    saida = Path(str(arquivo)[:-len(".json")] + ".res.json")
    saida.write_text(json.dumps({"checagens": r.checagens, "falhas": r.falhas, "comparados": sorted(comparados),
                                 "casos": n, "tempo": time.time() - t0}, ensure_ascii=False), encoding="utf-8")
