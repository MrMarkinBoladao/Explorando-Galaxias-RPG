# Capítulo 28 — Bestiário

Este capítulo é a caixa de ferramentas do Mestre. Ele tem três partes, nesta ordem de utilidade:

1. A **ficha padronizada** de inimigo, com todos os campos que o combate deste livro exige.
2. A **tabela de âncoras**, que preenche cada um desses campos por faixa de nível e por tipo de inimigo. Nenhum campo da ficha obriga você a inventar número.
3. **32 fichas nominais**, das cinco faixas, dos três tipos, prontas para colocar na mesa hoje.

> **A promessa deste capítulo:** você nunca precisa calcular um inimigo. Escolha a faixa, escolha o tipo, copie a linha, dê um nome e escolha as Fraquezas. O bicho está balanceado pelo orçamento do capítulo 27, e as contas de onde ele vem estão no apêndice do capítulo 29.

---

## 28.1 A ficha padronizada

Toda ficha de inimigo deste livro tem **os mesmos quinze campos**, sempre na mesma ordem:

| # | Campo | O que é | De onde vem |
|---|---|---|---|
| 1 | **Nome** | Como o bicho aparece na mesa | você |
| 2 | **Nível** | A **faixa** dele: 1-4, 5-8, 9-12, 13-16 ou 17-20 | você |
| 3 | **Tipo** | **Comum**, **Elite** ou **Boss** | você |
| 4 | **PV** | Pontos de Vida | **âncora** (28.3) |
| 5 | **Defesa** | O número contra o qual o grupo rola o Teste de Ataque | **âncora** |
| 6 | **RD** | Redução de Dano, subtraída de **cada instância** (capítulo 18) | **âncora** |
| 7 | **Tenacidade** | Valor **máximo** da barra. Só inimigos têm (capítulo 20) | **âncora** |
| 8 | **Velocidade** | A VEL que define a casa dele na Fila (capítulo 19) | **âncora** |
| 9 | **Teste de Ataque** | O bônus que ele soma ao d20 para acertar o grupo | **âncora** |
| 10 | **Dano por acerto** | O que cada ataque dele causa, em dados e média | **âncora** |
| 11 | **DT dos efeitos** | A DT contra a qual o **grupo** rola Teste de Resistência (capítulo 22) | **âncora** |
| 12 | **Teste de Resistência** | O bônus que **ele** soma quando a Habilidade de um personagem exige Teste de Resistência | **âncora** |
| 13 | **Fraquezas e Resistências** | Quais Elementos ferem mais e quais ferem menos (capítulo 20) | **quantas**: âncora · **quais**: você |
| 14 | **Ações especiais** | De 1 a 3, com recarga contada em Ciclos | você, pela régua de 28.4 |
| 15 | **Na Fila** | A VEL dele e se ele tem **Firmeza** (capítulo 19) | decorre do Tipo |

**O formato que este capítulo usa**, e que você pode copiar à mão num cartão:

```
NOME DO BICHO                         Tipo · Facção · faixa de nível
PV ___   Defesa ___   RD ___   Tenacidade ___   VEL ___
Ataque +___    DT dos efeitos ___    Teste de Resistência +___
Fraquezas: ___________    Resistências: ___________
Ataques:   nome (alcance, Elemento) — dados · média ___
Especiais: nome (recarga) — efeito
Na Fila:   VEL ___, com / sem Firmeza
```

---

## 28.2 Como ler a ficha

Nove regras governam **todo** inimigo deste livro, inclusive os que você criar. Elas não são repetidas em cada ficha — estão aqui uma vez, e valem sempre.

**1. Inimigos não têm Esquiva nem Intervir.** As duas são Reações de personagem (capítulo 18). A defesa de um inimigo é **PV, Defesa e RD**, e nada mais. Um inimigo só tem Reação se a ficha dele declarar uma entre as ações especiais, e ela **nunca** é um bônus de Defesa.

**2. Inimigos não acumulam Energia e não têm Ultimate.** A ficha não tem campo de Energia. O equivalente à Ultimate de um Boss é uma **ação especial com recarga contada em Ciclos**, declarada na ficha. É simplificação deliberada: você já rastreia a Fila, a Tenacidade e as condições de todo mundo.

**3. Elite e Boss têm Firmeza.** Some todas as casas de Atraso do Ciclo, divida por 2 arredondando para baixo, mínimo 1 casa **no total do Ciclo**, teto de 2 casas (capítulo 19). Comum **não** tem Firmeza e tem teto de 3 casas.

**4. Elite e Boss não perdem o turno por Congelamento.** Eles são Atrasados em 2 casas e **não podem usar ação especial no turno seguinte**. Comum perde o turno (capítulo 19). Tirar a ação especial de um Boss costuma valer mais que o dano.

**5. Quantas ações agressivas cada tipo tem por turno:**

| Tipo | Por turno | Por Ciclo, na prática |
|---|---|---|
| **Comum** | 1 ataque | 1 ação agressiva |
| **Elite** | 1 ataque, mais **1 ação especial a cada 2 Ciclos** | 1,5 ações agressivas |
| **Boss** | **2 ataques**, ou 1 ataque + 1 ação especial | 2 ações agressivas |

Essa é a premissa que sustenta o orçamento do capítulo 27. Um Boss que age uma vez por turno é metade de um Boss; um Comum que age duas vezes custa o dobro do que você pagou por ele.

**6. A Tenacidade é pequena de propósito.** Os números da coluna já contam que **boa parte dos ataques do grupo erra** — a Redução de Tenacidade é condicionada ao acerto (capítulo 20). A cadência que a tabela entrega é: **Comum** quebra no primeiro ataque sério que receber, **Elite** quase todo Ciclo, **Boss** a cada **2 Ciclos**.

**7. Quantas Fraquezas, e o contrato que vem com elas.**

| Tipo | Fraquezas |
|---|---|
| **Comum** | 1 a 2 |
| **Elite** | 3 |
| **Boss** | 4 |

> **O contrato de encontro da Fraqueza:** monte a cena de modo que **pelo menos 3 dos Elementos do grupo apareçam como Fraqueza** entre os inimigos presentes. As fichas deste capítulo trazem Fraquezas sugeridas; **troque-as livremente** para cumprir o contrato. Um encontro que não cumpre isso é um encontro deliberadamente mais duro e dura cerca de **1 Ciclo a mais** — ferramenta legítima de tensão, desde que você saiba que está usando ela. A regra inteira, com o porquê, está no capítulo 27.

**8. Resistência é endurecimento, não orçamento.** Uma Resistência tira 2 dados do ataque (conservando sempre 1 dado) e derruba a Redução de Tenacidade para **1 ponto fixo**. Isso **não** está no orçamento de PV: um inimigo com Resistência ao Elemento certo é mais duro do que a ficha dele sugere. Use com parcimônia, e nunca contra o único Elemento que o grupo tem em dobro.

**9. O que inimigo não faz.** Ele não recebe a condição **Quebrado** de ninguém a não ser pela própria Quebra; ele não gera nem gasta **PH**; ele não tem **Esforço**; e ele não aplica **Congelamento** em personagem jogador — personagens não têm Tenacidade, logo não existe efeito de Quebra vindo deles. Um inimigo de Gelo aplica **Lentidão** ou Dano Contínuo, que é o que as fichas deste capítulo usam.

---

## 28.3 Âncoras: a tabela que preenche qualquer ficha

**Esta é a tabela mestra do bestiário.** Treze colunas, cinco faixas, três tipos. Toda ficha deste capítulo foi preenchida a partir dela, e toda ficha que você criar também deve ser.

| Faixa | PV Comum | PV Elite | PV Boss | Defesa C / E / B | RD C / E / B | Tenacidade C / E / B | VEL C / E / B | Ataque | Dano por acerto C / E / B | DT dos efeitos C / E / B | Teste de Resistência C / E / B | Fraquezas C / E / B |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1-4** | **50** | **120** | **305** | 13 / 15 / 16 | 0 / 2 / 4 | 3 / 5 / 10 | 11 / 12 / 13 | **+7** | **3 / 7 / 10** | 12 / 13 / 14 | +1 / +2 / +3 | 1-2 / 3 / 4 |
| **5-8** | **70** | **160** | **410** | 16 / 18 / 19 | 0 / 2 / 4 | 3 / 6 / 11 | 12 / 13 / 15 | **+9** | **7 / 13 / 20** | 14 / 15 / 16 | +3 / +4 / +5 | 1-2 / 3 / 4 |
| **9-12** | **95** | **225** | **580** | 19 / 21 / 22 | 0 / 3 / 6 | 4 / 7 / 12 | 13 / 15 / 16 | **+11** | **9 / 19 / 28** | 16 / 17 / 18 | +4 / +5 / +6 | 1-2 / 3 / 4 |
| **13-16** | **125** | **295** | **750** | 20 / 22 / 23 | 0 / 3 / 6 | 4 / 6 / 12 | 14 / 16 / 18 | **+12** | **12 / 24 / 36** | 17 / 18 / 19 | +5 / +6 / +7 | 1-2 / 3 / 4 |
| **17-20** | **155** | **365** | **935** | 24 / 26 / 27 | 0 / 4 / 8 | 4 / 7 / 13 | 15 / 17 / 19 | **+13** | **16 / 32 / 48** | 19 / 20 / 21 | +7 / +8 / +9 | 1-2 / 3 / 4 |

Três leituras que valem a pena, porque elas explicam o formato de todas as fichas abaixo:

- **O Dano por acerto é um por tipo, não um por faixa.** Comum bate **1/3**, Elite **2/3** e Boss **1** do valor da faixa. O Boss é a âncora: é ele que calibra a Defesa do personagem e as **4 a 7 pancadas** até alguém chegar a Morrendo. Um Comum que bate como um Boss faz um encontro de 7 Comuns custar sete vezes o que você pagou.
- **A Tenacidade de Elite e de Comum é baixa de propósito.** Num encontro de 3 Elites ou de 7 Comuns, a Redução de Tenacidade do grupo **se reparte** entre eles. Um Comum que nunca sofre Quebra não participa do melhor subsistema do jogo.
- **O Teste de Resistência do inimigo é `Eficiência da faixa −1 / Eficiência / Eficiência +1`.** Contra a DT de Habilidade de um personagem típico (15 / 17 / 18 / 19 / 21 nas cinco faixas), o inimigo falha em **65% / 60% / 55%** conforme o tipo — a mesma janela do acerto do grupo. **Não existe inimigo sem esse número.**

### Dano por acerto, convertido em dados

A âncora é uma **média**. Estas são as expressões que este capítulo usa, e toda média impressa aqui é `número de dados × (lados + 1) ÷ 2`, arredondada para baixo (capítulo 02):

| Faixa | Comum | Elite | Boss |
|---|---|---|---|
| **1-4** | `1d6` · **3** | `2d6` · **7** | `3d6` · **10** |
| **5-8** | `2d6` · **7** | `3d8` · **13** | `4d8 + 2` · **20** |
| **9-12** | `2d8` · **9** | `4d8 + 1` · **19** | `5d10 + 1` · **28** |
| **13-16** | `3d6 + 2` · **12** | `4d10 + 2` · **24** | `6d10 + 3` · **36** |
| **17-20** | `3d8 + 3` · **16** | `5d12` · **32** | `7d12 + 3` · **48** |

Se você preferir não rolar o dano do inimigo, **use a média direto**. Ela é o número do orçamento, e a mesa não vai sentir diferença nenhuma — além de andar mais rápido.

---

## 28.4 Como criar um inimigo

Sete passos. O quinto é o único que exige criatividade; os outros são cópia.

**1. Escolha a faixa.** A faixa do inimigo é a faixa do **grupo**, não a do conceito. Um bandido de rua na faixa 17-20 tem 155 PV e isso é correto: ele não é um bandido qualquer, é um bandido que sobreviveu até aqui.

**2. Escolha o tipo.** Comum é unidade de pelotão. Elite é o nome que o grupo vai lembrar. Boss é a cena.

