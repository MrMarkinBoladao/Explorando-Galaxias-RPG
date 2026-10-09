# -*- coding: utf-8 -*-
"""
oraculo_mestre_ger.py — o oráculo dos geradores da Fase 3: Mundos (G = 510…560), Improviso (G = 600…650 e a DT
rápida), Minhas Tabelas (G = 701…710) e os números do grupo agora no Escudo do Mestre (27.9, 23.6, 23.3).
Mesma convenção dos outros oráculos; as listas de sabor vêm do .xlsx gerado (oraculo_mestre_hist.lista), as tabelas do
livro estão transcritas abaixo com a seção, e build\\mestre_dados*.py / build\\mestre\\* não são importados.
"""
import oraculo_mestre as S
import oraculo_mestre_hist as OH
from oraculo_mestre_abas import num, tx
from oraculo_mestre_livro import RACAS
from oraculo_mestre_camp import eq, inteiro_ok, floor, dt_faixa, SUG

M = S.M
CAMINHOS = ["A Destruição", "A Inexistência", "A Harmonia", "A Abundância", "A Recordação", "A Erudição",
            "A Euforia", "A Caça", "A Preservação"]                                            # 06.3 (ordem da tabela)
ULTIMATE = {"1-4": (2, 27, 33), "5-8": (3, 39, 52), "9-12": (4, 63, 73), "13-16": (5, 105, 105),
            "17-20": (6, 147, 147)}                                                         # 27.9 (Nível eq., dano, cura)
FACES = (2, 4, 6, 8, 10, 12, 20, 100)
PROB = {"Quase impossível": -6, "Improvável": -3, "Meio a meio": 0, "Provável": 3, "Quase certo": 6}   # H10
EXEMPLOS_ARMA = {"Leve": "adaga, lâmina curta, chicote, par de garras",
                 "Média": "espada de uma mão, lança curta, bastão, machado de mão",
                 "Pesada": "martelo, montante, punhos reforçados, foice de haste longa",
                 "Disparo curto": "pistola, besta de mão, lançador de dardos",
                 "Disparo longo": "arco, rifle, fuzil de precisão",
                 "Energia": "canhão de palma, catalisador, drone de combate, núcleo ressonante"}     # 24.2
TIPOS_LOJA = ["Armas", "Armaduras", "Suprimentos", "Farmácia", "Mercado geral", "Mercado da Frota de Jade"]  # H15


def _loja():
    """H15: o estoque de cada tipo de loja, só com linhas de 24.1–24.3 e o preço do livro."""
    armas = [(f"Arma {c}", pr, f"{d}, {al}, {at}; ex.: {EXEMPLOS_ARMA[c]}") for c, d, al, at, _, pr in OH.ARMAS]
    armad = [(f"Armadura {t}", pr, f"Defesa +{d}" + ("" if o == "—" else f"; {o}")) for t, d, o, _, pr in OH.ARMADURAS]
    poc = [(f"Poção {n}", pr, f"Cura {c}") for n, c, _, pr in OH.POCOES]
    itens = [(n, pr, uso) for n, _, pr, uso in OH.ITENS]
    por = {x[0]: x for x in armas + armad + poc + itens}
    return {"Armas": armas + [por["Munição ou célula de reserva"]],
            "Armaduras": armad + [por[n] for n in ("Kit de ferramentas", "Traje de vedação",
                                                   "Munição ou célula de reserva")],
            "Suprimentos": itens,
            "Farmácia": poc + [por[n] for n in ("Kit de primeiros socorros (3 usos)", "Kit de pesquisa de campo",
                                                "Ração de viagem (3 dias)")],
            "Mercado geral": armas + armad + poc + itens, "Mercado da Frota de Jade": armas + armad + poc + itens}


LOJA = _loja()


def passo(n):
    """sorteio.passo: o primeiro de 7, 11, 13, 17, 19, 23 que não divide n (6.17)."""
    for p in (7, 11, 13, 17, 19):
        if n % p != 0:
            return p
    return 23


def seq(i0, k, n):
    return 0 if n <= 0 else (i0 - 1 + k * passo(n)) % n + 1


