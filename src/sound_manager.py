import pygame
import os
from src.config import DEFAULT_SOUND_VOLUME, THRUST_SOUND_VOLUME, HIT_SOUND_VOLUME

class SoundManager:
    def __init__(self):
        # Inicializa o sistema de som
        self.engine_thrust_sound = None
        self.explosion_sound = None
        self.hitting_obstacle_sound = None
        self.welcome_sounds = {}
        self.background_music = {}
        self.current_music = None
        self.music_active = False
        self.music_volume = 0.3  # Volume inicial baixo
        self.target_volume = 0.7  # Volume alvo após 2 pontos
        
        # Garante que o mixer esteja inicializado corretamente
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.quit()
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
            except pygame.error as e:
                print(f"Erro ao reinicializar o mixer: {e}")
        
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
            
            # Carrega as músicas de fundo para cada planeta
            music_files = {
                "Earth": "Cosmic Dreams.mp3",
                "Mercury": "Adorable Walk.mp3",
                "Venus": "Aurora's Lullaby.mp3",
                "Moon": "Lunar Tides.mp3",
                "Mars": "Melancholia (Cover).mp3",
                "Jupiter": "Interstellar Odyssey.mp3",
                "Saturn": "Odyssey.mp3",
                "Uranus": "Stellar Journey.mp3",
                "Neptune": "Cosmic Dreams-2.mp3"
            }
            
            for planet, music_file in music_files.items():
                music_path = os.path.join("assets", "musics", music_file)
                if os.path.exists(music_path):
                    self.background_music[planet] = music_path
                else:
                    print(f"Aviso: Música para {planet} não encontrada: {music_path}")
            
            # Define o volume para os sons do jogo
            self.engine_thrust_sound.set_volume(THRUST_SOUND_VOLUME)  # Volume do propulsor reduzido
            self.explosion_sound.set_volume(DEFAULT_SOUND_VOLUME)
            self.hitting_obstacle_sound.set_volume(HIT_SOUND_VOLUME)  # Volume de colisão igualado ao do propulsor
            
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
            
    def play_planet_music(self, planet_name):
        """Inicia a música de fundo para um planeta específico"""
        # Se já estiver tocando a música para este planeta, não faz nada
        if self.music_active and self.current_music == planet_name and pygame.mixer.music.get_busy():
            return True
            
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(1000)  # Fade out se houver música tocando
            
        if planet_name in self.background_music:
            try:
                # Adicionando tratamento de erro robusto
                try:
                    pygame.mixer.music.unload()  # Descarrega qualquer música anterior
                except (pygame.error, AttributeError):
                    # Alguns sistemas/versões não suportam unload
                    pass
                    
                # Tenta carregar e reproduzir a música com verificação
                pygame.mixer.music.load(self.background_music[planet_name])
                pygame.mixer.music.set_volume(self.music_volume)  # Volume baixo no início
                pygame.mixer.music.play(-1)  # Toca em loop
                
                # Verifica se conseguiu reproduzir
                if pygame.mixer.music.get_busy():
                    self.current_music = planet_name
                    self.music_active = True
                    return True
                else:
                    # Se não estiver tocando, tente novamente uma vez
                    pygame.time.delay(100)  # Pequeno atraso
                    pygame.mixer.music.play(-1)
                    self.current_music = planet_name
                    self.music_active = True
                    return True
                    
            except pygame.error as e:
                print(f"Erro ao reproduzir música para {planet_name}: {e}")
                # Tenta recuperar o mixer em caso de falha
                try:
                    pygame.mixer.quit()
                    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
                    pygame.time.delay(500)  # Espera a reinicialização
                    # Tenta novamente após reiniciar o mixer
                    pygame.mixer.music.load(self.background_music[planet_name])
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(-1)
                    self.current_music = planet_name
                    self.music_active = True
                    return True
                except pygame.error as e2:
                    print(f"Tentativa de recuperação falhou: {e2}")
                    self.music_active = False
                    return False
        else:
            print(f"Sem música disponível para {planet_name}")
            self.music_active = False
            return False
    
    def stop_music(self, fadeout_time=1000):
        """Para a música de fundo com fadeout"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fadeout_time)
            self.music_active = False
    
    def adjust_music_volume(self, volume=None, fade_time=1000):
        """Ajusta o volume da música de fundo com fadeout suave"""
        if volume is not None:
            self.music_volume = max(0.0, min(1.0, volume))  # Limita entre 0.0 e 1.0
        
        if pygame.mixer.music.get_busy():
            current_volume = pygame.mixer.music.get_volume()
            steps = 20
            delay = fade_time / steps
            volume_step = (self.music_volume - current_volume) / steps
            
            # Função que ajusta o volume gradualmente
            def fade_volume():
                for i in range(steps):
                    new_volume = current_volume + (volume_step * (i + 1))
                    new_volume = max(0.0, min(1.0, new_volume))  # Limita entre 0.0 e 1.0
                    pygame.mixer.music.set_volume(new_volume)
                    pygame.time.delay(int(delay))
            
            # Inicia fade em thread separada para não bloquear o jogo
            import threading
            fade_thread = threading.Thread(target=fade_volume)
            fade_thread.daemon = True
            fade_thread.start()
    
    def increase_music_volume_on_progress(self, score):
        """Aumenta o volume da música quando o jogador alcança determinada pontuação"""
        if score >= 2 and pygame.mixer.music.get_busy() and pygame.mixer.music.get_volume() < self.target_volume:
            self.adjust_music_volume(self.target_volume)