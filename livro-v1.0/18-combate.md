# Capítulo 18 — Combate

Combate em Explorando Galáxias é um loop curto e reconhecível: você bate para gerar **Pontos de Habilidade**, gasta os Pontos de Habilidade na **Habilidade** que importa, acumula **Energia** e, quando ela fecha em 100, grita o nome da sua **Ultimate**. No meio disso, você arranca a **Tenacidade** do inimigo até ele Quebrar.

Este capítulo cuida de **o que você faz no seu turno** e de **como se resolve um ataque**. A **ordem** em que os turnos acontecem é o capítulo 19. A Tenacidade e os Elementos são o capítulo 20.

---

## 18.1 O seu turno

No seu turno você tem, por padrão:

| Ação | Quantas | O que é |
|---|---|---|
| **Ataque Básico** | 1 | Qualquer ação agressiva que não seja Habilidade nem Ultimate |
| **Ação Complementar** | 1 | Pegar ou guardar um objeto, recarregar, beber poção, interagir, falar sob pressão |
| **Ação de Movimento** | 1 | Mover-se **1 Distância** |
| **Ativar Ultimate** | 1 por Ciclo | **Não consome o turno** e não ocupa nenhuma das linhas acima (capítulo 17) |
| **Reação** | 1 | Esquiva, Intervir, ou uma Reação de Bênção ou Habilidade |

As três primeiras são do **seu turno**. A Ultimate pode sair a qualquer momento. A Reação pode sair no turno de outra pessoa.

> **Usar uma Habilidade ocupa o espaço do seu Ataque Básico**, a menos que o texto da Habilidade diga que ela é uma **Ação Complementar** ou uma **Reação**.
>
> Essa linha é curta e sustenta meio sistema: ela impede "Ataque Básico + Habilidade todo turno", que dobraria o dano por turno e detonaria o orçamento de PV de todo inimigo do livro. É o mesmo loop do jogo de origem — você escolhe entre bater e usar a Habilidade.

### Esforço Total

> **Esforço Total:** gaste o **Ataque Básico e a Ação Complementar** do turno para dobrar a Ação de Movimento: **2 Distâncias** (3, com bônus).

Não é uma quinta ação, é uma troca declarada: abro mão de bater e de interagir para correr. É também a única forma de sair do lugar quando você está com **Lentidão** (capítulo 21).

### Ação Extra

Algumas Bênçãos, Habilidades de Nível 5 ou maior e Ultimates concedem uma **Ação Extra**. Ela permite **uma** destas três:

- um **Ataque Básico**; **ou**
- uma **Habilidade de Nível 2 ou menor**, pagando o PH normalmente; **ou**
- uma **Ação de Movimento**.

> **Máximo de 1 Ação Extra por criatura por Ciclo**, somando todas as fontes. A segunda e as seguintes são **perdidas**.

A Ação Extra **não** concede Reação nem Ação Complementar, **não** recarrega a Reação já gasta e **não** permite uma segunda Ultimate no Ciclo.

*Por quê o teto:* turno extra é o efeito mais forte do jogo. Sem teto, dois personagens da Harmonia — ou um deles mais uma Habilidade de Nível 5 — entregam Ação Extra ao mesmo personagem todo Ciclo, e numa mesa de 4 isso é **+25% de turnos**. O **Avanço Total** (capítulo 19) tem o mesmo teto, pelo mesmo motivo.

### Reação

> **Toda criatura começa o combate com a Reação disponível.** Dali em diante, ela recarrega no **início do seu turno**.

Sem essa linha, quem tem VEL baixa — a Preservação, que é feita de Reações defensivas — passaria o primeiro Ciclo inteiro sem poder Esquivar nem Intervir, exatamente quando os inimigos rápidos atacam.

Você tem **1 Reação por turno** e não acumula Reações, a menos que uma Habilidade ou Bênção diga o contrário. **Não existem ataques de oportunidade** neste sistema: eles obrigariam a rastrear posição exata, e a escala de Distâncias é abstrata de propósito.

