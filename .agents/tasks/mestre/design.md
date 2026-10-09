# Design — Planilha do Mestre · Explorando Galáxias v1.1

Pasta de entrega: `Mestre\`. Código: `build\` (pacote `build\mestre\`). Internos: `.agents\tasks\mestre\`.
Este documento é o contrato de implementação. Ele não contém código de produção. Onde ele cita o livro, a seção é a do livro v1.1 (pasta histórica `livro-v1.0\`).

---

## 1. Visão geral

A Planilha do Mestre é **um `.xlsx` de 18 abas**, gerado por Python com `openpyxl` a partir dos capítulos `.md` do livro, no mesmo pipeline da ficha automatizada: os estilos, a convenção de mapa lógico, o lint de compatibilidade com o Google Planilhas, o motor de cálculo dos testes (`formulas` 1.3.4), o léxico de ortografia e o renderizador de PNG vêm **por import** dos arquivos da ficha, que não são alterados. O que é novo: um parser do capítulo 28 (âncoras, 32 fichas, fases, ações) e do capítulo 27 (orçamento, composições, recompensas, facções, locais, ganchos), um módulo de tabelas de sabor escritas para os geradores, um gerador modular por aba, um oráculo Python independente e uma bateria de testes própria.

A planilha cobre quatro trabalhos do Mestre, nesta ordem de valor: **(1) rodar o combate** (Fila de Ação com Firmeza e Atraso, PV, Tenacidade e Quebra, condições, Morrendo, recursos do grupo, recargas, fases de Boss e calculadora de dano), **(2) preparar o combate** (bestiário consultável, Criador de Inimigos, Construtor de Encontros com orçamento e contrato da Fraqueza, encontro aleatório), **(3) preparar a história** (NPCs, aventuras, recompensas, mundos, improviso e tabelas editáveis) e **(4) administrar a campanha** (grupo, marcos, missões, facções, relógios, linha do tempo, sessões, Sessão Zero, Ficha de Decisões da Mesa e Escudo do Mestre imprimível).

Todo gerador é **determinístico por semente** (seção 5): mesma semente e mesma "Rolagem nº" dão o mesmo resultado, editar outra célula não muda nada, e o oráculo reproduz cada sorteio. Não há macro, Apps Script, `RAND`/`RANDBETWEEN` nem função exclusiva do Google. Mudança de estado é sempre entrada do Mestre; "salvar" um resultado gerado é copiar a linha de saída e colar como valores na tabela de registro, que tem as colunas na mesma ordem (seção 2, D6).

Números e regras vêm do livro e citam a seção. Onde o livro não tem regra (inimigo por nível dentro da faixa, orçamento para grupo diferente de 4, tesouro por encontro, pesos de sorteio etc.), a planilha usa uma **heurística derivada do próprio livro**, escrita na célula como **"Sugestão da planilha — não é regra do livro"**, listada na seção 8 com o método e a validação.

---

## 2. Decisões-chave (travadas com a aprovação deste design)

**D1 — Pilha tecnológica.** Python 3.14.7, `openpyxl` 3.1.5 (gera e lê), `formulas` 1.3.4 (calcula nos testes), `pillow` 12.1.0 (preview). Versões de `build\requirements-ficha.txt`, sem dependência nova. Saída `.xlsx` para importar no Google Planilhas (alvo principal), abrindo também no Excel. Fórmulas em inglês canônico com vírgula, só funções de `build\ficha_funcoes_ok.json` (IF, IFERROR, AND, OR, NOT, SUM, SUMIF, SUMPRODUCT, COUNTIF, COUNTIFS, COUNTA, COUNTBLANK, INDEX, MATCH, VLOOKUP, HLOOKUP, CHOOSE, MIN, MAX, ROUNDUP, ROUND, INT, MOD, ABS, LEN, CONCATENATE, REPT, ISBLANK, ISNUMBER, ISERROR, ROWS, LARGE, SMALL) e o operador `&`. Proibido: `_xlfn`, FILTER, SORT, UNIQUE, SEQUENCE, XLOOKUP, LET, LAMBDA, TEXTJOIN, IFS, SWITCH, TEXT, INDIRECT, OFFSET, ROUNDDOWN, TRIM, CHAR, `--`, referência a outra aba em formatação condicional ou validação personalizada, nome definido, Tabela do Excel, caixa de seleção, proteção, painel congelado. Arredondamento só com `INT`. `wb.calculation.fullCalcOnLoad = True`.

**D2 — Nomes dos entregáveis.** O briefing chegou sem acentos em todo o texto (inclusive na citação do usuário, que no original tem acento), e a regra dura é ortografia PT-BR. Os nomes ficam: `Mestre\Planilha do Mestre - Explorando Galáxias V1.1.xlsx`, `Mestre\Planilha do Mestre - Exemplo.xlsx` e `Mestre\COMO-USAR-PLANILHA-DO-MESTRE.md` — o primeiro com o mesmo "Galáxias" do nome da ficha (`Ficha Automatizada - Explorando Galáxias V1.1.xlsx`). Os três nomes são constantes únicas em `build\mestre\nucleo.py` (`SAIDA_MODELO`, `SAIDA_EXEMPLO`, `SAIDA_GUIA`); trocar é uma linha.

**D3 — Uma planilha, 18 abas**, nesta ordem: Início, Campanha, Grupo, Sessões, Missões, NPCs, Inimigos, Bestiário, Encontros, Combate, Aventuras, Recompensas, Mundos, Improviso, Escudo do Mestre, Minhas Tabelas, Tabelas, Dados. Nomes com acento (o spike da ficha aprovou acento em nome de aba). **Tabelas** = listas dos geradores, editáveis pelo Mestre. **Dados** = tabelas do livro lidas pelas fórmulas; o gerador reescreve, não edite.

**D4 — Identidade visual e usabilidade da ficha**, sem exceção: os estilos de `gerar_ficha.py` (Arial; entrada `#FFF2CC` com borda `#BF9000`; calculada `#E8EEF7`; aviso texto `#9C0006` com fundo `#FFC7CE` por formatação condicional `LEN>0` na mesma aba; título `#1F3864`/branco; cabeçalho de coluna `#B4C6E7`/`#1F3864`; zebra; não se aplica `#D9D9D9`), legenda na linha 2 de cada aba, subtítulo na linha 3, cabeçalhos com "(preencha)"/"(automático)" (cor nunca é o único sinal), contraste ≥ 4,5:1, fonte ≥ 9 pt, nenhum texto cortado (régua `renderizar_ficha.medir`), área principal de cada aba ≤ 1360 px de largura, nenhuma linha de dados a mais de 15 linhas do cabeçalho da tabela (cabeçalho repetido quando precisar), sem painel congelado. Toda entrada sai **vazia** no modelo (a bateria simula "vazio" omitindo a entrada); a semente padrão vale quando a célula da semente está vazia.

**D5 — Semente determinística, sem `RAND`.** Confirmado o modelo pedido (seção 5). O rolador de dados também usa semente: `RAND`/`RANDBETWEEN` recalculam a cada edição em qualquer aba do Google (quebraria "editar outra célula não muda o resultado"), não estão na lista branca (o lint precisa ficar 0) e não são testáveis. "Rolar de novo" = somar 1 na "Rolagem nº" do gerador ou trocar a semente global.

**D6 — Salvar sem macro = copiar e colar valores.** Cada gerador mostra a saída numa **linha de saída** com as colunas na mesma ordem da tabela de registro correspondente (NPC → Elenco; aventura → Missões; recompensa → Tesouro; encontro → Encontros salvos; facção → Facções). O Mestre copia a linha e usa "Colar especial → Somente valores". O guia ensina isso com figura de passos. Exceção deliberada: inimigos criados **não** precisam de cópia — a tabela "Inimigos da campanha" (aba Inimigos) é o próprio criador, uma linha por inimigo, e já alimenta as listas do combate e dos encontros.

**D7 — Combate sem macro.** O estado do combate é entrada do Mestre (PV atual, redução de Tenacidade, Atraso do Ciclo, já agiu, condições, PH, Energia). As fórmulas calculam o resto: a Fila do Ciclo atual pela regra do 19.3–19.6 (com Firmeza), a Fila prevista do próximo Ciclo, quem age agora, Quebra, fase do Boss, avisos de Morrendo e de Executado. Avançar o Ciclo é o Mestre somar 1 em "Ciclo atual", copiar os "pendentes" calculados para a coluna de entrada e limpar as colunas "neste Ciclo" (o guia e a própria aba dizem a sequência em 4 linhas, como a Trilha de Ação de 29.10).

**D8 — Reaproveitamento por import, zero edição dos arquivos da ficha.** `gerar_ficha.py`, `ficha_dados.py`, `oraculo_ficha.py`, `testar_ficha.py`, `renderizar_ficha.py`, `ficha_funcoes_ok.json`, `ficha_protegidos.json`, `ficha_mapa.json` e `requirements-ficha.txt` ficam byte a byte iguais (conferido contra `.agents\tasks\mestre\baseline-hashes.json` e `ficha_protegidos.json`). Importar `gerar_ficha` não tem efeito colateral (só constantes, funções e um `Mapa()` que a Mestre não usa); a Mestre tem o seu próprio mapa e o seu próprio registro de referências.

**D9 — Um registro de cada coisa.** Nível do grupo e tamanho da mesa são digitados uma vez (aba Campanha) e lidos por todas as abas. Os números de cada PJ são digitados uma vez (aba Grupo, copiados da ficha do jogador). Nenhuma entrada existe em dois lugares.

**D10 — Fases sequenciais num ramo só.** Quatro fases (seção 13), cada uma termina com as duas planilhas geradas, lint 0 e as suítes da fase passando. Nenhum ramo paralelo mexe nos mesmos arquivos.

**D11 — Layout das tabelas largas: sub-tabelas por assunto (revisão 1).** Precedente da ficha: a tabela mestra de 16 colunas da aba Progressão "vem em 2 partes de 8 colunas (cada uma repete o Nível)" (`gerar_ficha.aba_progressao`). A Mestre generaliza isso numa regra única, conferida pelo `nucleo.ajustar_layout` e pela suíte `lint`:

- **Grade padrão de A:L = 1360 px:** A = 150 px (rótulo do item), B…J = 100 px cada (900 px), K:L = 155 px cada (310 px, coluna de aviso mesclada). Uma aba pode trocar larguras dentro de A:L, desde que a soma continue ≤ 1360 px. Um campo de texto longo (Dano por acerto, Fraquezas, efeito de condição, Dano de Quebra) ocupa 2 ou 3 colunas mescladas na linha.
- **No máximo 9 campos (B:J) por linha de tabela**, mais o rótulo em A e o aviso em K:L. Tabela com mais campos vira **sub-tabelas por assunto**, uma embaixo da outra. A linha *i* de cada sub-tabela é sempre o mesmo item *i*. A coluna A de cada sub-tabela, a partir da segunda, repete o rótulo do item por fórmula (calculada, ex. "3 · Larva Fuliginosa 2").
- **Cada sub-tabela tem no máximo 13 linhas de dados** sob o seu cabeçalho. Com 16 combatentes, ela vem em 2 blocos (10 + 6), cada um com o cabeçalho repetido. Assim vale a distância de 15 linhas de D4.
- **Colunas auxiliares** (sorteio `u/y/x`, contadores, chaves de ordenação, `passa`/`ordem`) ficam **à direita de L, ocultas**, como na ficha ("M:O são auxiliares ocultas"). Elas não são entrada e não contam na área de 1360 px. A decisão anterior, que as deixava visíveis com 40 px, caiu: um `x` de 10 dígitos numa coluna de 40 px vira "####", e isso conta como texto cortado.
- O mapa registra cada sub-tabela em `subtabelas` (aba, id, itens, colunas). A suíte `lint` falha se alguma linha tiver mais de 12 colunas usadas em A:L, se uma tabela passar de 13 linhas sem cabeçalho repetido ou se a área passar de 1360 px.

As divisões de cada aba larga estão em 6.3 (Grupo), 6.7.1 (Inimigos), 6.8 (Bestiário), 6.9 (Encontros) e 6.10 (Combate).

---

## 3. Arquitetura de módulos

### 3.1 Arquivos

| Arquivo | Tamanho-alvo | Papel |
|---|---|---|
| `build\gerar_mestre.py` | < 15 KB | Ponto de entrada. Monta o workbook (`nucleo.novo_workbook`), chama cada `mestre.aba_*.montar(ctx)` na ordem de dependência, resolve marcadores, ajusta layout (`nucleo.ajustar_layout`), grava o modelo em branco, grava o Exemplo (`mestre.exemplo.preencher`) e o `build\mestre_mapa.json`. Grava num arquivo temporário na mesma pasta e só então substitui o destino (nunca deixa `.xlsx` pela metade). |
| `build\mestre_dados.py` | < 60 KB | Dados do livro para a Mestre: parser do cap. 28 (28.3 âncoras e conversão em dados; 28.6–28.10 as 32 fichas com campos, fases e ações; 28.11 índice) e do cap. 27 (27.2, 27.3, 27.4 orçamento e composições, 27.7 attrition, 27.8 recompensas, 27.9 Ultimate, 27.16 facções, 27.17 locais, 27.18 ganchos), mais o que reaproveita de `ficha_dados` (seção 3.2). Expõe `blocos()` (aba Dados), `listas()` (validações), `bestiario()`, `acoes()`, `fases()`, `GERADORES` (ids estáveis, seção 5) e `ancoras()`. Toda leitura de tabela falha alto (`ValueError` com capítulo e seção) se a tabela não for encontrada ou tiver colunas diferentes do esperado. |
| `build\mestre_sabor.py` | < 60 KB (dividir em `mestre_sabor_nomes.py` se passar) | Tabelas de sabor escritas para os geradores (nomes por cultura, ocupações, aparências, rumores, bugigangas…), cada uma com `id`, título, fonte (`"Sugestão da planilha"` ou seção do livro quando derivada dele) e valores. Texto original, PT-BR, sem nome de personagem do jogo. |
| `build\mestre\__init__.py` | — | Pacote. |
| `build\mestre\nucleo.py` | < 40 KB | Caminhos e nomes de saída; `MapaMestre` (mesmo formato do `Mapa` da ficha, gravando `mestre_mapa.json`); `reg`, `T`, `ref`, `resolver_marcadores` (mesma convenção «nome.logico» da ficha, com registro próprio); `ent`, `cal`, `av`, `aux`, `rot`, `cabecalhos`, `sugestao` (rótulo "Sugestão da planilha — não é regra do livro"); `cabecalho_aba`; `escrever_dados` (aba Dados, no mesmo leiaute de blocos da ficha); `ajustar_layout` (alturas e quebras pela régua `renderizar_ficha.medir`, área ≤ 1360 px). Os estilos vêm de `gerar_ficha` (3.2). |
| `build\mestre\sorteio.py` | < 15 KB | O **único** construtor de fórmulas de sorteio: `semente_efetiva()`, `rolagem(cel)`, `valor(gerador, campo, rolagem_ref)` (escreve as 3 células auxiliares `u`, `y`, `x` da seção 5 e devolve a referência de `x`), `escolha(lista_id, x_ref)`, `escolha_sem_repetir(lista_id, x_ref, indice1_ref)`, `varios_sem_repetir(lista_id, x_ref, k)` (sequência com passo primo de 6.17), `inteiro(x_ref, minimo, maximo)`, `dado(x_ref, faces)`. Mais `TAMANHO(lista_id)` (célula "Tamanho da lista" da aba Tabelas). |
| `build\mestre\aba_combate.py` | < 60 KB | Aba Combate (seção 6.10). |
| `build\mestre\aba_inimigos.py` | < 60 KB | Abas Inimigos e Bestiário (6.7, 6.8). |
| `build\mestre\aba_encontros.py` | < 45 KB | Aba Encontros (6.9). |
| `build\mestre\aba_npcs.py` | < 40 KB | Aba NPCs (6.6). |
| `build\mestre\aba_aventuras.py` | < 40 KB | Aba Aventuras (6.11). |
| `build\mestre\aba_recompensas.py` | < 40 KB | Aba Recompensas (6.12). |
| `build\mestre\aba_campanha.py` | < 60 KB | Abas Campanha, Grupo, Sessões e Missões (6.2–6.5). |
| `build\mestre\aba_mundos.py` | < 50 KB | Abas Mundos e Improviso (6.13, 6.14). |
| `build\mestre\aba_escudo.py` | < 30 KB | Aba Escudo do Mestre (6.15). |
| `build\mestre\aba_tabelas.py` | < 30 KB | Abas Tabelas e Minhas Tabelas (6.16, 6.17). |
| `build\mestre\aba_inicio.py` | < 25 KB | Aba Início (6.1). |
| `build\mestre\exemplo.py` | < 40 KB | Entradas da campanha de demonstração (seção 14); os números dos 4 PJs saem de `oraculo_ficha.calcular`. |
| `build\oraculo_mestre.py` | < 60 KB | Oráculo independente (seção 12.2). Não importa `mestre_dados`, `mestre\*` nem lê fórmula; tem as tabelas do livro transcritas com a seção ao lado e reimplementa sorteio, Criador de Inimigos, orçamento, Fila/Firmeza, Quebra, recompensas e geradores. Lê as tabelas de sabor do `.xlsx` gerado (valores, não fórmulas), porque elas são conteúdo, não regra. |
| `build\testar_mestre.py` | < 60 KB (+ `build\mestre\testes_*.py` se crescer) | Bateria (seção 12). |
| `build\mestre_mapa.json` | gerado | Contrato gerador × testes (seção 4.3). |
| `build\mestre_lexico_extra.txt` | pequeno | Palavras PT-BR das tabelas de sabor que não estão no livro. |

Nenhum módulo passa de ~60 KB. A ordem de montagem não importa para as fórmulas (marcadores resolvidos no fim), mas as abas que **registram** listas (Tabelas, Dados) montam primeiro.

### 3.2 O que é reaproveitado, e de onde

| De | O quê | Para quê |
|---|---|---|
| `gerar_ficha` | `fonte, entrada, calculada, aviso, titulo, nao_se_aplica, cabecalho, texto, estilo_rotulo_linha, legenda, q, slug, _abs, sinal, texto_dano, _px_largura, larguras, _dv_lista, _dv_numero, formatar_avisos`, constantes `COR_*`, `TAM_*`, `FONTE`, `VERSAO` | Estilo idêntico; validações com `errorStyle="warning"` e mensagens PT-BR |
| `ficha_dados` | `secao, tabelas, tabela, limpar, num, dados` e os parsers `racas, caminhos, elementos, condicoes, fraqueza_resistencia, dt_fraqueza, tenacidade, armas, armaduras, propriedades, pocoes, itens, verba, cone, faixas_equipamento, reliquias, conjuntos, ressonancias, tabela_mestra, habilidades, ultimate, ph, custo_ph, energia, dt_faixa, dt_subsistema, dt_inimigo, alcances` | Blocos do livro na aba Dados |
| `renderizar_ficha` | `px_coluna, px_linha, medir, quebrar, fonte, tabelas, contraste, PiorTexto, renderizar_estado, gravar_indice, gravar_recortes, LADO_RECORTE` | Ajuste de layout no gerador; suítes preview e visual |
| `testar_ficha` | `Modelo, Resultado, normalizar_valor, eh_erro, _igual, separar_ref, _checar_formula, _tem_emoji, _sha256, _arquivos_protegidos, LISTA_BRANCA, PROIBIDAS, _textos_visiveis, _lexico, _proibidas_ps1, _glossario_30_1, _sem_acento_mesmo_tamanho, ler_funcoes_ok` | Motor de cálculo, lint, texto, protegidos |
| `oraculo_ficha` | `calcular`, `eficiencia`, `faixa`, `ph_grupo` | Números dos PJs do Exemplo; conferência cruzada |

