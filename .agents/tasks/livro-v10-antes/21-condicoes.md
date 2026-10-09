# Capítulo 21 — Condições

Uma **condição** é um estado com nome, número e prazo. Se está neste capítulo, está fechado: você não precisa negociar com o Mestre o que ela faz.

Este capítulo é o **catálogo único** do livro. Nenhuma Bênção, Habilidade, Ultimate, arma, Relíquia ou ficha de inimigo cria condição nova: todas elas apontam para um verbete daqui.

---

## 21.1 Regras gerais

**Como se lê um verbete.** Cada condição tem **efeito mecânico exato**, **duração** e **como termina**. Quando a duração diz "definida pela fonte", é o texto da Bênção ou da Habilidade que diz quantos turnos — e se ele não disser, é **1 turno**.

**Duração.** Efeito em alvo único se conta em **turnos do alvo**. Efeito de cena ou de grupo se conta em **Ciclos** (capítulo 19). Uma condição de "2 turnos" dura os dois próximos turnos **do alvo**, não dois turnos de quem aplicou.

**Quando o dano contínuo acontece.** Todo tique de **Dano Contínuo** aplica no **início do turno do alvo**, antes de ele agir. Dano Contínuo **não crita, não recebe dados de Fraqueza e ignora RD** (capítulo 20).

> **Regra de acúmulo global: nenhum alvo acumula mais de 5 instâncias de uma mesma condição.** Vale para todas, inclusive as que não citam acúmulo no verbete. Este capítulo é o dono dessa regra.

**Como condições terminam.** Por ordem de frequência na mesa:

| Via | O que remove |
|---|---|
| **A duração acabar** | o caso normal |
| **Habilidade de Nível 4 ou maior** construída para isso | **1** condição (capítulo 16) |
| **Bênção, Ultimate ou item** com texto explícito | o que o texto disser |
| **Descanso Longo** | **todas** as condições (capítulo 23) |
| **Descanso Curto** | **nenhuma**, salvo texto explícito |

**Cura não remove condição.** Curar PV não apaga Queimadura, não descongela e não limpa marca. A única exceção é o estado **Morrendo**: qualquer cura o remove e zera o contador (capítulo 23).

**Bônus e penalidades de condição entram nos tetos do capítulo 26** — o teto de bônus somado, o de penalidade somada e o de dados adicionais. Uma condição que dá +1 dado está disputando os mesmos três dados que o resto do seu arsenal.

---

## 21.2 As sete condições de Quebra

Uma por Elemento, aplicadas quando você Quebra a Tenacidade de um inimigo (capítulo 20). A **Eficiência** usada é a de quem aplicou.

### Sangramento — Físico

**Dano Contínuo igual a 5% dos PV máximos do alvo** por turno, até o teto de **3 × Eficiência**.

**Duração:** 2 turnos.

> Esta é a **única** exceção declarada da política do livro de não expressar efeito em porcentagem de PV máximo — e ela é exceção porque é assim que o autor escreveu o Sangramento na v0.1, e porque ela já tem teto próprio. Todo o resto do livro paga em valor fixo, dados ou múltiplo de nível.

**Na mesa:** contra um Elite de 365 PV, o Sangramento tira 18 por turno (`5% de 365 = 18`, e o teto de `3 × 8` = 24 não limita). Contra um Boss de 935, tiraria 46 — mas o teto corta em **24**.

### Queimadura — Fogo

**Dano Contínuo de `2d6 + Eficiência`**, de Fogo.

**Duração:** 2 turnos.

### Choque — Raio

**Dano Contínuo de `1d6 + Eficiência`**, de Raio.

**Duração:** 2 turnos.

### Cisalhamento de Vento — Vento

**Dano Contínuo de `1d6` por acúmulo**, de Vento, até **5 acúmulos**.

**Duração:** 2 turnos.

### Embaraço — Quântico

**`1d6` de dano Quântico por acúmulo**, até 5 acúmulos, e **Atrasa o alvo em 1 casa**.

