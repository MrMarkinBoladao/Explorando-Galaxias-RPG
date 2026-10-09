# -*- coding: utf-8 -*-
"""
Suítes da Fase 4 (plano §7 e §8): exemplo, entregaveis e guia.

  exemplo      o Exemplo gravado é o do gerador (cada entrada igual a exemplo.entradas_nomes()); os 4 PJs iguais a
               oraculo_ficha.calcular; o encontro A (320 de 352, 91%, típico, contrato com 3); a Fila do Ciclo 1 e a do
               Ciclo 2 iguais às do oráculo; o critério de aceitação do pedido do Memoespírito e das condições (M1–M4,
               C1–C6, seção 5 do pedido); §14 inteira; nenhuma célula de erro; e o modelo em branco com os geradores
               funcionando na semente padrão (12345), iguais ao oráculo.
  entregaveis  os 3 entregáveis com os nomes exatos (nucleo.SAIDA_*) e nada mais em Mestre\\ além do registro V1.1, dos
               atalhos .gsheet do usuário (só o nome é olhado) e do desktop.ini do Drive.
  guia         toda célula citada no COMO-USAR como `Aba!A1` mostra **valor** é conferida na planilha calculada (o
               Exemplo; "em branco" na linha = o modelo em branco); as abas citadas existem; "página N de 5" do Escudo.
               A ortografia e o glossário do guia ficam na suíte texto.
"""

import re

import testar_ficha as TF
import oraculo_mestre as O
from mestre import nucleo as N
from mestre import testes_comum as TC

Resultado = TF.Resultado

# um campo de saída por gerador, conferido no modelo em branco (semente padrão 12345, Rolagem nº 1)
GERADORES_BRANCO = {100: "encontros.ale.v1.criatura", 200: "npcs.saida.nome", 300: "aventuras.saida.missao",
                    400: "recompensas.ach.bugiganga", 410: "recompensas.cone.nome", 420: "recompensas.conj.nome",
                    510: "mundos.planeta.nome", 520: "mundos.estacao.nome", 530: "mundos.nave.nome",
                    540: "mundos.faccao.nome", 550: "mundos.org.nome", 560: "mundos.nomes.1.pessoa",
                    600: "improviso.rumor.1", 610: "improviso.evento.evento", 620: "improviso.loja.1.item",
                    630: "improviso.bug.1"}
REGISTRO_V11 = "Planilha do Mestre - Explorando Galáxias V1.1.xlsx"


def _calc_arquivo(caminho, nomes, E=None):
    m = TC.modelo(caminho)
    refs = [TC.C(n) for n in nomes]
    sol = m.calcular(TC.entradas(E or {}), refs)
    inv = {TC.C(n): n for n in nomes}
    return {inv[k]: ("" if v is None else v) for k, v in sol.items()}


