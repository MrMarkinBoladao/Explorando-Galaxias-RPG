# -*- coding: utf-8 -*-
"""
Exemplo (design §14) — parte da Fase 1: Campanha (Mesa, semente 2026), Grupo (4 PJs com os números de
build\\oraculo_ficha.calcular: a Nadir é a de 29.7), Inimigos da campanha (Carcereiro Orbital e Capataz do Duto 4),
Encontros A e B e o estado de Combate do Ciclo 2. As outras partes chegam na Fase 4.
"""
import copy
import json

N_ENTRADAS = 0


def _pj(nome, aceitos=(), **mud):
    import testar_ficha as TF
    import oraculo_ficha as O
    e = TF._nadir(**mud)
    s = O.calcular(e)
    # ESQUIVA_PROIBIDA com Armadura Pesada é a própria regra (24.1), não erro do PJ: aceito só onde é pedido
    if [a for a in s["avisos"] if a not in aceitos]:
        raise ValueError(f"Exemplo: o oráculo da ficha avisou para {nome}: {s['avisos']}")
    b = s["bonus"]
    pj = {"nome": nome, "raca": e["raca"], "caminho": e["caminho"], "elemento": e["elemento"],
          "pv": s["pv_max"], "def": s["defesa"], "esq": s["esquiva"] if s["esquiva"] is not None else None, "rd": s["rd"],
          "vel": s["velocidade"], "ag": b["Agilidade"], "disc": b["Discernimento"], "pres": b["Presença"], "dt": s["dt"],
          "cone": 1, "tier": 1}
    # Fase 3 (G5 e G6): os totais que a ficha mostra para os 6 Testes de Resistência e as Perícias de mesa
    from mestre.aba_campanha import TR6, PER6
    for c, t in TR6 + PER6:
        pj[c] = s["testes_resistencia"][t]["total"] if t in s["testes_resistencia"] else s["pericias"][t]["total"]
    return pj


def grupo():
    """Os 4 PJs do Exemplo (design §14), calculados pelo oráculo da ficha (sem aviso: senão é fatal)."""
    nadir = _pj("Nadir")
    tess = _pj("Tessaly Varonne", raca="Vulpes", caminho="A Caça", elemento="Vento",
               atributos={"Agilidade": 15, "Discernimento": 14, "Poder": 13, "Presença": 12, "Vigor": 10,
                          "Sincronia": 8},
               atributo_habilidade="Agilidade", arma={"categoria": "Disparo longo", "propriedade": "Nenhuma"},
               armadura="Leve", bencaos=[], pericias_escolhidas=["Pilotagem", "Investigação"],
               bonus_racial={"modo": "+2 em um", "attr1": "Discernimento"})
    shen = _pj("Shen Wanqing", aceitos=("ESQUIVA_PROIBIDA",), raca="Xianzhouíta", caminho="A Preservação", elemento="Gelo",
               atributos={"Vigor": 15, "Poder": 14, "Discernimento": 13, "Presença": 12, "Agilidade": 10,
                          "Sincronia": 8},
               atributo_habilidade="Vigor", armadura="Pesada", bencaos=[], pericias_escolhidas=["Mecânica",
                                                                                                 "Sobrevivência"],
               bonus_racial={"modo": "+2 em um", "attr1": "Vigor"})
    # Fase 4: KV-12 é da Recordação e tem um Memoespírito (o Exemplo mostra o pedido do usuário funcionando)
    kv = _pj("KV-12, Paciência", raca="Intellitron", caminho="A Recordação", elemento="Quântico",
             atributos={"Discernimento": 15, "Sincronia": 14, "Vigor": 13, "Agilidade": 12, "Presença": 10,
                        "Poder": 8},
             atributo_habilidade="Sincronia", arma={"categoria": "Energia", "propriedade": "Nenhuma"},
             bencaos=[], pericias_escolhidas=["Tecnologia", "Mecânica"],
             bonus_racial={"modo": "+2 em um", "attr1": "Sincronia"}, memoespirito=MEMO_KV)
    return [nadir, tess, shen, kv]


# o Memoespírito de KV-12 (11.3): 12 pontos, Guardião, Velocidade Espiritual; os números vêm de oraculo_ficha (11.4)
MEMO_KV = {"pontos": {"Sincronia": 4, "Agilidade": 4, "Vigor": 4}, "atributo_ataque": "Sincronia", "funcao": "Guardião",
           "bonus_menores": ["Velocidade Espiritual", "Memória Afiada", "Vínculo Profundo"], "evolucoes": []}
