import pygame
from src.config import DEFAULT_SOUND_VOLUME

class SoundManager:
    def __init__(self):
        # Inicializa o sistema de som
        self.engine_thrust_sound = None
        self.explosion_sound = None
        self.hitting_obstacle_sound = None
        self.welcome_sounds = {}
        
        # Carrega todos os sons
        self.load_sounds()
        
    def load_sounds(self):
        try:
            # Carrega os sons do jogo
            self.engine_thrust_sound = pygame.mixer.Sound("assets/sounds/thrust.mp3")
            self.explosion_sound = pygame.mixer.Sound("assets/sounds/exploding.mp3")
            self.hitting_obstacle_sound = pygame.mixer.Sound("assets/sounds/hitting_obstacle.mp3")
            
            # Carrega os sons de boas-vindas para cada planeta
            self.welcome_sounds = {
                "Earth": pygame.mixer.Sound("assets/sounds/welcome/terra.mp3"),
                "Mercury": pygame.mixer.Sound("assets/sounds/welcome/mercurio.mp3"),
                "Venus": pygame.mixer.Sound("assets/sounds/welcome/venus.mp3"),
                "Moon": pygame.mixer.Sound("assets/sounds/welcome/lua.mp3"),
                "Mars": pygame.mixer.Sound("assets/sounds/welcome/marte.mp3"),
                "Jupiter": pygame.mixer.Sound("assets/sounds/welcome/jupiter.mp3"),
                "Saturn": pygame.mixer.Sound("assets/sounds/welcome/saturno.mp3"),
                "Uranus": pygame.mixer.Sound("assets/sounds/welcome/urano.mp3"),
                "Neptune": pygame.mixer.Sound("assets/sounds/welcome/Netuno.mp3")
            }
            
            # Define o volume padrão para os sons do jogo
            self.engine_thrust_sound.set_volume(DEFAULT_SOUND_VOLUME)
            self.explosion_sound.set_volume(DEFAULT_SOUND_VOLUME)
            self.hitting_obstacle_sound.set_volume(DEFAULT_SOUND_VOLUME)
            
            # Define o volume máximo para os sons de boas-vindas (narração)
            for sound in self.welcome_sounds.values():
                sound.set_volume(1.0)
                
            return True
            
        except pygame.error as e:
            print(f"Não foi possível carregar os arquivos de som: {e}")
            return False
    
    def play_thrust(self, loop=True):
        """Reproduz o som de propulsão do motor com loop opcional"""
        if loop:
            self.engine_thrust_sound.play(-1)  # Repete indefinidamente
        else:
            self.engine_thrust_sound.play()
    
    def stop_thrust(self, fadeout_time=None):
        """Para o som de propulsão com fadeout opcional"""
        if fadeout_time:
            self.engine_thrust_sound.fadeout(fadeout_time)
        else:
            self.engine_thrust_sound.stop()
    
    def play_explosion(self):
        """Reproduz o som de explosão (fim de jogo)"""
        self.explosion_sound.play()
    
    def play_collision(self):
        """Reproduz o som de colisão (atingindo obstáculos)"""
        self.hitting_obstacle_sound.play()
    
    def play_welcome(self, planet_name):
        """Reproduz o som de boas-vindas para um planeta específico"""
        if planet_name in self.welcome_sounds:
            # Garante que todos os outros sons de boas-vindas sejam parados
            for sound in self.welcome_sounds.values():
                sound.fadeout(100)
            
            # Reproduz o som de boas-vindas para este planeta
            self.welcome_sounds[planet_name].play()
            
            # Retorna a duração do som em milissegundos
            return int(self.welcome_sounds[planet_name].get_length() * 1000)
        
        return 0
    
    def stop_all_sounds(self, fadeout_time=200):
        """Para todos os sons com fadeout"""
        # Para os sons do jogo
        self.engine_thrust_sound.fadeout(fadeout_time)
        self.hitting_obstacle_sound.fadeout(fadeout_time)
        self.explosion_sound.fadeout(fadeout_time)
        
        # Para todos os sons de boas-vindas
        for sound in self.welcome_sounds.values():
            sound.fadeout(fadeout_time)
            
    def adjust_welcome_volume(self, planet_name, volume=0.3):
        """Ajusta o volume de um som de boas-vindas específico"""
        if planet_name in self.welcome_sounds:
            self.welcome_sounds[planet_name].set_volume(volume)