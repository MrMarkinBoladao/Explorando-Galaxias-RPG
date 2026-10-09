# Plano — Ficha de Personagem Automatizada (Google Planilhas) · Explorando Galáxias v1.0

Escopo: gerar UM `.xlsx` com openpyxl (sem Apps Script, sem macro), pronto para importar no Google Planilhas, níveis 1 a 20, e auditá-lo por script. O livro v1.0 é intocável: nada em `livro-v1.0\`, nos `.docx`/`.pdf` v1.0 nem em `build\gerar_docx.py` / `build\gerar_pdf.py` é editado. Este arquivo é plano: não contém código de produção.

Ambiente fixo: Windows/PowerShell (`;` no lugar de `&&`), `$env:PYTHONUTF8="1"`, aspas duplas em todo caminho, Python 3.14.7 (`python`), openpyxl 3.1.5, formulas 1.3.4, pillow 12.1.0. Nada é instalado. A pasta NÃO é repositório git: trabalhar direto, sem commit. Código Python sempre em arquivo `.py` executado pelo caminho (nunca stdin).

Raiz: `R = g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG`

## 0. Arquivos que o trabalho cria

| Arquivo | Papel |
|---|---|
| `R\build\ficha_dados.py` | Parser dos `.md` do livro + módulo transcrito (só interpretação). Fonte única dos dados da aba Dados |
| `R\build\gerar_ficha.py` | Gera o `.xlsx` (10 abas, fórmulas, estilos, validações) e grava `R\build\ficha_mapa.json` (nome lógico → célula) |
| `R\build\oraculo_ficha.py` | Oráculo Python independente: implementa as regras a partir do livro; não importa `gerar_ficha.py` nem `ficha_dados.py` e não lê fórmula |
| `R\build\testar_ficha.py` | Bateria (`--suite spike|protegidos|dados|ouro|oraculo|extremos|lint|texto|preview|tudo`); sai com código 1 em qualquer falha |
| `R\build\renderizar_ficha.py` | Renderiza cada aba em PNG (openpyxl + pillow) e detecta texto cortado |
| `R\build\ficha_lexico_extra.txt` | Palavras PT-BR permitidas que não aparecem no livro (ex.: "planilha", "célula"), uma por linha |
| `R\Ficha de Personagem - Explorando Galáxias v1.0.xlsx` | Entregável |
| `R\.agents\tasks\ficha-preview\*.png` | Inspeção visual (1 PNG por aba × 3 estados) |
| `R\.agents\tasks\relatorio-auditoria-ficha.md` | Relatório da auditoria: divergências, decisões, resultado de cada suíte |

Comandos oficiais (todas as verificações usam estes):

```
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\gerar_ficha.py"
$env:PYTHONUTF8="1"; python "g:\Meu Drive\DriveSyncFiles\Explorando Galáxias RPG\build\testar_ficha.py" --suite tudo
```

---

## 1. Inventário de regras (cada número que a planilha calcula ou mostra)

Fonte = capítulo `.md` em `livro-v1.0\` + seção. Se capítulo e `design.md` divergirem, vale o capítulo e a divergência vai para o relatório.

### 1.1 Nível, faixa e tabela mestra

| Item | Regra | Fonte |
|---|---|---|
| Nível | inteiro 1–20 | 26.1, 26.2 |
| Faixa | 1-4, 5-8, 9-12, 13-16, 17-20 (índice `INT((L-1)/4)+1`) | 26.3, 17.3 |
| Eficiência | +2 (1-3) +3 (4-6) +4 (7-9) +5 (10-12) +6 (13-15) +7 (16-18) +8 (19-20) = `2+INT((L-1)/3)` | 02.3, 26.4 |
| Eficácia | 2 × Eficiência; slots P/TR: 5→1/1, 8→2/1, 11→2/2, 14→3/2, 17→4/2, 20→5/3; nunca em Teste de Ataque nem na Esquiva | 02.3, 26.4, 18.4 |
| Especialização de Combate | +1 (5), +2 (11), +3 (17), em todo Teste de Ataque, fora do teto | 26.5 |
| Bênçãos possuídas | uma por nível ímpar: `INT((L+1)/2)` | 06.7, 26.2 |
| Habilidades conhecidas | 1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,8,8,8,8; do 16 em diante reescreve 1 por nível | 26.2, 16.6 |
| Nível máximo de Habilidade | 1 (1), 2 (2-5), 3 (6-8), 4 (9-11), 5 (12-14), 6 (15-17), 7 (18-20) | 26.2, 16.6 |
| Aumento de Atributo | níveis 3,6,9,12,15,18: +2 em um **ou** +1 em dois diferentes, teto 20 | 04.3, 26.2 |
| Dados de Ataque Básico | 1 (1-4), 2 (5-8), 3 (9-12), 4 (13-16), 5 (17-20); Energia +1 | 18.5, 26.2, 24.2 |
| Teto de RD | `2 + 2×Eficiência` (6/8/10/12/14/16/18) | 18.4, 26.2 |
| Teto de PV temporários | `3 × Eficiência` (6/9/12/15/18/21/24) | 23.3 |
| Teto de bônus / penalidade somada | +3/-3 (1-9), +4/-4 (10-15), +5/-5 (16-20); somatórios separados | 26.6 |
| Teto de dados adicionais | +3 dados temporários por rolagem, fora os +2 da Fraqueza | 26.6, 16.9 |
| PH do grupo | máx = `1 + nº de jogadores` +1 (9-16) +2 (17-20); início = máx − 2; geração por Ataque Básico que acerta +1 (1-8) / +2 (9-20) | 16.2, 26.3 |
| Ultimate | Nível equivalente 2/3/4/5/6 por faixa | 17.3 |
| Cone de Luz máximo | Nível 1 (1-4), 2 (5-8), 3 (9-12), 4 (13-16), 5 (17-20) | 25.1, 25.2 |
| Tier de Relíquia | I (1-6), II (7-12), III (13-17), IV (18-20) | 25.1, 25.3 |
| Pontos do Memoespírito | `12 + INT(L/2)` (22 no 20), máximo 5 por Atributo | 11.3, 26.3 |
| Evoluções do Memoespírito | níveis 8, 14, 20, cada uma escolhida uma vez | 11.3 |
| Ressonâncias | I (5), II (10), III (15), IV (20) | 26.7 |
| DT geral por faixa | Trivial 8/9/10/11/12 · Fácil 10/12/14/16/18 · Média 13/16/19/22/25 · Difícil 16/19/23/27/30 · Muito Difícil 19/23/27/31/35 · Heroica 22/26/31/34/38 | 27.2, 29.12 |
| DTs de subsistema | Fraqueza 13/14/15/16/17 · Surpresa 13 · Morrendo 10 · Raposa Astuta 10 · To na sua mente 13 | 02.2, 27.3, 20.2 |
| Verba de marco (grupo) | 200 / 500 / 1.200 / 2.500 / 5.000 Cr | 24.5 |

### 1.2 Atributos

| Item | Regra | Fonte |
|---|---|---|
| 6 Atributos | Poder, Agilidade, Vigor, Sincronia, Discernimento, Presença | 04.1 |
| Método A | array 15, 14, 13, 12, 10, 8 — cada valor usado exatamente uma vez (`COUNTIF`=1 por valor) | 03 Passo 4 |
| Método B | todos começam em 8; custo acumulado 8:0 9:1 10:2 11:3 12:4 13:5 14:7 15:10; total ≤ 28 | 03 Passo 4 |
| Tetos | ≤ 15 antes da Raça; ≤ 20 sempre | 03 Passo 4 |
| Bônus de Raça (depois da distribuição) | Humano +2 em um **ou** +1 em dois diferentes · Xianzhouíta +2 Vigor ou Sincronia · Vidyadhara +2 Vigor · Vulpes +2 Discernimento ou Presença · Haloviano +2 Sincronia ou Presença · Avginiano +2 Discernimento · Intellitron +2 Sincronia | 05 (tabela final), 03 |
| Bônus de Atributo | 8-9 -1 · 10-11 +0 · 12-13 +1 · 14 +2 · 15-16 +3 · 17-18 +4 · 19-20 +5 (≥ 15: `INT((v-15)/2)+3`) | 04.2, 29.12 |
| Valor atual | base + Raça + aumentos com nível ≤ nível atual, limitado a 20 (aviso de aumento desperdiçado) | 04.3 |
| Vigor novo e PV | ganho na hora = nível + 2; equivale à fórmula fechada com o Bônus de Vigor atual | 04.3, 06.4 |

### 1.3 Perícias e Testes de Resistência

| Item | Regra | Fonte |
|---|---|---|
| 18 Perícias | Poder: Atletismo · Agilidade: Acrobacia, Furtividade, Pilotagem · Vigor: Resistência · Sincronia: Tecnologia, Pesquisa, Ciência, Mecânica · Discernimento: Percepção, Sobrevivência, Intuição, Investigação · Presença: Persuasão, Intimidação, Enganação, Liderança · Sintonia: Discernimento **ou** Sincronia, fixo na criação | 04.4 |
| Perícias do Caminho | 3 automáticas com Eficiência | 06.3 |
| Perícias escolhidas | `MAX(2, 2 + Bônus de Sincronia)` com a Sincronia da criação (após Raça, sem aumentos); escolher Perícia do Caminho gera aviso "escolha outra" | 03 Passo 7, 04.5 |
| Rolagem | `d20 + Bônus + Eficiência` (Eficácia no slot); sem Eficiência `d20 + Bônus` | 04.4, 02.1 |
| Eficácia em Perícia | só em Perícia que já tem Eficiência; quantidade ≤ slots P | 04.5, 26.4 |
| Sucesso Automático | bônus total ≥ DT → não rola; só Perícia | 27.2 |
| 6 TR | Potência Física (Poder) · Reflexos (Agilidade) · Resistência Física (Vigor) · Resistência Mental (Sincronia) · Percepção Mental (Discernimento) · Força de Vontade (Presença); Eficiência em todos desde o nível 1; Eficácia nos slots TR; sem crítico, sempre rolado | 04.6, 22.1, 22.2 |
| Armadura Pesada | -2 em Reflexos, Acrobacia, Furtividade, Pilotagem (fora do teto) | 24.1, 26.6 |
| Vantagens raciais | Xianzhouíta: todo TR · Avginiano: Resistência Mental, Percepção Mental, Força de Vontade · Vulpes: Persuasão, Intimidação, Enganação, Liderança, Força de Vontade · Vidyadhara: Resistência Física contra água/frio/afogamento (condicional) · Intellitron: Tecnologia, Mecânica, teste de Fraqueza | 05, 22.6 |
| DT das Habilidades | `8 + Bônus do Atributo de Habilidade + Eficiência` | 02.2, 22.3 |

### 1.4 As cinco estatísticas

| Item | Regra | Fonte |
|---|---|---|
| PV máximo | `25 + 5N + 3V + (L-1)×(5+N+V)` (V = Bônus de Vigor atual) + Cabeça + Cone (PV) + Corpo Imortal `2L` (Abundância #7) + Avatar da Recordação Forma Sincronizada `2L` | 06.4, 04.3, 25.2, 25.3, 10, 11 |
| N | Destruição 6 · Preservação 5 · Abundância 5 · Inexistência 4 · Harmonia/Erudição/Euforia/Recordação 3 · Caça 2 | 06.3 |
| Defesa | `10 + Agilidade + armadura (Leve 3 / Média 5 / Pesada 6) + Tronco + Cone (Defesa) + Forma Sincronizada (+1)` + temporários no teto | 18.4, 24.1, 25 |
| Esquiva | Reação: Defesa + **Eficiência**; proibida com Pesada | 18.4 |
| RD | Pesada 2 + Cone (RD) + Pele de Pedra 2 (Preservação #4) + Corpo Imortal (= Ef) + Conjunto (+1) + temporária; limitada ao teto | 18.4, 24.1, 25, 15, 10 |
| Velocidade | `10 + Agilidade + Bônus do Caminho + Leve(+1)/Pesada(-2) + Botas + Cone (VEL) + Conjunto (+1) + Ressonância I (+1) + Avatar da Caça (+2)`; aviso fora de 7–25 | 19.1, 06.5, 24.1, 25.3, 26.7, 14 |
| Bônus de VEL do Caminho | Caça +4 · Euforia +3 · Harmonia +2 · Inexistência +2 · Destruição/Erudição/Abundância/Recordação +1 · Preservação +0 | 06.3, 19.1 |
| PV temporários / Barreira | teto `3×Ef`; não acumulam (fica o maior); RD antes, temporário depois | 23.3, 15.2 |
| Movimento | 1 Distância por Ação de Movimento; Esforço Total = 2 | 18.1, 18.6 |

### 1.5 Ataques, Habilidades, Ultimate, Energia

| Item | Regra | Fonte |
|---|---|---|
| Teste de Ataque | `d20 + Atributo de Ataque + Eficiência + Especialização + Cone (Teste de Ataque) ± temporários (teto)` | 18.2, 26.6 |
| Armas | Leve 1d8 Pessoal Agilidade · Média 1d10 Pessoal Poder ou Agilidade (fixo) · Pesada 1d12 Pessoal Poder · Disparo curto 1d8 Média Agilidade · Disparo longo 1d10 Longa Agilidade · Energia 2d8 Longa Sincronia; RT 1; Espaço 1/1/2/1/2/2; 100/150/200/250/350/500 Cr | 18.5, 24.2 |
| Propriedade especial (máx. 1) | Recarga · Arremessável · Alcance estendido (+1 passo) · Peso de impacto (+1 RT; Leve/Média viram 2 mãos) · Dissimulada (0,5 Espaço) | 24.2, 18.7 |
| Dano do Ataque Básico | `nd(face) + Atributo + Mãos + Cone (AB) + Conjunto (+2)`; média `INT(n×(f+1)/2)` + fixos; Elemento da arma ou Físico; Esfera Planar nunca no básico | 18.5, 25.3, 02.5 |
| Fraqueza / Resistência | +2 dados (não critam) / -2 dados (mín. 1); RT total / metade (mín. 1) / 1 | 20.2 |
| Crítico | 20 natural; 19-20 só com Olho de Lan (Caça #1); dobra só dados base | 18.3, 14.3 |
| Habilidade por Nível | dano 6d6/5d10/6d12/6d20/10d20/14d20/18d20 (21/27/39/63/105/147/189); cura 5d8/6d10/8d12/7d20/10d20/14d20/18d20 (22/33/52/73/105/147/189); PH 1/1/2/3/4/5/6; RT 2/2/3/4/5/6/7; alcance cumulativo Pessoal+Curta / +Média / +Longa / +Extrema / Extrema | 16.3 |
| Dano/cura de Habilidade | dados + Bônus do Atributo de Habilidade (uma vez) + Esfera Planar (se Elemento da Esfera = Elemento pessoal) + Cone (Habilidade) | 16.3, 25.3 |
| Área | metade dos dados (mín. 1); até 3 alvos (4 nos Níveis 6-7); teto 6; mesmo custo | 16.4 |
| Passiva | não custa PH; conta no teto de 8 | 16.5 |
| Buff/Debuff/Passiva | texto-guia da linha do Nível | 16.5 |
| Ataque de Habilidade/Ultimate | `d20 + Atributo de Habilidade + Eficiência + Especialização + Cone` | 18.2, 03 Passo 5 |
| Ultimate | equiv. 2/3/4/5/6; dano 5d10/6d12/6d20/10d20/14d20; cura 6d10/8d12/7d20/10d20/14d20; RT 5; área: metade e 3 alvos (4 com equiv. 6); custo 100 (80 com Ressonância IV opção A); 1 por Ciclo | 17.1, 17.3, 26.7 |
| Energia | AB +20 · Habilidade +30 · sofrer dano +10 (1/Ciclo) · derrotar +10 · Quebrar +10 (1/Ciclo) · Memoespírito metade · Corda de Ligação 10/15/20/25 (1/combate) · Cone Nível ≥ 3 +5 (1/Ciclo); acima de 100 perdido; não zera em descanso | 17.2, 25.3 |
| Ressonância III | uma Habilidade sobe 1 Nível de efeito e custa o PH do Nível novo, sem passar do máximo | 26.7 |

### 1.6 Caminhos, Bênçãos, Memoespírito

| Item | Regra | Fonte |
|---|---|---|
| 9 Caminhos | Aeon, Atributo de Habilidade, 3 Perícias, N, Bônus de VEL | 06.2, 06.3 |
| Atributo de Habilidade | Destruição Poder/Vigor · Inexistência Discernimento/Sincronia · Harmonia Presença · Abundância Presença/Sincronia · Recordação Sincronia/Discernimento · Erudição Sincronia · Euforia Presença/Discernimento · Caça Agilidade · Preservação Vigor/Poder | 03 Passo 5, 06.3 |
| Recurso próprio | Erudição Acúmulos de Cálculo (máx. 5) 12.2 · Euforia Tabela do Riso 1d6 13.2 · Caça Marcação de Presa (1 alvo) + crítico 19-20 14.2/14.3 · Preservação Barreira (`3×Ef`) 15.2 · Recordação Memoespírito 11 · Destruição PV como moeda (`2×L`, `5×L`) 7.2 · Inexistência/Harmonia/Abundância: sem linha "Recurso próprio" | 07–15 |
| 108 Bênçãos | 12 por Caminho: 6 Tier I (sem requisito), 4 Tier II (nível 9), 2 Tier III (nível 17, uma é Avatar); slots 1,3,…,19; Tier I cabe em qualquer slot; sem repetição; permanente | 06.6, 06.7, 07–15 |
| Contadores | frequência ("uma vez por turno/Ciclo/combate/Descanso Longo", "2 vezes por dia") e acúmulos (Fúria 2, Marcas da Ruína 5, Florescimento 5, Fragmentos de Memória 5, Corrupção 5, Marca do Vazio 3, Lembranças Passadas 3) | textos das Bênçãos |
| Memoespírito (só Recordação) | pontos `12+INT(L/2)`, máx. 5 por atributo; PV `8L + 3×Vigor`; Defesa `10 + Agilidade + Ef`; VEL `10 + Agilidade + Bônus de VEL do Caminho`; ataque `d20 + Atributo de Habilidade do dono + pontos de ataque + Ef`; dano `(dados de AB do dono)d6 + pontos de ataque`; RT 1 (2 a partir do 11); TR `d20 + pontos + Ef`; RD 0; Função: Predador +1d8 · Guardião +3L PV · Catalisador +1 no ataque do dono · Controlador; Bônus menores: Força Espiritual +2 dano · Resistência Espiritual +2L PV e +1 RD · Velocidade Espiritual +2 VEL · Memória Afiada · Vínculo Profundo · Forma Mutável; invocar = Ação Complementar + 1 PH; Energia metade | 11.3–11.5, 29.9 |

### 1.7 Equipamento

| Item | Regra | Fonte |
|---|---|---|
| Armaduras | Leve +3, +1 VEL, Esp 1, 150 Cr · Média +5, Esp 2, 300 Cr · Pesada +6, 2 RD, -2 Agilidade, -2 VEL, sem Esquiva, Esp 3, 500 Cr | 24.1 |
| Poções | Pequena 15 / 0,5 / 50 Cr · Média 30 / 1 / 150 · Grande 50 / 2 / 400 | 24.3 |
| Itens comuns | 11 itens com Espaço e preço | 24.3 |
| Inventário | capacidade `10 + 2×Bônus de Poder`; acima → Lentidão; acima do dobro → não se move; vestido/empunhado conta; Créditos não ocupam | 24.4 |
| Técnica | 1 por personagem, 2 usos por Descanso Longo, fora de combate | 24.6 |
| Cone de Luz | Nível 1 +1 **ou** +10 PV · 2 +1 **e** +10 PV · 3 +2 ou +25 PV · 4 +2 e +25 PV · 5 +3 ou +50 PV; alvo: PV, Defesa, VEL, Dano (AB/Habilidade/Ultimate), RD, Teste de Ataque, um TR, uma Perícia; Sobreposição: teto +3 / +50 PV, no máximo uma por faixa | 25.2 |
| Relíquias | Cabeça PV 10/20/35/50 · Mãos AB 2/4/6/8 · Tronco Defesa 1/1/2/2 · Botas VEL 2/3/4/5 · Esfera Planar dano de um Elemento 2/4/6/8 · Corda de Ligação Energia 10/15/20/25 | 25.3 |
| Conjuntos | 2 peças: +1 em um tipo de rolagem, +1 VEL, +2 dano ou +1 RD · 4 peças: efeito condicional por Ciclo · 4+2 ou 2+2+2 · teto +3 e dentro do teto global | 25.3, 25.4 |

### 1.8 Condições, Elemento/Quebra, Morte e Descanso

| Item | Regra | Fonte |
|---|---|---|
| Catálogo | 16 condições (tabela 21.5); máx. 5 instâncias; cura não remove; Descanso Longo remove todas | 21.1, 21.5 |
| Elemento → Quebra | Físico Sangramento · Fogo Queimadura · Gelo Congelamento · Raio Choque · Vento Cisalhamento de Vento · Quântico Embaraço · Imaginário Aprisionamento | 20.1 |
| Dano de Quebra | Físico/Fogo `2d6 + 2×Ef` · Raio/Vento `1d6 + Ef` · Gelo/Quântico/Imaginário `Ef` | 20.5 |
| Quebra | Dano de Quebra + efeito + Atrasa 1 casa + Quebrado + 10 Energia | 20.4 |
| Redução de Tenacidade | AB 1 · Habilidade 2/2/3/4/5/6/7 · Ultimate 5 · Dano Contínuo 0 | 20.3 |
| Morrendo | 0 PV, mantém a casa; `d20 + Bônus de Presença` (sem Eficiência) ≥ 10; 3 sucessos → 1 PV; 3 falhas → morre; 20 natural levanta; 1 natural = 2 falhas; dano = 1 falha (2 se crítico ou Nível 5+); cura tira e zera | 23.4 |
| Executado | ser racional, Ataque Básico, Distância Pessoal; Intervir cancela; Xianzhouíta imune | 23.5, 05 |
| Xianzhouíta | Vantagem em todo TR (inclusive Morrendo, 23.5); não pode ser Executado | 05, 23.5 |
| Vidyadhara | reencarna um dia depois; 1d20: 16-20 lembra nome, Raça, Propósito e 2 coisas; 1-15 só nome, Raça, Propósito | 05 |
| Descanso Curto | 1 hora, até 2 por dia; PV `2L + Bônus de Vigor`; recarrega "1 vez por descanso"; reinvoca o Memoespírito | 23.6 |
| Descanso Longo | 8 horas, 1 por dia; todos os PV; remove condições; recarrega tudo; devolve Esforço; recria Habilidade | 23.6 |
| Esforço (Humano) | máximo 1 | 05 |
| To na sua mente (Haloviano) | 2 vezes por dia; ativação Sintonia DT 13 (sem teste na Harmonia) | 05 |
| Aritmética | arredonda para baixo; dano mínimo 1; mínimo 1 dado | 02.5 |
| Vantagem/Desvantagem | 2d20 maior/menor; não acumulam; cancelam por presença | 02.4 |

### 1.9 Divergências já encontradas (vão para o relatório com a decisão)

- **D1** — 29.7 "ficha fechada": marreta `1d12 + 4` (média 10), mas a mesma ficha tem **Mãos I** (+2 no Ataque Básico, 25.3). Pela regra o total é `1d12 + 6` (média 12). A planilha mostra duas colunas: "dados + atributo" (= livro) e "total com equipamento" (= regra).
- **D2** — Só 12–15 têm a linha "Recurso próprio"; 07 tem "PV como moeda" (7.2), 11 o Memoespírito; 08–10 não declaram. A planilha mostra "Sem recurso próprio declarado" nesses três, mais os contadores das Bênçãos adquiridas.
- **D3** — Vantagem no Teste de Morrendo: 23.5 cita só o Xianzhouíta; Vulpes e Avginiano têm Vantagem em Força de Vontade e 22.1 diz que esse "é o Teste de Morrendo". A planilha mostra Vantagem nos três, com nota "leitura combinada de 05 e 22.1".
- **D4** — Pesada "-2 em Testes e Perícias de Agilidade": aplicado em Reflexos e nas 3 Perícias de Agilidade; não no Teste de Ataque (18.2 não lista penalidade de armadura).
- **D5** — Sobreposição sem incremento numerado: usa-se o exemplo de 25.2 (`+1 e +10 PV` → `+2 e +20 PV`): +1 numérico e +10 PV por cópia, tetos +3 / +50 PV, no máximo uma por faixa alcançada.
- **D6** — Congelado em personagem: o verbete só define Comum/Elite/Boss; na ficha só texto.
- **D7** — Perícias escolhidas usam a Sincronia da criação (04.5).

Toda divergência nova encontrada pela bateria entra no relatório.

---

## 2. Arquitetura das abas

Nomes com acento correto em PT-BR (o usuário pediu revisão de ortografia; o Google aceita): **Início, Criação, Em Jogo, Testes, Habilidades, Caminho, Equipamento, Progressão, Regras Rápidas, Dados**. Só se o spike (item 1) mostrar que `formulas` 1.3.4 quebra com acento em nome de aba, usar a forma sem acento e registrar no relatório.

### 2.1 Convenções visuais (legenda no topo de cada aba)

| Tipo de célula | Estilo |
|---|---|
| Entrada (você preenche) | fundo `#FFF2CC`, borda fina `#BF9000`, texto preto |
| Calculada (não editar) | fundo `#E8EEF7`, texto `#1F1F1F` |
| Aviso | texto `#9C0006` negrito; fundo `#FFC7CE` só quando há aviso (formatação condicional `LEN(célula)>0`) |
| Título de bloco | fundo `#1F3864`, texto branco, negrito |
| Não se aplica / slot futuro | fundo `#D9D9D9`, texto `#595959` |

