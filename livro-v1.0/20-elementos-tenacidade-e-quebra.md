# Capítulo 20 — Elementos, Tenacidade e Quebra

Todo dano neste jogo tem um **Elemento**. E todo inimigo tem uma barra de **Tenacidade** que você arranca batendo nele até ela chegar a zero — e aí acontece a melhor coisa do combate: a **Quebra**.

Os dois subsistemas são um só, e este capítulo é o dono dele.

---

## 20.1 Os 7 Elementos

> **Físico · Fogo · Gelo · Raio · Vento · Quântico · Imaginário**

Cada personagem escolhe **1 Elemento** na criação (capítulo 03), ligado ao Caminho e ao conceito. Ele não muda.

- As suas **Habilidades** e a sua **Ultimate** causam dano desse Elemento.
- **Armas sem Elemento próprio causam dano Físico**, mesmo que o seu Elemento pessoal seja outro. Se você quer que a sua arma bata com o seu Elemento, ela precisa ter esse Elemento declarado (capítulo 18).
- **Dano de Quebra** e **Dano Contínuo** herdam o Elemento da fonte.

O Elemento faz duas coisas que importam: define **quanto dano a mais** você causa contra Fraqueza e define **quanta Tenacidade** você arranca.

| Elemento | Temática | O que ele entrega na Quebra |
|---|---|---|
| **Físico** | Impacto, lâmina, calibre, pancada | **Sangramento** — o maior Dano de Quebra do jogo |
| **Fogo** | Combustão, forja, fúria | **Queimadura** — empatado como maior Dano de Quebra |
| **Gelo** | Frio, paralisia, silêncio branco | **Congelamento** — tira o turno de um Comum |
| **Raio** | Descarga, sobrecarga, nervo | **Choque** — dano contínuo que dura **3 turnos** |
| **Vento** | Corte, pressão, erosão | **Cisalhamento de Vento** — acumula até 5 vezes |
| **Quântico** | Probabilidade, emaranhado, peso | **Embaraço** — dano acumulável e **Atrasa 1 casa** |
| **Imaginário** | Significado, selo, prisão de ideias | **Aprisionamento** — **Atrasa 2 casas** |

A hierarquia é clara e é de propósito, e os sete Elementos se dividem em **três grupos**:

- **Físico e Fogo pagam em dano na hora da Quebra.** São os dois maiores Danos de Quebra do jogo (20.5), e o efeito deles é o complemento, não o ponto.
- **Raio e Vento pagam em dano que fica.** O Dano de Quebra deles é a metade do de Fogo, e a troca está no Dano Contínuo: o **Choque** tira menos por tique que a Queimadura e dura **3 turnos** em vez de 2; o **Cisalhamento de Vento** começa menor e **concentra**, somando um acúmulo a cada ataque seu, até `5d6` por turno do alvo (capítulo 21). Um estende, o outro empilha.
- **Gelo, Quântico e Imaginário pagam em controle.** O Dano de Quebra deles é só a sua Eficiência, e o que você compra com isso é turno do inimigo. Num sistema com a Fila de Ação do capítulo 19, isso vale muito.

> **O que mudou da v1.1:** antes desta versão o Raio não estava em grupo nenhum desta lista, e a tabela acima prometia "dano contínuo confiável" sem nada na mecânica que entregasse confiabilidade: o Choque tinha a mesma duração da Queimadura e metade do dano por tique. Com os **3 turnos** do capítulo 21, o grupo existe e a promessa é verdadeira. **Nenhum número de 20.5 mudou.**

---

## 20.2 Fraquezas e Resistências

Todo inimigo tem Fraquezas. Normalmente:

| Tipo de inimigo | Fraquezas |
|---|---|
| **Comum** | 1 a 2 |
| **Elite** | 3 |
| **Boss** | 4 |

**O que acontece quando o Elemento do seu ataque bate no alvo:**

| Situação | Dano | Redução de Tenacidade |
|---|---|---|
| É **Fraqueza** do alvo | **+2 dados** do mesmo tipo do ataque | **total** |
| **Neutro** (nem Fraqueza, nem Resistência) | dano normal | **metade** (arredonda para baixo, mínimo 1) |
| O alvo tem **Resistência** | **-2 dados**, conservando sempre **no mínimo 1 dado** | **1 ponto**, fixo |

