# Capítulo 23 — Dano, cura e morte

Este capítulo cuida do número mais importante da sua ficha: os **PV**. Como eles caem, como eles voltam, o que acontece quando eles chegam a zero e o que acontece quando alguém decide terminar o serviço.

---

## 23.1 Como o dano chega em você

**Uma instância de dano** é um ataque, uma Habilidade, um tique de **Dano Contínuo**, um **Dano de Quebra**. Cada instância é resolvida inteira, uma por vez, e **toda instância causa no mínimo 1 de dano** (capítulo 02).

A ordem de resolução está no capítulo 18 e é sempre esta:

1. Dados base da fonte.
2. Ajuste de Elemento: `+2 dados` por Fraqueza, `-2 dados` por Resistência (mínimo 1 dado).
3. Crítico, se houver: dobra **só os dados base**.
4. Soma o Bônus de Atributo e os bônus fixos de dano.
5. Subtrai a **RD** (capítulo 18) — **menos** se for Dano Contínuo, que ignora RD.
6. **Mínimo 1.**

**Quando você tem PV temporários ou Barreira, eles absorvem primeiro** (23.3).

Sobre **RD**, teto de RD e Esquiva: capítulo 18. Sobre **condições** que o dano traz de brinde: capítulo 21.

---

## 23.2 Cura

- **Cura acima do PV máximo é perdida.** A única exceção é a Bênção **Excesso de Vida** do Caminho da Abundância (capítulo 10), que converte o excedente em PV temporários, dentro do teto de 23.3.
- **Cura não remove condições** (capítulo 21). Ela devolve PV, e só.
- **Cura remove o estado Morrendo** e zera o contador (23.4). Qualquer quantidade: 1 PV de cura levanta alguém.
- **Não existe cura total neste livro.** Nenhuma Habilidade, Bênção, Ultimate ou item devolve "todos os PV" fora de um Descanso Longo. Com cura total, PV deixa de ser recurso e o orçamento inteiro do jogo cai.

**De onde a cura vem:**

| Fonte | Onde está |
|---|---|
| Habilidade de cura, Níveis 1 a 7 | Capítulo 16 |
| Ultimate de cura | Capítulo 17 |
| Bênçãos do Caminho da Abundância e da Preservação | Capítulos 10 e 15 |
| Poções | Capítulo 24 |
| **Descanso Curto e Descanso Longo** | 23.6, aqui |

> **Nenhum efeito do livro cura, concede PV ou causa dano em porcentagem do PV máximo.** Tudo é valor fixo, dados ou múltiplo de nível e de Eficiência. A **única** exceção declarada é o **Sangramento** (capítulo 21), que já tem teto próprio.
>
> *Por quê:* no nível 20, "metade da vida máxima" é 130 de cura numa Bênção — mais do que uma Habilidade de Nível 6, de graça e sem custar PH. Efeitos em porcentagem são inúteis no começo da campanha e quebrados no fim, e nunca na mesma proporção para dois personagens diferentes.

---

## 23.3 PV temporários e Barreira

> **Teto global de PV temporários = 3 × Eficiência**, vindos de **qualquer** fonte — Habilidade, Bênção, Ultimate, Cone de Luz, item, Barreira.
>
> **PV temporários não acumulam entre fontes: fica o maior valor.**

Este capítulo é o dono desse teto.

| Nível | 1-3 | 4-6 | 7-9 | 10-12 | 13-15 | 16-18 | 19-20 |
|---|---|---|---|---|---|---|---|
| **Teto de PV temporários** | 6 | 9 | 12 | 15 | 18 | 21 | 24 |

Como funcionam:

- Eles **absorvem dano antes dos seus PV**.
- Eles **não são curados**: cura vai para os PV, não para o temporário.
- Quando a duração acaba ou eles são consumidos, somem. **PV temporário não sobra.**
- **A RD se aplica primeiro, o PV temporário depois.** O dano é reduzido pela RD e o que resta bate no temporário.

**Barreira** é o PV temporário do Caminho da Preservação (capítulo 15). Ela tem nome próprio, segue este mesmo teto, não acumula com outras fontes de PV temporário e **não** é afetada por cura. A Barreira que você **concede a um aliado** conta no teto **dele**, não no seu.

