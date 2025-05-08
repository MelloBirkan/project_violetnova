import pygame
import sys
import random
import math
from src.spacecraft import Spacecraft
from src.obstacle import Obstacle
from src.collectible import Collectible
from src.planet import Planet
from src.highscore import HighScore
from src.nova_ai import NovaAI
# Para funcionalidade de quiz
from src.quiz import Quiz

# Mapeamentos de localização para exibição em português
COLOR_NAME_PT = {
    "silver": "Prateado",
    "gold": "Dourado",
    "blue": "Azul",
    "red": "Vermelho"
}
PLANET_NAME_PT = {
    "Earth": "Terra",
    "Mercury": "Mercúrio",
    "Venus": "Vênus",
    "Moon": "Lua",
    "Mars": "Marte",
    "Jupiter": "Júpiter",
    "Saturn": "Saturno",
    "Uranus": "Urano",
    "Neptune": "Netuno",
    "Pluto": "Plutão"
}

# Inicializa o pygame
pygame.init()
pygame.mixer.init()

# Constantes do jogo
# Define resolução HD fixa (1280x720)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FLOOR_HEIGHT = 100
GAME_FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)
COUNTDOWN_FONT = pygame.font.Font(None, 180)  # Fonte maior para contagem regressiva

# Estados do jogo
MENU = 0
PLAYING = 1
GAME_OVER = 2
TRANSITION = 3
QUIZ = 4
QUIZ_FAILURE = 5  # Novo estado para atraso de falha no quiz
# Modos de controle
CONTROL_MODE_FLAPPY = 0  # Apenas toque, estilo Flappy Bird
CONTROL_MODE_HOLD = 1    # Segure espaço para impulso contínuo

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Project Blue Nova: Explorador do Sistema Solar")
clock = pygame.time.Clock()

# Carrega assets
try:
    # Carrega sons
    thrust_sound = pygame.mixer.Sound("assets/sounds/flap.wav")
    score_sound = pygame.mixer.Sound("assets/sounds/score.wav")
    hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")

except pygame.error as e:
    print(f"Não foi possível carregar o asset: {e}")
    pygame.quit()
    sys.exit()

