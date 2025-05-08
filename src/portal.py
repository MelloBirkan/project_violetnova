import pygame
import math
import random

class Portal:
    WIDTH = 60
    HEIGHT = 100
    
    def __init__(self, x, y, target_planet):
        self.x = x
        self.y = y
        self.target_planet = target_planet
        self.active = True
        
        # Variáveis de animação
        self.animation_counter = 0
        self.particles = []
        self.generate_particles()
        
        # Cores para diferentes portais de planetas
        self.portal_colors = {
            "Moon": (200, 200, 200),       # Prata
            "Mercury": (255, 165, 0),     # Laranja
            "Venus": (255, 215, 0),       # Dourado
            "Earth": (0, 191, 255),       # Azul Céu Profundo
            "Mars": (255, 69, 0),         # Vermelho-Laranja
            "Jupiter": (222, 184, 135),   # Marrom Arenoso
            "Saturn": (245, 222, 179),    # Trigo
            "Uranus": (64, 224, 208),     # Turquesa
            "Neptune": (65, 105, 225)     # Azul Royal
        }
        
        # Obtém cor com base no planeta alvo
        self.color = self.portal_colors.get(target_planet, (128, 0, 128))  # Roxo padrão
    
    def generate_particles(self):
        """Gera partículas para o efeito do portal"""
        self.particles = []
        for _ in range(20):
            angle = random.random() * 2 * math.pi
            speed = 0.5 + random.random() * 1.5
            size = 2 + random.random() * 4
            lifetime = 30 + random.random() * 30
            self.particles.append({
                "x": self.x + self.WIDTH // 2,
                "y": self.y + self.HEIGHT // 2,
                "angle": angle,
                "speed": speed,
                "size": size,
                "lifetime": lifetime,
                "current_life": lifetime
            })
    
    def update(self):
        """Atualiza a animação do portal"""
        self.animation_counter += 0.05
        
        # Atualiza partículas existentes
        for particle in self.particles:
            particle["x"] += math.cos(particle["angle"]) * particle["speed"]
            particle["y"] += math.sin(particle["angle"]) * particle["speed"]
            particle["current_life"] -= 1
            
            # Reinicia partículas mortas
            if particle["current_life"] <= 0:
                particle["x"] = self.x + self.WIDTH // 2
                particle["y"] = self.y + self.HEIGHT // 2
                particle["angle"] = random.random() * 2 * math.pi
                particle["current_life"] = particle["lifetime"]
    
    def draw(self, screen):
        """Desenha o portal"""
        if not self.active:
            return
            
        # Desenha a forma principal do portal (oval com efeito pulsante)
        pulse = math.sin(self.animation_counter) * 0.2 + 0.8  # Fator de escala de 0.6 a 1.0
        
        # Desenha brilho externo
        glow_color = (self.color[0], self.color[1], self.color[2], 100)  # Adiciona alfa
        glow_surface = pygame.Surface((self.WIDTH + 20, self.HEIGHT + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface, glow_color, 
                          (0, 0, self.WIDTH + 20, self.HEIGHT + 20))
        
        # Aplica efeito de pulso à posição do brilho
        glow_x = self.x - 10 + (1 - pulse) * 5
        glow_y = self.y - 10 + (1 - pulse) * 5
        screen.blit(glow_surface, (glow_x, glow_y))
        
        # Desenha portal principal
        width = int(self.WIDTH * pulse)
        height = int(self.HEIGHT * pulse)
        x = self.x + (self.WIDTH - width) // 2
        y = self.y + (self.HEIGHT - height) // 2
        
        pygame.draw.ellipse(screen, self.color, (x, y, width, height))
        
        # Elipse interna mais escura
        inner_width = width * 0.7
        inner_height = height * 0.7
        inner_x = self.x + (self.WIDTH - inner_width) // 2
        inner_y = self.y + (self.HEIGHT - inner_height) // 2
        
        # Versão mais escura da cor
        darker_color = (max(0, self.color[0] - 60), 
                        max(0, self.color[1] - 60), 
                        max(0, self.color[2] - 60))
        pygame.draw.ellipse(screen, darker_color, 
                          (inner_x, inner_y, inner_width, inner_height))
        
        # Desenha partículas
        for particle in self.particles:
            # Calcula alfa com base na vida útil restante
            alpha = int(255 * (particle["current_life"] / particle["lifetime"]))
            particle_color = (self.color[0], self.color[1], self.color[2], alpha)
            particle_surface = pygame.Surface((int(particle["size"]), int(particle["size"])), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle_color, 
                             (int(particle["size"]) // 2, int(particle["size"]) // 2), 
                             int(particle["size"]) // 2)
            screen.blit(particle_surface, 
                       (int(particle["x"] - particle["size"] // 2), 
                        int(particle["y"] - particle["size"] // 2)))
    
    def check_collision(self, spacecraft):
        """Verifica se a nave espacial entrou no portal"""
        if not self.active:
            return False
            
        # Colisão simples de retângulo
        # Ajusta x para centralizar a colisão dentro do sprite visual, se necessário
        spacecraft_hitbox_x = spacecraft.x + spacecraft.flame_extent + (spacecraft.WIDTH - spacecraft.HITBOX_WIDTH) / 2
        spacecraft_hitbox_y = spacecraft.y + (spacecraft.HEIGHT - spacecraft.HITBOX_HEIGHT) / 2

        spacecraft_rect = pygame.Rect(spacecraft_hitbox_x, spacecraft_hitbox_y, spacecraft.HITBOX_WIDTH, spacecraft.HITBOX_HEIGHT)
        portal_rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        
        return spacecraft_rect.colliderect(portal_rect)