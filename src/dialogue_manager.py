import pygame
import math
import src.config as config

class DialogueManager:
    def __init__(self, game):
        self.game = game
        self.dialogues = []  # Lista de entradas de diálogo
        self.current_dialogue_index = 0
        self.displayed_text = ""
        self.char_index = 0
        self.char_delay = 2  # Quadros entre a adição de caracteres
        self.char_timer = 0
        self.text_complete = False
        
    def load_dialogue(self, dialogue_list):
        """Carrega uma lista de entradas de diálogo"""
        # Formato: [{"speaker": "Violet/Nova", "text": "Mensagem", "expression": "normal"}]
        self.dialogues = dialogue_list
        self.current_dialogue_index = 0
        self.reset_text_display()
        
    def reset_text_display(self):
        """Reseta o efeito de digitação do texto"""
        self.displayed_text = ""
        self.char_index = 0
        self.char_timer = 0
        self.text_complete = False
        
    def advance_dialogue(self):
        """Avança para a próxima entrada de diálogo ou pula a digitação"""
        # Se o texto ainda está sendo digitado, completa-o imediatamente
        if not self.text_complete:
            self.displayed_text = self.get_current_dialogue()["text"]
            self.text_complete = True
            return True
            
        # Caso contrário, avança para o próximo diálogo
        self.current_dialogue_index += 1
        
        # Verifica se o diálogo terminou
        if self.current_dialogue_index >= len(self.dialogues):
            # Termina o estado de diálogo
            self.game.state_manager.change_state(config.MENU)
            return False
            
        # Reseta para o próximo diálogo
        self.reset_text_display()
        return True
        
    def get_current_dialogue(self):
        """Obtém a entrada de diálogo atual"""
        if 0 <= self.current_dialogue_index < len(self.dialogues):
            return self.dialogues[self.current_dialogue_index]
        return {"speaker": "", "text": "", "expression": "normal"}
        
    def update(self):
        """Atualiza a exibição do texto do diálogo"""
        current = self.get_current_dialogue()
        
        # Atualiza o efeito de digitação do texto
        if not self.text_complete and self.char_index < len(current["text"]):
            self.char_timer += 1
            if self.char_timer >= self.char_delay:
                self.char_timer = 0
                self.displayed_text += current["text"][self.char_index]
                self.char_index += 1
                
                # Verifica se o texto está completo
                if self.char_index >= len(current["text"]):
                    self.text_complete = True
                    
    def draw(self, screen):
        """Desenha a interface de diálogo"""
        current = self.get_current_dialogue()
        
        # Sobreposição semitransparente para o fundo
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        
        # Desenha a caixa de diálogo na parte inferior
        box_height = 150
        box_y = config.SCREEN_HEIGHT - box_height - 20
        pygame.draw.rect(
            screen, 
            (50, 50, 80), 
            (20, box_y, config.SCREEN_WIDTH - 40, box_height),
            border_radius=15
        )
        pygame.draw.rect(
            screen, 
            (100, 100, 150), 
            (20, box_y, config.SCREEN_WIDTH - 40, box_height),
            width=3,
            border_radius=15
        )
        
        # Desenha o nome do personagem
        if current["speaker"]:
            name_box_width = 120
            name_box_height = 40
            name_box_x = 40
            name_box_y = box_y - 20
            
            # Fundo do nome
            pygame.draw.rect(
                screen,
                (50, 50, 80),
                (name_box_x, name_box_y, name_box_width, name_box_height),
                border_radius=10
            )
            pygame.draw.rect(
                screen,
                (100, 100, 150),
                (name_box_x, name_box_y, name_box_width, name_box_height),
                width=2,
                border_radius=10
            )
            
            # Nome do personagem
            name_text = config.SMALL_FONT.render(current["speaker"], True, (255, 255, 255))
            screen.blit(
                name_text, 
                (name_box_x + name_box_width//2 - name_text.get_width()//2, 
                 name_box_y + name_box_height//2 - name_text.get_height()//2)
            )
        
        # Desenha o texto do diálogo
        text_padding = 20
        font = pygame.font.Font(None, 28)
        
        # Trata texto multilinha quebrando
        words = self.displayed_text.split(' ')
        lines = []
        line = ""
        max_width = config.SCREEN_WIDTH - 80
        
        for word in words:
            test_line = line + word + " "
            test_width = font.size(test_line)[0]
            
            if test_width < max_width:
                line = test_line
            else:
                lines.append(line)
                line = word + " "
                
        lines.append(line)  # Adiciona a última linha
        
        # Desenha cada linha
        for i, line in enumerate(lines):
            line_surf = font.render(line, True, (255, 255, 255))
            screen.blit(line_surf, (40, box_y + text_padding + (i * 30)))
            
        # Desenha o indicador "continuar" se o texto estiver completo
        if self.text_complete:
            continue_text = config.SMALL_FONT.render("Pressione ESPAÇO para continuar", True, (200, 200, 255))
            
            # Adiciona efeito de pulsação
            alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
            continue_text.set_alpha(alpha)
            
            continue_x = config.SCREEN_WIDTH - continue_text.get_width() - 40
            continue_y = box_y + box_height - 30
            screen.blit(continue_text, (continue_x, continue_y))