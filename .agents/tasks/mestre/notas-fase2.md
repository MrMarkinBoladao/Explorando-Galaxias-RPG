# Notas da Fase 2 — NPCs, Aventuras, Recompensas (R5, R6, R7)

Iteração 1 (não havia `review-fase2.json`). Plano: `plano-mestre.md` §5 (2.1–2.5); design: §6.6, §6.11, §6.12, §6.16.
Nenhum arquivo do livro ou da ficha foi editado (a ficha só é lida por import; `protegidos` confere).

## Arquivos
- Novos: `build\mestre_sabor.py` (tabelas de sabor), `build\mestre_sabor_nomes.py` (nomes por cultura),
  `build\mestre\historia.py` (peças comuns dos geradores), `build\mestre\aba_npcs.py`, `aba_aventuras.py`,
  `aba_recompensas.py`, `build\oraculo_mestre_hist.py` (oráculo da fase), `build\mestre\testes_hist.py`.
- Alterados (só arquivos da Mestre): `gerar_mestre.py` (monta as 3 abas), `mestre_dados.py` (G = 200…420, blocos
  de 24.1–24.3, 25.2, 25.3, 26.7, 27.7, 27.8, 27.16, 27.17 e listas), `mestre\nucleo.py` (`ABAS_PRONTAS`),
  `mestre\aba_tabelas.py` (blocos 2–6 de sabor, tabelas de duas colunas), `mestre\protecao.py` (2ª coluna das
  tabelas), `mestre\aba_inicio.py` (índice), `mestre\exemplo.py`, `oraculo_mestre.py`, `testar_mestre.py`
  (`sabor`, `fase2`), `mestre\testes_*.py` (ganchos da fase), `mestre_lexico_extra.txt`.

## O que cada aba faz
- **NPCs (R5):** gerador G = 200 — Raça (Sortear ou escolhida), nome + sobrenome pela cultura (05; montagem por
  cultura: Xianzhouíta família primeiro, Avginiano "do clã", Intellitron "que se chama"), Caminho (06.3; Nenhum ×3,
  27.12, H11), ocupação, aparência (2 traços sem repetir, H25), personalidade, motivação (por Caminho, 27.12, ou
  geral), segredo, maneirismo/voz, atitude (H11), gancho (27.18 da faixa ou tabela, 50/50 H20), papel. Bloco de
  combate opcional = âncoras de 28.3 (o mesmo número do Criador de Inimigos no modo Faixa) e o caminho para levá-lo
  à aba Inimigos. Linha de saída em 4 partes na ordem do Elenco (D6); Elenco de 30 NPCs em 5 sub-tabelas (D11,
  cabeçalho a cada 10); avisos de nome repetido e de nome igual a criatura; 4 cartões (A4 paisagem).
- **Aventuras (R6):** G = 300 — tipo, gancho (H20), contratante (facção ≠ a do conflito, ocupação e nome pela
  cultura), objetivo por tipo, local (lugares de 27.17 que servem à faixa ou tabela, H26), facção do conflito
  (27.16), antagonista (Boss da facção na faixa → Elite da facção → Boss da faixa, H22, pelas fichas de 27.16),
  complicação, reviravolta, prazo (27.7 abre a lista), recompensa (verba 24.5 da faixa da aventura + equipamento de
  faixa 25.1 + 1 consumível de 24.3, H9 + pista; não lê a aba Recompensas). 5 cenas (H14): DT Média/Difícil da faixa
  do desafio (27.2), orçamento 50% e 100% (27.4; H5 com grupo ≠ 4), "objetivo que não seja matar" de 27.7. Linha
  de saída na ordem de Missões.
