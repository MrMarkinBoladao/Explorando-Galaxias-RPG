# Plano de Escrita — Explorando Galáxias v1.0

**Fonte de verdade:** `.agents/tasks/design.md` (2.154 linhas, 27 seções, aprovado — idêntico byte a byte a `design-APROVADO.md`).
**Fonte de fidelidade de tom, nomes e Bênçãos herdadas:** `.agents/tasks/v01-extraido.txt`.
**Contexto e checklists de escopo:** `HANDOFF-RETOMADA-v1.0.md`, seções 7, 8, 9, 12 e 13.

Este documento é o mapa `capítulo → arquivo → bloco → seções do design`. Ele **não** reabre decisão mecânica nenhuma. Onde o design deixou um buraco de alocação editorial (não de mecânica), a decisão está registrada em "Decisões de planejamento", abaixo, com uma ou duas linhas de motivo.

---

## Invariantes deste run (valem em todos os 31 arquivos)

1. **A faixa do sistema é nível 1 a 20.** Não é 1 a 10. A string `nível 1 a 10` é proibida pelo checador de nomenclatura (design 3.1) e só é tolerada em `00-*`, `01-*`, `30-*` ou em linha marcada com `<!-- termo-historico -->` (design 23). Nenhuma tabela pode parar no nível 10: progressão, Eficiência, Bênçãos, PV, DT, bestiário e equipamento vão até 20.
2. **Nenhum dos 9 Caminhos pode ficar com zero Bênçãos.** São **12 Bênçãos escritas por Caminho × 9 Caminhos = 108** (design 11.3): 60 nos cinco Caminhos da v0.1 (10 herdadas + 2 novas de tier alto cada) e 48 escritas do zero em Erudição, Euforia, Caça e Preservação. Aquisição nos níveis ímpares (1, 3, 5, 7, 9, 11, 13, 15, 17, 19) = 10 adquiridas de 12 escritas. Tiers: 6 sem requisito, 4 com nível 9+, 2 com nível 17+ (uma delas é o Avatar, que **exige nível 17**, não 5).
3. **São exatamente 31 arquivos** em `livro-v1.0/`, prefixo de 2 dígitos, kebab-case sem acento, UTF-8, GFM. A lista é a de design 20 e está reproduzida integralmente abaixo. Não se cria arquivo novo nem se renomeia nenhum.
4. **Idioma PT-BR**, segunda pessoa ("você"), tom direto e informal com exemplos (handoff 13), texto **100% original** — nada copiado de wiki ou do jogo.
5. **Toda régua numérica vem do design.** Médias de dados são `floor(nº de dados × (N+1)/2)`; arredondamento sempre para baixo; dano mínimo 1. Bênção herdada fora de escala passa pela régua de conversão de design 11.4, sem inventar número.

---

## Decisões de planejamento (buracos de alocação que eu fecho aqui)

- **D1 — Os 4 HIGH do review já estão resolvidos no `design.md`; não são tarefa desta escrita.** O handoff, seção 6, diz "sua primeira tarefa: os 4 HIGH" — essa seção é **anterior** à iteração 3 do design e está obsoleta. Conferido linha por linha no `design.md` atual: Tenacidade condicionada ao acerto e republicada (9.4, 18.1 linha 1493, 18.3 com Boss 10/11/12/12/13), alvo que passa no Teste de Resistência leva metade do dano sem efeito secundário mais a coluna de Teste de Resistência do inimigo (4.5 linha 250, 10.4 linha 1017, 18.3), Dano por acerto repartido em Comum 1/3 / Elite 2/3 / Boss 1 (18.1 linha 1497, 18.3), Ressonância I limitada a Habilidade de Nível 3 ou menor e Ressonância III cobrando o PH do Nível novo (16.5 linhas 1390-1396). A escrita **consome** esses números; não os re-deriva.
- **D2 — Ambientação não tem capítulo próprio e não vai ganhar um.** A lista de 31 arquivos está travada, e o design coloca cenário fora do escopo de *regras* (24). A ambientação exigida pelo pedido original (lacuna 17) é distribuída: **cosmologia dos Aeons e dos Caminhos, Stellaron, Fragmentum e o Expresso Astral** entram em `01-introducao.md` (seção "O universo") e em `06-caminhos-visao-geral.md` (os 9 Aeons como cosmologia prática); **facções, locais e ganchos** entram em `27-guia-do-mestre.md` como material de Mestre, com as fichas das facções no `28-bestiario.md`. Motivo: é o único arranjo que entrega a lacuna sem furar a estrutura aprovada.
- **D3 — O changelog completo mora em `01-introducao.md`, e esse capítulo é escrito por último.** O handoff pede um arquivo `00-changelog-...md`, que seria um 32º arquivo; o design manda o "o que mudou da v0.1" para o capítulo 01. Decide-se pelo design, com dois ganhos: `01-*` é um dos três arquivos **isentos** do checador da Coluna A (design 23), e o changelog *precisa* citar termos aposentados ("ação bônus", "DoT", "rodada") — num apêndice isso seria falha fatal de build. E ele só pode ficar completo depois que os outros 30 capítulos existirem, porque enumera cada desvio do que o autor escreveu. Daí a posição dele no fim do plano, apesar do número 01.
- **D4 — Créditos e Técnicas entram em `24-equipamentos.md`, em escala mínima.** O design manda "economia de créditos" para um suplemento (24), mas a lacuna 18 do pedido original pede Créditos. Entrega-se o mínimo coerente: uma tabela de preços de referência por faixa para o que o livro já lista (armas, armaduras, poções, itens) e as **Técnicas** como uso fora de combate, sem criar subsistema econômico. Regras de nave e viagem interestelar ficam declaradas fora de escopo no `01`.
- **D5 — Três dos cinco scripts de verificação do design 23 não existem ainda.** Em `scripts/` só existem `map-imagens.ps1` e `thumbs.ps1`. `checar-nomenclatura.ps1`, `checar-tabelas.ps1` e `simular-combate.ps1` são citados como gates do build e precisam ser escritos **antes** dos capítulos que eles guardam — são os itens 1, 2 e 32 deste plano. Acrescento um quarto, `checar-completude.ps1`, porque os dois invariantes de contrato com o usuário (faixa 1-20 e nenhum Caminho com zero Bênçãos) não são checados por nenhum script do design e são exatamente o tipo de coisa que se perde num livro de 31 arquivos.
- **D6 — Os capítulos 12 a 15 abrem com `<!-- ARTE PENDENTE: símbolo do Caminho -->`** (design 20.3). Não há arte para os 4 Caminhos novos, e isso não bloqueia a escrita.
- **D7 — Ambiente travado:** Windows, PowerShell 5.1 (`powershell.exe`; não existe `pwsh`), Python 3.14.7 com python-docx 1.2.0 instalado, **não é repositório git**, caminhos com espaço e acento sempre entre aspas duplas. Conferido na máquina.

