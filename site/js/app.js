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
    salvar(p) {
      const mapa = this.todas();
      p.atualizado = new Date().toISOString();
      mapa[p.id] = p;
      this.gravarTodas(mapa);
    },
    excluir(id) {
      const mapa = this.todas();
      delete mapa[id];
      this.gravarTodas(mapa);
      if (this.atualId() === id) localStorage.removeItem(CHAVE_ATUAL);
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
  // Backup completo: todas as fichas e a mesa do Mestre num arquivo só
  // ---------------------------------------------------------------------------
  const CHAVE_MESTRE = "explorando-galaxias:mestre";
  const MARCA_BACKUP = "explorando-galaxias:backup";

  function exportarTudo() {
    let mestre = null;
    try { mestre = JSON.parse(localStorage.getItem(CHAVE_MESTRE)); } catch (_) { mestre = null; }
    const fichas = Armazem.todas();
    const pacote = {
      tipo: MARCA_BACKUP, versao: 1, salvo_em: new Date().toISOString(),
      fichas: fichas, atual: Armazem.atualId(), mestre: mestre,
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
  // Rolador de dados: "d20+6", "6d6+4", "2d20" ...
  // ---------------------------------------------------------------------------
  const historico = [];
  const d = (faces) => 1 + Math.floor(Math.random() * faces);

  /**
   * opcoes: {rotulo, vantagem (bool), critico ("20" | "19-20"), teste (bool: é d20)}
   * Devolve {total, natural} e mostra o resultado.
   */
  function rolar(expr, opcoes) {
    opcoes = opcoes || {};
    const m = String(expr).replace(/\s+/g, "").match(/^(\d*)d(\d+)([+-]\d+)?$/i);
    if (!m) return null;
    const qtd = Number(m[1] || 1), faces = Number(m[2]), mod = Number(m[3] || 0);
    let dados = [], natural = null, extra = "";
    if (qtd === 1 && faces === 20) {
      const a = d(20);
      if (opcoes.vantagem) {
        const b = d(20);
        natural = Math.max(a, b);
        extra = " <span class='suave'>(Vantagem: " + a + " e " + b + ")</span>";
      } else natural = a;
      dados = [natural];
    } else {
      for (let i = 0; i < qtd; i++) dados.push(d(faces));
    }
    const soma = dados.reduce((x, y) => x + y, 0);
    const total = soma + mod;
    let nota = "";
    if (natural !== null) {
      const faixaCrit = opcoes.critico === "19-20" ? 19 : 20;
      if (natural >= faixaCrit && opcoes.critico) nota = " <b class='critico'>Crítico!</b>";
      else if (natural === 20) nota = " <b class='critico'>20 natural!</b>";
      else if (natural === 1) nota = " <b class='falha'>1 natural</b>";
    }
    const detalhe = (qtd > 1 ? "[" + dados.join(", ") + "]" : String(soma)) + (mod ? " " + sinal(mod) : "");
    const html = "<div class='rolagem-rotulo'>" + esc(opcoes.rotulo || expr) + "</div>" +
      "<div><span class='rolagem-total'>" + total + "</span> <span class='suave'>" + esc(expr) + " = " +
      esc(detalhe) + "</span>" + extra + nota + "</div>";
    historico.unshift(html);
    historico.length = Math.min(historico.length, 15);
    toast(html, "rolagem");
    const lista = document.getElementById("historico-lista");
    if (lista) lista.innerHTML = historico.map((h) => "<li>" + h + "</li>").join("");
    return { total: total, natural: natural };
  }

  // Qualquer elemento com data-rolar="expr" vira um botão de rolagem
  document.addEventListener("click", (ev) => {
    const alvo = ev.target.closest("[data-rolar]");
    if (!alvo) return;
    ev.preventDefault();
    rolar(alvo.dataset.rolar, {
      rotulo: alvo.dataset.rotulo, vantagem: alvo.dataset.vantagem === "1", critico: alvo.dataset.critico,
    });
  });

  /** Botão de rolagem pronto. */
  function botaoRolar(expr, rotulo, extra) {
    if (!expr || !/d\d/.test(expr)) return "<span class='valor'>" + esc(expr || "—") + "</span>";
    extra = extra || {};
    return "<button type='button' class='rolar' data-rolar='" + esc(expr) + "' data-rotulo='" + esc(rotulo || "") +
      "'" + (extra.vantagem ? " data-vantagem='1'" : "") + (extra.critico ? " data-critico='" + esc(extra.critico) + "'" : "") +
      " title='Clique para rolar'>" + esc(expr) + "</button>";
  }

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
    const selo = document.getElementById("selo-versao");
    if (selo && VERSAO && VERSAO !== "dev") selo.textContent = "Versão do site: " + VERSAO + ".";
    navegar();
    checarAtualizacao(true);
  });

  // Backup completo, chamado pelos menus "Mais" da ficha e da Área do Mestre
  document.addEventListener("change", (ev) => {
    if (ev.target.id === "arquivo-backup" && ev.target.files[0]) importarTudo(ev.target.files[0]);
  });

  Object.assign(EG, { esc, norm, sinal, uid, clonar, destacar, regexSemAcento, Armazem, toast, rolar, botaoRolar,
    registrarTela, rotaAtual, navegar, historico, exportarTudo, importarTudo, checarAtualizacao,
    baixarJSON, fatiarNome, VERSAO });
})();