---

## 18.2 Teste de Ataque

> **Teste de Ataque = d20 + Bônus do Atributo de Ataque + Eficiência + Especialização de Combate + bônus permanentes de equipamento ± bônus e penalidades temporários ≥ Defesa do alvo**

Parcela por parcela:

| Parcela | De onde vem | Entra no teto de bônus? |
|---|---|---|
| **d20** | o dado | — |
| **Bônus do Atributo de Ataque** | pela categoria da arma, ou o seu **Atributo de Habilidade** (tabela abaixo) | não (permanente) |
| **Eficiência** | nível (capítulo 02). **Nunca Eficácia** | não (permanente) |
| **Especialização de Combate** | +1 no nível 5, +2 no 11, +3 no 17 (capítulo 26) | **não**, está fora do teto |
| **Bônus Maior de Cone de Luz e bônus de slot de Relíquia** | equipamento permanente (capítulo 25) | **não**, estão fora do teto |
| **Bônus e penalidades temporários** | Bênção, Habilidade, Ultimate, conjunto de Relíquia, marcas, condições | **sim**, teto de +3/+4/+5 e -3/-4/-5 por faixa (capítulo 26) |

**Qual atributo você soma:**

| O que você está usando | Atributo de Ataque |
|---|---|
| **Leve** (adaga, lâmina curta, chicote) | Agilidade |
| **Média** (espada de uma mão, lança curta, bastão) | **Poder ou Agilidade**, fixo na criação |
| **Pesada, 2 mãos** (martelo, montante, punhos reforçados) | Poder |
| **Disparo curto** (pistola, besta de mão) | Agilidade |
| **Disparo longo, 2 mãos** (arco, rifle) | Agilidade |
| **Energia, 2 mãos** (canhão, catalisador, drone de combate) | Sincronia |
| **Habilidade ou Ultimate** | o seu **Atributo de Habilidade** |
| Ataque do Memoespírito | o atributo escolhido na ficha dele (capítulo 11) |

São **exatamente seis** categorias de arma, e os exemplos entre parênteses são ilustração — a sua arma pode ser o que você quiser, desde que caiba em uma delas. A categoria **Média** é a única que deixa escolher entre dois atributos: é a espada de uma mão que tanto o lutador de Poder quanto o esgrimista de Agilidade empunham. A escolha é feita na criação e não muda.

### Quando não há Teste de Ataque

Habilidades de **área, de controle e de debuff** podem, em vez disso, exigir um **Teste de Resistência do alvo** contra a sua DT (`8 + Bônus do Atributo de Habilidade + Eficiência`). Cada Habilidade declara qual das duas vias usa no momento em que é criada, e **nenhuma usa as duas**.

O que acontece quando o alvo passa nesse Teste está no **capítulo 22**, com todas as consequências.

### Acerto, falha e os dois naturais

| Resultado | O que acontece |
|---|---|
| **Soma ≥ Defesa** | Acerto. Resolva o dano (18.5) e a Redução de Tenacidade (capítulo 20) |
| **Soma < Defesa** | **Erra.** Sem dano, **sem Redução de Tenacidade**. A **Energia da ação é ganha normalmente** (capítulo 17). Um Ataque Básico que erra **não gera PH**, e o PH gasto por uma Habilidade que erra **não volta** |
| **20 natural** | Acerto automático e **acerto crítico**, independente da Defesa |
| **1 natural** | Falha automática, independente dos bônus, e você **não ganha Energia por essa ação** |

Não existe tabela de trapalhadas. Perder o ataque e perder o ganho de Energia já atrasa a sua Ultimate em cerca de um turno, o que é um custo real e trivial de aplicar.

> **O custo é pago na declaração.** Você gasta o PH ao declarar a Habilidade, não ao acertar. Se o dado trair você, o PH já foi — e é isso que torna errar relevante.

---

## 18.3 Acerto crítico