---

## Mapa mestre: capítulo → arquivo → bloco → seções do design

Blocos conforme o brief: **A** núcleo de regras · **B** Caminhos e Bênçãos · **C** Habilidades e equipamento · **D** bestiário · **E** Guia do Mestre e ambientação · **F** apêndices.

| # | Arquivo (`livro-v1.0/`) | Bloco | Seções do `design.md` que o alimentam | Outras fontes |
|---|---|---|---|---|
| 00 | `00-capa-e-creditos.md` | A (abertura) | 2, 20, 20.3 (capa = `image11.png`) | nome oficial e autoria: `orquestrador-override.md` |
| 01 | `01-introducao.md` | **F** (escrito por último, ver D3) | 1, 11.1, 12, 20.1, 20.2, 21.1, 21.2, 24, 25 | v0.1 inteira; handoff 8 e 9; **ambientação** (D2) e **changelog** (D3) |
| 02 | `02-como-jogar.md` | A | 3.2, 4.1, 4.2, 4.3, 4.4, 18.4 (lista fechada das 5 DTs de subsistema), 19 | — |
| 03 | `03-criacao-de-personagem.md` | A | 5.1, 5.2, 9.1, 10.3, 11.1 (Atributo de Habilidade por Caminho), 12, 17, 19 | v0.1 (passo a passo, Propósito de Vida) |
| 04 | `04-atributos-e-pericias.md` | A | 4.3, 5.1, 5.2, 5.3, 5.4, 14 | v0.1 (6 Atributos e 18 Perícias, texto preservado) |
| 05 | `05-racas.md` | A | 12, 15.2 e 18.1 (Esforço, exclusivo do Humano), 20.3 (7 imagens de raça) | v0.1 (citações e características) |
| 06 | `06-caminhos-visao-geral.md` | B | 4.3, 6.1 (PV e índice N), 6.5 (Bônus de Velocidade), 11.1, 11.2, 11.3 | cosmologia dos Aeons (D2) |
| 07 | `07-caminho-destruicao.md` | B | 11.3, 11.4 (as três linhas de custo em PV e o Avatar), 9.6, 10.1, 20.3 (`image13`, `image9`) | v0.1: 10 Bênçãos da Destruição |
| 08 | `08-caminho-inexistencia.md` | B | 9.5 (Dano Contínuo), 9.6, 11.3, 11.4, 7.9, 20.3 (`image17`) | v0.1: 10 Bênçãos da Inexistência |
| 09 | `09-caminho-harmonia.md` | B | 7.4, 7.5 (Atrasar/Avançar), 11.3, 11.4, 8.2, 20.3 (`image4`, `image8`) | v0.1: 10 Bênçãos da Harmonia |
| 10 | `10-caminho-abundancia.md` | B | 11.3, 11.4, 15.3 (cura e PV temporários), 20.3 (`image1`, `image3`) | v0.1: 10 Bênçãos da Abundância |
| 11 | `11-caminho-recordacao.md` | B | 11.3, 11.4, **13.1, 13.2, 13.3 (Memoespírito)**, 7.3, 20.3 (`image10`, `image15`) | v0.1: 10 Bênçãos da Recordação |
| 12 | `12-caminho-erudicao.md` | B | 11.1, 11.2 (Acúmulos de Cálculo), 11.3, 10.1 (alvos em área), 9.6 | — (12 Bênçãos do zero) |
| 13 | `13-caminho-euforia.md` | B | 11.1, 11.2 (Tabela do Riso, d6), 11.3, 7.4, 7.5, 8.2 | — (12 Bênçãos do zero) |
| 14 | `14-caminho-caca.md` | B | 11.1, 11.2 (Marcação de Presa), 11.3, 4.6 (crítico 19-20, teto do jogo), 6.5 | — (12 Bênçãos do zero) |
| 15 | `15-caminho-preservacao.md` | B | 11.1, 11.2 (Barreira), 11.3, 6.3, 6.4, 8.1 (Reações), 15.3 | — (12 Bênçãos do zero) |
| 16 | `16-habilidades.md` | C | 10.1, 10.2, 10.3, 10.4, 8.2 (PH), 9.6, 18.1, 19 | v0.1 (criação de Habilidade) |
| 17 | `17-ultimate-e-energia.md` | C | 8.3, 8.5 (Nível equivalente), 10.1, 10.2, 19 | v0.1 (Ultimate a 100 de Energia) |
| 18 | `18-combate.md` | A | 4.5, 4.6, 6.2, 6.3, 6.4, 8.1, 8.4 (Distâncias), 9.1, 9.2, 16.2, 19 | v0.1 (ações e armas) |
| 19 | `19-fila-de-acao-e-velocidade.md` | A | 7.1 a 7.9 inteiras, 6.5, 9.6 (Congelamento), 19 | v0.1 ("derrubar o turno", normalizado em 7.9) |
| 20 | `20-elementos-tenacidade-e-quebra.md` | A | 9.1, 9.3, 9.4, 9.5, 18.3 (Tenacidade por tipo), 19 | v0.1 (7 Elementos, Fraquezas) |
| 21 | `21-condicoes.md` | A | 9.6 (catálogo), 9.5, 11.4 (Sangramento como exceção única), 19 | v0.1 (condições espalhadas) |
| 22 | `22-testes-de-resistencia.md` | A | 14, 4.5 (segunda via de resolução), 18.3 (coluna do inimigo), 18.4 | — |
| 23 | `23-dano-cura-e-morte.md` | A | 15.1 (Morrendo sem Eficiência, Executado), 15.2 (Descanso), 15.3, 6.4, 9.1, 19 | v0.1 (Executado, hoje no traço Xianzhouíta) |
| 24 | `24-equipamentos.md` | C | 16.1, 16.2, 15.4 (inventário e Espaço), 9.2 | **Créditos e Técnicas (D4)**; v0.1 (itens e poções) |
| 25 | `25-cones-de-luz-e-reliquias.md` | C | 16.3, 16.4, 17 (tier por faixa), 6.5 | — (subsistema inteiramente novo) |
| 26 | `26-progressao-e-ressonancias.md` | C | 17, 17.1, 4.3 (Eficácia e Especialização de Combate), 9.6 (os dois tetos), 16.5, 10.3, 19 | — |
| 27 | `27-guia-do-mestre.md` | E | 18.1 (17 premissas e o contrato de encontro da Fraqueza), 18.3, 18.4, 10.4, 16.3, 16.4, 17, 22.1, 19 | **facções, locais e ganchos (D2)**; handoff 8 item 16 |
| 28 | `28-bestiario.md` | D | 18.3 (as 13 colunas de âncora), 18.1, 18.5, 9.4, 9.6, 14 | facções da lacuna 15 do handoff |
| 29 | `29-apendices-e-fichas.md` | F | 18.1 a 18.5 (apêndice de balanceamento), 13.1 (ficha do Memoespírito), 7.8 (Trilha de Ação), 6.1 a 6.5, 5.2, 3.2 | saída de `simular-combate.ps1` |
| 30 | `30-glossario.md` | F | 3.1, 3.2 (termos oficiais e aposentados), 23 (isenção do checador), 19 | v0.1 (termos antigos) |

