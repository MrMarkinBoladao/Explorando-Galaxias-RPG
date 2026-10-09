# -*- coding: utf-8 -*-
"""
oraculo_mestre_camp.py — o oráculo das abas da Fase 3 ligadas à campanha: Campanha (marcos, facções, relógios, linha do
tempo, Ficha de Decisões, Sessão Zero), Grupo (G4, G5, G6 e o resumo), Sessões, Missões e o painel da Início.
Os geradores da Fase 3 (Mundos, Improviso, Minhas Tabelas) e o Escudo ficam em oraculo_mestre_ger.py.

Mesma convenção de oraculo_mestre_hist.py: entrada {nome lógico da entrada: valor}, saída {nome lógico: esperado};
nenhuma fórmula é lida e build\\mestre_dados*.py / build\\mestre\\* não são importados. As tabelas do livro estão
TRANSCRITAS abaixo com a seção. Comparação de texto como no Excel e no Google: "=" e COUNTIF não diferenciam maiúscula.
"""
import math
import re
import unicodedata

import oraculo_mestre as S
from oraculo_mestre_abas import num, tx
from oraculo_mestre_livro import FAIXAS

M = S.M
SUG = "Sugestão da planilha — não é regra do livro"
DT27 = {"Trivial": (8, 9, 10, 11, 12), "Fácil": (10, 12, 14, 16, 18), "Média": (13, 16, 19, 22, 25),
        "Difícil": (16, 19, 23, 27, 30), "Muito Difícil": (19, 23, 27, 31, 35), "Heroica": (22, 26, 31, 34, 38)}  # 27.2
RITMO = [(8, 4, "2 a 4 sessões por nível (níveis 1 a 8)"), (20, 6, "4 a 6 sessões por nível (do nível 9 em diante)")]
RESS = [(5, "I"), (10, "II"), (15, "III"), (20, "IV")]                                      # 26.7
REPUTACAO = {-3: "−3 Inimiga declarada", -2: "−2 Hostil", -1: "−1 Desconfiada", 0: "0 Neutra", 1: "+1 Simpática",
             2: "+2 Amiga", 3: "+3 Aliada"}                                                 # H17
SEGMENTOS = (4, 6, 8, 10, 12)                                                               # H16
ESTADOS = ["Oferecida", "Ativa", "Concluída", "Falhou", "Abandonada"]                       # 6.5


def eq(a, b):
    return tx(a).casefold() == tx(b).casefold()


def conta(vals, alvo):
    """COUNTIF(intervalo, texto): igualdade sem diferenciar maiúscula."""
    return sum(1 for v in vals if tx(v) != "" and eq(v, alvo))


def inteiro_ok(v, a, b):
    return num(v) and a <= v <= b and int(v) == v


def floor(v):
    return int(math.floor(v))


def slug(s):
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def dt_faixa(dif, fx, out):
    """DT da dificuldade na faixa do desafio (27.2 regra 1); faixa vazia ou fora da lista = a do grupo."""
    if tx(dif) == "":
        return ""
    fi = FAIXAS.index(fx) + 1 if fx in FAIXAS else out["campanha.faixa_idx"]
    lin = next((v for k, v in DT27.items() if eq(k, dif)), None)
    return lin[fi - 1] if lin else ""


def calcular(E, out):
    campanha(E, out)
    grupo(E, out)
    missoes(E, out)
    sessoes(E, out)
    inicio(E, out)


# ---------------------------------------------------------------------------
# Campanha (6.2)
# ---------------------------------------------------------------------------

