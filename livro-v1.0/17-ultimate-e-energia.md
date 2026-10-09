# Capítulo 17 — Ultimate e Energia

A Ultimate é o momento do seu personagem. Ela é a única ação do jogo que **não gasta o seu turno**, sai **de graça** — sem Pontos de Habilidade — e você a anuncia **dizendo o nome dela em voz alta**. Essa última parte é regra, não piada: é como a mesa sabe que a sua vez de brilhar começou.

Este capítulo cuida da **Energia**, da **potência da Ultimate em cada faixa de nível** e de **como escrever a sua**. As Habilidades e a economia de PH são o capítulo 16.

Duas regras deste capítulo são invariantes do sistema: **1 Ultimate por Ciclo por personagem** e a **potência por faixa** de 17.3.

---

## 17.1 A regra básica

> **Toda Ultimate ativa com 100 de Energia.** Declare o **nome dela em voz alta**, a qualquer momento, **sem gastar ação**.

- **Uma Ultimate por Ciclo por personagem.** Declarável no **início ou no fim de qualquer turno** — seu ou de outra pessoa — e **nunca no meio da resolução de um efeito**. Se duas pessoas declaram ao mesmo tempo, resolve primeiro quem falou primeiro; se ninguém souber, resolve a maior Velocidade.
- A **Energia persiste entre combates.** Ela **não zera** em Descanso Curto nem em Descanso Longo (capítulo 23).
- **Energia acima de 100 é perdida.** Como a Ultimate não gasta ação, sempre dá para ultar antes de transbordar.
- Ativar consome **100 de Energia**. O medidor volta a zero e começa a encher de novo.
- A Ultimate **não custa nem gera PH** (capítulo 16).

> **O que mudou da v0.1:** o 100 de Energia, a declaração em voz alta e a perda do excedente são do autor e ficam inteiros. O que entra é o **teto de 1 por Ciclo**, a **tabela fechada de fontes de Energia** (17.2) e a **potência por faixa** (17.3) — a v0.1 dizia que a Ultimate "nos níveis iniciais será fraca" e nunca dava um número, então o Mestre não tinha como aprovar a criação de ninguém.

---

## 17.2 De onde vem a Energia

Tabela fechada. Nenhum capítulo acrescenta uma fonte nova sem passar por aqui.

| Fonte | Energia | Limite |
|---|---|---|
| **Ataque Básico** (acerte ou não) | **+20** | nenhum, salvo o **1 natural** |
| **Habilidade** (acerte ou não) | **+30** | nenhum, salvo o **1 natural** |
| **Sofrer dano** | **+10** | 1 vez por Ciclo |
| **Derrotar um inimigo** | **+10** | para quem desferiu o golpe |
| **Quebrar a Tenacidade de um inimigo** | **+10** | 1 vez por Ciclo |
| **Ativar a Ultimate** | **-100** | — |
| **Ação do Memoespírito** | **metade** do valor da ação, arredondando para baixo, para o dono | — |
| **Equipamento** | **Corda de Ligação:** +10 a +25 pelo tier, ao entrar na Fila · **Cone de Luz de Nível 3 ou maior:** +5 pelo Efeito Condicional | 1 vez por combate · 1 vez por Ciclo |

As duas linhas de **equipamento** são as únicas fontes que não vêm de uma ação sua, e estão fechadas no capítulo 25. Nenhum outro capítulo acrescenta fonte de Energia.

> **A Energia é da ação, não do acerto.** Este capítulo é o dono dessa regra. Você errou o ataque? Ganhou a Energia. A **única** falha que corta a Energia é o **1 natural** (capítulo 18).
>
> O que é condicionado ao acerto é o **PH** (capítulo 16), e a diferença não é retórica: a 60% de acerto, condicionar a Energia ao acerto custaria cerca de 8 de Energia por turno e trocaria uma Ultimate a cada 3,3 turnos por uma a cada 4,2. A Ultimate é a maior parcela isolada do dano do grupo — na faixa 17-20 ela é 106 dos 271 pontos por Ciclo.

*Por quê "sofrer dano" e "derrotar inimigo" entraram:* na v0.1 só quem ataca carrega a barra, e os Caminhos defensivos — Preservação e Abundância — ultariam a cada 5 ou 6 turnos enquanto a Destruição ulta a cada 3. "Sofrer dano" é a fonte canônica de Energia de quem segura a linha de frente, e conserta exatamente esse desequilíbrio. O limite de 1 por Ciclo evita que um inimigo de ataques múltiplos encha a barra do grupo inteiro de uma vez.