**Conferência de cobertura dos blocos do brief:** A = 00, 02, 03, 04, 05, 18, 19, 20, 21, 22, 23 · B = 06 a 15 (9 Caminhos, 108 Bênçãos, Memoespírito no 11) · C = 16, 17, 24, 25, 26 · D = 28 · E = 27 (+ a fatia de ambientação do 01 e do 06) · F = 01, 29, 30. Total: 31 arquivos, nenhum sem bloco, nenhum em dois blocos.

---

## Implementation Plan

Ordem por dependência. Cada item deixa `livro-v1.0/` num estado que passa os gates já existentes. Comandos sempre com caminho entre aspas duplas e `;` em vez de `&&`.

### Gates de verificação (antes de qualquer capítulo)

- [ ] 1. Escrever `scripts/checar-nomenclatura.ps1`: varre `livro-v1.0/*.md` buscando **só as 25 strings da Coluna A** de design 3.1, casamento insensível a maiúsculas e delimitado por `\b`, reportando arquivo, linha e termo. Implementar a válvula de design 23: ignorar `00-*`, `01-*`, `30-*` e qualquer linha com `<!-- termo-historico -->`. Aceitar `-Pasta` para apontar outra pasta (usado no autoteste). **Não** checar a Coluna B de 3.2.
      Files: `scripts/checar-nomenclatura.ps1`
      Verify: criar fixture em `"$env:TEMP\eg-fix"` com `05-x.md` contendo "ação bônus" e `01-x.md` contendo "HP"; `powershell -File "scripts\checar-nomenclatura.ps1" -Pasta "$env:TEMP\eg-fix"` sai com código 1 apontando só o `05-x.md`; `powershell -File "scripts\checar-nomenclatura.ps1"` em `livro-v1.0` vazia sai com código 0.

- [ ] 2. Escrever `scripts/checar-tabelas.ps1` conforme design 23: confere que toda média impressa de dano, cura e Ultimate é `floor(nº de dados × (N+1)/2)` (casos de referência `6d6=21`, `5d10=27`, `5d8=22`, `7d20=73`, `18d20=189`), que a tabela de Bônus de Atributo é monotônica não-decrescente, que a progressão 1-20 não tem nível vazio e que a coluna de Nível equivalente da Ultimate (8.5) aponta para linhas existentes em 10.1. Mesmo parâmetro `-Pasta`.
      Files: `scripts/checar-tabelas.ps1`
      Verify: fixture com uma linha `6d6` e média `18` (o erro da v0.1) faz o script sair com código 1 e imprimir esperado 21; corrigindo para 21 sai com código 0; rodando em `livro-v1.0` vazia sai com código 0.