def campanha(E, out):
    nv = out["campanha.nivel_ef"]
    mx, rt = (RITMO[0][1], RITMO[0][2]) if nv <= RITMO[0][0] else (RITMO[1][1], RITMO[1][2])
    out["campanha.ritmo"] = f"Ritmo sugerido: {rt} (26.1)."
    s = E.get("campanha.sessoes_nivel")
    out["campanha.aviso.ritmo"] = ("" if tx(s) == "" else "Sessões não é número" if not num(s) else
                                   "Sessões fora de 0 a 99" if not inteiro_ok(s, 0, 99) else
                                   f"Ritmo acima do sugerido (26.1): mais de {mx} sessões no nível" if s > mx else "")
    k = sum(1 for lv, _ in RESS if lv <= nv) + 1
    out["campanha.prox_ress"] = "Todas (nível 20)" if k > 4 else f"Ressonância {RESS[k - 1][1]} no nível {RESS[k - 1][0]}"
    dia = E.get("campanha.dia")
    out["campanha.dia_ef"] = max(1, floor(dia)) if num(dia) else 1
    _faccoes(E, out)
    _relogios(E, out)
    _linha_do_tempo(E, out)
    met, var = tx(E.get("campanha.metodo")), tx(E.get("campanha.variantes"))
    je, phm, phi = out["campanha.jogadores_ef"], out["campanha.ph_max"], out["campanha.ph_ini"]
    out["campanha.dec.mesa"] = (f"Método de atributos: {met or '(preencha na Mesa)'} · Tamanho da mesa: {je} jogadores → "
                                f"PH máximo {phm} / início {phi} (16.2) · Variantes em uso: {var or 'nenhuma anotada'}")
    out["campanha.sz.ph.texto"] = (f"Máximo de PH = 1 + número de personagens jogadores: com {je} jogadores, PH máximo "
                                   f"{phm} e início {phi} nesta faixa (16.2).")


def _faccoes(E, out):
    nomes = [tx(E.get(f"campanha.fac.{i}.nome")) for i in range(1, 13)]
    for i in range(1, 13):
        p = f"campanha.fac.{i}"
        at = E.get(f"{p}.atitude")
        lei = REPUTACAO.get(int(at), "") if num(at) and float(at).is_integer() else ""
        out[f"{p}.leitura"] = lei
        nm = nomes[i - 1]
        resto = tx(at) + tx(E.get(f"{p}.relogio")) + tx(E.get(f"{p}.notas")) + tx(E.get(f"{p}.ultimo"))
        out[f"{p}.aviso"] = (("Linha sem facção: preencha a facção" if resto else "") if not nm else
                             "Facção repetida: use uma linha por facção (H17)" if conta(nomes, nm) > 1 else
                             "Atitude fora de −3 a +3 (H17)" if tx(at) != "" and not lei else "")


def _relogios(E, out):
    falta = cheio = 0
    for i in range(1, 11):
        p = f"campanha.rel.{i}"
        s_, n_ = E.get(f"{p}.seg"), E.get(f"{p}.n")
        sok = 1 if num(s_) and s_ in SEGMENTOS else 0
        ne = 0 if tx(n_) == "" else n_
        ok = 1 if sok and num(ne) and ne >= 0 and int(ne) == ne and ne <= s_ else 0
        out.update({f"{p}.s_ok": sok, f"{p}.n_ef": ne, f"{p}.ok": ok})
        sit = ""
        if ok:
            n_i, s_i = int(ne), int(s_)
            out[f"{p}.barra"] = "●" * n_i + "○" * (s_i - n_i) + f" {n_i}/{s_i}"
            sit = "Cheio — aconteceu" if n_i == s_i else "Falta 1" if n_i == s_i - 1 else ""
        else:
            out[f"{p}.barra"] = ""
        out[f"{p}.situacao"] = sit
        falta += sit == "Falta 1"
        cheio += sit == "Cheio — aconteceu"
        nm = tx(E.get(f"{p}.nome"))
        out[f"{p}.aviso"] = ("" if not (nm + tx(s_) + tx(n_)) else
                             ("Escolha os segmentos: 4, 6, 8, 10 ou 12 (H16)" if tx(s_) == "" else
                              "Segmentos fora de 4, 6, 8, 10 ou 12 (H16)") if not sok else
                             "Preenchidos não é número (H16)" if not num(ne) else
                             f"Preenchidos fora de 0 a {tx(s_)} (H16)" if ne < 0 or int(ne) != ne else
                             "Preenchidos acima dos segmentos: confira (H16)" if ne > s_ else "")
    out["campanha.rel.resumo"] = (f"Relógios a 1 segmento de encher: {falta} · cheios: {cheio}. O livro pede relógio na "
                                  f"ficção para o Descanso Longo (27.7): a nave parte ao amanhecer, o lacre não aguenta "
                                  f"mais um dia.")
    out["campanha._falta1"] = falta


