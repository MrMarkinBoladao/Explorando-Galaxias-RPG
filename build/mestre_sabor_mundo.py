# -*- coding: utf-8 -*-
"""
mestre_sabor_mundo.py — tabelas de sabor da Fase 3 (abas Mundos e Improviso; design §6.13, §6.14, §6.16).

Texto original em PT-BR, sem nome de personagem do jogo (suíte sabor), no tom de 27.12–27.18 (facções que são um Caminho
levado a sério, lugares com uma condição e uma cena). Nada aqui é regra: os sorteios são uniformes e o peso é repetir a
entrada (H11). As três perguntas de 27.17 (qual Caminho vence, o que se faz de manhã, o que pararam de fazer) viram três
listas. Entra na aba Tabelas pelos blocos "mundos" e "improviso" (mestre_sabor.tabelas()).
"""

FONTE = "Sugestão da planilha (H11)"

LUGAR_A = ["Porto", "Vale", "Anel", "Doca", "Mirante", "Cidadela", "Vigia", "Colônia", "Abrigo", "Farol", "Ponte",
           "Cais", "Poço", "Pátio", "Torre", "Jardim", "Muralha", "Estaleiro", "Feira", "Arco", "Planalto", "Cratera",
           "Recife", "Ilha", "Bastião", "Santuário", "Refúgio", "Passagem", "Fenda", "Represa"]
LUGAR_B = ["de Cinza", "das Marés Lentas", "do Sol Partido", "de Ferrugem", "das Sete Luas", "do Último Aviso",
           "de Vidro Negro", "dos Ventos Mansos", "da Neve Quente", "do Eco Longo", "das Lanternas", "de Sal",
           "do Relógio Torto", "das Velas Apagadas", "da Maré Alta", "do Silêncio Verde", "de Âmbar", "dos Mineiros",
           "da Segunda Chance", "do Norte Frio", "das Correntes", "de Cobre Velho", "da Aurora Curta", "do Poente Duplo",
           "dos Sinos", "da Chuva Fina", "do Fundo", "das Asas", "de Pedra Viva", "da Última Rota"]
NAVE_A = ["Andorinha", "Teimosa", "Velha Senhora", "Promessa", "Agulha", "Mariposa", "Coruja", "Lâmpada", "Errante",
          "Fiel", "Garça", "Vaga-lume", "Bigorna", "Sereia", "Caravela", "Raposa", "Âncora", "Cometa", "Viúva", "Pérola",
          "Gaivota", "Formiga", "Baleia", "Faísca", "Sentinela", "Peregrina", "Boa Sorte", "Cigarra", "Lua Torta",
          "Corvo"]
NAVE_B = ["de Vidro", "do Último Aviso", "das Estrelas Frias", "Sem Rota", "de Sete Portos", "do Amanhecer", "da Maré",
          "de Ferro Velho", "Que Não Dorme", "de Ninguém", "do Norte", "das Cinzas", "Dourada", "Azul", "de Prata",
          "Silenciosa", "Que Volta", "do Vale", "Remendada", "da Sorte", "do Abismo", "de Papel", "Insistente",
          "Noturna", "do Farol", "de Bronze", "Distante", "da Neblina", "de Graça", "Sem Pressa"]
FACCAO_A = ["Irmandade", "Liga", "Conselho", "Coro", "Ordem", "Círculo", "Companhia", "Guilda", "Assembleia",
            "Confraria", "Sindicato", "Clã", "Casa", "Escola", "Frente", "Cooperativa", "Vigília", "Rede",
            "Congregação", "Corte", "Legado", "Tribunal", "Família", "Junta", "Coletivo", "Mesa", "Fraternidade",
            "Sociedade", "Comuna", "Guarda"]
FACCAO_B = ["da Chama Fria", "do Sétimo Portão", "dos Relógios Quebrados", "da Maré Quieta", "do Olho Aberto",
            "das Mãos Limpas", "do Último Verso", "da Estrela Cega", "dos Que Lembram", "do Vazio Manso", "da Ferrugem",
            "do Lacre", "da Ponte Partida", "dos Faróis", "da Semente Negra", "do Silêncio", "da Promessa Antiga",
            "dos Trilhos", "da Lâmina Gentil", "do Céu Baixo", "das Cem Portas", "do Inverno Longo", "da Brasa",
            "dos Nomes Riscados", "da Primeira Luz", "do Poço Fundo", "das Asas de Cobre", "da Cinza Branca",
            "do Juramento", "da Rota Perdida"]