- [ ] 3. Escrever `scripts/checar-completude.ps1` (gate dos dois invariantes de contrato, ver D5): falha se algum dos 9 arquivos de Caminho (`07-*` a `15-*`) tiver menos de 12 Bênçãos nomeadas; falha se faltar algum dos 31 arquivos esperados; falha em marcador de pendência (`TBD`, `a definir`, `farão juntamente`, `sujeito a mudanças`, `futuramente`, `provavelmente vou mudar o nome`, `ARTE PENDENTE` fora de `12-*` a `15-*`); falha se qualquer tabela de progressão, Eficiência, PV, DT ou bestiário parar no nível 10.
      Files: `scripts/checar-completude.ps1`
      Verify: `powershell -File "scripts\checar-completude.ps1"` com `livro-v1.0` vazia sai com código 1 listando os 31 arquivos ausentes (é o comportamento correto neste ponto); com fixture de um `07-x.md` de 12 Bênçãos o contador reporta 12.

### Bloco A — núcleo de regras

- [ ] 4. Escrever `00-capa-e-creditos.md`: título oficial **Explorando Galáxias**, autoria MC Filhos, versão 1.0, aviso de obra de fã sem fim comercial, capa referenciando `assets/imagens-v01/image11.png` por caminho relativo. Remover o parêntese "provavelmente vou mudar o nome" da v0.1.
      Files: `livro-v1.0/00-capa-e-creditos.md`
      Verify: `powershell -File "scripts\checar-nomenclatura.ps1"` sai com código 0.

- [ ] 5. Escrever `02-como-jogar.md`: a rolagem única (4.1), leitura de DT com os valores da faixa 1-4 e a **lista fechada das cinco DTs de subsistema** (4.2 + 18.4), Eficiência e Eficácia com a curva reespaçada para 1-20 (4.3), Vantagem e Desvantagem (4.4), arredondamento para baixo e dano mínimo 1, precedência de regras em 4 níveis, **falhe para frente** e a Regra de Ouro (3.2). É o capítulo dono dos invariantes "Eficácia nunca entra em Teste de Ataque", "dano mínimo 1" e "arredonda para baixo" (19).
      Files: `livro-v1.0/02-como-jogar.md`
      Verify: `powershell -File "scripts\checar-nomenclatura.ps1"; powershell -File "scripts\checar-tabelas.ps1"` — ambos com código 0 e a curva de Eficiência chegando ao nível 20.

- [ ] 6. Escrever `03-criacao-de-personagem.md`: passo a passo, array oficial `15, 14, 13, 12, 10, 8`, Compra de Pontos com 28 pontos (5.2), teto 15 na criação e 20 depois (invariante de 19), Propósito de Vida, Elemento (9.1), Atributo de Habilidade pela tabela de 11.1, e o ponteiro para o teto de 8 Habilidades (10.3).
      Files: `livro-v1.0/03-criacao-de-personagem.md`
      Verify: os dois gates acima com código 0; a tabela de Compra de Pontos soma 28 para o array oficial.

- [ ] 7. Escrever `04-atributos-e-pericias.md`: os 6 Atributos com o texto da v0.1 preservado, **tabela de Bônus de Atributo normalizada e monotônica** cobrindo até 20 (5.1), aumentos nos níveis 3, 6, 9, 12, 15 e 18 (5.3), as 18 Perícias com os três consertos de 5.4, Eficiência nos 6 Testes de Resistência desde o nível 1 (4.3).
      Files: `livro-v1.0/04-atributos-e-pericias.md`
      Verify: `powershell -File "scripts\checar-tabelas.ps1"` passa a checagem de monotonicidade do Bônus de Atributo; nomenclatura com código 0.

- [ ] 8. Escrever `05-racas.md`: as 7 Raças na ordem de apresentação padronizada de 12 (nome, citação, características, bônus de atributo, traços com regra fechada), com os consertos raça por raça, o **Esforço declarado exclusivo do Humano** e as 7 imagens do mapa de 20.3. Mover o Executado para fora do traço Xianzhouíta, deixando ponteiro para o capítulo 23.
      Files: `livro-v1.0/05-racas.md`
      Verify: nomenclatura e tabelas com código 0; as 7 referências de imagem resolvem para arquivos existentes em `assets/imagens-v01/`.

- [ ] 9. Escrever `18-combate.md`: as 4 Ações + Reação (8.1), Teste de Ataque formal com todas as parcelas e as **6 categorias de arma com o Atributo de cada** (4.5), crítico com teto 19-20 (4.6), Defesa (6.2), **Esquiva somando sempre Eficiência** (6.3), RD com teto `2 + (2 × Eficiência)` (6.4), dano e dados por categoria de arma (9.1, 9.2), Intervir, Distâncias (8.4), tabela de armas (16.2). Capítulo dono de três invariantes de 19.
      Files: `livro-v1.0/18-combate.md`
      Verify: nomenclatura e tabelas com código 0.

