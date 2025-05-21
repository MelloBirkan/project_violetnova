import pygame
import random
import os

class Obstacle:
    WIDTH = 80
    GAP = 225  # Espaço entre obstáculos superior e inferior

    # Cache para sprites já carregados, evitando carregamento repetido
    SPRITE_CACHE = {}

    @classmethod
    def _load_sprite(cls, path):
        """Carrega um sprite e armazena em cache."""
        if path not in cls.SPRITE_CACHE and os.path.exists(path):
            cls.SPRITE_CACHE[path] = pygame.image.load(path).convert_alpha()
        return cls.SPRITE_CACHE.get(path)

    # Tipos de obstáculos espaciais
    TYPES = {
        "asteroid": {
            "color": (139, 69, 19),  # Marrom sela
            "detail_color": (101, 67, 33)
        },
        "debris": {
            "color": (112, 128, 144),  # Cinza ardósia
            "detail_color": (47, 79, 79)  # Cinza ardósia escuro
        },
        "storm": {
            "color": (255, 165, 0),  # Laranja
            "detail_color": (255, 215, 0)  # Dourado
        }
    }

    def __init__(self, x, gap_y, speed, obstacle_type=None, screen_height=720, planet_name="Earth"):
        self.x = x
        self.gap_y = gap_y
        self.speed = speed
        self.scored = False
        self.screen_height = screen_height
        self.using_sprites = False
        self.planet_name = planet_name
        # Todos os planetas têm dois obstáculos agora
        self.has_two_obstacles = True
        self.top_sprite = None
        self.bottom_sprite = None
        self.top_width = self.WIDTH
        self.bottom_width = self.WIDTH
        
        # Tradução de nomes de planetas para caminhos de arquivo
        planet_folder_names = {
            "Earth": "terra",
            "Mercury": "mercurio",
            "Venus": "venus",
            "Mars": "marte",
            "Jupiter": "jupiter",
            "Saturn": "saturno",
            "Moon": "lua",
            "Uranus": "urano",
            "Neptune": "netuno"
        }
        
        folder_name = planet_folder_names.get(planet_name, "terra")
        
        # Tenta carregar as imagens de sprites específicas do planeta
        try:
            # Earth tem obstáculos específicos para cima e baixo
            if planet_name == "Earth":
                self.top_sprite_path = os.path.join("assets", "images", "planets_sprites", folder_name, f"obstaculo_cima_{folder_name}.png")
                self.bottom_sprite_path = os.path.join("assets", "images", "planets_sprites", folder_name, f"obstaculo_baixo_{folder_name}.png")
                
                # Verificando existência dos arquivos antes de carregar
                if os.path.exists(self.top_sprite_path) and os.path.exists(self.bottom_sprite_path):
                    # Carrega os sprites usando cache
                    self.top_sprite = self._load_sprite(self.top_sprite_path)
                    self.bottom_sprite = self._load_sprite(self.bottom_sprite_path)
                    
                    # Obtém as dimensões reais dos sprites
                    self.top_width = self.top_sprite.get_width()
                    self.bottom_width = self.bottom_sprite.get_width()
                    
                    # Marca que estamos usando sprites
                    self.using_sprites = True
                else:
                    print(f"Arquivos de sprite para {planet_name} não encontrados, usando fallback")
                    self.using_sprites = False
            else:
                # Outros planetas usam o mesmo sprite para ambos os obstáculos
                obstacle_path = os.path.join("assets", "images", "planets_sprites", folder_name, f"obstaculo_{folder_name}.png")
                
                # Verificando existência do arquivo antes de carregar
                if os.path.exists(obstacle_path):
                    obstacle_sprite = self._load_sprite(obstacle_path)
                    
                    # Usa o mesmo sprite para o topo e a base
                    self.top_sprite = obstacle_sprite
                    self.bottom_sprite = obstacle_sprite
                    
                    # Obtém as dimensões reais do sprite
                    self.top_width = obstacle_sprite.get_width()
                    self.bottom_width = obstacle_sprite.get_width()
                    
                    # Marca que estamos usando sprites
                    self.using_sprites = True
                else:
                    print(f"Arquivo de sprite para {planet_name} não encontrado, usando fallback")
                    self.using_sprites = False
        except (pygame.error, FileNotFoundError) as e:
            print(f"Não foi possível carregar os sprites de obstáculos para {planet_name}: {e}")
            self.using_sprites = False
            
        # Cria superfícies de fallback para quando não há sprites
        if not self.using_sprites:
            self._create_fallback_obstacles(obstacle_type)

        # Seleciona aleatoriamente o tipo de obstáculo se não especificado
        if obstacle_type is None or obstacle_type not in self.TYPES:
            obstacle_type = random.choice(list(self.TYPES.keys()))
        self.type = obstacle_type
        self.colors = self.TYPES[self.type]

        # Cria superfícies do obstáculo
        self.create_obstacle_surfaces()
        
    def _create_fallback_obstacles(self, obstacle_type):
        """Cria obstáculos de fallback quando sprites não estão disponíveis"""
        # Determina o tipo de obstáculo
        if obstacle_type is None or obstacle_type not in self.TYPES:
            obstacle_type = random.choice(list(self.TYPES.keys()))
        self.type = obstacle_type
        self.colors = self.TYPES[self.type]
        
        # Cria obstáculo superior
        top_obstacle_height = self.gap_y - self.GAP // 2
        # Garante que a altura seja de pelo menos 1 pixel
        top_obstacle_height = max(1, top_obstacle_height)
        self.top_obstacle = pygame.Surface((self.WIDTH, top_obstacle_height))
        self.top_obstacle.fill(self.colors["color"])
        
        # Cria obstáculo inferior
        bottom_obstacle_height = self.screen_height - self.gap_y - self.GAP // 2
        # Garante que a altura seja de pelo menos 1 pixel
        bottom_obstacle_height = max(1, bottom_obstacle_height)
        self.bottom_obstacle = pygame.Surface((self.WIDTH, bottom_obstacle_height))
        self.bottom_obstacle.fill(self.colors["color"])
        
        # Adiciona detalhes aos obstáculos
        if self.type == "asteroid":
            self._add_asteroid_details(self.top_obstacle)
            self._add_asteroid_details(self.bottom_obstacle)
        elif self.type == "debris":
            self._add_debris_details(self.top_obstacle)
            self._add_debris_details(self.bottom_obstacle)
        elif self.type == "storm":
            self._add_storm_details(self.top_obstacle)
            self._add_storm_details(self.bottom_obstacle)

    def create_obstacle_surfaces(self):
        if self.using_sprites:
            # Quando usamos sprites, padronizamos os sprites para garantir consistência
            
            # Redimensiona os sprites para a largura padrão, mantendo a proporção
            if self.top_width != self.WIDTH:
                top_height = int(self.top_sprite.get_height() * (self.WIDTH / self.top_width))
                self.top_sprite = pygame.transform.scale(self.top_sprite, (self.WIDTH, top_height))
                self.top_width = self.WIDTH
                
            if hasattr(self, 'bottom_width') and self.bottom_width != self.WIDTH:
                bottom_height = int(self.bottom_sprite.get_height() * (self.WIDTH / self.bottom_width))
                self.bottom_sprite = pygame.transform.scale(self.bottom_sprite, (self.WIDTH, bottom_height))
                self.bottom_width = self.WIDTH
            
            # Para o obstáculo superior, ajustamos sua posição Y
            # A parte superior do obstáculo fica na posição 0, 
            # mas precisamos ajustar a altura para que o espaço fique na posição gap_y - GAP/2
            self.top_y = 0
            self.top_sprite_height = self.gap_y - self.GAP // 2
            
            # Para o obstáculo inferior, calculamos a posição Y
            self.bottom_y = self.gap_y + self.GAP // 2
        else:
            # Se não estivermos usando sprites, criamos superfícies como antes
            top_obstacle_height = self.gap_y - self.GAP // 2
            # Garante que a altura seja de pelo menos 1 pixel para evitar dimensões de superfície inválidas
            top_obstacle_height = max(1, top_obstacle_height)
            self.top_obstacle = pygame.Surface((self.WIDTH, top_obstacle_height))
            self.top_obstacle.fill(self.colors["color"])

            bottom_obstacle_height = self.screen_height - self.gap_y - self.GAP // 2
            # Garante que a altura seja de pelo menos 1 pixel para evitar dimensões de superfície inválidas
            bottom_obstacle_height = max(1, bottom_obstacle_height)
            self.bottom_obstacle = pygame.Surface((self.WIDTH, bottom_obstacle_height))
            self.bottom_obstacle.fill(self.colors["color"])

            # Adiciona detalhes do obstáculo com base no tipo
            if self.type == "asteroid":
                # Adiciona detalhes semelhantes a crateras aos asteroides
                self._add_asteroid_details(self.top_obstacle)
                self._add_asteroid_details(self.bottom_obstacle)

            elif self.type == "debris":
                # Adiciona detalhes metálicos/tecnológicos aos detritos
                self._add_debris_details(self.top_obstacle)
                self._add_debris_details(self.bottom_obstacle)

            elif self.type == "storm":
                # Adiciona padrão de redemoinho às tempestades solares
                self._add_storm_details(self.top_obstacle)
                self._add_storm_details(self.bottom_obstacle)

    def _add_asteroid_details(self, surface):
        # Adiciona círculos semelhantes a crateras ao asteroide
        width, height = surface.get_size()
        for _ in range(width // 10):
            x = random.randint(5, width - 5)
            y = random.randint(5, height - 5)
            radius = random.randint(3, 8)
            pygame.draw.circle(surface, self.colors["detail_color"], (x, y), radius)

    def _add_debris_details(self, surface):
        # Adiciona detalhes de detritos tecnológicos (retângulos e linhas)
        width, height = surface.get_size()
        for _ in range(width // 15):
            x = random.randint(5, width - 15)
            y = random.randint(5, height - 15)
            w = random.randint(5, 15)
            h = random.randint(5, 15)
            pygame.draw.rect(surface, self.colors["detail_color"], (x, y, w, h))

            # Adiciona algumas linhas para representar detalhes tecnológicos
            line_x = random.randint(0, width - 1)
            pygame.draw.line(surface, (200, 200, 200), 
                             (line_x, 0), 
                             (line_x, random.randint(10, 30)))

    def _add_storm_details(self, surface):
        # Adiciona padrão de redemoinho para representar tempestades solares
        width, height = surface.get_size()

        # Cria padrões semelhantes a ondas
        for y in range(0, height, 10):
            amplitude = random.randint(5, 15)
            for x in range(0, width, 2):
                wave_y = y + int(amplitude * ((x / width) * 2 - 1) ** 2)
                if 0 <= wave_y < height and 0 <= x < width:
                    surface.set_at((x, wave_y), self.colors["detail_color"])

    def update(self):
        # Move o obstáculo para a esquerda
        self.x -= self.speed

    def draw(self, screen):
        if self.using_sprites and self.top_sprite is not None and self.bottom_sprite is not None:
            # Para todos os planetas, sempre desenhar ambos os obstáculos
            # Desenha o obstáculo superior
            top_y_position = (self.gap_y - self.GAP // 2) - self.top_sprite.get_height()
            
            # Garante que não desenhamos fora da tela (pode estar parcialmente visível)
            if top_y_position + self.top_sprite.get_height() > 0:
                screen.blit(self.top_sprite, (self.x, top_y_position))
            
            # Desenha o obstáculo inferior
            bottom_y = self.gap_y + self.GAP // 2
            screen.blit(self.bottom_sprite, (self.x, bottom_y))
        else:
            # Desenha obstáculo superior e inferior quando não há sprites
            if hasattr(self, 'top_obstacle') and hasattr(self, 'bottom_obstacle'):
                # Verifica se os obstáculos fallback foram criados corretamente
                
                # Sempre desenha ambos os obstáculos para todos os planetas
                # Desenha obstáculo superior
                screen.blit(self.top_obstacle, (self.x, 0))
                
                # Desenha obstáculo inferior
                bottom_obstacle_y = self.gap_y + self.GAP // 2
                screen.blit(self.bottom_obstacle, (self.x, bottom_obstacle_y))
