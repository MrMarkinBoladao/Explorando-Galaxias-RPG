# Revisão final da Fase 4: Exemplo completo, COMO-USAR e auditoria da Planilha do Mestre

A Fase 4 fecha a Planilha do Mestre. O Exemplo completa a campanha de §14, "O Lacre do Poço Sete". O COMO-USAR saiu em 12 seções. O relatório final faz o papel do AUDITORIA.md. Também entrou o pedido do usuário de Memoespírito e condições (M1–M4, C1–C6). A bateria `tudo` teve 18 suítes, 10 979 281 checagens e 0 falha. A suíte `origem` deu o mesmo resultado no começo e no fim. Recalculei os hashes de `baseline-hashes.json` depois da bateria: 50 iguais, 0 diferentes e só o ausente conhecido do P5. Os 1 332 recortes da prévia têm todos lado ≤ 1800 px. Nenhum critério de bloqueio foi atingido.

Watch for: a seção 1 do plano ainda chama o modelo de "V1.1". O entregável é "V1.2", por decisão registrada do usuário (confirmed, não bloqueia). No Exemplo, a Nadir aparece "Já agiu" na casa 4 enquanto a casa 1 está "Agindo agora", e isso contradiz o passo a passo do guia (likely, não bloqueia).

**Verdict**: APPROVED

## High-level view

Os três entregáveis estão em `Mestre\` com os nomes de `SAIDA_*`:

- `Planilha do Mestre - Explorando Galáxias V1.2.xlsx`
- `Planilha do Mestre - Exemplo.xlsx`
- `COMO-USAR-PLANILHA-DO-MESTRE.md`

O V1.2 segue a adoção do livro v1.2 pelo usuário. O pedido literal não fixa nome de arquivo, então isso não conta como nome errado. O plano é que não foi atualizado. Na pasta também ficam o `…V1.1.xlsx` antigo, o `.gsheet` do usuário e o `desktop.ini`. A suíte `entregaveis` aceita esses três e recusa qualquer outro, e o guia avisa para usar o V1.2.

R1 a R13 têm cada um a sua aba e a prova da suíte com 0 falha.

O Exemplo condiz com o pedido:

- grupo de 4: a Nadir de 29.7 mais 3 PJs iguais ao `oraculo_ficha`;
- encontro na Fila do Ciclo 2, com o Memoespírito na casa 2 e o Casco Oco 1 Congelado fora da Fila atual;
- 6 NPCs;
- 3 missões, em estados diferentes;
- sessão 2 com 5 cenas, os Encontros A e B ligados e pistas.

O único ponto fraco é o estado digitado da Fila, que vem detalhado abaixo.

O checklist de 2 minutos aponta células e valores reais. A suíte `guia` confere as 25 citações, e quatro delas (`Combate!B141`, `B142`, `A175` e `B175`) batem com os recortes. As sugestões H1–H27 estão nos dois documentos: no relatório com o erro máximo medido, e no guia com a aba onde cada uma aparece. A limitação do motor `formulas` está no relatório e no guia: o Google não foi executado, e também não foram conferidas em uso a validação de dados, a formatação condicional, a impressão real nem o IMPORTRANGE. Um detalhe de redação: o relatório diz "31 funções de `ficha_funcoes_ok.json`", mas o JSON tem 33. As 31 são o que sobra depois que a Mestre proíbe ROUND e ROUNDUP (confirmed).

<details>
<summary>Issues (3)</summary>

1. **Nome do modelo desatualizado no plano**: a seção 1 do `plano-mestre.md` e a tabela R12 ainda dizem `…V1.1.xlsx`, mas o entregável e `SAIDA_MODELO` são V1.2. Atualizar a seção 1 e citar a decisão do usuário de 07/10 (não bloqueia).
2. **Estado da Fila no Exemplo contradiz o guia**: na C9 do Combate, a Nadir (casa 4) está "Já agiu" enquanto a Tessaly (casa 1) está "Agindo agora". Marcar as casas 1–3 como já agiram, ou tirar o "Já agiu" da Nadir (não bloqueia).
3. **"31 funções" no relatório**: `ficha_funcoes_ok.json` tem 33 funções. Escrever "31 das 33 (sem ROUND e ROUNDUP)" (não bloqueia).

</details>

<details>
<summary>Details</summary>

### Nome V1.2 contra o plano

A seção 1 do plano ainda diz `Planilha do Mestre - Explorando Galáxias V1.1.xlsx` (confirmed). O usuário decidiu pelo V1.2 duas vezes: na adoção da v1.2 (`notas-fase2.md`, 07/10) e na resposta à pergunta 2 da Fase 4 (`notas-fase4.md`). Como a mensagem do usuário vale mais que o plano, isso não bloqueia. Mas o plano diz uma coisa e o disco tem outra, e quem retomar pelo plano vai procurar o arquivo errado. O `PROGRESSO.md` e o relatório explicam a troca; o plano não.

### Exemplo: Fila do Ciclo 2

```
C9  casa 1 Tessaly Varonne    20  Agindo agora
    casa 2 Eco do Construtor  17
    casa 3 KV-12, Paciência   14
    casa 4 Nadir              14  Já agiu
    ...
PENDENTES  Casco Oco 1: CONGELADO   (fora da Fila atual, volta na prevista)
```

A ordem calculada é a do oráculo (suíte `exemplo`). O estado digitado, porém, mostra a casa 4 já resolvida antes da casa 1 (likely). O guia ensina "marque Já agiu e a marca passa para o próximo", e o Exemplo é o material para aprender isso. Quem compara os dois vê um estado que o fluxo descrito não produz. Nenhum número muda.

</details>

<details>
<summary>Arquivos revisados</summary>

- `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx`: modelo em branco, 18 abas, 41 810 fórmulas.
- `Mestre\Planilha do Mestre - Exemplo.xlsx`: campanha completa, 519 entradas.
- `Mestre\COMO-USAR-PLANILHA-DO-MESTRE.md`: guia em 12 seções, checklist, H1–H27, IMPORTRANGE.
- `.agents\tasks\mestre\relatorio-final.md`, `suite-tudo.txt`, `PROGRESSO.md`, `notas-fase4.md`.
- Recortes `exemplo-combate-parte-05/06`, `exemplo-missoes-parte-01` e `exemplo-sessoes-parte-01` em `.agents\tasks\mestre\preview\`.

</details>
