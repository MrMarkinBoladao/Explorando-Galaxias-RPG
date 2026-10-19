# Site: ficha online e livro de consulta

Uma página só, sem instalação, com quatro abas:

- **Jogar** — a ficha na mesa: os **seis Atributos** no topo (valor final e Bônus, com o da **arma** em laranja e o de **Habilidade** em violeta, abaixo), PV com dano e cura (já desconta RD e PV temporários), o **painel de Energia** (abaixo), PH do grupo, ataques e Testes prontos para rolar (clique no valor — **com Vantagem, já rola os dois d20**, e todo Teste de Ataque tem o botão **Vantagem** do lado, abaixo), a **rolagem livre**, Bênçãos com usos, condições, Morrendo, Memoespírito (**alvo único ou em área**, abaixo), inventário e o **Cone de Luz com a arte e a história dele** (abaixo).
- **Editar ficha** — os doze passos do capítulo 03, mais progressão, equipamento e Memoespírito. Tudo é recalculado na hora, e o que fere uma regra aparece em vermelho na seção.
- **Regras** — o livro inteiro (v1.2) com pesquisa instantânea, sem acento e sem maiúscula.
- **Área do Mestre** — a mesa do Mestre, sincronizada com as fichas (abaixo). Fica para todo mundo, inclusive para quem é jogador numa mesa online: é a mesa *daquele navegador*.

As fichas ficam salvas **no navegador** de cada jogador. Para backup ou para mandar ao Mestre: **Mais > Exportar** (gera um arquivo `.json`) e **Mais > Importar**. Com a **mesa online** ligada, as fichas do grupo, o PH, o combate e as rolagens aparecem ao vivo no aparelho de cada um (abaixo).

## O Cone de Luz: a arte, o efeito e a história

Toda ficha — de jogador ou de NPC — guarda o Cone de Luz inteiro: Nome, Nível, Bônus Maior,
Sobreposições e Efeito Condicional, mais a **arte** e a **descrição** dele (25.2). Os dois últimos
são só sabor: não entram em conta nenhuma, nem no motor de regras. Em **Editar ficha > 8 ·
Equipamento**, embaixo de *A arte e a história do Cone*:

- **Escolher uma imagem…** pega um arquivo do computador ou do celular. Ela é **encolhida** (até
  560 px no maior lado, em `.webp`) e guardada **dentro da própria ficha**: aparece sem internet,
  vai no `.json` exportado e no backup, e não depende de nenhum site de fora. O peso final aparece
  ao lado do botão.
- **Ou cole um link** no campo *Endereço da imagem*. Não gasta espaço no navegador, mas depende da
  internet. Se o link não carregar, a moldura diz isso em vez de deixar uma imagem quebrada.
- **Descrição** é texto livre, do tamanho que você quiser. Linha em branco separa parágrafo, e é
  assim que ela aparece na tela — serve para a cena inteira que o Cone carrega, com as falas.

Onde isso aparece — e é sempre a **mesma ficha**, lida na hora de desenhar, nunca uma cópia:

| Onde | O que mostra |
|---|---|
| **Jogar** | O cartão *Cone de Luz*: a arte grande, Nome e Nível, o Bônus Maior que já está somado nos números da ficha, o Efeito Condicional e a descrição embaixo |
| **Mestre > Grupo** e o painel de combate | A arte em miniatura no cartão de cada personagem e de cada NPC em cena, com o Efeito Condicional à vista e a descrição em *Ler a descrição* |
| **Mestre > NPCs** | A mesma miniatura no cartão de cada NPC do banco |
| **Mestre > Recompensas** | *Cones de Luz da mesa*: a galeria com o Cone de todo mundo, grupo e NPCs lado a lado, e o nome do Cone na conferência de marco |

> **Espaço no navegador.** O `localStorage` tem uns 5 MB para a mesa inteira, e cada arte guardada
> come um pedaço dele. Se o navegador recusar gravar, o site avisa e **mantém a arte anterior** —
> nada da ficha se perde. Nesse caso, use um link em vez do arquivo, ou tire a arte de alguma ficha.

**Inimigo não tem Cone de Luz.** Pela regra 25.2 quem equipa um Cone é personagem, e o inimigo sai
da tabela de âncoras de 28.3 — treze números e nada mais. Um NPC, que é ficha de personagem
inteira, tem.

### O banco de Cones

A ficha guarda **um** Cone, o equipado. O **banco** guarda a coleção da mesa — o que a pessoa usa
hoje, o que ela usava antes, o que o Mestre ainda não entregou. Ele aparece em dois lugares, e é o
mesmo banco nos dois:

- **Editar ficha > 8 · Equipamento**, no quadro *Banco de Cones de Luz*: escolher um Cone na lista
  e **Equipar**, ou **Guardar o Cone desta ficha no banco**. *Ver a coleção* abre a galeria com a
  arte de cada um, para equipar ou tirar do banco direto de lá.
