# Auditoria da Ficha Automatizada · Explorando Galáxias v1.1

**Arquivos auditados:** `Ficha Automatizada - Explorando Galáxias V1.1.xlsx` (modelo em branco) e `Ficha Exemplo - Nadir.xlsx` (o mesmo modelo com a Nadir do capítulo 29.7). São 10 abas, níveis 1 a 20, para importar no Google Planilhas. Sem macro e sem script: só fórmula.

> **Revisão 2 (05/10):** a ficha quebrava no Google Planilhas real. Causa, correção e testes novos estão na seção 11. Onde este relatório diz "nenhuma fórmula dá erro" ou "0 erros", isso valia **só no motor local** (`formulas`), que não reproduzia o jeito como o Google lê o que se digita.

**Veredito:** as 10 suítes de teste saem OK (a nova suíte `visual` incluída) e a bateria completa termina com código de saída **0**. Planilha e oráculo independente concordam em todos os casos (0 divergência), nenhuma fórmula dá erro no motor local (veja a seção 11 para o Google), a revisão de texto não achou nada e todo texto cabe na própria célula nos 4 estados medidos. A aba Em Jogo cabe numa tela de 1360 × 768. O livro não foi alterado pela ficha. Os ajustes que você pediu depois da v1.1 estão na seção 8.

A ficha é gerada por `build\gerar_ficha.py` e auditada por `build\testar_ficha.py`. A saída completa da rodada final está em `.agents\tasks\suite-tudo-v11.txt`.

---

## 1. Resultado de cada suíte (rodada final, v1.1)

| Suíte | Resultado | O que os números dizem |
|---|---|---|
| spike | OK · 14 checagens · 0 falha | 33 funções liberadas + `&`; acento em nome de aba funciona |
| protegidos | OK · 76 · 0 | 38 arquivos do livro v1.1 (os `.md`, `.docx`/`.pdf` V1.1 e os geradores do livro) com o mesmo SHA-256: a ficha não mexeu no livro |
| dados | OK · 3297 · 0 | 49 blocos e 32 listas da aba Dados conferidos célula a célula contra o livro; 51 âncoras; 108 Bênçãos |
| ouro | OK · 533 · 0 | Nadir de 29.7 e as fichas de 29.8/29.9 (78 campos, 230 células); a Ficha Exemplo tem as 2363 fórmulas iguais ao modelo e 0 aviso |
| oraculo | OK · 247 · 0 | 247 casos (126 da matriz, 60 da varredura 1→20 em 3 personagens, 61 casos-limite); **43 712 saídas comparadas, 0 divergência**; 234 códigos de aviso conferidos nos dois sentidos |
| extremos | OK · 858 · 0 | todas as 2363 fórmulas calculadas em 765 cenários (657 deles mudando um campo por vez, com valor válido e inválido); 0 `#N/A`, `#VALUE!`, `#REF!` etc.; cada valor inválido acende um aviso em PT-BR |
| lint | OK · 6204 · 0 | 2363 fórmulas, 299 validações e 196 formatações condicionais compatíveis com o Google Planilhas; nenhuma aba com painel congelado ou dividido; "Resumo para o Mestre" não aparece em lugar nenhum do arquivo |
| texto | OK · 975 083 · 0 | 7415 trechos visíveis; termos proibidos e aposentados; grafia do glossário (97 termos); ortografia contra o léxico do livro; acentuação |
| preview | OK · 278 · 0 | 40 imagens de aba + 344 recortes em tamanho real nos 4 estados (em branco, Nadir nível 1, nível 20 completo e pior caso); 0 texto cortado; Em Jogo com 1360 × 760 px |
| visual | OK · 23 898 · 0 | 22 521 textos medidos nos 4 estados, todos cabendo na própria célula; 196 listas com espaço para a seta; 552 textos buscados na aba Dados e 185 avisos medidos pela mensagem mais longa possível; 55 tabelas a até 15 linhas do cabeçalho; 9 abas em até 1360 px (seção 8) |

Comparação com a auditoria anterior (contra o livro v1.0): ouro passou de 466 para 533 checagens e o oráculo de 245 para 247 casos (43 391 → 43 712 saídas), porque as correções da v1.1 ganharam casos próprios.

## 2. Como cada parte foi verificada

