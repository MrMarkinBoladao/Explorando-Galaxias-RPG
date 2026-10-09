# Verificação do PDF — Explorando Galáxias v1.0

Documento de conferência do gerador `build/gerar_pdf.py` e do PDF que ele produz.
Nenhuma linha do livro foi alterada: os 32 `.md` de `livro-v1.0/` continuam
intocados, e só a apresentação em PDF mudou.

> **Rodada desta nota.** Correção dos seis achados de
> `.agents/tasks/pdf-review.json` / `pdf-review.md` (veredito
> `CHANGES_REQUESTED`). Os três bloqueantes estão fechados; dos três não
> bloqueantes, dois estão fechados e um foi **medido e recusado** porque a
> mudança pedida aumentava o buraco em vez de fechá-lo (item 8.4 — está tudo
> explicado lá, com os números).

## 1. Comando e código de saída

| item | valor |
|---|---|
| comando de geração | `python "build\gerar_pdf.py"` (a partir da raiz do projeto) |
| exit code | **0** |
| comando de conferência | `python ".agents\tasks\verificar_pdf.py"` |
| exit code | **0** |
| teste do plano B de tabela larga | `python ".agents\tasks\teste_paisagem.py"` — exit code **0** |
| ambiente | Windows, Python 3.14.7, reportlab 4.4.4, pillow 12.1.0, pypdf 6.19.0, pymupdf 1.28.2 |
| fontes embutidas | Calibri (texto) + Consolas (monoespaçada), as duas TrueType do sistema |

## 2. O arquivo

| item | valor |
|---|---|
| caminho | `G:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\Sistema de HSR by MC Filhos V1.0.pdf` |
| tamanho | **17,41 MB** (18.251.188 bytes) |
| páginas | **250** (A4 retrato; moldura de texto com 2,2 cm nos lados e no pé, 2,4 cm no topo) |
| título/autor nos metadados | `Explorando Galáxias — Versão 1.0` / `MC Filhos` |
| capítulos montados | 32 arquivos `.md`, na ordem do prefixo numérico |
| tabelas | **295**, **0 em paisagem** |
| imagens | **17**, em 13 páginas (1, 44, 45, 46, 47, 48, 49, 50, 58, 65, 72, 78, 84 — quatro páginas levam duas) |
| marcadores (outline) | **599**, hierárquicos em **3 níveis** (H1 › H2 › H3), painel já aberto no leitor |
| sumário | páginas 2 a 9, **266 entradas**, todas com a página real |
| links internos | **532**, todos no sumário, **0 quebrados** |
| avisos do ReportLab | **0** (a captura de `logging` + `warnings` fica ligada durante a montagem) |

Eram 255 páginas na rodada anterior. As 5 que saíram são o espaço em branco que
os consertos do item 8 fecharam: nada de conteúdo foi retirado (as 295 tabelas,
as 17 imagens, os 599 marcadores e as 266 entradas de sumário continuam os
mesmos).

## 3. Conferências automáticas

| conferência | resultado |
|---|---|
| conteúdo fora da moldura de texto — texto **e** vetores, página por página | **nenhuma ocorrência** |
| imagens: caixa dentro da moldura e proporção igual à do arquivo de origem | **17 de 17 ok**, desvio de proporção máximo **0,01 %** |
| vazio no pé da página, separando fim de capítulo de meio de capítulo | **2 buracos no meio de capítulo** (ver item 4), 21 no fim de capítulo |
| página que termina com um título (título órfão) | **nenhuma das 250** |
| capítulo começando em página nova | **32 de 32** (mais a página 2, do sumário) |
| menor tamanho de fonte do livro | **6,4 pt** (código embutido numa célula de 7 pt); piso do gerador é 6 pt |
| links internos apontando para página existente | **532 de 532** |
| páginas quase vazias (quase nada impresso) | **nenhuma** |
| sumário com páginas reais | **266 entradas, 266 com a página certa, 0 divergentes** |
| marcadores apontando para o capítulo certo | amostra de 8 marcadores dos 3 níveis: **todos ok** |

Como a moldura é conferida: o limite é a moldura de texto **de verdade** (topo em
68,0 pt, lados e pé em 62,4 pt). Ficam fora da conta apenas o cabeçalho corrido
(régua a 1,74 cm do topo) e o número de página (1,25 cm do pé), que são
desenhados fora da área de texto de propósito. A folga é de **0,5 pt para
vetores** e de **1,0 pt para blocos de texto**, porque a caixa que o pymupdf
devolve para uma linha justificada inclui a sobra lateral do glifo.

## 4. Vazio no pé da página (a medição que faltava)

