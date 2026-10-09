# Achados da auditoria v1.2 — opções-armadilha, dominância e contradições de obrigatoriedade

Raiz: `g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG`
Etapa: **FEAT-001 concluído.** As correções abaixo marcadas como aplicadas já estão nos `.md` do livro.

## Régua da auditoria

- **Defeito A — opção-armadilha / dominância:** a opção só cobra e não entrega nada, **ou** é **dominada** por outra opção da mesma lista — igual ou pior em **todo** eixo, melhor em nenhum.
- **Defeito B — contradição de obrigatoriedade/limite:** dois capítulos discordam sobre se uma escolha é obrigatória, ou sobre o número que a limita.
- **Custo não é defeito.** PH, Energia, Espaço, Créditos, uma ação, uma desvantagem: design normal, desde que a opção entregue algo.
- **Diferença de potência que vem de um trade declarado é design, não defeito.** Mais dano por menos alcance, mais defesa por menos Velocidade: não se mexe.

## Guardas que a autoridade ampliada impôs, e que foram respeitadas

**A economia central não foi tocada.** Continuam idênticos à v1.1: dados base de toda categoria de arma, tabela de progressão (26.2), PV por nível (06.4), totais e geração de PH (16.2), fontes e total de Energia (17.2), orçamento de encontro e DTs (27), números do bestiário (28) e os Danos de Quebra de 20.5. As restrições anteriores também: nenhuma propriedade de arma aumenta dados base, nada dá bônus numérico de combate nem ação/Reação/Avanço/Atraso, nada cura mais que a Poção Grande.

**Ordem de preferência usada em cada correção:** (i) transformar bônus fixo em escolha, seguindo padrão que o livro já usa; (ii) ajustar um número já existente para a paridade da lista; (iii) corrigir a redação quando o defeito é só promessa não cumprida. Mecânica nova só onde nada disso resolvia — aconteceu **uma vez** (B6, e com o texto aprovado pelo autor).

---

## 1. Decisões do autor

| Ponto | Decisão | Situação |
|---|---|---|
| **A2 — Raio dominado pelo Fogo** | **Opção 2 aprovada:** Choque passa a durar **3 turnos**; Dano de Quebra do Raio intacto; e a frase de 20.1 passa a alocar o Raio num grupo, explicando o trade honestamente | **Aplicado** |
| **A3 — Avginiano dominado pelo Xianzhouíta** | **Opção 2 aprovada:** bônus vira `+2 em Discernimento **ou** Presença`; sem traço novo; a frase "Nenhuma Raça é melhor que outra" **fica** | **Aplicado** |
| **Planilha do Mestre** | **Escopo mudou:** ela vai para **V1.2**, não fica em V1.1. A V1.1 fica no disco, intacta | **Repassado** ao FEAT-002 (strings e caminho de saída) e ao FEAT-003 (geração + `testar_mestre.py`) |
| **B6 — condição de recarga de Habilidade** | **Aprovado o texto com número:** uma vez por combate por **1 PH menos**, piso de 1 PH, declarado na criação, sem mexer nos dados da linha do Nível, registrado na Ficha de Decisões | **Aplicado** em 16.7, com a linha de 16.8 apontando para lá |
| **Autoridade ampliada** | Análise de dominância completa de toda lista de escolha, com permissão de mexer em número sem pausar, dentro das guardas acima | **Executada** — seções 2, 3 e 4 |

### Reconferência que o autor pediu: a dominância do Avginiano sobreviveu?

**Não.** Com o bônus em escolha, o eixo de atributo deixa de ser comparável: o Avginiano escolhe entre **Discernimento e Presença**, o Xianzhouíta entre **Vigor e Sincronia** — nenhum dos dois cobre o do outro, então não existe mais "igual ou melhor em todo eixo". A Mente de Ferro continua sendo subconjunto da Vantagem do Xianzhouíta, e isso é legítimo: o Xianzhouíta paga por ela com um par de atributos que não serve a quem quer Discernimento ou Presença.

Também conferi o par que a mudança criou, porque o Avginiano passou a ter **o mesmo par de atributos do Vulpes**: os dois são incomparáveis. O Vulpes cobre as quatro Perícias de Presença e tem segunda chance contra a Surpresa; o Avginiano cobre **Resistência Mental e Percepção Mental**, que o Vulpes não cobre. Nenhum domina o outro. **Nenhuma correção adicional foi necessária.**

---

## 2. Todos os números alterados no livro

É a lista completa da minha mão no sistema. Cinco entradas, todas dentro de uma lista de opções.

