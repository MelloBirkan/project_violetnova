import pygame
import math
import random
import os

class Violet:
    # Dimensões base
    BASE_WIDTH = 200
    BASE_HEIGHT = 200
    
    # Tamanhos para foco/não-foco
    FOCUSED_SCALE = 1.3
    UNFOCUSED_SCALE = 0.9
    
    # Cores para diferentes expressões
    COLORS = {
        "normal": (255, 255, 255),       # Branco normal
        "excited": (255, 240, 240),      # Branco com tom rosa
        "curious": (240, 240, 255),      # Branco com tom azulado
        "surprised": (255, 255, 240),    # Branco com tom amarelado
        "warning": (255, 200, 200),      # Rosa claro
        "happy": (240, 255, 240),        # Verde muito claro
        "alert": (255, 180, 180),        # Rosa mais forte
        "hint": (240, 240, 255)          # Azul muito claro
    }
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Posição centralizada na tela
        self.x = screen_width // 2 - self.BASE_WIDTH // 2
        self.y = screen_height // 2 - self.BASE_HEIGHT // 2 - 50  # Um pouco acima do centro
        
        # Estado da expressão e foco
        self.expression = "normal"
        self.previous_expression = "normal"
        self.transition_progress = 1.0  # 1.0 significa sem transição
        self.is_focused = False
        self.focus_transition = 1.0  # Para transição suave entre foco/não-foco
        
        # Variáveis de animação
        self.pulse_factor = 1.0
        self.pulse_direction = 1
        self.pulse_speed = 0.003
        self.pulse_min = 0.97
        self.pulse_max = 1.03
        
        # Carrega a imagem de Violet (gatinha astronauta)
        self.image = None
        self.load_image()
        
        # Cria a superfície inicial
        self.surface = None
        self.update_surface()
        
    def load_image(self):
        """Carrega a imagem de Violet"""
        try:
            # Caminho para a imagem
            image_path = os.path.join('assets', 'images', 'violet.png')
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de Violet: {e}")
            # Cria uma superfície vazia como fallback se a imagem não puder ser carregada
            self.image = pygame.Surface((self.BASE_WIDTH, self.BASE_HEIGHT), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
    
    def set_focused(self, focused):
        """Define se Violet está em foco (falando) ou não"""
        if self.is_focused != focused:
            self.is_focused = focused
            self.focus_transition = 0.0  # Inicia a transição
    
    def set_expression(self, expression):
        """Muda a expressão de Violet com transição suave"""
        if expression in self.COLORS and expression != self.expression:
            self.previous_expression = self.expression
            self.expression = expression
            self.transition_progress = 0.0  # Inicia a transição
            self.update_surface()
    
    def update_surface(self):
        """Atualiza a superfície de Violet com a expressão atual e ajusta o foco"""
        if not self.image:
            return
            
        # Calcula o fator de escala com base no foco
        if self.focus_transition < 1.0:
            # Durante a transição, interpola entre os estados
            if self.is_focused:
                # Transição para foco: 0.9 -> 1.3
                scale = self.UNFOCUSED_SCALE + (self.FOCUSED_SCALE - self.UNFOCUSED_SCALE) * self.focus_transition
            else:
                # Transição para não-foco: 1.3 -> 0.9
                scale = self.FOCUSED_SCALE - (self.FOCUSED_SCALE - self.UNFOCUSED_SCALE) * self.focus_transition
        else:
            # Após a transição, usa o valor de escala final
            scale = self.FOCUSED_SCALE if self.is_focused else self.UNFOCUSED_SCALE
            
        # Aplica o efeito de pulsação ao fator de escala
        scale *= self.pulse_factor
        
        # Determina o tamanho final da imagem
        width = int(self.BASE_WIDTH * scale)
        height = int(self.BASE_HEIGHT * scale)
        
        # Calcula a mistura de cores para a expressão
        if self.transition_progress < 1.0:
            # Durante a transição de expressão, mescla as cores
            curr_color = self.COLORS[self.expression]
            prev_color = self.COLORS[self.previous_expression]
            color = [
                int(prev_color[0] * (1-self.transition_progress) + curr_color[0] * self.transition_progress),
                int(prev_color[1] * (1-self.transition_progress) + curr_color[1] * self.transition_progress),
                int(prev_color[2] * (1-self.transition_progress) + curr_color[2] * self.transition_progress)
            ]
        else:
            # Após a transição, usa a cor final
            color = self.COLORS[self.expression]
            
        # Determina a opacidade/brilho - mais brilhante quando em foco, mais suave quando não
        if self.is_focused:
            alpha = 255  # Totalmente opaca quando em foco
            blur_factor = 0  # Sem desfoque quando em foco
        else:
            alpha = 200  # Levemente transparente quando fora de foco
            blur_factor = 1  # Aplica leve desfoque quando fora de foco
            
        # Cria a superfície de trabalho
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Redimensiona a imagem original
        scaled_image = pygame.transform.smoothscale(self.image, (width, height))
        
        # Aplica efeito de desfoque sutil para quando não está em foco
        if blur_factor > 0 and not self.is_focused:
            # Simulação simples de desfoque usando redimensionamento para baixo e depois para cima
            blur_size = (width // 1.5, height // 1.5)
            blurred = pygame.transform.smoothscale(scaled_image, blur_size)
            scaled_image = pygame.transform.smoothscale(blurred, (width, height))
        
        # Aplica a cor e a opacidade à imagem
        color_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        color_surface.fill((*color, int(alpha * 0.3)))  # Cor leve apenas como tingimento
        
        # Combina imagem e cor
        self.surface.blit(scaled_image, (0, 0))
        self.surface.blit(color_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
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
                
        # Atualiza a transição de foco
        if self.focus_transition < 1.0:
            self.focus_transition += 0.08  # Velocidade da transição
            if self.focus_transition >= 1.0:
                self.focus_transition = 1.0
                
        # Sempre atualiza a superfície para a animação
        self.update_surface()
        
    def draw(self, screen):
        """Desenha Violet na tela"""
        if not self.surface:
            return
            
        # Calcula a posição central
        center_x = self.x + (self.BASE_WIDTH // 2)
        center_y = self.y + (self.BASE_HEIGHT // 2)
        
        # Ajusta para que a imagem fique centralizada mesmo com tamanhos diferentes
        offset_x = center_x - (self.surface.get_width() // 2)
        offset_y = center_y - (self.surface.get_height() // 2)
        
        # Desenha Violet na tela
        screen.blit(self.surface, (offset_x, offset_y))