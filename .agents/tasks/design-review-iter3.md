# Review de Design — Explorando Galáxias v1.0 (iteração 3)

**Documento revisado:** `.agents/tasks/design.md` (2.036 linhas, lido por inteiro)
**Fontes de verificação:** `.agents/tasks/v01-extraido.txt` (1.164 linhas, lido por inteiro, com contagens de termo medidas por regex), `.agents/orquestrador-override.md` (override de faixa 1-20), `assets/imagens-v01/` (17 PNGs conferidos), `scripts/` (2 scripts presentes), `livro-v1.0/` (vazio)
**Revisor:** subagente de review de design, sem o contexto que produziu o documento
**Método:** leitura integral; recálculo independente das 5 parcelas do DPC nas 5 faixas; recálculo das 45 células de PV, das 15 células de orçamento de inimigo, das janelas de acerto dos dois lados, da attrition e da derivação de Tenacidade; extração automática das 100 seções e de todas as referências `X.Y` para checar ponteiro quebrado
**Veredito:** **CHANGES_REQUESTED** — 4 HIGH, 12 MEDIUM, 10 NIT

---

## Avaliação narrativa

### (a) O design preserva o DNA do sistema? **Sim.**

Conferi contra a fonte, item por item. Fica tudo que era identidade: a rolagem única `d20 + Bônus de Atributo + Eficiência ≥ DT`; os 6 Atributos com as descrições do autor; as 18 Perícias (contei: 18) com os atributos originais e as 3 Perícias de cada Caminho escrito; os 7 Elementos e os 7 efeitos de Quebra; os 9 Caminhos na **ordem exata** de vitalidade (o `N` da v1.0 reproduz o número de dados da v0.1 um a um, de Destruição 6 a Caça 2); as 7 Raças; o array `15, 14, 13, 12, 10, 8`; a Ultimate em 100 de Energia declarada em voz alta, com desempate pelo ouvido do Mestre; Tenacidade e Quebra; o Guia de Criação de Memoespírito inteiro (12 pontos, teto 5, +1 a cada 2 níveis, 5 Conceitos, 4 Funções, 6 bônus menores escolhendo 3, 2 Habilidades próprias); e o coração do sistema, que é o jogador escrever as próprias Habilidades com tabelas-guia.

A curva de Eficiência é preservada **nos níveis 1 a 8**, e as duas alterações (nível 9 de +5 para +4, nível 10 de +6 para +5) estão no changelog como decisão. As 50 Bênçãos dos 5 Caminhos escritos (10 cada, contadas uma a uma) são preservadas por régua de conversão, não reescritas.

A ressalva de preservação do review anterior foi resolvida: a **Especialização de Combate** agora é apresentada em três lugares (3.2, 4.3, 21.2 item 14) como **mecânica nova**, e confirmei na fonte que a v0.1 realmente não tem nenhum bônus de ataque progressivo por nível.

Sobrou uma sequela de preservação, de conteúdo e não de número: a régua de 11.4 declara cobrir "todas as construções fora de escala que a v0.1 produz", mas o Caminho da Destruição inteiro é construído sobre **custo em porcentagem do PV máximo** e nenhuma das quatro Bênçãos que fazem isso tem linha na régua — incluindo o "sacrificar PV o quanto quiser por dados" do Avatar da Destruição, que é a construção mais explorável da v0.1 (achado 15).

### (b) As 6 lacunas estruturais estão resolvidas de forma coerente e jogável? **Cinco fechadas; a economia de ações ainda tem porta aberta, e o Teste de Ataque ganhou um segundo caminho sem saída.**

- **Ciclo/turno (L01) — a melhor parte do documento, e agora fechada.** A Firmeza ganhou **ordem de operação numerada** e teto de 2 casas contra Elite e Boss. Verifiquei os dois exemplos: 7 casas brutas → `floor(3,5) = 3` → teto **2**; 1 casa bruta → `floor(0,5) = 0` → mínimo **1**. Batem. O furo do Congelamento foi tapado pela mesma via, o que deixa **uma** regra para a mesa decorar em vez de duas.
- **Velocidade (L02).** Fórmula fechada; conferi o piso 7 e o teto 25 pela própria fórmula; coluna de VEL de inimigo publicada e calibrada por uma regra de projeto declarada. Só a frase "disputa a primeira casa com o Boss" exagera para baixo (achado 26).
- **Crítico (L03).** Faixa, o que dobra, o que não dobra, interação com Tenacidade e Dano Contínuo, teto do jogo em 19-20 com fonte única nomeada e "expandir a faixa" entre os efeitos proibidos. Fechado, e sem corrimão de escada inexistente.
- **Vantagem/Desvantagem (L05).** Quatro linhas, sem acúmulo, cancelamento por presença, 20 natural em qualquer dos dois dados. Fechado.
- **RD (L06).** Por instância, teto `2 + 2×Eficiência` (conferi: 6/8/10/12/14/16/18, idêntico à coluna de 17), mínimo 1 de dano, Dano Contínuo ignora, RD inimiga publicada e subtraída de cada instância nas contas de 18.2 — agora inclusive do Dano de Quebra.
- **Teste de Ataque (L04).** A tabela de Atributo de Ataque tem as seis categorias de 9.2, com a **Média** presente e marcada como arma de referência. Duas sobras: a fórmula publicada em 4.1 e 4.5 não soma a Especialização de Combate nem o Cone de Luz, que o orçamento de 18.2 soma (achado 7); e o caminho alternativo que 4.5 cria — Habilidade resolvida por **Teste de Resistência do alvo** — nunca diz o que acontece quando o alvo **passa**, nem o inimigo tem bônus de Teste de Resistência na ficha (achado 2). Esse é o achado mais sério do documento, porque é exatamente o defeito que a v1.0 existe para matar.
- **Economia de ações (L18).** "Habilidade ocupa o espaço do Ataque Básico" resolve o buraco silencioso da v0.1 e os PH resolvem a frequência. Mas a **Ação Extra** é termo oficial em 3.2, é a tradução normalizada de *Ritmo Acelerado* em 7.9 e é efeito permitido de Nível 5+ em 10.4 — e não é definida em 8.1 nem tem teto por Ciclo, ao contrário do Avanço Total (achado 5).

### (c) Cada ponto de decisão explícito foi decidido com fundamento? **Sim, os sete.**

Esquiva, dados de vida, compra de pontos, mitigação da regra de Tenacidade, aumentos de atributo por nível, Energia por sofrer dano e por derrotar. Cada um vem com o porquê e, nos casos difíceis, com a alternativa recusada.

Contas que verifiquei e que fecham:

- **Compra de Pontos:** o array oficial custa `10+7+5+4+2+0 = 28`. Os dois métodos nascem equivalentes, e "dois 15 custam 20 dos 28" também está certo.
- **Aumento de Vigor = nível + 2 PV.** Derivei de 6.1 (o Vigor entra 3 vezes no nível 1 e 1 vez por nível seguinte, logo `3 + (L−1) = L+2`) e simulei dois personagens subindo Vigor em níveis diferentes: chegam ao mesmo PV no nível 20.
- **PV:** recalculei as **45 células** de 6.1. Todas batem. A razão Destruição/Caça no nível 20 é 308/212 = **1,45:1**, e a diferença absoluta vai de 20 para 96 PV.
- **Esquiva:** `+13` contra Defesa 30 pede 17 ou mais, **20%**; e `(0,60+0,60+0,20)/3 = 47%` de acerto médio.
- **Energia:** as três fontes novas com limite de 1 por Ciclo dão 25-35 por turno, ou uma Ultimate a cada 3-4 turnos por personagem — a premissa de ~1 Ultimate por Ciclo no grupo.

