# Revisão final da v1.0 de Explorando Galáxias

A v1.0 entrega os 31 capítulos planejados mais o changelog, compilados em `Sistema de HSR by MC Filhos V1.0.docx` (14,6 MB, 3.626 parágrafos, 295 tabelas reais do Word, 33 Heading 1). Auditei os sete itens do escopo contra as três fontes (design aprovado, extrato da v0.1 e as 22 lacunas do handoff) lendo os `.md` e rodando os verificadores somente-leitura do projeto, sem regerar o `.docx`. Os dois defeitos estruturais da v0.1 estão fechados: os quatro Caminhos que tinham zero Bênçãos (Erudição, Euforia, Caça, Preservação) agora têm 12 cada, e nenhuma regra cita subsistema que o livro não define. Aritmética, faixa de níveis e tom também passam.

**Atenção:** três observações não bloqueantes — a Tenacidade de Elite cai de 7 para 6 entre as faixas 9-12 e 13-16 sem nota de rodapé que explique (confirmado; é fiel ao design aprovado, mas vai parecer erro de digitação para quem acabou de ler no changelog que tabela não monotônica é bug); "Provocado" aparece na lacuna 12 e na identidade da Preservação do handoff mas não existe como condição no livro nem no design (confirmado; nenhuma regra o cita, então não há referência pendurada); e os capítulos 12 a 15 não têm arte porque o acervo da v0.1 não tem símbolo para esses quatro Caminhos (confirmado).

**Verdict**: APPROVED

## Visão geral

São 108 Bênçãos nos 9 Caminhos, 12 por Caminho, em três Tiers (6 sem requisito, 4 no nível 9, 2 no nível 17) — contei por regex nos `.md` e conferi com `checar-completude.ps1`. Os quatro Caminhos novos ganharam recurso próprio e eixo mecânico que não repete nenhum dos cinco que o autor já havia escrito: Acúmulos de Cálculo (área, até o teto de 6 alvos), Tabela do Riso (aleatório), Marcação de Presa (alvo único e crítico) e Barreira (PV temporário com nome próprio).

Nas médias de dado, o livro adota uma convenção que **divergiu do design**: a média de um dN é `(N+1)/2` e toda média impressa é arredondada para baixo (capítulo 02). O design pedia 22,5 para `5d8`; o livro imprime 22. Verifiquei 90 declarações de forma independente, tratando modificadores fixos do tipo `4d8 + 1`, e o piso é aplicado de forma consistente em todo o volume.

A referência cruzada — o defeito central da v0.1 — está fechada. O livro define 176 seções numeradas, todas as referências internas de seção resolvem, as 548 citações de capítulo resolvem e o glossário cobre 42 de 42 termos oficiais. Os termos que a v0.1 usava sem definir ("DoT", "ação bônus", "barra de resistência") só aparecem nos três arquivos isentos, e lá como tabela de aposentadoria.

Na faixa de níveis, a tabela mestra tem os 20 níveis e os capstones "Avatar" dos nove Caminhos subiram do nível 5 da v0.1 para o 17. As tabelas que param em 7 ou em 5 são de outro eixo — Nível de Habilidade (1-7) e tier de Cone de Luz (1-5) — e não nível de personagem; quem auditar por busca de "nível" vai tropeçar nelas.

Os únicos resquícios de pendência são quatro comentários HTML `<!-- ARTE PENDENTE -->` nos capítulos 12 a 15, e o build os remove antes de escrever o `.docx` — conferi a regex no script e a ausência no arquivo compilado. O parêntese "(provavelmente vou mudar o nome)" sobrevive apenas como linha da tabela de termos aposentados do glossário, declarando que o nome está fechado. Nome, autoria, versão e tom de livro publicado em PT-BR conferem na capa, na ficha técnica e nas propriedades do `.docx`.

<details>
<summary>Achados (5)</summary>

1. **Tenacidade de Elite não monotônica** — a tabela publica 5 / 6 / 7 / **6** / 7 por faixa (capítulo 20 e apêndice 29.4); o valor é derivado do DPC e é fiel ao design aprovado, mas vai ler como erro. Acrescentar uma linha dizendo que a Tenacidade é derivada da redução efetiva do grupo por Ciclo, e que por isso pode não subir a cada faixa.
2. **"Provocado" não existe** — a lacuna 12 pede a condição no catálogo e a lacuna 1 lista "provocar" na identidade da Preservação; o design nunca a definiu e o livro não a usa. Confirmar com o autor que Barreira + Intervir cobrem a fantasia de tanque, ou abrir a condição numa v1.1.
3. **Capítulos 12 a 15 sem arte** — o acervo da v0.1 tem 17 imagens e nenhuma para Erudição, Euforia, Caça e Preservação. Os outros cinco Caminhos têm. Conseguir quatro símbolos ou aceitar a assimetria.
4. **Tabela de armas repartida em dois capítulos** — dados, alcance, atributo e redução de Tenacidade estão em 18.5; Elemento e propriedade especial em 18.7 e 24.2. A lacuna 8 pedia "tabela completa". Considerar consolidar ou cruzar as duas com uma referência explícita.
5. **`verificar-livro-final.ps1` checa presença de Heading, não quantidade** — ele imprime `H1=1 H2=1 H3=1` como flags booleanas, então passaria um `.docx` com um único título. A contagem real (33 / 234 / 332) está correta; o indicador é que é fraco. Trocar por contagem mínima.

