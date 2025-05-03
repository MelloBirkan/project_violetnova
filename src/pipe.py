import pygame

class Pipe:
    WIDTH = 80
    GAP = 150
    
    def __init__(self, x, gap_y, speed):
        self.x = x
        self.gap_y = gap_y
        self.speed = speed
        self.scored = False
        
        # Cria superfícies do cano
        self.top_pipe = pygame.Surface((self.WIDTH, self.gap_y - self.GAP // 2))
        self.top_pipe.fill((0, 128, 0))  # Cor verde
        
        bottom_pipe_height = 600 - self.gap_y - self.GAP // 2
        self.bottom_pipe = pygame.Surface((self.WIDTH, bottom_pipe_height))
        self.bottom_pipe.fill((0, 128, 0))  # Cor verde
        
        # Adiciona detalhes do cano
        pygame.draw.rect(self.top_pipe, (0, 100, 0), (0, self.top_pipe.get_height() - 30, self.WIDTH, 30))
        pygame.draw.rect(self.bottom_pipe, (0, 100, 0), (0, 0, self.WIDTH, 30))
    
    def update(self):
        # Move o cano para a esquerda
        self.x -= self.speed
    
    def draw(self, screen):
        # Desenha cano superior
        screen.blit(self.top_pipe, (self.x, 0))
        
        # Desenha cano inferior
        bottom_pipe_y = self.gap_y + self.GAP // 2
        screen.blit(self.bottom_pipe, (self.x, bottom_pipe_y))