ORGANIZACAO = [
    "Sindicato dos Estivadores do Anel", "Cooperativa dos Pilotos Sem Rota", "Coral do Bairro Baixo",
    "Arquivo Livre das Docas", "Clube de Corrida de Sucata", "Associação dos Mineiros Aposentados",
    "Hospital de Caridade da Estação", "Casa de Penhores do Mercado Velho", "Escola de Navegação Estelar",
    "Companhia de Teatro Itinerante", "Grêmio dos Relojoeiros", "Liga dos Contrabandistas Honestos",
    "Agência de Correio Interestelar", "Fundação de Restauro de Autômatos", "Círculo dos Observadores do Céu",
    "Guarda de Bairro Voluntária", "Casa de Apostas do Anel Externo", "Oficina Comunitária de Próteses",
    "Jornal Clandestino da Colônia", "Cartório de Rotas e Licenças", "Irmandade dos Faroleiros",
    "Mutirão de Reconstrução", "Leilão de Achados Orbitais", "Clínica Sem Perguntas",
    "Associação de Herdeiros de Naves", "Escritório de Cobrança Educada", "Coletivo de Cozinheiros de Estação",
    "Sociedade dos Mapas Proibidos", "Comitê de Boas-Vindas do Porto", "Escola de Esgrima da Ponte"]
ORG_OFERECE = [
    "abrigo por uma noite, sem perguntas", "uma rota segura até a próxima estação", "documentos novos em dois dias",
    "informação sobre quem chegou ontem", "reparos baratos e rápidos", "uma escolta de dois veteranos",
    "acesso ao arquivo antigo", "um contato dentro da Corporação", "comida quente e um lugar para conversar",
    "crédito para uma compra urgente", "um mapa dos dutos de serviço", "tratamento médico discreto",
    "um palco e uma plateia", "um advogado que conhece a cláusula", "peças que não se acham em loja",
    "a palavra de alguém respeitado", "transporte de carga sem registro", "uma testemunha para um acordo",
    "treino para quem não sabe lutar", "um esconderijo para um objeto perigoso"]
ORG_COBRA = [
    "um favor, cobrado depois", "que o grupo entregue uma carta sem abrir", "uma parte do que o grupo achar",
    "silêncio sobre o que viu lá dentro", "presença numa reunião de votação",
    "que o grupo vigie um armazém por uma noite", "o nome de quem mandou o grupo", "trabalho braçal por um dia",
    "um objeto que pertenceu a alguém do grupo", "que ninguém da Corporação saiba", "lealdade numa disputa de bairro",
    "que o grupo leve um aprendiz junto", "créditos adiantados, sem recibo", "uma história verdadeira, contada em público",
    "que o grupo devolva algo roubado há anos", "uma visita ao túmulo de um fundador", "que o grupo vote contra alguém",
    "um retrato tirado na frente da sede", "o fim de uma rivalidade antiga", "que o grupo não volte nunca mais"]
MUNDO_TIPO = [
    "mundo-oceano com ilhas flutuantes", "lua de gelo com cidades subterrâneas", "planeta-deserto de vidro",
    "mundo-floresta com árvores do tamanho de torres", "asteroide minerador escavado por dentro",
    "planeta de crepúsculo eterno", "mundo-cidade coberto de prédios", "lua vulcânica com colônias em cúpulas",
    "planeta de pântanos luminosos", "mundo de tempestades permanentes", "planeta com anéis e vilas nos anéis",
    "mundo agrícola de planícies sem fim", "lua morta com ruínas antigas", "planeta-jardim cuidado por máquinas",
    "mundo de cânions profundos", "planeta de chuva ácida e torres seladas", "mundo gelado com um único mar quente",
    "estação construída sobre o casco de uma nave morta", "planeta de montanhas que se movem devagar",
    "lua-santuário de peregrinos", "mundo de areia que canta com o vento", "planeta de noites de três dias"]
