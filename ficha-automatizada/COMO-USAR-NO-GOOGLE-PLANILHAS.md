# Como usar a ficha no Google Planilhas

Explorando Galáxias · livro **v1.2** · níveis 1 a 20

Nesta pasta:

| Arquivo | Para quê |
|---|---|
| `Ficha Automatizada - Explorando Galáxias V1.2.xlsx` | O modelo em branco. Cada jogador faz a ficha dele a partir deste |
| `Ficha Exemplo - Nadir.xlsx` | O mesmo modelo já preenchido com a Nadir do exemplo do capítulo 29.7. Serve para conferir se a importação deu certo e para ver uma ficha pronta |

A ficha não tem macro nem script: é só fórmula. Preencha as células **amarelas** e o resto se calcula sozinho.

---

## 1. Abrir no Drive

1. Envie o `.xlsx` para o seu Google Drive (arrastar para a janela do Drive funciona).
2. Clique com o botão direito no arquivo → **Abrir com** → **Planilhas Google**.
3. No Planilhas: **Arquivo** → **Salvar como Planilhas Google**. Use essa cópia nova. O `.xlsx` original continua no Drive como estava.
4. Abra a aba **Início** e confira o **Painel de avisos**: com a ficha em branco ele mostra **0** avisos. Logo abaixo, **Células com erro na ficha** (B19) também precisa mostrar **0**.

## 1.1 Não comece um texto com +, - ou =

O Google entende como **fórmula** tudo que você digita começando com `+`, `-`, `=` ou `@`. Um efeito de Habilidade como `+1d6 de Fogo` vira `#ERROR!` na hora. Se o texto precisar começar assim, digite um **apóstrofo** antes: `'+1d6 de Fogo`. O apóstrofo não aparece na célula.

A ficha se protege disso de dois jeitos:

- **Nenhuma opção de lista começa com esses sinais.** Os bônus aparecem assim: **Um Atributo (+2)** e **Dois Atributos (+1 cada)** (bônus do Humano e Aumentos de Atributo), **Um tipo de rolagem +1**, **Velocidade +1**, **Dano +2** e **RD +1** (bônus de 2 peças dos Conjuntos) e **Velocidade +1** (Ressonância I).
- **O erro não se espalha.** Se uma célula amarela ficar com `#ERROR!`, só ela fica assim: o resto da ficha continua calculando como se ela estivesse vazia, e o aviso da linha diz *"O Google leu como fórmula: ..."*. Na aba **Início**, **Células com erro na ficha** conta as células com erro e a linha de baixo mostra em qual aba elas estão. Para consertar, apague a célula e escreva de novo com `'` na frente, ou escolha de novo na lista.

A aba **Dados** guarda as tabelas do livro que as fórmulas leem. Pode escondê-la (botão direito na aba → **Ocultar página**), mas **não apague**.

## 2. Uma cópia para cada personagem

Faça o passo 1 uma vez com o modelo em branco e guarde essa versão limpa. Para cada personagem novo:

1. Abra o modelo limpo → **Arquivo** → **Fazer uma cópia**.
2. Dê à cópia o nome do personagem. Se quiser que o Mestre acompanhe a ficha, compartilhe com ele (**Compartilhar** → e-mail → **Leitor**).

Assim você mexe só na ficha do personagem, e o modelo continua limpo para o próximo.

## 2.1 Como a ficha se organiza na tela

- **Sem linhas congeladas, de propósito.** Nenhuma aba trava linhas ou colunas. Em vez disso, cada tipo de célula tem um visual próprio, e a parte que você usa de cada aba cabe em 1360 px de largura (não precisa rolar para o lado). Tabelas longas repetem o cabeçalho, e nenhuma linha fica a mais de 15 linhas dele (as Perícias vêm em 3 grupos de Atributos; a tabela mestra da Progressão, em 2 partes de 10 níveis).
- **Resumo para o Jogador** (aba **Em Jogo**, A1:D12): o seu personagem numa olhada (PV, Defesa, RD, VEL, DT, melhor ataque, condições). A linha 13 mostra quantos avisos a aba tem e o primeiro deles; a lista inteira fica na coluna N.
- Colunas auxiliares (valores de apoio das listas) ficam **ocultas**. Não precisa mexer nelas.

Legenda de estilos (aparece no topo de cada aba):

| Estilo | Como aparece |
|---|---|
| Entrada (preencha) | fundo amarelo-claro, borda dourada |
| Calculada (automático) | fundo azul-claro |
| Aviso | texto vermelho-escuro em negrito; fundo rosa quando há aviso |
| Título de bloco | faixa azul-escura, texto branco |
| Cabeçalho de coluna | fundo azul-médio, texto azul-escuro em negrito, borda inferior grossa |
| Rótulo da linha | 1ª coluna em negrito, com borda grossa à direita |
| Linha alternada | linhas pares da tabela num tom mais escuro do mesmo tipo |
| Não se aplica | fundo cinza |

A cor nunca é o único sinal: os cabeçalhos dizem "(preencha)" ou "(automático)" e os avisos são texto.

## 3. Proteger as fórmulas (modo "Mostrar um aviso")

A proteção nativa do Google não usa senha e não atrapalha o jogador: ela só pergunta antes de alguém apagar uma fórmula sem querer.

