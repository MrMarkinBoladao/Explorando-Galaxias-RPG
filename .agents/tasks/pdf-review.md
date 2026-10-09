# Revisão de visualização — PDF "Explorando Galáxias v1.0" (2ª rodada)

Os três achados bloqueantes da rodada anterior estão fechados, e conferi cada um
na página, não no relatório: o H2 "Vulpes" (pág. 47) já tem a arte da raça
embaixo dele em vez de 7,3 cm de vazio, as aberturas de Caminho fecham no pé da
moldura (págs. 58 e 72), e a conferência passou a medir e a publicar o vazio no
pé em vez de afirmar que não existe. O livro saiu de 255 para 250 páginas, e as
5 que sumiram são exatamente o espaço em branco que os consertos fecharam —
tabelas (295), imagens (17), marcadores (599) e entradas de sumário (266)
continuam iguais. O outline eu conferi por conta própria com pypdf: 599
marcadores em três níveis (33 H1 / 234 H2 / 332 H3), em ordem de página, com o
painel abrindo sozinho no leitor. O que sobra é de acabamento, e o item que mais
pesa é efeito colateral do próprio conserto: a figura agora encolhe para fechar
a página, então o tamanho da arte virou função da sobra, e a mesma classe de
imagem sai entre 6,3 cm e 11,7 cm ao longo do livro.

**Atenção:** tamanho da arte governado pela sobra da página — na pág. 72 o
símbolo decorativo sai com 11,8 cm e a arte do capítulo com 6,3 cm, hierarquia
invertida (*confirmado*); as fichas de preenchimento à mão saem sobre o fundo
cinza de bloco de código (*confirmado*); caixa de citação de 5 linhas se parte
entre as págs. 82 e 83 (*confirmado*). Os dois buracos que sobraram (págs. 238 e
240) foram medidos, o conserto pedido foi testado e **aumentava** o vazio — está
aceito como está (*confirmado, com os números*).

**Veredito**: APPROVED

## Visão geral

Os itens obrigatórios passam. Página de título com a capa `image11.png` em
403,2 × 403,2 pt (quadrada, sem distorção), nome, régua, subtítulo, "by MC
Filhos" e "Versão 1.0". Sumário de 8 páginas com número real em 266 entradas e
532 links internos; cruzei as entradas visíveis com a lista de páginas de
capítulo e batem (Raças → 44, Vulpes → 47, Caminhos → 52, Progressão → 169).
Cabeçalho corrido com o capítulo da própria página e folio nas 249 páginas de
conteúdo. Os 32 capítulos abrem em página nova. As 17 imagens do acervo são as
17 embutidas — nenhuma ficou de fora. Tipografia hierárquica e estável:
H1 23 pt com régua grossa, H2 15 pt com régua fina, H3 12 pt, corpo 10,5/14,6
justificado, citação com barra e fundo, mono em Consolas.

A tabela de 13 colunas do bestiário — o risco apontado na tarefa — cabe no
retrato a 7 pt com todos os dados em uma linha só. A de 12 colunas com as 15
fichas sai inteira numa página, e a mestra de progressão quebra entre as
págs. 169 e 170 repetindo o cabeçalho. 7 pt é o piso de conforto declarado no
gerador, e é o preço de não deitar a página: nenhuma das 295 precisou de
paisagem.

A estratégia de figura mudou: o bloco figura + legenda encolhe
proporcionalmente até caber no que resta da página, com piso de 50 % ou 6 cm de
altura. Foi isso que fechou os buracos, e o custo é que o tamanho da arte passou
a ser decidido pela sobra de espaço, não por uma regra de desenho — oito das 17
figuras encolheram, de 54,1 % a 95,2 %.

Os dois buracos restantes (12,3 cm na pág. 238 e 8,1 cm na 240) são as fichas em
arte ASCII de página inteira do capítulo 29. O conserto que a rodada anterior
pediu foi implementado, medido e recusado com número: o buraco ia de 12,3 para
15,1 cm e a ficha caía de 8 pt para 7,1 pt. A recusa está documentada e tem
chave de reversão (`TETO_DA_AMARRACAO`). Aceito.

Sobram dois itens de acabamento. As duas fichas de preenchimento (págs. 239 e
241) são impressas com o fundo e a barra lateral de bloco de código, embora o
texto da pág. 238 convide a fotocopiá-las e preenchê-las à mão. E a caixa de
citação que fecha a pág. 82 se parte no meio da frase, com o fundo recomeçando
na pág. 83.

