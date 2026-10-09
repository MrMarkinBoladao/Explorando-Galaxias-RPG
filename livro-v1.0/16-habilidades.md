# Capítulo 16 — Habilidades

Aqui está a melhor ideia do sistema, e ela é da v0.1: **você escreve as suas próprias Habilidades.** Não existe lista fechada de poderes para escolher. Existe uma régua — as tabelas deste capítulo — e um checklist. Dentro dela, o que você imagina entra na ficha.

Este capítulo cuida de **como uma Habilidade é feita, quanto ela custa e o que ela pode fazer**. A sua Ultimate segue um caminho parecido e tem capítulo próprio (17). A ordem em que as ações acontecem é o capítulo 19.

Duas regras deste capítulo são invariantes do sistema e ninguém mais pode mexer nelas: **a economia de Pontos de Habilidade** (16.2) e **o número de alvos de uma Habilidade em área** (16.4).

---

## 16.1 O que é uma Habilidade

Uma Habilidade é uma ação com nome próprio, escrita por você, que faz uma coisa que o seu Ataque Básico não faz.

| Campo | O que você decide |
|---|---|
| **Nome** | O que você grita quando usa |
| **Nível** | De **1 a 7**, até o seu Nível máximo (16.6) |
| **Tipo** | Dano, Cura, Buff, Debuff ou Passiva |
| **Resolução** | **Teste de Ataque** ou **Teste de Resistência do alvo** — nunca os dois |
| **Alvos** | Alvo único ou área (16.4) |
| **Efeito** | Os dados da tabela do Nível, mais o que o Nível permite de extra |
| **Descrição** | Como isso se parece na mesa. Não é enfeite: é o que o Mestre usa para arbitrar |

Três linhas valem para todas elas:

> **Usar uma Habilidade ocupa o espaço do seu Ataque Básico no turno**, a menos que o texto dela diga que é uma **Ação Complementar** ou uma **Reação** (capítulo 18).
>
> **Toda Habilidade custa Pontos de Habilidade**, pelo Nível dela (16.2). **Habilidades Passivas não custam** — elas estão sempre ligadas.
>
> **O dano de uma Habilidade é do seu Elemento** (capítulo 03), salvo Bênção que permita outro.

---

## 16.2 Pontos de Habilidade — a reserva do grupo

Os **Pontos de Habilidade (PH)** são a espinha do balanceamento do jogo e a mecânica mais reconhecível dele depois da Ultimate. Eles **não são seus**: são do grupo.

> **Máximo de PH = 1 + número de personagens jogadores.** Mais **+1** nos níveis **9 a 16** e **+2** nos níveis **17 a 20**.
> **O grupo começa cada combate com o máximo menos 2.**

| Nº de jogadores | Máximo (1-8 / 9-16 / 17-20) | Início de combate (1-8 / 9-16 / 17-20) |
|---|---|---|
| 3 | 4 / 5 / 6 | 2 / 3 / 4 |
| **4** | **5 / 6 / 7** | **3 / 4 / 5** |
| 5 | 6 / 7 / 8 | 4 / 5 / 6 |
| 6 | 7 / 8 / 9 | 5 / 6 / 7 |

### Como se ganha PH

> **Cada Ataque Básico que acerta gera +1 PH** nos níveis **1 a 8** e **+2 PH** nos níveis **9 a 20**.
> **Ataque Básico que erra não gera PH.** O PH é do acerto; a **Energia** é da ação (capítulo 17). A diferença é de propósito.

### Como se gasta PH

| Nível da Habilidade | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| **Custo** | 1 PH | 1 PH | 2 PH | 3 PH | 4 PH | 5 PH | 6 PH |

- **Sem PH suficiente, a Habilidade não pode ser declarada.** Nada é rolado e você escolhe outra ação.
- **Não existe PH negativo, PH devido nem PH emprestado.**
- **O custo é pago na declaração.** Se o ataque errar depois de declarado, o PH já foi.
- A **Ultimate não custa nem gera PH** (capítulo 17).
- **Invocar o Memoespírito custa 1 PH** (capítulo 11). As Habilidades dele não custam PH: o preço foi pago na invocação.
- **O PH volta ao valor inicial no começo de cada combate.** Fora de combate ele não existe, e **nenhum descanso devolve PH** (capítulo 23).

