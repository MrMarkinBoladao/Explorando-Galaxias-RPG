# Relatório da v1.2 — auditoria de opções-armadilha e contradições de obrigatoriedade

Origem: você montou uma arma de Energia (2d8, Longa, Sincronia) com Elemento Raio e perguntou por que
escolheria a propriedade **Recarga**, que só cobra. A resposta honesta era "você não escolheria" — e daí
veio o pedido de varrer o livro procurando mais nada assim, subir para a v1.2 e regerar o PDF e a ficha.

Detalhe por achado em `achados-v12.md`. Este arquivo é o fechamento: o que mudou, o que não mudou, o que
foi gerado e o que cada bateria respondeu.

---

## 1. As decisões que você tomou

| Ponto | Decisão | Onde entrou |
|---|---|---|
| **A2 — Raio dominado pelo Fogo** | Opção 2: Choque passa de 2 para **3 turnos** | 21.2, 21.5 e a frase dos três grupos de Elemento em 20.1 |
| **A3 — Avginiano dominado pelo Xianzhouíta** | Opção 2: bônus vira **+2 em Discernimento ou Presença** | 05, na seção da Raça e na tabela de consulta rápida |
| **Planilha do Mestre** | Sobe para **V1.2** junto com o resto | `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx` |
| **B6 — condição de recarga de Habilidade** | Texto **com número**: 1 vez por combate em troca de 1 PH menos, piso 1 PH | 16.7, com a linha do checklist de 16.8 apontando para lá |

A frase "nenhuma Raça é melhor que outra" ficou no capítulo 05, por sua ordem. Nenhum traço racial novo
foi inventado e a Mente de Ferro continua igual.

Na conferência final você decidiu mais duas coisas, as duas aplicadas:

| Ponto | Decisão | O que foi feito |
|---|---|---|
| **Cabeçalho das Ressonâncias nas planilhas** (achado E15) | Alinhar com o livro | "Escolha uma opção" → **"O que ela dá"** nas abas Dados da Ficha e da Planilha do Mestre; as duas foram regeradas |
| **Linha de base da ficha usada pela bateria da Mestre** | Regravar, provando antes que a lista de alterados é a esperada | Linha de base regravada, anterior guardada em `baseline-hashes-antes-v12.json`; a prova está na seção 8 |

## 2. Os números alterados — antes e depois

Cinco mudanças mexeram em regra. Cada uma está **dentro de uma lista de opções**, que era o alvo da
auditoria; nada da economia central foi tocado.

| # | Lista a que pertence | Onde | Antes | Depois |
|---|---|---|---|---|
| 1 | as 7 condições de Quebra | 21.2 e 21.5, **Choque** | 2 turnos | **3 turnos** |
| 2 | as 7 Raças | 05, **Avginiano** | +2 em Discernimento, fixo | **+2 em Discernimento ou Presença** |
| 3 | as 6 categorias de arma | 24.2, **Leve** | Espaço 1 | **Espaço 0,5** |
| 4 | as 4 propriedades de arma | 24.2, **Arremessável** | um alcance acima | **dois passos acima, no máximo Extrema** |
| 5 | — (regra que faltava) | 16.7, **condição de recarga** | não existia | 1 vez por combate por 1 PH menos, piso 1 PH |
| 6 | as 6 categorias de arma, refletidas no Memoespírito | 11.4, **dados do Memoespírito** | a escada `1 / 2 / 3 / 4 / 5`, sem a exceção da Energia | as duas escadas: `1 / 2 / 3 / 4 / 5` e, para **Energia**, `2 / 3 / 4 / 5 / 6` |

A **6** é o achado que você levantou depois, lendo o livro. Ela não vem da auditoria de dominância e está
detalhada na seção 10: **para quem usa arma de Energia, o Memoespírito rolava um dado a menos** — 1d6 no
nível 1 e 5d6 no 17, quando devia ser 2d6 e 6d6. Era erro de dano, no livro **e** na ficha.

Estrutural, não numérico: a propriedade **Recarga** saiu da tabela de 24.2, que ficou com 4 linhas, e
"precisa recarregar" passou a ser sabor livre, de graça, que não consome a propriedade especial.

**Não mudou nada** em: dados base de arma, tabela de progressão, PV por nível, totais de PH e de Energia,
orçamento de encontro, DTs, bestiário e os Danos de Quebra de 20.5. A Leve continua 1d8 a 100 Cr.

## 3. Achados reportados e NÃO corrigidos

| Achado | Por que ficou de fora | Recomendação |
|---|---|---|
| O custo "duas mãos" de **Peso de impacto** é fictício: empunhadura não tem peso mecânico no sistema | Não é opção-armadilha (nenhuma propriedade é dominada por ela) e consertar exigiria inventar regra de empunhadura | Deixar como está, ou criar a regra de empunhadura numa versão futura — é escopo novo, não correção |
| **"Efeito menor"** (16.5, Buff/Debuff Nível 2) nunca é definido, enquanto "efeito maior" é | Lacuna de definição, não defeito A/B | Definir numa próxima passagem de redação de 16.5 |
| A arma de **Energia** começa em 2 dados | É trade declarado (2 de Espaço, duas mãos, 500 Cr, atributo Sincronia) e mexer nisso seria economia central | Não mexer |
| Com a Leve em 0,5 de Espaço, **Dissimulada** numa arma Leve entrega só o "passa por busca superficial" | Dissimulada continua não dominada: vale nas 6 categorias e o bypass de busca é exclusivo dela | Se quiser reverter, custa uma célula em 24.2 e dois espelhos de oráculo |

## 4. Arquivos alterados