Arial em todo o arquivo (10 pt corpo, 12–16 pt títulos). Cor nunca é o único sinal: cabeçalhos dizem "(preencha)" ou "(automático)" e avisos são texto. Contraste ≥ 4,5:1 nas combinações acima.

### 2.2 Abas

**Início** — título, autoria MC Filhos, versão; "Como usar em 6 passos"; legenda; guia de importação (Drive → Abrir com → Planilhas Google → Arquivo → Salvar como Planilhas Google); guia de proteção nativa (Dados → Proteger páginas e intervalos → intervalos calculados → "Mostrar um aviso ao editar este intervalo"); **Painel de avisos**: uma linha por aba com a contagem de avisos (`SUMPRODUCT(--(LEN(intervalo)>0))` sobre a coluna de avisos) e o primeiro aviso.

**Criação** — os 12 passos do capítulo 03 de cima para baixo:
- Cabeçalho: Nome, Jogador, **Nível atual** (1–20), **Nº de jogadores na mesa**, **Método de atributos** (Array oficial / Compra de Pontos).
- Passo 1: Conceito, Propósito de Vida, crença do Esforço (só Humano).
- Passo 2: Raça (lista) + bônus racial (lista dependente: modo do Humano "+2 em um / +1 em dois", Atributo 1, Atributo 2); traços com o texto inteiro.
- Passo 3: Caminho (lista) + Aeon, N, Bônus de VEL, 3 Perícias.
- Passo 4: 6 Atributos: valor distribuído (entrada) · Raça · aumentos (da Progressão) · valor atual · Bônus · aviso; abaixo, validação do array (uso único) ou custo da Compra (gasto/28).
- Passo 5: Atributo de Habilidade (lista dependente do Caminho) + DT e ataque de Habilidade.
- Passo 6: Elemento (lista) + efeito e Dano de Quebra.
- Passo 7: Sintonia usa (Discernimento/Sincronia); permitidas; marcação "Escolhida" das 18 Perícias (as 3 do Caminho já aparecem como "Caminho").
- Passo 8: Armadura (lista) + PV, Defesa, Esquiva, RD (teto), VEL.
- Passos 9–11: status ("Preencha a Habilidade 1 na aba Habilidades" / "OK").
- Passo 12: Arma principal (nome, categoria, atributo se Média, Elemento próprio, propriedade), Técnica, "a coisa que não serve para nada".
- Coluna de avisos à direita de cada passo.

