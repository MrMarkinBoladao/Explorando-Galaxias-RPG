/*
 * mestre-npcs.js — O banco de NPCs da Área do Mestre e a ficha de cada um.
 *
 * Um NPC aqui é uma ficha de personagem completa, igual à de um jogável: mesmo modelo,
 * mesmo motor de regras, mesmo Memoespírito e — literalmente — a mesma tela de editar,
 * porque esta tela chama `F.corpoDoEditor({npc: true})`. A diferença é só onde a ficha
 * mora: na mesa do Mestre, e não no mapa de fichas dos jogadores. Por isso o NPC não entra
 * no grupo, não conta no tamanho da mesa e não encosta no PH, que é dos jogadores (16.2).
 *
 * O modelo, a Fila de Ação e o formato do arquivo ficam em mestre-base.js.
 */
(function () {
  "use strict";

  const EG = window.EG;
  const { esc, sinal, botaoRolar } = EG;
  const M = window.Motor;
  const F = EG.Ficha;
  const G = EG.Mestre;
  const H = G.H;
  const link = (n, t, r) => EG.Regras.link(n, t, r);

  const app = G.app;
  const vazio = G.vazio;
  const topo = G.topo;

  const A = G.acoes;
  const el = (id) => document.getElementById(id);
  const lerVal = (id) => (el(id) ? el(id).value : "");
  const lerNum = (id) => {
    const e = el(id), n = e ? Math.floor(Number(e.value)) : 0;
    return Number.isFinite(n) && n > 0 ? n : 0;
  };

  /**
   * Coleções prontas que o site serve em `npcs/`, como as de inimigos. Caminho relativo
   * porque as rotas são de hash: o index.html está sempre na raiz do site.
   */
  const COLECOES = [
    ["npcs/tripulacao-do-expresso-astral.json", "Tripulação do Expresso Astral"],
    ["npcs/cacadores-de-stellaron.json", "Caçadores de Stellaron"],
  ];

  const selo = () => (EG.VERSAO && EG.VERSAO !== "dev" ? "?v=" + EG.VERSAO : "");

  // Relatório da última importação. Fica em memória de propósito: é recado de tela, não
  // estado de campanha, e não deve ir para o localStorage nem para o arquivo de mesa.
  let relatorio = null;

  // ---------------------------------------------------------------------------
  // A ficha de NPC aberta na tela
  // ---------------------------------------------------------------------------
  /**
   * Aponta a ficha aberta do site (`F.P`) para a ficha de um NPC e diz onde ela é gravada.
   * Daqui para frente os delegados de ficha-base.js fazem todo o trabalho: cada tecla
   * escreve em `F.P` e chama `F.salvar()`, que cai no `aoSalvar` daqui e grava a mesa.
   *
   * `G.tela()` zera `F.P`, `F.R` e `F.aoSalvar` ao entrar em qualquer rota do Mestre, então
   * isto é refeito a cada desenho e nenhuma outra tela herda a ficha do NPC.
   */
  function abrirFicha(m) {
    F.P = m.p;
    F.aoSalvar = function () { G.salvar(); };
    F.recalcular();
  }

  /** O que está em branco na ficha, sem mexer na ficha que estiver aberta. */
  function pendenciasDe(m) {
    const p0 = F.P, r0 = F.R;
    F.P = m.p;
    F.R = m.R;
    const falta = F.pendencias();
    F.P = p0;
    F.R = r0;
    return falta;
  }

  const etiquetaPapel = (papel) =>
    "<span class='etiqueta npc" + (papel === "Adversário" ? " adversario" : papel === "Aliado" ? " aliado" : "") +
    "'>" + esc(papel || "Neutro") + "</span>";

  const resumoDe = (p) => [p.npc.faccao, p.raca, p.caminho, "nível " + p.nivel, p.elemento]
    .filter(Boolean).join(" · ");

  // ---------------------------------------------------------------------------
  // Banco de NPCs
  // ---------------------------------------------------------------------------
  function cartaoCriar() {
    const fichas = Object.values(EG.Armazem.todas())
      .sort((a, b) => (a.nome || "").localeCompare(b.nome || ""));
    return H.cartao("Criar um NPC",
      "<div class='linha'>" +
      H.campo("Nome", "<input type='text' id='npc-nome' placeholder='Kafka' aria-label='Nome do NPC'>") +
      H.campo("Papel", "<select id='npc-papel' aria-label='Papel'>" +
        G.PAPEIS.map((x) => "<option" + (x === "Neutro" ? " selected" : "") + ">" + esc(x) + "</option>").join("") +
        "</select>", "", "estreito") +
      H.campo("Nível", "<input type='number' id='npc-nivel' min='1' max='20' value='" + G.nivel() +
        "' class='curto' aria-label='Nível'>", "", "estreito") +
      H.botao("criar-npc", "Criar", { classe: "primario" }) +
      "</div>" +
      "<p class='ajuda'>Nasce em branco, com a ficha inteira para preencher — e <b>nada é obrigatório</b>. " +
      "Um NPC só de nome já serve para a sua lista; se ele for lutar, você preenche Caminho, Atributos, " +
      "Elemento, Armadura e Arma, e os números saem sozinhos.</p>" +
      (fichas.length
        ? "<h3>Copiar de uma ficha salva</h3>" +
          "<div class='linha'><label class='sr-only' for='npc-de-ficha'>Ficha salva</label>" +
          "<select id='npc-de-ficha'>" + fichas.map((p) => "<option value='" + esc(p.id) + "'>" +
            esc(p.nome || "Personagem sem nome") + " · nível " + esc(p.nivel) +
            (p.caminho ? " · " + esc(p.caminho) : "") + "</option>").join("") + "</select>" +
          H.botao("npc-de-ficha", "Copiar como NPC") + "</div>" +
          "<p class='ajuda'>Faz uma <b>cópia</b> da ficha como NPC: a ficha do jogador continua intacta e " +
          "separada. É o caminho do personagem que saiu da campanha e virou figura da história.</p>"
        : ""),
      "criador");
  }

  function filtrosDoBanco(quantos, total) {
    return H.cartao("Procurar no banco",
      "<div class='linha'>" +
      H.campo("Papel", H.lista("g", "filtros.npc_papel", G.PAPEIS, { rotulo: "Papel", vazio: "todos os papéis" }),
        "", "estreito") +
      H.campo("Procurar", H.texto("g", "filtros.npc_q", { rotulo: "Procurar no banco", busca: true, vivo: true,
        ph: "nome, facção, Caminho ou Elemento" })) +
      "</div>" +
      "<p class='ajuda'>" + quantos + " de " + total + (total === 1 ? " NPC" : " NPCs") + " no banco.</p>",
      "filtros-npcs");
  }

  /** O cartão de um NPC no banco: o essencial para decidir, e os botões para usar. */
  function cartaoDoNpc(m, i) {
    const p = m.p, R = m.R, j = p.jogo;
    const pv = G.pvAtual(m);
    const cam = "npcs." + i;
    const emCena = G.npcEstaEmCena(m.id);
    const falta = pendenciasDe(m);
    const ab = R.ataque_basico;

    let corpo = "<p class='suave'>" + esc(resumoDe(p)) + "</p>" +
      (p.conceito ? "<p class='efeito'><i>" + esc(p.conceito) + "</i></p>" : "") +
      "<div class='pv'><span class='pv-numero'>" + pv + "<small> / " + R.pv_max + "</small></span>" +
      H.barraPV(pv, R.pv_max, "PV de " + G.nome(m)) + "</div>" +
      "<div class='numeros compactos'>" +
      H.num("Defesa", R.defesa) +
      H.num("Esquiva", R.esquiva == null ? "—" : R.esquiva) +
      H.num("RD", R.rd) + H.num("VEL", R.velocidade) +
      H.num("DT dele", R.dt, "Habilidades") +
      H.num("Energia", (j.energia || 0) + "<small>/100</small>", "Ult a " + R.ultimate.custo) +
      "</div>";

    if (ab) {
      corpo += "<div class='acao-numeros'>" +
        "<span>Ataque Básico " + botaoRolar(M.rolagem(ab.ataque), G.nome(m) + ": Ataque Básico") + "</span>" +
        "<span>Dano " + botaoRolar(ab.texto, G.nome(m) + ": dano do Ataque Básico") +
        " <small>média " + ab.media + "</small></span>" +
        "<span class='suave'>" + esc(ab.elemento) + " · " + esc(ab.alcance) + "</span></div>";
    }
    if (R.memo) {
      corpo += "<p class='ajuda'><b>Memoespírito:</b> " + esc(p.memoespirito.nome || "sem nome") +
        " · PV " + R.memo.pv + " · VEL " + R.memo.velocidade +
        (j.memo_ativo ? " · <span class='etiqueta pronta'>em campo</span>" : "") + "</p>";
    }
    if ((j.condicoes || []).length) {
      corpo += "<p class='ajuda ruim'>" + j.condicoes.map((c) => esc(c.nome) +
        (c.turnos != null ? " (" + c.turnos + "t)" : "")).join(", ") + "</p>";
    }
    if (falta.length) {
      corpo += "<p class='ajuda'>Em branco: " + esc(falta.join(", ")) + ".</p>";
    }

    corpo += "<div class='linha'>" +
      H.campo("Papel", H.lista("g", cam + ".npc.papel", G.PAPEIS, { rotulo: "Papel", vazio: false }), "", "estreito") +
      H.campo("Facção", H.texto("g", cam + ".npc.faccao", { rotulo: "Facção" })) +
      "</div>" +
      "<div class='botoes'>" +
      "<a class='botao primario' href='#mestre/npcs/" + esc(m.id) + "'>Abrir a ficha</a>" +
      (emCena
        ? H.botao("tirar-npc-da-cena", "Tirar da cena", { classe: "perigo", dados: { mid: m.id } }) +
          "<a class='botao' href='#mestre/combate'>Ver no combate »</a>"
        : H.botao("por-npc-em-cena", "Pôr em cena »", { dados: { mid: m.id, ir: "1" },
            titulo: "Entra na Fila de Ação pela VEL da ficha dele" })) +
      H.botao("descanso-npc", "Descanso Longo", { dados: { mid: m.id, t: "longo" },
        titulo: "PV cheios, condições removidas, Memoespírito dispensado (23.6)" }) +
      H.botao("duplicar-npc", "Duplicar", { dados: { mid: m.id } }) +
      H.botao("exportar-npc", "Exportar .json", { dados: { mid: m.id } }) +
      H.botao("excluir-npc", "Excluir", { classe: "perigo", dados: { mid: m.id } }) +
      "</div>";

    return H.cartao(esc(G.nome(m)) + " " + etiquetaPapel(p.npc.papel), corpo,
      "npc-cartao" + (emCena ? " em-cena" : ""),
      "<span class='suave'>" + (emCena ? "<b class='destaque'>em cena</b> · " : "") +
      R.pv_max + " PV · VEL " + R.velocidade + "</span>");
  }

  function cartaoDeArquivos(quantos) {
    const aviso = !relatorio ? "" :
      "<div class='relatorio-import" + (relatorio.erro ? " ruim" : "") + "'>" +
      "<p><b>" + esc(relatorio.titulo) + "</b></p>" +
      (relatorio.avisos && relatorio.avisos.length
        ? "<ul class='lista-avisos'>" + relatorio.avisos.map((a) => "<li>" + esc(a) + "</li>").join("") + "</ul>"
        : "") +
      H.botao("limpar-relatorio-npcs", "Fechar", { classe: "pequeno" }) +
      "</div>";

    return H.cartao("Importar e exportar NPCs",
      "<p class='ajuda'>A ficha de NPC é uma ficha de personagem, então o arquivo é o mesmo " +
      "<code>.json</code> que a aba Jogar exporta — com um bloco <code>npc</code> a mais. Isso vale nos " +
      "dois sentidos: <b>o <code>.json</code> que um jogador mandou importa aqui como NPC</b>, e um NPC " +
      "exportado abre como ficha na aba Jogar. A importação <b>soma</b> ao banco e nunca apaga nada.</p>" +
      "<div class='botoes'>" +
      H.botao("importar-npcs", "Importar NPCs (.json)", { classe: "primario" }) +
      H.botao("exportar-npcs", "Exportar meus NPCs", { desabilitado: !quantos,
        titulo: quantos ? "Baixa os " + quantos + " NPCs do banco num arquivo só" : "O banco está vazio" }) +
      "</div>" + aviso +
      "<h3>Coleções prontas para baixar</h3>" +
      "<p class='ajuda'>Baixe o arquivo e importe aqui mesmo. São fichas de exemplo, no nível 10 — " +
      "mude nível, Elemento e Bênçãos à vontade: depois de importadas, são suas.</p>" +
      "<ul class='lista-colecoes'>" + COLECOES.map(([caminho, rotulo]) =>
        "<li><a href='" + esc(caminho + selo()) + "' download>" + esc(rotulo) + "</a></li>").join("") + "</ul>" +
      "<details><summary>O formato do arquivo</summary>" +
      "<p class='ajuda'>A exportação grava assim, e a importação aceita de volta. Ela também aceita uma " +
      "ficha sozinha (a que o jogador exporta), uma lista solta de fichas, um arquivo de mesa e um backup " +
      "completo — do backup ela pega as fichas e traz como NPC.</p>" +
      "<pre class='exemplo-json'>" + esc(
        "{\n" +
        '  "tipo": "' + G.MARCA_NPCS + '",\n' +
        '  "versao": 1,\n' +
        '  "nome": "Minha coleção",\n' +
        '  "npcs": [\n' +
        "    {\n" +
        '      "nome": "Kafka",\n' +
        '      "npc": { "papel": "Adversário", "faccao": "Caçadores de Stellaron" },\n' +
        '      "nivel": 10,\n' +
        '      "raca": "Humano",\n' +
        '      "caminho": "A Inexistência",\n' +
        '      "elemento": "Raio",\n' +
        '      "atributos": { "Poder": 12, "Agilidade": 14, "Vigor": 13,\n' +
        '                     "Sincronia": 10, "Discernimento": 15, "Presença": 8 }\n' +
        "    }\n" +
        "  ]\n" +
        "}") + "</pre>" +
      "<p class='ajuda'><b>Só o <code>nome</code> é obrigatório.</b> Todo campo que faltar fica em branco, " +
      "como numa ficha nova, e o motor calcula com o que tiver — uma ficha de NPC quase vazia é um caso " +
      "válido, não um erro. <code>npc.papel</code> aceita Aliado, Neutro ou Adversário (o padrão é Neutro). " +
      "Se a ficha ferir alguma regra do livro, a importação avisa e a tela de editar mostra onde.</p>" +
      "</details>",
      "arquivos-npcs");
  }

  function telaBanco() {
    const est = G.estado();
    const fl = est.filtros;
    const q = EG.norm(fl.npc_q || "");
    const todos = G.npcs();
    const visiveis = [];
    todos.forEach((p, i) => {
      if (fl.npc_papel && p.npc.papel !== fl.npc_papel) return;
      if (q && !EG.norm([p.nome, p.npc.faccao, p.caminho, p.elemento, p.raca, p.conceito].join(" ")).includes(q)) return;
      visiveis.push([p, i]);
    });
    const emCena = G.npcsEmCena();

    const explicacao = H.cartao("NPCs",
      "<p>Um NPC tem a <b>ficha inteira de um personagem jogável</b> — Caminho, Atributos, Perícias, " +
      "Habilidades, Ultimate, equipamento e Memoespírito — e os números dele saem do mesmo motor de " +
      "regras. O que ele <b>não</b> faz é entrar no grupo: ele não aparece na ficha de nenhum jogador, " +
      "não conta no tamanho da mesa e não usa o PH, que é recurso dos jogadores (" +
      link("16", "16.2", "16.2") + ").</p>" +
      "<p class='ajuda'>Para usar um NPC numa luta, ponha ele em cena: ele ganha casa própria na " +
      "<b>Fila de Ação</b> pela VEL da ficha dele, com os desempates de " + link("19", "19.3", "19.3") +
      " (em empate, os jogadores vêm antes dos NPCs). Lá ele tem PV com dano e cura, Energia, condições " +
      "com turnos, o painel de Morrendo e o Memoespírito — tudo pelos mesmos controles do grupo.</p>" +
      (emCena.length
        ? "<p><b>Em cena agora:</b> " + emCena.map((m) => esc(G.nome(m)) + " " +
            H.botao("tirar-npc-da-cena", "tirar", { classe: "pequeno", dados: { mid: m.id } })).join(" · ") +
          " <a href='#mestre/combate'>abrir o combate »</a></p>"
        : ""),
      "explicacao-npcs");

    app().innerHTML = topo("npcs") + explicacao + cartaoCriar() + cartaoDeArquivos(todos.length) +
      "<h2 class='titulo-secao'>O banco</h2>" +
      (todos.length ? filtrosDoBanco(visiveis.length, todos.length) : "") +
      (!todos.length
        ? H.cartao("Banco vazio", vazio("Crie um NPC acima, copie uma ficha salva ou importe uma coleção " +
            "pronta. Dá para criar só com o nome e preencher o resto no dia que ele precisar rolar dado."), "vazio")
        : visiveis.length
          ? "<div class='grade-npcs'>" + visiveis.map(([p, i]) => cartaoDoNpc(G.npc(p.id), i)).join("") + "</div>"
          : H.cartao("Nada encontrado", vazio("Nenhum NPC com esse filtro."), "vazio"));
  }

  // ---------------------------------------------------------------------------
  // A ficha de um NPC: a tela Editar ficha inteira, com outro cabeçalho
  // ---------------------------------------------------------------------------
  function telaFicha(id) {
    const m = G.npc(id);
    if (!m) {
      app().innerHTML = topo("npcs") +
        H.cartao("NPC não encontrado", vazio("Essa ficha não está mais no banco.") +
          "<div class='botoes'><a class='botao primario' href='#mestre/npcs'>Voltar ao banco</a></div>", "vazio");
      return;
    }
    abrirFicha(m);
    const R = F.R, p = F.P;
    const emCena = G.npcEstaEmCena(id);
    const cabeca = H.cartao(esc(G.nome(m)) + " " + etiquetaPapel(p.npc.papel),
      "<p class='suave'>" + esc(resumoDe(p)) + "</p>" +
      "<div class='numeros compactos'>" +
      H.num("PV", R.pv_max) + H.num("Defesa", R.defesa) +
      H.num("Esquiva", R.esquiva == null ? "—" : R.esquiva) +
      H.num("RD", R.rd) + H.num("VEL", R.velocidade) +
      H.num("DT dele", R.dt, "Habilidades") +
      H.num("Eficiência", sinal(R.eficiencia)) +
      "</div>" +
      "<div class='botoes'>" +
      "<a class='botao' href='#mestre/npcs'>« Voltar ao banco</a>" +
      (emCena
        ? "<a class='botao' href='#mestre/combate'>Ver no combate »</a>" +
          H.botao("tirar-npc-da-cena", "Tirar da cena", { classe: "perigo", dados: { mid: id } })
        : H.botao("por-npc-em-cena", "Pôr em cena »", { classe: "primario", dados: { mid: id, ir: "1" } })) +
      H.botao("exportar-npc", "Exportar .json", { dados: { mid: id } }) +
      "</div>",
      "npc-cabeca");

    // F.corpoDoEditor desenha a tela Editar ficha inteira sobre a ficha aberta, que é a
    // deste NPC. Os delegados de ficha-base.js cuidam de salvar e recalcular a cada tecla.
    app().innerHTML = topo("npcs") + cabeca + F.corpoDoEditor({ npc: true });
  }

  function tela(r) {
    const id = r && r.partes && r.partes[1];
    if (id) telaFicha(id);
    else telaBanco();
  }

  // ---------------------------------------------------------------------------
  // A tira de NPCs na tela de Combate
  // ---------------------------------------------------------------------------
  G.cartaoNpcsEmCena = function () {
    const banco = G.npcs();
    const emCena = G.npcsEmCena();
    if (!banco.length) {
      return H.cartao("Pôr NPC em cena",
        vazio("Nenhum NPC no banco ainda. <a href='#mestre/npcs'>Criar um NPC »</a>") +
        "<p class='ajuda'>Um NPC é uma ficha de personagem que não é de ninguém da mesa: ele entra na " +
        "Fila pela VEL da ficha dele, com Memoespírito e condições, e não encosta no PH do grupo.</p>",
        "por-npc");
    }
    const dentro = new Set(emCena.map((m) => m.id));
    const fora = banco.filter((p) => !dentro.has(p.id));
    return H.cartao("NPCs em cena",
      (emCena.length
        ? "<ul class='tira-grupo'>" + emCena.map((m) => {
            const pv = G.pvAtual(m), j = m.p.jogo;
            return "<li><div class='tira-topo'><b>" + esc(G.nome(m)) + "</b> " + etiquetaPapel(m.p.npc.papel) +
              "<span class='suave'>" + esc(resumoDe(m.p)) + "</span></div>" +
              "<div class='tira-pv'><span>" + pv + "<small>/" + m.R.pv_max + "</small></span>" +
              H.barraPV(pv, m.R.pv_max, "PV de " + G.nome(m)) + "</div>" +
              "<div class='tira-extra'>" +
              "<span title='Velocidade'>VEL " + m.R.velocidade + "</span>" +
              "<span title='Defesa'>DEF " + m.R.defesa_com_temporarios + "</span>" +
              "<span title='Energia'>Energia " + (j.energia || 0) + "/100</span>" +
              (m.R.memo ? "<span>" + (j.memo_ativo ? "<span class='etiqueta pronta'>Memo em campo</span>"
                : "Memo fora") + "</span>" : "") +
              (pv === 0 ? "<span class='etiqueta ruim'>Morrendo</span>" : "") +
              "</div>" +
              "<div class='botoes compactos'>" +
              H.botao("escolher-alvo", "Abrir o painel", { classe: "pequeno", dados: { k: "n:" + m.id } }) +
              "<a class='botao pequeno' href='#mestre/npcs/" + esc(m.id) + "'>abrir a ficha</a>" +
              H.botao("tirar-npc-da-cena", "Tirar da cena", { classe: "pequeno perigo", dados: { mid: m.id } }) +
              "</div></li>";
          }).join("") + "</ul>"
        : vazio("Nenhum NPC nesta cena.")) +
      (fora.length
        ? "<div class='linha'><label class='sr-only' for='novo-npc'>NPC</label>" +
          "<select id='novo-npc'>" + G.PAPEIS.map((papel) => {
            const doPapel = fora.filter((p) => p.npc.papel === papel);
            return !doPapel.length ? "" : "<optgroup label='" + esc(papel) + "'>" +
              doPapel.map((p) => "<option value='" + esc(p.id) + "'>" + esc(p.nome || "NPC sem nome") +
                " · nível " + esc(p.nivel) + (p.elemento ? " · " + esc(p.elemento) : "") +
                "</option>").join("") + "</optgroup>";
          }).join("") + "</select>" +
          H.botao("por-npc-escolhido", "Pôr em cena", { classe: "primario" }) + "</div>"
        : "<p class='ajuda'>Todos os NPCs do banco já estão nesta cena.</p>") +
      "<p class='ajuda'>O NPC entra na Fila pela <b>VEL da ficha dele</b> e age um turno por Ciclo, como " +
      "qualquer personagem. Em empate, os jogadores vêm antes (" + link("19", "19.3", "19.3") + "). " +
      "Ele não entra no grupo nem no PH, e o que você mexer no PV e nas condições dele fica salvo na " +
      "ficha do NPC, no banco.</p>",
      "por-npc", "<a href='#mestre/npcs'>banco de NPCs »</a>");
  };

  // ---------------------------------------------------------------------------
  // Ações
  // ---------------------------------------------------------------------------
  A["criar-npc"] = () => {
    const nome = lerVal("npc-nome").trim();
    const papel = lerVal("npc-papel") || "Neutro";
    const p = G.novoNpc(nome, papel);
    const nivel = lerNum("npc-nivel");
    if (nivel) p.nivel = Math.max(1, Math.min(20, nivel));
    G.estado().npcs.unshift(p);
    G.salvar();
    location.hash = "#mestre/npcs/" + p.id;
    EG.toast("<b>" + esc(nome || "NPC sem nome") + "</b> criado no nível " + p.nivel +
      ". Preencha só o que você for usar.");
    return false;
  };

  A["npc-de-ficha"] = () => {
    const id = lerVal("npc-de-ficha");
    const bruta = EG.Armazem.todas()[id];
    if (!bruta) { EG.toast("Escolha uma ficha salva.", "erro"); return false; }
    const p = G.completarNpc(EG.clonar(bruta));
    p.id = EG.uid();
    p.jogador = "";
    p.npc.papel = "Aliado";
    G.estado().npcs.unshift(p);
    G.salvar();
    location.hash = "#mestre/npcs/" + p.id;
    EG.toast("<b>" + esc(p.nome || "NPC sem nome") + "</b> copiado para o banco de NPCs como <b>Aliado</b>. " +
      "A ficha do jogador continua salva e separada.");
    return false;
  };

  A["duplicar-npc"] = (b) => {
    const est = G.estado(), i = G.indiceDoNpc(b.dataset.mid);
    if (i < 0) return false;
    const p = G.completarNpc(EG.clonar(est.npcs[i]));
    p.id = EG.uid();
    p.nome = (p.nome || "NPC") + " (cópia)";
    est.npcs.splice(i + 1, 0, p);
    EG.toast("<b>" + esc(p.nome) + "</b> no banco.");
  };

  A["excluir-npc"] = (b) => {
    const est = G.estado(), i = G.indiceDoNpc(b.dataset.mid);
    if (i < 0) return false;
    const p = est.npcs[i];
    if (!confirm("Excluir a ficha de " + (p.nome || "NPC sem nome") + "? Isso não tem volta " +
      "(a não ser que você tenha exportado).")) return false;
    G.tirarNpcDaCena(p.id);
    est.npcs.splice(i, 1);
    for (const e of est.encontros || []) {
      if (!Array.isArray(e.npcs)) continue;
      const j = e.npcs.indexOf(p.id);
      if (j >= 0) e.npcs.splice(j, 1);
    }
    if (location.hash.indexOf("#mestre/npcs/") === 0) location.hash = "#mestre/npcs";
    EG.toast("Ficha de NPC excluída.");
  };

  A["por-npc-em-cena"] = (b) => {
    const m = G.porNpcEmCena(b.dataset.mid);
    if (!m) { EG.toast("Não achei essa ficha de NPC.", "erro"); return false; }
    const cb = G.estado().combate;
    cb.alvo = "n:" + m.id;
    EG.toast("<b>" + esc(G.nome(m)) + "</b> entrou na cena com " + m.R.pv_max + " PV, " +
      "na Fila pela VEL " + m.R.velocidade + " (19.3).");
    if (b.dataset.ir) {
      G.salvar();
      location.hash = "#mestre/combate";
      return false;
    }
  };

  A["por-npc-escolhido"] = () => {
    const id = lerVal("novo-npc");
    if (!id) return false;
    const m = G.porNpcEmCena(id);
    if (!m) { EG.toast("Escolha um NPC do banco.", "erro"); return false; }
    G.estado().combate.alvo = "n:" + m.id;
    EG.toast("<b>" + esc(G.nome(m)) + "</b> entrou na cena com " + m.R.pv_max + " PV, na Fila pela VEL " +
      m.R.velocidade + ".");
  };

  // --- NPCs em arquivo -------------------------------------------------------
  A["exportar-npc"] = (b) => {
    const m = G.npc(b.dataset.mid);
    if (!m) return false;
    EG.baixarJSON("npc-" + EG.fatiarNome(m.p.nome, "sem-nome") + ".json",
      G.pacoteDeNpcs([m.p], m.p.nome || ""));
    EG.toast("<b>" + esc(G.nome(m)) + "</b> exportado. O arquivo importa como NPC em qualquer navegador — " +
      "e abre como ficha na aba Jogar, se você quiser.");
    return false;
  };

  A["exportar-npcs"] = () => {
    const est = G.estado(), lista = G.npcs();
    if (!lista.length) {
      EG.toast("O banco de NPCs está vazio.", "erro");
      return false;
    }
    EG.baixarJSON("npcs-" + EG.fatiarNome(est.campanha.nome, "campanha") + ".json",
      G.pacoteDeNpcs(lista, est.campanha.nome || ""));
    EG.toast("<b>" + lista.length + (lista.length === 1 ? " NPC" : " NPCs") + "</b> exportados.");
    return false;
  };

  A["importar-npcs"] = () => {
    const campo = el("arquivo-npcs");
    campo.value = "";                  // deixa reimportar o mesmo arquivo
    campo.click();
    return false;
  };

  A["limpar-relatorio-npcs"] = () => { relatorio = null; };

  function lerTexto(arquivo) {
    return new Promise((resolve) => {
      const leitor = new FileReader();
      leitor.onload = () => resolve(leitor.result);
      leitor.onerror = () => resolve(null);
      leitor.readAsText(arquivo);
    });
  }

  async function importarNpcs(arquivos) {
    const prontos = [], avisos = [], recusados = [];

    for (const arquivo of Array.from(arquivos)) {
      const cru = await lerTexto(arquivo);
      let bruto = null;
      try { bruto = JSON.parse(cru); } catch (_) {
        recusados.push(arquivo.name + ": não é um JSON válido");
        continue;
      }
      const fichas = G.listaDeNpcsDoArquivo(bruto);
      if (!fichas) { recusados.push(arquivo.name + ": nenhuma ficha encontrada dentro dele"); continue; }
      if (!fichas.length) { recusados.push(arquivo.name + ": a lista de fichas está vazia"); continue; }
      for (const ficha of fichas) {
        const r = G.npcDeArquivo(ficha);
        if (r.erro) { avisos.push(arquivo.name + ": uma ficha foi pulada, " + r.erro); continue; }
        prontos.push(r.npc);
        for (const a of r.avisos) avisos.push(a);
      }
    }

    if (!prontos.length) {
      relatorio = { erro: true, titulo: "Nada foi importado.", avisos: recusados.concat(avisos) };
      EG.toast("Nenhum NPC veio desse arquivo. Veja o motivo na aba NPCs.", "erro");
      G.redesenhar();
      return;
    }

    const est = G.estado();
    const quantos = prontos.length;
    const jaTinha = prontos.filter((p) => est.npcs.some((y) => EG.norm(y.nome) === EG.norm(p.nome)));
    if (!confirm("Importar " + quantos + (quantos === 1 ? " NPC" : " NPCs") + " para o banco?\n\n" +
      "Eles entram somados aos " + est.npcs.length + " que você já tem. Nada é apagado." +
      (jaTinha.length ? "\n\n" + jaTinha.length + (jaTinha.length === 1 ? " nome já existe" : " nomes já existem") +
        " no banco e vão aparecer repetidos." : ""))) return;

    // Id repetido viraria duas fichas apontando para a mesma: cada uma ganha a sua.
    const usados = new Set(est.npcs.map((p) => p.id).concat(Object.keys(EG.Armazem.todas())));
    for (const p of prontos) {
      if (usados.has(p.id)) p.id = EG.uid();
      usados.add(p.id);
    }
    est.npcs.unshift(...prontos);
    if (jaTinha.length) avisos.push("Nome repetido no banco: " + jaTinha.map((p) => p.nome).join(", "));
    relatorio = {
      titulo: quantos + (quantos === 1 ? " NPC importado" : " NPCs importados") +
        (recusados.length ? ", e " + recusados.length +
          (recusados.length === 1 ? " arquivo recusado" : " arquivos recusados") : "") + ".",
      avisos: recusados.concat(avisos),
    };
    G.salvar();
    EG.toast("<b>" + quantos + (quantos === 1 ? " NPC" : " NPCs") + "</b> no banco." +
      (avisos.length ? " Confira os avisos no cartão de importação." : ""));
    G.redesenhar();
  }

  document.addEventListener("change", (ev) => {
    if (ev.target.id === "arquivo-npcs" && ev.target.files.length) importarNpcs(ev.target.files);
  });

  G.telas.npcs = tela;
})();
