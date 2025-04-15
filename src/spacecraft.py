import pygame

class Spacecraft:
    WIDTH = 50
    HEIGHT = 30
    
    # Spacecraft color options
    COLORS = {
        "silver": {
            "body": (192, 192, 192),  # Silver
            "window": (135, 206, 250),  # Light sky blue
            "engine": (255, 69, 0)      # Red-orange for engine glow
        },
        "gold": {
            "body": (255, 215, 0),     # Gold
            "window": (135, 206, 250),  # Light sky blue
            "engine": (255, 69, 0)      # Red-orange for engine glow
        },
        "blue": {
            "body": (70, 130, 180),    # Steel blue
            "window": (135, 206, 250),  # Light sky blue
            "engine": (255, 69, 0)      # Red-orange for engine glow
        },
        "red": {
            "body": (178, 34, 34),     # Firebrick red
            "window": (135, 206, 250),  # Light sky blue
            "engine": (255, 215, 0)     # Gold for engine glow
        }
    }
    
    def __init__(self, x, y, color="silver"):
        self.x = x
        self.y = y
        self.velocity = 0
        self.angle = 0
        self.color = color if color in self.COLORS else "silver"
        
        # Thrust control
        self.thrusting = False
        self.thrust_power = 0.5
        
        # Animation variables
        self.animation_frames = 2  # Number of frames in animation
        self.current_frame = 0
        self.animation_speed = 0.1  # How fast to animate
        self.animation_counter = 0
        
        # Create spacecraft images for animation
        self.images = []
        self.create_animation_frames()
    
    def update(self, gravity):
        # Apply gravity and update position
        self.velocity += gravity
        
        # Apply thrust if thrusting
        if self.thrusting:
            self.velocity -= self.thrust_power
            self.thrusting = False
        
        self.y += self.velocity
        
        # Update spacecraft angle based on velocity
        self.angle = min(max(-30, -self.velocity * 2), 60)
        
        # Update animation
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % self.animation_frames
    
    def thrust(self):
        # Apply thrust
        self.thrusting = True
    
    def create_animation_frames(self):
        """Create all frames for spacecraft animation"""
        self.images = []
        
        # Get color values
        color_values = self.COLORS[self.color]
        
        # Create first frame (normal thrust)
        frame1 = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        frame1.fill((0, 0, 0, 0))  # Transparent
        
        # Draw spacecraft shape
        # Main body (elongated ellipse)
        pygame.draw.ellipse(frame1, color_values["body"], (0, 5, self.WIDTH - 10, self.HEIGHT - 10))
        # Pointed nose
        pygame.draw.polygon(frame1, color_values["body"], [
            (self.WIDTH - 10, self.HEIGHT // 2),
            (self.WIDTH, self.HEIGHT // 2 - 5),
            (self.WIDTH, self.HEIGHT // 2 + 5)
        ])
        # Cockpit/window
        pygame.draw.ellipse(frame1, color_values["window"], (self.WIDTH - 30, self.HEIGHT // 2 - 5, 10, 10))
        # Engine exhaust (normal)
        pygame.draw.polygon(frame1, color_values["engine"], [
            (0, self.HEIGHT // 2 - 5),
            (-10, self.HEIGHT // 2),
            (0, self.HEIGHT // 2 + 5)
        ])
        
        # Create second frame (larger thrust)
        frame2 = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        frame2.fill((0, 0, 0, 0))  # Transparent
        
        # Draw spacecraft shape (same as frame1)
        pygame.draw.ellipse(frame2, color_values["body"], (0, 5, self.WIDTH - 10, self.HEIGHT - 10))
        pygame.draw.polygon(frame2, color_values["body"], [
            (self.WIDTH - 10, self.HEIGHT // 2),
            (self.WIDTH, self.HEIGHT // 2 - 5),
            (self.WIDTH, self.HEIGHT // 2 + 5)
        ])
        pygame.draw.ellipse(frame2, color_values["window"], (self.WIDTH - 30, self.HEIGHT // 2 - 5, 10, 10))
        # Engine exhaust (larger)
        pygame.draw.polygon(frame2, color_values["engine"], [
            (0, self.HEIGHT // 2 - 5),
            (-15, self.HEIGHT // 2),
            (0, self.HEIGHT // 2 + 5)
        ])
        
        self.images.append(frame1)
        self.images.append(frame2)
    
    def update_image(self):
        """Update all animation frames with the current color"""
        self.create_animation_frames()
    
    def change_color(self, color):
        """Change spacecraft color"""
        if color in self.COLORS:
            self.color = color
            self.update_image()
            
    def draw(self, screen):
        # Get the current animation frame
        current_image = self.images[self.current_frame]
        
        # Rotate the spacecraft image based on the angle
        rotated_image = pygame.transform.rotate(current_image, -self.angle)
        
        # Get the rect of the rotated image and center it at the spacecraft's position
        rect = rotated_image.get_rect(center=(self.x + self.WIDTH // 2, self.y + self.HEIGHT // 2))
        
        # Draw the rotated image
        screen.blit(rotated_image, rect.topleft)