- **Mestre > Recompensas**, no cartão *Banco de Cones de Luz*: **Entregar** um Cone a qualquer
  personagem ou NPC. A entrega **guarda no banco o Cone que a pessoa estava usando** antes de
  equipar o novo, então nenhum Cone com nome e história se perde numa troca. O botão
  *Ver os N Cones do banco* / *Recolher os N Cones* esconde e mostra a galeria: com o banco cheio
  ela toma a tela inteira, e aí ele já abre a aba recolhido (até 4 Cones ele abre aberto).

- **Equipar copia.** Daí em diante a ficha tem a cópia dela: mudar o Cone na ficha não mexe no
  banco, e tirar um Cone do banco não mexe em ficha nenhuma.
- **Dois Cones com o mesmo nome são o mesmo Cone.** Guardar de novo **atualiza** o que está lá, em
  vez de encher o banco de quase-duplicatas.
- **O banco tem chave própria no navegador** (`explorando-galaxias:cones`), vai no backup completo
  (*Mais > Exportar tudo*) e se exporta sozinho em **Exportar o banco**. É assim que os Cones saem
  do navegador do Mestre e entram no do jogador: a importação **soma** ao banco de quem recebe e
  nunca apaga nada.
- **Importar aceita vários arquivos** e também aceita um **arquivo de ficha ou de NPC** — dele sai
  o Cone equipado, que é como se pega um Cone bonito de uma coleção pronta.

Um Cone se **escreve na ficha** (é lá que estão o Bônus Maior, o Efeito Condicional, a arte e a
história, com todos os avisos de regra) e depois vai para o banco. O banco guarda e entrega.

## O Inventário: o que está ocupando o Espaço

Na aba **Jogar**, o cartão *Inventário* lista **tudo o que pesa**, uma linha por coisa, com o nome
e, encostado na direita, quanto ela ocupa — a coluna se lê de cima a baixo até o *Total ocupado*.
A conta é a de 24.4: `10 + 2 × bônus de Poder` de capacidade, mais 2 se o personagem tiver a Bênção
*Peso do Juramento*.

- **Arma e armadura entram na lista**, porque ocupam Espaço. Elas vêm em linha tracejada e **não se
  editam aqui**: trocar categoria ou propriedade é da aba *Editar ficha*. Uma arma **Dissimulada**
  aparece com a propriedade no rótulo, que é o motivo de ela ocupar 0,5 em vez do peso da categoria.
- **Cada item mostra a conta**: `quantidade × Espaço de cada`. Três poções de 1 ocupam 3; duas
  lanternas de 0,5 ocupam 1. O número da direita é esse produto, não o Espaço unitário.
- **O topo do cartão diz a folga**: *"ainda cabe 8"*, ou *"6 acima da capacidade"* em vermelho, com
  a etiqueta **Lentidão** (acima da capacidade) ou **não se move** (acima do dobro).
- **Créditos não ocupam Espaço**, nem Relíquias, nem o Cone de Luz.
- Os campos de **quantidade** e de **Espaço de cada** gravam quando você sai do campo ou aperta
  Enter; o nome do item grava a cada tecla.

## Os Atributos da arma e da Habilidade

A faixa de Atributos da aba Jogar destaca sozinha qual Atributo cada coisa usa: **laranja** com a
etiqueta **ARMA** para o do Ataque Básico, **violeta** com **HABILIDADE** para o das Habilidades, da
Ultimate e da DT. O que serve aos dois leva as duas cores. No cartão de Ações, cada ataque traz o
mesmo selo com o Bônus (`Agilidade +4`), e na Área do Mestre a faixa compacta tem uma linha que diz
qual é qual.

O destaque é o Atributo que o motor **soma de verdade**, e não um campo da ficha:

- **A arma segue a categoria** (18.5): Leve, Disparo curto e Disparo longo usam **Agilidade**,
  Pesada usa **Poder**, Energia usa **Sincronia**, e só a **Média** usa o Atributo escolhido em
  Editar ficha (Poder ou Agilidade).
- **A Habilidade usa o Atributo de Habilidade do Caminho.** Num Caminho de dois Atributos sem
  escolha, nada é destacado e as Ações avisam *sem Atributo de Habilidade* — aí o motor não soma
  Atributo nenhum, e a escolha se faz em Editar ficha > 3 · Caminho.

## O painel de Energia

Na aba **Jogar**, o cartão **Energia** junta tudo o que muda a Energia (a tabela fechada de 17.2),
para o jogador acompanhar o combate sem fazer conta: a barra com a marca da Ultimate, um botão por
fonte — **Atacou e acertou** (+20 e o PH do grupo), **Atacou e errou** (+20), **Usou** cada
Habilidade (+30, paga o PH), **Sofreu dano** (+10), **Derrotou um inimigo** (+10), **Quebrou a
Tenacidade** (+10), as ações do **Memoespírito** (+10 e +15, a metade), a **Corda de Ligação** e o
**Cone de Luz** de Nível 3+ quando a ficha tem — e o **Registro** das últimas mudanças, com
**Desfazer a última** para o clique errado.