Sobrou um conflito **dentro** da decisão de Energia: 4.5 e 22.1 dizem que a Energia é da ação (fiel à v0.1), e a tabela "fechada" de 8.3, que é a camada dona, diz "Ataque Básico **que acerta**" (achado 6).

### (d) A tabela de Bônus de Atributo não-monotônica foi corrigida? **Sim.**

Sequência nova de 8 a 20: `-1, -1, 0, 0, +1, +1, +2, +3, +3, +4, +4, +5, +5`. Monotônica não-decrescente, preserva todos os marcos do autor (8 = -1, 10 = +0, 12 = +1, 14 = +2, 15 = +3), corrige só o 13 e cobre a faixa que Raças e aumentos por nível produzem. O array oficial dá `+3, +2, +1, +1, +0, -1`, soma **+6**, e a justificativa amarra corretamente o "+1 a cada 2 pontos" aos aumentos em +2 de 5.3. **E02 está morto e a tabela sobrevive ao `checar-tabelas.ps1`.**

### (e) A abordagem de balanceamento faz o combate durar 3-5 rodadas? **O método está certo, o DPC agora é reproduzível, e dois buracos de modelo derrubam a conclusão.**

O que melhorou de verdade, e vale registrar porque era o maior risco do projeto: **o DPC publicado agora reproduz**. Recalculei parcela por parcela, do zero, nas cinco faixas:

| Faixa | 2 ABs | Habilidade | Ultimate | Crítico | Quebra | **Meu total** | **Publicado** | Δ |
|---|---|---|---|---|---|---|---|---|
| 1-4 | 19,2 | 25,8 | 25,8 | 3,3 | 13,5 | **87,6** | 88 | 0,5% |
| 5-8 | 28,2 | 33,3 | 35,4 | 4,9 | 17,5 | **119,3** | 119 | 0,3% |
| 9-12 | 33,6 | 54,0 | 54,0 | 8,0 | 19,0 | **168,6** | 168 | 0,4% |
| 13-16 | 42,6 | 61,8 | 80,4 | 11,6 | 21,0 | **217,4** | 218 | 0,3% |
| 17-20 | 49,8 | 74,9 | 106,2 | 15,3 | 24,5 | **270,7** | 271 | 0,1% |

Também fecham: o orçamento `DPC × 4` repartido em 1/7, 1/3 e 85% reproduz as **15 células de PV de inimigo** a menos de 2,9% (a maior divergência é o Comum da faixa 5-8, 70 contra 68 — não o Elite da faixa 1-4 que o texto nomeia); a janela de acerto do grupo dá **exatamente** 70/60/55% nas cinco faixas; a janela do inimigo dá **exatamente** 60/70/55% contra Defesa de referência, Leve e Pesada nas cinco faixas, e as 15 células de Defesa do PC reproduzem pela build declarada; e a tabela de attrition dá 81/76/76/75/73%, com a janela de 51-64% no terceiro combate fechando quando se usa a cura de Descanso Curto da faixa certa.

Os dois buracos são de **modelo**, não de aritmética:

1. **A Redução de Tenacidade não é condicionada ao acerto** (achado 1). O documento aplica a taxa de acerto à geração de PH e diz isso com todas as letras, mas a derivação de Tenacidade soma `1 + 1 + Nível + 5` como se as quatro ações agressivas sempre acertassem, quando 4.5 diz que o ataque que erra não reduz Tenacidade. Com a taxa de acerto do perfil, a Quebra contra Boss sai a cada **~3,6 Ciclos**, não a cada 2; a parcela de Quebra cai ~45% e o DPC da faixa 1-4 sai da tolerância de 5% que o próprio `simular-combate.ps1` usa para reprovar.
2. **Não existe orçamento de dano recebido** (achado 3). O encontro é dimensionado só por PV, e "Dano por acerto" é **uma coluna única** para Comum, Elite e Boss. Das quatro composições que 18.3 chama de típicas, a janela de attrition publicada (73-81%) só vale para `1 Boss + 1 Comum`. O encontro de `7 Comuns` entrega ~182 por Ciclo na faixa 17-20 e deixa o grupo entre **45% e 63%** dos PV.

Há um terceiro vazamento, pequeno em escrita e grande em efeito: **as Ressonâncias estão fora do modelo** (achado 4). A Ressonância I entrega, a partir do nível 5, "1 uso de Habilidade por combate sem custo de PH" — em uma mesa de 4, até +1 Habilidade por Ciclo, +48% de DPC na faixa alta e combate em 2,6 Ciclos. A economia de PH é, pelas palavras do documento, "a espinha do balanceamento"; é a única coisa que não pode ter porta de serviço.

### (f) Os 22 itens de lacuna e os erros concretos estão mapeados a capítulos? **Sim, e com folga.**

20.1 mapeia L01 a L22 com decisão e capítulo de destino; 20.2 mapeia 31 erros concretos; 21.1 fecha os 16 pontos pedidos com ponteiro de seção; 19 atribui **uma** camada dona a cada invariante; 20 lista os 31 arquivos com conteúdo por arquivo; 20.3 mapeia as 17 imagens e declara as lacunas de arte. Nada relevante ficou sem endereço. Dois ajustes de completude estão nos achados 21 e 25.

### (g) Sobrou alguma referência cruzada quebrada? **Nenhuma de ponteiro. Quatro de subsistema.**

Extraí as 100 seções e **todas** as referências `X.Y` do documento: nenhuma aponta para seção inexistente (o único falso positivo é "1.0", de `v1.0`). Todas as referências a capítulo caem em 00-30 e são coerentes com a lista de 20. A tabela de 7.9 cobre as construções herdadas que encontrei na v0.1, e as contagens de termo da fonte conferem ("derrub" 3, "distância" 15, "uma vez por descanso" 3, "ação comum" 6, "casa" 3).

O defeito central da v0.1 — regra que cita subsistema inexistente — **não voltou por herança, voltou por texto novo**, em quatro lugares criados nesta versão:

1. **Teste de Resistência do alvo:** caminho de resolução criado em 4.5, sem resultado definido para o sucesso do alvo e sem bônus correspondente na ficha de inimigo (achado 2, HIGH).
2. **Ação Extra:** termo oficial usado em três seções, definido em nenhuma (achado 5).
3. **Intervir contra Executado:** 15.1 manda usar uma Reação que, como está escrita em 8.1, não tem onde se aplicar (achado 13).
4. **Marcado:** condição do catálogo cujo efeito é "o que a fonte disser" (achado 14) — a definição vazia que 7.9 proíbe duas páginas antes.

---

## Achados

### HIGH

