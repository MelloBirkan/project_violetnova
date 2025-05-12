from src.config import SCREEN_HEIGHT, FLOOR_HEIGHT, SPACECRAFT_KNOCKBACK, SPACECRAFT_INVULNERABILITY_TIME

class CollisionManager:
    def __init__(self, game):
        self.game = game
        
    def check_collisions(self):
        """Main collision detection method"""
        # Skip collision detection if spacecraft is invulnerable
        if self.game.invulnerable:
            return False
        
        # Check for boundary collisions (ceiling and floor)
        if self._check_boundary_collision():
            return True
        
        # Check for obstacle collisions
        return self._check_obstacle_collisions()
    
    def _check_boundary_collision(self):
        """Check if spacecraft has collided with screen boundaries"""
        spacecraft = self.game.spacecraft
        
        # Check if spacecraft has hit the ceiling or floor
        if (spacecraft.y <= 0 or 
            spacecraft.y + spacecraft.HITBOX_HEIGHT >= SCREEN_HEIGHT - FLOOR_HEIGHT):
            
            return self.handle_collision("boundary")
        
        return False
    
    def _check_obstacle_collisions(self):
        """Check if spacecraft has collided with any obstacles"""
        spacecraft = self.game.spacecraft
        
        # Calculate spacecraft hitbox position
        spacecraft_body_x = spacecraft.x + spacecraft.flame_extent + (spacecraft.WIDTH - spacecraft.HITBOX_WIDTH) / 2
        spacecraft_body_y = spacecraft.y + (spacecraft.HEIGHT - spacecraft.HITBOX_HEIGHT) / 2
        
        # Check each obstacle for collision
        for obstacle in self.game.obstacles:
            # Determine if using sprites and get the width
            using_sprites = hasattr(obstacle, 'using_sprites') and obstacle.using_sprites
            obstacle_width = obstacle.top_width if using_sprites else obstacle.WIDTH
            
            # Check for horizontal overlap
            horizontal_overlap = (
                spacecraft_body_x + spacecraft.HITBOX_WIDTH > obstacle.x and
                spacecraft_body_x < obstacle.x + obstacle_width
            )
            
            if horizontal_overlap:
                # Calculate gap boundaries
                upper_gap_limit = obstacle.gap_y - obstacle.GAP // 2
                lower_gap_limit = obstacle.gap_y + obstacle.GAP // 2
                
                # Check collision with upper obstacle
                if spacecraft_body_y < upper_gap_limit:
                    return self.handle_collision("obstacle", obstacle, "upper")
                
                # Check collision with lower obstacle
                if spacecraft_body_y + spacecraft.HITBOX_HEIGHT > lower_gap_limit:
                    return self.handle_collision("obstacle", obstacle, "lower")
        
        return False
    
    def handle_collision(self, collision_type, obstacle=None, obstacle_part=None):
        """Handle collision effects and consequences"""
        # Reduce lives and check if game over
        has_lives_left = self.game.lose_life()
        
        # Apply appropriate knockback based on collision type
        if collision_type == "boundary":
            self._handle_boundary_collision()
        else:
            self._handle_obstacle_collision(obstacle, obstacle_part)
        
        # Set invulnerability
        self.game.invulnerable = True
        self.game.invulnerable_timer = SPACECRAFT_INVULNERABILITY_TIME
        
        # Visual effects
        self.game.screen_shake = 18
        self.game.flash_effect = 5
        
        # NOVA AI notification
        self.game.nova.show_message("Hull integrity compromised!", "alert")
        
        # Return if still has lives
        return has_lives_left
    
    def _handle_boundary_collision(self):
        """Handle collision with screen boundaries"""
        spacecraft = self.game.spacecraft
        
        # If collision with floor
        if spacecraft.y + spacecraft.HITBOX_HEIGHT >= SCREEN_HEIGHT - FLOOR_HEIGHT:
            # Apply upward knockback
            spacecraft.velocity = SPACECRAFT_KNOCKBACK * 0.8
            # Ensure spacecraft doesn't go below floor
            spacecraft.y = SCREEN_HEIGHT - FLOOR_HEIGHT - spacecraft.HITBOX_HEIGHT
        else:
            # If collision with ceiling, apply downward knockback
            spacecraft.velocity = abs(SPACECRAFT_KNOCKBACK) * 0.8
            # Ensure spacecraft doesn't go above ceiling
            spacecraft.y = 0
    
    def _handle_obstacle_collision(self, obstacle, obstacle_part):
        """Handle collision with obstacles"""
        spacecraft = self.game.spacecraft
        
        # Default knockback
        spacecraft.velocity = SPACECRAFT_KNOCKBACK
        
        # Add horizontal movement to move away from obstacle
        if obstacle:
            # Horizontal knockback
            if spacecraft.x > obstacle.x:
                spacecraft.x += 15  # Push right
            else:
                spacecraft.x -= 15  # Push left
            
            # Vertical knockback based on which part was hit
            if obstacle_part == "upper":
                # Hit top obstacle, push down
                spacecraft.velocity = abs(SPACECRAFT_KNOCKBACK) * 0.8
            elif obstacle_part == "lower":
                # Hit bottom obstacle, push up
                spacecraft.velocity = SPACECRAFT_KNOCKBACK * 0.8
    
    def check_collectible_collisions(self):
        """Check and handle collectible collisions"""
        spacecraft = self.game.spacecraft
        
        for collectible in list(self.game.collectibles):
            # Check collision
            if collectible.check_collision(spacecraft):
                self._handle_collectible_effect(collectible)
                
                # Remove collected item
                self.game.collectibles.remove(collectible)
    
    def _handle_collectible_effect(self, collectible):
        """Apply the effect of a collected item"""
        effect = collectible.get_effect()
        
        if effect["effect"] == "info":
            # Show planet information
            self.game.nova.give_random_fact(self.game.current_planet.name)
            self.game.score += effect["value"]
            self._check_level_progression()
            
        elif effect["effect"] == "time":
            # Extend game time (add score)
            self.game.score += effect["value"]
            self.game.nova.react_to_discovery("fuel")
            self._check_level_progression()
            
        elif effect["effect"] == "attack":
            # Enable weapon temporarily
            self.game.weapon_active = True
            self.game.weapon_timer = 600  # 10 seconds at 60fps
            self.game.nova.react_to_discovery("weapon")
            
        elif effect["effect"] == "life":
            # Add an extra life
            self.game.add_life()
    
    def _check_level_progression(self):
        """Check if score has reached the threshold for planet progression"""
        from src.config import LEVEL_PROGRESSION_THRESHOLDS, PLANET_NAME_PT
        
        # Get threshold for current planet
        current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
            self.game.current_planet.name,
            10  # Default threshold
        )
        
        # Check if score exceeds threshold and more planets are available
        if (self.game.score >= current_threshold and 
            self.game.current_planet_index < len(self.game.planets) - 1):
            
            # Get next planet name
            next_planet_en = self.game.planets[self.game.current_planet_index + 1].name
            next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
            
            # Show navigation message
            self.game.nova.show_message(
                f"Navegação automática engajada! Indo para {next_planet_pt}!", 
                "excited"
            )
            
            # Start quiz for planet advancement
            self.game.state_manager.start_quiz()
            return True
        
        return False