- **Os limites valem sozinhos.** O que é *1 vez por Ciclo* (sofrer dano, Quebrar, o Cone) fica
  marcado como feito até o Ciclo virar; a Corda, até o combate acabar. Na mesa online o Ciclo é o do
  Mestre — avançou lá, libera aqui. Sem a mesa, o próprio cartão tem **Próximo Ciclo**, e **Novo
  combate** (em Recursos) libera tudo.
- **Sofrer dano já dá a Energia.** O botão *Sofrer dano* do cartão Vida soma os +10 junto (se ainda
  não vieram neste Ciclo), e o dano que o Mestre aplica em combate pela Área do Mestre também.
- **O 1 natural não dá Energia** (17.2): nesse caso, não clique. Acima de 100 se perde, e o registro
  guarda o que entrou de fato.

## O Memoespírito: alvo único ou em área

O ataque normal do Memoespírito é em **alvo único**. O que decide se a **Técnica Principal** dele é
em alvo único ou em área é o **acréscimo** dela (11.3, passo 5), escolhido em **Editar ficha > 10 ·
Memoespírito** (ou direto no cartão dele, na aba Jogar, enquanto não houver um):

| Acréscimo | Alvo | Dano |
|---|---|---|
| **Golpe Ancestral** | alvo único | **+1 dado** |
| **Explosão de Memória** | **até 3 alvos** | **metade dos dados** (mínimo 1) |
| **Marca do Passado** | alvo único | normal; ao acertar, Marcado ou Vulnerável |
| **Ataque Evolutivo** | alvo único | +1 por uso no combate, até +5 (o cartão conta) |

**O Memoespírito é chamado pelo nome** que está na ficha dele: *Ataque Básico de Gwen Fallon*,
*Gwen Fallon atacou (+10 Energia para você)*, *Técnica Principal de Gwen Fallon* (ou *Sick ·
Técnica Principal de Gwen Fallon*, quando a Técnica tem nome próprio), *PV de Gwen Fallon agora*,
*Invocar Gwen Fallon* — na aba Jogar, no painel e no registro de Energia, nas rolagens e na Área do
Mestre. Sem nome, a ficha diz *do Memoespírito*.

Com a Evolução **Forma Completa** a Técnica tem um **segundo acréscimo**; com Golpe Ancestral e
Explosão de Memória juntos, o cartão mostra **Alvo único (+1 dado)** e **Em área (até 3 alvos)**, e o
dano rolado muda com o botão aceso. Com **Memória Devastadora** os Fragmentos já entram no dano, e no
quinto aparece o ataque em área que ela dá (11.2).

## Rolagem com Vantagem

Teste com **V** do lado rola com Vantagem sozinho: o clique já tira os dois d20, o total sai com o
**maior** e o outro aparece **riscado**, para a mesa ver que ele saiu e não contou — ~~6~~ **15** +3
= 18. O aviso diz de onde a Vantagem veio, e o histórico de **Rolagens** guarda os dois dados. Um
20 em qualquer dos dois é 20 natural; o 1 natural só sai quando os dois são 1 (02.4). Vale também
no Teste de Morrendo e na Área do Mestre (a Surpresa e o Morrendo de cada um).

**Teste de Ataque com Vantagem da cena.** Todo Teste de Ataque — o Ataque Básico, as Habilidades,
a Ultimate, o Memoespírito e os inimigos na Área do Mestre — tem o botão **Vantagem** do lado do
valor: ele rola os dois d20 na hora, para quando a mesa diz que o ataque tem Vantagem.

## Rolagem livre

Qualquer pessoa rola qualquer coisa: o cartão **Rolagem livre** da aba Jogar, a caixa no topo do
painel **Rolagens** (no canto, em toda tela) e o cartão **Rolar** do Painel do Mestre. Aceita
`d20+5`, `2d6+3` e somas de dados (`1d8+1d6+2`), com **Vantagem** quando é um d20 só, e os dados
mais usados num clique. Na mesa online a rolagem livre do jogador aparece para todos com o nome dele.

**Os dados são sorteados pelo `crypto.getRandomValues` do navegador** (o gerador de senhas e chaves),
com descarte da sobra para que toda face tenha exatamente a mesma chance.

O que dá Vantagem sozinho é o que vale **sempre**, no Teste que o livro nomeia. Várias fontes no
mesmo Teste ainda são 2d20:

| Fonte | Testes |
|---|---|
| **Xianzhouíta** | os seis Testes de Resistência |
| **Avginiano** | Resistência Mental, Percepção Mental e Força de Vontade |
| **Vulpes** | Força de Vontade, Persuasão, Intimidação, Enganação e Liderança |
| **Intellitron** | Tecnologia e Mecânica |
| **Harmonia Interior** | Força de Vontade e Resistência Mental |
| **Laço Inquebrável** | Força de Vontade e Resistência Mental, enquanto o Memoespírito está em campo e os dois estão de pé |
| **Acrobata do Caos** | Reflexos |
| **Passos de Sombra** | Furtividade |
| **Peso do Juramento** | Potência Física e Resistência Física |

O Teste de Morrendo segue a lista de 23.5: Xianzhouíta, Vulpes e Avginiano.

A Vantagem que **depende da cena** — *contra veneno e doença*, *contra efeitos que apliquem
condições*, *o próximo Teste de Ataque*, a Sorte do tolo — não entra sozinha, porque a ficha não
sabe o que está acontecendo na mesa. E a Vantagem das Bênçãos é só do site (`vantagem_fontes`, em
`motor.js`): o oráculo e a planilha continuam com a Vantagem racial.

## Mesa online

Com a mesa online, cada um usa o site no próprio aparelho e tudo aparece ao vivo para quem deve ver:
o jogador toma 10 de dano na ficha dele e o PV muda na Área do Mestre; o Mestre cura pela Área do
Mestre e a ficha muda na tela do jogador. Sem importar nada. Quem não entra numa mesa usa o site como
sempre, inclusive sem internet.

| Quem | O que vê e mexe |
|---|---|
| **Mestre** | Todas as fichas da mesa (edita tudo, igual ao jogador), o PH, a Fila, as rolagens, quem está conectado e o convite. A Área do Mestre — inimigos, encontros, NPCs, notas — **continua só no navegador dele** e não vai para a nuvem |
| **Jogador** | A **própria ficha** (edita tudo), o **PH do grupo**, as **rolagens de todo mundo** e, em combate, a **Fila de Ação**: a ordem, quem está agindo, quem já agiu, o PV, a Energia e a Ultimate pronta dos aliados, as condições, e as barras de PV e Tenacidade dos inimigos (sem número; o Mestre pode desligar). A ficha dos outros jogadores e a mesa do Mestre, não: o servidor recusa. A **Área do Mestre continua na aba** — é a mesa do navegador *dele*, para o dia em que ele mestrar, e nada da campanha do Mestre aparece nela |

**Como usar.** O Mestre vai em **Área do Mestre > Painel > Mesa online**, entra com a conta Google,
cria a mesa e copia o convite. Cada jogador abre o link, entra com a conta Google, aceita e leva a
ficha dele para a mesa (um clique). Na mesa:

- **No combate, a vez de cada um aparece na tela dele**, com o botão **Terminei meu turno**: a Fila
  do Mestre marca *já agiu* sozinha (e desconta as condições, como o botão do Mestre). Ativar a
  Ultimate marca *Ultimate usada* no Ciclo (uma por Ciclo, 17.1). Atacar, acertar o Básico, gastar
  PH, tomar dano: os botões de sempre da ficha, e o Mestre vê na hora.
- **O PH é um número só da mesa**: quando dois gastam no mesmo instante, os dois gastos contam, e a
  Área do Mestre mostra e mexe nesse número — mesmo que o grupo do navegador dele tenha uma ficha
  fora da mesa (uma cópia importada antes) com um PH velho. Sem internet, o que mudar no PH fica
  guardado no aparelho e vai na volta, mesmo com a página fechada no meio.
- **A Área do Mestre de quem é jogador** é dele: ela não recebe nada da mesa do Mestre, e o que ele
  rola lá não vai para a mesa. Para mestrar online, o cartão *Mesa online* do Painel tem **Sair da
  mesa de jogador para mestrar** (um aparelho fica numa mesa por vez; as fichas não saem de lugar).
- **Rolagens**: todo mundo vê as de todo mundo, com o nome de quem rolou. O Mestre tem a caixa
  **Rolar escondido** para quando quiser segredo.
- **Sem internet**, a ficha continua funcionando e o que mudar fica pendente. Na volta, as duas
  versões se juntam campo a campo: vale o que cada lado mudou. Mesmo que a página tenha fechado.
- **Ninguém perde ficha.** Sair da mesa, ser tirado dela ou trocar de conta só para a sincronia: a
  cópia de cada aparelho fica. *Excluir* uma ficha que está na mesa tira ela da mesa também (o site
  avisa antes).
- **Outro aparelho** (o celular, além do computador): entre com a mesma conta, e as fichas da mesa
  chegam sozinhas.

> **Ficha importada antes da mesa.** Se o Mestre tinha importado a ficha de um jogador pelo `.json`,
> a do jogador chega pela mesa e substitui a cópia (quando é a mesma ficha) ou aparece ao lado dela
> (quando foi importada como cópia). Nesse segundo caso, tire a cópia velha do grupo.

### Ligar a mesa online (uma vez só)