Os acúmulos só entram **por ataques**, e eles precisam acontecer **antes do próximo turno do alvo** — passado o turno dele, a condição resolve e sai.

**Duração:** 1 turno.

### Aprisionamento — Imaginário

**`1d6 + Eficiência` de dano Imaginário** e **Atrasa o alvo em 2 casas**.

**Duração:** 1 turno.

### Congelado — Gelo

| Tipo de alvo | Efeito |
|---|---|
| **Comum** | **Perde o turno** (capítulo 19). Enquanto Congelado, **não pode ser Atrasado**, e os Atrasos pendentes contra ele são descartados |
| **Elite e Boss** (Firmeza) | **Não perdem o turno.** São **Atrasados em 2 casas** — que é o teto do Ciclo contra eles, então nada mais soma — e **não podem usar ação especial no turno seguinte** |

**Duração:** 1 turno. **Um alvo não pode ser Congelado em dois Ciclos consecutivos pela mesma fonte.**

> O Congelamento é o único efeito do livro que tira um turno inteiro, e é por isso que ele é o único com uma trava de repetição. A regra completa, com o que acontece se o alvo já agiu, está no capítulo 19.

---

## 21.3 Condições de controle e de marcação

### Lentidão

> **A sua Ação de Movimento não muda a sua Distância.** Para se mover **1 passo** você precisa gastar **Esforço Total** (capítulo 18) — ou seja, abrir mão do Ataque Básico e da Ação Complementar do turno.

**Não acumula.** **Duração:** definida pela fonte.

*Por quê ela zera o movimento em vez de reduzi-lo:* uma Ação de Movimento cobre exatamente **1** Distância, então "-1 Distância" já era zero. A versão fechada diz o que acontece (você não sai do lugar com o movimento normal) e dá a saída com nome e preço. O personagem **sobrecarregado** de inventário (capítulo 24) lê exatamente esta linha.

### Marcado

> **Quem aplicou a marca ganha +1 em Testes de Ataque contra o alvo marcado.**

- A fonte **pode** acrescentar um efeito por cima, dentro do teto de bônus somado (capítulo 26).
- Acumula até **3 vezes**.
- **Marcas de fontes diferentes não somam entre si:** cada um colhe a própria marca.

**Duração:** definida pela fonte.

A **Marcação de Presa** do Caminho da Caça (capítulo 14) é uma marca com regra própria, mais forte, e ela não é esta: é um recurso de Caminho, não a condição genérica.

### Silenciado

> **O alvo não pode usar Habilidades de Nível 4 ou maior.**

**Duração:** 1 turno.

Contra um personagem, isso derruba a ação grande do turno dele. Contra um inimigo, isso costuma significar a **ação especial** — e é por isso que o Silenciado é uma das ferramentas mais subestimadas do livro.

### Vulnerável

> **O alvo recebe +1 dado de dano da fonte indicada** pelo texto que aplicou a condição.

**Duração:** definida pela fonte.

### Controlado

> **Quem aplicou a condição decide as ações do alvo no turno dele.**

Quatro limites, e eles são o que impede o Controlado de ser o efeito mais forte do jogo:

1. O alvo pode usar **Ataque Básico, Ação de Movimento e Ação Complementar**. Ele **não** usa Habilidade, **não** usa Ultimate, **não** gasta PH, Energia nem Esforço.
2. Ele **não** executa ação que cause dano a si mesmo.
3. A condição termina na hora se quem controla **cair em Morrendo**, ficar Silenciado ou sair de cena.
4. Causar dano no alvo **não** remove a condição. Só a duração ou o item 3 removem.

**Duração:** definida pela fonte — o traço **To na sua mente** do Haloviano (capítulo 05), que é a fonte canônica, dá **2 turnos** contra Comum e **1 turno** contra Elite e Boss.

### Corrupção

Acúmulo do Caminho da Inexistência (capítulo 08).

