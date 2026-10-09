# -*- coding: utf-8 -*-
"""
mestre_sabor.py — tabelas de sabor dos geradores da Fase 2 (NPC, aventura, recompensa; design §6.16, §4.2).

Texto ORIGINAL escrito para a planilha, PT-BR, sem nome de personagem do jogo. Cada tabela tem id (tab.<id> na aba
Tabelas), título, fonte ("Sugestão da planilha (H11)" ou a seção do livro quando as primeiras entradas vêm dele) e
valores. Onde a lista começa com texto do livro (prazos de 27.7, gatilhos de 25.2, efeitos de 4 peças de 25.3), as
primeiras entradas são as do livro, na ordem do livro (a suíte dados confere contra o .md).
Tabelas de duas colunas (objetivo por tipo de aventura, motivação por Caminho) usam a mesma convenção da lista
"ambiente por facção" da Fase 1: a 1ª coluna é a chave, a 2ª o valor; o Mestre acrescenta linhas nas vagas vazias.

TABELAS: lista de dicionários {id, titulo, fonte, valores, minimo, sem_ortografia, pesos, segunda, bloco}.
"""

import mestre_sabor_nomes as NM

FONTE_SUG = "Sugestão da planilha (H11)"

OCUPACAO = [
    "piloto de cargueiro", "mecânico de doca", "despachante de carga", "médico de bordo",
    "comerciante de peças usadas", "contrabandista aposentado", "arquivista da Frota de Jade", "cozinheiro de estação",
    "guarda de alfândega", "minerador de asteroide", "cartógrafo de rotas", "tradutor de dialetos",
    "jornalista independente", "sacerdote de um Aeon esquecido", "engenheiro de suporte de vida",
    "dono de bar no anel externo", "caçador de recompensas novato", "professor de história estelar", "agiota da doca",
    "técnico de comunicações", "apostador profissional", "artesão de próteses", "colecionador de antiguidades falsas",
    "mensageiro", "guia turístico", "segurança particular", "botânico de estufa orbital", "operador de guindaste",
    "fiscal da Corporação", "músico de rua", "ladrão de dados", "corretor de seguros", "enfermeiro de campanha",
    "pescador de um mundo oceânico", "alfaiate de trajes de vácuo", "relojoeiro", "advogado de porto", "ex-soldado",
    "inventor fracassado", "vendedor de mapas estelares", "zelador de templo", "astrônomo amador",
    "tratador de animais de carga", "informante",
]

APARENCIA = [
    "cicatriz que atravessa a sobrancelha", "olhos de cores diferentes", "tatuagem de rota estelar no pescoço",
    "mãos manchadas de graxa", "cabelo trançado com fios de cobre", "prótese de braço antiga e barulhenta",
    "sardas por todo o rosto", "casaco grande demais", "anéis em todos os dedos", "óculos remendados com fita",
    "dentes de metal", "pele queimada pelo sol de outro mundo", "sempre de luvas", "cheiro forte de óleo de motor",
    "postura militar impecável", "roupas caras e gastas", "um olho artificial que brilha fraco",
    "cabelo raspado de um lado", "marcas antigas de Fragmentum nos braços", "colar de dentes de criatura",
    "uniforme de uma empresa que faliu", "chapéu de aba larga", "unhas pintadas de dourado",
    "cabelos brancos muito cedo", "sorriso com um dente faltando", "maquiagem de palco borrada",
    "lenço que cobre metade do rosto", "pulseira de identificação de prisioneiro", "muito alto e curvado",
    "baixo e largo como uma porta", "fios de luz tecidos no cabelo", "botas de mineiro gastas",
    "medalha militar presa do lado errado",
]

PERSONALIDADE = [
    "desconfiado, mas leal quando conquistado", "fala demais quando está nervoso",
    "gentil com crianças e ríspido com adultos", "orgulhoso e fácil de ofender", "calmo até a primeira mentira",
    "curioso a ponto de se meter em perigo", "pessimista que sempre ajuda mesmo assim", "brincalhão que esconde o medo",
    "metódico, anota tudo", "generoso com o dinheiro dos outros", "ansioso, sempre olhando o relógio",
    "cínico com a Corporação", "romântico incurável", "vaidoso e inseguro", "direto, sem paciência para rodeios",
    "supersticioso com números", "rancoroso, mas justo", "otimista teimoso",
    "tímido que se solta depois do segundo copo", "competitivo em tudo", "melancólico, vive no passado",
    "protetor com quem considera família", "preguiçoso, mas brilhante", "pragmático: tudo tem preço",
    "devoto e tolerante", "sarcástico com quem manda", "ingênuo, acredita em quase tudo", "paranoico com escutas",
    "educado demais para dizer não", "impulsivo, decide e depois pensa",
]

