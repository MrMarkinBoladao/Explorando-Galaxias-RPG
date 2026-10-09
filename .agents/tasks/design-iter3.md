# Documento de Design — Explorando Galáxias v1.0

**Sistema:** Explorando Galáxias
**Autor:** MC Filhos
**Universo:** Honkai: Star Rail (conteúdo original, fidelidade de tom e temática, zero cópia de wiki ou do jogo)
**Base:** v0.1 (`.agents/tasks/v01-extraido.txt`, 1164 linhas, lida por inteiro)
**Faixa de níveis:** 1 a 20
**Status:** decisões mecânicas FECHADAS — **iteração 3**, com os 26 achados do review da iteração 2 endereçados (respostas achado por achado em 26.1) e os 41 da iteração 1 já incorporados (26.2)

> O nome do sistema é **Explorando Galáxias**. O aviso "(provavelmente vou mudar o nome)" da v0.1 sai do livro em definitivo.

---

## ⚠ OVERRIDE DO USUÁRIO — FAIXA DE NÍVEIS

> **O sistema vai do nível 1 ao 20. Qualquer menção a "nível 1 a 10" em prompts de passos posteriores está obsoleta e deve ser ignorada.**

Esta decisão do usuário substitui a linha "faixa de níveis 1 a 10" do briefing original e de qualquer prompt gerado antes dela (incluindo os passos `plan` e o loop de escrita de capítulos). Toda curva, tabela e orçamento deste documento já está dimensionado para **1 a 20**.

Consequências já resolvidas aqui, para ninguém regredir:

| Consequência | Onde está resolvida |
|---|---|
| Curva de Eficiência reespaçada (+2 a +8, um degrau a cada 3 níveis) | 4.3 |
| Nível de desbloqueio da Eficácia (mantido no 5, com slots progressivos) | 4.3 |
| Níveis de Habilidade expandidos para **1-7**, com tabelas novas | 10.1 e 10.2 |
| Teto de **8 Habilidades conhecidas** (em vez de "uma por nível") | 10.3 |
| Bênçãos: **12 escritas por Caminho, 10 adquiridas**, Avatar movido para o **nível 17** | 11.3 |
| PV fixo estendido até o 20 | 6.1 |
| Passe de balanceamento em 5 faixas (1-4, 5-8, 9-12, 13-16, 17-20) | 18 |
| Tabela de DT por faixa + regra de Sucesso Automático | 18.4 |
| Bestiário em 5 faixas (Comum/Elite/Boss) | 18.3 e capítulo 28 |
| Cones de Luz, Relíquias e Ressonâncias espalhados pelos 20 níveis | 16.3 a 16.5 |

Tudo isso está no changelog da seção 21.

---

## 1. Visão geral

A v0.1 já tem um sistema de verdade dentro dela: d20 + Bônus de Atributo + Eficiência contra uma DT, 6 Atributos, 9 Caminhos, 7 Elementos, Tenacidade e Quebra, Habilidades criadas pelo jogador e Ultimate em 100 de energia. O que falta não é identidade, é fechamento. A v0.1 cita "derrubar o turno em N casas" em 3 lugares e "distância" em outros 15, sem nunca dizer o que é uma casa; usa Vantagem, RD e acerto crítico sem defini-los; e tem três lugares onde a matemática se contradiz (Bônus de Atributo 13/14, Esquiva somando Agilidade duas vezes, PV de nível 1 variando de 2d20 a 6d20).

Este documento fecha tudo isso. Ele **não** escreve o livro: ele trava as decisões mecânicas, os números-âncora e a estrutura de capítulos, para que a fase de escrita não redescubra problemas já resolvidos. Toda decisão aqui vem com o porquê, porque a fase de escrita vai precisar defender esses números no texto.

Três princípios guiaram cada escolha:

1. **Preservar o DNA.** Nada do que a v0.1 estabeleceu como identidade foi trocado. O que estava quebrado foi consertado pelo caminho mais curto, não pelo mais elegante.
2. **Rastreável no papel.** Honkai: Star Rail calcula ordem de turno com `10000/VEL` por ação. Isso é inviável numa mesa. A v1.0 usa uma **Fila de Ação** com casas numeradas, que o Mestre desenha numa tira de papel e move com fichas.
3. **Matemática com teto.** Todo bônus tem limite, todo acúmulo tem máximo, toda redução tem piso. Um sistema de **nível 1 a 20** com Eficácia (dobro da Eficiência) estoura muito rápido se ninguém colocar um teto — e com 20 níveis o estouro é o dobro do que seria com 10.

---

## 2. Stack e formato do projeto (travado)

| Item | Decisão |
|---|---|
| Idioma | PT-BR, em tudo (regras, nomes de arquivo em kebab-case sem acento, comentários de script) |
| Formato do livro | Markdown (GitHub Flavored Markdown), UTF-8, tabelas nativas do GFM |
| Organização | 1 arquivo `.md` por capítulo em `livro-v1.0/`, prefixo numérico de 2 dígitos definindo a ordem |
| Imagens | PNG já extraídos, em `assets/imagens-v01/`, referenciados por caminho relativo |
| Scripts de apoio | PowerShell 5.1 (`powershell.exe`; **não** existe `pwsh` nesta máquina) em `scripts/` |
| Montagem final | Pandoc (opcional) de `livro-v1.0/*.md` para `.docx`/`.pdf` em `build/` |
| Versionamento | O `.docx` da v0.1 permanece intocado como registro histórico |

Essa stack está fechada. A escrita dos capítulos não introduz outro formato, outro gerador de PDF nem outra linguagem de script.

---

## 3. Convenção de nomenclatura normalizada

A convenção tem **duas naturezas diferentes**, e misturá-las foi o que quase transformou o checador de nomenclatura num gate que reprovava o livro inteiro. Elas estão separadas de propósito:

- **Coluna A — strings proibidas.** Palavras que **não existem** no vocabulário de Explorando Galáxias. `scripts/checar-nomenclatura.ps1` procura por elas e **falha o build**. Lista fechada, abaixo.
- **Coluna B — uso incorreto.** Palavras que o livro **usa**, mas que não podem aparecer no lugar do termo oficial. Isso é julgamento de contexto, **não** é checável por string, e por isso **não** entra no script: fica para a revisão humana.

### 3.1 Coluna A — strings proibidas (checagem automática, falha fatal)

`HP` · `DoT` · `iniciativa` · `ação bônus` · `ação menor` · `ação comum` · `ação completa` · `rodada` · `round` · `stagger` · `poise` · `break` · `skill points` · `SP` · `mana` · `memosprite` · `CD` · `salvaguarda` · `save` · `proficiência` · `ult charge` · `push back` · `action advance` · `provavelmente vou mudar o nome` · `nível 1 a 10`

Nenhuma dessas 25 strings tem uso legítimo em nenhum dos 28 capítulos de regra. As exceções de arquivo e de linha estão em 23.

**Como o script casa** (para `checar-nomenclatura.ps1` não gerar falso positivo): busca **insensível a maiúsculas** e **delimitada por fronteira de palavra** (`\b`). É por isso que `break` não casa dentro de "Quebra" e `CD` e `SP` não casam dentro de outra palavra. As frases de duas palavras (`ação bônus`, `ação comum`, `ação completa`, `ação menor`, `ult charge`, `skill points`) são buscadas inteiras, e nenhuma delas é prefixo de termo oficial — `Ação Complementar` não contém `ação comum` nem `ação completa`.

### 3.2 Coluna B — termo oficial e o uso incorreto que ele substitui (revisão humana)

| Oficial | Não use no lugar dele | Observação |
|---|---|---|
| **PV** (Pontos de Vida) | "vida", "pontos de saúde" como estatística | "PV" em tabelas; "pontos de vida" é aceitável em prosa. A palavra "vida" continua legítima em **Propósito de Vida**, **Fonte da Vida Eterna**, **Excesso de Vida**, **Último Fragmento de Vida** e em prosa narrativa |
| **DT** (Dificuldade do Teste) | "classe de dificuldade" | DT **é** "Dificuldade do Teste": a palavra "dificuldade" é parte do termo oficial e aparece como cabeçalho de coluna em 18.4 |
| **Teste de Perícia** | "checagem", "rolagem de perícia" | |
| **Teste de Ataque** | "rolagem de ataque", "jogada de ataque" | |
| **Teste de Resistência** | "resistência" sozinho, quando se fala do teste | 6 nomes oficiais, ver abaixo. "Resistência" continua sendo o nome de uma **Perícia** e da **Resistência a Elemento** |
| **Eficiência** / **Eficácia** | "bônus de nível" | Eficácia = dobro da Eficiência |
| **Tenacidade** | "barra de resistência" | |
| **Quebra** / **Quebrado** | "romper" | "sofrer Quebra", "está Quebrado". "Romper" continua válido em prosa de ação |
| **Dano de Quebra** | — | |
| **Ciclo** | "turno do grupo" | Um Ciclo = uma passagem completa pela Fila de Ação |
| **Turno** | "vez" | O turno é de um combatente só. A palavra "ação" é oficial em **Ação Complementar**, **Ação de Movimento**, **Ação Extra** e "as 4 Ações" |
| **Fila de Ação** / **casa** | "ordem de iniciativa" | A "casa" é a posição na Fila |
| **Atrasar** (em N casas) | "derrubar o turno", "empurrar" | Termo da v0.1 aposentado em favor de "Atrasar" |
| **Avançar** (em N casas) / **Avanço Total** | "adiantar" | |
| **Distância** | "metros", "quadrados", "casas de grade" | Escala: Pessoal, Curta, Média, Longa, Extrema |
| **Ação Complementar** | "ação bônus" (proibida), "bônus" como nome de ação | **Bônus de Atributo**, **Bônus Maior** e **Bônus de Velocidade** são termos oficiais e aparecem em quase toda tabela |
| **Ataque Básico** | "ataque comum", "ação de ataque" | |
| **Ação de Movimento** | "deslocamento", "move" | |
| **Reação** | "reação livre", "interrupção" | 1 por turno |
| **RD** (Redução de Dano) | "resistência a dano" | "Resistência" (a Elemento) é outra coisa. **Armadura ou Vestimenta** e **Bônus de Armadura** são termos oficiais (6.2, 16.1) |
| **Velocidade** (VEL) | "speed" | |
| **PH** (Pontos de Habilidade) | — | Reserva compartilhada do grupo |
| **Energia** | "carga" | Energia é só da Ultimate |
| **Dano Contínuo** (DC) | "dano ao longo do tempo" | A v0.1 usa "DoT" nas Bênçãos da Inexistência |
| **Bênção** | "talento", "feat", "perk" | Poderes de Caminho |
| **Memoespírito** | "invocação", "pet" | |
| **Executado** | "morte instantânea", "finalizar" | |
| **Propósito de Vida** | "objetivo", "meta" | |
| **Esforço** | "ponto de sorte", "inspiração" | Recurso **exclusivo do Humano** (12) |
| **Esforço Total** | "turno inteiro" | Trocar o Ataque Básico e a Ação Complementar por movimento dobrado (8.1) |
| **Especialização de Combate** | — | **Mecânica nova da v1.0**, sem termo correspondente na v0.1 (nada a aposentar). Vale em **todos** os seus Testes de Ataque (4.3) |
| **Barreira** | "escudo", "shield" | PV temporário com nome próprio, recurso da Preservação |
| **Nível equivalente** | "nível da Ultimate" | A faixa da Ultimate para ler as tabelas de 10.1 e 10.2 (8.5) |
| **Falhe para frente** | "falha seca", "nada acontece" | Regra nomeada do capítulo 02, definida abaixo |

**Os 6 Testes de Resistência oficiais** (nomes fechados, nunca abreviados nem reordenados): Potência Física, Reflexos, Resistência Física, Resistência Mental, Percepção Mental, Força de Vontade.

**Falhe para frente (regra nomeada, capítulo 02 e glossário):** uma falha em Teste de Perícia **não trava a cena**. O Mestre descreve o que acontece de pior — a cena avança, com custo: tempo, ruído, um recurso gasto, uma complicação nova, a informação chegando incompleta. "Você não conseguiu, tente de novo" não é resultado de falha; é a cena parada.

**Arredondamento e mínimos (regra global, capítulo 02):** todo resultado fracionário arredonda **para baixo** — inclusive as **médias impressas** nas tabelas de dano e cura, que são `floor(número de dados × média do dado)`. Toda instância de dano que chegaria a 0 por RD, Resistência ou divisão causa **1 de dano**. Todo efeito que reduziria um número de dados a 0 conserva **1 dado**.

**Precedência de regras:** (1) texto específico de uma Habilidade, Bênção ou item; (2) regra do capítulo daquele subsistema; (3) regra geral do capítulo 02; (4) decisão do Mestre, registrada na Ficha de Decisões da Mesa (apêndice). O específico sempre vence o geral, e o Mestre só entra quando os três primeiros níveis se calam.

---

## 4. O núcleo matemático

### 4.1 A rolagem única

Tudo no sistema é a mesma conta:

> **d20 + Bônus de Atributo + Eficiência (ou Eficácia, se você tiver) ≥ DT**

Isso vale para Teste de Perícia, Teste de Ataque (a DT se chama Defesa) e Teste de Resistência. Não existe outra fórmula de resolução no livro.

### 4.2 Como se lê uma DT (exemplo; a tabela oficial é a de 18.4)

> **Existe uma única tabela de DT GERAL no livro: a tabela por faixa de nível de 18.4.** O que está abaixo é o exemplo de leitura que o capítulo 02 usa para ensinar a escala, com os valores **da faixa 1-4** copiados de lá.
>
> **Subsistemas específicos podem ter DT própria**, e quando têm, ela mora na tabela do próprio subsistema e **vence a geral**. A lista é fechada, são cinco, e nenhum capítulo cria uma sexta:
>
> 1. **DT para descobrir uma Fraqueza** — por faixa do inimigo (9.3).
> 2. **DT da Surpresa — 13, fixa em todas as faixas** (7.3).
> 3. **DT 10 do Teste de Força de Vontade de Morrendo** (15.1).
> 4. **DT 10 do Teste de Percepção Mental** do traço Raposa Astuta dos Vulpes (12).
> 5. **DT 13 do Teste de Sintonia** do traço To na sua mente do Haloviano (12).

| Dificuldade | DT na faixa 1-4 | Quando usar |
|---|---|---|
| Trivial | 8 | Só role se houver pressa ou plateia |
| Fácil | 10 | Um profissional faz dormindo |
| Média | 13 | O padrão de uma cena tensa |
| Difícil | 16 | Exige treino e um pouco de sorte |
| Muito Difícil | 19 | Feito digno de nota na Expresso Astral |
| Heroica | 22 | Beira o impossível para a faixa |

**DT das suas Habilidades e efeitos** (quando a Habilidade pede um Teste de Resistência do alvo em vez de um Teste de Ataque):

> **DT = 8 + Bônus do seu Atributo de Habilidade + Eficiência**

### 4.3 Eficiência e Eficácia: onde cada uma se aplica

#### Curva de Eficiência reespaçada para 1-20

A curva da v0.1 só vai até o 10 e **acelera no fim**: um degrau a cada 3 níveis (1-3, 4-6), depois a cada 2 (7-8), depois a cada 1 (9, 10). Estender esse padrão até o 20 daria algo como +16 de Eficiência, +32 de Eficácia, e nenhuma DT do universo seguraria isso.

**Decisão: um degrau a cada 3 níveis, do +2 ao +8.**

| Nível | 1-3 | 4-6 | 7-9 | 10-12 | 13-15 | 16-18 | 19-20 |
|---|---|---|---|---|---|---|---|
| **Eficiência** | +2 | +3 | +4 | +5 | +6 | +7 | +8 |
| **Eficácia** | +4 | +6 | +8 | +10 | +12 | +14 | +16 |

*Por quê:* mantém **intactos os níveis 1 a 6 da v0.1** (+2 e +3 nas mesmas faixas), que é onde a maioria das mesas joga, e troca a aceleração do fim por um ritmo constante que chega ao nível 20 com um número que a tabela de DT consegue sustentar. O teto +8 foi escolhido porque, somado ao Bônus de Atributo máximo (+5), à Especialização de Combate (+3) e ao Cone de Luz (+3), fecha em **+19** de ataque no nível 19-20 para o atacante de referência. Com os personagens de suporte e sustentação 3 pontos abaixo, o grupo inteiro fica entre **+16 e +19** na faixa 17-20, e o ponto médio dessa faixa (+17,5) entrega **70% de acerto contra Comum, 60% contra Elite e 55% contra Boss** — a janela única que o passe de balanceamento usa nas cinco faixas (18.1 e 18.3).

*O que muda em relação ao que o autor escreveu:* o nível 9 passa de +5 para +4 e o nível 10 passa de +6 para +5. Está registrado no changelog (21) como mudança consciente, não como erro de transcrição.

#### Onde cada uma se aplica

**Decisão travada: a Eficácia NUNCA entra em Teste de Ataque.** Ela se aplica a Perícias e Testes de Resistência escolhidos, e só entra num ataque se o texto de uma Habilidade específica disser isso em letras claras.

*Por quê:* no nível 20 a Eficiência vale +8 e a Eficácia +16. Se a Eficácia valesse para ataque, o personagem especializado chegaria a `d20 + 5 + 16 + 3 + 3 = +27` em vez dos +19 orçados em 18.2, obrigando Defesas de Boss na casa de 35 para manter os **mesmos 65% de acerto do atacante de referência** (que hoje são +19 contra Defesa 27 de Boss: 8 ou mais no d20). Com Defesa 35, o ataque de um aliado de suporte (+16) precisaria de 19 ou 20 no dado. Um único número duplicado arrastaria a tabela inteira de Defesa, de dano inimigo e de sobrevivência dos PJs, e a diferença entre o ataque especializado e o resto viraria 8 pontos de d20 (40% de acerto). A Eficácia continua existindo e continua sendo o dobro: ela só não mora na linha de ataque.

A escalada de acerto que o jogador sente vem da **Especialização de Combate**: **+1 em todos os seus Testes de Ataque** no **nível 5**, **+2** no **nível 11**, **+3** no **nível 17**. Limitada, previsível, permanente e **fora do teto de bônus somado** (9.6), porque já está no orçamento de 18.2.

> **A Especialização de Combate é mecânica NOVA da v1.0, não a renomeação de nada.** A v0.1 não tem bônus de ataque progressivo por nível de nenhum tipo — lá o acerto cresce só pela Eficiência. Ela entra no changelog (21.2) na lista de **mecânicas novas**, e o capítulo 01 precisa apresentá-la como acréscimo, para o autor não procurar na v0.1 de onde ela veio.

*Por quê em todos os Testes de Ataque e não só numa categoria de arma:* amarrá-la a uma categoria de arma deixaria as Habilidades **3 pontos atrás** do Ataque Básico no nível 20 — e Habilidade é a maior fonte de dano do jogo. O efeito prático seria dois números de ataque diferentes na mesma ficha e um incentivo torto a bater com a arma justamente nos turnos em que a Habilidade importa. Um número de ataque por personagem é mais rápido na mesa. (Quem escolhe uma arma que usa um Atributo diferente do seu Atributo de Habilidade continua com dois números, mas isso é consequência da escolha de atributo, não da Especialização.)

**Onde você ganha Eficácia (slots progressivos):**

| Nível | Ganho | Total acumulado |
|---|---|---|
| **5** | 1 Perícia + 1 Teste de Resistência | 1 P / 1 TR |
| 8 | +1 Perícia | 2 P / 1 TR |
| 11 | +1 Teste de Resistência | 2 P / 2 TR |
| 14 | +1 Perícia | 3 P / 2 TR |
| 17 | +1 Perícia | 4 P / 2 TR |
| 20 | +1 Perícia +1 Teste de Resistência | 5 P / 3 TR |

*Por quê manter o desbloqueio no nível 5:* o número 5 é DNA — o autor escreveu "desbloqueado no Nível 5" e a mesa dele já conhece essa promessa. O problema de "o 5 é cedo demais num jogo de 20 níveis" não está em *existir* Eficácia, está em *quanta* Eficácia. Resolvi gatilhando a quantidade: no nível 5 você dobra **uma** Perícia e **um** Teste de Resistência (ganho real, comemorável, contido), e os outros slots chegam a cada 3 níveis. Mover o desbloqueio para o 10 teria o efeito colateral de deixar os níveis 5 a 9 sem nenhuma entrega de sistema, já que Habilidade e Bênção já ocupam outros níveis.

Você tem **Eficiência nos 6 Testes de Resistência** desde o nível 1 — eles são o piso de competência de um personagem. Perícia sem Eficiência rola só `d20 + Bônus de Atributo`.

### 4.4 Vantagem e Desvantagem (lacuna L05)

A v0.1 distribui Vantagem em quatro raças e várias Bênçãos sem nunca dizer o que é. Fechado:

- **Vantagem:** role 2d20 e use o maior.
- **Desvantagem:** role 2d20 e use o menor.
- **Não acumulam.** Três fontes de Vantagem ainda são 2d20. Isso é deliberado: acumular dados vira contabilidade e dá curvas absurdas.
- **Vantagem e Desvantagem se cancelam** por presença, não por contagem. Uma de cada, ou cinco de uma e uma de outra: em todos os casos você rola 1d20 puro.
- Vale para qualquer rolagem de d20 (Ataque, Perícia, Resistência).
- Com Vantagem, um **20 natural em qualquer um dos dois dados** é acerto crítico. Com Desvantagem, o que conta (para crítico e para 1 natural) é o dado efetivamente usado.

### 4.5 Teste de Ataque formal (lacuna L04)

> **Teste de Ataque = d20 + Bônus do Atributo de Ataque + Eficiência ≥ Defesa do alvo**

**Qual atributo, por categoria** (tabela fechada, capítulo 18). As categorias são **exatamente as seis de 9.2**, nem uma mais; os exemplos entre parênteses são ilustração, não taxonomia:

| O que você está usando | Atributo de Ataque |
|---|---|
| **Leve** (adaga, lâmina curta, chicote) | Agilidade |
| **Média** (espada de uma mão, lança curta, bastão) | **Poder ou Agilidade, fixo na criação** |
| **Pesada, 2 mãos** (martelo, montante, punhos reforçados) | Poder |
| **Disparo curto** (pistola, besta de mão) | Agilidade |
| **Disparo longo, 2 mãos** (arco, rifle) | Agilidade |
| **Energia, 2 mãos** (canhão, catalisador, drone de combate) | Sincronia |
| **Habilidade ou Ultimate** | Seu **Atributo de Habilidade** |
| Ataque do Memoespírito | Atributo escolhido na ficha dele |

A categoria **Média** é a arma de referência do orçamento de balanceamento (18.2), e é a única que deixa o jogador escolher entre dois atributos — é a espada de uma mão que tanto o lutador de Poder quanto o esgrimista de Agilidade empunham. A escolha é feita na criação e não muda.

O **Atributo de Habilidade** é escolhido na criação do personagem, dentro do que o Caminho permite (tabela em **11.1**), e é fixo. É o mesmo atributo que define a DT das suas Habilidades. Isso impede o personagem de otimizar um atributo para acertar e outro para a DT.

**Quando não há Teste de Ataque:** Habilidades de área, de controle e de debuff podem exigir um Teste de Resistência do alvo contra a sua DT (8 + atributo + Eficiência) em vez de um Teste de Ataque. Cada Habilidade declara qual dos dois usa, no momento em que é criada. Nenhuma Habilidade usa os dois.

**Falha:** o ataque erra, não causa dano e não reduz Tenacidade. A **Energia da ação é ganha normalmente** (8.3): a v0.1 concede Energia pela ação e não pelo acerto, e isso fica. O **PH não é gerado** por um Ataque Básico que erra, e o PH gasto por uma Habilidade que erra **não é devolvido** — o custo é pago na declaração, e é isso que torna errar relevante. (Essa é a leitura única: nenhuma outra seção condiciona Energia ao acerto.)

**20 natural:** acerto automático e acerto crítico, independente da Defesa.

**1 natural (erro crítico):** falha automática, independente dos bônus, e você **não ganha Energia de Ultimate por essa ação**. Não existe tabela de trapalhadas.

*Por quê sem tabela de trapalhada:* num sistema onde o jogador desenha as próprias Habilidades, punir o 1 natural com efeitos aleatórios castiga builds que atacam muitas vezes e gera discussão de mesa. Perder o ataque e o ganho de Energia já é um custo real (atrasa a Ultimate em ~1 turno) e é trivial de aplicar.

### 4.6 Acerto crítico (lacuna L03)

| Pergunta | Resposta travada |
|---|---|
| Faixa | **20 natural**. **Teto absoluto do jogo: 19-20**, e a **única** fonte que chega lá é a Bênção de abertura do Caminho da Caça. Nenhum Cone de Luz, Relíquia, Bênção ou Habilidade expande a faixa de crítico, e **expandir a faixa de crítico é efeito proibido** em Habilidade criada pelo jogador (10.4) |
| O que dobra | **Só os dados base** do ataque: os dados da arma, ou os dados da tabela da Habilidade, ou os dados da Ultimate. Você rola esses dados duas vezes e soma |
| O que **não** dobra | Dados ganhos por **Fraqueza** do alvo (regra já escrita na v0.1), dados e bônus de Bênçãos/buffs/itens, modificadores fixos (incluindo o Bônus de Atributo) e **Dano Contínuo** |
| Tenacidade | Crítico reduz Tenacidade normalmente (sem bônus). A Quebra já é o "crítico" do sistema de Tenacidade |
| Em Perícias e Testes de Resistência | Não existe crítico. 20 natural é um sucesso memorável (narrativo), 1 natural é uma falha memorável. Zero efeito mecânico |
| Caminho da Caça | A Bênção de abertura da Caça expande a faixa para **19-20**. A Bênção capstone da Caça (requisito nível 17) adiciona **+1 dado base** ao dano do crítico (não dobra de novo e **não expande a faixa de novo**: adiciona um dado) |

*Por quê o teto é 19-20 e não 18-20:* a iteração anterior reservava 18-20 como guarda-corpo, mas nenhuma fonte do livro chegava lá — era corrimão de escada inexistente, e um corrimão desse tipo é convite para a próxima pessoa construir a escada. Com o teto em 19-20 e a expansão de faixa na lista de efeitos proibidos de 10.4, a Caça fica com um privilégio que **ninguém pode copiar**, e o crítico continua valendo 5% das rolagens para todo o resto da mesa — que é a premissa que o DPC usa em 18.1.

*Por quê dobrar dados e não o dano total:* a v0.1 já diz, com essas palavras, que os dados ganhos por Fraqueza não critam — dobrar o total contrariaria o autor. E dobrar o total arrastaria junto todo bônus fixo empilhado (atributo, Relíquia, Cone de Luz, buff de aliado), fazendo o crítico premiar a **pilha de bônus** em vez da ação. Com a regra fechada, um crítico de Habilidade Nível 7 com Fraqueza no nível 20 vai de **215 para 404** contra um Boss de 935 PV (18.3) — 43% da barra dele em um golpe, com 5% de chance de acontecer: assustador, memorável e raro, que é exatamente o lugar do crítico neste sistema.

*Por quê 19-20 é privilégio da Caça:* é a identidade do Caminho em Honkai: Star Rail (precisão e dano em alvo único) e dá à Caça algo que nenhum outro Caminho tem, compensando ela ser a mais frágil em PV.

---

## 5. Atributos

Os 6 Atributos e suas descrições da v0.1 ficam idênticos: Poder, Agilidade, Vigor, Sincronia, Discernimento, Presença.

### 5.1 Tabela de Bônus de Atributo (lacuna L07 / erro E02)

A v0.1 tem: 8 → -1, 10 → +0, 12 → +1, **13 → +2, 14 → +2**, 15 → +3. Dois problemas: 13 e 14 dão o mesmo bônus (então subir de 13 para 14 é desperdício puro), e o salto de 12 para 13 vale mais que o de 13 para 14. Além disso a tabela não cobre valores acima de 15, que as raças já produzem (+2 sobre um 15 dá 17) e que os aumentos por nível vão produzir.

**Tabela nova, monotônica, cobrindo 8 a 20:**

| Valor | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Bônus** | -1 | -1 | +0 | +0 | +1 | +1 | +2 | **+3** | +3 | +4 | +4 | +5 | +5 |

*Por quê assim:* a tabela preserva todos os marcos que o autor escreveu (8 = -1, 10 = +0, 12 = +1, 14 = +2, **15 = +3**) e só muda o 13, que cai de +2 para +1. O 15 continua sendo o degrau premiado, porque é o topo do array e é onde o autor quis que a especialização aparecesse. Daí para cima a progressão é de +1 a cada 2 pontos, e é justamente por isso que os aumentos por nível (5.3) vêm em **+2**: cada aumento entrega um degrau cheio, nunca meio degrau. **Teto do jogo: 20 (bônus +5)**, alcançável já no nível 6 por quem foca — e é por isso que o Bônus de Atributo **não** é o motor de crescimento da campanha longa: ele satura cedo de propósito, e quem cresce depois é a Eficiência, a Habilidade e o equipamento.

Resultado do array oficial `15, 14, 13, 12, 10, 8` → **+3, +2, +1, +1, +0, -1** (soma +6).

### 5.2 Compra de Pontos (lacuna L10 / ponto 10)

A v0.1 promete: "futuramente outras opções de valores poderão ser usadas como por exemplo a compra de pontos". **Decisão: implementar como método oficial alternativo**, não como variante marcada. O Mestre escolhe um método para a mesa inteira na primeira sessão.

**28 pontos**, todos os atributos começam em 8, máximo de 15 antes de bônus de Raça:

| Valor | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|
| **Custo acumulado** | 0 | 1 | 2 | 3 | 4 | 5 | 7 | 10 |

*Por quê 28 e por quê o custo sobe:* 28 é exatamente o preço do array oficial nessa tabela (10+7+5+4+2+0), então os dois métodos nascem equivalentes e ninguém chega à mesa com vantagem matemática. O custo acelera em 14 e 15 porque o 15 vale +3 na tabela nova: sem encarecer, todo mundo compraria dois 15 e três 8, e o jogo viraria duas estatísticas. Com esse preço, dois 15 custam 20 dos 28 pontos e sobram 8 para espalhar — é uma build legítima, mas paga caro.

### 5.3 Aumentos de Atributo por nível (lacuna L12 / ponto 12)

**Decisão: adicionar.** Nos níveis **3, 6, 9, 12, 15 e 18** você ganha **+2 em um Atributo ou +1 em dois**, respeitando o teto 20.

*Por quê adicionar:* sem isso, o Bônus de Atributo fica congelado por 20 níveis e toda a sensação de crescimento recai sobre a Eficiência e as Habilidades. Com 6 aumentos (+12 no total) e teto 20 por atributo, o personagem focado satura o atributo principal cedo (nível 6) e depois **espalha**: vira um personagem completo em vez de um pico só. É o arco de progressão que um jogo de 20 níveis precisa.

*Por quê nesses níveis:* são os níveis sem outra entrega. O 1, 3, 5... (ímpares) entregam Bênção; o 3, 6, 9... entregam Habilidade de Nível novo a cada 3; o 5 entrega Eficácia. Alinhar os aumentos ao múltiplo de 3 garante que **nenhum dos 20 níveis suba vazio** (ver a tabela mestra em 17).

**PV e aumento de Vigor:** quando o seu Bônus de Vigor aumenta, você ganha **PV igual ao seu nível atual + 2**, na hora. Não recalcule níveis anteriores.

*Por quê o +2:* pela fórmula de 6.1, o Bônus de Vigor entra **3 vezes** no nível 1 e **1 vez** em cada nível seguinte. Um ponto ganho no nível L vale, retroativamente, `3 + (L-1)` = **L+2** PV. Como daí para frente o seu incremento por nível já usa o Vigor novo, o ganho na hora mais os incrementos seguintes somam exatamente o valor retroativo: dois personagens idênticos que subiram Vigor em níveis diferentes chegam ao **mesmo PV** no mesmo nível. Com "PV igual ao nível", quem subisse Vigor cedo era punido e nenhum dos dois batia com a tabela de 6.1.

