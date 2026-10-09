/*
 * mestre.js — As telas de mesa da Área do Mestre: Painel, Grupo, Combate, Inimigos e
 * Encontros, com as ações de todas elas. O estado, a sincronia com as fichas e as regras
 * ficam em mestre-base.js; as telas de consulta, em mestre-escudo.js.
 */
(function () {
  "use strict";

  const EG = window.EG;
  const { esc, sinal, botaoRolar } = EG;
  const M = window.Motor;
  const C = () => window.CATALOGO;
  const F = EG.Ficha;
  const G = EG.Mestre;
  const H = G.H;
  const link = (n, t, r) => EG.Regras.link(n, t, r);

  const app = G.app;
  const vazio = G.vazio;
  const topo = G.topo;
  const linhaDaAncora = G.linhaDaAncora;
  const fichasTexto = G.fichasTexto;

  // ---------------------------------------------------------------------------
  // Painel
  // ---------------------------------------------------------------------------
  function tiraDoGrupo(g) {
    if (!g.length) return vazio("Nenhuma ficha no grupo ainda. <a href='#mestre/grupo'>Monte o grupo »</a>");
    return "<ul class='tira-grupo'>" + g.map((m) => {
      const pv = G.pvAtual(m), j = m.p.jogo;
      const conds = (j.condicoes || []).length;
      return "<li><div class='tira-topo'><b>" + esc(G.nome(m)) + "</b>" +
        "<span class='suave'>" + esc([m.p.caminho, "nível " + m.p.nivel, m.p.elemento].filter(Boolean).join(" · ")) + "</span></div>" +
        "<div class='tira-pv'><span>" + pv + "<small>/" + m.R.pv_max + "</small></span>" + H.barraPV(pv, m.R.pv_max, "PV de " + G.nome(m)) + "</div>" +
        "<div class='tira-extra'>" +
        "<span title='Energia'>Energia " + (j.energia || 0) + "/100" + ((j.energia || 0) >= m.R.ultimate.custo ? " <span class='etiqueta pronta'>Ult</span>" : "") + "</span>" +
        "<span title='Velocidade'>VEL " + m.R.velocidade + "</span>" +
        "<span title='Defesa'>DEF " + m.R.defesa_com_temporarios + "</span>" +
        (conds ? "<span class='ruim'>" + conds + (conds > 1 ? " condições" : " condição") + "</span>" : "") +
        (m.R.memo ? "<span>" + (j.memo_ativo ? "<span class='etiqueta pronta'>Memo em campo</span>" : "Memo fora") + "</span>" : "") +
        (pv === 0 ? "<span class='etiqueta ruim'>Morrendo " + j.morrendo.s + " sucesso(s) e " + j.morrendo.f + " falha(s)</span>" : "") +
        "</div></li>";
    }).join("") + "</ul>";
  }

  function cartaoPH(g) {
    const r = G.recursoPH(g);
    if (!r) return "";
    return H.cartao("PH do grupo", "<div class='recurso-topo'><b class='ph-grande'>" + r.atual + " / " + r.max + "</b>" +
      "<span class='suave'>começa o combate com " + r.inicio + " · gera " + r.geracao + " por Ataque Básico que acerta</span></div>" +
      "<div class='botoes compactos'>" +
      H.botao("ph", "−1", { dados: { v: -1 } }) + H.botao("ph", "+1", { dados: { v: 1 } }) +
      H.botao("ph", "Início do combate (" + r.inicio + ")", { dados: { v: "inicio" } }) +
      H.botao("ph", "Cheio", { dados: { v: "max" } }) + "</div>" +
      (r.divergente ? "<p class='ajuda ruim'>As fichas do grupo não concordam no PH ou no tamanho do grupo. " +
        "Qualquer botão daqui grava o mesmo valor em todas.</p>"
        : "<p class='ajuda'>O PH é um recurso só (" + link("16", "16.2", "16.2") + "): tudo que você mexer aqui " +
          "vai " + fichasTexto(g.length) + " do grupo.</p>"), "ph-mestre");
  }

  function cartaoDTdaFaixa() {
    const dt = C().mestre.dt_faixa, f = G.faixaN();
    const linhas = dt.linhas.map((l) => [
      "<b>" + esc(l.dificuldade) + "</b>",
      ...l.dt.map((v, i) => (i + 1 === f ? "<b class='destaque'>" + v + "</b>" : String(v))),
    ]);
    return H.cartao("DT por faixa", H.tabela(["Dificuldade"].concat(dt.faixas.map((x, i) =>
      i + 1 === f ? "<b class='destaque'>" + esc(x) + "</b>" : esc(x))), linhas) +
      "<p class='ajuda'>A faixa é <b>do desafio</b>, não do personagem: um muro continua DT 13 no nível 20. " +
      "Sucesso automático só em Teste de Perícia. " + link("27", "27.2", "27.2") + "</p>", "dt-faixa",
      link("27", "27.2"));
  }

  function cartaoRolador() {
    const atalhos = ["d20", "d100", "2d6", "1d6", "1d8", "1d10", "1d12"];
    return H.cartao("Rolar", "<div class='botoes compactos'>" +
      atalhos.map((d) => botaoRolar(d, "Mestre: " + d)).join(" ") + "</div>" +
      "<div class='linha'>" + H.campo("Rolagem livre",
        "<input type='text' id='rolagem-livre' placeholder='3d8+2' aria-label='Rolagem livre'>",
        "Formato <code>NdF+M</code>", "estreito") +
      H.botao("rolar-livre", "Rolar", { classe: "primario" }) + "</div>" +
      "<p class='ajuda'>Qualquer valor em dourado na tela toda é clicável e rola. O histórico fica no " +
      "canto, em <b>Rolagens</b>.</p>", "rolador");
  }

  function telaPainel() {
    const est = G.estado(), g = G.grupo(), cb = est.combate;
    const nivelReal = G.nivelGrupo(g);
    const cartaoCampanha = H.cartao("Campanha",
      "<div class='linha'>" +
      H.campo("Nome da campanha", H.texto("g", "campanha.nome", { rotulo: "Nome da campanha", ph: "O Lacre do Poço Sete" })) +
      H.campo("Mestre", H.texto("g", "campanha.mestre", { rotulo: "Mestre" }), "", "estreito") +
      H.campo("Sessão", H.numero("g", "campanha.sessao", { min: 1, rotulo: "Sessão" }), "", "estreito") +
      "</div><div class='linha'>" +
      H.campo("Nível do grupo", H.numero("g", "campanha.nivel", { min: 1, max: 20, rotulo: "Nível do grupo" }),
        "Define a faixa, o orçamento e as DTs", "estreito") +
      H.campo("Faixa", "<span class='valor grande-valor'>" + esc(G.faixaTexto()) + "</span>", "", "estreito") +
      H.campo("Onde o grupo está", H.texto("g", "campanha.local", { rotulo: "Onde o grupo está", ph: "Doca orbital de Jarilo-VI" })) +
      "</div>" +
      (nivelReal && nivelReal !== G.nivel()
        ? "<p class='ajuda'>As fichas do grupo vão até o <b>nível " + nivelReal + "</b>. " +
          H.botao("usar-nivel-do-grupo", "Usar o nível " + nivelReal, { classe: "pequeno" }) + "</p>" : "") +
      H.campo("Semente e anotações da campanha",
        H.texto("g", "campanha.notas", { area: true, linhas: 3, rotulo: "Anotações da campanha",
          ph: "Decisões da mesa, precedentes, promessas feitas aos jogadores…" }),
        "A Ficha de Decisões da Mesa do " + link("27", "27.11", "27.11")),
      "campanha");

    const cartaoCombate = H.cartao("Combate",
      cb.ativo
        ? "<p><b>" + esc(cb.nome || "Combate sem nome") + "</b> — <b>Ciclo " + cb.ciclo + "</b> · " +
          cb.inimigos.length + (cb.inimigos.length === 1 ? " inimigo" : " inimigos") + " em cena.</p>" +
          "<div class='botoes'><a class='botao primario' href='#mestre/combate'>Voltar ao combate »</a></div>"
        : "<p class='ajuda'>Nenhum combate em curso.</p>" +
          "<div class='botoes'><a class='botao' href='#mestre/encontros'>Montar um encontro</a>" +
          "<a class='botao primario' href='#mestre/combate'>Abrir a mesa de combate</a></div>",
      "combate-resumo");

    const checklist = H.cartao("Antes de abrir a sessão",
      "<ul class='checklist'>" +
      "<li>O grupo tem o <b>Cone e o Tier da faixa</b>? <a href='#mestre/recompensas'>Conferir</a> — o orçamento de encontro assume que sim (" + link("27", "27.8", "27.8") + ")</li>" +
      "<li>O encontro cumpre o <b>contrato da Fraqueza</b>? <a href='#mestre/encontros'>Conferir</a> (" + link("27", "27.5", "27.5") + ")</li>" +
      "<li>Os <b>PV e o PH</b> do grupo estão como terminou a sessão passada? <a href='#mestre/grupo'>Ver o grupo</a></li>" +
      "<li>Alguma condição ficou pendurada de antes? O Descanso Longo limpa tudo (" + link("23", "23.6", "23.6") + ")</li>" +
      "</ul>", "checklist");

    app().innerHTML = topo("painel") +
      "<div class='grade-mestre'>" +
      "<div class='coluna'>" + cartaoCampanha + H.cartao("Grupo", tiraDoGrupo(g) +
        "<div class='botoes'><a class='botao' href='#mestre/grupo'>Abrir o grupo</a>" +
        (g.length ? H.botao("descanso-curto", "Descanso Curto") + H.botao("descanso-longo", "Descanso Longo") : "") +
        "</div>", "grupo-resumo", link("23", "23.6", "descansos")) + "</div>" +
      "<div class='coluna'>" + cartaoPH(g) + cartaoCombate + cartaoDTdaFaixa() + "</div>" +
      "<div class='coluna'>" + cartaoRolador() + checklist + "</div>" +
      "</div>" +
      "<p class='ajuda rodape-mestre'>PV, Energia, PH, condições e Memoespírito que você mexer aqui " +
      "são gravados nas fichas salvas neste navegador, e aparecem na aba <b>Jogar</b> de cada jogador. " +
      "Use <b>Mais &gt; Exportar tudo</b> para guardar uma cópia de tudo.<br>" +
      H.botao("rever-aviso", "Rever o aviso de spoiler", { classe: "pequeno" }) + "</p>";
  }

  // ---------------------------------------------------------------------------
  // Grupo
  // ---------------------------------------------------------------------------
  function condicoesDe(m) {
    const j = m.p.jogo;
    const lista = C().condicoes.filter((c) => c.so_inimigos === "Não" && c.condicao !== "Morrendo");
    const ativas = (j.condicoes || []).map((c, i) => {
      const info = G.infoCondicao(c.nome);
      return "<li><div><b>" + esc(c.nome) + "</b>" +
        (c.turnos != null ? " <span class='etiqueta'>" + c.turnos + (c.turnos === 1 ? " turno" : " turnos") + "</span>" : "") +
        (c.acumulos > 1 ? " <span class='etiqueta'>" + c.acumulos + "×</span>" : "") +
        " <span class='suave'>" + esc(info.duracao || "") + "</span> " + link("21", c.nome, "regra") + "</div>" +
        "<p class='efeito'>" + esc(info.efeito || "") + "</p>" +
        "<div class='botoes compactos'>" +
        H.botao("cond-turno", "−1 turno", { classe: "pequeno", dados: { mid: m.id, i: i, v: -1 } }) +
        H.botao("cond-turno", "+1", { classe: "pequeno", dados: { mid: m.id, i: i, v: 1 } }) +
        H.botao("tirar-cond-pj", "Tirar", { classe: "pequeno perigo", dados: { mid: m.id, i: i } }) +
        "</div></li>";
    }).join("");
    return (ativas ? "<ul class='lista-condicoes'>" + ativas + "</ul>" : vazio("Nenhuma condição ativa.")) +
      "<div class='linha'><label class='sr-only' for='cond-" + esc(m.id) + "'>Condição</label>" +
      "<select id='cond-" + esc(m.id) + "'><option value=''>— aplicar condição —</option>" +
      lista.map((c) => "<option>" + esc(c.condicao) + "</option>").join("") + "</select>" +
      "<input type='number' min='1' class='curto' id='cond-t-" + esc(m.id) + "' placeholder='turnos' aria-label='Turnos'>" +
      H.botao("por-cond-pj", "Aplicar", { dados: { mid: m.id } }) + "</div>";
  }

  function cartaoMemoDoPJ(m) {
    if (!m.R.memo || m.p.caminho !== "A Recordação") return "";
    const memo = m.p.memoespirito, mm = m.R.memo, j = m.p.jogo;
    const pv = j.memo_pv == null ? mm.pv : Math.min(j.memo_pv, mm.pv);
    return "<div class='subcartao memo-mestre'>" +
      "<div class='subcartao-topo'><b>" + esc(memo.nome || "Memoespírito") + "</b>" +
      "<span class='suave'>de " + esc(G.nome(m)) + " · " + esc([memo.funcao, memo.elemento].filter(Boolean).join(" · ")) + "</span></div>" +
      "<div class='linha'>" +
      (j.memo_ativo
        ? "<span class='etiqueta pronta'>em campo</span> " +
          H.botao("dispensar-memo", "Dispensar", { classe: "pequeno", dados: { mid: m.id } })
        : H.botao("invocar-memo", "Invocar (Ação Complementar + 1 PH)", { classe: "primario pequeno", dados: { mid: m.id } })) +
      "</div>" +
      "<div class='numeros compactos'>" + H.num("PV", pv + "<small>/" + mm.pv + "</small>") +
      H.num("Defesa", mm.defesa) + H.num("VEL", mm.velocidade) + H.num("RD", mm.rd) +
      H.num("Tenacidade", mm.rt, "reduz") + "</div>" +
      "<div class='linha'>" + H.campo("PV dele agora", H.numero(m.id, "jogo.memo_pv", { min: 0, max: mm.pv, rotulo: "PV do Memoespírito" }), "", "estreito") +
      "<div class='campo estreito'><span class='rotulo'>Ataque e dano</span><span>" +
      botaoRolar(M.rolagem(mm.ataque), (memo.nome || "Memoespírito") + ": ataque") + " " +
      botaoRolar(mm.texto, (memo.nome || "Memoespírito") + ": dano") + " <small>média " + mm.media + "</small></span></div></div>" +
      "<p class='ajuda'>Casa própria na Fila pela VEL dele, 1 ação por turno. A 0 PV ele cai e só volta no " +
      "próximo Descanso Curto. " + link("11", "11.5", "11.5") + "</p></div>";
  }

  function cartaoMembro(m) {
    const R = m.R, j = m.p.jogo, pv = G.pvAtual(m);
    const falta = (function () { F.P = m.p; F.R = R; const x = F.pendencias(); F.P = null; F.R = null; return x; })();
    let corpo = "<div class='membro-topo'>" +
      "<div><h3>" + esc(G.nome(m)) + "</h3><p class='suave'>" +
      esc([m.p.jogador && "jogador: " + m.p.jogador, m.p.raca, m.p.caminho, "nível " + m.p.nivel, m.p.elemento].filter(Boolean).join(" · ")) + "</p></div>" +
      "<div class='botoes compactos'>" +
      "<a class='botao pequeno' href='#jogar'>abrir a ficha</a>" +
      H.botao("subir", "subir", { classe: "pequeno", dados: { mid: m.id, v: -1 }, titulo: "Subir na ordem da mesa" }) +
      H.botao("subir", "descer", { classe: "pequeno", dados: { mid: m.id, v: 1 }, titulo: "Descer na ordem da mesa" }) +
      H.botao("tirar-do-grupo", "Tirar do grupo", { classe: "pequeno perigo", dados: { mid: m.id } }) +
      "</div></div>" +
      (falta.length ? "<div class='status-ficha pendente'>Falta escolher na ficha: <b>" + esc(falta.join(", ")) + "</b></div>" : "");

    corpo += "<div class='pv'><span class='pv-numero'>" + pv + "<small> / " + R.pv_max + "</small></span>" +
      H.barraPV(pv, R.pv_max, "PV de " + G.nome(m)) + "</div>" +
      "<div class='linha controles-pv'>" +
      "<label class='sr-only' for='dano-" + esc(m.id) + "'>Valor</label>" +
      "<input id='dano-" + esc(m.id) + "' type='number' inputmode='numeric' min='0' placeholder='Valor'>" +
      H.botao("dano-pj", "Sofrer dano", { classe: "perigo", dados: { mid: m.id } }) +
      H.botao("curar-pj", "Curar", { classe: "bom", dados: { mid: m.id } }) +
      "<label class='marca'><input type='checkbox' id='cont-" + esc(m.id) + "'> <span>Contínuo (ignora RD " + R.rd + ")</span></label>" +
      "</div>" +
      "<div class='linha'>" +
      H.campo("PV agora", H.numero(m.id, "jogo.pv", { min: 0, max: R.pv_max, rotulo: "PV atual", ph: String(pv) }),
        "Em branco = cheio", "estreito") +
      H.campo("PV temporário", H.numero(m.id, "jogo.temp", { min: 0, max: R.teto_temporarios, rotulo: "PV temporário" }), "Teto " + R.teto_temporarios, "estreito") +
      H.campo("Energia", H.numero(m.id, "jogo.energia", { min: 0, max: 100, rotulo: "Energia" }),
        "Ultimate a " + R.ultimate.custo, "estreito") +
      "</div>" +
      "<div class='botoes compactos'>" +
      H.botao("energia-pj", "+10", { dados: { mid: m.id, v: 10 }, titulo: "Sofrer dano, derrotar ou Quebrar" }) +
      H.botao("energia-pj", "+20", { dados: { mid: m.id, v: 20 }, titulo: "Ataque Básico" }) +
      H.botao("energia-pj", "+30", { dados: { mid: m.id, v: 30 }, titulo: "Habilidade" }) +
      H.botao("energia-pj", "−" + R.ultimate.custo, { dados: { mid: m.id, v: -R.ultimate.custo }, titulo: "Gastou a Ultimate" }) +
      ((j.energia || 0) >= R.ultimate.custo ? " <span class='etiqueta pronta'>Ultimate pronta</span>" : "") +
      "</div>";

    corpo += "<div class='numeros compactos'>" +
      H.num("Defesa", R.defesa_com_temporarios) +
      H.num("Esquiva", R.esquiva == null ? "—" : R.esquiva) +
      H.num("RD", R.rd) + H.num("VEL", R.velocidade) +
      H.num("DT dele", R.dt, "Habilidades") +
      H.num("Eficiência", sinal(R.eficiencia)) +
      "</div>" +
      "<p class='ajuda'>Descanso Curto devolve <b>" + Math.max(0, R.descanso_curto) + " PV</b> a ele. " +
      (R.esforco_max ? "Esforço: " + (j.esforco ? "<b>disponível</b>" : "gasto") + ". " : "") +
      "Capacidade " + R.ocupado + "/" + R.capacidade + " de Espaço.</p>";

    if (pv === 0) {
      const mo = j.morrendo;
      const bolas = (n, t) => Array.from({ length: 3 }, (_, i) => "<span class='bolinha" + (i < n ? " cheia " + t : "") + "'></span>").join("");
      corpo += "<div class='morrendo'><h3>Morrendo</h3>" +
        "<p>No turno dele: <b>d20 " + sinal(R.morrendo_bonus) + "</b> contra DT 10" +
        (R.morrendo_vantagem ? ", com <b>Vantagem</b>" : "") + ". 3 sucessos: 1 PV. 3 falhas: morte. " + link("23", "23.4", "23.4") + "</p>" +
        "<p>Sucessos " + bolas(mo.s, "s") + " &nbsp; Falhas " + bolas(mo.f, "f") +
        (R.pode_ser_executado ? " &nbsp; <span class='etiqueta ruim'>pode ser Executado</span>" : "") + "</p>" +
        "<div class='linha'>" + H.botao("rolar-morrendo", "Rolar o Teste de Morrendo", { classe: "primario", dados: { mid: m.id } }) +
        H.campo("Sucessos", H.numero(m.id, "jogo.morrendo.s", { min: 0, max: 3, rotulo: "Sucessos" }), "", "estreito") +
        H.campo("Falhas", H.numero(m.id, "jogo.morrendo.f", { min: 0, max: 3, rotulo: "Falhas" }), "", "estreito") +
        "</div></div>";
    }

    corpo += "<h3>Condições</h3>" + condicoesDe(m) + cartaoMemoDoPJ(m);
    return "<section class='cartao membro'>" + corpo + "</section>";
  }

  function telaGrupo() {
    const est = G.estado(), g = G.grupo(), fora = G.foraDoGrupo();
    const tam = G.tamanhoGrupo(g);
    const r = G.recursoPH(g);
    const elementos = G.elementosDoGrupo(g);

    let cabeca = H.cartao("Tamanho e recursos do grupo",
      "<div class='linha'>" +
      H.campo("Jogadores na mesa",
        "<select id='tamanho-grupo' aria-label='Jogadores na mesa'>" +
        [1, 2, 3, 4, 5, 6].map((n) => "<option value='" + n + "'" + (n === tam ? " selected" : "") + ">" + n + "</option>").join("") +
        "</select>", "Grava o número " + fichasTexto(g.length) + " do grupo", "estreito") +
      (r ? H.campo("PH máximo", "<span class='valor grande-valor'>" + r.max + "</span>", "1 + jogadores + extra do nível", "estreito") +
        H.campo("PH no início do combate", "<span class='valor grande-valor'>" + r.inicio + "</span>", "máximo − 2", "estreito") +
        H.campo("PH gerado por acerto", "<span class='valor grande-valor'>" + r.geracao + "</span>", "Ataque Básico que acerta", "estreito") : "") +
      "</div>" +
      (tam < 3 || tam > 6 ? "<p class='ajuda ruim'>A tabela de PH do livro vai de 3 a 6 jogadores (" +
        link("16", "16.2", "16.2") + ").</p>" : "") +
      "<p class='ajuda'>O tamanho do grupo entra na tabela de PH (" + link("16", "16.2", "16.2") + ") e é lido " +
      "pela ficha de cada jogador.</p>", "tamanho");

    if (r) cabeca += cartaoPH(g);

    const elementosFaltando = G.ELEMENTOS.filter((e) => !elementos.includes(e));
    const cobertura = H.cartao("Elementos, Fila e surpresa",
      "<p><b>Elementos do grupo:</b> " + (elementos.length ? elementos.map((e) => "<span class='etiqueta'>" + esc(e) + "</span>").join(" ") : "<span class='suave'>nenhum ainda</span>") + "</p>" +
      "<p class='ajuda'>O contrato de 27.5 pede que <b>pelo menos 3 destes</b> apareçam como Fraqueza entre os " +
      "inimigos da cena. Fora do grupo: " + (elementosFaltando.length ? esc(elementosFaltando.join(", ")) : "nenhum") + ". " +
      link("27", "27.5", "27.5") + "</p>" +
      (g.length ? "<h3>Ordem por Velocidade</h3>" + H.tabela(["#", "Quem", "VEL", "Agilidade", "Discernimento"],
        g.slice().sort((a, b) => b.R.velocidade - a.R.velocidade).map((m, i) => [
          String(i + 1), esc(G.nome(m)), "<b>" + m.R.velocidade + "</b>",
          sinal((m.R.bonus || {}).Agilidade || 0), sinal((m.R.bonus || {}).Discernimento || 0),
        ])) + "<p class='ajuda'>Empate: maior bônus de Agilidade, depois Discernimento, depois os jogadores " +
        "escolhem entre si e vêm antes dos NPCs. Nunca se rola a ordem. " + link("19", "19.3", "19.3") + "</p>" : "") +
      "<h3>Surpresa</h3><p class='ajuda'>Teste de Percepção Mental contra <b>DT 13</b>, fixa em todas as faixas. " +
      "Quem falha fica Surpreso e tem a casa pulada no primeiro Ciclo. Se há um atacante escondido, o " +
      "Teste de Furtividade dele substitui a DT 13 para o lado todo. " + link("19", "19.3", "19.3") + "</p>" +
      (g.length ? "<div class='botoes compactos'>" + g.map((m) => {
        const tr = (m.R.testes_resistencia || {})["Percepção Mental"] || {};
        return "<span class='rolagem-pj'>" + esc(G.nome(m).split(" ")[0]) + " " +
          botaoRolar(tr.rolagem || "d20", G.nome(m) + ": Percepção Mental (Surpresa, DT 13)",
            { vantagem: !!tr.vantagem }) + "</span>";
      }).join(" ") + "</div>" : ""),
      "cobertura");

    const descansos = H.cartao("Descansos e combate",
      "<div class='botoes'>" +
      H.botao("descanso-curto", "Descanso Curto no grupo", { titulo: "1 hora, até 2 por dia: cada um recupera 2 × nível + Vigor" }) +
      H.botao("descanso-longo", "Descanso Longo no grupo", { classe: "primario", titulo: "8 horas: PV cheios, condições removidas, usos e Esforço de volta" }) +
      "</div>" +
      "<p class='ajuda'>O Descanso Longo zera as condições de todos, devolve o Esforço e dispensa os " +
      "Memoespíritos. " + link("23", "23.6", "23.6") + "</p>", "descansos");

    const adicionar = H.cartao("Pôr ficha no grupo",
      (fora.length
        ? "<div class='linha'><label class='sr-only' for='nova-ficha'>Ficha salva</label>" +
          "<select id='nova-ficha'>" + fora.map((m) => "<option value='" + esc(m.id) + "'>" +
            esc(G.nome(m)) + " · nível " + esc(m.p.nivel) + (m.p.caminho ? " · " + esc(m.p.caminho) : "") +
            "</option>").join("") + "</select>" +
          H.botao("por-no-grupo", "Pôr no grupo", { classe: "primario" }) +
          (fora.length > 1 ? H.botao("por-todas", "Pôr todas (" + fora.length + ")") : "") + "</div>"
        : vazio("Todas as fichas salvas neste navegador já estão no grupo.")) +
      "<div class='botoes'>" +
      H.botao("importar-ficha", "Importar ficha (.json do jogador)") +
      "<a class='botao' href='#editar'>Criar uma ficha nova</a>" +
      H.botao("exemplo-nadir", "Pôr o exemplo (Nadir, 29.7)") +
      "</div>" +
      "<p class='ajuda'>As fichas ficam salvas neste navegador. Peça a cada jogador o arquivo " +
      "<code>.json</code> (<b>Mais &gt; Exportar</b> na ficha dele) e importe aqui: o grupo passa a mostrar os " +
      "números reais da ficha, e o que você mexer volta para ela.</p>", "adicionar");

    app().innerHTML = topo("grupo") + cabeca + adicionar +
      (g.length ? "<div class='grade-membros'>" + g.map(cartaoMembro).join("") + "</div>"
        : H.cartao("Grupo vazio", vazio("Ponha uma ficha no grupo acima para ver PV, Energia, condições e " +
          "Memoespírito de cada jogador aqui."), "vazio")) +
      "<div class='grade-mestre duas'><div class='coluna'>" + cobertura + "</div>" +
      "<div class='coluna'>" + descansos + "</div></div>";
  }

  // ---------------------------------------------------------------------------
  // Combate
  // ---------------------------------------------------------------------------
  const inimigoPorUid = (uid) => G.estado().combate.inimigos.find((x) => x.uid === uid);
  const indiceDoInimigo = (uid) => G.estado().combate.inimigos.findIndex((x) => x.uid === uid);

  /** O item da Fila de uma chave ("p:id", "m:id", "i:uid"). */
  function itemDaChave(chave) {
    const f = G.fila();
    return f.casas.concat(f.fora).find((i) => i.chave === chave) || null;
  }

  function casaDaFila(i, cb) {
    const cc = i.cc;
    const tipoAtraso = i.kind === "inimigo" ? i.tipo : "Comum";
    const etiqueta = i.kind === "inimigo"
      ? "<span class='etiqueta tipo-" + i.tipo.toLowerCase() + "'>" + esc(i.tipo) + "</span>"
      : i.kind === "memo" ? "<span class='etiqueta'>Memoespírito</span>" : "<span class='etiqueta pj'>PJ</span>";
    const quebrado = i.x && i.x.quebrado;
    let vitais = "<div class='casa-vital'><span class='rotulo'>PV</span>" +
      "<b>" + i.pv + "<small>/" + i.pv_max + "</small></b>" + H.barraPV(i.pv, i.pv_max, "PV de " + i.nome) + "</div>";
    if (i.kind === "inimigo") {
      const t = G.tenacidadeAtual(i.x);
      vitais += "<div class='casa-vital'><span class='rotulo'>Tenacidade</span>" +
        "<b>" + t + "<small>/" + (i.x.tenacidade || 0) + "</small></b>" + H.barraTenacidade(t, i.x.tenacidade || 0) + "</div>";
    }
    const conds = (i.condicoes || []).filter((c) => c.nome !== "Quebrado");
    return "<li class='fila-casa" + (i.agora ? " agora" : "") + (cc.agiu ? " agiu" : "") +
      (i.pv === 0 ? " caiu" : "") + (quebrado ? " quebrado" : "") + "'>" +
      "<div class='casa-num'>" + i.casa + (i.agora ? "<span class='sr-only'> (agindo agora)</span>" : "") + "</div>" +
      "<div class='casa-quem'><div><b>" + esc(i.nome) + "</b> " + etiqueta +
      (i.agora ? " <span class='etiqueta pronta'>agindo agora</span>" : "") +
      (quebrado ? " <span class='etiqueta ruim'>Quebrado</span>" : "") +
      (i.pv === 0 ? " <span class='etiqueta ruim'>" + (i.kind === "pj" ? "Morrendo" : i.kind === "memo" ? "caiu" : "derrotado") + "</span>" : "") +
      "</div><div class='suave'>" + esc(i.sub) + " · VEL " + i.vel +
      (i.atraso_casas ? " · <span class='ruim'>atrasado " + i.atraso_casas + (i.atraso_casas > 1 ? " casas" : " casa") +
        (i.atraso_bruto !== i.atraso_casas ? " (de " + i.atraso_bruto + " brutas" + (G.temFirmeza(tipoAtraso) ? ", Firmeza" : "") + ")" : "") + "</span>" : "") +
      (i.avanco_casas ? " · <span class='bom-texto'>avançado " + i.avanco_casas + "</span>" : "") +
      (cc.pendente ? " · <span class='ruim'>" + cc.pendente + " pendente</span>" : "") +
      "</div>" +
      (conds.length ? "<div class='casa-cond'>" + conds.map((c) => "<span class='etiqueta'>" + esc(c.nome) +
        (c.turnos != null ? " " + c.turnos + "t" : "") + (c.acumulos > 1 ? " ×" + c.acumulos : "") + "</span>").join(" ") + "</div>" : "") +
      "</div>" +
      "<div class='casa-vitais'>" + vitais + "</div>" +
      "<div class='casa-botoes'>" +
      H.botao("agiu", cc.agiu ? "Desfazer o turno" : "Já agiu", { classe: "pequeno" + (cc.agiu ? "" : " primario"), dados: { k: i.chave } }) +
      H.botao("atrasar", "Atrasar +1", { classe: "pequeno", dados: { k: i.chave, v: 1 }, titulo: "Soma 1 casa bruta no Ciclo (19.4)" }) +
      H.botao("atrasar", "−1", { classe: "pequeno", dados: { k: i.chave, v: -1 }, desabilitado: !cc.atraso }) +
      H.botao("avancar", "Avançar +1", { classe: "pequeno", dados: { k: i.chave, v: 1 }, desabilitado: cc.agiu, titulo: "Só funciona em quem ainda não agiu (19.5)" }) +
      H.botao("avanco-total", cc.avanco_total ? "Avanço Total: ligado" : "Avanço Total", { classe: "pequeno", dados: { k: i.chave }, titulo: "Age logo depois do turno atual, 1× por Ciclo (19.5)" }) +
      H.botao("escolher-alvo", cb.alvo === i.chave ? "Fechar" : "Abrir", { classe: "pequeno", dados: { k: i.chave } }) +
      H.botao("fora-da-fila", "Fora", { classe: "pequeno perigo", dados: { k: i.chave }, titulo: "Tira da Fila deste combate" }) +
      "</div></li>";
  }

  function painelDoInimigo(x) {
    const i = indiceDoInimigo(x.uid), cam = "combate.inimigos." + i;
    const t = G.tenacidadeAtual(x);
    const pv = x.pv == null ? x.pv_max : x.pv;
    const marcas = (campo) => G.ELEMENTOS.map((e) =>
      "<label class='marca'><input type='checkbox' data-m='toggle-elemento' data-uid='" + esc(x.uid) +
      "' data-campo='" + campo + "' data-el='" + esc(e) + "'" + ((x[campo] || []).includes(e) ? " checked" : "") +
      "> <span>" + esc(e) + "</span></label>").join("");
    let corpo = "<div class='linha'>" +
      H.campo("Nome", H.texto("g", cam + ".nome", { rotulo: "Nome do inimigo" })) +
      H.campo("Tipo", H.lista("g", cam + ".tipo", G.TIPOS, { rotulo: "Tipo", vazio: false }), "", "estreito") +
      H.campo("Faixa", "<span class='valor'>" + esc(x.faixa || "—") + "</span>", esc(x.origem || ""), "estreito") +
      (x.fases > 1 ? H.campo("Fase em vigor", H.numero("g", cam + ".fase", { min: 1, max: x.fases, rotulo: "Fase" }),
        "de " + x.fases, "estreito") : "") +
      "</div>" +
      "<div class='pv'><span class='pv-numero'>" + pv + "<small> / " + x.pv_max + "</small></span>" +
      H.barraPV(pv, x.pv_max, "PV de " + (x.nome || "inimigo")) + "</div>" +
      "<div class='linha controles-pv'>" +
      "<label class='sr-only' for='dano-i-" + esc(x.uid) + "'>Valor</label>" +
      "<input id='dano-i-" + esc(x.uid) + "' type='number' inputmode='numeric' min='0' placeholder='Dano bruto'>" +
      H.botao("dano-inimigo", "Dano", { classe: "perigo", dados: { uid: x.uid } }) +
      H.botao("curar-inimigo", "Curar", { classe: "bom", dados: { uid: x.uid } }) +
      "<label class='marca'><input type='checkbox' id='cont-i-" + esc(x.uid) + "'> <span>Contínuo (ignora RD " + (x.rd || 0) + ")</span></label>" +
      "</div>" +
      "<p class='ajuda'>A RD sai de <b>cada instância</b> de dano (" + link("18", "18.4", "18.4") + "). " +
      (x.quebrado ? "Ele está <b>Quebrado</b>: −2 de Defesa e <b>+1 dado</b> de dano de qualquer fonte." : "") + "</p>";

    corpo += "<div class='numeros compactos'>" +
      H.num("Defesa", (x.defesa || 0) - (x.quebrado ? 2 : 0), x.quebrado ? "base " + x.defesa + ", Quebrado −2" : "") +
      H.num("RD", x.rd || 0) + H.num("VEL", x.vel || 0) +
      H.num("Ataque", sinal(x.ataque || 0)) +
      H.num("DT dos efeitos", x.dt || 0, "o grupo rola") +
      H.num("TR dele", sinal(x.tr || 0), "contra a DT do PJ") +
      "</div>";

    corpo += "<h3>Tenacidade e Quebra</h3>" +
      "<div class='tenacidade-painel'><b>" + t + " / " + (x.tenacidade || 0) + "</b>" +
      H.barraTenacidade(t, x.tenacidade || 0) + "</div>" +
      "<div class='linha'>" +
      H.campo("Máximo", H.numero("g", cam + ".tenacidade", { min: 0, rotulo: "Tenacidade máxima" }), "", "estreito") +
      H.campo("Redução acumulada", H.numero("g", cam + ".reducao", { min: 0, rotulo: "Redução acumulada" }), "", "estreito") +
      "</div>" + calculadoraTenacidade(x) +
      (x.quebrado ? "<p class='ajuda'>A barra volta ao máximo e a condição Quebrado sai <b>no fim do próximo " +
        "turno dele</b> — é o que acontece quando você marca <b>Já agiu</b> na Fila. " + link("20", "20.4", "20.4") + "</p>" : "");

    corpo += "<h3>Fraquezas e Resistências</h3>" +
      "<div class='linha'><div class='campo'><span class='rotulo'>Fraquezas (" +
      (C().mestre.fraquezas_tipo.find((y) => y.tipo === x.tipo) || {}).fraquezas + " para " + esc(x.tipo) + ")</span>" +
      "<div class='grade-marcas'>" + marcas("fraquezas") + "</div></div></div>" +
      "<div class='linha'><div class='campo'><span class='rotulo'>Resistências</span>" +
      "<div class='grade-marcas'>" + marcas("resistencias") + "</div></div></div>" +
      "<p class='ajuda'>Resistência tira 2 dados (conservando 1) e trava a redução de Tenacidade em 1 ponto. " +
      "Nunca aponte uma Resistência para o Elemento de dois personagens. " + link("20", "20.2", "20.2") + "</p>";

    if ((x.ataques || []).length) {
      corpo += "<h3>Ataques</h3><ul class='lista-acoes'>" + x.ataques.map((a) =>
        "<li><div><b>" + esc(a.nome) + "</b> <span class='suave'>" +
        esc([a.alcance, a.elemento, a.nota].filter(Boolean).join(", ")) + "</span></div>" +
        "<div class='acao-numeros'><span>Ataque " + botaoRolar(M.rolagem(x.ataque || 0), (x.nome || "Inimigo") + ": " + a.nome) + "</span>" +
        (a.dados ? "<span>Dano " + botaoRolar(a.dados, (x.nome || "Inimigo") + ": dano de " + a.nome) +
          (a.media ? " <small>média " + a.media + "</small>" : "") + "</span>" : "") +
        (a.elemento ? "<span class='suave'>" + esc(a.elemento) + "</span>" : "") + "</div></li>").join("") + "</ul>";
    } else {
      corpo += "<h3>Ataque</h3><div class='acao-numeros'>" +
        "<span>Ataque " + botaoRolar(M.rolagem(x.ataque || 0), (x.nome || "Inimigo") + ": ataque") + "</span>" +
        (x.dano ? "<span>Dano " + botaoRolar(x.dano, (x.nome || "Inimigo") + ": dano") +
          (x.dano_media ? " <small>média " + x.dano_media + "</small>" : "") + "</span>" : "") +
        "</div><p class='ajuda'>Se preferir não rolar, use a média direto: é o número do orçamento (" +
        link("28", "28.3", "28.3") + ").</p>";
    }

    if ((x.especiais || []).length) {
      corpo += "<h3>Ações especiais</h3><ul class='lista-acoes'>" + x.especiais.map((a) =>
        "<li><div><b>" + esc(a.nome) + "</b>" + (a.recarga ? " <span class='etiqueta'>" + esc(a.recarga) + "</span>" : "") + "</div>" +
        "<p class='efeito'>" + esc(a.efeito) + "</p></li>").join("") + "</ul>";
    }

    corpo += "<h3>Condições nele</h3>" + condicoesDoInimigo(x) +
      (x.fila ? "<p class='ajuda'><b>Na Fila:</b> " + esc(x.fila) + "</p>" : "") +
      (x.frase ? "<p class='efeito'><i>" + esc(x.frase) + "</i></p>" : "") +
      "<div class='botoes'>" +
      (x.fases > 1 ? H.botao("virar-fase", "Virar a fase do Boss", { classe: "primario", dados: { uid: x.uid },
        titulo: "Tenacidade cheia de novo, troca as Fraquezas e anuncia em voz alta (28.5)" }) : "") +
      H.botao("salvar-inimigo", "Salvar na campanha", { dados: { uid: x.uid } }) +
      H.botao("tirar-inimigo", "Tirar do combate", { classe: "perigo", dados: { uid: x.uid } }) +
      (G.doBestiario(x.nome) ? "<a class='botao' href='" + esc(EG.Regras.href("28", x.nome)) + "'>Ficha completa no livro</a>" : "") +
      "</div>";
    return H.cartao(esc(x.nome || "Inimigo sem nome"), corpo, "alvo-painel",
      "<span class='suave'>" + esc(x.tipo) + " · faixa " + esc(x.faixa || "—") + "</span>");
  }

  function condicoesDoInimigo(x) {
    const lista = C().condicoes.filter((c) => c.condicao !== "Morrendo");
    const ativas = (x.condicoes || []).map((c, i) => {
      const info = G.infoCondicao(c.nome);
      return "<li><div><b>" + esc(c.nome) + "</b>" +
        (c.turnos != null ? " <span class='etiqueta'>" + c.turnos + (c.turnos === 1 ? " turno" : " turnos") + "</span>" : "") +
        (c.acumulos > 1 ? " <span class='etiqueta'>" + c.acumulos + "×</span>" : "") +
        (c.origem ? " <span class='suave'>" + esc(c.origem) + "</span>" : "") + " " + link("21", c.nome, "regra") + "</div>" +
        "<p class='efeito'>" + esc(info.efeito || "") + "</p>" +
        "<div class='botoes compactos'>" +
        H.botao("cond-turno-i", "−1 turno", { classe: "pequeno", dados: { uid: x.uid, i: i, v: -1 } }) +
        H.botao("cond-turno-i", "+1", { classe: "pequeno", dados: { uid: x.uid, i: i, v: 1 } }) +
        H.botao("tirar-cond-i", "Tirar", { classe: "pequeno perigo", dados: { uid: x.uid, i: i } }) +
        "</div></li>";
    }).join("");
    return (ativas ? "<ul class='lista-condicoes'>" + ativas + "</ul>" : vazio("Nenhuma condição nele.")) +
      "<div class='linha'><label class='sr-only' for='cond-i-" + esc(x.uid) + "'>Condição</label>" +
      "<select id='cond-i-" + esc(x.uid) + "'><option value=''>— aplicar condição —</option>" +
      lista.map((c) => "<option>" + esc(c.condicao) + (c.so_inimigos === "Sim" ? " (só inimigos)" : "") + "</option>").join("") + "</select>" +
      "<input type='number' min='1' class='curto' id='cond-it-" + esc(x.uid) + "' placeholder='turnos' aria-label='Turnos'>" +
      H.botao("por-cond-i", "Aplicar", { dados: { uid: x.uid } }) + "</div>";
  }

  /** 20.3 + 20.2: redução pela fonte e pela relação do Elemento com o alvo. */
  function calculadoraTenacidade(x) {
    const g = G.grupo();
    const rt = G.estado().combate.rt;
    const fonte = G.FONTES_RT.find((f) => f.id === rt.fonte) || G.FONTES_RT[0];
    const m = rt.quem ? G.membro(rt.quem) : null;
    const elemento = rt.elemento || (m ? m.p.elemento : "");
    const relacao = G.relacaoElemento(x, elemento);
    const previa = G.reducaoTenacidade(fonte.base, relacao);
    return "<div class='subcartao'><div class='subcartao-topo'><b>Calculadora de Tenacidade</b>" +
      link("20", "20.3", "20.3") + "</div>" +
      "<div class='linha'>" +
      H.campo("Quem reduziu", H.lista("g", "combate.rt.quem",
        g.map((y) => [y.id, G.nome(y) + " · " + (y.p.elemento || "sem Elemento") + " · Ef " + sinal(y.R.eficiencia)]),
        { rotulo: "Quem reduziu", vazio: "Eficiência +" + M.eficiencia(G.nivel()) + " (nível do grupo)" }), "", "estreito") +
      H.campo("Fonte", H.lista("g", "combate.rt.fonte",
        G.FONTES_RT.map((f) => [f.id, f.rotulo + " (" + f.base + ")"]),
        { rotulo: "Fonte", vazio: false }), "", "estreito") +
      H.campo("Elemento", H.lista("g", "combate.rt.elemento",
        G.ELEMENTOS.map((e) => [e, e + " (" + G.relacaoElemento(x, e) + ")"]),
        { rotulo: "Elemento", vazio: m && m.p.elemento ? m.p.elemento + " (do personagem)" : "sem Elemento" }), "", "estreito") +
      H.campo("Vai reduzir", "<span class='valor grande-valor'>" + (previa ? "−" + previa : "0") + "</span>",
        elemento ? relacao : "escolha o Elemento", "estreito") +
      H.botao("aplicar-rt", "Reduzir", { classe: "primario", dados: { uid: x.uid } }) +
      "</div>" +
      "<p class='ajuda'>Fraqueza reduz o <b>total</b>; neutro, a <b>metade</b> (arredonda para baixo, mínimo 1); " +
      "Resistência, <b>1 ponto fixo</b>. Dano Contínuo não reduz nada. Zerou? Sai a Quebra: dano do Elemento, " +
      "a condição dele, <b>1 casa de Atraso</b> e <b>+10 de Energia</b> para quem quebrou. " +
      link("20", "20.4", "20.4") + "</p></div>";
  }

  function painelDoPJ(i) {
    const m = i.m;
    if (i.kind === "memo") {
      return H.cartao(esc(i.nome), cartaoMemoDoPJ(m) +
        "<p class='ajuda'>Memoespírito não tem Tenacidade, não fica Quebrado nem Congelado, e o dano nele se " +
        "aplica no campo <b>PV dele agora</b>. " + link("20", "20.1", "20.1") + "</p>", "alvo-painel");
    }
    return "<div class='alvo-painel-pj'>" + cartaoMembro(m) + "</div>";
  }

  function painelDeCondicoes() {
    const f = G.fila();
    const linhas = [];
    for (const i of f.casas) {
      for (const c of i.condicoes || []) {
        const info = G.infoCondicao(c.nome);
        linhas.push([
          esc(i.nome), "<b>" + esc(c.nome) + "</b>" + (c.acumulos > 1 ? " ×" + c.acumulos : ""),
          c.turnos == null ? "<span class='suave'>sem contador</span>" : "<b>" + c.turnos + "</b>",
          esc(c.origem || "—"), esc(info.efeito || "") + " " + link("21", c.nome, "regra"),
        ]);
      }
    }
    return H.cartao("Condições ativas no combate",
      linhas.length
        ? H.tabela(["Em quem", "Qual", "Turnos", "Quem aplicou", "O que faz"], linhas) +
          "<p class='ajuda'>O contador desce 1 quando você marca <b>Já agiu</b> na casa do alvo — é o fim do " +
          "turno dele. Com 0 a condição sai sozinha. " + link("21", "21.5", "21.5") + "</p>"
        : vazio("Nenhuma condição ativa. Aplique pelo painel de cada combatente."),
      "condicoes-combate", "<span class='suave'>" + linhas.length + " ativa" + (linhas.length === 1 ? "" : "s") + "</span>");
  }

  function porInimigosEmCena() {
    const est = G.estado();
    const encontros = est.encontros || [];
    return H.cartao("Pôr inimigo em cena",
      "<div class='linha'><label class='sr-only' for='novo-inimigo'>Inimigo</label>" +
      "<select id='novo-inimigo'>" + G.opcoesDeInimigo(G.faixaN()) + "</select>" +
      "<input type='number' min='1' max='12' value='1' class='curto' id='qtd-inimigo' aria-label='Quantidade'>" +
      H.botao("por-inimigo", "Pôr em cena", { classe: "primario" }) + "</div>" +
      "<div class='linha'>" +
      H.campo("Criar pela âncora", "<select id='ancora-tipo' aria-label='Tipo'>" +
        G.TIPOS.map((t) => "<option" + (t === "Comum" ? " selected" : "") + ">" + t + "</option>").join("") + "</select>", "", "estreito") +
      H.campo("Faixa", "<select id='ancora-faixa' aria-label='Faixa'>" +
        C().mestre.ancoras.map((a) => "<option value='" + a.n + "'" + (a.n === G.faixaN() ? " selected" : "") + ">" +
          esc(a.faixa) + "</option>").join("") + "</select>", "", "estreito") +
      H.botao("por-ancora", "Criar em branco") + "</div>" +
      (encontros.length ? "<div class='linha'><label class='sr-only' for='carregar-encontro'>Encontro</label>" +
        "<select id='carregar-encontro'>" + encontros.map((e, i) => "<option value='" + i + "'>" +
          esc(e.nome || "Encontro " + (i + 1)) + "</option>").join("") + "</select>" +
        H.botao("carregar-encontro", "Carregar encontro") + "</div>" : "") +
      "<p class='ajuda'>O bestiário do capítulo 28 e os inimigos que você salvou aparecem na mesma lista. " +
      "A criação pela âncora copia os 13 números da faixa e do tipo (" + link("28", "28.3", "28.3") + ").</p>",
      "por-inimigo");
  }

  function telaCombate() {
    const est = G.estado(), cb = est.combate, g = G.grupo();
    const f = G.fila();
    const barra = H.cartao("Mesa de combate",
      "<div class='linha'>" +
      H.campo("Encontro", H.texto("g", "combate.nome", { rotulo: "Nome do encontro", ph: "Emboscada no Poço Sete" })) +
      H.campo("Ciclo", "<div class='ciclo-controle'>" + H.botao("ciclo", "−", { classe: "pequeno", dados: { v: -1 } }) +
        "<b class='ciclo-num'>" + (cb.ciclo || 1) + "</b>" + H.botao("ciclo", "+", { classe: "pequeno", dados: { v: 1 } }) +
        "</div>", "alvo de projeto: 3 a 5", "estreito") +
      "</div>" +
      "<div class='botoes'>" +
      H.botao("avancar-ciclo", "Avançar o Ciclo »", { classe: "primario",
        titulo: "Soma 1 no Ciclo, carrega os atrasos pendentes e limpa as marcas do Ciclo" }) +
      H.botao("novo-combate", "Novo combate", { titulo: "Limpa a cena e põe o PH do grupo no valor de início" }) +
      H.botao("encerrar-combate", "Encerrar", { classe: "perigo" }) +
      "</div>" +
      "<p class='ajuda'><b>Avançar o Ciclo</b> faz os 4 passos de uma vez: soma 1 no Ciclo, transforma o atraso " +
      "excedente em pendente para a remontagem, e apaga <i>já agiu</i>, atrasos e avanços deste Ciclo. " +
      link("19", "19.3", "19.3") + "</p>", "mesa-combate", "<span class='suave'>" + f.casas.length + " na Fila</span>");

    let fila;
    if (!f.casas.length) {
      fila = H.cartao("Fila de Ação", vazio("A Fila está vazia. Ponha o grupo em " +
        "<a href='#mestre/grupo'>Grupo</a> e um inimigo em cena abaixo."), "fila-vazia");
    } else {
      fila = H.cartao("Fila de Ação",
        "<ol class='fila'>" + f.casas.map((i) => casaDaFila(i, cb)).join("") + "</ol>" +
        (f.fora.length ? "<p class='ajuda'>Fora desta Fila: " + f.fora.map((i) => esc(i.nome) + " " +
          H.botao("voltar-pra-fila", "voltar", { classe: "pequeno", dados: { k: i.chave } })).join(" · ") + "</p>" : "") +
        "<p class='ajuda'>Ordem por VEL, com os desempates de 19.3. Atrasar soma casas brutas do Ciclo: " +
        "Elite e Boss dividem por 2 pela <b>Firmeza</b> (mínimo 1, teto 2) e Comum tem teto 3. " +
        "O que não couber vira pendente para a remontagem. " + link("19", "19.4", "19.4") + "</p>",
        "fila-cartao", "<b>Ciclo " + (cb.ciclo || 1) + "</b>");
    }

    const alvo = cb.alvo ? itemDaChave(cb.alvo) : null;
    const painelAlvo = !alvo ? "" : alvo.kind === "inimigo" ? painelDoInimigo(alvo.x) : painelDoPJ(alvo);

    const ph = G.recursoPH(g);
    app().innerHTML = topo("combate") + barra +
      (ph ? "<div class='faixa-ph'><span class='rotulo'>PH do grupo</span><b>" + ph.atual + " / " + ph.max + "</b>" +
        "<div class='botoes compactos'>" + H.botao("ph", "−1", { classe: "pequeno", dados: { v: -1 } }) +
        H.botao("ph", "+1", { classe: "pequeno", dados: { v: 1 } }) +
        H.botao("ph", "+" + ph.geracao + " (acertou o Básico)", { classe: "pequeno", dados: { v: ph.geracao } }) +
        "</div></div>" : "") +
      fila + painelAlvo + painelDeCondicoes() + porInimigosEmCena();
  }

  // ---------------------------------------------------------------------------
  // Inimigos: criador pela âncora, inimigos da campanha e bestiário
  // ---------------------------------------------------------------------------
  function editorDeInimigo(x, i) {
    const cam = "inimigos_salvos." + i;
    const marcas = (campo) => G.ELEMENTOS.map((e) =>
      "<label class='marca'><input type='checkbox' data-m='toggle-elemento-salvo' data-i='" + i +
      "' data-campo='" + campo + "' data-el='" + esc(e) + "'" + ((x[campo] || []).includes(e) ? " checked" : "") +
      "> <span>" + esc(e) + "</span></label>").join("");
    const corpo = "<div class='linha'>" +
      H.campo("Nome", H.texto("g", cam + ".nome", { rotulo: "Nome", ph: "Carcereiro da prisão orbital" })) +
      H.campo("Facção", H.texto("g", cam + ".faccao", { rotulo: "Facção" }), "", "estreito") +
      H.campo("Tipo", H.lista("g", cam + ".tipo", G.TIPOS, { rotulo: "Tipo", vazio: false }), "", "estreito") +
      "</div><div class='linha'>" +
      H.campo("PV", H.numero("g", cam + ".pv", { min: 1, rotulo: "PV" }), "é o custo no orçamento", "estreito") +
      H.campo("Defesa", H.numero("g", cam + ".defesa", { min: 0, rotulo: "Defesa" }), "", "estreito") +
      H.campo("RD", H.numero("g", cam + ".rd", { min: 0, rotulo: "RD" }), "", "estreito") +
      H.campo("Tenacidade", H.numero("g", cam + ".tenacidade", { min: 0, rotulo: "Tenacidade" }), "", "estreito") +
      H.campo("Velocidade", H.numero("g", cam + ".vel", { min: 0, rotulo: "Velocidade" }), "", "estreito") +
      "</div><div class='linha'>" +
      H.campo("Teste de Ataque", H.numero("g", cam + ".ataque", { rotulo: "Teste de Ataque" }), "", "estreito") +
      H.campo("Dano por acerto", H.texto("g", cam + ".dano", { rotulo: "Dano por acerto", ph: "4d8+1" }), "", "estreito") +
      H.campo("Média", H.numero("g", cam + ".dano_media", { min: 0, rotulo: "Média do dano" }), "", "estreito") +
      H.campo("DT dos efeitos", H.numero("g", cam + ".dt", { min: 0, rotulo: "DT dos efeitos" }), "", "estreito") +
      H.campo("TR dele", H.numero("g", cam + ".tr", { rotulo: "Teste de Resistência dele" }), "", "estreito") +
      "</div>" +
      "<div class='linha'><div class='campo'><span class='rotulo'>Fraquezas</span>" +
      "<div class='grade-marcas'>" + marcas("fraquezas") + "</div></div></div>" +
      "<div class='linha'><div class='campo'><span class='rotulo'>Resistências</span>" +
      "<div class='grade-marcas'>" + marcas("resistencias") + "</div></div></div>" +
      H.campo("Ações especiais e comportamento",
        H.texto("g", cam + ".fila", { area: true, linhas: 3, rotulo: "Comportamento na Fila",
          ph: "VEL 15, com Firmeza. Vai em quem está mais longe do grupo." }),
        "A régua de ações especiais está em " + link("28", "28.4", "28.4") +
        ": dano até 1,5× num alvo, ou o dano cheio por alvo em 2 ou 3 alvos, com recarga de 2 ou 3 Ciclos") +
      "<div class='acao-numeros'><span>Ataque " + botaoRolar(M.rolagem(x.ataque || 0), (x.nome || "Inimigo") + ": ataque") + "</span>" +
      (x.dano ? "<span>Dano " + botaoRolar(x.dano, (x.nome || "Inimigo") + ": dano") + "</span>" : "") + "</div>" +
      "<div class='botoes'>" +
      H.botao("por-salvo-em-cena", "Pôr em cena", { classe: "primario", dados: { i: i } }) +
      H.botao("duplicar-salvo", "Duplicar", { dados: { i: i } }) +
      H.botao("excluir-salvo", "Excluir", { classe: "perigo", dados: { i: i } }) +
      "</div>";
    return H.cartao(esc(x.nome || "Inimigo sem nome"), corpo, "inimigo-salvo",
      "<span class='suave'>" + esc(x.tipo) + " · faixa " + esc(x.faixa || "—") + " · " + (x.pv || 0) + " PV</span>");
  }

  function fichaDoBestiario(b) {
    const corpo =
      "<p class='suave'>" + esc([b.tipo, b.faccao, "faixa " + b.faixa].filter(Boolean).join(" · ")) +
      (b.fases > 1 ? " · <b>" + b.fases + " fases</b>" : "") + "</p>" +
      (b.frase ? "<p class='efeito'><i>" + esc(b.frase) + "</i></p>" : "") +
      "<div class='numeros compactos'>" +
      H.num("PV", b.pv) + H.num("Defesa", b.defesa) + H.num("RD", b.rd) +
      H.num("Tenacidade", b.tenacidade) + H.num("VEL", b.vel) +
      H.num("Ataque", sinal(b.ataque)) + H.num("DT", b.dt, "dos efeitos") + H.num("TR", sinal(b.tr), "dele") +
      "</div>" +
      "<p><b>Fraquezas:</b> " + (b.fraquezas.length ? b.fraquezas.map((e) => "<span class='etiqueta'>" + esc(e) + "</span>").join(" ") : "—") +
      (b.resistencias.length ? " &nbsp; <b>Resistências:</b> " + b.resistencias.map((e) =>
        "<span class='etiqueta ruim'>" + esc(e) + "</span>").join(" ") : "") + "</p>" +
      (b.ataques.length ? "<ul class='lista-acoes'>" + b.ataques.map((a) =>
        "<li><div><b>" + esc(a.nome) + "</b> <span class='suave'>" +
        esc([a.alcance, a.elemento].filter(Boolean).join(", ")) + "</span></div>" +
        "<div class='acao-numeros'><span>Ataque " + botaoRolar(M.rolagem(b.ataque), b.nome + ": " + a.nome) + "</span>" +
        (a.dados ? "<span>Dano " + botaoRolar(a.dados, b.nome + ": dano") + " <small>média " + a.media + "</small></span>" : "") +
        "</div></li>").join("") + "</ul>" : "") +
      (b.especiais.length ? "<h3>Ações especiais</h3><ul class='lista-acoes'>" + b.especiais.map((a) =>
        "<li><div><b>" + esc(a.nome) + "</b>" + (a.recarga ? " <span class='etiqueta'>" + esc(a.recarga) + "</span>" : "") +
        "</div><p class='efeito'>" + esc(a.efeito) + "</p></li>").join("") + "</ul>" : "") +
      (b.fila ? "<p class='ajuda'><b>Na Fila:</b> " + esc(b.fila) + "</p>" : "") +
      "<div class='botoes'>" +
      H.botao("por-bestiario-em-cena", "Pôr em cena", { classe: "primario", dados: { nome: b.nome } }) +
      H.botao("copiar-bestiario", "Copiar para os meus inimigos", { dados: { nome: b.nome } }) +
      "<a class='botao' href='" + esc(EG.Regras.href("28", b.nome)) + "'>Ficha completa no livro</a>" +
      "</div>";
    return H.cartao(esc(b.nome), corpo, "ficha-bicho",
      "<span class='etiqueta tipo-" + b.tipo.toLowerCase() + "'>" + esc(b.tipo) + "</span>");
  }

  function telaInimigos() {
    const est = G.estado(), fl = est.filtros;
    const q = EG.norm(fl.q || "");
    const lista = C().bestiario.filter((b) =>
      (!fl.faixa || String(b.faixa_n) === String(fl.faixa)) &&
      (!fl.tipo || b.tipo === fl.tipo) &&
      (!q || EG.norm(b.nome + " " + b.faccao + " " + b.fraquezas.join(" ")).includes(q)));

    const criador = H.cartao("Criar um inimigo pela âncora",
      "<p class='ajuda'>Escolha a faixa e o tipo, copie a linha, dê um nome e escolha as Fraquezas. " +
      "Nenhum campo exige conta. " + link("28", "28.4", "28.4") + "</p>" +
      "<div class='linha'>" +
      H.campo("Faixa", "<select id='criar-faixa' aria-label='Faixa'>" +
        C().mestre.ancoras.map((a) => "<option value='" + a.n + "'" + (a.n === G.faixaN() ? " selected" : "") + ">" +
          esc(a.faixa) + "</option>").join("") + "</select>", "a faixa é a do <b>grupo</b>", "estreito") +
      H.campo("Tipo", "<select id='criar-tipo' aria-label='Tipo'>" +
        G.TIPOS.map((t) => "<option" + (t === "Comum" ? " selected" : "") + ">" + t + "</option>").join("") +
        "</select>", "", "estreito") +
      H.campo("Nome", "<input type='text' id='criar-nome' placeholder='Carcereiro da prisão orbital' aria-label='Nome'>") +
      H.botao("criar-inimigo", "Criar", { classe: "primario" }) +
      "</div>" +
      "<h3>A linha da faixa " + esc(G.faixaTexto()) + "</h3>" + linhaDaAncora(G.faixaN()) +
      "<p class='ajuda'>Resistência é endurecimento e <b>não</b> entra no orçamento: um inimigo com " +
      "Resistência no Elemento certo é mais duro do que a ficha dele sugere. " + link("28", "28.2", "28.2") + "</p>",
      "criador");

    const meus = est.inimigos_salvos.length
      ? est.inimigos_salvos.map(editorDeInimigo).join("")
      : H.cartao("Inimigos da campanha",
        vazio("Nenhum inimigo seu ainda. Crie um pela âncora acima, ou copie uma ficha do bestiário."), "vazio");

    const filtros = H.cartao("Bestiário do capítulo 28",
      "<div class='linha'>" +
      H.campo("Faixa", H.lista("g", "filtros.faixa", C().mestre.ancoras.map((a) => [String(a.n), a.faixa]),
        { rotulo: "Faixa", vazio: "todas as faixas" }), "", "estreito") +
      H.campo("Tipo", H.lista("g", "filtros.tipo", G.TIPOS, { rotulo: "Tipo", vazio: "todos os tipos" }), "", "estreito") +
      H.campo("Procurar", H.texto("g", "filtros.q", { rotulo: "Procurar no bestiário", busca: true, vivo: true,
        ph: "nome, facção ou Fraqueza" })) +
      "</div>" +
      "<p class='ajuda'>" + lista.length + " de " + C().bestiario.length + " fichas. " +
      "Todas foram preenchidas pela tabela de âncoras, então você pode trocar as Fraquezas livremente para " +
      "cumprir o contrato de " + link("27", "27.5", "27.5") + ".</p>", "filtros-bestiario");

    app().innerHTML = topo("inimigos") + criador +
      "<h2 class='titulo-secao'>Inimigos da campanha</h2>" + meus +
      "<h2 class='titulo-secao'>Bestiário</h2>" + filtros +
      (lista.length ? "<div class='grade-bichos'>" + lista.map(fichaDoBestiario).join("") + "</div>"
        : H.cartao("Nada encontrado", vazio("Nenhuma ficha com esse filtro."), "vazio"));
  }

  // ---------------------------------------------------------------------------
  // Encontros
  // ---------------------------------------------------------------------------
  function cartaoOrcamento() {
    const o = C().mestre.orcamento;
    const f = G.faixaN();
    const linhas = o.map((x) => [
      (x.n === f ? "<b class='destaque'>" + esc(x.faixa) + "</b>" : esc(x.faixa)),
      String(x.dano_ciclo), "<b>" + x.orcamento + "</b>",
      String(x.custo.Comum), String(x.custo.Elite), String(x.custo.Boss),
    ]);
    return H.cartao("Orçamento de encontro",
      H.tabela(["Faixa", "Dano do grupo por Ciclo", "Orçamento", "Comum", "Elite", "Boss"], linhas) +
      "<p class='ajuda'>O <b>custo de um inimigo é o PV dele</b>. Comum vale 1/7 do orçamento, Elite 1/3 e Boss " +
      "85%. O alvo de projeto é <b>3 a 5 Ciclos</b>, com 4 no centro. " + link("27", "27.4", "27.4") + "</p>" +
      "<h3>As quatro composições equivalentes</h3>" +
      H.tabela(["Composição", "Como ela se sente na mesa", "Duração"],
        C().mestre.composicoes.map((c) => ["<b>" + esc(c.composicao) + "</b>", esc(c.sensacao), esc(c.duracao)])) +
      "<p class='ajuda'>Encontro de metade do orçamento é cena de passagem e deve durar 2 Ciclos: nem toda luta " +
      "precisa ser <i>a</i> luta.</p>", "orcamento", link("27", "27.4"));
  }

  /** Quem do grupo entra na cena. Encontro sem a lista salva conta o grupo inteiro. */
  function participantesDo(e, g) {
    if (!Array.isArray(e.participantes)) return g.slice();
    return g.filter((m) => e.participantes.indexOf(m.id) >= 0);
  }

  function escolhaDeParticipantes(e, i, g, emCena) {
    if (!g.length) {
      return vazio("Nenhuma ficha no grupo. <a href='#mestre/grupo'>Monte o grupo</a> para a tela ajustar o " +
        "orçamento a quem está na cena.");
    }
    const dentro = new Set(emCena.map((m) => m.id));
    return "<div class='participantes'>" + g.map((m) =>
      "<label class='marca'><input type='checkbox' data-m='toggle-participante' data-i='" + i +
      "' data-mid='" + esc(m.id) + "'" + (dentro.has(m.id) ? " checked" : "") + "> <span>" +
      esc(G.nome(m)) + (m.p.elemento ? " <span class='suave'>" + esc(m.p.elemento) + "</span>" : "") +
      "</span></label>").join("") + "</div>" +
      "<p class='ajuda'><b>" + emCena.length + " de " + g.length + "</b> na cena. " +
      (emCena.length === G.GRUPO_DE_REFERENCIA
        ? "É o grupo de " + G.GRUPO_DE_REFERENCIA + " para o qual o livro publica o orçamento (" +
          link("29", "29.1", "29.1") + ")."
        : "O orçamento do livro é para um grupo de <b>" + G.GRUPO_DE_REFERENCIA + "</b> (" +
          link("29", "29.1", "29.1") + "), porque o dano por Ciclo é uma ação agressiva por personagem. " +
          "Com " + emCena.length + " em cena, esta tela ajusta na mesma proporção — <b>é conta da tela, não " +
          "tabela do livro</b>.") + "</p>";
  }

  function cartaoEncontro(e, i, g) {
    const faixaN = Number(e.faixa_n) || G.faixaN();
    const emCena = participantesDo(e, g);
    const conta = G.contaDoEncontro(e.itens, faixaN, g.length ? emCena.length : null);
    const contrato = G.contratoDaFraqueza(e.itens, emCena);
    const cat = G.catalogoDeInimigos();
    const linhas = (e.itens || []).map((it, j) => {
      const t = cat.find((x) => x.ref === it.ref);
      return [
        t ? "<b>" + esc(t.nome) + "</b> <span class='suave'>" + esc(t.faccao || "") + "</span>" : "<span class='ruim'>ficha removida</span>",
        t ? esc(t.tipo) : "—", t ? esc(t.faixa) : "—",
        H.numero("g", "encontros." + i + ".itens." + j + ".qtd", { min: 1, max: 20, rotulo: "Quantidade" }),
        t ? "<b>" + (t.pv || 0) * (Number(it.qtd) || 1) + "</b> PV" : "—",
        H.botao("tirar-do-encontro", "×", { classe: "pequeno perigo", dados: { i: i, j: j }, titulo: "Tirar do encontro" }),
      ];
    });
    const pctClasse = conta.pct <= 60 ? "" : conta.pct <= 110 ? " medio" : " baixo";
    const corpo = "<div class='linha'>" +
      H.campo("Nome do encontro", H.texto("g", "encontros." + i + ".nome", { rotulo: "Nome do encontro", ph: "Emboscada no Poço Sete" })) +
      H.campo("Faixa", H.lista("g", "encontros." + i + ".faixa_n",
        C().mestre.ancoras.map((a) => [String(a.n), a.faixa]), { rotulo: "Faixa", vazio: false, num: true }), "", "estreito") +
      "</div>" +
      (linhas.length ? H.tabela(["Inimigo", "Tipo", "Faixa", "Qtd.", "Custo", ""], linhas)
        : vazio("Encontro vazio: ponha inimigos abaixo.")) +
      "<div class='linha'><label class='sr-only' for='add-enc-" + i + "'>Inimigo</label>" +
      "<select id='add-enc-" + i + "'>" + G.opcoesDeInimigo(faixaN) + "</select>" +
      H.botao("por-no-encontro", "Adicionar", { dados: { i: i } }) + "</div>" +
      "<h3>Quem do grupo entra nesta cena</h3>" + escolhaDeParticipantes(e, i, g, emCena) +
      "<div class='orcamento-leitura'>" +
      "<div><span class='rotulo'>Gasto</span><b>" + conta.custo + " / " + conta.orcamento_ajustado + " PV</b>" +
      "<div class='barra-pv'><span style='width:" + Math.min(100, conta.pct) + "%' class='" + pctClasse.trim() + "'></span></div>" +
      "<span class='sub'>" + conta.pct + "% do orçamento — " + esc(conta.leitura) + "</span></div>" +
      "<div><span class='rotulo'>Orçamento da faixa " + esc(C().mestre.ancoras[faixaN - 1].faixa) + "</span>" +
      "<b>" + conta.orcamento_ajustado + " PV</b>" +
      "<span class='sub'>" + (conta.ajustado
        ? "ajustado de " + conta.orcamento + " para " + conta.em_cena +
          (conta.em_cena === 1 ? " personagem" : " personagens")
        : "o número publicado, para um grupo de " + conta.referencia) + "</span></div>" +
      "<div><span class='rotulo'>Dano do grupo por Ciclo</span><b>" + conta.dpc_ajustado + "</b>" +
      "<span class='sub'>" + (conta.ajustado ? "de " + conta.dpc + " com " + conta.referencia + " personagens"
        : "o orçamento é esse dano em 4 Ciclos") + "</span></div>" +
      "<div><span class='rotulo'>Ações agressivas do inimigo por Ciclo</span><b>" + conta.acoes + "</b>" +
      "<span class='sub'>" + conta.n + (conta.n === 1 ? " inimigo" : " inimigos") + " em cena</span></div>" +
      "</div>" +
      "<div class='contrato " + (contrato.cumprido ? "ok" : "pendente") + "'>" +
      "<b>Contrato da Fraqueza: " + (contrato.cumprido ? "cumprido" : "não cumprido") + "</b> — " +
      (contrato.do_grupo.length
        ? contrato.cobertos.length + " de " + contrato.alvo + " Elementos do grupo aparecem como Fraqueza" +
          (contrato.faltam.length ? ". Fora da cena: <b>" + esc(contrato.faltam.join(", ")) + "</b>" : "") +
          (contrato.cumprido ? "." : ". Sem isso o combate dura cerca de <b>1 Ciclo a mais</b> — ferramenta " +
            "legítima de tensão, desde que você saiba que está usando ela.")
        : "nenhum personagem do grupo tem Elemento escolhido ainda.") +
      " " + link("27", "27.5", "27.5") +
      (contrato.resistencia_perigosa.length
        ? "<p class='ruim'>Atenção: Resistência apontada para o Elemento de dois personagens: <b>" +
          esc(contrato.resistencia_perigosa.join(", ")) + "</b>. Isso tira dois jogadores da luta sem " +
          "aparecer na ficha do inimigo.</p>" : "") +
      "</div>" +
      "<div class='botoes'>" +
      H.botao("carregar-no-combate", "Levar para o combate »", { classe: "primario", dados: { i: i } }) +
      H.botao("duplicar-encontro", "Duplicar", { dados: { i: i } }) +
      H.botao("excluir-encontro", "Excluir", { classe: "perigo", dados: { i: i } }) +
      "</div>";
    return H.cartao(esc(e.nome || "Encontro " + (i + 1)), corpo, "encontro",
      "<span class='suave'>" + conta.custo + " PV · " + conta.pct + "% do orçamento</span>");
  }

  function telaEncontros() {
    const est = G.estado(), g = G.grupo();
    const fraqueza = H.cartao("Descobrir uma Fraqueza",
      H.tabela(["Faixa do inimigo", "DT"], C().mestre.dt_fraqueza.map((x) => [
        (x.faixa === G.faixaTexto() ? "<b class='destaque'>" + esc(x.faixa) + "</b>" : esc(x.faixa)), "<b>" + x.dt + "</b>",
      ])) +
      "<p class='ajuda'>DT fixa por faixa do <b>inimigo</b>, uma das cinco DTs de subsistema: ela não escala com " +
      "o nível do grupo de propósito, porque é rotina de quase todo combate. " + link("27", "27.3", "27.3") + "</p>" +
      "<p><b>Elementos do grupo:</b> " + (G.elementosDoGrupo(g).length
        ? G.elementosDoGrupo(g).map((e) => "<span class='etiqueta'>" + esc(e) + "</span>").join(" ")
        : "<span class='suave'>nenhum</span>") + "</p>", "dt-fraqueza");

    app().innerHTML = topo("encontros") +
      "<div class='botoes'>" + H.botao("novo-encontro", "+ Novo encontro", { classe: "primario" }) + "</div>" +
      (est.encontros.length
        ? est.encontros.map((e, i) => cartaoEncontro(e, i, g)).join("")
        : H.cartao("Nenhum encontro montado",
          vazio("Monte um encontro para ver o custo contra o orçamento da faixa e a conferência do contrato " +
            "da Fraqueza. Depois é um clique para levar a cena para a mesa de combate."), "vazio")) +
      "<div class='grade-mestre duas'><div class='coluna'>" + cartaoOrcamento() + "</div>" +
      "<div class='coluna'>" + fraqueza + "</div></div>";
  }


  // ---------------------------------------------------------------------------
  // Ações
  // ---------------------------------------------------------------------------
  const A = G.acoes;
  const el = (id) => document.getElementById(id);
  const lerNum = (id) => {
    const e = el(id), n = e ? Math.floor(Number(e.value)) : 0;
    return Number.isFinite(n) && n > 0 ? n : 0;
  };
  const lerVal = (id) => (el(id) ? el(id).value : "");
  const marcado = (id) => !!(el(id) && el(id).checked);

  // --- Aviso, mesa, arquivos -------------------------------------------------
  A["dispensar-aviso"] = () => { G.estado().aviso_lido = true; };
  A["rever-aviso"] = () => { G.estado().aviso_lido = false; };

  A["exportar-mesa"] = () => {
    const est = G.estado();
    const nome = (est.campanha.nome || "mesa").normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      .replace(/[^\w-]+/g, "-").replace(/^-+|-+$/g, "").toLowerCase();
    const blob = new Blob([JSON.stringify(est, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "mesa-do-mestre-" + (nome || "campanha") + ".json";
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    EG.toast("Mesa exportada. O arquivo é o seu backup — as fichas se exportam uma a uma, na aba Jogar.");
    return false;
  };

  A["importar-mesa"] = () => { el("arquivo-mesa").click(); return false; };
  A["importar-ficha"] = () => { el("arquivo-ficha-mestre").click(); return false; };
  A["exportar-tudo"] = () => { EG.exportarTudo(); return false; };
  A["importar-tudo"] = () => { el("arquivo-backup").click(); return false; };

  A["zerar-mesa"] = () => {
    if (!confirm("Apagar a mesa do Mestre deste navegador? Campanha, inimigos, encontros e tesouro se " +
      "perdem. As fichas dos jogadores NÃO são apagadas.\n\n(Exporte antes, se quiser guardar.)")) return false;
    G.zerar();
    EG.toast("Mesa apagada. As fichas dos jogadores continuam salvas.");
  };

  A["imprimir"] = () => { window.print(); return false; };

  A["usar-nivel-do-grupo"] = () => {
    const n = G.nivelGrupo();
    if (n) G.estado().campanha.nivel = n;
  };

  A["rolar-livre"] = () => {
    const v = lerVal("rolagem-livre").trim();
    if (!v) { EG.toast("Escreva a rolagem, como <code>3d8+2</code>.", "erro"); return false; }
    if (!EG.rolar(v, { rotulo: "Mestre: " + v })) EG.toast("Não entendi <b>" + esc(v) + "</b>. Use <code>NdF+M</code>.", "erro");
    return false;
  };

  // --- Grupo -----------------------------------------------------------------
  A["ph"] = (b) => {
    const r = G.recursoPH();
    if (!r) { EG.toast("Ponha fichas no grupo para controlar o PH.", "erro"); return false; }
    const v = b.dataset.v;
    const novo = G.definirPH(v === "max" ? r.max : v === "inicio" ? r.inicio : r.atual + Number(v));
    EG.toast("PH do grupo: <b>" + novo + " / " + r.max + "</b> (gravado nas fichas).");
  };

  A["descanso-curto"] = () => {
    const n = G.descanso("curto");
    EG.toast(n ? "Descanso Curto em " + n + (n > 1 ? " fichas" : " ficha") + ": cada um recuperou 2 × nível + Vigor."
      : "Nenhuma ficha no grupo.", n ? "" : "erro");
  };

  A["descanso-longo"] = () => {
    const n = G.descanso("longo");
    EG.toast(n ? "Descanso Longo em " + n + (n > 1 ? " fichas" : " ficha") + ": PV cheios, condições removidas, " +
      "usos e Esforço de volta." : "Nenhuma ficha no grupo.", n ? "" : "erro");
  };

  A["por-no-grupo"] = () => {
    const id = lerVal("nova-ficha");
    if (!id) return false;
    const est = G.estado();
    if (!est.grupo.includes(id)) est.grupo.push(id);
  };

  A["por-todas"] = () => {
    const est = G.estado();
    for (const m of G.foraDoGrupo()) if (!est.grupo.includes(m.id)) est.grupo.push(m.id);
  };

  A["tirar-do-grupo"] = (b) => {
    const est = G.estado(), i = est.grupo.indexOf(b.dataset.mid);
    if (i >= 0) est.grupo.splice(i, 1);
    EG.toast("Tirado do grupo. A ficha continua salva no navegador.");
  };

  A["subir"] = (b) => {
    const est = G.estado(), i = est.grupo.indexOf(b.dataset.mid), j = i + Number(b.dataset.v);
    if (i < 0 || j < 0 || j >= est.grupo.length) return false;
    est.grupo.splice(j, 0, est.grupo.splice(i, 1)[0]);
  };

  A["exemplo-nadir"] = () => {
    const p = F.exemploNadir();
    EG.Armazem.salvar(p);
    G.estado().grupo.push(p.id);
    EG.toast("Nadir (exemplo do 29.7) entrou no grupo.");
  };

  A["dano-pj"] = (b) => {
    const m = G.membro(b.dataset.mid);
    const v = lerNum("dano-" + b.dataset.mid);
    if (!m || !v) { EG.toast("Digite quanto de dano ele sofreu.", "erro"); return false; }
    const r = G.aplicarDano(m, v, marcado("cont-" + b.dataset.mid));
    if (r) EG.toast(r.msg);
  };

  A["curar-pj"] = (b) => {
    const m = G.membro(b.dataset.mid);
    const v = lerNum("dano-" + b.dataset.mid);
    if (!m || !v) { EG.toast("Digite quanto ele cura.", "erro"); return false; }
    const r = G.curar(m, v);
    if (r) EG.toast(r.msg);
  };

  A["energia-pj"] = (b) => {
    const m = G.membro(b.dataset.mid);
    if (m) G.energia(m, Number(b.dataset.v));
  };

  A["rolar-morrendo"] = (b) => {
    const m = G.membro(b.dataset.mid);
    if (!m) return false;
    const j = m.p.jogo, R = m.R;
    const r = EG.rolar(M.rolagem(R.morrendo_bonus), { rotulo: G.nome(m) + ": Teste de Morrendo (DT 10)",
      vantagem: R.morrendo_vantagem });
    if (!r) return false;
    if (r.natural === 20) { j.pv = 1; j.morrendo = { s: 0, f: 0 }; EG.toast("20 natural: " + esc(G.nome(m)) + " se levanta com 1 PV!"); }
    else {
      if (r.natural === 1) j.morrendo.f += 2;
      else if (r.total >= 10) j.morrendo.s += 1;
      else j.morrendo.f += 1;
      if (j.morrendo.s >= 3) { j.pv = 1; j.morrendo = { s: 0, f: 0 }; EG.toast("3 sucessos: " + esc(G.nome(m)) + " estabiliza com 1 PV."); }
      else if (j.morrendo.f >= 3) EG.toast("3 falhas: " + esc(G.nome(m)) + " morre.", "erro");
    }
    G.gravarFicha(m);
  };

  A["por-cond-pj"] = (b) => {
    const m = G.membro(b.dataset.mid);
    const nome = lerVal("cond-" + b.dataset.mid);
    if (!m || !nome) return false;
    const t = lerNum("cond-t-" + b.dataset.mid);
    G.porCondicao(m.p.jogo.condicoes, nome, t || null, "Mestre");
    G.gravarFicha(m);
  };

  A["tirar-cond-pj"] = (b) => {
    const m = G.membro(b.dataset.mid);
    if (!m) return false;
    m.p.jogo.condicoes.splice(Number(b.dataset.i), 1);
    G.gravarFicha(m);
  };

  A["cond-turno"] = (b) => {
    const m = G.membro(b.dataset.mid);
    if (!m) return false;
    const c = m.p.jogo.condicoes[Number(b.dataset.i)];
    if (!c) return false;
    c.turnos = Math.max(0, (c.turnos || 0) + Number(b.dataset.v));
    if (c.turnos === 0) m.p.jogo.condicoes.splice(Number(b.dataset.i), 1);
    G.gravarFicha(m);
  };

  A["invocar-memo"] = (b) => {
    const m = G.membro(b.dataset.mid);
    if (!m || !m.R.memo) return false;
    const r = G.recursoPH();
    if (r && r.atual < 1) { EG.toast("Invocar custa 1 PH e o grupo está sem PH.", "erro"); return false; }
    if (r) G.definirPH(r.atual - 1);
    const m2 = G.membro(b.dataset.mid);
    m2.p.jogo.memo_ativo = true;
    m2.p.jogo.memo_pv = m2.R.memo.pv;
    G.gravarFicha(m2);
    EG.toast("Memoespírito de " + esc(G.nome(m2)) + " em campo: Ação Complementar e −1 PH. Ele ganha casa própria na Fila.");
  };

  A["dispensar-memo"] = (b) => {
    const m = G.membro(b.dataset.mid);
    if (!m) return false;
    m.p.jogo.memo_ativo = false;
    G.gravarFicha(m);
  };

  // --- Combate ---------------------------------------------------------------
  A["ciclo"] = (b) => {
    const cb = G.estado().combate;
    cb.ciclo = Math.max(1, (cb.ciclo || 1) + Number(b.dataset.v));
    cb.ativo = true;
  };

  A["avancar-ciclo"] = () => {
    const r = G.avancarCiclo();
    G.estado().combate.ativo = true;
    EG.toast("<b>Ciclo " + r.ciclo + ".</b> Fila remontada: atrasos excedentes viraram pendentes e as marcas do " +
      "Ciclo foram limpas. As condições descontam no fim do turno de cada um (botão <b>Já agiu</b>).");
  };

  A["novo-combate"] = () => {
    const nome = G.estado().combate.nome;
    if (G.estado().combate.inimigos.length && !confirm("Começar um combate novo? Os inimigos em cena saem e o " +
      "PH do grupo volta ao valor de início.")) return false;
    const n = G.novoCombate(nome);
    EG.toast("Novo combate: Ciclo 1, PH do grupo no valor de início em " + n + (n === 1 ? " ficha" : " fichas") +
      ", acúmulos zerados.");
  };

  A["encerrar-combate"] = () => {
    const cb = G.estado().combate;
    cb.ativo = false;
    cb.inimigos = [];
    cb.cc = {};
    cb.alvo = "";
    EG.toast("Combate encerrado. Vá em <b>Recompensas</b> para o que a cena entrega.");
  };

  A["agiu"] = (b) => {
    const chave = b.dataset.k, cc = G.cc(chave);
    const i = itemDaChave(chave);
    cc.agiu = !cc.agiu;
    if (cc.agiu && !cc.descontou) {
      cc.descontou = true;
      let saiu = [];
      if (i && i.kind === "inimigo") saiu = G.fimDeTurno(i.x.condicoes, i.x);
      else if (i && i.kind === "pj") { saiu = G.fimDeTurno(i.m.p.jogo.condicoes); G.gravarFicha(i.m); }
      if (saiu.length) EG.toast("Fim do turno de " + esc(i.nome) + ": saiu <b>" + esc(saiu.join(", ")) + "</b>.");
    } else if (!cc.agiu && cc.descontou) {
      cc.descontou = false;
      if (i && i.kind === "inimigo") G.desfazerFimDeTurno(i.x.condicoes);
      else if (i && i.kind === "pj") { G.desfazerFimDeTurno(i.m.p.jogo.condicoes); G.gravarFicha(i.m); }
    }
  };

  A["atrasar"] = (b) => {
    const cc = G.cc(b.dataset.k);
    cc.atraso = Math.max(0, (cc.atraso || 0) + Number(b.dataset.v));
    const i = itemDaChave(b.dataset.k);
    if (i) {
      const tipo = i.kind === "inimigo" ? i.tipo : "Comum";
      const casas = G.casasAtraso((cc.atraso || 0) + (cc.pendente || 0), tipo);
      const regra = C().mestre.atraso_tipo.find((y) => y.tipo === tipo) || { teto: 3, firmeza: "Não" };
      EG.toast(esc(i.nome) + ": " + ((cc.atraso || 0) + (cc.pendente || 0)) + " casas brutas no Ciclo valem " +
        "<b>" + casas + (casas === 1 ? " casa" : " casas") + "</b>" +
        (regra.firmeza === "Sim" ? " (Firmeza: metade, mínimo 1, teto " + regra.teto + ")"
          : " (teto " + regra.teto + ", sem Firmeza)") + ".");
    }
  };

  A["avancar"] = (b) => {
    const cc = G.cc(b.dataset.k);
    if (cc.agiu) { EG.toast("Avançar só funciona em quem ainda não agiu neste Ciclo (19.5).", "erro"); return false; }
    cc.avanco = Math.max(0, (cc.avanco || 0) + Number(b.dataset.v));
  };

  A["avanco-total"] = (b) => {
    const cc = G.cc(b.dataset.k);
    cc.avanco_total = !cc.avanco_total;
    if (cc.avanco_total) EG.toast("Avanço Total: age logo depois do turno atual. No máximo 1 por Ciclo por criatura (19.5).");
  };

  A["escolher-alvo"] = (b) => {
    const cb = G.estado().combate;
    cb.alvo = cb.alvo === b.dataset.k ? "" : b.dataset.k;
  };

  A["fora-da-fila"] = (b) => { G.cc(b.dataset.k).participa = false; };
  A["voltar-pra-fila"] = (b) => { G.cc(b.dataset.k).participa = true; };

  A["dano-inimigo"] = (b) => {
    const x = inimigoPorUid(b.dataset.uid);
    const v = lerNum("dano-i-" + b.dataset.uid);
    if (!x || !v) { EG.toast("Digite o dano bruto.", "erro"); return false; }
    const r = G.danoNoInimigo(x, v, { continuo: marcado("cont-i-" + b.dataset.uid) });
    EG.toast(esc(x.nome || "Inimigo") + ": " + v + (r.rd ? " − RD " + r.rd : "") + " = <b>" + r.entrou + "</b> · PV " +
      x.pv + "/" + x.pv_max + (r.caiu ? " · <b>derrotado</b> (+10 de Energia para quem derrubou)" : ""));
  };

  A["curar-inimigo"] = (b) => {
    const x = inimigoPorUid(b.dataset.uid);
    const v = lerNum("dano-i-" + b.dataset.uid);
    if (!x || !v) return false;
    x.pv = Math.min(x.pv_max, (x.pv == null ? x.pv_max : x.pv) + v);
  };

  A["aplicar-rt"] = (b) => {
    const x = inimigoPorUid(b.dataset.uid);
    if (!x) return false;
    const rt = G.estado().combate.rt;
    const m = rt.quem ? G.membro(rt.quem) : null;
    const ef = m ? m.R.eficiencia : M.eficiencia(G.nivel());
    const fonte = G.FONTES_RT.find((f) => f.id === rt.fonte) || G.FONTES_RT[0];
    const elemento = rt.elemento || (m ? m.p.elemento : "");
    const relacao = G.relacaoElemento(x, elemento);
    const reducao = G.reducaoTenacidade(fonte.base, relacao);
    if (!reducao) {
      EG.toast("<b>" + esc(fonte.rotulo) + "</b> não reduz Tenacidade: só ataque reduz (20.3).");
      return false;
    }
    x.reducao = Math.min(x.tenacidade || 0, (x.reducao || 0) + reducao);
    let msg = esc(x.nome || "Inimigo") + ": " + esc(fonte.rotulo) + " (" + fonte.base + ")" +
      (elemento ? " com " + esc(elemento) + " — " + relacao : "") + " reduz <b>−" + reducao + "</b> · Tenacidade " +
      G.tenacidadeAtual(x) + "/" + (x.tenacidade || 0);
    if (G.tenacidadeAtual(x) === 0 && !x.quebrado) {
      const q = G.quebrar(x, elemento, ef);
      const cc = G.cc("i:" + x.uid);
      cc.atraso = (cc.atraso || 0) + 1;
      if (m) G.energia(m, 10);
      msg += "<br><b>Quebra!</b> " + (q
        ? "Dano de " + esc(elemento) + ": " + botaoRolar(q.texto, "Dano de Quebra de " + elemento) +
          " (média " + q.media + ", sofre RD) + <b>" + esc(q.efeito) + "</b>. "
        : "") + "Atraso de 1 casa e <b>Quebrado</b> até o fim do próximo turno dele" +
        (m ? ". <b>+10 de Energia</b> para " + esc(G.nome(m)) + "."
          : ". Diga em <b>Quem reduziu</b> quem quebrou para os <b>+10 de Energia</b> entrarem na ficha dele.");
    }
    EG.toast(msg, "rolagem");
  };

  A["virar-fase"] = (b) => {
    const x = inimigoPorUid(b.dataset.uid);
    if (!x) return false;
    if (x.fase >= x.fases) { EG.toast("Ele já está na última fase.", "erro"); return false; }
    x.fase += 1;
    x.reducao = 0;
    x.quebrado = false;
    x.condicoes = (x.condicoes || []).filter((c) => c.nome !== "Quebrado");
    EG.toast("<b>" + esc(x.nome) + " — fase " + x.fase + " de " + x.fases + ".</b> Tenacidade cheia de novo. " +
      "Troque as Fraquezas no painel e <b>anuncie em voz alta</b>: esconder isso transforma a fase nova em " +
      "adivinhação. A virada não gasta a ação dele (28.5).");
  };

  A["toggle-elemento"] = (b) => {
    const x = inimigoPorUid(b.dataset.uid);
    if (!x) return false;
    const campo = b.dataset.campo, e = b.dataset.el;
    x[campo] = x[campo] || [];
    const i = x[campo].indexOf(e);
    if (i >= 0) x[campo].splice(i, 1);
    else {
      x[campo].push(e);
      const outro = campo === "fraquezas" ? "resistencias" : "fraquezas";
      x[outro] = (x[outro] || []).filter((y) => y !== e);
    }
  };

  A["por-cond-i"] = (b) => {
    const x = inimigoPorUid(b.dataset.uid);
    const nome = lerVal("cond-i-" + b.dataset.uid).replace(" (só inimigos)", "");
    if (!x || !nome) return false;
    G.porCondicao(x.condicoes, nome, lerNum("cond-it-" + b.dataset.uid) || null, "Mestre");
  };

  A["tirar-cond-i"] = (b) => {
    const x = inimigoPorUid(b.dataset.uid);
    if (x) x.condicoes.splice(Number(b.dataset.i), 1);
  };

  A["cond-turno-i"] = (b) => {
    const x = inimigoPorUid(b.dataset.uid);
    if (!x) return false;
    const c = x.condicoes[Number(b.dataset.i)];
    if (!c) return false;
    c.turnos = Math.max(0, (c.turnos || 0) + Number(b.dataset.v));
    if (c.turnos === 0) x.condicoes.splice(Number(b.dataset.i), 1);
  };

  function porEmCena(x, aviso) {
    if (!x) return false;
    const cb = G.estado().combate;
    const iguais = cb.inimigos.filter((y) => (y.nome || "").replace(/ \d+$/, "") === (x.nome || "")).length;
    if (iguais) x.nome = (x.nome || "Inimigo") + " " + (iguais + 1);
    cb.inimigos.push(x);
    cb.ativo = true;
    cb.alvo = "i:" + x.uid;
    if (aviso !== false) EG.toast("<b>" + esc(x.nome) + "</b> entrou na cena com " + x.pv_max + " PV. " +
      "Ele entra na Fila pela VEL " + x.vel + " (19.7).");
    return true;
  }

  A["por-inimigo"] = () => {
    const ref = lerVal("novo-inimigo");
    const qtd = Math.max(1, Math.min(12, lerNum("qtd-inimigo") || 1));
    let n = 0;
    for (let i = 0; i < qtd; i++) if (porEmCena(G.inimigoDaRef(ref), false)) n++;
    EG.toast(n ? n + (n === 1 ? " inimigo entrou" : " inimigos entraram") + " na cena." : "Não achei essa ficha.",
      n ? "" : "erro");
    if (!n) return false;
  };

  A["por-ancora"] = () => {
    porEmCena(G.inimigoDaAncora(Number(lerVal("ancora-faixa")) || G.faixaN(), lerVal("ancora-tipo") || "Comum",
      lerVal("ancora-tipo") + " da faixa " + G.faixaTexto(Number(lerVal("ancora-faixa")))));
  };

  A["carregar-encontro"] = () => {
    const i = Number(lerVal("carregar-encontro"));
    carregarEncontro(i);
  };

  function carregarEncontro(i) {
    const e = G.estado().encontros[i];
    if (!e) return false;
    const cb = G.estado().combate;
    cb.nome = e.nome || cb.nome;
    cb.inimigos = [];
    cb.cc = {};
    cb.ciclo = 1;
    cb.ativo = true;
    // Quem ficou fora do encontro já entra fora da Fila (19.3).
    let fora = 0;
    if (Array.isArray(e.participantes)) {
      for (const m of G.grupo()) {
        if (e.participantes.indexOf(m.id) < 0) { G.cc("p:" + m.id).participa = false; fora++; }
      }
    }
    let n = 0;
    for (const it of e.itens || []) {
      for (let k = 0; k < Math.max(1, Number(it.qtd) || 1); k++) {
        const x = G.inimigoDaRef(it.ref);
        if (!x) continue;
        const iguais = cb.inimigos.filter((y) => (y.nome || "").replace(/ \d+$/, "") === (x.nome || "")).length;
        if (iguais) x.nome = (x.nome || "Inimigo") + " " + (iguais + 1);
        cb.inimigos.push(x);
        n++;
      }
    }
    cb.alvo = "";
    EG.toast("<b>" + esc(e.nome || "Encontro") + "</b> na mesa: " + n + (n === 1 ? " inimigo" : " inimigos") +
      ", Ciclo 1" + (fora ? ", e " + fora + (fora === 1 ? " personagem fora" : " personagens fora") +
        " da Fila (quem você não marcou na cena)" : "") +
      ". Confira a Surpresa antes de montar a Fila (19.3).");
    return true;
  }

  // --- Inimigos --------------------------------------------------------------
  A["criar-inimigo"] = () => {
    const faixaN = Number(lerVal("criar-faixa")) || G.faixaN();
    const tipo = lerVal("criar-tipo") || "Comum";
    const x = G.inimigoDaAncora(faixaN, tipo, lerVal("criar-nome").trim() ||
      (tipo + " da faixa " + G.faixaTexto(faixaN)));
    G.estado().inimigos_salvos.unshift(x);
    EG.toast("<b>" + esc(x.nome) + "</b> criado com os números da faixa " + esc(x.faixa) + ". " +
      "Agora escolha as Fraquezas (" + (C().mestre.fraquezas_tipo.find((y) => y.tipo === tipo) || {}).fraquezas +
      " para " + esc(tipo) + ") e escreva as ações.");
  };

  A["toggle-elemento-salvo"] = (b) => {
    const x = G.estado().inimigos_salvos[Number(b.dataset.i)];
    if (!x) return false;
    const campo = b.dataset.campo, e = b.dataset.el;
    x[campo] = x[campo] || [];
    const i = x[campo].indexOf(e);
    if (i >= 0) x[campo].splice(i, 1);
    else {
      x[campo].push(e);
      const outro = campo === "fraquezas" ? "resistencias" : "fraquezas";
      x[outro] = (x[outro] || []).filter((y) => y !== e);
    }
  };

  A["por-salvo-em-cena"] = (b) => {
    const x = G.estado().inimigos_salvos[Number(b.dataset.i)];
    if (!x || !porEmCena(G.inimigoSalvo(x.uid))) return false;
    G.salvar();
    location.hash = "#mestre/combate";
    return false;
  };

  A["duplicar-salvo"] = (b) => {
    const est = G.estado(), x = EG.clonar(est.inimigos_salvos[Number(b.dataset.i)]);
    x.uid = EG.uid();
    x.nome = (x.nome || "Inimigo") + " (cópia)";
    est.inimigos_salvos.splice(Number(b.dataset.i) + 1, 0, x);
  };

  A["excluir-salvo"] = (b) => {
    const est = G.estado(), x = est.inimigos_salvos[Number(b.dataset.i)];
    if (x && x.nome && !confirm("Excluir " + x.nome + "?")) return false;
    est.inimigos_salvos.splice(Number(b.dataset.i), 1);
  };

  A["por-bestiario-em-cena"] = (b) => {
    if (!porEmCena(G.inimigoDoBestiario(b.dataset.nome))) return false;
    G.salvar();
    location.hash = "#mestre/combate";
    return false;
  };

  A["copiar-bestiario"] = (b) => {
    const x = G.inimigoDoBestiario(b.dataset.nome);
    if (!x) return false;
    G.estado().inimigos_salvos.unshift(x);
    EG.toast("<b>" + esc(x.nome) + "</b> copiado para os seus inimigos: troque o que quiser sem mexer no livro.");
  };

  // --- Encontros -------------------------------------------------------------
  A["novo-encontro"] = () => {
    G.estado().encontros.unshift({ nome: "", faixa_n: G.faixaN(), itens: [],
      participantes: G.estado().grupo.slice() });
  };

  A["toggle-participante"] = (b) => {
    const e = G.estado().encontros[Number(b.dataset.i)];
    if (!e) return false;
    const id = b.dataset.mid;
    // Encontro antigo, sem a lista: começa do grupo inteiro e tira quem foi desmarcado.
    if (!Array.isArray(e.participantes)) e.participantes = G.estado().grupo.slice();
    const j = e.participantes.indexOf(id);
    if (j >= 0) e.participantes.splice(j, 1);
    else e.participantes.push(id);
  };

  A["por-no-encontro"] = (b) => {
    const i = Number(b.dataset.i), e = G.estado().encontros[i];
    const ref = lerVal("add-enc-" + i);
    if (!e || !ref) return false;
    const atual = e.itens.find((x) => x.ref === ref);
    if (atual) atual.qtd = (Number(atual.qtd) || 1) + 1;
    else e.itens.push({ ref: ref, qtd: 1 });
  };

  A["tirar-do-encontro"] = (b) => {
    const e = G.estado().encontros[Number(b.dataset.i)];
    if (e) e.itens.splice(Number(b.dataset.j), 1);
  };

  A["duplicar-encontro"] = (b) => {
    const est = G.estado(), e = EG.clonar(est.encontros[Number(b.dataset.i)]);
    if (!e) return false;
    e.nome = (e.nome || "Encontro") + " (cópia)";
    est.encontros.splice(Number(b.dataset.i) + 1, 0, e);
  };

  A["excluir-encontro"] = (b) => {
    const est = G.estado(), e = est.encontros[Number(b.dataset.i)];
    if (e && (e.itens || []).length && !confirm("Excluir " + (e.nome || "este encontro") + "?")) return false;
    est.encontros.splice(Number(b.dataset.i), 1);
  };

  A["carregar-no-combate"] = (b) => {
    if (!carregarEncontro(Number(b.dataset.i))) return false;
    G.salvar();
    location.hash = "#mestre/combate";
    return false;
  };

  // --- Recompensas -----------------------------------------------------------
  A["por-tesouro"] = () => {
    G.estado().tesouro.push({ o_que: "", de_onde: G.estado().combate.nome || "", para_quem: "" });
  };

  A["tirar-tesouro"] = (b) => { G.estado().tesouro.splice(Number(b.dataset.i), 1); };

  // ---------------------------------------------------------------------------
  // Eventos soltos da Área do Mestre
  // ---------------------------------------------------------------------------
  document.addEventListener("change", (ev) => {
    if (ev.target.id === "tamanho-grupo") {
      const n = G.definirTamanho(Number(ev.target.value));
      const r = G.recursoPH();
      EG.toast("Grupo de <b>" + n + "</b>: PH máximo " + (r ? r.max : "—") + ", começa o combate com " +
        (r ? r.inicio : "—") + " (16.2). Gravado em todas as fichas.");
      G.redesenhar();
    }
    if (ev.target.id === "arquivo-mesa" && ev.target.files[0]) importarMesa(ev.target.files[0]);
    if (ev.target.id === "arquivo-ficha-mestre" && ev.target.files[0]) importarFicha(ev.target.files[0]);
  });

  function importarMesa(arquivo) {
    const leitor = new FileReader();
    leitor.onload = () => {
      try {
        const bruto = JSON.parse(leitor.result);
        if (!bruto || typeof bruto !== "object" || !("campanha" in bruto) || !("combate" in bruto)) throw new Error("formato");
        if (!confirm("Substituir a mesa deste navegador pela do arquivo? As fichas dos jogadores não são tocadas."))
          return;
        const novo = G.completar(bruto);
        novo.semeado = true;
        localStorage.setItem(G.CHAVE, JSON.stringify(novo));
        location.reload();
      } catch (_) {
        EG.toast("Esse arquivo não é uma mesa do Mestre deste site.", "erro");
      }
    };
    leitor.readAsText(arquivo);
  }

  function importarFicha(arquivo) {
    const leitor = new FileReader();
    leitor.onload = () => {
      try {
        const p = JSON.parse(leitor.result);
        if (!p || typeof p !== "object" || !("atributos" in p) || !("jogo" in p)) throw new Error("formato");
        const todas = EG.Armazem.todas();
        if (!p.id || todas[p.id]) {
          if (!(p.id && todas[p.id] && confirm("Já existe esta ficha no navegador. Substituir pela do arquivo?\n" +
            "(Cancelar importa como uma cópia.)"))) p.id = EG.uid();
        }
        const completa = F.completar(p);
        EG.Armazem.salvar(completa);
        const est = G.estado();
        if (!est.grupo.includes(completa.id)) est.grupo.push(completa.id);
        G.salvar();
        EG.toast("Ficha de <b>" + esc(completa.nome || "sem nome") + "</b> importada e posta no grupo.");
        G.redesenhar();
      } catch (_) {
        EG.toast("Esse arquivo não é uma ficha deste site.", "erro");
      }
    };
    leitor.readAsText(arquivo);
  }

  // Enter nos campos de valor
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "Enter") return;
    const id = ev.target.id || "";
    if (id === "rolagem-livre") { ev.preventDefault(); A["rolar-livre"](); }
    else if (/^dano-i-/.test(id)) {
      ev.preventDefault();
      const b = document.querySelector("[data-m='dano-inimigo'][data-uid='" + id.slice(7) + "']");
      if (b) b.click();
    } else if (/^dano-/.test(id)) {
      ev.preventDefault();
      const b = document.querySelector("[data-m='dano-pj'][data-mid='" + id.slice(5) + "']");
      if (b) b.click();
    }
  });

  G.telas.painel = telaPainel;
  G.telas.grupo = telaGrupo;
  G.telas.combate = telaCombate;
  G.telas.inimigos = telaInimigos;
  G.telas.encontros = telaEncontros;
})();