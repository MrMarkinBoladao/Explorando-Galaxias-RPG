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
    telas[r.tela](r);
  }

  window.addEventListener("hashchange", navegar);
  document.addEventListener("DOMContentLoaded", () => {
    if (!window.CATALOGO || !window.LIVRO || !window.Motor) {
      document.getElementById("app").innerHTML = "<div class='cartao'><h2>Faltam os dados do site</h2>" +
        "<p>Rode <code>python site/gerar_site.py</code> na pasta do projeto e abra a página de novo.</p></div>";
      return;
    }
    document.getElementById("versao-livro").textContent = "Livro v" + window.CATALOGO.versao;
    navegar();
  });

  Object.assign(EG, { esc, norm, sinal, uid, clonar, destacar, regexSemAcento, Armazem, toast, rolar, botaoRolar,
    registrarTela, rotaAtual, navegar, historico });
})();
