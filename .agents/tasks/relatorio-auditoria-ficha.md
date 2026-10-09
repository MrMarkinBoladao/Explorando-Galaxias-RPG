# Relatório de auditoria — Ficha de Personagem automatizada · Explorando Galáxias v1.0

Entregável: `Ficha de Personagem - Explorando Galáxias v1.0.xlsx` (raiz do projeto), 10 abas, níveis 1 a 20, para importar no Google Planilhas. Gerado por `build\gerar_ficha.py`; auditado por `build\testar_ficha.py` (9 suítes). O livro v1.0 não foi alterado (suíte `protegidos`, SHA-256 de 37 arquivos).

**Veredito:** as 9 suítes saem OK e `--suite tudo` termina com código de saída **0**: 0 divergências planilha × oráculo, 0 valores de erro, 0 achados de texto, 0 textos cortados, Em Jogo dentro de 1360 × 768.

## 1. Comandos exatos e saída (rodada final, 04/10/2026)

```
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\gerar_ficha.py"
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\testar_ficha.py" --suite tudo
```

O gerador imprimiu `2131 células, 49 blocos, 32 listas`. A bateria terminou com `$LASTEXITCODE = 0`.

| Suíte | Resultado | Números |
|---|---|---|
| spike | OK · 14 checagens · 0 falha | lista efetiva de 33 funções + `&`; acento em nome de aba OK; carga 1,5 s |
| protegidos | OK · 74 · 0 | 37 arquivos do livro, `.docx`/`.pdf` V1.0, `gerar_docx.py`, `gerar_pdf.py` com o mesmo SHA-256 |
| dados | OK · 3297 · 0 | 49 blocos e 32 listas conferidos célula a célula com parser próprio do teste; 51 âncoras; 108 Bênçãos (12 × 9, tiers 6/4/2) |
| ouro | OK · 466 · 0 | casos (a)–(n) do plano no oráculo e na planilha; cobertura de 78 campos das fichas 29.8/29.9 = 230 células |
| oraculo | OK · 245 · 0 | 126 casos da matriz + 60 da varredura (3 × 20) + 59 casos-limite = 245 casos; **43 391 saídas comparadas**; 230 códigos de aviso do oráculo achados na planilha; **0 divergência**; 8 processos, 80 s |
| extremos | OK · 862 · 0 | 2360 células com fórmula calculadas em 769 cenários (661 de um campo por vez); 360 entradas; 185 células de aviso; 0 valor de erro; 330 s |
| lint | OK · 6182 · 0 | 2360 fórmulas, 301 validações, 195 regras de formatação condicional em 10 abas; Em Jogo A:L = 1359 px |
| texto | OK · 946 774 · 0 | 7197 trechos visíveis; 25 proibidas + 18 aposentadas (309 471 buscas); 97 termos do glossário (2604 ocorrências); 22 931 palavras contra léxico de 4883 + 89 extras; 85 formas sem acento (611 745 buscas) |
| preview | OK · 228 · 0 | 30 PNGs inteiros + **201 recortes 1:1 (≤ 1800 × 1800 px)**; 0 texto cortado; Em Jogo A:L × linhas 1-40 = **1359 × 760 px** |

Antes de mexer no código (passo 0, mesmos comandos), o estado real já era: spike 14 · protegidos 74 · dados 3297 · ouro 466 · oraculo 245 (0 divergência) · extremos 862 · lint 6181 · texto 946 515 · preview 138, todas OK. O que faltava da FEAT-004 era o renderizador em recortes, a inspeção visual, este relatório e o fechamento.

## 2. O que cada suíte verifica

