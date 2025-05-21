import pygame
import os
import math
import json
import src.config as config
from src.planet_data import PLANET_NAME_PT

class MusicPlayer:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_track_index = 0
        self.is_playing = False
        self.unlocked_planets = []
        self.music_files = {
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
        self.planet_order = ["Earth", "Mercury", "Venus", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
        self.track_names = []
        self.selected_track = 0
        self.load_unlocked_planets()
        
    def load_unlocked_planets(self):
        """Carrega os planetas desbloqueados do arquivo de progresso"""
        try:
            with open("planet_progress.json", "r") as file:
                progress = json.load(file)
                furthest_planet = progress.get("furthest_planet", "earth").lower()
                
                # Debug para verificar o planeta mais distante
                print(f"Furthest planet from progress file: {furthest_planet}")
                
                # Limpa a lista de faixas
                self.track_names = []
                self.unlocked_planets = []
                
                # Ordem correta dos planetas
                planet_order_map = {
                    "earth": 0,
                    "mercury": 1,
                    "venus": 2,
                    "moon": 3,
                    "mars": 4,
                    "jupiter": 5,
                    "saturn": 6,
                    "uranus": 7,
                    "neptune": 8
                }
                
                # Obtém o índice do planeta mais distante alcançado
                furthest_idx = planet_order_map.get(furthest_planet, 0)
                print(f"Furthest planet index: {furthest_idx}")
                
                # Popula as listas com planetas desbloqueados
                for planet in self.planet_order:
                    planet_lower = planet.lower()
                    planet_idx = planet_order_map.get(planet_lower, 0)
                    
                    # Se o planeta está até o mais distante, está desbloqueado
                    if planet_idx <= furthest_idx:
                        self.unlocked_planets.append(planet)
                        # Adiciona a faixa desbloqueada com o nome traduzido
                        self.track_names.append({
                            "planet": planet,
                            "name": self.music_files[planet],
                            "pt_name": PLANET_NAME_PT.get(planet, planet)
                        })
                
                # Se não há faixas desbloqueadas, desbloqueia pelo menos a Terra
                if not self.track_names:
                    self.unlocked_planets.append("Earth")
                    self.track_names.append({
                        "planet": "Earth",
                        "name": self.music_files["Earth"],
                        "pt_name": PLANET_NAME_PT.get("Earth", "Earth")
                    })
                    
                # Debug para verificar os planetas desbloqueados
                print(f"Unlocked planets: {self.unlocked_planets}")
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Erro ao carregar progresso do planeta: {e}")
            # Se ocorrer um erro, desbloqueia apenas a Terra
            self.unlocked_planets = ["Earth"]
            self.track_names = [{
                "planet": "Earth",
                "name": self.music_files["Earth"],
                "pt_name": PLANET_NAME_PT.get("Earth", "Earth")
            }]
    
    def handle_event(self, event):
        """Processa eventos de entrada para o player de música"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Seleciona a faixa anterior
                self.selected_track = (self.selected_track - 1) % len(self.track_names)
            elif event.key == pygame.K_DOWN:
                # Seleciona a próxima faixa
                self.selected_track = (self.selected_track + 1) % len(self.track_names)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                # Reproduz ou pausa a faixa selecionada
                self.toggle_play()
            elif event.key == pygame.K_ESCAPE:
                # Volta ao menu principal
                if self.is_playing:
                    pygame.mixer.music.fadeout(500)
                    self.is_playing = False
                return False
        
        return True
    
    def toggle_play(self):
        """Inicia ou pausa a reprodução da faixa selecionada"""
        if not self.track_names:
            return
            
        track = self.track_names[self.selected_track]
        
        if self.is_playing and pygame.mixer.music.get_busy():
            # Pause music
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            # Se a música atual for diferente da selecionada, carrega e inicia
            if track["planet"] != self.current_track_index or not pygame.mixer.music.get_busy():
                music_path = os.path.join("assets", "musics", track["name"])
                if os.path.exists(music_path):
                    # Tenta carregar a nova música
                    try:
                        pygame.mixer.music.load(music_path)
                        pygame.mixer.music.play(-1)  # Loop infinito
                        pygame.mixer.music.set_volume(0.7)  # Volume padrão
                        self.current_track_index = track["planet"]
                        self.is_playing = True
                    except pygame.error as e:
                        print(f"Erro ao reproduzir música: {e}")
                        # Tenta recuperar o mixer em caso de falha
                        try:
                            pygame.mixer.quit()
                            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
                            pygame.time.delay(500)
                            pygame.mixer.music.load(music_path)
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.7)
                            self.current_track_index = track["planet"]
                            self.is_playing = True
                        except pygame.error as e2:
                            print(f"Falha na recuperação do mixer: {e2}")
                            self.is_playing = False
            else:
                # Continua reproduzindo a mesma música que foi pausada
                pygame.mixer.music.unpause()
                self.is_playing = True
    
    def draw(self, screen):
        """Desenha a interface do player de música"""
        # Fundo
        background = pygame.Surface((self.screen_width, self.screen_height))
        background.fill((10, 10, 40))  # Azul escuro espacial
        
        # Adiciona um gradiente do centro para as bordas
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        center_x, center_y = self.screen_width // 2, self.screen_height // 2
        max_radius = int(math.sqrt(center_x**2 + center_y**2))
        
        for radius in range(0, max_radius, 2):
            alpha = 255 - int(255 * (radius / max_radius) * 0.8)
            pygame.draw.circle(overlay, (50, 50, 100, alpha), (center_x, center_y), radius)
        
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))
        
        # Título
        title_text = config.GAME_FONT.render("PLAYER DE MÚSICA", True, (255, 255, 255))
        subtitle_text = config.SMALL_FONT.render("Sistema Solar Sonoro", True, (200, 200, 255))
        
        screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 80))
        screen.blit(subtitle_text, (self.screen_width // 2 - subtitle_text.get_width() // 2, 130))
        
        # Player central
        player_width = 600
        player_height = 400
        player_x = self.screen_width // 2 - player_width // 2
        player_y = 180
        
        # Desenha o quadro do player com borda brilhante
        player_background = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
        player_background.fill((0, 0, 30, 180))
        screen.blit(player_background, (player_x, player_y))
        
        # Borda brilhante
        border_color = (100, 100, 255)
        border_width = 2
        pygame.draw.rect(screen, border_color, (player_x, player_y, player_width, player_height), border_width, border_radius=10)
        
        # Área de listagem de faixas
        tracks_y = player_y + 60
        track_height = 40
        visible_tracks = 7  # Número de faixas visíveis
        
        # Desenha as faixas disponíveis
        if self.track_names:
            # Adiciona uma rolagem se houver mais faixas do que espaço visível
            start_idx = max(0, min(self.selected_track - visible_tracks // 2, len(self.track_names) - visible_tracks))
            end_idx = min(start_idx + visible_tracks, len(self.track_names))
            
            # Título da seção
            tracks_title = config.GAME_FONT.render("Faixas Desbloqueadas", True, (255, 255, 255))
            screen.blit(tracks_title, (player_x + player_width // 2 - tracks_title.get_width() // 2, player_y + 20))
            
            for i, track_data in enumerate(self.track_names[start_idx:end_idx]):
                track_idx = start_idx + i
                y_pos = tracks_y + i * track_height
                
                # Destaca a faixa selecionada
                if track_idx == self.selected_track:
                    # Caixa de seleção
                    selection_rect = pygame.Rect(player_x + 20, y_pos, player_width - 40, track_height - 5)
                    pygame.draw.rect(screen, (50, 50, 150), selection_rect, border_radius=5)
                    pygame.draw.rect(screen, (100, 100, 255), selection_rect, 2, border_radius=5)
                    
                    # Efeito de brilho para a faixa selecionada
                    glow_surf = pygame.Surface((selection_rect.width + 20, selection_rect.height + 20), pygame.SRCALPHA)
                    for offset in range(3):
                        alpha = 30 - (offset * 10)
                        pygame.draw.rect(glow_surf, (100, 100, 255, alpha), 
                                        (10 - offset * 3, 10 - offset * 3, 
                                         selection_rect.width + offset * 6, selection_rect.height + offset * 6), 
                                        2, border_radius=5)
                    screen.blit(glow_surf, (selection_rect.x - 10, selection_rect.y - 10))
                
                # Nome da faixa e planeta
                planet_text = track_data["pt_name"]
                track_name = track_data["name"].replace(".mp3", "")
                
                # Status de reprodução
                if self.is_playing and self.current_track_index == track_data["planet"]:
                    status_icon = "▶" if pygame.mixer.music.get_busy() else "⏸"
                else:
                    status_icon = ""
                
                # Desenha o texto da faixa
                track_font_color = (255, 255, 255) if track_idx == self.selected_track else (200, 200, 200)
                track_text = config.SMALL_FONT.render(f"{status_icon} {planet_text}: {track_name}", True, track_font_color)
                screen.blit(track_text, (player_x + 30, y_pos + 10))
        else:
            # Mensagem se não houver faixas
            no_tracks_text = config.SMALL_FONT.render("Nenhuma faixa desbloqueada ainda!", True, (255, 100, 100))
            screen.blit(no_tracks_text, (player_x + player_width // 2 - no_tracks_text.get_width() // 2, tracks_y + 100))
        
        # Informações da faixa atual ou mensagem de reprodução
        current_info_y = player_y + player_height - 80
        
        if self.is_playing and pygame.mixer.music.get_busy() and self.track_names:
            current_track = self.track_names[self.selected_track]
            current_planet = current_track["pt_name"]
            current_name = current_track["name"].replace(".mp3", "")
            
            now_playing = config.SMALL_FONT.render("Reproduzindo agora:", True, (150, 150, 255))
            track_info = config.GAME_FONT.render(f"{current_planet}: {current_name}", True, (255, 255, 255))
            
            screen.blit(now_playing, (player_x + player_width // 2 - now_playing.get_width() // 2, current_info_y))
            screen.blit(track_info, (player_x + player_width // 2 - track_info.get_width() // 2, current_info_y + 30))
        else:
            not_playing = config.SMALL_FONT.render("Nenhuma música tocando", True, (150, 150, 150))
            screen.blit(not_playing, (player_x + player_width // 2 - not_playing.get_width() // 2, current_info_y + 15))
        
        # Instruções
        controls_y = player_y + player_height + 20
        controls_text1 = config.SMALL_FONT.render("SETA PARA CIMA/BAIXO - Selecionar faixa", True, (255, 255, 255))
        controls_text2 = config.SMALL_FONT.render("ESPAÇO/ENTER - Reproduzir/Pausar", True, (255, 255, 255))
        controls_text3 = config.SMALL_FONT.render("ESC - Voltar ao menu", True, (255, 255, 255))
        
        # Draw backgrounds for better readability
        for i, text in enumerate([controls_text1, controls_text2, controls_text3]):
            text_y = controls_y + i * 30
            bg_rect = pygame.Rect(
                self.screen_width // 2 - text.get_width() // 2 - 10,
                text_y - 2,
                text.get_width() + 20,
                24
            )
            pygame.draw.rect(screen, (0, 0, 30, 180), bg_rect, border_radius=5)
            screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, text_y))
        
        # Informação de desbloqueio
        unlock_info = config.SMALL_FONT.render("Explore o Sistema Solar para desbloquear mais faixas!", True, (200, 200, 200))
        screen.blit(unlock_info, (self.screen_width // 2 - unlock_info.get_width() // 2, self.screen_height - 40))