- [ ] 10. Escrever `19-fila-de-acao-e-velocidade.md`, o capítulo mais pesado do bloco: Velocidade como quinta estatística (6.5), montagem da Fila e gatilho de Surpresa com DT 13 fixa (7.3), Atrasar com teto de 3 casas contra Comum e 2 contra Elite/Boss e a **ordem de operação da Firmeza** (7.4), Avançar e Avanço Total 1 por Ciclo (7.5), Congelamento com Firmeza (7.6), os casos-limite de 7.7 todos resolvidos, a Trilha de Ação em papel (7.8) e a normalização das referências herdadas (7.9).
      Files: `livro-v1.0/19-fila-de-acao-e-velocidade.md`
      Verify: nomenclatura com código 0 (nenhuma ocorrência de `iniciativa`, `rodada`, `round`, `push back`, `action advance`); os 8 casos-limite de 7.7 aparecem respondidos.

- [ ] 11. Escrever `20-elementos-tenacidade-e-quebra.md`: os 7 Elementos, Fraquezas e Resistências (9.3), Tenacidade e Quebra com a fórmula **por tipo de inimigo** e os valores publicados de 18.3, Dano de Quebra sofrendo RD, Dano Contínuo com as três exceções numa frase (9.5), e a declaração de que **só inimigos têm Tenacidade** (19).
      Files: `livro-v1.0/20-elementos-tenacidade-e-quebra.md`
      Verify: nomenclatura e tabelas com código 0 (`stagger`, `poise`, `break`, `DoT` ausentes).

- [ ] 12. Escrever `21-condicoes.md`: catálogo completo de 9.6 com máximo de 5 acúmulos por condição, **Lentidão** com efeito de movimento definido, **Marcado** com conteúdo mecânico, e o Sangramento como exceção declarada da política de porcentagem de PV (11.4).
      Files: `livro-v1.0/21-condicoes.md`
      Verify: nomenclatura e tabelas com código 0; toda condição citada em 9.6 tem verbete.

- [ ] 13. Escrever `22-testes-de-resistencia.md`: os 6 Testes com os nomes fechados e seus atributos (14), quando o Mestre pede, a segunda via de resolução e **o que acontece quando o alvo passa** (4.5), e a DT contra a qual se rola, com a coluna de inimigo de 18.3.
      Files: `livro-v1.0/22-testes-de-resistencia.md`
      Verify: nomenclatura com código 0 (`salvaguarda`, `save`, `CD` ausentes).

- [ ] 14. Escrever `23-dano-cura-e-morte.md`: cura, PV temporários com teto `3 × Eficiência` de qualquer fonte (15.3), **Morrendo com Força de Vontade DT 10 sem Eficiência** como exceção declarada (15.1), Executado, Descanso Curto e Longo (15.2). Capítulo dono dos invariantes de PV temporário e do Teste de Morrendo (19).
      Files: `livro-v1.0/23-dano-cura-e-morte.md`
      Verify: nomenclatura e tabelas com código 0.

### Bloco B — os 9 Caminhos e as 108 Bênçãos

- [ ] 15. Escrever `06-caminhos-visao-geral.md`: os 9 Caminhos com Aeon, eixo, Atributo de Habilidade, as 3 Perícias com Eficiência, o índice de vitalidade N e o PV por nível até 20 (6.1), o Bônus de Velocidade (6.5), **como se lê uma Bênção** e a cadência de aquisição nos ímpares com os três tiers (11.3), mais a cosmologia dos Aeons em texto original (D2).
      Files: `livro-v1.0/06-caminhos-visao-geral.md`
      Verify: nomenclatura e tabelas com código 0; a tabela de PV vai até o nível 20 nos 9 Caminhos.

- [ ] 16. Escrever `07-caminho-destruicao.md`: 12 Bênçãos (as 10 da v0.1 reescritas pela régua de 11.4 + 2 novas nos tiers 9+ e 17+). Aplicar as três linhas novas de custo em PV (`2 × nível` e `5 × nível`), e o **Avatar da Destruição** com requisito nível 17, `5 × nível` PV por dado, teto de +2 dados por Ciclo e sujeito ao teto de dados adicionais de 9.6. Imagens `image13.png` e `image9.png`.
      Files: `livro-v1.0/07-caminho-destruicao.md`
      Verify: `powershell -File "scripts\checar-completude.ps1"` conta 12 Bênçãos neste arquivo; nomenclatura e tabelas com código 0; nenhuma Bênção expressa valor em porcentagem de PV máximo.

- [ ] 17. Escrever `08-caminho-inexistencia.md`: 12 Bênçãos, Corrupção, Dano Contínuo convertido para `1d6 + Eficiência` uma vez por turno do alvo, Implante de Fraqueza, "ação bônus" da v0.1 padronizada em **Ação Complementar**, "Teste de Resistência de Resistência Física" corrigido, acúmulo de penalidade preso ao teto de 9.6. Imagem `image17.png`.
      Files: `livro-v1.0/08-caminho-inexistencia.md`
      Verify: completude conta 12; nomenclatura com código 0 (`ação bônus` e `DoT` ausentes).

- [ ] 18. Escrever `09-caminho-harmonia.md`: 12 Bênçãos, Ritmo Acelerado, buffs de grupo dentro do teto de bônus somado (9.6), interações com Avançar e Atrasar apontando para o capítulo 19. Imagens `image4.png` e `image8.png`.
      Files: `livro-v1.0/09-caminho-harmonia.md`
      Verify: completude conta 12; nomenclatura e tabelas com código 0.

- [ ] 19. Escrever `10-caminho-abundancia.md`: 12 Bênçãos, cura convertida para `5 × nível` com teto de metade do PV máximo do alvo, barreira e PV temporários dentro do teto de 15.3, Excesso de Vida com `+2 RD`. Imagens `image1.png` e `image3.png`.
      Files: `livro-v1.0/10-caminho-abundancia.md`
      Verify: completude conta 12; tabelas com código 0 (médias de cura corrigidas: `5d8 = 22`, `7d20 = 73`).

