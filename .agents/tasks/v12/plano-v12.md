# Plano v1.2 — auditoria de opções-armadilha e contradições de obrigatoriedade

Raiz: `g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG`

Origem: o usuário montou uma arma de **Energia** (2d8, Longa, Sincronia) com Elemento **Raio** e perguntou por que escolheria a propriedade **Recarga**, que só traz desvantagem. Ele está certo. Daí o pedido: varrer o livro procurando "nada assim de novo", subir para a v1.2, regerar PDF e ficha.

## Confirmação de intocáveis

- **`Explorando Galáxias RPG - Players\`** — nada será lido, criado, modificado ou apagado. Tratada como inexistente em todas as etapas.
- **`versões antigas\`** — nada será tocado.
- Entregáveis **V1.1 ficam intactos**: `Sistema de HSR by MC Filhos V1.1.pdf`, `...V1.1.docx`, `Modelo para copia - Ficha players - Explorando Galáxias V1.1.gsheet`, `ficha-automatizada\Ficha Automatizada - Explorando Galáxias V1.1.xlsx`. Os novos saem **ao lado** com `V1.2`. Mesma política que a v1.1 usou com a v1.0.
- **Não existe git aqui** (sem `.git`, sem branch, sem worktree). Edição direta no lugar; nenhum comando git.
- A pasta `livro-v1.0\` **não é renomeada** (nome legado; `testar_ficha.py:76` documenta isso).

---

## 1. Lista real de capítulos (`livro-v1.0\`, 34 arquivos `.md`)

Levantada com `Get-ChildItem`, não presumida.

`00-capa-e-creditos` · `00-changelog-v01-para-v10` · `00-changelog-v10-para-v11` · `01-introducao` · `02-como-jogar` · `03-criacao-de-personagem` · `04-atributos-e-pericias` · `05-racas` · `06-caminhos-visao-geral` · `07-caminho-destruicao` · `08-caminho-inexistencia` · `09-caminho-harmonia` · `10-caminho-abundancia` · `11-caminho-recordacao` · `12-caminho-erudicao` · `13-caminho-euforia` · `14-caminho-caca` · `15-caminho-preservacao` · `16-habilidades` · `17-ultimate-e-energia` · `18-combate` · `19-fila-de-acao-e-velocidade` · `20-elementos-tenacidade-e-quebra` · `21-condicoes` · `22-testes-de-resistencia` · `23-dano-cura-e-morte` · `24-equipamentos` · `25-cones-de-luz-e-reliquias` · `26-progressao-e-ressonancias` · `27-guia-do-mestre` · `28-bestiario` · `29-apendices-e-fichas` · `30-glossario`

Fora da auditoria: os **dois changelogs** (registro histórico) e o **`28-bestiario`** (inimigo não é escolha de jogador; a recarga em Ciclos de lá está correta). `29` e `30` entram só para consistência com o que mudar.

**Correção de numeração do brief:** o passo a passo "Para criar uma arma" e a tabela de checagem do Mestre estão em **24.7**, não em 24.5. A **24.5 é "Créditos: preços de referência"** — e `ficha_dados.verba()` depende disso (lê `## 24.5` pela coluna "Faixa de nível"). Este plano usa a numeração real.

---

## 2. Tabela preliminar de achados

Defeito **A** = opção-armadilha (só custo, ou dominada por outra opção da mesma lista). Defeito **B** = contradição de obrigatoriedade/limite. Regra de julgamento: **custo não é defeito**; ausência de contrapartida é.

