# Plano de implementação — Planilha do Mestre · Explorando Galáxias v1.1

Contrato: `.agents\tasks\mestre\design.md` (aprovado no ciclo 2) + `design-review.md`. Este plano **sequencia** o design e não redecide a arquitetura. Onde o design deixa escolha, a decisão está na seção 0 com o motivo. "§n" = seção do design.

Leitura obrigatória antes de cada fase: este plano (seções 0, 3, a fase e 8), `PROGRESSO.md` e as seções do design citadas no item. O repositório não tem README, AGENTS.md nem steering. A regra de casa está em `.agents\orquestrador-override.md`: o livro **nunca** é alterado (inconsistências vão para relatório), recortes ≤ 1800 px, no máximo 4 imagens por vez.

---

## 0. Decisões deste plano (com o motivo)

| # | Decisão | Motivo |
|---|---|---|
| P1 | **Sem reestruturar o workflow.** Os 4 loops de fase existentes (`fase1-loop` … `fase4-loop`, vereditos `review-fase1.json` … `review-fase4.json`) implementam as Fases 1–4 deste plano. | As fases do design já são a decomposição natural e cada uma depende da anterior (D10). FEATs só recriariam os mesmos 4 portões. |
| P2 | **Sem `requirements-mestre.txt`.** | D1: nenhuma dependência nova. `build\requirements-ficha.txt` já fixa openpyxl 3.1.5, formulas 1.3.4, pillow 12.1.0 e as transitivas. Conferido no ambiente: Python 3.14.7, openpyxl 3.1.5, formulas 1.3.4, Pillow 12.1.0. |
| P3 | **A lista efetiva de funções da Mestre é `ficha_funcoes_ok.json["funcoes"]`** (33 funções, **sem TRIM**), e não `testar_ficha.LISTA_BRANCA`. | `testar_ficha.LISTA_BRANCA` ainda contém `TRIM`, que o próprio `ficha_funcoes_ok.json` reprova. O lint da Mestre chama `testar_ficha._checar_formula(r, texto, onde, permitidas)` com a lista do JSON e proíbe também `RAND`, `RANDBETWEEN`, `SUBSTITUTE`, `CHAR`, `TRIM` e `COUNT` (D1, §12.1). |
| P4 | **Nunca chamar `testar_ficha.suite_protegidos`.** A suíte `protegidos` da Mestre só lê `ficha_protegidos.json` e `baseline-hashes.json` e usa `testar_ficha._arquivos_protegidos()` e `_sha256()`. | `suite_protegidos` da ficha **grava** `ficha_protegidos.json` quando ele não existe, o que é efeito colateral num arquivo protegido. |
| P5 | **Arquivo que já falta na linha de base.** `baseline-hashes.json` lista `ficha-automatizada\Cópia de Ficha Automatizada - Explorando Galáxias V1.1.xlsx`, que **não existe mais** no disco. Isso foi conferido na exploração, e os outros 13 hashes batem. A suíte guarda esse caso na constante `AUSENTES_CONHECIDOS` de `testar_mestre.py`, com o motivo "ausente já antes da Fase 1; a Mestre nunca grava em `ficha-automatizada\`", e o reporta como `info`. Qualquer **outro** arquivo ausente ou com hash diferente é falha. Nunca recriar o arquivo. | O arquivo sumiu fora deste trabalho, e recriá-lo seria alterar a ficha. Ler o JSON sempre com `encoding="utf-8"`: o "GalÃ¡xias" que o `Get-Content` do PowerShell 5.1 mostra é só exibição. |
| P6 | **Na prévia, o PNG da aba inteira nunca fica na pasta.** `renderizar_ficha.renderizar_estado` grava o PNG inteiro (até 6000 px) **e** os recortes `-parte-NN.png`. A suíte `preview` renderiza em `$env:TEMP\mestre-preview-*`, copia para `.agents\tasks\mestre\preview\` só os `-parte-NN.png` e o `indice-recortes.txt` (regravado nesse momento só com os recortes) e confere com Pillow que todo PNG copiado tem lado ≤ 1800 px; senão, falha. O temporário é apagado no `finally`. Antes da cópia, a pasta de prévia é esvaziada de PNGs antigos. | Regra de imagem do usuário e o incidente da FEAT-004 da ficha, registrado no override. |
| P7 | **Bestiário B2 (achado 1 da revisão):** Execução sai de K:L e vai para B:J, e "DT · TR" fica numa célula só (D:E mesclado). K:L serve só para aviso em todas as abas, sem exceção. | Mantém a convenção de D4/§6 sem abrir exceção no lint. |
| P8 | **Inimigos I5 (achado 2 da revisão):** na sub-tabela I5, o rótulo "Inimigo" fica na coluna A, repetido por fórmula como em toda sub-tabela a partir da segunda (D11). Fase, 4 Fraquezas, Tenacidade e ritmo ocupam B:J. | É a única disposição que cabe em B:J, como o revisor conferiu. |
| P9 | **"Grupo 1 e 8"** (pedido de verificação) vira três estados: 1 PJ na aba Grupo; Grupo cheio (6 PJs, o máximo de §6.3); e "Nº de jogadores" = 8 digitado na Campanha, que está fora de 1–6, acende aviso e calcula com o limite (§10.1). | O design só tem 6 linhas de PJ, e 8 PJs não cabem. O "8" vira o teste de entrada inválida. |
| P10 | **A cobertura do oráculo é medida, não declarada.** `nucleo.cal(..., regra=True)` registra em `mestre_mapa.json → numeros_de_regra` toda célula calculada que mostra número de regra. A suíte `oraculo` falha se alguma dessas células não for comparada por pelo menos um caso. | Para afirmar "oráculo para **todo** número de regra" é preciso provar a cobertura. |
| P11 | **A saída das suítes é gravada em UTF-8 pelo próprio script:** `testar_mestre.py --saida "<arquivo>"` duplica num arquivo UTF-8 tudo o que imprime. Não usar `Tee-Object` nem `>` do PowerShell 5.1, porque eles gravam UTF-16. | `suite-tudo.txt` legível e comparável. |
| P12 | **Atalhos de fase na CLI:** `--suite fase1`, `fase2`, `fase3` e `tudo` rodam a lista de suítes da fase (seções 4–7). Uma suíte nunca sai de um atalho para "passar". | Critério de pronto reproduzível com um comando só. |
| P13 | **Divergência nova do livro é fatal no build** até ser registrada em `mestre_dados.DIVERGENCIAS_DOCUMENTADAS` (seção, criatura/campo, valor do livro, o que a planilha mostra) e na seção 9 deste plano / `AUDITORIA.md`. O livro não é corrigido. | §10.2 e a regra dura "livro intocado". |
| P14 | **Spike primeiro.** Se a suíte `spike` mostrar divergência entre `formulas` e Python em `MOD`/`INT` grandes (estágios `h`, `L3`, `Q` e `X` de §5), o coder **não** troca a fórmula da semente por conta própria. Ele para e chama `send_message` com severity `warning`, informando o padrão que diverge, os valores e a alternativa já medida em §16 (juntar `y` e `x`). | A semente é decisão travada (D5) e afeta todos os geradores. |
| P15 | **"~200 sementes" em `extremos`:** além dos estados de §12.1, `extremos` recalcula modelo e Exemplo com 200 sementes (incluindo 1, 12345, 2026 e 2 147 483 646) × Rolagem nº 1 e 1 000 000 e confere 0 célula de erro em todas as fórmulas. | Pedido do passo. Complementa `determinismo`, que confere valores e não erros. |

---

## 0.1 Requisito do Google — OBRIGATÓRIO em todas as fases (lição da revisão 2 da ficha)

Pedido do orquestrador na iteração 2 da Fase 1. O Google lê como **fórmula** todo valor digitado, ou escolhido numa lista, que comece com `=`, `+`, `-` ou `@` ("+1 em dois" vira `#ERROR!`), e o erro se espalha para tudo que lê a célula. Na ficha isso deu 261 células com `#ERROR!`. Texto gravado pelo openpyxl entra como texto; o risco é só o que o mestre digita ou escolhe.