Esta é a conferência nova desta rodada, e é a que derrubou o relatório anterior:
a nota afirmava "páginas quase vazias: nenhuma" olhando só para páginas quase
**sem nada impresso**, quando o defeito real era outro — página com conteúdo
normal e um buraco grande no pé, no meio de um capítulo.

`verificar_pdf.py` agora mede, página por página, a distância entre o último
conteúdo (texto, vetor **ou** imagem) e o pé da moldura, e classifica:

- **fim de capítulo** — a página seguinte abre capítulo novo, ou é a última do
  livro. Capítulo acaba onde acaba: o vazio é normal.
- **meio de capítulo** — a página seguinte continua o mesmo capítulo. Vazio
  grande aqui é defeito de paginação.

O limite é 5 cm (cerca de um quinto da moldura).

```
antes (PDF revisado, 255 pag.)        agora (250 pag.)
  no MEIO de capitulo: 7 paginas        no MEIO de capitulo: 2 paginas
    pag.  47:  7,3 cm (titulo orfao)      pag. 238: 12,3 cm
    pag.  51: 13,0 cm (titulo orfao)      pag. 240:  8,1 cm
    pag.  60:  7,0 cm
    pag.  74:  7,0 cm                   no FIM de capitulo: 21 paginas
    pag.  81:  7,0 cm                     (11, 23, 28, 33, 43, 57, 64, 71,
    pag.  88:  7,0 cm                      83, 93, 103, 108, 125, 133, 139,
    pag. 243: 12,3 cm                      149, 154, 168, 190, 243, 250)
  titulos orfaos: 2                     titulos orfaos: 0
```

Os dois que sobraram são a mesma coisa, e são estruturais: as **fichas em arte
ASCII do capítulo 29**, que ocupam uma página inteira e não podem ser partidas
nem reduzidas sem deixar de servir para preencher à mão. A página 238 apresenta
a ficha de personagem, que sai inteira em 8 pt na 239; a 240 fecha com a ficha
do Memoespírito, e a ficha seguinte (29.10), com o título dela, vai inteira para
a 241. O item 8.4 mostra por que mover o título para a página da ficha — o
conserto pedido pelo revisor — **aumentaria** o buraco de 12,3 para 15,1 cm.

## 5. Inspeção visual (páginas rasterizadas)

As páginas estão em `.agents/tasks/pdf-paginas/`, renderizadas a 1,6×
(953×1348 px). Os quatro `revisao-buraco-*.png` são do revisor e retratam o PDF
da rodada **anterior**; ficaram na pasta para comparação.