MUNDO_CONDICAO = [
    "a gravidade fica mais leve ao meio-dia", "o céu tem duas auroras de cores diferentes",
    "ninguém fala alto depois do pôr do sol", "a água potável é dividida por sorteio", "o vento traz vozes de muito longe",
    "as sombras chegam um pouco depois dos corpos", "metade da população dorme durante o dia",
    "a comunicação com fora cai toda tarde", "a poeira brilha no escuro", "as estações do ano duram uma semana",
    "chove para cima uma vez por mês", "o ar tem cheiro de metal quente", "os sinos tocam sozinhos antes de uma tempestade",
    "a noite é clara como o dia", "o mar recua quilômetros toda madrugada", "as plantas se viram para quem passa",
    "os relógios atrasam uma hora por dia", "há um eco que responde com outras palavras", "a neve é morna",
    "toda porta tem duas fechaduras, por lei", "o horizonte parece perto demais", "a luz do sol chega azulada",
    "as pedras mudam de lugar durante a noite", "o chão treme de leve o tempo todo",
    "o céu fica sem estrelas uma noite por semana", "a fumaça das fábricas desenha formas no céu",
    "os rios mudam de curso a cada estação", "o ar rarefeito obriga a usar máscara",
    "o barulho do mar se ouve mesmo longe dele", "a cor do céu anuncia o humor do dia"]
MANHA = [
    "fazem fila na bomba de água", "acendem lanternas nas janelas", "rezam em voz baixa voltados para o céu",
    "consertam as redes de pesca", "trocam notícias na feira", "levam as crianças até a escola do abrigo",
    "varrem a poeira das calçadas", "conferem o painel de radiação", "esperam o trem de carga",
    "cantam na troca de turno da mina", "regam as estufas", "leem os avisos da Corporação no mural",
    "alimentam os animais de carga", "abrem as comportas das docas", "fazem pão em fornos comunitários",
    "limpam os filtros de ar", "marcam no muro os dias sem acidente", "medem a altura da maré",
    "treinam com espadas de madeira na praça", "trocam o turno de vigia", "levam flores a um memorial",
    "compram peças usadas no mercado", "testam os trajes de vedação", "carregam caixas para o porto",
    "dão corda nos relógios da torre", "recolhem os painéis solares", "conversam com os autômatos de rua",
    "jogam cartas antes do expediente", "acendem fogueiras contra o frio", "escutam o boletim da rádio local"]
PARARAM = [
    "pescar no lago", "olhar para o céu", "dizer o nome da cidade antiga", "enterrar os mortos",
    "abrir a porta para estranhos", "cantar no trabalho", "usar a estrada do norte", "mandar cartas",
    "acender luzes à noite", "ir ao templo", "consertar as máquinas velhas", "comemorar aniversários",
    "confiar na rádio", "beber a água do poço", "descer para os níveis de baixo", "ensinar a história do lugar",
    "vender para forasteiros", "sonhar, ou dizem que pararam", "perguntar pelos desaparecidos",
    "plantar no campo leste", "usar a moeda local", "rir em público", "dormir sem vigia", "visitar o farol", "votar",
    "construir casas novas", "chamar o médico", "olhar nos espelhos", "tocar os sinos", "esperar o trem"]
# H11: "Nenhuma" aparece 3 vezes (peso), como o "Nenhum" do Caminho do NPC
AMEACA = [
    "Um Stellaron dormindo no núcleo", "Um Stellaron recém-cravado, que ninguém viu chegar",
    "Rumores de um Stellaron sob a cidade", "Um culto que diz guardar um Stellaron",
    "Caçadores de Stellaron de passagem, discretos", "Um Stellaron que já começou a reescrever as estações do ano",
    "Uma facção que oferece um Stellaron a quem pagar mais", "Um Stellaron que só se nota pelos sonhos dos moradores",
    "Um Stellaron que a Corporação jura não existir",
    "Fragmentum nos dutos antigos", "Fragmentum na água de um poço", "Uma mina fechada por causa do Fragmentum",
    "Fragmentum avançando devagar pelo deserto", "Uma vila esvaziada pelo Fragmentum",
    "Gente que voltou do Fragmentum e não fala", "Fragmentum preso atrás de um lacre que range",
    "Fragmentum vendido em frascos como remédio",
    "Nenhuma: o lugar está em paz, por enquanto", "Nenhuma: o lugar está em paz, por enquanto",
    "Nenhuma: o lugar está em paz, por enquanto"]
