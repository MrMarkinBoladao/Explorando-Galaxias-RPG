# -*- coding: utf-8 -*-
"""
Aba Mundos (R8; design §6.13): planeta ou local (G = 510, as três perguntas de 27.17), estação (520), nave (530), facção
nova (540, com a linha de saída para Facções da aba Campanha), organização (550), nomes avulsos (560: 10 pessoas de uma
cultura, lugares, naves e organizações, sem repetir) e, para consulta, as 8 facções (27.16) e os 6 locais (27.17) do
livro. Todo sorteio passa por mestre\\sorteio.py (semente da Início + Rolagem nº de cada gerador).
"""

import mestre_sabor_nomes as NM
from mestre import nucleo as N
from mestre import sorteio as S
from mestre import historia as H
from mestre.nucleo import T, q, ent, cal, av, rot, cabs, titulo, dcol, sugestao, sugestao_formula

GERADORES = [(510, "Planeta ou local"), (520, "Estação"), (530, "Nave"), (540, "Facção nova"), (550, "Organização"),
             (560, "Nomes avulsos")]
NOMES_AVULSOS = 10
M = "2147483647"


def rolagens(ws, r0, geradores, prefixo, explica):
    """Bloco "Rolagem nº" (uma por gerador): entrada, efetiva e aviso. Devolve a próxima linha livre."""
    titulo(ws, r0, "Rolagem nº de cada gerador (vazio = 1; some 1 para rolar de novo; a semente é a da aba Início)")
    cabs(ws, r0 + 1, {"A": "Gerador", "B": "Rolagem nº (preencha)", "C": "Rolagem efetiva", "D": ("Como funciona", "J"),
                      "K": ("Aviso", "L")})
    for k, (g, nome) in enumerate(geradores):
        r = r0 + 2 + k
        rot(ws, f"A{r}", f"{nome} (G = {g})", negrito=True)
        ent(ws, f"B{r}", f"{prefixo}.r{g}", tipo="inteiro", minimo=1, maximo=1000000, rotulo="Rolagem nº", centro=True,
            amostra=2)
        cal(ws, f"C{r}", S.rolagem_efetiva(T(f"{prefixo}.r{g}")), nome=f"{prefixo}.r{g}_ef", centro=True)
        rot(ws, f"D{r}", explica if k == 0 else "Mesma semente e mesma Rolagem nº dão o mesmo resultado.", ate="J",
            italico=True)
        av(ws, f"K{r}", f"{prefixo}.aviso.r{g}", S.aviso_rolagem(T(f"{prefixo}.r{g}")), ate="L")
    N.subtabela(ws, f"{prefixo}.rolagens", [r0 + 1], "A:L", len(geradores))
    return r0 + 2 + len(geradores)


def junta(a, b, sep=" "):
    """a + sep + b, sem o separador quando um dos dois está vazio."""
    return f'IF(LEN({a})=0,{b},IF(LEN({b})=0,{a},{a}&"{sep}"&{b}))'


def linha(ws, r, rotulo, formula, nome, origem=None, aviso=None, negrito=False):
    rot(ws, f"A{r}", rotulo, negrito=True)
    cal(ws, f"B{r}", formula, nome=nome, ate="H", negrito=negrito)
    if origem is not None:
        cal(ws, f"I{r}", origem, nome=f"{nome}.origem", ate="J")
    if aviso is not None:
        av(ws, f"K{r}", f"{nome}.aviso", aviso, ate="L")


def vazia(id_, tit):
    return f'=IF({H.n(id_)}<=0,"Lista \'{tit}\' está vazia (aba Tabelas)","")'


def cabecalho(ws, r, tit, g, h=None):
    titulo(ws, r, f"{tit} (G = {g})", ate="J" if h else "L")
    if h:
        sugestao(ws, f"K{r}", h, f"mundos.g{g}.{h.lower()}", ate="L")
    cabs(ws, r + 1, {"A": "Campo", "B": ("Sorteado (automático)", "H"), "I": ("De onde vem", "J"), "K": ("Aviso", "L")})