| # | Lista a que pertence | Onde | Antes | Depois | Motivo |
|---|---|---|---|---|---|
| **1** | As 7 condições de Quebra (um Elemento cada) | `21-condicoes.md` §21.2 e §21.5, verbete **Choque** | Duração **2 turnos** | Duração **3 turnos** | A2: o Raio era dominado pelo Fogo em dano de Quebra **e** em Dano Contínuo, com duração e acúmulo idênticos. Decisão do autor. O Dano de Quebra do Raio (`1d6 + Eficiência`, 20.5) **não mudou** |
| **2** | As 7 Raças | `05-racas.md`, Avginiano (seção e tabela de consulta rápida) | `+2 em Discernimento`, fixo | `+2 em Discernimento **ou** Presença` | A3: dominância pelo Xianzhouíta. Segue o padrão de 4 das 7 Raças (regra (i): bônus fixo → escolha). Decisão do autor |
| **3** | As 6 categorias de arma | `24-equipamentos.md` §24.2, linha **Leve** | Espaço **1** | Espaço **0,5** | A6 (novo): com 1 de Espaço, a Leve era dominada pela Média — mesmo Espaço, mesmo alcance, atributo que inclui Agilidade, e **1d10** contra 1d8. Regra (ii): ajuste de um número existente, **fora** da economia central. Os **dados base não foram tocados** (continua 1d8), e o preço também não |
| **4** | As 4 propriedades de arma | `24-equipamentos.md` §24.2, **Arremessável** | "lançada a **um** alcance acima do normal da categoria" | "lançada a **dois passos** acima do alcance normal da categoria, no máximo **Extrema**" | A7 (novo): era dominada por **Alcance estendido**, que dá o mesmo passo e **não** te deixa sem a arma. Regra (ii). Não dá bônus numérico de combate, não dá ação, não mexe em dados base |
| **5** | Os campos opcionais de uma Habilidade (checklist 16.8) | `16-habilidades.md` §16.7 (régua nova) e §16.8 (linha do checklist aponta para ela) | A troca existia no checklist e **não era definida em lugar nenhum** | **Uma vez por combate** em troca de **1 PH menos**, piso de **1 PH** | B6: a linha do checklist estava correta mas órfã. Mecânica nova, única da auditoria, com o texto aprovado pelo autor. Não mexe nos dados da linha do Nível, e Habilidade de Nível 1 ou 2 não tem o que trocar |

**Uma linha estrutural, não numérica:** a propriedade **Recarga** saiu da tabela de 24.2 (A1), que passou a ter 4 linhas.

### Efeito colateral registrado — vale um "sim" do autor quando sobrar tempo

Com a arma **Leve** em 0,5 de Espaço, a propriedade **Dissimulada** numa arma Leve passa a entregar só a metade útil dela (passar por busca superficial), porque o 0,5 de Espaço já vem de graça. **Dissimulada continua não sendo dominada** — ela vale em qualquer das seis categorias e o "passa por busca" é exclusivo dela —, mas o alcance dela encolheu um pouco para quem joga Leve. É o preço de desarmar a dominância da Leve sem tocar nos dados base. **Mudança de identidade: não.** Se o autor preferir o contrário (Leve volta a 1 de Espaço e a dominância fica registrada como achado conhecido), é uma reversão de uma linha de tabela mais os dois espelhos de oráculo.

---

## 3. Achados confirmados e aplicados

