# HANDOFF — Retomada do projeto "Explorando Galáxias"

> ## ✅ PAUSA DE 05/10 (09:46) RETOMADA E CONCLUÍDA
> O pedido "pode apagar os backups da ficha" foi concluído. Nada desta sessão está rodando.
>
> - **O usuário reorganizou a pasta:** este arquivo agora fica em `versões antigas\`. Na raiz ficaram
>   o livro V1.1 (`.docx` e `.pdf`) e `Marcos Filho - Explorando Galáxias V1.1.gsheet`, que é a
>   planilha Google dele: não mexa.
> - **Pedido em andamento:** "pode apagar os backups da ficha". O usuário apagou de propósito a
>   "Cópia de Ficha..." que estava em `ficha-automatizada\`.
> - **Já feito:**
>   - A pasta `.agents\tasks\backup-usuario-0410\` foi apagada.
>   - Os dois exports do Google que estavam nela NÃO foram descartados, porque a suíte `google` de
>     `build\testar_ficha.py` depende deles: são os únicos valores reais calculados pelo Google.
>     Eles foram movidos para `build\google_rev1\export-google-haloviano-0-erros.xlsx` e
>     `build\google_rev1\export-google-humano-261-erros.xlsx`.
>   - `testar_ficha.py` foi atualizado para os caminhos novos (constantes `GOOGLE_REF`,
>     `GOOGLE_COPIA` e `GOOGLE_ERRO`, perto da linha 3776), e também as seções 11.3 e 11.4 de
>     `ficha-automatizada\AUDITORIA-DA-FICHA.md`.
> - **Concluído (05/10, 09:50):** `testar_ficha.py --suite google` passou com os caminhos novos
>   (4.734 checagens, 0 falha). A revisão 1 e a revisão 2 deram 2.363 de 2.363 células iguais ao
>   Google, e o caso do usuário (Humano + "Dois Atributos (+1 cada)") deu 0 erros. O usuário foi
>   avisado.
> - **Atenção:** a planilha Google do usuário, `Marcos Filho - Explorando Galáxias V1.1.gsheet`
>   (na raiz), é de 04/10 23:18, antes da revisão 2 (05/10 08:31). Ela ainda tem o bug e precisa
>   ser recriada a partir do `.xlsx` novo. Foi oferecido passar o personagem dela para a ficha
>   nova, a partir de um export `.xlsx` feito pelo usuário.
> - **Atenção, sessão paralela:** outro chat está fazendo a "Planilha do Mestre" (`Mestre\`,
>   `build\*mestre*.py`, `.agents\tasks\mestre\PROGRESSO.md`). Às 09:46, ela rodava
>   `testar_mestre.py --suite oraculo` com 7 processos. Não mexa nesses arquivos nem nesses
>   processos. O usuário recebeu um recado para mandar a ela, sobre a linha de base dos hashes da
>   ficha e as listas "1-4", "5-8" e "9-12", que o Google pode transformar em data.
> - **Ambiente:** rode cada comando PowerShell numa linha só, separando com `;` (um comando com
>   quebras de linha não executou direito). Abrir `.xlsx` com openpyxl direto do drive G: travou o
>   shell algumas vezes; copiar o arquivo para `$env:TEMP` antes resolve.

**Para:** a próxima sessão do Kiro (outro chat, mesma Kiro IDE).
**Atualizado em:** 04/10/2026, ~22:50 (seções 2, 3 e 4: **projeto concluído**, workflow `wf_109b35b843b0aaa2`).
O texto abaixo da seção 4 é o contexto da parada anterior, mantido como histórico.
**Motivo da parada:** cota de créditos do usuário quase esgotada (930.95 / 1000). O usuário
pediu parada imediata. O último workflow (`wf_f5844c6597dfe7c1`) foi **abortado por mim**
no meio do passo `ficha-v11`.

> Este arquivo substitui a versão anterior do handoff, que descrevia a fase do livro v1.0 e
> está obsoleta. O registro bruto de decisões e incidentes fica em
> `.agents\orquestrador-override.md`.

Leia por inteiro antes de agir. **O usuário pediu para economizar créditos:** siga a seção 5.

---

## 1. O PROJETO EM 30 SEGUNDOS

- RPG de mesa original em **PT-BR**, **"Explorando Galáxias"**, no universo de **Honkai: Star
  Rail**. O autor é o usuário (**MC Filhos**).
- **Livro**: a v1.0 foi entregue e aprovada. A **v1.1** (correções que a auditoria da ficha
  encontrou) está **publicada e completa**.
- **Ficha de personagem automatizada** (`.xlsx` para importar no **Google Planilhas**):
  **quase pronta**. Falta fechar a atualização para a v1.1 e escrever o relatório de auditoria
  (seção 4).

### Decisões já confirmadas com o usuário (não reabrir)

| Item | Decisão |
|---|---|
| Nome / autoria / idioma | **Explorando Galáxias**, **by MC Filhos**, **PT-BR** em tudo |
| Faixa de níveis | **1 a 20** |
| Versão atual | **v1.1** do livro **e** da ficha |
| Formato da ficha | `.xlsx` gerado com `openpyxl`, importável no Google Planilhas. Daqui não dá para criar Planilha Google nativa, mas a pasta do projeto **sincroniza com o Google Drive** do usuário. **Sem Apps Script e sem macros.** |
| Economia | O usuário pediu explicitamente para não gastar créditos à toa |

---

## 2. ESTADO EM UMA TELA

| Fase | Status |
|---|---|
| Livro v1.0 (32 capítulos `.md`, `.docx`, `.pdf` de 250 páginas) | ✅ COMPLETO, aprovado, mantido como histórico |
| **Livro v1.1** (D1–D7 + N1–N5) | ✅ **COMPLETO**: `.docx` e `.pdf` V1.1 (PDF com **253 páginas, 0 avisos**), changelog v1.0→v1.1 dentro do livro, `verificar-livro-final.ps1` passando, simulação de combate rodada |
| Ficha: FEAT-001 a FEAT-004 | ✅ COMPLETO, mas **medido contra o livro v1.0** (antes das correções) |
| **Ficha v1.1** (modelo, Ficha Exemplo da Nadir, `COMO-USAR`, `AUDITORIA-DA-FICHA.md`) | ✅ **CONCLUÍDA** em 04/10/2026 |
| Revisão independente da v1.1 | ✅ **CONCLUÍDA**: aprovou ficha e livro, 6 achados não bloqueantes, todos tratados (`AUDITORIA-DA-FICHA.md`, seção 9) |
| Auditoria visual final da ficha (pedido do usuário) | ✅ **CONCLUÍDA** em 04/10/2026 (`AUDITORIA-DA-FICHA.md`, seção 10) |
| Verificação final + limpeza | ✅ **CONCLUÍDA**: `verificar-livro-final.ps1` passa; temporários apagados |
| **Ficha V1.1 · revisão 2** (05/10, usuário viu "CHEIO de erros" no Google) | ✅ **CONCLUÍDA e APROVADA** na revisão independente (2 achados baixos, tratados). Causa: opções de lista que começavam com "+" (ex.: "+1 em dois" do Humano) viravam **fórmula** no Google → `#ERROR!` em 261 células. Correção: rótulos sem sinal, leitura protegida das 358 entradas, aviso por linha e contador de erros em Início!B19 (`AUDITORIA-DA-FICHA.md`, seção 11) |

