import pygame

class Bird:
    WIDTH = 40
    HEIGHT = 30
    
    # Bird color options
    COLORS = {
        "yellow": {
            "body": (255, 255, 0),      # Yellow
            "beak": (255, 165, 0),      # Orange
            "eye": (0, 0, 0)            # Black
        },
        "red": {
            "body": (255, 0, 0),        # Red
            "beak": (255, 165, 0),      # Orange
            "eye": (0, 0, 0)            # Black
        },
        "blue": {
            "body": (0, 191, 255),      # Deep Sky Blue
            "beak": (255, 140, 0),      # Dark Orange
            "eye": (0, 0, 0)            # Black
        },
        "green": {
            "body": (50, 205, 50),      # Lime Green
            "beak": (255, 165, 0),      # Orange
            "eye": (0, 0, 0)            # Black
        }
    }
    
    def __init__(self, x, y, color="yellow"):
        self.x = x
        self.y = y
        self.velocity = 0
        self.angle = 0
        self.color = color if color in self.COLORS else "yellow"
        
        # Animation variables
        self.animation_frames = 2  # Number of frames in animation
        self.current_frame = 0
        self.animation_speed = 0.1  # How fast to animate
        self.animation_counter = 0
        
        # Create bird images for animation
        self.images = []
        self.create_animation_frames()
    
    def update(self, gravity):
        # Apply gravity and update position
        self.velocity += gravity
        self.y += self.velocity
        
        # Update bird angle based on velocity
        self.angle = min(max(-30, -self.velocity * 3), 60)
        
        # Update animation
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % self.animation_frames
    
    def flap(self):
        # Give the bird upward velocity
        self.velocity = -7
    
    def create_animation_frames(self):
        """Create all frames for bird animation"""
        self.images = []
        
        # Get color values
        color_values = self.COLORS[self.color]
        
        # Create first frame (wings up)
        frame1 = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        frame1.fill((0, 0, 0, 0))  # Transparent
        
        # Draw bird shape - wings up position
        pygame.draw.ellipse(frame1, color_values["body"], (0, 0, self.WIDTH, self.HEIGHT))  # Body
        pygame.draw.ellipse(frame1, color_values["beak"], (self.WIDTH - 15, 10, 15, 10))  # Beak
        pygame.draw.ellipse(frame1, color_values["eye"], (self.WIDTH - 30, 5, 5, 5))  # Eye
        # Wing up
        pygame.draw.ellipse(frame1, (200, 200, 200), (5, 5, 15, 8))  # Wing
        
        # Create second frame (wings down)
        frame2 = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        frame2.fill((0, 0, 0, 0))  # Transparent
        
        # Draw bird shape - wings down position
        pygame.draw.ellipse(frame2, color_values["body"], (0, 0, self.WIDTH, self.HEIGHT))  # Body
        pygame.draw.ellipse(frame2, color_values["beak"], (self.WIDTH - 15, 10, 15, 10))  # Beak
        pygame.draw.ellipse(frame2, color_values["eye"], (self.WIDTH - 30, 5, 5, 5))  # Eye
        # Wing down
        pygame.draw.ellipse(frame2, (200, 200, 200), (5, 15, 15, 8))  # Wing
        
        self.images.append(frame1)
        self.images.append(frame2)
    
    def update_image(self):
        """Update all animation frames with the current color"""
        self.create_animation_frames()
    
    def change_color(self, color):
        """Change bird color"""
        if color in self.COLORS:
            self.color = color
            self.update_image()
            
    def draw(self, screen):
        # Get the current animation frame
        current_image = self.images[self.current_frame]
        
        # Rotate the bird image based on the angle
        rotated_image = pygame.transform.rotate(current_image, -self.angle)
        
        # Get the rect of the rotated image and center it at the bird's position
        rect = rotated_image.get_rect(center=(self.x + self.WIDTH // 2, self.y + self.HEIGHT // 2))
        
        # Draw the rotated image
        screen.blit(rotated_image, rect.topleft)