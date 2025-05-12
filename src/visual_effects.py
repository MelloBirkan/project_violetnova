import random
import math
import pygame
import src.config as config
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_HEIGHT

class VisualEffectsManager:
    def __init__(self, game):
        self.game = game
        self.screen_shake = 0
        self.flash_effect = 0
        self.stars = self._generate_stars(100)
        
    def update(self):
        """Update all visual effects"""
        # Update star twinkle effect
        self._update_stars()
        
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
            
        # Update flash effect
        if self.flash_effect > 0:
            self.flash_effect -= 1
    
    def _update_stars(self):
        """Update stars' twinkle effect"""
        for star in self.stars:
            star["phase"] += star["twinkle_speed"]
            twinkle_factor = 0.5 + 0.5 * math.sin(star["phase"])
            star["brightness"] = int(star["base_brightness"] * twinkle_factor)
    
    def _generate_stars(self, count):
        """Generate background stars"""
        stars = []
        for _ in range(count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT - FLOOR_HEIGHT)
            size = random.uniform(0.5, 2.0)
            brightness = random.randint(150, 255)
            twinkle_speed = random.uniform(0.02, 0.1)
            phase = random.uniform(0, 2 * math.pi)
            stars.append({
                "x": x,
                "y": y,
                "size": size,
                "brightness": brightness,
                "base_brightness": brightness,
                "twinkle_speed": twinkle_speed,
                "phase": phase
            })
        return stars
    
    def trigger_screen_shake(self, intensity=18):
        """Trigger a screen shake effect"""
        self.screen_shake = intensity
        
    def trigger_flash(self, intensity=5):
        """Trigger a screen flash effect"""
        self.flash_effect = intensity
    
    def get_screen_shake_offset(self):
        """Get the current screen shake offset for rendering"""
        if self.screen_shake > 0:
            shake_intensity = min(8, self.screen_shake / 2)
            offset_x = random.randint(-int(shake_intensity), int(shake_intensity))
            offset_y = random.randint(-int(shake_intensity), int(shake_intensity))
            return offset_x, offset_y
        return 0, 0
    
    def draw_background(self, screen, planet):
        """Draw the background with stars and planet background"""
        # Get screen shake offset
        offset_x, offset_y = self.get_screen_shake_offset()
        
        # Fill with dark space background
        screen.fill((0, 0, 20))
        
        # Draw stars
        self._draw_stars(screen, offset_x, offset_y)
        
        # Draw planet background
        self._draw_planet_background(screen, planet, offset_x, offset_y)
        
        # Draw damage flash effect
        self._draw_flash_effect(screen)
    
    def _draw_stars(self, screen, offset_x, offset_y):
        """Draw twinkling stars"""
        for star in self.stars:
            color = (star["brightness"], star["brightness"], star["brightness"])
            x_pos = int(star["x"]) + offset_x
            y_pos = int(star["y"]) + offset_y
            pygame.draw.circle(screen, color, (x_pos, y_pos), star["size"])
    
    def _draw_planet_background(self, screen, planet, offset_x, offset_y):
        """Draw planet's background image or color"""
        if planet.background_image:
            # If planet has a background image, tile it
            bg_width, bg_height = planet.background_image.get_size()
            
            # Calculate tiles needed
            tiles_x = SCREEN_WIDTH // bg_width + 1
            tiles_y = SCREEN_HEIGHT // bg_height + 1
            
            # Draw tiles
            for y in range(tiles_y):
                for x in range(tiles_x):
                    screen.blit(planet.background_image,
                              (x * bg_width + offset_x, y * bg_height + offset_y))
        else:
            # Use color overlay
            bg_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            bg_color = (*planet.background_color, 100)  # Add alpha
            bg_overlay.fill(bg_color)
            screen.blit(bg_overlay, (offset_x, offset_y))
    
    def _draw_flash_effect(self, screen):
        """Draw damage flash effect"""
        if self.flash_effect > 0:
            flash_alpha = min(180, self.flash_effect * 40)
            flash_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_overlay.fill((255, 0, 0, flash_alpha))  # Red flash
            screen.blit(flash_overlay, (0, 0))
    
    def draw_life_icons(self, screen, lives, max_lives, spacecraft_color):
        """Draw life indicator icons"""
        from src.spacecraft import Spacecraft
        
        # Setup dimensions
        life_icon_width = 30
        life_icon_height = 15
        life_icon_padding = 5
        life_base_x = 80
        life_y = 112
        
        for i in range(max_lives):
            # Determine color based on whether this life is available
            if i < lives:
                # Available life - use current spacecraft color
                color = Spacecraft.COLORS[spacecraft_color]["body"]
                alpha = 255
            else:
                # Lost life - gray and semi-transparent
                color = (100, 100, 100)
                alpha = 128
            
            # Create mini-spacecraft icon
            life_icon = pygame.Surface((life_icon_width, life_icon_height), pygame.SRCALPHA)
            life_icon.fill((0, 0, 0, 0))  # Transparent
            
            # Draw simplified spacecraft shape
            pygame.draw.ellipse(life_icon, (*color, alpha),
                              (0, 0, life_icon_width, life_icon_height))
            
            # Add small window/cabin
            window_color = Spacecraft.COLORS[spacecraft_color]["window"]
            pygame.draw.ellipse(life_icon, (*window_color, alpha),
                              (life_icon_width // 2, life_icon_height // 4,
                               life_icon_width // 4, life_icon_height // 2))
            
            # Position the icon
            icon_x = life_base_x + (life_icon_width + life_icon_padding) * i
            
            # Pulsing effect for last life
            if i == 0 and lives == 1:  # Last life
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 255
                pulse_overlay = pygame.Surface((life_icon_width, life_icon_height), pygame.SRCALPHA)
                pulse_overlay.fill((255, 0, 0, int(pulse * 0.5)))  # Pulsing red
                life_icon.blit(pulse_overlay, (0, 0))
            
            # Invulnerability effect
            if self.game.invulnerable and i < lives:
                # Blinking effect
                blink = (pygame.time.get_ticks() // 200) % 2  # Alternates 0/1 every 200ms
                if blink:
                    # Blue overlay to indicate invulnerability
                    shield_overlay = pygame.Surface((life_icon_width, life_icon_height), pygame.SRCALPHA)
                    shield_overlay.fill((100, 100, 255, 100))  # Translucent light blue
                    life_icon.blit(shield_overlay, (0, 0))
            
            # Draw the icon
            screen.blit(life_icon, (icon_x, life_y))
            
    def draw_countdown(self, screen, countdown_number):
        """Draw large countdown number with special effects"""
        if countdown_number <= 0:
            return

        # Add pulse effect to size
        pulse_factor = 1.0 + 0.15 * math.sin(pygame.time.get_ticks() * 0.01)
        pulse_size = int(config.COUNTDOWN_FONT_SIZE * pulse_factor)

        # Use countdown font with pulse effect
        countdown_font = pygame.font.Font(None, pulse_size)

        # Color also pulses
        color_pulse = int(255 * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.015)))
        countdown_text = countdown_font.render(str(countdown_number), True,
                                              (255, color_pulse, color_pulse))
        countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Draw with enhanced glow effect
        glow_size = 12
        for offset_x in range(-glow_size, glow_size + 1, 3):
            for offset_y in range(-glow_size, glow_size + 1, 3):
                if offset_x == 0 and offset_y == 0:
                    continue
                    
                # Calculate distance for glow fade
                distance = math.sqrt(offset_x**2 + offset_y**2)
                alpha = int(120 * (1 - distance/glow_size))
                if alpha <= 0:
                    continue
                
                glow_rect = countdown_rect.move(offset_x, offset_y)
                glow_text = countdown_font.render(str(countdown_number), True, 
                                                 (80, 80, 220, alpha))
                screen.blit(glow_text, glow_rect)
        
        # Draw main text
        screen.blit(countdown_text, countdown_rect)
        
    def draw_pulsing_text(self, screen, text, font, color, position, amplitude=0.3, speed=0.008):
        """Draw text with pulsing alpha effect"""
        alpha_pulse = int(255 * (0.7 + amplitude * math.sin(pygame.time.get_ticks() * speed)))
        text_surface = font.render(text, True, color)
        text_surface.set_alpha(alpha_pulse)
        
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)