> **Exemplo.** Lin Hai (nível 11, Eficiência +5) concede Barreira a Nadir, que já tinha 9 PV temporários de uma Habilidade. O teto dela é **15**. A Barreira de Lin Hai vale 15; os dois não somam, então Nadir fica com **15** — o maior dos dois, não 24.

---

## 23.4 Morrendo

> **A 0 PV você fica Morrendo:** inconsciente, **mantendo a casa na Fila de Ação**. No seu turno, em vez de agir, você faz um **Teste de Força de Vontade contra DT 10**.

> **Este Teste soma só `d20 + Bônus de Presença`. Sem Eficiência e sem Eficácia.** É a única rolagem do livro que não soma o seu bônus de nível, e este capítulo é o dono dessa exceção.

**O contador:**

| Resultado | Efeito |
|---|---|
| **Sucesso** (10 ou mais) | 1 sucesso |
| **Falha** (9 ou menos) | 1 falha |
| **3 sucessos** antes de 3 falhas | Você **estabiliza com 1 PV** e sai do estado |
| **3 falhas** antes de 3 sucessos | O personagem **morre** |
| **20 natural** | Você **se levanta na hora com 1 PV** |
| **1 natural** | Conta como **2 falhas** |

**Enquanto você está Morrendo:**

- **Receber dano é 1 falha automática.** Dano de uma Habilidade de Nível 5 ou maior, ou um crítico: **2 falhas**.
- **Qualquer cura remove o estado e zera o contador.** O contador zera também se você estabilizar: cada queda recomeça de 0 a 0.
- Você mantém a casa na Fila porque é **no seu turno** que a rolagem acontece. A mesa inteira conta com você junto.

*Por quê este Teste não soma o seu nível:* porque, somando, ele deixaria de ser um teste. Um personagem de nível 20 com Presença +5 e Eficiência somaria +13 contra DT 10 e só falharia no 1 natural — da metade da campanha em diante, **ninguém morreria**, e um jogo em que ninguém morre perde a única consequência que faz a mesa jogar com cuidado. Sem Eficiência, a conta fica honesta nos dois extremos: Presença -1 estabiliza em cerca de metade das rolagens, Presença +5 em 80%, e **nunca** em 100%.

> **Exemplo.** Vesper cai a 0 PV no Ciclo 2. Presença dela é +0.
> Turno dela, Ciclo 2: rola **12** → 1 sucesso.
> Ciclo 3: o Comum ao lado dela ataca e acerta → **1 falha automática**. No turno dela, rola **4** → 2 falhas. Está em **1 sucesso, 2 falhas**, e a mesa percebe que ela vai morrer no próximo Ciclo.
> Ciclo 3, ainda: Lin Hai usa a Habilidade de cura nela. Ela volta com PV, **o contador zera** e ela age normalmente no Ciclo 4.
>
> Repare no que aconteceu de verdade: a cura não foi a ação ótima do turno de Lin Hai em dano por Ciclo. Foi a ação ótima porque **o dado já tinha avisado**.

---

## 23.5 Executado

> **Executado:** um **ser racional** que gaste o **Ataque Básico** dele a **Distância Pessoal** de um personagem Morrendo o **mata automaticamente**. Sem rolagem.

Quatro limites, e eles são o que separam o Executado de um golpe de misericórdia gratuito:

1. **Só ser racional executa.** Bestas, monstros e máquinas sem consciência — que não pensam nem tomam decisões — **não** executam. Boa parte do bestiário é besta ou máquina.
2. **Custa o Ataque Básico** do executor, a Distância Pessoal. Ele está gastando o turno dele para matar quem já está no chão, em vez de atacar quem ainda está de pé.
3. **Um aliado pode impedir com a Reação Intervir** (capítulo 18). **Intervir cancela a Execução:** no lugar dela, o executor pode fazer o Ataque Básico dele **contra o interventor**, resolvido normalmente. A Execução não é dano — é morte automática sem rolagem — então não há o que "receber no lugar". O que Intervir faz é interromper o ato e obrigar o executor a lutar com alguém de pé.
4. **Xianzhouítas não podem ser Executados** (capítulo 05). Eles continuam caindo em Morrendo e continuam rolando o Teste — com Vantagem, pelo traço racial.

