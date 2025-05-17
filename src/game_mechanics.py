import random
import pygame
from src.obstacle import Obstacle
from src.collectible import Collectible
import src.config as config
from src.planet_data import LEVEL_PROGRESSION_THRESHOLDS, PLANET_NAME_PT

class GameMechanics:
    def __init__(self, game):
        self.game = game
        
    def update(self):
        """Updates game mechanics, obstacles, collectibles, etc."""
        if self.game.state != config.PLAYING:
            return
            
        # Update spacecraft with current planet's gravity and screen limits
        self.game.spacecraft.update(self.game.current_planet.gravity, config.SCREEN_HEIGHT, config.FLOOR_HEIGHT)
        
        # Continuous thrust when space is held in hold mode
        if self.game.control_mode == config.CONTROL_MODE_HOLD and self.game.space_held:
            # Apply small continuous thrust (20% of thrust power)
            cont = self.game.spacecraft.thrust_power * self.game.spacecraft.thrust_multiplier * 0.2
            self.game.spacecraft.velocity -= cont
            # Maintain flame effect
            self.game.spacecraft.last_thrust_time = pygame.time.get_ticks()
            # Ensure engine thrust sound continues playing
            if not pygame.mixer.get_busy() or not self.game.sound_manager.engine_thrust_sound.get_num_channels():
                self.game.sound_manager.play_thrust()
                
        # Generate obstacles
        current_time = pygame.time.get_ticks()
        if current_time - self.game.last_obstacle_time > self.game.obstacle_spawn_rate:
            self.generate_obstacle()
            self.game.last_obstacle_time = current_time
            
        # Generate collectibles
        current_time = pygame.time.get_ticks()
        if current_time - self.game.last_collectible_time > self.game.collectible_spawn_rate:
            self.generate_collectible()
            self.game.last_collectible_time = current_time
            
        # Update obstacles and check score
        for obstacle in self.game.obstacles:
            obstacle.update()
            
            # Score when passing an obstacle
            if not obstacle.scored and obstacle.x + obstacle.WIDTH < self.game.spacecraft.x:
                self.game.score += 1
                obstacle.scored = True
                
                # Check progression
                self.check_progression()
                
        # Check collisions with collectibles
        self.game.collision_manager.check_collectible_collisions()
        
        # Update collectibles
        for collectible in list(self.game.collectibles):
            collectible.update()
            collectible.x -= self.game.obstacle_speed  # Move at same speed as obstacles
            
        # Remove off-screen obstacles and collectibles
        self.game.obstacles = [obs for obs in self.game.obstacles if obs.x > -obs.WIDTH]
        self.game.collectibles = [col for col in self.game.collectibles if col.x > -col.WIDTH]
        
        # Check collisions
        collision_result = self.game.collision_manager.check_collisions()
        if collision_result is not False:
            # Play collision sound
            self.game.sound_manager.play_collision()
            
        # Move the floor
        self.game.floor_x = (self.game.floor_x - self.game.obstacle_speed) % 800
            
    def generate_obstacle(self):
        """Generates a new obstacle"""
        # Define fixed gap between obstacles
        gap_size = Obstacle.GAP
        
        # Calculate minimum and maximum values for gap center
        min_gap_center_y = gap_size // 2
        max_gap_center_y = config.SCREEN_HEIGHT - config.FLOOR_HEIGHT - (gap_size // 2)
        
        # Handle extreme cases with extreme constants
        if min_gap_center_y > max_gap_center_y:
            target_y = ((gap_size // 2) + (config.SCREEN_HEIGHT - config.FLOOR_HEIGHT - (gap_size // 2))) // 2
            
            # Define absolute limits for fixing
            abs_min_y = gap_size // 2
            abs_max_y = config.SCREEN_HEIGHT - config.FLOOR_HEIGHT - (gap_size // 2)
            
            if abs_min_y > abs_max_y:  # e.g., gap_size > playable height
                # Just use the middle of the playable screen height
                target_y = (config.SCREEN_HEIGHT - config.FLOOR_HEIGHT) // 2
            else:
                # Fix target_y to physically possible range
                target_y = max(abs_min_y, min(target_y, abs_max_y))
                
            min_gap_center_y = target_y
            max_gap_center_y = target_y
            
        # Generate random y position for gap center
        gap_y = random.randint(min_gap_center_y, max_gap_center_y)
        
        # Randomly select obstacle type
        obstacle_type = random.choice(list(Obstacle.TYPES.keys()))
        
        # Get current planet name
        current_planet_name = self.game.current_planet.name
        
        # Create new obstacle with planet name
        new_obstacle = Obstacle(
            config.SCREEN_WIDTH, 
            gap_y, 
            self.game.obstacle_speed, 
            obstacle_type, 
            config.SCREEN_HEIGHT,
            current_planet_name
        )
        self.game.obstacles.append(new_obstacle)
        
        # Occasionally have NOVA alert about obstacles
        if random.random() < 0.3:  # 30% chance
            pass  # Placeholder for any future NOVA alerts about obstacles
            
    def generate_collectible(self):
        """Generates a new collectible"""
        settings = config.DIFFICULTY_SETTINGS[self.game.difficulty]

        # Se não houver colecionáveis nesta dificuldade, sai
        if settings["life_collectible_chance"] == 0 and settings["weapon_collectible_chance"] == 0:
            return

        x = config.SCREEN_WIDTH
        y = random.randint(100, config.SCREEN_HEIGHT - config.FLOOR_HEIGHT - 50)

        rand_val = random.random()
        collectible_type = "data"
        life_chance = settings["life_collectible_chance"]
        weapon_chance = settings["weapon_collectible_chance"]

        if rand_val < life_chance:
            collectible_type = "life"
        elif rand_val < life_chance + weapon_chance and not self.game.weapon_active:
            collectible_type = "weapon"

        self.game.collectibles.append(Collectible(x, y, collectible_type))
        
    def check_progression(self):
        """Checks if player has met criteria to progress to next planet"""
        # Get threshold for current planet
        current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
            self.game.current_planet.name,
            10  # Default limit
        )
        
        # Check if score threshold has been reached for automatic progression
        if (self.game.score >= current_threshold and 
            self.game.current_planet_index < len(self.game.planets) - 1):
            
            # NOVA announces automatic progression
            next_planet_en = self.game.planets[self.game.current_planet_index + 1].name
            next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
            self.game.nova.show_message(f"Navegação automática engajada! Indo para {next_planet_pt}!", "excited")
            
            # Update furthest planet reached
            next_planet = self.game.planets[self.game.current_planet_index + 1].name.lower()
            current_planet = self.game.current_planet.name.lower()
            self.game.furthest_planet_index = max(self.game.furthest_planet_index, self.game.current_planet_index + 1)
            
            # Save current planet and update furthest planet, respeitando checkpoints
            self.game.planet_tracker.save(
                current_planet,  # Salva o planeta ATUAL, não o próximo
                update_furthest=True,
                allow_save=config.DIFFICULTY_SETTINGS[self.game.difficulty]["save_checkpoint"],
            )
            
            # Start quiz without incrementing planet index yet - let quiz handle progression
            self.game.state_manager.start_quiz()
            
    def handle_collectible_effect(self, collectible):
        """Applies the effect of a collected collectible"""
        if collectible.type == "data":
            self.game.score += 1
            self.game.nova.show_message("Dados coletados! +1 ponto", "normal")
            
        elif collectible.type == "life":
            if self.game.add_life():
                self.game.nova.show_message("Vida extra obtida!", "excited")
            else:
                self.game.nova.show_message("Já está com o máximo de vidas!", "normal")
                self.game.score += 2  # Bonus points instead
                
        elif collectible.type == "weapon":
            self.game.weapon_system.activate()