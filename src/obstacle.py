import pygame
import random

class Obstacle:
    WIDTH = 80
    GAP = 150
    
    # Types of space obstacles
    TYPES = {
        "asteroid": {
            "color": (139, 69, 19),  # Saddle brown
            "detail_color": (101, 67, 33)
        },
        "debris": {
            "color": (112, 128, 144),  # Slate gray
            "detail_color": (47, 79, 79)  # Dark slate gray
        },
        "storm": {
            "color": (255, 165, 0),  # Orange
            "detail_color": (255, 215, 0)  # Gold
        }
    }
    
    def __init__(self, x, gap_y, speed, obstacle_type=None):
        self.x = x
        self.gap_y = gap_y
        self.speed = speed
        self.scored = False
        
        # Randomly select obstacle type if not specified
        if obstacle_type is None or obstacle_type not in self.TYPES:
            obstacle_type = random.choice(list(self.TYPES.keys()))
        self.type = obstacle_type
        self.colors = self.TYPES[self.type]
        
        # Create obstacle surfaces
        self.create_obstacle_surfaces()
    
    def create_obstacle_surfaces(self):
        # Create top and bottom obstacle surfaces
        self.top_obstacle = pygame.Surface((self.WIDTH, self.gap_y - self.GAP // 2))
        self.top_obstacle.fill(self.colors["color"])
        
        bottom_obstacle_height = 600 - self.gap_y - self.GAP // 2
        self.bottom_obstacle = pygame.Surface((self.WIDTH, bottom_obstacle_height))
        self.bottom_obstacle.fill(self.colors["color"])
        
        # Add obstacle details based on type
        if self.type == "asteroid":
            # Add crater-like details to asteroids
            self._add_asteroid_details(self.top_obstacle)
            self._add_asteroid_details(self.bottom_obstacle)
        
        elif self.type == "debris":
            # Add metallic/technological details to debris
            self._add_debris_details(self.top_obstacle)
            self._add_debris_details(self.bottom_obstacle)
        
        elif self.type == "storm":
            # Add swirling pattern to solar storms
            self._add_storm_details(self.top_obstacle)
            self._add_storm_details(self.bottom_obstacle)
    
    def _add_asteroid_details(self, surface):
        # Add crater-like circles to asteroid
        width, height = surface.get_size()
        for _ in range(width // 10):
            x = random.randint(5, width - 5)
            y = random.randint(5, height - 5)
            radius = random.randint(3, 8)
            pygame.draw.circle(surface, self.colors["detail_color"], (x, y), radius)
    
    def _add_debris_details(self, surface):
        # Add technological debris details (rectangles and lines)
        width, height = surface.get_size()
        for _ in range(width // 15):
            x = random.randint(5, width - 15)
            y = random.randint(5, height - 15)
            w = random.randint(5, 15)
            h = random.randint(5, 15)
            pygame.draw.rect(surface, self.colors["detail_color"], (x, y, w, h))
            
            # Add some lines to represent tech details
            line_x = random.randint(0, width - 1)
            pygame.draw.line(surface, (200, 200, 200), 
                             (line_x, 0), 
                             (line_x, random.randint(10, 30)))
    
    def _add_storm_details(self, surface):
        # Add swirling pattern to represent solar storms
        width, height = surface.get_size()
        
        # Create wave-like patterns
        for y in range(0, height, 10):
            amplitude = random.randint(5, 15)
            for x in range(0, width, 2):
                wave_y = y + int(amplitude * ((x / width) * 2 - 1) ** 2)
                if 0 <= wave_y < height and 0 <= x < width:
                    surface.set_at((x, wave_y), self.colors["detail_color"])
    
    def update(self):
        # Move obstacle left
        self.x -= self.speed
    
    def draw(self, screen):
        # Draw top obstacle
        screen.blit(self.top_obstacle, (self.x, 0))
        
        # Draw bottom obstacle
        bottom_obstacle_y = self.gap_y + self.GAP // 2
        screen.blit(self.bottom_obstacle, (self.x, bottom_obstacle_y))