| arquivo | página | o que eu olhei |
|---|---|---|
| `titulo.png` | 1 | Capa `image11.png` centrada, quadrada, sem distorção (1679×1679 px → 403,2×403,2 pt), com título, régua, subtítulo, "by MC Filhos" e "Versão 1.0" equilibrados na vertical. Sem cabeçalho e, agora, **sem folio** (achado 6). |
| `sumario.png` | 2 | Sumário com **números de página reais** (10, 11, 12, 13, 17, 20, 22, 24…), pontinhos de condução, capítulos em negrito/indigo e seções recuadas. Cabeçalho "Explorando Galáxias / Sumário", folio "2". |
| `sumario-2.png` | 3 | Continuação do sumário: mesmo padrão, sem corte nem sobreposição. |
| `raca-titulo-com-arte.png` | 47 | **O achado 1 fechado.** O H2 "Vulpes" já não é a última coisa da página: a arte da raça vem logo abaixo dele, reduzida a 55,9 % (6,5 cm), e a página fecha no pé da moldura. Antes o título ficava sozinho com 7,3 cm de vazio e a arte caía na página seguinte. |
| `caminho-abertura.png` | 58 | **O achado 2 fechado (caso fácil).** Abertura do capítulo 07: H1, símbolo da Destruição no tamanho cheio, ficha do Aeon, parágrafo e a arte do Caminho a 95,2 % — tudo na mesma página, sem o buraco de 7,0 cm. |
| `caminho-abertura-2.png` | 72 | **O achado 2 fechado (caso difícil).** Abertura do capítulo 09: o símbolo da Harmonia é quadrado e ocupa 11,7 cm, então a arte do Caminho (também quadrada) entrou a 54,1 % (6,3 cm). Página cheia, arte sem distorção, legenda no lugar. |
| `caminho-ficha.png` | 59 | Ficha do Caminho: tabela de duas colunas sem faixa de cabeçalho (o Markdown traz cabeçalho vazio), citação com barra lateral e fundo, H2 com régua fina, texto justificado. |
| `tabela-bestiario-13-colunas.png` | 193 | A tabela de âncoras do bestiário, **13 colunas**, em 7 pt no retrato: cada célula de dados numa linha só (`13 / 15 / 16`, `+1 / +2 / +3`, `1-2 / 3 / 4`), só os títulos de coluna quebram em 2 linhas. A regra nova de célula numérica (achado 5) **não** custou tamanho de fonte aqui. |
| `tabela-fichas-12-colunas.png` | 232 | As 15 fichas de inimigo (**12 colunas × 15 linhas**) inteiras numa página, sem quebra de linha em nenhuma célula, mais a tabela de Ciclos do combate A embaixo. |
| `tabela-progressao.png` | 169 | Abertura do capítulo 26 em página nova + a tabela mestra de progressão (**10 colunas**) começando legível em 8 pt. |
| `tabela-progressao-continuacao.png` | 170 | A mesma tabela continuando na página seguinte **com a linha de cabeçalho repetida** (`repeatRows=1`), e as setas `→` em Unicode de verdade. |
| `texto.png` | 126 | Texto corrido (capítulo 18): hierarquia H1/H2/H3 clara, parágrafos justificados, negrito e itálico, listas recuadas, citações em caixa, tabela de 3 colunas. A citação de dois parágrafos continua formando **um bloco contínuo**. |
| `ficha-ascii.png` | 239 | A ficha de personagem em arte ASCII (71 linhas) **inteira numa página, ainda em 8 pt**, alinhamento das colunas de preenchimento preservado, fundo e barra lateral. |
| `bestiario-abertura.png` | 191 | Abertura do capítulo 28: lista numerada com os números do Markdown, citação, tabela dos campos da ficha e bloco de código do formato de ficha. |
| `citacao-no-topo-da-pagina.png` | 28 | Caso de borda: citação como **primeiro** elemento da página. O fundo começa exatamente na moldura, abaixo da régua do cabeçalho. |
| `citacao-no-pe-da-pagina.png` | 82 | Caso de borda: citação que **fecha** a página e continua na seguinte. O fundo para exatamente na moldura, longe do folio. |
| `buraco-1-p238.png` | 238 | O buraco que sobrou: a ficha de personagem (página inteira) não cabe nos 12,3 cm que restaram depois da seção 29.7. Ver item 8.4. |
| `buraco-2-p240.png` | 240 | O outro: a ficha do Memoespírito fecha a página e a ficha seguinte, com o título dela, vai inteira para a página 241. |
| `paisagem-fallback.png` | — | Saída do `teste_paisagem.py`: a tabela de 13 colunas na página deitada, agora **sem valor partido** (ver achado 5). |

Em todas elas: texto sem corte, tabelas dentro da margem, imagens sem
esticamento, cabeçalho corrido com o nome do capítulo e folio no pé.

## 6. Como as figuras passaram a caber

Cada figura é um bloco único (`GrupoDeFigura`): figura + legenda, que nunca se
separam. A diferença desta rodada é que o bloco **encolhe** quando é isso que
falta para ele não pular de página:

1. se o bloco cabe no que resta da página, sai no tamanho cheio;
2. se não cabe, a figura é reduzida **proporcionalmente** (largura e altura pelo
   mesmo fator: nunca distorce) até preencher exatamente o espaço que restou;
3. a redução tem dois limites, e vale o mais apertado: **nunca menos de 50 % do
   tamanho natural** e **nunca menos de 6 cm de altura**. O segundo protege as
   figuras pequenas — uma arte de 4 cm não encolhe, ela pula de página, e o
   buraco que ela deixaria seria pequeno de qualquer jeito;
4. se nem com a redução couber, o bloco inteiro vai para a página seguinte e lá
   a figura sai cheia.

As duas constantes são `ESCALA_MINIMA_FIGURA` e `ALTURA_MINIMA_FIGURA`, no topo
de `build/gerar_pdf.py`. Subir a primeira preserva o tamanho da arte e aceita
mais buraco; baixá-la fecha mais buraco e aceita arte menor.

O gerador imprime, no fim da montagem, toda figura que chegou ao pé de uma
página. Nesta montagem foram 8 das 17, todas acomodadas:

```
image14.png  natural 11,68 cm  pedida 55,9%  piso 51,4%  encolheu
image16.png  natural 13,41 cm  pedida 62,1%  piso 50,0%  encolheu
image7.png   natural 11,68 cm  pedida 63,0%  piso 51,4%  encolheu
image6.png   natural 15,75 cm  pedida 72,8%  piso 50,0%  encolheu
image9.png   natural  6,64 cm  pedida 95,2%  piso 90,4%  encolheu
image8.png   natural 11,68 cm  pedida 54,1%  piso 51,4%  encolheu
image3.png   natural 11,68 cm  pedida 54,1%  piso 51,4%  encolheu
image15.png  natural 11,68 cm  pedida 54,1%  piso 51,4%  encolheu
```