Números da revisão 2 (`--suite tudo`, código 0, `.agents\tasks\suite-tudo-rev2.txt`): spike 23,
protegidos 76, dados 3297, ouro 533, oráculo 247, extremos 2714, lint 11 924, texto 1 006 920,
preview 278, visual 24 036, google 4734 (2363 de 2363 células iguais ao export do Google); 0 falha.
Fórmulas: 2947 (eram 2363). Os números abaixo são da rodada anterior (revisão 1).

Números finais (`--suite tudo`, código 0, saída em `.agents\tasks\suite-tudo-final.txt`): spike 14,
protegidos 76, dados 3297, ouro 533, oráculo **247 casos / 43 712 saídas / 0 divergência**,
extremos 858, lint 6204, texto 975 083, preview 278 (40 PNG + 344 recortes ≤ 1800 px, 0 texto
cortado), visual 23 898 (22 521 textos nos 4 estados, 0 não coube); todas com 0 falha. Área do
jogador em 1360 px em 7 abas (Início 1264, Regras Rápidas 1243); Em Jogo 1360 × 760 px; 0 painel
congelado; maior distância ao cabeçalho 12 linhas; menor contraste 4,96:1.

---

## 3. O QUE FOI FEITO (conferido em disco em 04/10/2026, ~22:50)