ESTACAO_FUNCAO = [
    "triagem, alfândega, armazém, tribunal e hotel no mesmo cilindro, como Vértice-9 (27.17)",
    "estaleiro de reparos de cargueiros", "hospital orbital", "posto de reabastecimento",
    "observatório de tempestades solares", "prisão de segurança média", "mercado livre de impostos",
    "laboratório de pesquisa da Corporação", "entreposto de minério", "estação de retransmissão de rádio",
    "santuário de peregrinos", "escola de pilotagem", "fazenda de estufas", "depósito de naves desativadas",
    "hotel para tripulações em trânsito", "base de quarentena", "arquivo de registros de rota",
    "fábrica de trajes de vedação", "posto avançado de exploração", "cassino de passagem"]
ESTACAO_PROBLEMA = [
    "o sistema de ar está falhando num anel inteiro", "uma greve parou as docas", "um passageiro sumiu do registro",
    "a Corporação mandou uma auditoria surpresa", "um surto de doença na ala de carga",
    "o diretor desapareceu há três dias", "contrabandistas tomaram um setor", "a gravidade artificial falha à noite",
    "uma nave bateu no atracadouro", "os autômatos de manutenção pararam de obedecer",
    "falta comida para a próxima semana", "uma facção exige a entrega de um refugiado",
    "o reator está mais quente do que deveria", "alguém sabota os elevadores", "uma tempestade solar está chegando",
    "o Fragmentum apareceu num duto de serviço", "dois chefes de turno disputam o comando",
    "a rádio só transmite estática e uma voz", "os registros de carga não fecham",
    "um Tolo Mascarado anunciou um espetáculo"]
NAVE_CLASSE = [
    "cargueiro pesado", "rebocador de asteroides", "transporte de passageiros", "corveta de patrulha",
    "nave de pesquisa", "iate de luxo antigo", "barcaça de minério", "nave-hospital", "batedor rápido", "nave-correio",
    "draga de detritos orbitais", "nave-fábrica", "transporte de colonos", "nave de resgate", "cargueiro refrigerado",
    "veleiro solar", "nave-escola", "caçador de sucata", "nave de mudança de uma família inteira",
    "fragata aposentada que virou loja"]
NAVE_PECULIARIDADE = [
    "a gravidade muda de lado no corredor central", "o computador de bordo só responde em verso",
    "tem um jardim no porão de carga", "a tripulação nunca desliga a música", "um compartimento está soldado há anos",
    "o capitão dorme na ponte de comando", "as luzes piscam quando alguém levanta a voz",
    "carrega um gato que ninguém trouxe", "a porta da enfermaria abre sozinha", "o motor faz um barulho de choro",
    "há um assento vazio que ninguém usa", "a nave já mudou de nome três vezes",
    "tem um mapa pintado no teto do refeitório", "as paredes estão cobertas de assinaturas",
    "o reator foi trocado por um de outra nave", "o banheiro tem a melhor vista da galáxia",
    "a tripulação vota toda decisão", "metade dos painéis está em outra língua", "o casco tem marcas de garras",
    "a nave cheira a canela", "existe um tripulante que só aparece à noite",
    "o piloto automático evita uma rota sem explicação", "o porão tem uma cela",
    "a comida é toda em lata, de um único sabor", "há uma estufa de flores no convés",
    "a nave transmite sem querer um sinal antigo", "o relógio de bordo marca outra data",
    "um autômato antigo faz a limpeza e fala sozinho", "a antena foi feita com uma escada",
    "a nave nunca pousou em planeta nenhum"]