def item(lst, i):
    return lst[i - 1] if 1 <= i <= len(lst) else ""


def junta(a, b, sep=" "):
    return b if not a else a if not b else f"{a}{sep}{b}"


def vazia(id_, tit):
    return "" if OH.lista(id_) else f"Lista '{tit}' está vazia (aba Tabelas)"


def aviso_rolagem(rv):
    if rv is None or tx(rv) == "":
        return ""
    return "" if inteiro_ok(rv, 1, 1000000) else "Rolagem nº fora de 1 a 1.000.000: usando 1"


def _x(out, g, rol):
    sem = out["inicio.semente_ef"]
    return lambda c: S.valor(sem, g, rol, c)


def calcular(E, out):
    mundos(E, out)
    improviso(E, out)
    minhas(E, out)
    escudo(E, out)


# ---------------------------------------------------------------------------
# Mundos (6.13)
# ---------------------------------------------------------------------------

def mundos(E, out):
    so = OH.sorteia
    rs = {g: S.rolagem_efetiva(E.get(f"mundos.r{g}")) for g in (510, 520, 530, 540, 550, 560)}
    for g in rs:
        out[f"mundos.r{g}_ef"] = rs[g]
        out[f"mundos.aviso.r{g}"] = aviso_rolagem(E.get(f"mundos.r{g}"))
    x = _x(out, 510, rs[510])
    p = "mundos.planeta"
    out.update({f"{p}.nome": junta(so("lugar_a", x(8)), so("lugar_b", x(9))), f"{p}.tipo": so("mundo_tipo", x(1)),
                f"{p}.condicao": so("mundo_condicao", x(2)), f"{p}.caminho": CAMINHOS[(x(3) * 9) // M],
                f"{p}.manha": so("manha", x(4)), f"{p}.pararam": so("pararam", x(5)), f"{p}.presenca": so("ameaca", x(6)),
                f"{p}.faccao": so("faccoes", x(7)), f"{p}.presenca.origem": f"Tabelas (27.13, 27.14) · {SUG} (H11)",
                f"{p}.nome.aviso": vazia("lugar_a", "Nome de lugar (início)"),
                f"{p}.tipo.aviso": vazia("mundo_tipo", "Tipo de mundo"),
                f"{p}.presenca.aviso": vazia("ameaca", "Presença")})
    x = _x(out, 520, rs[520])
    p = "mundos.estacao"
    out.update({f"{p}.nome": junta(so("lugar_a", x(4)), so("lugar_b", x(5))), f"{p}.funcao": so("estacao_funcao", x(1)),
                f"{p}.dono": so("faccoes", x(2)), f"{p}.problema": so("estacao_problema", x(3))})
    x = _x(out, 530, rs[530])
    p = "mundos.nave"
    out.update({f"{p}.nome": junta(so("nave_a", x(1)), so("nave_b", x(2))), f"{p}.classe": so("nave_classe", x(3)),
                f"{p}.peculiaridade": so("nave_peculiaridade", x(4)),
                f"{p}.tripulacao": f"{S.inteiro(x(5), 1, 20)} pessoa(s); a bordo, um(a) {so('ocupacao', x(6))}",
                f"{p}.tripulacao.origem": f"Tabelas: Ocupação (NPC) · {SUG} (H25)"})
    x = _x(out, 540, rs[540])
    f_ = {"nome": junta(so("faccao_a", x(1)), so("faccao_b", x(2))), "caminho": CAMINHOS[(x(3) * 9) // M],
          "quer": so("faccao_quer", x(4)), "metodo": so("faccao_metodo", x(5)), "recurso": so("faccao_recurso", x(6)),
          "uso": so("faccao_uso", x(7))}
    out.update({f"mundos.faccao.{k}": v for k, v in f_.items()})
    out["mundos.saida.faccao"] = f_["nome"]
    out["mundos.saida.notas"] = ("" if not f_["nome"] else f"{f_['caminho']}; quer {f_['quer']}; método: {f_['metodo']}; "
                                                           f"recurso: {f_['recurso']}. Como usar: {f_['uso']}")
    x = _x(out, 550, rs[550])
    raca = RACAS[(x(2) * 7) // M]
    out.update({"mundos.org.nome": so("organizacao", x(1)),
                "mundos.org.lider": f"{OH.nome_cultura(raca, x(3), x(4))} ({raca})",
                "mundos.org.oferece": so("org_oferece", x(5)), "mundos.org.cobra": so("org_cobra", x(6)),
                "mundos.org.sede": junta(so("lugar_a", x(7)), so("lugar_b", x(8)))})
    _nomes(E, out, _x(out, 560, rs[560]))
    for nome, id_, tit in (("planeta.condicao", "mundo_condicao", "Condição marcante"),
                           ("planeta.manha", "manha", "O que fazem de manhã"),
                           ("planeta.pararam", "pararam", "O que pararam de fazer"),
                           ("planeta.faccao", "faccoes", "Facções"), ("estacao.nome", "lugar_b", "Nome de lugar (fim)"),
                           ("estacao.funcao", "estacao_funcao", "Função da estação"),
                           ("estacao.problema", "estacao_problema", "Problema da estação"),
                           ("nave.nome", "nave_a", "Nome de nave (início)"), ("nave.classe", "nave_classe",
                                                                              "Classe da nave"),
                           ("nave.peculiaridade", "nave_peculiaridade", "Peculiaridade da nave"),
                           ("faccao.nome", "faccao_a", "Nome de facção (início)"),
                           ("faccao.quer", "faccao_quer", "Facção: o que quer"),
                           ("faccao.metodo", "faccao_metodo", "Facção: método"),
                           ("faccao.recurso", "faccao_recurso", "Facção: recurso"),
                           ("faccao.uso", "faccao_uso", "Facção: como usar"),
                           ("org.nome", "organizacao", "Organização"),
                           ("org.oferece", "org_oferece", "Organização: o que oferece"),
                           ("org.cobra", "org_cobra", "Organização: o que cobra")):
        out[f"mundos.{nome}.aviso"] = vazia(id_, tit)


def _nomes(E, out, x):
    """G = 560: 10 nomes de uma cultura (escolhida ou sorteada) e 10 lugares, naves e organizações, sem repetir."""
    cu = tx(E.get("mundos.nomes.cultura"))
    ok = next((r for r in RACAS if eq(r, cu)), None)
    raca = ok or RACAS[(x(1) * 7) // M]
    out["mundos.nomes.cultura_ef"] = ("Escolhida: " if ok else "Sorteada: ") + (cu if ok else raca) + " (estilo de 05)"
    out["mundos.nomes.aviso"] = ("Cultura fora da lista do capítulo 05: sorteando" if cu and not eq(cu, "Sortear") and
                                 not ok else "")
    ln, ls = OH.lista(f"nome.{OH.SLUG[raca]}"), OH.lista(f"sobrenome.{OH.SLUG[raca]}")
    out["mundos.nomes.aviso.vazia"] = "" if ln or ls else f"Listas de nome da cultura {raca} vazias (aba Tabelas)"
    ordem, sep = OH.MONTAGEM[raca]
    seqs = {}
    for id_, c in (("lugar_a", 4), ("lugar_b", 5), ("nave_a", 6), ("nave_b", 7), ("organizacao", 8)):
        L_ = OH.lista(id_)
        seqs[id_] = (L_, S.escolha(x(c), len(L_)))
    i0n, i0s = S.escolha(x(2), len(ln)), S.escolha(x(3), len(ls))
    for j in range(10):
        nm, sb = item(ln, seq(i0n, j, len(ln))), item(ls, seq(i0s, j, len(ls)))
        out[f"mundos.nomes.{j + 1}.pessoa"] = (nm if not sb else sb if not nm else
                                               sb + sep + nm if ordem == 2 else nm + sep + sb)
        it = {k: item(L_, seq(i0, j, len(L_))) for k, (L_, i0) in seqs.items()}
        out[f"mundos.nomes.{j + 1}.lugar"] = junta(it["lugar_a"], it["lugar_b"])
        out[f"mundos.nomes.{j + 1}.nave"] = junta(it["nave_a"], it["nave_b"])
        out[f"mundos.nomes.{j + 1}.org"] = it["organizacao"]


# ---------------------------------------------------------------------------
# Improviso (6.14)
# ---------------------------------------------------------------------------

def improviso(E, out):
    so = OH.sorteia
    rs = {g: S.rolagem_efetiva(E.get(f"improviso.r{g}")) for g in (600, 610, 620, 630, 640, 650)}
    for g in rs:
        out[f"improviso.r{g}_ef"] = rs[g]
        out[f"improviso.aviso.r{g}"] = aviso_rolagem(E.get(f"improviso.r{g}"))
    x = _x(out, 600, rs[600])
    L_ = OH.lista("rumor")
    i0 = S.escolha(x(1), len(L_))
    for k in range(3):
        out[f"improviso.rumor.{k + 1}"] = item(L_, seq(i0, k, len(L_)))
        out[f"improviso.rumor.{k + 1}.verdade"] = so("veracidade", x(2 + k))
    out["improviso.rumor.aviso"] = vazia("rumor", "Rumor")
    out["improviso.rumor.aviso2"] = vazia("veracidade", "Veracidade do rumor")
    fx = out["campanha.faixa"]
    out["improviso.gancho.livro"] = so(f"ganchos_{fx.replace('-', '_')}", x(5))
    out["improviso.gancho.livro.origem"] = f"27.18, faixa {fx}"
    out["improviso.gancho.tabela"] = so("gancho", x(6))
    out["improviso.gancho.aviso"] = vazia("gancho", "Gancho de aventura")
    _eventos(E, out, _x(out, 610, rs[610]))
    _loja(E, out, _x(out, 620, rs[620]))
    x = _x(out, 630, rs[630])
    L_ = OH.lista("bugiganga")
    i0 = S.escolha(x(1), len(L_))
    for k in range(3):
        out[f"improviso.bug.{k + 1}"] = item(L_, seq(i0, k, len(L_)))
    out["improviso.bug.aviso"] = vazia("bugiganga", "Bugiganga")
    _oraculo(E, out, _x(out, 640, rs[640]))
    _rolador(E, out, _x(out, 650, rs[650]))
    dif, fx = E.get("improviso.dt.dificuldade"), tx(E.get("improviso.dt.faixa"))
    out["improviso.dt.valor"] = dt_faixa(dif, fx, out)
    from oraculo_mestre_camp import DT27
    from oraculo_mestre_livro import FAIXAS
    out["improviso.dt.aviso"] = ("Dificuldade fora da lista (27.2)" if tx(dif) and not any(eq(d, dif) for d in DT27) else
                                 "Faixa fora da lista: usando a do grupo" if fx and fx not in FAIXAS else "")


def _eventos(E, out, x):
    so = OH.sorteia
    on = tx(E.get("improviso.evento.onde"))
    ok = next((o for o in ("Viagem", "Espaço", "Cidade") if eq(o, on)), None)
    oe = on if ok else ["Viagem", "Espaço", "Cidade"][S.escolha(x(1), 3) - 1]
    out["improviso.evento.onde_ef"] = ("Escolhido: " if ok else "Sorteado: ") + oe
    out["improviso.evento.aviso.onde"] = ("Fora da lista: sorteando entre viagem, espaço e cidade" if on and
                                          not eq(on, "Sortear") and not ok else "")
    lid = "evento_viagem" if eq(oe, "Viagem") else "evento_espaco" if eq(oe, "Espaço") else "evento_cidade"
    ev = so(lid, x(2))
    out.update({"improviso.evento.evento": ev, "improviso.evento.evento.origem": f"Tabelas: Evento ({oe})",
                "improviso.evento.evento.aviso": "" if ev else "Lista de eventos vazia (aba Tabelas)",
                "improviso.evento.complicacao": so("complicacao", x(3)),
                "improviso.evento.complicacao.aviso": vazia("complicacao", "Complicação"),
                "improviso.evento.custo": so("custo_falha", x(4)),
                "improviso.evento.custo.aviso": vazia("custo_falha", "Falhe para frente: o custo")})


def _loja(E, out, x):
    so = OH.sorteia
    tl = tx(E.get("improviso.loja.tipo"))
    okl = next((t for t in TIPOS_LOJA if eq(t, tl)), None)
    te = okl or TIPOS_LOJA[S.escolha(x(1), 6) - 1]
    out["improviso.loja.tipo_ef"] = ("Escolhida: " if okl else "Sorteada: ") + (tl if okl else te)
    out["improviso.loja.aviso.tipo"] = ("Tipo de loja fora da lista: sorteando" if tl and not eq(tl, "Sortear") and
                                        not okl else "")
    pool = LOJA[te]
    i0 = S.escolha(x(2), len(pool))
    for k in range(6):
        nome, preco, oque = pool[seq(i0, k, len(pool)) - 1]
        out.update({f"improviso.loja.{k + 1}.item": nome, f"improviso.loja.{k + 1}.preco": preco,
                    f"improviso.loja.{k + 1}.oque": oque, f"improviso.loja.{k + 1}.qtd": S.inteiro(x(3 + k), 1, 3)})
    raca = RACAS[(x(9) * 7) // M]
    out["improviso.loja.lojista"] = f"{OH.nome_cultura(raca, x(10), x(11))} ({raca}): {so('maneirismo', x(12))}"
    out.update({"improviso.loja.raro": so("item_raro", x(13)),
                "improviso.loja.raro.oque": "Sem efeito no jogo até o Mestre decidir (27.9).",
                "improviso.loja.raro.preco": "O que o Mestre disser (24.5)",
                "improviso.loja.aviso.raro": vazia("item_raro", "Item fora do comum")})


def _oraculo(E, out, x):
    """H10: d20 + modificador da probabilidade; a resposta é a primeira faixa cujo teto não é menor que o total."""
    pr = tx(E.get("improviso.oraculo.prob"))
    okp = next((k for k in PROB if eq(k, pr)), None)
    mod = PROB[okp] if okp else 0
    out["improviso.oraculo.mod_txt"] = (("" if okp else "Vazio = Meio a meio. ") + "Modificador " +
                                        ("+" if mod > 0 else "") + str(mod))
    out["improviso.oraculo.aviso.prob"] = "Probabilidade fora da lista: usando Meio a meio" if pr and not okp else ""
    d20 = S.dado(x(1), 20)
    tot = d20 + mod
    resp = OH.lista("oraculo")
    limites = [b for _, b in OH.pares("oraculo") if b not in ("", None) and num(_n(b))]
    k = min(len(resp), 1 + sum(1 for b in limites if _n(b) < tot)) if resp else 0
    out["improviso.oraculo.rolagem"] = (f"{d20}" + ("" if mod == 0 else f" {'+' if mod > 0 else '−'} {abs(mod)}") +
                                        f" = {tot}")
    out["improviso.oraculo.resposta"] = item(resp, k)
    out["improviso.oraculo.aviso"] = vazia("oraculo", "Oráculo: resposta")
    out["improviso.g.oraculo.d20"], out["improviso.g.oraculo.total"] = d20, tot


def _n(v):
    """O teto da faixa do oráculo como a planilha o vê (número de verdade; o texto 'acima' não conta)."""
    try:
        return int(v) if str(v).lstrip("-").isdigit() else float(v)
    except (TypeError, ValueError):
        return None


def _rolador(E, out, x):
    for e in range(1, 4):
        p = f"improviso.rol.{e}"
        NN, FF, MM, VV = (E.get(f"{p}.{c}") for c in "nfmv")
        ne = min(20, max(1, floor(NN))) if num(NN) else 0
        fok = num(FF) and FF in FACES
        fe = int(FF) if fok else 20
        me = min(50, max(-50, floor(MM))) if num(MM) else 0
        va = (1 if eq(VV, "Vantagem") else -1 if eq(VV, "Desvantagem") else 0) if ne == 1 and fe == 20 else 0
        ds = [S.dado(x(20 * (e - 1) + d), fe) if d <= ne or (d == 2 and va) else "" for d in range(1, 21)]
        kept = (max(ds[0], ds[1]) if va == 1 else min(ds[0], ds[1]) if va == -1 else ds[0]) if ne else ""
        for d in range(1, 21):
            out[f"improviso.g.rol.{e}.d{d}"] = ds[d - 1]
        if ne == 0:
            out.update({f"{p}.dados": "", f"{p}.total": "", f"{p}.media": ""})
        else:
            out[f"{p}.dados"] = f"{ds[0]} e {ds[1]} (fica o {kept})" if va else ", ".join(str(d) for d in ds[:ne])
            out[f"{p}.total"] = (kept if va else sum(ds[:ne])) + me
            out[f"{p}.media"] = (ne * (fe + 1)) // 2 + me
        out[f"{p}.aviso"] = ("Nº de dados fora de 1 a 20: usando o limite" if num(NN) and not inteiro_ok(NN, 1, 20) else
                             "Preencha o nº de dados" if tx(NN) == "" and (tx(FF) + tx(MM) + tx(VV)) else
                             "Faces fora da lista: usando 20" if tx(FF) and not fok else
                             "Modificador fora de −50 a +50: usando o limite" if num(MM) and not inteiro_ok(MM, -50, 50)
                             else "Vantagem só vale para 1d20: rolando normal"
                             if (eq(VV, "Vantagem") or eq(VV, "Desvantagem")) and not va and ne > 0 else "")


# ---------------------------------------------------------------------------
# Minhas Tabelas (6.17) e o Escudo (os números do grupo agora)
# ---------------------------------------------------------------------------

def minhas(E, out):
    sem = out["inicio.semente_ef"]
    for t in range(1, 11):
        p = f"minhas.{t}"
        vals = [tx(E.get(f"{p}.vaga{k}")) for k in range(1, 101)]
        L_ = [v for v in vals if v != ""]
        n = len(L_)
        R_, Q = E.get(f"{p}.rolagem"), E.get(f"{p}.quantos")
        rol = S.rolagem_efetiva(R_)
        qe = min(5, max(1, floor(Q))) if num(Q) else 1
        x = S.valor(sem, 700 + t, rol, 1)
        i0 = S.escolha(x, n)
        res = [item(L_, seq(i0, k, n)) if k < qe else "" for k in range(5)]
        nome = tx(E.get(f"{p}.nome"))
        out.update({f"{p}.tamanho": n, f"{p}.rol_ef": rol, f"{p}.quantos_ef": qe, f"{p}.rotulo": nome or f"Tabela {t}",
                    **{f"{p}.res.{k + 1}": res[k] for k in range(5)}})
        out[f"{p}.resultado"] = "" if not res[0] else f"1. {res[0]}" + "".join(f" · {k + 1}. {res[k]}" for k in
                                                                                 range(1, 5) if res[k])
        av = aviso_rolagem(R_)
        out[f"{p}.aviso"] = (av if av else "Quantos fora de 1 a 5: usando o limite" if num(Q) and not inteiro_ok(Q, 1, 5)
                             else "Tabela vazia: preencha as vagas abaixo" if n <= 0 and (nome + tx(Q) + tx(R_)) else
                             f"A lista tem só {n} entrada(s): os resultados se repetem" if 0 < n < qe else
                             "Lista cheia (100)" if n >= 100 else "")


def escudo(E, out):
    nv, fx, ef = out["campanha.nivel_ef"], out["campanha.faixa"], out["campanha.ef"]
    niv, dano, cura = ULTIMATE[fx]
    out.update({"escudo.grupo.ult_nivel": niv, "escudo.grupo.ult_dano": dano, "escudo.grupo.ult_cura": cura,
                "escudo.grupo.descanso": 2 * nv + 2, "escudo.grupo.pv_temp": 3 * ef,
                "escudo.grupo.nivel.texto": f"Nível {nv}, faixa {fx}, Eficiência +{ef}",
                "escudo.grupo.ultimate.texto": f"Ultimate: Nível equivalente {niv}; dano médio {dano}, cura média {cura} "
                                               f"(27.9)",
                "escudo.grupo.descanso.texto": f"Descanso Curto: {2 * nv + 2} PV com Vigor +2 (23.6)",
                "escudo.grupo.pv_temp.texto": f"Teto de PV temporários: {3 * ef} (23.3)",
                "escudo.grupo.ph.texto": f"PH do grupo: máximo {out['campanha.ph_max']}, início {out['campanha.ph_ini']} "
                                         f"(16.2)"})