| Pergunta | Resposta |
|---|---|
| **Faixa** | **20 natural.** O **teto absoluto do jogo é 19-20**, e a **única** fonte que chega lá é a Bênção de abertura do **Caminho da Caça** |
| **O que dobra** | **Só os dados base**: os dados da arma, ou os dados da tabela da Habilidade, ou os da Ultimate. Role esses dados duas vezes e some |
| **O que não dobra** | Dados ganhos por **Fraqueza**, dados e bônus de Bênção, buff ou item, **modificadores fixos** (inclusive o Bônus de Atributo) e **Dano Contínuo** |
| **Tenacidade** | O crítico reduz Tenacidade normalmente, sem bônus. A Quebra já é o "crítico" do sistema de Tenacidade |
| **Perícia e Teste de Resistência** | **Não existe crítico.** Um 20 natural é um sucesso memorável e um 1 natural é uma falha memorável — narrativamente, com zero efeito mecânico |

**Nenhum Cone de Luz, Relíquia, Bênção ou Habilidade expande a faixa de crítico**, e "expandir a faixa de crítico" está na lista de **efeitos proibidos** de Habilidade criada pelo jogador (capítulo 16). A Caça tem um privilégio que ninguém pode copiar; para todo o resto da mesa, crítico vale 5% das rolagens.

> **Exemplo.** Nadir, nível 19, acerta um 20 natural com a Habilidade de Nível 7 contra um Boss com Fraqueza a Fogo. Dados base: 18d20. Fraqueza: +2d20, que **não** dobram. Crítico: os 18d20 são rolados **duas vezes**. Com o Bônus de Atributo e a Relíquia por cima, o golpe sai perto de **404** contra um Boss de 935 PV — 43% da barra dele em uma ação, com 5% de chance de acontecer. É o lugar exato do crítico neste sistema: raro, memorável, assustador.

---

## 18.4 Defesa, Esquiva, Intervir e RD

### Defesa

> **Defesa = 10 + Bônus de Agilidade + Bônus de Armadura ou Vestimenta + outros bônus aplicáveis**

A Defesa é **passiva**: o inimigo rola contra ela, você não rola nada.

| Armadura ou Vestimenta | Defesa | Outros | Esquiva |
|---|---|---|---|
| Leve | +3 | +1 de Velocidade | Permitida |
| Média | +5 | — | Permitida |
| Pesada | +6 | **2 RD**, -2 em Reflexos e nas Perícias de Agilidade (não no Teste de Ataque), -2 de Velocidade | **Proibida** |

A tabela completa, com aparência, peso e preço, está no capítulo 24.

### Esquiva

> **Esquiva (Reação):** declare **antes da rolagem de ataque inimigo** e some a sua **Eficiência** à sua Defesa contra **aquele único ataque**.

- Custa a sua **Reação** do turno. Só em cena de combate.
- **A Esquiva soma sempre Eficiência, nunca Eficácia.** Não existe fonte neste livro que troque uma pela outra aqui: nem Eficácia em Acrobacia, nem Bênção, nem Habilidade, nem Cone de Luz. Este capítulo é o dono dessa regra.
- **Armadura Pesada não permite Esquiva.** É o preço dos +6 de Defesa.

*Por quê a Eficácia não toca a Esquiva:* ela é gratuita, universal e está disponível **todo turno**, sem gastar PH, Energia nem acúmulo. Com Eficácia, o bônus chegaria a **+16** no nível 20 e o inimigo de referência só acertaria no 20 natural. Isso não é uma Reação boa, é imunidade a um ataque por turno.

Com Eficiência, você sabe o número de antemão — **+2 no nível 1, +5 no 12, +8 no 20** — e pode decidir se vale gastar a Reação. Contra o ataque inimigo da faixa 17-20, a Esquiva leva o acerto dele de 60% para **20%**.

### Intervir

> **Intervir (Reação):** declare **antes da rolagem**, contra um ataque de **alvo único** dirigido a um aliado a até **Distância Curta**. O ataque passa a ter **você** como alvo e resolve contra a **sua** Defesa e a **sua** RD.