def suite_exemplo(args):
    import openpyxl
    from mestre import exemplo
    from mestre.aba_combate_base import slot, MI0
    r = Resultado("exemplo")
    E = exemplo.entradas_nomes()
    # (1) o arquivo é o do gerador: cada entrada do Exemplo tem o valor de entradas_nomes(); as outras, vazias
    wb = openpyxl.load_workbook(N.SAIDA_EXEMPLO)
    mp = TC.mapa()
    for nome in mp["entradas"]:
        aba, cel = TF.separar_ref(mp["celulas"][nome])
        v = wb[aba][cel].value
        esp = TC.digitado(nome, E[nome]) if nome in E else None
        r.ok(v == esp or (v is not None and esp is not None and TF._igual(v, esp)),
             f"Exemplo {nome} ({aba}!{cel}) = {v!r}, esperado {esp!r}")
    r.info(f"{len(E)} entradas preenchidas no Exemplo, conferidas uma a uma contra exemplo.entradas_nomes()")
    # (2) §14 inteira
    conta = lambda pref, suf: sum(1 for k in E if k.startswith(pref) and k.endswith(suf))  # noqa: E731
    for rot, n, minimo in (("facções", conta("campanha.fac.", ".nome"), 3), ("relógios", conta("campanha.rel.", ".nome"), 3),
                           ("linha do tempo", conta("campanha.tl.", ".evento"), 6), ("missões", conta("missoes.", ".missao"), 3),
                           ("NPCs no Elenco", conta("npcs.elenco.", ".nome"), 6), ("cartões", conta("npcs.cartao", ".npc"), 4),
                           ("Tesouro", conta("recompensas.tes.", ".item"), 2), ("inimigos criados", conta("inimigos.", ".nome")
                                                                             - conta("inimigos.acao", ".nome"), 2),
                           ("cenas da sessão 2", conta("sessoes.cena.", ".tipo"), 5), ("diário", conta("sessoes.diario.", ".resumo"), 1),
                           ("Clima no Expresso", conta("minhas.1.vaga", ""), 12), ("PJs", conta("grupo.pj", ".nome")
                                                                                 - conta("grupo.pj", "memo.nome"), 4)):
        r.ok(n >= minimo, f"§14: {rot} = {n} (mínimo {minimo})")
    r.ok(E.get("inicio.semente") == 2026 and E.get("sessoes.prep.n") == 2 and E.get("recompensas.nivel") == 2,
         "§14: semente 2026, sessão 2 preparada, marco do nível 2")
    # (3) os 4 PJs = oraculo_ficha.calcular (o Exemplo grava os números de exemplo.grupo(), que já falha com aviso)
    gr = exemplo.grupo()
    r.ok([p["nome"] for p in gr][0] == "Nadir" and len({p["raca"] for p in gr}) == 4 and len({p["caminho"] for p in gr}) == 4,
         f"grupo: Nadir de 29.7 + 3 de outras Raças e Caminhos: {[(p['raca'], p['caminho']) for p in gr]}")
    for i, p in enumerate(gr, start=1):
        for k, v in p.items():
            if v is not None:
                r.ok(TF._igual(E.get(f"grupo.pj{i}.{k}"), v), f"PJ {i} {k}: Exemplo {E.get(f'grupo.pj{i}.{k}')!r} ≠ ficha {v!r}")
    memo = exemplo.memo_kv()
    for k, cm in (("pv", "pv"), ("def", "defesa"), ("vel", "velocidade"), ("rd", "rd")):
        r.ok(E[f"grupo.pj4.memo.{k}"] == memo[cm], f"Memoespírito de KV-12 {k}: {E[f'grupo.pj4.memo.{k}']} ≠ ficha {memo[cm]}")
    # (4) o Exemplo calculado (o arquivo entregue, sem entrada extra) × oráculo
    esp = O.calcular(E)
    nomes = [n for n in esp if n in mp["celulas"] and ":" not in mp["celulas"][n] and
             (n.startswith(("combate.", "encontros.A.", "grupo.pj", "campanha.")) or n == "encontros.orc")]
    got = _calc_arquivo(N.SAIDA_EXEMPLO, nomes)
    ruins = [n for n in nomes if not (TF._igual(got.get(n), esp[n]) or (esp[n] == "" and got.get(n) in ("", None)))]
    r.ok(not ruins, f"Exemplo × oráculo: {len(ruins)} diferença(s): {[(n, got.get(n), esp[n]) for n in ruins[:6]]}")
    r.checagens += len(nomes)
    r.ok((got["encontros.A.custo"], got["encontros.orc"]) == (320, 352) and
         str(got["encontros.A.dificuldade"]).startswith("Encontro típico") and got["encontros.A.contrato_n"] == 3 and
         got["encontros.A.contrato"] == "Cumprido", "encontro A: 320 de 352, típico, contrato cumprido com 3")
    r.ok(round(got["encontros.A.pct"]) == 91 if isinstance(got.get("encontros.A.pct"), (int, float)) else False,
         f"encontro A: {got.get('encontros.A.pct')}% (esperado 91%)")
    # a Fila do Ciclo 1 (o mesmo estado com Ciclo atual = 1) igual à do oráculo
    E1 = dict(E, **{"combate.ciclo": 1})
    esp1 = O.calcular(E1)
    fila = [f"combate.fila{k}.{c}" for k in range(1, TC.NC + 1) for c in ("nome", "vel", "situacao")]
    g1 = _calc_arquivo(N.SAIDA_EXEMPLO, fila, {"combate.ciclo": 1})
    r.ok(all(TF._igual(g1[n], esp1[n]) or (esp1[n] == "" and g1[n] in ("", None)) for n in fila),
         f"Fila do Ciclo 1 ≠ oráculo: {[(n, g1[n], esp1[n]) for n in fila if not TF._igual(g1[n], esp1[n])][:4]}")
    # (5) critério de aceitação do pedido (seção 5): Memoespírito ligado, invocado e na Fila pela VEL; 3 condições num
    # inimigo e 2 num aliado; o painel com tudo; a expirada fora da conta
    lab = exemplo.MEMO_LAB
    ordem = [got[f"combate.fila{k}.nome"] for k in range(1, TC.NC + 1) if got[f"combate.fila{k}.nome"]]
    r.ok(lab in ordem, f"aceitação 1–2: Memoespírito na Fila ({ordem})")
    # o estado digitado da Fila tem de ser alcançável no meio de um Ciclo (guia, seção 7): "Já agiu" nas casas antes
    # da que está "Agindo agora" e em nenhuma depois dela (revisão da Fase 4, achado N2)
    sit = [got[f"combate.fila{k}.situacao"] for k in range(1, len(ordem) + 1)]
    agora = [k for k, v in enumerate(sit, start=1) if v == "Agindo agora"]
    r.ok(len(agora) == 1 and all(v in ("Já agiu", "Surpreso: casa pulada") for v in sit[:agora[0] - 1]) and
         "Já agiu" not in sit[agora[0]:],
         f"N2: estado da Fila do Exemplo não é alcançável no meio de um Ciclo: {list(zip(ordem, sit))}")
    r.ok(got["grupo.pj4.memo.pv_ef"] == memo["pv"] and got["combate.memo4.nafila"] == "Sim" and
         got["combate.memo4.vel"] == memo["velocidade"], "aceitação 1–2: números do Memoespírito e Na Fila? = Sim")
    painel = [(got[f"combate.painel{k}.quem"], got[f"combate.painel{k}.cond"], got[f"combate.painel{k}.turnos"],
               got[f"combate.painel{k}.efeito"]) for k in range(1, 31) if got[f"combate.painel{k}.quem"]]
    sarg = [p for p in painel if p[0] == "Sargento de Trincheira"]
    nadir = [p for p in painel if p[0] == "Nadir"]
    r.ok(len({p[1] for p in sarg}) == 3 and len({p[1] for p in nadir}) == 2,
         f"aceitação 3: 3 condições no Sargento e 2 na Nadir no painel: {sarg} {nadir}")
    r.ok(all(p[3] and isinstance(p[2], (int, float)) for p in sarg + nadir),
         "aceitação 4: o painel mostra os turnos e o que cada condição faz")
    r.ok(not any(p[1] == "Sangramento" for p in sarg) and
         str(got[f"combate.c{slot(7, 4)}.efeito"]).startswith("EXPIRADA"),
         "aceitação 5: a condição com 0 turnos sai do painel e fica EXPIRADA na C7")
    r.ok(any(p[0] == lab for p in painel), "C1: o Memoespírito também recebe condição própria (painel)")
    r.ok(len(painel) == sum(1 for i, c, t, q in exemplo.CONDICOES_EXEMPLO if t != 0 and i != 8),
         f"C4: todas as condições ativas no painel ({len(painel)})")
    r.ok(MI0 + 4 == 20, "o Memoespírito de KV-12 é o combatente 20")
    # (6) nenhuma célula de erro no Exemplo entregue
    todas = TC.todas_formulas(N.SAIDA_EXEMPLO)
    sol = TC.modelo(N.SAIDA_EXEMPLO).calcular({}, todas)
    erros = [k for k, v in sol.items() if TF.eh_erro(v)]
    r.ok(not erros, f"Exemplo: {len(erros)} célula(s) com erro: {erros[:8]}")
    r.checagens += len(todas)
    r.info(f"Exemplo: {len(todas)} fórmulas recalculadas, {len(erros)} com erro; Fila do Ciclo 2: {', '.join(ordem)}")
    # (7) modelo em branco: geradores funcionando na semente padrão, iguais ao oráculo
    eb = O.calcular({})
    nomes_b = list(GERADORES_BRANCO.values()) + ["inicio.semente_ef"]
    gb = _calc_arquivo(N.SAIDA_MODELO, nomes_b)
    for g, n in GERADORES_BRANCO.items():
        r.ok(gb[n] not in ("", None) and TF._igual(gb[n], eb.get(n)), f"em branco, G = {g} ({n}): planilha {gb[n]!r}, "
                                                                     f"oráculo {eb.get(n)!r}")
    r.ok(gb["inicio.semente_ef"] == 12345, f"semente padrão do modelo em branco: {gb['inicio.semente_ef']}")
    r.info("modelo em branco: " + "; ".join(f"G={g}: {gb[n]}" for g, n in list(GERADORES_BRANCO.items())[:6]) + " …")
    return r