**1 — A Redução de Tenacidade do grupo é derivada sem a taxa de acerto, e isso quebra a cadência de Quebra publicada.**
*Onde:* 18.1 (premissas "Tenacidade, por tipo de inimigo" e "Cadência de Quebra"), 18.3 (tabela de derivação e coluna Tenacidade C/E/B), 18.2 (parcela "Quebra ÷ 2 Ciclos"), 4.5.
*Problema:* 4.5 diz que o ataque que erra "não causa dano e **não reduz Tenacidade**" (a v0.1 diz o mesmo: "para retirar Tenacidade é obrigatório que o alvo receba um ataque"). O documento aplica essa condição à geração de PH e a declara como premissa, mas a derivação de Tenacidade soma `1 + 1` (dois Ataques Básicos) `+ Nível da Habilidade + 5` (Ultimate) **a 100% de acerto**, chegando a 9 / 9,75 / 11 / 10,75 / 11,25 por Ciclo. Com a taxa de acerto do perfil (55% contra Boss), a redução real é 4,95 / 5,36 / 6,05 / 5,91 / 6,19, e um Boss de Tenacidade 18/20/22/22/24 sofre Quebra a cada **3,6 Ciclos**. Consequências: a premissa "1 Quebra a cada 2 Ciclos no perfil de Boss" é falsa; a parcela de Quebra (14/18/19/21/25) está ~45% alta e, refeita, o DPC cai para 82/111/160/209/260 — na faixa 1-4 isso é **6,9% abaixo do publicado**, acima do gate de 5% de `simular-combate.ps1`; e o perfil de Elite ("quase todo Ciclo") passa a ser 1 a cada 1,7 Ciclos.
*Correção (escolher uma e escrever):* **(a)** manter a cadência e republicar a Tenacidade como `multiplicador × redução × taxa de acerto do perfil` → **Boss 10/11/12/12/13, Elite 5/6/7/6/7, Comum 3/3/4/4/4**, preservando o DPC e as 15 células de PV; **(b)** manter a coluna de Tenacidade e republicar a cadência (~3,6 Ciclos contra Boss, ~1,7 contra Elite), a parcela de Quebra e o DPC (82/111/160/209/260), rederivando as 15 células de 18.3. A (a) é mais barata. Em qualquer caso, acrescentar à tabela de premissas: "a Redução de Tenacidade é condicionada ao acerto, igual à geração de PH (4.5)".

**2 — O caminho de resolução por Teste de Resistência do alvo não tem resultado definido, e o inimigo não tem bônus de Teste de Resistência.**
*Onde:* 4.5 ("Quando não há Teste de Ataque"), 4.2, 8.5, 10.2, 10.4 (linha Resolução), 9.4, 18.1, 18.3 (ficha padronizada e âncoras), 22.1.
*Problema:* o documento cria um segundo caminho de resolução — "Habilidades de área, de controle e de debuff podem exigir um Teste de Resistência do alvo contra a sua DT em vez de um Teste de Ataque; cada Habilidade declara qual dos dois usa" — e **nunca diz o que acontece quando o alvo passa**: dano nenhum, metade do dano, dano sem efeito secundário? Nem se o sucesso impede a Redução de Tenacidade (9.4) ou o ganho de Energia. A linha "Teste de Resistência" de 22.1 trata só do PC falhando no próprio teste. Pior: a ficha padronizada de 18.3 tem Defesa, RD, Teste de Ataque e "DT dos efeitos **dele**", e **não** tem bônus de Teste de Resistência — não existe número contra o qual rolar, apesar da afirmação de que "todos os campos da ficha têm coluna na tabela de âncoras". Toda Habilidade de área, controle e debuff do jogo, e qualquer Ultimate construída nesse caminho (permitido por 8.5), fica irresolvível na mesa, e o DPC não tem premissa para elas.
*Correção:* fechar em 4.5 e repetir na linha Resolução de 10.4: *"Alvo que passa no Teste de Resistência: Habilidade de dano causa **metade do dano** (arredonda para baixo, mínimo 1) e nenhum efeito secundário; Habilidade sem dano (controle, debuff) não produz efeito nenhum. A Redução de Tenacidade só acontece se houver dano. A Energia da ação é ganha normalmente (8.3)."* E publicar a coluna que falta em 18.3: **Teste de Resistência do inimigo = Eficiência da faixa −1 (Comum) / Eficiência (Elite) / Eficiência +1 (Boss)** → 1/2/3, 3/4/5, 4/5/6, 5/6/7, 7/8/9. Contra a DT de Habilidade do personagem de referência (`8 + 5 + Eficiência` = 15/17/18/19/21), o inimigo falha em **65% / 60% / 55%** em todas as faixas — a mesma janela do acerto do grupo — e o campo passa a existir na ficha.

**3 — O orçamento de encontro é só de PV, e "Dano por acerto" é uma coluna única para os três tipos de inimigo.**
*Onde:* 18.1 (premissas "Ações agressivas do inimigo", "Janelas-alvo do inimigo", "Attrition do grupo"), 18.3 (coluna "Dano por acerto", "Composição do encontro", tabela de attrition).
*Problema:* o encontro é dimensionado exclusivamente pelo PV do inimigo (`DPC × 4`, em 1/7, 1/3 e 85%), e o dano devolvido é um número único por faixa aplicado igualmente a Comum, Elite e Boss. Cruzando com "Comum 1 ataque por turno; Elite 1 + especial a cada 2 Ciclos; Boss 2 por turno", as quatro composições que 18.3 declara equivalentes entregam dano muito diferente. Na faixa 17-20 (dano 48, PV do grupo 996, uma Esquiva por Ciclo): `1 Boss + 1 Comum` = **67/Ciclo** (o único caso modelado); `3 Elites` ≈ 77; `1 Elite + 4 Comuns` ≈ 134; `7 Comuns` ≈ **182**. O encontro de 7 Comuns, que o texto diz resolver em 2-3 Ciclos, custa 364 a 546 PV e deixa o grupo entre **45% e 63%** — uma faixa inteira abaixo do publicado. Um Comum batendo igual a um Boss também contradiz o enquadramento do próprio documento ("um Comum existe para sofrer Quebra").
*Correção:* publicar "Dano por acerto" **por tipo** e reverificar a attrition por composição. Mantendo o Boss como está (é ele que calibra a Defesa do PC e as 4-7 pancadas até Morrendo): **Comum = 1/3, Elite = 2/3, Boss = 1** → faixa 1-4: 3/7/10; 5-8: 7/13/20; 9-12: 9/19/28; 13-16: 12/24/36; 17-20: 16/32/48. Com isso `1 Boss + 1 Comum` entrega ~61/Ciclo (a janela de 73-81% sobrevive) e `7 Comuns` entrega ~61/Ciclo em 2-3 Ciclos (~85% dos PV restantes). Acrescentar a premissa: "o orçamento de encontro é de PV; o dano recebido é verificado por composição, e as quatro composições de 18.3 ficam entre 55 e 70 por Ciclo na faixa de referência".

**4 — As Ressonâncias furam a economia de PH e de Energia e não estão nem nas premissas nem nas omissões declaradas.**
*Onde:* 16.5, 18.1 (premissas de PH e de Ultimate, lista de omissões), 8.2, 8.5, 17.
*Problema:* a Ressonância I, a partir do **nível 5**, concede "1 uso de Habilidade por combate sem custo de PH". Em uma mesa de 4 com combate de 4 Ciclos, são até 4 usos grátis, ou **+1 Habilidade por Ciclo**, sobre os 0,75 por Ciclo que a economia de PH sustenta. Na faixa 17-20 cada uso grátis de Nível 7 vale `219 × 0,60 = 131` de DPC: o DPC vai de 271 para ~400 (+48%) e o Boss de 935 PV cai em **2,6 Ciclos**, fora da janela de 3 a 5 que é o critério único do documento. A Ressonância IV baixa a Ultimate para 80 de Energia (+25% na maior parcela do DPC, ~+26). A Ressonância III ("uma Habilidade sua sobe 1 Nível de efeito") não diz se o custo em PH sobe junto — se não subir, é um Nível 6 pelo preço de um Nível 5. Nenhuma das quatro aparece nas premissas nem na lista de omissões, que nomeia Memoespírito, Esforço, Vantagem, acúmulos de Caminho e Efeitos Condicionais de Cone.
*Correção:* (i) limitar a Ressonância I a **"1 uso por combate de uma Habilidade de Nível 3 ou menor sem custo de PH"** (~37 de DPC no grupo, dentro da margem) ou trocá-la por **"+1 PH no início de cada combate"**, que já é a moeda de 8.2; (ii) na Ressonância III, escrever "sobe 1 Nível de efeito **e passa a custar o PH do Nível novo**"; (iii) acrescentar a Ressonância IV à lista de omissões com o número, ou embuti-la na faixa 17-20 do DPC.