- **Oráculo independente** (`build\oraculo_ficha.py`): as regras de personagem reescritas em Python direto do livro, sem ler nenhuma fórmula da planilha. A planilha é calculada pela biblioteca `formulas` com as mesmas entradas, e cada saída é comparada: atributos e bônus, Eficiência e Eficácia, PV, Defesa, Esquiva, RD, Velocidade, DT, as 18 Perícias, os 6 Testes de Resistência, Morrendo (com Vantagem), Ataque Básico, Habilidades, Ultimate, slots de Bênção, Cone de Luz, Relíquias, Conjuntos, inventário, Barreira e Memoespírito. Um aviso que aparece só num dos lados também conta como divergência.
- **Casos-limite** (61): Humano com +1/+1, atributos 3 e 25, nível 0 e 21, mesa de 0 a 7 jogadores, Compra de Pontos acima de 28, Perícias a mais, Armadura Pesada, Habilidade de Nível 9, Ressonância III repetida, Bênção de outro Caminho ou acima do slot, Cone acima da faixa, Sobreposições a mais, Conjuntos 2+2+2, inventário acima da capacidade, Memoespírito inválido de 6 formas, nível 20 com tudo no máximo e outros.
- **Extremos:** ficha em branco, só nome, cada Raça, cada Caminho, um campo por vez com valor válido e inválido (texto em campo numérico, nível "abc", Bênção colada à mão…). Meta cumprida no motor local: nenhum valor de erro, e o aviso aparece na célula certa. (Até a revisão 2, nenhum cenário punha um valor de erro numa entrada, que é o que o Google faz com um texto começando por `+`: seção 11.)
- **Lint:** fórmulas em inglês com vírgula, só funções da lista branca, arredondamento com `INT`, sem `INDIRECT`, sem `_xlfn`, sem referência a outra aba em formatação condicional ou validação personalizada, só Arial, sem macro.
- **Texto:** termos proibidos de `scripts\checar-nomenclatura.ps1` e os aposentados de 30.2, grafia exata do glossário 30.1, ortografia contra as palavras do próprio livro e acentos. Duas grafias fora do glossário ficam aceitas porque são citação literal do livro: "Bônus de atributo" (`Dados!B6`) e "dano contínuo" (`Dados!C377`).
- **Preview:** cada aba é desenhada em PNG com larguras, alturas, mesclas, cores e fonte da planilha, e cada texto é medido para ver se cabe na célula. Os recortes ficam em `.agents\tasks\ficha-preview\` (lista em `indice-recortes.txt`).

## 3. Bugs encontrados e corrigidos

### 3.1 Nesta atualização para a v1.1

| Onde | Antes | Depois |
|---|---|---|
| Ataque Básico (Equipamento e Em Jogo) | Duas leituras lado a lado: "como no livro" (`1d12 + 4`, média 10) e "pela regra" (`1d12 + 6`, média 12) | Uma só, a da regra: Nadir com `1d12 + 6`, média 12, com colunas "Do atributo" (+4) e "Equipamento" (+2 de Mãos I). Segue D1 |
| Em Jogo, cabeçalho `G15` | "Do equipamento" quebrava em duas linhas e ficava cortado nos 3 estados (achado da suíte preview na v1.1) | "Equipamento", que cabe na coluna. Nenhuma largura mudou, para não estourar a tela |
| Cone de Luz, Sobreposição | +1 e +10 PV por cópia, com tetos separados de +3 e +50 PV | +1 e +10 PV por cópia; o PV para junto com o numérico: até +30 PV nos Níveis 1 e 2, +35 PV nos 3 e 4. Segue D5 |
| Teste de Morrendo | Vantagem para Vulpes e Avginiano era dedução da ficha (05 + 22.1) | Lida do quadro novo de 23.5, que nomeia Xianzhouíta, Vulpes e Avginiano. Segue D3 |
| Condições do personagem (Em Jogo) | Congelado aparecia na lista | Saiu: só existe em inimigo. Segue D6 |
| Caminho, recurso próprio | Inexistência, Harmonia e Abundância mostravam "Sem recurso próprio declarado (D2)" | Os nove Caminhos mostram a linha "Recurso próprio" do livro (para esses três: os acúmulos de Marca do Vazio e Corrupção, Eco da Vitória e Florescimento). Segue D2 |
| Armadura Pesada | Texto lido de "-2 em Testes e Perícias de Agilidade" | Lido da nova frase de 24.1: -2 em Reflexos e nas Perícias de Agilidade, nunca no Teste de Ataque. Segue D4 |
| Reescrita de Habilidade no 16 | Intervalo deduzido de 16.6 | Lido da célula nova de 26.2 ("do 16 ao 20"). Segue N1 |
| DT típica do inimigo | Conferida nos níveis 3, 8, 11, 14 e 19 | Conferida nos níveis de referência 3, 7, 11, 15 e 19 do livro (mesmos 15/17/18/19/21). Segue N4 |
| Arquivos | Um `.xlsx` "v1.0" na raiz do projeto | Os entregáveis ficam em `ficha-automatizada\`, com nome V1.1 e uma Ficha Exemplo da Nadir |

### 3.2 Na auditoria anterior (FEAT-004), mantidos

- **Diferencial planilha × oráculo:** seis diferenças, todas decididas pelo livro. Em todas o errado era o oráculo, e ele foi corrigido citando a seção: bônus do Cone em "um Teste de Resistência ou uma Perícia" (25.2); Conjunto "+1 em um tipo de rolagem" (25.3); Conjuntos sem passar de +3 numa mesma rolagem (25.3); Ressonância III só para uma Habilidade (26.7); item com quantidade 0 não ocupa Espaço (24.4); rótulo de acúmulo de Bênção de outro Caminho tratado como texto.
- **Layout:** títulos de bloco curtos da aba Dados com o fim em branco sobre branco passaram a ter a faixa azul estendida; rótulos centrados na vertical (antes ficavam no rodapé das linhas altas); caixas de Morrendo da Em Jogo ganharam legenda "↑ sucessos (0 a 3)" e "↑ falhas (0 a 3)"; Tipo, Em área? e Resolução da Ultimate mesclados para "Teste de Resistência" caber na caixa; números da Criação e da Progressão centrados com o cabeçalho; Regras Rápidas sem "21" encostado em "5d8".

### 3.3 Erros de digitação e de texto

- A suíte `texto` termina com 0 achado: nenhuma palavra fora do léxico do livro, nenhum termo proibido ou aposentado, nenhuma forma sem acento ("Criacao", "Pericia", "Bencao"…), e os termos oficiais com a grafia do glossário.
- Saíram da Início e das Regras Rápidas as marcas "(decisão 4)", "(decisão 5)" e "(decisão 9)", que eram número interno do plano e não diziam nada ao jogador.
- Na v1.1, os códigos internos "(D1)", "(D2)" e "(D5)" saíram da planilha. A busca no modelo final não acha nenhum código Dn ou Nn em texto visível.
- Toda menção de versão na planilha diz **v1.1** (títulos das abas e Início). As únicas outras versões que aparecem são conteúdo do livro: a coluna "Nova da v1.0" das Bênçãos (`Dados!H118`, marca do próprio livro) e "Modelo da v0.1" (`Dados!A567` e `A574`).

## 4. As 12 decisões de projeto

1. Condições entram nos números só quando o efeito é inequívoco (Lentidão, Silenciado, Controlado, Surpreso, Morrendo com PV 0, sobrecarga). Danos Contínuos e o resto ficam como texto, com o tique estimado.
2. Bênçãos de efeito fixo entram nos números (Corpo Imortal, Pele de Pedra, Olho de Lan, Avatares, Instinto, Memória Compartilhada etc.). Temporários sempre limitados ao teto da faixa, com aviso.
3. As tabelas vêm dos `.md` do livro por um leitor automático, mais dados transcritos com âncora literal. A suíte `dados` confere tudo.
4. Sem rolador de dados: a ficha entrega a rolagem pronta (`d20+6`, `1d12+6`).
5. PV atual é digitado, e a Em Jogo tem uma calculadora de dano (RD, exceto Dano Contínuo → mínimo 1 → temporário → PV).
6. Sem nomes definidos na planilha; o mapa das células fica em `build\ficha_mapa.json`.
7. Arredondamento só com `INT`.
8. Valor fora da faixa gera aviso em PT-BR e a conta segue com o valor limitado. Nunca dá erro.
9. PV rolado (variante de 06.4) não é calculado; a regra está nas Regras Rápidas.
10. Listas que dependem de outra escolha usam `INDEX/MATCH` em colunas auxiliares cinzas na própria aba.
11. A validação avisa, mas não bloqueia; a regra fica na coluna de aviso.
12. Nenhuma informação se digita em dois lugares (arma principal e armadura na Criação, espelhadas na Equipamento).

## 5. Inconsistências do livro — corrigidas na v1.1

Todas vieram desta auditoria e estão registradas em `livro-v1.0\00-changelog-v10-para-v11.md`. A ficha segue a v1.1 em cada uma.

| # | Onde estava | O que foi feito no livro |
|---|---|---|
| D1 | 29.7, Passo 12 e ficha fechada da Nadir | A marreta passou de `1d12 + 4` (média 10) para `1d12 + 4 + 2` = `1d12 + 6` (média 12): o exemplo esquecia o +2 de Mãos I (25.3) |
| D2 | 07.1 a 11.1 | As nove fichas de Caminho ganharam a linha "Recurso próprio" |
| D3 | 23.5 | Quadro novo: Xianzhouíta, Vulpes e Avginiano rolam Morrendo com Vantagem. **É a única que muda o jogo** |
| D4 | 24.1 (e 03, 18.4, resumo de 24) | Pesada: -2 em Reflexos e nas Perícias de Agilidade; não afeta o Teste de Ataque. Sem Esquiva com Pesada |
| D5 | 25.2 (e tabela de tetos, resumo e glossário) | Cada Sobreposição soma +1 e +10 PV; o PV para junto com o numérico (+30 PV nos Níveis 1 e 2, +35 nos 3 e 4) |
| D6 | 21.2, 21.5 e 29.12 | Escrito que Congelado só existe em inimigo |
| D7 | 04.5 | A quantidade de Perícias escolhidas é fixada na criação |
| N1 | 26.2, linha do nível 16 | "reescreve 1 por nível, do 16 ao 20" |
| N2 | 29.7, Passo 12 | Escrito que o Cone de Luz sem alvo do Bônus Maior não soma em nada |
| N3 | 07 a 15, Bênçãos | Sem mudança: a frequência já está no texto do Efeito, e a ficha a extrai de lá |
| N4 | 22.3 | DT típica contada nos níveis de referência 3, 7, 11, 15 e 19 |
| N5 | 26.3, PH | Sem mudança: a tabela é de mesa de 4 e o texto já aponta a fórmula de 16.2, que a ficha usa para 1 a 6 jogadores |

Nenhuma inconsistência nova do livro apareceu na rodada da v1.1.

## 6. Limitações

- **A biblioteca `formulas` não é o Google Planilhas.** As diferenças conhecidas (`--`, `COUNTIF "?*"` com números, `TRIM` com espaço duplo) foram evitadas na ficha, e o lint garante isso. Mesmo assim, a conferência final é abrir no Google: siga a checklist de 2 minutos de `COMO-USAR-NO-GOOGLE-PLANILHAS.md`.
- **Validação de dados e formatação condicional não foram executadas** pela `formulas` (destaque da linha do nível na Progressão, fundo rosa dos avisos, cinza do Memoespírito fora da Recordação). O lint confere a sintaxe; o desenho só simula o fundo rosa dos avisos.
- O desenho dos recortes é uma aproximação do Google (Arial do Windows, largura de coluna estimada). Por isso a suíte `visual` mede com 10% de folga na largura do texto e 8 px de margem; a Em Jogo usa exatamente os 1360 px da tela, então um navegador com zoom diferente de 100% pode pedir rolagem lateral.
- Não verificado: o separador decimal quando um número entra num texto (ex.: "itens 4.5" na Equipamento). Com o Google em pt-BR pode aparecer "4.5" ou "4,5"; o número da célula ao lado está certo.
- Cosmético, sem efeito nas contas: o bloco "No próximo nível você ganha" deixa linhas vazias entre os itens que não mudam.

## 7. Como regenerar e retestar

```powershell
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\gerar_ficha.py"
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\testar_ficha.py" --suite tudo
```

O gerador grava o modelo, a Ficha Exemplo e `build\ficha_mapa.json`. Para uma suíte só: `--suite spike|protegidos|dados|ouro|oraculo|extremos|lint|texto|preview|visual|google`. A bateria completa leva uns 22 minutos (revisão 2; extremos ≈ 13 min). As versões das dependências estão em `build\requirements-ficha.txt`.
## 8. Ajustes pedidos pelo usuário

### 8.1 "Resumo para o Jogador" no lugar de "Resumo para o Mestre"
- O bloco A1:D12 da aba Em Jogo agora se chama **Resumo para o Jogador**, com o mesmo conteúdo. O lint confere o título e procura "Resumo para o Mestre" em todas as células, fórmulas, validações e notas do `.xlsx`: 0 ocorrência.
- Textos revistos pensando no jogador: no `COMO-USAR`, a seção 2 virou "Uma cópia para cada personagem" (você faz a sua cópia e, se quiser, compartilha com o Mestre como Leitor) e a checklist manda refazer a importação em vez de "avisar o mestre". "Mestre" ficou só onde é regra do livro ("o Mestre escolhe" o método de atributos, "escreva com o Mestre" o Efeito Condicional, "o Espaço que o Mestre aprovar").

### 8.2 Sem linhas congeladas
- As 9 abas que tinham painel congelado (A5, B5, B9, B5, A5, A5, C5, A5, A5) não têm mais. O lint confere nas 10 abas que `freeze_panes` é vazio e que o `sheet_view` não tem painel.

### 8.3 Células visualmente diferentes, para não precisar congelar
- **Estilos novos** (legenda no topo de cada aba): cabeçalho de coluna em azul-médio `#B4C6E7` com texto `#1F3864` em negrito e borda inferior grossa (6,7:1); rótulo da linha em negrito com borda direita grossa; linhas alternadas em dois tons do mesmo tipo (calculada `#E8EEF7`/`#D6E0F0`, entrada `#FFF2CC`/`#FFE9B0`, texto `#FFFFFF`/`#F2F2F2`). As 14 combinações de texto e fundo da planilha têm contraste de no mínimo 4,96:1. "(preencha)" e "(automático)" continuam nos cabeçalhos.
- **Na vertical**, 55 tabelas, todas com as linhas a no máximo 15 linhas do cabeçalho: Perícias em 3 grupos de Atributos (Criação e Testes), tabela mestra da Progressão em 2 partes × 2 blocos de 10 níveis, inventário em 2 blocos de 10 itens e as tabelas de Regras Rápidas com mais de 15 linhas com o cabeçalho repetido a cada 10. As fórmulas que contam Eficácia, Perícias escolhidas e Espaço continuam com o mesmo intervalo contínuo (os cabeçalhos repetidos no meio não são "Sim" nem número).
- **Na horizontal**, a área do jogador de cada aba cabe em 1360 px: Criação 1360, Testes 1360, Habilidades 1360, Caminho 1360, Equipamento 1360, Progressão 1360 (A:I), Em Jogo 1360 (A:L), Início e Regras Rápidas sem mudança. As colunas auxiliares foram ocultadas (Criação M:O, Em Jogo O:AD, Habilidades O:W, Caminho M:N, Equipamento M:AA, Progressão R). Os avisos da Em Jogo seguem na coluna N, fora da tela, com o resumo em A13 ("Avisos (n): o primeiro · os outros estão na coluna N").
- Para caber, algumas tabelas mudaram de forma: o Efeito das Habilidades e o Efeito de 4 peças dos Conjuntos ganharam tabelas próprias com a largura toda; o guia de 16.5 e o bônus fixo das Habilidades saíram para uma tabela logo abaixo; a Ultimate mostra o guia numa linha própria.
- **Na Em Jogo** (a tela de uma página), para os nomes de até 40 caracteres caberem: o nome da arma e das Habilidades ocupa 2 colunas; dano e média aparecem juntos ("6d6+4 (25)"); Nível, PH, RT e alvos juntos; Alcance e Elemento juntos; o Resumo mostra a primeira condição ativa e quantas mais; a rolagem bloqueada mostra só "BLOQUEADA" (o motivo está nas condições e na situação da Ultimate); a situação da Ultimate traz a Energia e não repete o efeito (que está na aba Habilidades). **Duas reduções que você vai notar:** Perícias com Eficiência passaram de 14 para 10 vagas (3 do Caminho + 2 + Bônus de Sincronia não passam disso) e os Usos por combate e descanso passaram de 10 para 8 linhas, uma por linha, para "Bênção · frequência" caber inteiro; com mais de 8 usos, o aviso manda ver a aba Caminho, como antes.

