import pygame
import random

class NovaAI:
    WIDTH = 80
    HEIGHT = 80
    
    # Expressions the AI can show
    EXPRESSIONS = {
        "normal": "😊",
        "excited": "😃",
        "curious": "🤔",
        "surprised": "😲",
        "warning": "⚠️",
        "happy": "😄",
        "alert": "🚨"
    }
    
    # Scientific facts about planets
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
        self.message = ""
        self.message_timer = 0
        self.message_duration = 180  # Frames (3 seconds at 60fps)
        
        # Create the AI assistant surface
        self.update_surface()
    
    def update_surface(self):
        """Update the AI assistant surface with current expression"""
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))  # Transparent
        
        # Draw circular background
        pygame.draw.circle(self.surface, (50, 50, 50, 200), 
                          (self.WIDTH // 2, self.HEIGHT // 2), self.WIDTH // 2)
        pygame.draw.circle(self.surface, (70, 130, 180, 230), 
                          (self.WIDTH // 2, self.HEIGHT // 2), self.WIDTH // 2 - 3)
        
        # We'll use a font to display the emoji expression
        # This is a simplified approach - for a real game, you'd want to use proper emoji support
        font = pygame.font.Font(None, 50)  # Large font for the expression
        expression_text = font.render(self.EXPRESSIONS[self.expression], True, (255, 255, 255))
        expression_rect = expression_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        
        self.surface.blit(expression_text, expression_rect)
    
    def set_expression(self, expression):
        """Change the AI's expression"""
        if expression in self.EXPRESSIONS:
            self.expression = expression
            self.update_surface()
    
    def show_message(self, message, expression="normal"):
        """Display a message from the AI"""
        self.message = message
        self.set_expression(expression)
        self.message_timer = self.message_duration
    
    def alert_gravity_change(self, planet_name, gravity_factor):
        """Alert the player about the gravity change on a new planet"""
        # Convert percentage to g-value (e.g., 100% -> g = 1.0)
        g_value = gravity_factor / 100.0
        self.show_message(f"Gravidade em {planet_name}: {gravity_factor}% da Terra (g = {g_value})", "alert")
    
    def give_random_fact(self, planet_name):
        """Share a random scientific fact about the current planet"""
        if planet_name in self.FACTS:
            fact = random.choice(self.FACTS[planet_name])
            self.show_message(fact, "curious")
    
    def react_to_discovery(self, collectible_type):
        """React to the player collecting an item"""
        if collectible_type == "data":
            self.show_message("Dados científicos coletados!", "excited")
        elif collectible_type == "fuel":
            self.show_message("Células de combustível adquiridas!", "happy")
        elif collectible_type == "weapon":
            self.show_message("Sistemas defensivos online!", "alert")
    
    def react_to_obstacle(self, obstacle_type):
        """React to an approaching obstacle"""
        if obstacle_type == "asteroid":
            self.show_message("Campo de asteroides à frente!", "warning")
        elif obstacle_type == "debris":
            self.show_message("Detritos espaciais detectados!", "warning")
        elif obstacle_type == "storm":
            self.show_message("Tempestade solar se aproximando!", "warning")
    
    def update(self):
        """Update the AI assistant"""
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
            
            # Reset to normal expression when message expires
            if self.message_timer == 0:
                self.message = ""
                self.set_expression("normal")
    
    def draw(self, screen):
        """Draw the AI assistant and any active messages"""
        # Draw the AI circle
        screen.blit(self.surface, (self.x, self.y))
        
        # Draw any active message
        if self.message and self.message_timer > 0:
            # Prepare the message text surface
            font = pygame.font.Font(None, 24)
            message_surf = font.render(self.message, True, (255, 255, 255))
            
            # Position message at the top-center of the screen
            message_rect = message_surf.get_rect(midtop=(self.screen_width // 2, 10))
            
            # Draw a backdrop for the message
            backdrop_rect = message_rect.inflate(20, 10)
            pygame.draw.rect(screen, (0, 0, 0, 180), backdrop_rect, border_radius=5)
            
            # Draw the message text
            screen.blit(message_surf, message_rect)