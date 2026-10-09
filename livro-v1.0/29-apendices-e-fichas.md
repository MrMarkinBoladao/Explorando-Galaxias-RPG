# Capítulo 29 — Apêndices e fichas

Este capítulo não traz regra nova. Ele traz **as contas** que sustentam as regras e **os papéis** que você leva para a mesa.

Ele tem quatro partes:

1. O **apêndice de balanceamento** (29.1 a 29.6): de onde vem cada número do bestiário e do orçamento de encontro, aberto parcela por parcela, faixa por faixa.
2. O **exemplo completo de criação de personagem** (29.7), com cada conta feita à mão.
3. As **fichas** (29.8 a 29.11): personagem, Memoespírito, Trilha de Ação e Decisões da Mesa.
4. A **referência rápida de uma página** (29.12).

> **Para quem é o apêndice de balanceamento.** Para o Mestre que quer criar inimigo fora da tabela, para quem quer saber se uma Habilidade caseira está fora de escala, e para quem simplesmente não acredita num número e quer conferir. Nada aqui é necessário para jogar. Se você só quer jogar hoje, pule para 29.12.

---

## 29.1 O método do balanceamento

O critério é **um só** e vale em todas as cinco faixas:

> **Um combate típico termina em 3 a 5 Ciclos, com 4 Ciclos como centro de projeto.**

Todo número de inimigo deste livro saiu de quatro passos:

1. **Construir o personagem de referência** por faixa: array oficial, Raça somando no atributo principal, aumentos de Atributo gastos no principal até o teto, Eficiência da faixa, equipamento do tier da faixa, Habilidades no Nível máximo da faixa.
2. **Calcular o DPC** — o **Dano do grupo por Ciclo** — para um grupo de 4, parcela por parcela.
3. **Derivar o orçamento de PV do inimigo:** `PV do encontro = DPC × 4`, repartido em Comum (1/7), Elite (1/3) e Boss (85%).
4. **Derivar Defesa, dano do inimigo, Tenacidade, VEL e DTs** a partir das janelas-alvo.

Os níveis de referência de cada faixa são o **ponto médio**: **3, 7, 11, 15 e 19**.

### As premissas publicadas

Sem elas o DPC é uma afirmação; com elas, qualquer pessoa da mesa reproduz a conta. **Todas são consequência das regras, com uma exceção: a da Fraqueza, que depende de uma escolha sua e por isso é escrita como obrigação** (capítulo 27).

| Premissa | Valor travado |
|---|---|
| Tamanho do grupo | **4 jogadores**: 2 ofensivos, 1 de suporte, 1 de sustentação |
| Como os 4 turnos do Ciclo são gastos | **1 Habilidade** + **2 Ataques Básicos** + **1 turno sem dano direto** (cura, buff, remover condição), que alterna entre o suporte e a sustentação. Mais a **Ultimate do Ciclo**, que não gasta ação |
| Nível da Habilidade por Ciclo | O que a geração de PH sustenta (capítulo 16): Nível 2 · `0,75 × Nível 3 + 0,25 × Nível 2` · Nível 4 · `0,5 × Nível 6 + 0,25 × Nível 3` · `0,5 × Nível 7 + 0,25 × Nível 3` |
| Geração de PH | `2 Ataques Básicos × valor da faixa × taxa de acerto` — **condicionada ao acerto** |
| Ultimate | **1 por Ciclo no grupo**, na potência do Nível equivalente da faixa (capítulo 17) |
| Taxa de acerto | **70% contra Comum, 60% contra Elite, 55% contra Boss**, já com o suporte dentro. O DPC publicado usa o **perfil de Elite (60%)** |
| **Fraqueza** | A **Habilidade** e a **Ultimate** do Ciclo acertam Fraqueza, e **1 dos 2 Ataques Básicos** também: 3 das 4 ações agressivas, com +2 dados que **não** critam. **Isto é contrato de encontro, não sorte** |
| Esquiva | **1 ataque inimigo por Ciclo é Esquivado.** Acerto inimigo efetivo: 60% nos não Esquivados, 20% no Esquivado. Modelada no ataque de **menor dano** — o caso pior para o grupo |
| Área | O DPC é de **alvo único**. Contra 3 ou mais inimigos, uma Habilidade em área entrega cerca de **1,5 ×** isso |
| RD do inimigo | **0 / 2 / 4** (faixas 1-8), **0 / 3 / 6** (9-16), **0 / 4 / 8** (17-20), subtraída de **cada instância** |
| RD do personagem | **0**. Quem tem RD está acima do orçamento, e isso é margem a favor do grupo |
| Crítico | **5%** das rolagens, dobrando **só os dados base** |
| Redução de Tenacidade | **Condicionada ao acerto**, igual ao PH. Ataque que erra não tira Tenacidade |
| Tenacidade por tipo | **Boss = 2 ×** a redução efetiva do grupo por Ciclo · **Elite = 1 ×** · **Comum = 0,5 ×** |
| Cadência de Quebra | **1 a cada 2 Ciclos** contra Boss · **1 por Ciclo** contra Elite e contra Comum |
| Ações agressivas do inimigo | Comum **1** por turno · Elite **1,5** por Ciclo · Boss **2** por turno |
| Dano do inimigo por tipo | **Comum = 1/3 · Elite = 2/3 · Boss = 1** do dano por acerto da faixa |
| Janelas-alvo do inimigo | Acerto de **60%** contra a Defesa de referência, **70%** contra Armadura Leve, **55%** contra Pesada. Um personagem focado aguenta **4 a 7 acertos** |
| Orçamento e dano recebido | O **orçamento é de PV** (`DPC × 4`). O **dano recebido é verificado por composição**, e não é parte do orçamento |
| Attrition | **73% a 81%** dos PV restantes no fim de um combate típico; **51% a 64%** no fim do terceiro combate do dia |
| Testes de Resistência do grupo | Passam em **55% a 65%** com o atributo certo; em **35% a 45%** com o errado |

### O que o modelo deixa de fora, de propósito

Tudo nesta lista é **margem a favor dos jogadores**, e é por isso que o alvo é "3 a 5 Ciclos" e não "exatamente 4".

| Omissão declarada | Quanto vale |
|---|---|
| Buff de mais de um aliado na mesma rolagem | Limitado pelo teto de bônus somado (+3 a +5, capítulo 26) |
| **Memoespírito** | 15% a 25% do dano do dono: **DPC do grupo 5% a 8% acima** da referência numa mesa com Recordação |
| **Esforço** (só em mesas com Humano) | 1 rerrolagem por Descanso Longo, por Humano |
| Vantagem | Cerca de **+16 pontos percentuais** de acerto na rolagem em que sai |
| Acúmulos de Caminho e Efeito Condicional de Cone de Luz | Dentro do teto de bônus somado e do teto de dados adicionais |
| Condição **Quebrado** | +1 dado e -2 de Defesa do inimigo em metade dos Ciclos: cerca de **+6% de DPC** e +10 pontos percentuais de acerto |
| **Ressonância I** (nível 5+) | 1 Habilidade de Nível 3 ou menor grátis por combate, por personagem: ~**37** de DPC na faixa 17-20, ou 13% |
| **Ressonância IV** (nível 20) | Ultimate a 80 de Energia: **+25%** na parcela de Ultimate, ~+26 de DPC |
| Habilidades construídas na via de **Teste de Resistência** | `0,80 × dano` em vez de `0,60 × dano`: até **+25%** nas parcelas de Habilidade e de Ultimate |
| Bônus de **Esfera Planar** no tique de Dano Contínuo | Entre +2 e +8 por tique, duas vezes por Quebra. A parcela de Quebra abaixo é contada **sem** ele |

A **Esquiva não está nesta lista**, e isso é deliberado: ela é a única coisa que todo personagem tem de graça, todo turno, sem gastar recurso. Deixá-la de fora derrubava o dano recebido em um terço. Omissão que muda o resultado em um terço não é margem, é erro de modelo.

---

## 29.2 Âncoras do personagem de referência

**Orçamento de ataque.** O atacante de referência soma Atributo + Eficiência + Especialização de Combate + Bônus Maior de Cone de Luz. O suporte e a sustentação ficam **3 pontos abaixo** — eles investiram o Cone e o atributo em outra coisa.

| Faixa | Nível de referência | Atributo | Eficiência | Especialização | Cone de Luz | **Atacante** | Suporte / sustentação | **Ponto médio** |
|---|---|---|---|---|---|---|---|---|
| 1-4 | 3 | +5 | +2 | — | +1 | **+8** | +5 | **+6,5** |
| 5-8 | 7 | +5 | +4 | +1 | +1 | **+11** | +8 | **+9,5** |
| 9-12 | 11 | +5 | +5 | +2 | +2 | **+14** | +11 | **+12,5** |
| 13-16 | 15 | +5 | +6 | +2 | +2 | **+15** | +12 | **+13,5** |
| 17-20 | 19 | +5 | +8 | +3 | +3 | **+19** | +16 | **+17,5** |