- **oraculo** — `build\oraculo_ficha.py` reimplementa as regras direto do livro (não importa o gerador nem `ficha_dados.py`, não lê fórmula). Cenários determinísticos por semente: atributos pelo array ou Compra, bônus racial, Atributo de Habilidade permitido, Elemento, Perícias no limite, armadura e arma variadas, Bênçãos válidas por slot, Habilidades até o limite, Ressonâncias, Cone e Relíquias da faixa, Conjuntos, inventário, Memoespírito na Recordação. A planilha é calculada pela biblioteca `formulas` com as entradas postas pelo mapa (`build\ficha_mapa.json`). Por caso compara atributos, bônus, núcleo do nível (Eficiência, Eficácia, slots, Especialização, tetos, PH, Ultimate, Cone, Tier…), PV, Defesa, Esquiva, RD, VEL, DT, 18 Perícias, 6 TR e Morrendo (total, rolagem, Vantagem), Ataque Básico (as duas colunas de D1), Habilidades, Ultimate, slots de Bênção, Pacto da Ruína, inventário, Relíquias, Conjuntos, Barreira, Memoespírito, e os códigos de aviso nos dois sentidos (aviso só na planilha ou só no oráculo = divergência).
  - Varreduras 1→20: Humano/Destruição; Xianzhouíta/Recordação com Memoespírito ativo; Intellitron/Caça com Olho de Lan e Pesada.
  - Casos-limite (59): Humano +1/+1 diferente e no mesmo atributo, atributo > 15 antes da Raça, aumentos até 20 e além, atributo 3 e 25, nível 0 e 21, jogadores 0/2/7, array repetido, Compra acima de 28, Perícias a mais, Perícia do Caminho escolhida, Eficácia sem Eficiência e acima dos slots, Esquiva com Pesada, Habilidades a mais, Nível acima do máximo e Nível 9, Ressonância III repetida e no Nível máximo, Bênção de tier acima do slot, repetida, de outro Caminho, em slot futuro, Cone acima da faixa e Sobreposições a mais, Conjuntos 2+2+2, RD no teto, VEL > 25, inventário com quantidade 0 / acima da capacidade / acima do dobro, Florescimento no teto, Instinto, Cicatriz, Corpo Imortal, Recordação 20 completa, Memoespírito inválido de 6 formas, nível 20 tudo no máximo, Caça 20 com Pesada.
- **extremos** — calcula TODAS as fórmulas em: ficha em branco, só nome, cada Raça, cada Caminho, um campo por vez (valor válido e inválido: texto em número, nível 0/21/"abc", atributo 3 e 25, Bênção de outro Caminho colada, jogadores 0, Nível de Habilidade 9…), Nadir completa, Recordação 20, Caça 20 Pesada, Destruição 12 e Em Jogo com condições. Meta cumprida: nenhum `#N/A #VALUE! #REF! #DIV/0! #NAME? #NUM!`; cada inválido acende aviso PT-BR não vazio na célula de aviso certa; ficha em branco e Nadir completa sem aviso.
- **lint** — toda fórmula, validação e formatação condicional via Tokenizer: só funções da lista efetiva, sintaxe inglesa com vírgula, sem `;`, sem `SE`/`PROCV`, sem `ROUNDDOWN` (arredonda com `INT`), sem `INDIRECT`/`OFFSET`/matriz dinâmica/`_xlfn`, sem `--`, sem `[`, formatação condicional e validação personalizada sem referência a outra aba, só Arial, sem proteção, sem nome definido, sem macro, `fullCalcOnLoad`.
- **texto** — strings proibidas de `scripts\checar-nomenclatura.ps1` (`\b…\b`, sem caixa) e aposentadas de 30.2; grafia exata do glossário 30.1; ortografia por léxico (palavras dos `.md` do livro + `build\ficha_lexico_extra.txt`); acentuação. Duas grafias fora do glossário são citação literal do livro e ficam aceitas: "Bônus de atributo" (`'Dados'!B6`, cabeçalho da tabela de 05) e "dano contínuo" (`'Dados'!C377`, texto de 20.1).
- **preview** — ver seção 4.

## 3. Correções feitas nesta FEAT

### 3.1 Diferencial planilha × oráculo (feitas antes da queda, confirmadas agora com 0 divergência)

As seis diferenças que a FEAT-003 previu foram decididas pelo livro; em todas o errado era o **oráculo** (a planilha já seguia a seção), e a correção está em `oraculo_ficha.py` com a seção no comentário:

| # | Diferença | Seção que decide | Correção |
|---|---|---|---|
| a | Cone "Um Teste de Resistência"/"Uma Perícia" | 25.2: bônus em "um Teste de Resistência, ou uma Perícia" | oráculo passou a aplicar no TR/Perícia indicado em "qual"; sem "qual", não vale |
| b | Conjunto "+1 em um tipo de rolagem" | 25.3 | oráculo aplica na rolagem escolhida (TA, TR ou Perícia) |
| c | Conjuntos 2+2+2 com "+2 de dano" | 25.3: "não somam mais de +3 em uma mesma rolagem" | oráculo limita o dano de Conjunto a +3 |
| d | Ressonância III marcada em várias | 26.7: "uma Habilidade" | oráculo dá o Nível só à primeira marcada (aviso RESSONANCIA_III_REPETIDA) |
| e | Inventário com quantidade 0 | 24.4: o Espaço conta o que você carrega, veste e empunha | oráculo conta 0 unidades como nada carregado (vazio = 1) |
| f | Rótulo do acúmulo com Bênção de outro Caminho | — | não é saída numérica: fica como texto de exibição (decisão de leitura 8 da FEAT-003) |

O aviso `em_jogo.aviso.usos` (a tabela de Usos da Em Jogo tem 10 linhas) é limite de layout, não regra do livro, e fica fora do diferencial.

### 3.2 Renderizador e suíte preview

`build\renderizar_ficha.py` agora desenha cada aba sempre em escala 1:1 e grava, além do PNG inteiro (reduzido só se passar de 6000 px), **recortes de no máximo 1800 × 1800 px em 1:1**, cortados na divisa de coluna/linha, com as letras das colunas e os números das linhas repetidos em cada recorte, como `<estado>-<aba>-parte-NN.png`, mais `indice-recortes.txt` com o intervalo de células de cada recorte. A suíte confere que todo recorte existe, nenhum passa de 1800 px e que juntos cobrem a área inteira da aba (prova de que não houve redução). Duas melhorias de fidelidade: o preenchimento esconde a grade (como no Google), e texto branco que transborda da faixa azul para fundo branco agora conta como texto cortado (no Google ele some).

### 3.3 Layout e texto (achados da inspeção visual dos recortes)

- Títulos de bloco curtos na aba Dados ("Vantagens e traços automáticos por Raça…", "Compra de Pontos — 03 Passo 4 (Método B)" e outros) tinham o fim em branco sobre branco: novo `estender_titulos()` estende a faixa azul até o texto caber.
- Rótulos e textos fixos (`texto()`, `nao_se_aplica()`) e textos quebrados (`cal(..., quebra=True)`) passaram a centro vertical: nas linhas altas o rótulo ficava no rodapé e o valor no meio (Início, Caminho, Habilidades, Equipamento, Progressão).
- Em Jogo: as duas caixas de Morrendo (B33/C33) não diziam qual era qual; a linha de respiro 34 ganhou "↑ sucessos (0 a 3)" e "↑ falhas (0 a 3)" em 8 pt cinza. Nenhuma entrada mudou de endereço.
- Habilidades: Tipo, Em área? e Resolução da Ultimate mescladas em C:D ("Teste de Resistência" saía da caixa amarela).
- Criação (Números do seu nível) e Progressão (tabela mestra): cabeçalho e número centrados na mesma coluna.
- Regras Rápidas: nas tabelas copiadas da Dados, coluna simples centrada e texto à esquerda, centro vertical ("21" encostava em "5d8").
- Progressão: a coluna auxiliar R (Ressonância efetiva) virou cinza de auxiliar; linhas das Ressonâncias de 60 para 45 pt.
- Texto: "(decisão 4)", "(decisão 5)" e "(decisão 9)" saíram da Início e das Regras Rápidas (número de decisão do plano não diz nada ao jogador); o conteúdo da frase não mudou.

Nenhum cálculo, endereço de entrada, lista ou aviso mudou: as suítes ouro, oraculo e extremos seguem com 0 falha depois dessas mudanças.

## 4. Inspeção visual