A capa e as outras 8 figuras saem em 100 %.

## 7. Estratégia das tabelas largas (e por que nenhuma página saiu deitada)

A escolha está documentada em `escolher_layout_tabela`:

1. a fonte da tabela começa entre 9 pt (até 4 colunas) e 7 pt (11 colunas ou mais);
2. se a soma das larguras mínimas não couber na faixa útil, a fonte desce de
   meio em meio ponto, com **piso de 6 pt**;
3. se não couber no retrato com pelo menos 7 pt, a tabela sai sozinha numa
   **página em paisagem** e o texto volta ao retrato na página seguinte —
   preferi isso a partir a tabela em blocos de colunas porque a tabela de
   âncoras só se lê inteira (cada linha é um orçamento completo de inimigo);
4. a repartição da largura entre as colunas é **max-min** (nível de água): a
   coluna que quer pouco recebe exatamente o que quer, e só a coluna de texto
   comprido aperta;
5. **novo nesta rodada:** célula que é só número com separadores
   (`13 / 15 / 16`, `+1 / +2 / +3`, `0 / 2 / 4`) conta como **uma palavra** no
   cálculo da largura mínima, até 20 caracteres. Número partido em duas linhas
   não se lê, e o espaço ganho apertando essa coluna não compensa;
6. há uma trava final que reescala as larguras se a soma passar da faixa útil.

Resultado no livro v1.0: **todas as 295 tabelas couberam no retrato** com 7 pt ou
mais. Nenhuma página deitada foi necessária (`em paisagem: 0`), e o caminho de
paisagem continua testado à parte por `teste_paisagem.py`, que aperta o piso de
fonte para forçar o caso: 3 páginas — retrato, paisagem (842×595) com a tabela
entre x=56,7 e x=785,2 (margem em 56,7 e 785,3), retrato de novo.

## 8. Os seis achados do revisor, um por um

### 8.1 Título H2 órfão no pé da página — **bloqueante, fechado**

A reserva fixa de 3 cm antes de um H2 (`CondPageBreak(3.0 * cm)`) bastava para
um título seguido de parágrafo, mas não para um título seguido de arte: o título
passava no teste dos 3 cm e era impresso, a figura pedia 12 a 16 cm, não cabia e
pulava de página. Sobrava o título sozinho no pé ("Vulpes", pág. 47;
"Intellitron", pág. 51).

O conserto é `amarrar_titulos_aos_blocos`, uma passada que roda **depois** de o
livro inteiro estar montado e troca a reserva fixa pela altura **medida** do que
precisa ficar junto do título:

- título + figura → título + a figura no menor tamanho que ela aceita. Se isso
  couber, o título é impresso e a própria figura encolhe para fechar o espaço;
  se não couber, título e figura vão juntos para a página seguinte;
- título + parágrafo de abertura + bloco de código → os três juntos;
- título + parágrafo → título + as duas primeiras linhas do parágrafo (o mínimo
  contra órfão, nunca menor que a reserva de antes);
- título + tabela → a reserva mínima de sempre, porque tabela se parte entre
  páginas repetindo o cabeçalho; forçar quebra ali abriria buraco em vez de
  fechar.

275 dos 566 títulos de seção (234 H2 + 332 H3) ganharam reserva maior que a
fixa. A conferência passou a medir isso direto: `titulos_orfaos` olha o último
trecho impresso de cada página e acusa se ele é um título (negrito de 12 pt ou
mais). Resultado: **nenhuma das 250 páginas termina com um título.**

### 8.2 Buraco de 7,0 cm nas quatro aberturas de Caminho — **bloqueante, fechado**

A medida do revisor ("perde por poucos milímetros") valia para o capítulo 07, em
que a arte é larga e baixa (6,64 cm): ela entrou na página com 95,2 %. Nos
capítulos 09, 10 e 11 a conta é outra — símbolo **e** arte são quadrados de
11,68 cm, e a página de abertura ainda leva H1, ficha do Aeon e parágrafo. Ali a
arte precisava de 54,1 %, não de 95 %.

Por isso o conserto não foi afrouxar a legenda nem o espaçador (ganharia 0,5 cm,
e faltavam 5), mas dar à figura a capacidade de encolher proporcionalmente
dentro de limites declarados (item 6). As quatro aberturas de Caminho fecharam:
páginas 58, 72, 78 e 84, cada uma com símbolo e arte juntas e o pé da moldura
preenchido.

