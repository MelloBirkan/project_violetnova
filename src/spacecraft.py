import pygame
import os

class Spacecraft:
    WIDTH = 98
    HEIGHT = 38
    
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
        # Flame colors override: gradient from outer to inner (static outer, dynamic inner)
        self.flame_colors = [
            (178, 34, 34),    # Dark red (outer)
            (255, 69, 0),     # Red-orange
            (255, 165, 0),    # Orange
            (255, 255, 0),    # Yellow
            (255, 200, 0)   # White (inner tip dynamic)
        ]
        # Thrust control
        self.thrusting = False
        self.thrust_power = 3.0
        self.thrust_multiplier = 1.0
        # Thrust visual timing and flame extent (ms & px)
        self.last_thrust_time = 0
        self.thrust_display_time = 400  # ms to display thrust flame
        # Flame extension width for more prominent engine flame (wider for bigger effect)
        self.flame_extent = 40
        # Flame animation variables
        self.animation_frames = 10
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_counter = 0
        # Load spacecraft sprite
        self.sprite_path = os.path.join("assets", "images", "nova_2x.png")
        self.sprite = pygame.image.load(self.sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (self.WIDTH, self.HEIGHT))
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
        """Create all frames for spacecraft animation with layered fire colors"""
        # Prepare base surface with spacecraft sprite
        fe = self.flame_extent
        total_w = self.WIDTH + fe
        base = pygame.Surface((total_w, self.HEIGHT), pygame.SRCALPHA)
        base.fill((0, 0, 0, 0))
        sprite_rect = pygame.Rect(fe, 0, self.WIDTH, self.HEIGHT)
        base.blit(self.sprite, sprite_rect)

        # Position flame slightly lower than center
        lower_offset = int(self.HEIGHT * 0.2)
        center_y = self.HEIGHT // 2 + lower_offset
        height_offset = max(5, int(self.HEIGHT * 0.2))

        # Separate outer static gradient layers and inner dynamic tip
        engine_colors = self.flame_colors if self.flame_colors else [self.COLORS[self.color]["engine"]]
        static_colors = engine_colors[:-1]
        dynamic_color = engine_colors[-1]

        # Flicker widths for dynamic tip animation
        flicker_widths = [int(fe * 0.2), fe]

        thrust_images = []
        for fw in flicker_widths:
            img = base.copy()
            # Draw static outer gradient layers (continuous)
            for i, sc in enumerate(static_colors):
                lw_static = fe * (len(static_colors) - i) / len(static_colors)
                points = [
                    (lw_static, center_y - height_offset),
                    (0,         center_y),
                    (lw_static, center_y + height_offset)
                ]
                pygame.draw.polygon(img, sc, points)
            # Draw dynamic inner tip (end animation)
            points_tip = [
                (fw, center_y - height_offset),
                (0,  center_y),
                (fw, center_y + height_offset)
            ]
            pygame.draw.polygon(img, dynamic_color, points_tip)
            thrust_images.append(img)

        self.base_image = base
        self.thrust_images = thrust_images
        self.animation_frames = len(self.thrust_images)
    
    def update_image(self):
        """Update all animation frames with the current color"""
        self.create_animation_frames()
    
    def change_color(self, color):
        """Change spacecraft color"""
        if color in self.COLORS:
            self.color = color
            # With sprite implementation, we just need to update the flame colors
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