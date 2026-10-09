# Diff do livro: v1.0 -> v1.1

Diff unificado (3 linhas de contexto) de cada `.md` alterado. Arquivo novo: `00-changelog-v10-para-v11.md` (inteiro, no fim).

## 00-capa-e-creditos.md

```diff
--- v1.0/00-capa-e-creditos.md
+++ v1.1/00-capa-e-creditos.md
@@ -6,7 +6,7 @@
 
 **by MC Filhos**
 
-**Versão 1.0**
+**Versão 1.1**
 
 ---
 
@@ -15,7 +15,7 @@
 | | |
 |---|---|
 | **Sistema** | Explorando Galáxias |
-| **Versão** | 1.0 |
+| **Versão** | 1.1 |
 | **Autoria, criação e regras** | MC Filhos |
 | **Idioma** | Português do Brasil |
 | **Faixa de níveis** | **1 a 20** |
@@ -47,6 +47,8 @@
 
 O capítulo 01 resume o que mudou da v0.1 para cá. O **changelog completo** — tudo que foi adicionado, tudo que foi corrigido e cada decisão que alterou um número do autor, com justificativa — está em **`00-changelog-v01-para-v10.md`**, escrito para ser discordado ponto a ponto.
 
+A **v1.1** é a v1.0 revisada contra a ficha automatizada: corrige o exemplo que contrariava a regra e escreve por extenso as regras que deixavam dúvida. Nenhum número de balanceamento (PV, dano, Tenacidade, orçamento) mudou. A lista está em **`00-changelog-v10-para-v11.md`**.
+
 ---
 
 ## Como este livro está organizado
```

## 01-introducao.md

```diff
--- v1.0/01-introducao.md
+++ v1.1/01-introducao.md
@@ -94,7 +94,7 @@
 - **Construção de base, criação de facção e artesanato profundo.** Nada no livro cita essas coisas como regra.
 - **Posicionamento exato.** Não existe grade, não existe medida em metros. A escala de **Distâncias** (Pessoal, Curta, Média, Longa, Extrema) é abstrata de propósito, e "os alvos estão juntos?" é uma pergunta que o Mestre responde olhando a cena.
 
-Nenhuma regra deste livro depende de nada dessa lista. Isso é intencional: o defeito mais comum de um sistema inacabado é uma regra apontando para um subsistema que não existe, e a v1.0 foi varrida justamente para isso.
+Nenhuma regra deste livro depende de nada dessa lista. Isso é intencional: o defeito mais comum de um sistema inacabado é uma regra apontando para um subsistema que não existe, e este livro foi varrido justamente para isso.
 
 ---
 
```

## 03-criacao-de-personagem.md

```diff
--- v1.0/03-criacao-de-personagem.md
+++ v1.1/03-criacao-de-personagem.md
@@ -229,7 +229,7 @@
 ## Passo 12 — Equipamento, nome e acabamento
 
 - **Uma arma.** Escolha uma das 6 categorias do capítulo 18 e descreva a sua. Se ela tiver um Elemento próprio, ele entra aqui; senão, o dano é Físico.
-- **Uma Armadura ou Vestimenta:** Leve (+3 de Defesa, +1 de Velocidade), Média (+5) ou Pesada (+6, 2 RD, -2 em Testes e Perícias de Agilidade, -2 de Velocidade e **não permite Esquiva**). A aparência é sua (capítulo 24).
+- **Uma Armadura ou Vestimenta:** Leve (+3 de Defesa, +1 de Velocidade), Média (+5) ou Pesada (+6, 2 RD, -2 em Reflexos e nas Perícias de Agilidade, -2 de Velocidade e **não permite Esquiva**). A aparência é sua (capítulo 24).
 - **Um Cone de Luz de Nível 1** e as **Relíquias de Tier I** nos slots que você tiver (capítulo 25). Eles são concedidos pelo Mestre como recompensa de marco, não comprados — e no começo da campanha o marco é "você começou".
 - **Inventário:** a capacidade é `10 + (2 × Bônus de Poder)` de Espaço (capítulo 24).
 - **Nome, aparência, de onde você veio e uma coisa que você carrega e não serve para nada.** Essa última é a que a mesa vai lembrar.
```

## 04-atributos-e-pericias.md

```diff
--- v1.0/04-atributos-e-pericias.md
+++ v1.1/04-atributos-e-pericias.md
@@ -148,6 +148,8 @@
 
 O **mínimo de 2** é um conserto: a conta da v0.1, com Sincronia 8, entregava **uma** Perícia escolhida. Agora o piso é 2, e a Sincronia continua sendo o atributo que amplia a sua folha de competências.
 
+**A quantidade de Perícias escolhidas é fixada na criação**, com o Bônus de Sincronia que você tem nesse momento (já com o bônus da Raça). Aumentar a Sincronia depois (4.3) **não dá Perícia nova**.
+
 Perícia nova depois da criação só entra pela via dos **slots de Eficácia** (capítulo 02): eles dobram uma Perícia que você já tem, não adicionam Perícias novas. Se a sua mesa quiser treinar Perícias novas em jogo, isso é decisão de mesa — anote na Ficha de Decisões (capítulo 29).
 
 ---
```

