# Capítulo 19 — Fila de Ação e Velocidade

Este é o capítulo que diz **quem age antes de quem**, e ele é o coração mecânico de Explorando Galáxias. Metade das Bênçãos do livro fala de mover alguém na Fila; a Quebra move; o Gelo move; o Quântico e o Imaginário movem. Para tudo isso significar alguma coisa, a Fila precisa ser uma coisa concreta, desenhada numa tira de papel, que a mesa inteira vê.

É exatamente isso que ela é.

---

## 19.1 Velocidade — a quinta estatística

> **Velocidade (VEL) = 10 + Bônus de Agilidade + Bônus de Velocidade do Caminho + bônus de equipamento e efeitos**

A Velocidade fica na ficha ao lado de PV, Defesa, Esquiva e RD. Ela não é usada para calcular distância de movimento: ela serve para decidir **ordem**.

| Caminho | Bônus de VEL | Leitura |
|---|---|---|
| A Caça | **+4** | Age primeiro, quase sempre |
| A Euforia | +3 | Imprevisível e rápida |
| A Harmonia | +2 | Precisa agir antes para buffar |
| A Inexistência | +2 | Aplica o debuff antes da porrada chegar |
| A Destruição | +1 | |
| A Erudição | +1 | |
| A Abundância | +1 | |
| A Recordação | +1 | |
| A Preservação | +0 | Age por último e aguenta |

**Faixa esperada:** VEL **10 a 19** no nível 1; **12 a 21** no nível 10; **13 a 24** no nível 20 com equipamento. Os extremos absolutos da fórmula são **7** (Agilidade 8, Caminho +0, Armadura Pesada -2 — uma Preservação de tanque puro) e **25** (Agilidade 20, Caça +4, Botas de Tier IV +5, Armadura Leve +1).

> **Não existe ganho automático de Velocidade por nível.** O crescimento vem de **Relíquias** (as Botas dão +2/+3/+4/+5 por tier), de **Cone de Luz** e de **Bênção**.
>
> *Por quê:* se todos ganhassem VEL nos mesmos níveis, a ordem relativa do grupo nunca mudaria e a coluna seria decoração. Jogando o crescimento no equipamento, a Velocidade vira uma decisão de build — "abro mão de +1 de Defesa por +2 de VEL?" — e o Mestre ganha uma alavanca clara para desenhar inimigos rápidos.

A VEL dos inimigos por tipo e faixa está no capítulo 28, e ela foi calibrada com uma promessa: **a Caça equipada chega à frente de todo Comum e Elite da faixa dela** e disputa a primeira casa com o Boss. Essa promessa é verdadeira na mesa, não só na descrição do Caminho.

### Velocidade fora de combate

Perseguições, corridas e "quem chega primeiro na comporta" se resolvem com um **teste oposto**:

> `d20 + (VEL - 10)` contra `d20 + (VEL - 10)`, **melhor de três trocas**.

O `-10` existe porque a VEL é um valor absoluto, de 10 a 24, numa ordem de grandeza diferente de qualquer outro modificador do livro; subtraindo a base ela volta para a escala dos outros bônus. **Nunca se rola Velocidade contra uma DT da tabela de dificuldades** — a Velocidade só aparece em teste oposto.

---

## 19.2 Os quatro termos

| Termo | O que é |
|---|---|
| **Fila de Ação** | A lista ordenada de **todos** os combatentes, uma **casa** por combatente, numerada de 1 a N |
| **Casa** | A posição na Fila. A casa 1 age primeiro |
| **Turno** | A vez de **um** combatente. Ele usa as ações dele e a Fila avança |
| **Ciclo** | Uma passagem completa pela Fila. Quando o último combatente age, o Ciclo termina e a Fila é **remontada** |

Duração de combate se conta em **Ciclos**. Duração de efeito em alvo único se conta em **turnos do alvo**. As duas coisas não são a mesma, e o livro nunca as mistura.

> **Por quê uma Fila, e não um medidor.** O jogo de origem calcula a ordem com uma divisão por Velocidade, refeita a cada ação. Isso é inviável numa mesa: num combate com 4 personagens e 5 inimigos viram nove contas por Ciclo. Rolar a ordem a cada Ciclo também não serve — apagaria o efeito de Atrasar e Avançar, que é justamente a mecânica que mais aparece nas Bênçãos deste livro. A Fila de casas tem zero aritmética durante o combate, estado visível para a mesa inteira, e faz "Atrasar em 2 casas" significar literalmente duas casas.