### 5.4 Perícias — correções pontuais

As 18 Perícias da v0.1 ficam idênticas, com três consertos:

- **Quantidade:** Eficiência nas 3 Perícias do seu Caminho + `2 + Bônus de Sincronia` escolhidas, **mínimo de 2 escolhidas** (erro E17: com Sincronia 8, a conta dava 1).
- **Sintonia (+Discernimento ou +Sincronia):** você escolhe o atributo na criação e ele é **fixo** (erro E18). Trocar por teste faria da Perícia a melhor do livro.
- **Teste de Atenção dos Vulpes:** aposentado. Vira **Teste de Percepção Mental, DT 10** (erro E13). O sistema tem 6 Testes de Resistência oficiais; não existe um sétimo exclusivo de uma raça.

---

## 6. PV, Defesa, Esquiva, RD e Velocidade

### 6.1 PV: fim dos dados de vida oscilantes (lacuna L09 / ponto 9 / erros E04, E05)

A v0.1 manda rolar os dados de vida do Caminho no nível 1 (de 2d20 na Caça a 6d20 na Destruição) e 1d20 por nível depois. Dois defeitos sérios:

- Um Caça pode rolar 2 em 2d20 e começar a campanha com **2 PV**. Um aliado da Destruição pode rolar 100 e ter 50x mais vida que ele.
- O 1d20 fixo por nível é igual para todos, então a diferença entre Caminhos **encolhe** conforme o jogo avança — o contrário do que a fantasia pede.

**Decisão: PV fixo, com variante de rolagem opcional.** Mantive o número de dados do Caminho como o "índice de vitalidade" (N), porque é a proporção que o autor desenhou:

> **PV no nível 1 = 25 + (5 × N) + (3 × Bônus de Vigor)**
> **PV por nível (2 a 20) = 5 + N + Bônus de Vigor**

| Caminho | N | PV nível 1 (Vigor +2) | Por nível | PV nível 10 | PV nível 20 |
|---|---|---|---|---|---|
| A Destruição | 6 | 61 | 13 | 178 | 308 |
| A Preservação | 5 | 56 | 12 | 164 | 284 |
| A Abundância | 5 | 56 | 12 | 164 | 284 |
| A Inexistência | 4 | 51 | 11 | 150 | 260 |
| A Harmonia | 3 | 46 | 10 | 136 | 236 |
| A Erudição | 3 | 46 | 10 | 136 | 236 |
| A Euforia | 3 | 46 | 10 | 136 | 236 |
| A Recordação | 3 | 46 | 10 | 136 | 236 |
| A Caça | 2 | 41 | 9 | 122 | 212 |

> **Como ler esta tabela:** os valores são calculados com **Bônus de Vigor +2 constante**, que é o que o array oficial entrega a um personagem que não foca Vigor. Cada ponto de Bônus de Vigor acima disso adiciona `nível + 2` PV no nível em que foi ganho e `+1` em cada nível seguinte (5.3). As âncoras de 18.2 usam a mesma premissa.

*Por quê comprimir a faixa:* a v0.1 tem 6d20 contra 2d20, uma razão de 3 para 1. Nenhum jogo sobrevive a isso: ou o inimigo mata o Caça em um golpe, ou não arranha a Destruição. A fórmula nova mantém a **ordem exata** dos Caminhos e aperta a razão para 1,45:1 — que é a diferença real entre um tanque e um DPS frágil em Honkai: Star Rail.

*Por quê a fórmula funciona até o 20:* o incremento por nível também carrega o N do Caminho, então a diferença entre Caminhos **cresce em valor absoluto** (20 PV de diferença no nível 1, 96 no nível 20) mas **se mantém em proporção**. É o oposto do 1d20 fixo da v0.1, que fazia os Caminhos convergirem. Com 20 níveis isso seria desastroso: no nível 20 da v0.1, Destruição (25d20 ≈ 262) e Caça (21d20 ≈ 220) ficariam a 19% de distância, ou seja, o Caminho mais resistente do jogo e o mais frágil seriam praticamente iguais — e com uma variância de rolagem de mais de 100 PV entre dois personagens do mesmo Caminho.

*Por quê PV fixo e não média arredondada com rolagem:* numa campanha de 1 a 20 com Habilidades que causam até 189 de dano, PV é a estatística que decide se a mesa é divertida ou aleatória. Rolagem de PV transfere o balanceamento do designer para o dado. Para quem gosta do risco, fica a **variante oficial**: role `1d20` por nível no lugar do valor fixo, com **piso igual ao valor fixo menos 3 e teto igual ao valor fixo mais 5**. Variante marcada, não padrão.

### 6.2 Defesa

> **Defesa = 10 + Bônus de Agilidade + Bônus de Armadura ou Vestimenta + outros bônus aplicáveis**

Idêntica à v0.1. Defesa é passiva: o inimigo rola contra ela, você não rola nada.

### 6.3 Esquiva: parar de contar Agilidade duas vezes (lacuna L08 / ponto 8 / erro E03)

A v0.1 define Esquiva como `Defesa + Bônus de Agilidade`, e a Defesa já inclui o Bônus de Agilidade. Um personagem com Agilidade 20 ganharia +10 de Defesa de uma Reação só.

**Decisão: Esquiva = Reação que soma a sua Eficiência à sua Defesa contra um único ataque.**

- Declare **antes** da rolagem de ataque inimigo (regra que a v0.1 já tinha, mantida).
- Custa a sua Reação do turno. Só em cena de combate.
- **A Esquiva soma sempre Eficiência, nunca Eficácia.** Não existe fonte no livro que troque uma pela outra aqui — nem Eficácia em Acrobacia, nem Bênção, nem Habilidade, nem Cone de Luz.
- **Armadura Pesada não permite Esquiva.** É o preço dos +6 de Defesa.

> **Por quê a Esquiva é a única coisa no livro que a Eficácia não toca:** ela é gratuita, universal e disponível **todo turno**, sem gastar PH, Energia nem acúmulo. Ela é a única estatística defensiva que entra em **toda** rolagem de ataque inimigo que o jogador quiser, e por isso está dentro das premissas de balanceamento (18.1) com número fechado. Somar Eficácia levaria o bônus a **+16** no nível 20: o inimigo de referência precisaria de 25 num d20 e só acertaria no 20 natural. Isso não é uma Reação boa, é imunidade a um ataque por turno — e derrubaria a janela de attrition inteira (18.3).

*Por quê Eficiência e não um Teste oposto:* o teste oposto (rolar d20 + Agilidade contra o ataque) é mais emocionante, mas acrescenta uma rolagem a cada ataque inimigo e transforma qualquer combate contra 4 inimigos em 8 rolagens por Ciclo. A Esquiva como bônus fixo resolve em zero dados e dá um número que o jogador conhece de antemão (+2 no nível 1, +5 no 12, +8 no 20), o que permite decidir se vale gastar a Reação. E ela escala com nível em vez de escalar com a estatística que o personagem já maximizou e que já satura no nível 6.

*Quanto ela vale no orçamento:* contra o ataque inimigo da faixa 17-20 (+13 contra Defesa de referência 22, 60% de acerto), a Esquiva leva o alvo a Defesa 30 e o acerto a **20%**. Como cada personagem tem **1 Reação** e ela também paga Intervir e as Reações de Bênção, a premissa publicada é **1 ataque Esquivado por Ciclo no grupo** (18.1) — não todos. É isso que mantém a attrition na janela de **73% a 81%** dos PV (18.3) em vez dos 89% que a Esquiva irrestrita produziria.

*Por quê não cortar a Esquiva de vez:* é a única Reação universalmente útil da v0.1 e a razão de existir o campo "Reação" na ficha. Sem ela, personagens sem Bênção de Reação nunca usariam o recurso.

### 6.4 RD — Redução de Dano (lacuna L06 / ponto 6 / erro E11)

A v0.1 usa "RD" em Armadura Pesada (10 RD) e em pelo menos 8 Bênçãos (+10, +15, +5 RD) sem definir o que significa.

**Regra travada:**

- RD subtrai um valor fixo **de cada instância de dano**, aplicada **depois** dos ajustes de dados por Fraqueza/Resistência e **depois** do crítico.
- Uma instância = um ataque, uma Habilidade, um tique de Dano Contínuo, um Dano de Quebra. Habilidade em área: a RD se aplica **uma vez por alvo** — e "área" tem número de alvos fechado em **10.1** (até 3 alvos; 4 nos Níveis 6 e 7; nunca mais de 6).
- Múltiplas fontes de RD **somam**, até o teto.
- **Teto de RD = 2 + (2 × Eficiência)**: 6 nos níveis 1-3, 8 nos 4-6, 10 nos 7-9, 12 nos 10-12, 14 nos 13-15, 16 nos 16-18, 18 nos 19-20.
- Toda instância causa **no mínimo 1 de dano**. Não existe imunidade por RD.
- **Dano Contínuo ignora RD** (ver 9.5).

*Por quê o teto:* com Armadura Pesada (v0.1: 10 RD) mais duas Bênçãos de Abundância (+10 e +10), um personagem de nível 2 teria 30 de RD contra ataques inimigos de 10-14 de dano — literalmente invulnerável. O teto amarra a RD à Eficiência, então ela cresce junto com o dano do jogo em vez de estourá-lo.

**RD de inimigo:** inimigos usam a mesma regra e o mesmo teto, lendo a **Eficiência da faixa de nível deles** (um Boss de faixa 17-20 lê Eficiência +8, teto 18). Os valores fechados por tipo e faixa estão na tabela de âncoras de 18.3, e a RD inimiga entra nas premissas publicadas do DPC (18.2) — ignorá-la inflaria o PV efetivo do inimigo em 10% a 20%.

*Reescalonamento obrigatório na escrita:* todo "10 RD" e "15 RD" da v0.1 vira **"RD igual à sua Eficiência"** ou um valor fixo de +2/+3, caso a caso. A Armadura Pesada passa de 10 RD para **2 RD**. A lista completa de conversões está em **11.4**.

### 6.5 Velocidade — a estatística nova (lacuna L02 / ponto 2)

A v0.1 fala de "casas", de "derrubar turno" e de "aumento na velocidade" sem ter uma estatística de Velocidade. Ela existe a partir da v1.0 e é a quinta estatística da ficha, ao lado de PV, Defesa, Esquiva e RD.

> **Velocidade (VEL) = 10 + Bônus de Agilidade + Bônus de Caminho + bônus de equipamento e efeitos**

| Caminho | Bônus de VEL | Leitura |
|---|---|---|
| A Caça | +4 | Age primeiro, quase sempre |
| A Euforia | +3 | Imprevisível e rápida |
| A Harmonia | +2 | Precisa agir antes para buffar |
| A Inexistência | +2 | Aplica debuff antes da porrada chegar |
| A Destruição | +1 | |
| A Erudição | +1 | |
| A Abundância | +1 | |
| A Recordação | +1 | |
| A Preservação | +0 | Age por último e aguenta |

Faixa esperada, calculada a partir da própria fórmula: **VEL 10 a 19** no nível 1; **12 a 21** no nível 10; **13 a 24** no nível 20 com equipamento. **Não existe ganho automático de VEL por nível** — o crescimento vem de Relíquias (Botas: +2/+3/+4/+5 por tier), Cone de Luz e Bênçãos.

Os extremos, para o Mestre saber com o que está lidando: o **piso absoluto é 7** (Agilidade 8, Caminho +0, Armadura Pesada −2 — uma Preservação de tanque puro) e o **teto absoluto é 25** (Agilidade 20, Caça +4, Botas IV +5, Armadura Leve +1). A VEL de inimigo por tipo e faixa está na tabela de âncoras de 18.3, e ela foi calibrada para que a Caça equipada **chegue à frente de todo Comum e Elite da faixa dela** — essa é a promessa do Caminho, e ela precisa ser verdadeira na mesa, não só na descrição.

*Por quê sem ganho automático:* se todos ganhassem VEL nos mesmos níveis, a ordem relativa do grupo nunca mudaria e a coluna seria decorativa. Jogando o crescimento no equipamento, a Velocidade se torna uma decisão de build ("abro mão de +1 Defesa por +2 de VEL?") e o Mestre tem uma alavanca clara para desenhar inimigos rápidos.

A Velocidade também resolve **perseguições e corridas fora de combate**: Teste oposto de `d20 + (VEL - 10)` contra `d20 + (VEL - 10)`, melhor de três trocas. O `-10` existe porque VEL é um valor absoluto (10 a 24), de uma ordem de grandeza diferente de qualquer outro modificador do livro; subtraindo a base de 10 ela volta para a escala dos outros bônus. **Nunca se rola Velocidade contra uma DT da tabela de dificuldades** (18.4) — a Velocidade só aparece em teste oposto.

---

## 7. Fila de Ação, Ciclo e Velocidade na prática (lacuna L01 / ponto 1)

Esta é a maior lacuna da v0.1 e o coração mecânico da v1.0. Capítulo dedicado: `19-fila-de-acao-e-velocidade.md`.

### 7.1 Decisão de arquitetura

Honkai: Star Rail usa um medidor de distância de ação (`10000 / VEL`) recalculado a cada ação. Isso é aritmética de fração contínua: inviável numa mesa com papel e lápis.

**Decisão: Fila de Ação com casas numeradas.** O Mestre desenha uma tira com uma casa por combatente e move fichas (moedas, dados, pedaços de papel com nomes). O estado do combate inteiro cabe numa linha.

Avaliei três alternativas antes de travar:

| Alternativa | Por que foi recusada |
|---|---|
| Iniciativa rolada (d20 + VEL) a cada Ciclo | Rerolar tudo a cada Ciclo apaga o efeito de Atrasar/Avançar: o castigo que você aplicou neste Ciclo evapora no próximo. Mata a mecânica que a v0.1 cita 15 vezes |
| Medidor de pontos de ação (estilo HSR simplificado, 100 ÷ VEL) | Exige divisão e rastrear frações por combatente. Em um combate com 4 PJs e 5 inimigos, viram 9 contas por Ciclo |
| **Fila de casas por VEL (escolhida)** | Zero aritmética durante o combate, estado visível, "Atrasar em N casas" e "Avançar em N casas" têm significado literal e imediato |

### 7.2 Definições oficiais

- **Fila de Ação:** a lista ordenada de todos os combatentes, uma **casa** por combatente, numerada de 1 a N.
- **Casa:** posição na Fila. Casa 1 age primeiro.
- **Turno:** a vez de um combatente. Ele usa as ações dele e a Fila avança.
- **Ciclo:** uma passagem completa pela Fila. Quando o último combatente age, o Ciclo termina e a Fila é **remontada**. Durações de combate se contam em Ciclos; durações de efeito em alvo único se contam em turnos do alvo.

### 7.3 Montagem da Fila

1. No início do combate, ordene todos os combatentes por **VEL, do maior para o menor**.
2. **Empates:** maior Bônus de Agilidade vence; se persistir, maior Bônus de Discernimento; se ainda persistir, os jogadores escolhem a ordem entre si e vêm antes dos NPCs empatados. Nada de rolar dado para desempatar — o empate é frequente e o dado tornaria a Fila imprevisível.
3. No início de cada Ciclo novo, **remonte a Fila com os valores de VEL atuais** (buffs e debuffs de Velocidade entram aqui) e aplique os **Atrasos pendentes** marcados no Ciclo anterior. **Não existe Avanço pendente** — Avançar só funciona em quem ainda não agiu, dentro do Ciclo (7.5).
4. **Sem iniciativa rolada.** Quem é rápido age antes, sempre. É a promessa do Caminho da Caça e do atributo Agilidade, e é o que faz a Velocidade valer dinheiro em Relíquia.

**Surpresa (o gatilho que faltava).** Quando um lado começa o combate sem ser notado, cada combatente do lado pego de surpresa faz um **Teste de Percepção Mental contra DT 13, fixa em todas as faixas**. Quem falha recebe a condição **Surpreso** e tem a casa **pulada no primeiro Ciclo**. Quem passa age normalmente.

- **Se houver um atacante declarado se aproximando às escondidas**, ele faz **um** Teste de Furtividade e o resultado dele **substitui a DT 13** para todo o lado emboscado. Um teste, não um por alvo — é o lado que se esconde que rola, e quem está sendo emboscado reage a esse número.
- **A DT 13 é fixa de propósito e é uma das cinco DTs de subsistema do livro** (4.2). Surpresa é surpresa em qualquer nível de jogo: indexá-la à faixa do grupo faria um PC de nível 20 sem Discernimento ser emboscado em 80% das cenas, perdendo o Ciclo inteiro justamente onde o Boss age duas vezes por turno. Isso contraria a regra de 18.4 de que **a faixa é do desafio, não do personagem**.

- O **Mestre declara** quando há surpresa, antes de montar a Fila. Não existe surpresa em combate já iniciado, e não existe "rodada de surpresa" separada.
- O traço **Raposa Astuta** dos Vulpes (12) é uma segunda chance contra exatamente esse teste.
- Grupo emboscando um inimigo funciona igual, com os papéis trocados.

### 7.4 Atrasar (o "derrubar o turno em N casas" da v0.1)

> **Atrasar em N casas:** mova a ficha do alvo N casas para o fim da Fila. Cada casa que ele desce é um combatente que age antes dele.

- Se o alvo **ainda não agiu** neste Ciclo, o efeito é imediato e visível.
- Se o alvo **já agiu** neste Ciclo, ou se não há casas suficientes atrás dele, o excedente fica marcado como **Atraso pendente** e é aplicado na remontagem do próximo Ciclo (ele começa N casas abaixo da posição que a VEL lhe daria).
**Teto de Atraso, por alvo, por Ciclo:**

| Tipo de alvo | Teto | Firmeza |
|---|---|---|
| Comum | **3 casas** | Não tem |
| Elite e Boss | **2 casas** | **Tem** |

**Firmeza (Elite e Boss) — ordem de operação fechada, nesta ordem e sem atalho:**

1. **Some todas as casas de Atraso** aplicadas ao alvo neste Ciclo, de todas as fontes.
2. **Divida o total por 2, arredondando para baixo.**
3. Se o resultado for 0 e houver pelo menos 1 casa bruta, o resultado é **1**. O mínimo de 1 casa vale para o **total do Ciclo**, nunca para cada fonte separadamente.
4. **Aplique o teto de 2 casas.** O excedente é perdido.

*Por quê a ordem importa tanto que virou lista numerada:* aplicar a Firmeza **por fonte** anula a Firmeza. Exemplo real do livro: Embaraço (5 acúmulos de 1 casa) + Aprisionamento (2 casas) = 7 casas brutas. Por fonte, cada acúmulo de 1 casa vira `floor(0,5) = 0`, o "mínimo 1" devolve 1, e os 5 acúmulos continuam valendo 5 — a Firmeza não fez nada. Pelo total: `floor(7 ÷ 2) = 3`, teto 2, **o Boss perde 2 casas**. Um caso pequeno, para mostrar que o mínimo funciona: 1 casa bruta (só a Quebra) → `floor(0,5) = 0` → mínimo → **1 casa**.

*Por quê teto e Firmeza existem:* sem eles, um grupo com Quântico e Imaginário tranca um Boss fora da Fila para sempre. Isso é "vencer sem lutar", o que é tecnicamente bom e dramaticamente péssimo — a mesa inteira olha o Mestre passar a vez. Com teto 2 e Firmeza pelo total, o grupo rouba **1 ou 2 casas** de um Boss por Ciclo: exatamente o que o texto promete, suficiente para sentir controle, insuficiente para apagar o vilão. Contra Comum, onde controle total é o ponto, o teto é 3 e não há Firmeza.

### 7.5 Avançar e Avanço Total

> **Avançar em N casas:** mova a ficha N casas para o início da Fila. Só funciona se o alvo ainda não agiu neste Ciclo.
> **Avanço Total:** o alvo age **imediatamente após o turno atual**, mesmo que já tenha agido neste Ciclo. No máximo **uma vez por Ciclo por criatura**.

O Avanço Total é o "ganhar um turno extra" de Honkai: Star Rail e é o efeito mais forte que uma Habilidade de Nível 5 ou uma Ultimate de suporte pode conceder. Tratá-lo como recurso raro e explicitamente limitado evita loops de dois jogadores se adiantando um ao outro.

### 7.6 Perder o turno (Congelamento)

A v0.1 diz que o Congelamento "faz com que o alvo perca seu turno neste Ciclo". Fechado:

- O alvo é **retirado da Fila neste Ciclo** (a ficha sai da tira, não age).
- Se o alvo **já agiu** quando o Congelamento é aplicado, ele perde o turno do **próximo** Ciclo; marque "Congelado" na ficha dele.
- Enquanto estiver Congelado, o alvo **não pode ser Atrasado** (não há turno para atrasar) e Atrasos pendentes contra ele são descartados.
- O Congelamento consome exatamente um turno e termina. Na remontagem seguinte, o alvo volta à posição normal de VEL.
- Um alvo não pode ser Congelado em dois Ciclos consecutivos pela mesma fonte.

**Firmeza contra Congelamento (Elite e Boss):**

> **Elite e Boss não perdem o turno por Congelamento.** Em vez disso, o Congelamento os **Atrasa em 2 casas** — que é o teto de Atraso de um Ciclo contra eles (7.4), e por isso nenhum outro Atraso aplicado no mesmo Ciclo soma com este — e eles **não podem usar ação especial no turno seguinte**. Só **Comuns** perdem o turno por Congelamento.

*Por quê:* a Firmeza de 7.4 protege Elite e Boss contra Atraso e **esquecia** de protegê-los contra perder o turno, o que era o furo maior dos dois. Com a cadência de Quebra publicada (uma Quebra a cada ~2 Ciclos contra Boss, 18.1), um único personagem de Gelo Congelaria o Boss a cada 2 Ciclos, e a trava de "não em Ciclos consecutivos" **permite** exatamente esse ritmo: num combate de 4 Ciclos o Boss perderia 2 dos 4 turnos, metade das 8 ações agressivas que a premissa de 18.1 lhe dá. É o mesmo cenário que o teto de Atraso existe para evitar, e agora os dois casos têm a mesma resposta. O Gelo não perdeu o papel: Atrasar 2 casas num Boss é o máximo que o sistema permite a qualquer fonte, e tirar a ação especial dele por um turno costuma valer mais que o dano.

### 7.7 Casos-limite da Fila (todos resolvidos no capítulo 19)

| Situação | Resolução |
|---|---|
| Combatente entra no meio do combate (invocação, reforço) | Entra pela VEL nas casas **restantes** do Ciclo. Se a VEL dele seria maior que a de quem está agindo, ele entra na casa imediatamente seguinte |
| Memoespírito | Tem **casa própria** na Fila, pela VEL dele, e **1 ação por turno** (ver 13.3) |
| Combatente morre ou foge | A casa é removida e o Ciclo continua. Atrasos pendentes dele são descartados |
| Combatente a 0 PV (Morrendo) | **Mantém a casa.** O turno dele é onde o Teste de Força de Vontade acontece |
| Surpresa | Quem falha no Teste de Percepção Mental de 7.3 fica **Surpreso** e tem a casa **pulada** no primeiro Ciclo. Não existe "rodada de surpresa" separada |
| Duas Ultimates declaradas juntas | Regra do autor mantida: quem falou primeiro resolve primeiro, e quem decide quem falou primeiro é o Mestre |
| Atrasar alguém que está na última casa | Vira Atraso pendente do próximo Ciclo (respeitando o teto de 3) |
| Avançar alguém que já agiu | Não acontece. Só Avanço Total faz isso |
| Efeito muda a VEL no meio do Ciclo | A posição atual **não** muda. A VEL nova entra na próxima remontagem |

### 7.8 Como isso fica no papel

```
CICLO 2
casa:   1      2       3       4        5       6
      [Caça] [Robin] [PJ-3] [Elite] [Comum] [Preserv.]
       VEL16  VEL14   VEL13   VEL12   VEL11    VEL10
                        ^ agindo agora
pendentes: Elite -1 casa (Quebra, Ciclo 3)   Comum: CONGELADO (Ciclo 3)
```

O Mestre precisa de uma tira de papel, uma ficha por combatente e duas anotações (pendentes e condições). Nada de calculadora. O apêndice traz a **Trilha de Ação** para imprimir.

### 7.9 Normalização das referências herdadas da v0.1

A v0.1 espalha "derrubar o turno", "+1 de distância" e variações em cerca de 15 lugares. Todas passam a usar a linguagem travada acima. Tabela de conversão obrigatória para a escrita:

| Onde (v0.1) | Texto original | Texto normalizado v1.0 |
|---|---|---|
| Elemento Quântico — Embaraço | "derruba o turno do alvo em 1 casa" | "**Atrasa** o alvo em **1 casa**" |
| Elemento Imaginário — Aprisionamento | "turno derrubado em 2 casas" | "**Atrasa** o alvo em **2 casas**" |
| Elemento Gelo — Congelamento | "perde seu turno neste Ciclo" | "o alvo fica **Congelado** (ver 7.6)" |
| Tenacidade — Quebra | "turno derrubado por 1 casa" | "**Atrasa** o alvo em **1 casa**" |
| Destruição — Instinto de Sobrevivência | "deslocamento aumenta em +1 Distância" | "+1 **Distância de Movimento**" |
| Destruição — Impacto Devastador | "mover-se metade da sua Distância total" | "mover-se **1 Distância**" |
| Inexistência — Marca do Vazio | "-1 de distância... não menos que Curta" | "o alvo recebe **Lentidão** (ver 9.6)" |
| Inexistência — Olhar da Ausência | "**Como ação bônus**" | "Como **Ação Complementar**" |
| Inexistência — Névoa da Inexistência | "Como ação comum" | "**No lugar do seu Ataque Básico**" |
| Harmonia — Melodia da União | "+1 distância de deslocamento" | "+1 **Distância de Movimento**" |
| Harmonia — Campo da Harmonia Universal | "Aumento na velocidade (+1 de distância)" | "+2 de **Velocidade**" (é buff de VEL, não de alcance) |
| Harmonia — Ritmo Acelerado | "ação adicional limitada" | "**Ação Extra**: um Ataque Básico, uma Habilidade de Nível 2 ou menor, ou uma Ação de Movimento" |
| Harmonia — Bênção da Harmonia | "(Reação)" | "**Reação**" (consome a Reação do turno) |
| Recordação — Memória Compartilhada | "+1 de distância" | "+1 **Distância de Movimento**" |
| Recordação — Recordação Absoluta | "+1 de distância" | "+1 **Distância de Movimento**" |
| Recordação — Avatar, Forma Manifestada | "+1 de distância e +2 dados" | "+1 **Distância de Movimento** e +2 dados base" |
| Recordação — Memória da Sabedoria | "enquanto estiver a 1 distância de você" | "enquanto estiver a até **Distância Curta** de você" |
| Abundância / Harmonia / Recordação | "ação comum" (6 ocorrências) | "**No lugar do seu Ataque Básico**" |
| Todos os Caminhos | "ação complementar" (minúsculas, grafia variável) | "**Ação Complementar**" |
| Destruição, Harmonia, Abundância, Recordação (4 Bênçãos) | "por 1 rodada" / "durante essa rodada" | "por **1 Ciclo**" |
| Todos os Caminhos | "turno" usado no sentido de rodada do grupo | "**Ciclo**" |
| Inexistência — Silêncio da Existência | "o alvo demorará mais um turno" | "o alvo fica **Silenciado** (9.6)" |
| Inexistência — Erosão Mental | "tem dificuldade para conjurar habilidades poderosas" | "o alvo fica **Silenciado** (9.6)" |
| Destruição — Aniquilador de Resistências | "o DT será o acerto do seu Ataque -8" | "**DT = 8 + Bônus do seu Atributo de Habilidade + Eficiência**" (a DT oficial de 4.2; não existe DT derivada de rolagem no livro) |

> **Nenhuma frase do livro descreve um subsistema que não existe.** "O alvo demorará mais um turno" é o arquétipo do defeito que afundou a v0.1: soa como regra, não é regra, e cada mesa resolve diferente. Toda vez que a escrita encontrar uma construção desse tipo numa Bênção herdada, ela tem duas saídas e só essas duas: traduzir para uma **condição do catálogo de 9.6** ou para um **número da régua de 11.4**.

---

## 8. Economia de ações, Pontos de Habilidade e Ultimate

### 8.1 As 4 Ações + 1 Reação (lacuna L18 / erro E09)

Os quatro tipos de ação da v0.1 ficam, com uma clarificação que resolve o buraco mais silencioso da v0.1: **em nenhum lugar ela diz qual ação uma Habilidade consome**.

| Ação | Quantas por turno | O que é |
|---|---|---|
| **Ataque Básico** | 1 | Qualquer ação agressiva que não seja Habilidade nem Ultimate |
| **Ação Complementar** | 1 | Pegar ou guardar um objeto, recarregar, beber poção, interagir, falar sob pressão |
| **Ativar Ultimate** | 1 por Ciclo | **Não consome o turno.** Declarável a qualquer momento (ver 8.3) |
| **Ação de Movimento** | 1 | 1 Distância |
| **Esforço Total** | — | Gaste o Ataque Básico **e** a Ação Complementar do turno para dobrar uma Ação de Movimento: **2 Distâncias** (3 com bônus) |
| **Reação** | 1, recarrega no início do seu turno | Esquiva, Intervir ou uma Reação de Bênção/Habilidade |

> **Toda criatura começa o combate com a Reação disponível**; dali em diante ela recarrega no início do turno dela. Sem essa linha, quem tem VEL baixa — a Preservação, com Bônus de VEL +0 e Reações defensivas no centro da identidade — passaria o primeiro Ciclo inteiro sem poder Esquivar nem Intervir, exatamente quando os inimigos rápidos atacam.

**Esforço Total** é o nome oficial do que a v0.1 chamava de "ação completa". Ele não é uma quinta ação: é uma troca declarada (abro mão de bater e de interagir para correr o dobro).

> **Usar uma Habilidade ocupa o espaço do seu Ataque Básico no turno**, a menos que o texto da Habilidade diga que ela é uma Ação Complementar ou uma Reação.

*Por quê assim:* preserva os 4 tipos de ação que o autor escreveu, impede o combo "Ataque Básico + Habilidade todo turno" (que dobraria o dano por turno e detonaria o orçamento de PV dos inimigos) e reproduz exatamente o loop de Honkai: Star Rail, onde você escolhe entre ataque básico e Habilidade.

**Reações padrão de todo personagem:** **Esquiva** (6.3) e **Intervir** (você se joga na frente de um aliado a até Distância Curta e recebe o dano no lugar dele; só contra um ataque de alvo único). Não existem ataques de oportunidade — eles obrigariam a rastrear posição exata, o que a escala de Distâncias abstratas não suporta.

### 8.2 Pontos de Habilidade (PH) — a reserva do grupo

**Decisão: criar os PH como reserva compartilhada do grupo.**

- O grupo tem uma reserva **comum**, dimensionada pelo **tamanho da mesa** e pela faixa de nível:

> **Máximo de PH = 1 + número de personagens jogadores**, +1 na faixa 10-15, +2 na faixa 16-20.
> **PH no início de cada combate = máximo - 2.**

| Nº de jogadores | Máximo 1-9 / 10-15 / 16-20 | Início 1-9 / 10-15 / 16-20 |
|---|---|---|
| 3 | 4 / 5 / 6 | 2 / 3 / 4 |
| **4 (mesa de referência)** | **5 / 6 / 7** | **3 / 4 / 5** |
| 5 | 6 / 7 / 8 | 4 / 5 / 6 |
| 6 | 7 / 8 / 9 | 5 / 6 / 7 |

*Por quê amarrar ao número de jogadores:* os PH são reserva coletiva, então uma mesa de 6 gera o dobro do que uma de 3 contra um teto fixo — com 6 o recurso deixa de ser decisão e com 3 o grupo nunca paga uma Habilidade de topo. A fórmula reproduz **exatamente** os números da mesa de 4 (5/6/7 e 3/4/5), que é a mesa que o passe de balanceamento usa em 18.

