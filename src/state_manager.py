import pygame
import src.config as config

class StateManager:
    def __init__(self, game):
        self.game = game
        self.current_state = config.MENU
        self.transition_time = 0
        self.welcome_sound_timer = 0
        self.quiz_failure_timer = 0
        self.last_countdown_number = 0
        
    def change_state(self, new_state):
        """Muda o estado do jogo e realiza a configuração necessária"""
        self.current_state = new_state
        # Atualiza o estado interno do jogo para corresponder
        self.game._state = new_state

        # Reseta temporizadores específicos do estado
        if new_state == config.TRANSITION:
            self.transition_time = 0
        elif new_state == config.QUIZ_FAILURE:
            self.quiz_failure_timer = 180  # 3 segundos a 60fps
            self.last_countdown_number = 3
            
        # Inicia música do planeta ao entrar no modo de jogo
        if new_state == config.PLAYING and hasattr(self.game, 'sound_manager') and hasattr(self.game, 'current_planet'):
            # Inicia a música de fundo específica do planeta com volume baixo
            self.game.sound_manager.play_planet_music(self.game.current_planet.name)
            
    def is_state(self, state):
        """Verifica se o estado atual corresponde ao estado fornecido"""
        return self.current_state == state
        
    def update(self):
        """Atualiza temporizadores e transições de estado"""
        # Atualiza o temporizador do som de boas-vindas
        if self.welcome_sound_timer > 0:
            self.welcome_sound_timer -= 16  # Aproximadamente 16ms por quadro a 60fps

        try:
            # Lida com temporizadores e transições específicos do estado
            if self.current_state == config.TRANSITION:
                self.transition_time += 1

                # Verifica se a transição está completa
                if self.transition_time >= config.TRANSITION_DURATION and self.welcome_sound_timer <= 0:
                    # Se estiver em transição após a morte, mantém o mesmo planeta
                    if hasattr(self.game, 'planet_at_death') and self.game.current_planet_index == self.game.planet_at_death:
                        # Continua no mesmo planeta após a morte
                        self.change_state(config.PLAYING)
                        # Garante que a música esteja tocando
                        if hasattr(self.game, 'sound_manager') and hasattr(self.game, 'current_planet'):
                            self.game.sound_manager.play_planet_music(self.game.current_planet.name)
                    else:
                        # Transição normal entre planetas
                        self.game.reset(new_planet=True)

            elif self.current_state == config.QUIZ:
                # Atualiza o quiz
                if hasattr(self.game, 'quiz'):
                    self.game.quiz.update()

                    # Verifica se o quiz está completo
                    if self.game.quiz.is_complete():
                        if self.game.quiz.is_correct():
                            # Prossegue para o próximo planeta
                            self.start_transition()
                        else:
                            # Quiz falhou, define atraso antes de retornar ao jogo
                            # NÃO parar a música, apenas continuar tocando
                                
                            self.change_state(config.QUIZ_FAILURE)
                            self.quiz_failure_timer = 180  # 3 segundos a 60fps
                            self.last_countdown_number = 3
                            # Adiciona uma mensagem da NOVA sobre a falha no quiz
                            if hasattr(self.game, 'nova'):
                                self.game.nova.show_message("Quiz falhou! Retornando à órbita em...", "alert")

            elif self.current_state == config.QUIZ_FAILURE:
                self.quiz_failure_timer -= 1

                # Atualiza o número da contagem regressiva, se necessário
                current_countdown = self.quiz_failure_timer // 60 + 1
                if current_countdown < self.last_countdown_number and current_countdown >= 0:
                    self.last_countdown_number = current_countdown

                    # Mostra mensagem da NOVA sobre a contagem regressiva
                    if current_countdown > 0 and hasattr(self.game, 'nova'):
                        self.game.nova.show_message(
                            f"Retornando à órbita em {current_countdown}...",
                            "alert"
                        )

                # Verifica se o temporizador de falha está completo
                if self.quiz_failure_timer <= 0:
                    self.change_state(config.PLAYING)
                    
                    # Verifica se a música está tocando e só reinicia se necessário
                    if hasattr(self.game, 'sound_manager') and hasattr(self.game, 'current_planet'):
                        if not pygame.mixer.music.get_busy():
                            # Música parou, reinicia com fade in suave
                            self.game.sound_manager.music_volume = 0.3  # Volume baixo para fade in
                            self.game.sound_manager.play_planet_music(self.game.current_planet.name)
                            self.game.sound_manager.adjust_music_volume(0.7, 2000)  # Fade in para volume normal
                        # Caso contrário, deixa a música continuar tocando
                        
                    if hasattr(self.game, 'nova'):
                        self.game.nova.show_message(
                            "De volta ao voo orbital! Continue explorando.",
                            "info"
                        )
                    self.last_countdown_number = 0
        except AttributeError:
            # Se algum atributo estiver faltando durante a inicialização, apenas pula a atualização
            pass
                
    def start_quiz(self):
        """Inicia o estado do quiz com uma pergunta aleatória"""
        # Garante que a música atual continue durante o quiz
        # Não precisamos parar nem reiniciar a música
        current_music_was_active = False
        current_music_planet = None
        
        if hasattr(self.game, 'sound_manager'):
            # Armazena o estado atual da música para restaurar se necessário
            current_music_was_active = self.game.sound_manager.music_active
            current_music_planet = self.game.sound_manager.current_music
            current_volume = 0.7
            if pygame.mixer.music.get_busy():
                current_volume = pygame.mixer.music.get_volume()
                # Pode reduzir um pouco o volume durante o quiz (opcional)
                pygame.mixer.music.set_volume(current_volume * 0.8)
            
        self.change_state(config.QUIZ)
        self.last_countdown_number = 2

        try:
            # Certifica-se de que o jogo tem os atributos necessários
            if hasattr(self.game, 'current_planet') and hasattr(self.game, 'quiz'):
                # Seleciona uma pergunta aleatória do quiz para o planeta atual
                import random
                question_data = random.choice(self.game.current_planet.quiz_questions)

                # Inicia o quiz com a pergunta selecionada
                self.game.quiz.start_quiz(
                    question_data["question"],
                    question_data["options"],
                    question_data["answer"],
                    question_data.get("explanation")
                )
                
                # Certifica-se de que a música continue tocando durante o quiz
                if hasattr(self.game, 'sound_manager') and not pygame.mixer.music.get_busy():
                    # A música parou por algum motivo, reinicia
                    if current_music_was_active and current_music_planet:
                        self.game.sound_manager.play_planet_music(current_music_planet)
        except (AttributeError, IndexError) as e:
            # Registra o erro e continua
            print(f"Erro ao iniciar o quiz: {e}")
        
    def start_transition(self):
        """Inicia a transição para o próximo planeta"""
        self.change_state(config.TRANSITION)

        try:
            # Para todos os sons do jogo, mas mantém a música se estivermos no mesmo planeta
            if hasattr(self.game, 'sound_manager'):
                # Paramos apenas os efeitos sonoros
                self.game.sound_manager.stop_all_sounds()
                
                # Só paramos a música se vamos para um novo planeta
                # (quando acertamos o quiz e avançamos)
                if self.game.quiz.is_correct():
                    self.game.sound_manager.stop_music(1000)  # Fade out da música em 1 segundo

            # Incrementa o índice do planeta
            if hasattr(self.game, 'current_planet_index') and hasattr(self.game, 'planets'):
                self.game.current_planet_index += 1

                # Verifica se chegamos ao fim de todos os planetas
                if self.game.current_planet_index >= len(self.game.planets):
                    self.change_state(config.GAME_OVER)
                    if hasattr(self.game, 'sound_manager'):
                        self.game.sound_manager.play_explosion()

                    # Atualiza o high score, se necessário
                    if hasattr(self.game, 'score') and hasattr(self.game, 'high_score_manager'):
                        if self.game.score > self.game.high_score_manager.get():
                            self.game.high_score = self.game.score
                            self.game.high_score_manager.save(self.game.score)
                    return

                # Atualiza o planeta atual
                self.game.current_planet = self.game.planets[self.game.current_planet_index]

                # Toca o som de boas-vindas para o novo planeta
                from src.planet_data import PLANET_NAME_PT
                planet_name_en = self.game.current_planet.name
                planet_name_pt = PLANET_NAME_PT.get(planet_name_en, planet_name_en)

                # Toca o som de boas-vindas e define o temporizador
                if hasattr(self.game, 'sound_manager'):
                    duration_ms = self.game.sound_manager.play_welcome(planet_name_en)
                    self.welcome_sound_timer = duration_ms
                    if hasattr(self.game, 'nova'):
                        self.game.nova.start_radio_signal(duration_ms)

                # NOVA anuncia o novo planeta
                if hasattr(self.game, 'nova'):
                    self.game.nova.show_message(
                        f"Entrando na órbita de {planet_name_pt}!",
                        "excited"
                    )

        except (AttributeError, IndexError) as e:
            # Registra o erro e continua
            print(f"Erro ao iniciar a transição: {e}")