| # | Local | Frase (verbatim) | Def. | Sev. | O que foi feito |
|---|---|---|---|---|---|
| **A1** | `24-equipamentos.md` §24.2 | `\| **Recarga** \| Precisa de uma **Ação Complementar** para recarregar depois de um número de disparos definido na criação \|` | A | **Alta** | **Linha removida.** Abaixo da tabela, parágrafo novo: recarregar é sabor livre, de graça, e **não consome** a propriedade especial. Quadro `> **O que mudou da v1.1:**` acrescentado. A linha "Nenhuma propriedade aumenta os **dados base** da categoria." ficou intacta |
| **A1-p** | §24.3, itens comuns | `\| Munição ou célula de reserva \| 0,5 \| 20 Cr \| Recarrega uma arma com a propriedade **Recarga** \|` | A | Alta | Item mantido, **mesmo Espaço (0,5)** e **mesmo preço (20 Cr)**. Coluna "Para quê" reescrita. Texto novo, exato: `Reposição de projétil ou de célula de energia` |
| **B2** | `18-combate.md` §18.7 | `Exemplos: recarga, arremessável, duas mãos, alcance um passo acima do normal da categoria, ou **+1 de Redução de Tenacidade**.` | A+B | **Alta** | Lista trocada pelos **quatro nomes reais** de 24.2. Saíram "recarga" (A1) e "duas mãos", que é puro custo: não há escudo, ataque com a mão secundária nem regra de empunhadura no livro |
| **B1** | §24.7 passo 3 e resumo do cap. 24 | `3. Escolha **uma** propriedade especial.` | B | **Alta** | `Escolha **até uma** propriedade especial — ou nenhuma.` e `mais **até uma**` no resumo. Contradizia 18.7, a própria 24.2 e a tabela de checagem do Mestre em 24.7 |
| **B7** | `27-guia-do-mestre.md` §27.9 | `\| **Arma** \| Categoria da tabela + um Elemento + **uma** propriedade especial (capítulo 24) \|` | B | Média | **Achado novo da varredura**, mesma família de B1. Virou `+ **até uma** propriedade especial` |
| **A2** | `21-condicoes.md` §21.2/§21.5 e `20-...-quebra.md` §20.1 | §20.5 Raio `1d6 + Eficiência` × Fogo `2d6 + (2 × Eficiência)`; Choque 2 turnos × Queimadura 2 turnos; `**Raio** \| ... \| **Choque** — dano contínuo confiável` | A | **Alta** | **Aprovado pelo autor.** Choque → **3 turnos**. §20.1 passou a ter **três grupos** de Elemento, com Raio e Vento no grupo do "dano que fica", e um quadro explicando o trade. Nenhum número de 20.5 mudou |
| **A3** | `05-racas.md`, Avginiano × Xianzhouíta | `**+2 em Discernimento**` + Vantagem em 3 dos 6 TR, contra `+2 em Vigor ou Sincronia` + Vantagem em **qualquer** TR + imunidade à Execução | A | **Alta** | **Aprovado pelo autor.** Bônus virou `+2 em Discernimento ou Presença`, nos dois lugares do capítulo. Quadro novo explicando. Mente de Ferro intacta, nenhum traço inventado |
| **A5** | `21-condicoes.md` §21.2/§21.5, **Cisalhamento de Vento** | `**Dano Contínuo de `1d6` por acúmulo**, de Vento, até **5 acúmulos**.` | A | Média | **Achado novo.** O Vento era dominado pelo Raio: mesmo Dano de Quebra, mesma duração, e o tique do Choque somava **+Eficiência** que o Cisalhamento não soma. O diferencial anunciado em 20.1 ("acumula até 5 vezes") **não tinha porta de entrada**: o livro nunca dizia como se acumula. Corrigido por **redação** (regra (iii)): **1 acúmulo por ataque seu de Vento** enquanto a condição durar, sem precisar de Quebra nova — o mesmo idioma que o Embaraço já usa. **Nenhum número mudou** |
| **A6** | `24-equipamentos.md` §24.2, categoria **Leve** | `\| **Leve** \| 1d8 \| Pessoal \| Agilidade \| 1 \| 1 \| 100 Cr \|` | A | Média | **Achado novo.** Dominada pela Média. Espaço **1 → 0,5** (ver seção 2, nº 3) |
| **A7** | `24-equipamentos.md` §24.2, **Arremessável** | `Pode ser lançada a um alcance acima do normal da categoria; depois disso, você está sem ela` | A | Média | **Achado novo.** Dominada por Alcance estendido. Alcance **um → dois passos**, teto Extrema (ver seção 2, nº 4) |
| **B3** | `17-ultimate-e-energia.md` §17.4 passo 2 e §17.3 | `**Escolha o Tipo:** dano, cura, buff, debuff ou controle.` / `**Efeitos de buff, debuff e controle**` | B | Média | "Controle" **não é Tipo**: a lista é fechada em 16.1 e 16.8, e é a linha de 16.1 que a ficha lê para validar o campo. O passo 2 passou a usar os Tipos de 16.1 (sem Passiva, que não cabe numa ação declarada) e diz que controle é o **"aplica 1 condição"** de 16.5. O bullet de 17.3 foi ajustado do mesmo jeito |
| **B8** | `16-habilidades.md` §16.5 | As duas tabelas não diziam se a linha de um Nível incluía as de baixo | B | Média | **Achado novo.** Na leitura restritiva, uma Habilidade de Nível 5 não poderia aplicar condição (linha do Nível 3) e seria **pior que uma de Nível 4** para quem joga controle. Escrito que as duas tabelas são **cumulativas**, como o alcance de 16.3: a linha do seu Nível é teto, não lista fechada |
| **A4** | `25-cones-de-luz-e-reliquias.md` §25.2 | Nível 4 `+2 **e** +25 PV` · Nível 5 `+3 **ou** +50 PV` | A | Média | Progressão não monotônica: trocar um Nível 4 por um Nível 5 pode **piorar** a ficha. Nota nova, **só texto, sem mexer em número**: a troca é opcional (25.1 já dizia "pode trocar") e um Cone de Nível menor, sobretudo de "e" e com Sobreposição, pode valer mais. O que o Nível alto compra é **Efeito Condicional** |
| **B4** | `26-progressao-e-ressonancias.md` §26.7 | cabeçalho `\| Ressonância \| Nível \| Escolha uma opção \|` | B | Baixa | Cabeçalho virou **"O que ela dá"**, com a observação de que só **I** e **IV** têm duas opções |
| **B5** | §26.7, Ressonância IV | `**ou** sua Bênção **Avatar** afeta **um alvo adicional**` | A | Baixa | Opção morta para quem não tem o Avatar, numa escolha permanente. Passou a valer **"se você tiver a Bênção Avatar"**, e as regras comuns dizem que quem não a tem tem uma opção só |
| **B6** | `16-habilidades.md` §16.8 → §16.7 | `\| Condição de recarga \| Opcional \| Só se você quiser trocar custo por frequência \| — \|` | B | Média | A linha do checklist **não foi removida** (tem contrapartida declarada); ela era **órfã**. Régua escrita em 16.7 com o texto aprovado pelo autor, e a linha do checklist agora aponta para lá |

---

## 4. Auditoria de dominância — todas as listas de escolha do jogador

Cobertura completa pedida na autoridade ampliada. "Sem defeito" significa: nenhuma opção da lista é igual-ou-pior que outra em todo eixo, e nenhuma só cobra.