- Você **não pode Esquivar** o ataque que acabou de atrair: a Reação do turno foi gasta em Intervir.
- **Contra uma Execução (capítulo 23), Intervir cancela a Execução.** No lugar dela, o executor pode fazer o **Ataque Básico** dele contra você, resolvido normalmente. A Execução não é dano — é morte automática sem rolagem — então não há o que "receber no lugar": o que Intervir faz é interromper o ato e obrigar o executor a lutar com você.

### RD — Redução de Dano

> **RD subtrai um valor fixo de cada instância de dano.**

- Uma **instância** é um ataque, uma Habilidade, um tique de **Dano Contínuo** ou um **Dano de Quebra**.
- Em Habilidade de **área**, a RD se aplica **uma vez por alvo**.
- Múltiplas fontes de RD **somam**, até o teto.
- Toda instância causa **no mínimo 1 de dano**. **Não existe imunidade por RD.**
- **Dano Contínuo ignora RD** (capítulo 20).

> **Teto de RD = 2 + (2 × Eficiência).** Este capítulo é o dono dele.

| Nível | 1-3 | 4-6 | 7-9 | 10-12 | 13-15 | 16-18 | 19-20 |
|---|---|---|---|---|---|---|---|
| **Teto de RD** | 6 | 8 | 10 | 12 | 14 | 16 | 18 |

O teto amarra a RD à Eficiência, então ela cresce junto com o dano do jogo em vez de estourá-lo. Sem ele, um personagem de nível 2 com Armadura Pesada e duas Bênçãos de Abundância chegaria a 30 de RD contra ataques de 10 a 14 de dano — literalmente invulnerável.

**Inimigos usam a mesma regra e o mesmo teto**, lendo a Eficiência da faixa de nível deles. Os valores por tipo e faixa estão no capítulo 28.

> **Inimigos não têm Esquiva nem Intervir.** As duas são Reações **de personagem**. Um inimigo só tem Reação se a ficha dele declarar uma, entre as ações especiais, e ela **nunca é um bônus de Defesa**. A defesa do inimigo é **PV, Defesa e RD** — os três números que o orçamento do capítulo 27 controla.

---

## 18.5 Dano

### Os três tipos de dano

Eles são **categorias de escalonamento**: é por elas que Relíquias, Cones de Luz e Bênçãos dizem o que aumentam.

- **Dano de Ataque Básico** — toda ação agressiva que não seja Habilidade nem Ultimate.
- **Dano de Habilidade** — uma Habilidade que causa dano.
- **Dano de Ultimate** — a sua Ultimate, quando causa dano.

### Dados por categoria de arma

| Categoria | Dados base | Alcance | Atributo | Redução de Tenacidade |
|---|---|---|---|---|
| **Leve** | 1d8 | Pessoal | Agilidade | 1 |
| **Média** | 1d10 | Pessoal | Poder ou Agilidade | 1 |
| **Pesada** (2 mãos) | 1d12 | Pessoal | Poder | 1 |
| **Disparo curto** | 1d8 | Média | Agilidade | 1 |
| **Disparo longo** (2 mãos) | 1d10 | Longa | Agilidade | 1 |
| **Energia** (2 mãos) | 2d8 | Longa | Sincronia | 1 |

> **Dano = dados base + Bônus do Atributo de Ataque** (uma vez, **não** por dado).
>
> **Você ganha +1 dado base nos Ataques Básicos nos níveis 5, 9, 13 e 17.**

A coluna conta **quantos dados a sua arma rola**, partindo de 1 — ou de **2**, se for de Energia, e esse dado a mais sobrevive à progressão inteira:

