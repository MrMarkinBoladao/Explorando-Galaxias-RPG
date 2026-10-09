/*
 * motor.js — As regras de personagem de Explorando Galáxias (livro v1.2) em JavaScript.
 *
 * É uma tradução, linha por linha, de build/oraculo_ficha.py: mesmas entradas, mesmas
 * saídas, mesmos códigos de aviso. A seção do livro de cada número está no comentário.
 * Se uma regra do livro mudar, mude aqui e no oráculo.
 *
 * API:  Motor.calcular(entradas, catalogo) -> resultado
 *       (catalogo = window.CATALOGO, gerado por site/gerar_site.py; só as Bênçãos são lidas dele)
 */
(function (raiz) {
  "use strict";

  const ATRIBUTOS = ["Poder", "Agilidade", "Vigor", "Sincronia", "Discernimento", "Presença"]; // 04.1

  // 04.2 — Tabela de Bônus de Atributo
  const BONUS = { 8: -1, 9: -1, 10: 0, 11: 0, 12: 1, 13: 1, 14: 2, 15: 3, 16: 3, 17: 4, 18: 4, 19: 5, 20: 5 };

  const ARRAY_OFICIAL = [15, 14, 13, 12, 10, 8];                                   // 03 Passo 4, Método A
  const CUSTO_COMPRA = { 8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 10 };   // 03 Passo 4, Método B
  const VERBA_COMPRA = 28;                                                         // 03 Passo 4
  const TETO_CRIACAO = 15, TETO_ATRIBUTO = 20;                                     // 03 "Os dois tetos"
  const NIVEIS_AUMENTO = [3, 6, 9, 12, 15, 18];                                    // 04.3

  // 05 (v1.2) — par de Atributos de cada Raça (Humano: os seis)
  const RACAS = {
    "Humano": null,
    "Xianzhouíta": ["Vigor", "Sincronia"],
    "Vidyadhara": ["Vigor", "Poder"],
    "Vulpes": ["Agilidade", "Discernimento"],
    "Haloviano": ["Discernimento", "Presença"],
    "Avginiano": ["Agilidade", "Presença"],
    "Intellitron": ["Sincronia", "Poder"],
  };

  // 04.4 — Perícias e atributo (Sintonia: Discernimento ou Sincronia, fixo na criação)
  const PERICIAS = [["Atletismo", "Poder"], ["Acrobacia", "Agilidade"], ["Furtividade", "Agilidade"],
    ["Pilotagem", "Agilidade"], ["Resistência", "Vigor"], ["Tecnologia", "Sincronia"],
    ["Pesquisa", "Sincronia"], ["Ciência", "Sincronia"], ["Mecânica", "Sincronia"],
    ["Percepção", "Discernimento"], ["Sobrevivência", "Discernimento"],
    ["Intuição", "Discernimento"], ["Investigação", "Discernimento"],
    ["Persuasão", "Presença"], ["Intimidação", "Presença"], ["Enganação", "Presença"],
    ["Liderança", "Presença"], ["Sintonia", null]];

  // 04.6 — Testes de Resistência
  const TESTES_RESISTENCIA = [["Potência Física", "Poder"], ["Reflexos", "Agilidade"],
    ["Resistência Física", "Vigor"], ["Resistência Mental", "Sincronia"],
    ["Percepção Mental", "Discernimento"], ["Força de Vontade", "Presença"]];

  // 06.3 — [atributos de Habilidade, 3 Perícias, N, Bônus de VEL]
  const CAMINHOS = {
    "A Destruição": [["Poder", "Vigor"], ["Atletismo", "Sobrevivência", "Resistência"], 6, 1],
    "A Inexistência": [["Discernimento", "Sincronia"], ["Percepção", "Pesquisa", "Furtividade"], 4, 2],
    "A Harmonia": [["Presença"], ["Liderança", "Sintonia", "Persuasão"], 3, 2],
    "A Abundância": [["Presença", "Sincronia"], ["Liderança", "Intuição", "Sobrevivência"], 5, 1],
    "A Recordação": [["Sincronia", "Discernimento"], ["Intimidação", "Investigação", "Ciência"], 3, 1],
    "A Erudição": [["Sincronia"], ["Ciência", "Pesquisa", "Tecnologia"], 3, 1],
    "A Euforia": [["Presença", "Discernimento"], ["Enganação", "Acrobacia", "Persuasão"], 3, 3],
    "A Caça": [["Agilidade"], ["Furtividade", "Percepção", "Acrobacia"], 2, 4],
    "A Preservação": [["Vigor", "Poder"], ["Resistência", "Atletismo", "Intuição"], 5, 0],
  };

  // 24.1 — Armaduras: [Defesa, VEL, RD, penalidade de Agilidade, Esquiva permitida, Espaço]
  const ARMADURAS = { "Leve": [3, 1, 0, 0, true, 1], "Média": [5, 0, 0, 0, true, 2],
    "Pesada": [6, -2, 2, -2, false, 3] };
  const PERICIAS_PENALIZADAS_PESADA = ["Acrobacia", "Furtividade", "Pilotagem"];   // 24.1

  // 24.2 / 18.5 — Armas: [face, dados extras iniciais, alcance, atributo, Espaço]
  const ARMAS = { "Leve": [8, 0, "Pessoal", "Agilidade", 0.5], "Média": [10, 0, "Pessoal", null, 1],
    "Pesada": [12, 0, "Pessoal", "Poder", 2], "Disparo curto": [8, 0, "Média", "Agilidade", 1],
    "Disparo longo": [10, 0, "Longa", "Agilidade", 2], "Energia": [8, 1, "Longa", "Sincronia", 2] };
  const ESCALA_DISTANCIA = ["Pessoal", "Curta", "Média", "Longa", "Extrema"];      // 18.8

  // 16.3 — Níveis de Habilidade: [dano n, face, cura n, face, PH, RT]
  const NIVEIS_HAB = { 1: [6, 6, 5, 8, 1, 2], 2: [5, 10, 6, 10, 1, 2], 3: [6, 12, 8, 12, 2, 3],
    4: [6, 20, 7, 20, 3, 4], 5: [10, 20, 10, 20, 4, 5], 6: [14, 20, 14, 20, 5, 6],
    7: [18, 20, 18, 20, 6, 7] };
  const ALCANCE_MAX_HAB = { 1: "Curta", 2: "Média", 3: "Longa" };                 // 16.3 (4+: Extrema)

  // 26.2 — Habilidades conhecidas e Nível máximo por nível do personagem
  const HAB_CONHECIDAS = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 8, 8, 8, 8];
  const NIVEL_MAX_HAB = [1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7];
  // 26.2 — slots de Eficácia [Perícias, Testes de Resistência]
  const SLOTS_EFICACIA = { 1: [0, 0], 5: [1, 1], 8: [2, 1], 11: [2, 2], 14: [3, 2], 17: [4, 2], 20: [5, 3] };

  // 17.3 — Ultimate por faixa: [Nível equivalente, dano n, face, cura n, face]
  const ULTIMATE = { 1: [2, 5, 10, 6, 10], 2: [3, 6, 12, 8, 12], 3: [4, 6, 20, 7, 20],
    4: [5, 10, 20, 10, 20], 5: [6, 14, 20, 14, 20] };

  // 20.5 — Dano de Quebra: [dados, face, multiplicador da Eficiência]
  const QUEBRA = { "Físico": [2, 6, 2], "Fogo": [2, 6, 2], "Raio": [1, 6, 1], "Vento": [1, 6, 1],
    "Gelo": [0, 0, 1], "Quântico": [0, 0, 1], "Imaginário": [0, 0, 1] };

  // 25.2 — Cone de Luz: nível -> [bônus numérico, bônus de PV, "e"/"ou"]
  const CONE = { 1: [1, 10, "ou"], 2: [1, 10, "e"], 3: [2, 25, "ou"], 4: [2, 25, "e"], 5: [3, 50, "ou"] };
  const TETO_CONE_NUM = 3;                                                         // 25.2 Sobreposição
  const SOBREPOSICAO_PV = 10;                  // 25.2 (v1.1): cada Sobreposição soma +1 e +10 PV

  // 25.3 — Relíquias: slot -> valores por Tier I..IV
  const RELIQUIAS = { "Cabeça": [10, 20, 35, 50], "Mãos": [2, 4, 6, 8], "Tronco": [1, 1, 2, 2],
    "Botas": [2, 3, 4, 5], "Esfera Planar": [2, 4, 6, 8], "Corda de Ligação": [10, 15, 20, 25] };

  // 27.2 — DT por faixa
  const DT_FAIXA = { "Trivial": [8, 9, 10, 11, 12], "Fácil": [10, 12, 14, 16, 18],
    "Média": [13, 16, 19, 22, 25], "Difícil": [16, 19, 23, 27, 30],
    "Muito Difícil": [19, 23, 27, 31, 35], "Heroica": [22, 26, 31, 34, 38] };
  const DT_FRAQUEZA = [13, 14, 15, 16, 17];                                        // 20.2
  const VERBA_MARCO = [200, 500, 1200, 2500, 5000];                                // 24.5

  const VANTAGEM_PERICIA = { "Vulpes": ["Persuasão", "Intimidação", "Enganação", "Liderança"],
    "Intellitron": ["Tecnologia", "Mecânica"] };                                   // 05
  const VANTAGEM_TR = { "Xianzhouíta": TESTES_RESISTENCIA.map((t) => t[0]),
    "Avginiano": ["Resistência Mental", "Percepção Mental", "Força de Vontade"],
    "Vulpes": ["Força de Vontade"] };                                              // 05, 22.6
  const VANTAGEM_TR_CONDICIONAL = {};                                               // 05 (v1.2): vazio
  const VANTAGEM_MORRENDO = ["Xianzhouíta", "Vulpes", "Avginiano"];               // 23.5

  // Mensagens dos avisos, em linguagem de mesa
  const AVISOS = {
    NIVEL_FORA: "O nível precisa estar entre 1 e 20.",
    JOGADORES_INVALIDO: "O número de jogadores precisa estar entre 1 e 6.",
    JOGADORES_FORA_DA_TABELA: "A tabela de PH do livro vai de 3 a 6 jogadores (16.2).",
    ATRIBUTO_FORA_8_20: "Atributo fora de 8 a 20.",
    ATRIBUTO_ACIMA_15_NA_CRIACAO: "Nenhum Atributo passa de 15 na criação, antes do bônus da Raça (03).",
    ARRAY_INVALIDO: "No array oficial, cada valor (15, 14, 13, 12, 10, 8) é usado uma vez só (03).",
    COMPRA_ACIMA_DE_28: "A Compra de Pontos passou de 28 pontos (03).",
    BONUS_RACIAL_INVALIDO: "Esse Atributo não está entre as opções da sua Raça (05).",
    BONUS_RACIAL_MESMO_ATRIBUTO: "No +1 em dois, os dois Atributos precisam ser diferentes (05).",
    AUMENTO_MESMO_ATRIBUTO: "No aumento de +1 em dois, os Atributos precisam ser diferentes (04.3).",
    AUMENTO_DESPERDICADO: "Um aumento passou do teto 20: o excesso se perde (04.3).",
    AUMENTO_ANTES_DO_NIVEL: "Há aumento de Atributo de um nível que você ainda não alcançou (04.3).",
    RESSONANCIA_ANTES_DO_NIVEL: "Há Ressonância escolhida antes do nível dela (5, 10, 15, 20).",
    RESSONANCIA_III_REPETIDA: "A Ressonância III vale para uma Habilidade só: vale a primeira marcada (26.7).",
    ATRIBUTO_HABILIDADE_INVALIDO: "Escolha o Atributo de Habilidade entre os que o seu Caminho permite (03, Passo 5).",
    PERICIAS_A_MAIS: "Perícias escolhidas acima do permitido (03, Passo 7).",
    PERICIA_DO_CAMINHO_ESCOLHIDA: "Essa Perícia já vem do Caminho: escolha outra (03, Passo 7).",
    EFICACIA_SEM_EFICIENCIA: "Eficácia só vale em Perícia que já tem Eficiência (04.5).",
    EFICACIA_PERICIAS_A_MAIS: "Eficácia em mais Perícias do que o seu nível permite (26.4).",
    EFICACIA_TR_A_MAIS: "Eficácia em mais Testes de Resistência do que o seu nível permite (26.4).",
    HABILIDADES_A_MAIS: "Mais Habilidades do que o seu nível permite (26.2).",
    HABILIDADE_NIVEL_ACIMA: "Uma Habilidade passou do Nível máximo do seu nível (26.2).",
    BENCAO_EM_SLOT_FUTURO: "Há Bênção num slot que o seu nível ainda não liberou (06.7).",
    BENCAO_TIER_ACIMA_DO_SLOT: "Há Bênção de Tier acima do nível do slot (06.7).",
    BENCAO_REPETIDA: "A mesma Bênção foi escolhida duas vezes.",
    BENCAO_DE_OUTRO_CAMINHO: "Há Bênção que não é do seu Caminho.",
    CONE_NIVEL_ACIMA: "O Cone de Luz está acima do Nível que a sua faixa permite (25.1).",
    SOBREPOSICOES_A_MAIS: "Sobreposições acima de uma por faixa alcançada (25.2).",
    SOBREPOSICOES_ACIMA_DO_TETO: "As Sobreposições passaram do teto +3 do Cone (25.2).",
    CONJUNTOS_DANO_ACIMA_DE_3: "Os Conjuntos não somam mais de +3 na mesma rolagem (25.3).",
    ESQUIVA_PROIBIDA: "Armadura Pesada não permite Esquiva (24.1).",
    RD_NO_TETO: "A sua RD passou do teto e foi limitada (18.4).",
    VEL_FORA_7_25: "Velocidade fora de 7 a 25: confira com o Mestre (19.1).",
    BONUS_TEMPORARIO_NO_TETO: "Bônus temporários passaram do teto da faixa e foram limitados (26.6).",
    SOBRECARGA: "Carga acima da capacidade: você fica com Lentidão (24.4).",
    IMOVEL: "Carga acima do dobro da capacidade: você não se move (24.4).",
    MEMO_FORA_DA_RECORDACAO: "Memoespírito é só do Caminho da Recordação.",
    MEMO_ATRIBUTO_ACIMA_5: "Memoespírito: no máximo 5 pontos por Atributo (11.3).",
    MEMO_PONTOS_A_MAIS: "Memoespírito: pontos acima do total disponível (11.3).",
    MEMO_EVOLUCAO_ANTES_DO_NIVEL: "Memoespírito: Evolução antes do nível 8, 14 ou 20 (11.3).",
    MEMO_EVOLUCAO_REPETIDA: "Memoespírito: Evolução repetida (11.3).",
    MEMO_BONUS_MENORES: "Memoespírito: escolha até 3 Bônus menores diferentes (11.3).",
  };

  // ---------------------------------------------------------------------------
  // Regras por nível
  // ---------------------------------------------------------------------------
  const div = (a, b) => Math.floor(a / b);
  const eficiencia = (n) => 2 + div(n - 1, 3);                                    // 02.3 / 26.4
  const faixa = (n) => div(n - 1, 4) + 1;                                          // 26.3
  const especializacao = (n) => (n < 5 ? 0 : n < 11 ? 1 : n < 17 ? 2 : 3);         // 26.5
  function slotsEficacia(n) {                                                      // 26.4
    const chave = Math.max(...Object.keys(SLOTS_EFICACIA).map(Number).filter((k) => k <= n));
    return SLOTS_EFICACIA[chave];
  }
  const tetoBonus = (n) => (n <= 9 ? 3 : n <= 15 ? 4 : 5);                         // 26.6
  const dadosAb = (n) => 1 + div(n - 1, 4);                                        // 18.5 / 26.2
  const tierReliquia = (n) => (n <= 6 ? 1 : n <= 12 ? 2 : n <= 17 ? 3 : 4);        // 25.1 / 25.3
  function phGrupo(n, jogadores) {                                                 // 16.2 / 26.3
    const extra = n >= 9 && n <= 16 ? 1 : n >= 17 ? 2 : 0;
    const mx = 1 + jogadores + extra;
    return [mx, mx - 2, n <= 8 ? 1 : 2];
  }
  const bonus = (v) => BONUS[Math.max(8, Math.min(20, v))];
  const media = (n, face) => div(n * (face + 1), 2);                               // 02.5
  const rolagem = (b) => (b >= 0 ? "d20+" + b : "d20" + b);
  function textoDano(n, face, fixo) {
    if (n <= 0) return String(fixo);
    return n + "d" + face + (fixo > 0 ? "+" + fixo : fixo < 0 ? String(fixo) : "");
  }
  const ehInt = (v) => typeof v === "number" && Number.isInteger(v);
  const contar = (lista, x) => lista.filter((y) => y === x).length;

  // Catálogo de Bênçãos: {nome: [caminho, número, tier, requisito]}
  function catalogoBencaos(catalogo) {
    const cat = {};
    for (const b of (catalogo && catalogo.bencaos) || []) {
      cat[b.bencao] = [b.caminho, b.n, b.tier, b.requisito];
    }
    return cat;
  }

  // ---------------------------------------------------------------------------
  // Cálculo (mesma ordem e mesmos nomes de build/oraculo_ficha.py)
  // ---------------------------------------------------------------------------
  function calcular(e, catalogo) {
    e = e || {};
    const av = [];
    const aviso = (cod) => { if (!av.includes(cod)) av.push(cod); };
    const s = {};

    // --- Nível e mesa ---
    const nivelIn = e.nivel;
    let L = ehInt(nivelIn) ? nivelIn : 1;
    if (nivelIn != null && (!ehInt(nivelIn) || nivelIn < 1 || nivelIn > 20)) aviso("NIVEL_FORA");
    L = Math.max(1, Math.min(20, L));
    const jogIn = e.jogadores;
    let jog = ehInt(jogIn) ? jogIn : 4;
    if (jogIn != null && (!ehInt(jogIn) || jogIn < 1 || jogIn > 6)) aviso("JOGADORES_INVALIDO");
    jog = Math.max(1, Math.min(6, jog));
    if (jog < 3 || jog > 6) aviso("JOGADORES_FORA_DA_TABELA");
    const ef = eficiencia(L);
    const fx = faixa(L);
    const [pSlots, trSlots] = slotsEficacia(L);
    Object.assign(s, {
      nivel: L, faixa: fx, eficiencia: ef, eficacia: 2 * ef,
      slots_eficacia_pericias: pSlots, slots_eficacia_tr: trSlots,
      especializacao: especializacao(L), teto_bonus: tetoBonus(L),
      teto_penalidade: -tetoBonus(L), teto_dados_adicionais: 3,
      teto_rd: 2 + 2 * ef, teto_temporarios: 3 * ef,
      bencaos_possuidas: div(L + 1, 2), habilidades_conhecidas: HAB_CONHECIDAS[L - 1],
      reescreve: L >= 16, nivel_max_habilidade: NIVEL_MAX_HAB[L - 1],
      dados_ab: dadosAb(L), aumento_neste_nivel: NIVEIS_AUMENTO.includes(L),
      tier_reliquia: tierReliquia(L), cone_maximo: fx,
      ultimate_equivalente: ULTIMATE[fx][0], pontos_memo: 12 + div(L, 2),
      verba_marco: VERBA_MARCO[fx - 1], dt_fraqueza: DT_FRAQUEZA[fx - 1],
      dt_faixa: Object.fromEntries(Object.entries(DT_FAIXA).map(([k, v]) => [k, v[fx - 1]])),
      ressonancias_liberadas: [["I", 5], ["II", 10], ["III", 15], ["IV", 20]]
        .filter(([, n]) => L >= n).map(([r]) => r),
    });
    [s.ph_max, s.ph_inicio, s.ph_geracao] = phGrupo(L, jog);

    // --- Atributos ---
    const raca = e.raca;
    const caminho = e.caminho;
    const base = Object.assign({}, e.atributos || {});
    for (const a of ATRIBUTOS) {
      if (!(a in base)) base[a] = e.metodo === "Compra de Pontos" ? 8 : null;
    }
    const valoresBase = ATRIBUTOS.map((a) => base[a]);
    if (e.metodo === "Array oficial" && valoresBase.every(ehInt)) {
      const ord = valoresBase.slice().sort((x, y) => y - x);
      if (ord.some((v, i) => v !== ARRAY_OFICIAL[i])) aviso("ARRAY_INVALIDO");
    }
    if (e.metodo === "Compra de Pontos") {
      let gasto = 0;
      for (const v of valoresBase) if (ehInt(v)) gasto += CUSTO_COMPRA[Math.max(8, Math.min(15, v))] || 0;
      s.compra_gasto = gasto;
      if (gasto > VERBA_COMPRA) aviso("COMPRA_ACIMA_DE_28");
    }
    for (const v of valoresBase) {
      if (ehInt(v) && v > TETO_CRIACAO) aviso("ATRIBUTO_ACIMA_15_NA_CRIACAO");
      if (ehInt(v) && (v < 8 || v > 20)) aviso("ATRIBUTO_FORA_8_20");
    }
    const racial = Object.fromEntries(ATRIBUTOS.map((a) => [a, 0]));
    const br = e.bonus_racial || {};
    if (raca in RACAS) {
      const opcoes = RACAS[raca];
      const dois = br.modo === "Dois Atributos (+1 cada)";
      if (opcoes === null) {                                   // Humano: os seis Atributos
        if (dois) {
          const a1 = br.attr1, a2 = br.attr2;
          if (a1 in racial) racial[a1] += 1;
          if (a2 in racial) {
            if (a2 === a1) aviso("BONUS_RACIAL_MESMO_ATRIBUTO");
            else racial[a2] += 1;
          }
        } else if (br.attr1 in racial) {
          racial[br.attr1] += 2;
        }
      } else if (dois) {
        for (const a of opcoes) racial[a] += 1;                // "+1 em cada": o par da Raça
      } else {
        const escolhido = br.attr1 || (opcoes.length === 1 ? opcoes[0] : null);
        if (opcoes.includes(escolhido)) racial[escolhido] += 2;
        else if (escolhido != null) aviso("BONUS_RACIAL_INVALIDO");
      }
    }
    const aumentos = Object.fromEntries(ATRIBUTOS.map((a) => [a, 0]));
    for (const [nvTxt, au] of Object.entries(e.aumentos || {})) {
      const nv = Number(nvTxt);
      if (NIVEIS_AUMENTO.includes(nv) && nv > L && au && (au.attr1 || au.attr2)) aviso("AUMENTO_ANTES_DO_NIVEL");
      if (!NIVEIS_AUMENTO.includes(nv) || nv > L || !au) continue;
      if (au.modo === "Dois Atributos (+1 cada)") {
        const a1 = au.attr1, a2 = au.attr2;
        if (a1 in aumentos) aumentos[a1] += 1;
        if (a2 in aumentos) {
          if (a2 === a1) aviso("AUMENTO_MESMO_ATRIBUTO");
          else aumentos[a2] += 1;
        }
      } else if (au.attr1 in aumentos) {
        aumentos[au.attr1] += 2;
      }
    }
    const attr = {}, bon = {}, criacao = {};
    for (const a of ATRIBUTOS) {
      let b0 = ehInt(base[a]) ? base[a] : 8;
      b0 = Math.max(8, Math.min(20, b0));
      criacao[a] = Math.min(TETO_ATRIBUTO, b0 + racial[a]);
      const bruto = b0 + racial[a] + aumentos[a];
      if (bruto > TETO_ATRIBUTO && aumentos[a] > 0) aviso("AUMENTO_DESPERDICADO");
      attr[a] = Math.min(TETO_ATRIBUTO, bruto);
      bon[a] = bonus(attr[a]);
    }
    s.atributos = attr;
    s.bonus = bon;
    s.atributos_criacao = criacao;

    // --- Caminho ---
    const cam = CAMINHOS[caminho];
    const [attrsHab, perCam, N, velCam] = cam || [[], [], 0, 0];
    let ah = e.atributo_habilidade;
    if (cam && attrsHab.length === 1 && !ah) ah = attrsHab[0];
    if (cam && !attrsHab.includes(ah)) aviso("ATRIBUTO_HABILIDADE_INVALIDO");
    const bah = attrsHab.includes(ah) ? (bon[ah] || 0) : 0;
    Object.assign(s, { N: N, vel_caminho: velCam, pericias_caminho: perCam.slice(),
      atributo_habilidade: ah == null ? null : ah });

    const bencaos = (e.bencaos || []).slice();
    const tem = new Set(bencaos.slice(0, div(L + 1, 2)));
    const cat = catalogoBencaos(catalogo);
    const acum = e.acumulos || {};
    const memoAtivo = !!e.memo_ativo && caminho === "A Recordação";
    const formaSinc = tem.has("Avatar da Recordação") && e.forma_avatar === "Sincronizada";

    // --- Equipamento ---
    const tier = tierReliquia(L);
    const rel = {};
    for (const slot of Object.keys(e.reliquias || {})) rel[slot] = RELIQUIAS[slot][tier - 1];
    s.reliquias = rel;
    const conjPecas = {};
    for (const info of Object.values(e.reliquias || {})) {
      const letra = (info || {}).conjunto;
      if (["A", "B", "C"].includes(letra)) conjPecas[letra] = (conjPecas[letra] || 0) + 1;
    }
    const conjBonus = { vel: 0, dano: 0, rd: 0, rolagem: 0 };
    const conjRolagens = [];
    const conjAtivos = {};
    for (const [letra, nP] of Object.entries(conjPecas)) {
      const info = (e.conjuntos || {})[letra] || {};
      conjAtivos[letra] = nP >= 4 ? 4 : nP >= 2 ? 2 : 0;
      if (nP >= 2) {
        const b2 = info.bonus2;
        if (b2 === "Velocidade +1") conjBonus.vel += 1;
        else if (b2 === "Dano +2") conjBonus.dano += 2;
        else if (b2 === "RD +1") conjBonus.rd += 1;
        else if (b2 === "Um tipo de rolagem +1") {
          conjBonus.rolagem += 1;
          if (info.rolagem) conjRolagens.push(info.rolagem);
        }
      }
    }
    if (conjBonus.dano > 3) {                                  // 25.3: no máximo +3 na mesma rolagem
      aviso("CONJUNTOS_DANO_ACIMA_DE_3");
      conjBonus.dano = 3;
    }
    s.conjuntos_rolagens = conjRolagens;
    s.conjuntos_pecas = conjPecas;
    s.conjuntos_ativos = conjAtivos;
    s.conjuntos_bonus = conjBonus;

    const coneIn = e.cone || {};
    let coneB = { alvo: null, numerico: 0, pv: 0 };
    if (coneIn.nivel) {
      let nc = coneIn.nivel;
      if (nc > fx) aviso("CONE_NIVEL_ACIMA");
      nc = Math.max(1, Math.min(5, nc));
      let [num, pv, modo] = CONE[nc];
      let sob = coneIn.sobreposicoes || 0;
      if (sob > fx) { aviso("SOBREPOSICOES_A_MAIS"); sob = fx; }
      const cabem = TETO_CONE_NUM - num;
      if (sob > cabem) { aviso("SOBREPOSICOES_ACIMA_DO_TETO"); sob = cabem; }
      num += sob;
      pv += SOBREPOSICAO_PV * sob;
      const alvo = coneIn.alvo == null ? null : coneIn.alvo;
      if (alvo === "PV máximos") coneB = { alvo: alvo, numerico: 0, pv: pv };
      else if (modo === "e") coneB = { alvo: alvo, numerico: num, pv: pv };
      else if (coneIn.escolha === "PV") coneB = { alvo: alvo, numerico: 0, pv: pv };
      else coneB = { alvo: alvo, numerico: num, pv: 0 };
    }
    coneB.qual = ["Um Teste de Resistência", "Uma Perícia"].includes(coneB.alvo)
      ? (coneIn.qual == null ? null : coneIn.qual) : null;
    s.cone = coneB;
    function coneEm(alvo, qual) {
      if (coneB.alvo !== alvo) return 0;
      if (["Um Teste de Resistência", "Uma Perícia"].includes(alvo) && coneB.qual !== (qual == null ? null : qual)) return 0;
      return coneB.numerico;
    }

    const ress = e.ressonancias || {};
    const ressOk = {};
    for (const [k, v] of Object.entries(ress)) if (s.ressonancias_liberadas.includes(k) && v) ressOk[k] = v;
    if (Object.entries(ress).some(([k, v]) => v && !s.ressonancias_liberadas.includes(k))) aviso("RESSONANCIA_ANTES_DO_NIVEL");

    // --- Estatísticas ---
    const V = bon.Vigor;
    let pvMax = 25 + 5 * N + 3 * V + (L - 1) * (5 + N + V);                         // 06.4
    pvMax += (rel["Cabeça"] || 0) + coneB.pv;
    if (tem.has("Corpo Imortal")) pvMax += 2 * L;
    if (formaSinc) pvMax += 2 * L;
    s.pv_max = pvMax;
    s.pv_ganho_vigor = L + 2;                                                      // 04.3
    s.descanso_curto = 2 * L + V;                                                  // 23.6
    s.morrendo_bonus = bon["Presença"];                                            // 23.4
    s.morrendo_vantagem = VANTAGEM_MORRENDO.includes(raca);
    s.morrendo_dt = 10;
    s.pode_ser_executado = raca !== "Xianzhouíta";
    s.esforco_max = raca === "Humano" ? 1 : 0;

    const arm = ARMADURAS[e.armadura];
    const [aDef, aVel, aRd, aPen, aEsq, aEsp] = arm || [0, 0, 0, 0, true, 0];
    let tempDef = 0;
    if (tem.has("Florescimento da Alma")) tempDef += Math.min(5, acum["Florescimento"] || 0);
    if (tem.has("Fragmentos do Eu Perdido") && memoAtivo && e.fragmento === "Guarda") tempDef += ef;
    const defesa = 10 + bon.Agilidade + aDef + (rel["Tronco"] || 0) + coneEm("Defesa") + (formaSinc ? 1 : 0);
    if (tempDef > s.teto_bonus) aviso("BONUS_TEMPORARIO_NO_TETO");
    s.defesa = defesa;
    s.defesa_com_temporarios = defesa + Math.min(s.teto_bonus, tempDef);
    if (aEsq) s.esquiva = defesa + ef;
    else { s.esquiva = null; aviso("ESQUIVA_PROIBIDA"); }
    let rd = aRd + coneEm("RD") + conjBonus.rd;
    if (tem.has("Pele de Pedra")) rd += 2;
    if (tem.has("Corpo Imortal")) rd += ef;
    if (rd > s.teto_rd) aviso("RD_NO_TETO");
    s.rd = Math.min(rd, s.teto_rd);
    const vel = 10 + bon.Agilidade + velCam + aVel + (rel["Botas"] || 0) + coneEm("Velocidade") +
      conjBonus.vel + (ressOk.I === "Velocidade +1" ? 1 : 0) + (tem.has("Avatar da Caça") ? 2 : 0);
    if (vel < 7 || vel > 25) aviso("VEL_FORA_7_25");
    s.velocidade = vel;
    s.barreira_max = caminho === "A Preservação" ? 3 * ef : null;

    // --- Perícias ---
    const sincCriacao = bonus(criacao.Sincronia);
    let permitidas = Math.max(2, 2 + sincCriacao);                                 // 04.5
    if (raca === "Humano") permitidas += 1;                                        // 05: Vocação Livre
    const escolhidas = (e.pericias_escolhidas || []).slice();
    s.pericias_permitidas = permitidas;
    if (escolhidas.length > permitidas) aviso("PERICIAS_A_MAIS");
    if (escolhidas.some((p) => perCam.includes(p))) aviso("PERICIA_DO_CAMINHO_ESCOLHIDA");
    const eficP = (e.eficacia_pericias || []).slice();
    if (eficP.length > pSlots) aviso("EFICACIA_PERICIAS_A_MAIS");
    const pericias = {};
    const comEf = new Set(perCam.concat(escolhidas.slice(0, permitidas)));
    for (const [nome, at0] of PERICIAS) {
      const at = at0 || e.sintonia || "Discernimento";
      const b = bon[at];
      const temEf = comEf.has(nome);
      const usaEfc = eficP.slice(0, pSlots).includes(nome) && temEf;
      if (eficP.includes(nome) && !temEf) aviso("EFICACIA_SEM_EFICIENCIA");
      const prof = usaEfc ? 2 * ef : temEf ? ef : 0;
      const pen = PERICIAS_PENALIZADAS_PESADA.includes(nome) ? aPen : 0;
      const extra = coneEm("Uma Perícia", nome) + Math.min(s.teto_bonus, contar(conjRolagens, nome));
      const total = b + prof + pen + extra;
      pericias[nome] = { atributo: at, bonus_atributo: b, eficiencia: temEf, eficacia: usaEfc,
        penalidade: pen, total: total, rolagem: rolagem(total),
        vantagem: (VANTAGEM_PERICIA[raca] || []).includes(nome) };
    }
    s.pericias = pericias;
    s.pericias_com_eficiencia = Object.values(pericias).filter((p) => p.eficiencia).length;

    // --- Testes de Resistência ---
    const eficTr = (e.eficacia_tr || []).slice();
    if (eficTr.length > trSlots) aviso("EFICACIA_TR_A_MAIS");
    const trs = {};
    for (const [nome, at] of TESTES_RESISTENCIA) {
      const prof = eficTr.slice(0, trSlots).includes(nome) ? 2 * ef : ef;
      const pen = nome === "Reflexos" ? aPen : 0;
      let temp = 0;
      if (tem.has("Cicatriz da Destruição") && (nome === "Força de Vontade" || nome === "Resistência Mental")) {
        temp += Math.min(5, acum["Marcas da Ruína"] || 0);
      }
      if (tem.has("Florescimento da Alma")) temp += Math.min(5, acum["Florescimento"] || 0);
      temp += contar(conjRolagens, nome);
      if (temp > s.teto_bonus) aviso("BONUS_TEMPORARIO_NO_TETO");
      const total = bon[at] + prof + pen + Math.min(s.teto_bonus, temp) + coneEm("Um Teste de Resistência", nome);
      trs[nome] = { atributo: at, total: total, rolagem: rolagem(total),
        vantagem: (VANTAGEM_TR[raca] || []).includes(nome),
        vantagem_condicional: (VANTAGEM_TR_CONDICIONAL[raca] || []).includes(nome) };
    }
    s.testes_resistencia = trs;

    // --- DT, ataques ---
    s.dt = 8 + bah + ef;                                                           // 02.2 / 22.3
    const pvAtual = e.pv_atual;
    let tempAtk = 0;
    if (tem.has("Instinto de Sobrevivência") && ehInt(pvAtual) && pvAtual * 3 <= pvMax) tempAtk += 2;
    if (memoAtivo) {
      const memo = e.memoespirito || {};
      if (memo.funcao === "Catalisador") tempAtk += 1;
      if ((memo.evolucoes || []).includes("Fusão de Memórias")) tempAtk += 1;
      if (tem.has("Memória Compartilhada")) tempAtk += 1;
    }
    tempAtk += contar(conjRolagens, "Teste de Ataque");
    if (tempAtk > s.teto_bonus) aviso("BONUS_TEMPORARIO_NO_TETO");
    tempAtk = Math.min(s.teto_bonus, tempAtk);
    s.ataque_habilidade = bah + ef + especializacao(L) + coneEm("Teste de Ataque") + tempAtk;
    const arma = e.arma || {};
    const catArma = ARMAS[arma.categoria];
    let ab = null;
    if (catArma) {
      let [face, extra, alcance, atAb, espArma] = catArma;
      atAb = atAb || (["Poder", "Agilidade"].includes(arma.atributo) ? arma.atributo : "Poder");
      const n = dadosAb(L) + extra + (formaSinc ? 1 : 0);
      if (arma.propriedade === "Alcance estendido") {
        alcance = ESCALA_DISTANCIA[Math.min(4, ESCALA_DISTANCIA.indexOf(alcance) + 1)];
      }
      const fixo = bon[atAb];
      const equip = (rel["Mãos"] || 0) + coneEm("Dano de Ataque Básico") + conjBonus.dano;
      ab = { atributo: atAb, ataque: bon[atAb] + ef + especializacao(L) + coneEm("Teste de Ataque") + tempAtk,
        n: n, face: face, dados: n + "d" + face, fixo: fixo,
        equip: equip, fixo_total: fixo + equip,
        texto: textoDano(n, face, fixo + equip), media: media(n, face) + fixo + equip,
        fraqueza: (n + 2) + "d" + face, texto_fraqueza: textoDano(n + 2, face, fixo + equip),
        resistencia: Math.max(1, n - 2) + "d" + face,
        rt: 1 + (arma.propriedade === "Peso de impacto" ? 1 : 0),
        alcance: alcance, elemento: arma.elemento || "Físico",
        critico: tem.has("Olho de Lan") ? "19-20" : "20", espaco: espArma };
      if (arma.propriedade === "Dissimulada") ab.espaco = 0.5;
    }
    s.ataque_basico = ab;

    // --- Habilidades ---
    const elem = e.elemento;
    const esfera = e.esfera_elemento && e.esfera_elemento === elem ? (rel["Esfera Planar"] || 0) : 0;
    const habs = [];
    const listaH = (e.habilidades || []).slice();
    if (listaH.length > HAB_CONHECIDAS[L - 1]) aviso("HABILIDADES_A_MAIS");
    const nmax = NIVEL_MAX_HAB[L - 1];
    let ress3Usada = false;
    for (const h of listaH) {
      let nv = h.nivel || 1;
      if (nv > nmax) aviso("HABILIDADE_NIVEL_ACIMA");
      nv = Math.max(1, Math.min(7, nv));
      if (h.ress3 && ressOk.III) {
        if (ress3Usada) aviso("RESSONANCIA_III_REPETIDA");
        else { ress3Usada = true; nv = nv < nmax ? Math.min(nmax, nv + 1) : nv; }
      }
      const [dn, df, cn, cf, ph, rt] = NIVEIS_HAB[nv];
      const tipo = h.tipo;
      const out = { nivel_efetivo: nv, ph: tipo === "Passiva" ? 0 : ph, rt: tipo === "Dano" ? rt : 0,
        alcance_max: ALCANCE_MAX_HAB[nv] || "Extrema" };
      const area = !!h.area;
      if (tipo === "Dano" || tipo === "Cura") {
        let n_ = tipo === "Dano" ? dn : cn;
        const f_ = tipo === "Dano" ? df : cf;
        if (area) n_ = Math.max(1, div(n_, 2));
        const fixo = bah + (tipo === "Dano" ? esfera + coneEm("Dano de Habilidade") : 0);
        Object.assign(out, { n: n_, face: f_, fixo: fixo, texto: textoDano(n_, f_, fixo), media: media(n_, f_) + fixo });
      }
      out.alvos = area ? (nv >= 6 ? 4 : 3) : 1;
      out.rolagem = h.resolucao === "Teste de Ataque" ? rolagem(s.ataque_habilidade)
        : h.resolucao === "Teste de Resistência" ? "DT " + s.dt : "";
      habs.push(out);
    }
    s.habilidades = habs;

    const ultIn = e.ultimate || {};
    const [eq, udn, udf, ucn, ucf] = ULTIMATE[fx];
    const ult = { equivalente: eq, rt: 5, custo: ressOk.IV === "Ultimate com 80 de Energia" ? 80 : 100 };
    if (ultIn.tipo === "Dano" || ultIn.tipo === "Cura") {
      let n_ = ultIn.tipo === "Dano" ? udn : ucn;
      const f_ = ultIn.tipo === "Dano" ? udf : ucf;
      const area = !!ultIn.area;
      if (area) n_ = Math.max(1, div(n_, 2));
      const fixo = bah + (ultIn.tipo === "Dano" ? esfera + coneEm("Dano de Ultimate") : 0);
      Object.assign(ult, { n: n_, face: f_, dados: n_ + "d" + f_, fixo: fixo,
        texto: textoDano(n_, f_, fixo), media: media(n_, f_) + fixo,
        alvos: area ? (eq >= 6 ? 4 : 3) : 1 });
    }
    s.ultimate = ult;

    // --- Quebra ---
    if (elem in QUEBRA) {
      const [qn, qf, qm] = QUEBRA[elem];
      s.quebra = { texto: textoDano(qn, qf, qm * ef), media: media(qn, qf) + qm * ef };
    } else {
      s.quebra = null;
    }

    // --- Bênçãos ---
    const slots = [];
    const vistos = new Set();
    bencaos.slice(0, 10).forEach((nome, k) => {
      const nivelSlot = 2 * k + 1;
      const info = { nivel_slot: nivelSlot, bencao: nome == null ? null : nome, liberado: L >= nivelSlot };
      if (nome) {
        const c = cat[nome];
        if (L < nivelSlot) aviso("BENCAO_EM_SLOT_FUTURO");
        if (c === undefined || c[0] !== caminho) aviso("BENCAO_DE_OUTRO_CAMINHO");
        else {
          info.tier = c[2];
          info.requisito = c[3];
          if (c[3] > nivelSlot) aviso("BENCAO_TIER_ACIMA_DO_SLOT");
        }
        if (vistos.has(nome)) aviso("BENCAO_REPETIDA");
        vistos.add(nome);
      }
      slots.push(info);
    });
    s.bencoes_slots = slots;
    if (tem.has("Pacto da Ruína")) {
      s.pacto_da_ruina = { custo_pv: 2 * L, bonus: ef, bonus_ferido: 2 * ef, limiar_pv: div(pvMax, 2) };
    }

    // --- Inventário ---
    const capInv = 10 + 2 * bon.Poder + (tem.has("Peso do Juramento") ? 2 : 0);
    let ocupado = (ab ? ab.espaco : 0) + aEsp;
    for (const i of e.inventario || []) ocupado += (i.espaco || 0) * (i.qtd == null ? 1 : i.qtd);
    s.capacidade = capInv;
    s.ocupado = ocupado;
    if (ocupado > 2 * capInv) aviso("IMOVEL");
    else if (ocupado > capInv) aviso("SOBRECARGA");

    // --- Memoespírito ---
    const memo = e.memoespirito;
    if (memo) {
      if (caminho !== "A Recordação") aviso("MEMO_FORA_DA_RECORDACAO");
      const pts = {};
      for (const a of ATRIBUTOS) pts[a] = (memo.pontos || {})[a] || 0;
      if (Object.values(pts).some((v) => v > 5)) aviso("MEMO_ATRIBUTO_ACIMA_5");
      const totalPts = 12 + div(L, 2);
      const gastos = Object.values(pts).reduce((x, y) => x + y, 0);
      if (gastos > totalPts) aviso("MEMO_PONTOS_A_MAIS");
      const menores = (memo.bonus_menores || []).slice();
      if (menores.length > 3 || new Set(menores).size !== menores.length) aviso("MEMO_BONUS_MENORES");
      const evol = (memo.evolucoes || []).slice();
      if (evol.length > [8, 14, 20].filter((n) => L >= n).length) aviso("MEMO_EVOLUCAO_ANTES_DO_NIVEL");
      if (new Set(evol).size !== evol.length) aviso("MEMO_EVOLUCAO_REPETIDA");
      const p = {};
      for (const a of ATRIBUTOS) p[a] = Math.min(5, pts[a]);
      const atk = memo.atributo_ataque || "Poder";
      let pvM = 8 * L + 3 * p.Vigor;
      if (memo.funcao === "Guardião") pvM += 3 * L;
      if (menores.includes("Resistência Espiritual")) pvM += 2 * L;
      if (tem.has("Ecos do Passado")) pvM += 4 * L;
      let defM = 10 + p.Agilidade + ef;
      let velM = 10 + p.Agilidade + velCam + (menores.includes("Velocidade Espiritual") ? 2 : 0);
      if (evol.includes("Memória Desperta")) {
        if (memo.memoria_desperta === "Velocidade") velM += 2;
        else defM += 2;
      }
      // 11.4 (v1.2, E17): a quantidade de dados vem da arma do dono; a face é sempre d6
      const nM = dadosAb(L) + (catArma ? catArma[1] : 0) + (evol.includes("Forma Completa") ? 1 : 0);
      const fixoM = p[atk] + (menores.includes("Força Espiritual") ? 2 : 0) + (tem.has("Ecos do Passado") ? bah : 0);
      const rtM = (L >= 11 ? 2 : 1) + (tem.has("Eternidade Recordada") ? 1 : 0);
      s.memo = { pontos_total: totalPts, pontos_gastos: gastos,
        pv: pvM, defesa: defM, velocidade: velM,
        ataque: bah + p[atk] + ef, n: nM, fixo: fixoM,
        texto: textoDano(nM, 6, fixoM), media: media(nM, 6) + fixoM,
        media_fraqueza: media(nM + 2, 6) + fixoM,
        rt: rtM, rd: menores.includes("Resistência Espiritual") ? 1 : 0,
        tr: Object.fromEntries(ATRIBUTOS.map((a) => [a, p[a] + ef])),
        predador_d8: memo.funcao === "Predador" };
    } else {
      s.memo = null;
    }

    s.avisos = av;
    return s;
  }

  const Motor = {
    calcular, AVISOS, ATRIBUTOS, RACAS, PERICIAS, TESTES_RESISTENCIA, CAMINHOS, ARMADURAS, ARMAS,
    ESCALA_DISTANCIA, NIVEIS_HAB, CONE, RELIQUIAS, NIVEIS_AUMENTO, ARRAY_OFICIAL, CUSTO_COMPRA,
    VERBA_COMPRA, HAB_CONHECIDAS, NIVEL_MAX_HAB, ULTIMATE, QUEBRA,
    eficiencia, faixa, tierReliquia, dadosAb, media, textoDano, rolagem, bonus,
  };
  if (typeof module === "object" && module.exports) module.exports = Motor;
  else raiz.Motor = Motor;
})(typeof globalThis !== "undefined" ? globalThis : this);