1. **Dados** → **Proteger páginas e intervalos** → **Adicionar uma página ou um intervalo**.
2. Escolha **Página** e a aba (por exemplo, **Em Jogo**). Marque **Exceto certas células** e adicione os intervalos das células amarelas daquela aba, para elas ficarem livres.
3. **Definir permissões** → **Mostrar um aviso ao editar este intervalo** → **Concluído**.
4. Repita para as outras abas que quiser. Na aba **Dados**, proteja a página inteira (ela não tem entrada).

Quem tentar editar uma célula azul (calculada) recebe um aviso e pode cancelar.

## 4. Opcional: trocar as listas Sim/Não por caixas de seleção

Várias entradas são listas com **Sim** e **Não** (Eficácia na aba Testes, "Possui" nas Relíquias, Memoespírito ativo na Em Jogo). As fórmulas comparam com o texto "Sim", então a caixa de seleção precisa gravar esse texto:

1. Selecione o intervalo, por exemplo **Testes!E16:E20**, **E22:E29** e **E31:E35** (Eficácia nas 18 Perícias; pule as linhas 21 e 30, que são cabeçalho), **Testes!E40:E45** (Eficácia nos 6 Testes de Resistência) ou **Equipamento!B36:B41** (Relíquias que você possui).
2. **Inserir** → **Caixa de seleção**.
3. Ainda com o intervalo selecionado: **Dados** → **Validação de dados** → clique na regra → em **Critérios**, marque **Usar valores de célula personalizados**: **Marcada = Sim**, **Desmarcada = Não** → **Concluído**.

Sem o passo 3 a caixa grava VERDADEIRO/FALSO e a ficha deixa de contar aquela linha. Se der errado, **Editar** → **Desfazer** volta a lista original.

---

## 5. Checklist de 2 minutos (com a Ficha Exemplo - Nadir)

Importe `Ficha Exemplo - Nadir.xlsx` como no passo 1 e confira estas células. Todas batem com a Nadir do capítulo 29.7 do livro v1.2, e todas foram confirmadas pela bateria de testes (suíte `ouro`). Se uma delas mostrar outra coisa, a importação mudou alguma fórmula: refaça a importação (passo 1) antes de usar a ficha.

| # | Onde | Deve mostrar | No livro (29.7) |
|---|---|---|---|
| 1 | aba **Início**, células **B18** (Painel de avisos, Total) e **B19** (Células com erro na ficha) | **0** e **0** | — |
| 2 | aba **Em Jogo**, célula **B3** | Humano · A Destruição · nível 1 | Raça, Caminho e nível |
| 3 | aba **Em Jogo**, célula **B5** | **61 / 61** | PV 61 |
| 4 | aba **Em Jogo**, célula **B6** | **16 · Esquiva 18** | Defesa 16, Esquiva 18 |
| 5 | aba **Em Jogo**, célula **B7** | **RD 0 · VEL 14** | VEL 14 com Botas I |
| 6 | aba **Em Jogo**, célula **B8** | **14 · ataque de Habilidade d20+6** | DT 14 |
| 7 | aba **Em Jogo**, célula **C16** | **d20+6** | Teste de Ataque da marreta +6 |
| 8 | aba **Em Jogo**, células **D16** e **E16** | **1d12+6** e **12** | `1d12 + 4 + 2` = `1d12 + 6`, 12 médio (com Mãos I) |
| 9 | aba **Em Jogo**, células **F16** e **G16** | **4** e **2** | +4 do Poder e +2 da Relíquia de Mãos I |
| 10 | aba **Em Jogo**, células **A19**, **C19** e **D19** | Rebarba · d20+6 · 6d6+4 (25) | Rebarba, Nível 1, `6d6 + 4` |
| 11 | aba **Habilidades**, células **D61** e **E61** | **5d10+4** e **31** | A Doca Inteira, `5d10 + 4` |
| 12 | aba **Equipamento**, célula **B56** | **18** | Inventário `10 + (2 × 4)` = 18 |

Depois, um teste de digitação: na aba **Criação**, célula **B8** (Nível), troque 1 por 4 e veja **Testes!I16** (Atletismo) virar **d20+7**, porque a Eficiência sobe de +2 para +3 no nível 4 (capítulo 02). Volte o nível para 1.

Por último, o teste da lista do Humano (foi aqui que a revisão 1 quebrava): na aba **Criação**, escolha **B25** = Humano, **B26** = **Dois Atributos (+1 cada)**, **B27** = Poder e **B28** = Agilidade. Confira **C44** (Poder) e **C45** (Agilidade) mostrando **1**, e **Início!B19** (Células com erro na ficha) em **0**. Desfaça (Ctrl+Z) para voltar à Nadir.

## 6. Se algo der errado

- **Uma célula amarela mostra `#ERROR!`:** o Google leu o que você digitou como fórmula (começou com `+`, `-` ou `=`). Apague e digite de novo com um apóstrofo (`'`) na frente, ou escolha de novo na lista. O contador **Início!B19** volta a 0.
- **Uma célula azul mostra `#ERROR!` ou `#REF!`:** alguém apagou ou colou por cima de uma fórmula. **Arquivo** → **Histórico de versões** recupera a versão anterior. A proteção do passo 3 evita que isso aconteça de novo.
- **Apareceu texto vermelho em fundo rosa:** é um aviso da ficha, não um erro. Ele diz qual regra do livro não fechou (por exemplo, Perícias a mais ou Bênção acima do slot). A aba Início lista quantos avisos há em cada aba.
- **Números com ponto em vez de vírgula dentro de um texto** (ex.: "itens 4.5"): é só a exibição. O número da célula ao lado está certo.