> **Cada acúmulo aumenta em +1 o dano de cada Dano Contínuo seu naquele alvo**, até **5 acúmulos**.

**Duração:** até o fim do combate.

A Corrupção é do **aplicador**: dois jogadores da Inexistência no mesmo alvo contam acúmulos separados.

---

## 21.4 Condições de estado

### Quebrado — *só inimigos*

> **-2 de Defesa** e **recebe +1 dado de dano de qualquer fonte.**

**Duração:** até o **fim do próximo turno** do alvo, quando a Tenacidade dele também volta ao máximo (capítulo 20).

**Personagens jogadores e Memoespíritos nunca recebem esta condição**, porque não têm Tenacidade.

### Surpreso

> **A casa do alvo é pulada no primeiro Ciclo** (capítulo 19).

**Duração:** 1 Ciclo.

### Morrendo

> **0 PV, inconsciente.** O alvo **mantém a casa na Fila**, e no turno dele faz um **Teste de Força de Vontade contra DT 10** — somando só `d20 + Bônus de Presença`, **sem Eficiência**.

**Duração:** até estabilizar ou morrer. A regra inteira — os 3 sucessos contra 3 falhas, o 20 natural, o 1 natural, o dano enquanto Morrendo e a Execução — está no **capítulo 23**.

---

## 21.5 Tabela de consulta rápida

| Condição | Efeito | Duração | Acúmulo |
|---|---|---|---|
| **Sangramento** | Dano Contínuo = 5% dos PV máximos, teto `3 × Eficiência` | 2 turnos | até 5 |
| **Queimadura** | Dano Contínuo `2d6 + Eficiência` (Fogo) | 2 turnos | até 5 |
| **Choque** | Dano Contínuo `1d6 + Eficiência` (Raio) | 2 turnos | até 5 |
| **Cisalhamento de Vento** | Dano Contínuo `1d6` por acúmulo (Vento) | 2 turnos | **5** |
| **Embaraço** | `1d6` por acúmulo (só por ataques) e **Atrasa 1 casa** | 1 turno | **5** |
| **Aprisionamento** | `1d6 + Eficiência` e **Atrasa 2 casas** | 1 turno | até 5 |
| **Congelado** | Comum perde o turno; Elite e Boss são Atrasados 2 casas e perdem a ação especial | 1 turno | não repete em Ciclos seguidos pela mesma fonte |
| **Lentidão** | Ação de Movimento não muda a Distância; só sai do lugar com Esforço Total | fonte | **não acumula** |
| **Marcado** | +1 em Testes de Ataque de quem marcou | fonte | **3**, sem somar entre fontes |
| **Silenciado** | não pode usar Habilidade de Nível 4 ou maior | 1 turno | — |
| **Vulnerável** | +1 dado de dano da fonte indicada | fonte | até 5 |
| **Controlado** | quem aplicou decide as ações do alvo, sem Habilidade, Ultimate nem recursos | fonte | não acumula |
| **Corrupção** | +1 no dano de cada Dano Contínuo seu no alvo | fim do combate | **5** |
| **Quebrado** *(só inimigos)* | -2 de Defesa e +1 dado de dano de qualquer fonte | até o fim do próximo turno dele | — |
| **Surpreso** | casa pulada no primeiro Ciclo | 1 Ciclo | — |
| **Morrendo** | 0 PV, inconsciente, mantém a casa, Teste de Força de Vontade DT 10 no turno | até estabilizar ou morrer | — |

> **O que mudou da v0.1:** as condições existiam espalhadas pelos efeitos de Quebra e pelas Bênçãos, com durações vagas e, em alguns casos, com nome mas sem regra — "o alvo demorará mais um turno" e "tem dificuldade para conjurar habilidades poderosas" eram as duas piores, e as duas agora são **Silenciado**. Toda condição citada em qualquer página deste livro tem verbete aqui, com número e prazo. Se você achar uma que não tenha, é erro nosso: trate como a condição mais próxima desta lista e anote na Ficha de Decisões da Mesa.