Dois pontos do critério eu não consigo verificar sem refazer o build, e aceito
como reportado: os **0 avisos do ReportLab** sobre conteúdo largo demais (a
captura de `logging` + `warnings` está ligada durante a montagem) e as 289
tabelas que não vi rasterizadas, cobertas pela conferência automática de
conteúdo fora da moldura do coder. O conteúdo do livro não foi tocado: os 32
`.md` de `livro-v1.0/` têm data de 03/10 23:57 ou anterior, contra 04/10 01:59
do gerador e 02:00 do PDF.

<details>
<summary>Achados (3)</summary>

1. **Tamanho da arte governado pela sobra da página** — oito das 17 figuras
   encolheram, de 54,1 % a 95,2 %, então a mesma classe de imagem sai entre
   6,3 cm e 11,7 cm ao longo do livro (fator 1,85 entre duas artes de raça). Na
   pág. 72 a hierarquia inverte: o símbolo decorativo em 11,8 cm e a arte do
   capítulo em 6,3 cm. Dar a cada classe de figura uma altura-alvo declarada
   (símbolo e arte em ~8 cm) e deixar o encolhimento agir só numa faixa estreita
   em volta dela. **Não bloqueante.**
2. **Fichas de preenchimento com fundo de bloco de código** — as fichas das
   págs. 239 e 241 saem sobre o cinza claro com barra lateral indigo, e a pág.
   238 pede para fotocopiar e preencher à mão. Fundo branco com um fio de
   contorno imprime e preenche melhor; é um estilo à parte do bloco de código.
   **Não bloqueante.**
3. **Caixa de citação partida entre páginas** — a citação de 5 linhas que fecha
   a pág. 82 corta no meio da frase e o fundo recomeça na 83, quebrando a
   identidade da caixa. Uma reserva de espaço para citações curtas (até ~6
   linhas), como a que o bloco de código já usa, resolve com buraco de no
   máximo 2 cm. **Não bloqueante.**

</details>

<details>
<summary>Detalhes</summary>

### O que eu olhei

As 19 páginas rasterizadas desta rodada, uma por uma (`pdf-paginas/`): título,
sumário (2 e 3), raça com arte (47), aberturas de Caminho (58 e 72), ficha do
Caminho (59), citação no topo (28) e no pé (82), texto corrido (126), progressão
e continuação (169 e 170), abertura do bestiário (191), 13 colunas (193), 12
colunas (232), buracos (238 e 240), ficha ASCII (239) e a saída do teste de
paisagem. Mais a nota de verificação e as decisões de layout do gerador
(`GrupoDeFigura`, `amarrar_titulos_aos_blocos`, `escolher_layout_tabela`,
`montar_pagina_titulo`).

Os quatro `revisao-buraco-*.png` são da rodada anterior e retratam o PDF antigo;
não os usei como evidência do PDF de hoje.

Um spot-check só-leitura, sem rodar o gerador: pypdf no PDF para o que a imagem
não mostra — 250 páginas, metadados `Explorando Galáxias — Versão 1.0` /
`MC Filhos`, 599 marcadores distribuídos em 33 / 234 / 332 pelos três níveis,
nenhum fora de ordem de página, `/PageMode /UseOutlines`. E a contagem dos
arquivos de imagem do acervo: 17 arquivos, 17 embutidos.

### A arte encolhe para fechar a página, e o tamanho virou função da sobra

O conserto dos dois bloqueantes anteriores aparece na pág. 47 (arte da Vulpes a
55,9 % logo abaixo do H2) e na pág. 72 (arte da Harmonia a 54,1 %). O fator de
redução é calculado em `GrupoDeFigura.wrap` a partir da altura que sobrou na
coluna, e a altura que sobra depende de quanto texto veio antes:

```
figura        natural   saiu em    altura final
image9.png     6,64 cm   95,2%      6,32 cm   <- Destruição, pág. 58
image8.png    11,68 cm   54,1%      6,32 cm   <- Harmonia,   pág. 72
image3.png    11,68 cm   54,1%      6,32 cm
image15.png   11,68 cm   54,1%      6,32 cm
image14.png   11,68 cm   55,9%      6,53 cm   <- Vulpes,     pág. 47
image7.png    11,68 cm   63,0%      7,36 cm
image16.png   13,41 cm   62,1%      8,33 cm
image6.png    15,75 cm   72,8%     11,47 cm
(as outras 9, inclusive a capa, saem em 100%)
```

As sete artes de raça estão em páginas vizinhas (44 a 50) e são a mesma coisa:
um retrato vertical de 11,68 cm. Duas encolheram para 6,53 e 7,36 cm e as outras
saíram em 11,68 cm. Quem folheia o capítulo 05 vê o mesmo tipo de ilustração
variando por um fator de 1,85 sem razão visível na página.

O caso da pág. 72 é mais incômodo porque a hierarquia inverte. Medindo na
rasterização (1,601 px/pt):