| Nível | 1-4 | 5-8 | 9-12 | 13-16 | 17-20 |
|---|---|---|---|---|---|
| **Leve / Disparo curto** (d8) | 1d8 · média 4 | 2d8 · 9 | 3d8 · 13 | 4d8 · 18 | 5d8 · 22 |
| **Média / Disparo longo** (d10) | 1d10 · 5 | 2d10 · 11 | 3d10 · 16 | 4d10 · 22 | 5d10 · 27 |
| **Pesada** (d12) | 1d12 · 6 | 2d12 · 13 | 3d12 · 19 | 4d12 · 26 | 5d12 · 32 |
| **Energia** (d8, começa em 2) | 2d8 · 9 | 3d8 · 13 | 4d8 · 18 | 5d8 · 22 | 6d8 · 27 |

*Por quê o Ataque Básico escala:* ele é o motor dos **Pontos de Habilidade** (capítulo 16). Se não crescesse, no nível 15 ninguém ia querer gerar PH, e a economia que sustenta o balanceamento do jogo morreria. Com 5 dados no nível 17, um básico de arma Média faz uns 33 de dano somando o Bônus de Atributo — não compete com uma Habilidade de Nível 7, mas vale o turno.

### Ordem de resolução do dano

Sempre nesta ordem:

1. **Monte os dados base** da arma, da Habilidade ou da Ultimate.
2. **Ajuste por Elemento:** `+2 dados` se for Fraqueza do alvo, `-2 dados` se ele tiver Resistência (mínimo **1 dado**).
3. **Crítico**, se houver: role os **dados base** de novo e some (os dados de Fraqueza não dobram).
4. **Some o Bônus de Atributo** uma vez, mais bônus fixos de dano.
5. **Subtraia a RD** do alvo.
6. **Mínimo 1 de dano**, sempre.

> **Exemplo.** Vesper, nível 11, atira com rifle (Disparo longo, 3d10 no nível dela) em um Elite com **Fraqueza a Vento**, o Elemento dela. Dados: `3d10 + 2d10` de Fraqueza = 5d10 → rolou **29**. Bônus de Agilidade +5 e Relíquia Mãos +4 → 38. RD de Elite (3) → **35 de dano**. E, por ter acertado, ela arranca **1 de Tenacidade** — total, porque bateu na Fraqueza.

A cura, os PV temporários e o que acontece quando o seu PV chega a 0 estão no **capítulo 23**.

---

## 18.6 Distâncias

A escala é abstrata, de propósito: **não existe grade, não existe medida em metros**.

> **Pessoal → Curta → Média → Longa → Extrema**

- **Pessoal** é corpo a corpo.
- Uma **Ação de Movimento** sobe ou desce **um passo** na escala.
- Com **Esforço Total**, dois passos. O máximo por turno, com todos os bônus do livro, é **três**.
- O alcance de uma Habilidade é **cumulativo** pelo Nível dela (capítulo 16): uma Habilidade de Nível 4 alcança de Pessoal a Extrema.

"Os alvos estão juntos?" é uma pergunta que o Mestre responde olhando a cena. Habilidade em área exige que os alvos estejam a **até uma Distância um do outro** (capítulo 16), e em caso de dúvida o Mestre diz quantos dos alvos escolhidos estão agrupados o suficiente — esse número vale.

---

## 18.7 Armas: propriedades e criação

> **Onde está cada coisa sobre armas.** A ficha de uma arma está repartida em três
> lugares, de propósito, para cada capítulo falar do que é dele: **dados de dano,
> alcance, atributo usado e Redução de Tenacidade em 18.5**; **Elemento e propriedade
> especial aqui em 18.7**; e **preço, disponibilidade e a tabela de propriedades
> em 24.2**. Para montar uma arma do zero, leia os três.

A tabela de 18.5 é a tabela de armas do jogo. O que distingue a sua arma das outras da mesma categoria é a **aparência**, o **Elemento** e **uma** propriedade especial.

- **Elemento.** A arma pode ter um Elemento próprio. Se não tiver, o dano dela é **Físico** — inclusive para quem tem outro Elemento pessoal.
- **Uma propriedade especial, no máximo** — e nenhuma também é resposta. São quatro, com o texto fechado em **24.2**: **Arremessável**, **Alcance estendido**, **Peso de impacto** e **Dissimulada**.

