/*
 * cones.js — O banco de Cones de Luz.
 *
 * Um Cone de Luz é equipamento de marco (25.1): o Mestre concede, e trocar é opcional. Na
 * prática isso quer dizer que a mesa acumula Cones — o que o personagem usa hoje, o que ele
 * usava antes, o que o Mestre já escreveu e ainda não entregou. A ficha guarda **um** Cone,
 * o equipado; este banco guarda a coleção, à parte das fichas, e serve para duas coisas:
 *
 *  - o jogador escolher qual Cone está usando, sem reescrever nome, efeito, arte e história;
 *  - o Mestre montar os Cones antes da sessão e entregar o próximo quando a faixa virar.
 *
 * Mora numa chave própria do navegador ("explorando-galaxias:cones"), vai no backup
 * completo e se exporta em .json — que é como um banco sai do navegador do Mestre e entra
 * no do jogador. Equipar **copia** o Cone para a ficha: daí para frente são duas coisas
 * separadas, como acontece com um NPC vindo de uma coleção pronta.
 */
(function () {
  "use strict";

  const EG = window.EG;
  const { esc, norm } = EG;

  const CHAVE = "explorando-galaxias:cones";
  const MARCA = "explorando-galaxias:cones";

  const C = (EG.Cones = EG.Cones || {});
  C.MARCA = MARCA;

  // ---------------------------------------------------------------------------
  // Modelo e armazenamento
  // ---------------------------------------------------------------------------
  function modeloVazio() {
    return { id: "", nome: "", nivel: null, alvo: "", qual: "", escolha: "Numérico", sobreposicoes: 0,
      efeito: "", descricao: "", imagem: "", nota: "" };
  }

  const texto = (v) => (typeof v === "string" ? v : v == null ? "" : String(v));

  /** Completa um Cone solto (de arquivo, de ficha ou de versão antiga). */
  function completar(bruto) {
    const c = Object.assign(modeloVazio(), bruto && typeof bruto === "object" ? bruto : {});
    c.id = texto(c.id) || EG.uid();
    for (const k of ["nome", "alvo", "qual", "escolha", "efeito", "descricao", "imagem", "nota"]) c[k] = texto(c[k]);
    if (!c.escolha) c.escolha = "Numérico";
    const n = Number(c.nivel);
    c.nivel = Number.isFinite(n) && n >= 1 && n <= 5 ? Math.round(n) : null;
    const s = Number(c.sobreposicoes);
    c.sobreposicoes = Number.isFinite(s) && s > 0 ? Math.min(5, Math.round(s)) : 0;
    return c;
  }
  C.completar = completar;

  C.todos = function () {
    let bruto = null;
    try { bruto = JSON.parse(localStorage.getItem(CHAVE)); } catch (_) { bruto = null; }
    const lista = bruto && Array.isArray(bruto.cones) ? bruto.cones : Array.isArray(bruto) ? bruto : [];
    return lista.map(completar);
  };

  C.quantos = () => C.todos().length;
  C.achar = (id) => C.todos().find((c) => c.id === id) || null;

  /** Devolve false quando o navegador recusou gravar (espaço cheio). */
  C.gravar = function (lista) {
    try {
      localStorage.setItem(CHAVE, JSON.stringify({ tipo: MARCA, versao: 1, cones: lista }));
      return true;
    } catch (_) {
      EG.toast("Não cabe mais no navegador. Tire a arte de algum Cone do banco, ou exporte o banco " +
        "em <b>.json</b> e apague o que não usa.", "erro");
      return false;
    }
  };

  /** Os campos de Cone de uma ficha, sem o resto dela. */
  C.daFicha = function (p) {
    const c = (p && p.cone) || {};
    return completar({ nome: c.nome, nivel: c.nivel, alvo: c.alvo, qual: c.qual, escolha: c.escolha,
      sobreposicoes: c.sobreposicoes, efeito: c.efeito, descricao: c.descricao, imagem: c.imagem });
  };

  /**
   * Guarda um Cone no banco. Dois Cones com o **mesmo nome** são o mesmo Cone: o segundo
   * atualiza o primeiro, em vez de encher o banco de quase-duplicatas. Devolve
   * `{ok, novo, cone}` — `novo` é false quando atualizou um que já estava lá.
   */
  C.guardar = function (cone) {
    const c = completar(cone);
    const lista = C.todos();
    const i = c.nome ? lista.findIndex((x) => norm(x.nome) === norm(c.nome)) : -1;
    let novo = true;
    if (i >= 0) { c.id = lista[i].id; c.nota = c.nota || lista[i].nota; lista[i] = c; novo = false; }
    else lista.unshift(c);
    return { ok: C.gravar(lista), novo: novo, cone: c };
  };

  C.remover = function (id) {
    const lista = C.todos().filter((c) => c.id !== id);
    return C.gravar(lista);
  };

  /** Copia um Cone do banco para a ficha. A ficha fica com a cópia dela. */
  C.aplicar = function (p, cone) {
    const c = completar(cone);
    Object.assign(p.cone, { nome: c.nome, nivel: c.nivel, alvo: c.alvo, qual: c.qual, escolha: c.escolha,
      sobreposicoes: c.sobreposicoes, efeito: c.efeito, descricao: c.descricao, imagem: c.imagem });
    return p;
  };

  // ---------------------------------------------------------------------------
  // Arquivos (.json)
  // ---------------------------------------------------------------------------
  C.exportar = function (lista, nomeDoArquivo) {
    const limpa = lista.map((c) => {
      const x = completar(c);
      delete x.id;                               // id é deste navegador, não do arquivo
      return x;
    });
    return EG.baixarJSON("cones-" + EG.fatiarNome(nomeDoArquivo || "da-mesa", "da-mesa") + ".json",
      { tipo: MARCA, versao: 1, nome: nomeDoArquivo || "", cones: limpa });
  };

  /**
   * Os Cones que há num arquivo. Aceita o pacote que a exportação grava, uma lista solta, um
   * Cone sozinho, um backup completo, e também **uma ficha de personagem ou de NPC** — daí
   * ele pega o Cone equipado, que é como se rouba um Cone bonito de uma coleção pronta.
   */
  C.doArquivo = function (dado) {
    if (!dado || typeof dado !== "object") return [];
    if (Array.isArray(dado)) return dado.filter((x) => x && typeof x === "object");
    if (Array.isArray(dado.cones)) return dado.cones.filter((x) => x && typeof x === "object");
    if (dado.cones && Array.isArray(dado.cones.cones)) return dado.cones.cones;   // backup completo
    if (dado.cone && typeof dado.cone === "object") return [dado.cone];           // ficha ou NPC
    if (dado.npcs || dado.fichas) {                                               // mesa ou backup
      const fichas = [].concat(Object.values(dado.fichas || {}), dado.npcs || []);
      return fichas.map((p) => p && p.cone).filter((c) => c && typeof c === "object");
    }
    if ("nome" in dado || "nivel" in dado) return [dado];                         // um Cone sozinho
    return [];
  };

  /**
   * Importa somando ao banco: nunca apaga o que já está lá. Cone com nome que já existe
   * atualiza aquele; Cone sem nome nenhum é descartado (não teria como ser escolhido).
   */
  C.importar = function (dado) {
    const achados = C.doArquivo(dado).map(completar);
    const comNome = achados.filter((c) => c.nome.trim());
    const semNome = achados.length - comNome.length;
    const lista = C.todos();
    let novos = 0, atualizados = 0;
    for (const c of comNome) {
      const i = lista.findIndex((x) => norm(x.nome) === norm(c.nome));
      if (i >= 0) { c.id = lista[i].id; lista[i] = c; atualizados++; } else { lista.push(c); novos++; }
    }
    const ok = comNome.length ? C.gravar(lista) : true;
    return { ok: ok, novos: novos, atualizados: atualizados, semNome: semNome, achados: achados.length };
  };

  // ---------------------------------------------------------------------------
  // Pedaços de tela, compartilhados pela ficha e pela Área do Mestre
  // ---------------------------------------------------------------------------
  /** "+1 e +10 PV em Defesa · 1 sobreposição" — sem o Nível, que vem na etiqueta ao lado. */
  C.resumo = function (c) {
    const partes = [];
    if (c.nivel) partes.push(EG.Ficha.ROTULO_CONE[c.nivel] + (c.alvo ? " em " + (c.qual || c.alvo) : ""));
    else if (c.alvo) partes.push("em " + (c.qual || c.alvo));
    if (c.nivel && c.alvo && c.escolha === "PV") partes.push("escolhido em PV");
    if (c.sobreposicoes) partes.push("+" + c.sobreposicoes + " sobrepos" + (c.sobreposicoes > 1 ? "ições" : "ição"));
    if (!partes.length) partes.push("sem Bônus Maior escolhido");
    return partes.join(" · ");
  };

  /** O rótulo de um Cone num <select>. */
  C.rotulo = function (c) {
    return (c.nome || "Cone sem nome") + " — " + (c.nivel ? "Nível " + c.nivel + ", " : "sem Nível, ") +
      C.resumo(c) + (c.imagem ? " · com arte" : "");
  };

  /** Um <select> com o banco inteiro. `id` é lido pela ação que equipa. */
  C.seletor = function (id, o) {
    o = o || {};
    const lista = C.todos();
    if (!lista.length) return "";
    return "<select id='" + esc(id) + "' aria-label='" + esc(o.rotulo || "Cone do banco") + "'>" +
      "<option value=''>" + esc(o.vazio || "— escolha um Cone do banco —") + "</option>" +
      lista.map((c) => "<option value='" + esc(c.id) + "'>" + esc(C.rotulo(c)) + "</option>").join("") +
      "</select>";
  };

  /**
   * O cartão de um Cone do banco: a arte pequena, o nome, o resumo, o Efeito Condicional e
   * a história. Os botões vêm de fora, porque a ficha usa `data-acao` e a Área do Mestre
   * usa `data-m` — cada tela entrega os seus.
   */
  C.cartaoHtml = function (c, botoes) {
    const arte = (c.imagem || "").trim()
      ? "<figure class='cone-arte'><img src='" + esc(c.imagem) + "' loading='lazy' decoding='async'" +
        " alt='Arte do Cone de Luz " + esc(c.nome || "sem nome") + "'></figure>"
      : "";
    const descricao = EG.paragrafos(c.descricao);
    return "<article class='cone-guardado'><div class='cone mini'>" + arte + "<div class='cone-corpo'>" +
      "<div class='cone-topo'><b>" + esc(c.nome || "Cone sem nome") + "</b>" +
      (c.nivel ? " <span class='etiqueta'>Nível " + c.nivel + "</span>" : " <span class='etiqueta ruim'>sem Nível</span>") +
      "</div>" +
      "<p class='ajuda'>" + esc(C.resumo(c)) + "</p>" +
      (c.efeito ? "<p class='efeito'>" + esc(c.efeito) + "</p>" : "") +
      (c.nota ? "<p class='ajuda'><i>" + esc(c.nota) + "</i></p>" : "") +
      (descricao ? "<details class='cone-descricao-fechada'" +
        EG.atributosAbre("cone-banco:" + c.id, false) + "><summary>Ler a descrição</summary>" +
        "<div class='cone-descricao'>" + descricao + "</div></details>" : "") +
      "<div class='botoes compactos'>" + (botoes || "") + "</div>" +
      "</div></div></article>";
  };

  /** A coleção inteira em grade, com os botões que a tela pedir por Cone. */
  C.galeriaHtml = function (botoesDe) {
    const lista = C.todos();
    if (!lista.length) return "";
    return "<div class='galeria-cones'>" + lista.map((c) => C.cartaoHtml(c, botoesDe(c))).join("") + "</div>";
  };

  // ---------------------------------------------------------------------------
  // O seletor de arquivo, que serve às duas telas
  //
  // O mesmo `<input type=file>` atende a ficha e a Área do Mestre: ele é criado fora de
  // #app (EG.seletorDeArquivo) e a leitura acontece aqui, não na tela — assim importar um
  // banco funciona igual nos dois lugares, e só o redesenho é que muda de tela.
  // ---------------------------------------------------------------------------
  C.ID_ARQUIVO = "arquivo-cones";
  C.pedirArquivo = function () {
    EG.seletorDeArquivo(C.ID_ARQUIVO, ".json,application/json", true).click();
  };

  document.addEventListener("change", (ev) => {
    const campo = ev.target;
    if (campo.id !== C.ID_ARQUIVO || !campo.files || !campo.files.length) return;
    const arquivos = Array.from(campo.files);
    campo.value = "";
    let novos = 0, atualizados = 0, semNome = 0, achados = 0, ruins = 0, faltam = arquivos.length;
    const fim = () => {
      if (--faltam > 0) return;
      if (!achados) {
        EG.toast("Nenhum Cone nesses arquivos. Vale o banco exportado aqui, um Cone sozinho, " +
          "uma ficha, um NPC, uma mesa ou um backup completo.", "erro");
      } else {
        EG.toast("Banco de Cones atualizado: <b>" + novos +
          (novos === 1 ? " Cone novo" : " Cones novos") + "</b>" +
          (atualizados ? ", " + atualizados + " atualizado" + (atualizados > 1 ? "s" : "") + " (mesmo nome)" : "") +
          (semNome ? ". " + semNome + " sem nome " + (semNome > 1 ? "ficaram de fora" : "ficou de fora") : "") +
          (ruins ? ". " + ruins + " arquivo" + (ruins > 1 ? "s não deram" : " não deu") + " para ler" : "") + ".");
      }
      EG.redesenharTela();
    };
    for (const arquivo of arquivos) {
      const leitor = new FileReader();
      leitor.onerror = () => { ruins++; fim(); };
      leitor.onload = () => {
        try {
          const r = C.importar(JSON.parse(leitor.result));
          novos += r.novos; atualizados += r.atualizados; semNome += r.semNome; achados += r.achados;
        } catch (_) { ruins++; }
        fim();
      };
      leitor.readAsText(arquivo);
    }
  });
})();