| Lista | Itens conferidos | Veredito |
|---|---|---|
| **Raças** (cap. 05) | 7 | **Um defeito, corrigido** (A3). Reconferidos todos os pares depois da correção: Vidyadhara e Intellitron têm bônus fixo mas traço que o Xianzhouíta não tem (Reencarnação Ancestral; Vantagem em Tecnologia/Mecânica e duas Fraquezas por sucesso), então não são dominados; Humano paga o bônus livre com o Esforço exclusivo; Haloviano e Vulpes têm traço ativo próprio |
| **Caminhos** (cap. 06) | 9 | **Sem defeito.** As cinco colunas (Atributo de Habilidade, 3 Perícias, índice N, Bônus de VEL, 12 Bênçãos) trocam entre si: a Caça tem o maior VEL e o menor N, a Preservação o inverso. Nenhum é igual-ou-pior em tudo |
| **Bênçãos** (caps. 07 a 15) | **108** | **Sem defeito. Nenhuma mudou.** Nenhuma é só custo e nenhuma é dominada por outra do mesmo Caminho. Os custos em PV da Destruição (§7.2), o 1 PH do *Implante de Fraqueza* e o -1 dado de *Ritmo Acelerado* são contrapartida declarada |
| **Escolhas internas de Caminho** | `07:74` Elemento da Resistência · `09:73` tipo de rolagem · `11:88` três Memórias · `11:171` duas formas do Avatar | **Sem defeito.** A mais apertada é *Fragmentos do Eu Perdido*: a Memória da Sabedoria entrega **dado base** (que crita e reduz Tenacidade) mais Eficácia em Perícia, contra `+1d8` nos dois lados da Fúria — mais fraca em dano bruto, **diferente** em natureza |
| **Memoespírito** (cap. 11) | 4 Funções · 6 Bônus menores (escolhe 3) · 4 Técnicas Principais · 4 Técnicas Auxiliares · 3 Evoluções | **Sem defeito.** Cada lista troca entre eixos (dano, PV/RD, Velocidade, acerto, controle, flexibilidade). As três Evoluções são adquiridas todas, nos níveis 8, 14 e 20 — não é escolha excludente |
| **Habilidades — as 14 linhas de 16.5** | Buff/Debuff 1 a 7 · Passivas 1 a 7 | **Nenhum número mudou.** Nenhum Nível é dominado pelo de baixo: cada degrau cresce em valor, duração, alvos ou efeito maior. Os que trocam de natureza — Passiva 5 (gatilho forte 1×/combate) × Passiva 4 (+2 fixo e um gatilho de dado) — são incomparáveis. O único defeito era a **ambiguidade** de cumulatividade (B8), corrigida em texto |
| **Habilidades — campos do checklist** (16.8) | 11 campos | **Um defeito, corrigido** (B6, a condição de recarga órfã) |
| **Ultimate** (cap. 17) | Nível equivalente por faixa | **Sem defeito** de dominância: não é lista de escolha, é tabela por faixa. O defeito era de **Tipo inexistente** (B3) |
| **Elementos** (caps. 20 e 21) | 7 | **Dois defeitos, corrigidos** (A2 Raio, A5 Vento). Reconferidos os três grupos depois: Físico × Fogo são incomparáveis (Sangramento escala com o PV máximo do alvo até `3 × Eficiência`, Queimadura é dado fixo maior); Quântico × Imaginário também (o Embaraço chega a `5d6` com acúmulos, acima do `1d6 + Eficiência` do Aprisionamento, e paga com 1 casa de Atraso em vez de 2); Gelo compra turno inteiro com o menor Dano de Quebra. **Nenhum número de 20.5 foi tocado** |
| **Categorias de arma** (18.5 e 24.2) | 6 | **Um defeito, corrigido** (A6 Leve). Disparo curto × Disparo longo × Energia trocam alcance por Espaço e por atributo; Pesada paga as duas mãos pelo 1d12 |
| **Propriedades de arma** (24.2) | 5 → 4 | **Dois defeitos, corrigidos** (A1 Recarga removida, A7 Arremessável). As quatro restantes pagam em eixos diferentes: alcance permanente, alcance de arremesso, Redução de Tenacidade, Espaço e busca |
| **Armaduras e Vestimentas** (24.1) | 3 | **Sem defeito.** Leve troca 2 de Defesa por +1 VEL e menos Espaço; Pesada compra +6 e 2 RD com -2 de VEL, -2 em Reflexos/Perícias de Agilidade e **sem Esquiva** |
| **Poções** (24.3) | 3 | **Sem defeito.** A Grande é pior por Crédito e por Espaço e melhor por **ação**: 50 de cura numa Ação Complementar. Economia de ação é contrapartida real |
| **Itens comuns** (24.3) | 11 | **Sem defeito.** Cada um resolve uma ficção diferente, e nenhum dá bônus numérico de combate (a seção já declara isso) |
| **Cones de Luz** (25.2) | 5 Níveis · 6 opções de Bônus Maior · Efeito Condicional · Sobreposição | **Um defeito, corrigido em texto** (A4). As 6 opções de Bônus Maior são eixos distintos; nenhuma domina |
| **Relíquias** (25.3) | 6 slots · 4 opções de Conjunto de 2 peças · Conjunto de 4 | **Sem defeito.** Slot é estatística fixa por tier, não escolha; as 4 opções de Conjunto de 2 peças são eixos distintos |
| **Ressonâncias** (26.7) | 4, com 2 opções em I e IV | **Dois defeitos, corrigidos** (B4 cabeçalho, B5 opção morta) |
| **Atributos, Perícias e Eficácia** (03, 04, 26.4) | 6 Atributos · 18 Perícias · slots de Eficácia · 2 métodos de criação | **Sem defeito.** Os dois métodos nascem empatados (28 pontos = preço exato do array), a tabela de Bônus não tem degrau morto (o 13 vale +1), nenhuma Perícia é coberta por outra e a Sintonia tem atributo fixo na criação de propósito |
| **Fila de Ação, Testes de Resistência, dano/cura/morte** (19, 22, 23) | Avançar/Atrasar, os 6 TR, escolhas a 0 PV | **Sem defeito.** A §22.4 já publica a conta honesta das duas vias de resolução, com o que cada uma perde |
| **Limites do Mestre** (27.9 e 27.10) | Todos os números | **Nenhum limite numérico divergiu do capítulo dono.** A única divergência era de obrigatoriedade (B7) |

