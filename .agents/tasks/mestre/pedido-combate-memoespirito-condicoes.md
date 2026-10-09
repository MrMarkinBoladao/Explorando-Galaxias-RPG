# Pedido do usuário — Memoespírito e Condições no Combate (planilha do Mestre v1.2)

**Origem:** o usuário testou a Planilha do Mestre **em mesa, num combate de verdade**, e sentiu falta
destas capacidades. Registrado pelo orquestrador em 06/10/2026.

**Status:** requisito firme, aprovado pelo usuário. **Não é opcional e não pode ser descartado.**
Deve entrar **antes da Fase 4** (Exemplo e COMO-USAR), para que o Exemplo e o guia já mostrem o
recurso funcionando.

**Peso:** é a maior mudança na aba Combate desde a Fase 1. A Fase 1 já foi aprovada, então isto
**estende** o que existe: nada que a Fase 1 validou pode ser perdido.

---

## 1. O pedido, nas palavras do usuário

> Na planilha do mestre, eu estou sentindo falta de uma coisa. Suponhamos que um player seja da
> recordação e tenha um memoespirito. Não tem como adicionar ou inserir esse memoespirito em lugar
> nenhum. Nem na fila, nem na lista de combate, nem em lugar nenhum. Tinha que ter uma opção e
> escolher em qual personagem esse memoespirito fosse ligado. Ai nas batalhas, poderia escolher algo
> como "Memoespirito invocado?" Sim/Não.
>
> Gostaria de inserir essa capacidade dos personagens tenham memoespirito.
>
> Outra coisa, sobre condições. Se um inimigo levar alguma condição, não tem lugar pra colocar isso.
> Gostaria de tipo, uma lista de condições para o inimigo levar e quantos turnos falta pra terminar.
>
> Se um jogador no meio da batalha levar alguma condição, também não mostra nada. E se o jogador
> acumular condições? Tinha que contabilizar todas elas.
>
> Tinha que mostrar do lado todas as condições que o inimigo e alidos tomaram, para consulta rapida
> do mestre (vai que ele esquece o que faz né?)
>
> Tinha que ter um lugar pra adicionar condições aos inimigos e aliados, varios, e quantos turnos
> faltam pra terminar.

---

## 2. Antes de implementar: verificar, não presumir

O `PROGRESSO.md` afirma que a aba Combate já tem "condições 21.5". **O usuário, usando a planilha em
mesa, não encontrou onde lançar condição nem de inimigo nem de jogador.** As duas coisas podem ser
verdade ao mesmo tempo (por exemplo: existe só um espaço por combatente, ou existe apenas a lista de
referência das condições, ou o campo existe mas não é visível/alcançável no uso real).

Regra: **o relato do usuário é autoritativo.** Abra a aba Combate do `.xlsx` entregue, veja o que de
fato existe hoje para condições e para o Memoespírito, e descreva o achado em `notas-*.md`. É
proibido concluir "já funciona, nada a fazer". Se alguma parte já existir, o trabalho é ampliar e
tornar óbvio no uso, não remover.

---

## 3. Requisitos — Memoespírito (Caminho da Recordação)

- **M1. Vínculo com o PJ.** Na aba **Grupo**, cada PJ pode ter um Memoespírito ligado a ele. O
  vínculo é explícito e escolhido pelo mestre: o Memoespírito pertence ao PJ *X*. Campos: tem
  Memoespírito? (Sim/Não), nome, e os números que o livro define para ele (PV, Velocidade,
  Tenacidade e defesas, ações, custo/limites de invocação, duração).
- **M2. "Memoespírito invocado?" no combate.** Na aba **Combate**, o Memoespírito entra como
  combatente próprio, com a chave **Sim/Não** pedida pelo usuário. Com **Sim**: entra na **Fila de
  Ação** pela Velocidade dele (regra do cap. 19), tem PV, Tenacidade/Quebra e **condições próprias**,
  e aparece identificado como Memoespírito do PJ a que pertence. Com **Não**: sai da Fila e não
  ocupa lugar.
- **M3. Regras do livro v1.2.** Duração da invocação, o que acontece quando o PJ dono cai, limites
  por combate, se ele age no turno do PJ ou em turno próprio: tudo pelo **cap. 11 (Caminho da
  Recordação)** e pelo que os caps. 18 e 19 disserem. Onde o livro não definir o que a ferramenta
  precisa, rotule como **"Sugestão da planilha — não é regra do livro"**, valide e liste no
  relatório e no COMO-USAR.