---

## 19.3 Montando a Fila

1. **Ordene todos os combatentes por VEL, do maior para o menor.** Personagens e inimigos na mesma lista.
2. **Empates**, nesta ordem: maior **Bônus de Agilidade** vence; se persistir, maior **Bônus de Discernimento**; se ainda persistir, **os jogadores escolhem a ordem entre si** e vêm **antes** dos NPCs empatados.
3. **No início de cada Ciclo novo, remonte a Fila** com os valores de VEL **atuais** (buffs e debuffs de Velocidade entram aqui) e aplique os **Atrasos pendentes** marcados no Ciclo anterior.
4. **Não se rola nada para definir a ordem.** Quem é rápido age antes, sempre.

O passo 4 é uma decisão, não uma simplificação: é a promessa do Caminho da Caça, é o que faz o atributo Agilidade valer o investimento e é o que faz as Botas de Relíquia valerem dinheiro.

**Não existe Avanço pendente.** Avançar só funciona em quem ainda não agiu, dentro do Ciclo (19.5).

### Surpresa

Quando um lado começa o combate sem ser notado:

1. Cada combatente do lado pego de surpresa faz um **Teste de Percepção Mental contra DT 13**.
2. Quem **falha** recebe a condição **Surpreso** e tem a casa **pulada no primeiro Ciclo**. Quem passa age normalmente.

- **Se houver um atacante declarado se aproximando às escondidas**, ele faz **um** Teste de Furtividade, e o resultado dele **substitui a DT 13** para todo o lado emboscado. Um teste, não um por alvo: quem se esconde é quem rola, e quem está sendo emboscado reage a esse número.
- **A DT 13 é fixa em todas as faixas** e é uma das cinco DTs de subsistema do livro (capítulo 02). Surpresa é surpresa em qualquer nível de jogo: se ela escalasse com a faixa, um personagem de nível 20 sem Discernimento seria emboscado em quatro de cada cinco cenas, perdendo o Ciclo inteiro justamente onde o Boss age duas vezes por turno.
- **O Mestre declara** se há surpresa **antes** de montar a Fila. Não existe surpresa em combate já iniciado, e **não existe um Ciclo de surpresa separado**: a casa simplesmente é pulada.
- O traço **Raposa Astuta** dos Vulpes (capítulo 05) é uma segunda chance contra exatamente esse teste.
- Grupo emboscando inimigo funciona igual, com os papéis trocados.

---

## 19.4 Atrasar

> **Atrasar em N casas:** mova a ficha do alvo **N casas para o fim da Fila**. Cada casa que ele desce é um combatente que age antes dele.

- Se o alvo **ainda não agiu** neste Ciclo, o efeito é imediato e visível na tira.
- Se o alvo **já agiu** neste Ciclo, ou se não há casas suficientes atrás dele, o excedente fica marcado como **Atraso pendente** e entra na remontagem do próximo Ciclo: ele começa N casas abaixo da posição que a VEL lhe daria.

**Teto de Atraso, por alvo, por Ciclo:**

| Tipo de alvo | Teto | Firmeza |
|---|---|---|
| **Comum** | **3 casas** | Não tem |
| **Elite e Boss** | **2 casas** | **Tem** |

### Firmeza — a ordem de operação

Elite e Boss têm **Firmeza**. Resolva **nesta ordem**, sem atalho:

1. **Some todas as casas de Atraso** aplicadas ao alvo neste Ciclo, **de todas as fontes**.
2. **Divida o total por 2, arredondando para baixo.**
3. Se o resultado for **0** e houver pelo menos 1 casa bruta, o resultado é **1**. Esse mínimo vale para o **total do Ciclo**, nunca para cada fonte separadamente.
4. **Aplique o teto de 2 casas.** O excedente é perdido.