- **Geração:** cada **Ataque Básico que acerta** gera **+1 PH** (faixas 1-9) ou **+2 PH** (faixas 10-20). Ataque Básico que erra não gera PH (4.5).
- **Usar uma Habilidade custa PH** conforme o Nível dela: Nível 1-2 = **1 PH**; Nível 3 = **2**; Nível 4 = **3**; Nível 5 = **4**; Nível 6 = **5**; Nível 7 = **6**.
- Sem PH suficiente, a Habilidade **não pode ser declarada**: nada é rolado e o jogador escolhe outra ação. **Não existe PH negativo, PH devido nem PH emprestado.** O custo é pago na declaração: se o ataque erra depois de declarado, o PH já foi.
- A **Ultimate não custa nem gera PH**. Habilidades **Passivas** não custam PH.
- Invocar o Memoespírito custa **1 PH**.
- **Recarga:** o PH volta ao valor inicial **no começo de cada combate**. Não existe PH fora de combate, e nenhum descanso devolve PH (15.2).

**Quanto isso sustenta de verdade** (é esta tabela, e não um palpite, que alimenta o DPC de 18.2 — mesa de 4, combate de 4 Ciclos, 2 Ataques Básicos por Ciclo, 60% de acerto):

| Faixa | Geração por Ciclo | Orçamento do combate (início + 4 Ciclos) | O que ele compra em 4 Ciclos | Habilidade por Ciclo |
|---|---|---|---|---|
| 1-4 | 1,2 | 3 + 4,8 = **7,8 PH** | 4 Habilidades de Nível 2 (4 PH) — sobra folga | **1 × Nível 2** |
| 5-8 | 1,2 | 3 + 4,8 = **7,8 PH** | 3 de Nível 3 + 1 de Nível 2 (7 PH) | **0,75 × Nível 3 + 0,25 × Nível 2** |
| 9-12 | 2,4 | 4 + 9,6 = **13,6 PH** | 4 de Nível 4 (12 PH) | **1 × Nível 4** |
| 13-16 | 2,4 | 4 + 9,6 = **13,6 PH** | 2 de Nível 6 + 1 de Nível 3 (12 PH) | **0,5 × Nível 6 + 0,25 × Nível 3** |
| 17-20 | 2,4 | 5 + 9,6 = **14,6 PH** | 2 de Nível 7 + 1 de Nível 3 (14 PH) | **0,5 × Nível 7 + 0,25 × Nível 3** |

O recado que essa tabela dá para a mesa, e que o livro precisa dizer em voz alta: **a Habilidade de topo não é a ação de todo turno.** Nas faixas altas ela sai uma vez a cada dois Ciclos, e é o Ataque Básico de alguém que paga por ela.

*Por quê criar um recurso novo:* sem ele, a conta não fecha. Uma Habilidade Nível 5 causa ~105 de dano médio e a Nível 7 causa ~189; quatro jogadores de nível 20 usando a melhor Habilidade todo turno entregariam ~525 de dano efetivo por Ciclo em vez dos 275 orçados (18.2), e qualquer Boss morreria no Ciclo 2 ou precisaria de mais de 2000 PV — o que o obrigaria a bater proporcionalmente mais forte e a aniquilar o grupo. Os PH resolvem isso sem nerfar as tabelas de Habilidade que são DNA do sistema: você **pode** usar o Nível 7, mas gastou 6 dos 7 PH do grupo, e alguém vai ter que dar Ataques Básicos para repor.

*Por quê a geração sobe para +2 no nível 10:* com Habilidades de Nível 6 e 7 custando 5 e 6 PH, uma geração de +1 por Ataque Básico faria o grupo passar dois Ciclos inteiros batendo de leve para pagar uma Habilidade. Com +2, o grupo sustenta **uma Habilidade de topo a cada dois Ciclos** e uma Habilidade intermediária nos Ciclos do meio — o ritmo que o passe de balanceamento assume em 18.2, com a conta aberta na tabela acima.

É também a mecânica mais reconhecível de Honkai: Star Rail depois da Ultimate, e cria a conversa de mesa que o jogo de origem tem ("não gasta tudo, deixa 1 para a cura").

*Alternativa recusada:* usos por combate por Habilidade ("Nível 4 = 1 vez por combate"). Funciona, mas é bookkeeping individual (10 Habilidades × 4 jogadores = 40 contadores) e não gera decisão coletiva.

### 8.3 Ultimate e Energia (lacuna L13 / ponto 13 / erro E19)

Mantido da v0.1: **toda Ultimate ativa com 100 de Energia**, declarada em voz alta pelo nome, **sem gastar ação**, em qualquer momento. Acrescentado:

- **Uma Ultimate por Ciclo por personagem**, declarável no início ou no fim de qualquer turno (seu ou de outro), nunca no meio da resolução de um efeito.
- A Energia **persiste entre combates**. Não zera em descanso.
- Energia acima de 100 é perdida (regra do autor mantida) — e como a Ultimate não gasta ação, é sempre possível ultar antes de transbordar.

**Fontes de Energia (tabela fechada):**

| Fonte | Energia | Limite |
|---|---|---|
| Ataque Básico que acerta | +20 | — |
| Habilidade (acerte ou não) | +30 | — |
| **Sofrer dano** | **+10** | 1 vez por Ciclo |
| **Derrotar um inimigo** | **+10** | quem desferiu o golpe |
| **Quebrar a Tenacidade de um inimigo** | **+10** | 1 vez por Ciclo |
| Ativar a Ultimate | -100 | — |
| Ação do Memoespírito | metade do valor | arredonda para baixo |

*Por quê adicionar "sofrer dano" e "derrotar inimigo":* sem elas, só quem ataca carrega Ultimate, e os Caminhos defensivos (Preservação, Abundância) ultam a cada 5-6 turnos enquanto a Destruição ulta a cada 3. "Sofrer dano" é a fonte canônica de Energia do tanque em Honkai: Star Rail e conserta exatamente esse desequilíbrio. O limite de 1 por Ciclo evita que um inimigo de ataques múltiplos encha a barra do grupo inteiro.

Com essa tabela, a renda fica em **25-35 de Energia por turno**, ou seja, uma Ultimate a cada **3 ou 4 turnos** por personagem. É o ritmo que o passe de balanceamento assume.

### 8.4 Distâncias

Escala da v0.1 mantida: **Pessoal, Curta, Média, Longa, Extrema**. Uma Ação de Movimento sobe ou desce **um passo** na escala; com **Esforço Total** (8.1), dois passos; o máximo por turno com todos os bônus é **três passos**. Distância Pessoal é corpo a corpo. Alcance de Habilidade por Nível segue a tabela da v0.1 (cumulativa), intocada.

### 8.5 Potência da Ultimate

A v0.1 diz que a Ultimate "nos níveis iniciais será fraca" e que o jogador pode "mantê-la visualmente e só aumentar seu efeito ao passar de nível", mas nunca dá um número. Sem número, o Mestre não tem como aprovar a criação de ninguém e o passe de balanceamento não fecha — a Ultimate é a única ação do jogo que **não gasta ação** e dispara a cada 3 ou 4 turnos.

**Decisão: a Ultimate não tem Nível próprio. Ela tem um Nível equivalente por faixa, e lê as linhas de 10.1 e 10.2 nesse Nível.**

| Faixa de nível | Nível equivalente | Dano | Média | Cura | Média | Redução de Tenacidade |
|---|---|---|---|---|---|---|
| 1-4 | **2** | 5d10 | **27** | 6d10 | **33** | 5 |
| 5-8 | **3** | 6d12 | **39** | 8d12 | **52** | 5 |
| 9-12 | **4** | 6d20 | **63** | 7d20 | **73** | 5 |
| 13-16 | **5** | 10d20 | **105** | 10d20 | **105** | 5 |
| 17-20 | **6** | 14d20 | **147** | 14d20 | **147** | 5 |

- **Dano ou cura = dados da tabela + Bônus do Atributo de Habilidade** (uma vez, não por dado), igual às Habilidades.
- **Em área:** metade dos dados (arredonda para baixo, mínimo 1 dado) e **até 3 alvos** — **4 alvos** quando o Nível equivalente da sua faixa for 6, ou seja a partir do nível 17. É a mesma regra de 10.1, lida no Nível equivalente.
- Uma Ultimate que ataca exige **Teste de Ataque ou Teste de Resistência do alvo**, nunca os dois (4.5).
- **Efeitos de buff, debuff e controle:** leia a linha do **Nível equivalente** na tabela de 10.2. No nível 20, isso significa teto de **+4/-4 e um efeito maior** — e não os +5/-5 e dois efeitos maiores de uma Habilidade de Nível 7.
- A Ultimate é **criada e validada pelo mesmo checklist de 10.4**, usando o Nível equivalente da faixa no campo "Nível da Habilidade". Vale a mesma lista de efeitos proibidos.
- **Não custa nem gera PH** (8.2), não gasta ação, **1 por Ciclo por personagem** (8.3), custa 100 de Energia.
- **Ao mudar de faixa, a Ultimate sobe sozinha.** O jogador não reescreve nada: os dados e o teto de efeito passam a ser os da faixa nova. Se ele quiser mudar a descrição ou o efeito, faz isso no próximo Descanso Longo, com a aprovação do Mestre.

*Por quê um Nível abaixo do topo da faixa:* nas faixas altas a Ultimate fica **um Nível equivalente abaixo** da melhor Habilidade disponível (147 contra 189 na faixa 17-20) porque ela é a única ação grande que sai **de graça** — sem PH e sem ocupar o turno. Se empatasse com a Habilidade de topo, o jogador racional pararia de gastar PH e a economia que sustenta o balanceamento (8.2) viraria decoração. Nas faixas baixas elas empatam de propósito: no nível 3, a Ultimate **é** o grande momento do personagem, e é isso que a v0.1 promete ao mandar declarar o nome em voz alta.

*Por quê Redução de Tenacidade 5 em todas as faixas:* é o único número da Ultimate que não escala, e é deliberado. No nível 3, 5 de Redução contra um Comum de Tenacidade 4 significa **Quebra garantida** — a Ultimate é a ferramenta de Quebra do grupo desde o começo. Nas faixas altas, 5 é a mesma contribuição de uma Habilidade de Nível 5, e a Quebra continua acontecendo a cada ~2 Ciclos (18.2).

---

## 9. Dano, Elementos, Tenacidade e Quebra

### 9.1 Os 3 tipos de dano e o Elemento do personagem

Os três tipos da v0.1 ficam, e passam a ser **categorias de escalonamento** (é por eles que Relíquias e Bênçãos dizem o que aumentam): **Dano de Ataque Básico**, **Dano de Habilidade**, **Dano de Ultimate**.

Cada personagem escolhe **1 Elemento** na criação, ligado ao Caminho e ao conceito. Suas Habilidades e sua Ultimate causam dano desse Elemento. Armas sem Elemento próprio causam dano **Físico**. Os 7 Elementos da v0.1 ficam idênticos: Físico, Fogo, Gelo, Raio, Vento, Quântico, Imaginário.

### 9.2 Dano de Ataque Básico e dados por categoria de arma

| Categoria | Dados base | Alcance | Atributo |
|---|---|---|---|
| Leve | 1d8 | Pessoal | Agilidade |
| Média | 1d10 | Pessoal | Poder ou Agilidade (fixo na criação) |
| Pesada (2 mãos) | 1d12 | Pessoal | Poder |
| Disparo curto | 1d8 | Média | Agilidade |
| Disparo longo (2 mãos) | 1d10 | Longa | Agilidade |
| Energia (2 mãos) | 2d8 | Longa | Sincronia |

> **Dano = dados base + Bônus do Atributo de Ataque** (uma vez, não por dado).
> Você ganha **+1 dado base** nos Ataques Básicos nos níveis **5, 9, 13 e 17**.

**Como ler a coluna "Dados de Ataque Básico" da tabela mestra (17):** ela conta **quantos dados a sua arma rola**, partindo de 1 — ou seja, quantos degraus você já ganhou. Uma arma de 1 dado chega a **5 dados** no nível 17 (5d10 numa arma Média). Uma arma de **Energia**, que já começa com 2 dados, chega a **6** (6d8). Esse +1 dado inicial é o traço que distingue a categoria Energia, e ele sobrevive à progressão. O orçamento de 18.2 usa a arma **Média** (1d10 → 5d10) como referência.

*Por quê dar dados ao Ataque Básico:* o Ataque Básico é o motor dos PH. Se ele não escalar, no nível 15 ninguém vai querer gerar PH, e a economia que sustenta o balanceamento morre. Com 5 dados no nível 17, um básico de arma média faz ~33 — não compete com uma Habilidade de Nível 7, mas é uma ação que vale o turno.

### 9.3 Fraquezas e Resistências

Regra da v0.1 mantida ao pé da letra, incluindo a quantidade de Fraquezas por tipo de inimigo (Comum 1-2, Elite 3, Boss 4):

- Ataque do Elemento da **Fraqueza** do alvo: **+2 dados** do mesmo tipo do ataque. Esses dados **não critam** (regra do autor).
- Elemento neutro: dano normal.
- Elemento ao qual o alvo tem **Resistência**: **-2 dados**, conservando sempre **no mínimo 1 dado** e causando no mínimo 1 de dano.
- **Descobrir Fraquezas** é uma ação de jogo: **Teste de Pesquisa, Ciência ou Sintonia** como **Ação Complementar**, contra a DT da faixa do inimigo. Sucesso revela **uma** Fraqueza à escolha do Mestre; cada tentativa seguinte contra o mesmo inimigo revela outra.

| Faixa de nível do inimigo | 1-4 | 5-8 | 9-12 | 13-16 | 17-20 |
|---|---|---|---|---|---|
| **DT para descobrir uma Fraqueza** | 13 | 14 | 15 | 16 | 17 |

> **Esta é uma das cinco DTs de subsistema do livro** (4.2) e ela **vence** a tabela geral de 18.4. Ela cresce muito mais devagar do que a DT Média da faixa (que vai a 25 na faixa 17-20) porque descobrir Fraqueza é uma **ação de rotina de combate** que o grupo precisa conseguir fazer, não um feito heroico: com DT 25 o subsistema de Fraqueza morreria justamente na faixa onde ele vale mais.

  Inimigo de nível misto usa a faixa do **mais forte** do grupo dele. O **Intellitron** faz esse teste com **Vantagem** e, em sucesso, descobre **duas** Fraquezas em vez de uma — é assim que o traço racial da v0.1 continua sendo vantagem depois de a regra geral existir (12).

### 9.4 Tenacidade e Quebra (lacuna L11 / ponto 11 / erros E10, E12)

> **Só inimigos têm Tenacidade.** Personagens jogadores e o Memoespírito **não** têm barra de Tenacidade, não podem ser Quebrados e nunca recebem a condição **Quebrado**. A ficha do personagem tem PV, Defesa, Esquiva, RD e Velocidade (6.5) — e nada mais. Nenhuma Bênção, Habilidade, Ultimate, Cone de Luz ou conjunto de Relíquias pode disparar "quando um aliado é Quebrado", porque isso não existe.

**O problema:** a v0.1 diz "Você não pode reduzir a Tenacidade de um Inimigo que não possua Fraqueza ao seu elemento". Numa mesa de 4 jogadores com 4 Elementos fixos contra um Comum com 1 Fraqueza, três jogadores ficam estruturalmente fora do sistema de Quebra — e Quebra é metade da graça do combate.

**Decisão: redução em três níveis, em vez de tudo-ou-nada.**

| Situação do seu Elemento contra o alvo | Redução de Tenacidade |
|---|---|
| É **Fraqueza** do alvo | Redução **total** |
| **Neutro** | **Metade** (arredonda para baixo, mínimo 1) |
| O alvo tem **Resistência** | **1 ponto**, fixo |

Mais duas mitigações:

- **Implante de Fraqueza:** uma Habilidade de Nível 4+ (10.2) e a Bênção **Implante de Fraqueza** — que é **uma das 2 Bênçãos novas da Inexistência, tier nível 9+** (11.3), e não a reinterpretação de nenhuma Bênção herdada — podem **adicionar** uma Fraqueza temporária a um inimigo (1 Ciclo). É o papel clássico de quebrador de defesas em Honkai: Star Rail e dá ao grupo uma resposta ativa contra inimigos de Elemento inconveniente.
- **Fraqueza revelada:** o Mestre informa as Fraquezas assim que o grupo passa um teste de identificação (9.3) ou após o primeiro Ciclo de combate. Esconder Fraquezas o combate inteiro converte o sistema em adivinhação.

**Valores de Redução de Tenacidade:**

| Fonte | Redução |
|---|---|
| Ataque Básico | 1 |
| Habilidade Nível 1-2 | 2 |
| Habilidade Nível 3 | 3 |
| Habilidade Nível 4 | 4 |
| Habilidade Nível 5 | 5 |
| Habilidade Nível 6 | 6 |
| Habilidade Nível 7 | 7 |
| Ultimate | 5 |
| Dano Contínuo | **0** (a regra do autor fica: só ataque reduz Tenacidade) |

**Quando a Tenacidade chega a 0, o alvo sofre Quebra:**

1. Sofre **Dano de Quebra** do Elemento que causou a Quebra.
2. É **Atrasado em 1 casa**. Contra Elite e Boss, essa casa entra no somatório de Firmeza do Ciclo (7.4): sozinha ela ainda vale 1 casa pelo mínimo, mas somada a outras fontes ela é dividida junto.
3. Recebe a condição **Quebrado** até o fim do próximo turno dele: **-2 de Defesa** e recebe **+1 dado** de dano de qualquer fonte.
4. Quem quebrou ganha **+10 de Energia** (1 vez por Ciclo).
5. A Tenacidade **volta ao máximo no fim do próximo turno do alvo**, junto com o fim da condição Quebrado.

**Dano de Quebra reescalonado** (erro E10 — a v0.1 tinha 6d4 para Físico e 1d2 para Gelo, uma diferença de 12x que ficava absurda em qualquer nível):

| Elemento | Dano de Quebra | Efeito de Quebra |
|---|---|---|
| Físico | 2d6 + (2 × Eficiência) | Sangramento |
| Fogo | 2d6 + (2 × Eficiência) | Queimadura |
| Raio | 1d6 + Eficiência | Choque |
| Vento | 1d6 + Eficiência | Cisalhamento de Vento |
| Gelo | Eficiência | **Congelamento** |
| Quântico | Eficiência | Embaraço |
| Imaginário | Eficiência | Aprisionamento |

A hierarquia que o autor escreveu está preservada ("sendo Físico e Fogo os maiores causadores de Dano de Quebra"), e Gelo/Quântico/Imaginário continuam pagando em dano porque pagam em **controle** — e controle, com a Fila de Ação definida, agora vale muito mais do que valia na v0.1.

### 9.5 Dano Contínuo (lacuna L19)

A v0.1 chama isso de "DoT" e espalha nas Bênçãos da Inexistência e nos efeitos de Quebra. Nome oficial: **Dano Contínuo (DC)**.

- Aplica no **início do turno do alvo**.
- **Não crita**, **não recebe dados de Fraqueza** e **ignora RD**.
- Múltiplos Danos Contínuos de Elementos diferentes coexistem. Do mesmo Elemento, acumulam até o limite daquele efeito.
- Duração contada em **turnos do alvo**.

*Por quê ignorar RD:* o Dano Contínuo é a identidade mecânica do Caminho da Inexistência. Com RD de 6 a 18 pelo jogo e tiques de 1d6 a 2d6+8, a RD anularia o Caminho inteiro. Em troca, o Dano Contínuo não crita e não ganha dados de Fraqueza — ele é confiável, não explosivo.

### 9.6 Catálogo de condições (lacuna L19)

Capítulo dedicado: `21-condicoes.md`. Toda condição tem: nome, efeito mecânico exato, duração e como termina. Os sete efeitos de Quebra da v0.1 são preservados com os números reescalonados.

| Condição | Efeito | Duração |
|---|---|---|
| **Sangramento** (Físico) | Dano Contínuo = 5% dos PV máximos do alvo por turno, até o teto de 3 × Eficiência | 2 turnos |
| **Queimadura** (Fogo) | Dano Contínuo de 2d6 + Eficiência (Fogo) | 2 turnos |
| **Choque** (Raio) | Dano Contínuo de 1d6 + Eficiência (Raio) | 2 turnos |
| **Cisalhamento de Vento** (Vento) | Dano Contínuo de 1d6 por acúmulo, até 5 acúmulos | 2 turnos |
| **Embaraço** (Quântico) | 1d6 por acúmulo (até 5, só por ataques, antes do próximo turno do alvo) e **Atrasa 1 casa** | 1 turno |
| **Aprisionamento** (Imaginário) | 1d6 + Eficiência e **Atrasa 2 casas** | 1 turno |
| **Congelado** (Gelo) | **Comum:** perde o turno (7.6), não pode ser Atrasado. **Elite e Boss (Firmeza):** não perdem o turno — são Atrasados em 2 casas e perdem a ação especial do turno seguinte. Não repetível pela mesma fonte em Ciclos seguidos | 1 turno |
| **Quebrado** *(só inimigos)* | -2 de Defesa, recebe +1 dado de dano de qualquer fonte | até o fim do próximo turno |
| **Lentidão** | -1 Distância por Ação de Movimento (sempre consegue mover ao menos até Pessoal/Curta gastando o turno) | definida pela fonte |
| **Marcado** | O que a fonte disser; acumula até 3 vezes | definida pela fonte |
| **Corrupção** | Acúmulo da Inexistência: +1 no dano de cada Dano Contínuo seu no alvo, até 5 | até o fim do combate |
| **Silenciado** | Não pode usar Habilidades de Nível 4 ou maior | 1 turno |
| **Vulnerável** | Recebe +1 dado de dano da fonte indicada | definida pela fonte |
| **Surpreso** | Casa pulada no primeiro Ciclo | 1 Ciclo |
| **Morrendo** | 0 PV, inconsciente, mantém a casa na Fila, faz Teste de Força de Vontade no turno (ver 15) | até estabilizar ou morrer |

**Regra de acúmulo global:** nenhum alvo acumula mais de **5** instâncias de uma mesma condição.

**Dois tetos independentes, não um saldo.** Esta é a parte que a mesa erra se o livro não disser com todas as letras:

> **Teto de bônus somado:** em uma mesma rolagem, a soma dos **bônus numéricos temporários** que um alvo recebe não passa de **+3** (níveis 1-9), **+4** (10-15) ou **+5** (16-20).
> **Teto de penalidade somada:** em uma mesma rolagem, a soma das **penalidades numéricas temporárias** que um alvo sofre não passa de **-3**, **-4** ou **-5** nas mesmas faixas.
> **Os dois são somatórios separados e não se cancelam para efeito de teto.** Um alvo com +3 de buff e -4 de penalidade **soma -1 na rolagem**, e nenhum dos dois tetos foi excedido.

| Entra nos tetos (é temporário) | Fica fora (é permanente e já está no orçamento de 18.2) |
|---|---|
| Bênçãos | Bônus de Atributo |
| Habilidades (buff e debuff de 10.2) | Eficiência e Eficácia |
| Ultimates | **Especialização de Combate** |
| Efeitos de conjunto de Relíquia (2 e 4 peças) | **Bônus Maior de Cone de Luz** (16.3) |
| Efeitos Condicionais de Cone de Luz | **Bônus de slot de Relíquia** (16.4) |
| Marcas e acúmulos | Bônus de Armadura ou Vestimenta |
| Penalidades aplicadas por inimigos e por jogadores | Penalidade fixa de Armadura Pesada (16.1) |

*Por quê dois tetos e não um saldo único:* num saldo único, bônus e penalidade se cancelariam **antes** do teto ser testado, e nenhum alvo nunca encostaria nele — um PC com +3 de buff e -2 de debuff estaria em +1 e teria espaço para mais +2 de buff. O teto viraria letra morta exatamente na situação para a qual ele foi escrito. Do lado do inimigo a pergunta importa ainda mais, porque **o Caminho da Inexistência é feito de acumular penalidade**: com um teto próprio de -5 na faixa alta, o jogador da Inexistência sabe quando parou de valer a pena empilhar debuff do mesmo tipo e começa a diversificar — que é como o Caminho deve ser jogado. Uma Habilidade de Nível 7 dá **-5 sozinha** (10.2): ela consome o teto inteiro da faixa alta, de propósito, e é por isso que ela é Nível 7.

*Por quê a penalidade de Armadura Pesada fica fora:* é escolha permanente de equipamento feita pelo jogador, igual ao bônus de Defesa que vem com ela, e já está dentro do orçamento de Defesa de 18.2.

Os dois tetos são invariantes do sistema, e o dono deles é o capítulo 26 (ver 19).

---

## 10. Habilidades criadas pelo jogador

Capítulo dedicado: `16-habilidades.md`. A v0.1 entrega o melhor da sua identidade aqui: o jogador escreve as próprias Habilidades com apoio de tabelas-guia. Isso fica, com números corrigidos e com os níveis novos que a faixa 1-20 exige.

### 10.1 Níveis de Habilidade 1-7 (override: expansão)

**Decisão: expandir de 1-5 para 1-7.**

*Por quê 7 e não 10:* a cada nível de Habilidade o dano cresce ~40%. Indo até 10, a Habilidade de topo passaria de 500 de dano médio e exigiria Bosses com milhares de PV — o que transforma cada combate num banco de dados. Com 7 níveis, o topo fica em 189, o Boss de fim de campanha fica em **935 PV** (18.3) e o combate termina em ~3,7 Ciclos. Expandir para 7 também **preserva as 5 linhas originais do autor intactas**: as duas linhas novas são adição, não revisão.

*Alternativa recusada:* reespaçar 1-5 pelos 20 níveis (Nível 5 chegando só no 18). Recusada porque congela a fantasia do jogador: um personagem de nível 14 ainda estaria usando a mesma Habilidade de Nível 4 que tinha no nível 9, com o mesmo dado e o mesmo texto.

**Tabela de Dano, Cura e custo em PH:**

| Nível da Habilidade | Dano | Média | Cura | Média | Custo | Redução de Tenacidade | Alcance cumulativo |
|---|---|---|---|---|---|---|---|
| 1 | 6d6 | **21** | 5d8 | **22** | 1 PH | 2 | Pessoal, Curta |
| 2 | 5d10 | **27** | 6d10 | **33** | 1 PH | 2 | + Média |
| 3 | 6d12 | **39** | 8d12 | **52** | 2 PH | 3 | + Longa |
| 4 | 6d20 | **63** | 7d20 | **73** | 3 PH | 4 | + Extrema |
| 5 | 10d20 | **105** | 10d20 | **105** | 4 PH | 5 | Extrema |
| **6** | **14d20** | **147** | **14d20** | **147** | 5 PH | 6 | Extrema |
| **7** | **18d20** | **189** | **18d20** | **189** | 6 PH | 7 | Extrema |

- **Dano/cura = dados da tabela + Bônus do Atributo de Habilidade** (uma vez, não por dado).

**Habilidade em área — regra travada (a escala de alvos que faltava):**

> **Área:** metade dos dados (arredonda para baixo, **mínimo 1 dado**) e **até 3 alvos** à sua escolha, todos dentro do alcance da Habilidade e a **até uma Distância um do outro**. Habilidades de **Nível 6 e 7** atingem **até 4 alvos**. Alvos além disso só com recurso de Caminho (Acúmulos de Cálculo da Erudição, 11.2) ou texto específico de Bênção, e **nunca mais de 6**. O custo em PH é o mesmo da versão de alvo único.

- O **Bônus do Atributo de Habilidade soma uma vez por alvo**, como em qualquer rolagem de dano.
- A **RD se aplica uma vez por alvo** (6.4), e os **dados de Fraqueza são calculados por alvo** — um alvo fraco ao seu Elemento recebe +2 dados, o vizinho neutro não.
- **Cura em área** segue a mesma contagem de alvos. A "cura em todos os aliados" da Habilidade de Nível 5 (abaixo) é a exceção declarada, porque uma mesa tem no máximo 6 personagens.
- O alcance é o do Nível (coluna "Alcance cumulativo"); a **área não estende o alcance**, ela só espalha o dano dentro dele.

*Por quê 3 alvos (4 nos Níveis 6 e 7) e por quê um teto absoluto de 6:* sem número de alvos, "metade dos dados" é o contrário de um limite. Uma Habilidade de Nível 7 em área rola 9d20 ≈ 94, e com atributo e Esfera Planar isso é **107 por alvo** na faixa 17-20. Contra os 7 Comuns de um encontro daquela faixa (1.085 PV no total) seriam **749 de dano numa ação só** — 2,8 vezes o DPC inteiro do grupo, e o encontro acabaria antes do segundo turno de alguém. Com **4 alvos** (que é o que o Nível 7 permite), ela entrega **428**; com 3, **321**. Comparando com os **219** que a mesma Habilidade faz concentrada num Elite (18.2), a versão em área vale cerca de **1,5 ×** o alvo único — forte, decisiva contra um pelotão, e **não** um apagador de encontros. É exatamente a razão de 1,5 que a premissa de Área usa em 18.1.

O degrau para 4 alvos nos Níveis 6 e 7 existe para a Habilidade de topo **parecer** de topo também em área. O teto de 6 existe porque 6 é o tamanho máximo de um grupo e de um pelotão desenhável na escala abstrata de Distâncias — e porque acima disso o Mestre para de conseguir narrar quem estava junto de quem.

*Por quê "a até uma Distância um do outro" e não um raio em metros:* a escala de 8.4 é de **alcance**, não de geometria — não existe grade, não existe medida. "Os alvos estão juntos" é uma pergunta que o Mestre responde olhando a cena, e é a única forma de área compatível com um sistema sem posicionamento exato (24). Em caso de dúvida, o Mestre diz quantos dos alvos escolhidos estão agrupados o suficiente, e esse número vale.
- **Médias corrigidas** (erro E06): a v0.1 listava 18, 25, 36, 60 e 100, calculados como `dados × valor médio truncado`. As médias reais são 21, 27,5, 39, 63 e 105, e **toda média impressa no livro é `floor(dados × média do dado)`** — a mesma regra de arredondamento para baixo da seção 3, sem exceção. É por isso que 5d10 aparece como **27** (e não 28), 5d8 como **22** e 7d20 como **73**. Os valores do autor subestimavam o dano em até 17%, o que contaminaria todo o orçamento de PV; arredondar para cima contaminaria o script `checar-tabelas.ps1` (23), que compara contra `floor`.
- **Cura de Nível 5 (erro E07):** a v0.1 dizia "Cura toda a Vida". Vira **10d20** (ou **5d20 em todos os aliados**). Cura total é incontrolável em qualquer orçamento: com ela, PV deixa de ser recurso.
- **Mesa rápida (variante oficial):** em vez de rolar 18d20, use a média impressa. Recomendado para Habilidades de Nível 5 ou maior.

### 10.2 Buff, Debuff e Passivas (a v0.1 deixava em aberto)

A v0.1 diz "O jogador fará juntamente do mestre podendo usar a criação dele como exemplo". Isso não é tabela-guia, é promissória. Fechado:

| Nível | Buff / Debuff permitido | Duração | Alvos |
|---|---|---|---|
| 1 | +1 ou -1 em **um** tipo de rolagem, **ou** PV temporários = **1 × Eficiência** | 1 turno | 1 |
| 2 | +1/-1 e um efeito menor, **ou** +2/-2 em um tipo | 2 turnos | 1 |
| 3 | +2/-2, **ou** +1/-1 em dois tipos; PV temporários = **2 × Eficiência**; aplica 1 condição da lista | 2 turnos | 2 |
| 4 | +3/-3; aplica ou remove 1 condição; PV temporários = **3 × Eficiência**; **Implante de Fraqueza** | 2 turnos | 3 ou área |
| 5 | +3/-3 e um efeito maior (ex.: **Avanço Total**, imunidade a 1 condição) | 3 turnos | grupo |
| 6 | +4/-4 e um efeito maior | 3 turnos | grupo |
| 7 | +5/-5 e dois efeitos maiores | 3 turnos | grupo |