### 8.4 Tamanhos das células (suíte `visual`, nova)
Rodada final: **23 898 checagens, 0 falha** (a auditoria visual final está na seção 10).

| Critério | Resultado |
|---|---|
| Todo texto cabe na própria célula ou mescla, sem transbordar (Arial, 10% de folga, 8 px de margem), nos 4 estados: em branco, Nadir 29.7, nível 20 completo e **pior caso** | 22 521 textos, 0 não coube |
| Pior caso (novo estado do `renderizar_ficha.py`): toda lista na opção mais longa, números no máximo, textos reais do capítulo 01 do livro com Nome 40, Jogador 30, Conceito 80, Propósito 200, Aparência 300, nomes 40, efeitos 300 e itens de inventário 40 caracteres | sem valor de erro; a ficha não tem campo "Anotações", então esse tamanho não se aplica |
| Lista suspensa ≥ opção mais longa + 24 px | 196 células |
| Texto buscado na aba Dados cabe com o texto mais longo da coluna | 552 células |
| Aviso cabe com a mensagem mais longa que a fórmula pode montar (literais lidos com o Tokenizer do openpyxl) | 185 avisos |
| Toda entrada com rótulo visível à esquerda ou no cabeçalho acima, fora de linha/coluna oculta | 358 entradas |
| Fonte ≥ 9 pt e contraste ≥ 4,5:1 | 0 célula abaixo de 9 pt (as 13 de 8 pt da Em Jogo subiram para 9); menor contraste 4,96:1 |
| Distância ao cabeçalho ≤ 15 linhas e área do jogador ≤ 1360 px | 55 tabelas e 9 abas OK; Em Jogo A:L × 1-40 = 1360 × 760 px |
| Aviso não bloqueante: coluna com mais que o dobro do maior conteúdo | 51 colunas, quase todas estreitas com números curtos embaixo de um cabeçalho de palavra longa ("Especialização", "Eficiência"); aceito como cosmético: estreitar cortaria o cabeçalho |

