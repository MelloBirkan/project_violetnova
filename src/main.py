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
from src.quiz import Quiz

# Import refactored modules
from src.config import *
from src.sound_manager import SoundManager
from src.state_manager import StateManager
from src.collision_manager import CollisionManager
from src.visual_effects import VisualEffectsManager

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Configure screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Project Blue Nova: Explorador do Sistema Solar")
clock = pygame.time.Clock()

# Initialize fonts after pygame is initialized
import src.config as config
config.GAME_FONT = pygame.font.Font(None, config.GAME_FONT_SIZE)
config.SMALL_FONT = pygame.font.Font(None, config.SMALL_FONT_SIZE)
config.COUNTDOWN_FONT = pygame.font.Font(None, config.COUNTDOWN_FONT_SIZE)

# Define planet data for game progression
def create_planet_data():
    """Create data for all planets in the game"""
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
            "background_color": (70, 50, 40),  # Brown
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
            "background_color": (140, 90, 40),  # Amber
            "obstacle_count": 4,
            "quiz_questions": [
                {
                    "question": "Vênus gira em qual direção?",
                    "options": ["Igual à Terra", "Oposta à Terra", "Não gira", "Muda aleatoriamente"],
                    "answer": 1  # Opposite to Earth (retrograde)
                },
                {
                    "question": "A atmosfera de Vênus é composta principalmente por:",
                    "options": ["Nitrogênio", "Dióxido de Carbono", "Ácido Sulfúrico", "Metano"],
                    "answer": 1  # Carbon Dioxide
                },
                {
                    "question": "Vênus é frequentemente chamado de planeta irmão da Terra porque:",
                    "options": ["Tem oceanos", "Tamanho e massa similares", "Tem vida", "Mesmo tempo de órbita"],
                    "answer": 1  # Similar size and mass
                }
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
                    "answer": 1  # Iron oxide
                },
                {
                    "question": "Quantas luas Marte possui?",
                    "options": ["Nenhuma", "Uma", "Duas", "Três"],
                    "answer": 2  # Two (Phobos and Deimos)
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
            "background_color": (210, 140, 70),  # Tan
            "obstacle_count": 20,
            "quiz_questions": [
                {
                    "question": "Do que Júpiter é composto principalmente?",
                    "options": ["Rocha e metal", "Água e gelo", "Hidrogênio e hélio", "Dióxido de carbono"],
                    "answer": 2  # Hydrogen and helium
                },
                {
                    "question": "O que é a Grande Mancha Vermelha em Júpiter?",
                    "options": ["Um vulcão", "Uma tempestade de poeira", "Uma tempestade tipo furacão", "Uma cratera de impacto"],
                    "answer": 2  # A hurricane-like storm
                },
                {
                    "question": "Júpiter tem o dia mais curto de qualquer planeta. Quanto tempo dura?",
                    "options": ["6 horas", "10 horas", "14 horas", "18 horas"],
                    "answer": 1  # ~10 hours
                }
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
                    "answer": 3  # Ice particles
                },
                {
                    "question": "Quantos anéis principais Saturno possui?",
                    "options": ["3", "5", "7", "9"],
                    "answer": 2  # 7 main rings
                },
                {
                    "question": "Saturno é o único planeta que poderia flutuar na água porque:",
                    "options": ["É oco", "É muito pequeno", "Sua densidade é menor que a da água", "Tem hélio"],
                    "answer": 2  # Low density
                }
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
                    "answer": 2  # 384,000 km
                },
                {
                    "question": "O primeiro humano a caminhar na Lua foi:",
                    "options": ["Buzz Aldrin", "Neil Armstrong", "Yuri Gagarin", "Alan Shepard"],
                    "answer": 1  # Neil Armstrong
                },
                {
                    "question": "O que causa as fases da Lua?",
                    "options": ["Sombra da Terra", "Posição do Sol", "Rotação da Lua", "Nuvens na Lua"],
                    "answer": 1  # Sun position
                }
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
                    "answer": 3  # 98 degrees
                },
                {
                    "question": "O que dá a Urano sua cor azul-esverdeada?",
                    "options": ["Água", "Metano", "Amônia", "Nitrogênio"],
                    "answer": 1  # Methane
                },
                {
                    "question": "Urano foi o primeiro planeta descoberto usando um:",
                    "options": ["Olho nu", "Telescópio", "Sonda espacial", "Radiotelescópio"],
                    "answer": 1  # Telescope
                }
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
                    "answer": 2  # 1846
                },
                {
                    "question": "O que é a Grande Mancha Escura em Netuno?",
                    "options": ["Um oceano", "Um sistema de tempestade", "Uma cratera", "Uma sombra"],
                    "answer": 1  # A storm system
                },
                {
                    "question": "A maior lua de Netuno é:",
                    "options": ["Tritão", "Nereida", "Proteus", "Larissa"],
                    "answer": 0  # Triton
                }
            ]
        }
        # Pluto removed from main progression
    ]

    return planet_data