**Em Jogo** — cabe em uma tela (A:L, largura somada ≤ 1360 px; linhas 1–40), por frequência de uso:
- A1:D12 **Resumo para o Mestre** (fixo no canto superior esquerdo): Nome · Raça/Caminho/Nível · Elemento · PV atual/máx · Defesa/Esquiva · RD · VEL · DT das Habilidades · melhor ataque · Vantagens raciais · condições ativas · "Pode ser Executado?".
- E1:H12 **Recursos**: PV atual (entrada), PV temporários/Barreira (entrada, teto), Energia (entrada) + "Ultimate pronta?", PH do grupo (entrada; máx/início automáticos), Esforço (Humano), recurso do Caminho, Memoespírito ativo (Sim/Não, só Recordação), acúmulos das Bênçãos adquiridas.
- I1:L12 **Calculadora de dano**: dano bruto + "É Dano Contínuo?" → RD aplicada, absorvido pelo temporário, PV perdidos (mín. 1), "PV novo: X"; e "Descanso Curto recupera X PV".
- A14:L24 **Ações**: Ataque Básico (rolagem `d20+6`, dano `1d12+6 · média 12`, com Fraqueza, crítico, RT, alcance, Elemento), arma secundária, Habilidades 1–8 resumidas (Nível, PH, rolagem ou DT, média, RT, "BLOQUEADA" se Silenciado/Controlado), Ultimate (custo, dados, média, RT 5).
- A26:F33 **Testes de Resistência** (6 + Morrendo com sucessos/falhas) e G26:L33 Perícias com Eficiência (rolagem pronta).
- A35:L40 **Condições ativas** (4 linhas: condição em lista + turnos, efeito exibido) e **Usos por combate/descanso** (Bênção ou traço, frequência, usado Sim/Não).

