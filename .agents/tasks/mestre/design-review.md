# Revisão do design — Planilha do Mestre (Explorando Galáxias v1.1), ciclo 2

Ciclo 2 de `.agents\tasks\mestre\design.md`. Pela regra da revisão limitada, este ciclo só confere se os achados do ciclo 1 fecharam e não abre bloqueante novo. A revisão completa do ciclo 1 está guardada em `design-review-ciclo1.md` / `.json`.

Os 9 achados bloqueantes e os 3 não bloqueantes do ciclo 1 estão fechados no texto do design, e não só na tabela de respostas da seção 17. Cada correção foi conferida na seção indicada. A semente nova (`L3 → Q → L3 → X → L3`) foi reproduzida em Python e bate com a tabela da seção 5. A aritmética continua abaixo de 2⁴⁸. R1–R13, os 3 entregáveis com os nomes de D2, a lista branca e as 4 fases com critério de pronto não mudaram. Sobraram dois deslizes de layout que não bloqueiam.

Watch for: Execução da sub-tabela B2 do Bestiário ocupa K:L, a coluna reservada aos avisos (**confirmed**, não bloqueia); na I5 de Inimigos, os campos só cabem em B:J se "Inimigo" for a coluna A, e o texto não diz isso (**likely**, não bloqueia).

**Verdict**: APPROVED

## High-level view

A semente ganhou dois estágios não lineares: `Q` (quadrado mod M por partição de 16 bits) e `X` (mistura com `INT` e `MOD 65536`). Eles eliminam a correlação entre campos e o passo fixo entre rolagens. O autor mediu que a variante sugerida no ciclo 1 ainda deixava correlação de 2ª diferença e foi além dela. A propriedade (g), nova na suíte `determinismo`, testa correlação serial.

H1 interpola só o PV, com pior caso de −14,7% contra o limite de 20%. O Dano volta a ser a âncora, com desvio 0. A fase do Boss em vigor passou a ser entrada do Mestre, e a da barra só avisa, como pedem 28.5 regras 3 e 5. Na chave da Fila, os termos do inimigo valem 0, e o PJ vence o empate de VEL.

D11 resolve a largura com sub-tabelas de até 9 campos em B:J e no máximo 13 linhas por cabeçalho, conferidas pelo lint. As heurísticas soltas viraram H12 e H19–H25, e H16/H17 ganharam validação. `COUNT`, o índice 0 e a contagem de 12 fases foram corrigidos. Restam duas exceções de layout, que não bloqueiam.

<details>
<summary>Issues (2)</summary>

1. **Execução em K:L no Bestiário** — a sub-tabela B2 põe Execução em K:L, que D4 e a convenção da seção 6 reservam ao aviso. Ou declarar a exceção para tabelas só de leitura (e conferir que o lint aceita), ou levar Execução para B:J, juntando por exemplo D e E (DT · TR) numa célula. Não bloqueia.
2. **Coluna do "Inimigo" na I5** — Inimigo, Fase, 4 Fraquezas, Tenacidade e ritmo em H:J só cabem em B:J se o Inimigo ficar em A. Escrever isso na tabela de 6.7.1. Não bloqueia.

</details>

<details>
<summary>Details</summary>

### Semente: correção conferida por simulação

Reproduzi a fórmula da seção 5 com S = 12345. Os resultados batem com a tabela do design: 89,7% de cobertura na (f) com C = 8 × C = 10 em listas de 30, as 216 triplas de d6 consecutivos com C = 1…20, frequência de 168 a 237 em lista de 100 com 20 000 rolagens, e χ² da 1ª à 5ª diferença ao longo de R (lista de 30) entre 18 e 34, abaixo do crítico de 58,3. O 10d6 da Rolagem 1, que no ciclo 1 saía em escada, agora sai `[6,1,3,5,2,3,1,3,1,1]`.

Conferi também as contas de cada estágio. `Q` é mesmo z² mod M: com z = a·2¹⁶ + b, `MOD(a·z, M)·2¹⁶ + b·z` ≡ z². Os intermediários ficam < 2⁴⁶, 2⁴⁷ e 2⁴⁷, e a soma < 2⁴⁸. O maior quociente de `MOD` é 2¹⁷ ≈ 1,31·10⁵. `X` fica < 2³² e devolve de 1 a M−1, então nenhum estágio recebe 0. Só funções da lista branca são usadas (`MOD`, `INT`).