## 07-caminho-destruicao.md

```diff
--- v1.0/07-caminho-destruicao.md
+++ v1.1/07-caminho-destruicao.md
@@ -16,6 +16,7 @@
 |---|---|
 | **Aeon** | Nanook |
 | **Eixo mecânico** | Dano bruto pago com os próprios PV |
+| **Recurso próprio** | **Os seus PV**, gastos como moeda (7.2) |
 | **Atributo de Habilidade** | **Poder** ou **Vigor** (escolha fixa na criação) |
 | **Perícias com Eficiência** | **Atletismo**, **Sobrevivência**, **Resistência** |
 | **Índice de vitalidade N** | **6** — o maior do jogo |
```

## 08-caminho-inexistencia.md

```diff
--- v1.0/08-caminho-inexistencia.md
+++ v1.1/08-caminho-inexistencia.md
@@ -14,6 +14,7 @@
 |---|---|
 | **Aeon** | Ix |
 | **Eixo mecânico** | Dano Contínuo e acúmulo de penalidades |
+| **Recurso próprio** | Nenhum além dos acúmulos das Bênçãos: **Marca do Vazio** (até 3) e **Corrupção** (até 5) |
 | **Atributo de Habilidade** | **Discernimento** ou **Sincronia** (escolha fixa na criação) |
 | **Perícias com Eficiência** | **Percepção**, **Pesquisa**, **Furtividade** |
 | **Índice de vitalidade N** | **4** |
```

## 09-caminho-harmonia.md

```diff
--- v1.0/09-caminho-harmonia.md
+++ v1.1/09-caminho-harmonia.md
@@ -16,6 +16,7 @@
 |---|---|
 | **Aeon** | Xipe |
 | **Eixo mecânico** | Fortalecer o grupo e mexer na Fila de Ação |
+| **Recurso próprio** | Nenhum além dos acúmulos das Bênçãos: **Eco da Vitória** (até 3) |
 | **Atributo de Habilidade** | **Presença** |
 | **Perícias com Eficiência** | **Liderança**, **Sintonia**, **Persuasão** |
 | **Índice de vitalidade N** | **3** |
```

## 10-caminho-abundancia.md

```diff
--- v1.0/10-caminho-abundancia.md
+++ v1.1/10-caminho-abundancia.md
@@ -16,6 +16,7 @@
 |---|---|
 | **Aeon** | Yaoshi |
 | **Eixo mecânico** | Cura, PV temporários e sustentação do grupo |
+| **Recurso próprio** | Nenhum além dos acúmulos das Bênçãos: **Florescimento** (até 5) |
 | **Atributo de Habilidade** | **Presença** ou **Sincronia** (escolha fixa na criação) |
 | **Perícias com Eficiência** | **Liderança**, **Intuição**, **Sobrevivência** |
 | **Índice de vitalidade N** | **5** |
```

## 11-caminho-recordacao.md

```diff
--- v1.0/11-caminho-recordacao.md
+++ v1.1/11-caminho-recordacao.md
@@ -16,6 +16,7 @@
 |---|---|
 | **Aeon** | Fuli |
 | **Eixo mecânico** | Lutar acompanhado: o **Memoespírito** |
+| **Recurso próprio** | **Memoespírito** (11.3 a 11.5) |
 | **Atributo de Habilidade** | **Sincronia** ou **Discernimento** (escolha fixa na criação) |
 | **Perícias com Eficiência** | **Intimidação**, **Investigação**, **Ciência** |
 | **Índice de vitalidade N** | **3** |
```

## 18-combate.md

```diff
--- v1.0/18-combate.md
+++ v1.1/18-combate.md
@@ -133,7 +133,7 @@
 |---|---|---|---|
 | Leve | +3 | +1 de Velocidade | Permitida |
 | Média | +5 | — | Permitida |
-| Pesada | +6 | **2 RD**, -2 em Testes e Perícias de Agilidade, -2 de Velocidade | **Proibida** |
+| Pesada | +6 | **2 RD**, -2 em Reflexos e nas Perícias de Agilidade (não no Teste de Ataque), -2 de Velocidade | **Proibida** |
 
 A tabela completa, com aparência, peso e preço, está no capítulo 24.
 
```

## 21-condicoes.md