MOTIVACAO = [
    "pagar uma dívida antes que a cobrança chegue", "encontrar um irmão desaparecido",
    "sair desta estação para sempre", "provar que não é covarde", "proteger o negócio da família",
    "juntar dinheiro para uma prótese melhor", "limpar o próprio nome", "ver o mar de verdade uma vez na vida",
    "esquecer alguém", "ser lembrado por algo bom", "vingar um amigo", "subir na hierarquia",
    "manter um segredo enterrado", "curar uma doença que ninguém sabe nomear", "voltar para casa",
    "descobrir quem o abandonou", "conseguir uma passagem no Expresso Astral", "terminar a obra de um mestre morto",
    "ficar rico depressa", "manter a filha longe da guerra", "recuperar um objeto roubado",
    "ganhar o respeito do pai", "fugir de um contrato", "entender um sonho que se repete", "ter uma noite de paz",
    "expor uma injustiça", "salvar um bairro da demolição", "reconquistar um amor perdido",
    "sobreviver a mais um ciclo de trabalho", "abrir a própria oficina",
]

# 27.12: "Toda facção deste capítulo é um Caminho levado a sério" — 5 motivações por Caminho (06.3)
MOTIVACAO_CAMINHO = {
    "A Destruição": ["derrubar algo velho que já devia ter caído", "testar os próprios limites numa luta de verdade",
                     "acabar com uma fonte de sofrimento, custe o que custar", "romper a corrente que prende a sua gente",
                     "ver arder o lugar onde sofreu"],
    "A Inexistência": ["descobrir se alguma coisa ainda vale a pena", "desaparecer sem deixar dívida",
                       "aceitar uma perda que ainda dói", "encontrar silêncio num mundo barulhento",
                       "provar que nada é para sempre"],
    "A Harmonia": ["unir dois grupos que se odeiam", "manter a paz na vizinhança", "reunir a família espalhada",
                   "fazer uma festa que todos lembrem", "achar um lugar onde todos caibam"],
    "A Abundância": ["curar quem ninguém mais quer curar", "manter alguém vivo a qualquer preço",
                     "plantar algo que dure séculos", "devolver a saúde a um mundo doente",
                     "encontrar o remédio que salvou e condenou a sua gente"],
    "A Recordação": ["guardar a memória de quem morreu", "recuperar uma lembrança apagada",
                     "escrever a história verdadeira de um lugar", "encontrar a fotografia que prova o passado",
                     "impedir que um nome seja esquecido"],
    "A Erudição": ["resolver um enigma que ninguém resolveu", "entender como um Stellaron funciona",
                   "ler um arquivo proibido", "construir uma máquina que pense melhor do que ele",
                   "vencer uma discussão com um gênio"],
    "A Euforia": ["rir na cara do perigo outra vez", "transformar uma tragédia em espetáculo",
                  "sentir o coração disparar mais uma vez", "pregar a maior peça da galáxia",
                  "viver cada noite como se fosse a última"],
    "A Caça": ["acertar as contas com um alvo antigo", "rastrear quem destruiu a sua casa",
               "pegar o maior predador do setor", "cumprir um contrato que ninguém aceitou",
               "proteger os seus, caçando antes de ser caçado"],
    "A Preservação": ["manter uma muralha de pé mais um dia", "proteger uma colônia esquecida",
                      "cumprir uma promessa feita a um morto", "guardar a porta que não pode abrir",
                      "construir um abrigo para quem não tem nenhum"],
}

SEGREDO = [
    "trabalha em segredo para a Corporação", "deve dinheiro a um Tolo Mascarado", "já foi soldado da Legião",
    "carrega um fragmento de Stellaron sem saber", "matou alguém e nunca contou", "não é quem diz ser",
    "tem uma família em outro mundo", "roubou o próprio patrão", "foi tocado de leve pelo Fragmentum",
    "sabe onde está um carregamento desaparecido", "é informante dos Caçadores de Stellaron",
    "foi curado pelos Cavaleiros da Beleza e voltou diferente", "vende informação para os dois lados",
    "tem medo de máquinas, mas trabalha com elas", "é procurado pela Frota de Jade", "ainda ouve a voz de um morto",
    "falsificou a própria idade", "perdeu a memória de um ano inteiro", "esconde um Intellitron foragido",
    "ama alguém do lado inimigo", "sabotou a nave que trouxe o grupo", "é herdeiro de uma fortuna que não quer",
    "assinou uma apólice sobre a própria vida", "já viu o Expresso Astral antes", "não sabe ler e disfarça",
    "planeja fugir esta noite", "guarda um mapa que leva a uma ruína", "fez um acordo com um Devoto do Silêncio",
    "tem uma doença que piora com o frio", "é a única testemunha de um crime",
]

MANEIRISMO = [
    "fala baixo e obriga todos a se aproximarem", "termina toda frase com uma pergunta", "assobia quando mente",
    "conta dinheiro enquanto conversa", "cita provérbios inventados", "ri antes de dar uma má notícia",
    "nunca olha nos olhos", "estala os dedos quando pensa", "chama todo mundo de chefe",
    "fala de si na terceira pessoa", "repete a última palavra de quem falou", "gagueja diante de quem tem patente",
    "canta baixinho sem perceber", "mexe num amuleto o tempo todo", "fala depressa e engole sílabas",
    "usa gírias de uma estação distante", "pede desculpas o tempo inteiro", "faz uma pausa longa antes de responder",
    "voz grave e lenta como um sino", "risada alta e contagiante", "conversa com as próprias máquinas",
    "corrige a gramática dos outros", "estala a língua quando discorda", "está sempre mastigando alguma coisa",
    "coça a cicatriz quando fica nervoso", "fala em números e estatísticas",
    "sussurra nomes como se alguém escutasse", "usa títulos formais com todo mundo",
    "conta histórias que nunca terminam", "aponta com o queixo",
]