| # | Local | Frase (verbatim) | Def. | Sev. | Correção proposta |
|---|---|---|---|---|---|
| **A1** | `24-equipamentos.md` §24.2 | `\| **Recarga** \| Precisa de uma **Ação Complementar** para recarregar depois de um número de disparos definido na criação \|` | A | **Alta** | **Remover a linha.** As outras quatro entregam algo (Arremessável: alcance acima do normal; Alcance estendido: um passo acima; Peso de impacto: +1 RT; Dissimulada: 0,5 de Espaço + passa por busca). Recarga é a única estritamente pior que não escolher nada. Ver §3. |
| **B1** | `24-equipamentos.md` §24.7 | `3. Escolha **uma** propriedade especial.` | B | **Alta** | `Escolha **até uma** propriedade especial — ou nenhuma.` Contradiz 18.7 ("no máximo" / "até uma"), a própria 24.2 ("Uma propriedade especial, no máximo"), a tabela de checagem de 24.7 ("Tem mais de uma? Máximo uma") e 27.9. A ficha já concorda com "até uma": a lista suspensa começa em `"Nenhuma"` (`ficha_dados.py:939-940`). Ajustar também o Resumo do capítulo (`mais **uma** propriedade especial`). |
| **B2** | `18-combate.md:262` | `Exemplos: recarga, arremessável, duas mãos, alcance um passo acima do normal da categoria, ou **+1 de Redução de Tenacidade**.` | A+B | **Alta** | Lista desalinhada de 24.2 e com dois defeitos próprios: "recarga" (A1) e **"duas mãos"**, que é puro custo — nada no livro dá benefício por mão livre (grep de `duas mãos`, `uma mão`, `arma secundária`, `empunh` em todos os `.md`: não há escudo, não há ataque com a mão secundária, não há regra de empunhadura). Reescrever apontando as 4 propriedades reais de 24.2, pelos nomes, sem inventar exemplo novo. |
| **A2** | `20-...-quebra.md` §20.5 + §20.1, com `21-condicoes.md` §21.2 | §20.5 Raio `1d6 + Eficiência` × Fogo `2d6 + (2 × Eficiência)`; §21.2 Choque `1d6 + Eficiência` 2 turnos acúmulo até 5 × Queimadura `2d6 + Eficiência` 2 turnos acúmulo até 5 | A | **Alta** | **Raio é estritamente dominado por Fogo:** Dano de Quebra menor e Dano Contínuo menor, com **duração e acúmulo idênticos** e nenhuma compensação de controle. A hierarquia de §20.1 ("Físico e Fogo pagam em dano; Gelo, Quântico e Imaginário pagam em controle") **não aloca o Raio em grupo nenhum**, e "Choque — dano contínuo confiável" promete um diferencial que a mecânica não entrega. Elemento é escolha permanente de jogador e sem custo diferenciado (§20.1), logo é defeito A. **Correção mexe em número de balanceamento: NÃO aplicar sem confirmação.** Ver §2.1. |
| **A3** | `05-racas.md`, Avginiano × Xianzhouíta | Avginiano `**+2 em Discernimento**` + Vantagem em Resistência Mental, Percepção Mental e Força de Vontade. Xianzhouíta `**+2 em Vigor ou Sincronia**` + `Vantagem em qualquer Teste de Resistência` + `não pode ser Executado` | A | **Alta** | **Avginiano é estritamente dominado:** bônus de atributo menos flexível (fixo × escolha de dois) e Vantagem que é **subconjunto próprio** (3 dos 6 TR × todos os 6), sem nada que o Xianzhouíta não tenha, mais a imunidade à Execução de brinde. Contradiz a abertura do capítulo ("**Nenhuma Raça é melhor que outra**"). A justificativa impressa do Xianzhouíta ("paga por isso não tendo nenhum traço ativo") **não diferencia os dois**: o Avginiano também não tem traço ativo. **Correção mexe em traço racial: NÃO aplicar sem confirmação.** Ver §2.1. |
| **B3** | `17-ultimate-e-energia.md` §17.4 passo 2 e §17.3 | `**Escolha o Tipo:** dano, cura, buff, debuff ou **controle**.` / `**Efeitos de buff, debuff e controle**` | B | Média | "Controle" **não existe** na lista de Tipos, fechada em §16.1 (`Dano, Cura, Buff, Debuff ou Passiva`) e §16.8. A lista de 16.1 é **lida pela ficha** (`testar_ficha.py:1197-1198` extrai `tipos_habilidade` da linha "Tipo" de 16.1), então divergir aqui é divergir do que a planilha valida. Correção de texto: usar os Tipos de 16.1 e dizer que o efeito de controle é o "aplica 1 condição" das linhas de 16.5. |
| **A4** | `25-cones-...md` §25.2 | Nível 4 `+2 **e** +25 PV` · Nível 5 `+3 **ou** +50 PV` | A | Média | Progressão **não monotônica**: trocar um Cone de Nível 4 por um de Nível 5 pode **piorar** a ficha (perde o +25 PV, ou perde o +2). Quem supõe "Nível maior é melhor" cai numa troca ruim. Correção **só de texto, sem mexer em número**: §25.1 já diz "**pode** trocar o Cone" — tornar explícito em 25.2 que a troca é opcional e que um Cone de Nível menor com Sobreposição pode valer mais que um de Nível maior (o que a própria seção de Sobreposição já implica). |
| **B4** | `26-progressao-...md` §26.7 | cabeçalho `\| Ressonância \| Nível \| Escolha uma opção \|` | B | Baixa | Só **I** e **IV** têm duas opções; **II** e **III** têm uma só. O cabeçalho promete escolha onde não há. Trocar o cabeçalho por "O que ela dá" e manter o "ou" dentro de I e IV. |
| **B5** | `26-progressao-...md` §26.7, Ressonância IV | `**ou** sua Bênção **Avatar** afeta **um alvo adicional**` | A | Baixa | Opção morta para quem não tem a Bênção **Avatar** (capstone da Recordação, cap. 11) — e a escolha é permanente ("feita na hora… e **não muda** depois"). Acrescentar a condição "…se você tiver a Bênção **Avatar**". |
| **B6** | `16-habilidades.md:267` | `\| Condição de recarga \| Opcional \| Só se você quiser trocar custo por frequência \| — \|` | B | Média | **Esta linha está correta e NÃO se remove** (tem contrapartida declarada). O defeito é que ela é **órfã**: nenhuma seção define o que é "condição de recarga" de Habilidade nem a régua da troca. Correção: uma frase em 16.5 ou 16.7 dizendo o que a troca permite. **Não confundir** com a propriedade de arma (A1) nem com a recarga em Ciclos dos inimigos (cap. 28) — as duas últimas são outras coisas, e as do cap. 28 estão corretas. |