Import com `sys.path.insert(0, BUILD)`. Se um desses nomes deixar de existir, o import falha na hora (fatal, mensagem com o nome) — é o sinal para não "consertar" a ficha, e sim adaptar a Mestre.

---

## 4. Modelo de dados

### 4.1 Aba Dados (livro; o gerador reescreve)

Blocos com título que já traz a fonte ("Âncoras do inimigo — 28.3"), cabeçalho e linhas, no leiaute da aba Dados da ficha, listas de validação à direita. Blocos:

| Bloco (`dados.<id>`) | Conteúdo | Fonte |
|---|---|---|
| `ancoras` | 15 linhas (faixa × tipo): PV, Defesa, RD, Tenacidade, VEL, Ataque, Dano médio, DT dos efeitos, Teste de Resistência, nº de Fraquezas, Firmeza, ações agressivas por turno | 28.3, 28.2 (regras 3 e 5), 20.3 |
| `dano_dados` | 15 linhas: expressão (`4d8 + 2`), nº de dados, faces, fixo, média | 28.3 "Dano por acerto, convertido em dados" |
| `dano_especial` | 15 linhas: expressão e média de "1,5 ×" por faixa × tipo, coluna Fonte = ficha do livro ou "Sugestão da planilha" | 28.4 regra 5 + fichas (H2) |
| `bestiario` | 32 fichas: nº, nome, tipo, faixa, facção, fases, PV, Defesa, RD, Tenacidade, VEL, Ataque, DT, TR, Fraquezas (fase 1), Resistências, Execução ("Pode", "Não", "Não declarado"), Na Fila (texto), frase, ambiente (H8) | 28.6–28.11 |
| `bestiario_fases` | Uma linha por fase dos 5 Bosses com fases (**12 linhas**: três Bosses de 2 fases, com 305, 580 e 750 PV, e dois de 3 fases, com 935 PV cada): criatura, fase, PV do topo e do piso, Fraquezas, Tenacidade, ritmo (ex.: "1 ataque + 1 ação especial por turno") | 28.5–28.10 |
| `bestiario_acoes` | Uma linha por ataque/ação especial (≈ 95): criatura, fase (0 = todas), ordem, tipo (Ataque/Especial/Reação/Gatilho), nome, alcance, Elemento, recarga, **texto-modelo** com marcadores (seção 6.7.3) | 28.6–28.10 |
| `orcamento` | 5 faixas: dano do grupo por Ciclo, orçamento, custo Comum/Elite/Boss | 27.4 |
| `composicoes` | 4 composições: fórmula de tipos, sensação, duração | 27.4, 28.11 |
| `attrition` | 5 faixas: nível de referência, PV do grupo, dano em 4 Ciclos, % ao fim | 27.7 |
| `dt_faixa`, `dt_subsistema`, `dt_fraqueza`, `dt_inimigo` | DT por faixa, as 5 DTs fixas, DT de Fraqueza, DT/TR de inimigo | 27.2, 27.3, 20.2, 22.3 |
| `fila` | VEL por Caminho, teto de Atraso por tipo, Firmeza (passos), casos-limite | 19.1, 19.4–19.7 |
| `elementos`, `fraqueza_resistencia`, `tenacidade` | Elemento, Dano de Quebra, efeito; +2/−2 dados e redução total/metade/1; redução por fonte | 20.1–20.5 |
| `condicoes` | 21.5 inteira (efeito, duração, acúmulo, "só inimigos") | 21.5 |
| `morrendo`, `descanso`, `execucao` | contador, Vantagem por Raça, Executado, Descansos | 23.4–23.6 |
| `ph`, `energia`, `ultimate_faixa` | PH por nº de jogadores, fontes de Energia, Ultimate por faixa | 16.2, 17.2, 27.9 |
| `racas`, `caminhos` | Raça + traço curto; Caminho + Elemento sugerido não (o livro não liga Caminho a Elemento) + Bônus de VEL | 05, 06.3, 19.1 |
| `armas`, `armaduras`, `propriedades`, `pocoes`, `itens`, `verba` | Equipamento e preços | 24.1–24.5 |
| `cone`, `faixa_equipamento`, `reliquias`, `conjuntos`, `ressonancias`, `bonus_maior` | Recompensas de marco | 25.1–25.3, 26.7 |
| `progressao` | 26.1 ritmo de sessões; Eficiência por nível | 26.1, 29.12 |
| `faccoes`, `locais`, `ganchos` | 8 facções (resumo + fichas), 6 locais, 20 ganchos | 27.16–27.18 |
| `casos_limite` | 27.10 (seleção completa) | 27.10 |
| `tetos` | tetos que a mesa esquece | 29.12 |

### 4.2 Aba Tabelas (listas dos geradores, editáveis)

Uma lista por coluna, com cabeçalho (nome da lista), linha "Fonte" ("Livro 27.18" ou "Sugestão da planilha"), linha "Tamanho da lista" (calculada) e **100 vagas** de valores (entrada; as de fonte do livro vêm preenchidas com o texto do livro; as de sabor, com as tabelas de `mestre_sabor`). Para cumprir a distância de 15 linhas ao cabeçalho, as 100 vagas vêm em 8 faixas de 13 vagas (a última com 9), cada faixa precedida de uma linha de cabeçalho repetido (estilo cabeçalho, não é entrada). Ao lado de cada coluna, uma coluna auxiliar cinza estreita com o **contador corrido**: na vaga, `aux_i = aux_{i-1} + IF(LEN(valor_i)>0,1,0)`; na linha de cabeçalho repetido, `aux_i = aux_{i-1}` (o gerador sabe quais linhas são cabeçalho). "Tamanho da lista" = último contador. O sorteio pega o k-ésimo valor não vazio por `INDEX(coluna, MATCH(k, aux, 0))`: o `MATCH` exato devolve a primeira linha em que o contador chega a k, que é sempre uma vaga preenchida (a linha de cabeçalho seguinte repete o mesmo k, mas vem depois). Linha vazia no meio da lista não quebra nada. **Não se inserem linhas** (o contador corrido pularia a linha nova): a aba e o guia dizem "100 vagas por lista; apague para trocar, use as vagas vazias para ampliar". Uma lista cheia acende o aviso "Lista cheia (100): use Minhas Tabelas para uma lista maior". Validação: texto livre de até 200 caracteres; mais longo = aviso (o sorteio usa o texto mesmo assim).

Listas (id `tab.<id>`, mínimo de entradas): ver seção 6.16. Tabelas de sabor ≥ 20 entradas; nomes ≥ 30 por cultura.

### 4.3 `build\mestre_mapa.json`