**Testes** — 18 Perícias (atributo · Bônus · origem · Eficiência · Eficácia (entrada) · penalidade · Vantagem · bônus total · rolagem · aviso), 6 TR (mesmas colunas) + Morrendo; slots de Eficácia usados/permitidos; DT da faixa.

**Habilidades** — 8 linhas: Nome · Tipo (Dano/Cura/Buff/Debuff/Passiva) · Nível · Área (Sim/Não) · Resolução (Teste de Ataque / Teste de Resistência) · Alcance · Ressonância III aqui (Sim/Não) → Nível efetivo · dados · média · bônus fixo · total · PH · RT · alcance máximo · alvos · rolagem ou DT · guia de 16.5 · aviso. Bloco Ultimate (nome, frase, tipo, área, resolução, efeito; automáticos: Nível equivalente, dados, média, RT, custo). Conhecidas/permitidas e aviso de reescrita a partir do 16.

**Caminho** — ficha do Caminho; recurso próprio com máximo e custos; 10 slots de Bênção (nível do slot · Bênção em lista dependente · tier · requisito · liberado? · resumo · frequência · aviso); catálogo das 12 com "pode escolher agora?"; bloco **Memoespírito** (cinza e "Só para A Recordação" fora dela): nome, Conceito, Função, Elemento, pontos por atributo (total/gastos/aviso), atributo de ataque, 3 Bônus menores, 2 Habilidades (texto), Evoluções 8/14/20, estatísticas.