ATITUDE = ["Hostil", "Desconfiado", "Indiferente", "Cordial", "Prestativo"]

GANCHO_NPC = [
    "pede ajuda para tirar alguém de uma cela da Corporação", "oferece pagamento adiantado por uma escolta curta",
    "jura ter visto um dos personagens num lugar onde ele nunca esteve",
    "precisa entregar um pacote que não pode ser aberto", "quer que o grupo recupere uma carga roubada pela Legião",
    "vende um mapa que parece verdadeiro demais", "pede que o grupo finja ser a sua família por uma noite",
    "tem uma dívida que só o grupo pode quitar", "conhece um atalho pelos dutos abandonados",
    "procura um médico que não faça perguntas", "quer comprar um objeto que o grupo carrega",
    "pede proteção contra alguém que não quer nomear", "promete uma informação em troca de um favor",
    "foi testemunha de algo e agora é caçado", "precisa de alguém para ganhar uma aposta",
    "desafia um dos personagens para um duelo de honra", "quer sair do planeta escondido na bagagem do grupo",
    "traz um recado de alguém do passado de um personagem", "pede que o grupo investigue um sumiço no bairro",
    "oferece trabalho numa mina que ninguém mais aceita", "precisa de ajuda para enterrar um amigo com dignidade",
    "quer que o grupo devolva algo que ele mesmo roubou", "sabe quem está seguindo o grupo",
    "propõe sociedade num negócio arriscado", "pede ao grupo que apague um registro da Corporação",
    "está sendo chantageado e não sabe por quem", "quer conhecer o Expresso Astral por dentro",
    "tem uma máquina que só funciona perto de um dos personagens",
    "procura alguém para cuidar de uma criança por um dia", "conta um rumor sobre um Stellaron perto dali",
]

# H11: "Nenhum" 3 vezes — o resto da galáxia não segue Caminho com afinco (27.12)
CAMINHO_NPC = ["A Destruição", "A Inexistência", "A Harmonia", "A Abundância", "A Recordação", "A Erudição",
               "A Euforia", "A Caça", "A Preservação", "Nenhum", "Nenhum", "Nenhum"]

TIPO_AVENTURA = ["Resgate", "Escolta", "Investigação", "Infiltração", "Defesa de posição", "Caçada", "Entrega",
                 "Sabotagem", "Negociação", "Exploração", "Fuga", "Contenção de Fragmentum", "Rastro de Stellaron",
                 "Cobrança de dívida"]

OBJETIVO = {
    "Resgate": ["tirar um refém de uma cela antes da transferência",
                "encontrar e trazer de volta uma equipe de mineiros presa",
                "libertar um Intellitron leiloado como peça de reposição"],
    "Escolta": ["levar um informante até a nave que o espera", "proteger uma caravana de suprimentos até a colônia",
                "acompanhar um diplomata por um bairro hostil"],
    "Investigação": ["descobrir quem sabotou o suporte de vida",
                     "achar a origem de um sinal que repete nomes de mortos", "provar que um acidente não foi acidente"],
    "Infiltração": ["entrar num arquivo da Corporação e copiar um contrato",
                    "atravessar um baile de máscaras sem ser reconhecido",
                    "colocar um rastreador na nave de um contrabandista"],
    "Defesa de posição": ["segurar uma ponte até a evacuação terminar", "manter um gerador funcionando durante o cerco",
                          "proteger um hospital de campanha por uma noite"],
    "Caçada": ["rastrear uma criatura do Fragmentum até o ninho", "capturar vivo um desertor da Legião",
               "encontrar o Autômato que foge pelos dutos"],
    "Entrega": ["levar um pacote lacrado sem abrir nem perguntar",
                "entregar remédios antes que a colônia feche os portões",
                "fazer chegar uma carta a alguém que não quer ser achado"],
    "Sabotagem": ["desligar a forja que alimenta um batalhão", "apagar os registros de uma apólice",
                  "danificar um transmissor sem deixar rastro"],
    "Negociação": ["convencer dois clãs a dividir um poço de água", "comprar tempo com a Legião antes do ultimato",
                   "fechar um acordo com um Tolo Mascarado sem ser enganado"],
    "Exploração": ["mapear uma estação abandonada", "chegar ao fundo de uma ruína antes dos saqueadores",
                   "descobrir o que existe atrás de uma porta que ninguém abriu"],
    "Fuga": ["sair do planeta antes do bloqueio", "escapar de uma prisão orbital com os outros detentos",
             "atravessar a cidade com caçadores no encalço"],
    "Contenção de Fragmentum": ["fechar um lacre que começou a ceder",
                                "isolar um bairro antes que o Fragmentum se espalhe",
                                "queimar o ninho sem derrubar a mina inteira"],
    "Rastro de Stellaron": ["seguir as anomalias até a fonte", "recuperar um fragmento antes dos Caçadores",
                            "descobrir por que as estações do ano trocam em horas"],
    "Cobrança de dívida": ["cobrar um devedor que fugiu para outro mundo", "recuperar a garantia de um empréstimo",
                           "decidir se a dívida de um velho amigo vale uma briga"],
}

