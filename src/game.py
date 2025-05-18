import pygame
import sys
from src.spacecraft import Spacecraft
from src.planet import Planet
from src.highscore import PlanetTracker
from src.nova_ai import NovaAI
from src.quiz import Quiz

# Import refactored modules
import src.config as config
from src.sound_manager import SoundManager
from src.state_manager import StateManager
from src.collision_manager import CollisionManager
from src.visual_effects import VisualEffectsManager
from src.ui_manager import UIManager
from src.input_handler import InputHandler
from src.game_mechanics import GameMechanics
from src.weapon_system import WeaponSystem
from src.planet_data import create_planet_data, PLANET_NAME_PT, LEVEL_PROGRESSION_THRESHOLDS

class Game:
    def __init__(self):
        # Estado do jogo
        self.score = 0
        self.planet_tracker = PlanetTracker()
        self.last_planet = self.planet_tracker.get_last_planet()
        self.furthest_planet = self.planet_tracker.get_furthest_planet()
        self.furthest_planet_index = 0  # Registra o planeta mais distante alcançado

        # Sistema de vidas e dificuldade
        self.difficulty = config.DEFAULT_DIFFICULTY
        self.max_lives = config.DIFFICULTY_SETTINGS[self.difficulty].get(
            "max_lives",
            config.DIFFICULTY_SETTINGS[self.difficulty]["lives"],
        )
        self.lives = self.max_lives
        self.invulnerable = False
        self.invulnerable_timer = 0
        # Controle do menu de dificuldade
        self.in_difficulty_menu = False
        self.selected_difficulty = self.difficulty
        # Rastreia o planeta em que o jogador morreu para continuar dali
        self.planet_at_death = 0

        # Inicializa o estado interno antes de usar a propriedade
        self._state = config.MENU

        # Controle de som de boas-vindas
        self.welcome_sound_played = False
        self.current_welcome_sound = None
        self.welcome_sound_timer = 0

        # Configuração dos planetas
        self.planet_data = create_planet_data()
        self.planets = [Planet(data["name"],
                             data["gravity_factor"],
                             data["background_color"],
                             data["obstacle_count"],
                             data["quiz_questions"],
                             data.get("hints", []))
                      for data in self.planet_data]

        # Encontra o índice do planeta salvo e do mais distante
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

        # Configuração da nave espacial
        self.spacecraft = Spacecraft(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        # Elementos do jogo
        self.obstacles = []
        self.collectibles = []
        # Inicializa controle de tempo
        self.last_obstacle_time = pygame.time.get_ticks() - 2000
        self.last_collectible_time = pygame.time.get_ticks()
        self.floor_x = 0

        # Temporização de obstáculos e colecionáveis
        self.obstacle_spawn_rate = config.DEFAULT_OBSTACLE_SPAWN_RATE
        self.collectible_spawn_rate = config.DEFAULT_COLLECTIBLE_SPAWN_RATE

        # Progressão do jogo
        self.obstacle_speed = 3
        self.weapon_active = False
        self.weapon_timer = 0

        # Inicializa a assistente NOVA AI
        self.nova = NovaAI(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, PLANET_NAME_PT)

        # Inicializa o sistema de quiz
        self.quiz = Quiz(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        # Configurações de progressão
        self.difficulty_multiplier = 1.0

        # Inicializa os gerenciadores
        self.sound_manager = SoundManager()
        self.visual_effects = VisualEffectsManager(self)
        self.collision_manager = CollisionManager(self)
        self.ui_manager = UIManager(self)
        self.input_handler = InputHandler(self)
        self.game_mechanics = GameMechanics(self)
        self.weapon_system = WeaponSystem(self)

        # Inicializa o gerenciador de estado por último para evitar dependências circulares
        self.state_manager = StateManager(self)

        # Inicializa o estado do jogo (usa o valor existente de _state)
        self.state_manager.change_state(config.MENU)

        # Control settings
        self.space_held = False
        self.control_mode = config.CONTROL_MODE_HOLD  # Padrão alterado para HOLD
        
        # Menu navigation
        self.selected_menu_option = 0

    @property
    def state(self):
        """Obtém o estado atual do jogo"""
        return self._state

    @state.setter
    def state(self, new_state):
        """Define o estado do jogo e atualiza o gerenciador"""
        self._state = new_state
        # Don't call state_manager.change_state here to avoid infinite recursion
        # when the state_manager changes the state

    def reset(self, new_planet=False, continue_from_death=False, continue_from_saved=False):
        """Reinicia o jogo, podendo mudar de planeta, continuar após a morte ou a partir do salvo"""
        settings = config.DIFFICULTY_SETTINGS[self.difficulty]
        self.max_lives = settings.get("max_lives", settings["lives"])
        if not new_planet:
            self.lives = self.max_lives
        
        if continue_from_saved:
            # Continue from the saved planet (checkpoint)
            # current_planet_index já está definido no __init__ baseado no planeta salvo
            self.state_manager.change_state(config.TRANSITION)
            self.state = config.TRANSITION
            # Play welcome sound for saved planet
            self.state_manager.welcome_sound_timer = self.sound_manager.play_welcome(self.current_planet.name)
        elif continue_from_death:
            # Continue from the planet where the player died
            self.current_planet_index = self.planet_at_death
            self.current_planet = self.planets[self.current_planet_index]
            self.state_manager.change_state(config.PLAYING)
            self.state = config.PLAYING
            
            # NOVA message about continuing on same planet
            from src.planet_data import PLANET_NAME_PT
            planet_name_pt = PLANET_NAME_PT.get(self.current_planet.name, self.current_planet.name)
            self.nova.show_message(f"Reabastecendo e retornando a {planet_name_pt}...", "info")
        elif not new_planet:
            # When starting a new game, begin with Earth's transition screen
            self.state_manager.change_state(config.TRANSITION)
            self.state = config.TRANSITION
        else:
            # When changing planets, go directly to playing
            self.state_manager.change_state(config.PLAYING)
            self.state = config.PLAYING
        
        self.weapon_active = False
        self.weapon_timer = 0

        # Stop all sounds with smooth fadeout
        self.sound_manager.stop_thrust(config.SOUND_FADEOUT_TIME)
        self.sound_manager.hitting_obstacle_sound.fadeout(config.SOUND_FADEOUT_TIME)

        # Handle welcome sounds based on reset type
        if not new_planet:
            # Stop all welcome sounds in full reset
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
            
            # Save current planet and update furthest planet se permitido
            self.planet_tracker.save(
                self.current_planet.name.lower(),
                update_furthest=True,
                allow_save=settings["save_checkpoint"],
            )
        elif not continue_from_death:
            # Start from scratch on Earth (only when not continuing from death)
            self.score = 0
            # Find Earth's index in the planets list
            earth_index = 0
            for i, planet in enumerate(self.planets):
                if planet.name.lower() == "earth":
                    earth_index = i
                    break
            
            self.current_planet_index = earth_index
            self.current_planet = self.planets[self.current_planet_index]
            self.difficulty_multiplier = 1.0
            # Reset lives to maximum when starting a new game
            self.reset_lives()
            
            # Save current planet (Earth) se checkpoints estiverem ativos
            self.planet_tracker.save(
                self.current_planet.name.lower(),
                update_furthest=False,
                allow_save=settings["save_checkpoint"],
            )

            # Play Earth welcome sound through sound manager
            if hasattr(self, 'sound_manager'):
                # Stop any playing sounds first
                for sound in self.sound_manager.welcome_sounds.values():
                    sound.fadeout(100)

                # Play welcome sound and set timer
                duration_ms = self.sound_manager.play_welcome(self.current_planet.name)
                self.state_manager.welcome_sound_timer = duration_ms
                self.welcome_sound_played = True
                if hasattr(self, 'nova'):
                    self.nova.start_radio_signal(duration_ms)

        # Reset spacecraft position
        self.spacecraft = Spacecraft(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        # Clear all obstacles and collectibles
        self.obstacles = []
        self.collectibles = []
        # Initialize time tracking for immediate obstacle generation
        self.last_obstacle_time = pygame.time.get_ticks() - 2000
        self.last_collectible_time = pygame.time.get_ticks()
        # Reset floor position
        self.floor_x = 0

        # Base difficulty ajustada pela dificuldade e progressão
        self.obstacle_speed = 3 * self.difficulty_multiplier
        base_rate = (config.DEFAULT_OBSTACLE_SPAWN_RATE *
                     settings["obstacle_distance_multiplier"])
        self.obstacle_spawn_rate = int(base_rate / self.difficulty_multiplier)
        self.collectible_spawn_rate = int(
            config.DEFAULT_COLLECTIBLE_SPAWN_RATE / self.difficulty_multiplier
        )

        # NOVA should alert about gravity
        if new_planet:
            self.nova.alert_gravity_change(
                self.current_planet.name,
                self.current_planet.gravity_factor
            )

    def lose_life(self):
        """Reduz o número de vidas e verifica se o jogo terminou"""
        if not self.invulnerable:
            self.lives -= 1

            if self.lives <= 0:
                self.lives = 0
                self.nova.show_message("Dano crítico! Fim de jogo!", "alert")
                self.state_manager.change_state(config.GAME_OVER)
                self.state = config.GAME_OVER
                self.sound_manager.stop_thrust(100)
                self.sound_manager.hitting_obstacle_sound.fadeout(100)
                self.sound_manager.play_explosion()
                # Save the current planet index to continue from where player failed
                self.planet_at_death = self.current_planet_index
                return False
            elif self.lives == 1 and self.max_lives > 1:
                self.nova.show_message("Atenção: Última vida restante!", "alert")
            elif self.lives == 2 and self.max_lives > 2:
                self.nova.show_message("Atenção: Duas vidas restantes!", "alert")

            return True  # Still has lives
        return True  # Didn't lose life due to invulnerability

    def add_life(self):
        """Adiciona uma vida até o máximo permitido"""
        if self.lives < self.max_lives:
            self.lives += 1
            self.nova.show_message("Vida extra adquirida!", "excited")
            return True
        return False  # Already at maximum lives

    def reset_lives(self):
        """Reseta as vidas para o valor máximo"""
        self.lives = self.max_lives
        self.invulnerable = False
        self.invulnerable_timer = 0

    def is_invulnerable(self):
        """Retorna o estado atual de invulnerabilidade"""
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

                # Check if the user tries to skip the intro (by pressing space)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and self.state == config.TRANSITION:
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
                
            # Update weapon system
            if hasattr(self, 'weapon_system'):
                self.weapon_system.update()
                
            # Update game mechanics if playing
            if self.state == config.PLAYING and hasattr(self, 'game_mechanics'):
                self.game_mechanics.update()
                
        except AttributeError as e:
            # Print error for debugging
            print(f"Error in update: {e}")
            # Continue game loop

    def draw(self):
        """Desenha o jogo"""
        screen = pygame.display.get_surface()
        self.ui_manager.draw(screen)

def main():
    # Create and start the game
    game = Game()

    # Game loop
    clock = pygame.time.Clock()
    while True:
        game.input_handler.handle_events()
        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()
    
    # Setup screen
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Projeto Violeta Nova: Explorador do Sistema Solar")
    
    # Initialize fonts after pygame is initialized
    import src.config as config
    config.GAME_FONT = pygame.font.Font(None, config.GAME_FONT_SIZE)
    config.SMALL_FONT = pygame.font.Font(None, config.SMALL_FONT_SIZE)
    config.COUNTDOWN_FONT = pygame.font.Font(None, config.COUNTDOWN_FONT_SIZE)
    
    main()