> **Os dados ganhos por Fraqueza não critam.** Essa é regra do autor e continua valendo (capítulo 18). Eles também ficam **fora** do teto de dados adicionais (capítulo 26), porque a Fraqueza é o contrato de encontro do jogo, não um bônus de build.

### Descobrir uma Fraqueza

> **Ação Complementar:** faça um **Teste de Pesquisa, Ciência ou Sintonia** contra a DT da **faixa do inimigo**. Em um sucesso, o Mestre revela **uma** Fraqueza, à escolha dele. Cada tentativa seguinte contra o mesmo inimigo revela outra.

| Faixa de nível do inimigo | 1-4 | 5-8 | 9-12 | 13-16 | 17-20 |
|---|---|---|---|---|---|
| **DT para descobrir uma Fraqueza** | 13 | 14 | 15 | 16 | 17 |

Esta é uma das **cinco DTs de subsistema** do livro (capítulo 02) e ela **vence** a tabela geral de DT do capítulo 27. Ela cresce muito mais devagar que a DT Média da faixa — que chega a 25 no fim do jogo — porque descobrir Fraqueza é **rotina de combate**, não feito heroico. Com DT 25, o subsistema morreria justamente onde ele vale mais.

Inimigo de nível misto usa a faixa do **mais forte** do grupo dele.

O **Intellitron** (capítulo 05) faz esse teste **com Vantagem** e descobre **duas** Fraquezas num sucesso.

> **O Mestre não esconde Fraqueza o combate inteiro.** A regra, do lado dele, está no capítulo 27: ele revela as Fraquezas assim que o grupo passa num teste de identificação **ou** depois do primeiro Ciclo de combate. Esconder tudo converteria o sistema de Elementos em adivinhação, e adivinhação não é decisão.

---

## 20.3 Tenacidade

> **Só inimigos têm Tenacidade.** Personagens jogadores e o Memoespírito **não** têm barra de Tenacidade, **não** podem ser Quebrados e **nunca** recebem a condição Quebrado. A ficha do personagem tem PV, Defesa, Esquiva, RD e Velocidade — e nada mais.
>
> Nenhuma Bênção, Habilidade, Ultimate, Cone de Luz ou conjunto de Relíquias deste livro dispara "quando um aliado é Quebrado", porque isso não existe. Este capítulo é o dono dessa regra.

A **Tenacidade** é um número por inimigo: quanto ele aguenta de pressão antes de ceder. Você a reduz batendo, e quanto mais forte a ação, mais ela cai.

| Fonte | Redução de Tenacidade |
|---|---|
| **Ataque Básico** | 1 |
| Habilidade de **Nível 1-2** | 2 |
| Habilidade de **Nível 3** | 3 |
| Habilidade de **Nível 4** | 4 |
| Habilidade de **Nível 5** | 5 |
| Habilidade de **Nível 6** | 6 |
| Habilidade de **Nível 7** | 7 |
| **Ultimate** | **5**, em todas as faixas |
| **Dano Contínuo** | **0** — só ataque reduz Tenacidade |

Esse número é o **bruto**. Ele passa pelo filtro do seu Elemento (20.2): total contra Fraqueza, **metade** contra neutro, **1 ponto** contra Resistência.

> **A Redução de Tenacidade é condicionada ao acerto.** Ataque que erra **não** reduz Tenacidade. Efeito resolvido por Teste de Resistência em que o alvo **passa** só reduz Tenacidade **se ainda houver dano** (capítulo 22). A v0.1 já dizia isso com outras palavras: para retirar Tenacidade é obrigatório que o alvo receba um ataque.

*Por quê a redução não é tudo-ou-nada:* a v0.1 dizia que você não pode reduzir a Tenacidade de um inimigo que não tenha Fraqueza ao seu Elemento. Numa mesa de 4 jogadores com 4 Elementos fixos contra um Comum de 1 Fraqueza, **três jogadores ficariam estruturalmente fora** do sistema de Quebra — e a Quebra é metade da graça do combate. No jogo de origem você troca de personagem; na mesa, o jogador fica sentado. Com a redução em três níveis, todo mundo participa, e quem bate na Fraqueza participa **o dobro**.

### Implante de Fraqueza