| Nível | Passiva permitida |
|---|---|
| 1 | +1 fixo pequeno, ou um gatilho de +1 dado do seu Elemento 1 vez por turno |
| 2 | +1 fixo e uma condição de gatilho (ex.: "quando você Quebra um inimigo") |
| 3 | +2 fixo, ou 1 RD, ou +1 de Velocidade |
| 4 | +2 e um gatilho que concede dado extra; ou 2 RD |
| 5 | Um gatilho forte 1 vez por combate (ex.: "ao cair a 0 PV, fique com 1 PV") |
| 6 | +3 fixo e um gatilho forte |
| 7 | Um gatilho que altera uma regra sua (ex.: "seus Ataques Básicos reduzem 2 de Tenacidade em vez de 1"; "sua Habilidade em área atinge 1 alvo adicional") 1 vez por Ciclo. **Nunca** uma regra da lista de proibidos de 10.4 |

Buffs e debuffs respeitam o **teto global de bônus somado** (9.6) e o **teto global de PV temporários** (15.3: `3 × Eficiência`, de qualquer fonte, sem acumular entre fontes). Nenhuma Habilidade concede Vantagem permanente, Avanço Total mais de uma vez por Ciclo, nem imunidade a dano.

*Por quê PV temporários em múltiplos de Eficiência e não em valor fixo:* valor fixo obriga a escolher entre ser inútil no fim da campanha (10 PV contra 260 de PV máximo) ou quebrado no começo (40 PV contra 46). Em múltiplos de Eficiência, a mitigação vale 2 a 8 PV no nível 1-3 e 8 a 24 no nível 19-20 — e as três seções que falam de PV temporário (10.2, 11.4 e 15.3) passam a dizer a mesma coisa, com o mesmo teto.

### 10.3 Quantas Habilidades você tem (override: teto)

A v0.1 diz "o número de habilidades que você pode ter por nível é igual ao seu nível". No nível 20 isso dá 20 Habilidades escritas pelo jogador — uma ficha que ninguém lê e um combate em que ninguém decide.

**Decisão: teto de 8 Habilidades conhecidas**, com desbloqueio de Nível a cada 3 níveis:

| Nível do personagem | 1 | 3 | 5 | 6 | 7 | 9 | 11 | 12 | 13 | 15 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Habilidades conhecidas** | 1 | 2 | 3 | 3 | 4 | 5 | 6 | 6 | 7 | 8 | 8 |
| **Nível máximo de Habilidade** | 1 | 2 | 2 | 3 | 3 | 4 | 4 | 5 | 5 | 6 | 7 |

- A partir do **nível 16**, em vez de aprender Habilidades novas, você **reescreve uma Habilidade conhecida por nível** (mesmo processo de criação, agora podendo subir o Nível dela até o seu máximo).
- Habilidades Passivas contam no teto de 8.

*Por quê 8:* é o número de blocos de texto que um jogador consegue manejar sem consultar a ficha a cada turno, e com a economia de PH ele usa 2 ou 3 por combate de qualquer jeito. A regra de reescrita a partir do 16 mantém a progressão viva sem inflar a ficha: no fim da campanha você não tem mais Habilidades, você tem **Habilidades melhores** — que é exatamente o que acontece com um personagem de Honkai: Star Rail subindo os traços.

### 10.4 Validação do conteúdo criado pelo jogador

Toda Habilidade escrita por jogador passa por esta checagem antes de entrar na ficha. O capítulo 16 traz a lista como checklist, e o capítulo 27 (Guia do Mestre) repete do lado do Mestre.

| Campo | Obrigatório? | Limite | Se violar |
|---|---|---|---|
| Nome e descrição narrativa | Sim | — | Devolve para o jogador reescrever |
| Nível da Habilidade | Sim | ≤ seu Nível máximo (10.3) | Rejeitada |
| Tipo | Sim | Dano, Cura, Buff, Debuff ou Passiva | Rejeitada |
| Dados | Sim, se Dano ou Cura | Exatamente os da tabela 10.1 do Nível escolhido | Ajusta para a linha correta |
| Alcance | Sim | ≤ o alcance cumulativo do Nível | Reduz ao alcance do Nível |
| Alvos / área | Sim | Alvo único, ou **área = metade dos dados e até 3 alvos** (4 nos Níveis 6 e 7), agrupados a até uma Distância um do outro (10.1) | Converte para área com metade dos dados e corta os alvos excedentes |
| Resolução | Sim | Teste de Ataque **ou** Teste de Resistência do alvo, nunca os dois | Mestre escolhe um |
| Elemento | Sim | O Elemento do personagem, salvo Bênção que permita outro | Troca para o Elemento do personagem |
| Custo em PH | Automático | Pelo Nível (10.1) | — |
| Efeitos extras | Opcional | Dentro das linhas de 10.2 | Reduz ao permitido pelo Nível |
| Condição de recarga | Opcional | Só se o jogador quiser trocar custo por frequência | — |

**Efeitos proibidos em qualquer Nível** (lista fechada, para o Mestre não ter que argumentar): imunidade a dano; Vantagem permanente; **expandir a faixa de acerto crítico** (4.6 — isso é exclusivo do Caminho da Caça); mais de um Avanço Total por Ciclo; ação extra fora de Ritmo Acelerado ou Nível 5+; ignorar Tenacidade; ignorar o teto de RD; **atingir mais alvos em área do que 10.1 permite**; cura total; "o alvo morre"; remover a casa de alguém da Fila por mais de 1 turno; alterar a Eficiência ou a Eficácia de alguém; **trocar Eficiência por Eficácia na Esquiva** (6.3).

**Comportamento na falha:** o Mestre **ajusta** (primeira opção, preserva a ideia do jogador) ou **rejeita** (segunda opção, quando o conceito só funciona quebrando um limite). Em ambos os casos o motivo é registrado na Ficha de Decisões da Mesa, para a decisão valer para todo mundo na mesma situação. Habilidade aprovada que se revele quebrada em jogo pode ser **recriada sem custo** no próximo Descanso Longo — essa é a válvula de escape que mantém o sistema aberto sem travar a campanha.

A mesma estrutura de validação vale para **armas e itens criados pelos jogadores** (a v0.1 já convida: "Itens Comuns e Armas serão criadas com os jogadores"), para o **Memoespírito** (13) e para os **Cones de Luz** (16.3): tabela de limites, ajuste antes de rejeição, registro da decisão.

---

## 11. Caminhos

### 11.1 Os 9 Caminhos e o que a v0.1 entregou

A v0.1 tem 9 Caminhos na tabela de dados de vida, mas **só 5 foram escritos** com Bênçãos: Destruição, Inexistência, Harmonia, Abundância e Recordação. Erudição, Euforia, Caça e Preservação existem apenas como uma linha de PV. Essa é a maior lacuna de **conteúdo** da v0.1 (L17) e o maior volume de escrita da v1.0.

| Caminho | Aeon | Estado na v0.1 | Atributo de Habilidade (escolha fixa) |
|---|---|---|---|
| A Destruição | Nanook | Completo (10 Bênçãos) | Poder ou Vigor |
| A Inexistência | Ix | Completo (10 Bênçãos) | Discernimento ou Sincronia |
| A Harmonia | Xipe | Completo (10 Bênçãos) | Presença |
| A Abundância | Yaoshi | Completo (10 Bênçãos) | Presença ou Sincronia |
| A Recordação | Fuli | Completo (10 Bênçãos + Memoespírito) | Sincronia ou Discernimento |
| **A Erudição** | **Nous** | **Só PV — escrever do zero** | Sincronia |
| **A Euforia** | **Aha** | **Só PV — escrever do zero** | Presença ou Discernimento |
| **A Caça** | **Lan** | **Só PV — escrever do zero** | Agilidade |
| **A Preservação** | **Qlipoth** | **Só PV — escrever do zero** | Vigor ou Poder |

Cada Caminho entrega: 3 Perícias com Eficiência, o índice de vitalidade N (6.1), o Bônus de Velocidade (6.5), o Atributo de Habilidade permitido e as Bênçãos.

**Perícias dos 4 Caminhos novos** (seguindo o padrão dos 5 existentes — 3 Perícias temáticas cada):

- **A Erudição:** Ciência, Pesquisa e Tecnologia.
- **A Euforia:** Enganação, Acrobacia e Persuasão.
- **A Caça:** Furtividade, Percepção e Acrobacia.
- **A Preservação:** Resistência, Atletismo e Intuição.

### 11.2 Identidade mecânica dos 4 Caminhos novos

Para a escrita não inventar do zero, cada Caminho novo já tem o seu eixo travado — e nenhum deles repete o eixo de um Caminho existente:

| Caminho | Eixo mecânico | Recurso próprio |
|---|---|---|
| **A Erudição (Nous)** | Dano em área e multi-alvo; converte conhecimento em alcance | **Acúmulos de Cálculo**: cada inimigo atingido no turno dá 1 acúmulo; gaste acúmulos para adicionar alvos ou dados |
| **A Euforia (Aha)** | Caos controlado: efeitos aleatórios com resultado sempre útil, troca de posição na Fila | **Tabela do Riso** (d6 de efeitos) + capacidade de Avançar aliados |
| **A Caça (Lan)** | Alvo único, crítico e velocidade; a maior VEL do jogo | **Faixa de crítico 19-20** + marcação de presa (dano extra em um alvo por vez) |
| **A Preservação (Qlipoth)** | Escudos, RD e proteção de aliados; age por último e aguenta | **Barreira** (PV temporário que não acumula com cura) + Reações defensivas extras |

**Os quatro recursos, com número.** Isto aqui é o que impede a escrita das 48 Bênçãos novas de inventar economia nova em cada página:

**Acúmulos de Cálculo (Erudição).**
- Você ganha **1 acúmulo por inimigo atingido** por um mesmo ataque ou Habilidade sua, no seu turno. Máximo de **5** acúmulos.
- **Gastar não consome ação**, e pode ser feito no meio da sua própria ação: **1 acúmulo** adiciona **1 alvo** dentro do alcance; **2 acúmulos** adicionam **1 dado base** à rolagem de dano.
- Os alvos comprados com acúmulos **somam sobre a base de 10.1** (3 alvos, ou 4 nos Níveis 6 e 7) e respeitam o **teto absoluto de 6 alvos**. É a Erudição, e só ela, que alcança esse teto — é literalmente a promessa do Caminho, e é por isso que o teto existe em 10.1 em vez de ser "o que o Mestre achar".
- Zera no **fim do combate**. Não zera no fim do Ciclo.
- Os dados comprados com acúmulos são **dados base**: critam (4.6) e contam para a Redução de Tenacidade do ataque.

**Tabela do Riso (Euforia).** Role **1d6** quando uma Bênção da Euforia mandar. O resultado é sempre útil — é essa a piada do Caminho — e **nenhuma entrada passa de +2 ou de 1 dado**:

| d6 | Efeito |
|---|---|
| 1 | **Piada interna** — +1 dado base no seu próximo ataque neste Ciclo |
| 2 | **Tropeço cósmico** — o alvo mais próximo é **Atrasado em 1 casa** (respeita Firmeza, 7.4) |
| 3 | **Riso contagioso** — um aliado a até Distância Média ganha **+2** na próxima rolagem dele |
| 4 | **Troca de lugar** — você e um aliado trocam de casa na Fila; nenhum dos dois pode já ter agido neste Ciclo |
| 5 | **Sorte do tolo** — você ganha **Vantagem** na sua próxima rolagem neste Ciclo |
| 6 | **Aha! aprova** — o grupo recupera **1 PH** (1 vez por Ciclo) |

**Marcação de Presa (Caça).**
- **Ação Complementar**, **1 alvo por vez**, sem custo de PH.
- Seus ataques contra o alvo marcado ganham **+1 dado base**.
- A marca **migra de graça** para outro alvo quando o marcado é derrotado — é isso que faz a Caça parecer uma caçadora e não uma atiradora de turno único.
- Dura até o fim do combate ou até você marcar outro alvo.

**Barreira (Preservação).**
- É **PV temporário com nome próprio**: segue o teto global de `3 × Eficiência` (15.3), não acumula com outras fontes de PV temporário (fica a maior) e **não** é afetada por cura.
- Absorve dano antes dos PV e **ignora a ordem da RD**: a RD se aplica primeiro, a Barreira depois.
- A Barreira que você concede a um aliado conta no teto **dele**, não no seu.

### 11.3 Bênçãos: cadência para 20 níveis (override)

A v0.1 tem 10 Bênçãos por Caminho e o "Avatar" como capstone com requisito de nível 5.

**Decisões:**

1. **12 Bênçãos escritas por Caminho, 10 adquiridas** — uma a cada **nível ímpar** (1, 3, 5, 7, 9, 11, 13, 15, 17, 19).
2. **Três tiers de requisito por Caminho:** 6 Bênçãos sem requisito, 4 com requisito **nível 9+**, 2 com requisito **nível 17+** (uma delas é o Avatar).
3. **O Avatar passa a exigir nível 17** (era 5).

*Por quê 12 escritas e 10 adquiridas:* duas Bênçãos que você **não** pega é o mínimo para dois personagens do mesmo Caminho se diferenciarem, e é um volume de escrita realista. Fazer 20 Bênçãos por Caminho para cobrir 20 níveis um a um daria 180 Bênçãos no livro — meses de escrita e um capítulo que ninguém termina de ler. Com aquisição nos ímpares, os pares ficam livres para Habilidade, Atributo e equipamento, e **nenhum nível sobe vazio**.

*Por quê mover o Avatar para o 17:* é literalmente "você se torna uma manifestação viva do Caminho". Os efeitos que o autor escreveu são de capstone (bônus dobrados, +2 dados, ressuscitar aliado, dobro de Redução de Tenacidade em área). No nível 5 de um jogo de 20 níveis, isso é poder de fim de campanha entregue no primeiro quinto dela — e invalidaria os 15 níveis seguintes de progressão do Caminho.

**Volume de escrita que isso define** (vai para o plano):

| Caminho | Bênçãos existentes | A escrever | Total |
|---|---|---|---|
| Destruição, Inexistência, Harmonia, Abundância, Recordação | 10 cada | **+2 cada = 10** | 60 |
| Erudição, Euforia, Caça, Preservação | 0 | **12 cada = 48** | 48 |
| **Total** | 50 | **58 novas** | **108** |

As 2 Bênçãos novas de cada Caminho existente devem ocupar os **tiers altos** (nível 9+ e 17+), porque é exatamente onde os Caminhos da v0.1 são rasos: a progressão deles hoje termina no Avatar.

### 11.4 Reescalonamento das Bênçãos herdadas (erro E25)

Várias Bênçãos da v0.1 carregam números fora de qualquer escala: "+10 em qualquer teste de Perícia 2 vezes ao dia", "-10 de dano", "a defesa inimiga conta como -10", "+10 de Defesa por 1 rodada", "15 de RD", "-3 dados de dano causado". Em um jogo onde a Defesa típica vai de 13 a 27 e a Eficiência vai de +2 a +8, um "+10" fixo é maior que qualquer outro bônus do sistema.

**Regra de conversão para a escrita** (aplicada caso a caso nos capítulos 07 a 15). A tabela cobre **todas** as construções fora de escala que a v0.1 produz; se a escrita encontrar uma que não está aqui, ela não inventa número — ela cai na linha mais próxima e registra na Ficha de Decisões da Mesa:

| Padrão da v0.1 | Conversão v1.0 |
|---|---|
| "+10 em qualquer teste" (Memória da Sabedoria) | "+Eficácia em um teste" |
| "+10 de Defesa" | "+Eficiência de Defesa" |
| **"+4 de Defesa"** (Memória da Guarda) | "+Eficiência de Defesa" |
| "-10 de dano" / "-3 dados de dano" | "-1 dado de dano (máx. -2 dados)" |
| **"50% mais de dano"** (Memória da Sabedoria) | "+1 dado base" |
| "defesa inimiga conta como -10" (Ataque Espiritual) | "ignora Eficiência pontos de Defesa do alvo" |
| **"você ignora 5 de defesa"** (Colapso das Defesas) | "ignora Eficiência pontos de Defesa do alvo" |
| **"romper (-5 na defesa)"** (Aniquilador de Resistências) | "ignora Eficiência pontos de Defesa do alvo" |
| **"o DT será o acerto do seu Ataque -8"** (Aniquilador de Resistências) | "**DT = 8 + Bônus do seu Atributo de Habilidade + Eficiência**" — a DT oficial de 4.2. Não existe DT derivada de uma rolagem no livro |
| **"+5 no teste de ataque"** (Sincronia de Memórias) | "+1 no Teste de Ataque" (dentro do teto de bônus somado, 9.6) |
| **"-1 em ataques (chegando no máximo em -10)"** (Silêncio da Existência) | "-1 em ataques, acumulando **até o teto de penalidade somada** da faixa (9.6)" |
| "10 RD" / "15 RD" | "RD igual à sua Eficiência" ou "+2 RD" |
| **"+5 RD"** (Excesso de Vida) | "+2 RD" |
| **"+10 de RD"** (Memória da Guarda, Guardião) | "RD igual à sua Eficiência" |
| "+30 de PV máximo" (Guardião) | "+PV igual a 3 × nível" |
| **"+20 de PV máximo"** (Corpo Imortal) | "+PV igual a 2 × nível" |
| "+20 PV temporários" (Cântico Inspirador) | "PV temporários = 2 × Eficiência" (teto global em 15.3) |
| **"1d10 / 1d12 de efeito contínuo"** (Ataque Espiritual, Raízes da Abundância, Campo da Harmonia Universal) | "1d6 + Eficiência, uma vez por turno do alvo" |
| "cura igual a **metade da vida máxima** do alvo" (Bênção Revitalizante, Renascimento Natural, Avatar da Abundância) | "cura igual a **5 × nível**, com teto de metade do PV máximo do alvo" |
| "recupera **metade dos PV perdidos**" (Avatar da Destruição) | "recupera **5 × nível** PV" |
| "o Memoespírito recebe **metade da sua vida** de PV máximo" (Ecos do Passado) | "+PV máximo igual a **4 × nível do dono**" |
| "20% de Vida / 10% de Defesa / 15% de Ataque" (Avatar da Recordação, Forma Sincronizada) | "+PV igual a 2 × nível, +1 de Defesa, +1 dado base" |
| "causa 1d4/1d6/1d8 fixo" | mantém, por ser dado pequeno de efeito contínuo |
| "+1 dano", "+2 de dano" | mantém (é bônus pequeno de acúmulo) |
| "o dobro de Redução de Tenacidade" | mantém, respeitando a Firmeza de Elite/Boss |

**Regra geral de política, que vale para todo capítulo:** **nenhum efeito do livro cura, concede PV ou causa dano em porcentagem do PV máximo.** Tudo é valor fixo, dados, ou múltiplo de nível / Eficiência. O motivo é o mesmo que aposentou a "Cura toda a Vida" da Habilidade Nível 5 (10.1): no nível 20, "metade da vida máxima" é 130 de cura numa Bênção — mais que uma Habilidade de Nível 6, de graça e sem custar PH. Cortar a cura total da Habilidade e manter a porcentagem na Bênção seria incoerência de política entre capítulos.

**Única exceção, declarada:** o **Sangramento** (9.6) causa Dano Contínuo de 5% dos PV máximos do alvo, porque é o efeito de Quebra do elemento Físico que a v0.1 escreveu assim e porque ele já tem teto próprio (`3 × Eficiência`). Ele é a exceção justamente por ser o único.

**Fora da régua de conversão:** as **penalidades de armadura** (16.1). Elas são escolha de equipamento feita pelo jogador, não número herdado solto, e por isso são calibradas na própria tabela de armaduras.

---

## 12. Raças

As 7 Raças da v0.1 ficam: Humano, Xianzhouíta, Vidyadhara, Vulpes, Haloviano, Avginiano, Intellitron.

**O que é padronizado:** cada Raça entrega **bônus de atributo mais um ou dois traços**, apresentados sempre na mesma ordem (nome, citação, características, bônus de atributo, traços com regra fechada). **Não** existe exigência de "exatamente um traço passivo e um traço especial": nenhuma das 7 Raças da v0.1 está nesse formato, e forçar a simetria obrigaria a fase de escrita a **inventar** traços para cinco raças — exatamente o que este documento existe para evitar. O que se padroniza é a apresentação e a precisão das regras, não a contagem de traços.

**Consertos, raça por raça:**

| Raça | Conserto |
|---|---|
| **Humano** | "+2 em algum atributo" ganha teto explícito: nenhum atributo passa de **15 antes dos bônus de Raça** nem de **20 depois** (erro E16). O **Esforço** passa a ter regra fechada: 1 ponto, re-rola qualquer dado, máximo 1 acumulado, recupera no Descanso Longo ou ao agir de acordo com a crença (1 vez por sessão, aprovação do Mestre) |

> **O Esforço é recurso exclusivo do Humano.** Nenhuma outra Raça, Caminho, Bênção, Habilidade, Cone de Luz ou item concede Esforço, e uma mesa sem nenhum Humano simplesmente não tem esse recurso. É assim na v0.1 — o Esforço nasce da passiva **Força de Vontade** do Humano e de nenhum outro lugar — e fica assim. Os três lugares que falam dele dizem a mesma coisa: aqui, no Descanso Longo (15.2) e na lista de omissões do balanceamento (18.1).
| **Xianzhouíta** | Mantido. "Não pode ser Executado" e Vantagem em Testes de Resistência é forte, e está certo que seja: é a raça da longevidade |
| **Vidyadhara** | Ganha traço passivo (faltava): **Vantagem em Testes de Resistência Física contra afogamento, frio e efeitos de água**, além da Reencarnação Ancestral |
| **Vulpes** | O "Teste de Atenção" exclusivo vira **Teste de Percepção Mental, DT 10** (erro E13) |
| **Haloviano** | O traço **To na sua mente** passa a ter uma sequência fechada, abaixo (erro E15) |
| **Avginiano** | Mantido. "Testes Mentais" passa a nomear os Testes oficiais: **Resistência Mental, Percepção Mental e Força de Vontade** |
| **Intellitron** | Mantido, com mecânica: o teste racial virou a regra geral de 9.3, e o Intellitron faz esse teste **com Vantagem** e descobre **duas** Fraquezas em um sucesso. Mantém a Vantagem em Tecnologia e Mecânica |

**To na sua mente (Haloviano) — texto fechado, para o capítulo 05 não decidir sozinho:**

> **2 vezes por dia.** Gaste a sua **Ação Complementar**. Se você segue o Caminho da Harmonia, não há teste de ativação; caso contrário, faça um **Teste de Sintonia, DT 13** e, na falha, você não pode usar este traço até o próximo **Descanso Longo**.
> Em ambos os casos o alvo faz um **Teste de Força de Vontade** contra a sua DT (`8 + Bônus do Atributo de Habilidade + Eficiência`). Na falha, fica **controlado** por **2 turnos** (Comum) ou **1 turno** (Elite/Boss). Não funciona em Boss em cena de clímax sem autorização do Mestre.

*O que mudou e por quê:* é **Força de Vontade** e não Resistência Mental porque a tabela de 14 atribui "medo, intimidação, controle mental, possessão" explicitamente à Força de Vontade — e a descrição da v0.1 diz a mesma coisa. O **teste oposto de Persuasão contra Intuição** da v0.1 foi aposentado (está no changelog 21.2): com os 6 Testes de Resistência oficiais existindo, abrir um teste oposto exclusivo de uma raça reintroduz o problema que a v1.0 fechou no Teste de Atenção dos Vulpes. O limite de **2 usos por dia** e o **bloqueio na falha** são da v0.1 e ficam — só o "1 dia" passou a ser "até o próximo Descanso Longo", que é o relógio oficial do sistema (15.2).

---

## 13. Memoespírito (Caminho da Recordação)

O Guia de Criação de Memoespírito da v0.1 é bom e fica quase inteiro. Faltava a ficha (erro E26) e faltava dizer como ele age (L01).

### 13.1 Ficha do Memoespírito

**Decisão: as estatísticas do Memoespírito são ancoradas no dono. Os 12 pontos da v0.1 ficam, mas como diferenciação entre dois Memoespíritos, não como escala de campanha.**

| Estatística | Fórmula |
|---|---|
| **PV** | `8 × nível do dono + (3 × pontos em Vigor)` |
| **Defesa** | `10 + pontos em Agilidade + Eficiência do dono` |
| **Velocidade** | `10 + pontos em Agilidade + Bônus de Velocidade do Caminho do dono` |
| **Teste de Ataque** | `d20 + Bônus do Atributo de Habilidade do dono + pontos no atributo de ataque + Eficiência do dono` |
| **Dano do ataque** | `(Dados de Ataque Básico do dono, coluna de 17) de d6 + pontos no atributo de ataque`, no Elemento escolhido na criação |
| **Redução de Tenacidade** | 1 (**2** a partir do nível 11 do dono) |
| **Testes de Resistência** | `d20 + pontos no atributo + Eficiência do dono` |
| **RD** | 0 (salvo Função Guardião ou Bênção) |

**Pontos:** 12 na criação, **+1 a cada 2 níveis** do dono (22 no nível 20), **máximo 5 por atributo** — tudo preservado da v0.1. Os pontos funcionam como bônus direto, exatamente como o autor escreveu.

*Por quê ancorar no dono:* a economia de 12 pontos com teto 5 é da v0.1 e é boa para **diferenciar** dois Memoespíritos, mas ela não cresce com a campanha. Preservar o número sem reescalar o alcance dele produzia um companheiro que, no nível 20, tinha Teste de Ataque +13 contra Defesa 28 de Boss (30% de acerto), Defesa 15 contra ataque inimigo +15 (o inimigo nunca erra) e 12 de dano num Ciclo em que o grupo precisa entregar 275. Ele ocupava casa própria na Fila — tempo de mesa — e contribuía ~2% do dano: o Caminho da Recordação parava de funcionar na metade da campanha. Amarrando Defesa, ataque, dano e Velocidade ao dono, o Memoespírito acompanha a curva, e os pontos continuam decidindo **que tipo** de companheiro ele é.

**Alvo de projeto, que `simular-combate.ps1` (23) verifica:** *o Memoespírito entrega entre **15% e 25%** do dano do dono na mesma faixa.* Na faixa 17-20, com 5 pontos no atributo de ataque, ele ataca a `+18` e causa `5d6 + 5` ≈ 22 (29 com Fraqueza), uma vez por Ciclo — cerca de **25%** do que o dono entrega. Isso significa que um grupo com Recordação tem DPC 5% a 8% acima do grupo de referência de 18.2, e essa folga está dentro do arredondamento do orçamento de PV do inimigo.

### 13.2 Conceito, Função e Bônus

Mantidos integralmente: os 5 Conceitos (Guerra, Perdida, Animal, Artificial, Celestial), as 4 Funções (Predador, Guardião, Catalisador, Controlador), os 6 Bônus menores (escolhe 3), as 2 Habilidades próprias (1 ofensiva + 1 auxiliar) e as Evoluções. As Evoluções mudam de nível: a v0.1 as colocava nos níveis 5 e 10; na v1.0 elas ficam nos níveis **8, 14 e 20** (três evoluções, uma por faixa alta).

### 13.3 Como o Memoespírito age (lacuna L01)

- **Tem casa própria na Fila de Ação**, pela VEL dele.
- No turno dele, executa **1 ação**: um Ataque Básico, **ou** uma das suas 2 Habilidades, **ou** uma Ação de Movimento. Mais 1 Reação própria.
- **Invocar:** Ação Complementar do dono + **1 PH**. Fica até ser dispensado ou cair a 0 PV. Se cair, só volta no próximo **Descanso Curto**.
- As ações do Memoespírito geram **metade da Energia** (arredonda para baixo) para o dono.
- As Habilidades do Memoespírito **não** gastam PH (o custo foi pago na invocação).

*Por quê casa própria e não "age no turno do dono":* as Bênçãos da Recordação na v0.1 já pressupõem que ele ataca, reage e sofre dano por conta própria ("quando o Memoespírito acertar um ataque", "o Memoespírito pode realizar um ataque como reação"). Dar casa própria preserva tudo isso. A contrapartida de **1 ação por turno** é o que evita o jogador da Recordação ter o dobro do tempo de mesa dos outros.

---

## 14. Testes de Resistência

Os 6 Testes da v0.1 ficam com os nomes e as descrições exatos. O que faltava era dizer **qual atributo cada um usa** — e aqui há uma simetria que vale travar: um Teste por Atributo.

| Teste de Resistência | Atributo | Resiste a |
|---|---|---|
| **Potência Física** | Poder | Empurrões, agarrões, romper obstáculos, impactos |
| **Reflexos** | Agilidade | Desviar de área, armadilhas, perigos repentinos |
| **Resistência Física** | Vigor | Venenos, doenças, fadiga, temperatura, Sangramento |
| **Resistência Mental** | Sincronia | Ilusões, manipulação cognitiva, ataque psíquico |
| **Percepção Mental** | Discernimento | Reconhecer ameaça, manter concentração, não ser enganado pelos sentidos |
| **Força de Vontade** | Presença | Medo, intimidação, controle mental, possessão, Morrendo |

> **Teste de Resistência = d20 + Bônus do Atributo + Eficiência** (ou Eficácia, no que você escolheu em 4.3).

> **Exceção única, declarada:** o **Teste de Força de Vontade de Morrendo** (15.1) é `d20 + Bônus de Presença`, **sem Eficiência e sem Eficácia**, contra DT 10. É a única rolagem do livro que não soma o seu bônus de nível, e isso tem razão de ser: Morrendo não é resistir a um efeito externo, é a sua vontade de continuar de pé. Não existe treino que te torne bom em não morrer, e é esse teste que mantém a morte sendo uma possibilidade real no nível 20 (15.1).

*Por quê Resistência Mental com Sincronia:* a descrição do autor fala de "manipulações cognitivas" e "ataques psíquicos", e Sincronia é o atributo de domínio da energia dos Caminhos e da própria mente treinada. Essa atribuição também é a única que fecha a simetria de **um Teste por Atributo**, o que torna a ficha autoexplicativa e impede a pergunta "qual eu uso?" na mesa. Percepção Mental fica com Discernimento (instinto e atenção) e Força de Vontade com Presença (determinação), exatamente como as descrições da v0.1 sugerem.

Todo personagem tem **Eficiência nos 6** desde o nível 1.

---

## 15. Dano, cura, Morrendo, Executado e Descanso

### 15.1 Morrendo e Executado (erro E14)

A v0.1 descreve o estado mas não diz qual Teste, qual DT, nem quando se rola. Fechado:

- A 0 PV você fica **Morrendo**: inconsciente, **mantém a casa na Fila**, e no seu turno faz um **Teste de Força de Vontade, DT 10** — e este é o único Teste de Resistência do livro que soma **só `d20 + Bônus de Presença`, sem Eficiência nem Eficácia** (14).
- **3 sucessos** antes de **3 falhas**: você estabiliza com 1 PV (regra do autor preservada). 3 falhas antes: o personagem morre.
- **20 natural:** você se levanta na hora com 1 PV. **1 natural:** conta como **2 falhas**.
- Receber dano enquanto Morrendo: **1 falha automática**. Dano de uma Habilidade de Nível 5 ou maior, ou um crítico: **2 falhas**.
- Qualquer cura remove o estado e zera o contador.
- **Executado:** um ser racional gastando o Ataque Básico dele a Distância Pessoal mata você automaticamente. Bestas e máquinas sem consciência não executam (regra do autor preservada). Um aliado pode impedir com a Reação **Intervir**.
- **Xianzhouítas** não podem ser Executados (traço racial preservado).

*Por quê este teste não soma Eficiência:* com Eficiência, um PC de nível 20 com Presença +5 somaria +13 contra DT 10 e só falharia no 1 natural. Dos níveis 8-10 em diante **ninguém morreria**, e a margem de attrition que 18.3 calibra com cuidado ("um personagem que vira foco cai em 4 a 7 acertos") perderia a consequência. Sem Eficiência, a conta fica honesta nos dois extremos: um personagem de Presença -1 estabiliza em 50% das rolagens e um de Presença +5 em 80% — nunca em 100%. Três falhas seguidas a 80% ainda acontecem, e é esse 1% que faz a mesa prender a respiração quando alguém cai. A alternativa era deixar a DT 10 somando tudo e declarar que, a partir do meio da campanha, a ameaça real passa a ser o Executado; preferi manter a ameaça distribuída, porque o Executado depende de um inimigo **racional** estar a Distância Pessoal e boa parte do bestiário é besta ou máquina.