def _linha_do_tempo(E, out):
    hoje = out["campanha.dia_ef"]
    chaves = {}
    for i in range(1, 31):
        d = E.get(f"campanha.tl.{i}.dia")
        if inteiro_ok(d, 1, 9999):
            chaves[i] = d + i / 100
    for i in range(1, 31):
        p = f"campanha.tl.{i}"
        k_ = chaves.get(i)
        out[f"{p}.chave"] = k_ if k_ is not None else ""
        out[f"{p}.ordem"] = sum(1 for v in chaves.values() if v < k_) + 1 if k_ is not None else ""
        out[f"{p}.fut"] = k_ if k_ is not None and floor(k_) >= hoje else ""
        resto = "".join(tx(E.get(f"{p}.{c}")) for c in ("evento", "quem", "consequencia", "sessao"))
        out[f"{p}.aviso"] = (("Sem dia: o evento fica fora da ordem" if resto else "") if tx(E.get(f"{p}.dia")) == ""
                             else "" if k_ is not None else "Dia fora de 1 a 9.999 (inteiro)")
    futs = sorted((v, i) for i, v in chaves.items() if floor(v) >= hoje)
    nf = len(futs)
    out["campanha.prox.resumo"] = (f"A partir do dia {hoje} (Dia de campanha, na Mesa). " +
                                   ("Nenhum evento agendado de hoje em diante." if nf == 0 else
                                    f"{nf} evento(s) de hoje em diante."))
    campos = (("eventos", "evento"), ("quem", "quem"), ("consequencias", "consequencia"), ("publicos", "publico"))
    for k in range(1, 6):
        p = f"campanha.prox.{k}"
        if k > nf:
            out.update({f"{p}.{c}": "" for c in ("chave", "idx", "dias", "faltam", "sessoes", "eventos", "quem",
                                                  "consequencias", "publicos")})
            continue
        v, i = futs[k - 1]
        q = lambda c: E.get(f"campanha.tl.{i}.{c}")  # noqa: E731
        # idx = posição no intervalo da linha do tempo, que inclui o cabeçalho repetido a cada 10 linhas
        out.update({f"{p}.chave": v, f"{p}.idx": i + (i - 1) // 10, f"{p}.dias": q("dia"),
                    f"{p}.faltam": q("dia") - hoje,
                    f"{p}.sessoes": "" if q("sessao") is None else q("sessao"),
                    **{f"{p}.{c}": tx(q(o)) for c, o in campos}})


# ---------------------------------------------------------------------------
# Grupo: G4 (Tier), G5, G6 e o resumo
# ---------------------------------------------------------------------------

TR6 = ["tr_pot", "tr_ref", "tr_rfis", "tr_rmen", "tr_pm", "tr_fv", "per_perc", "per_int", "per_furt"]
PER6 = ["per_pesq", "per_cien", "per_sint", "per_pers"]


