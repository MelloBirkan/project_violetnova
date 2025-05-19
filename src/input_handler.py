import pygame
import pygame.time
import sys
import src.config as config

class InputHandler:
    def __init__(self, game):
        self.game = game
        
    def handle_events(self):
        """Processa todos os eventos de entrada do jogo"""
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
        """Lida com eventos de pressionamento de tecla"""
        if event.key == pygame.K_ESCAPE:
            # Se está no menu principal ou submenu de dificuldade
            if self.game.state == config.MENU:
                if self.game.in_difficulty_menu:
                    # Se está no submenu de dificuldade, volta ao menu principal
                    self.game.in_difficulty_menu = False
                else:
                    # Se está no menu principal, sai do jogo
                    pygame.quit()
                    sys.exit()
            else:
                # Se está jogando, volta ao menu
                self.game.state_manager.change_state(config.MENU)
                self.game.state = config.MENU
                self.game.sound_manager.stop_all_sounds()
                # Reseta alguns estados
                self.game.space_held = False
                self.game.in_difficulty_menu = False
            
        if self.game.state == config.MENU:
            if self.game.in_difficulty_menu:
                if event.key == pygame.K_UP:
                    self.game.selected_difficulty = (self.game.selected_difficulty - 1) % 3
                elif event.key == pygame.K_DOWN:
                    self.game.selected_difficulty = (self.game.selected_difficulty + 1) % 3
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.game.difficulty = self.game.selected_difficulty
                    self.game.in_difficulty_menu = False
            else:
                # Navegação do menu principal
                if event.key == pygame.K_UP:
                    self.game.selected_menu_option = (self.game.selected_menu_option - 1) % len(config.MENU_OPTIONS)
                    if hasattr(self.game.sound_manager, 'menu_select_sound'):
                        self.game.sound_manager.menu_select_sound.play()
                elif event.key == pygame.K_DOWN:
                    self.game.selected_menu_option = (self.game.selected_menu_option + 1) % len(config.MENU_OPTIONS)
                    if hasattr(self.game.sound_manager, 'menu_select_sound'):
                        self.game.sound_manager.menu_select_sound.play()
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._handle_menu_selection()
        elif self.game.state == config.QUIZ or self.game.state == config.QUIZ_FAILURE:
            # Só repassa eventos ao quiz se estiver no estado QUIZ
            if self.game.state == config.QUIZ:
                self.game.quiz.handle_event(event)
        else:
            if event.key == pygame.K_SPACE:
                self._handle_space_key_press()
                
            # Alterna o modo de controle com C
            if event.key == pygame.K_c and self.game.state == config.PLAYING:
                self._handle_c_key_press()
                
            # Ativa a arma com W se disponível
            if event.key == pygame.K_w and self.game.state == config.PLAYING and self.game.weapon_active:
                self.game.weapon_system.use()
                
            # Alterna o controle de IA com A
            if event.key == pygame.K_a and self.game.state == config.PLAYING:
                self._handle_a_key_press()
                
            # Inicia o modo de treinamento com T (para desenvolvimento)
            if event.key == pygame.K_t and self.game.state == config.PLAYING:
                self._handle_t_key_press()
    
    def _handle_key_up(self, event):
        """Lida com eventos de soltura de tecla"""
        if event.key == pygame.K_SPACE:
            # Para o impulso contínuo ao soltar a tecla
            self.game.space_held = False
            # Faz fade out no som do motor
            self.game.sound_manager.stop_thrust(config.SOUND_FADEOUT_TIME)
    
    def _handle_mouse_down(self, event):
        """Lida com cliques do mouse"""
        if event.button == 1:  # Botão esquerdo do mouse
            if self.game.state == config.QUIZ or self.game.state == config.QUIZ_FAILURE:
                # Só repassa eventos ao quiz se estiver no estado QUIZ
                if self.game.state == config.QUIZ:
                    self.game.quiz.handle_event(event)
            else:
                self._handle_left_click()
    
    def _handle_space_key_press(self):
        """Trata a tecla Espaço conforme o estado do jogo"""
        if self.game.state == config.MENU:
            # Tecla Espaço no menu ativa a opção selecionada
            self._handle_menu_selection()
        elif self.game.state == config.PLAYING:
            # Impulso único ao pressionar
            self.game.spacecraft.thrust()
            # Reproduz o som do motor
            self.game.sound_manager.play_thrust()
            # Habilita impulso contínuo se estiver no modo segurar
            if self.game.control_mode == config.CONTROL_MODE_HOLD:
                self.game.space_held = True
        elif self.game.state == config.GAME_OVER:
            # Reset welcome_sound_played flag
            self.game.welcome_sound_played = False
            # Verifica as configurações de dificuldade
            difficulty_settings = config.DIFFICULTY_SETTINGS[self.game.difficulty]
            
            # Garante que qualquer som ou música ainda em execução seja pausada
            self.game.sound_manager.stop_all_sounds()
            self.game.sound_manager.stop_music(500)
            pygame.time.delay(100)  # Pequena pausa para garantir que o mixer esteja pronto
            
            # Se tem checkpoint, continua do planeta onde morreu
            # Se não tem checkpoint (médio/difícil), volta para a Terra
            if difficulty_settings["save_checkpoint"]:
                self.game.reset(continue_from_death=True)
            else:
                self.game.reset()  # Volta para a Terra
        elif self.game.state == config.TRANSITION:
            # Skip transition and force start on new planet
            self.game.reset(new_planet=True)
    
    def _handle_c_key_press(self):
        """Trata a tecla C para alternar o modo de controle"""
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
        
    def _handle_a_key_press(self):
        """Trata a tecla A para alternar o controle de IA"""
        # Desativa o modo de segurar espaço se a IA estiver ativada
        if not self.game.ai_enabled:
            # Se estamos ativando a IA, armazena o estado atual de space_held
            self.prev_space_held = self.game.space_held
            self.game.space_held = False
        else:
            # Se estamos desativando a IA, restaura o estado anterior de space_held
            if hasattr(self, 'prev_space_held'):
                self.game.space_held = self.prev_space_held
        
        # Alterna o modo de IA
        self.game.toggle_ai()
        
    def _handle_t_key_press(self):
        """Trata a tecla T para iniciar o treinamento acelerado da IA"""
        # Verifica se já estamos em modo de treinamento
        if self.game.ai_training_mode:
            self.game.nova.show_message("Treinamento já em andamento!", "warning")
            return
            
        # Inicia o treinamento acelerado
        self.game.start_training_mode(iterations=10)
    
    def _handle_menu_selection(self):
        """Processa a seleção de opções do menu"""
        selected_option = config.MENU_OPTIONS[self.game.selected_menu_option]

        if selected_option == "Jogar":
            # Verifica se deve continuar do planeta salvo ou começar novo jogo
            difficulty_settings = config.DIFFICULTY_SETTINGS[self.game.difficulty]
            
            # Se permite checkpoint e tem planeta salvo diferente de Earth/Terra
            if (difficulty_settings["save_checkpoint"] and 
                self.game.last_planet.lower() not in ["earth", "terra"] and
                self.game.current_planet_index > 0):
                # Continua do planeta salvo
                self.game.reset(continue_from_saved=True)
            else:
                # Começa novo jogo da Terra
                self.game.reset()
        elif selected_option == "Dificuldade":
            self.game.in_difficulty_menu = True
            self.game.selected_difficulty = self.game.difficulty
        elif selected_option == "Configurações":
            # TODO: Implement settings screen
            self.game.nova.show_message("Configurações em breve!", "info")
        elif selected_option == "Créditos":
            # TODO: Implement credits screen
            self.game.nova.show_message("Créditos em breve!", "info")
        elif selected_option == "Sair":
            pygame.quit()
            sys.exit()
    
    def _handle_left_click(self):
        """Lida com clique do botão esquerdo conforme o estado"""
        if self.game.state == config.MENU:
            if self.game.in_difficulty_menu:
                self.game.difficulty = self.game.selected_difficulty
                
                # Atualiza o número máximo de vidas de acordo com a dificuldade
                settings = config.DIFFICULTY_SETTINGS[self.game.difficulty]
                self.game.max_lives = settings.get("max_lives", settings["lives"])
                
                # Limita as vidas ao novo máximo (se o máximo foi reduzido)
                if self.game.lives > self.game.max_lives:
                    self.game.lives = self.game.max_lives
                    
                self.game.in_difficulty_menu = False
            else:
                self.game.reset()
        elif self.game.state == config.PLAYING:
            self.game.spacecraft.thrust()
            self.game.sound_manager.play_thrust()
        elif self.game.state == config.GAME_OVER:
            # Reset welcome_sound_played flag
            self.game.welcome_sound_played = False
            # Verifica as configurações de dificuldade
            difficulty_settings = config.DIFFICULTY_SETTINGS[self.game.difficulty]
            
            # Garante que qualquer som ou música ainda em execução seja pausada
            self.game.sound_manager.stop_all_sounds()
            self.game.sound_manager.stop_music(500)
            pygame.time.delay(100)  # Pequena pausa para garantir que o mixer esteja pronto
            
            # Se tem checkpoint, continua do planeta onde morreu
            # Se não tem checkpoint (médio/difícil), volta para a Terra
            if difficulty_settings["save_checkpoint"]:
                self.game.reset(continue_from_death=True)
            else:
                self.game.reset()  # Volta para a Terra
        elif self.game.state == config.TRANSITION:
            # If in transition and sound is playing, allow skipping but continue sound with reduced volume
            if self.game.welcome_sound_timer > 0 and self.game.current_welcome_sound:
                self.game.sound_manager.adjust_welcome_volume(self.game.current_planet.name, 0.3)
            # Force completion of sound timer to allow proceeding
            self.game.welcome_sound_timer = 0
            # Skip transition and force start on new planet
            if self.game.state_manager.transition_time >= config.TRANSITION_DURATION // 2:  # Allow skipping only after half of transition
                self.game.reset(new_planet=True)