---

## 5. Achados conhecidos e NÃO corrigidos

Nenhum destes entrou no livro. Ficam registrados com a recomendação, como a autoridade ampliada manda.

| Achado | Por que não foi aplicado | Recomendação |
|---|---|---|
| **O custo de "duas mãos" da propriedade Peso de impacto é fictício.** `Numa arma **Leve** ou **Média**, ela passa a exigir **as duas mãos**` — e empunhadura **não tem peso mecânico** neste sistema: não há escudo, ataque com a mão secundária nem regra de mão livre (grep de `duas mãos`, `uma mão`, `arma secundária` e `empunh` nos 34 `.md`) | **Não é defeito A:** nenhuma propriedade é dominada por Peso de impacto, porque as outras três pagam em eixos que ela não toca. O defeito é só o custo declarado não existir, e consertar isso exigiria **inventar regra de empunhadura** — mecânica nova, fora da guarda de mudança mínima | Deixar como está, ou tirar a frase das duas mãos numa versão futura, assumindo que Peso de impacto é a propriedade de combate e as outras três são de alcance e de inventário |
| **"Efeito menor" não é definido.** `16-habilidades.md` §16.5, Buff/Debuff Nível 2: "+1/-1 e um **efeito menor**". O livro define "efeito **maior**" na linha do Nível 5 (Avanço Total, Ação Extra, imunidade a 1 condição) e nunca define o menor | Lacuna de definição, não defeito A/B: a linha entrega valor de qualquer jeito, e o checklist de 16.8 manda o Mestre reduzir ao permitido pelo Nível. Definir a lista seria **mecânica nova** sem dominância para resolver | Numa revisão de texto futura, dar três exemplos de efeito menor como a linha do Nível 5 faz com o maior |
| **A arma de Energia começa em 2 dados e isso atravessa a progressão inteira** (24.2, 18.5, 26.2) | **Não é defeito:** é trade declarado — 2 de Espaço, duas mãos, 500 Cr e atributo **Sincronia**, que não é o atributo de ataque de nenhum Caminho além da Erudição e da Inexistência. E qualquer mexida aqui é **economia central** (dados base), proibida pela guarda | Nenhuma. É o desenho do autor, e foi a arma que o próprio autor montou na pergunta que abriu esta versão |

---

## 6. O que NÃO foi alterado, de propósito

- **"Recarregar" como exemplo de Ação Complementar** continua em `18-combate.md:16`, `14-caminho-caca.md:84` e `30-glossario.md:17`. Com a propriedade fora, essas três linhas são exatamente o que o parágrafo novo de 24.2 autoriza: sabor, de graça. **Nenhuma foi tocada.**
- **A recarga em Ciclos** das ações especiais de inimigo (`28-bestiario.md`) e a **recarga de efeitos "1 vez por descanso"** (`23-dano-cura-e-morte.md:131-132`) são outras coisas, estão corretas e ficaram intactas.
- **Os dois changelogs anteriores** (`00-changelog-v01-para-v10.md` e `00-changelog-v10-para-v11.md`) são registro histórico e não foram abertos para edição.
- **O parágrafo da v1.1 na capa** continua, como o da v1.0 continuou. A capa agora diz **Versão 1.2** em dois lugares (linha 9 e a ficha técnica) e tem o parágrafo novo apontando o changelog da v1.2.

---

## 7. Arquivos `.md` alterados no FEAT-001

| Arquivo | O que mudou |
|---|---|
| `livro-v1.0/00-capa-e-creditos.md` | `**Versão 1.1**` → `**Versão 1.2**`; ficha técnica `1.1` → `1.2`; parágrafo novo da v1.2 depois do da v1.1, que continua |
| `livro-v1.0/00-changelog-v11-para-v12.md` | **Arquivo novo**, 16 correções (E1 a E16) no formato do changelog anterior. Entra sozinho no PDF e no DOCX pela ordenação de prefixo |
| `livro-v1.0/05-racas.md` | Avginiano: bônus vira escolha, nos dois lugares; quadro `> **O que mudou da v1.1:**` |
| `livro-v1.0/16-habilidades.md` | 16.5: quadro de cumulatividade das duas tabelas (B8). 16.7: régua da condição de recarga (B6). 16.8: linha do checklist aponta para 16.7 |
| `livro-v1.0/17-ultimate-e-energia.md` | 17.4 passo 2 e o bullet de 17.3: "controle" deixa de ser Tipo (B3) |
| `livro-v1.0/18-combate.md` | 18.7: lista de exemplos trocada pelos quatro nomes reais de 24.2 (B2) |
| `livro-v1.0/20-elementos-tenacidade-e-quebra.md` | 20.1: linha do Raio, os três grupos de Elemento e quadro novo (A2, A5) |
| `livro-v1.0/21-condicoes.md` | 21.2: Choque 3 turnos, Cisalhamento com a regra de acúmulo, quadro novo. 21.5: as duas linhas correspondentes (A2, A5) |
| `livro-v1.0/24-equipamentos.md` | 24.2: Recarga removida, Arremessável com dois passos, Leve com 0,5 de Espaço, parágrafo do sabor, quadro novo. 24.3: "Para quê" da munição. 24.7 passo 3 e resumo: "até uma" (A1, A6, A7, B1) |
| `livro-v1.0/25-cones-de-luz-e-reliquias.md` | 25.2: nota de que trocar o Cone é opcional e que Nível maior não é automaticamente melhor (A4) |
| `livro-v1.0/26-progressao-e-ressonancias.md` | 26.7: cabeçalho da tabela e a condição da segunda opção da Ressonância IV (B4, B5) |
| `livro-v1.0/27-guia-do-mestre.md` | 27.9: linha "Arma" da tabela de limites, "até uma" (B7) |

