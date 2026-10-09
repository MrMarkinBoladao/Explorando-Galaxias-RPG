# Revisão da v1.1: livro corrigido pela auditoria da ficha e ficha automatizada atualizada

A v1.1 aplica no livro as 12 decisões que a auditoria da ficha levantou (D1 a D7, N1 a N5) e atualiza a ficha `.xlsx` para seguir esse texto. Também atende aos três pedidos do usuário: o bloco agora se chama "Resumo para o Jogador", nenhuma aba tem painel congelado e as células foram redimensionadas. Conferi as correções no `.md`, no `.docx` e no `.pdf`. Recalculei à mão, direto dos capítulos, 18 números da Nadir e 20 de um personagem de nível 20 (Avginiano, Caça, Armadura Pesada) e comparei com a planilha calculada pela biblioteca `formulas`: todos bateram. Também abri 8 recortes da prévia e li as abas com openpyxl.

Watch for: as alturas de linha são fixas e dimensionadas pelo aviso mais longo possível, e por isso a Criação e o Equipamento ficam muito altos no uso normal (confirmed). O teste de digitação da checklist de 2 minutos não detecta nada, porque Atletismo já é d20+6 no nível 1 (confirmed). A Ficha Exemplo usa para a Nadir uma crença diferente da que o capítulo 29.7 dá a ela (confirmed).

**Verdict**: APPROVED

## High-level view

No livro, as correções batem com as regras vizinhas. O D3 fecha com 05 e 22.6, o D4 com as três Perícias de Agilidade do capítulo 04, o D5 com a tabela do Bônus Maior de 25.2 (+1/+10 → +3/+30 nos Níveis 1 e 2, +2/+25 → +3/+35 nos Níveis 3 e 4) e o N4 com a tabela de Eficiência de 02/26.2 e com os níveis de referência de 01, 27 e 29. A forma antiga só sobrou nos dois changelogs, onde é histórica. A capa diz 1.1, os arquivos V1.1 existem na raiz e o PDF tem 253 páginas. Duas frases do texto corrido, em 01 e em 27, ainda chamam o livro de "v1.0" (confirmed).

Na ficha, os números que a v1.1 mudou batem com o livro: dano 1d12+6 (12) da Nadir; -2 da Pesada em Reflexos e nas Perícias de Agilidade e nunca no ataque (d20+16); Esquiva proibida; Morrendo com Vantagem para o Avginiano; Perícias escolhidas fixadas pela Sincronia da criação (3, mesmo com a Sincronia final em +2). As 10 suítes saem com 0 falha. Os 12 itens da checklist apontam para células e valores reais do mapa atual. O que falha é o teste de digitação no fim da checklist.

Os pedidos do usuário foram atendidos na horizontal. As 10 abas dos dois arquivos têm `freeze_panes` e `pane` vazios. "Mestre" aparece só em regra do livro ou em nome de Bênção ("Mestre das Aflições"). A1 da Em Jogo diz "Resumo para o Jogador", e A:L cabe em 1360 × 760. A falha é vertical: as linhas da Criação e do Equipamento têm altura fixa, dimensionada para o aviso mais longo possível, e ficam quase vazias no uso normal. A suíte `visual` só procura colunas largas demais. Ela não mede linhas altas demais.

<details>
<summary>Issues (6)</summary>

1. **Linhas altas demais no uso normal** (confirmed, não bloqueia) — as linhas da Criação e do Equipamento têm 71 a 150 pt e ficam quase vazias numa ficha comum. Dimensionar a altura pelo conteúdo típico e deixar o aviso longo quebrar dentro da célula (ou alargar a coluna de aviso). Incluir na suíte `visual` um alerta para linha com mais que o dobro da altura usada.
2. **Teste de digitação da checklist não detecta nada** (confirmed) — Testes!I16 já mostra d20+6 no nível 1. Trocar o teste por "mude B8 para 4 e veja Testes!I16 virar d20+7" (Eficiência +3).
3. **Crença da Nadir diferente do livro** (confirmed) — a Criação!B22 da Ficha Exemplo tem "Eu não deixo ninguém para trás, nem inimigo", que é o exemplo genérico de 05. O 29.7 dá à Nadir "eu não assino nada que eu não consertei". Trocar em `build\testar_ficha.py` (`entradas_nadir_exemplo`) e regerar.
4. **Livro ainda se chama "v1.0" no texto corrido** (confirmed, opcional) — 27 ("Esta v1.0 é o livro de regras") e 01 ("a v1.0 foi varrida") falam da v1.0 como se fosse a versão atual. Trocar por "este livro" ou deixar claro que é histórico.
5. **Duas frases imprecisas na AUDITORIA** (confirmed) — a seção 3.1 cita o cabeçalho `F15`, mas "Equipamento" está em `G15` (F15 é "Do atributo"). A 8.4 diz que as 51 colunas largas "ficam para a auditoria final", e este já é o documento final. Corrigir as duas.
6. **Arquivos de retomada obsoletos** (confirmed) — as seções 2, 3 e 8 do `HANDOFF-RETOMADA-v1.0.md` ainda dizem que a ficha está "quase pronta" e que a `suite-tudo-v11.txt` está incompleta. `.agents\tasks\tmp_checklist.py` e `.txt` guardam um layout antigo (Em Jogo B16/C16, Criação D93). Atualizar o handoff e apagar os temporários na limpeza final.