> **Para o Mestre.** O Executado é uma ferramenta de tensão, não de contabilidade. Um inimigo racional que executa é um inimigo que está mandando uma mensagem, e a mesa vai lembrar dele. Use quando a cena pedir; não use porque o Comum estava ali do lado. O capítulo 27 fala disso.

> **O que mudou da v0.1:** a regra do Executado estava escrita **dentro** do traço racial dos Xianzhouítas — ou seja, a regra mais letal do jogo morava num benefício que seis das sete Raças nunca leriam, e ela não dizia qual Teste nem qual DT usar. Agora ela é uma regra geral, com o Teste nomeado (**Força de Vontade**), a DT escrita (**10**) e a exceção Xianzhouíta no lugar certo: como exceção.

---

## 23.6 Descanso

| Tipo | Tempo | Quantas | Recupera |
|---|---|---|---|
| **Descanso Curto** | 1 hora | até **2 por dia** | **PV = (2 × nível) + Bônus de Vigor** · recarrega efeitos de "1 vez por descanso" · **reinvoca o Memoespírito** que caiu |
| **Descanso Longo** | 8 horas | **1 por dia** | **Todos os PV** · **remove todas as condições** · recarrega tudo · devolve o ponto de **Esforço** a quem tem o traço que o concede (Humano) · permite **recriar uma Habilidade** problemática |

Quanto o Descanso Curto devolve, na prática:

| Nível | 3 | 7 | 11 | 15 | 19 |
|---|---|---|---|---|---|
| **PV por Descanso Curto** (Vigor +2) | 8 | 16 | 24 | 32 | 40 |

Os dois Descansos Curtos de um dia devolvem, somados, cerca de **30% dos PV do grupo** — e é exatamente por isso que o terceiro combate de um dia é o combate perigoso, não o primeiro (capítulo 27).

**Duas coisas que o descanso não faz:**

> **A Energia de Ultimate não zera em nenhum dos dois.** Ela persiste entre combates e entre dias (capítulo 17). Você pode terminar uma sessão com 80 de Energia e começar a próxima com 80.
>
> **Descanso não mexe em PH.** Os Pontos de Habilidade voltam ao valor inicial **no começo de cada combate** (capítulo 16), e fora de combate eles simplesmente não existem. Não há como "descansar para ter mais PH".

**Recriar uma Habilidade.** Se uma Habilidade aprovada se revelou quebrada — para cima ou para baixo — em jogo, você pode reescrevê-la **sem custo** no próximo Descanso Longo, pelo mesmo processo do capítulo 16. Essa é a válvula de escape que mantém o sistema aberto sem travar a campanha, e ela é para ser usada.

> **O que mudou da v0.1:** três Bênçãos da v0.1 diziam "uma vez por descanso" sem que descanso existisse como regra. Agora existe, com tempo, limite diário e lista do que volta.

---

## Resumo do capítulo

| | |
|---|---|
| **Instância de dano** | ataque, Habilidade, tique de Dano Contínuo, Dano de Quebra. **Mínimo 1 de dano** |
| **Cura acima do máximo** | perdida (salvo Excesso de Vida) |
| **PV temporários** | teto `3 × Eficiência` de qualquer fonte, **não acumulam: fica o maior** |
| **Barreira** | PV temporário com nome próprio, não é curada, conta no teto de quem recebe |
| **Morrendo** | 0 PV, mantém a casa, **Força de Vontade DT 10 com `d20 + Presença` apenas** |
| **O contador** | 3 sucessos estabiliza com 1 PV · 3 falhas morre · 20 natural levanta · 1 natural vale 2 falhas |
| **Dano enquanto Morrendo** | 1 falha (2 se crítico ou Habilidade de Nível 5+) |
| **Executado** | ser racional, Ataque Básico, Distância Pessoal. **Intervir cancela.** Xianzhouíta é imune |
| **Descanso Curto** | 1 hora, 2 por dia, `(2 × nível) + Vigor` de PV |
| **Descanso Longo** | 8 horas, 1 por dia, tudo volta e todas as condições saem |