**3. Copie a linha da tabela de 28.3.** Nove números, sem conta nenhuma.

**4. Escolha as Fraquezas** — quantas pela tabela, quais pelo contrato de encontro (28.2, regra 7). Resistência, só se você quer endurecer de propósito.

**5. Escreva os ataques e as ações especiais.** Aqui está a régua, e ela é curta:

> **Ataque normal:** causa o **Dano por acerto** da ficha. Um inimigo pode ter dois ou três ataques diferentes — alcances e Elementos diferentes — mas **todos causam o mesmo dano**. A variedade está no alcance, no Elemento e no efeito, nunca no número.
>
> **Ação especial de dano:** até **1,5 vez** o Dano por acerto da ficha num alvo único, **ou** o Dano por acerto cheio **por alvo** quando pega 2 ou 3 alvos. Recarga de **2 ou 3 Ciclos**, declarada na ficha.
>
> **Ação especial de controle:** aplica uma condição do **capítulo 21** — nada de condição nova — ou força um Teste de Resistência contra a **DT dos efeitos** da ficha. Se ela também causa dano, use o Dano por acerto normal, não o aumentado.
>
> **Uma ação especial ocupa uma das ações agressivas do turno** (28.2, regra 5). Ela é o **pico de dano que a média esconde**, e é o momento em que o grupo precisa de uma Ultimate de cura pronta — não um bônus de graça por cima do ataque.

**6. Decida o comportamento na Fila.** A VEL vem da tabela. Firmeza decorre do tipo. A única decisão sua é **quem ele ataca**, e vale escrever isso na ficha em uma linha: "vai no de menor PV", "vai em quem curou por último", "vai em quem o feriu".

**7. Dê um nome e uma frase.** Uma frase. É ela que a mesa vai lembrar, não os 225 PV.

> **Exemplo completo, do zero, em um minuto.** O grupo é de nível 10 e eu quero um carcereiro de prisão orbital, Elite.
> Faixa **9-12**, tipo **Elite**: PV **225**, Defesa **21**, RD **3**, Tenacidade **7**, VEL **15**, Ataque **+11**, Dano **`4d8 + 1` · 19**, DT dos efeitos **17**, Teste de Resistência **+5**, **3 Fraquezas**.
> O grupo tem Fogo, Vento, Gelo e Físico. Pelo contrato, pego três deles: **Fogo, Vento e Físico**.
> Ataques: um cassetete de choque (Pessoal, Raio) e um lançador de rede (Média, Físico), **os dois a 19**.
> Ação especial, recarga 2 Ciclos: **Trancafiar** — o alvo faz Teste de Reflexos contra **DT 17**; se falhar, recebe **Lentidão** por 2 turnos.
> Na Fila: VEL 15, com Firmeza. Vai em quem está mais longe do grupo.
> Pronto. Nenhuma conta foi feita.

---

## 28.5 Bosses com fases

Um Boss com fases é o mesmo Boss duas ou três vezes: **o PV é uma barra só**, e a fase vira quando a barra cruza um limiar. Isso mantém o orçamento intacto e dá à cena a virada que ela precisa.

**As cinco regras das fases:**

1. **O PV não se multiplica.** Os 935 PV de um Boss da faixa 17-20 são 935 no total, repartidos entre as fases. Fase nova **não** cura e **não** acrescenta barra, a menos que a ficha diga explicitamente — e as deste capítulo não dizem.
2. **A fase nova troca, não soma.** O **dano por Ciclo** da ficha é o mesmo em todas as fases: duas ações agressivas no Dano por acerto da faixa. O que muda é a **forma** — alvo único vira área, dano direto vira Dano Contínuo, dois ataques viram um ataque e uma ação especial.
3. **A Tenacidade pode cair, nunca subir.** Ela **volta ao máximo** na virada de fase (é uma barra nova para o grupo derrubar, e isso já é o custo), e o valor dela nunca passa do publicado em 28.3 para a faixa.
4. **As Fraquezas mudam, e o grupo é avisado.** Mudar as 4 Fraquezas na virada é o coração da mecânica: ela obriga a mesa a reavaliar quem bate em quem. **Anuncie as Fraquezas novas em voz alta** no momento da virada, ou dê um teste de identificação de graça. Esconder isso transforma a fase 2 em adivinhação.
5. **A virada acontece no fim do turno do Boss**, nunca no meio de uma ação do grupo, e **ela não gasta a ação dele**. O grupo termina o Ciclo sabendo o que mudou.

> **Por quê a virada é no fim do turno dele:** se ela acontecesse no instante em que a barra cruza o limiar, metade de uma Habilidade de área resolveria contra as Fraquezas antigas e metade contra as novas, e a mesa pararia para discutir ordem de resolução. No fim do turno dele, todo mundo vê a mudança acontecer de uma vez — e quem Atrasou o Boss ganhou um Ciclo inteiro de fase antiga, o que é exatamente o prêmio que o controle deveria dar.

**Cinco dos seis Bosses deste capítulo têm fases.** O sexto — o Pretor Vazio-Nove, faixa 5-8 — é de fase única de propósito, como modelo do Boss direto: ele é a parede que o grupo aprende a derrubar antes de a mesa ganhar truques.

---

## 28.6 Faixa 1-4 — o Fragmentum e as primeiras trincheiras

Nesta faixa o grupo luta contra **coisas**: matéria que foi gente, carcaças que esqueceram de parar, e a infantaria mais barata da Legião da Antimatéria. Os números são pequenos e as decisões já são de verdade.

> **Os números desta faixa:** Comum 50 PV · Elite 120 PV · Boss 305 PV. Ataque de todos: **+7**.

### Casco Oco

*Comum · Fragmentum · faixa 1-4*

> *"Ainda dá para ler o nome dele no crachá."*

A primeira coisa que o Fragmentum faz com um corpo é soldar a ferramenta na mão. O resto leva semanas.

| Campo | Valor |
|---|---|
| **PV** | 50 |
| **Defesa** | 13 |
| **RD** | 0 |
| **Tenacidade** | 3 |
| **Velocidade** | 11 |
| **Teste de Ataque** | +7 |
| **DT dos efeitos** | 12 |
| **Teste de Resistência** | +1 |
| **Fraquezas** | **Físico**, **Fogo** |
| **Resistências** | — |

**Ataques**

- **Braço fundido** (Pessoal, Físico): `1d6` · média **3**

**Ações especiais** — nenhuma.

**Na Fila:** VEL 11, **sem Firmeza**. Avança em linha reta no alvo mais próximo e não recua nunca.

---

### Larva Fuliginosa

*Comum · Fragmentum · faixa 1-4*

> *"Elas não atacam você. Elas atacam o lugar onde você está."*

Vêm em bando, estouram quando morrem e deixam no ar uma poeira que arde na garganta por horas.

| Campo | Valor |
|---|---|
| **PV** | 50 |
| **Defesa** | 13 |
| **RD** | 0 |
| **Tenacidade** | 3 |
| **Velocidade** | 11 |
| **Teste de Ataque** | +7 |
| **DT dos efeitos** | 12 |
| **Teste de Resistência** | +1 |
| **Fraquezas** | **Fogo**, **Vento** |
| **Resistências** | — |

**Ataques**

- **Mordida de cinza** (Pessoal, Fogo): `1d6` · média **3**

**Ações especiais**

- **Estouro** (quando ela cai a 0 PV, uma vez): cada criatura a Distância **Pessoal** dela faz um **Teste de Reflexos contra DT 12**. Quem falha recebe **Queimadura** por 2 turnos.

**Na Fila:** VEL 11, **sem Firmeza**. Nunca aparece sozinha: use 3 a 5 por cena, e deixe a mesa descobrir o Estouro do jeito difícil.

---

### Esporo Rancoroso

*Comum · Fragmentum · faixa 1-4*

> *"Parece um tronco. Até abrir."*

Um nó de matéria corrompida que finge ser paisagem. É a armadilha mais honesta do Fragmentum: ele só pega quem passa perto.

| Campo | Valor |
|---|---|
| **PV** | 50 |
| **Defesa** | 13 |
| **RD** | 0 |
| **Tenacidade** | 3 |
| **Velocidade** | 11 |
| **Teste de Ataque** | +7 |
| **DT dos efeitos** | 12 |
| **Teste de Resistência** | +1 |
| **Fraquezas** | **Fogo** |
| **Resistências** | — |

**Ataques**

- **Chicote de raiz** (Curta, Físico): `1d6` · média **3**

**Ações especiais**

- **Agarrar** (recarga 2 Ciclos): um alvo a até Distância Curta faz **Teste de Potência Física contra DT 12**. Se falhar, recebe **Lentidão** por 2 turnos.

**Na Fila:** VEL 11, **sem Firmeza**. Tem **1 Fraqueza só** — é o exemplo de Comum na ponta baixa da coluna, e ele é notavelmente mais chato de Quebrar por causa disso.

---

### Peão da Antimatéria

*Comum · Legião da Antimatéria · faixa 1-4*

> *"Eles não querem o planeta. Eles querem que ele deixe de existir."*

Carne descartável da Legião: um macacão selado, um rifle de ferrolho e doutrina suficiente para não correr.

| Campo | Valor |
|---|---|
| **PV** | 50 |
| **Defesa** | 13 |
| **RD** | 0 |
| **Tenacidade** | 3 |
| **Velocidade** | 11 |
| **Teste de Ataque** | +7 |
| **DT dos efeitos** | 12 |
| **Teste de Resistência** | +1 |
| **Fraquezas** | **Físico**, **Raio** |
| **Resistências** | — |

**Ataques**

- **Rifle de ferrolho** (Longa, Físico): `1d6` · média **3**
- **Coronhada** (Pessoal, Físico): `1d6` · média **3**

**Ações especiais**

- **Fogo de supressão** (recarga 2 Ciclos): escolha **2 alvos** a até uma Distância um do outro. Cada um faz **Teste de Reflexos contra DT 12**; quem falha recebe `1d6` · **3** de dano Físico e fica **Marcado** por 1 turno.

**Na Fila:** VEL 11, **sem Firmeza**. Dois ataques na ficha, **um por turno**: ele escolhe o alcance, não dobra o dano.

---

### Sentinela Enferrujada

*Comum · Autômato · faixa 1-4*

> *"O protocolo dela expirou há oitenta anos. Ninguém avisou."*

Máquina de vigilância civil que continua cumprindo uma ordem que ninguém mais lembra de ter dado.

| Campo | Valor |
|---|---|
| **PV** | 50 |
| **Defesa** | 13 |
| **RD** | 0 |
| **Tenacidade** | 3 |
| **Velocidade** | 11 |
| **Teste de Ataque** | +7 |
| **DT dos efeitos** | 12 |
| **Teste de Resistência** | +1 |
| **Fraquezas** | **Raio**, **Imaginário** |
| **Resistências** | — |

**Ataques**

- **Bastão de contenção** (Pessoal, Raio): `1d6` · média **3**

**Ações especiais**

- **Holofote de identificação** (recarga 2 Ciclos): um alvo fica **Marcado** por 2 turnos. Enquanto a marca durar, **todo** inimigo da cena some o +1 dela contra esse alvo — é a única marca do bestiário que não é exclusiva de quem aplicou, e é por isso que ela é uma máquina de vigilância e não um soldado.

**Na Fila:** VEL 11, **sem Firmeza**. **Máquina sem consciência: não pode Executar** ninguém (capítulo 23).

---

### Capataz Oco

*Elite · Fragmentum · faixa 1-4*

> *"A voz dele ainda dá ordens. Só não são ordens de trabalho."*

Quando o Fragmentum pega alguém que mandava nos outros, ele mantém a parte que mandava.

| Campo | Valor |
|---|---|
| **PV** | 120 |
| **Defesa** | 15 |
| **RD** | 2 |
| **Tenacidade** | 5 |
| **Velocidade** | 12 |
| **Teste de Ataque** | +7 |
| **DT dos efeitos** | 13 |
| **Teste de Resistência** | +2 |
| **Fraquezas** | **Físico**, **Fogo**, **Imaginário** |
| **Resistências** | **Quântico** |