### MEDIUM

**5 — "Ação Extra" é termo oficial, aparece em três seções e não é definida nem limitada em nenhuma.**
*Onde:* 3.2, 7.9 (conversão de *Ritmo Acelerado*), 8.1, 10.2 (Nível 5), 10.4.
*Problema:* 3.2 declara o termo oficial; 7.9 normaliza a "ação adicional limitada" para "Ação Extra: um Ataque Básico, uma Habilidade de Nível 2 ou menor, ou uma Ação de Movimento"; 10.4 proíbe "ação extra fora de Ritmo Acelerado ou Nível 5+", o que **autoriza** Habilidades de Nível 5+ a concedê-la. E 8.1, seção dona da economia de ações, não a define. Falta o essencial: quantas por criatura por Ciclo (o Avanço Total tem teto de 1; esta não tem nenhum), se a Habilidade usada nela paga PH, se recarrega a Reação, se permite uma segunda Ultimate. Dois personagens da Harmonia, ou um deles mais uma Habilidade de Nível 5, entregam Ação Extra todo Ciclo ao mesmo PJ: +25% de turnos em uma mesa de 4, fora de todas as premissas de 18.1.
*Correção:* acrescentar à tabela de 8.1: *"**Ação Extra:** concedida por Bênção, por Habilidade de Nível 5 ou maior, ou por Ultimate. Permite **um** Ataque Básico, **ou** uma Habilidade de Nível 2 ou menor (pagando o PH normalmente), **ou** uma Ação de Movimento. Não concede Reação nem Ação Complementar e não permite uma segunda Ultimate no Ciclo. **Máximo de 1 Ação Extra por criatura por Ciclo, somando todas as fontes.**"* Registrar o invariante em 19 com dono no capítulo 19, ao lado do Avanço Total.

**6 — A tabela de Energia diz "Ataque Básico que acerta"; 4.5 e 22.1 dizem que a Energia é da ação.**
*Onde:* 8.3 (tabela de fontes), 4.5, 22.1.
*Problema:* 4.5 é explícita — "a **Energia da ação é ganha normalmente**: a v0.1 concede Energia pela ação e não pelo acerto, e isso fica" — e 22.1 repete. A tabela "fechada" de 8.3, apontada pelo quadro de invariantes como camada dona, diz "Ataque Básico **que acerta** | +20". A diferença é 8 de Energia por turno a 60% de acerto, ou seja uma Ultimate a cada 3,3 turnos contra uma a cada 4,2 — e a Ultimate é a maior parcela isolada do DPC (106 de 271 na faixa 17-20).
*Correção:* em 8.3, trocar a linha por "**Ataque Básico (acerte ou não)** | +20 | nenhum limite, salvo o **1 natural** (4.5)", espelhando a linha de Habilidade, que já diz "(acerte ou não)".

**7 — A fórmula publicada do Teste de Ataque não soma a Especialização de Combate.**
*Onde:* 4.1, 4.5, 4.3, 18.2, descrição do capítulo 18 em 20.
*Problema:* 4.1 publica a "rolagem única" e 4.5 publica `Teste de Ataque = d20 + Bônus do Atributo de Ataque + Eficiência ≥ Defesa do alvo`. A Especialização de Combate (+1/+2/+3 permanente em **todos** os Testes de Ataque) e o Bônus Maior de Cone de Luz não aparecem em nenhuma das duas — e juntos são **6 dos 19 pontos** do atacante de referência de 18.2. O capítulo 18 será escrito a partir de 4.5 e publicaria uma fórmula que não produz o número do orçamento.
*Correção:* 4.5 → *"**Teste de Ataque = d20 + Bônus do Atributo de Ataque + Eficiência + Especialização de Combate + bônus permanentes de equipamento (Cone de Luz, Relíquia) ± bônus e penalidades temporários dentro dos tetos de 9.6 ≥ Defesa do alvo**"*; e em 4.1 acrescentar "mais a Especialização de Combate, quando a rolagem for um Teste de Ataque".

**8 — Os alvos de buff/debuff de Nível 5-7 ("grupo") e a passiva de Nível 7 contradizem o teto de alvos.**
*Onde:* 10.2 (coluna Alvos e tabela de passivas), 10.1, 10.4.
*Problema:* 10.2 dá "grupo" como contagem de alvos para buff **e debuff** nos Níveis 5, 6 e 7, enquanto 10.1 e 10.4 travam a área em 3 alvos (4 nos Níveis 6-7, teto absoluto 6). "Grupo" não é definido: lido como grupo inimigo, um debuff de Nível 7 aplica **-5** — o teto inteiro de penalidade da faixa — a todos os inimigos da cena, que no encontro de 7 Comuns são 7 alvos, acima do teto absoluto declarado. Segundo conflito: o exemplo de passiva de Nível 7 é "sua Habilidade em área atinge 1 alvo adicional", enquanto 10.1 restringe alvos extras a recurso de Caminho ou texto de Bênção e 10.4 lista "atingir mais alvos em área do que 10.1 permite" entre os proibidos.
*Correção:* em 10.2, trocar "grupo" por *"todos os aliados (até 6), se for buff; se for debuff, os limites de área de 10.1 — 3 alvos, 4 nos Níveis 6 e 7"*; e, na passiva de Nível 7, trocar o exemplo ou acrescentar "passiva de Nível 7" às exceções de 10.1, mantendo o teto absoluto de 6.

**9 — Bônus em dados não têm teto, e a condição Quebrado está fora do DPC e fora das omissões.**
*Onde:* 9.6 (os dois tetos e a tabela de escopo), 9.2, 9.3, 9.4, 10.2, 11.2, 11.4, 18.1 (omissões), 18.2.
*Problema:* o documento fecha os bônus numéricos em +3/+4/+5 e as penalidades em -3/-4/-5, mas **nada limita dados adicionais**, que são a outra moeda do sistema: Fraqueza +2 (9.3), Quebrado +1 (9.4), Vulnerável +1 (9.6), Marcação de Presa +1 (11.2), Acúmulos de Cálculo até +2 (11.2), Tabela do Riso +1 (11.2), duas linhas da régua de 11.4, Avatar Forma Manifestada +2 (11.4), gatilho de passiva de Nível 4 (10.2) e a capstone da Caça +1 no crítico (4.6). Uma Caça de nível 20 atacando alvo marcado, Quebrado e com Fraqueza rola **9d10** onde o DPC modela 7d10 (+29%); uma Habilidade de Nível 7 chega a 23d20 contra os 20d20 modelados. Além disso a condição **Quebrado** (+1 dado de qualquer fonte e -2 de Defesa) acontece em metade dos Ciclos pela cadência publicada e não aparece em nenhuma parcela de 18.2 nem na lista de omissões: é margem não declarada em cima de um teto que não existe.
*Correção:* acrescentar o terceiro teto a 9.6, com dono no capítulo 26: *"**Teto de dados adicionais:** uma mesma rolagem não ganha mais de **+3 dados base** de fontes temporárias, **sem contar os +2 da Fraqueza** (9.3). Os dados base ganhos por nível (9.2) e os dados da tabela da Habilidade não entram nesse teto."* E acrescentar Quebrado à lista de omissões de 18.1 com o número, ou embuti-lo nas parcelas.

