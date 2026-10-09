# Changelog — da v0.1 para a v1.0

**Sistema:** Explorando Galáxias · **Autoria:** MC Filhos · **Versão:** 1.0

Este documento existe por um motivo só: **você escreveu a v0.1, e a v1.0 mudou algumas coisas que você escreveu.** Cada uma dessas mudanças está aqui, com a conta que a motivou e com o caminho de volta, para você poder discordar **ponto a ponto** em vez de ter que aceitar o pacote inteiro.

Ele tem seis partes:

| Parte | O que você encontra |
|---|---|
| **1** | O que ficou **intacto** — e é a maior parte do sistema |
| **2** | As **nove decisões** que mudam número seu. Leia estas primeiro |
| **3** | As outras correções: regra que faltava, regra que se contradizia |
| **4** | Tudo que foi **adicionado** |
| **5** | A **normalização de nomenclatura** |
| **6** | O **índice de decisões**, com uma coluna para você marcar discordância |

> **Como cada entrada da parte 2 e 3 é escrita.** Quatro campos fixos: **o que a v0.1 dizia** (com as suas palavras, quando couberem), **o que a v1.0 faz**, **por quê**, e **como reverter** — o que quebra se você quiser o número antigo de volta. O último campo é o mais importante: ele é o preço da sua discordância, não um argumento contra ela.
>
> Este arquivo e o capítulo 01 são os **únicos** lugares do livro onde termos aposentados ("ação bônus", "DoT", "rodada", "HP") aparecem escritos. No resto do livro, eles não existem.

---

## Parte 1 — O que ficou intacto

Antes da lista do que mudou, a lista do que **não** mudou. É a parte maior, e é ela que faz a v1.0 ser a sua v0.1 terminada e não outro jogo:

- **A rolagem única:** `d20 + Bônus de Atributo + Eficiência` contra uma DT. Nenhuma segunda fórmula de resolução entrou no livro.
- **Os 6 Atributos** e as descrições deles, palavra por palavra: Poder, Agilidade, Vigor, Sincronia, Discernimento, Presença.
- **As 18 Perícias**, com os nomes que você deu.
- **As 7 Raças**, com as citações, as características e os traços — reescalonados onde o número não cabia, nunca substituídos.
- **Os 9 Caminhos** e a ordem de vitalidade entre eles. O número de dados de vida que você escreveu virou o **índice N** da fórmula de PV, então a proporção que você desenhou sobreviveu.
- **As 50 Bênçãos** dos cinco Caminhos escritos, uma por uma, com nome e efeito. Nenhuma foi cortada.
- **Os 7 Elementos**, as Fraquezas, as Resistências e os sete efeitos de Quebra.
- **Tenacidade e Quebra** como subsistema, inclusive a regra de que **é obrigatório acertar** para retirar Tenacidade — que a v1.0 generalizou para o PH.
- **A Ultimate a 100 de Energia**, declarada pelo nome **em voz alta**, com o excedente perdido.
- **O jogador escreve as próprias Habilidades**, com tabelas-guia. É a melhor ideia da v0.1 e é a espinha da v1.0.
- **O array `15, 14, 13, 12, 10, 8`** e os marcos da tabela de bônus (8 = -1, 10 = +0, 12 = +1, 14 = +2, **15 = +3**).
- **A Eficácia desbloqueando no nível 5** — o número que a sua mesa já conhece.
- **O Nível máximo de Habilidade 2 já no nível 2**, que está escrito com essas palavras na v0.1.
- **O Propósito de Vida**, o **Esforço** do Humano, o **Executado**, o **Guia de Criação de Memoespírito** (Conceitos, Funções, Bônus menores, as 12 pontos e o teto de 5 por atributo) e os nomes das três Evoluções.
- **O `.docx` da v0.1 permanece intocado** na raiz do projeto, como registro histórico.

**A faixa de níveis mudou de 1-10 para 1-20 por decisão sua**, e é a única mudança deste documento que não precisa de justificativa — ela é o pedido original. Tudo o mais na parte 2 é consequência de fazer a matemática da v0.1 chegar sã ao nível 20.

---

## Parte 2 — As nove decisões que mudam número seu

### 2.1 Tabela de Bônus de Atributo normalizada

| | |
|---|---|
| **O que a v0.1 dizia** | 8 → -1 · 10 → +0 · 12 → +1 · **13 → +2** · **14 → +2** · 15 → +3. E nada acima de 15 |
| **O que a v1.0 faz** | Tabela monotônica de 8 a 20. **A única célula alterada é o 13, que cai de +2 para +1** |
| **Por quê** | Com 13 e 14 valendo o mesmo, **subir de 13 para 14 não fazia nada** — e 14 é um dos valores do seu próprio array. Pior: o degrau de 12 para 13 valia mais que o de 13 para 14, então a tabela recompensava parar no 13. E ela não cobria valores que a própria v0.1 produz: um 15 com +2 racial é 17, que não tinha linha |
| **Como reverter** | Se você quiser 13 = +2, o 14 precisa virar +3 para o degrau não desaparecer de novo — e aí toda a tabela desloca +1 a partir do 13, o que infla Defesa, DT de Habilidade, dano e PV de todo personagem do livro em 1 ponto. A alternativa barata é deixar 13 = +2 e aceitar que 13 e 14 empatam; nesse caso corrija também o preço do 14 na Compra de Pontos, que hoje cobra 7 por um degrau |

**A tabela publicada:**

| Valor | 8 | 9 | 10 | 11 | 12 | **13** | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Bônus** | -1 | -1 | +0 | +0 | +1 | **+1** | +2 | **+3** | +3 | +4 | +4 | +5 | +5 |

