/*
 * ficha-editar.js — Tela "Editar ficha": os doze passos do capítulo 03, mais progressão,
 * equipamento e Memoespírito. Cada mudança recalcula a ficha na hora.
 */
(function () {
  "use strict";

  const EG = window.EG;
  const { esc, sinal } = EG;
  const M = window.Motor;
  const C = () => window.CATALOGO;
  const F = EG.Ficha;
  const H = F.H;
  const link = (n, t, r) => EG.Regras.link(n, t, r);

  // Em qual seção cada aviso aparece
  const SECAO_DO_AVISO = {
    NIVEL_FORA: "basico", JOGADORES_INVALIDO: "basico", JOGADORES_FORA_DA_TABELA: "basico",
    BONUS_RACIAL_INVALIDO: "raca", BONUS_RACIAL_MESMO_ATRIBUTO: "raca",
    ATRIBUTO_HABILIDADE_INVALIDO: "caminho",
    ATRIBUTO_FORA_8_20: "atributos", ATRIBUTO_ACIMA_15_NA_CRIACAO: "atributos", ARRAY_INVALIDO: "atributos",
    COMPRA_ACIMA_DE_28: "atributos", AUMENTO_MESMO_ATRIBUTO: "atributos", AUMENTO_DESPERDICADO: "atributos",
    AUMENTO_ANTES_DO_NIVEL: "atributos",
    PERICIAS_A_MAIS: "pericias", PERICIA_DO_CAMINHO_ESCOLHIDA: "pericias", EFICACIA_SEM_EFICIENCIA: "pericias",
    EFICACIA_PERICIAS_A_MAIS: "pericias", EFICACIA_TR_A_MAIS: "pericias",
    HABILIDADES_A_MAIS: "habilidades", HABILIDADE_NIVEL_ACIMA: "habilidades", RESSONANCIA_III_REPETIDA: "habilidades",
    BENCAO_EM_SLOT_FUTURO: "bencaos", BENCAO_TIER_ACIMA_DO_SLOT: "bencaos", BENCAO_REPETIDA: "bencaos",
    BENCAO_DE_OUTRO_CAMINHO: "bencaos",
    CONE_NIVEL_ACIMA: "equipamento", SOBREPOSICOES_A_MAIS: "equipamento", SOBREPOSICOES_ACIMA_DO_TETO: "equipamento",
    CONJUNTOS_DANO_ACIMA_DE_3: "equipamento", ESQUIVA_PROIBIDA: "equipamento", RD_NO_TETO: "equipamento",
    VEL_FORA_7_25: "equipamento", SOBRECARGA: "equipamento", IMOVEL: "equipamento",
    RESSONANCIA_ANTES_DO_NIVEL: "ressonancias",
    MEMO_FORA_DA_RECORDACAO: "memo", MEMO_ATRIBUTO_ACIMA_5: "memo", MEMO_PONTOS_A_MAIS: "memo",
    MEMO_EVOLUCAO_ANTES_DO_NIVEL: "memo", MEMO_EVOLUCAO_REPETIDA: "memo", MEMO_BONUS_MENORES: "memo",
  };
  // Avisos que são só informação (não são erro de preenchimento)
  const SO_INFORMACAO = ["ESQUIVA_PROIBIDA", "RD_NO_TETO", "BONUS_TEMPORARIO_NO_TETO", "SOBRECARGA", "IMOVEL"];

  const avisosDa = (secao) => F.R.avisos.filter((a) => SECAO_DO_AVISO[a] === secao);

  function secao(id, titulo, corpo, o) {
    o = o || {};
    return "<section class='cartao secao' id='sec-" + id + "'><header class='secao-topo'><h2>" + titulo + "</h2>" +
      (o.regra ? "<span class='secao-regra'>" + o.regra + "</span>" : "") + "</header>" +
      H.avisos(avisosDa(id)) + corpo + "</section>";
  }

  const TIPOS_HABILIDADE = ["Dano", "Cura", "Buff", "Debuff", "Passiva"];
  const ROTULO_CONE = ["", "+1 ou +10 PV", "+1 e +10 PV", "+2 ou +25 PV", "+2 e +25 PV", "+3 ou +50 PV"];
  const linha = (...campos) => "<div class='linha'>" + campos.join("") + "</div>";
  const info = (html) => "<p class='info'>" + html + "</p>";

  // ---------------------------------------------------------------------------
  // Seções
  // ---------------------------------------------------------------------------
  function secaoBasico() {
    return secao("basico", "1 · Personagem",
      linha(H.campo("Nome", H.texto("nome", { rotulo: "Nome" })),
        H.campo("Jogador", H.texto("jogador", { rotulo: "Jogador" }))) +
      linha(H.campo("Nível", H.numero("nivel", { min: 1, max: 20, rotulo: "Nível" }), "1 a 20", "estreito"),
        H.campo("Jogadores na mesa", H.numero("jogadores", { min: 1, max: 6, rotulo: "Jogadores na mesa" }),
          "Define o PH do grupo", "estreito")) +
      H.campo("Conceito", H.texto("conceito", { rotulo: "Conceito", ph: "Quem é esse sujeito, em uma frase" })) +
      H.campo("Propósito de Vida", H.texto("proposito", { area: true, rotulo: "Propósito de Vida",
        ph: "O que ele quer: um objetivo de longo prazo, alcançável e que envolva outras pessoas" }),
      link("03", "Passo 1 — Conceito e Propósito de Vida", "Passo 1 do capítulo 03")),
      { regra: link("03", "Criação de personagem", "Criação, capítulo 03") });
  }

  function secaoRaca() {
    const p = F.P, r = F.racaInfo();
    let corpo = H.campo("Raça", H.lista("raca", C().racas.map((x) => x.raca), { rotulo: "Raça" }));
    if (r) {
      const dois = p.bonus_racial.modo === "Dois Atributos (+1 cada)";
      const opcoes = r.livre ? M.ATRIBUTOS : [r.opcao1, r.opcao2].filter(Boolean);
      let escolha = H.campo("Bônus de atributo", H.lista("bonus_racial.modo", C().listas.modo_humano, { vazio: false, rotulo: "Modo do bônus" }), esc(r.bonus));
      if (!dois) escolha += H.campo("+2 em", H.lista("bonus_racial.attr1", opcoes, { rotulo: "Atributo do +2" }));
      else if (r.livre) {
        escolha += H.campo("+1 em", H.lista("bonus_racial.attr1", opcoes, { rotulo: "Primeiro +1" })) +
          H.campo("e +1 em", H.lista("bonus_racial.attr2", opcoes, { rotulo: "Segundo +1" }));
      } else escolha += H.campo("+1 em cada", "<span class='valor'>" + esc(opcoes.join(" e ")) + "</span>");
      corpo += linha(escolha);
      corpo += "<div class='tracos'>" + tracosDaRaca(r) + "</div>";
      if (p.raca === "Humano") {
        corpo += H.campo("O que você acredita (recarrega o Esforço)", H.texto("crenca", { rotulo: "Crença do Esforço",
          ph: "Ex.: eu não assino nada que eu não consertei" }));
      }
    }
    return secao("raca", "2 · Raça", corpo, { regra: link("05", "Raças", "Raças, capítulo 05") });
  }

  /** Os dois traços da Raça, com a regra inteira do livro. */
  function tracosDaRaca(r) {
    const cap = window.LIVRO.capitulos.find((c) => c.num === "05");
    const i = cap.blocos.findIndex((b) => b.nivel === 2 && b.titulo === r.raca);
    const tracos = [];
    for (let j = i + 1; j < cap.blocos.length && cap.blocos[j].nivel === 3; j++) {
      if (/^Traço/.test(cap.blocos[j].titulo)) tracos.push(cap.blocos[j]);
    }
    if (!tracos.length) return info(esc(r.tracos));
    return tracos.map((b) => "<details class='traco'><summary><b>" + esc(b.titulo.replace(/^Traço \S+ — /, "")) +
      "</b> <span class='suave'>" + esc(/ativável/.test(b.titulo) ? "ativável" : "passivo") + "</span></summary>" +
      "<div class='texto-livro'>" + window.marked.parse(b.md.replace(/^###.*\n/, "")) + "</div></details>").join("");
  }

  function secaoCaminho() {
    const p = F.P, c = F.caminhoInfo(), R = F.R;
    let corpo = H.campo("Caminho", H.lista("caminho", C().caminhos.map((x) => [x.caminho, x.caminho + " (" + x.aeon + ")"]), { rotulo: "Caminho" }));
    if (c) {
      corpo += info("<i>" + esc(c.ideia) + "</i> " + link(F.capituloDoCaminho(c.caminho), "Capítulo " + F.capituloDoCaminho(c.caminho), "ler o Caminho"));
      corpo += "<dl class='resumo'>" +
        "<div><dt>Perícias</dt><dd>" + esc([c.pericia1, c.pericia2, c.pericia3].join(", ")) + "</dd></div>" +
        "<div><dt>N (vitalidade)</dt><dd>" + c.n + "</dd></div>" +
        "<div><dt>Bônus de VEL</dt><dd>" + sinal(c.vel) + "</dd></div>" +
        "<div><dt>Recurso próprio</dt><dd>" + esc(c.recurso) + "</dd></div></dl>";
      const opcoes = [c.attr1, c.attr2].filter(Boolean);
      const atrib = opcoes.length > 1
        ? H.lista("atributo_habilidade", opcoes, { rotulo: "Atributo de Habilidade" })
        : "<span class='valor'>" + esc(opcoes[0]) + "</span>";
      corpo += linha(H.campo("Atributo de Habilidade", atrib, "Fixo pela campanha. Acerta, dimensiona e dá a DT das Habilidades e da Ultimate"));
      if (R.atributo_habilidade && opcoes.includes(R.atributo_habilidade)) {
        corpo += info("Ataque de Habilidade <b>" + M.rolagem(R.ataque_habilidade) + "</b> · DT das Habilidades <b>" + R.dt + "</b>");
      }
    }
    const el = C().elementos.find((x) => x.elemento === p.elemento);
    corpo += H.campo("Elemento", H.lista("elemento", C().elementos.map((x) => x.elemento), { rotulo: "Elemento" }),
      "Suas Habilidades e sua Ultimate causam dano desse Elemento. Arma sem Elemento próprio causa dano Físico.");
    if (el) {
      corpo += info("<b>" + esc(el.elemento) + "</b>: " + esc(el.tematica) + ". Quebra: <b>" + esc(R.quebra ? R.quebra.texto : el.dano_quebra) +
        "</b> de dano + " + esc(el.efeito_quebra) + ". " + link("20", "20.5", "Quebra, 20.5"));
    }
    return secao("caminho", "3 · Caminho, Atributo de Habilidade e Elemento", corpo,
      { regra: link("06", "Os Caminhos: visão geral", "Caminhos, capítulo 06") });
  }

  function secaoAtributos() {
    const p = F.P, R = F.R;
    const array = p.metodo === "Array oficial";
    let corpo = linha(H.campo("Método", H.lista("metodo", C().listas.metodo, { vazio: false, rotulo: "Método" }),
      "O Mestre escolhe um para a mesa inteira"));
    if (array) {
      const usados = Object.values(p.atributos).filter((v) => v != null);
      const faltam = M.ARRAY_OFICIAL.slice();
      usados.forEach((v) => { const i = faltam.indexOf(v); if (i >= 0) faltam.splice(i, 1); });
      corpo += info("Distribua <b>15, 14, 13, 12, 10, 8</b>, um valor para cada Atributo." +
        (faltam.length ? " Faltam: <b>" + faltam.join(", ") + "</b>." : " Todos distribuídos."));
    } else {
      const gasto = R.compra_gasto || 0;
      corpo += info("Todos começam em 8. Custo acumulado: 9 custa 1, 10 custa 2, 11 custa 3, 12 custa 4, 13 custa 5, 14 custa 7, 15 custa 10. " +
        "Pontos gastos: <b class='" + (gasto > 28 ? "ruim" : "") + "'>" + gasto + " de 28</b>.");
    }
    corpo += "<div class='tabela'><table class='tabela-atributos'><thead><tr><th>Atributo</th><th>Distribuído</th><th class='opcional'>Raça</th>" +
      "<th class='opcional'>Aumentos</th><th>Valor</th><th>Bônus</th></tr></thead><tbody>";
    for (const a of M.ATRIBUTOS) {
      const v = p.atributos[a];
      const b0 = Number.isInteger(v) ? Math.max(8, Math.min(20, v)) : 8;
      const raca = R.atributos_criacao[a] - b0, aum = R.atributos[a] - R.atributos_criacao[a];
      const controle = array
        ? H.lista("atributos." + a, M.ARRAY_OFICIAL.map((x) => [x, String(x)]), { num: true, vazio: "—", rotulo: a })
        : H.numero("atributos." + a, { min: 8, max: 15, rotulo: a, classe: "curto" });
      corpo += "<tr><th scope='row'>" + esc(a) + "</th><td>" + controle + "</td><td class='opcional'>" + (raca ? sinal(raca) : "") +
        "</td><td class='opcional'>" + (aum ? sinal(aum) : "") + "</td><td><b>" + R.atributos[a] + "</b></td><td><b>" + sinal(R.bonus[a]) + "</b></td></tr>";
    }
    corpo += "</tbody></table></div>";
    // Aumentos por nível
    const marcos = M.NIVEIS_AUMENTO.filter((n) => n <= R.nivel);
    if (marcos.length) {
      corpo += "<h3>Aumentos de Atributo</h3>" + info("Em cada marco: +2 em um Atributo ou +1 em dois diferentes, teto 20. " +
        link("04", "4.3", "regra 4.3"));
      for (const n of marcos) {
        const base = "aumentos." + n;
        if (!F.P.aumentos[n]) F.P.aumentos[n] = { modo: "Um Atributo (+2)", attr1: "", attr2: "" };
        const dois = F.P.aumentos[n].modo === "Dois Atributos (+1 cada)";
        corpo += linha(H.campo("Nível " + n, H.lista(base + ".modo", C().listas.modo_aumento, { vazio: false, rotulo: "Aumento do nível " + n })),
          H.campo(dois ? "+1 em" : "+2 em", H.lista(base + ".attr1", M.ATRIBUTOS, { rotulo: "Atributo" })),
          dois ? H.campo("e +1 em", H.lista(base + ".attr2", M.ATRIBUTOS, { rotulo: "Segundo Atributo" })) : "");
      }
    } else {
      corpo += info("O primeiro Aumento de Atributo chega no nível 3.");
    }
    return secao("atributos", "4 · Atributos", corpo, { regra: link("04", "Atributos e Perícias", "capítulo 04") });
  }

  function secaoPericias() {
    const p = F.P, R = F.R;
    const doCaminho = R.pericias_caminho;
    const escolhidas = p.pericias_escolhidas.filter((x) => !doCaminho.includes(x));
    const cheio = escolhidas.length >= R.pericias_permitidas;
    let corpo = linha(H.campo("Sintonia usa", H.lista("sintonia", C().listas.sintonia, { vazio: false, rotulo: "Atributo da Sintonia" }),
      "Fixo na criação"));
    corpo += info("Você tem Eficiência nas 3 Perícias do Caminho e escolhe <b>" + R.pericias_permitidas + "</b> " +
      "(2 + Bônus de Sincronia da criação, mínimo 2" + (p.raca === "Humano" ? ", +1 do Humano" : "") + "). " +
      "Escolhidas: <b>" + escolhidas.length + " de " + R.pericias_permitidas + "</b>.");
    const dadosPericia = Object.fromEntries(C().pericias.map((x) => [x.pericia, x]));
    corpo += "<div class='grade-pericias'>";
    for (const [nome, info_] of Object.entries(R.pericias)) {
      const desc = dadosPericia[nome] ? dadosPericia[nome].resolve : "";
      const marca = doCaminho.includes(nome)
        ? "<label class='marca travada'><input type='checkbox' checked disabled> <span>" + esc(nome) + " <small>(Caminho)</small></span></label>"
        : H.naLista("pericias_escolhidas", nome, esc(nome), { desabilitado: cheio });
      corpo += "<div class='pericia' title='" + esc(desc) + "'>" + marca + "<span class='suave'>" + esc(info_.atributo) +
        "</span><span class='valor'>" + esc(info_.rolagem) + "</span></div>";
    }
    corpo += "</div>";
    const pSlots = R.slots_eficacia_pericias, trSlots = R.slots_eficacia_tr;
    if (pSlots || trSlots) {
      corpo += "<h3>Eficácia</h3>" + info("A Eficácia dobra a Eficiência (+" + R.eficacia + " em vez de +" + R.eficiencia +
        "). Nunca entra em Teste de Ataque. " + link("26", "26.4", "regra 26.4"));
      const comEf = Object.entries(R.pericias).filter(([, x]) => x.eficiencia).map(([n]) => n);
      const usadosP = p.eficacia_pericias.length, usadosT = p.eficacia_tr.length;
      corpo += "<p class='rotulo'>Perícias (" + usadosP + " de " + pSlots + ")</p><div class='grade-marcas'>" +
        comEf.map((n) => H.naLista("eficacia_pericias", n, esc(n), { desabilitado: usadosP >= pSlots })).join("") + "</div>";
      corpo += "<p class='rotulo'>Testes de Resistência (" + usadosT + " de " + trSlots + ")</p><div class='grade-marcas'>" +
        M.TESTES_RESISTENCIA.map(([n]) => H.naLista("eficacia_tr", n, esc(n), { desabilitado: usadosT >= trSlots })).join("") + "</div>";
    } else {
      corpo += info("A Eficácia (dobra a Eficiência em algumas Perícias e Testes) chega no nível 5.");
    }
    return secao("pericias", "5 · Perícias", corpo, { regra: link("04", "4.4", "Perícias, 4.4") });
  }

  function resumoHabilidade(h, out) {
    const partes = [];
    if (out.texto) partes.push("<b>" + esc(out.texto) + "</b> (média " + out.media + ")");
    if (out.rolagem) partes.push(out.rolagem.startsWith("DT") ? out.rolagem : "ataque " + out.rolagem);
    partes.push(out.ph ? out.ph + " PH" : "sem PH");
    if (out.rt) partes.push("Tenacidade " + out.rt);
    partes.push("alcance até " + out.alcance_max);
    if (h.area) partes.push(out.alvos + " alvos");
    let html = "<p class='previa'>" + partes.join(" · ") + (out.nivel_efetivo !== h.nivel ? " <span class='etiqueta'>Nível " + out.nivel_efetivo + " pela Ressonância III</span>" : "") + "</p>";
    const guia = h.tipo === "Buff" || h.tipo === "Debuff" ? C().buff_debuff.find((x) => x.nivel === out.nivel_efetivo)
      : h.tipo === "Passiva" ? C().passivas.find((x) => x.nivel === out.nivel_efetivo) : null;
    if (guia) {
      html += "<p class='guia'><b>O que cabe no Nível " + out.nivel_efetivo + ":</b> " + esc(guia.texto) +
        (guia.duracao ? " · duração " + esc(guia.duracao) + " · alvos " + esc(guia.alvos) : "") + "</p>";
    }
    return html;
  }

  function secaoHabilidades() {
    const p = F.P, R = F.R;
    const nmax = R.nivel_max_habilidade;
    let corpo = info("No seu nível: até <b>" + R.habilidades_conhecidas + "</b> Habilidades, de Nível até <b>" + nmax + "</b>." +
      (R.reescreve ? " A partir do nível 16 você reescreve uma por nível em vez de aprender novas." : "") +
      " Você mesmo escreve cada uma, pelas tabelas do capítulo 16. " + link("16", "16.8", "checklist de validação"));
    const alcances = M.ESCALA_DISTANCIA;
    const ress3 = R.ressonancias_liberadas.includes("III") && p.ressonancias.III;
    p.habilidades.forEach((h, i) => {
      const out = R.habilidades[i];
      const base = "habilidades." + i;
      const alcanceMax = alcances.indexOf(out.alcance_max);
      corpo += "<div class='subcartao'><div class='subcartao-topo'><b>Habilidade " + (i + 1) + "</b>" +
        "<button type='button' class='botao pequeno perigo' data-acao='remover-habilidade' data-i='" + i + "' aria-label='Remover Habilidade " + (i + 1) + "'>Remover</button></div>" +
        linha(H.campo("Nome", H.texto(base + ".nome", { rotulo: "Nome da Habilidade" })),
          H.campo("Tipo", H.lista(base + ".tipo", TIPOS_HABILIDADE, { vazio: false, rotulo: "Tipo" }), "", "estreito"),
          H.campo("Nível", H.lista(base + ".nivel", Array.from({ length: Math.max(nmax, h.nivel || 1) }, (_, k) => [k + 1, String(k + 1)]), { num: true, vazio: false, rotulo: "Nível" }), "", "estreito")) +
        (h.tipo === "Passiva" ? "" : linha(
          H.campo("Resolução", H.lista(base + ".resolucao", C().listas.resolucao, { vazio: "—", rotulo: "Resolução" })),
          H.campo("Alcance", H.lista(base + ".alcance", alcances.slice(0, alcanceMax + 1), { vazio: "—", rotulo: "Alcance" }), "", "estreito"),
          "<div class='campo marcas-inline'>" + H.marca(base + ".area", "Em área") +
          (ress3 ? H.marca(base + ".ress3", "Ressonância III aqui") : "") + "</div>")) +
        H.campo("O que ela faz (ficção e efeito)", H.texto(base + ".efeito", { area: true, rotulo: "Efeito da Habilidade",
          ph: "Ex.: crava a marreta no chão; o impacto sai numa linha de brasa" })) +
        resumoHabilidade(h, out) + "</div>";
    });
    const podeMais = p.habilidades.length < R.habilidades_conhecidas;
    corpo += "<button type='button' class='botao' data-acao='nova-habilidade'" + (podeMais ? "" : " disabled") + ">+ Adicionar Habilidade</button>";
    // Ultimate
    const u = R.ultimate;
    corpo += "<h3>Ultimate</h3>" + info("Ativa com " + u.custo + " de Energia, declarada pelo nome, não gasta ação, 1 por Ciclo. Sobe sozinha a cada faixa. " +
      link("17", "Ultimate e Energia", "capítulo 17"));
    corpo += "<div class='subcartao'>" + linha(H.campo("Nome", H.texto("ultimate.nome", { rotulo: "Nome da Ultimate", ph: "Um nome que você vai querer gritar" })),
      H.campo("Tipo", H.lista("ultimate.tipo", ["Dano", "Cura", "Buff", "Debuff"], { vazio: false, rotulo: "Tipo da Ultimate" }), "", "estreito")) +
      linha(H.campo("Resolução", H.lista("ultimate.resolucao", C().listas.resolucao, { vazio: "—", rotulo: "Resolução da Ultimate" })),
        "<div class='campo marcas-inline'>" + H.marca("ultimate.area", "Em área") + "</div>") +
      H.campo("O que ela faz", H.texto("ultimate.efeito", { area: true, rotulo: "Efeito da Ultimate" })) +
      "<p class='previa'>Nível equivalente <b>" + u.equivalente + "</b>" + (u.texto ? " · <b>" + esc(u.texto) + "</b> (média " + u.media + ")" : "") +
      " · Tenacidade " + u.rt + (u.alvos > 1 ? " · " + u.alvos + " alvos" : "") + "</p></div>";
    return secao("habilidades", "6 · Habilidades e Ultimate", corpo, { regra: link("16", "Habilidades", "capítulo 16") });
  }

  function secaoBencaos() {
    const p = F.P, R = F.R;
    if (!p.caminho) return secao("bencaos", "7 · Bênçãos", info("Escolha um Caminho primeiro."));
    const doCaminho = C().bencaos.filter((b) => b.caminho === p.caminho);
    let corpo = info("Uma Bênção a cada nível ímpar (1, 3, 5... 19): você tem <b>" + R.bencaos_possuidas + " de 10</b>. " +
      "Tier I abre no nível 1, Tier II no 9, Tier III no 17. A escolha é permanente.");
    for (let k = 0; k < R.bencaos_possuidas; k++) {
      const nivelSlot = 2 * k + 1;
      const atual = p.bencaos[k] || "";
      const outras = p.bencaos.filter((b, j) => b && j !== k);
      const opcoes = doCaminho.filter((b) => b.requisito <= nivelSlot && !outras.includes(b.bencao))
        .map((b) => [b.bencao, b.n + ". " + b.bencao + " (Tier " + b.tier + ")"]);
      const b = F.bencaoInfo(atual);
      let extra = "";
      if (atual === "Fragmentos do Eu Perdido") {
        extra = H.campo("Memória escolhida", H.lista("fragmento", ["Fúria", "Guarda", "Sabedoria"], { rotulo: "Memória" }));
      } else if (atual === "Avatar da Recordação") {
        extra = H.campo("Forma", H.lista("forma_avatar", ["Manifestada", "Sincronizada"], { rotulo: "Forma do Avatar" }));
      }
      corpo += "<div class='bencao-slot'>" + linha(H.campo("Nível " + nivelSlot, H.lista("bencaos." + k, opcoes, { rotulo: "Bênção do nível " + nivelSlot })), extra) +
        (b ? "<p class='previa'>" + esc(b.resumo) + " · <span class='suave'>" + esc(b.frequencia) + "</span> · " + F.linkBencao(b.bencao, "ler a Bênção") + "</p>" : "") + "</div>";
    }
    if (R.bencaos_possuidas < 10) corpo += info("Próxima Bênção no nível " + (2 * R.bencaos_possuidas + 1) + ".");
    return secao("bencaos", "7 · Bênçãos do Caminho", corpo, { regra: link("06", "6.7", "regra 6.7") });
  }

  function secaoEquipamento() {
    const p = F.P, R = F.R;
    const arm = C().armaduras.find((a) => a.tipo === p.armadura);
    let corpo = "<h3>Armadura ou Vestimenta</h3>" + linha(
      H.campo("Tipo", H.lista("armadura", C().armaduras.map((a) => [a.tipo, a.tipo + " (+" + a.defesa + " Defesa)"]), { rotulo: "Armadura" }), "", "estreito"),
      H.campo("Descrição", H.texto("armadura_nome", { rotulo: "Descrição da armadura", ph: "A aparência é sua" })));
    if (arm) corpo += info(esc(arm.outros) + " · Espaço " + H.espaco(arm.espaco));
    // Arma
    const ab = R.ataque_basico;
    const cat = C().armas.find((a) => a.categoria === p.arma.categoria);
    corpo += "<h3>Arma</h3>" + linha(H.campo("Nome", H.texto("arma.nome", { rotulo: "Nome da arma", ph: "Ex.: marreta de doca" })),
      H.campo("Categoria", H.lista("arma.categoria", C().armas.map((a) => [a.categoria, a.categoria + " (" + a.dados + ")"]), { rotulo: "Categoria" }), "", "estreito")) +
      linha(p.arma.categoria === "Média" ? H.campo("Atributo", H.lista("arma.atributo", ["Poder", "Agilidade"], { vazio: false, rotulo: "Atributo da arma" }), "fixo", "estreito") : "",
        H.campo("Elemento próprio", H.lista("arma.elemento", C().elementos.map((x) => x.elemento), { vazio: "Nenhum (Físico)", rotulo: "Elemento da arma" }), "", "estreito"),
        H.campo("Propriedade especial", H.lista("arma.propriedade", ["Nenhuma"].concat(C().propriedades.map((x) => x.propriedade)), { vazio: false, rotulo: "Propriedade" }), "no máximo uma"));
    const prop = C().propriedades.find((x) => x.propriedade === p.arma.propriedade);
    if (prop) corpo += info("<b>" + esc(prop.propriedade) + ":</b> " + esc(prop.efeito));
    if (ab && cat) {
      corpo += "<p class='previa'>Ataque <b>" + M.rolagem(ab.ataque) + "</b> (" + esc(ab.atributo) + ") · dano <b>" + esc(ab.texto) + "</b> (média " + ab.media + ") · " +
        esc(ab.elemento) + " · alcance " + esc(ab.alcance) + " · Tenacidade " + ab.rt + " · Espaço " + H.espaco(ab.espaco) + "</p>";
    }
    // Cone de Luz
    const cone = R.cone, nivelCone = p.cone.nivel;
    const modoOu = nivelCone && M.CONE[Math.max(1, Math.min(5, nivelCone))][2] === "ou";
    corpo += "<h3>Cone de Luz</h3>" + info("Seu nível permite Cone até Nível <b>" + R.cone_maximo + "</b>. O Mestre concede, como recompensa de marco. " + link("25", "25.2", "regra 25.2"));
    corpo += linha(H.campo("Nome", H.texto("cone.nome", { rotulo: "Nome do Cone" })),
      H.campo("Nível", H.lista("cone.nivel", [1, 2, 3, 4, 5].map((n) => [n, n + " (" + ROTULO_CONE[n] + ")"]), { num: true, vazio: "Sem Cone", rotulo: "Nível do Cone" }), "", "estreito"));
    if (nivelCone) {
      corpo += linha(H.campo("Bônus Maior em", H.lista("cone.alvo", C().listas.alvo_cone, { vazio: "ainda sem alvo", rotulo: "Alvo do Bônus Maior" })),
        p.cone.alvo === "Um Teste de Resistência" ? H.campo("Qual", H.lista("cone.qual", M.TESTES_RESISTENCIA.map((t) => t[0]), { rotulo: "Qual Teste" })) : "",
        p.cone.alvo === "Uma Perícia" ? H.campo("Qual", H.lista("cone.qual", M.PERICIAS.map((t) => t[0]), { rotulo: "Qual Perícia" })) : "",
        modoOu && p.cone.alvo && p.cone.alvo !== "PV máximos" ? H.campo("Numérico ou PV", H.lista("cone.escolha", C().listas.cone_escolha, { vazio: false, rotulo: "Numérico ou PV" }), "", "estreito") : "",
        H.campo("Sobreposições", H.numero("cone.sobreposicoes", { min: 0, max: 5, rotulo: "Sobreposições" }), "", "estreito"));
      corpo += H.campo("Efeito Condicional", H.texto("cone.efeito", { area: true, rotulo: "Efeito Condicional" }));
      const partes = [];
      if (cone.numerico) partes.push("+" + cone.numerico + " em " + (cone.qual || cone.alvo));
      if (cone.pv) partes.push("+" + cone.pv + " PV máximos");
      corpo += "<p class='previa'>" + (partes.length ? "Somando na ficha: <b>" + esc(partes.join(" e ")) + "</b>" : "O Cone ainda não soma em nada: escolha o alvo do Bônus Maior.") + "</p>";
    }
    // Relíquias
    const tier = ["I", "II", "III", "IV"][R.tier_reliquia - 1];
    const textoSlot = { "Cabeça": "PV máximos", "Mãos": "de dano no Ataque Básico", "Tronco": "de Defesa", "Botas": "de Velocidade",
      "Esfera Planar": "de dano de Habilidade e Ultimate do Elemento da Esfera", "Corda de Ligação": "de Energia ao entrar na Fila (1 por combate)" };
    corpo += "<h3>Relíquias (Tier " + tier + ")</h3>" + info("Marque os slots que o Mestre já concedeu. O Tier sobe sozinho com o seu nível. " + link("25", "25.3", "regra 25.3"));
    corpo += "<div class='reliquias'>";
    for (const s of F.SLOTS_RELIQUIA) {
      const valor = M.RELIQUIAS[s][R.tier_reliquia - 1];
      const base = "reliquias." + s;
      corpo += "<div class='reliquia" + (p.reliquias[s].tem ? " ativa" : "") + "'>" + H.marca(base + ".tem", "<b>" + esc(s) + "</b> <span class='suave'>+" + valor + " " + esc(textoSlot[s]) + "</span>") +
        (p.reliquias[s].tem ? linha(H.campo("Nome", H.texto(base + ".nome", { rotulo: "Nome da Relíquia " + s })),
          H.campo("Conjunto", H.lista(base + ".conjunto", C().listas.conjunto, { vazio: false, rotulo: "Conjunto" }), "", "estreito"),
          s === "Esfera Planar" ? H.campo("Elemento da Esfera", H.lista("esfera_elemento", C().elementos.map((x) => x.elemento), { rotulo: "Elemento da Esfera" }),
            p.esfera_elemento && p.esfera_elemento !== p.elemento ? "Só soma se for o seu Elemento (" + esc(p.elemento || "?") + ")" : "", "estreito") : "") : "") + "</div>";
    }
    corpo += "</div>";
    const usados = F.LETRAS_CONJUNTO.filter((l) => R.conjuntos_pecas[l]);
    if (usados.length) {
      corpo += "<h3>Conjuntos</h3>" + info("2 peças do mesmo Conjunto dão um bônus; 4 peças, um efeito condicional por Ciclo. Até +3 na mesma rolagem.");
      for (const l of usados) {
        const base = "conjuntos." + l, pecas = R.conjuntos_pecas[l], c = p.conjuntos[l];
        corpo += "<div class='subcartao'><b>Conjunto " + l + "</b> <span class='etiqueta'>" + pecas + " peça" + (pecas > 1 ? "s" : "") +
          (R.conjuntos_ativos[l] ? " · bônus de " + R.conjuntos_ativos[l] + " ativo" : " · precisa de 2") + "</span>" +
          linha(H.campo("Nome", H.texto(base + ".nome", { rotulo: "Nome do Conjunto " + l })),
            H.campo("Bônus de 2 peças", H.lista(base + ".bonus2", C().listas.bonus_conjunto2, { rotulo: "Bônus de 2 peças" })),
            c.bonus2 === "Um tipo de rolagem +1" ? H.campo("Em qual rolagem", H.lista(base + ".rolagem", ["Teste de Ataque"].concat(M.TESTES_RESISTENCIA.map((t) => t[0]), M.PERICIAS.map((t) => t[0])), { rotulo: "Rolagem" })) : "") +
          (pecas >= 4 ? H.campo("Efeito de 4 peças", H.texto(base + ".efeito4", { area: true, rotulo: "Efeito de 4 peças" })) : "") + "</div>";
      }
    }
    corpo += "<h3>Técnica e acabamento</h3>" +
      H.campo("Técnica", H.texto("tecnica", { area: true, rotulo: "Técnica", ph: "Uma por personagem, 2 usos por Descanso Longo, fora de combate (24.6)" })) +
      H.campo("Uma coisa que você carrega e não serve para nada", H.texto("coisa", { rotulo: "Coisa que não serve para nada" })) +
      H.campo("Aparência e de onde você veio", H.texto("aparencia", { area: true, rotulo: "Aparência e origem" }));
    return secao("equipamento", "8 · Equipamento", corpo, { regra: link("24", "Equipamentos", "capítulo 24") });
  }

  function secaoRessonancias() {
    const R = F.R, L = C().listas;
    if (!R.ressonancias_liberadas.length) {
      return secao("ressonancias", "9 · Ressonâncias", info("A primeira Ressonância chega no nível 5 (depois 10, 15 e 20)."));
    }
    const nomes = { I: ["ress1", 5], II: ["ress2", 10], III: ["ress3", 15], IV: ["ress4", 20] };
    let corpo = info("Cada Ressonância é permanente e é um bom lugar para fechar um capítulo do seu Propósito de Vida. " + link("26", "26.7", "regra 26.7"));
    for (const r of R.ressonancias_liberadas) {
      const [lista, nivel] = nomes[r];
      let ajuda = "";
      if (r === "III" && F.P.ressonancias.III) ajuda = "Marque a Habilidade que sobe na seção 6.";
      if (r === "IV" && F.P.ressonancias.IV === "Avatar afeta um alvo adicional" && !F.bencaosPossuidas().some((b) => /^Avatar/.test(b))) ajuda = "Só vale se você tiver a Bênção Avatar.";
      corpo += linha(H.campo("Ressonância " + r + " (nível " + nivel + ")", H.lista("ressonancias." + r, L[lista], { vazio: "— escolha —", rotulo: "Ressonância " + r }), ajuda));
    }
    return secao("ressonancias", "9 · Ressonâncias", corpo);
  }

  function secaoMemo() {
    const p = F.P, R = F.R, m = p.memoespirito, memo = R.memo;
    if (p.caminho !== "A Recordação") return "";
    const MM = C().memo;
    let corpo = info("O seu companheiro: as estatísticas dele são lidas de você. " + link("11", "11.3", "como criar (11.3)"));
    corpo += linha(H.campo("Nome", H.texto("memoespirito.nome", { rotulo: "Nome do Memoespírito" })),
      H.campo("Conceito", H.lista("memoespirito.conceito", MM.conceitos.map((x) => x.nome), { rotulo: "Conceito" })),
      H.campo("Elemento", H.lista("memoespirito.elemento", C().elementos.map((x) => x.elemento), { rotulo: "Elemento do Memoespírito" }), "", "estreito"));
    const funcao = MM.funcoes.find((x) => x.nome === m.funcao);
    corpo += H.campo("Função", H.lista("memoespirito.funcao", MM.funcoes.map((x) => x.nome), { rotulo: "Função" }), funcao ? esc(funcao.texto) : "");
    corpo += "<p class='rotulo'>Pontos: <b>" + memo.pontos_gastos + " de " + memo.pontos_total + "</b> (máximo 5 por Atributo)</p><div class='linha pontos-memo'>" +
      M.ATRIBUTOS.map((a) => H.campo(a, H.numero("memoespirito.pontos." + a, { min: 0, max: 5, rotulo: "Pontos em " + a, classe: "curto" }), "", "estreito")).join("") + "</div>";
    corpo += linha(H.campo("Atributo de ataque dele", H.lista("memoespirito.atributo_ataque", M.ATRIBUTOS, { vazio: false, rotulo: "Atributo de ataque" }), "", "estreito"));
    const menores = m.bonus_menores;
    corpo += "<p class='rotulo'>Bônus menores (" + menores.length + " de 3)</p><div class='grade-marcas'>" +
      MM.bonus_menores.map((x) => "<span title='" + esc(x.texto) + "'>" + H.naLista("memoespirito.bonus_menores", x.nome, esc(x.nome), { desabilitado: menores.length >= 3 }) + "</span>").join("") + "</div>";
    const evolLiberadas = [8, 14, 20].filter((n) => R.nivel >= n).length;
    corpo += "<p class='rotulo'>Evoluções (" + m.evolucoes.length + " de " + evolLiberadas + " liberadas: níveis 8, 14 e 20)</p><div class='grade-marcas'>" +
      MM.evolucoes.map((x) => "<span title='" + esc(x.texto) + "'>" + H.naLista("memoespirito.evolucoes", x.nome, esc(x.nome), { desabilitado: m.evolucoes.length >= evolLiberadas }) + "</span>").join("") + "</div>";
    if (m.evolucoes.includes("Memória Desperta")) {
      corpo += linha(H.campo("Memória Desperta: +2 em", H.lista("memoespirito.memoria_desperta", ["Defesa", "Velocidade"], { rotulo: "Memória Desperta" }), "", "estreito"));
    }
    corpo += H.campo("Habilidade ofensiva", H.texto("memoespirito.hab_ofensiva", { area: true, rotulo: "Habilidade ofensiva" })) +
      H.campo("Habilidade auxiliar", H.texto("memoespirito.hab_auxiliar", { area: true, rotulo: "Habilidade auxiliar" }));
    corpo += "<p class='previa'>PV <b>" + memo.pv + "</b> · Defesa <b>" + memo.defesa + "</b> · VEL <b>" + memo.velocidade + "</b> · ataque <b>" +
      M.rolagem(memo.ataque) + "</b> · dano <b>" + esc(memo.texto) + "</b> (média " + memo.media + ")" + (memo.predador_d8 ? " +1d8" : "") +
      " · Tenacidade " + memo.rt + (memo.rd ? " · RD " + memo.rd : "") + "</p>";
    return secao("memo", "10 · Memoespírito", corpo);
  }

  // ---------------------------------------------------------------------------
  // Tela
  // ---------------------------------------------------------------------------
  const SECOES = [["basico", "Personagem"], ["raca", "Raça"], ["caminho", "Caminho"], ["atributos", "Atributos"],
    ["pericias", "Perícias"], ["habilidades", "Habilidades"], ["bencaos", "Bênçãos"], ["equipamento", "Equipamento"],
    ["ressonancias", "Ressonâncias"], ["memo", "Memoespírito"]];

  function tela() {
    const app = document.getElementById("app");
    F.abrirAtual();
    if (!F.P) {
      app.innerHTML = F.barra() + "<div class='cartao boas-vindas'><h2>Bem-vindo à ficha de Explorando Galáxias</h2>" +
        "<p>Crie a sua ficha seguindo os doze passos do capítulo 03. Tudo é calculado sozinho e salvo neste navegador.</p>" +
        "<div class='botoes'><button type='button' class='botao primario' data-acao='nova'>Criar minha ficha</button>" +
        "<button type='button' class='botao' data-acao='exemplo'>Ver o exemplo pronto (Nadir)</button>" +
        "<button type='button' class='botao' data-acao='importar'>Importar arquivo</button></div></div>";
      return;
    }
    const falta = F.pendencias();
    const erros = F.R.avisos.filter((a) => !SO_INFORMACAO.includes(a)).length;
    const mostrar = SECOES.filter(([id]) => id !== "memo" || F.P.caminho === "A Recordação");
    app.innerHTML = F.barra() +
      "<nav class='atalhos' aria-label='Seções da ficha'>" + mostrar.map(([id, t]) =>
        "<button type='button' class='atalho" + (F.R.avisos.some((a) => SECAO_DO_AVISO[a] === id && !SO_INFORMACAO.includes(a)) ? " com-aviso" : "") +
        "' data-ir='sec-" + id + "'>" + t + "</button>").join("") + "</nav>" +
      "<div class='status-ficha " + (falta.length || erros ? "pendente" : "ok") + "'>" +
      (falta.length ? "Falta escolher: <b>" + esc(falta.join(", ")) + "</b>." : "Ficha completa.") +
      (erros ? " " + erros + (erros > 1 ? " avisos" : " aviso") + " de regra (em vermelho nas seções)." : "") +
      " <a href='#jogar'>Ir para Jogar »</a></div>" +
      secaoBasico() + secaoRaca() + secaoCaminho() + secaoAtributos() + secaoPericias() + secaoHabilidades() +
      secaoBencaos() + secaoEquipamento() + secaoRessonancias() + secaoMemo();
  }

  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-ir]");
    if (!b) return;
    const alvo = document.getElementById(b.dataset.ir);
    if (alvo) alvo.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  // Ajustes quando um campo muda (antes de recalcular)
  F.aoMudar = function (el) {
    const p = F.P, cam = el.dataset.p || el.dataset.lista;
    if (cam === "caminho") {
      const c = F.caminhoInfo();
      p.atributo_habilidade = c && !c.attr2 ? c.attr1 : (c && [c.attr1, c.attr2].includes(p.atributo_habilidade) ? p.atributo_habilidade : "");
      p.bencaos = [];
      p.pericias_escolhidas = p.pericias_escolhidas.filter((x) => !(c && [c.pericia1, c.pericia2, c.pericia3].includes(x)));
    }
    if (cam === "raca" || cam === "bonus_racial.modo") { p.bonus_racial.attr1 = ""; p.bonus_racial.attr2 = ""; }
    if (cam === "metodo") {
      for (const a of M.ATRIBUTOS) p.atributos[a] = p.metodo === "Compra de Pontos" ? 8 : null;
    }
    if (cam === "nivel" && Number.isInteger(p.nivel)) p.nivel = Math.max(1, Math.min(20, p.nivel));
    if (cam === "cone.alvo") p.cone.qual = "";
    if (/^habilidades\.\d+\.tipo$/.test(cam)) {
      const h = p.habilidades[Number(cam.split(".")[1])];
      if (h.tipo === "Passiva") { h.resolucao = ""; h.area = false; }
      else h.resolucao = { Dano: "Teste de Ataque", Debuff: "Teste de Resistência" }[h.tipo] || "";
    }
    if (/^habilidades\.\d+\.ress3$/.test(cam) && el.checked) {
      p.habilidades.forEach((h, i) => { if (i !== Number(cam.split(".")[1])) h.ress3 = false; });
    }
  };

  F.acoes = F.acoes || {};
  F.acoes["nova-habilidade"] = () => { F.P.habilidades.push(F.novaHabilidade()); };
  F.acoes["remover-habilidade"] = (b) => {
    const i = Number(b.dataset.i), h = F.P.habilidades[i];
    if (h.nome && !confirm("Remover a Habilidade " + h.nome + "?")) return;
    F.P.habilidades.splice(i, 1);
  };

  EG.registrarTela("editar", tela);
})();