- [ ] 20. Escrever `11-caminho-recordacao.md`: 12 Bênçãos + **Guia e ficha do Memoespírito** (13.1, 13.2, 13.3), com o Memoespírito ancorado no dono, agindo na Fila conforme 13.3, e `Ecos do Passado` convertido para `+PV máximo igual a 4 × nível do dono`. Imagens `image10.png` e `image15.png`.
      Files: `livro-v1.0/11-caminho-recordacao.md`
      Verify: completude conta 12; nomenclatura com código 0 (`memosprite` ausente); a ficha do Memoespírito tem todos os campos de 13.1.

- [ ] 21. Escrever `12-caminho-erudicao.md` do zero: identidade (Nous, área e multi-alvo), as 3 Perícias (Ciência, Pesquisa, Tecnologia), **Acúmulos de Cálculo** com os números de 11.2, e 12 Bênçãos nos três tiers respeitando a regra de alvos de 10.1 e o teto absoluto de 6 alvos. Abertura com `<!-- ARTE PENDENTE: símbolo do Caminho -->`.
      Files: `livro-v1.0/12-caminho-erudicao.md`
      Verify: completude conta 12 e aceita o marcador de arte neste arquivo; nomenclatura e tabelas com código 0; nenhuma Bênção passa de 6 alvos.

- [ ] 22. Escrever `13-caminho-euforia.md` do zero: identidade (Aha, caos controlado), Perícias (Enganação, Acrobacia, Persuasão), **Tabela do Riso** com as 6 entradas exatas de 11.2, 12 Bênçãos, nenhuma entrada aleatória passando de +2 ou 1 dado, interação com a Fila sempre respeitando a Firmeza.
      Files: `livro-v1.0/13-caminho-euforia.md`
      Verify: completude conta 12; a Tabela do Riso tem as 6 entradas de 11.2 sem alteração de valor.

- [ ] 23. Escrever `14-caminho-caca.md` do zero: identidade (Lan, alvo único e velocidade), Perícias (Furtividade, Percepção, Acrobacia), **faixa de crítico 19-20 declarada como teto do jogo**, **Marcação de Presa** com os números de 11.2, 12 Bênçãos, e a maior VEL do jogo conforme a calibração de 18.3.
      Files: `livro-v1.0/14-caminho-caca.md`
      Verify: completude conta 12; nenhuma Bênção amplia a faixa de crítico além de 19-20.

- [ ] 24. Escrever `15-caminho-preservacao.md` do zero: identidade (Qlipoth, escudos e proteção), Perícias (Resistência, Atletismo, Intuição), **Barreira** com as regras de 11.2 e o teto de 15.3, Reações defensivas extras dentro de 1 Reação por turno (8.1), 12 Bênçãos, RD sempre dentro do teto de 6.4.
      Files: `livro-v1.0/15-caminho-preservacao.md`
      Verify: completude conta 12 e **os 9 Caminhos passam a ter 12 cada (108 no total, nenhum com zero)** — este é o item que fecha o invariante 2; nomenclatura e tabelas com código 0.

### Bloco C — Habilidades e equipamento

- [ ] 25. Escrever `16-habilidades.md`: criação de Habilidade, Níveis 1 a 7 com as tabelas de dano, cura, alcance, buff, debuff e passiva (10.1, 10.2), **regra de área com número de alvos** (até 3, 4 nos Níveis 6 e 7, teto 6), custo e geração de PH por faixa condicionada ao acerto (8.2), teto de 8 Habilidades conhecidas e desbloqueio do Nível 2 no nível 2 (10.3), teto de dados adicionais (9.6), e o checklist de validação com a lista de efeitos proibidos (10.4). Capítulo dono dos invariantes de área e de PH (19).
      Files: `livro-v1.0/16-habilidades.md`
      Verify: `powershell -File "scripts\checar-tabelas.ps1"` confere todas as médias impressas dos Níveis 1 a 7; nomenclatura com código 0 (`skill points`, `SP`, `mana` ausentes).

- [ ] 26. Escrever `17-ultimate-e-energia.md`: Ultimate, 100 de Energia, fontes de Energia incluindo sofrer dano e derrotar inimigo, Energia ganha **na ação** e não no acerto, 1 Ultimate por Ciclo, **tabela de potência por faixa com o Nível equivalente** de 8.5, criação e validação da Ultimate. Depende do item 25 (as tabelas de 10.1 e 10.2 que o Nível equivalente indexa).
      Files: `livro-v1.0/17-ultimate-e-energia.md`
      Verify: `powershell -File "scripts\checar-tabelas.ps1"` confirma que cada Nível equivalente aponta para uma linha existente em `16-habilidades.md`; nomenclatura com código 0 (`ult charge` ausente).

- [ ] 27. Escrever `24-equipamentos.md`: armaduras e vestimentas com as penalidades calibradas na própria tabela (16.1), tabela completa de armas com dano, elemento, alcance, atributo, propriedades e redução de Tenacidade (16.2, 9.2), itens e poções, inventário e Espaço (15.4), criação de itens, mais **Créditos como preços de referência por faixa e Técnicas como uso fora de combate** (D4).
      Files: `livro-v1.0/24-equipamentos.md`
      Verify: nomenclatura e tabelas com código 0; a Armadura Pesada aparece com **2 RD** (não 10) e nenhuma arma excede os dados de 9.2.

