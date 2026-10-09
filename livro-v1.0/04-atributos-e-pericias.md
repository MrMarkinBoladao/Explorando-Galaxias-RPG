# Capítulo 04 — Atributos e Perícias

Os **6 Atributos** são quem o seu personagem é. As **18 Perícias** são o que ele treinou. Em toda rolagem do jogo, um Atributo entra pelo **Bônus** dele, e é só isso que você precisa carregar na cabeça.

---

## 4.1 Os 6 Atributos

**Poder** — Força física, impacto, capacidade de levantar peso e ataques corpo a corpo.

**Agilidade** — Reflexos, velocidade, precisão, esquiva e coordenação.

**Vigor** — Resistência física, PV, fôlego e capacidade de suportar danos.

**Sincronia** — Conhecimento, domínio de tecnologia, ciência e manipulação da energia dos Caminhos.

**Discernimento** — Instinto, atenção, intuição e força mental contra ilusões e manipulações.

**Presença** — Liderança, influência, determinação e capacidade de convencer ou intimidar.

Cada um deles é dono de coisas concretas na ficha:

| Atributo | O que ele carrega |
|---|---|
| **Poder** | Ataque de arma Pesada e Média, Atletismo, Teste de Potência Física, capacidade de inventário |
| **Agilidade** | Ataque de arma Leve, de Disparo e Média, **Defesa**, **Velocidade**, 3 Perícias, Teste de Reflexos |
| **Vigor** | **PV**, Teste de Resistência Física, Perícia Resistência |
| **Sincronia** | Ataque de arma de Energia, **quantas Perícias você escolhe**, 4 Perícias, Teste de Resistência Mental |
| **Discernimento** | 4 Perícias, Teste de Percepção Mental, desempate na Fila de Ação |
| **Presença** | 4 Perícias, Teste de Força de Vontade, **o Teste de Morrendo** |

Nenhum Atributo é inútil para ninguém. **Vigor** e **Presença** são os dois que todo personagem sente falta se ignorar por completo: um é o seu PV, o outro é a sua chance de levantar quando o PV acaba.

---

## 4.2 Tabela de Bônus de Atributo

O número do Atributo não entra em rolagem nenhuma. O que entra é o **Bônus**:

| Valor | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Bônus** | -1 | -1 | +0 | +0 | +1 | +1 | +2 | **+3** | +3 | +4 | +4 | +5 | +5 |

Três coisas para notar, porque elas governam toda decisão de build do livro:

- **O 15 é o degrau premiado.** Ele é o topo do array e o topo da Compra de Pontos, e vale **+3** — um salto de dois degraus. É onde a especialização aparece.
- **Daí para cima, +1 a cada 2 pontos.** É exatamente por isso que os aumentos por nível vêm em **+2**: cada aumento entrega um degrau cheio, nunca meio degrau perdido.
- **O teto é 20, com Bônus +5**, e quem foca chega lá já no **nível 6**. Isso é de propósito: o Bônus de Atributo **satura cedo**. Quem cresce no resto da campanha é a Eficiência, a Habilidade, a Bênção e o equipamento.

O array oficial `15, 14, 13, 12, 10, 8` entrega **+3, +2, +1, +1, +0, -1** — soma **+6** espalhada em seis linhas da ficha.

> **O que mudou da v0.1:** lá, 13 e 14 davam os dois **+2**, o que fazia subir de 13 para 14 não valer absolutamente nada, e a tabela parava no 15, que as Raças já ultrapassam. Nesta tabela o **13 vale +1** e a escala vai até 20. Todos os marcos que o autor escreveu continuam de pé: 8 = -1, 10 = +0, 12 = +1, 14 = +2, **15 = +3**.

---

## 4.3 Aumentos de Atributo por nível

Nos níveis **3, 6, 9, 12, 15 e 18** você ganha:

> **+2 em um Atributo**, ou **+1 em dois Atributos diferentes** — respeitando o teto 20.

São seis aumentos, +12 no total, ao longo da campanha. Um personagem focado satura o atributo principal no nível 6 e depois **espalha**: ele vira um personagem completo, não um pico só.