Recortes abertos e olhados (todos ≤ 1800 px): Em Jogo parte-01 nos 3 estados e parte-02 (nível 20); Início; Criação parte-01 e parte-03 (Nadir); Testes; Habilidades parte-01; Caminho parte-01, 02 e 03 (nível 20) e parte-03 (em branco); Equipamento parte-01 (Nadir e nível 20) e parte-02; Progressão (Nadir e nível 20); Regras Rápidas parte-01 e 02; Dados parte-01, 02 e 06. Depois de cada lote de correções os recortes foram regerados e reabertos. Resultado: texto legível em 1:1 (corpo 9–10 pt), blocos separados por faixa azul com capítulo, entradas amarelas com borda, avisos em vermelho no fundo rosa, Em Jogo inteira numa tela com Resumo para o Mestre no canto superior esquerdo.

Não abertos (cobertos só pela checagem automática de texto cortado): Criação parte-02/04 e Habilidades parte-02 (colunas auxiliares), Equipamento parte-03/04, Em Jogo parte-03 e 42 dos 45 recortes da aba Dados.

PNGs: `.agents\tasks\ficha-preview\` tem 231 arquivos = 30 inteiros (`<estado>-<aba>.png`) + 201 recortes (67 por estado: Início 1, Criação 4, Em Jogo 3, Testes 1, Habilidades 2, Caminho 4, Equipamento 4, Progressão 1, Regras Rápidas 2, Dados 45). Estados: `em-branco`, `nadir-nivel-1` (29.7), `nivel-20-completo` (Lin Qiu, Xianzhouíta da Recordação). Lista completa com intervalos em `indice-recortes.txt`.

## 5. Divergências e lacunas do livro (o livro NÃO foi editado)

| Código | Onde | O que acontece | Decisão na ficha |
|---|---|---|---|
| D1 | 29.7 × 25.3 | A ficha fechada da Nadir dá a marreta `1d12 + 4` (média 10), mas a mesma ficha tem Mãos I (+2 no Ataque Básico): pela regra o total é `1d12 + 6` (média 12) | Duas colunas no Ataque Básico (Equipamento e Em Jogo): "Dados + atributo" = livro; "Com equipamento" = regra |
| D2 | 08, 09, 10 | Só 07 e 11–15 têm "Recurso próprio"; Inexistência, Harmonia e Abundância não declaram | Mostra "Sem recurso próprio declarado (D2)" e os contadores das Bênçãos adquiridas |
| D3 | 23.5 × 05 e 22.1 | 23.5 cita Vantagem no Teste de Morrendo só para o Xianzhouíta; Vulpes e Avginiano têm Vantagem em Força de Vontade, e 22.1 diz que esse é o Teste de Morrendo | Vantagem nos três, com nota "leitura combinada de 05 e 22.1" |
| D4 | 24.1 × 18.2 | Pesada dá "-2 em Testes e Perícias de Agilidade" | -2 em Reflexos, Acrobacia, Furtividade e Pilotagem; não no Teste de Ataque (18.2 não lista penalidade de armadura) |
| D5 | 25.2 | Sobreposição sem incremento numerado | Exemplo de 25.2: +1 e +10 PV por cópia, tetos +3 / +50 PV, no máximo uma por faixa alcançada, com aviso |
| D6 | 21.5 | Congelado só define Comum/Elite/Boss | No personagem é só texto |
| D7 | 04.5 | Perícias escolhidas dependem da Sincronia, sem dizer qual momento | Usa a Sincronia da criação (após Raça, sem aumentos) |
| N1 | 26.2 × 16.6 | 26.2 escreve "reescreve 1 por nível" só na linha do 16; 16.6 diz "a partir do nível 16" | "Sim" do 16 ao 20 |
| N2 | 29.7 | Nadir tem Cone de Luz Nível 1 sem alvo do Bônus Maior; nenhum número impresso o inclui | Cone sem alvo não soma o numérico e não gera aviso |
| N3 | 07–15 | Frequência das Bênçãos não está em campo próprio | Extraída do corpo do Efeito ("uma vez por turno/Ciclo/combate…"); sem expressão = "Sem limite declarado" |
| N4 | 22.3 | A DT típica 15/17/18/19/21 não diz o nível | Corresponde aos níveis 3, 8, 11, 14 e 19 com Bônus +5 (conferido no ouro) |
| N5 | 26.3 | A tabela de PH é de mesa de 4 | PH calculado pela fórmula de 16.2 para 1–6 jogadores (3–6 = tabela; fora disso, aviso) |

Divergências novas do livro nesta FEAT: nenhuma. As diferenças do diferencial (3.1) eram do oráculo, não do livro. Os códigos "(D1)", "(D2)" e "(D5)" que aparecem na ficha apontam para esta tabela.

## 6. Decisões registradas (seção 3 do plano, resumo)

1. Condições nos números só quando inequívocas (Lentidão, Silenciado, Controlado, Surpreso, Morrendo automático com PV 0, sobrecarga); Danos Contínuos e o resto só como texto + tique estimado.
2. Bênçãos de efeito fixo entram nos números (Corpo Imortal, Pele de Pedra, Olho de Lan, Avatares, Instinto, Memória Compartilhada etc.), temporários sempre por `MIN(teto da faixa, soma)` com aviso.
3. Dados por parser dos `.md` + módulo transcrito com âncora literal (testado pela suíte dados).
4. Sem rolador de dados: a ficha entrega a rolagem pronta.
5. PV atual é entrada direta + calculadora de dano (RD, exceto Dano Contínuo → mínimo 1 → temporário → PV).
6. Sem nomes definidos; o mapa lógico fica em `build\ficha_mapa.json`.
7. Arredondamento só com `INT`.
8. Fora da faixa: aviso PT-BR e conta com o valor limitado, nunca erro.
9. PV rolado (variante de 06.4) não é calculado; está nas Regras Rápidas.
10. Listas dependentes por `INDEX/MATCH` em colunas auxiliares cinzas na própria aba.
11. Validação com `errorStyle="warning"`; a regra vive na coluna de aviso.
12. Nenhuma entrada em dois lugares (arma principal e armadura na Criação, espelhadas na Equipamento).

As decisões de leitura das FEATs 002 e 003 (ordem das linhas para Perícias/Eficácia excedentes, Bênção de outro Caminho conta com aviso, Esquiva "Proibida (Armadura Pesada)", ficha em branco = nível 1 / mesa de 4 / atributos 8, Cone sem alvo, Ressonância III só na primeira, Instinto só com PV preenchido etc.) estão nos findings de `FEAT-002.json` e `FEAT-003.json` e foram todas confirmadas pelo diferencial.

## 7. Limitações honestas

- A biblioteca `formulas` 1.3.4 não é o Google Planilhas. Diferenças conhecidas pelo spike e evitadas na ficha: `--` (proibido pelo lint), `COUNTIF "?*"` com números, `TRIM` com espaço duplo (fora da lista). **Recomendação:** importar uma vez no Google, abrir a aba Início e conferir que o Painel de avisos mostra 0 com a ficha em branco; depois preencher a Nadir de 29.7 e conferir PV 61, Defesa 16, Esquiva 18, ataque d20+6.
- Validações de dados e formatação condicional (destaque da linha do nível na Progressão, fundo rosa dos avisos, cinza do Memoespírito fora da Recordação) não são executadas pela `formulas`; o lint confere a sintaxe e o renderizador só simula o fundo rosa dos avisos.
- O renderizador é uma aproximação (Arial do Windows, largura de coluna `×7+5` px); a quebra de linha do Google pode diferir em 1–2 px.
- Não verificado: separador decimal quando um número é concatenado em texto (ex.: "itens 4.5 · armas 2" na Equipamento). Com o local pt-BR o Google pode mostrar "4,5" ou "4.5"; o valor numérico da célula ao lado está certo.
- Cosmético, sem efeito em conta: o bloco "No próximo nível você ganha" deixa linhas em branco entre os itens que não mudam; as listas de validação da Dados dividem linhas altas com a tabela de Raças.

## 8. Como regenerar e retestar

```
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\gerar_ficha.py"
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\testar_ficha.py" --suite tudo
```

Uma suíte só: `--suite spike|protegidos|dados|ouro|oraculo|extremos|lint|texto|preview`. Tempo total ≈ 9 min (extremos ≈ 5,5 min, oraculo ≈ 1,5 min e preview ≈ 1,5 min, todas com multiprocessing). A suíte preview apaga e regrava os PNGs e o índice em `.agents\tasks\ficha-preview\`.