**Ataques**

- **Marreta soldada** (Pessoal, Físico): `2d6` · média **7**

**Ações especiais**

- **Chamado de turno** (recarga 3 Ciclos): **2 Cascos Ocos** entram na cena. Eles entram pela VEL nas casas restantes do Ciclo (capítulo 19).
- **Esmagar** (recarga 2 Ciclos): um alvo a Distância Pessoal recebe `3d6` · **10** de dano Físico e faz **Teste de Potência Física contra DT 13**; se falhar, recebe **Lentidão** por 1 turno.

**Na Fila:** VEL 12, **com Firmeza**. Prioriza quem causou mais dano a ele no Ciclo anterior.

> **Leia a Resistência a Quântico com cuidado.** Contra o personagem de Quântico da mesa, este Elite tira 2 dados **do ataque desse personagem** — a Resistência penaliza quem ataca, não quem defende (20.2) — e só perde **1 ponto** de Tenacidade por acerto. Se o grupo tem **dois** personagens de Quântico, troque a Resistência por outro Elemento ou tire ela: você não quer dois jogadores sentados.

---

### Sargento de Trincheira

*Elite · Legião da Antimatéria · faixa 1-4*

> *"Formação! A antimatéria não espera!"*

O primeiro inimigo da campanha que tem um plano. Ele não é mais forte que o grupo — ele é mais organizado.

| Campo | Valor |
|---|---|
| **PV** | 120 |
| **Defesa** | 15 |
| **RD** | 2 |
| **Tenacidade** | 5 |
| **Velocidade** | 12 |
| **Teste de Ataque** | +7 |
| **DT dos efeitos** | 13 |
| **Teste de Resistência** | +2 |
| **Fraquezas** | **Raio**, **Gelo**, **Vento** |
| **Resistências** | — |

**Ataques**

- **Fuzil de assalto** (Longa, Físico): `2d6` · média **7**
- **Baioneta** (Pessoal, Físico): `2d6` · média **7**

**Ações especiais**

- **Marcar alvo prioritário** (recarga 2 Ciclos): um alvo fica **Marcado** por 2 turnos **para todos os Peões da Antimatéria da cena**, e cada Peão que atacar o alvo marcado causa `1d6` · **3** normalmente, com o +1 da marca no Teste de Ataque.
- **Granada de fragmentação** (recarga 3 Ciclos): **até 3 alvos** a até uma Distância um do outro fazem **Teste de Reflexos contra DT 13**. Quem falha recebe `2d6` · **7** de dano Físico e **Sangramento** por 2 turnos; quem passa recebe **metade** do dano e nenhum Sangramento.

**Na Fila:** VEL 12, **com Firmeza**. Fica atrás dos Peões e usa a marca no personagem de menor PV.

---

### O Afogado do Poço Sete

*Boss · Fragmentum · faixa 1-4 · **2 fases***

> *"Sete turnos desceram. O poço devolveu um."*

Dezenove mineiros, três escavadeiras e uma veia de minério que não devia ter sido aberta. O Fragmentum fundiu tudo numa coisa só, e ela subiu.

| Campo | Valor |
|---|---|
| **PV** | **305** (barra única: fase 1 de 305 a 153, fase 2 de 152 a 0) |
| **Defesa** | 16 |
| **RD** | 4 |
| **Tenacidade** | 10 (volta ao máximo na virada de fase) |
| **Velocidade** | 13 |
| **Teste de Ataque** | +7 |
| **DT dos efeitos** | 14 |
| **Teste de Resistência** | +3 |

**Fase 1 — A massa (305 a 153 PV)**

| Campo | Valor |
|---|---|
| **Fraquezas** | **Fogo**, **Raio**, **Vento**, **Imaginário** |
| **Tenacidade** | 10 |

**Ataques** — 2 por turno, qualquer combinação:

- **Pá de dragline** (Curta, Físico): `3d6` · média **10**
- **Jato de lama quente** (Média, Fogo): `3d6` · média **10**

**Ação especial**

- **Engolir** (recarga 3 Ciclos; ocupa uma das 2 ações do turno): um alvo a Distância Pessoal faz **Teste de Potência Física contra DT 14**. Se falhar, recebe `3d8 + 2` · **15** de dano Físico e **Lentidão** por 2 turnos. Se passar, recebe **metade** do dano e nenhuma Lentidão.

**Fase 2 — Os rostos (152 a 0 PV)**

A massa se abre e os dezenove rostos aparecem, todos falando ao mesmo tempo. **Anuncie as Fraquezas novas em voz alta.**

| O que muda | De | Para |
|---|---|---|
| **Fraquezas** | Fogo, Raio, Vento, Imaginário | **Gelo**, **Quântico**, **Imaginário**, **Físico** |
| **Tenacidade** | 10 | **10** (volta ao máximo) |
| **Dano** | 2 ataques de `3d6` · 10 | **1 ataque** de `3d6` · 10 **+ 1 ação especial por turno** |
| **Ataque novo** | — | **Coro** (Longa, Imaginário) |

**Ataques e ações da fase 2** — 1 ataque + 1 ação especial por turno:

- **Pá de dragline** (Curta, Físico): `3d6` · média **10**
- **Coro** (Longa, Imaginário, ação especial, **sem recarga**): **até 3 alvos** a até uma Distância um do outro fazem **Teste de Resistência Mental contra DT 14**. Quem falha recebe `3d6` · **10** de dano Imaginário; quem passa recebe **metade** e nada mais.

> **Por quê a fase 2 não bate mais forte.** Ela bate **diferente**: o dano por Ciclo continua sendo duas ações no valor da faixa, mas uma delas agora pega até três personagens e exige Teste de Resistência em vez de rolar contra a Defesa. Quem tinha Armadura Pesada e Defesa 17 parou de estar seguro, e o grupo tem que se espalhar. Isso é a virada — não um multiplicador.

**Na Fila:** VEL 13, **com Firmeza**. Na fase 1 vai no alvo mais próximo; na fase 2 vai onde o Coro pegar mais gente.

> **Como esse combate costuma andar.** Um grupo de 4 no nível 3 entrega cerca de **83 de dano por Ciclo** contra um perfil de Boss. São **3,7 Ciclos** para derrubar os 305 PV, com a virada de fase caindo entre o segundo e o terceiro Ciclo — exatamente onde ela faz a mesa endireitar a coluna. A conta aberta está no capítulo 29.

---

## 28.7 Faixa 5-8 — a Legião em formação e os ternos da Corporação

Agora o grupo é um problema reconhecido. A Legião da Antimatéria manda unidades de verdade, e a **Corporação da Paz Interastral** descobre que há um passivo ambulante no balanço dela. Esta é a faixa em que o inimigo começa a ter procedimento.

> **Os números desta faixa:** Comum 70 PV · Elite 160 PV · Boss 410 PV. Ataque de todos: **+9**.

### Fuzileiro da Legião

*Comum · Legião da Antimatéria · faixa 5-8*

> *"O Peão aponta. O Fuzileiro acerta."*

Infantaria treinada, armadura selada, dois anos de trincheira. Não corre, não negocia e não atira sem apoio.

| Campo | Valor |
|---|---|
| **PV** | 70 |
| **Defesa** | 16 |
| **RD** | 0 |
| **Tenacidade** | 3 |
| **Velocidade** | 12 |
| **Teste de Ataque** | +9 |
| **DT dos efeitos** | 14 |
| **Teste de Resistência** | +3 |
| **Fraquezas** | **Físico**, **Raio** |
| **Resistências** | — |

**Ataques**

- **Carabina de pulso** (Longa, Físico): `2d6` · média **7**
- **Faca de trincheira** (Pessoal, Físico): `2d6` · média **7**

**Ações especiais**

- **Fogo cruzado** (recarga 2 Ciclos): escolha um alvo que esteja ao alcance de **outro** Fuzileiro da cena. Ele recebe `2d6` · **7** de dano Físico e fica **Marcado** por 1 turno.

**Na Fila:** VEL 12, **sem Firmeza**. Use em pares ou em quatro. Um Fuzileiro sozinho é uma cena de passagem.

---

### Dron de Vigilância Pacificadora

*Comum · Corporação da Paz Interastral · Autômato · faixa 5-8*

> *"Sorria. Isto é uma apólice."*

A Corporação não manda soldados primeiro. Manda câmeras com permissão de atirar.

| Campo | Valor |
|---|---|
| **PV** | 70 |
| **Defesa** | 16 |
| **RD** | 0 |
| **Tenacidade** | 3 |
| **Velocidade** | 12 |
| **Teste de Ataque** | +9 |
| **DT dos efeitos** | 14 |
| **Teste de Resistência** | +3 |
| **Fraquezas** | **Raio**, **Quântico** |
| **Resistências** | — |

**Ataques**

- **Agulha sedativa** (Média, Físico): `2d6` · média **7**

**Ações especiais**

- **Notificação de infração** (recarga 2 Ciclos): um alvo faz **Teste de Resistência Mental contra DT 14**. Se falhar, fica **Silenciado** por 1 turno — a papelada chega na cabeça dele junto com o anúncio.

**Na Fila:** VEL 12, **sem Firmeza**. **Máquina sem consciência: não Executa.** Foge quando fica sozinho, e isso não é covardia: é o seguro dele vencendo.

---

### Devoto do Silêncio

*Comum · Culto da Inexistência · faixa 5-8*

> *"Ele agradece cada ferida. Em voz muito baixa."*

Fanático que encontrou paz na ideia de que nada disso importa. Ele não luta para vencer: luta para encurtar.

| Campo | Valor |
|---|---|
| **PV** | 70 |
| **Defesa** | 16 |
| **RD** | 0 |
| **Tenacidade** | 3 |
| **Velocidade** | 12 |
| **Teste de Ataque** | +9 |
| **DT dos efeitos** | 14 |
| **Teste de Resistência** | +3 |
| **Fraquezas** | **Fogo**, **Imaginário** |
| **Resistências** | — |

**Ataques**

- **Punhal de oração** (Pessoal, Físico): `2d6` · média **7**, e o alvo recebe **Sangramento** por 2 turnos

**Ações especiais**

- **Litania** (recarga 3 Ciclos): um alvo a até Distância Média faz **Teste de Força de Vontade contra DT 14**. Se falhar, recebe **Vulnerável** por 2 turnos — **+1 dado de dano de qualquer fonte da Inexistência** na cena.

**Na Fila:** VEL 12, **sem Firmeza**. Ataca quem está mais ferido, sempre.

> **Um Comum que aplica Sangramento no ataque normal é o limite do tipo.** O Sangramento tira 5% dos PV máximos do alvo por turno, com teto de `3 × Eficiência` (capítulo 21) — num personagem de 120 PV na faixa 5-8, isso é 6 por turno. É um Comum caro de ignorar, e é assim que um Comum vira ameaça sem ganhar um ponto de PV.

---

### Centurião Catafracto

*Elite · Legião da Antimatéria · faixa 5-8*

> *"A armadura dele foi fechada por dentro. Ele não pretende sair."*

Uma tonelada de blindagem soldada em volta de um oficial que assinou um contrato sem cláusula de saída.

| Campo | Valor |
|---|---|
| **PV** | 160 |
| **Defesa** | 18 |
| **RD** | 2 |
| **Tenacidade** | 6 |
| **Velocidade** | 13 |
| **Teste de Ataque** | +9 |
| **DT dos efeitos** | 15 |
| **Teste de Resistência** | +4 |
| **Fraquezas** | **Raio**, **Quântico**, **Imaginário** |
| **Resistências** | **Físico** |

**Ataques**

- **Maça de impacto** (Pessoal, Físico): `3d8` · média **13**
- **Lança-arpéu** (Média, Físico): `3d8` · média **13**, e o alvo é **puxado 1 Distância** na direção do Centurião

**Ações especiais**