O site continua no GitHub Pages; quem guarda e espalha os dados é o **Firebase Realtime Database**,
do Google. O plano grátis (Spark) não pede cartão e sobra para uma mesa: 100 conexões ao mesmo tempo,
1 GB guardado e 10 GB por mês de download.

1. Em <https://console.firebase.google.com>, **Criar um projeto** (o Google Analytics pode ficar
   desligado).
2. **Authentication > Começar > Método de login > Google**: ligar a chave **Ativar**, escolher o
   **e-mail de suporte do projeto** e clicar em **Salvar**. A linha do Google tem que aparecer como
   *Ativado* na lista; sem isso, *Entrar com Google* avisa que o login não está ativado.
3. **Authentication > Configurações > Domínios autorizados > Adicionar domínio**:
   `mrmarkinboladao.github.io`.
4. **Realtime Database > Criar banco de dados**, no **modo bloqueado**.
5. **Realtime Database > Regras**: apagar o que estiver lá, colar o conteúdo de
   [`firebase/database.rules.json`](../firebase/database.rules.json) e **Publicar**. São as regras
   que decidem quem lê o quê; sem elas, o banco recusa tudo.
6. **Configurações do projeto (engrenagem) > Seus apps > Web (`</>`)**: registrar o app (sem
   Firebase Hosting) e copiar o `firebaseConfig`. O console mostra junto um `npm install` e umas
   linhas de `import`; elas não são para este site, que carrega o Firebase sozinho — o que serve é
   só o objeto `firebaseConfig = { ... }`. Se ele vier sem `databaseURL`, o endereço está no topo
   da página do Realtime Database.
7. Colar os campos do `firebaseConfig` em [`site/js/mesa-online-config.js`](js/mesa-online-config.js)
   e rodar `python site/gerar_site.py`. (O `measurementId` é do Analytics e pode ficar de fora.)

**A configuração do passo 6 não é senha.** No Firebase ela é pública de propósito e vai no site de
quem usa o serviço; o que protege os dados são as regras do passo 5, que rodam no servidor do Google.
Se as regras mudarem no repositório, cole de novo (passo 5).

O SDK do Firebase (uns 330 KB) só carrega para quem está numa mesa, abre a tela *Mesa online* ou
o Painel da Área do Mestre. Para desligar a mesa, troque a configuração por `null`.

## A história do personagem

Em **Editar ficha > 1 · Personagem** há o campo **História do personagem**: é o texto comprido que
o jogador escreve fora da mesa, e ele aceita **Markdown**. Cole o `.md` do jeito que você escreveu
— `# títulos`, `**negrito**`, `*itálico*`, listas, `> citações`, tabelas, linhas e links — e ele
aparece formatado. A *Prévia formatada*, ali embaixo do campo, mostra exatamente como vai ficar, e
o campo conta as palavras.

- **Na aba Jogar** ela vem embaixo da ficha, na largura toda (texto longo em coluna estreita não se
  lê), **aberta e inteira**. Um clique no título recolhe.
- **Na Área do Mestre** ela aparece **fechada** em *Ler a história de X*, no cartão de cada
  personagem (Grupo e combate) e de cada NPC: são várias fichas na mesma tela, e um texto de mil
  palavras aberto afogaria o combate. Um clique abre.
- **Imprimir abre tudo.** O que estiver recolhido na tela — a história, a descrição do Cone, as
  ações de um inimigo — é aberto para o papel e volta a fechar depois.
- **NPC também tem.** É a mesma ficha, então o mesmo campo está lá.

> **Markdown colado é peneirado.** O livro vem do repositório e é renderizado direto; um `.md`
> colado de fora, não. O HTML gerado passa por um filtro que mantém a formatação (títulos, ênfase,
> listas, tabelas, links, imagens) e remove o que é comportamento: `<script>`, `<iframe>`,
> atributos `on...` e endereços `javascript:`. Link externo sai com `target="_blank"` e
> `rel="noopener"`.

## A Área do Mestre

Abre com um **aviso de spoiler** curto — é a página que mostra o bestiário e as recompensas, então
quem é jogador e não está mestrando é melhor não entrar. Um clique dispensa o aviso para sempre, e
o botão **Rever o aviso de spoiler**, no fim do Painel, traz ele de volta. Oito telas:

| Tela | O que tem |
|---|---|
| **Painel** | Campanha, faixa, PH do grupo, a tira do grupo com PV e Energia, o Ciclo em curso, a DT da faixa (27.2), rolador e checklist de abertura de sessão |
| **Grupo** | Tamanho do grupo com o PH resultante (16.2); por jogador: PV com dano e cura já descontando RD, PV temporário, Energia, Defesa/Esquiva/RD/VEL/DT, condições com turnos, Memoespírito (invocar, dispensar, PV) e o painel de Morrendo; cobertura de Elementos, ordem de VEL e os descansos do grupo |
| **Combate** | A Fila de Ação (19.3) com PJs, Memoespíritos em campo, NPCs e inimigos; Ciclo com os quatro passos de avanço; Atrasar e Avançar com Firmeza e teto (19.4); Tenacidade com a calculadora de redução (20.3) e a Quebra com dano e efeito por Elemento (20.5); virada de fase de Boss (28.5); condições com turnos. **Inimigo a 0 PV pula a vez sozinho** — a Fila não espera *Já agiu* por ele —, e curado ele volta |
| **Inimigos** | O bestiário das 32 fichas do capítulo 28 com filtro, o criador pela tabela de âncoras (28.3), **os inimigos da campanha com filtro, ordem e agrupamento** (abaixo) e a **importação/exportação de inimigos em `.json`** |
| **NPCs** | O banco de NPCs: **ficha de personagem completa**, igual à de um jogável, para quem não é do grupo. Criar do zero, copiar de uma ficha salva, filtrar por papel, pôr em cena e a **importação/exportação em `.json`** (abaixo) |
| **Encontros** | Orçamento de PV (27.4) com a leitura de passagem/típico/pesado, **quem do grupo entra na cena** e **quais NPCs entram** (o orçamento e o contrato da Fraqueza se ajustam a isso), as quatro composições e a DT para descobrir Fraqueza (27.3) |
| **Recompensas** | O calendário de marco (27.8), a verba (24.5), a conferência do que o nível de cada um já libera, a **galeria dos Cones de Luz da mesa** (arte, Bônus Maior e Efeito Condicional de cada um) e o tesouro do grupo |
| **Escudo do Mestre** | As tabelas de consulta, imprimíveis: DTs, Tenacidade e Quebra, Fila, as nove regras de inimigo, âncoras, condições e Energia |

**O que é da ficha fica na ficha.** PV, PV temporário, Energia, PH do grupo, condições e Memoespírito que o
Mestre mexer aparecem na aba **Jogar** de cada ficha salva naquele navegador — é o que mantém a mesa
sincronizada. O PH e o tamanho do grupo são gravados em **todas** as fichas, porque são um recurso só.
Só o estado do combate (quem participa, quem já agiu, atrasos) mora na mesa do Mestre.

A mesa tem chave própria no navegador (`explorando-galaxias:mestre`) e se exporta em **Mais > Exportar a
mesa**. Para pôr um jogador no grupo, peça o `.json` da ficha dele e use **Importar ficha**.

### Inimigos em arquivo

Na aba **Inimigos**, o cartão *Importar e exportar inimigos* troca fichas de inimigo em `.json`.
A diferença em relação a **Mais > Importar mesa** é que esta importação **soma** aos inimigos que
você já tem, em vez de substituir a mesa inteira.

- **Exportar .json** no cartão de um inimigo salva só aquela ficha; **Exportar meus inimigos**
  salva todos num arquivo só. O que é de combate (PV gasto, Tenacidade reduzida, condições, fase
  em vigor) não vai no arquivo — a ficha viaja limpa.
- **Importar inimigos** aceita vários arquivos de uma vez e reconhece cinco formatos: o pacote
  que a exportação gera, uma ficha sozinha, uma lista solta de fichas, um arquivo de mesa e um
  backup completo. Nos dois últimos ele pega **apenas** os inimigos e não toca em mais nada.
- **Só o campo `nome` é obrigatório.** Dê `tipo` (Comum, Elite ou Boss) e `faixa_n` (1 a 5) e os
  treze números da ficha vêm da tabela de âncoras de 28.3 sozinhos. Todo remendo que a importação
  precisar fazer aparece como aviso na tela — inclusive quando a contagem de Fraquezas não bate
  com a que o tipo pede (28.2, regra 7).

As coleções prontas ficam em **`site/inimigos/*.json`**, com link de download no próprio cartão.
São 40 fichas montadas pela tabela de âncoras, oito por faixa de nível (5 Comum, 2 Elite, 1 Boss):

| Arquivo | Faixa | Mundo |
|---|---|---|
| `inimigos/estacao-espacial-herta.json` | 1-4 | Estação Espacial Herta |
| `inimigos/jarilo-vi.json` | 5-8 | Jarilo-VI |
| `inimigos/xianzhou-o-loufu.json` | 9-12 | Xianzhou: O Loufu |
| `inimigos/penacony.json` | 13-16 | Penacony |
| `inimigos/amphoreus.json` | 17-20 | Amphoreus |

As Fraquezas delas são **sugestões**: troque à vontade para cumprir o contrato de encontro de 27.5,
que é o que as fichas do capítulo 28 também pedem.

### Achar um inimigo no meio de quarenta

A lista dos **inimigos da campanha** cresce rápido, então ela é feita para ser lida de relance:
cada ficha vem **fechada**, mostrando só nome, tipo, facção, faixa, PV e as Fraquezas, com **Pôr em
cena**, Duplicar, Exportar e Excluir sempre à mão. Clique no nome para abrir e editar — e ela
**continua aberta** enquanto você mexe nos campos.

