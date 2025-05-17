import pygame
import random

class Collectible:
    WIDTH = 30
    HEIGHT = 30
    
    # Tipos de colecionáveis
    TYPES = {
        "data": {
            "color": (0, 191, 255),  # Azul céu profundo
            "value": 0,  # Valor em pontos
            "effect": "info"  # Mostra informações do planeta
        },
        "weapon": {
            "color": (220, 20, 60),  # Carmesim
            "value": 0,  # Valor em pontos
            "effect": "attack"  # Permite destruir obstáculos
        },
        "life": {
            "color": (50, 220, 50),  # Verde brilhante
            "value": 0,  # Valor em pontos
            "effect": "life"  # Adiciona uma vida extra
        }
    }
    
    def __init__(self, x, y, collectible_type=None, quiz_index=None):
        self.x = x
        self.y = y
        self.collected = False
        self.animation_counter = 0
        self.bob_offset = 0  # Para animação flutuante
        self.quiz_index = quiz_index  # Índice da pergunta do quiz associada
        
        # Seleciona aleatoriamente o tipo de colecionável se não especificado
        if collectible_type is None or collectible_type not in self.TYPES:
            # Padrão para tipos disponíveis (dados ou arma)
            collectible_type = random.choice(list(self.TYPES.keys()))
        self.type = collectible_type
        self.properties = self.TYPES[self.type]
        
        # Cria superfície do colecionável
        self.create_collectible_surface()
    
    def create_collectible_surface(self):
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))  # Fundo transparente
        
        color = self.properties["color"]
        
        # Formas diferentes baseadas no tipo de colecionável
        if self.type == "data":
            # Módulo de dados (hexágono com detalhes internos)
            pygame.draw.polygon(self.surface, color, [
                (self.WIDTH//2, 0),                    # Topo
                (self.WIDTH, self.HEIGHT//4),         # Canto superior direito
                (self.WIDTH, self.HEIGHT*3//4),       # Canto inferior direito
                (self.WIDTH//2, self.HEIGHT),         # Base
                (0, self.HEIGHT*3//4),               # Canto inferior esquerdo
                (0, self.HEIGHT//4)                  # Canto superior esquerdo
            ])
            # Detalhes internos
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (self.WIDTH//2, self.HEIGHT//2), self.WIDTH//4)
            pygame.draw.lines(self.surface, (0, 0, 0), False, [
                (self.WIDTH//4, self.HEIGHT//2),
                (self.WIDTH*3//4, self.HEIGHT//2)
            ], 2)
            pygame.draw.lines(self.surface, (0, 0, 0), False, [
                (self.WIDTH//2, self.HEIGHT//4),
                (self.WIDTH//2, self.HEIGHT*3//4)
            ], 2)
            # Ícone de dica de quiz (apenas se for um colecionável de dados com quiz)
            if self.quiz_index is not None:
                font = pygame.font.Font(None, 18)
                text = font.render("?", True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
                self.surface.blit(text, text_rect)
            
        elif self.type == "fuel":
            # Contêiner de combustível (cilindro)
            pygame.draw.rect(self.surface, color, 
                           (self.WIDTH//4, self.HEIGHT//6, self.WIDTH//2, self.HEIGHT*2//3))
            pygame.draw.ellipse(self.surface, color,
                              (self.WIDTH//4, self.HEIGHT//6 - self.HEIGHT//12, 
                               self.WIDTH//2, self.HEIGHT//6))
            pygame.draw.ellipse(self.surface, color,
                              (self.WIDTH//4, self.HEIGHT*5//6 - self.HEIGHT//12, 
                               self.WIDTH//2, self.HEIGHT//6))
            # Indicador de nível de combustível
            pygame.draw.rect(self.surface, (255, 0, 0),
                           (self.WIDTH*3//8, self.HEIGHT//3, self.WIDTH//4, self.HEIGHT//3))
            
        elif self.type == "weapon":
            # Arma (forma de estrela)
            points = []
            for i in range(10):
                angle = 2 * 3.14159 * i / 10
                radius = self.WIDTH//2 if i % 2 == 0 else self.WIDTH//4
                points.append((
                    self.WIDTH//2 + int(radius * 0.9 * (0 if i % 2 != 0 else 1) * 0.8 * (0.5 if i == 0 else 1) * (0.5 if i == 4 else 1) * (0.6 if i == 6 else 1) * (0.7 if i == 8 else 1) * (0.8 if i == 2 else 1) * (-1 if i > 5 else 1)),
                    self.HEIGHT//2 + int(radius * 0.9 * (0 if i % 2 != 0 else 1) * 0.8 * (0.5 if i == 2 else 1) * (0.5 if i == 6 else 1) * (0.6 if i == 0 else 1) * (0.7 if i == 8 else 1) * (0.8 if i == 4 else 1) * (-1 if i > 7 or i < 3 else 1))
                ))
            pygame.draw.polygon(self.surface, color, points)
            # Círculo interno
            pygame.draw.circle(self.surface, (255, 255, 255),
                             (self.WIDTH//2, self.HEIGHT//2), self.WIDTH//6)
                             
        elif self.type == "life":
            # Vida (forma de coração)
            center_x, center_y = self.WIDTH//2, self.HEIGHT//2 - 2
            
            # Desenha as duas partes superiores do coração
            pygame.draw.circle(self.surface, color, (center_x - 6, center_y - 3), 8)
            pygame.draw.circle(self.surface, color, (center_x + 6, center_y - 3), 8)
            
            # Desenha a parte inferior do coração
            points = [
                (center_x - 14, center_y + 1),
                (center_x, center_y + 14),
                (center_x + 14, center_y + 1),
                (center_x, center_y - 2)
            ]
            pygame.draw.polygon(self.surface, color, points)
            
            # Adiciona um brilho no coração
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (center_x - 4, center_y - 3), 3)
    
    def update(self):
        # Animação flutuante
        self.animation_counter += 0.1
        self.bob_offset = int(3 * (0.5 - 0.5 * (self.animation_counter % 1)))
        
    def draw(self, screen):
        if not self.collected:
            # Aplica deslocamento para efeito flutuante
            screen.blit(self.surface, (self.x, self.y + self.bob_offset))
    
    def check_collision(self, spacecraft):
        """Verifica se a nave espacial coletou este item"""
        if self.collected:
            return False
            
        # Colisão simples de retângulo
        # Ajusta x para centralizar a hitbox dentro do sprite visual, se necessário
        spacecraft_hitbox_x = spacecraft.x + spacecraft.flame_extent + (spacecraft.WIDTH - spacecraft.HITBOX_WIDTH) / 2
        spacecraft_hitbox_y = spacecraft.y + (spacecraft.HEIGHT - spacecraft.HITBOX_HEIGHT) / 2

        spacecraft_rect = pygame.Rect(spacecraft_hitbox_x, spacecraft_hitbox_y, spacecraft.HITBOX_WIDTH, spacecraft.HITBOX_HEIGHT)
        collectible_rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        
        if spacecraft_rect.colliderect(collectible_rect):
            self.collected = True
            return True
        
        return False
    
    def get_effect(self):
        """Retorna o efeito deste colecionável"""
        return {
            "type": self.type,
            "effect": self.properties["effect"],
            "value": self.properties["value"],
            "quiz_index": self.quiz_index
        }