- **Avanço de aríete** (recarga 2 Ciclos): ele se move **2 Distâncias** e ataca ao chegar: `4d8 + 1` · média **19** de dano Físico, e o alvo faz **Teste de Potência Física contra DT 15** ou recebe **Lentidão** por 1 turno.
- **Selar visor** (recarga 3 Ciclos, Reação): declare depois de o grupo declarar uma Habilidade contra ele. Até o fim do próximo turno dele, a **RD dele sobe para 4**. Fim.

**Na Fila:** VEL 13, **com Firmeza**. Puxa o personagem de menor PV para perto e fica em cima dele.

> **A Reação dele não é um bônus de Defesa, e isso é regra, não detalhe.** Inimigo nenhum deste livro ganha Defesa por Reação (28.2, regra 1). O que o Centurião faz é dobrar a **RD**, que subtrai de cada instância e tem teto próprio (capítulo 18) — um efeito que o grupo responde com dado maior, não com bônus de acerto.

---

### Auditora de Risco

*Elite · Corporação da Paz Interastral · faixa 5-8*

> *"Eu não vim prender vocês. Vim precificar vocês."*

Terno impecável, maleta blindada, dois drones de escolta e autoridade para liquidar um ativo problemático no local.

| Campo | Valor |
|---|---|
| **PV** | 160 |
| **Defesa** | 18 |
| **RD** | 2 |
| **Tenacidade** | 6 |
| **Velocidade** | 13 |
| **Teste de Ataque** | +9 |
| **DT dos efeitos** | 15 |
| **Teste de Resistência** | +4 |
| **Fraquezas** | **Físico**, **Fogo**, **Vento** |
| **Resistências** | — |

**Ataques**

- **Pistola de execução contratual** (Longa, Físico): `3d8` · média **13**
- **Estilete de lacre** (Pessoal, Quântico): `3d8` · média **13**

**Ações especiais**

- **Cláusula de perda** (recarga 2 Ciclos): um alvo faz **Teste de Força de Vontade contra DT 15**. Se falhar, fica **Marcado** por 3 turnos e **Vulnerável** por 2 — e todo Dron de Vigilância da cena passa a atacá-lo preferencialmente.
- **Liquidação antecipada** (recarga 3 Ciclos): contra um alvo que esteja **Marcado** por ela, um ataque de `4d8 + 1` · média **19** de dano Físico.

**Na Fila:** VEL 13, **com Firmeza**. Marca primeiro, cobra depois. Entra em cena com 2 a 4 Drons de Vigilância.

---

### Pretor Vazio-Nove

*Boss · Legião da Antimatéria · faixa 5-8 · **fase única***

> *"Nove planetas. Nove notas de rodapé."*

O oficial de campo que a Legião manda quando quer o assunto encerrado. Armadura de comando, dois canhões de ombro e uma paciência administrativa que assusta mais que os canhões.

| Campo | Valor |
|---|---|
| **PV** | 410 |
| **Defesa** | 19 |
| **RD** | 4 |
| **Tenacidade** | 11 |
| **Velocidade** | 15 |
| **Teste de Ataque** | +9 |
| **DT dos efeitos** | 16 |
| **Teste de Resistência** | +5 |
| **Fraquezas** | **Fogo**, **Gelo**, **Raio**, **Imaginário** |
| **Resistências** | — |

**Ataques** — 2 por turno, qualquer combinação:

- **Canhão de ombro** (Longa, Físico): `4d8 + 2` · média **20**
- **Lâmina de comando** (Pessoal, Físico): `4d8 + 2` · média **20**

**Ações especiais**

- **Salva de antimatéria** (recarga 2 Ciclos; ocupa uma das 2 ações do turno): **até 3 alvos** a até uma Distância um do outro fazem **Teste de Reflexos contra DT 16**. Quem falha recebe `4d8 + 2` · **20** de dano Físico; quem passa recebe **metade** do dano.
- **Ordem de cerco** (recarga 3 Ciclos; ocupa uma das 2 ações do turno): **3 Fuzileiros da Legião** entram em cena, e todo Fuzileiro presente ganha **+1 no Teste de Ataque** até o fim do próximo turno do Pretor.
- **Retaliação de comando** (1 vez por combate, Reação): quando ele sofre **Quebra**, o personagem que a causou faz **Teste de Reflexos contra DT 16** ou recebe `4d8 + 2` · **20** de dano Físico.

**Na Fila:** VEL 15, **com Firmeza**. Age antes de quase todo o grupo. Prioriza quem cura.

> **Por quê este Boss não tem fases.** Porque a mesa ainda está aprendendo a derrubar um Boss, e um Boss de fase única ensina uma coisa por vez: a barra de 410 PV, a Tenacidade 11 que cede a cada 2 Ciclos, a Firmeza que come metade do controle do grupo, e a **Retaliação de comando** — que é a primeira vez que a Quebra, a melhor coisa que o grupo faz, cobra um preço. Fases vêm depois, quando o grupo já sabe o básico de cor.
>
> **Um aviso de orçamento:** a Ordem de cerco gasta uma das duas ações agressivas do turno dele e acrescenta **3 Comuns** à cena. Isso **aumenta o orçamento do encontro** (capítulo 27). Se você vai usar a Ordem de cerco, monte a cena com o Pretor **sozinho** — ele é o encontro inteiro, e os reforços são o que ele tem em vez de acompanhantes iniciais.

---

## 28.8 Faixa 9-12 — ordens de caça e aplausos

Esta é a faixa em que o grupo deixa de lutar contra monstros e passa a lutar contra **gente com motivo**. A **Aliança Xianzhou** emite uma ordem de caça; os **Tolos Mascarados** acham o grupo divertido, o que é pior. Nenhum dos dois é mal por ser mal, e isso muda a mesa.

> **Os números desta faixa:** Comum 95 PV · Elite 225 PV · Boss 580 PV. Ataque de todos: **+11**.

### Lanceiro da Frota de Jade

*Comum · Aliança Xianzhou · faixa 9-12*

> *"Não é pessoal. Está escrito."*

Soldado de uma frota que caça há seis séculos. Disciplina de pedra, lança de liga leve e nenhuma vontade de conversar sobre a ordem de caça.

| Campo | Valor |
|---|---|
| **PV** | 95 |
| **Defesa** | 19 |
| **RD** | 0 |
| **Tenacidade** | 4 |
| **Velocidade** | 13 |
| **Teste de Ataque** | +11 |
| **DT dos efeitos** | 16 |
| **Teste de Resistência** | +4 |
| **Fraquezas** | **Gelo**, **Quântico** |
| **Resistências** | — |

**Ataques**

- **Lança de jade** (Curta, Físico): `2d8` · média **9**
- **Dardo de contenção** (Média, Gelo): `2d8` · média **9**

**Ações especiais**

- **Formação de muro** (recarga 2 Ciclos): enquanto houver **outro** Lanceiro a Distância Pessoal dele, os dois ganham **RD 2** até o fim do próximo turno dele.

**Na Fila:** VEL 13, **sem Firmeza**. **Ser racional: pode Executar** um personagem em Morrendo (capítulo 23) — e, pela doutrina da frota, ele faz isso sem hesitar se o alvo for o nome da ordem de caça.

---

### Palhaço de Pólvora

*Comum · Tolos Mascarados · faixa 9-12*

> *"Ele ri antes da explosão. Isso é o aviso."*

Nem todo Tolo Mascarado tem um plano. Alguns só têm fósforos e um senso de oportunidade.

| Campo | Valor |
|---|---|
| **PV** | 95 |
| **Defesa** | 19 |
| **RD** | 0 |
| **Tenacidade** | 4 |
| **Velocidade** | 13 |
| **Teste de Ataque** | +11 |
| **DT dos efeitos** | 16 |
| **Teste de Resistência** | +4 |
| **Fraquezas** | **Gelo**, **Imaginário** |
| **Resistências** | — |

**Ataques**

- **Buquê incendiário** (Média, Fogo): `2d8` · média **9**, e o alvo recebe **Queimadura** por 2 turnos

**Ações especiais**

- **Troca de lugar** (recarga 2 Ciclos): ele e **outro Palhaço de Pólvora** da cena trocam de posição e de casa na Fila. Todo efeito que estava marcado contra um passa a valer contra o outro, **inclusive Marcado e Vulnerável** — mas **não** Dano Contínuo, que fica em quem o recebeu.

**Na Fila:** VEL 13, **sem Firmeza**. Use três. A Troca de lugar só é piada quando a mesa perde a conta de quem é quem.

---

### Centenário Enlouquecido

*Comum · Xianzhou · faixa 9-12*

> *"Seiscentos anos de memória num crânio feito para oitenta."*

A longevidade de Xianzhou cobra juros. Quando a conta chega, o que sobra tem a força de um veterano e o julgamento de nada.

| Campo | Valor |
|---|---|
| **PV** | 95 |
| **Defesa** | 19 |
| **RD** | 0 |
| **Tenacidade** | 4 |
| **Velocidade** | 13 |
| **Teste de Ataque** | +11 |
| **DT dos efeitos** | 16 |
| **Teste de Resistência** | +4 |
| **Fraquezas** | **Fogo**, **Imaginário** |
| **Resistências** | — |

**Ataques**

- **Golpe de memória antiga** (Pessoal, Físico): `2d8` · média **9**

**Ações especiais**

- **Lembrança alheia** (recarga 2 Ciclos): um alvo a até Distância Média faz **Teste de Resistência Mental contra DT 16**. Se falhar, recebe `2d8` · **9** de dano Imaginário e fica **Silenciado** por 1 turno.

**Na Fila:** VEL 13, **sem Firmeza**. Ataca quem falou com ele por último. **Ser racional, mas sem julgamento: não Executa.**

---

### Oficial-Lâmina da Frota de Jade

*Elite · Aliança Xianzhou · faixa 9-12*

> *"Eu assinei a sua sentença e eu vou cumpri-la. As duas coisas são meu trabalho."*

Xianzhouíta de três séculos, armadura de cerimônia, uma única espada e o costume de atacar duas vezes antes de a mesa entender que ela se mexeu.

| Campo | Valor |
|---|---|
| **PV** | 225 |
| **Defesa** | 21 |
| **RD** | 3 |
| **Tenacidade** | 7 |
| **Velocidade** | 15 |
| **Teste de Ataque** | +11 |
| **DT dos efeitos** | 17 |
| **Teste de Resistência** | +5 |
| **Fraquezas** | **Fogo**, **Vento**, **Quântico** |
| **Resistências** | — |

**Ataques**

- **Corte em arco** (Pessoal, Físico): `4d8 + 1` · média **19**
- **Estocada longa** (Curta, Físico): `4d8 + 1` · média **19**

**Ações especiais**

- **Sentença** (recarga 2 Ciclos): ela declara um alvo. Até o fim do combate, **ela só ataca esse alvo** enquanto ele estiver de pé, e os ataques dela contra ele somam **+2 no Teste de Ataque**. Em troca, ela **não usa nenhuma outra ação especial** contra mais ninguém.
- **Lâmina de encerramento** (recarga 3 Ciclos): contra o alvo da Sentença, um ataque de `5d10 + 1` · média **28** de dano Físico. Se o alvo cair a 0 PV com esse ataque, ela **recua um passo e espera** — a frota executa sentença, não cadáver.

**Na Fila:** VEL 15, **com Firmeza**. **Ser racional: pode Executar.** Não vai executar o alvo da Sentença enquanto houver testemunhas.

> **A Sentença é o modelo de ação especial que não dá dano nenhum e muda o combate inteiro.** Ela transforma um Elite em um relógio apontado para um jogador. A mesa responde com **Intervir** (capítulo 18), com cura, ou com a decisão desconfortável de deixar aquele personagem fora do alcance dela. Nenhuma dessas três é óbvia, e é por isso que ela funciona.

---

### Mestre de Cerimônias Mascarado

*Elite · Tolos Mascarados · faixa 9-12*

> *"Vocês chegaram no segundo ato. Não se preocupem, eu resumo."*