**10 — As faixas de PH (1-9 / 10-15 / 16-20) não coincidem com as cinco faixas de balanceamento, e o nível 9 não sustenta a premissa da faixa dele.**
*Onde:* 8.2 (fórmula de máximo, geração e a tabela "Quanto isso sustenta de verdade"), 18.1 (premissa "Nível da Habilidade por Ciclo"), 17.
*Problema:* o máximo de PH sobe nos níveis 10 e 16 e a geração sobe no nível 10, enquanto as faixas de balanceamento quebram em 9, 13 e 17. No **nível 9** — primeiro nível da faixa 9-12 — o grupo ainda tem máximo 5, início 3 e +1 por acerto, ou seja **7,8 PH por combate**, mas a premissa da faixa pede 4 Habilidades de Nível 4 (**12 PH**) e a tabela de 8.2 publica 13,6 PH para "faixa 9-12". No nível 9 o grupo sustenta ~2,6 usos, logo o DPC e a cadência de Quebra da faixa não valem no primeiro nível dela.
*Correção:* mover os degraus para as fronteiras de faixa, sem mexer em nenhum número publicado (os níveis de referência são 3/7/11/15/19): *"Máximo de PH = 1 + número de PJs, **+1 na faixa 9-16**, **+2 na faixa 17-20**"* e *"geração: **+1 nas faixas 1-8**, **+2 nas faixas 9-20**"*. Conferi: com isso, as linhas de 8.2 (7,8 / 7,8 / 13,6 / 13,6 / 14,6) e a linha de recursos de 17 passam a ser verdadeiras em **todos** os níveis de cada faixa, e as setas de transição saem da tabela.

**11 — O nível 2 sobe vazio, contra a afirmação feita em dois lugares e contra o próprio `checar-tabelas.ps1`.**
*Onde:* 17 ("Nenhum nível sobe vazio" e a tabela mestra), 5.3, 10.3, 23.
*Problema:* na tabela mestra o nível 2 repete **todas** as colunas do nível 1: Eficiência +2, 1 Bênção, 1 Habilidade conhecida, Nível máximo 1, sem aumento de Atributo, 1 dado de Ataque Básico, sem Especialização, teto de RD 6. A única entrega é PV. A afirmação "nenhum dos 20 níveis suba vazio" aparece em 5.3 e no cabeçalho de 17, e 23 especifica que `checar-tabelas.ps1` verifica exatamente isso — o gate do projeto reprovaria a própria tabela. O reespaçamento de 10.3 criou o buraco: na v0.1, "no Nível 2 você pode ter Habilidades Nível 2".
*Correção:* devolver o desbloqueio ao nível 2, que é DNA e é o remendo mais barato: **Nível máximo de Habilidade = 1 no nível 1, 2 no nível 2**, sem mexer em mais nada (o nível 3 continua com 2 Habilidades conhecidas e o primeiro aumento de Atributo). Atualizar as duas tabelas e definir no texto de 23 o que conta como "entrega" para o script.

**12 — Não está decidido se inimigo tem Reação e Esquiva, e a decisão move todo o DPC.**
*Onde:* 8.1, 6.3, 18.1 (janelas-alvo), 18.3 (ficha padronizada e âncoras).
*Problema:* 8.1 diz "**toda criatura** começa o combate com a Reação disponível" e, logo abaixo, "Reações padrão de todo **personagem**: Esquiva e Intervir". A ficha de inimigo de 18.3 não tem campo de Reação nem de Esquiva, e as janelas de acerto do grupo (70/60/55% nas cinco faixas) são calculadas contra Defesa crua. Se um Elite ou um Boss puder Esquivar, ele soma a Eficiência da faixa (+8 na 17-20) à Defesa uma vez por Ciclo, o acerto do grupo naquele ataque cai de 60% para 20% e o DPC cai cerca de um sexto — e o argumento que o documento usa contra Eficácia na Esquiva ("não é uma Reação boa, é imunidade a um ataque por turno") vale igual para o Boss.
*Correção:* decidir em 18.3 e repetir em 8.1: *"**Inimigos não têm Esquiva nem Intervir.** A Reação de um inimigo só existe se a ficha dele declarar uma, entre as 1 a 3 ações especiais, e ela nunca é um bônus de Defesa."* Isso preserva as janelas publicadas. Se a decisão for a oposta, a Esquiva do inimigo precisa de premissa em 18.1 e o DPC das cinco faixas precisa ser refeito.

**13 — Intervir contra Executado não tem regra: a Execução não é dano.**
*Onde:* 15.1, 8.1.
*Problema:* 15.1 diz que um aliado pode impedir a Execução "com a Reação **Intervir**". Intervir é definida em 8.1 como "você se joga na frente de um aliado a até Distância Curta e **recebe o dano** no lugar dele; só contra um ataque de alvo único" — e a Execução não é dano, é morte automática sem rolagem. A Reação citada não tem onde se aplicar. 8.1 também não diz se Intervir é declarada antes ou depois da rolagem, nem se o interventor usa a própria Defesa e a própria RD contra o ataque redirecionado.
*Correção:* escrever a Reação inteira em 8.1, incluindo o caso da Execução: *"**Intervir (Reação):** declare **antes da rolagem**, contra um ataque de alvo único dirigido a um aliado a até Distância Curta. O ataque passa a ter você como alvo e resolve contra a **sua** Defesa e a **sua** RD. Contra uma **Execução** (15.1), Intervir **cancela a Execução**: no lugar dela, o executor pode fazer o Ataque Básico dele contra você, resolvido normalmente."*

**14 — Duas entradas do catálogo de condições não fecham: Lentidão e Marcado.**
*Onde:* 9.6, 8.4, 15.4, 7.9.
*Problema:* (i) **Lentidão** é "-1 Distância por Ação de Movimento", e uma Ação de Movimento cobre exatamente **1** Distância (8.4) — a condição zera o movimento, e a ressalva entre parênteses ("sempre consegue mover ao menos até Pessoal/Curta gastando o turno") mistura contagem de passos com nomes de Distância e não diz qual ação paga isso. 15.4 usa a mesma condição para o personagem sobrecarregado, então a ambiguidade se propaga. (ii) **Marcado** tem como efeito "O que a fonte disser" — condição catalogada sem conteúdo mecânico, exatamente a construção que 7.9 proíbe duas páginas antes, e é o destino de *Marca do Vazio* na régua de 11.4.
*Correção:* (i) *"**Lentidão:** a sua Ação de Movimento não muda a sua Distância. Para mover 1 passo você precisa gastar **Esforço Total** (8.1). Não acumula."* (ii) dar piso mecânico a Marcado: *"**Marcado:** quem aplicou a marca ganha **+1 em Testes de Ataque** contra o alvo; a fonte pode acrescentar um efeito, dentro do teto de bônus somado. Acumula até 3 vezes, e marcas de fontes diferentes não somam entre si."* Alternativa igualmente válida: apagar Marcado do catálogo e mandar as Bênçãos usarem **Vulnerável**, que já tem efeito fechado.