- **(a) Opções de lista:** nenhuma opção, fixa ou por intervalo, começa com `=`, `+`, `-` ou `@`, nem parece data ou hora (`1-4`, `3/7`, `1:30`), número em texto, percentual ou booleano. Listas numéricas vêm de células com número. O travessão é permitido. Na Fase 1 as faixas aparecem como "Faixa 1-4" (`mestre_dados.ROTULOS_FAIXA`; as fórmulas convertem com `nucleo.faixa_da_lista`; os testes com `testes_comum.digitado`).
- **(b) Contenção:** nenhuma fórmula lê uma entrada diretamente. `build\mestre\protecao.py` (`proteger(wb)`, chamada pelo gerador depois de `resolver_marcadores`) cria a camada de leitura protegida `=IF(ISERROR(X),"",IF(ISBLANK(X),"",X))` em colunas ocultas, reescreve as referências, põe um sinal de erro por linha e acende o aviso da linha em PT-BR. Entradas = as do mapa + **todas as vagas das listas editáveis** (Tabelas e, na Fase 3, Minhas Tabelas). O contador corrido das listas lê a camada, então vaga vazia ou com erro não conta.
- **(c) Contador na Início:** "Células com erro na planilha: N", com a contagem por aba (`SUMPRODUCT(ISERROR(intervalo)*1)`), sem referência circular, com explicação quando N > 0, e a dica no topo ("Não comece um texto com +, - ou =…"). A Fase 4 leva isso para o COMO-USAR.
- **(d) Testes permanentes:** `lint` roda `testar_ficha._lint_google` (por import) com o mapa da Mestre (opções de lista e leitura direta = 0); `extremos` injeta erro em cada entrada lida (todas as de lista, semente, nível, nº de jogadores, combatente, 10 vagas, 10 de texto, 10 numéricas): contador = exatamente 1, aviso aceso, nenhuma outra célula com erro; e em todas ao mesmo tempo. `spike` confere `""+1` → `#VALUE!`, célula vazia = 0 na formulas (vazio no Google) e `ISBLANK("")` = FALSE, que a camada neutraliza.
- **(e) Reuso sem alterar a ficha:** `gerar_ficha._tokens/_RE_REF/_limites/MSG_ERRO_*`, `testar_ficha.risco_google/_lint_google/_valor_de_erro`.
- **(f) Fases 2 a 4:** toda aba nova usa `ent()` (ou registra as vagas em `MAPA.tabelas`) para que `proteger` a cubra; o lint cobra.

---

## 1. Entregáveis (nomes exatos) e conferência contra o pedido