NOME_MEMO = "Eco do Construtor"


def memo_kv():
    """Os números do Memoespírito de KV-12 pela ficha (oraculo_ficha.calcular, 11.4)."""
    import testar_ficha as TF
    import oraculo_ficha as O
    e = TF._nadir(raca="Intellitron", caminho="A Recordação", elemento="Quântico",
                  atributos={"Discernimento": 15, "Sincronia": 14, "Vigor": 13, "Agilidade": 12, "Presença": 10,
                             "Poder": 8},
                  atributo_habilidade="Sincronia", arma={"categoria": "Energia", "propriedade": "Nenhuma"},
                  bencaos=[], pericias_escolhidas=["Tecnologia", "Mecânica"],
                  bonus_racial={"modo": "+2 em um", "attr1": "Sincronia"}, memoespirito=MEMO_KV)
    return O.calcular(e)["memo"]


def entradas_nomes():
    """{nome lógico: valor} do Exemplo (Fase 1)."""
    d = {"campanha.nome": "O Lacre do Poço Sete", "campanha.jogadores": 4, "campanha.nivel": 1,
         "campanha.sessao": 2, "campanha.dia": 3, "campanha.metodo": "Array oficial", "inicio.semente": 2026}
    jog = ["Ana", "Bruno", "Carla", "Davi"]
    for i, pj in enumerate(grupo(), start=1):
        for k, v in pj.items():
            if v is not None:
                d[f"grupo.pj{i}.{k}"] = v
        d[f"grupo.pj{i}.jogador"] = jog[i - 1]
    d.update({
        "inimigos.1.nome": "Carcereiro Orbital", "inimigos.1.modo": "Faixa do livro", "inimigos.1.faixa": "9-12",
        "inimigos.1.tipo": "Elite", "inimigos.1.f1": "Fogo", "inimigos.1.f2": "Vento", "inimigos.1.f3": "Físico",
        "inimigos.1.faccao": "Outra", "inimigos.1.elemento": "Raio", "inimigos.1.racional": "Sim",
        "inimigos.1.comportamento": "Vai em quem está mais longe do grupo.",
        "inimigos.acao1.inimigo": "Carcereiro Orbital", "inimigos.acao1.tipo": "Ataque normal",
        "inimigos.acao1.nome": "Cassetete de choque", "inimigos.acao1.alcance": "Pessoal",
        "inimigos.acao1.elemento": "Raio",
        "inimigos.acao2.inimigo": "Carcereiro Orbital", "inimigos.acao2.tipo": "Ataque normal",
        "inimigos.acao2.nome": "Lançador de rede", "inimigos.acao2.alcance": "Média",
        "inimigos.acao2.elemento": "Físico",
        "inimigos.acao3.inimigo": "Carcereiro Orbital", "inimigos.acao3.tipo": "Especial de controle",
        "inimigos.acao3.nome": "Trancafiar", "inimigos.acao3.recarga": 2, "inimigos.acao3.duracao": 2,
        "inimigos.acao3.condicao": "Lentidão", "inimigos.acao3.tr": "Reflexos",
        "inimigos.2.nome": "Capataz do Duto 4", "inimigos.2.modo": "Ajustar do bestiário",
        "inimigos.2.base": "Capataz Oco", "inimigos.2.faixa": "5-8",
        "inimigos.ver": "Carcereiro Orbital", "bestiario.ver": "O Afogado do Poço Sete",
        "encontros.A.nome": "Emboscada no duto 4", "encontros.A.ambiente": "Colônia ou mina abandonada",
        "encontros.A.1.criatura": "Sargento de Trincheira", "encontros.A.1.qtd": 1,
        "encontros.A.2.criatura": "Larva Fuliginosa", "encontros.A.2.qtd": 2,
        "encontros.A.3.criatura": "Casco Oco", "encontros.A.3.qtd": 2,
        "encontros.B.nome": "O fundo do poço", "encontros.B.ambiente": "Colônia ou mina abandonada",
        "encontros.B.1.criatura": "O Afogado do Poço Sete", "encontros.B.1.qtd": 1,
        "encontros.B.2.criatura": "Casco Oco", "encontros.B.2.qtd": 1,
        "combate.ciclo": 2, "combate.carregar": "A", "combate.ph": 4,
        # C8/C9 (19.3; guia, seção 7: "Já agiu?" = Sim é marcado na ordem da Fila e a marca passa para o próximo).
        # Meio do Ciclo 2: já agiram as casas 1 a 4 — Tessaly (f2), o Memoespírito de KV-12 (f20), KV-12 (f4) e a
        # Nadir (f1) —, então "Agindo agora" cai na casa 5, o Sargento de Trincheira: é a vez do mestre, com as três
        # condições do Sargento à vista no painel C9b.
        "combate.f2.ja": "Sim", "combate.f20.ja": "Sim", "combate.f4.ja": "Sim", "combate.f1.ja": "Sim",
        "combate.in2.pv": 0, "combate.in1.reducao": 3,
        "combate.pj1.energia": 50, "combate.pj2.energia": 40, "combate.pj3.energia": 30, "combate.pj4.energia": 40,
    })
    d.update(_memo_e_condicoes())
    d.update(_fase2(d))
    d.update(_fase3())
    return d


