# Notas do Orquestrador

> **PROJETO INTERROMPIDO em 03/10/2026 ~20:45** por esgotamento de cota do plano
> kiro.dev do usuário (910.63 / 1000).
>
> **➡️ LEIA PRIMEIRO: `HANDOFF-RETOMADA-v1.0.md` na raiz do workspace.**
> Esse é o documento de retomada completo e autossuficiente. Este arquivo aqui é
> apenas o registro bruto de decisões e incidentes.

Runs: wf_a39197a8faab22be (ABORTADO no teto do loop de design) →
wf_cfdc2530c4b2fa10 (ABORTADO a pedido do usuário, por cota).

Arquivo de controle do orquestrador. Não faz parte do livro. Serve para não perder
decisões do usuário entre turnos e entre passos do workflow.

## OVERRIDE ATIVO DO USUÁRIO

**O sistema vai do NÍVEL 1 AO 20.**

Decidido pelo usuário depois que o workflow já havia sido gerado. Os prompts dos passos
`plan`, `write`, `review-mecanica`, `review-conteudo`, `aggregate` e `verify` foram
baked com a frase "Faixa de níveis: 1 a 10 (como na v0.1)" e portanto estão
**obsoletos nesse ponto**. Qualquer passo que mencionar 1 a 10 deve ser corrigido.

Injetado em:

- [x] `design` (sess_047a68ac-711e-46b7-ae5e-2d46dfaf7ae9) — enviado via send_message
      com as 10 consequências de design detalhadas.
- [ ] `plan` — reinjetar quando o passo iniciar
- [ ] `write` (cada iteração do build-loop) — reinjetar
- [ ] `review-mecanica` / `review-conteudo` — reinjetar, senão podem reprovar
      conteúdo correto de 1-20 por conflito com o prompt deles de 1-10
- [ ] `verify` — reinjetar, mesma razão

## Consequências de 1-20 que precisam sobreviver até o fim

1. Curva de Eficiência reespaçada até 20 (a da v0.1 acelera e não estende: daria +16)
2. Nível de desbloqueio da Eficácia revisto (era 5, que em 1-20 é começo de jogo)
3. Níveis de Habilidade: expandir além de 1-5 ou reespaçar os desbloqueios até 20
4. Teto na quantidade de Habilidades (a fórmula da v0.1 daria 20 no nível 20)
5. Cadência de Bênçãos por Caminho + mover o capstone "Avatar" (era requisito nível 5).
   Se a cadência exigir mais de 10 Bênçãos, vale para TODOS os 9 Caminhos.
6. PV no nível 20 (25d20 ~262 para Destruição) somado ao conserto da oscilação
7. Apêndice de balanceamento cobrindo as faixas 1-4, 5-8, 9-12, 13-16, 17-20,
   mantendo o alvo de combate em 3-5 rodadas em TODAS as faixas
8. Tabela de DT ancorada na inflação de bônus do fim de jogo
9. Bestiário com Comum/Elite/Boss em todas as faixas até 20
10. Cones de Luz / Relíquias / Eidolons com progressão espalhada pelos 20 níveis

## Outras decisões já confirmadas com o usuário