- **Recompensas (R7):** entrega de marco por regra (sem sorteio): verba de marco (24.5), Cone máximo e Bônus Maior
  (25.1, 25.2), Tier (viradas 7, 13, 18 — 25.1/25.3), Ressonância (26.7), ritmo (26.1), Sobreposição (≤ 1 por faixa,
  teto pelo Nível do Cone, por PJ a partir da aba Grupo), slot novo, o que não dar (27.8), preços de 24.1–24.3.
  Achados G = 400 (créditos H18, 0–2 consumíveis H9, bugiganga, pista) com linha de saída na ordem do Tesouro;
  sabor de Cone G = 410 (números de 25.2 pelo Nível da faixa) e de Conjunto G = 420 (opções de 25.3); Relíquias
  por Tier e o Tier do grupo; Tesouro de 25 linhas com saldo e aviso de saldo negativo.

## Heurísticas (rotuladas "Sugestão da planilha — não é regra do livro (H#)")
- Usadas na fase: H5, H9, H11, H14, H17 (relação −3…+3 do Elenco), H18, H20, H22, H25 e **H26 (nova)**.
- **H26 (nova, não estava no design):** (a) o contratante é de uma facção de 27.16 diferente da do conflito;
  (b) o local vem 50/50 dos lugares de 27.17 que servem à faixa ou da tabela de sabor; (c) "Faixa alta" de
  Ferro-Vazio (27.17) = faixas 13-16 e 17-20; lugar sem faixa no livro serve a qualquer faixa. Validação
  (`oraculo`): contratante nunca da facção do conflito em 200 rolagens; lugar do livro só na faixa que o livro diz
  em 400 rolagens; a tabela `locais_faixa` conferida contra o .md (`dados`).
- **Tesouro por nível (L6, sem regra no livro) = H18 + H9.** Créditos achados = INT(verba de marco da faixa ×
  5/10/15%) por leitura Passagem/Típico/Pesado; 0–2 consumíveis de 24.3 (poção Pequena 1-8, Média 5-16, Grande
  13-20). Erro máximo de arredondamento do INT: 0 Cr (as verbas de 24.5 são múltiplas de 20). Teto informativo:
  num nível com o ritmo de 26.1 (até 4 sessões × 3 combates de 27.7), os achados somam até 12 × 15% = 180% da verba
  — o livro diz que nada no balanceamento depende de Créditos (24.5). Validação: créditos ≤ 15% e inteiros (300
  casos); quantidade 0/1/2 entre 28% e 39% em 3 000 rolagens; todo item com o preço de 24.3; poção sempre da faixa.

## Decisões de implementação
- Tabelas de duas colunas (motivação por Caminho, objetivo por tipo) seguem a convenção do "ambiente por facção" da
  Fase 1: 1ª coluna chave, 2ª valor, contador corrido condicionado à chave (`historia.contador_chave`), com as
  linhas de cabeçalho repetido fora da contagem. A 2ª coluna também passa pela camada de leitura do Google.
- Listas suspensas de Tipo e Facção da aba Aventuras leem as vagas da aba Tabelas (coluna oculta com "Sortear"),
  então o Mestre pode ampliar as listas.
- Bônus Maior do sabor de Cone: as 6 escolhas de 25.2 abertas em 10 (as três categorias de Dano e os três tipos
  de Teste viram itens próprios); a suíte `dados` confere cada item contra o texto de 25.2.
- `Nao` (nome Vulpes) foi trocado por `Nagi`: a suíte `texto` reprova "Nao" como forma sem acento.
- Nomes: lista do teste com 131 nomes do jogo (palavra, sequência e pedaço colado de 5+ letras nas listas de
  nomes); 3 trocas na escrita: "Evaluna" (continha "lunae" com o sobrenome), "Bolanxin"/"Haoranbo" (curtos para
  Vidyadhara). "Saber" e outras palavras comuns do português só contam como nome nas listas de nomes.
- Exemplo (§14): 6 NPCs no Elenco = saídas do gerador nas Rolagens 1–6 (pelo oráculo, que a suíte confere contra a
  planilha), com onde está / relação / sessão e uma nota editada à mão; 4 cartões; marco do nível 2 (Subiu de
  nível); Tesouro com 200 Cr de verba e 1 Poção Pequena.