O gerador usa a mesma régua (`renderizar_ficha.medir`) para ligar a quebra de linha e aumentar a altura das linhas de texto fixo, das entradas livres, dos avisos e dos textos buscados na Dados; quando uma palavra não cabe e a coluna precisa alargar, a coluna de aviso da aba encolhe para a área continuar em 1360 px.

## 9. Revisão independente

Uma revisão independente da v1.1 aprovou a ficha e o livro e levantou 6 achados, nenhum bloqueante.

| # | Achado | O que foi feito |
|---|---|---|
| 1 | Linhas da Criação (atributos, Perícias) e do Equipamento têm altura fixa pelo aviso mais longo possível e ficam quase vazias no uso normal | Resolvido na auditoria visual final (seção 10): os avisos passaram para K:L onde K estava livre, e as linhas encolheram sem cortar nada |
| 2 | O teste de digitação do guia (nível 1 → 3) não detectava recálculo quebrado: Atletismo já é d20+6 no nível 1 | Trocado em `COMO-USAR-NO-GOOGLE-PLANILHAS.md`, seção 5: nível 4, e Testes!I16 vira d20+7 (Eficiência +3) |
| 3 | A crença da Nadir na Ficha Exemplo era o exemplo genérico do capítulo 05 | Trocada pela de 29.7, "Eu não assino nada que eu não consertei", e a Ficha Exemplo foi regerada |
| 4 | O texto corrido de 01.6 e 27.19 chamava o livro de "v1.0" | Trocado por "este livro" e "Este é o livro de regras" (R1 no changelog da v1.1); `.docx` e `.pdf` V1.1 regerados e verificados |
| 5 | A seção 3.1 citava `F15` (é `G15`) e a 8.4 adiava as 51 colunas largas | Corrigidos: `G15`, e as colunas largas ficam aceitas como cosmético |
| 6 | Handoff e temporários `.agents\tasks\tmp_checklist.*` desatualizados | Feito na limpeza final (seção 10) |