```diff
--- v1.0/21-condicoes.md
+++ v1.1/21-condicoes.md
@@ -86,6 +86,8 @@
 | **Elite e Boss** (Firmeza) | **Não perdem o turno.** São **Atrasados em 2 casas** — que é o teto do Ciclo contra eles, então nada mais soma — e **não podem usar ação especial no turno seguinte** |
 
 **Duração:** 1 turno. **Um alvo não pode ser Congelado em dois Ciclos consecutivos pela mesma fonte.**
+
+**Congelado só existe em inimigo.** Ele vem da Quebra do Gelo, e personagem não tem Tenacidade (capítulos 20 e 28): nenhum inimigo, Bênção ou Habilidade deste livro Congela um personagem. Por isso a tabela acima não tem linha para você.
 
 > O Congelamento é o único efeito do livro que tira um turno inteiro, e é por isso que ele é o único com uma trava de repetição. A regra completa, com o que acontece se o alvo já agiu, está no capítulo 19.
 
@@ -186,7 +188,7 @@
 | **Cisalhamento de Vento** | Dano Contínuo `1d6` por acúmulo (Vento) | 2 turnos | **5** |
 | **Embaraço** | `1d6` por acúmulo (só por ataques) e **Atrasa 1 casa** | 1 turno | **5** |
 | **Aprisionamento** | `1d6 + Eficiência` e **Atrasa 2 casas** | 1 turno | até 5 |
-| **Congelado** | Comum perde o turno; Elite e Boss são Atrasados 2 casas e perdem a ação especial | 1 turno | não repete em Ciclos seguidos pela mesma fonte |
+| **Congelado** | **Só inimigos.** Comum perde o turno; Elite e Boss são Atrasados 2 casas e perdem a ação especial | 1 turno | não repete em Ciclos seguidos pela mesma fonte |
 | **Lentidão** | Ação de Movimento não muda a Distância; só sai do lugar com Esforço Total | fonte | **não acumula** |
 | **Marcado** | +1 em Testes de Ataque de quem marcou | fonte | **3**, sem somar entre fontes |
 | **Silenciado** | não pode usar Habilidade de Nível 4 ou maior | 1 turno | — |
```

## 22-testes-de-resistencia.md

```diff
--- v1.0/22-testes-de-resistencia.md
+++ v1.1/22-testes-de-resistencia.md
@@ -101,7 +101,7 @@
 
 O valor é `Eficiência da faixa -1` para Comum, `Eficiência` para Elite e `Eficiência +1` para Boss. **Não existe inimigo sem esse número.**
 
-Contra a DT de Habilidade de um personagem típico (`8 + 5 + Eficiência`, ou seja **15 / 17 / 18 / 19 / 21** nas cinco faixas), o inimigo **falha em 65% / 60% / 55%** das vezes conforme o tipo — exatamente a mesma janela do seu acerto com Teste de Ataque. As duas vias de resolução têm a mesma chance de passar. A diferença entre elas é só o que acontece quando o alvo **tem** sucesso.
+Contra a DT de Habilidade de um personagem típico (`8 + 5 + Eficiência`, ou seja **15 / 17 / 18 / 19 / 21** nas cinco faixas, contadas no nível de referência de cada uma: **3, 7, 11, 15 e 19**, os do capítulo 27), o inimigo **falha em 65% / 60% / 55%** das vezes conforme o tipo — exatamente a mesma janela do seu acerto com Teste de Ataque. As duas vias de resolução têm a mesma chance de passar. A diferença entre elas é só o que acontece quando o alvo **tem** sucesso.
 
 ---
 
```

## 23-dano-cura-e-morte.md

```diff
--- v1.0/23-dano-cura-e-morte.md
+++ v1.1/23-dano-cura-e-morte.md
@@ -116,6 +116,8 @@
 3. **Um aliado pode impedir com a Reação Intervir** (capítulo 18). **Intervir cancela a Execução:** no lugar dela, o executor pode fazer o Ataque Básico dele **contra o interventor**, resolvido normalmente. A Execução não é dano — é morte automática sem rolagem — então não há o que "receber no lugar". O que Intervir faz é interromper o ato e obrigar o executor a lutar com alguém de pé.
 4. **Xianzhouítas não podem ser Executados** (capítulo 05). Eles continuam caindo em Morrendo e continuam rolando o Teste — com Vantagem, pelo traço racial.
 
+> **Quem rola o Teste de Morrendo com Vantagem.** Três Raças, e pelo mesmo motivo: todas têm **Vantagem em Força de Vontade** (capítulo 05), e a Força de Vontade é o Teste de Morrendo (capítulo 22). O **Xianzhouíta**, pela Vantagem em todo Teste de Resistência; o **Vulpes**, pela Vantagem em Testes de Presença; e o **Avginiano**, pela Mente de Ferro. A Vantagem não muda a conta: continua `d20 + Bônus de Presença`, sem Eficiência.
+
 > **Para o Mestre.** O Executado é uma ferramenta de tensão, não de contabilidade. Um inimigo racional que executa é um inimigo que está mandando uma mensagem, e a mesa vai lembrar dele. Use quando a cena pedir; não use porque o Comum estava ali do lado. O capítulo 27 fala disso.
 
 > **O que mudou da v0.1:** a regra do Executado estava escrita **dentro** do traço racial dos Xianzhouítas — ou seja, a regra mais letal do jogo morava num benefício que seis das sete Raças nunca leriam, e ela não dizia qual Teste nem qual DT usar. Agora ela é uma regra geral, com o Teste nomeado (**Força de Vontade**), a DT escrita (**10**) e a exceção Xianzhouíta no lugar certo: como exceção.
```