**Defesa, com dispersão.** A escolha de armadura e de Agilidade produz uma faixa de 6 pontos. Esconder isso num número único seria mentir sobre quanto dano o personagem de Armadura Leve recebe.

> **Build de referência:** `10 + Bônus de Agilidade típico da faixa + Armadura Média (+5) + Tronco do tier`. O Bônus de Agilidade típico por faixa é **+0 / +2 / +4 / +4 / +5**.

| Faixa | **Defesa de referência** (Média) | Mais baixa realista (Leve) | Mais alta (Pesada, **sem Esquiva**) |
|---|---|---|---|
| 1-4 | **16** | 14 | 17 |
| 5-8 | **18** | 16 | 19 |
| 9-12 | **20** | 18 | 21 |
| 13-16 | **21** | 19 | 22 |
| 17-20 | **22** | 20 | 23 |

Contra o Teste de Ataque do inimigo (capítulo 28), isso dá **60% de acerto contra a referência, 70% contra Leve e 55% contra Pesada** nas cinco faixas. O personagem de Armadura Leve — tipicamente a **Caça**, que já tem o menor PV do jogo — é quem recebe 17% mais dano, e é exatamente **por ele** que existem a Esquiva, o Caminho de sustentação e a Reação Intervir.

**PV do grupo**, com Bônus de Vigor +2 (capítulo 06):

| Faixa | PV típico (N=4) | Mais frágil (Caça) | Mais resistente (Destruição) |
|---|---|---|---|
| 1-4 | 51-84 | 41-68 | 61-100 |
| 5-8 | 95-128 | 77-104 | 113-152 |
| 9-12 | 139-172 | 113-140 | 165-204 |
| 13-16 | 183-216 | 149-176 | 217-256 |
| 17-20 | 227-260 | 185-212 | 269-308 |

**Equipamento que entra nas contas:** Relíquia de **Mãos** no dano de Ataque Básico (+2 / +4 / +4 / +6 / +8 pelas cinco faixas) e **Esfera Planar** no dano de Habilidade e de Ultimate (os mesmos valores). As duas nunca somam na mesma rolagem (capítulo 25). Arma **Média** (d10) como referência, rolando **1 / 2 / 3 / 4 / 5 dados** pelas cinco faixas (capítulo 26).

---

## 29.3 O DPC aberto, faixa por faixa

Toda média abaixo é `número de dados × (lados + 1) ÷ 2`, arredondada para baixo — a regra do capítulo 02, sem exceção. Então `1d10 = 5`, `2d10 = 11`, `5d10 = 27`, `6d20 = 63`, `14d20 = 147`, `18d20 = 189`.

O cálculo é sempre o mesmo: **dados + atributo + equipamento**, mais os **+2 dados de Fraqueza** onde a premissa diz que a Fraqueza acerta, **menos a RD do Elite**, tudo **multiplicado pela taxa de acerto de 60%**.

### Faixa 1-4 (nível 3 · Eficiência +2 · arma 1d10 · Mãos e Esfera +2 · RD de Elite 2)

| Parcela | Conta | Resultado |
|---|---|---|
| Ataque Básico com Fraqueza | `5 + 5 + 2 = 12`; `+2d10 (11)` = 23; `-2` = 21; `× 0,60` | **12,6** |
| Ataque Básico neutro | `12 - 2 = 10`; `× 0,60` | **6,0** |
| Habilidade (Nível 2) | `27 + 5 + 2 = 34`; `+11` = 45; `-2` = 43; `× 0,60` | **25,8** |
| Ultimate (Nível equivalente 2) | `27 + 5 + 2 = 34`; `+11` = 45; `-2` = 43; `× 0,60` | **25,8** |
| Crítico (5%) | dados base no Ciclo `5 + 5 + 27 + 27 = 64`; `× 0,05` | **3,2** |
| Quebra ÷ 2 Ciclos | `(7 + 4) - 2 = 9`, mais Queimadura `(7 + 2) × 2 = 18`; total 27; `÷ 2` | **13,5** |
| | **Soma** | **86,9** |

**DPC publicado: 88.** A diferença de 1,1 ponto é o arredondamento das parcelas (19 + 26 + 26 + 3 + 14), e é a maior divergência das cinco faixas: **1,3%**, dentro da tolerância de 5%.

### Faixa 5-8 (nível 7 · Eficiência +4 · arma 2d10 · Mãos e Esfera +4 · RD de Elite 2)

| Parcela | Conta | Resultado |
|---|---|---|
| Ataque Básico com Fraqueza | `11 + 5 + 4 = 20`; `+11` = 31; `-2` = 29; `× 0,60` | **17,4** |
| Ataque Básico neutro | `20 - 2 = 18`; `× 0,60` | **10,8** |
| Habilidade (`0,75 × Nível 3 + 0,25 × Nível 2`) | Nível 3: `39 + 5 + 4 = 48`; `+2d12 (13)` = 61; `-2` = 59. Nível 2: `27 + 5 + 4 = 36`; `+11` = 47; `-2` = 45. `0,75 × 59 + 0,25 × 45 = 55,5`; `× 0,60` | **33,3** |
| Ultimate (Nível equivalente 3) | `39 + 5 + 4 = 48`; `+13` = 61; `-2` = 59; `× 0,60` | **35,4** |
| Crítico (5%) | `11 + 11 + 36 + 39 = 97`; `× 0,05` | **4,9** |
| Quebra ÷ 2 Ciclos | `(7 + 8) - 2 = 13`, mais Queimadura `(7 + 4) × 2 = 22`; total 35; `÷ 2` | **17,5** |
| | **Soma** | **119,3** |

**DPC publicado: 119.**

### Faixa 9-12 (nível 11 · Eficiência +5 · arma 3d10 · Mãos e Esfera +4 · RD de Elite 3)

| Parcela | Conta | Resultado |
|---|---|---|
| Ataque Básico com Fraqueza | `16 + 5 + 4 = 25`; `+11` = 36; `-3` = 33; `× 0,60` | **19,8** |
| Ataque Básico neutro | `25 - 3 = 22`; `× 0,60` | **13,2** |
| Habilidade (Nível 4) | `63 + 5 + 4 = 72`; `+2d20 (21)` = 93; `-3` = 90; `× 0,60` | **54,0** |
| Ultimate (Nível equivalente 4) | `63 + 5 + 4 = 72`; `+21` = 93; `-3` = 90; `× 0,60` | **54,0** |
| Crítico (5%) | `16 + 16 + 63 + 63 = 158`; `× 0,05` | **7,9** |
| Quebra ÷ 2 Ciclos | `(7 + 10) - 3 = 14`, mais Queimadura `(7 + 5) × 2 = 24`; total 38; `÷ 2` | **19,0** |
| | **Soma** | **167,9** |

**DPC publicado: 168.** Repare que a Habilidade e a Ultimate empatam: nesta faixa o Nível equivalente da Ultimate **é** o Nível máximo de Habilidade. O desempate só acontece a partir da faixa 13-16.

### Faixa 13-16 (nível 15 · Eficiência +6 · arma 4d10 · Mãos e Esfera +6 · RD de Elite 3)

| Parcela | Conta | Resultado |
|---|---|---|
| Ataque Básico com Fraqueza | `22 + 5 + 6 = 33`; `+11` = 44; `-3` = 41; `× 0,60` | **24,6** |
| Ataque Básico neutro | `33 - 3 = 30`; `× 0,60` | **18,0** |
| Habilidade (`0,5 × Nível 6 + 0,25 × Nível 3`) | Nível 6: `147 + 5 + 6 = 158`; `+21` = 179; `-3` = 176. Nível 3: `39 + 5 + 6 = 50`; `+13` = 63; `-3` = 60. `0,5 × 176 + 0,25 × 60 = 103`; `× 0,60` | **61,8** |
| Ultimate (Nível equivalente 5) | `105 + 5 + 6 = 116`; `+21` = 137; `-3` = 134; `× 0,60` | **80,4** |
| Crítico (5%) | `22 + 22 + (0,5 × 147 + 0,25 × 39) + 105 = 232,25`; `× 0,05` | **11,6** |
| Quebra ÷ 2 Ciclos | `(7 + 12) - 3 = 16`, mais Queimadura `(7 + 6) × 2 = 26`; total 42; `÷ 2` | **21,0** |
| | **Soma** | **217,4** |

**DPC publicado: 218.**

### Faixa 17-20 (nível 19 · Eficiência +8 · arma 5d10 · Mãos e Esfera +8 · RD de Elite 4)