def montar(wb):
    ws = wb["Mundos"]
    r = rolagens(ws, 5, GERADORES, "mundos", "Um gerador não lê o outro: rolar um não muda os demais (design §5).")
    g = lambda nome: T(f"mundos.g.{nome}")  # noqa: E731
    a = lambda rr, f, nome: N.aux(ws, f"N{rr}", f, nome=f"mundos.g.{nome}")  # noqa: E731
    xs = {}
    lin_aux = 10
    for gid, nome in GERADORES:
        params = {560: ["cultura", "listas tab.* de nomes"]}.get(gid, ["listas tab.* do gerador"])
        xs[gid] = H.campos(ws, gid, f"mundos.r{gid}_ef", lin_aux, "AA", params)
        lin_aux += len(N.MAPA.geradores[str(gid)]["campos"]) + 1
    r += 1
    # --- Planeta ou local (510) --------------------------------------------------------------------------------
    x = xs[510]
    cabecalho(ws, r, "Planeta ou local", 510)
    rr = r + 2
    cam = dcol("caminhos", "Caminho")
    linha(ws, rr, "Nome", "=" + junta(H.sorteia("lugar_a", x[8]), H.sorteia("lugar_b", x[9])), "mundos.planeta.nome",
          '="Tabelas: Nome de lugar (início + fim)"', vazia("lugar_a", "Nome de lugar (início)"), negrito=True)
    linha(ws, rr + 1, "Tipo", "=" + H.sorteia("mundo_tipo", x[1]), "mundos.planeta.tipo", '="Tabelas: Tipo de mundo"',
          vazia("mundo_tipo", "Tipo de mundo"))
    linha(ws, rr + 2, "Condição marcante", "=" + H.sorteia("mundo_condicao", x[2]), "mundos.planeta.condicao",
          '="Tabelas: Condição marcante"', vazia("mundo_condicao", "Condição marcante"))
    linha(ws, rr + 3, "Qual Caminho está vencendo aqui?", f"=INDEX({cam},INT({x[3]}*9/{M})+1)", "mundos.planeta.caminho",
          '="Os 9 Caminhos (06.3), pergunta 1 de 27.17"')
    linha(ws, rr + 4, "O que fazem de manhã?", "=" + H.sorteia("manha", x[4]), "mundos.planeta.manha",
          '="Tabelas, pergunta 2 de 27.17"', vazia("manha", "O que fazem de manhã"))
    linha(ws, rr + 5, "O que pararam de fazer?", "=" + H.sorteia("pararam", x[5]), "mundos.planeta.pararam",
          '="Tabelas, pergunta 3 de 27.17"', vazia("pararam", "O que pararam de fazer"))
    linha(ws, rr + 6, "Presença", "=" + H.sorteia("ameaca", x[6]), "mundos.planeta.presenca",
          f'="Tabelas (27.13, 27.14) · {N.ROTULO_SUGESTAO} (H11)"', vazia("ameaca", "Presença"))
    sugestao_formula("mundos.planeta.presenca.origem", "H11", [f"B{rr + 6}"])
    linha(ws, rr + 7, "Facção presente", "=" + H.sorteia("faccoes", x[7]), "mundos.planeta.faccao",
          '="Tabelas: Facções (27.16)"', vazia("faccoes", "Facções"))
    cal(ws, f"A{rr + 8}", "=" + N.dtexto("perguntas") + '&" (27.17)"',
        nome="mundos.planeta.perguntas", ate="L")
    N.subtabela(ws, "mundos.planeta", [r + 1], "A:L", 8)
    r = rr + 10
    # --- Estação (520) -----------------------------------------------------------------------------------------
    x = xs[520]
    cabecalho(ws, r, "Estação", 520)
    rr = r + 2
    linha(ws, rr, "Nome", "=" + junta(H.sorteia("lugar_a", x[4]), H.sorteia("lugar_b", x[5])), "mundos.estacao.nome",
          '="Tabelas: Nome de lugar (início + fim)"', vazia("lugar_b", "Nome de lugar (fim)"), negrito=True)
    linha(ws, rr + 1, "Função", "=" + H.sorteia("estacao_funcao", x[1]), "mundos.estacao.funcao",
          '="Tabelas: Função da estação (a primeira é a de Vértice-9, 27.17)"', vazia("estacao_funcao", "Função da estação"))
    linha(ws, rr + 2, "Dono", "=" + H.sorteia("faccoes", x[2]), "mundos.estacao.dono", '="Tabelas: Facções (27.16)"')
    linha(ws, rr + 3, "Problema atual", "=" + H.sorteia("estacao_problema", x[3]), "mundos.estacao.problema",
          '="Tabelas: Problema da estação"', vazia("estacao_problema", "Problema da estação"))
    N.subtabela(ws, "mundos.estacao", [r + 1], "A:L", 4)
    r = rr + 5
    # --- Nave (530) --------------------------------------------------------------------------------------------
    x = xs[530]
    cabecalho(ws, r, "Nave", 530, "H25")
    rr = r + 2
    linha(ws, rr, "Nome", "=" + junta(H.sorteia("nave_a", x[1]), H.sorteia("nave_b", x[2])), "mundos.nave.nome",
          '="Tabelas: Nome de nave (início + fim)"', vazia("nave_a", "Nome de nave (início)"), negrito=True)
    linha(ws, rr + 1, "Classe", "=" + H.sorteia("nave_classe", x[3]), "mundos.nave.classe", '="Tabelas: Classe da nave"',
          vazia("nave_classe", "Classe da nave"))
    linha(ws, rr + 2, "Peculiaridade", "=" + H.sorteia("nave_peculiaridade", x[4]), "mundos.nave.peculiaridade",
          '="Tabelas: Peculiaridade da nave"', vazia("nave_peculiaridade", "Peculiaridade da nave"))
    oc = H.sorteia("ocupacao", x[6])
    linha(ws, rr + 3, "Tripulação", f'={S.inteiro(x[5], 1, 20)}&" pessoa(s); a bordo, um(a) "&{oc}',
          "mundos.nave.tripulacao", f'="Tabelas: Ocupação (NPC) · {N.ROTULO_SUGESTAO} (H25)"')
    sugestao_formula("mundos.nave.tripulacao.origem", "H25", [f"B{rr + 3}"])
    cal(ws, f"A{rr + 4}", "=" + N.dtexto("viagem") + '&" "&' +
        N.dtexto("viagem_cena"), nome="mundos.nave.lembrete", ate="L")
    N.subtabela(ws, "mundos.nave", [r + 1], "A:L", 4)
    r = rr + 6
    # --- Facção nova (540) -------------------------------------------------------------------------------------
    x = xs[540]
    cabecalho(ws, r, "Facção nova: um Caminho levado a sério (27.16)", 540)
    rr = r + 2
    linha(ws, rr, "Nome", "=" + junta(H.sorteia("faccao_a", x[1]), H.sorteia("faccao_b", x[2])), "mundos.faccao.nome",
          '="Tabelas: Nome de facção (início + fim)"', vazia("faccao_a", "Nome de facção (início)"), negrito=True)
    linha(ws, rr + 1, "Caminho levado a sério", f"=INDEX({cam},INT({x[3]}*9/{M})+1)", "mundos.faccao.caminho",
          '="Os 9 Caminhos (06.3; 27.16)"')
    linha(ws, rr + 2, "O que quer", "=" + H.sorteia("faccao_quer", x[4]), "mundos.faccao.quer",
          '="Tabelas: Facção, o que quer"', vazia("faccao_quer", "Facção: o que quer"))
    linha(ws, rr + 3, "Método", "=" + H.sorteia("faccao_metodo", x[5]), "mundos.faccao.metodo",
          '="Tabelas: Facção, método"', vazia("faccao_metodo", "Facção: método"))
    linha(ws, rr + 4, "Recurso", "=" + H.sorteia("faccao_recurso", x[6]), "mundos.faccao.recurso",
          '="Tabelas: Facção, recurso"', vazia("faccao_recurso", "Facção: recurso"))
    linha(ws, rr + 5, "Como usar", "=" + H.sorteia("faccao_uso", x[7]), "mundos.faccao.uso",
          '="Tabelas: Facção, como usar (no tom de 27.16)"', vazia("faccao_uso", "Facção: como usar"))
    N.subtabela(ws, "mundos.faccao", [r + 1], "A:L", 6)
    rr += 7
    titulo(ws, rr, "Linha de saída: cole como valores numa linha livre de Facções (aba Campanha): A em A e G:I em G:I")
    cabs(ws, rr + 1, {"A": "Facção", "B": "Atitude", "C": ("Leitura", "D"), "E": ("Relógio ligado", "F"),
                      "G": ("Notas", "I"), "J": "Último contato"})
    cal(ws, f"A{rr + 2}", f'={T("mundos.faccao.nome")}', nome="mundos.saida.faccao")
    cal(ws, f"G{rr + 2}", f'=IF(LEN({T("mundos.faccao.nome")})=0,"",{T("mundos.faccao.caminho")}&"; quer "&'
                          f'{T("mundos.faccao.quer")}&"; método: "&{T("mundos.faccao.metodo")}&"; recurso: "&'
                          f'{T("mundos.faccao.recurso")}&". Como usar: "&{T("mundos.faccao.uso")})',
        nome="mundos.saida.notas", ate="I")
    rot(ws, f"A{rr + 3}", "As colunas estão na ordem de Facções (D6). Não cole por cima da Leitura (C:D): ela é "
                          "calculada pela atitude que você escolher.", ate="L", italico=True)
    r = rr + 5
    # --- Organização (550) -------------------------------------------------------------------------------------
    x = xs[550]
    cabecalho(ws, r, "Organização", 550)
    rr = r + 2
    rac = dcol("racas", "Raça")
    a(rr, f"=INDEX({rac},INT({x[2]}*7/{M})+1)", "org.raca")
    a(rr + 1, "=" + H.ridx(g("org.raca")), "org.ri")
    nm, sb = H.nome_cultura(g("org.ri"), x[3], x[4])
    a(rr + 2, "=" + nm, "org.nome")
    a(rr + 3, "=" + sb, "org.sob")
    linha(ws, rr, "Nome", "=" + H.sorteia("organizacao", x[1]), "mundos.org.nome", '="Tabelas: Organização"',
          vazia("organizacao", "Organização"), negrito=True)
    linha(ws, rr + 1, "Quem manda", f'={H.montar_nome(g("org.ri"), g("org.nome"), g("org.sob"))}&" ("&{g("org.raca")}'
                                    f'&")"', "mundos.org.lider", '="Tabelas: nome da cultura da Raça sorteada (05)"')
    linha(ws, rr + 2, "O que oferece", "=" + H.sorteia("org_oferece", x[5]), "mundos.org.oferece",
          '="Tabelas: Organização, o que oferece"', vazia("org_oferece", "Organização: o que oferece"))
    linha(ws, rr + 3, "O que cobra", "=" + H.sorteia("org_cobra", x[6]), "mundos.org.cobra",
          '="Tabelas: Organização, o que cobra"', vazia("org_cobra", "Organização: o que cobra"))
    linha(ws, rr + 4, "Sede", "=" + junta(H.sorteia("lugar_a", x[7]), H.sorteia("lugar_b", x[8])), "mundos.org.sede",
          '="Tabelas: Nome de lugar (início + fim)"')
    N.subtabela(ws, "mundos.org", [r + 1], "A:L", 5)
    r = rr + 6
    # --- Nomes avulsos (560) -----------------------------------------------------------------------------------
    r = _nomes(ws, r, xs[560], a, g)
    r = _consulta(ws, r + 1)