- [ ] 28. Escrever `25-cones-de-luz-e-reliquias.md`: Cones de Luz com Sobreposição (16.3), 6 slots de Relíquia com Esfera Planar e Mãos declaradas disjuntas, conjuntos de 2 e 4 peças (16.4), e a **regra de aquisição** — tier por faixa concedido como recompensa de marco (16.3, 16.4, 17), que é o furo apontado no handoff.
      Files: `livro-v1.0/25-cones-de-luz-e-reliquias.md`
      Verify: nomenclatura e tabelas com código 0; existe tier para todas as 5 faixas até o nível 20.

- [ ] 29. Escrever `26-progressao-e-ressonancias.md`: **tabela mestra 1-20 sem nível vazio** (17), progressão por marco narrativo sem XP (17.1), Eficácia, **Especialização de Combate** como mecânica nova, os **dois tetos** (bônus somado +3/+4/+5 e penalidade somada -3/-4/-5) com escopo fechado (9.6), e as Ressonâncias I a IV com os limites de 16.5. Depende dos itens 25 e 26 (Habilidades e Ultimate são colunas da tabela mestra).
      Files: `livro-v1.0/26-progressao-e-ressonancias.md`
      Verify: `powershell -File "scripts\checar-tabelas.ps1"` confirma 20 linhas sem nível vazio; `powershell -File "scripts\checar-completude.ps1"` não acusa tabela presa no nível 10.

### Bloco D — bestiário

- [ ] 30. Escrever a primeira metade de `28-bestiario.md`: **ficha padronizada** com as 13 colunas de âncora de 18.3 (PV, Defesa, RD, Tenacidade, VEL, ataque, dano por acerto por tipo, DT de efeitos, Teste de Resistência, Fraquezas), como ler e como criar um inimigo, mais as fichas nominais das faixas **1-4 e 5-8** (Comum, Elite e Boss), cobrindo Fragmentum e Legião da Antimatéria. Inimigos **não têm Esquiva** e **Elite e Boss não perdem o turno por Congelamento**.
      Files: `livro-v1.0/28-bestiario.md`
      Verify: nomenclatura e tabelas com código 0; toda ficha tem os 13 campos preenchidos e os valores batem com as linhas de 18.3 das duas faixas.

- [ ] 31. Completar `28-bestiario.md` com as faixas **9-12, 13-16 e 17-20** e as facções restantes (Corporação da Paz Interastral, Aliança Xianzhou, Caçadores de Stellaron, Tolos Mascarados, Cavaleiros da Beleza, autômatos), fechando **30+ fichas nominais** e **3 ou mais Bosses com fases**, cada fase declarando o que muda em Tenacidade, Fraquezas e dano.
      Files: `livro-v1.0/28-bestiario.md`
      Verify: `powershell -File "scripts\checar-completude.ps1"` conta 30 ou mais fichas e 3 ou mais Bosses com fases; as 15 células de PV conferem com 18.3; nomenclatura e tabelas com código 0.

### Bloco E — Guia do Mestre e ambientação

- [ ] 32. Escrever `27-guia-do-mestre.md`: tabela de DT por faixa com linha Trivial, **as cinco DTs de subsistema como lista fechada**, Sucesso Automático restrito a Teste de Perícia (18.4), montagem de encontro com orçamento de PV e as 4 composições equivalentes, o **contrato de encontro da Fraqueza** (18.1), revelar Fraquezas, cadeia de combates entre Descansos, recompensas e concessão de Cones e Relíquias (16.3, 16.4), **procedimento para aprovar Habilidade e Ultimate criadas pelo jogador** (10.4), Ficha de Decisões da Mesa, e o tratamento de casos-limite de mesa (22.1). Depende dos blocos A, B, C e D: é o capítulo que arbitra tudo o que eles definem.
      Files: `livro-v1.0/27-guia-do-mestre.md`
      Verify: nomenclatura e tabelas com código 0; a DT por faixa vai até 17-20 e a lista de DTs de subsistema tem exatamente cinco entradas.

- [ ] 33. Acrescentar ao `27-guia-do-mestre.md` a seção de ambientação (D2): Aeons e Caminhos como cosmologia, **Stellaron**, **Fragmentum**, **Expresso Astral**, verbetes das facções e dos locais, e ganchos de cena. Texto 100% original, nada de wiki ou do jogo. Declarar campanha pronta, regras de nave e viagem interestelar fora de escopo.
      Files: `livro-v1.0/27-guia-do-mestre.md`
      Verify: nomenclatura com código 0; os verbetes das facções casam nome por nome com as fichas do `28-bestiario.md`.

### Bloco F — apêndices, glossário, introdução e build

- [ ] 34. Escrever `scripts/simular-combate.ps1` conforme design 23: recebe as premissas de 18.1 como parâmetros (taxa de acerto, mix de ações, Nível de Habilidade sustentável pelo PH, RD dos dois lados, crítico, cadência de Quebra por perfil, ataques Esquivados por Ciclo, alvos em área), reproduz o DPC de 18.2 parcela por parcela e imprime, por faixa, o DPC de referência, o DPC puro de Elite, o DPC puro de Boss, os Ciclos até a resolução e a attrition do grupo. Reprova fora das janelas publicadas: 3 a 5 Ciclos, DPC divergindo mais de 5%, attrition fora de 70-85% por combate ou 45-70% no terceiro combate do dia, Memoespírito fora de 15-25% do dano do dono.
      Files: `scripts/simular-combate.ps1`
      Verify: `powershell -File "scripts\simular-combate.ps1"` sai com código 0 e reproduz, nas 5 faixas, os Ciclos de 18.3 (~3,7 e ~3,8 nas pontas) com divergência de DPC abaixo de 5%.