def grupo(E, out):
    nv, fi = out["campanha.nivel_ef"], out["campanha.faixa_idx"]
    te = 1 if nv <= 6 else 2 if nv <= 12 else 3 if nv <= 17 else 4                       # 25.3
    nomes = [tx(E.get(f"grupo.pj{i}.nome")) for i in range(1, 7)]
    pms, melhores = [], []
    for i in range(1, 7):
        g = lambda c: E.get(f"grupo.pj{i}.{c}")  # noqa: E731
        rot = nomes[i - 1] or f"PJ {i}"
        out[f"grupo.pj{i}.rotulo5"], out[f"grupo.pj{i}.rotulo6"] = rot, rot
        co, ti = g("cone"), g("tier")
        out[f"grupo.pj{i}.aviso4"] = ("Cone abaixo do esperado: encontros ficam mais duros (27.8)" if num(co) and co < fi
                                      else "Tier abaixo do esperado: encontros ficam mais duros (27.8)"
                                      if num(ti) and ti < te else
                                      "Tier acima do Tier do nível do grupo (25.1, 25.3)" if num(ti) and ti > te else "")
        fora = lambda cs: any(num(g(c)) and (g(c) < -5 or g(c) > 40) for c in cs)  # noqa: E731
        out[f"grupo.pj{i}.aviso5"] = "Total fora de −5 a +40: confira na ficha" if fora(TR6) else ""
        out[f"grupo.pj{i}.aviso6"] = "Total fora de −5 a +40: confira na ficha" if fora(PER6) else ""
        pms.append(g("tr_pm") if num(g("tr_pm")) else None)
        fr = [g(c) for c in PER6[:3] if num(g(c))]
        out[f"grupo.pj{i}.melhor_fraq"] = max(fr) if fr else ""
        melhores.append(max(fr) if fr else None)
    vals = [v for v in pms if v is not None]
    if not vals:
        out["grupo.surpresa"] = "Preencha a Percepção Mental na G5."
    else:
        mn = min(vals)
        out["grupo.surpresa"] = (f"Menor Percepção Mental do grupo: {tx(mn)} ({nomes[pms.index(mn)]}). Surpresa: Teste de "
                                 f"Percepção Mental contra DT 13, fixa em todas as faixas (19.3, 27.3).")
    vals = [v for v in melhores if v is not None]
    if not vals:
        out["grupo.fraqueza"] = "Preencha Pesquisa, Ciência ou Sintonia na G6."
    else:
        mx = max(vals)
        intel = conta([E.get(f"grupo.pj{i}.raca") for i in range(1, 7)], "Intellitron") > 0
        out["grupo.fraqueza"] = (f"Melhor total de Pesquisa, Ciência ou Sintonia: {tx(mx)} ({nomes[melhores.index(mx)]}), "
                                 f"contra DT {out['campanha.dt_fraqueza']} na faixa do grupo (20.2)" +
                                 ("; o Intellitron rola com Vantagem e descobre duas por sucesso (20.2)." if intel
                                  else "."))


# ---------------------------------------------------------------------------
# Sessões e Missões (6.4, 6.5)
# ---------------------------------------------------------------------------