FACCAO_QUER = [
    "controlar a única rota segura da região", "apagar um registro antigo", "proteger um segredo de família",
    "provar que uma profecia é falsa", "comprar uma estação inteira", "vingar uma colônia destruída",
    "libertar autômatos de uma última ordem", "reunir os pedaços de um Cone de Luz famoso",
    "manter a paz entre duas vilas", "derrubar um governador corrupto", "encontrar o fundador desaparecido",
    "fechar um poço tomado pelo Fragmentum", "guardar um Stellaron longe de todos", "transformar um planeta num museu",
    "ensinar todos a ler os mapas antigos", "acabar com a fome numa lua", "levar o Expresso Astral até a sua estação",
    "calar uma rádio que diz a verdade", "abrir uma escola em cada porto", "voltar para casa, onde quer que seja"]
FACCAO_METODO = [
    "contratos com letras miúdas", "sabotagem silenciosa", "doações generosas com condições", "chantagem educada",
    "espetáculos públicos", "milícias de bairro", "subornos de pequenos funcionários", "boatos plantados nas feiras",
    "alianças por casamento", "greves organizadas", "pesquisa científica", "pregação de porta em porta",
    "falsificação de documentos", "proteção paga", "infiltração em cargos baixos", "duelos formais",
    "leilões viciados", "rádio clandestina", "favores que nunca cobram na hora", "mapas falsos vendidos a rivais"]
FACCAO_RECURSO = [
    "uma frota de cargueiros velhos", "um arquivo que ninguém mais tem", "um médico que salva qualquer um",
    "acesso às docas de uma estação", "uma fortuna escondida num asteroide", "um exército pequeno e leal",
    "um Intellitron que lembra de tudo", "terras férteis numa lua seca", "uma rede de informantes nas feiras",
    "um estaleiro clandestino", "o apoio de uma família antiga", "um farol que guia as naves",
    "um tribunal que decide a favor deles", "uma mina de minério raro", "um contrato assinado pela Corporação",
    "uma relíquia de outra era", "a confiança dos mineiros", "um teatro inteiro", "uma rota secreta pelos anéis",
    "um refúgio que ninguém acha"]
FACCAO_USO = [
    "eles pedem ajuda antes de pedir obediência: ofereça o pedido na primeira cena",
    "mande um representante educado; o conflito começa quando o grupo recusa",
    "eles cumprem a palavra: use uma promessa deles como relógio",
    "coloque-os do lado certo de uma causa errada",
    "eles oferecem exatamente o que o grupo precisa, cedo demais",
    "use-os como testemunhas: eles sempre viram alguma coisa",
    "faça da primeira cena com eles uma conversa, não um combate",
    "eles sabem o nome de um personagem antes de ele se apresentar",
    "mostre o que eles constroem antes de mostrar o que destroem",
    "deixe o grupo dever um favor a eles bem cedo", "eles mudam de lado quando o grupo muda de ideia",
    "use um membro jovem que discorda dos líderes", "eles chegam depois do problema, sempre com uma explicação",
    "mostre um lugar que eles salvaram e um que eles arruinaram",
    "faça-os negociar com outra facção na frente do grupo", "eles cobram juros em favores, não em créditos",
    "use a sede deles como lugar seguro, até não ser mais", "eles respeitam quem os enfrenta de frente",
    "comece por um boato sobre eles e confirme na sessão seguinte",
    "eles têm um rival dentro de casa: o grupo pode escolher quem ajudar"]