- [ ] 35. Escrever `29-apendices-e-fichas.md`: **apêndice de balanceamento** com as contas por faixa (18.1 a 18.5) e as três simulações de referência resolvidas Ciclo por Ciclo, alimentado pela saída do item 34; ficha de personagem preenchível com as cinco estatísticas (PV, Defesa, Esquiva, RD, Velocidade); ficha do Memoespírito (13.1); Trilha de Ação (7.8); referência rápida de uma página; **exemplo completo de criação de personagem passo a passo mostrando as contas** (5.1, 5.2, 6.1, 11.1).
      Files: `livro-v1.0/29-apendices-e-fichas.md`
      Verify: `powershell -File "scripts\checar-tabelas.ps1"` com código 0; os números do apêndice batem com a saída de `simular-combate.ps1`; nomenclatura com código 0.

- [ ] 36. Escrever `30-glossario.md`: todos os termos oficiais em ordem alfabética, incluindo **falhe para frente**, os 6 Testes de Resistência e a Especialização de Combate, mais os **termos aposentados da v0.1 com o nome novo ao lado** (3.1, 3.2). Arquivo isento do checador da Coluna A por design 23.
      Files: `livro-v1.0/30-glossario.md`
      Verify: `powershell -File "scripts\checar-nomenclatura.ps1"` com código 0 (a isenção de `30-*` funciona e nenhum outro arquivo quebra); todo termo oficial de 3.2 tem verbete.

- [ ] 37. Escrever `01-introducao.md`, por último (D3): o que é Explorando Galáxias, o universo e a cosmologia dos Aeons (D2), o que você precisa para jogar, **a faixa de nível 1 a 20 declarada em texto**, o que está fora de escopo, e o **changelog completo da v0.1 para a v1.0** — tudo que foi adicionado, tudo que foi corrigido e **cada decisão que alterou o que o autor escreveu, com justificativa**, obrigatoriamente cobrindo: Bônus de Atributo normalizado, fórmula de Esquiva, todas as médias de dados corrigidas, Eficiência reespaçada para 1-20, Avatar movido para o nível 17, teto de 8 Habilidades, PV fixo no lugar dos dados de vida oscilantes, RD reescalonada, régua de conversão de 11.4 e os 4 Caminhos escritos do zero (20.1, 20.2, 21.1, 21.2).
      Files: `livro-v1.0/01-introducao.md`
      Verify: `powershell -File "scripts\checar-completude.ps1"` sai com código 0 — os 31 arquivos existem, os 9 Caminhos têm 12 Bênçãos cada, nenhum marcador de pendência fora dos 4 Caminhos sem arte, nenhuma tabela presa no nível 10; os três gates (`checar-nomenclatura`, `checar-tabelas`, `checar-completude`) com código 0.

- [ ] 38. Escrever `build/gerar_docx.py` em Python 3 com python-docx 1.2.0, comentado em português: lê os 31 `.md` de `livro-v1.0/` em ordem de prefixo e gera `Sistema de HSR by MC Filhos V1.0.docx` na raiz, com página de título, sumário, **estilos Heading 1/2/3 reais do Word**, **tabelas como objetos tabela de verdade** (o defeito da v0.1) e as imagens embutidas conforme o mapa de 20.3, capa = `image11.png`.
      Files: `build/gerar_docx.py`
      Verify: `python "build\gerar_docx.py"` sai com código 0 e cria o `.docx` na raiz com mais de 1 MB.

- [ ] 39. Verificação final conforme o protocolo do handoff, seção 12. Reabrir o `.docx` com python-docx e conferir número de parágrafos, mais de 15 tabelas, presença de Heading 1/2/3, nenhuma tabela vazia e imagens realmente embutidas; rodar os quatro scripts de checagem; reconferir toda média de dado por `(N+1)/2`; fazer a varredura de referência cruzada — **nenhuma regra pode citar subsistema que o livro não define** (foi o defeito central da v0.1 e reincidiu uma vez no design); confirmar em texto que o livro é de nível 1 a 20.
      Files: `scripts/verificar-livro-final.ps1` (orquestra os quatro scripts e a reabertura do `.docx`)
      Verify: `powershell -File "scripts\verificar-livro-final.ps1"` sai com código 0 e imprime o relatório com as contagens; relatar "pronto" **somente** com esse relatório em mãos, nunca porque um script rodou sem erro.

---

## Lacunas conhecidas e assunções

- **Arte dos 4 Caminhos novos não existe.** Capítulos 12 a 15 saem com `<!-- ARTE PENDENTE: símbolo do Caminho -->`; o `checar-completude.ps1` aceita o marcador nesses quatro arquivos e só nesses (design 20.3).
- **Fichas nominais do bestiário são escrita, não design** (design 26.3). O design fecha a ficha padronizada e as âncoras das 5 faixas; nome, tema e sabor dos 30+ bichos são decisão de escrita, presa às colunas de 18.3.
- **Pandoc é opcional e não foi verificado nesta máquina.** O caminho oficial de montagem é `build/gerar_docx.py` com python-docx, que está instalado e funcionando. Pandoc não entra em nenhum item deste plano.
- **O `.docx` da v0.1 permanece intocado** como registro histórico (design 2).