### Fechamento dos outros bloqueantes

O H1 está coerente nas duas pontas. A fórmula de 6.7.1 com as âncoras de PV de 28 (Comum 50/70/95/125/155, Elite 120/160/225/295/365, Boss 305/410/580/750/935) dá 60 contra 70 no Comum nível 5, 192 contra 225 no Elite nível 9 e 495 contra 580 no Boss nível 9. São os −14,3% e −14,7% publicados, dentro dos 20%. O critério (c) agora exige desvio 0 no Dano, e isso fecha, porque o Dano não é interpolado.

A virada de fase ficou como pede 28.5. A regra 3 está no aviso ("a Tenacidade volta ao máximo"), e a Tenacidade máxima é a da fase em vigor, presa à âncora. A regra 5 está na separação entre barra e fase em vigor. A suíte `oraculo` testa que Fraquezas e Tenacidade só mudam quando a fase em vigor muda. A limitação de que a planilha não sabe se a Redução foi apagada está declarada, e é inerente ao modelo sem macro de D7.

Na Fila, o menor PJ soma ≥ 15 000 + 150 + 5. O inimigo soma só `T_linha` < 1. Entre PJs, `T_disc·10 + T_tipo + T_linha` ≤ 309,1 < 1000, então o Discernimento nunca invade a Agilidade. O oráculo tem o caso de Agilidade −1 contra Boss de mesma VEL.

No layout, contei as colunas de C1–C8, I1–I4, B1, E1 e E2: todas cabem em 9 colunas de B:J, contando as mescladas, e os blocos ficam com no máximo 13 linhas (C7 em blocos de 12, C8 em 10 + 6, Bestiário em 11 + 11 + 10). As duas exceções estão nas Issues. Na B2, Execução ocupa K:L (**confirmed**), a coluna que D4 e o cabeçalho da seção 6 reservam ao aviso. Como a tabela é só leitura, não perde aviso nenhum, mas a convenção quebra sem estar declarada. Na I5, a lista de campos só cabe com o Inimigo em A (**likely**), porque com ele em B o ritmo em H:J colide com a Tenacidade em H.

H12 e H16–H25 têm método e validação concretos na seção 8. H21 é só o registro de que os 0–2 consumíveis entraram em H9, que agora valida a quantidade (cada valor entre 28% e 39% em 3 000 rolagens). O Bestiário usa `SUMPRODUCT(ISNUMBER(ordem)*1)`. Minhas Tabelas usa `MOD(i₀ − 1 + k·passo, n) + 1` com passo primo que não divide n, e assim os resultados não se repetem enquanto "quantos" ≤ n. `bestiario_fases` diz 12 linhas.

### Não bloqueantes do ciclo 1

Os três fecharam. A tabela de parâmetros por gerador na propriedade (b) torna as dependências explícitas, e a recompensa da aventura não lê mais a aba Recompensas. A impressão no Google ganhou linhas de "página N de 3" e o passo a passo do diálogo na seção 11 do guia. Embaraço (`1d6 × acúmulos`, Atrasa 1) e Aprisionamento (`1d6 + Ef`, Atrasa 2) entraram em C7 com o texto de 21.5.

</details>

<details>
<summary>Arquivos consultados</summary>

- `.agents\tasks\mestre\design.md` — seções 2 (D1, D2, D11), 4.1, 5, 6.7–6.17, 8, 9, 12, 13 e 17, lidas por trecho.
- `.agents\tasks\mestre\design-review-ciclo1.md` / `.json` — a revisão anterior, guardada antes de reescrever estes arquivos.
- `.agents\tasks\mestre\PROGRESSO.md` — estado das fases (2.1, revisão do ciclo 1 atendida).
- `livro-v1.0\28-bestiario.md` — só busca dirigida: 28.5 regras 3–5 e o resumo de PV por faixa.
- Simulação em Python da semente da seção 5, rodada pela linha de comando e não gravada em disco.

</details>