def suite_entregaveis(args):
    r = Resultado("entregaveis")
    for p in (N.SAIDA_MODELO, N.SAIDA_EXEMPLO, N.SAIDA_GUIA):
        r.ok(p.exists() and p.stat().st_size > 0, f"entregável ausente ou vazio: {p.name}")
        r.info(f"entregável: {p}")
    nomes = {N.SAIDA_MODELO.name, N.SAIDA_EXEMPLO.name, N.SAIDA_GUIA.name}
    for p in sorted(N.PASTA_MESTRE.iterdir()):
        if p.name in nomes:
            continue
        if p.name == REGISTRO_V11:
            r.info(f"registro antigo mantido (decisão do usuário, não apagado): {p.name}")
            continue
        if p.suffix.lower() == ".gsheet" or p.name.lower() == "desktop.ini":
            r.info(f"arquivo do usuário/Drive ignorado: {p.name}")
            continue
        r.falha(f"arquivo que não é entregável em Mestre\\: {p.name}")
    r.ok(not list(N.PASTA_MESTRE.glob("*.tmp.xlsx")), "temporário .tmp.xlsx esquecido em Mestre\\")
    return r


RE_CEL = re.compile(r"`([A-Za-zÀ-ú ]+)!([A-Z]{1,2}\d{1,4})` mostra \*\*([^*]+)\*\*")