## 10. Auditoria visual final (04/10, depois da revisão)

Pedido: dados visualmente organizados, visíveis para quem preenche e células do tamanho certo. Bateria completa (`--suite tudo`) depois das correções: **as 10 suítes saem OK, código 0** (spike 14, protegidos 76, dados 3297, ouro 533, oráculo 247 casos com 0 divergência, extremos 858, lint 6204, texto 975 083, preview 278, visual 23 898; todas com 0 falha). Saída completa em `.agents\tasks\suite-tudo-final.txt`.

### 10.1 O que foi medido

| Medida | Resultado |
|---|---|
| Textos medidos por estado (cada um cabe na própria célula ou mescla, Arial, 10% de folga, 8 px de margem) | em branco 5236 · Nadir nível 1 5446 · nível 20 completo 5770 · pior caso 6069 = **22 521, 0 não coube** |
| Entradas com rótulo visível (à esquerda ou no cabeçalho), fora de linha ou coluna oculta | 358, 0 sem rótulo |
| Listas suspensas com espaço para a opção mais longa + 24 px da seta | 196 |
| Textos buscados na aba Dados medidos pelo mais longo da coluna | 552 |
| Avisos medidos pela mensagem mais longa que a fórmula monta | 185 |
| Largura da área do jogador | Início 1264 · Criação 1360 · Em Jogo 1360 (A:L × linhas 1-40 = 1360 × 760) · Testes 1360 · Habilidades 1360 · Caminho 1360 · Equipamento 1360 · Progressão 1360 (A:I) · Regras Rápidas 1243 px. A aba Dados (2168 px em A:L) não é área do jogador |
| Maior distância de uma linha ao cabeçalho da tabela | 12 linhas (catálogo de Bênçãos da Caminho, cabeçalho na linha 39); limite 15, em 55 tabelas |
| Painéis congelados ou divididos | **0** nas 10 abas |
| Fonte e contraste | nenhuma célula abaixo de 9 pt; 14 combinações de texto e fundo, a menor com 4,96:1 (mínimo 4,5:1) |

