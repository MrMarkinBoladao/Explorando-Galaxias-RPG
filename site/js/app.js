/*
 * app.js — Núcleo do site: utilidades, armazenamento das fichas, rolador de dados e rotas.
 * As telas ficam em ficha.js (Jogar e Editar) e regras.js (livro de consulta).
 */
(function () {
  "use strict";

  const EG = (window.EG = window.EG || {});

  // ---------------------------------------------------------------------------
  // Utilidades
  // ---------------------------------------------------------------------------
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g,
    (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const norm = (s) => String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const sinal = (n) => (n >= 0 ? "+" + n : String(n));
  const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  const clonar = (o) => JSON.parse(JSON.stringify(o));

  /** Regex que acha `termo` ignorando acento e maiúscula (para destacar na tela). */
  function regexSemAcento(termos) {
    const classes = { a: "aáàâãä", e: "eéèêë", i: "iíìîï", o: "oóòôõö", u: "uúùûü", c: "cç", n: "nñ" };
    const partes = termos.filter(Boolean).map((t) => norm(t).replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      .replace(/[aeioucn]/g, (ch) => "[" + classes[ch] + classes[ch].toUpperCase() + "]"));
    return partes.length ? new RegExp("(" + partes.join("|") + ")", "gi") : null;
  }

  /** Texto com os termos destacados em <mark>, já escapado. */
  function destacar(texto, termos) {
    const re = regexSemAcento(termos);
    if (!re) return esc(texto);
    return String(texto).split(re).map((p, i) => (i % 2 ? "<mark>" + esc(p) + "</mark>" : esc(p))).join("");
  }

  /**
   * Texto de várias linhas virando parágrafos, já escapado: linha em branco separa
   * parágrafo, linha solta vira quebra. É assim que a descrição de um Cone de Luz mantém
   * na tela a forma com que foi escrita, sem precisar de markdown (que aceitaria HTML).
   */
  function paragrafos(texto, classe) {
    const t = String(texto == null ? "" : texto).replace(/\r\n?/g, "\n").trim();
    if (!t) return "";
    const c = classe ? " class='" + classe + "'" : "";
    return t.split(/\n{2,}/).map((b) => "<p" + c + ">" + esc(b).replace(/\n/g, "<br>") + "</p>").join("");
  }

  // ---------------------------------------------------------------------------
  // Markdown escrito por gente (a história de um personagem)
  //
  // O livro vem do próprio repositório e é renderizado direto (regras.js): é texto
  // confiável, e HTML escrito nele deve valer. Um `.md` colado por um jogador, não — ele
  // pode trazer <script>, <iframe> ou um `onerror=` escondido num atributo. Então aqui o
  // HTML que o marked produz passa por uma peneira: as etiquetas de formatação ficam, as
  // de comportamento somem, e todo atributo que não está na lista é apagado.
  //
  // O HTML é montado num <template>, que o navegador analisa sem rodar script nenhum e sem
  // buscar imagem nenhuma — a limpeza acontece antes de qualquer coisa entrar na página.
  // ---------------------------------------------------------------------------
  const MD_ETIQUETAS = new Set(["P", "BR", "HR", "STRONG", "B", "EM", "I", "U", "S", "DEL", "INS", "MARK",
    "SMALL", "CODE", "PRE", "BLOCKQUOTE", "UL", "OL", "LI", "DL", "DT", "DD", "SUP", "SUB",
    "H1", "H2", "H3", "H4", "H5", "H6", "A", "IMG", "TABLE", "THEAD", "TBODY", "TFOOT", "TR", "TH", "TD",
    "SPAN", "DIV", "DETAILS", "SUMMARY"]);
  const MD_FORA = new Set(["SCRIPT", "STYLE", "IFRAME", "OBJECT", "EMBED", "APPLET", "LINK", "META", "BASE",
    "FORM", "INPUT", "BUTTON", "SELECT", "TEXTAREA", "OPTION", "SVG", "MATH", "NOSCRIPT", "TITLE",
    "AUDIO", "VIDEO", "SOURCE", "TRACK", "TEMPLATE", "CANVAS", "DIALOG", "PORTAL"]);
  const MD_ATRIBUTOS = { A: ["href", "title"], IMG: ["src", "alt", "title"],
    TD: ["colspan", "rowspan"], TH: ["colspan", "rowspan", "scope"], OL: ["start"] };
  const MD_ENDERECO = /^(https?:\/\/|mailto:|#|\/|\.{0,2}\/)/i;

  function limparHtml(raiz) {
    for (const el of Array.from(raiz.querySelectorAll("*"))) {
      // `contains`, e não `isConnected`: dentro de um <template> nada está "conectado" a um
      // documento, e o que precisa ser visto aqui é só se o elemento ainda está na árvore.
      if (!raiz.contains(el)) continue;                    // já saiu junto com o pai
      if (MD_FORA.has(el.tagName)) { el.remove(); continue; }
      if (!MD_ETIQUETAS.has(el.tagName)) { el.replaceWith(...el.childNodes); continue; }  // guarda o texto
      const permitidos = MD_ATRIBUTOS[el.tagName] || [];
      for (const at of Array.from(el.attributes)) {
        const nome = at.name.toLowerCase();
        if (!permitidos.includes(nome)) { el.removeAttribute(at.name); continue; }
        if ((nome === "href" || nome === "src") && !MD_ENDERECO.test(at.value.trim()) &&
          !(nome === "src" && /^data:image\//i.test(at.value.trim()))) el.removeAttribute(at.name);
      }
      if (el.tagName === "A" && el.getAttribute("href")) {
        el.setAttribute("rel", "noopener noreferrer nofollow");
        el.setAttribute("target", "_blank");
      }
      if (el.tagName === "IMG") { el.setAttribute("loading", "lazy"); el.setAttribute("decoding", "async"); }
    }
    return raiz;
  }

  // Converter e peneirar uma história de mil palavras custa caro, e as telas redesenham a
  // cada tecla digitada — a Área do Mestre desenha a história de todo o grupo de uma vez.
  // Como o texto só muda quando alguém o edita, guardar o resultado pelo próprio texto
  // resolve: o mesmo texto nunca é convertido duas vezes.
  const feitos = new Map();

  /** Markdown de um texto escrito por gente, em HTML já peneirado. */
  function markdown(md) {
    const t = String(md == null ? "" : md).trim();
    if (!t) return "";
    if (feitos.has(t)) return feitos.get(t);
    if (!window.marked || !window.marked.parse) return paragrafos(t);   // sem a biblioteca, texto puro
    let bruto;
    try { bruto = window.marked.parse(t, { gfm: true, breaks: false }); } catch (_) { return paragrafos(t); }
    const molde = document.createElement("template");
    molde.innerHTML = bruto;
    limparHtml(molde.content);
    const html = molde.innerHTML;
    if (feitos.size > 40) feitos.clear();
    feitos.set(t, html);
    return html;
  }

  /** Quantas palavras tem um texto — para dizer o tamanho de uma história. */
  const palavras = (t) => (String(t || "").trim().match(/\S+/g) || []).length;

  // ---------------------------------------------------------------------------
  // Armazenamento (localStorage do navegador)
  // ---------------------------------------------------------------------------
  const CHAVE = "explorando-galaxias:fichas";
  const CHAVE_ATUAL = "explorando-galaxias:ficha-atual";

  const Armazem = {
    todas() {
      try { return JSON.parse(localStorage.getItem(CHAVE)) || {}; } catch (_) { return {}; }
    },
    gravarTodas(mapa) {
      try { localStorage.setItem(CHAVE, JSON.stringify(mapa)); return true; } catch (_) {
        toast("Não foi possível salvar no navegador. Use <b>Exportar</b> para guardar a ficha.", "erro");
        return false;
      }
    },
    /**
     * Devolve false quando o navegador recusou gravar (espaço cheio).
     * A mesa online pendura em `EG.aoSalvarFicha` o envio do que mudou. Quem aplica aqui
     * uma mudança que veio de fora grava com gravarTodas(), que não chama o gancho — senão
     * a mudança voltaria para a mesa como se fosse nova.
     */
    salvar(p) {
      const mapa = this.todas();
      p.atualizado = new Date().toISOString();
      mapa[p.id] = p;
      const ok = this.gravarTodas(mapa);
      if (ok && typeof EG.aoSalvarFicha === "function") {
        try { EG.aoSalvarFicha(p); } catch (e) { console.error(e); }
      }
      return ok;
    },
    excluir(id) {
      const mapa = this.todas();
      delete mapa[id];
      this.gravarTodas(mapa);
      if (this.atualId() === id) localStorage.removeItem(CHAVE_ATUAL);
      if (typeof EG.aoExcluirFicha === "function") {
        try { EG.aoExcluirFicha(id); } catch (e) { console.error(e); }
      }
    },
    atualId() { return localStorage.getItem(CHAVE_ATUAL); },
    definirAtual(id) { localStorage.setItem(CHAVE_ATUAL, id); },
  };

  // ---------------------------------------------------------------------------
  // Arquivos: baixar um .json e transformar um nome em nome de arquivo
  // ---------------------------------------------------------------------------

  /** Nome de arquivo seguro: sem acento, sem espaço, sem maiúscula. */
  function fatiarNome(s, padrao) {
    const limpo = norm(s).replace(/[^\w-]+/g, "-").replace(/^-+|-+$/g, "");
    return limpo || padrao || "arquivo";
  }

  /**
   * Um `<input type=file>` criado uma vez e **fora de #app**: as telas redesenham inteiras,
   * e um elemento dentro de #app seria trocado por outro enquanto a janela de escolher
   * arquivo estivesse aberta — aí a resposta dela não chegaria a ninguém.
   */
  function seletorDeArquivo(id, aceita, varios) {
    let el = document.getElementById(id);
    if (!el) {
      el = document.createElement("input");
      el.type = "file";
      el.id = id;
      el.accept = aceita || ".json,application/json";
      if (varios) el.multiple = true;
      el.hidden = true;
      document.body.appendChild(el);
    }
    return el;
  }

  // ---------------------------------------------------------------------------
  // O que está recolhido na tela
  //
  // As telas redesenham inteiras a cada campo mudado, então um <details> aberto pela pessoa
  // se fecharia sozinho na próxima tecla. Quem desenha um recolhível põe `data-abre="chave"`
  // e pergunta `EG.estaAberto(chave, padrao)`; o resto é este par de linhas.
  //
  // Fica em memória de propósito: é estado de tela, não de campanha. Não vai para o
  // localStorage, não vai para o arquivo de mesa e não vai para o backup.
  // ---------------------------------------------------------------------------
  const abertos = {};
  const estaAberto = (chave, padrao) => (chave in abertos ? abertos[chave] : !!padrao);

  document.addEventListener("toggle", (ev) => {
    const d = ev.target;
    if (!d || d.tagName !== "DETAILS" || !d.dataset.abre) return;
    abertos[d.dataset.abre] = d.open;
  }, true);

  /** Marca um recolhível como aberto ou fechado sem esperar o clique da pessoa. */
  function definirAberto(chave, aberto) { abertos[chave] = !!aberto; }

  /** `data-abre` + `open`, pronto para entrar na etiqueta <details>. */
  const atributosAbre = (chave, padrao) =>
    " data-abre='" + esc(chave) + "'" + (estaAberto(chave, padrao) ? " open" : "");

  /**
   * Imprimir abre tudo o que estiver recolhido e devolve ao estado anterior depois. A tela
   * recolhe para não poluir; o papel não tem esse problema, e uma ficha impressa pela
   * metade — sem a história do personagem, sem a descrição do Cone — não serve.
   */
  let recolhidos = [];
  window.addEventListener("beforeprint", () => {
    recolhidos = Array.from(document.querySelectorAll("details:not([open])"))
      .filter((d) => !d.classList.contains("menu"));
    recolhidos.forEach((d) => { d.open = true; });
  });
  window.addEventListener("afterprint", () => {
    recolhidos.forEach((d) => { d.open = false; });
    recolhidos = [];
  });

  /**
   * Guarda o foco e o cursor antes de a tela ser refeita, e devolve quem põe os dois de
   * volta. A tela inteira é trocada a cada redesenho; sem o cursor, quem acabou de clicar
   * no meio de um texto voltaria a digitar do começo dele.
   */
  function guardarFoco() {
    const a = document.activeElement;
    const id = a && a.id;
    if (!id) return () => {};
    let sel = null;
    try {
      if (typeof a.selectionStart === "number") sel = [a.selectionStart, a.selectionEnd, a.selectionDirection, a.value];
    } catch (_) { sel = null; }
    return () => {
      const el = document.getElementById(id);
      if (!el) return;
      el.focus({ preventScroll: true });
      if (sel && el.value === sel[3]) {
        try { el.setSelectionRange(sel[0], sel[1], sel[2] || "none"); } catch (_) { /* campo sem cursor */ }
      }
    };
  }

  /** Redesenha a tela que está aberta, preservando foco e rolagem. */
  function redesenharTela() {
    const t = rotaAtual().tela;
    if (t === "mestre" && EG.Mestre) EG.Mestre.redesenhar();
    else if (EG.Ficha) EG.Ficha.redesenhar();
    else navegar();
  }

  /** Baixa `dados` como .json. Devolve false para servir de retorno de ação. */
  function baixarJSON(nomeArquivo, dados) {
    const blob = new Blob([JSON.stringify(dados, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = nomeArquivo;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    return false;
  }

  // ---------------------------------------------------------------------------
  // Imagens guardadas na ficha (a arte do Cone de Luz)
  //
  // O site não tem servidor: o único lugar para guardar é o localStorage do navegador, que
  // é pequeno (uns 5 MB para a mesa inteira) e só guarda texto. Então a imagem escolhida é
  // redesenhada num <canvas> menor e vira um endereço `data:` — o mesmo texto que entra na
  // ficha, no .json exportado e no backup, e que por isso aparece sozinho na Área do
  // Mestre. Sem encolher, duas fotos de celular enchem o espaço de todas as fichas.
  //
  // Quem preferir não gastar esse espaço pode colar um link (http...) no mesmo campo: a
  // ficha guarda só o endereço, e aí a imagem depende da internet para aparecer.
  // ---------------------------------------------------------------------------
  const IMAGEM_LADO = 560;              // maior lado, em pixels
  const IMAGEM_LIMITE = 220 * 1024;     // teto do texto final, em caracteres

  /** Quantos KB a imagem tem (o peso do arquivo, não o do texto em base64). */
  function pesoDaImagem(url) {
    const s = String(url || ""), i = s.indexOf(",");
    if (!/^data:/.test(s) || i < 0) return 0;
    return Math.max(1, Math.round((s.length - i - 1) * 0.75 / 1024));
  }

  const ehImagemGuardada = (url) => /^data:image\//.test(String(url || ""));

  function encolherImagem(img, lado, qualidade) {
    const maior = Math.max(img.naturalWidth, img.naturalHeight);
    const escala = Math.min(1, lado / maior);
    const tela = document.createElement("canvas");
    tela.width = Math.max(1, Math.round(img.naturalWidth * escala));
    tela.height = Math.max(1, Math.round(img.naturalHeight * escala));
    tela.getContext("2d").drawImage(img, 0, 0, tela.width, tela.height);
    const url = tela.toDataURL("image/webp", qualidade);
    // Navegador sem webp devolve png (ignora o formato pedido): aí vai de jpeg.
    return url.indexOf("data:image/webp") === 0 ? url : tela.toDataURL("image/jpeg", qualidade);
  }

  /**
   * Lê o arquivo escolhido e devolve a imagem já encolhida, em `data:`.
   * `aoPronto(erro, url, kb)` — `erro` é texto pronto para mostrar em um toast.
   */
  function lerImagem(arquivo, aoPronto) {
    if (!arquivo) return;
    if (!/^image\//.test(arquivo.type || "")) {
      aoPronto("Esse arquivo não é uma imagem. Escolha um <b>.png</b>, <b>.jpg</b> ou <b>.webp</b>.");
      return;
    }
    const leitor = new FileReader();
    leitor.onerror = () => aoPronto("Não foi possível ler esse arquivo.");
    leitor.onload = () => {
      const img = new Image();
      img.onerror = () => aoPronto("Não foi possível abrir essa imagem.");
      img.onload = () => {
        if (!img.naturalWidth || !img.naturalHeight) { aoPronto("Essa imagem não tem tamanho definido."); return; }
        let url = "", lado = IMAGEM_LADO, q = 0.82;
        // Tenta até caber: primeiro baixa a qualidade, depois o tamanho.
        for (let i = 0; i < 7 && (!url || url.length > IMAGEM_LIMITE); i++) {
          if (url) { if (q > 0.55) q -= 0.12; else lado = Math.round(lado * 0.8); }
          url = encolherImagem(img, lado, q);
        }
        if (url.length > IMAGEM_LIMITE) {
          aoPronto("Não deu para encolher essa imagem o bastante. Recorte a arte antes de escolher, " +
            "ou cole um link dela no campo de endereço.");
          return;
        }
        aoPronto(null, url, pesoDaImagem(url));
      };
      img.src = leitor.result;
    };
    leitor.readAsDataURL(arquivo);
  }

  // ---------------------------------------------------------------------------
  // Backup completo: todas as fichas e a mesa do Mestre num arquivo só
  // ---------------------------------------------------------------------------
  const CHAVE_MESTRE = "explorando-galaxias:mestre";
  const CHAVE_CONES = "explorando-galaxias:cones";
  const MARCA_BACKUP = "explorando-galaxias:backup";

  function exportarTudo() {
    let mestre = null, cones = null;
    try { mestre = JSON.parse(localStorage.getItem(CHAVE_MESTRE)); } catch (_) { mestre = null; }
    try { cones = JSON.parse(localStorage.getItem(CHAVE_CONES)); } catch (_) { cones = null; }
    const fichas = Armazem.todas();
    const pacote = {
      tipo: MARCA_BACKUP, versao: 1, salvo_em: new Date().toISOString(),
      fichas: fichas, atual: Armazem.atualId(), mestre: mestre, cones: cones,
    };
    const dia = new Date().toISOString().slice(0, 10);
    baixarJSON("explorando-galaxias-backup-" + dia + ".json", pacote);
    const n = Object.keys(fichas).length;
    toast("Backup salvo: <b>" + n + (n === 1 ? " ficha" : " fichas") + "</b>" +
      (mestre ? " e a mesa do Mestre" : "") + ". Guarde o arquivo.");
  }

  function importarTudo(arquivo) {
    const leitor = new FileReader();
    leitor.onload = () => {
      try {
        const p = JSON.parse(leitor.result);
        if (!p || p.tipo !== MARCA_BACKUP || typeof p.fichas !== "object") throw new Error("formato");
        const quantas = Object.keys(p.fichas || {}).length;
        if (!confirm("Restaurar o backup de " + (p.salvo_em || "data desconhecida").slice(0, 10) + "?\n\n" +
          quantas + (quantas === 1 ? " ficha" : " fichas") + (p.mestre ? " e a mesa do Mestre" : "") +
          " vão substituir o que está neste navegador.")) return;
        Armazem.gravarTodas(p.fichas);
        if (p.atual && p.fichas[p.atual]) Armazem.definirAtual(p.atual);
        if (p.mestre) localStorage.setItem(CHAVE_MESTRE, JSON.stringify(p.mestre));
        else localStorage.removeItem(CHAVE_MESTRE);
        // Backup antigo (sem banco de Cones) não apaga o banco que está no navegador.
        if (p.cones) localStorage.setItem(CHAVE_CONES, JSON.stringify(p.cones));
        location.reload();
      } catch (_) {
        toast("Esse arquivo não é um backup deste site. O backup se faz em <b>Mais &gt; Exportar tudo</b>.", "erro");
      }
    };
    leitor.readAsText(arquivo);
  }

  // ---------------------------------------------------------------------------
  // Avisos rápidos (toast)
  // ---------------------------------------------------------------------------
  function toast(html, tipo) {
    const area = document.getElementById("toasts");
    const el = document.createElement("div");
    el.className = "toast " + (tipo || "");
    el.setAttribute("role", "status");
    el.innerHTML = html;
    area.appendChild(el);
    setTimeout(() => el.classList.add("saindo"), tipo === "rolagem" ? 6000 : 3500);
    setTimeout(() => el.remove(), tipo === "rolagem" ? 6400 : 3900);
  }

  // ---------------------------------------------------------------------------
  // Rolador de dados: "d20+6", "6d6+4", "2d20", "1d8+1d6+2" ...
  // ---------------------------------------------------------------------------
  const historico = [];
  const HISTORICO_MAX = 30;

  /**
   * Um dado. O sorteio vem do `crypto.getRandomValues` do navegador — o mesmo gerador que
   * cria senhas e chaves —, e não do `Math.random`, que é estatisticamente bom mas é um
   * gerador de sequência. O "módulo" sozinho daria um viés minúsculo nas faces baixas
   * (2^32 não é múltiplo de 20); por isso o número que cai na sobra é descartado e
   * sorteado de novo: toda face sai com a mesma chance, exatamente.
   */
  const cripto = typeof window !== "undefined" && window.crypto && window.crypto.getRandomValues ? window.crypto : null;
  const sorteio = new Uint32Array(1);
  function d(faces) {
    if (!cripto) return 1 + Math.floor(Math.random() * faces);
    const limite = Math.floor(0x100000000 / faces) * faces;
    let x;
    do { cripto.getRandomValues(sorteio); x = sorteio[0]; } while (x >= limite);
    return 1 + (x % faces);
  }

  /**
   * Lê a expressão de uma rolagem: "d20+6", "6d6+4", "2d6+1d8+3", "d20-1". Devolve
   * {grupos: [{n, f}], mod} ou null se não entendeu. Grupo de dado só soma; o número solto
   * soma ou subtrai. O teto (200 dados, d1000) é para um erro de digitação não travar a página.
   */
  function lerExpressao(expr) {
    const s = String(expr == null ? "" : expr).replace(/\s+/g, "").toLowerCase();
    if (!s || s.length > 40 || !/^[+-]?[\dd+-]+$/.test(s)) return null;
    const termos = s.match(/[+-]?[^+-]+/g) || [];
    if (termos.join("") !== s) return null;
    const grupos = [];
    let mod = 0, quantos = 0;
    for (const t of termos) {
      const neg = t[0] === "-", corpo = t.replace(/^[+-]/, "");
      const m = corpo.match(/^(\d*)d(\d+)$/);
      if (m) {
        const n = m[1] === "" ? 1 : Number(m[1]), f = Number(m[2]);
        if (neg || !(n >= 1) || !(f >= 1) || f > 1000) return null;
        quantos += n;
        grupos.push({ n: n, f: f });
      } else if (/^\d+$/.test(corpo)) {
        mod += (neg ? -1 : 1) * Number(corpo);
      } else return null;
    }
    if (!grupos.length || quantos > 200) return null;
    return { grupos: grupos, mod: mod };
  }

  /** É um d20 só (com ou sem modificador)? É nele que a Vantagem vale (02.4). */
  const ehUmD20 = (e) => !!e && e.grupos.length === 1 && e.grupos[0].n === 1 && e.grupos[0].f === 20;

  /**
   * opcoes: {rotulo, vantagem, fontes, critico ("20" | "19-20")}
   *
   * `vantagem` é true/false ou a lista de quem dá a Vantagem (a Raça, uma Bênção) — lista
   * vazia é rolagem normal. `fontes` é essa mesma lista em texto, para quem passa true.
   * Com Vantagem num d20 (02.4) saem os dois dados e fica o maior: o total já vem com ele,
   * e o outro aparece riscado, para a mesa ver que ele saiu e não contou.
   * Devolve {total, natural} e mostra o resultado.
   */
  function rolar(expr, opcoes) {
    opcoes = opcoes || {};
    const e = lerExpressao(expr);
    if (!e) return null;
    const texto = String(expr).replace(/\s+/g, "");
    const mod = e.mod;
    const emLista = Array.isArray(opcoes.vantagem);
    const vantagem = emLista ? opcoes.vantagem.length > 0 : !!opcoes.vantagem;
    const fontes = emLista ? opcoes.vantagem.join(", ") : String(opcoes.fontes || "");
    let dados = [], natural = null, descartado = null;
    if (ehUmD20(e)) {
      const a = d(20);
      if (vantagem) {
        const b = d(20);
        natural = Math.max(a, b);
        descartado = Math.min(a, b);
      } else natural = a;
      dados = [natural];
    } else {
      for (const g of e.grupos) for (let i = 0; i < g.n; i++) dados.push(d(g.f));
    }
    const total = dados.reduce((x, y) => x + y, 0) + mod;
    let nota = "";
    if (natural !== null) {
      // Com Vantagem, um 20 em qualquer dos dois é crítico (02.4): é o maior, o que contou.
      const faixaCrit = opcoes.critico === "19-20" ? 19 : 20;
      if (natural >= faixaCrit && opcoes.critico) nota = "critico";
      else if (natural === 20) nota = "20";
      else if (natural === 1) nota = "1";
    }
    const r = { rotulo: String(opcoes.rotulo || texto), expr: texto, total: total, natural: natural,
      descartado: descartado, dados: dados.length > 1 ? dados : null, mod: mod, nota: nota,
      fontes: descartado !== null ? fontes : "" };
    mostrarRolagem(r);
    // A mesa online pendura aqui o envio da rolagem para os outros aparelhos.
    if (typeof EG.aoRolar === "function") { try { EG.aoRolar(r); } catch (erro) { console.error(erro); } }
    return { total: total, natural: natural };
  }

  const NOTAS = { critico: " <b class='critico'>Crítico!</b>", 20: " <b class='critico'>20 natural!</b>",
    1: " <b class='falha'>1 natural</b>" };

  /**
   * Uma rolagem desenhada. Ela é montada aqui a partir dos números, e nunca de um HTML
   * pronto, porque a mesa online desenha com esta mesma função a rolagem que veio do
   * aparelho de outra pessoa: tudo o que é texto passa por esc(), e os números por Number().
   * `quem` é o nome de quem rolou, quando não foi neste aparelho.
   */
  function htmlDaRolagem(r, quem) {
    const num = (v) => (Number.isFinite(Number(v)) ? Number(v) : 0);
    const mod = num(r.mod);
    const modTexto = mod ? " " + sinal(mod) : "";
    const temDescarte = r.descartado != null && Number.isFinite(Number(r.descartado));
    const dados = Array.isArray(r.dados) ? r.dados.map(num) : null;
    // O dado que não contou vem primeiro, riscado, e o que contou fica encostado no
    // modificador: "~~4~~ 17 +5" se lê como a conta que deu o total.
    const detalhe = temDescarte
      ? "<s class='dado descartado' title='Não conta: com Vantagem fica o maior'>" + num(r.descartado) +
        "<span class='sr-only'> (não conta)</span></s><b class='dado usado'>" + num(r.natural) + "</b>" + esc(modTexto)
      : esc((dados && dados.length > 1 ? "[" + dados.join(", ") + "]" : String(num(r.total) - mod)) + modTexto);
    const marcaVantagem = temDescarte
      ? " <span class='etiqueta'>Vantagem</span>" + (r.fontes ? " " + esc(r.fontes) : "") : "";
    return "<div class='rolagem-rotulo'>" + (quem ? "<b class='quem-rolou'>" + esc(quem) + "</b> · " : "") +
      esc(r.rotulo || r.expr) + marcaVantagem + "</div>" +
      "<div><span class='rolagem-total'>" + num(r.total) + "</span> <span class='suave'>" + esc(r.expr) + " = " +
      detalhe + "</span>" + (NOTAS[r.nota] || "") + "</div>";
  }

  /** Mostra a rolagem no aviso e no histórico de Rolagens. `aviso: false` só guarda. */
  function mostrarRolagem(r, quem, o) {
    const html = htmlDaRolagem(r, quem);
    historico.unshift(html);
    historico.length = Math.min(historico.length, HISTORICO_MAX);
    if (!o || o.aviso !== false) toast(html, "rolagem");
    const lista = document.getElementById("historico-lista");
    if (lista) lista.innerHTML = historico.map((h) => "<li>" + h + "</li>").join("");
  }

  // Qualquer elemento com data-rolar="expr" vira um botão de rolagem
  document.addEventListener("click", (ev) => {
    const alvo = ev.target.closest("[data-rolar]");
    if (!alvo) return;
    ev.preventDefault();
    rolar(alvo.dataset.rolar, {
      rotulo: alvo.dataset.rotulo, vantagem: alvo.dataset.vantagem === "1", fontes: alvo.dataset.fontes,
      critico: alvo.dataset.critico,
    });
  });

  /**
   * Botão de rolagem pronto.
   * extra: {vantagem, critico}. `vantagem` é true/false ou a lista de quem dá a Vantagem
   * (`vantagem_fontes` do motor): com ela, o clique já rola os dois d20.
   */
  function botaoRolar(expr, rotulo, extra) {
    if (!expr || !/d\d/.test(expr)) return "<span class='valor'>" + esc(expr || "—") + "</span>";
    extra = extra || {};
    const fontes = Array.isArray(extra.vantagem) ? extra.vantagem : [];
    const vantagem = Array.isArray(extra.vantagem) ? fontes.length > 0 : !!extra.vantagem;
    return "<button type='button' class='rolar' data-rolar='" + esc(expr) + "' data-rotulo='" + esc(rotulo || "") + "'" +
      (vantagem ? " data-vantagem='1'" + (fontes.length ? " data-fontes='" + esc(fontes.join(", ")) + "'" : "") : "") +
      (extra.critico ? " data-critico='" + esc(extra.critico) + "'" : "") +
      " title='" + (vantagem ? "Clique para rolar com Vantagem: 2d20, fica o maior" : "Clique para rolar") + "'>" +
      esc(expr) + "</button>";
  }

  /**
   * Teste de Ataque com o botão de Vantagem do lado (02.4). A Vantagem num ataque quase
   * sempre vem da cena — "Vantagem no próximo Teste de Ataque", um alvo que não vê, uma
   * Bênção que acabou de disparar —, e a ficha não tem como saber disso sozinha. Quem sabe
   * é a mesa: o botão do lado rola os dois d20 na hora e fica o maior. Um 20 em qualquer
   * dos dois é crítico, como em toda rolagem com Vantagem.
   */
  function botoesAtaque(expr, rotulo, extra) {
    extra = extra || {};
    if (!expr || !/^d20(?:[+-]\d+)?$/i.test(String(expr).replace(/\s+/g, ""))) return botaoRolar(expr, rotulo, extra);
    return "<span class='rolar-par'>" + botaoRolar(expr, rotulo, extra) +
      "<button type='button' class='rolar vantagem' data-rolar='" + esc(expr) + "' data-rotulo='" + esc(rotulo || "") +
      "' data-vantagem='1'" + (extra.critico ? " data-critico='" + esc(extra.critico) + "'" : "") +
      " title='Rolar com Vantagem: 2d20, fica o maior (2.4)' aria-label='" + esc((rotulo || expr) + " com Vantagem") + "'>" +
      "Vantagem</button></span>";
  }

  // ---------------------------------------------------------------------------
  // Rolagem livre: qualquer expressão, para qualquer pessoa, em qualquer tela
  //
  // Há uma caixa no painel Rolagens (no canto, em toda tela), uma na aba Jogar e uma no
  // Painel do Mestre. Todas passam pelo mesmo `rolar`, então a rolagem livre do jogador vai
  // para a mesa online com o nome dele, igual a qualquer outra.
  // ---------------------------------------------------------------------------
  const ultimaLivre = {};          // o que estava escrito em cada caixa, para o redesenho não apagar

  function rolarLivre(texto, o) {
    o = o || {};
    const expr = String(texto == null ? "" : texto).replace(/\s+/g, "");
    if (!expr) { toast("Escreva a rolagem, como <code>2d6+3</code> ou <code>d20+5</code>.", "erro"); return null; }
    const e = lerExpressao(expr);
    if (!e) {
      toast("Não entendi <b>" + esc(expr) + "</b>. Use <code>NdF+M</code>: <code>d20+5</code>, <code>2d6+3</code>, " +
        "<code>1d8+1d6+2</code>.", "erro");
      return null;
    }
    const vantagem = !!o.vantagem && ehUmD20(e);
    if (o.vantagem && !vantagem) toast("A Vantagem vale para um d20 só (2.4): <b>" + esc(expr) + "</b> foi rolado normal.");
    return rolar(expr, { rotulo: (o.prefixo || "Rolagem livre") + ": " + expr, vantagem: vantagem });
  }

  /**
   * A caixa de rolagem livre: a expressão, a Vantagem e os dados mais usados num clique.
   * `id` identifica a caixa; `o.prefixo` é o começo do rótulo no histórico ("Mestre").
   */
  function formRolagemLivre(id, o) {
    o = o || {};
    const rapidos = o.rapidos || ["d20", "d4", "d6", "d8", "d10", "d12", "d100"];
    return "<div class='rolagem-livre' data-livre-caixa='" + esc(id) + "' data-prefixo='" + esc(o.prefixo || "Rolagem livre") + "'>" +
      "<div class='rolagem-livre-linha'><label class='sr-only' for='" + esc(id) + "'>Rolagem livre</label>" +
      "<input type='text' id='" + esc(id) + "' data-livre='" + esc(id) + "' autocomplete='off' spellcheck='false' " +
      "placeholder='" + esc(o.ph || "2d6+3") + "' value='" + esc(ultimaLivre[id] || "") + "'>" +
      "<label class='marca' title='2d20, fica o maior (2.4)'><input type='checkbox' id='" + esc(id) + "-v' data-livre-v='" +
      esc(id) + "'" + (ultimaLivre[id + "-v"] ? " checked" : "") + "> <span>Vantagem</span></label>" +
      "<button type='button' class='botao primario' data-livre-rolar='" + esc(id) + "'>Rolar</button></div>" +
      "<div class='botoes compactos'>" + rapidos.map((x) => "<button type='button' class='rolar' data-livre-rapido='" +
        esc(x) + "' data-livre-de='" + esc(id) + "' title='Rolar " + esc(x) + "'>" + esc(x) + "</button>").join("") + "</div></div>";
  }

  function caixaLivre(id) {
    const c = document.querySelector("[data-livre-caixa='" + id + "']");
    const v = document.getElementById(id + "-v");
    return { prefixo: c ? c.dataset.prefixo : "", vantagem: !!(v && v.checked), input: document.getElementById(id) };
  }

  document.addEventListener("input", (ev) => {
    const id = ev.target && ev.target.dataset && ev.target.dataset.livre;
    if (id) ultimaLivre[id] = ev.target.value;
  });
  document.addEventListener("change", (ev) => {
    const id = ev.target && ev.target.dataset && ev.target.dataset.livreV;
    if (id) ultimaLivre[id + "-v"] = !!ev.target.checked;
  });

  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-livre-rolar], [data-livre-rapido]");
    if (!b) return;
    ev.preventDefault();
    if (b.dataset.livreRolar) {
      const c = caixaLivre(b.dataset.livreRolar);
      rolarLivre(c.input ? c.input.value : "", { prefixo: c.prefixo, vantagem: c.vantagem });
    } else {
      const c = caixaLivre(b.dataset.livreDe), dado = b.dataset.livreRapido;
      rolarLivre(dado, { prefixo: c.prefixo, vantagem: c.vantagem && dado === "d20" });
    }
  });

  document.addEventListener("keydown", (ev) => {
    const id = ev.key === "Enter" && ev.target && ev.target.dataset && ev.target.dataset.livre;
    if (!id) return;
    ev.preventDefault();
    const c = caixaLivre(id);
    rolarLivre(ev.target.value, { prefixo: c.prefixo, vantagem: c.vantagem });
  });

  // ---------------------------------------------------------------------------
  // Rotas: #jogar, #editar, #regras, #regras?q=..., #regras/capitulo/bloco
  // ---------------------------------------------------------------------------
  const telas = {};
  function registrarTela(nome, fn) { telas[nome] = fn; }

  function rotaAtual() {
    const h = decodeURIComponent(location.hash.replace(/^#/, ""));
    const [caminho, consulta] = h.split("?");
    const partes = caminho.split("/").filter(Boolean);
    const params = new URLSearchParams(consulta || "");
    return { tela: partes[0] || "", partes: partes.slice(1), params: params };
  }

  function navegar() {
    let r = rotaAtual();
    if (!telas[r.tela]) {
      r = { tela: EG.Ficha && EG.Ficha.temFicha() ? "jogar" : "editar", partes: [], params: new URLSearchParams() };
      history.replaceState(null, "", "#" + r.tela);
    }
    document.querySelectorAll("[data-aba]").forEach((a) => {
      const ativa = a.dataset.aba === r.tela;
      a.classList.toggle("ativa", ativa);
      if (ativa) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    document.body.dataset.tela = r.tela;
    try {
      telas[r.tela](r);
    } catch (e) {
      telaComErro(r.tela, e);
    }
  }

  /**
   * Rede de segurança: se desenhar uma tela der erro, mostra o que aconteceu e um jeito de
   * sair. Sem isso, um erro deixa a página sem resposta — clicar na aba não faz nada, porque
   * o `innerHTML` nunca chega a ser trocado — e não há nada na tela dizendo o motivo.
   */
  function telaComErro(tela, erro) {
    console.error("Erro ao desenhar a tela " + tela, erro);
    const app = document.getElementById("app");
    if (!app) return;
    app.innerHTML = "<div class='cartao'><h2>Esta tela não abriu</h2>" +
      "<p>Deu erro ao desenhar <b>" + esc(tela) + "</b>. O motivo mais comum é o navegador estar " +
      "com uma versão do site pela metade. <b>Nada do que está salvo se perde</b>: as fichas e a " +
      "mesa do Mestre continuam aí.</p>" +
      "<div class='botoes'>" +
      "<button type='button' class='botao primario' id='botao-recarregar'>Buscar a versão nova</button>" +
      "<a class='botao' href='#jogar'>Ir para a ficha</a>" +
      "<a class='botao' href='#regras'>Ir para as Regras</a></div>" +
      "<details class='erro-tecnico'><summary>Detalhe técnico (para relatar o problema)</summary>" +
      "<pre>" + esc(tela + "\n" + ((erro && erro.stack) || erro)) + "</pre></details></div>";
    const b = document.getElementById("botao-recarregar");
    if (b) b.onclick = () => atualizarAgora(null);
  }

  window.addEventListener("hashchange", navegar);

  // ---------------------------------------------------------------------------
  // Atualização do site
  //
  // O index.html pede os arquivos com ?v=<selo>, então um site novo já vem inteiro e
  // coerente. Mas o navegador pode ter guardado o próprio index.html antigo — e aí nada
  // muda nem apertando F5. Para isso existe o versao.json: ele é lido direto do servidor
  // (sem cache) e, se o selo de lá for diferente do que está rodando, o aviso aparece.
  // Atualizar NUNCA apaga nada: as fichas e a mesa ficam no localStorage, intactas.
  // ---------------------------------------------------------------------------
  const VERSAO = window.EG_VERSAO || "";
  const CHAVES_DE_DADOS = ["racas", "caminhos", "bencaos", "pericias", "condicoes", "elementos",
    "mestre", "bestiario"];
  let ultimaChecagem = 0;
  let avisando = false;

  function mostrarAviso(nova) {
    const caixa = document.getElementById("aviso-versao");
    if (!caixa || avisando) return;
    avisando = true;
    caixa.hidden = false;
    caixa.innerHTML = "<div class='faixa-versao'><div><b>Saiu uma versão nova do site.</b> " +
      "O seu navegador ainda está com a anterior guardada. " +
      "<span class='suave'>Atualizar não apaga nada: as fichas e a mesa do Mestre continuam salvas.</span></div>" +
      "<div class='botoes compactos'><button type='button' class='botao primario' id='botao-atualizar'>" +
      "Atualizar agora</button>" +
      "<button type='button' class='botao' id='botao-depois'>Depois</button></div></div>";
    document.getElementById("botao-depois").onclick = () => { caixa.hidden = true; };
    document.getElementById("botao-atualizar").onclick = () => atualizarAgora(nova);
  }

  /**
   * Busca de novo, do servidor, a casca e todos os arquivos da versão nova (`cache:
   * "reload"` troca a cópia guardada pela do servidor) e só então recarrega a página.
   */
  async function atualizarAgora(nova) {
    const botao = document.getElementById("botao-atualizar") || document.getElementById("botao-recarregar");
    if (botao) { botao.disabled = true; botao.textContent = "Atualizando…"; }
    if (!nova) {
      // Chamado pela tela de erro: busca a lista de arquivos da versão publicada.
      try {
        const r = await fetch("versao.json?t=" + Date.now(), { cache: "no-store" });
        if (r.ok) nova = await r.json();
      } catch (_) { /* sem rede: recarrega do jeito que der */ }
    }
    const selo = (nova && nova.versao) || Date.now();
    // A casca vai sem query: é esse o endereço que a navegação vai pedir.
    // Os arquivos vão com ?v=<selo novo>, que é como o index.html novo vai pedir cada um.
    const lista = ["./", "index.html", "versao.json"]
      .concat(((nova && nova.arquivos) || []).map((u) => u + "?v=" + selo));
    try {
      await Promise.all(lista.map((u) => fetch(u, { cache: "reload" }).catch(() => null)));
    } catch (_) { /* se a rede falhar, o recarregar abaixo ainda tenta */ }
    location.reload();
  }

  async function checarAtualizacao(forcar) {
    if (location.protocol === "file:" || !VERSAO || VERSAO === "dev") return;
    const agora = Date.now();
    if (!forcar && agora - ultimaChecagem < 120000) return;
    ultimaChecagem = agora;
    try {
      const r = await fetch("versao.json?t=" + agora, { cache: "no-store" });
      if (!r.ok) return;
      const nova = await r.json();
      if (nova && nova.versao && nova.versao !== VERSAO) mostrarAviso(nova);
    } catch (_) { /* sem internet: a cópia que está aberta continua servindo */ }
  }

  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) checarAtualizacao(false);
  });

  document.addEventListener("DOMContentLoaded", () => {
    const faltando = !window.CATALOGO || !window.LIVRO || !window.Motor ? ["tudo"]
      : CHAVES_DE_DADOS.filter((k) => !window.CATALOGO[k]);
    if (faltando.length) {
      // Pode ser cópia local sem gerar_site.py, ou um dados/ velho preso no cache.
      document.getElementById("app").innerHTML = "<div class='cartao'><h2>Os dados do site estão desatualizados</h2>" +
        "<p>O seu navegador carregou uma mistura de arquivo novo e arquivo velho" +
        (faltando[0] === "tudo" ? "" : " (falta <code>" + esc(faltando.join("</code>, <code>")) + "</code>)") +
        ".</p><div class='botoes'><button type='button' class='botao primario' id='botao-recarregar'>" +
        "Buscar a versão nova</button></div>" +
        "<p class='ajuda'>Isso não apaga nada: as fichas e a mesa do Mestre ficam salvas. " +
        "Se você abriu uma cópia local do site, rode <code>python site/gerar_site.py</code> na pasta do projeto.</p></div>";
      const b = document.getElementById("botao-recarregar");
      if (b) b.onclick = () => atualizarAgora(null);
      checarAtualizacao(true);
      return;
    }
    document.getElementById("versao-livro").textContent = "Livro v" + window.CATALOGO.versao;
    // A caixa de rolagem livre do painel Rolagens: fica fora de #app, então vale em toda tela
    // e nenhum redesenho de tela mexe nela.
    const caixa = document.getElementById("rolagem-livre-painel");
    if (caixa) caixa.innerHTML = formRolagemLivre("rolagem-livre-global", { rapidos: ["d20", "d6", "d8", "d10", "d12", "d100"] });
    const selo = document.getElementById("selo-versao");
    if (selo && VERSAO && VERSAO !== "dev") selo.textContent = "Versão do site: " + VERSAO + ".";
    navegar();
    checarAtualizacao(true);
  });

  // Backup completo, chamado pelos menus "Mais" da ficha e da Área do Mestre
  document.addEventListener("change", (ev) => {
    if (ev.target.id === "arquivo-backup" && ev.target.files[0]) importarTudo(ev.target.files[0]);
  });

  Object.assign(EG, { esc, norm, sinal, uid, clonar, destacar, regexSemAcento, paragrafos, markdown,
    limparHtml, palavras, Armazem, toast, rolar, botaoRolar, botoesAtaque, rolarLivre, formRolagemLivre, lerExpressao,
    registrarTela, rotaAtual, navegar, historico,
    mostrarRolagem, htmlDaRolagem,
    exportarTudo, importarTudo, checarAtualizacao, baixarJSON, fatiarNome, seletorDeArquivo,
    redesenharTela, guardarFoco, estaAberto, definirAberto, atributosAbre, lerImagem, pesoDaImagem,
    ehImagemGuardada, VERSAO });
})();