Mesmo formato do `ficha_mapa.json`: `celulas` (`"<aba>.<campo>" → "'Aba'!A1"`, aba em minúsculas sem acento: `inicio, campanha, grupo, sessoes, missoes, npcs, inimigos, bestiario, encontros, combate, aventuras, recompensas, mundos, improviso, escudo, minhas, tabelas, dados`), `blocos` (`dados.<id>` com intervalo e colunas), `listas` (`lista.<id>`), `tabelas` (`tab.<id>` → intervalo de valores, auxiliar, tamanho, fonte, `sem_ortografia` para listas de nomes), `geradores` (`<id>` → campos com célula da Rolagem nº e das auxiliares `u`, `y`, `x` de cada campo, mais a lista de parâmetros da seção 5), `subtabelas` (D11), `entradas` (tipo, mínimo, máximo, amostra válida e inválida), `avisos` (por aba), `sugestoes` (células com rótulo de Sugestão e a heurística H#), `constantes` (constantes procedimentais escritas dentro de fórmula, cada uma com a seção: ex. `"firmeza.divisor": [2, "19.4"]`).

---

## 5. Modelo de semente determinística

**Entradas.** `Início!` "Semente da campanha" (inteiro 1 a 2 147 483 646; vazia = **semente padrão 12345**; fora da faixa ou não inteiro = aviso "Semente fora de 1 a 2.147.483.646: usando 12345"). Em cada gerador, "Rolagem nº" (inteiro 1 a 1 000 000; vazia = 1; inválida = aviso e 1). "Rolar de novo" = somar 1 na Rolagem nº; "outra campanha" = trocar a semente.

**Constantes.** `M = 2147483647` (primo de Mersenne 2³¹−1), `A = 16807` (multiplicador de Lehmer/Park–Miller). Cada gerador tem um id `G` (inteiro fixo, nunca reaproveitado) e cada campo sorteado um id `C`, em `mestre_dados.GERADORES`:

| G | Gerador | G | Gerador |
|---|---|---|---|
| 100 | Encontro aleatório | 540 | Facção |
| 110 | Fraquezas sugeridas (Criador) | 550 | Organização |
| 200 | NPC | 560 | Nomes avulsos |
| 300 | Aventura | 600 | Rumor |
| 400 | Recompensa de encontro | 610 | Evento / complicação |
| 410 | Cone de Luz (sabor) | 620 | Loja |
| 420 | Conjunto de Relíquias (sabor) | 630 | Bugiganga |
| 510 | Planeta / local | 640 | Oráculo sim/não |
| 520 | Estação | 650 | Rolador de dados |
| 530 | Nave | 701–710 | Minhas Tabelas 1–10 |

**Fórmula (revisão 1: três células auxiliares por campo, `u`, `y` e `x`, ocultas à direita de L — D11):**

```
S  = semente efetiva (Início)                              1 ≤ S ≤ 2 147 483 646
R  = Rolagem nº efetiva do gerador                          1 ≤ R ≤ 1 000 000
h  = MOD(S + 7919*G + 104729*R + 1299709*C, 2147483646) + 1                     1 ≤ h ≤ M−1
L3(z) = MOD(MOD(MOD(z*16807,2147483647)*16807,2147483647)*16807,2147483647)    (3 rodadas de Lehmer)
Q(z)  = MOD(MOD(INT(z/65536)*z,2147483647)*65536 + MOD(z,65536)*z, 2147483647) (z² mod M, partido em 16 bits)
X(z)  = MOD(z + INT(z/65536)*MOD(z,65536), 2147483646) + 1                     (mistura por partição: não é polinômio mod M)

u = L3(h)        célula aux. 1 (h escrito dentro dela)
y = L3(Q(u))     célula aux. 2
x = L3(X(y))     célula aux. 3 — é o "valor sorteado" do campo, 1 ≤ x ≤ M−1
```

**Por que três estágios.** A primeira versão (`x3 = L3(h)`) era afim em `h`: dois campos do mesmo gerador ficavam sempre à mesma distância, e cada "rolar de novo" andava um passo fixo. O revisor mediu 6,7% de cobertura na propriedade (f), e o rolador saiu em escada. A correção sugerida pelo revisor (`L3 → Q → L3`) foi simulada nesta revisão. Ela resolve os pares, mas continua polinomial (grau 2) em `h`. A segunda diferença de três campos ou rolagens consecutivos fica constante mod M, e por isso só 144 das 216 triplas de d6 consecutivos aparecem. Com dois quadrados (grau 4), a quarta diferença ainda concentra (χ² = 9 449 com 29 graus de liberdade, listas de 30). A rotação de bits não serve, porque, com M = 2³¹−1, rotacionar 16 bits é multiplicar por 2¹⁶ mod M, que continua linear. `X` usa `INT` e `MOD 65536`, que não são polinômio mod M, e assim quebra a estrutura. Simulação desta revisão (S = 12345, script apagado depois):

| Medida | Afim (v0) | L3-Q-L3 (revisor) | **L3-Q-L3-X-L3 (adotada)** | Meta |
|---|---|---|---|---|
| (f) pares de campos C = 8 × C = 10, listas de 30, 2 000 rolagens | 6,7% | 89,4% | **89,7%** | ≥ 60% |
| Pares de rolagens consecutivas (R, R+1), lista de 30 | 6,7% | 87,4% | **89,6%** | ≥ 60% |
| Triplas de d6 consecutivos (rolador, C = 1…20) | 18/216 | 144/216 | **216/216** | todas |
| 5-uplas de d6 consecutivos, 64 000 amostras | — | 719/7 776 | **7 772/7 776** (χ² 7 738, gl 7 775) | χ² ≤ 8 100 |
| χ² da 2ª a 5ª diferença de índices consecutivos (n = 6, gl 5 / n = 30, gl 29) | 18 264 | 41 149 | **≤ 12 / ≤ 46** | ≤ 20 / ≤ 55 |
| Frequência por índice, lista de 100, 20 000 rolagens (esperado 200) | 194–208 | 172–233 | **168–237** | 150–250 (±25%) |
| 10d6: média / desvio (teórico 35 / 5,40) | 35,0 / 10,86 | 34,8 / 5,39 | **34,8 / 5,34** | ±0,5 / ±0,4 |

- **Aritmética segura:** em `h`, o maior intermediário é ≈ 1,1·10¹¹. Em `L3`, o maior produto é `z·16807` < 3,6·10¹³. Em `Q`, `INT(z/65536)·z` < 2⁴⁶, `MOD(…)·65536` < 2⁴⁷ e `MOD(z,65536)·z` < 2⁴⁷, então a soma fica < 2⁴⁸ ≈ 2,8·10¹⁴. Em `X`, `z + INT(z/65536)·MOD(z,65536)` < 2³². Tudo fica < 2⁵³ ≈ 9·10¹⁵, então todo valor é inteiro exato em ponto flutuante (Google, Excel e `formulas`). O maior quociente de `MOD` é ≈ 1,31·10⁵ (em `Q`), abaixo do limite histórico de 2²⁷ ≈ 1,34·10⁸ do `MOD` do Excel. Nos extremos (S = 1 e 2 147 483 646, G = 100 e 710, R = 1 e 1 000 000, C = 1 e 400), o maior intermediário simulado foi 2,78·10¹⁴. O oráculo confere esses limites com `assert` para todo `G` e `C` usados e para R e S nos extremos.
- **Nunca zero:** `h` ≥ 1. `L3` de um valor não nulo mod M primo é não nulo. `Q(z)` = z² mod M ≠ 0. `X` devolve de 1 a M−1. Então `u`, `y` e `x` ficam em [1, M−1], e `L3` nunca recebe 0.
- **Custo:** 3 células ocultas por campo sorteado, ≈ 400 campos ≈ 1 200 células de uma conta cada (sem matriz). Isso fica dentro do risco de desempenho da seção 16.
- **Uso:** índice numa lista de tamanho `n` = `INT(x*n/2147483647)+1` (de 1 a n; `x·n` < 2,2·10¹¹). Dado de `f` faces = `INT(x*f/2147483647)+1`. Inteiro em [a, b] = `a + INT(x*(b−a+1)/2147483647)`. Segundo sorteio **sem repetir** o índice `i₁` na mesma lista: `j = 1 + INT(x₂*(n−1)/2147483647)` e índice₂ = `MOD(i₁ − 1 + j, n) + 1`, que nunca dá i₁ (com n = 1, mostra a mesma entrada). Toda fórmula desta seção é gerada só por `mestre\sorteio.py`.
- **Lista vazia** (`n = 0`): o campo mostra "" e o aviso "Lista '<nome>' está vazia (aba Tabelas)". Nunca erro.
- **Propriedades garantidas** (suíte `determinismo`):
  - (a) Mesma S, R, parâmetros e listas dão o mesmo resultado em qualquer motor.
  - (b) Editar uma célula que não seja S, a Rolagem nº do gerador, um **parâmetro listado na tabela abaixo** ou a lista usada não muda o resultado.
  - (c) Trocar R muda o resultado de pelo menos 90% dos campos com lista ≥ 20 entradas, em 200 rolagens.
  - (d) Toda entrada de toda lista aparece em até 2 000 rolagens.
  - (e) Em 20 000 rolagens, a frequência de cada índice fica dentro de ±25% do uniforme, para listas de até 100 itens.
  - (f) Para dois campos do mesmo gerador, os pares (índice₁, índice₂) em 2 000 rolagens cobrem pelo menos 60% das combinações de listas de até 30 itens.
  - (g) **Correlação serial** (novo na revisão 1): em listas de 6 e de 30, o χ² da distribuição mod n da 1ª à 5ª diferença de índices consecutivos fica abaixo do valor crítico de p = 0,001 (20,5 com 5 graus de liberdade; 58,3 com 29). Vale em dois sentidos: entre rolagens R, R+1… do mesmo campo e entre campos C, C+1… da mesma rolagem, inclusive os 20 dados de uma expressão do rolador. Também precisam aparecer todas as 216 triplas de d6 consecutivos em 2 000 rolagens. O teste roda no oráculo, em Python puro (é unidade da fórmula), e confere em 300 rolagens que a planilha devolve exatamente os mesmos `u`, `y` e `x` do oráculo.

**Parâmetros de cada gerador** (a lista fechada da propriedade (b); "faixa do grupo" = calculada do nível da aba Campanha):

| G | Parâmetros (além de S e da Rolagem nº do gerador) |
|---|---|
| 100 | ambiente, faixa (vazia = do grupo), composição; listas do bestiário (Dados) e `tab.ambiente_por_faccao`; Elementos do grupo (só para a troca sugerida, H19) |
| 110 | tipo da linha; Elementos do grupo; Fraquezas já escolhidas nas outras linhas de Inimigos da campanha (H12) |
| 200 | Raça, Caminho, papel, faixa e tipo do bloco; **faixa do grupo** (ganchos de 27.18, H20); listas `tab.*` do NPC |
| 300 | tipo, faixa (vazia = do grupo, para ganchos, antagonista, DTs e recompensa), facção; listas `tab.*` da aventura. A recompensa da aventura **não** lê a aba Recompensas: usa G = 300 (C = 13 e 14), a faixa da aventura e a leitura fixa "Típico" (6.11) |
| 400 | faixa (vazia = do grupo), leitura de dificuldade (vazia = Típico) |
| 410, 420 | faixa (vazia = do grupo) para os números do Cone; listas `tab.cone_*` e `tab.conjunto_*` |
| 510–560 | cultura (só 560); listas `tab.*` do gerador |
| 600, 610, 630 | faixa do grupo (só os ganchos rápidos de 600); listas `tab.*` |
| 620 | tipo de loja; blocos de 24.1–24.3 (Dados) |
| 640 | probabilidade; `tab.oraculo` |
| 650 | as 3 expressões (N, F, M, Vantagem) |
| 701–710 | a própria tabela e "quantos sortear" |
- **Peso:** os sorteios são uniformes. Peso é repetir a entrada na lista (o Mestre faz isso na aba Tabelas). As únicas tabelas com faixas de d20 (oráculo sim/não) guardam as faixas como números na aba Tabelas.
- **Editar a lista muda o sorteio** — esperado e dito no guia: o resultado é função da semente **e** da lista.
- **Dependência entre geradores** é explícita e só "para baixo": a aventura sorteia o antagonista pelo bestiário com o próprio G=300; o NPC não lê a aventura. Assim um gerador nunca muda porque outro rolou.

---

## 6. Mapa de abas e conteúdo

Convenções de todas as abas: linha 1 título "‹Aba› — Explorando Galáxias v1.1" (A:L), linha 2 legenda, linha 3 subtítulo; blocos com título azul; tabelas com cabeçalho de coluna; coluna de avisos à direita da área (K:L, como na ficha); colunas auxiliares (sorteio `u/y/x`, contadores, chaves de ordenação) à direita de L, **ocultas**, como na ficha (D11; nenhuma entrada fica em coluna oculta, e o lint confere isso). Tabelas largas seguem a regra das sub-tabelas de D11. Toda `MATCH/INDEX/VLOOKUP`/divisão é protegida por `IF(x="","",…)` e/ou `IFERROR(…,"")`. "Sortear" é sempre a primeira opção das listas suspensas dos geradores, e vazio = "Sortear".

### 6.1 Início

- **Comece por aqui:** 8 passos curtos (importar, preencher Campanha e Grupo, preparar com Encontros/NPCs/Aventuras, jogar com Combate, registrar em Sessões/Missões, imprimir o Escudo).
- **Semente da campanha** (entrada) e **semente efetiva** (calculada, 5).
- **Painel** (calculado): campanha, sessão atual, nível e faixa do grupo, PH do grupo (16.2), missões ativas (COUNTIF "Ativa"), relógios a 1 segmento de encher, próxima Ressonância (5/10/15/20), sessões no nível atual × ritmo sugerido (26.1), próxima sessão preparada (título).
- **Índice das abas:** uma linha por aba com "para que serve" e "quando usar".
- **Painel de avisos:** uma linha por aba, contagem `SUMPRODUCT((LEN(intervalo)>0)*1)` dos avisos e o primeiro aviso (`INDEX/MATCH` do primeiro não vazio via contador auxiliar).
- **Importar no Google** e **proteger fórmulas** (texto curto, igual ao da ficha).

### 6.2 Campanha

- **Mesa** (entradas): nome da campanha; nº de jogadores (1–6; 3–6 é a tabela de 16.2 — fora disso aviso e conta com o limite); **nível do grupo** (1–20; fonte única, D9); sessão atual; dia de campanha (inteiro ≥ 1); método de atributos (lista: Array oficial / Compra de Pontos); variantes (PV rolado, média impressa, outra).
- **Calculadas:** faixa (`1-4`…`17-20` por `INT((nível−1)/4)`), Eficiência (02.3), PH máximo e de início (16.2, lido de `dados.ph`), DT da faixa (linha Média e Difícil, 27.2), DT de Fraqueza da faixa (20.2), equipamento de faixa esperado (Cone máximo e Tier, 25.1, com virada de Tier no 7 e no 18), verba de marco do próximo nível (24.5).
- **Marcos e progressão (26.1):** sessões jogadas no nível atual (entrada), ritmo sugerido (2–4 sessões por nível nos níveis 1–8; 4–6 depois) com aviso "Ritmo acima do sugerido" quando passar; próxima Ressonância e o lembrete "sempre marco de história (26.7)"; texto fixo "Não existe experiência por inimigo derrotado (26.1)".
- **Facções e reputação** (12 linhas): facção (lista com as 8 de 27.16 + texto livre), atitude com o grupo (lista −3 a +3, H17), relógio ligado (nome), notas, último contato (sessão). Calculado: rótulo da atitude ("−3 Inimiga declarada"… "+3 Aliada"), aviso se facção repetida.
- **Relógios de progresso** (10 linhas, H16): nome, segmentos (lista 4/6/8/10/12), preenchidos (0–segmentos), o que acontece ao encher. Calculado: barra `REPT("●",n)&REPT("○",s−n)` + "n/s", situação ("Cheio — aconteceu" / "Falta 1"); aviso se preenchidos > segmentos.
- **Linha do tempo** (30 linhas): dia de campanha, sessão, evento, quem (facção/NPC), consequência, público? (Sim/Não). Calculado: ordem crescente por dia (coluna "nº na ordem" com `COUNTIF` + desempate pela linha) e o bloco "Próximos eventos agendados" (os 5 primeiros com dia ≥ dia atual, via SMALL/INDEX/MATCH).
- **Ficha de Decisões da Mesa (29.11)**: os campos de 29.11 como entradas — Habilidades e Ultimates aprovadas com ajuste (10 linhas: quem, nome, o que foi ajustado, por quê), regras decididas na mesa (10), armas/itens/efeitos caseiros aceitos (8), nomes que a mesa criou (10). Topo com a frase de 27.11 "a decisão de hoje é precedente amanhã" e o "vai / não vai para a ficha".
- **Sessão Zero** (checklist de entradas Sim/Não com nota): tom e temas e limites da mesa (os dois itens são **H24**: prática geral de RPG que o livro não traz; rotulados "Sugestão da planilha — não é regra do livro (H24)"); método de atributos (03); tamanho da mesa → PH (16.2); variantes (06.4, 28.3 média); Regra de Ouro (27.1); "falhe para frente" (02); Propósito de Vida de cada PJ ligado a um gancho (27.18, 03); a casa do grupo (Expresso Astral, 27.15); o que o livro não cobre (27.19); como se sobe de nível (26.1); recompensa de marco, sem compra de Relíquia (25.1).

### 6.3 Grupo

Até **6 PJs**, uma linha por PJ, em **4 sub-tabelas de 6 linhas** (D11). Na G1 a coluna A é o Nome (entrada); nas outras, A repete o Nome.

| Sub-tabela | B…J (≤ 9 campos) | K:L |
|---|---|---|
| G1 Quem é (entradas) | Jogador, Raça, Caminho, Elemento, Propósito de Vida (F:H mesclado), crença do Esforço (I:J mesclado) | aviso |
| G2 Números de combate (entradas) | PV máx., Defesa, Esquiva, RD, VEL, Bônus de Agilidade, Bônus de Discernimento, Bônus de Presença, DT das Habilidades | aviso |
| G3 Equipamento de faixa (entradas) | Nível do Cone, Tier de Relíquias, slots que possui, Sobreposições nesta faixa, total de Sobreposições no Cone atual (com as de faixas anteriores; revisão da Fase 2, F1), Ressonâncias escolhidas (G:J mesclado) | aviso |
| G4 O que a Raça e o equipamento mudam (calculada) | Morrendo com Vantagem?, pode ser Executado?, Esforço?, Intellitron (Fraqueza), Surpresa / Raposa Astuta (Vulpes), "Tô na sua mente" (Haloviano), Cone/Tier contra a faixa (G:J mesclado) | aviso |

**Entradas** (digitadas da ficha de cada jogador, com o nome da célula da ficha no cabeçalho, ex. "PV máx. (Em Jogo)"): Nome, Jogador, Raça (lista 05), Caminho (lista 06), Elemento (lista 20.1), PV máximo, Defesa, Esquiva, RD, VEL, Bônus de Agilidade, Bônus de Discernimento, Bônus de Presença, DT das Habilidades, Propósito de Vida, Nível do Cone de Luz, Tier de Relíquias, slots de Relíquia que possui (0–6), Sobreposições recebidas nesta faixa (0–2), total de Sobreposições no Cone atual (0–5, conta as de faixas anteriores, 25.2), Ressonâncias escolhidas (texto), crença do Esforço (Humano). O nível vem da Campanha (o grupo sobe junto, 26.1).

**Calculadas e avisos por PJ:** Morrendo com Vantagem (Xianzhouíta, Vulpes, Avginiano — 23.5); não pode ser Executado (Xianzhouíta — 05, 23.5); Esforço (só Humano — 05); Intellitron descobre Fraqueza com Vantagem e 2 por sucesso (05, 20.2); DT de Surpresa 13 e Raposa Astuta DT 10 (Vulpes); To na sua mente (Haloviano, DT 13 de ativação fora da Harmonia); Cone acima do máximo da faixa (aviso, 25.1); Cone ou Tier abaixo do esperado (aviso "abaixo do orçamento: encontros ficam mais duros — 27.8"); Sobreposição > 1 nesta faixa (aviso, 25.2); total no Cone acima do teto do Nível do Cone ou menor que as desta faixa (aviso, 25.2); VEL fora dos extremos absolutos da fórmula, 7 a 25 (aviso "confira na ficha — 19.1"; a "faixa esperada" de 19.1 só é dada nos níveis 1, 10 e 20 e aparece como texto, sem aviso, para não interpolar regra); Elemento repetido no grupo (informação, para a regra irmã de 27.5).

**Resumo do grupo** (calculado): nº de PJs (COUNTA dos nomes) — e aviso se diferente do nº de jogadores da Campanha; Elementos distintos do grupo (lista de 7 com Sim/Não e contagem); PH máx./início (16.2); Elementos em dobro (para a regra irmã); presença de Intellitron, Humano (Esforço), Preservação/Abundância (sustentação, 27.7).

### 6.4 Sessões

- **Preparar a próxima sessão** (entradas): nº, data real, título, objetivo da sessão, **5 cenas planejadas** (tipo: social/exploração/combate/viagem/descanso; descrição; encontro ligado — lista com os 3 encontros salvos de Encontros; NPCs presentes; DT principal — lista Trivial…Heroica, com o número da faixa **do desafio** calculado ao lado, 27.2 regra 1), **segredos e pistas** (10 linhas: pista, revelada? Sim/Não), recompensas planejadas (texto + link "ver Recompensas"), ganchos de Propósito de Vida (um por PJ, com o nome do PJ puxado do Grupo).
- **Checklist de preparo** (calculado + entradas Sim/Não): orçamento conferido (27.4); contrato da Fraqueza cumprido (puxa o resultado de cada encontro ligado); relógio na ficção para o Descanso Longo (27.7); nº de combates do dia (2 tranquilo / 3 de verdade / 4 emergência, 27.7) com aviso no 4º; equipamento de faixa entregue se houve virada (25.1).
- **Diário** (30 linhas, cabeçalho repetido): nº, data real, dia de campanha, resumo (até 300 caracteres), marco atingido? (Sim/Não), decisões importantes, ganchos abertos, NPCs que apareceram. Calculado: total de sessões, sessões desde o último marco (conta "Não" desde o último "Sim").

### 6.5 Missões

20 linhas: missão, tipo (lista de aventuras), contratante, objetivo, local, prazo (texto), estado (lista: Oferecida / Ativa / Concluída / Falhou / Abandonada), recompensa combinada, é marco de nível? (Sim/Não), sessão de início, sessão de fim, notas. As colunas de "missão" a "recompensa" estão na **mesma ordem da linha de saída da aba Aventuras** (D6). Calculado: contagem por estado; aviso "Concluída sem sessão de fim"; aviso informativo "Mais de 3 missões Ativas: o grupo pode perder o fio — Sugestão da planilha (H23)".

### 6.6 NPCs (R5)

**Gerador** (G=200). Entradas: Rolagem nº; Raça (lista: Sortear + as 7 de 05); Caminho (Sortear + 9 + "Nenhum"); papel na história (lista: Sortear, Aliado, Contratante, Rival, Neutro, Informante, Vítima, Antagonista); faixa do bloco de combate (lista: Nenhum, 1-4…17-20, "Do grupo"); tipo do bloco (Comum/Elite). Saídas, uma por linha, cada uma com o sorteio próprio (`C` entre parênteses):

| Campo | Fonte do sorteio | Observação |
|---|---|---|
| Raça (1) | lista `racas` | só se "Sortear" |
| Nome (2) + sobrenome/epíteto (3) | `tab.nome.<raça>` e `tab.sobrenome.<raça>` | a lista escolhida depende da Raça **resultante** por `CHOOSE(MATCH(raça, racas,0), …)` sobre as 7 colunas (sem INDIRECT) |
| Caminho (4) | lista `caminhos` + "Nenhum" | o resto da galáxia não segue Caminho com afinco (27.12): "Nenhum" aparece 3 vezes na lista de sorteio por padrão (H11) |
| Ocupação (5) | `tab.ocupacao` (≥ 40) | |
| Aparência (6, 7) | `tab.aparencia_traco` (≥ 30) duas vezes; o 2º sorteio usa `escolha_sem_repetir` (seção 5: `MOD(i₁ − 1 + j, n) + 1`, j de 1 a n−1) | 2 traços: quantidade de saída, H25 |
| Personalidade (8) | `tab.personalidade` (≥ 30) | |
| Motivação (9) | `tab.motivacao_<caminho>` (5 por Caminho, ecoando a leitura de 27.12 "cada facção é um Caminho levado a sério") + `tab.motivacao` geral (≥ 30) quando Caminho = Nenhum | |
| Segredo (10) | `tab.segredo` (≥ 30) | |
| Maneirismo / voz (11) | `tab.maneirismo` (≥ 30) | |
| Atitude inicial (12) | `tab.atitude` (Hostil, Desconfiado, Indiferente, Cordial, Prestativo; H11) | |
| Gancho (13) | 50%: os 4 ganchos de 27.18 da faixa do grupo; 50%: `tab.gancho_npc` (≥ 30) | a escolha entre as duas fontes é o campo 14 (`inteiro(x, 1, 2)`); a divisão 50/50 é **H20**, rotulada |
| Bloco de combate | âncoras 28.3 da faixa × tipo (se pedido), com o aviso "NPC aliado também usa as âncoras de 28.3; Execução: ser racional pode Executar (23.5)" | regra do livro |

**Linha de saída** (para copiar): Nome completo, Raça, Caminho, Ocupação, Aparência, Personalidade, Motivação, Segredo, Maneirismo, Atitude, Gancho, Papel.

**Elenco da campanha** (30 linhas, cabeçalho repetido a cada 10): as 12 colunas acima (entrada) + Onde está, Relação com o grupo (lista −3 a +3), Vivo? (Sim/Não), Sessão em que apareceu, Notas. Aviso: nome repetido no elenco; nome igual a criatura do bestiário.

**Cartões de NPC (R13):** 4 cartões lado a lado (A:L), cada um com uma entrada "NPC" (lista do elenco) e o cartão calculado (nome, Raça · Caminho · ocupação, aparência, voz, quer, esconde, atitude). Área de impressão própria, A4 paisagem.

### 6.7 Inimigos (R1)

#### 6.7.1 Inimigos da campanha (o criador, uma linha por inimigo)

**12 linhas** (um inimigo por linha), em **4 sub-tabelas de 12 linhas** e uma tabela de fases (D11). A linha *i* é sempre o inimigo *i*. Na I1 a coluna A é o Nome (entrada); nas outras, A repete "i · Nome".

| Sub-tabela | B…J (≤ 9 campos) | K:L |
|---|---|---|
| I1 Conceito (entradas) | Modo, Base do bestiário, Faixa, Nível, Tipo, Facção/origem, Elemento dos ataques, Ser racional?, Fases | aviso |
| I2 Fraquezas e Fila (entradas + sugestão) | Fraqueza 1, 2, 3, 4 (vazia = sugerida, mostrada ao lado como "(sugerida)" na I4), Resistência, Comportamento na Fila (G:J mesclado) | aviso |
| I3 Ficha — números (calculada) | Faixa efetiva, PV, Defesa, RD, Tenacidade, VEL, Ataque, DT dos efeitos, Teste de Resistência | rótulo H1 quando o modo é Por nível |
| I4 Ficha — dano e regras (calculada) | Dano por acerto (B:C mesclado), nº de Fraquezas pela regra, Fraquezas efetivas (E:G mesclado, com "(sugerida)"), Firmeza, ações agressivas, Custo no orçamento | rótulo H12 quando há Fraqueza sugerida |
| I5 Fases dos inimigos criados (24 linhas = 12 × fases 2 e 3, em 2 blocos de 12) | Inimigo (lista dos 12), Fase (2/3), Fraqueza 1–4 da fase, Tenacidade da fase (≤ âncora — 28.5 regra 3), ritmo (texto, H:J mesclado) | aviso: fase para inimigo sem Fases ≥ 2; Tenacidade acima da âncora; Fraquezas iguais às da fase anterior ("as Fraquezas mudam — 28.5 regra 4", informativo) |

Na fase 1 de um Boss criado valem as Fraquezas da I2. No modo Ajustar, as fases vêm da base (`dados.bestiario_fases`) e a I5 fica vazia para aquele inimigo (se preenchida, ela vence a base e o aviso diz isso). Os limiares das fases criadas seguem H4.

Entradas por linha: Nome (até 40); **Modo** (lista: "Faixa do livro" [padrão quando vazio], "Por nível — Sugestão", "Ajustar do bestiário"); Base do bestiário (lista dos 32; só no modo Ajustar); Faixa (lista; vazio = faixa do grupo) **ou** Nível (1–20, só no modo Por nível; vazio = nível do grupo); Tipo (Comum/Elite/Boss; no modo Ajustar vem da base se vazio); Facção/origem (lista 27.16 + "Fragmentum", "Stellaron", "Emanador", "Outra"); Elemento dos ataques (lista 20.1; vazio = Físico); Fraquezas 1–4 (lista 20.1; vazias = "sugeridas", 6.7.2); Resistência (lista 20.1 ou vazio); Ser racional? (Pode Executar / Não Executa); Fases (1–3; só Boss); Comportamento na Fila (texto, 28.4 passo 6).

**Calculadas por linha** — o bloco de 15 campos de 28.1: Faixa efetiva; PV; Defesa; RD; Tenacidade; VEL; Teste de Ataque (+X); Dano por acerto (`4d8 + 1 · média 19`); DT dos efeitos; Teste de Resistência (+X); nº de Fraquezas pela regra (Comum 1–2, Elite 3, Boss 4 — 20.2/28.2 regra 7); Fraquezas efetivas; Firmeza (Elite/Boss: "com Firmeza"; Comum: "sem Firmeza" — 28.2 regra 3); ações agressivas (28.2 regra 5); Na Fila: "VEL n, com/sem Firmeza"; Custo no orçamento (= PV, 27.4).

Fórmulas-chave:
- **Faixa do livro:** `INDEX(dados.ancoras.<coluna>, MATCH(faixa&"|"&tipo, dados.ancoras.chave, 0))` (a aba Dados tem a coluna-chave "1-4|Comum").
- **Por nível (H1, revisão 1):** **só o PV** é interpolado entre os níveis de referência 3/7/11/15/19 (29.1). `k = MIN(4, MAX(1, INT((L−3)/4)+1))`; `v = IF(L<=3, a₁, IF(L>=19, a₅, a_k + (a_{k+1}−a_k)*(L−(4k−1))/4))`; resultado `INT(v)`. **Todos os outros números, inclusive o Dano por acerto (expressão e média), são a âncora da faixa do nível, sem ajuste.** Motivo: o Dano dá saltos proporcionais muito maiores que o PV entre as faixas 1-4 e 5-8 (Comum 3 → 7, Elite 7 → 13, Boss 10 → 20). Interpolado, ele desviava até 33,3% da âncora (Comum nível 4), e o Dano é o número que calibra a Defesa do personagem e as "4 a 7 pancadas" (28.3, primeira leitura). Ele fica exatamente como o livro imprime. O custo no orçamento é o PV interpolado (27.4: custo = PV). O rótulo "Sugestão da planilha — não é regra do livro (H1)" aparece só na célula de PV da linha.
- **Ajustar do bestiário:** números = âncoras da faixa nova (regra 28.4 passo 3: "copie a linha"); Fraquezas, Resistência, Execução, fases e ações vêm da base (troca livre de Fraquezas é regra: 28.2 regra 7); ações reescritas pelos marcadores (6.7.3).
- **Avisos:** mais Fraquezas que a regra do tipo ("Elite tem 3 Fraquezas — 20.2"); Fraqueza repetida; Resistência igual a uma Fraqueza; Resistência ao Elemento de 2+ PJs ("nunca aponte uma Resistência para o Elemento de dois personagens — 27.5"); Fases em Comum/Elite; nome repetido ou igual a criatura do bestiário; nível fora de 1–20; modo Ajustar sem base.

#### 6.7.2 Fraquezas sugeridas (G=110, H12)

Quando as Fraquezas de uma linha estão vazias, a planilha sugere o número da regra do tipo escolhendo **primeiro Elementos do grupo que ainda faltam** para o contrato de 27.5 entre os inimigos da campanha, e depois os demais, sorteando a ordem com G=110, C=linha (campo de Rolagem nº único da tabela). A coluna mostra "(sugerida)" ao lado. Para Comum, o nº sugerido é 2 (ponta alta de 1–2). Isto é ajuda de montagem; o número de Fraquezas é regra, **quais** são é decisão do Mestre (28.1 campo 13). A ordem de preferência e o "Comum = 2" são **H12**, com rótulo na I4 e registro em `sugestoes`.

Método exato (para o oráculo): (1) faltantes = Elementos do grupo (Grupo, coluna Elemento) que ainda não são Fraqueza de nenhuma linha **anterior** de Inimigos da campanha (linhas 1…i−1, com Fraquezas digitadas ou sugeridas). Só olhar para trás evita referência circular. (2) Ordem dos 7 Elementos *e* = 1…7 (ordem de 20.1): chave_e = `IF(faltante_e, 0, 2147483647) + x_e + e/10` (x_e é o sorteio de G=110, C = 10·i + e; a chave fica < 2³³). A Resistência da linha recebe chave 9·10⁹, e assim fica sempre por último. (3) A j-ésima Fraqueza sugerida = o Elemento cuja chave é `SMALL(chaves, j)` (via `MATCH` exato), para j = 1…k, com k = 2, 3 ou 4 pelo tipo. Tudo isso em 7 colunas auxiliares ocultas por linha.

#### 6.7.3 Ficha detalhada e ações

Entrada "Ver ficha de" (lista: os 12 inimigos da campanha). Mostra o inimigo no **formato de cartão de 28.1** (uma linha de célula por linha do cartão: `NOME · Tipo · Facção · faixa`, `PV · Defesa · RD · Tenacidade · VEL`, `Ataque · DT dos efeitos · Teste de Resistência`, `Fraquezas · Resistências`, ataques, especiais, `Na Fila`), com área de impressão própria.

**Ações** (tabela de 36 linhas = 12 inimigos × 3, cabeçalho repetido a cada 12): Inimigo (lista dos 12), Tipo de ação (lista: Ataque normal; Especial de dano 1 alvo (até 1,5×); Especial de dano 2–3 alvos (dano cheio por alvo); Especial de controle; Reação), Nome, Alcance (lista 18.3: Pessoal, Curta, Média, Longa, Extrema), Elemento, Condição (lista 21.5 sem "Quebrado", "Surpreso", "Morrendo" — 28.4: "nada de condição nova"), Teste de Resistência do alvo (lista dos 6 TR de 04.6), Duração (turnos), Recarga (2/3 Ciclos; Ataque normal sem recarga). Calculado: **texto pronto** da ação na régua de 28.4 — ex.: "Trancafiar (recarga 2 Ciclos): o alvo faz Teste de Reflexos contra DT 17; se falhar, recebe Lentidão por 2 turnos." — com o dano certo (normal, 1,5× de `dados.dano_especial`, ou cheio por alvo) e a DT da ficha. Avisos: especial sem recarga; Comum com especial de 1,5× em alvo único (a régua permite, mas informa "pico de dano: ocupa a ação do turno — 28.4"); mais de 3 especiais por inimigo (28.1: 1 a 3); condição de controle com dano aumentado (28.4: "use o Dano por acerto normal").

Inimigos no modo **Ajustar** usam as ações da base, reescritas a partir do **texto-modelo** de `dados.bestiario_acoes`. Marcadores (substituídos por fórmula com aninhamento de `&`, sem SUBSTITUTE — que não está na lista branca: o texto-modelo é guardado já **partido** em até 6 pedaços literais intercalados com até 5 marcadores, colunas `p0, m1, p1, m2, p2 …`):

| Marcador | Vira | Regra |
|---|---|---|
| `{DANO}` | Dano por acerto da faixa nova (`3d8 + 3 · média 16`) | 28.4 passo 5 |
| `{DANO15}` | 1,5 × da faixa nova (`dados.dano_especial`) | 28.4 passo 5; H2 onde não há ficha |
| `{DANOC}` | Dano por acerto de **Comum** da faixa nova (ex.: o Sargento fala do dano dos Peões) | 28.4 |
| `{DT}` | DT dos efeitos da faixa nova | 28.3 |
| `{PV:n}` | `INT(n × PV novo ÷ PV original)` (limiares de fase, "metade dos PV (78)", "145 PV ou menos") | H3 |
| `{TEN:n}` | `INT(n × Tenacidade nova ÷ original)`, nunca acima da âncora (28.5 regra 3) | H3 |
| `{F2}`, `{F3}`, `{F2B}`, `{F3B}` | Limiares das fases: 2 fases → topo da fase 2 = `INT(PV/2)`, piso da fase 1 = topo + 1; 3 fases → `INT(2·PV/3)` e `INT(PV/3)` | H4 (reproduz as 5 fichas) |

Texto sem marcador fica como no livro (RD de Reação, acúmulos, número de casas, duração), e a ficha mostra "Números sem marcador são os do livro, na faixa original". Validação forte (suíte `bestiario`): renderizar as 32 criaturas **na própria faixa** reproduz, palavra por palavra, cada linha de ataque e de ação do `.md` (sem marcação markdown).

### 6.8 Bestiário (R2)

- **Filtro** (entradas): faixa (lista + "Todas"), tipo (lista + "Todos"), Elemento que é Fraqueza (lista + "Qualquer"), facção (lista + "Todas"), ambiente (lista H8 + "Todos"), só com Resistência? (Sim/Não), só com fases? (Sim/Não).
- **Resultado** (calculado, até 32 linhas). Para cada linha `i` da aba Dados, a coluna auxiliar `passa_i = AND(…filtros…)` e `ordem_i = IF(passa_i, faixa_i*1000 + tipo_i*100 + i, "")`. O total que passou é `N = SUMPRODUCT(ISNUMBER(ordem)*1)` (`COUNT` não está na lista branca), numa célula própria. A k-ésima linha mostrada é `IF(k>N, "", INDEX(…, MATCH(SMALL(ordem, k), ordem, 0)))`. O resultado vem em **2 sub-tabelas** (D11), cada uma com 32 linhas em blocos de 11 e cabeçalho repetido:
  - B1 Números: A = nome; B…J = tipo, faixa, facção, PV, Defesa, RD, Tenacidade, VEL, Ataque.
  - B2 Dano e Fraquezas: A = nome repetido; B:C = Dano por acerto (mesclado); D = DT; E = TR; F:H = Fraquezas da fase 1 (mesclado); I = Resistência; J = fases; K:L = Execução.
  - Contador "N de 32 fichas".
- **Ficha completa** (entrada "Ver criatura", lista dos 32): o cartão de 28.1 com todos os ataques, ações, fases (tabela "o que muda") e a frase. Texto lido de `dados.bestiario_acoes` montado na faixa original (igual ao livro).
- Rodapé fixo: "As Fraquezas sugeridas podem ser trocadas livremente para cumprir o contrato de encontro (28.2 regra 7). Os cinco inimigos com Resistência: Capataz Oco, Centurião Catafracto, Mestre de Cerimônias Mascarado, Executora de Contrato, Arcanjo de Ferro-Vazio (28.11)."
- O Bestiário é a fonte das listas suspensas de Encontros e Combate (com os inimigos da campanha).

### 6.9 Encontros (R3)

**Parâmetros** (calculados da Campanha/Grupo com campo de troca opcional): nº de PJs, nível e faixa do grupo, Elementos do grupo.

**Orçamento** (27.4): orçamento da faixa; dano do grupo por Ciclo; se nº de PJs ≠ 4, orçamento e dano × nº/4 com rótulo H5 (a tabela do livro é de 4 personagens, 29.1).

**3 encontros salvos (A, B, C)** — cada um com nome, ambiente (texto) e **8 linhas**: criatura (lista: inimigos da campanha + bestiário; procura primeiro nos da campanha), quantidade (0–10), Fraquezas trocadas (entrada opcional "Fraquezas nesta cena", 4 listas; vazias = as da ficha). Cada encontro vem em **2 sub-tabelas de 8 linhas** (D11): E1 Montagem: A:B = criatura (mesclado, entrada), C = quantidade, D…G = Fraquezas nesta cena 1–4, H = tipo, I = PV, J = custo; E2 Leitura: A = criatura repetida, B = faixa, C:F = Fraquezas efetivas (mesclado), G = Resistência, H = ações agressivas, I:J = Execução/notas, K:L = aviso. Calculado por linha: tipo, faixa, PV, custo (= PV × quantidade; **Escória de Stellaron custa 1,5 × PV** — ficha de 28.10), Fraquezas efetivas, Resistência, ações agressivas por Ciclo (Comum 1, Elite 1,5, Boss 2 × quantidade — 28.2 regra 5). Totais e leituras:

- **Custo total** e **% do orçamento**; **Ciclos estimados** = custo ÷ dano do grupo por Ciclo (é a própria definição do orçamento em 27.4: orçamento = dano do grupo em 4 Ciclos), +1 Ciclo se o contrato não for cumprido (27.5) — rótulo H7.
- **Leitura de dificuldade** (H6): ≤ 60% "Cena de passagem — cerca de 2 Ciclos (27.4)"; 60–115% "Encontro típico — 3 a 5 Ciclos (27.4)"; 115–160% "Pesado — Sugestão da planilha"; > 160% "Dois orçamentos num só encontro: passa de 6 Ciclos (27.4)".
- **Composição reconhecida** (27.4): se bate com 1 Boss + 1 Comum, 1 Elite + 4 Comuns, 3 Elites ("a mais pesada em dano recebido") ou 7 Comuns ("a mais rápida"), mostra a linha da tabela com a duração esperada.
- **Contrato da Fraqueza** (27.5): Elementos do grupo que aparecem como Fraqueza entre os inimigos (lista de 7 Sim/Não + contagem); ≥ 3 = "Contrato cumprido"; < 3 = aviso "Contrato não cumprido: encontro deliberadamente mais duro, cerca de 1 Ciclo a mais (27.5)" e as três saídas de 27.5 em texto.
- **Regra irmã** (27.5): aviso se alguma Resistência da cena aponta para um Elemento que 2+ PJs têm.
- **DT para descobrir Fraqueza** da cena = a da faixa do inimigo mais forte (20.2, "nível misto usa a faixa do mais forte"); lembrete do Intellitron se houver no grupo.
- **Avisos de ficha:** Pretor Vazio-Nove ou Dramaturgo com acompanhantes ("monte sozinho: os reforços são o que ele tem em vez de acompanhantes — 28.7/28.8"); Germe de Pavor com Comuns ("o Parto falso traz os Comuns — 28.11"); inimigo de faixa diferente da do grupo (informação, 28.4 passo 1: "a faixa do inimigo é a faixa do grupo").
- **Attrition de referência** (27.7) da faixa e o lembrete "2 combates por dia é tranquilo, 3 é de verdade, 4 é emergência".
- **Sem XP:** texto "Progressão por marco narrativo; não existe experiência por inimigo derrotado (26.1). Recompensas: aba Recompensas."

**Encontro aleatório** (G=100): entradas Rolagem nº, ambiente (lista H8 + "Qualquer"), faixa (vazio = do grupo), composição (Sortear + as 4). Sorteio: composição (C=1); para cada vaga de tipo da composição, uma criatura do tipo e da faixa no ambiente (C=2…8; sem nenhuma no ambiente, cai para "qualquer ambiente da faixa" e diz isso). As Fraquezas sugeridas da saída são as das fichas; a planilha mostra se o contrato fecha e, se não, **quais Fraquezas trocar**. É a **H19**, determinística, sem sorteio e com rótulo. As vagas da saída são percorridas na ordem (1…8) e, dentro de cada inimigo, as Fraquezas na ordem da ficha. A primeira Fraqueza que não é Elemento do grupo vira o primeiro Elemento do grupo ainda faltante, na ordem de 20.1. Isso se repete até cobrir 3 Elementos do grupo ou acabar as Fraquezas trocáveis. Nunca se troca a única Fraqueza que já cobre um Elemento do grupo, nem se cria Fraqueza igual à Resistência do inimigo. A troca é livre pela regra (28.2 regra 7); a escolha de *qual* trocar é a heurística. Também é heurística a composição sortear as 4 de 27.4 com peso igual (H11). A saída tem as colunas dos encontros salvos, para copiar para A, B ou C.

### 6.10 Combate (R4)

Tela principal em A:L ≤ 1360 px. Tem as tabelas de combatentes, a Fila, os recursos e a calculadora. Cada tabela é dividida em **sub-tabelas por assunto** (D11). O rótulo do combatente (ex. "Nadir", "Larva Fuliginosa 2") fica na coluna A de todas, e a linha *i* de cada sub-tabela é sempre o combatente *i*. A ordem na aba é a ordem de uso no turno:

| Sub-tabela | Linhas | B…J (≤ 9 campos) | K:L |
|---|---|---|---|
| C0 Controle | 1 | Ciclo atual, Carregar encontro, Surpresa, PH atual, PH máx. (calc.), início do combate (calc.) | aviso |
| C1 PJs — PV e Energia | 6 | Participa?, Ajuste de VEL, VEL efetiva (calc.), PV máx. (calc.), PV atual, Dano agora, PV depois (calc.), Energia, Ultimate pronta? (calc.) | aviso |
| C2 PJs — Morrendo e recursos | 6 | Ultimate usada neste Ciclo, Esforço disponível, Sucessos, Falhas, Rolagem do Morrendo (F:G, calc.), Situação (H:I, calc.), Pode ser Executado? (calc.) | aviso |
| C3 Inimigos — quem é | 10 | Do encontro (calc.), Trocar por (entrada), Tipo · faixa, Ataque, Dano por acerto (F:G), DT · TR, Firmeza, Execução | aviso |
| C4 Inimigos — PV e fase | 10 | Ajuste de VEL, VEL efetiva, PV máx., PV atual, Dano agora, PV depois, Fase da barra (calc.), **Fase em vigor** (entrada), Fraquezas em vigor (calc.; a Resistência vai junto, no aviso) | aviso |
| C5 Inimigos — Tenacidade e Quebra | 10 | Tenacidade máx. da fase em vigor, Redução acumulada (entrada), Tenacidade atual, Elemento que quebrou, Quem quebrou, Dano de Quebra (G:I, calc.), Defesa atual | aviso |
| C6 Inimigos — recargas | 10 | Especial 1: nome, usada no Ciclo, disponível?; Especial 2: idem; Especial 3: idem | aviso |
| C7 Condições | 48 (16 × 3), blocos de 12 | Combatente (lista), Condição, Turnos restantes, Acúmulos, Quem aplicou, Efeito (G:H), Dano da condição (I:J) | aviso |
| C8 Fila — entradas | 16, blocos de 10 + 6 | VEL efetiva (calc.), Ordem entre empatados (PJ), Atraso deste Ciclo, Atraso pendente do Ciclo anterior, Avançar, Avanço Total, Já agiu?, Casa manual, Pendente para o Ciclo seguinte (calc.) | aviso |
| C9 Fila do Ciclo / Fila prevista | 16, blocos de 10 + 6 | A:E = Ciclo atual (casa, nome, VEL, já agiu, "agindo agora"); G:J = próximo Ciclo (casa, nome, VEL, pendente aplicado) | — |
| C10 Calculadora | 1 entrada + 1 saída | as entradas e saídas descritas abaixo, em 2 linhas de 9 campos | aviso |

Chaves de ordenação, `passa`, contadores e expansão do encontro carregado ficam em colunas ocultas à direita de L.

**Controle:** Ciclo atual (entrada, inteiro ≥ 1; vazio = 1); "Carregar encontro" (lista: Nenhum, A, B, C, Aleatório); surpresa (lista: Ninguém, Grupo surpreendido, Inimigos surpreendidos) — só vale no Ciclo 1 (19.3).

**PJs (6 linhas, calculadas do Grupo):** nome; participa? (entrada Sim/Não, vazio = Sim se o nome existe); VEL base (Grupo) + ajuste de VEL (entrada −10…+10, buffs/debuffs que entram na remontagem — 19.3 passo 3); PV máx.; **PV atual** (entrada; vazio = máximo); Dano agora (entrada; negativo = cura) → "PV depois" calculado (cura não passa do máximo, 23.2; mínimo 0) — o Mestre digita o "PV depois" no PV atual (decisão 5 da ficha); Energia (entrada 0–100) e "Ultimate pronta" (≥ 100; 80 com Ressonância IV não é calculado — o Mestre marca); Ultimate usada neste Ciclo (Sim/Não; segunda = aviso, 27.10); Esforço disponível (Humano; Sim/Não); **Morrendo** (liga com PV atual = 0): sucessos (0–3) e falhas (0–3) entradas; calculado: rolagem "d20 + Presença (+X), sem Eficiência" com "com Vantagem" pela Raça (23.4–23.5), situação "Estabiliza com 1 PV" (3 sucessos) / "Morre" (3 falhas) / "Recebeu dano: +1 falha (2 se crítico ou Habilidade de Nível 5+)" como lembrete; aviso "PV 0 e Morrendo: X pode Executar" se há inimigo de pé com Execução "Pode" e o PJ não é Xianzhouíta (23.5).

**Inimigos (10 linhas):** "Do encontro" (calculado: o encontro carregado expandido por quantidade, na ordem das linhas) e "Trocar por" (entrada, lista: inimigos da campanha + bestiário); efetivo = troca se preenchida, senão do encontro. Rótulo calculado "Nome 2" quando o nome se repete (`COUNTIF` acima). Dados puxados (Inimigos da campanha primeiro, senão bestiário): tipo, faixa, PV máx., Defesa, RD, VEL, Ataque, Dano, DT, TR, Firmeza, Execução, fases. Entradas: ajuste de VEL; **PV atual** (vazio = máximo); Dano agora → PV depois (mínimo 0; 0 = "Derrotado — remova a casa, 19.7"); **Redução de Tenacidade acumulada** desde a última recuperação (entrada); **Fases do Boss (revisão 1, 28.5 regras 3 a 5):** são dois valores separados.
  - **Fase da barra** (calculada): a fase que o PV atual alcançou contra os limiares (`dados.bestiario_fases`, I5 ou H4). Ela **só acende o aviso**: "A barra cruzou o limiar da fase N. No **fim do turno do Boss** (não agora), digite N em 'Fase em vigor', apague a 'Redução acumulada' (a Tenacidade volta ao máximo — 28.5 regra 3) e anuncie as Fraquezas novas em voz alta (28.5 regras 4 e 5). A virada não gasta a ação dele".
  - **Fase em vigor** (entrada; vazia = 1; inteiro de 1 até o nº de fases): é ela que manda nas Fraquezas, na Tenacidade máxima, no ritmo e nas ações em vigor, e é dela que a calculadora lê. Assim, uma Habilidade de área resolvida no meio do Ciclo usa só as Fraquezas da fase antiga, e quem Atrasou o Boss ganha o Ciclo inteiro de fase antiga (28.5, "Por quê").
  - Avisos: fase em vigor maior que a da barra ("fase adiantada: a barra ainda não cruzou o limiar"); fase em vigor fora de 1…fases; Comum/Elite com fase ≠ 1.
  - Tenacidade máx. = a da **fase em vigor**, nunca acima da âncora de 28.3 (28.5 regra 3). **Tenacidade atual** = MAX(0, máx. − redução acumulada). Na virada, a volta ao máximo é o Mestre apagar a redução, o mesmo gesto da recuperação depois da Quebra. A célula pede isso no aviso da virada. Sem macro, a planilha não sabe se a redução foi apagada. **Quebra** quando chega a 0: as cinco coisas de 20.4 em texto, com "Elemento que quebrou" (entrada, lista) e "Quem quebrou" (entrada, lista dos PJs) → Dano de Quebra da Eficiência de quem quebrou (20.5; Eficiência pelo nível do grupo, 02.3): ex. "Fogo: 2d6 + 4 · média 11 + Queimadura (2d6 + 2 por turno, 2 turnos)"; Sangramento calculado `MIN(INT(5% × PV máx.), 3 × Eficiência)` (21.2); "Quebrado até o fim do próximo turno dele: −2 de Defesa e +1 dado de qualquer fonte" e Defesa atual com −2; "Tenacidade volta ao máximo no fim do próximo turno dele" (o Mestre zera a redução). Recargas: até 3 ações especiais da criatura (nomes puxados) com "usada no Ciclo" (entrada) → "volta no Ciclo X" e "disponível agora?" (Ciclo atual ≥ usada + recarga); Congelado em Elite/Boss bloqueia especial no turno seguinte (19.6, lembrete).

**Condições (tabela própria, 16 combatentes × 3 condições):** condição (lista 21.5 menos "Quebrado" — automático — e "Morrendo" — automático), turnos restantes (0–20), acúmulos (0–5), quem aplicou (lista dos combatentes). Calculado: efeito em uma linha (21.5), teto de acúmulo e aviso se passou (21.5: 5; Marcado 3), aviso "Congelado só em inimigo (21.2)" e "Quebrado não existe em PJ (20.3)" se a condição não cabe no alvo; dano da condição com a Eficiência de quem aplicou (expressão e média pela regra de 02). Os Danos Contínuos (20.6, 21.5) são Sangramento (com o PV máx. do alvo e o teto), Queimadura `2d6 + Ef`, Choque `1d6 + Ef` e Cisalhamento `1d6 × acúmulos`, com o lembrete "ignora RD, não crita, sem dados de Fraqueza". Mais as duas condições de dano de 21.5 que não são chamadas de Dano Contínuo: **Embaraço** `1d6 × acúmulos` (até 5; "os acúmulos só entram por ataques, antes do próximo turno do alvo; passado o turno dele, a condição resolve e sai"; **Atrasa 1 casa**) e **Aprisionamento** `1d6 + Ef` (**Atrasa 2 casas**). Nas duas, o texto de 21.5 aparece como está, sem inventar momento de resolução, junto com o lembrete "some o Atraso em 'Atraso deste Ciclo' do alvo (C8)". Lembrete: "Dano Contínuo aplica no início do turno do alvo; duração em turnos do alvo (20.6, 19.2)". Cura não remove condição (21.1).

**Fila de Ação** (19.3–19.6, D7). Por combatente ativo (participa, PV > 0 ou PJ Morrendo — 19.7 "mantém a casa"; inimigo derrotado sai):
- **Chave de ordenação** (coluna oculta; maior chave = casa mais cedo; revisão 1):
  `chave = VEL × 100000 + T_ag × 1000 + T_disc × 10 + T_tipo + T_linha`
  - **PJ:** `T_ag = Bônus de Agilidade + 20`, `T_disc = Bônus de Discernimento + 20` (dentro da chave, cada termo é limitado com `MIN(30, MAX(15, bônus + 20))`. A faixa válida é de −1 a +5, e um valor fora dela já acende o aviso "confira na ficha", 10.1. O limite só garante que um número digitado errado não desmonte a chave). `T_tipo = 5 + (5 − E)`, em que E é a "ordem entre empatados", de 1 a 5 (vazia = 5; 1 age primeiro), e o termo fica de 5 a 9. `T_linha = (10 − linha do PJ)/100`, com linha de 1 a 6.
  - **Inimigo:** `T_ag = 0`, `T_disc = 0`, `T_tipo = 0` (**sem o +20**), `T_linha = (20 − linha)/100`, com linha de 1 a 10.
  - Inimigo não tem Agilidade nem Discernimento (28.2). Por isso, no empate de VEL entre PJ e inimigo, a comparação de atributos de 19.3 passo 2 não se aplica, e vale a última cláusula: "os jogadores… vêm **antes** dos NPCs empatados". Com os termos do inimigo em 0, qualquer PJ (mesmo com Agilidade −1) vence o empate. Entre PJs vale 19.3 passo 2 inteiro (Agilidade, depois Discernimento, depois a escolha dos jogadores, E). Entre inimigos vale a ordem da linha (H13).
  - **Faixas sem sobreposição:** VEL efetiva vai de 0 a 40 (ajuste de ±10), então VEL × 100000 ≤ 4·10⁶. A soma dos outros termos fica < 30 × 1000 + 30 × 10 + 9,1 < 100000, e `T_disc × 10 + T_tipo + T_linha` ≤ 309,1 < 1000. Ou seja, um termo nunca invade o de cima.
  - O oráculo tem os casos: PJ com Agilidade −1 e VEL 13 contra Boss com VEL 13 (o PJ vem antes); dois PJs empatados em VEL e Agilidade, decididos pelo Discernimento; dois PJs empatados em tudo, decididos por E; dois inimigos iguais, decididos pela linha.
- Casa base = 1 + nº de ativos com chave maior.
- **Atraso deste Ciclo** (entrada, casas brutas somadas de todas as fontes) e **Atraso pendente do Ciclo anterior** (entrada). Efetivo: Comum `MIN(3, bruto)`; Elite/Boss com Firmeza `IF(bruto=0, 0, MIN(2, MAX(1, INT(bruto/2))))` (19.4, pelo total do Ciclo); Congelado: Comum é **retirado da Fila neste Ciclo** e os Atrasos pendentes contra ele são descartados; Elite/Boss = Atraso 2, que é o teto, e nada mais soma (19.6).
- **Avançar** (entrada, casas) só vale se "já agiu" ≠ Sim (19.5); Avanço Total = entrada Sim/Não, 1 por Ciclo (aviso na segunda).
- Casa no Ciclo = posição pela chave 2 = `casa base + atraso efetivo (+0,5 se > 0) − avanço (−0,5 se > 0) + linha/1000`, ordenada com `SMALL` + `MATCH`. Atraso que passa da última casa ou aplicado a quem **já agiu** vira **pendente do próximo Ciclo** (calculado e mostrado na coluna "pendente para o Ciclo seguinte", respeitando o teto — 19.4). Surpreso no Ciclo 1 = casa pulada (19.3).
- **Mostra:** a Fila do Ciclo atual (16 casas: nº, nome, VEL, "já agiu", marca **"agindo agora"** na primeira casa sem "já agiu"), as linhas "PENDENTES" e "CONDIÇÕES" no formato de 29.10, e a **Fila prevista do Ciclo seguinte** (casa base pelas VEL atuais + pendentes, sem os Atrasos deste Ciclo) — a "ordem dos próximos turnos" que o Mestre pediu, sem medidor de tempo (19.2: a Fila não usa divisão por Velocidade).
- **Avançar o Ciclo (4 linhas fixas):** (1) some 1 em Ciclo atual; (2) copie a coluna "pendente para o Ciclo seguinte" e cole como valores em "Atraso pendente do Ciclo anterior"; (3) apague "Atraso deste Ciclo", "Avançar", "já agiu", "Avanço Total" e "Ultimate usada"; (4) desconte 1 turno das condições de quem agiu.
- **Virar a fase do Boss (3 linhas fixas, ao lado de C4):** acontece no fim do turno do Boss, quando o aviso "a barra cruzou o limiar" está aceso. (1) Digite a fase nova em "Fase em vigor". (2) Apague a "Redução acumulada" dele: a Tenacidade volta ao máximo da fase nova. (3) Leia em voz alta as Fraquezas novas, que já aparecem em C4. A virada não gasta a ação dele (28.5 regra 5).
- H13: quando dois combatentes são movidos no mesmo Ciclo, a ordem final segue a chave 2 (o livro não define a interação); o Mestre pode digitar "casa manual" (entrada), que vence a calculada.

**Recursos do grupo:** PH atual (entrada; vazio = início do combate pela tabela de 16.2 — "começa cada combate com o máximo menos 2"); máximo; aviso se acima do máximo ou negativo ("não existe PH negativo — 27.10"); geração lembrada: +1 por Ataque Básico que acerta (1–8), +2 (9–20). Energia por PJ está na tabela dos PJs. Esforço (Humano).

**Calculadora de dano e Tenacidade (R13)** — a ordem de 23.1 e 20.2/20.3: alvo (lista de rótulos), fonte (Ataque Básico / Habilidade Nível 1–7 / Ultimate / Dano de Quebra / Dano Contínuo), nº de dados e faces base, bônus fixo, Elemento, crítico? (Sim/Não), dados extras de condição (Quebrado/Vulnerável/marcas, 0–5), resultado rolado (opcional). Calculado: Fraqueza/neutro/Resistência pelo alvo (Fraquezas da **fase em vigor**, nunca a da barra); dados = base (×2 no crítico, só os base) + 2 de Fraqueza ou −2 de Resistência (mínimo 1) + extras limitados a **+3** (teto de dados adicionais, sem contar a Fraqueza — 16.9/26.6); média; − RD do alvo (não em Dano Contínuo); mínimo 1; com o "resultado rolado", o dano final. Redução de Tenacidade: bruto da fonte (20.3: AB 1, Nível 1–2 = 2 … 7, Ultimate 5, DC 0) → total / metade arredondada para baixo mínimo 1 / 1 ponto; "só se acertou (20.3)". Mostra "Tenacidade depois".

### 6.11 Aventuras (R6)

Gerador G=300. Entradas: Rolagem nº; tipo (Sortear + `tab.tipo_aventura`, ≥ 12: resgate, escolta, investigação, infiltração, defesa de posição, caçada, entrega, sabotagem, negociação, exploração, fuga, contenção de Fragmentum, rastro de Stellaron, cobrança de dívida…); faixa (vazio = do grupo); facção do conflito (Sortear + 27.16).

| Campo (C) | Fonte | Base no livro |
|---|---|---|
| Tipo (1) | `tab.tipo_aventura` | — (H14) |
| Gancho (2) | os 4 ganchos de 27.18 da faixa (50%) ou `tab.gancho` (≥ 30); a fonte sai do campo C = 15 e a divisão 50/50 é **H20** | 27.18 ("cada um é uma primeira cena com um problema dentro") |
| Contratante (3) | facção (27.16) + "um(a) " & ocupação (`tab.ocupacao`) & " chamado(a) " & nome (`tab.nome.*`, Raça sorteada C=4) | 27.16 "Como usar" |
| Objetivo (5) | `tab.objetivo_<tipo>` (3 por tipo) | — |
| Local (6) | 6 locais de 27.17 (filtrados pela faixa quando o livro diz a faixa: Poço Sete 1-4, Ferro-Vazio alta, Hesperin 17-20) ou `tab.local` (≥ 30) | 27.17 |
| Antagonista (7) | criatura **Boss** da faixa da facção sorteada (bestiário); sem Boss da facção na faixa, um **Elite** da facção; sem nenhum, Boss da faixa (a cadeia de recurso Boss → Elite → Boss da faixa é **H22**, rotulada; sorteio uniforme entre os candidatos do degrau que achou) | 28.11, 27.16 |
| Complicação (8) | `tab.complicacao` (≥ 30) | 02 "falhe para frente" |
| Reviravolta (9) | `tab.reviravolta` (≥ 30) | — |
| Prazo / risco (10) | `tab.prazo` (≥ 20; "a nave parte ao amanhecer", "o lacre não aguenta mais um dia", "a escolta chega em seis horas" — os 3 de 27.7 abrem a lista) | 27.7 "ponha relógio na ficção" |
| Recompensa (13, 14) | verba de marco da faixa **da aventura** (24.5) + "equipamento de faixa se esta aventura fechar o arco" (25.1) + 1 consumível sorteado com G = 300 (C = 13) na lista de consumíveis da faixa da aventura (H9) + 1 pista (`tab.pista`, C = 14). Não lê nenhuma entrada da aba Recompensas (seção 5, parâmetros de G = 300) | 24.5, 25.1, 27.8 |

**Estrutura de cenas** (H14, rotulada): 5 cenas — (1) Gancho: cena social ou de descoberta com o gancho; (2) Investigação ou viagem: 1 Teste de Perícia da faixa do **desafio** (DT Média da faixa, 27.2) com falha para frente; (3) Primeiro encontro: composição sorteada de 27.4 (C=11) a 50% do orçamento ("cena de passagem", 27.4); (4) Complicação: a complicação sorteada + 1 encontro típico **ou** objetivo sem matar (27.7 "fugir com a carga, aguentar 3 Ciclos, chegar ao console"), C=12; (5) Clímax: o antagonista; lembrete do contrato da Fraqueza e de que o dia tem no máximo 3 combates (27.7). Cada cena mostra DT da faixa (Média/Difícil) e o orçamento correspondente.

**Linha de saída** na ordem das colunas de Missões (6.5).

### 6.12 Recompensas (R7)

**Entrega de marco** (regra, sem sorteio — 25.1, 27.8): entradas nível novo do grupo (vazio = nível da Campanha) e "o que aconteceu" (lista: Subiu de nível; Entrou em faixa nova; Fim de arco). Calculado:
- Verba de marco do nível ganho, para o grupo (24.5).
- Na virada de faixa: Cone de Luz máximo (Nível 1–5) e Tier de Relíquia da faixa, com as viradas de Tier nos níveis 7 e 18 (25.1); texto "cada personagem recebe o Tier da faixa nos slots que já possui e pode trocar o Cone".
- Ressonância nos níveis 5, 10, 15, 20 ("marco de história, escolhida na hora com o Mestre e não muda — 26.7") e as opções da Ressonância (26.7).
- **Sobreposição:** no máximo 1 por faixa, decisão do Mestre como marco narrativo (25.2, 27.8); mostra quantas o Grupo já recebeu nesta faixa (aviso se > 1), o total no Cone atual (com as de faixas anteriores) e o teto do Cone pelo Nível (Nível 1–2: 2; 3–4: 1; 5: 0 — 25.2). A Situação compara o total com o teto ("no teto" quando o total chega a ele; aviso acima dele) antes do limite de 1 por faixa.
- **Slot de Relíquia novo:** "quando a história entrega — decisão sua (25.1)".
- **O que não dar** (27.8, lista fechada em texto) e o lembrete "Não existe compra de Relíquia, sorteio nem economia de equipamento".
- "Como entregar sem que pareça planilha" (27.8, uma linha).

**Gerador de sabor de Cone de Luz** (G=410): nome do Cone (`tab.cone_nome_a` + `tab.cone_nome_b`, ≥ 30 cada, estilo "O Último Trem Para Casa"), memória que ele carrega (`tab.cone_memoria`, ≥ 30), Bônus Maior sugerido (lista de 25.2: PV, Defesa, VEL, Dano de AB/Habilidade/Ultimate, RD, um tipo de Teste), gatilho do Efeito Condicional (os 6 exemplos de 25.2 + `tab.cone_gatilho` ≥ 20). Números do Cone pela tabela de 25.2 no Nível da faixa ("+1 ou +10 PV, 1 vez por combate" etc.). Rótulo: "Sabor sorteado; o Cone é recompensa de marco escrita com o jogador (25.1, 25.2)".

**Gerador de sabor de Conjunto de Relíquias** (G=420): nome (`tab.conjunto_nome`, ≥ 20, estilo "Cinzas do Forno Parado"), origem (`tab.conjunto_origem` ≥ 20: "de um mesmo lugar, de uma mesma catástrofe, de um mesmo morto ilustre" — 25.3), bônus de 2 peças sugerido (as 4 opções de 25.3), efeito de 4 peças sugerido (os 2 exemplos de 25.3 + `tab.conjunto_4` ≥ 10).

**Achados de encontro** (G=400, H9 e H18, rotulados): entradas Rolagem nº, faixa, leitura de dificuldade do encontro (lista: Passagem/Típico/Pesado). Créditos achados = `INT(verba da faixa × fator)` com fator 5% / 10% / 15% (H18); 0–2 consumíveis de 24.3 (a quantidade, `inteiro(x, 0, 2)`, faz parte de **H9**; poções e itens comuns, com preço do livro; poção Pequena nas faixas 1-8, Média 5-16, Grande 13-20 — H9); 1 bugiganga (`tab.bugiganga`); 1 pista/informação (`tab.pista`, ≥ 20). Texto fixo: "Créditos são preço de referência, não economia; nada no balanceamento depende deles (24.5)".

**Tesouro do grupo** (25 linhas): sessão, item ou Créditos, quantidade, valor em Cr (+ entrada / − saída), com quem, notas. As 5 primeiras colunas na ordem da linha de saída dos achados. Calculado: saldo de Créditos; aviso se saldo < 0.

### 6.13 Mundos (R8)

- **Planeta ou local** (G=510): tipo (`tab.mundo_tipo` ≥ 20), condição marcante (`tab.mundo_condicao` ≥ 30), **as três perguntas de 27.17** respondidas por sorteio: qual Caminho está vencendo aqui (9 Caminhos), o que as pessoas comuns fazem de manhã (`tab.manha` ≥ 30), o que elas pararam de fazer (`tab.pararam` ≥ 30); presença (Stellaron / Fragmentum / nenhum — `tab.ameaca` com "nenhum" repetido, H11); facção presente (27.16); nome do lugar (`tab.lugar_a` + `tab.lugar_b`, ≥ 30 cada).
- **Estação** (G=520): função (`tab.estacao_funcao` ≥ 20: triagem, alfândega, estaleiro, hospital…, abrindo com Vértice-9 de 27.17 como modelo), dono (facção), problema atual (`tab.estacao_problema` ≥ 20), nome.
- **Nave** (G=530): nome (`tab.nave_a` + `tab.nave_b` ≥ 30), classe (`tab.nave_classe` ≥ 20), peculiaridade (`tab.nave_peculiaridade` ≥ 30), tripulação (nº e uma ocupação); lembrete "regras de nave e viagem não estão no livro: trate viagem como cena com Teste da faixa e falha para frente (27.15, 27.19)".
- **Facção nova** (G=540): nome (`tab.faccao_a` + `tab.faccao_b`), Caminho levado a sério (9), o que quer, método (`tab.faccao_metodo` ≥ 20), recurso (`tab.faccao_recurso` ≥ 20), "como usar" (`tab.faccao_uso` ≥ 20, no tom de 27.16); linha de saída nas colunas de Facções (Campanha).
- **Organização** (G=550) e **Nomes avulsos** (G=560: 10 nomes de uma cultura escolhida, de lugar, de nave e de organização, C=1…40).
- **As 8 facções e os 6 locais do livro** (consulta, lidos de Dados).

### 6.14 Improviso (R8, R13)

- **Rumores** (G=600): 3 rumores por rolagem (quantidade de saída, H25; `tab.rumor` ≥ 40, os 3 sem repetir pela sequência com passo de 6.17, `sorteio.varios_sem_repetir`; o mesmo vale para as 3 bugigangas e os 6 itens da loja), cada um com "verdadeiro?" sorteado (Verdadeiro / Meia-verdade / Falso, H11).
- **Ganchos rápidos:** 1 de 27.18 da faixa + 1 de `tab.gancho`.
- **Eventos e complicações** (G=610): evento de cena (`tab.evento` ≥ 30), complicação (`tab.complicacao`), "falha para frente" sugerida (`tab.custo_falha` ≥ 20: tempo, ruído, recurso, informação incompleta, complicação nova — 02, 27.1).
- **Loja** (G=620): tipo de loja (lista: Armas, Armaduras, Suprimentos, Farmácia, Mercado geral, Mercado da Frota de Jade), lojista (nome + Raça + maneirismo), estoque de **6 itens** sorteados sem repetição entre as linhas do livro para aquele tipo (24.1 armaduras, 24.2 armas por categoria com um exemplo de 24.2, 24.3 poções e itens), **preço do livro** ("os preços não escalam — 24.5"), quantidade 1–3 (H15), e 1 item fora do comum com "preço: o que o Mestre disser (24.5)". Nada de Cone nem Relíquia à venda (25.1), dito em texto.
- **Bugigangas sem efeito** (G=630): 3 por rolagem (H25; `tab.bugiganga` ≥ 50, no espírito do "crachá cortado ao meio" de 29.7).
- **Oráculo sim/não** (G=640, H10): pergunta (entrada texto), probabilidade (lista: Quase impossível, Improvável, 50/50, Provável, Quase certo). d20 sorteado + modificador (−6, −3, 0, +3, +6) → faixas: ≤ 3 "Não, e…", 4–7 "Não", 8–10 "Não, mas…", 11–13 "Sim, mas…", 14–17 "Sim", ≥ 18 "Sim, e…". Faixas como números em `tab.oraculo` (editáveis).
- **Rolador de dados** (G=650, R13): até 3 expressões `N d F + M` (N 1–20, F de 2/4/6/8/10/12/20/100, M −50…+50) e "Vantagem/Desvantagem" para d20; mostra cada dado (até 20 por expressão, C = 20·(expressão−1)+dado), total e a média pela regra de 02 (`INT(N·(F+1)/2) + M`). Rolagem nº própria.
- **DT rápida** (27.2): dificuldade (lista) × faixa do desafio → DT; lembrete das regras 1–3 de 27.2 e das 5 DTs fixas (27.3).

### 6.15 Escudo do Mestre (R10)

Aba de impressão, **A4 paisagem**, `fitToWidth=1`, área de impressão e quebras de página definidas pelo gerador (5 páginas; o design pedia 3, mas com o corpo em 9 pt o conteúdo pede 5, e cada página tem a altura de uma A4 paisagem ajustada à largura, ≤ 633 pt, conferida pelo lint). O Excel usa essas definições. O Google, ao importar, não usa, e por isso cada página começa com uma linha visível "— Escudo do Mestre · página N de 5 · título —", que serve de guia para as quebras personalizadas do diálogo do Google (guia, seção 11). Cada página cabe em A:L, com no máximo 40 linhas na altura padrão (conferido pela suíte `preview`). Todo número é **lido da aba Dados por fórmula** (fidelidade conferida pela suíte `dados` + `escudo`). Como foi implementado (revisão da Fase 3, F3; o título de cada página diz o que ela tem): Página 1 — "Preparar a sessão e o encontro; descanso": DT por faixa (27.2) e as 3 regras; as 5 DTs de subsistema (27.3); orçamento e custos (27.4) e as 4 composições; contrato da Fraqueza e regra irmã (27.5; 28.2 regras 5 e 7); Ultimate por faixa (27.9); "Para o grupo agora"; Descanso (23.6). Página 2 — "O inimigo, a Tenacidade e o PH": âncoras do inimigo (28.3) e dano em dados; régua das ações especiais (28.4); Fraqueza/Resistência e redução de Tenacidade (20.2–20.3); PH (16.2). Página 3 — "Combate: a Fila, a Quebra e o Dano Contínuo": a Fila e a Surpresa (19.3), Firmeza e teto de Atraso (19.4), Avançar/Avanço Total (19.5), Congelamento (19.6), casos-limite (19.7), Quebra em 5 passos (20.4), Dano Contínuo (20.6), Dano de Quebra (20.5). Página 4 — "Pessoas: condições, Morrendo e PV temporários": condições (21.5), Morrendo e Executado (23.4–23.5), teto de PV temporários (23.3). Página 5 — "Mesa: Energia, tetos e casos-limite": Energia (17.2), tetos (29.12), casos-limite de mesa (27.10, seleção que cabe). Rodapé: "Explorando Galáxias v1.1 · referência do Mestre · em dúvida, o capítulo vence". O lint confere `orientation="landscape"`, `paperSize=9`.

### 6.16 Tabelas (R11)

Inventário das listas (`tab.<id>`), todas com 100 vagas (4.2). Fonte "Livro" = preenchida com o texto do livro e marcada com a seção; "Sugestão" = escrita para a planilha (`mestre_sabor`), mínimo indicado:

| Grupo | Listas (mínimo) |
|---|---|
| Nomes por cultura | `nome.humano`, `nome.xianzhouita`, `nome.vidyadhara`, `nome.vulpes`, `nome.haloviano`, `nome.avginiano`, `nome.intellitron` (≥ 30 cada) e `sobrenome.<cultura>` (≥ 30 cada; epíteto/clã/designação conforme a cultura) |
| Lugares, naves, organizações, facções | `lugar_a`, `lugar_b`, `nave_a`, `nave_b`, `faccao_a`, `faccao_b`, `organizacao` (≥ 30) |
| NPC | `ocupacao` (≥ 40), `aparencia_traco`, `personalidade`, `motivacao`, `segredo`, `maneirismo` (≥ 30), `motivacao_<caminho>` (5 × 9), `atitude` (5), `gancho_npc` (≥ 30) |
| Aventura | `tipo_aventura` (≥ 12), `objetivo_<tipo>` (3 por tipo), `gancho` (≥ 30), `local` (≥ 30), `complicacao`, `reviravolta` (≥ 30), `prazo` (≥ 20) |
| Mundos | `mundo_tipo` (≥ 20), `mundo_condicao`, `manha`, `pararam` (≥ 30), `ameaca`, `estacao_funcao`, `estacao_problema`, `nave_classe` (≥ 20), `nave_peculiaridade` (≥ 30), `faccao_metodo`, `faccao_recurso`, `faccao_uso` (≥ 20) |
| Improviso e recompensa | `rumor` (≥ 40), `evento` (≥ 30), `custo_falha` (≥ 20), `bugiganga` (≥ 50), `pista` (≥ 20), `cone_nome_a`, `cone_nome_b`, `cone_memoria` (≥ 30), `cone_gatilho` (≥ 20), `conjunto_nome`, `conjunto_origem` (≥ 20), `conjunto_4` (≥ 10), `oraculo` (6 faixas) |
| Do livro (editáveis) | `ganchos_<faixa>` (4 × 5, 27.18), `locais` (6, 27.17), `faccoes` (8, 27.16), `ambiente_por_faccao` (H8) |

**Regras de escrita das tabelas de sabor** (conferidas pela suíte `texto` e `sabor`): PT-BR com acento; terminologia do glossário 30.1; nenhum termo aposentado de 30.2; **nenhum nome de personagem do jogo** (lista de nomes proibidos na suíte, ≈ 90 nomes do Honkai: Star Rail, comparação sem caixa e sem acento, também como palavra dentro do nome composto); nomes no estilo de cada cultura descrita em 05 — Humano: cosmopolita, de várias origens terrestres misturadas; Xianzhouíta: duas sílabas de sonoridade chinesa clássica, nomes de virtude/elemento; Vidyadhara: nomes longos de mar e de linhagem ("da Maré Funda"); Vulpes: nomes curtos de sonoridade leste-asiática com epíteto de mercador/cauda; Haloviano: nomes melódicos de vogais abertas, sobrenome de canção; Avginiano: nome curto + nome de clã errante; Intellitron: designação alfanumérica + nome escolhido ("KV-12, chamado Paciência"). Nenhuma entrada vazia, repetida ou com mais de 200 caracteres.

### 6.17 Minhas Tabelas (R11)

10 tabelas do Mestre (G=701…710): para cada uma, nome (entrada), 100 vagas (entrada, mesmo contador corrido de 4.2), Rolagem nº, "quantos sortear" (1–5, sem repetir quando possível). Os índices saem em sequência: o k-ésimo resultado, para k = 0…4, é `MOD(i₀ − 1 + k·passo, n) + 1` (revisão 1: de 1 a n, nunca 0), em que i₀ = `escolha(x)` (de 1 a n) e o passo é o primeiro de 7, 11, 13, 17, 19, 23 que não divide n. Com n ≤ 100, sempre existe um, porque 7·11·13 > 100. Um primo que não divide n é primo com n, então os k < n resultados são distintos. Com n < quantos, a lista repete, e o aviso "a lista tem só n entradas" acende. A tabela mostra ainda o tamanho da lista e os resultados. Uma tabela vem de exemplo no **Exemplo** (clima do Expresso).

### 6.18 Dados

Blocos de 4.1. Título da aba diz "Tabelas do livro usadas pelas fórmulas. Não edite: o gerador reescreve esta aba". Fica no fim, pode ser ocultada.

---

## 7. Regras do livro implementadas (exatas, com a seção)

| Regra | Seção | Onde |
|---|---|---|
| Âncoras do inimigo por faixa × tipo (PV, Defesa, RD, Tenacidade, VEL, Ataque, Dano, DT, TR, nº de Fraquezas) e dano em dados com média `n×(f+1)÷2` para baixo + fixo | 28.3, 02 | Inimigos, Bestiário, Encontros, Combate |
| Ficha de 15 campos e formato do cartão | 28.1 | Inimigos, Bestiário |
| Nove regras da ficha: sem Esquiva/Intervir/Energia/Ultimate/PH/Esforço; Firmeza de Elite e Boss; Congelamento em Elite/Boss; ações agressivas por tipo; nº de Fraquezas; Resistência tira 2 dados e reduz Tenacidade a 1 | 28.2 | Inimigos, Combate, Escudo |
| Régua das ações: ataques no Dano por acerto; especial até 1,5× em 1 alvo ou cheio por alvo em 2–3; controle com condição de 21 e DT dos efeitos; recarga 2–3 Ciclos; 1 a 3 especiais | 28.4 | Inimigos (ações) |
| Fases: barra única, a fase troca e não soma, Tenacidade pode cair e nunca subir e **volta ao máximo na virada**, Fraquezas anunciadas, **virada no fim do turno do Boss, sem gastar a ação** (fase da barra só avisa; fase em vigor é do Mestre) | 28.5 regras 1–5 | Combate (C4, C5), Bestiário, Inimigos (I5) |
| As 32 fichas, 5 Bosses com fases, 5 inimigos com Resistência, Escória custa 1,5 Comum, Pretor/Dramaturgo sozinhos | 28.6–28.11 | Bestiário, Encontros |
| Orçamento = dano do grupo em 4 Ciclos; custos; 4 composições; metade = passagem; alvo 3–5 Ciclos | 27.4 | Encontros |
| Contrato da Fraqueza (≥ 3 Elementos do grupo como Fraqueza; senão ~1 Ciclo a mais) e regra irmã da Resistência | 27.5, 28.11 | Encontros, Inimigos |
| DT para descobrir Fraqueza 13–17 pela faixa do inimigo mais forte; Intellitron com Vantagem e 2 por sucesso | 20.2, 05, 27.6 | Encontros, Grupo |
| Attrition e o dia de jogo (2/3/4 combates) | 27.7, 23.6 | Encontros, Sessões, Aventuras |
| DT por faixa, a faixa é do desafio, Sucesso Automático só em Perícia, 5 DTs fixas | 27.2, 27.3 | Sessões, Improviso, Escudo |
| Fila: ordenar por VEL, empates (Agilidade, Discernimento, jogadores antes dos NPCs; inimigo sem atributos perde o empate de VEL para o PJ), remontagem com VEL atual e pendentes, sem rolagem | 19.3, 28.2 | Combate |
| Embaraço (`1d6` por acúmulo, Atrasa 1) e Aprisionamento (`1d6 + Eficiência`, Atrasa 2) | 21.5 | Combate (C7) |
| VEL: fórmula e extremos absolutos 7 e 25 | 19.1 | Grupo (aviso) |
| Surpresa: casa pulada no 1º Ciclo, DT 13 | 19.3, 21.4 | Combate |
| Atraso: teto Comum 3 / Elite e Boss 2; pendente quando já agiu ou sem casas; Firmeza pelo total do Ciclo com mínimo 1 | 19.4 | Combate |
| Avançar só em quem não agiu; Avanço Total 1 por Ciclo | 19.5 | Combate |
| Congelamento: Comum perde o turno e descarta pendentes; Elite/Boss Atraso 2 e sem especial no turno seguinte | 19.6, 21.2 | Combate |
| Casos-limite da Fila (reforço entra nas casas restantes; morto sai; Morrendo mantém a casa) | 19.7 | Combate (texto + regra de casa) |
| Fraqueza +2 dados / Resistência −2 (mínimo 1); redução de Tenacidade total/metade (mín. 1)/1; condicionada ao acerto; valores por fonte | 20.2, 20.3 | Combate (calculadora) |
| Quebra em 5 passos; Dano de Quebra por Elemento com a Eficiência de quem quebrou | 20.4, 20.5 | Combate |
| Dano Contínuo: início do turno do alvo, ignora RD, não crita, sem Fraqueza, não reduz Tenacidade | 20.6 | Combate |
| Condições: efeito, duração, acúmulos e tetos; Sangramento 5% com teto 3×Ef; cura não remove condição | 21.1–21.5 | Combate |
| Ordem do dano e mínimo 1; PV temporário absorve primeiro | 23.1, 02 | Combate (calculadora) |
| Cura acima do máximo perdida | 23.2 | Combate |
| Morrendo: d20 + Presença sem Eficiência contra 10, contador, 20 e 1 naturais, dano = falha; Vantagem de 3 Raças | 23.4, 05 | Combate |
| Executado: só ser racional, Ataque Básico a Distância Pessoal; Xianzhouíta imune | 23.5, 05 | Combate, Grupo |
| PH do grupo por nº de jogadores e faixa; começa com o máximo −2; geração | 16.2 | Campanha, Combate |
| Energia e 1 Ultimate por Ciclo; segunda Ultimate inválida | 17.2, 27.10 | Combate |
| Teto de dados adicionais +3 sem a Fraqueza | 16.9, 26.6, 29.12 | Combate (calculadora) |
| Progressão por marco, sem XP; ritmo de sessões; Ressonâncias 5/10/15/20 | 26.1, 26.7 | Campanha, Recompensas, Encontros |
| Cone e Tier por faixa; viradas de Tier no 7 e 18; sem compra/sorteio; Sobreposição 1 por faixa e tetos; Bônus Maior; Conjuntos | 25.1–25.3, 27.8 | Recompensas, Grupo |
| Verba de marco por nível; preços de 24.2/24.3; preços não escalam | 24.2–24.5 | Recompensas, Improviso (loja) |
| Eficiência por nível | 02.3, 29.12 | Campanha, Combate (Quebra) |
| Ficha de Decisões da Mesa | 27.11, 29.11 | Campanha |
| Trilha de Ação (formato) | 29.10 | Combate |
| Facções, locais e ganchos do livro | 27.16–27.18 | Tabelas, Aventuras, Mundos, NPCs |

Constantes procedimentais escritas dentro de fórmulas (Firmeza ÷ 2, teto 2/3, mínimo 1, 5%, ±2 dados, +3 dados, 100 de Energia, DT 10 do Morrendo) ficam registradas em `mestre_mapa.json → constantes` com a seção; todo número de tabela vem da aba Dados.

---

## 8. Heurísticas "Sugestão da planilha" (H1–H25)

Toda célula que mostra o resultado de uma heurística tem, na mesma linha ou no cabeçalho, o texto **"Sugestão da planilha — não é regra do livro (H#)"**, e o mapa lista a célula em `sugestoes`. Nenhuma heurística altera um número que o livro fixa.

| # | Heurística | Método (derivado do livro) | Validação |
|---|---|---|---|
| H1 | Inimigo por nível dentro da faixa (revisão 1: só o PV) | **Só o PV** é interpolado linearmente entre os níveis de referência 3/7/11/15/19 de 29.1 (constante abaixo de 3 e acima de 19). Todos os outros números, **inclusive o Dano por acerto**, são a âncora da faixa do nível, sem ajuste (6.7.1 diz o porquê). É opcional: o padrão é a faixa (28.4 passo 1: "a faixa do inimigo é a faixa do grupo") | (a) Nos níveis 3/7/11/15/19, erro 0 contra 28.3 nas 15 células de PV. (b) Cada uma das 32 fichas, no nível de referência da sua faixa, tem PV idêntico. (c) Em todo nível de 1 a 20, os outros 10 números e o Dano (expressão e média) são **idênticos** à âncora da faixa: desvio 0, e qualquer diferença reprova. (d) Para o PV, a suíte grava o desvio máximo por tipo em relação à âncora da própria faixa, nível a nível, e **falha acima de 20%**. Os valores medidos nesta revisão, com a fórmula de 6.7.1: Comum −14,3% (nível 5: 60 contra 70), Elite −14,7% (nível 9: 192 contra 225), Boss −14,7% (nível 9: 495 contra 580). O relatório publica a tabela. O limiar de 20% vale só para o PV, porque é a única coluna interpolada |
| H2 | Dano de especial 1,5× onde não há ficha | Elite: o livro usa sempre a expressão da linha de Boss ou a de 1,5× (Capataz `3d6 · 10`, Centurião/Auditora `4d8 + 1 · 19`, Oficial-Lâmina `5d10 + 1 · 28`, Escultor/Executora `6d10 + 3 · 36`, Arcanjo/Arauto `7d12 + 3 · 48`). Boss: das fichas (`3d8 + 2 · 15`, `7d10 + 4 · 42`, `9d10 + 5 · 54`, `10d12 + 7 · 72`). Faltam Comum (5 faixas) e Boss 5-8: dados normais do tipo + fixo até `INT(1,5 × média)`: `1d6 + 1 · 4`, `2d6 + 3 · 10`, `2d8 + 4 · 13`, `3d6 + 8 · 18`, `3d8 + 11 · 24`; Boss 5-8 `4d8 + 12 · 30` | Cada célula com fonte "ficha" é lida do `.md` pela suíte `bestiario`; cada média = `INT(1,5 × âncora)` (28.4) nas 15 células |
| H3 | Reescala de números de ação ao mudar de faixa | Marcadores `{PV:n}` e `{TEN:n}` proporcionais; o resto pelos marcadores de âncora (6.7.3) | Na faixa original os 32 textos voltam idênticos ao livro (0 diferença); `{TEN}` nunca passa da âncora (28.5 regra 3) |
| H4 | Limiares de fase | Partes iguais: 2 fases `INT(PV/2)`, 3 fases `INT(PV/3)` e `INT(2PV/3)` | Reproduz as barras das 5 fichas (305/153/152; 580/291/290; 750/376/375; 935/624/623/312/311) |
| H5 | Grupo com nº de PJs ≠ 4 | Orçamento e dano por Ciclo × nº/4 (o DPC de 29.3 é soma de 4 personagens) | Com 4 PJs, igual a 27.4 nas 5 faixas |
| H6 | Rótulos de dificuldade | ≤ 60% passagem (27.4 "metade do orçamento"); 60–115% típico; 115–160% pesado; > 160% dois orçamentos (27.4) | As 4 composições de 27.4 na faixa caem em "típico" nas 5 faixas; metade do orçamento cai em "passagem" |
| H7 | Ciclos estimados | custo ÷ dano por Ciclo (+1 sem contrato) | As 4 composições dão 3,6–4,2 Ciclos em todas as faixas (ex. 1-4: 4,0 / 3,6 / 4,1 / 4,0) (dentro de 3–5 de 27.4); o Combate A de 29.5 (305 + 50 contra 88) dá 4,0 (o livro publica 3,7 com o DPC puro de Boss, mais otimista; a diferença é dita no rótulo) |
| H8 | Ambiente por facção (encontro aleatório e filtro) | Tabela editável facção → ambientes, lida dos locais e facções de 27.16–27.17: Fragmentum → "Colônia ou mina abandonada", "Ruína"; Legião → "Frente de guerra", "Lua-forja"; Corporação → "Estação", "Cidade corporativa"; Xianzhou → "Nave-cidade"; Tolos → "Teatro, festa ou multidão"; Beleza → "Clínica ou ateliê"; Caçadores → "Qualquer lugar onde o grupo esteja"; Culto → "Lugar esvaziado"; Autômatos → "Instalação antiga"; Stellaron/Emanadora → "Mundo com Stellaron" | Toda criatura do bestiário tem pelo menos 1 ambiente; todo ambiente tem pelo menos 1 criatura em pelo menos 2 faixas |
| H9 | Consumíveis por faixa e quantidade nos achados | poção Pequena 1-8, Média 5-16, Grande 13-20 (pela escala de PV do personagem de 06.4/23.6); **0 a 2 consumíveis** por achado de encontro, uniforme (`inteiro(x, 0, 2)`); 1 consumível na recompensa da aventura | Todo item sorteado existe em 24.3 com o preço do livro; em 3 000 rolagens a quantidade fica sempre em 0–2 e cada valor aparece entre 28% e 39%; a poção sorteada sempre pertence à faixa |
| H10 | Oráculo sim/não | d20 + modificador por probabilidade; 6 faixas | Distribuição conferida pelo oráculo (50/50 = 50% de "Sim…") |
| H11 | Pesos de sabor | uniforme; "Nenhum Caminho" ×3, "nenhuma ameaça" ×3, rumor Verdadeiro/Meia/Falso 1/1/1 | Contagem nas listas |
| H12 | Fraquezas sugeridas do Criador (G = 110) | Ordem de preferência: primeiro os Elementos do grupo ainda sem Fraqueza nas linhas anteriores (contrato de 27.5), depois os demais em ordem sorteada; Resistência por último; **Comum recebe 2** (ponta alta de 1–2, 28.2 regra 7) | Oráculo × planilha em 300 rolagens × 3 grupos; nº sugerido = 2/3/4 por tipo; nenhuma sugerida igual à Resistência; com 12 linhas vazias e grupo de 4 Elementos distintos, as linhas 1…k cobrem os 4 Elementos do grupo antes de repetir |
| H13 | Ordem com vários movimentos no mesmo Ciclo; empate PJ × inimigo | Chave 2 (6.10); inimigo sem atributos: termos 0 na chave, então o PJ vem antes do inimigo empatado em VEL (19.3 passo 2, última cláusula); entre inimigos, a linha | Oráculo × planilha em 300 estados aleatórios; casos de 19.4 (7 casas → 2; 1 casa → 1) e de 19.6; os 4 casos de empate de 6.10 (inclusive PJ com Agilidade −1 contra Boss de mesma VEL) |
| H14 | Estrutura de cenas da aventura | 5 cenas pela régua de 27.4 (metade + típico) e 27.7 (até 3 combates, objetivo sem matar) | Orçamentos das cenas = 50% e 100% da faixa; DTs da linha Média/Difícil |
| H15 | Loja: quantidade e itens por tipo | 1–3 de cada; tipos de loja → blocos de 24.1–24.3 | Todo preço = livro |
| H16 | Relógios de progresso | segmentos 4/6/8/10/12 (ferramenta de mesa; o livro pede "relógio na ficção", 27.7) | Para **todo** par segmentos s ∈ {4, 6, 8, 10, 12} × preenchidos n ∈ 0…s (45 casos): barra = n "●" + (s−n) "○" + " n/s"; situação "Cheio — aconteceu" se n = s, "Falta 1" se n = s−1, vazia nos outros; n > s, n < 0 e s fora da lista acendem aviso e nunca dão erro; o painel do Início conta exatamente os relógios com n = s−1 |
| H17 | Reputação −3 a +3 | escala de 7 degraus com rótulo | Os 7 valores dão os 7 rótulos exatos ("−3 Inimiga declarada", "−2 Hostil", "−1 Desconfiada", "0 Neutra", "+1 Simpática", "+2 Amiga", "+3 Aliada"); vazio dá ""; fora de −3…+3 ou não inteiro dá aviso e ""; facção repetida dá aviso |
| H18 | Créditos achados num encontro | 5% / 10% / 15% da verba de marco da faixa (24.5) por leitura de dificuldade | Valor sempre ≤ 15% da verba; inteiro |
| H19 | Troca de Fraqueza sugerida no encontro aleatório | Regra de varredura de 6.9 (vaga 1…8, Fraquezas na ordem da ficha, Elementos faltantes na ordem de 20.1), sem sorteio | Oráculo × planilha em 500 encontros aleatórios × 3 grupos; depois da troca, o contrato fica cumprido sempre que houver Fraquezas trocáveis suficientes; nenhuma troca cria Fraqueza igual à Resistência; nº de Fraquezas por inimigo inalterado (é regra, 28.2 regra 7) |
| H20 | Fonte do gancho de NPC e de aventura | 50% os ganchos de 27.18 da faixa, 50% a tabela da planilha | Em 2 000 rolagens, cada fonte fica entre 45% e 55%; todo gancho "Livro" é um dos 4 da faixa do parâmetro |
| H21 | (absorvida em H9: 0–2 consumíveis) | — | — |
| H22 | Antagonista da aventura | Boss da facção na faixa → Elite da facção na faixa → Boss da faixa | Para cada facção × faixa (incluindo combinações sem Boss), o antagonista é sempre do primeiro degrau que tem candidato; nunca vazio |
| H23 | Aviso "mais de 3 missões Ativas" | limiar 3 (o livro não fala em quantas missões abertas) | Aviso com 4 Ativas, sem aviso com 3; texto rotulado |
| H24 | Tom, temas e limites da mesa na Sessão Zero | itens de checklist de prática geral de RPG; o livro não tem Sessão Zero | Os dois itens têm o rótulo; nenhum outro item da checklist cita regra que não esteja na seção indicada (suíte `texto`, conferindo a seção citada em cada item) |
| H25 | Quantidades de saída dos geradores de sabor | 2 traços de aparência, 3 rumores, 3 bugigangas, 6 itens na loja, 10 nomes avulsos, 5 cenas: formato de apresentação, sem efeito em número do jogo | Contagem de saídas por gerador; nenhuma repetição dentro de uma rolagem quando a lista tem entradas suficientes |

---

## 9. Cobertura dos requisitos R1–R13

| R | Atendido por | Aba / módulo |
|---|---|---|
| R1 Criador de Inimigos | 6.7: faixa/nível, tipo, facção, Elemento, Fraquezas (regra + sugestão), Resistência, bloco completo de 28.1 com dano `dados · média`, PV, VEL, Tenacidade, ações pela régua 28.4; modo "Ajustar do bestiário" para outra faixa; modo por nível (H1) validado | Inimigos · `aba_inimigos.py` |
| R2 Bestiário | 6.8: as 32 fichas, filtro por faixa/tipo/Elemento/facção/ambiente, ficha completa; fonte das listas de Encontros e Combate | Bestiário · `aba_inimigos.py`, `mestre_dados.bestiario()` |
| R3 Construtor de Encontros | 6.9: orçamento por faixa e tamanho, 3 encontros salvos com bestiário e criados, dificuldade, Ciclos, composições, contrato da Fraqueza, regra irmã, recompensa (sem XP — 26.1, com link à aba Recompensas), encontro aleatório por ambiente/faixa | Encontros · `aba_encontros.py` |
| R4 Rastreador de combate | 6.10: Fila com VEL, empates, Atraso/Firmeza/Avanço/Congelamento/Surpresa, Fila prevista; PV; Tenacidade, Quebra e efeito por Elemento; condições com duração e acúmulos; Morrendo e Executado; PH, Energia, Ultimate, Esforço; recargas; fases; 16 combatentes; inimigo da lista preenche os próprios dados | Combate · `aba_combate.py` |
| R5 Criador de NPCs | 6.6: nome por cultura, Raça, Caminho, ocupação, aparência, personalidade, motivação, segredo, maneirismo/voz, atitude, gancho, papel; bloco de combate opcional; Elenco de 30 | NPCs · `aba_npcs.py` |
| R6 Criador de Aventuras | 6.11: tipo, gancho, contratante, objetivo, local, antagonista, complicação, reviravolta, prazo/risco, recompensa, 5 cenas | Aventuras · `aba_aventuras.py` |
| R7 Gerador de Recompensas | 6.12: verba (24.5), consumíveis e itens (24.3), Cone e Tier por faixa com Sobreposição (25.1–25.2), sabor de Cone e de Conjunto, Ressonâncias e marcos (26.1, 26.7), Tesouro do grupo | Recompensas · `aba_recompensas.py` |
| R8 Outros geradores | 6.13–6.14: nomes por cultura/naves/lugares/organizações; planetas/locais/estações; facções; rumores e ganchos; eventos e complicações; lojas com estoque e preço de 24; bugigangas; oráculo sim/não | Mundos, Improviso · `aba_mundos.py` |
| R9 Gestão de campanha | Início (painel, índice, semente, avisos) 6.1; Grupo 6.3; progressão por marco 6.2; Missões 6.5; Facções e reputação, relógios, linha do tempo, Ficha de Decisões, Sessão Zero 6.2; preparação de sessão e diário 6.4 | `aba_inicio.py`, `aba_campanha.py` |
| R10 Escudo do Mestre | 6.15: 5 páginas A4 paisagem lidas da aba Dados | `aba_escudo.py` |
| R11 Tabelas editáveis | 6.16 (listas com 100 vagas, contador, tamanho, fonte), 6.17 (Minhas Tabelas com sorteio); sabor ≥ 20, nomes ≥ 30 por cultura | `aba_tabelas.py`, `mestre_sabor.py` |
| R12 Três entregáveis | D2; seção 14 (Exemplo); seção 15 (guia) | `gerar_mestre.py`, `exemplo.py` |
| R13 Extras | Calculadora de dano e Tenacidade (6.10), rolador de dados com semente (6.14), cartões de NPC (6.6), DT rápida (6.14), Ficha de Decisões (6.2), Fila prevista (6.10) | várias |

---

## 10. Validação de entradas e tratamento de erros

### 10.1 Na planilha (o Mestre digitando)

Regra geral (herdada da ficha): **nunca valor de erro**, em nenhum estado; validação de dados com `errorStyle="warning"` (deixa digitar, mostra a mensagem PT-BR); a regra de negócio vive na coluna de aviso; entrada inválida conta com o valor limitado ou cai no padrão e diz qual. Todas recuperáveis; nada é fatal numa planilha.

| Entrada | Obrigatória? | Tipo / limites | Se inválida |
|---|---|---|---|
| Semente da campanha | não (vazia = 12345) | inteiro 1–2 147 483 646 | aviso; usa 12345 |
| Rolagem nº (todo gerador) | não (vazia = 1) | inteiro 1–1 000 000 | aviso; usa 1 |
| Nível do grupo | sim para a maioria dos cálculos | inteiro 1–20 | vazio: abas mostram "Preencha o nível na aba Campanha" e calculam com 1; fora: aviso e limite |
| Nº de jogadores | não (vazio = nº de PJs do Grupo, mínimo 1) | inteiro 1–6 | fora de 3–6: aviso "fora da tabela de 16.2" e conta com o limite 3–6 para o PH |
| Números de PJ (PV, Defesa, VEL…) | não | inteiros, faixas largas (PV 1–999, Defesa 5–40, VEL 5–30, bônus −1…+5) | aviso "confira na ficha"; usa o valor |
| Listas (Raça, Caminho, Elemento, tipo, faixa, condição…) | não | valor da lista | texto fora da lista: aviso "não está na lista"; o campo dependente fica "" |
| Quantidade no encontro | não | inteiro 0–10 | aviso; limite |
| PV atual, Dano agora | não | inteiro (Dano pode ser negativo = cura) | não inteiro: `INT`; PV acima do máximo: aviso e usa o máximo |
| Redução de Tenacidade | não | inteiro ≥ 0 | negativo: aviso e 0 |
| Atraso / Avanço (casas) | não | inteiro 0–20 | aviso; o teto da regra corta |
| Turnos e acúmulos de condição | não | 0–20 / 0–5 | acima do teto da condição: aviso com a seção (21.5) e usa o teto |
| Sucessos / falhas de Morrendo | não | 0–3 | aviso; limite |
| Energia | não | 0–100 | aviso; limite (excedente perdido, 17) |
| PH atual | não (vazio = início) | inteiro | negativo ou acima do máximo: aviso (27.10) |
| Textos livres | não | até 300 caracteres (resumo de diário) / 200 (tabelas) / 40 (nomes) | aviso de tamanho; mantém |
| Dados do rolador | não | N 1–20, F da lista, M −50…+50 | aviso; limite |

Proteções de fórmula: todo `MATCH` dentro de `IFERROR(…,"")`; toda divisão protegida (`IF(d=0,"",…)`); nenhuma referência circular (o gerador confere com o grafo de dependências do `formulas` na suíte `extremos`).

### 10.2 No build (Python)

| Operação | Falha | Fatal? | O que acontece | Log |
|---|---|---|---|---|
| Ler capítulo / seção / tabela do livro | arquivo, cabeçalho ou colunas não encontrados | **fatal** | `ValueError("cap 28, seção 28.3: tabela 'Faixa' não encontrada")`, código de saída 1, nenhum `.xlsx` gravado | `stderr`, uma linha |
| Parser das 32 fichas | ficha com campo faltando, número que não bate com a âncora 28.3 (exceto as divergências documentadas: Tenacidade de fase) | **fatal** | erro com o nome da criatura e o campo | `stderr` |
| Import da ficha (`gerar_ficha`, `ficha_dados`, `renderizar_ficha`) | nome reaproveitado não existe | **fatal** | `ImportError` com o nome; não editar a ficha | `stderr` |
| Marcador «nome» sem registro | referência para célula inexistente | **fatal** | lista dos marcadores órfãos | `stderr` |
| Nome lógico repetido no mapa | dois `reg` iguais | **fatal** | `ValueError` | `stderr` |
| Tabela de sabor com menos que o mínimo, vazio ou repetido | dados de `mestre_sabor` | **fatal** | erro com o id da lista | `stderr` |
| Texto que não cabe (layout) | medida > célula | recuperável no gerador | `ajustar_layout` aumenta a altura da linha; se a coluna precisa alargar e a área passaria de 1360 px, **fatal** com a aba e a célula | `stderr` |
| Gravar o `.xlsx` | arquivo aberto no Excel/Drive bloqueado | **fatal** | grava em `<nome>.tmp.xlsx` e tenta substituir; se não der, mensagem "feche o arquivo" e o temporário é apagado | `stderr` |
| Exemplo: PJ inválido pelo `oraculo_ficha` | aviso do oráculo da ficha | **fatal** | lista dos avisos | `stderr` |

O gerador imprime no fim um resumo de uma linha por saída (abas, fórmulas, validações, tempo). Sem log em arquivo.

---

## 11. Invariantes e quem as garante

| Invariante | Dono | Por quê ali |
|---|---|---|
| Todo número do livro na planilha é igual ao `.md` | aba Dados gerada de `mestre_dados`/`ficha_dados` + suíte `dados` (parser próprio do teste) | Uma fonte; as fórmulas só leem Dados |
| As 32 fichas e os textos de ação batem com o livro | `mestre_dados.bestiario()` (falha alto) + suíte `bestiario` | Transcrição por marcadores é o ponto mais frágil |
| Sorteio determinístico e aritmética < 2⁵³ | `mestre\sorteio.py` (único construtor) + `oraculo_mestre` (`assert` de limites) + suíte `determinismo` | Uma fórmula, um lugar |
| Nenhuma heurística sem rótulo | `nucleo.sugestao()` registra a célula em `sugestoes`; suíte `texto` exige o rótulo em toda célula listada e procura células de heurística sem registro pelas funções que as geram | O pedido proíbe regra inventada em silêncio |
| Compatibilidade Google | suíte `lint` (reuso de `_checar_formula` + checagens de workbook) | Mesmo critério da ficha |
| Arquivos da ficha e do livro intocados | suíte `protegidos` (`ficha_protegidos.json` + `baseline-hashes.json`) | Regra dura do pedido |
| Toda entrada vazia no modelo | `nucleo.ent()` nunca escreve valor; suíte `lint` confere no modelo | Os testes simulam vazio omitindo a entrada |
| Nenhuma entrada em dois lugares | `nucleo.ent()` recusa nome lógico repetido; nível e nº de jogadores só na Campanha | D9 |
| Usabilidade (sem corte, contraste, 1360 px, 15 linhas) | `nucleo.ajustar_layout` + suítes `preview` e `visual` | Mesmos critérios da auditoria da ficha (seção 10) |

---

## 12. Testes (`build\testar_mestre.py`)

### 12.1 Suítes

Todas calculam com `formulas` 1.3.4 através de `testar_ficha.Modelo` (um modelo carregado por processo, cenários por `inputs`, `outputs` restritos, até 8 processos). Saída com código 1 em qualquer falha. Uso: `$env:PYTHONUTF8="1"; python "build\testar_mestre.py" --suite <nome>`.

| Suíte | Tipo | O que faz | Meta |
|---|---|---|---|
| `spike` | integração | Workbook mínimo com os padrões novos: `MOD` com 2³¹·16807, três `MOD` aninhados, os estágios `Q` (intermediário até 2,8·10¹⁴, `INT(z/65536)`) e `X` da seção 5 nos extremos de S, G, R e C, `INT(x·n/M)`, `INDEX(MATCH(k, contador corrido))`, `SMALL`+`MATCH` com chaves fracionárias, `CHOOSE(MATCH())` sobre 7 intervalos, `REPT` com "●", validação de lista apontando outra aba; compara com Python. **Não regrava** `ficha_funcoes_ok.json`: grava `build\mestre_spike.json` | 0 divergência; se um padrão divergir, ele sai do design e o lint passa a proibir |
| `protegidos` | integração | SHA-256 do livro (via `testar_ficha._arquivos_protegidos` + `ficha_protegidos.json`) e dos arquivos da ficha (`baseline-hashes.json`) | 0 alterado |
| `dados` | integração | Parser próprio do teste relê 27, 28, 19–25 e compara com a aba Dados e com as listas "Livro" da aba Tabelas | 0 diferença |
| `bestiario` | integração | 32 fichas: 15 campos, fases, ações; cada número contra 28.3 e o índice 28.11; texto de cada ataque/ação renderizado na faixa original = linha do `.md`; H2 e H4 | 0 diferença |
| `ouro` | integração | Números impressos no livro calculados **na planilha**: os 15 cartões de referência de 29.4; o carcereiro de 28.4 (225/21/3/7/15/+11/`4d8 + 1 · 19`/17/+5/3 Fraquezas, Trancafiar DT 17); orçamento 27.4 nas 5 faixas e as composições prontas de 28.11; Firmeza 7 → 2 e 1 → 1 (19.4); Sangramento 365 → 18 e 935 → 24 com Ef 8 (21.2); Quebra de Fogo `2d6 + 4 · 11` no nível 3 e `2d6 + 16 · 23` no 19, Gelo 2 e 8 (20.5); exemplo de Ciclo com Quebra de 20.4 (12 − 4 − 1 − 1 − 2 = 4, depois Quebra); Morrendo de 23.4 (Vesper); PH de 16.2 (3–6 × 3 degraus); Descanso Curto 8/16/24/32/40 (23.6); verba 24.5; Cone/Tier 25.1; DT 27.2/27.3/20.2; Ultimate 27.9 | 0 diferença |
| `oraculo` | integração (diferencial) | `oraculo_mestre` × planilha: Criador nos 3 modos × 20 níveis × 3 tipos × 4 Elementos de ataque; Ajustar para as 32 × 5 faixas; encontros aleatórios (500 sementes); Fila em 300 estados aleatórios (VEL, empates, Atrasos, Firmeza, Congelado, Surpresa, Avanço, já agiu, derrotado, Morrendo), mais os 4 casos fixos de empate de 6.10 (PJ com Agilidade −1 contra Boss de mesma VEL vem antes); fases de Boss (fase da barra × fase em vigor: Fraquezas e Tenacidade da calculadora só mudam quando a fase em vigor muda; Tenacidade máx. da fase nova; avisos de fase adiantada e de virada pendente) para os 5 Bosses com fases e para Bosses criados com I5; dano de condição de Embaraço e Aprisionamento; calculadora de dano e Tenacidade (2 000 casos); todos os geradores (NPC, aventura, recompensa, Cone, Conjunto, mundos, loja, rumor, oráculo, rolador, Minhas Tabelas) em 300 Rolagens nº × 3 sementes; avisos nos dois sentidos | ZERO divergência |
| `determinismo` | unidade + integração | Propriedades (a)–(g) da seção 5. A (g), de correlação serial entre rolagens e entre campos consecutivos, inclusive os 20 dados de uma expressão do rolador e as triplas de d6, roda no oráculo. A planilha confere `u`, `y` e `x` iguais ao oráculo em 300 rolagens por gerador. Recalcular duas vezes dá o mesmo. Mudar uma entrada que não é parâmetro (amostra de 50 entradas de outras abas, tirada fora da tabela de parâmetros da seção 5) não muda nenhum sorteio. Mudar cada parâmetro listado muda o resultado de pelo menos um campo | todas valem |
| `extremos` | integração | Todas as células com fórmula: modelo em branco; um campo por vez com valor válido e inválido; Combate cheio (16) com todos os estados; listas da aba Tabelas esvaziadas; nível 1 e 20; 1 e 6 jogadores | 0 valor de erro; aviso esperado na coluna certa; modelo em branco sem aviso |
| `lint` | integração | `_checar_formula` em toda fórmula, validação e formatação condicional; abas = D3; sem nome definido, proteção, Tabela, caixa de seleção, painel congelado; só Arial; `fullCalcOnLoad`; toda entrada vazia no modelo; área ≤ 1360 px em cada aba (exceto Dados e Tabelas, que não são área de jogo); regra das sub-tabelas de D11 (≤ 12 colunas usadas em A:L por linha de tabela, ≤ 13 linhas sob cada cabeçalho, coluna A de cada sub-tabela com o rótulo do item); colunas auxiliares ocultas e sem nenhuma entrada; nenhuma função fora de `ficha_funcoes_ok.json` (pega `COUNT` e afins); Escudo A4 paisagem; sem `RAND`, `RANDBETWEEN`, `SUBSTITUTE`, `CHAR`, `TRIM` | 0 achado |
| `texto` | integração | `testar_ficha` (termos proibidos, aposentados de 30.2, grafia de 30.1, ortografia pelo léxico do livro + `mestre_lexico_extra.txt`, formas sem acento) sobre o texto visível; listas de nomes (`sem_ortografia`) fora da ortografia; rótulo de Sugestão em toda célula de `sugestoes` | 0 achado |
| `sabor` | unidade | `mestre_sabor`: mínimos, sem vazio, sem repetido, ≤ 200 caracteres, **nenhum nome de personagem do jogo** (lista do teste), nomes ≥ 30 por cultura | 0 achado |
| `preview` / `visual` | integração | `renderizar_ficha` sobre as 18 abas em 3 estados (em branco, Exemplo, pior caso); recortes ≤ 1800 px em `.agents\tasks\mestre\preview\`; texto cortado, listas com espaço da seta, avisos pela mensagem mais longa, contraste, distância ao cabeçalho, 1360 px | 0 falha; o executor abre recortes (no máximo 4 por vez, conferindo o tamanho com Pillow antes) e registra o que viu |
| `exemplo` | integração | O Exemplo: entradas = `exemplo.py`; os 4 PJs conferem com `oraculo_ficha.calcular` (Nadir = 29.7); o encontro carregado cumpre o contrato e está em "típico"; Fila do Ciclo 1 igual ao oráculo; NPCs, missões e sessão preenchidos; toda fórmula sem erro | 0 falha |
| `tudo` | — | todas, na ordem acima | código 0 |

### 12.2 Oráculo e testabilidade

O que é **unidade** (Python puro, sem planilha): `oraculo_mestre` (sorteio, âncoras, interpolação, reescrita de marcadores, Firmeza, chave de Fila, calculadora, geradores) com testes próprios dentro da suíte `oraculo --so-oraculo` (casos do livro); `mestre_sabor` (suíte `sabor`); os parsers de `mestre_dados` (contra o parser próprio do teste). O que é **integração**: tudo que calcula a planilha. As fórmulas grandes ficam testáveis porque cada sorteio tem as células auxiliares `u`, `y` e `x` registradas no mapa (o teste confere os três estágios antes do texto, e assim uma divergência aponta o estágio) e porque a Fila expõe as chaves em colunas auxiliares.

---

## 13. Implementação em 4 fases

Cada fase termina com: `gerar_mestre.py` gravando as **duas** planilhas (o Exemplo com o que a fase já tem), lint 0, `protegidos` OK e as suítes da fase passando; `PROGRESSO.md` atualizado. Uma fase só começa com a anterior pronta. Nenhuma suíte é desligada para "passar".

| Fase | Entrega | Abas | Suítes que precisam passar |
|---|---|---|---|
| **1 — Combate e preparação de combate** | `nucleo`, `sorteio`, `mestre_dados` (caps. 19–23, 27.2–27.7, 28), aba Dados, Tabelas (só `ambiente_por_faccao` e as listas do livro de 27.16–27.18), Grupo (só as entradas e o resumo que Combate e Encontros leem), Campanha (só Mesa e calculadas), Início (título, semente, índice), **Bestiário, Inimigos, Encontros, Combate**; `oraculo_mestre` (partes de combate) | Início, Campanha, Grupo, Inimigos, Bestiário, Encontros, Combate, Tabelas, Dados (as demais abas existem com título e "em construção" para a ordem de abas já ser a final) | spike, protegidos, dados, bestiario, ouro (combate/encontro), oraculo (Criador, Ajustar, encontros, Fila, calculadora), determinismo (a)–(g) com G=100 e 110 (a (g) roda já na fase 1 sobre o sorteio do oráculo, inclusive com G = 650, porque a fórmula é uma só), extremos, lint, texto, preview/visual das abas da fase |
| **2 — História** | `mestre_sabor` (NPC, aventura, recompensa), NPCs (gerador, Elenco, cartões), Aventuras, Recompensas (marco, sabores, achados, Tesouro) | + NPCs, Aventuras, Recompensas | as da fase 1 + sabor + oraculo/determinismo de G=200, 300, 400, 410, 420 |
| **3 — Campanha, demais geradores e Escudo** | Campanha completa (facções, relógios, linha do tempo, Ficha de Decisões, Sessão Zero, marcos), Grupo completo (checagens), Sessões, Missões, Mundos, Improviso (com rolador e oráculo), Escudo do Mestre, Minhas Tabelas, Início completo (painel e avisos) | todas as 18 | todas menos `exemplo` |
| **4 — Exemplo e guia** | `exemplo.py` completo (seção 14), `COMO-USAR-PLANILHA-DO-MESTRE.md` (seção 15), auditoria interna `.agents\tasks\mestre\AUDITORIA.md` (resultados das suítes, tabela de desvio de H1 com o erro máximo do PV por tipo, tabela de correlação da semente, lista H1–H25, recortes olhados) | — | `tudo` |

---

## 14. Exemplo (`Planilha do Mestre - Exemplo.xlsx`)

O mesmo modelo, com entradas preenchidas por `exemplo.py`:

- **Campanha:** "O Lacre do Poço Sete", 4 jogadores, nível 1, sessão 2, dia de campanha 3, array oficial; 3 facções com atitude (Legião −2, Corporação 0, Xianzhou +1); 3 relógios ("A Legião cumpre o ultimato" 2/6, "O lacre cede" 3/8, "A Corporação manda a apólice" 1/4); 6 eventos na linha do tempo (incluindo o ultimato de 27.16 "eles avisam"); 3 linhas na Ficha de Decisões (as três de 27.11, adaptadas aos PJs); Sessão Zero marcada.
- **Grupo** (4 PJs, nível 1, faixa 1-4, todos validados por `oraculo_ficha.calcular` sem aviso; os números digitados são os que o oráculo da ficha calcula):
  - **Nadir** — Humana, A Destruição, Fogo — exatamente a de 29.7 (PV 61, Defesa 16, Esquiva 18, RD 0, VEL 14, DT 14, Presença +0).
  - **Tessaly Varonne** — Vulpes, A Caça, Vento (arma Disparo longo, Botas I) — a Caça chega à frente da faixa (19.1).
  - **Shen Wanqing** — Xianzhouíta, A Preservação, Gelo (Armadura Pesada) — não pode ser Executada; Morrendo com Vantagem.
  - **KV-12, "Paciência"** — Intellitron, A Abundância, Quântico — descobre Fraquezas com Vantagem, duas por sucesso.
  - Elementos do grupo: Fogo, Vento, Gelo, Quântico (sem repetição: a regra irmã não pesa).
  - Os nomes passam pela suíte `sabor` (nenhum é personagem do jogo).
- **Encontros:** A = "Emboscada no duto 4": Sargento de Trincheira + 2 Larvas Fuliginosas + 2 Cascos Ocos, todos do bestiário sem alteração: custo 120 + 200 = 320 de 352 (91%, típico), 1 Elite + 4 Comuns (3 a 4 Ciclos), Fraquezas na cena com Gelo e Vento (Sargento) e Fogo (Larvas e Cascos) → **contrato cumprido com 3**, nenhuma Resistência; B = "O fundo do poço": O Afogado do Poço Sete + 1 Casco Oco (1 Boss + 1 Comum); C vazio.
- **Combate:** encontro A carregado, Ciclo 2, um estado de mesa plausível: Nadir já agiu; Tessaly agindo; uma Larva derrotada; Sargento com Tenacidade 2/5 e Marcado; um Casco Congelado (pendentes descartados); PH 4/5; Energia de cada PJ; uma condição Queimadura no Sargento aplicada pela Nadir. A Fila mostrada é a do oráculo (suíte `exemplo`).
- **Inimigos da campanha:** 2 criados — "Carcereiro Orbital" (o exemplo de 28.4 refeito na faixa 9-12, para mostrar o modo Faixa) e "Capataz do Duto 4" (Capataz Oco ajustado para 5-8, modo Ajustar).
- **NPCs:** 6 no Elenco (saídas do gerador nas Rolagens 1–6, copiadas como valores, com uma nota editada à mão), 4 cartões montados.
- **Missões:** 3 (Ativa: "Fechar o lacre do Poço Sete" — marco; Oferecida: "Apólice da Corporação"; Concluída: "Tirar os mineiros do duto 2").
- **Sessões:** sessão 2 preparada (5 cenas, encontros A e B ligados, 6 pistas, 2 reveladas) e 1 linha de diário (sessão 1).
- **Recompensas:** entrega de marco do nível 2 calculada; 2 linhas de Tesouro (200 Cr de verba de marco, 1 Poção Pequena).
- **Minhas Tabelas:** "Clima no Expresso" com 12 entradas.
- Semente da campanha **2026**.

---

## 15. Guia `COMO-USAR-PLANILHA-DO-MESTRE.md` (estrutura)

No estilo do `COMO-USAR-NO-GOOGLE-PLANILHAS.md` da ficha (frases curtas, passos numerados, sem jargão): 1. Abrir no Drive (importar `.xlsx`, abrir com Planilhas Google, salvar como Planilhas Google; Tabelas e Dados podem ser ocultadas, nunca apagadas). 2. Uma cópia por campanha. 2.1 Como a planilha se organiza (legenda, entradas amarelas, calculadas azuis, avisos em vermelho, "Sugestão da planilha"). 3. Proteger as fórmulas (modo aviso). 4. Começar uma campanha (Campanha → Grupo copiando da ficha de cada jogador, com a tabela "campo da Mestre ↔ célula da ficha"). 5. Semente e "Rolagem nº": como rolar de novo, por que o resultado não muda sozinho. 6. Salvar um resultado (copiar → colar somente valores) com a tabela gerador → registro. 7. Preparar um combate (Inimigos, Bestiário, Encontros, contrato da Fraqueza). 8. Rodar o combate (Fila, PV, Tenacidade e Quebra, condições, Morrendo, avançar o Ciclo em 4 passos). 9. Entre sessões (Sessões, Missões, Campanha, Recompensas). 10. Ampliar as tabelas (100 vagas, Minhas Tabelas). 11. Imprimir o Escudo e os cartões. O Google Planilhas **não usa** a área de impressão nem as quebras de página gravadas no `.xlsx`, por isso o guia ensina o diálogo de impressão do Google passo a passo: Arquivo → Imprimir; "Imprimir: Página atual"; para um cartão só, selecione o intervalo antes e use "Células selecionadas"; Tamanho do papel A4; Orientação Paisagem; Escala "Ajustar à largura"; Margens "Normais"; em "Quebras de página personalizadas", confira as 5 páginas do Escudo ("— página N de 5 —") (as linhas de corte vêm escritas na própria aba, "— página 2 —"). No Excel, a área e as quebras gravadas já funcionam. 12. Checklist de 2 minutos com o Exemplo (células e valores conferidos pela suíte `exemplo`, ex. custo do encontro A = 320, "Contrato cumprido", casa 1 da Fila, PV da Nadir 61) e um teste de digitação (trocar a semente e ver o NPC mudar; voltar e ver o NPC voltar). 13. Se algo der errado. 14. Lista das Sugestões da planilha (H1–H25 em uma linha cada, para o Mestre saber o que não é regra). Um passo de 8 é "Virar a fase do Boss" (3 linhas, 6.10).

---

## 16. Riscos, limites e fora de escopo

- **`formulas` ≠ Google.** Os padrões novos passam pelo `spike` da Mestre; o guia tem a checklist de 2 minutos no Google. Risco residual: desempenho do Google com ~15 000 fórmulas — mitigado por auxiliares de uma conta só (sem `SUMPRODUCT` sobre colunas inteiras), contador corrido O(n) e nenhuma fórmula de matriz.
- **Tempo de teste.** Modelo grande demora a carregar no `formulas`; as suítes usam `outputs` restritos e paralelismo, como a ficha (a bateria da ficha leva ~11 min; a da Mestre deve ficar em até ~20 min).
- **Sem histórico automático no combate:** é limite do "sem macro"; o guia ensina o ciclo de 4 passos e a coluna "PV depois". Pelo mesmo motivo, a planilha não sabe se o Mestre apagou a Redução de Tenacidade na virada de fase. Ela pede isso no aviso da virada e nas 3 linhas de "Virar a fase", mas não consegue conferir.
- **Custo do sorteio não linear:** são 3 células ocultas por campo (≈ 1 200 no total), somadas às ≈ 15 000 fórmulas. Se o Google ficar lento na checklist de 2 minutos, a alternativa já medida é juntar `y` e `x` numa célula só, com `y` escrito 3 vezes dentro de `X`. O resultado é o mesmo, e o oráculo não muda.
- **Fora de escopo:** regras de nave e viagem (27.19), economia detalhada, mapa de galáxia, XP, Habilidades de PJ (são da ficha), importação automática da ficha do jogador (IMPORTRANGE proibido), níveis acima de 20.
- **Não muda nada fora da pasta Mestre, de `build\` (arquivos novos) e de `.agents\tasks\mestre\`.**


---

## 17. Respostas à revisão (ciclo 1)

Revisão: `.agents\tasks\mestre\design-review.md` / `.json` (veredito NEEDS_CHANGES, 9 bloqueantes e 3 não bloqueantes). Todos os 12 achados foram **atendidos**: nenhum foi para o backlog e nenhum foi ignorado. Os requisitos R1–R13 e os 3 entregáveis não mudaram.

| # | Achado | Resposta | Onde |
|---|---|---|---|
| 1 | Semente com correlação linear | **Atendido, com correção além da proposta.** A variante do revisor (`L3 → Q → L3`) foi simulada. Ela corrige os pares, mas continua polinomial: 144/216 triplas de d6 e χ² de 41 149 na 2ª diferença. A adotada é `L3 → Q → L3 → X → L3`, com `X` não polinomial por partição em 16 bits. Ela fecha (f) com 89,7%, as 216 triplas, as 5-uplas e as diferenças de 2ª a 5ª ordem, com intermediários < 2,8·10¹⁴. A rotação de bits foi descartada, porque com M = 2³¹−1 ela equivale a multiplicar mod M. A suíte ganhou a propriedade (g), de correlação serial entre rolagens e entre campos, inclusive os dados do rolador | 5, 12.1 |
| 2 | Aceite de H1 impossível no Dano | **Atendido pela 1ª opção do revisor:** o Dano não é mais interpolado e usa a âncora da faixa do nível, com desvio 0 exigido. Só o PV é interpolado, com limiar de 20% só nessa coluna. O pior desvio medido é −14,7% | 6.7.1, 8 (H1) |
| 3 | Virada de fase pelo PV | **Atendido.** A "fase da barra" é calculada e só avisa. A "fase em vigor" é entrada do Mestre e manda nas Fraquezas, na Tenacidade e na calculadora. O aviso e as 3 linhas de "Virar a fase" pedem para apagar a Redução (a Tenacidade volta ao máximo, 28.5 regra 3) no fim do turno do Boss (regra 5) | 6.10 (C4, C5), 7, 12.1 |
| 4 | Chave da Fila sem atributo de inimigo | **Atendido.** Os termos do inimigo são 0, sem o +20, e os do PJ são limitados a 15–30. Assim o PJ vence o empate de VEL mesmo com Agilidade −1. A não sobreposição dos termos foi verificada, e o oráculo tem os 4 casos fixos | 6.10, 7, 8 (H13), 12.1 |
| 5 | Layout de Combate, Inimigos e Grupo | **Atendido.** A nova decisão D11 (sub-tabelas por assunto, ≤ 9 campos em B:J, rótulo repetido em A, ≤ 13 linhas por cabeçalho, auxiliares ocultas) segue o precedente da aba Progressão da ficha. As divisões estão declaradas para Grupo (4), Inimigos (4 + fases), Bestiário (2), Encontros (2 por encontro) e Combate (C0–C10). O lint confere | 2 (D11), 6.3, 6.7.1, 6.8, 6.9, 6.10, 12.1 |
| 6 | Heurísticas sem número ou sem validação | **Atendido.** H16 e H17 ganharam validação exaustiva (45 casos; 7 rótulos). As heurísticas soltas viraram H12 (Fraquezas sugeridas, com método exato), H19 (troca no encontro aleatório), H20 (50/50 dos ganchos), H22 (cadeia do antagonista), H23 (mais de 3 Ativas), H24 (tom e limites da Sessão Zero) e H25 (quantidades de saída). Os 0–2 consumíveis foram absorvidos em H9, e H21 fica como marcador dessa absorção. Também saiu um aviso de "faixa esperada" de VEL que interpolava 19.1: agora o aviso usa só os extremos 7–25 do livro | 6.2, 6.3, 6.5, 6.6, 6.7.2, 6.9, 6.11, 6.12, 6.14, 8 |
| 7 | `COUNT` fora da lista branca | **Atendido:** `N = SUMPRODUCT(ISNUMBER(ordem)*1)`, e o lint passa a apontar qualquer função fora da lista | 6.8, 12.1 |
| 8 | Índice 0 em Minhas Tabelas | **Atendido:** `MOD(i₀ − 1 + k·passo, n) + 1`. O passo é o primeiro primo da lista que não divide n (sempre existe com n ≤ 100). O mesmo construtor, `varios_sem_repetir`, serve a rumores, bugigangas e loja | 6.17, 6.14, 3.1 |
| 9 | Contagem de `bestiario_fases` | **Atendido:** 12 linhas, conferidas nos cabeçalhos "Fase N" de 28 (305: 2, 580: 2, 750: 2, 935: 3 + 3) | 4.1 |
| 10 | Dependências implícitas de geradores (não bloqueante) | **Atendido.** Há uma tabela fechada de parâmetros por gerador na propriedade (b). A recompensa da aventura passou a usar G = 300 (C = 13, 14) com a faixa da aventura e não lê a aba Recompensas. A faixa do grupo aparece como parâmetro de NPC, aventura e ganchos rápidos | 5, 6.11 |
| 11 | Impressão no Google (não bloqueante) | **Atendido.** A seção 11 do guia traz o diálogo de impressão do Google (A4, Paisagem, Ajustar à largura, células selecionadas, quebras personalizadas), e o Escudo tem linhas visíveis de "página N de 3" | 6.15, 15 |
| 12 | Tique de Embaraço e Aprisionamento (não bloqueante) | **Atendido:** `1d6 × acúmulos` e `1d6 + Ef`, com o Atraso de 1 e 2 casas e o texto de 21.5 sem inventar o momento de resolução | 6.10 (C7), 7 |

Mudança não pedida pela revisão e registrada aqui: as colunas auxiliares passaram de visíveis com 40 px para ocultas (D11). Um valor de sorteio de 10 dígitos em 40 px vira "####", o que contraria "sem texto cortado", e a ficha já oculta as suas auxiliares.
