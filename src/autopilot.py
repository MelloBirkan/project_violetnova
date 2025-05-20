import numpy as np
import random
import pygame
import src.config as config

class QLearningAutopilot:
    """
    Implementa um piloto automático baseado em Q-Learning para a espaçonave.
    O agente aprende a jogar observando a posição da espaçonave, a posição dos obstáculos,
    e recebe recompensas/punições com base em seu desempenho.
    """
    
    def __init__(self, game):
        """
        Inicializa o piloto automático com o ambiente do jogo.
        """
        self.game = game
        
        # Hiperparâmetros do Q-learning
        self.learning_rate = 0.2  # Taxa de aprendizado (alpha) - aumentada para aprender mais rápido
        self.discount_factor = 0.95  # Fator de desconto (gamma) - reduzido para focar mais em recompensas imediatas
        self.exploration_rate = 1.0  # Taxa de exploração inicial (epsilon)
        self.exploration_min = 0.05  # Taxa mínima de exploração - aumentada para manter alguma exploração
        self.exploration_decay = 0.99  # Decaimento da taxa de exploração - mais lento para manter exploração por mais tempo
        
        # Discretização do espaço de estados
        self.y_bins = 10  # Número de bins para a posição vertical da nave
        self.velocity_bins = 5  # Número de bins para a velocidade da nave
        self.obstacle_dist_bins = 5  # Número de bins para a distância do obstáculo
        self.obstacle_height_bins = 5  # Número de bins para a altura do obstáculo
        
        # Ações possíveis: [0: não impulsionar, 1: impulsionar]
        self.actions = [0, 1]
        
        # Inicializa a tabela Q
        self._init_q_table()
        
        # Estado anterior e ação para aprendizado
        self.last_state = None
        self.last_action = None
        
        # Estatísticas de aprendizado
        self.episodes = 0
        self.steps = 0
        self.total_reward = 0
        self.lives_lost = 0
        
        # Controle de tempo para não tomar decisões a cada frame
        self.last_decision_time = 0
        self.decision_interval = 100  # ms entre decisões
        
        # Flags para quiz e outras interações
        self.in_quiz = False
        self.waiting_to_restart = False
        
        # Controle de log para evitar spam no console
        self.log_throttle = {}
        self.log_interval = 5000  # ms entre mensagens idênticas (5 segundos)
        
        print("Autopilot: Inicializado e pronto para aprender")
        
    def _init_q_table(self):
        """
        Inicializa a tabela Q com valores aleatórios pequenos.
        A tabela possui dimensões baseadas na discretização do espaço de estados.
        """
        table_shape = (
            self.y_bins,             # Posição vertical da nave
            self.velocity_bins,      # Velocidade vertical
            self.obstacle_dist_bins, # Distância do próximo obstáculo
            self.obstacle_height_bins,# Altura do próximo obstáculo
            len(self.actions)        # Ações possíveis
        )
        
        # Inicializa com pequenos valores aleatórios para encorajar exploração inicial
        self.q_table = np.random.uniform(low=0, high=0.1, size=table_shape)
        
    def discretize_state(self):
        """
        Converte o estado contínuo do jogo em um estado discreto para a tabela Q.
        """
        try:
            # Obtém valores do estado atual com verificação de segurança
            if not hasattr(self.game, 'spacecraft'):
                # Estado padrão se não houver nave (pode acontecer durante transições)
                return (self.y_bins // 2, self.velocity_bins // 2, 
                       self.obstacle_dist_bins - 1, self.obstacle_height_bins // 2)
                
            spacecraft = self.game.spacecraft
            y_position = spacecraft.y / config.SCREEN_HEIGHT  # Normalizado [0, 1]
            velocity = spacecraft.velocity / 10.0  # Normalizado aproximadamente [-1, 1]
            
            # Obtém informações do próximo obstáculo (se existir)
            next_obstacle_dist = 1.0  # Se não houver obstáculo, assume distância máxima
            next_obstacle_height = 0.5  # Valor intermediário padrão
            
            if hasattr(self.game, 'obstacles') and self.game.obstacles and len(self.game.obstacles) > 0:
                try:
                    # Encontra o próximo obstáculo (o mais próximo à direita da nave)
                    next_obstacles = [obs for obs in self.game.obstacles if obs.x > spacecraft.x]
                    if next_obstacles:
                        closest = min(next_obstacles, key=lambda obs: obs.x)
                        next_obstacle_dist = (closest.x - spacecraft.x) / config.SCREEN_WIDTH  # Normalizado [0, 1]
                        
                        # Usa gap_y ao invés de y pois o obstáculo tem dois componentes (superior e inferior)
                        # gap_y é a posição vertical do meio do espaço entre os obstáculos
                        if hasattr(closest, 'gap_y'):
                            next_obstacle_height = closest.gap_y / config.SCREEN_HEIGHT  # Normalizado [0, 1]
                        else:
                            next_obstacle_height = 0.5  # Valor padrão se gap_y não estiver disponível
                except Exception as e:
                    print(f"Erro ao processar obstáculo: {str(e)}")
                    next_obstacle_dist = 1.0
                    next_obstacle_height = 0.5
            
            # Discretiza os valores em bins
            y_bin = min(self.y_bins - 1, max(0, int(y_position * self.y_bins)))
            velocity_bin = min(self.velocity_bins - 1, max(0, int((velocity + 1) / 2 * self.velocity_bins)))
            obstacle_dist_bin = min(self.obstacle_dist_bins - 1, max(0, int(next_obstacle_dist * self.obstacle_dist_bins)))
            obstacle_height_bin = min(self.obstacle_height_bins - 1, max(0, int(next_obstacle_height * self.obstacle_height_bins)))
            
            return (y_bin, velocity_bin, obstacle_dist_bin, obstacle_height_bin)
        except Exception as e:
            # Em caso de erro, retorna um estado padrão
            error_message = f"Erro ao discretizar estado: {e}"
            
            # Controle de log para evitar spam no console
            current_time = pygame.time.get_ticks()
            last_log_time = self.log_throttle.get(error_message, 0)
            
            if current_time - last_log_time > self.log_interval:
                print(error_message)
                self.log_throttle[error_message] = current_time
                
            return (self.y_bins // 2, self.velocity_bins // 2, 
                   self.obstacle_dist_bins - 1, self.obstacle_height_bins // 2)
    
    def select_action(self):
        """
        Seleciona uma ação usando a política epsilon-greedy.
        """
        # Explora com probabilidade epsilon
        if random.random() < self.exploration_rate:
            return random.choice(self.actions)
        
        # Explora os valores Q para o estado atual
        current_state = self.discretize_state()
        return np.argmax(self.q_table[current_state])
    
    def update_q_table(self, state, action, reward, next_state):
        """
        Atualiza a tabela Q usando a fórmula do Q-learning.
        Q(s,a) = Q(s,a) + α * [R + γ * max(Q(s',a')) - Q(s,a)]
        """
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error
        
    def calculate_reward(self):
        """
        Calcula a recompensa com base no estado atual do jogo.
        """
        try:
            reward = 0.1  # Pequena recompensa por sobreviver
            
            # Verifica se temos acesso aos atributos necessários
            if not hasattr(self.game, 'lives') or not hasattr(self.game, 'spacecraft'):
                return reward
            
            # Punição por colisão (perda de vida)
            if not hasattr(self, 'lives_lost'):
                self.lives_lost = self.game.lives
            
            if self.lives_lost > self.game.lives:
                reward -= 20.0  # Punição mais severa por perder vidas
                print(f"Autopilot: Perdeu vida! Recompensa negativa: {reward}")
                self.lives_lost = self.game.lives
            
            # Recompensa por pontuação
            if hasattr(self.game, 'score'):
                current_score = self.game.score
                if hasattr(self, 'last_score'):
                    score_diff = current_score - self.last_score
                    if score_diff > 0:
                        reward += score_diff * 1.0  # Recompensa maior por pontuação
                        # Log de pontuação apenas ocasionalmente
                        if score_diff > 0 and random.random() < 0.1:  # 10% de chance de logar
                            print(f"Autopilot: Ganhou pontos! Recompensa: +{score_diff}")
                self.last_score = current_score
            
            # Recompensa/punição por posição inadequada
            # Evitar ficar muito perto do chão ou do teto
            spacecraft = self.game.spacecraft
            screen_height = config.SCREEN_HEIGHT
            floor_height = config.FLOOR_HEIGHT
            
            # Punição por estar muito perto do chão
            ground_limit = screen_height - floor_height - spacecraft.HITBOX_HEIGHT
            if spacecraft.y > ground_limit - 50:
                reward -= 1.0  # Punição maior por estar perto do chão
            elif spacecraft.y > ground_limit - 100:
                reward -= 0.5  # Punição menor por estar moderadamente perto do chão
            
            # Punição por estar muito perto do teto
            if spacecraft.y < 50:
                reward -= 1.0  # Punição maior por estar perto do teto
            elif spacecraft.y < 100:
                reward -= 0.5  # Punição menor por estar moderadamente perto do teto
                
            # Recompensa por estar na região central segura
            safe_center_min = 150
            safe_center_max = ground_limit - 150
            if safe_center_min < spacecraft.y < safe_center_max:
                reward += 0.1  # Pequena recompensa por se manter em zona segura
                
            return reward
        except Exception as e:
            print(f"Erro ao calcular recompensa: {e}")
            return 0.0
    
    def update(self):
        """
        Atualiza o agente de aprendizado, tomando decisões e aprendendo a partir delas.
        Esta função deve ser chamada a cada atualização do jogo.
        """
        # Só toma decisões em intervalos específicos (não a cada frame)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_decision_time < self.decision_interval:
            return
            
        self.last_decision_time = current_time
        
        # Identifica o estado do jogo
        game_state = self.game.state
        
        # Processa o estado atual do jogo
        if game_state == config.MENU:
            # Processo o estado de menu
            self._handle_menu_state()
        elif game_state == config.PLAYING:
            # Funcionamento normal durante o jogo
            self._handle_playing_state()
        elif game_state == config.QUIZ or game_state == config.QUIZ_FAILURE:
            # Processa o estado de quiz
            self._handle_quiz_state()
        elif game_state == config.GAME_OVER:
            # Processa o estado de game over
            self._handle_game_over_state()
        elif game_state == config.TRANSITION:
            # Processa o estado de transição
            self._handle_transition_state()
            
        # Decai a taxa de exploração
        self.exploration_rate = max(self.exploration_min, 
                                   self.exploration_rate * self.exploration_decay)
    
    def _handle_playing_state(self):
        """
        Processa o estado de jogo normal (PLAYING).
        """
        try:
            # Obtém o estado atual discretizado
            current_state = self.discretize_state()
            
            # Seleciona uma ação
            action = self.select_action()
            
            # Executa a ação escolhida
            if action == 1:  # Ação de empuxo
                if hasattr(self.game, 'spacecraft') and self.game.spacecraft:
                    self.game.spacecraft.thrust()
                
            # Calcula a recompensa para esta ação
            reward = self.calculate_reward()
            self.total_reward += reward
            
            # Atualiza a tabela Q se houver um estado e ação anteriores
            if self.last_state is not None and self.last_action is not None:
                self.update_q_table(self.last_state, self.last_action, reward, current_state)
                
            # Armazena o estado e ação atuais para a próxima atualização
            self.last_state = current_state
            self.last_action = action
            
            # Incrementa o contador de passos
            self.steps += 1
        except Exception as e:
            print(f"Erro no estado de jogo: {e}")
    
    def _handle_quiz_state(self):
        """
        Responde a perguntas no estado de quiz.
        Escolhe a resposta correta (trapaceando um pouco para fins de treinamento).
        """
        try:
            if self.game.state == config.QUIZ and not self.in_quiz:
                self.in_quiz = True
                
                # Verifica se o quiz está disponível
                if hasattr(self.game, 'quiz') and hasattr(self.game.quiz, 'correct_answer'):
                    # Obtém a resposta correta do quiz atual
                    correct_answer = self.game.quiz.correct_answer
                    
                    # Simula um atraso antes de responder (reduzido para evitar bloqueio)
                    pygame.time.delay(500)
                    
                    # Seleciona a resposta correta (para fins de treinamento)
                    # Na implementação real, isso poderia ser baseado em aprendizado também
                    # Verifica se a resposta está dentro dos limites válidos (0-3 geralmente)
                    if 0 <= correct_answer <= 3:
                        print(f"Autopilot: Respondendo quiz com opção {correct_answer+1}")
                        event = pygame.event.Event(pygame.KEYDOWN, key=49 + correct_answer)  # Teclas 1-4
                        pygame.event.post(event)
                    else:
                        print(f"Resposta inválida: {correct_answer}")
            
            # Reseta o flag quando o quiz termina
            if self.game.state != config.QUIZ:
                self.in_quiz = False
        except Exception as e:
            print(f"Erro ao processar quiz: {e}")
            self.in_quiz = False
    
    def _handle_game_over_state(self):
        """
        Processa o estado de game over, pressionando espaço para reiniciar.
        """
        try:
            # Limita a frequência de tentativas de reinício
            static_timer = getattr(self, 'restart_timer', 0)
            current_time = pygame.time.get_ticks()
            
            # Finaliza o episódio uma vez
            if not self.waiting_to_restart:
                self.waiting_to_restart = True
                self.episodes += 1
                
                # Registra estatísticas (para visualização ou análise)
                print(f"Episódio {self.episodes} finalizado. "
                     f"Passos: {self.steps}, Recompensa total: {self.total_reward:.2f}")
                
                # Reseta contadores para o próximo episódio
                self.steps = 0
                self.total_reward = 0
                self.last_state = None
                self.last_action = None
                self.restart_timer = current_time
            
            # Tenta reiniciar periodicamente (a cada 2 segundos)
            if current_time - static_timer > 2000:
                self.restart_timer = current_time
                
                # Primeiro clica com o mouse no centro da tela
                screen_center = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
                mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, 
                                              pos=screen_center, 
                                              button=1)
                pygame.event.post(mouse_event)
                
                # Depois pressiona espaço para garantir
                print("Autopilot: Tentando reiniciar após game over")
                space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                pygame.event.post(space_event)
                
                # Força um clique simulado no botão de reinício
                # Usa a função direta do input handler
                if hasattr(self.game, 'input_handler') and hasattr(self.game.input_handler, '_handle_left_click'):
                    print("Autopilot: Chamando handler de clique diretamente")
                    self.game.input_handler._handle_left_click()
            
            # Reseta o flag quando o jogo não está mais em game over
            if self.game.state != config.GAME_OVER:
                print("Autopilot: Saiu do estado game over com sucesso")
                self.waiting_to_restart = False
                self.lives_lost = 0
                
        except Exception as e:
            print(f"Erro ao processar game over: {e}")
            self.waiting_to_restart = False
    
    def _handle_transition_state(self):
        """
        Processa o estado de transição entre planetas.
        """
        try:
            # Verifica se o gerenciador de estados existe e se a transição está em andamento
            if (hasattr(self.game, 'state_manager') and 
                hasattr(self.game.state_manager, 'transition_time')):
                
                # Espera a transição terminar naturalmente ou pressiona espaço para pular
                if self.game.state_manager.transition_time > config.TRANSITION_DURATION // 2:
                    # Pressiona espaço para pular a transição após metade do tempo
                    print("Autopilot: Pulando transição")
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                    pygame.event.post(event)
        except Exception as e:
            print(f"Erro ao processar transição: {e}")
            
    def _handle_menu_state(self):
        """
        Processa o estado de menu, iniciando o jogo.
        """
        try:
            # Limita a frequência com que enviamos eventos para evitar sobrecarregar a fila de eventos
            static_timer = getattr(self, 'menu_timer', 0)
            current_time = pygame.time.get_ticks()
            
            if current_time - static_timer < 1000:  # Espera 1 segundo entre ações de menu
                return
                
            self.menu_timer = current_time
            
            # Seleciona a opção "Jogar" e pressiona Enter/Space
            if hasattr(self.game, 'in_difficulty_menu') and self.game.in_difficulty_menu:
                # Se estiver no menu de dificuldade, confirma a seleção atual
                print("Autopilot: Confirmando seleção de dificuldade")
                event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                pygame.event.post(event)
            else:
                # Seleciona a opção "Jogar" e pressiona Enter
                if hasattr(self.game, 'selected_menu_option'):
                    # Certifica-se de que a opção "Jogar" está selecionada
                    if self.game.selected_menu_option != 0:
                        print("Autopilot: Selecionando opção Jogar")
                        self.game.selected_menu_option = 0  # 0 é a opção "Jogar"
                    
                    # Confirma a seleção
                    print("Autopilot: Iniciando jogo")
                    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                    pygame.event.post(event)
        except Exception as e:
            print(f"Erro ao processar menu: {e}")
    
    def save_model(self, filename="q_model.npy"):
        """
        Salva o modelo Q-learning em um arquivo.
        """
        np.save(filename, self.q_table)
        print(f"Modelo salvo em {filename}")
    
    def load_model(self, filename="q_model.npy"):
        """
        Carrega o modelo Q-learning de um arquivo.
        """
        try:
            self.q_table = np.load(filename)
            print(f"Modelo carregado de {filename}")
            return True
        except:
            print(f"Falha ao carregar o modelo de {filename}")
            return False