# -*- coding: utf-8 -*-
"""
mestre_sabor_nomes.py — nomes por cultura da Planilha do Mestre (design §6.16, R5).

Texto ORIGINAL escrito para a planilha, no estilo de cada cultura descrita no capítulo 05 (e na regra de escrita
de 6.16): Humano cosmopolita (origens terrestres misturadas); Xianzhouíta com nome de duas sílabas de sonoridade
chinesa clássica (virtude, elemento) e sobrenome de família na frente; Vidyadhara com nome longo de mar e linhagem
("da Maré Funda"); Vulpes com nome curto de sonoridade leste-asiática e epíteto de mercador ou de cauda; Haloviano
com nome melódico de vogais abertas e sobrenome de canção; Avginiano com nome curto e o clã errante; Intellitron
com designação alfanumérica e o nome que escolheu ("KV-12, que se chama Paciência").
Nenhum nome é de personagem do jogo (a suíte sabor confere contra a lista de nomes proibidos, também cada
combinação nome + sobrenome). Estas listas ficam fora da ortografia (sem_ortografia), não fora do glossário.
"""

CULTURAS = ["Humano", "Xianzhouíta", "Vidyadhara", "Vulpes", "Haloviano", "Avginiano", "Intellitron"]   # 05
SLUG = {"Humano": "humano", "Xianzhouíta": "xianzhouita", "Vidyadhara": "vidyadhara", "Vulpes": "vulpes",
        "Haloviano": "haloviano", "Avginiano": "avginiano", "Intellitron": "intellitron"}
# como o nome completo se monta (sem SUBSTITUTE: ordem 1 = nome + separador + sobrenome; 2 = sobrenome primeiro)
MONTAGEM = {"Humano": (1, " "), "Xianzhouíta": (2, " "), "Vidyadhara": (1, " "), "Vulpes": (1, " "),
            "Haloviano": (1, " "), "Avginiano": (1, " do clã "), "Intellitron": (1, ", que se chama ")}

NOMES = {
    "Humano": [
        "Teodora", "Ilan", "Marisol", "Kwame", "Ingrid", "Tadeu", "Yasmin", "Oleg", "Beatriz", "Ravi",
        "Joaquim", "Aiko", "Dário", "Fenna", "Emeka", "Lúcia", "Bastian", "Priya", "Caetano", "Sigrid",
        "Matteo", "Zuleica", "Anselmo", "Hanna", "Otávio", "Renata", "Kofi", "Ilse", "Esperança", "Leif",
        "Amara", "Vítor",
    ],
    "Xianzhouíta": [
        "Wenshu", "Zhaolin", "Chunhe", "Qiuyan", "Shuiming", "Rongan", "Huaijin", "Lianshu", "Mingde", "Yaozhen",
        "Shoucheng", "Xinhe", "Jinlu", "Zhenhai", "Yuehan", "Songli", "Ruoshui", "Heqing", "Lianyi", "Chengfeng",
        "Mujin", "Tianze", "Xuanhe", "Jianshu", "Shanqiu", "Yuanxi", "Zhuoran", "Kunlin", "Haoyu", "Baozhen",
        "Dezhao", "Qiaoming",
    ],
    "Vidyadhara": [
        "Chaoyinhe", "Haishenglu", "Langqiuyan", "Yuanchaoming", "Shuiyueqing", "Haiyuanzhi", "Bolanxinyu",
        "Chenhaijun", "Yongchaoxi", "Ruohaifeng", "Qianlangsu", "Haitangrui", "Xuchaolin", "Mingchaohua",
        "Taoshuiwen", "Liuhaiqing", "Shenlanyue", "Zhaochaoyi", "Wuhaisheng", "Yinlangshu", "Huaichaoyun",
        "Pingbohai", "Jiangyuexin", "Moshuilan", "Haoranbohai", "Qingchaozhi", "Ruilanhai", "Xiaochaoming",
        "Duhaiyuan", "Lanchaosong", "Wenbolang",
    ],
    "Vulpes": [
        "Rin", "Kiku", "Yuna", "Tomo", "Haru", "Mika", "Aoi", "Ren", "Kaede", "Nagi",
        "Sae", "Ryo", "Hina", "Taki", "Kumi", "Shin", "Emi", "Yori", "Koto", "Sumi",
        "Maru", "Chika", "Rei", "Ayu", "Tsuki", "Nami", "Hoshi", "Kazu", "Fumi", "Akane",
        "Ume",
    ],
    "Haloviano": [
        "Aelia", "Ilauna", "Oraelo", "Mirava", "Solenne", "Liora", "Avaneh", "Elaré", "Ianthe", "Orimae",
        "Saluen", "Valoa", "Eolin", "Amarae", "Noelia", "Ilevara", "Auralie", "Selaro", "Maelune", "Oriane",
        "Leova", "Inaela", "Aruena", "Celavo", "Elouan", "Yselde", "Amaleo", "Oleanor", "Siora", "Evarina",
        "Aurenor",
    ],
    "Avginiano": [
        "Kesh", "Tavi", "Ondo", "Zev", "Ilo", "Saka", "Bren", "Dalu", "Hesk", "Nima",
        "Teva", "Kalo", "Asha", "Rovi", "Siv", "Arno", "Leku", "Mavi", "Odda", "Raki",
        "Tesa", "Uli", "Vasko", "Yeni", "Zora", "Gabo", "Pema", "Orik", "Dessa", "Fen",
        "Juta",
    ],
    "Intellitron": [
        "AT-07", "RQ-31", "MN-40", "ZL-9", "OX-112", "PT-5", "VK-23", "HL-88", "SN-14", "TM-60",
        "QB-17", "LX-02", "EV-71", "GR-45", "NC-8", "WY-19", "BT-306", "IO-22", "FK-11", "UR-6",
        "JD-90", "CA-27", "YM-13", "KR-55", "SB-4", "PL-73", "XE-38", "MO-1", "TR-210", "DV-66",
        "HZ-501",
    ],
}

