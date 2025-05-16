import pygame
from src.planet_data import LEVEL_PROGRESSION_THRESHOLDS, PLANET_NAME_PT

class WeaponSystem:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.timer = 0
        
    def update(self):
        """Updates the weapon state"""
        if self.active:
            self.timer -= 1
            self.game.weapon_timer = self.timer
            if self.timer <= 0:
                self.deactivate()
                
    def activate(self, duration=600):
        """Activates the weapon for a specified duration (default 10 seconds at 60fps)"""
        self.active = True
        self.timer = duration
        self.game.weapon_active = True
        self.game.weapon_timer = duration
        self.game.nova.show_message("Sistemas defensivos ativados! Pressione W para usar.", "excited")
        
    def deactivate(self):
        """Deactivates the weapon"""
        self.active = False
        self.timer = 0
        self.game.weapon_active = False
        self.game.weapon_timer = 0
        self.game.nova.show_message("Sistemas defensivos offline", "normal")
        
    def use(self):
        """Uses the weapon to destroy obstacles"""
        if not self.active:
            return

        # Find closest obstacle ahead of the spacecraft
        target_obstacle = None
        min_distance = float('inf')

        # Define the x position of spacecraft body
        spacecraft_body_x = self.game.spacecraft.x + self.game.spacecraft.flame_extent

        for obstacle in self.game.obstacles:
            # Only target obstacles ahead of spacecraft body
            if obstacle.x > spacecraft_body_x:
                distance = obstacle.x - spacecraft_body_x
                if distance < min_distance:
                    min_distance = distance
                    target_obstacle = obstacle

        if target_obstacle:
            # Remove obstacle and grant points
            self.game.obstacles.remove(target_obstacle)
            self.game.score += 2
            self.game.nova.show_message("Obstáculo destruído!", "alert")
            
            # Check progression to next planet based on new score
            current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
                self.game.current_planet.name,
                10  # Default limit for unspecified planets
            )
            if (self.game.score >= current_threshold and 
                self.game.current_planet_index < len(self.game.planets) - 1):
                next_planet_en = self.game.planets[self.game.current_planet_index + 1].name
                next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
                self.game.nova.show_message(f"Navegação automática engajada! Indo para {next_planet_pt}!", "excited")
                
                # Update furthest planet reached in memory
                next_planet = self.game.planets[self.game.current_planet_index + 1].name.lower()
                self.game.furthest_planet_index = max(self.game.furthest_planet_index, self.game.current_planet_index + 1)
                
                # Save current planet and update furthest planet
                self.game.planet_tracker.save(next_planet, update_furthest=True)
                
                # Start quiz for planet advancement
                self.game.state_manager.start_quiz()