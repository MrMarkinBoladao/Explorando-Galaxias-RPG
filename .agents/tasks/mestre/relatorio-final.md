# Relatório final: Planilha do Mestre (Explorando Galáxias, livro v1.2)

A bateria completa (`suite-tudo.txt`, `--suite tudo`, 09/10 04:08–12:28, 30 000 s) tem 18 suítes, 10 979 281 checagens e 0 falha. Ela rodou sobre as planilhas de 03:46 e o código de antes dessa hora, e nada foi editado em `build\` ou em `Mestre\` durante a bateria (a suíte `origem` deu 9/9 no começo e no fim). O pedido do usuário de Memoespírito e condições entrou nesta fase, e o critério de aceitação dele está em `notas-fase4.md` e abaixo. Este relatório faz o papel do `AUDITORIA.md` do plano 4.3.

## Entregáveis (`Mestre\`)

| Arquivo | O que é |
|---|---|
| `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx` | Modelo em branco: 18 abas, 41 810 fórmulas, 3 636 validações, 4 544 entradas (todas vazias), geradores funcionando na semente padrão 12345 |
| `Mestre\Planilha do Mestre - Exemplo.xlsx` | Campanha "O Lacre do Poço Sete", 519 entradas: Nadir (29.7), Tessaly Varonne (Vulpes, Caça), Shen Wanqing (Xianzhouíta, Preservação), KV-12 (Intellitron, Recordação, com o Memoespírito "Eco do Construtor"); Carcereiro Orbital e Capataz do Duto 4; Encontros A e B; combate no Ciclo 2 com o Memoespírito invocado e 8 condições (1 expirada); 6 NPCs, 4 cartões, 3 missões, sessão 2 preparada, diário, facções, relógios, linha do tempo, Sessão Zero, marco do nível 2, "Clima no Expresso" |
| `Mestre\COMO-USAR-PLANILHA-DO-MESTRE.md` | Guia em PT-BR: abrir no Google, tour pelas 18 abas, sementes, guardar resultado (Ctrl+Shift+V), Fila de Ação, Memoespírito, condições e painel, impressão do Escudo (5 páginas), checklist de 2 minutos (25 citações de célula conferidas pela suíte `guia`), H1–H27, IMPORTRANGE com os endereços de `ficha_mapa.json` |

Na pasta ficam também o `…V1.1.xlsx` de 05/10 (registro, por decisão do usuário; ele decide se apaga), o atalho `.gsheet` do usuário e o `desktop.ini` do Drive. A suíte `entregaveis` aceita esses três e recusa qualquer outro arquivo. O nome é V1.2 porque o usuário adotou o livro v1.2 ("Vamos continuar com a planilha da versão 1.2"); o "V1.1" do pedido da Fase 4 era texto anterior a essa decisão.

## Suítes (bateria final)

| Suíte | Checagens | Falhas | O que confirma |
|---|---:|---:|---|
| origem (início e fim) | 9 + 9 | 0 | os dois `.xlsx` são os do gerador, sem regravação no meio da bateria |
| entregaveis | 4 | 0 | os 3 nomes exatos; nada além do registro V1.1, `.gsheet` e `desktop.ini` |
| spike | 142 | 0 | padrões de fórmula × Python; maior intermediário 2,8e14 < 2^53 |
| protegidos | 165 | 0 | **livro intocado** (38 arquivos, SHA-256 de `ficha_protegidos.json`) e **ficha intocada** (50 arquivos de `baseline-hashes.json`); o único ausente é a "Cópia de Ficha…", já ausente antes da Fase 1 (P5) |
| dados | 1 574 | 0 | parser próprio × aba Dados, listas do livro, 24–27, Escudo × Dados (555 células) |
| bestiario | 34 | 0 | 32 fichas criatura por criatura, 116 ações iguais ao `.md` |
| ouro | 334 | 0 | números impressos no livro calculados na planilha; novos: o exemplo de 11.4 (PV 151, Defesa 21, VEL 15, RT 2, 5d6/6d6), 11.5/19.7 (casa própria pela VEL, Não = fora, 0 PV = some), H27 e Congelado no Memoespírito |
| oraculo | 1 135 830 | 0 | oráculo independente × planilha em 5 089 casos; **cobertura P10 1 966/1 966** números de regra; novos: 300 Filas com Memoespíritos, 120 estados de condições (12 com as 88 cheias, inclusive "Mais N" do painel), 150 de Memoespírito |
| determinismo | 298 956 | 0 | mesma semente = mesmo resultado; sementes diferentes variam; nenhuma saída vazia; toda entrada alcançável; u/y/x = oráculo em 29 geradores |
| extremos | 1 103 | 0 | 0 célula de erro nas 41 810 fórmulas em 14 estados (branco, Exemplo, grupo de 1 e de 6, 8 jogadores, nível 1 e 20, listas vazias e cheias, os 22 combatentes ocupados com as 88 condições, Elenco/Tesouro/campanha cheios), 200 sementes × 2 rolagens, erro injetado em 107 entradas uma a uma e todas juntas |
| lint | 232 391 | 0 | requisito do Google: 0 achado, 1 311 listas e 74 489 opções, 0 leitura direta de entrada, 12 657 células na camada protegida; Escudo A4 paisagem, 5 páginas ≤ 633 pt |
| texto | 9 195 537 | 0 | PT-BR, glossário 30.1, termos de 30.2, léxico, rótulos H1–H27, e as 186 linhas do COMO-USAR |
| preview | 1 336 | 0 | 1 332 recortes ≤ 1800 px, 18 abas × 3 estados, 0 texto cortado |
| visual | 53 025 | 0 | 48 808 textos medidos, 0 não couberam; contraste mínimo 4,96:1; A:L ≤ 1360 px |
| sabor | 10 855 | 0 | 70 tabelas de sabor, nomes ≥ 30 por cultura |
| exemplo | 47 852 | 0 | Exemplo = gerador (519 entradas), 4 PJs = `oraculo_ficha`, encontro A 320/352 (91%, típico, contrato com 3), Filas dos Ciclos 1 e 2 = oráculo, critério de aceitação do pedido, 0 erro nas 41 810 fórmulas, 16 geradores no branco = oráculo |
| guia | 125 | 0 | as 19 citações do Exemplo e as 6 do branco no COMO-USAR batem com a planilha calculada |
| **total** | **10 979 281** | **0** | |

Recortes olhados (tamanho conferido, ≤ 1800 px): `exemplo-combate-parte-01.png` (C2b com o Eco do Construtor invocado, nota H27), `exemplo-combate-parte-05.png` (Fila com o Memoespírito na casa 2, CONDIÇÕES apontando o painel), `exemplo-combate-parte-06.png` (painel C9b: 7 ativas, efeito e duração), `exemplo-grupo-parte-02.png` (G7/G8). Nada cortado.

## Pedido do usuário: Memoespírito e condições (M1–M4, C1–C6)

- **M1** Grupo G7 (Tem? Sim/Não, nome, PV, Defesa, VEL, RD, pontos em Discernimento, Agilidade e Vigor, da ficha 29.9) e G8 (números em uso; vazio = 11.4 sem Bênção, com aviso; dano do ataque; Redução de Tenacidade).
- **M2** Combate C2b: "Invocado? (Sim/Não)". Com Sim, o Memoespírito é o combatente 17–22, entra na Fila pela VEL dele, tem PV, Defesa e as próprias condições, e aparece como "nome (de PJ)". Com Não, sai da Fila.
- **M3** 11.5 e 19.7 escritos na aba: Ação Complementar + 1 PH; casa própria; 1 ação por turno; a 0 PV some até o Descanso Curto; sem Tenacidade, Quebra ou Congelado. O que o livro não diz virou a H27.
- **M4** 1 por PJ (6); a Fila passou de 16 para 22 combatentes.
- **C1/C4** 4 condições por combatente (88 linhas na C7), para PJs, inimigos e Memoespíritos, todas valendo juntas. **C2** lista do capítulo 21 + turnos digitados. **C3** painel C9b, logo abaixo da Fila: em quem, qual, turnos, acúmulos, quem aplicou, o que faz (21.5), o número de agora e a duração. **C5** a C7 antiga foi absorvida (mesmo dano, Congelado, Surpreso, Quebra, Morrendo e Fila; o `ouro` de 19.4, 20.4, 20.5, 21.2 e 23.4 passa igual). **C6** com 0 turnos a linha diz "EXPIRADA (0 turnos)…" e a condição sai do painel, do Congelado e do Surpreso.

Uma mudança visível que veio junto: a linha CONDIÇÕES (abaixo da Fila) agora mostra a contagem e os Quebrados e aponta o painel, em vez de listar cada condição, porque com 88 condições a lista não cabia na linha.

## Sugestões da planilha (fora do livro) e o erro máximo medido

| H | O quê | Validação e erro máximo |
|---|---|---|
| H1 | PV por nível dentro da faixa | erro 0 nos níveis de referência (3/7/11/15/19); desvio máximo do PV contra a âncora da própria faixa: Comum 14,3% (nível 5), Elite 14,7% (nível 9), Boss 14,7% (nível 9), teto 20% |
| H2 | Dano de especial 1,5× | média = INT(1,5 × âncora) nas 15 linhas; erro 0 |
| H3 | Reescala de ação | 0 diferença na faixa original (116 ações) |
| H4 | Limiares de fase | barras das 5 fichas com fases iguais ao livro; erro 0 |
| H5 | Grupo ≠ 4 | com 4 jogadores, igual a 27.4 nas 5 faixas; erro 0 |
| H6 | Rótulos de dificuldade | composições de 27.4/28.11 em "típico"; 0 fora |
| H7 | Ciclos estimados | Combate A de 29.5: 4,0 contra 3,7 publicado (diferença 0,3 Ciclo, L3) |
| H8 | Ambiente por facção | toda criatura com ambiente; 6 ambientes têm criatura numa faixa só (o livro dá uma faixa por facção) |
| H9 | 0–2 consumíveis | 34,0 / 32,5 / 33,5% em 3 000 rolagens (alvo 28–39%) |
| H10 | Oráculo sim/não | chance medida = a nominal (20/35/50/65/80%) |
| H11 | Pesos de sabor | contagem exata nas listas |
| H12 | Fraquezas sugeridas | nunca igual à Resistência; cobre os Elementos do grupo antes de repetir (300 × 3 grupos) |
| H13 | Ordem com vários movimentos | 300 estados + 4 empates fixos = oráculo |
| H14 | 5 cenas da aventura | orçamentos 50%/100%, DTs Média/Difícil; erro 0 |
| H15 | Loja | 300 lojas, todo preço igual a 24.1–24.3 |
| H16 | Relógios | 45 casos + inválidos |
| H17 | Reputação | 7 rótulos exatos |
| H18 | Créditos no encontro | erro de arredondamento 0 Cr; teto 15% da verba (informativo: 12 × 15% = 180% num nível) |
| H19 | Troca de Fraqueza no aleatório | 501 encontros × 3 grupos; contrato cumprido quando possível |
| H20 | Gancho do livro ou de sabor | 51,1% (NPC) e 48,3% (aventura) em 2 000 rolagens (alvo 45–55%) |
| H21 | (absorvida na H9) | — |
| H22 | Antagonista | 40 facção × faixa, nenhum vazio (degraus 4/5/31) |
| H23 | Mais de 3 Ativas | aviso com 4, nenhum com 3 |
| H24 | Sessão Zero | 3 itens sem seção do livro, rotulados; os demais citam a seção certa |
| H25 | Quantidades de saída | 0 repetição em 300 rolagens |
| H26 | Contratante, local, "Faixa alta" | contratante nunca da facção do conflito; local só na faixa do livro (400 casos) |
| H27 (nova) | Memoespírito: empate total do lado dos jogadores, logo após os PJs; mantido na Fila com o dono a 0 PV | `ouro` (empate total: a dona antes) e `oraculo` (150 estados + 300 Filas); erro 0 |

## Inconsistências e lacunas do livro (para o autor decidir; o livro não foi alterado)

| # | Capítulo e seção | Achado |
|---|---|---|
| L1 | 28.6–28.10 | 16 das 32 fichas não declaram Execução (Casco Oco, Larva, Esporo, Peão, Capataz, Sargento, Afogado, Fuzileiro, Devoto, Centurião, Auditora, Pretor, Palhaço, Dramaturgo, Vênia, Germe). A planilha mostra "Não declarado" e lembra 23.5 |
| L2 | 28.5 regra 3 × 28.3 | Tenacidade de fase abaixo da âncora: Dramaturgo f2 = 9, Germe f3 = 10, Vazia Coroada f2 = 12 e f3 = 10 (permitido por 28.5; registrado) |
| L3 | 29.5 × 27.4 | O Combate A publica 3,7 Ciclos; a conta de 27.4 com o contrato cumprido dá 4,0 |
| L4 | 28.3, 28.4 | Não há regra de inimigo por nível dentro da faixa (H1) |
| L5 | 27.4, 29.3 | Orçamento só para 4 PJs (H5) |
| L6 | 24.5, 26.1, 27.8 | Sem tesouro por encontro, só a progressão por marco (H9, H18) |
| L7 | 19.4–19.6 | Ordem com vários movimentos no mesmo Ciclo não definida (H13) |
| L8 | 06.3 | O livro não liga Caminho a Elemento (o NPC sorteia o Elemento à parte) |
| L9 | 27 | Sem Sessão Zero, limite de missões, relógio numerado ou escala de reputação (H16, H17, H23, H24) |
| L10 | 19.1 | A faixa esperada de VEL só é dada nos níveis 1, 10 e 20 |
| L11 | 28.4 regra 5 | Sem estimativa de dano especial para Comum e Boss 5-8 (H2) |
| L12 | 27.16 × 28 | Cada facção tem criaturas numa faixa só: 6 ambientes (Colônia ou mina, Estação, Cidade corporativa, Nave-cidade, Clínica ou ateliê, Mundo com Stellaron) só têm criatura numa faixa (H8) |
| L13 | 27.17 | Só Poço Sete (1-4), Hesperin (17-20) e Ferro-Vazio ("Faixa alta", sem número) têm faixa (H26) |
| L14 | 11.5 | Não diz o que acontece com o Memoespírito quando o dono cai a 0 PV (Morrendo) nem se ele continua agindo (H27) |
| L15 | 19.3 passo 2 × 11.5 | O desempate "os jogadores escolhem e vêm antes dos NPCs" não diz se o Memoespírito conta como jogador (H27) |
| L16 | 21.5 | A Corrupção ("+1 no dano de cada Dano Contínuo seu") não é Dano Contínuo, mas fica na mesma família; a tabela não diz quando ela "tica". A planilha a trata como efeito, sem dano próprio |
| L17 | 11.5 × 23.6 | "Só volta depois do próximo Descanso Curto" (11.5) e "reinvoca o Memoespírito que caiu" (23.6) concordam, mas nenhum dos dois diz se a reinvocação custa de novo a Ação Complementar e o PH |

## Limitação honesta

- O motor de recálculo é a biblioteca `formulas` 1.3.4, não o Google Planilhas. As fórmulas usam só 31 das 33 funções de `ficha_funcoes_ok.json` (sem ROUND e ROUNDUP, que a Mestre proíbe: arredondamento só com INT, D1) e passam no lint do Google, mas o comportamento no Google **não foi executado aqui**.
- A `formulas` não executa **validação de dados** (listas suspensas, limites de inteiro) nem **formatação condicional**: elas foram conferidas como estrutura (lint e visual), não em uso. A checklist de 2 minutos do COMO-USAR existe para o usuário conferir isso no Google.
- A impressão do Escudo foi conferida pela área de impressão, pelas quebras e pela altura das páginas (≤ 633 pt), não por uma impressão real.
- O IMPORTRANGE do COMO-USAR é só documentação: os endereços vêm de `ficha_mapa.json`, mas a ligação não foi testada no Google.

## O que ficou aberto

- O `…V1.1.xlsx` de 05/10 continua em `Mestre\` como registro: o usuário decide se apaga.
- A checklist de 2 minutos no Google Planilhas (validação, formatação condicional, impressão e IMPORTRANGE) só o usuário pode fazer.
- A bateria leva cerca de 8 h 20 com as quantidades do plano (8 processos). O "poucos minutos" do pedido foi retirado pelo orquestrador.
- Os pontos L1–L17 são para o autor do livro.
