# Ficha V1.1 revisão 2: blindagem contra o Google ler entrada como fórmula

A revisão 2 trata a causa dos 261 `#ERROR!` que o usuário viu no Google: a opção "+1 em dois" do Humano, lida como fórmula, quebrava Criação!B26 e o erro se espalhava. Agora nenhuma opção de lista começa com sinal, toda entrada lida por fórmula passa por uma leitura protegida (`IF(ISERROR(x),"",IF(ISBLANK(x),"",x))`), cada linha ganhou um aviso `ISERROR` e a Início conta as células com erro (B19). Tudo foi conferido com scripts próprios (openpyxl + formulas), sem usar o lint nem as suítes do coder.

Watch for: nada bloqueante; só dois pontos de baixa severidade (arquivo e texto da AUDITORIA).

**Verdict**: APPROVED

## High-level view

Nenhuma das 196 listas oferece uma opção que o Google vá ler como fórmula, número, data, hora, percentual ou booleano. Isso vale para as 4 listas literais, as 35 fontes por intervalo e as 5 fontes dependentes, calculadas em 29 cenários. Nas 358 entradas, as fórmulas só chegam ao valor bruto pela leitura protegida ou por um `ISERROR`. Por isso um erro injetado não se espalha, e o contador da Início marca 1.

Os números batem com o Google e com o livro. Recalculada pelo `formulas`, a ficha confere com os valores em cache da Cópia em todas as 30 células da amostra. A Nadir confere com o capítulo 29.7. O caso do usuário dá 0 erro e +1 em Poder e Agilidade.

<details>
<summary>Issues (2)</summary>

1. **Cópia fora da pasta `ficha-automatizada`** (low, confirmed): a "Cópia de Ficha…" não está em `ficha-automatizada\`, e já faltava antes desta etapa (plano-mestre P5/A2). O backup é idêntico byte a byte ao hash da linha de base (SHA-256 941E34…), então nada se perdeu. Se o usuário quiser o arquivo de volta na pasta, é só copiar do backup.
2. **Tempo da bateria contraditório** (low, confirmed): a seção 7 da AUDITORIA diz "uns 22 minutos" (revisão 2) e, logo depois, "uns 11 minutos". Basta deixar só o número da revisão 2.

</details>

<details><summary>Details</summary>

### Opções de lista e listas dependentes

Meu script leu cada `dataValidation` do tipo lista. Separou os itens das listas literais, resolveu os intervalos da Dados e testou cada valor contra o mesmo critério: começa com `= + - @`, tem espaço nas pontas, ou parece número (inclusive `1,5`, `R$` e `%`), data (`d/m`, `d-m-a`, "3 de mar"), hora ou booleano (TRUE/FALSE/VERDADEIRO/FALSO). Valor não textual também conta como problema. Resultado: 0.

As 61 células-fonte das listas dependentes passaram por duas checagens. A primeira, estática, olhou os literais das fórmulas e as 12 faixas da Dados que elas leem. A segunda calculou as fontes com o `formulas` em 29 cenários: em branco, cada uma das 7 Raças, os 2 modos do Humano, os 9 Caminhos e as 10 opções de Equipamento!B20. Saíram 0 valor-armadilha e 0 erro.

Nenhuma lista dependente fica vazia quando o pai está escolhido. As únicas faixas vazias aparecem quando a lista nem se aplica: Y21:Y38 fica vazia para as 8 opções de B20 que não são "Um Teste de Resistência" nem "Uma Perícia".

### Contenção

Pela análise estática das referências (Tokenizer), são 987 leituras protegidas e 716 `ISERROR`, e nenhuma outra fórmula lê uma entrada diretamente. As 29 entradas sem leitura protegida (nome do jogador, conceito, nomes de Cone e Relíquia…) são lidas só pelos sinais `ISERROR`.

Partindo das 42 entradas da Nadir, injetei um erro em cada uma de 5 entradas: Criação!B26, Equipamento!B20 (lista), Equipamento!B18 (texto livre), Em Jogo!F2 (número) e Criação!B8 (Nível). Nas 5, só a própria entrada ficou com erro, e Início!B19 marcou 1.

Também testei a armadilha da validação. Todas as 299 validações estão em modo "warning", e o Google aceita o valor inválido. Com "abc" em B8, F2, B44 e Equipamento!C60, ou com "5 " em B8, a ficha dá 0 erro e o Painel de avisos (B18) marca 1. O contador da Início cobre exatamente a área usada de cada aba.

### Fidelidade com o Google e números do livro

A suíte `google` passou com 2.363 de 2.363 células iguais. Repeti a comparação por conta própria. Tirei da Cópia as 4 entradas preenchidas (nome, jogador, Compra de Pontos, Haloviano) e calculei a revisão 2 com elas. Depois comparei uma amostra aleatória (semente 20261005) de 30 células, 20 numéricas e 10 de texto, com o cache do Google, e as 30 bateram. A amostra cobre todas as abas, menos a Dados.

O caso do usuário (Humano + "Dois Atributos (+1 cada)" + Poder + Agilidade) dá 0 erro, B19 = 0, C44:C49 = 1, 1, 0, 0, 0, 0 e avisos K25:K28 vazios.

Para a Nadir, comparei os números da ficha com as contas abertas do capítulo 29.7, todos iguais: PV 61 (25 + 5×6 + 3×2), Defesa 16 (10+1+5), Esquiva 18 (16+2), Velocidade 14 (10+1+1+2 das Botas I), DT 14 (8+4+2), ataque de Habilidade +6 e Ataque Básico 1d12+6 com média 12.

### Entregáveis

O `COMO-USAR` tem a seção 1.1 com a dica do apóstrofo. O passo 4 confere o B19, a checklist confere B18 e B19 em 0, e há um passo novo para testar o Humano +1/+1. O backup em `backup-usuario-0410\` está intacto (veja o achado 1).

</details>

<details>
<summary>Arquivos conferidos</summary>

- `ficha-automatizada\Ficha Automatizada - Explorando Galáxias V1.1.xlsx`: validações, fórmulas e cálculo
- `ficha-automatizada\Ficha Exemplo - Nadir.xlsx`: entradas da Nadir
- `ficha-automatizada\COMO-USAR-NO-GOOGLE-PLANILHAS.md`: dica e checklist
- `ficha-automatizada\AUDITORIA-DA-FICHA.md`, seção 11
- `.agents\tasks\suite-tudo-rev2.txt`: 11 suítes OK, código 0
- `.agents\tasks\backup-usuario-0410\`: exports do Google

</details>