GANCHO = [
    "Uma nave de resgate pede socorro na frequência do grupo, e a voz é de um dos personagens",
    "Um cargueiro chega ao porto com a carga trocada por pedras", "A luz de uma estação inteira se apaga de madrugada",
    "Um mensageiro morre na porta do grupo com um endereço na mão",
    "Uma criança entrega um desenho do Expresso Astral com uma data futura",
    "O mercado amanhece fechado e ninguém diz por quê", "Um contrato aparece assinado com o nome de um personagem",
    "Um velho mapa ganha uma rota nova durante a noite", "A Corporação congela a conta de um aliado do grupo",
    "Um sino toca numa colônia que não tem sino", "Um minerador sai da mina falando uma língua que não existe",
    "Uma festa de casamento é interrompida por um alarme de lacre",
    "Três desconhecidos pedem a mesma informação ao grupo no mesmo dia", "Um transporte de prisioneiros desvia de rota",
    "As máquinas de uma oficina começam a construir algo sozinhas",
    "O informante de sempre não aparece no encontro marcado",
    "Um navio-hospital pede abrigo e não deixa ninguém subir a bordo", "Um bairro inteiro sonha o mesmo sonho",
    "Uma moeda antiga aparece no troco de todo mundo",
    "O rádio da nave capta uma transmissão de vinte anos atrás",
    "Um soldado da Legião bate à porta pedindo para desertar", "A água da estação fica com gosto de ferro",
    "Um artista convida o grupo para uma estreia que ainda não tem palco",
    "O dono do bar oferece bebida de graça em troca de um favor estranho",
    "Um animal de carga segue o grupo e não vai embora",
    "Um diário é encontrado num duto com o nome do grupo na última página",
    "Um tremor abre uma passagem sob a praça", "Uma apólice de seguro vence amanhã, e o segurado sumiu",
    "Um retrato do grupo aparece pendurado numa galeria",
    "Uma estação pede ajuda e, quando o grupo chega, diz que ninguém pediu",
]

LOCAL = [
    "um mercado flutuante preso a um asteroide", "uma estufa orbital com plantas que cantam",
    "um cemitério de naves no anel externo", "uma vila de mineiros escavada no gelo",
    "um hotel de luxo numa estação em quarentena", "um arquivo subterrâneo cheio de goteiras",
    "uma torre de comunicação abandonada", "uma feira de trocas num deserto de vidro",
    "um templo dedicado a um Aeon esquecido", "uma refinaria que nunca desliga",
    "um porto clandestino escondido numa lua", "um bairro construído dentro de um navio encalhado",
    "um laboratório lacrado há cem anos", "um trem de carga que dá a volta num planeta",
    "uma prisão com uma fuga recente", "um teatro de marionetes mecânicas", "uma fazenda de algas num oceano raso",
    "um observatório numa montanha sem ar", "uma cidade-mercado sobre pernas de ferro",
    "um hospital de campanha num vale nevado", "um depósito de sucata que vende de tudo",
    "uma estação de pesquisa sem tripulação", "o palácio de festas de uma família falida",
    "uma ponte de mil quilômetros entre duas colônias", "um mosteiro silencioso de Intellitrons",
    "uma doca seca cheia de naves inacabadas", "um bairro de refugiados ao redor de um farol",
    "uma mina de cristal que canta com o vento", "uma biblioteca itinerante a bordo de um cargueiro",
    "um parque de diversões fechado numa lua de gelo",
]

COMPLICACAO = [
    "o contato do grupo foi preso ontem", "a rota mais curta está bloqueada por um desabamento",
    "outra equipe foi contratada para o mesmo serviço", "o pagamento chega numa moeda que ninguém aceita",
    "um personagem é reconhecido por um velho inimigo", "a gravidade do lugar muda a cada hora",
    "o lugar está em quarentena", "o equipamento do grupo fica retido na alfândega",
    "um aliado exige ir junto e só atrapalha", "a Legião declara toque de recolher",
    "uma tempestade de poeira corta a comunicação", "o alvo está protegido por uma apólice da Corporação",
    "a ponte de acesso desaba no meio do caminho", "um Tolo Mascarado decide transformar a missão em espetáculo",
    "a energia da estação falha nos piores momentos", "o grupo precisa voltar antes da troca de guarda",
    "um inocente fica preso no meio da confusão", "o contratante muda as condições pela metade",
    "uma criatura do Fragmentum aparece onde não devia", "os moradores não querem ajuda e dizem isso com pedras",
    "o mapa está duas décadas desatualizado", "um dos acessos só abre com a senha de um morto",
    "a carga é mais pesada do que disseram", "o grupo é seguido desde o porto",
    "a nave do grupo precisa de conserto urgente", "o idioma do lugar mudou desde o último contato",
    "um dos personagens adoece no caminho", "o lugar marcado para o encontro pega fogo", "o alvo tem um gêmeo",
    "a Frota de Jade emite uma ordem de inspeção",
]

