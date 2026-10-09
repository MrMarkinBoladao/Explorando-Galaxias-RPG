# Fase 1 da Planilha do Mestre: combate, bestiário, Criador de Inimigos e Encontros (ciclo 2)

Este ciclo só confere se os 8 achados do ciclo 1 fecharam. Os cinco bloqueantes (F1–F5) estão fechados. O `suite-tudo.txt` (13:01:47–13:42) traz as 12 suítes da `fase1` com 5 023 257 checagens e 0 falha, e foi rodado sobre a versão final: nenhum arquivo de `build\mestre\`, `gerar_mestre.py`, `mestre_dados.py`, `testar_mestre.py`, `oraculo_mestre*.py` nem das planilhas mudou depois das 13:01:38 (confirmed pelas datas). `oraculo` e `extremos` chegaram ao resumo, rodando em 8 processos e sem cortar quantidades. O `PROGRESSO.md` já não tem o marcador e marca o portão 1.10 fechado. Os dois não bloqueantes (F7, F8) também fecharam. A linha de base da ficha (F6) foi regravada com causa documentada, e isso precisa chegar ao usuário no relatório final.

Watch for: a regravação de `baseline-hashes.json` foi feita sem confirmação explícita do usuário registrada (confirmed; informativo, não bloqueia).

**Verdict**: APPROVED

## High-level view

A prova que faltava no ciclo 1 agora existe. O `oraculo` cobre o Criador em 120 combinações modo × nível × tipo mais 160 Ajustar, 501 encontros aleatórios, a Fila em 4 empates fixos + 300 estados, a calculadora em 2 000 casos e 1 466/1 466 números de regra (P10). O `extremos` cobre 10 estados com as 11 855 fórmulas. Assim R1, R3 e R4 ficam provados em volume, e o R2 continua com 32/32 fichas e 116 ações idênticas ao `.md`. O modo "bloco" da calculadora só recalcula o grafo que descende das 9 entradas, e a exatidão vem da própria comparação com o oráculo independente. Isso só vale porque o lint garante 0 leitura direta de entrada, e ele passou.

Os erros de fórmula (Inimigos O203:O207, Combate D94:J95) e o texto cortado (B140/B141, C33:C42, C75:C84) estão zerados em `preview` e `visual` nos 3 estados. No spot-check do recorte `pior-caso-combate-parte-01.png`, o "Trocar por" de C33:C42 mostra "Operativo de Campo dos Caçadores" em três linhas, sem corte. No ambiente do encontro aleatório, `determinismo` (b) agora usa um caso que discrimina: "Ruína" e "Frente de guerra" mudam as criaturas no oráculo, a planilha segue o oráculo e cada criatura sorteada é de facção daquele ambiente.

A `protegidos` passa com 38 arquivos do livro e 13 da ficha conferidos. A linha de base foi regravada duas vezes (09:43:38 e 11:37:09), sempre por edições do workflow paralelo da ficha (`corrigir-erros-google`), e as anteriores ficaram guardadas. Os arquivos da ficha não mudaram depois das 09:44:12, e nada no código da Mestre grava neles.

<details>
<summary>Issues (1)</summary>

1. **Regravação da linha de base sem aval registrado** (informativo, não bloqueia): a decisão sobre `baseline-hashes.json` era do usuário. Citar no relatório final as duas regravações, a causa e os backups (`baseline-hashes-antes-rev2.json`, `baseline-hashes-0943.json`) para que ele confirme.

</details>

<details><summary>Details</summary>

### Situação dos achados do ciclo 1

```
F1 portão sem evidência        -> fechado: suite-tudo.txt, 12 suítes, 0 falha, PROGRESSO transcrito
F2 oraculo/extremos sem resumo -> fechado: 123 265 e 987 checagens, 0 falha (paralelo.py, 8 processos)
F3 erros de fórmula            -> fechado: preview 385/0 nos 3 estados
F4 texto cortado no Combate    -> fechado: preview 0 cortado, visual 20 202 textos/0; recorte C33:C42 conferido
F5 ambiente sem efeito         -> fechado: determinismo (b) com caso que discrimina, 50 093/0
F6 linha de base da ficha      -> regravada com causa e backup; protegidos 124/0 (aval do usuário pendente)
F7 ROUND em Encontros          -> fechado: ROUND só aparece no autoteste do lint, que agora o proíbe
F8 temporários                 -> fechado: nenhum %TEMP%\mestre-* restante
```

A sonda das 09:28 nas notas mostra que a falha do F5 vinha da planilha anterior às edições das 09:02, não de um filtro inerte. O teste novo discrimina, então uma regressão real no filtro passa a aparecer.

No recorte do pior caso, os nomes de PJ em A15:A20 e A24:A29 param em exatamente 30 caracteres ("um capítulo inteiro de validaç"). Pelo corte exato, deve ser truncamento feito pela fórmula, e não texto que vaza da célula (likely). Fica só como observação de leitura no pior caso e não abre achado neste ciclo.

O ciclo 1 deixou a linha de base para o usuário decidir. A `protegidos` agora também ignora o `desktop.ini` do livro, que é metadado do Drive. Falta registrar o aval do usuário às duas regravações.

</details>

<details>
<summary>Arquivos</summary>

Desde o ciclo 1 surgiram `build\mestre\paralelo.py` (8 processos para `oraculo`/`extremos`) e `build\mestre\protecao.py` (camada de leitura protegida, sinais de erro por linha, contador na Início). Os arquivos editados por último foram `testes_base.py`, `sorteio.py` e `aba_campanha.py` (13:00), `aba_bestiario.py`, `aba_inimigos.py` e `aba_inimigos_acoes.py` (12:10), além de `testes_estados.py`, `testes_regras.py` e `paralelo.py` (11:36). As notas também citam `aba_encontros.py` (ROUND → INT) e `gerar_mestre.py` (pior caso do "Trocar por"). As planilhas e o `build\mestre_mapa.json` foram regravados às 13:01:38. A evidência está em `suite-tudo.txt`, `PROGRESSO.md` e `notas-fase1.md` (seção Iteração 2). Não há repositório git, então o diff é o conjunto de arquivos acima.

</details>
