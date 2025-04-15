import pygame

class Quiz:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.current_question = None
        self.options = []
        self.correct_answer = None
        self.selected_option = None
        self.result = None  # 'correct', 'incorrect', or None
        self.quiz_timer = 0
        self.result_timer = 0
        
        # Font for quiz text
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 24)
    
    def start_quiz(self, question, options, correct_answer):
        """Start a new quiz with the given question and options"""
        self.active = True
        self.current_question = question
        self.options = options
        self.correct_answer = correct_answer
        self.selected_option = None
        self.result = None
        self.quiz_timer = 600  # 10 seconds at 60fps
    
    def handle_event(self, event):
        """Handle user input for the quiz"""
        if not self.active or self.result is not None:
            return False
            
        if event.type == pygame.KEYDOWN:
            # Number keys 1-4 for selecting options
            if 49 <= event.key <= 49 + len(self.options) - 1:  # 1-4 keys
                self.selected_option = event.key - 49  # Convert to 0-based index
                self.check_answer()
                return True
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if user clicked on an option button
            mouse_pos = pygame.mouse.get_pos()
            
            # Check each option button
            for i in range(len(self.options)):
                button_rect = self._get_option_rect(i)
                if button_rect.collidepoint(mouse_pos):
                    self.selected_option = i
                    self.check_answer()
                    return True
                    
        return False
    
    def check_answer(self):
        """Check if the selected answer is correct"""
        if self.selected_option == self.correct_answer:
            self.result = "correct"
        else:
            self.result = "incorrect"
            
        self.result_timer = 120  # 2 seconds at 60fps
    
    def update(self):
        """Update quiz state"""
        if not self.active:
            return
            
        # Update timer if quiz is active and no result yet
        if self.result is None:
            self.quiz_timer -= 1
            if self.quiz_timer <= 0:
                # Time's up - count as incorrect
                self.result = "timeout"
                self.result_timer = 120  # 2 seconds at 60fps
        else:
            # Update result display timer
            self.result_timer -= 1
            if self.result_timer <= 0:
                # End quiz
                self.active = False
    
    def _get_option_rect(self, option_index):
        """Get the rectangle for an option button"""
        option_width = 300
        option_height = 40
        option_margin = 20
        
        x = self.screen_width // 2 - option_width // 2
        y = self.screen_height // 2 + 50 + option_index * (option_height + option_margin)
        
        return pygame.Rect(x, y, option_width, option_height)
    
    def draw(self, screen):
        """Draw the quiz interface"""
        if not self.active:
            return
            
        # Draw semi-transparent backdrop
        backdrop = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 200))  # Semi-transparent black
        screen.blit(backdrop, (0, 0))
        
        # Draw quiz title
        title_text = self.font_large.render("Solar System Quiz", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Draw question
        question_text = self.font_medium.render(self.current_question, True, (255, 255, 255))
        question_rect = question_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(question_text, question_rect)
        
        # Draw timer
        timer_width = 200
        timer_height = 10
        timer_x = self.screen_width // 2 - timer_width // 2
        timer_y = self.screen_height // 2 - 20
        
        # Draw timer background
        pygame.draw.rect(screen, (100, 100, 100), (timer_x, timer_y, timer_width, timer_height))
        
        # Draw timer fill based on remaining time
        timer_fill_width = int(timer_width * (self.quiz_timer / 600))
        timer_color = (0, 255, 0) if self.quiz_timer > 200 else (255, 165, 0) if self.quiz_timer > 100 else (255, 0, 0)
        pygame.draw.rect(screen, timer_color, (timer_x, timer_y, timer_fill_width, timer_height))
        
        # Draw options
        for i, option in enumerate(self.options):
            # Get button rectangle
            button_rect = self._get_option_rect(i)
            
            # Determine button color based on state
            button_color = (70, 70, 70)
            text_color = (255, 255, 255)
            
            if self.result is not None:
                if i == self.correct_answer:
                    button_color = (0, 180, 0)  # Green for correct answer
                elif i == self.selected_option and self.result == "incorrect":
                    button_color = (180, 0, 0)  # Red for selected wrong answer
            elif self.selected_option == i:
                button_color = (0, 120, 200)  # Blue for selected option
            
            # Draw button
            pygame.draw.rect(screen, button_color, button_rect, border_radius=5)
            pygame.draw.rect(screen, (200, 200, 200), button_rect, width=2, border_radius=5)
            
            # Draw option text
            option_text = self.font_small.render(f"{i+1}. {option}", True, text_color)
            option_text_rect = option_text.get_rect(midleft=(button_rect.left + 20, button_rect.centery))
            screen.blit(option_text, option_text_rect)
        
        # Draw result message if appropriate
        if self.result is not None:
            if self.result == "correct":
                result_text = self.font_large.render("Correct!", True, (0, 255, 0))
            elif self.result == "incorrect":
                result_text = self.font_large.render("Incorrect!", True, (255, 0, 0))
            else:  # timeout
                result_text = self.font_large.render("Time's Up!", True, (255, 165, 0))
                
            result_rect = result_text.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
            screen.blit(result_text, result_rect)
    
    def is_complete(self):
        """Check if the quiz has been completed"""
        return self.active and self.result is not None and self.result_timer <= 0
    
    def is_correct(self):
        """Check if the player answered correctly"""
        return self.result == "correct"