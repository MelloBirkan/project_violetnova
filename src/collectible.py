import pygame
import random

class Collectible:
    WIDTH = 30
    HEIGHT = 30
    
    # Types of collectibles
    TYPES = {
        "data": {
            "color": (0, 191, 255),  # Deep sky blue
            "value": 1,  # Points value
            "effect": "info"  # Shows planet info
        },
        "fuel": {
            "color": (255, 215, 0),  # Gold
            "value": 3,  # Points value
            "effect": "time"  # Extends gameplay time
        },
        "weapon": {
            "color": (220, 20, 60),  # Crimson
            "value": 5,  # Points value
            "effect": "attack"  # Allows destroying obstacles
        }
    }
    
    def __init__(self, x, y, collectible_type=None):
        self.x = x
        self.y = y
        self.collected = False
        self.animation_counter = 0
        self.bob_offset = 0  # For floating animation
        
        # Randomly select collectible type if not specified
        if collectible_type is None or collectible_type not in self.TYPES:
            collectible_type = random.choice(["data", "fuel"])  # Weapons are rarer, so exclude from random
        self.type = collectible_type
        self.properties = self.TYPES[self.type]
        
        # Create collectible surface
        self.create_collectible_surface()
    
    def create_collectible_surface(self):
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))  # Transparent background
        
        color = self.properties["color"]
        
        # Different shapes based on collectible type
        if self.type == "data":
            # Data module (hexagon with inner details)
            pygame.draw.polygon(self.surface, color, [
                (self.WIDTH//2, 0),                    # Top
                (self.WIDTH, self.HEIGHT//4),         # Top right
                (self.WIDTH, self.HEIGHT*3//4),       # Bottom right
                (self.WIDTH//2, self.HEIGHT),         # Bottom
                (0, self.HEIGHT*3//4),               # Bottom left
                (0, self.HEIGHT//4)                  # Top left
            ])
            # Inner details
            pygame.draw.circle(self.surface, (255, 255, 255), 
                             (self.WIDTH//2, self.HEIGHT//2), self.WIDTH//4)
            pygame.draw.lines(self.surface, (0, 0, 0), False, [
                (self.WIDTH//4, self.HEIGHT//2),
                (self.WIDTH*3//4, self.HEIGHT//2)
            ], 2)
            pygame.draw.lines(self.surface, (0, 0, 0), False, [
                (self.WIDTH//2, self.HEIGHT//4),
                (self.WIDTH//2, self.HEIGHT*3//4)
            ], 2)
            
        elif self.type == "fuel":
            # Fuel container (cylinder)
            pygame.draw.rect(self.surface, color, 
                           (self.WIDTH//4, self.HEIGHT//6, self.WIDTH//2, self.HEIGHT*2//3))
            pygame.draw.ellipse(self.surface, color,
                              (self.WIDTH//4, self.HEIGHT//6 - self.HEIGHT//12, 
                               self.WIDTH//2, self.HEIGHT//6))
            pygame.draw.ellipse(self.surface, color,
                              (self.WIDTH//4, self.HEIGHT*5//6 - self.HEIGHT//12, 
                               self.WIDTH//2, self.HEIGHT//6))
            # Fuel level indicator
            pygame.draw.rect(self.surface, (255, 0, 0),
                           (self.WIDTH*3//8, self.HEIGHT//3, self.WIDTH//4, self.HEIGHT//3))
            
        elif self.type == "weapon":
            # Weapon (star shape)
            points = []
            for i in range(10):
                angle = 2 * 3.14159 * i / 10
                radius = self.WIDTH//2 if i % 2 == 0 else self.WIDTH//4
                points.append((
                    self.WIDTH//2 + int(radius * 0.9 * (0 if i % 2 != 0 else 1) * 0.8 * (0.5 if i == 0 else 1) * (0.5 if i == 4 else 1) * (0.6 if i == 6 else 1) * (0.7 if i == 8 else 1) * (0.8 if i == 2 else 1) * (-1 if i > 5 else 1)),
                    self.HEIGHT//2 + int(radius * 0.9 * (0 if i % 2 != 0 else 1) * 0.8 * (0.5 if i == 2 else 1) * (0.5 if i == 6 else 1) * (0.6 if i == 0 else 1) * (0.7 if i == 8 else 1) * (0.8 if i == 4 else 1) * (-1 if i > 7 or i < 3 else 1))
                ))
            pygame.draw.polygon(self.surface, color, points)
            # Inner circle
            pygame.draw.circle(self.surface, (255, 255, 255),
                             (self.WIDTH//2, self.HEIGHT//2), self.WIDTH//6)
    
    def update(self):
        # Floating animation
        self.animation_counter += 0.1
        self.bob_offset = int(3 * (0.5 - 0.5 * (self.animation_counter % 1)))
        
    def draw(self, screen):
        if not self.collected:
            # Apply bob offset for floating effect
            screen.blit(self.surface, (self.x, self.y + self.bob_offset))
    
    def check_collision(self, spacecraft):
        """Check if the spacecraft has collected this item"""
        if self.collected:
            return False
            
        # Simple rectangle collision
        spacecraft_rect = pygame.Rect(spacecraft.x, spacecraft.y, spacecraft.WIDTH, spacecraft.HEIGHT)
        collectible_rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        
        if spacecraft_rect.colliderect(collectible_rect):
            self.collected = True
            return True
        
        return False
    
    def get_effect(self):
        """Return the effect of this collectible"""
        return {
            "type": self.type,
            "effect": self.properties["effect"],
            "value": self.properties["value"]
        }