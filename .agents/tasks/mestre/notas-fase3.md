# Notas da Fase 3 (R8–R11, R13): decisões e achados

## Decisões
- **Nome do arquivo:** o modelo continua `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx` (`nucleo.SAIDA_MODELO`),
  porque o livro v1.2 foi adotado na Fase 2. O pedido da Fase 3 fala em "V1.1"; o `…V1.1.xlsx` fica só como registro.
- **Escudo em 5 páginas A4 paisagem** (design §6.15 previa 3): o conteúdo não cabe em 3 com corpo de 9 pt. A altura útil
  da página é calculada (`ALTURA_PAGINA_PT` = 633 pt), e o gerador para se uma página passar disso
  (`aba_escudo.paginas_altas`). Alturas atuais: 629,5 / 631,0 / 574,5 / 576,5 / 555,5 pt.
- **27.10 no Escudo:** só os 14 casos que a mesa mais consulta (`CASOS_MESA`); a tabela inteira está na aba Dados.
- **Trechos de regra do Escudo e das abas** (bloco `textos` da aba Dados): a coluna de chave mostra "T01"… e as
  fórmulas apontam a célula pela posição (`nucleo.dtexto`). Assim nenhuma chave interna, como "precos", vai para uma
  fórmula ou para o texto visível.
- **Oráculo sim/não:** o rótulo da probabilidade é "Meio a meio", e não "50/50", porque o Google lê "50/50" como data.
- **Rolador de dados (G = 650) e Minhas Tabelas (G = 701–710)** usam a semente da Início (`sorteio.py`), e não
  RAND/RANDBETWEEN. O lint proíbe RAND, e o Google recalcularia a cada edição.
- **H15 (estoque por tipo de loja):** o mapa é curado em `mestre_dados3._LOJA_ITENS`/`loja()`. Há uma cópia
  independente em `testes_fase3.LOJA_H15` e outra no oráculo, e todo preço é conferido contra 24.1–24.3.
- **Grupo:** novos G5 (6 Testes de Resistência + Percepção, Intuição e Furtividade) e G6 (Pesquisa, Ciência, Sintonia,
  Persuasão + "Traços e passivas"); aviso de Tier no G4 (25.3); linhas de resumo de surpresa e de fraqueza.
- **Sessão Zero (H24):** só tom e temas, limites e véus, expectativas e o bloco "Combinados" não têm seção do livro,
  e estão rotulados assim. Todos os outros itens citam uma seção, e a suíte `texto` confere a seção e a palavra-chave.
- **Relógios (H16):** a barra usa ● e ○, como manda o design; a checagem de emoji da suíte `texto` aceita esses dois
  caracteres.
- **Determinismo (e):** a uniformidade é medida em 100 000 rolagens (1 000 ± 25% por entrada), e não em 20 000.
  Com 20 000 a tolerância é de 3,5 desvios, e com 21 geradores um sorteio uniforme falha em cerca de metade das
  rodadas. G = 540 deu 254 com χ² = 98,4 em 99 graus de liberdade.

## Achados corrigidos nesta iteração
- `formulas`: `AND(ISNUMBER(X),OR(X<1,INT(X)<>X))` dá #VALUE! com X = "". A forma correta é
  `IF(ISNUMBER(X),OR(...),FALSE)`. Corrigido em Sessões (combates), Improviso (rolador N e M) e Minhas Tabelas (quantos).
- Oráculo da linha do tempo: `campanha.prox.k.idx` é a posição no intervalo, que inclui o cabeçalho repetido a cada
  10 linhas (`i + (i − 1) // 10`). A planilha já estava certa; o oráculo divergia a partir do evento 11.
- Texto: "sessão(ões)" virou singular ou plural por fórmula; "a 1ª" virou "a primeira"; o formato "(cap. N)" do
  Escudo virou "(capítulo N)"; um custo da falha passou a dizer "informação incompleta", como 27.1; o subtítulo do
  Escudo dizia "4 páginas" (recorte do Exemplo) e agora diz 5. O léxico extra ganhou as palavras da Fase 3, e
  "carregue" e "macro" saíram porque ficaram sem uso.

## Iteração 2 (revisão `review-fase3.json`, 08/10 16:40)
- **F1 (bloqueante):** Campanha!E10 passou a dizer "Lida pela aba Sessões (preparação e diário) e pela Início." e
  E11 "Usado pela linha do tempo (nesta aba, mais abaixo)." (`aba_campanha.py`). O `lint_fase3` barra "Em
  construção" e "próxima fase" como substring, sem distinguir maiúsculas, em toda célula de texto ou fórmula das 18
  abas. Autoteste: no Exemplo antigo o lint acusa Campanha E10 e E11; no regenerado, 0.
- **F2:** o Exemplo de 12:51:38 foi copiado antes de regenerar e comparado célula a célula com o novo; a cópia foi
  apagada depois da comparação. As 4 318 entradas são iguais e, fora das fórmulas, as células também (só mudaram os 4
  títulos do Escudo desta iteração). Ninguém digitou nada: foi só uma regravação pelo Google Planilhas no modo Office,
  sincronizada pelo Drive, e nenhum dado do usuário se perdeu na regeneração. Suíte nova `origem`
  (`testes_base.suite_origem`), que roda no início e no fim da `fase3`: `docProps/app.xml` presente, sem
  `xl/metadata*`, área de impressão do Escudo gravada, Exemplo com as mesmas validações do modelo e os dois arquivos
  gravados até ±900 s do mapa. Sobre o arquivo regravado ela acusou 5 falhas; sobre o regenerado, 0. Com isso, uma
  regravação no meio da bateria passa a aparecer como falha.
- **F3:** cada título de página do Escudo diz o que a página tem: 1 "Preparar a sessão e o encontro; descanso",
  2 "O inimigo, a Tenacidade e o PH", 3 (igual), 4 "Pessoas: condições, Morrendo e PV temporários", 5 "Mesa: Energia,
  tetos e casos-limite". O plano 3.3 e o design §6.15 foram atualizados para 5 páginas ("página N de 5"), com o
  conteúdo de cada página.