**15 — A régua de 11.4 não cobre os custos em porcentagem de PV do Caminho da Destruição.**
*Onde:* 11.4 (régua e regra geral de política), 7.9, descrição do capítulo 07 em 20.
*Problema:* 11.4 declara que a tabela cobre "**todas** as construções fora de escala que a v0.1 produz" e que "nenhum efeito do livro cura, concede PV ou causa dano em porcentagem do PV máximo", com o Sangramento como única exceção. O Caminho da Destruição é construído sobre porcentagem de PV máximo **como custo**, e nenhuma dessas construções tem linha: *Pacto da Ruína* (perder 5% do PV máximo por turno), *Sacrifício Desesperado* (perder até 25%, 1d6 por cada 10% perdido), *Cicatriz da Destruição* (1 Marca a cada 20% de PV perdido) e, acima de tudo, *Avatar da Destruição* ("sacrificar seus próprios PV, **o quanto quiser**, para aumentar o dado de dano; se o dano já for d20 você ganha +d20") — troca ilimitada de PV por dados. O catch-all ("cai na linha mais próxima") não resolve, porque não existe linha próxima. *Pacto da Ruína* ainda diz que o dano extra é igual ao "seu bônus de Eficiência **ou Eficácia**", e nada no documento decide se a Eficácia pode ser bônus de dano (4.3 só governa Testes).
*Correção:* três linhas novas na régua: *"custo em % do PV máximo (Pacto da Ruína, Sacrifício Desesperado, Cicatriz da Destruição) → **mantém-se como custo**, porque é a identidade do Caminho, convertido em **PV igual a 2 × nível** por ativação ou por acúmulo"*; *"sacrificar PV à vontade por dados (Avatar da Destruição) → gaste **PV igual a 5 × nível** para ganhar **+1 dado base**, no máximo **+2 dados por Ciclo**, dentro do teto de dados adicionais (achado 9)"*; *"dano adicional igual à Eficiência **ou Eficácia** → **sempre Eficiência**; a Eficácia não entra em dano, como não entra em Teste de Ataque (4.3)"*.

**16 — Não existe regra de aquisição de Cone de Luz e de Relíquia, e o orçamento depende de o grupo tê-los.**
*Onde:* 16.3, 16.4, 17.1, 18.2, 24.
*Problema:* o orçamento de 18.2 assume que cada PJ carrega o Nível de Cone e o Tier de Relíquia da faixa — são 3 dos 19 pontos de ataque e 2 dos 22 de Defesa na faixa 17-20, e as Relíquias Mãos e Esfera Planar entram em todas as parcelas de dano. 17.1 diz que um substituto entra "com o equipamento do tier da faixa". Mas nenhuma seção diz **como** um PJ adquire um Cone ou uma Relíquia, quem concede, nem com que ritmo; e a Sobreposição de 16.3 pressupõe Cones duplicados, isto é, uma economia de drop que 24 coloca fora de escopo. Sem a regra, cada capítulo inventa a sua e o balanceamento depende de uma suposição não escrita.
*Correção:* um parágrafo em 16.4, com ponteiro em 16.3 e no capítulo 27: *"**Aquisição.** Cones de Luz e Relíquias são **recompensas de marco**, concedidas pelo Mestre. Ao entrar em cada faixa de nível, cada personagem recebe o Tier de Relíquia da faixa nos slots que já possui e pode trocar o Cone de Luz pelo Nível que o nível dele permite. **Sobreposição** é recompensa narrativa, no máximo uma por faixa. Não existe compra de Relíquia nem economia de créditos (24)."*

### NIT

**17 — "As 17 premissas" são 18 linhas.**
*Onde:* 18.1 (cabeçalho e o parágrafo "Dezesseis são consequência das regras"), 18.5, 21.1 (ponto 16), 23.
*Problema:* contei as linhas da tabela: são **18** (a 18ª é "Testes de Resistência contra efeitos do inimigo"). O texto diz 17 em quatro lugares e descreve a Fraqueza como "a décima sétima", quando ela é a sétima linha.
*Correção:* trocar por "as 18 premissas" nos quatro lugares e reescrever: "**dezessete** são consequência das regras e qualquer leitor as recalcula; a da **Fraqueza** é a única que depende de uma escolha do Mestre".

**18 — O "~83 por Ciclo" do perfil de Boss na faixa 1-4 não reproduz.**
*Onde:* 18.3 ("Ciclos até a resolução").
*Problema:* refazendo a conta do perfil de Boss na faixa 1-4 (acerto 55%, RD 4, Quebra a cada 2 Ciclos) eu chego a **~76** por Ciclo, não 83 — o que dá **4,0 Ciclos** contra os 305 PV do Boss, e não 3,7. O número da faixa 17-20 (~246 contra 935, 3,8 Ciclos) reproduz a 2%. Os dois ficam dentro da janela de 3 a 5, então é precisão, não conclusão.
*Correção:* publicar 76 e 4,0 Ciclos, ou abrir a conta do perfil de Boss no apêndice 29 junto com as outras quatro faixas, como já está previsto.

**19 — "Já incluindo o efeito do suporte" não é verdade na premissa de taxa de acerto.**
*Onde:* 18.1 (linha "Taxa de acerto usada no cálculo"), 18.2.
*Problema:* as taxas de 70/60/55% saem **exatamente** do bônus cru do ponto médio de 18.2 contra as Defesas de 18.3 (conferi as 15 combinações). Nenhum buff de aliado entra na conta, e um buff dentro do teto (+3 a +5) mudaria o acerto em 15 a 25 pontos percentuais.
*Correção:* apagar "já incluindo o efeito do suporte" e, se a intenção era dizer que um dos quatro turnos é do suporte, dizer isso: "o turno de suporte está contado no mix de ações, e o buff dele é margem declarada em 'o que as premissas deixam de fora'".

**20 — "Cerca de 30%" dos dois Descansos Curtos só vale na faixa alta.**
*Onde:* 18.3 ("o dia, não o combate"), 15.2.
*Problema:* pela fórmula `2 × nível + Bônus de Vigor`, dois Descansos Curtos devolvem **22%** do PV do grupo na faixa 1-4 e **32%** na 17-20. A janela publicada de 51-64% no terceiro combate está certa justamente porque as duas pontas usam valores diferentes; é a frase intermediária que arredonda demais.
*Correção:* trocar por "os dois Descansos Curtos devolvem de **22% (faixa 1-4) a 32% (faixa 17-20)** do PV do grupo".

**21 — E06 corrige só as médias de dano; as de cura da v0.1 também estavam erradas.**
*Onde:* 20.2 (linha E06), 10.1.
*Problema:* E06 cita "18/25/36/60/100 → 21/27/39/63/105", que é a tabela de dano. A tabela de **cura** da v0.1 (20/30/48/70) tem o mesmo defeito e 10.1 já publica os valores certos (22/33/52/73), mas o erro não está no mapa de erros, que é o checklist que a escrita vai usar.
*Correção:* acrescentar à célula: "e as médias de cura **20/30/48/70 → 22/33/52/73**".