def _sequencia(ws, a, g, rr, id_, x, nome):
    """Aux: n, passo e i₀ da sequência sem repetição na lista tab.<id> (6.17); devolve (n, passo, i₀)."""
    a(rr, f"={H.n(id_)}", f"{nome}.n")
    a(rr + 1, "=" + S.passo(g(f"{nome}.n")), f"{nome}.passo")
    a(rr + 2, "=" + S.escolha(x, g(f"{nome}.n")), f"{nome}.i0")
    return g(f"{nome}.n"), g(f"{nome}.passo"), g(f"{nome}.i0")


def _nomes(ws, r, x, a, g):
    titulo(ws, r, f"Nomes avulsos (G = 560): {NOMES_AVULSOS} de cada, sem repetir", ate="J")
    sugestao(ws, f"K{r}", "H25", "mundos.g560.h25", ate="L")
    rot(ws, f"A{r + 1}", "Cultura", negrito=True)
    ent(ws, f"B{r + 1}", "mundos.nomes.cultura", tipo="lista", fonte="lista.racas_sortear", ate="C", rotulo="Cultura")
    CU = T("mundos.nomes.cultura")
    rac = dcol("racas", "Raça")
    base = r + 1
    a(base, f'=IF(COUNTIF({rac},{CU})>0,{CU},INDEX({rac},INT({x[1]}*7/{M})+1))', "nomes.raca")
    a(base + 1, "=" + H.ridx(g("nomes.raca")), "nomes.ri")
    cal(ws, f"D{r + 1}", f'=IF(COUNTIF({rac},{CU})>0,"Escolhida: ","Sorteada: ")&{g("nomes.raca")}&" (estilo de 05)"',
        nome="mundos.nomes.cultura_ef", ate="J")
    av(ws, f"K{r + 1}", "mundos.nomes.aviso",
       f'=IF(AND(LEN({CU})>0,{CU}<>"Sortear",COUNTIF({rac},{CU})=0),"Cultura fora da lista do capítulo 05: sorteando",'
       f'"")', ate="L")
    RI = g("nomes.ri")
    # n, passo e i₀ por cultura (nome e sobrenome) e das listas de lugar, nave e organização
    rr = base + 2
    nn = H.escolher(RI, [H.n(f"nome.{NM.SLUG[c]}") for c in NM.CULTURAS])
    ns = H.escolher(RI, [H.n(f"sobrenome.{NM.SLUG[c]}") for c in NM.CULTURAS])
    a(rr, "=" + nn, "nomes.nn")
    a(rr + 1, "=" + S.passo(g("nomes.nn")), "nomes.pn")
    a(rr + 2, "=" + S.escolha(x[2], g("nomes.nn")), "nomes.in")
    a(rr + 3, "=" + ns, "nomes.ns")
    a(rr + 4, "=" + S.passo(g("nomes.ns")), "nomes.ps")
    a(rr + 5, "=" + S.escolha(x[3], g("nomes.ns")), "nomes.is")
    seqs = {}
    k = rr + 6
    for id_, c in (("lugar_a", 4), ("lugar_b", 5), ("nave_a", 6), ("nave_b", 7), ("organizacao", 8)):
        seqs[id_] = _sequencia(ws, a, g, k, id_, x[c], f"nomes.{id_}")
        k += 3
    cabs(ws, r + 2, {"A": "Nº", "B": ("Pessoa", "D"), "E": ("Lugar", "F"), "G": ("Nave", "H"),
                     "I": ("Organização", "J"), "K": ("Aviso", "L")})
    for j in range(NOMES_AVULSOS):
        rl = r + 3 + j
        rot(ws, f"A{rl}", str(j + 1), negrito=True)
        i_n = S.kesimo_sem_repetir(g("nomes.in"), j, g("nomes.nn"), g("nomes.pn"))
        i_s = S.kesimo_sem_repetir(g("nomes.is"), j, g("nomes.ns"), g("nomes.ps"))
        a(k + 2 * j, "=" + i_n, f"nomes.{j}.in")
        a(k + 2 * j + 1, "=" + i_s, f"nomes.{j}.is")
        nome = H.escolher(RI, [H.k_esimo(f"nome.{NM.SLUG[c]}", g(f"nomes.{j}.in")) for c in NM.CULTURAS])
        sob = H.escolher(RI, [H.k_esimo(f"sobrenome.{NM.SLUG[c]}", g(f"nomes.{j}.is")) for c in NM.CULTURAS])
        N.aux(ws, f"O{rl}", "=" + nome, nome=f"mundos.g.nomes.{j}.nome")
        N.aux(ws, f"P{rl}", "=" + sob, nome=f"mundos.g.nomes.{j}.sob")
        cal(ws, f"B{rl}", "=" + H.montar_nome(RI, g(f"nomes.{j}.nome"), g(f"nomes.{j}.sob")),
            nome=f"mundos.nomes.{j + 1}.pessoa", ate="D")

        def item(id_):
            n, p, i0 = seqs[id_]
            return f'IF({n}<=0,"",{H.k_esimo(id_, S.kesimo_sem_repetir(i0, j, n, p))})'
        cal(ws, f"E{rl}", "=" + junta(item("lugar_a"), item("lugar_b")), nome=f"mundos.nomes.{j + 1}.lugar", ate="F")
        cal(ws, f"G{rl}", "=" + junta(item("nave_a"), item("nave_b")), nome=f"mundos.nomes.{j + 1}.nave", ate="H")
        cal(ws, f"I{rl}", "=" + item("organizacao"), nome=f"mundos.nomes.{j + 1}.org", ate="J")
        if j == 0:
            av(ws, f"K{rl}", "mundos.nomes.aviso.vazia",
               "=" + H.escolher(RI, [f'IF({H.n("nome." + NM.SLUG[c])}+{H.n("sobrenome." + NM.SLUG[c])}<=0,'
                                     f'"Listas de nome da cultura {c} vazias (aba Tabelas)","")' for c in NM.CULTURAS]),
               ate="L")
    N.subtabela(ws, "mundos.nomes", [r + 2], "A:L", NOMES_AVULSOS)
    rot(ws, f"A{r + 3 + NOMES_AVULSOS}", "Com 10 ou mais entradas na lista, os 10 nomes de cada coluna não se repetem "
                                         "(sequência com passo primo, 6.17).", ate="L", italico=True)
    return r + 4 + NOMES_AVULSOS


