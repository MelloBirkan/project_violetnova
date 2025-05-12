from src.config import (
    MENU, PLAYING, GAME_OVER, TRANSITION, QUIZ, QUIZ_FAILURE,
    TRANSITION_DURATION
)

class StateManager:
    def __init__(self, game):
        self.game = game
        self.current_state = MENU
        self.transition_time = 0
        self.welcome_sound_timer = 0
        self.quiz_failure_timer = 0
        self.last_countdown_number = 0
        
    def change_state(self, new_state):
        """Change the game state and perform necessary setup"""
        self.current_state = new_state
        # Update game's internal state to match
        self.game._state = new_state

        # Reset state-specific timers
        if new_state == TRANSITION:
            self.transition_time = 0
        elif new_state == QUIZ_FAILURE:
            self.quiz_failure_timer = 180  # 3 seconds at 60fps
            self.last_countdown_number = 3
            
    def is_state(self, state):
        """Check if the current state matches the given state"""
        return self.current_state == state
        
    def update(self):
        """Update timers and state transitions"""
        # Update welcome sound timer
        if self.welcome_sound_timer > 0:
            self.welcome_sound_timer -= 16  # Approximately 16ms per frame at 60fps

        try:
            # Handle state-specific timers and transitions
            if self.current_state == TRANSITION:
                self.transition_time += 1

                # Check if transition is complete
                if self.transition_time >= TRANSITION_DURATION and self.welcome_sound_timer <= 0:
                    self.game.reset(new_planet=True)

            elif self.current_state == QUIZ:
                # Update the quiz
                if hasattr(self.game, 'quiz'):
                    self.game.quiz.update()

                    # Check if the quiz is complete
                    if self.game.quiz.is_complete():
                        if self.game.quiz.is_correct():
                            # Proceed to the next planet
                            self.start_transition()
                        else:
                            # Failed quiz, set delay before returning to game
                            self.change_state(QUIZ_FAILURE)
                            self.quiz_failure_timer = 180  # 3 seconds at 60fps
                            self.last_countdown_number = 3
                            # Add a NOVA message about quiz failure
                            if hasattr(self.game, 'nova'):
                                self.game.nova.show_message("Quiz falhou! Retornando à órbita em...", "alert")

            elif self.current_state == QUIZ_FAILURE:
                self.quiz_failure_timer -= 1

                # Update countdown number if needed
                current_countdown = self.quiz_failure_timer // 60 + 1
                if current_countdown < self.last_countdown_number and current_countdown >= 0:
                    self.last_countdown_number = current_countdown

                    # Show NOVA message about countdown
                    if current_countdown > 0 and hasattr(self.game, 'nova'):
                        self.game.nova.show_message(
                            f"Retornando à órbita em {current_countdown}...",
                            "alert"
                        )

                # Check if failure timer is complete
                if self.quiz_failure_timer <= 0:
                    self.change_state(PLAYING)
                    if hasattr(self.game, 'nova'):
                        self.game.nova.show_message(
                            "De volta ao voo orbital! Continue explorando.",
                            "info"
                        )
                    self.last_countdown_number = 0
        except AttributeError:
            # If any attribute is missing during initialization, just skip the update
            pass
                
    def start_quiz(self):
        """Start the quiz state with a random question"""
        self.change_state(QUIZ)
        self.last_countdown_number = 2

        try:
            # Make sure the game has the necessary attributes
            if hasattr(self.game, 'current_planet') and hasattr(self.game, 'quiz'):
                # Select a random quiz question for the current planet
                import random
                question_data = random.choice(self.game.current_planet.quiz_questions)

                # Start the quiz with the selected question
                self.game.quiz.start_quiz(
                    question_data["question"],
                    question_data["options"],
                    question_data["answer"]
                )
        except (AttributeError, IndexError) as e:
            # Log error and continue
            print(f"Error starting quiz: {e}")
        
    def start_transition(self):
        """Start transition to the next planet"""
        self.change_state(TRANSITION)

        try:
            # Stop all sounds
            if hasattr(self.game, 'sound_manager'):
                self.game.sound_manager.stop_all_sounds()

            # Increment planet index
            if hasattr(self.game, 'current_planet_index') and hasattr(self.game, 'planets'):
                self.game.current_planet_index += 1

                # Check if we've reached the end of all planets
                if self.game.current_planet_index >= len(self.game.planets):
                    self.change_state(GAME_OVER)
                    if hasattr(self.game, 'sound_manager'):
                        self.game.sound_manager.play_explosion()

                    # Update high score if needed
                    if hasattr(self.game, 'score') and hasattr(self.game, 'high_score_manager'):
                        if self.game.score > self.game.high_score_manager.get():
                            self.game.high_score = self.game.score
                            self.game.high_score_manager.save(self.game.score)
                    return

                # Update current planet
                self.game.current_planet = self.game.planets[self.game.current_planet_index]

                # Play welcome sound for new planet
                from src.config import PLANET_NAME_PT
                planet_name_en = self.game.current_planet.name
                planet_name_pt = PLANET_NAME_PT.get(planet_name_en, planet_name_en)

                # Play welcome sound and set timer
                if hasattr(self.game, 'sound_manager'):
                    self.welcome_sound_timer = self.game.sound_manager.play_welcome(planet_name_en)

                # NOVA announces the new planet
                if hasattr(self.game, 'nova'):
                    self.game.nova.show_message(
                        f"Entrando na órbita de {planet_name_pt}!",
                        "excited"
                    )

        except (AttributeError, IndexError) as e:
            # Log error and continue
            print(f"Error starting transition: {e}")