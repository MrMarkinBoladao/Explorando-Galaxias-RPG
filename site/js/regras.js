/*
 * regras.js — O livro de consulta: pesquisa instantânea e leitura dos capítulos.
 * Os textos vêm de dados/livro.js (gerado por site/gerar_site.py a partir de livro-v1.0/).
 */
(function () {
  "use strict";

  const EG = window.EG;
  const { esc, norm, destacar } = EG;
  const LIVRO = () => window.LIVRO;
  const MAX_RESULTADOS = 40;

  // ---------------------------------------------------------------------------
  // Índice de pesquisa
  // ---------------------------------------------------------------------------
  function textoPlano(md) {
    return md
      .replace(/!\[[^\]]*\]\([^)]*\)/g, "")                    // imagens
      .replace(/^```.*$/gm, "")                                // cercas de código
      .replace(/^[ \t]*>?[ \t]*\|?[ \t]*:?-{3,}[-|: \t]*$/gm, "")  // linha separadora de tabela
      .replace(/^#{1,6}[ \t]+/gm, "")                          // títulos
      .replace(/^[ \t]*>[ \t]?/gm, "")                         // citações
      .replace(/\\\|/g, "\u0001")                              // pipe escapado
      .replace(/^[ \t]*\|[ \t]?|[ \t]?\|[ \t]*$/gm, "")          // bordas da tabela
      .replace(/[ \t]*\|[ \t]*/g, " · ")                        // colunas
      .replace(/\u0001/g, "|")
      .replace(/\*\*|__|`/g, "")
      .replace(/(^|[\s(])\*(\S[^*\n]*?)\*(?=[\s).,;:!?]|$)/gm, "$1$2")
      .replace(/^[ \t]*[-*][ \t]+/gm, "• ")
      .replace(/^[ \t]*---[ \t]*$/gm, "");
  }

  let indice = null;
  function montarIndice() {
    if (indice) return indice;
    indice = [];
    for (const cap of LIVRO().capitulos) {
      const capN = norm(cap.titulo);
      for (const b of cap.blocos) {
        const linhas = textoPlano(b.md).split("\n").map((l) => l.trim()).filter(Boolean);
        if (b.titulo && linhas.length && norm(linhas[0]) === norm(b.titulo)) linhas.shift();
        if (!linhas.length) continue;          // só o título: o conteúdo está nos blocos de baixo
        indice.push({
          cap: cap, bloco: b, linhas: linhas, linhasN: linhas.map(norm),
          tituloN: norm(b.titulo), paiN: norm(b.pai), capN: capN,
        });
      }
    }
    for (const e of indice) e.textoN = e.linhasN.join("\n");
    return indice;
  }

  const contarOcorrencias = (texto, termo) => {
    let n = 0, i = texto.indexOf(termo);
    while (i !== -1 && n < 6) { n++; i = texto.indexOf(termo, i + termo.length); }
    return n;
  };
  const inicioDePalavra = (texto, termo) => new RegExp("(^|[^a-z0-9])" + termo.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).test(texto);

  function pesquisar(consulta) {
    const q = norm(consulta).trim();
    const termos = q.split(/\s+/).filter((t) => t.length > 0);
    if (!termos.length) return [];
    const resultados = [];
    for (const e of montarIndice()) {
      const onde = e.tituloN + "\n" + e.paiN + "\n" + e.capN + "\n" + e.textoN;
      if (!termos.every((t) => onde.includes(t))) continue;
      let pontos = 0;
      for (const t of termos) {
        if (e.tituloN.includes(t)) pontos += inicioDePalavra(e.tituloN, t) ? 14 : 8;
        if (e.paiN.includes(t) || e.capN.includes(t)) pontos += 3;
        pontos += contarOcorrencias(e.textoN, t);
      }
      if (e.tituloN === q) pontos += 40;
      if (termos.length > 1 && e.tituloN.includes(q)) pontos += 25;
      if (termos.length > 1 && e.textoN.includes(q)) pontos += 8;
      // Linha que começa pelo termo: definição de glossário ou linha de tabela
      let melhor = -1, melhorPontos = -1;
      e.linhasN.forEach((l, i) => {
        let p = termos.filter((t) => l.includes(t)).length * 2;
        const sem = l.replace(/^[•·\s]+/, "");
        if (sem.startsWith(q)) p += 5;
        if (p > melhorPontos) { melhorPontos = p; melhor = i; }
      });
      if (melhor >= 0 && e.linhasN[melhor].replace(/^[•·\s]+/, "").startsWith(q)) pontos += 12;
      if (!e.bloco.titulo || e.bloco.nivel === 1) pontos -= 2;
      resultados.push({ e: e, pontos: pontos, linha: melhor });
    }
    resultados.sort((a, b) => b.pontos - a.pontos);
    return resultados;
  }

  function trecho(linha, termos, max) {
    max = max || 240;
    if (linha.length <= max) return linha;
    const ln = norm(linha);
    let pos = Math.min(...termos.map((t) => { const i = ln.indexOf(t); return i < 0 ? Infinity : i; }));
    if (!isFinite(pos)) pos = 0;
    const ini = Math.max(0, pos - 70);
    return (ini > 0 ? "…" : "") + linha.slice(ini, ini + max) + (ini + max < linha.length ? "…" : "");
  }

  // ---------------------------------------------------------------------------
  // Links para as regras (usados também pela ficha)
  // ---------------------------------------------------------------------------
  function capituloPorNumero(num) {
    return LIVRO().capitulos.find((c) => c.num === String(num).padStart(2, "0"));
  }

  /** Bloco do capítulo `num` cujo título contém `termo` (exato tem preferência). */
  function acharBloco(num, termo) {
    const cap = capituloPorNumero(num);
    if (!cap) return null;
    const t = norm(termo);
    const b = cap.blocos.find((x) => norm(x.titulo) === t) ||
      cap.blocos.find((x) => norm(x.titulo).replace(/^\d+\.\s*/, "") === t) ||
      cap.blocos.find((x) => norm(x.titulo).includes(t));
    return b ? { cap: cap, bloco: b } : null;
  }

  function href(num, termo) {
    const r = acharBloco(num, termo);
    return r ? "#regras/" + r.cap.id + "/" + r.bloco.id : "#regras?q=" + encodeURIComponent(termo);
  }

  /** <a> "ver regra" pronto. */
  function link(num, termo, rotulo) {
    return "<a class='link-regra' href='" + esc(href(num, termo)) + "' title='Abrir a regra no livro'>" +
      esc(rotulo || "ver regra") + "</a>";
  }

  // ---------------------------------------------------------------------------
  // Telas
  // ---------------------------------------------------------------------------
  const app = () => document.getElementById("app");
  let ultimaConsulta = "";
  const htmlCapitulo = {};

  function renderizarMarkdown(md) {
    return window.marked.parse(md, { gfm: true, breaks: false });
  }

  function capituloHtml(cap) {
    if (!htmlCapitulo[cap.id]) {
      htmlCapitulo[cap.id] = cap.blocos.map((b) =>
        "<section class='bloco' id='" + cap.id + "--" + b.id + "'>" + renderizarMarkdown(b.md) + "</section>").join("");
    }
    return htmlCapitulo[cap.id];
  }

  function telaPesquisa(r) {
    const q = r.params.get("q") || "";
    let caixa = document.getElementById("busca-regras");
    document.body.dataset.subtela = "pesquisa";
    if (!caixa) {
      app().innerHTML =
        "<div class='regras'>" +
        "<div class='busca'>" +
        "<label for='busca-regras' class='sr-only'>Pesquisar nas regras</label>" +
        "<input id='busca-regras' type='search' autocomplete='off' spellcheck='false' " +
        "placeholder='Pesquise uma regra: esquiva, morrendo, cone de luz, queimadura…'>" +
        "<p class='dica'>Dica: aperte <kbd>/</kbd> em qualquer lugar para pesquisar. O livro inteiro (v" +
        esc(LIVRO().versao) + ") está aqui.</p></div>" +
        "<div id='resultados' aria-live='polite'></div></div>";
      caixa = document.getElementById("busca-regras");
      caixa.addEventListener("input", () => {
        const v = caixa.value;
        history.replaceState(null, "", "#regras" + (v.trim() ? "?q=" + encodeURIComponent(v) : ""));
        mostrarResultados(v);
      });
      caixa.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter") {
          const primeiro = document.querySelector("#resultados a.resultado");
          if (primeiro) location.hash = primeiro.getAttribute("href").slice(1);
        }
      });
    }
    if (caixa.value !== q) caixa.value = q;
    mostrarResultados(q);
    if (!("ontouchstart" in window)) caixa.focus();
  }

  function mostrarResultados(consulta) {
    ultimaConsulta = consulta;
    const alvo = document.getElementById("resultados");
    if (!alvo) return;
    if (!consulta.trim()) { alvo.innerHTML = sumario(); return; }
    const termos = norm(consulta).split(/\s+/).filter(Boolean);
    const res = pesquisar(consulta);
    if (!res.length) {
      alvo.innerHTML = "<p class='vazio'>Nada encontrado para <b>" + esc(consulta) + "</b>. Tente outra palavra, ou uma palavra só.</p>";
      return;
    }
    const q = encodeURIComponent(consulta);
    alvo.innerHTML = "<p class='contagem'>" + res.length + (res.length === 1 ? " trecho" : " trechos") +
      (res.length > MAX_RESULTADOS ? " · mostrando os " + MAX_RESULTADOS + " mais relevantes" : "") + "</p>" +
      res.slice(0, MAX_RESULTADOS).map((x) => {
        const e = x.e;
        let titulo = e.bloco.titulo || e.cap.titulo;
        // No glossário os blocos são letras ("E"): o título útil é o termo da linha achada
        if (titulo.length <= 2 && x.linha >= 0) titulo = e.linhas[x.linha].split(" · ")[0];
        const caminho = "Cap. " + e.cap.num + " · " + e.cap.titulo + (e.bloco.pai ? " › " + e.bloco.pai : "");
        const linha = x.linha >= 0 ? trecho(e.linhas[x.linha], termos) : "";
        return "<a class='resultado' href='#regras/" + e.cap.id + "/" + e.bloco.id + "?q=" + q + "'>" +
          "<span class='res-caminho'>" + destacar(caminho, termos) + "</span>" +
          "<span class='res-titulo'>" + destacar(titulo, termos) + "</span>" +
          (linha ? "<span class='res-trecho'>" + destacar(linha, termos) + "</span>" : "") + "</a>";
      }).join("");
  }

  function sumario() {
    return "<h2 class='sumario-titulo'>Capítulos</h2><ol class='sumario'>" + LIVRO().capitulos.map((c) => {
      const secoes = c.blocos.filter((b) => b.nivel === 2 && !/^resumo do capítulo$/i.test(b.titulo));
      return "<li><a href='#regras/" + c.id + "'><span class='num'>" + esc(c.num) + "</span> " + esc(c.titulo) + "</a>" +
        (secoes.length ? "<span class='secoes'>" + secoes.slice(0, 8).map((b) =>
          "<a href='#regras/" + c.id + "/" + b.id + "'>" + esc(b.titulo) + "</a>").join("") +
          (secoes.length > 8 ? "<span class='suave'>+" + (secoes.length - 8) + "</span>" : "") + "</span>" : "") + "</li>";
    }).join("") + "</ol>";
  }

  function telaCapitulo(r) {
    document.body.dataset.subtela = "capitulo";
    const caps = LIVRO().capitulos;
    const i = caps.findIndex((c) => c.id === r.partes[0]);
    if (i < 0) { location.hash = "#regras"; return; }
    const cap = caps[i];
    const q = r.params.get("q") || "";
    const voltar = q ? "#regras?q=" + encodeURIComponent(q) : "#regras";
    const anterior = caps[i - 1], proximo = caps[i + 1];
    const secoes = cap.blocos.filter((b) => b.nivel === 2);
    app().innerHTML =
      "<div class='regras leitor'>" +
      "<nav class='leitor-topo' aria-label='Navegação do livro'>" +
      "<a class='botao' href='" + esc(voltar) + "'>« " + (q ? "Voltar aos resultados" : "Todos os capítulos") + "</a>" +
      (secoes.length ? "<details class='indice-cap'><summary>Seções deste capítulo</summary><ul>" +
        secoes.map((b) => "<li><a href='#regras/" + cap.id + "/" + b.id + "'>" + esc(b.titulo) + "</a></li>").join("") +
        "</ul></details>" : "") + "</nav>" +
      "<article class='capitulo'>" + capituloHtml(cap) + "</article>" +
      "<nav class='leitor-rodape'>" +
      (anterior ? "<a class='botao' href='#regras/" + anterior.id + "'>« " + esc(anterior.num + " " + anterior.titulo) + "</a>" : "<span></span>") +
      (proximo ? "<a class='botao' href='#regras/" + proximo.id + "'>" + esc(proximo.num + " " + proximo.titulo) + " »</a>" : "") +
      "</nav></div>";
    const artigo = app().querySelector(".capitulo");
    artigo.querySelectorAll("table").forEach((t) => {
      const caixa = document.createElement("div");
      caixa.className = "tabela";
      t.parentNode.insertBefore(caixa, t);
      caixa.appendChild(t);
    });
    artigo.querySelectorAll("img").forEach((img) => { img.loading = "lazy"; img.decoding = "async"; });
    const alvo = r.partes[1] ? document.getElementById(cap.id + "--" + r.partes[1]) : null;
    if (alvo) {
      alvo.classList.add("alvo");
      if (q) marcarTermos(alvo, norm(q).split(/\s+/).filter(Boolean));
      requestAnimationFrame(() => alvo.scrollIntoView({ block: "start" }));
    } else {
      window.scrollTo(0, 0);
    }
  }

  function marcarTermos(raiz, termos) {
    const re = EG.regexSemAcento(termos);
    if (!re) return;
    const andador = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT);
    const nos = [];
    while (andador.nextNode()) nos.push(andador.currentNode);
    for (const no of nos) {
      if (!re.test(no.nodeValue)) continue;
      re.lastIndex = 0;
      const span = document.createElement("span");
      span.innerHTML = EG.destacar(no.nodeValue, termos);
      no.parentNode.replaceChild(span, no);
    }
  }

  function tela(r) {
    if (r.partes[0]) telaCapitulo(r); else telaPesquisa(r);
  }

  // "/" abre a pesquisa de qualquer lugar
  document.addEventListener("keydown", (ev) => {
    if (ev.key !== "/" || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const t = ev.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
    ev.preventDefault();
    if (EG.rotaAtual().tela === "regras" && !EG.rotaAtual().partes.length) {
      document.getElementById("busca-regras").focus();
    } else {
      location.hash = "#regras" + (ultimaConsulta ? "?q=" + encodeURIComponent(ultimaConsulta) : "");
    }
  });

  EG.registrarTela("regras", tela);
  EG.Regras = { pesquisar, acharBloco, href, link, textoPlano };
})();