No cartão *Procurar nos meus inimigos*:

- **Facção**, **Tipo** e **Faixa** filtram; há também uma opção **— sem facção —** para achar o que
  você criou e ainda não batizou.
- **Procurar** acha sem acento e sem maiúscula em nome, facção, tipo, faixa, origem, Fraquezas,
  Resistências e no texto de comportamento.
- **Ordem** reordena: na ordem em que você criou, por nome (A–Z), por **facção** (com título de
  grupo), por tipo (Comum → Elite → Boss), por **faixa** (com título de grupo) ou por PV.
- **Abrir todas as fichas** / **Fechar todas** valem para o que o filtro está mostrando.
- A contagem **"X de Y"** diz quantos o filtro deixou passar, e **Limpar o filtro** devolve tudo.

Filtrar e reordenar não mexe em nada: a ordem de verdade da sua lista continua a mesma, e editar um
inimigo com o filtro ligado edita **aquele** inimigo. Abrir e fechar é estado de tela — não vai
para o arquivo da mesa nem para o backup.

### NPCs

Inimigo e NPC resolvem problemas diferentes. O **inimigo** sai da tabela de âncoras de 28.3: treze
números e nada mais, para a cena de luta. O **NPC** é uma figura com nome — e por isso ele tem a
**ficha de personagem inteira**, a mesma dos jogadores: Raça, Caminho, Atributos, Perícias,
Habilidades, Ultimate, Bênçãos, equipamento, Cone, Relíquias, Ressonâncias e Memoespírito. A tela
que edita a ficha dele é literalmente a aba **Editar ficha**, com os mesmos cálculos e os mesmos
avisos de regra.

- **Nada é obrigatório.** Um NPC só de nome já serve para a sua lista. Se ele for lutar, preencha
  Caminho, Atributos, Elemento, Armadura e Arma — PV, Defesa, RD, VEL, DT e dano saem sozinhos do
  mesmo motor de regras da ficha. A tela diz o que está em branco, sem tratar como erro.
- **NPC não entra no grupo.** A ficha dele mora na mesa do Mestre, não no mapa de fichas dos
  jogadores: ele não aparece no seletor de personagem de ninguém, não é somado ao tamanho do grupo
  e não encosta no PH, que é recurso dos jogadores (16.2). O Memoespírito de um NPC custa a Ação
  Complementar dele e mais nada.
- **Em combate** ele ganha **casa própria na Fila de Ação** pela VEL da ficha, com os desempates de
  19.3 — em empate, os jogadores vêm antes dos NPCs. No painel dele estão os mesmos controles do
  grupo: dano já descontando RD, cura, PV temporário, Energia e Ultimate, condições com turnos,
  Morrendo e o Memoespírito (que também ganha casa própria na Fila).
- **Três papéis**, que mudam só a conta do encontro: **Aliado** age um turno por Ciclo do lado do
  grupo, então o orçamento de 27.4 sobe na mesma proporção de quem está em cena; **Adversário**
  custa os PV máximos da ficha dele, pela regra de que o custo de um inimigo é o PV dele;
  **Neutro** entra na Fila e não mexe em conta nenhuma.
- **O arquivo de NPC é um arquivo de ficha.** Isso vale nos dois sentidos: o `.json` que um jogador
  exporta na aba Jogar importa aqui como NPC (o personagem que saiu da campanha e virou figura da
  história), e um NPC exportado abre como ficha de personagem. A importação **soma** ao banco e
  nunca apaga nada. Só o `nome` é obrigatório; o que faltar fica em branco, e se a ficha ferir
  alguma regra do livro a importação avisa e a tela de editar mostra onde.
- **Copiar de uma ficha salva** faz uma cópia como NPC: a ficha do jogador continua intacta.

As coleções de exemplo ficam em **`site/npcs/*.json`**, com link de download no próprio cartão.
São fichas de **nível 10** (faixa 9-12), todas sem nenhum aviso de regra:

| Arquivo | Papel | Quem |
|---|---|---|
| `npcs/tripulacao-do-expresso-astral.json` | Aliado | Himeko, Welt, Dan Heng e March 7th |
| `npcs/cacadores-de-stellaron.json` | Adversário | Kafka, Silver Wolf e Blade |

Depois de importadas são **suas**: mude nível, Elemento, Bênçãos e Habilidades à vontade.

## Como abrir

- **Pela internet:** o GitHub publica o site sozinho a cada envio para a `main` (`.github/workflows/site.yml`), em `https://mrmarkinboladao.github.io/Explorando-Galaxias-RPG/`.
- **No computador:** abra `site/index.html` no navegador. Funciona sem internet.

## Backup: como não perder as fichas

Tudo fica salvo **no navegador** (`localStorage`), que é apagado se você limpar os dados do site.
Então:

- **Mais → Exportar tudo** gera um arquivo `.json` com **todas as fichas, a mesa do Mestre e o
  banco de Cones**. É o backup da mesa inteira. **Mais → Restaurar um backup** devolve tudo.
- **Mais → Exportar esta ficha** gera o `.json` de um personagem só — é o arquivo que o jogador
  manda para o Mestre pôr no grupo.
- Para ver uma versão nova do site, **nunca** limpe os dados do site: isso apaga as fichas. Use
  `Ctrl+Shift+R` (`Cmd+Shift+R` no Mac), que atualiza o site e **não** mexe no que está salvo.

## Atualizações sem limpar o navegador

Um site estático fica guardado no navegador e no CDN do GitHub, e isso fazia uma versão nova
demorar a aparecer — ou aparecer pela metade, misturando arquivo novo com arquivo velho. Três
peças resolvem isso, e `gerar_site.py` cuida das três:

1. **Selo nos endereços.** O `index.html` carrega tudo com `?v=<selo>`, e o selo é o hash do
   conteúdo desses arquivos. Versão nova = endereço novo, então o navegador é obrigado a buscar
   de novo, e nunca mistura versões.
2. **A casca não se guarda.** O `index.html` vai com `Cache-Control: no-cache` nas metatags.
3. **`versao.json` + aviso.** O site lê esse arquivo direto do servidor (sem cache). Se o selo de
   lá for diferente do que está rodando, aparece uma faixa no topo com **Atualizar agora** — que
   rebusca tudo e recarrega **sem tocar no que está salvo**.

Se algum dia o navegador servir um `dados/` velho com código novo, o site avisa na tela em vez de
quebrar, com o mesmo botão de atualizar.

## Quando o livro mudar

Os textos e as tabelas saem de `livro-v1.0/`. Depois de mudar um capítulo:

```
python site/gerar_site.py
```

Isso refaz `site/dados/livro.js` e `site/dados/catalogo.js`, e atualiza o selo de versão no
`index.html` e no `versao.json`. No GitHub não precisa: o site publicado roda o script sozinho.

Rode também depois de mexer em qualquer arquivo de `js/` ou no `estilo.css` — é o que troca o selo
e faz a atualização chegar nos navegadores.

Os **números das fórmulas** (PV, Defesa, dano, tetos...) moram em `site/js/motor.js`, que é a tradução de `build/oraculo_ficha.py` para JavaScript. Se uma regra numérica mudar, mude nos dois.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `index.html`, `estilo.css` | A página e o visual |
| `js/motor.js` | As regras de personagem (cópia fiel do oráculo Python) |
| `js/ficha-base.js` | Modelo da ficha, salvar, exportar e importar, e o desenho do Cone de Luz |
| `js/cones.js` | O banco de Cones de Luz: a coleção, o arquivo `.json` e os pedaços de tela que a ficha e a Área do Mestre compartilham |
| `js/ficha-editar.js` | A aba Editar ficha |
| `js/ficha-jogar.js` | A aba Jogar |
| `js/mestre-base.js` | Estado da mesa do Mestre, sincronia com as fichas, o modelo de inimigo e de NPC, as regras de mesa (Fila, Firmeza, Tenacidade, Quebra, orçamento), o aviso de abertura e a rota |
| `js/mestre.js` | As telas de mesa: Painel, Grupo, Combate, Inimigos e Encontros |
| `js/mestre-npcs.js` | A tela NPCs: o banco e a ficha de cada NPC (que reaproveita a aba Editar ficha) |
| `js/mestre-escudo.js` | As telas de consulta: Recompensas e Escudo do Mestre |
| `js/regras.js` | A aba Regras (pesquisa e leitura) |
| `js/app.js` | Rolador de dados, avisos e navegação |
| `js/mesa-online.js` | A mesa online: login, convite, fichas ao vivo, PH do grupo, o retrato do combate para os jogadores, pedidos, rolagens e quem está conectado |
| `js/mesa-online-config.js` | A configuração do projeto Firebase da mesa (projeto `explorando-galaxias-rpg`; `null` = desligada) |
| `../firebase/database.rules.json` | As regras do banco da mesa online: quem lê e quem grava o quê. Coladas no console do Firebase |
| `../firebase/firebase.json` | Para rodar a mesa no emulador do Firebase, nos testes |
| `js/vendor/marked.umd.js` | Biblioteca que transforma o texto do livro em página (licença MIT) |
| `inimigos/*.json` | As coleções de inimigos prontas para importar na aba Inimigos |
| `npcs/*.json` | As coleções de NPCs prontas para importar na aba NPCs |
| `dados/*.js`, `img/`, `versao.json` | Gerados por `gerar_site.py`. Não edite à mão |
| `index.html` | A casca. O `?v=<selo>` dos endereços é posto por `gerar_site.py` — rode o script depois de mexer em qualquer `.js` ou no `.css` |