| | Item |
|---|---|
| ✅ | `build\ficha_protegidos.json` refeito com a v1.1 do livro (suíte `protegidos`: 76 checagens OK) |
| ✅ | `gerar_ficha.py` grava em `ficha-automatizada\` |
| ✅ | `ficha-automatizada\Ficha Automatizada - Explorando Galáxias V1.1.xlsx` (modelo em branco, 126 KB, 22:28) |
| ✅ | `ficha-automatizada\Ficha Exemplo - Nadir.xlsx` (exemplo preenchido do capítulo 29.7, 126 KB, 22:28) |
| ✅ | `ficha-automatizada\COMO-USAR-NO-GOOGLE-PLANILHAS.md` (7 KB); a checklist de 2 minutos usa células que não mudaram de lugar e valores da v1.1 |
| ✅ | `ficha-automatizada\AUDITORIA-DA-FICHA.md`: suítes, bugs, decisões, inconsistências do livro corrigidas na v1.1, revisão independente (seção 9) e **auditoria visual final (seção 10)** |
| ✅ | `build\requirements-ficha.txt` (versões exatas) |
| ✅ | Nenhum arquivo V1.0 em `ficha-automatizada\`. Lá existe também `explorando galaxias ficha teste mc filhos.xlsx`, que não é da ficha gerada e não foi mexido |
| ✅ | Livro V1.1 (`.docx` 21:27 e `.pdf` 21:28, depois do último `.md` de 21:26); não foi alterado na auditoria final; `verificar-livro-final.ps1` passa |
| ✅ | Auditoria visual final: avisos em K:L onde K estava livre (`alargar_avisos`), régua de `VLOOKUP` só na coluna buscada (`renderizar_ficha.PiorTexto`), Traços medidos, inventário com "Do catálogo?" em G:J, larguras da Caminho; Criação 5353 → 4406 px, Caminho 4504 → 3841 px, Equipamento 5218 → 4253 px no pior caso, sem texto cortado. A suíte `visual` agora informa os textos medidos por estado |
| ✅ | Limpeza: `$env:TEMP\fx_*` e `eg-*` e `.agents\tasks\tmp_checklist.*` apagados |
| ✅ | **Revisão 2 (05/10)**: os dois `.xlsx` regenerados (08:31, Início!A6 diz "Ficha V1.1 · revisão 2"); nova suíte `google` (compara com o export do Google); exports do usuário guardados em `.agents\tasks\backup-usuario-0410\` (a "Cópia de Ficha…" só existe lá, SHA-256 941E3443…); livro intocado (`protegidos` OK) |

Abaixo, o estado da parada anterior (18:45), só como histórico:

| | Item |
|---|---|
| ⚠️ | `.agents\tasks\suite-tudo-v11.txt` (9 KB) está **INCOMPLETO**: só traz `spike` (OK, 14), `protegidos` (OK, 76) e `dados` (OK, 3297). As suítes **ouro, oraculo, extremos, lint, texto e preview NÃO têm resultado depois das mudanças da v1.1.** As linhas "DIVERGE" da `spike` são informativas (diferenças entre o motor local e o Google que a ficha evita de propósito) e **não são falha**. |
| ❌ | `ficha-automatizada\AUDITORIA-DA-FICHA.md` **NÃO EXISTE**. A base é `.agents\tasks\relatorio-auditoria-ficha.md` (17 KB, escrito na FEAT-004, ainda referente à v1.0). |
| ❓ | Não confirmado: (a) se o contorno da divergência D1 (duas colunas, "livro" e "regra") foi simplificado para a regra única; (b) se **todo** texto de versão dentro da planilha diz V1.1; (c) se os recortes PNG foram regerados para a v1.1 (`renderizar_ficha.py` é das 17:43, antes da v1.1). |

---

## 4. O QUE FALTA

**Nada do pedido.** Ficha v1.1, revisão independente e auditoria visual final concluídas em
04/10/2026. Pontos cosméticos aceitos, sem texto cortado, estão em `AUDITORIA-DA-FICHA.md`,
seção 10.4 (linhas das Habilidades e das Relíquias um pouco altas, tabela de Energia das Regras
Rápidas, colunas espaçadoras M e N). As ofertas da seção 7 continuam **não pedidas**. A
conferência no Google Planilhas de verdade é a checklist do `COMO-USAR`, seção 5, feita pelo
usuário.

Lista original desta seção (toda feita), como histórico:

1. Rodar `gerar_ficha.py` e `testar_ficha.py --suite tudo`, e corrigir até **todas** as suítes
   saírem 0, inclusive **ouro** (o Nadir da v1.1, com a marreta em `1d12 + 6 · média 12`) e
   **oraculo** (zero divergência). Gravar a saída completa em `.agents\tasks\suite-tudo-v11.txt`.
2. Conferir os três itens ❓ da seção 3 e corrigir o que faltar.
3. Escrever **`ficha-automatizada\AUDITORIA-DA-FICHA.md`** (PT-BR, para o usuário), partindo de
   `.agents\tasks\relatorio-auditoria-ficha.md` e atualizando para a v1.1. Conteúdo: o que foi
   verificado e como; o resultado de cada suíte com números; bugs encontrados e corrigidos,
   com antes e depois; erros de digitação corrigidos; as 12 decisões de projeto
   (`.agents\tasks\plano-ficha.md`, seção 3); limitações honestas (o motor `formulas` não é o
   Google Planilhas; validação e formatação condicional não foram executadas por ele); a seção
   **"Inconsistências do livro — corrigidas na v1.1"** (cada Dn/Nn, onde estava e o que foi
   feito, conforme `livro-v1.0\00-changelog-v10-para-v11.md`); e como regenerar e retestar.
4. Conferir se a **checklist de 2 minutos** de `COMO-USAR-NO-GOOGLE-PLANILHAS.md` usa valores da
   **v1.1** que a suíte ouro confirma.
5. Regerar os recortes de pré-visualização (`--suite preview`, 3 estados).
6. *(Opcional, só se houver crédito)* uma revisão independente com `semantic_reviewer`, em uma
   volta.
7. Verificação final: `scripts\verificar-livro-final.ps1` passando; todos os entregáveis da
   seção 8 existindo; nenhum arquivo com nome V1.0 em `ficha-automatizada\`; e apagar os
   temporários `$env:TEMP\fx_*.py` e `$env:TEMP\eg-*.py`.
8. Reportar ao usuário, incluindo as decisões da seção 7.

---

## 5. COMO RETOMAR GASTANDO POUCO

- **Não use `run_workflow` com `workflowPrompt`.** O criador de workflow faz uma rodada de
  design que também consome créditos. O que falta é pequeno e bem definido.
- **Opção A (recomendada):** um único `run_workflow` com `workflowPath: "agent://wf-coder"` e o
  prompt pronto da seção 6 como input `prompt`. Cobre os itens 1–5 e 7.
- **Opção B:** fazer direto no chat, com os comandos da seção 9. Só compensa se as suítes
  passarem de primeira.
- **Antes de lançar, avise o usuário** do que vai rodar. Ele está sem margem de créditos.

---

## 6. PROMPT PRONTO PARA `agent://wf-coder`

