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
        # Position and physics
        self.x = x
        self.y = y
        self.velocity = 0
        self.angle = 0
        # Color selection
        self.color = color if color in self.COLORS else "silver"
        # Flame colors override: if empty, use static engine color
        self.flame_colors = []
        # Thrust control
        self.thrusting = False
        self.thrust_power = 5.0
        self.thrust_multiplier = 1.0
        # Thrust visual timing and flame extent (ms & px)
        self.last_thrust_time = 0
        self.thrust_display_time = 400  # ms to display thrust flame
        # Flame extension width for more prominent engine flame
        self.flame_extent = 30
        # Flame animation variables
        self.animation_frames = 2
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_counter = 0
        # Create spacecraft base and thrust frames
        self.create_animation_frames()
    
    def update(self, gravity):
        # Apply gravity and update position
        self.velocity += gravity
        
        # Adapt thrust power based on planet gravity
        self.thrust_multiplier = max(1.0, gravity * 4)
        
        # Apply thrust impulse
        if self.thrusting:
            self.velocity -= self.thrust_power * self.thrust_multiplier
            self.thrusting = False
        
        self.y += self.velocity
        
        # Update spacecraft angle based on velocity
        self.angle = min(max(-30, -self.velocity * 2), 60)
        
        # Animate thrust flame frames (always cycling)
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % self.animation_frames
    
    def thrust(self):
        # Apply thrust
        self.thrusting = True
        # Immediate velocity for responsiveness
        self.velocity -= 0.5 * self.thrust_multiplier
        # Record time to show thrust flame
        self.last_thrust_time = pygame.time.get_ticks()
    
    def create_animation_frames(self):
        """Create all frames for spacecraft animation"""
        # Prepare base and thrust frames with horizontal flame extension
        color_values = self.COLORS[self.color]
        fe = self.flame_extent
        total_w = self.WIDTH + fe
        # Base image surface (spacecraft without flame)
        base = pygame.Surface((total_w, self.HEIGHT), pygame.SRCALPHA)
        base.fill((0, 0, 0, 0))
        # Draw spacecraft body offset by flame extent
        pygame.draw.ellipse(base, color_values["body"], (fe, 5, self.WIDTH - 10, self.HEIGHT - 10))
        pygame.draw.polygon(base, color_values["body"], [
            (fe + self.WIDTH - 10, self.HEIGHT // 2),
            (fe + self.WIDTH,      self.HEIGHT // 2 - 5),
            (fe + self.WIDTH,      self.HEIGHT // 2 + 5)
        ])
        pygame.draw.ellipse(base, color_values["window"], (fe + self.WIDTH - 30, self.HEIGHT // 2 - 5, 10, 10))
        # Determine engine colors: use flame_colors for gradient, else default engine color
        engine_colors = self.flame_colors if self.flame_colors else [color_values["engine"]]
        # Build thrust frames for each engine color
        thrust_images = []
        for ec in engine_colors:
            # Small thrust flame frame
            small = base.copy()
            pygame.draw.polygon(small, ec, [
                (fe,               self.HEIGHT // 2 - 5),
                (0,                self.HEIGHT // 2),
                (fe,               self.HEIGHT // 2 + 5)
            ])
            thrust_images.append(small)
            # Large thrust flame frame
            large = base.copy()
            pygame.draw.polygon(large, ec, [
                (fe,               self.HEIGHT // 2 - 5),
                (0,                self.HEIGHT // 2),
                (fe,               self.HEIGHT // 2 + 5)
            ])
            thrust_images.append(large)
        # Store base image and generated thrust frames
        self.base_image = base
        self.thrust_images = thrust_images
        # Update frame count for animation
        self.animation_frames = len(self.thrust_images)
    
    def update_image(self):
        """Update all animation frames with the current color"""
        self.create_animation_frames()
    
    def change_color(self, color):
        """Change spacecraft color"""
        if color in self.COLORS:
            self.color = color
            self.update_image()
            
    def draw(self, screen):
        """Draw spacecraft, showing thrust flame if recently thrusted"""
        # Determine if we should display thrust flame
        now = pygame.time.get_ticks()
        if now - self.last_thrust_time < self.thrust_display_time:
            # Animated thrust image
            current = self.thrust_images[self.current_frame]
        else:
            # Base image without exhaust
            current = self.base_image
        # Rotate current frame image (positive angle tilts nose up)
        rotated = pygame.transform.rotate(current, self.angle)
        # Compute center position considering flame extension
        cx = self.x + self.WIDTH // 2 + self.flame_extent // 2
        cy = self.y + self.HEIGHT // 2
        rect = rotated.get_rect(center=(cx, cy))
        screen.blit(rotated, rect.topleft)