**Equipamento** — arma principal e armadura (espelho da Criação) e arma secundária (entrada); Cone de Luz (nome, Nível, alvo, "numérico ou PV" nos Níveis "ou", Sobreposições, efeito em texto) com valor e aviso de Nível acima do permitido; Relíquias (possui Sim/Não · nome · Conjunto A/B/C/— · Tier automático · bônus); Conjuntos A/B/C (nome, tipo do bônus de 2 peças, texto de 4 peças, peças por `COUNTIF`, ativo 2/4); inventário (20 linhas; Espaço automático para item do catálogo) + capacidade, ocupado (inclui arma e armadura), estado; Créditos (saldo inicial + 10 lançamentos).

**Progressão** — tabela mestra 1–20 (26.2 + PH, Ultimate, Cone, Tier) com a linha do nível atual destacada; aumentos (3,6,9,12,15,18: modo, Atributo 1, Atributo 2, aviso); Ressonâncias I–IV (opção, ativa quando nível ≥ marco); "O que você ganha no próximo nível".

**Regras Rápidas** — referência de uma página (29.12) + condições completas (21.5) + Dano de Quebra (20.5) + Energia + tetos + Morrendo + Descanso.

**Dados** — tabelas usadas por fórmula, em blocos com título e fonte (capítulo/seção) na linha de cima; listas de validação. Visível (o guia ensina a ocultar).

---

## 3. Decisões registradas

