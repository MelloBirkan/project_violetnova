import pygame
import random

class Obstacle:
    WIDTH = 80
    GAP = 225

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

    def __init__(self, x, gap_y, speed, obstacle_type=None, screen_height=600):
        self.x = x
        self.gap_y = gap_y
        self.speed = speed
        self.scored = False
        self.screen_height = screen_height

        # Seleciona aleatoriamente o tipo de obstáculo se não especificado
        if obstacle_type is None or obstacle_type not in self.TYPES:
            obstacle_type = random.choice(list(self.TYPES.keys()))
        self.type = obstacle_type
        self.colors = self.TYPES[self.type]

        # Cria superfícies do obstáculo
        self.create_obstacle_surfaces()

    def create_obstacle_surfaces(self):
        # Cria superfícies de obstáculo superior e inferior
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
        # Desenha obstáculo superior
        screen.blit(self.top_obstacle, (self.x, 0))

        # Desenha obstáculo inferior
        bottom_obstacle_y = self.gap_y + self.GAP // 2
        screen.blit(self.bottom_obstacle, (self.x, bottom_obstacle_y))