| Parcela | Conta | Resultado |
|---|---|---|
| Ataque Básico com Fraqueza | `27 + 5 + 8 = 40`; `+11` = 51; `-4` = 47; `× 0,60` | **28,2** |
| Ataque Básico neutro | `40 - 4 = 36`; `× 0,60` | **21,6** |
| Habilidade (`0,5 × Nível 7 + 0,25 × Nível 3`) | Nível 7: `189 + 5 + 8 = 202`; `+21` = 223; `-4` = 219. Nível 3: `39 + 5 + 8 = 52`; `+13` = 65; `-4` = 61. `0,5 × 219 + 0,25 × 61 = 124,75`; `× 0,60` | **74,9** |
| Ultimate (Nível equivalente 6) | `147 + 5 + 8 = 160`; `+21` = 181; `-4` = 177; `× 0,60` | **106,2** |
| Crítico (5%) | `27 + 27 + (0,5 × 189 + 0,25 × 39) + 147 = 305,25`; `× 0,05` | **15,3** |
| Quebra ÷ 2 Ciclos | `(7 + 16) - 4 = 19`, mais Queimadura `(7 + 8) × 2 = 30`; total 49; `÷ 2` | **24,5** |
| | **Soma** | **270,7** |

**DPC publicado: 271.**

### O resumo das cinco faixas

| Faixa | 2 Ataques Básicos | Habilidade | Ultimate | Crítico | Quebra ÷ 2 | **DPC de referência** |
|---|---|---|---|---|---|---|
| **1-4** | 19 | 26 | 26 | 3 | 14 | **88** |
| **5-8** | 28 | 33 | 35 | 5 | 18 | **119** |
| **9-12** | 33 | 54 | 54 | 8 | 19 | **168** |
| **13-16** | 43 | 62 | 80 | 12 | 21 | **218** |
| **17-20** | 50 | 75 | 106 | 15 | 25 | **271** |

> **Por quê a curva do DPC é mais suave que a curva de dano.** Entre a faixa 1-4 e a 17-20, o dano de **uma** Habilidade multiplica por 9 (21 → 189), mas o DPC só multiplica por 3. O freio é o **custo em PH**: quanto maior o Nível da Habilidade, menos vezes por combate ela sai. Esse é o mecanismo que mantém o combate em 4 Ciclos em todas as faixas sem precisar de Boss com milhares de PV — e é por isso que a economia de PH não é detalhe de sabor, é a espinha do balanceamento.

### Os três DPCs: referência, Elite puro e Boss puro

O DPC publicado é um **DPC de referência**, e isso é decisão, não descuido: as parcelas de acerto e RD são do perfil de **Elite** (60%, o caso médio), mas a parcela de Quebra usa a cadência do perfil de **Boss** (1 a cada 2 Ciclos), porque é o Boss que dimensiona 85% do orçamento e é contra ele que o alvo de 3 a 5 Ciclos é verificado.

As duas pontas, calculadas do mesmo jeito:

| Faixa | **DPC de referência** | **DPC puro de Elite** (Quebra todo Ciclo) | **DPC puro de Boss** (acerto 55%, RD de Boss, 4 Fraquezas) |
|---|---|---|---|
| 1-4 | 88 | **100** | **82** |
| 5-8 | 119 | **137** | **112** |
| 9-12 | 168 | **187** | **154** |
| 13-16 | 218 | **238** | **200** |
| 17-20 | 271 | **295** | **247** |

- **Contra Elite** a Tenacidade mais baixa faz a Quebra sair quase todo Ciclo: a parcela de Quebra dobra e o DPC sobe cerca de 11%.
- **Contra Boss** o acerto cai para 55% e a RD sobe, mas as **4 Fraquezas** do Boss fazem os dois Ataques Básicos acertarem Fraqueza em vez de um só. O resultado líquido é cerca de 9% abaixo da referência.

> **Uma divergência de arredondamento, declarada.** O capítulo 28 cita "cerca de 83" para o DPC puro de Boss da faixa 1-4; a conta aberta acima dá **81,7**, publicada como 82. São **1,6%** de diferença, e as duas levam ao mesmo resultado de mesa: `305 ÷ 82` e `305 ÷ 83` dão **3,7 Ciclos**.

É o **DPC puro de Boss** que verifica o alvo de Ciclos, e é ele que aparece nas três simulações de 29.5.

### A parcela de Quebra nas duas versões de Elemento

As contas acima usam **Fogo**, que produz **Queimadura**. **Físico** produz **Sangramento**, e Sangramento é porcentagem de PV com teto — ou seja, ele **depende do alvo**. Os dois têm o mesmo Dano de Quebra (`2d6 + 2 × Eficiência`); o que muda é o contínuo.

Contra o **Elite** de cada faixa:

| Faixa | Dano de Quebra (menos RD) | Queimadura (2 turnos) | **Total Fogo** | Sangramento (2 turnos, 5% dos PV com teto `3 × Eficiência`) | **Total Físico** |
|---|---|---|---|---|---|
| 1-4 | 9 | 18 | **27** → 13,5/Ciclo | `5% de 120 = 6` (teto 6) → 12 | **21** → 10,5/Ciclo |
| 5-8 | 13 | 22 | **35** → 17,5/Ciclo | `5% de 160 = 8` → 16 | **29** → 14,5/Ciclo |
| 9-12 | 14 | 24 | **38** → 19,0/Ciclo | `5% de 225 = 11` → 22 | **36** → 18,0/Ciclo |
| 13-16 | 16 | 26 | **42** → 21,0/Ciclo | `5% de 295 = 14` → 28 | **44** → 22,0/Ciclo |
| 17-20 | 19 | 30 | **49** → 24,5/Ciclo | `5% de 365 = 18` → 36 | **55** → 27,5/Ciclo |

**A leitura que importa:** Fogo é melhor nas faixas baixas e Físico nas altas, e a virada acontece na faixa 13-16. Contra **Boss**, o Físico é ainda melhor — `5% de 935 = 46`, cortado pelo teto em **24** por turno, ou 48 em dois turnos, contra os 30 da Queimadura. A escolha de Elemento tem consequência mecânica real, e ela não está na descrição bonita: está aqui.

> O Dano de Quebra **sofre RD**; o Dano Contínuo **ignora RD** (capítulos 18 e 20). É por isso que a coluna da esquerda leva desconto e as duas colunas de contínuo não.

---

## 29.4 De onde vêm as âncoras do inimigo

A tabela de âncoras do capítulo 28 não foi escolhida a dedo. Cada coluna dela é uma conta.

### PV: `DPC × 4`, repartido

| Faixa | DPC | Orçamento (`× 4`) | Comum (1/7) | Elite (1/3) | Boss (85%) |
|---|---|---|---|---|---|
| 1-4 | 88 | 352 | 50 → **50** | 117 → **120** | 299 → **305** |
| 5-8 | 119 | 476 | 68 → **70** | 159 → **160** | 405 → **410** |
| 9-12 | 168 | 672 | 96 → **95** | 224 → **225** | 571 → **580** |
| 13-16 | 218 | 872 | 125 → **125** | 291 → **295** | 741 → **750** |
| 17-20 | 271 | 1.084 | 155 → **155** | 361 → **365** | 921 → **935** |

Os valores publicados são o derivado **arredondado para número legível**, e todos ficam a menos de 3% do derivado. A maior divergência é o Elite da faixa 1-4: **120 publicado contra 117 derivado**, 2,6%. Ela está escrita aqui de propósito — um orçamento cuja tolerância é 5% não vale uma revisão de 15 células para ganhar 2%.

### Tenacidade: três fatores, nesta ordem

Este é o número que mais confunde, porque ele é **pequeno** e parece baixo demais. Ele é pequeno porque já conta que boa parte dos ataques do grupo **erra**.

1. **Redução bruta do grupo por Ciclo**, pelo mix de ações: `1 + 1` (os dois Ataques Básicos) `+` o Nível da Habilidade que o PH sustenta `+ 5` (Ultimate).
2. **Taxa de acerto do perfil** — a Redução de Tenacidade é condicionada ao acerto.
3. **Multiplicador por tipo:** Comum `0,5 ×`, Elite `1 ×`, Boss `2 ×`.

| | 1-4 | 5-8 | 9-12 | 13-16 | 17-20 |
|---|---|---|---|---|---|
| Redução bruta do grupo | 9 | 9,75 | 11 | 10,75 | 11,25 |
| Comum: `× 0,70 × 0,5` | 3,2 | 3,4 | 3,9 | 3,8 | 3,9 |
| Elite: `× 0,60 × 1` | 5,4 | 5,9 | 6,6 | 6,5 | 6,8 |
| Boss: `× 0,55 × 2` | 9,9 | 10,7 | 12,1 | 11,8 | 12,4 |
| **Publicado (C / E / B)** | **3 / 5 / 10** | **3 / 6 / 11** | **4 / 7 / 12** | **4 / 6 / 12** | **4 / 7 / 13** |

