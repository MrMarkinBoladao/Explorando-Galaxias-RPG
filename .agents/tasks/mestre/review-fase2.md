# Fase 2 da Planilha do Mestre, iteração 2: teto de Sobreposição do Cone e 27.9 adiado

Este é o segundo ciclo, limitado, da revisão da Fase 2 (NPCs, Aventuras e Recompensas sobre o livro v1.2). Conferi só se os achados do ciclo 1 fecharam. O F1 (bloqueante) tratava o teto de Sobreposição de 25.2 como teto do Cone, contando as de faixas anteriores. O F2 era o registro do adiamento de 27.9 para a Fase 3. Os dois fecharam (**confirmed**).

A bateria `--suite fase2` (07/10 20:59–23:23) rodou sobre as planilhas regeneradas às 19:49: 7 248 118 checagens, 0 falha. Ela inclui as suítes da Fase 1, então a Fase 1 continua sem quebra: lint 0 (0 achado do Google), `extremos` 0 nos 11 estados e nas 86 injeções de erro, `oraculo` e `determinismo` 0, bestiário 32/32, `protegidos` 165/0. Depois do início da bateria, o único arquivo alterado fora de `.agents\` foi `build\mestre_spike.json`, que a própria suíte grava. O livro e a ficha não foram tocados.

Watch for: nada bloqueante.

**Verdict**: APPROVED

## High-level view

O teto de 25.2 agora é do Cone. Na aba Grupo, G3 ganhou a entrada "Total no Cone" (coluna F, via `ent()`, inteiro de 0 a 5), coberta pela camada de leitura protegida do Google. Ela acende aviso quando o total passa do teto e quando é menor que as Sobreposições desta faixa. Em Recompensas, o quadro separa "Nesta faixa (máx. 1)", "No Cone (total)" e "Teto do Cone". A Situação compara o total com o teto antes do limite da faixa: Cone 3 com 1 anterior e Cone 1 com 2 anteriores dão "Cone no teto (+3) com as que já tem: nenhuma a mais". O total usado é `MAX(informado, desta faixa)`, e o aviso acima do teto acende nas duas abas. O `ouro` cobre esses casos e os de aviso. O oráculo sorteia o total, inclusive com texto inválido.

A decisão sobre 27.9 está no item 2.4 do plano: 27.9 só aparece no Escudo (design §6.15), e o item 3.3 cobra o caso no `ouro` da Fase 3.

<details>
<summary>Issues (0)</summary>

Nenhum achado aberto.

</details>

<details>
<summary>File map</summary>

- `build\mestre\aba_campanha.py`: G3 com a entrada `grupo.pjN.sobrep_total` ("Total no Cone") e os avisos de teto e de total menor.
- `build\mestre\aba_recompensas.py`: quadro de Sobreposições com as colunas novas, a Situação pelo total e o aviso acima do teto.
- `build\mestre\testes_hist.py`, `build\oraculo_mestre_hist.py`, `build\testar_mestre.py`: +11 casos de `ouro` da 25.2; o total entra no sorteio do oráculo.
- `plano-mestre.md` (itens 2.4 e 3.3): decisão de 27.9.
- Saídas: `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx` e `Mestre\Planilha do Mestre - Exemplo.xlsx` (19:49).
- Evidência: `.agents\tasks\mestre\suite-tudo.txt`, `PROGRESSO.md`.

</details>