1. **Condições aplicadas nos números** só quando inequívocas no próprio personagem: Lentidão (Movimento "0; 1 Distância só com Esforço Total"), Silenciado (Habilidades Nível ≥ 4 BLOQUEADAS), Controlado (Habilidades e Ultimate BLOQUEADAS), Surpreso (aviso "casa pulada no 1º Ciclo"), Morrendo (liga sozinho com PV atual = 0 e mostra `d20 + Presença ≥ 10` com contador), sobrecarga → Lentidão. Só exibição: os Danos Contínuos (texto + tique estimado com "Eficiência de quem aplicou"; Sangramento calcula `INT(5% × PV máx)` com teto `3×Ef` do aplicador), Congelado, Marcado, Vulnerável, Corrupção. Quebrado fica fora da lista do personagem (20.3). Motivo: o resto depende do aplicador ou do inimigo, e número errado na ficha é pior que texto.
2. **Bênçãos aplicadas nos números** (efeito fixo, sem decisão de mesa): Corpo Imortal (PV +2L, RD = Ef), Pele de Pedra (RD +2), Olho de Lan (crítico 19-20), Avatar da Caça (VEL +2), Avatar da Recordação Forma Sincronizada (PV +2L, Defesa +1, +1 dado base), Instinto de Sobrevivência (+2 ataque com PV ≤ 1/3 do máximo), Memória Compartilhada / Memória da Guarda / Função Catalisador / Fusão de Memórias (com "Memoespírito ativo = Sim"), Sacrifício Desesperado (+1d6 por acúmulo), Cicatriz da Destruição (+1 dano, +1 Força de Vontade e Resistência Mental por Marca), Florescimento da Alma (+1 TR e Defesa por acúmulo), Ecos do Passado (Memoespírito). Todo bônus temporário passa por `MIN(teto da faixa, soma)` e o excesso gera aviso. As demais Bênçãos aparecem como resumo de uma linha do livro + frequência.
3. **Dados: parser + módulo transcrito, com teste obrigatório.** Tabelas markdown (Raças 05, Perícias 04.4, TR 04.6, Caminhos 06.3, PV 06.4, Bênçãos via `### N. Nome` + linha `**Tier …**` + "Resumo do capítulo" de 07–15, armas 24.2, armaduras 24.1, poções/itens 24.3, Cone 25.2, Relíquias 25.3, Ressonâncias 26.7, tabela mestra 26.2, Habilidades 16.3/16.5, Ultimate 17.3, PH 16.2, Energia 17.2, Dano de Quebra 20.5, condições 21.5, DT 27.2, TR/DT de inimigo 22.3) são lidas por parser em `ficha_dados.py` na hora de gerar. Fica transcrito só o que é interpretação (frequência/acúmulo por Bênção, efeitos automáticos, textos de traço), cada item com uma "âncora" literal do capítulo, e o teste confere que a âncora existe no `.md`. A suíte `dados` relê os `.md` com um parser próprio do teste e compara célula a célula com a aba Dados.
4. **Rolador de dados: não incluir.** A ficha entrega a rolagem pronta (`d20+6`, `6d6+4 · média 25`). Motivo: `RANDBETWEEN` recalcula a cada edição em qualquer aba; as 10 abas não reservam espaço; a mesa rola dado físico.
5. **PV atual: entrada direta + calculadora de dano** (ordem 23.1/23.3: RD, exceto Dano Contínuo → PV temporário → PV, mínimo 1) que mostra "PV novo: X". Motivo: registro corrido exigiria referência circular ou histórico crescente e não há botão sem Apps Script.
6. **Sem nomes definidos nas fórmulas.** Referência direta `'Em Jogo'!E3`. O gerador grava `ficha_mapa.json` (nome lógico → célula) para os testes.
7. **Arredondamento só com `INT`**; `ROUNDDOWN` banido pelo lint (falha em negativo).
8. **Fora da faixa** (atributo < 8 ou > 20, nível fora de 1–20, jogadores fora de 1–6): aviso PT-BR e conta com o valor limitado; nunca erro. Jogadores fora de 3–6: aviso "fora da tabela do livro" e calcula.
9. **PV rolado** (variante de 06.4) não é calculado; citado em Regras Rápidas.
10. **Listas dependentes** usam intervalo auxiliar `INDEX/MATCH` na própria aba da entrada (colunas auxiliares à direita, cinza e estreitas); sem `INDIRECT`.
11. **Validação de dados** com `errorStyle="warning"` e mensagens PT-BR; a regra de negócio vive na coluna de aviso.
12. **Inputs de criação na Criação; equipamento de faixa na Equipamento.** Arma principal e armadura são entradas da Criação (passos 8 e 12, como no livro) e aparecem espelhadas na Equipamento; Cone, Relíquias, Conjuntos, inventário e Créditos são entradas da Equipamento. Nenhuma entrada existe em dois lugares.

---

## 4. Regras de compatibilidade Google Planilhas (checadas pelo lint)

- Sintaxe canônica em inglês, separador `,`, ponto decimal (`=IF(A1>=0,"+"&A1,A1)`); nunca função em português nem `;`.
- Lista branca: `IF, IFERROR, AND, OR, NOT, SUM, SUMIF, SUMPRODUCT, COUNTIF, COUNTIFS, COUNTA, COUNTBLANK, INDEX, MATCH, VLOOKUP, HLOOKUP, CHOOSE, MIN, MAX, ROUNDUP, ROUND, INT, MOD, ABS, LEN, TRIM, CONCATENATE, REPT, ISBLANK, ISNUMBER, ISERROR, ROWS, LARGE, SMALL` e `&` (`ROUNDDOWN` sai pela decisão 7). Função que o spike mostrar que `formulas` 1.3.4 não calcula também sai e vai para o relatório.
- Proibidas: `LET, LAMBDA, XLOOKUP, FILTER, UNIQUE, SORT, SEQUENCE, TEXTJOIN, IFS, SWITCH, ARRAYFORMULA, QUERY, IMPORTRANGE, REGEX*, TEXT, INDIRECT, OFFSET, ROUNDDOWN`; referência estruturada; link externo `[arquivo]`.
- Sinal `+3` com `IF`, nunca `TEXT()`.
- Formatação condicional e validação personalizada só na mesma aba (sem `!`); dropdown por intervalo explícito pode apontar outra aba.
- Sem caixa de seleção, sem proteção do Excel, sem macro, sem Tabela do Excel, sem nome definido; abas sem emoji; só Arial; `wb.calculation.fullCalcOnLoad = True`.
- Nenhum valor de erro em nenhum estado: toda `MATCH`/`INDEX`/`VLOOKUP`/divisão protegida por `IF(célula="","",…)` e/ou `IFERROR`.

---

## 5. Plano de testes (`build\testar_ficha.py`)