class Game:
    def __init__(self):
        # Game state
        self.score = 0
        self.high_score_manager = HighScore()
        self.high_score = self.high_score_manager.get()

        # Life system
        self.lives = SPACECRAFT_MAX_LIVES
        self.invulnerable = False
        self.invulnerable_timer = 0

        # Initialize internal state before property is used
        self._state = MENU

        # Welcome sound control
        self.welcome_sound_played = False
        self.current_welcome_sound = None
        self.welcome_sound_timer = 0

        # Planet setup
        self.planet_data = create_planet_data()
        self.planets = [Planet(data["name"],
                             data["gravity_factor"],
                             data["background_color"],
                             data["obstacle_count"],
                             data["quiz_questions"])
                      for data in self.planet_data]

        # Start on Earth
        self.current_planet_index = 0
        self.current_planet = self.planets[self.current_planet_index]

        # Spacecraft setup
        self.spacecraft_color = "silver"  # Default color
        self.spacecraft = Spacecraft(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.spacecraft_color)
        self.available_colors = list(Spacecraft.COLORS.keys())
        self.current_color_index = 0

        # Game elements
        self.obstacles = []
        self.collectibles = []
        # Initialize time tracking
        self.last_obstacle_time = pygame.time.get_ticks() - 2000
        self.last_collectible_time = pygame.time.get_ticks()
        self.floor_x = 0

        # Obstacle and collectible timing
        self.obstacle_spawn_rate = DEFAULT_OBSTACLE_SPAWN_RATE
        self.collectible_spawn_rate = DEFAULT_COLLECTIBLE_SPAWN_RATE

        # Game progression
        self.obstacle_speed = 3
        self.weapon_active = False
        self.weapon_timer = 0

        # Initialize NOVA AI assistant
        self.nova = NovaAI(SCREEN_WIDTH, SCREEN_HEIGHT, PLANET_NAME_PT)

        # Initialize quiz system
        self.quiz = Quiz(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Game progression settings
        self.difficulty_multiplier = 1.0

        # Initialize managers
        self.sound_manager = SoundManager()
        self.visual_effects = VisualEffectsManager(self)
        self.collision_manager = CollisionManager(self)

        # Initialize state manager last to avoid circular dependencies
        self.state_manager = StateManager(self)

        # Initialize game state (uses existing _state value)
        self.state_manager.change_state(MENU)

        # Control settings
        self.space_held = False
        self.control_mode = CONTROL_MODE_HOLD  # Default changed to HOLD

    @property
    def state(self):
        """Get the current game state"""
        return self._state

    @state.setter
    def state(self, new_state):
        """Set the game state and update state manager"""
        self._state = new_state
        # We don't call state_manager.change_state here to avoid infinite recursion
        # when state_manager changes the state

    def reset(self, new_planet=False):
        """Reset the game, optionally changing to a new planet"""
        self.state_manager.change_state(PLAYING)
        self.state = PLAYING  # Keep synchronized with state manager
        self.weapon_active = False
        self.weapon_timer = 0

        # Stop all sounds with smooth fadeout
        self.sound_manager.stop_thrust(SOUND_FADEOUT_TIME)
        self.sound_manager.hitting_obstacle_sound.fadeout(SOUND_FADEOUT_TIME)

        # Handle welcome sounds based on reset type
        if not new_planet:
            # Stop all welcome sounds on complete reset
            for sound in self.sound_manager.welcome_sounds.values():
                sound.fadeout(200)
            self.current_welcome_sound = None
            self.welcome_sound_timer = 0

        if new_planet:
            # Reset score for new planet
            self.score = 0
            # Update difficulty based on planet index
            self.difficulty_multiplier = 1.0 + (self.current_planet_index * 0.1)
            # Don't reset lives when changing planets
        else:
            # Start from scratch
            self.score = 0
            self.current_planet_index = 0
            self.current_planet = self.planets[self.current_planet_index]
            self.difficulty_multiplier = 1.0
            # Reset lives to maximum when starting new game
            self.reset_lives()

            # Play Earth's welcome sound when starting/restarting
            if self.current_planet.name in self.sound_manager.welcome_sounds:
                # Stop any playing sounds first
                for sound in self.sound_manager.welcome_sounds.values():
                    sound.fadeout(100)

                # Small delay before playing Earth welcome sound
                pygame.time.delay(200)

                # Store reference to current sound
                self.current_welcome_sound = self.sound_manager.welcome_sounds[self.current_planet.name]
                self.current_welcome_sound.play()
                # Set timer based on sound duration (in milliseconds)
                self.welcome_sound_timer = int(self.current_welcome_sound.get_length() * 1000)
                self.welcome_sound_played = True

        # Reset spacecraft position
        self.spacecraft = Spacecraft(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.spacecraft_color)

        # Clear all obstacles and collectibles
        self.obstacles = []
        self.collectibles = []
        # Initialize time tracking for immediate obstacle generation
        self.last_obstacle_time = pygame.time.get_ticks() - 2000
        self.last_collectible_time = pygame.time.get_ticks()
        # Reset floor position
        self.floor_x = 0

        # Base difficulty adjusted by planet and progression
        self.obstacle_speed = 3 * self.difficulty_multiplier
        self.obstacle_spawn_rate = int(DEFAULT_OBSTACLE_SPAWN_RATE / self.difficulty_multiplier)
        self.collectible_spawn_rate = int(DEFAULT_COLLECTIBLE_SPAWN_RATE / self.difficulty_multiplier)

        # NOVA should alert about gravity
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
                    # Pass events to quiz system only if in QUIZ state
                    if self.state == QUIZ:
                        self.quiz.handle_event(event)
                else:
                    if event.key == pygame.K_SPACE:
                        if self.state == MENU:
                            self.reset()
                        elif self.state == PLAYING:
                            # Single thrust on press
                            self.spacecraft.thrust()
                            # Play engine thrust sound
                            self.sound_manager.play_thrust()
                            # Enable continuous thrust if in hold mode
                            if self.control_mode == CONTROL_MODE_HOLD:
                                self.space_held = True
                        elif self.state == GAME_OVER:
                            # Reset welcome_sound_played flag
                            self.welcome_sound_played = False
                            self.reset()
                        elif self.state == TRANSITION:
                            # Skip transition and force start on new planet
                            self.reset(new_planet=True)
                    
                    # Change spacecraft color with C in menu, toggle control mode in game
                    if event.key == pygame.K_c:
                        if self.state == MENU:
                            self.current_color_index = (self.current_color_index + 1) % len(self.available_colors)
                            self.spacecraft_color = self.available_colors[self.current_color_index]
                            self.spacecraft.change_color(self.spacecraft_color)
                        elif self.state == PLAYING:
                            # Toggle control mode between flappy and hold
                            self.control_mode = CONTROL_MODE_HOLD if self.control_mode == CONTROL_MODE_FLAPPY else CONTROL_MODE_FLAPPY
                            mode_name = "Hold" if self.control_mode == CONTROL_MODE_HOLD else "Flappy"
                            
                            # Update spacecraft flame colors for thrust effect
                            if self.control_mode == CONTROL_MODE_HOLD:
                                # Yellow to orange to red gradient
                                self.spacecraft.flame_colors = [(255, 255, 0), (255, 165, 0), (255, 69, 0)]
                            else:
                                # Single color flame
                                self.spacecraft.flame_colors = []
                            self.spacecraft.update_image()
                            self.nova.show_message(f"Modo de controle: {mode_name}", "info")
                    
                    # Activate weapon with W if available
                    if event.key == pygame.K_w and self.state == PLAYING and self.weapon_active:
                        self._use_weapon()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # Stop continuous thrust on release
                    self.space_held = False
                    # Fade out engine thrust sound
                    self.sound_manager.stop_thrust(SOUND_FADEOUT_TIME)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.state == QUIZ or self.state == QUIZ_FAILURE:
                        # Pass events to quiz system only if in QUIZ state
                        if self.state == QUIZ:
                            self.quiz.handle_event(event)
                    else:
                        if self.state == MENU:
                            self.reset()
                        elif self.state == PLAYING:
                            self.spacecraft.thrust()
                            self.sound_manager.play_thrust()
                        elif self.state == GAME_OVER:
                            # Reset welcome_sound_played flag
                            self.welcome_sound_played = False
                            self.reset()
                        elif self.state == TRANSITION:
                            # If in transition and sound is playing, allow skipping but continue sound at reduced volume
                            if self.welcome_sound_timer > 0 and self.current_welcome_sound:
                                self.sound_manager.adjust_welcome_volume(self.current_planet.name, 0.3)
                            # Force sound timer completion to allow proceeding
                            self.welcome_sound_timer = 0
                            # Skip transition and force start on new planet
                            if self.state_manager.transition_time >= TRANSITION_DURATION // 2:  # Only allow skipping after half the transition
                                self.reset(new_planet=True)

    def _use_weapon(self):
        """Use weapon to destroy obstacles"""
        if not self.weapon_active:
            return

        # Find closest obstacle ahead of spacecraft
        target_obstacle = None
        min_distance = float('inf')

        # Define spacecraft body x position
        spacecraft_body_x = self.spacecraft.x + self.spacecraft.flame_extent

        for obstacle in self.obstacles:
            # Only target obstacles ahead of spacecraft body
            if obstacle.x > spacecraft_body_x:
                distance = obstacle.x - spacecraft_body_x
                if distance < min_distance:
                    min_distance = distance
                    target_obstacle = obstacle

        if target_obstacle:
            # Remove obstacle and grant points
            self.obstacles.remove(target_obstacle)
            self.score += 2
            self.nova.show_message("Obstáculo destruído!", "alert")
            
            # Check for progression to next planet based on new score
            current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
                self.current_planet.name,
                10  # Default threshold for unspecified planets
            )
            if self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                next_planet_en = self.planets[self.current_planet_index + 1].name
                next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
                self.nova.show_message(f"Navegação automática engajada! Indo para {next_planet_pt}!", "excited")
                # Start quiz for planet advancement
                self.state_manager.start_quiz()

    def lose_life(self):
        """Reduce number of lives and check for game over"""
        if not self.invulnerable:
            self.lives -= 1

            # More intuitive hit counting (start with 3 lives, 4th hit = game over)
            hit_count = SPACECRAFT_MAX_LIVES - self.lives

            # Check if all lives are lost
            if hit_count >= 4:  # 4 hits = game over
                self.lives = 0  # Ensure it doesn't go negative
                self.nova.show_message("Dano crítico! Fim de jogo!", "alert")
                self.state_manager.change_state(GAME_OVER)
                self.state = GAME_OVER  # Keep synchronized with state manager
                # Play explosion sound on game over
                self.sound_manager.stop_thrust(100)  # Ensure thrust sound stops quickly
                self.sound_manager.hitting_obstacle_sound.fadeout(100)  # Stop collision sound if playing
                self.sound_manager.play_explosion()
                if self.score > self.high_score_manager.get():
                    self.high_score = self.score
                    self.high_score_manager.save(self.score)
                return False  # Fourth collision causes game over
            elif hit_count == 3:  # 3 hits = last life
                self.nova.show_message("Atenção: Última vida restante!", "alert")
            elif hit_count == 2:  # 2 hits = second-to-last life
                self.nova.show_message("Atenção: Duas vidas restantes!", "alert")

            return True  # Still has lives
        return True  # Didn't lose a life due to invulnerability

    def add_life(self):
        """Add a life, up to the maximum allowed"""
        if self.lives < SPACECRAFT_MAX_LIVES:
            self.lives += 1
            self.nova.show_message("Vida extra adquirida!", "excited")
            return True
        return False  # Already at maximum lives

    def reset_lives(self):
        """Reset lives to maximum value"""
        self.lives = SPACECRAFT_MAX_LIVES
        self.invulnerable = False
        self.invulnerable_timer = 0

    def is_invulnerable(self):
        """Return current invulnerability state"""
        return self.invulnerable

    def update(self):
        try:
            # Update visual effects if available
            if hasattr(self, 'visual_effects'):
                self.visual_effects.update()

            # Update NOVA AI if available
            if hasattr(self, 'nova'):
                self.nova.update()

            # Update welcome sound timer
            if hasattr(self, 'welcome_sound_timer') and self.welcome_sound_timer > 0:
                self.welcome_sound_timer -= 16  # Approximately 16ms per frame at 60fps

                # Check if user tries to skip introduction (by pressing space)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and self.state == TRANSITION:
                    # Don't completely stop welcome sound, just reduce volume
                    if hasattr(self, 'current_welcome_sound') and self.current_welcome_sound and hasattr(self, 'sound_manager'):
                        self.sound_manager.adjust_welcome_volume(self.current_planet.name, 0.3)
                    self.welcome_sound_timer = 0  # Allow proceeding with game

            # Update invulnerability timer
            if hasattr(self, 'invulnerable') and self.invulnerable:
                self.invulnerable_timer -= 1
                if self.invulnerable_timer <= 0:
                    self.invulnerable = False
                    if hasattr(self, 'nova'):
                        self.nova.show_message("Sistemas de escudo restaurados", "normal")

            # Update state manager
            if hasattr(self, 'state_manager'):
                self.state_manager.update()
        except AttributeError as e:
            # Print error for debugging purposes
            print(f"Error in update: {e}")
            # Continue game loop

        if self.state == PLAYING:
            try:
                if hasattr(self, 'spacecraft') and hasattr(self, 'current_planet'):
                    # Update spacecraft with current planet's gravity and screen limits
                    self.spacecraft.update(self.current_planet.gravity, SCREEN_HEIGHT, FLOOR_HEIGHT)

                    # Continuous thrust while space is held in hold mode
                    if hasattr(self, 'control_mode') and hasattr(self, 'space_held') and self.control_mode == CONTROL_MODE_HOLD and self.space_held:
                        # Apply small continuous thrust (20% of thrust power)
                        cont = self.spacecraft.thrust_power * self.spacecraft.thrust_multiplier * 0.2
                        self.spacecraft.velocity -= cont
                        # Maintain flame effect
                        self.spacecraft.last_thrust_time = pygame.time.get_ticks()
                        # Ensure thrust sound continues playing
                        if hasattr(self, 'sound_manager'):
                            if not pygame.mixer.get_busy() or not self.sound_manager.engine_thrust_sound.get_num_channels():
                                self.sound_manager.play_thrust()

                # Generate obstacles
                if hasattr(self, 'last_obstacle_time') and hasattr(self, 'obstacle_spawn_rate'):
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_obstacle_time > self.obstacle_spawn_rate:
                        # Generate obstacle
                        self._generate_obstacle()
                        self.last_obstacle_time = current_time

                # Generate collectibles
                if hasattr(self, 'last_collectible_time') and hasattr(self, 'collectible_spawn_rate'):
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_collectible_time > self.collectible_spawn_rate:
                        # Generate collectible
                        self._generate_collectible()
                        self.last_collectible_time = current_time

                # Update obstacles and check scoring
                if hasattr(self, 'obstacles'):
                    for obstacle in self.obstacles:
                        obstacle.update()

                        # Score when passing an obstacle
                        if hasattr(self, 'spacecraft') and not obstacle.scored and obstacle.x + obstacle.WIDTH < self.spacecraft.x:
                            self.score += 1
                            obstacle.scored = True

                            # Check for automatic progression
                            if hasattr(self, 'current_planet') and hasattr(self, 'state_manager'):
                                current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
                                    self.current_planet.name,
                                    10  # Default threshold
                                )

                                # Check if score threshold reached for automatic progression
                                if hasattr(self, 'planets') and self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                                    # NOVA announces automatic progression
                                    if hasattr(self, 'nova'):
                                        next_planet_en = self.planets[self.current_planet_index + 1].name
                                        next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
                                        self.nova.show_message(f"Navegação automática engajada! Indo para {next_planet_pt}!", "excited")

                                    # Start quiz without incrementing planet index yet - let quiz handle progression
                                    self.state_manager.start_quiz()

                # Update collectibles and check collision
                if hasattr(self, 'collision_manager') and hasattr(self, 'collectibles'):
                    # Check collectible collisions
                    self.collision_manager.check_collectible_collisions()

                    # Update collectibles
                    for collectible in list(self.collectibles):
                        collectible.update()
                        if hasattr(self, 'obstacle_speed'):
                            collectible.x -= self.obstacle_speed  # Move at same speed as obstacles

                # Update weapon timer
                if hasattr(self, 'weapon_active') and self.weapon_active:
                    self.weapon_timer -= 1
                    if self.weapon_timer <= 0:
                        self.weapon_active = False
                        if hasattr(self, 'nova'):
                            self.nova.show_message("Sistemas defensivos offline", "normal")

                # Remove off-screen obstacles and collectibles
                if hasattr(self, 'obstacles'):
                    self.obstacles = [obs for obs in self.obstacles if obs.x > -obs.WIDTH]
                if hasattr(self, 'collectibles'):
                    self.collectibles = [col for col in self.collectibles if col.x > -col.WIDTH]

                # Check collisions
                if hasattr(self, 'collision_manager'):
                    collision_result = self.collision_manager.check_collisions()
                    if collision_result is not False and hasattr(self, 'sound_manager'):  # If collision occurred
                        # Play obstacle collision sound
                        self.sound_manager.play_collision()
                        # Game over is already handled within lose_life

                # Move floor
                if hasattr(self, 'floor_x') and hasattr(self, 'obstacle_speed'):
                    self.floor_x = (self.floor_x - self.obstacle_speed) % 800

            except AttributeError as e:
                print(f"Error in PLAYING state update: {e}")
            
    def _generate_obstacle(self):
        """Generate a new obstacle"""
        # Define fixed gap between obstacles
        gap_size = Obstacle.GAP

        # Calculate min and max values for gap center
        min_gap_center_y = gap_size // 2
        max_gap_center_y = SCREEN_HEIGHT - FLOOR_HEIGHT - (gap_size // 2)

        # Handle edge cases with extreme constants
        if min_gap_center_y > max_gap_center_y:
            target_y = ((gap_size // 2) + (SCREEN_HEIGHT - FLOOR_HEIGHT - (gap_size // 2))) // 2

            # Define absolute boundaries for clamping
            abs_min_y = gap_size // 2
            abs_max_y = SCREEN_HEIGHT - FLOOR_HEIGHT - (gap_size // 2)

            if abs_min_y > abs_max_y:  # e.g. gap_size > playable height
                # Just use middle of screen's playable height
                target_y = (SCREEN_HEIGHT - FLOOR_HEIGHT) // 2
            else:
                # Clamp target_y to physically possible range
                target_y = max(abs_min_y, min(target_y, abs_max_y))

            min_gap_center_y = target_y
            max_gap_center_y = target_y

        # Generate random y position for gap center
        gap_y = random.randint(min_gap_center_y, max_gap_center_y)

        # Randomly select obstacle type
        obstacle_type = random.choice(list(Obstacle.TYPES.keys()))

        # Create new obstacle
        new_obstacle = Obstacle(SCREEN_WIDTH, gap_y, self.obstacle_speed, obstacle_type, SCREEN_HEIGHT)
        self.obstacles.append(new_obstacle)

        # Occasionally have NOVA alert about obstacles
        if random.random() < 0.3:  # 30% chance
            pass

    def _generate_collectible(self):
        """Generate a new collectible"""
        # Place collectible in a safe location
        x = SCREEN_WIDTH
        y = random.randint(100, SCREEN_HEIGHT - FLOOR_HEIGHT - 50)

        # Determine collectible type (1% chance for life, 10% weapon, rest data)
        collectible_type = "data"
        rand_val = random.random()
        if rand_val < 0.01:  # 1% chance for life
            collectible_type = "life"
        elif rand_val < 0.11 and not self.weapon_active:  # 10% chance for weapon
            collectible_type = "weapon"

        self.collectibles.append(Collectible(x, y, collectible_type))

    def draw(self):
        # Draw background
        self.visual_effects.draw_background(screen, self.current_planet)

        # Draw content based on game state
        if self.state == PLAYING or self.state == MENU or self.state == GAME_OVER or self.state == QUIZ_FAILURE:
            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(screen)

            # Draw collectibles
            for collectible in self.collectibles:
                collectible.draw(screen)

            # Draw floor/ground
            self.current_planet.draw_ground(screen, self.floor_x, SCREEN_HEIGHT)

            # Draw spacecraft (with invulnerability effect if applicable)
            self.spacecraft.draw(screen, self.invulnerable)

            # Draw current planet name and player score
            if self.state != MENU:
                # Left side information
                display_name = PLANET_NAME_PT.get(self.current_planet.name, self.current_planet.name)
                planet_text = config.SMALL_FONT.render(f"Planeta: {display_name}", True, (255, 255, 255))
                screen.blit(planet_text, (20, 20))

                # Get threshold for current planet
                current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
                    self.current_planet.name,
                    10  # Default threshold
                )

                score_text = config.SMALL_FONT.render(f"Pontuação: {self.score}/{current_threshold}", True, (255, 255, 255))
                screen.blit(score_text, (20, 50))

                high_score_text = config.SMALL_FONT.render(f"Maior Pontuação: {self.high_score_manager.get()}", True, (255, 255, 255))
                screen.blit(high_score_text, (20, 80))

                # Draw lives indicator
                lives_text = config.SMALL_FONT.render(f"Vidas:", True, (255, 255, 255))
                screen.blit(lives_text, (20, 110))

                # Draw life icons
                self.visual_effects.draw_life_icons(screen, self.lives, SPACECRAFT_MAX_LIVES, self.spacecraft_color)

                # Draw weapon status in top center if active
                if self.weapon_active:
                    weapon_time = self.weapon_timer // 60  # Convert to seconds
                    weapon_text = config.SMALL_FONT.render(f"Arma Ativa: {weapon_time}s", True, (255, 100, 100))
                    screen.blit(weapon_text, (SCREEN_WIDTH // 2 - weapon_text.get_width() // 2, 20))

            # Draw NOVA AI assistant
            self.nova.draw(screen)
            
            # If quiz failed, overlay large countdown before resuming
            if self.state == QUIZ_FAILURE and self.state_manager.quiz_failure_timer > 0:
                countdown = math.ceil(self.state_manager.quiz_failure_timer / 60)
                self.visual_effects.draw_countdown(screen, countdown)

            # Draw menu screen
            if self.state == MENU:
                self._draw_menu_screen(screen)

            # Draw game over screen
            if self.state == GAME_OVER:
                self._draw_game_over_screen(screen)

        elif self.state == TRANSITION:
            self._draw_transition_screen(screen)

        elif self.state == QUIZ:
            # Draw quiz
            self.quiz.draw(screen)

            # Always draw NOVA AI assistant on top in quiz state as well
            self.nova.draw(screen)

        elif self.state == QUIZ_FAILURE:
            self._draw_quiz_failure_screen(screen)

        # Always draw NOVA AI assistant on top
        self.nova.draw(screen)

    def _draw_menu_screen(self, screen):
        """Draw the menu screen"""
        # Semi-transparent overlay
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

        # Show controls
        controls_title = config.SMALL_FONT.render("Controles:", True, (255, 255, 255))
        controls_space = config.SMALL_FONT.render("ESPAÇO - Impulsionar", True, (200, 200, 200))
        controls_w = config.SMALL_FONT.render("W - Usar Arma (quando disponível)", True, (200, 200, 200))

        controls_y = SCREEN_HEIGHT - 120
        screen.blit(controls_title, (SCREEN_WIDTH // 2 - controls_title.get_width() // 2, controls_y))
        screen.blit(controls_space, (SCREEN_WIDTH // 2 - controls_space.get_width() // 2, controls_y + 30))
        screen.blit(controls_w, (SCREEN_WIDTH // 2 - controls_w.get_width() // 2, controls_y + 60))

    def _draw_game_over_screen(self, screen):
        """Draw the game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        game_over_text = config.GAME_FONT.render("MISSÃO CONCLUÍDA", True, (255, 215, 0))
        score_text = config.GAME_FONT.render(f"Pontuação Final: {self.score}", True, (255, 255, 255))
        high_score_text = config.GAME_FONT.render(f"Maior Pontuação: {self.high_score_manager.get()}", True, (255, 255, 255))
        restart_text = config.GAME_FONT.render("Pressione ESPAÇO para iniciar nova missão", True, (255, 255, 255))

        # Calculate furthest planet reached
        furthest_planet = self.planets[min(self.current_planet_index, len(self.planets) - 1)].name
        planet_text = config.GAME_FONT.render(f"Planeta mais distante: {furthest_planet}", True, (255, 255, 255))

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 220))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 270))
        screen.blit(planet_text, (SCREEN_WIDTH // 2 - planet_text.get_width() // 2, 320))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

    def _draw_transition_screen(self, screen):
        """Draw the transition screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Darker overlay for text readability
        screen.blit(overlay, (0, 0))

        # Draw destination planet name
        display_name = PLANET_NAME_PT.get(self.current_planet.name, self.current_planet.name)
        planet_title = config.GAME_FONT.render(f"Bem-vindo a {display_name}", True, (255, 255, 255))
        screen.blit(planet_title, (SCREEN_WIDTH // 2 - planet_title.get_width() // 2, 100))

        # Draw gravity information
        gravity_text = config.GAME_FONT.render(f"Gravidade: {self.current_planet.gravity_factor}% da Terra", True, (255, 255, 255))
        screen.blit(gravity_text, (SCREEN_WIDTH // 2 - gravity_text.get_width() // 2, 150))

        # Draw planet info text
        info_text = self.current_planet.get_info_text()
        # Wrap text to fit screen
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
        wrapped_lines.append(line)  # Add last line

        # Draw wrapped text
        for i, line in enumerate(wrapped_lines):
            line_surface = config.SMALL_FONT.render(line, True, (200, 200, 255))
            screen.blit(line_surface, (SCREEN_WIDTH // 2 - line_surface.get_width() // 2, 220 + i * 30))

        # Draw progress indicator
        progress_text = config.SMALL_FONT.render(f"Planeta {self.current_planet_index + 1} de {len(self.planets)}", True, (180, 180, 180))
        screen.blit(progress_text, (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, 350))

        # Draw continue prompt
        if self.state_manager.transition_time > 60:  # Only show after 1 second
            continue_text = config.SMALL_FONT.render("Pressione ESPAÇO para continuar", True, (255, 255, 255))
            # Make it pulse
            alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
            continue_text.set_alpha(alpha)
            screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 450))

    def _draw_quiz_failure_screen(self, screen):
        """Draw the quiz failure screen with countdown"""
        # Add semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # More visible semi-transparent black
        screen.blit(overlay, (0, 0))

        # Calculate countdown number
        countdown_number = self.state_manager.quiz_failure_timer // 60 + 1

        # Draw large countdown number
        self.visual_effects.draw_countdown(screen, countdown_number)

        # Draw "Returning..." text with pulse effect
        self.visual_effects.draw_pulsing_text(
            screen,
            "Retornando à órbita...",
            pygame.font.Font(None, 42),  # Create a temporary font for the pulsing text
            (255, 255, 255),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        )

def main():
    # Create and start the game
    game = Game()

    # Game loop
    while True:
        game.handle_events()
        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()