def citacoes_guia():
    texto = N.SAIDA_GUIA.read_text(encoding="utf-8")
    saida = []
    for ln in texto.splitlines():
        for m in RE_CEL.finditer(ln):
            saida.append((m.group(1), m.group(2), m.group(3), "em branco" in ln))
    return texto, saida


def suite_guia(args):
    r = Resultado("guia")
    r.ok(N.SAIDA_GUIA.exists(), "COMO-USAR ausente")
    if not N.SAIDA_GUIA.exists():
        return r
    texto, cits = citacoes_guia()
    r.ok(len(cits) >= 12, f"o guia cita só {len(cits)} célula(s) com valor (checklist de 2 minutos)")
    inv = {v: k for k, v in TC.mapa()["celulas"].items()}
    for caminho, branco in ((N.SAIDA_EXEMPLO, False), (N.SAIDA_MODELO, True)):
        alvo = [(a, c, v) for a, c, v, b in cits if b == branco]
        if not alvo:
            continue
        refs = [f"'{a}'!{c}" for a, c, _ in alvo]
        sol = TC.modelo(caminho).calcular({}, refs)
        import openpyxl
        wb = openpyxl.load_workbook(caminho)
        for (a, c, v), ref in zip(alvo, refs):
            r.ok(a in N.ABAS, f"guia cita a aba {a!r}, que não existe")
            if a not in N.ABAS:
                continue
            obt = sol.get(ref) if ref in sol else wb[a][c].value
            if obt is None:
                obt = wb[a][c].value
            ok = TF._igual(obt, v) or str(obt).strip() == v.strip() or (
                isinstance(obt, (int, float)) and v.replace(",", ".").strip().lstrip("+").replace(" ", "")
                .rstrip("%") == f"{obt:g}")
            r.ok(ok, f"guia: `{a}!{c}` mostra {v!r}, mas a planilha ({'em branco' if branco else 'Exemplo'}) mostra "
                     f"{obt!r} ({inv.get(ref, 'sem nome lógico')})")
        r.info(f"{len(alvo)} citação(ões) conferida(s) no {'modelo em branco' if branco else 'Exemplo'}")
    for a in re.findall(r"aba \*\*([^*]+)\*\*", texto):
        r.ok(a in N.ABAS, f"guia fala da aba {a!r}, que não existe")
    r.ok("página 1 de 5" in texto or "5 páginas" in texto, "guia sem as 5 páginas do Escudo")
    r.ok("3 páginas" not in texto, "guia ainda fala em 3 páginas do Escudo")
    for h in [s["h"] for s in TC.mapa()["sugestoes"]]:
        r.ok(re.search(rf"\b{h}\b", texto) is not None, f"guia sem a sugestão {h} na lista de heurísticas")
    return r


def textos_guia():
    """Trechos do guia para a suíte texto (sem markdown, sem blocos de código nem endereços)."""
    if not N.SAIDA_GUIA.exists():
        return []
    itens, codigo = [], False
    for k, ln in enumerate(N.SAIDA_GUIA.read_text(encoding="utf-8").splitlines(), start=1):
        if ln.strip().startswith("```"):
            codigo = not codigo
            continue
        if codigo:
            continue
        s = re.sub(r"`[^`]*`", " ", ln)
        s = re.sub(r"\]\([^)]*\)", "]", s)
        s = re.sub(r"[*#>|\[\]_]", " ", s).strip()
        if s:
            itens.append((f"{N.SAIDA_GUIA.name}: linha {k}", s))
    return itens