def sessoes(E, out):
    ses = E.get("campanha.sessao")
    out["sessoes.prep.atual"] = f"Sessão atual na Mesa: {tx(ses) if num(ses) else '(vazia)'}."
    n_ = E.get("sessoes.prep.n")
    out["sessoes.aviso.prep"] = ("Sessão preparada anterior à sessão atual da Mesa" if num(n_) and num(ses) and n_ < ses
                                 else "")
    tipos, encs = [], []
    for k in range(1, 6):
        p = f"sessoes.cena.{k}"
        dif, fx, en = E.get(f"{p}.dificuldade"), tx(E.get(f"{p}.faixa")), tx(E.get(f"{p}.encontro"))
        tipos.append(E.get(f"{p}.tipo"))
        encs.append(en)
        out[f"{p}.dt"] = dt_faixa(dif, fx, out)
        out[f"{p}.aviso"] = ("Dificuldade fora da lista (27.2)" if tx(dif) and not any(eq(d, dif) for d in DT27) else
                             "Faixa fora da lista: usando a do grupo" if fx and fx not in FAIXAS else
                             "Encontro fora da lista (A, B ou C)" if en and not any(eq(en, x) for x in
                                                                                     ("Nenhum", "A", "B", "C")) else "")
        X = next((x for x in "ABC" if eq(en, x)), None)
        if X:
            nm = tx(E.get(f"encontros.{X}.nome"))
            out[f"{p}.encontro_txt"] = ((f"{nm}: " if nm else f"Encontro {X}: ") +
                                        f"custo {tx(out[f'encontros.{X}.custo'])} · "
                                        f"{tx(out[f'encontros.{X}.dificuldade'])}")
            out[f"{p}.contrato"] = out[f"encontros.{X}.contrato"]
        else:
            out[f"{p}.encontro_txt"], out[f"{p}.contrato"] = "", ""
    pistas = [tx(E.get(f"sessoes.pista.{k}.texto")) for k in range(1, 11)]
    rev = conta([E.get(f"sessoes.pista.{k}.revelada") for k in range(1, 11)], "Sim")
    out["sessoes.pistas.resumo"] = f"Pistas: {sum(1 for p in pistas if p)} · reveladas: {rev}"
    for i in range(1, 7):
        nm, pr = tx(E.get(f"grupo.pj{i}.nome")), tx(E.get(f"grupo.pj{i}.proposito"))
        out[f"sessoes.gancho.{i}.pj"] = nm or f"PJ {i}"
        out[f"sessoes.gancho.{i}.proposito"] = pr
        out[f"sessoes.gancho.{i}.aviso"] = (f"PJ {i} sem nome na aba Grupo" if tx(E.get(f"sessoes.gancho.{i}.texto")) and
                                            not nm else "")
    _checklist(E, out, tipos, encs)
    _diario(E, out)


def _checklist(E, out, tipos, encs):
    out["sessoes.check.orcamento.auto"] = f"Orçamento da faixa para o grupo: {out['encontros.orc']} PV (aba Encontros)."
    partes = "".join(f"{X}: {out[f'encontros.{X}.contrato']}. " for X in "ABC" if conta(encs, X) > 0)
    nenhum = sum(conta(encs, X) for X in "ABC") == 0
    out["sessoes.check.contrato.auto"] = partes + ("Nenhum encontro ligado às cenas." if nenhum else "")
    out["sessoes.check.relogio.auto"] = f"Relógios a 1 de encher: {out['campanha._falta1']} (aba Campanha)."
    nc = E.get("sessoes.check.combates.n")
    ef = nc if num(nc) else conta(tipos, "Combate")
    out["sessoes.check.combates.ef"] = ef
    out["sessoes.check.combates.auto"] = ("Nenhum combate previsto" if ef <= 0 else
                                          f"{tx(ef)} combate(s): " + ("dia tranquilo" if ef <= 2 else
                                                                      "dia de verdade" if ef == 3 else
                                                                      "emergência, e o grupo deve sentir que é") +
                                          " (27.7)")
    out["sessoes.check.combates.aviso"] = ("Combates fora de 0 a 9" if num(nc) and not inteiro_ok(nc, 0, 9) else
                                           "Quatro combates ou mais no dia é emergência (27.7)" if ef >= 4 else "")
    nv = out["campanha.nivel_ef"]
    out["sessoes.check.equipamento.auto"] = (f"Nível {nv}: faixa nova (Cone e Tier)" if nv in (1, 5, 9, 13, 17) else
                                             f"Nível {nv}: Tier novo" if nv in (7, 18) else f"Nível {nv}: sem virada")