Todas as suítes calculam com `formulas` 1.3.4 (`ExcelModel().loads(xlsx).finish()`, depois `model.calculate(inputs=…, outputs=…)` com chaves `'[ARQUIVO.XLSX]ABA'!A1` em maiúsculas). Nunca se valida lendo o texto da fórmula. Um modelo carregado por processo; cenários via `inputs`. Se uma rodada passar de 5 s, usar `outputs=` restrito e `multiprocessing`.

| Suíte | O que faz | Meta |
|---|---|---|
| `spike` | Workbook mínimo com cada função da lista branca, referência entre abas com espaço e acento, `INDEX/MATCH` em outra aba, célula vazia em conta, `IFERROR`, `COUNTIF` com texto; compara com Python e mede tempo | lista efetiva gravada em `build\ficha_funcoes_ok.json` |
| `dados` | Parser do teste relê os `.md` e compara com a aba Dados: 7 Raças, 18 Perícias, 6 TR, 9 Caminhos, 108 Bênçãos (12×9 com tier/requisito), armas, armaduras, poções/itens, Cone, Relíquias, Ressonâncias, 16 condições, 7 Elementos/Dano de Quebra, tabela mestra 1–20, Habilidades 1–7, Ultimate, PH, Energia, DT; âncoras do transcrito | 0 diferenças |
| `ouro` | (a) Nadir nível 1 de 29.7: Poder 17/+4, Vigor 14/+2, Agilidade 13/+1, Discernimento 12/+1, Presença 10/+0, Sincronia 8/-1, PV 61, Defesa 16, Esquiva 18, RD 0, teto 6, VEL 14 com Botas I (12 sem, 03), DT 14, ataque +6, AB `1d12+4` média 10 e total 12 (D1), Rebarba `6d6+4` média 25, A Doca Inteira `5d10+4` média 31, PH 3/5, Espaço 18, 5 Perícias, Pacto da Ruína 2 PV/+2 (+4 com PV ≤ 30); (b) Atletismo +6 no nível 3 (02.1); (c) tabela de PV de 06.4 (20 níveis × 5 N, Vigor +2); (d) Lin Hai +11 PV no 9 (04.3); (e) Memoespírito nível 17 de 11.4 (PV 151, Defesa 21, VEL 15, ataque +17, `5d6+5` ≈ 22, RT 2); (f) Barreira no 13 = 18 (15.2), teto temporário no 11 = 15 (23.3); (g) Descanso Curto 8/16/24/32/40 (23.6); (h) Quebra Físico `2d6+4` média 11 no 3 e `2d6+16` média 23 no 19, Gelo 2 e 8 (20.5); (i) Vesper nível 11 rifle `3d10+9` e `5d10+9` com Fraqueza (18.5), Ultimate `6d20` → `10d20` no 13 (17.4); (j) Nadir nível 15 Tier III com Conjuntos 4+2: +35 PV, +2 Defesa, +5 VEL, +6 AB, +6 Fogo (25.3); (k) DT típica 15/17/18/19/21 (22.3); (l) PH de 16.2 (3–6 jogadores × 3 degraus); (m) Progressão = 26.2 linha a linha; (n) cobertura: todo campo das fichas 29.8 e 29.9 tem célula em `ficha_mapa.json` | 0 diferenças; cobertura 100% |
| `oraculo` | `oraculo_ficha.py` calcula ~45 saídas por caso (atributos, bônus, PV, Defesa, Esquiva, RD, VEL, tetos, Eficiência/Eficácia, Especialização, 18 Perícias, 6 TR, Morrendo, DT, AB, Habilidades, Ultimate, PH, Bênçãos/slots, Cone, Relíquias, Conjuntos, inventário, Memoespírito, avisos esperados). Matriz 7 Raças × 9 Caminhos × níveis {1, 20} (126 casos, escolhas determinísticas por semente); varredura 1→20 em 3 combinações (Humano/Destruição; Xianzhouíta/Recordação com Memoespírito; Intellitron/Caça com Olho de Lan e Pesada); casos-limite: Humano +1/+1 e +1/+1 no mesmo atributo (aviso), atributo > 15 após Raça e aumentos até 20 e além (aviso), Recordação completa, nível 20 tudo no máximo (Cone 5 + Sobreposições, Tier IV, Conjuntos, 4 Ressonâncias), Perícias escolhidas a mais, Habilidades a mais e de Nível acima do máximo, Bênção de tier acima do slot, Bênção repetida, Eficácia sem Eficiência, Esquiva com Pesada | ZERO divergências |
| `extremos` | Calcula TODAS as células com fórmula em: ficha em branco; só nome; só Raça; só Caminho; um campo por vez; entradas inválidas (texto em número, nível 0/21/"abc", atributo 3 e 25, Bênção de outro Caminho colada, jogadores 0) | 0 valores de erro (`#N/A #VALUE! #REF! #DIV/0! #NAME? #NUM!`); inválidos geram aviso PT-BR na coluna certa; ficha em branco sem aviso falso de erro grave |
| `lint` | Varre TODA fórmula de célula, validação e formatação condicional com `openpyxl.formula.Tokenizer`: funções na lista efetiva, sem `;` fora de string, sem proibidas, sem `[`, CF/validação personalizada sem `!`, fonte só Arial, sem proteção, sem nome definido, sem caixa de seleção, abas sem emoji, `fullCalcOnLoad` | 0 achados |
| `texto` | Extrai o texto visível (valores literais, literais de string dentro das fórmulas, mensagens de validação, nomes de aba; nunca nomes de função): (1) as 25 strings proibidas de `scripts\checar-nomenclatura.ps1`, mesma regra `\b…\b` sem caixa, + termos aposentados da tabela 30.2; (2) termos oficiais do glossário 30.1 grafados exatamente (ex.: "Ação Complementar", "Teste de Resistência", "Memoespírito", "Esfera Planar"); (3) ortografia: toda palavra deve existir no léxico montado com as palavras de todos os `.md` do livro + `ficha_lexico_extra.txt`; palavra fora do léxico = achado; (4) acentuação: lista de pares sem acento proibidos (Criacao, Progressao, Pericia, Bencao, Eficiencia, Eficacia, Nivel, Habilidade sem acento etc.) | 0 achados |
| `preview` | `renderizar_ficha.py` desenha cada aba (larguras, alturas, mesclas, preenchimento, bordas, fonte, valores calculados pelo `formulas`) em PNG em `.agents\tasks\ficha-preview\` para 3 estados: em branco, Nadir nível 1, personagem nível 20 completo; detecta texto que não cabe na célula (mede com `ImageFont.truetype("arial.ttf")`) e confere que **Em Jogo** cabe em 1360 × 768 px | PNGs gerados; 0 textos cortados; Em Jogo dentro da tela; o executor abre e olha cada PNG e registra no relatório |

---

# Implementation Plan

- [ ] 1. Spike de compatibilidade e utilitários de base.
      Criar `testar_ficha.py` com o esqueleto de suítes e a suíte `spike` (workbook temporário em `%TEMP%`, apagado no fim), e `gerar_ficha.py` com: constantes de estilo (2.1), helpers `entrada()`, `calculada()`, `aviso()`, `titulo()`, `legenda()`, registro de mapa lógico → célula, e criação das 10 abas vazias com legenda. Decide acento nos nomes de aba e grava `ficha_funcoes_ok.json`. Suíte `protegidos`: na primeira execução grava `R\build\ficha_protegidos.json` com o SHA-256 de todo arquivo de `livro-v1.0\`, dos `.docx`/`.pdf` V1.0, de `gerar_docx.py` e `gerar_pdf.py`; nas seguintes, compara (entra em `tudo`).
      Files: `R\build\testar_ficha.py`, `R\build\gerar_ficha.py`
      Verify: `testar_ficha.py --suite spike` sai 0 e imprime a lista efetiva; `gerar_ficha.py` cria o `.xlsx` com as 10 abas e `testar_ficha.py --suite lint` sai 0.

- [ ] 2. Camada de dados e aba Dados.
      `ficha_dados.py`: parser de tabela markdown + extratores por capítulo (lista da decisão 3, inclusive as 108 Bênçãos com tier, requisito e resumo de uma linha) e o módulo transcrito com âncoras (frequência/acúmulo das Bênçãos, efeitos automáticos da decisão 2, textos dos traços raciais). `gerar_ficha.py` escreve a aba Dados em blocos com título e fonte. Suíte `dados` com parser próprio do teste.
      Files: `R\build\ficha_dados.py`, `R\build\gerar_ficha.py`, `R\build\testar_ficha.py`
      Verify: gerar e rodar `--suite dados` → 0 diferenças, 108 Bênçãos (12 por Caminho: 6/4/2 por tier); `--suite lint` 0.

- [ ] 3. Oráculo independente.
      `oraculo_ficha.py` com constantes próprias citando seção, função `calcular(entradas) -> saídas` cobrindo o inventário 1.1–1.8 e os avisos esperados. Teste interno do oráculo contra os números de ouro (suíte `ouro` em modo `--so-oraculo`), sem planilha ainda.
      Files: `R\build\oraculo_ficha.py`, `R\build\testar_ficha.py`
      Verify: `--suite ouro --so-oraculo` → todos os números de ouro de (a)–(m) batem.

- [ ] 4. Abas Criação e Progressão (depende de 1–2).
      Criação com os 12 passos (2.2), validação do array e da Compra, bônus racial com listas dependentes, aumentos vindos da Progressão, as cinco estatísticas; Progressão com tabela mestra, aumentos, Ressonâncias e "próximo nível". Grava todas as células no mapa.
      Files: `R\build\gerar_ficha.py`
      Verify: gerar; `--suite lint` 0; `--suite extremos` (já roda sobre o que existe) 0 erros; `--suite ouro` itens (a) atributos/PV/Defesa/Esquiva/VEL, (c), (d), (m) batem.

- [ ] 5. Abas Testes e Caminho (depende de 4).
      Testes: 18 Perícias e 6 TR com Eficiência, Eficácia, penalidade Pesada, Vantagem racial, Morrendo. Caminho: ficha, recurso próprio, 10 slots de Bênção com lista dependente e avisos, catálogo, Memoespírito completo.
      Files: `R\build\gerar_ficha.py`
      Verify: gerar; `--suite lint` 0; `--suite extremos` 0 erros; `--suite ouro` (a) Perícias/DT/Pacto, (b), (e), (k) batem.

- [ ] 6. Abas Equipamento e Habilidades (depende de 4–5).
      Equipamento: arma secundária, Cone com Sobreposição, Relíquias por Tier, Conjuntos A/B/C, inventário, Créditos. Habilidades: 8 linhas + Ultimate + Ressonância III.
      Files: `R\build\gerar_ficha.py`
      Verify: gerar; `--suite lint` 0; `--suite extremos` 0 erros; `--suite ouro` (a) AB/Rebarba/Ultimate/Espaço, (f), (h), (i), (j), (l) batem.

- [ ] 7. Abas Em Jogo, Regras Rápidas e Início (depende de 4–6).
      Em Jogo no layout de 2.2 (Resumo para o Mestre, recursos, calculadora, ações, testes, condições e usos), condições aplicadas (decisão 1), Bênçãos aplicadas (decisão 2) com tetos; Regras Rápidas; Início com guia e painel de avisos.
      Files: `R\build\gerar_ficha.py`
      Verify: gerar; `--suite lint` 0; `--suite extremos` 0 erros; `--suite ouro` completo (inclui (n) cobertura) 0 diferenças.

- [ ] 8. Teste diferencial completo e estados extremos (depende de 3 e 7).
      Ligar o oráculo à planilha: matriz 126 casos, 3 varreduras 1→20, casos-limite; ampliar `extremos` para todos os estados inválidos. Corrigir `gerar_ficha.py` (ou o oráculo, quando o erro for dele, citando a seção) até zerar.
      Files: `R\build\testar_ficha.py`, `R\build\gerar_ficha.py`, `R\build\oraculo_ficha.py`
      Verify: `--suite oraculo` → 0 divergências; `--suite extremos` → 0 erros e avisos onde esperado (timeout de 1800 s).

- [ ] 9. Auditoria de texto e inspeção visual (depende de 7).
      Suíte `texto` (proibidas, glossário, ortografia por léxico, acentuação) e `renderizar_ficha.py` + suíte `preview`. Corrigir textos e larguras até zerar; olhar cada PNG.
      Files: `R\build\testar_ficha.py`, `R\build\renderizar_ficha.py`, `R\build\ficha_lexico_extra.txt`, `R\build\gerar_ficha.py`
      Verify: `--suite texto` 0 achados; `--suite preview` gera os PNGs em `.agents\tasks\ficha-preview\`, 0 textos cortados, Em Jogo dentro de 1360 × 768.

- [ ] 10. Relatório de auditoria e rodada final.
      Escrever `relatorio-auditoria-ficha.md` (PT-BR): o que foi verificado, resultado de cada suíte (números), divergências D1–D7 + novas, decisões da seção 3, limitações (o `formulas` não é o Google: recomenda abrir no Google uma vez e conferir o painel de avisos), como regenerar. Apagar temporários.
      Files: `R\.agents\tasks\relatorio-auditoria-ficha.md`
      Verify: `--suite tudo` sai 0 (inclui `protegidos`: nenhum hash do livro, dos `.docx`/`.pdf` V1.0, de `gerar_docx.py` ou `gerar_pdf.py` mudou); o `.xlsx` existe na raiz.