**A cadência de Quebra sai verdadeira da própria tabela.** Dividindo a Tenacidade publicada pela redução **efetiva** por Ciclo (bruta × taxa de acerto do perfil):

| Faixa | Boss: Tenacidade ÷ redução efetiva | Elite | Comum |
|---|---|---|---|
| 1-4 | `10 ÷ 4,95` = **2,0 Ciclos** | `5 ÷ 5,4` = **0,9** | `3 ÷ 6,3` = **0,5** |
| 5-8 | `11 ÷ 5,36` = **2,1** | `6 ÷ 5,85` = **1,0** | `3 ÷ 6,8` = **0,4** |
| 9-12 | `12 ÷ 6,05` = **2,0** | `7 ÷ 6,60` = **1,1** | `4 ÷ 7,7` = **0,5** |
| 13-16 | `12 ÷ 5,91` = **2,0** | `6 ÷ 6,45` = **0,9** | `4 ÷ 7,5` = **0,5** |
| 17-20 | `13 ÷ 6,19` = **2,1** | `7 ÷ 6,75` = **1,0** | `4 ÷ 7,9` = **0,5** |

Boss a cada **2 Ciclos**, Elite **quase todo Ciclo**, Comum no **primeiro ataque sério** que receber. É exatamente a cadência que o capítulo 28 promete, e ela reproduz a menos de 5% nas cinco faixas.

Dois desvios de arredondamento merecem estar escritos: o **Comum é um pouco mais frágil** que o derivado nas faixas altas (4 contra 3,9), de propósito — um Comum existe para sofrer Quebra, e a Quebra é o que faz um pelotão parecer um pelotão. E o **Boss da faixa 17-20 é um pouco mais duro** (13 contra 12,4), o que lhe dá meio Ciclo a mais de barra, também de propósito: é o inimigo que fecha a campanha.

### Dano por acerto: um por tipo

Com o Boss como âncora (é ele que calibra a Defesa do personagem e as pancadas até Morrendo) e a repartição `Comum = 1/3`, `Elite = 2/3`:

| Faixa | Boss (âncora) | Elite = 2/3 | Comum = 1/3 |
|---|---|---|---|
| 1-4 | 10 | **7** | **3** |
| 5-8 | 20 | **13** | **7** |
| 9-12 | 28 | **19** | **9** |
| 13-16 | 36 | **24** | **12** |
| 17-20 | 48 | **32** | **16** |

**Quantas pancadas um personagem focado aguenta**, dividindo o PV pelo dano por acerto do Boss da faixa:

| Faixa | Mais frágil, no começo da faixa | Mais resistente, no fim da faixa |
|---|---|---|
| 1-4 | Caça nível 1: `41 ÷ 10` = **4,1** | Destruição nível 4: `100 ÷ 10` = **10,0** |
| 5-8 | Caça nível 5: `77 ÷ 20` = **3,9** | Destruição nível 8: `152 ÷ 20` = **7,6** |
| 9-12 | Caça nível 9: `113 ÷ 28` = **4,0** | Destruição nível 12: `204 ÷ 28` = **7,3** |
| 13-16 | Caça nível 13: `149 ÷ 36` = **4,1** | Destruição nível 16: `256 ÷ 36` = **7,1** |
| 17-20 | Caça nível 17: `185 ÷ 48` = **3,9** | Destruição nível 20: `308 ÷ 48` = **6,4** |

A janela publicada é **4 a 7 acertos**, e ela vale em quatro das cinco faixas. **A exceção declarada é a ponta resistente da faixa 1-4: 10 acertos.** A razão é a forma da curva de PV dentro da faixa: o dano por acerto do Boss é **constante nos quatro níveis** da faixa, mas o PV de uma Destruição vai de **61 para 100** do nível 1 ao 4 — **64% de crescimento dentro da própria faixa**, contra 14% na faixa 17-20 (269 para 308). O efeito de mesa é bom — o tanque de nível 4 é difícil de derrubar — e o Mestre que quiser pressionar um personagem da Destruição no fim dessa faixa precisa de dois inimigos, não de um.

### Defesa, VEL, DT dos efeitos e Teste de Resistência do inimigo

- **Ataque do inimigo** foi resolvido de trás para frente: ele precisa acertar **60%** contra a Defesa de referência de 29.2 nas cinco faixas, ou seja precisar de **9 ou mais** no d20. É por isso que o ataque da faixa 17-20 é **+13** e não +14.
- **Defesa do inimigo** foi resolvida contra o ponto médio de ataque do grupo: **70% contra Comum, 60% contra Elite, 55% contra Boss**, nas cinco faixas, sem exceção.
- **VEL** foi calibrada contra a faixa de VEL de personagem do capítulo 19, com uma regra de projeto: **a Caça equipada age antes de todo Comum e Elite da faixa dela** e disputa a primeira casa com o Boss. Um Boss de faixa 17-20 tem VEL 19; uma Caça de nível 19 com Agilidade 20, Caminho +4 e Botas IV chega a **24**. A promessa do Caminho é verdadeira na mesa, não só na descrição.
- **DT dos efeitos** é `8 + atributo plausível + Eficiência da faixa`, resolvida para entregar a janela de Testes de Resistência da premissa: o grupo passa em **55% a 65%** com o atributo certo e em **35% a 45%** com o errado.
- **Teste de Resistência do inimigo** é `Eficiência da faixa −1 / Eficiência / Eficiência +1`. Contra a DT de Habilidade do personagem de referência (`8 + 5 + Eficiência` = **15 / 17 / 18 / 19 / 21**), o inimigo falha em **65% / 60% / 55%** conforme o tipo — **a mesma janela do acerto do grupo**. As duas vias de resolução do capítulo 04 têm a mesma chance de passar; o que muda entre elas é só o que acontece no sucesso do alvo.

### Fichas de inimigo de referência, preenchidas pelas âncoras

Estas não são bichos — são as **linhas da tabela vestidas de ficha**, uma por tipo e por faixa. Toda ficha nominal do capítulo 28 saiu de uma destas quinze linhas.

| Faixa | Tipo | PV | Defesa | RD | Tenacidade | VEL | Ataque | Dano por acerto | DT dos efeitos | Teste de Resistência | Fraquezas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-4 | Comum | 50 | 13 | 0 | 3 | 11 | +7 | `1d6` · 3 | 12 | +1 | 1-2 |
| 1-4 | Elite | 120 | 15 | 2 | 5 | 12 | +7 | `2d6` · 7 | 13 | +2 | 3 |
| 1-4 | Boss | 305 | 16 | 4 | 10 | 13 | +7 | `3d6` · 10 | 14 | +3 | 4 |
| 5-8 | Comum | 70 | 16 | 0 | 3 | 12 | +9 | `2d6` · 7 | 14 | +3 | 1-2 |
| 5-8 | Elite | 160 | 18 | 2 | 6 | 13 | +9 | `3d8` · 13 | 15 | +4 | 3 |
| 5-8 | Boss | 410 | 19 | 4 | 11 | 15 | +9 | `4d8 + 2` · 20 | 16 | +5 | 4 |
| 9-12 | Comum | 95 | 19 | 0 | 4 | 13 | +11 | `2d8` · 9 | 16 | +4 | 1-2 |
| 9-12 | Elite | 225 | 21 | 3 | 7 | 15 | +11 | `4d8 + 1` · 19 | 17 | +5 | 3 |
| 9-12 | Boss | 580 | 22 | 6 | 12 | 16 | +11 | `5d10 + 1` · 28 | 18 | +6 | 4 |
| 13-16 | Comum | 125 | 20 | 0 | 4 | 14 | +12 | `3d6 + 2` · 12 | 17 | +5 | 1-2 |
| 13-16 | Elite | 295 | 22 | 3 | 6 | 16 | +12 | `4d10 + 2` · 24 | 18 | +6 | 3 |
| 13-16 | Boss | 750 | 23 | 6 | 12 | 18 | +12 | `6d10 + 3` · 36 | 19 | +7 | 4 |
| 17-20 | Comum | 155 | 24 | 0 | 4 | 15 | +13 | `3d8 + 3` · 16 | 19 | +7 | 1-2 |
| 17-20 | Elite | 365 | 26 | 4 | 7 | 17 | +13 | `5d12` · 32 | 20 | +8 | 3 |
| 17-20 | Boss | 935 | 27 | 8 | 13 | 19 | +13 | `7d12 + 3` · 48 | 21 | +9 | 4 |