REVIRAVOLTA = [
    "o contratante é o verdadeiro culpado", "a vítima não quer ser salva",
    "o antagonista está tentando impedir algo pior", "a carga é uma pessoa",
    "o informante trabalha para os dois lados", "o lugar já foi a casa de um dos personagens",
    "a ameaça foi criada por quem pediu ajuda", "o refém é um impostor", "o prazo era falso: já passou",
    "o tesouro é uma lembrança, não um objeto", "o inimigo derrotado era só um disfarce",
    "a missão era um teste de recrutamento", "o mapa leva ao Expresso Astral de outra época",
    "dois grupos rivais querem a mesma coisa por motivos opostos", "a criatura protege os filhotes",
    "o aliado de confiança vendeu o grupo há semanas", "o objeto procurado está dentro de alguém",
    "a colônia inteira sabia e se calou", "o contrato da Corporação tem uma cláusula que prende o grupo",
    "o morto não está morto", "o sinal de socorro foi enviado pelo próprio antagonista",
    "a porta trancada protegia o lado de fora", "alguém atrasou o grupo de propósito",
    "a recompensa prometida não existe", "o antagonista conhece o Propósito de Vida de um personagem",
    "o verdadeiro alvo era a nave do grupo", "o lacre foi aberto para salvar alguém",
    "a facção inimiga oferece uma trégua sincera", "uma testemunha muda de lado no último minuto",
    "o Stellaron não é a causa, é a consequência",
]

# 27.7: "Ponha relógio na ficção: a nave parte ao amanhecer, o lacre não aguenta mais um dia, a escolta chega em
# seis horas" — os 3 abrem a lista, na ordem do livro
PRAZO_LIVRO = ["a nave parte ao amanhecer", "o lacre não aguenta mais um dia", "a escolta chega em seis horas"]
PRAZO = PRAZO_LIVRO + [
    "o leilão termina à meia-noite", "a maré de radiação volta em dois dias", "o julgamento é amanhã cedo",
    "o oxigênio da estação dura três turnos de trabalho", "o ultimato vence em três dias",
    "a janela de lançamento fecha ao pôr do sol", "a carga estraga em quarenta horas",
    "o refém será transferido na próxima troca de guarda", "a ponte será demolida no fim da semana",
    "o eclipse dura só uma hora", "a festa acaba quando a música parar", "a tempestade chega antes do jantar",
    "o contrato expira no fim do mês", "o reator esfria em doze horas", "a frota parte no próximo salto",
    "a testemunha embarca hoje à noite", "o sinal se apaga em seis dias", "o inverno fecha as estradas em uma semana",
]

PISTA = [
    "um recibo com o carimbo de uma doca que não existe mais", "pegadas que entram numa parede",
    "um nome riscado numa lista de passageiros", "cheiro de ozônio onde não há máquina nenhuma",
    "uma gravação com dois segundos apagados", "uma chave com o símbolo da Corporação",
    "um cartucho da Legião com a data de amanhã", "um bilhete escrito numa língua antiga de Xianzhou",
    "marcas de garra do lado de dentro de uma porta", "um copo ainda quente numa sala vazia",
    "uma conta paga em nome de um morto", "um desenho infantil com o rosto do antagonista",
    "uma lista de compras com remédios proibidos", "terra de outro planeta na sola de uma bota",
    "um anel de noivado num ninho do Fragmentum", "um mapa com uma rota marcada a sangue",
    "um aviso de despejo de um prédio já demolido", "um ingresso de teatro para uma peça que nunca estreou",
    "um rastro de óleo que leva aos dutos", "uma testemunha que descreve o mesmo homem com três rostos",
    "um selo de lacre quebrado por dentro", "uma frequência de rádio anotada num guardanapo",
]