> **Por quê a ordem virou lista numerada:** porque aplicar a Firmeza **por fonte** anula a Firmeza.
>
> **Exemplo que mostra isso.** Embaraço (5 acúmulos de 1 casa cada) + Aprisionamento (2 casas) = **7 casas brutas** no mesmo Ciclo.
> - *Errado, por fonte:* cada acúmulo de 1 casa vira `floor(0,5) = 0`, o mínimo devolve 1, e os 5 acúmulos continuam valendo 5 casas. A Firmeza não fez nada.
> - *Certo, pelo total:* `floor(7 ÷ 2) = 3`, teto 2 → **o Boss perde 2 casas**.
>
> **Exemplo pequeno, para o mínimo aparecer.** Só a Quebra, 1 casa bruta: `floor(0,5) = 0` → mínimo → **1 casa**.

*Por quê teto e Firmeza existem:* sem eles, um grupo com Quântico e Imaginário tranca um Boss fora da Fila para sempre. Isso é vencer sem lutar — tecnicamente ótimo, dramaticamente péssimo, porque a mesa inteira fica olhando o Mestre passar a vez. Com teto 2 e Firmeza pelo total, o grupo rouba **1 ou 2 casas** de um Boss por Ciclo: o suficiente para sentir controle, insuficiente para apagar o vilão. Contra Comum, onde controle total **é** o ponto, o teto é 3 e não há Firmeza.

---

## 19.5 Avançar e Avanço Total

> **Avançar em N casas:** mova a ficha **N casas para o início da Fila**. Só funciona se o alvo **ainda não agiu** neste Ciclo.
>
> **Avanço Total:** o alvo age **imediatamente após o turno atual**, mesmo que já tenha agido neste Ciclo. **No máximo uma vez por Ciclo por criatura.**

O Avanço Total é o "turno extra" do sistema e é o efeito mais forte que uma Habilidade de Nível 5 ou uma Ultimate de suporte pode conceder. Ele é recurso raro e explicitamente limitado — sem o teto, dois jogadores se adiantam um ao outro em loop e o Ciclo deixa de significar nada.

> **O teto do Avanço Total e o teto da Ação Extra (capítulo 18) são o mesmo teto, pelo mesmo motivo:** os dois entregam turno extra, e dois efeitos que entregam turno extra não podem ter respostas diferentes. **Eles são contados separadamente** — uma criatura pode receber 1 Ação Extra **e** 1 Avanço Total no mesmo Ciclo, e nenhum dos dois tetos foi excedido.

---

## 19.6 Perder o turno (Congelamento)

O **Congelamento** é o efeito de Quebra do Gelo (capítulo 20), e é a única coisa no jogo que tira um turno inteiro de alguém.

**Contra Comum:**

- O alvo é **retirado da Fila neste Ciclo**: a ficha sai da tira e ele não age.
- Se ele **já agiu** quando o Congelamento é aplicado, ele perde o turno do **próximo** Ciclo. Marque "Congelado" ao lado do nome.
- Enquanto está Congelado, o alvo **não pode ser Atrasado** — não há turno para atrasar — e os **Atrasos pendentes contra ele são descartados**.
- O Congelamento consome exatamente **um turno** e termina. Na remontagem seguinte, o alvo volta à posição normal de VEL.
- **Um alvo não pode ser Congelado em dois Ciclos consecutivos pela mesma fonte.**

**Contra Elite e Boss (Firmeza):**

> **Elite e Boss não perdem o turno por Congelamento.** Em vez disso, o Congelamento os **Atrasa em 2 casas** — que é o teto de Atraso de um Ciclo contra eles, e por isso **nenhum outro Atraso aplicado no mesmo Ciclo soma com este** — e eles **não podem usar ação especial no turno seguinte**.

*Por quê:* a Firmeza protege Elite e Boss contra Atraso, e perder o turno é um Atraso infinito. Com a cadência de Quebra do jogo — cerca de uma Quebra a cada 2 Ciclos contra Boss — um único personagem de Gelo Congelaria o Boss a cada 2 Ciclos, e num combate de 4 Ciclos o Boss perderia **metade** das ações dele. O Gelo não perdeu o papel: Atrasar 2 casas num Boss é o **máximo** que o sistema permite a qualquer fonte, e tirar a ação especial dele por um turno costuma valer mais que o dano.

---

## 19.7 Casos-limite

Todos resolvidos, para a mesa não ter que inventar no meio da cena:

| Situação | Resolução |
|---|---|
| **Combatente entra no meio do combate** (invocação, reforço) | Entra pela VEL nas casas **restantes** do Ciclo. Se a VEL dele seria maior que a de quem está agindo, ele entra na **casa imediatamente seguinte** |
| **Memoespírito** | Tem **casa própria** na Fila, pela VEL dele, e **1 ação por turno** (capítulo 11) |
| **Combatente morre ou foge** | A casa é removida e o Ciclo continua. Atrasos pendentes dele são descartados |
| **Combatente a 0 PV (Morrendo)** | **Mantém a casa.** O turno dele é onde o Teste de Força de Vontade acontece (capítulo 23) |
| **Surpresa** | Quem falha no Teste de Percepção Mental de 19.3 fica **Surpreso** e tem a casa **pulada** no primeiro Ciclo |
| **Duas Ultimates declaradas juntas** | Quem falou primeiro resolve primeiro, e quem decide quem falou primeiro é o **Mestre** |
| **Atrasar alguém que está na última casa** | Vira **Atraso pendente** do próximo Ciclo, respeitando o teto |
| **Avançar alguém que já agiu** | **Não acontece.** Só o Avanço Total faz isso |
| **Efeito muda a VEL no meio do Ciclo** | A posição **atual não muda**. A VEL nova entra na próxima remontagem |

---

## 19.8 Como isso fica no papel

Você precisa de uma tira de papel, uma ficha por combatente — moeda, dado, pedaço de papel com o nome — e duas linhas de anotação.

```
CICLO 2
casa:   1       2        3       4        5        6
      [Vesper] [Nadir]  [Koru]  [Elite]  [Comum]  [Lin Hai]
       VEL 16   VEL 14   VEL 13  VEL 12   VEL 11    VEL 10
                          ^ agindo agora

pendentes: Elite -1 casa (Quebra, Ciclo 3)     Comum: CONGELADO (Ciclo 3)
condições: Nadir: Queimadura (2 turnos)        Elite: Quebrado (até o fim do turno dele)
```

Nada de calculadora, nada de planilha. O estado do combate inteiro cabe em quatro linhas, e qualquer pessoa da mesa pode olhar e saber o que vai acontecer.

A **Trilha de Ação** para imprimir está no capítulo 29.

> **Dica de Mestre.** Deixe a tira virada para os jogadores, não para você. A decisão interessante do jogo — "eu ulto agora ou espero o Boss Quebrar?" — só existe se a mesa consegue **ver** quem age depois de quem.

---

## 19.9 Se você jogou a v0.1

A v0.1 falava de "casas" e de **derrubar o turno** em cerca de quinze lugares, sem nunca dizer o que era uma casa. Agora diz, e a linguagem é uma só:

- **Derrubar o turno em N casas** passou a se chamar **Atrasar em N casas** (19.4).
- Adiantar alguém passou a se chamar **Avançar**, e o turno extra passou a se chamar **Avanço Total** (19.5).
- Perder o turno por Gelo passou a ser a condição **Congelado** (19.6 e capítulo 21).
- O que a v0.1 chamava de "turno do grupo" é o **Ciclo**; "turno" é de **um** combatente só.

Toda Bênção, Habilidade, condição e ficha de inimigo deste livro usa essas quatro palavras, com esses significados. A lista completa dos termos aposentados, com o nome novo ao lado, está no **capítulo 30**.

---

## Resumo do capítulo

| | |
|---|---|
| **VEL** | 10 + Agilidade + Caminho + equipamento. Cresce só por equipamento e Bênção |
| **Fila** | todos ordenados por VEL, uma casa cada, remontada a cada Ciclo. Nada é rolado |
| **Empate** | Agilidade → Discernimento → jogadores escolhem e vêm antes dos NPCs |
| **Surpresa** | Teste de Percepção Mental **DT 13** (ou contra o Teste de Furtividade de quem emboscou); quem falha tem a casa pulada |
| **Atrasar** | teto **3 casas** contra Comum, **2** contra Elite e Boss |
| **Firmeza** | some o Ciclo → divida por 2 arredondando para baixo → mínimo 1 no total → teto 2 |
| **Avançar** | só em quem não agiu. **Avanço Total:** 1 por Ciclo por criatura |
| **Congelamento** | Comum perde o turno; Elite e Boss são Atrasados 2 casas e perdem a ação especial |