Faltam dois campos para a ficha ficar completa, e os dois são **seus**: o **nome** e **quais** Fraquezas (a quantidade está na tabela; a escolha cumpre o contrato de encontro). As **ações especiais** seguem a régua do capítulo 28.

---

## 29.5 Os três combates de referência, Ciclo por Ciclo

Composição de referência: **1 Boss + 1 Comum**, que é o encontro que gasta o orçamento inteiro. O dano do grupo é o **DPC puro de Boss** de 29.3 — o mais baixo dos três, para a simulação ser teto e não promessa.

O dano recebido pelo grupo sai da premissa de Esquiva: são **3 ataques inimigos por Ciclo** (Boss 2 + Comum 1) e **1 deles é Esquivado**, logo `0,60 + 0,60 + 0,20` = **1,4 acerto por Ciclo**. O modelo conta as três pancadas no **dano por acerto do Boss** — inclusive a do Comum, que bate um terço disso. É deliberadamente pessimista: a attrition publicada é **teto**, não média.

### Combate A — faixa 1-4 (nível 3)

Boss 305 PV · Tenacidade 10 · RD 4 · Defesa 16 — Comum 50 PV · Tenacidade 3 · RD 0 · Defesa 13
Grupo: 4 personagens, **292 PV** · DPC puro de Boss **82** · dano recebido **14 por Ciclo**

| Ciclo | Dano no Boss | PV do Boss | Tenacidade do Boss | Evento | PV do grupo |
|---|---|---|---|---|---|
| 1 | 82 | 223 | 10 → 5,1 | Comum sofre Quebra no primeiro ataque sério | 278 (95%) |
| 2 | 82 | 141 | 5,1 → 0,1 | **Boss sofre Quebra** no fim do Ciclo | 264 (90%) |
| 3 | 82 | 59 | restaura 10 → 5,1 | Boss **Quebrado**: +1 dado para todos, -2 de Defesa | 250 (86%) |
| 4 | 59 | **0** | — | Boss cai a **0,7 do Ciclo 4** | 236 (**81%**) |

**Resolução: 3,7 Ciclos** (`305 ÷ 82`). O grupo termina com **81%** dos PV.

E o Comum? Os quatro Ciclos de DPC puro de Boss somam 328, contra **355** de PV no encontro inteiro. A diferença de 27 vem do próprio Comum: contra ele o acerto é **70%** e a RD é **0**, então os mesmos dois Ataques Básicos entregam 24,5 em vez de 20,9 por Ciclo, e ele passa boa parte do combate **Quebrado**. É margem que o orçamento não conta e que a mesa recebe.

### Combate B — faixa 9-12 (nível 11)

Boss 580 PV · Tenacidade 12 · RD 6 · Defesa 22 — Comum 95 PV · Tenacidade 4 · RD 0 · Defesa 19
Grupo: **644 PV** · DPC puro de Boss **154** · dano recebido **39,2 por Ciclo**

| Ciclo | Dano no Boss | PV do Boss | Tenacidade do Boss | Evento | PV do grupo |
|---|---|---|---|---|---|
| 1 | 154 | 426 | 12 → 6,0 | Habilidade de Nível 4 arranca 4 sozinha | 605 (94%) |
| 2 | 154 | 272 | 6,0 → 0 | **Boss sofre Quebra** no fim do Ciclo | 566 (88%) |
| 3 | 154 | 118 | restaura 12 → 6,0 | Boss **Quebrado**; o grupo gasta o que tem | 526 (82%) |
| 4 | 118 | **0** | — | Boss cai a **0,8 do Ciclo 4** | 487 (**76%**) |

**Resolução: 3,8 Ciclos** (`580 ÷ 154`). O grupo termina com **76%**.

### Combate C — faixa 17-20 (nível 19)

Boss 935 PV · Tenacidade 13 · RD 8 · Defesa 27 — Comum 155 PV · Tenacidade 4 · RD 0 · Defesa 24
Grupo: **996 PV** · DPC puro de Boss **247** · dano recebido **67,2 por Ciclo**

| Ciclo | Dano no Boss | PV do Boss | Tenacidade do Boss | Evento | PV do grupo |
|---|---|---|---|---|---|
| 1 | 247 | 688 | 13 → 6,8 | Ultimate sai: 95 dos 247 vêm dela | 929 (93%) |
| 2 | 247 | 441 | 6,8 → 0,6 | Falta pouco: a Quebra cai no começo do Ciclo 3 | 862 (87%) |
| 3 | 247 | 194 | **Quebra** · restaura 13 → 6,8 | Boss **Quebrado** no meio do Ciclo | 794 (80%) |
| 4 | 194 | **0** | — | Boss cai a **0,8 do Ciclo 4** | 727 (**73%**) |

**Resolução: 3,8 Ciclos** (`935 ÷ 247`). O grupo termina com **73%** — o piso da janela publicada, e é esperado que seja aqui: é a faixa em que o Boss bate mais forte em relação ao PV do grupo.

### As três janelas, verificadas

| Verificação | Alvo | Faixa 1-4 | 9-12 | 17-20 | Resultado |
|---|---|---|---|---|---|
| Ciclos até a resolução | 3 a 5 | 3,7 | 3,8 | 3,8 | **passa** |
| Attrition no fim do combate | 70% a 85% restantes | 81% | 76% | 73% | **passa** |
| Divergência do DPC publicado | abaixo de 5% | 1,3% | 0,1% | 0,1% | **passa** |

As faixas 5-8 e 13-16 reproduzem o mesmo padrão: **3,7 e 3,7 Ciclos** (`410 ÷ 112` e `750 ÷ 200`), com **76% e 75%** de PV restante.

---

## 29.6 O dia, o foco e o pelotão

Três cenários que a média de um combate esconde. Eles são a razão de o capítulo 27 insistir em quatro coisas que parecem opcionais e não são.

### O dia de referência: três combates e dois Descansos Curtos

O Descanso Curto devolve `(2 × nível) + Bônus de Vigor` de PV por personagem, duas vezes por dia (capítulo 23). Para o grupo de 4:

| Faixa | PV do grupo | Dano por combate | Devolvido por Descanso Curto (grupo) | Fim do 1º | Fim do 2º | **Fim do 3º** |
|---|---|---|---|---|---|---|
| 1-4 | 292 | 56 | 32 | 236 (81%) | 212 (73%) | **188 (64%)** |
| 5-8 | 468 | 112 | 64 | 356 (76%) | 308 (66%) | **260 (56%)** |
| 9-12 | 644 | 157 | 96 | 487 (76%) | 426 (66%) | **365 (57%)** |
| 13-16 | 820 | 202 | 128 | 618 (75%) | 544 (66%) | **470 (57%)** |
| 17-20 | 996 | 269 | 160 | 727 (73%) | 618 (62%) | **509 (51%)** |

> **Janela publicada: o grupo sai do terceiro combate do dia com 51% a 64% dos PV.** Os três combates somam **57% a 81%** do PV total do grupo; os dois Descansos Curtos devolvem **22%** na faixa 1-4 e **32%** na 17-20.

É aqui que a conta vira, e não no primeiro combate. **Um quarto combate no mesmo dia, sem Descanso Longo, é uma decisão de risco** — não é continuação da sessão.

### O cenário de foco

O inimigo escolhe o alvo, e a Esquiva protege **um** ataque de **um** personagem por Ciclo. Um Boss que decide concentrar os dois ataques do turno em quem tem menos PV:

| | Conta | Resultado |
|---|---|---|
| Caça de nível 19, Armadura Leve | 203 PV, Defesa 20, acerto inimigo **70%** | — |
| Dano por acerto do Boss | 48 | **4,2 acertos** até 0 PV |
| Se o Boss acerta os dois ataques | `2 × 48` por Ciclo | **2,1 Ciclos** |
| Com 70% de acerto e 1 Esquiva por Ciclo | `(0,70 + 0,20) × 48 = 43,2` por Ciclo | **4,7 Ciclos** |

**O número que o Mestre precisa é o pior caso: 2 Ciclos.** Um Boss focado derruba o personagem mais frágil do grupo antes do terceiro Ciclo, e a média do grupo nem percebe — ela continua dizendo 73%. É por isso que existe Caminho de sustentação, é por isso que Intervir existe, e é por isso que o capítulo 27 pede que você escolha o alvo **na ficção** e não no PV mais baixo da mesa.

### O encontro de 7 Comuns

Pela regra de área (capítulo 16), uma Habilidade em área rola **metade dos dados** e pega **até 3 alvos** (4 nos Níveis 6 e 7). Contra um pelotão, isso entrega cerca de **1,5 ×** o dano de alvo único:

| Faixa | PV do pelotão (7 Comuns) | DPC em área (`1,5 × DPC`) | **Ciclos** |
|---|---|---|---|
| 1-4 | 350 | 132 | **2,7** |
| 9-12 | 665 | 252 | **2,6** |
| 17-20 | 1.085 | 407 | **2,7** |