### 2.1 Os dois achados que exigem decisão do usuário

**A2 (Raio) e A3 (Avginiano)** são defeito A legítimo — exatamente a classe pedida — mas **a correção muda o que o jogador vê e como o sistema se comporta**: A2 mexe em número de balanceamento, A3 em traço racial. O pedido também diz "não transforme isso em rebalanceamento geral" e "não reescreva o que já funciona".

**Procedimento:** o implementador **relata e não aplica**. Chama `send_message` com severidade `warning` descrevendo achado, correção mínima, efeito visível e alternativa que preserva o comportamento, e **espera a resposta**. Enquanto não houver resposta, A2 e A3 ficam fora do livro e os demais itens seguem. Opções a oferecer:

- **A2 opção 1 (só texto, zero impacto):** corrigir a descrição de §20.1 para não prometer diferencial inexistente e declarar o Raio no grupo de dano, um degrau abaixo de Físico/Fogo. Honesta, mas o Raio continua dominado.
- **A2 opção 2 (um número):** Choque com duração **3 turnos** em vez de 2 (§21.2 e §21.5) — é o que "dano contínuo confiável" significa: menos por tique, por mais tempo. O Dano de Quebra fica intacto.
- **A3 opção 1 (só texto):** remover a afirmação "Nenhuma Raça é melhor que outra" e assumir que o Avginiano é a versão de bônus fixo. Não corrige a dominância.
- **A3 opção 2 (local):** tornar o bônus do Avginiano uma escolha (`+2 em Discernimento **ou** Presença`), que é o padrão de 4 das 7 Raças, ou dar-lhe um segundo traço pequeno.

**Recomendação:** A2 opção 2 e A3 opção 2 — as de menor alcance que de fato resolvem a dominância. **Nenhuma entra sem o "sim" do usuário.**

### 2.2 O que a varredura ainda tem de cobrir

Os achados acima vieram da leitura integral de 16, 17, 20, 21, 24, 25 e `05-racas`, das seções 18.5-18.8 e 26.7, e de greps de obrigatoriedade/limite em todos os `.md`. **Falta varrer com a mesma régua** (item 1 do §5):

- `16-habilidades.md` **linha por linha de 16.5** (Buff/Debuff 1-7 e Passivas 1-7), efeitos extras, custo em PH, níveis — foco explícito do usuário. Checar se alguma linha é dominada pela de nível inferior.
- Os **9 capítulos de Caminho** (07-15), 12 Bênçãos cada ≈ 108 Bênçãos, mais as escolhas internas ("escolha um Elemento" 07:74, "escolha um tipo de rolagem" 09:73, "uma das três Memórias" 11:88, "uma das duas formas" 11:171, a Função do Memoespírito 11:225, a Técnica Auxiliar 11:264). Maior bloco de escolha do livro, ainda não auditado.
- `03`, `04`, `06` — distribuição de atributos, perícias escolhidas, perícias de Caminho.
- `19`, `22`, `23` — Avanço/Atraso, os 6 TR, escolhas em PV 0/Morrendo/Execução.
- `26` — Eficácia (quais slots escolher) e os três tetos.
- `27` §27.9 e §27.10 — confirmar que nenhum limite numérico divergiu do capítulo dono.