MEMO_LAB = f"{NOME_MEMO} (de KV-12, Paciência)"
# Combate do Exemplo (Fase 4): condições acumuladas na C7 — combatente (índice da tabela de estado), condição, turnos,
# quem aplicou. 1–4 os PJs, 7 o Sargento, 9 a Larva 2, 10 o Casco Oco 1, 20 o Memoespírito de KV-12.
CONDICOES_EXEMPLO = [
    (7, "Queimadura", 2, "Nadir"), (7, "Marcado", 2, "Tessaly Varonne"), (7, "Vulnerável", 1, MEMO_LAB),
    (7, "Sangramento", 0, "Shen Wanqing"),                                  # expirada (C6): sai do painel
    (10, "Congelado", 1, "Shen Wanqing"),
    (1, "Lentidão", 1, "Sargento de Trincheira"), (1, "Marcado", 2, "Larva Fuliginosa 2"),
    (20, "Marcado", 1, "Sargento de Trincheira")]


def _memo_e_condicoes():
    """O Memoespírito de KV-12 ligado na aba Grupo (G7), invocado no Combate (C2b) e as condições da C7."""
    from mestre.aba_combate_base import slot
    m = memo_kv()
    d = {"grupo.pj4.memo.tem": "Sim", "grupo.pj4.memo.nome": NOME_MEMO, "grupo.pj4.memo.pv": m["pv"],
         "grupo.pj4.memo.def": m["defesa"], "grupo.pj4.memo.vel": m["velocidade"], "grupo.pj4.memo.rd": m["rd"],
         "grupo.pj4.memo.agi": MEMO_KV["pontos"]["Agilidade"], "grupo.pj4.memo.disc": 0,
         "grupo.pj4.memo.vigor": MEMO_KV["pontos"]["Vigor"],
         "combate.memo4.invocado": "Sim", "combate.memo4.pv": m["pv"] - 5}
    usados = {}
    for i, cond, t, quem in CONDICOES_EXEMPLO:
        usados[i] = usados.get(i, 0) + 1
        n = slot(i, usados[i])
        d.update({f"combate.c{n}.cond": cond, f"combate.c{n}.turnos": t, f"combate.c{n}.quem": quem})
    return d


