import pygame
import random
import math
import os
import sys

# Add the assets directory to the Python path
assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
if assets_dir not in sys.path:
    sys.path.insert(0, assets_dir)

# Import custom expression drawing functions
try:
    from images.nova_expressions import EXPRESSION_FUNCTIONS
    USE_CUSTOM_EXPRESSIONS = True
except ImportError:
    USE_CUSTOM_EXPRESSIONS = False
    print("Could not import custom expressions, falling back to emojis")

class NovaAI:
    WIDTH = 80
    HEIGHT = 80

    # Colors for different expression types
    COLORS = {
        "normal": (70, 130, 180),  # Steel blue
        "excited": (65, 105, 225),  # Royal blue
        "curious": (106, 90, 205),  # Slate blue
        "surprised": (138, 43, 226),  # Blue violet
        "warning": (255, 140, 0),   # Dark orange
        "happy": (50, 205, 50),     # Lime green
        "alert": (220, 20, 60)      # Crimson
    }

    # Expressões que a IA pode mostrar (serão substituídas por gráficos)
    EXPRESSIONS = {
        "normal": "😊",
        "excited": "😃",
        "curious": "🤔",
        "surprised": "😲",
        "warning": "⚠️",
        "happy": "😄",
        "alert": "🚨"
    }
    
    # Fatos científicos sobre planetas
    FACTS = {
        "Earth": [
            "A atmosfera da Terra nos protege da radiação solar.",
            "71% da Terra é coberta por água.",
            "O campo magnético da Terra nos protege dos ventos solares.",
            "A Terra é o único planeta não nomeado em homenagem a um deus.",
            "A rotação da Terra está gradualmente ficando mais lenta."
        ],
        "Moon": [
            "A Lua está se afastando lentamente da Terra a 3,8 cm por ano.",
            "A Lua não tem atmosfera ou clima.",
            "Um dia na Lua dura cerca de 29,5 dias terrestres.",
            "A gravidade da Lua é 1/6 da gravidade da Terra.",
            "A superfície da Lua é coberta por regolito, um pó fino."
        ],
        "Mercury": [
            "Mercúrio não tem atmosfera e tem variações extremas de temperatura.",
            "Mercúrio é o menor planeta do nosso sistema solar.",
            "Um dia em Mercúrio tem 59 dias terrestres.",
            "Mercúrio tem alto teor de ferro e um grande núcleo.",
            "Mercúrio não tem luas próprias."
        ],
        "Venus": [
            "Vênus gira no sentido contrário em comparação com outros planetas.",
            "Vênus tem o dia mais longo de qualquer planeta, com 243 dias terrestres.",
            "Vênus é o planeta mais quente devido à sua atmosfera espessa.",
            "Vênus não tem luas nem campo magnético.",
            "A atmosfera de Vênus é 96% dióxido de carbono."
        ],
        "Mars": [
            "Marte tem o maior vulcão do sistema solar: Olympus Mons.",
            "Marte tem duas pequenas luas: Phobos e Deimos.",
            "Marte tem estações semelhantes à Terra, mas duas vezes mais longas.",
            "Marte tem calotas polares feitas de gelo de água e dióxido de carbono.",
            "A cor vermelha de Marte vem do óxido de ferro (ferrugem) em sua superfície."
        ],
        "Jupiter": [
            "Júpiter tem o campo magnético mais forte de qualquer planeta.",
            "Júpiter tem pelo menos 79 luas, incluindo as quatro grandes luas galileanas.",
            "A Grande Mancha Vermelha de Júpiter é uma tempestade que dura há séculos.",
            "Júpiter é um gigante gasoso sem superfície sólida.",
            "Júpiter tem anéis tênues, quase invisíveis."
        ],
        "Saturn": [
            "Os anéis de Saturno são feitos principalmente de partículas de gelo e detritos rochosos.",
            "Saturno tem a menor densidade de todos os planetas e flutuaria na água.",
            "Saturno tem pelo menos 82 luas.",
            "A lua de Saturno, Titã, tem uma atmosfera espessa.",
            "Os anéis de Saturno têm até 175.000 milhas de largura, mas são apenas 10 metros de espessura."
        ],
        "Uranus": [
            "Urano gira de lado, com seu eixo inclinado em 98 graus.",
            "Urano tem 27 luas conhecidas, nomeadas após personagens literários.",
            "Urano aparece azul-esverdeado devido ao metano em sua atmosfera.",
            "Urano é um gigante de gelo composto principalmente de gelos de água, metano e amônia.",
            "Urano tem 13 anéis estreitos."
        ],
        "Neptune": [
            "Netuno tem os ventos mais fortes do sistema solar, atingindo 2.100 km/h.",
            "Netuno tem 14 luas conhecidas, incluindo Tritão que orbita para trás.",
            "A cor azul de Netuno vem do metano em sua atmosfera.",
            "Netuno tem uma Grande Mancha Escura, semelhante à Grande Mancha Vermelha de Júpiter.",
            "A distância de Netuno ao Sol muda devido à sua órbita elíptica."
        ],
        "Pluto": [
            "Plutão foi reclassificado de planeta para planeta anão em 2006.",
            "Plutão tem cinco luas conhecidas, sendo Caronte a maior.",
            "A região em forma de coração em Plutão é chamada Região Tombaugh.",
            "A atmosfera de Plutão expande e contrai à medida que se aproxima e se afasta do Sol.",
            "Plutão leva 248 anos terrestres para orbitar o Sol uma vez."
        ]
    }
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = screen_width - self.WIDTH - 10
        self.y = 10
        self.expression = "normal"
        self.previous_expression = "normal"
        self.transition_progress = 1.0  # 1.0 means no transition
        self.message = ""
        self.displayed_message = ""  # For typewriter effect
        self.message_timer = 0
        self.message_duration = 180  # Quadros (3 segundos a 60fps)
        self.char_timer = 0
        self.char_delay = 2  # Frames between character additions

        # Animation variables
        self.pulse_factor = 1.0
        self.pulse_direction = 1
        self.pulse_speed = 0.005
        self.pulse_min = 0.95
        self.pulse_max = 1.05

        # Particle system
        self.particles = []
        self.particle_timer = 0
        self.particle_spawn_delay = 5  # Frames between particle spawns

        # Tails for speech bubble animation
        self.tail_offset = 0
        self.tail_direction = 1
        self.tail_speed = 0.5

        # Cria a superfície do assistente AI
        self.update_surface()
    
    def update_surface(self):
        """Atualiza a superfície do assistente AI com a expressão atual"""
        scaled_width = int(self.WIDTH * self.pulse_factor)
        scaled_height = int(self.HEIGHT * self.pulse_factor)

        self.surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))  # Transparente

        # Determine the color based on expression or transition
        if self.transition_progress < 1.0:
            # During transition, blend colors
            curr_color = self.COLORS[self.expression]
            prev_color = self.COLORS[self.previous_expression]
            blend_color = [
                int(prev_color[0] * (1-self.transition_progress) + curr_color[0] * self.transition_progress),
                int(prev_color[1] * (1-self.transition_progress) + curr_color[1] * self.transition_progress),
                int(prev_color[2] * (1-self.transition_progress) + curr_color[2] * self.transition_progress)
            ]
            color = (blend_color[0], blend_color[1], blend_color[2], 230)
        else:
            # No transition, use current expression color
            color = (*self.COLORS[self.expression], 230)

        # Draw the outer and inner circles
        pygame.draw.circle(self.surface, (50, 50, 50, 200),
                          (scaled_width // 2, scaled_height // 2), scaled_width // 2)
        pygame.draw.circle(self.surface, color,
                          (scaled_width // 2, scaled_height // 2), scaled_width // 2 - 3)

        # Use custom expressions or fall back to emojis
        if globals().get('USE_CUSTOM_EXPRESSIONS', False):
            # Get the appropriate drawing function for the current expression
            draw_func = EXPRESSION_FUNCTIONS.get(self.expression)
            if draw_func:
                # Create a temporary surface for the expression and have the function draw on it
                expression_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
                expression_surface.fill((0, 0, 0, 0))  # Start with transparency

                # Call the drawing function
                draw_func(expression_surface, scaled_width, scaled_height)

                # Blit the expression onto the main surface
                self.surface.blit(expression_surface, (0, 0))
            else:
                # Fall back to emoji if drawing function not found
                self._draw_emoji_expression(scaled_width, scaled_height)
        else:
            # Fall back to emoji representation
            self._draw_emoji_expression(scaled_width, scaled_height)

    def _draw_emoji_expression(self, width, height):
        """Fallback method to draw emoji-based expressions"""
        font = pygame.font.Font(None, int(50 * self.pulse_factor))  # Scale font with pulse
        expression_text = font.render(self.EXPRESSIONS[self.expression], True, (255, 255, 255))
        expression_rect = expression_text.get_rect(center=(width // 2, height // 2))

        self.surface.blit(expression_text, expression_rect)
    
    def set_expression(self, expression):
        """Muda a expressão da IA com transição suave"""
        if expression in self.EXPRESSIONS and expression != self.expression:
            self.previous_expression = self.expression
            self.expression = expression
            self.transition_progress = 0.0  # Start transition
            self.update_surface()
    
    def show_message(self, message, expression="normal"):
        """Exibe uma mensagem da IA com efeito de digitação"""
        self.message = message
        self.displayed_message = ""  # Reset displayed message for typewriter effect
        self.set_expression(expression)
        self.message_timer = self.message_duration
        self.char_timer = 0

        # Reset particle system when showing important messages
        if expression in ["warning", "alert", "excited"]:
            self.particles = []  # Clear existing particles
            self.particle_timer = 0  # Reset timer to spawn particles immediately
    
    def alert_gravity_change(self, planet_name, gravity_factor):
        """Alerta o jogador sobre a mudança de gravidade em um novo planeta"""
        # Converte porcentagem para valor g (ex: 100% -> g = 1.0)
        g_value = gravity_factor / 100.0
        self.show_message(f"Gravidade em {planet_name}: {gravity_factor}% da Terra (g = {g_value})", "alert")
    
    def give_random_fact(self, planet_name):
        """Compartilha um fato científico aleatório sobre o planeta atual"""
        if planet_name in self.FACTS:
            fact = random.choice(self.FACTS[planet_name])
            self.show_message(fact, "curious")
    
    def react_to_discovery(self, collectible_type):
        """Reage ao jogador coletando um item"""
        if collectible_type == "data":
            self.show_message("Dados científicos coletados!", "excited")
        elif collectible_type == "fuel":
            self.show_message("Células de combustível adquiridas!", "happy")
        elif collectible_type == "weapon":
            self.show_message("Sistemas defensivos online!", "alert")
    
    def react_to_obstacle(self, obstacle_type):
        """Reage a um obstáculo se aproximando"""
        if obstacle_type == "asteroid":
            self.show_message("Campo de asteroides à frente!", "warning")
        elif obstacle_type == "debris":
            self.show_message("Detritos espaciais detectados!", "warning")
        elif obstacle_type == "storm":
            self.show_message("Tempestade solar se aproximando!", "warning")
    
    def update(self):
        """Atualiza o assistente AI"""
        # Update pulsing animation
        self.pulse_factor += self.pulse_direction * self.pulse_speed
        if self.pulse_factor >= self.pulse_max:
            self.pulse_factor = self.pulse_max
            self.pulse_direction = -1
        elif self.pulse_factor <= self.pulse_min:
            self.pulse_factor = self.pulse_min
            self.pulse_direction = 1

        # Update expression transition
        if self.transition_progress < 1.0:
            self.transition_progress += 0.05  # Transition speed
            if self.transition_progress >= 1.0:
                self.transition_progress = 1.0
            self.update_surface()

        # Animate speech bubble tail
        self.tail_offset += self.tail_direction * self.tail_speed
        if abs(self.tail_offset) > 3:
            self.tail_direction *= -1

        # Update typewriter effect for message
        if self.message and len(self.displayed_message) < len(self.message):
            self.char_timer += 1
            if self.char_timer >= self.char_delay:
                self.char_timer = 0
                self.displayed_message += self.message[len(self.displayed_message)]

        # Update particle system
        if len(self.message) > 0 and self.message_timer > 0 and self.expression in ["warning", "alert", "excited"]:
            self.particle_timer += 1
            if self.particle_timer >= self.particle_spawn_delay:
                self.particle_timer = 0
                # Add new particle
                center_x = self.x + self.WIDTH // 2
                center_y = self.y + self.HEIGHT // 2
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(0.5, 2.0)
                size = random.uniform(2, 5)

                color = self.COLORS[self.expression]
                # Add alpha channel
                color_with_alpha = (*color, 200)

                self.particles.append({
                    'x': center_x,
                    'y': center_y,
                    'dx': math.cos(angle) * speed,
                    'dy': math.sin(angle) * speed,
                    'size': size,
                    'color': color_with_alpha,
                    'life': 30  # Frames until particle disappears
                })

        # Update existing particles
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

        # Atualiza temporizador da mensagem
        if self.message_timer > 0:
            self.message_timer -= 1

            # Reinicia para expressão normal quando a mensagem expira
            if self.message_timer == 0:
                self.message = ""
                self.displayed_message = ""
                self.set_expression("normal")

        # Always update surface for pulsing animation
        if self.message_timer > 0 or self.transition_progress < 1.0:
            self.update_surface()
    
    def draw(self, screen):
        """Desenha o assistente AI e quaisquer mensagens ativas"""
        # Draw particles behind the AI
        for particle in self.particles:
            # Calculate alpha based on remaining life
            alpha = int(255 * (particle['life'] / 30))
            color = (particle['color'][0], particle['color'][1], particle['color'][2], alpha)

            pygame.draw.circle(
                screen,
                color,
                (int(particle['x']), int(particle['y'])),
                int(particle['size'])
            )

        # Desenha o círculo da IA (centered on the original position)
        center_x = self.x + (self.WIDTH // 2)
        center_y = self.y + (self.HEIGHT // 2)
        offset_x = center_x - (self.surface.get_width() // 2)
        offset_y = center_y - (self.surface.get_height() // 2)
        screen.blit(self.surface, (offset_x, offset_y))

        # Desenha qualquer mensagem ativa
        if self.message and self.message_timer > 0:
            # Calculate bubble dimensions
            font = pygame.font.Font(None, 24)
            message_surf = font.render(self.displayed_message, True, (255, 255, 255))
            message_width = message_surf.get_width() + 20  # Padding
            message_height = message_surf.get_height() + 15  # Padding

            # Calculate position (centered on top part of screen)
            bubble_x = (self.screen_width - message_width) // 2
            bubble_y = 10

            # Draw speech bubble with rounded corners
            bubble_rect = pygame.Rect(bubble_x, bubble_y, message_width, message_height)

            # Determine bubble color based on expression type
            bubble_color = self.COLORS[self.expression]
            border_color = (50, 50, 50)

            # Draw bubble outline
            pygame.draw.rect(screen, border_color, bubble_rect, border_radius=10)
            # Draw bubble fill with transparency
            inner_rect = bubble_rect.inflate(-4, -4)
            pygame.draw.rect(screen, (*bubble_color, 180), inner_rect, border_radius=8)

            # Draw animated tail pointing to NOVA
            tail_height = 15
            tail_width = 20
            tail_top_x = self.screen_width // 2 + self.tail_offset

            # Points for the speech bubble tail (triangle)
            tail_points = [
                (tail_top_x - tail_width//2, bubble_y + message_height),  # Bottom left
                (tail_top_x + tail_width//2, bubble_y + message_height),  # Bottom right
                (self.x + self.WIDTH//2, self.y)                         # Point to AI
            ]

            # Draw tail
            pygame.draw.polygon(screen, border_color, tail_points)

            # Draw slightly smaller inner tail with the same color as the bubble
            inner_tail_points = [
                (tail_top_x - tail_width//2 + 2, bubble_y + message_height - 2),
                (tail_top_x + tail_width//2 - 2, bubble_y + message_height - 2),
                (self.x + self.WIDTH//2, self.y + 5)
            ]
            pygame.draw.polygon(screen, (*bubble_color, 180), inner_tail_points)

            # Position and draw the message text
            text_x = bubble_x + 10  # Left padding
            text_y = bubble_y + 8   # Top padding
            screen.blit(message_surf, (text_x, text_y))