**Armas criadas pelos jogadores** passam pela mesma validação das Habilidades (capítulo 16): escolha uma categoria da tabela, um Elemento e até uma propriedade. O Mestre **ajusta antes de rejeitar**, e a decisão vai para a Ficha de Decisões da Mesa. Arma aprovada entra na lista oficial da mesa — e o capítulo 24 reserva espaço para isso.

> **O que mudou da v0.1:** a v0.1 prometia que "Itens Comuns e Armas serão criadas com os jogadores" e nunca deu dado, alcance nem atributo de nenhuma arma. A promessa fica; o que entra é a tabela que faltava para cumpri-la.

---

## 18.8 A sequência de um combate

1. **O Mestre declara se há surpresa** e **monta a Fila de Ação** por Velocidade (capítulo 19).
2. **Primeiro Ciclo.** Cada combatente age na casa dele: Ataque Básico ou Habilidade, Ação Complementar, Ação de Movimento, e Ultimate a qualquer momento.
3. **Fim do Ciclo.** Quando o último combatente age, o Ciclo termina: a Fila é **remontada** com as VEL atuais, os **Atrasos pendentes** entram, as durações contadas em Ciclos avançam.
4. **Repita.** Um combate típico dura **3 a 5 Ciclos**.
5. **Fim.** Combate acabou quando um dos lados não pode mais lutar. O **PH volta ao valor inicial** no começo do próximo combate; a **Energia não zera** nunca (capítulo 17).

> **Exemplo de um turno inteiro.** Ciclo 2, a casa é de Nadir (nível 11, Fogo, marreta Pesada 3d12).
> O Boss está com 7 de Tenacidade e tem Fraqueza a Fogo. O grupo tem 4 PH.
> - Ela declara a **Habilidade de Nível 4** (*Rebarba*, 3 PH): rola o Teste de Ataque, acerta. `6d20 + 2d20` de Fraqueza, mais Poder +5 e Esfera Planar de Tier II +4. Arranca **4 de Tenacidade** — redução total, porque bateu na Fraqueza. O Boss cai para 3.
> - A Habilidade ocupou o Ataque Básico dela, então sobram a **Ação Complementar** (ela guarda a marreta e saca a pistola, para o caso de precisar de alcance) e a **Ação de Movimento** (recua para Distância Média).
> - A Energia dela fecha em 100 com a Habilidade. Ela **não** ulta agora: o Boss Quebra no Ciclo que vem, e Quebrado ele recebe +1 dado de dano de qualquer fonte. Ela espera.
>
> Essa última linha é o jogo. Não é a ação ótima de um turno: é a decisão que se toma olhando dois Ciclos à frente.

---

## Resumo do capítulo

| | |
|---|---|
| **Turno** | 1 Ataque Básico + 1 Ação Complementar + 1 Ação de Movimento, mais a Ultimate (que não gasta ação) e 1 Reação |
| **Habilidade** | ocupa o espaço do Ataque Básico |
| **Esforço Total** | troca Ataque Básico + Ação Complementar por 2 Distâncias de movimento |
| **Ação Extra** | no máximo **1 por criatura por Ciclo** |
| **Teste de Ataque** | d20 + Atributo de Ataque + Eficiência + Especialização + equipamento ± temporários ≥ Defesa |
| **Crítico** | 20 natural; dobra **só os dados base**; teto do jogo 19-20, exclusivo da Caça |
| **Defesa** | 10 + Agilidade + Armadura |
| **Esquiva** | Reação: Defesa + **Eficiência** (nunca Eficácia). Pesada não esquiva |
| **Intervir** | Reação: o ataque passa a ser contra você. Cancela Execução |
| **RD** | fixa, por instância, soma até `2 + (2 × Eficiência)`. Dano mínimo 1 |
| **Distâncias** | Pessoal, Curta, Média, Longa, Extrema. 1 passo por Ação de Movimento |
