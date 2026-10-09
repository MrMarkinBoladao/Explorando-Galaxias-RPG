# Notas da Fase 1 — decisões de implementação e achados (para o revisor)

Iteração 1 (não havia `review-fase1.json`). Plano: `plano-mestre.md` §4; design: `design.md` §5–§12.

## Arquivos novos (nenhum arquivo da ficha ou do livro foi editado)
- `build\gerar_mestre.py` — ponto de entrada; grava modelo + Exemplo via `.tmp.xlsx` + `os.replace`.
- `build\mestre_dados.py` — parsers dos caps. 27/28 + reuso de `ficha_dados` (19–25); P13 (divergência nova é fatal).
- `build\mestre\nucleo.py`, `sorteio.py`, `aba_inicio.py`, `aba_campanha.py`, `aba_tabelas.py`, `aba_inimigos.py`,
  `aba_inimigos_acoes.py`, `aba_bestiario.py`, `aba_encontros.py`, `aba_combate.py`, `aba_combate_base.py`,
  `aba_combate_inimigos.py`, `aba_combate_fila.py`, `exemplo.py`, `testes_*.py`.
- Oráculo independente: `build\oraculo_mestre.py` (sorteio + `calcular`), `oraculo_mestre_livro.py` (tabelas transcritas
  com a seção + parser próprio do cap. 28), `oraculo_mestre_abas.py`, `oraculo_mestre_cmb.py`. Não importam
  `mestre_dados` nem `mestre\*` e não leem fórmula.
- `build\testar_mestre.py` (CLI, `--suite`, `--saida` UTF-8, atalho `fase1`/`tudo`).

## Decisões de implementação (dentro do que o design deixa em aberto)
- Catálogo único (12 inimigos da campanha + 32 do bestiário) em colunas ocultas da aba Inimigos; Encontros e Combate
  procuram nele (os da campanha primeiro, como pede 6.9).
- H12 (Fraquezas sugeridas) só quando as 4 Fraquezas da linha estão vazias; no modo Ajustar, vazio = as da base.
- Marcadores do texto-modelo (6.7.3) guardados como tipo + parâmetro em colunas separadas (`DANO.e/.m`,
  `DANO15.e/.m`, `COMUM.e/.m`, `DT`, `PV`) — sem SUBSTITUTE/MID. Máximo medido: 4 marcadores por ação.