Duas coisas do livro **acrescentam** uma Fraqueza temporária a um inimigo, por **1 Ciclo**:

- uma **Habilidade de Nível 4 ou maior** construída para isso (capítulo 16);
- a Bênção **Implante de Fraqueza**, do Caminho da Inexistência (capítulo 08).

É a resposta ativa do grupo contra um inimigo de Elemento inconveniente, e é o papel clássico do quebrador de defesas.

### Tenacidade dos inimigos, por tipo e faixa

| Faixa | Comum | Elite | Boss |
|---|---|---|---|
| **1-4** | 3 | 5 | 10 |
| **5-8** | 3 | 6 | 11 |
| **9-12** | 4 | 7 | 12 |
| **13-16** | 4 | 6 | 12 |
| **17-20** | 4 | 7 | 13 |

> **Por que a coluna não sobe sempre.** Repare que o Elite cai de 7 para 6 entre as
> faixas 9-12 e 13-16, e o Boss empata em 12 nas duas. **Não é erro de digitação.** A
> Tenacidade não é um número escolhido a dedo: ela é **derivada da redução efetiva que o
> grupo entrega por Ciclo** naquela faixa — Boss a cada 2 Ciclos, Elite e Comum a cada
> Ciclo — já descontando os ataques que erram. Como o poder do grupo não cresce em
> degraus iguais de faixa para faixa, a Tenacidade derivada também não. O que é constante
> é a **cadência de Quebra**, não a altura da barra. As contas estão abertas no
> apêndice 29.4.

Os números parecem pequenos, e são pequenos de propósito: eles já contam que **boa parte dos seus ataques erra**. Na prática, a cadência que essa tabela entrega é:

| Contra | Quebra sai a cada |
|---|---|
| **Comum** | o primeiro ataque sério que ele receber |
| **Elite** | quase todo Ciclo |
| **Boss** | **cerca de 2 Ciclos** |

A derivação completa — redução do grupo por Ciclo, taxa de acerto por perfil e multiplicador por tipo — está no apêndice de balanceamento do capítulo 29. O capítulo 28 traz a ficha de inimigo com todas as colunas.

---

## 20.4 Quebra

> **Quando a Tenacidade de um inimigo chega a 0, ele sofre Quebra.**

Resolva as cinco coisas, nesta ordem:

1. Ele sofre **Dano de Quebra** do Elemento que causou a Quebra, mais o **efeito de Quebra** daquele Elemento (20.5).
2. Ele é **Atrasado em 1 casa** (capítulo 19). Contra Elite e Boss, essa casa entra no somatório de **Firmeza** do Ciclo: sozinha ela ainda vale 1 casa pelo mínimo, mas somada a outras fontes ela é dividida junto.
3. Ele recebe a condição **Quebrado** até o fim do próximo turno dele: **-2 de Defesa** e recebe **+1 dado** de dano de qualquer fonte.
4. Quem quebrou ganha **+10 de Energia** (1 vez por Ciclo — capítulo 17).
5. A **Tenacidade volta ao máximo no fim do próximo turno do alvo**, junto com o fim da condição Quebrado.

O passo 5 é o que faz a Quebra ser um **ritmo** e não um interruptor: a barra volta, e o grupo tem que derrubar de novo. É a batida do combate inteiro.

> **O Dano de Quebra é uma instância de dano**, então ele **sofre RD** (capítulo 18). O Dano Contínuo que vem junto, não — Dano Contínuo ignora RD (20.6).

> **Exemplo de Ciclo com Quebra.** O Boss da faixa 9-12 tem **12** de Tenacidade e Fraqueza a Fogo.
> Ciclo 1: Nadir acerta a Habilidade de Nível 4 com Fogo (**-4**, total) e dois Ataques Básicos do grupo acertam com Elementos neutros (**-1** cada, metade de 1 arredondada para baixo é 0, mínimo 1). A Ultimate de Vesper sai e acerta (**-5**, mas o Vento dela é neutro contra esse Boss → **-2**). Tenacidade em **12 - 4 - 1 - 1 - 2 = 4**.
> Ciclo 2: Nadir acerta de novo com a Habilidade (**-4**). **Zerou: Quebra.** O Boss toma o Dano de Quebra de Fogo, pega **Queimadura** por 2 turnos, é **Atrasado em 1 casa** (Firmeza: 1 casa bruta → mínimo 1 → 1 casa), fica **Quebrado** até o fim do turno dele, e Nadir ganha **+10 de Energia**.
> Ciclo 3: enquanto ele está Quebrado, **todo mundo** ganha +1 dado de dano e a Defesa dele caiu 2. É o Ciclo em que o grupo gasta o que tem.

