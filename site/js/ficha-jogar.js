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
    recarregar(["combate"]);
    EG.toast("Novo combate: PH do grupo em " + j.ph + ", acúmulos zerados, usos \"por combate\" e \"por cena\" de volta.");
  };

  A["energia"] = (b) => {
    const j = J();
    j.energia = Math.max(0, Math.min(100, (j.energia || 0) + Number(b.dataset.v)));
  };

  A["ultimate"] = () => {
    const j = J(), custo = F.R.ultimate.custo;
    if ((j.energia || 0) < custo) { EG.toast("Faltam " + (custo - (j.energia || 0)) + " de Energia para a Ultimate.", "erro"); return; }
    j.energia -= custo;
    EG.toast("<b>" + esc(F.P.ultimate.nome || "Ultimate") + "!</b> −" + custo + " de Energia.");
  };

  A["ph"] = (b) => { const j = J(); j.ph = Math.max(0, Math.min(F.R.ph_max, (j.ph || 0) + Number(b.dataset.v))); };

  A["usar-habilidade"] = (b) => {
    const i = Number(b.dataset.i), h = F.P.habilidades[i], out = F.R.habilidades[i], j = J();
    if (out.ph > (j.ph || 0)) { EG.toast("Sem PH suficiente: " + esc(h.nome || "a Habilidade") + " custa " + out.ph + " PH e o grupo tem " + (j.ph || 0) + ".", "erro"); return; }
    j.ph -= out.ph;
    j.energia = Math.min(100, (j.energia || 0) + 30);
    EG.toast("<b>" + esc(h.nome || "Habilidade") + "</b>: −" + out.ph + " PH, +30 de Energia.");
  };

  A["ataque-basico"] = () => {
    const j = J();
    j.energia = Math.min(100, (j.energia || 0) + 20);
    EG.toast("Ataque Básico: +20 de Energia (acertando ou não; o 1 natural não dá).");
  };

  A["acertou"] = () => {
    const j = J();
    j.ph = Math.min(F.R.ph_max, (j.ph || 0) + F.R.ph_geracao);
    EG.toast("Acertou o Ataque Básico: +" + F.R.ph_geracao + " PH para o grupo.");
  };

  A["acumulo"] = (b) => {
    const j = J(), k = b.dataset.k;
    j.acumulos[k] = Math.max(0, Math.min(Number(b.dataset.max), (j.acumulos[k] || 0) + Number(b.dataset.v)));
  };

  A["morrendo"] = () => {
    const j = J(), R = F.R;
    const r = EG.rolar("d20" + (R.morrendo_bonus >= 0 ? "+" : "") + R.morrendo_bonus,
      { rotulo: "Teste de Morrendo (DT 10)", vantagem: R.morrendo_vantagem });
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
    EG.toast("Memoespírito invocado: Ação Complementar e −1 PH.");
  };
  A["dispensar"] = () => { J().memo_ativo = false; };

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

  function cartaoRecursos() {
    const R = F.R, j = J(), p = F.P;
    const energia = j.energia || 0, custo = R.ultimate.custo;
    let corpo = "<div class='recurso'><div class='recurso-topo'><span class='rotulo'>Energia</span><b>" + energia + " / 100</b>" +
      (energia >= custo ? " <span class='etiqueta pronta'>Ultimate pronta</span>" : "") + "</div>" +
      "<div class='barra-energia'><span style='width:" + energia + "%'></span><i style='left:" + custo + "%'></i></div>" +
      "<div class='botoes compactos'>" + [10, 20, 30].map((v) => botao("energia", "+" + v, { dados: { v: v }, titulo: v === 10 ? "Sofrer dano, derrotar ou Quebrar" : v === 20 ? "Ataque Básico" : "Habilidade" })).join("") +
      botao("energia", "−10", { dados: { v: -10 } }) + H.numero("jogo.energia", { min: 0, max: 100, rotulo: "Energia", classe: "curto" }) + "</div></div>";
    corpo += "<div class='recurso'><div class='recurso-topo'><span class='rotulo'>PH do grupo</span><b>" + (j.ph || 0) + " / " + R.ph_max + "</b>" +
      " <span class='suave'>começa o combate com " + R.ph_inicio + "</span></div>" +
      "<div class='botoes compactos'>" + botao("ph", "−1", { dados: { v: -1 } }) + botao("ph", "+1", { dados: { v: 1 } }) +
      botao("novo-combate", "Novo combate", { titulo: "PH volta ao início, zera acúmulos e recarrega usos por combate/cena" }) + "</div></div>";
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

  function cartaoAcoes() {
    const p = F.P, R = F.R, ab = R.ataque_basico;
    let corpo = "";
    if (ab) {
      corpo += "<div class='acao'><div class='acao-topo'><b>Ataque Básico</b> <span class='suave'>" + esc(p.arma.nome || p.arma.categoria) + "</span></div>" +
        "<div class='acao-numeros'><span>Ataque " + botaoRolar(M.rolagem(ab.ataque), "Ataque Básico", { critico: ab.critico }) + "</span>" +
        "<span>Dano " + botaoRolar(ab.texto, "Dano do Ataque Básico") + " <small>média " + ab.media + "</small></span>" +
        "<span>Fraqueza " + botaoRolar(ab.texto_fraqueza, "Dano com Fraqueza") + "</span></div>" +
        "<p class='ajuda'>" + esc(ab.elemento) + " · " + esc(ab.alcance) + " · Tenacidade " + ab.rt + " · crítico " + ab.critico + " (dobra só os dados base)</p>" +
        "<div class='botoes compactos'>" + botao("ataque-basico", "Atacar (+20 Energia)") + botao("acertou", "Acertou (+" + R.ph_geracao + " PH)") + "</div></div>";
    }
    p.habilidades.forEach((h, i) => {
      const out = R.habilidades[i];
      if (!out) return;
      const bloq = h.tipo === "Passiva" ? "" : bloqueio(out.nivel_efetivo);
      const rol = out.rolagem
        ? (out.rolagem.startsWith("DT") ? "<span>" + esc(out.rolagem) + " <small>(o alvo rola)</small></span>"
          : "<span>Ataque " + botaoRolar(out.rolagem, (h.nome || "Habilidade") + ": ataque", { critico: ab ? ab.critico : "20" }) + "</span>") : "";
      const dano = out.texto ? "<span>" + (h.tipo === "Cura" ? "Cura " : "Dano ") + botaoRolar(out.texto, (h.nome || "Habilidade") + ": " + h.tipo.toLowerCase()) + " <small>média " + out.media + "</small></span>" : "";
      corpo += "<div class='acao" + (bloq ? " bloqueada" : "") + "'><div class='acao-topo'><b>" + esc(h.nome || "Habilidade " + (i + 1)) + "</b> <span class='suave'>" +
        esc(h.tipo) + " · Nível " + out.nivel_efetivo + (h.tipo === "Passiva" ? "" : " · " + out.ph + " PH") + "</span>" +
        (bloq ? " <span class='etiqueta ruim'>bloqueada: " + bloq + "</span>" : "") + "</div>" +
        (rol || dano ? "<div class='acao-numeros'>" + rol + dano + "</div>" : "") +
        "<p class='ajuda'>" + [p.elemento, h.alcance ? "até " + h.alcance : "", out.rt ? "Tenacidade " + out.rt : "", out.alvos > 1 ? out.alvos + " alvos" : ""].filter(Boolean).map(esc).join(" · ") + "</p>" +
        (h.efeito ? "<p class='efeito'>" + esc(h.efeito) + "</p>" : "") +
        (h.tipo === "Passiva" ? "" : "<div class='botoes compactos'>" + botao("usar-habilidade", "Usar (−" + out.ph + " PH, +30 Energia)", { dados: { i: i }, desabilitado: !!bloq }) + "</div>") + "</div>";
    });
    const u = R.ultimate, energia = J().energia || 0, bloqU = bloqueio(0, true);
    corpo += "<div class='acao ultimate" + (bloqU ? " bloqueada" : "") + "'><div class='acao-topo'><b>" + esc(p.ultimate.nome || "Ultimate") + "</b> <span class='suave'>Ultimate · Nível equivalente " + u.equivalente + " · " + u.custo + " de Energia</span>" +
      (bloqU ? " <span class='etiqueta ruim'>bloqueada: " + bloqU + "</span>" : "") + "</div>" +
      "<div class='acao-numeros'>" + (p.ultimate.resolucao === "Teste de Ataque" ? "<span>Ataque " + botaoRolar(M.rolagem(R.ataque_habilidade), "Ultimate: ataque") + "</span>" :
        p.ultimate.resolucao === "Teste de Resistência" ? "<span>DT " + R.dt + "</span>" : "") +
      (u.texto ? "<span>" + (p.ultimate.tipo === "Cura" ? "Cura " : "Dano ") + botaoRolar(u.texto, "Ultimate") + " <small>média " + u.media + "</small></span>" : "") + "</div>" +
      "<p class='ajuda'>Não gasta ação · 1 por Ciclo · Tenacidade " + u.rt + (u.alvos > 1 ? " · " + u.alvos + " alvos" : "") + "</p>" +
      (p.ultimate.efeito ? "<p class='efeito'>" + esc(p.ultimate.efeito) + "</p>" : "") +
      "<div class='botoes compactos'>" + botao("ultimate", "Ativar a Ultimate (−" + u.custo + ")", { classe: "primario", desabilitado: energia < u.custo || !!bloqU }) + "</div></div>";
    if (R.quebra) {
      const el = C().elementos.find((x) => x.elemento === p.elemento);
      corpo += "<p class='ajuda'><b>Quebra (" + esc(p.elemento) + "):</b> " + botaoRolar(R.quebra.texto, "Dano de Quebra") + " (média " + R.quebra.media + ")" +
        (el ? " + " + esc(el.efeito_quebra) : "") + " · Atrasa 1 casa · +10 Energia. " + link("20", "20.4", "regra") + "</p>";
    }
    return cartao("Ações", corpo, "acoes");
  }

  function cartaoTestes() {
    const R = F.R;
    const tr = Object.entries(R.testes_resistencia).map(([nome, t]) =>
      "<li><span>" + esc(nome) + (t.vantagem ? " <span class='etiqueta' title='Vantagem'>V</span>" : "") + "</span>" +
      botaoRolar(t.rolagem, nome, { vantagem: t.vantagem }) + "</li>").join("");
    const pericias = Object.entries(R.pericias).map(([nome, x]) =>
      "<li class='" + (x.eficiencia ? "treinada" : "") + "'><span>" + (x.eficacia ? "<i class='marcador eficacia' title='Eficácia'></i>" : x.eficiencia ? "<i class='marcador' title='Eficiência'></i>" : "") + esc(nome) +
      (x.vantagem ? " <span class='etiqueta' title='Vantagem'>V</span>" : "") + (x.penalidade ? " <small class='ruim'>" + x.penalidade + "</small>" : "") + "</span>" +
      botaoRolar(x.rolagem, nome, { vantagem: x.vantagem }) + "</li>").join("");
    return cartao("Testes", "<div class='duas-colunas'><div><h3>Testes de Resistência</h3><ul class='lista-testes'>" + tr + "</ul>" +
      "<p class='ajuda'>Sem crítico e sempre rolados. " + link("22", "Testes de Resistência", "capítulo 22") + "</p></div>" +
      "<div><h3>Perícias</h3><ul class='lista-testes'>" + pericias + "</ul><p class='ajuda'><i class='marcador'></i> Eficiência · <i class='marcador eficacia'></i> Eficácia · <span class='etiqueta'>V</span> Vantagem</p></div></div>", "testes");
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

  function cartaoMemo() {
    const p = F.P, R = F.R, j = J(), m = R.memo;
    if (p.caminho !== "A Recordação" || !m) return "";
    const pv = j.memo_pv == null ? m.pv : Math.min(j.memo_pv, m.pv);
    const memo = p.memoespirito;
    const corpo = "<p class='suave'>" + esc([memo.conceito, memo.funcao, memo.elemento].filter(Boolean).join(" · ")) + "</p>" +
      "<div class='linha'>" + (j.memo_ativo ? "<span class='etiqueta pronta'>em campo</span> " + botao("dispensar", "Dispensar", { classe: "pequeno" })
        : botao("invocar", "Invocar (Ação Complementar + 1 PH)", { classe: "primario" })) + "</div>" +
      "<div class='numeros'>" + num("PV", pv + "<small>/" + m.pv + "</small>") + num("Defesa", m.defesa) + num("VEL", m.velocidade) + num("RD", m.rd) + "</div>" +
      "<div class='linha'>" + H.campo("PV dele agora", H.numero("jogo.memo_pv", { min: 0, max: m.pv, rotulo: "PV do Memoespírito", classe: "curto" }), "", "estreito") + "</div>" +
      "<div class='acao-numeros'><span>Ataque " + botaoRolar(M.rolagem(m.ataque), "Memoespírito: ataque") + "</span><span>Dano " +
      botaoRolar(m.texto, "Memoespírito: dano") + (m.predador_d8 ? " + " + botaoRolar("1d8", "Predador") : "") + " <small>média " + m.media + "</small></span></div>" +
      "<p class='ajuda'>Tenacidade " + m.rt + " · Testes de Resistência: " + Object.entries(m.tr).map(([a, v]) => esc(a) + " " + sinal(v)).join(", ") +
      " · a Energia das ações dele vem pela metade para você.</p>" +
      (memo.hab_ofensiva ? "<p class='efeito'><b>Ofensiva:</b> " + esc(memo.hab_ofensiva) + "</p>" : "") +
      (memo.hab_auxiliar ? "<p class='efeito'><b>Auxiliar:</b> " + esc(memo.hab_auxiliar) + "</p>" : "");
    return cartao(esc(memo.nome || "Memoespírito"), corpo, "memo", link("11", "11.4", "ficha dele"));
  }

  function cartaoInventario() {
    const p = F.P, R = F.R;
    const estado = R.avisos.includes("IMOVEL") ? "<span class='etiqueta ruim'>não se move</span>"
      : R.avisos.includes("SOBRECARGA") ? "<span class='etiqueta ruim'>Lentidão</span>" : "";
    const linhas = p.inventario.map((it, i) => {
      const pocao = acharPocao(it.nome);
      return "<tr><td>" + H.texto("inventario." + i + ".nome", { rotulo: "Item" }) + "</td>" +
        "<td>" + H.numero("inventario." + i + ".qtd", { min: 0, rotulo: "Quantidade", classe: "curto" }) + "</td>" +
        "<td>" + H.numero("inventario." + i + ".espaco", { min: 0, passo: "0.5", rotulo: "Espaço", classe: "curto" }) + "</td>" +
        "<td class='acoes-item'>" + (pocao ? botao("beber", "Beber +" + pocao.cura, { classe: "pequeno bom", dados: { i: i }, desabilitado: !(it.qtd > 0) }) : "") +
        botao("tirar-item", "×", { classe: "pequeno", dados: { i: i }, titulo: "Tirar item" }) + "</td></tr>";
    }).join("");
    const opcoes = C().pocoes.map(nomePocao).concat(C().itens.map((x) => x.item));
    const corpo = "<p><b>" + H.espaco(R.ocupado) + " / " + R.capacidade + "</b> de Espaço " + estado +
      " <span class='suave'>(arma e armadura já contam)</span></p>" +
      (linhas ? "<div class='tabela'><table class='inventario'><thead><tr><th>Item</th><th>Qtd.</th><th>Espaço</th><th></th></tr></thead><tbody>" + linhas + "</tbody></table></div>" : "") +
      "<div class='linha'><label class='sr-only' for='novo-item'>Item</label><select id='novo-item'><option value='__outro'>Outro item…</option>" +
      opcoes.map((o) => "<option>" + esc(o) + "</option>").join("") + "</select>" + botao("add-item", "Adicionar") + "</div>" +
      "<div class='linha'>" + H.campo("Créditos (Cr)", H.numero("creditos", { min: 0, rotulo: "Créditos", classe: "curto" }), "Não ocupam Espaço", "estreito") + "</div>" +
      (p.coisa ? "<p class='ajuda'>Carrega e não serve para nada: <i>" + esc(p.coisa) + "</i></p>" : "");
    return cartao("Inventário", corpo, "inventario", link("24", "24.4", "regra"));
  }

  function cartaoNotas() {
    return cartao("Notas", H.texto("notas", { area: true, linhas: 5, rotulo: "Notas", ph: "Anotações da sessão, nomes, pistas…" }), "notas");
  }

  // ---------------------------------------------------------------------------
  // Tela
  // ---------------------------------------------------------------------------
  function tela() {
    F.abrirAtual();
    const app = document.getElementById("app");
    if (!F.P) { location.hash = "#editar"; return; }
    app.innerHTML = F.barra() + cabecalho() +
      "<div class='grade-jogo'>" +
      "<div class='coluna'>" + cartaoVida() + cartaoRecursos() + cartaoDefesa() + cartaoCondicoes() + "</div>" +
      "<div class='coluna'>" + cartaoAcoes() + cartaoMemo() + cartaoBencaos() + "</div>" +
      "<div class='coluna'>" + cartaoTestes() + cartaoInventario() + cartaoNotas() + "</div>" +
      "</div>";
  }

  // Enter no campo de valor aplica dano
  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter" && ev.target.id === "valor-pv") { ev.preventDefault(); document.querySelector("[data-acao='sofrer-dano']").click(); }
  });

  EG.registrarTela("jogar", tela);
})();