### 15.2 Descanso (lacuna L20 / erro E20)

A v0.1 usa "uma vez por descanso" em 3 Bênçãos (Último Fragmento de Vida, Bênção da Harmonia, Renascimento Natural) sem definir descanso.

| Tipo | Tempo | Recupera |
|---|---|---|
| **Descanso Curto** | 1 hora, até 2 por dia | PV = (2 × nível) + Bônus de Vigor; recarrega efeitos "1 vez por descanso"; reinvoca Memoespírito |
| **Descanso Longo** | 8 horas, 1 por dia | Todos os PV, remove todas as condições, recarrega tudo, devolve o ponto de **Esforço a quem tiver o traço que o concede** (Humano, 12), permite recriar uma Habilidade problemática |

A **Energia de Ultimate não zera** em nenhum dos dois (8.3). **Descanso não mexe em PH:** o PH volta ao valor inicial no começo de cada combate (8.2), e fora de combate ele simplesmente não existe — por isso nenhuma das duas linhas cita PH.

### 15.3 Cura e PV temporários

> **Teto global de PV temporários = 3 × Eficiência**, vindos de **qualquer fonte** (Habilidade, Bênção, Ultimate, Cone de Luz, item, Barreira). **PV temporários não acumulam entre fontes: fica o maior valor.** Esse teto é invariante do sistema (19) e é o mesmo número citado em 10.2, 11.4 e aqui.

- Cura acima do PV máximo é **perdida**, exceto pela Bênção "Excesso de Vida" da Abundância, que a converte em PV temporário dentro do teto acima.
- **Barreira** (recurso da Preservação, 11.2) é PV temporário com nome próprio e segue a mesma regra e o mesmo teto.
- Poções (erro E22): a v0.1 cura 1d20/2d20/3d20, o que faz uma poção pequena curar de 1 a 20. Vira **fixo: 15 / 30 / 50**, ocupando 0,5 / 1 / 2 de Espaço.

### 15.4 Inventário (erro E21)

A v0.1 mede itens em "Espaço" sem dizer quanto cabe. **Capacidade = 10 + (2 × Bônus de Poder)**. Acima disso você fica com **Lentidão**. Acima do dobro, não consegue se mover.

---

## 16. Equipamentos

### 16.1 Armaduras e Vestimentas (erro E11)

| Tipo | Defesa | Outros | Esquiva |
|---|---|---|---|
| Leve | +3 | +1 de Velocidade | Permitida |
| Média | +5 | — | Permitida |
| Pesada | +6 | **2 RD**, **-2 em Testes e Perícias de Agilidade**, **-2 de Velocidade** | **Proibida** |

A Armadura Leve da v0.1 dava "+1 de Bônus de Agilidade", o que mexia em PV indireto, Defesa, Esquiva e Perícias de uma vez. Virou **+1 de Velocidade**: o mesmo sabor de "leve e rápido", sem tocar no atributo. A Pesada perdeu 10 RD e ganhou 2 RD mais a proibição de Esquiva, que é um custo de verdade.

*Por quê o -5 da v0.1 virou -2 e -2 de Velocidade:* num jogo onde a Eficiência chega a +8 e os bônus temporários têm teto de +5, um **-5 fixo** seria a maior penalidade do livro e tornaria a Armadura Pesada inutilizável para qualquer personagem que role Agilidade. Dois pontos de penalidade (um degrau inteiro de Bônus de Atributo) mais dois de Velocidade — que na Fila de Ação custam posição de verdade — entregam o mesmo recado "você está dentro de uma lata" com números na escala do resto do sistema. A penalidade de Velocidade é a tradução correta de "armadura pesada te deixa lento" agora que Velocidade existe.

### 16.2 Armas

Tabela por categoria em 9.2. **Armas criadas pelos jogadores** seguem a validação de 10.4: escolhem uma categoria da tabela, um Elemento (ou Físico) e até **uma** propriedade especial (ex.: recarga, duas mãos, arremessável, +1 de Redução de Tenacidade). A v0.1 já prometia que armas aprovadas entram na lista oficial do livro — a v1.0 mantém a promessa e reserva um apêndice para isso.

### 16.3 Cones de Luz (lacuna L15 / ponto 15)

Cada personagem equipa **1 Cone de Luz**: um artefato-memória que carrega uma história. Mecanicamente, cada Cone tem **Nível** (1 a 5) e entrega **duas coisas**:

1. **Bônus Maior** (numérico, fixo): escolhido na lista — PV, Defesa, Velocidade, dano de uma das 3 categorias, RD, ou bônus em um tipo de Teste.
2. **Efeito Condicional** (o "sabor"): dispara em uma condição temática, como "quando você usa a Ultimate", "quando **você Quebra um inimigo**", "no primeiro Ciclo do combate", "quando um aliado cai a Morrendo". Gatilho que depende de um **aliado ser Quebrado não existe** — só inimigos têm Tenacidade (9.4).

| Nível do Cone | Nível do personagem necessário | Bônus Maior | Efeito Condicional |
|---|---|---|---|
| 1 | 1 | +1 ou +10 PV | 1 efeito simples, 1 vez por combate |
| 2 | 5 | +1 e +10 PV | 1 efeito, 1 vez por Ciclo |
| 3 | 9 | +2 ou +25 PV | 1 efeito + pequeno ganho de Energia |
| 4 | 13 | +2 e +25 PV | 2 efeitos |
| 5 | 17 | +3 ou +50 PV | 2 efeitos, um deles podendo conceder Avanço |

**Sobreposição 1-5:** duplicatas do mesmo Cone aumentam o Bônus Maior, **até o teto absoluto de +3** (ou +50 PV) — a Sobreposição serve para um Cone de Nível baixo alcançar o valor de um Cone de Nível alto, não para ultrapassá-lo. Nenhum Cone concede Vantagem permanente nem mexe em Eficiência/Eficácia.

**Onde o Cone entra no teto de bônus (9.6):** o **Bônus Maior é permanente e fica fora** do teto de bônus somado — ele é equipamento, está no orçamento de ataque de 4.3 e de 18.2, e é o que fecha o `+19` do atacante de referência. O **Efeito Condicional é temporário e entra** no teto. Essa separação é o que impede o Cone de competir com o buff do aliado da Harmonia pelo mesmo espaço.

### 16.4 Relíquias (lacuna L15)

**6 slots:** Cabeça, Mãos, Tronco, Botas, Esfera Planar e Corda de Ligação. Quatro tiers por faixa de nível.

| Slot | Bônus | Tier I (1-6) | Tier II (7-12) | Tier III (13-17) | Tier IV (18-20) |
|---|---|---|---|---|---|
| Cabeça | PV máximos | +10 | +20 | +35 | +50 |
| Mãos | Dano de Ataque Básico | +2 | +4 | +6 | +8 |
| Tronco | Defesa | +1 | +1 | +2 | +2 |
| Botas | Velocidade | +2 | +3 | +4 | +5 |
| Esfera Planar | Dano de um Elemento escolhido | +2 | +4 | +6 | +8 |
| Corda de Ligação | Energia, **1 vez por combate** | +10 | +15 | +20 | +25 |

**Bônus de conjunto** (as peças pertencem a Conjuntos temáticos):

- **2 peças:** um bônus pequeno e fixo (+1 em um tipo de rolagem, +1 de Velocidade, +2 de dano, +1 RD).
- **4 peças:** um efeito condicional por Ciclo (ex.: "ao Quebrar um inimigo, seu próximo ataque ganha +1 dado"; "ao usar a Ultimate, o grupo recebe +1 de Defesa por 1 Ciclo").
- **Teto:** os bônus de conjunto não somam mais de **+3** em uma mesma rolagem, e **entram** no teto global de 9.6 (são efeitos temáticos temporários, ao contrário do bônus de slot, que é permanente e fica fora).

**Corda de Ligação, regra fechada:** a Energia é concedida **1 vez por combate**, no momento em que você entra na Fila de Ação. O excedente acima de 100 é perdido (8.3). Entrar em duas lutas seguidas sem Descanso concede o bônus nas duas — cada combate é um combate.

**Mãos e Esfera Planar nunca somam na mesma rolagem.** O bônus da **Esfera Planar** se aplica a **dano de Habilidade, de Ultimate e de Dano Contínuo** do Elemento escolhido, e **não ao Ataque Básico**, que já é coberto pelas **Mãos**. Sem essa linha, um personagem cuja arma causa dano do próprio Elemento (permitido por 9.1 e 16.2) somaria os dois no mesmo Ataque Básico e teria **+16** no Tier IV em vez de +8 — e o orçamento de 18.2, que usa Mãos no básico e Esfera na Habilidade e na Ultimate, trata os dois como conjuntos disjuntos.

*Por quê bônus pequenos e fixos:* Relíquia é o lugar onde um sistema de 20 níveis costuma estourar, porque são 6 slots multiplicados por 20 níveis. Amarrando cada slot a **uma** estatística e a **um** valor por tier, o Mestre sabe exatamente quanto o equipamento contribui em cada faixa — e o passe de balanceamento consegue somar isso (é a coluna "equipamento" dos cálculos de 18).

### 16.5 Ressonâncias (os Eidolons do sistema)

**Decisão: Eidolons não são compráveis nem aleatórios — são marcos narrativos, chamados Ressonâncias.**

| Ressonância | Nível | O que concede (escolha uma opção) |
|---|---|---|
| **I** | 5 | 1 uso de Habilidade por combate sem custo de PH; **ou** +1 de Velocidade permanente |
| **II** | 10 | Sua Ultimate ganha um efeito extra, dentro dos limites de 10.2 lidos no **Nível equivalente da sua faixa** (8.5) |
| **III** | 15 | Uma Habilidade sua sobe 1 Nível de efeito, sem passar do seu Nível máximo |
| **IV** | 20 | Sua Ultimate **ativa com 80 de Energia e consome 80** (o teto de Energia continua 100); **ou** sua Bênção Avatar afeta um alvo adicional |

*Por quê narrativo e não aleatório:* em Honkai: Star Rail, Eidolon é progressão de longo prazo que aprofunda o que o personagem já é. Numa mesa, transformar isso em sorteio cria disparidade entre jogadores por motivo nenhum. Amarrando às Ressonâncias nos níveis 5, 10, 15 e 20, cada faixa da campanha tem um marco próprio, todos os jogadores evoluem juntos e o Mestre tem quatro momentos de história garantidos para pendurar arcos pessoais (o **Propósito de Vida** de cada personagem).

---

## 17. Tabela mestra de progressão 1-20 (lacuna L14 / ponto 14)

Esta é a tabela que vai no capítulo `26-progressao-e-ressonancias.md` e na contracapa. Nenhum nível sobe vazio.

| Nível | Eficiência | Eficácia | Bênçãos | Habs. conhecidas | Nível máx. de Habilidade | Aumento de Atributo | Dados de Ataque Básico | Especialização | Teto de RD |
|---|---|---|---|---|---|---|---|---|---|
| 1 | +2 | — | 1 | 1 | 1 | — | 1 | — | 6 |
| 2 | +2 | — | 1 | 1 | 1 | — | 1 | — | 6 |
| 3 | +2 | — | 2 | 2 | 2 | **+2** | 1 | — | 6 |
| 4 | +3 | — | 2 | 2 | 2 | — | 1 | — | 8 |
| 5 | +3 | **1 P / 1 TR** | 3 | 3 | 2 | — | **2** | **+1** | 8 |
| 6 | +3 | 1 P / 1 TR | 3 | 3 | **3** | **+2** | 2 | +1 | 8 |
| 7 | +4 | 1 P / 1 TR | 4 | 4 | 3 | — | 2 | +1 | 10 |
| 8 | +4 | **2 P / 1 TR** | 4 | 4 | 3 | — | 2 | +1 | 10 |
| 9 | +4 | 2 P / 1 TR | 5 | 5 | **4** | **+2** | **3** | +1 | 10 |
| 10 | +5 | 2 P / 1 TR | 5 | 5 | 4 | — | 3 | +1 | 12 |
| 11 | +5 | **2 P / 2 TR** | 6 | 6 | 4 | — | 3 | **+2** | 12 |
| 12 | +5 | 2 P / 2 TR | 6 | 6 | **5** | **+2** | 3 | +2 | 12 |
| 13 | +6 | 2 P / 2 TR | 7 | 7 | 5 | — | **4** | +2 | 14 |
| 14 | +6 | **3 P / 2 TR** | 7 | 7 | 5 | — | 4 | +2 | 14 |
| 15 | +6 | 3 P / 2 TR | 8 | 8 | **6** | **+2** | 4 | +2 | 14 |
| 16 | +7 | 3 P / 2 TR | 8 | 8 (reescreve 1/nível) | 6 | — | 4 | +2 | 16 |
| 17 | +7 | **4 P / 2 TR** | 9 | 8 | 6 | — | **5** | **+3** | 16 |
| 18 | +7 | 4 P / 2 TR | 9 | 8 | **7** | **+2** | 5 | +3 | 16 |
| 19 | +8 | 4 P / 2 TR | 10 | 8 | 7 | — | 5 | +3 | 18 |
| 20 | +8 | **5 P / 3 TR** | 10 | 8 | 7 | — | 5 | +3 | 18 |

**Como ler as colunas:**

- **Eficácia:** **P** = Perícias, **TR** = Testes de Resistência com Eficácia. Negrito marca o nível em que o ganho acontece.
- **Dados de Ataque Básico:** é **quantos dados a sua arma rola**, partindo de 1 (9.2). Uma arma de 1 dado chega a 5 dados no nível 17; uma arma de **Energia**, que começa com 2, chega a **6**.
- **Especialização:** é a **Especialização de Combate** (4.3) e vale em **todos os seus Testes de Ataque**, com arma, Habilidade ou Ultimate. Não é por categoria de arma e está fora do teto de bônus somado (9.6).

**Recursos do grupo e equipamento por faixa:**

| Faixa | PH (máx / início / geração) | Ultimate (Nível equiv. / média) | Cone de Luz máx. | Relíquias | Ressonância | Pontos do Memoespírito | Teto de bônus somado |
|---|---|---|---|---|---|---|---|
| 1-4 | 5 / 3 / +1 | **2** / 27 | Nível 1 | Tier I | — | 12-14 | +3 |
| 5-8 | 5 / 3 / +1 | **3** / 39 | Nível 2 | Tier I → II (7) | **I** (nível 5) | 14-16 | +3 |
| 9-12 | 5 / 3 / +1 → 6 / 4 / +2 (10) | **4** / 63 | Nível 3 | Tier II | **II** (nível 10) | 16-18 | +3 → +4 (10) |
| 13-16 | 6 / 4 / +2 → 7 / 5 / +2 (16) | **5** / 105 | Nível 4 | Tier III | **III** (nível 15) | 18-20 | +4 → +5 (16) |
| 17-20 | 7 / 5 / +2 | **6** / 147 | Nível 5 | Tier III → IV (18) | **IV** (nível 20) | 20-22 | +5 |

Os valores de **PH** desta tabela são de uma mesa de **4 jogadores**; a fórmula por tamanho de mesa está em 8.2. **Ultimate:** potência e teto de efeito em 8.5. **PV:** fórmula e tabela por Caminho em 6.1. **Velocidade:** fórmula em 6.5, crescimento só por equipamento e Bênção.

### 17.1 Como se sobe de nível

Faltava a regra mais básica de um sistema cujo eixo é uma curva de 20 níveis. Fechada:

> **Progressão por marco narrativo.** O grupo sobe de nível **junto**, ao concluir um arco da campanha ou um objetivo que o Mestre tenha anunciado como marco. **Não existe XP por inimigo derrotado.**

- **Ritmo sugerido:** 2 a 4 sessões por nível nas faixas 1-8; 4 a 6 sessões por nível daí em diante.
- As **Ressonâncias** (níveis 5, 10, 15 e 20) são **sempre** marcos de história, nunca ganhos automáticos de tabela — é o lugar natural para fechar um capítulo do **Propósito de Vida** de alguém.
- Subir de nível acontece **fora de combate**, num momento de respiro (tipicamente um Descanso Longo). Tudo que o nível novo entrega (tabela acima) vale a partir dali.
- Personagem novo ou substituto entra no **nível do grupo**, com o equipamento do tier da faixa.

*Por quê marco e não XP:* o sistema já tem três contadores em jogo (PV, PH, Energia) e um quarto, fora de combate, só serviria para transformar a mesa em planilha. Mais importante: num jogo em que o jogador **escreve as próprias Habilidades**, subir de nível é um evento de oficina — você reescreve, escolhe Bênção, ajusta a Ultimate. Isso precisa acontecer quando a história respira, não no meio de um corredor porque o terceiro Comum morreu. O dono dessa regra é o capítulo 26.

---

## 18. Passe de balanceamento 1-20 (lacuna L16 / ponto 16)

### 18.1 A abordagem e as premissas fechadas

O critério é um só e vale em **todas as faixas**: **um combate típico termina em 3 a 5 Ciclos**, com 4 Ciclos como centro de projeto.

O método tem quatro passos:

1. **Construir o personagem de referência** por faixa: array oficial, Raça somando no atributo principal, aumentos de Atributo gastos no principal até o teto, Eficiência da faixa, equipamento do tier da faixa, Habilidades no Nível máximo da faixa.
2. **Calcular o DPC** (Dano do grupo por Ciclo) para um grupo de 4, parcela por parcela, com as premissas abaixo.
3. **Derivar o orçamento de PV do inimigo:** `PV do encontro = DPC × 4`. Dividir entre Comum (1/7 do orçamento), Elite (1/3) e Boss (85%, porque Boss costuma vir sozinho ou com 1-2 acompanhantes).
4. **Derivar Defesa, dano inimigo e Tenacidade** a partir das janelas-alvo.

**As 17 premissas do DPC — fechadas, publicadas e usadas por `simular-combate.ps1`.** Sem elas o DPC é uma afirmação; com elas, qualquer pessoa reproduz a conta. Dezesseis são **consequência das regras** e qualquer leitor as recalcula; a décima sétima (Fraqueza) é a única que depende de uma escolha do Mestre, e por isso ela é escrita como **obrigação** logo abaixo da tabela:

| Premissa | Valor travado |
|---|---|
| Tamanho do grupo | **4 jogadores**: 2 ofensivos, 1 de suporte, 1 de sustentação |
| Como os 4 turnos do Ciclo são gastos | **1 Habilidade** (um ofensivo) + **2 Ataques Básicos** (o outro ofensivo, mais aquele entre o suporte e a sustentação que **não** estiver cuidando do grupo neste Ciclo) + **1 turno sem dano direto** (cura, buff, remover condição), que **alterna entre o suporte e a sustentação**. Mais a **Ultimate do Ciclo**, que não gasta ação |
| Nível da Habilidade por Ciclo | O que a geração de PH sustenta, pela tabela de 8.2: Nível 2 (faixa 1-4), 0,75×Nível 3 + 0,25×Nível 2 (5-8), Nível 4 (9-12), 0,5×Nível 6 + 0,25×Nível 3 (13-16), 0,5×Nível 7 + 0,25×Nível 3 (17-20) |
| Geração de PH | `2 Ataques Básicos × valor da faixa × taxa de acerto` — a geração é **condicionada ao acerto** (4.5 e 8.2) |
| Ultimate | **1 por Ciclo no grupo**, com a potência de 8.5 (Nível equivalente da faixa) |
| Taxa de acerto usada no cálculo | **70% contra Comum, 60% contra Elite, 55% contra Boss** — já incluindo o efeito do suporte. O DPC publicado é calculado contra o **perfil de Elite (60%)**, que é o caso médio |
| Fraqueza | **A Habilidade e a Ultimate do Ciclo acertam Fraqueza, e 1 dos 2 Ataques Básicos também** — ou seja 3 das 4 ações agressivas, com +2 dados do mesmo tipo, que **não** critam. O outro Ataque Básico é neutro. **Isto é contrato de encontro, não sorte** (ver abaixo) |
| Esquiva | **1 ataque inimigo por Ciclo é Esquivado.** O grupo tem 4 Reações por Ciclo e gasta as outras em Intervir e em Reações de Bênção. O acerto inimigo efetivo fica em **60% nos ataques não Esquivados e 20% no Esquivado**, ou seja **~47% de acerto médio** no encontro típico de 3 ataques por Ciclo |
| Área | O DPC é calculado em **alvo único**. Contra 3 ou mais inimigos, uma Habilidade em área entrega cerca de **1,5 × o dano de alvo único** depois de cortar metade dos dados e respeitar o limite de alvos (10.1: 321 contra 3 alvos, ou 428 contra 4, contra os 219 de alvo único na faixa 17-20) — é por isso que o encontro de 7 Comuns resolve em **2 a 3 Ciclos** e não em 4, e isso é correto, não é desbalanceamento |
| RD do inimigo | **Comum 0 / Elite 2 / Boss 4** (faixas 1-8), **0 / 3 / 6** (9-16), **0 / 4 / 8** (17-20), subtraída de **cada instância** |
| RD do personagem | **0** no cálculo. Quem tiver RD por Bênção ou armadura está acima do orçamento, e isso é margem a favor do grupo |
| Crítico | **5%** das rolagens (20 natural), **dobrando só os dados base** (4.6). Entra como `0,05 × dados base` |
| Tenacidade, **por tipo de inimigo** | **Boss = 2 ×** a redução de Tenacidade do grupo por Ciclo; **Elite = 1 ×**; **Comum = 0,5 ×**, e o resultado é arredondado para número de mesa (a derivação está aberta em 18.3). A de Elite e de Comum é mais baixa de propósito: num encontro de 3 Elites ou 7 Comuns a redução do grupo **se reparte entre eles**, e um Comum que nunca sofre Quebra não participa do subsistema |
| Cadência de Quebra | **1 a cada 2 Ciclos** no perfil de **Boss**; **1 por Ciclo** nos perfis de **Elite** e de **Comum** (consequência direta da linha acima) |
| Ações agressivas do inimigo | Comum **1** por turno; Elite **1** mais uma ação especial a cada 2 Ciclos; Boss **2** por turno (ou 1 ataque + 1 ação especial) |
| Janelas-alvo do inimigo | Acerto do inimigo: **60% contra a Defesa de referência** (Armadura Média), **70% contra o PC de Armadura Leve** e **55% contra o de Pesada** (que em troca não pode Esquivar). Um PC que vira foco aguenta **4 a 7 acertos** antes de chegar a Morrendo — 4 para o mais frágil no começo da faixa, 7 para o mais resistente no fim dela |
| Attrition do grupo | O grupo termina o combate típico de 4 Ciclos com **73% a 81% dos PV**, e chega ao terceiro combate do dia entre **51% e 64%** (contando os dois Descansos Curtos). A conta aberta está em 18.3 |
| Testes de Resistência contra efeitos do inimigo | Um PC com Eficiência e o atributo relevante positivo passa em **55% a 65%**; um PC com o atributo errado passa em **35% a 45%**. É isso que faz valer a pena escolher onde gastar os slots de Eficácia de 4.3. As DTs por tipo e faixa estão em 18.3 |

#### O contrato de encontro da Fraqueza (a única premissa que depende do Mestre)

As outras treze premissas são consequência das regras. Esta é diferente, e por isso ela é escrita como **obrigação**, repetida no capítulo 27:

> **O Mestre monta o encontro de modo que pelo menos 3 dos Elementos do grupo apareçam como Fraqueza entre os inimigos da cena.** Um encontro que não cumpre isso é um encontro **deliberadamente mais duro**, e dura cerca de **1 Ciclo a mais** — o que é uma ferramenta legítima de tensão, desde que o Mestre saiba que está usando ela.

*Por quê como contrato e não como estatística:* o grupo tem **4 Elementos fixos** (9.1) contra **7 Elementos** possíveis e 1-2 / 3 / 4 Fraquezas por tipo de inimigo (9.3). Se as Fraquezas fossem sorteadas, o valor esperado de ações que acertam Fraqueza por Ciclo seria **0,86 contra Comum, 1,71 contra Elite e 2,29 contra Boss** — abaixo da premissa de 3 em todos os casos, e o DPC publicado estaria inflado em 5% a 8%, arrastando junto o orçamento de PV. Só existem duas saídas honestas: baixar o DPC para a média do sorteio, ou transferir a obrigação para quem **pode cumpri-la**. Escolhi a segunda, por três razões: é fiel à origem (em Honkai: Star Rail o jogador monta a equipe olhando as Fraquezas do inimigo, e na mesa é o Mestre que monta o inimigo olhando a equipe), mantém a Quebra acontecendo na cadência que o combate precisa (9.4 dá redução **total** contra Fraqueza e **metade** contra neutro, então a mesma premissa governa dano e Tenacidade), e preserva as 15 células de âncora de 18.3. O custo é uma linha de obrigação no Guia do Mestre — barato.

*O que o Mestre faz quando o encontro é temático e fecha mal:* distribui as Fraquezas entre **vários** inimigos da cena em vez de empilhar no Boss, usa o **Implante de Fraqueza** (9.4) como resposta do grupo, ou aceita o Ciclo extra e avisa a mesa de que aquele bicho é desconfortável de propósito.

**O que essas premissas deixam de fora, de propósito:** buff acumulado de mais de um aliado na mesma rolagem (o teto de 9.6 já limita), Memoespírito (13.1 declara o alvo de 15-25% do dano do dono como margem), **Esforço (só em mesas com Humano, 12)**, Vantagem, acúmulos de Caminho e Efeitos Condicionais de Cone de Luz. Tudo isso é **margem a favor dos jogadores**, e é por isso que o alvo é 3 a 5 Ciclos e não "exatamente 4".

**O que NÃO está mais de fora, e por quê:** a **Esquiva** tem premissa própria na tabela acima. Ela era a única coisa omitida que **todo personagem tem de graça, todo turno**, sem gastar recurso nenhum — e sozinha ela derrubava o dano recebido em um terço e levava a attrition do grupo de 65% para perto de 89% dos PV. Omissão que muda o resultado em um terço não é margem, é erro de modelo.

### 18.2 Âncoras do personagem de referência e o DPC aberto

**Orçamento de ataque do grupo.** O atacante de referência soma Atributo + Eficiência + Especialização de Combate + Bônus Maior de Cone de Luz; o suporte e a sustentação ficam **3 pontos abaixo** (eles investem o Cone e o atributo em outra coisa). A taxa de acerto usa o **ponto médio** da faixa:

| Faixa | Nível de referência | Atributo | Eficiência | Especialização | Cone de Luz | **Atacante** | Suporte/sustentação | **Ponto médio** |
|---|---|---|---|---|---|---|---|---|
| 1-4 | 3 | +5 | +2 | — | +1 | **+8** | +5 | **+6,5** |
| 5-8 | 7 | +5 | +4 | +1 | +1 | **+11** | +8 | **+9,5** |
| 9-12 | 11 | +5 | +5 | +2 | +2 | **+14** | +11 | **+12,5** |
| 13-16 | 15 | +5 | +6 | +2 | +2 | **+15** | +12 | **+13,5** |
| 17-20 | 19 | +5 | +8 | +3 | +3 | **+19** | +16 | **+17,5** |

**Defesa do grupo, com dispersão.** A Defesa tem três colunas pelo mesmo motivo que o PV tem: a escolha de armadura e de Agilidade produz uma faixa de 6 pontos, e esconder isso num número único era mentir sobre quanto dano o personagem de Armadura Leve recebe.

> **Build de referência:** `10 + Bônus de Agilidade típico da faixa + Armadura Média (+5) + Tronco do tier`. O Bônus de Agilidade típico por faixa é **+0 / +2 / +4 / +4 / +5** (um personagem que investe em Agilidade sem fazer dela o atributo principal). As outras duas colunas são a mesma conta trocando a armadura.

| Faixa | **Defesa de referência** (Média) | Mais baixa realista (Leve) | Mais alta (Pesada, **sem Esquiva**) |
|---|---|---|---|
| 1-4 | **16** | 14 | 17 |
| 5-8 | **18** | 16 | 19 |
| 9-12 | **20** | 18 | 21 |
| 13-16 | **21** | 19 | 22 |
| 17-20 | **22** | 20 | 23 |

Contra o Teste de Ataque do inimigo de 18.3, isso dá **60% de acerto contra a referência, 70% contra Leve e 55% contra Pesada** nas cinco faixas. O personagem de Armadura Leve — tipicamente a **Caça**, que já é o menor PV do jogo (212 no nível 20) — é quem recebe 17% mais dano e é exatamente **por ele** que existem a Esquiva (6.3, que a Pesada não pode usar), o Caminho de sustentação e a Reação Intervir. A troca é explícita: a Pesada compra 3 pontos de Defesa e paga com a Reação defensiva e com 2 de Velocidade.

**PV do grupo** (com Bônus de Vigor +2 constante, como em 6.1):

| Faixa | PV típico (N=4) | PV do mais frágil (Caça) | PV do mais resistente (Destruição) |
|---|---|---|---|
| 1-4 | 51-84 | 41-68 | 61-100 |
| 5-8 | 95-128 | 77-104 | 113-152 |
| 9-12 | 139-172 | 113-140 | 165-204 |
| 13-16 | 183-216 | 149-176 | 217-256 |
| 17-20 | 227-260 | 185-212 | 269-308 |

**O DPC, aberto por parcela.** Calculado contra o **perfil de Elite** da faixa (acerto 60%, RD de Elite), arma Média como referência (1d10 → 5d10 no nível 17), Relíquia Mãos no dano de Ataque Básico e Esfera Planar no dano de Elemento:

| Faixa | 2 Ataques Básicos | Habilidade | Ultimate | Crítico (5%) | Quebra ÷ 2 Ciclos | **DPC de referência** |
|---|---|---|---|---|---|---|
| 1-4 | 19 | 26 | 26 | 3 | 14 | **88** |
| 5-8 | 28 | 33 | 35 | 5 | 18 | **119** |
| 9-12 | 33 | 54 | 54 | 8 | 19 | **168** |
| 13-16 | 43 | 62 | 80 | 12 | 21 | **218** |
| 17-20 | 50 | 75 | 106 | 15 | 25 | **271** |

> **O DPC publicado é um DPC de referência, e isso é uma decisão, não um descuido.** As parcelas de **acerto e RD** são do perfil de **Elite** (60%, o caso médio). A parcela de **Quebra** usa a cadência do perfil de **Boss** (1 a cada 2 Ciclos), porque é o Boss que dimensiona 85% do orçamento de PV do encontro e é contra o Boss que o alvo de 3 a 5 Ciclos é verificado. Contra Elite, a Tenacidade mais baixa (18.1) faz a Quebra sair **quase todo Ciclo** e o DPC real sobe para cerca de **300** na faixa 17-20; contra Boss ele cai para cerca de **246**. Essas duas pontas são margem conhecida, e `simular-combate.ps1` (23) imprime as três: o DPC de referência, o puro de Elite e o puro de Boss, comparando **o de referência** contra o publicado.

**A faixa 17-20 aberta número por número**, como modelo de como o apêndice faz as outras quatro:

- **Ataque Básico com Fraqueza:** `5d10 (27) + 5 de atributo + 8 de Relíquia Mãos = 40`; `+2d10 (11)` de Fraqueza = 51; `-4` de RD de Elite = 47; `× 0,60` = **28,2**.
- **Ataque Básico neutro:** `40 - 4 = 36`; `× 0,60` = **21,6**. Os dois somam **49,8**.
- **Habilidade:** Nível 7 = `189 + 5 + 8 de Esfera = 202`, `+2d20 (21)` = 223, `-4` = 219. Nível 3 = `39 + 5 + 8 = 52`, `+2d12 (13)` = 65, `-4` = 61. Pela tabela de PH de 8.2, `0,5 × 219 + 0,25 × 61 = 124,75`; `× 0,60` = **74,9**.
- **Ultimate:** `147 + 5 + 8 = 160`, `+21` = 181, `-4` = 177; `× 0,60` = **106,2**.
- **Crítico:** dados base no Ciclo = `27 + 27 + (0,5 × 189 + 0,25 × 39) + 147 = 305`; `× 0,05` = **15,3**.
- **Quebra, com o Elemento certo e com RD:** o exemplo usa **Fogo**. Dano de Quebra = `2d6 (7) + 2 × 8 = 23`, **menos 4 de RD de Elite = 19** (Dano de Quebra é instância de dano por 6.4, logo sofre RD). Mais 2 turnos de **Queimadura** = `(2d6 (7) + 8) × 2 = 30`, que **ignora RD** por ser Dano Contínuo (9.5). Total **49** a cada 2 Ciclos = **24,5**.
- **Soma: 270,7** → DPC de referência publicado **271**.