## 24-equipamentos.md

```diff
--- v1.0/24-equipamentos.md
+++ v1.1/24-equipamentos.md
@@ -14,11 +14,12 @@
 |---|---|---|---|---|---|
 | **Leve** | **+3** | **+1 de Velocidade** | Permitida | 1 | 150 Cr |
 | **Média** | **+5** | — | Permitida | 2 | 300 Cr |
-| **Pesada** | **+6** | **2 RD**, **-2 em Testes e Perícias de Agilidade**, **-2 de Velocidade** | **Proibida** | 3 | 500 Cr |
+| **Pesada** | **+6** | **2 RD**, **-2 em Reflexos e nas Perícias de Agilidade**, **-2 de Velocidade** | **Proibida** | 3 | 500 Cr |
 
 - **A aparência é sua.** Casaco de piloto, placa de combate da Legião, uniforme de gala com fibra blindada por baixo: o que importa é a linha da tabela.
 - A **penalidade fixa da Pesada fica fora do teto de penalidade somada** (capítulo 26): é escolha permanente de equipamento, igual ao +6 de Defesa que vem com ela.
-- **Armadura Pesada não permite Esquiva.** É o preço real dos +6, e é o que mantém a Pesada dentro do orçamento de defesa do jogo.
+- **O -2 da Pesada, por extenso:** vale no **Teste de Resistência de Reflexos** e nas três **Perícias de Agilidade** — **Acrobacia**, **Furtividade** e **Pilotagem** (capítulo 04). Ele **não** mexe no seu Bônus de Agilidade: **não afeta o Teste de Ataque**, nem a Defesa, nem a conta da Velocidade além do -2 de Velocidade que já está na linha.
+- **Armadura Pesada não permite Esquiva.** Não é Esquiva com -2: com a Pesada, a Reação Esquiva **não existe** (capítulo 18). É o preço real dos +6, e é o que mantém a Pesada dentro do orçamento de defesa do jogo.
 - Vestir ou trocar de armadura **não** é coisa de combate: leva alguns minutos de ficção.
 
 > **O que mudou da v0.1:** a Leve dava "+1 de Bônus de Agilidade", o que mexia em PV, Defesa, Esquiva e Perícias de uma vez só; virou **+1 de Velocidade**, o mesmo sabor de leve e rápido sem tocar no atributo. A Pesada tinha **10 de RD** e **-5 em Testes de Agilidade**; virou **2 RD**, **-2** e **-2 de Velocidade**, mais a proibição de Esquiva. Num jogo onde a Eficiência chega a +8 e os bônus temporários têm teto de +5, um -5 fixo seria a maior penalidade do livro e tornaria a Pesada inutilizável para quem rola Agilidade; e 10 de RD, no nível 2, era invulnerabilidade.
@@ -208,7 +209,7 @@
 
 | | |
 |---|---|
-| **Armaduras** | Leve +3 e +1 VEL · Média +5 · Pesada +6, **2 RD**, -2 em Agilidade, -2 VEL, **sem Esquiva** |
+| **Armaduras** | Leve +3 e +1 VEL · Média +5 · Pesada +6, **2 RD**, -2 em Reflexos e Perícias de Agilidade, -2 VEL, **sem Esquiva** |
 | **Armas** | 6 categorias: 1d8 / 1d10 / 1d12 / 1d8 / 1d10 / 2d8, mais **uma** propriedade especial |
 | **Dado extra de arma** | níveis **5, 9, 13 e 17** |
 | **Poções** | cura fixa **15 / 30 / 50**, Espaço 0,5 / 1 / 2 |
```

## 25-cones-de-luz-e-reliquias.md