- Nome do sistema: **Explorando Galáxias** (mantido; a v0.1 dizia "provavelmente vou
  mudar o nome" — remover esse parêntese na v1.0)
- Autoria: MC Filhos
- Idioma: PT-BR
- Saída: Markdown por capítulo em `livro-v1.0\` + `Sistema de HSR by MC Filhos V1.0.docx`
  + script reproduzível `build\gerar_docx.py`

## Histórico de incidentes do run

- Geração inicial falhou na validação: o creator usou o agente inexistente `wf-reviewer`.
  Relançado com a lista de agentes válidos explicitada. Run válido: wf_a39197a8faab22be.
- Run pausou uma vez por "Interrupted by agent restart"; retomado com
  update_workflow status=running. Nenhum trabalho perdido (o passo mantém a sessão).
- **wf_a39197a8faab22be ABORTOU** no loop de design: `maxIterations: 3` com
  `onMaxIterations: "abort"`. As 3 iterações de design rodaram e melhoraram muito
  (41 achados → 26 → 26), mas o revisor nunca emitiu APPROVED, então o loop estourou
  e abortou o run inteiro. O `plan` e o loop de escrita nunca executaram.
  Causa raiz: revisor que re-deriva a matemática inteira a cada passada sempre acha
  uma camada mais profunda; combinado com `abort`, isso destrói o run.
  **Lição aplicada no run novo: nenhum loop usa "abort". Design-fix usa "continue",
  loop de escrita usa "pause" (recuperável por mim com extend_repeat).**
- Artefatos do run abortado preservados antes do relançamento:
  `design-iter3.md` (226 KB, 2.036 linhas), `design-review-iter3.json` (30 KB,
  26 achados com fix prescrito), `design-review-iter3.md` (51 KB).

## Estado do design na virada de run

O design.md de 2.036 linhas JÁ FECHOU: ordem de turno (Velocidade/Ciclo/casas),
acerto crítico, Teste de Ataque, Vantagem/Desvantagem, RD, descanso, Pontos de
Habilidade (PH), potência da Ultimate por Nível equivalente, estrutura de 31
capítulos, mapa de imagens (capa = image11.png), e o apêndice de balanceamento com
DPC e PV de inimigos derivados nas 5 faixas (1-4, 5-8, 9-12, 13-16, 17-20).

Os 4 HIGH que restaram, todos com correção numérica já prescrita pelo revisor:
1. Redução de Tenacidade derivada a 100% de acerto → republicar com taxa de acerto
   (Boss 10/11/12/12/13, Elite 5/6/7/6/7, Comum 3/3/4/4/4)
2. Resolução por Teste de Resistência do alvo sem resultado definido quando o alvo
   PASSA, e ficha de inimigo sem bônus de Teste de Resistência → metade do dano sem
   efeito secundário + publicar a coluna que falta
3. Dano do inimigo igual para Comum/Elite/Boss → repartir em 1/3, 2/3, 1
4. Ressonância I furando a economia de PH (+48% de DPC na faixa 17-20)

## Fase pós-livro (04/10/2026)

- **Livro v1.0 concluído**: wf_82958fe6e7d903ee (escrita, 32 .md + .docx) e
  wf_1816ff0fdf5cf1a0 (PDF, 250 páginas, aprovado). Usuário trocou de conta, cota OK.
- **Run ativo: `wf_f4c2390f834ea13d`**: ficha de personagem automatizada (.xlsx para
  Google Planilhas) + auditoria completa. Saída em `ficha-automatizada\`, gerador em
  `build\gerar_ficha.py`, testes em `build\testar_ficha.py`.
  Decisões: .xlsx via openpyxl (não dá para criar Planilha Google nativa daqui; a pasta
  sincroniza com o Drive), sem Apps Script, fórmulas em inglês canônico com vírgula
  (o Google traduz para PT na importação), livro NÃO pode ser alterado (inconsistências
  vão para o relatório). Escopo: ficha do jogador. Ferramenta separada do mestre
  (Fila de Ação + bestiário) foi oferecida ao usuário como próximo passo, não incluída.

- **wf_f4c2390f834ea13d FALHOU na FEAT-004** (auditoria final). Causa: limite técnico
  da API de imagem (no máximo 2000 px por lado quando várias imagens vão na mesma
  requisição). O `renderizar_ficha.py` gerava PNG da aba inteira (até 2943×6001) e o
  agente abriu essas imagens. FEAT-001 a 003 concluídas, com testes passando (lint
  6.174/0, extremos 856/0, ouro 466, dados 3.297, livro intacto).
  O plano também deixou de fora 4 entregáveis pedidos: a pasta `ficha-automatizada\`,
  a ficha de exemplo preenchida, a auditoria visível ao usuário e o guia do Google.
  O `.xlsx` foi parar na raiz com outro nome.
- **Run ativo: `wf_f5844c6597dfe7c1`**: continuação a partir do disco. Regra
  nova: recortes ≤1800 px, no máximo 4 imagens por vez, nunca abrir os PNG antigos.
  Recupera os 4 entregáveis que faltaram.
  **Lição para briefs futuros: qualquer passo que renderiza e abre imagem precisa
  receber o limite de tamanho no prompt.**

- **Usuário pediu a v1.1**: corrigir as inconsistências no livro e na ficha, gastando
  o mínimo de créditos. Em vez de parar o run ou abrir outro, usei `replace_remaining`
  no `wf_f5844c6597dfe7c1` e troquei o que vinha depois da FEAT-004 (que segue rodando
  e gera a lista final de inconsistências). Passos novos: `livro-v11` (corrige D1..Dn,
  versão 1.1, changelog v1.0→v1.1, diff para o revisor, rebuild do docx/pdf) →
  `ficha-v11` (nova linha de base de protegidos, ajuste ao livro, entregáveis V1.1) →
  loop com 1 revisor e no máximo 2 voltas, `pause` → `final-v11`.
  Decisões tomadas por mim (o usuário pode vetar): D1 corrigir o exemplo; D3 Vulpes e
  Avginiano também ganham Vantagem no Teste de Morrendo (segue o texto de 05 + 22.1);
  D2, D4, D5, D6 e D7 são só esclarecimento de texto. A pasta `livro-v1.0\` mantém o
  nome (histórico) para não mexer em todos os scripts.

- **wf_f5844c6597dfe7c1 abortado por cota** (930.95/1000) no meio do `ficha-v11`.
  Handoff reescrito. O usuário recarregou +1000 créditos e pediu para ir até o fim.
- **Run ativo: `wf_109b35b843b0aaa2`**, a partir de `.kiro\workflows\concluir-v11.workflow.json`
  (escrito à mão, sem criador, sem loop): concluir-ficha-v11 (wf-coder, executa a
  seção 6 do handoff) → revisar-v11 (semantic_reviewer, 1 volta) →
  corrigir-e-finalizar (wf-coder, corrige, verifica e marca o handoff como concluído).

- **Novos pedidos do usuário (durante o passo concluir-ficha-v11 do wf_109b35b843b0aaa2):**
  (1) "Resumo para o Mestre" → "Resumo para o Jogador" (a ficha é dos jogadores);
  (2) tirar o congelamento de todas as abas, com células visualmente distintas no lugar;
  (3) auditoria final visual: organização, visibilidade para quem preenche, tamanho das células.
  Usei `replace_remaining` e troquei os 2 passos pendentes por 4: layout-sem-congelar →
  revisar-ficha-final → corrigir-revisao → auditoria-visual-final.
  Critérios que defini: abas do jogador ≤ 1360 px de largura, colunas auxiliares ocultas,
  nenhuma linha a mais de 15 linhas do cabeçalho da tabela, 4º estado "pior-caso" no
  renderizador, nova `--suite visual` (folga de 10%, lista suspensa ≥ opção mais longa + 24 px,
  rótulo em toda entrada, fonte ≥ 9 pt, contraste ≥ 4,5:1).
  O arquivo `.kiro\workflows\concluir-v11.workflow.json` NÃO foi atualizado: ele mostra os 3
  passos originais. Os passos que valem são os do run.

- **wf_109b35b843b0aaa2 CONCLUÍDO (04/10).** `--suite tudo` = 0 nas 10 suítes (oráculo: 247 casos,
  43.712 saídas, 0 divergência; visual: 23.898 checagens, 0 texto que não coube nos 4 estados).
  A revisão aprovou, com 6 achados não bloqueantes, todos tratados. O livro V1.1 foi regerado
  no passo 4 (texto corrido de 01.6 e 27.19). Conferi por conta própria: nenhuma aba congelada,
  Em Jogo!A1 = "Resumo para o Jogador", "Resumo para o Mestre" não aparece em lugar nenhum, e
  o recorte do pior caso da Em Jogo está legível.
  O arquivo `ficha-automatizada\explorando galaxias ficha teste mc filhos.xlsx` é do usuário
  (19:23, exportado do Google) e é a versão ANTIGA: tem "Resumo para o Mestre" e 9 abas
  congeladas. Não foi mexido.
  Em aberto, só cosmético: a seção 10.4 da AUDITORIA; números alinhados à direita encostados
  em texto alinhado à esquerda na tabela de Ataque Básico da Em Jogo ("8 7d10+11 (49)");
  a entrada do Memoespírito (H7) continua amarela fora da Recordação.

- **Bug grave no Google (04/10, noite):** o usuário editou a ficha V1.1 no Google Planilhas e viu
  "erros em todo lugar". Diagnóstico feito por mim nos exports do Google que ele deixou na pasta:
  261 células com `#ERROR!` e UMA raiz, Criação!B26. A opção "+1 em dois" (Humano) começa com "+",
  e o Google lê como fórmula `=+1 em dois`. O erro se espalha porque as fórmulas leem as entradas
  direto. 11 listas têm o mesmo defeito (Criação!B26, Progressão!C57:C62 e C67, Equipamento!C45:C47).
  A "Cópia de ..." do usuário (Haloviano) tem 0 erros: prova de que as fórmulas funcionam no Google.
  **As 10 suítes não pegaram** porque gravam as entradas por programa e nunca simulam a digitação no
  Google. Lição: testar contra os valores que o Google calcula, e nenhuma fórmula pode ler uma entrada
  sem proteção.
  Backup dos exports do usuário: `.agents\tasks\backup-usuario-0410\`.
- **Run ativo: `wf_fd7515ce8085fd7d`**, a partir de `.kiro\workflows\corrigir-erros-google.workflow.json`
  (3 passos): corrigir-ficha → revisar-correcao → fechar. Escopo: rótulos sem "+", leitura protegida
  de toda entrada, contador de erros na Início, suíte nova `google` (compara com os 2.363 valores que o
  Google gravou no export) e o caso do usuário reproduzido.

- **wf_fd7515ce8085fd7d CONCLUÍDO (05/10 ~09:14), revisão 2 da ficha.** A revisão aprovou, com 2
  achados baixos. Na suíte nova `google`, 2.363 de 2.363 células batem com os valores que o Google
  calculou. 358 entradas passam por 333 células ocultas de leitura protegida. Contador de erros em
  Início!B19 e dica do apóstrofo em Início!A7.
  **Conferi por conta própria** (no modelo em branco): 196 listas, nenhuma opção de risco, com o
  mesmo método que achou as 11 listas antes; rótulos novos nas 4 listas que quebravam; nenhuma aba
  congelada; Em Jogo!A1 = "Resumo para o Jogador".
  Detalhe do ambiente: `openpyxl.load_workbook` direto do G: (Google Drive) travou o shell duas
  vezes (exit -1). Copiar para `$env:TEMP` antes resolveu.
- **SESSÃO PARALELA ATIVA (não é minha): "Planilha do Mestre"**, em `Mestre\`,
  `build\*mestre*.py` e `.agents\tasks\mestre\`. Três processos python rodando às 09:18.
  Ela importa `gerar_ficha` e `ficha_dados`. A `baseline-hashes.json` dela (04/10 23:24) é de antes
  da revisão 2: 10 arquivos mudaram (exatamente os da revisão 2) e a "Cópia de Ficha..." sumiu.
  É o "bloqueio externo" das `notas-fase1.md` dela.
  A Planilha do Mestre tem 15 listas na aba Inimigos (G11 em diante) com opções "1-4", "5-8" e
  "9-12", que o Google pode converter em data. Não mexi: está avisado ao usuário, com uma mensagem
  pronta para ele mandar ao outro chat.
- A "Cópia de Ficha..." do usuário sumiu de `ficha-automatizada\` entre 23:24 e ~08:00. Os geradores
  e os testes não apagam arquivos dessa pasta (conferido por grep). Há backup em
  `.agents\tasks\backup-usuario-0410\`.

- **05/10, pedido "pode apagar os backups da ficha"** (o usuário apagou a Cópia de propósito).
  A pasta `backup-usuario-0410` foi apagada. Os 2 exports do Google foram MOVIDOS (não apagados)
  para `build\google_rev1\`, como `export-google-haloviano-0-erros.xlsx` e
  `export-google-humano-261-erros.xlsx`, porque a suíte `google` depende deles. `testar_ficha.py`
  e a AUDITORIA (seções 11.3 e 11.4) foram atualizados.
  **PAUSA pedida pelo usuário** antes de confirmar com `--suite google`. O passo pendente está no
  topo do HANDOFF.
  O usuário reorganizou a pasta: o HANDOFF agora está em `versões antigas\HANDOFF-RETOMADA-v1.0.md`,
  com o bloco PAUSA no topo. Na raiz ficaram o livro V1.1 e `Marcos Filho - Explorando Galáxias
  V1.1.gsheet`, a planilha Google dele. Às 09:46 nenhum processo meu estava rodando. A sessão do
  Mestre rodava `testar_mestre.py --suite oraculo` com 7 processos; não mexi.
- **05/10 09:50: retomado e concluído.** `--suite google` passou com os exports em
  `build\google_rev1\` (4.734 checagens, 0 falha, 2.363/2.363 nas duas revisões, caso do usuário com
  0 erros, 40,5 s). Lição do ambiente: comando em primeiro plano demorado volta com "^C" e exit -1,
  mas o processo filho (Start-Process) termina sozinho. Ler o arquivo de saída depois.
  A única planilha Google do projeto, `Marcos Filho - Explorando Galáxias V1.1.gsheet`, é de 04/10
  23:18, anterior à revisão 2: avisei o usuário e ofereci migrar o personagem a partir de um export.