O array oficial continua entregando **+3, +2, +1, +1, +0, -1** (soma +6), e o 15 continua sendo o degrau premiado — que é onde você quis que a especialização aparecesse.

### 2.2 Fórmula de Esquiva

| | |
|---|---|
| **O que a v0.1 dizia** | **Esquiva = Defesa + Bônus de Agilidade** |
| **O que a v1.0 faz** | **Esquiva = Defesa + Eficiência**, como Reação, declarada antes da rolagem do inimigo, contra um ataque. Armadura Pesada não permite Esquiva |
| **Por quê** | A Defesa da v0.1 **já inclui o Bônus de Agilidade**. A fórmula antiga contava Agilidade **duas vezes**: um personagem com Agilidade 20 ganhava **+5 de Defesa de graça e +5 de novo** ao Esquivar, ou seja +10 de Defesa de uma Reação só. Contra o ataque inimigo da faixa alta, isso é imunidade a um ataque por turno — e a Esquiva é gratuita, universal e disponível **todo turno** |
| **Como reverter** | Se você quiser a Agilidade na Esquiva, tire-a da Defesa (`Defesa = 10 + armadura`), senão a conta dupla volta. E saiba o preço: a Esquiva por Eficiência vale +2 no nível 1 e +8 no 20, previsível e dentro do orçamento; por Agilidade ela vale até +5 e **satura no nível 6**, quando o atributo bate no teto 20 |

A Esquiva entrou nas premissas do balanceamento com número próprio: **1 ataque Esquivado por Ciclo no grupo**, levando o acerto daquele ataque de 60% para 20%. É ela que sustenta a janela de attrition de 73% a 81% dos PV por combate (capítulo 29).

### 2.3 Todas as médias de dados corrigidas

| | |
|---|---|
| **O que a v0.1 dizia** | As médias impressas eram `número de dados × valor médio truncado`: `6d6 = 18`, `5d10 = 25`, `6d12 = 36`, `6d20 = 60`, `10d20 = 100` de dano; `5d8 = 20`, `6d10 = 30`, `8d12 = 48`, `7d20 = 70` de cura |
| **O que a v1.0 faz** | A média de um `dN` é **`(N + 1) ÷ 2`**. Toda média impressa no livro é `número de dados × (N + 1) ÷ 2`, **arredondada para baixo** pela regra global do capítulo 02 |
| **Por quê** | A média de um d6 é **3,5**, não 3. Truncar o dado antes de multiplicar **subestimava o dano em até 17%** — e esse erro contaminava tudo o que se calcula a partir do dano: PV de inimigo, orçamento de encontro, quantos Ciclos dura um combate. **Nenhum dado foi trocado:** a quantidade e o tipo que você escreveu estão intactos. Só a média impressa mudou |
| **Como reverter** | Não há o que reverter sem reescrever a aritmética: `(N+1)/2` é a média de um dado honesto. O que **é** escolha nossa é o **arredondamento para baixo** das médias fracionárias — se você preferir arredondar para cima, troque 27 por 28, 22 por 23 e 73 por 74, e ajuste o orçamento de PV do capítulo 29 em 1% |

| Linha | Dados | v0.1 dizia | **Média real `(N+1)/2`** | **Impresso na v1.0** |
|---|---|---|---|---|
| Dano Nível 1 | `6d6` | 18 | **21,0** | **21** |
| Dano Nível 2 | `5d10` | 25 | **27,5** | **27** |
| Dano Nível 3 | `6d12` | 36 | **39,0** | **39** |
| Dano Nível 4 | `6d20` | 60 | **63,0** | **63** |
| Dano Nível 5 | `10d20` | 100 | **105,0** | **105** |
| Cura Nível 1 | `5d8` | 20 | **22,5** | **22** |
| Cura Nível 2 | `6d10` | 30 | **33,0** | **33** |
| Cura Nível 3 | `8d12` | 48 | **52,0** | **52** |
| Cura Nível 4 | `7d20` | 70 | **73,5** | **73** |
| **Nível 6** (novo) | `14d20` | — | **147,0** | **147** |
| **Nível 7** (novo) | `18d20` | — | **189,0** | **189** |

As três médias fracionárias — **27,5**, **22,5** e **73,5** — são impressas como **27**, **22** e **73** porque o livro arredonda para baixo em toda parte, sem exceção. É a mesma regra que corta meio ponto de dano, meio PV e meia casa de Atraso.

### 2.4 Curva de Eficiência reespaçada para 1 a 20

| | |
|---|---|
| **O que a v0.1 dizia** | +2 nos níveis 1-3, +3 nos 4-6, +4 nos 7-8, +5 no 9, +6 no 10. Um degrau a cada 3 níveis, depois a cada 2, depois **a cada 1** |
| **O que a v1.0 faz** | **Um degrau a cada 3 níveis, do +2 ao +8.** Os níveis **1 a 6 ficam idênticos** à v0.1 |
| **Por quê** | A curva da v0.1 **acelera no fim**. Estendida até o nível 20 no mesmo padrão, ela chegaria perto de **+16 de Eficiência e +32 de Eficácia** — e nenhuma DT que um livro consegue publicar segura isso. Com um degrau a cada 3 níveis, o nível 20 fecha em +8, que somado ao atributo (+5), à Especialização (+3) e ao Cone de Luz (+3) dá **+19** de ataque, exatamente a janela de acerto que o balanceamento usa nas cinco faixas |
| **Como reverter** | A conta muda em **duas células**: o nível 9 cai de +5 para +4 e o nível 10 de +6 para +5. Se você quiser os valores antigos nesses dois níveis, precisa decidir o que acontece do 11 ao 20 — e qualquer curva que preserve a aceleração estoura a tabela de DT do capítulo 27 e a Defesa de inimigo do capítulo 28 |

