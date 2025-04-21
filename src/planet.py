import pygame

class Planet:
    def __init__(self, name, gravity_factor, background_color, obstacle_count, quiz_questions):
        self.name = name
        self.gravity_factor = gravity_factor  # Percentage of Earth gravity
        self.background_color = background_color
        self.obstacle_count = obstacle_count  # Number of obstacles based on planet size
        self.quiz_questions = quiz_questions  # List of dict with 'question', 'options', and 'answer'
        self.completed = False
        
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
            self.ground_texture.fill((34, 139, 34))  # Forest green
            # Add some grass details
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
            "Earth": "Home planet with 100% gravity (g = 1.0). Our blue planet is the only known celestial body to harbor life.",
            "Mercury": "Closest planet to the Sun with 40% gravity (g = 0.4). Mercury has virtually no atmosphere.",
            "Venus": "Second planet from the Sun with 90% gravity (g = 0.9). Venus has a thick, toxic atmosphere filled with carbon dioxide.",
            "Moon": "Earth's satellite with 16% gravity (g = 0.16). The Moon is about 1/4 the diameter of Earth.",
            "Mars": "The Red Planet with 40% gravity (g = 0.4). Mars has the largest dust storms in the solar system.",
            "Jupiter": "Largest planet with 240% gravity (g = 2.4). Jupiter is a gas giant and has the Great Red Spot, a storm that has lasted hundreds of years.",
            "Saturn": "Known for its rings with 110% gravity (g = 1.1). Saturn is a gas giant composed mostly of hydrogen and helium.",
            "Uranus": "Ice giant with 90% gravity (g = 0.9). Uranus rotates on its side with an axial tilt of about 98 degrees.",
            "Neptune": "Furthest planet with 110% gravity (g = 1.1). Neptune has the strongest winds in the Solar System, reaching up to 2,100 km/h.",
            "Pluto": "Dwarf planet with 6% gravity (g = 0.06). Pluto is part of the Kuiper Belt, a region of icy bodies beyond Neptune."
        }
        return info_texts.get(self.name, "Unknown planet")
    
    def draw_ground(self, screen, x, screen_height):
        """Draw the ground for this planet"""
        # Calculate the position to draw the ground
        ground_y = screen_height - 100
        
        # Draw multiple copies of the ground texture to fill the screen width
        screen.blit(self.ground_texture, (x % 800, ground_y))
        screen.blit(self.ground_texture, ((x % 800) - 800, ground_y))
        screen.blit(self.ground_texture, ((x % 800) + 800, ground_y))