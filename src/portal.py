import pygame
import math
import random

class Portal:
    WIDTH = 60
    HEIGHT = 100
    
    def __init__(self, x, y, target_planet):
        self.x = x
        self.y = y
        self.target_planet = target_planet
        self.active = True
        
        # Animation variables
        self.animation_counter = 0
        self.particles = []
        self.generate_particles()
        
        # Colors for different planet portals
        self.portal_colors = {
            "Moon": (200, 200, 200),       # Silver
            "Mercury": (255, 165, 0),     # Orange
            "Venus": (255, 215, 0),       # Gold
            "Earth": (0, 191, 255),       # Deep Sky Blue
            "Mars": (255, 69, 0),         # Red-Orange
            "Jupiter": (222, 184, 135),   # Sandy Brown
            "Saturn": (245, 222, 179),    # Wheat
            "Uranus": (64, 224, 208),     # Turquoise
            "Neptune": (65, 105, 225)     # Royal Blue
        }
        
        # Get color based on target planet
        self.color = self.portal_colors.get(target_planet, (128, 0, 128))  # Default purple
    
    def generate_particles(self):
        """Generate particles for the portal effect"""
        self.particles = []
        for _ in range(20):
            angle = random.random() * 2 * math.pi
            speed = 0.5 + random.random() * 1.5
            size = 2 + random.random() * 4
            lifetime = 30 + random.random() * 30
            self.particles.append({
                "x": self.x + self.WIDTH // 2,
                "y": self.y + self.HEIGHT // 2,
                "angle": angle,
                "speed": speed,
                "size": size,
                "lifetime": lifetime,
                "current_life": lifetime
            })
    
    def update(self):
        """Update portal animation"""
        self.animation_counter += 0.05
        
        # Update existing particles
        for particle in self.particles:
            particle["x"] += math.cos(particle["angle"]) * particle["speed"]
            particle["y"] += math.sin(particle["angle"]) * particle["speed"]
            particle["current_life"] -= 1
            
            # Reset dead particles
            if particle["current_life"] <= 0:
                particle["x"] = self.x + self.WIDTH // 2
                particle["y"] = self.y + self.HEIGHT // 2
                particle["angle"] = random.random() * 2 * math.pi
                particle["current_life"] = particle["lifetime"]
    
    def draw(self, screen):
        """Draw the portal"""
        if not self.active:
            return
            
        # Draw the main portal shape (oval with pulsing effect)
        pulse = math.sin(self.animation_counter) * 0.2 + 0.8  # 0.6 to 1.0 scale factor
        
        # Draw outer glow
        glow_color = (self.color[0], self.color[1], self.color[2], 100)  # Add alpha
        glow_surface = pygame.Surface((self.WIDTH + 20, self.HEIGHT + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface, glow_color, 
                          (0, 0, self.WIDTH + 20, self.HEIGHT + 20))
        
        # Apply pulse effect to glow position
        glow_x = self.x - 10 + (1 - pulse) * 5
        glow_y = self.y - 10 + (1 - pulse) * 5
        screen.blit(glow_surface, (glow_x, glow_y))
        
        # Draw main portal
        width = int(self.WIDTH * pulse)
        height = int(self.HEIGHT * pulse)
        x = self.x + (self.WIDTH - width) // 2
        y = self.y + (self.HEIGHT - height) // 2
        
        pygame.draw.ellipse(screen, self.color, (x, y, width, height))
        
        # Inner darker ellipse
        inner_width = width * 0.7
        inner_height = height * 0.7
        inner_x = self.x + (self.WIDTH - inner_width) // 2
        inner_y = self.y + (self.HEIGHT - inner_height) // 2
        
        # Darker version of the color
        darker_color = (max(0, self.color[0] - 60), 
                        max(0, self.color[1] - 60), 
                        max(0, self.color[2] - 60))
        pygame.draw.ellipse(screen, darker_color, 
                          (inner_x, inner_y, inner_width, inner_height))
        
        # Draw particles
        for particle in self.particles:
            # Calculate alpha based on remaining lifetime
            alpha = int(255 * (particle["current_life"] / particle["lifetime"]))
            particle_color = (self.color[0], self.color[1], self.color[2], alpha)
            particle_surface = pygame.Surface((int(particle["size"]), int(particle["size"])), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle_color, 
                             (int(particle["size"]) // 2, int(particle["size"]) // 2), 
                             int(particle["size"]) // 2)
            screen.blit(particle_surface, 
                       (int(particle["x"] - particle["size"] // 2), 
                        int(particle["y"] - particle["size"] // 2)))
    
    def check_collision(self, spacecraft):
        """Check if the spacecraft has entered the portal"""
        if not self.active:
            return False
            
        # Simple rectangle collision
        spacecraft_rect = pygame.Rect(spacecraft.x, spacecraft.y, spacecraft.WIDTH, spacecraft.HEIGHT)
        portal_rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        
        return spacecraft_rect.colliderect(portal_rect)