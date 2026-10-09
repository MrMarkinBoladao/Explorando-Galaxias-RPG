# Changelog — da v1.0 para a v1.1

**Sistema:** Explorando Galáxias · **Autoria:** MC Filhos · **Versão:** 1.1

A v1.1 nasceu da **ficha automatizada**. Para a planilha fazer as contas sozinha, cada regra do livro precisou virar fórmula, e uma fórmula não aceita "depende". Onde o livro deixava dúvida ou um exemplo contrariava a regra, a ficha teve que escolher uma leitura. Esta versão escreve essas leituras no livro, para o livro e a ficha dizerem a mesma coisa.

**Nenhum número de balanceamento mudou:** PV, dano, DPC, Tenacidade, orçamento de encontro e tabelas de Habilidade são os mesmos da v1.0. Só uma correção altera um número impresso: o dano da marreta da Nadir (D1), que estava errado pela própria regra do livro.

> **Sobre o nome da pasta.** Os capítulos continuam na pasta `livro-v1.0/`. O nome é **histórico**: renomeá-la obrigaria a mexer em todos os scripts de montagem e verificação, e o conteúdo dela já é o da v1.1. A versão atual é a que está na capa.

---

## As correções

| # | Onde | Como era | Como ficou | Por quê |
|---|---|---|---|---|
| **D1** | 29.7, Passo 12 e ficha fechada | Marreta da Nadir: `1d12 + 4`, **10** médio | `1d12 + 4 + 2` = `1d12 + 6`, **12** médio, com o +2 de **Mãos I** escrito | A mesma ficha tem Mãos I, que soma +2 em todo Ataque Básico (25.3). O exemplo esquecia a Relíquia. A regra manda, então o exemplo mudou |
| **D2** | 07.1 a 11.1, ficha do Caminho | Só 12 a 15 tinham a linha **Recurso próprio** | 07: **os seus PV** (7.2) · 08: acúmulos de **Marca do Vazio** e **Corrupção** · 09: acúmulos de **Eco da Vitória** · 10: acúmulos de **Florescimento** · 11: **Memoespírito** | As nove fichas de Caminho agora têm as mesmas linhas. Onde o Caminho não tem recurso além das Bênçãos, a linha diz isso |
| **D3** | 23.5 | A Vantagem no Teste de Morrendo só aparecia para o Xianzhouíta | Quadro novo: **Xianzhouíta, Vulpes e Avginiano** rolam Morrendo com Vantagem | Vulpes e Avginiano têm Vantagem em Força de Vontade (05), e Força de Vontade é o Teste de Morrendo (22.1). A regra já valia; faltava escrita |
| **D4** | 24.1 (também 03, 18.4 e o resumo de 24) | Pesada: "-2 em Testes e Perícias de Agilidade" | **-2 no Teste de Resistência de Reflexos e nas Perícias de Agilidade** (Acrobacia, Furtividade, Pilotagem). Não afeta o Teste de Ataque, a Defesa nem o Bônus de Agilidade. A Esquiva não fica com -2: ela **não existe** com a Pesada | "Testes de Agilidade" podia ser lido como o Teste de Ataque das armas de Agilidade. 18.2 não lista penalidade de armadura no ataque |
| **D5** | 25.2, Sobreposição (também a tabela de tetos, o resumo de 25 e o glossário) | "Aumenta o Bônus Maior até o teto absoluto de +3 (ou +50 PV)", sem dizer quanto cada cópia soma | **Cada Sobreposição soma +1 na parte numérica e +10 na de PV.** A parte numérica para em +3, e a de PV para junto: 2 Sobreposições nos Níveis 1 e 2 (+30 PV), 1 nos Níveis 3 e 4 (+35 PV), nenhuma no 5. Continua **uma por faixa** | O incremento vem do exemplo do próprio 25.2 (`+1 e +10 PV` → `+2 e +20 PV`). Com +10 por cópia, "+3 ou +50 PV" não fechava: o +3 chegava em 2 cópias e os +50 PV só em 4. Agora a mesma contagem leva aos dois tetos, e nada passa do Cone de Nível 5 (+3 ou +50 PV) |
| **D6** | 21.2, verbete Congelado (também a tabela de 21.5 e 29.12) | O verbete só definia o efeito em Comum, Elite e Boss | Escrito: **Congelado só existe em inimigo** | Congelado vem da Quebra do Gelo, e personagem não tem Tenacidade (20.3, 28.2). Nenhum inimigo, Bênção ou Habilidade do livro Congela personagem |
| **D7** | 04.5 | Perícias escolhidas = `2 + Bônus de Sincronia`, sem dizer de quando | **A quantidade é fixada na criação** (Sincronia já com a Raça). Aumentar a Sincronia depois não dá Perícia nova | O parágrafo seguinte já dizia que Perícia nova depois da criação só vem por decisão de mesa. Faltava dizer que a Sincronia não reabre a conta |
| **N1** | 26.2, linha do nível 16 | "8 (reescreve 1 por nível)" só na linha do 16 | "8 (reescreve 1 por nível, do 16 ao 20)" | 16.6 diz "a partir do nível 16". A célula agora diz o mesmo |
| **N2** | 29.7, Passo 12 | A Nadir tinha Cone de Luz de Nível 1 sem alvo do Bônus Maior | Escrito: o alvo ainda não foi escolhido, e até lá o Cone **não soma em nada** | Nenhum número da ficha fechada incluía o Cone. Agora o texto diz por quê |
| **N3** | 07 a 15, Bênçãos | A frequência das Bênçãos fica no texto do Efeito | **Sem mudança** | Não é erro: cada Bênção já diz no Efeito quando vale ("uma vez por turno", "por Ciclo", "por combate") |
| **N4** | 22.3, Teste de Resistência do inimigo | DT típica 15 / 17 / 18 / 19 / 21 "nas cinco faixas", sem dizer o nível | Escrito: contada no **nível de referência** de cada faixa, **3, 7, 11, 15 e 19** (capítulo 27) | Sem o nível, a conta `8 + 5 + Eficiência` não podia ser refeita. A ficha usava 3, 8, 11, 14 e 19, que dão os mesmos cinco números; o livro fica com os níveis de referência que ele já usa no capítulo 27 |
| **N5** | 26.3, PH | A tabela de PH é de mesa de 4 | **Sem mudança** | 26.3 já diz isso e aponta a fórmula de 16.2, que vale para qualquer tamanho de mesa |
| **R1** | 01.6 e 27.19 (revisão independente) | "a v1.0 foi varrida" e "Esta v1.0 é o livro de regras" no texto corrido | "este livro foi varrido" e "Este é o livro de regras" | O texto falava da v1.0 como versão atual, mas a capa é 1.1. A seção 01.7, que conta a história da v0.1 para a v1.0, fica como está |

---

## O que não mudou

- O changelog **da v0.1 para a v1.0** continua com o nome e o conteúdo dele. Ele registra o que a v1.0 fez com a v0.1, e isso é história. A linha da Armadura Pesada lá ainda diz "-2 em Testes e Perícias de Agilidade", porque era o texto da v1.0; a leitura correta é a de D4 acima.
- Os arquivos `Sistema de HSR by MC Filhos V1.0.docx` e `.pdf` ficam como estão, como registro. Os da v1.1 têm `V1.1` no nome.