- Calculadora C10: a fonte "Dano de Quebra" não entra na lista (o Dano de Quebra já sai pronto em C5b).
- Atraso em PJ: sem teto (19.4 só dá teto para Comum/Elite/Boss).
- Eficiência de inimigo (dano de condição aplicada por inimigo) = TR do Elite da faixa (28.3: TR = Ef−1/Ef/Ef+1).
- Surpresa: por combatente, pela condição "Surpreso" em C7, só no Ciclo 1 (19.3: quem falha recebe Surpreso).
- Escória de Stellaron conta 1,5 Comum também no reconhecimento da composição (28.10: "três Escórias são quatro e
  meia"), o que faz "4 Guardas + 2 Escórias" de 28.11 ser lido como "7 Comuns".
- Exemplo (parte da Fase 1): os 4 PJs saem de `oraculo_ficha.calcular` (fatal se avisar). Shen usa Armadura Pesada,
  e o oráculo da ficha emite `ESQUIVA_PROIBIDA`, que é a regra de 24.1 e não erro do PJ: é o único aviso aceito, e
  a Esquiva dela fica vazia.

## Itens "a confirmar na implementação" (plano §10) — resultado
1. L1: **16 fichas sem Execução declarada** (Casco Oco, Larva, Esporo, Peão, Capataz, Sargento, Afogado, Fuzileiro,
   Devoto, Centurião, Auditora, Pretor, Palhaço, Dramaturgo, Vênia, Germe) → "Não declarado" + aviso no Combate
   ("só ser racional Executa, 23.5"); 16 declaram (Pode/Não).
2. L2: as divergências de Tenacidade de fase estão em `mestre_dados.DIVERGENCIAS_DOCUMENTADAS` (Dramaturgo f2 = 9;
   Germe f3 = 10; Vazia Coroada f2 = 12 e f3 = 10). Todas abaixo da âncora, o que 28.5 regra 3 permite. Nenhum outro
   número de ficha diverge de 28.3.
3. Ataques/ações: **116** (não ≈ 95); todos voltam idênticos ao `.md` na faixa original (suíte bestiario).
4. `ficha_dados` já parseia condições, PH, Tenacidade, Elementos e DTs no formato usado.
5. 27.16–27.18: 8 facções, 6 locais, 20 ganchos (4 por faixa) — conferidos pela suíte dados.
6. Casos de ouro relidos no `.md` antes de virar expectativa (suíte ouro). 23.6 (Descanso Curto), 24.5 e 25.1 ficam
   para as fases que têm as abas.
7. Nadir = 29.7 (PV 61, Defesa 16, Esquiva 18, RD 0, VEL 14, DT 14, Presença +0) via `oraculo_ficha`.
8. Desempenho: carga do modelo no `formulas` ≈ 40 s; recálculo de todas as 8 925 fórmulas ≈ 15 s; subconjuntos < 1 s.
9. Validação de lista apontando para outra aba: aprovada no spike (`formulas` e reabertura no openpyxl). No Google:
   **não verificado aqui** (vai para a checklist do guia, Fase 4).

## Achados de heurística (honestos)
- H8: o design pede "todo ambiente com criatura em ≥ 2 faixas". Com as fichas do livro isso **não vale**: cada facção
  aparece numa faixa só (ex.: Ruína e Colônia só 1-4; Clínica só 13-16). A suíte dados confere "≥ 1 criatura por
  ambiente" e lista os ambientes de uma faixa só; o encontro aleatório cai para "qualquer ambiente da faixa" e avisa.
- H7: a composição "Combate A" de 29.5 (305 + 50 contra 88) dá 4,0 Ciclos com o contrato cumprido (o livro publica
  3,7 com o DPC puro de Boss — L3).

## Iteração 2 — correções da revisão (`review-fase1.json`) e requisito do Google

- **F1/F2 (portão e suítes de volume):** `build\mestre\paralelo.py` reparte `oraculo` e `extremos` em até 8 processos
  (`$env:MESTRE_PROCESSOS`), plano §10 item 8, sem reduzir as quantidades do plano. A calculadora (2 000 casos) usa o
  modo "bloco": a base do alvo é calculada uma vez e cada caso recalcula só o grafo que descende das 9 entradas da
  calculadora (~0,35 s em vez de ~4 s); a exatidão é provada pela própria comparação com o oráculo. Casos de um
  mesmo grupo preenchem com "" as entradas que outro caso usa (mesma redução do grafo): é exato porque nenhuma
  fórmula lê entrada direto (lint). Lição: o timeout de 30 min da ferramenta manda Ctrl+C para a árvore de
  processos; a bateria tem de rodar destacada (`Start-Process`).
- **F3:** `preview` sem célula de erro nos 3 estados (rodada da fase1 abaixo).
- **F4:** a lista "Trocar por" (Combate C33:C42) passa a ser medida com o nome digitado no máximo (catálogo inclui os
  inimigos da campanha); `gerar_mestre.py` registra esse pior caso e a altura da linha cresce.
- **F5:** o filtro de ambiente funciona na planilha atual: a sonda de 09:28 (semente 777, rolagem 9, faixa 1-4) dá
  "Sentinela Enferrujada, Casco Oco…" sem ambiente e "Esporo Rancoroso, Casco Oco…" com "Ruína", igual no oráculo e na
  planilha; a falha da revisão era da planilha anterior às edições das 09:02. Para a suíte provar isso sempre, o
  `determinismo` (b) ganhou um caso explícito: "Ruína" e "Frente de guerra" mudam as criaturas no oráculo (o caso
  discrimina), a planilha segue o oráculo, e toda criatura sorteada é de facção daquele ambiente (H8).
- **F6 (linha de base da ficha):** regravada duas vezes, sempre por mudança feita por outro trabalho (a Mestre não tem
  caminho de gravação em arquivo da ficha — grep em `build\mestre\*.py`, `gerar_mestre.py`, `testar_mestre.py`,
  `mestre_dados.py`, `oraculo_mestre*.py`):
  - 05/10 09:43:38 — causa: revisão 2 da ficha (workflow `corrigir-erros-google`); 10 arquivos: `gerar_ficha.py`,
    `testar_ficha.py`, `oraculo_ficha.py`, `ficha_dados.py`, `ficha_funcoes_ok.json`, `ficha_mapa.json`,
    `AUDITORIA-DA-FICHA.md`, `COMO-USAR-NO-GOOGLE-PLANILHAS.md`, `Ficha Automatizada - Explorando Galáxias V1.1.xlsx`,
    `Ficha Exemplo - Nadir.xlsx`. Anterior guardada em `baseline-hashes-antes-rev2.json`.
  - 05/10 11:37:09 — causa: o mesmo trabalho da ficha mexeu de novo em `AUDITORIA-DA-FICHA.md` (09:43:59) e
    `testar_ficha.py` (09:44:12); 2 arquivos. Anterior guardada em `baseline-hashes-0943.json`.
  A "Cópia de Ficha…" segue ausente (P5; backup do usuário em `.agents\tasks\backup-usuario-0410\`), não foi tocada.
- **F7:** ROUND trocado por INT com meio para cima em aritmética inteira (`% do orçamento`, `Ciclos estimados`); o
  lint proíbe ROUND/ROUNDUP (autoteste incluído).
- **F8:** temporários `%TEMP%\mestre-*` apagados no fechamento.
- **Bugs achados pelo oráculo nesta iteração:** (1) a nota de rodapé do Bestiário era gravada por cima da fórmula da
  fase 3 da ficha (A120) — nota descida uma linha; (2) a Tenacidade de fase no Ajustar (sem linha em I5) nunca
  usava a da base reescalada (o `IFERROR` não pegava o `INDEX(…,#N/A)` dentro de `ISNUMBER`) — teste por
  `ISNUMBER(MATCH)`; (3) com a camada protegida, "Ver inimigo" vazio vira "" e `MATCH("")` achava uma linha sem nome —
  guarda `LEN(ver)=0`.

### Requisito do Google (pedido do orquestrador, lição da revisão 2 da ficha)
- `build\mestre\protecao.py`: camada de leitura protegida `=IF(ISERROR(X),"",IF(ISBLANK(X),"",X))` (colunas ocultas),
  referências reescritas, um sinal de erro por linha, aviso da linha em PT-BR (mensagens da ficha por import), contador
  na Início ("Células com erro na planilha", por aba, `SUMPRODUCT(ISERROR(…)*1)`, sem circularidade) e a dica no topo
  da Início. Entradas cobertas: as do mapa e todas as vagas das listas editáveis da aba Tabelas (o contador corrido
  das listas lê a camada, então vaga vazia ou com erro não conta).
- Faixas nas listas suspensas como "Faixa 1-4" ("1-4" vira data no Google): `mestre_dados.ROTULOS_FAIXA`,
  `nucleo.faixa_da_lista`; Exemplo e testes convertem com `valor_digitado`/`testes_comum.digitado`.
- Testes: `lint` chama `testar_ficha._lint_google` com o mapa da Mestre (0 opção arriscada, 0 leitura direta);
  `spike` confere `""+1`→#VALUE!, vazio=0 na formulas, `ISBLANK("")`=FALSE, camada e contador; `extremos` injeta
  erro numa amostra de ~60 entradas (uma de cada lista distinta por aba, semente, nível, nº de jogadores, combatente,
  PV, 10 vagas, 10 de texto, 10 numéricas — amostra decidida pelo orquestrador; a prova para TODA entrada é o lint)
  e em todas as entradas ao mesmo tempo: contador = exatamente 1 (total e na aba), aviso aceso, nenhuma outra célula
  com erro.
- Registrado como seção obrigatória 0.1 do `plano-mestre.md` para as Fases 2–4.

## Bloqueio externo (precisa de decisão do usuário)
- Durante esta sessão, **outro processo alterou arquivos da ficha** (`build\gerar_ficha.py` 07:37, `testar_ficha.py`
  07:58, `ficha_funcoes_ok.json` 07:58, `ficha_dados.py`/`oraculo_ficha.py` 01:08, `ficha_mapa.json`, os `.xlsx` e
  `.md` de `ficha-automatizada\`; há uma tarefa `.agents\tasks\google-rev2` ativa). A Mestre não grava nesses
  arquivos (só lê por import). A suíte `protegidos` acusa 10 hashes diferentes de `baseline-hashes.json`; o livro
  (`ficha_protegidos.json`) está intacto. Re-gravar a linha de base é decisão do usuário, não desta fase.