BUGIGANGA = [
    "uma bússola que aponta para o último lugar onde você dormiu", "um relógio parado nas três e quinze",
    "uma moeda com duas caras", "uma caixinha de música que toca uma canção desconhecida",
    "um dado de osso com seis em todas as faces", "um mapa dobrado de uma cidade que não existe",
    "um frasco com areia de um planeta morto", "um broche da Corporação de uma filial fechada",
    "uma pena luminosa de uma ave extinta", "uma passagem do Expresso Astral, sem data",
    "uma chave sem fechadura conhecida", "um par de óculos que mostra tudo em preto e branco",
    "um boneco de pano com um bolso secreto", "um pedaço de casco com um nome gravado",
    "uma carta de baralho com o rosto de um personagem", "uma semente que não germina em lugar nenhum",
    "um cachimbo que nunca apaga", "um anel de lata com uma promessa gravada por dentro",
    "um livro com todas as páginas em branco menos a última", "um cristal que esquenta ao luar",
    "uma fotografia de uma família desconhecida", "um apito que só os Autômatos escutam",
    "um selo postal de um mundo extinto", "uma colher dobrada em forma de estrela",
    "um lenço bordado com um brasão de Xianzhou", "um medalhão vazio",
    "um fone de ouvido que capta uma rádio distante", "um vidro de perfume quase vazio",
    "um ingresso rasgado de um circo", "uma pedra lisa que flutua um dedo acima da mão",
    "um pião de metal que gira por horas", "uma luva de criança", "um crachá de visitante do Vértice-9",
    "um parafuso de ouro", "um pote de tinta que muda de cor", "um mapa estelar bordado num pano",
    "uma faca de cozinha com cabo de coral", "um tabuleiro de xadrez com uma peça a mais",
    "uma etiqueta de bagagem de uma viagem que ninguém lembra", "uma concha que guarda o som de outro mar",
    "um caderno de receitas de um cozinheiro famoso", "uma fita de cabelo com um nó que não desata",
    "uma ampulheta que corre para cima", "um sino pequeno sem badalo",
    "um retrato a lápis de um Intellitron sorrindo", "uma garrafa com uma mensagem ilegível",
    "um cartão de visita de um detetive aposentado", "uma flor seca de uma estufa orbital",
    "um botão de farda da Legião", "um carimbo de alfândega com o nome do grupo", "um amuleto de cauda de raposa",
]

CONE_NOME_A = [
    "O Último Trem", "A Última Carta", "O Farol", "Um Sonho", "A Canção", "O Relógio Parado", "A Ponte", "O Jardim",
    "Uma Noite", "O Retrato", "A Promessa", "O Mapa Rasgado", "A Lanterna", "O Silêncio", "A Viagem",
    "O Primeiro Passo", "Uma Janela", "A Chuva", "O Eco", "A Fogueira", "O Navio", "A Despedida", "O Brinde",
    "A Sombra", "O Espelho", "Uma Estrela", "O Vento", "A Porta", "O Livro", "A Dança", "O Juramento",
]

CONE_NOME_B = [
    "Para Casa", "Que Ninguém Leu", "Sobre o Mar", "Antes do Fim", "em Outro Mundo", "da Estação Vazia",
    "Que Volta Sempre", "Depois da Guerra", "Entre as Estrelas", "ao Amanhecer", "Que Não Apagou", "de Quem Ficou",
    "Sem Volta", "no Fim do Corredor", "do Último Inverno", "Que Prometemos", "Sob a Chuva", "de um Velho Amigo",
    "Para Ninguém", "no Céu Errado", "Que Esperou", "Além do Lacre", "do Primeiro Dia", "Sem Nome", "em Silêncio",
    "Que o Tempo Esqueceu", "de Mil Noites", "por um Instante", "Contra o Vento", "Até Logo",
]

CONE_MEMORIA = [
    "a última viagem de um maquinista que nunca chegou", "o primeiro dia de aula numa colônia que já não existe",
    "um casamento interrompido por um alarme", "a vigília de um faroleiro durante uma tempestade de cem anos",
    "o último jantar de uma família antes da evacuação", "a vitória de um time de várzea num mundo esquecido",
    "a despedida de dois irmãos num porto lotado",
    "a noite em que uma cidade inteira apagou as luzes para ver as estrelas",
    "o perdão que um soldado nunca pediu", "um concerto tocado para uma plateia vazia",
    "a fuga de uma criança pelos dutos de uma estação", "a promessa de voltar feita por alguém que não voltou",
    "o último voo de uma piloto que salvou um comboio", "o silêncio de um mosteiro na manhã de um ataque",
    "a colheita de uma estufa orbital antes do inverno", "a carta que um prisioneiro escreveu e nunca enviou",
    "a primeira vez que um Intellitron sonhou", "o riso de um palhaço num hospital de campanha",
    "uma dança numa nave-cidade durante um cerco", "o mapa desenhado por uma exploradora perdida",
    "a canção de ninar de uma mãe num navio afundando", "o momento em que um juiz decidiu não condenar",
    "a reconstrução de uma ponte por mãos voluntárias", "o último dia de um mercado antes da demolição",
    "o encontro de dois inimigos que dividiram um abrigo", "a travessia de um deserto por uma caravana sem água",
    "o dia em que um farol voltou a acender", "um beijo trocado sob uma chuva de meteoros",
    "a última aula de um professor que perdeu a voz",
    "a noite em que uma colônia inteira cantou para não ter medo",
    "o sacrifício de uma tripulação para fechar um lacre",
]

# 25.2 — os seis exemplos de gatilho do livro abrem a lista, na ordem do livro
CONE_GATILHO_LIVRO = ["quando você usa a Ultimate", "quando você Quebra um inimigo", "no primeiro Ciclo do combate",
                      "quando um aliado cai a Morrendo", "quando você acerta um alvo que já está Marcado",
                      "quando você gasta o último PH do grupo"]