def _consulta(ws, r):
    titulo(ws, r, "As 8 facções do livro: como usar (27.16)")
    cabs(ws, r + 1, {"A": ("Facção", "B"), "C": ("Como usar (27.16)", "J")})
    for k in range(1, 9):
        rr = r + 1 + k
        cal(ws, f"A{rr}", "=" + N.dcel("faccoes_uso", "Facção", k), nome=f"mundos.livro.faccao.{k}", ate="B",
            negrito=True)
        cal(ws, f"C{rr}", "=" + N.dcel("faccoes_uso", "Como usar", k), nome=f"mundos.livro.faccao.{k}.uso", ate="J")
    r = r + 11
    titulo(ws, r, "Os 6 locais do livro (27.17)")
    cabs(ws, r + 1, {"A": "Lugar", "B": ("O que é", "F"), "G": ("A cena que ele entrega", "J")})
    for k in range(1, 7):
        rr = r + 1 + k
        cal(ws, f"A{rr}", "=" + N.dcel("locais_livro", "Lugar", k), nome=f"mundos.livro.local.{k}", negrito=True)
        cal(ws, f"B{rr}", "=" + N.dcel("locais_livro", "O que é", k), nome=f"mundos.livro.local.{k}.oque", ate="F")
        cal(ws, f"G{rr}", "=" + N.dcel("locais_livro", "A cena que ele entrega", k),
            nome=f"mundos.livro.local.{k}.cena", ate="J")
    return r + 9