### Quanto isso sustenta de verdade

Mesa de 4, combate de 4 Ciclos, dois Ataques Básicos por Ciclo no grupo, 60% de acerto:

| Faixa de nível | Geração por Ciclo | Orçamento do combate | O que ele compra em 4 Ciclos | Na prática, por Ciclo |
|---|---|---|---|---|
| 1-4 | 1,2 | 3 + 4,8 = **7,8 PH** | 4 Habilidades de Nível 2 (4 PH), com folga | **1 × Nível 2** |
| 5-8 | 1,2 | 3 + 4,8 = **7,8 PH** | 3 de Nível 3 + 1 de Nível 2 (7 PH) | **0,75 × Nível 3** |
| 9-12 | 2,4 | 4 + 9,6 = **13,6 PH** | 4 de Nível 4 (12 PH) | **1 × Nível 4** |
| 13-16 | 2,4 | 4 + 9,6 = **13,6 PH** | 2 de Nível 6 + 1 de Nível 3 (12 PH) | **0,5 × Nível 6** |
| 17-20 | 2,4 | 5 + 9,6 = **14,6 PH** | 2 de Nível 7 + 1 de Nível 3 (14 PH) | **0,5 × Nível 7** |

Leia essa tabela em voz alta na primeira sessão, porque ela diz uma coisa que a ficha não diz:

> **A sua Habilidade de topo não é a ação de todo turno.** Nas faixas altas ela sai uma vez a cada dois Ciclos, e é o Ataque Básico de alguém que paga por ela.

É daí que vem a conversa de mesa que o jogo de origem tem: *"não gasta tudo, deixa 1 para a cura."*

*Por quê os degraus caem no nível 9 e no 17:* porque as cinco faixas de balanceamento do livro quebram em 9, 13 e 17 (capítulo 27). Com os degraus em 10 e 16, o grupo de nível 9 — primeiro nível da faixa 9-12 — teria 7,8 PH por combate contra os 13,6 que a faixa dele pressupõe, e a cadência de Quebra e o dano por Ciclo da faixa valeriam só na metade dela.

*Por quê os PH existem:* sem eles a conta não fecha. Quatro jogadores de nível 20 usando a melhor Habilidade todo turno entregariam cerca de **525** de dano efetivo por Ciclo, contra os **275** que o jogo orça — e aí todo Boss morreria no Ciclo 2 ou precisaria de mais de 2.000 PV, o que o obrigaria a bater proporcionalmente mais forte e aniquilar o grupo. Os PH resolvem isso **sem nerfar nenhuma tabela**: você pode usar o Nível 7, mas gastou 6 dos 7 PH do grupo, e alguém vai ter que bater para repor.

---

## 16.3 Os sete Níveis de Habilidade

Esta é a tabela central do capítulo. Os dados não são sugestão: uma Habilidade de Nível 3 que causa dano causa **6d12**, ponto.

| Nível | Dano | Média | Cura | Média | Custo | Redução de Tenacidade | Alcance (cumulativo) |
|---|---|---|---|---|---|---|---|
| **1** | 6d6 | **21** | 5d8 | **22** | 1 PH | 2 | Pessoal, Curta |
| **2** | 5d10 | **27** | 6d10 | **33** | 1 PH | 2 | + Média |
| **3** | 6d12 | **39** | 8d12 | **52** | 2 PH | 3 | + Longa |
| **4** | 6d20 | **63** | 7d20 | **73** | 3 PH | 4 | + Extrema |
| **5** | 10d20 | **105** | 10d20 | **105** | 4 PH | 5 | Extrema |
| **6** | 14d20 | **147** | 14d20 | **147** | 5 PH | 6 | Extrema |
| **7** | 18d20 | **189** | 18d20 | **189** | 6 PH | 7 | Extrema |

> **Dano ou cura = os dados da tabela + o Bônus do seu Atributo de Habilidade**, somado **uma vez**, não por dado.