```
moldura 25,1 cm  |  pág. 72 (Capítulo 09 — A Harmonia)
  H1 + régua ............ 1,2 cm
  símbolo da Harmonia .. 11,8 cm   100% — imagem decorativa, repetida nos 5 Caminhos
  legenda ............... 0,4 cm
  ficha do Aeon ......... 0,8 cm
  parágrafo ............. 3,0 cm
  ARTE DO CAPÍTULO ...... 6,3 cm   54,1% — a imagem que é o assunto da página
  legenda ............... 0,4 cm
```

O símbolo entra primeiro, leva 11,8 cm no tamanho cheio, e a arte fica com o
resto. Travar o símbolo em 8 cm libera 3,8 cm e deixa a arte ir a ~10 cm: as
duas figuras ficam equilibradas, a página continua cheia e a composição passa a
ser decidida por regra, não por sobra. As constantes para isso já existem
(`ESCALA_MINIMA_FIGURA`, `ALTURA_MINIMA_FIGURA`); falta uma altura-alvo por
classe de figura.

### Os dois buracos que sobraram

A aritmética fecha a discussão: a ficha de 71 linhas ocupa 25,0 cm dos 25,1 cm
da moldura em 8 pt, então nada pode acompanhá-la na página. Levar o H2 "29.8
Ficha de personagem" e o parágrafo de abertura para junto dela tira 2,8 cm de
uma página que já estava vazia e obriga a ficha a encolher para abrir espaço —
foi o que a medição mostrou. Daí o teto da amarração (`TETO_DA_AMARRACAO`, 85 %
da moldura): quando título + bloco pedem quase a página inteira, o título fica
onde está, apresentando a ficha na página anterior. É o menor dos dois vazios
possíveis, e a reversão é uma linha se o autor preferir o contrário.

Fora do meio de capítulo, a maior página em branco do livro é a 28: o capítulo
01 termina com uma caixa de citação e a frase "O Expresso Astral tem um assento
vazio. Senta.", e sobram 23,5 cm. A medição classifica como fim de capítulo, o
que é correto, e nenhum ajuste de apresentação fecha isso sem mexer no texto.

### Tabelas

Na de âncoras do bestiário (pág. 193) só os rótulos de coluna quebram em duas
linhas; os dados saem inteiros (`13 / 15 / 16`, `+1 / +2 / +3`, `1-2 / 3 / 4`) e
nada toca a margem. No teste de paisagem a coluna "RD C / E / B" agora imprime
`0 / 2 / 4` numa linha, em vez de partir o valor.

A ordem de tentativas de `escolher_layout_tabela` merece registro: retrato em
tamanho confortável, depois **paisagem** em tamanho confortável, e só então
retrato descendo até o piso de 6 pt. Uma tabela que caberia no retrato a 6,5 pt
vai para a página deitada em 7 pt. No livro de hoje isso não aparece (0 páginas
em paisagem), mas é a ordem que decide o caso quando aparecer.

### Fichas de preenchimento e caixa de citação partida

As fichas das págs. 239 e 241 são o único conteúdo do livro feito para ser
escrito, não lido: a pág. 238 diz "copie à mão, fotocopie ou transcreva num
caderno". Elas herdam o estilo de bloco de código — cinza claro de fundo e barra
indigo à esquerda — porque é assim que vêm do Markdown. O fundo cobre a A4
inteira, o que consome tinta na fotocópia e deixa a escrita a lápis com menos
contraste.

A citação que fecha a pág. 82 corta depois de "gasto numa linha de uma" e
recomeça na 83. O fundo para exatamente na moldura, longe do folio — o conserto
de rodadas anteriores continua valendo —, mas a caixa em si se parte; as
citações que ficam no meio ou no topo da página (28 e 126) saem inteiras.

</details>

<details>
<summary>Arquivos e evidências</summary>

| arquivo | o que é |
|---|---|
| `Sistema de HSR by MC Filhos V1.0.pdf` | o PDF desta rodada: 250 páginas, 17,41 MB |
| `build/gerar_pdf.py` | gerador; o que olhei: `GrupoDeFigura`, `amarrar_titulos_aos_blocos`, `escolher_layout_tabela`, `montar_pagina_titulo` |
| `.agents/tasks/pdf-verificacao.md` | nota do coder: comando, exit code 0, contagens, os seis achados anteriores um por um |
| `.agents/tasks/pdf-paginas/*.png` | 19 páginas desta rodada + 4 `revisao-buraco-*` da anterior (PDF antigo) |
| `livro-v1.0/*.md` | 32 capítulos, intocados (03/10 23:57 ou anterior, contra 04/10 02:00 do PDF) |
| `assets/imagens-v01/*.png` | 17 arquivos, 17 embutidos |

</details>