Esses níveis foram escolhidos porque são os que não tinham outra entrega: os ímpares dão Bênção, o 5 dá Eficácia, os múltiplos de 3 dão Nível de Habilidade novo. Com os aumentos aqui, **nenhum dos 20 níveis sobe vazio** (a tabela mestra está no capítulo 26).

> ### Aumento de Vigor e PV
>
> Quando o seu **Bônus de Vigor** aumenta, você ganha, na hora, **PV igual ao seu nível atual + 2**. Não recalcule os níveis anteriores.
>
> *Por quê exatamente +2:* pela fórmula de PV do capítulo 06, o Bônus de Vigor entra **3 vezes** no nível 1 e **1 vez** em cada nível seguinte. Um ponto ganho no nível L vale, retroativamente, `3 + (L-1)` = **L+2** de PV. Como daí para frente o seu incremento por nível já usa o Vigor novo, o ganho na hora mais os incrementos seguintes somam exatamente o valor retroativo — **dois personagens idênticos que subiram Vigor em níveis diferentes chegam ao mesmo PV no mesmo nível.**
>
> **Exemplo.** Lin Hai sobe para o nível 9 e gasta o aumento em Vigor, levando o Bônus de +2 para +3. Ele ganha `9 + 2 = 11` PV na hora, e dali em diante o incremento por nível dele é 1 ponto maior.

Aumento de Vigor é a única coisa deste capítulo que mexe em outra estatística. Subir Agilidade **não** recalcula a Defesa retroativamente — a Defesa é lida da fórmula, então ela simplesmente passa a ser maior a partir daquele momento. O mesmo vale para a Velocidade.

---

## 4.4 As 18 Perícias

**Como funciona um Teste de Perícia:** `d20 + Bônus do Atributo da Perícia + Eficiência (ou Eficácia) ≥ DT`. Perícia em que você não tem Eficiência rola `d20 + Bônus de Atributo`.

### Perícias de Poder

| Perícia | O que resolve |
|---|---|
| **Atletismo** | Escalar, nadar, saltar, empurrar, quebrar objetos e feitos de força |

### Perícias de Agilidade

| Perícia | O que resolve |
|---|---|
| **Acrobacia** | Equilíbrio, rolamentos, parkour e escapar de agarrões |
| **Furtividade** | Passar despercebido |
| **Pilotagem** | Conduzir naves, mechas, motos voadoras ou outros veículos |

### Perícias de Vigor

| Perícia | O que resolve |
|---|---|
| **Resistência** | Suportar venenos, frio, calor, fadiga, fome e longas marchas |

### Perícias de Sincronia

| Perícia | O que resolve |
|---|---|
| **Tecnologia** | Invadir sistemas, consertar máquinas, usar computadores e dispositivos |
| **Pesquisa** | Encontrar informações, consultar arquivos e lembrar conhecimentos |
| **Ciência** | Física, química, medicina, astronomia e biologia, entre outras |
| **Mecânica** | Construir, modificar ou reparar armas, robôs e veículos |

### Perícias de Discernimento

| Perícia | O que resolve |
|---|---|
| **Percepção** | Notar armadilhas, inimigos escondidos e detalhes |
| **Sobrevivência** | Rastrear, encontrar recursos e orientar-se em ambientes hostis |
| **Intuição** | Perceber mentiras, intenções e emoções |
| **Investigação** | Reconstruir cenas, encontrar pistas e resolver mistérios |

### Perícias de Presença

| Perícia | O que resolve |
|---|---|
| **Persuasão** | Convencer e negociar |
| **Intimidação** | Ameaçar e impor respeito |
| **Enganação** | Mentir, blefar e criar disfarces |
| **Liderança** | Coordenar aliados, motivar equipes e comandar grupos |

### A Perícia de dois atributos

| Perícia | O que resolve |
|---|---|
| **Sintonia** (+Discernimento **ou** +Sincronia) | Usar ou compreender fenômenos ligados aos Caminhos, ao Stellaron, ao Fragmentum e a outras energias sobrenaturais |