CONE_GATILHO = CONE_GATILHO_LIVRO + [
    "quando você termina o turno sem ter sido atingido", "quando você cura um aliado", "quando um inimigo erra você",
    "quando você é o último a agir no Ciclo", "quando você derrota um inimigo",
    "quando você recebe dano acima da metade dos PV", "quando você usa uma Habilidade de Nível 3 ou mais",
    "quando você age antes de todos os inimigos", "quando você aplica uma condição",
    "quando você Avança um aliado na Fila", "quando a sua Energia chega a 100",
    "quando você fica abaixo da metade dos PV", "quando o grupo revela uma Fraqueza",
    "quando um aliado é Congelado",
]

CONJUNTO_NOME = [
    "Vigília do Farol Afogado", "Rastro da Caravana Perdida", "Ossos da Lua-Forja", "Sinos da Cidade Submersa",
    "Véus do Teatro Queimado", "Engrenagens do Relojoeiro Cego", "Espinhos do Jardim Fechado",
    "Pegadas do Último Mineiro", "Brasões da Frota Esquecida", "Correntes da Prisão Orbital",
    "Pétalas do Ateliê Branco", "Lanternas do Cais Noturno", "Escamas da Maré Funda", "Fios da Tecelã Ausente",
    "Moedas do Mercador Sem Rosto", "Chaves do Cofre Vazio", "Penas do Coro Distante", "Pedras do Templo Sem Deus",
    "Agulhas da Bússola Torta", "Selos do Arquivo Proibido",
]

CONJUNTO_ORIGEM = [
    "de um mesmo lugar: um farol que afundou com o vigia dentro",
    "de uma mesma catástrofe: a queda de uma lua-forja",
    "de um mesmo morto ilustre: um general que se recusou a marchar",
    "de uma cidade engolida pelo Fragmentum numa única noite", "de um teatro que pegou fogo na noite de estreia",
    "da frota que desapareceu no primeiro salto", "de um jardim fechado depois de uma praga",
    "de um relojoeiro que parou o tempo da própria loja", "da última caravana de um clã errante",
    "de um mosteiro de Intellitrons desligado à força", "de um navio-hospital abandonado em órbita",
    "de uma prisão orbital que libertou todos de uma vez", "de um mercado que vendia memórias",
    "do ateliê de um escultor que desapareceu", "de uma estação de pesquisa que estudou um Stellaron de perto",
    "de uma família nobre de Xianzhou que caiu em desgraça",
    "de uma equipe de mineiros soterrados que nunca foi resgatada",
    "de uma biblioteca que queimou durante uma revolta", "de um coral que cantou até a última nota de um cerco",
    "de um caçador que perseguiu a mesma presa por cinquenta anos",
]

# 25.3 — os dois exemplos de 4 peças do livro abrem a lista, na ordem do livro
CONJUNTO_4_LIVRO = ["ao Quebrar um inimigo, o seu próximo ataque ganha +1 dado",
                    "ao usar a Ultimate, o grupo recebe +1 de Defesa por 1 Ciclo"]
CONJUNTO_4 = CONJUNTO_4_LIVRO + [
    "ao derrotar um inimigo, você recebe +1 de Velocidade até o fim do Ciclo",
    "ao curar um aliado, ele recebe +1 de Defesa por 1 Ciclo",
    "ao aplicar uma condição, o seu próximo Teste de Ataque ganha +1",
    "ao revelar uma Fraqueza, o grupo ganha +1 no próximo Teste de Ataque contra aquele inimigo",
    "ao Avançar um aliado, o seu próximo ataque causa +2 de dano",
    "ao ficar abaixo da metade dos PV, você recebe +1 RD por 1 Ciclo",
    "ao agir primeiro no Ciclo, o seu primeiro ataque causa +2 de dano",
    "ao acertar um alvo Marcado, você recebe +1 de Velocidade por 1 Ciclo",
    "ao curar um aliado, o alvo recebe +1 nos Testes de Resistência por 1 Ciclo",
    "ao derrotar um inimigo, o aliado mais próximo recebe +1 de Defesa por 1 Ciclo",
]


def _t(id_, titulo, valores, minimo, bloco, fonte=FONTE_SUG, sem_ortografia=False, pesos=False, segunda=None):
    return {"id": id_, "titulo": titulo, "fonte": fonte, "valores": list(valores), "minimo": minimo, "bloco": bloco,
            "sem_ortografia": sem_ortografia, "pesos": pesos, "segunda": segunda}


def _pares(d):
    chaves, vals = [], []
    for k, vs in d.items():
        for v in vs:
            chaves.append(k)
            vals.append(v)
    return chaves, vals