- **Alcance é cumulativo.** Uma Habilidade de Nível 4 pode ser escrita em qualquer alcance de Pessoal a Extrema. Nível 1 alcança Pessoal e Curta.
- **A Redução de Tenacidade vale só se o ataque acertar** (capítulo 20).
- **Cura não ressuscita** e cura acima do PV máximo é perdida (capítulo 23).

### Como as médias são calculadas

A média de um dado de N faces é `(N+1)/2`, e **toda média impressa neste livro é arredondada para baixo** (capítulo 02).

| Conta | Exato | Impresso |
|---|---|---|
| 6d6 = 6 × 3,5 | 21 | **21** |
| 5d10 = 5 × 5,5 | 27,5 | **27** |
| 6d12 = 6 × 6,5 | 39 | **39** |
| 6d20 = 6 × 10,5 | 63 | **63** |
| 5d8 = 5 × 4,5 | 22,5 | **22** |
| 8d12 = 8 × 6,5 | 52 | **52** |
| 7d20 = 7 × 10,5 | 73,5 | **73** |
| 18d20 = 18 × 10,5 | 189 | **189** |

> **O que mudou da v0.1:** a v0.1 imprimia 18, 25, 36, 60 e 100 para as cinco linhas de dano, e 20, 30, 48 e 70 para as de cura. As contas tinham sido feitas com o valor médio do dado truncado, e subestimavam o dano em até 17% — o que contaminaria o orçamento de PV de todo inimigo do livro. Os dados do autor ficaram **intactos**; só as médias foram recalculadas. As linhas de **Nível 6 e 7** são adição, não revisão.

> **Cura de Nível 5.** A v0.1 dizia "cura toda a Vida". Na v1.0 ela é **10d20** (média 105) **ou 5d20 em todos os aliados** (média 52). Cura total não cabe em nenhum orçamento: com ela, PV deixa de ser um recurso e passa a ser um incômodo.

> **Mesa rápida (variante oficial).** Em vez de rolar 18d20, use a média impressa. Recomendado para Habilidades de Nível 5 ou maior — rolar dezoito dados de vinte faces é bonito uma vez e cansativo na terceira.

---

## 16.4 Habilidade em área

Este capítulo é o **dono** desta regra. O combate, o equipamento e o bestiário só a consomem.

> **Área:** **metade dos dados** (arredonda para baixo, **mínimo 1 dado**) e **até 3 alvos** à sua escolha, todos dentro do alcance da Habilidade e a **até uma Distância um do outro**.
> Habilidades de **Nível 6 e 7** atingem **até 4 alvos**.
> Mais alvos do que isso só com recurso de Caminho (os **Acúmulos de Cálculo** da Erudição, capítulo 12) ou texto específico de Bênção, e **nunca mais de 6**.
> O custo em PH é **o mesmo** da versão de alvo único.

Como se resolve, alvo por alvo:

- O **Bônus do Atributo de Habilidade soma uma vez por alvo**, como em qualquer rolagem de dano.
- A **RD se aplica uma vez por alvo** (capítulo 18).
- Os **dados de Fraqueza são calculados por alvo**: o alvo fraco ao seu Elemento recebe +2 dados, o vizinho neutro não (capítulo 20).
- **Cura em área** conta alvos do mesmo jeito. A "cura em todos os aliados" do Nível 5 é a exceção declarada, porque uma mesa tem no máximo 6 personagens.
- O alcance é o do Nível. **A área não estende o alcance** — ela espalha o efeito dentro dele.

*Por quê 3 alvos, 4 nos Níveis 6 e 7, e um teto absoluto de 6:* sem número de alvos, "metade dos dados" é o contrário de um limite. Uma Habilidade de Nível 7 em área rola 9d20 ≈ 94, e com atributo e Esfera Planar isso é **107 por alvo** na faixa 17-20. Contra os 7 Comuns de um encontro daquela faixa seriam **749 de dano numa ação só** — 2,8 vezes o dano que o grupo inteiro entrega por Ciclo, e o encontro acabaria antes do segundo turno de alguém. Com 4 alvos ela entrega 428; com 3, 321. Contra os 219 que a mesma Habilidade faz concentrada num Elite, a versão em área vale cerca de **1,5 ×** o alvo único: forte, decisiva contra um pelotão, e **não** um apagador de encontros.

