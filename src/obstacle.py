import pygame
import random
import os

class Obstacle:
    WIDTH = 80
    GAP = 225  # Espaço entre obstáculos superior e inferior

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

    def __init__(self, x, gap_y, speed, obstacle_type=None, screen_height=720):
        self.x = x
        self.gap_y = gap_y
        self.speed = speed
        self.scored = False
        self.screen_height = screen_height
        self.using_sprites = False
        
        # Tenta carregar as imagens de sprites
        try:
            # Caminho para as imagens de obstáculos
            self.top_sprite_path = os.path.join("assets", "images", "obstaculo_cima_terra.png")
            self.bottom_sprite_path = os.path.join("assets", "images", "obstaculo_baixo_terra.png")
            
            # Carrega os sprites
            self.top_sprite = pygame.image.load(self.top_sprite_path)
            self.bottom_sprite = pygame.image.load(self.bottom_sprite_path)
            
            # Obtém as dimensões reais do sprite
            self.top_width = self.top_sprite.get_width()
            self.bottom_width = self.bottom_sprite.get_width()
            
            # Marca que estamos usando sprites
            self.using_sprites = True
        except (pygame.error, FileNotFoundError) as e:
            print(f"Não foi possível carregar os sprites de obstáculos: {e}")
            self.using_sprites = False

        # Seleciona aleatoriamente o tipo de obstáculo se não especificado
        if obstacle_type is None or obstacle_type not in self.TYPES:
            obstacle_type = random.choice(list(self.TYPES.keys()))
        self.type = obstacle_type
        self.colors = self.TYPES[self.type]

        # Cria superfícies do obstáculo
        self.create_obstacle_surfaces()

    def create_obstacle_surfaces(self):
        if self.using_sprites:
            # Quando usamos sprites, não precisamos criar superfícies personalizadas
            # Apenas definimos a posição para os obstáculos superior e inferior
            
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
        if self.using_sprites:
            # Desenha o obstáculo superior usando o sprite na posição correta
            # Não precisamos recortar - apenas posicionamos o sprite completo no topo
            # e ajustamos sua posição Y para que a base fique na posição gap_y - GAP/2
            top_y_position = (self.gap_y - self.GAP // 2) - self.top_sprite.get_height()
            
            # Garante que não desenhamos fora da tela (pode estar parcialmente visível)
            if top_y_position + self.top_sprite.get_height() > 0:
                screen.blit(self.top_sprite, (self.x, top_y_position))
            
            # Desenha o obstáculo inferior usando o sprite na posição gap_y + GAP/2
            bottom_y = self.gap_y + self.GAP // 2
            screen.blit(self.bottom_sprite, (self.x, bottom_y))
        else:
            # Desenha obstáculo superior
            screen.blit(self.top_obstacle, (self.x, 0))

            # Desenha obstáculo inferior
            bottom_obstacle_y = self.gap_y + self.GAP // 2
            screen.blit(self.bottom_obstacle, (self.x, bottom_obstacle_y))