---

## 20.5 Dano de Quebra

| Elemento | Dano de Quebra | Efeito de Quebra |
|---|---|---|
| **Físico** | **2d6 + (2 × Eficiência)** | Sangramento |
| **Fogo** | **2d6 + (2 × Eficiência)** | Queimadura |
| **Raio** | **1d6 + Eficiência** | Choque |
| **Vento** | **1d6 + Eficiência** | Cisalhamento de Vento |
| **Gelo** | **Eficiência** | **Congelamento** |
| **Quântico** | **Eficiência** | Embaraço |
| **Imaginário** | **Eficiência** | Aprisionamento |

A Eficiência usada é a **sua** (capítulo 02), então o Dano de Quebra cresce com o seu nível sem precisar de tabela nova.

Nos valores de mesa: no nível 3, um Dano de Quebra Físico sai em `2d6 + 4` (média **11**); no nível 19, em `2d6 + 16` (média **23**). Gelo, Quântico e Imaginário saem em **2** no nível 3 e **8** no nível 19 — e entregam, em troca, o efeito que decide o Ciclo.

Os efeitos de Quebra são **condições**, e todas elas têm verbete com números, duração e como terminam no **capítulo 21**.

> **O que mudou da v0.1:** o Dano de Quebra ia de **6d4** (Físico) a **1d2** (Gelo) — uma diferença de doze vezes, com números que não escalavam com nada. A hierarquia que o autor escreveu está preservada (Físico e Fogo no topo, controle embaixo), mas agora ela escala com a Eficiência e cabe na mesma escala do resto do livro.

---

## 20.6 Dano Contínuo

O **Dano Contínuo (DC)** é o dano que fica. É a identidade mecânica do Caminho da Inexistência e a sobra de quase todo efeito de Quebra.

- Aplica no **início do turno do alvo**.
- A duração é contada em **turnos do alvo**.
- **Três exceções, e elas andam juntas:** o Dano Contínuo **não crita**, **não recebe dados de Fraqueza** e **ignora RD**.
- Danos Contínuos de **Elementos diferentes coexistem**. Do **mesmo** Elemento, acumulam até o limite daquele efeito.
- Ele **não reduz Tenacidade** (20.3).

*Por quê ignora RD:* com RD de 6 a 18 ao longo do jogo e tiques de `1d6` a `2d6 + 16`, a RD anularia o Caminho da Inexistência por completo. Em troca, o Dano Contínuo não crita e não ganha dados de Fraqueza — ele é **confiável, não explosivo**. E é a única fonte de dano do livro contra a qual nada na ficha defende, a não ser cura: é um dos quatro motivos pelos quais um grupo quer alguém cuidando dele (capítulo 27).

---

## Resumo do capítulo

| | |
|---|---|
| **Elementos** | Físico, Fogo, Gelo, Raio, Vento, Quântico, Imaginário. 1 por personagem, fixo |
| **Fraqueza** | +2 dados (que não critam) e redução **total** de Tenacidade |
| **Neutro** | dano normal e **metade** da Redução de Tenacidade |
| **Resistência** | -2 dados (mínimo 1 dado) e **1 ponto** de Tenacidade |
| **Descobrir Fraqueza** | Ação Complementar: Pesquisa, Ciência ou Sintonia vs DT 13/14/15/16/17 |
| **Tenacidade** | **só inimigos**. Comum 3-4 · Elite 5-7 · Boss 10-13, pelas cinco faixas |
| **Quebra** | Dano de Quebra + efeito + **Atrasa 1 casa** + **Quebrado** + 10 de Energia; barra volta no fim do próximo turno dele |
| **Quebrado** | -2 de Defesa e +1 dado de dano de qualquer fonte |
| **Dano Contínuo** | início do turno do alvo; **não crita, não ganha Fraqueza, ignora RD**, não tira Tenacidade |