```
Termine a atualização da FICHA AUTOMATIZADA para o livro v1.1 do RPG "Explorando Galáxias"
(PT-BR). Raiz: g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG

Leia primeiro, por inteiro: HANDOFF-RETOMADA-v1.0.md (raiz), seções 3, 4, 8 e 9. Elas
dizem exatamente o que já foi feito e o que falta. Depois leia
livro-v1.0\00-changelog-v10-para-v11.md e .agents\tasks\diff-v10-v11.md (o que mudou no
livro). O plano da ficha está em .agents\tasks\plano-ficha.md, e as FEATs em
.agents\tasks\task-ficha-automatizada\features\FEAT-001..004.json.

Faça os itens 1 a 5 e 7 da seção 4 do handoff:
1. gerar_ficha.py + testar_ficha.py --suite tudo, até todas as suítes saírem 0 (ouro com o
   Nadir da v1.1 e oraculo com 0 divergência). Grave a saída em
   .agents\tasks\suite-tudo-v11.txt.
2. Confira e corrija: contorno de D1 simplificado para a regra única; todo texto de versão
   da planilha em V1.1; recortes PNG regerados.
3. Escreva ficha-automatizada\AUDITORIA-DA-FICHA.md (conteúdo na seção 4, item 3).
4. Confira a checklist de 2 minutos de COMO-USAR-NO-GOOGLE-PLANILHAS.md com valores v1.1.
5. Verificação final e limpeza (seção 4, item 7).

NÃO altere o livro (livro-v1.0\), nem os .docx/.pdf, nem build\gerar_docx.py ou
build\gerar_pdf.py. Problema no livro vai para o relatório.

Compatibilidade com o Google Planilhas (o lint confere e deve ficar em zero): fórmulas em
inglês canônico com vírgula, só funções da lista branca, INT para arredondar, sem
referência a outra aba em formatação condicional ou validação personalizada, sem _xlfn,
sem INDIRECT.

Ambiente: Windows/PowerShell (";" em vez de "&&", aspas duplas em todo caminho), comando
python com $env:PYTHONUTF8="1", código Python sempre em arquivo .py executado pelo
caminho (o stdin corrompe o acento do caminho). Mojibake no console é o codepage do
console, não o arquivo. Não é git. Imagens: nunca abra uma com mais de 1800 px em qualquer
lado, no máximo 4 por vez. Economize créditos: use busca em vez de ler inteiros os
arquivos grandes (gerar_ficha.py ~200 KB, testar_ficha.py ~170 KB).

Ao terminar, envie send_message com severity success e os números de cada suíte.
```