### 10.2 Problemas encontrados e corrigidos

| Onde | Antes | Depois |
|---|---|---|
| Criação, atributos (linhas 44-50) e outras linhas com aviso | Aviso na coluna L (152 px): a linha crescia até 95 px pelo aviso mais longo possível, quase vazia no uso normal | Onde K estava livre, o aviso e o cabeçalho "Aviso" passam para K:L (255 px): atributos com 65 px, nível, jogadores, crença, Raça e arma com 1 a 2 linhas a menos. Numa tabela, ou todas as linhas mudam ou nenhuma, para a coluna ficar alinhada (`alargar_avisos` em `gerar_ficha.py`) |
| Criação, Traços (texto inteiro do livro), linha 30 | Altura fixa de 213 px para um texto de no máximo 7 linhas | A altura sai da medida do texto de Raça mais longo (≈ 110 px) |
| Criação linha 93 e Equipamento linha 9 (números da armadura) | 110 e 120 px vazios: a régua tomava o texto mais longo da tabela de armaduras inteira, não da coluna buscada | A régua (`renderizar_ficha.PiorTexto`) usa só a coluna do `VLOOKUP`/`HLOOKUP` com índice fixo: linhas de 1 linha |
| Caminho, Bênçãos adquiridas (slots 1-10) | Aviso em L com 130 px: linhas de 95 px | Aviso em K:L com 198 px (Requisito, Frequência e Conta na ficha cederam espaço; quebram em 2 linhas como antes): linhas de 64 px |
| Equipamento, inventário (20 itens) | "Do catálogo?" ocupava G:K e o aviso ficava em L: linhas de 80 px | "Do catálogo?" em G:J, aviso em K:L: linhas de 49 px |
| Equipamento, arma secundária | Aviso em L, linha de 200 px | Aviso em K:L, linha de 125 px |
| Altura total das abas no pior caso | Criação 5353 · Caminho 4504 · Equipamento 5218 px | Criação 4406 · Caminho 3841 · Equipamento 4253 px (2575 px a menos de rolagem) |

No caminho, a suíte `visual` pegou um caso-limite: com uma das larguras testadas, uma linha do aviso dos slots ficava exatamente na borda (187 px em 187 px). A largura final passa, e a suíte continua cobrindo esse caso.

Nada mudou nas contas: os nomes lógicos seguem as células novas (`build\ficha_mapa.json`), ouro, oráculo e extremos saem com os mesmos números, e nenhuma célula da checklist do `COMO-USAR` mudou de lugar (Início!B17, Em Jogo!B3:B8, C16:G16, A19, C19, D19, Habilidades!D61:E61, Equipamento!B56, Criação!B8, Testes!I16 e os intervalos de caixa de seleção). Os valores da Nadir nessas células foram vistos no recorte da Em Jogo e são os do livro.

### 10.3 Recortes olhados (24, todos com no máximo 1800 px)