| Nível | 1-3 | 4-6 | 7-9 | 10-12 | 13-15 | 16-18 | 19-20 |
|---|---|---|---|---|---|---|---|
| **Eficiência** | +2 | +3 | **+4** | **+5** | +6 | +7 | +8 |
| **Eficácia** | +4 | +6 | +8 | +10 | +12 | +14 | +16 |

### 2.5 Fim dos dados de vida oscilantes

| | |
|---|---|
| **O que a v0.1 dizia** | Role os dados de vida do seu Caminho no nível 1 — de **2d20** (Caça) a **6d20** (Destruição) — e **1d20 por nível** depois |
| **O que a v1.0 faz** | **PV fixo.** `PV no nível 1 = 25 + (5 × N) + (3 × Bônus de Vigor)`; `PV por nível = 5 + N + Bônus de Vigor`, onde **N é o número de dados que você escreveu** para o Caminho |
| **Por quê** | Dois defeitos sérios, e o primeiro é fatal: **um Caça que rola 2 em 2d20 começa a campanha com 2 PV** — menos que um único ataque de Comum da primeira faixa. No outro extremo, uma Destruição que rola bem tem 50 vezes mais vida que ele. O segundo defeito só aparece no longo prazo: com **1d20 fixo por nível** para todos, a diferença entre Caminhos **encolhe** conforme o jogo avança. No nível 20 da v0.1, Destruição (`25d20` ≈ 262) e Caça (`21d20` ≈ 220) ficariam a 19% de distância — o Caminho mais resistente e o mais frágil praticamente iguais, com variação de mais de 100 PV entre dois personagens do mesmo Caminho |
| **Como reverter** | Existe **variante oficial** no capítulo 06 para quem quer o dado de volta: role `1d20` por nível no lugar do valor fixo, com **piso igual ao valor fixo menos 3 e teto igual ao valor fixo mais 5**. Ela devolve o risco sem devolver o personagem de 2 PV. Reverter a rolagem **sem** piso significa aceitar que a ficha mais importante do jogo seja decidida no dado, e que o orçamento de encontro do capítulo 29 não valha para a sua mesa |

A **ordem exata** dos nove Caminhos sobreviveu; o que mudou foi a razão entre as pontas, de **3:1** para **1,45:1**.

| Caminho | N | PV nível 1 (Vigor +2) | Por nível | PV nível 20 |
|---|---|---|---|---|
| A Destruição | 6 | 61 | 13 | 308 |
| A Preservação / A Abundância | 5 | 56 | 12 | 284 |
| A Inexistência | 4 | 51 | 11 | 260 |
| A Harmonia / Erudição / Euforia / Recordação | 3 | 46 | 10 | 236 |
| A Caça | 2 | 41 | 9 | 212 |

### 2.6 O Avatar de cada Caminho mudou de nível 5 para nível 17

| | |
|---|---|
| **O que a v0.1 dizia** | O **Avatar** era o capstone do Caminho, com **requisito de nível 5** |
| **O que a v1.0 faz** | O Avatar é a Bênção de **Tier III**, com **requisito de nível 17**. Cada Caminho tem **12 Bênçãos escritas** em três tiers: **6 sem requisito**, **4 a partir do nível 9**, **2 a partir do nível 17** — e uma das duas últimas é o Avatar |
| **Por quê** | Num jogo que vai ao nível 20, um capstone no nível 5 deixa **quinze níveis sem nada acima dele**: a progressão do Caminho terminaria antes de um quarto da campanha. E o Avatar é, por desenho, a Bênção mais forte do Caminho — no nível 5 ela domina o jogo, e depois do 10 ela é a única coisa que a ficha tem de interessante |
| **Como reverter** | Se você quiser o Avatar no nível 5, ele precisa ficar **muito** mais fraco — e aí deixa de ser Avatar. O meio-termo que a v1.0 oferece sem mexer em nada: os **6 Tier I** estão abertos desde o nível 1, então o personagem de nível 5 já escolheu **3 Bênçãos** e tem acesso às 6 mais baratas. A fantasia de "virar o Caminho" chega no 17; a de "o Caminho me responde" chega no 1 |

A aquisição acontece nos **níveis ímpares** — 1, 3, 5, 7, 9, 11, 13, 15, 17 e 19 — logo você adquire **10 das 12** escritas. Dois personagens do mesmo Caminho nunca ficam iguais, o que é novo: na v0.1, com 10 escritas e 10 adquiridas, eles ficavam.

### 2.7 Teto na quantidade de Habilidades

| | |
|---|---|
| **O que a v0.1 dizia** | "O número de habilidades que você pode ter por nível é **igual ao seu nível**" |
| **O que a v1.0 faz** | **Teto de 8 Habilidades conhecidas**, alcançado no nível 15. A partir do nível 16, em vez de aprender novas, você **reescreve uma por nível**, podendo subir o Nível dela |
| **Por quê** | A fórmula da v0.1 entrega **20 Habilidades** no nível 20. Como é o **jogador** que escreve cada uma, isso são vinte blocos de texto autoral por ficha: ninguém lê, ninguém lembra, e o turno vira consulta. E a economia de PH já limita o uso a 2 ou 3 Habilidades por combate de qualquer jeito — as outras dezessete seriam decoração |
| **Como reverter** | Se você quiser mais de 8, o número que aguenta é o que a mesa consegue manejar sem parar o combate. O que **não** dá para reverter sem mexer no resto é a fórmula "igual ao nível": ela também era a única regra de progressão de Habilidade da v0.1, e a v1.0 separou as duas coisas — **quantas** você tem (teto 8) e **de que Nível** (o máximo sobe a cada 3 níveis, até o 7 no nível 18) |

