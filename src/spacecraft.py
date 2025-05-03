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
        """Create all frames for spacecraft animation with continuous triangle flame gradient and animated tip."""
        fe = self.flame_extent  # Flame Extent (max length)
        total_w = self.WIDTH + fe
        base = pygame.Surface((total_w, self.HEIGHT), pygame.SRCALPHA)
        base.fill((0, 0, 0, 0))
        # Sprite positioned leaving space for the flame on the left
        sprite_rect = pygame.Rect(fe, 0, self.WIDTH, self.HEIGHT)
        base.blit(self.sprite, sprite_rect)

        # Flame positioning
        flame_origin_x = fe  # X-coordinate where flame starts (right side of flame area)
        # Increase the offset to move the flame lower
        lower_offset = int(self.HEIGHT * 0.25) # Slightly lower origin for flame base
        center_y = self.HEIGHT // 2 + lower_offset
        # Max half-height of the flame at its base (nozzle)
        max_flame_base_half_height = max(3, int(self.HEIGHT * 0.15))

        engine_colors = self.flame_colors

        # Flicker lengths for dynamic animation
        # Adjusted lengths for potentially more visible flicker effect
        flicker_tip_lengths = [int(fe * 0.8), int(fe * 1.0), int(fe * 0.9)]
        # Tip animation parameters (size variation for the bright tip element)
        tip_animation_sizes = [3, 5, 4] # Example sizes for the bright tip element

        num_anim_frames = len(flicker_tip_lengths)
        if len(tip_animation_sizes) != num_anim_frames:
             # Ensure animation sizes list matches frame count
             tip_animation_sizes = (tip_animation_sizes * (num_anim_frames // len(tip_animation_sizes) + 1))[:num_anim_frames]

        thrust_images = []
        for idx, current_flame_length in enumerate(flicker_tip_lengths):
            img = base.copy()

            # --- Draw Gradient Flame using Nested Triangles ---
            num_colors = len(engine_colors)
            for i in range(num_colors):
                 color = engine_colors[i]
                 # Length fraction for this color layer (outer layers are longer, inner shorter)
                 # Layer i=0 is outermost, i=num_colors-1 is innermost
                 length_fraction = 1.0 - (i / num_colors)
                 layer_length = current_flame_length * length_fraction

                 # Tip x-coordinate for this layer (extends left from origin)
                 layer_tip_x = flame_origin_x - layer_length

                 # Half-height at the base for this layer (tapers linearly with length)
                 layer_base_half_height = max_flame_base_half_height * length_fraction

                 # Points for this color layer's triangle
                 p_tip = (int(layer_tip_x), center_y)
                 p_base1 = (flame_origin_x, int(center_y - layer_base_half_height))
                 p_base2 = (flame_origin_x, int(center_y + layer_base_half_height))

                 # Ensure points form a valid triangle before drawing
                 if p_tip[0] < p_base1[0] and p_base1[1] < p_base2[1]:
                     pygame.draw.polygon(img, color, [p_tip, p_base1, p_base2]) # Corrected indentation


            # --- Add Animated Tip Element ---
            # Position the tip element at the end of the current frame's flame
            tip_center_x = flame_origin_x - current_flame_length
            tip_center_y = center_y
            tip_size = tip_animation_sizes[idx] # Get size for this frame
            tip_color = (255, 255, 220) # Bright yellowish-white tip

            # Draw a small circle at the tip for animation
            pygame.draw.circle(img, tip_color, (int(tip_center_x), int(tip_center_y)), tip_size)

            thrust_images.append(img)

        self.base_image = base # Store the base image without any flame
        self.thrust_images = thrust_images
        # Update the number of animation frames based on generated images
        self.animation_frames = len(self.thrust_images)
        # Reset frame index just in case
    
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