# Define progressão de planetas e perguntas do quiz
def create_planet_data():
    """Cria dados para todos os planetas no jogo"""
    planet_data = [
        {
            "name": "Earth",
            "gravity_factor": 100,  # Gravidade base (g = 1.0)
            "background_color": (25, 25, 112),  # Azul meia-noite
            "obstacle_count": 6,  # Atualizado de 4 para 6
            "quiz_questions": [
                {
                    "question": "Qual percentual da Terra é coberto por água?",
                    "options": ["51%", "61%", "71%", "81%"],
                    "answer": 2  # 71% (índice baseado em 0)
                },
                {
                    "question": "A atmosfera da Terra é composta principalmente por qual gás?",
                    "options": ["Oxigênio", "Dióxido de Carbono", "Hidrogênio", "Nitrogênio"],
                    "answer": 3  # Nitrogênio
                },
                {
                    "question": "Quanto tempo leva para a Terra girar uma vez em seu eixo?",
                    "options": ["12 horas", "24 horas", "365 dias", "28 dias"],
                    "answer": 1  # 24 horas
                }
            ]
        },
        {
            "name": "Mercury",
            "gravity_factor": 40,  # Atualizado de 38 para 40 (g = 0.4)
            "background_color": (70, 50, 40),  # Marrom
            "obstacle_count": 2,  # Atualizado de 5 para 2
            "quiz_questions": [
                {
                    "question": "Mercúrio é o _____ planeta a partir do Sol.",
                    "options": ["Primeiro", "Segundo", "Terceiro", "Quarto"],
                    "answer": 0  # Primeiro
                },
                {
                    "question": "Um dia em Mercúrio equivale a aproximadamente quantos dias terrestres?",
                    "options": ["29 dias", "59 dias", "88 dias", "176 dias"],
                    "answer": 1  # 59 dias
                },
                {
                    "question": "A temperatura na superfície de Mercúrio pode chegar a:",
                    "options": ["100°C", "230°C", "430°C", "530°C"],
                    "answer": 2  # 430°C
                }
            ]
        },
        {
            "name": "Venus",
            "gravity_factor": 90,  # Inalterado (g = 0.9)
            "background_color": (140, 90, 40),  # Âmbar
            "obstacle_count": 4,  # Atualizado de 6 para 4
            "quiz_questions": [
                {
                    "question": "Vênus gira em qual direção?",
                    "options": ["Igual à Terra", "Oposta à Terra", "Não gira", "Muda aleatoriamente"],
                    "answer": 1  # Oposto à Terra (retrógrado)
                },
                {
                    "question": "A atmosfera de Vênus é composta principalmente por:",
                    "options": ["Nitrogênio", "Dióxido de Carbono", "Ácido Sulfúrico", "Metano"],
                    "answer": 1  # Dióxido de Carbono
                },
                {
                    "question": "Vênus é frequentemente chamado de planeta irmão da Terra porque:",
                    "options": ["Tem oceanos", "Tamanho e massa similares", "Tem vida", "Mesmo tempo de órbita"],
                    "answer": 1  # Tamanho e massa similares
                }
            ]
        },
        {
            "name": "Mars",
            "gravity_factor": 40,  # Atualizado de 38 para 40 (g = 0.4)
            "background_color": (150, 70, 40),  # Vermelho ferrugem
            "obstacle_count": 3,  # Atualizado de 5 para 3
            "quiz_questions": [
                {
                    "question": "O que dá a Marte sua cor vermelha distintiva?",
                    "options": ["Vida vegetal", "Óxido de ferro (ferrugem)", "Dióxido de carbono", "Luz solar refletida"],
                    "answer": 1  # Óxido de ferro
                },
                {
                    "question": "Quantas luas Marte possui?",
                    "options": ["Nenhuma", "Uma", "Duas", "Três"],
                    "answer": 2  # Duas (Phobos e Deimos)
                },
                {
                    "question": "Qual é o nome do maior vulcão em Marte?",
                    "options": ["Mauna Loa", "Olympus Mons", "Monte Everest", "Mons Huygens"],
                    "answer": 1  # Olympus Mons
                }
            ]
        },
        {
            "name": "Jupiter",
            "gravity_factor": 240,  # Inalterado (g = 2.4)
            "background_color": (210, 140, 70),  # Bronzeado
            "obstacle_count": 20,  # Atualizado de 8 para 20
            "quiz_questions": [
                {
                    "question": "Do que Júpiter é composto principalmente?",
                    "options": ["Rocha e metal", "Água e gelo", "Hidrogênio e hélio", "Dióxido de carbono"],
                    "answer": 2  # Hidrogênio e hélio
                },
                {
                    "question": "O que é a Grande Mancha Vermelha em Júpiter?",
                    "options": ["Um vulcão", "Uma tempestade de poeira", "Uma tempestade tipo furacão", "Uma cratera de impacto"],
                    "answer": 2  # Uma tempestade tipo furacão
                },
                {
                    "question": "Júpiter tem o dia mais curto de qualquer planeta. Quanto tempo dura?",
                    "options": ["6 horas", "10 horas", "14 horas", "18 horas"],
                    "answer": 1  # ~10 horas
                }
            ]
        },
        {
            "name": "Saturn",
            "gravity_factor": 110,  # Inalterado (g = 1.1)
            "background_color": (180, 150, 100),  # Bronzeado claro
            "obstacle_count": 15,  # Atualizado de 7 para 15
            "quiz_questions": [
                {
                    "question": "Do que são feitos os anéis de Saturno principalmente?",
                    "options": ["Gás", "Poeira", "Rocha e metal", "Partículas de gelo"],
                    "answer": 3  # Partículas de gelo
                },
                {
                    "question": "Quantos anéis principais Saturno possui?",
                    "options": ["3", "5", "7", "9"],
                    "answer": 2  # 7 anéis principais
                },
                {
                    "question": "Saturno é o único planeta que poderia flutuar na água porque:",
                    "options": ["É oco", "É muito pequeno", "Sua densidade é menor que a da água", "Tem hélio"],
                    "answer": 2  # Baixa densidade
                }
            ]
        },
        {
            "name": "Moon",
            "gravity_factor": 16,  # Atualizado de 16.6 para 16 (g = 0.16)
            "background_color": (20, 20, 20),  # Cinza muito escuro
            "obstacle_count": 2,  # Atualizado de 3 para 2
            "quiz_questions": [
                {
                    "question": "Qual é a distância média da Lua à Terra?",
                    "options": ["184.000 km", "238.000 km", "384.000 km", "584.000 km"],
                    "answer": 2  # 384.000 km
                },
                {
                    "question": "O primeiro humano a caminhar na Lua foi:",
                    "options": ["Buzz Aldrin", "Neil Armstrong", "Yuri Gagarin", "Alan Shepard"],
                    "answer": 1  # Neil Armstrong
                },
                {
                    "question": "O que causa as fases da Lua?",
                    "options": ["Sombra da Terra", "Posição do Sol", "Rotação da Lua", "Nuvens na Lua"],
                    "answer": 1  # Posição do Sol
                }
            ]
        },
        {
            "name": "Uranus",
            "gravity_factor": 90,  # Inalterado (g = 0.9)
            "background_color": (140, 210, 210),  # Ciano
            "obstacle_count": 12,  # Atualizado de 6 para 12
            "quiz_questions": [
                {
                    "question": "Urano gira de lado com uma inclinação axial de aproximadamente:",
                    "options": ["23 graus", "45 graus", "72 graus", "98 graus"],
                    "answer": 3  # 98 graus
                },
                {
                    "question": "O que dá a Urano sua cor azul-esverdeada?",
                    "options": ["Água", "Metano", "Amônia", "Nitrogênio"],
                    "answer": 1  # Metano
                },
                {
                    "question": "Urano foi o primeiro planeta descoberto usando um:",
                    "options": ["Olho nu", "Telescópio", "Sonda espacial", "Radiotelescópio"],
                    "answer": 1  # Telescópio
                }
            ]
        },
        {
            "name": "Neptune",
            "gravity_factor": 110,  # Inalterado (g = 1.1)
            "background_color": (30, 50, 180),  # Azul profundo
            "obstacle_count": 11,  # Atualizado de 7 para 11
            "quiz_questions": [
                {
                    "question": "Netuno foi descoberto com base em previsões matemáticas em:",
                    "options": ["1646", "1746", "1846", "1946"],
                    "answer": 2  # 1846
                },
                {
                    "question": "O que é a Grande Mancha Escura em Netuno?",
                    "options": ["Um oceano", "Um sistema de tempestade", "Uma cratera", "Uma sombra"],
                    "answer": 1  # Um sistema de tempestade
                },
                {
                    "question": "A maior lua de Netuno é:",
                    "options": ["Tritão", "Nereida", "Proteus", "Larissa"],
                    "answer": 0  # Tritão
                }
            ]
        }
        # Pluto removido da progressão principal
        # {
        #     "name": "Pluto",
        #     "gravity_factor": 6,  # g = 0.06
        #     "background_color": (50, 50, 80),  # Azul ardósia escuro
        #     "obstacle_count": 1,  # Nível terminal com 1 obstáculo
        #     "quiz_questions": [
        #         {
        #             "question": "Em que ano Plutão foi reclassificado como planeta anão?",
        #             "options": ["2000", "2006", "2010", "2015"],
        #             "answer": 1  # 2006
        #         },
        #         {
        #             "question": "Qual sonda da NASA forneceu as primeiras imagens de perto de Plutão?",
        #             "options": ["Voyager", "New Horizons", "Cassini", "Juno"],
        #             "answer": 1  # New Horizons
        #         },
        #         {
        #             "question": "A maior lua de Plutão é chamada:",
        #             "options": ["Hydra", "Nix", "Caronte", "Kerberos"],
        #             "answer": 2  # Caronte
        #         }
        #     ]
        # }
    ]

    return planet_data