RUMOR = [
    "dizem que o diretor da estação vendeu o reator reserva",
    "contam que um Tolo Mascarado comprou todos os ingressos do teatro", "o novo médico do porto nunca dorme",
    "uma nave sem nome atracou no anel externo à meia-noite", "alguém está pagando o dobro por mapas antigos",
    "a Legião mandou um ultimato para uma vila vizinha", "o lacre da mina velha foi aberto por dentro",
    "a Corporação vai fechar o mercado na semana que vem",
    "há um Caçador de Stellaron hospedado na pensão da doca", "os autômatos de limpeza estão desenhando no chão",
    "o poço da praça voltou a dar água, e a água é morna", "um ex-soldado da Legião procura os antigos colegas",
    "o Expresso Astral foi visto parado numa estação que não existe", "a filha do prefeito fugiu com um piloto",
    "o arquivo da cidade pegou fogo, menos uma prateleira", "a rádio pirata vai revelar um nome hoje à noite",
    "os mineiros acharam uma porta no fundo do túnel", "o chefe da guarda deve dinheiro a todo mundo",
    "um Intellitron se recusa a desligar e pede asilo", "a festa da colheita foi cancelada sem explicação",
    "um cargueiro voltou com a tripulação inteira, mas mais jovem",
    "os Cavaleiros da Beleza abriram uma clínica gratuita", "alguém compra cabelo e dentes no mercado velho",
    "a estrada do norte está livre pela primeira vez em anos", "uma criança desenha a mesma estrela todos os dias",
    "o banco do porto não abre há três dias", "o sino do templo tocou sozinho às três da manhã",
    "um contrabandista vende água de outro planeta",
    "um general aposentado está escrevendo as memórias e citando nomes",
    "dizem que o Fragmentum sobe pelos canos quando chove",
    "uma nave da Frota de Jade procura alguém com uma cicatriz no queixo", "o casamento de amanhã é uma armadilha",
    "o cozinheiro da estação já foi capitão de guerra",
    "a Corporação ofereceu seguro de vida a todos os moradores, de graça",
    "um farol apagado voltou a piscar uma mensagem",
    "alguém viu um personagem do grupo num lugar onde ele nunca esteve",
    "as lojas estão sem trajes de vedação, todas ao mesmo tempo",
    "o Culto da Inexistência deixou uma flor em cada porta", "um velho jura que conhece a cura para o Fragmentum",
    "a melhor pilota da doca perdeu uma aposta e agora deve um favor perigoso"]
VERACIDADE = ["Verdadeiro", "Meia-verdade", "Falso"]                       # H11: 1/1/1
EVENTO_VIAGEM = [
    "o trem atrasa e a próxima conexão já partiu", "um passageiro passa mal e pede ajuda",
    "a rota é desviada por um campo de detritos", "um controle de documentos surpresa no meio do caminho",
    "o combustível acaba antes do previsto", "uma tempestade obriga a parar numa vila desconhecida",
    "um vendedor ambulante oferece um mapa curioso", "a bagagem de um personagem foi trocada",
    "um pedido de socorro numa frequência antiga", "o piloto contratado some na escala",
    "uma ponte caiu e o desvio custa um dia", "alguém da tripulação reconhece um personagem",
    "o motor faz um barulho novo", "um animal de carga se recusa a seguir",
    "uma patrulha pede para revistar a carga", "a comida estraga na metade da viagem",
    "um mapa antigo mostra um atalho que não deveria existir",
    "um carona oferece pagar a passagem com uma história", "o rádio capta uma conversa que não deveria",
    "um fiscal cobra uma taxa que ninguém conhece",
    "a estrada está cheia de refugiados indo na direção contrária",
    "uma criança aparece escondida no porão de carga", "a escala é numa estação em quarentena",
    "um passageiro tenta vender um objeto roubado", "a navegação aponta para o lugar errado",
    "o vagão-refeitório do Expresso fecha por causa de uma briga", "uma luz estranha acompanha a nave por horas",
    "um carteiro pede que o grupo leve uma carta urgente", "a passagem de volta foi cancelada",
    "um velho conhecido embarca na mesma viagem"]
EVENTO_ESPACO = [
    "um campo de asteroides fora do mapa", "uma nave à deriva sem sinal de vida",
    "uma tempestade solar obriga a desligar os sistemas", "um pedido de atracação de uma nave da Corporação",
    "o casco é atingido por um pequeno meteoro", "um farol de navegação transmite uma rota falsa",
    "catadores de sucata cercam a nave e pedem pedágio", "uma estação abandonada aparece onde não havia nada",
    "o sensor detecta um sinal fraco de Stellaron", "uma cápsula de fuga com alguém dormindo dentro",
    "a gravidade de um planeta próximo puxa a rota", "uma frota da Legião passa em formação",
    "um sinal de socorro gravado há décadas", "falha no suprimento de ar de um compartimento",
    "uma nave da Frota de Jade pede identificação", "o reator dá sinais de superaquecimento",
    "um cardume de criaturas do vácuo cruza a rota", "uma baliza de quarentena avisa para não seguir",
    "outro trem parece correr em trilhos paralelos", "um satélite antigo responde ao chamado da nave",
    "destroços de uma batalha recente bloqueiam a passagem", "a comunicação com a estação cai no pior momento",
    "uma luz pisca em código numa lua sem colônia", "uma nave-cidade pede ajuda para um resgate",
    "a nave recebe uma mensagem endereçada a um personagem",
    "um rombo no casco de uma nave vizinha espalha carga pelo vácuo", "o piloto automático muda a rota sozinho",
    "um rebocador oferece ajuda por um preço alto",
    "uma nuvem de poeira estelar apaga as estrelas por uma hora",
    "um dron de vigilância segue a nave sem se identificar"]