> **Você escolhe o atributo da Sintonia na criação, e ele é fixo.** Não é "o maior dos dois na hora": se fosse, a Sintonia seria a melhor Perícia do livro por motivo nenhum. Escolha pelo conceito — o Discernimento sente a energia, a Sincronia a entende.

A Sintonia é a Perícia mais usada do jogo fora de combate, e **dentro** dele ela é uma das três que descobrem Fraqueza de inimigo (capítulo 20), ao lado de **Pesquisa** e **Ciência**.

---

## 4.5 Quantas Perícias você tem

> **Eficiência nas 3 Perícias do seu Caminho** (capítulo 06, de graça) **+ `2 + Bônus de Sincronia` Perícias escolhidas por você**, com **mínimo de 2 escolhidas**.
>
> **Humano: +1 Perícia escolhida**, pelo traço passivo **Vocação Livre** (capítulo 05). Entra na conta acima e é fixada na criação como todas as outras.

| Bônus de Sincronia | -1 | +0 | +1 | +2 | +3 | +4 | +5 |
|---|---|---|---|---|---|---|---|
| **Perícias escolhidas** | **2** | 2 | 3 | 4 | 5 | 6 | 7 |
| **Perícias escolhidas — Humano** | **3** | 3 | 4 | 5 | 6 | 7 | 8 |

O **mínimo de 2** é um conserto: a conta da v0.1, com Sincronia 8, entregava **uma** Perícia escolhida. Agora o piso é 2, e a Sincronia continua sendo o atributo que amplia a sua folha de competências.

**A quantidade de Perícias escolhidas é fixada na criação**, com o Bônus de Sincronia que você tem nesse momento (já com o bônus da Raça). Aumentar a Sincronia depois (4.3) **não dá Perícia nova**. O **+1 do Humano** entra nessa mesma conta e na mesma hora: ele é parte da criação, não um ganho posterior.

Perícia nova depois da criação só entra pela via dos **slots de Eficácia** (capítulo 02): eles dobram uma Perícia que você já tem, não adicionam Perícias novas. Se a sua mesa quiser treinar Perícias novas em jogo, isso é decisão de mesa — anote na Ficha de Decisões (capítulo 29).

---

## 4.6 Eficiência nos Testes de Resistência

> **Todo personagem tem Eficiência nos 6 Testes de Resistência desde o nível 1.** Não se escolhe, não se compra, não se perde.

| Teste de Resistência | Atributo |
|---|---|
| Potência Física | Poder |
| Reflexos | Agilidade |
| Resistência Física | Vigor |
| Resistência Mental | Sincronia |
| Percepção Mental | Discernimento |
| Força de Vontade | Presença |

Um Teste por Atributo: a ficha fica autoexplicativa e ninguém pergunta "qual eu uso?" no meio da cena. O capítulo 22 traz o que cada um resiste, quando o Mestre pede e o que acontece quando você passa.

A **única exceção** da fórmula é o **Teste de Força de Vontade de Morrendo** (capítulo 23), que soma só `d20 + Bônus de Presença`, **sem Eficiência e sem Eficácia**. É a única rolagem do livro que não soma o seu bônus de nível, e o capítulo 23 explica por quê.

---

## Resumo do capítulo

| | |
|---|---|
| **Atributos** | Poder, Agilidade, Vigor, Sincronia, Discernimento, Presença |
| **Bônus** | 8 = -1 · 10 = +0 · 12 = +1 · 14 = +2 · **15 = +3** · 17 = +4 · 19 = +5 · teto 20 |
| **Aumentos** | níveis 3, 6, 9, 12, 15 e 18: +2 em um ou +1 em dois, teto 20 |
| **Vigor novo** | ganha `nível atual + 2` de PV na hora |
| **Perícias** | 18 · Eficiência nas 3 do Caminho + `2 + Sincronia` escolhidas (mínimo 2) |
| **Sintonia** | +Discernimento ou +Sincronia, **fixo na criação** |
| **Testes de Resistência** | Eficiência nos 6 desde o nível 1 |
