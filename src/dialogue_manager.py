import pygame
import math
import os
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
        
        # Áudio para diálogos
        self.current_audio = None
        self.nova_audio_files = []
        self.violet_audio_files = []
        self.audio_playing = False
        
        # Carrega os arquivos de áudio
        self._load_audio_files()
        
    def _load_audio_files(self):
        """Carrega os arquivos de áudio para os diálogos"""
        # Caminho para os arquivos de áudio
        nova_path = os.path.join('assets', 'sounds', 'dialog', 'nova')
        violet_path = os.path.join('assets', 'sounds', 'dialog', 'violet')
        
        # Inicializa lista de áudios de Nova com tamanho 10
        self.nova_audio_files = [None] * 10
        
        # Carrega áudios de NOVA numerados - garante a ordem correta
        for i in range(1, 11):  # Arquivos 1.mp3 a 10.mp3
            audio_path = os.path.join(nova_path, f"{i}.mp3")
            try:
                sound = pygame.mixer.Sound(audio_path)
                # Armazena no índice correto (0-9)
                self.nova_audio_files[i-1] = sound
            except:
                print(f"Não foi possível carregar o áudio: {audio_path}")
        
        # Carrega áudios da Violet
        for i in range(1, 4):  # Arquivos miau1.mp3 a miau3.mp3
            audio_path = os.path.join(violet_path, f"miau{i}.mp3")
            try:
                sound = pygame.mixer.Sound(audio_path)
                self.violet_audio_files.append(sound)
            except:
                print(f"Não foi possível carregar o áudio: {audio_path}")
                self.violet_audio_files.append(None)
    
    def _play_dialogue_audio(self):
        """Toca o áudio para o diálogo atual"""
        current = self.get_current_dialogue()
        speaker = current.get("speaker", "")
        text = current.get("text", "")
        
        # Apenas para o áudio atual se estiver tocando
        if self.current_audio and self.audio_playing:
            self.current_audio.stop()
            self.current_audio = None
            self.audio_playing = False
            
        # Última linha - toca a música do planeta e o último áudio
        if self.current_dialogue_index == len(self.dialogues) - 1:
            # Primeiro toca o último áudio de NOVA
            if speaker == "NOVA-22" and not (text.startswith("[") and text.endswith("]")):
                # Sempre usar o último áudio para a última linha
                if len(self.nova_audio_files) > 0:
                    last_audio = self.nova_audio_files[9]  # Arquivo 10.mp3 (índice 9)
                    if last_audio:
                        last_audio.play()
                        self.current_audio = last_audio
                        self.audio_playing = True
                        if hasattr(self.game, 'nova'):
                            self.game.nova.start_radio_signal(last_audio.get_length() * 1000)
            
            # Inicia a música do planeta atual
            if hasattr(self.game, 'sound_manager') and hasattr(self.game, 'current_planet'):
                self.game.sound_manager.play_planet_music(self.game.current_planet.name)
            return
        
        # Pula o áudio para texto que é descrição narrativa (entre colchetes)
        if text.startswith("[") and text.endswith("]"):
            return
                
        # Seleciona o áudio apropriado para o falante
        if speaker == "NOVA-22":
            # Mapeia as linhas de diálogo para os arquivos de áudio (em ordem numérica)
            # Apenas para falas de NOVA-22 que não são descrições narrativas
            nova_count = 0
            for i in range(self.current_dialogue_index):
                dialogue = self.dialogues[i]
                dialogue_text = dialogue.get("text", "")
                # Conta apenas diálogos reais, ignorando descrições narrativas
                if (dialogue.get("speaker", "") == "NOVA-22" and 
                    not (dialogue_text.startswith("[") and dialogue_text.endswith("]"))):
                    nova_count += 1
            
            # Certifica-se de não exceder o número de arquivos disponíveis
            if nova_count < len(self.nova_audio_files):
                audio = self.nova_audio_files[nova_count]
                if audio:
                    audio.play()
                    self.current_audio = audio
                    self.audio_playing = True
                    # Mostra animação de fala para NOVA
                    if hasattr(self.game, 'nova'):
                        self.game.nova.start_radio_signal(audio.get_length() * 1000)
        elif speaker == "Violet":
            # Para a Violet, utilizamos um áudio aleatório de miau
            import random
            if self.violet_audio_files:
                audio = random.choice(self.violet_audio_files)
                if audio:
                    audio.play()
                    self.current_audio = audio
                    self.audio_playing = True
    
    def load_dialogue(self, dialogue_list):
        """Carrega uma lista de entradas de diálogo"""
        # Formato: [{"speaker": "Violet/Nova", "text": "Mensagem", "expression": "normal"}]
        self.dialogues = dialogue_list
        self.current_dialogue_index = 0
        self.reset_text_display()
        
        # Inicia o áudio para o primeiro diálogo
        self._play_dialogue_audio()
        
        # Define o foco com base no falante do primeiro diálogo
        self._update_focus()
        
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
            # Para qualquer áudio ainda tocando
            if self.current_audio and self.audio_playing:
                self.current_audio.stop()
                self.current_audio = None
                self.audio_playing = False
                
            # Termina o estado de diálogo
            self.game.state_manager.change_state(config.MENU)
            return False
            
        # Reseta para o próximo diálogo e toca o áudio correspondente
        self.reset_text_display()
        self._play_dialogue_audio()
        
        # Atualiza o foco com base no falante atual
        self._update_focus()
        return True
        
    def get_current_dialogue(self):
        """Obtém a entrada de diálogo atual"""
        if 0 <= self.current_dialogue_index < len(self.dialogues):
            return self.dialogues[self.current_dialogue_index]
        return {"speaker": "", "text": "", "expression": "normal"}
        
    def _update_focus(self):
        """Atualiza o foco dos personagens com base no falante atual"""
        current = self.get_current_dialogue()
        speaker = current.get("speaker", "")
        
        # Define o foco com base no falante
        try:
            if speaker == "NOVA-22" or speaker == "Nova":
                if hasattr(self.game, 'nova'):
                    self.game.nova.set_focused(True)
                if hasattr(self.game, 'violet'):
                    self.game.violet.set_focused(False)
            elif speaker == "Violet":
                if hasattr(self.game, 'nova'):
                    self.game.nova.set_focused(False)
                if hasattr(self.game, 'violet'):
                    self.game.violet.set_focused(True)
        except AttributeError:
            # Ignora erros se os métodos não existirem
            pass
    
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
                    
    def draw_background(self, screen):
        """Desenha o fundo e a caixa de diálogo"""
        # Sobreposição semitransparente para o fundo
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
    
    def draw_text(self, screen):
        """Desenha o texto do diálogo e elementos da interface"""
        current = self.get_current_dialogue()
        
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
    
    def draw(self, screen):
        """Método compatível com versões anteriores que desenha tudo"""
        self.draw_background(screen)
        self.draw_text(screen)