> **Nota de Elemento, porque o erro é fácil de repetir:** Fogo produz **Queimadura** e Físico produz **Sangramento** (9.4 e 9.6). Os dois têm o **mesmo** Dano de Quebra (`2d6 + 2 × Eficiência`), então trocar um pelo outro não muda os 23 — mas muda o efeito contínuo, e muda a conta: contra um Elite de 361 PV, o Sangramento daria `5% × 361 = 18` por turno (dentro do teto de `3 × Eficiência` = 24), ou 36 em dois turnos, e o total por Quebra seria 55 em vez de 49. O apêndice 29 abre as duas versões; a tabela acima é a de **Fogo**.

*Por quê a curva do DPC é mais suave do que a curva de dano:* entre a faixa 1-4 e a 17-20 o dano de uma única Habilidade multiplica por 9 (21 → 189), mas o DPC só multiplica por 3. O freio é o **custo em PH** (8.2): quanto maior o Nível da Habilidade, menos vezes por combate ela sai. Esse é o mecanismo que mantém o combate em 4 Ciclos em todas as faixas sem precisar de Bosses com milhares de PV — e é por isso que a economia de PH não é detalhe de sabor, é a espinha do balanceamento.

*O que isso corrige da iteração 1:* o DPC publicado na primeira versão (110/180/250/360/500) não era reproduzível a partir das regras do documento e superestimava o dano real em até 80% na faixa alta, porque contava Habilidade de topo por Ciclo e não contava RD inimiga. Os valores da iteração 2 (90/120/170/220/275) vieram da conta aberta acima.

*O que a iteração 3 ajustou:* a parcela de Quebra passou a **sofrer RD** (6.4 define Dano de Quebra como instância de dano, e a premissa de RD manda subtrair de cada instância) e o exemplo passou a usar o Elemento **certo**. Isso baixou o DPC em 1% a 2% — de 90/120/170/220/275 para **88/119/168/218/271**. As âncoras de inimigo de 18.3 **não mudaram**, porque elas são arredondamentos legíveis de `DPC × 4` e continuam a menos de 3% do valor derivado (a maior divergência é o Elite da faixa 1-4: 120 publicado contra 117 derivado). Mudar 15 células para ganhar 2% de precisão num orçamento cuja tolerância de verificação é 5% seria churn, não rigor — mas **a divergência tinha que estar escrita**, e agora está.

### 18.3 Âncoras do inimigo (base do bestiário, capítulo 28)

Tudo nesta tabela é derivado do DPC de 18.2. **Orçamento do encontro = DPC × 4**; Comum vale 1/7 dele, Elite 1/3, Boss 85%. Os valores de PV estão **arredondados para números legíveis** e ficam a menos de 3% do valor derivado.

| Faixa | PV Comum | PV Elite | PV Boss | Defesa C / E / B | **RD C / E / B** | Tenacidade C / E / B | **VEL C / E / B** | Ataque do inimigo | Dano por acerto | **DT dos efeitos C / E / B** | Fraquezas C / E / B |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-4 | 50 | 120 | 305 | 13 / 15 / 16 | **0 / 2 / 4** | 4 / 9 / 18 | **11 / 12 / 13** | +7 | 10 | **12 / 13 / 14** | 1-2 / 3 / 4 |
| 5-8 | 70 | 160 | 410 | 16 / 18 / 19 | **0 / 2 / 4** | 4 / 10 / 20 | **12 / 13 / 15** | +9 | 20 | **14 / 15 / 16** | 1-2 / 3 / 4 |
| 9-12 | 95 | 225 | 580 | 19 / 21 / 22 | **0 / 3 / 6** | 5 / 11 / 22 | **13 / 15 / 16** | +11 | 28 | **16 / 17 / 18** | 1-2 / 3 / 4 |
| 13-16 | 125 | 295 | 750 | 20 / 22 / 23 | **0 / 3 / 6** | 5 / 11 / 22 | **14 / 16 / 18** | +12 | 36 | **17 / 18 / 19** | 1-2 / 3 / 4 |
| 17-20 | 155 | 365 | 935 | 24 / 26 / 27 | **0 / 4 / 8** | 6 / 12 / 24 | **15 / 17 / 19** | **+13** | 48 | **19 / 20 / 21** | 1-2 / 3 / 4 |

**Por quê a Tenacidade tem três valores diferentes e não um múltiplo só, e de onde vem cada número.** Pela fórmula por tipo de 18.1, com o mix de ações publicado, a **redução de Tenacidade do grupo por Ciclo** é `1 + 1` (os dois Ataques Básicos) `+` o Nível da Habilidade sustentável pelo PH `+ 5` (Ultimate), ou seja **9 / 9,75 / 11 / 10,75 / 11,25** nas cinco faixas. Aplicando os multiplicadores:

| | 1-4 | 5-8 | 9-12 | 13-16 | 17-20 |
|---|---|---|---|---|---|
| Comum, `0,5 ×` derivado | 4,5 | 4,9 | 5,5 | 5,4 | 5,6 |
| Elite, `1 ×` derivado | 9 | 9,8 | 11 | 10,8 | 11,3 |
| Boss, `2 ×` derivado | 18 | 19,5 | 22 | 21,5 | 22,5 |
| **Publicado (C / E / B)** | **4 / 9 / 18** | **4 / 10 / 20** | **5 / 11 / 22** | **5 / 11 / 22** | **6 / 12 / 24** |

A coluna publicada é o valor derivado **arredondado para número de mesa**: inteiro pequeno, monotônico e fácil de riscar num papel. A redução do grupo oscila (11 na faixa 9-12, 10,75 na 13-16) porque o Nível de Habilidade sustentável pelo PH oscila, e publicar essa oscilação faria o Mestre consultar duas casas decimais no meio do combate. Dois desvios merecem estar escritos: o **Comum é um pouco mais frágil** que o derivado (4 contra 4,5), de propósito — um Comum existe para sofrer Quebra, e a Quebra é o que faz um pelotão parecer um pelotão; e o **Boss da faixa 17-20 é um pouco mais duro** (24 contra 22,5), o que lhe dá cerca de meio Ciclo a mais de barra, também de propósito, porque é o inimigo que fecha a campanha.

Na prática: contra Boss a Quebra sai a cada ~2 Ciclos; contra Elite, quase todo Ciclo; contra Comum, no primeiro ataque sério que ele receber.

**Por quê a VEL do inimigo é essa.** Ela foi calibrada contra a faixa de VEL de personagem de 6.5, com uma regra de projeto: **a Caça equipada age antes de todo Comum e Elite da faixa dela**, e disputa a primeira casa com o Boss. Um Boss de faixa 17-20 tem VEL 19; uma Caça de nível 19 com Agilidade 20, Bônus de Caminho +4 e Botas IV chega a 24. A promessa do Caminho é verdadeira na mesa. Na outra ponta, uma Preservação de Armadura Pesada fica em 13 ou menos e age depois de quase todo mundo — o que é a identidade dela, não um castigo.

**Por quê a DT dos efeitos do inimigo é essa.** É `8 + atributo + Eficiência da faixa` resolvido para um atributo de inimigo plausível, e ela entrega a janela de 18.1: um PC com Eficiência e o atributo relevante positivo passa em **55% a 65%**; um PC com o atributo errado, em **35% a 45%**. Sem essa coluna, o Mestre não tinha número para o campo que a ficha padronizada exige, e os 6 Testes de Resistência do grupo ficavam sem contraparte.

**As três janelas, verificadas nas cinco faixas:**

- **Acerto do grupo:** o ponto médio de 18.2 contra estas Defesas dá **70% contra Comum, 60% contra Elite, 55% contra Boss** em **todas** as faixas. Não há faixa fora da janela.
- **Acerto do inimigo:** o Teste de Ataque do inimigo contra a **Defesa de referência** do PC precisa de **9 ou mais no d20** nas cinco faixas, ou seja **60%** cravado. Contra Armadura Leve são 7 ou mais (**70%**); contra Pesada, 10 ou mais (**55%**). O ataque da faixa 17-20 é **+13** e não +14 justamente para fechar isso com a Defesa de referência 22 de 18.2.
- **Ciclos até a resolução:** recalculando o DPC contra o perfil de Boss (RD maior, acerto 55%, 4 Fraquezas, Quebra a cada 2 Ciclos), o grupo entrega ~83 por Ciclo na faixa 1-4 e ~246 na 17-20 — contra 305 e 935 de PV, dá **3,7 e 3,8 Ciclos**. Dentro do alvo, com folga para os dois lados.

**Composição do encontro.** Um encontro típico gasta o orçamento inteiro: **1 Boss + 1 Comum**, ou **1 Elite + 4 Comuns**, ou **3 Elites**, ou **7 Comuns**. Encontro que gasta metade do orçamento é uma cena de passagem e deve durar 2 Ciclos — isso é correto, não é erro de balanceamento. E, pela premissa de Área de 18.1, **encontros de 3 ou mais inimigos resolvem mais rápido** (2 a 3 Ciclos) do que o encontro de Boss: é o preço de colocar sete alvos na frente de uma Habilidade em área, e é a razão de existir o Caminho da Erudição.

**Attrition esperada, com a Esquiva dentro do modelo.** O encontro típico de 4 Ciclos entrega **3 ataques inimigos por Ciclo** (Boss 2 + Comum 1), e pela premissa de Esquiva de 18.1 um deles é Esquivado: acerto efetivo `0,60 + 0,60 + 0,20`, ou **1,4 acerto por Ciclo**. Multiplicando pelo dano por acerto e por 4 Ciclos:

| Faixa | Nível de referência | PV do grupo (4 × típico) | Dano recebido em 4 Ciclos | **Grupo termina com** | (sem a Esquiva seria) |
|---|---|---|---|---|---|
| 1-4 | 3 | 292 | 56 | **81%** | 75% |
| 5-8 | 7 | 468 | 112 | **76%** | 69% |
| 9-12 | 11 | 644 | 157 | **76%** | 69% |
| 13-16 | 15 | 820 | 202 | **75%** | 68% |
| 17-20 | 19 | 996 | 269 | **73%** | 65% |

> **Janela publicada: o grupo termina um combate típico com 73% a 81% dos PV**, perdendo entre um quinto e um quarto do total. A iteração anterior publicava 50-70% porque a Esquiva estava fora do modelo; com ela dentro, o número verdadeiro é este, e publicar o número verdadeiro é o ponto.

**Então por que existe um Caminho de sustentação?** Porque a média de um combate é a métrica errada para decidir isso, e o capítulo 27 precisa dizer as quatro razões em voz alta:

1. **Foco.** O inimigo escolhe o alvo, e a Esquiva protege **um** ataque, de **um** personagem, por Ciclo. Um personagem que vira foco cai em **4 a 7 acertos**: 4 para uma Caça no começo da faixa, 5 para o personagem típico, 7 para uma Destruição no fim dela. Um Boss que decide concentrar dois ataques por turno em quem tem menos PV derruba esse personagem em **2 Ciclos**, e a média do grupo nem percebe.
2. **Dano Contínuo.** Ele **ignora RD** e não admite Esquiva (9.5), aplica no início do turno do alvo e é a fonte que mais cresce nas faixas altas. Nada na ficha defende contra ele a não ser cura.
3. **Ações especiais de Boss.** A premissa de 18.1 conta "2 ataques por turno ou 1 ataque + 1 ação especial"; a ação especial é o pico de dano que a média esconde, e é o momento em que o grupo precisa de uma Ultimate de cura pronta.
4. **O dia, não o combate.** O relógio real é a cadeia: **três combates típicos** somam 57% a 81% do PV total do grupo, e os dois Descansos Curtos do dia devolvem cerca de 30%. O grupo chega ao terceiro combate entre **51% e 64%** — e é aí que a conta vira, não no primeiro.

É a soma dessas quatro, e não a média de um combate, que o Guia do Mestre usa para montar uma sessão.

**Ficha de inimigo padronizada** (lacuna L21, capítulo 28), campo por campo: Nome; Nível; Tipo (Comum/Elite/Boss); PV; Defesa; **Velocidade** (coluna VEL acima); **Tenacidade (valor máximo)**; **Fraquezas e Resistências** (é isso que determina quanta Tenacidade ele perde por 9.4); RD; Teste de Ataque; dano e Elemento de cada ataque; **DT dos efeitos dele** (coluna acima, derivada de `8 + atributo + Eficiência da faixa`); 1 a 3 ações especiais; e o comportamento na Fila (VEL e se tem Firmeza). **Todos os campos da ficha têm coluna na tabela de âncoras acima** — nenhum campo obriga o Mestre a inventar número.

**Inimigos não acumulam Energia e não têm Ultimate.** A ficha não tem campo de Energia. O equivalente à Ultimate de um Boss é uma **ação especial com recarga contada em Ciclos**, declarada na ficha dele ("uma vez a cada 3 Ciclos"). É simplificação deliberada: o Mestre já rastreia a Fila, a Tenacidade e as condições de todo mundo.

**Elite e Boss têm Firmeza** (7.4): some todas as casas de Atraso do Ciclo, divida por 2 arredondando para baixo (mínimo 1 casa **no total do Ciclo**, não por fonte) e aplique o **teto de 2 casas**. E, por 7.6, **Elite e Boss não perdem o turno por Congelamento** — eles são Atrasados em 2 casas e perdem a ação especial do turno seguinte. As duas regras existem para a mesma coisa: a premissa de 18.1 assume o Boss agindo em **todos** os Ciclos, e um Boss que passa metade do combate fora da Fila não é um combate.

**Teto de RD do inimigo:** vale a mesma regra do personagem (6.4), lendo a Eficiência da faixa do inimigo. Nenhum valor desta tabela chega perto do teto, e isso é de propósito — RD alta transforma Ataque Básico em ação inútil e quebra a geração de PH.

### 18.4 DT por faixa e Sucesso Automático (override: inflação de bônus)

Com Eficácia +16 e atributo +5, um especialista de nível 20 soma **+21** em uma Perícia. Uma tabela de DT fixa viraria decoração.

> **Esta é a única tabela de DT GERAL do livro.** A de 4.2 é a mesma coluna da faixa 1-4, publicada no capítulo 02 como exemplo de leitura. Em caso de dúvida sobre a dificuldade de uma ação, vale esta.
>
> **Os cinco subsistemas com DT própria vencem esta tabela** (lista fechada, repetida em 4.2): descobrir Fraqueza (9.3), Surpresa DT 13 (7.3), Morrendo DT 10 (15.1), Raposa Astuta DT 10 e To na sua mente DT 13 (12). Eles existem porque são **rotinas**, não feitos: um teste que o grupo precisa conseguir fazer todo combate não pode escalar com a faixa, senão o subsistema morre na faixa alta. Nenhum capítulo cria um sexto.

| Dificuldade | 1-4 | 5-8 | 9-12 | 13-16 | 17-20 |
|---|---|---|---|---|---|
| **Trivial** | **8** | **9** | **10** | **11** | **12** |
| Fácil | 10 | 12 | 14 | 16 | 18 |
| Média | 13 | 16 | 19 | 22 | 25 |
| Difícil | 16 | 19 | 23 | 27 | 30 |
| Muito Difícil | 19 | 23 | 27 | 31 | 35 |
| Heroica | 22 | 26 | 31 | 34 | 38 |

Três regras acompanham a tabela, e sem elas ela machuca mais do que ajuda:

- **A faixa é do desafio, não do personagem.** Um muro é um muro: escalar continua **DT 13** (Média da faixa 1-4) no nível 20. Use a faixa alta para desafios que **só existem** naquele patamar de jogo — selar um Stellaron, hackear o núcleo de uma nave de guerra, convencer um Emanador.
- **Sucesso Automático, só em Teste de Perícia:** se o seu bônus total for **igual ou maior que a DT**, não role. Você consegue. **Teste de Ataque e Teste de Resistência são sempre rolados**, porque o 20 e o 1 naturais têm efeito próprio (4.5, 4.6): não rolar um ataque apagaria o acerto crítico e o erro crítico, e não rolar um Teste de Resistência tiraria do efeito a chance de pegar.
- **Teste sem Eficiência contra DT de faixa alta é exceção.** Se o Mestre pedir, deve conceder Vantagem por preparação, ajuda de aliado ou equipamento adequado. Perícia não treinada não foi feita para vencer desafio de faixa 17-20.

### 18.5 Onde as contas finais moram

Este design fixa o **método**, as **17 premissas** (18.1), o **DPC de referência aberto** (18.2) e as **âncoras de inimigo** (18.3) — ou seja, tudo que a escrita precisaria adivinhar. O apêndice `29-apendices-e-fichas.md` traz, durante a escrita:

- as **outras quatro faixas** abertas parcela por parcela no formato da faixa 17-20 de 18.2;
- a parcela de Quebra aberta nas **duas versões de Elemento** (Fogo com Queimadura e Físico com Sangramento), para a faixa-modelo não propagar o Elemento errado;
- as **fichas de inimigo de exemplo** em cada faixa (Comum, Elite e Boss), preenchendo todos os campos da ficha padronizada a partir das colunas de 18.3;
- os **três combates de referência** simulados Ciclo por Ciclo (faixas 1-4, 9-12 e 17-20), provando o alvo de 3 a 5 Ciclos e a attrition de 73-81% **com a Esquiva em jogo**;
- um **dia de referência** com três combates e dois Descansos Curtos, provando a janela de 51-64% que justifica o Caminho de sustentação;
- um **cenário de foco**, em que o Boss concentra os ataques no personagem de menor PV, mostrando que ele chega a Morrendo em 2 Ciclos;
- um **encontro de 7 Comuns** simulado, provando a premissa de Área (2 a 3 Ciclos).

A verificação automatizada está em 23: `simular-combate.ps1` recebe as 17 premissas como parâmetros e **reprova** qualquer faixa que saia da janela de 3 a 5 Ciclos, da attrition de 70-85% por combate, da de 45-70% no terceiro combate do dia, ou de 5% de divergência contra o DPC de referência publicado.

---

## 19. Invariantes do sistema e quem os guarda

Cada invariante tem **uma** camada dona. Se duas camadas tentarem garantir a mesma coisa, uma delas vai esquecer — e é assim que nasce combo quebrado.

| Invariante | Camada dona | Por que é essa camada |
|---|---|---|
| Eficácia nunca entra em Teste de Ataque | Capítulo 02 (regras gerais) | É regra de resolução; se morasse em cada Habilidade, cada jogador reinventaria |
| Toda instância de dano causa no mínimo 1 | Capítulo 02 | Vale para RD, Resistência, divisão e área ao mesmo tempo |
| Arredondamento sempre para baixo | Capítulo 02 | Única regra aritmética do livro |
| Teto de RD = 2 + (2 × Eficiência) | Capítulo 18 (Combate) | A RD só existe em combate; o Mestre consulta no mesmo lugar onde resolve dano |
| Teto de Atraso (3 casas contra Comum, 2 contra Elite/Boss) e a **ordem de operação da Firmeza** (somar o Ciclo, dividir, mínimo, teto) | Capítulo 19 (Fila de Ação) | A Fila é a única estrutura que conhece as casas, e a ordem de operação só faz sentido ao lado delas |
| Elite e Boss não perdem o turno por Congelamento | Capítulo 19 | Perder o turno é um fato da Fila, não do Elemento. O capítulo 20 descreve o efeito e aponta para cá |
| Avanço Total: 1 por Ciclo por criatura | Capítulo 19 | Idem |
| **Área: até 3 alvos (4 nos Níveis 6 e 7), teto absoluto de 6** | Capítulo 16 (Habilidades) | A área é propriedade da Habilidade; o combate e o equipamento só consomem a regra |
| **A Esquiva soma sempre Eficiência, nunca Eficácia** | Capítulo 18 (Combate) | É onde a Esquiva mora, e é a única Reação com número no orçamento |
| **O Teste de Morrendo não soma Eficiência** | Capítulo 23 (Dano, cura e morte) | Exceção única à fórmula de 14; fica ao lado do estado que ela governa |
| **As cinco DTs de subsistema vencem a tabela geral; não existe uma sexta** | Capítulo 27 (Mestre) | Quem publica a tabela geral é quem precisa declarar as exceções dela |
| Tenacidade restaura no fim do próximo turno do alvo | Capítulo 20 (Elementos) | Tenacidade e Quebra são um subsistema fechado |
| Dano Contínuo ignora RD, não crita, não ganha dados de Fraqueza | Capítulo 20 | As três exceções ficam juntas, numa frase |
| Máximo de 5 acúmulos de uma mesma condição | Capítulo 21 (Condições) | O catálogo é a lista única de condições |
| Teto de bônus somado (+3 / +4 / +5 por faixa), **teto de penalidade somada (-3 / -4 / -5)** e o que entra em cada um | Capítulo 26 (Progressão) | Só a progressão conhece a faixa de nível, e os dois tetos são a mesma regra lida nos dois sentidos |
| Teto de PV temporários = 3 × Eficiência, de qualquer fonte, sem acumular | Capítulo 23 (Dano, cura e morte) | É onde cura, barreira e PV temporário se resolvem |
| Só inimigos têm Tenacidade; personagem não é Quebrado | Capítulo 20 (Elementos) | A Tenacidade é um subsistema fechado e é lá que se diz de quem ela é |
| Potência da Ultimate por faixa (Nível equivalente) | Capítulo 17 (Ultimate) | A Ultimate não tem Nível próprio; quem indexa a faixa é o capítulo dela |
| Sucesso Automático só em Teste de Perícia | Capítulo 27 (Mestre) | Nasce com a tabela de DT por faixa, que mora lá |
| Progressão por marco narrativo, sem XP | Capítulo 26 | É a porta de entrada de todo ganho de nível |
| Máximo de 8 Habilidades conhecidas; Nível máx. por nível | Capítulo 26 | É limite de progressão, não de combate |
| PH: máximo e geração por faixa | Capítulo 16 (Habilidades) | O PH só é gasto e gerado ali |
| 1 Ultimate por Ciclo; 100 de Energia | Capítulo 17 (Ultimate) | |
| Atributo nunca passa de 15 na criação nem de 20 depois | Capítulo 03 (Criação) | A criação é a única porta de entrada de valores de atributo |
| Lista de efeitos proibidos em Habilidades criadas | Capítulo 16 + Capítulo 27 (Mestre) | Dupla intencional: o jogador lê o limite, o Mestre lê o procedimento |

---

## 20. Estrutura de capítulos do livro

Arquivos em `livro-v1.0/`, prefixo numérico definindo a ordem de montagem. 31 arquivos.

| Arquivo | Conteúdo |
|---|---|
| `00-capa-e-creditos.md` | Capa, nome oficial, autoria MC Filhos, versão 1.0, aviso de obra de fã |
| `01-introducao.md` | O que é Explorando Galáxias, o universo, o que você precisa para jogar, o que mudou da v0.1 |
| `02-como-jogar.md` | d20, Teste, DT (exemplo de leitura e a **lista fechada das cinco DTs de subsistema**), Eficiência/Eficácia, Vantagem/Desvantagem, arredondamento, dano mínimo, precedência de regras, **falhe para frente**, Regra de Ouro |
| `03-criacao-de-personagem.md` | Passo a passo, array oficial, Compra de Pontos, Propósito de Vida, Elemento, Atributo de Habilidade |
| `04-atributos-e-pericias.md` | 6 Atributos, tabela de Bônus, aumentos por nível, 18 Perícias, Sintonia |
| `05-racas.md` | 7 Raças, traços padronizados, Esforço |
| `06-caminhos-visao-geral.md` | Os 9 Caminhos, PV, N, Velocidade, Perícias, como ler uma Bênção |
| `07-caminho-destruicao.md` | 12 Bênçãos (10 da v0.1 + 2 novas de tier alto) |
| `08-caminho-inexistencia.md` | 12 Bênçãos (10 + 2), Corrupção, Dano Contínuo, Implante de Fraqueza |
| `09-caminho-harmonia.md` | 12 Bênçãos (10 + 2), Ritmo Acelerado, buffs de grupo |
| `10-caminho-abundancia.md` | 12 Bênçãos (10 + 2), cura, barreira, Excesso de Vida |
| `11-caminho-recordacao.md` | 12 Bênçãos (10 + 2) + Guia e ficha do Memoespírito |
| `12-caminho-erudicao.md` | **Novo:** identidade, 12 Bênçãos, Acúmulos de Cálculo |
| `13-caminho-euforia.md` | **Novo:** identidade, 12 Bênçãos, Tabela do Riso |
| `14-caminho-caca.md` | **Novo:** identidade, 12 Bênçãos, crítico 19-20, marcação de presa |
| `15-caminho-preservacao.md` | **Novo:** identidade, 12 Bênçãos, Barreira, Reações defensivas |
| `16-habilidades.md` | Criação, Níveis 1-7, tabelas de dano/cura/alcance/buff/debuff/passiva, **regra de área com número de alvos (10.1)**, PH, checklist de validação com a lista de efeitos proibidos |
| `17-ultimate-e-energia.md` | Ultimate, 100 de Energia, fontes, 1 por Ciclo, **tabela de potência por faixa com o Nível equivalente (8.5)**, criação e validação da Ultimate |
| `18-combate.md` | 4 Ações + Reação, Teste de Ataque e **as 6 categorias de arma com o Atributo de cada**, crítico (faixa 19-20 como teto), dano, RD, **Esquiva (sempre Eficiência)**, Intervir, Distâncias, armas |
| `19-fila-de-acao-e-velocidade.md` | Velocidade, Fila, casas, Ciclo, Atrasar, **Firmeza (ordem de operação e teto por tipo)**, Avançar, Avanço Total, **Congelamento e a Firmeza contra ele**, **Surpresa (DT 13 fixa)**, casos-limite, Trilha de Ação |
| `20-elementos-tenacidade-e-quebra.md` | 7 Elementos, Fraquezas, Resistências, Tenacidade, Quebra, Dano de Quebra, Dano Contínuo |
| `21-condicoes.md` | Catálogo completo de condições |
| `22-testes-de-resistencia.md` | Os 6 Testes, atributos, quando o Mestre pede |
| `23-dano-cura-e-morte.md` | Cura, PV temporários, **Morrendo (Força de Vontade DT 10, sem Eficiência — a exceção declarada)**, Executado, Descanso Curto e Longo |
| `24-equipamentos.md` | Armaduras, armas, itens, poções, inventário e Espaço, criação de itens |
| `25-cones-de-luz-e-reliquias.md` | Cones de Luz, Sobreposição, 6 slots de Relíquia, conjuntos 2/4 peças |
| `26-progressao-e-ressonancias.md` | Tabela mestra 1-20, **como se sobe de nível (marco narrativo, 17.1)**, Eficácia, **Especialização de Combate (mecânica nova)**, **os dois tetos: bônus somado e penalidade somada**, Ressonâncias I-IV |
| `27-guia-do-mestre.md` | DT por faixa e as **cinco DTs de subsistema**, Sucesso Automático, montar encontro, **o contrato de encontro da Fraqueza (18.1)**, orçamento de PV, revelar Fraquezas, cadeia de combates entre Descansos, aprovar criação de jogador, Ficha de Decisões da Mesa |
| `28-bestiario.md` | Ficha padronizada + inimigos de exemplo (Comum/Elite/Boss) nas 5 faixas |
| `29-apendices-e-fichas.md` | Ficha de personagem, ficha do Memoespírito, Trilha de Ação, referência rápida, apêndice de balanceamento |
| `30-glossario.md` | Todos os termos oficiais em ordem alfabética, incluindo **falhe para frente**, mais os termos **aposentados** da v0.1 com o nome novo ao lado (é um capítulo isento do checador de nomenclatura, ver 23) |

### 20.1 As 22 lacunas e onde cada uma é resolvida

| # | Lacuna da v0.1 | Decisão | Capítulo(s) |
|---|---|---|---|
| L01 | Ordem de turno, Ciclo e "casas" nunca definidos (~15 referências órfãs) | Fila de Ação com casas, Atrasar/Avançar, Ciclo, Firmeza com ordem de operação | **19**, 20, 07-15 |
| L02 | Velocidade não existe como estatística | `VEL = 10 + Agilidade + Caminho + equipamento` | **19**, 06, 25, 26 |
| L03 | Acerto crítico usado sem regra | 20 natural (19-20 só na Caça, teto do jogo), dobra só dados base, Fraqueza não crita | **18**, 14 |
| L04 | Teste de Ataque não formalizado | d20 + atributo + Eficiência vs Defesa; atributo por categoria; DT 8+atr+Ef | **18**, 16 |
| L05 | Vantagem/Desvantagem sem regra | 2d20 maior/menor, não acumulam, cancelam por presença | **02** |
| L06 | RD sem regra nem teto | Por instância, soma até teto `2 + 2×Eficiência`, mínimo 1 de dano | **18**, 24 |
| L07 | Tabela de Bônus de Atributo não monotônica | Tabela nova 8-20, 15 = +3, 13 = +1 | **04** |
| L08 | Esquiva conta Agilidade duas vezes | Reação: Defesa + Eficiência (sempre, nunca Eficácia); Pesada não esquiva; premissa própria no orçamento | **18**, 27 |
| L09 | PV de nível 1 oscilante (2d20-6d20) e achatado por nível | PV fixo por Caminho, incremento com N, variante de rolagem com piso e teto | **06**, 26 |
| L10 | Compra de Pontos prometida e não entregue | 28 pontos, custo crescente, equivalente ao array | **03** |
| L11 | Tenacidade só reduzível com Fraqueza (punitivo) | Total / metade / 1 ponto + Implante de Fraqueza + revelar Fraquezas | **20**, 08, 27 |
| L12 | Sem aumentos de Atributo por nível | +2 (ou +1/+1) nos níveis 3, 6, 9, 12, 15, 18; teto 20 | **04**, 26 |
| L13 | Energia de Ultimate com fontes incompletas | +10 ao sofrer dano, +10 ao derrotar, +10 ao Quebrar | **17** |
| L14 | Sem tabela mestra de progressão | Tabela 1-20 completa | **26** |
| L15 | Sem equipamento icônico de HSR | Cones de Luz, 6 slots de Relíquia, conjuntos, Ressonâncias I-IV | **25**, 26 |
| L16 | Sem passe de balanceamento | Método em 4 passos + premissas publicadas (incluindo Esquiva, Área e o contrato de Fraqueza) + DPC de referência aberto por parcela + âncoras por faixa com VEL e DT de efeitos + apêndice | **27**, 28, 29 |
| L17 | 4 Caminhos sem Bênçãos (Erudição, Euforia, Caça, Preservação) | 12 Bênçãos cada, identidade mecânica travada | **12, 13, 14, 15** |
| L18 | Economia de ações ambígua; Habilidade sem espaço de ação; **dano em área sem número de alvos** | Habilidade ocupa o Ataque Básico; 4 Ações + 1 Reação; PH; **área = metade dos dados e até 3 alvos (4 nos Níveis 6 e 7, teto 6)** | **18**, **16** |
| L19 | Sem catálogo de condições; durações vagas; frases sem subsistema ("o alvo demorará mais um turno") | Catálogo fechado, duração em turnos do alvo, tabela de normalização em 7.9 | **21**, 20 |
| L20 | "Uma vez por descanso" sem definir descanso | Descanso Curto e Longo | **23** |
| L21 | Sem ficha de inimigo, bestiário ou DTs de referência | Ficha padronizada com **todos** os campos tendo coluna de âncora (incluindo VEL e DT dos efeitos), bestiário em 5 faixas, DT por faixa | **27**, **28** |
| L22 | Inconsistências numéricas e de nomenclatura herdadas | **31 correções pontuais** (20.2) + convenção de nomes dividida em strings proibidas e uso incorreto (3.1, 3.2) | todos |