### 8.3 A conferência não detectava página quase vazia — **bloqueante, fechado**

`verificar_pdf.py` ganhou `vazio_no_pe` e `buracos_no_meio` (item 4): medição do
vazio no pé contra a moldura de texto real, com classificação entre fim de
capítulo e meio de capítulo, e rasterização automática das páginas com buraco
(`buraco-N-pNNN.png`). O relatório não volta a afirmar o contrário do que as
páginas mostram: ele diz, com número, que **sobraram dois buracos**, onde e por
quê.

### 8.4 Buraco de 12,3 cm na pág. 243 — **não bloqueante, medido e recusado**

O conserto pedido foi "mover título e parágrafo para a página da ficha". Eu
implementei exatamente isso e **medi o resultado: o buraco cresceu de 12,3 cm
para 15,1 cm**, e a ficha teve de cair de 8 pt para 7,1 pt.

A razão é que o buraco não é causado pelo título. Ele está na página **anterior**
à ficha, e existe porque a seção 29.7 acaba ali e a ficha de personagem (71
linhas de arte ASCII) precisa de uma página inteira — 25,0 cm dos 25,1 cm da
moldura. Mover o título e o parágrafo de abertura para a página da ficha tira
2,8 cm de conteúdo da página que já estava vazia e obriga a ficha a encolher
para abrir espaço para eles. Fechar o buraco de verdade exigiria a ficha em
3,8 pt, que não serve para preencher à mão.

Então a amarração ganhou um teto (`TETO_DA_AMARRACAO`, 85 % da moldura): quando o
conjunto título + bloco pede quase a página inteira, o título fica onde está, e
o bloco começa em página nova. O resultado é o menor dos dois buracos possíveis,
com o título apresentando a ficha na página de antes. Se o autor preferir o
contrário (ficha em 7,1 pt e título na mesma página dela), é uma linha: subir
`TETO_DA_AMARRACAO` para 1,0.

### 8.5 Plano B de paisagem partia valor no meio — **não bloqueante, fechado**

`_medir_colunas` passou a tratar célula numérica como palavra única (item 7,
passo 5). Na saída do `teste_paisagem.py` a coluna "RD C / E / B" agora imprime
`0 / 2 / 4` e `0 / 4 / 8` numa linha só — antes saía `0 / 2 /` + `4`. As 295
tabelas do livro continuam cabendo no retrato, e a de 13 colunas continua em
7 pt (a regra nova não custou tamanho de fonte).

### 8.6 Folio na página de título — **não bloqueante, fechado**

A página 1 não imprime mais o número debaixo da capa, que é a convenção de
livro. Ela continua contando na sequência: a página 2 imprime "2", e as outras
249 seguem numeradas. A decisão é uma constante no topo do gerador,
`FOLIO_NA_PAGINA_DE_TITULO = False` — troque para `True` e o folio volta.

## 9. Defeitos das rodadas anteriores (continuam fechados)

1. **O fundo da citação saía da moldura de texto.** `folgas_de_decoracao` corta a
   folga de 5 pt no espaço que realmente existe entre o parágrafo e a moldura.
   Conferido de novo nesta rodada: 0 ocorrências de vetor fora da moldura, com
   folga de 0,5 pt.
2. **O fundo do bloco de código passava 1 pt da margem direita.** O limite da
   direita é preso na largura do flowable.
3. **Capítulo não começava em página nova.** A montagem usa uma lista única do
   livro inteiro; a quebra sai antes de todo H1 — as 32 aberturas de capítulo
   estão nas páginas 10, 12, 24, 29, 34, 40, 44, 52, 58, 65, 72, 78, 84, 94, 99,
   104, 109, 114, 122, 126, 134, 140, 145, 150, 155, 159, 164, 169, 175, 191,
   224 e 244 (mais a página 2, do sumário).
4. **Sumário aparentemente deslocado em 1 página.** Era falso positivo do script
   de conferência, que agora lê o número do sumário por coordenada: 266 de 266
   batem.

## 10. Como o autor regera o PDF

```powershell
cd "G:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG"
python "build\gerar_pdf.py"
```

O PDF é refeito por inteiro, sobrescrevendo o anterior — o mesmo fluxo do
`build\gerar_docx.py`. Se o arquivo estiver aberto num leitor de PDF, o script
avisa para fechar e rodar de novo em vez de estourar um erro de permissão.

Para reconferir tudo e regravar as páginas rasterizadas:

```powershell
python ".agents\tasks\verificar_pdf.py"
python ".agents\tasks\teste_paisagem.py"
```