def _fase3():
    """Fase 3 (design §14): facções, relógios, linha do tempo, Ficha de Decisões, Sessão Zero, 3 missões, a sessão 2
    preparada com 1 linha de diário, a tabela "Clima no Expresso" (12 entradas) e os testes dos PJs (G5 e G6)."""
    d = {"campanha.sessoes_nivel": 1}
    for i, (fac, at, rel, nota, ult) in enumerate([
            ("Legião da Antimatéria", -2, "A Legião cumpre o ultimato", "Mandou ultimato de três dias pelo lacre", 2),
            ("Corporação da Paz Interastral", 0, "A Corporação manda a apólice", "Quer o lacre segurado em nome dela", 2),
            ("Aliança Xianzhou", 1, "", "Shen Wanqing ainda tem amigos na Frota de Jade", 1)], start=1):
        d.update({f"campanha.fac.{i}.nome": fac, f"campanha.fac.{i}.atitude": at, f"campanha.fac.{i}.notas": nota,
                  f"campanha.fac.{i}.ultimo": ult})
        if rel:
            d[f"campanha.fac.{i}.relogio"] = rel
    for i, (nome, s, n, enc) in enumerate([
            ("A Legião cumpre o ultimato", 6, 2, "O Pretor marcha sobre a colônia"),
            ("O lacre cede", 8, 3, "O Afogado do Poço Sete sobe pelos dutos"),
            ("A Corporação manda a apólice", 4, 1, "A Auditora chega com a apólice e uma escolta")], start=1):
        d.update({f"campanha.rel.{i}.nome": nome, f"campanha.rel.{i}.seg": s, f"campanha.rel.{i}.n": n,
                  f"campanha.rel.{i}.ao_encher": enc})
    for i, (dia, ses, ev, quem, cons, pub) in enumerate([
            (1, 1, "O grupo desce do Expresso Astral na colônia do Poço Sete", "Grupo",
             "Os mineiros pedem ajuda no duto 2", "Sim"),
            (2, 1, "Os mineiros presos no duto 2 voltam para casa", "Grupo", "A colônia confia no grupo", "Sim"),
            (3, 2, "A Legião entrega o ultimato: três dias para entregar o lacre", "Legião da Antimatéria",
             "Eles avisam e cumprem o prazo (27.16)", "Sim"),
            (4, None, "A Corporação oferece a apólice do lacre", "Corporação da Paz Interastral",
             "A apólice exige que o grupo entregue alguém", "Não"),
            (6, None, "Vence o prazo do ultimato da Legião", "Legião da Antimatéria",
             "O Pretor marcha sobre a colônia se o lacre não for entregue", "Sim"),
            (8, None, "O lacre do Poço Sete cede se ninguém o fechar", "Fragmentum", "O Afogado sobe pelos dutos",
             "Não")], start=1):
        d.update({f"campanha.tl.{i}.dia": dia, f"campanha.tl.{i}.evento": ev, f"campanha.tl.{i}.quem": quem,
                  f"campanha.tl.{i}.consequencia": cons, f"campanha.tl.{i}.publico": pub})
        if ses:
            d[f"campanha.tl.{i}.sessao"] = ses
    # as três linhas de exemplo de 27.11, com os PJs do Exemplo
    d.update({"campanha.dec.hab.1.quem": "Nadir", "campanha.dec.hab.1.nome": "Corte Duplo",
              "campanha.dec.hab.1.ajuste": "pedia dois ataques; aprovada como um ataque com +1 dado",
              "campanha.dec.hab.1.porque": "dois ataques dobrariam a geração de PH",
              "campanha.dec.item.1": "Arma 'estilhaço de jade' de Shen Wanqing aceita como Média arremessável, Elemento "
                                     "Gelo.",
              "campanha.dec.regra.1": "Decidido: a Barreira da Preservação cobre Dano Contínuo no turno em que é "
                                      "aplicada. Vale para todo mundo.",
              "campanha.dec.nome.1.nome": "Conselho da colônia", "campanha.dec.nome.1.tipo": "Facção",
              "campanha.dec.nome.1.notas": "Os cinco mais velhos do Poço Sete; decidem por voto."})
    from mestre.aba_campanha3 import SESSAO_ZERO
    for chave, *_ in SESSAO_ZERO:
        d[f"campanha.sz.{chave}.feito"] = "Sim"
    d.update({"campanha.sz.comb.tom": "Aventura com horror educado; o perigo mora no dia, não no combate.",
              "campanha.sz.comb.temas": "Memória, dívida e o que se deve a quem ficou para trás.",
              "campanha.sz.comb.linhas": "Nada de tortura em cena.",
              "campanha.sz.comb.veus": "A morte de civis acontece fora de cena.",
              "campanha.sz.comb.expectativas": "Sessões quinzenais de três horas, metade combate, metade história."})
    for i, (mi, tp, co, ob, lo, pr, es, rc, mc, ini, fim) in enumerate([
            ("Fechar o lacre do Poço Sete", "Contenção de Fragmentum", "Conselho da colônia do Poço Sete",
             "descer ao fundo do poço e fechar o lacre", "Poço Sete", "o lacre não aguenta mais um dia", "Ativa",
             "200 Cr de verba de marco e o nível 2", "Sim", 2, None),
            ("Apólice da Corporação", "Negociação", "Auditora de Risco da Corporação da Paz Interastral",
             "assinar a apólice ou recusar sem briga", "Vértice-9", "a apólice vence em dois dias", "Oferecida",
             "um ano de seguro pago para o grupo", "Não", 2, None),
            ("Tirar os mineiros do duto 2", "Resgate", "Os mineiros da colônia",
             "trazer de volta a equipe presa no duto 2", "Poço Sete", "o ar do duto acaba ao amanhecer", "Concluída",
             "um favor da colônia", "Não", 1, 1)], start=1):
        d.update({f"missoes.{i}.missao": mi, f"missoes.{i}.tipo": tp, f"missoes.{i}.contratante": co,
                  f"missoes.{i}.objetivo": ob, f"missoes.{i}.local": lo, f"missoes.{i}.prazo": pr,
                  f"missoes.{i}.estado": es, f"missoes.{i}.recompensa": rc, f"missoes.{i}.marco": mc,
                  f"missoes.{i}.inicio": ini})
        if fim:
            d[f"missoes.{i}.fim"] = fim
    d.update({"sessoes.prep.n": 2, "sessoes.prep.data": "sábado", "sessoes.prep.titulo": "O fundo do poço",
              "sessoes.prep.objetivo": "Fechar o lacre antes que o prazo da Legião vença."})
    for k, (tp, desc, npcs, enc, dif, fx) in enumerate([
            ("Social", "O conselho da colônia discute o ultimato da Legião", "Conselho da colônia", "Nenhum", "Média",
             None),
            ("Exploração", "Descer pelos dutos alagados até o nível 3", "", "Nenhum", "Difícil", "1-4"),
            ("Combate", "Emboscada no duto 4", "", "A", None, None),
            ("Social", "A Auditora aparece com a apólice", "Auditora de Risco", "Nenhum", "Média", None),
            ("Combate", "O fundo do poço", "", "B", None, None)], start=1):
        d.update({f"sessoes.cena.{k}.tipo": tp, f"sessoes.cena.{k}.descricao": desc, f"sessoes.cena.{k}.encontro": enc})
        if npcs:
            d[f"sessoes.cena.{k}.npcs"] = npcs
        if dif:
            d[f"sessoes.cena.{k}.dificuldade"] = dif
        if fx:
            d[f"sessoes.cena.{k}.faixa"] = fx
    for k, (p, rv) in enumerate([("O lacre foi aberto por dentro", "Sim"),
                                  ("Quem abriu usava o uniforme do grupo", "Sim"),
                                  ("A Corporação já sabia do lacre antes do acidente", "Não"),
                                  ("O Afogado ainda usa o crachá de um mineiro", "Não"),
                                  ("O Pretor quer o lacre fechado, não aberto", "Não"),
                                  ("Há um segundo lacre no nível 5", "Não")], start=1):
        d.update({f"sessoes.pista.{k}.texto": p, f"sessoes.pista.{k}.revelada": rv})
    d.update({"sessoes.recompensas": "Verba de marco do nível 2 (200 Cr) se o lacre fechar; 1 Poção Pequena achada "
                                     "no duto.",
              "sessoes.gancho.1.texto": "A doca que expulsou Nadir é a dona da apólice.",
              "sessoes.check.orcamento.feito": "Sim", "sessoes.check.contrato.feito": "Sim",
              "sessoes.check.relogio.feito": "Sim", "sessoes.check.equipamento.feito": "Não",
              "sessoes.diario.1.n": 1, "sessoes.diario.1.data": "sábado passado", "sessoes.diario.1.dia": 2,
              "sessoes.diario.1.marco": "Não",
              "sessoes.diario.1.resumo": "O grupo chegou ao Poço Sete e tirou os mineiros do duto 2.",
              "sessoes.diario.1.decisoes": "Aceitaram ajudar a colônia de graça.",
              "sessoes.diario.1.ganchos": "Quem abriu o lacre usava o uniforme do grupo.",
              "sessoes.diario.1.npcs": "Conselho da colônia"})
    clima = ["Silêncio de vagão de carga", "Música baixa no vagão-refeitório", "Discussão sobre a rota na cabine",
             "Cheiro de café queimado no corredor", "Luzes piscando por uma tempestade estelar",
             "Um passageiro novo que ninguém viu embarcar", "Frio no vagão-oficina", "Festa improvisada nos dormitórios",
             "O trem para por uma hora sem explicação", "Uma janela mostra um mundo que não está no mapa",
             "Conserto barulhento no vagão de carga lacrado", "Noite calma: todo mundo dorme"]
    d.update({"minhas.1.nome": "Clima no Expresso", "minhas.1.quantos": 3, "minhas.1.rolagem": 1})
    for k, v in enumerate(clima, start=1):
        d[f"minhas.1.vaga{k}"] = v
    # os testes dos PJs (G5 e G6) vêm de grupo() (oráculo da ficha); aqui só os traços que o Mestre lembra
    d["grupo.pj4.passivas"] = "Chassi: Vantagem em Tecnologia e Mecânica; imune a doença natural (05)."
    d["grupo.pj3.passivas"] = "Ad Vitam Aeternam: não pode ser Executada; Vantagem em todo Teste de Resistência (05)."
    return d