**22 — A Ultimate não fica "um Nível equivalente abaixo" da melhor Habilidade na maior parte dos níveis.**
*Onde:* 8.5 (justificativa), 10.3, 17.
*Problema:* cruzando o Nível equivalente por faixa com o Nível máximo de Habilidade por nível, a Ultimate **empata** com o topo nos níveis 9, 10, 11, 13, 14 e 17, fica **acima** nos níveis 5 a 8 (equivalente 3 contra Nível máximo 2 no nível 5) e só fica abaixo nos níveis 12, 15, 16, 18, 19 e 20. A justificativa escrita descreve 6 dos 20 níveis.
*Correção:* manter a tabela (é boa e simples) e corrigir a justificativa: a Ultimate empata com o topo em metade dos níveis **de propósito**, e o PH continua valendo porque a Ultimate sai 1 vez a cada 3-4 turnos e a Habilidade sai todo turno — a limitação dela é Energia, não PH.

**23 — O gate de 15-25% do Memoespírito não define "dano do dono".**
*Onde:* 13.1, 23.
*Problema:* `simular-combate.ps1` deve reprovar se o Memoespírito sair da janela de "15% a 25% do dano do dono", e o documento não diz o que é o dano do dono — o DPC do grupo dividido por 4, a parcela do turno dele, ou o dano de uma Habilidade de topo. As três leituras dão 19%, ~50% e ~10% para o mesmo Memoespírito de faixa 17-20 (recalculei os `+18` de ataque e os `5d6+5 ≈ 22` de dano: batem com as fórmulas de 13.1).
*Correção:* definir em 13.1: "dano do dono = **DPC de referência da faixa ÷ 4** (o dano médio de um personagem por Ciclo). Na faixa 17-20 isso é 68, e os ~13 do Memoespírito depois de RD e taxa de acerto são **19%**".

**24 — "Distância de Movimento" é usada como termo oficial e não está na nomenclatura.**
*Onde:* 7.9 (cinco conversões), 3.2, 8.4.
*Problema:* cinco linhas da tabela de normalização mandam a escrita usar "+1 **Distância de Movimento**", termo que não aparece em 3.2 nem é definido em 8.4 (que fala de "passos" na escala). A escrita vai inferir certo, mas o glossário ficará sem a entrada.
*Correção:* acrescentar a 3.2 e ao glossário: "**Distância de Movimento** — quantos passos da escala de 8.4 uma Ação de Movimento cobre. Base 1; Esforço Total dobra; o máximo por turno, com todos os bônus, é 3."

**25 — 9.3 diz "regra da v0.1 mantida ao pé da letra" e descarta uma cláusula.**
*Onde:* 9.3, 21.2.
*Problema:* a v0.1 fecha a regra de Fraquezas com "a Redução e Aumento de dados com base em Fraquezas e Resistências **pode ser aumentada ou diminuída com base na força do causador de dano**". A v1.0 fixa ±2 dados e, corretamente, não implementa a cláusula — mas afirma manter a regra ao pé da letra e não registra o descarte em lugar nenhum.
*Correção:* trocar por "regra da v0.1 mantida, com os ±2 dados fixos" e acrescentar ao changelog 21.2: "a cláusula de variação por força do causador foi **aposentada**: dado extra sem teto era a porta aberta que o teto de dados adicionais (9.6) fecha".

**26 — "A Caça disputa a primeira casa com o Boss" não é disputa.**
*Onde:* 18.3 (parágrafo de VEL), 6.5.
*Problema:* com os números do próprio parágrafo, a Caça equipada da faixa 17-20 chega a VEL 24 (25 com Armadura Leve) contra VEL 19 do Boss: não é disputa, é vitória com 5 casas de folga. Uma Caça que não investe em Agilidade (+1) chega a 19 e aí sim empata.
*Correção:* trocar por "a Caça equipada **age antes de todo Comum, Elite e Boss da faixa dela**; uma Caça que não investe em Agilidade empata com o Boss e decide o empate pelo Bônus de Agilidade (7.3)".

---

## Assunções verificadas

Tudo abaixo eu recalculei ou medi na fonte. Está correto no documento.

1. **Contagens da v0.1** (medidas por regex no extraído): "derrubar o turno" em **3** lugares, "distância" em **15**, "uma vez por descanso" em **3** Bênçãos (as três nomeadas corretamente), "ação comum" em **6** ocorrências, "casa" em **3**, RD em **9** (Armadura Pesada + 8 Bênçãos). As afirmações de 1, 6.4, 7.9 e 15.2 batem.
2. **50 Bênçãos** nos 5 Caminhos escritos, 10 em cada (contadas uma a uma), e 4 Caminhos sem nenhuma. O volume de escrita de 11.3 (58 novas, 108 totais) está correto.
3. **Dados de vida da v0.1 → índice N:** 6/5/5/4/3/3/3/3/2, preservados na ordem exata, Caminho por Caminho.
4. **Curva de Eficiência:** níveis 1 a 8 idênticos à v0.1; só 9 e 10 mudam, e as duas mudanças estão no changelog.
5. **18 Perícias** com os atributos originais; as 3 Perícias de cada Caminho escrito conferem com a fonte, e as 12 dos Caminhos novos não repetem combinação proibida.
6. **Médias `floor`:** dano 21/27/39/63/105/147/189 e cura 22/33/52/73/105/147/189 — todas iguais a `floor(nº de dados × média do dado)`. A tabela da Ultimate (8.5) lê as mesmas linhas.
7. **Tabela de Bônus de Atributo:** monotônica não-decrescente de 8 a 20; array oficial `+3/+2/+1/+1/+0/-1`, soma +6.
8. **Compra de Pontos:** o array custa exatamente 28; "dois 15 custam 20 dos 28" confere.
9. **PV:** as 45 células de 6.1 batem com `25 + 5N + 3×Vigor` e `5 + N + Vigor`; razão 1,45:1 no nível 20; diferença de 20 PV no nível 1 e 96 no nível 20.
10. **Teto de RD:** 6/8/10/12/14/16/18 = `2 + 2×Eficiência`, idêntico à coluna de 17.
11. **Slots de Eficácia:** 5/8/11/14/17/20 coerentes entre 4.3 e a tabela mestra (1P/1TR → 5P/3TR).
12. **Habilidades conhecidas e Nível máximo:** 10.3 e 17 são idênticas nos 20 níveis.
13. **DPC:** reproduzi as cinco faixas parcela por parcela, com divergência máxima de 0,5% (tabela na seção (e) acima). A conta aberta da faixa 17-20 fecha em 270,7.
14. **Orçamento de PV de inimigo:** `DPC × 4` em 1/7, 1/3 e 85% reproduz as 15 células a ≤2,9%.
15. **Janela de acerto do grupo:** o ponto médio de 18.2 contra as Defesas de 18.3 dá exatamente 70/60/55% nas cinco faixas.
16. **Janela de acerto do inimigo:** o ataque de 18.3 contra as três colunas de Defesa de 18.2 dá exatamente 60/70/55% nas cinco faixas, e as 15 células de Defesa reproduzem pela build declarada (`10 + Agilidade típica + armadura + Tronco do tier`).
17. **Attrition:** 81/76/76/75/73% conferem com 1,4 acerto por Ciclo × dano × 4 Ciclos; as colunas "sem a Esquiva" (75/69/69/68/65%) também; e a janela de 51-64% no terceiro combate do dia fecha usando a cura de Descanso Curto da faixa certa.
18. **Firmeza:** os dois exemplos de 7.4 (7 casas → 2; 1 casa → 1) estão corretos pela ordem de operação publicada.
19. **Derivação de Tenacidade:** 9 / 9,75 / 11 / 10,75 / 11,25 confere com o mix de ações, e os três multiplicadores (0,5× / 1× / 2×) produzem as colunas publicadas depois do arredondamento — o que falta é a taxa de acerto (achado 1).
20. **Memoespírito:** `+18` de Teste de Ataque e `5d6 + 5 ≈ 22` de dano na faixa 17-20 batem com as fórmulas de 13.1, e a folga de 5-8% de DPC para um grupo com Recordação é consistente.
21. **Velocidade:** piso 7 e teto 25 batem com a fórmula e com a tabela de armaduras e Botas; a Caça equipada passa à frente de todo Comum e Elite em todas as faixas.
22. **Cadência de Bênçãos:** 10 Bênçãos nos níveis ímpares com tiers 6/4/2 fecha exatamente (4 sem requisito nos níveis 1-7, 4 do tier 9+ nos níveis 9-15, 2 do tier 17+ nos níveis 17 e 19), sobrando exatamente as 2 não adquiridas que 11.3 promete.
23. **Pontos do Memoespírito:** 12 na criação e +1 a cada 2 níveis dá 22 no nível 20, e as faixas de 17 (12-14 / 14-16 / 16-18 / 18-20 / 20-22) conferem.
24. **Ciclos contra Boss na faixa 17-20:** `935 ÷ 246 = 3,8`, dentro da janela.
25. **Referências internas:** extraí as 100 seções e todas as referências `X.Y`; nenhuma aponta para seção inexistente. Todas as referências a capítulo caem em 00-30 e são coerentes com a lista de 20. A Coluna A de 3.1 tem de fato 25 strings, e a válvula de exceção (`00-*`, `01-*`, `30-*`, `<!-- termo-historico -->`) é consistente entre 3.1, 22.2 e 23.

