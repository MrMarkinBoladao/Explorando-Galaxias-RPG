# Notas da Fase 4: Exemplo, COMO-USAR, Memoespírito e condições, verificação final

## Decisões do usuário (09/10, resposta às 3 perguntas do início da fase)
1. **Memoespírito e condições** (`pedido-combate-memoespirito-condicoes.md`) entram nesta fase: o escopo da Fase 4
   foi ampliado pelo orquestrador.
2. **O modelo é V1.2**: `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx`. O "V1.1" do pedido da fase é
   texto de antes da adoção da v1.2. O `…V1.1.xlsx` de 05/10 fica na pasta como registro (o usuário decide se apaga).
   A suíte `entregaveis` exige os 3 entregáveis e aceita o registro V1.1, os `.gsheet` (só o nome é olhado) e o
   `desktop.ini`.
3. **Quantidades do plano mantidas**: uma bateria completa, destacada, como evidência.
4. A regravação do Exemplo em 08/10 12:51 foi o usuário testando no Google. O arquivo regravado nunca é fonte: a
   planilha é sempre regenerada pelo gerador, e a suíte `origem` confere isso no começo e no fim da bateria.

## O que existia antes (o relato do usuário confirmado)
A aba Combate tinha só a C7: 48 linhas livres, uma condição por linha, com combatente escolhido numa lista, turnos,
acúmulos e quem aplicou. Não havia painel com o efeito, nem lugar para o Memoespírito (nem no Grupo, nem na Fila).
A C7 foi absorvida (mesmas colunas, mesmo cálculo de dano), não descartada.

## Critério de aceitação do pedido (seção 5), item a item
| # | Critério (do ponto de vista do Mestre em mesa) | Onde | Prova |
|---|---|---|---|
| 1 | Ligar um Memoespírito a um PJ da Recordação e ver os números dele | Grupo G7 (Tem? Sim/Não, nome, PV, Defesa, VEL, RD, pontos) e G8 (números em uso, dano do ataque, Redução de Tenacidade; vazio = 11.4 sem Bênção) | `ouro` (o exemplo de 11.4: 151 / 21 / 15 / RT 2); `oraculo` (150 estados "Memoespírito"); `exemplo` (G8 = oraculo_ficha) |
| 2 | Marcar "Memoespírito invocado? Sim" e vê-lo entrar na Fila pela VEL | Combate C2b (Invocado?, VEL, PV, Defesa, Na Fila?); combatentes 17–22 da tabela de estado | `ouro` (VEL 15 antes da dona de VEL 14; Não = fora; 0 PV = "Não: caiu"; empate total H27); `oraculo` (Fila em 300 estados com Memoespíritos aleatórios); `exemplo` (Eco do Construtor na casa 2) |
| 3 | 3 condições diferentes num inimigo e 2 num aliado, com turnos | C7: 4 linhas por combatente (88), cada uma com condição, turnos, acúmulos e quem aplicou | `exemplo` (Sargento: Queimadura, Marcado, Vulnerável; Nadir: Lentidão, Marcado); `oraculo` (120 estados de condições, 12 com as 88 cheias) |
| 4 | Um painel só, ao lado da Fila, com tudo que está ativo: em quem, por quantos turnos e o que faz | C9b (logo abaixo da Fila C9): 30 linhas, "Agora" com o resumo, efeito de 21.5 + número de agora + duração | `oraculo` (painel × oráculo, inclusive "Mais N" acima de 30); `exemplo`; `preview` |
| 5 | A condição sai da conta sozinha quando os turnos acabam | Turnos = 0 → "EXPIRADA (0 turnos)…" na C7 (texto, não só cor), fora do painel, do Congelado e do Surpreso | `exemplo` (Sangramento do Sargento); `oraculo` (turnos 0 sorteados) |

Requisitos M1–M4 e C1–C6:
- **M1** G7/G8 (acima). **M2** C2b + Fila. **M3** 11.5 e 19.7 na própria aba (invocar = Ação Complementar + 1 PH; casa
  própria; 1 ação por turno; some a 0 PV até o Descanso Curto; sem Tenacidade/Quebra/Congelado); o que o livro não
  diz é a **H27** (rotulada em `Combate!A41`). **M4** 1 por PJ (6), num limite novo de 22 combatentes na Fila.
- **C1/C4** 4 por combatente, para PJs, inimigos e Memoespíritos. **C2** lista do capítulo 21 + turnos digitados.
  **C3** painel C9b. **C5** Fase 1 preservada: mesmas fórmulas de dano, Congelado, Surpreso, Quebra, Morrendo e Fila
  (o `ouro` de 19.4, 20.4, 20.5, 21.2, 23.4 passa igual). **C6** EXPIRADA.

## Decisões de leiaute
- 22 combatentes: 1–6 PJs, 7–16 inimigos (índices de antes, nada muda para eles), 17–22 os Memoespíritos dos PJs 1–6.
- C8 e C9 em blocos de 10 (22 linhas); a "Casa manual" vai até 22.
- C7 com 4 condições por combatente (o pedido diz 4 a 6): 88 linhas em 8 blocos de 12, cada linha já com o nome do
  combatente (não precisa escolher na lista). Nome lógico `combate.c{n}`, n = (combatente − 1) × 4 + k.
- O painel fica em A:L, logo abaixo da Fila: as colunas à direita de L são auxiliares e ocultas, e a área usada de cada
  aba cabe em 1360 px. "Do lado" virou "colado na Fila".
- Os números do Memoespírito vêm da ficha do jogador (como os do PJ na G2); vazio = 11.4 sem Bênção, com aviso.
- O PJ KV-12 do Exemplo passou da Abundância para a Recordação, com um Memoespírito (oraculo_ficha: 0 aviso; Perícias
  Tecnologia e Mecânica, porque Ciência já vem do Caminho).

## Achados nesta fase
- `formulas`: `{pvat}-{entrada}` dentro de AND com a entrada vazia dá #VALUE! (o aviso de cura do C2b). A forma certa
  é ler a entrada já convertida (`IF(ISNUMBER(x),INT(x),0)`).
- 21.5 × Dados: a Corrupção sai com "Dano Contínuo = Sim" no bloco `condicoes` (o efeito cita Dano Contínuo); o aviso da
  C7 diz "Dano Contínuo: início do turno do alvo…" para ela. É da Fase 1 e não muda número; fica registrado.
