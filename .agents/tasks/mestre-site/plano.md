# Plano — Área do Mestre no site

Aba nova no site (`site/`), ao lado de **Jogar**, **Editar ficha** e **Regras**, com tudo que o
Mestre precisa para rodar uma campanha inteira. O que já existe na planilha `Mestre/*.xlsx` vira
tela, e o estado do combate fica **sincronizado com as fichas dos jogadores** salvas no navegador.

## 1. Navegação

- `index.html`: 4ª aba `<a href="#mestre" data-aba="mestre">Área do Mestre</a>`.
- Sub-rotas (o roteador de `app.js` já entrega `partes`): `#mestre` (Painel), `#mestre/grupo`,
  `#mestre/combate`, `#mestre/inimigos`, `#mestre/encontros`, `#mestre/recompensas`,
  `#mestre/consulta`, `#mestre/campanha`.
- Sub-abas internas (`.sub-abas`) para trocar de tela sem sair da Área do Mestre.

## 2. Aviso inicial, dispensável para sempre

Cartão de abertura que ocupa a tela toda quando `estado.aviso_lido` é falso: explica que a área é
só do Mestre (tem spoiler de bestiário), que os dados ficam **neste navegador** e que a área
**escreve nas fichas** dos jogadores salvas aqui. Um clique em *Entendi — não mostrar mais* grava
`aviso_lido: true` e o aviso nunca volta. Fica um link discreto no rodapé do Painel para quem
quiser reler.

## 3. Estado próprio, chave própria

`localStorage["explorando-galaxias:mestre"]` — **nunca** encostar em
`explorando-galaxias:fichas`, que é o mapa de fichas e é lido como tal em todo o site.

```
{ versao, aviso_lido,
  campanha: { nome, mestre, nivel, jogadores, sessao, notas },
  grupo: [fichaId...],                        // ordem da mesa
  combate: { nome, ciclo, ativo, pjs:{}, memos:{}, inimigos:[] },
  inimigos_salvos: [], encontros: [], tesouro: [], missoes: [], npcs: [], notas: "" }
```

Exportar/importar o estado inteiro em `.json`, igual à ficha.

### Sincronia com as fichas

| O que | Onde mora | Como sincroniza |
|---|---|---|
| PV, PV temporário, Energia, Esforço, Morrendo | `ficha.jogo` | Mestre escreve via `EG.Armazem.salvar` |
| Condições | `ficha.jogo.condicoes` | o Mestre grava `{nome, turnos, origem}`; a ficha lê `nome` e ignora o resto |
| Memoespírito em campo | `ficha.jogo.memo_ativo` / `memo_pv` | igual à ficha |
| **PH do grupo** | `ficha.jogo.ph` de **cada** ficha | escrever em todas, porque o PH é um recurso só |
| **Tamanho do grupo** | `ficha.jogadores` de cada ficha | muda a tabela de PH (16.2): escrever em todas |
| Estado de combate (participa, já agiu, atraso, avanço) | só no estado do Mestre | não é da ficha |

Cuidado de implementação: `ficha-base.js` tem delegados globais em `data-p`, `data-lista` e
`data-acao` que escrevem em `F.P` e chamam `F.salvar()`. A Área do Mestre usa **namespace
próprio** (`data-mp`, `data-m`) e zera `F.P` ao entrar, para não gravar ficha velha por cima.

## 4. Telas

1. **Painel** — campanha, faixa, PH do grupo, tira do grupo com PV/Energia/condições, Ciclo em
   curso, DT da faixa (27.2), rolador e checklist de abertura de sessão.
2. **Grupo** — tamanho do grupo (1-6) com o PH resultante; pôr ficha salva no grupo, importar
   `.json` ou criar ficha; por PJ: PV com dano/cura já descontando RD, PV temporário, Energia com
   aviso de Ultimate pronta, Esforço, Defesa/Esquiva/RD/VEL/DT, condições com turnos,
   Memoespírito (invocar/dispensar, PV, números de 11.4), painel de Morrendo a 0 PV; cobertura de
   Elementos para o contrato da Fraqueza (27.5), ordem de VEL e descansos do grupo.
3. **Combate** — Fila de Ação (19.3) com PJs, Memoespíritos em campo e inimigos; Ciclo com os 4
   passos de avanço; *Agindo agora* / *Já agiu*; Atrasar e Avançar com Firmeza e teto (19.4);
   Tenacidade com a calculadora de redução (20.3) e Quebra com dano e efeito por Elemento (20.5);
   virada de fase de Boss (28.5); condições com turnos; Morrendo (23.4).
4. **Inimigos** — bestiário das 32 fichas com filtro e ficha completa do livro; criador pela
   tabela de âncoras (28.3) com a régua de ações de 28.4; inimigos salvos da campanha.
5. **Encontros** — orçamento de PV (27.4) com leitura de passagem/típico/pesado, as 4 composições,
   contrato da Fraqueza (27.5), DT para descobrir Fraqueza (27.3) e encontros salvos.
6. **Recompensas** — calendário de marco (27.8), verba (24.5), conferência por PJ (o que o nível
   dele já deveria ter), tesouro do grupo e a lista do que não se deve dar.
7. **Consulta** — o Escudo do Mestre: DT por faixa, as 5 DTs de subsistema, redução de
   Tenacidade, dano de Quebra, âncoras, as 9 regras de inimigo, condições (inclusive as de
   inimigo) e as regras da Fila. Imprimível.

## 5. Dados novos, gerados do livro

`build/ficha_dados.py` ganha extratores e `site/gerar_site.py` os publica em `CATALOGO`:

- `mestre.ancoras` (28.3) e `mestre.dano_dados` (28.3)
- `mestre.orcamento` e `mestre.composicoes` (27.4)
- `mestre.acoes_tipo` e `mestre.fraquezas_tipo` (28.2)
- `mestre.atraso_tipo` (19.4)
- `mestre.recompensas` e `mestre.equipamento_faixa` (27.8)
- `bestiario`: as 32 fichas de 28.6 a 28.10, com os números estruturados e o id do bloco do livro
  para abrir a ficha completa

Nada é digitado à mão: se o livro mudar, `python site/gerar_site.py` refaz tudo (é o que o CI faz).

## 6. Arquivos

| Arquivo | O que muda |
|---|---|
| `site/index.html` | aba nova + 2 `<script>` |
| `site/estilo.css` | sub-abas, Fila, barras de Tenacidade, cartões de inimigo |
| `site/js/mestre-base.js` | **novo** — estado, sincronia com as fichas, regras (Fila, Firmeza, Tenacidade, Quebra), aviso e rota |
| `site/js/mestre.js` | **novo** — as telas de mesa (Painel, Grupo, Combate, Inimigos, Encontros) e as ações |
| `site/js/mestre-escudo.js` | **novo** — as telas de consulta (Recompensas, Escudo do Mestre) |
| `build/ficha_dados.py` | extratores novos |
| `site/gerar_site.py` | `mestre` e `bestiario` no catálogo |
| `site/dados/catalogo.js` | regerado |
| `site/LEIA-ME.md` | documenta a aba |