### 20.2 Erros concretos a corrigir (31)

| # | Erro na v0.1 | Correção | Capítulo |
|---|---|---|---|
| E01 | Título com "(provavelmente vou mudar o nome)" | Nome oficial: Explorando Galáxias | 00, 01 |
| E02 | 13 → +2 e 14 → +2 (não monotônico) | Tabela nova (5.1) | 04 |
| E03 | Esquiva = Defesa + Agilidade (dupla contagem) | Defesa + Eficiência | 18 |
| E04 | PV nível 1 pode sair 2 (Caça, 2d20) | PV fixo | 06 |
| E05 | 1d20 por nível para todos achata os Caminhos | Incremento `5 + N + Vigor` (fórmula em 6.1) | **06** |
| E06 | Médias erradas nas tabelas de Habilidade (18/25/36/60/100) | **21/27/39/63/105** (média `floor`, ver 3 e 10.1) | 16 |
| E07 | Cura de Nível 5 = "toda a Vida" | 10d20 ou 5d20 em área | 16 |
| E08 | "Como ação bônus" (Olhar da Ausência) | Ação Complementar | 08 |
| E09 | "Ação comum" e "ação completa" sem definição (6+ ocorrências) | Linguagem das 4 Ações | 18, 07-15 |
| E10 | Dano de Quebra de 6d4 a 1d2 (12x de diferença) | Tabela escalada por Eficiência (9.4) | 20 |
| E11 | 10 RD na Armadura Pesada e em 8 Bênçãos | 2 RD + teto de RD + conversões (11.4) | 18, 24, 07-15 |
| E12 | "Não pode reduzir Tenacidade sem Fraqueza" | Redução em três níveis | 20 |
| E13 | Teste de Atenção exclusivo dos Vulpes | Teste de Percepção Mental DT 10 | 05, 22 |
| E14 | Executado sem Teste nem DT definidos | Força de Vontade DT 10, **sem Eficiência** (exceção única, 14), 3 sucessos / 3 falhas | 23 |
| E15 | Haloviano com "1-10 falha, 11-20 sucesso" | Teste de Sintonia DT 13 + **Teste de Força de Vontade** do alvo contra a sua DT (12) | 05 |
| E16 | "+2 em algum atributo" sem teto | Máx 15 na criação, 20 depois | 03, 05 |
| E17 | Perícias = "2 + Sincronia" pode dar 1 | Mínimo 2 | 04 |
| E18 | Sintonia com dois atributos simultâneos | Escolha fixa na criação | 04 |
| E19 | Energia excedente perdida, sem regra de declaração | Ultimate não gasta ação, 1 por Ciclo | 17 |
| E20 | "Uma vez por descanso" sem definição | Descanso Curto/Longo | 23 |
| E21 | Inventário em "Espaço" sem capacidade | `10 + 2 × Poder` | 24 |
| E22 | Poções curam 1d20/2d20/3d20 | 15 / 30 / 50 fixos | 24 |
| E23 | Avatar com requisito nível 5, potência de capstone | Requisito nível 17 | 07-15 |
| E24 | Acúmulos e marcas sem teto global | Teto por faixa (+3/+4/+5) e 5 acúmulos | 21, 26 |
| E25 | Bênçãos com "+10", "-10", "15 RD", "+4 de Defesa", "+5 RD", "+20 de PV", "+5 no teste de ataque", "ignora 5 de defesa", "50% mais de dano", "1d10/1d12" fora de escala | Régua de conversão de **25 linhas** (11.4) | 07-15 |
| E26 | Memoespírito sem ficha | Ficha completa (13.1) | 11 |
| E27 | Faixa de níveis nunca declarada | **Nível 1 a 20**, explícito | 01, 26 |
| E28 | Nomes de Teste de Resistência usados de forma confusa | 6 nomes oficiais + atributo de cada | 22 |
| E29 | Frases que soam como regra e não têm subsistema: "o alvo demorará mais um turno" (Silêncio da Existência, Erosão Mental), "tem dificuldade para conjurar habilidades poderosas" | Traduzidas para a condição **Silenciado** do catálogo (9.6), via tabela de normalização (7.9) | 08, 21 |
| E30 | *Aniquilador de Resistências* cria uma fórmula de DT própria ("o DT será o acerto do seu Ataque -8") | **DT = 8 + Bônus do Atributo de Habilidade + Eficiência** (4.2). Não existe DT derivada de uma rolagem no livro | 07 |
| E31 | Dano em área sem número de alvos nem escala (a v0.1 fala de área em 5 Bênçãos e não define nenhuma) | Até 3 alvos, 4 nos Níveis 6 e 7, teto absoluto de 6 (10.1) | 16, 12 |

### 20.3 Mapa de imagens

Posição confirmada abrindo o `.docx` da v0.1 e lendo a ordem real de `document.xml` (script `scripts/map-imagens.ps1`). Cada Caminho da v0.1 tem **duas** imagens: o símbolo (quadrado, ~100-165 KB) e a arte do Aeon.

| Arquivo | Dimensões | Onde estava na v0.1 | Destino na v1.0 |
|---|---|---|---|
| `image2.png` | 607×1080 | Raça Humano | `05-racas.md` — Humano |
| `image5.png` | 1000×706 | Raça Xianzhouítas | `05-racas.md` — Xianzhouíta |
| `image12.png` | 1000×873 | Raça Vidyadhara | `05-racas.md` — Vidyadhara |
| `image14.png` | 1000×1000 | Raça Vulpes | `05-racas.md` — Vulpes |
| `image16.png` | 1000×1148 | Raça Halovianos | `05-racas.md` — Haloviano |
| `image7.png` | 736×736 | Raça Avginianos | `05-racas.md` — Avginiano |
| `image6.png` | 607×1080 | Raça Intellitrons | `05-racas.md` — Intellitron |
| `image13.png` | 700×700 | Símbolo da Destruição (torre em chamas) | `07-caminho-destruicao.md` — abertura |
| `image9.png` | 1760×1000 | Arte do Caminho da Destruição | `07-caminho-destruicao.md` — página dupla |
| `image17.png` | 700×700 | Símbolo da Inexistência | `08-caminho-inexistencia.md` — abertura |
| `image11.png` | 2048×2048 | Arte da Inexistência (vórtice cósmico) | **`00-capa-e-creditos.md` — capa** |
| `image4.png` | 700×700 | Símbolo da Harmonia | `09-caminho-harmonia.md` — abertura |
| `image8.png` | 554×554 | Arte da Harmonia | `09-caminho-harmonia.md` |
| `image1.png` | 700×700 | Símbolo da Abundância | `10-caminho-abundancia.md` — abertura |
| `image3.png` | 640×640 | Arte da Abundância | `10-caminho-abundancia.md` |
| `image10.png` | 447×447 | Símbolo da Recordação | `11-caminho-recordacao.md` — abertura |
| `image15.png` | 529×529 | Arte da Recordação | `11-caminho-recordacao.md` |

**Decisão de capa:** `image11.png` é a maior e melhor imagem do acervo (2048×2048, vórtice cósmico roxo e abstrato) e não retrata personagem nenhum — serve melhor como **capa** do que como ilustração de um Caminho só. A Inexistência mantém o símbolo `image17.png` na abertura dela.

**Lacunas de arte** (vão para o plano, não bloqueiam a escrita): faltam os símbolos de **Erudição, Euforia, Caça e Preservação** e a arte dos 4 Caminhos novos. Os capítulos 12 a 15 são escritos com um marcador `<!-- ARTE PENDENTE: símbolo do Caminho -->` no lugar, para a montagem não quebrar.

---

## 21. Índice das decisões e changelog

### 21.1 Os 16 pontos pedidos, resolvidos

| # | Ponto | Decisão | Seção |
|---|---|---|---|
| 1 | Ordem de turno / Ciclo | Fila de Ação com casas por VEL, remontada por Ciclo; Atrasar (teto 3 casas/Ciclo contra Comum, **2 contra Elite e Boss**, com a **ordem de operação da Firmeza** fechada); Avançar e Avanço Total (1/Ciclo); Congelamento retira a casa do Comum e **Atrasa 2 casas** o Elite e o Boss | 7 |
| 2 | Velocidade como estatística | `10 + Agilidade + Caminho + equipamento`; cresce só por equipamento e Bênção | 6.5 |
| 3 | Acerto crítico | 20 natural; **19-20 só na Caça, e esse é o teto do jogo**; dobra só dados base; Fraqueza e Dano Contínuo não dobram; expandir a faixa é efeito proibido em Habilidade criada | 4.6 |
| 4 | Teste de Ataque formal | `d20 + atributo + Eficiência vs Defesa`; atributo por categoria de arma; DT de Habilidade `8 + atributo + Eficiência`; 1 natural erra e não gera Energia | 4.5 |
| 5 | Vantagem / Desvantagem | 2d20 maior/menor, não acumulam, cancelam por presença | 4.4 |
| 6 | RD | Por instância, soma até `2 + 2×Eficiência`, mínimo 1 de dano, Dano Contínuo ignora | 6.4 |
| 7 | Tabela de Bônus de Atributo | Monotônica de 8 a 20, mantém 15 = +3, corrige 13 → +1 | 5.1 |
| 8 | Esquiva | Reação: Defesa + **Eficiência, sempre** (nunca Eficácia); Armadura Pesada não esquiva; premissa própria no balanceamento (1 ataque Esquivado por Ciclo) | 6.3, 18.1 |
| 9 | Dados de vida | PV fixo por Caminho (`25 + 5N + 3×Vigor`; `5 + N + Vigor` por nível); variante de rolagem com piso e teto | 6.1 |
| 10 | Compra de Pontos | Oficial: 28 pontos, custo crescente, equivalente ao array | 5.2 |
| 11 | Tenacidade e Fraqueza | Redução total / metade / 1 ponto; Implante de Fraqueza; Fraquezas reveladas | 9.4 |
| 12 | Aumentos de Atributo | +2 (ou +1/+1) nos níveis 3, 6, 9, 12, 15 e 18; teto 20 | 5.3 |
| 13 | Energia de Ultimate | +10 ao sofrer dano (1/Ciclo), +10 ao derrotar, +10 ao Quebrar (1/Ciclo) | 8.3 |
| 14 | Tabela mestra 1-20 | Completa, nenhum nível vazio | 17 |
| 15 | Equipamento icônico | Cones de Luz (Nível 1-5 + Sobreposição), Relíquias (6 slots, 4 tiers, conjuntos 2/4), Ressonâncias I-IV | 16.3-16.5 |
| 16 | Passe de balanceamento | Método de 4 passos, **17 premissas publicadas** (incluindo Esquiva, Área, Tenacidade por tipo e o contrato de encontro da Fraqueza), **DPC de referência aberto por parcela** (88/119/168/218/271), âncoras de inimigo com VEL e DT de efeitos, Defesa do PC com dispersão, alvo de 3-5 Ciclos verificado nas 5 faixas | 18 |

### 21.2 Changelog da v0.1 para a v1.0 (para o capítulo 01 e para o autor)

**Mudanças que alteram números que o autor escreveu** — todas conscientes:

1. **Faixa de níveis: 1 a 10 → 1 a 20** (override do usuário).
2. **Eficiência reespaçada:** +2/+3/+4/+5/+6/+7/+8, um degrau a cada 3 níveis. Os níveis 1-6 ficam idênticos à v0.1; o nível 9 cai de +5 para +4 e o 10 de +6 para +5, em troca da curva chegar sã ao 20.
3. **Eficácia:** continua desbloqueando no **nível 5**, mas em slots (1 Perícia + 1 Teste de Resistência no 5, chegando a 5 + 3 no nível 20). E **nunca** entra em Teste de Ataque.
4. **Bônus de Atributo:** 13 passa de +2 para +1; tabela estendida até 20.
5. **Níveis de Habilidade:** 1-5 → **1-7**, com duas linhas novas de dano, cura, alcance, buff/debuff e passiva.
6. **Quantidade de Habilidades:** "igual ao seu nível" → **teto de 8**, com reescrita de uma Habilidade por nível a partir do 16.
7. **Bênçãos:** 10 escritas → **12 escritas por Caminho, 10 adquiridas** (níveis ímpares). **Avatar: requisito nível 5 → 17.**
8. **PV:** dados de vida rolados → **PV fixo** com a mesma ordem entre Caminhos.
9. **Esquiva:** `Defesa + Agilidade` → `Defesa + Eficiência`.
10. **Armaduras:** Leve dá +1 de Velocidade (era +1 de Agilidade); Pesada dá 2 RD (era 10) e não permite Esquiva.
11. **Dano de Quebra e Dano Contínuo** reescalonados por Eficiência.
12. **Tenacidade:** elemento neutro agora reduz metade (antes, zero).
13. **Médias das tabelas de Habilidade** corrigidas; cura de Nível 5 deixa de ser cura total.
14. **Mecânicas novas:** Velocidade, Fila de Ação, Pontos de Habilidade, **Especialização de Combate**, Cones de Luz, Relíquias, Ressonâncias, catálogo de condições, regras de Descanso, bestiário, Surpresa, Esforço Total, progressão por marco narrativo, **regra de alvos em área**.
    - **Especialização de Combate (nova):** +1 no nível 5, +2 no 11, +3 no 17, em **todos** os Testes de Ataque. A v0.1 não tinha escalada de acerto própria — o acerto crescia só pela Eficiência. Não é renomeação de nada.
    - **Regra de alvos em área (nova):** a v0.1 fala de dano em área sem dizer quantos alvos. Agora são até 3 (4 nos Níveis 6 e 7), teto absoluto de 6.
15. **Nome do sistema** consolidado, sem o aviso de mudança de nome.
16. **Ultimate ganhou potência fechada** (8.5): dados por faixa, lidos na tabela de Habilidade pelo Nível equivalente (2/3/4/5/6). A v0.1 nunca deu número para a Ultimate.
17. **Esquiva, Eficácia e balanceamento:** a Esquiva soma **sempre Eficiência**, nunca Eficácia, e nenhuma fonte do livro muda isso. Ela também deixou de ser omissão do orçamento e passou a ter premissa publicada (18.1).
18. **Teste de Atenção dos Vulpes: DT 8 → Teste de Percepção Mental DT 10.** É mudança numérica, e a DT nova vem acompanhada de Eficiência (o teste original não somava nada), então na prática o traço ficou **mais** confiável — de propósito, porque ele é a identidade da raça.
19. **To na sua mente (Haloviano):** o teste oposto de Persuasão contra Intuição da v0.1 foi **aposentado** em favor de um Teste de Força de Vontade do alvo contra a sua DT. Os 2 usos por dia e o bloqueio na falha ficam.
20. **Armadura Pesada:** a penalidade de "-5 em Testes de Agilidade" virou **-2 em Testes e Perícias de Agilidade e -2 de Velocidade**.
21. **Efeitos em porcentagem de PV aposentados** (11.4): "metade da vida máxima" e companhia viram múltiplos de nível, com o Sangramento como única exceção declarada.
22. **PH dimensionado pelo tamanho da mesa** (8.2): `1 + número de jogadores`, preservando exatamente os números da mesa de 4.
23. **Evoluções do Memoespírito:** 2 (níveis 5 e 10) → **3** (níveis 8, 14 e 20), uma por faixa alta. As três opções que o autor escreveu (Forma Completa, Fusão de Memórias, Memória Desperta) ficam, e agora **todas as três** podem ser escolhidas ao longo de uma campanha completa.
24. **Teste de Morrendo:** `d20 + Bônus de Presença`, **sem Eficiência**, DT 10. A v0.1 descrevia o estado ("3 vitórias antes de 3 derrotas") sem dizer qual teste nem qual DT; a v1.0 escolhe o teste e declara a única exceção à fórmula de Teste de Resistência do livro.
25. **Congelamento contra Elite e Boss:** eles não perdem o turno; são Atrasados em 2 casas e perdem a ação especial do turno seguinte. Só Comuns perdem o turno. A v0.1 dizia "perde seu turno neste Ciclo" para todo mundo.

---

## 22. Tratamento de falhas e casos-limite

### 22.1 Na mesa (regras)

Cada operação que pode falhar, o que o jogador recebe e o que fica registrado:

| Operação | Condição de falha | Recuperável? | O que o jogador recebe | Registro |
|---|---|---|---|---|
| Teste de Ataque | Resultado < Defesa | Sim (próximo turno) | Erra; sem dano e sem Tenacidade. A **Energia da ação é ganha** (8.3); o PH gasto não volta; Ataque Básico que erra **não gera PH** | Nenhum |
| Teste de Ataque, 1 natural | 1 natural | Sim (próximo turno) | Falha automática e **não ganha Energia por essa ação** (4.5) | Nenhum |
| Teste de Perícia | Resultado < DT | Sim | O Mestre narra a consequência pela regra **falhe para frente** (3 e capítulo 02): a cena avança com custo | Nenhum |
| Teste de Resistência | Resultado < DT | Depende do efeito | Sofre o efeito completo | Condição na ficha |
| Declarar Habilidade sem PH | PH do grupo insuficiente | Sim | **Declaração inválida: nada é rolado e a ação é trocada.** Se os dados já foram rolados por engano, a rolagem é descartada. **Não existe PH negativo, PH devido nem PH emprestado** (8.2) | Contador de PH |
| Declarar Ultimate sem 100 de Energia | Energia < 100 | Sim | Declaração inválida, nada acontece | Contador de Energia |
| Segunda Ultimate no mesmo Ciclo | Já ultou neste Ciclo | Sim (próximo Ciclo) | Declaração inválida | Trilha de Ação |
| Dano reduzido a 0 | RD ou Resistência altas | — | **1 de dano** | Nenhum |
| Atraso acima do teto | Mais de **3 casas** no Ciclo contra Comum, mais de **2** contra Elite ou Boss (depois da Firmeza, 7.4) | — | Excedente perdido; o que couber vira Atraso pendente | Trilha de Ação |
| Bônus ou penalidade acima do teto | Soma passa de **+3/+4/+5** ou de **-3/-4/-5** na faixa (9.6) | — | O excedente **não se aplica**; a rolagem usa o teto. Os dois somatórios são independentes | Nenhum |
| Habilidade em área com alvos demais | Mais de 3 alvos (4 nos Níveis 6 e 7), ou alvos não agrupados (10.1) | Sim | O jogador escolhe quais alvos ficam, até o limite; os outros não são atingidos | Nenhum |
| Cura acima do PV máximo | — | — | Excedente perdido (salvo Excesso de Vida, com teto) | Ficha |
| Chegar a 0 PV | — | Sim | **Morrendo**: 3 sucessos antes de 3 falhas | Ficha + Trilha |
| Receber dano enquanto Morrendo | — | Sim | 1 falha (2 se crítico ou Habilidade Nível 5+) | Ficha |
| Memoespírito a 0 PV | — | Parcial | Desaparece; volta no próximo Descanso Curto | Ficha |
| Habilidade criada inválida | Viola 10.4 | Sim | Mestre **ajusta** antes de rejeitar | **Ficha de Decisões da Mesa** |
| Habilidade aprovada e quebrada em jogo | Descoberto em jogo | Sim | Recriação sem custo no próximo Descanso Longo | Ficha de Decisões |
| Regras em conflito | Dois textos se contradizem | Sim | Precedência da seção 3; Mestre decide em último caso | Ficha de Decisões |

A **Ficha de Decisões da Mesa** (apêndice) é o único registro persistente que o livro pede, e existe por um motivo: num sistema onde o jogador escreve conteúdo, a decisão de hoje é precedente amanhã.

### 22.2 Na montagem do livro (pipeline)

| Falha | Gravidade | Comportamento |
|---|---|---|
| Arquivo de capítulo faltando na sequência numérica | Aviso | Monta sem ele e lista o número ausente |
| Imagem referenciada que não existe | **Fatal** | Aborta informando arquivo e capítulo |
| Marcador `ARTE PENDENTE` | Aviso | Monta normalmente e conta quantos restam |
| String proibida da **Coluna A** (3.1) | **Fatal**, exceto em `00-*`, `01-*`, `30-*` e linhas com `<!-- termo-historico -->` | Aborta apontando arquivo, linha e termo |
| Uso incorreto da **Coluna B** (3.2) | **Não é verificado pelo script** | É julgamento de contexto: fica para a revisão de texto. O script não tem como distinguir "a vida do personagem" (errado) de "Propósito de Vida" (oficial) |
| Tabela Markdown malformada | Aviso | Pandoc degrada para texto; o aviso pede revisão |
| Pandoc ausente | Aviso | Os `.md` continuam sendo a entrega válida |

---

## 23. Testabilidade e verificação

Um livro de regras se testa em duas camadas, e as duas precisam existir antes da escrita acabar.

**Camada automatizável (equivalente a teste unitário)** — scripts em `scripts/`, PowerShell 5.1:

- `checar-nomenclatura.ps1`: varre `livro-v1.0/*.md` buscando **só as 25 strings da Coluna A de 3.1** ("ação bônus", "HP", "rodada", "DoT", "iniciativa", "provavelmente vou mudar o nome", "nível 1 a 10"…). Falha com arquivo, linha e termo.
  **O script NÃO verifica a Coluna B de 3.2**, e essa é a diferença que decide se o gate é útil ou se ele reprova o livro inteiro. A Coluna B lista palavras que o sistema **usa como termo oficial** em outro contexto — "vida" em Propósito de Vida e em Excesso de Vida, "dificuldade" dentro de "Dificuldade do Teste" e como cabeçalho de coluna em 18.4, "ação" em Ação Complementar, "bônus" em Bônus de Atributo, "armadura" em Bônus de Armadura, "resistência" nos 6 Testes de Resistência e na Perícia Resistência. Procurar essas strings reprovaria os 28 capítulos no primeiro `git commit`. Uso incorreto de termo é **revisão humana**, e está listado como tal em 3.2.
  **Válvula obrigatória para a Coluna A:** as strings proibidas são **ignoradas** em `00-*`, `01-*` e `30-*` — a introdução precisa contar o que mudou da v0.1 e o glossário precisa citar os termos aposentados para a mesa antiga se localizar — e em **qualquer linha marcada com `<!-- termo-historico -->`**. Nos outros 28 capítulos a ocorrência é **fatal**.
- `checar-tabelas.ps1`: confere que as médias impressas das tabelas de dano, cura e Ultimate batem com `floor(nº de dados × média do dado)` (`6d6 = 21`, `5d10 = 27`, `5d8 = 22`, `7d20 = 73`, `18d20 = 189`), que a tabela de Bônus de Atributo é monotônica não-decrescente, que a progressão 1-20 não tem nível vazio, e que a coluna de Nível equivalente da Ultimate (8.5) aponta para linhas que existem em 10.1.
- `simular-combate.ps1`: recebe as **premissas de 18.1 como parâmetros** (taxa de acerto, mix de ações, Nível de Habilidade sustentável pelo PH, RD dos dois lados, crítico, **cadência de Quebra por perfil**, **ataques Esquivados por Ciclo**, **alvos em área**), reproduz o DPC de 18.2 parcela por parcela e imprime três valores por faixa: o **DPC de referência** (acerto e RD de Elite, cadência de Quebra de Boss), o **DPC puro de Elite** e o **DPC puro de Boss**. Também imprime **em quantos Ciclos o combate termina** nas cinco faixas e a **attrition do grupo** com a premissa de Esquiva. Reprova se: alguma faixa sair de **3 a 5 Ciclos**; o **DPC de referência** divergir do publicado em mais de 5%; a attrition de um combate sair da janela de **70% a 85%** ou a do terceiro combate do dia sair de **45% a 70%**; ou o Memoespírito sair da janela de **15% a 25%** do dano do dono (13.1).
- `map-imagens.ps1` (já escrito): reextrai a posição das imagens do `.docx` da v0.1, garantindo que o mapa de 20.3 não vire achismo.
- `thumbs.ps1` (já escrito): gera miniaturas leves das imagens para inspeção rápida de arte sem abrir arquivos de 5 MB.

**Camada de mesa (equivalente a teste de integração):** cinco cenários de playtest, um por faixa (1-4, 5-8, 9-12, 13-16, 17-20), cada um com Comum + Elite + Boss, medindo Ciclos até a resolução, quantas vezes o grupo Quebrou o alvo, quantos PH sobraram e quantos personagens chegaram a Morrendo. O apêndice de balanceamento traz as três simulações de referência resolvidas Ciclo por Ciclo.

**O que não é testável automaticamente** e precisa de leitura humana: tom de voz, fidelidade ao universo, clareza dos exemplos e se as Bênçãos novas dos 4 Caminhos têm a mesma "pegada" das originais. Isso é trabalho do review de design e da revisão de texto, não de script.

---

## 24. Fora do escopo da v1.0

Registrado para não voltar como surpresa:

- **Campanha, cenário e aventura pronta.** A v1.0 é o livro de regras. Ganchos de mundo aparecem só como exemplo.
- **Regras de nave, viagem interestelar e economia de créditos.** Ficam para um suplemento.
- **Combate em grade com posicionamento exato.** A escala de Distâncias abstratas é uma decisão, não uma falta.
- **PvP balanceado.** O sistema é cooperativo; duelos entre PJs funcionam, mas não são alvo de balanceamento.
- **Níveis acima de 20.**
- **Arte nova.** O acervo é o da v0.1 mais os marcadores de arte pendente.
- **Mais de 12 Bênçãos por Caminho**, Eidolons compráveis e níveis de Habilidade acima de 7.

---

## 25. Histórico deste documento

| Iteração | O que mudou |
|---|---|
| 1 | Documento inicial. Fecha os 16 pontos pedidos, as 22 lacunas, 28 erros concretos (hoje 31), a estrutura de 31 capítulos e o mapa de imagens. Incorpora o **override do usuário para a faixa 1-20** (Eficiência reespaçada, Habilidades de Nível 1-7, teto de 8 Habilidades, 12 Bênçãos por Caminho com Avatar no 17, PV até o 20, balanceamento em 5 faixas, DT por faixa, bestiário em 5 faixas, equipamento espalhado pelos 20 níveis) |
| 2 | **Passe de revisão sobre os 41 achados da iteração 1 (5 HIGH, 22 MEDIUM, 14 NIT).** Principais entregas: potência da Ultimate (8.5); premissas de balanceamento publicadas e DPC aberto parcela por parcela, com âncoras de inimigo rededuzidas (18.1 a 18.3); ficha do Memoespírito ancorada no dono (13.1); PH sem crédito e dimensionado pelo tamanho da mesa (8.2); teto de bônus somado com escopo fechado (9.6); tabela única de DT com linha Trivial e Sucesso Automático restrito a Perícia (18.4, 4.2); regra de progressão de nível (17.1); gatilho de Surpresa (7.3); os quatro recursos dos Caminhos novos com número, incluindo as 6 entradas da Tabela do Riso (11.2); efeitos em porcentagem de PV aposentados (11.4); e 20 consertos pontuais de número, escopo e ponteiro. Respostas achado por achado em 26.2 |
| **3** | **Passe de revisão sobre os 26 achados da iteração 2 (3 HIGH, 14 MEDIUM, 9 NIT).** As três entregas estruturais: **regra de alvos em área** (10.1, repetida em 6.4, 8.5, 10.4 e 11.2 — era a única regra inteiramente em branco e bloqueava o capítulo 12 e o bestiário em grupo); a **Esquiva dentro do modelo de balanceamento**, com premissa publicada, Eficácia removida dela e attrition recalculada e republicada em 73-81% por combate e 51-64% no terceiro combate do dia (6.3, 18.1, 18.3); e o **contrato de encontro da Fraqueza**, que transforma a única premissa não reproduzível numa obrigação do Mestre (18.1, capítulo 27). Mais: nomenclatura dividida em strings proibidas e uso incorreto, para o gate de pipeline parar de reprovar o próprio livro (3.1, 3.2, 22.2, 23); **teto de penalidade somada** separado do de bônus (9.6); **ordem de operação da Firmeza** e teto de 2 casas contra Elite/Boss (7.4); **Congelamento com Firmeza** (7.6); Tenacidade com fórmula **por tipo de inimimigo** e cadência de Quebra por perfil (18.1); **Defesa do PC com dispersão** e ataque inimigo da faixa alta recalibrado (18.2, 18.3); colunas de **VEL e DT de efeitos** na tabela de âncoras (18.3); Dano de Quebra sofrendo RD e com o Elemento certo no exemplo-modelo (18.2); **Esforço declarado exclusivo do Humano** (12, 15.2, 18.1); **Teste de Morrendo sem Eficiência** (14, 15.1); as **cinco DTs de subsistema** declaradas em lista fechada (4.2, 9.3, 18.4); categoria de arma **Média** na tabela de Atributo de Ataque (4.5); dez conversões a mais na régua de 11.4 e três em 7.9; teto de crítico reduzido a 19-20 (4.6); Esfera Planar e Mãos declaradas disjuntas (16.4); e a Especialização de Combate reclassificada como **mecânica nova** (3.2, 4.3, 21.2). Respostas achado por achado em 26.1 |

---

## 26. Respostas aos achados do review

### 26.1 Iteração 3 — os 26 achados do review da iteração 2

Review lido: `.agents/tasks/design-review.json` e `.agents/tasks/design-review.md` — veredito **CHANGES_REQUESTED**, 26 achados (3 HIGH, 14 MEDIUM, 9 NIT). **Nenhum achado foi ignorado e nenhum foi deixado para depois.** Onde a minha decisão difere da correção sugerida, o motivo está escrito na linha.

#### HIGH

| # | Decisão | O que foi feito e onde |
|---|---|---|
| 1 | **Atendido pela opção (a)** | A premissa de Fraqueza virou **contrato de encontro**, com bloco próprio em 18.1 e obrigação repetida no capítulo 27 (descrição atualizada em 20): *"o Mestre monta o encontro de modo que pelo menos 3 dos Elementos do grupo apareçam como Fraqueza entre os inimigos da cena; encontro que não cumpre isso é deliberadamente mais duro e dura ~1 Ciclo a mais"*. A linha da tabela de premissas passou a nomear **quais** ações acertam Fraqueza (Habilidade + Ultimate + 1 dos 2 Ataques Básicos), o que torna a conta de 18.2 literalmente rastreável. Escolhi (a) e não recalcular com 1,7: preserva as 15 células de 18.3, mantém a cadência de Quebra que o combate precisa (9.4 amarra Tenacidade à Fraqueza pela mesma premissa) e é fiel à origem — em Honkai: Star Rail é o jogador que monta a equipe olhando as Fraquezas; na mesa, é o Mestre que monta o inimigo olhando a equipe. O bloco também diz o que fazer quando o encontro é temático e fecha mal. |
| 2 | **Atendido pelas duas vias, com a opção mais limpa** | (i) A **Esquiva ganhou premissa publicada** em 18.1 ("1 ataque inimigo por Ciclo é Esquivado; 60% nos não Esquivados e 20% no Esquivado; ~47% de acerto médio") e saiu da lista de omissões, com um parágrafo explicando por que a omissão era erro de modelo e não margem. (ii) **A Esquiva soma sempre Eficiência, nunca Eficácia:** a cláusula de Acrobacia saiu de 6.3, a passiva de Nível 7 de 10.2 trocou de exemplo, "trocar Eficiência por Eficácia na Esquiva" entrou na lista de efeitos **proibidos** de 10.4, o índice de 21.1 foi corrigido e o invariante entrou em 19 com camada dona. (iii) A **attrition foi recalculada e republicada com a conta aberta nas cinco faixas** (18.3): o grupo termina um combate típico com **73% a 81% dos PV**, não os 50-70% de antes nem os 89% que o achado estimava para o caso de Esquiva irrestrita. Publiquei a tabela de derivação (PV do grupo, dano recebido em 4 Ciclos, resultado com e sem Esquiva) em vez de só o número, mais as **quatro razões** pelas quais o Caminho de sustentação continua necessário apesar da média confortável: foco inimigo (um PC cai em 4 a 7 acertos, e um Boss concentrado o derruba em 2 Ciclos), Dano Contínuo (ignora RD e não admite Esquiva), ação especial de Boss (o pico que a média esconde) e **o dia em vez do combate** (três combates com dois Descansos Curtos levam o grupo a 51-64%). Preferi o teto absoluto ao "+Eficiência +2 com Eficácia em Acrobacia": a Esquiva é a única defesa gratuita e universal do jogo, e um número só é mais fácil de orçar e de checar na mesa. |
| 3 | **Atendido com a regra proposta** | **10.1 passou a ter bloco próprio de área:** metade dos dados (mínimo 1), **até 3 alvos** agrupados a até uma Distância um do outro, **4 alvos nos Níveis 6 e 7**, teto absoluto de **6** só com recurso de Caminho ou Bênção. Repetida em 8.5 (Ultimate, lida no Nível equivalente), em 10.4 (checklist, com "atingir mais alvos do que 10.1 permite" entre os proibidos), em 6.4 (RD uma vez por alvo) e em 11.2 (os alvos dos Acúmulos de Cálculo **somam sobre a base** e respeitam o teto de 6 — a Erudição é o único Caminho que alcança o teto, o que é a promessa dela). Acrescentei o que a correção não pedia mas a regra exige para ser jogável: atributo somando por alvo, Fraqueza calculada por alvo, cura em área com a mesma contagem, e a área não estendendo o alcance. E a **premissa de área** entrou em 18.1, com a consequência registrada em 18.3: encontro de 3+ inimigos resolve em 2-3 Ciclos, e isso é correto. |