*Por quê "a até uma Distância um do outro" e não um raio em metros:* a escala de Distâncias é de **alcance**, não de geometria — não existe grade neste jogo (capítulo 18). "Os alvos estão juntos?" é uma pergunta que o Mestre responde olhando a cena. Em caso de dúvida, ele diz quantos dos alvos escolhidos estão agrupados o suficiente, e esse número vale.

> **Exemplo.** Nível 3, área: 6d12 viram **3d12** (média 19) em até 3 alvos. Você rolou 22. O primeiro alvo é fraco ao seu Elemento: ele leva `3d12 + 2d12` rolados só para ele, mais o seu Bônus de Atributo, menos a RD dele. Os outros dois levam os 22 mais o Bônus, menos a RD de cada um. Três subtrações, uma rolagem de dados por alvo. É mais rápido do que parece escrito.

---

## 16.5 Buff, Debuff e Passivas

A v0.1 dizia, nestas duas tabelas, "o jogador fará juntamente do mestre". Isso não é tabela-guia, é promessa. Aqui estão elas.

> **As duas tabelas são cumulativas, como o alcance de 16.3.** O que um Nível permite escrever, **todo Nível acima também permite**: a linha do seu Nível é o **teto**, não uma lista fechada. Uma Habilidade de Nível 5 pode aplicar 1 condição (que é a linha do Nível 3) ou dar PV temporários de `3 × Eficiência` (linha do Nível 4) **e** ainda ler o `+3/-3` com efeito maior da linha dela. Nenhum Nível é pior que o de baixo.

### Buff e Debuff

| Nível | O que você pode escrever | Duração | Alvos |
|---|---|---|---|
| 1 | +1 ou -1 em **um** tipo de rolagem, **ou** PV temporários = **1 × Eficiência** | 1 turno | 1 |
| 2 | +1/-1 e um efeito menor, **ou** +2/-2 em um tipo | 2 turnos | 1 |
| 3 | +2/-2, **ou** +1/-1 em dois tipos; PV temporários = **2 × Eficiência**; aplica 1 condição da lista do capítulo 21 | 2 turnos | 2 |
| 4 | +3/-3; aplica **ou** remove 1 condição; PV temporários = **3 × Eficiência**; **Implante de Fraqueza** | 2 turnos | 3 ou área |
| 5 | +3/-3 e um **efeito maior** (Avanço Total, Ação Extra, imunidade a 1 condição) | 3 turnos | **Buff:** todos os aliados (até 6) · **Debuff:** 3 alvos |
| 6 | +4/-4 e um efeito maior | 3 turnos | **Buff:** todos os aliados (até 6) · **Debuff:** 4 alvos |
| 7 | +5/-5 e **dois** efeitos maiores | 3 turnos | **Buff:** todos os aliados (até 6) · **Debuff:** 4 alvos |

> **"Grupo" não é contagem de alvos, e é por isso que a palavra não está na coluna.** Buff em "todos os aliados" tem teto natural: uma mesa tem no máximo **6** personagens, e o buff não cresce com o tamanho do encontro. Debuff, não — lido como "o grupo inimigo", um debuff de Nível 7 aplicaria **-5**, o teto inteiro de penalidade da faixa alta, a **todos** os inimigos da cena, que num encontro de 7 Comuns são sete alvos. Então cada lado da linha lê a regra do lugar certo: aliado, o tamanho da mesa; inimigo, a escala de área de 16.4.

### Passivas

| Nível | O que você pode escrever |
|---|---|
| 1 | +1 fixo pequeno, ou um gatilho de **+1 dado** do seu Elemento 1 vez por turno |
| 2 | +1 fixo e uma condição de gatilho (ex.: "quando você Quebra um inimigo") |
| 3 | +2 fixo, **ou** 1 RD, **ou** +1 de Velocidade |
| 4 | +2 e um gatilho que concede dado extra; **ou** 2 RD |
| 5 | Um gatilho forte 1 vez por combate (ex.: "ao cair a 0 PV, fique com 1 PV") |
| 6 | +3 fixo e um gatilho forte |
| 7 | Um gatilho que **altera uma regra sua**, 1 vez por Ciclo (ex.: "seus Ataques Básicos reduzem 2 de Tenacidade em vez de 1") |