def tabelas():
    """As tabelas da Fase 2, na ordem dos blocos da aba Tabelas."""
    T = []
    for c in NM.CULTURAS:
        T.append(_t(f"nome.{NM.SLUG[c]}", f"Nome — {c}", NM.NOMES[c], 30, "nomes",
                    fonte=f"Sugestão da planilha (estilo de 05, {c})", sem_ortografia=True))
    for c in NM.CULTURAS:
        T.append(_t(f"sobrenome.{NM.SLUG[c]}", f"Sobrenome — {c}", NM.SOBRENOMES[c], 30, "sobrenomes",
                    fonte=f"Sugestão da planilha (estilo de 05, {c})", sem_ortografia=True))
    T += [
        _t("ocupacao", "Ocupação (NPC)", OCUPACAO, 40, "npc"),
        _t("aparencia_traco", "Traço de aparência", APARENCIA, 30, "npc"),
        _t("personalidade", "Personalidade", PERSONALIDADE, 30, "npc"),
        _t("motivacao", "Motivação (sem Caminho)", MOTIVACAO, 30, "npc"),
        _t("segredo", "Segredo", SEGREDO, 30, "npc"),
        _t("maneirismo", "Maneirismo e voz", MANEIRISMO, 30, "npc"),
        _t("caminho_npc", "Caminho do NPC (peso)", CAMINHO_NPC, 12, "npc",
           fonte="Livro 06.3 + Sugestão da planilha (H11: Nenhum ×3, 27.12)", pesos=True),
        _t("atitude", "Atitude com o grupo", ATITUDE, 5, "npc"),
        _t("gancho_npc", "Gancho do NPC", GANCHO_NPC, 30, "npc"),
    ]
    ck, cv = _pares(MOTIVACAO_CAMINHO)
    ok_, ov = _pares(OBJETIVO)
    T += [
        _t("motivacao_caminho", "Caminho (motivação)", ck, 45, "aventura", pesos=True,
           segunda=("Motivação por Caminho", cv)),
        _t("objetivo", "Tipo (objetivo)", ok_, 36, "aventura", pesos=True, segunda=("Objetivo por tipo", ov)),
        _t("tipo_aventura", "Tipo de aventura", TIPO_AVENTURA, 12, "aventura"),
        _t("gancho", "Gancho de aventura", GANCHO, 30, "aventura"),
        _t("local", "Local (sabor)", LOCAL, 30, "aventura"),
        _t("complicacao", "Complicação", COMPLICACAO, 30, "aventura"),
        _t("reviravolta", "Reviravolta", REVIRAVOLTA, 30, "aventura"),
        _t("prazo", "Prazo ou risco", PRAZO, 20, "aventura",
           fonte="Livro 27.7 (3 primeiras) + Sugestão da planilha (H11)"),
    ]
    T += [
        _t("pista", "Pista", PISTA, 20, "recompensa"),
        _t("bugiganga", "Bugiganga", BUGIGANGA, 50, "recompensa"),
        _t("cone_nome_a", "Nome do Cone (início)", CONE_NOME_A, 30, "recompensa"),
        _t("cone_nome_b", "Nome do Cone (fim)", CONE_NOME_B, 30, "recompensa"),
        _t("cone_memoria", "Memória do Cone", CONE_MEMORIA, 30, "recompensa"),
        _t("cone_gatilho", "Gatilho do Efeito Condicional", CONE_GATILHO, 20, "recompensa",
           fonte="Livro 25.2 (6 primeiras) + Sugestão da planilha (H11)"),
        _t("conjunto_nome", "Nome do Conjunto", CONJUNTO_NOME, 20, "recompensa"),
        _t("conjunto_origem", "Origem do Conjunto", CONJUNTO_ORIGEM, 20, "recompensa"),
        _t("conjunto_4", "Efeito de 4 peças", CONJUNTO_4, 10, "recompensa",
           fonte="Livro 25.3 (2 primeiras) + Sugestão da planilha (H11)"),
    ]
    import mestre_sabor_mundo as MU       # Fase 3: abas Mundos e Improviso
    T += MU.tabelas(_t)
    return T


LIVRO_NO_INICIO = {"prazo": ("27", "## 27.7", PRAZO_LIVRO), "cone_gatilho": ("25", "## 25.2", CONE_GATILHO_LIVRO),
                   "conjunto_4": ("25", "## 25.3", CONJUNTO_4_LIVRO)}


def conferir():
    """Fatal no build (design §10.2): menos que o mínimo, vazio, repetido (fora das listas de peso) ou > 200."""
    for t in tabelas():
        vs = t["valores"]
        if len(vs) < t["minimo"]:
            raise ValueError(f"mestre_sabor: tab.{t['id']} com {len(vs)} entradas (mínimo {t['minimo']})")
        if len(vs) > 100:
            raise ValueError(f"mestre_sabor: tab.{t['id']} passa de 100 vagas")
        for v in vs + [str(x) for x in (t["segunda"] or ("", []))[1]]:    # a 2ª coluna do oráculo tem números (H10)
            if not v or not v.strip() or len(v) > 200:
                raise ValueError(f"mestre_sabor: tab.{t['id']}: entrada vazia ou com mais de 200 caracteres: {v!r}")
            if v[0] in "=+-@":
                raise ValueError(f"mestre_sabor: tab.{t['id']}: {v!r} começa com {v[0]} (o Google lê como fórmula)")
        if not t["pesos"] and len(set(vs)) != len(vs):
            raise ValueError(f"mestre_sabor: tab.{t['id']} com entrada repetida")
        if t["segunda"] and len(set(t["segunda"][1])) != len(t["segunda"][1]):
            raise ValueError(f"mestre_sabor: tab.{t['id']} com valor repetido na 2ª coluna")
    return True