**O ritmo que isso produz:** entre **25 e 35 de Energia por turno**, ou seja **uma Ultimate a cada 3 ou 4 turnos** por personagem. É esse ritmo que o balanceamento do livro assume (capítulo 27). Se na sua mesa estiver saindo Ultimate todo Ciclo para todo mundo, alguém está somando duas vezes.

---

## 17.3 Potência: o Nível equivalente da sua faixa

> **A Ultimate não tem Nível próprio.** Ela tem um **Nível equivalente por faixa de nível**, e lê as tabelas do capítulo 16 nesse Nível.

| Faixa de nível | Nível equivalente | Dano | Média | Cura | Média | Redução de Tenacidade |
|---|---|---|---|---|---|---|
| **1-4** | **2** | 5d10 | **27** | 6d10 | **33** | 5 |
| **5-8** | **3** | 6d12 | **39** | 8d12 | **52** | 5 |
| **9-12** | **4** | 6d20 | **63** | 7d20 | **73** | 5 |
| **13-16** | **5** | 10d20 | **105** | 10d20 | **105** | 5 |
| **17-20** | **6** | 14d20 | **147** | 14d20 | **147** | 5 |

- **Dano ou cura = os dados da tabela + o Bônus do seu Atributo de Habilidade**, somado **uma vez**, não por dado. Igual às Habilidades.
- **Em área:** **metade dos dados** (arredonda para baixo, mínimo 1 dado) e **até 3 alvos** — **4 alvos** quando o Nível equivalente da sua faixa for **6**, ou seja do nível 17 em diante. É a mesma regra do capítulo 16, lida no Nível equivalente.
- Uma Ultimate que ataca exige **Teste de Ataque ou Teste de Resistência do alvo**, nunca os dois.
- **Efeitos de buff e debuff:** leia a linha do **Nível equivalente** na tabela de 16.5. No nível 20 isso significa teto de **+4/-4 e um efeito maior** — e **não** os +5/-5 e dois efeitos maiores de uma Habilidade de Nível 7. O **efeito de controle** sai da mesma linha: ele é o **"aplica 1 condição"** de 16.5, com a condição vindo do catálogo do capítulo 21.
- **Alcance:** o do Nível equivalente, cumulativo (capítulo 16). Na faixa 9-12 em diante, isso é Extrema.

> **Ao mudar de faixa, a sua Ultimate sobe sozinha.** Você não reescreve nada: os dados e o teto de efeito passam a ser os da faixa nova, na virada do nível 5, 9, 13 e 17. Se você quiser mudar a descrição ou o efeito, faz isso no próximo **Descanso Longo**, com a aprovação do Mestre.

*Por quê um Nível abaixo do topo:* nas faixas altas a Ultimate fica **um Nível equivalente abaixo** da melhor Habilidade disponível — 147 contra 189 na faixa 17-20 — porque ela é a única ação grande que sai **de graça**, sem PH e sem ocupar o turno. Se empatasse com a Habilidade de topo, o jogador racional pararia de gastar PH e a economia que sustenta o balanceamento viraria decoração. Nas faixas baixas elas **empatam de propósito**: no nível 3, a Ultimate **é** o grande momento do personagem, e é isso que a v0.1 promete ao mandar declarar o nome em voz alta.

*Por quê a Redução de Tenacidade é 5 em todas as faixas:* é o único número da Ultimate que não escala, e é deliberado. No nível 3, 5 de Redução contra um Comum de Tenacidade 4 é **Quebra garantida** — a Ultimate é a ferramenta de Quebra do grupo desde o começo da campanha. Nas faixas altas, 5 é a mesma contribuição de uma Habilidade de Nível 5, e a Quebra continua acontecendo a cada dois Ciclos.

---

## 17.4 Como escrever a sua Ultimate

Mesmo processo das Habilidades, com uma diferença: onde o checklist pede "Nível da Habilidade", você escreve o **Nível equivalente da sua faixa**.

