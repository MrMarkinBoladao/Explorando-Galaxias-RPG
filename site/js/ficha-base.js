/*
 * ficha-base.js — O modelo da ficha: personagem em branco, exemplo (Nadir), tradução para o
 * motor de regras, campos de formulário e a barra de personagens. As telas ficam em
 * ficha-editar.js e ficha-jogar.js.
 */
(function () {
  "use strict";

  const EG = window.EG;
  const { esc } = EG;
  const M = window.Motor;
  const C = () => window.CATALOGO;

  const SLOTS_RELIQUIA = ["Cabeça", "Mãos", "Tronco", "Botas", "Esfera Planar", "Corda de Ligação"];
  const LETRAS_CONJUNTO = ["A", "B", "C"];

  // ---------------------------------------------------------------------------
  // Modelo
  // ---------------------------------------------------------------------------
  function novaHabilidade() {
    return { nome: "", tipo: "Dano", nivel: 1, area: false, resolucao: "Teste de Ataque", alcance: "Curta",
      ress3: false, efeito: "" };
  }

  function modeloVazio() {
    return {
      id: "", versao: 1,
      nome: "", jogador: "", conceito: "", proposito: "", crenca: "", aparencia: "", coisa: "", notas: "",
      // A história do personagem, escrita pelo jogador, em Markdown: ela é longa de
      // propósito e por isso mora num campo só dela, mostrada formatada e recolhível.
      lore: "",
      nivel: 1, jogadores: 4,
      raca: "", bonus_racial: { modo: "Um Atributo (+2)", attr1: "", attr2: "" },
      caminho: "", atributo_habilidade: "", elemento: "",
      metodo: "Array oficial",
      atributos: { Poder: null, Agilidade: null, Vigor: null, Sincronia: null, Discernimento: null, "Presença": null },
      aumentos: {},
      sintonia: "Discernimento", pericias_escolhidas: [], eficacia_pericias: [], eficacia_tr: [],
      habilidades: [novaHabilidade()],
      ultimate: { nome: "", tipo: "Dano", area: false, resolucao: "Teste de Ataque", efeito: "" },
      bencaos: [], fragmento: "", forma_avatar: "",
      armadura: "", armadura_nome: "",
      arma: { nome: "", categoria: "", atributo: "Poder", elemento: "", propriedade: "Nenhuma" },
      // `descricao` e `imagem` são só o sabor do Cone (25.2) e por isso não vão ao motor:
      // a descrição é a história que ele carrega, e a imagem é a arte dele, guardada na
      // própria ficha (um endereço `data:`) ou um link para fora.
      cone: { nome: "", nivel: null, alvo: "", qual: "", escolha: "Numérico", sobreposicoes: 0, efeito: "",
        descricao: "", imagem: "" },
      reliquias: Object.fromEntries(SLOTS_RELIQUIA.map((s) => [s, { tem: false, nome: "", conjunto: "—" }])),
      esfera_elemento: "",
      conjuntos: Object.fromEntries(LETRAS_CONJUNTO.map((l) => [l, { nome: "", bonus2: "", rolagem: "", efeito4: "" }])),
      ressonancias: { I: "", II: "", III: "", IV: "" },
      tecnica: "",
      inventario: [], creditos: 0,
      memoespirito: { nome: "", conceito: "", funcao: "", elemento: "", pontos: {}, atributo_ataque: "Poder",
        bonus_menores: [], evolucoes: [], memoria_desperta: "", hab_ofensiva: "", hab_auxiliar: "" },
      jogo: { pv: null, temp: 0, energia: 0, ph: null, esforco: 1, memo_ativo: false, memo_pv: null,
        acumulos: {}, condicoes: [], usos: {}, morrendo: { s: 0, f: 0 }, presa: "" },
    };
  }

  /** Completa um personagem (de versão antiga ou importado) com os campos que faltam. */
  function completar(p) {
    const base = modeloVazio();
    const juntar = (alvo, padrao) => {
      for (const [k, v] of Object.entries(padrao)) {
        if (!(k in alvo) || alvo[k] === undefined) alvo[k] = EG.clonar(v);
        else if (v && typeof v === "object" && !Array.isArray(v) && alvo[k] && typeof alvo[k] === "object") juntar(alvo[k], v);
      }
      return alvo;
    };
    juntar(p, base);
    p.habilidades = (p.habilidades || []).map((h) => juntar(h, novaHabilidade()));
    return p;
  }

  function novoPersonagem() {
    const p = modeloVazio();
    p.id = EG.uid();
    p.criado = new Date().toISOString();
    return p;
  }

  /** A Nadir do capítulo 29.7, nível 1 — serve para conferir que a ficha bate com o livro. */
  function exemploNadir() {
    const p = novoPersonagem();
    Object.assign(p, {
      nome: "Nadir (exemplo)", jogador: "",
      conceito: "Uma mecânica de doca orbital que foi expulsa da Aliança por consertar a nave errada.",
      proposito: "Encontrar a doca que a expulsou e provar que o acidente não foi culpa dela.",
      crenca: "Eu não assino nada que eu não consertei.",
      coisa: "O crachá cortado ao meio da doca que a expulsou.",
      nivel: 1, jogadores: 4, raca: "Humano", caminho: "A Destruição", metodo: "Array oficial",
      atributos: { Poder: 15, Agilidade: 13, Vigor: 14, Sincronia: 8, Discernimento: 12, "Presença": 10 },
      bonus_racial: { modo: "Um Atributo (+2)", attr1: "Poder", attr2: "" },
      atributo_habilidade: "Poder", elemento: "Fogo", sintonia: "Discernimento",
      pericias_escolhidas: ["Intimidação", "Mecânica"],
      armadura: "Média", armadura_nome: "Macacão de serviço reforçado nas placas",
      bencaos: ["Pacto da Ruína"],
    });
    p.arma = { nome: "Marreta de doca", categoria: "Pesada", atributo: "Poder", elemento: "", propriedade: "Nenhuma" };
    p.habilidades = [Object.assign(novaHabilidade(), { nome: "Rebarba", alcance: "Curta",
      efeito: "Ela crava a marreta no chão e o impacto sai pelo piso numa linha de brasa." })];
    p.ultimate = { nome: "A Doca Inteira", tipo: "Dano", area: false, resolucao: "Teste de Ataque", efeito: "" };
    p.cone.nivel = 1;
    p.reliquias["Mãos"].tem = true;
    p.reliquias["Botas"].tem = true;
    return p;
  }

  // ---------------------------------------------------------------------------
  // Tradução para o motor (mesmas entradas de build/oraculo_ficha.py)
  // ---------------------------------------------------------------------------
  const ou = (v) => (v === "" || v === undefined ? null : v);

  function paraMotor(p) {
    const reliquias = {};
    for (const s of SLOTS_RELIQUIA) {
      const r = p.reliquias[s];
      if (r && r.tem) reliquias[s] = { conjunto: r.conjunto || "—" };
    }
    const conjuntos = {};
    for (const l of LETRAS_CONJUNTO) {
      const c = p.conjuntos[l];
      conjuntos[l] = { bonus2: ou(c.bonus2), rolagem: ou(c.rolagem) };
    }
    const atributos = {};
    for (const [a, v] of Object.entries(p.atributos)) if (Number.isInteger(v)) atributos[a] = v;
    const memo = p.memoespirito;
    return {
      nivel: p.nivel, jogadores: p.jogadores, raca: ou(p.raca), caminho: ou(p.caminho), metodo: ou(p.metodo),
      atributos: atributos,
      bonus_racial: { modo: ou(p.bonus_racial.modo), attr1: ou(p.bonus_racial.attr1), attr2: ou(p.bonus_racial.attr2) },
      aumentos: p.aumentos,
      atributo_habilidade: ou(p.atributo_habilidade), elemento: ou(p.elemento), sintonia: ou(p.sintonia),
      pericias_escolhidas: p.pericias_escolhidas, eficacia_pericias: p.eficacia_pericias, eficacia_tr: p.eficacia_tr,
      armadura: ou(p.armadura),
      arma: { categoria: ou(p.arma.categoria), atributo: ou(p.arma.atributo), elemento: ou(p.arma.elemento),
        propriedade: ou(p.arma.propriedade) },
      habilidades: p.habilidades.map((h) => ({ nome: h.nome, tipo: ou(h.tipo), nivel: h.nivel, area: !!h.area,
        resolucao: ou(h.resolucao), ress3: !!h.ress3 })),
      ultimate: { nome: p.ultimate.nome, tipo: ou(p.ultimate.tipo), area: !!p.ultimate.area },
      bencaos: p.bencaos.map(ou),
      cone: { nivel: p.cone.nivel, alvo: ou(p.cone.alvo), escolha: ou(p.cone.escolha),
        sobreposicoes: p.cone.sobreposicoes || 0, qual: ou(p.cone.qual) },
      reliquias: reliquias, esfera_elemento: ou(p.esfera_elemento), conjuntos: conjuntos,
      ressonancias: Object.fromEntries(Object.entries(p.ressonancias).filter(([, v]) => v)),
      inventario: p.inventario.map((i) => ({ espaco: Number(i.espaco) || 0, qtd: i.qtd == null ? 1 : i.qtd })),
      pv_atual: p.jogo.pv, memo_ativo: !!p.jogo.memo_ativo, memo_pv: p.jogo.memo_pv,
      forma_avatar: ou(p.forma_avatar), fragmento: ou(p.fragmento), acumulos: p.jogo.acumulos,
      memoespirito: p.caminho === "A Recordação" ? {
        pontos: memo.pontos, atributo_ataque: ou(memo.atributo_ataque), funcao: ou(memo.funcao),
        bonus_menores: memo.bonus_menores, evolucoes: memo.evolucoes, memoria_desperta: ou(memo.memoria_desperta),
      } : null,
    };
  }

  // ---------------------------------------------------------------------------
  // Estado atual
  // ---------------------------------------------------------------------------
  const F = (EG.Ficha = EG.Ficha || {});
  F.P = null;      // personagem aberto
  F.R = null;      // resultado do motor

  /**
   * Para onde `F.salvar()` grava, quando a ficha aberta não é do mapa de fichas.
   *
   * O mapa "explorando-galaxias:fichas" é só das fichas dos jogadores — todo o site o lê
   * assim. Mas a ficha de um NPC é igual à de um personagem jogável e mora na mesa do
   * Mestre, então quem abre uma ficha de fora põe aqui a função que grava, e a tela de
   * editar inteira funciona sem saber de onde a ficha veio. Nulo = mapa de fichas.
   */
  F.aoSalvar = null;

  F.temFicha = () => Object.keys(EG.Armazem.todas()).length > 0;

  F.abrirAtual = function () {
    const todas = EG.Armazem.todas();
    let id = EG.Armazem.atualId();
    if (!todas[id]) id = Object.keys(todas)[0];
    F.aoSalvar = null;                 // esta ficha é do mapa de fichas
    F.P = id ? completar(todas[id]) : null;
    if (F.P) EG.Armazem.definirAtual(F.P.id);
    F.recalcular();
  };

  F.recalcular = function () {
    F.R = F.P ? M.calcular(paraMotor(F.P), C()) : null;
    if (F.P && F.R) {
      const j = F.P.jogo;
      if (j.ph == null) j.ph = F.R.ph_inicio;
    }
  };

  /** Devolve false quando o navegador recusou gravar (espaço cheio). */
  F.salvar = function () {
    if (!F.P) return false;
    if (F.aoSalvar) return F.aoSalvar(F.P) !== false;
    return EG.Armazem.salvar(F.P) !== false;
  };

  F.trocar = function (id) {
    EG.Armazem.definirAtual(id);
    F.abrirAtual();
  };

  F.criar = function (p) {
    F.aoSalvar = null;
    F.P = completar(p || novoPersonagem());
    F.salvar();
    EG.Armazem.definirAtual(F.P.id);
    F.recalcular();
  };

  // ---------------------------------------------------------------------------
  // Leitura e escrita por caminho ("arma.categoria", "habilidades.0.nome")
  // ---------------------------------------------------------------------------
  function obter(obj, caminho) {
    return caminho.split(".").reduce((o, k) => (o == null ? undefined : o[k]), obj);
  }
  function definir(obj, caminho, valor) {
    const partes = caminho.split(".");
    let o = obj;
    for (let i = 0; i < partes.length - 1; i++) {
      if (o[partes[i]] == null || typeof o[partes[i]] !== "object") o[partes[i]] = /^\d+$/.test(partes[i + 1]) ? [] : {};
      o = o[partes[i]];
    }
    o[partes[partes.length - 1]] = valor;
  }
  const idDe = (caminho) => "f-" + caminho.replace(/[^A-Za-z0-9]/g, (c) => "_" + c.charCodeAt(0).toString(16));

  // ---------------------------------------------------------------------------
  // Campos de formulário (HTML)
  // ---------------------------------------------------------------------------
  const H = {};
  H.campo = (rotulo, controle, ajuda, classe) =>
    "<div class='campo " + (classe || "") + "'><span class='rotulo'>" + rotulo + "</span>" + controle +
    (ajuda ? "<span class='ajuda'>" + ajuda + "</span>" : "") + "</div>";

  H.texto = (caminho, o) => {
    o = o || {};
    const v = obter(F.P, caminho);
    // redesenha: campo de texto que muda o desenho da tela (a arte do Cone), e por isso
    // redesenha quando a pessoa sai dele — digitando, só grava, como todos os outros.
    const comum = " id='" + idDe(caminho) + "' data-p='" + esc(caminho) + "' aria-label='" + esc(o.rotulo || caminho) + "'" +
      (o.ph ? " placeholder='" + esc(o.ph) + "'" : "") + (o.redesenha ? " data-redesenha='1'" : "");
    return o.area
      ? "<textarea rows='" + (o.linhas || 2) + "'" + comum + ">" + esc(v) + "</textarea>"
      : "<input type='text'" + comum + " value='" + esc(v) + "'>";
  };

  H.numero = (caminho, o) => {
    o = o || {};
    const v = obter(F.P, caminho);
    return "<input type='number' inputmode='numeric' id='" + idDe(caminho) + "' data-p='" + esc(caminho) + "' data-t='num'" +
      (o.min != null ? " min='" + o.min + "'" : "") + (o.max != null ? " max='" + o.max + "'" : "") +
      (o.passo ? " step='" + o.passo + "'" : "") + " value='" + (v == null ? "" : esc(v)) + "'" +
      " aria-label='" + esc(o.rotulo || caminho) + "'" + (o.classe ? " class='" + o.classe + "'" : "") + ">";
  };

  /** opcoes: lista de valores, ou de [valor, rótulo]. */
  H.lista = (caminho, opcoes, o) => {
    o = o || {};
    const v = obter(F.P, caminho);
    const atual = v == null ? "" : String(v);
    let html = "<select id='" + idDe(caminho) + "' data-p='" + esc(caminho) + "'" + (o.num ? " data-t='num'" : "") +
      " aria-label='" + esc(o.rotulo || caminho) + "'" + (o.desabilitado ? " disabled" : "") + ">";
    if (o.vazio !== false) html += "<option value=''>" + esc(o.vazio || "— escolha —") + "</option>";
    let achou = atual === "";
    for (const op of opcoes) {
      const [valor, rotulo] = Array.isArray(op) ? op : [op, op];
      const sel = String(valor) === atual;
      if (sel) achou = true;
      html += "<option value='" + esc(valor) + "'" + (sel ? " selected" : "") + ">" + esc(rotulo) + "</option>";
    }
    if (!achou) html += "<option value='" + esc(atual) + "' selected>" + esc(atual) + " (fora da lista)</option>";
    return html + "</select>";
  };

  H.marca = (caminho, rotulo, o) => {
    o = o || {};
    const v = !!obter(F.P, caminho);
    return "<label class='marca'><input type='checkbox' id='" + idDe(caminho) + "' data-p='" + esc(caminho) +
      "' data-t='bool'" + (v ? " checked" : "") + (o.desabilitado ? " disabled" : "") + "> <span>" + rotulo + "</span></label>";
  };

  /** Caixa que põe/tira `valor` da lista em `caminho`. */
  H.naLista = (caminho, valor, rotulo, o) => {
    o = o || {};
    const lista = obter(F.P, caminho) || [];
    const marcado = lista.includes(valor);
    return "<label class='marca" + (o.classe ? " " + o.classe : "") + "'><input type='checkbox' id='" + idDe(caminho + "." + valor) +
      "' data-lista='" + esc(caminho) + "' value='" + esc(valor) + "'" + (marcado ? " checked" : "") +
      (o.desabilitado && !marcado ? " disabled" : "") + "> <span>" + rotulo + "</span></label>";
  };

  H.avisos = (codigos) => codigos.length
    ? "<ul class='avisos'>" + codigos.map((c) => "<li>" + esc(M.AVISOS[c] || c) + "</li>").join("") + "</ul>" : "";

  H.dano = (n, face, fixo) => M.textoDano(n, face, fixo);
  /**
   * Espaço com vírgula, como se escreve em português ("0,5"). Arredonda em duas casas porque
   * o campo de Espaço de um item aceita qualquer número: somar três itens de 0,1 daria
   * 0,30000000000000004 na tela, e ninguém carrega isso.
   */
  H.espaco = (n) => String(Math.round((Number(n) || 0) * 100) / 100).replace(".", ",");

  // ---------------------------------------------------------------------------
  // Eventos de formulário (delegados em #app)
  // ---------------------------------------------------------------------------
  let renderPendente = false;
  F.redesenhar = function () {
    if (renderPendente) return;
    renderPendente = true;
    requestAnimationFrame(() => {
      renderPendente = false;
      const voltarFoco = EG.guardarFoco();
      const y = window.scrollY;
      EG.navegar();
      window.scrollTo(0, y);
      voltarFoco();
    });
  };

  function valorDo(el) {
    if (el.dataset.t === "bool") return el.checked;
    if (el.dataset.t === "num") {
      if (el.value === "") return null;
      const n = Number(el.value);
      return Number.isFinite(n) ? (el.step && el.step !== "1" ? n : Math.round(n)) : null;
    }
    return el.value;
  }

  document.addEventListener("input", (ev) => {
    const el = ev.target;
    if (!F.P || !el.dataset || !el.dataset.p || !document.getElementById("app").contains(el)) return;
    if (el.tagName === "SELECT" || el.type === "checkbox" || el.dataset.t === "num") return;
    definir(F.P, el.dataset.p, valorDo(el));
    F.salvar();
  });

  document.addEventListener("change", (ev) => {
    const el = ev.target;
    if (!F.P || !document.getElementById("app").contains(el)) return;
    if (el.dataset.lista) {
      const lista = (obter(F.P, el.dataset.lista) || []).slice();
      const i = lista.indexOf(el.value);
      if (el.checked && i < 0) lista.push(el.value);
      if (!el.checked && i >= 0) lista.splice(i, 1);
      definir(F.P, el.dataset.lista, lista);
    } else if (el.dataset.p) {
      definir(F.P, el.dataset.p, valorDo(el));
      if (el.tagName !== "SELECT" && el.type !== "checkbox" && el.dataset.t !== "num") {
        F.salvar();
        if (el.dataset.redesenha !== "1") return;
      }
    } else return;
    if (F.aoMudar) F.aoMudar(el);
    F.salvar();
    F.recalcular();
    F.redesenhar();
  });

  /**
   * Arte de Cone que não carregou (link errado, site fora do ar, sem internet): a moldura
   * diz o que aconteceu em vez de deixar o ícone de imagem quebrada na ficha. Vale em
   * qualquer tela, porque a moldura é a mesma na ficha e na Área do Mestre.
   */
  document.addEventListener("error", (ev) => {
    const img = ev.target;
    if (!img || img.tagName !== "IMG" || !img.closest || !img.closest(".cone-arte")) return;
    const moldura = img.closest(".cone-arte");
    moldura.classList.add("vazia", "quebrada");
    moldura.innerHTML = "<span>A imagem do Cone não carregou. Confira o endereço em Editar ficha.</span>";
  }, true);

  // ---------------------------------------------------------------------------
  // Barra de personagens (topo das telas Jogar e Editar)
  // ---------------------------------------------------------------------------
  F.barra = function () {
    const todas = Object.values(EG.Armazem.todas()).sort((a, b) => (a.nome || "").localeCompare(b.nome || ""));
    const opcoes = todas.map((p) => "<option value='" + esc(p.id) + "'" + (F.P && p.id === F.P.id ? " selected" : "") + ">" +
      esc(p.nome || "Personagem sem nome") + (p.nivel ? " · nível " + esc(p.nivel) : "") + "</option>").join("");
    return "<div class='barra-personagem'>" +
      (todas.length ? "<label class='sr-only' for='escolher-personagem'>Personagem</label>" +
        "<select id='escolher-personagem'>" + opcoes + "</select>" : "") +
      "<button type='button' class='botao' data-acao='nova'>+ Nova ficha</button>" +
      "<details class='menu'><summary class='botao'>Mais</summary><div class='menu-itens'>" +
      (F.P ? "<button type='button' data-acao='exportar'>Exportar esta ficha</button>" : "") +
      "<button type='button' data-acao='importar'>Importar arquivo de ficha</button>" +
      "<hr>" +
      "<button type='button' data-acao='exportar-tudo'>Exportar tudo (backup)</button>" +
      "<button type='button' data-acao='importar-tudo'>Restaurar um backup</button>" +
      "<hr>" +
      (EG.MesaOnline && EG.MesaOnline.configurada() ? "<button type='button' data-acao='mesa-online'>Mesa online…</button><hr>" : "") +
      "<button type='button' data-acao='exemplo'>Abrir o exemplo (Nadir, 29.7)</button>" +
      (F.P ? "<button type='button' data-acao='imprimir'>Imprimir</button>" : "") +
      (F.P ? "<button type='button' class='perigo' data-acao='excluir'>Excluir esta ficha</button>" : "") +
      "</div></details>" +
      "<input type='file' id='arquivo-importar' accept='.json,application/json' hidden>" +
      "<input type='file' id='arquivo-backup' accept='.json,application/json' hidden>" +
      "</div>";
  };

  function exportar() {
    const nome = (F.P.nome || "personagem").normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^\w-]+/g, "-").replace(/^-+|-+$/g, "");
    const blob = new Blob([JSON.stringify(F.P, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "ficha-" + nome.toLowerCase() + ".json";
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    EG.toast("Ficha exportada. Guarde o arquivo: é o seu backup.");
  }

  function importar(arquivo) {
    const leitor = new FileReader();
    leitor.onload = () => {
      try {
        const p = JSON.parse(leitor.result);
        if (!p || typeof p !== "object" || !("atributos" in p) || !("jogo" in p)) throw new Error("formato");
        const todas = EG.Armazem.todas();
        if (!p.id || todas[p.id]) {
          if (p.id && todas[p.id] && confirm("Já existe esta ficha no navegador. Substituir pela do arquivo?\n(Cancelar importa como uma cópia.)")) {
            // mantém o id: substitui
          } else p.id = EG.uid();
        }
        F.criar(p);
        EG.toast("Ficha <b>" + esc(p.nome || "sem nome") + "</b> importada.");
        F.redesenhar();
      } catch (_) {
        EG.toast("Esse arquivo não é uma ficha deste site.", "erro");
      }
    };
    leitor.readAsText(arquivo);
  }

  document.addEventListener("change", (ev) => {
    if (ev.target.id === "escolher-personagem") { F.trocar(ev.target.value); F.redesenhar(); }
    if (ev.target.id === "arquivo-importar" && ev.target.files[0]) importar(ev.target.files[0]);
  });

  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-acao]");
    if (!b || b.tagName === "SELECT") return;
    const acao = b.dataset.acao;
    const menu = b.closest("details.menu");
    if (menu) menu.open = false;
    if (acao === "nova") { F.criar(); location.hash = "#editar"; F.redesenhar(); }
    else if (acao === "exemplo") { F.criar(exemploNadir()); location.hash = "#jogar"; F.redesenhar(); }
    else if (acao === "exportar") exportar();
    else if (acao === "importar") document.getElementById("arquivo-importar").click();
    else if (acao === "exportar-tudo") EG.exportarTudo();
    else if (acao === "importar-tudo") document.getElementById("arquivo-backup").click();
    else if (acao === "imprimir") { location.hash = "#jogar"; setTimeout(() => window.print(), 300); }
    else if (acao === "excluir") {
      const naMesa = EG.MesaOnline && EG.MesaOnline.estaNaMesa(F.P.id);
      if (confirm("Excluir a ficha de " + (F.P.nome || "personagem sem nome") + "? Isso não tem volta (a não ser que você tenha exportado)." +
        (naMesa ? "\n\nEla também sai da mesa online. A cópia que estiver em outro aparelho continua lá." : ""))) {
        EG.Armazem.excluir(F.P.id);
        F.abrirAtual();
        F.redesenhar();
      }
    } else if (F.acoes && F.acoes[acao]) {
      // Devolver false é "não mexi na ficha, não redesenhe" — é o que uma ação precisa
      // fazer quando ela abre uma janela do sistema (escolher um arquivo): um redesenho
      // aqui trocaria o elemento que está esperando a resposta dessa janela.
      if (F.acoes[acao](b) === false) return;
      F.salvar();
      F.recalcular();
      F.redesenhar();
    }
  });

  // ---------------------------------------------------------------------------
  // Consultas úteis às duas telas
  // ---------------------------------------------------------------------------
  F.caminhoInfo = () => C().caminhos.find((c) => c.caminho === F.P.caminho);
  F.racaInfo = () => C().racas.find((r) => r.raca === F.P.raca);
  F.bencaoInfo = (nome) => C().bencaos.find((b) => b.bencao === nome);
  F.bencaosPossuidas = () => F.P.bencaos.slice(0, Math.floor((F.R.nivel + 1) / 2)).filter(Boolean);
  F.capituloDoCaminho = (caminho) => {
    const i = M && Object.keys(M.CAMINHOS).indexOf(caminho);
    return i >= 0 ? String(7 + i).padStart(2, "0") : "06";
  };
  F.linkBencao = (nome, rotulo) => {
    const b = F.bencaoInfo(nome);
    return b ? EG.Regras.link(F.capituloDoCaminho(b.caminho), b.n + ". " + b.bencao, rotulo || nome) : esc(nome);
  };

  // ---------------------------------------------------------------------------
  // O Cone de Luz desenhado (25.2)
  //
  // Uma função só, usada pela tela Jogar, pela Área do Mestre e pela galeria de Cones do
  // grupo: as três leem a mesma ficha, então o jogador e o Mestre veem sempre a mesma arte,
  // o mesmo Bônus Maior, o mesmo Efeito Condicional e a mesma descrição.
  // ---------------------------------------------------------------------------
  const ROTULO_CONE = ["", "+1 ou +10 PV", "+1 e +10 PV", "+2 ou +25 PV", "+2 e +25 PV", "+3 ou +50 PV"];

  /** Tem algo de Cone para mostrar? (Nível, nome, arte, efeito ou descrição.) */
  F.temCone = function (p) {
    const c = (p && p.cone) || {};
    return !!(c.nivel || c.nome || (c.imagem || "").trim() || c.efeito || c.descricao);
  };

  /** A moldura com a arte do Cone, ou nada se a ficha não tem imagem. */
  F.arteDoCone = function (p, o) {
    o = o || {};
    const url = (p.cone.imagem || "").trim();
    if (!url) return "";
    return "<figure class='cone-arte" + (o.classe ? " " + o.classe : "") + "'><img src='" + esc(url) +
      "' loading='lazy' decoding='async' alt='Arte do Cone de Luz " + esc(p.cone.nome || "sem nome") + "'></figure>";
  };

  /** O Bônus Maior que o Cone está somando na ficha, em texto. Vazio quando não soma nada. */
  F.bonusDoCone = function (p, R) {
    const c = R && R.cone;
    // Sem alvo escolhido o Cone não soma em nada: o motor já calcula o número, mas ele não
    // se aplica a coisa alguma (`coneEm` compara o alvo), então aqui não se anuncia bônus.
    if (!c || !c.alvo) return "";
    const partes = [];
    if (c.numerico) partes.push("+" + c.numerico + " em " + (c.qual || c.alvo));
    if (c.pv) partes.push("+" + c.pv + " PV máximos");
    return partes.join(" e ");
  };

  /**
   * O Cone inteiro: arte, Nome com o Nível, o Bônus Maior que já está somado na ficha, o
   * Efeito Condicional e a descrição.
   * o: {mini (arte pequena ao lado do texto), descricaoFechada (descrição num <details>)}
   */
  F.coneHTML = function (p, R, o) {
    o = o || {};
    const c = p.cone;
    if (!F.temCone(p)) return "";
    const nivel = c.nivel ? Math.max(1, Math.min(5, c.nivel)) : 0;
    const bonus = F.bonusDoCone(p, R);
    const descricao = EG.paragrafos(c.descricao);

    let texto = "<div class='cone-topo'><b>" + esc(c.nome || "Cone de Luz sem nome") + "</b>" +
      (nivel ? " <span class='etiqueta'>Nível " + nivel + "</span> <span class='suave'>" + esc(ROTULO_CONE[nivel]) + "</span>" : "") +
      (c.sobreposicoes ? " <span class='suave'>+" + c.sobreposicoes + " sobrepos" + (c.sobreposicoes > 1 ? "ições" : "ição") + "</span>" : "") +
      (!nivel ? " <span class='etiqueta ruim'>sem Nível</span>" : "") + "</div>";
    if (bonus) texto += "<p class='cone-bonus'>Bônus Maior, sempre ligado: <b>" + esc(bonus) + "</b></p>";
    else if (nivel) texto += "<p class='ajuda'>O Bônus Maior ainda não soma em nada: escolha o alvo em Editar ficha.</p>";
    if (c.efeito) texto += "<p class='efeito'><b>Efeito Condicional:</b> " + esc(c.efeito) + "</p>";
    if (descricao) {
      texto += o.descricaoFechada
        ? "<details class='cone-descricao-fechada'" +
          EG.atributosAbre("cone-desc:" + (o.chave || p.id || c.nome), false) +
          "><summary>Ler a descrição</summary>" +
          "<div class='cone-descricao'>" + descricao + "</div></details>"
        : "<div class='cone-descricao'>" + descricao + "</div>";
    }
    return "<div class='cone" + (o.mini ? " mini" : "") + "'>" + F.arteDoCone(p) +
      "<div class='cone-corpo'>" + texto + "</div></div>";
  };

  /** O que ainda falta escolher para a ficha ficar jogável. */
  F.pendencias = function () {
    const p = F.P, falta = [];
    if (!p.raca) falta.push("Raça");
    if (!p.caminho) falta.push("Caminho");
    if (Object.values(p.atributos).some((v) => v == null)) falta.push("Atributos");
    const cam = F.caminhoInfo();
    if (cam && cam.attr2 && !p.atributo_habilidade) falta.push("Atributo de Habilidade");
    if (!p.elemento) falta.push("Elemento");
    if (!p.armadura) falta.push("Armadura");
    if (!p.arma.categoria) falta.push("Arma");
    if (!p.habilidades.some((h) => h.nome)) falta.push("Habilidade");
    if (!p.ultimate.nome) falta.push("Ultimate");
    if (!p.bencaos[0]) falta.push("primeira Bênção");
    return falta;
  };

  Object.assign(F, { SLOTS_RELIQUIA, LETRAS_CONJUNTO, ROTULO_CONE, novaHabilidade, novoPersonagem, exemploNadir,
    completar, paraMotor, obter, definir, idDe, H });
})();