Ele não quer matar o grupo. Ele quer uma cena boa, e está disposto a matar o grupo para conseguir uma.

| Campo | Valor |
|---|---|
| **PV** | 225 |
| **Defesa** | 21 |
| **RD** | 3 |
| **Tenacidade** | 7 |
| **Velocidade** | 15 |
| **Teste de Ataque** | +11 |
| **DT dos efeitos** | 17 |
| **Teste de Resistência** | +5 |
| **Fraquezas** | **Físico**, **Gelo**, **Imaginário** |
| **Resistências** | **Quântico** |

**Ataques**

- **Bengala-estoque** (Pessoal, Quântico): `4d8 + 1` · média **19**
- **Confete cortante** (Média, Vento): `4d8 + 1` · média **19**

**Ações especiais**

- **Deixa!** (recarga 2 Ciclos): um alvo faz **Teste de Força de Vontade contra DT 17**. Se falhar, fica **Controlado** por **1 turno** (capítulo 21) — ele age no turno dele, com Ataque Básico, Ação de Movimento e Ação Complementar, sob a direção do Mestre de Cerimônias, e não gasta recurso nenhum.
- **Chuva de improviso** (recarga 3 Ciclos): **até 3 alvos** a até uma Distância um do outro fazem **Teste de Reflexos contra DT 17**. Quem falha recebe `4d8 + 1` · **19** de dano Vento e **Cisalhamento de Vento** com **2 acúmulos**; quem passa recebe **metade** do dano.

**Na Fila:** VEL 15, **com Firmeza**. **Ser racional: pode Executar** — e faz isso se, e só se, render uma fala melhor.

---

### O Dramaturgo de Mil Faces

*Boss · Tolos Mascarados · faixa 9-12 · **2 fases***

> *"Primeiro ato: vocês acham que estão lutando comigo."*

Ninguém sabe se o Dramaturgo é uma pessoa, um cargo ou uma piada que ficou grande demais. O que se sabe é que, quando a máscara cai, tem outra atrás.

| Campo | Valor |
|---|---|
| **PV** | **580** (barra única: fase 1 de 580 a 291, fase 2 de 290 a 0) |
| **Defesa** | 22 |
| **RD** | 6 |
| **Tenacidade** | 12 na fase 1, **9** na fase 2 (volta ao máximo na virada) |
| **Velocidade** | 16 |
| **Teste de Ataque** | +11 |
| **DT dos efeitos** | 18 |
| **Teste de Resistência** | +6 |

**Fase 1 — O elenco (580 a 291 PV)**

Ele luta à distância, atrás de dois figurantes, e o grupo passa o primeiro Ciclo inteiro batendo nas pessoas erradas.

| Campo | Valor |
|---|---|
| **Fraquezas** | **Físico**, **Gelo**, **Vento**, **Imaginário** |
| **Tenacidade** | 12 |

**Ataques** — 2 por turno, qualquer combinação:

- **Vara de contrarregra** (Curta, Imaginário): `5d10 + 1` · média **28**
- **Aplauso dirigido** (Longa, Quântico): `5d10 + 1` · média **28**

**Ações especiais**

- **Entra o dublê** (recarga 3 Ciclos; ocupa uma das 2 ações do turno): **2 Palhaços de Pólvora** entram na cena. Enquanto houver pelo menos um deles de pé, **todo ataque de alvo único contra o Dramaturgo** exige um **Teste de Percepção Mental contra DT 18** antes da rolagem; quem falha acerta um Palhaço em vez dele, resolvendo o ataque contra a ficha do Palhaço.
- **Reviravolta** (recarga 2 Ciclos; ocupa uma das 2 ações do turno): ele **Avança** ele mesmo em 2 casas (capítulo 19) e um alvo faz **Teste de Resistência Mental contra DT 18** ou fica **Vulnerável** por 2 turnos.

**Fase 2 — Nenhuma face (290 a 0 PV)**

A máscara cai e não tem rosto embaixo. Os figurantes param de se mexer. Ele para de atuar, e é agora que ele é perigoso.

| O que muda | De | Para |
|---|---|---|
| **Fraquezas** | Físico, Gelo, Vento, Imaginário | **Fogo**, **Raio**, **Quântico**, **Físico** |
| **Tenacidade** | 12 | **9** (volta ao máximo, e mais baixa) |
| **Dano** | 2 ataques de `5d10 + 1` · 28 | 1 ataque de `5d10 + 1` · 28 **+ 1 ação especial por turno** |
| **Entra o dublê** | disponível | **indisponível**: os Palhaços restantes ficam inertes e podem ser ignorados |
| **Ataque novo** | — | **Plateia vazia** (área, Imaginário) |

**Ataques e ações da fase 2** — 1 ataque + 1 ação especial por turno:

- **Vara de contrarregra** (Curta, Imaginário): `5d10 + 1` · média **28**
- **Plateia vazia** (ação especial, **sem recarga**): **todos** os personagens a até uma Distância um do outro, até 3, fazem **Teste de Força de Vontade contra DT 18**. Quem falha recebe `5d10 + 1` · **28** de dano Imaginário e fica **Silenciado** por 1 turno; quem passa recebe **metade** do dano e nada mais.
- **A última fala** (1 vez por combate, quando ele chega a **145 PV ou menos**; ocupa a ação especial do turno): ele **Avança** em 2 casas, e **até 3 alvos** fazem **Teste de Resistência Mental contra DT 18** ou recebem `7d10 + 4` · média **42** de dano Imaginário. Quem passa recebe metade.

> **Por quê a Tenacidade **cai** na fase 2.** Porque a fase 1 já cobrou do grupo um Ciclo de confusão e uma barra inteira de 12, e porque a graça da fase 2 é o grupo finalmente conseguir **bater no bicho certo**. Tenacidade 9 significa Quebra quase todo Ciclo no fim do combate — o grupo sente a virada a favor dele, mesmo levando mais dano. Fase nova nunca sobe a Tenacidade acima do publicado em 28.3; ela pode descer, e aqui desce de propósito.

**Na Fila:** VEL 16, **com Firmeza**. Na fase 1, ataca quem está menos ferido (ele quer que a cena dure). Na fase 2, ataca quem **mais** o feriu.

> **Aviso de orçamento, igual ao do Pretor:** o Entra o dublê acrescenta **2 Comuns** à cena e sobe o custo do encontro (capítulo 27). Monte o Dramaturgo **sozinho** — os dublês são o que ele tem em vez de acompanhantes iniciais, e a fase 2 devolve o orçamento ao desativá-los.

---

## 28.9 Faixa 13-16 — contratos e cinzéis

Aqui o grupo é um nome em uma lista. Os **Caçadores de Stellaron** querem o que o grupo está carregando; os **Cavaleiros da Beleza** querem o grupo, literalmente, como material. Nenhum dos dois manda um pelotão: manda um profissional.

> **Os números desta faixa:** Comum 125 PV · Elite 295 PV · Boss 750 PV. Ataque de todos: **+12**.
>
> **Repare na Tenacidade de Elite:** **6**, um ponto **abaixo** da faixa 9-12. Não é erro de impressão. A coluna é o valor derivado arredondado para número de mesa, e nesta faixa a derivação cai um pouco porque o mix de Habilidades que o PH sustenta muda (capítulo 29). O efeito prático é bom: Elite desta faixa Quebra **todo** Ciclo, e é exatamente o que um encontro de 3 Elites precisa para não virar uma parede.

### Noviço da Beleza

*Comum · Cavaleiros da Beleza · faixa 13-16*

> *"Ele já cortou tudo que sobrava dele. Agora precisa de você."*

Candidato à ordem. Metade do corpo é prótese de cerâmica branca, e ele considera isso progresso.

| Campo | Valor |
|---|---|
| **PV** | 125 |
| **Defesa** | 20 |
| **RD** | 0 |
| **Tenacidade** | 4 |
| **Velocidade** | 14 |
| **Teste de Ataque** | +12 |
| **DT dos efeitos** | 17 |
| **Teste de Resistência** | +5 |
| **Fraquezas** | **Físico**, **Fogo** |
| **Resistências** | — |

**Ataques**

- **Bisturi de cerâmica** (Pessoal, Físico): `3d6 + 2` · média **12**, e o alvo recebe **Sangramento** por 2 turnos

**Ações especiais**

- **Correção** (recarga 2 Ciclos): um alvo faz **Teste de Resistência Física contra DT 17**. Se falhar, recebe **Vulnerável** por 2 turnos — **+1 dado de dano de qualquer Cavaleiro da Beleza** na cena.

**Na Fila:** VEL 14, **sem Firmeza**. **Ser racional: pode Executar** — e para a ordem dele, isso não é matar, é terminar.

---

### Operativo de Campo dos Caçadores

*Comum · Caçadores de Stellaron · faixa 13-16*

> *"Ele não estava aqui no Ciclo passado. Ninguém sabe desde quando está."*

Os Caçadores não têm infantaria. Têm pessoas que trabalham sozinhas e aparecem em três lugares ao mesmo tempo.

| Campo | Valor |
|---|---|
| **PV** | 125 |
| **Defesa** | 20 |
| **RD** | 0 |
| **Tenacidade** | 4 |
| **Velocidade** | 14 |
| **Teste de Ataque** | +12 |
| **DT dos efeitos** | 17 |
| **Teste de Resistência** | +5 |
| **Fraquezas** | **Gelo**, **Quântico** |
| **Resistências** | — |

**Ataques**

- **Pistola suprimida** (Longa, Físico): `3d6 + 2` · média **12**
- **Fio de garrote** (Pessoal, Físico): `3d6 + 2` · média **12**, e o alvo faz **Teste de Potência Física contra DT 17** ou fica **Silenciado** por 1 turno

**Ações especiais**

- **Reposicionar** (recarga 2 Ciclos): ele se move **2 Distâncias** e, se terminar fora do alcance de todo personagem, **Avança** 2 casas na Fila do próximo Ciclo (capítulo 19).

**Na Fila:** VEL 14, **sem Firmeza**. Vai sempre em quem cura, e sai de perto depois. **Ser racional: pode Executar.**

---

### Autômato Taciturno

*Comum · Autômato de guerra · faixa 13-16*

> *"Modelo descontinuado. Munição, não."*

Plataforma de guerra antiga que alguém religou. Ela não fala, não negocia e não tem nada por onde ser convencida.

| Campo | Valor |
|---|---|
| **PV** | 125 |
| **Defesa** | 20 |
| **RD** | 0 |
| **Tenacidade** | 4 |
| **Velocidade** | 14 |
| **Teste de Ataque** | +12 |
| **DT dos efeitos** | 17 |
| **Teste de Resistência** | +5 |
| **Fraquezas** | **Raio**, **Vento** |
| **Resistências** | — |

**Ataques**

- **Metralha pesada** (Longa, Físico): `3d6 + 2` · média **12**

**Ações especiais**

- **Travar alvo** (recarga 2 Ciclos): um alvo fica **Marcado** por 3 turnos. Enquanto a marca durar, este autômato **não ataca mais ninguém** e some **+1 acúmulo de Marcado** por Ciclo, até o teto de **3** (capítulo 21).

**Na Fila:** VEL 14, **sem Firmeza**. **Máquina sem consciência: não Executa.** É a melhor demonstração do teto de 3 acúmulos de Marcado em toda a mesa: no terceiro Ciclo ele está em +3 e ninguém fora do alvo correu risco nenhum.

---

### Escultor de Carne

*Elite · Cavaleiros da Beleza · faixa 13-16*

> *"Fique parado. Vai doer mais se você se mexer, e vai ficar torto."*

Cavaleiro pleno. Seis braços-ferramenta, um avental limpo e convicção genuína de que está fazendo um favor.

| Campo | Valor |
|---|---|
| **PV** | 295 |
| **Defesa** | 22 |
| **RD** | 3 |
| **Tenacidade** | 6 |
| **Velocidade** | 16 |
| **Teste de Ataque** | +12 |
| **DT dos efeitos** | 18 |
| **Teste de Resistência** | +6 |
| **Fraquezas** | **Fogo**, **Gelo**, **Raio** |
| **Resistências** | — |