**Encontros de 3 ou mais inimigos resolvem em 2 a 3 Ciclos, e isso é correto** — não é desbalanceamento. É o preço de colocar sete alvos na frente de uma Habilidade em área, e é a razão de existir o Caminho da Erudição. Na prática o pelotão cai ainda mais rápido: contra Comum o acerto é 70% e a RD é 0, e os 2,6 Ciclos acima usam a taxa de 60% do perfil de Elite.

### Então por quê existe um Caminho de sustentação?

Porque a média de um combate é a métrica errada para decidir isso. São quatro razões, e nenhuma delas aparece na tabela de attrition:

1. **Foco.** Um personagem que vira alvo cai em 2 Ciclos, como acabou de ser mostrado.
2. **Dano Contínuo.** Ele **ignora RD**, não admite Esquiva e é a fonte que mais cresce nas faixas altas. Nada na ficha defende contra ele a não ser cura.
3. **Ações especiais de Boss.** A premissa conta "2 ataques por turno **ou** 1 ataque + 1 ação especial". A ação especial é o pico que a média esconde, e é o momento em que o grupo precisa de uma Ultimate de cura pronta.
4. **O dia, não o combate.** O relógio real é a cadeia de três combates da tabela acima, não o primeiro deles.

---

## 29.7 Exemplo completo de criação de personagem

Os doze passos do capítulo 03, feitos de verdade, com **todas as contas abertas**. A personagem é a **Nadir**, que aparece como exemplo em meia dúzia de capítulos deste livro — aqui está de onde ela veio.

### Passo 1 — Conceito e Propósito de Vida

*Quem é:* uma mecânica de doca orbital que foi expulsa da Aliança por consertar a nave errada.
*O que quer:* **encontrar a doca que a expulsou e provar que o acidente não foi culpa dela.**

Isso é um **Propósito de Vida** válido pelos dois pedidos do capítulo 03: é alcançável em campanha e envolve outras pessoas — tem gente com nome no fim dessa linha.

### Passo 2 — Raça

**Humana.** O bônus é **+2 em um Atributo ou +1 em dois**; ela vai de +2, guardado para o passo 4.
Traço: **Força de Vontade**, que concede o **Esforço** — 1 ponto, gasto para rolar de novo qualquer dado que ela acabou de rolar. Volta no Descanso Longo ou agindo de acordo com o que ela acredita, uma vez por sessão. O que ela acredita, por escrito na ficha: *"eu não assino nada que eu não consertei."*

### Passo 3 — Caminho

**A Destruição.** O que isso entrega, pelo capítulo 06:

| O que o Caminho dá | Valor |
|---|---|
| Índice de vitalidade **N** | **6** (o maior do jogo) |
| **Bônus de Velocidade** | **+1** |
| 3 Perícias com Eficiência | **Atletismo, Sobrevivência, Resistência** |
| Atributo de Habilidade permitido | **Poder ou Vigor** |
| Bênçãos | 12 escritas, 10 adquiridas (capítulo 07) |

### Passo 4 — Atributos

Método A, o **array oficial**: `15, 14, 13, 12, 10, 8`.

| Atributo | Valor distribuído | Com o +2 racial | **Bônus** |
|---|---|---|---|
| **Poder** | 15 | **17** | **+4** |
| **Vigor** | 14 | 14 | **+2** |
| **Agilidade** | 13 | 13 | **+1** |
| **Discernimento** | 12 | 12 | **+1** |
| **Presença** | 10 | 10 | **+0** |
| **Sincronia** | 8 | 8 | **-1** |

Duas conferências que valem o minuto que levam:

- **Os tetos.** Nenhum valor passou de **15 na distribuição**. O 17 do Poder só existe porque o bônus racial entra **depois** — e 17 está dentro do teto 20 do jogo.
- **A equivalência com a Compra de Pontos.** Se a mesa tivesse escolhido o método B, esse mesmo array custaria `10 + 7 + 5 + 4 + 2 + 0 = 28` pontos, que é exatamente a verba. Os dois métodos nascem empatados, como promete o capítulo 03.

### Passo 5 — Atributo de Habilidade

A Destruição permite **Poder ou Vigor**. Ela escolhe **Poder (+4)** — é com a marreta que ela resolve as coisas.

Isso fixa três números para o resto da campanha:

- **Teste de Ataque das Habilidades:** `d20 + 4 (Poder) + 2 (Eficiência)` = **+6**
- **Dano das Habilidades:** dados da linha do Nível **+ 4**, somado uma vez
- **DT das Habilidades:** `8 + 4 + 2` = **14**

### Passo 6 — Elemento

**Fogo.** Combustão, forja, fúria — e, pelo capítulo 20, o Elemento que produz **Queimadura**, empatado como o maior Dano de Quebra do jogo. A arma dela não tem Elemento próprio, então o Ataque Básico dela é **Físico**; o Fogo vale para as Habilidades e para a Ultimate.

### Passo 7 — Perícias

A conta do capítulo 03: **3 do Caminho + `2 + Bônus de Sincronia` escolhidas, mínimo de 2.**

`2 + (-1) = 1` → o mínimo manda: **2 escolhidas**.

| Origem | Perícias |
|---|---|
| Do Caminho da Destruição | Atletismo, Sobrevivência, Resistência |
| Escolhidas | **Intimidação, Mecânica** |
| **Total com Eficiência** | **5** |

Mais **Eficiência nos 6 Testes de Resistência**, de graça, desde o nível 1: `d20 + Bônus do atributo + 2`.

### Passo 8 — As cinco estatísticas

Armadura escolhida: **Média** (+5 de Defesa, sem penalidade).

| Estatística | Conta | **Valor** |
|---|---|---|
| **PV** | `25 + (5 × 6) + (3 × 2)` = `25 + 30 + 6` | **61** |
| **Defesa** | `10 + 1 (Agilidade) + 5 (Média)` | **16** |
| **Esquiva** | `16 + 2 (Eficiência)`, como Reação, contra um ataque | **18** |
| **RD** | nenhuma fonte ainda (teto da faixa: 6) | **0** |
| **Velocidade** | `10 + 1 (Agilidade) + 1 (Destruição)` | **12** |

Mais dois contadores: **Energia 0/100** (dela) e **PH 3/5** (do grupo, numa mesa de 4 — capítulo 16).

### Passo 9 — A primeira Habilidade

Nível 1, uma só. Ela escreve a ***Rebarba***, pelos sete passos do capítulo 16:

| Campo | Decisão | De onde vem |
|---|---|---|
| Ficção | Ela crava a marreta no chão e o impacto sai pelo piso numa linha de brasa | dela |
| Nível | **1** | é o Nível máximo no nível 1 |
| Tipo | Dano | escolha |
| Dados | **6d6** (média **21**) **+ 4 de Poder** = **25** médio | linha do Nível 1 |
| Elemento | Fogo | passo 6 |
| Resolução | **Teste de Ataque**, `+6` | escolha |
| Alcance | Curta | o Nível 1 permite Pessoal e Curta |
| Custo | **1 PH** | linha do Nível 1 |
| Redução de Tenacidade | **2** | linha do Nível 1 |

> **A mesma Rebarba, oito níveis depois.** No nível 9 o Nível máximo dela chega a 4, e ela escreve a *Rebarba* de **Nível 4** que aparece no capítulo 16: `6d20` (média 63), 3 PH, Redução de Tenacidade 4, com Queimadura como condição. A versão de Nível 1 **continua na ficha** — e é o que ela usa quando a reserva do grupo está no fim, que é exatamente o papel que uma Habilidade barata tem na economia de PH.

### Passo 10 — A Ultimate

***A Doca Inteira***, declarada em voz alta. Na faixa 1-4 ela lê o **Nível equivalente 2** (capítulo 17):

- **Dano:** `5d10` (média **27**) `+ 4` = **31** médio, de Fogo
- **Redução de Tenacidade:** **5** — contra um Comum de Tenacidade 3, isso é **Quebra garantida**
- **Custo:** 100 de Energia. Não gasta ação, não custa PH, **1 por Ciclo**
- Sobe sozinha de potência quando Nadir muda de faixa. Ela não reescreve nada

### Passo 11 — A primeira Bênção

No nível 1 só os **6 Tier I** do Caminho estão abertos. Ela escolhe ***Pacto da Ruína***: gastar `2 × nível` de PV para somar `+Eficiência` ao dano, dobrando o bônus quando ela está abaixo da metade dos PV.

No nível 1 isso é: **gastar 2 PV por +2 de dano** (ou **+4**, abaixo de 31 PV). Um terço de um Ataque Básico de dano por 3% do PV dela — e é por isso que a Destruição é o Caminho com o maior N do jogo.

