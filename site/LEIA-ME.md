# Site: ficha online e livro de consulta

Uma página só, sem instalação, com quatro abas:

- **Jogar** — a ficha na mesa: PV com dano e cura (já desconta RD e PV temporários), Energia, PH do grupo, ataques e Testes prontos para rolar (clique no valor), Bênçãos com usos, condições, Morrendo, Memoespírito e inventário.
- **Editar ficha** — os doze passos do capítulo 03, mais progressão, equipamento e Memoespírito. Tudo é recalculado na hora, e o que fere uma regra aparece em vermelho na seção.
- **Regras** — o livro inteiro (v1.2) com pesquisa instantânea, sem acento e sem maiúscula.
- **Área do Mestre** — a mesa do Mestre, sincronizada com as fichas (abaixo).

As fichas ficam salvas **no navegador** de cada jogador. Para backup ou para mandar ao Mestre: **Mais > Exportar** (gera um arquivo `.json`) e **Mais > Importar**.

## A Área do Mestre

Abre com um **aviso de spoiler** curto — é a página que mostra o bestiário e as recompensas, então
quem é jogador e não está mestrando é melhor não entrar. Um clique dispensa o aviso para sempre, e
o botão **Rever o aviso de spoiler**, no fim do Painel, traz ele de volta. Sete telas:

| Tela | O que tem |
|---|---|
| **Painel** | Campanha, faixa, PH do grupo, a tira do grupo com PV e Energia, o Ciclo em curso, a DT da faixa (27.2), rolador e checklist de abertura de sessão |
| **Grupo** | Tamanho do grupo com o PH resultante (16.2); por jogador: PV com dano e cura já descontando RD, PV temporário, Energia, Defesa/Esquiva/RD/VEL/DT, condições com turnos, Memoespírito (invocar, dispensar, PV) e o painel de Morrendo; cobertura de Elementos, ordem de VEL e os descansos do grupo |
| **Combate** | A Fila de Ação (19.3) com PJs, Memoespíritos em campo e inimigos; Ciclo com os quatro passos de avanço; Atrasar e Avançar com Firmeza e teto (19.4); Tenacidade com a calculadora de redução (20.3) e a Quebra com dano e efeito por Elemento (20.5); virada de fase de Boss (28.5); condições com turnos |
| **Inimigos** | O bestiário das 32 fichas do capítulo 28 com filtro, o criador pela tabela de âncoras (28.3) e os inimigos da campanha |
| **Encontros** | Orçamento de PV (27.4) com a leitura de passagem/típico/pesado, as quatro composições, o contrato da Fraqueza (27.5) e a DT para descobrir Fraqueza (27.3) |
| **Recompensas** | O calendário de marco (27.8), a verba (24.5), a conferência do que o nível de cada um já libera e o tesouro do grupo |
| **Escudo do Mestre** | As tabelas de consulta, imprimíveis: DTs, Tenacidade e Quebra, Fila, as nove regras de inimigo, âncoras, condições e Energia |

**O que é da ficha fica na ficha.** PV, PV temporário, Energia, PH do grupo, condições e Memoespírito que o
Mestre mexer aparecem na aba **Jogar** de cada ficha salva naquele navegador — é o que mantém a mesa
sincronizada. O PH e o tamanho do grupo são gravados em **todas** as fichas, porque são um recurso só.
Só o estado do combate (quem participa, quem já agiu, atrasos) mora na mesa do Mestre.

A mesa tem chave própria no navegador (`explorando-galaxias:mestre`) e se exporta em **Mais > Exportar a
mesa**. Para pôr um jogador no grupo, peça o `.json` da ficha dele e use **Importar ficha**.

## Como abrir

- **Pela internet:** o GitHub publica o site sozinho a cada envio para a `main` (`.github/workflows/site.yml`), em `https://mrmarkinboladao.github.io/Explorando-Galaxias-RPG/`.
- **No computador:** abra `site/index.html` no navegador. Funciona sem internet.

## Backup: como não perder as fichas

Tudo fica salvo **no navegador** (`localStorage`), que é apagado se você limpar os dados do site.
Então:

- **Mais → Exportar tudo** gera um arquivo `.json` com **todas as fichas e a mesa do Mestre**.
  É o backup da mesa inteira. **Mais → Restaurar um backup** devolve tudo.
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
| `js/ficha-base.js` | Modelo da ficha, salvar, exportar e importar |
| `js/ficha-editar.js` | A aba Editar ficha |
| `js/ficha-jogar.js` | A aba Jogar |
| `js/mestre-base.js` | Estado da mesa do Mestre, sincronia com as fichas, as regras de mesa (Fila, Firmeza, Tenacidade, Quebra, orçamento), o aviso de abertura e a rota |
| `js/mestre.js` | As telas de mesa: Painel, Grupo, Combate, Inimigos e Encontros |
| `js/mestre-escudo.js` | As telas de consulta: Recompensas e Escudo do Mestre |
| `js/regras.js` | A aba Regras (pesquisa e leitura) |
| `js/app.js` | Rolador de dados, avisos e navegação |
| `js/vendor/marked.umd.js` | Biblioteca que transforma o texto do livro em página (licença MIT) |
| `dados/*.js`, `img/`, `versao.json` | Gerados por `gerar_site.py`. Não edite à mão |
| `index.html` | A casca. O `?v=<selo>` dos endereços é posto por `gerar_site.py` — rode o script depois de mexer em qualquer `.js` ou no `.css` |