EVENTO_CIDADE = [
    "um tumulto no mercado bloqueia a rua principal", "a guarda fecha um bairro para uma busca",
    "uma procissão atravessa o caminho do grupo", "um batedor de carteiras leva algo importante",
    "um prédio desaba e há gente presa", "um leilão público de bens confiscados",
    "uma briga de taverna envolve alguém conhecido", "a energia cai em metade da cidade",
    "um pregador acusa o grupo em praça pública", "uma criança perdida segue o grupo",
    "um festival fecha as ruas com fogos", "um incêndio começa numa fábrica de tecidos",
    "um mensageiro entrega um convite anônimo", "um cobrador procura alguém com o nome de um personagem",
    "os sinos tocam o alarme sem motivo aparente", "uma greve para o transporte público",
    "um comerciante oferece um negócio bom demais", "um autômato de rua começa a seguir o grupo",
    "o grupo é confundido com outra equipe", "uma eleição local divide a vizinhança",
    "um julgamento público acontece na praça", "a rádio local fala do grupo",
    "um vendedor reconhece um item do grupo como roubado", "chega uma notícia de guerra numa lua vizinha",
    "um duelo formal está marcado para o meio-dia", "um hospital pede doadores com urgência",
    "uma inundação nos níveis de baixo", "um teatro anuncia uma peça sobre o grupo",
    "a polícia da Corporação cobra uma taxa nova", "um velho amigo pede abrigo por uma noite"]
# 02 e 27.1: a falha cobra "tempo, ruído, recurso, informação incompleta, uma complicação nova" — os 5 abrem a lista
CUSTO_FALHA_LIVRO = ["tempo", "ruído", "recurso", "informação incompleta", "uma complicação nova"]
CUSTO_FALHA = [
    "custa tempo: a cena leva o dobro e o prazo aperta", "faz ruído: alguém ouviu e vem ver",
    "gasta um recurso: uma poção, um kit ou créditos", "dá só informação incompleta: falta a parte mais importante",
    "traz uma complicação nova: mais alguém se envolve", "custa um favor a um NPC",
    "deixa um rastro que pode ser seguido", "deixa o personagem exausto: ele chega por último à próxima cena",
    "irrita um aliado", "o equipamento quebra e precisa de conserto",
    "dá certo, mas atrai a atenção de uma facção", "dá certo, mas outra pessoa leva o crédito",
    "dá certo pela metade, e é preciso voltar depois", "o grupo perde a surpresa na próxima cena",
    "a porta abre, mas fica aberta para os outros também", "dá certo, mas em troca de uma promessa",
    "a pista leva a um lugar mais perigoso", "o tempo extra deixa o adversário se preparar",
    "o objeto chega danificado", "a testemunha muda de versão"]
ITEM_RARO = [
    "um mapa estelar gravado em osso", "uma bússola que aponta para o Stellaron mais próximo",
    "um traje de vedação de outra era", "uma caixa de música dos Halovianos",
    "um frasco de água de um mundo que não existe mais", "uma lâmina de jade com uma inscrição apagada",
    "um diário de bordo antigo do Expresso Astral", "uma prótese antiga que ainda se mexe sozinha",
    "um selo da Corporação em branco", "um pedaço de casco de uma nave lendária",
    "uma semente de árvore de um planeta-jardim", "uma máscara de Tolo usada em cena",
    "um cristal que guarda uma voz", "um chip de memória de um Intellitron", "o cachimbo de um capitão aposentado",
    "o sino do templo de uma nave-cidade", "uma carta de baralho com o rosto de um personagem",
    "um relógio que marca a hora de outro planeta", "uma medalha da Legião partida ao meio",
    "uma lanterna que só acende perto do Fragmentum"]