**Ataques**

- **Leque de lâminas** (Pessoal, Físico): `4d10 + 2` · média **24**, e o alvo recebe **Sangramento** por 2 turnos
- **Serra de arco** (Curta, Físico): `4d10 + 2` · média **24**

**Ações especiais**

- **Anestesia** (recarga 2 Ciclos): um alvo faz **Teste de Resistência Física contra DT 18**. Se falhar, recebe **Lentidão** por 2 turnos e **Silenciado** por 1.
- **Obra em progresso** (recarga 3 Ciclos): contra um alvo que esteja com **Sangramento**, um ataque de `6d10 + 3` · média **36** de dano Físico. Se o ataque acertar, o Sangramento é **renovado** por mais 2 turnos.

**Na Fila:** VEL 16, **com Firmeza**. Escolhe o alvo pela estética e não muda de ideia. **Ser racional: pode Executar.**

> **Ele é o exemplo de Elite construído em volta de uma condição.** O ataque normal aplica Sangramento; a ação especial grande **exige** Sangramento. O grupo que remove a condição (Habilidade de Nível 4 ou maior, capítulo 21) desarma metade da ficha dele — e essa é a decisão que a ficha existe para provocar.

---

### Executora de Contrato

*Elite · Caçadores de Stellaron · faixa 13-16*

> *"Eu li o seu contrato. Você não leu."*

Especialista em encerramento. Chega sem escolta, com um dossiê completo sobre cada personagem e a paciência de quem já ganhou essa discussão antes.

| Campo | Valor |
|---|---|
| **PV** | 295 |
| **Defesa** | 22 |
| **RD** | 3 |
| **Tenacidade** | 6 |
| **Velocidade** | 16 |
| **Teste de Ataque** | +12 |
| **DT dos efeitos** | 18 |
| **Teste de Resistência** | +6 |
| **Fraquezas** | **Físico**, **Vento**, **Imaginário** |
| **Resistências** | **Gelo** |

**Ataques**

- **Revólver de ruptura** (Longa, Quântico): `4d10 + 2` · média **24**
- **Adaga de encerramento** (Pessoal, Físico): `4d10 + 2` · média **24**

**Ações especiais**

- **Dossiê** (recarga 2 Ciclos): ela nomeia um personagem e declara **em voz alta** uma Habilidade que ele usou neste combate. Até o fim do próximo turno dela, aquele personagem está **Silenciado** para Habilidades de **Nível 4 ou maior** (capítulo 21) e fica **Marcado** por 3 turnos.
- **Encerramento** (recarga 3 Ciclos): contra um alvo **Marcado** por ela, `6d10 + 3` · média **36** de dano Quântico, e o alvo faz **Teste de Reflexos contra DT 18** ou recebe **Embaraço** com **3 acúmulos** (capítulo 21).

**Na Fila:** VEL 16, **com Firmeza**. Abre no personagem que mais depende de uma única Habilidade. **Ser racional: pode Executar**, e é a única coisa do contrato dela que não é negociável.

---

### Vênia, a Primeira Obra

*Boss · Cavaleiros da Beleza · faixa 13-16 · **2 fases***

> *"Ela foi a primeira coisa que a ordem considerou terminada. Depois disso, a ordem não terminou mais nada."*

Vênia não é cavaleira. É o que os Cavaleiros fizeram antes de aprenderem a parar. Porcelana e cabo de aço do pescoço aos pés, e uma voz que ainda pede desculpa antes de cada golpe.

| Campo | Valor |
|---|---|
| **PV** | **750** (barra única: fase 1 de 750 a 376, fase 2 de 375 a 0) |
| **Defesa** | 23 |
| **RD** | 6 |
| **Tenacidade** | 12 nas duas fases (volta ao máximo na virada) |
| **Velocidade** | 18 |
| **Teste de Ataque** | +12 |
| **DT dos efeitos** | 19 |
| **Teste de Resistência** | +7 |

**Fase 1 — A obra acabada (750 a 376 PV)**

Movimentos perfeitos, simétricos, de uma lentidão deliberada. Ela luta como uma demonstração.

| Campo | Valor |
|---|---|
| **Fraquezas** | **Físico**, **Fogo**, **Raio**, **Quântico** |
| **Tenacidade** | 12 |

**Ataques** — 2 por turno, qualquer combinação:

- **Braço-cinzel** (Pessoal, Físico): `6d10 + 3` · média **36**
- **Fio de cabo** (Média, Físico): `6d10 + 3` · média **36**, e o alvo é **puxado 1 Distância**

**Ações especiais**

- **Simetria** (recarga 2 Ciclos; ocupa uma das 2 ações do turno): **2 alvos** fazem **Teste de Reflexos contra DT 19**. Quem falha recebe `6d10 + 3` · **36** de dano Físico e **Sangramento** por 2 turnos; quem passa recebe **metade** e nenhum Sangramento.
- **Retoque** (recarga 3 Ciclos; ocupa uma das 2 ações do turno): ela remove **todas** as condições que estão sobre ela e ganha **RD 2** extra até o fim do próximo turno dela. Ela **não** recupera PV e **não** recupera Tenacidade.

**Fase 2 — A rachadura (375 a 0 PV)**

A porcelana cede no ombro esquerdo, e o que estava dentro há trezentos anos vem junto. Ela para de pedir desculpa. **Anuncie as Fraquezas novas em voz alta.**

| O que muda | De | Para |
|---|---|---|
| **Fraquezas** | Físico, Fogo, Raio, Quântico | **Gelo**, **Vento**, **Imaginário**, **Quântico** |
| **Tenacidade** | 12 | **12** (volta ao máximo) |
| **Dano** | 2 ataques de `6d10 + 3` · 36 | 1 ataque de `6d10 + 3` · 36 **+ 1 ação especial por turno** |
| **Retoque** | disponível | **indisponível** |
| **Ataque novo** | — | **Desmoronar** (área, Físico) |

**Ataques e ações da fase 2** — 1 ataque + 1 ação especial por turno:

- **Braço-cinzel** (Pessoal, Físico): `6d10 + 3` · média **36**
- **Desmoronar** (ação especial, **sem recarga**): **até 3 alvos** a até uma Distância um do outro fazem **Teste de Reflexos contra DT 19**. Quem falha recebe `6d10 + 3` · **36** de dano Físico e **Lentidão** por 1 turno; quem passa recebe **metade** do dano e nada mais.
- **Terminem o trabalho** (1 vez por combate, quando ela chega a **150 PV ou menos**; ocupa a ação especial do turno): `9d10 + 5` · média **54** de dano Físico em **um** alvo a Distância Pessoal, resolvido por **Teste de Ataque** normal. Se o alvo cair a 0 PV, ela gasta o turno seguinte inteiro **parada**.

**Na Fila:** VEL 18, **com Firmeza**. Ela tem a maior VEL de inimigo da faixa e age antes de quase todo grupo — a Caça equipada ainda chega na frente dela, e isso é promessa de Caminho, não coincidência (capítulo 19).

> **Por quê o Retoque sai na fase 2.** Na fase 1 ele é o freio: o grupo investe em condições e vê as condições sumirem, o que ensina a mesa a guardar o controle para o momento certo. Na fase 2 ela não limpa mais nada — tudo que o grupo aplicar **fica**, e a cena acelera na direção do grupo. É a mesma lógica da Tenacidade do Dramaturgo: a fase final devolve poder para a mesa, mesmo entregando mais dano.

---

## 28.10 Faixa 17-20 — o Stellaron e o que anda com ele

Última faixa. Aqui o grupo não enfrenta mais organizações: enfrenta o que as organizações estavam tentando conter. Um **Stellaron** maduro não é um monstro — é uma condição do lugar, e tudo em volta dele já desistiu de ser o que era.

> **Os números desta faixa:** Comum 155 PV · Elite 365 PV · Boss 935 PV. Ataque de todos: **+13**.
>
> **O Comum desta faixa bate mais forte que o Boss da faixa 1-4** (16 contra 10) e tem três vezes o PV dele. É assim que se lê a tabela de âncoras: o tipo diz o papel na cena, a faixa diz o patamar do jogo. Um pelotão de "Comuns" aqui é um pelotão de pesadelos.

### Guarda Pretoriano da Antimatéria

*Comum · Legião da Antimatéria · faixa 17-20*

> *"A Legião tem exatamente duzentos deles. Nunca precisou de mais."*

Armadura de comando produzida em série, canhão de braço e um piloto que foi apagado e reescrito até só sobrar a função.

| Campo | Valor |
|---|---|
| **PV** | 155 |
| **Defesa** | 24 |
| **RD** | 0 |
| **Tenacidade** | 4 |
| **Velocidade** | 15 |
| **Teste de Ataque** | +13 |
| **DT dos efeitos** | 19 |
| **Teste de Resistência** | +7 |
| **Fraquezas** | **Raio**, **Imaginário** |
| **Resistências** | — |

**Ataques**

- **Canhão de braço** (Longa, Físico): `3d8 + 3` · média **16**
- **Punho de aríete** (Pessoal, Físico): `3d8 + 3` · média **16**

**Ações especiais**

- **Falange** (recarga 2 Ciclos): enquanto houver **outro** Guarda Pretoriano a Distância Pessoal dele, os dois ganham **RD 4** até o fim do próximo turno dele.

**Na Fila:** VEL 15, **sem Firmeza**. Nunca aparece sozinho, nunca em número ímpar, e a Falange é o motivo. **Ser racional, mas reescrito: não Executa** — não sobrou nada nele que decida isso.

---

### Escória de Stellaron

*Comum · Stellaron · faixa 17-20*

> *"É o chão. O chão se levantou."*

Perto de um Stellaron, a matéria para de concordar com a própria forma. A Escória é o que isso faz com um pedaço de cidade.

| Campo | Valor |
|---|---|
| **PV** | 155 |
| **Defesa** | 24 |
| **RD** | 0 |
| **Tenacidade** | 4 |
| **Velocidade** | 15 |
| **Teste de Ataque** | +13 |
| **DT dos efeitos** | 19 |
| **Teste de Resistência** | +7 |
| **Fraquezas** | **Gelo**, **Quântico** |
| **Resistências** | — |

**Ataques**

- **Avalanche curta** (Curta, Físico): `3d8 + 3` · média **16**

**Ações especiais**

- **Dividir** (quando ela cai a 0 PV, uma vez por Escória): **uma** Escória de Stellaron nova entra em cena com **metade dos PV** (78) e **sem** esta ação especial. Ela entra pela VEL nas casas restantes do Ciclo (capítulo 19).

**Na Fila:** VEL 15, **sem Firmeza**. **Besta sem consciência: não Executa.**

> **A Divisão é a única coisa do bestiário que multiplica inimigo sem ação de ninguém, e por isso ela é cortada duas vezes:** a filha tem **metade** do PV e **não** se divide de novo. Uma Escória custa, no total, 1,5 Comum de orçamento — conte assim na hora de montar a cena (capítulo 27). Três Escórias são, na verdade, quatro e meia.

---

### Arcanjo de Ferro-Vazio

*Elite · Legião da Antimatéria · faixa 17-20*

> *"Seis asas. Nenhuma delas serve para voar."*

O projeto mais caro da Legião: uma moldura de seis braços articulados em volta de um núcleo que não existe de verdade. Ele não é pilotado. Ele é **obedecido**.

| Campo | Valor |
|---|---|
| **PV** | 365 |
| **Defesa** | 26 |
| **RD** | 4 |
| **Tenacidade** | 7 |
| **Velocidade** | 17 |
| **Teste de Ataque** | +13 |
| **DT dos efeitos** | 20 |
| **Teste de Resistência** | +8 |
| **Fraquezas** | **Raio**, **Quântico**, **Imaginário** |
| **Resistências** | **Físico** |

**Ataques**