**Nenhum outro `.md` foi tocado.** `28-bestiario.md`, `29-apendices-e-fichas.md`, `30-glossario.md`, os dois changelogs antigos, `01` a `04`, `06` a `15`, `19`, `22` e `23` estão byte a byte como estavam.

---

## 8. Propagação que os próximos passos precisam fazer

Levantada e conferida no FEAT-001, já escrita nos arquivos de FEAT.

**Propaga sozinho, não editar:** `ficha_dados.racas()` lê a tabela de consulta rápida do cap. 05 e deriva `opcao1`/`opcao2` (conferido: Avginiano já sai com Discernimento e Presença); `ficha_dados.armas()` lê o Espaço de 24.2 e `num()` devolve `0.5` para a célula `0,5` (conferido); `ficha_dados.propriedades()` lê as 4 propriedades e o texto novo de Arremessável (conferido: a lista já sai sem Recarga); `ficha_dados.itens()` lê o "Para quê" novo da munição (conferido); `ficha_dados.condicoes()` lê a duração em 21.5, então o Choque com 3 turnos chega à aba Dados sozinho.

**Hardcoded, precisa de mão (está no FEAT-002):**

| Arquivo | Linha | O que fazer |
|---|---|---|
| `build/oraculo_ficha.py` | 59 | `RACAS["Avginiano"] = ("Discernimento",)` → `("Discernimento", "Presença")` |
| `build/oraculo_ficha.py` | 99 | `ARMAS["Leve"]` → último campo (Espaço) `1` → `0.5` |
| `build/oraculo_mestre_hist.py` | 59 | texto do item → `Reposição de projétil ou de célula de energia` (idêntico ao livro) |
| `build/oraculo_mestre_hist.py` | 63 | `ARMAS`, tupla da Leve → Espaço `1` → `0.5`, preço 100 intacto |
| `build/oraculo_mestre_cmb.py` | 330 | string do Choque: `2 turnos` → `3 turnos` |
| `build/mestre/aba_combate_inimigos.py` | 202 | a mesma frase, dentro da fórmula Excel: `2 turnos` → `3 turnos` |
| `build/testar_ficha.py` | 2288, 2504 | tirar `"Recarga"` do caso de teste e de `_OR_PROPRIEDADES` |
| `build/gerar_ficha.py` | 1320-1321, 2257-2258 | `amostra`/`invalido` com `"Recarga"` → propriedades existentes |

**Não mexer:** `build/oraculo_mestre_livro.py` `CONDICOES` não tem campo de duração — a tupla é (dados, faces, por acúmulo, soma Eficiência, % PV, teto ×Ef, atrasa, teto de acúmulos, DC) —, então o Choque lá **não muda**. `oraculo_ficha.py:144` (Vantagem da Mente de Ferro) e `:147` (`VANTAGEM_MORRENDO`) também não: o traço não mudou. Todo `recarga` de `mestre_dados.py`, `oraculo_mestre_abas.py` e `oraculo_mestre_livro.py` é a recarga em Ciclos do capítulo 28.

---

## 9. Intocáveis — confirmação

