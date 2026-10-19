/*
 * ficha-jogar.js — Tela "Jogar": o que você usa na mesa. PV com dano e cura já
 * descontando RD e PV temporários, Energia, PH, ataques prontos para rolar, Testes,
 * Bênçãos com usos, condições, Memoespírito e inventário.
 */
(function () {
  "use strict";

  const EG = window.EG;
  const { esc, sinal, botaoRolar } = EG;
  const M = window.Motor;
  const C = () => window.CATALOGO;
  const F = EG.Ficha;
  const H = F.H;
  const link = (n, t, r) => EG.Regras.link(n, t, r);

  // ---------------------------------------------------------------------------
  // Frequências: o que dá para marcar como "usado" e quando volta
  // ---------------------------------------------------------------------------
  function recarga(texto) {
    const t = texto.toLowerCase();
    if (/por alvo|turno|ciclo/.test(t)) return null;          // muda rápido demais para marcar
    if (/descanso curto/.test(t)) return "curto";
    if (/descanso longo|dia/.test(t)) return "longo";
    if (/combate|cena/.test(t)) return "combate";
    if (/sessão/.test(t)) return "sessao";
    return null;
  }
  const quantasVezes = (texto) => (/duas|2 vezes/i.test(texto) ? 2 : 1);

  /** Usos marcáveis: [{chave, rotulo, recarga}] das Bênçãos possuídas e do traço ativável da Raça. */
  function usosMarcaveis() {
    const usos = [];
    const chave = (...partes) => partes.join(":").replace(/\./g, "");
    for (const nome of F.bencaosPossuidas()) {
      const b = F.bencaoInfo(nome);
      if (!b) continue;
      b.frequencia.split(" · ").forEach((fr) => {
        const r = recarga(fr);
        if (!r) return;
        for (let i = 0; i < quantasVezes(fr); i++) usos.push({ chave: chave("b", nome, fr, i), dono: nome, rotulo: fr, recarga: r });
      });
    }
    const traco = tracoAtivavel();
    if (traco && F.P.raca !== "Humano") {
      const r = recarga(traco.desc) || "combate";
      for (let i = 0; i < quantasVezes(traco.desc); i++) usos.push({ chave: chave("r", traco.nome, i), dono: traco.nome, rotulo: traco.desc.split(",")[0], recarga: r });
    }
    return usos;
  }

  function tracosResumo() {
    const r = F.racaInfo();
    if (!r) return [];
    return r.tracos.split(" · ").map((t) => {
      const m = t.match(/^(.+?) \((ativável|passivo): (.+)\)$/);
      return m ? { nome: m[1], tipo: m[2], desc: m[3] } : { nome: t, tipo: "", desc: "" };
    });
  }
  const tracoAtivavel = () => tracosResumo().find((t) => t.tipo === "ativável");

  // ---------------------------------------------------------------------------
  // Ações dos botões
  // ---------------------------------------------------------------------------
  const A = (F.acoes = F.acoes || {});
  const J = () => F.P.jogo;
  const pvAtual = () => (J().pv == null ? F.R.pv_max : Math.min(J().pv, F.R.pv_max));
  const lerValor = () => {
    const el = document.getElementById("valor-pv");
    const n = el ? Math.floor(Number(el.value)) : 0;
    return Number.isFinite(n) && n > 0 ? n : 0;
  };

  /** Muda a Energia por uma fonte de 17.2 e avisa. Os limites por Ciclo valem aqui também. */
  const energia = (fonte, o) => {
    const r = F.mudarEnergia(F.P, F.R, fonte, o);
    if (r) EG.toast(r.msg, r.bloqueado ? "erro" : "");
    return r;
  };

  A["sofrer-dano"] = () => {
    const bruto = lerValor();
    if (!bruto) { EG.toast("Digite quanto de dano você sofreu.", "erro"); return; }
    const continuo = document.getElementById("dano-continuo").checked;
    const j = J();
    if (pvAtual() === 0) {
      j.morrendo.f += 1;
      EG.toast("Dano enquanto Morrendo: <b>+1 falha</b> (2 se for crítico ou Habilidade de Nível 5+; ajuste nas caixas).");
      return;
    }
    const depoisRd = Math.max(1, bruto - (continuo ? 0 : F.R.rd));     // 23.1: RD, mínimo 1
    const absorvido = Math.min(j.temp || 0, depoisRd);                // 23.3: temporário absorve depois da RD
    j.temp = (j.temp || 0) - absorvido;
    const perde = depoisRd - absorvido;
    j.pv = Math.max(0, pvAtual() - perde);
    let msg = "Dano " + bruto + (continuo ? " (Contínuo, ignora RD)" : F.R.rd ? " − RD " + F.R.rd : "") + " = <b>" + depoisRd + "</b>";
    if (absorvido) msg += " · " + absorvido + " no PV temporário";
    msg += " · PV " + j.pv + "/" + F.R.pv_max;
    if (j.pv === 0) { msg += " · <b>Morrendo!</b>"; j.morrendo = { s: 0, f: 0 }; }
    // 17.2: sofrer dano dá +10 de Energia, 1 vez por Ciclo. Vem junto, sem outro clique.
    const e = F.mudarEnergia(F.P, F.R, "dano");
    msg += e && !e.bloqueado ? "<br>+" + e.aplicado + " de Energia por sofrer dano (1 vez por Ciclo) · " + e.energia + "/100"
      : "<br><span class='suave'>A Energia de sofrer dano já veio neste Ciclo.</span>";
    EG.toast(msg);
  };

  A["curar"] = () => {
    const v = lerValor();
    if (!v) { EG.toast("Digite quanto você cura.", "erro"); return; }
    const j = J(), antes = pvAtual();
    j.pv = Math.min(F.R.pv_max, antes + v);
    if (antes === 0) j.morrendo = { s: 0, f: 0 };
    EG.toast("Curou " + (j.pv - antes) + " · PV " + j.pv + "/" + F.R.pv_max + (antes === 0 ? " · saiu de Morrendo" : ""));
  };

  function recarregar(tipos) {
    const usos = J().usos;
    for (const u of usosMarcaveis()) if (tipos.includes(u.recarga)) delete usos[u.chave];
  }

  A["descanso-curto"] = () => {
    const j = J(), antes = pvAtual();
    j.pv = Math.min(F.R.pv_max, antes + Math.max(0, F.R.descanso_curto));
    if (antes === 0 && j.pv > 0) j.morrendo = { s: 0, f: 0 };
    recarregar(["curto"]);
    if (F.R.memo) j.memo_pv = F.R.memo.pv;
    EG.toast("Descanso Curto: +" + (j.pv - antes) + " PV. Recarregou o que é \"por Descanso Curto\"" + (F.R.memo ? " e reinvocou o Memoespírito." : "."));
  };

  A["descanso-longo"] = () => {
    const j = J();
    j.pv = F.R.pv_max; j.temp = 0; j.condicoes = []; j.morrendo = { s: 0, f: 0 };
    j.esforco = F.R.esforco_max;
    recarregar(["curto", "longo", "combate"]);
    if (F.R.memo) j.memo_pv = F.R.memo.pv;
    EG.toast("Descanso Longo: PV cheios, condições removidas, usos recarregados" + (F.R.esforco_max ? ", Esforço de volta." : "."));
  };

  A["novo-combate"] = () => {
    const j = J();
    j.ph = F.R.ph_inicio;
    j.acumulos = {};
    // Combate novo: os limites de Energia "por Ciclo" e "por combate" começam do zero.
    j.combate_local = (Number(j.combate_local) || 1) + 1;
    j.ciclo_local = 1;
    F.zerarEnergiaDoCombate(j);
    recarregar(["combate"]);
    EG.toast("Novo combate: PH do grupo em " + j.ph + ", acúmulos zerados, usos \"por combate\" e \"por cena\" de volta, " +
      "e a Energia do Ciclo e do combate liberada (17.2).");
  };

  // Os botões de ajuste (−10, +10) da Energia, fora da tabela de fontes.
  A["energia"] = (b) => { energia("ajuste", { valor: Number(b.dataset.v) }); };

  // Uma fonte da tabela de 17.2 (sofrer dano, derrotar, Quebrar, Memoespírito, Corda, Cone).
  A["energia-fonte"] = (b) => { energia(b.dataset.fonte); };

  A["desfazer-energia"] = () => {
    const e = F.desfazerEnergia(F.P);
    if (!e) { EG.toast("Nada para desfazer no registro de Energia.", "erro"); return; }
    const def = F.ENERGIA[e.f] || { rotulo: "Energia" };
    EG.toast("Desfeito: <b>" + esc(e.r || def.rotulo) + "</b> (" + (e.v >= 0 ? "−" + e.v : "+" + -e.v) + " de Energia) · " +
      (J().energia || 0) + "/100");
  };

  // Sem a mesa online, quem conta o Ciclo é o jogador: virar o Ciclo libera o que é 1×/Ciclo.
  A["proximo-ciclo"] = () => {
    const j = J();
    j.ciclo_local = (Number(j.ciclo_local) || 1) + 1;
    EG.toast("<b>Ciclo " + j.ciclo_local + "</b>: sofrer dano, Quebrar e o Cone voltam a dar Energia (1 vez por Ciclo, 17.2).");
  };

  A["ultimate"] = () => {
    const j = J(), custo = F.R.ultimate.custo;
    if ((j.energia || 0) < custo) { EG.toast("Faltam " + (custo - (j.energia || 0)) + " de Energia para a Ultimate.", "erro"); return; }
    F.mudarEnergia(F.P, F.R, "ultimate");
    EG.toast("<b>" + esc(F.P.ultimate.nome || "Ultimate") + "!</b> −" + custo + " de Energia.");
    // Na mesa online, a Fila do Mestre marca a Ultimate do Ciclo (uma por Ciclo, 17.1).
    if (EG.MesaOnline) EG.MesaOnline.pedir("ultimate", F.P.id);
  };

  A["ph"] = (b) => { const j = J(); j.ph = Math.max(0, Math.min(F.R.ph_max, (j.ph || 0) + Number(b.dataset.v))); };

  A["usar-habilidade"] = (b) => {
    const i = Number(b.dataset.i), h = F.P.habilidades[i], out = F.R.habilidades[i], j = J();
    if (out.ph > (j.ph || 0)) { EG.toast("Sem PH suficiente: " + esc(h.nome || "a Habilidade") + " custa " + out.ph + " PH e o grupo tem " + (j.ph || 0) + ".", "erro"); return; }
    j.ph -= out.ph;
    const e = F.mudarEnergia(F.P, F.R, "habilidade");
    EG.toast("<b>" + esc(h.nome || "Habilidade") + "</b>: −" + out.ph + " PH, +" + e.aplicado + " de Energia · " + e.energia + "/100.");
  };

  // O Ataque Básico dá +20 de Energia acertando ou não (17.2); o PH é só do acerto (16.2).
  A["ataque-basico"] = () => {
    const e = F.mudarEnergia(F.P, F.R, "basico");
    EG.toast("Ataque Básico (errou): +" + e.aplicado + " de Energia · " + e.energia + "/100. Errar não corta a Energia; só o 1 natural.");
  };

  A["acertou"] = () => {
    const j = J(), antes = j.ph || 0;
    j.ph = Math.min(F.R.ph_max, antes + F.R.ph_geracao);
    const e = F.mudarEnergia(F.P, F.R, "basico");
    const ph = j.ph - antes;
    EG.toast("Acertou o Ataque Básico: +" + e.aplicado + " de Energia (" + e.energia + "/100) e " +
      (ph ? "<b>+" + ph + " PH</b> para o grupo (" + j.ph + "/" + F.R.ph_max + ")."
        : "o PH do grupo já está no máximo (" + F.R.ph_max + "): não sobe mais."));
  };

  A["acumulo"] = (b) => {
    const j = J(), k = b.dataset.k;
    j.acumulos[k] = Math.max(0, Math.min(Number(b.dataset.max), (j.acumulos[k] || 0) + Number(b.dataset.v)));
  };

  A["morrendo"] = () => {
    const j = J(), R = F.R;
    const r = EG.rolar("d20" + (R.morrendo_bonus >= 0 ? "+" : "") + R.morrendo_bonus,
      { rotulo: "Teste de Morrendo (DT 10)", vantagem: R.morrendo_vantagem, fontes: F.P.raca });
    if (!r) return;
    if (r.natural === 20) { j.pv = 1; j.morrendo = { s: 0, f: 0 }; EG.toast("20 natural: você se levanta com 1 PV!"); return; }
    if (r.natural === 1) j.morrendo.f += 2;
    else if (r.total >= 10) j.morrendo.s += 1;
    else j.morrendo.f += 1;
    if (j.morrendo.s >= 3) { j.pv = 1; j.morrendo = { s: 0, f: 0 }; EG.toast("3 sucessos: você estabiliza com 1 PV."); }
    else if (j.morrendo.f >= 3) EG.toast("3 falhas: o personagem morre.", "erro");
  };

  A["riso"] = () => {
    const r = EG.rolar("1d6", { rotulo: "Tabela do Riso" });
    const linha = C().tabela_do_riso.find((x) => x.d6 === (r && r.total));
    if (linha) EG.toast("<b>" + r.total + "</b> — " + esc(linha.efeito), "rolagem");
  };

  A["add-condicao"] = () => {
    const sel = document.getElementById("nova-condicao");
    if (!sel || !sel.value) return;
    if (!J().condicoes.some((c) => c.nome === sel.value)) J().condicoes.push({ nome: sel.value });
  };
  A["tirar-condicao"] = (b) => { J().condicoes.splice(Number(b.dataset.i), 1); };

  A["invocar"] = () => {
    const j = J();
    if ((j.ph || 0) < 1) { EG.toast("Invocar custa 1 PH e o grupo está sem PH.", "erro"); return; }
    j.ph -= 1; j.memo_ativo = true; j.memo_pv = F.R.memo.pv;
    EG.toast("<b>" + esc(F.nomeDoMemo(F.P).nome) + "</b> em campo: Ação Complementar e −1 PH.");
  };
  A["dispensar"] = () => {
    J().memo_ativo = false;
    EG.toast(esc(F.nomeDoMemo(F.P).nome) + " saiu de campo.");
  };

  // A Técnica Principal com dois acréscimos (Forma Completa): alvo único ou em área, na hora.
  A["memo-modo"] = (b) => { J().memo_modo = b.dataset.v === "area" ? "area" : "unico"; };

  A["memo-evolutivo"] = (b) => {
    const j = J();
    j.memo_evolutivo = b.dataset.v === "0" ? 0 : Math.max(0, Math.min(5, (Number(j.memo_evolutivo) || 0) + Number(b.dataset.v)));
  };

  // O Memoespírito agiu: metade da Energia da ação vai para o dono (17.2 e 11.5).
  A["memo-acao"] = (b) => {
    const j = J(), nm = F.nomeDoMemo(F.P), hab = b.dataset.fonte === "memo_hab";
    const e = F.mudarEnergia(F.P, F.R, hab ? "memo_hab" : "memo_basico",
      { rotulo: nm.nome + (hab ? ": Técnica" : ": Ataque Básico") });
    let extra = "";
    if (b.dataset.tecnica === "1") {
      const atq = F.ataquesDoMemo(F.P, F.R);
      if (atq && atq.tecnica.evolutivo) {
        j.memo_evolutivo = Math.min(5, (Number(j.memo_evolutivo) || 0) + 1);
        extra = " Ataque Evolutivo: o próximo uso tem +" + Math.min(5, j.memo_evolutivo + 1) + " de dano.";
      }
    }
    EG.toast(e.msg + " — metade da ação " + esc(nm.de) + " vai para você." + extra);
  };

  const nomePocao = (x) => (/^Poção/i.test(x.pocao) ? x.pocao : "Poção de Vida " + x.pocao);
  const acharPocao = (nome) => C().pocoes.find((x) => nomePocao(x) === nome);

  A["add-item"] = () => {
    const sel = document.getElementById("novo-item");
    const v = sel ? sel.value : "";
    const cat = C().itens.find((i) => i.item === v) || acharPocao(v);
    F.P.inventario.push({ nome: v && v !== "__outro" ? v : "", qtd: 1, espaco: cat ? cat.espaco : 0 });
  };
  A["tirar-item"] = (b) => { F.P.inventario.splice(Number(b.dataset.i), 1); };
  A["beber"] = (b) => {
    const item = F.P.inventario[Number(b.dataset.i)];
    const pocao = acharPocao(item.nome);
    if (!pocao || !(item.qtd > 0)) return;
    item.qtd -= 1;
    const j = J(), antes = pvAtual();
    j.pv = Math.min(F.R.pv_max, antes + pocao.cura);
    if (antes === 0) j.morrendo = { s: 0, f: 0 };
    EG.toast(esc(nomePocao(pocao)) + ": +" + (j.pv - antes) + " PV (Ação Complementar).");
  };

  // ---------------------------------------------------------------------------
  // Pedaços da tela
  // ---------------------------------------------------------------------------
  const cartao = (titulo, corpo, classe, extra) =>
    "<section class='cartao " + (classe || "") + "'><header class='cartao-topo'><h2>" + titulo + "</h2>" + (extra || "") + "</header>" + corpo + "</section>";
  const num = (rotulo, valor, sub) => "<div class='numero'><span class='rotulo'>" + rotulo + "</span><span class='grande'>" + valor + "</span>" +
    (sub ? "<span class='sub'>" + sub + "</span>" : "") + "</div>";
  const botao = (acao, texto, o) => {
    o = o || {};
    return "<button type='button' class='botao" + (o.classe ? " " + o.classe : "") + "' data-acao='" + acao + "'" +
      Object.entries(o.dados || {}).map(([k, v]) => " data-" + k + "='" + esc(v) + "'").join("") +
      (o.desabilitado ? " disabled" : "") + (o.titulo ? " title='" + esc(o.titulo) + "'" : "") + ">" + texto + "</button>";
  };

  function cabecalho() {
    const p = F.P, R = F.R;
    const partes = [p.raca, p.caminho, "nível " + R.nivel, p.elemento].filter(Boolean);
    const falta = F.pendencias();
    const avisos = R.avisos.filter((a) => !["ESQUIVA_PROIBIDA", "RD_NO_TETO", "SOBRECARGA", "IMOVEL", "BONUS_TEMPORARIO_NO_TETO"].includes(a));
    return "<div class='cabecalho-personagem'><div><h1>" + esc(p.nome || "Personagem sem nome") + "</h1><p class='suave'>" + esc(partes.join(" · ")) +
      (p.proposito ? "<br><i>Propósito de Vida:</i> " + esc(p.proposito) : "") + "</p></div>" +
      "<div class='cabecalho-botoes'><a class='botao' href='#editar'>Editar ficha</a></div></div>" +
      F.atributosHTML(p, R) +
      (falta.length || avisos.length ? "<div class='status-ficha pendente'>" +
        (falta.length ? "Falta escolher: <b>" + esc(falta.join(", ")) + "</b>. " : "") +
        (avisos.length ? avisos.length + (avisos.length > 1 ? " avisos" : " aviso") + " de regra. " : "") +
        "<a href='#editar'>Resolver em Editar »</a></div>" : "");
  }

  function cartaoVida() {
    const R = F.R, j = J(), pv = pvAtual();
    const pct = Math.round(100 * pv / Math.max(1, R.pv_max));
    const tetoTemp = R.teto_temporarios;
    const nomeTemp = F.P.caminho === "A Preservação" ? "Barreira / PV temporários" : "PV temporários";
    let corpo = "<div class='pv'><span class='pv-numero'>" + pv + "<small> / " + R.pv_max + "</small></span>" +
      "<div class='barra-pv' role='progressbar' aria-label='Pontos de Vida' aria-valuemin='0' aria-valuemax='" + R.pv_max + "' aria-valuenow='" + pv + "'>" +
      "<span style='width:" + pct + "%' class='" + (pct <= 33 ? "baixo" : pct <= 50 ? "medio" : "") + "'></span></div></div>" +
      "<div class='linha controles-pv'><label class='sr-only' for='valor-pv'>Valor</label>" +
      "<input id='valor-pv' type='number' inputmode='numeric' min='0' placeholder='Valor'>" +
      botao("sofrer-dano", "Sofrer dano", { classe: "perigo" }) + botao("curar", "Curar", { classe: "bom" }) + "</div>" +
      "<label class='marca'><input type='checkbox' id='dano-continuo'> <span>Dano Contínuo (ignora a RD)</span></label>" +
      "<p class='ajuda'>O dano já desconta a sua RD (" + R.rd + ") e depois o PV temporário. Mínimo 1. " + link("23", "23.1", "regra 23.1") + "</p>" +
      "<div class='linha'>" + H.campo(nomeTemp, H.numero("jogo.temp", { min: 0, max: tetoTemp, rotulo: nomeTemp, classe: "curto" }),
        "Teto " + tetoTemp + ". Não somam entre fontes: fica o maior.", "estreito") +
      H.campo("Ajustar PV", H.numero("jogo.pv", { min: 0, max: R.pv_max, rotulo: "PV atual", classe: "curto" }).replace("<input", "<input placeholder='" + pv + "'"), "Digite direto, se preferir", "estreito") + "</div>" +
      "<div class='botoes'>" + botao("descanso-curto", "Descanso Curto (+" + Math.max(0, R.descanso_curto) + " PV)", { titulo: "1 hora, até 2 por dia (23.6)" }) +
      botao("descanso-longo", "Descanso Longo", { titulo: "8 horas, 1 por dia: PV cheios, remove condições, recarrega tudo (23.6)" }) + "</div>";
    if (j.temp > tetoTemp) corpo += H.avisos(["BONUS_TEMPORARIO_NO_TETO"]);
    if (pv === 0) {
      const m = j.morrendo;
      const caixas = (n, tipo) => Array.from({ length: 3 }, (_, i) => "<span class='bolinha" + (i < n ? " cheia " + tipo : "") + "'></span>").join("");
      corpo += "<div class='morrendo'><h3>Morrendo</h3><p>No seu turno: <b>d20 " + sinal(R.morrendo_bonus) + "</b> (só Presença) contra DT 10" +
        (R.morrendo_vantagem ? ", com <b>Vantagem</b>" : "") + ". 3 sucessos: 1 PV. 3 falhas: morte. 20 natural levanta; 1 natural são 2 falhas. " + link("23", "23.4", "regra") + "</p>" +
        "<p>Sucessos " + caixas(m.s, "s") + " &nbsp; Falhas " + caixas(m.f, "f") + "</p>" +
        "<div class='linha'>" + botao("morrendo", "Rolar Teste de Morrendo", { classe: "primario" }) +
        H.campo("Sucessos", H.numero("jogo.morrendo.s", { min: 0, max: 3, rotulo: "Sucessos", classe: "curto" }), "", "estreito") +
        H.campo("Falhas", H.numero("jogo.morrendo.f", { min: 0, max: 3, rotulo: "Falhas", classe: "curto" }), "", "estreito") + "</div></div>";
    }
    return cartao("Vida", corpo, "vida");
  }

  /**
   * O painel de Energia: tudo o que muda a Energia num lugar só (17.2), pronto para o
   * combate. Cada botão é uma linha da tabela fechada do livro, com o limite dela — o que é
   * "1 vez por Ciclo" fica marcado como feito até o Ciclo virar —, e o registro embaixo
   * mostra de onde veio cada ponto, com o desfazer para o clique errado.
   */
  function cartaoEnergia() {
    const p = F.P, R = F.R, j = J();
    const e = j.energia || 0, custo = R.ultimate.custo;
    const chaves = F.chavesDeCombate(p);
    const marcas = F.marcasDeEnergia(j, chaves);
    const bloqU = bloqueio(0, true);
    // Um botão de fonte: o que aconteceu à esquerda, quanto dá à direita.
    const fonte = (acao, texto, ganho, o) => {
      o = o || {};
      const feito = o.feito;
      return "<button type='button' class='botao fonte-energia" + (feito ? " feito" : "") + (o.classe ? " " + o.classe : "") +
        "' data-acao='" + acao + "'" + Object.entries(o.dados || {}).map(([k, v]) => " data-" + k + "='" + esc(v) + "'").join("") +
        (feito || o.desabilitado ? " disabled" : "") + (o.titulo ? " title='" + esc(o.titulo) + "'" : "") + "><span>" + texto +
        (o.limite ? " <small>" + o.limite + "</small>" : "") + "</span><b>" + (feito ? "✓ " + esc(feito) : ganho) + "</b></button>";
    };
    const limite = (id, texto, ganho, por) => fonte("energia-fonte", texto, ganho,
      { dados: { fonte: id }, limite: "1×/" + por, feito: marcas[id] ? "neste " + por : "" });

    let fontes = fonte("acertou", "Atacou e <b>acertou</b>", "+20 · +" + R.ph_geracao + " PH",
      { titulo: "Ataque Básico que acerta: +20 de Energia e +" + R.ph_geracao + " PH para o grupo (16.2, 17.2)", desabilitado: !R.ataque_basico }) +
      fonte("ataque-basico", "Atacou e <b>errou</b>", "+20",
        { titulo: "Ataque Básico que erra: a Energia vem igual; o PH, não", desabilitado: !R.ataque_basico });
    p.habilidades.forEach((h, i) => {
      const out = R.habilidades[i];
      if (!out || h.tipo === "Passiva") return;
      const bloq = bloqueio(out.nivel_efetivo);
      fontes += fonte("usar-habilidade", "Usou <b>" + esc(h.nome || "Habilidade " + (i + 1)) + "</b>", "+30 · −" + out.ph + " PH",
        { dados: { i: i }, desabilitado: !!bloq || out.ph > (j.ph || 0),
          titulo: bloq ? "Bloqueada: " + bloq : out.ph > (j.ph || 0) ? "O grupo tem " + (j.ph || 0) + " PH" : "Paga o PH e dá +30 de Energia" });
    });
    fontes += limite("dano", "Sofreu dano", "+10", "Ciclo") +
      fonte("energia-fonte", "Derrotou um inimigo", "+10", { dados: { fonte: "derrotou" }, titulo: "Para quem desferiu o golpe" }) +
      limite("quebra", "Quebrou a Tenacidade", "+10", "Ciclo");
    if (R.memo && j.memo_ativo) {
      const nm = F.nomeDoMemo(p);
      fontes += fonte("memo-acao", "<b>" + esc(nm.nome) + "</b> atacou", "+10", { dados: { fonte: "memo_basico" },
        titulo: "Ataque Básico " + nm.de + ": metade dos +20 vai para você" }) +
        fonte("memo-acao", "<b>" + esc(nm.nome) + "</b> usou a Técnica", "+15", { dados: { fonte: "memo_hab", tecnica: "1" },
          titulo: "Técnica " + nm.de + ": metade dos +30 vai para você" });
    }
    const corda = F.valorCorda(p, R);
    if (corda) fontes += limite("corda", "Corda de Ligação", "+" + corda, "combate");
    if (F.coneDaEnergia(p)) fontes += limite("cone", "Cone de Luz", "+5", "Ciclo");

    const origem = chaves.origem === "mesa" ? "da mesa online" : chaves.origem === "mestre" ? "da Área do Mestre" : "";
    const ciclo = "<div class='energia-ciclo'><span>Ciclo <b>" + chaves.n + "</b>" + (origem ? " <span class='suave'>· " + origem + "</span>" : "") +
      "</span>" + (chaves.origem === "local" ? botao("proximo-ciclo", "Próximo Ciclo", { classe: "pequeno",
        titulo: "Libera de novo o que é 1 vez por Ciclo: sofrer dano, Quebrar e o Cone" }) : "") + "</div>";

    const log = (Array.isArray(j.energia_log) ? j.energia_log : []).slice(-6).reverse();
    const registro = log.length
      ? "<ol class='log-energia'>" + log.map((x) => {
          const def = F.ENERGIA[x.f] || { rotulo: x.f };
          const v = Number(x.v) || 0;
          return "<li><b class='" + (v < 0 ? "ruim" : "bom-texto") + "'>" + (v >= 0 ? "+" : "−") + Math.abs(v) + "</b> " +
            esc(x.r || def.rotulo) + (x.q ? " <span class='suave'>(" + esc(x.q) + ")</span>" : "") +
            (x.c ? " <span class='suave'>· Ciclo " + Number(x.c) + "</span>" : "") + "</li>";
        }).join("") + "</ol>" + botao("desfazer-energia", "Desfazer a última", { classe: "pequeno", titulo: "Devolve a Energia da última linha" })
      : "<p class='ajuda'>Nada ainda neste combate.</p>";

    const corpo = "<div class='energia-topo'><span class='energia-numero'><b data-energia>" + e + "</b><small> / 100</small></span>" +
      (e >= custo ? "<span class='etiqueta pronta'>Ultimate pronta</span>" : "<span class='suave'>Ultimate a " + custo + "</span>") + "</div>" +
      "<div class='barra-energia grande' role='progressbar' aria-label='Energia' aria-valuemin='0' aria-valuemax='100' aria-valuenow='" + e + "'>" +
      "<span style='width:" + e + "%'></span><i style='left:" + custo + "%'></i></div>" + ciclo +
      "<h3>O que aconteceu?</h3><div class='fontes-energia'>" + fontes + "</div>" +
      "<p class='ajuda'>Errar o ataque não corta a Energia; só o <b>1 natural</b> corta (aí não clique). Acima de 100 se perde. " +
      link("17", "17.2", "tabela 17.2") + "</p>" +
      "<div class='botoes compactos'>" + botao("ultimate", "Ativar a Ultimate (−" + custo + ")", { classe: "primario", desabilitado: e < custo || !!bloqU }) +
      botao("energia", "−10", { dados: { v: -10 } }) + botao("energia", "+10", { dados: { v: 10 } }) +
      H.numero("jogo.energia", { min: 0, max: 100, rotulo: "Energia", classe: "curto" }) + "</div>" +
      "<h3>Registro</h3>" + registro;
    return cartao("Energia", corpo, "energia");
  }

  function cartaoRecursos() {
    const R = F.R, j = J(), p = F.P;
    let corpo = "<div class='recurso'><div class='recurso-topo'><span class='rotulo'>PH do grupo</span><b data-ph-grupo data-ph-max='" + R.ph_max + "'>" +
      (j.ph || 0) + " / " + R.ph_max + "</b>" +
      " <span class='suave'>começa o combate com " + R.ph_inicio + " · +" + R.ph_geracao + " por Ataque Básico que acerta</span></div>" +
      "<div class='botoes compactos'>" + botao("ph", "−1", { dados: { v: -1 } }) + botao("ph", "+1", { dados: { v: 1 } }) +
      botao("novo-combate", "Novo combate", { titulo: "PH volta ao início, zera acúmulos, recarrega usos por combate/cena e libera a Energia do combate" }) + "</div></div>";
    if (R.esforco_max) {
      corpo += "<div class='recurso'>" + H.marca("jogo.esforco", "<b>Esforço</b> disponível — re-rola um dado que você acabou de rolar") +
        (p.crenca ? "<p class='ajuda'>Volta no Descanso Longo ou agindo pelo que você acredita: <i>" + esc(p.crenca) + "</i></p>" : "") + "</div>";
    }
    // Acúmulos e recursos do Caminho
    const possuidas = F.bencaosPossuidas();
    const contadores = C().acumulos.filter((a) => a.caminho === p.caminho && possuidas.includes(a.bencao)).map((a) => [a.recurso, a.maximo, a.bencao]);
    if (p.caminho === "A Erudição") contadores.unshift(["Acúmulos de Cálculo", 5, "Recurso do Caminho"]);
    for (const [nome, max, origem] of contadores) {
      const v = j.acumulos[nome] || 0;
      corpo += "<div class='recurso'><div class='recurso-topo'><span class='rotulo'>" + esc(nome) + "</span><b>" + v + " / " + max + "</b> <span class='suave'>" + esc(origem) + "</span></div>" +
        "<div class='botoes compactos'>" + botao("acumulo", "−1", { dados: { k: nome, v: -1, max: max } }) + botao("acumulo", "+1", { dados: { k: nome, v: 1, max: max } }) + "</div></div>";
    }
    if (p.caminho === "A Destruição") corpo += "<p class='ajuda'><b>PV como moeda:</b> ativar custa <b>" + 2 * R.nivel + " PV</b> (2 × nível); no Avatar, " + 5 * R.nivel + " PV por dado. " + link("07", "7.2", "regra 7.2") + "</p>";
    if (p.caminho === "A Euforia") corpo += "<div class='recurso'>" + botao("riso", "Rolar a Tabela do Riso (1d6)") + " " + link("13", "13.2", "tabela") + "</div>";
    if (p.caminho === "A Caça") corpo += H.campo("Presa marcada", H.texto("jogo.presa", { rotulo: "Presa marcada", ph: "1 alvo" }), "Crítico " + (R.ataque_basico ? R.ataque_basico.critico : "20") + " · " + link("14", "14.2", "Marcação de Presa"));
    return cartao("Recursos", corpo, "recursos");
  }

  function cartaoDefesa() {
    const R = F.R, j = J();
    const conds = j.condicoes.map((c) => c.nome);
    const lento = conds.includes("Lentidão") || R.avisos.includes("SOBRECARGA");
    const movimento = R.avisos.includes("IMOVEL") ? "não se move (carga)" : lento ? "Lentidão: só sai do lugar com Esforço Total" : "1 Distância por Ação de Movimento";
    return cartao("Defesa e números", "<div class='numeros'>" +
      num("Defesa", R.defesa_com_temporarios, R.defesa_com_temporarios !== R.defesa ? "base " + R.defesa : "") +
      num("Esquiva", R.esquiva == null ? "—" : R.esquiva, R.esquiva == null ? "Pesada não permite" : "Reação") +
      num("RD", R.rd, "teto " + R.teto_rd) +
      num("Velocidade", R.velocidade) +
      num("DT", R.dt, "das Habilidades") +
      num("Eficiência", sinal(R.eficiencia), R.especializacao ? "Especialização " + sinal(R.especializacao) : "") + "</div>" +
      "<p class='ajuda'>Movimento: " + esc(movimento) + " · teto de bônus somado " + sinal(R.teto_bonus) + " · " +
      (R.pode_ser_executado ? "pode ser Executado" : "não pode ser Executado") + "</p>", "defesa");
  }

  function bloqueio(nivelEfetivo, ultimate) {
    const conds = J().condicoes.map((c) => c.nome);
    if (conds.includes("Controlado")) return "Controlado";
    if (!ultimate && conds.includes("Silenciado") && nivelEfetivo >= 4) return "Silenciado";
    return "";
  }

  /**
   * "Agilidade +4" na cor de quem usa — dourado-laranja para a arma, violeta para a
   * Habilidade —, a mesma cor do destaque na faixa de Atributos. Sem Atributo de Habilidade
   * válido (Caminho de dois Atributos sem escolha), avisa: aí o motor não soma nada.
   */
  function usaAtributo(qual) {
    const a = F.usosDosAtributos(F.P, F.R)[qual];
    if (!a) {
      return qual === "habilidade" && M.CAMINHOS[F.P.caminho]
        ? " <span class='etiqueta ruim' title='Escolha o Atributo de Habilidade em Editar ficha: sem ele, nada é somado'>sem Atributo de Habilidade</span>"
        : "";
    }
    return " " + F.etiquetaDeUso(qual, a + " " + sinal(F.R.bonus[a]),
      qual === "arma" ? "O Atributo que esta arma usa no ataque e no dano (18.5)" : "O seu Atributo de Habilidade, no ataque, na DT e no dano");
  }

  function cartaoAcoes() {
    const p = F.P, R = F.R, ab = R.ataque_basico;
    let corpo = "";
    if (ab) {
      corpo += "<div class='acao'><div class='acao-topo'><b>Ataque Básico</b>" + usaAtributo("arma") +
        " <span class='suave'>" + esc(p.arma.nome || p.arma.categoria) + "</span></div>" +
        "<div class='acao-numeros'><span>Ataque " + EG.botoesAtaque(M.rolagem(ab.ataque), "Ataque Básico", { critico: ab.critico }) + "</span>" +
        "<span>Dano " + botaoRolar(ab.texto, "Dano do Ataque Básico") + " <small>média " + ab.media + "</small></span>" +
        "<span>Fraqueza " + botaoRolar(ab.texto_fraqueza, "Dano com Fraqueza") + "</span></div>" +
        "<p class='ajuda'>" + esc(ab.elemento) + " · " + esc(ab.alcance) + " · Tenacidade " + ab.rt + " · crítico " + ab.critico + " (dobra só os dados base)</p>" +
        "<div class='botoes compactos'>" + botao("acertou", "Acertou (+20 Energia, +" + R.ph_geracao + " PH)", { classe: "primario",
          titulo: "Acertou: +20 de Energia para você e +" + R.ph_geracao + " PH para o grupo" }) +
        botao("ataque-basico", "Errou (+20 Energia)", { titulo: "Errou: a Energia vem igual (17.2); só o 1 natural corta" }) + "</div></div>";
    }
    p.habilidades.forEach((h, i) => {
      const out = R.habilidades[i];
      if (!out) return;
      const bloq = h.tipo === "Passiva" ? "" : bloqueio(out.nivel_efetivo);
      const rol = out.rolagem
        ? (out.rolagem.startsWith("DT") ? "<span>" + esc(out.rolagem) + " <small>(o alvo rola)</small></span>"
          : "<span>Ataque " + EG.botoesAtaque(out.rolagem, (h.nome || "Habilidade") + ": ataque", { critico: ab ? ab.critico : "20" }) + "</span>") : "";
      const dano = out.texto ? "<span>" + (h.tipo === "Cura" ? "Cura " : "Dano ") + botaoRolar(out.texto, (h.nome || "Habilidade") + ": " + h.tipo.toLowerCase()) + " <small>média " + out.media + "</small></span>" : "";
      corpo += "<div class='acao" + (bloq ? " bloqueada" : "") + "'><div class='acao-topo'><b>" + esc(h.nome || "Habilidade " + (i + 1)) + "</b>" +
        (out.rolagem || out.texto ? usaAtributo("habilidade") : "") + " <span class='suave'>" +
        esc(h.tipo) + " · Nível " + out.nivel_efetivo + (h.tipo === "Passiva" ? "" : " · " + out.ph + " PH") + "</span>" +
        (bloq ? " <span class='etiqueta ruim'>bloqueada: " + bloq + "</span>" : "") + "</div>" +
        (rol || dano ? "<div class='acao-numeros'>" + rol + dano + "</div>" : "") +
        "<p class='ajuda'>" + [p.elemento, h.alcance ? "até " + h.alcance : "", out.rt ? "Tenacidade " + out.rt : "", out.alvos > 1 ? out.alvos + " alvos" : ""].filter(Boolean).map(esc).join(" · ") + "</p>" +
        (h.efeito ? "<p class='efeito'>" + esc(h.efeito) + "</p>" : "") +
        (h.tipo === "Passiva" ? "" : "<div class='botoes compactos'>" + botao("usar-habilidade", "Usar (−" + out.ph + " PH, +30 Energia)", { dados: { i: i }, desabilitado: !!bloq }) + "</div>") + "</div>";
    });
    const u = R.ultimate, energia = J().energia || 0, bloqU = bloqueio(0, true);
    const ultRola = !!u.texto || ["Teste de Ataque", "Teste de Resistência"].includes(p.ultimate.resolucao);
    corpo += "<div class='acao ultimate" + (bloqU ? " bloqueada" : "") + "'><div class='acao-topo'><b>" + esc(p.ultimate.nome || "Ultimate") + "</b>" +
      (ultRola ? usaAtributo("habilidade") : "") + " <span class='suave'>Ultimate · Nível equivalente " + u.equivalente + " · " + u.custo + " de Energia</span>" +
      (bloqU ? " <span class='etiqueta ruim'>bloqueada: " + bloqU + "</span>" : "") + "</div>" +
      "<div class='acao-numeros'>" + (p.ultimate.resolucao === "Teste de Ataque" ? "<span>Ataque " + EG.botoesAtaque(M.rolagem(R.ataque_habilidade), "Ultimate: ataque") + "</span>" :
        p.ultimate.resolucao === "Teste de Resistência" ? "<span>DT " + R.dt + "</span>" : "") +
      (u.texto ? "<span>" + (p.ultimate.tipo === "Cura" ? "Cura " : "Dano ") + botaoRolar(u.texto, "Ultimate") + " <small>média " + u.media + "</small></span>" : "") + "</div>" +
      "<p class='ajuda'>Não gasta ação · 1 por Ciclo · Tenacidade " + u.rt + (u.alvos > 1 ? " · " + u.alvos + " alvos" : "") +
      (EG.MesaOnline && EG.MesaOnline.ultimateUsada(p.id) ? " · <span class='etiqueta'>já usada neste Ciclo</span>" : "") + "</p>" +
      (p.ultimate.efeito ? "<p class='efeito'>" + esc(p.ultimate.efeito) + "</p>" : "") +
      "<div class='botoes compactos'>" + botao("ultimate", "Ativar a Ultimate (−" + u.custo + ")", { classe: "primario", desabilitado: energia < u.custo || !!bloqU }) + "</div></div>";
    if (R.quebra) {
      const el = C().elementos.find((x) => x.elemento === p.elemento);
      corpo += "<p class='ajuda'><b>Quebra (" + esc(p.elemento) + "):</b> " + botaoRolar(R.quebra.texto, "Dano de Quebra") + " (média " + R.quebra.media + ")" +
        (el ? " + " + esc(el.efeito_quebra) : "") + " · Atrasa 1 casa · +10 Energia. " + link("20", "20.4", "regra") + "</p>";
    }
    return cartao("Ações", corpo, "acoes");
  }

  /** O "V" ao lado do Teste, dizendo de onde a Vantagem vem (a Raça, a Bênção). */
  const marcaVantagem = (fontes) => (fontes && fontes.length
    ? " <span class='etiqueta' title='Vantagem: " + esc(fontes.join(", ")) + "'>V</span>" : "");

  function cartaoTestes() {
    const R = F.R;
    // `vantagem_fontes` é a Raça e as Bênçãos: com ela o clique já rola 2d20 e fica o maior.
    const tr = Object.entries(R.testes_resistencia).map(([nome, t]) =>
      "<li><span>" + esc(nome) + marcaVantagem(t.vantagem_fontes) + "</span>" +
      botaoRolar(t.rolagem, nome, { vantagem: t.vantagem_fontes || [] }) + "</li>").join("");
    const pericias = Object.entries(R.pericias).map(([nome, x]) =>
      "<li class='" + (x.eficiencia ? "treinada" : "") + "'><span>" + (x.eficacia ? "<i class='marcador eficacia' title='Eficácia'></i>" : x.eficiencia ? "<i class='marcador' title='Eficiência'></i>" : "") + esc(nome) +
      marcaVantagem(x.vantagem_fontes) + (x.penalidade ? " <small class='ruim'>" + x.penalidade + "</small>" : "") + "</span>" +
      botaoRolar(x.rolagem, nome, { vantagem: x.vantagem_fontes || [] }) + "</li>").join("");
    return cartao("Testes", "<div class='duas-colunas'><div><h3>Testes de Resistência</h3><ul class='lista-testes'>" + tr + "</ul>" +
      "<p class='ajuda'>Sem crítico e sempre rolados. " + link("22", "Testes de Resistência", "capítulo 22") + "</p></div>" +
      "<div><h3>Perícias</h3><ul class='lista-testes'>" + pericias + "</ul><p class='ajuda'><i class='marcador'></i> Eficiência · <i class='marcador eficacia'></i> Eficácia · " +
      "<span class='etiqueta'>V</span> Vantagem: o clique já rola 2d20 e fica o maior " + link("02", "2.4", "2.4") + "</p></div></div>", "testes");
  }

  function cartaoBencaos() {
    const p = F.P, R = F.R, usos = J().usos, marcaveis = usosMarcaveis();
    const caixasDe = (dono) => marcaveis.filter((u) => u.dono === dono).map((u) =>
      "<label class='marca uso'><input type='checkbox' data-p='jogo.usos." + esc(u.chave) + "' data-t='bool' id='" + F.idDe("jogo.usos." + u.chave) + "'" +
      (usos[u.chave] ? " checked" : "") + "> <span>usado (" + esc(u.rotulo.toLowerCase()) + ")</span></label>").join("");
    let corpo = "";
    const possuidas = F.bencaosPossuidas();
    if (possuidas.length) {
      corpo += "<ul class='lista-bencaos'>" + possuidas.map((nome) => {
        const b = F.bencaoInfo(nome);
        let extra = "";
        if (nome === "Pacto da Ruína" && R.pacto_da_ruina) {
          const x = R.pacto_da_ruina;
          extra = "<p class='efeito'>Gaste <b>" + x.custo_pv + " PV</b>: +" + x.bonus + " de dano (+" + x.bonus_ferido + " com " + x.limiar_pv + " PV ou menos).</p>";
        }
        if (nome === "Fragmentos do Eu Perdido" && p.fragmento) extra = "<p class='efeito'>Memória da " + esc(p.fragmento) + "</p>";
        if (nome === "Avatar da Recordação" && p.forma_avatar) extra = "<p class='efeito'>Forma " + esc(p.forma_avatar) + "</p>";
        return "<li><div>" + F.linkBencao(nome) + (b ? " <span class='suave'>Tier " + b.tier + " · " + esc(b.frequencia) + "</span>" : "") + "</div>" +
          (b ? "<p>" + esc(b.resumo) + "</p>" : "") + extra + caixasDe(nome) + "</li>";
      }).join("") + "</ul>";
    } else corpo += "<p class='ajuda'>Nenhuma Bênção ainda. <a href='#editar'>Escolher em Editar</a>.</p>";
    const tracos = tracosResumo();
    if (tracos.length) {
      corpo += "<h3>Traços de " + esc(p.raca) + " " + link("05", p.raca, "ler") + "</h3><ul class='lista-bencaos'>" + tracos.map((t) =>
        "<li><div><b>" + esc(t.nome) + "</b> <span class='suave'>" + esc(t.tipo) + "</span></div><p>" + esc(t.desc) + "</p>" + (t.tipo === "ativável" ? caixasDe(t.nome) : "") + "</li>").join("") + "</ul>";
    }
    if (p.tecnica) corpo += "<h3>Técnica</h3><p class='efeito'>" + esc(p.tecnica) + "</p>";
    return cartao("Bênçãos e traços", corpo, "bencaos");
  }

  function cartaoCondicoes() {
    const j = J();
    const lista = C().condicoes.filter((c) => c.so_inimigos === "Não" && c.condicao !== "Morrendo");
    const ativas = j.condicoes.map((c, i) => {
      const info = C().condicoes.find((x) => x.condicao === c.nome) || {};
      return "<li><div><b>" + esc(c.nome) + "</b> <span class='suave'>" + esc(info.duracao || "") + (info.acumulo && info.acumulo !== "—" ? " · acúmulo " + esc(info.acumulo) : "") + "</span> " +
        link("21", c.nome, "regra") + "</div><p>" + esc(info.efeito || "") + "</p>" +
        botao("tirar-condicao", "Tirar", { classe: "pequeno", dados: { i: i } }) + "</li>";
    }).join("");
    const corpo = (ativas ? "<ul class='lista-condicoes'>" + ativas + "</ul>" : "<p class='ajuda'>Nenhuma condição ativa.</p>") +
      "<div class='linha'><label class='sr-only' for='nova-condicao'>Condição</label><select id='nova-condicao'><option value=''>— adicionar condição —</option>" +
      lista.filter((c) => !j.condicoes.some((x) => x.nome === c.condicao)).map((c) => "<option>" + esc(c.condicao) + "</option>").join("") + "</select>" +
      botao("add-condicao", "Adicionar") + "</div><p class='ajuda'>Silenciado e Controlado bloqueiam as Habilidades aqui na ficha. Cura não remove condição; o Descanso Longo remove todas.</p>";
    return cartao("Condições", corpo, "condicoes");
  }

  /**
   * O Memoespírito em campo: a ficha dele (11.4) e os ataques prontos para rolar. O ataque
   * normal é em alvo único; a Técnica Principal segue o acréscimo escolhido — Golpe Ancestral
   * (+1 dado, alvo único) ou Explosão de Memória (até 3 alvos, metade dos dados) — e, com os
   * dois (Forma Completa), quem joga escolhe na hora. O dano na tela muda junto.
   */
  function cartaoMemo() {
    const p = F.P, R = F.R, j = J(), m = R.memo;
    if (p.caminho !== "A Recordação" || !m) return "";
    const pv = j.memo_pv == null ? m.pv : Math.min(j.memo_pv, m.pv);
    const memo = p.memoespirito, nm = F.nomeDoMemo(p), nome = nm.nome;
    const atq = F.ataquesDoMemo(p, R), t = atq.tecnica;
    const predador = m.predador_d8 ? " + " + botaoRolar("1d8", nome + ": Predador") : "";
    const fragmentos = atq.bonus_fragmentos ? " <small>(+" + atq.bonus_fragmentos + " dos Fragmentos)</small>" : "";
    // Os botões de "agiu" só valem com ele em campo.
    const foraDeCampo = { desabilitado: !j.memo_ativo, titulo: j.memo_ativo ? "" : "Invoque " + nm.ele + " primeiro" };

    // O ataque normal: sempre em alvo único.
    let ataques = "<div class='acao'><div class='acao-topo'><b>Ataque Básico " + esc(nm.de) + "</b> <span class='suave'>alvo único</span></div>" +
      "<div class='acao-numeros'><span>Ataque " + EG.botoesAtaque(M.rolagem(m.ataque), nome + ": Ataque Básico") + "</span>" +
      "<span>Dano " + botaoRolar(atq.basico.texto, nome + ": dano do Ataque Básico") + predador + " <small>média " + atq.basico.media + "</small>" + fragmentos + "</span>" +
      "<span>Fraqueza " + botaoRolar(atq.basico.fraqueza.texto, nome + ": dano com Fraqueza") + "</span></div>" +
      "<div class='botoes compactos'>" + botao("memo-acao", esc(nome) + " atacou (+10 Energia para você)",
        Object.assign({ classe: "pequeno", dados: { fonte: "memo_basico" } }, foraDeCampo)) + "</div></div>";

    // A Técnica Principal: o acréscimo decide alvo único ou área (11.3, passo 5). Com nome
    // próprio, o nome dela vem na frente; sem, ela é "a Técnica Principal de <nome>".
    const daTecnica = "Técnica Principal " + nm.de;
    const titulo = t.nome
      ? "<b>" + esc(t.nome) + "</b> <span class='suave'>" + esc(daTecnica) + " · 1 vez por Ciclo</span>"
      : "<b>" + esc(daTecnica) + "</b> <span class='suave'>1 vez por Ciclo</span>";
    const rotTecnica = nome + " · " + (t.nome || "Técnica Principal");
    let tecnica;
    if (!t.acrescimos.length) {
      tecnica = "<p class='ajuda'>A " + esc(daTecnica) + " é <b>em alvo único ou em área</b>? Escolha o acréscimo dela — é ele que muda o dano " +
        "(" + link("11", "Passo 5 — As duas Habilidades dele", "11.3") + "):</p>" +
        H.campo("Acréscimo da Técnica Principal", H.lista("memoespirito.acrescimo",
          F.ACRESCIMOS_MEMO.map((a) => [a.nome, a.nome + " — " + a.resumo]), { rotulo: "Acréscimo da Técnica Principal" }));
    } else {
      const modo = t.modo;
      const escolha = t.modos.length > 1 ? "<div class='alternar' role='group' aria-label='Alvo da " + esc(daTecnica) + "'>" +
        t.modos.map((x) => botao("memo-modo", x.rotulo, { classe: "pequeno" + (x.id === modo.id ? " primario" : ""),
          dados: { v: x.id }, titulo: x.id === "area" ? "Até 3 alvos a até uma Distância um do outro, com metade dos dados (mínimo 1)"
            : "+1 dado base contra um alvo só" })).join("") + "</div>" : "";
      tecnica = escolha +
        "<div class='acao-numeros'><span>Ataque " + EG.botoesAtaque(M.rolagem(m.ataque), rotTecnica + ": ataque") + "</span>" +
        "<span>Dano " + botaoRolar(modo.texto, rotTecnica + ": dano" + (modo.alvos > 1 ? " (em área)" : "")) + predador +
        " <small>média " + modo.media + "</small></span>" +
        "<span class='etiqueta" + (modo.alvos > 1 ? " pronta" : "") + "'>" + (modo.alvos > 1 ? "até 3 alvos" : "alvo único") + "</span></div>" +
        "<p class='ajuda'>" + esc(t.acrescimos.map((a) => (F.ACRESCIMOS_MEMO.find((x) => x.nome === a) || {}).nome + ": " +
          (F.ACRESCIMOS_MEMO.find((x) => x.nome === a) || {}).resumo).join(" · ")) + "</p>" +
        (t.marca ? "<p class='efeito'><b>Marca do Passado:</b> ao acertar, aplica Marcado ou Vulnerável até o fim do próximo turno do alvo.</p>" : "") +
        (t.evolutivo ? "<div class='linha'><span class='ajuda'><b>Ataque Evolutivo:</b> este uso tem <b>+" + t.bonus_evolutivo +
          "</b> de dano (já na conta acima) · " + t.usos + (t.usos === 1 ? " uso" : " usos") + " neste combate</span>" +
          botao("memo-evolutivo", "−1", { classe: "pequeno", dados: { v: -1 } }) + botao("memo-evolutivo", "zerar", { classe: "pequeno", dados: { v: 0 } }) + "</div>" : "");
    }
    ataques += "<div class='acao'><div class='acao-topo'>" + titulo + "</div>" + tecnica +
      (memo.hab_ofensiva ? "<p class='efeito'>" + esc(memo.hab_ofensiva) + "</p>" : "") +
      "<div class='botoes compactos'>" + botao("memo-acao", esc(nome) + " usou a Técnica (+15 Energia para você)",
        Object.assign({ classe: "pequeno", dados: { fonte: "memo_hab", tecnica: "1" } }, foraDeCampo)) + "</div></div>";

    // Memória Devastadora: no quinto Fragmento o próximo ataque dele é em área (11.2).
    if (atq.devastadora) {
      ataques += "<div class='acao ultimate'><div class='acao-topo'><b>5 Fragmentos de Memória</b> <span class='suave'>Memória Devastadora</span></div>" +
        "<div class='acao-numeros'><span>Dano " + botaoRolar(atq.devastadora.texto, nome + ": dano em área (5 Fragmentos)") +
        " <small>média " + atq.devastadora.media + "</small></span><span class='etiqueta pronta'>até 3 alvos</span></div>" +
        "<p class='ajuda'>O próximo ataque " + esc(nm.de) + " atinge até 3 alvos com metade dos dados. Depois os Fragmentos zeram (em Recursos).</p></div>";
    }

    const quem = (p.nome ? "Memoespírito de " + p.nome : "O seu Memoespírito");
    const corpo = "<p class='suave'>" + esc([quem, memo.conceito, memo.funcao, memo.elemento].filter(Boolean).join(" · ")) + "</p>" +
      "<div class='linha'>" + (j.memo_ativo ? "<span class='etiqueta pronta'>em campo</span> " + botao("dispensar", "Dispensar", { classe: "pequeno",
          titulo: "Sai de campo, de graça, no seu turno (11.5)" })
        : botao("invocar", (nm.tem ? "Invocar " + esc(nome) : "Invocar o Memoespírito") + " (Ação Complementar + 1 PH)", { classe: "primario" })) + "</div>" +
      "<div class='numeros'>" + num("PV", pv + "<small>/" + m.pv + "</small>") + num("Defesa", m.defesa) + num("VEL", m.velocidade) + num("RD", m.rd) + "</div>" +
      "<div class='linha'>" + H.campo("PV " + esc(nm.de) + " agora", H.numero("jogo.memo_pv", { min: 0, max: m.pv, rotulo: "PV " + nm.de, classe: "curto" }), "", "estreito") + "</div>" +
      ataques +
      "<p class='ajuda'>Tenacidade " + m.rt + " · Testes de Resistência: " + Object.entries(m.tr).map(([a, v]) => esc(a) + " " + sinal(v)).join(", ") +
      " · a Energia das ações " + esc(nm.de) + " vem pela metade para você.</p>" +
      (memo.hab_auxiliar ? "<p class='efeito'><b>Técnica Auxiliar " + esc(nm.de) + ":</b> " + esc(memo.hab_auxiliar) + "</p>" : "");
    return cartao(esc(nome), corpo, "memo", link("11", "11.4", "regra 11.4"));
  }

  /** Rolagem livre do jogador: qualquer expressão, com ou sem Vantagem, e vai para a mesa. */
  function cartaoRolagemLivre() {
    return cartao("Rolagem livre", EG.formRolagemLivre("rolagem-livre-jogar", { ph: "2d6+3 · d20+5 · 1d8+1d6" }) +
      "<p class='ajuda'>Escreva qualquer rolagem (<code>NdF+M</code>, e dá para somar dados: <code>1d8+1d6+2</code>). " +
      "Vantagem vale num d20. Na mesa online, todo mundo vê com o seu nome.</p>", "rolagem-livre-cartao");
  }

  /**
   * O Inventário: o que o personagem carrega e, principalmente, **o que está ocupando o
   * Espaço dele**. O total sozinho não responde a pergunta que a mesa faz ("estou em
   * Lentidão, o que eu deixo cair?"), então a lista traz uma linha por coisa carregada, com
   * nome e com quanto ela ocupa de verdade — a quantidade multiplicada pelo Espaço de cada.
   *
   * Arma e armadura entram na lista porque pesam (24.4), mas são **lidas**, não editadas:
   * trocar uma arma é escolher categoria e propriedade, e isso é da aba Editar ficha. O peso
   * delas vem do motor (`R.espaco_arma`, `R.espaco_armadura`) junto com o total, e não de uma
   * conta refeita aqui — é o que garante que a lista some exatamente o que gera a Lentidão.
   */
  function cartaoInventario() {
    const p = F.P, R = F.R;
    const imovel = R.avisos.includes("IMOVEL"), sobrecarga = R.avisos.includes("SOBRECARGA");
    const estado = imovel ? "<span class='etiqueta ruim'>não se move</span>"
      : sobrecarga ? "<span class='etiqueta ruim'>Lentidão</span>" : "";
    const sobra = R.espaco_livre;
    const resto = sobra < 0
      ? "<span class='ruim'>" + H.espaco(-sobra) + " acima da capacidade</span>"
      : "<span class='suave'>" + (sobra ? "ainda cabe " + H.espaco(sobra) : "sem folga nenhuma") + "</span>";

    // Cada coisa carregada é uma linha de duas alturas: em cima o nome e, encostado na
    // direita, **quanto ela ocupa** — é essa coluna que o olho desce para achar o que soltar.
    // Embaixo, a conta que deu nesse número, com os campos editáveis quando é um item.
    const linha = (classe, nome, ocupa, pe) =>
      "<li class='carga-linha" + (classe ? " " + classe : "") + "'>" +
      "<div class='carga-topo'>" + nome + "<b class='ocupa'>" + H.espaco(ocupa) + "</b></div>" +
      "<div class='carga-pe'>" + pe + "</div></li>";

    // --- O que está equipado: pesa (24.4), mas se troca em Editar ficha ---
    // Sem descrição escrita, a categoria vira o nome da linha ("Armadura leve"): repetir
    // "Armadura Leve · armadura leve" não diz nada a mais a quem está lendo.
    const equipado = [];
    if (p.armadura) equipado.push([p.armadura_nome, "armadura " + p.armadura.toLowerCase(), R.espaco_armadura]);
    if (R.ataque_basico) {
      equipado.push([p.arma.nome, "arma " + p.arma.categoria.toLowerCase() +
        (p.arma.propriedade === "Dissimulada" ? ", Dissimulada" : ""), R.espaco_arma]);
    }
    const linhasEquipado = equipado.map(([nome, oQue, esp]) => linha("equipado",
      "<b>" + esc(nome || oQue.charAt(0).toUpperCase() + oQue.slice(1)) + "</b>", esp,
      "<span class='suave'>" + esc(nome ? oQue : "equipado") + "</span>")).join("");

    // --- Os itens: estes sim se editam aqui ---
    const linhasItens = p.inventario.map((it, i) => {
      const pocao = acharPocao(it.nome);
      const qtd = it.qtd == null ? 1 : it.qtd;
      return linha("", H.texto("inventario." + i + ".nome", { rotulo: "Item", ph: "O que é" }),
        (Number(it.espaco) || 0) * qtd,
        H.numero("inventario." + i + ".qtd", { min: 0, rotulo: "Quantidade", classe: "curto" }) +
        "<span class='suave'>×</span>" +
        H.numero("inventario." + i + ".espaco", { min: 0, passo: "0.5", rotulo: "Espaço de cada", classe: "curto" }) +
        "<span class='suave'>de Espaço</span>" +
        "<span class='carga-botoes'>" +
        (pocao ? botao("beber", "Beber +" + pocao.cura, { classe: "pequeno bom", dados: { i: i }, desabilitado: !(it.qtd > 0) }) : "") +
        botao("tirar-item", "×", { classe: "pequeno", dados: { i: i }, titulo: "Tirar item" }) + "</span>");
    }).join("");

    const lista = linhasEquipado || linhasItens
      ? "<ul class='carga'>" + linhasEquipado + linhasItens + "</ul>" +
        "<p class='carga-total'><span>Total ocupado</span><b class='ocupa'>" + H.espaco(R.ocupado) + "</b></p>"
      : "<p class='ajuda'>Nada ocupando Espaço ainda: sem arma, sem armadura e sem item nenhum.</p>";

    const opcoes = C().pocoes.map(nomePocao).concat(C().itens.map((x) => x.item));
    const corpo = "<p><b>" + H.espaco(R.ocupado) + " / " + R.capacidade + "</b> de Espaço " + estado +
      " · " + resto + "</p>" + lista +
      (linhasEquipado ? "<p class='ajuda'>Arma e armadura também ocupam Espaço, e se trocam em " +
        "<a href='#editar'>Editar ficha</a>.</p>" : "") +
      "<div class='linha'><label class='sr-only' for='novo-item'>Item</label><select id='novo-item'><option value='__outro'>Outro item…</option>" +
      opcoes.map((o) => "<option>" + esc(o) + "</option>").join("") + "</select>" + botao("add-item", "Adicionar") + "</div>" +
      "<div class='linha'>" + H.campo("Créditos (Cr)", H.numero("creditos", { min: 0, rotulo: "Créditos", classe: "curto" }), "Não ocupam Espaço", "estreito") + "</div>" +
      (p.coisa ? "<p class='ajuda'>Carrega e não serve para nada: <i>" + esc(p.coisa) + "</i></p>" : "");
    return cartao("Inventário", corpo, "inventario", link("24", "24.4", "regra"));
  }

  function cartaoCone() {
    const p = F.P;
    if (!F.temCone(p)) return "";
    return cartao("Cone de Luz", F.coneHTML(p, F.R) +
      "<p class='ajuda'>O Bônus Maior já está somado nos números desta ficha e fica <b>fora</b> do teto de " +
      "bônus; o Efeito Condicional <b>entra</b> no teto. " + link("25", "25.2", "regra 25.2") + "</p>",
      "cone-cartao", "<a class='botao pequeno' href='#editar'>trocar a arte</a>");
  }

  function cartaoNotas() {
    return cartao("Notas", H.texto("notas", { area: true, linhas: 5, rotulo: "Notas", ph: "Anotações da sessão, nomes, pistas…" }), "notas");
  }

  /**
   * A história do personagem, inteira e já formatada (o Markdown que o jogador escreveu).
   * Vem embaixo da grade e ocupa a largura toda, porque texto longo em coluna estreita não
   * se lê — e é um <details> aberto: um clique recolhe quando a mesa precisa da tela.
   */
  function cartaoLore() {
    const p = F.P, html = EG.markdown(p.lore);
    if (!html) return "";
    const n = EG.palavras(p.lore);
    return "<details class='cartao lore'" + EG.atributosAbre("lore", true) + "><summary class='cartao-topo'>" +
      "<h2>História de " + esc(p.nome || "este personagem") + "</h2>" +
      "<span class='suave'>" + n + (n === 1 ? " palavra" : " palavras") + " · um clique recolhe</span>" +
      "</summary><div class='texto-lore'>" + html + "</div></details>";
  }

  // ---------------------------------------------------------------------------
  // Tela
  // ---------------------------------------------------------------------------
  function tela() {
    F.abrirAtual();
    const app = document.getElementById("app");
    if (!F.P) { location.hash = "#editar"; return; }
    app.innerHTML = F.barra() + cabecalho() +
      (EG.MesaOnline ? EG.MesaOnline.faixaJogador(F.P) : "") +
      "<div class='grade-jogo'>" +
      "<div class='coluna'>" + cartaoVida() + cartaoEnergia() + cartaoRecursos() + cartaoDefesa() + cartaoCondicoes() + "</div>" +
      "<div class='coluna'>" + cartaoAcoes() + cartaoMemo() + cartaoBencaos() + "</div>" +
      "<div class='coluna'>" + cartaoTestes() + cartaoRolagemLivre() + cartaoCone() + cartaoInventario() + cartaoNotas() + "</div>" +
      "</div>" + cartaoLore();
  }

  // Enter no campo de valor aplica dano
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter" && ev.target.id === "valor-pv") { ev.preventDefault(); document.querySelector("[data-acao='sofrer-dano']").click(); }
  });

  EG.registrarTela("jogar", tela);
})();