def _diario(E, out):
    cont = desde = 0
    for i in range(1, 31):
        p = f"sessoes.diario.{i}"
        mc = E.get(f"{p}.marco")
        tem = "".join(tx(E.get(f"{p}.{c}")) for c in ("n", "resumo", "data", "dia", "marco"))
        cont += 1 if tem else 0
        desde = 0 if eq(mc, "Sim") else desde + (1 if eq(mc, "Não") else 0)
        out.update({f"{p}.cont": cont, f"{p}.desde": desde})
        nn = E.get(f"{p}.n")
        out[f"{p}.rot2"] = f"Sessão {tx(nn)}" if num(nn) else f"Linha {i}"
        out[f"{p}.aviso"] = "Marco: escolha Sim ou Não" if tx(mc) and not (eq(mc, "Sim") or eq(mc, "Não")) else ""
    out["sessoes.diario.resumo"] = (f"Sessões registradas: {cont} · sessões desde o último marco: {desde} (conta os Não "
                                    f"desde o último Sim). Ritmo sugerido: veja Marcos e progressão na aba Campanha "
                                    f"(26.1).")


def missoes(E, out):
    est = [E.get(f"missoes.{i}.estado") for i in range(1, 21)]
    marcos = 0
    for i in range(1, 21):
        p = f"missoes.{i}"
        es, mi = tx(est[i - 1]), tx(E.get(f"{p}.missao"))
        out[f"{p}.aviso"] = ("Estado fora da lista" if es and not any(eq(es, x) for x in ESTADOS) else
                             "Linha sem o nome da missão" if not mi and (es + tx(E.get(f"{p}.objetivo"))) else "")
        out[f"{p}.rot2"] = mi or f"Missão {i}"
        ini, fim = E.get(f"{p}.inicio"), E.get(f"{p}.fim")
        out[f"{p}.aviso2"] = ("Concluída sem sessão de fim" if eq(es, "Concluída") and tx(fim) == "" else
                              "Sessão de fim antes da de início" if num(ini) and num(fim) and fim < ini else "")
        marcos += 1 if eq(es, "Concluída") and eq(E.get(f"{p}.marco"), "Sim") else 0
    for e in ESTADOS:
        out[f"missoes.n.{slug(e)}"] = conta(est, e)
    out["missoes.n.total"] = sum(out[f"missoes.n.{slug(e)}"] for e in ESTADOS)
    out["missoes.n.marcos"] = marcos
    out["campanha.marcos"] = marcos
    out["missoes.aviso.ativas"] = ("Mais de 3 missões Ativas: o grupo pode perder o fio — Sugestão da planilha (H23)"
                                   if out["missoes.n.ativa"] > 3 else "")


def inicio(E, out):
    nm = tx(E.get("campanha.nome"))
    ses = E.get("campanha.sessao")
    out["inicio.painel.campanha"] = nm or "(sem nome: aba Campanha)"
    out["inicio.painel.sessao"] = f"{tx(ses) if num(ses) else '(vazia)'} · dia de campanha {out['campanha.dia_ef']}"
    out["inicio.painel.nivel"] = (f"Nível {out['campanha.nivel_ef']}, faixa {out['campanha.faixa']} · Eficiência "
                                  f"+{out['campanha.ef']}")
    out["inicio.painel.ph"] = (f"Máximo {out['campanha.ph_max']} · início do combate {out['campanha.ph_ini']} "
                               f"({out['campanha.jogadores_ef']} jogadores)")
    out["inicio.painel.missoes"] = (f"{out['missoes.n.ativa']} ativa(s) · {out['missoes.n.oferecida']} oferecida(s) · "
                                    f"{out['missoes.n.concluida']} concluída(s)")
    out["inicio.painel.relogios"] = out["campanha._falta1"]
    out["inicio.painel.ressonancia"] = out["campanha.prox_ress"]
    s = E.get("campanha.sessoes_nivel")
    out["inicio.painel.ritmo"] = ((f"{tx(s)} " + ("sessão" if s == 1 else "sessões") + " no nível · ") if num(s)
                                  else "") + out["campanha.ritmo"]
    ti, n_ = tx(E.get("sessoes.prep.titulo")), E.get("sessoes.prep.n")
    out["inicio.painel.proxima"] = ((f"Sessão {tx(n_)}: " if num(n_) else "") + ti) if ti else "(nenhuma: aba Sessões)"
