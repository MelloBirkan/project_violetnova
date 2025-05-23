import pygame

# Dicionário de tradução de planetas
PLANET_NAME_PT = {
    "Earth": "Terra",
    "Mercury": "Mercúrio",
    "Venus": "Vênus",
    "Mars": "Marte",
    "Jupiter": "Júpiter",
    "Saturn": "Saturno",
    "Moon": "Lua",
    "Uranus": "Urano",
    "Neptune": "Netuno"
}


# Limiares de progressão de nível
LEVEL_PROGRESSION_THRESHOLDS = {
    "Earth": 9,
    "Mercury": 7,
    "Venus": 7,
    "Moon": 3,
    "Mars": 6,
    "Jupiter": 20,
    "Saturn": 17,
    "Uranus": 15,
    "Neptune": 14,
}

def create_planet_data():
    """Cria os dados para todos os planetas do jogo"""
    planet_data = [
        {
            "name": "Earth",
            "gravity_factor": 100,  # Base gravity (g = 1.0)
            "background_color": (25, 25, 112),  # Midnight blue
            "obstacle_count": 6,
            "quiz_questions": [
                {
                    "question": "Qual percentual da Terra é coberto por água?",
                    "options": ["51%", "61%", "71%", "81%"],
                    "answer": 2,  # 71%
                    "explanation": "Mais de dois terços do planeta é recoberto por oceanos."
                },
                {
                    "question": "A atmosfera da Terra é composta principalmente por qual gás?",
                    "options": ["Oxigênio", "Dióxido de Carbono", "Hidrogênio", "Nitrogênio"],
                    "answer": 3,  # Nitrogênio
                    "explanation": "Esse gás corresponde a cerca de 78% da atmosfera."
                },
                {
                    "question": "Quanto tempo leva para a Terra girar uma vez em seu eixo?",
                    "options": ["12 horas", "24 horas", "365 dias", "28 dias"],
                    "answer": 1,  # 24 horas
                    "explanation": "É o período que define a duração de um dia na Terra."
                }
            ],
            "hints": [
                "Mais de dois terços do planeta é recoberto por oceanos.",
                "Esse gás corresponde a cerca de 78% da atmosfera.",
                "É o período que define a duração de um dia na Terra."
            ]
        },
        {
            "name": "Mercury",
            "gravity_factor": 40,  # g = 0.4
            "background_color": (70, 50, 40),  # Brown
            "obstacle_count": 2,
            "quiz_questions": [
                {
                    "question": "Mercúrio é o _____ planeta a partir do Sol.",
                    "options": ["Primeiro", "Segundo", "Terceiro", "Quarto"],
                    "answer": 0,
                    "explanation": "É o planeta mais próximo do Sol."
                },
                {
                    "question": "Um dia em Mercúrio equivale a aproximadamente quantos dias terrestres?",
                    "options": ["29 dias", "59 dias", "88 dias", "176 dias"],
                    "answer": 1,
                    "explanation": "Sua rotação leva quase dois meses terrestres."
                },
                {
                    "question": "A temperatura na superfície de Mercúrio pode chegar a:",
                    "options": ["100°C", "230°C", "430°C", "530°C"],
                    "answer": 2,
                    "explanation": "A face iluminada pode superar 400°C."
                }
            ],
            "hints": [
                "É o planeta mais próximo do Sol.",
                "Sua rotação leva quase dois meses terrestres.",
                "A face iluminada pode superar 400°C."
            ]
        },
        {
            "name": "Venus",
            "gravity_factor": 90,  # g = 0.9
            "background_color": (140, 90, 40),  # Amber
            "obstacle_count": 4,
            "quiz_questions": [
                {
                    "question": "Vênus gira em qual direção?",
                    "options": ["Igual à Terra", "Oposta à Terra", "Não gira", "Muda aleatoriamente"],
                    "answer": 1,
                    "explanation": "Seu movimento de rotação é contrário ao da maioria dos planetas."
                },
                {
                    "question": "A atmosfera de Vênus é composta principalmente por:",
                    "options": ["Nitrogênio", "Dióxido de Carbono", "Ácido Sulfúrico", "Metano"],
                    "answer": 1,
                    "explanation": "A atmosfera é espessa e composta quase toda por CO2."
                },
                {
                    "question": "Vênus é frequentemente chamado de planeta irmão da Terra porque:",
                    "options": ["Tem oceanos", "Tamanho e massa similares", "Tem vida", "Mesmo tempo de órbita"],
                    "answer": 1,
                    "explanation": "Possui tamanho e massa parecidos com os da Terra."
                }
            ],
            "hints": [
                "Seu movimento de rotação é contrário ao da maioria dos planetas.",
                "A atmosfera é espessa e composta quase toda por CO2.",
                "Possui tamanho e massa parecidos com os da Terra."
            ]
        },
        {
            "name": "Mars",
            "gravity_factor": 40,  # g = 0.4
            "background_color": (150, 70, 40),  # Rust red
            "obstacle_count": 3,
            "quiz_questions": [
                {
                    "question": "O que dá a Marte sua cor vermelha distintiva?",
                    "options": ["Vida vegetal", "Óxido de ferro (ferrugem)", "Dióxido de carbono", "Luz solar refletida"],
                    "answer": 1,
                    "explanation": "Sua superfície contém muito óxido de ferro."
                },
                {
                    "question": "Quantas luas Marte possui?",
                    "options": ["Nenhuma", "Uma", "Duas", "Três"],
                    "answer": 2,
                    "explanation": "O planeta possui dois pequenos satélites naturais."
                },
                {
                    "question": "Qual é o nome do maior vulcão em Marte?",
                    "options": ["Mauna Loa", "Olympus Mons", "Monte Everest", "Mons Huygens"],
                    "answer": 1,
                    "explanation": "O maior vulcão conhecido do Sistema Solar está aqui."
                }
            ],
            "hints": [
                "Sua superfície contém muito óxido de ferro.",
                "O planeta possui dois pequenos satélites naturais.",
                "O maior vulcão conhecido do Sistema Solar está aqui."
            ]
        },
        {
            "name": "Jupiter",
            "gravity_factor": 240,  # g = 2.4
            "background_color": (210, 140, 70),  # Tan
            "obstacle_count": 20,
            "quiz_questions": [
                {
                    "question": "Do que Júpiter é composto principalmente?",
                    "options": ["Rocha e metal", "Água e gelo", "Hidrogênio e hélio", "Dióxido de carbono"],
                    "answer": 2,
                    "explanation": "É formado basicamente por gases leves."
                },
                {
                    "question": "O que é a Grande Mancha Vermelha em Júpiter?",
                    "options": ["Um vulcão", "Uma tempestade de poeira", "Uma tempestade tipo furacão", "Uma cratera de impacto"],
                    "answer": 2,
                    "explanation": "Sua famosa mancha é uma enorme tempestade."
                },
                {
                    "question": "Júpiter tem o dia mais curto de qualquer planeta. Quanto tempo dura?",
                    "options": ["6 horas", "10 horas", "14 horas", "18 horas"],
                    "answer": 1,
                    "explanation": "O planeta gira muito rápido em torno de si."
                }
            ],
            "hints": [
                "É formado basicamente por gases leves.",
                "Sua famosa mancha é uma enorme tempestade.",
                "O planeta gira muito rápido em torno de si."
            ]
        },
        {
            "name": "Saturn",
            "gravity_factor": 110,  # g = 1.1
            "background_color": (180, 150, 100),  # Light tan
            "obstacle_count": 15,
            "quiz_questions": [
                {
                    "question": "Do que são feitos os anéis de Saturno principalmente?",
                    "options": ["Gás", "Poeira", "Rocha e metal", "Partículas de gelo"],
                    "answer": 3,
                    "explanation": "Seus anéis são compostos principalmente de gelo."
                },
                {
                    "question": "Quantos anéis principais Saturno possui?",
                    "options": ["3", "5", "7", "9"],
                    "answer": 2,
                    "explanation": "O sistema de anéis visíveis é formado por sete divisões."
                },
                {
                    "question": "Saturno é o único planeta que poderia flutuar na água porque:",
                    "options": ["É oco", "É muito pequeno", "Sua densidade é menor que a da água", "Tem hélio"],
                    "answer": 2,
                    "explanation": "Por ter baixa densidade, poderia flutuar em água."
                }
            ],
            "hints": [
                "Seus anéis são compostos principalmente de gelo.",
                "O sistema de anéis visíveis é formado por sete divisões.",
                "Por ter baixa densidade, poderia flutuar em água."
            ]
        },
        {
            "name": "Moon",
            "gravity_factor": 16,  # g = 0.16
            "background_color": (20, 20, 20),  # Very dark gray
            "obstacle_count": 2,
            "quiz_questions": [
                {
                    "question": "Qual é a distância média da Lua à Terra?",
                    "options": ["184.000 km", "238.000 km", "384.000 km", "584.000 km"],
                    "answer": 2,
                    "explanation": "Fica a aproximadamente 384 mil quilômetros do nosso planeta."
                },
                {
                    "question": "O primeiro humano a caminhar na Lua foi:",
                    "options": ["Buzz Aldrin", "Neil Armstrong", "Yuri Gagarin", "Alan Shepard"],
                    "answer": 1,
                    "explanation": "Neil Armstrong foi quem deu os primeiros passos em seu solo."
                },
                {
                    "question": "O que causa as fases da Lua?",
                    "options": ["Sombra da Terra", "Posição do Sol", "Rotação da Lua", "Nuvens na Lua"],
                    "answer": 1,
                    "explanation": "As fases acontecem conforme sua posição em relação ao Sol."
                }
            ],
            "hints": [
                "Fica a aproximadamente 384 mil quilômetros do nosso planeta.",
                "Neil Armstrong foi quem deu os primeiros passos em seu solo.",
                "As fases acontecem conforme sua posição em relação ao Sol."
            ]
        },
        {
            "name": "Uranus",
            "gravity_factor": 90,  # g = 0.9
            "background_color": (140, 210, 210),  # Cyan
            "obstacle_count": 12,
            "quiz_questions": [
                {
                    "question": "Urano gira de lado com uma inclinação axial de aproximadamente:",
                    "options": ["23 graus", "45 graus", "72 graus", "98 graus"],
                    "answer": 3,
                    "explanation": "Seu eixo de rotação é extremamente inclinado."
                },
                {
                    "question": "O que dá a Urano sua cor azul-esverdeada?",
                    "options": ["Água", "Metano", "Amônia", "Nitrogênio"],
                    "answer": 1,
                    "explanation": "A coloração azulada vem do metano na atmosfera."
                },
                {
                    "question": "Urano foi o primeiro planeta descoberto usando um:",
                    "options": ["Olho nu", "Telescópio", "Sonda espacial", "Radiotelescópio"],
                    "answer": 1,
                    "explanation": "Foi o primeiro planeta descoberto com o auxílio de telescópios."
                }
            ],
            "hints": [
                "Seu eixo de rotação é extremamente inclinado.",
                "A coloração azulada vem do metano na atmosfera.",
                "Foi o primeiro planeta descoberto com o auxílio de telescópios."
            ]
        },
        {
            "name": "Neptune",
            "gravity_factor": 110,  # g = 1.1
            "background_color": (30, 50, 180),  # Deep blue
            "obstacle_count": 11,
            "quiz_questions": [
                {
                    "question": "Netuno foi descoberto com base em previsões matemáticas em:",
                    "options": ["1646", "1746", "1846", "1946"],
                    "answer": 2,
                    "explanation": "Sua existência foi prevista antes mesmo de ser observado."
                },
                {
                    "question": "O que é a Grande Mancha Escura em Netuno?",
                    "options": ["Um oceano", "Um sistema de tempestade", "Uma cratera", "Uma sombra"],
                    "answer": 1,
                    "explanation": "Abriga uma grande tempestade conhecida como Mancha Escura."
                },
                {
                    "question": "A maior lua de Netuno é:",
                    "options": ["Tritão", "Nereida", "Proteus", "Larissa"],
                    "answer": 0,
                    "explanation": "Tritão é sua maior lua e possui órbita retrógrada."
                }
            ],
            "hints": [
                "Sua existência foi prevista antes mesmo de ser observado.",
                "Abriga uma grande tempestade conhecida como Mancha Escura.",
                "Tritão é sua maior lua e possui órbita retrógrada."
            ]
        }
        # Plutão removido da progressão principal
    ]

    return planet_data