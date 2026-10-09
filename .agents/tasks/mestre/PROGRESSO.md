# Progresso: Planilha do Mestre (pasta Mestre)

Entregáveis em `Mestre\`. Linha de base da ficha em `baseline-hashes.json` (regravada só por mudança de outro trabalho; ver notas-fase1).
Design: `design.md`; plano: `plano-mestre.md`; notas da Fase 1 (decisões, achados, bloqueio): `notas-fase1.md`.

## Fases
- [x] 0. Preparação (pastas, baseline de hashes)
- [x] 1. Levantamento das regras/dados do sistema (caps. 05, 16, 19–29 lidos; 27 e 28 inteiros)
- [x] 2. Design (`design.md`: 18 abas, módulos, semente, regras citadas, H1–H25, 4 fases)
  - [x] 2.1 Revisão ciclo 1 atendida
- [x] 3. Implementação — Fase 1 (combate, bestiário, Criador de Inimigos, encontros) — portão 1.10 fechado (05/10 13:42, iteração 2)
- [x] 4. Implementação — Fase 2 (NPCs, aventuras, recompensas) — portão 2.5 fechado sobre o livro **v1.2**
      (iteração 2, revisão `review-fase2.json`: 07/10 20:59–23:23, `--suite fase2`: 7 248 118 checagens, 0 falha);
      v1.2 adotada por decisão do usuário
- [x] 5. Implementação — Fase 3 (campanha, demais geradores, Escudo, Minhas Tabelas): portão 3.5 fechado em 08/10
      (iteração 1, `--suite fase3`: 8 399 289 checagens, 0 falha; plano 3.1–3.5 marcados); iteração 2 (revisão
      `review-fase3.json`, F1–F3) em 09/10 00:47: 10 108 171 checagens, 0 falha
- [x] 6. Fase 4 — Exemplo, COMO-USAR, Memoespírito e condições (pedido de 06/10), auditoria (`relatorio-final.md`)
- [x] 7. Verificação final e conferência de intocabilidade do livro e da ficha (`--suite tudo`, 09/10 04:08–12:28:
      10 979 281 checagens, 0 falha)

## Fase 1 — o que ficou pronto
- `Mestre\Planilha do Mestre - Explorando Galáxias V1.1.xlsx` (modelo em branco) e `Mestre\Planilha do Mestre - Exemplo.xlsx`
  (Exemplo parcial: Mesa, semente 2026, 4 PJs pelo `oraculo_ficha`, Carcereiro Orbital e Capataz do Duto 4, Encontros A e B,
  Combate no Ciclo 2). 18 abas na ordem de D3; as 9 fora da fase dizem "Em construção".
- Abas da fase: Início (semente + índice), Campanha (Mesa + calculadas), Grupo (G1–G4 + resumo), Inimigos (Criador nos 3
  modos, H1, H12, I5, ações pela régua de 28.4, ficha no formato de 28.1), Bestiário (32 fichas, filtro, ficha completa),
  Encontros (orçamento 27.4/H5, 3 encontros salvos, H6/H7, composição, contrato 27.5, regra irmã, DT 20.2, aleatório G = 100
  com H19), Combate (C0–C10: 16 combatentes, Fila 19.3–19.6 + prevista, PV, Tenacidade/Quebra/Dano de Quebra, fases do Boss
  28.5, condições 21.5, Morrendo/Executado, PH/Energia, recargas, calculadora), Tabelas (27.16–27.18 + H8), Dados.

## Iteração 2 (revisão `review-fase1.json`) — o que foi feito
- F1: `suite-tudo.txt` gravado pela `--suite fase1` sobre a versão final (planilhas de 13:01:38); números abaixo.
- F2: `oraculo` e `extremos` terminam: `build\mestre\paralelo.py` (8 processos, plano §10 item 8; mesmas quantidades);
  calculadora em modo "bloco" (recalcula só o que descende das entradas da calculadora). Detalhe em `notas-fase1.md`.
- F3: preview sem célula de erro nos 3 estados. F4: visual e preview com 0 texto cortado (lista "Trocar por" medida
  com o nome digitado no máximo).
- F5: filtro de ambiente funciona; `determinismo` (b) ganhou caso que discrimina ("Ruína", "Frente de guerra").
- F6: linha de base regravada às 09:43:38 (revisão 2 da ficha, workflow `corrigir-erros-google`, 10 arquivos; anterior em
  `baseline-hashes-antes-rev2.json`) e às 11:37:09 (o mesmo trabalho mexeu em `testar_ficha.py` 09:44:12 e
  `AUDITORIA-DA-FICHA.md` 09:43:59; anterior em `baseline-hashes-0943.json`). A Mestre não grava em arquivo da ficha.
  `desktop.ini` do livro (metadado do Drive) passa a ser ignorado pela `protegidos`.
- F7: ROUND → INT; lint proíbe ROUND/ROUNDUP. F8: `%TEMP%\mestre-*` apagados.
- Bugs achados pelo oráculo e corrigidos: nota do Bestiário por cima da fórmula da fase 3; Tenacidade de fase no Ajustar;
  "Ver inimigo" vazio; 5 avisos com `ISBLANK` acesos no modelo em branco (lint agora proíbe ISBLANK fora da camada).

## Requisito do Google — obrigatório em todas as fases (plano §0.1)
- Feito na Fase 1: `build\mestre\protecao.py` (camada de leitura protegida em 2 344 células, 426 sinais de linha,
  aviso PT-BR por linha, contador "Células com erro na planilha" por aba na Início, dica no topo da Início); faixas
  nas listas como "Faixa 1-4"; listas editáveis da aba Tabelas cobertas (vaga vazia ou com erro não conta).
- Fases 2–4: toda entrada nova via `ent()` ou vagas em `MAPA.tabelas` (Minhas Tabelas); o lint cobra; o COMO-USAR
  (Fase 4) leva a dica e o contador.

## Fase 1 — suítes (saída completa em `suite-tudo.txt`, 05/10 13:01–13:42, 2 441 s)
| Suíte | Checagens | Falhas | Destaque |
|---|---:|---:|---|
| spike | 142 | 0 | inclui ""+1 → #VALUE!, vazio = 0 na formulas, ISBLANK("") = FALSE, camada e contador |
| protegidos | 124 | 0 | 38 do livro + 13 da ficha (SHA-256) |
| dados | 647 | 0 | |
| bestiario | 34 | 0 | 32 fichas; 116 ações iguais ao `.md` |
| ouro | 73 | 0 | |
| oraculo | 123 265 | 0 | 2 973 casos; cobertura P10 1 466/1 466; H1 desvio máx. do PV 14,7% |
| determinismo | 50 093 | 0 | |
| extremos | 987 | 0 | 10 estados; 200 sementes × 2; injeção de erro em 70 entradas + todas juntas |
| lint | 87 729 | 0 | 0 opção de lista arriscada; 0 leitura direta de entrada |
| texto | 4 738 127 | 0 | |
| preview | 385 | 0 | 381 recortes ≤ 1800 px; 0 texto cortado |
| visual | 21 651 | 0 | |
| **total** | **5 023 257** | **0** | |

Recortes olhados (Pillow antes): `exemplo-inicio-parte-01.png` (dica no topo em negrito, contador 0 por aba) e
`pior-caso-combate-parte-01.png` (C33:C42 "Trocar por" com o nome longo em 3 linhas, sem corte).

## Fase 2 — o que ficou pronto (detalhes, heurísticas e a adoção da v1.2 em `notas-fase2.md`)
- Abas NPCs (R5, G = 200, Elenco de 30, 4 cartões, bloco de combate pelas âncoras de 28.3), Aventuras (R6, G = 300,
  5 cenas H14, antagonista H22, linha de saída na ordem de Missões) e Recompensas (R7: entrega de marco por regra
  24.5/25.1–25.3/26.7/27.8, Sobreposição por PJ, preços 24.1–24.3, achados G = 400 com H9/H18, sabor de Cone G = 410
  e de Conjunto G = 420, Relíquias por Tier, Tesouro de 25 linhas). Aba Tabelas: 40 tabelas de sabor (nomes ≥ 30
  por cultura em 7 culturas de 05, originais). Exemplo: 6 NPCs do gerador no Elenco, 4 cartões, marco do nível 2,
  2 linhas de Tesouro. Heurística nova **H26** (contratante, local, "Faixa alta"), rotulada e validada.
- **Livro v1.2 adotado (07/10):** changelog E1–E35 conferido item a item contra a Mestre (tabela em `notas-fase2.md`):
  E3, E4, E7, E14, E15, E16 e o capítulo 05 reescrito (E10, E20–E34) aplicados; os demais não tocam a Mestre.
- Entregáveis (07/10 16:52): `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx` (modelo, abas "… v1.2") e
  `Mestre\Planilha do Mestre - Exemplo.xlsx`; 18 abas, 24 676 fórmulas, 2 266 validações, 2 215 entradas, leitura
  protegida do Google em 7 265 células. O `…V1.1.xlsx` fica como registro; os `.gsheet` são do usuário (ignorados).
- Linha de base: `baseline-hashes.json` regravado em 07/10 16:51 (ficha + livro v1.2, 51 arquivos); v1.1 em
  `baseline-hashes-v11.json`. Nenhum arquivo do livro ou da ficha foi editado.

## Fase 2 — iteração 2 (revisão `review-fase2.json`; detalhe em `notas-fase2.md`)
- **F1 (bloqueante, 25.2):** o teto de Sobreposição é do Cone e conta as de faixas anteriores. Grupo G3 ganhou a
  entrada "Total no Cone" (F; Ressonâncias em G:J) com aviso acima do teto e quando o total é menor que as desta faixa.
  Recompensas: cabeçalho "no máximo 1 por faixa; o teto é do Cone", colunas "Nesta faixa (máx. 1)", "No Cone
  (total)", "Teto do Cone"; a Situação compara o total com o teto antes do limite da faixa ("Cone no teto (+3) com as
  que já tem: nenhuma a mais") e o aviso acende acima do teto. Oráculo igual; `ouro` +11 casos (Cone 3/4 + 1
  anterior e Cone 1/2 + 2 anteriores → no teto; 1 + 1, 2 + 0, 3 + 0 → pode receber; 3 + 2, 1 + 3, 5 + 1 → aviso nas
  duas abas; total < desta faixa → aviso); `oraculo` sorteia também o total (0–3 e texto).
- **F2 (27.9):** decisão registrada no plano (itens 2.4 e 3.3): 27.9 só aparece no Escudo (design §6.15); o `ouro`
  da Fase 3 o cobre.
- Planilhas regeneradas em 07/10 19:49 (`…V1.2.xlsx` e `…Exemplo.xlsx`): 24 688 fórmulas, 2 272 validações,
  2 221 entradas, camada de leitura protegida com 7 271 células.

## Fase 2 — suítes v1.2 (saída completa em `suite-tudo.txt`, 07/10 20:59–23:23, 8 588 s)
| Suíte | Checagens | Falhas | Destaque |
|---|---:|---:|---|
| spike | 142 | 0 | |
| protegidos | 165 | 0 | livro (ficha_protegidos.json) + 51 arquivos da linha de base v1.2 |
| dados | 803 | 0 | 156 checagens item a item da Fase 2 (24.1–24.5, 25.1–25.3, 26.7, 27.7, 27.8, 27.16, 27.17) + tabelas do oráculo × .md |
| bestiario | 34 | 0 | 32/32 fichas |
| ouro | 141 | 0 | 24.5/25.1/25.3/26.7 nível a nível; teto da Sobreposição do Cone com as de faixas anteriores (25.2, F1); preços 24.1–24.3 |
| oraculo | 609 756 | 0 | 900 casos G = 200…420 + H22 em 40 facção × faixa; cobertura P10 1 602/1 602 |
| determinismo | 161 479 | 0 | (a)–(g) também para G = 200, 300, 400, 410, 420 |
| extremos | 1 024 | 0 | 11 estados (inclui Elenco/Tesouro cheios), 200 sementes × 2, injeção de erro em 86 entradas (a amostra aleatória de 150 entradas mudou com as 6 entradas novas de G3) |
| lint | 149 589 | 0 | 0 achado do Google |
| texto | 6 281 292 | 0 | |
| preview | 688 | 0 | 684 recortes ≤ 1800 px, 12 abas × 3 estados, 0 texto cortado |
| visual | 33 736 | 0 | 0 texto que não coube |
| sabor | 9 269 | 0 | 131 nomes do jogo × 40 tabelas e 6 666 combinações nome + sobrenome |
| **total** | **7 248 118** | **0** | |

Recortes olhados na iteração 2: `exemplo-grupo-parte-01.png` (G3 com "Total no Cone", nada cortado) e
`exemplo-recompensas-parte-01.png` (quadro de Sobreposições com o cabeçalho e as colunas novas).

H20: fonte "livro" 51,1% (NPC) e 48,3% (aventura) em 2 000 rolagens. H9: 0/1/2 consumíveis 34,0/32,5/33,5% em
3 000. H18: erro máximo de arredondamento 0 Cr. H22: 40 combinações, nenhuma vazia (degraus 4/5/31).

Recortes olhados (Pillow antes, ≤ 1800 px): `exemplo-npcs-parte-01.png`, `exemplo-aventuras-parte-01.png`,
`exemplo-recompensas-parte-01.png`, `exemplo-npcs-parte-17.png` (cartões). Nada cortado; rótulos de Sugestão visíveis.

## Pedido novo do usuário (06/10) — Memoespírito e Condições
- Especificação: `.agents\tasks\mestre\pedido-combate-memoespirito-condicoes.md` (M1–M4, C1–C6): Memoespírito da
  Recordação ligado a um PJ, com "invocado? Sim/Não" e entrada na Fila; várias condições por combatente (inimigos e
  aliados) com turnos restantes e painel lateral de consulta rápida.
- Entra **antes da Fase 4**, para o Exemplo e o COMO-USAR já cobrirem o recurso. Não implementado nesta iteração.

## Fase 3 — o que ficou pronto (decisões e achados em `notas-fase3.md`)
- **Início (R9):** semente, painel (nível, faixa, DT, PH, missões, relógios a 1 de encher, Ressonância, ritmo,
  próxima sessão), índice das 18 abas e avisos agregados por aba.
- **Campanha (R9):** marcos e ritmo (26.1, 26.7), 12 facções com reputação de −3 a +3 (H17), 10 relógios (H16, barra
  ●○), linha do tempo de 30 eventos com os 5 próximos, Ficha de Decisões (27.11, 29.11) e Sessão Zero (03 + H24:
  expectativas, tom, limites e véus, combinados).
- **Grupo:** G5 e G6 (Resistências, perícias e passivas), aviso de Tier (25.3) e resumo de surpresa e de fraqueza.
- **Sessões e Missões:** preparação com cenas, pistas, ganchos e checklist, diário, e missões com estado e contagem
  (H23).
- **Mundos (R8, G = 510–560):** planeta ou local, estação, nave, facção nova, organização e nomes avulsos (pessoas
  por cultura, naves, lugares, organizações).
- **Improviso (R8, R13, G = 600–650):** rumores com veracidade, evento de viagem, espaço ou cidade com o custo da
  falha (02, 27.1), loja com estoque H15 e preços de 24.1–24.3, bugigangas, oráculo "Sim, e…"/"Não, mas…" (H10),
  rolador semeado e DT rápida.
- **Escudo do Mestre (R10):** 5 páginas A4 paisagem, tudo lido da aba Dados (27.2–27.5, 27.9, 28.3, 28.4, 20.2–20.6,
  16.2, 17.2, 19.3–19.7, 23.3–23.6, 27.10 com 14 casos, 29.12) e "Para o grupo agora".
- **Minhas Tabelas (R11, G = 701–710):** 10 tabelas × 100 vagas, com sorteio de 1 a 5 sem repetir. A aba Tabelas
  ganhou os blocos de sabor Mundos e Improviso: 70 tabelas de sabor no total, com ≥ 20 entradas cada e nomes ≥ 30
  por cultura.
- **Entregáveis (08/10 08:52):** `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx` e
  `Mestre\Planilha do Mestre - Exemplo.xlsx`; 18 abas, nenhuma "Em construção"; 39 600 fórmulas, 3 410 validações,
  4 318 entradas, 1 624 números de regra; leitura protegida do Google em 12 419 células. O nome continua V1.2 (livro
  v1.2 adotado), e não V1.1 como diz o pedido da Fase 3.
- Exemplo: facções, relógios, linha do tempo, decisões, Sessão Zero, 3 missões, sessão 2 com diário e a tabela
  "Clima no Expresso" em Minhas Tabelas.

## Fase 3 — suítes (saída completa em `suite-tudo.txt` e `suite-fase3.txt`, 08/10 08:52–16:04, 25 895 s; Fase 2 em `suite-fase2.txt`)
| Suíte | Checagens | Falhas | Destaque |
|---|---:|---:|---|
| spike | 142 | 0 | |
| protegidos | 165 | 0 | livro e ficha intocados |
| dados | 1 574 | 0 | 771 checagens da Fase 3: 16 blocos, 65 trechos de regra, loja × 24.1–24.3, Escudo × Dados |
| bestiario | 34 | 0 | |
| ouro | 322 | 0 | 27.9 no Escudo, 23.3, 23.6, 27.2 (30 casos), 26.1, 26.7, loja, H16 (45), H17 (7), H23 |
| oraculo | 988 136 | 0 | 900 casos G = 510…710 + 60 estados de campanha; cobertura P10 1 624/1 624 |
| determinismo | 298 956 | 0 | 21 geradores; (e) em 100 000 rolagens (ver notas) |
| extremos | 1 084 | 0 | 14 estados, 200 sementes × 2 em 4 406 células, erro injetado em 106 entradas |
| lint | 221 185 | 0 | Escudo A4 paisagem, páginas ≤ 633 pt |
| texto | 6 824 009 | 0 | heurísticas H1–H26 rotuladas; 1 283 palavras extras |
| preview | 1 339 | 0 | 1 335 recortes ≤ 1800 px, 18 abas × 3 estados, 0 texto cortado |
| visual | 51 488 | 0 | 47 403 textos medidos, 0 não couberam |
| sabor | 10 855 | 0 | 70 tabelas; 6 666 combinações nome + sobrenome |
| **total** | **8 399 289** | **0** | |

Recortes olhados (Pillow antes, ≤ 1800 px):
- `exemplo-escudo-do-mestre-parte-01.png`: páginas 1 e 2 legíveis. O subtítulo dizia "4 páginas" e foi corrigido
  para 5.
- `exemplo-improviso-parte-01.png`: rumores, evento, loja de Farmácia com preços e oráculo, com os rótulos H10, H15
  e H25 visíveis.
- `exemplo-campanha-parte-05.png`: linha do tempo do Exemplo em ordem, nada cortado. As linhas são altas porque são
  medidas pelo pior caso de 200 caracteres.

## Fase 3 — iteração 2 (revisão `review-fase3.json`; detalhe em `notas-fase3.md`)
- **F1 (bloqueante):** Campanha!E10 e E11 não dizem mais "(próxima fase)". Agora: "Lida pela aba Sessões
  (preparação e diário) e pela Início." e "Usado pela linha do tempo (nesta aba, mais abaixo).". O lint barra "Em
  construção" e "próxima fase" em qualquer célula das 18 abas. No arquivo antigo ele acusa E10 e E11; no novo, 0.
- **F2:** o Exemplo de 12:51:38 era uma regravação pelo Google Planilhas (modo Office, sincronizada pelo Drive).
  Antes de regenerar, comparei esse arquivo com o novo, célula a célula: as 4 318 entradas são iguais, ninguém digitou
  nada, e nenhum dado foi perdido. A cópia foi apagada depois da comparação. **Pergunta ao usuário, antes da Fase 4:**
  você abriu o `…Exemplo.xlsx` no Google Planilhas em 08/10 por volta de 12:51? Se abrir um `.xlsx` desta pasta no
  Google durante uma bateria, ele é regravado. Suíte nova `origem` (no início e no fim da `fase3`): app.xml, sem
  xl/metadata, área de impressão do Escudo, mesmas validações nos dois arquivos, gravação até ±900 s do mapa.
- **F3:** os títulos das páginas do Escudo dizem o que cada página tem: 1 "…; descanso", 2 "O inimigo, a Tenacidade
  e o PH", 4 "Pessoas: condições, Morrendo e PV temporários", 5 "Mesa: Energia, tetos e casos-limite". O plano 3.3 e
  o design §6.15 agora falam em 5 páginas ("página N de 5").
- Planilhas regeneradas em 08/10 16:47 (`…V1.2.xlsx` e `…Exemplo.xlsx`): 39 600 fórmulas, 3 410 validações,
  4 318 entradas. Livro e ficha intocados (`protegidos`).

## Fase 3 — suítes da iteração 2 (`suite-tudo.txt` = `suite-fase3.txt`, 08/10 17:26 – 09/10 00:47, 26 442 s)
| Suíte | Checagens | Falhas | Destaque |
|---|---:|---:|---|
| origem (início) | 9 | 0 | os 2 arquivos do gerador; Exemplo +5 s do mapa, 3 410 validações |
| spike | 142 | 0 | |
| protegidos | 165 | 0 | |
| dados | 1 574 | 0 | Escudo × Dados: 555 células |
| bestiario | 34 | 0 | |
| ouro | 322 | 0 | |
| oraculo | 988 136 | 0 | cobertura P10 1 624/1 624 |
| determinismo | 298 956 | 0 | |
| extremos | 1 084 | 0 | 14 estados, 200 sementes × 2 |
| lint | 221 203 | 0 | +18: "Em construção"/"próxima fase" por aba |
| texto | 8 532 855 | 0 | mede agora o Exemplo do gerador (o regravado tinha menos fórmulas) |
| preview | 1 339 | 0 | 1 335 recortes ≤ 1800 px, 0 texto cortado |
| visual | 51 488 | 0 | 47 403 textos, 0 não couberam |
| sabor | 10 855 | 0 | |
| origem (fim) | 9 | 0 | nada regravou os arquivos durante a bateria |
| **total** | **10 108 171** | **0** | |

Recortes olhados: `exemplo-campanha-parte-01.png` (E10/E11 novos, nada cortado) e
`exemplo-escudo-do-mestre-parte-02.png` (títulos das páginas 4 e 5).

## Fase 4 — o que ficou pronto (decisões em `notas-fase4.md`; relatório em `relatorio-final.md`)
- Decisões do usuário (09/10): (1) o Memoespírito e as condições entram nesta fase; (2) o modelo é o V1.2, e o
  `…V1.1.xlsx` fica como registro; (3) as quantidades do plano são mantidas, numa bateria completa destacada. Os
  `.gsheet` são do usuário e não são tocados. A regravação de 08/10 12:51 foi o usuário testando no Google.
- **Memoespírito e condições:**
  - Grupo G7/G8: o Memoespírito ligado ao PJ.
  - Combate C2b: "Invocado?" Sim/Não. O Memoespírito entra na Fila pela VEL dele; são 22 combatentes no total.
  - C7: 4 condições por combatente (88 linhas), com turnos e EXPIRADA.
  - Painel C9b com o efeito de 21.5.
  - H27 nova (`Combate!A41`).
- **Exemplo completo (§14):**
  - KV-12 passou para a Recordação, com o Memoespírito "Eco do Construtor" (PV 23, VEL 17), que age na casa 2.
  - Condições acumuladas no Sargento (3) e na Nadir (2), e 1 expirada.
- **COMO-USAR:** `Mestre\COMO-USAR-PLANILHA-DO-MESTRE.md`, com 12 seções. O checklist tem 25 células conferidas pela
  suíte `guia`. Os endereços do IMPORTRANGE foram conferidos contra `build\ficha_mapa.json`.
- **Planilhas** (09/10 03:46): 41 810 fórmulas, 3 636 validações, 4 544 entradas, 1 966 números de regra.

## >>> CRITÉRIO DE ACEITAÇÃO do pedido de Memoespírito e condições (seção 5) — para a revisão conferir item a item <<<
| # | Critério (o Mestre em mesa, sem sair da planilha) | Onde | Prova |
|---|---|---|---|
| 1 | Ligar um Memoespírito a um PJ da Recordação e ver os números dele | Grupo G7 (entradas) e G8 (números em uso) | `ouro` 11.4 (151 / 21 / 15 / RT 2); `oraculo` 150 estados; `exemplo` (= oraculo_ficha) |
| 2 | "Memoespírito invocado? Sim" e ele entra na Fila na posição certa pela VEL | Combate C2b; combatentes 17–22 | `ouro` 11.5/19.7 e H27; `oraculo` 300 Filas; `exemplo` (casa 2, VEL 17) |
| 3 | 3 condições diferentes num inimigo e 2 num aliado, com turnos | C7: 4 por combatente (88 linhas) | `exemplo` (Sargento 3, Nadir 2); `oraculo` 120 estados |
| 4 | Um painel só, ao lado da Fila: em quem, por quantos turnos, o que faz | C9b, logo abaixo da Fila (30 linhas + "Mais N") | `oraculo`; `exemplo`; recorte `exemplo-combate-parte-06.png` |
| 5 | A condição sai da conta sozinha quando os turnos acabam | 0 turnos = "EXPIRADA (0 turnos)…", fora do painel, do Congelado e do Surpreso | `exemplo` (Sangramento do Sargento); `oraculo` |

M1–M4 e C1–C6 item a item em `notas-fase4.md` e em `relatorio-final.md`.

## Fase 4 — suítes (`suite-tudo.txt`, 09/10 04:08–12:28, 30 000 s)
| Suíte | Checagens | Falhas |
|---|---:|---:|
| origem (início) | 9 | 0 |
| entregaveis | 4 | 0 |
| spike | 142 | 0 |
| protegidos | 165 | 0 |
| dados | 1 574 | 0 |
| bestiario | 34 | 0 |
| ouro | 334 | 0 |
| oraculo | 1 135 830 | 0 |
| determinismo | 298 956 | 0 |
| extremos | 1 103 | 0 |
| lint | 232 391 | 0 |
| texto | 9 195 537 | 0 |
| preview | 1 336 | 0 |
| visual | 53 025 | 0 |
| sabor | 10 855 | 0 |
| exemplo | 47 852 | 0 |
| guia | 125 | 0 |
| origem (fim) | 9 | 0 |
| **total** | **10 979 281** | **0** |

Recortes olhados: `exemplo-combate-parte-01.png` (C2b com o Memoespírito invocado) e `exemplo-combate-parte-06.png`
(painel C9b). Nada está cortado.

## Revisão da Fase 4 e ajustes finais (09/10) — projeto fechado
Veredito: **APPROVED** (`review-fase4.json`), com 3 achados não bloqueantes, todos fechados em 09/10.
Saída das suítes em `suite-ajustes-finais.txt`.

- **N1** — `plano-mestre.md` §1 e a tabela R12 ainda diziam `…V1.1.xlsx`: atualizados para `…V1.2.xlsx`,
  citando a decisão do usuário (`notas-fase2.md` 07/10, confirmada em `notas-fase4.md` 09/10).
- **N2** — o estado da Fila no Exemplo contradizia o guia (a Nadir, na casa 4, com "Já agiu" enquanto a
  Tessaly, na casa 1, estava "Agindo agora"). Corrigido em `build\mestre\exemplo.py`: no meio do Ciclo 2 já
  agiram as casas 1 a 4 (Tessaly, o Memoespírito de KV-12, a KV-12 e a Nadir), e "Agindo agora" cai na casa
  5, o Sargento de Trincheira, que é justamente quem está com três condições. Exemplo regenerado.
- **N3** — "31 funções" no relatório virou "31 das 33 (sem ROUND e ROUNDUP)", igual ao que o `lint` imprime.

Suítes afetadas, todas com 0 falha: `origem` 9, `entregaveis` 4, `lint` 232 391, `exemplo` 47 853, `guia` 125.
Recorte do Combate do Exemplo conferido, sem texto cortado. Temporários `$env:TEMP\mestre-*` apagados.

O run `wf_5ddda4dd5c81a008` que fez estes ajustes terminou com "Usage limit reached" **depois** de aplicar as
3 correções e rodar as 5 suítes; faltava só esta anotação e a limpeza, feitas pelo orquestrador.

## O que falta
- Nada da implementação nem da revisão: o projeto está fechado.
- Fica com o usuário: o checklist de 2 minutos no Google (validação, formatação condicional, impressão e
  IMPORTRANGE) e decidir se apaga o `…V1.1.xlsx`, que ficou na pasta como registro.
- Fica com o autor do livro: L1–L17 (`relatorio-final.md`, seção "Inconsistências e lacunas do livro").

## Como retomar
1. `$env:PYTHONUTF8="1"; python "build\gerar_mestre.py"` (≈ 3 min) grava as 2 planilhas e `build\mestre_mapa.json`.
2. `$env:PYTHONUTF8="1"; python "build\testar_mestre.py" --suite tudo --saida ".agents\tasks\mestre\suite-tudo.txt"`
   (suíte avulsa: `--suite <nome>`). Leva ≈ 8 h 20. Rode destacado com
   `Invoke-CimMethod Win32_Process Create` (`cmd /c "set PYTHONUTF8=1&& python …"`). Em 08/10, um `Start-Process`
   foi encerrado junto com a chamada da ferramenta.
3. Leia `notas-fase1.md`, `notas-fase2.md` (adoção da v1.2, linha de base), `notas-fase3.md` e o §0.1 do plano.