A regra de reescrita a partir do 16 existe para a progressão não parar no 15: **no fim da campanha você não tem mais Habilidades, você tem Habilidades melhores.**

### 2.8 "Ação bônus" virou Ação Complementar

| | |
|---|---|
| **O que a v0.1 dizia** | Bênçãos da Inexistência pediam uma **"ação bônus"** (*Olhar da Ausência*) e uma **"ação comum"** (*Névoa da Inexistência*) |
| **O que a v1.0 faz** | As ações do turno são **quatro, e fechadas**: **Ataque Básico**, **Ação Complementar**, **Ação de Movimento** e **Reação**, mais a **Ultimate**, que não gasta ação. "Ação bônus" virou **Ação Complementar**; "ação comum" virou **"no lugar do seu Ataque Básico"** |
| **Por quê** | A v0.1 usava um termo **que o próprio sistema dela não tinha**. Não existia "ação bônus" na lista de ações da v0.1 — era vocabulário emprestado de outro jogo, e numa mesa isso produz exatamente a pergunta que trava o turno: "então eu uso isso **e** ataco?" Com quatro ações nomeadas, a resposta está na ficha |
| **Como reverter** | Nada a reverter de mecânica: as duas Bênçãos continuam fazendo o que você escreveu, com o mesmo custo de turno. O que mudou é o **nome da ação**. E vale registrar: a palavra **Bônus** continua oficial e aparece em quase toda tabela — **Bônus de Atributo**, **Bônus Maior**, **Bônus de Velocidade**, **Bônus de Armadura**. O que foi aposentado é "bônus" como **nome de ação** |

### 2.9 A cláusula de variação de dados "com base na força do causador" foi aposentada

| | |
|---|---|
| **O que a v0.1 dizia** | "A Redução e Aumento de dados com base em Fraquezas e Resistências **pode ser aumentada ou diminuída com base na força do causador de dano**" |
| **O que a v1.0 faz** | **Fraqueza dá sempre +2 dados** do mesmo tipo (e eles não critam). **Resistência tira sempre 2 dados**, conservando no mínimo 1. Dado adicional só vem de **fonte declarada** — condição Quebrado, Vulnerável, Cone de Luz, Conjunto de Relíquia, Bênção — e tudo isso disputa o **teto de +3 dados por rolagem**, que não conta os +2 da Fraqueza |
| **Por quê** | A cláusula é uma **válvula aberta no número mais sensível do sistema**. A premissa de balanceamento assume que **3 das 4 ações agressivas do Ciclo acertam Fraqueza**; cada dado a mais ou a menos nessa parcela move o dano do grupo por Ciclo em **5% a 8%**, e o orçamento de PV de **todos** os inimigos do livro é `dano por Ciclo × 4`. Na prática, a cláusula pedia que o Mestre decidisse no meio do combate um número que arrasta o bestiário inteiro — e sem escala nenhuma para guiar a decisão, porque "força do causador" não é uma estatística do jogo |
| **Como reverter** | Se você quer a variação de volta, ela precisa de **escala e teto**. A forma que cabe no orçamento: "+1 dado adicional contra Fraqueza, **dentro do teto de dados adicionais**" — mesmo lugar onde já moram Quebrado e Vulnerável, e por isso automaticamente limitado. Reverter a cláusula **aberta** significa abrir mão da janela de 3 a 5 Ciclos: com dois dados extras por ação agressiva, o combate típico da faixa alta termina em 2,8 Ciclos |

---

## Parte 3 — As outras correções

Estas são do mesmo tipo das nove de cima, mas de impacto menor: regra citada e nunca escrita, número fora de escala, ou duas passagens da v0.1 que diziam coisas diferentes. Cada uma tem a mesma estrutura, em forma curta.

### 3.1 RD — Redução de Dano ganhou definição e escala

- **A v0.1 dizia:** "10 RD" na Armadura Pesada e "+10 RD", "+15 RD", "+5 RD" em pelo menos 8 Bênçãos — **sem nunca dizer o que RD significa**.
- **A v1.0 faz:** RD subtrai um valor fixo **de cada instância** de dano, depois dos ajustes de dados e do crítico; fontes somam até o **teto `2 + (2 × Eficiência)`**; toda instância causa **no mínimo 1**; **Dano Contínuo ignora RD**. A **Armadura Pesada passa de 10 RD para 2 RD**, e todo "+10/+15 RD" de Bênção virou **"RD igual à sua Eficiência"** ou um valor fixo de +2 ou +3.
- **Por quê:** com a Armadura Pesada da v0.1 (10) mais duas Bênçãos de Abundância (+10 e +10), um personagem de **nível 2** teria **30 de RD** contra ataques de 10 a 14 de dano: literalmente invulnerável. O teto amarra a RD à Eficiência, então ela cresce junto com o dano do jogo em vez de estourá-lo.
- **Como reverter:** manter os valores antigos exige inflar o dano de todo inimigo do livro em 10 a 15 pontos por acerto, o que mata o personagem sem RD. O teto é o ponto de contato: suba-o se quiser, mas suba a tabela de dano do capítulo 28 junto.

### 3.2 Efeitos em porcentagem de PV foram aposentados

