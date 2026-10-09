# Revisão do design — Planilha do Mestre (Explorando Galáxias v1.1)

Ciclo 1 (revisão completa) de `.agents\tasks\mestre\design.md`.

O design especifica um `.xlsx` de 18 abas gerado por Python, que reaproveita por import o pipeline da ficha (estilos, lint Google, motor `formulas`, léxico, renderizador) sem alterar os arquivos dela. Ele cobre o pedido inteiro do usuário: criador de inimigos, bestiário, encontros, rastreador de combate, NPCs, aventuras, recompensas, geradores diversos, gestão de campanha, Escudo e tabelas editáveis, com os entregáveis na pasta `Mestre\`. Os números do livro conferidos por busca dirigida batem: âncoras de 28.3, orçamento de 27.4, Firmeza de 19.4, Quebra de 20.4–20.5, Morrendo de 23.4, PH de 16.2, Sobreposição de 25.2, verba de 24.5, limiares de fase e H2 inteira. A semente é determinística e segura em ponto flutuante, mas é afim, então os sorteios saem correlacionados.

Watch for: correlação linear da semente entre campos e entre rolagens (**confirmed**, simulado); critério de aceite de H1 que o próprio método reprova (**confirmed**); virada de fase do Boss calculada pelo PV, contra 28.5 regra 5, sem a volta da Tenacidade ao máximo (**confirmed**); layout de Combate e Inimigos sem estratégia para caber em A:L ≤ 1360 px (**likely**); `COUNT` fora da lista branca (**confirmed**).

**Verdict**: NEEDS_CHANGES

## High-level view

R1–R13 têm seção e aba (tabela da seção 9), os três entregáveis estão em D2 como constantes únicas e cada uma das 4 fases tem critério de pronto. Os nomes usam "Galáxias" com acento, enquanto o briefing escreve sem acento. Mas o briefing veio sem acento em tudo, até em "Sugestao da planilha", e a ficha existente se chama `Ficha Automatizada - Explorando Galáxias V1.1.xlsx`. Então D2 está certa e não bloqueia.

A semente mistura entradas por soma e depois aplica só multiplicações de Lehmer, que são lineares. Resultado: dois campos do mesmo gerador ficam sempre à mesma distância um do outro, e cada "rolar de novo" anda um passo fixo na lista. A propriedade (f) do próprio design falha e os dados do rolador saem em escada. Um passo não linear corrige isso e cabe na lista branca.

No combate, a fase do Boss é calculada direto do PV. Assim as Fraquezas trocam no meio da ação do grupo, quando o livro manda virar no fim do turno do Boss, e a Tenacidade não volta ao máximo na virada. A chave da Fila não diz que atributos o inimigo usa, e a leitura mais natural contradiz a regra de empate que o design promete. Algumas tabelas têm de 20 a 40 colunas por linha, sem plano para caber na área exigida.

As heurísticas têm rótulo, mas o aceite de H1 não fecha no Dano, H16 e H17 estão sem validação e há heurísticas soltas nas seções 6.x sem número H. O resto são deslizes de uma linha: `COUNT`, um índice 0 em Minhas Tabelas e 13 linhas de fase onde o livro dá 12.

<details>
<summary>Issues (9)</summary>

1. **Semente com correlação linear** — trocar o passo afim por um passo não linear (ex.: quadrado modular com partição de 16 bits entre duas rodadas de Lehmer) e acrescentar à suíte `determinismo` testes de correlação serial entre rolagens consecutivas e entre campos consecutivos (inclusive os dados do rolador).
2. **Aceite de H1 impossível no Dano** — o Dano interpolado desvia até 33,3% (Comum, nível 4) contra o limite de 20%. Ou o Dano deixa de ser interpolado (usa a âncora da faixa do nível), ou o limite passa a ser por coluna, com justificativa.
3. **Virada de fase pelo PV** — separar "fase da barra" (calculada, só acende o aviso) de "fase em vigor" (entrada do Mestre, aplicada no fim do turno do Boss) e fazer a virada pedir ou aplicar a volta da Tenacidade ao máximo.
4. **Chave da Fila sem atributo de inimigo** — fixar que os termos de Agilidade e Discernimento do inimigo valem 0 na chave (sem o +20), para o PJ vencer o empate de VEL como o design diz, e pôr um caso com Agilidade −1 no oráculo.
5. **Layout de Combate, Inimigos e Grupo** — declarar como as 20–40 colunas por linha cabem em A:L ≤ 1360 px (sub-tabelas por assunto com o rótulo do combatente repetido, ou cartão de várias linhas).
6. **Heurísticas sem número ou sem validação** — dar validação a H16 e H17 e registrar como H# (com rótulo e validação) as heurísticas soltas: Fraquezas sugeridas G=110 (ordem e Comum = 2), troca sugerida no encontro aleatório, 50/50 entre ganchos do livro e da tabela, 0–2 consumíveis, cadeia de fallback do antagonista, "mais de 3 missões Ativas", limites da mesa na Sessão Zero.
7. **`COUNT` fora da lista branca** — trocar `COUNT(ordem)` do Bestiário (6.8) por `SUMPRODUCT(ISNUMBER(ordem)*1)`.
8. **Índice 0 em Minhas Tabelas** — `MOD(i₀ + k·passo, n)` devolve de 0 a n−1; escrever `MOD(i₀ − 1 + k·passo, n) + 1`.
9. **Contagem de `bestiario_fases`** — são 12 linhas (2+2+2+3+3), não 13; corrigir antes que o parser "falhe alto" no build.

</details>

<details>
<summary>Details</summary>

### Correlação linear no modelo de semente

Determinismo e aritmética estão certos. `h` fica em [1, M−1] e o maior produto, `x·16807`, fica abaixo de 3,6·10¹³. `INT(x3·n/M)` nunca chega a n, porque `x3·n/M` fica a pelo menos 1/M de qualquer inteiro, muito acima do erro de arredondamento. O resultado é o mesmo em Google, Excel e `formulas`. O defeito está na qualidade do sorteio (**confirmed**). `h` é uma soma, e cada rodada de Lehmer só multiplica por 16807 módulo M. Então `x3` é uma função afim de `h`:

```
x3(C₂) ≡ x3(C₁) + 16807³·1299709·(C₂−C₁)   (mod M)   — deslocamento fixo, independe de S e R
x3(R+1) ≡ x3(R) + 16807³·104729            (mod M)   — passo fixo a cada "rolar de novo"
```

Simulado com as constantes do design (S = 12345):

```
pares (Personalidade C=8, Segredo C=10), listas de 30, 2000 rolagens: 60/900 = 6,7%  (meta (f): ≥ 60%)
rolador G=650, 10d6, Rolagem 1: [4,4,4,5,5,5,5,6,6,6]   Rolagem 2: [3,3,3,3,4,4,4,4,5,5]
rumor C=1, Rolagens 1..12 (lista de 30): 20,14,8,1,25,19,12,6,30,24,17,11   (sempre −6)
```

Na mesa, isso significa que cada nome sai sempre com os mesmos dois sobrenomes e cada personalidade com os mesmos dois segredos. Os três rumores de uma rolagem andam juntos e os dados do rolador (R13) saem em escada. As propriedades (a)–(e) passam e só a (f) falha, então a suíte `determinismo` da fase 1 (G=100, G=110) não fecha. A seção 5 diz que a constante por campo impede que dois campos andem juntos, mas isso não vale: uma constante somada antes de uma transformação linear continua sendo um deslocamento constante depois dela.

Uma variante testada resolve: `v = Lehmer³(h)`, depois `w = v² mod M` por partição de 16 bits (`MOD(MOD(INT(v/65536)*v, M)*65536 + MOD(v,65536)*v, M)`), depois `x3 = Lehmer³(w)`. O maior intermediário fica em ≈ 2,9·10¹⁴ e o quociente de `MOD` em ≈ 1,3·10⁵, abaixo de 2²⁷. Ela dá 88–91% de cobertura na (f) e dados sem padrão. Há 30 passos distintos entre rolagens consecutivas, e a frequência fica entre 161 e 240 contra 200 esperados em 20 000 rolagens, dentro dos ±25% da (e). O quadrado é 2-para-1 (v e M−v colidem), o que não pesa em listas de até 100 itens. Com essa variante ou outra, a suíte `determinismo` precisa de uma propriedade de correlação serial: a distribuição dos passos entre rolagens consecutivas e entre campos consecutivos, inclusive os 20 dados de uma expressão. Das propriedades atuais, só a (f) pega esse defeito.

### H1: método e critério de aceite incompatíveis

No PV, a interpolação fica dentro do previsto (pior caso 14,7%, Elite e Boss no nível 9). No Dano, não (**confirmed**, calculado com a fórmula de 6.7.1 e as âncoras de 28.3):

```
Dano Comum   nível 4: 4 contra 3  (+33,3%)
Dano Elite   nível 5: 10 contra 13 (−23,1%)
Dano Boss    nível 5: 15 contra 20 (−25,0%)
```

O critério (c) de H1 diz "falha se algum desvio passar de 20%", então a suíte da fase 1 reprova o próprio design. Entre as faixas 1-4 e 5-8, o Dano dá saltos proporcionalmente muito maiores que o PV (3→7, 7→13, 10→20). É nesse trecho que a interpolação linear se afasta da âncora.

### Fases do Boss no Combate

Em 6.10, a fase "sai do PV atual contra os limiares", e as "Fraquezas da fase atual" alimentam a calculadora de dano. Assim, a fase vira no instante em que a barra cruza o limiar (**confirmed**). Isso contraria 28.5 regra 5: "A virada acontece no fim do turno do Boss, nunca no meio de uma ação do grupo". O livro ainda explica o motivo: "quem Atrasou o Boss ganhou um Ciclo inteiro de fase antiga". O aviso "Virou a fase N no fim do turno dele" diz o certo, mas os números da calculadora já mudaram antes da hora. No modelo sem macro, a fase em vigor deveria ser entrada do Mestre (vazia = 1). A fase da barra fica só para acender o aviso.

A regra 3 de 28.5 também falta: a Tenacidade "volta ao máximo na virada de fase" (**confirmed**: o design não menciona). Com `Tenacidade atual = MAX(0, máx − redução)`, a redução acumulada na fase anterior continua descontando da barra nova.

### Chave de ordenação da Fila

A chave é `VEL × 100000 + (Ag + 20) × 1000 + (Disc + 20) × 10 + IF(PJ, 5, 0) + desempate`, e o design afirma que "empate PJ × inimigo dá o PJ antes". Inimigo não tem Agilidade nem Discernimento (28.2), e o design não diz que valor entra no lugar (**likely**). Com o valor de célula vazia (0, que soma 20 000 na chave), um PJ de Agilidade −1 soma 19 000 e perde o empate para o inimigo. O −1 está na faixa válida de 10.1 (−1…+5). Isso contradiz a promessa do design e o passo de 19.3 em que ele se apoia.

### Layout das tabelas largas

O design fixa A:L, área ≤ 1360 px, nenhum painel congelado e no máximo 15 linhas entre um dado e o cabeçalho. Se a área passar de 1360 px, `ajustar_layout` para o build. A tabela de inimigos do Combate lista cerca de 40 campos por combatente: dados puxados, PV, Tenacidade, Quebra, quem quebrou, Dano de Quebra, Sangramento, Defesa atual, 3 recargas × 4 colunas e as colunas da Fila. Inimigos da campanha tem 17 entradas e 16 calculadas por linha. Grupo tem 21 entradas por PJ (**likely**). Os "dois blocos de 6" resolvem a distância de 15 linhas, mas não a largura. Sem uma estratégia declarada, a fase 1 só descobre o problema quando o gerador falhar.

### Heurísticas fora do livro

H16 (relógios) e H17 (reputação) têm "—" na coluna de validação (**confirmed**). As duas são fáceis de validar: barra e situação para todo par segmentos × preenchidos, e os 7 rótulos. Outras heurísticas aparecem nas seções 6.x e não estão na tabela (**confirmed**). Por isso não entram em `sugestoes` e escapam da checagem de rótulo da suíte `texto`:

- a ordem das Fraquezas sugeridas de G=110 e o "Comum = 2" (6.7.2);
- a troca de Fraqueza sugerida no encontro aleatório (6.9);
- a divisão 50/50 entre os ganchos de 27.18 e `tab.gancho_npc`/`tab.gancho` (6.6, 6.11);
- os 0–2 consumíveis dos achados (6.12);
- a cadeia Boss → Elite → Boss da faixa na escolha do antagonista (6.11);
- o aviso "mais de 3 missões Ativas" (6.5);
- os limites da mesa da Sessão Zero (6.2).

### Deslizes pontuais de fórmula e contagem

O Bestiário (6.8) usa `IF(k>COUNT(ordem),"",…)`. `COUNT` não está em `ficha_funcoes_ok.json`, que tem `COUNTIF`, `COUNTIFS`, `COUNTA` e `COUNTBLANK`, então o lint reprova (**confirmed**). Em Minhas Tabelas (6.17), com i₀ de 1 a n, `MOD(i₀ + k·passo, n)` dá 0 sempre que a soma é múltiplo de n (**confirmed**, na leitura literal). Nesse caso, `MATCH(0, aux, 0)` cai na primeira linha com contador zero, não numa vaga. O bloco `bestiario_fases` (4.1) diz 13 linhas, mas os cinco Bosses com fases somam 12 (**confirmed** nos cabeçalhos "Fase N" de 28). São três Bosses de 2 fases (305, 580 e 750 PV) e dois de 3 fases (935 PV cada). Como o parser falha alto quando a contagem difere, esse número errado vira erro de build.

### Observações que não bloqueiam

- A recompensa da aventura usa o gerador G=400 "com a mesma Rolagem nº", mas o design não diz de onde vêm a faixa e a leitura de dificuldade (**likely**). Se vierem das entradas da aba Recompensas, editar aquela aba muda a aventura, contra a propriedade (b) da seção 5.
- Os ganchos de NPC e de aventura dependem do nível do grupo na Campanha. A (b) precisa listar esse nível como parâmetro desses geradores.
- O Escudo e os cartões dependem da área de impressão e das quebras de página gravadas no `.xlsx`, e o Google Planilhas não usa essas definições ao importar (**likely**). A seção 11 do guia precisa ensinar os ajustes do diálogo de impressão do Google: A4, paisagem, ajustar à largura.
- A lista de tique de Dano Contínuo das condições (6.10) não traz Embaraço (`1d6` por acúmulo) nem Aprisionamento (`1d6 + Eficiência`), que estão em 21.5.

</details>

<details>
<summary>Arquivos consultados</summary>

- `.agents\tasks\mestre\design.md` — o documento revisado, lido inteiro.
- `.agents\tasks\mestre\PROGRESSO.md` — estado das fases (design concluído, implementação não iniciada).
- `build\ficha_funcoes_ok.json` — lista branca de funções (33), base do lint.
- `livro-v1.0\16`, `19`, `20`, `21`, `23`, `24`, `25`, `26`, `27`, `28`, `29` — só busca dirigida: PH, Fila e Firmeza, Quebra e Dano de Quebra, condições, Morrendo e Descanso, verba, Sobreposição e Tiers, ritmo e Ressonâncias, orçamento e attrition, âncoras, regras de fase, fichas do Exemplo, ficha da Nadir.
- Simulações em Python, não gravadas: fórmula de semente do design, variante não linear e interpolação de H1.

</details>