SOBRENOMES = {
    "Humano": [
        "Okonkwo-Reis", "Vasquez", "Lindqvist", "Moraes", "Tanaka-Oduya", "Brandão", "Kowalczyk", "Haddad",
        "Fonseca", "Achterberg", "Nakamura", "Sorensen", "Albuquerque", "Mbeki", "Petrov", "Castellanos", "Iwu",
        "Halvorsen", "Quaresma", "Delacroix", "Ferraz", "Oyelaran", "Varga", "Montenegro", "Szabo", "Rocha",
        "Abernathy", "Kaur", "Lisboa", "Ostrowski", "Duarte-Kim",
    ],
    "Xianzhouíta": [
        "Shen", "Lou", "Qian", "Guo", "Cen", "Pei", "Xu", "Tang", "Zou", "Kong",
        "Shi", "Feng", "Wei", "Hua", "Jiang", "Yao", "Ning", "Qu", "Rong", "Xiang",
        "Zeng", "Mu", "Dou", "Ke", "Ji", "Tao", "Ou", "Bian", "Gong", "Zhuo",
        "Cui", "Gao",
    ],
    "Vidyadhara": [
        "da Maré Funda", "do Recife Calado", "da Corrente Fria", "das Águas Paradas", "do Abismo Azul",
        "da Espuma Antiga", "do Poço de Pérolas", "da Baía Sem Nome", "da Onda Quebrada", "do Leito de Coral",
        "da Névoa Salgada", "do Farol Afundado", "da Maré Vazante", "das Escamas de Prata", "do Mar de Dentro",
        "da Fonte Submersa", "do Redemoinho Lento", "da Concha Partida", "das Profundezas Mansas",
        "do Estreito Velho", "da Lua sobre a Água", "da Chuva de Sal", "do Lago Sem Fundo", "da Corrente Quente",
        "das Ilhas Caídas", "do Cardume Dourado", "da Água que Lembra", "do Rio que Volta", "da Maré Cheia",
        "das Algas Altas",
    ],
    "Vulpes": [
        "Sete Caudas", "Cauda de Cobre", "Balança Fiel", "Preço Justo", "Moeda Dobrada", "Cauda Ruiva",
        "Pelo de Prata", "Bolsa Funda", "Conta Certa", "Feira Longa", "Selo de Âmbar", "Cauda Partida",
        "Três Contratos", "Lanterna do Cais", "Palavra Doce", "Faro Fino", "Caravana Lenta", "Cauda Branca",
        "Juro Baixo", "Troca Rápida", "Orelha Atenta", "Balcão Antigo", "Leilão da Lua", "Cauda de Fumaça",
        "Peso Honesto", "Conchas Contadas", "Lucro Paciente", "Fio de Ouro", "Nove Recibos", "Cauda Inquieta",
    ],
    "Haloviano": [
        "Canto da Aurora", "Coro Distante", "Nota Suspensa", "Hino das Asas", "Balada Lenta", "Refrão de Prata",
        "Voz do Halo", "Acorde Aberto", "Cantiga do Vento", "Prelúdio Azul", "Canção de Ninar", "Eco Sereno",
        "Melodia Quebrada", "Ária da Manhã", "Toada Antiga", "Harpa Silenciosa", "Verso Final", "Coral das Luzes",
        "Sonata Breve", "Cadência Doce", "Serenata Longa", "Nota Alta", "Canto Sem Fim", "Abertura Dourada",
        "Refrão Perdido", "Hino do Sono", "Cantiga de Roda", "Coro das Marés", "Acorde Menor", "Canção do Retorno",
    ],
    "Avginiano": [
        "Tenda Vermelha", "Caravana do Sal", "Trilha Cinzenta", "Poeira Viva", "Fogueira Sem Chão",
        "Estrada Longa", "Rebanho de Estrelas", "Vento de Passagem", "Último Oásis", "Pegada Funda",
        "Lona Remendada", "Roda Quebrada", "Dunas Altas", "Cinza Errante", "Sem Porto", "Ponte de Corda",
        "Fronteira Aberta", "Chão Emprestado", "Mapa Rasgado", "Tenda de Couro", "Brasa Guardada", "Passo Leve",
        "Céu Aberto", "Rota Esquecida", "Água Contada", "Pedra Carregada", "Sol Poente", "Bússola Torta",
        "Noite Fria", "Muitos Portos",
    ],
    "Intellitron": [
        "Vigília", "Constância", "Silêncio", "Prudência", "Aurora", "Engrenagem", "Lembrança", "Sereno",
        "Cuidado", "Persistência", "Origem", "Bússola", "Resposta", "Ternura", "Clemência", "Horizonte",
        "Faísca", "Medida", "Âncora", "Promessa", "Teimosia", "Inverno", "Coerência", "Gentileza", "Atenção",
        "Retorno", "Calma", "Curiosidade", "Esperança", "Fôlego",
    ],
}