- Passivas **não custam PH** e **contam no seu teto de 8 Habilidades** (16.6).
- Uma Passiva de Nível 7 **nunca** altera uma regra da lista de proibidos de 16.8, e **nunca** dá mais alvos em área do que 16.4 permite.

Buffs e debuffs respeitam o **teto de bônus somado** e o **teto de penalidade somada** (capítulo 26), e os PV temporários respeitam o **teto de 3 × Eficiência de qualquer fonte** (capítulo 23). Nenhuma Habilidade concede Vantagem permanente, mais de um Avanço Total por Ciclo, nem imunidade a dano.

*Por quê PV temporários em múltiplos de Eficiência:* valor fixo obriga a escolher entre ser inútil no fim da campanha (10 PV contra 260 de PV máximo) ou quebrado no começo (40 PV contra 46). Em múltiplos de Eficiência, a mesma linha de texto vale 2 a 8 PV no começo e 8 a 24 no fim.

---

## 16.6 Quantas Habilidades você tem

| Nível do personagem | 1 | **2** | 3 | 5 | 6 | 7 | 9 | 11 | 12 | 13 | 15 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Habilidades conhecidas** | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 6 | 6 | 7 | 8 | 8 |
| **Nível máximo de Habilidade** | 1 | **2** | 2 | 2 | 3 | 3 | 4 | 4 | 5 | 5 | 6 | 7 |

A tabela completa, nível por nível de 1 a 20, está no **capítulo 26**, que é o dono desta régua. A versão acima lista só os níveis em que algo muda.

- **O teto é 8 Habilidades conhecidas**, alcançado no nível 15.
- **O Nível máximo sobe para 2 já no nível 2.** Isso é DNA: a v0.1 diz, com essas palavras, que no Nível 2 você pode ter Habilidades de Nível 2.
- **A partir do nível 16**, em vez de aprender Habilidades novas, você **reescreve uma Habilidade conhecida por nível** — mesmo processo de criação, podendo agora subir o Nível dela até o seu máximo.
- **Habilidades Passivas contam no teto de 8.**

> **O que mudou da v0.1:** lá, "o número de habilidades que você pode ter por nível é igual ao seu nível". Num jogo de 20 níveis isso dá **20 Habilidades** escritas por jogador — uma ficha que ninguém lê e um combate em que ninguém decide. O teto de **8** é o número de blocos de texto que dá para manejar sem consultar a ficha a cada turno, e com a economia de PH você usa 2 ou 3 por combate de qualquer jeito. A regra de reescrita a partir do 16 mantém a progressão viva: no fim da campanha você não tem **mais** Habilidades, você tem Habilidades **melhores**.

---

## 16.7 Como escrever uma Habilidade

Sete passos. Faça na mesa, com o Mestre do lado.

1. **Diga o que ela faz na ficção.** "Eu bato o chão com a marreta e a onda de calor sai rachando o piso." Comece por aqui, não pelo dado.
2. **Escolha o Nível.** Até o seu Nível máximo (16.6). Olhe o custo em PH antes de decidir: Nível 4 custa 3 PH, e isso é mais da metade da reserva do grupo na faixa baixa.
3. **Escolha o Tipo:** Dano, Cura, Buff, Debuff ou Passiva. Uma Habilidade pode ter um efeito secundário do outro tipo, dentro do que o Nível permite (16.5).
4. **Copie os dados da linha do Nível** (16.3). Não arredonde, não troque d12 por d10 "porque fica melhor". Se for em área, aplique 16.4 agora.
5. **Escolha a resolução:** **Teste de Ataque** contra a Defesa do alvo, **ou Teste de Resistência do alvo** contra a sua DT (`8 + Bônus do Atributo de Habilidade + Eficiência`). Uma das duas. O que acontece quando o alvo passa está no capítulo 22.
6. **Escolha o alcance**, dentro do alcance cumulativo do Nível.
7. **Passe pelo checklist** de 16.8 e escreva na ficha.