- **A v0.1 dizia:** "metade da vida máxima", "cura 25% da vida", "perde 10% da vida máxima" e variações, em várias Bênçãos.
- **A v1.0 faz:** tudo virou **valor fixo, dados ou múltiplo de nível e de Eficiência** (`2 × nível`, `5 × nível`, `4 × nível`, `RD = Eficiência`). A **única exceção declarada é o Sangramento**, que é 5% dos PV máximos **com teto `3 × Eficiência`**.
- **Por quê:** porcentagem de PV escala com o alvo, não com o jogo. "Metade da vida máxima" contra um Comum de 50 PV é 25; contra o Boss de 935 é 467 — a mesma Bênção, a mesma linha de texto, dezenove vezes o efeito. Num jogo de 20 níveis isso não é um bônus, é uma alavanca quebrada.
- **Como reverter:** se quiser porcentagem em alguma Bênção específica, ela precisa de teto, como o Sangramento tem.

### 3.3 Tenacidade: Elemento neutro agora reduz metade

- **A v0.1 dizia:** "Você não pode reduzir a Tenacidade de um Inimigo que não possua Fraqueza ao seu elemento."
- **A v1.0 faz:** **redução total** contra Fraqueza, **metade** (mínimo 1) contra neutro, **1 ponto fixo** contra Resistência.
- **Por quê:** com a regra antiga, metade do grupo não participava do melhor subsistema do jogo em metade dos encontros. O grupo tem **4 Elementos** fixos contra **7** possíveis e 1 a 4 Fraquezas por inimigo: zerar a contribuição de quem não acertou a Fraqueza transformava a Quebra em sorteio de criação de personagem.
- **Como reverter:** a regra antiga é jogável, mas aí a cadência de Quebra do capítulo 28 (Boss a cada 2 Ciclos) precisa ser recalculada contando só metade das ações do grupo, e a Tenacidade de Boss cai para cerca de 6.

### 3.4 Cura de Nível 5 deixou de ser cura total

- **A v0.1 dizia:** "Cura toda a Vida".
- **A v1.0 faz:** **`10d20`** (média 105), ou **`5d20` em todos os aliados**.
- **Por quê:** com cura total disponível, **PV deixa de ser recurso** — e PV é o recurso contra o qual todo o orçamento de encontro é escrito. Uma Habilidade que apaga a conta de atrito apaga também a tensão da cadeia de três combates do dia.
- **Como reverter:** não dá, sem desligar o orçamento. O que existe como meio-termo já está no livro: a cura de Nível 7 chega a **189** por alvo, o que na prática é cura total para quase todo mundo — só não é **garantida**.

### 3.5 Perícias: três consertos pontuais

| O que | v0.1 | v1.0 | Por quê |
|---|---|---|---|
| **Quantidade** | 3 do Caminho + `2 + Bônus de Sincronia` | Igual, **com mínimo de 2 escolhidas** | Com Sincronia 8 (Bônus -1), a conta da v0.1 dava **1** Perícia escolhida |
| **Sintonia** | "+Discernimento ou +Sincronia" | Você **escolhe o atributo na criação** e ele é **fixo** | Escolher a cada teste faria dela a melhor Perícia do livro, de graça |
| **Teste de Atenção** (Vulpes) | Teste próprio, DT 8 | **Teste de Percepção Mental, DT 10** | O sistema tem **6** Testes de Resistência oficiais; não existe um sétimo exclusivo de uma Raça. Com Eficiência somando, o traço ficou **mais** confiável que o original |

### 3.6 Correções de Raça e de equipamento

| O que | v0.1 | v1.0 | Por quê |
|---|---|---|---|
| **"To na sua mente"** (Haloviano) | Teste oposto de Persuasão contra Intuição | **Teste de Força de Vontade do alvo contra a sua DT**, DT 13 fixa. Os 2 usos por dia e o bloqueio na falha ficam | Teste oposto exige duas rolagens e uma tabela de empate que a v0.1 não tinha |
| **Armadura Pesada** | 10 RD · "-5 em Testes de Agilidade" | **2 RD** · **-2 em Testes e Perícias de Agilidade** · **-2 de Velocidade** · **não permite Esquiva** | -5 era maior que qualquer bônus do jogo. A troca agora é explícita: 3 pontos de Defesa pagos com a Reação defensiva e com velocidade |
| **Armadura Leve** | +1 de Agilidade | **+1 de Velocidade** | Bônus de **atributo** por armadura mexia em PV, Defesa, Esquiva e meia dúzia de Perícias de uma vez |
| **Executado** | Dentro do traço Xianzhouíta | Regra geral no capítulo 23; o traço Xianzhouíta aponta para lá | A regra valia para todo mundo, mas só estava escrita na ficha de uma Raça |

### 3.7 Congelamento contra Elite e Boss

- **A v0.1 dizia:** o alvo Congelado "perde seu turno neste Ciclo" — para todo mundo.
- **A v1.0 faz:** **Comum perde o turno.** **Elite e Boss são Atrasados em 2 casas e não podem usar ação especial no turno seguinte.**
- **Por quê:** a premissa de balanceamento assume o Boss agindo em **todos** os Ciclos. Um Boss que passa metade do combate fora da Fila não é um combate — é uma animação. E, na prática de mesa, tirar a ação especial de um Boss costuma valer mais que tirar o turno dele.
- **Como reverter:** se quiser Congelamento tirando o turno do Boss, conte um Ciclo a mais no orçamento e espere que o Caminho do Gelo vire obrigatório na mesa.

### 3.8 O Teste de Morrendo ganhou teste e DT

