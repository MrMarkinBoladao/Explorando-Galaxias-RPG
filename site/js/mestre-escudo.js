/*
 * mestre-escudo.js — As telas de consulta da Área do Mestre: Recompensas (o calendário de
 * marco do 27.8) e o Escudo do Mestre (as tabelas que o Mestre mais olha na mesa).
 * Nenhuma das duas muda o combate: elas só leem o livro e as fichas do grupo.
 */
(function () {
  "use strict";

  const EG = window.EG;
  const { esc, botaoRolar } = EG;
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
  const ROMANOS = G.ROMANOS;

  function conferenciaDoPJ(m) {
    const R = m.R, p = m.p;
    const slots = F.SLOTS_RELIQUIA.filter((s) => p.reliquias[s] && p.reliquias[s].tem).length;
    const ress = Object.values(p.ressonancias).filter(Boolean).length;
    const liberadas = (R.ressonancias_liberadas || []).length;
    const falta = [];
    if ((p.cone.nivel || 0) < R.cone_maximo) falta.push("Cone de Luz Nível " + R.cone_maximo);
    if (ress < liberadas) falta.push("Ressonância " + ROMANOS[ress]);
    if (!slots) falta.push("o primeiro slot de Relíquia");
    return [
      "<b>" + esc(G.nome(m)) + "</b> <span class='suave'>nível " + p.nivel + "</span>",
      "Nível " + (p.cone.nivel || 0) + " / <b>" + R.cone_maximo + "</b>" +
        (p.cone.sobreposicoes ? " <span class='suave'>+" + p.cone.sobreposicoes + " sobrep.</span>" : ""),
      "<b>Tier " + ROMANOS[R.tier_reliquia - 1] + "</b> <span class='suave'>em " + slots + "/6 slots</span>",
      ress + " / " + liberadas,
      R.verba_marco + " Cr",
      falta.length ? "<span class='ruim'>falta " + esc(falta.join(", ")) + "</span>" : "<span class='bom-texto'>em dia</span>",
    ];
  }

  function telaRecompensas() {
    const est = G.estado(), g = G.grupo(), f = G.faixaN();
    const calendario = H.cartao("Calendário das recompensas",
      H.tabela(["Recompensa", "Quando entra", "Quem decide"],
        C().mestre.recompensas.map((r) => ["<b>" + esc(r.recompensa) + "</b>", esc(r.quando), esc(r.quem)])) +
      "<h3>Equipamento e verba por faixa</h3>" +
      H.tabela(["Faixa", "Cone de Luz máximo", "Relíquias", "Verba de marco", "O que ela compra"],
        C().mestre.equipamento_faixa.map((x, i) => {
          const v = C().mestre.verba[i] || {};
          return [
            x.n === f ? "<b class='destaque'>" + esc(x.faixa) + "</b>" : esc(x.faixa),
            esc(x.cone), esc(x.reliquias), "<b>" + (v.verba || 0) + " Cr</b>", esc(v.compra || ""),
          ];
        })) +
      "<p class='ajuda'>Não existe compra de Relíquia, nem sorteio, nem economia de equipamento: isto é " +
      "calendário, e é <b>obrigação sua</b>. O orçamento de encontro assume que cada personagem carrega o Cone " +
      "e o Tier da faixa dele — um grupo sem isso está abaixo do orçamento e todo encontro fica mais duro do " +
      "que a tabela diz. " + link("27", "27.8", "27.8") + "</p>" +
      "<h3>Sobreposição</h3><p class='ajuda'>No máximo <b>uma por faixa alcançada</b>, e quem decide é você, " +
      "como marco narrativo. Teto de +3 no bônus numérico do Cone. " + link("25", "25.2", "25.2") + "</p>",
      "calendario", link("27", "27.8"));

    const conferencia = H.cartao("O que o grupo já deveria ter",
      g.length
        ? H.tabela(["Personagem", "Cone de Luz", "Relíquias", "Ressonâncias", "Verba de marco", "Situação"],
          g.map(conferenciaDoPJ)) +
          "<p class='ajuda'>O número em negrito é o que a faixa do personagem já libera. " +
          "Ressonâncias entram nos níveis 5, 10, 15 e 20, e são <b>sempre</b> um marco de história. " +
          link("26", "26.7", "26.7") + "</p>"
        : vazio("Ponha fichas no grupo para conferir o equipamento de cada um."),
      "conferencia");

    const entregas = H.cartao("Marcos entregues",
      "<ul class='checklist'>" + C().mestre.equipamento_faixa.map((x, i) =>
        "<li>" + H.marca("g", "entregas.faixa_" + x.n, "<b>Faixa " + esc(x.faixa) + "</b> — " +
          esc(x.cone) + " · " + esc(x.reliquias) + " · " +
          ((C().mestre.verba[i] || {}).verba || 0) + " Cr de verba") + "</li>").join("") + "</ul>" +
      "<p class='ajuda'>Marque quando a entrega já aconteceu na ficção. Amarre cada uma ao <b>Propósito de " +
      "Vida</b> de alguém e você nunca mais precisa de uma cena de loja.</p>", "entregas");

    const tesouro = H.cartao("Tesouro do grupo",
      (est.tesouro.length
        ? H.tabela(["O que é", "De onde veio", "Para quem", ""], est.tesouro.map((t, i) => [
          H.texto("g", "tesouro." + i + ".o_que", { rotulo: "O que é" }),
          H.texto("g", "tesouro." + i + ".de_onde", { rotulo: "De onde veio" }),
          H.texto("g", "tesouro." + i + ".para_quem", { rotulo: "Para quem" }),
          H.botao("tirar-tesouro", "×", { classe: "pequeno perigo", dados: { i: i } }),
        ]))
        : vazio("Nada no tesouro ainda.")) +
      "<div class='botoes'>" + H.botao("por-tesouro", "+ Anotar um achado") + "</div>", "tesouro");

    const proibido = H.cartao("O que não dar",
      "<ul class='lista-aviso'>" +
      "<li><b>Vantagem permanente</b> em qualquer coisa, ou bônus fora dos tetos do capítulo 26.</li>" +
      "<li><b>PH extra</b> de presente: a economia de PH é a espinha do balanceamento.</li>" +
      "<li><b>Habilidade acima do Nível máximo</b> do nível do personagem.</li>" +
      "<li>Item que <b>ignora Tenacidade, teto de RD, teto de dados ou limite de alvos</b> em área.</li>" +
      "<li><b>Dinheiro que resolve a cena.</b> A verba responde \"quanto custa?\", não compra poder.</li>" +
      "</ul><p class='ajuda'>" + link("27", "27.8", "27.8") + " e a lista de efeitos proibidos de " +
      link("27", "27.9", "27.9") + ".</p>", "proibido");

    app().innerHTML = topo("recompensas") + conferencia +
      "<div class='grade-mestre duas'><div class='coluna'>" + entregas + tesouro + "</div>" +
      "<div class='coluna'>" + proibido + "</div></div>" + calendario;
  }

  // ---------------------------------------------------------------------------
  // Escudo do Mestre
  // ---------------------------------------------------------------------------
  function telaConsulta() {
    const mt = C().mestre, f = G.faixaN();
    const dt = mt.dt_faixa;

    const dts = H.cartao("DT por faixa",
      H.tabela(["Dificuldade"].concat(dt.faixas.map((x, i) => i + 1 === f ? "<b class='destaque'>" + esc(x) + "</b>" : esc(x))),
        dt.linhas.map((l) => ["<b>" + esc(l.dificuldade) + "</b>"].concat(
          l.dt.map((v, i) => (i + 1 === f ? "<b class='destaque'>" + v + "</b>" : String(v)))))) +
      "<h3>As cinco DTs de subsistema</h3>" +
      H.tabela(["Teste", "DT", "Capítulo"], mt.dt_subsistema.map((x) =>
        ["<b>" + esc(x.teste) + "</b>", esc(x.dt), esc(x.capitulo)])) +
      "<p class='ajuda'>Estas cinco <b>vencem</b> a tabela de cima, e a lista é fechada: não existe uma sexta. " +
      link("27", "27.3", "27.3") + "</p>", "dts", link("27", "27.2"));

    const tenacidade = H.cartao("Tenacidade e Quebra",
      H.tabela(["Fonte", "Redução de Tenacidade"], mt.reducao_tenacidade.map((x) =>
        ["<b>" + esc(x.fonte) + "</b>", esc(x.rt)])) +
      "<h3>E o Elemento</h3>" +
      H.tabela(["Situação", "Dano", "Redução de Tenacidade"], mt.fraqueza_resistencia.map((x) =>
        ["<b>" + esc(x.situacao) + "</b>", esc(x.dano), esc(x.rt)])) +
      "<h3>Dano de Quebra por Elemento</h3>" +
      H.tabela(["Elemento", "Fórmula", "Na Eficiência +" + M.eficiencia(G.nivel()), "Efeito"],
        C().elementos.map((e) => {
          const q = G.quebraDe(e.elemento, M.eficiencia(G.nivel()));
          return ["<b>" + esc(e.elemento) + "</b>", esc(e.dano_quebra),
            botaoRolar(q.texto, "Dano de Quebra de " + e.elemento) + " <small>média " + q.media + "</small>",
            link("21", e.efeito_quebra, e.efeito_quebra)];
        })) +
      "<p class='ajuda'>A Tenacidade a 0 é Quebra: dano do Elemento, a condição dele, <b>1 casa de Atraso</b>, " +
      "<b>Quebrado</b> até o fim do próximo turno dele (−2 de Defesa e +1 dado de dano de qualquer fonte) e " +
      "<b>+10 de Energia</b> para quem quebrou. A barra volta cheia no fim do turno dele. " +
      link("20", "20.4", "20.4") + "</p>", "tenacidade-ref", link("20", "20.3"));

    const fila = H.cartao("Fila de Ação",
      "<p><b>Montar:</b> todos por VEL decrescente, personagens e inimigos na mesma lista. Empate: maior bônus " +
      "de Agilidade, depois Discernimento, depois os jogadores escolhem entre si e vêm <b>antes</b> dos NPCs. " +
      "Remonte a cada Ciclo com a VEL atual e os atrasos pendentes. <b>Nunca se rola a ordem.</b> " +
      link("19", "19.3", "19.3") + "</p>" +
      H.tabela(["Tipo de alvo", "Teto de Atraso por Ciclo", "Firmeza"], mt.atraso_tipo.map((x) =>
        ["<b>" + esc(x.tipo) + "</b>", x.teto + (x.teto === 1 ? " casa" : " casas"), esc(x.firmeza)])) +
      "<p class='ajuda'><b>Firmeza, na ordem:</b> (1) some todas as casas de Atraso do Ciclo, de todas as " +
      "fontes; (2) divida por 2 arredondando para baixo; (3) se der 0 e houver ao menos 1 casa bruta, o " +
      "resultado é 1 — <b>no total do Ciclo</b>, nunca por fonte; (4) aplique o teto de 2. " +
      link("19", "19.4", "19.4") + "</p>" +
      "<p><b>Avançar</b> só funciona em quem ainda não agiu. <b>Avanço Total</b> age logo após o turno atual, " +
      "no máximo 1 por Ciclo por criatura. Não existe Avanço pendente. " + link("19", "19.5", "19.5") + "</p>" +
      "<p><b>Congelamento:</b> Comum perde o turno; Elite e Boss são Atrasados em 2 casas (o teto do Ciclo, " +
      "então nada mais soma) e <b>não podem usar ação especial</b> no turno seguinte. " + link("19", "19.6", "19.6") + "</p>",
      "fila-ref", link("19", "19.3"));

    const inimigos = H.cartao("As regras de todo inimigo",
      "<ol class='lista-regras'>" +
      "<li>Inimigo <b>não tem Esquiva nem Intervir</b>. A defesa dele é PV, Defesa e RD.</li>" +
      "<li>Inimigo <b>não acumula Energia e não tem Ultimate</b>. O equivalente é ação especial com recarga em Ciclos.</li>" +
      "<li><b>Elite e Boss têm Firmeza.</b> Comum não tem, e tem teto de 3 casas.</li>" +
      "<li><b>Elite e Boss não perdem o turno</b> por Congelamento.</li>" +
      "<li>Ações agressivas: " + mt.acoes_tipo.map((x) => "<b>" + esc(x.tipo) + "</b> " + esc(x.por_turno)).join("; ") + ".</li>" +
      "<li>A <b>Tenacidade é pequena de propósito</b>: Comum quebra no primeiro ataque sério, Elite quase todo " +
      "Ciclo, Boss a cada 2 Ciclos.</li>" +
      "<li>Fraquezas: " + mt.fraquezas_tipo.map((x) => "<b>" + esc(x.tipo) + "</b> " + esc(x.fraquezas)).join("; ") +
      ". E vale o contrato de encontro de " + link("27", "27.5", "27.5") + ".</li>" +
      "<li><b>Resistência é endurecimento, não orçamento</b>: tira 2 dados (conservando 1) e trava a redução " +
      "de Tenacidade em 1.</li>" +
      "<li>Inimigo <b>não gera nem gasta PH</b>, não tem Esforço, e não aplica Congelamento em personagem.</li>" +
      "</ol><p class='ajuda'>" + link("28", "28.2", "28.2") + "</p>", "inimigos-ref", link("28", "28.2"));

    const ancoras = H.cartao("Âncoras de inimigo",
      "<div class='linha'>" + H.campo("Faixa",
        H.lista("g", "filtros.ancora", C().mestre.ancoras.map((a) => [String(a.n), a.faixa]),
          { rotulo: "Faixa", vazio: "a faixa do grupo (" + G.faixaTexto() + ")" }), "", "estreito") + "</div>" +
      linhaDaAncora(Number(G.estado().filtros.ancora) || f) +
      "<p class='ajuda'>Toda ficha do bestiário saiu desta tabela, e toda ficha que você criar também deve. " +
      "O <b>custo de um inimigo é o PV dele</b>. " + link("28", "28.3", "28.3") + "</p>", "ancoras-ref", link("28", "28.3"));

    const condicoes = H.cartao("Condições",
      H.tabela(["Condição", "Efeito", "Duração", "Acúmulo", "Só inimigos"],
        C().condicoes.map((c) => [
          "<b>" + link("21", c.condicao, c.condicao) + "</b>", esc(c.efeito), esc(c.duracao),
          esc(c.acumulo), c.so_inimigos === "Sim" ? "<b>sim</b>" : "não",
        ])) +
      "<p class='ajuda'>Cura não remove condição; o Descanso Longo remove todas. O dano das condições " +
      "contínuas sai pela <b>Eficiência de quem aplicou</b>. " + link("21", "21.5", "21.5") + "</p>",
      "condicoes-ref", link("21", "21.5"));

    const energia = H.cartao("Energia e PH",
      H.tabela(["Fonte", "Energia", "Limite"], C().energia.map((x) =>
        ["<b>" + esc(x.fonte) + "</b>", esc(x.energia), esc(x.limite)])) +
      "<p class='ajuda'>O PH é do <b>grupo</b>: máximo 1 + jogadores (+1 do nível 9, +2 do 17), começa o " +
      "combate 2 abaixo do máximo e gera 1 (ou 2 do nível 9) por Ataque Básico que acerta. " +
      link("16", "16.2", "16.2") + "</p>", "energia-ref", link("17", "17.2"));

    app().innerHTML = topo("consulta") +
      "<p class='ajuda'>Tudo nesta tela sai do livro v" + esc(C().versao) + ". Use <b>Mais &gt; Imprimir esta " +
      "tela</b> para ter o escudo no papel.</p>" +
      "<div class='grade-mestre'>" +
      "<div class='coluna'>" + dts + fila + "</div>" +
      "<div class='coluna'>" + tenacidade + inimigos + "</div>" +
      "<div class='coluna'>" + energia + "</div>" +
      "</div>" + ancoras + condicoes;
  }

  // ---------------------------------------------------------------------------
  // Ações do tesouro
  // ---------------------------------------------------------------------------
  G.acoes["por-tesouro"] = () => {
    G.estado().tesouro.push({ o_que: "", de_onde: G.estado().combate.nome || "", para_quem: "" });
  };

  G.acoes["tirar-tesouro"] = (b) => { G.estado().tesouro.splice(Number(b.dataset.i), 1); };

  G.telas.recompensas = telaRecompensas;
  G.telas.consulta = telaConsulta;
})();