Regra de corte, repetida porque é o que mantém a tarefa no tamanho pedido: **só entra no relatório opção sem lado bom ou contradição de obrigatoriedade/limite.** Não é rebalanceamento, não é revisão de estilo, não é reescrita do que funciona.

---

## 3. Decisão sobre Recarga, com justificativa

**Decisão: remover `Recarga` da tabela de propriedades de 24.2 e reclassificá-la como sabor narrativo sem custo mecânico**, deixando explícito que descrever a arma como "precisa recarregar" é estética, é de graça e **não consome** a propriedade especial.

### Por quê não dar a ela uma contrapartida

A restrição dura: nenhuma propriedade aumenta os **dados base** ("esse número é o orçamento de dano do jogo e não se negocia por sabor") e a checagem de 24.7 proíbe propriedade que "dá bônus numérico em combate" ou "dá ação, Reação, Avanço ou Atraso". Sobram quatro moedas — e **as quatro já estão gastas ou não valem nada**:

| Moeda | Por que não serve |
|---|---|
| **Alcance** | Já é de **Arremessável** e de **Alcance estendido**. Qualquer ganho duplica uma das duas. |
| **Espaço** | Já é de **Dissimulada**, e de um jeito que **domina** qualquer alternativa: ela fixa o Espaço em **0,5**, então numa arma de 2 de Espaço (Pesada, Disparo longo, Energia — justamente as que recarregam) nenhum desconto chega perto. |
| **Redução de Tenacidade** | É de **Peso de impacto**, e é bônus numérico em combate: proibido criar um segundo. |
| **Preço em Créditos** | Contrapartida **falsa**. §24.5: "Se a sua mesa não gosta de contabilidade, **ignore este bloco inteiro. Nada no balanceamento do livro depende de Créditos**." Desconto em Cr é não dar nada. |

Testei também "libera uma mão" (arma de 2 mãos com Recarga passaria a exigir uma só, o inverso de Peso de impacto): **não funciona**. O rótulo "2 mãos" **não tem peso mecânico** no sistema — sem escudo, sem ataque com a mão secundária, sem regra de empunhadura (grep em todos os `.md`). Seria outro ganho de zero.

Diminuir o custo (recarregar sem gastar a Ação Complementar) também não resolve: opção com custo menor e ganho **zero** continua estritamente pior que não escolher nada. O defeito é a ausência de contrapartida, não o tamanho do custo.

**Conclusão:** não existe contrapartida real e barata de arbitrar dentro das restrições do livro. A remoção é a correção honesta e é a de menor alcance **no sistema de regras**: nada no livro concede, consome ou depende da propriedade Recarga além dos pontos de texto abaixo — nenhuma Bênção, nenhum Cone, nenhum Conjunto, nenhuma ficha de inimigo a cita (grep de `recarga|recarregar|recarrega` nos 34 `.md`).

### Propagação completa

| Onde | Hoje | Depois |
|---|---|---|
| `24-equipamentos.md` §24.2 | linha `**Recarga**` na tabela | removida; a lista passa a ter **4** propriedades |
| `24-equipamentos.md` §24.2, abaixo da tabela | — | uma frase: recarregar é descrição livre e **não custa** a propriedade especial |
| `24-equipamentos.md` §24.3, itens comuns | `\| Munição ou célula de reserva \| 0,5 \| 20 Cr \| Recarrega uma arma com a propriedade **Recarga** \|` | **item mantido**, mesmo Espaço e mesmo preço, com o "Para quê" reescrito sem citar a propriedade (ex.: reposição de projétil ou célula de energia). É sabor e inventário, não mecânica de propriedade. |
| `24-equipamentos.md` §24.7 passo 3 + Resumo | `**uma** propriedade especial` | `**até uma**` (achado B1) |
| `18-combate.md:262` | `Exemplos: recarga, arremessável, duas mãos, …` | lista alinhada às 4 propriedades reais (achado B2) |
| `build\oraculo_mestre_hist.py:59` | `("Munição ou célula de reserva", 0.5, 20, "Recarrega uma arma com a propriedade Recarga")` | texto igual ao novo "Para quê" de 24.3 |