**Livro (14 `.md` em `livro-v1.0\`)** — `00-capa-e-creditos.md`, `00-changelog-v11-para-v12.md` (novo, 19
correções E1–E19), `05-racas.md`, `11-caminho-recordacao.md`, `16-habilidades.md`,
`17-ultimate-e-energia.md`, `18-combate.md`, `20-elementos-tenacidade-e-quebra.md`, `21-condicoes.md`,
`24-equipamentos.md`, `25-cones-de-luz-e-reliquias.md`, `26-progressao-e-ressonancias.md`,
`27-guia-do-mestre.md`, `28-bestiario.md`. Os dois últimos a entrar foram o 11 e o 28, pelos achados da
seção 10.

**Código** — `build\gerar_pdf.py`, `build\gerar_docx.py`, `build\gerar_ficha.py`, `build\testar_ficha.py`,
`build\oraculo_ficha.py`, `build\oraculo_mestre_hist.py`, `build\oraculo_mestre_cmb.py`,
`build\mestre\aba_combate_inimigos.py`, `build\mestre\nucleo.py`, `build\mestre\__init__.py`,
`build\gerar_mestre.py`, `build\testar_mestre.py`, `scripts\verificar-livro-final.ps1`.

**Correção de versão corrente que faltava, achada na conferência de integração** —
`build\ficha_dados.py` (as duas linhas do cabeçalho ainda diziam "v1.1" e
"00-changelog-v10-para-v11", enquanto `testar_ficha.py` e `oraculo_ficha.py` já diziam v1.2) e
`ficha-automatizada\COMO-USAR-NO-GOOGLE-PLANILHAS.md` (o guia do jogador mandava importar o
`.xlsx` **V1.1** e dizia "livro v1.1" no subtítulo e no checklist). Detalhe em 8.2.

**Correção do achado do autor (seção 10)** — `livro-v1.0\11-caminho-recordacao.md`,
`livro-v1.0\28-bestiario.md`, `livro-v1.0\00-changelog-v11-para-v12.md` (E17, E18 e E19),
`build\gerar_ficha.py` (a fórmula de `memo.n`), `build\oraculo_ficha.py` (o `n_m` do Memoespírito),
`build\testar_ficha.py` (os casos **(e2)** da suíte `ouro`, nos dois lados) e
`build\mestre_lexico_extra.txt`.

**Cabeçalho de 26.7 (E15), os 5 pontos que tinham o texto antigo** — o cabeçalho é lido por nome, então
trocar um só criaria inconsistência nova. Foram juntos: `build\ficha_dados.py` (cabeçalho do bloco),
`build\gerar_ficha.py` (o `dcol('ressonancias', …)` da aba Progressão), `build\mestre_dados.py` (cabeçalho
do bloco), `build\mestre\aba_recompensas.py` (o `dcol(…)` da aba Recompensas) e
`build\mestre\testes_hist.py` (a conferência de 26.7 contra o livro). A busca por "Escolha uma opção" em
`build\**\*.py` só devolve, agora, a mensagem de aviso de escolha de Caminho em `gerar_ficha.py`, que é
outra coisa. Os dois `*_mapa.json` passaram a dizer `"O que ela dá": "C"` ao serem regerados;
`build\google_rev1\ficha_mapa_rev1.json` **não** foi tocado (é export congelado, e a suíte `google` liga as
células por nome lógico, não por nome de coluna).

**Ajustes de manutenção desta etapa** (nenhum muda regra do jogo):

- `build\ficha_lexico_extra.txt` e `build\mestre_lexico_extra.txt`: saíram as palavras que o texto novo da
  v1.2 trouxe para o livro (`cabeçalho`, `conferida`, `listas`, `secundária`, `totais`, `xlsx` na ficha;
  `cabeçalho`, `gastas`, `listas`, `observação`, `sabia` na Mestre). As duas suítes `texto` falham de
  propósito quando uma palavra está nos dois lugares.
- `build\testar_ficha.py`: a suíte `google` ganhou a tabela `LIVRO_V12`, com as quatro células em que o
  export do Google (de 04/10, da v1.1, e que não pode ser refeito) tinha de divergir da v1.2 — Espaço da
  Leve, duração do Choque, acúmulo do Cisalhamento e o texto da Ressonância IV. Só o par exato
  (valor antigo → valor novo) é aceito; qualquer outra diferença continua falhando.
- `build\oraculo_mestre_hist.py`: o texto da Ressonância IV passou a ser o de 26.7 (espelho hardcoded que
  o FEAT-002 não tinha mapeado). Era o que fazia as suítes `dados` e `oraculo` da Mestre divergirem.
- `scripts\verificar-livro-final.ps1`: o BOM de UTF-8 do arquivo se perdeu na edição das strings de versão,
  e sem ele o PowerShell 5.1 lê os acentos errado e o script não compila. O BOM foi restaurado; o conteúdo
  não mudou.
- `build\mestre_lexico_extra.txt`: saiu `nomear`, pelo mesmo motivo das outras — o quadro novo de 11.4 e
  as linhas E18/E19 do changelog levaram a palavra para o livro, e a suíte `texto` da Mestre falha de
  propósito quando a mesma palavra está no léxico do livro e nesse arquivo. Ficou um comentário no topo
  do arquivo registrando a saída.
- `build\ficha_dados.py`: as duas linhas do cabeçalho que diziam qual versão o módulo transcreve ainda
  estavam em v1.1 ("Explorando Galáxias v1.1" e "o conteúdo é a v1.1 — 00-changelog-v10-para-v11"),
  enquanto `testar_ficha.py` e `oraculo_ficha.py` já diziam v1.2. É versão corrente, não registro de
  decisão: as duas foram para v1.2, apontando para o changelog novo. Nenhuma linha de código mudou.
- `ficha-automatizada\COMO-USAR-NO-GOOGLE-PLANILHAS.md`: o guia do jogador mandava importar
  `Ficha Automatizada - Explorando Galáxias V1.1.xlsx` e dizia "livro v1.1" no subtítulo e no checklist de
  2 minutos. Com o V1.2 na mesma pasta, o guia estava apontando para o modelo velho. As três menções
  passaram para V1.2; o passo a passo, as células do checklist e os valores conferidos não mudaram.

**Gerados** — `build\ficha_mapa.json`, `build\mestre_mapa.json`, `build\ficha_protegidos.json` (linha de
base refeita, 38 hashes), `build\ficha_funcoes_ok.json`, `ficha-automatizada\Ficha Exemplo - Nadir.xlsx`,
`Mestre\Planilha do Mestre - Exemplo.xlsx`, as prévias em `.agents\tasks\ficha-preview\` e
`.agents\tasks\mestre\preview\`.

**Linha de base de outra tarefa, regravada com a sua autorização** —
`.agents\tasks\mestre\baseline-hashes.json`, com a versão anterior guardada em
`baseline-hashes-antes-v12.json`. A prova de que a lista de alterados é a esperada está na seção 8.

## 5. Entregáveis V1.2

| Arquivo | Tamanho | Data |
|---|---|---|
| `Sistema de HSR by MC Filhos V1.2.docx` | 15 308 875 bytes (14,6 MB) | 06/10/2026 18:17:17 |
| `Sistema de HSR by MC Filhos V1.2.pdf` | 18 291 156 bytes (17,4 MB) | 06/10/2026 18:17:48 |
| `ficha-automatizada\Ficha Automatizada - Explorando Galáxias V1.2.xlsx` | 138 550 bytes | 06/10/2026 17:59:39 |
| `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx` | 535 049 bytes | 06/10/2026 18:00:59 |

Os quatro foram **regerados** depois das correções da seção 10 (E17, E18 e E19): o livro mudou de texto em
dois capítulos e no changelog, e a ficha mudou de fórmula no bloco do Memoespírito. O DOCX e o PDF saíram
por último, porque o changelog foi o último `.md` a mudar.

O DOCX e o PDF saíram com os 34 capítulos, o changelog novo entrando sozinho pela ordenação do prefixo
(`[04/34] 00-changelog-v11-para-v12.md`). O PDF tem 261 páginas, 297 tabelas, 0 aviso.

**Os cinco entregáveis V1.1 continuam no disco, intactos, com a data de modificação original:**

| Arquivo | Tamanho | Data |
|---|---|---|
| `Sistema de HSR by MC Filhos V1.1.docx` | 15 298 480 bytes | 04/10/2026 21:27:42 |
| `Sistema de HSR by MC Filhos V1.1.pdf` | 18 264 614 bytes | 04/10/2026 21:28:07 |
| `Modelo para copia - Ficha players - Explorando Galáxias V1.1.gsheet` | 195 bytes | 05/10/2026 11:39:03 |
| `ficha-automatizada\Ficha Automatizada - Explorando Galáxias V1.1.xlsx` | 138 536 bytes | 05/10/2026 08:31:17 |
| `Mestre\Planilha do Mestre - Explorando Galáxias V1.1.xlsx` | 535 024 bytes | 05/10/2026 19:41:55 |

Nada foi sobrescrito e nada foi apagado: os V1.2 saíram ao lado.

## 6. Conferência visual do PDF V1.2

Na rodada da seção 10 as páginas novas foram conferidas do mesmo jeito, a 100 dpi, em
`.agents\tasks\v12\png-e17\`: as duas páginas do changelog com E17, E18 e E19 (**29 e 30**), as duas
páginas de 11.4 e 11.5 (**99 e 100**), as outras do capítulo 11 (94, 97, 98), a nota de 26.2 (**181** e
**183**) e a do Autômato de Guerra no 28 (**210**). A varredura automática de bloco de texto fora da área
útil deu **0** nas dez páginas (fora o número do pé, que é por projeto), e `gerar_pdf.py` reportou
**avisos: 0**.

Essa conferência pegou um defeito real: na primeira passada a linha **E19** tinha sido escrita **depois**
de uma linha em branco e ficou **fora** da tabela do changelog — o PDF mostrava os `|` crus como texto
corrido. A linha foi movida para dentro do bloco da tabela, o `.md` voltou para LF (a reescrita tinha
convertido o arquivo para CRLF, contra os outros 33), e o DOCX/PDF foram regerados. Na segunda passada a
tabela de 19 linhas fecha certo, repetindo o cabeçalho nas páginas 29 e 30, sem linha órfã nem cortada.

As páginas alteradas foram renderizadas em PNG a 100 dpi e olhadas uma por uma: changelog novo
(27–30), capa (1), Avginiano (57), 16.5–16.8 (125–128), 17.3 e 17.4 (131–133), 18.7 (141), 20.1 (149),
21.2 (155), 21.5 (159), 24.2 a 24.7 e o resumo (168–174), 25.2 (175–178), 26.7 (183–185) e 27.9 (186–194).

A tabela larga do changelog, de 16 linhas e 5 colunas, **não quebrou**: cabe na área útil, repete o
cabeçalho nas páginas 28 e 29 e nenhuma linha ficou órfã ou cortada. As 41 páginas também passaram por
uma varredura automática de bloco de texto fora da área útil — o único bloco fora da margem em cada
página é o número do pé, que é por projeto.

## 7. Saída das baterias

**`python build\testar_ficha.py --suite tudo` — código de saída 0, as 11 suítes OK**

```
spike       OK      23 checagens, 0 falha(s)
protegidos  OK      76 checagens, 0 falha(s)
dados       OK      3294 checagens, 0 falha(s)
ouro        OK      539 checagens, 0 falha(s)
oraculo     OK      247 checagens, 0 falha(s)
extremos    OK      2714 checagens, 0 falha(s)
lint        OK      11922 checagens, 0 falha(s)
texto       OK      1006673 checagens, 0 falha(s)
preview     OK      278 checagens, 0 falha(s)
visual      OK      24029 checagens, 0 falha(s)
google      OK      4735 checagens, 0 falha(s)
```

Essa rodada é a final, já com as correções da seção 10 e os quatro entregáveis regerados. A `ouro` passou
de 533 para **539** checagens: são os casos **(e2)** novos, da arma de Energia no Memoespírito.
A `dados` é a que prova que a planilha bate com o livro novo, relendo os `.md` com parser próprio: os
quatro números da auditoria passaram. A `protegidos` foi refeita depois de gerar o DOCX e o PDF V1.2 —
apagar `build\ficha_protegidos.json` e rodar a suíte é o procedimento — e a nova linha de base tem os 34
`.md` do livro corrigido (inclusive o changelog novo), os dois entregáveis V1.2 e
`gerar_docx.py`/`gerar_pdf.py`; os V1.1 saíram da lista, igual ao que se fez com os V1.0. Rodada uma
segunda vez, a suíte sai 0 sem regravar nada (76 checagens, 38 arquivos conferidos).

**`powershell -File scripts\verificar-livro-final.ps1` — código de saída 0**

As quatro checagens do livro passam (nomenclatura, tabelas, completude, simulação de combate), o DOCX
V1.2 existe com 14,6 MB e está mais novo que o `.md` mais recente, as **576** citações de "capítulo NN"
resolvem sem nenhuma quebrada, o glossário cobre 42 de 42 termos e as 297 tabelas reabrem sem célula
vazia (3 688 parágrafos e 7 511 células, contra 3 684 e 7 496 antes da seção 10).

**`python build\testar_mestre.py --suite tudo` — código de saída 0, as 13 suítes OK**

```
spike        OK      142 checagens, 0 falha(s)
protegidos   OK      127 checagens, 0 falha(s)
dados        OK      803 checagens, 0 falha(s)
bestiario    OK      34 checagens, 0 falha(s)
ouro         OK      130 checagens, 0 falha(s)
oraculo      OK      604308 checagens, 0 falha(s)
determinismo OK      161479 checagens, 0 falha(s)
extremos     OK      1029 checagens, 0 falha(s)
lint         OK      149535 checagens, 0 falha(s)
texto        OK      6252932 checagens, 0 falha(s)
preview      OK      688 checagens, 0 falha(s)
visual       OK      33714 checagens, 0 falha(s)
sabor        OK      9269 checagens, 0 falha(s)
```

Total: **7 214 190 checagens, 0 falha(s)**, em 8 904 s. A `dados` e a `oraculo` são as que provam que o
texto do item de 24.3, a duração do Choque e o texto da Ressonância IV batem entre livro, oráculos e a
planilha V1.2.

**A ordem das três, e por que ela importa:** DOCX e PDF primeiro, depois a linha de base de `protegidos`
refeita, depois a bateria da ficha, depois a linha de base de hashes da Mestre, e só então a bateria da
Mestre. Rodar fora dessa ordem faz `protegidos` ou a linha de base falharem por construção. O `diff` final
dos 14 arquivos, depois de tudo, deu **0 divergentes e 1 ausente conhecido** — a bateria da Mestre
continua não escrevendo em nenhum arquivo da ficha.

## 8. A linha de base da ficha usada pela bateria da Mestre

A suíte `protegidos` da Mestre confere, por SHA-256, se os 14 arquivos **da ficha** listados em
`.agents\tasks\mestre\baseline-hashes.json` continuam idênticos. É o guarda que prova que o trabalho da
Planilha do Mestre nunca escreve em arquivo da ficha. A v1.2 mexeu legitimamente em parte deles, você
autorizou a regravação com a condição de provar antes que a lista de alterados era a esperada, e é isso
que está abaixo.

**Alterados: 8 — os 7 previstos mais `ficha_dados.py`, que mudou pelo cabeçalho de 26.7 que você aprovou
na mesma mensagem.** Cada um com a mudança que o explica:

| Arquivo | O que mudou nele |
|---|---|
| `build\gerar_ficha.py` | A1: as amostras de propriedade de arma deixaram de citar Recarga; versão corrente 1.1 → 1.2 e caminho de saída V1.2; E15: o `dcol('ressonancias', …)` da aba Progressão passou a usar "O que ela dá" |
| `build\testar_ficha.py` | A1: `_OR_PROPRIEDADES` sem Recarga e o caso de propriedade dupla trocado; caminho do `.xlsx` e os dois arquivos protegidos agora V1.2; tabela `LIVRO_V12` nova na suíte `google` |
| `build\oraculo_ficha.py` | A3: `RACAS['Avginiano']` com dois atributos; A6: `ARMAS['Leve']` com Espaço 0,5; docstrings de versão corrente |
| `build\ficha_dados.py` | **E15: cabeçalho do bloco de Ressonâncias "Escolha uma opção" → "O que ela dá"** (a decisão que você tomou na conferência final) |
| `build\ficha_funcoes_ok.json` | Gerado pela suíte `spike` a cada execução — ele grava os tempos de carga, então o hash muda em toda rodada da bateria da ficha |
| `build\ficha_protegidos.json` | Linha de base de hashes do livro, refeita de propósito depois de gerar o DOCX e o PDF V1.2 |
| `build\ficha_mapa.json` | Gerado por `gerar_ficha.py` (contrato gerador × testes), reescrito nas duas regerações |
| `ficha-automatizada\Ficha Exemplo - Nadir.xlsx` | Gerado por `gerar_ficha.py` junto do modelo |

**Intactos: 5, com hash idêntico** — `renderizar_ficha.py`, `requirements-ficha.txt`,
`AUDITORIA-DA-FICHA.md`, `COMO-USAR-NO-GOOGLE-PLANILHAS.md` e
`Ficha Automatizada - Explorando Galáxias V1.1.xlsx`. É isso que continua provando que nada escreveu
em arquivo da ficha por fora do trabalho da v1.2 — em particular, o entregável V1.1 da ficha não foi
tocado. (O `COMO-USAR` deixou de estar intacto depois disso, na conferência de integração: veja 8.2.)

**Ausente: 1** — `Cópia de Ficha Automatizada - Explorando Galáxias V1.1.xlsx`, que já faltava antes da
Fase 1 da Mestre (exceção P5, documentada em `build\mestre\testes_base.py`). A entrada foi **preservada na
lista com o hash antigo**, para não apagar o registro.

A versão anterior está guardada em `.agents\tasks\mestre\baseline-hashes-antes-v12.json` (2 364 bytes,
com a data original 05/10 11:37:09), ao lado dos dois backups que a própria tarefa da Mestre já tinha
feito pelo mesmo motivo. Depois da regravação, `testar_mestre.py --suite tudo` fecha **13 de 13**.

Uma observação para as próximas rodadas: como `ficha_funcoes_ok.json` grava tempo de carga, **toda
execução da bateria da ficha invalida essa linha de base de novo**. A ordem que funciona é rodar a bateria
da ficha, regravar a linha de base e só então rodar a bateria da Mestre. Foi essa a ordem usada aqui, e um
`diff` final dos 14 arquivos depois da bateria da Mestre deu 0 alterados — ou seja, a bateria da Mestre
realmente não escreveu em nenhum arquivo da ficha.

## 8.1 Conferência do cabeçalho novo nas planilhas

As duas planilhas foram regeradas e o bloco de Ressonâncias saiu com `{'Ressonância': 'A', 'Nível': 'B',
'O que ela dá': 'C'}` nos dois mapas. Na renderização: a suíte `preview` da ficha mediu 40 PNGs e 348
recortes com **0 texto cortado**; a `visual` mediu 22 617 textos em 4 estados com **0 que não couberam**;
a lista informativa de colunas largas continua com as mesmas 57 colunas de antes da troca, e
`'Dados'!C` **não** aparece nela. As larguras da aba Dados não mudaram (A/B/C = 26/20/20 na ficha e
34/22/22 na Mestre) — o cabeçalho novo é mais curto que o antigo, e a coluna já era dimensionada pelo
texto das opções, que é muito maior que qualquer um dos dois cabeçalhos.

## 8.2 Conferência de integração e a segunda regravação da linha de base

Fechada a geração, uma passagem de integração reconferiu as costuras entre as três etapas da v1.2:
versão corrente em 1.1 num arquivo e 1.2 noutro, texto do item de 24.3 contra `oraculo_mestre_hist.py`,
lista de propriedades de arma contra as constantes escritas à mão, linha de base de protegidos e
presença dos quatro entregáveis V1.2. O texto do item, a lista de propriedades (as 4 linhas de 24.2
contra `_OR_PROPRIEDADES`), a linha de base de protegidos e os entregáveis já estavam coerentes. As duas
costuras de versão que sobraram estão na seção 4: `build\ficha_dados.py` e
`ficha-automatizada\COMO-USAR-NO-GOOGLE-PLANILHAS.md`.

Essas duas edições alteraram dois dos 14 arquivos conferidos pela linha de base da Mestre, e a rodada
final da bateria da ficha alterou `ficha_funcoes_ok.json` de novo (ele grava tempo de carga). O `diff`
antes de regravar deu exatamente esses **3 alterados**, com os outros **10 idênticos** — inclusive
`Ficha Automatizada - Explorando Galáxias V1.1.xlsx`, `renderizar_ficha.py`, `requirements-ficha.txt`,
`AUDITORIA-DA-FICHA.md`, `ficha_protegidos.json` e `ficha_mapa.json` — e a entrada ausente de sempre
preservada com o hash antigo. Só os três hashes foram trocados no arquivo; a versão anterior está em
`.agents\tasks\mestre\baseline-hashes-antes-correcao-v12.json`.

**Armadilha de ambiente que apareceu aqui, para a próxima rodada:** escrever esse JSON com
`Set-Content -Encoding UTF8` do PowerShell 5.1 **grava um BOM**, e `testes_base.py` lê o arquivo com
`encoding="utf-8"` — a suíte `protegidos` da Mestre morre com
`JSONDecodeError('Unexpected UTF-8 BOM')`. É o oposto do caso dos `.ps1`, que **precisam** de BOM. O
arquivo tem de ser gravado com `UTF8Encoding($false)`. Foi assim que ele ficou.

**Terceira regravação, depois das correções da seção 10.** O `diff` deu **6 alterados** e **7 idênticos**:
`gerar_ficha.py` (a fórmula de `memo.n`), `oraculo_ficha.py` (o `n_m`), `testar_ficha.py` (os casos (e2)),
`ficha_funcoes_ok.json` (gerado pela `spike`), `ficha_protegidos.json` (linha de base do livro refeita
depois do DOCX/PDF novos) e `Ficha Exemplo - Nadir.xlsx` (regerada por `gerar_ficha.py`). Ficaram com
hash **idêntico** `ficha_dados.py`, `ficha_mapa.json` (o mapa guarda endereço e nome lógico, não a
fórmula), `renderizar_ficha.py`, `requirements-ficha.txt`, `AUDITORIA-DA-FICHA.md`,
`COMO-USAR-NO-GOOGLE-PLANILHAS.md` e — o que importa — o entregável
`Ficha Automatizada - Explorando Galáxias V1.1.xlsx`. A versão anterior ficou em
`.agents\tasks\mestre\baseline-hashes-antes-e17.json`.

Uma pendência que só você pode fechar, registrada aqui porque não é coisa de código: os dois atalhos
`.gsheet` (o `Modelo para copia - Ficha players - Explorando Galáxias V1.1.gsheet` da raiz e o
`Planilha do Mestre - Explorando Galáxias V1.1.gsheet` em `Mestre\`) apontam para planilhas que vivem no
Google, e por isso continuam na V1.1. Para publicar a V1.2 para a mesa, o caminho é o passo 1 do
`COMO-USAR`: subir o `.xlsx` V1.2 e salvar como Planilhas Google.

## 9. Intocáveis

- **Nada** dentro de `Explorando Galáxias RPG - Players\` foi lido, criado, modificado ou apagado. A pasta
  foi tratada como inexistente: nenhuma busca, nenhum `Get-ChildItem`, nenhum arquivo aberto.
- **Nada** em `versões antigas\` foi tocado.
- A pasta `livro-v1.0` não foi renomeada (nome legado; o conteúdo é a v1.2).
- Os exports do Google em `build\google_rev1\` não foram movidos nem alterados.
- Nenhum comando `git` foi executado: este projeto não é repositório git.
- Vale igual para a rodada da seção 10: as buscas foram filtradas para `livro-v1.0\`, `build\` e
  `scripts\`, os entregáveis V1.1 foram reconferidos por SHA-256 depois de tudo e continuam idênticos, e
  nada em `Explorando Galáxias RPG - Players\` ou em `versões antigas\` foi aberto.

---

## 10. O achado que você levantou lendo o livro (E17, E18 e E19)

Você montou a arma de **Energia** (2d8, Longa, Sincronia), foi ler o bloco do Memoespírito em 11.4 e topou
com dois defeitos no mesmo parágrafo. O detalhe completo está na seção 11 de `achados-v12.md`.

### 10.1 O que estava escrito, e o que ficou

| # | Classe | Antes | Depois |
|---|---|---|---|
| **E17** | **Numérico** | "a contagem de dados da sua arma pela tabela mestra (capítulo 26): **1** dado nos níveis 1-4, **2** nos 5-8, **3** nos 9-12, **4** nos 13-16 e **5** nos 17-20" | As **duas** escadas: `1 / 2 / 3 / 4 / 5` e, para arma de **Energia**, `2 / 3 / 4 / 5 / 6`, "que começa em dois dados e carrega esse dado a mais pela progressão inteira" |
| **E18** | Redação | "O dado **dele** é sempre **d6**, independente da sua arma" | "**A sua arma empresta ao Memoespírito quantos dados ele rola, nunca qual dado.** … a **quantidade** vem de você; o **tipo** é do **Memoespírito**, e é sempre **d6**" |
| **E19** | Redação | Três pronomes sem antecedente, achados pela varredura: duas linhas da Técnica Auxiliar em 11.5 e a nota da Resistência a Quântico do Autômato de Guerra, no 28 | "…do próximo turno **daquele aliado**", "…do próximo turno **daquele inimigo**" e "tira 2 dados **do ataque desse personagem** — a Resistência penaliza quem ataca, não quem defende (20.2)" |

**O número que mudou, com antes e depois:** o Memoespírito de quem carrega arma de **Energia** passou de
**1d6 para 2d6 no nível 1**, 2d6→3d6 no 5, 3d6→4d6 no 9, 4d6→5d6 no 13 e **5d6 para 6d6 no 17**. Para as
outras cinco categorias **nada mudou**. No exemplo de nível 17 do livro, que agora declara a arma **Média**,
o dano continua `5d6 + 5` ≈ 22; a linha nova mostra o mesmo personagem com arma de Energia em `6d6 + 5` ≈ 26.

Dois acréscimos de apoio no mesmo bloco: o exemplo passou a **declarar a categoria da arma** (sem isso o
`5d6 + 5` dele seguia ambíguo) e ganhou a linha do caso de Energia. O quadro
`> **O que mudou da v1.1:**` de 11.4 registra os dois defeitos, como o livro faz nas outras seções.

### 10.2 A classe de defeito, para registro

Isto **não** é opção-armadilha nem contradição de obrigatoriedade: é **erro de consistência interna** —
uma regra local que **repete** um número da tabela mestra em vez de referenciá-la, e no caminho perde a
exceção. A auditoria da v1.2 estava calibrada para dominância entre opções e por isso passou por cima.
Fica anotado porque o defeito reaparece em qualquer ponto onde o livro reescreve um número que já mora em
outro capítulo — e o antídoto é referenciar, não recopiar.

### 10.3 A varredura por reincidência: o que ela achou

**(i) A escada sem a exceção da Energia — um só caso, e a fonte canônica está intacta.** Procurei em
`livro-v1.0\*.md` por `partindo de 1`, `se for de Energia`, `dado a mais sobrevive`, `começa com 2`,
`Dados de Ataque Básico`, `dado nos níveis`, `dados por faixa`, `+1 dado` e pelas cinco faixas de nível.
A **nota da coluna em 26.2** — a fonte canônica, que era a sua prioridade máxima — **tem** a frase certa:
"partindo de 1. Uma arma de **Energia** começa em 2 e chega a **6** no nível 17". As duas outras
reafirmações, em **18.5** (com a linha própria da Energia na tabela, `2d8` → `6d8`) e no quadro de
**24.2**, também estão corretas. A ficha em branco do Memoespírito em 29 **referencia** em vez de repetir
("dados de Ataque Básico do dono, em d6"). O único lugar errado era **11.4**. Todas as outras ocorrências
de "+1 dado" são dados **adicionais** dentro do teto do capítulo 26, outro assunto.

**(ii) Pronome sem antecedente em regra — três casos, todos no E19.** Li uma por uma as 122 ocorrências de
"dele"/"dela" nos capítulos em que dois sujeitos convivem: 52 no 11 (dono e Memoespírito), 56 no 28
(personagem e inimigo), 6 no 21 (quem marca e quem é marcado), 6 no 23 (quem executa e quem é executado) e
2 no 13. O critério foi o seu: só onde há **dois sujeitos possíveis na mesma frase** e a regra **muda de
sentido** conforme a leitura. Os três que passaram estão na tabela de 10.1. O do capítulo 28 era o mais
grave dos três, porque a leitura errada **invertia** a regra — parecia que o Elite tirava dados do próprio
ataque, quando 20.2 diz que Resistência é -2 dados para **quem ataca**.

Os que **não** passaram ficaram como estão, de propósito, e estão listados um por um em `achados-v12.md`
§11.2: os verbetes de condição do 21 têm um sujeito só (o alvo) e usam o idioma padrão de duração do livro;
a Execução no 23 já nomeia "o executor"; Marcado e Controlado já nomeiam "quem aplicou" e "o alvo"; e no 28
e no 11 o pronome é o inimigo e o Memoespírito, que são os sujeitos dos capítulos.

### 10.4 A ficha errava junto; a Planilha do Mestre, não

| Ponto | Estado |
|---|---|
| Ataque Básico do **próprio personagem**, na ficha e no oráculo | **Já estava certo**, e não dependia de o jogador digitar nada: a fórmula é `nucleo.dados_ab + VLOOKUP(categoria, armas, 3) - 1`, e a coluna 3 da tabela de armas de 24.2 vale **2** na Energia. No oráculo, `dados_ab(L) + extra`, com `extra = 1` em `ARMAS["Energia"]` |
| **Dados de dano do Memoespírito** (`memo.n`) em `build\gerar_ficha.py` | **ERRADO, corrigido.** Era a escada crua, `nucleo.dados_ab + IF(Forma Completa,1,0)`. Passou a somar o mesmo termo de arma que o Ataque Básico já usava |
| **`memo.n`** em `build\oraculo_ficha.py` | **ERRADO, corrigido.** `dados_ab(L) + (cat_arma[1] se houver arma) + (1 se Forma Completa)` |
| `build\mestre_dados.py`, `build\mestre\*`, `build\oraculo_mestre*.py` | **Nada a corrigir.** A Planilha do Mestre não modela Memoespírito nem a escada de dados do jogador — grep de `Memoesp`, `dados_ab` e `Dados de Ataque Básico` em todo o pacote da Mestre não devolve nada |

**A suíte não cobria a categoria, como você suspeitou.** O caso **(e)** da suíte `ouro` é o Memoespírito de
nível 17 de 11.4, e o personagem dele usa a arma **Pesada** padrão do fixture: passava com 5 dados mesmo
com o bug. Entrou um caso **(e2)**, nos **dois** lados da suíte (oráculo e planilha calculada): a mesma
ficha com arma de **Energia** dá `6d6+5`, média **26** e **33** contra Fraqueza no 17; no nível 1 dá
`2d6+5`; e a mesma ficha com arma **Média** no nível 1 dá `1d6+5` — o guarda contra a correção vazar para
as outras cinco categorias. A `ouro` do oráculo passou de 219 para **228** checagens.Os quatro achados conhecidos e não corrigidos da seção 3 continuam valendo, com a mesma recomendação.

---

## 12. Conferência de fechamento (07/10, madrugada)

**A revisão independente foi dispensada pelo autor.** Não houve passo de revisor nesta versão; as
correções das seções 1, 2 e 10 estão aprovadas por ele diretamente. Este fechamento é conferência, não
implementação nova: a única coisa que mudou no disco aqui foi um hash da linha de base (12.4) e os PNGs
de conferência (12.3).

### 12.1 Os quatro entregáveis, reconferidos no disco

Conferidos **depois** das três baterias desta rodada: tamanho e data idênticos aos da seção 5, ou seja
nenhuma bateria regerou entregável. Todos com data **posterior** à última correção do capítulo 11
(`livro-v1.0\11-caminho-recordacao.md`, 06/10 17:55:39).

| Arquivo | Tamanho | Data |
|---|---|---|
| `Sistema de HSR by MC Filhos V1.2.pdf` | 18 291 156 bytes | 06/10/2026 18:17:48 |
| `Sistema de HSR by MC Filhos V1.2.docx` | 15 308 875 bytes | 06/10/2026 18:17:17 |
| `ficha-automatizada\Ficha Automatizada - Explorando Galáxias V1.2.xlsx` | 138 550 bytes | 06/10/2026 17:59:39 |
| `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx` | 535 049 bytes | 06/10/2026 18:00:59 |

Os V1.1 continuam no disco com a data original: `.pdf` 18 264 614 / 04/10 21:28:07, `.docx`
15 298 480 / 04/10 21:27:42, ficha 138 536 / 05/10 08:31:17, Mestre 535 024 / 05/10 19:41:55.

Os quatro achados conhecidos e não corrigidos da seção 3 continuam valendo, com a mesma recomendação.

---

## 12. Conferência de fechamento (07/10, madrugada)

**A revisão independente foi dispensada pelo autor.** Não houve passo de revisor nesta versão; as
correções das seções 1, 2 e 10 estão aprovadas por ele diretamente. Este fechamento é conferência, não
implementação nova: a única coisa que mudou no disco aqui foi um hash da linha de base (12.4) e os PNGs
de conferência (12.3).

### 12.1 Os quatro entregáveis, reconferidos no disco

Conferidos **depois** das três baterias desta rodada: tamanho e data idênticos aos da seção 5, ou seja
nenhuma bateria regerou entregável. Todos com data **posterior** à última correção do capítulo 11
(`livro-v1.0\11-caminho-recordacao.md`, 06/10 17:55:39).

| Arquivo | Tamanho | Data |
|---|---|---|
| `Sistema de HSR by MC Filhos V1.2.pdf` | 18 291 156 bytes | 06/10/2026 18:17:48 |
| `Sistema de HSR by MC Filhos V1.2.docx` | 15 308 875 bytes | 06/10/2026 18:17:17 |
| `ficha-automatizada\Ficha Automatizada - Explorando Galáxias V1.2.xlsx` | 138 550 bytes | 06/10/2026 17:59:39 |
| `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx` | 535 049 bytes | 06/10/2026 18:00:59 |

Os V1.1 continuam no disco com a data original: `.pdf` 18 264 614 / 04/10 21:28:07, `.docx`
15 298 480 / 04/10 21:27:42, ficha 138 536 / 05/10 08:31:17, Mestre 535 024 / 05/10 19:41:55.

**`versões antigas\`**: nada escrito — o arquivo mais novo da pasta é `HANDOFF-RETOMADA-v1.0.md`, de
05/10 09:52:03. **`Explorando Galáxias RPG - Players\`**: nenhum arquivo de conteúdo tocado — as três
cópias de `Explorando Galáxias RPG - Livro do Jogador V1.1.pdf` estão com 18 264 614 bytes (o tamanho
exato do PDF V1.1) e data de 05/10. O que aparece com data de 06/10 à noite nessa pasta são quatro
ponteiros do Google Drive de 195 bytes (`.gsheet` e `.gdoc`, 18:23 a 22:03), que são atalhos para
documentos que vivem na nuvem; nenhuma etapa desta tarefa gera arquivo `.gsheet` ou `.gdoc`, e nenhuma
escreveu ali. **Ressalva honesta:** não existe linha de base de hashes dessa pasta, então essas quatro
datas não podem ser provadas por hash — a conferência possível é a de tamanho e tipo, que fecha.

Correção de registro da seção 9: este passo **rodou** um `Get-ChildItem -Recurse` só de leitura em
`Explorando Galáxias RPG - Players\`, por pedido do autor, exatamente para poder afirmar o parágrafo
acima. Nenhum arquivo da pasta foi aberto, criado, alterado ou apagado.

### 12.2 As três baterias, rodada final

| Comando | Código de saída | Resultado |
|---|---|---|
| `python "build\testar_ficha.py" --suite tudo` | **0** | 11 de 11 suítes OK |
| `python "build\testar_mestre.py" --suite tudo` | **0** | 13 de 13 suítes OK, **7 214 190** checagens em 7 965 s |
| `scripts\verificar-livro-final.ps1` | **0** | 14 de 14 itens, 576 citações de capítulo com 0 quebrada |

```
ficha    spike 23 · protegidos 76 · dados 3294 · ouro 539 · oraculo 247 · extremos 2714
         lint 11922 · texto 1006673 · preview 278 · visual 24029 · google 4735     -> 0 falha(s)

mestre   spike 142 · protegidos 127 · dados 803 · bestiario 34 · ouro 130 · oraculo 604308
         determinismo 161479 · extremos 1029 · lint 149535 · texto 6252932 · preview 688
         visual 33714 · sabor 9269                                                 -> 0 falha(s)
```

Log das duas em `.agents\tasks\v12\suite-ficha-final.txt` e `suite-mestre-final.txt`. O
`verificar-livro-final.ps1` reconfirmou o DOCX V1.2 com 14,6 MB e mais novo que o `.md` mais recente,
3 688 parágrafos, 297 tabelas, 7 511 células, 0 tabela vazia, 18 imagens embutidas, glossário com 42 de
42 termos e as cinco faixas de combate reproduzindo as janelas publicadas.

### 12.3 A correção do capítulo 11 no PDF entregue, por amostragem

Quatro páginas do `Sistema de HSR by MC Filhos V1.2.pdf` renderizadas a 140 dpi em
`.agents\tasks\v12\paginas\` e **olhadas** uma por uma:

| PNG | O que confirma |
|---|---|
| `cap11-memoespirito-p099.png` | O parágrafo de 11.4 traz as **duas** escadas: "**1** dado nos níveis 1-4, **2** nos 5-8, **3** nos 9-12, **4** nos 13-16 e **5** nos 17-20 — e **2 / 3 / 4 / 5 / 6** nas mesmas faixas se a sua arma for de **Energia**". Logo abaixo, a frase sem pronome ambíguo: "A sua arma empresta ao Memoespírito quantos dados ele rola, nunca qual dado… o **tipo** é do **Memoespírito**, e é sempre **d6**" |
| `cap11-memoespirito-p100.png` | A linha do caso de Energia no exemplo de nível 17 (`6d6 + 5` ≈ **26**, "seis dados") e o quadro `O que mudou da v1.1` inteiro, explicando o dado a menos e a troca do pronome |
| `cap26-tabela-mestra-p180.png` | A tabela mestra de 26.2 com a coluna **Dados de Ataque Básico** em 1/1/1/1, 2/2/2/2, 3/3/3/3, 4 — a escada base de que 11.4 deriva |
| `cap26-tabela-mestra-p181.png` | O fim da tabela (4/4/4, 5/5/5/5) e a nota de "Como ler as colunas": "quantos dados a sua arma rola, partindo de 1. Uma arma de **Energia** começa em 2 e chega a **6** no nível 17" — a fonte canônica, idêntica ao que 11.4 agora diz |

Conferência por `openpyxl` nas duas planilhas entregues:

| Planilha | Célula | Conteúdo |
|---|---|---|
| Ficha V1.2 | `'Caminho'!B85` (`memo.n`) | `='Criação'!$D$16 + IF('Criação'!$Q$108="",0, IFERROR(VLOOKUP('Criação'!$Q$108,'Dados'!$A$457:$J$462,3,FALSE),1)-1) + IF(Forma Completa,1,0)` — a escada da tabela mestra **mais** o termo da categoria de arma |
| Ficha V1.2 | `'Dados'!A462:D462` | `Energia · 2d8 · 3ª coluna = 2 · face 8` → o termo acima soma **+1** só na Energia |
| Ficha V1.2 | `'Dados'!J258:J277` | `1,1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4, 5,5,5,5` — a escada base intacta. Nível 17 com Energia: 5 + 1 = **6** dados |
| Mestre V1.2 | `'Dados'!A439:E439` | `Energia · 2d8 · Longa · Sincronia · 2` — a tabela de 24.2 reproduzida com os 2 dados base |
| Mestre V1.2 | — | **Nada a conferir além disso**, e isso é o esperado: a Planilha do Mestre não modela Memoespírito nem a coluna de Dados de Ataque Básico de 26.2 (ela só traz de 26.2 a escada de Eficiência). Busca por `Memoesp`, `Dados de Ataque Básico` e `tabela mestra` no arquivo inteiro não devolve fórmula de dados do jogador |

### 12.4 Quarta regravação da linha de base (a única escrita deste passo)

A bateria da ficha desta rodada reescreveu `build\ficha_funcoes_ok.json` — ele grava `tempo_carga_s`,
`tempo_calculate_s` e `tempo_calculate_cenario_s`, então o SHA-256 muda em **toda** execução, como a
seção 8 já avisava. Com isso, a suíte `protegidos` da Mestre falhou na primeira tentativa
(`arquivo da ficha ALTERADO: build\ficha_funcoes_ok.json`, 1 falha em 127 checagens). Foi a única
vermelha da rodada, e a causa é de ordem, não de conteúdo.

O `diff` antes de regravar deu exatamente **1 alterado** (`ficha_funcoes_ok.json`) e **12 idênticos** —
inclusive o entregável `Ficha Automatizada - Explorando Galáxias V1.1.xlsx`, `gerar_ficha.py`,
`oraculo_ficha.py`, `testar_ficha.py`, `ficha_dados.py`, `ficha_mapa.json`, `ficha_protegidos.json`,
`renderizar_ficha.py`, `requirements-ficha.txt`, `AUDITORIA-DA-FICHA.md`, `COMO-USAR-NO-GOOGLE-PLANILHAS.md`
e `Ficha Exemplo - Nadir.xlsx` — mais a ausência conhecida de sempre, preservada com o hash antigo. Só
aquele hash foi trocado (`69bb1b36…` → `764711e8…`), gravado em UTF-8 **sem BOM** pela armadilha de 8.2.
A versão anterior está em `.agents\tasks\mestre\baseline-hashes-antes-fechamento-v12.json` (2 364 bytes).

Depois disso a bateria da Mestre fechou 13 de 13, e o `diff` final dos 14 arquivos deu **0 alterados, 13
idênticos e 1 ausente conhecido**: a Planilha do Mestre continua não escrevendo em nenhum arquivo da
ficha.

**Para a próxima rodada, a ordem obrigatória continua sendo:** gerar DOCX/PDF → refazer
`ficha_protegidos.json` → bateria da ficha → regravar `baseline-hashes.json` → bateria da Mestre. Rodar
fora dessa ordem faz `protegidos` falhar por construção, e não por defeito.

### 12.5 Achados conhecidos e não corrigidos

Não apareceu nada novo neste fechamento. Continuam valendo, sem mudança:

- os **quatro** da seção 3 (empunhadura de Peso de impacto, "efeito menor" de 16.5, os 2 dados base da
  Energia como trade declarado, e Dissimulada numa arma Leve);
- os **dois** da seção 11 (os atalhos `.gsheet` em V1.1, que só você pode republicar no Google, e o
  `AUDITORIA-DA-FICHA.md` datado da v1.1 de propósito);
- a fragilidade de ordem de 12.4, que é de processo e não de produto.

O que **não** foi verificado nesta rodada, declarado: o comportamento real das fórmulas **dentro do
Google Planilhas** (a suíte `google` compara contra um export de 04/10 da v1.1, congelado, com as quatro
divergências esperadas declaradas em tabela — ninguém reimportou o V1.2 no Google), e as quatro datas de
06/10 à noite dos ponteiros `.gsheet`/`.gdoc` em `Explorando Galáxias RPG - Players\`, que não têm linha
de base de hashes para comparar.
05/10 09:52:03. **`Explorando Galáxias RPG - Players\`**: nenhum arquivo de conteúdo tocado — as três
cópias de `Explorando Galáxias RPG - Livro do Jogador V1.1.pdf` estão com 18 264 614 bytes (o tamanho
exato do PDF V1.1) e data de 05/10. O que aparece com data de 06/10 à noite nessa pasta são quatro
ponteiros do Google Drive de 195 bytes (`.gsheet` e `.gdoc`, 18:23 a 22:03), que são atalhos para
documentos que vivem na nuvem; nenhuma etapa desta tarefa gera arquivo `.gsheet` ou `.gdoc`, e nenhuma
escreveu ali. **Ressalva honesta:** não existe linha de base de hashes dessa pasta, então essas quatro
datas não podem ser provadas por hash — a conferência possível é a de tamanho e tipo, que fecha.

Correção de registro da seção 9: este passo **rodou** um `Get-ChildItem -Recurse` só de leitura em
`Explorando Galáxias RPG - Players\`, por pedido do autor, exatamente para poder afirmar o parágrafo
acima. Nenhum arquivo da pasta foi aberto, criado, alterado ou apagado.

### 12.2 As três baterias, rodada final

| Comando | Código de saída | Resultado |
|---|---|---|
| `python "build\testar_ficha.py" --suite tudo` | **0** | 11 de 11 suítes OK |
| `python "build\testar_mestre.py" --suite tudo` | **0** | 13 de 13 suítes OK, **7 214 190** checagens em 7 965 s |
| `scripts\verificar-livro-final.ps1` | **0** | 14 de 14 itens, 576 citações de capítulo com 0 quebrada |

```
ficha       spike 23 · protegidos 76 · dados 3294 · ouro 539 · oraculo 247 · extremos 2714
            lint 11922 · texto 1006673 · preview 278 · visual 24029 · google 4735      → 0 falha(s)

mestre      spike 142 · protegidos 127 · dados 803 · bestiario 34 · ouro 130 · oraculo 604308
            determinismo 161479 · extremos 1029 · lint 149535 · texto 6252932 · preview 688
            visual 33714 · sabor 9269                                                  → 0 falha(s)
```

Log das duas em `.agents\tasks\v12\suite-ficha-final.txt` e `suite-mestre-final.txt`. O
`verificar-livro-final.ps1` reconfirmou o DOCX V1.2 com 14,6 MB e mais novo que o `.md` mais recente,
3 688 parágrafos, 297 tabelas, 7 511 células, 0 tabela vazia, 18 imagens embutidas, glossário com 42 de
42 termos e as cinco faixas de combate reproduzindo as janelas publicadas.

### 12.3 A correção do capítulo 11 no PDF entregue, por amostragem

Quatro páginas do `Sistema de HSR by MC Filhos V1.2.pdf` renderizadas a 140 dpi em
`.agents\tasks\v12\paginas\` e **olhadas** uma por uma:

| PNG | O que confirma |
|---|---|
| `cap11-memoespirito-p099.png` | O parágrafo de 11.4 traz as **duas** escadas: "**1** dado nos níveis 1-4, **2** nos 5-8, **3** nos 9-12, **4** nos 13-16 e **5** nos 17-20 — e **2 / 3 / 4 / 5 / 6** nas mesmas faixas se a sua arma for de **Energia**". Logo abaixo, a frase sem pronome ambíguo: "A sua arma empresta ao Memoespírito quantos dados ele rola, nunca qual dado… o **tipo** é do **Memoespírito**, e é sempre **d6**" |
| `cap11-memoespirito-p100.png` | A linha do caso de Energia no exemplo de nível 17 (`6d6 + 5` ≈ **26**, "seis dados") e o quadro `O que mudou da v1.1` inteiro, explicando o dado a menos e a troca do pronome |
| `cap26-tabela-mestra-p180.png` | A tabela mestra de 26.2 com a coluna **Dados de Ataque Básico** em 1/1/1/1, 2/2/2/2, 3/3/3/3, 4 — a escada base de que 11.4 deriva |
| `cap26-tabela-mestra-p181.png` | O fim da tabela (4/4/4, 5/5/5/5) e a nota de "Como ler as colunas": "quantos dados a sua arma rola, partindo de 1. Uma arma de **Energia** começa em 2 e chega a **6** no nível 17" — a fonte canônica, idêntica ao que 11.4 agora diz |

Conferência por `openpyxl` nas duas planilhas entregues:

| Planilha | Célula | Conteúdo |
|---|---|---|
| Ficha V1.2 | `'Caminho'!B85` (`memo.n`) | `='Criação'!$D$16 + IF('Criação'!$Q$108="",0, IFERROR(VLOOKUP('Criação'!$Q$108,'Dados'!$A$457:$J$462,3,FALSE),1)-1) + IF(Forma Completa,1,0)` — a escada da tabela mestra **mais** o termo da categoria de arma |
| Ficha V1.2 | `'Dados'!A462:D462` | `Energia · 2d8 · 3ª coluna = 2 · face 8` → o termo acima soma **+1** só na Energia |
| Ficha V1.2 | `'Dados'!J258:J277` | `1,1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4, 5,5,5,5` — a escada base intacta. Nível 17 com Energia: 5 + 1 = **6** dados |
| Mestre V1.2 | `'Dados'!A439:E439` | `Energia · 2d8 · Longa · Sincronia · 2` — a tabela de 24.2 reproduzida com os 2 dados base |
| Mestre V1.2 | — | **Nada a conferir além disso**, e isso é o esperado: a Planilha do Mestre não modela Memoespírito nem a coluna de Dados de Ataque Básico de 26.2 (ela só traz de 26.2 a escada de Eficiência). Busca por `Memoesp`, `Dados de Ataque Básico` e `tabela mestra` no arquivo inteiro não devolve fórmula de dados do jogador |

### 12.4 Quarta regravação da linha de base (a única escrita deste passo)

A bateria da ficha desta rodada reescreveu `build\ficha_funcoes_ok.json` — ele grava `tempo_carga_s`,
`tempo_calculate_s` e `tempo_calculate_cenario_s`, então o SHA-256 muda em **toda** execução, como a
seção 8 já avisava. Com isso, a suíte `protegidos` da Mestre falhou na primeira tentativa
(`arquivo da ficha ALTERADO: build\ficha_funcoes_ok.json`, 1 falha em 127 checagens). Foi a única
vermelha da rodada, e a causa é de ordem, não de conteúdo.

O `diff` antes de regravar deu exatamente **1 alterado** (`ficha_funcoes_ok.json`) e **12 idênticos** —
inclusive o entregável `Ficha Automatizada - Explorando Galáxias V1.1.xlsx`, `gerar_ficha.py`,
`oraculo_ficha.py`, `testar_ficha.py`, `ficha_dados.py`, `ficha_mapa.json`, `ficha_protegidos.json`,
`renderizar_ficha.py`, `requirements-ficha.txt`, `AUDITORIA-DA-FICHA.md`, `COMO-USAR-NO-GOOGLE-PLANILHAS.md`
e `Ficha Exemplo - Nadir.xlsx` — mais a ausência conhecida de sempre, preservada com o hash antigo. Só
aquele hash foi trocado (`69bb1b36…` → `764711e8…`), gravado em UTF-8 **sem BOM** pela armadilha de 8.2.
A versão anterior está em `.agents\tasks\mestre\baseline-hashes-antes-fechamento-v12.json` (2 364 bytes).

Depois disso a bateria da Mestre fechou 13 de 13, e o `diff` final dos 14 arquivos deu **0 alterados, 13
idênticos e 1 ausente conhecido**: a Planilha do Mestre continua não escrevendo em nenhum arquivo da
ficha.

**Para a próxima rodada, a ordem obrigatória continua sendo:** gerar DOCX/PDF → refazer
`ficha_protegidos.json` → bateria da ficha → regravar `baseline-hashes.json` → bateria da Mestre. Rodar
fora dessa ordem faz `protegidos` falhar por construção, e não por defeito.

### 12.5 Achados conhecidos e não corrigidos

Não apareceu nada novo neste fechamento. Continuam valendo, sem mudança:

- os **quatro** da seção 3 (empunhadura de Peso de impacto, "efeito menor" de 16.5, os 2 dados base da
  Energia como trade declarado, e Dissimulada numa arma Leve);
- os **dois** da seção 11 (os atalhos `.gsheet` em V1.1, que só você pode republicar no Google, e o
  `AUDITORIA-DA-FICHA.md` datado da v1.1 de propósito);
- a fragilidade de ordem de 12.4, que é de processo e não de produto.

O que **não** foi verificado nesta rodada, declarado: o comportamento real das fórmulas **dentro do
Google Planilhas** (a suíte `google` compara contra um export de 04/10 da v1.1, congelado, com as quatro
divergências esperadas declaradas em tabela — ninguém reimportou o V1.2 no Google), e as quatro datas de
06/10 à noite dos ponteiros `.gsheet`/`.gdoc` em `Explorando Galáxias RPG - Players\`, que não têm linha
de base de hashes para comparar.