---

## 7. DECISÕES DA v1.1 QUE O USUÁRIO PRECISA CONHECER

Todas estão registradas em `livro-v1.0\00-changelog-v10-para-v11.md`. O diff completo está em
`.agents\tasks\diff-v10-v11.md`, e as cópias dos `.md` antes da mudança em
`.agents\tasks\livro-v10-antes\` (17 arquivos).

- **D3, a única que muda o jogo:** Vulpes e Avginiano passam a ter **Vantagem no Teste de
  Morrendo**, como o Xianzhouíta (cap. 05 + 22.1). O usuário foi avisado e **não vetou** antes
  da parada.
- **D1:** o exemplo do Nadir foi corrigido para a regra: marreta `1d12 + 6 · média 12` (Mãos I
  dá +2 no Ataque Básico).
- **D5, diferente do que eu havia sugerido:** a Sobreposição de Cone de Luz agora chega ao
  mesmo ponto nos dois tetos, com **PV máximo de +30/+35** em vez de +50.
- **N4:** usou os níveis de referência 3/7/11/15/19.
- **N1–N5** são inconsistências novas achadas pela auditoria (FEAT-004). **N3 e N5** ficaram
  sem mudança de texto. Os detalhes estão no changelog.
- D2, D4, D6 e D7 são só esclarecimentos de texto, sem mudar regra.
- A pasta-fonte continua se chamando `livro-v1.0\` (nome histórico, para não mexer em todos os
  scripts). Os arquivos V1.0 continuam na raiz como histórico.

### Ofertas feitas ao usuário e ainda NÃO pedidas (não faça sem ele pedir)
- Ferramenta separada para o mestre: rastreador da Fila de Ação + bestiário em lista suspensa.
- PDF: inverter a hierarquia símbolo × arte nas aberturas de Caminho (o símbolo hoje sai maior
  que a arte do personagem).
- Arte para os 4 Caminhos novos (Erudição, Euforia, Caça, Preservação), que hoje estão sem
  imagem porque o acervo da v0.1 não tem esses símbolos.
- Condição "Provocado" (o livro cobre a fantasia de tanque com Barreira + Intervir).

---

## 8. INVENTÁRIO DE ARQUIVOS

Raiz: `g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG`

| Caminho | O que é |
|---|---|
| `Sistema de HSR by MC Filhos V0.1.docx` | **Original do autor. NÃO MODIFICAR.** |
| `Sistema de HSR by MC Filhos V1.0.docx` / `.pdf` | Histórico da v1.0 |
| **`Sistema de HSR by MC Filhos V1.1.docx` / `.pdf`** | **Livro atual** (PDF de 253 páginas) |
| `livro-v1.0\*.md` | Fonte do livro **v1.1**: 33 arquivos, contando o novo `00-changelog-v10-para-v11.md` |
| `build\gerar_docx.py`, `build\gerar_pdf.py` | Geradores do livro (já gravam V1.1) |
| `build\gerar_ficha.py` | Gerador da ficha (10 abas, cerca de 2.360 fórmulas). Grava `build\ficha_mapa.json` |
| `build\ficha_dados.py` | Parser dos `.md` do livro + dados transcritos |
| `build\oraculo_ficha.py` | Oráculo independente das regras (não lê fórmulas) |
| `build\testar_ficha.py` | Bateria: `--suite spike, protegidos, dados, ouro, oraculo, extremos, lint, texto, preview, tudo` |
| `build\renderizar_ficha.py` | Renderiza as abas em PNG e grava recortes de no máximo 1800 px |
| `build\ficha_protegidos.json` | Hashes SHA-256 do livro v1.1 (garantem que a ficha não altera o livro) |
| `build\requirements-ficha.txt` | Versões exatas das dependências da ficha |
| **`ficha-automatizada\`** | **Entregáveis da ficha** (os 4 prontos) |
| `scripts\*.ps1` | Verificações do livro (`verificar-livro-final.ps1`, `simular-combate.ps1`, `checar-nomenclatura.ps1` etc.) |
| `assets\imagens-v01\` | As 17 imagens da v0.1 (capa: `image11.png`) |
| `.agents\tasks\plano-ficha.md` | Plano aprovado da ficha (inventário de regras, abas, 12 decisões, testes) |
| `.agents\tasks\relatorio-auditoria-ficha.md` | Relatório da FEAT-004 (base da auditoria final) |
| `.agents\tasks\suite-tudo-antes-v11.txt` | Saída completa das suítes antes da v1.1 (referência) |
| `.agents\tasks\suite-tudo-v11.txt` | Saída **incompleta** depois da v1.1 (seção 3) |
| `.agents\tasks\diff-v10-v11.md`, `livro-v10-antes\` | Registro das mudanças do livro na v1.1 |
| `.agents\tasks\ficha-preview\` | PNGs. **Os de aba inteira são grandes demais para abrir**: use só os recortes `*-parte-NN.png` |
| `.agents\tasks\design.md` / `design-APROVADO.md` | Especificação mecânica do sistema (cerca de 250 KB; use busca, não leia inteiro) |
| `.agents\orquestrador-override.md` | Log bruto de decisões e incidentes |

---

## 9. AMBIENTE E COMANDOS

- **Windows + PowerShell.** Use `;` em vez de `&&` e `$env:TEMP` em vez de `%TEMP%`. **Aspas
  duplas em todo caminho**: eles têm espaços e o acento em "Galáxias".
- Python **3.14.7**, comando `python`. Instalados: `openpyxl` 3.1.5, `formulas` 1.3.4,
  `pillow` 12.1.0, `pypdf` 6.19.0, `python-docx` 1.2.0, `reportlab` 4.4.4.
- **Grave código Python em arquivo e execute pelo caminho**, com `$env:PYTHONUTF8="1"`. Mandar
  pelo stdin corrompe o acento do caminho (`Gal?xias`).
- Mojibake no console (`Ã¡`, `├¡`) é o **codepage do console**, não o arquivo. Os arquivos estão
  em UTF-8 correto. **Não "conserte" codificação.**
- **Não é repositório git**: sem commit, sem worktree. A pasta sincroniza com o Google Drive
  (ignore os `desktop.ini`).
- **O workflow roda na máquina do usuário**: o PC precisa ficar ligado e o Kiro aberto.

```powershell
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\gerar_ficha.py"
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\testar_ficha.py" --suite tudo
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\gerar_docx.py"
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\gerar_pdf.py"
& "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\scripts\verificar-livro-final.ps1"
```

---

## 10. LIÇÕES DE ORQUESTRAÇÃO (cada uma já custou créditos)

1. **Nunca use `onMaxIterations: "abort"`.** Um run morreu assim e perdeu a fase de escrita
   inteira. Use `"pause"` (recuperável com `extend_repeat`) ou `"continue"`.
2. **`wf-reviewer` NÃO EXISTE.** Agentes válidos: `wf-coder`, `wf-planner`, `semantic_reviewer`,
   `wf-review-aggregator`, `wf-design`, `wf-design-reviewer`.
3. **Limite de imagem:** nenhum passo pode abrir imagem com mais de 1800 px em qualquer lado,
   nem mais de 4 por vez. Um run falhou com
   `image dimensions exceed max allowed size ... 2000 pixels`. Repita essa regra no prompt de
   **todo** passo que puder abrir imagem.
4. **Revisor em espiral:** um revisor de design com portão aberto nunca aprova documento
   grande. Use conferência limitada ("os N achados fecharam?") e proíba abrir bloqueante novo.
5. **Planos podem perder entregáveis:** o planejador da ficha esqueceu 4 entregáveis pedidos.
   Confira o plano contra o pedido original.
6. **Para economizar:** `replace_remaining` com nós escritos à mão (validados com
   `validate_workflow`) evita a rodada de design do criador. `agent://wf-coder` é o caminho mais
   barato para um passo único. Um revisor só, lendo o diff em vez do livro inteiro, custa bem
   menos que dois revisores mais o agregador.
7. Prompts de passo são fixados no lançamento: mudança de requisito no meio do run precisa ser
   injetada por `send_message` ou `replace_remaining`.

---

## 11. HISTÓRICO DE RUNS

| Run | Resultado |
|---|---|
| (geração 1) | Falhou na validação: agente `wf-reviewer` inexistente |
| `wf_a39197a8faab22be` | Design. Abortou no teto do loop de design (`abort`) |
| `wf_cfdc2530c4b2fa10` | Correção do design. Abortado por cota |
| `wf_82958fe6e7d903ee` | ✅ Escrita do livro v1.0 (32 capítulos + `.docx`) |
| `wf_1816ff0fdf5cf1a0` | ✅ PDF v1.0 (250 páginas) |
| `wf_f4c2390f834ea13d` | Ficha: plano + FEAT-001..003 ✅; falhou na FEAT-004 (limite de imagem) |
| `wf_f5844c6597dfe7c1` | Ficha: FEAT-004 ✅, livro v1.1 ✅; **abortado por cota no meio do `ficha-v11`** |