</details>

<details>
<summary>Details</summary>

### Números conferidos à mão

Nadir (29.7): PV 61, Defesa 16, Esquiva 18, RD 0, VEL 14, DT 14, bônus +4/+1/+2/-1/+1/+0, Perícias 2 escolhidas e 5 com Eficiência, ataque d20+6, dano 1d12+6 (12), contra Fraqueza 3d12+6 (25), Rebarba 6d6+4 (25) com d20+6, 1 PH e RT 2, Ultimate 5d10+4 (31), Espaço 18 e os 6 Testes de Resistência d20+6/3/4/1/3/2.

Nível 20: Avginiano da Caça, array 15/14/13/12/10/8, Agilidade como Atributo de Habilidade, seis aumentos (Vigor no 9 e no 12), Pesada e Disparo longo. O livro dá PV 234 (`25 + 10 + 9` + `19 × 10`, pela equivalência de 4.3), Defesa 21, Esquiva proibida, RD 2, VEL 17, DT 21, ataque d20+16, dano 5d10+5, Reflexos, Acrobacia, Furtividade e Pilotagem d20+11 (com o -2), Percepção Mental d20+11 e Força de Vontade d20+8 com Vantagem, Morrendo com Vantagem (23.5), 3 Perícias permitidas, Espaço 10 e Ultimate 14d20+5 (152). A planilha dá os mesmos valores.

### Alturas de linha fixas pelo pior caso

O gerador escolhe a altura das linhas pelo texto mais longo que o aviso da coluna L consegue montar. A altura fica gravada no `.xlsx` e não se ajusta ao conteúdo depois, então vale em qualquer estado:

```
Criação 44-50 (atributos)   71 pt cada  → ~95 px por linha com um número
Criação 69-88 (Perícias)    37 pt cada
Equipamento 8 (secundária) 150 pt       → ~200 px
Equipamento 9, 20, 23       93-94 pt
Criação inteira            ~4000 pt em 126 linhas
```

No recorte da Nadir, a tabela de atributos ocupa cerca de 570 px e as 18 Perícias cerca de 880 px. Nada fica cortado e a regra das 15 linhas é cumprida, mas o jogador rola bem mais do que o conteúdo pede (confirmed). A Em Jogo não tem o problema.

### Teste de digitação da checklist

O teste final pede nível 3 e espera d20+6, mas a Eficiência é +2 do nível 1 ao 3. A célula não muda, e o teste passa mesmo com o recálculo quebrado (confirmed).

</details>

<details>
<summary>Arquivos revisados</summary>

- `livro-v1.0\00-capa-e-creditos.md`, `03`, `04`, `07` a `11`, `18`, `21` a `26`, `29` e `30`: as correções D1 a D7, N1, N2 e N4.
- `livro-v1.0\00-changelog-v10-para-v11.md`: o changelog novo.
- `Sistema de HSR by MC Filhos V1.1.docx` / `.pdf`: o livro montado (capa 1.1, 253 páginas, correções presentes nas tabelas).
- `ficha-automatizada\*.xlsx`, `AUDITORIA-DA-FICHA.md` e `COMO-USAR-NO-GOOGLE-PLANILHAS.md`: a ficha e os documentos dela.
- Diff completo em `.agents\tasks\diff-v10-v11.md`. Saída das suítes em `.agents\tasks\suite-tudo-v11.txt`.

</details>
