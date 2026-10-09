# Fase 3 da Planilha do Mestre, iteração 2: fechamento de F1–F3

Esta passagem só confere se os três achados da revisão anterior foram fechados, sem abrir bloqueante novo. F1, o único bloqueante, está fechado: Campanha!E10 e E11 apontam a aba Sessões e a linha do tempo, e o lint barra "próxima fase" em todas as 18 abas (**confirmado**). F3 também está fechado. F2 foi tratado com uma comparação célula a célula, com a suíte nova `origem` e com a pergunta ao usuário registrada para antes da Fase 4. A bateria (`suite-tudo.txt`, 08/10 17:26 a 09/10 00:47) tem 15 suítes, 10 108 171 checagens e 0 falha. Ela rodou sobre planilhas de 16:47 e código de até 16:43, os dois gravados antes do início.

Watch for: o design ainda diz "3 páginas" na linha R10 da tabela de rastreio e no item 11 do guia §15 (**confirmado**, não bloqueante). O COMO-USAR da Fase 4 tem de dizer "página N de 5".

**Verdict**: APPROVED

## Visão geral

F1 está fechado no gerador e no arquivo. `aba_campanha.py` (linhas 39 e 40) grava "Lida pela aba Sessões (preparação e diário) e pela Início." e "Usado pela linha do tempo (nesta aba, mais abaixo).", e o recorte `exemplo-campanha-parte-01.png` mostra os dois textos inteiros. O lint (`testes_fase3`, linha 532) procura "em construção", "próxima fase" e "proxima fase" como substring, sem distinguir maiúsculas. A `lint` subiu de 221 185 para 221 203 checagens, com 0 falha. O texto de `nucleo.EM_CONSTRUCAO` ainda contém "próxima fase", mas nenhuma aba o usa, e o lint o barraria se alguma usasse.

F2 está coberto. A `origem` deu 9/9 no começo e 9/9 no fim da bateria (app.xml, sem `xl/metadata`, área de impressão do Escudo, 3 410 validações nos dois arquivos), então nada regravou os `.xlsx` no meio dela. O `.gsheet` de 22:27 é o atalho do Google, que fica de fora desde a Fase 2, e não toca o `.xlsx`.

F3 está fechado. Os títulos das páginas 4 ("Pessoas: condições, Morrendo e PV temporários") e 5 ("Mesa: Energia, tetos e casos-limite") aparecem nas linhas 111 e 144 do recorte `exemplo-escudo-do-mestre-parte-02.png` e correspondem ao conteúdo: 21.5, 23.4, 23.5 e 23.3 na página 4, e 17.2 e 29.12 na página 5. As alturas das páginas continuam ≤ 633 pt.

Pela evidência, as Fases 1 e 2 continuam intactas. A `bestiario` dá 34/34 fichas e 116 ações. A `ouro` cobre 24.5, 25.1–25.3, 26.7 e o teto do Cone. A `oraculo` tem cobertura P10 de 1 624/1 624 com G = 100…420, e a `determinismo` também passa por G = 100…420. A `protegidos` (165) confirma o livro e a ficha por SHA-256.

<details>
<summary>Issues (1)</summary>

1. **"3 páginas" que sobrou no design** (não bloqueante): o `design.md` ainda diz "3 páginas A4 paisagem" na linha R10 da tabela de rastreio e "confira as 3 páginas do Escudo" no item 11 do guia §15. Trocar os dois por 5 antes de escrever o COMO-USAR na Fase 4.

</details>

<details><summary>Detalhes</summary>

## O que ainda fala em 3 páginas

A busca no design achou duas menções antigas (**confirmado**). Uma está na tabela de rastreio de requisitos (`R10 Escudo do Mestre | 6.15: 3 páginas A4 paisagem…`). A outra está na estrutura do guia §15, que manda conferir "as 3 páginas do Escudo" em "Quebras de página personalizadas". A planilha está certa. O risco fica para a Fase 4: o COMO-USAR é escrito a partir do §15 e, se o copiar ao pé da letra, vai mandar o usuário procurar 3 páginas num Escudo que tem 5. O plano 3.3 já diz "O guia da Fase 4 diz 'página N de 5'". A linha 11 da tabela de revisão do design é registro histórico e pode ficar como está.

</details>

<details>
<summary>Arquivos</summary>

- `build\mestre\aba_campanha.py`: E10 e E11 da Mesa (F1).
- `build\mestre\aba_escudo.py`: títulos das páginas 1, 2, 4 e 5 (F3).
- `build\mestre\testes_fase3.py`: lint contra "Em construção" e "próxima fase" em toda célula (F1).
- `build\mestre\testes_base.py`, `build\testar_mestre.py`: suíte `origem` no começo e no fim da `fase3` (F2).
- `.agents\tasks\mestre\plano-mestre.md` (3.3) e `design.md` (§6.15): Escudo com 5 páginas (F3).
- `Mestre\…V1.2.xlsx` e `…Exemplo.xlsx`: regenerados às 16:47.
- Evidência: `suite-tudo.txt` (= `suite-fase3.txt`), `PROGRESSO.md`, `notas-fase3.md`, recortes em `preview\`.

</details>
