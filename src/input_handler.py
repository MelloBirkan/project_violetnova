import pygame
import sys
import src.config as config

class InputHandler:
    def __init__(self, game):
        self.game = game
        
    def handle_events(self):
        """Handles all game input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                self._handle_key_down(event)
                    
            if event.type == pygame.KEYUP:
                self._handle_key_up(event)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event)
    
    def _handle_key_down(self, event):
        """Handles key press events"""
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
            
        if self.game.state == config.QUIZ or self.game.state == config.QUIZ_FAILURE:
            # Only pass events to quiz system if in QUIZ state
            if self.game.state == config.QUIZ:
                self.game.quiz.handle_event(event)
        else:
            if event.key == pygame.K_SPACE:
                self._handle_space_key_press()
                
            # Toggle control mode in game with C
            if event.key == pygame.K_c and self.game.state == config.PLAYING:
                self._handle_c_key_press()
                
            # Activate weapon with W if available
            if event.key == pygame.K_w and self.game.state == config.PLAYING and self.game.weapon_active:
                self.game.weapon_system.use()
    
    def _handle_key_up(self, event):
        """Handles key release events"""
        if event.key == pygame.K_SPACE:
            # Stop continuous thrust when released
            self.game.space_held = False
            # Fade out engine thrust sound
            self.game.sound_manager.stop_thrust(config.SOUND_FADEOUT_TIME)
    
    def _handle_mouse_down(self, event):
        """Handles mouse button press events"""
        if event.button == 1:  # Left mouse button
            if self.game.state == config.QUIZ or self.game.state == config.QUIZ_FAILURE:
                # Only pass events to quiz system if in QUIZ state
                if self.game.state == config.QUIZ:
                    self.game.quiz.handle_event(event)
            else:
                self._handle_left_click()
    
    def _handle_space_key_press(self):
        """Handles Space key press based on game state"""
        if self.game.state == config.MENU:
            self.game.reset()
        elif self.game.state == config.PLAYING:
            # Single thrust when pressed
            self.game.spacecraft.thrust()
            # Play engine thrust sound
            self.game.sound_manager.play_thrust()
            # Enable continuous thrust if in hold mode
            if self.game.control_mode == config.CONTROL_MODE_HOLD:
                self.game.space_held = True
        elif self.game.state == config.GAME_OVER:
            # Reset welcome_sound_played flag
            self.game.welcome_sound_played = False
            self.game.reset()
        elif self.game.state == config.TRANSITION:
            # Skip transition and force start on new planet
            self.game.reset(new_planet=True)
    
    def _handle_c_key_press(self):
        """Handles C key press to toggle control mode"""
        # Toggle control mode between flappy and hold
        self.game.control_mode = config.CONTROL_MODE_HOLD if self.game.control_mode == config.CONTROL_MODE_FLAPPY else config.CONTROL_MODE_FLAPPY
        mode_name = "Segurando" if self.game.control_mode == config.CONTROL_MODE_HOLD else "Toque"
        
        # Update spacecraft flame colors for thrust effect
        if self.game.control_mode == config.CONTROL_MODE_HOLD:
            # Gradient from yellow to orange to red
            self.game.spacecraft.flame_colors = [(255, 255, 0), (255, 165, 0), (255, 69, 0)]
        else:
            # Single color flame
            self.game.spacecraft.flame_colors = []
        self.game.spacecraft.update_image()
        self.game.nova.show_message(f"Modo de controle: {mode_name}", "info")
    
    def _handle_left_click(self):
        """Handles left mouse button click based on game state"""
        if self.game.state == config.MENU:
            self.game.reset()
        elif self.game.state == config.PLAYING:
            self.game.spacecraft.thrust()
            self.game.sound_manager.play_thrust()
        elif self.game.state == config.GAME_OVER:
            # Reset welcome_sound_played flag
            self.game.welcome_sound_played = False
            self.game.reset()
        elif self.game.state == config.TRANSITION:
            # If in transition and sound is playing, allow skipping but continue sound with reduced volume
            if self.game.welcome_sound_timer > 0 and self.game.current_welcome_sound:
                self.game.sound_manager.adjust_welcome_volume(self.game.current_planet.name, 0.3)
            # Force completion of sound timer to allow proceeding
            self.game.welcome_sound_timer = 0
            # Skip transition and force start on new planet
            if self.game.state_manager.transition_time >= config.TRANSITION_DURATION // 2:  # Allow skipping only after half of transition
                self.game.reset(new_planet=True)