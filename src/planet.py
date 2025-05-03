import pygame
import os

class Planet:
    def __init__(self, name, gravity_factor, background_color, obstacle_count, quiz_questions):
        self.name = name
        self.gravity_factor = gravity_factor  # Percentage of Earth gravity
        self.background_color = background_color
        self.obstacle_count = obstacle_count  # Number of obstacles based on planet size
        self.quiz_questions = quiz_questions  # List of dict with 'question', 'options', and 'answer'
        self.completed = False
        self.background_image = None  # Will store the background image if available

        # Calculate actual gravity value (Earth gravity * factor)
        self.gravity = 0.25 * (self.gravity_factor / 100.0) 

        # Create planet-specific assets
        self.create_assets()

    def create_assets(self):
        """Create planet-specific visual assets"""
        # Base surface size for ground texture
        self.ground_texture = pygame.Surface((800, 100))

        # Different ground styling based on planet
        if self.name == "Earth":
            # Load background image for Earth
            bg_path = os.path.join("assets", "images", "ceu_terra.png")
            try:
                self.background_image = pygame.image.load(bg_path).convert_alpha()
            except pygame.error:
                print("Failed to load Earth background image, using fallback")
                self.background_image = None
                
            # Load ground texture image for Earth and tile it to avoid stretching
            img_path = os.path.join("assets", "images", "earth_ground.png")
            try:
                tile_img = pygame.image.load(img_path).convert_alpha()
                tile_w, tile_h = tile_img.get_size()
                # Create a new surface for the ground texture with proper height
                self.ground_texture = pygame.Surface((800, tile_h), pygame.SRCALPHA)
                # Tile the image horizontally
                for x in range(0, 800, tile_w):
                    self.ground_texture.blit(tile_img, (x, 0))
            except pygame.error:
                # Fallback to default solid green if image load fails
                self.ground_texture = pygame.Surface((800, 100))
                self.ground_texture.fill((34, 139, 34))  # Forest green
                # Add grass details
                for i in range(0, 800, 20):
                    pygame.draw.rect(self.ground_texture, (0, 100, 0), (i, 0, 10, 20))

        elif self.name == "Moon":
            self.ground_texture.fill((169, 169, 169))  # Dark grey
            # Add some crater details
            for i in range(0, 800, 50):
                pygame.draw.circle(self.ground_texture, (120, 120, 120), (i, 20), 10)

        elif self.name == "Mercury":
            self.ground_texture.fill((160, 82, 45))  # Sienna brown
            # Add some crater details
            for i in range(0, 800, 40):
                pygame.draw.circle(self.ground_texture, (139, 69, 19), (i, 20), 8)

        elif self.name == "Venus":
            self.ground_texture.fill((218, 165, 32))  # Golden rod
            # Add some rock details
            for i in range(0, 800, 30):
                pygame.draw.rect(self.ground_texture, (184, 134, 11), (i, 0, 15, 15))

        elif self.name == "Mars":
            self.ground_texture.fill((205, 92, 92))  # Indian red
            # Add some rock details
            for i in range(0, 800, 35):
                pygame.draw.rect(self.ground_texture, (178, 34, 34), (i, 0, 12, 12))

        elif self.name == "Jupiter":
            # Jupiter doesn't have a solid surface, so create a gas-like pattern
            self.ground_texture.fill((244, 164, 96))  # Sandy brown
            for i in range(0, 800, 25):
                pygame.draw.rect(self.ground_texture, (210, 105, 30), (i, 10, 15, 80))

        elif self.name == "Saturn":
            # Saturn doesn't have a solid surface, so create a gas-like pattern
            self.ground_texture.fill((245, 222, 179))  # Wheat color
            for i in range(0, 800, 20):
                pygame.draw.rect(self.ground_texture, (222, 184, 135), (i, 5, 10, 90))

        elif self.name == "Uranus":
            # Uranus doesn't have a solid surface, so create a gas-like pattern
            self.ground_texture.fill((175, 238, 238))  # Pale turquoise
            for i in range(0, 800, 30):
                pygame.draw.rect(self.ground_texture, (127, 255, 212), (i, 0, 20, 100))

        elif self.name == "Neptune":
            # Neptune doesn't have a solid surface, so create a gas-like pattern
            self.ground_texture.fill((65, 105, 225))  # Royal blue
            for i in range(0, 800, 22):
                pygame.draw.rect(self.ground_texture, (0, 0, 205), (i, 0, 11, 100))

        elif self.name == "Pluto":
            # Pluto's icy surface
            self.ground_texture.fill((220, 220, 230))  # Very light blue-gray
            # Add some ice craters details
            for i in range(0, 800, 60):
                pygame.draw.circle(self.ground_texture, (200, 200, 210), (i, 25), 12)
                pygame.draw.circle(self.ground_texture, (190, 190, 200), (i+30, 15), 8)

    def get_info_text(self):
        """Return information about the planet for the transition screen"""
        info_texts = {
            "Earth": "Planeta natal com 100% de gravidade (g = 1,0). Nosso planeta azul é o único corpo celeste conhecido a abrigar vida.",
            "Mercury": "Planeta mais próximo do Sol com 40% de gravidade (g = 0,4). Mercúrio praticamente não tem atmosfera.",
            "Venus": "Segundo planeta a partir do Sol com 90% de gravidade (g = 0,9). Vênus tem uma atmosfera espessa e tóxica cheia de dióxido de carbono.",
            "Moon": "Satélite da Terra com 16% de gravidade (g = 0,16). A Lua tem cerca de 1/4 do diâmetro da Terra.",
            "Mars": "O Planeta Vermelho com 40% de gravidade (g = 0,4). Marte tem as maiores tempestades de poeira do sistema solar.",
            "Jupiter": "Maior planeta com 240% de gravidade (g = 2,4). Júpiter é um gigante gasoso e tem a Grande Mancha Vermelha, uma tempestade que dura há centenas de anos.",
            "Saturn": "Conhecido por seus anéis com 110% de gravidade (g = 1,1). Saturno é um gigante gasoso composto principalmente de hidrogênio e hélio.",
            "Uranus": "Gigante de gelo com 90% de gravidade (g = 0,9). Urano gira de lado com uma inclinação axial de cerca de 98 graus.",
            "Neptune": "Planeta mais distante com 110% de gravidade (g = 1,1). Netuno tem os ventos mais fortes do Sistema Solar, atingindo até 2.100 km/h.",
            "Pluto": "Planeta anão com 6% de gravidade (g = 0,06). Plutão faz parte do Cinturão de Kuiper, uma região de corpos gelados além de Netuno."
        }
        return info_texts.get(self.name, "Planeta desconhecido")

    def draw_ground(self, screen, x, screen_height):
        """Draw the ground for this planet"""
        # Calculate the position to draw the ground
        ground_y = screen_height - 100

        # Get the screen width to determine how many copies we need
        screen_width = screen.get_width()

        # Calculate how many copies of the ground texture we need to cover the screen
        # Add 2 extra copies to ensure smooth scrolling at the edges
        num_copies = (screen_width // 800) + 3

        # Draw multiple copies of the ground texture to fill the screen width
        for i in range(-1, num_copies):
            screen.blit(self.ground_texture, ((x % 800) + (i * 800), ground_y))