**Propaga-se sozinho (não editar à mão):** a lista de propriedades da ficha é **derivada do livro** em dois lugares independentes — `ficha_dados.propriedades()` lê `## 24.2` pela coluna "Propriedade" (`ficha_dados.py:354-356`, usada em `:873-874` e `:939-940`) e `testar_ficha.py` relê o mesmo `.md` com parser próprio (`:1153`, `:1196`). Tirar a linha do livro já tira a opção da planilha e do oráculo. Idem a tabela de itens de 24.3 (`ficha_dados.itens()` em `:365`). E **`build\ficha_mapa.json` é gerado** por `gerar_ficha.py:316` — nunca se edita à mão (vale também para `mestre_mapa.json`).

**Hardcoded, precisa de edição manual:**

| Arquivo | Linha | O que tem |
|---|---|---|
| `build\testar_ficha.py` | 2504 | `_OR_PROPRIEDADES = ["Nenhuma", "Recarga", "Arremessável", "Alcance estendido", "Peso de impacto", "Dissimulada"]` → tirar `"Recarga"` |
| `build\testar_ficha.py` | 2288 | caso `("propriedade de arma dupla", e(criacao__arma__propriedade="Recarga, Arremessável"), …)` → usar duas propriedades que ainda existam |
| `build\gerar_ficha.py` | 1320-1321 | `amostra="Recarga"`, `invalido="Recarga, Arremessável"` (arma principal) |
| `build\gerar_ficha.py` | 2257-2258 | `invalido="Recarga, Arremessável"` (arma secundária; `amostra="Dissimulada"` segue válida) |
| `build\oraculo_mestre_hist.py` | 59 | texto do item de 24.3 |

**Sem alteração:** `build\oraculo_ficha.py` só cita `Peso de impacto` (`:675`) e `Dissimulada` (`:678`), que sobrevivem. `SOBRECARGA` (`oraculo_ficha.py:184,782`, `testar_ficha.py:2559`) é a condição de inventário, sem relação. Todo `recarga` de `mestre_dados.py`, `mestre_mapa.json`, `oraculo_mestre_abas.py`, `oraculo_mestre_livro.py` é a **recarga em Ciclos de ação especial de inimigo** (cap. 28) — **correta, não mexer**. A "condição de recarga" de Habilidade (`16-habilidades.md:267`) fica (B6).

### Efeito colateral mapeado: a Planilha do Mestre é tocada

A mudança no "Para quê" do item de 24.3 chega à Planilha do Mestre por dois caminhos: `mestre_dados.py:749,764` lê os itens via `ficha_dados.itens()` (que lê o livro → muda sozinho) e `oraculo_mestre_hist.py:460-462` publica `recompensas.preco.itens.N.desc` a partir da constante hardcoded. Se só um mudar, `testar_mestre.py` diverge.

**Decisão:** atualizar a constante do oráculo **e** regerar a Planilha do Mestre **mantendo o nome atual** (`Mestre\Planilha do Mestre - Explorando Galáxias V1.1.xlsx`). Justificativa: o usuário pediu v1.2 do **PDF e da ficha**; a Planilha do Mestre não está no escopo de versionamento desta tarefa e renomeá-la criaria entregável não pedido — mas deixá-la contradizendo o livro é pior. É uma frase num campo de descrição. **O implementador confirma este ponto via `send_message`** junto de A2/A3, porque mexe num entregável que o usuário não nomeou.

---

## 4. Strings de versão: 1.1 → 1.2

Levantadas por grep de `1\.1`, `V1\.1`, `v1\.1` em `livro-v1.0\*.md`, `build\*.py` e `scripts\*.ps1`.

### 4.1 Versão corrente — TROCAR