#### MEDIUM

| # | Decisão | O que foi feito e onde |
|---|---|---|
| 4 | Atendido nas três edições | (1) 21.2: a Especialização de Combate saiu do item 17 e entrou no **item 14, lista de mecânicas novas**, com o texto *"a v0.1 não tinha escalada de acerto própria — o acerto crescia só pela Eficiência"*; o item 17 foi reaproveitado para a decisão de Esquiva/Eficácia. (2) 3.2: a coluna de uso incorreto dela ficou vazia e a observação declara *"mecânica nova da v1.0, sem termo correspondente na v0.1 (nada a aposentar)"*. (3) 4.3 ganhou um aviso em bloco de citação dizendo o mesmo, para o capítulo 01 apresentá-la como acréscimo. A linha de arraste de 26.2 também foi corrigida. |
| 5 | Atendido nas duas partes | (i) A premissa única de Tenacidade virou **fórmula por tipo**: Boss `2 ×` a redução do grupo por Ciclo, Elite `1 ×`, Comum `0,5 ×`, com o motivo escrito (num encontro de 3 Elites ou 7 Comuns a redução se reparte). A **cadência de Quebra** virou premissa separada: 1 a cada 2 Ciclos no perfil de Boss, 1 por Ciclo nos de Elite e Comum. **As 15 células de Tenacidade de 18.3 não mudaram**, e 18.3 agora publica a **derivação completa numa tabela própria** (redução do grupo 9 / 9,75 / 11 / 10,75 / 11,25 e os três multiplicadores aplicados), mais os dois desvios de arredondamento que valem a pena nomear: o Comum é um pouco mais frágil que o derivado (4 contra 4,5) e o Boss da faixa 17-20 um pouco mais duro (24 contra 22,5). Não escrevi "sai exatamente a coluna" porque não sai — sai o arredondamento dela, e essa é a frase honesta. (ii) 18.2 declara que o número publicado é um **DPC de referência** (acerto e RD de Elite, cadência de Quebra de Boss), explica por quê, e publica as duas pontas: ~300 contra Elite e ~246 contra Boss. 23 manda `simular-combate.ps1` imprimir as três e comparar **a de referência** contra o publicado, o que resolve a divergência de 8% que reprovaria o script. |
| 6 | Atendido, com o teto baixado | 7.4 ganhou **lista numerada de ordem de operação** (somar as casas do Ciclo → dividir por 2 com `floor` → mínimo 1 **no total do Ciclo** → teto) e tabela de teto por tipo: **3 casas contra Comum, 2 contra Elite e Boss**. O exemplo de 7 casas brutas virando 2 e o de 1 casa bruta virando 1 estão escritos, porque é a ordem que decide o resultado. 18.3 e o invariante de 19 foram atualizados. Agora a regra entrega o que o texto promete (1-2 casas por Ciclo) em vez de 3. |
| 7 | Atendido pela primeira opção | 7.6 ganhou o bloco **Firmeza contra Congelamento**: Elite e Boss **não perdem o turno**; são Atrasados em **2 casas** (o teto do Ciclo contra eles, logo nada mais soma) e **perdem a ação especial do turno seguinte**. Só Comuns perdem o turno. Cortei a cláusula de "não gerar Energia" da sugestão porque inimigos não acumulam Energia neste sistema (18.3). Escolhi esta em vez de "só pode ser Congelado uma vez por combate" porque mantém o Gelo relevante em todos os Ciclos sem nunca remover o Boss da Fila — e porque é a **mesma** resposta que o Atraso já tinha, o que deixa uma regra só para a mesa decorar. Registrado no changelog (21.2, item 25) e em 18.3. |
| 8 | Atendido, ampliado | 11.4 passou de 14 para **25 linhas** de conversão (`+4 de Defesa`, `+10 de RD`, `+5 RD`, `+20 de PV máximo`, `+5 no teste de ataque`, `ignora 5 de defesa`, `romper -5 na defesa`, `-1 até -10 em ataques`, `1d10/1d12 de efeito contínuo`, `50% mais de dano`) e uma linha de política: se a escrita achar uma construção fora da tabela, ela **não inventa número**, cai na linha mais próxima e registra na Ficha de Decisões. 7.9 ganhou **três linhas** (`o alvo demorará mais um turno` → Silenciado, nas duas Bênçãos onde aparece, e a DT derivada de rolagem de *Aniquilador de Resistências* → a DT oficial de 4.2), mais um bloco declarando que nenhuma frase do livro descreve subsistema inexistente e que as duas únicas saídas são o catálogo de 9.6 ou a régua de 11.4. A `-1` acumulativa ficou amarrada ao **teto de penalidade somada** (achado 16) em vez de a `-Eficiência`, que estouraria o teto na faixa alta. |
| 9 | Atendido | A seção 3 foi **dividida em duas de natureza diferente**: **3.1 Coluna A**, as 25 strings que não existem no vocabulário do sistema (checagem automática, falha fatal), e **3.2 Coluna B**, termo oficial contra uso incorreto (revisão humana, **fora** do script). As palavras que o livro usa como termo oficial — vida, dificuldade, ação, bônus, armadura, resistência — saíram da lista de strings e foram para a Coluna B, cada uma com a observação de onde o uso é legítimo (Propósito de Vida, Dificuldade do Teste, Ação Complementar, Bônus de Atributo, Bônus de Armadura, os 6 Testes de Resistência). 23 e 22.2 agora dizem explicitamente que o gate fatal é **só** a Coluna A, com o motivo. |
| 10 | Atendido delimitando escopo | As três declarações absolutas viraram declarações de **escopo**: 4.2 e 18.4 dizem "única tabela de DT **geral**" e publicam a **lista fechada de cinco DTs de subsistema** que vencem a geral (Fraqueza 9.3, Surpresa 13 em 7.3, Morrendo 10 em 15.1, Raposa Astuta 10 e To na sua mente 13 em 12), com o motivo: subsistema que é **rotina de combate** não pode escalar com a faixa, senão morre na faixa alta. 9.3 ganhou o aviso de que ela é uma das cinco e vence 18.4. O invariante de 19 foi reescrito como "as cinco vencem a geral; não existe uma sexta", com dono no capítulo 27. Incluí a Surpresa na lista, que o achado 14 criou — são cinco, não quatro. |
| 11 | Atendido com os valores propostos | 18.3 ganhou as colunas **VEL C/E/B** (11/12/13, 12/13/15, 13/15/16, 14/16/18, 15/17/19) e **DT dos efeitos C/E/B** (12/13/14, 14/15/16, 16/17/18, 17/18/19, 19/20/21), mais dois parágrafos explicando de onde vêm: a VEL foi calibrada com a regra de projeto *"a Caça equipada age antes de todo Comum e Elite da faixa dela e disputa a primeira casa com o Boss"*, e a DT dos efeitos entrega a janela que entrou em 18.1 (55-65% com o atributo certo, 35-45% com o errado). Fechei o parágrafo da ficha padronizada com a frase que faltava: **todos os campos da ficha têm coluna na tabela de âncoras**, nenhum obriga o Mestre a inventar número. 6.5 também passou a apontar para a coluna de VEL de inimigo. |
| 12 | Atendido | 4.5 passou a ter **exatamente as seis categorias de 9.2** (Leve, Média, Pesada 2 mãos, Disparo curto, Disparo longo 2 mãos, Energia 2 mãos), com os exemplos marcados como ilustração e não como taxonomia, mais as linhas de Habilidade/Ultimate e Memoespírito. A linha **Média** (Poder ou Agilidade, fixo na criação) existe e está destacada como a arma de referência do orçamento de 18.2. |
| 13 | Atendido | 20.2, linha E06: a célula de correção virou **21/27/39/63/105**, com "(média `floor`, ver 3 e 10.1)". Agora os cinco lugares dizem 27. |
| 14 | Atendido, fechando as duas pontas | 7.3: a DT da Surpresa é **13, fixa em todas as faixas**, e isso está justificado contra a regra de 18.4 ("a faixa é do desafio, não do personagem") com a conta do PC de nível 20 sendo emboscado em 80% das cenas. A ambiguidade DT-estática-ou-teste-oposto foi resolvida: **se houver um atacante declarado se aproximando às escondidas, ele faz UM Teste de Furtividade e o resultado substitui a DT 13 para todo o lado emboscado** — um teste, não um por alvo. A DT 13 entrou na lista fechada de 4.2 e 18.4. |
| 15 | Atendido pela via recomendada (fidelidade à fonte) | 12 ganhou bloco declarando o **Esforço como recurso exclusivo do Humano**, com a frase "nenhuma outra Raça, Caminho, Bênção, Habilidade, Cone de Luz ou item concede Esforço" e a observação de que uma mesa sem Humano não tem o recurso. 15.2: o Descanso Longo "devolve o ponto de Esforço **a quem tiver o traço que o concede** (Humano, 12)". 18.1: a omissão virou "**Esforço (só em mesas com Humano, 12)**". 3.2 registra o escopo na própria linha do termo. Os quatro lugares dizem a mesma coisa. |
| 16 | Atendido dividindo o invariante | 9.6 passou a publicar **dois tetos independentes**: bônus somado (+3/+4/+5) e **penalidade somada (-3/-4/-5)**, com a frase que mata a ambiguidade — *"os dois são somatórios separados e não se cancelam para efeito de teto: +3 de buff e -4 de penalidade somam -1 na rolagem, e nenhum dos dois tetos foi excedido"*. A tabela de escopo ganhou linha para penalidades aplicadas por inimigos **e por jogadores**, e a penalidade fixa de Armadura Pesada foi declarada **fora** dos tetos (é equipamento permanente, igual ao bônus que vem com ela). O parágrafo de justificativa explica por que isso importa mais do lado do inimigo: o Caminho da Inexistência é feito de empilhar penalidade, e com teto próprio o jogador sabe quando parar de repetir o mesmo debuff. O invariante de 19 virou um só, com os dois tetos. |
| 17 | Atendido publicando dispersão e recalibrando o inimigo | 18.2 publica a **Defesa com três colunas** (referência/Média 16/18/20/21/22, mais baixa realista/Leve 14/16/18/19/20, mais alta/Pesada 17/19/21/22/23) e a **build de referência explícita** (`10 + Agilidade típica da faixa + Média + Tronco do tier`, com a Agilidade típica publicada: +0/+2/+4/+4/+5), de modo que qualquer pessoa reproduz as 15 células. A janela de 18.1 virou **60% contra a referência, 70% contra Leve, 55% contra Pesada**, e o parágrafo diz em voz alta que é pelo personagem de Armadura Leve — tipicamente a Caça, o menor PV do jogo — que existem a Esquiva, o Intervir e o Caminho de sustentação. Como a referência da faixa 17-20 caiu de 23 para 22, o **Teste de Ataque do inimigo dessa faixa caiu de +14 para +13** em 18.3, exatamente como o achado indicava, e os 60% voltaram a ficar cravados nas cinco faixas. |

#### NIT

| # | Decisão | O que foi feito |
|---|---|---|
| 18 | Atendido | 18.2: a linha do exemplo-modelo trocou **Físico por Fogo** (os números já eram de Fogo), e ganhou uma nota de Elemento explicando que os dois têm o mesmo Dano de Quebra mas efeitos contínuos diferentes, com a conta do Sangramento (18 por turno contra um Elite de 361 PV, dentro do teto de `3 × Eficiência`; 55 por Quebra em vez de 49). O apêndice 29 abre as duas versões, para a faixa-modelo não propagar o erro. |
| 19 | Atendido aplicando a RD | 18.2: o Dano de Quebra passou a **sofrer RD** (é instância de dano por 6.4), a parcela caiu de 26,5 para **24,5** e a coluna foi republicada como 14/18/19/21/25. O DPC publicado virou **88/119/168/218/271**. As âncoras de 18.3 **não mudaram**, e isso está declarado com o número: elas são arredondamentos legíveis de `DPC × 4` e ficam a menos de 3% do derivado (maior divergência: Elite da faixa 1-4, 120 contra 117). Mudar 15 células para ganhar 2% num orçamento cuja tolerância é 5% seria churn — mas a divergência tinha que estar escrita. |
| 20 | Atendido | 6.5: "**VEL 10 a 19** no nível 1; **12 a 21** no nível 10; **13 a 24** no nível 20 com equipamento", mais os extremos calculados pela própria fórmula: piso **7** (Agilidade 8, Caminho +0, Armadura Pesada) e teto **25** (Agilidade 20, Caça +4, Botas IV +5, Armadura Leve +1 — o achado dizia 24 porque não somava o +1 da Leve). |
| 21 | Atendido | 4.3: "obrigando Defesas de Boss na casa de 35 para manter os **mesmos 65% de acerto do atacante de referência**", com a conta explícita (+19 contra Defesa 27 de Boss pede 8 no d20). |
| 22 | Atendido | 21.2, item **23**: *"Evoluções do Memoespírito: 2 (níveis 5 e 10) → 3 (níveis 8, 14 e 20), uma por faixa alta. As três opções do autor ficam, e agora todas as três podem ser escolhidas ao longo de uma campanha completa."* Aproveitei para registrar duas outras mudanças que também não estavam no changelog e que a iteração 3 criou: o **Teste de Morrendo sem Eficiência** (item 24) e o **Congelamento contra Elite e Boss** (item 25). |
| 23 | Atendido removendo a escada inexistente | Em vez de declarar o 18-20 como guarda-corpo de conteúdo futuro, **baixei o teto para 19-20** e declarei a Caça como **única** fonte, porque um corrimão de escada inexistente é convite para alguém construir a escada. "Expandir a faixa de crítico" entrou na lista de **efeitos proibidos** de 10.4, o que protege a identidade da Caça contra Habilidade criada na mesa, e 4.6 registra que a capstone da Caça não expande de novo. Com isso, os 5% de crítico que o DPC usa como premissa (18.1) valem para todo mundo menos um Caminho, e está escrito qual. |
| 24 | Atendido | 16.4 ganhou o bloco **"Mãos e Esfera Planar nunca somam na mesma rolagem"**: a Esfera vale para dano de Habilidade, de Ultimate e de Dano Contínuo do Elemento escolhido, e **não** para Ataque Básico, que já é coberto pelas Mãos — com a conta do +16 no Tier IV que a regra em branco permitia. |
| 25 | Atendido pela opção A (manter a tensão) | 15.1: o Teste de Força de Vontade de Morrendo é **`d20 + Bônus de Presença`, sem Eficiência nem Eficácia**, DT 10. Declarado como **exceção única** também em 14 ("não existe treino que te torne bom em não morrer"), com invariante e camada dona em 19 (capítulo 23) e entrada no changelog (21.2, item 24). Escolhi A e não B porque a margem de attrition de 18.3 **subiu** para 73-81% com a premissa de Esquiva: deixar a morte também virar formalidade na metade da campanha tiraria consequência de duas coisas ao mesmo tempo. O parágrafo de justificativa mostra os dois extremos (50% de sucesso por rolagem com Presença -1, 80% com Presença +5 — nunca 100%) e explica por que o Executado não cobre a lacuna: ele exige um inimigo **racional** a Distância Pessoal, e boa parte do bestiário é besta ou máquina. |
| 26 | Atendido pela segunda via (declarar), com a conta das casas | 18.1: a premissa de ações virou uma linha que diz **de quem é cada turno** — "1 Habilidade (um ofensivo) + 2 Ataques Básicos (o outro ofensivo, mais aquele entre o suporte e a sustentação que **não** estiver cuidando do grupo neste Ciclo) + 1 turno sem dano direto (cura, buff, remover condição), que **alterna** entre o suporte e a sustentação; mais a Ultimate do Ciclo, que não gasta ação". O turno de cura que o achado mostrou faltando **é** o quarto turno, e agora está nomeado como tal. Preferi isso a recalcular com 1,5 Ataques Básicos: a leitura alternada é a composição real de uma mesa de 4 (nem o suporte nem a sustentação têm algo para consertar todo Ciclo), preserva o DPC aberto parcela por parcela e não arrasta as 15 células de 18.3 por um ajuste de redação. |

### 26.2 Iteração 2 — os 41 achados do review da iteração 1

Mantido como registro de processo. Veredito do review: **CHANGES_REQUESTED**, 41 achados, todos endereçados.

#### HIGH

| # | Decisão | O que foi feito e onde |
|---|---|---|
| 1 | **Atendido** | Nova seção **8.5 Potência da Ultimate**. Em vez de criar uma tabela de dados paralela, a Ultimate passa a ter um **Nível equivalente** por faixa (2/3/4/5/6) e **lê as linhas de 10.1 e 10.2 nesse Nível** — uma tabela a menos para a mesa decorar e o indexador que o achado pedia para a Ressonância II (16.5, corrigida) e para o checklist de 10.4. Médias: 27/39/63/105/147. Redução de Tenacidade 5 em todas as faixas, com justificativa. A descrição do capítulo 17 em 20 agora aponta para essa tabela, e o DPC de 18.2 traz a Ultimate como parcela explícita. |
| 2 | **Atendido na leitura recomendada** | **Energia pela ação** (fiel à v0.1), **PH condicionado ao acerto**. 4.5 reescrita, 8.2 passa a dizer "Ataque Básico **que acerta** gera", 18.1 publica a geração de PH multiplicada pela taxa de acerto como premissa, e a linha correspondente de 22.1 foi refeita. O 1 natural continua sendo a única falha que também corta a Energia (4.5). |
| 3 | **Atendido, sem a válvula** | 22.1 agora diz: declaração inválida, nada é rolado, rolagem feita por engano é descartada, **não existe PH negativo, devido nem emprestado** — e a mesma frase está em 8.2, que é a camada dona. Optei por **não** criar a válvula de "1 PH fiado por combate" que o achado oferecia: seria recurso novo fora do orçamento de 18.1, e o remédio para grupo sem PH já existe (bater, usar Habilidade de Nível menor, ou ultar, que não custa PH). |
| 4 | **Atendido com as fórmulas propostas** | 13.1 reescrita: Teste de Ataque, Defesa, dano e Velocidade do Memoespírito **ancorados no dono**; os 12 pontos com teto 5 ficam como diferenciação, exatamente como a v0.1 escreveu. Redução de Tenacidade 1 (2 a partir do nível 11 do dono). Alvo de projeto declarado — **15% a 25% do dano do dono** — e `simular-combate.ps1` (23) reprova fora dessa janela. |
| 5 | **Atendido, e foi o conserto mais profundo da iteração** | 18.1 publica **14 premissas fechadas** (mix de ações, Nível de Habilidade sustentável pelo PH, taxa de acerto, Fraqueza, RD dos dois lados, crítico, cadência de Quebra, ações inimigas por turno). 18.2 abre o DPC **parcela por parcela** nas cinco faixas e detalha a faixa 17-20 conta por conta. O DPC publicado caiu para **90/120/170/220/275** — a iteração 1 superestimava em até 80% porque contava Habilidade de topo por Ciclo e ignorava RD inimiga. 18.3 foi **rededuzida** desse DPC. A janela de acerto virou **uma só, por tipo de inimigo: 70% Comum / 60% Elite / 55% Boss**, válida nas cinco faixas, e a frase errada de 4.3 foi substituída pela conta correta. |

#### MEDIUM

| # | Decisão | O que foi feito e onde |
|---|---|---|
| 6 | Atendido | 6.1: "PV por nível (**2 a 20**)". |
| 7 | Atendido | 5.3: o aumento de Vigor concede **nível atual + 2** PV, com a demonstração de que isso fecha com a fórmula de 6.1 (o ganho na hora mais o incremento por nível somam o valor retroativo). Nota de "Vigor +2 constante" acrescentada à tabela de 6.1 e às âncoras de 18.2. |
| 8 | Atendido pelas duas vias | 9.6 reescrita com **escopo fechado em tabela**: entram no teto os bônus temporários (Bênção, Habilidade, Ultimate, conjunto, Efeito Condicional de Cone); ficam fora os permanentes (Atributo, Eficiência/Eficácia, Especialização de Combate, Bônus Maior de Cone, slot de Relíquia, armadura). Além disso, a Sobreposição de Cone (16.3) teve o teto baixado de +4 para **+3**. |
| 9 | Atendido | **18.4 é a tabela única**, com a linha **Trivial** (8/9/10/11/12) acrescentada. 4.2 virou "como se lê uma DT", com os valores **da faixa 1-4** copiados de 18.4, e diz isso em uma linha de aviso. O exemplo do muro (DT 13) agora está coerente com a tabela. |
| 10 | Atendido | 18.4: Sucesso Automático **só em Teste de Perícia**; Ataque e Resistência são sempre rolados, porque o 20 e o 1 naturais têm efeito próprio. |
| 11 | Atendido | 9.2 e a legenda de 17 declaram que a coluna conta **quantos dados a arma rola** a partir de 1: arma de 1 dado chega a 5, arma de Energia chega a **6**. O orçamento de 18.2 usa a arma Média (1d10 → 5d10). |
| 12 | Atendido | 10.1 publica **21/27/39/63/105/147/189** (dano) e **22/33/52/73/105/147/189** (cura); a seção 3 declara que médias impressas são `floor`; 23 registra que o script compara contra `floor`. A tabela da Ultimate (8.5) segue a mesma regra. |
| 13 | Atendido | 9.4 abre com "**Só inimigos têm Tenacidade**"; o catálogo de 9.6 marca **Quebrado (só inimigos)**; o exemplo de 16.3 virou "quando **você Quebra** um inimigo", com a proibição explícita de gatilho por aliado Quebrado. |
| 14 | Atendido | 12 traz **To na sua mente** como sequência fechada: 2 usos por dia, Ação Complementar, Teste de Sintonia DT 13 só para quem não segue a Harmonia, bloqueio até o Descanso Longo na falha, e **Teste de Força de Vontade** do alvo (não Resistência Mental) contra `8 + atributo + Eficiência`. O teste oposto da v0.1 foi aposentado e está no changelog 21.2. |
| 15 | Atendido | 8.1: "**toda criatura começa o combate com a Reação disponível**; depois disso ela recarrega no início do turno dela", com o motivo (a Preservação). |
| 16 | Atendido nas duas partes | 8.2: **máximo de PH = 1 + número de jogadores** (+1 na faixa 10-15, +2 na 16-20), início = máximo − 2 — fórmula que reproduz exatamente 5/6/7 e 3/4/5 da mesa de 4, com tabela para 3, 4, 5 e 6 jogadores. Recarga única: **no começo de cada combate**; a cláusula de PH saiu do Descanso Curto (15.2). |
| 17 | Atendido | 7.3 ganhou o bloco **Surpresa**, com o gatilho (Teste de Percepção Mental contra a DT Média da faixa ou contra `8 + Furtividade`), quem declara, e o que acontece. 7.7 passou a apontar para lá, e o traço dos Vulpes virou segunda chance contra esse mesmo teste. |
| 18 | Atendido | Nova seção **17.1 Como se sobe de nível**: progressão por **marco narrativo**, grupo junto, sem XP por inimigo, ritmo sugerido por faixa, Ressonâncias como marcos de história, personagem novo entra no nível do grupo. Dono: capítulo 26 (descrição atualizada em 20 e invariante registrado em 19). |
| 19 | Atendido | 11.2 fecha os quatro recursos com número: **Acúmulos de Cálculo** (teto 5, 1 por alvo, 2 por dado, não consome ação, zera no fim do combate), **Tabela do Riso** com as **6 entradas escritas**, **Marcação de Presa** (Ação Complementar, 1 alvo, +1 dado base, migra na morte do alvo) e **Barreira** (teto de PV temporário, ordem contra RD, conta no teto de quem recebe). |
| 20 | Atendido, ampliado | 11.4 ganhou **4 linhas** de conversão de efeitos percentuais (não só as 2 sugeridas: incluí também "metade dos PV perdidos" e os percentuais da Forma Sincronizada) e a **regra geral de política**: nenhum efeito cura, concede PV ou causa dano em porcentagem do PV máximo. A única exceção é o **Sangramento**, declarada como exceção e com teto próprio. |
| 21 | Atendido | 23 documenta a válvula: termos proibidos são ignorados em `00-*`, `01-*`, `30-*` e em linhas marcadas com `<!-- termo-historico -->`; fatais nos outros 28 capítulos. 22.2 repete a exceção. A conversão **"por 1 rodada" → "por 1 Ciclo"** entrou na tabela de 7.9. |
| 22 | Atendido | **Teto global de PV temporários = 3 × Eficiência**, de qualquer fonte, sem acumular entre fontes — declarado em 15.3, reexpresso em 10.2 (1×/2×/3× Eficiência) e já referenciado em 11.4 e 11.2. Virou invariante com camada dona em 19. |
| 23 | Atendido | 18.3 tem coluna de **RD C/E/B** (0/2/4 nas faixas 1-8, 0/3/6 nas 9-16, 0/4/8 na 17-20); 6.4 declara que o teto de RD vale para inimigos lendo a Eficiência da faixa deles; e a RD inimiga é premissa publicada do DPC em 18.1, subtraída de cada instância nas contas de 18.2. |
| 24 | Atendido, com varredura | 6.4 → **11.4**; 4.5 → **11.1**; E05 → capítulo **06**. Fiz o passe de conferência em todos os "ver X.Y" do documento: as referências a 11.2 e 20.3 que restam são as corretas (identidade dos Caminhos novos e mapa de imagens). |
| 25 | Atendido | 9.3 publica a **coluna de DT por faixa** (13/14/15/16/17), diz como ler faixa de inimigo de nível misto, e dá ao **Intellitron** mecânica concreta: faz o teste com **Vantagem** e descobre **duas** Fraquezas em um sucesso. |
| 26 | Atendido | 16.5: "**Ressonância IV:** a sua Ultimate **ativa com 80 de Energia e consome 80**. O teto de Energia continua 100." |
| 27 | Atendido pela primeira opção | 12 abandona a exigência de "exatamente 1 passivo + 1 especial" e declara que cada Raça tem **bônus de atributo mais um ou dois traços**, padronizando a **apresentação** e a precisão das regras em vez da contagem. É a opção fiel ao material que existe, e evita inventar traços para cinco raças. |

#### NIT

| # | Decisão | O que foi feito |
|---|---|---|
| 28 | Atendido | 1: "em 3 lugares e 'distância' em outros 15". 15.2: "em 3 Bênçãos", com os três nomes. |
| 29 | Atendido | 6.1: **20** PV de diferença no nível 1. |
| 30 | Atendido | 5.1: a frase passou a ligar o +1 a cada 2 pontos com os aumentos em +2 de 5.3 ("cada aumento entrega um degrau cheio"). |
| 31 | Atendido | DT 10 mantida (o traço é identidade da raça e merece ser confiável) e a mudança entrou no changelog 21.2, com a observação de que o teste novo soma Eficiência e o original não somava. |
| 32 | Atendido | 7.3: "aplique os **Atrasos** pendentes... **não existe Avanço pendente**". |
| 33 | Atendido | 16.1: Armadura Pesada passa a dar **-2 em Testes e Perícias de Agilidade e -2 de Velocidade**, com a justificativa de escala. 11.4 declara que penalidades de armadura ficam fora da régua de conversão por serem escolha de equipamento. |
| 34 | Atendido | 18.3: a cláusula confusa saiu. A ficha agora lista **Tenacidade (valor máximo)** e **Fraquezas e Resistências**, campo por campo. |
| 35 | Atendido | **Falhe para frente** definida na seção 3, listada na nomenclatura, mandada para o capítulo 02 e para o glossário (descrições de 20 atualizadas), e a linha de 22.1 passou a citá-la como regra nomeada. |
| 36 | Atendido | 6.5: `d20 + (VEL - 10)`, melhor de três trocas, com a proibição explícita de rolar Velocidade contra DT de tabela. |
| 37 | Atendido | 8.1 ganhou a linha **Esforço Total**, o termo entrou na nomenclatura (3) e 8.4 passou a usá-lo em vez de "gastando o turno inteiro". |
| 38 | Atendido | 18.3: "**Inimigos não acumulam Energia** e não têm Ultimate. O equivalente num Boss é uma ação especial com recarga em Ciclos, declarada na ficha dele." |
| 39 | Atendido | 16.4: Corda de Ligação concede Energia **1 vez por combate**, ao entrar na Fila, com o excedente acima de 100 perdido. |
| 40 | Atendido | 9.4 nomeia: o **Implante de Fraqueza** é **uma das 2 Bênçãos novas da Inexistência, tier nível 9+**. |
| 41 | Atendido | 8.2: "a **Ultimate não custa nem gera PH**". |

#### Mudanças que o conserto do achado 5 arrastou (iteração 2)

Publicar as premissas obrigou a mexer em números que o review não pediu diretamente. Registro aqui para o próximo review não tratar como achado novo:

- **Especialização de Combate (mecânica nova, 4.3):** vale em todos os Testes de Ataque. Sem ela, o orçamento de ataque tinha dois valores por personagem (arma e Habilidade, 3 pontos de diferença) e o DPC não podia usar uma taxa de acerto só. **Não é renomeação de nada da v0.1** — está no changelog 21.2 como mecânica nova (item 14).
- **Defesa de inimigo recalibrada** nas faixas 5-8 (16/18/19), 13-16 (20/22/23) e 17-20 (24/26/27), para a janela 70/60/55% valer nas cinco faixas. As faixas 1-4 e 9-12 não mudaram.
- **Teste de Ataque do inimigo** nas faixas 9-12, 13-16 e 17-20 passou a +11/+12/+14, e a **Defesa do PC** nas faixas 9-12 e 17-20 passou a 20 e 23 (valores alcançáveis com a tabela de armaduras e Relíquias), mantendo os 60% de acerto do inimigo cravados.
- **PV de inimigo rededuzido** do DPC novo: Comum 50/70/95/125/155, Elite 120/160/225/295/365, Boss 305/410/580/750/935.
- **Tenacidade de Elite e Boss** ajustada para `2 × redução do grupo por Ciclo` com o mix de ações publicado: Boss 18/20/22/22/24.
- **Composição de encontro e attrition esperada** passaram a ser texto explícito em 18.3, porque sem elas o orçamento `DPC × 4` não diz quantos inimigos colocar na mesa.

### 26.3 O que este documento continua não fechando, de propósito

- As **outras quatro faixas** do DPC abertas linha por linha (só a 17-20 está aberta aqui; o formato está definido e vai para o apêndice 29 durante a escrita, com `simular-combate.ps1` conferindo).
- As **108 Bênçãos** em si. O design fecha cadência, tiers, tetos, recursos e régua de conversão; o texto de cada Bênção é escrita, não design.
- As **fichas de inimigo nominais** do bestiário. O design fecha a ficha padronizada e as âncoras das cinco faixas; os bichos com nome são escrita.