- **Varredura de seis lâminas** (Curta, Físico): `5d12` · média **32**
- **Lança de vazio** (Longa, Quântico): `5d12` · média **32**

**Ações especiais**

- **Negar** (recarga 2 Ciclos): um alvo faz **Teste de Resistência Mental contra DT 20**. Se falhar, fica **Silenciado** por 1 turno e perde **toda a Barreira e todos os PV temporários** que tiver (capítulos 15 e 23).
- **Coluna de ferro-vazio** (recarga 3 Ciclos): **até 3 alvos** a até uma Distância um do outro fazem **Teste de Reflexos contra DT 20**. Quem falha recebe `7d12 + 3` · média **48** de dano Quântico e **Embaraço** com **2 acúmulos**; quem passa recebe **metade** do dano e nenhum Embaraço.

**Na Fila:** VEL 17, **com Firmeza**. Abre em quem está com mais Barreira. **Máquina sem consciência: não Executa.**

> **Negar é a resposta do bestiário ao Caminho da Preservação**, e ela é deliberadamente dura: apaga Barreira e PV temporários de um personagem só, uma vez a cada 2 Ciclos, sem causar dano nenhum. A Preservação responde reaplicando — a Barreira dela é reaplicável, e o Arcanjo gasta meia ficha para apagar um turno de trabalho dela. É troca justa, e é exatamente o tipo de inimigo que faz um Caminho defensivo parecer necessário em vez de opcional.

---

### Arauto da Tempestade Vazia

*Elite · Culto da Inexistência · faixa 17-20*

> *"Ele não está atacando vocês. Ele está terminando a frase."*

Um devoto que chegou longe o bastante para que o Caminho responda. Tudo em volta dele está um pouco menos presente do que estava.

| Campo | Valor |
|---|---|
| **PV** | 365 |
| **Defesa** | 26 |
| **RD** | 4 |
| **Tenacidade** | 7 |
| **Velocidade** | 17 |
| **Teste de Ataque** | +13 |
| **DT dos efeitos** | 20 |
| **Teste de Resistência** | +8 |
| **Fraquezas** | **Físico**, **Fogo**, **Gelo** |
| **Resistências** | — |

**Ataques**

- **Sopro de ausência** (Média, Vento): `5d12` · média **32**, e o alvo recebe **Cisalhamento de Vento** com **1 acúmulo**
- **Mão aberta** (Pessoal, Imaginário): `5d12` · média **32**

**Ações especiais**

- **Rasgar a frase** (recarga 2 Ciclos): **até 3 alvos** fazem **Teste de Força de Vontade contra DT 20**. Quem falha recebe **Sangramento** por 2 turnos e **Vulnerável** por 2 turnos. Sem dano direto.
- **Tempestade** (recarga 3 Ciclos): **até 3 alvos** a até uma Distância um do outro fazem **Teste de Reflexos contra DT 20**. Quem falha recebe `7d12 + 3` · média **48** de dano Vento e **Cisalhamento de Vento** com **3 acúmulos**; quem passa recebe **metade** do dano e **1 acúmulo**.

**Na Fila:** VEL 17, **com Firmeza**. **Ser racional: pode Executar**, e ele considera isso um ato de gentileza.

> **Ele é a ficha que mostra Dano Contínuo do lado do Mestre.** Cisalhamento de Vento acumula até 5 e cada acúmulo é `1d6` por turno, ignorando RD (capítulos 20 e 21). Três acúmulos num grupo de quatro é `3d6` por turno em cada personagem, e nada na ficha de ninguém defende contra isso a não ser cura. É um dos quatro motivos pelos quais o grupo quer alguém cuidando dele (capítulo 27) — e aqui, na última faixa, o motivo fica explícito.

---

### O Germe de Pavor

*Boss · Stellaron · faixa 17-20 · **3 fases***

> *"O Stellaron não é o inimigo. O Stellaron é a gravidez."*

O que cresce dentro de um Stellaron maduro não tem forma própria: ele usa a do planeta. Quando o grupo chega, o chão já tem costelas.

| Campo | Valor |
|---|---|
| **PV** | **935** (barra única: fase 1 de 935 a 624, fase 2 de 623 a 312, fase 3 de 311 a 0) |
| **Defesa** | 27 |
| **RD** | 8 |
| **Tenacidade** | 13 / 13 / **10** (volta ao máximo em cada virada) |
| **Velocidade** | 19 |
| **Teste de Ataque** | +13 |
| **DT dos efeitos** | 21 |
| **Teste de Resistência** | +9 |

**Fase 1 — A casca (935 a 624 PV)**

Ele não se move. O terreno se move.

| Campo | Valor |
|---|---|
| **Fraquezas** | **Físico**, **Fogo**, **Gelo**, **Raio** |
| **Tenacidade** | 13 |

**Ataques** — 2 por turno, qualquer combinação:

- **Costela do chão** (Curta, Físico): `7d12 + 3` · média **48**
- **Vomitar escória** (Longa, Físico): `7d12 + 3` · média **48**

**Ação especial**

- **Parto falso** (recarga 3 Ciclos; ocupa uma das 2 ações do turno): **2 Escórias de Stellaron** entram em cena, **sem** a ação especial Dividir.

**Fase 2 — O interior (623 a 312 PV)**

A casca racha e o grupo vê o que estava sendo gerado. Ele ainda não tem corpo, então pega emprestado o de quem está perto. **Anuncie as Fraquezas novas em voz alta.**

| O que muda | De | Para |
|---|---|---|
| **Fraquezas** | Físico, Fogo, Gelo, Raio | **Fogo**, **Vento**, **Quântico**, **Imaginário** |
| **Tenacidade** | 13 | **13** (volta ao máximo) |
| **Dano** | 2 ataques de `7d12 + 3` · 48 | 1 ataque de `7d12 + 3` · 48 **+ 1 ação especial por turno** |
| **Parto falso** | disponível | **indisponível** |
| **Ação nova** | — | **Tomar emprestado** |

**Ataques e ações da fase 2** — 1 ataque + 1 ação especial por turno:

- **Costela do chão** (Curta, Físico): `7d12 + 3` · média **48**
- **Tomar emprestado** (ação especial, **sem recarga**): um alvo faz **Teste de Força de Vontade contra DT 21**. Se falhar, fica **Controlado** por **1 turno** (capítulo 21). Se passar, recebe `7d12 + 3` · **48** de dano Imaginário. **Nunca os dois.**

**Fase 3 — Nascido (311 a 0 PV)**

Ele desiste de copiar qualquer coisa e simplesmente acontece. A partir daqui o combate é uma corrida: ele bate em todo mundo, todo turno, e o grupo tem Tenacidade 10 para trabalhar.

| O que muda | De | Para |
|---|---|---|
| **Fraquezas** | Fogo, Vento, Quântico, Imaginário | **Físico**, **Gelo**, **Raio**, **Quântico** |
| **Tenacidade** | 13 | **10** (volta ao máximo, e mais baixa) |
| **Dano** | 1 ataque + 1 ação especial | **1 ação especial de área por turno**, e nada mais |
| **Tomar emprestado** | disponível | **indisponível** |

**Ação da fase 3** — 1 por turno, sem recarga:

- **Primeira respiração** (área, Quântico): **todos** os personagens a até uma Distância um do outro, até **3**, fazem **Teste de Resistência Física contra DT 21**. Quem falha recebe `7d12 + 3` · **48** de dano Quântico e **Embaraço** com **1 acúmulo**; quem passa recebe **metade** do dano e nada mais.
- **Sem desfecho** (1 vez por combate, quando ele chega a **100 PV ou menos**; ocupa a ação do turno): **todos** os personagens de pé fazem **Teste de Força de Vontade contra DT 21**. Quem falha recebe `10d12 + 7` · média **72** de dano Imaginário; quem passa recebe **metade**. Esta é a única ação do bestiário que pega a mesa inteira sem limite de alvos, e ela sai **uma vez**, perto do fim.

**Na Fila:** VEL 19, **com Firmeza**. VEL 19 é o teto de inimigo do livro: só uma Caça equipada chega na frente dele (capítulo 19). Ele não escolhe alvo — a fase 1 vai no mais próximo, a fase 2 em quem tem mais Presença, a fase 3 pega todo mundo.

> **Como ler o dano por Ciclo deste Boss, fase por fase.** Fase 1: duas ações de 48 em alvo único. Fase 2: uma de 48 mais um controle que **ou** controla **ou** bate. Fase 3: uma ação que entrega 48 em **até três personagens** — o mesmo orçamento de duas ações, distribuído. Em nenhuma das três fases o número por Ciclo sobe; o que muda é quantas fichas são atingidas e quanta escolha o grupo ainda tem. Isso é a regra 2 de 28.5 funcionando numa ficha de verdade.

---

### Vazia Coroada, Emanadora da Inexistência

*Boss · Emanadora · faixa 17-20 · **3 fases***

> *"Ela não quer que você morra. Ela quer que você concorde."*

Uma Emanadora é alguém a quem um Aeon respondeu. Esta respondeu à Inexistência, e o que voltou tem a forma de uma mulher muito calma com uma coroa que não toca a cabeça dela.

**É o inimigo de encerramento de campanha deste livro.** Monte-a sozinha. Ela é o encontro inteiro.

| Campo | Valor |
|---|---|
| **PV** | **935** (barra única: fase 1 de 935 a 624, fase 2 de 623 a 312, fase 3 de 311 a 0) |
| **Defesa** | 27 |
| **RD** | 8 |
| **Tenacidade** | 13 / **12** / **10** (volta ao máximo em cada virada) |
| **Velocidade** | 19 |
| **Teste de Ataque** | +13 |
| **DT dos efeitos** | 21 |
| **Teste de Resistência** | +9 |

**Fase 1 — A audiência (935 a 624 PV)**

Ela conversa. Entre as frases, mata.

| Campo | Valor |
|---|---|
| **Fraquezas** | **Fogo**, **Vento**, **Quântico**, **Imaginário** |
| **Tenacidade** | 13 |

**Ataques** — 2 por turno, qualquer combinação:

- **Gesto de dispensa** (Longa, Imaginário): `7d12 + 3` · média **48**
- **Coroa descendo** (Pessoal, Físico): `7d12 + 3` · média **48**

**Ações especiais**

- **Concordância** (recarga 2 Ciclos; ocupa uma das 2 ações do turno): um alvo faz **Teste de Força de Vontade contra DT 21**. Se falhar, recebe **Corrupção** com **3 acúmulos** (capítulo 21) e **Vulnerável** por 2 turnos. Sem dano direto.
- **Nada disso importou** (recarga 3 Ciclos; ocupa uma das 2 ações do turno): **até 3 alvos** fazem **Teste de Resistência Mental contra DT 21**. Quem falha recebe `7d12 + 3` · **48** de dano Imaginário e **Silenciado** por 1 turno; quem passa recebe **metade** do dano.

**Fase 2 — A coroa (623 a 312 PV)**

A coroa desce até a altura dos olhos dela e para de girar. Ela para de conversar. **Anuncie as Fraquezas novas em voz alta.**

| O que muda | De | Para |
|---|---|---|
| **Fraquezas** | Fogo, Vento, Quântico, Imaginário | **Físico**, **Gelo**, **Raio**, **Quântico** |
| **Tenacidade** | 13 | **12** (volta ao máximo) |
| **Dano** | 2 ataques de `7d12 + 3` · 48 | 1 ataque de `7d12 + 3` · 48 **+ 1 ação especial por turno** |
| **Concordância** | 3 acúmulos de Corrupção | **5 acúmulos**, o teto da condição |
| **Ação nova** | — | **Maré de Inexistência** |

**Ataques e ações da fase 2** — 1 ataque + 1 ação especial por turno:

- **Coroa descendo** (Pessoal, Físico): `7d12 + 3` · média **48**
- **Maré de Inexistência** (ação especial, **sem recarga**): **até 3 alvos** a até uma Distância um do outro fazem **Teste de Resistência Física contra DT 21**. Quem falha recebe **Sangramento** e **Queimadura** por 2 turnos, os dois com a Eficiência dela (**+8**); quem passa recebe só o Sangramento. **Esta ação não causa dano direto nenhum** — ela instala o relógio.
- **Concordância** (recarga 2 Ciclos, versão da fase 2): como na fase 1, com **5 acúmulos** de Corrupção.

**Fase 3 — Sem coroa (311 a 0 PV)**

Ela solta a coroa. A coroa não cai — fica onde estava, no ar, enquanto ela avança.

| O que muda | De | Para |
|---|---|---|
| **Fraquezas** | Físico, Gelo, Raio, Quântico | **Fogo**, **Gelo**, **Vento**, **Imaginário** |
| **Tenacidade** | 12 | **10** (volta ao máximo, e mais baixa) |
| **Dano** | 1 ataque + 1 ação especial | **2 ataques** de `7d12 + 3` · 48, outra vez |
| **Maré de Inexistência** | disponível | **indisponível**: os Danos Contínuos já aplicados **continuam** correndo |
| **Concordância** | disponível | **indisponível** |

**Ataques e ações da fase 3** — 2 ataques por turno:

- **Coroa descendo** (Pessoal, Físico): `7d12 + 3` · média **48**
- **Mão vazia** (Curta, Imaginário): `7d12 + 3` · média **48**
- **O nome dela** (1 vez por combate, quando ela chega a **120 PV ou menos**; ocupa as **duas** ações do turno): **até 3 alvos** fazem **Teste de Força de Vontade contra DT 21**. Quem falha recebe `10d12 + 7` · média **72** de dano Imaginário e **Silenciado** por 1 turno; quem passa recebe **metade** do dano. Ela diz o nome dela ao fazer isso, e é a única informação que o grupo leva dessa cena.

**Na Fila:** VEL 19, **com Firmeza**. **Ser racional: pode Executar** — e ela faz isso, sem pressa, em quem já estiver no chão com Corrupção.

> **O arco dela, em uma linha:** a fase 1 conversa e castiga erro de posicionamento, a fase 2 **para de causar dano direto** e instala Dano Contínuo em todo mundo — a única fase do bestiário em que o grupo perde PV sem ninguém rolar ataque contra a Defesa dele —, e a fase 3 volta a ser duas pancadas por turno, com o relógio da fase 2 ainda correndo por baixo. É o combate em que o grupo precisa ter sobrado cura, e é por isso que ele é o último.
>
> **O que o Mestre precisa rastrear nela, e nada além disso:** o PV (um número), a Tenacidade da fase atual (um número), as quatro Fraquezas da fase atual (uma linha), as duas recargas e, na fase 2, quem está com quais Danos Contínuos. Se isso for muito para a sua mesa, corte a Maré de Inexistência e use a fase 2 igual à fase 1 com as Fraquezas novas. O combate continua funcionando.

---

## 28.11 Índice do bestiário

**32 fichas:** 16 Comuns, 10 Elites e 6 Bosses, sendo **5 Bosses com fases**. As cinco faixas têm os três tipos.

| # | Nome | Tipo | Faixa | Facção ou origem | PV | Fraquezas sugeridas |
|---|---|---|---|---|---|---|
| 1 | Casco Oco | Comum | 1-4 | Fragmentum | 50 | Físico, Fogo |
| 2 | Larva Fuliginosa | Comum | 1-4 | Fragmentum | 50 | Fogo, Vento |
| 3 | Esporo Rancoroso | Comum | 1-4 | Fragmentum | 50 | Fogo |
| 4 | Peão da Antimatéria | Comum | 1-4 | Legião da Antimatéria | 50 | Físico, Raio |
| 5 | Sentinela Enferrujada | Comum | 1-4 | Autômato | 50 | Raio, Imaginário |
| 6 | Capataz Oco | Elite | 1-4 | Fragmentum | 120 | Físico, Fogo, Imaginário |
| 7 | Sargento de Trincheira | Elite | 1-4 | Legião da Antimatéria | 120 | Raio, Gelo, Vento |
| 8 | **O Afogado do Poço Sete** | **Boss, 2 fases** | 1-4 | Fragmentum | 305 | Fogo, Raio, Vento, Imaginário |
| 9 | Fuzileiro da Legião | Comum | 5-8 | Legião da Antimatéria | 70 | Físico, Raio |
| 10 | Dron de Vigilância Pacificadora | Comum | 5-8 | Corporação da Paz Interastral | 70 | Raio, Quântico |
| 11 | Devoto do Silêncio | Comum | 5-8 | Culto da Inexistência | 70 | Fogo, Imaginário |
| 12 | Centurião Catafracto | Elite | 5-8 | Legião da Antimatéria | 160 | Raio, Quântico, Imaginário |
| 13 | Auditora de Risco | Elite | 5-8 | Corporação da Paz Interastral | 160 | Físico, Fogo, Vento |
| 14 | **Pretor Vazio-Nove** | **Boss, fase única** | 5-8 | Legião da Antimatéria | 410 | Fogo, Gelo, Raio, Imaginário |
| 15 | Lanceiro da Frota de Jade | Comum | 9-12 | Aliança Xianzhou | 95 | Gelo, Quântico |
| 16 | Palhaço de Pólvora | Comum | 9-12 | Tolos Mascarados | 95 | Gelo, Imaginário |
| 17 | Centenário Enlouquecido | Comum | 9-12 | Xianzhou | 95 | Fogo, Imaginário |
| 18 | Oficial-Lâmina da Frota de Jade | Elite | 9-12 | Aliança Xianzhou | 225 | Fogo, Vento, Quântico |
| 19 | Mestre de Cerimônias Mascarado | Elite | 9-12 | Tolos Mascarados | 225 | Físico, Gelo, Imaginário |
| 20 | **O Dramaturgo de Mil Faces** | **Boss, 2 fases** | 9-12 | Tolos Mascarados | 580 | Físico, Gelo, Vento, Imaginário |
| 21 | Noviço da Beleza | Comum | 13-16 | Cavaleiros da Beleza | 125 | Físico, Fogo |
| 22 | Operativo de Campo dos Caçadores | Comum | 13-16 | Caçadores de Stellaron | 125 | Gelo, Quântico |
| 23 | Autômato Taciturno | Comum | 13-16 | Autômato de guerra | 125 | Raio, Vento |
| 24 | Escultor de Carne | Elite | 13-16 | Cavaleiros da Beleza | 295 | Fogo, Gelo, Raio |
| 25 | Executora de Contrato | Elite | 13-16 | Caçadores de Stellaron | 295 | Físico, Vento, Imaginário |
| 26 | **Vênia, a Primeira Obra** | **Boss, 2 fases** | 13-16 | Cavaleiros da Beleza | 750 | Físico, Fogo, Raio, Quântico |
| 27 | Guarda Pretoriano da Antimatéria | Comum | 17-20 | Legião da Antimatéria | 155 | Raio, Imaginário |
| 28 | Escória de Stellaron | Comum | 17-20 | Stellaron | 155 | Gelo, Quântico |
| 29 | Arcanjo de Ferro-Vazio | Elite | 17-20 | Legião da Antimatéria | 365 | Raio, Quântico, Imaginário |
| 30 | Arauto da Tempestade Vazia | Elite | 17-20 | Culto da Inexistência | 365 | Físico, Fogo, Gelo |
| 31 | **O Germe de Pavor** | **Boss, 3 fases** | 17-20 | Stellaron | 935 | Físico, Fogo, Gelo, Raio |
| 32 | **Vazia Coroada** | **Boss, 3 fases** | 17-20 | Emanadora da Inexistência | 935 | Fogo, Vento, Quântico, Imaginário |

**Os cinco inimigos com Resistência**, para você decidir de propósito e nunca por acidente: Capataz Oco (Quântico), Centurião Catafracto (Físico), Mestre de Cerimônias Mascarado (Quântico), Executora de Contrato (Gelo), Arcanjo de Ferro-Vazio (Físico).

### Montando a cena com estas fichas

Um encontro típico gasta o orçamento inteiro da faixa (capítulo 27), e estas são as quatro composições equivalentes:

| Composição | Exemplo pronto, faixa 1-4 | Exemplo pronto, faixa 17-20 | Duração esperada |
|---|---|---|---|
| **1 Boss + 1 Comum** | O Afogado do Poço Sete + 1 Casco Oco | O Germe de Pavor, **sozinho** (o Parto falso traz os Comuns) | **3 a 5 Ciclos** |
| **1 Elite + 4 Comuns** | Sargento de Trincheira + 4 Peões da Antimatéria | Arcanjo de Ferro-Vazio + 4 Guardas Pretorianos | 3 a 4 Ciclos |
| **3 Elites** | Capataz Oco + 2 Sargentos de Trincheira | 2 Arcanjos + 1 Arauto da Tempestade Vazia | 3 a 4 Ciclos, **o mais pesado dos quatro** em dano recebido |
| **7 Comuns** | 4 Larvas Fuliginosas + 3 Cascos Ocos | 4 Guardas Pretorianos + 2 Escórias | **2 a 3 Ciclos** |

> **Encontro de 3 ou mais inimigos resolve mais rápido que o de Boss, e isso é correto.** É o preço de colocar sete alvos na frente de uma Habilidade em área, e é uma das razões de existir o Caminho da Erudição. Encontro que gasta **metade** do orçamento é cena de passagem e deve durar 2 Ciclos.
>
> **Antes de pôr a cena na mesa, confira duas coisas:** (1) pelo menos **3 dos Elementos do grupo** aparecem como Fraqueza entre os inimigos presentes; (2) nenhuma Resistência da cena aponta para o Elemento de dois personagens ao mesmo tempo. São dez segundos de conferência e eles decidem se o combate vai ser divertido.

---

## Resumo do capítulo

| | |
|---|---|
| **A ficha** | 15 campos. **Todos** têm coluna de âncora em 28.3 ou são identidade do bicho |
| **Comum / Elite / Boss** | 1 ação agressiva por turno · 1 + especial a cada 2 Ciclos · **2** por turno |
| **PV por faixa** | Comum 50/70/95/125/155 · Elite 120/160/225/295/365 · Boss 305/410/580/750/935 |
| **Dano por acerto** | Comum **1/3**, Elite **2/3**, Boss **1** do valor da faixa: 3-7-10 / 7-13-20 / 9-19-28 / 12-24-36 / 16-32-48 |
| **Tenacidade** | Comum 3-4 · Elite 5-7 · Boss 10-13. Quebra: Comum no primeiro golpe sério, Elite quase todo Ciclo, Boss a cada 2 |
| **Fraquezas** | Comum 1-2 · Elite 3 · Boss 4. **Troque-as** para cumprir o contrato de encontro |
| **Inimigos não têm** | Esquiva, Intervir, Energia, Ultimate, PH nem Esforço |
| **Elite e Boss têm** | **Firmeza** (teto de 2 casas de Atraso) e **não perdem o turno por Congelamento** |
| **Ação especial** | até **1,5 ×** o dano da ficha em alvo único, ou o dano cheio **por alvo** em 2-3 alvos; recarga de 2 ou 3 Ciclos |
| **Fases** | barra de PV **única**; a fase **troca** e não soma; Tenacidade pode cair, nunca subir; Fraquezas novas **anunciadas em voz alta** |
| **O catálogo** | **32 fichas** — 16 Comuns, 10 Elites, 6 Bosses, **5 deles com fases** |

> **O que mudou da v0.1:** a v0.1 não tinha bestiário. Nenhum inimigo, nenhum número, nenhuma ficha — o Mestre tinha sete Elementos, uma barra de Tenacidade e nada em que bater. Este capítulo é, em volume, a maior adição da v1.0, e ele não inventou régua nenhuma: cada um dos 32 bichos foi preenchido a partir da mesma tabela de 13 colunas, que por sua vez sai do orçamento de dano do grupo. Se um dia você achar um número aqui que não bate com 28.3, o errado é o número — a tabela é a fonte.