# Fase 2 (design §14): 6 NPCs no Elenco (saídas do gerador nas Rolagens 1–6, copiadas como valores, com uma nota
# editada à mão), 4 cartões, a entrega de marco do nível 2 e 2 linhas de Tesouro.
_NPCS = None


def npcs_do_gerador(base, rolagens=range(1, 7)):
    """As linhas de saída do gerador de NPCs (G = 200) nas Rolagens dadas, como o Mestre as copiaria. Os valores vêm do
    oráculo independente (build\\oraculo_mestre_hist.py), que a suíte oraculo confere contra a própria planilha."""
    import oraculo_mestre_abas as OA
    import oraculo_mestre_hist as OH
    saida = []
    for r in rolagens:
        E = dict(base, **{"npcs.rolagem": r})
        out = {}
        OA.campanha(E, out)
        OH.npcs(E, out)
        saida.append({k[len("npcs.saida."):]: v for k, v in out.items() if k.startswith("npcs.saida.")})
    return saida


def _fase2(base):
    global _NPCS
    if _NPCS is None:
        _NPCS = npcs_do_gerador(base)
    d = {"npcs.rolagem": 6}
    extra = [("Poço Sete, na cantina da colônia", 1, "Sim", 1, "Conheceu o grupo no duto 2 e deve um favor a Nadir."),
             ("Doca de carga do Poço Sete", 0, "Sim", 1, ""), ("Vértice-9", -1, "Sim", 2, ""),
             ("Expresso Astral, vagão-refeitório", 2, "Sim", 2, ""), ("Poço Sete, nível 3", 0, "Sim", 2, ""),
             ("Desconhecido", -2, "Sim", 2, "")]
    for i, npc in enumerate(_NPCS, start=1):
        for k, v in npc.items():
            d[f"npcs.elenco.{i}.{k}"] = v
        onde, rel, vivo, ses, nota = extra[i - 1]
        d.update({f"npcs.elenco.{i}.onde": onde, f"npcs.elenco.{i}.relacao": rel, f"npcs.elenco.{i}.vivo": vivo,
                  f"npcs.elenco.{i}.sessao": ses})
        if nota:
            d[f"npcs.elenco.{i}.notas"] = nota
    for c in range(1, 5):
        d[f"npcs.cartao{c}.npc"] = _NPCS[c - 1]["nome"]
    d.update({"recompensas.nivel": 2, "recompensas.marco": "Subiu de nível",
              "recompensas.tes.1.sessao": 1, "recompensas.tes.1.item": "Créditos (verba de marco do nível 2)",
              "recompensas.tes.1.qtd": 1, "recompensas.tes.1.cr": 200, "recompensas.tes.1.quem": "Grupo",
              "recompensas.tes.1.notas": "24.5: 200 Cr por nível ganho na faixa 1-4",
              "recompensas.tes.2.sessao": 1, "recompensas.tes.2.item": "Poção Pequena", "recompensas.tes.2.qtd": 1,
              "recompensas.tes.2.quem": "Shen Wanqing",
              "recompensas.tes.2.notas": "Achada no duto 2; preço de referência 50 Cr (24.3)"})
    return d


def preencher(wb):
    global N_ENTRADAS
    from mestre import nucleo as N
    wb2 = wb                     # o modelo já foi gravado: o Exemplo preenche o mesmo workbook (deepcopy quebra as fontes)
    d = entradas_nomes()
    for nome, v in d.items():
        aba, cel = N.REFS[nome]
        wb2[aba][cel].value = N.valor_digitado(nome, v)     # faixa "9-12" → "Faixa 9-12" (opção da lista)
    N_ENTRADAS = len(d)
    return wb2