> **Condição de recarga (opcional) — a troca que o checklist de 16.8 oferece.** Na criação, você pode escrever que a Habilidade só pode ser usada **uma vez por combate** e, em troca, ela custa **1 PH menos** — nunca menos de **1 PH**. É só isso que "trocar custo por frequência" significa.
>
> - A troca é **declarada na criação** e vale só para aquela Habilidade.
> - Ela **não muda os dados da linha do Nível** (16.3), nem o alcance, nem os alvos, nem nada da lista de 16.5. O que muda é **quando** você pode usar e **quanto** você paga.
> - Habilidade de **Nível 1 ou 2** já custa 1 PH, então nela não há o que trocar.
> - A troca vai para a **Ficha de Decisões da Mesa** (capítulo 27), como qualquer coisa que o Mestre aprova.

> **Exemplo completo — *Rebarba*, a Habilidade de Nível 4 da Nadir.**
>
> *Ficção:* ela crava a marreta no chão e o impacto sai pelo piso numa linha de brasa até o alvo.
>
> | Campo | Decisão |
> |---|---|
> | Nível | 4 (ela é nível 11, Nível máximo 4) |
> | Tipo | Dano |
> | Dados | **6d20** (média 63) + Bônus de Poder |
> | Elemento | Fogo, o Elemento dela |
> | Resolução | Teste de Ataque |
> | Alvos | Alvo único |
> | Alcance | Média (o Nível 4 permitiria até Extrema; ela não quis) |
> | Custo | **3 PH** |
> | Redução de Tenacidade | 4 |
> | Efeito extra | Nível 4 permite aplicar 1 condição: **Queimadura** |
>
> Na mesa isso virou: *"Rebarba. Teste de Ataque, acertei. 6d20 mais 2d20 de Fraqueza, Poder +5, Esfera Planar +4. Quatro de Tenacidade, total, porque bati na Fraqueza. E ele sai Queimando."*
>
> Repare no que ela **não** pôde escrever: o Nível 4 não concede Ação Extra (isso é Nível 5), não dá +4 de buff (isso é Nível 6) e não atinge 5 alvos em área (o teto do Nível 4 é 3).

---

## 16.8 Checklist de validação

Toda Habilidade escrita por jogador passa por esta checagem antes de entrar na ficha. O capítulo 27 traz o mesmo quadro do lado do Mestre, com o procedimento.

| Campo | Obrigatório? | Limite | Se violar |
|---|---|---|---|
| Nome e descrição | Sim | — | Volta para o jogador reescrever |
| Nível | Sim | ≤ o seu Nível máximo (16.6) | Rejeitada |
| Tipo | Sim | Dano, Cura, Buff, Debuff ou Passiva | Rejeitada |
| Dados | Sim, se Dano ou Cura | **Exatamente** os da linha do Nível (16.3) | Ajusta para a linha correta |
| Alcance | Sim | ≤ o alcance cumulativo do Nível | Reduz ao alcance do Nível |
| Alvos / área | Sim | Alvo único, ou **metade dos dados e até 3 alvos** (4 nos Níveis 6 e 7), agrupados a até uma Distância um do outro | Converte para área com metade dos dados e corta os alvos excedentes |
| Resolução | Sim | Teste de Ataque **ou** Teste de Resistência, **nunca os dois** | O Mestre escolhe um |
| Elemento | Sim | O seu Elemento, salvo Bênção que permita outro | Troca para o seu Elemento |
| Custo em PH | Automático | Pelo Nível (16.3) | — |
| Efeitos extras | Opcional | Dentro das linhas de 16.5 | Reduz ao permitido pelo Nível |
| Condição de recarga | Opcional | Só se você quiser trocar custo por frequência: **uma vez por combate por 1 PH menos**, piso de 1 PH (a régua está em **16.7**) | — |

**Alvo que passa no Teste de Resistência** (a regra completa está no capítulo 22): Habilidade de dano causa **metade do dano** (arredonda para baixo, mínimo 1) e **nenhum efeito secundário**; Habilidade sem dano **não produz efeito**; a Redução de Tenacidade só acontece **se houver dano**; e a **Energia da ação é ganha normalmente**.