Pasta: `g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\Mestre\`, que já existe e está vazia. Ao fim da Fase 4, ela contém **exatamente** estes 3 arquivos (fora um `desktop.ini` do Drive, se aparecer):

1. `Mestre\Planilha do Mestre - Explorando Galáxias V1.2.xlsx`: o modelo em branco, com 18 abas (D3).
2. `Mestre\Planilha do Mestre - Exemplo.xlsx`: o mesmo modelo, com a campanha "O Lacre do Poço Sete" (§14).
3. `Mestre\COMO-USAR-PLANILHA-DO-MESTRE.md`: o guia (§15).

O item 1 nasceu `…V1.1.xlsx` (o design e a Fase 1 usaram esse nome, como a ficha da época). **Decisão do usuário**, registrada em `notas-fase2.md` (07/10) e confirmada em `notas-fase4.md` (09/10): o livro e a ficha passaram para a v1.2, então o modelo é o **V1.2** e o `…V1.1.xlsx` fica na pasta como registro, até o usuário decidir se o apaga. A suíte `entregaveis` trata esse arquivo como registro conhecido, não como sobra.

Os nomes são as constantes únicas `SAIDA_MODELO`, `SAIDA_EXEMPLO` e `SAIDA_GUIA` em `build\mestre\nucleo.py` (D2). Da Fase 1 em diante, a suíte `lint` confere que os dois `.xlsx` existem com esses nomes. A suíte `entregaveis` (Fase 4) confere os 3 e que não sobrou outro arquivo na pasta, como um `.tmp.xlsx` esquecido.

Conferência item a item contra o pedido literal. Os trechos são: "criar uma pasta chamada Mestre, e criar essa planilha e tudo que o mestre usa la dentro"; "Criador de inimigos, criador de npcs, criador de aventuras, gerador de recompensas, gerador de varias coisas, etc"; "Não so geradores, mas tudo que eu precisaria para jogar uma campanha, e outras coisas que você achar interessante".

| R | Trecho literal do pedido | Onde fica | Fase | Prova (suíte) |
|---|---|---|---|---|
| R1 Criador de Inimigos | "Criador de inimigos" | aba Inimigos (§6.7), `aba_inimigos.py` | 1 | `oraculo` (3 modos × 20 níveis × 3 tipos × 4 Elementos; Ajustar 32 × 5), `ouro` (carcereiro de 28.4), `bestiario` |
| R2 Bestiário | "tudo que eu precisaria para jogar uma campanha" | aba Bestiário (§6.8) | 1 | `bestiario` (32 fichas, criatura por criatura), `dados` |
| R3 Construtor de Encontros | "tudo que eu precisaria para jogar" + "gerador de varias coisas" (encontro aleatório) | aba Encontros (§6.9) | 1 | `ouro` (27.4, 28.11), `oraculo` (500 encontros aleatórios), `determinismo` G=100 |
| R4 Rastreador de combate | "Não so geradores, mas tudo que eu precisaria para jogar" | aba Combate (§6.10) | 1 | `oraculo` (Fila em 300 estados + 4 empates fixos; fases de Boss; calculadora em 2 000 casos), `ouro` (19.4, 20.4, 20.5, 21.2, 23.4) |
| R5 Criador de NPCs | "criador de npcs" | aba NPCs (§6.6) | 2 | `oraculo`/`determinismo` G=200, `sabor` |
| R6 Criador de Aventuras | "criador de aventuras" | aba Aventuras (§6.11) | 2 | `oraculo`/`determinismo` G=300 |
| R7 Gerador de Recompensas | "gerador de recompensas" | aba Recompensas (§6.12) | 2 | `ouro` (24.5, 25.1), `oraculo`/`determinismo` G=400/410/420 |
| R8 Outros geradores | "gerador de varias coisas, etc" | abas Mundos e Improviso (§6.13–6.14) | 3 | `oraculo`/`determinismo` G=510…650 |
| R9 Gestão de campanha | "tudo que eu precisaria para jogar uma campanha" | Início, Campanha, Grupo, Sessões, Missões (§6.1–6.5) | 1 (parcial), 3 | `extremos`, `oraculo` (relógios H16, reputação H17, H23), `exemplo` |
| R10 Escudo do Mestre | "tudo que eu precisaria para jogar" | aba Escudo do Mestre (§6.15) | 3 | `dados` (lido da aba Dados), `lint` (A4 paisagem), `preview` |
| R11 Tabelas editáveis | "gerador de varias coisas" + "tudo que o mestre usa" | Tabelas e Minhas Tabelas (§6.16–6.17) | 1 (listas do livro), 2 (sabor), 3 (Minhas Tabelas) | `sabor`, `extremos` (listas vazias e cheias), `oraculo` G=701–710 |
| R12 Pasta + planilha + o que o Mestre usa | "criar uma pasta chamada Mestre, e criar essa planilha e tudo que o mestre usa la dentro" | os 3 entregáveis acima | 1–4 (as 2 planilhas em toda fase; o guia na 4) | `lint` (nomes), `exemplo`, `entregaveis`, `texto` (guia) |
| R13 Extras | "e outras coisas que você achar interessante" | calculadora de dano e Tenacidade e Fila prevista (Combate); rolador com semente, DT rápida e oráculo sim/não (Improviso); cartões de NPC; Ficha de Decisões; Sessão Zero | 1, 2, 3 | `oraculo`, `ouro` |

Nenhum R está resolvido só por leitura. Cada um só fecha quando a suíte da coluna "Prova" passa na fase indicada. O revisor de cada portão confere as linhas desta tabela que a fase dele cobre.

---

## 2. Arquitetura de arquivos (todos novos; nenhum arquivo da ficha é editado)

Em `build\` (D8, tamanhos-alvo de §3.1). Nenhum módulo passa de ~60 KB; se passar, ele é dividido no pacote.

| Arquivo | Papel | Nasce na fase |
|---|---|---|
| `build\gerar_mestre.py` | Ponto de entrada. Monta o workbook, chama `mestre.aba_*.montar(ctx)`, resolve marcadores, roda `ajustar_layout` e grava modelo, Exemplo e mapa via temporário na mesma pasta | 1 |
| `build\mestre_dados.py` | Parsers de 19–25, 27 e 28 e reuso de `ficha_dados`: `blocos()`, `listas()`, `bestiario()`, `acoes()`, `fases()`, `ancoras()`, `GERADORES`, `DIVERGENCIAS_DOCUMENTADAS` | 1 (cresce na 2 e na 3) |
| `build\mestre_sabor.py` (+ `build\mestre_sabor_nomes.py` se passar de 60 KB) | Tabelas de sabor | 2 (cresce na 3) |
| `build\mestre_lexico_extra.txt` | Palavras PT-BR das tabelas de sabor que não estão no livro | 1 (só o cabeçalho), 2 e 3 |
| `build\oraculo_mestre.py` | Oráculo independente: não importa `mestre_dados` nem `mestre\*` e não lê fórmula | 1 (sorteio + combate), 2, 3 |
| `build\testar_mestre.py` | CLI e suítes; delega a `build\mestre\testes_*.py` quando crescer | 1 |
| `build\mestre_mapa.json` | Gerado | 1 |
| `build\mestre_spike.json` | Gerado pela suíte `spike` | 1 |
| `build\mestre\__init__.py`, `nucleo.py`, `sorteio.py` | Infraestrutura | 1 |
| `build\mestre\aba_inicio.py`, `aba_campanha.py`, `aba_inimigos.py`, `aba_encontros.py`, `aba_combate.py`, `aba_tabelas.py` | Abas da Fase 1 | 1 |
| `build\mestre\aba_npcs.py`, `aba_aventuras.py`, `aba_recompensas.py` | Abas da Fase 2 | 2 |
| `build\mestre\aba_mundos.py`, `aba_escudo.py` | Abas da Fase 3 | 3 |
| `build\mestre\exemplo.py` | Entradas do Exemplo | 1 (parcial) → 4 |
| `build\mestre\testes_*.py` | Divisão da bateria se `testar_mestre.py` passar de 60 KB | quando precisar |

A aba Dados é montada por `nucleo.escrever_dados`, chamada de `gerar_mestre.py`.

**Reuso por import** (§3.2), com `sys.path.insert(0, BUILD)`. Todos os nomes foram conferidos e existem hoje:
- `gerar_ficha`: estilos, `COR_*`, `TAM_*`, `FONTE`, `VERSAO`, `_dv_lista`, `_dv_numero`, `formatar_avisos`, `_px_largura`, `larguras`, `legenda`, `texto_dano`, `sinal` etc.
- `ficha_dados`: `secao`, `tabelas`, `tabela`, `limpar`, `num`, `dados` e os 28 parsers listados em §3.2.
- `renderizar_ficha`: `medir`, `px_coluna`, `px_linha`, `quebrar`, `tabelas`, `contraste`, `PiorTexto`, `renderizar_estado`, `gravar_indice`, `gravar_recortes`, `LADO_RECORTE`.
- `testar_ficha`: `Modelo`, `Resultado`, `normalizar_valor`, `eh_erro`, `_igual`, `separar_ref`, `_checar_formula`, `_tem_emoji`, `_sha256`, `_arquivos_protegidos`, `_textos_visiveis(caminho)`, `_lexico`, `_proibidas_ps1`, `_glossario_30_1`, `_sem_acento_mesmo_tamanho`, `ler_funcoes_ok`.
- `oraculo_ficha`: `calcular`, `eficiencia`, `faixa`, `ph_grupo`.

**Cuidados conferidos no código da ficha:**
- `gerar_ficha` tem estado global (`REFS`, `MAPA = Mapa()`). A Mestre **não** usa `gerar_ficha.reg/ref/ent/cal/av/aux/resolver_marcadores/escrever_dados/ajustar_layout`; tem os seus em `nucleo`, com registro próprio (D8, §3.1). Nunca chamar `gerar_ficha.gerar()` nem `gravar_exemplo_nadir()`: eles regravariam `ficha_mapa.json` e a ficha.
- `testar_ficha._textos_visiveis` usa a ficha por padrão. Passar sempre o caminho da planilha da Mestre.
- `testar_ficha._proibidas_ps1` lê `scripts\checar-nomenclatura.ps1` na raiz, que existe.
- Em `testar_ficha.Modelo.calcular`, a entrada `None` é omitida, o que equivale a célula vazia. As chaves do `formulas` são `'[Arquivo.xlsx]ABA'!A1`, e `Modelo.chave` as resolve.
- `testar_ficha.suite_spike` usa o prefixo `spike_ficha_`. O spike da Mestre é próprio e usa o prefixo `mestre-`.

---

## 3. Ambiente e comandos

- **Shell:** Windows + PowerShell 5.1. Separar comandos com `;`, pôr aspas duplas em todo caminho, rodar `$env:PYTHONUTF8="1"` antes de todo `python`, usar `cwd` = raiz do workspace. **Sem git:** não há worktree nem commit. O "estado bom" de cada fase é o disco + `PROGRESSO.md`.
- **Gerar:** `$env:PYTHONUTF8="1"; python "build\gerar_mestre.py"`. Saída: as 2 planilhas em `Mestre\` + `build\mestre_mapa.json`, com uma linha por saída (abas, fórmulas, validações, tempo). Código ≠ 0 em qualquer erro fatal de §10.2.
- **Testar:** `$env:PYTHONUTF8="1"; python "build\testar_mestre.py" --suite <nome|fase1|fase2|fase3|tudo> --saida "<arquivo.txt>"`. Código 1 em qualquer falha.
- **Temporários:** sempre `tempfile.mkdtemp(prefix="mestre-", dir=os.environ["TEMP"])`, apagados em `finally`. O gerador grava `<nome>.tmp.xlsx` na pasta de destino e troca com `os.replace`. Se o destino estiver bloqueado (Excel/Drive), apaga o temporário e sai com "feche o arquivo". Ao fim de cada fase, `Get-ChildItem "$env:TEMP" -Filter "mestre-*"` tem de vir vazio, e `Mestre\` não pode ter `*.tmp.xlsx`.
- **Imagens:** nunca abrir PNG com lado > 1800 px. Conferir antes com Pillow: `python -c "from PIL import Image; print(Image.open(r'<png>').size)"`. No máximo 4 por vez, e só os `-parte-NN.png` de `.agents\tasks\mestre\preview\`.
- **Tempo:** carregar o modelo no `formulas` é lento. Usar `outputs` restritos, um `Modelo` por processo e até 8 processos (`multiprocessing`, no padrão de `testar_ficha._extremos_iniciar/_trabalhar`). A meta da bateria inteira é ≈ 20 min (§16). Suíte longa roda com `timeout` explícito (até 1 800 000 ms) ou em segundo plano.
- **Economia:** não ler inteiros os arquivos grandes da ficha (`gerar_ficha.py` 234 KB, `testar_ficha.py` 201 KB, `ficha_mapa.json` 201 KB) nem o `design.md` (132 KB). Usar busca dirigida pelo nome da função ou da seção.

---

## 4. Fase 1 — Combate e preparação de combate (R1–R4; R9 e R11 parciais)

Abas com conteúdo: Início (título, semente, índice), Campanha (só Mesa e calculadas), Grupo (entradas + resumo), Inimigos, Bestiário, Encontros, Combate, Tabelas (só `ambiente_por_faccao` e as listas do livro de 27.16–27.18) e Dados. As outras 9 abas existem na ordem final de D3, com título, legenda e a linha "Em construção" (texto fixo, sem fórmula).

- [ ] 1.1 **Spike dos padrões novos.** Criar `build\testar_mestre.py` com a CLI (`--suite`, `--saida`, os atalhos de P12, o `Resultado` de `testar_ficha`) e a suíte `spike` de §12.1. Ela monta um workbook mínimo em `$env:TEMP\mestre-spike-*` com: `MOD` sobre 2³¹·16807; 3 `MOD` aninhados (`L3`); `Q` e `X` nos extremos (S = 1 e 2 147 483 646; G = 100 e 710; R = 1 e 1 000 000; C = 1 e 400); `INT(x*n/M)`; `INDEX(MATCH(k, contador corrido))`; `SMALL`+`MATCH` com chaves fracionárias; `CHOOSE(MATCH())` sobre 7 intervalos; `REPT("●",n)`; e validação de lista apontando para outra aba. Compara tudo com Python e grava `build\mestre_spike.json`. **Não** regrava `ficha_funcoes_ok.json`.
      Arquivos: `build\testar_mestre.py`.
      Verificar: `python "build\testar_mestre.py" --suite spike` → 0 divergência. Se divergir, seguir P14.

- [ ] 1.2 **Núcleo, esqueleto do gerador e suítes de base.**
      - `build\mestre\__init__.py`.
      - `build\mestre\nucleo.py`, com tudo de §3.1:
        - constantes `SAIDA_*`;
        - `MapaMestre`, no formato de `ficha_mapa.json` mais as chaves `subtabelas`, `entradas`, `avisos`, `sugestoes`, `constantes`, `geradores` e `numeros_de_regra` (P10);
        - `reg`/`T`/`ref`/`resolver_marcadores`, com «nome.logico»;
        - `ent`, que nunca escreve valor e recusa nome repetido (D9);
        - `cal(…, regra=False)`, `av`, `aux` (sempre em coluna oculta à direita de L), `rot`, `cabecalhos`, `sugestao(H#)`;
        - `cabecalho_aba` (linhas 1–3, título "‹Aba› — Explorando Galáxias v1.1");
        - `escrever_dados`;
        - `ajustar_layout`, com a régua `renderizar_ficha.medir`, a grade A:L de D11 e área ≤ 1360 px; é fatal se o texto não couber.
      - `build\gerar_mestre.py`: cria as 18 abas de D3 com título, legenda e "Em construção", liga `fullCalcOnLoad = True` e grava via temporário. Por enquanto, o Exemplo é cópia do modelo.
      - Em `testar_mestre.py`, as suítes `protegidos` (P4, P5) e `lint` (§12.1 inteiro, com P3).
      Arquivos: `build\mestre\__init__.py`, `build\mestre\nucleo.py`, `build\gerar_mestre.py`, `build\testar_mestre.py`, `build\mestre_lexico_extra.txt`.
      Verificar: `python "build\gerar_mestre.py"` grava as 2 planilhas com os nomes de D2; `--suite protegidos` → 0 alterado (1 info, do P5); `--suite lint` → 0 achado.

- [ ] 1.3 **Sorteio e oráculo do sorteio.**
      - `build\mestre\sorteio.py`, o único construtor: `semente_efetiva`, `rolagem`, `valor` (com `u`/`y`/`x` exatamente como em §5), `escolha`, `escolha_sem_repetir`, `varios_sem_repetir` (com o passo primo de §6.17), `inteiro`, `dado` e `TAMANHO`.
      - `GERADORES` em `mestre_dados.py`, com ids G/C estáveis.
      - `build\oraculo_mestre.py`, com o sorteio reimplementado e `assert` de limites < 2⁵³ para todo G/C usado.
      - Suíte `determinismo`, com as propriedades (a)–(g) de §5 no oráculo, incluindo G = 650 e as 216 triplas de d6. A parte "planilha = oráculo em 300 rolagens" entra quando houver gerador (item 1.7).
      - Semente na aba Início, com a validação e o aviso de §5.
      Arquivos: `build\mestre\sorteio.py`, `build\mestre_dados.py`, `build\oraculo_mestre.py`, `build\mestre\aba_inicio.py`, `build\testar_mestre.py`.
      Verificar: `--suite determinismo` → todas as propriedades valem; `--suite lint` → 0.

- [ ] 1.4 **Dados do livro: parsers, aba Dados e aba Tabelas (parte do livro).**
      - Em `mestre_dados.py`, os blocos de §4.1 dos caps. 19–23, 27.2–27.7 e 28, reaproveitando os parsers de `ficha_dados`. Os blocos são:
        - do cap. 28: âncoras 28.3, `dano_dados`, `dano_especial` (com H2), `bestiario` (32 fichas), `bestiario_fases` (12 linhas) e `bestiario_acoes` (com o texto-modelo de §6.7.3);
        - do cap. 27: `orcamento`, `composicoes`, `attrition`, as DTs, `faccoes`/`locais`/`ganchos` e `casos_limite`;
        - de combate: `fila`, `elementos`, `fraqueza_resistencia`, `tenacidade`, `condicoes`, `morrendo`/`descanso`/`execucao` e `ph`/`energia`/`ultimate_faixa`;
        - os demais: `racas`, `caminhos` e `tetos`.
      - Toda leitura falha alto, com capítulo e seção. As divergências seguem P13.
      - Formato da ficha a parsear (conferido em "### Casco Oco"): linha de tipo `*Comum · Fragmentum · faixa 1-4*`, frase em citação, tabela `| Campo | Valor |`, listas **Ataques** e **Ações especiais** e a linha **Na Fila:**. Execução só aparece em parte das fichas; na implementação, conferir quantas. As demais ficam "Não declarado".
      - `aba_tabelas.py`: as listas do livro (27.16–27.18) e `ambiente_por_faccao` (H8), com 100 vagas em 8 faixas de 13, contador corrido, "Tamanho da lista" e "Fonte" (§4.2).
      - Suítes `dados` e `bestiario` (§12.1), com **parser próprio do teste** (não importa `mestre_dados`) e relatório criatura por criatura: uma linha "OK/✗ <nº> <nome>: campos, fases, ações" por ficha.
      Arquivos: `build\mestre_dados.py`, `build\mestre\nucleo.py`, `build\mestre\aba_tabelas.py`, `build\gerar_mestre.py`, `build\testar_mestre.py` (ou `build\mestre\testes_dados.py`).
      Verificar: gerar; `--suite dados` → 0 diferença; `--suite bestiario` → 32/32 fichas OK, 12 fases, H2 e H4 conferidos; `--suite lint` → 0.

- [ ] 1.5 **Campanha (Mesa), Grupo e Início (base).**
      - `aba_campanha.py`:
        - na Campanha, só a Mesa (nível do grupo, nº de jogadores, sessão, dia) e as calculadas (faixa, Eficiência, PH), conforme D9;
        - o Grupo completo de §6.3: G1–G4 em 4 sub-tabelas de 6 linhas, resumo do grupo e avisos.
      - `aba_inicio.py`: título, semente e índice das 18 abas.
      - Oráculo: faixa, Eficiência, PH (16.2) e os avisos do Grupo (VEL 7–25, Raças).
      Arquivos: `build\mestre\aba_campanha.py`, `build\mestre\aba_inicio.py`, `build\oraculo_mestre.py`, `build\gerar_mestre.py`.
      Verificar: gerar; `--suite lint` → 0; `--suite extremos` (estado em branco + os 3 estados de P9) → 0 erro.

- [ ] 1.6 **Bestiário e Inimigos (R1, R2).** Tudo em `aba_inimigos.py`.
      - **Bestiário (§6.8):** filtros por faixa, tipo, Elemento, facção e ambiente, com `SUMPRODUCT(ISNUMBER(ordem)*1)`; ficha completa; sub-tabelas 11 + 11 + 10; Execução em B:J (P7).
      - **Inimigos (§6.7):**
        - 6.7.1: modos Faixa, Nível (H1) e Ajustar do bestiário; sub-tabelas I1–I5, com o Inimigo na coluna A na I5 (P8);
        - 6.7.2: Fraquezas sugeridas, G = 110 (H12);
        - 6.7.3: ficha detalhada e ações por marcadores (H3).
      - **Oráculo:** o Criador nos 3 modos; H1 (só o PV é interpolado; os demais números e o Dano são a âncora); H3; H12. Ligar `numeros_de_regra`.
      Arquivos: `build\mestre\aba_inimigos.py`, `build\oraculo_mestre.py`, `build\gerar_mestre.py`.
      Verificar: gerar; `--suite oraculo` (casos de Criador, Ajustar, H1 e H12) → 0 divergência, com a tabela de desvio de PV de H1 impressa e ≤ 20%; `--suite bestiario` → 0; `--suite lint` → 0.

- [ ] 1.7 **Encontros (R3).** `aba_encontros.py`, conforme §6.9:
      - orçamento por faixa e por nº de PJs (H5), com 3 encontros salvos (do bestiário e criados);
      - custo, dificuldade (H6) e Ciclos (H7);
      - composições de 27.4/28.11, contrato da Fraqueza e regra irmã (27.5), DT para descobrir Fraqueza (20.2);
      - Ressonâncias e marcos, sem XP (26.1);
      - encontro aleatório, G = 100, por ambiente e faixa, com a troca sugerida H19;
      - linha de saída com as colunas na ordem de "Encontros salvos" (D6).
      Fazer o oráculo correspondente. A partir daqui, `determinismo` passa a conferir `u`/`y`/`x` da planilha em 300 rolagens para G = 100 e 110.
      Arquivos: `build\mestre\aba_encontros.py`, `build\oraculo_mestre.py`, `build\gerar_mestre.py`, `build\testar_mestre.py`.
      Verificar: gerar; `--suite ouro` (orçamento de 27.4 nas 5 faixas, composições de 28.11) → 0; `--suite oraculo` (500 encontros × 3 grupos) → 0; `--suite determinismo` → todas valem.

- [ ] 1.8 **Combate (R4).** `aba_combate.py`, com §6.10 inteira (C0–C10):
      - **Combatentes:** 16, em blocos de 10 + 6; o inimigo escolhido da lista preenche os próprios dados.
      - **Fila do Ciclo:** chave de 3 termos (PJ ≥ 15 000 + …, inimigo só `T_linha`); Atraso, teto e Firmeza (19.4); Avanço e Avanço Total (19.5); Congelamento (19.6); Surpresa (19.3); Fila prevista e quem age agora.
      - **Dano e estado:** PV, PV temporário e cura perdida; Tenacidade, Quebra e Dano de Quebra por Elemento com a Eficiência; condições com duração, acúmulo e tetos (21.5, inclusive Embaraço e Aprisionamento); Dano Contínuo; Morrendo e Executado.
      - **Recursos:** PH, Energia, Ultimate e Esforço; recargas.
      - **Fases do Boss:** fase da barra × fase em vigor (28.5), com as 3 linhas "Virar a fase" e as 4 linhas "Avançar o Ciclo".
      - **Calculadora de dano:** Fraqueza ±2 dados, teto +3, mínimo 1.
      - **Constantes procedimentais:** em `constantes` do mapa, cada uma com a sua seção.
      Arquivos: `build\mestre\aba_combate.py`, `build\oraculo_mestre.py`, `build\gerar_mestre.py`.
      Verificar: gerar; `--suite ouro` → 0, com os casos 19.4 (7→2 e 1→1), 21.2 (Sangramento 365→18 e 935→24), 20.5 (Quebra de Fogo `2d6 + 4 · 11` e `2d6 + 16 · 23`, Gelo 2 e 8), 20.4 (12−4−1−1−2 = 4), 23.4 (Vesper), 16.2 e 23.6. `--suite oraculo` → 0, com Fila em 300 estados + 4 empates fixos, fases dos 5 Bosses e de Boss criado, calculadora em 2 000 casos, e Embaraço/Aprisionamento.

- [ ] 1.9 **Exemplo parcial e suítes transversais.** `build\mestre\exemplo.py` com o que a Fase 1 já tem (§14):
      - Campanha: Mesa e semente 2026.
      - Grupo: os 4 PJs calculados por `oraculo_ficha.calcular`. A Nadir é a de 29.7 (PV 61, Defesa 16, Esquiva 18, RD 0, VEL 14, DT 14, Presença +0). Se o oráculo da ficha avisar, é fatal.
      - Inimigos da campanha: Carcereiro Orbital e Capataz do Duto 4.
      - Encontros A e B, e o estado de Combate do Ciclo 2.
      Ligar também as suítes `extremos`, `texto`, `preview` e `visual` (seção 8 deste plano) para as abas da fase.
      Arquivos: `build\mestre\exemplo.py`, `build\gerar_mestre.py`, `build\testar_mestre.py`.
      Verificar: gerar; `--suite extremos` → 0 erro; `--suite texto` → 0; `--suite preview` e `--suite visual` → 0 texto cortado nos 3 estados, com os recortes conferidos conforme P6 (no máximo 4 por vez).

- [ ] 1.10 **Portão da Fase 1.** Rodar `python "build\testar_mestre.py" --suite fase1 --saida ".agents\tasks\mestre\suite-fase1.txt"`. Atualizar `PROGRESSO.md` (item 3 marcado, checagens e falhas por suíte, recortes olhados). Limpar os temporários.
      Suítes de `fase1`: `spike`, `protegidos`, `dados`, `bestiario`, `ouro` (combate e encontro), `oraculo` (Criador, Ajustar, encontros, Fila, fases, calculadora), `determinismo` (G = 100 e 110, mais (g) com G = 650), `extremos`, `lint`, `texto`, `preview`, `visual`.
      **Pronto quando:** `gerar_mestre.py` grava as 2 planilhas sem erro, o lint dá 0, todas as suítes de `fase1` têm 0 falha e o `PROGRESSO.md` está atualizado.

---

## 5. Fase 2 — História: NPCs, Aventuras, Recompensas (R5–R7; sabor de R11)

- [ ] 2.1 **Tabelas de sabor.**
      - `build\mestre_sabor.py`, com as tabelas de NPC, aventura, recompensa e o sabor de Cone e de Conjunto. Cada tabela tem `id`, título, fonte e valores: ≥ 20 entradas por tabela e nomes ≥ 30 por cultura, em texto original PT-BR, sem nome de personagem do jogo.
      - `aba_tabelas.py` passa a escrever essas listas, marcando `sem_ortografia` nas de nomes.
      - As palavras novas legítimas vão para `mestre_lexico_extra.txt`.
      - Suíte `sabor` (§12.1), com a lista de nomes proibidos do jogo dentro do próprio teste.
      Arquivos: `build\mestre_sabor.py`, `build\mestre\aba_tabelas.py`, `build\mestre_lexico_extra.txt`, `build\testar_mestre.py`.
      Verificar: `--suite sabor` → 0; `--suite texto` → 0.

- [ ] 2.2 **NPCs (R5).** `aba_npcs.py`, conforme §6.6:
      - gerador G = 200: nome por cultura, Raça, Caminho, ocupação, aparência (2 traços, H25), personalidade, motivação, segredo, maneirismo/voz, atitude, gancho (H20), papel e bloco de combate opcional pelas âncoras;
      - linha de saída na ordem do Elenco (D6);
      - Elenco de 30 e cartões.
      Arquivos: `build\mestre\aba_npcs.py`, `build\oraculo_mestre.py`, `build\gerar_mestre.py`.
      Verificar: gerar; `--suite oraculo` e `--suite determinismo` com G = 200 → 0 divergência e (a)–(g) valendo; H20 entre 45% e 55% em 2 000 rolagens.

- [ ] 2.3 **Aventuras (R6).** `aba_aventuras.py`, conforme §6.11:
      - gerador G = 300: tipo, gancho (H20), contratante, objetivo, local, antagonista (H22), complicação, reviravolta, prazo/risco e 5 cenas (H14);
      - recompensa por C = 13/14, sem ler a aba Recompensas;
      - linha de saída na ordem de Missões.
      Arquivos: `build\mestre\aba_aventuras.py`, `build\oraculo_mestre.py`, `build\gerar_mestre.py`.
      Verificar: `--suite oraculo`/`determinismo` com G = 300 → 0; H22 nunca vazio em nenhuma combinação de facção × faixa.

- [ ] 2.4 **Recompensas (R7).** `aba_recompensas.py`, conforme §6.12:
      - entrega de marco: verba (24.5), Cone e Tier (25.1), Sobreposição (25.2), Ressonâncias (26.7);
      - achados de encontro, G = 400: créditos (H18) e 0–2 consumíveis (H9);
      - Cone, G = 410, e Conjunto, G = 420 (sabor);
      - Tesouro do grupo.
      O Exemplo ganha os NPCs do Elenco (Rolagens 1–6 copiadas como valores) e 2 linhas de Tesouro.
      Arquivos: `build\mestre\aba_recompensas.py`, `build\mestre\exemplo.py`, `build\oraculo_mestre.py`, `build\gerar_mestre.py`.
      Verificar: `--suite ouro` (24.5, 25.1, 27.9) → 0; `--suite oraculo`/`determinismo` com G = 400, 410 e 420 → 0; H9 com cada valor entre 28% e 39% em 3 000 rolagens.
      **Decisão (revisão da Fase 2, F2):** 27.9 (Ultimate por faixa) só aparece no Escudo do Mestre (design §6.15), que é da Fase 3. O `ouro` da Fase 2 cobre 24.5 e 25.1 (mais 25.2, 25.3, 26.7 e 24.1–24.3), e o caso de 27.9 entra no `ouro` do item 3.3.

- [ ] 2.5 **Portão da Fase 2.** Rodar `--suite fase2 --saida ".agents\tasks\mestre\suite-fase2.txt"`, atualizar `PROGRESSO.md` e limpar os temporários.
      Suítes de `fase2`: todas as de `fase1` + `sabor`. `oraculo`/`determinismo` passam a cobrir também G = 200, 300, 400, 410 e 420, e `preview`/`visual` incluem NPCs, Aventuras e Recompensas.
      **Pronto quando:** as 2 planilhas são geradas, o lint dá 0 e as suítes de `fase2` têm 0 falha.

---

## 6. Fase 3 — Campanha completa, demais geradores, Escudo, Minhas Tabelas (R8–R11, R13)

- [x] 3.1 **Campanha completa e Grupo (R9).** Em `aba_campanha.py` (§6.2–6.5):
      - Campanha: marcos e progressão (26.1); facções e reputação (H17); relógios (H16); linha do tempo com "Próximos eventos"; Ficha de Decisões (27.11/29.11); Sessão Zero (H24 só nos 2 itens de tom e limites).
      - Grupo: todas as checagens.
      - Sessões: preparação com 5 cenas, encontros ligados e pistas; diário.
      - Missões: com o aviso H23.
      Arquivos: `build\mestre\aba_campanha.py`, `build\oraculo_mestre.py`, `build\gerar_mestre.py`.
      Verificar: `--suite oraculo` → 0, com H16 nos 45 casos + entradas inválidas, H17 nos 7 rótulos + vazio + fora da faixa + facção repetida, e H23 com 3 e com 4 Ativas; `--suite extremos` → 0.

- [x] 3.2 **Mundos e Improviso (R8, R13).** Em `aba_mundos.py` (§6.13–6.14):
      - geradores G = 510–560 (planeta/local, estação, nave, facção, organização, nomes avulsos);
      - geradores G = 600–650 (rumor, evento, loja com preços de 24 e H15, bugiganga, oráculo sim/não H10, rolador de dados);
      - DT rápida (27.2/27.3).
      As listas de sabor vão para `mestre_sabor.py`/`aba_tabelas.py`.
      Arquivos: `build\mestre\aba_mundos.py`, `build\mestre_sabor.py`, `build\mestre\aba_tabelas.py`, `build\oraculo_mestre.py`, `build\gerar_mestre.py`.
      Verificar: `--suite oraculo`/`determinismo` com G = 510…650 → 0, com (g) no rolador; `--suite sabor` → 0; todo preço da loja igual ao livro.

- [x] 3.3 **Escudo do Mestre e Minhas Tabelas (R10, R11).**
      - `aba_escudo.py` (§6.15): 5 páginas A4 paisagem lidas da aba Dados, com as linhas "— Escudo do Mestre · página N de 5 · título —" (o design pedia 3; com o corpo em 9 pt o conteúdo pede 5; revisão da Fase 3, F3: o título de cada página diz o que ela tem). O guia da Fase 4 diz "página N de 5".
      - Em `aba_tabelas.py`, Minhas Tabelas (§6.17): G = 701–710, com "quantos sortear" e `varios_sem_repetir`.
      Arquivos: `build\mestre\aba_escudo.py`, `build\mestre\aba_tabelas.py`, `build\gerar_mestre.py`.
      Verificar: `--suite lint` → 0, com o Escudo em A4 paisagem; `--suite dados` → 0, com o Escudo igual à aba Dados; `--suite oraculo` → 0 para G = 701–710, sem repetição enquanto "quantos" ≤ n; `--suite ouro` → 0 com 27.9 (Ultimate por faixa) calculado no Escudo (adiado da Fase 2, item 2.4).

- [x] 3.4 **Início completo.** Painel, índice e avisos agregados (§6.1), incluindo os relógios com n = s−1.
      Arquivos: `build\mestre\aba_inicio.py`.
      Verificar: `--suite extremos` → 0 erro, e o modelo em branco sem nenhum aviso aceso.

- [x] 3.5 **Portão da Fase 3.** Rodar `--suite fase3 --saida ".agents\tasks\mestre\suite-fase3.txt"`. `fase3` = todas as suítes menos `exemplo` e `entregaveis`, sobre as 18 abas. Nenhuma aba mostra mais "Em construção" nem "próxima fase" (revisão da Fase 3, F1), e o lint confere isso a partir desta fase.
      **Pronto quando:** as 2 planilhas são geradas, o lint dá 0 e as suítes de `fase3` têm 0 falha.

---

## 7. Fase 4 — Exemplo, guia e auditoria (R12)

- [x] 4.1 **Exemplo completo.** (09/10: feito, com o Memoespírito e as condições do pedido do usuário; `exemplo` 47 852 checagens, 0 falha) `exemplo.py` com §14 inteira: facções, relógios, linha do tempo, Ficha de Decisões, Sessão Zero, 3 missões, sessão 2 preparada + 1 linha de diário, entrega de marco do nível 2, "Clima no Expresso" com 12 entradas e semente 2026. Suíte `exemplo` (§12.1). Ela confere: os 4 PJs contra `oraculo_ficha.calcular`; o encontro A com custo 320 de 352 (91%), "típico" e contrato cumprido com 3; a Fila do Ciclo 1 igual à do oráculo; e toda fórmula sem erro.
      Arquivos: `build\mestre\exemplo.py`, `build\testar_mestre.py`.
      Verificar: `--suite exemplo` → 0.

- [x] 4.2 **Guia.** (09/10: feito em 12 seções, que cobrem as de §15 mais Memoespírito, condições e IMPORTRANGE; `texto` e `guia` → 0) `Mestre\COMO-USAR-PLANILHA-DO-MESTRE.md`, com as 14 seções de §15, no estilo de `ficha-automatizada\COMO-USAR-NO-GOOGLE-PLANILHAS.md`:
      - impressão no Google passo a passo;
      - os 4 passos de "Avançar o Ciclo" e os 3 de "Virar a fase";
      - a tabela gerador → registro;
      - checklist de 2 minutos com valores **lidos do Exemplo calculado**, não digitados de memória;
      - lista H1–H25.
      A suíte `texto` passa a cobrir o `.md`: ortografia, glossário 30.1, termos de 30.2, e toda célula ou valor citado no guia conferido contra o Exemplo calculado.
      Arquivos: `Mestre\COMO-USAR-PLANILHA-DO-MESTRE.md`, `build\testar_mestre.py`.
      Verificar: `--suite texto` → 0.

- [x] 4.3 **Auditoria interna e saída completa.** (09/10: `tudo` 10 979 281 checagens, 0 falha; o AUDITORIA.md é o `relatorio-final.md`) Rodar `python "build\testar_mestre.py" --suite tudo --saida ".agents\tasks\mestre\suite-tudo.txt"`. `tudo` = todas as suítes de §12.1 + `entregaveis` (os 3 arquivos com os nomes exatos e nada mais em `Mestre\`).
      Escrever `.agents\tasks\mestre\AUDITORIA.md`, com:
      - o resultado por suíte;
      - a tabela de desvio do PV de H1 por tipo;
      - a tabela de correlação da semente;
      - H1–H25 com o resultado da validação de cada uma;
      - as divergências e lacunas do livro (seção 9);
      - os recortes olhados.
      Atualizar `PROGRESSO.md` (itens 6 e 7) e limpar os temporários.
      Verificar: `suite-tudo.txt` termina com o RESUMO de todas as suítes em OK e o código de saída é 0.
      **Pronto quando:** `tudo` passa com 0 falha, os 3 entregáveis existem com os nomes da seção 1, a ficha e o livro estão intocados, e `AUDITORIA.md` e `PROGRESSO.md` estão atualizados.

---

## 8. Especificação das suítes de verificação (`build\testar_mestre.py`)

Todas usam `testar_ficha.Modelo` (`formulas` 1.3.4) e `Resultado`, e saem com código 1 em qualquer falha. A tabela de §12.1 é o contrato. Abaixo está o que este plano acrescenta ou deixa explícito. A meta de todas é 0 falha.

| Suíte | Exigência | Fases |
|---|---|---|
| `spike` | §12.1 e P14 | 1–4 |
| `protegidos` | **Livro intocado:** os SHA-256 de `testar_ficha._arquivos_protegidos()` (livro, `.docx`, `.pdf`, `gerar_docx.py`, `gerar_pdf.py`) iguais a `build\ficha_protegidos.json`, e nenhum arquivo novo em `livro-v1.0\`. **Ficha intocada:** os 14 hashes de `.agents\tasks\mestre\baseline-hashes.json`, com a exceção de P5. Só leitura (P4) | 1–4 |
| `dados` | Parser próprio do teste × aba Dados e listas "Livro" da aba Tabelas: 0 diferença | 1–4 |
| `bestiario` | **Conferência criatura por criatura** das 32 fichas: os 15 campos de 28.1, a Execução, as Fraquezas e Resistências, as fases (12 linhas) e cada ataque/ação renderizado na faixa original igual à linha do `.md`. Cada número contra 28.3, exceto as entradas de `DIVERGENCIAS_DOCUMENTADAS`, e contra o índice de 28.11. Imprime uma linha por criatura | 1–4 |
| `ouro` | Os números impressos no livro, calculados **na planilha** (§12.1) | 1–4 (cresce por fase) |
| `oraculo` | **Oráculo independente para todo número de regra:** `oraculo_mestre` × planilha com 0 divergência. A cobertura vem de P10: toda célula de `numeros_de_regra` comparada. Os avisos são conferidos nos dois sentidos | 1–4 |
| `determinismo` | **Determinismo dos geradores:** (a)–(g) de §5. Para cada G existente, `u`/`y`/`x` iguais aos do oráculo em 300 rolagens × 3 sementes. Recalcular duas vezes dá o mesmo resultado. 50 entradas fora da tabela de parâmetros não mudam nenhum sorteio, e cada parâmetro listado muda pelo menos um campo | 1–4 |
| `extremos` | **Recálculo com `formulas` 1.3.4 sem nenhuma célula de erro**, em todas as fórmulas, nos estados: modelo em branco; Exemplo; ~200 sementes (P15); grupo com 1 PJ, grupo cheio (6) e nº de jogadores 8 (P9); nível 1 e 20; 1 e 6 jogadores; listas da aba Tabelas **vazias** e **cheias** (100 vagas); Combate com os 16 combatentes ocupados e todos os estados (Congelado, Morrendo, derrotado, Surpresa, Avanço, fases); um campo por vez com valor válido e inválido (amostras de `entradas` do mapa). Também confere que o aviso esperado aparece na coluna certa, que o modelo em branco não tem aviso e que não há referência circular | 1–4 |
| `lint` | **Lint Google com 0 achado:** §12.1 inteiro + P3, os nomes dos entregáveis e, da Fase 3 em diante, nenhum "Em construção" | 1–4 |
| `texto` | **Ortografia PT-BR e glossário:** termos proibidos (`_proibidas_ps1`), aposentados de 30.2, grafia de 30.1 (`_glossario_30_1`), léxico do livro + `mestre_lexico_extra.txt`, formas sem acento, emoji. Abrange o texto visível das 2 planilhas (`_textos_visiveis(caminho)`) e, na Fase 4, o guia. Também exige o rótulo "Sugestão da planilha — não é regra do livro (H#)" em toda célula de `sugestoes` | 1–4 |
| `sabor` | §12.1 | 2–4 |
| `preview` / `visual` | **Prévia visual renderizada** em `.agents\tasks\mestre\preview\`: só recortes ≤ 1800 px (P6), em 3 estados (em branco, Exemplo, pior caso), nas abas da fase. **0 texto cortado**, listas com espaço para a seta, avisos medidos pela mensagem mais longa, contraste ≥ 4,5:1, fonte ≥ 9 pt, distância ≤ 15 linhas ao cabeçalho e área ≤ 1360 px. O coder abre recortes (no máximo 4 por vez, conferindo o tamanho com Pillow antes) e registra em `PROGRESSO.md` o que viu | 1–4 |
| `exemplo` | §12.1 + item 4.1 | 4 |
| `entregaveis` | Os 3 arquivos com os nomes exatos da seção 1 e nada mais em `Mestre\` | 4 |
| `tudo` | Todas, nesta ordem. A saída completa vai para `.agents\tasks\mestre\suite-tudo.txt` (P11) | 4 |

---

## 9. Heurísticas "Sugestão da planilha" e o livro

### 9.1 Heurísticas (fora do livro) e método de validação

Toda célula de heurística sai de `nucleo.sugestao("H#")`, fica registrada em `sugestoes` e mostra "Sugestão da planilha — não é regra do livro (H#)". Método e validação completos estão em §8 do design. Este é o resumo do que a bateria executa:

| H | O quê | Validação executada (suíte) |
|---|---|---|
| H1 | PV por nível dentro da faixa | erro 0 nos níveis 3/7/11/15/19; as 32 fichas idênticas no nível de referência; os demais 10 números e o Dano com desvio 0; o PV com desvio ≤ 20%, com a tabela publicada (`oraculo`) |
| H2 | Dano de especial 1,5× sem ficha | células "ficha" lidas do `.md`; média = `INT(1,5 × âncora)` nas 15 (`bestiario`) |
| H3 | Reescala de ação | 0 diferença na faixa original; `{TEN}` ≤ âncora (`bestiario`, `oraculo`) |
| H4 | Limiares de fase | as barras das 5 fichas (`bestiario`) |
| H5 | Grupo ≠ 4 | com 4, igual a 27.4 nas 5 faixas (`ouro`) |
| H6 | Rótulos de dificuldade | composições em "típico"; metade em "passagem" (`oraculo`) |
| H7 | Ciclos estimados | 3,6–4,2 nas composições; Combate A de 29.5 = 4,0 (`ouro`) |
| H8 | Ambiente por facção | toda criatura com ≥ 1 ambiente; todo ambiente com criatura em ≥ 2 faixas (`dados`) |
| H9 | Consumíveis | item e preço de 24.3; 0–2 com cada valor entre 28% e 39% em 3 000 rolagens; poção da faixa (`oraculo`) |
| H10 | Oráculo sim/não | distribuição; 50/50 = 50% (`oraculo`) |
| H11 | Pesos de sabor | contagem nas listas (`sabor`) |
| H12 | Fraquezas sugeridas | 300 rolagens × 3 grupos; 2/3/4 por tipo; nunca igual à Resistência; cobre os Elementos do grupo antes de repetir (`oraculo`) |
| H13 | Ordem com vários movimentos; empate PJ × inimigo | 300 estados; casos de 19.4 e 19.6; 4 empates fixos (`oraculo`) |
| H14 | 5 cenas da aventura | orçamentos de 50% e 100%; DTs Média/Difícil (`oraculo`) |
| H15 | Loja | todo preço igual ao do livro (`oraculo`) |
| H16 | Relógios | 45 casos + inválidos; painel do Início (`oraculo`, `extremos`) |
| H17 | Reputação | 7 rótulos exatos, vazio, fora da faixa, repetida (`oraculo`) |
| H18 | Créditos no encontro | ≤ 15% da verba; inteiro (`oraculo`) |
| H19 | Troca de Fraqueza no encontro aleatório | 500 × 3 grupos; contrato cumprido quando possível; nº de Fraquezas inalterado (`oraculo`) |
| H20 | Fonte do gancho 50/50 | 45–55% em 2 000 rolagens; gancho "Livro" da faixa (`oraculo`) |
| H21 | (absorvida em H9) | — |
| H22 | Antagonista | primeiro degrau com candidato; nunca vazio (`oraculo`) |
| H23 | Mais de 3 Ativas | aviso com 4, nenhum com 3 (`oraculo`) |
| H24 | Tom/limites da Sessão Zero | rótulo nos 2 itens; seção citada em cada item conferida (`texto`) |
| H25 | Quantidades de saída | contagem; sem repetição dentro de uma rolagem (`oraculo`) |

### 9.2 Inconsistências e lacunas do livro (e do ambiente) encontradas

O livro **não** é alterado. Cada item vai para `AUDITORIA.md`, e os de dados também para `mestre_dados.DIVERGENCIAS_DOCUMENTADAS`.

| # | Achado | Onde | Tratamento | Situação |
|---|---|---|---|---|
| L1 | Muitas fichas não declaram Execução (ex.: "### Casco Oco" não tem a linha) | 28.6–28.10 | "Não declarado" no Bestiário e aviso no Combate. Regra geral de 23.5 (só ser racional) | **verificar na implementação** (contar as fichas e confirmar o texto de 23.5) |
| L2 | Tenacidade de fase dos Bosses diferente da âncora de 28.3 | 28.5–28.10 | divergência documentada (§10.2) | **verificar na implementação**: listar criatura, fase, valor do livro e âncora |
| L3 | Combate A de 29.5 publica 3,7 Ciclos; H7 dá 4,0 | 29.5 × 27.4 | o rótulo de H7 explica a diferença (DPC puro de Boss) | **verificar na implementação** (reler 29.5) |
| L4 | Sem regra de inimigo por nível dentro da faixa | 28.3/28.4 | H1 | lacuna |
| L5 | Orçamento só para 4 PJs | 27.4/29.3 | H5 | lacuna |
| L6 | Sem tesouro por encontro (só a progressão por marco) | 24.5/26.1/27.8 | H18, H9 | lacuna |
| L7 | Ordem com vários movimentos no mesmo Ciclo não definida | 19.4–19.6 | H13 + "casa manual" | lacuna |
| L8 | O livro não liga Caminho a Elemento | 06.3 | o NPC sorteia o Elemento à parte | lacuna |
| L9 | Sem Sessão Zero, sem limite de missões abertas, sem relógio numerado nem escala de reputação | 27 | H24, H23, H16, H17 | lacuna |
| L10 | A "faixa esperada" de VEL só é dada nos níveis 1, 10 e 20 | 19.1 | texto sem aviso; aviso só para 7–25 | lacuna |
| L11 | Estimativa de dano especial ausente para Comum e Boss 5-8 | 28.4 regra 5 | H2 | lacuna |
| A1 | `testar_ficha.LISTA_BRANCA` tem TRIM, que `ficha_funcoes_ok.json` reprova | ficha (não se edita) | P3 | ambiente |
| A2 | `baseline-hashes.json` cita a "Cópia de Ficha…", que já não existe | `ficha-automatizada\` | P5 | ambiente |
| A3 | `testar_ficha.suite_protegidos` grava o JSON de protegidos se ele faltar | ficha | P4 | ambiente |
| A4 | `renderizar_ficha` grava o PNG inteiro (até 6000 px) junto dos recortes | ficha | P6 | ambiente |

Qualquer divergência nova achada pelos parsers é fatal (P13) até entrar nesta tabela, em `AUDITORIA.md` e em `DIVERGENCIAS_DOCUMENTADAS`.

---

## 10. Itens a confirmar em contexto na implementação

Nada do pedido foi dado como "já resolvido" por leitura. O coder confirma estes pontos quando chegar a eles e registra o resultado em `PROGRESSO.md`:

1. A contagem exata de fichas com e sem Execução (L1) e o texto de 23.5/05 sobre Executado e Xianzhouíta.
2. As Tenacidades de fase e quaisquer outros números de ficha que não batem com 28.3 (L2), criatura por criatura.
3. Os ≈ 95 ataques/ações de `bestiario_acoes`: o número real e se todo texto volta idêntico ao `.md` com os marcadores (H3).
4. Se `ficha_dados` já parseia `condicoes`, `dt_inimigo`, `ph`, `energia`, `ultimate` no formato que a Mestre precisa. Se não, a Mestre escreve parser próprio em `mestre_dados.py`, sem editar a ficha.
5. As 8 facções, os 6 locais e os 20 ganchos de 27.16–27.18 (contagens de §4.1) e os ganchos por faixa (4 por faixa, H20).
6. Os casos de `ouro` (29.4, 28.4, 21.2, 20.4, 20.5, 23.4, 23.6, 24.5, 25.1, 27.9): cada número relido no `.md` antes de virar expectativa do teste.
7. Os números dos 4 PJs do Exemplo por `oraculo_ficha.calcular`, e a Nadir de 29.7.
8. O desempenho: tempo de carga do modelo no `formulas` e o tempo de `fase1`. Se `tudo` passar de ~30 min, paralelizar mais (até 8 processos) antes de reduzir casos, e nunca reduzir abaixo das quantidades deste plano.
9. Que a validação de lista apontando para outra aba funciona no `formulas` (`spike`). O Google é conferido pela checklist de 2 minutos do guia, que este ambiente não consegue executar. Fica dito no `AUDITORIA.md` como **não verificado aqui**.
