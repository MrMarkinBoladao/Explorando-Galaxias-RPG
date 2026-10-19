/*
 * mesa-online.js — A mesa online: as fichas, o PH, o combate e as rolagens ao vivo entre os
 * aparelhos do grupo.
 *
 * O site continua sem servidor. Quem guarda e espalha os dados é o Firebase Realtime
 * Database, e o navegador fala direto com ele. As regras do banco (firebase/
 * database.rules.json) rodam no servidor do Google e decidem quem lê o quê: o Mestre lê a
 * mesa inteira; o jogador lê a própria ficha, o PH do grupo, o retrato do combate e as
 * rolagens. Sem configuração (mesa-online-config.js) nada disto liga.
 *
 * Como isto se encaixa num site feito para funcionar sem internet:
 *
 * - A ficha continua morando no localStorage (EG.Armazem). A mesa guarda uma cópia
 *   compartilhada: cada gravação daqui manda só os campos que mudaram, e cada mudança que
 *   chega de fora é gravada aqui e a tela se redesenha. Lista vai inteira, como um campo.
 * - O PH é um número só da mesa (grupo/ph), não uma cópia em cada ficha. Gastar ou ganhar
 *   PH manda a diferença, e o servidor soma a de todo mundo numa transação.
 * - O combate é do Mestre. O navegador dele publica um retrato da Fila de Ação sem os
 *   números secretos dos inimigos, e o jogador manda pedidos ("terminei meu turno", "usei
 *   a Ultimate") que o navegador do Mestre aplica.
 * - O que é só do Mestre (inimigos, encontros, NPCs, notas) não sai do navegador dele.
 * - Sem internet, a gravação fica marcada como pendente. Na volta, as duas versões se
 *   juntam campo a campo: vale o que cada lado mudou desde a última vez que concordaram.
 */