```diff
--- v1.0/25-cones-de-luz-e-reliquias.md
+++ v1.1/25-cones-de-luz-e-reliquias.md
@@ -85,8 +85,9 @@
 
 ### Sobreposição
 
-> **Sobreposição:** uma segunda cópia do **mesmo** Cone aumenta o **Bônus Maior** dele, até o **teto absoluto de +3** (ou **+50 PV**).
+> **Sobreposição:** uma cópia a mais do **mesmo** Cone aumenta o **Bônus Maior** dele. **Cada Sobreposição soma +1 na parte numérica e +10 na parte de PV** — nas duas, num Cone de "e"; só na que você escolheu, num Cone de "ou".
 
+- **Teto: a parte numérica para em +3, e a de PV para junto com ela.** Quem conta é a parte numérica, inclusive num Cone de "ou" que você fez em PV: **2 Sobreposições** num Cone de Nível 1 ou 2 (a parte numérica chega a **+3**; a de PV, a **+30**), **1** num de Nível 3 ou 4 (**+3**; PV **+35**) e **nenhuma** num de Nível 5, que já está no teto absoluto (**+3** ou **+50 PV**).
 - A Sobreposição serve para um Cone de Nível baixo **alcançar** o valor de um Cone de Nível alto, **não para ultrapassá-lo**.
 - Ela **não** é comprada nem sorteada: é **recompensa narrativa**, no máximo **uma por faixa de nível**.
 - Sobreposição **não** acrescenta Efeito Condicional novo nem aumenta a frequência dele.
@@ -155,7 +156,7 @@
 | **Conjunto de 2 peças** | Temporário | **Sim** |
 | **Conjunto de 4 peças** | Temporário | **Sim** |
 | **Bônus de Armadura ou Vestimenta** | Permanente | **Não** |
-| **Sobreposição de Cone** | Permanente (aumenta o Bônus Maior) | **Não**, até o teto de +3 ou +50 PV |
+| **Sobreposição de Cone** | Permanente (aumenta o Bônus Maior) | **Não**, até o teto de +3 (25.2) |
 
 E os dados: **+1 dado** vindo de Cone ou de Conjunto disputa o **teto de dados adicionais** (+3 por rolagem, sem contar os +2 da Fraqueza) com Quebrado, Vulnerável, marcas e acúmulos. O dono desse teto é o capítulo 26.
 
@@ -169,7 +170,7 @@
 |---|---|
 | **Como se consegue** | **Recompensa de marco.** Tier da faixa em todos os slots; Cone trocável pelo Nível que o seu nível permite. Sem compra, sem sorteio |
 | **Cone de Luz** | 1 por personagem, Nível 1 a 5, com **Bônus Maior** (fixo) e **Efeito Condicional** (gatilho) |
-| **Sobreposição** | Mesma cópia aumenta o Bônus Maior, teto **+3** ou **+50 PV**, no máximo **uma por faixa** |
+| **Sobreposição** | Cada cópia do mesmo Cone soma **+1** e **+10 PV** ao Bônus Maior, até **+3** (o PV para junto), no máximo **uma por faixa** |
 | **Relíquias** | 6 slots: Cabeça, Mãos, Tronco, Botas, Esfera Planar, Corda de Ligação |
 | **Tiers** | I (1-6) · II (7-12) · III (13-17) · IV (18-20) |
 | **Disjuntos** | **Mãos** no Ataque Básico, **Esfera Planar** na Habilidade, na Ultimate e no Dano Contínuo. Nunca na mesma rolagem |
```

## 26-progressao-e-ressonancias.md

```diff
--- v1.0/26-progressao-e-ressonancias.md
+++ v1.1/26-progressao-e-ressonancias.md
@@ -39,7 +39,7 @@
 | 13 | +6 | 2 P / 2 TR | 7 | 7 | 5 | — | **4** | +2 | 14 |
 | 14 | +6 | **3 P / 2 TR** | 7 | 7 | 5 | — | 4 | +2 | 14 |
 | 15 | +6 | 3 P / 2 TR | 8 | 8 | **6** | **+2** | 4 | +2 | 14 |
-| 16 | +7 | 3 P / 2 TR | 8 | 8 (reescreve 1 por nível) | 6 | — | 4 | +2 | 16 |
+| 16 | +7 | 3 P / 2 TR | 8 | 8 (reescreve 1 por nível, do 16 ao 20) | 6 | — | 4 | +2 | 16 |
 | 17 | +7 | **4 P / 2 TR** | 9 | 8 | 6 | — | **5** | **+3** | 16 |
 | 18 | +7 | 4 P / 2 TR | 9 | 8 | **7** | **+2** | 5 | +3 | 16 |
 | 19 | +8 | 4 P / 2 TR | 10 | 8 | 7 | — | 5 | +3 | 18 |
```

## 27-guia-do-mestre.md