### Efeitos proibidos em qualquer Nível

Lista fechada, para o Mestre não ter que argumentar:

- imunidade a dano;
- Vantagem permanente;
- **expandir a faixa de acerto crítico** — isso é exclusivo do Caminho da Caça (capítulo 14);
- mais de um **Avanço Total** por Ciclo;
- **Ação Extra** fora de *Ritmo Acelerado* ou de Habilidade de Nível 5 ou maior;
- ignorar Tenacidade;
- ignorar o **teto de RD**;
- **atingir mais alvos em área do que 16.4 permite**;
- cura total;
- "o alvo morre";
- remover a casa de alguém da Fila de Ação por mais de 1 turno;
- alterar a **Eficiência** ou a **Eficácia** de alguém;
- **trocar Eficiência por Eficácia na Esquiva**.

### Quando algo não passa

O Mestre tem duas respostas, nesta ordem:

1. **Ajusta.** É a primeira opção, e preserva a sua ideia: a mesma Habilidade, com o dado da linha certa ou um alvo a menos.
2. **Rejeita.** Só quando o conceito **só** funciona quebrando um limite.

Nos dois casos o motivo vai para a **Ficha de Decisões da Mesa** (capítulo 27), para a decisão valer para todo mundo na mesma situação.

> **A válvula de escape.** Habilidade aprovada que se revele quebrada em jogo pode ser **recriada sem custo** no próximo Descanso Longo. É isso que mantém o sistema aberto sem travar a campanha: ninguém precisa acertar de primeira.

A mesma estrutura — tabela de limites, ajuste antes de rejeição, registro da decisão — vale para **armas e itens** criados pelos jogadores (capítulo 24), para o **Memoespírito** (capítulo 11) e para os **Cones de Luz** (capítulo 25).

---

## 16.9 O terceiro teto: dados adicionais

Bônus numérico é uma moeda do sistema. **Dado** é a outra, e ela também tem limite.

> **Uma mesma rolagem não ganha mais de +3 dados base de fontes temporárias**, sem contar os **+2 da Fraqueza**. Os dados ganhos **por nível** (capítulo 18) e os **dados da tabela da Habilidade** (16.3) **não entram** nesse teto.

As fontes que disputam esses três dados, todas num lugar só: **Quebrado** +1, **Vulnerável** +1, **Marcação de Presa** +1, **Acúmulos de Cálculo** até +2, **Tabela do Riso** +1, as linhas de dado da régua de conversão das Bênçãos, **Avatar em Forma Manifestada** +2, o gatilho de Passiva de Nível 4 e a capstone da Caça no crítico.

O **dono deste teto é o capítulo 26**, junto com os outros dois. Ele aparece aqui porque é aqui que você escreve a Habilidade que vai tentar furá-lo.

---

## Resumo do capítulo

| | |
|---|---|
| **Quem escreve** | Você, com as tabelas deste capítulo e o aval do Mestre |
| **Níveis** | 1 a 7. Dano 21 / 27 / 39 / 63 / 105 / 147 / 189 de média |
| **Custo** | 1 / 1 / 2 / 3 / 4 / 5 / 6 PH |
| **PH do grupo** | `1 + nº de jogadores`, +1 nos níveis 9-16, +2 nos 17-20. Começa o combate com o máximo -2 |
| **Geração** | +1 PH por Ataque Básico que **acerta** (níveis 1-8), +2 (níveis 9-20) |
| **Ação** | A Habilidade ocupa o espaço do **Ataque Básico** |
| **Área** | Metade dos dados, **até 3 alvos** (4 nos Níveis 6 e 7), **teto absoluto de 6** |
| **Resolução** | Teste de Ataque **ou** Teste de Resistência do alvo — nunca os dois |
| **Teto da ficha** | **8 Habilidades conhecidas**, no nível 15. Do 16 em diante, reescreve 1 por nível |
| **Validação** | Checklist de 16.8 + lista fechada de efeitos proibidos |
