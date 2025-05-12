import pygame
from src.config import DEFAULT_SOUND_VOLUME

class SoundManager:
    def __init__(self):
        # Initialize sound system
        self.engine_thrust_sound = None
        self.explosion_sound = None
        self.hitting_obstacle_sound = None
        self.welcome_sounds = {}
        
        # Load all sounds
        self.load_sounds()
        
    def load_sounds(self):
        try:
            # Load game sounds
            self.engine_thrust_sound = pygame.mixer.Sound("assets/sounds/thrust.mp3")
            self.explosion_sound = pygame.mixer.Sound("assets/sounds/exploding.mp3")
            self.hitting_obstacle_sound = pygame.mixer.Sound("assets/sounds/hitting_obstacle.mp3")
            
            # Load welcome sounds for each planet
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
            
            # Set default volume for game sounds
            self.engine_thrust_sound.set_volume(DEFAULT_SOUND_VOLUME)
            self.explosion_sound.set_volume(DEFAULT_SOUND_VOLUME)
            self.hitting_obstacle_sound.set_volume(DEFAULT_SOUND_VOLUME)
            
            # Set maximum volume for welcome sounds (narration)
            for sound in self.welcome_sounds.values():
                sound.set_volume(1.0)
                
            return True
            
        except pygame.error as e:
            print(f"Could not load sound assets: {e}")
            return False
    
    def play_thrust(self, loop=True):
        """Play the engine thrust sound with optional looping"""
        if loop:
            self.engine_thrust_sound.play(-1)  # Loop indefinitely
        else:
            self.engine_thrust_sound.play()
    
    def stop_thrust(self, fadeout_time=None):
        """Stop the thrust sound with optional fadeout"""
        if fadeout_time:
            self.engine_thrust_sound.fadeout(fadeout_time)
        else:
            self.engine_thrust_sound.stop()
    
    def play_explosion(self):
        """Play the explosion sound (game over)"""
        self.explosion_sound.play()
    
    def play_collision(self):
        """Play the collision sound (hitting obstacles)"""
        self.hitting_obstacle_sound.play()
    
    def play_welcome(self, planet_name):
        """Play welcome sound for a specific planet"""
        if planet_name in self.welcome_sounds:
            # Ensure all other welcome sounds are stopped
            for sound in self.welcome_sounds.values():
                sound.fadeout(100)
            
            # Play the welcome sound for this planet
            self.welcome_sounds[planet_name].play()
            
            # Return the sound length in milliseconds
            return int(self.welcome_sounds[planet_name].get_length() * 1000)
        
        return 0
    
    def stop_all_sounds(self, fadeout_time=200):
        """Stop all sounds with a fadeout"""
        # Stop game sounds
        self.engine_thrust_sound.fadeout(fadeout_time)
        self.hitting_obstacle_sound.fadeout(fadeout_time)
        self.explosion_sound.fadeout(fadeout_time)
        
        # Stop all welcome sounds
        for sound in self.welcome_sounds.values():
            sound.fadeout(fadeout_time)
            
    def adjust_welcome_volume(self, planet_name, volume=0.3):
        """Adjust volume of a specific welcome sound"""
        if planet_name in self.welcome_sounds:
            self.welcome_sounds[planet_name].set_volume(volume)