</details>

<details>
<summary>Detalhes</summary>

## As 22 lacunas, item por item

Todas têm seção própria. O mapeamento:

| # | Lacuna | Onde | Como verifiquei |
|---|---|---|---|
| 1 | 4 Caminhos sem Bênção | 12, 13, 14, 15 | 12 Bênçãos em cada, 108 no total |
| 2 | Ordem de turno | 19 (Fila de Ação, Ciclo, casa) | seções 19.1-19.6 |
| 3 | Velocidade como estatística | 19 | `10 + Bônus de Agilidade + Caminho + equipamento` |
| 4 | Acerto crítico | 18 (faixa 20; 19-20 só na Caça) | 18.3 |
| 5 | Teste de Ataque | 18 | 18.2 |
| 6 | Vantagem e Desvantagem | 02 | cancelam por presença, não por contagem |
| 7 | RD | 18.4, escala no bestiário | changelog 3.1 |
| 8 | Ataque Básico e tabela de armas | 18.5, 18.7, 24.2 | 6 categorias, progressão até 5 dados |
| 9 | Tenacidade por nível de ameaça | 20 | tabela Comum / Elite / Boss × 5 faixas |
| 10 | Tabela mestra 1→20 | 26 | 20 linhas |
| 11 | Descanso | 23 | Curto e Longo |
| 12 | Catálogo de condições | 21 | ver abaixo |
| 13 | Buff/Debuff e Passivas por Nível | 16.5 | duas tabelas de Nível 1 a 7 |
| 14 | Cones de Luz, Relíquias, Ressonâncias | 25, 26 | subsistema novo inteiro |
| 15 | Bestiário 30+ fichas e 3 Bosses | 28 | 32 fichas, 6 Bosses, 5 com fase 2 |
| 16 | Guia do Mestre | 27.2 a 27.11 | DT, encontro, ritmo, recompensa, aprovação |
| 17 | Ambientação | 27.12 a 27.18 | Aeons, Stellaron, Fragmentum, Expresso, facções, locais |
| 18 | Exploração, Técnicas, Créditos | 24.5, 24.6, 27 | preços de referência e Técnicas |
| 19 | Ficha de personagem | 29.8 | mais Memoespírito (29.9) e Trilha (29.10) |
| 20 | Exemplo de criação passo a passo | 29.7, e "Exemplo rápido" no 03 | com as contas abertas |
| 21 | Morte/Executado como capítulo | 23 | saiu de dentro do benefício racial |
| 22 | Energia ao sofrer dano e ao abater | 17 | `sofrer dano +10 (1×/Ciclo) · derrotar inimigo +10` |

O catálogo de condições do capítulo 21 tem verbete próprio para Sangramento, Queimadura, Congelado, Choque, Cisalhamento de Vento, Embaraço, Aprisionamento, Marcado, Corrupção, Silenciado e Vulnerável. Dos itens que a lacuna 12 listava, três mudaram de endereço por decisão de design: Dano Contínuo é dono do capítulo 20, PV temporários e Escudo foram unificados em **Barreira** (capítulos 15 e 23), e **Provocado** não existe — é o achado 2.

## Os 11 erros concretos da v0.1

Todos fechados, cada um com nota "O que mudou da v0.1" no lugar onde a regra mora. Bônus de Atributo monotônico, com 13 valendo +1 e escala até 20, preservando os marcos do autor (8 = -1, 10 = +0, 12 = +1, 14 = +2, 15 = +3). Esquiva virou `Defesa + Eficiência`, sem contar Agilidade duas vezes. Dados de vida viraram PV fixo por Caminho, com o índice **N** sobrevivendo e a rolagem indo para variante opcional com piso e teto. Eficiência reespaçada para +8 no nível 20 (Eficácia +16), em vez dos +16 que a curva da v0.1 extrapolada daria. "Ação bônus" virou Ação Complementar, com as quatro ações do turno fechadas. Os absolutos que não escalavam (+20 PV temporários, +30 PV, 15 de RD, +10 em teste) viraram múltiplos de Eficiência ou de nível. O "Teste de Resistência de Resistência Física" virou Teste de Potência Física com DT fixa, em vez de DT derivada de rolagem. Os nove capstones "Avatar" subiram para o nível 17. A regra punitiva de Tenacidade virou redução em três níveis (total / metade / 1 ponto), mais o Implante de Fraqueza e a regra geral de revelar Fraquezas — ninguém fica estruturalmente fora da Quebra. E a quantidade de Habilidades ganhou teto de **8**, com Nível máximo de Habilidade escalando em paralelo.