## Assunções não verificadas ou erradas

1. **ERRADA — "redução de Tenacidade do grupo por Ciclo = 9 / 9,75 / 11 / 10,75 / 11,25"** (18.3). A conta não aplica a taxa de acerto que a própria premissa de PH aplica, e a regra de 4.5 diz que ataque que erra não reduz Tenacidade. Achado 1.
2. **ERRADA como generalização — "o grupo termina um combate típico com 73% a 81% dos PV"** (18.3). Vale para `1 Boss + 1 Comum`; nas outras três composições publicadas o grupo termina entre 45% e 70%, porque "Dano por acerto" é um número único para os três tipos. Achado 3.
3. **ERRADA — "as 17 premissas"** (18.1, 18.5, 21.1, 23). São 18 linhas. Achado 17.
4. **NÃO REPRODUZ — "o grupo entrega ~83 por Ciclo na faixa 1-4 [perfil de Boss], o que dá 3,7 Ciclos"** (18.3). Meu recálculo dá ~76 e 4,0 Ciclos. Achado 18.
5. **ERRADA — "taxa de acerto ... já incluindo o efeito do suporte"** (18.1). As taxas saem do bônus cru contra a Defesa, sem buff nenhum. Achado 19.
6. **PARCIAL — "os dois Descansos Curtos do dia devolvem cerca de 30%"** (18.3). É 22% na faixa 1-4 e 32% na 17-20. Achado 20.
7. **ERRADA — "nenhum dos 20 níveis sobe vazio"** (5.3 e cabeçalho de 17). O nível 2 repete todas as colunas do nível 1. Achado 11.
8. **PARCIAL — "nas faixas altas a Ultimate fica um Nível equivalente abaixo da melhor Habilidade disponível"** (8.5). Verdadeira em 6 dos 20 níveis; nos níveis 5 a 8 a Ultimate está **acima** do Nível máximo de Habilidade. Achado 22.
9. **ERRADA — "a tabela cobre todas as construções fora de escala que a v0.1 produz"** (11.4). Não cobre os custos em % do PV máximo de quatro Bênçãos da Destruição, incluindo o sacrifício ilimitado do Avatar. Achado 15.
10. **PARCIAL — "regra da v0.1 mantida ao pé da letra"** (9.3). A cláusula de variação dos ±2 dados por força do causador foi descartada sem registro. Achado 25.
11. **PARCIAL — "a Caça ... disputa a primeira casa com o Boss"** (18.3). Com os números do próprio parágrafo, ela ganha com 5 casas de folga. Achado 26.
12. **NÃO VERIFICÁVEL — "todos os campos da ficha [de inimigo] têm coluna na tabela de âncoras"** (18.3). Falta a coluna de Teste de Resistência do inimigo, exigida pelo caminho de resolução que 4.5 cria. Achado 2.
13. **NÃO VERIFICÁVEL — gate do Memoespírito em "15% a 25% do dano do dono"** (13.1, 23). O denominador não é definido; as três leituras plausíveis dão 10%, 19% e 50%. Achado 23.
14. **NÃO VERIFICÁVEL — "o DPC de referência ... 5% de divergência"** como critério de reprovação (18.5, 23) **enquanto a janela de Ciclos for única**. O documento declara o critério "3 a 5 Ciclos" para toda faixa e, ao mesmo tempo, declara correto o encontro de 3+ inimigos resolver em 2-3 Ciclos; o script precisa de duas janelas, uma para o encontro de alvo único e outra para o de pelotão, senão reprova um caso que o próprio design aprova. Isso está coberto pela correção do achado 3 (verificação por composição).

---

## Conclusão

A iteração 3 fechou os três HIGH e os quatorze MEDIUM da iteração 2 com trabalho de verdade, e o ganho mais importante é de natureza diferente dos anteriores: **o balanceamento deixou de ser uma afirmação e passou a ser uma conta que um terceiro reproduz**. Eu refiz o DPC das cinco faixas do zero, mais o orçamento de PV, as duas janelas de acerto, as Defesas, a attrition com e sem Esquiva e a derivação de Tenacidade — e, com duas exceções nomeadas acima, tudo bate com três casas de precisão. A regra de alvos em área, que era a única regra em branco, está fechada e repetida nos cinco lugares que a consomem. As referências internas estão limpas: nenhum ponteiro quebrado em 2.036 linhas.

Os quatro HIGH desta rodada são de três tipos, e nenhum deles é "número errado":

- **um subsistema inteiro não escrito** (achado 2: o caminho de resolução por Teste de Resistência, criado por este documento, sem resultado de sucesso e sem o campo correspondente na ficha de inimigo) — é a reincidência do defeito que a v1.0 existe para corrigir, agora em texto novo;
- **duas premissas que não resistem às próprias regras do livro** (achado 1, Tenacidade sem taxa de acerto; achado 3, orçamento sem dano recebido);
- **uma porta de serviço na economia que sustenta o resto** (achado 4, Ressonância I).

Os doze MEDIUM são, na maioria, edições de uma a cinco linhas com o texto de substituição já escrito acima; três deles (5, 13, 14) são a mesma classe do achado 2 em escala menor — regra nomeada apontando para subsistema que não foi escrito.

Prioridade para a próxima iteração, se for preciso escolher: **achados 2, 1, 3 e 4**, nessa ordem. O 2 bloqueia os capítulos 16, 17 e 28 e não tem contorno na mesa; o 1 e o 3 decidem se as 15 células de 18.3 e a janela de attrition ficam de pé; o 4 é uma linha de texto que vale 48% de DPC. Os achados 5 a 16 podem entrar no mesmo passe sem risco, porque nenhum deles move número publicado — com a exceção do 10, que move dois degraus de faixa de PH e, pela conta que fiz, não altera nenhum valor de referência.