## Adoção da v1.2 (decisão do usuário, 07/10/2026)
O livro passou para a v1.2 em 05–07/10 (outro trabalho; changelog `00-changelog-v11-para-v12.md`, E1–E35). O usuário
mandou adotar a v1.2 em toda a Planilha do Mestre. O trabalho paralelo da v1.2 (`.agents\tasks\v12\`) já tinha
mexido em parte dos arquivos da Mestre (versão, nome de saída, E4/E3/E7/E15/E16 nas transcrições); esta iteração
conferiu, completou e regenerou sobre o livro atual (05, 04 e 22 mudaram de novo em 07/10, depois da última geração).

Changelog × Mestre, item a item:
| Item | Toca a Mestre? | O que foi feito |
|---|---|---|
| E1, E2, E5, E6 (propriedades de arma, 18.7, 24.7, 27.9) | Não: a Mestre não mostra propriedades de arma | — |
| E3 (24.2 Leve, Espaço 0,5) | Sim (aba Dados, preços da aba Recompensas, oráculo) | Dados lê `ficha_dados.armas()`; `oraculo_mestre_hist.ARMAS` com 0,5 |
| E4 (24.3 Munição, "Para quê") | Sim | Dados lê o livro; `oraculo_mestre_hist.ITENS` com o texto novo |
| E7 (Choque 3 turnos) | Sim (Combate C5b e aba Dados 21.5) | `aba_combate_inimigos.py` e `oraculo_mestre_cmb.py` com 3 turnos; a duração de 21.5 vem do livro |
| E8, E9 (20.1, Cisalhamento) | Só texto lido do livro (Dados, efeito de Quebra) | regenerado; nenhum número mudou |
| E10, E20–E34 (05 reescrito) | Sim: aba Dados `racas`, Grupo G4 e o Exemplo | Dados relê 05; G4 "Lembrete da Raça" ganhou Maré que Volta (Vidyadhara), Não Foi a Primeira Vez (Avginiano) e a falha do To na sua mente que só gasta o uso (E25); Morrendo com Vantagem, Executado, Esforço e Descobre Fraqueza conferem com a v1.2 (E27 mantém o Vulpes em 23.5). O Exemplo continua válido no `oraculo_ficha` v1.2 |
| E11–E13, E17–E19 (Habilidades, Ultimate, Memoespírito) | Não: a Mestre não modela Habilidade nem Memoespírito de PJ | E19 (nota do Autômato de Guerra, cap. 28) é texto de nota, não de ação: bestiário 32/32 |
| E14 (25.2: trocar o Cone é opcional) | Sim (Recompensas, entrega de marco) | a linha do Cone na faixa nova diz "Trocar é opcional: Nível maior não é automaticamente melhor (25.2)"; oráculo igual |
| E15, E16 (26.7 cabeçalho e Ressonância IV) | Sim | bloco Dados "O que ela dá"; `oraculo_mestre_hist.RESSONANCIAS` com o texto novo da IV |
| E29 (22.6) e E35 (ficha) | Não | — |

Entregáveis: o modelo agora é `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx` (`nucleo.SAIDA_MODELO`;
títulos das abas "… — Explorando Galáxias v1.2", de `gerar_ficha.VERSAO`), gravado por `gerar_mestre.py` por cima
do arquivo de mesmo nome; o Exemplo segue `Planilha do Mestre - Exemplo.xlsx`. O `…V1.1.xlsx` fica como registro
(o changelog da v1.2 diz isso). Os `.gsheet` são do usuário e ficam fora de tudo.

Linha de base (07/10/2026 16:51): `baseline-hashes.json` regravado com os hashes atuais: os 14 arquivos da ficha
(nenhum mudou desde a regravação do trabalho da v1.2, 15:22) **mais** o livro v1.2 (os 34 `.md` de `livro-v1.0\`,
o DOCX e o PDF V1.2) e a ficha V1.2 — `protegidos` passa a conferir o livro também pelo lado da Mestre (165
checagens). A v1.1 está em `baseline-hashes-v11.json`; a imediatamente anterior em
`baseline-hashes-antes-adocao-v12-mestre.json`. `ficha_protegidos.json` e os arquivos da ficha não foram editados.

Léxico: 9 palavras saíram de `mestre_lexico_extra.txt` porque a v1.2 do livro passou a usá-las (aba, abas, data,
deserto, marcador, opostos, recuperar, sobreviver, voo).

`extremos` (falha do teste na iteração 1): `mestre\paralelo.py` preenche as vagas pré-preenchidas da aba Tabelas com
o valor do arquivo, não com "" — reconfirmado na bateria v1.2.

Visto de passagem (para o pedido novo de Memoespírito e condições): a aba Combate (C7) já tem 48 linhas de condição,
uma condição por linha, cada uma com combatente (PJ ou inimigo), condição de 21.5, turnos restantes, acúmulos e quem
aplicou — vários por combatente ao somar linhas; não há painel de resumo por combatente nem Memoespírito na Fila.

## Achados do livro nesta fase (o livro não muda)
- 25.1 × 25.3 consistentes ("virando Tier II no nível 7" e "Tier IV no 18" são as fronteiras de 25.3).
- 27.17 só dá faixa a Poço Sete (1-4), Hesperin (17-20) e Ferro-Vazio ("Faixa alta", sem número): H26 (c).
- 27.9 (Ultimate por faixa) não aparece nas abas da Fase 2: fica para o Escudo (Fase 3).

## Iteração 2 (revisão `review-fase2.json`)
- **F1 (teto do Cone na Situação, 25.2).** 25.2 fixa dois limites independentes: no máximo 1 Sobreposição por faixa
  e o teto do Cone (2 no Nível 1–2, 1 no 3–4, 0 no 5), que conta as recebidas em faixas anteriores (trocar o Cone é
  opcional, E14). Antes a planilha só guardava as "desta faixa".
  - Grupo G3 ganhou a entrada F "Total no Cone" (`grupo.pjN.sobrep_total`, 0–5, as do Cone atual, com as desta
    faixa); Ressonâncias passou de F:J para G:J. O aviso de G3 acende "Acima do teto do Cone (25.2): o Nível N
    aceita até T" e "Total no Cone menor que as desta faixa".
  - Recompensas: cabeçalho "Sobreposições do grupo (25.2: no máximo 1 por faixa; o teto é do Cone; …)", colunas
    "Nesta faixa (máx. 1)", "No Cone (total)" (`recompensas.sob.N.total` = máx(total informado, desta faixa)) e
    "Teto do Cone". A Situação compara o total com o teto antes do limite da faixa: "Cone no teto (+3) com as que
    já tem: nenhuma a mais (25.2)"; o aviso acende acima do teto. A regra da entrega de marco diz "o teto é do Cone
    e conta as de faixas anteriores".
  - Oráculo (`oraculo_mestre_hist`) igual; `ouro` com Cone 3/4 + 1 anterior e Cone 1/2 + 2 anteriores → "no teto",
    Cone 1 + 1, 2 + 0, 3 + 0 → "Pode receber 1", acima do teto (3 + 2, 1 + 3, 5 + 1) nas duas abas e total menor
    que as desta faixa; os casos aleatórios do `oraculo` sorteiam também o total (0–3 e texto).
- **F2 (27.9 fora do `ouro`).** Decisão registrada no plano (2.4 e 3.3): 27.9 só aparece no Escudo (design §6.15),
  e o `ouro` da Fase 3 o cobre.
- `testar_mestre.py`: o duplicador de `--saida` não dá mais flush no arquivo já fechado (a mensagem "Exception
  ignored … I/O operation on closed file" no fim da bateria).