- **A v0.1 dizia:** o estado existia ("3 vitórias antes de 3 derrotas"), **sem dizer qual teste nem qual DT**.
- **A v1.0 faz:** **Teste de Força de Vontade contra DT 10**, somando **só `d20 + Bônus de Presença`** — **sem Eficiência e sem Eficácia**. 3 sucessos estabiliza com 1 PV; 3 falhas mata; 20 natural levanta com 1 PV; 1 natural vale 2 falhas; receber dano é 1 falha (2 se crítico ou Habilidade de Nível 5+).
- **Por quê:** é a **única** exceção à fórmula de Teste de Resistência do livro, e é deliberada: com Eficiência, um personagem de nível 20 passaria em 95% das rolagens e o estado deixaria de ser um estado. Sem ela, a chance é a mesma no nível 1 e no 20 — morrer continua possível na última sessão.
- **Como reverter:** somar Eficiência é trivial, mas aí considere subir a DT junto, ou aceitar que Morrendo é um inconveniente e não um risco.

### 3.9 Memoespírito: ficha, âncoras e Evoluções

| O que | v0.1 | v1.0 | Por quê |
|---|---|---|---|
| **Ficha** | Não existia | **Ficha completa** (capítulo 29) | O Guia de Criação era bom e ficou quase inteiro, mas não havia onde escrever PV, Defesa e ataque |
| **Estatísticas** | Os 12 pontos eram a escala | **Ancoradas no dono** (PV, Defesa, VEL, ataque, Testes de Resistência); os 12 pontos **diferenciam** dois Memoespíritos | Sem âncora, no nível 20 ele acertaria 30% das vezes contra Boss, seria sempre acertado e entregaria ~2% do dano do grupo: o Caminho da Recordação parava de funcionar na metade da campanha |
| **Evoluções** | 2, nos níveis **5 e 10** | **3**, nos níveis **8, 14 e 20** | Com 20 níveis, as três opções que você escreveu — Forma Completa, Fusão de Memórias, Memória Desperta — **todas** podem ser escolhidas numa campanha completa |
| **Como age** | Não estava escrito | **Casa própria na Fila** pela VEL dele; invocar custa 1 PH | A Fila de Ação é nova, e sem essa linha o companheiro não tinha quando agir |

### 3.10 PH dimensionado pelo tamanho da mesa

- **A v1.0 adiciona** os Pontos de Habilidade como reserva **compartilhada do grupo**: `máximo = 1 + número de jogadores`, +1 na faixa 9-16 e +2 na 17-20; começa cada combate com o máximo menos 2; cada **Ataque Básico que acerta** gera +1 (faixas 1-8) ou +2 (9-20).
- **Por quê a fórmula depende do número de jogadores:** uma mesa de 6 gera o dobro de PH de uma mesa de 3 contra um teto fixo — com 6 o recurso deixa de ser decisão, com 3 o grupo nunca paga uma Habilidade de topo. A fórmula reproduz **exatamente** os números da mesa de 4 (5/6/7 de máximo, 3/4/5 de início), que é a mesa que o balanceamento usa.
- **O que isso corrige na v0.1:** nada — é mecânica nova. Ela existe porque sem ela quatro jogadores de nível 20 usando a melhor Habilidade todo turno entregariam ~525 de dano por Ciclo em vez dos 271 orçados, e todo Boss precisaria de mais de 2.000 PV.

### 3.11 A Ultimate ganhou número

- **A v0.1 dizia:** a Ultimate "nos níveis iniciais será fraca" e o jogador pode "mantê-la visualmente e só aumentar seu efeito ao passar de nível" — **sem nunca dar um valor**.
- **A v1.0 faz:** a Ultimate não tem Nível próprio; ela tem um **Nível equivalente por faixa** (2 / 3 / 4 / 5 / 6) e lê as tabelas de Habilidade nesse Nível. Redução de Tenacidade **5** em todas as faixas. **Sobe sozinha** quando você muda de faixa.
- **Por quê:** sem número, o Mestre não tinha como aprovar a criação de ninguém e o balanceamento não fechava — a Ultimate é a única ação do jogo que **não gasta ação**, e na faixa alta ela é a maior parcela isolada do dano do grupo (106 dos 271 por Ciclo).
- **Por quê um Nível abaixo do topo:** se a Ultimate empatasse com a melhor Habilidade, o jogador racional pararia de gastar PH, e a economia que sustenta o balanceamento viraria decoração. Nas faixas baixas elas empatam de propósito: no nível 3, a Ultimate **é** o grande momento do personagem.

### 3.12 Nome do sistema consolidado

- **A v0.1 dizia:** o nome vinha acompanhado de um parêntese avisando que ele provavelmente mudaria.
- **A v1.0 faz:** **Explorando Galáxias**, sem aviso. Autoria **MC Filhos**, versão **1.0**.
- **Por quê:** um livro que avisa que vai trocar de nome não é uma versão 1.0. Se você quiser outro nome, troque — é um achar-e-substituir em 31 arquivos, e nenhuma regra depende dele.

---

## Parte 4 — Tudo que foi adicionado

### 4.1 Os quatro Caminhos que existiam só como uma linha de PV

A v0.1 tinha **9 Caminhos na tabela de dados de vida e 5 escritos**. Erudição, Euforia, Caça e Preservação existiam apenas como um número de dados. Foi o maior volume de escrita da v1.0:

| Caminho | Aeon | Eixo mecânico novo | Perícias | O que ganhou |
|---|---|---|---|---|
| **A Erudição** | Nous | **Acúmulos de Cálculo** — área e multi-alvo | Ciência, Pesquisa, Tecnologia | 12 Bênçãos |
| **A Euforia** | Aha | **Tabela do Riso** (`d6`) — caos controlado | Enganação, Acrobacia, Persuasão | 12 Bênçãos |
| **A Caça** | Lan | **Marcação de Presa** — alvo único, velocidade, crítico **19-20** | Furtividade, Percepção, Acrobacia | 12 Bênçãos |
| **A Preservação** | Qlipoth | **Barreira** — escudos e Reações defensivas | Resistência, Atletismo, Intuição | 12 Bênçãos |

