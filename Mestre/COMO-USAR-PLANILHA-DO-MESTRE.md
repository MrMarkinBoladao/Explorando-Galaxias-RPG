# Como usar a Planilha do Mestre no Google Planilhas

Explorando Galáxias · livro **v1.2** · níveis 1 a 20

Nesta pasta:

| Arquivo | Para quê |
|---|---|
| `Planilha do Mestre - Explorando Galáxias V1.2.xlsx` | O modelo em branco. Faça uma cópia por campanha |
| `Planilha do Mestre - Exemplo.xlsx` | O mesmo modelo preenchido com a campanha "O Lacre do Poço Sete": grupo de 4 (a Nadir do capítulo 29.7 e mais 3), um combate montado, NPCs, missões e a sessão 2 preparada. Serve para ver a planilha em uso e para conferir a importação (seção 9) |
| `COMO-USAR-PLANILHA-DO-MESTRE.md` | Este guia |

O `Planilha do Mestre - Explorando Galáxias V1.1.xlsx`, se ainda estiver na pasta, é um registro antigo, de antes do livro v1.2. Use o V1.2.

A planilha não tem macro nem script: é só fórmula. Preencha as células **amarelas** e o resto se calcula sozinho. Nada nela substitui o livro: os números de regra vêm do livro v1.2, e o que a planilha inventa para preencher uma lacuna está rotulado como **Sugestão da planilha — não é regra do livro (H#)** (lista na seção 10).

---

## 1. Abrir no Google Planilhas

1. Envie o `.xlsx` para o seu Google Drive (arrastar para a janela do Drive funciona).
2. Clique com o botão direito no arquivo → **Abrir com** → **Planilhas Google**.
3. No Planilhas: **Arquivo** → **Salvar como Planilhas Google**. Use essa cópia nova. O `.xlsx` original continua no Drive como estava.
4. Abra a aba **Início** e confira **Células com erro na planilha**: `Início!B76` mostra **0** na planilha em branco. A linha de baixo mostra a contagem por aba.

Uma cópia por campanha: guarde o modelo em branco convertido e, para cada campanha nova, **Arquivo** → **Fazer uma cópia**.

### 1.1 Não comece um texto com +, - ou =

O Google entende como **fórmula** tudo que você digita começando com `+`, `-`, `=` ou `@`. Uma nota como `+2 contra a Legião` vira `#ERROR!` na hora. Se o texto precisar começar assim, digite um **apóstrofo** antes: `'+2 contra a Legião`. O apóstrofo não aparece na célula. A dica está no topo da aba **Início** (`Início!A13`).

A planilha se protege disso de dois jeitos:

- **Nenhuma opção de lista começa com esses sinais**, nem parece data ou número: as faixas aparecem como "Faixa 1-4", e a probabilidade do oráculo é "Meio a meio".
- **O erro não se espalha.** Se uma célula amarela ficar com `#ERROR!`, só ela fica assim: o resto calcula como se ela estivesse vazia, e o aviso da linha diz que o Google leu o texto como fórmula. Na aba **Início**, **Células com erro na planilha** conta as células com erro, aba por aba. Para consertar, apague a célula e escreva de novo com `'` na frente, ou escolha de novo na lista.

As abas **Tabelas** e **Dados** guardam as listas e as tabelas do livro que as fórmulas leem. Pode ocultar as duas (botão direito na aba → **Ocultar página**), mas **não apague**.

## 2. Como a planilha se organiza

- **Sem linhas congeladas, de propósito.** A parte que você usa de cada aba (colunas A a L) cabe numa tela comum sem rolar para o lado. Tabelas longas repetem o cabeçalho a cada 10 ou 12 linhas.
- As colunas à direita de L são **auxiliares e ficam ocultas**. Não precisa mexer nelas.
- Cada tabela tem um código (G1, C7, I3…) no título, e cada linha tem a coluna **Aviso** no fim. O aviso é texto: a cor nunca é o único sinal.

| Estilo | Como aparece |
|---|---|
| Entrada (preencha) | fundo amarelo-claro, borda dourada |
| Calculada (automático) | fundo azul-claro |
| Aviso | texto vermelho-escuro em negrito; fundo rosa quando há aviso |
| Título de bloco | faixa azul-escura, texto branco |
| Não se aplica | fundo cinza |

## 3. As abas, uma por uma

| Aba | O que tem | Quando usar |
|---|---|---|
| **Início** | Semente da campanha, painel (nível, faixa, DT, PH, missões, relógios quase cheios, próxima sessão), índice, avisos e erros por aba | Abra a sessão por aqui |
| **Campanha** | Mesa (nome, nº de jogadores, nível, sessão, dia; todas as abas leem daqui), marcos e ritmo (26.1, 26.7), 12 facções com reputação de −3 a +3, 10 relógios, linha do tempo, Ficha de Decisões da Mesa (27.11) e Sessão Zero | Entre sessões |
| **Grupo** | G1 a G6: quem é cada PJ e os números da ficha de cada jogador; G7 e G8: o **Memoespírito** de cada PJ (seção 7.1); resumo de Elementos, surpresa e Fraqueza | Na criação e a cada nível |
| **Sessões** | Preparação (cenas, pistas, ganchos, checklist) e diário | Antes e depois de cada sessão |
| **Missões** | Missões oferecidas, ativas e concluídas, com o aviso de mais de 3 Ativas | Entre sessões |
| **NPCs** | Gerador de NPCs, Elenco de 30, 4 cartões para imprimir e o bloco de combate pelas âncoras de 28.3 | Preparando a história |
| **Inimigos** | Criador de Inimigos nos 3 modos (Faixa do livro, Por nível, Ajustar do bestiário), Fraquezas sugeridas, ações pela régua de 28.4 e a ficha no formato de 28.1 | Preparando o combate |
| **Bestiário** | As 32 fichas do capítulo 28 com filtro e a ficha completa | Preparando o combate |
| **Encontros** | Orçamento (27.4), 3 encontros salvos (A, B e C), contrato da Fraqueza (27.5), DT para descobrir Fraqueza e o encontro aleatório | Preparando o combate |
| **Combate** | A Fila de Ação, PV, Tenacidade e Quebra, fases do Boss, Memoespíritos, condições com turnos, painel de consulta rápida, Morrendo e a calculadora de dano | Na mesa, durante a luta (seção 7) |
| **Aventuras** | Gerador de aventura com 5 cenas, antagonista e a linha de saída para Missões | Preparando a história |
| **Recompensas** | Entrega de marco (24.5, 25.1–25.3, 26.7), Sobreposições, preços, achados de encontro, Cone e Conjunto sorteados, Relíquias e o Tesouro do grupo | No fim do combate e no marco |
| **Mundos** | Planeta ou local, estação, nave, facção, organização e nomes avulsos por cultura | Improvisando o cenário |
| **Improviso** | Rumores, eventos de viagem, loja com estoque e preço, bugigangas, oráculo "Sim, e…", rolador de dados e DT rápida | Na mesa, quando o grupo sai do roteiro |
| **Escudo do Mestre** | 5 páginas A4 paisagem com as tabelas que o Mestre mais consulta (seção 8) | Imprima uma vez |
| **Minhas Tabelas** | 10 tabelas suas, com 100 vagas cada e sorteio de 1 a 5 sem repetir | Quando quiser uma tabela própria |
| **Tabelas** | As listas que os geradores usam (as do livro e as de sabor), editáveis | Para trocar nomes e opções |
| **Dados** | As tabelas do livro que as fórmulas leem | Não mexa |

## 4. Como funcionam as sementes

Os geradores **não sorteiam escondido**. Cada resultado vem de três números: a **Semente da campanha** (`Início!B16`), o número do gerador (G = 100, 200, 300…) e a **Rolagem nº** de cada gerador (a primeira célula amarela do gerador, por exemplo `NPCs!A7`).

- **Mesma semente e mesma Rolagem nº = mesmo resultado**, em qualquer computador e a qualquer hora. Duas pessoas com a mesma planilha veem o mesmo NPC.
- **Quer outro resultado? Some 1 na Rolagem nº.** Voltar o número traz o resultado anterior de volta.
- Vazia, a semente vale **12345** e a Rolagem nº vale **1**. Uma semente nova (de 1 a 2 147 483 646) dá à campanha uma sequência própria: no Exemplo ela é 2026.
- A planilha não usa sorteio que muda a cada edição: o resultado só muda quando você muda a semente, a Rolagem nº ou uma escolha do gerador (Raça, faixa, tipo).

## 5. Guardar um resultado gerado

O resultado de um gerador é uma fórmula: muda se a Rolagem nº mudar. Para guardar, copie a linha de saída e cole **só os valores** numa aba de registro:

1. Selecione a linha de saída e copie (**Ctrl+C**).
2. Clique na primeira célula da linha de destino e cole com **Ctrl+Shift+V** (colar só valores). Colar normal levaria a fórmula junto.

| Gerador | Copie | Cole só os valores em |
|---|---|---|
| NPC (G = 200) | `NPCs!A34:J34`, depois `B36:J36`, `B38:J38` e `B40:J40` (as 4 partes) | a mesma linha do Elenco: `NPCs!A46`, `B80`, `B114` e `B148` para o NPC 1 |
| Aventura (G = 300) | `Aventuras!A34:J34` | `Missões!A8` (a próxima linha livre) |
| Encontro aleatório (G = 100) | `Encontros!A108:G114` | o Encontro A, B ou C (`Encontros!A21`, por exemplo): as colunas estão na mesma ordem |
| Achados de encontro (G = 400) | `Recompensas!A95:J98` (as linhas de saída) | o Tesouro do grupo (`Recompensas!A133`, a próxima linha livre) |
| Mundos, Improviso, Minhas Tabelas | a célula do resultado | Campanha (linha do tempo ou Ficha de Decisões) ou Sessões (pistas e ganchos) |

No Exemplo, os 6 NPCs do Elenco são as Rolagens 1 a 6 do gerador coladas assim.

## 6. Preparar o combate

1. **Inimigos**: crie os inimigos próprios da campanha (uma linha por inimigo). Eles entram sozinhos nas listas de Encontros e Combate.
2. **Encontros**: monte o Encontro A com criaturas do bestiário ou suas. A linha de leitura diz o custo contra o orçamento (27.4), se é passagem, típico ou pesado, e se o **contrato da Fraqueza** (27.5: 3 Elementos do grupo como Fraqueza) está cumprido.
3. **Combate**, C0: escolha o encontro em **Carregar encontro**. Os inimigos entram em C3 com os números da ficha.

## 7. Conduzir um combate na Fila de Ação

A aba **Combate** não tem macro: todo estado é o que você digita. A Fila se monta sozinha pela VEL (19.3), com os desempates do livro.

**No começo:** em C0, Ciclo atual = 1, o encontro carregado e a Surpresa, se houver. Em C1, **Participa?** = Não para quem ficou de fora. Em C2b, **Invocado?** = Sim para cada Memoespírito em campo.

**A cada turno:**

1. A C9 (Fila do Ciclo atual) marca quem está **Agindo agora**.
2. Quando ele terminar, marque **Já agiu?** = Sim na linha dele, em C8. A marca passa para o próximo.
3. Dano: digite em **Dano agora** (C1 para PJ, C2b para Memoespírito, C4 para inimigo) e copie o **PV depois** para o **PV atual**.
4. Tenacidade: a calculadora (C10) dá a redução pela fonte e pelo Elemento; some em **Redução acumulada** (C5). Com a Tenacidade a 0, o inimigo fica **Quebrado**, e a C5b mostra o Dano de Quebra e o efeito do Elemento (20.4, 20.5).
5. Atrasar e Avançar: digite as casas em C8. A Firmeza e o teto (19.4) entram sozinhos; o excedente vira pendente.

No Exemplo, o combate está no meio do Ciclo 2: as casas 1 a 4 já estão com **Já agiu?** = Sim e a marca **Agindo agora** parou na casa 5, o Sargento de Trincheira.

**Avançar o Ciclo** (4 passos, escritos também em C0):

1. Some 1 em **Ciclo atual**.
2. Copie a coluna **Pendente para o Ciclo seguinte** (C8) e cole como valores em **Atraso pendente do Ciclo anterior**.
3. Apague **Atraso deste Ciclo**, **Avançar**, **Já agiu?**, **Avanço Total** e **Ultimate usada**.
4. Desconte 1 turno das condições de quem agiu (C7). Com 0, a condição expira e sai do painel.

**Virar a fase do Boss** (3 passos, em C4): (1) digite a fase nova em **Fase em vigor**; (2) apague a **Redução acumulada** dele em C5; (3) leia em voz alta as Fraquezas novas. A virada não gasta a ação dele (28.5).

**PJ a 0 PV:** a C2 mostra o Teste de Morrendo (23.4) e quem pode Executar (23.5). Digite sucessos e falhas.

### 7.1 Memoespírito: ligar ao PJ e invocar

O Memoespírito é do Caminho da Recordação (capítulo 11). Ele tem **casa própria na Fila**, pela VEL dele, e faz 1 ação por turno (11.5, 19.7).

1. **Ligar ao PJ** (aba **Grupo**, G7): na linha do PJ dono, **Tem? (Sim/Não)** = Sim, o nome dele e os números da ficha do jogador (PV máx., Defesa, VEL, RD e os pontos em Discernimento, Agilidade e Vigor). O que ficar vazio sai pela fórmula de 11.4 sem Bênção nem Bônus menor, e o aviso diz isso. A G8 mostra os números que o Combate usa.
2. **Invocar** (aba **Combate**, C2b): **Invocado?** = Sim. Ele aparece na Fila como "nome (de PJ)" e conta como combatente próprio, com PV e condições dele. Invocar custa a Ação Complementar do dono e 1 PH: desconte em **PH atual** (C0).
3. **Dispensar**: **Invocado?** = Não. Ele sai da Fila.
4. **A 0 PV ele some** (**Na Fila?** = Não: caiu) e só volta depois do próximo Descanso Curto (11.5).

Ele não tem Tenacidade, não fica Quebrado nem Congelado (20.1, 21.2). Se o dono cair a 0 PV, a planilha o mantém na Fila: o livro não diz o que acontece (Sugestão H27).

No Exemplo, KV-12 é da Recordação e o Memoespírito dela, o **Eco do Construtor**, está invocado com VEL 17: ele age na casa 2, antes da dona.

### 7.2 Condições com turnos e o painel de consulta rápida

- **Lançar** (C7): cada combatente tem **4 linhas** de condição, já com o nome dele na coluna A. Escolha a condição na lista (capítulo 21), digite os **Turnos restantes**, os **Acúmulos** e **Quem aplicou**. As 4 valem ao mesmo tempo: uma nunca sobrescreve a outra.
- **O dano** (Queimadura, Choque, Sangramento…) sai pela Eficiência de quem aplicou, na coluna **Efeito e dano**.
- **Descontar**: no fim do turno do alvo, tire 1 de **Turnos restantes**. Com **0**, a linha mostra **EXPIRADA** e a condição sai da conta (da Fila, do Congelado e do painel). Apague a linha quando quiser. Vazio = sem contador (dura o que a fonte disser).
- **O painel** (C9b, logo abaixo da Fila): todas as condições ativas do combate de uma vez, com **em quem**, **qual**, **quantos turnos faltam**, **quem aplicou** e **o que faz** (o efeito de 21.5, o número de agora e a duração do livro). A linha **Agora** resume quantas estão ativas e quantas expiraram.

No Exemplo, o Sargento de Trincheira tem Queimadura, Marcado e Vulnerável, a Nadir tem Lentidão e Marcado, e o Sangramento do Sargento já expirou.

## 8. Imprimir o Escudo do Mestre

A aba **Escudo do Mestre** tem **5 páginas A4 paisagem**, cada uma com uma linha "— página N de 5 —" no topo. Tudo nela vem da aba Dados.

1. Abra a aba **Escudo do Mestre**.
2. **Arquivo** → **Imprimir**.
3. Em **Imprimir**, escolha **Página atual**. **Tamanho do papel**: A4. **Orientação da página**: Paisagem. **Escala**: Ajustar à largura. **Margens**: Normais.
4. Em **Quebras de página personalizadas**, confira as 5 páginas: as linhas de corte já estão no lugar das linhas "— página N de 5 —".
5. **Próxima** → imprima ou salve em PDF.

Os 4 cartões de NPC (aba **NPCs**) imprimem do mesmo jeito.

## 9. Checklist de 2 minutos (com o Exemplo)

Importe `Planilha do Mestre - Exemplo.xlsx` como na seção 1 e confira estas células. Todos os valores foram confirmados pela bateria de testes (suítes `exemplo` e `guia`). Se uma delas mostrar outra coisa, a importação mudou alguma fórmula: refaça a importação antes de usar a planilha.

- [ ] `Início!B76` mostra **0** (nenhuma célula com erro).
- [ ] `Início!E16` mostra **2026** (a semente do Exemplo).
- [ ] `Campanha!B24` mostra **5** e `Campanha!B25` mostra **3** (PH máximo e de início, 16.2, 4 jogadores no nível 1).
- [ ] `Grupo!D73` mostra **23** e `Grupo!F73` mostra **17** (PV e VEL do Memoespírito de KV-12).
- [ ] `Encontros!B11` mostra **352** e `Encontros!B38` mostra **320** (orçamento e custo do Encontro A, 27.4).
- [ ] `Encontros!D38` mostra **91** e `Encontros!J41` mostra **Cumprido** (91% do orçamento; contrato da Fraqueza, 27.5).
- [ ] `Inimigos!C57` mostra **225** (PV do Carcereiro Orbital, Elite da faixa 9-12, 28.3).
- [ ] `Combate!J7` mostra **8** (combatentes na Fila, com o Memoespírito).
- [ ] `Combate!B141` mostra **Tessaly Varonne** e `Combate!B142` mostra **Eco do Construtor (de KV-12, Paciência)** (as 2 primeiras casas).
- [ ] `Combate!J36` mostra **Sim** (o Memoespírito está na Fila).
- [ ] `Combate!A175` mostra **Sargento de Trincheira** e `Combate!B175` mostra **Queimadura** (o painel de condições).
- [ ] `Combate!H238` mostra **EXPIRADA (0 turnos): já não vale; apague a condição** (o Sangramento com 0 turnos).
- [ ] `Campanha!D63` mostra **●●●○○○○○ 3/8** (o relógio "O lacre cede").

Na planilha em branco (o modelo V1.2):

- [ ] Na planilha em branco, `Início!B76` mostra **0** e `Início!E16` mostra **12345** (a semente padrão).
- [ ] Na planilha em branco, `Encontros!B11` mostra **88** (orçamento da faixa 1-4 para 4 jogadores, 27.4).
- [ ] Na planilha em branco, `NPCs!A34` mostra **Maelune Sonata Breve** (o gerador de NPCs funcionando na semente padrão).
- [ ] Na planilha em branco, `Combate!B171` mostra **Nenhuma condição ativa: lance as condições na C7, na linha de cada combatente.**

O que esta bateria **não** confere é o próprio Google: as fórmulas foram recalculadas com a biblioteca `formulas` 1.3.4, que não é o Google Planilhas, e ela não executa a validação de dados nem a formatação condicional. Por isso o checklist existe.

## 10. Sugestões da planilha (o que não é regra do livro)

Onde o livro não dá o número que a ferramenta precisa, a planilha usa uma heurística, sempre rotulada na célula como **Sugestão da planilha — não é regra do livro (H#)**. Na mesa, a palavra final é sua.

| H | Onde | O que a planilha faz |
|---|---|---|
| H1 | Inimigos | PV por nível dentro da faixa (o livro só dá a âncora da faixa); os outros números ficam iguais aos de 28.3 |
| H2 | Inimigos, Bestiário | Dano de ação especial 1,5× quando a ficha não diz |
| H3 | Inimigos | Reescala das ações ao ajustar uma criatura para outra faixa |
| H4 | Inimigos | Limiares de fase do Boss criado em partes iguais dos PV |
| H5 | Encontros | Orçamento proporcional para grupo diferente de 4 |
| H6 | Encontros | Rótulos de dificuldade (passagem, típico, pesado) pela fração do orçamento |
| H7 | Encontros | Ciclos estimados (custo ÷ DPC do grupo) |
| H8 | Tabelas, Encontros | Ambiente por facção para o filtro e o encontro aleatório |
| H9 | Recompensas | 0 a 2 consumíveis por encontro |
| H10 | Improviso | Oráculo "Sim, e…" / "Não, mas…" |
| H11 | NPCs, Recompensas | Pesos das tabelas de sabor |
| H12 | Inimigos | Fraquezas sugeridas com os Elementos do grupo que faltam no contrato |
| H13 | Combate | Ordem quando dois combatentes são movidos no mesmo Ciclo; empate PJ × inimigo |
| H14 | Aventuras | As 5 cenas da aventura e as DTs delas |
| H15 | Improviso | Estoque da loja por tipo (os preços são os de 24.1–24.3) |
| H16 | Campanha | Relógios com segmentos |
| H17 | Campanha | Reputação de −3 a +3 com rótulos |
| H18 | Recompensas | Créditos achados num encontro (até 15% da verba de marco) |
| H19 | Encontros | Troca de Fraqueza no encontro aleatório para cumprir o contrato |
| H20 | NPCs, Aventuras | Gancho do livro ou de sabor, meio a meio |
| H21 | (absorvida na H9) | — |
| H22 | Aventuras | Antagonista: Boss da facção na faixa, depois Elite da facção, depois Boss da faixa |
| H23 | Missões | Aviso com mais de 3 missões Ativas |
| H24 | Campanha | Tom, limites e véus, expectativas e combinados da Sessão Zero |
| H25 | NPCs, Improviso | Quantidades de saída sem repetir dentro de uma rolagem |
| H26 | Aventuras | Contratante de outra facção, local da faixa, "Faixa alta" |
| H27 | Grupo, Combate | Memoespírito: em empate total ele fica do lado dos jogadores, logo depois dos PJs; se o dono cai a 0 PV, ele continua na Fila |

## 11. Opcional: ligar a aba Grupo às fichas dos jogadores (IMPORTRANGE)

Se cada jogador usa a **Ficha Automatizada** no Google, a aba **Grupo** pode ler os números direto da ficha. Isto é só no Google; o `.xlsx` não traz nenhuma ligação.

1. Na ficha do jogador, copie o endereço da planilha (a parte entre `/d/` e `/edit` na barra do navegador).
2. Na aba **Grupo** do Mestre, numa célula amarela, digite por exemplo:
   ```
   =IMPORTRANGE("endereço-da-ficha";"'Criação'!D99")
   ```
3. Na primeira vez o Google pede **Permitir acesso**. Clique e pronto.

Endereços da ficha V1.2 (aba e célula):

| Campo do Grupo | Na ficha do jogador |
|---|---|
| Nome do PJ | `'Criação'!B6` |
| Raça · Caminho · Elemento | `'Criação'!B25` · `'Criação'!B33` · `'Criação'!B60` |
| Defesa · Esquiva · RD · VEL | `'Criação'!D96` · `'Criação'!D97` · `'Criação'!D98` · `'Criação'!D99` |
| Bônus de Agilidade · Discernimento · Presença | `'Criação'!F45` · `'Criação'!F48` · `'Criação'!F49` |
| DT das Habilidades | `'Criação'!B56` |
| Memoespírito: PV · Defesa · VEL · RD | `'Caminho'!B80` · `'Caminho'!B81` · `'Caminho'!B82` · `'Caminho'!B91` |

O PV máximo do PJ, digite à mão, pela aba Em Jogo da ficha do jogador. Se a importação falhar, a célula fica com erro, o resto da planilha continua calculando e o contador da Início acusa (seção 1.1).

## 12. O que a planilha não faz

- Não guarda histórico sozinha: o que você quer manter, cole como valores (seção 5) ou registre no diário (Sessões).
- Não move a Fila nem desconta turnos por conta própria: mudar o estado é sempre uma entrada sua.
- Não altera o livro: quando a planilha e o livro discordarem, vale o livro.