- Pior caso, antes das correções: Em Jogo 01, Início 01, Testes 01, Criação 01-03, Habilidades 01-02, Caminho 01, Equipamento 01-02, Progressão 01.
- Pior caso, depois das correções: Criação 01-02, Caminho 01 (2 vezes, com larguras diferentes), Caminho 02, Equipamento 01-03, Regras Rápidas 01.
- Nadir nível 1: Em Jogo 01, Criação 01, Habilidades 01.

Em todas: blocos com título e na ordem de uso (os 12 passos na Criação; Recursos, Ações e Testes na Em Jogo); nada cortado; toda entrada amarela com rótulo; Resumo para o Jogador em A1:D12 da Em Jogo; nenhuma linha ou coluna congelada.

### 10.4 Ficou como está (cosmético, sem corte de texto)

- Habilidades, linhas 12-19 (≈ 65 px): o aviso de cada Habilidade pode juntar até 235 caracteres. Equipamento, Relíquias (linhas 36-41) e Cone de Luz (linhas 20 e 23): a coluna K já tem dado, então o aviso fica só em L.
- Regras Rápidas, tabela de Energia (linhas 66-71): linhas um pouco mais altas que o texto.
- Habilidades e Em Jogo mostram as colunas espaçadoras M e N (≈ 20 px cada) à direita da área do jogador.
- As 51 colunas com mais que o dobro do conteúdo (cabeçalho de palavra longa sobre números curtos), já aceitas na seção 8.4.
- Em `ficha-automatizada\` há um arquivo que não é entregável nem foi gerado pela ficha: `explorando galaxias ficha teste mc filhos.xlsx`. Não foi mexido.

### 10.5 Limitação

A régua é a do `renderizar_ficha.py` (Arial, medida em pixel). O Google Planilhas desenha um pouco diferente (fonte, margem interna, quebra de linha), por isso cada texto precisa caber com 10% de folga e 8 px de margem. A importação real é conferida pela checklist de 2 minutos da seção 5 do `COMO-USAR-NO-GOOGLE-PLANILHAS.md`.

O livro não foi alterado nesta etapa: os `.md` são de 21:26, o `.docx` V1.1 de 21:27 e o `.pdf` V1.1 de 21:28, e `scripts\verificar-livro-final.ps1` passa (código 0).

## 11. Correção dos erros no Google (revisão 2)

**O que aconteceu.** Editando a ficha V1.1 no Google Planilhas, a escolha **Humano → "+1 em dois"** encheu a ficha de `#ERROR!`: no export do Google, **261 das 2.363 fórmulas** estavam com erro (Criação 89, Em Jogo 84, Testes 75, Equipamento 5, Início 5, Habilidades 1, Progressão 1, Regras Rápidas 1). Outro export, com Raça Haloviano, tinha **0 erros**. A única entrada diferente entre os dois era Criação!B25:B28, e as 261 células tinham **uma raiz só: Criação!B26**.

**Causa.** O Google lê como **fórmula** qualquer valor digitado ou escolhido numa lista que comece com `=`, `+`, `-` ou `@`. A opção "+1 em dois" virava a fórmula `=+1 em dois` (erro de sintaxe), e o erro se espalhava por toda fórmula que lia B26, direta ou indiretamente. Onze listas tinham esse defeito: Criação!B26, Progressão!C57:C62 (Aumentos), Equipamento!C45:C47 (bônus de 2 peças) e Progressão!C67 (Ressonância I).

**Por que as suítes não pegaram.** Elas gravam as entradas por programa e nunca simulavam como o Google interpreta o que se digita; nenhum cenário punha um valor de erro numa entrada; e as fórmulas liam as entradas diretamente, então um erro numa entrada contaminava tudo. A afirmação "nenhum valor de erro em estado algum" das seções anteriores valia só para o motor local.

### 11.1 O que mudou

| Mudança | Detalhe |
|---|---|
| Rótulos novos (causa raiz) | "+2 em um" → **Um Atributo (+2)**; "+1 em dois" → **Dois Atributos (+1 cada)**; "+1 em um tipo de rolagem" → **Um tipo de rolagem +1**; "+1 de Velocidade" → **Velocidade +1**; "+2 de dano" → **Dano +2**; "+1 RD" → **RD +1**. Fórmulas, dados, oráculo, testes e textos de ajuda acompanham |
| Leitura protegida (contenção) | Nenhuma fórmula lê uma entrada diretamente. **333 células auxiliares ocultas** (à direita de cada aba) leem as **358 entradas** com `IF(ISERROR(X),"",IF(ISBLANK(X),"",X))`: entrada vazia ou com erro vira vazio, o resto passa igual. 2.548 leituras diretas da revisão 1 foram trocadas |
| Aviso de erro por linha | 206 sinais `ISERROR(...)*1`, um por linha com entrada; o aviso da linha mostra "O Google leu como fórmula: escolha de novo na lista" (ou "digite de novo com ' na frente"). 33 linhas que não tinham aviso (nome, conceito, Memoespírito, condições da Em Jogo...) ganharam um |
| Contador na Início | **B19** "Células com erro na ficha" e a linha 21 com a contagem por aba, `SUMPRODUCT(ISERROR(área)*1)` sobre a área usada de cada aba (sem as linhas do próprio contador). Com N > 0, C19 explica o que fazer. Dica no topo (A7): não comece um texto com +, - ou =, ou digite um apóstrofo antes |
| Versão | Início!A6 diz "Ficha V1.1 · revisão 2". O total do Painel de avisos passou de B17 para **B18** (a checklist do COMO-USAR foi atualizada) |
| Larguras | Criação!B (180 px) e Progressão!C (180 px) cabem "Dois Atributos (+1 cada)" com a seta; Progressão!H e I cederam a diferença (A:I continua em 1360 px) |