```diff
--- v1.0/27-guia-do-mestre.md
+++ v1.1/27-guia-do-mestre.md
@@ -510,7 +510,7 @@
 
 Dito em voz alta para não voltar como surpresa no meio da sua campanha:
 
-- **Campanha, cenário e aventura prontas.** Esta v1.0 é o **livro de regras**. Todo o material de 27.12 a 27.18 é ambientação de apoio e gancho de cena, não uma campanha publicada: não há mapa de galáxia, linha do tempo nem arco escrito sessão por sessão.
+- **Campanha, cenário e aventura prontas.** Este é o **livro de regras**. Todo o material de 27.12 a 27.18 é ambientação de apoio e gancho de cena, não uma campanha publicada: não há mapa de galáxia, linha do tempo nem arco escrito sessão por sessão.
 - **Regras de nave, rota e viagem interestelar.** O Expresso Astral chega quando a história precisa. Ficam para um suplemento.
 - **Economia detalhada.** Os Créditos do capítulo 24 são preços de referência e verba de marco, não um subsistema econômico.
 - **Combate em grade com posicionamento exato.** A escala de Distâncias abstratas é uma decisão, não uma falta.
```

## 29-apendices-e-fichas.md

```diff
--- v1.0/29-apendices-e-fichas.md
+++ v1.1/29-apendices-e-fichas.md
@@ -591,9 +591,9 @@
 
 ### Passo 12 — Equipamento, nome e acabamento
 
-- **Arma:** *marreta de doca*, categoria **Pesada** (`1d12`, Poder, 2 mãos). Teste de Ataque do básico: `d20 + 4 + 2` = **+6**. Dano: `1d12 + 4` = **10** médio, Físico.
+- **Arma:** *marreta de doca*, categoria **Pesada** (`1d12`, Poder, 2 mãos). Teste de Ataque do básico: `d20 + 4 + 2` = **+6**. Dano: `1d12 + 4 + 2` = `1d12 + 6` = **12** médio, Físico. O **+2** é a Relíquia de **Mãos I**, logo abaixo, que soma no dano de todo Ataque Básico (capítulo 25).
 - **Armadura Média**, um macacão de serviço reforçado nas placas.
-- **Cone de Luz de Nível 1** e **Relíquias de Tier I** nos slots que o Mestre já concedeu: **Mãos** (+2 de dano de Ataque Básico) e **Botas** (+2 de Velocidade) → a VEL dela sobe para **14**.
+- **Cone de Luz de Nível 1** e **Relíquias de Tier I** nos slots que o Mestre já concedeu: **Mãos** (+2 de dano de Ataque Básico) e **Botas** (+2 de Velocidade) → a VEL dela sobe para **14**. O Bônus Maior do Cone **ainda não tem alvo**: ela escolhe quando o Mestre der nome e história ao Cone, e até lá ele não soma em nada — por isso nenhum número desta ficha o inclui.
 - **Inventário:** `10 + (2 × 4)` = **18** de Espaço.
 - **Uma coisa que ela carrega e não serve para nada:** o crachá cortado ao meio da doca que a expulsou.
 
@@ -614,7 +614,7 @@
                          Intimidação, Mecânica
 Testes de Resistência: todos os 6, com Eficiência
 
-Arma:      marreta de doca — Pesada, 1d12 + 4, Físico, ataque +6
+Arma:      marreta de doca — Pesada, 1d12 + 6 (com Mãos I), Físico, ataque +6
 Armadura:  Média (+5 de Defesa)
 Habilidade: Rebarba — Nível 1, 6d6 + 4 de Fogo, 1 PH, Tenacidade 2
 Ultimate:   A Doca Inteira — 5d10 + 4 de Fogo, Tenacidade 5
@@ -874,7 +874,7 @@
 
 **Tetos que a mesa esquece:** bônus somado **+3 / +4 / +5** por faixa · penalidade somada **-3 / -4 / -5** · dados adicionais **+3** por rolagem (sem contar a Fraqueza) · RD `2 + (2 × Eficiência)` · PV temporários `3 × Eficiência` · acúmulos de uma condição **5** · Habilidades conhecidas **8**.
 
-**Condições, em uma linha cada:** Sangramento, Queimadura, Choque, Cisalhamento de Vento (Dano Contínuo, 2 turnos, ignora RD) · Embaraço e Aprisionamento (dano + Atraso) · Congelado (Comum perde o turno; Elite e Boss são Atrasados 2 casas) · Lentidão · Marcado · Silenciado · Vulnerável · Controlado · Corrupção · Quebrado (só inimigos) · Surpreso · Morrendo. Os verbetes completos estão no capítulo 21.
+**Condições, em uma linha cada:** Sangramento, Queimadura, Choque, Cisalhamento de Vento (Dano Contínuo, 2 turnos, ignora RD) · Embaraço e Aprisionamento (dano + Atraso) · Congelado (só inimigos: Comum perde o turno; Elite e Boss são Atrasados 2 casas) · Lentidão · Marcado · Silenciado · Vulnerável · Controlado · Corrupção · Quebrado (só inimigos) · Surpreso · Morrendo. Os verbetes completos estão no capítulo 21.
 
 **Morrendo:** 0 PV, mantém a casa na Fila, **Força de Vontade DT 10** com `d20 + Presença` **apenas**. 3 sucessos estabiliza com 1 PV, 3 falhas morre, 20 natural levanta, 1 natural vale 2 falhas, dano é 1 falha (2 se crítico ou Habilidade de Nível 5+). Cura de 1 PV levanta.
 
```