- **`Explorando Galáxias RPG - Players\`** — **nada foi criado, modificado ou apagado**, e nenhum arquivo de lá foi aberto, lido ou usado como fonte. Registro honesto de uma ressalva: uma das buscas de texto desta auditoria (o termo `Avginiano`) rodou sobre o workspace inteiro, sem filtro de pasta, e pode ter varrido essa pasta no índice de busca. Nenhum resultado de lá foi consultado ou aproveitado, e nenhuma escrita aconteceu. Todas as outras buscas foram filtradas para `livro-v1.0/`, `build/` ou `scripts/`.
- **`versões antigas\`** — nada foi criado, modificado ou apagado, e nada de lá foi aberto.
- Os entregáveis **V1.1** (os dois da raiz, o `.gsheet`, o `.xlsx` da ficha e o `.xlsx` da Planilha do Mestre) continuam no disco, intactos. Os V1.2 sairão **ao lado**, no FEAT-003.
- A pasta `livro-v1.0\` **não foi renomeada** (nome legado; `testar_ficha.py:76` documenta).
- Nenhum comando git foi executado: o projeto não é um repositório git.

---

## 10. Verificação do FEAT-001

| Comando | Resultado |
|---|---|
| `powershell -File "scripts\checar-tabelas.ps1"` | **0** — 200 médias de dados conferidas, monotonicidade do Bônus de Atributo, os 20 níveis na tabela mestra, Níveis equivalentes da Ultimate dentro de 1 a 7 |
| `powershell -File "scripts\checar-nomenclatura.ps1"` | **0** — nenhuma das 25 strings proibidas nos 28 capítulos de regra |
| `powershell -File "scripts\checar-completude.ps1"` | **0** — 108 Bênçãos nos 9 Caminhos, 32 fichas de bestiário, nenhuma pendência de rascunho. **O changelog novo não quebrou a checagem de capítulos** |
| Extra, read-only: `ficha_dados.propriedades()`, `armas()`, `itens()`, `racas()` | As quatro tabelas editadas continuam parseáveis: 4 propriedades sem Recarga, Leve com `espaco: 0.5`, munição com o texto novo, Avginiano com `opcao1: Discernimento` e `opcao2: Presença` |
| `--suite protegidos` | **Não rodada, de propósito.** Ela falha por projeto quando o livro muda; a linha de base só é refeita no FEAT-003 |

---

## 11. Achados do autor, fora da auditoria de dominância (E17, E18 e E19)

Estes não vieram da varredura. Vieram de leitura direta do livro pelo autor, que montou uma arma de
**Energia** e foi conferir o Memoespírito. São de **outra classe de defeito**: não é opção-armadilha nem
contradição de obrigatoriedade, é **erro de consistência interna** — uma regra local que **repete** um
número que mora na tabela mestra, em vez de referenciá-la, e no caminho perde a exceção. Vale o registro
da classe: ela reaparece em qualquer ponto onde o livro reescreve um número de outro capítulo.

### 11.1 Os dois defeitos do parágrafo de 11.4

| # | Classe | Frase antiga (verbatim) | O que ficou | Impacto |
|---|---|---|---|---|
| **E17** | Numérico | "é a contagem de dados da sua arma pela tabela mestra (capítulo 26): **1** dado nos níveis 1-4, **2** nos 5-8, **3** nos 9-12, **4** nos 13-16 e **5** nos 17-20" | As **duas** escadas: `1 / 2 / 3 / 4 / 5` e, para arma de **Energia**, `2 / 3 / 4 / 5 / 6`, "que começa em dois dados e carrega esse dado a mais pela progressão inteira (capítulos 18 e 24)" | **Erro de dano.** 18.5, 24.2 e a nota da coluna em 26.2 todas dizem que a Energia começa em 2 e chega a 6. O Memoespírito de quem usa Energia rolava **um dado a menos** em toda a campanha: **2d6 no nível 1** e **6d6 no 17**, não 1d6 e 5d6 |
| **E18** | Redação | "O dado **dele** é sempre **d6**, independente da sua arma" | "**A sua arma empresta ao Memoespírito quantos dados ele rola, nunca qual dado.** São duas coisas separadas: a **quantidade** vem de você, pela tabela acima; o **tipo** é do **Memoespírito**, e é sempre **d6**, mesmo que a sua arma role d8, d10 ou d12" | O antecedente mais próximo de "dele" era **"sua arma"**, e o leitor amarrava o pronome errado: "minha arma é 2d8, como o dado dela é d6?". Foi o que aconteceu com o autor |

Dois acréscimos no mesmo bloco, pela convenção do livro: o exemplo de nível 17 passou a **declarar a
categoria da arma** ("com uma arma **Média** (5 dados de Ataque Básico nesta faixa)") — sem isso, o
`5d6 + 5` dele continuava ambíguo — e ganhou uma linha com o caso de Energia (`6d6 + 5` ≈ 26). O quadro
`> **O que mudou da v1.1:**` da seção registra os dois defeitos.

### 11.2 A varredura por reincidência, e tudo que ela encontrou

**(i) A escada de dados restada sem a exceção da Energia.** Procurei em `livro-v1.0\*.md` por
`partindo de 1`, `se for de Energia`, `dado a mais sobrevive`, `começa com 2`, `Dados de Ataque Básico`,
`dado nos níveis`, `dados nos níveis`, `dados por faixa`, `+1 dado` e pelas cinco faixas
(`1-4`, `5-8`, `9-12`, `13-16`, `17-20`). Resultado:

| Local | Estado |
|---|---|
| `18-combate.md` §18.5, frase acima da tabela de dados por faixa | **Correto.** "partindo de 1 — ou de **2**, se for de Energia, e esse dado a mais sobrevive à progressão inteira", e a tabela tem a linha própria da Energia (`2d8 · 9` → `6d8 · 27`) |
| `24-equipamentos.md` §24.2, quadro abaixo da tabela de armas | **Correto.** Repete a exceção com as mesmas palavras |
| `26-progressao-e-ressonancias.md` §26.2, nota da coluna "Dados de Ataque Básico" (a **fonte canônica**) | **Correto.** "partindo de 1. Uma arma de **Energia** começa em 2 e chega a **6** no nível 17 (capítulos 18 e 24)". A frase que o documento de design pedia **está** lá — o defeito não chegou à fonte |
| `11-caminho-recordacao.md` §11.4 | **ERRADO** — é o E17, corrigido |
| `29-apendices-e-fichas.md`, linha da ficha em branco do Memoespírito | **Correto.** "dados de Ataque Básico do dono, em d6" — referencia, não repete número |
| Todas as outras ocorrências de `+1 dado` (Caminhos, condições, Cones, Conjuntos, bestiário, glossário) | **Outro assunto.** São dados **adicionais** dentro do teto de 26, não a contagem base da arma. Nenhuma repete a escada |

**Um só caso. A fonte canônica de 26.2 está intacta**, e as outras duas reafirmações (18.5 e 24.2) também.

**(ii) Pronome sem antecedente em regra.** Procurei `\bdele\b` e `\bdela\b` nos capítulos em que **dois
sujeitos** convivem: 11 e 13 (dono e criatura), 28 (personagem e inimigo), 21 (quem marca e quem é
marcado) e 23 (quem executa e quem é executado) — 52 ocorrências no 11, 56 no 28, 6 no 21, 6 no 23 e 2 no
13, lidas uma por uma. O critério foi o do autor: **só** onde há dois sujeitos possíveis na mesma frase
**e** a regra muda de sentido conforme a leitura. Três casos passaram o critério, todos no **E19**:

| Local | Antes | Depois | Por que passou o critério |
|---|---|---|---|
| `11-caminho-recordacao.md` §11.5, **Proteção da Memória** | "**PV temporários** a um aliado, ou **+1 RD** até o fim do próximo turno **dele**" | "…até o fim do próximo turno **daquele aliado**" | "Aliado" e "Memoespírito" na mesma frase, e a duração muda de dono conforme a leitura. O próprio capítulo já escreve a forma explícita duas vezes (Bênção nº 8 e Função **Guardião**: "até o fim do próximo turno **daquele aliado**") |
| `11-caminho-recordacao.md` §11.5, **Presença Assombrosa** | "aplica **Lentidão** até o fim do próximo turno **dele**" | "…até o fim do próximo turno **daquele inimigo**" | Mesma tabela, mesmo padrão, com "inimigo" e "Memoespírito" disponíveis |
| `28-bestiario.md`, nota da Resistência a Quântico do **Autômato de Guerra** | "este Elite tira 2 dados do ataque **dele**" | "este Elite tira 2 dados **do ataque desse personagem** — a Resistência penaliza quem ataca, não quem defende (20.2)" | O sujeito mais próximo era "este Elite", e a leitura errada **inverte a regra**: parecia que o Elite tirava dados do próprio ataque. 20.2 é clara — Resistência é **-2 dados** para quem ataca |

**Casos que NÃO passaram o critério, e por quê** (ficaram como estão, de propósito):

- **Capítulo 21, verbetes de condição** ("até o fim do próximo turno dele", Quebrado e Lentidão): a frase
  tem **um** sujeito, o alvo, nomeado na linha. É o idioma padrão do livro para duração, usado em 20.5,
  21.2 e no glossário. Trocar aqui seria mexer em dezenas de linhas sem ganho.
- **Capítulo 23, Execução**: o livro já nomeia tudo — "o turno **do executor**", "o Ataque Básico **do
  executor** contra o interventor". Nada ambíguo.
- **Capítulo 21, Marcado e Controlado**: escritos com sujeito nomeado ("**quem aplicou** a marca", "o
  **alvo marcado**", "**quem aplicou** decide as ações do alvo").
- **Capítulo 28, o resto das 56 ocorrências**: "dele"/"dela" é o inimigo da ficha, e o capítulo inteiro
  tem o inimigo como sujeito. Nos casos em que um personagem aparece na mesma frase, o livro ou nomeia
  ("aquele personagem está Silenciado"), ou o gênero resolve (a inimiga "ela" × o personagem "ele").
- **Capítulo 11, as outras 49 ocorrências**: "dele" é o Memoespírito, e é o sujeito do capítulo. Só o
  parágrafo de 11.4 tinha "sua arma" competindo pelo pronome.
- **Capítulo 13, as 2 ocorrências**: "um aliado ganha +2 na próxima rolagem dele" — o bônus vai para o
  aliado, então a rolagem é dele; a leitura alternativa não faz sentido mecânico.

### 11.3 Onde o mesmo defeito estava no código

A ficha e a Planilha do Mestre foram conferidas contra o E17. Resultado:

| Ponto | Estado |
|---|---|
| `build\gerar_ficha.py`, Ataque Básico do **próprio personagem** (`equipamento.ab.*`) | **Já estava certo.** A fórmula é `nucleo.dados_ab + VLOOKUP(categoria, armas, 3) - 1`, e a coluna 3 da tabela de armas de 24.2 vale **2** na Energia e 1 nas outras. O +1 da Energia **não** dependia de o jogador digitar nada |
| `build\oraculo_ficha.py`, Ataque Básico do personagem | **Já estava certo.** `n = dados_ab(L) + extra`, com `extra = 1` em `ARMAS["Energia"]` |
| `build\gerar_ficha.py`, **dados de dano do Memoespírito** (`memo.n`) | **ERRADO, corrigido.** Era `nucleo.dados_ab + IF(Forma Completa,1,0)` — a escada crua, sem a arma. Passou a somar o mesmo termo do Ataque Básico |
| `build\oraculo_ficha.py`, **`memo.n`** | **ERRADO, corrigido.** Era `dados_ab(L) + (1 se Forma Completa)`. Passou a `dados_ab(L) + (cat_arma[1] se houver arma) + (1 se Forma Completa)` |
| `build\mestre_dados.py`, `build\mestre\*`, `build\oraculo_mestre*.py` | **Nada a corrigir.** A Planilha do Mestre não modela Memoespírito nem a escada de dados do jogador: grep de `Memoesp`, `dados_ab` e `Dados de Ataque Básico` em todo `build\mestre\` e nos oráculos da Mestre não devolve nada |

**Cobertura de teste nova** (a antiga não cobria a categoria, como o autor suspeitou): o caso **(e)** da
suíte `ouro` — o Memoespírito de nível 17 de 11.4 — usava a arma **Pesada** padrão do fixture e por isso
passava com 5 dados mesmo com o bug. Entrou um caso **(e2)**, nos **dois** lados da suíte (oráculo e
planilha calculada): a mesma ficha com arma de **Energia** dá `6d6+5`, média **26** e **33** contra
Fraqueza no nível 17; no nível 1 dá `2d6+5`; e a mesma ficha com arma **Média** no nível 1 dá `1d6+5`,
que é o guarda contra a correção vazar para as outras cinco categorias.