## Aritmética

Amostra das médias que mais aparecem, conferidas contra `(N+1)/2` com o piso do capítulo 02:

```
6d6   = 21,0  -> 21     5d8  = 22,5 -> 22     7d20 = 73,5 -> 73
5d10  = 27,5  -> 27     8d12 = 52,0 -> 52     10d20 = 105  -> 105
6d12  = 39,0  -> 39     3d12 = 19,5 -> 19     18d20 = 189  -> 189
4d8+1 = 19    5d10+1 = 28    7d12+3 = 48    10d12+7 = 72
```

O `checar-tabelas.ps1` do projeto confere 200 médias, a monotonicidade do Bônus de Atributo (13 degraus, de -1 a +5) e os 20 níveis da tabela mestra. O `simular-combate.ps1` reproduz o DPC publicado das cinco faixas com divergência de 0,1% a 1,2%, dentro da janela de 5%.

## A não monotonicidade da Tenacidade

O design deriva a Tenacidade do inimigo da redução efetiva do grupo por Ciclo: `Boss = 2 ×`, `Elite = 1 ×`, `Comum = 0,5 ×`, tudo sobre a redução **já condicionada ao acerto**. Como a taxa de acerto e o número de dados não crescem de forma uniforme entre faixas, a saída da fórmula pode cair:

```
Faixa    Comum  Elite  Boss
1-4        3      5     10
5-8        3      6     11
9-12       4      7     12
13-16      4      6 <<  12     Elite cai; Boss empata
17-20      4      7     13
```

Conferi na tabela de âncoras do design aprovado: os valores do livro são exatamente os dela, inclusive o 6. O livro é fiel; a fórmula é que produz o degrau. O problema é de leitura, não de número: o changelog ensina ao autor, em duas páginas, que tabela não monotônica é bug — e então uma tabela do próprio livro desce. Uma frase na tabela do capítulo 20 resolve.

## Cobertura de teste

Rodei os cinco verificadores somente-leitura do projeto, todos com código 0: nomenclatura (25 strings proibidas em 28 capítulos de regra; `00-*`, `01-*` e `30-*` são isentos de propósito, porque é onde os termos aposentados devem aparecer), completude, tabelas, simulação de combate e verificação do livro compilado.

**Não coberto:** ninguém valida que o *texto* de uma Bênção respeita os tetos que o capítulo 26 publica (bônus somado, penalidade somada, +3 dados adicionais, PV temporários a `3 × Eficiência`) — hoje é conferência humana, e é a maior superfície de erro que sobra. O `verificar-livro-final` mede Heading por presença e não por contagem (achado 5). E a validação do sumário é manual por natureza: o Word só calcula as páginas quando o campo TOC é atualizado.

</details>

<details>
<summary>Arquivos auditados</summary>

**Fontes de verdade:** `.agents/tasks/design.md` (design aprovado, incluindo 3.1/3.2 de nomenclatura e 18.3 das âncoras de inimigo) · `.agents/tasks/v01-extraido.txt` · `HANDOFF-RETOMADA-v1.0.md` seções 8 e 9 · `.agents/tasks/plano-escrita.md`

**Livro:** 32 arquivos em `livro-v1.0/` — `00-capa-e-creditos`, `00-changelog-v01-para-v10`, e `01` a `30`. Os 31 capítulos do plano mais o changelog exigido pelo handoff 7.2.

**Compilado:** `Sistema de HSR by MC Filhos V1.0.docx` — 14,6 MB, 3.626 parágrafos, 295 tabelas (7.333 células, nenhuma vazia), 33 Heading 1 / 234 Heading 2 / 332 Heading 3, 17 imagens, propriedades com título "Explorando Galáxias" e autor "MC Filhos".

**Build e verificação:** `build/gerar_docx.py` · `scripts/checar-nomenclatura.ps1` · `scripts/checar-tabelas.ps1` · `scripts/checar-completude.ps1` · `scripts/simular-combate.ps1` · `scripts/verificar-livro-final.ps1`

Não regerei o `.docx` nem rodei o build. Os spot-checks que fiz no arquivo compilado foram leituras com python-docx para conferir estrutura de títulos e metadados, porque o indicador de Heading do verificador do projeto é uma flag de presença e não dava para confiar nele sozinho.

</details>
