# Proposta de revisão das Raças — auditoria de design

**Escopo:** as 7 Raças do capítulo 05. **Somente leitura** — nenhum arquivo do projeto foi alterado, nenhum gerador foi rodado. Este arquivo é a única coisa que eu escrevi.
**Base lida:** `livro-v1.0\05-racas.md` inteiro, mais `03`, `04`, `16`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `29`, `30`, o changelog v1.1→v1.2, e o código de `build\` que consome Raça.

---

## 1. Veredito em 5 linhas

1. **Há obrigatoriedade, e ela é estrutural:** **Poder** e **Agilidade** são concedidos por **zero** das 7 Raças. Só o Humano alcança esses dois, porque o bônus dele é livre.
2. Isso explica a sua mesa sem precisar de teoria: quem quer Poder ou Agilidade **não tem escolha de Raça** — tem uma Raça e seis recusas.
3. **Duas Raças não escolhem nada:** Vidyadhara (+2 Vigor) e Intellitron (+2 Sincronia) têm bônus fixo. As outras cinco escolhem entre dois atributos ou livremente.
4. **O Avginiano e o Vidyadhara têm traço que é subconjunto próprio do traço da Xianzhouíta.** A correção E10 da v1.2 desfez a dominância *formal* do Avginiano, mas não deu a ele conteúdo próprio — e deixou passar o Vidyadhara, que é o caso pior.
5. **Recomendo o caminho (A):** toda Raça passa a dar **+2 em um de dois atributos**, com os pares redesenhados para que cada um dos 6 atributos apareça em exatamente **2 Raças**. O Humano fica como está. Custo de código: **baixo** — a ficha já lê os dois atributos direto do livro.

---

## 2. Tabela comparativa das 7 Raças

Bônus citado literalmente de `05-racas.md` (linha indicada).

| Raça | Bônus de atributo (literal) | L. | Traços | Vantagens | Imunidade / efeito único |
|---|---|---|---|---|---|
| **Humano** | "**+2 em um Atributo à sua escolha**, ou **+1 em dois Atributos diferentes**" | 25 | Força de Vontade | — | **Esforço** (1 ponto, rerrola qualquer dado) — exclusivo |
| **Xianzhouíta** | "**+2 em Vigor ou Sincronia**" | 55 | Ad Vitam Aeternam | **Vantagem em qualquer Teste de Resistência** (6 de 6) | **Não pode ser Executado** (23.5) |
| **Vidyadhara** | "**+2 em Vigor**" (fixo) | 82 | Corpo das Marés · Reencarnação Ancestral | Resistência Física **contra afogamento, frio e efeitos de água** | Não morre em definitivo (volta 1 dia depois) |
| **Vulpes** | "**+2 em Discernimento ou Presença**" | 116 | Língua de Prata · Raposa Astuta | Testes de **Presença** (4 Perícias + Força de Vontade) | 2ª chance contra Surpresa (Perc. Mental DT 10) |
| **Haloviano** | "**+2 em Sincronia ou Presença**" | 148 | To na sua mente | — | Aplica **Controlado**, 2×/dia (21.x) |
| **Avginiano** | "**+2 em Discernimento ou Presença**" | 180 | Mente de Ferro | **Resistência Mental, Percepção Mental, Força de Vontade** (3 de 6) | — |
| **Intellitron** | "**+2 em Sincronia**" (fixo) | 210 | Sabedoria de Intellitron | Tecnologia e Mecânica; **descobrir Fraqueza** | 2 Fraquezas por sucesso (20.x) |

Promessa de abertura do capítulo, linha 5: *"Nenhuma Raça é melhor que outra."* Ela é tratada como requisito no changelog (E10 a invoca para justificar a correção do Avginiano). **Hoje ela não se sustenta** — ver seção 5.

---

## 3. Matriz Raça × atributo

`●` = a Raça pode pôr o +2 aqui. `livre` = qualquer um.

| Raça | Poder | Agilidade | Vigor | Sincronia | Discern. | Presença |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Humano | livre | livre | livre | livre | livre | livre |
| Xianzhouíta | | | ● | ● | | |
| Vidyadhara | | | ● | | | |
| Vulpes | | | | | ● | ● |
| Haloviano | | | | ● | | ● |
| Avginiano | | | | | ● | ● |
| Intellitron | | | | ● | | |
| **Raças (fora do Humano)** | **0** | **0** | **2** | **3** | **2** | **3** |

**Os três furos:**

- **Poder: nenhuma Raça.** **Agilidade: nenhuma Raça.** Esta é a raiz do problema. São os dois atributos que o capítulo 04 (§4.1) carrega de conteúdo mais visível na ficha — Agilidade é **Defesa, Velocidade, 3 Perícias e 3 das 6 categorias de arma**; Poder é **capacidade de inventário, Atletismo e 2 categorias de arma**. Quem quer qualquer um dos dois, por qualquer motivo, tem **uma** Raça disponível.
- **Nenhum atributo é concedido por exatamente uma Raça.** Esse furo específico o livro não tem.
- **Nenhum atributo é inútil.** O quadro de §4.1 dá conteúdo concreto aos 6, e o próprio capítulo afirma: *"Nenhum Atributo é inútil para ninguém."* Nenhuma Raça concede atributo morto.

Dois pares são **idênticos**: Vulpes e Avginiano são os dois `+2 em Discernimento ou Presença`. Duas das sete Raças têm a mesma cara numérica.

---

## 4. Crítica de design, Raça por Raça

Aqui está o que você pediu: cada Raça olhada por si, sem comparar DPS.

### Humano — **está boa, não mexer** (com um reparo de texto)

A identidade é exemplar: o **Esforço** é o único recurso do livro que uma Raça traz, o livro declara isso explicitamente (linha 37) e a recarga por crença concreta é a melhor regra de roleplay do capítulo. O bônus livre é coerente com "grande capacidade de adaptação".

Dois reparos, ambos de redação:

- A Característica "**Sem limitações naturais, podendo seguir qualquer Caminho**" sugere que alguma Raça tem limitação de Caminho. **Nenhuma tem** — o capítulo 03, passo 3, manda escolher entre os 9 sem ressalva. A frase promete uma vantagem que não existe porque a desvantagem dela não existe.
- A linha 37 diz que o Esforço "compensa o bônus de atributo livre ser **o mais discreto da lista**". Isso é o contrário da verdade: bônus livre é, por construção, maior ou igual a qualquer bônus restrito. A frase inverte o eixo do balanceamento do próprio capítulo.

### Xianzhouíta — identidade forte, custo declarado que não é custo

`+2 Vigor ou Sincronia`, **Vantagem em todos os 6 Testes de Resistência** e **imunidade à Execução**. O livro admite que é "o traço mais forte da lista" e justifica: *"ela paga por isso não tendo nenhum traço ativo para usar em cena."*

**Essa justificativa não fecha.** Vidyadhara e Intellitron também não têm traço ativo e não recebem nada em troca disso. "Não ter traço ativo" não é moeda se três das sete Raças não têm. O pacote da Xianzhouíta é o maior do capítulo e o preço declarado é zero.

Fora isso, a Raça é bem feita: a ficção (longevidade, corpo que não envelhece, disciplina) e a mecânica (resistir a tudo, não poder ser finalizado) se explicam uma pela outra, e a imunidade à Execução é narrativamente a melhor ideia do capítulo.

### Vidyadhara — **a Raça mais fraca do livro, e por três motivos somados**

1. **Bônus fixo em Vigor**, sem escolha. É o único atributo que a Xianzhouíta também oferece — ou seja, o bônus do Vidyadhara é um subconjunto das opções de outra Raça.
2. **Corpo das Marés é quase letra morta.** Vantagem em Resistência Física *contra afogamento, frio e efeitos de água*, numa campanha de ópera espacial. Em 28 capítulos de livro, zero inimigos do bestiário aplicam afogamento. Depende inteiramente de o Mestre montar a cena de água — e, quando monta, a Xianzhouíta tem a mesma Vantagem **e** todas as outras.
3. **Reencarnação Ancestral é o único conteúdo próprio dele** e o próprio livro pede para você não contar com ela: *"Converse com o Mestre antes de usar isso como plano... você volta um dia depois, e um dia é tempo suficiente para a cena inteira terminar sem você."*

Resultado: a Raça dos dragões, que a ficção descreve com "regeneração", "poderes ancestrais" e "conexão com a água", entrega na mesa **um atributo que você não escolhe e uma Vantagem que raramente é pedida**. Ela precisa de trabalho, e é a que mais precisa.

### Vulpes — **está boa**, com uma incoerência de texto

Dois traços, os dois com gatilho claro e arbitragem óbvia: Língua de Prata cobre 4 Perícias e um Teste de Resistência; Raposa Astuta tem DT fixa escrita, aparece citada em 19.x como segunda chance do teste de Surpresa, e o "não pode mais ser surpreendido pelo resto da cena" é uma recompensa legível. É o melhor pacote de traços do capítulo em relação custo/clareza.

A incoerência: a Característica diz "**Grande agilidade e percepção**" e o bônus **não pode dar Agilidade**. A Raça que o livro descreve como a ágil é uma das seis que não conseguem comprar Agilidade.

### Haloviano — bom conceito, com uma armadilha e um acoplamento a Caminho

É a **única Raça com traço ativo de combate**, e Controlado é, pelo texto de 21.x, um dos efeitos mais fortes do jogo. A estrutura em três passos (ativação → resistência do alvo → efeito) é clara, tem DT escrita e limites declarados (não funciona em Boss em clímax, duração menor contra Elite e Boss). Bem construído.

Dois problemas:

- **A falha na ativação queima o dia inteiro, não o uso.** O texto: *"faça um Teste de Sintonia contra DT 13; se falhar, você não pode usar este traço até o próximo Descanso Longo."* Numa primeira tentativa com 60-70% de sucesso, a expectativa é de **1,2 de 2 usos**; com Sintonia ruim (40%), **0,56 de 2**. O traço cobra um dia por um dado ruim.
- **A Raça empurra para um Caminho.** Quem segue a Harmonia **não faz o teste** e recebe 2 usos garantidos. É exatamente o seu incômodo invertido: aqui não é o arquétipo que obriga a Raça, é a Raça que premia um Caminho entre nove.

### Avginiano — depois de E10, deixou de ser dominado, mas continua sem cara própria

A correção da v1.2 funcionou no que se propôs: com `Discernimento ou Presença` contra `Vigor ou Sincronia`, as duas Raças deixaram de ser comparáveis ponto a ponto, e a dominância **formal** acabou. Mas ela resolveu o eixo errado para a pergunta que você está fazendo agora:

- **Mente de Ferro continua sendo um subconjunto próprio de Ad Vitam Aeternam.** Três dos seis Testes de Resistência contra seis de seis. O Avginiano não tem **nenhuma** linha mecânica que a Xianzhouíta não tenha, exceto a escolha de atributos.
- **O par de atributos é idêntico ao do Vulpes.** Então, das sete Raças, a que tem a mesma cara numérica do Vulpes tem o traço que é versão menor do da Xianzhouíta.
- **Duas das três Características não têm tradução mecânica nenhuma:** "instinto de sobrevivência elevado" e "facilidade para negociação" não aparecem em regra alguma. Só "grande resistência psicológica" virou Mente de Ferro.

A ficção do Avginiano é a mais forte do capítulo (povo perseguido, escravizado, cultura destruída, errante, comerciante). A mecânica entrega um terço dela.

### Intellitron — **está boa**, com dois reparos

A identidade é nítida e insubstituível: é o especialista em informação, e o traço dele aumenta o dano **do grupo inteiro** (descobrir Fraqueza vale +2 dados para todos, por 20.x). O livro já o tratou bem na v1.0, quando transformou o monopólio dele em especialidade. Citado em 20.x e em 27.x como lembrete de mesa — é um traço que a mesa usa.

Reparos:

- **Bônus fixo em Sincronia**, a mesma rigidez do Vidyadhara.
- **O terceiro item do traço é vago demais para arbitrar:** *"Fora de combate, o mesmo tipo de teste — Pesquisa, Ciência ou Sintonia — contra a DT da cena — serve para arrancar uma **pista** sobre algo que você queira saber, a critério do Mestre."* Sem frequência, sem limite, sem definição de "pista". Na mesa isso é ou nunca usado ou usado sem teto, e nos dois casos o Mestre fica sem régua.
- **"Não sofrem com doenças naturais"** está nas Características, lido como regra, e não é regra nenhuma.

---

## 5. Dominância e traços fora da curva

| # | Achado | Severidade |
|---|---|---|
| **D1** | **Poder e Agilidade: zero Raças.** Humano é a única porta para os dois. É o defeito que gerou o seu pedido. | **Alta** |
| **D2** | **Vidyadhara perde da Xianzhouíta em todo eixo mecânico**: bônus é subconjunto das opções dela (Vigor); Corpo das Marés é subconjunto próprio de Ad Vitam Aeternam; a Xianzhouíta ainda tem imunidade à Execução. O único eixo em que o Vidyadhara ganha é Reencarnação Ancestral, que o próprio livro manda não planejar. Pela **letra** do critério E10 ("melhor em nenhum eixo") não é dominância estrita; pelo **espírito**, é o mesmo defeito que E10 corrigiu — e o pior caso restante. | **Alta** |
| **D3** | **Mente de Ferro ⊂ Ad Vitam Aeternam** (3 de 6 contra 6 de 6). Não é mais dominância formal, mas o Avginiano não tem conteúdo mecânico próprio. | **Alta** (identidade) |
| **D4** | **Vulpes e Avginiano têm o par de atributos idêntico** e nichos sobrepostos (resistir a efeito mental / ser bom socialmente). Duas de sete Raças ocupando o mesmo lugar. | **Média** |
| **D5** | **Ad Vitam Aeternam está acima da curva** e o custo declarado ("não tem traço ativo") não é custo — Vidyadhara e Intellitron também não têm. **A promessa "nenhuma Raça é melhor que outra" não se sustenta hoje.** | **Média** |
| **D6** | **"To na sua mente": falha na ativação custa o dia.** Vira armadilha para 8 dos 9 Caminhos e premia a Harmonia. | **Média** |
| **D7** | **Corpo das Marés é quase letra morta** no gênero do livro. | **Média** |
| **D8** | **Terceiro item da Sabedoria de Intellitron é inarbitrável** (sem frequência, sem limite, sem definição). | **Baixa** |
| **D9** | **Características que prometem regra e não entregam:** Humano "podendo seguir qualquer Caminho" (nenhuma Raça tem restrição); Intellitron "não sofrem com doenças naturais"; Avginiano "instinto de sobrevivência" e "facilidade para negociação". | **Baixa** |
| **D10** | Linha 37: o bônus livre do Humano descrito como "o mais discreto da lista". É o mais flexível, logo o maior em valor de opção. | **Baixa** |

### Sobre a promessa de abertura

A frase da linha 5 — *"Nenhuma Raça é melhor que outra"* — é forte demais para ser verdade em qualquer jogo com traços assimétricos, e o capítulo não precisa dela. O que o capítulo **pode** prometer e cumprir é: **nenhuma Raça é escolha ruim, e nenhuma é obrigatória para um conceito.** Recomendo trocar a frase (item 14 da seção 7). É uma linha, propagação zero, e para de criar uma dívida que toda revisão futura vai ter que pagar.

---

## 6. Os quatro caminhos, comparados

O problema central é que os seus critérios 2 e 3 brigam: se toda Raça serve igualmente para tudo, a escolha de Raça deixa de significar algo mecanicamente; se cada Raça é especializada, ela vira pré-requisito. A saída não é escolher um extremo — é decidir **onde** mora a identidade. Hoje ela mora no bônus de atributo, e é por isso que o bônus está te travando.

| | O que é | Prós | Contras |
|---|---|---|---|
| **(A) Bônus flexível** | Toda Raça dá `+2 em um de dois atributos`, com os pares redesenhados para cobrir os 6 | Padrão que o livro **já usa** em 4 das 7 Raças — zero vocabulário novo. O par continua sendo parte da cara da Raça (6 pares distintos). Fecha o furo de Poder/Agilidade. **A ficha automatizada já suporta: `ficha_dados.racas()` extrai as duas opções do próprio texto do livro.** | Não resolve sozinho os traços fora da curva (D2, D3, D5, D6) — precisa dos itens de traço junto |
| **(B) Bônus livre** | Toda Raça dá `+2 em qualquer atributo`; identidade 100% nos traços | O mais simples de explicar. Flexibilidade máxima | **Apaga a cara numérica das 7 Raças de uma vez** e, pior, **destrói metade do design do Humano**: o bônus livre é a identidade dele. E é o caminho **mais caro em código**: `gerar_ficha.py` codifica `{RACA}="Humano"` em ~8 fórmulas para distinguir o modo livre (linhas ~904-941 e 1022-1024); todas teriam de passar a ler uma flag |
| **(C) Bônus dividido** | `+1 fixo` + `+1 livre` | Preserva identidade e destrava arquétipo ao mesmo tempo. Elegante no papel | **Briga com a tabela de Bônus do próprio livro.** §4.2 diz: *"+1 a cada 2 pontos... é exatamente por isso que os aumentos por nível vêm em +2: cada aumento entrega um degrau cheio, nunca meio degrau perdido."* No array oficial (15,14,13,12,10,8), um +1 só rende degrau em **14** e **13**; em 15, 12, 10 e 8 ele é **meio degrau jogado fora**. Você estaria criando exatamente a armadilha que a v1.2 foi feita para remover — e que exige o jogador decorar a tabela de bônus para não cair nela. Além disso, pede um **terceiro modo** de bônus na ficha (hoje são dois: fixo/escolha e livre do Humano) |
| **(D) Manter fixo e só redistribuir** | Bônus fixo em todas, redistribuídos para cobrir os 6 | Identidade máxima, leitura mais simples | **Não resolve o seu problema, só o move.** Com um atributo por Raça, quem quer Agilidade continua tendo 1 ou 2 Raças, e a escolha continua sendo decidida pelo número. Ainda exige reescrever todos os 7 bônus — mesmo custo de texto do (A) por menos resultado |

### Recomendação: **(A)**, com os pares redesenhados e os reparos de traço da seção 7

O raciocínio em uma frase: **(A) é o único que fecha o furo sem inventar vocabulário novo, sem criar meio degrau perdido e sem apagar a diferença entre as Raças** — porque com 6 pares distintos entre 6 atributos, o par continua sendo um traço da Raça, e ainda assim nenhum atributo fica atrás de uma única porta.

E a tensão entre os seus critérios 2 e 3 se resolve assim: **a identidade sai do número e vai para o traço.** O bônus passa a dizer "para onde esta Raça tende"; o traço passa a dizer "o que só esta Raça faz". É por isso que a proposta da seção 7 não para no bônus — se eu mexesse só nos números, o Avginiano e o Vidyadhara continuariam sem motivo para existir.

---

## 7. Proposta concreta, item por item

Numerada para você aprovar ou recusar cada uma. Os itens **1 a 7** são o bônus (aprovar em bloco ou não aprovar — eles formam um sistema fechado, ver nota no fim). Os **8 a 16** são independentes entre si.

### Os bônus — cobertura 2 Raças por atributo

Cada atributo aparece em exatamente 2 Raças, e nenhum par se repete:

| Atributo | Raças que concedem |
|---|---|
| Poder | **Vidyadhara, Intellitron** |
| Agilidade | **Vulpes, Avginiano** |
| Vigor | Xianzhouíta, **Vidyadhara** |
| Sincronia | Xianzhouíta, **Intellitron** |
| Discernimento | **Vulpes, Haloviano** |
| Presença | **Haloviano, Avginiano** |

---

**1. Humano — não mexer.** Bônus permanece, **com a frase literalmente intacta** (ela é âncora de teste, ver seção 8):

> **Bônus de atributo:** **+2 em um Atributo à sua escolha**, ou **+1 em dois Atributos diferentes**.

**2. Xianzhouíta — não mexer.** Permanece `+2 em Vigor ou Sincronia`. É a Raça mais citada fora do capítulo 05 (22.6, 23.5, 28, 30, ficha, Planilha do Mestre) e o par dela já é coerente com a ficção. Mexer aqui custa caro e rende pouco.

**3. Vidyadhara — `+2 em Vigor` → `+2 em Vigor ou Poder`.**

> **Bônus de atributo:** **+2 em Vigor ou Poder**.

*Por quê:* resolve a rigidez (D1, parcialmente D2) e é a ficção mais direta do capítulo para Poder — são dragões humanoides, e Poder é "força física, impacto" (§4.1). Dá a eles o primeiro atributo que a Xianzhouíta não oferece.

**4. Vulpes — `+2 em Discernimento ou Presença` → `+2 em Agilidade ou Discernimento`.**

> **Bônus de atributo:** **+2 em Agilidade ou Discernimento**.

*Por quê:* é literalmente a Característica que já está escrita na linha 112 — "**Grande agilidade e percepção**". A Raça passa a entregar o que o próprio texto dela promete, e o par deixa de ser idêntico ao do Avginiano (D4).
*A perda:* o Vulpes não compra mais Presença, embora Língua de Prata seja um traço de Presença. Eu considero isso uma **melhora**: a Raça fica boa em Presença **sem precisar do número**, que é a definição prática de "fazer um pouco de tudo". Se você preferir o contrário, o par alternativo é `Agilidade ou Presença` — mas nesse caso o Discernimento precisa ir para o Avginiano, e o item 6 muda junto.

**5. Haloviano — `+2 em Sincronia ou Presença` → `+2 em Discernimento ou Presença`.**

> **Bônus de atributo:** **+2 em Discernimento ou Presença**.

*Por quê:* a ficção é "sensibilidade emocional, poderes ligados à mente e aos sonhos" — Discernimento é "instinto, atenção, intuição e força mental" (§4.1). Casa melhor que Sincronia. E o traço continua funcionando: o Teste de Sintonia da ativação pode somar **Discernimento ou Sincronia** (§4.4), e a DT do alvo lê o Atributo de Habilidade, que na Harmonia é Presença e na Euforia é Presença ou Discernimento — ou seja, o par novo alinha com os dois Caminhos mais naturais da Raça.

**6. Avginiano — `+2 em Discernimento ou Presença` → `+2 em Agilidade ou Presença`.**

> **Bônus de atributo:** **+2 em Agilidade ou Presença**.

*Por quê:* é o item que finalmente dá cara própria ao Avginiano (D3, D4) e **traduz em regra duas Características que hoje são letra morta** (D9): "instinto de sobrevivência elevado" → Agilidade; "facilidade para negociação" → Presença. É um povo errante e perseguido; reflexo e lábia são exatamente o que ele deveria ter.

**7. Intellitron — `+2 em Sincronia` → `+2 em Sincronia ou Poder`.**

> **Bônus de atributo:** **+2 em Sincronia ou Poder**.

*Por quê:* resolve o último bônus fixo e é coerente com "corpo mecânico ou sintético" — um chassi de combate. Sincronia continua sendo a primeira opção, então a identidade de processador não se perde.

---

### Os traços

**8. Vidyadhara — reescrever Corpo das Marés** (D7). Mantém o gatilho condicional (barato na ficha), amplia o alcance e acrescenta uma utilidade sempre ligada:

> ### Traço — Corpo das Marés
>
> Você tem **Vantagem em Testes de Resistência Física** contra **afogamento, frio, veneno e efeitos de água**, e você **respira debaixo d'água indefinidamente**.

*Por quê:* "veneno" é uma categoria que o capítulo 22 e a Perícia Resistência já usam, então a cena aparece. Respirar debaixo d'água é a única linha do capítulo 05 que a Xianzhouíta não cobre — é o primeiro conteúdo mecânico próprio do Vidyadhara fora da Reencarnação.

**9. Avginiano — acrescentar uma linha à Mente de Ferro** que a Xianzhouíta não tem (D3):

> ### Traço — Mente de Ferro
>
> *(os três Testes de Resistência mentais continuam exatamente como estão)*
>
> - Além disso: **quando você falha** num Teste de Resistência contra medo, ilusão, manipulação ou controle, **a duração do efeito sobre você cai pela metade** (arredonda para baixo, mínimo 1 turno).

*Por quê:* é a linha que faz Mente de Ferro **deixar de ser subconjunto** de Ad Vitam Aeternam. Não inventa número novo (metade/arredonda para baixo/mínimo 1 é a régua que 16.4 e 22.4 já usam), não dá bônus de rolagem, e é exatamente a ficção da Raça: *"sobreviver ao que não deu para evitar"*. Se você preferir não acrescentar nada, a alternativa é o item 10.

**10. *(alternativa ao 9, mais barata, mais agressiva)* Xianzhouíta — restringir Ad Vitam Aeternam aos três Testes de Resistência físicos** (Potência Física, Reflexos, Resistência Física), mantendo a imunidade à Execução.

*Por quê:* vira o espelho exato do Avginiano (3 físicos × 3 mentais), resolve D3 e D5 de uma vez, e é a leitura mais fiel da ficção ("o corpo que não envelhece"). **Eu não recomendo este item**, por três razões: (a) é o único da lista que **enfraquece** algo que funciona, contra a sua instrução de não mexer no que está funcional; (b) tira a Xianzhouíta do quadro de 23.5 ("Morrendo com Vantagem"), que é o ponto de maior propagação do capítulo — bate em `23-dano-cura-e-morte.md`, `22-testes-de-resistencia.md`, `oraculo_ficha.VANTAGEM_MORRENDO`, `oraculo_mestre_livro.MORRENDO_VANT` e nos testes dos dois lados; (c) o item 9 chega ao mesmo lugar subindo o piso em vez de baixar o teto. Deixo numerado porque é uma decisão sua, não minha.

**11. Haloviano — falha na ativação gasta o uso, não o dia** (D6):

> 1. **Ativação.** Se você segue o **Caminho da Harmonia**, não há teste de ativação. Caso contrário, faça um **Teste de Sintonia contra DT 13**; se falhar, **este uso é gasto** e nada acontece.

*Por quê:* tira a armadilha sem tirar o custo (você gastou a Ação Complementar e um dos dois usos) e sem tocar na DT 13, que é uma das cinco DTs de subsistema e está citada em 02 e 27. A vantagem da Harmonia continua existindo e fica legível: ela não rola. Com isso, 8 dos 9 Caminhos passam a ter um traço confiável em vez de um bilhete de loteria diário.

**12. Intellitron — delimitar o terceiro item da Sabedoria** (D8):

> - Fora de combate, **uma vez por cena**, o mesmo tipo de teste — **Pesquisa, Ciência ou Sintonia** contra a DT da cena — serve para arrancar **uma pista concreta** sobre algo que você queira saber: um nome, um lugar, uma data ou uma relação entre duas coisas. O Mestre escolhe qual.

*Por quê:* "uma vez por cena" é a mesma régua que 24.7 já usa para item que concede Vantagem, e "um nome, um lugar, uma data ou uma relação" dá ao Mestre o que arbitrar. Nenhum número novo.

**13. Intellitron — transformar "não sofrem com doenças naturais" em regra ou em sabor** (D9). Recomendo regra, porque é uma linha e fecha a ficção:

> - Você é **imune a doença natural** e a **veneno de origem biológica**. Toxina sintética, nanomáquina e gás de combate afetam você normalmente.

*Por quê:* a segunda frase é o que impede isso de virar imunidade ampla. Se você preferir sabor puro, basta reescrever a Característica como "Não adoecem" e não citar imunidade.

---

### Redação do capítulo

**14. Trocar a promessa da linha 5.** De:

> Nenhuma Raça é melhor que outra.

Para:

> Nenhuma Raça é escolha ruim, e nenhuma é obrigatória para um conceito: todo atributo do jogo é oferecido por **duas** Raças diferentes, além do bônus livre do Humano. O que distingue uma Raça da outra não é o tamanho do bônus — é para onde ele tende e o que o traço dela faz.

*Por quê:* a frase atual é uma promessa de simetria que nenhum jogo com traços assimétricos cumpre, e o changelog já a usou como requisito uma vez (E10). A nova é verificável e é exatamente o que a proposta entrega.

**15. Corrigir a Característica do Humano** (D9). De "Sem limitações naturais, podendo seguir qualquer Caminho" para:

> - Adaptável a qualquer cultura, planeta ou ofício.

*Por quê:* nenhuma Raça tem restrição de Caminho; a frase anuncia uma vantagem inexistente.

**16. Corrigir a nota da linha 37** (D10). Trocar o fecho "é o que compensa o bônus de atributo livre ser o mais discreto da lista" por:

> Não é esquecimento: é a identidade da Raça. O Humano é o único que escolhe livremente onde vai o bônus, e o Esforço é o único recurso que uma Raça traz para a mesa — as duas coisas dizem a mesma coisa sobre ele.

---

> **Nota sobre os itens 1 a 7:** eles formam um sistema fechado — a cobertura "2 Raças por atributo" só fecha com os sete juntos. Se você recusar um, me diga qual e eu remonto a distribuição; recusar um isoladamente reabre um furo (ex.: recusar o 6 deixa a Agilidade com uma única Raça, que é o defeito D1 em escala menor).

---

## 8. Custo de propagação e de migração

### Livro

| Arquivo | O que muda | Linhas |
|---|---|---|
| `livro-v1.0\05-racas.md` | 5 linhas de bônus (itens 3-7); traços (8, 9, 11, 12, 13); promessa (14); Características (15 e 13); nota (16); **e a Tabela de consulta rápida** | 82, 116, 148, 180, 210 · 84-86, 150-156, 182-190, 212-216 · 5 · 22 e 207 · 37 · **224-232** |
| `livro-v1.0\22-testes-de-resistencia.md` | §22.6, linha do Vidyadhara (item 8 muda o texto da Vantagem) | 168 |
| `livro-v1.0\00-changelog-v11-para-v12.md` | **Decisão sua:** a v1.2 já está publicada (`.docx` e `.pdf` V1.2 na raiz). Isto é changelog novo (E20+ na v1.2, ou abrir v1.3) | — |

**Não mudam** (verifiquei um a um): `03` (linha 44 lista nomes; linha 244 da Nadir usa o bônus livre do Humano, que fica intacto) · `04` · `19`, `20`, `21` (citam gatilhos de traço, e nenhum gatilho muda) · `23.5` (o quadro "Morrendo com Vantagem" nomeia Xianzhouíta, Vulpes e Avginiano — as três mantêm Vantagem em Força de Vontade na proposta recomendada; **muda só se você aprovar o item 10**) · `27` e `02` (DTs de subsistema 10 e 13 ficam) · `29` · `30` · `28`.

### Ficha do jogador

A boa notícia: **a redistribuição de bônus é quase toda automática.** `build\ficha_dados.py::racas()` (linha 162) lê a Tabela de consulta rápida do capítulo 05 e extrai as opções com `atributos_em()` (linha 152), que devolve os atributos **na ordem em que aparecem no texto**. Mudar `+2 em Vigor` para `+2 em Vigor ou Poder` no livro já produz `opcao1=Vigor, opcao2=Poder` na aba Dados, sem tocar em código.

| Arquivo | O que muda | Linhas |
|---|---|---|
| `build\oraculo_ficha.py` | **Obrigatório.** O dict `RACAS` codifica as tuplas à mão: 5 entradas mudam | 53-61 |
| `build\oraculo_ficha.py` | Só com o item 8: `VANTAGEM_TR_CONDICIONAL` (texto do Vidyadhara) | 146 |
| `build\oraculo_ficha.py` | Só com o item 10: `VANTAGEM_TR` e `VANTAGEM_MORRENDO` | 143-147 |
| `build\ficha_dados.py` | `TRANSCRITO["vantagens_raciais"]` — **os campos `ancora` são frases literais do capítulo 05 e o teste confere que elas existem no livro.** O item 8 muda a âncora do Vidyadhara; os itens 9/12/13 mudam as do Avginiano/Intellitron | 691-705 |
| `build\gerar_ficha.py` | `EJ_VANTAGENS_CURTAS` — texto curto por Raça, com **teste de largura** (cabe em B:D) | 3000-3006 |
| `build\gerar_ficha.py` | **Nada a mudar nas fórmulas de bônus.** Os `{RACA}="Humano"` (904-941, 1022-1024) continuam corretos porque o Humano segue sendo a única Raça de bônus livre — **este é o motivo técnico de o caminho (A) ser o mais barato e o (B) o mais caro** | — |
| `build\ficha_mapa.json`, `build\ficha_protegidos.json` | **Gerados.** `ficha_protegidos.json` guarda o sha256 de **todo** `.md` do livro, inclusive `05-racas.md` — a suíte `protegidos` falha até ser regravada | — |
| `ficha-automatizada\*.xlsx` | Regerar | — |

### Planilha do Mestre

| Arquivo | O que muda |
|---|---|
| `build\mestre_dados.py` (928-932, 976, 1003) | **Nada.** Deriva de `F.racas()` — só os nomes das Raças, que não mudam |
| `build\oraculo_mestre_livro.py` (70-71) | `RACAS` é lista de **nomes** → nada. `MORRENDO_VANT` → só com o item 10 |
| `build\oraculo_mestre_abas.py` (49-53), `oraculo_mestre_cmb.py` (81) | **Nada** — leem `Xianzhouíta`/`Humano`/`Intellitron` por nome, para Execução, Esforço e Fraqueza. Nenhum dos três muda na proposta recomendada |
| `build\mestre_sabor_nomes.py`, `oraculo_mestre_hist.py` | **Nada** — só geração de nomes por cultura |
| `build\mestre_mapa.json` | Gerado, regerar |

### Suítes que quebram

Rodando `python build\testar_ficha.py --suite tudo` (11 suítes) e `python build\testar_mestre.py --suite tudo` (13 suítes):

1. **`protegidos`** — falha garantida: o sha256 de `05-racas.md` (e de `22-...md`) muda. Regravar com `--suite protegidos`.
2. **`extremos`, caso "bônus racial fora das opções"** — `testar_ficha.py:2281-2282` usa `Vidyadhara` + `Poder` como o bônus inválido. **Com o item 3, Poder passa a ser válido e o teste deixa de detectar o que deveria.** Trocar o atributo inválido (ex.: `Presença`).
3. **`ouro`, mesmo caso** — `testar_ficha.py:3010`, idem.
4. **`dados`, âncoras do transcrito** — `testar_ficha.py:~1322` confere `item["ancora"] in _md(item["cap"])` para cada entrada de `vantagens_raciais`. Quebra com os itens 8, 9, 12 e 13 até as âncoras serem reescritas.
5. **`dados`, texto dos traços** — `testar_ficha.py:1262-1281` confere frase por frase que o texto da aba existe no capítulo 05. Passa sozinho depois de regerar, porque os dois lados leem o livro.
6. **`lint`/largura** — `testar_ficha.py:3508-3509` mede se cada `EJ_VANTAGENS_CURTAS` cabe em B:D. Textos novos precisam caber.
7. **Cobertura perdida, não falha:** `testar_ficha.py:2641-2651` tem um ramo `elif len(opcoes) == 1` ("a Raça de opção única aplica sozinha"). Com os itens 3 e 7, **nenhuma Raça tem opção única** e esse ramo morre — junto com a cobertura da fórmula `criacao.raca.escolhido` de `gerar_ficha.py:904-905`, que trata `op2=""`. Vale manter um caso sintético para não perder o teste.
8. **`lexico`** — `ficha_lexico_extra.txt` e `mestre_lexico_extra.txt` podem precisar de palavras novas (o item 13 introduz "nanomáquina").

Nada na economia central é tocado: dados base de arma, progressão, PV, PH, Energia, DTs, orçamento de encontro e bestiário ficam idênticos.

### Custo de migração para os personagens em jogo

**Praticamente zero, e esse é um argumento a favor do caminho (A).**

- Sua mesa é toda **Humano**, e o **item 1 não muda nada no Humano**. Nenhuma ficha em jogo precisa ser recalculada. Nenhum atributo, PV, Defesa, Velocidade, Perícia ou DT se altera.
- Se alguém tiver personagem **Vidyadhara ou Intellitron** com o `+2` fixo: o bônus antigo continua sendo uma das duas opções novas. **Nada a fazer.**
- Para **Vulpes, Haloviano e Avginiano** já em jogo, o atributo escolhido pode ter saído da lista. Regra de transição sugerida, uma linha: *"personagem criado antes da v1.3 mantém o bônus que tem, ou, se preferir, pode remanejá-lo para uma das opções novas da Raça dele, uma única vez, no próximo Descanso Longo."* É o mesmo mecanismo que 16.8/23.6 já usam para recriar Habilidade.
- Um detalhe para você saber antes de aprovar: **a quantidade de Perícias escolhidas é fixada na criação** com o Bônus de Sincronia daquele momento (§4.5). Se alguém remanejar um bônus **para fora** da Sincronia, o número de Perícias **não** diminui pela regra escrita. Vale dizer isso em voz alta na mesa; não é preciso mudar o livro.
- O item 11 (Haloviano) é puro ganho para quem está jogando. O item 10, se aprovado, é a única perda de ficha da lista — e sua mesa não tem Xianzhouíta.

---

## 9. O que eu não consegui verificar

- **Nada foi executado.** Não rodei `testar_ficha.py` nem `testar_mestre.py`, não gerei PDF/DOCX/XLSX e não rodei git. A lista de suítes que quebram vem de leitura do código dos testes (linhas citadas), não de execução. Os itens 1, 2 e 3 dessa lista eu considero certos; os outros são prováveis.
- **Não abri os `.xlsx` nem o `.gsheet`.** As afirmações sobre a ficha vêm dos geradores (`gerar_ficha.py`, `ficha_dados.py`, `oraculo_ficha.py`) e do `ficha_mapa.json`, não do arquivo renderizado. Se houver conteúdo escrito à mão na planilha publicada, ele não está coberto aqui.
- **Não li a pasta `Explorando Galáxias RPG - Players\` nem `versões antigas\`**, conforme a proibição. Se existir material de Raça lá (resumo de mesa, encarte), ele precisa de uma passada separada.
- **Não li `Mestre\`** (pasta na raiz, fora de `build\mestre\`). Se houver planilha ou texto com as Raças ali, não está no mapa de propagação.
- **Peso real dos traços na sua mesa.** Eu estimei a relevância do Corpo das Marés e do Raposa Astuta pela frequência com que o gênero do livro e o bestiário produzem essas cenas. Quem sabe se o traço aparece é você — se na sua campanha há água e emboscada toda sessão, D7 cai de média para baixa.
- **A decisão v1.2 vs v1.3.** Os `.docx`/`.pdf` V1.2 já estão na raiz, o que sugere v1.2 fechada. Se ela ainda não foi distribuída, isto entra como E20+ na v1.2; se foi, pede changelog novo. Essa é sua chamada, não minha.