# H10: d20 + modificador → resposta; a 2ª coluna é o teto de cada faixa (a última vale para o resto)
ORACULO = ["Não, e…", "Não", "Não, mas…", "Sim, mas…", "Sim", "Sim, e…"]
ORACULO_ATE = [3, 7, 10, 13, 17, "acima"]


def tabelas(_t):
    """As tabelas de sabor da Fase 3, com o construtor `_t` de mestre_sabor (mesmo formato da Fase 2)."""
    return [
        _t("lugar_a", "Nome de lugar (início)", LUGAR_A, 30, "mundos"),
        _t("lugar_b", "Nome de lugar (fim)", LUGAR_B, 30, "mundos"),
        _t("nave_a", "Nome de nave (início)", NAVE_A, 30, "mundos"),
        _t("nave_b", "Nome de nave (fim)", NAVE_B, 30, "mundos"),
        _t("faccao_a", "Nome de facção (início)", FACCAO_A, 30, "mundos"),
        _t("faccao_b", "Nome de facção (fim)", FACCAO_B, 30, "mundos"),
        _t("organizacao", "Organização", ORGANIZACAO, 30, "mundos"),
        _t("org_oferece", "Organização: o que oferece", ORG_OFERECE, 20, "mundos"),
        _t("org_cobra", "Organização: o que cobra", ORG_COBRA, 20, "mundos"),
        _t("mundo_tipo", "Tipo de mundo", MUNDO_TIPO, 20, "mundos"),
        _t("mundo_condicao", "Condição marcante", MUNDO_CONDICAO, 30, "mundos"),
        _t("manha", "O que fazem de manhã (27.17)", MANHA, 30, "mundos", fonte="Livro 27.17 (pergunta) + " + FONTE),
        _t("pararam", "O que pararam de fazer (27.17)", PARARAM, 30, "mundos",
           fonte="Livro 27.17 (pergunta) + " + FONTE),
        _t("ameaca", "Presença: Stellaron ou Fragmentum (peso)", AMEACA, 20, "mundos",
           fonte="Livro 27.13 e 27.14 + Sugestão da planilha (H11: Nenhuma ×3)", pesos=True),
        _t("estacao_funcao", "Função da estação", ESTACAO_FUNCAO, 20, "mundos",
           fonte="Livro 27.17 (a primeira) + " + FONTE),
        _t("estacao_problema", "Problema da estação", ESTACAO_PROBLEMA, 20, "mundos"),
        _t("nave_classe", "Classe da nave", NAVE_CLASSE, 20, "mundos"),
        _t("nave_peculiaridade", "Peculiaridade da nave", NAVE_PECULIARIDADE, 30, "mundos"),
        _t("faccao_quer", "Facção: o que quer", FACCAO_QUER, 20, "mundos"),
        _t("faccao_metodo", "Facção: método", FACCAO_METODO, 20, "mundos"),
        _t("faccao_recurso", "Facção: recurso", FACCAO_RECURSO, 20, "mundos"),
        _t("faccao_uso", "Facção: como usar", FACCAO_USO, 20, "mundos", fonte="Sugestão da planilha (H11), no tom de "
                                                                              "27.16"),
        _t("rumor", "Rumor", RUMOR, 40, "improviso"),
        _t("veracidade", "Veracidade do rumor (peso)", VERACIDADE, 3, "improviso", pesos=True),
        _t("evento_viagem", "Evento de viagem", EVENTO_VIAGEM, 30, "improviso"),
        _t("evento_espaco", "Evento no espaço", EVENTO_ESPACO, 30, "improviso"),
        _t("evento_cidade", "Evento na cidade", EVENTO_CIDADE, 30, "improviso"),
        _t("custo_falha", "Falhe para frente: o custo", CUSTO_FALHA, 20, "improviso",
           fonte="Livro 02 e 27.1 (os 5 custos) + " + FONTE),
        _t("item_raro", "Item fora do comum (loja)", ITEM_RARO, 20, "improviso"),
        _t("oraculo", "Oráculo: resposta", ORACULO, 6, "improviso", fonte="Sugestão da planilha (H10)", pesos=True,
           segunda=("Oráculo: até (d20 + modificador)", ORACULO_ATE)),
    ]