## 30-glossario.md

```diff
--- v1.0/30-glossario.md
+++ v1.1/30-glossario.md
@@ -164,7 +164,7 @@
 |---|---|---|
 | **Sangramento** | Dano Contínuo igual a **5% dos PV máximos** do alvo, com teto `3 × Eficiência`. A **única** exceção declarada à política de não usar porcentagem de PV | 21 |
 | **Silenciado** | Condição: não pode usar Habilidade de **Nível 4 ou maior** | 21 |
-| **Sobreposição** | Usar uma cópia do mesmo Cone de Luz para aumentar o **Bônus Maior**. Teto +3 ou +50 PV, no máximo uma por faixa | 25 |
+| **Sobreposição** | Usar uma cópia do mesmo Cone de Luz para aumentar o **Bônus Maior**. Cada uma soma +1 e +10 PV, até +3 (o PV para junto), no máximo uma por faixa | 25 |
 | **Stellaron** | A semente de catástrofe que escreve o fim de um mundo. Ferramenta de campanha | 27 |
 | **Sucesso Automático** | Se o seu bônus total for **igual ou maior que a DT**, não role. **Só em Teste de Perícia** | 27 |
 | **Surpresa / Surpreso** | Gatilho de **DT 13** no início do combate. Quem é Surpreso tem a casa pulada no primeiro Ciclo | 19, 21 |
```

## 00-changelog-v10-para-v11.md (novo)