- **M4. Capacidade.** Pelo menos um Memoespírito por PJ do grupo, sem estourar o limite de
  combatentes da Fila de Ação já implementado.

---

## 4. Requisitos — Condições (cap. 21)

- **C1. Várias por combatente, não uma.** Toda linha de combatente aceita **várias condições ao
  mesmo tempo**: inimigos, PJs/aliados e Memoespíritos. Mínimo de 4 a 6 espaços por combatente (o
  número exato fica a critério do implementador pelo espaço da tela, mas tem de ser "várias", como o
  usuário pediu).
- **C2. Condição + turnos restantes.** Cada espaço tem a condição escolhida numa **lista suspensa com
  as condições do cap. 21** e um **contador de turnos que faltam para terminar**. Sem macro: o mestre
  digita/ajusta o contador; se der para acompanhar o ciclo da Fila por fórmula, melhor, desde que
  continue sendo o mestre quem muda o estado.
- **C3. Painel lateral de consulta rápida.** Do lado, um painel que mostra **todas as condições
  ativas de todos os combatentes de uma vez**: quem está com ela, quantos turnos faltam e **o que a
  condição faz** (efeito resumido do cap. 21). O motivo é o do usuário: o mestre esquece o que cada
  condição faz e não quer abrir o livro no meio da luta.
- **C4. Acumular e contabilizar.** Se um combatente tem 3 condições, as 3 valem, as 3 aparecem e as 3
  entram no painel. Nada de sobrescrever a anterior.
- **C5. Não perder o que existe.** O que a Fase 1 já validou em condições (cap. 21.5), Quebra,
  Morrendo/Executado e Fila continua funcionando, com os mesmos números.
- **C6. Fim da condição.** Quando o contador chega a zero, a condição sai da conta ou fica marcada
  como expirada, com destaque visual (e sem depender só de cor).

---

## 5. Critério de aceitação (do ponto de vista do mestre em mesa)

Numa sessão de verdade, o mestre consegue, sem sair da planilha:

1. ligar um Memoespírito a um PJ da Recordação e ver os números dele;
2. marcar **Memoespírito invocado? Sim** e vê-lo entrar na Fila de Ação na posição certa pela
   Velocidade;
3. lançar **3 condições diferentes num inimigo** e **2 num aliado**, cada uma com os turnos
   restantes;
4. olhar **um painel só**, do lado, e ver tudo que está ativo no combate, em quem, por quantos
   turnos e **o que cada condição faz**;
5. ver a condição sair sozinha da conta quando os turnos acabam.

---

## 6. Regras que continuam valendo

- **Livro v1.2** é a fonte: cap. 21 (condições), cap. 11 (Recordação/Memoespírito), caps. 18 e 19
  (combate e Fila). Número e texto vêm do livro; o que for derivado vira "Sugestão da planilha".
- **Proteção do Google (§0.1 do plano):** toda entrada nova passa pela camada de leitura protegida;
  nenhuma opção de lista pode começar com `=`, `+`, `-` ou `@`, nem parecer data, hora, número em
  texto ou booleano; o contador de erros da Início cobre as células novas; **lint 0**.
- **Sem macro e sem Apps Script.** Mudança de estado é entrada do mestre.
- **Suítes:** estender `dados`, `oraculo`, `determinismo`, `extremos`, `lint`, `texto`, `preview` e
  `visual` ao que for novo, e fechar com **0 falha**. O oráculo independente cobre os números novos
  (Fila com o Memoespírito, duração de condição).
- **Usabilidade:** nenhum texto cortado, contraste ≥ 4,5:1, nada que dependa só de cor, área
  principal cabendo em ~1360 px. Conferir por recorte PNG (nunca abrir imagem com mais de 1800 px em
  qualquer lado, no máximo 4 por vez).
- **Exemplo (Fase 4):** a planilha de Exemplo tem de mostrar um combate com um Memoespírito
  invocado e vários combatentes com condições acumuladas.
- **COMO-USAR (Fase 4):** explicar como ligar o Memoespírito a um PJ, como invocá-lo na batalha, como
  lançar condições com turnos e como ler o painel de consulta rápida.
- **Não alterar** o livro (`livro-v1.0\`), os `.docx`/`.pdf`, nada em `ficha-automatizada\` nem os
  arquivos da ficha em `build\`. Os `.gsheet` são do usuário: ignorar por completo.
