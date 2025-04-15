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
            "Earth's atmosphere protects us from solar radiation.",
            "71% of Earth is covered by water.",
            "Earth's magnetic field protects us from solar winds.",
            "Earth is the only planet not named after a god.",
            "Earth's rotation is gradually slowing down."
        ],
        "Moon": [
            "The Moon is slowly moving away from Earth at 3.8 cm per year.",
            "The Moon has no atmosphere or weather.",
            "A day on the Moon lasts about 29.5 Earth days.",
            "The Moon's gravity is 1/6th of Earth's gravity.",
            "The Moon's surface is covered in regolith, a fine dust."
        ],
        "Mercury": [
            "Mercury has no atmosphere and extreme temperature variations.",
            "Mercury is the smallest planet in our solar system.",
            "A day on Mercury is 59 Earth days long.",
            "Mercury has a high iron content and a large core.",
            "Mercury has no moons of its own."
        ],
        "Venus": [
            "Venus rotates backwards compared to other planets.",
            "Venus has the longest day of any planet at 243 Earth days.",
            "Venus is the hottest planet due to its thick atmosphere.",
            "Venus has no moons and no magnetic field.",
            "Venus's atmosphere is 96% carbon dioxide."
        ],
        "Mars": [
            "Mars has the largest volcano in the solar system: Olympus Mons.",
            "Mars has two small moons: Phobos and Deimos.",
            "Mars has seasons similar to Earth, but twice as long.",
            "Mars has polar ice caps made of water and carbon dioxide ice.",
            "Mars's red color comes from iron oxide (rust) on its surface."
        ],
        "Jupiter": [
            "Jupiter has the strongest magnetic field of any planet.",
            "Jupiter has at least 79 moons, including the four large Galilean moons.",
            "Jupiter's Great Red Spot is a storm that has lasted for centuries.",
            "Jupiter is a gas giant with no solid surface.",
            "Jupiter has faint, barely visible rings."
        ],
        "Saturn": [
            "Saturn's rings are made mostly of ice particles and rock debris.",
            "Saturn has the lowest density of all planets and would float in water.",
            "Saturn has at least 82 moons.",
            "Saturn's moon Titan has a thick atmosphere.",
            "Saturn's rings span up to 175,000 miles wide, but are only about 10 meters thick."
        ],
        "Uranus": [
            "Uranus rotates on its side, with its axis tilted at 98 degrees.",
            "Uranus has 27 known moons, named after literary characters.",
            "Uranus appears blue-green due to methane in its atmosphere.",
            "Uranus is an ice giant composed mainly of water, methane, and ammonia ices.",
            "Uranus has 13 narrow rings."
        ],
        "Neptune": [
            "Neptune has the strongest winds in the solar system, reaching 2,100 km/h.",
            "Neptune has 14 known moons, including Triton which orbits backwards.",
            "Neptune's blue color comes from methane in its atmosphere.",
            "Neptune has a Great Dark Spot, similar to Jupiter's Great Red Spot.",
            "Neptune's distance from the Sun changes due to its elliptical orbit."
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
        self.show_message(f"Gravity on {planet_name}: {gravity_factor}% of Earth", "alert")
    
    def give_random_fact(self, planet_name):
        """Share a random scientific fact about the current planet"""
        if planet_name in self.FACTS:
            fact = random.choice(self.FACTS[planet_name])
            self.show_message(fact, "curious")
    
    def react_to_discovery(self, collectible_type):
        """React to the player collecting an item"""
        if collectible_type == "data":
            self.show_message("Scientific data collected!", "excited")
        elif collectible_type == "fuel":
            self.show_message("Fuel cells acquired!", "happy")
        elif collectible_type == "weapon":
            self.show_message("Defensive systems online!", "alert")
    
    def react_to_obstacle(self, obstacle_type):
        """React to an approaching obstacle"""
        if obstacle_type == "asteroid":
            self.show_message("Asteroid field ahead!", "warning")
        elif obstacle_type == "debris":
            self.show_message("Space debris detected!", "warning")
        elif obstacle_type == "storm":
            self.show_message("Solar storm approaching!", "warning")
    
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
            message_rect = message_surf.get_rect(midtop=(self.x + self.WIDTH // 2, self.y + self.HEIGHT + 5))
            
            # Draw a backdrop for the message
            backdrop_rect = message_rect.inflate(20, 10)
            pygame.draw.rect(screen, (0, 0, 0, 180), backdrop_rect, border_radius=5)
            
            # Draw the message text
            screen.blit(message_surf, message_rect)