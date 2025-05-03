import pygame

class Bird:
    WIDTH = 40
    HEIGHT = 30
    
    # Opções de cor do pássaro
    COLORS = {
        "yellow": {
            "body": (255, 255, 0),      # Amarelo
            "beak": (255, 165, 0),      # Laranja
            "eye": (0, 0, 0)            # Preto
        },
        "red": {
            "body": (255, 0, 0),        # Vermelho
            "beak": (255, 165, 0),      # Laranja
            "eye": (0, 0, 0)            # Preto
        },
        "blue": {
            "body": (0, 191, 255),      # Azul Céu Profundo
            "beak": (255, 140, 0),      # Laranja Escuro
            "eye": (0, 0, 0)            # Preto
        },
        "green": {
            "body": (50, 205, 50),      # Verde Lima
            "beak": (255, 165, 0),      # Laranja
            "eye": (0, 0, 0)            # Preto
        }
    }
    
    def __init__(self, x, y, color="yellow"):
        self.x = x
        self.y = y
        self.velocity = 0
        self.angle = 0
        self.color = color if color in self.COLORS else "yellow"
        
        # Variáveis de animação
        self.animation_frames = 2  # Número de quadros na animação
        self.current_frame = 0
        self.animation_speed = 0.1  # Quão rápido animar
        self.animation_counter = 0
        
        # Cria imagens do pássaro para animação
        self.images = []
        self.create_animation_frames()
    
    def update(self, gravity):
        # Aplica gravidade e atualiza posição
        self.velocity += gravity
        self.y += self.velocity
        
        # Atualiza o ângulo do pássaro baseado na velocidade
        self.angle = min(max(-30, -self.velocity * 3), 60)
        
        # Atualiza animação
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % self.animation_frames
    
    def flap(self):
        # Dá ao pássaro velocidade para cima
        self.velocity = -7
    
    def create_animation_frames(self):
        """Cria todos os quadros para a animação do pássaro"""
        self.images = []
        
        # Obtém valores de cor
        color_values = self.COLORS[self.color]
        
        # Cria primeiro quadro (asas para cima)
        frame1 = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        frame1.fill((0, 0, 0, 0))  # Transparente
        
        # Desenha forma do pássaro - posição asas para cima
        pygame.draw.ellipse(frame1, color_values["body"], (0, 0, self.WIDTH, self.HEIGHT))  # Corpo
        pygame.draw.ellipse(frame1, color_values["beak"], (self.WIDTH - 15, 10, 15, 10))  # Bico
        pygame.draw.ellipse(frame1, color_values["eye"], (self.WIDTH - 30, 5, 5, 5))  # Olho
        # Asa para cima
        pygame.draw.ellipse(frame1, (200, 200, 200), (5, 5, 15, 8))  # Asa
        
        # Cria segundo quadro (asas para baixo)
        frame2 = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        frame2.fill((0, 0, 0, 0))  # Transparente
        
        # Desenha forma do pássaro - posição asas para baixo
        pygame.draw.ellipse(frame2, color_values["body"], (0, 0, self.WIDTH, self.HEIGHT))  # Corpo
        pygame.draw.ellipse(frame2, color_values["beak"], (self.WIDTH - 15, 10, 15, 10))  # Bico
        pygame.draw.ellipse(frame2, color_values["eye"], (self.WIDTH - 30, 5, 5, 5))  # Olho
        # Asa para baixo
        pygame.draw.ellipse(frame2, (200, 200, 200), (5, 15, 15, 8))  # Asa
        
        self.images.append(frame1)
        self.images.append(frame2)
    
    def update_image(self):
        """Atualiza todos os quadros de animação com a cor atual"""
        self.create_animation_frames()
    
    def change_color(self, color):
        """Muda a cor do pássaro"""
        if color in self.COLORS:
            self.color = color
            self.update_image()
            
    def draw(self, screen):
        # Obtém o quadro de animação atual
        current_image = self.images[self.current_frame]
        
        # Rotaciona a imagem do pássaro baseado no ângulo
        rotated_image = pygame.transform.rotate(current_image, -self.angle)
        
        # Obtém o rect da imagem rotacionada e centraliza na posição do pássaro
        rect = rotated_image.get_rect(center=(self.x + self.WIDTH // 2, self.y + self.HEIGHT // 2))
        
        # Desenha a imagem rotacionada
        screen.blit(rotated_image, rect.topleft)