### Passo 12 — Equipamento, nome e acabamento

- **Arma:** *marreta de doca*, categoria **Pesada** (`1d12`, Poder, 2 mãos). Teste de Ataque do básico: `d20 + 4 + 2` = **+6**. Dano: `1d12 + 4 + 2` = `1d12 + 6` = **12** médio, Físico. O **+2** é a Relíquia de **Mãos I**, logo abaixo, que soma no dano de todo Ataque Básico (capítulo 25).
- **Armadura Média**, um macacão de serviço reforçado nas placas.
- **Cone de Luz de Nível 1** e **Relíquias de Tier I** nos slots que o Mestre já concedeu: **Mãos** (+2 de dano de Ataque Básico) e **Botas** (+2 de Velocidade) → a VEL dela sobe para **14**. O Bônus Maior do Cone **ainda não tem alvo**: ela escolhe quando o Mestre der nome e história ao Cone, e até lá ele não soma em nada — por isso nenhum número desta ficha o inclui.
- **Inventário:** `10 + (2 × 4)` = **18** de Espaço.
- **Uma coisa que ela carrega e não serve para nada:** o crachá cortado ao meio da doca que a expulsou.

### A ficha fechada, nível 1

```
NADIR                     Humana · A Destruição · nível 1 · Fogo
Propósito de Vida: provar que o acidente não foi culpa dela

Poder 17 (+4)   Agilidade 13 (+1)   Vigor 14 (+2)
Sincronia 8 (-1)   Discernimento 12 (+1)   Presença 10 (+0)

PV 61/61     Defesa 16     Esquiva 18     RD 0     VEL 14
Energia 0/100              PH do grupo 3/5          Eficiência +2
Atributo de Habilidade: Poder (+4)    DT das Habilidades: 14

Perícias com Eficiência: Atletismo, Sobrevivência, Resistência,
                         Intimidação, Mecânica
Testes de Resistência: todos os 6, com Eficiência

Arma:      marreta de doca — Pesada, 1d12 + 6 (com Mãos I), Físico, ataque +6
Armadura:  Média (+5 de Defesa)
Habilidade: Rebarba — Nível 1, 6d6 + 4 de Fogo, 1 PH, Tenacidade 2
Ultimate:   A Doca Inteira — 5d10 + 4 de Fogo, Tenacidade 5
Bênção:     Pacto da Ruína — 2 PV por +2 de dano (+4 abaixo de 31 PV)
Traço:      Força de Vontade — Esforço 1/1
Equipamento: Cone de Luz Nível 1 · Relíquias Mãos I, Botas I
Espaço: 18
```

**Tempo real para fazer isso na mesa, com o livro aberto: cerca de 25 minutos**, e vinte deles foram decidindo o crachá cortado ao meio.

---

## 29.8 Ficha de personagem

Copie à mão, fotocopie ou transcreva num caderno. Tudo que o combate deste livro pede está aqui, e **nada mais** — personagem não tem Tenacidade.

```
  EXPLORANDO GALÁXIAS — FICHA DE PERSONAGEM

  Nome ______________________  Jogador ______________  Nível ____
  Raça ______________________  Caminho ___________________________
  Elemento __________________  Atributo de Habilidade ____________
  Propósito de Vida _________________________________________________

  ATRIBUTOS                           PROGRESSÃO
  Poder          ____  (____)         Eficiência        + ____
  Agilidade      ____  (____)         Eficácia      P:__  TR:__
  Vigor          ____  (____)         Especialização    + ____
  Sincronia      ____  (____)         Bênçãos            ____ /10
  Discernimento  ____  (____)         Habilidades        ____ /8
  Presença       ____  (____)         Nível máx. de Habilidade __

  AS CINCO ESTATÍSTICAS
  PV ______ / ______      PV temporários ______ (teto 3 × Eficiência)
  Defesa ______           Esquiva ______ (Defesa + Eficiência, Reação)
  RD ______ (teto ______)  Velocidade ______

  RECURSOS
  Energia ______ / 100     PH do grupo ______ / ______
  Esforço ______ (só Humano)

  TESTES DE RESISTÊNCIA  (d20 + atributo + Eficiência)
  Potência Física ____   Reflexos ____        Resistência Física ____
  Resistência Mental __  Percepção Mental __  Força de Vontade ____

  PERÍCIAS COM EFICIÊNCIA  (3 do Caminho + 2 + Sincronia)
  ______________  ______________  ______________  ______________
  ______________  ______________  ______________  ______________

  HABILIDADES  (teto 8)
  # Nome                Nível  Tipo   Dados + atrib.   PH  Alcance  Ten.
  1 __________________  _____  _____  ______________  ___  _______  ___
  2 __________________  _____  _____  ______________  ___  _______  ___
  3 __________________  _____  _____  ______________  ___  _______  ___
  4 __________________  _____  _____  ______________  ___  _______  ___
  5 __________________  _____  _____  ______________  ___  _______  ___
  6 __________________  _____  _____  ______________  ___  _______  ___
  7 __________________  _____  _____  ______________  ___  _______  ___
  8 __________________  _____  _____  ______________  ___  _______  ___

  ULTIMATE  (100 de Energia · não gasta ação · 1 por Ciclo)
  Nome ______________________  Nível equivalente ____
  Efeito ____________________________________________________________

  BÊNÇÃOS DO CAMINHO  (níveis ímpares)
  N1 ______________  N3 ______________  N5 ______________
  N7 ______________  N9 ______________  N11 _____________
  N13 _____________  N15 _____________  N17 _____________
  N19 _____________

  TRAÇOS DE RAÇA  (escreva a regra inteira)
  ___________________________________________________________________
  ___________________________________________________________________

  EQUIPAMENTO
  Arma ______________________  Categoria ______  Dados ____  Elem ____
  Armadura / Vestimenta _____________________  Defesa ____  RD ____
  Cone de Luz _______________________  Nível ____  Sobreposição ____
  Relíquias: Cabeça ____  Mãos ____  Tronco ____
             Botas ____  Esfera Planar ____  Corda de Ligação ____
  Conjuntos _________________________________________________________

  INVENTÁRIO  —  Espaço: 10 + (2 × Bônus de Poder) = ______
  ___________________________________________________________________
  ___________________________________________________________________

  CONDIÇÕES ATIVAS ___________________________________________________
  RESSONÂNCIAS  I (5) [ ]   II (10) [ ]   III (15) [ ]   IV (20) [ ]
```

---

## 29.9 Ficha do Memoespírito

Só para o Caminho da Recordação (capítulo 11). As estatísticas são **ancoradas no dono** — é isso que faz o companheiro acompanhar a campanha em vez de virar decoração no nível 10.

```
  MEMOESPÍRITO — FICHA

  Nome ____________________  Dono ____________________  Nível do dono ____
  Conceito (Guerra / Perdida / Animal / Artificial / Celestial) __________
  Função (Predador / Guardião / Catalisador / Controlador) _______________
  Elemento ______________

  PONTOS  —  12 na criação, +1 a cada 2 níveis do dono, máximo 5 por atributo
  Total disponível ____   Gastos ____
  Ataque ____  Agilidade ____  Vigor ____  Outros ____________________

  ESTATÍSTICAS  (todas lidas do dono)
  PV ______ / ______      = 8 × nível do dono + (3 × pontos em Vigor)
  Defesa ______           = 10 + pontos em Agilidade + Eficiência do dono
  Velocidade ______       = 10 + pontos em Agilidade + Bônus de Velocidade
                            do Caminho do dono
  Teste de Ataque + ____  = Atributo de Habilidade do dono + pontos no
                            atributo de ataque + Eficiência do dono
  Dano ________________   = dados de Ataque Básico do dono, em d6,
                            + pontos no atributo de ataque
  Redução de Tenacidade _  = 1 (2 a partir do nível 11 do dono)
  Testes de Resistência + ____ = pontos no atributo + Eficiência do dono
  RD ____                 = 0, salvo Função Guardião ou Bênção

  3 BÔNUS MENORES  (escolhe 3 dos 6)
  ______________________  ______________________  ______________________

  2 HABILIDADES PRÓPRIAS  (1 ofensiva + 1 auxiliar)
  Ofensiva _______________________________________________________________
  Auxiliar _______________________________________________________________

  EVOLUÇÕES  (níveis 8, 14 e 20 do dono — as três, ao longo da campanha)
  [ ] Forma Completa   [ ] Fusão de Memórias   [ ] Memória Desperta

  NA FILA: casa própria pela VEL dele · invocar custa 1 PH ·
  reinvocado no Descanso Curto se caiu
```