| Arquivo | Linha | Hoje → Depois |
|---|---|---|
| `livro-v1.0\00-capa-e-creditos.md` | 9 | `**Versão 1.1**` → `**Versão 1.2**` |
| `livro-v1.0\00-capa-e-creditos.md` | 50 | acrescentar o parágrafo da v1.2 apontando o changelog novo; **o parágrafo da v1.1 continua** (como o da v1.0 continuou) |
| `build\gerar_pdf.py` | 3 | docstring `v1.1 em PDF` → `v1.2` |
| `build\gerar_pdf.py` | 34 | docstring `…V1.1.pdf` → `V1.2.pdf` |
| `build\gerar_pdf.py` | 87 | `ARQUIVO_SAIDA = …"Sistema de HSR by MC Filhos V1.1.pdf"` → `V1.2.pdf` |
| `build\gerar_pdf.py` | 93 | `VERSAO_LIVRO = "Versão 1.1"` → `"Versão 1.2"` |
| `build\gerar_pdf.py` | 1903 | `print("… montagem do livro v1.1 em PDF")` → `v1.2` |
| `build\gerar_docx.py` | 3 | docstring `v1.1` → `v1.2` |
| `build\gerar_docx.py` | 26 | docstring `…V1.1.docx` → `V1.2.docx` |
| `build\gerar_docx.py` | 67 | `ARQUIVO_SAIDA = …"…V1.1.docx"` → `V1.2.docx` |
| `build\gerar_docx.py` | 73 | `VERSAO_LIVRO = "Versão 1.1"` → `"Versão 1.2"` |
| `build\gerar_docx.py` | 231 | `core_properties.comments = "Explorando Galáxias v1.1 — gerado por build/gerar_docx.py"` → `v1.2` |
| `build\gerar_docx.py` | 688 | `print("… montagem do livro v1.1")` → `v1.2` |
| `build\gerar_ficha.py` | 4 | docstring `v1.1` → `v1.2` |
| `build\gerar_ficha.py` | 50 | docstring `…V1.1.xlsx` → `V1.2.xlsx` |
| `build\gerar_ficha.py` | 77 | `VERSAO = "v1.1"` → `"v1.2"` (o comentário diz "versão do livro (capa…)": tem de bater com a capa) |
| `build\gerar_ficha.py` | 79 | `SAIDA_XLSX = ENTREGA / "Ficha Automatizada - Explorando Galáxias V1.1.xlsx"` → `V1.2.xlsx` |
| `build\gerar_ficha.py` | 3754 | `"se calcula sozinho. Ficha V1.1 · revisão 2."` → `"… Ficha V1.2 · revisão 1."` (versão nova reinicia o contador) |
| `build\testar_ficha.py` | 4, 8, 20 | docstrings com `v1.1` / `V1.1.xlsx` / `.docx/.pdf V1.1` → `v1.2` / `V1.2` |
| `build\testar_ficha.py` | 78 | `XLSX = ENTREGA / "…V1.1.xlsx"` → `V1.2.xlsx` — **senão a bateria testa o arquivo velho** |
| `build\testar_ficha.py` | 544-545 | `_arquivos_protegidos()` lista `"…V1.1.docx"` e `"…V1.1.pdf"` → `V1.2`. Os V1.1 saem da lista protegida e ficam na raiz como registro, igual ao que foi feito com os V1.0 |
| `scripts\verificar-livro-final.ps1` | 40 | `$ArquivoDocx = … 'Sistema de HSR by MC Filhos V1.1.docx'` → `V1.2.docx` |
| `scripts\verificar-livro-final.ps1` | 57 | `' VERIFICAÇÃO FINAL — Explorando Galáxias v1.1'` → `v1.2` |

`build\testar_ficha.py:76` (`LIVRO = RAIZ / "livro-v1.0"`) é **caminho de pasta**: o caminho não muda; só o comentário passa a dizer v1.2.

### 4.2 Comentário histórico — NÃO TOCAR

Registro de decisão tomada, não versão corrente. Ficam **exatamente como estão**:

- `build\gerar_ficha.py` linhas **107, 735, 1760, 1783, 2210, 2318, 2397, 2981, 3007, 3024, 3303, 3548** — tipo `# 25.2 (v1.1, D5): …`, `# Congelado saiu da lista do personagem na v1.1`, `# 23.5 (v1.1, D3): …`.
- `build\testar_ficha.py` linhas **867, 882, 1047, 1056, 1140, 1159, 1376** — `# Pedido do usuário (v1.1): …`, `# 21.5 (v1.1): …`, `# 24.1 (v1.1)`, `(25.2, v1.1)`.
- `build\ficha_dados.py:342` — `# 24.1 (v1.1, D4): …`.
- `build\gerar_mestre.py:3,18` — a Planilha do Mestre **não muda de versão** nesta tarefa (§3).
- `livro-v1.0\00-changelog-v01-para-v10.md` e `00-changelog-v10-para-v11.md` — **arquivos históricos inteiros**, intocados (inclusive `:9` sobre o nome da pasta e `:36` sobre os V1.0 ficarem como registro).
- `build\requirements-ficha.txt:2` — "Versões exatas usadas na rodada da v1.1": registro de ambiente.

### 4.3 Nota de versão: seguir a convenção que o projeto já tem

O projeto **não tem `CHANGELOG.md` e não vai ter**. Ele registra mudança de duas formas, e as duas se usam:

1. **Arquivo de changelog por salto de versão** em `livro-v1.0\`: já existem `00-changelog-v01-para-v10.md` e `00-changelog-v10-para-v11.md`. Criar `livro-v1.0\00-changelog-v11-para-v12.md`, **enxuto**, no formato do anterior.
   **Risco mapeado:** `gerar_pdf.py:313` e `gerar_docx.py:125` fazem `os.listdir` de **todos** os `.md` e ordenam pelo prefixo numérico (empate de `00-` resolvido pelo nome). O arquivo novo **entra no PDF e no DOCX automaticamente** — que é o comportamento desejado, e é como os dois changelogs anteriores entraram. Confirmado que `scripts\checar-completude.ps1` usa lista de capítulos **esperados** e só acusa **ausentes** (`:104`), nunca "arquivo extra": o changelog novo não quebra a checagem.
2. **Quadro "O que mudou da vX" na seção afetada**: é o padrão do livro (`24.1`, `24.3`, `24.4`, `16.3`, `16.6`, `17.1`, `20.5`, `05`). Acrescentar um quadro **curto** `> **O que mudou da v1.1:**` em **24.2** (saída da Recarga) e, se A2/A3 forem aprovados, nas seções deles. Não espalhar quadro por seção que não mudou.

---

## 5. Plano de execução

Ordenado por dependência. Cada item deixa o projeto em estado utilizável.

- [ ] **1. Varredura sistemática e relatório de achados.**
      Aplicar a régua A/B de §2 aos capítulos listados em §2.2, confirmando os 10 achados já levantados e acrescentando o que aparecer. Escrever `achados-v12.md` com a mesma tabela (seção · frase verbatim · A/B · severidade · correção), separando "aplicar agora" de "pendente de decisão do usuário".
      Arquivos: cria `.agents\tasks\v12\achados-v12.md`. Nenhum `.md` do livro alterado neste item.
      Verificar: `powershell -File "scripts\checar-completude.ps1"` e `powershell -File "scripts\checar-tabelas.ps1"` continuam saindo 0 (nada mudou ainda — é a linha de base).

- [ ] **2. Confirmar com o usuário os achados que mudam comportamento.**
      `send_message` severidade `warning` com: A2 (Raio dominado por Fogo), A3 (Avginiano dominado por Xianzhouíta) e a regeração da Planilha do Mestre (§3). Para cada um: achado, correção mínima, efeito visível, alternativa que preserva comportamento. **Esperar a resposta.** O que não for aprovado fica fora e é registrado no relatório como achado conhecido e não corrigido.
      Verificar: resposta do usuário registrada em `achados-v12.md`.

- [ ] **3. Correções no livro (texto).**
      Aplicar A1, B1, B2, B3, A4, B4, B5, B6 e o que o item 1 acrescentar, mais o que o item 2 autorizar. Acrescentar o quadro `> **O que mudou da v1.1:**` em 24.2.
      Arquivos: `livro-v1.0\24-equipamentos.md`, `livro-v1.0\18-combate.md`, `livro-v1.0\17-ultimate-e-energia.md`, `livro-v1.0\25-cones-de-luz-e-reliquias.md`, `livro-v1.0\26-progressao-e-ressonancias.md`, `livro-v1.0\16-habilidades.md`, e `livro-v1.0\20-...md` / `livro-v1.0\21-condicoes.md` / `livro-v1.0\05-racas.md` só se A2/A3 forem aprovados.
      Verificar: `powershell -File "scripts\checar-tabelas.ps1"` e `powershell -File "scripts\checar-nomenclatura.ps1"` saem 0. **A suíte `protegidos` vai falhar de propósito a partir daqui** — é o detector de alteração do livro, e só volta ao verde na re-linha-de-base do item 7.

- [ ] **4. Nota de versão.**
      Criar `livro-v1.0\00-changelog-v11-para-v12.md` enxuto (o que mudou, por quê, o que **não** mudou — nenhum número de balanceamento, salvo o que o item 2 autorizar) e acrescentar o parágrafo da v1.2 em `00-capa-e-creditos.md:50`, mantendo o da v1.1.
      Arquivos: cria `livro-v1.0\00-changelog-v11-para-v12.md`; edita `livro-v1.0\00-capa-e-creditos.md`.
      Verificar: `powershell -File "scripts\checar-completude.ps1"` sai 0 (confirma que o arquivo extra não quebra a checagem).

- [ ] **5. Propagação da decisão sobre Recarga no código.**
      Editar os 5 pontos hardcoded da tabela de §3 (`testar_ficha.py:2288,2504`; `gerar_ficha.py:1320-1321,2257-2258`; `oraculo_mestre_hist.py:59`). Não tocar em `ficha_mapa.json` nem em `mestre_mapa.json` (gerados).
      Arquivos: `build\testar_ficha.py`, `build\gerar_ficha.py`, `build\oraculo_mestre_hist.py`.
      Verificar: `python -m py_compile "build\testar_ficha.py" "build\gerar_ficha.py" "build\oraculo_mestre_hist.py"` sem erro.

- [ ] **6. Versão 1.2 nas strings correntes.**
      Aplicar §4.1, **sem tocar em nada de §4.2**. Conferir ao final que `gerar_ficha.VERSAO` bate com a capa.
      Arquivos: `livro-v1.0\00-capa-e-creditos.md`, `build\gerar_pdf.py`, `build\gerar_docx.py`, `build\gerar_ficha.py`, `build\testar_ficha.py`, `scripts\verificar-livro-final.ps1`.
      Verificar: `python -m py_compile` nos quatro `.py`; e um grep de `V1\.1` nesses arquivos devolve **só** as linhas de §4.2.

- [ ] **7. Regerar entregáveis e refazer a linha de base de protegidos.**
      Ordem obrigatória: (a) `$env:PYTHONUTF8="1"; python "build\gerar_docx.py"`; (b) `python "build\gerar_pdf.py"`; (c) `python "build\gerar_ficha.py"`; (d) se o item 2 autorizou, `python "build\gerar_mestre.py"`; (e) **só então** apagar `build\ficha_protegidos.json` e rodar `python "build\testar_ficha.py" --suite protegidos`, que regrava a linha de base na primeira execução (`testar_ficha.py:570-576` — não existe flag de re-gravação; apagar o JSON **é** o procedimento).
      Arquivos: gera `Sistema de HSR by MC Filhos V1.2.docx`, `...V1.2.pdf`, `ficha-automatizada\Ficha Automatizada - Explorando Galáxias V1.2.xlsx`; regrava `build\ficha_mapa.json` e `build\ficha_protegidos.json`.
      Verificar: os três arquivos V1.2 existem e são mais novos que o `.md` mais recente; os V1.1 continuam na raiz; `--suite protegidos` sai 0.

- [ ] **8. Bateria completa.**
      `$env:PYTHONUTF8="1"; python "build\testar_ficha.py" --suite tudo` (11 suítes: spike, protegidos, dados, ouro, oraculo, extremos, lint, texto, preview, visual, google) e `powershell -File "scripts\verificar-livro-final.ps1"`. Se o item 2 autorizou a Planilha do Mestre, `python "build\testar_mestre.py" --suite tudo`.
      Verificar: saída 0 em tudo. A `dados` é a que prova que a planilha bate com o livro novo (ela relê os `.md`); a `texto` prova que nenhuma string proibida entrou; a `google` usa os exports de `build\google_rev1\`.

- [ ] **9. Relatório final.**
      `relatorio-v12.md` em `.agents\tasks\v12\`: achados corrigidos, achados reportados e não corrigidos (com a resposta do usuário), arquivos alterados, entregáveis V1.2 gerados, saída das suítes.
      Verificar: o relatório lista explicitamente que nada em `Explorando Galáxias RPG - Players\` e `versões antigas\` foi tocado.

### Notas de ambiente (do histórico do projeto, `.agents\orquestrador-override.md`)

- Sempre `$env:PYTHONUTF8="1"` antes dos scripts Python.
- Python 3.14.7 com `openpyxl 3.1.5`, `formulas 1.3.4`, `pillow 12.1.0`, `python-docx 1.2.0`, `reportlab 4.4.4` — **já instalados e conferidos**.
- `openpyxl.load_workbook` **direto do `G:`** (Google Drive) já travou o shell duas vezes. Copiar para `$env:TEMP` antes de abrir.
- Comando demorado em primeiro plano volta com `^C` e exit -1 **mas o processo filho termina**: rodar em background e ler o arquivo de saída depois.
- A suíte `google` depende dos dois exports em `build\google_rev1\` — não mover nem apagar.
- Pode haver uma **sessão paralela da Planilha do Mestre** rodando. Se `build\mestre\` ou `Mestre\` estiver em uso, não disputar.
- Nenhum `.md` do livro é fonte de verdade duplicada: o livro manda, a ficha e a planilha do Mestre leem dele.