1. **Comece pela imagem.** A Ultimate é a cena que a mesa vai lembrar. Escreva a frase que você vai dizer em voz alta.
2. **Escolha o Tipo:** **Dano, Cura, Buff ou Debuff** — os Tipos de 16.1, menos **Passiva**, que não cabe numa ação declarada. Pode combinar, dentro do que o Nível equivalente permite. **"Controle" não é um Tipo:** o efeito de controle é o **"aplica 1 condição"** das linhas de 16.5, escrito dentro de um Dano ou de um Debuff.
3. **Copie os dados** da linha da sua faixa (17.3). Se for em área, aplique a divisão e o limite de alvos.
4. **Escolha a resolução:** Teste de Ataque **ou** Teste de Resistência do alvo contra a sua DT (`8 + Bônus do Atributo de Habilidade + Eficiência`).
5. **Passe pelo checklist de validação de 16.8**, inclusive pela **lista de efeitos proibidos** — ela vale igual aqui. Uma Ultimate também não dá imunidade a dano, não expande a faixa de crítico e não atinge mais alvos em área do que o capítulo 16 permite.
6. **Escreva na ficha** o nome, a frase, os dados e a resolução. A potência você não anota: ela é a linha da sua faixa.

> **Exemplo — *A Estrela Não Pede Licença*, do Vesper, nível 11.**
>
> Faixa 9-12, **Nível equivalente 4**. Vento, Caminho da Caça.
>
> | Campo | Decisão |
> |---|---|
> | Tipo | Dano, alvo único |
> | Dados | **6d20** (média 63) + Bônus de Agilidade |
> | Resolução | Teste de Ataque |
> | Alcance | Extrema |
> | Redução de Tenacidade | 5 |
> | Efeito extra | A linha do Nível 4 em 16.5 permite **aplicar 1 condição**: ele aplica **Marcado** |
>
> No nível 13 nada disso é reescrito: os 6d20 viram **10d20** e o efeito extra passa a poder ser um **efeito maior**, porque a faixa 13-16 lê o Nível equivalente 5. A frase em voz alta continua a mesma.

---

## 17.5 A Ultimate no meio do combate

A Ultimate não gasta ação, então a decisão não é **se** você ulta: é **quando**. Três situações que aparecem em toda mesa:

- **Antes ou depois do turno de um aliado.** Você pode ultar no fim do turno de quem acabou de Atrasar o Boss, ou no início do turno de quem vai curar. A Ultimate entra **entre** turnos, nunca no meio da resolução de um efeito.
- **Esperando a Quebra.** Um inimigo **Quebrado** recebe **+1 dado** de dano de qualquer fonte e tem **-2 de Defesa** (capítulo 20). Guardar a Ultimate um Ciclo para ela cair em cima da Quebra é jogo bem jogado.
- **Transbordando.** Se você está com 100 e vai ganhar mais Energia nesse turno, o excedente é perdido. Ultar primeiro, agir depois.

A Ultimate também não escapa de nada: ela sofre **RD**, respeita os **tetos de bônus e penalidade** (capítulo 26), respeita o **teto de PV temporários** (capítulo 23) e, se resolvida por Teste de Resistência, obedece à regra do alvo que passa (capítulo 22).

**Ressonâncias.** Duas das quatro Ressonâncias mexem na sua Ultimate: a **II** (nível 10) dá a ela um efeito extra, lido no Nível equivalente da sua faixa, e a **IV** (nível 20) pode fazê-la **ativar com 80 de Energia e consumir 80** — o teto do medidor continua 100. Os detalhes estão no capítulo 26.

---

## Resumo do capítulo

| | |
|---|---|
| **Custo** | 100 de Energia. **Não gasta ação**, não custa PH |
| **Frequência** | **1 por Ciclo por personagem** |
| **Declaração** | O nome, em voz alta, no início ou no fim de um turno |
| **Energia por ação** | Ataque Básico +20 · Habilidade +30 · sofrer dano +10 (1×/Ciclo) · derrotar inimigo +10 · Quebrar +10 (1×/Ciclo) |
| **A Energia é da ação** | Errar não corta a Energia. Só o **1 natural** corta |
| **Excedente** | Energia acima de 100 é perdida. A Energia **não zera** em descanso |
| **Potência** | Nível equivalente **2 / 3 / 4 / 5 / 6** nas faixas 1-4, 5-8, 9-12, 13-16, 17-20 |
| **Dano médio** | 27 / 39 / 63 / 105 / 147 |
| **Redução de Tenacidade** | **5**, em todas as faixas |
| **Validação** | O mesmo checklist e a mesma lista de proibidos do capítulo 16 |