> **Alvo de projeto:** o Memoespírito entrega **15% a 25%** do dano do dono na mesma faixa. Se na sua mesa ele estiver entregando mais que isso, confira se algum ponto está sendo somado duas vezes — a Eficiência do dono entra **uma** vez em cada linha, não uma por fonte.

---

## 29.10 Trilha de Ação

A Fila de Ação do capítulo 19 em papel. Uma tira por combate, virada **para os jogadores** — a decisão interessante do jogo ("eu ulto agora ou espero o Boss Quebrar?") só existe se a mesa consegue **ver** quem age depois de quem.

```
  CICLO ____

  casa:     1        2        3        4        5        6        7
          [_____]  [_____]  [_____]  [_____]  [_____]  [_____]  [_____]
   VEL      ____     ____     ____     ____     ____     ____     ____

                      ^ agindo agora

  PENDENTES  (Atrasos e Avanços que entram na próxima remontagem)
  ___________________________________________________________________

  CONDIÇÕES  (quem, qual, quantos turnos)
  ___________________________________________________________________

  TENACIDADE DOS INIMIGOS
  ______________ ____/____   ______________ ____/____
  ______________ ____/____   ______________ ____/____

  PH DO GRUPO ____ / ____          ULTIMATE USADA NESTE CICLO: [ ]
```

**Como usar, em quatro linhas:** monte a Fila por VEL decrescente no início do combate; marque com um traço quem já agiu; anote Atraso e Avanço em "pendentes" e **aplique na remontagem do Ciclo seguinte**; risque a Tenacidade a cada ataque que **acertar**. O estado inteiro do combate cabe nesse retângulo, sem calculadora.

---

## 29.11 Ficha de Decisões da Mesa

O único registro persistente que este livro pede. Ele existe por um motivo simples: num sistema em que o jogador escreve conteúdo, **a decisão de hoje é precedente amanhã**.

```
  FICHA DE DECISÕES DA MESA        Campanha ____________________

  MÉTODO DE ATRIBUTOS: [ ] array oficial   [ ] Compra de Pontos
  TAMANHO DA MESA: ____ jogadores  →  PH máximo ____ / início ____
  VARIANTES EM USO: [ ] PV rolado   [ ] média impressa de dano
                    [ ] outra: _______________________________

  HABILIDADES E ULTIMATES APROVADAS COM AJUSTE
  Quem   Nome                O que foi ajustado           Por quê
  _____  __________________  ___________________________  ____________
  _____  __________________  ___________________________  ____________
  _____  __________________  ___________________________  ____________

  REGRAS DECIDIDAS NA MESA  (casos-limite que o livro não cobriu)
  ___________________________________________________________________
  ___________________________________________________________________
  ___________________________________________________________________

  ARMAS, ITENS E EFEITOS CASEIROS ACEITOS
  ___________________________________________________________________
  ___________________________________________________________________

  NOMES QUE A MESA CRIOU  (facções, lugares, pessoas)
  ___________________________________________________________________
  ___________________________________________________________________
```

**Vai para a ficha:** método de atributos, variantes em uso, toda Habilidade aprovada com ajuste, todo caso-limite decidido, todo nome criado pela mesa.
**Não vai:** resultado de rolagem, dano sofrido, condição ativa. Isso é ficha de personagem e Trilha de Ação.

---

## 29.12 Referência rápida de uma página

**A rolagem única:** `d20 + Bônus de Atributo + Eficiência (se treinado) ≥ DT`. Arredonde **para baixo**. Toda instância de dano causa **no mínimo 1**.

| Eficiência / Eficácia | Níveis |
|---|---|
| **+2 / +4** | 1-3 |
| **+3 / +6** | 4-6 |
| **+4 / +8** | 7-9 |
| **+5 / +10** | 10-12 |
| **+6 / +12** | 13-15 |
| **+7 / +14** | 16-18 |
| **+8 / +16** | 19-20 |

**A Eficácia nunca entra em Teste de Ataque.** A Esquiva soma **sempre Eficiência**.

| Bônus de Atributo | 8-9 | 10-11 | 12-13 | 14 | 15-16 | 17-18 | 19-20 |
|---|---|---|---|---|---|---|---|
| | **-1** | **+0** | **+1** | **+2** | **+3** | **+4** | **+5** |

| DT por faixa | 1-4 | 5-8 | 9-12 | 13-16 | 17-20 |
|---|---|---|---|---|---|
| Trivial | 8 | 9 | 10 | 11 | 12 |
| Fácil | 10 | 12 | 14 | 16 | 18 |
| **Média** | **13** | **16** | **19** | **22** | **25** |
| Difícil | 16 | 19 | 23 | 27 | 30 |
| Muito Difícil | 19 | 23 | 27 | 31 | 35 |
| Heroica | 22 | 26 | 31 | 34 | 38 |

**As cinco DTs de subsistema vencem a tabela acima** e não escalam: descobrir Fraqueza, Surpresa **13**, Morrendo **10**, Raposa Astuta **10**, To na sua mente **13**.

**O turno:** 1 **Ataque Básico** + 1 **Ação Complementar** + 1 **Ação de Movimento**, mais a **Ultimate** (que não gasta ação) e **1 Reação**. Habilidade ocupa o espaço do Ataque Básico. **Esforço Total** troca Ataque Básico + Ação Complementar por 2 Distâncias. Máximo de **1 Ação Extra** por criatura por Ciclo.

**Distâncias:** Pessoal → Curta → Média → Longa → Extrema. Um passo por Ação de Movimento.

**Teste de Ataque:** `d20 + Atributo de Ataque + Eficiência + Especialização + equipamento ± temporários ≥ Defesa`. **20 natural** é crítico (dobra só os dados base); **1 natural** erra e não gera Energia. A faixa **19-20** é exclusiva da Caça e é o teto do jogo.

| Habilidade | Nível 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| **Dano** | `6d6` 21 | `5d10` 27 | `6d12` 39 | `6d20` 63 | `10d20` 105 | `14d20` 147 | `18d20` 189 |
| **Cura** | `5d8` 22 | `6d10` 33 | `8d12` 52 | `7d20` 73 | `10d20` 105 | `14d20` 147 | `18d20` 189 |
| **PH** | 1 | 1 | 2 | 3 | 4 | 5 | 6 |
| **Tenacidade** | 2 | 2 | 3 | 4 | 5 | 6 | 7 |

Mais o **Bônus do Atributo de Habilidade**, uma vez. **Em área:** metade dos dados (mínimo 1), até **3 alvos** (4 nos Níveis 6 e 7), teto absoluto **6**.

**Energia:** Ataque Básico **+20**, Habilidade **+30** (acerte ou não), sofrer dano **+10** (1/Ciclo), derrotar **+10**, Quebrar **+10** (1/Ciclo). Ultimate a **100**, **1 por Ciclo**.

**Fraqueza** dá **+2 dados** do mesmo tipo (não critam); **Resistência** tira **2 dados** (mínimo 1). Redução de Tenacidade: **total** contra Fraqueza, **metade** contra neutro, **1 ponto** contra Resistência — e sempre **condicionada ao acerto**. Só inimigos têm Tenacidade.

**Tetos que a mesa esquece:** bônus somado **+3 / +4 / +5** por faixa · penalidade somada **-3 / -4 / -5** · dados adicionais **+3** por rolagem (sem contar a Fraqueza) · RD `2 + (2 × Eficiência)` · PV temporários `3 × Eficiência` · acúmulos de uma condição **5** · Habilidades conhecidas **8**.

**Condições, em uma linha cada:** Sangramento, Queimadura, Choque, Cisalhamento de Vento (Dano Contínuo, 2 turnos, ignora RD) · Embaraço e Aprisionamento (dano + Atraso) · Congelado (só inimigos: Comum perde o turno; Elite e Boss são Atrasados 2 casas) · Lentidão · Marcado · Silenciado · Vulnerável · Controlado · Corrupção · Quebrado (só inimigos) · Surpreso · Morrendo. Os verbetes completos estão no capítulo 21.

**Morrendo:** 0 PV, mantém a casa na Fila, **Força de Vontade DT 10** com `d20 + Presença` **apenas**. 3 sucessos estabiliza com 1 PV, 3 falhas morre, 20 natural levanta, 1 natural vale 2 falhas, dano é 1 falha (2 se crítico ou Habilidade de Nível 5+). Cura de 1 PV levanta.

**Descanso Curto:** 1 hora, 2 por dia, `(2 × nível) + Vigor` de PV. **Descanso Longo:** 8 horas, 1 por dia, tudo volta.

**Falhe para frente:** uma falha em Teste de Perícia nunca trava a cena. A cena avança com custo.

---

> **Fim do apêndice.** Se um número deste capítulo não bater com o do capítulo que você estava lendo, o **capítulo** vence e o erro é nosso: anote na Ficha de Decisões da Mesa e siga jogando.