As fórmulas são 2.947 (eram 2.363): 333 da camada, 206 sinais, 12 do contador, 33 avisos novos. Nenhum número mudou: ouro, oráculo e extremos dão os mesmos valores.

### 11.2 Testes novos (todos dentro de `--suite tudo`)

| Suíte | O que confere | Resultado |
|---|---|---|
| google (nova) | (a) a revisão 1, calculada pela `formulas` com as entradas do export "Cópia" do Google, comparada com os valores que o Google gravou | **2.363 de 2.363 iguais**, 0 divergência |
| | (b) a revisão 2 com as mesmas entradas, ligada pelo nome lógico do mapa | **2.363 de 2.363 iguais**, 0 divergência aceita por rótulo, contador = 0 |
| | (c) o caso do usuário: Humano + Dois Atributos (+1 cada) + Poder + Agilidade | 0 erro, contador 0, +1 em Poder e +1 em Agilidade (capítulo 05) |
| | evidência do export com erro | 261 `#ERROR!`, única entrada diferente = Criação!B26 |
| extremos | valor de erro (`#VALUE!` ou `#N/A`, do motor `formulas`) injetado em **cada uma das 358 entradas** (196 listas, 59 texto, 83 inteiro, 20 decimal), mais 7 por cima da Nadir completa (Raça, bônus, atributos 1 e 2, Nível, Poder, Caminho) e o caso do usuário | 366 cenários: em todos o contador mostra **exatamente 1**, nenhuma outra célula fica com erro e o aviso da linha acende |
| lint | nenhuma opção de lista (fixa, por intervalo ou dependente) começa com `=`, `+`, `-` ou `@`, parece data, hora, número ou booleano; nenhuma fórmula fora da camada lê uma entrada | 196 listas, 4.098 opções, 0 risco; 0 leitura direta. Na revisão 1 a mesma checagem acusa as 11 listas e as 2.548 leituras |
| spike | `""+1` dá `#VALUE!`; referência a célula vazia (Google: vazio; `formulas`: 0, diverge e está registrado); `ISBLANK("")` = FALSE; a camada e o contador com erro injetado | 23 checagens, 0 falha. A ficha não depende da divergência do vazio: a camada escreve o vazio de forma explícita |

### 11.3 Bateria completa (revisão 2)

spike 23 · protegidos 76 · dados 3.297 · ouro 533 · oráculo 247 casos · extremos 2.714 · lint 11.924 · texto 1.006.920 · preview 278 · visual 24.036 · google 4.734 — **11 suítes OK, 0 falha, código 0**. Saída em `.agents\tasks\suite-tudo-rev2.txt`. Os arquivos usados pela suíte `google` ficam em `build\google_rev1\`: a ficha da revisão 1 e os dois exports do Google feitos pelo usuário (`export-google-haloviano-0-erros.xlsx` e `export-google-humano-261-erros.xlsx`).

Recortes conferidos (estado Nadir): Início (dica do apóstrofo em vermelho na linha 7, contador em 0 nas linhas 19-21) e Criação, Passo 2 (B26 "Um Atributo (+2)" inteiro na célula, bônus racial +2 em Poder).

### 11.4 Revisão independente da revisão 2
Veredito: **APPROVED**, nada bloqueante. O revisor conferiu com scripts próprios: 196 listas sem opção-armadilha (29 cenários das listas dependentes), 0 leitura direta de entrada, erro injetado em 5 entradas contido em 1 célula, 30 de 30 células iguais ao cache do Google e os números da Nadir iguais ao capítulo 29.7.
| Achado | O que foi feito |
|---|---|
| 1 (baixo). A "Cópia de Ficha…" do usuário não está em `ficha-automatizada\` (já faltava antes da revisão 2) | O usuário confirmou que apagou de propósito. A pasta de backup foi apagada a pedido dele; o export continua só como referência da suíte `google`, em `build\google_rev1\export-google-haloviano-0-erros.xlsx` |
| 2 (baixo). A seção 7 dava dois tempos para a bateria (22 e 11 minutos) | Corrigido: ficou só o tempo da revisão 2 (uns 22 minutos) |
O gerador e os testes não mudaram, então a bateria de 11.3 continua valendo. Depois da revisão foram repetidas `protegidos` (76, 0 falha) e `google`.

**Limitação.** O teste continua sendo o motor `formulas`, agora comparado célula a célula com um export real do Google. Vale repetir no Google o passo da checklist do COMO-USAR (Humano → Dois Atributos (+1 cada) → Poder e Agilidade, contador em 0).
