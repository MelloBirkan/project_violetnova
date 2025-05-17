import pygame
import src.dados.config as config

class Quiz:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.current_question = None
        self.options = []
        self.correct_answer = None
        self.selected_option = None
        self.result = None  # 'correct', 'incorrect', ou None
        self.quiz_timer = 0
        self.result_timer = 0
        
        # Fonte para texto do quiz usando fontes globais
        # GAME_FONT e SMALL_FONT são inicializados em src.main
        self.font_large = config.GAME_FONT
        self.font_medium = config.GAME_FONT
        self.font_small = config.SMALL_FONT
    
    def start_quiz(self, question, options, correct_answer):
        """Inicia um novo quiz com a pergunta e opções dadas"""
        self.active = True
        self.current_question = question
        self.options = options
        self.correct_answer = correct_answer
        self.selected_option = None
        self.result = None
        self.quiz_timer = config.QUIZ_DURATION
    
    def handle_event(self, event):
        """Lida com a entrada do usuário para o quiz"""
        if not self.active or self.result is not None:
            return False
            
        if event.type == pygame.KEYDOWN:
            # Teclas numéricas 1-4 para selecionar opções
            if 49 <= event.key <= 49 + len(self.options) - 1:  # Teclas 1-4
                self.selected_option = event.key - 49  # Converte para índice baseado em 0
                self.check_answer()
                return True
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verifica se o usuário clicou em um botão de opção
            mouse_pos = pygame.mouse.get_pos()
            
            # Verifica cada botão de opção
            for i in range(len(self.options)):
                button_rect = self._get_option_rect(i)
                if button_rect.collidepoint(mouse_pos):
                    self.selected_option = i
                    self.check_answer()
                    return True
                    
        return False
    
    def check_answer(self):
        """Verifica se a resposta selecionada está correta"""
        if self.selected_option == self.correct_answer:
            self.result = "correct"
        else:
            self.result = "incorrect"
            
        self.result_timer = config.QUIZ_RESULT_DURATION
    
    def update(self):
        """Atualiza o estado do quiz"""
        if not self.active:
            return
            
        # Atualiza o temporizador se o quiz estiver ativo e ainda sem resultado
        if self.result is None:
            self.quiz_timer -= 1
            if self.quiz_timer <= 0:
                # Tempo esgotado - conta como incorreto
                self.result = "timeout"
                self.result_timer = config.QUIZ_RESULT_DURATION
        else:
            # Atualiza o temporizador de exibição do resultado
            self.result_timer -= 1
            if self.result_timer <= 0:
                # Fim do quiz
                self.active = False
    
    def _get_option_rect(self, option_index):
        """Obtém o retângulo para um botão de opção"""
        option_width = 300
        option_height = 40
        option_margin = 20
        
        x = self.screen_width // 2 - option_width // 2
        y = self.screen_height // 2 + 50 + option_index * (option_height + option_margin)
        
        return pygame.Rect(x, y, option_width, option_height)
    
    def draw(self, screen):
        """Desenha a interface do quiz"""
        if not self.active:
            return
            
        # Desenha fundo semitransparente
        backdrop = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 200))  # Preto semitransparente
        screen.blit(backdrop, (0, 0))
        
        # Desenha título do quiz
        title_text = self.font_large.render("Quiz do Sistema Solar", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Desenha pergunta
        question_text = self.font_medium.render(self.current_question, True, (255, 255, 255))
        question_rect = question_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(question_text, question_rect)
        
        # Desenha temporizador
        timer_width = 200
        timer_height = 10
        timer_x = self.screen_width // 2 - timer_width // 2
        timer_y = self.screen_height // 2 - 20
        
        # Desenha fundo do temporizador
        pygame.draw.rect(screen, (100, 100, 100), (timer_x, timer_y, timer_width, timer_height))
        
        # Desenha preenchimento do temporizador com base no tempo restante
        timer_fill_width = int(timer_width * (self.quiz_timer / config.QUIZ_DURATION))
        timer_color = (0, 255, 0) if self.quiz_timer > 200 else (255, 165, 0) if self.quiz_timer > 100 else (255, 0, 0)
        pygame.draw.rect(screen, timer_color, (timer_x, timer_y, timer_fill_width, timer_height))
        
        # Desenha opções
        for i, option in enumerate(self.options):
            # Obtém retângulo do botão
            button_rect = self._get_option_rect(i)
            
            # Determina a cor do botão com base no estado
            button_color = (70, 70, 70)
            text_color = (255, 255, 255)
            
            if self.result is not None:
                if i == self.correct_answer:
                    button_color = (0, 180, 0)  # Verde para resposta correta
                elif i == self.selected_option and self.result == "incorrect":
                    button_color = (180, 0, 0)  # Vermelho para resposta errada selecionada
            elif self.selected_option == i:
                button_color = (0, 120, 200)  # Azul para opção selecionada
            
            # Desenha botão
            pygame.draw.rect(screen, button_color, button_rect, border_radius=5)
            pygame.draw.rect(screen, (200, 200, 200), button_rect, width=2, border_radius=5)
            
            # Desenha texto da opção
            option_text = self.font_small.render(f"{i+1}. {option}", True, text_color)
            option_text_rect = option_text.get_rect(midleft=(button_rect.left + 20, button_rect.centery))
            screen.blit(option_text, option_text_rect)
        
        # Desenha mensagem de resultado se apropriado
        if self.result is not None:
            if self.result == "correct":
                result_text = self.font_large.render("Correto!", True, (0, 255, 0))
                result_rect = result_text.get_rect(center=(self.screen_width // 2, 150))
            elif self.result == "incorrect":
                result_text = self.font_large.render("Incorreto!", True, (255, 0, 0))
                result_rect = result_text.get_rect(center=(self.screen_width // 2, 150))
            else:  # timeout
                result_text = self.font_large.render("Tempo Esgotado!", True, (255, 165, 0))
                result_rect = result_text.get_rect(center=(self.screen_width // 2, self.screen_height - 100))

            screen.blit(result_text, result_rect)
    
    def is_complete(self):
        """Verifica se o quiz foi concluído"""
        return self.result is not None and self.result_timer <= 0
    
    def is_correct(self):
        """Verifica se o jogador respondeu corretamente"""
        return self.result == "correct"