class Game:
    def __init__(self):
        self.state = MENU
        self.score = 0
        self.high_score_manager = HighScore()
        self.high_score = self.high_score_manager.get()

        # Cria dados dos planetas
        self.planet_data = create_planet_data()
        self.planets = [Planet(data["name"], 
                              data["gravity_factor"], 
                              data["background_color"], 
                              data["obstacle_count"], 
                              data["quiz_questions"]) 
                       for data in self.planet_data]

        # Começa na Terra
        self.current_planet_index = 0
        self.current_planet = self.planets[self.current_planet_index]

        # Configuração da nave espacial
        self.spacecraft_color = "silver"  # Cor padrão
        self.spacecraft = Spacecraft(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.spacecraft_color)
        self.available_colors = list(Spacecraft.COLORS.keys())
        self.current_color_index = 0

        # Elementos do jogo
        self.obstacles = []
        self.collectibles = []
        # Inicializa last_obstacle_time com um valor que acionará a geração imediata de obstáculos
        self.last_obstacle_time = pygame.time.get_ticks() - 2000
        self.last_collectible_time = pygame.time.get_ticks()
        self.floor_x = 0

        # Temporização de obstáculos e colecionáveis
        self.obstacle_spawn_rate = 2500  # milissegundos (aumentado para maior espaçamento horizontal)
        self.collectible_spawn_rate = 3000  # milissegundos

        # Progressão do jogo
        self.obstacle_speed = 3
        self.weapon_active = False
        self.weapon_timer = 0

        # Limiares de pontuação para progressão automática de nível
        self.level_progression_thresholds = {
            "Earth": 6,   # 6 pontos necessários para a Terra (correspondendo à contagem de obstáculos)
            "Mercury": 2, # 2 pontos necessários para Mercúrio
            "Venus": 4,   # 4 pontos necessários para Vênus
            "Moon": 2,    # 2 pontos necessários para a Lua
            "Mars": 3,    # 3 pontos necessários para Marte
            "Jupiter": 20, # 20 pontos necessários para Júpiter
            "Saturn": 15,  # 15 pontos necessários para Saturno
            "Uranus": 12,  # 12 pontos necessários para Urano
            "Neptune": 11, # 11 pontos necessários para Netuno
            "Pluto": 1,    # 1 ponto necessário para Plutão (nível terminal)
        }

        # Assistente NOVA AI
        self.nova = NovaAI(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Sistema de quiz
        self.quiz = Quiz(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Tela de transição
        self.transition_time = 0
        self.transition_duration = 180  # 3 segundos a 60fps

        # Progressão de dificuldade
        self.difficulty_multiplier = 1.0

        # Visuais aprimorados
        self.stars = self._generate_stars(100)

        self.quiz_failure_timer = 0  # Temporizador para atraso de falha no quiz
        self.last_countdown_number = 0  # Último número de contagem regressiva exibido
        # Rastreia se o espaço está pressionado para impulso contínuo
        self.space_held = False
        # Modo de controle atual: flappy ou hold
        self.control_mode = CONTROL_MODE_HOLD # Padrão alterado para HOLD

    def _generate_stars(self, count):
        """Gera estrelas para o fundo"""
        stars = []
        for _ in range(count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT - FLOOR_HEIGHT)
            size = random.uniform(0.5, 2.0)
            brightness = random.randint(150, 255)
            twinkle_speed = random.uniform(0.02, 0.1)
            phase = random.uniform(0, 2 * math.pi)
            stars.append({
                "x": x,
                "y": y,
                "size": size,
                "brightness": brightness,
                "base_brightness": brightness,
                "twinkle_speed": twinkle_speed,
                "phase": phase
            })
        return stars

    def reset(self, new_planet=False):
        """Reinicia o jogo, opcionalmente mudando para um novo planeta"""
        self.state = PLAYING
        self.weapon_active = False
        self.weapon_timer = 0

        if new_planet:
            # Lembra a pontuação para progressão
            previous_score = self.score
            # Reinicia a pontuação para o novo planeta
            self.score = 0
            # Atualiza a dificuldade com base no índice do planeta
            self.difficulty_multiplier = 1.0 + (self.current_planet_index * 0.1)
        else:
            # Começo do zero
            self.score = 0
            self.current_planet_index = 0
            self.current_planet = self.planets[self.current_planet_index]
            self.difficulty_multiplier = 1.0

        # Reinicia a posição da nave espacial
        self.spacecraft = Spacecraft(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.spacecraft_color)

        # Limpa todos os obstáculos e colecionáveis
        self.obstacles = []
        self.collectibles = []
        # Inicializa last_obstacle_time com um valor que acionará a geração imediata de obstáculos
        self.last_obstacle_time = pygame.time.get_ticks() - 2000
        self.last_collectible_time = pygame.time.get_ticks()
        # Reinicia a posição do chão
        self.floor_x = 0

        # Dificuldade base ajustada pelo planeta e progressão
        self.obstacle_speed = 3 * self.difficulty_multiplier
        self.obstacle_spawn_rate = int(2500 / self.difficulty_multiplier)  # Aumentado para maior espaçamento horizontal
        self.collectible_spawn_rate = int(3000 / self.difficulty_multiplier)

        # NOVA AI deve alertar sobre a gravidade
        if new_planet:
            self.nova.alert_gravity_change(
                self.current_planet.name, 
                self.current_planet.gravity_factor
            )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if self.state == QUIZ or self.state == QUIZ_FAILURE:
                    # Passa eventos para o sistema de quiz apenas se estiver no estado QUIZ (não em QUIZ_FAILURE)
                    if self.state == QUIZ:
                        self.quiz.handle_event(event)
                else:
                    if event.key == pygame.K_SPACE:
                        if self.state == MENU:
                            self.reset()
                        elif self.state == PLAYING:
                            # Impulso único ao pressionar
                            self.spacecraft.thrust()
                            thrust_sound.play()
                            # Habilita impulso contínuo se estiver no modo hold
                            if self.control_mode == CONTROL_MODE_HOLD:
                                self.space_held = True
                        elif self.state == GAME_OVER:
                            self.reset()
                        elif self.state == TRANSITION:
                            # Pula a transição e força o início do jogo no novo planeta
                            self.reset(new_planet=True)
                    # Muda a cor da nave com a tecla C no menu e alterna o modo de controle no jogo
                    if event.key == pygame.K_c:
                        if self.state == MENU:
                            self.current_color_index = (self.current_color_index + 1) % len(self.available_colors)
                            self.spacecraft_color = self.available_colors[self.current_color_index]
                            self.spacecraft.change_color(self.spacecraft_color)
                        elif self.state == PLAYING:
                            # Alterna o modo de controle entre flappy e hold
                            self.control_mode = CONTROL_MODE_HOLD if self.control_mode == CONTROL_MODE_FLAPPY else CONTROL_MODE_FLAPPY
                            mode_name = "Hold" if self.control_mode == CONTROL_MODE_HOLD else "Flappy"
                            # Atualiza as cores da chama da nave para efeito de impulso
                            if self.control_mode == CONTROL_MODE_HOLD:
                                # Gradiente de amarelo para laranja para vermelho
                                self.spacecraft.flame_colors = [(255, 255, 0), (255, 165, 0), (255, 69, 0)]
                            else:
                                # Chama de cor única
                                self.spacecraft.flame_colors = []
                            self.spacecraft.update_image()
                            self.nova.show_message(f"Modo de controle: {mode_name}", "info")
                    # Ativa a arma com a tecla W se disponível
                    if event.key == pygame.K_w and self.state == PLAYING and self.weapon_active:
                        self._use_weapon()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # para o impulso contínuo ao soltar
                    self.space_held = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    if self.state == QUIZ or self.state == QUIZ_FAILURE: # Changed 'ou' to 'or'
                        # Passa eventos para o sistema de quiz apenas se estiver no estado QUIZ (não em QUIZ_FAILURE)
                        if self.state == QUIZ:
                            self.quiz.handle_event(event)
                    else:
                        if self.state == MENU:
                            self.reset()
                        elif self.state == PLAYING:
                            self.spacecraft.thrust()
                            thrust_sound.play()
                        elif self.state == GAME_OVER:
                            self.reset()
                        elif self.state == TRANSITION:
                            # Pula a transição e força o início do jogo no novo planeta
                            self.reset(new_planet=True)

    def _use_weapon(self):
        """Usa a arma para destruir obstáculos"""
        if not self.weapon_active:
            return

        # Encontra o obstáculo mais próximo da nave que está à frente dela
        target_obstacle = None
        min_distance = float('inf')

        for obstacle in self.obstacles:
            # Mira apenas em obstáculos à frente da nave
            if obstacle.x > self.spacecraft.x:
                distance = obstacle.x - self.spacecraft.x
                if distance < min_distance:
                    min_distance = distance
                    target_obstacle = obstacle

        if target_obstacle:
            # Remove o obstáculo e concede pontos
            self.obstacles.remove(target_obstacle)
            self.score += 2
            self.nova.show_message("Obstáculo destruído!", "alert")
            # Verifica a progressão para o próximo planeta com base na nova pontuação
            current_threshold = self.level_progression_thresholds.get(
                self.current_planet.name,
                10  # Limiar padrão para planetas não especificados
            )
            if self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                next_planet = self.planets[self.current_planet_index + 1]
                self.nova.show_message(f"Navegação automática engajada! Indo para {next_planet.name}!", "excited")
                # Inicia o quiz para avanço de planeta
                self._start_quiz()

    def update(self):
        # Atualiza estrelas (efeito de cintilação)
        for star in self.stars:
            star["phase"] += star["twinkle_speed"]
            twinkle_factor = 0.5 + 0.5 * math.sin(star["phase"])
            star["brightness"] = int(star["base_brightness"] * twinkle_factor)

        # Atualiza NOVA AI
        self.nova.update()

        if self.state == PLAYING:
            # Atualiza a nave com a gravidade do planeta atual
            self.spacecraft.update(self.current_planet.gravity)
            # Impulso contínuo enquanto o espaço está pressionado no modo hold
            if self.control_mode == CONTROL_MODE_HOLD and self.space_held:
                # Aplica pequeno impulso contínuo (20% da potência de impulso)
                cont = self.spacecraft.thrust_power * self.spacecraft.thrust_multiplier * 0.2
                self.spacecraft.velocity -= cont
                # Mantém o efeito de chama
                self.spacecraft.last_thrust_time = pygame.time.get_ticks()

            # Gera obstáculos
            current_time = pygame.time.get_ticks()
            if current_time - self.last_obstacle_time > self.obstacle_spawn_rate:
                # Definimos a abertura (gap) fixa entre os obstáculos
                # O gap precisa ser grande o suficiente para a nave passar
                gap_size = Obstacle.GAP
                
                # Variação de posição para tornar mais desafiador
                # Escolhe entre vários padrões de obstáculos para maior aleatoriedade
                obstacle_pattern = random.randint(1, 5)
                
                if obstacle_pattern == 1:
                    # Padrão 1: Passagem muito baixa (próxima ao solo)
                    min_gap_y = SCREEN_HEIGHT - FLOOR_HEIGHT - 200
                    max_gap_y = SCREEN_HEIGHT - FLOOR_HEIGHT - 120
                    # Garantir que o range é válido
                    min_gap_y = max(min_gap_y, gap_size // 2 + 50)
                elif obstacle_pattern == 2:
                    # Padrão 2: Passagem muito alta (próxima ao topo)
                    min_gap_y = 120
                    max_gap_y = 200
                elif obstacle_pattern == 3:
                    # Padrão 3: Obstáculo apenas em cima (sem obstáculo embaixo)
                    # Colocamos o gap perto do chão para que o obstáculo inferior fique fora da tela
                    min_gap_y = SCREEN_HEIGHT - FLOOR_HEIGHT - 100
                    max_gap_y = SCREEN_HEIGHT - FLOOR_HEIGHT - 20
                elif obstacle_pattern == 4:
                    # Padrão 4: Obstáculo apenas embaixo (sem obstáculo em cima)
                    # Colocamos o gap perto do topo para que o obstáculo superior fique fora da tela
                    min_gap_y = 20
                    max_gap_y = 100
                else:
                    # Padrão 5: Passagem no meio (padrão mais comum)
                    min_gap_y = 200
                    max_gap_y = SCREEN_HEIGHT - FLOOR_HEIGHT - 200
                
                # Garantir que max_gap_y é sempre maior que min_gap_y
                if max_gap_y <= min_gap_y:
                    # Caso os valores estejam invertidos, troca-os
                    min_gap_y, max_gap_y = max_gap_y, min_gap_y
                
                # Garantimos um range mínimo para evitar erro
                if max_gap_y - min_gap_y < 10:
                    max_gap_y = min_gap_y + 10
                
                # Posição central da abertura
                gap_y = random.randint(min_gap_y, max_gap_y)
                
                # Selecionamos aleatoriamente o tipo de obstáculo
                obstacle_type = random.choice(list(Obstacle.TYPES.keys()))

                # Cria um novo obstáculo
                new_obstacle = Obstacle(SCREEN_WIDTH, gap_y, self.obstacle_speed, obstacle_type, SCREEN_HEIGHT)
                self.obstacles.append(new_obstacle)
                self.last_obstacle_time = current_time

                # Ocasionalmente, faz a NOVA alertar sobre obstáculos
                if random.random() < 0.3:  # 30% de chance
                    self.nova.react_to_obstacle(obstacle_type)

            # Gera colecionáveis (dados ou arma)
            if current_time - self.last_collectible_time > self.collectible_spawn_rate:
                # Coloca o colecionável em um local seguro
                x = SCREEN_WIDTH
                y = random.randint(100, SCREEN_HEIGHT - FLOOR_HEIGHT - 50)
                # Determina o tipo de colecionável (90% dados, 10% arma)
                if self.weapon_active or random.random() < 0.9:
                    collectible_type = "data"
                else:
                    collectible_type = "weapon"
                self.collectibles.append(Collectible(x, y, collectible_type))
                self.last_collectible_time = current_time

            # Atualiza obstáculos e verifica pontuação
            for obstacle in self.obstacles:
                obstacle.update()

                # Pontua ao passar pelo obstáculo
                if not obstacle.scored and obstacle.x + obstacle.WIDTH < self.spacecraft.x:
                    self.score += 1
                    obstacle.scored = True
                    score_sound.play()

                    # Obtém o limiar para o planeta atual ou usa o padrão
                    current_threshold = self.level_progression_thresholds.get(
                        self.current_planet.name, 
                        10  # Limiar padrão para planetas não especificados
                    )

                    # Verifica se atingiu ou excedeu o limiar de pontuação para progredir automaticamente
                    if self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                        # NOVA anuncia progressão automática
                        next_planet = self.planets[self.current_planet_index + 1]
                        self.nova.show_message(f"Navegação automática engajada! Indo para {next_planet.name}!", "excited")

                        # Inicia o quiz sem incrementar o índice do planeta ainda - deixa o quiz lidar com a progressão
                        self._start_quiz()

            # Atualiza colecionáveis
            for collectible in list(self.collectibles):
                collectible.update()
                collectible.x -= self.obstacle_speed  # Move na mesma velocidade dos obstáculos

                # Verifica colisão com a nave
                if collectible.check_collision(self.spacecraft):
                    # Aplica efeito do colecionável
                    effect = collectible.get_effect()

                    if effect["effect"] == "info":
                        # Mostra informações do planeta
                        self.nova.give_random_fact(self.current_planet.name)
                        self.score += effect["value"]

                        # Verifica se adicionar pontos acionou a progressão de nível
                        current_threshold = self.level_progression_thresholds.get(
                            self.current_planet.name, 
                            10  # Limiar padrão para planetas não especificados
                        )

                        # Verifica progressão automática após coletar pontos
                        if self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                            # NOVA anuncia progressão automática
                            next_planet = self.planets[self.current_planet_index + 1]
                            self.nova.show_message(f"Navegação automática engajada! Indo para {next_planet.name}!", "excited")

                            # Inicia o quiz sem incrementar o índice do planeta ainda - deixa o quiz lidar com a progressão
                            self._start_quiz()
                            break  # Sai do loop para evitar processar mais colecionáveis
                    elif effect["effect"] == "time":
                        # Estende o tempo de jogo (adiciona pontuação)
                        self.score += effect["value"]
                        self.nova.react_to_discovery("fuel")

                        # Verifica se adicionar pontos acionou a progressão de nível
                        current_threshold = self.level_progression_thresholds.get(
                            self.current_planet.name, 
                            10  # Limiar padrão para planetas não especificados
                        )

                        # Verifica progressão automática após coletar pontos
                        if self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                            # NOVA anuncia progressão automática
                            next_planet = self.planets[self.current_planet_index + 1]
                            self.nova.show_message(f"Navegação automática engajada! Indo para {next_planet.name}!", "excited")

                            # Inicia o quiz sem incrementar o índice do planeta ainda - deixa o quiz lidar com a progressão
                            self._start_quiz()
                            break  # Sai do loop para evitar processar mais colecionáveis
                    elif effect["effect"] == "attack":
                        # Habilita a arma temporariamente
                        self.weapon_active = True
                        self.weapon_timer = 600  # 10 segundos a 60fps
                        self.nova.react_to_discovery("weapon")

                    # Remove item coletado
                    self.collectibles.remove(collectible)

            # Atualiza temporizador da arma
            if self.weapon_active:
                self.weapon_timer -= 1
                if self.weapon_timer <= 0:
                    self.weapon_active = False
                    self.nova.show_message("Sistemas defensivos offline", "normal")

            # Remove obstáculos e colecionáveis fora da tela
            self.obstacles = [obs for obs in self.obstacles if obs.x > -obs.WIDTH]
            self.collectibles = [col for col in self.collectibles if col.x > -col.WIDTH]

            # Verifica colisões
            if self.check_collision():
                hit_sound.play()
                self.state = GAME_OVER
                if self.score > self.high_score_manager.get():
                    self.high_score = self.score
                    self.high_score_manager.save(self.score)

            # Move o chão
            self.floor_x = (self.floor_x - self.obstacle_speed) % 800

        elif self.state == TRANSITION:
            # Atualiza tela de transição
            self.transition_time += 1
            if self.transition_time >= self.transition_duration:
                # Transição completa, inicia o jogo no novo planeta
                self.reset(new_planet=True)

        elif self.state == QUIZ:
            # Atualiza quiz
            self.quiz.update()

            # Verifica se o quiz está completo
            if self.quiz.is_complete():
                if self.quiz.is_correct():
                    # Procede para o próximo planeta
                    self._start_transition()
                else:
                    # Falhou no quiz, define atraso de 3 segundos antes de retornar ao jogo
                    self.state = QUIZ_FAILURE
                    self.quiz_failure_timer = 180  # 3 segundos a 60fps
                    self.last_countdown_number = 3  # Inicia contagem regressiva de 3
                    # Adiciona uma mensagem da NOVA sobre a falha no quiz
                    self.nova.show_message("Quiz falhou! Retornando à órbita em...", "alert")

        elif self.state == QUIZ_FAILURE:
            # Atualiza temporizador de atraso de falha no quiz
            self.quiz_failure_timer -= 1

            # Verifica o número atual da contagem regressiva
            # Converte quadros restantes para segundos (arredonda para cima)
            current_countdown = math.ceil(self.quiz_failure_timer / 60)

            # Se o número da contagem regressiva mudou, toca um efeito sonoro
            if current_countdown < self.last_countdown_number and current_countdown >= 0:
                self.last_countdown_number = current_countdown
                score_sound.play()  # Reutiliza o som de pontuação para a contagem regressiva

                # Adiciona uma mensagem da NOVA sobre a contagem regressiva
                if current_countdown > 0:
                    self.nova.show_message(f"Retornando à órbita em {current_countdown}...", "alert")

            if self.quiz_failure_timer <= 0:
                # Atraso completo, retorna ao jogo
                self.state = PLAYING
                self.nova.show_message("De volta ao voo orbital! Continue explorando.", "info")
                self.last_countdown_number = 0  # Reinicia para a próxima vez

    def _start_quiz(self):
        """Inicia um quiz para o planeta atual"""
        self.state = QUIZ

        # Reinicia o rastreador de número de contagem regressiva
        self.last_countdown_number = 2

        # Seleciona uma pergunta aleatória do quiz para este planeta
        question_data = random.choice(self.current_planet.quiz_questions)

        # Inicia o quiz
        self.quiz.start_quiz(
            question_data["question"],
            question_data["options"],
            question_data["answer"]
        )

    def _start_transition(self):
        """Inicia a transição para o próximo planeta"""
        self.state = TRANSITION
        self.transition_time = 0

        # Incrementa o índice do planeta para avançar para o próximo (só acontece após passar no quiz)
        self.current_planet_index += 1

        # Garante que current_planet_index é válido
        if self.current_planet_index >= len(self.planets):
            # Jogador chegou ao fim de todos os planetas, mostra game over
            self.state = GAME_OVER
            if self.score > self.high_score_manager.get():
                self.high_score = self.score
                self.high_score_manager.save(self.score)
            return

        # Garante que estamos usando o planeta correto após o quiz
        self.current_planet = self.planets[self.current_planet_index]

        # NOVA mostra empolgação sobre o novo planeta
        self.nova.show_message(f"Entrando na órbita de {self.current_planet.name}!", "excited")

    def check_collision(self):
        # Verifica colisão com chão e teto
        if self.spacecraft.y <= 0 or self.spacecraft.y + self.spacecraft.HEIGHT >= SCREEN_HEIGHT - FLOOR_HEIGHT:
            return True

        # Verifica colisão com obstáculos
        for obstacle in self.obstacles:
            # Determina se estamos usando sprites e obtém a largura
            using_sprites = hasattr(obstacle, 'using_sprites') and obstacle.using_sprites
            obstacle_width = obstacle.top_width if using_sprites else obstacle.WIDTH
            
            # Verifica se há sobreposição horizontal (independente do tipo de obstáculo)
            horizontal_overlap = (self.spacecraft.x + self.spacecraft.WIDTH > obstacle.x and 
                                  self.spacecraft.x < obstacle.x + obstacle_width)
            
            if horizontal_overlap:
                # Limite superior da abertura
                upper_gap_limit = obstacle.gap_y - obstacle.GAP // 2
                
                # Limite inferior da abertura
                lower_gap_limit = obstacle.gap_y + obstacle.GAP // 2
                
                # Verifica colisão com obstáculo superior - a nave precisa estar totalmente abaixo do limite
                if self.spacecraft.y < upper_gap_limit:
                    return True

                # Verifica colisão com obstáculo inferior - a nave precisa estar totalmente acima do limite
                if self.spacecraft.y + self.spacecraft.HEIGHT > lower_gap_limit:
                    return True

        return False

    def draw(self):
        # Cria um fundo escuro base para o espaço
        screen.fill((0, 0, 20))

        # Desenha estrelas com base no planeta atual (estrelas de primeiro plano)
        for star in self.stars:
            # Desenha estrela com brilho atual
            color = (star["brightness"], star["brightness"], star["brightness"])
            pygame.draw.circle(screen, color, (int(star["x"]), int(star["y"])), star["size"])
            
        # Se o planeta tiver uma imagem de fundo, usa ela
        if self.current_planet.background_image:
            # Obtém o tamanho da imagem de fundo original
            bg_width, bg_height = self.current_planet.background_image.get_size()
            
            # Determina quantos tiles precisamos horizontalmente e verticalmente
            tiles_x = SCREEN_WIDTH // bg_width + 1  # +1 para cobrir qualquer espaço restante
            tiles_y = SCREEN_HEIGHT // bg_height + 1
            
            # Ladrilha o fundo em vez de esticar
            for y in range(tiles_y):
                for x in range(tiles_x):
                    screen.blit(self.current_planet.background_image, 
                               (x * bg_width, y * bg_height))
        else:
            # Aplica a cor de fundo do planeta como uma sobreposição transparente
            bg_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            bg_color = (*self.current_planet.background_color, 100)  # Adiciona alfa
            bg_overlay.fill(bg_color)
            screen.blit(bg_overlay, (0, 0))

        # Draw different screens based on game state
        if self.state == PLAYING or self.state == MENU or self.state == GAME_OVER or self.state == QUIZ_FAILURE:
            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(screen)

            # Desenha colecionáveis
            for collectible in self.collectibles:
                collectible.draw(screen)

            # Desenha chão/solo
            self.current_planet.draw_ground(screen, self.floor_x, SCREEN_HEIGHT)

            # Desenha nave espacial
            self.spacecraft.draw(screen)

            # Desenha o nome do planeta atual e a pontuação do jogador
            if self.state != MENU:
                # Informações do lado esquerdo
                display_name = PLANET_NAME_PT.get(self.current_planet.name, self.current_planet.name)
                planet_text = SMALL_FONT.render(f"Planeta: {display_name}", True, (255, 255, 255))
                screen.blit(planet_text, (20, 20))

                # Obtém limiar para o planeta atual
                current_threshold = self.level_progression_thresholds.get(
                    self.current_planet.name, 
                    10  # Limiar padrão
                )

                score_text = SMALL_FONT.render(f"Pontuação: {self.score}/{current_threshold}", True, (255, 255, 255))
                screen.blit(score_text, (20, 50))

                high_score_text = SMALL_FONT.render(f"Maior Pontuação: {self.high_score_manager.get()}", True, (255, 255, 255))
                screen.blit(high_score_text, (20, 80))

                # Desenha status da arma no centro superior se ativa (movido do lado direito)
                if self.weapon_active:
                    weapon_time = self.weapon_timer // 60  # Converte para segundos
                    weapon_text = SMALL_FONT.render(f"Arma Ativa: {weapon_time}s", True, (255, 100, 100))
                    screen.blit(weapon_text, (SCREEN_WIDTH // 2 - weapon_text.get_width() // 2, 20))

            # Desenha assistente NOVA AI (círculo azul)
            self.nova.draw(screen)
            # If quiz failed, overlay large countdown before resuming
            if self.state == QUIZ_FAILURE and self.quiz_failure_timer > 0:
                # Calculate countdown seconds
                countdown = math.ceil(self.quiz_failure_timer / 60)
                # Renderiza número grande da contagem regressiva
                text_surf = COUNTDOWN_FONT.render(str(countdown), True, (255, 255, 255))
                # Centraliza na tela
                screen.blit(
                    text_surf,
                    (
                        SCREEN_WIDTH // 2 - text_surf.get_width() // 2,
                        SCREEN_HEIGHT // 2 - text_surf.get_height() // 2
                    )
                )

            # Desenha tela de menu
            if self.state == MENU:
                # Sobreposição semitransparente
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))

                title_text = GAME_FONT.render("PROJECT BLUE NOVA", True, (255, 255, 255))
                subtitle_text = SMALL_FONT.render("Explorador do Sistema Solar", True, (200, 200, 255))
                instruction_text = GAME_FONT.render("Pressione ESPAÇO para Iniciar", True, (255, 255, 255))
                color_text = GAME_FONT.render(f"Nave: {COLOR_NAME_PT.get(self.spacecraft_color, self.spacecraft_color)}", True, (255, 255, 255))
                color_instruction = SMALL_FONT.render("Pressione C para mudar a cor", True, (255, 255, 255))

                screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 180))
                screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 220))
                screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 280))
                screen.blit(color_text, (SCREEN_WIDTH // 2 - color_text.get_width() // 2, 330))
                screen.blit(color_instruction, (SCREEN_WIDTH // 2 - color_instruction.get_width() // 2, 370))

                # Exibe controles
                controls_title = SMALL_FONT.render("Controles:", True, (255, 255, 255))
                controls_space = SMALL_FONT.render("ESPAÇO - Impulsionar", True, (200, 200, 200))
                controls_w = SMALL_FONT.render("W - Usar Arma (quando disponível)", True, (200, 200, 200))

                controls_y = SCREEN_HEIGHT - 120
                screen.blit(controls_title, (SCREEN_WIDTH // 2 - controls_title.get_width() // 2, controls_y))
                screen.blit(controls_space, (SCREEN_WIDTH // 2 - controls_space.get_width() // 2, controls_y + 30))
                screen.blit(controls_w, (SCREEN_WIDTH // 2 - controls_w.get_width() // 2, controls_y + 60))

            # Desenha tela de game over
            if self.state == GAME_OVER:
                # Sobreposição semitransparente
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))

                game_over_text = GAME_FONT.render("MISSÃO CONCLUÍDA", True, (255, 215, 0))
                score_text = GAME_FONT.render(f"Pontuação Final: {self.score}", True, (255, 255, 255))
                high_score_text = GAME_FONT.render(f"Maior Pontuação: {self.high_score_manager.get()}", True, (255, 255, 255))
                restart_text = GAME_FONT.render("Pressione ESPAÇO para iniciar nova missão", True, (255, 255, 255))

                # Calcula o planeta mais distante alcançado
                furthest_planet = self.planets[min(self.current_planet_index, len(self.planets) - 1)].name
                planet_text = GAME_FONT.render(f"Planeta mais distante: {furthest_planet}", True, (255, 255, 255))

                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
                screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 220))
                screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 270))
                screen.blit(planet_text, (SCREEN_WIDTH // 2 - planet_text.get_width() // 2, 320))
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

        elif self.state == TRANSITION:
            # Desenha tela de transição

            # Sobreposição semitransparente
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))  # Sobreposição mais escura para legibilidade do texto
            screen.blit(overlay, (0, 0))

            # Desenha nome do planeta de destino
            display_name = PLANET_NAME_PT.get(self.current_planet.name, self.current_planet.name)
            planet_title = GAME_FONT.render(f"Bem-vindo a {display_name}", True, (255, 255, 255))
            screen.blit(planet_title, (SCREEN_WIDTH // 2 - planet_title.get_width() // 2, 100))

            # Desenha informações de gravidade
            gravity_text = GAME_FONT.render(f"Gravidade: {self.current_planet.gravity_factor}% da Terra", True, (255, 255, 255))
            screen.blit(gravity_text, (SCREEN_WIDTH // 2 - gravity_text.get_width() // 2, 150))

            # Desenha texto informativo do planeta
            info_text = self.current_planet.get_info_text()
            # Quebra o texto para caber na tela
            wrapped_lines = []
            words = info_text.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                test_surface = SMALL_FONT.render(test_line, True, (255, 255, 255))
                if test_surface.get_width() < SCREEN_WIDTH - 100:
                    line = test_line
                else:
                    wrapped_lines.append(line)
                    line = word + " "
            wrapped_lines.append(line)  # Adiciona a última linha

            # Desenha texto quebrado
            for i, line in enumerate(wrapped_lines):
                line_surface = SMALL_FONT.render(line, True, (200, 200, 255))
                screen.blit(line_surface, (SCREEN_WIDTH // 2 - line_surface.get_width() // 2, 220 + i * 30))

            # Desenha indicador de progresso
            progress_text = SMALL_FONT.render(f"Planeta {self.current_planet_index + 1} de {len(self.planets)}", True, (180, 180, 180))
            screen.blit(progress_text, (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, 350))

            # Desenha prompt para continuar
            if self.transition_time > 60:  # Mostra apenas após 1 segundo
                continue_text = SMALL_FONT.render("Pressione ESPAÇO para continuar", True, (255, 255, 255))
                # Faz pulsar
                alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
                continue_text.set_alpha(alpha)
                screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 450))

        elif self.state == QUIZ:
            # Desenha quiz
            self.quiz.draw(screen)

        elif self.state == QUIZ_FAILURE:
            # Adiciona uma sobreposição semitransparente
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Preto semitransparente mais visível
            screen.blit(overlay, (0, 0))

            # Calcula número da contagem regressiva (2, 1)
            countdown_number = self.quiz_failure_timer // 60 + 1

            # Desenha número grande da contagem regressiva
            if countdown_number > 0:
                # Adiciona efeito de pulso - tamanho oscila levemente com base nos ticks
                pulse_factor = 1.0 + 0.15 * math.sin(pygame.time.get_ticks() * 0.01)
                pulse_size = int(180 * pulse_factor)

                # Usa a fonte global de contagem regressiva com o efeito de pulso
                countdown_font = pygame.font.Font(None, pulse_size)

                # Cor também pulsa levemente - efeito mais pronunciado
                color_pulse = int(255 * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.015)))
                countdown_text = countdown_font.render(str(countdown_number), True, (255, color_pulse, color_pulse))
                countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

                # Desenha com efeito de brilho aprimorado
                glow_size = 12
                for offset_x in range(-glow_size, glow_size + 1, 3):
                    for offset_y in range(-glow_size, glow_size + 1, 3):
                        if offset_x == 0 and offset_y == 0:
                            continue
                        # Calcula distância para efeito de fade do brilho
                        distance = math.sqrt(offset_x**2 + offset_y**2)
                        alpha = int(120 * (1 - distance/glow_size))
                        if alpha <= 0:
                            continue

                        glow_rect = countdown_rect.move(offset_x, offset_y)
                        glow_text = countdown_font.render(str(countdown_number), True, (80, 80, 220, alpha))
                        screen.blit(glow_text, glow_rect)

                # Desenha texto principal
                screen.blit(countdown_text, countdown_rect)

                # Desenha texto "Retornando..." com efeito de pulso
                resume_font = pygame.font.Font(None, 42)
                alpha_pulse = int(255 * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.008)))
                resume_text = resume_font.render("Retornando à órbita...", True, (255, 255, 255))
                resume_text.set_alpha(alpha_pulse)
                resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
                screen.blit(resume_text, resume_rect)

        # Sempre desenha o assistente NOVA AI por cima
        self.nova.draw(screen)

def main():
    # Cria e inicia o jogo
    game = Game()

    # Loop do jogo
    while True:
        game.handle_events()
        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
