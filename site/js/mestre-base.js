/*
 * mestre-base.js — Área do Mestre: o estado da campanha, a sincronia com as fichas dos
 * jogadores e as regras que a mesa do Mestre opera (Fila de Ação, Firmeza, Tenacidade,
 * Quebra, orçamento de encontro e recompensas). As telas ficam em mestre.js.
 *
 * Duas decisões importantes:
 *
 * 1. O estado do Mestre tem chave própria no navegador. O mapa de fichas
 *    ("explorando-galaxias:fichas") continua sendo só de fichas: todo o site o lê assim.
 * 2. O que é da ficha fica na ficha. PV, Energia, PH, condições e Memoespírito são
 *    gravados nas fichas dos jogadores, então o que o Mestre faz aqui aparece na aba
 *    Jogar de cada um. Só o estado de combate (participa, já agiu, atraso) é do Mestre.
 */
(function () {
  "use strict";

  const EG = window.EG;
  const { esc } = EG;
  const M = window.Motor;
  const C = () => window.CATALOGO;
  const G = (EG.Mestre = EG.Mestre || {});

  const CHAVE = "explorando-galaxias:mestre";
  const ELEMENTOS = ["Físico", "Fogo", "Gelo", "Raio", "Vento", "Quântico", "Imaginário"];
  const TIPOS = ["Comum", "Elite", "Boss"];

  // ---------------------------------------------------------------------------
  // Modelo e armazenamento
  // ---------------------------------------------------------------------------
  function combateVazio() {
    return { nome: "", ciclo: 1, ativo: false, inimigos: [], cc: {}, alvo: "",
      rt: { quem: "", fonte: "basico", elemento: "" } };
  }

  function modeloVazio() {
    return {
      versao: 1, aviso_lido: false, semeado: false,
      campanha: { nome: "", mestre: "", sessao: 1, nivel: 1, semente: "", notas: "", local: "" },
      grupo: [],                       // ids de ficha, na ordem da mesa
      combate: combateVazio(),
      inimigos_salvos: [], encontros: [], tesouro: [], missoes: [], npcs: [],
      entregas: {},                    // "faixa:3" -> true, o calendário de 27.8
      filtros: { faixa: "", tipo: "", q: "", ancora: "" },
    };
  }

  function completar(e) {
    const base = modeloVazio();
    const juntar = (alvo, padrao) => {
      for (const [k, v] of Object.entries(padrao)) {
        if (!(k in alvo) || alvo[k] === undefined || alvo[k] === null) alvo[k] = EG.clonar(v);
        else if (v && typeof v === "object" && !Array.isArray(v) && typeof alvo[k] === "object") juntar(alvo[k], v);
      }
      return alvo;
    };
    return juntar(e, base);
  }

  let E = null;                        // estado em memória

  G.estado = function () {
    if (E) return E;
    let bruto = null;
    try { bruto = JSON.parse(localStorage.getItem(CHAVE)); } catch (_) { bruto = null; }
    E = completar(bruto && typeof bruto === "object" ? bruto : {});
    // Na primeira abertura, o grupo já vem com as fichas que estão salvas neste navegador.
    if (!E.semeado) {
      E.semeado = true;
      if (!E.grupo.length) E.grupo = G.idsDasFichas();
      const g = G.grupo();
      if (g.length) E.campanha.nivel = Math.max(...g.map((m) => m.p.nivel || 1));
      G.salvar();
    }
    return E;
  };

  G.salvar = function () {
    if (!E) return;
    try { localStorage.setItem(CHAVE, JSON.stringify(E)); } catch (_) {
      EG.toast("Não foi possível salvar a mesa do Mestre neste navegador. Use <b>Exportar</b>.", "erro");
    }
  };

  G.zerar = function () { E = modeloVazio(); E.semeado = true; G.salvar(); };

  // ---------------------------------------------------------------------------
  // O grupo: as fichas salvas neste navegador
  // ---------------------------------------------------------------------------
  G.idsDasFichas = function () {
    return Object.values(EG.Armazem.todas())
      .sort((a, b) => (a.nome || "").localeCompare(b.nome || ""))
      .map((p) => p.id);
  };

  /** Um membro do grupo: {id, p (ficha completa), R (resultado do motor)}. */
  G.membro = function (id) {
    const bruta = EG.Armazem.todas()[id];
    if (!bruta) return null;
    const p = EG.Ficha.completar(bruta);
    const R = M.calcular(EG.Ficha.paraMotor(p), C());
    if (p.jogo.ph == null) p.jogo.ph = R.ph_inicio;
    return { id: id, p: p, R: R };
  };

  G.grupo = function () {
    return (G.estado().grupo || []).map(G.membro).filter(Boolean);
  };

  G.foraDoGrupo = function () {
    const dentro = new Set(G.estado().grupo || []);
    return G.idsDasFichas().filter((id) => !dentro.has(id)).map(G.membro).filter(Boolean);
  };

  /** Grava o que mudou na ficha do jogador: é isso que sincroniza com a aba Jogar. */
  G.gravarFicha = function (m) { EG.Armazem.salvar(m.p); };

  G.nome = (m) => m.p.nome || "Personagem sem nome";

  G.nivelGrupo = function (g) {
    g = g || G.grupo();
    return g.length ? Math.max(...g.map((m) => m.p.nivel || 1)) : null;
  };

  G.nivel = function () {
    const n = G.estado().campanha.nivel;
    return Math.max(1, Math.min(20, Number(n) || 1));
  };

  G.faixaN = (nivel) => M.faixa(nivel == null ? G.nivel() : nivel);
  G.faixaTexto = (n) => (C().mestre.ancoras[(n || G.faixaN()) - 1] || {}).faixa || "—";

  // ---------------------------------------------------------------------------
  // PV, Energia e condições dos personagens (espelha ficha-jogar.js)
  // ---------------------------------------------------------------------------
  G.pvAtual = (m) => (m.p.jogo.pv == null ? m.R.pv_max : Math.min(m.p.jogo.pv, m.R.pv_max));

  /** 23.1/23.3: tira a RD (mínimo 1), depois o PV temporário. Contínuo ignora a RD. */
  G.aplicarDano = function (m, bruto, continuo) {
    const j = m.p.jogo, antes = G.pvAtual(m);
    if (!(bruto > 0)) return null;
    if (antes === 0) {
      j.morrendo.f += 1;
      G.gravarFicha(m);
      return { msg: esc(G.nome(m)) + " levou dano enquanto Morrendo: <b>+1 falha</b>." };
    }
    const depoisRd = Math.max(1, bruto - (continuo ? 0 : m.R.rd));
    const absorvido = Math.min(j.temp || 0, depoisRd);
    j.temp = (j.temp || 0) - absorvido;
    j.pv = Math.max(0, antes - (depoisRd - absorvido));
    if (j.pv === 0) j.morrendo = { s: 0, f: 0 };
    G.gravarFicha(m);
    return { msg: esc(G.nome(m)) + ": dano " + bruto + (continuo ? " (Contínuo, ignora RD)" : m.R.rd ? " − RD " + m.R.rd : "") +
      " = <b>" + depoisRd + "</b>" + (absorvido ? " · " + absorvido + " no temporário" : "") +
      " · PV " + j.pv + "/" + m.R.pv_max + (j.pv === 0 ? " · <b>Morrendo!</b>" : "") };
  };

  G.curar = function (m, v) {
    const j = m.p.jogo, antes = G.pvAtual(m);
    if (!(v > 0)) return null;
    j.pv = Math.min(m.R.pv_max, antes + v);
    if (antes === 0) j.morrendo = { s: 0, f: 0 };
    G.gravarFicha(m);
    return { msg: esc(G.nome(m)) + ": curou " + (j.pv - antes) + " · PV " + j.pv + "/" + m.R.pv_max +
      (antes === 0 ? " · saiu de Morrendo" : "") };
  };

  G.energia = function (m, delta) {
    const j = m.p.jogo;
    j.energia = Math.max(0, Math.min(100, (j.energia || 0) + delta));
    G.gravarFicha(m);
  };

  /** 23.6: Descanso Curto (+2×nível+Vigor) e Longo (tudo de volta) para o grupo inteiro. */
  G.descanso = function (tipo) {
    const g = G.grupo();
    for (const m of g) {
      const j = m.p.jogo, antes = G.pvAtual(m);
      if (tipo === "longo") {
        j.pv = m.R.pv_max; j.temp = 0; j.condicoes = []; j.morrendo = { s: 0, f: 0 };
        j.esforco = m.R.esforco_max;
        j.usos = {};
      } else {
        j.pv = Math.min(m.R.pv_max, antes + Math.max(0, m.R.descanso_curto));
        if (antes === 0 && j.pv > 0) j.morrendo = { s: 0, f: 0 };
      }
      if (m.R.memo) { j.memo_pv = m.R.memo.pv; if (tipo === "longo") j.memo_ativo = false; }
      G.gravarFicha(m);
    }
    return g.length;
  };

  // --- PH do grupo: um recurso só, guardado em todas as fichas (16.2) ---------
  G.recursoPH = function (g) {
    g = g || G.grupo();
    if (!g.length) return null;
    const ref = g[0];
    const valores = g.map((m) => (m.p.jogo.ph == null ? ref.R.ph_inicio : m.p.jogo.ph));
    return {
      atual: Math.min(...valores), max: ref.R.ph_max, inicio: ref.R.ph_inicio,
      geracao: ref.R.ph_geracao,
      divergente: g.some((m) => m.R.ph_max !== ref.R.ph_max) || new Set(valores).size > 1,
    };
  };

  G.definirPH = function (valor) {
    const g = G.grupo(), r = G.recursoPH(g);
    if (!r) return null;
    const novo = Math.max(0, Math.min(r.max, Math.round(valor) || 0));
    for (const m of g) { m.p.jogo.ph = novo; G.gravarFicha(m); }
    return novo;
  };

  /** 16.2: o tamanho do grupo muda a tabela de PH, então vai para todas as fichas. */
  G.definirTamanho = function (n) {
    n = Math.max(1, Math.min(6, Math.round(n) || 4));
    for (const m of G.grupo()) { m.p.jogadores = n; G.gravarFicha(m); }
    return n;
  };

  G.tamanhoGrupo = function (g) {
    g = g || G.grupo();
    return g.length ? g[0].p.jogadores || 4 : G.estado().grupo.length || 4;
  };

  // --- Condições com turnos (21.5) -------------------------------------------
  G.infoCondicao = (nome) => C().condicoes.find((x) => x.condicao === nome) || {};

  G.porCondicao = function (lista, nome, turnos, origem) {
    lista = lista || [];
    const atual = lista.find((c) => c.nome === nome);
    if (atual) {
      atual.turnos = turnos == null ? atual.turnos : turnos;
      atual.acumulos = (atual.acumulos || 1) + 1;
    } else {
      lista.push({ nome: nome, turnos: turnos == null ? null : turnos, acumulos: 1, origem: origem || "" });
    }
    return lista;
  };

  /** Desconta 1 turno de cada condição com contador. Devolve as que expiraram. */
  G.descontarTurnos = function (lista) {
    const expiradas = [];
    for (let i = (lista || []).length - 1; i >= 0; i--) {
      const c = lista[i];
      if (c.turnos == null) continue;
      c.turnos -= 1;
      if (c.turnos <= 0) { expiradas.push(c.nome); lista.splice(i, 1); }
    }
    return expiradas;
  };

  // ---------------------------------------------------------------------------
  // Inimigos
  // ---------------------------------------------------------------------------
  G.ancora = (faixaN) => C().mestre.ancoras[(faixaN || G.faixaN()) - 1];
  G.orcamento = (faixaN) => C().mestre.orcamento[(faixaN || G.faixaN()) - 1];

  function baseCombate(x) {
    x.uid = EG.uid();
    x.pv_max = x.pv;
    x.reducao = 0;
    x.fase = 1;
    x.quebrado = false;
    x.condicoes = [];
    return x;
  }

  /** Inimigo em branco, com os 13 números da linha da âncora (28.3). */
  G.inimigoDaAncora = function (faixaN, tipo, nome) {
    const a = G.ancora(faixaN);
    const d = (a.dano || {})[tipo] || {};
    return baseCombate({
      nome: nome || "", tipo: tipo, faccao: "", frase: "", faixa: a.faixa, faixa_n: a.n,
      pv: a.pv[tipo], defesa: a.defesa[tipo], rd: a.rd[tipo], tenacidade: a.tenacidade[tipo],
      vel: a.vel[tipo], ataque: a.ataque, dano: d.texto || "", dano_media: a.dano_media[tipo],
      dt: a.dt[tipo], tr: a.tr[tipo], fraquezas: [], resistencias: [],
      ataques: [], especiais: [], fila: "", firmeza: tipo === "Comum" ? "Não" : "Sim", fases: 1,
      origem: "âncora " + a.faixa,
    });
  };

  G.doBestiario = (nome) => C().bestiario.find((x) => x.nome === nome);

  /** Cópia de uma ficha do bestiário, pronta para entrar no combate. */
  G.inimigoDoBestiario = function (nome) {
    const b = G.doBestiario(nome);
    if (!b) return null;
    const x = EG.clonar(b);
    x.dano = (x.ataques[0] || {}).dados || "";
    x.dano_media = (x.ataques[0] || {}).media || null;
    x.faixa_n = b.faixa_n;
    x.origem = "bestiário 28";
    return baseCombate(x);
  };

  G.inimigoSalvo = function (uid) {
    const x = G.estado().inimigos_salvos.find((i) => i.uid === uid);
    return x ? baseCombate(EG.clonar(x)) : null;
  };

  /** Todas as fichas que podem entrar num encontro: bestiário + inimigos da campanha. */
  G.catalogoDeInimigos = function () {
    const meus = G.estado().inimigos_salvos.map((x) => ({ ref: "salvo:" + x.uid, nome: x.nome, tipo: x.tipo,
      faixa: x.faixa, faixa_n: x.faixa_n, pv: x.pv_max != null ? x.pv_max : x.pv, faccao: x.faccao || "da campanha" }));
    const livro = C().bestiario.map((x) => ({ ref: "livro:" + x.nome, nome: x.nome, tipo: x.tipo,
      faixa: x.faixa, faixa_n: x.faixa_n, pv: x.pv, faccao: x.faccao }));
    return meus.concat(livro);
  };

  G.inimigoDaRef = function (ref) {
    if (!ref) return null;
    const [tipo, resto] = [ref.slice(0, ref.indexOf(":")), ref.slice(ref.indexOf(":") + 1)];
    return tipo === "salvo" ? G.inimigoSalvo(resto) : G.inimigoDoBestiario(resto);
  };

  G.pvDeRef = function (ref) {
    const t = G.catalogoDeInimigos().find((x) => x.ref === ref);
    return t ? t.pv || 0 : 0;
  };

  // ---------------------------------------------------------------------------
  // Regras da mesa
  // ---------------------------------------------------------------------------
  /** 19.4: Atraso com Firmeza. Soma bruta do Ciclo ÷ 2 (mínimo 1), com teto por tipo. */
  G.casasAtraso = function (bruto, tipo) {
    bruto = Math.max(0, Math.round(bruto) || 0);
    if (!bruto) return 0;
    const t = C().mestre.atraso_tipo.find((x) => x.tipo === tipo) ||
      { teto: 3, firmeza: "Não" };                 // PJ e Memoespírito: sem Firmeza, como Comum
    if (t.firmeza === "Sim") return Math.min(t.teto, Math.max(1, Math.floor(bruto / 2)));
    return Math.min(t.teto, bruto);
  };

  G.temFirmeza = function (tipo) {
    const t = C().mestre.atraso_tipo.find((x) => x.tipo === tipo);
    return !!(t && t.firmeza === "Sim");
  };

  /** 20.3 — redução base da fonte. Habilidade reduz o próprio Nível (1-2 reduzem 2). */
  G.FONTES_RT = [
    { id: "basico", rotulo: "Ataque Básico", base: 1 },
    { id: "hab2", rotulo: "Habilidade de Nível 1-2", base: 2 },
    { id: "hab3", rotulo: "Habilidade de Nível 3", base: 3 },
    { id: "hab4", rotulo: "Habilidade de Nível 4", base: 4 },
    { id: "hab5", rotulo: "Habilidade de Nível 5", base: 5 },
    { id: "hab6", rotulo: "Habilidade de Nível 6", base: 6 },
    { id: "hab7", rotulo: "Habilidade de Nível 7", base: 7 },
    { id: "ult", rotulo: "Ultimate", base: 5 },
    { id: "continuo", rotulo: "Dano Contínuo", base: 0 },
  ];

  /** 20.2: Fraqueza reduz o total; neutro, a metade (mínimo 1); Resistência, 1 fixo. */
  G.reducaoTenacidade = function (base, relacao) {
    base = Math.max(0, Math.round(base) || 0);
    if (!base) return 0;
    if (relacao === "Resistência") return 1;
    if (relacao === "Fraqueza") return base;
    return Math.max(1, Math.floor(base / 2));
  };

  G.relacaoElemento = function (inimigo, elemento) {
    if (!elemento) return "Neutro";
    if ((inimigo.fraquezas || []).includes(elemento)) return "Fraqueza";
    if ((inimigo.resistencias || []).includes(elemento)) return "Resistência";
    return "Neutro";
  };

  /** 20.5: dano e efeito de Quebra do Elemento, com a Eficiência de quem quebrou. */
  G.quebraDe = function (elemento, eficiencia) {
    const el = C().elementos.find((x) => x.elemento === elemento);
    if (!el) return null;
    const fixo = (el.quebra_mult_ef || 1) * (eficiencia || 2);
    return {
      elemento: elemento, texto: M.textoDano(el.quebra_n, el.quebra_f, fixo),
      media: M.media(el.quebra_n, el.quebra_f) + fixo,
      efeito: el.efeito_quebra, formula: el.dano_quebra,
    };
  };

  /** Dano no inimigo: tira a RD de cada instância (18.4) e devolve o que entrou. */
  G.danoNoInimigo = function (x, bruto, o) {
    o = o || {};
    if (!(bruto > 0)) return null;
    const rd = o.continuo ? 0 : (x.rd || 0);
    const entrou = Math.max(0, bruto - rd);
    x.pv = Math.max(0, (x.pv == null ? x.pv_max : x.pv) - entrou);
    return { entrou: entrou, rd: rd, caiu: x.pv === 0 };
  };

  /** Tenacidade a 0 é Quebra (20.4): dano de Quebra, condição, 1 casa de Atraso e +10 Energia. */
  G.quebrar = function (x, elemento, eficiencia) {
    const q = G.quebraDe(elemento, eficiencia);
    x.quebrado = true;
    x.reducao = x.tenacidade;
    if (q && q.efeito) G.porCondicao(x.condicoes, q.efeito, 2, "Quebra de " + elemento);
    G.porCondicao(x.condicoes, "Quebrado", 1, "Quebra");
    return q;
  };

  /** Fim do turno do alvo Quebrado: a barra volta cheia e a condição sai (20.4, passo 5). */
  G.restaurarTenacidade = function (x) {
    x.quebrado = false;
    x.reducao = 0;
    // Tira em no lugar: a mesma lista é usada pelo desconto de turnos logo depois.
    x.condicoes = x.condicoes || [];
    for (let i = x.condicoes.length - 1; i >= 0; i--) {
      if (x.condicoes[i].nome === "Quebrado") x.condicoes.splice(i, 1);
    }
  };

  G.tenacidadeAtual = (x) => Math.max(0, (x.tenacidade || 0) - (x.reducao || 0));

  // ---------------------------------------------------------------------------
  // Fila de Ação (19.3)
  // ---------------------------------------------------------------------------
  G.cc = function (chave) {
    const cc = G.estado().combate.cc;
    if (!cc[chave]) cc[chave] = { participa: true, agiu: false, atraso: 0, pendente: 0, avanco: 0,
      avanco_total: false, surpreso: false, ultimate: false };
    return cc[chave];
  };

  /**
   * Monta a Fila do Ciclo: PJs, Memoespíritos em campo e inimigos numa lista só,
   * por VEL decrescente, com os desempates de 19.3 (Agilidade, Discernimento,
   * jogadores antes dos NPCs) e os Atrasos pendentes do Ciclo anterior.
   */
  G.fila = function () {
    const cb = G.estado().combate;
    const itens = [];
    for (const m of G.grupo()) {
      const chave = "p:" + m.id, cc = G.cc(chave);
      itens.push({
        chave: chave, kind: "pj", tipo: "PJ", nome: G.nome(m), sub: [m.p.caminho, m.p.elemento].filter(Boolean).join(" · "),
        vel: m.R.velocidade || 10, agi: (m.R.bonus || {}).Agilidade || 0,
        dis: (m.R.bonus || {}).Discernimento || 0, jogador: true, cc: cc, m: m,
        pv: G.pvAtual(m), pv_max: m.R.pv_max, condicoes: m.p.jogo.condicoes || [],
      });
      if (m.R.memo && m.p.jogo.memo_ativo) {
        const ck = "m:" + m.id, cm = G.cc(ck);
        itens.push({
          chave: ck, kind: "memo", tipo: "Memoespírito",
          nome: m.p.memoespirito.nome || "Memoespírito", sub: "de " + G.nome(m),
          vel: m.R.memo.velocidade, agi: (m.R.memo.tr.Agilidade || 0) - m.R.eficiencia,
          dis: (m.R.memo.tr.Discernimento || 0) - m.R.eficiencia, jogador: true, cc: cm, m: m,
          pv: m.p.jogo.memo_pv == null ? m.R.memo.pv : Math.min(m.p.jogo.memo_pv, m.R.memo.pv),
          pv_max: m.R.memo.pv, condicoes: [],
        });
      }
    }
    for (const x of cb.inimigos) {
      const chave = "i:" + x.uid, cc = G.cc(chave);
      itens.push({
        chave: chave, kind: "inimigo", tipo: x.tipo, nome: x.nome || "Inimigo sem nome",
        sub: [x.faccao, "faixa " + x.faixa].filter(Boolean).join(" · "),
        vel: x.vel || 10, agi: 0, dis: 0, jogador: false, cc: cc, x: x,
        pv: x.pv == null ? x.pv_max : x.pv, pv_max: x.pv_max, condicoes: x.condicoes || [],
      });
    }
    const dentro = itens.filter((i) => i.cc.participa !== false);
    dentro.sort((a, b) => b.vel - a.vel || b.agi - a.agi || b.dis - a.dis ||
      (b.jogador ? 1 : 0) - (a.jogador ? 1 : 0) || a.nome.localeCompare(b.nome));
    dentro.forEach((i, n) => { i.base = n; });
    for (const i of dentro) {
      const tipoAtraso = i.kind === "inimigo" ? i.tipo : "Comum";
      i.atraso_casas = G.casasAtraso((i.cc.atraso || 0) + (i.cc.pendente || 0), tipoAtraso);
      i.atraso_bruto = (i.cc.atraso || 0) + (i.cc.pendente || 0);
      i.avanco_casas = i.cc.agiu ? 0 : Math.max(0, Math.round(i.cc.avanco) || 0);
      i.pos = i.base + i.atraso_casas - i.avanco_casas;
    }
    dentro.sort((a, b) => a.pos - b.pos || a.base - b.base);
    // Avanço Total: age logo depois de quem está agindo agora (19.5)
    const total = dentro.filter((i) => i.cc.avanco_total);
    if (total.length) {
      const resto = dentro.filter((i) => !i.cc.avanco_total);
      const i0 = resto.findIndex((i) => !i.cc.agiu);
      resto.splice(i0 < 0 ? resto.length : i0 + 1, 0, ...total);
      dentro.length = 0;
      dentro.push(...resto);
    }
    dentro.forEach((i, n) => { i.casa = n + 1; });
    const agora = dentro.find((i) => !i.cc.agiu && !i.cc.surpreso);
    if (agora) agora.agora = true;
    return { casas: dentro, fora: itens.filter((i) => i.cc.participa === false), agora: agora || null };
  };

  /**
   * Fim do turno de um combatente: desconta 1 turno das condições dele e, se estava
   * Quebrado, devolve a Tenacidade cheia e tira a condição (20.4, passo 5).
   * As condições se contam em *turnos do alvo* (19.2), então o gancho é aqui e não no Ciclo.
   */
  G.fimDeTurno = function (lista, inimigo) {
    const saiu = [];
    if (inimigo && inimigo.quebrado) { G.restaurarTenacidade(inimigo); saiu.push("Quebrado"); }
    saiu.push(...G.descontarTurnos(lista));
    return saiu.filter((n, i) => saiu.indexOf(n) === i);
  };

  /** Desfaz o fim de turno: devolve 1 turno às condições com contador. */
  G.desfazerFimDeTurno = function (lista) {
    for (const c of lista || []) if (c.turnos != null) c.turnos += 1;
  };

  /** Avançar o Ciclo: soma 1, carrega o atraso excedente e limpa as marcas do Ciclo (19.3). */
  G.avancarCiclo = function () {
    const cb = G.estado().combate;
    cb.ciclo = (cb.ciclo || 1) + 1;
    for (const [chave, cc] of Object.entries(cb.cc)) {
      const tipoAtraso = chave.startsWith("i:")
        ? ((cb.inimigos.find((x) => "i:" + x.uid === chave) || {}).tipo || "Comum") : "Comum";
      const bruto = (cc.atraso || 0) + (cc.pendente || 0);
      const aplicado = G.casasAtraso(bruto, tipoAtraso);
      cc.pendente = Math.max(0, bruto - aplicado);
      cc.atraso = 0; cc.avanco = 0; cc.avanco_total = false;
      cc.agiu = false; cc.descontou = false;
      cc.ultimate = false; cc.surpreso = false;          // Surpresa só pula o 1º Ciclo (19.3)
    }
    G.salvar();
    return { ciclo: cb.ciclo };
  };

  G.novoCombate = function (nome) {
    const est = G.estado();
    est.combate = combateVazio();
    est.combate.nome = nome || "";
    est.combate.ativo = true;
    const g = G.grupo();
    for (const m of g) { m.p.jogo.ph = m.R.ph_inicio; m.p.jogo.acumulos = {}; G.gravarFicha(m); }
    G.salvar();
    return g.length;
  };

  // ---------------------------------------------------------------------------
  // Encontros (27.4 e 27.5)
  // ---------------------------------------------------------------------------
  /** Custo do encontro em PV contra o orçamento da faixa, e a leitura de 27.4. */
  G.contaDoEncontro = function (itens, faixaN) {
    const orc = G.orcamento(faixaN);
    let custo = 0, acoes = 0, n = 0;
    const porTipo = { Comum: 0, Elite: 0, Boss: 0 };
    for (const it of itens || []) {
      const qtd = Math.max(1, Number(it.qtd) || 1);
      const ref = G.catalogoDeInimigos().find((x) => x.ref === it.ref);
      if (!ref) continue;
      custo += (ref.pv || 0) * qtd;
      porTipo[ref.tipo] = (porTipo[ref.tipo] || 0) + qtd;
      acoes += ({ Comum: 1, Elite: 1.5, Boss: 2 }[ref.tipo] || 1) * qtd;
      n += qtd;
    }
    const pct = orc && orc.orcamento ? Math.round(100 * custo / orc.orcamento) : 0;
    const leitura = !n ? "vazio" : pct <= 60 ? "cena de passagem (2 Ciclos)"
      : pct <= 110 ? "encontro típico (3 a 5 Ciclos)" : "mais pesado que o orçamento da faixa";
    return { orcamento: orc ? orc.orcamento : 0, custo: custo, pct: pct, leitura: leitura,
      acoes: acoes, n: n, por_tipo: porTipo };
  };

  G.elementosDoGrupo = function (g) {
    g = g || G.grupo();
    const el = [];
    for (const m of g) if (m.p.elemento && !el.includes(m.p.elemento)) el.push(m.p.elemento);
    return el;
  };

  /** 27.5: pelo menos 3 Elementos do grupo têm de aparecer como Fraqueza na cena. */
  G.contratoDaFraqueza = function (itens, g) {
    const doGrupo = G.elementosDoGrupo(g);
    const naCena = new Set();
    const resistidos = new Set();
    for (const it of itens || []) {
      const x = G.inimigoDaRef(it.ref);
      if (!x) continue;
      for (const f of x.fraquezas || []) naCena.add(f);
      for (const r of x.resistencias || []) resistidos.add(r);
    }
    const cobertos = doGrupo.filter((e) => naCena.has(e));
    const dobrados = doGrupo.filter((e) => g && g.filter((m) => m.p.elemento === e).length > 1);
    return {
      do_grupo: doGrupo, cobertos: cobertos, faltam: doGrupo.filter((e) => !naCena.has(e)),
      cumprido: cobertos.length >= Math.min(3, doGrupo.length),
      alvo: Math.min(3, doGrupo.length),
      resistencia_perigosa: dobrados.filter((e) => resistidos.has(e)),
    };
  };

  // ---------------------------------------------------------------------------
  // Campos ligados ao estado do Mestre (data-mg) e às fichas (data-mf)
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
  const idDe = (s) => "m-" + String(s).replace(/[^A-Za-z0-9]/g, (c) => "_" + c.charCodeAt(0).toString(16));

  const H = (G.H = {});

  H.campo = (rotulo, controle, ajuda, classe) =>
    "<div class='campo " + (classe || "") + "'><span class='rotulo'>" + rotulo + "</span>" + controle +
    (ajuda ? "<span class='ajuda'>" + ajuda + "</span>" : "") + "</div>";

  const atributos = (alvo, caminho, extra) =>
    " id='" + idDe(alvo + "|" + caminho) + "' data-" + (alvo === "g" ? "mg" : "mf") + "='" + esc(caminho) + "'" +
    (alvo !== "g" ? " data-mid='" + esc(alvo) + "'" : "") + (extra || "");

  function valorEm(alvo, caminho) {
    if (alvo === "g") return obter(G.estado(), caminho);
    const m = G.membro(alvo);
    return m ? obter(m.p, caminho) : undefined;
  }

  H.texto = (alvo, caminho, o) => {
    o = o || {};
    const v = valorEm(alvo, caminho);
    const a = atributos(alvo, caminho, " aria-label='" + esc(o.rotulo || caminho) + "'" +
      (o.ph ? " placeholder='" + esc(o.ph) + "'" : "") + (o.classe ? " class='" + o.classe + "'" : "") +
      (o.vivo ? " data-vivo='1'" : ""));          // vivo: redesenha a cada tecla (campo de filtro)
    return o.area ? "<textarea rows='" + (o.linhas || 3) + "'" + a + ">" + esc(v == null ? "" : v) + "</textarea>"
      : "<input type='" + (o.busca ? "search" : "text") + "'" + a + " value='" + esc(v == null ? "" : v) + "'>";
  };

  H.numero = (alvo, caminho, o) => {
    o = o || {};
    const v = valorEm(alvo, caminho);
    return "<input type='number' inputmode='numeric' data-t='num'" +
      atributos(alvo, caminho, (o.min != null ? " min='" + o.min + "'" : "") +
        (o.max != null ? " max='" + o.max + "'" : "") +
        " aria-label='" + esc(o.rotulo || caminho) + "' class='" + (o.classe || "curto") + "'" +
        (o.ph ? " placeholder='" + esc(o.ph) + "'" : "")) +
      " value='" + (v == null ? "" : esc(v)) + "'>";
  };

  H.lista = (alvo, caminho, opcoes, o) => {
    o = o || {};
    const v = valorEm(alvo, caminho);
    const atual = v == null ? "" : String(v);
    let html = "<select" + atributos(alvo, caminho, (o.num ? " data-t='num'" : "") +
      " aria-label='" + esc(o.rotulo || caminho) + "'") + ">";
    if (o.vazio !== false) html += "<option value=''>" + esc(o.vazio || "— escolha —") + "</option>";
    for (const op of opcoes) {
      const [valor, rotulo] = Array.isArray(op) ? op : [op, op];
      html += "<option value='" + esc(valor) + "'" + (String(valor) === atual ? " selected" : "") + ">" +
        esc(rotulo) + "</option>";
    }
    return html + "</select>";
  };

  H.marca = (alvo, caminho, rotulo) => {
    const v = !!valorEm(alvo, caminho);
    return "<label class='marca'><input type='checkbox' data-t='bool'" + atributos(alvo, caminho, "") +
      (v ? " checked" : "") + "> <span>" + rotulo + "</span></label>";
  };

  H.cartao = (titulo, corpo, classe, extra) =>
    "<section class='cartao " + (classe || "") + "'><header class='cartao-topo'><h2>" + titulo + "</h2>" +
    (extra || "") + "</header>" + corpo + "</section>";

  H.num = (rotulo, valor, sub) => "<div class='numero'><span class='rotulo'>" + rotulo + "</span>" +
    "<span class='grande'>" + valor + "</span>" + (sub ? "<span class='sub'>" + sub + "</span>" : "") + "</div>";

  H.botao = (acao, texto, o) => {
    o = o || {};
    return "<button type='button' class='botao" + (o.classe ? " " + o.classe : "") + "' data-m='" + esc(acao) + "'" +
      Object.entries(o.dados || {}).map(([k, v]) => " data-" + k + "='" + esc(v) + "'").join("") +
      (o.desabilitado ? " disabled" : "") + (o.titulo ? " title='" + esc(o.titulo) + "'" : "") + ">" + texto + "</button>";
  };

  H.barraPV = (atual, max, rotulo) => {
    const pct = Math.round(100 * atual / Math.max(1, max));
    return "<div class='barra-pv' role='progressbar' aria-label='" + esc(rotulo || "Pontos de Vida") +
      "' aria-valuemin='0' aria-valuemax='" + max + "' aria-valuenow='" + atual + "'>" +
      "<span style='width:" + Math.min(100, pct) + "%' class='" + (pct <= 33 ? "baixo" : pct <= 50 ? "medio" : "") +
      "'></span></div>";
  };

  H.barraTenacidade = (atual, max) => {
    const pct = max ? Math.round(100 * atual / max) : 0;
    return "<div class='barra-tenacidade' role='progressbar' aria-label='Tenacidade' aria-valuemin='0' aria-valuemax='" +
      max + "' aria-valuenow='" + atual + "'><span style='width:" + pct + "%'" +
      (atual === 0 ? " class='zerada'" : "") + "></span></div>";
  };

  H.tabela = (cabecalho, linhas, classe) =>
    "<div class='tabela'><table class='tabela-mestre " + (classe || "") + "'><thead><tr>" +
    cabecalho.map((c) => "<th>" + c + "</th>").join("") + "</tr></thead><tbody>" +
    linhas.map((l) => "<tr>" + l.map((c) => "<td>" + c + "</td>").join("") + "</tr>").join("") +
    "</tbody></table></div>";

  // ---------------------------------------------------------------------------
  // Pedaços comuns às telas
  // ---------------------------------------------------------------------------
  const TELAS = [
    ["painel", "Painel"],
    ["grupo", "Grupo"],
    ["combate", "Combate"],
    ["inimigos", "Inimigos"],
    ["encontros", "Encontros"],
    ["recompensas", "Recompensas"],
    ["consulta", "Escudo do Mestre"],
  ];

  G.app = () => document.getElementById("app");
  G.vazio = (texto) => "<p class='ajuda'>" + texto + "</p>";
  G.fichasTexto = (n) => (n === 1 ? "na ficha" : "nas " + n + " fichas");
  G.ROMANOS = ["I", "II", "III", "IV"];

  /** Barra da campanha e as sub-abas, no topo de toda tela da Área do Mestre. */
  G.topo = function (atual) {
    const est = G.estado(), cb = est.combate;
    const abas = TELAS.map(([id, rotulo]) =>
      "<a href='#mestre" + (id === "painel" ? "" : "/" + id) + "' class='sub-aba" + (id === atual ? " ativa" : "") +
      "'>" + esc(rotulo) + (id === "combate" && cb.ativo ? " <span class='etiqueta pronta'>Ciclo " + cb.ciclo + "</span>" : "") +
      "</a>").join("");
    return "<div class='barra-mestre'>" +
      "<div><strong>" + esc(est.campanha.nome || "Campanha sem nome") + "</strong> " +
      "<span class='suave'>sessão " + esc(est.campanha.sessao || 1) + " · nível " + G.nivel() +
      " · faixa " + esc(G.faixaTexto()) + "</span></div>" +
      "<details class='menu'><summary class='botao'>Mais</summary><div class='menu-itens'>" +
      "<button type='button' data-m='exportar-tudo'>Exportar tudo (fichas + mesa)</button>" +
      "<button type='button' data-m='importar-tudo'>Restaurar um backup</button>" +
      "<hr>" +
      "<button type='button' data-m='exportar-mesa'>Exportar só a mesa</button>" +
      "<button type='button' data-m='importar-mesa'>Importar mesa</button>" +
      "<hr>" +
      "<button type='button' data-m='imprimir'>Imprimir esta tela</button>" +
      "<button type='button' class='perigo' data-m='zerar-mesa'>Apagar a mesa deste navegador</button>" +
      "</div></details>" +
      "<input type='file' id='arquivo-mesa' accept='.json,application/json' hidden>" +
      "<input type='file' id='arquivo-ficha-mestre' accept='.json,application/json' hidden>" +
      "<input type='file' id='arquivo-backup' accept='.json,application/json' hidden>" +
      "</div>" +
      "<nav class='sub-abas' aria-label='Área do Mestre'>" + abas + "</nav>";
  };

  /** A linha da tabela de âncoras (28.3) de uma faixa, por tipo de inimigo. */
  G.linhaDaAncora = function (faixaN) {
    const a = G.ancora(faixaN);
    const linhas = [
      ["PV", ...TIPOS.map((t) => "<b>" + a.pv[t] + "</b>")],
      ["Defesa", ...TIPOS.map((t) => String(a.defesa[t]))],
      ["RD", ...TIPOS.map((t) => String(a.rd[t]))],
      ["Tenacidade", ...TIPOS.map((t) => String(a.tenacidade[t]))],
      ["Velocidade", ...TIPOS.map((t) => String(a.vel[t]))],
      ["Teste de Ataque", ...TIPOS.map(() => EG.sinal(a.ataque))],
      ["Dano por acerto", ...TIPOS.map((t) => EG.botaoRolar((a.dano[t] || {}).texto, "Dano " + t + " da faixa " + a.faixa) +
        " <small>média " + a.dano_media[t] + "</small>")],
      ["DT dos efeitos", ...TIPOS.map((t) => String(a.dt[t]))],
      ["Teste de Resistência", ...TIPOS.map((t) => EG.sinal(a.tr[t]))],
      ["Fraquezas", ...TIPOS.map((t) => a.fraquezas[t])],
      ["Firmeza", ...TIPOS.map((t) => (G.temFirmeza(t) ? "tem" : "não tem"))],
      ["Ações agressivas por Ciclo", ...TIPOS.map((t) =>
        esc((C().mestre.acoes_tipo.find((y) => y.tipo === t) || {}).por_ciclo || ""))],
    ];
    return H.tabela(["Campo", "Comum", "Elite", "Boss"], linhas, "ancora");
  };

  // ---------------------------------------------------------------------------
  // Eventos dos campos ligados
  // ---------------------------------------------------------------------------
  function valorDo(el) {
    if (el.dataset.t === "bool") return el.checked;
    if (el.dataset.t === "num") {
      if (el.value === "") return null;
      const n = Number(el.value);
      return Number.isFinite(n) ? Math.round(n) : null;
    }
    return el.value;
  }

  function escrever(el) {
    const valor = valorDo(el);
    if (el.dataset.mg) {
      definir(G.estado(), el.dataset.mg, valor);
      G.salvar();
      return true;
    }
    if (el.dataset.mf && el.dataset.mid) {
      const m = G.membro(el.dataset.mid);
      if (!m) return false;
      definir(m.p, el.dataset.mf, valor);
      if (el.dataset.mf === "jogadores") return G.definirTamanho(valor), true;
      G.gravarFicha(m);
      return true;
    }
    return false;
  }

  let pendente = false;
  G.redesenhar = function () {
    if (pendente) return;
    pendente = true;
    requestAnimationFrame(() => {
      pendente = false;
      const foco = document.activeElement && document.activeElement.id;
      const y = window.scrollY;
      EG.navegar();
      window.scrollTo(0, y);
      if (foco) { const el = document.getElementById(foco); if (el) el.focus({ preventScroll: true }); }
    });
  };

  document.addEventListener("input", (ev) => {
    const el = ev.target;
    if (!el.dataset || (!el.dataset.mg && !el.dataset.mf)) return;
    if (el.tagName === "SELECT" || el.type === "checkbox" || el.dataset.t === "num") return;
    if (escrever(el) && el.dataset.vivo === "1") G.redesenhar();
  });

  document.addEventListener("change", (ev) => {
    const el = ev.target;
    if (!el.dataset || (!el.dataset.mg && !el.dataset.mf)) return;
    if (!escrever(el)) return;
    if (el.tagName === "SELECT" || el.type === "checkbox" || el.dataset.t === "num") G.redesenhar();
  });

  // ---------------------------------------------------------------------------
  // Ações (data-m), com namespace próprio para não encostar no delegado da ficha
  // ---------------------------------------------------------------------------
  G.acoes = {};

  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-m]");
    if (!b) return;
    const acao = b.dataset.m;
    if (!G.acoes[acao]) return;
    ev.preventDefault();
    const menu = b.closest("details.menu");
    if (menu) menu.open = false;
    if (G.acoes[acao](b) !== false) { G.salvar(); G.redesenhar(); }
  });

  // ---------------------------------------------------------------------------
  // Aviso de abertura — um clique dispensa para sempre
  // ---------------------------------------------------------------------------
  function telaAviso() {
    G.app().innerHTML =
      "<section class='cartao aviso-mestre'>" +
      "<h1>Área do Mestre</h1>" +
      "<p class='aviso-spoiler'>Esta página tem spoiler.</p>" +
      "<p>Aqui ficam o bestiário inteiro, as contas de encontro e as recompensas: é o que o grupo " +
      "ainda vai encontrar na campanha.</p>" +
      "<p>Se você é jogador e não está mestrando, melhor não abrir. Se spoiler não te incomoda, " +
      "fique à vontade.</p>" +
      "<div class='botoes'>" +
      H.botao("dispensar-aviso", "Entendi, pode abrir", { classe: "primario" }) +
      "<a class='botao' href='#jogar'>Voltar para a ficha</a>" +
      "</div>" +
      "<p class='ajuda'>Este aviso não aparece mais depois que você abrir.</p>" +
      "</section>";
  }

  // ---------------------------------------------------------------------------
  // Rota: as telas se registram em G.telas (mestre.js e mestre-escudo.js)
  // ---------------------------------------------------------------------------
  G.telas = {};

  function tela(r) {
    // A ficha aberta é zerada aqui: os delegados de ficha-base.js gravariam F.P em cima do que
    // esta tela escreveu. Jogar e Editar chamam F.abrirAtual() ao entrar, então nada se perde.
    EG.Ficha.P = null;
    EG.Ficha.R = null;
    if (!G.estado().aviso_lido) { telaAviso(); return; }
    const qual = (r && r.partes && r.partes[0]) || "painel";
    (G.telas[qual] || G.telas.painel)(r);
  }

  EG.registrarTela("mestre", tela);

  Object.assign(G, { ELEMENTOS, TIPOS, TELAS, obter, definir, idDe, modeloVazio, completar, CHAVE });
})();