```markdown
# Changelog — da v1.0 para a v1.1

**Sistema:** Explorando Galáxias · **Autoria:** MC Filhos · **Versão:** 1.1

A v1.1 nasceu da **ficha automatizada**. Para a planilha fazer as contas sozinha, cada regra do livro precisou virar fórmula, e uma fórmula não aceita "depende". Onde o livro deixava dúvida ou um exemplo contrariava a regra, a ficha teve que escolher uma leitura. Esta versão escreve essas leituras no livro, para o livro e a ficha dizerem a mesma coisa.

**Nenhum número de balanceamento mudou:** PV, dano, DPC, Tenacidade, orçamento de encontro e tabelas de Habilidade são os mesmos da v1.0. Só uma correção altera um número impresso: o dano da marreta da Nadir (D1), que estava errado pela própria regra do livro.

> **Sobre o nome da pasta.** Os capítulos continuam na pasta `livro-v1.0/`. O nome é **histórico**: renomeá-la obrigaria a mexer em todos os scripts de montagem e verificação, e o conteúdo dela já é o da v1.1. A versão atual é a que está na capa.

---

## As correções

| # | Onde | Como era | Como ficou | Por quê |
|---|---|---|---|---|
| **D1** | 29.7, Passo 12 e ficha fechada | Marreta da Nadir: `1d12 + 4`, **10** médio | `1d12 + 4 + 2` = `1d12 + 6`, **12** médio, com o +2 de **Mãos I** escrito | A mesma ficha tem Mãos I, que soma +2 em todo Ataque Básico (25.3). O exemplo esquecia a Relíquia. A regra manda, então o exemplo mudou |
| **D2** | 07.1 a 11.1, ficha do Caminho | Só 12 a 15 tinham a linha **Recurso próprio** | 07: **os seus PV** (7.2) · 08: acúmulos de **Marca do Vazio** e **Corrupção** · 09: acúmulos de **Eco da Vitória** · 10: acúmulos de **Florescimento** · 11: **Memoespírito** | As nove fichas de Caminho agora têm as mesmas linhas. Onde o Caminho não tem recurso além das Bênçãos, a linha diz isso |
| **D3** | 23.5 | A Vantagem no Teste de Morrendo só aparecia para o Xianzhouíta | Quadro novo: **Xianzhouíta, Vulpes e Avginiano** rolam Morrendo com Vantagem | Vulpes e Avginiano têm Vantagem em Força de Vontade (05), e Força de Vontade é o Teste de Morrendo (22.1). A regra já valia; faltava escrita |
| **D4** | 24.1 (também 03, 18.4 e o resumo de 24) | Pesada: "-2 em Testes e Perícias de Agilidade" | **-2 no Teste de Resistência de Reflexos e nas Perícias de Agilidade** (Acrobacia, Furtividade, Pilotagem). Não afeta o Teste de Ataque, a Defesa nem o Bônus de Agilidade. A Esquiva não fica com -2: ela **não existe** com a Pesada | "Testes de Agilidade" podia ser lido como o Teste de Ataque das armas de Agilidade. 18.2 não lista penalidade de armadura no ataque |
| **D5** | 25.2, Sobreposição (também a tabela de tetos, o resumo de 25 e o glossário) | "Aumenta o Bônus Maior até o teto absoluto de +3 (ou +50 PV)", sem dizer quanto cada cópia soma | **Cada Sobreposição soma +1 na parte numérica e +10 na de PV.** A parte numérica para em +3, e a de PV para junto: 2 Sobreposições nos Níveis 1 e 2 (+30 PV), 1 nos Níveis 3 e 4 (+35 PV), nenhuma no 5. Continua **uma por faixa** | O incremento vem do exemplo do próprio 25.2 (`+1 e +10 PV` → `+2 e +20 PV`). Com +10 por cópia, "+3 ou +50 PV" não fechava: o +3 chegava em 2 cópias e os +50 PV só em 4. Agora a mesma contagem leva aos dois tetos, e nada passa do Cone de Nível 5 (+3 ou +50 PV) |
| **D6** | 21.2, verbete Congelado (também a tabela de 21.5 e 29.12) | O verbete só definia o efeito em Comum, Elite e Boss | Escrito: **Congelado só existe em inimigo** | Congelado vem da Quebra do Gelo, e personagem não tem Tenacidade (20.3, 28.2). Nenhum inimigo, Bênção ou Habilidade do livro Congela personagem |
| **D7** | 04.5 | Perícias escolhidas = `2 + Bônus de Sincronia`, sem dizer de quando | **A quantidade é fixada na criação** (Sincronia já com a Raça). Aumentar a Sincronia depois não dá Perícia nova | O parágrafo seguinte já dizia que Perícia nova depois da criação só vem por decisão de mesa. Faltava dizer que a Sincronia não reabre a conta |
| **N1** | 26.2, linha do nível 16 | "8 (reescreve 1 por nível)" só na linha do 16 | "8 (reescreve 1 por nível, do 16 ao 20)" | 16.6 diz "a partir do nível 16". A célula agora diz o mesmo |
| **N2** | 29.7, Passo 12 | A Nadir tinha Cone de Luz de Nível 1 sem alvo do Bônus Maior | Escrito: o alvo ainda não foi escolhido, e até lá o Cone **não soma em nada** | Nenhum número da ficha fechada incluía o Cone. Agora o texto diz por quê |
| **N3** | 07 a 15, Bênçãos | A frequência das Bênçãos fica no texto do Efeito | **Sem mudança** | Não é erro: cada Bênção já diz no Efeito quando vale ("uma vez por turno", "por Ciclo", "por combate") |
| **N4** | 22.3, Teste de Resistência do inimigo | DT típica 15 / 17 / 18 / 19 / 21 "nas cinco faixas", sem dizer o nível | Escrito: contada no **nível de referência** de cada faixa, **3, 7, 11, 15 e 19** (capítulo 27) | Sem o nível, a conta `8 + 5 + Eficiência` não podia ser refeita. A ficha usava 3, 8, 11, 14 e 19, que dão os mesmos cinco números; o livro fica com os níveis de referência que ele já usa no capítulo 27 |
| **N5** | 26.3, PH | A tabela de PH é de mesa de 4 | **Sem mudança** | 26.3 já diz isso e aponta a fórmula de 16.2, que vale para qualquer tamanho de mesa |
| **R1** | 01.6 e 27.19 (revisão independente) | "a v1.0 foi varrida" e "Esta v1.0 é o livro de regras" no texto corrido | "este livro foi varrido" e "Este é o livro de regras" | O texto falava da v1.0 como versão atual, mas a capa é 1.1. A seção 01.7, que conta a história da v0.1 para a v1.0, fica como está |

---

## O que não mudou

- O changelog **da v0.1 para a v1.0** continua com o nome e o conteúdo dele. Ele registra o que a v1.0 fez com a v0.1, e isso é história. A linha da Armadura Pesada lá ainda diz "-2 em Testes e Perícias de Agilidade", porque era o texto da v1.0; a leitura correta é a de D4 acima.
- Os arquivos `Sistema de HSR by MC Filhos V1.0.docx` e `.pdf` ficam como estão, como registro. Os da v1.1 têm `V1.1` no nome.

```
