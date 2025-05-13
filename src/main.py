import pygame
import sys
import random
import math
from src.spacecraft import Spacecraft
from src.obstacle import Obstacle
from src.collectible import Collectible
from src.planet import Planet
from src.highscore import PlanetTracker
from src.nova_ai import NovaAI
from src.quiz import Quiz

# Importa módulos refatorados
from src.config import *
from src.sound_manager import SoundManager
from src.state_manager import StateManager
from src.collision_manager import CollisionManager
from src.visual_effects import VisualEffectsManager

# Inicializa o pygame
pygame.init()
pygame.mixer.init()

# Configura a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Project Blue Nova: Explorador do Sistema Solar")
clock = pygame.time.Clock()

# Inicializa as fontes após o pygame ser inicializado
import src.config as config
config.GAME_FONT = pygame.font.Font(None, config.GAME_FONT_SIZE)
config.SMALL_FONT = pygame.font.Font(None, config.SMALL_FONT_SIZE)
config.COUNTDOWN_FONT = pygame.font.Font(None, config.COUNTDOWN_FONT_SIZE)

# Define os dados dos planetas para a progressão do jogo
def create_planet_data():
    """Cria dados para todos os planetas no jogo"""
    planet_data = [
        {
            "name": "Earth",
            "gravity_factor": 100,  # Gravidade base (g = 1.0)
            "background_color": (25, 25, 112),  # Azul meia-noite
            "obstacle_count": 6,
            "quiz_questions": [
                {
                    "question": "Qual percentual da Terra é coberto por água?",
                    "options": ["51%", "61%", "71%", "81%"],
                    "answer": 2  # 71%
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
            "gravity_factor": 40,  # g = 0.4
            "background_color": (70, 50, 40),  # Marrom
            "obstacle_count": 2,
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
            "gravity_factor": 90,  # g = 0.9
            "background_color": (140, 90, 40),  # Âmbar
            "obstacle_count": 4,
            "quiz_questions": [
                {
                    "question": "Vênus gira em qual direção?",
                    "options": ["Igual à Terra", "Oposta à Terra", "Não gira", "Muda aleatoriamente"],
                    "answer": 1  # Oposta à Terra (retrógrado)
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
            "gravity_factor": 40,  # g = 0.4
            "background_color": (150, 70, 40),  # Vermelho ferrugem
            "obstacle_count": 3,
            "quiz_questions": [
                {
                    "question": "O que dá a Marte sua cor vermelha distintiva?",
                    "options": ["Vida vegetal", "Óxido de ferro (ferrugem)", "Dióxido de carbono", "Luz solar refletida"],
                    "answer": 1  # Óxido de ferro
                },
                {
                    "question": "Quantas luas Marte possui?",
                    "options": ["Nenhuma", "Uma", "Duas", "Três"],
                    "answer": 2  # Duas (Fobos e Deimos)
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
            "gravity_factor": 240,  # g = 2.4
            "background_color": (210, 140, 70),  # Bronzeado
            "obstacle_count": 20,
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
            "gravity_factor": 110,  # g = 1.1
            "background_color": (180, 150, 100),  # Bronzeado claro
            "obstacle_count": 15,
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
            "gravity_factor": 16,  # g = 0.16
            "background_color": (20, 20, 20),  # Cinza muito escuro
            "obstacle_count": 2,
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
            "gravity_factor": 90,  # g = 0.9
            "background_color": (140, 210, 210),  # Ciano
            "obstacle_count": 12,
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
            "gravity_factor": 110,  # g = 1.1
            "background_color": (30, 50, 180),  # Azul profundo
            "obstacle_count": 11,
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
        # Plutão removido da progressão principal
    ]

    return planet_data

class Game:
    def __init__(self):
        # Estado do jogo
        self.score = 0
        self.planet_tracker = PlanetTracker()
        self.last_planet = self.planet_tracker.get_last_planet()
        self.furthest_planet = self.planet_tracker.get_furthest_planet()
        self.furthest_planet_index = 0  # Rastreia o planeta mais distante alcançado

        # Sistema de vidas
        self.lives = SPACECRAFT_MAX_LIVES
        self.invulnerable = False
        self.invulnerable_timer = 0

        # Inicializa o estado interno antes da propriedade ser usada
        self._state = MENU

        # Controle do som de boas-vindas
        self.welcome_sound_played = False
        self.current_welcome_sound = None
        self.welcome_sound_timer = 0

        # Configuração dos planetas
        self.planet_data = create_planet_data()
        self.planets = [Planet(data["name"],
                             data["gravity_factor"],
                             data["background_color"],
                             data["obstacle_count"],
                             data["quiz_questions"])
                      for data in self.planet_data]

        # Encontra o índice do planeta salvo e do planeta mais distante
        self.current_planet_index = 0
        for i, planet in enumerate(self.planets):
            if planet.name.lower() == self.last_planet.lower():
                self.current_planet_index = i
                break
                
        # Encontra o índice do planeta mais distante
        for i, planet in enumerate(self.planets):
            if planet.name.lower() == self.furthest_planet.lower():
                self.furthest_planet_index = i
                break
        
        self.current_planet = self.planets[self.current_planet_index]

        # Configuração da espaçonave
        self.spacecraft_color = "silver"  # Cor padrão
        self.spacecraft = Spacecraft(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.spacecraft_color)
        self.available_colors = list(Spacecraft.COLORS.keys())
        self.current_color_index = 0

        # Elementos do jogo
        self.obstacles = []
        self.collectibles = []
        # Inicializa o rastreamento de tempo
        self.last_obstacle_time = pygame.time.get_ticks() - 2000
        self.last_collectible_time = pygame.time.get_ticks()
        self.floor_x = 0

        # Temporização de obstáculos e colecionáveis
        self.obstacle_spawn_rate = DEFAULT_OBSTACLE_SPAWN_RATE
        self.collectible_spawn_rate = DEFAULT_COLLECTIBLE_SPAWN_RATE

        # Progressão do jogo
        self.obstacle_speed = 3
        self.weapon_active = False
        self.weapon_timer = 0

        # Inicializa o assistente NOVA AI
        self.nova = NovaAI(SCREEN_WIDTH, SCREEN_HEIGHT, PLANET_NAME_PT)

        # Inicializa o sistema de quiz
        self.quiz = Quiz(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Configurações de progressão do jogo
        self.difficulty_multiplier = 1.0

        # Inicializa os gerenciadores
        self.sound_manager = SoundManager()
        self.visual_effects = VisualEffectsManager(self)
        self.collision_manager = CollisionManager(self)

        # Inicializa o gerenciador de estado por último para evitar dependências circulares
        self.state_manager = StateManager(self)

        # Inicializa o estado do jogo (usa o valor _state existente)
        self.state_manager.change_state(MENU)

        # Configurações de controle
        self.space_held = False
        self.control_mode = CONTROL_MODE_HOLD  # Padrão alterado para HOLD

    @property
    def state(self):
        """Obtém o estado atual do jogo"""
        return self._state

    @state.setter
    def state(self, new_state):
        """Define o estado do jogo e atualiza o gerenciador de estado"""
        self._state = new_state
        # Não chamamos state_manager.change_state aqui para evitar recursão infinita
        # quando o state_manager altera o estado

    def reset(self, new_planet=False):
        """Reseta o jogo, opcionalmente mudando para um novo planeta"""
        self.state_manager.change_state(PLAYING)
        self.state = PLAYING  # Mantém sincronizado com o gerenciador de estado
        self.weapon_active = False
        self.weapon_timer = 0

        # Para todos os sons com fadeout suave
        self.sound_manager.stop_thrust(SOUND_FADEOUT_TIME)
        self.sound_manager.hitting_obstacle_sound.fadeout(SOUND_FADEOUT_TIME)

        # Lida com os sons de boas-vindas com base no tipo de reset
        if not new_planet:
            # Para todos os sons de boas-vindas no reset completo
            for sound in self.sound_manager.welcome_sounds.values():
                sound.fadeout(200)
            self.current_welcome_sound = None
            self.welcome_sound_timer = 0

        if new_planet:
            # Reseta a pontuação para o novo planeta
            self.score = 0
            # Atualiza a dificuldade com base no índice do planeta
            self.difficulty_multiplier = 1.0 + (self.current_planet_index * 0.1)
            # Não reseta as vidas ao mudar de planeta
            
            # Salva o planeta atual e atualiza o planeta mais distante se necessário
            self.planet_tracker.save(self.current_planet.name.lower(), update_furthest=True)
        else:
            # Começa do zero
            self.score = 0
            self.current_planet_index = 0
            self.current_planet = self.planets[self.current_planet_index]
            self.difficulty_multiplier = 1.0
            # Reseta as vidas para o máximo ao iniciar um novo jogo
            self.reset_lives()
            
            # Salva o planeta atual (mercurio) - não atualiza o planeta mais distante ao resetar
            self.planet_tracker.save(self.current_planet.name.lower(), update_furthest=False)

            # Toca o som de boas-vindas da Terra ao iniciar/reiniciar
            if self.current_planet.name in self.sound_manager.welcome_sounds:
                # Para quaisquer sons tocando primeiro
                for sound in self.sound_manager.welcome_sounds.values():
                    sound.fadeout(100)

                # Pequeno atraso antes de tocar o som de boas-vindas da Terra
                pygame.time.delay(200)

                # Armazena referência ao som atual
                self.current_welcome_sound = self.sound_manager.welcome_sounds[self.current_planet.name]
                self.current_welcome_sound.play()
                # Define o temporizador com base na duração do som (em milissegundos)
                self.welcome_sound_timer = int(self.current_welcome_sound.get_length() * 1000)
                self.welcome_sound_played = True

        # Reseta a posição da espaçonave
        self.spacecraft = Spacecraft(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.spacecraft_color)

        # Limpa todos os obstáculos e colecionáveis
        self.obstacles = []
        self.collectibles = []
        # Inicializa o rastreamento de tempo para geração imediata de obstáculos
        self.last_obstacle_time = pygame.time.get_ticks() - 2000
        self.last_collectible_time = pygame.time.get_ticks()
        # Reseta a posição do chão
        self.floor_x = 0

        # Dificuldade base ajustada pelo planeta e progressão
        self.obstacle_speed = 3 * self.difficulty_multiplier
        self.obstacle_spawn_rate = int(DEFAULT_OBSTACLE_SPAWN_RATE / self.difficulty_multiplier)
        self.collectible_spawn_rate = int(DEFAULT_COLLECTIBLE_SPAWN_RATE / self.difficulty_multiplier)

        # NOVA deve alertar sobre a gravidade
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
                    # Passa eventos para o sistema de quiz apenas se estiver no estado QUIZ
                    if self.state == QUIZ:
                        self.quiz.handle_event(event)
                else:
                    if event.key == pygame.K_SPACE:
                        if self.state == MENU:
                            self.reset()
                        elif self.state == PLAYING:
                            # Empuxo único ao pressionar
                            self.spacecraft.thrust()
                            # Toca o som de empuxo do motor
                            self.sound_manager.play_thrust()
                            # Habilita empuxo contínuo se estiver no modo de segurar
                            if self.control_mode == CONTROL_MODE_HOLD:
                                self.space_held = True
                        elif self.state == GAME_OVER:
                            # Reseta a flag welcome_sound_played
                            self.welcome_sound_played = False
                            self.reset()
                        elif self.state == TRANSITION:
                            # Pula a transição e força o início no novo planeta
                            self.reset(new_planet=True)
                    
                    # Muda a cor da espaçonave com C no menu, alterna o modo de controle no jogo
                    if event.key == pygame.K_c:
                        if self.state == MENU:
                            self.current_color_index = (self.current_color_index + 1) % len(self.available_colors)
                            self.spacecraft_color = self.available_colors[self.current_color_index]
                            self.spacecraft.change_color(self.spacecraft_color)
                        elif self.state == PLAYING:
                            # Alterna o modo de controle entre flappy e segurar
                            self.control_mode = CONTROL_MODE_HOLD if self.control_mode == CONTROL_MODE_FLAPPY else CONTROL_MODE_FLAPPY
                            mode_name = "Hold" if self.control_mode == CONTROL_MODE_HOLD else "Flappy"
                            
                            # Atualiza as cores da chama da espaçonave para o efeito de empuxo
                            if self.control_mode == CONTROL_MODE_HOLD:
                                # Gradiente de amarelo para laranja para vermelho
                                self.spacecraft.flame_colors = [(255, 255, 0), (255, 165, 0), (255, 69, 0)]
                            else:
                                # Chama de cor única
                                self.spacecraft.flame_colors = []
                            self.spacecraft.update_image()
                            self.nova.show_message(f"Modo de controle: {mode_name}", "info")
                    
                    # Ativa a arma com W se disponível
                    if event.key == pygame.K_w and self.state == PLAYING and self.weapon_active:
                        self._use_weapon()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # Para o empuxo contínuo ao soltar
                    self.space_held = False
                    # Diminui o som de empuxo do motor
                    self.sound_manager.stop_thrust(SOUND_FADEOUT_TIME)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    if self.state == QUIZ or self.state == QUIZ_FAILURE:
                        # Passa eventos para o sistema de quiz apenas se estiver no estado QUIZ
                        if self.state == QUIZ:
                            self.quiz.handle_event(event)
                    else:
                        if self.state == MENU:
                            self.reset()
                        elif self.state == PLAYING:
                            self.spacecraft.thrust()
                            self.sound_manager.play_thrust()
                        elif self.state == GAME_OVER:
                            # Reseta a flag welcome_sound_played
                            self.welcome_sound_played = False
                            self.reset()
                        elif self.state == TRANSITION:
                            # Se estiver em transição e o som estiver tocando, permite pular mas continua o som com volume reduzido
                            if self.welcome_sound_timer > 0 and self.current_welcome_sound:
                                self.sound_manager.adjust_welcome_volume(self.current_planet.name, 0.3)
                            # Força a conclusão do temporizador de som para permitir prosseguir
                            self.welcome_sound_timer = 0
                            # Pula a transição e força o início no novo planeta
                            if self.state_manager.transition_time >= TRANSITION_DURATION // 2:  # Permite pular apenas após metade da transição
                                self.reset(new_planet=True)

    def _use_weapon(self):
        """Usa a arma para destruir obstáculos"""
        if not self.weapon_active:
            return

        # Encontra o obstáculo mais próximo à frente da espaçonave
        target_obstacle = None
        min_distance = float('inf')

        # Define a posição x do corpo da espaçonave
        spacecraft_body_x = self.spacecraft.x + self.spacecraft.flame_extent

        for obstacle in self.obstacles:
            # Mira apenas em obstáculos à frente do corpo da espaçonave
            if obstacle.x > spacecraft_body_x:
                distance = obstacle.x - spacecraft_body_x
                if distance < min_distance:
                    min_distance = distance
                    target_obstacle = obstacle

        if target_obstacle:
            # Remove o obstáculo e concede pontos
            self.obstacles.remove(target_obstacle)
            self.score += 2
            self.nova.show_message("Obstáculo destruído!", "alert")
            
            # Verifica a progressão para o próximo planeta com base na nova pontuação
            current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
                self.current_planet.name,
                10  # Limite padrão para planetas não especificados
            )
            if self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                next_planet_en = self.planets[self.current_planet_index + 1].name
                next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
                self.nova.show_message(f"Navegação automática engajada! Indo para {next_planet_pt}!", "excited")
                
                # Atualiza o planeta mais distante alcançado na memória
                next_planet = self.planets[self.current_planet_index + 1].name.lower()
                self.furthest_planet_index = max(self.furthest_planet_index, self.current_planet_index + 1)
                
                # Salva o planeta atual e atualiza o planeta mais distante
                self.planet_tracker.save(next_planet, update_furthest=True)
                
                # Inicia o quiz para avanço do planeta
                self.state_manager.start_quiz()

    def lose_life(self):
        """Reduz o número de vidas e verifica se o jogo acabou"""
        if not self.invulnerable:
            self.lives -= 1

            # Contagem de acertos mais intuitiva (começa com 3 vidas, 4º acerto = fim de jogo)
            hit_count = SPACECRAFT_MAX_LIVES - self.lives

            # Verifica se todas as vidas foram perdidas
            if hit_count >= 4:  # 4 acertos = fim de jogo
                self.lives = 0  # Garante que não fique negativo
                self.nova.show_message("Dano crítico! Fim de jogo!", "alert")
                self.state_manager.change_state(GAME_OVER)
                self.state = GAME_OVER  # Mantém sincronizado com o gerenciador de estado
                # Toca o som de explosão no fim de jogo
                self.sound_manager.stop_thrust(100)  # Garante que o som de empuxo pare rapidamente
                self.sound_manager.hitting_obstacle_sound.fadeout(100)  # Para o som de colisão se estiver tocando
                self.sound_manager.play_explosion()
                return False  # Quarta colisão causa fim de jogo
            elif hit_count == 3:  # 3 acertos = última vida
                self.nova.show_message("Atenção: Última vida restante!", "alert")
            elif hit_count == 2:  # 2 acertos = penúltima vida
                self.nova.show_message("Atenção: Duas vidas restantes!", "alert")

            return True  # Ainda tem vidas
        return True  # Não perdeu vida devido à invulnerabilidade

    def add_life(self):
        """Adiciona uma vida, até o máximo permitido"""
        if self.lives < SPACECRAFT_MAX_LIVES:
            self.lives += 1
            self.nova.show_message("Vida extra adquirida!", "excited")
            return True
        return False  # Já está no máximo de vidas

    def reset_lives(self):
        """Reseta as vidas para o valor máximo"""
        self.lives = SPACECRAFT_MAX_LIVES
        self.invulnerable = False
        self.invulnerable_timer = 0

    def is_invulnerable(self):
        """Retorna o estado atual de invulnerabilidade"""
        return self.invulnerable

    def update(self):
        try:
            # Atualiza os efeitos visuais se disponíveis
            if hasattr(self, 'visual_effects'):
                self.visual_effects.update()

            # Atualiza a NOVA AI se disponível
            if hasattr(self, 'nova'):
                self.nova.update()

            # Atualiza o temporizador do som de boas-vindas
            if hasattr(self, 'welcome_sound_timer') and self.welcome_sound_timer > 0:
                self.welcome_sound_timer -= 16  # Aproximadamente 16ms por quadro a 60fps

                # Verifica se o usuário tenta pular a introdução (pressionando espaço)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and self.state == TRANSITION:
                    # Não para completamente o som de boas-vindas, apenas reduz o volume
                    if hasattr(self, 'current_welcome_sound') and self.current_welcome_sound and hasattr(self, 'sound_manager'):
                        self.sound_manager.adjust_welcome_volume(self.current_planet.name, 0.3)
                    self.welcome_sound_timer = 0  # Permite prosseguir com o jogo

            # Atualiza o temporizador de invulnerabilidade
            if hasattr(self, 'invulnerable') and self.invulnerable:
                self.invulnerable_timer -= 1
                if self.invulnerable_timer <= 0:
                    self.invulnerable = False
                    if hasattr(self, 'nova'):
                        self.nova.show_message("Sistemas de escudo restaurados", "normal")

            # Atualiza o gerenciador de estado
            if hasattr(self, 'state_manager'):
                self.state_manager.update()
        except AttributeError as e:
            # Imprime o erro para fins de depuração
            print(f"Erro na atualização: {e}")
            # Continua o loop do jogo

        if self.state == PLAYING:
            try:
                if hasattr(self, 'spacecraft') and hasattr(self, 'current_planet'):
                    # Atualiza a espaçonave com a gravidade do planeta atual e os limites da tela
                    self.spacecraft.update(self.current_planet.gravity, SCREEN_HEIGHT, FLOOR_HEIGHT)

                    # Empuxo contínuo enquanto o espaço é segurado no modo de segurar
                    if hasattr(self, 'control_mode') and hasattr(self, 'space_held') and self.control_mode == CONTROL_MODE_HOLD and self.space_held:
                        # Aplica pequeno empuxo contínuo (20% da potência de empuxo)
                        cont = self.spacecraft.thrust_power * self.spacecraft.thrust_multiplier * 0.2
                        self.spacecraft.velocity -= cont
                        # Mantém o efeito de chama
                        self.spacecraft.last_thrust_time = pygame.time.get_ticks()
                        # Garante que o som de empuxo continue tocando
                        if hasattr(self, 'sound_manager'):
                            if not pygame.mixer.get_busy() or not self.sound_manager.engine_thrust_sound.get_num_channels():
                                self.sound_manager.play_thrust()

                # Gera obstáculos
                if hasattr(self, 'last_obstacle_time') and hasattr(self, 'obstacle_spawn_rate'):
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_obstacle_time > self.obstacle_spawn_rate:
                        # Gera obstáculo
                        self._generate_obstacle()
                        self.last_obstacle_time = current_time

                # Gera colecionáveis
                if hasattr(self, 'last_collectible_time') and hasattr(self, 'collectible_spawn_rate'):
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_collectible_time > self.collectible_spawn_rate:
                        # Gera colecionável
                        self._generate_collectible()
                        self.last_collectible_time = current_time

                # Atualiza obstáculos e verifica pontuação
                if hasattr(self, 'obstacles'):
                    for obstacle in self.obstacles:
                        obstacle.update()

                        # Pontua ao passar por um obstáculo
                        if hasattr(self, 'spacecraft') and not obstacle.scored and obstacle.x + obstacle.WIDTH < self.spacecraft.x:
                            self.score += 1
                            obstacle.scored = True

                            # Verifica a progressão automática
                            if hasattr(self, 'current_planet') and hasattr(self, 'state_manager'):
                                current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
                                    self.current_planet.name,
                                    10  # Limite padrão
                                )

                                # Verifica se o limite de pontuação foi atingido para progressão automática
                                if hasattr(self, 'planets') and self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                                    # NOVA anuncia progressão automática
                                    if hasattr(self, 'nova'):
                                        next_planet_en = self.planets[self.current_planet_index + 1].name
                                        next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
                                        self.nova.show_message(f"Navegação automática engajada! Indo para {next_planet_pt}!", "excited")

                                    # Atualiza o planeta mais distante alcançado
                                    next_planet = self.planets[self.current_planet_index + 1].name.lower()
                                    self.furthest_planet_index = max(self.furthest_planet_index, self.current_planet_index + 1)
                                    
                                    # Salva o planeta atual e atualiza o planeta mais distante
                                    self.planet_tracker.save(next_planet, update_furthest=True)
                                    
                                    # Inicia o quiz sem incrementar o índice do planeta ainda - deixa o quiz lidar com a progressão
                                    self.state_manager.start_quiz()

                # Atualiza colecionáveis e verifica colisão
                if hasattr(self, 'collision_manager') and hasattr(self, 'collectibles'):
                    # Verifica colisões com colecionáveis
                    self.collision_manager.check_collectible_collisions()

                    # Atualiza colecionáveis
                    for collectible in list(self.collectibles):
                        collectible.update()
                        if hasattr(self, 'obstacle_speed'):
                            collectible.x -= self.obstacle_speed  # Move na mesma velocidade dos obstáculos

                # Atualiza o temporizador da arma
                if hasattr(self, 'weapon_active') and self.weapon_active:
                    self.weapon_timer -= 1
                    if self.weapon_timer <= 0:
                        self.weapon_active = False
                        if hasattr(self, 'nova'):
                            self.nova.show_message("Sistemas defensivos offline", "normal")

                # Remove obstáculos e colecionáveis fora da tela
                if hasattr(self, 'obstacles'):
                    self.obstacles = [obs for obs in self.obstacles if obs.x > -obs.WIDTH]
                if hasattr(self, 'collectibles'):
                    self.collectibles = [col for col in self.collectibles if col.x > -col.WIDTH]

                # Verifica colisões
                if hasattr(self, 'collision_manager'):
                    collision_result = self.collision_manager.check_collisions()
                    if collision_result is not False and hasattr(self, 'sound_manager'):  # Se ocorreu colisão
                        # Toca o som de colisão com obstáculo
                        self.sound_manager.play_collision()
                        # Fim de jogo já é tratado em lose_life

                # Move o chão
                if hasattr(self, 'floor_x') and hasattr(self, 'obstacle_speed'):
                    self.floor_x = (self.floor_x - self.obstacle_speed) % 800

            except AttributeError as e:
                print(f"Erro na atualização do estado PLAYING: {e}")
            
    def _generate_obstacle(self):
        """Gera um novo obstáculo"""
        # Define o vão fixo entre os obstáculos
        gap_size = Obstacle.GAP

        # Calcula os valores mínimo e máximo para o centro do vão
        min_gap_center_y = gap_size // 2
        max_gap_center_y = SCREEN_HEIGHT - FLOOR_HEIGHT - (gap_size // 2)

        # Lida com casos extremos com constantes extremas
        if min_gap_center_y > max_gap_center_y:
            target_y = ((gap_size // 2) + (SCREEN_HEIGHT - FLOOR_HEIGHT - (gap_size // 2))) // 2

            # Define limites absolutos para fixação
            abs_min_y = gap_size // 2
            abs_max_y = SCREEN_HEIGHT - FLOOR_HEIGHT - (gap_size // 2)

            if abs_min_y > abs_max_y:  # ex: gap_size > altura jogável
                # Apenas usa o meio da altura jogável da tela
                target_y = (SCREEN_HEIGHT - FLOOR_HEIGHT) // 2
            else:
                # Fixa target_y ao intervalo fisicamente possível
                target_y = max(abs_min_y, min(target_y, abs_max_y))

            min_gap_center_y = target_y
            max_gap_center_y = target_y

        # Gera posição y aleatória para o centro do vão
        gap_y = random.randint(min_gap_center_y, max_gap_center_y)

        # Seleciona aleatoriamente o tipo de obstáculo
        obstacle_type = random.choice(list(Obstacle.TYPES.keys()))

        # Cria novo obstáculo
        new_obstacle = Obstacle(SCREEN_WIDTH, gap_y, self.obstacle_speed, obstacle_type, SCREEN_HEIGHT)
        self.obstacles.append(new_obstacle)

        # Ocasionalmente, faz a NOVA alertar sobre obstáculos
        if random.random() < 0.3:  # 30% de chance
            pass

    def _generate_collectible(self):
        """Gera um novo colecionável"""
        # Coloca o colecionável em um local seguro
        x = SCREEN_WIDTH
        y = random.randint(100, SCREEN_HEIGHT - FLOOR_HEIGHT - 50)

        # Determina o tipo de colecionável (1% de chance para vida, 10% para arma, resto dados)
        collectible_type = "data"
        rand_val = random.random()
        if rand_val < 0.01:  # 1% de chance para vida
            collectible_type = "life"
        elif rand_val < 0.11 and not self.weapon_active:  # 10% de chance para arma
            collectible_type = "weapon"

        self.collectibles.append(Collectible(x, y, collectible_type))

    def draw(self):
        # Desenha o fundo
        self.visual_effects.draw_background(screen, self.current_planet)

        # Desenha o conteúdo com base no estado do jogo
        if self.state == PLAYING or self.state == MENU or self.state == GAME_OVER or self.state == QUIZ_FAILURE:
            # Desenha obstáculos
            for obstacle in self.obstacles:
                obstacle.draw(screen)

            # Desenha colecionáveis
            for collectible in self.collectibles:
                collectible.draw(screen)

            # Desenha o chão/solo
            self.current_planet.draw_ground(screen, self.floor_x, SCREEN_HEIGHT)

            # Desenha a espaçonave (com efeito de invulnerabilidade se aplicável)
            self.spacecraft.draw(screen, self.invulnerable)

            # Desenha o nome do planeta atual e a pontuação do jogador
            if self.state != MENU:
                # Informações do lado esquerdo
                display_name = PLANET_NAME_PT.get(self.current_planet.name, self.current_planet.name)
                planet_text = config.SMALL_FONT.render(f"Planeta: {display_name}", True, (255, 255, 255))
                screen.blit(planet_text, (20, 20))
                
                # Mostra o planeta mais distante alcançado
                furthest_planet = self.planets[self.furthest_planet_index].name
                furthest_planet_pt = PLANET_NAME_PT.get(furthest_planet, furthest_planet)
                furthest_text = config.SMALL_FONT.render(f"Mais distante: {furthest_planet_pt}", True, (255, 215, 0))
                screen.blit(furthest_text, (20, 50))

                # Obtém o limite para o planeta atual
                current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
                    self.current_planet.name,
                    10  # Limite padrão
                )

                score_text = config.SMALL_FONT.render(f"Pontuação: {self.score}/{current_threshold}", True, (255, 255, 255))
                screen.blit(score_text, (20, 80))

                # Desenha o indicador de vidas
                lives_text = config.SMALL_FONT.render(f"Vidas:", True, (255, 255, 255))
                screen.blit(lives_text, (20, 110))

                # Desenha os ícones de vida
                self.visual_effects.draw_life_icons(screen, self.lives, SPACECRAFT_MAX_LIVES, self.spacecraft_color)

                # Desenha o status da arma no centro superior se ativa
                if self.weapon_active:
                    weapon_time = self.weapon_timer // 60  # Converte para segundos
                    weapon_text = config.SMALL_FONT.render(f"Arma Ativa: {weapon_time}s", True, (255, 100, 100))
                    screen.blit(weapon_text, (SCREEN_WIDTH // 2 - weapon_text.get_width() // 2, 20))

            # Desenha o assistente NOVA AI
            self.nova.draw(screen)
            
            # Se o quiz falhou, sobrepõe uma contagem regressiva grande antes de retomar
            if self.state == QUIZ_FAILURE and self.state_manager.quiz_failure_timer > 0:
                countdown = math.ceil(self.state_manager.quiz_failure_timer / 60)
                self.visual_effects.draw_countdown(screen, countdown)

            # Desenha a tela de menu
            if self.state == MENU:
                self._draw_menu_screen(screen)

            # Desenha a tela de fim de jogo
            if self.state == GAME_OVER:
                self._draw_game_over_screen(screen)

        elif self.state == TRANSITION:
            self._draw_transition_screen(screen)

        elif self.state == QUIZ:
            # Desenha o quiz
            self.quiz.draw(screen)

            # Sempre desenha o assistente NOVA AI por cima também no estado de quiz
            self.nova.draw(screen)

        elif self.state == QUIZ_FAILURE:
            self._draw_quiz_failure_screen(screen)

        # Sempre desenha o assistente NOVA AI por cima
        self.nova.draw(screen)

    def _draw_menu_screen(self, screen):
        """Desenha a tela de menu"""
        # Sobreposição semitransparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title_text = config.GAME_FONT.render("PROJECT BLUE NOVA", True, (255, 255, 255))
        subtitle_text = config.SMALL_FONT.render("Explorador do Sistema Solar", True, (200, 200, 255))
        instruction_text = config.GAME_FONT.render("Pressione ESPAÇO para Iniciar", True, (255, 255, 255))
        color_text = config.GAME_FONT.render(f"Nave: {COLOR_NAME_PT.get(self.spacecraft_color, self.spacecraft_color)}", True, (255, 255, 255))
        color_instruction = config.SMALL_FONT.render("Pressione C para mudar a cor", True, (255, 255, 255))

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 180))
        screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 220))
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 280))
        screen.blit(color_text, (SCREEN_WIDTH // 2 - color_text.get_width() // 2, 330))
        screen.blit(color_instruction, (SCREEN_WIDTH // 2 - color_instruction.get_width() // 2, 370))

        # Mostra os controles
        controls_title = config.SMALL_FONT.render("Controles:", True, (255, 255, 255))
        controls_space = config.SMALL_FONT.render("ESPAÇO - Impulsionar", True, (200, 200, 200))
        controls_w = config.SMALL_FONT.render("W - Usar Arma (quando disponível)", True, (200, 200, 200))

        controls_y = SCREEN_HEIGHT - 120
        screen.blit(controls_title, (SCREEN_WIDTH // 2 - controls_title.get_width() // 2, controls_y))
        screen.blit(controls_space, (SCREEN_WIDTH // 2 - controls_space.get_width() // 2, controls_y + 30))
        screen.blit(controls_w, (SCREEN_WIDTH // 2 - controls_w.get_width() // 2, controls_y + 60))

    def _draw_game_over_screen(self, screen):
        """Desenha a tela de fim de jogo"""
        # Sobreposição semitransparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        game_over_text = config.GAME_FONT.render("MISSÃO CONCLUÍDA", True, (255, 215, 0))
        score_text = config.GAME_FONT.render(f"Pontuação Final: {self.score}", True, (255, 255, 255))
        restart_text = config.GAME_FONT.render("Pressione ESPAÇO para iniciar nova missão", True, (255, 255, 255))

        # Calcula o planeta mais distante alcançado
        furthest_planet = self.planets[min(self.current_planet_index, len(self.planets) - 1)].name
        planet_text = config.GAME_FONT.render(f"Planeta mais distante: {furthest_planet}", True, (255, 255, 255))

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 220))
        screen.blit(planet_text, (SCREEN_WIDTH // 2 - planet_text.get_width() // 2, 320))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

    def _draw_transition_screen(self, screen):
        """Desenha a tela de transição"""
        # Sobreposição semitransparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Sobreposição mais escura para legibilidade do texto
        screen.blit(overlay, (0, 0))

        # Desenha o nome do planeta de destino
        display_name = PLANET_NAME_PT.get(self.current_planet.name, self.current_planet.name)
        planet_title = config.GAME_FONT.render(f"Bem-vindo a {display_name}", True, (255, 255, 255))
        screen.blit(planet_title, (SCREEN_WIDTH // 2 - planet_title.get_width() // 2, 100))

        # Desenha informações de gravidade
        gravity_text = config.GAME_FONT.render(f"Gravidade: {self.current_planet.gravity_factor}% da Terra", True, (255, 255, 255))
        screen.blit(gravity_text, (SCREEN_WIDTH // 2 - gravity_text.get_width() // 2, 150))

        # Desenha o texto informativo do planeta
        info_text = self.current_planet.get_info_text()
        # Quebra o texto para caber na tela
        wrapped_lines = []
        words = info_text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            test_surface = config.SMALL_FONT.render(test_line, True, (255, 255, 255))
            if test_surface.get_width() < SCREEN_WIDTH - 100:
                line = test_line
            else:
                wrapped_lines.append(line)
                line = word + " "
        wrapped_lines.append(line)  # Adiciona a última linha

        # Desenha o texto quebrado
        for i, line in enumerate(wrapped_lines):
            line_surface = config.SMALL_FONT.render(line, True, (200, 200, 255))
            screen.blit(line_surface, (SCREEN_WIDTH // 2 - line_surface.get_width() // 2, 220 + i * 30))

        # Desenha o indicador de progresso
        progress_text = config.SMALL_FONT.render(f"Planeta {self.current_planet_index + 1} de {len(self.planets)}", True, (180, 180, 180))
        screen.blit(progress_text, (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, 350))

        # Desenha o prompt para continuar
        if self.state_manager.transition_time > 60:  # Mostra apenas após 1 segundo
            continue_text = config.SMALL_FONT.render("Pressione ESPAÇO para continuar", True, (255, 255, 255))
            # Faz pulsar
            alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
            continue_text.set_alpha(alpha)
            screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 450))

    def _draw_quiz_failure_screen(self, screen):
        """Desenha a tela de falha no quiz com contagem regressiva"""
        # Adiciona sobreposição semitransparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Preto semitransparente mais visível
        screen.blit(overlay, (0, 0))

        # Calcula o número da contagem regressiva
        countdown_number = self.state_manager.quiz_failure_timer // 60 + 1

        # Desenha o número grande da contagem regressiva
        self.visual_effects.draw_countdown(screen, countdown_number)

        # Desenha o texto "Retornando..." com efeito de pulsação
        self.visual_effects.draw_pulsing_text(
            screen,
            "Retornando à órbita...",
            pygame.font.Font(None, 42),  # Cria uma fonte temporária para o texto pulsante
            (255, 255, 255),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        )

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