São **48 Bênçãos escritas do zero**. Nenhum dos nove Caminhos fica com zero Bênçãos, e nenhum eixo mecânico repete o de outro.

**Os cinco Caminhos da v0.1 ganharam 2 Bênçãos novas cada**, as duas nos **tiers altos** (nível 9+ e 17+) — são 10 Bênçãos novas, e elas entram exatamente onde os Caminhos da v0.1 eram rasos: a progressão deles terminava no Avatar. Total do livro: **108 Bênçãos escritas**.

### 4.2 Mecânicas novas

| Mecânica | O que resolve | Capítulo |
|---|---|---|
| **Velocidade (VEL)** | A v0.1 falava de "casas", de "derrubar turno" e de "aumento na velocidade" **sem ter uma estatística de Velocidade** | 19 |
| **Fila de Ação, Ciclo, casa, Firmeza** | A maior lacuna da v0.1: não havia ordem de combate escrita | 19 |
| **Atrasar / Avançar / Avanço Total** | Dá regra, teto e ordem de operação ao "derrubar o turno" que a v0.1 citava em três lugares | 19 |
| **PH (Pontos de Habilidade)** | Faz a Habilidade ter custo. É a espinha do balanceamento | 16 |
| **Especialização de Combate** | +1 / +2 / +3 nos níveis 5, 11 e 17, em **todos** os Testes de Ataque. **Não é renomeação de nada** — a v0.1 não tinha escalada de acerto própria | 26 |
| **Cones de Luz e Sobreposição** | Equipamento icônico, com Bônus Maior e Efeito Condicional | 25 |
| **Relíquias**, 6 slots, 4 tiers, Conjuntos de 2 e 4 | Idem, e com a regra de aquisição por marco | 25 |
| **Ressonâncias I a IV** | Os marcos de poder dos níveis 5, 10, 15 e 20 | 26 |
| **Catálogo de condições** | A v0.1 tinha condições espalhadas, algumas com nome e **sem regra** | 21 |
| **Descanso Curto e Longo** | Três Bênçãos da v0.1 diziam "uma vez por descanso" sem que descanso existisse | 23 |
| **Vantagem e Desvantagem** | A v0.1 distribuía Vantagem em quatro Raças e várias Bênçãos **sem nunca definir** | 02 |
| **Acerto crítico** | Idem: usado, nunca definido. **20 natural**, dobra só os dados base | 18 |
| **Teste de Ataque formal** | Com todas as parcelas, e o atributo de cada uma das 6 categorias de arma | 18 |
| **Os 6 Testes de Resistência** | Nomes fechados, atributos definidos, Eficiência desde o nível 1 | 22 |
| **Distâncias** | Fecha a escala Pessoal → Extrema que a v0.1 citava em 15 lugares sem definir | 18 |
| **Regra de alvos em área** | A v0.1 falava de dano em área sem dizer **quantos alvos**. Agora: até 3, 4 nos Níveis 6 e 7, teto absoluto 6 | 16 |
| **Surpresa** | Gatilho de DT 13 no início do combate | 19 |
| **Esforço Total** | Troca declarada de ações por movimento | 18 |
| **Intervir** | A v0.1 mandava "impedir com a Reação Intervir" sem escrever a Reação | 18 |
| **Progressão por marco narrativo** | Sem pontos de experiência, com tabela mestra de 1 a 20 sem nível vazio | 26 |
| **Níveis de Habilidade 6 e 7** | A faixa 1-20 pede mais teto. As **5 linhas originais ficaram intactas** | 16 |
| **Buff, Debuff e Passivas com tabela** | A v0.1 dizia "o jogador fará juntamente do mestre": promissória, não tabela | 16 |
| **Bestiário** | **32 fichas nominais**, cinco faixas, três tipos, com ficha padronizada de 15 campos e tabela de âncoras | 28 |
| **Orçamento de encontro** | `dano do grupo por Ciclo × 4`, com as quatro composições equivalentes | 27 |
| **DT por faixa de nível** | Com Trivial, Sucesso Automático e as cinco DTs de subsistema como lista fechada | 27 |
| **Guia do Mestre** | Montagem de encontro, aprovação de Habilidade criada, recompensas, casos-limite | 27 |
| **Ambientação** | Aeons, **Stellaron**, **Fragmentum**, **Expresso Astral**, 8 facções, 6 locais, 20 ganchos | 27 |
| **Técnicas e Créditos** | Uso de poder fora de combate e preços de referência por faixa | 24 |
| **Apêndice de balanceamento** | As contas abertas, parcela por parcela, faixa por faixa | 29 |
| **Fichas** | Personagem, Memoespírito, Trilha de Ação, Decisões da Mesa, referência rápida | 29 |
| **Glossário** | Todo termo oficial, mais os aposentados com o nome novo ao lado | 30 |
| **Falhe para frente** | Regra nomeada: falha em Perícia não trava a cena | 02 |

### 4.3 O que a v1.0 declarou fora de escopo

Registrado para não voltar como surpresa: **economia de créditos completa** (o livro traz preços de referência, não um subsistema econômico), **regras de nave e viagem interestelar**, **campanha pronta** e **suplementos de cenário**. Nada disso é citado como regra em nenhuma página — que era justamente o defeito central da v0.1, regra nomeada apontando para subsistema que não existe.

---

## Parte 5 — Normalização de nomenclatura

A v0.1 usava, em alguns lugares, vocabulário emprestado de outros jogos e, em outros, dois nomes para a mesma coisa. A v1.0 fechou um nome por conceito. **A lista completa, com o termo antigo de um lado e o oficial do outro, está no capítulo 30.** Os casos que mudam leitura de regra:

| v0.1 | v1.0 | O que estava em jogo |
|---|---|---|
| "ação bônus" | **Ação Complementar** | Ver 2.8 |
| "ação comum" | **No lugar do seu Ataque Básico** | Não era categoria de ação |
| "rodada" / "turno do grupo" | **Ciclo** · **Turno** (de um só) | A Fila de Ação precisa distinguir os dois |
| "derrubar o turno em N casas" | **Atrasar em N casas** | Ganhou teto e ordem de operação |
| "DoT" | **Dano Contínuo** (DC) | Sigla inglesa, nunca definida |
| "HP" | **PV** | Duas siglas para a mesma estatística |
| "+1 de distância" | **+1 Distância de Movimento** **ou** **+2 de Velocidade** | A mesma frase significava **duas coisas diferentes** em Bênçãos diferentes. Foi o caso mais perigoso da lista |
| "ação adicional limitada" | **Ação Extra** | Com lista fechada e teto de 1 por Ciclo |
| "barra de resistência" | **Tenacidade** | "Resistência" já é Perícia e Resistência a Elemento |

---

## Parte 6 — Índice de decisões

Uma linha por decisão que mudou algo que você escreveu. A última coluna é sua: marque e devolva.

| # | Decisão | Seção | Impacto se revertida | Eu discordo |
|---|---|---|---|---|
| 1 | Faixa de nível 1-10 → **1-20** | — | Decisão sua, não nossa | [ ] |
| 2 | Bônus de Atributo: **13 cai para +1** | 2.1 | Desloca a tabela inteira a partir do 13 | [ ] |
| 3 | Esquiva: **Defesa + Eficiência** | 2.2 | Attrition vai de 73-81% para ~89% | [ ] |
| 4 | Médias de dado por **`(N+1)/2`** | 2.3 | Subestima o dano em até 17% | [ ] |
| 5 | Eficiência reespaçada (**9 e 10** mudam) | 2.4 | DT e Defesa de inimigo sem teto | [ ] |
| 6 | **PV fixo** no lugar dos dados de vida | 2.5 | Caça de nível 1 com 2 PV volta a ser possível | [ ] |
| 7 | **Avatar no nível 17** | 2.6 | 15 níveis sem capstone | [ ] |
| 8 | **Teto de 8 Habilidades** | 2.7 | 20 blocos de texto por ficha no nível 20 | [ ] |
| 9 | "ação bônus" → **Ação Complementar** | 2.8 | Termo que o sistema não define | [ ] |
| 10 | Cláusula "**força do causador**" aposentada | 2.9 | Move o dano por Ciclo em 5-8% por dado | [ ] |
| 11 | **RD** definida, teto e Armadura Pesada 2 RD | 3.1 | Personagem de nível 2 invulnerável | [ ] |
| 12 | **Porcentagem de PV** aposentada | 3.2 | Mesma Bênção valendo 19× mais no Boss | [ ] |
| 13 | Tenacidade: **neutro reduz metade** | 3.3 | Metade do grupo fora do subsistema | [ ] |
| 14 | Cura de Nível 5: **`10d20`** | 3.4 | PV deixa de ser recurso | [ ] |
| 15 | Perícias: **mínimo 2**, Sintonia fixa, Atenção → Percepção Mental | 3.5 | 1 Perícia escolhida com Sincronia 8 | [ ] |
| 16 | **To na sua mente** por Teste de Força de Vontade | 3.6 | Teste oposto sem regra de empate | [ ] |
| 17 | **Armaduras** reescalonadas | 3.6 | -5 em Testes, maior penalidade do jogo | [ ] |
| 18 | **Executado** movido para o capítulo 23 | 3.6 | Regra geral escondida numa Raça | [ ] |
| 19 | **Congelamento** não tira o turno de Elite e Boss | 3.7 | Boss fora da Fila metade do combate | [ ] |
| 20 | **Morrendo:** Força de Vontade DT 10, sem Eficiência | 3.8 | Estado sem teste nem DT | [ ] |
| 21 | **Memoespírito** ancorado no dono; Evoluções em 8, 14 e 20 | 3.9 | Companheiro irrelevante a partir do nível 10 | [ ] |
| 22 | **PH** pelo tamanho da mesa | 3.10 | Dano por Ciclo dobra na faixa alta | [ ] |
| 23 | **Ultimate** com Nível equivalente | 3.11 | Impossível aprovar criação de ninguém | [ ] |
| 24 | **Nome** consolidado, sem o aviso | 3.12 | — | [ ] |
| 25 | **Bênçãos:** 12 escritas, 10 adquiridas, três tiers | 2.6 | Dois personagens do mesmo Caminho ficam idênticos | [ ] |
| 26 | **Níveis de Habilidade 1-7** (as 5 primeiras intactas) | 4.2 | Teto de dano baixo demais para 20 níveis | [ ] |
| 27 | **Área:** até 3 alvos (4 nos Níveis 6-7), teto 6 | 4.2 | Uma Habilidade apagando o encontro inteiro | [ ] |
| 28 | **Especialização de Combate** (nova) | 4.2 | Acerto cresceria só pela Eficiência | [ ] |

---

> **A regra deste documento.** Se você discordar de uma linha, o livro muda — não o contrário. O que cada entrada oferece é o **preço** da mudança, para você decidir com a conta na mão. E se o preço parecer alto demais em alguma delas, é porque o número que você escreveu estava carregando mais peso do que parecia.

**Resumo do que mudou, em uma frase:** nada da sua identidade saiu, nove números seus mudaram com justificativa, quatro Caminhos foram escritos do zero e tudo que a v0.1 citava sem definir passou a ter regra.
