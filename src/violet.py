import pygame
import math
import random

class Violet:
    WIDTH = 80
    HEIGHT = 80

    # Cores para diferentes tipos de expressão
    COLORS = {
        "normal": (147, 112, 219),  # Violeta
        "excited": (186, 85, 211),  # Orquídea médio
        "curious": (138, 43, 226),  # Azul violeta
        "surprised": (128, 0, 128), # Roxo
        "warning": (255, 20, 147),  # Rosa profundo
        "happy": (218, 112, 214),   # Orquídea
        "alert": (199, 21, 133),    # Violeta avermelhado
        "hint": (221, 160, 221)     # Ameixa
    }
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 10  # Posição na esquerda
        self.y = 10
        self.expression = "normal"
        self.previous_expression = "normal"
        self.transition_progress = 1.0  # 1.0 significa sem transição
        
        # Variáveis de animação
        self.pulse_factor = 1.0
        self.pulse_direction = 1
        self.pulse_speed = 0.005
        self.pulse_min = 0.95
        self.pulse_max = 1.05
        
        # Sistema de partículas
        self.particles = []
        self.particle_timer = 0
        self.particle_spawn_delay = 5  # Quadros entre a geração de partículas
        
        # Cria a superfície inicial
        self.update_surface()
        
    def update_surface(self):
        """Atualiza a superfície do personagem Violet com a expressão atual"""
        scaled_width = int(self.WIDTH * self.pulse_factor)
        scaled_height = int(self.HEIGHT * self.pulse_factor)

        self.surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))  # Transparente

        # Determina a cor com base na expressão ou transição
        if self.transition_progress < 1.0:
            # Durante a transição, mescla as cores
            curr_color = self.COLORS[self.expression]
            prev_color = self.COLORS[self.previous_expression]
            blend_color = [
                int(prev_color[0] * (1-self.transition_progress) + curr_color[0] * self.transition_progress),
                int(prev_color[1] * (1-self.transition_progress) + curr_color[1] * self.transition_progress),
                int(prev_color[2] * (1-self.transition_progress) + curr_color[2] * self.transition_progress)
            ]
            color = (blend_color[0], blend_color[1], blend_color[2], 230)
        else:
            # Sem transição, usa a cor da expressão atual
            color = (*self.COLORS[self.expression], 230)

        # Desenha os círculos externo e interno
        pygame.draw.circle(self.surface, (50, 50, 50, 200),
                          (scaled_width // 2, scaled_height // 2), scaled_width // 2)
        pygame.draw.circle(self.surface, color,
                          (scaled_width // 2, scaled_height // 2), scaled_width // 2 - 3)

        # Desenha uma expressão facial simples
        eye_size = scaled_width // 8
        mouth_width = scaled_width // 4
        
        # Diferentes expressões
        if self.expression == "normal":
            # Olhos normais
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2 - eye_size*2, scaled_height // 2 - eye_size), eye_size)
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2 + eye_size*2, scaled_height // 2 - eye_size), eye_size)
            # Boca neutra
            pygame.draw.line(self.surface, (255, 255, 255),
                           (scaled_width // 2 - mouth_width//2, scaled_height // 2 + eye_size*2),
                           (scaled_width // 2 + mouth_width//2, scaled_height // 2 + eye_size*2), 2)
                           
        elif self.expression == "happy" or self.expression == "excited":
            # Olhos felizes (semi-círculos)
            pygame.draw.arc(self.surface, (255, 255, 255),
                          (scaled_width // 2 - eye_size*2 - eye_size//2, scaled_height // 2 - eye_size*2, 
                           eye_size*2, eye_size*2), math.pi, 2*math.pi, 2)
            pygame.draw.arc(self.surface, (255, 255, 255),
                          (scaled_width // 2 + eye_size*1 - eye_size//2, scaled_height // 2 - eye_size*2, 
                           eye_size*2, eye_size*2), math.pi, 2*math.pi, 2)
            # Boca sorrindo
            pygame.draw.arc(self.surface, (255, 255, 255),
                          (scaled_width // 2 - mouth_width//2, scaled_height // 2, 
                           mouth_width, mouth_width), 0, math.pi, 2)
                           
        elif self.expression == "warning" or self.expression == "alert":
            # Olhos preocupados
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2 - eye_size*2, scaled_height // 2 - eye_size), eye_size)
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2 + eye_size*2, scaled_height // 2 - eye_size), eye_size)
            # Sobrancelhas inclinadas
            pygame.draw.line(self.surface, (255, 255, 255),
                           (scaled_width // 2 - eye_size*2 - eye_size, scaled_height // 2 - eye_size*2),
                           (scaled_width // 2 - eye_size*2 + eye_size, scaled_height // 2 - eye_size*2 - eye_size), 2)
            pygame.draw.line(self.surface, (255, 255, 255),
                           (scaled_width // 2 + eye_size*2 - eye_size, scaled_height // 2 - eye_size*2 - eye_size),
                           (scaled_width // 2 + eye_size*2 + eye_size, scaled_height // 2 - eye_size*2), 2)
            # Boca preocupada
            pygame.draw.arc(self.surface, (255, 255, 255),
                          (scaled_width // 2 - mouth_width//2, scaled_height // 2 + eye_size, 
                           mouth_width, mouth_width), math.pi, 2*math.pi, 2)
                           
        elif self.expression == "curious" or self.expression == "hint":
            # Olhos curiosos
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2 - eye_size*2, scaled_height // 2 - eye_size), eye_size)
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2 + eye_size*2, scaled_height // 2 - eye_size), eye_size * 1.3)  # Olho direito maior
            # Boca pensativa
            pygame.draw.arc(self.surface, (255, 255, 255),
                          (scaled_width // 2 - mouth_width//2, scaled_height // 2, 
                           mouth_width, mouth_width//2), math.pi/4, 3*math.pi/4, 2)
                           
        elif self.expression == "surprised":
            # Olhos surpresos (círculos maiores)
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2 - eye_size*2, scaled_height // 2 - eye_size), eye_size * 1.3)
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2 + eye_size*2, scaled_height // 2 - eye_size), eye_size * 1.3)
            # Boca surpresa (pequeno círculo)
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2, scaled_height // 2 + eye_size*2), eye_size)
        else:
            # Expressão padrão para casos não tratados
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2 - eye_size*2, scaled_height // 2 - eye_size), eye_size)
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (scaled_width // 2 + eye_size*2, scaled_height // 2 - eye_size), eye_size)
            pygame.draw.line(self.surface, (255, 255, 255),
                           (scaled_width // 2 - mouth_width//2, scaled_height // 2 + eye_size*2),
                           (scaled_width // 2 + mouth_width//2, scaled_height // 2 + eye_size*2), 2)
    
    def set_expression(self, expression):
        """Muda a expressão de Violet com transição suave"""
        if expression in self.COLORS and expression != self.expression:
            self.previous_expression = self.expression
            self.expression = expression
            self.transition_progress = 0.0  # Inicia a transição
            self.update_surface()
    
    def update(self):
        """Atualiza a animação de Violet"""
        # Atualiza a animação de pulsação
        self.pulse_factor += self.pulse_direction * self.pulse_speed
        if self.pulse_factor >= self.pulse_max:
            self.pulse_factor = self.pulse_max
            self.pulse_direction = -1
        elif self.pulse_factor <= self.pulse_min:
            self.pulse_factor = self.pulse_min
            self.pulse_direction = 1

        # Atualiza a transição de expressão
        if self.transition_progress < 1.0:
            self.transition_progress += 0.05  # Velocidade da transição
            if self.transition_progress >= 1.0:
                self.transition_progress = 1.0

        # Atualiza o sistema de partículas para expressões especiais
        if self.expression in ["excited", "alert", "surprised"]:
            self.particle_timer += 1
            if self.particle_timer >= self.particle_spawn_delay:
                self.particle_timer = 0
                # Adiciona nova partícula
                center_x = self.x + self.WIDTH // 2
                center_y = self.y + self.HEIGHT // 2
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(0.5, 2.0)
                size = random.uniform(2, 5)

                color = self.COLORS[self.expression]
                # Adiciona canal alfa
                color_with_alpha = (*color, 200)

                self.particles.append({
                    'x': center_x,
                    'y': center_y,
                    'dx': math.cos(angle) * speed,
                    'dy': math.sin(angle) * speed,
                    'size': size,
                    'color': color_with_alpha,
                    'life': 30  # Quadros até a partícula desaparecer
                })

        # Atualiza partículas existentes
        i = 0
        while i < len(self.particles):
            particle = self.particles[i]
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1

            if particle['life'] <= 0:
                self.particles.pop(i)
            else:
                i += 1
            
        # Sempre atualiza a superfície para a animação
        self.update_surface()
        
    def draw(self, screen):
        """Desenha Violet na tela"""
        # Desenha partículas atrás de Violet
        for particle in self.particles:
            # Calcula o alfa com base na vida restante
            alpha = int(255 * (particle['life'] / 30))
            color = (particle['color'][0], particle['color'][1], particle['color'][2], alpha)

            pygame.draw.circle(
                screen,
                color,
                (int(particle['x']), int(particle['y'])),
                int(particle['size'])
            )
            
        # Desenha o círculo de Violet (centralizado na posição original)
        center_x = self.x + (self.WIDTH // 2)
        center_y = self.y + (self.HEIGHT // 2)
        offset_x = center_x - (self.surface.get_width() // 2)
        offset_y = center_y - (self.surface.get_height() // 2)
        screen.blit(self.surface, (offset_x, offset_y))