(function () {
  "use strict";

  const EG = window.EG;
  const { esc } = EG;
  const F = EG.Ficha;
  const G = EG.Mestre;
  const M = window.Motor;
  const C = () => window.CATALOGO;

  const SDK = "https://www.gstatic.com/firebasejs/13.0.0/";
  const CHAVE = "explorando-galaxias:mesa-online";
  const N = (EG.MesaOnline = {});

  const config = () => window.EG_MESA_ONLINE;
  const configurada = () => !!(config() && config().apiKey);
  N.configurada = configurada;

  // ---------------------------------------------------------------------------
  // O que este aparelho lembra da mesa
  //
  // `ligadas`: as fichas deste aparelho que estão na mesa. `base`: o último estado em que
  // este aparelho e a mesa concordavam, por ficha — é com ele que se descobre, depois de
  // uma queda de internet, quem mudou o quê. `sujas`: as fichas com gravação ainda não
  // confirmada pelo servidor.
  // ---------------------------------------------------------------------------
  // `ph_valor` é o último PH da mesa que este aparelho conheceu e `ph_pendente`, a soma do
  // que mudou aqui e ainda não chegou ao servidor (sem internet, ou com a página fechada).
  function localVazio() {
    return { mesa: "", papel: "", uid: "", nome_mesa: "", ligadas: {}, base: {}, sujas: {},
      barras: true, escondido: false, ph_valor: null, ph_pendente: 0 };
  }

  function lerLocal() {
    let x = null;
    try { x = JSON.parse(localStorage.getItem(CHAVE)); } catch (_) { x = null; }
    return Object.assign(localVazio(), x && typeof x === "object" ? x : {});
  }

  let L = lerLocal();
  const gravarLocal = () => { try { localStorage.setItem(CHAVE, JSON.stringify(L)); } catch (_) { /* cheio */ } };

  // ---------------------------------------------------------------------------
  // A ficha no formato do banco
  //
  // O Firebase não aceita . # $ [ ] / numa chave, apaga nulos e objetos vazios e faz o que
  // quer com listas. Então: chave escapada, lista vira um texto JSON sob a chave "~a" (muda
  // inteira, como um campo só) e nulo simplesmente não vai — o completar() da ficha devolve
  // o padrão do modelo, que para todo campo que aceita nulo é equivalente.
  // ---------------------------------------------------------------------------
  const LISTA = "~a";
  const codChave = (k) => (k === "" ? "%E" : String(k).replace(/[.#$[\]/%~]/g,
    (c) => "%" + c.charCodeAt(0).toString(16).toUpperCase().padStart(2, "0")));
  const decChave = (k) => (k === "%E" ? "" : k.replace(/%([0-9A-F]{2})/g, (_, h) => String.fromCharCode(parseInt(h, 16))));

  /** Objeto em {caminho: valor}, só com folhas (texto, número, sim/não ou lista em JSON). */
  function achatar(obj, prefixo, saida) {
    saida = saida || {};
    for (const [k, v] of Object.entries(obj || {})) {
      if (v === null || v === undefined) continue;
      const cam = (prefixo ? prefixo + "/" : "") + codChave(k);
      if (Array.isArray(v)) saida[cam + "/" + LISTA] = JSON.stringify(v);
      else if (typeof v === "object") achatar(v, cam, saida);
      else if (typeof v === "number" && !Number.isFinite(v)) continue;
      else saida[cam] = v;
    }
    return saida;
  }

  /** {caminho: valor} de volta em objeto aninhado, ainda no formato do banco. */
  function desachatar(plano) {
    const raiz = {};
    for (const [cam, v] of Object.entries(plano)) {
      const partes = cam.split("/");
      let o = raiz;
      for (let i = 0; i < partes.length - 1; i++) {
        if (!o[partes[i]] || typeof o[partes[i]] !== "object") o[partes[i]] = {};
        o = o[partes[i]];
      }
      o[partes[partes.length - 1]] = v;
    }
    return raiz;
  }

  /** Do formato do banco para o da ficha: chaves de volta e listas de volta. */
  function decodificar(no) {
    if (no === null || typeof no !== "object") return no;
    const chaves = Object.keys(no);
    if (chaves.length === 1 && chaves[0] === LISTA) {
      try { const l = JSON.parse(no[LISTA]); return Array.isArray(l) ? l : []; } catch (_) { return []; }
    }
    const saida = {};
    for (const k of chaves) saida[decChave(k)] = decodificar(no[k]);
    return saida;
  }

  /**
   * O que da ficha vai para a mesa: tudo, menos o PH (que é do grupo, em grupo/ph) e a hora
   * da última gravação local (cada aparelho tem a sua).
   */
  function paraMesa(p) {
    const c = F.completar(EG.clonar(p));
    delete c.atualizado;
    if (c.jogo) delete c.jogo.ph;
    return c;
  }
  const planoDe = (p) => achatar(paraMesa(p));

  // Texto comprido (a arte do Cone em `data:`) entra na `base` como uma impressão digital:
  // a base guarda só o bastante para saber se mudou, e não uma segunda cópia da imagem.
  const LONGO = 1500;
  function marca(v) {
    if (typeof v !== "string" || v.length <= LONGO) return v;
    let h = 0x811c9dc5;
    for (let i = 0; i < v.length; i++) { h ^= v.charCodeAt(i); h = Math.imul(h, 0x01000193); }
    return "#h" + (h >>> 0).toString(36) + ":" + v.length;
  }
  const marcado = (plano) => { const m = {}; for (const k in plano) m[k] = marca(plano[k]); return m; };

  /** O que mudou de `de` para `para`: {caminho: valor novo, ou null para o que sumiu}. */
  function diferenca(de, para) {
    de = de || {};
    const mud = {};
    for (const k in para) if (marca(para[k]) !== marca(de[k])) mud[k] = para[k];
    for (const k in de) if (!(k in para)) mud[k] = null;
    return mud;
  }

  /**
   * O update do Firebase recusa um caminho dentro do outro na mesma gravação ("a" e "a/b").
   * Isso só acontece quando um campo troca de forma (de valor para lista, por exemplo): aí
   * vai o galho inteiro de uma vez.
   */
  function semSobreposicao(mud, plano) {
    const cams = Object.keys(mud);
    const pais = cams.filter((c) => cams.some((d) => d !== c && d.startsWith(c + "/")));
    if (!pais.length) return mud;
    const saida = Object.assign({}, mud);
    for (const c of pais) {
      for (const d of cams) if (d.startsWith(c + "/")) delete saida[d];
      if (c in plano) { saida[c] = plano[c]; continue; }
      const sub = {};
      for (const k in plano) if (k.startsWith(c + "/")) sub[k.slice(c.length + 1)] = plano[k];
      saida[c] = Object.keys(sub).length ? desachatar(sub) : null;
    }
    for (const c of Object.keys(saida)) {
      if (Object.keys(saida).some((d) => d !== c && c.startsWith(d + "/"))) delete saida[c];
    }
    return saida;
  }

  const resultadoDe = (p) => M.calcular(F.paraMotor(F.completar(EG.clonar(p))), C());

  // ---------------------------------------------------------------------------
  // Firebase: o SDK só carrega para quem usa a mesa (são uns 330 KB)
  // ---------------------------------------------------------------------------
  let sdk = null, iniciando = null;
  let auth = null, db = null, usuario = null;
  let fase = configurada() ? "parada" : "desligada";   // parada · carregando · sem-login · sem-mesa · conectando · conectada · erro
  let motivo = "";                                      // o porquê do erro, em texto de gente
  let online = false;                                   // .info/connected
  let mesasDoUsuario = {};                              // {mesa: papel} — para escolher, quando há várias

  function carregarScript(url) {
    return new Promise((ok, falha) => {
      const s = document.createElement("script");
      s.src = url;
      s.async = false;
      s.onload = () => ok();
      s.onerror = () => { s.remove(); falha(new Error("não carregou " + url)); };
      document.head.appendChild(s);
    });
  }

  function carregarSDK() {
    if (window.firebase && window.firebase.database && window.firebase.auth) return Promise.resolve();
    if (!sdk) {
      sdk = carregarScript(SDK + "firebase-app-compat.js")
        .then(() => Promise.all([carregarScript(SDK + "firebase-auth-compat.js"),
          carregarScript(SDK + "firebase-database-compat.js")]))
        .catch((e) => { sdk = null; throw e; });
    }
    return sdk;
  }

  /** Liga o Firebase e passa a acompanhar o login. Pode ser chamada quantas vezes for. */
  function iniciar() {
    if (!configurada()) return Promise.resolve(false);
    if (auth) return Promise.resolve(true);
    if (iniciando) return iniciando;
    fase = "carregando";
    iniciando = carregarSDK().then(() => {
      const cfg = config();
      const app = window.firebase.apps.length ? window.firebase.app() : window.firebase.initializeApp(cfg);
      auth = app.auth();
      db = app.database();
      if (cfg.emulador) {                       // só nos testes: o emulador do Firebase
        auth.useEmulator(cfg.emulador.auth);
        const [host, porta] = String(cfg.emulador.database).split(":");
        db.useEmulator(host, Number(porta));
      }
      db.ref(".info/connected").on("value", (s) => {
        const antes = online;
        online = s.val() === true;
        // Voltou a conexão: o PH que mudou sem internet vai agora.
        if (online && !antes && (ph.pendente || ph.absoluto != null)) agendarEnvioPH();
        if (antes !== online) redesenhar();
      });
      return new Promise((ok) => {
        let primeira = true;
        auth.onAuthStateChanged((u) => {
          aoMudarUsuario(u);
          if (primeira) { primeira = false; ok(true); }
        });
      });
    }).catch((e) => {
      console.error(e);
      iniciando = null;
      fase = "erro";
      motivo = "Não foi possível falar com a mesa online. Sem internet? As fichas continuam salvas neste aparelho.";
      redesenhar();
      return false;
    });
    return iniciando;
  }

  N.iniciar = iniciar;

  const ts = () => window.firebase.database.ServerValue.TIMESTAMP;
  const ref = (cam) => db.ref("mesas/" + L.mesa + (cam ? "/" + cam : ""));
  const nomeDoUsuario = () => (usuario && (usuario.displayName || usuario.email)) || "Jogador";
  const conectada = () => fase === "conectada" && !!db && !!L.mesa;

  function avisarErro(e, oQue) {
    console.error(e);
    const negado = /permission|PERMISSION_DENIED/i.test(String(e && (e.code || e.message)));
    EG.toast(negado ? "A mesa online recusou gravar " + oQue + ": sem permissão. Você ainda está nesta mesa?"
      : "Não deu para gravar " + oQue + " na mesa online agora. Tentando de novo quando a conexão voltar.", "erro");
  }

  // ---------------------------------------------------------------------------
  // Login
  // ---------------------------------------------------------------------------
  /**
   * A janela do Google precisa abrir dentro do clique, senão o navegador bloqueia. Com o
   * Firebase já carregado (as telas da mesa carregam ao abrir) ela abre na hora; se ainda
   * estiver carregando, tenta assim mesmo e, se bloquear, pede um segundo clique.
   */
  function entrar() {
    const janela = () => {
      const prov = new window.firebase.auth.GoogleAuthProvider();
      prov.setCustomParameters({ prompt: "select_account" });
      return auth.signInWithPopup(prov).catch((e) => {
        const c = (e && e.code) || "";
        if (/popup-closed-by-user|cancelled-popup-request/.test(c)) return;
        EG.toast(/popup-blocked/.test(c)
          ? "O navegador bloqueou a janela de login. Clique de novo em Entrar com Google (e, se continuar, permita pop-ups deste site)."
          : /unauthorized-domain/.test(c)
            ? "Este endereço não está autorizado no Firebase (Authentication &gt; Configurações &gt; Domínios autorizados)."
            : /operation-not-allowed/.test(c)
              ? "O login com Google ainda não está ativado no Firebase: Authentication &gt; Método de login &gt; Google &gt; " +
                "<b>Ativar</b> e <b>Salvar</b>."
              : /network-request-failed/.test(c)
                ? "Sem conexão com o Google agora. Confira a internet e tente de novo."
                : "Não deu para entrar: " + esc(e && e.message ? e.message : c), "erro");
      });
    };
    if (auth) return janela();
    return iniciar().then((ligou) => (ligou && !usuario ? janela() : null));
  }

  /** Sair da conta: primeiro apaga a presença (ainda com o login), depois sai. */
  function sair() {
    if (!auth) return Promise.resolve();
    return pararTudo().then(() => auth.signOut());
  }

  function aoMudarUsuario(u) {
    usuario = u;
    if (!u) { pararTudo(); fase = "sem-login"; redesenhar(); return; }
    if (L.uid && L.uid !== u.uid) {
      // Outra conta neste aparelho: as ligações eram da conta de antes. As fichas ficam.
      const op = { barras: L.barras, escondido: L.escondido };
      L = Object.assign(localVazio(), op);
      zerarPH();
      EG.toast("Você entrou com outra conta. As fichas deste aparelho continuam salvas, fora da mesa.");
    }
    L.uid = u.uid;
    gravarLocal();
    db.ref("usuarios/" + u.uid + "/mesas").once("value").then((s) => {
      mesasDoUsuario = s.val() || {};
      if (L.mesa) return conectar(L.mesa);
      const ids = Object.keys(mesasDoUsuario);
      if (ids.length === 1 && !convitePendente()) return conectar(ids[0]);
      fase = "sem-mesa";
      redesenhar();
    }).catch((e) => { console.error(e); fase = "sem-mesa"; redesenhar(); });
  }

  const convitePendente = () => EG.rotaAtual().tela === "entrar";

  // ---------------------------------------------------------------------------
  // Conectar e desconectar
  // ---------------------------------------------------------------------------
  const ouvintes = [];
  function ouvir(r, evento, fn) {
    r.on(evento, fn, (e) => perdeuAcesso(e));
    ouvintes.push({ r: r, evento: evento, fn: fn });
  }

  /** Para de ouvir a mesa. Devolve quando a presença deste aparelho já saiu da lista. */
  // O PH conhecido e o pendente sobrevivem a parar de ouvir: reconectar à mesma mesa não pode
  // perder o +1 que alguém clicou enquanto a conexão caía. Quem zera é trocar de mesa ou sair.
  function pararTudo() {
    for (const o of ouvintes.splice(0)) o.r.off(o.evento, o.fn);
    for (const id of Object.keys(sync)) { sync[id].r.off("value", sync[id].fn); delete sync[id]; }
    const p = presencaRef;
    presencaRef = null;
    clearTimeout(combateTimer);
    combate = null; combateEnviado = ""; membros = {}; presentes = {}; convite = null;
    pedidoFeito = null;
    return p ? p.remove().catch(() => {}) : Promise.resolve();
  }

  function perdeuAcesso(e) {
    console.error(e);
    if (fase !== "conectada") return;
    pararTudo();
    EG.toast("A mesa online não deixou mais este aparelho ler a mesa <b>" + esc(L.nome_mesa) + "</b>. " +
      "As fichas continuam salvas aqui.", "erro");
    soltarMesa();
  }

  /** Este aparelho larga a mesa: as fichas ficam, só param de sincronizar. */
  function soltarMesa() {
    const op = { barras: L.barras, escondido: L.escondido, uid: L.uid };
    L = Object.assign(localVazio(), op);
    zerarPH();
    gravarLocal();
    fase = usuario ? "sem-mesa" : "sem-login";
    mostrarAbaDoMestre();
    redesenhar();
  }

  function conectar(mesa) {
    pararTudo();
    fase = "conectando";
    redesenhar();
    return db.ref("mesas/" + mesa + "/info").once("value").then((s) => {
      const info = s.val();
      if (!info) throw new Error("mesa sumiu");
      const mudouDeMesa = L.mesa && L.mesa !== mesa;
      if (mudouDeMesa) { L.ligadas = {}; L.base = {}; L.sujas = {}; zerarPH(); }
      L.mesa = mesa;
      L.nome_mesa = info.nome || "Mesa sem nome";
      L.papel = info.mestre === usuario.uid ? "mestre" : "jogador";
      gravarLocal();
      fase = "conectada";
      mostrarAbaDoMestre();
      marcarPresenca();
      ouvir(ref("grupo/ph"), "value", aoChegarPH);
      ouvir(ref("presenca"), "value", (x) => { presentes = x.val() || {}; redesenhar(); });
      ouvirRolagens();
      if (L.papel === "mestre") {
        ouvir(ref("fichas"), "child_added", (x) => ligar(x.key));
        ouvir(ref("membros"), "value", (x) => { membros = x.val() || {}; redesenhar(); });
        ouvir(ref("pedidos"), "child_added", tratarPedido);
        db.ref("usuarios/" + usuario.uid + "/mesas/" + mesa).set("mestre").catch(() => {});
        limparRolagensVelhas();
        agendarCombate();
      } else {
        ouvir(ref("membros/" + usuario.uid), "value", aoChegarMembro);
        ouvir(ref("combate"), "value", aoChegarCombate);
      }
      redesenhar();
    }).catch((e) => {
      console.error(e);
      // Sem permissão: não é mais membro (ou a mesa foi apagada). Sem rede: tenta depois.
      if (/permission|denied|sumiu/i.test(String(e && (e.code || e.message)))) {
        if (usuario) db.ref("usuarios/" + usuario.uid + "/mesas/" + mesa).remove().catch(() => {});
        delete mesasDoUsuario[mesa];
        EG.toast("Você não está mais na mesa <b>" + esc(L.nome_mesa || "") + "</b>. As fichas continuam salvas aqui.", "erro");
        soltarMesa();
      } else {
        fase = "erro";
        motivo = "Não deu para abrir a mesa agora. Sem internet?";
        redesenhar();
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Criar a mesa, convidar e entrar
  // ---------------------------------------------------------------------------
  function codigoNovo() {
    const b = new Uint8Array(18);
    (window.crypto || window.msCrypto).getRandomValues(b);
    return btoa(String.fromCharCode.apply(null, b)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  function criarMesa(nome) {
    if (!usuario) return Promise.resolve();
    const id = db.ref("mesas").push().key;
    const base = db.ref("mesas/" + id);
    nome = String(nome || "").trim().slice(0, 80) || "Mesa de Explorando Galáxias";
    // Primeiro a mesa existir (é ela que diz quem é o Mestre), depois o resto.
    return base.child("info").set({ nome: nome, mestre: usuario.uid, criada: ts() })
      .then(() => base.child("convite").set({ codigo: codigoNovo() }))
      .then(() => db.ref("usuarios/" + usuario.uid + "/mesas/" + id).set("mestre"))
      .then(() => {
        mesasDoUsuario[id] = "mestre";
        // O PH da mesa começa com o do grupo que já está neste navegador.
        const r = G.recursoPH();
        if (r) base.child("grupo/ph").set(r.atual).catch(() => {});
        return conectar(id);
      })
      .then(() => EG.toast("Mesa online <b>" + esc(nome) + "</b> criada. Copie o convite e mande para o grupo."))
      .catch((e) => avisarErro(e, "a mesa"));
  }

  let convite = null;                         // null: ainda não leu; "": a mesa está sem convite
  function lerConvite() {
    if (L.papel !== "mestre" || !conectada() || convite !== null) return;
    convite = "";
    ref("convite/codigo").once("value").then((s) => { convite = s.val() || ""; redesenhar(); }).catch(() => {});
  }

  function gerarConvite() {
    const c = codigoNovo();
    return ref("convite").set({ codigo: c }).then(() => {
      convite = c;
      EG.toast("Convite novo gerado. O link antigo não funciona mais; quem já entrou continua na mesa.");
      redesenhar();
    }).catch((e) => avisarErro(e, "o convite"));
  }

  function linkDoConvite() {
    return convite ? location.href.split("#")[0] + "#entrar/" + L.mesa + "/" + convite : "";
  }

  function entrarNaMesa(mesa, codigo) {
    if (!usuario) return Promise.resolve();
    return db.ref("mesas/" + mesa + "/info/mestre").once("value").then(
      (s) => s.val() === usuario.uid,                // o próprio Mestre abrindo o convite
      () => false)
      .then((souMestre) => souMestre ? null
        : db.ref("mesas/" + mesa + "/membros/" + usuario.uid).update({ nome: nomeDoUsuario().slice(0, 80),
          codigo: codigo, entrou: ts() }))
      .then(() => db.ref("usuarios/" + usuario.uid + "/mesas/" + mesa).set("jogador").catch(() => {}))
      .then(() => conectar(mesa))
      .then(() => {
        if (fase !== "conectada") return;
        EG.toast("Você entrou na mesa <b>" + esc(L.nome_mesa) + "</b>.");
        location.hash = L.papel === "mestre" ? "#mestre" : "#mesa";
      })
      .catch((e) => {
        console.error(e);
        EG.toast(/permission|denied/i.test(String(e && (e.code || e.message)))
          ? "Este convite não vale mais. Peça um link novo ao Mestre." : "Não deu para entrar na mesa agora.", "erro");
      });
  }

  // ---------------------------------------------------------------------------
  // Fichas: ligar, chegar de fora, sair daqui
  // ---------------------------------------------------------------------------
  const sync = {};       // por ficha: {r, fn, pronto, enviado (plano), pendentes, dono}
  let aplicando = 0;

  function ligar(id) {
    if (!conectada() || sync[id]) return;
    const r = ref("fichas/" + id);
    const st = { r: r, pronto: false, enviado: null, pendentes: 0, dono: "" };
    st.fn = (snap) => aoChegarFicha(id, snap);
    sync[id] = st;
    r.on("value", st.fn, (e) => { console.error(e); desligar(id); redesenhar(); });
    if (!L.ligadas[id]) { L.ligadas[id] = true; gravarLocal(); }
  }

  function desligar(id) {
    const st = sync[id];
    if (st) { st.r.off("value", st.fn); delete sync[id]; }
    delete L.ligadas[id];
    delete L.base[id];
    delete L.sujas[id];
    gravarLocal();
  }

  /** A ficha local com estas mudanças aplicadas, campo a campo, sem chamar o gancho. */
  function escreverLocal(id, plano) {
    const mapa = EG.Armazem.todas();
    const antes = mapa[id];
    const nova = F.completar(decodificar(desachatar(plano)));
    nova.id = id;
    nova.atualizado = new Date().toISOString();
    nova.jogo.ph = ph.valor != null ? ph.valor : antes && antes.jogo ? antes.jogo.ph : null;
    mapa[id] = nova;
    aplicando++;
    try { EG.Armazem.gravarTodas(mapa); } finally { aplicando--; }
    // A ficha aberta na tela é a mesma ficha: sem isto, a próxima tecla gravaria por cima a
    // versão de antes. O objeto é o mesmo (só troca o recheio), então quem guardou uma
    // referência para ele continua certo.
    if (F.P && F.P.id === id && !F.aoSalvar) {
      for (const k of Object.keys(F.P)) delete F.P[k];
      Object.assign(F.P, EG.clonar(nova));
      F.recalcular();
    }
    return nova;
  }

  /** A ficha saiu da mesa (por este aparelho ou por outro): para de sincronizar, e a cópia fica. */
  function saiuDaMesa(id) {
    if (!sync[id] && !L.ligadas[id]) return;
    const p = EG.Armazem.todas()[id];
    desligar(id);
    if (L.papel === "mestre") tirarDoGrupo(id);
    EG.toast("<b>" + esc((p && p.nome) || "Uma ficha") + "</b> saiu da mesa online." +
      (p ? " A cópia deste aparelho continua salva." : ""));
    aposMudarFichas();
  }

  function aoChegarFicha(id, snap) {
    const st = sync[id];
    if (!st) return;
    const v = snap.val();
    if (!v || !v.f) { saiuDaMesa(id); return; }
    st.dono = v.dono || "";
    const remota = F.completar(decodificar(v.f));
    const planoR = planoDe(remota);
    if (!st.pronto) {
      primeiraSincronia(id, st, planoR);
      st.pronto = true;
      if (L.papel === "mestre") porNoGrupo(id);
      aposMudarFichas();
      return;
    }
    const mud = diferenca(st.enviado, planoR);
    if (!Object.keys(mud).length) return;
    const local = EG.Armazem.todas()[id];
    const plano = local ? planoDe(local) : {};
    for (const [c, val] of Object.entries(mud)) {
      for (const k of Object.keys(plano)) if (k === c || k.startsWith(c + "/")) delete plano[k];
      if (val !== null) plano[c] = val;
    }
    escreverLocal(id, plano);
    st.enviado = planoR;
    if (!st.pendentes) { L.base[id] = marcado(planoR); delete L.sujas[id]; gravarLocal(); }
    aposMudarFichas();
  }

  /**
   * A primeira vez que a ficha chega depois de conectar. Se este aparelho não tem nada
   * pendente, vale a da mesa. Se tem (gravou sem internet e a página fechou antes de
   * mandar), junta as duas: o que mudou aqui desde a última vez em que concordavam vai
   * para a mesa, e o resto vem de lá.
   */
  function primeiraSincronia(id, st, planoR) {
    const local = EG.Armazem.todas()[id];
    const base = L.base[id];
    if (local && L.sujas[id] && base) {
      const planoL = planoDe(local);
      const minhas = diferenca(base, planoL);
      const final = Object.assign({}, planoR);
      for (const [c, v] of Object.entries(minhas)) {
        for (const k of Object.keys(final)) if (k === c || k.startsWith(c + "/")) delete final[k];
        if (v !== null) final[c] = v;
      }
      escreverLocal(id, final);
      st.enviado = final;
      if (Object.keys(minhas).length) enviar(id, semSobreposicao(minhas, final));
      else { L.base[id] = marcado(final); delete L.sujas[id]; gravarLocal(); }
      return;
    }
    escreverLocal(id, planoR);
    st.enviado = planoR;
    L.base[id] = marcado(planoR);
    delete L.sujas[id];
    gravarLocal();
  }

  function enviar(id, mud) {
    const st = sync[id];
    if (!st || !Object.keys(mud).length) return;
    const caminhos = {};
    for (const [c, v] of Object.entries(mud)) caminhos["f/" + c] = v;
    st.pendentes++;
    L.sujas[id] = true;
    gravarLocal();
    st.r.update(caminhos).then(() => {
      st.pendentes--;
      if (!st.pendentes && sync[id] === st) { L.base[id] = marcado(st.enviado); delete L.sujas[id]; gravarLocal(); }
    }).catch((e) => { st.pendentes--; avisarErro(e, "a ficha"); });
  }

  /** O gancho de EG.Armazem.salvar: manda para a mesa só o que mudou. */
  EG.aoSalvarFicha = function (p) {
    if (aplicando || !p || !L.ligadas[p.id]) return;
    // O PH é do grupo (grupo/ph), não desta ficha: a mudança dele vale mesmo que a ficha
    // ainda não tenha chegado da mesa ou que a internet tenha caído — fica pendente e vai.
    registrarPH(p);
    const st = sync[p.id];
    if (!conectada() || !st || !st.pronto) {
      // Sem conexão, ou a ficha ainda não chegou: fica marcada, e junta quando chegar.
      L.sujas[p.id] = true;
      gravarLocal();
      return;
    }
    const plano = planoDe(p);
    const mud = diferenca(st.enviado, plano);
    st.enviado = plano;
    if (Object.keys(mud).length) enviar(p.id, semSobreposicao(mud, plano));
    aposMudarFichas(false);
  };

  /** O gancho de EG.Armazem.excluir: quem exclui uma ficha da mesa tira ela da mesa também. */
  EG.aoExcluirFicha = function (id) {
    if (!L.ligadas[id]) return;
    const st = sync[id];
    if (conectada()) {
      const dono = (st && st.dono) || (L.papel === "jogador" ? usuario.uid : "");
      const apagar = { ["fichas/" + id]: null };
      if (dono) apagar["membros/" + dono + "/fichas/" + id] = null;
      ref().update(apagar).catch((e) => avisarErro(e, "a saída da ficha"));
    }
    desligar(id);
    if (L.papel === "mestre") tirarDoGrupo(id);
  };

  N.estaNaMesa = (id) => !!(id && L.ligadas[id]);

  /** O jogador leva uma ficha deste aparelho para a mesa. */
  function levarFicha(id) {
    const p = EG.Armazem.todas()[id];
    if (!p || !conectada() || L.papel !== "jogador") return Promise.resolve();
    const plano = planoDe(p);
    const fichaRef = ref("fichas/" + id);
    return fichaRef.set({ dono: usuario.uid, f: desachatar(plano) })
      .then(() => ref("membros/" + usuario.uid + "/fichas/" + id).set(true))
      .then(() => {
        // Se a mesa ainda não tem PH, começa com o desta ficha.
        const valor = p.jogo && Number.isFinite(p.jogo.ph) ? p.jogo.ph : resultadoDe(p).ph_inicio;
        ref("grupo/ph").transaction((cur) => (cur == null ? valor : undefined)).catch(() => {});
        L.base[id] = marcado(plano);
        delete L.sujas[id];
        gravarLocal();
        EG.toast("<b>" + esc(p.nome || "A ficha") + "</b> está na mesa <b>" + esc(L.nome_mesa) + "</b>. " +
          "O que mudar nela agora aparece para o Mestre na hora.");
      })
      .catch((e) => {
        console.error(e);
        EG.toast(/permission|denied/i.test(String(e && (e.code || e.message)))
          ? "Esta ficha já está na mesa com outro dono. Faça uma cópia dela (Mais &gt; Exportar e Importar como cópia)."
          : "Não deu para levar a ficha agora.", "erro");
      });
  }

  /** Tira uma ficha da mesa (o dono, ou o Mestre). A cópia de cada aparelho fica. */
  function tirarFicha(id) {
    const st = sync[id];
    const dono = (st && st.dono) || (L.papel === "jogador" ? usuario.uid : "");
    const apagar = { ["fichas/" + id]: null };
    if (dono) apagar["membros/" + dono + "/fichas/" + id] = null;
    return ref().update(apagar).catch((e) => avisarErro(e, "a saída da ficha"));
  }

  /** Jogador: a lista de fichas dele nesta mesa diz o que ligar e o que desligar. */
  function aoChegarMembro(snap) {
    const v = snap.val();
    if (!v) {                                   // o Mestre tirou este jogador da mesa
      EG.toast("Você saiu da mesa <b>" + esc(L.nome_mesa) + "</b>. As fichas continuam salvas aqui.", "erro");
      if (usuario) db.ref("usuarios/" + usuario.uid + "/mesas/" + L.mesa).remove().catch(() => {});
      pararTudo();
      soltarMesa();
      return;
    }
    const minhas = Object.keys(v.fichas || {});
    for (const id of minhas) ligar(id);
    for (const id of Object.keys(L.ligadas)) if (minhas.indexOf(id) < 0) saiuDaMesa(id);
    redesenhar();
  }

  // Mestre: a ficha que chega entra no grupo, e a que sai, sai do grupo (a cópia fica).
  function porNoGrupo(id) {
    const est = G.estado();
    if (est.grupo.indexOf(id) < 0) { est.grupo.push(id); G.salvar(); }
  }
  function tirarDoGrupo(id) {
    const est = G.estado(), i = est.grupo.indexOf(id);
    if (i >= 0) { est.grupo.splice(i, 1); G.salvar(); }
  }

  // ---------------------------------------------------------------------------
  // PH do grupo: um número só, somado no servidor (16.2)
  //
  // Cada mudança vira uma **diferença**, calculada na hora do clique contra o PH que este
  // aparelho conhece (`valor`), e as diferenças vão somadas numa transação: dois jogadores
  // gastando no mesmo instante, os dois gastos contam. A diferença não pode ser calculada
  // depois — se o PH de outra pessoa chegasse no meio, o clique daqui viraria outra conta.
  // O que ainda não foi (`pendente`) fica guardado no aparelho e vai quando a mesa voltar,
  // mesmo que a página tenha fechado nesse meio-tempo.
  // ---------------------------------------------------------------------------
  // `emVoo` é o que já foi numa transação que o servidor ainda não confirmou. No aparelho
  // fica guardada a soma de `pendente` e `emVoo`: se a página fechar antes da confirmação,
  // a mudança vai de novo na volta, em vez de sumir.
  const ph = {
    valor: L.mesa && Number.isFinite(L.ph_valor) ? L.ph_valor : null,
    pendente: L.mesa && Number.isFinite(L.ph_pendente) ? L.ph_pendente : 0,
    emVoo: 0,
    absoluto: null,                 // mudança feita antes de conhecer o PH da mesa
    max: 99, timer: 0,
  };

  function zerarPH() {
    clearTimeout(ph.timer);
    Object.assign(ph, { valor: null, pendente: 0, emVoo: 0, absoluto: null, max: 99, timer: 0 });
    L.ph_valor = null;
    L.ph_pendente = 0;
  }

  function guardarPH() {
    L.ph_valor = ph.valor;
    L.ph_pendente = ph.pendente + ph.emVoo;
    gravarLocal();
  }

  /**
   * Põe o PH da mesa em todas as fichas deste aparelho que estão nela, sem chamar o gancho
   * (senão a mudança voltaria para a mesa como se fosse nova). Devolve se algo mudou.
   */
  function espalharPH(v) {
    const mapa = EG.Armazem.todas();
    let mudou = false;
    for (const id of Object.keys(L.ligadas)) {
      const p = mapa[id];
      if (p && p.jogo && p.jogo.ph !== v) { p.jogo.ph = v; mudou = true; }
    }
    if (mudou) {
      aplicando++;
      try { EG.Armazem.gravarTodas(mapa); } finally { aplicando--; }
    }
    if (F.P && L.ligadas[F.P.id] && !F.aoSalvar && F.P.jogo.ph !== v) { F.P.jogo.ph = v; mudou = true; }
    return mudou;
  }

  /**
   * O número do PH na tela, trocado no lugar. A tela inteira só se redesenha quando ninguém
   * está digitando; o PH do grupo não pode esperar isso — quem acabou de digitar o dano e
   * ficou com o cursor no campo veria o PH velho até clicar em outro lugar.
   */
  function mostrarPHNaTela(v) {
    document.querySelectorAll("[data-ph-grupo]").forEach((el) => {
      const max = el.getAttribute("data-ph-max");
      el.textContent = v + (max ? " / " + max : "");
    });
  }

  function aoChegarPH(snap) {
    const v = snap.val();
    if (v == null) { if (ph.pendente || ph.absoluto != null) agendarEnvioPH(); return; }
    // O que mudou aqui e ainda não foi continua valendo por cima do que chegou. (O que está
    // em voo já vem dentro de `v`: a transação mostra o valor dela aqui antes de confirmar.)
    ph.valor = Math.max(0, v + ph.pendente);
    guardarPH();
    if (ph.pendente || ph.absoluto != null) agendarEnvioPH();
    if (!espalharPH(ph.valor)) return;
    mostrarPHNaTela(ph.valor);
    aposMudarFichas();
  }

  /** Uma ficha da mesa foi gravada aqui: se o PH dela mudou, a diferença vai para o grupo. */
  function registrarPH(p) {
    const v = p && p.jogo && Number.isFinite(p.jogo.ph) ? p.jogo.ph : null;
    if (v == null || v === ph.valor) return;
    ph.max = resultadoDe(p).ph_max || 99;
    if (ph.valor == null) ph.absoluto = v;           // ainda não conheço o PH da mesa
    else ph.pendente += v - ph.valor;
    ph.valor = v;
    guardarPH();
    espalharPH(v);                                   // as outras fichas da mesa, neste aparelho
    agendarEnvioPH();
  }

  /**
   * Várias fichas gravando o mesmo PH no mesmo instante (o Mestre ajustando o grupo todo)
   * são uma mudança só: o envio espera o fim da rodada e manda a soma uma vez.
   */
  function agendarEnvioPH() {
    if (!ph.timer) ph.timer = setTimeout(enviarPH, 0);
  }

  function enviarPH() {
    ph.timer = 0;
    // Sem conexão a transação ficaria só na memória e sumiria se a página fechasse: a mudança
    // espera aqui, guardada, e vai quando a conexão voltar (`.info/connected`).
    if (!conectada() || !online) return;
    const d = ph.pendente, absoluto = ph.absoluto, local = ph.valor, max = ph.max;
    if (!d && absoluto == null) return;
    ph.pendente = 0;
    ph.absoluto = null;
    ph.emVoo += d;
    guardarPH();
    const limitar = (x) => Math.max(0, Math.min(max, Math.round(x)));
    const fim = () => { ph.emVoo -= d; guardarPH(); };
    ref("grupo/ph").transaction((cur) => {
      if (cur == null) return limitar(absoluto != null ? absoluto : local);   // a mesa ainda não tinha PH
      if (!d) return undefined;                      // só um valor solto e a mesa já tem o dela: vale o da mesa
      return limitar(cur + d);
    }).then(fim, (e) => { fim(); avisarErro(e, "o PH"); });
  }

  /**
   * O PH da mesa, para a Área do Mestre: com uma ficha do grupo na mesa online, o PH que
   * vale é o da mesa — e não o menor PH das fichas deste navegador. Nulo fora da mesa.
   */
  N.phDaMesa = function (g) {
    if (!configurada() || !L.mesa || ph.valor == null) return null;
    if (g && !g.some((m) => L.ligadas[m.id])) return null;
    return ph.valor;
  };

  // ---------------------------------------------------------------------------
  // O combate: o Mestre publica o retrato, o jogador lê
  // ---------------------------------------------------------------------------
  let combate = null, combateEnviado = "", combateTimer = 0;

  const pct = (v, max) => (max > 0 ? Math.max(0, Math.min(100, Math.round(100 * v / max))) : 0);

  /**
   * O que o jogador vê do combate. Do grupo e dos aliados: PV, Energia, Ultimate pronta,
   * Morrendo e condições. Dos inimigos: nome, tipo, Quebrado, condições e — se o Mestre
   * deixar — as barras de PV e de Tenacidade, sem número. Fraqueza, ataque, Defesa e DT
   * nunca saem do navegador do Mestre.
   */
  function retratoDoCombate() {
    const cb = G.estado().combate;
    if (!cb.ativo) return { v: 1, ativo: false };
    const f = G.fila();
    const casa = (i) => {
      const aliado = i.kind === "pj" || i.kind === "memo" ||
        ((i.kind === "npc" || i.kind === "npcmemo") && i.papel === "Aliado");
      const o = { k: i.chave, n: i.nome, t: i.kind, tipo: i.kind === "inimigo" ? i.tipo : i.papel || "",
        c: i.casa, agora: !!i.agora, agiu: !!i.cc.agiu, ult: !!i.cc.ultimate, sur: !!i.cc.surpreso,
        atr: i.atraso_casas || 0, ava: i.avanco_casas || 0, caiu: i.pv === 0, pula: !!i.derrotado, aliado: aliado,
        cond: (i.condicoes || []).filter((c) => c.nome !== "Quebrado").map((c) =>
          ({ n: c.nome, t: c.turnos == null ? null : c.turnos, a: c.acumulos > 1 ? c.acumulos : 0 })) };
      if (i.x) o.qb = !!i.x.quebrado;
      if (aliado) {
        o.pv = i.pv;
        o.pvm = i.pv_max;
        if (i.m && (i.kind === "pj" || i.kind === "npc")) {
          const j = i.m.p.jogo;
          o.en = j.energia || 0;
          o.uc = i.m.R.ultimate.custo;
          if (i.pv === 0) o.mo = { s: (j.morrendo || {}).s || 0, f: (j.morrendo || {}).f || 0 };
        }
      } else if (L.barras) {
        o.pct = pct(i.pv, i.pv_max);
        if (i.x) o.tpct = pct(G.tenacidadeAtual(i.x), i.x.tenacidade || 0);
      }
      return o;
    };
    // `id` é o começo do combate: com o Ciclo, ele diz à ficha de cada jogador em que combate e
    // em que Ciclo a Energia "1 vez por Ciclo" (17.2) já contou.
    return { v: 1, ativo: true, id: Number(cb.inicio) || 0, nome: cb.nome || "", ciclo: cb.ciclo || 1, fila: f.casas.map(casa) };
  }

  EG.aoSalvarMesa = () => agendarCombate();

  function agendarCombate() {
    if (L.papel !== "mestre" || !conectada()) return;
    clearTimeout(combateTimer);
    combateTimer = setTimeout(publicarCombate, 150);
  }

  function publicarCombate() {
    if (L.papel !== "mestre" || !conectada()) return;
    let json;
    try { json = JSON.stringify(retratoDoCombate()); } catch (e) { console.error(e); return; }
    if (json === combateEnviado) return;
    combateEnviado = json;
    ref("combate").set({ json: json, em: ts() }).catch((e) => { combateEnviado = ""; avisarErro(e, "o combate"); });
  }

  function aoChegarCombate(snap) {
    const v = snap.val();
    let c = null;
    try { c = v && v.json ? JSON.parse(v.json) : null; } catch (_) { c = null; }
    combate = c && typeof c === "object" ? c : null;
    if (combate) combate.em = v.em || 0;
    // O pedido de "terminei" vale até o Mestre aplicar (a casa aparece como já agiu) ou o
    // Ciclo virar. Depois disso o botão volta a valer, inclusive se o Mestre desfizer.
    if (pedidoFeito) {
      const eu = combate && combate.ativo && Array.isArray(combate.fila)
        ? combate.fila.find((x) => x.k === "p:" + pedidoFeito.ficha) : null;
      if (!eu || eu.agiu || combate.ciclo !== pedidoFeito.ciclo) pedidoFeito = null;
    }
    redesenhar();
  }

  N.combate = () => combate;

  // ---------------------------------------------------------------------------
  // Pedidos do jogador ao Mestre: "terminei meu turno", "usei a Ultimate"
  // ---------------------------------------------------------------------------
  let pedidoFeito = null;                     // {ficha, ciclo}: o botão some até o Mestre responder

  N.pedir = function (tipo, ficha) {
    if (!conectada() || L.papel !== "jogador" || !L.ligadas[ficha]) return false;
    if (!combate || !combate.ativo) return false;
    const pedido = { uid: usuario.uid, ficha: ficha, tipo: tipo, ciclo: combate.ciclo || 1, em: ts() };
    ref("pedidos").push(pedido).catch((e) => avisarErro(e, "o pedido"));
    if (tipo === "agiu") pedidoFeito = { ficha: ficha, ciclo: combate.ciclo };
    return true;
  };

  function tratarPedido(snap) {
    const p = snap.val() || {};
    snap.ref.remove().catch(() => {});
    const est = G.estado(), cb = est.combate;
    if (!cb.ativo || (p.ciclo && p.ciclo !== cb.ciclo) || est.grupo.indexOf(p.ficha) < 0) return;
    const m = G.membro(p.ficha);
    if (!m) return;
    const chave = "p:" + p.ficha, cc = G.cc(chave);
    if (p.tipo === "agiu") {
      if (cc.agiu || cc.participa === false) return;
      G.acoes.agiu({ dataset: { k: chave } });
      EG.toast("<b>" + esc(G.nome(m)) + "</b> terminou o turno.");
    } else if (p.tipo === "ultimate") {
      if (cc.ultimate) return;
      cc.ultimate = true;
      EG.toast("<b>" + esc(G.nome(m)) + "</b> usou a Ultimate.");
    } else return;
    G.salvar();
    G.redesenhar();
  }

  // ---------------------------------------------------------------------------
  // Rolagens: todo mundo vê as de todo mundo
  // ---------------------------------------------------------------------------
  const corta = (s, n) => String(s == null ? "" : s).slice(0, n);

  EG.aoRolar = function (r) {
    if (!conectada() || (L.papel === "mestre" && L.escondido)) return;
    // A Área do Mestre de quem é jogador é a mesa dele, não esta: o que ele rola lá não vai.
    if (L.papel === "jogador" && EG.rotaAtual().tela === "mestre") return;
    const quem = L.papel === "mestre" ? "Mestre" : (F.P && F.P.nome) || nomeDoUsuario();
    const d = { uid: usuario.uid, quem: corta(quem, 80), rotulo: corta(r.rotulo, 160), expr: corta(r.expr, 32),
      total: Number(r.total) || 0, mod: Number(r.mod) || 0, em: ts() };
    if (r.natural != null) d.natural = r.natural;
    if (r.descartado != null) d.descartado = r.descartado;
    if (Array.isArray(r.dados) && JSON.stringify(r.dados).length <= 200) d.dados = JSON.stringify(r.dados);
    if (r.nota) d.nota = String(r.nota);
    if (r.fontes) d.fontes = corta(r.fontes, 160);
    ref("rolagens").push(d).catch(() => {});
  };

  // As rolagens que já entraram no histórico deste aparelho. Reconectar recarrega as últimas
  // 20 da mesa, e sem isto cada queda de conexão repetia todas elas no histórico.
  const rolagensVistas = new Set();

  function ouvirRolagens() {
    const q = ref("rolagens").orderByKey().limitToLast(20);
    let carregou = false;
    ouvir(q, "child_added", (s) => {
      const r = s.val() || {};
      if (!usuario || r.uid === usuario.uid) return;          // a própria já apareceu aqui
      const chave = L.mesa + "/" + s.key;
      if (rolagensVistas.has(chave)) return;
      rolagensVistas.add(chave);
      let dados = null;
      try { dados = r.dados ? JSON.parse(r.dados) : null; } catch (_) { dados = null; }
      EG.mostrarRolagem({ rotulo: r.rotulo, expr: r.expr, total: r.total, natural: r.natural,
        descartado: r.descartado, dados: Array.isArray(dados) ? dados : null, mod: r.mod, nota: r.nota,
        fontes: r.fontes }, r.quem || "Alguém", { aviso: carregou });
    });
    q.once("value", () => { carregou = true; }, () => {});
  }

  /** O Mestre guarda só as últimas rolagens: a mesa não precisa do histórico da campanha. */
  function limparRolagensVelhas() {
    ref("rolagens").once("value").then((s) => {
      const chaves = Object.keys(s.val() || {}).sort();
      if (chaves.length <= 60) return;
      const apagar = {};
      for (const k of chaves.slice(0, chaves.length - 50)) apagar[k] = null;
      return ref("rolagens").update(apagar);
    }).catch(() => {});
  }

  // ---------------------------------------------------------------------------
  // Quem está conectado
  // ---------------------------------------------------------------------------
  let presencaRef = null, membros = {}, presentes = {};

  function marcarPresenca() {
    presencaRef = ref("presenca/" + usuario.uid);
    const fn = (s) => {
      if (s.val() !== true || !presencaRef) return;
      presencaRef.onDisconnect().remove();
      presencaRef.set({ nome: nomeDoUsuario().slice(0, 80), papel: L.papel, em: ts() }).catch(() => {});
    };
    ouvir(db.ref(".info/connected"), "value", fn);
  }

  const mestrePresente = () => Object.values(presentes).some((x) => x && x.papel === "mestre");

  // ---------------------------------------------------------------------------
  // Redesenhar sem atropelar quem está digitando
  // ---------------------------------------------------------------------------
  // A tela inteira se refaz a cada mudança, e refazer embaixo de quem está digitando perde o
  // número que ainda não foi gravado e quebra o acento em composição. Então a mudança de
  // fora espera: a ficha e os dados já estão certos, só o desenho fica para quando a pessoa
  // sair do campo (ou fechar o menu Mais).
  let redesenhoPendente = false, compondo = false;
  document.addEventListener("compositionstart", () => { compondo = true; }, true);
  document.addEventListener("compositionend", () => { compondo = false; }, true);

  function ocupado() {
    if (compondo || document.querySelector("details.menu[open]")) return true;
    const a = document.activeElement, app = document.getElementById("app");
    if (!a || !app || !app.contains(a)) return false;
    if (a.tagName === "TEXTAREA" || a.tagName === "SELECT") return true;
    return a.tagName === "INPUT" && !/^(checkbox|radio|button|submit|file|range|color)$/i.test(a.type);
  }

  function redesenhar() {
    if (EG.rotaAtual().tela === "regras" || !document.body.dataset.tela) return;
    if (ocupado()) { redesenhoPendente = true; return; }
    redesenhoPendente = false;
    EG.redesenharTela();
  }

  // Saiu do campo: o redesenho que esperava acontece quando o foco não estiver em campo
  // nenhum. Indo direto de um campo para outro, ele continua esperando — redesenhar ali
  // recriaria o campo novo no instante em que a pessoa começa a digitar nele.
  const talvezRedesenhar = () => setTimeout(() => { if (redesenhoPendente && !ocupado()) redesenhar(); }, 60);
  document.addEventListener("focusout", talvezRedesenhar);
  document.addEventListener("toggle", (ev) => {
    if (ev.target && ev.target.classList && ev.target.classList.contains("menu") && !ev.target.open) talvezRedesenhar();
  }, true);

  function aposMudarFichas(redesenha) {
    if (L.papel === "mestre") agendarCombate();
    if (redesenha !== false) redesenhar();
  }

  // ---------------------------------------------------------------------------
  // A Área do Mestre de quem é jogador numa mesa
  //
  // Ela continua aberta: é a mesa *deste navegador*, para a campanha que a pessoa mestrar um
  // dia. Nada da mesa do Mestre de lá chega aqui — inimigos, encontros, NPCs e notas nunca
  // saem do navegador de quem mestra, e as regras do banco não deixam jogador ler o que é do
  // Mestre. O que ela tem em comum com a mesa online são as fichas desta pessoa que estão
  // nela: mexer nelas aqui é mexer na ficha, igual à aba Jogar.
  // ---------------------------------------------------------------------------
  N.ehJogador = () => configurada() && !!L.mesa && L.papel === "jogador";

  /** A aba fica para todo mundo. (Até a versão anterior, ela sumia para os jogadores.) */
  function mostrarAbaDoMestre() {
    const aba = document.querySelector("[data-aba='mestre']");
    if (aba) aba.hidden = false;
  }

  /** A faixa no topo da Área do Mestre de quem está como jogador numa mesa online. */
  N.faixaMestreDoJogador = function () {
    if (!N.ehJogador()) return "";
    return "<p class='faixa-mesa'>" + pontoOnline(online) + " Você está na mesa online <b>" + esc(L.nome_mesa) +
      "</b> como <b>jogador</b>. Esta Área do Mestre é <b>sua</b>, só deste navegador: nela não aparece nada da " +
      "campanha do Mestre de lá, e o que você fizer aqui não vai para ele — só as suas fichas que estão na mesa " +
      "continuam sincronizadas. Para mestrar a sua própria mesa online, veja <b>Mesa online</b> no Painel.</p>";
  };

  // ---------------------------------------------------------------------------
  // Pedaços de tela
  // ---------------------------------------------------------------------------
  const botao = (acao, texto, o) => {
    o = o || {};
    return "<button type='button' class='botao" + (o.classe ? " " + o.classe : "") + "' data-mo='" + acao + "'" +
      Object.entries(o.dados || {}).map(([k, v]) => " data-" + k + "='" + esc(v) + "'").join("") +
      (o.titulo ? " title='" + esc(o.titulo) + "'" : "") + (o.desabilitado ? " disabled" : "") + ">" + texto + "</button>";
  };

  const pontoOnline = (sim, rotulo) => "<span class='ponto-online" + (sim ? " sim" : "") + "' role='img' aria-label='" +
    esc(rotulo || (sim ? "conectado" : "desconectado")) + "'></span>";

  /**
   * Enquanto o Firebase carrega, quem já está numa mesa vê "conectando"; quem não está vê
   * logo o botão de entrar (o clique espera o carregamento, se precisar).
   */
  function linhaDeEstado() {
    if (fase === "erro") return "<p class='ajuda ruim'>" + esc(motivo) + "</p>" +
      "<div class='botoes'>" + botao("tentar", "Tentar de novo", { classe: "pequeno" }) + "</div>";
    if (fase === "conectando" || ((fase === "parada" || fase === "carregando") && L.mesa)) {
      return "<p class='ajuda'>Conectando à mesa online…</p>";
    }
    return "";
  }

  /** O cartão do Painel do Mestre. */
  N.cartaoMestre = function () {
    const titulo = "Mesa online";
    if (configurada() && fase === "parada") iniciar();
    if (!configurada()) {
      return "<section class='cartao mesa-online-cartao'><header class='cartao-topo'><h2>" + titulo + "</h2></header>" +
        "<p class='ajuda'>Ainda não está ligada neste site. Com ela, as fichas, o PH, o combate e as rolagens " +
        "do grupo aparecem ao vivo no aparelho de cada um. Para ligar (uma vez só, uns 10 minutos), siga " +
        "<b>Mesa online</b> no arquivo <code>site/LEIA-ME.md</code> do repositório.</p></section>";
    }
    let corpo = linhaDeEstado();
    if (!corpo && !usuario) {
      corpo = "<p class='ajuda'>Com a mesa online, cada jogador vê a própria ficha mudar na hora — o dano que você " +
        "aplica aqui aparece no celular dele —, o PH do grupo é um só, e o combate e as rolagens são da mesa toda.</p>" +
        "<div class='botoes'>" + botao("entrar", "Entrar com Google", { classe: "primario" }) + "</div>";
    } else if (!corpo && L.mesa && L.papel === "jogador") {
      const minhas = Object.entries(mesasDoUsuario).filter(([, papel]) => papel === "mestre");
      corpo = "<p>" + pontoOnline(online) + " Este aparelho está na mesa <b>" + esc(L.nome_mesa) + "</b> como <b>jogador</b>.</p>" +
        "<p class='ajuda'>Um aparelho fica numa mesa online por vez. Para criar e mestrar a sua, saia da mesa de jogador " +
        "aqui: as fichas continuam salvas neste aparelho e na mesa, e você volta para ela pelo convite ou pela tela " +
        "<a href='#mesa'>Mesa online</a>.</p>" +
        (minhas.length ? "<p class='ajuda'>Mesas que você mestra: " + minhas.map(([id]) =>
          botao("conectar", "Abrir a mesa " + esc(id.slice(-6)), { classe: "pequeno", dados: { mesa: id } })).join(" ") + "</p>" : "") +
        "<div class='botoes'>" + botao("soltar", "Sair da mesa de jogador para mestrar", { classe: "pequeno",
          titulo: "As fichas ficam aqui e na mesa; depois é só criar a sua mesa neste cartão" }) + "</div>";
    } else if (!corpo && !(L.mesa && L.papel === "mestre" && fase === "conectada")) {
      const outras = Object.entries(mesasDoUsuario).filter(([, papel]) => papel === "mestre");
      corpo = "<p class='ajuda'>Conta: <b>" + esc(nomeDoUsuario()) + "</b>. Crie a mesa e mande o convite para o grupo.</p>" +
        "<div class='linha'><div class='campo'><span class='rotulo'>Nome da mesa</span>" +
        "<input type='text' id='mo-nome-mesa' maxlength='80' value='" + esc(G.estado().campanha.nome || "") +
        "' placeholder='O Lacre do Poço Sete' aria-label='Nome da mesa'></div>" +
        botao("criar", "Criar mesa online", { classe: "primario" }) + "</div>" +
        (outras.length ? "<p class='ajuda'>Ou volte para uma mesa sua: " + outras.map(([id]) =>
          botao("conectar", "Abrir a mesa " + esc(id.slice(-6)), { classe: "pequeno", dados: { mesa: id } })).join(" ") + "</p>" : "") +
        "<div class='botoes'>" + botao("sair", "Sair da conta", { classe: "pequeno" }) + "</div>";
    } else if (!corpo) {
      lerConvite();
      const link = linkDoConvite();
      const lista = Object.entries(membros).map(([uid, mb]) => {
        const fichas = Object.keys((mb && mb.fichas) || {}).map((id) => {
          const p = EG.Armazem.todas()[id];
          return "<span class='etiqueta'>" + esc((p && p.nome) || "ficha chegando…") + "</span> " +
            botao("tirar", "Tirar da mesa", { classe: "pequeno perigo", dados: { ficha: id },
              titulo: "A ficha sai da mesa e do grupo. A cópia do jogador fica no aparelho dele." });
        }).join(" ");
        return "<li>" + pontoOnline(!!presentes[uid]) + " <b>" + esc((mb && mb.nome) || "Jogador") + "</b> " +
          (fichas || "<span class='suave'>ainda sem ficha na mesa</span>") + "</li>";
      }).join("");
      corpo = "<p>" + pontoOnline(online) + " <b>" + esc(L.nome_mesa) + "</b> <span class='suave'>· você é o Mestre · " +
        esc(nomeDoUsuario()) + "</span></p>" +
        (online ? "" : "<p class='ajuda ruim'>Sem conexão agora: o que mudar aqui vai quando a internet voltar.</p>") +
        "<div class='campo'><span class='rotulo'>Convite</span>" +
        "<div class='linha convite'><input type='text' id='mo-convite' readonly value='" + esc(link || "carregando…") +
        "' aria-label='Link do convite'>" + botao("copiar", "Copiar", { classe: "pequeno primario", desabilitado: !link }) +
        "</div><span class='ajuda'>Mande no grupo. Quem abrir entra com a conta Google e traz a própria ficha.</span></div>" +
        "<h3>Na mesa</h3>" + (lista ? "<ul class='lista-mesa'>" + lista + "</ul>"
          : "<p class='ajuda'>Ninguém entrou ainda.</p>") +
        "<label class='marca'><input type='checkbox' data-mo-op='barras'" + (L.barras ? " checked" : "") +
        "> <span>Jogadores veem as barras de PV e Tenacidade dos inimigos (sem os números)</span></label>" +
        "<label class='marca'><input type='checkbox' data-mo-op='escondido'" + (L.escondido ? " checked" : "") +
        "> <span>Rolar escondido: as suas rolagens não aparecem para os jogadores</span></label>" +
        "<div class='botoes compactos'>" + botao("gerar-convite", "Gerar outro convite", { classe: "pequeno",
          titulo: "O link antigo para de funcionar; quem já entrou continua" }) +
        botao("soltar", "Desconectar este aparelho", { classe: "pequeno" }) + "</div>";
    }
    return "<section class='cartao mesa-online-cartao'><header class='cartao-topo'><h2>" + titulo + "</h2></header>" +
      corpo + "</section>";
  };

  /** A faixa da aba Jogar: a mesa e, em combate, a Fila. */
  N.faixaJogador = function (p) {
    if (!configurada() || !p || !L.mesa) return "";
    if (L.papel === "mestre") {
      return L.ligadas[p.id] ? "<p class='faixa-mesa'>" + pontoOnline(online) + " Esta é a ficha de um jogador da sua mesa " +
        "<b>" + esc(L.nome_mesa) + "</b>: o que mudar aqui vai para ele na hora.</p>" : "";
    }
    if (fase !== "conectada") {
      return "<p class='faixa-mesa'>" + pontoOnline(false) + " Mesa online <b>" + esc(L.nome_mesa) + "</b>: " +
        (fase === "sem-login" ? "entre de novo para sincronizar. " + botao("entrar", "Entrar com Google", { classe: "pequeno" })
          : fase === "erro" ? esc(motivo) + " " + botao("tentar", "Tentar de novo", { classe: "pequeno" }) : "conectando…") + "</p>";
    }
    if (!L.ligadas[p.id]) {
      return "<p class='faixa-mesa'>" + pontoOnline(online) + " Esta ficha não está na mesa <b>" + esc(L.nome_mesa) + "</b>. " +
        botao("levar", "Levar para a mesa", { classe: "pequeno primario", dados: { ficha: p.id } }) + "</p>";
    }
    return "<p class='faixa-mesa'>" + pontoOnline(online) + " Mesa online <b>" + esc(L.nome_mesa) + "</b>" +
      (online ? "" : " · <span class='ruim'>sem conexão: o que mudar vai quando a internet voltar</span>") +
      " · <a href='#mesa'>detalhes</a></p>" + cartaoCombate(p);
  };

  // O retrato do combate vem de outro aparelho: todo número passa por num() e todo texto
  // por esc() antes de virar HTML, mesmo sendo o Mestre o único que pode gravá-lo.
  const num = (v) => (Number.isFinite(Number(v)) ? Math.round(Number(v)) : 0);
  const classeDe = (s) => String(s || "").toLowerCase().replace(/[^a-z]/g, "");

  function cartaoCombate(p) {
    const cb = combate;
    if (!cb || !cb.ativo || !Array.isArray(cb.fila)) return "";
    const minha = "p:" + p.id;
    const agora = cb.fila.find((x) => x.agora);
    const eu = cb.fila.find((x) => x.k === minha);
    const esperando = !!(pedidoFeito && pedidoFeito.ficha === p.id && pedidoFeito.ciclo === cb.ciclo && eu && !eu.agiu);
    const minhaVez = agora && agora.k === minha && !esperando;
    let topo = "";
    if (minhaVez) {
      topo = "<div class='sua-vez'><b>É a sua vez!</b>" + botao("agiu", "Terminei meu turno",
        { classe: "primario", dados: { ficha: p.id }, titulo: "Avisa o Mestre, e a Fila anda" }) + "</div>";
    } else if (esperando) {
      topo = "<p class='ajuda'>Turno encerrado: esperando o Mestre…</p>";
    } else if (agora) {
      topo = "<p>Agindo agora: <b>" + esc(agora.n) + "</b>" + (eu && eu.agiu ? " · <span class='suave'>você já agiu neste Ciclo</span>" : "") + "</p>";
    }
    if (!mestrePresente()) topo += "<p class='ajuda'>" + pontoOnline(false) + " O Mestre está offline: a Fila volta a andar quando ele voltar.</p>";
    const etiq = (t, cls) => " <span class='etiqueta" + (cls ? " " + cls : "") + "'>" + t + "</span>";
    const casas = cb.fila.map((x) => {
      const tipo = x.t === "inimigo" ? etiq(esc(x.tipo || "Inimigo"), "tipo-" + (classeDe(x.tipo) || "comum"))
        : x.t === "pj" ? (x.k === minha ? etiq("você", "pronta") : etiq("PJ", "pj"))
        : x.t === "memo" || x.t === "npcmemo" ? etiq("Memoespírito") : etiq("NPC" + (x.tipo ? " · " + esc(x.tipo) : ""), "npc");
      let vitais = "";
      if (x.aliado && num(x.pvm) > 0) {
        vitais += "<div class='casa-vital'><span class='rotulo'>PV</span><b>" + num(x.pv) + "<small>/" + num(x.pvm) + "</small></b>" +
          barra("barra-pv", pct(num(x.pv), num(x.pvm)), "PV de " + x.n) + "</div>";
      }
      if (x.aliado && x.en != null) {
        const pronta = num(x.uc) > 0 && num(x.en) >= num(x.uc);
        vitais += "<div class='casa-vital'><span class='rotulo'>Energia</span><b>" + num(x.en) + "<small>/100</small>" +
          (pronta ? etiq("Ultimate pronta", "pronta") : "") + "</b>" + barra("barra-energia", num(x.en), "Energia de " + x.n) + "</div>";
      }
      if (!x.aliado && x.pct != null) {
        vitais += "<div class='casa-vital'><span class='rotulo'>PV</span>" + barra("barra-pv", num(x.pct), "PV de " + x.n) + "</div>";
        if (x.tpct != null) vitais += "<div class='casa-vital'><span class='rotulo'>Tenacidade</span>" +
          barra("barra-tenacidade", num(x.tpct), "Tenacidade de " + x.n, num(x.tpct) === 0) + "</div>";
      }
      const conds = (Array.isArray(x.cond) ? x.cond : []).map((c) => "<span class='etiqueta'>" + esc(c && c.n) +
        (c && c.t != null ? " " + num(c.t) + "t" : "") + (c && c.a ? " ×" + num(c.a) : "") + "</span>").join(" ");
      const caiu = x.caiu ? etiq(x.t === "pj" || x.t === "npc"
        ? "Morrendo" + (x.mo ? " " + num(x.mo.s) + "✓ " + num(x.mo.f) + "✗" : "")
        : x.t === "inimigo" ? "derrotado" + (x.pula ? " · pula a vez" : "") : "caiu", "ruim") : "";
      const atr = num(x.atr), ava = num(x.ava);
      return "<li class='fila-casa" + (x.agora ? " agora" : "") + (x.agiu ? " agiu" : "") + (x.caiu ? " caiu" : "") +
        (x.caiu && x.t !== "pj" && x.t !== "npc" ? " fora" : "") + (x.pula ? " pulado" : "") +
        (x.qb ? " quebrado" : "") + (x.k === minha ? " minha" : "") + "'>" +
        "<div class='casa-num'>" + num(x.c) + (x.agora ? "<span class='sr-only'> (agindo agora)</span>" : "") + "</div>" +
        "<div class='casa-quem'><div><b>" + esc(x.n) + "</b>" + tipo +
        (x.agora ? etiq("agindo agora", "pronta") : "") + (x.agiu ? etiq("já agiu") : "") +
        (x.ult ? etiq("Ultimate usada") : "") + (x.qb ? etiq("Quebrado", "ruim") : "") + caiu + "</div>" +
        ((atr || ava || x.sur) ? "<div class='suave'>" + [atr ? "atrasado " + atr + (atr > 1 ? " casas" : " casa") : "",
          ava ? "avançado " + ava : "", x.sur ? "Surpreso" : ""].filter(Boolean).join(" · ") + "</div>" : "") +
        (conds ? "<div class='casa-cond'>" + conds + "</div>" : "") + "</div>" +
        "<div class='casa-vitais'>" + vitais + "</div></li>";
    }).join("");
    return "<section class='cartao combate-jogador'><header class='cartao-topo'><h2>Combate" +
      (cb.nome ? " · " + esc(cb.nome) : "") + "</h2><b class='destaque'>Ciclo " + (num(cb.ciclo) || 1) + "</b></header>" +
      topo + "<ol class='fila'>" + casas + "</ol></section>";
  }

  function barra(classe, valor, rotulo, zerada) {
    const v = Math.max(0, Math.min(100, Math.round(Number(valor) || 0)));
    return "<div class='" + classe + "' role='progressbar' aria-label='" + esc(rotulo) + "' aria-valuemin='0' " +
      "aria-valuemax='100' aria-valuenow='" + v + "'><span style='width:" + v + "%'" +
      (classe === "barra-pv" ? " class='" + (v <= 33 ? "baixo" : v <= 50 ? "medio" : "") + "'" : zerada ? " class='zerada'" : "") +
      "></span></div>";
  }

  N.ultimateUsada = (id) => {
    const eu = combate && combate.ativo && Array.isArray(combate.fila) ? combate.fila.find((x) => x.k === "p:" + id) : null;
    return !!(eu && eu.ult);
  };

  // ---------------------------------------------------------------------------
  // Telas: #mesa (a mesa deste aparelho) e #entrar/<mesa>/<convite>
  // ---------------------------------------------------------------------------
  function soltarFicha() { F.P = null; F.R = null; F.aoSalvar = null; }

  function telaMesa() {
    soltarFicha();
    if (configurada() && fase === "parada") iniciar();
    const app = document.getElementById("app");
    let corpo;
    if (!configurada()) {
      corpo = "<p>A mesa online ainda não está ligada neste site. Quem cuida do site liga uma vez só, seguindo " +
        "<b>Mesa online</b> em <code>site/LEIA-ME.md</code>.</p>";
    } else if (linhaDeEstado()) {
      corpo = linhaDeEstado();
    } else if (!usuario) {
      corpo = "<p>Entre com a sua conta Google para usar a mesa online. Para entrar numa mesa, abra o link de " +
        "convite que o Mestre mandar.</p><div class='botoes'>" + botao("entrar", "Entrar com Google", { classe: "primario" }) + "</div>";
    } else if (!L.mesa || fase !== "conectada") {
      const ids = Object.keys(mesasDoUsuario);
      corpo = "<p>Conta: <b>" + esc(nomeDoUsuario()) + "</b>.</p>" +
        (ids.length ? "<p>Suas mesas: " + ids.map((id) => botao("conectar", (mesasDoUsuario[id] === "mestre" ? "Mestre · " : "") +
          "Abrir a mesa " + esc(id.slice(-6)), { classe: "pequeno", dados: { mesa: id } })).join(" ") + "</p>"
          : "<p class='ajuda'>Você ainda não está em nenhuma mesa. Peça o link de convite ao Mestre e abra neste aparelho.</p>") +
        "<div class='botoes'>" + botao("sair", "Sair da conta") + "</div>";
    } else if (L.papel === "mestre") {
      corpo = "<p>" + pontoOnline(online) + " Você é o Mestre da mesa <b>" + esc(L.nome_mesa) + "</b>. O convite e a lista " +
        "de quem está na mesa ficam no <a href='#mestre'>Painel da Área do Mestre</a>.</p>" +
        "<div class='botoes'>" + botao("sair", "Sair da conta") + "</div>";
    } else {
      const mapa = EG.Armazem.todas();
      const ligadas = Object.keys(L.ligadas).filter((id) => mapa[id]);
      const fora = Object.values(mapa).filter((p) => !L.ligadas[p.id]);
      corpo = "<p>" + pontoOnline(online) + " Mesa <b>" + esc(L.nome_mesa) + "</b> · " + esc(nomeDoUsuario()) +
        (online ? "" : " · <span class='ruim'>sem conexão agora</span>") + "</p>" +
        "<h3>Suas fichas na mesa</h3>" + (ligadas.length ? "<ul class='lista-mesa'>" + ligadas.map((id) =>
          "<li><b>" + esc(mapa[id].nome || "Personagem sem nome") + "</b> " +
          botao("abrir", "Abrir", { classe: "pequeno", dados: { ficha: id } }) + " " +
          botao("tirar", "Tirar da mesa", { classe: "pequeno perigo", dados: { ficha: id },
            titulo: "A ficha sai da mesa; a cópia deste aparelho fica" }) + "</li>").join("") + "</ul>"
          : "<p class='ajuda'>Nenhuma ainda. Leve uma ficha deste aparelho para a mesa:</p>") +
        (fora.length ? "<h3>Fichas deste aparelho fora da mesa</h3><ul class='lista-mesa'>" + fora.map((p) =>
          "<li><b>" + esc(p.nome || "Personagem sem nome") + "</b> " +
          botao("levar", "Levar para a mesa", { classe: "pequeno primario", dados: { ficha: p.id } }) + "</li>").join("") + "</ul>"
          : (!ligadas.length ? "<p class='ajuda'>Este aparelho ainda não tem ficha. <a href='#editar'>Crie a sua</a> e volte aqui.</p>" : "")) +
        "<p class='ajuda'>O Mestre vê e pode mexer nas fichas que estão na mesa; os outros jogadores não. " +
        "Do grupo, você vê o PH e, em combate, a Fila de Ação.</p>" +
        "<div class='botoes'>" + botao("soltar", "Sair da mesa neste aparelho", { titulo: "As fichas ficam aqui e na mesa" }) +
        botao("sair", "Sair da conta") + "</div>";
    }
    app.innerHTML = "<section class='cartao mesa-online-cartao tela-mesa'><header class='cartao-topo'><h2>Mesa online</h2>" +
      "<a href='#jogar'>Voltar para a ficha</a></header>" + corpo + "</section>";
  }

  function telaEntrar(r) {
    soltarFicha();
    const mesa = r.partes[0] || "", codigo = r.partes[1] || "";
    if (configurada() && fase === "parada") iniciar();
    const app = document.getElementById("app");
    let corpo;
    if (!configurada()) corpo = "<p>Esta cópia do site não tem a mesa online ligada.</p>";
    else if (!mesa || !codigo) corpo = "<p>Este link de convite está incompleto. Peça outro ao Mestre.</p>";
    else if (linhaDeEstado()) corpo = linhaDeEstado();
    else if (!usuario) {
      corpo = "<p>Você foi convidado para uma mesa online de <b>Explorando Galáxias</b>. Entre com a sua conta Google " +
        "para aceitar: a sua ficha vai aparecer ao vivo para o Mestre, e o combate e as rolagens da mesa, para você.</p>" +
        "<div class='botoes'>" + botao("entrar", "Entrar com Google", { classe: "primario" }) + "</div>";
    } else if (L.mesa === mesa && fase === "conectada") {
      corpo = "<p>Você já está nesta mesa (<b>" + esc(L.nome_mesa) + "</b>).</p><div class='botoes'>" +
        "<a class='botao primario' href='" + (L.papel === "mestre" ? "#mestre" : "#mesa") + "'>Continuar</a></div>";
    } else {
      corpo = "<p>Entrar na mesa como <b>" + esc(nomeDoUsuario()) + "</b>?</p>" +
        (L.mesa ? "<p class='ajuda'>Este aparelho sai da mesa <b>" + esc(L.nome_mesa) + "</b>. As fichas continuam salvas.</p>" : "") +
        "<div class='botoes'>" + botao("aceitar", "Entrar na mesa", { classe: "primario", dados: { mesa: mesa, codigo: codigo } }) +
        botao("sair", "Usar outra conta") + "</div>";
    }
    app.innerHTML = "<section class='cartao mesa-online-cartao tela-mesa'><header class='cartao-topo'><h2>Convite para a mesa</h2>" +
      "</header>" + corpo + "</section>";
  }

  EG.registrarTela("mesa", telaMesa);
  EG.registrarTela("entrar", telaEntrar);

  // ---------------------------------------------------------------------------
  // Botões (data-mo) e opções (data-mo-op)
  // ---------------------------------------------------------------------------
  const acoes = {
    entrar: () => entrar(),
    sair: () => sair(),
    tentar: () => { fase = "parada"; return iniciar().then(() => usuario && aoMudarUsuario(usuario)); },
    criar: () => {
      const el = document.getElementById("mo-nome-mesa");
      return criarMesa(el ? el.value : "");
    },
    conectar: (b) => conectar(b.dataset.mesa),
    aceitar: (b) => entrarNaMesa(b.dataset.mesa, b.dataset.codigo),
    soltar: () => {
      if (!confirm("Desconectar este aparelho da mesa " + L.nome_mesa + "? As fichas continuam salvas aqui e na mesa; " +
        "para voltar, abra o convite de novo ou a tela Mesa online.")) return;
      pararTudo();
      soltarMesa();
    },
    levar: (b) => levarFicha(b.dataset.ficha),
    tirar: (b) => {
      const p = EG.Armazem.todas()[b.dataset.ficha];
      if (!confirm("Tirar " + ((p && p.nome) || "esta ficha") + " da mesa? A cópia de cada aparelho continua salva.")) return;
      return tirarFicha(b.dataset.ficha);
    },
    abrir: (b) => { EG.Armazem.definirAtual(b.dataset.ficha); location.hash = "#jogar"; },
    agiu: (b) => {
      if (N.pedir("agiu", b.dataset.ficha)) EG.toast("Avisei o Mestre que o seu turno acabou.");
      redesenhar();
    },
    copiar: () => {
      const link = linkDoConvite(), el = document.getElementById("mo-convite");
      const ok = () => EG.toast("Convite copiado. Cole no grupo.");
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(link).then(ok, () => { if (el) el.select(); });
      else if (el) { el.select(); document.execCommand("copy"); ok(); }
    },
    "gerar-convite": () => gerarConvite(),
  };

  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-mo]");
    if (!b || !acoes[b.dataset.mo]) return;
    ev.preventDefault();
    const r = acoes[b.dataset.mo](b);
    if (r && typeof r.then === "function") r.then(() => redesenhar(), () => redesenhar());
    else redesenhar();
  });

  document.addEventListener("change", (ev) => {
    const op = ev.target && ev.target.dataset && ev.target.dataset.moOp;
    if (!op) return;
    L[op] = !!ev.target.checked;
    gravarLocal();
    if (op === "barras") { combateEnviado = ""; agendarCombate(); }
  });

  // A barra de personagens ganha "Mesa online…" no menu Mais.
  (F.acoes = F.acoes || {})["mesa-online"] = () => { location.hash = "#mesa"; return false; };

  // ---------------------------------------------------------------------------
  // Partida: só liga o Firebase se este aparelho já está numa mesa, ou se a pessoa
  // chegou por um convite ou pela tela da mesa. Para os outros, nada carrega.
  // ---------------------------------------------------------------------------
  mostrarAbaDoMestre();
  if (configurada()) {
    const t = EG.rotaAtual().tela;
    if (L.mesa || t === "entrar" || t === "mesa") iniciar();
  }
})();
