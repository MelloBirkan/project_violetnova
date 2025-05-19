import os
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import pygame
from collections import deque, namedtuple

# Define a namedtuple to store experience replay memories
Experience = namedtuple('Experience', ('state', 'action', 'next_state', 'reward', 'done'))

class DQN(nn.Module):
    """
    Deep Q-Network para controlar a espaçonave.
    """
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        
        # Rede neural com camadas ocultas
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_size)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

class ReplayMemory:
    """
    Memória de Experiência para armazenar e amostrar transições passadas.
    """
    def __init__(self, capacity=10000):
        self.memory = deque(maxlen=capacity)
        
    def push(self, *args):
        """Salva uma transição."""
        self.memory.append(Experience(*args))
        
    def sample(self, batch_size):
        """Amostra aleatoriamente um batch de transições."""
        return random.sample(self.memory, batch_size)
    
    def __len__(self):
        return len(self.memory)

class SpacecraftAI:
    """
    Classe principal de IA para controlar a espaçonave usando Deep Q-Learning.
    """
    def __init__(self, state_size=6, action_size=2, planet_name="Earth", device="cpu"):
        self.state_size = state_size  # Tamanho do estado (características observáveis)
        self.action_size = action_size  # Tamanho da ação (thrust ou não thrust)
        self.planet_name = planet_name  # Nome do planeta atual
        self.device = device  # Dispositivo de computação (CPU ou GPU)
        
        # Parâmetros do modelo
        self.gamma = 0.99  # Fator de desconto
        self.epsilon = 1.0  # Taxa de exploração inicial
        self.epsilon_min = 0.01  # Taxa mínima de exploração
        self.epsilon_decay = 0.995  # Taxa de decaimento da exploração
        self.learning_rate = 0.001  # Taxa de aprendizado
        self.batch_size = 64  # Tamanho do lote para treinamento
        
        # Cria modelos de rede neural (modelo principal e modelo alvo)
        self.model = DQN(state_size, action_size).to(self.device)
        self.target_model = DQN(state_size, action_size).to(self.device)
        
        # Atualiza o modelo alvo para corresponder ao modelo principal
        self.update_target_model()
        
        # Otimizador
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        # Memória de replay
        self.memory = ReplayMemory()
        
        # Estatísticas de aprendizado
        self.losses = []
        self.rewards = []
        
        # Contadores para atualizações periódicas
        self.update_counter = 0
        self.target_update_freq = 100  # Frequência de atualização do modelo alvo
        
        # Diretório para salvar modelos
        self.model_dir = os.path.join("models")
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Indicador da atividade da IA
        self.active = False
        
    def update_target_model(self):
        """Copia os pesos do modelo principal para o modelo alvo."""
        self.target_model.load_state_dict(self.model.state_dict())
        
    def get_state(self, game):
        """
        Extrair e normalizar o estado do jogo.
        
        Estado inclui:
        - Posição Y normalizada da espaçonave
        - Velocidade normalizada da espaçonave
        - Posição X normalizada do próximo obstáculo
        - Posição do vão central do próximo obstáculo
        - Fator de gravidade do planeta normalizado
        - Distância normalizada até o próximo obstáculo
        """
        import src.config as config  # Importa o módulo de configuração diretamente
        
        # Valores padrão para quando não há obstáculos
        next_obstacle_x = 1.0
        next_obstacle_gap_y = 0.5
        distance_to_obstacle = 1.0
        
        # Encontra o próximo obstáculo (o primeiro que ainda não foi passado)
        next_obstacle = None
        for obstacle in game.obstacles:
            if obstacle.x + obstacle.WIDTH > game.spacecraft.x:
                next_obstacle = obstacle
                break
                
        if next_obstacle:
            # Normaliza valores entre 0 e 1
            next_obstacle_x = next_obstacle.x / config.SCREEN_WIDTH
            next_obstacle_gap_y = next_obstacle.gap_y / config.SCREEN_HEIGHT
            
            # Calcula a distância normalizada até o próximo obstáculo
            distance_to_obstacle = (next_obstacle.x - game.spacecraft.x) / config.SCREEN_WIDTH
            distance_to_obstacle = max(0.0, min(1.0, distance_to_obstacle))
        
        # Extrai e normaliza os dados da espaçonave
        spacecraft_y = game.spacecraft.y / config.SCREEN_HEIGHT
        spacecraft_velocity = (game.spacecraft.velocity + 20) / 40  # Normaliza velocidade de aproximadamente -20 a 20
        
        # Normaliza o fator de gravidade (normalmente entre 0.1 e 2.0)
        gravity_factor = game.current_planet.gravity_factor / 200
        
        # Combina todos os elementos de estado
        state = np.array([
            spacecraft_y,
            spacecraft_velocity,
            next_obstacle_x,
            next_obstacle_gap_y,
            gravity_factor,
            distance_to_obstacle
        ], dtype=np.float32)
        
        return torch.FloatTensor(state).unsqueeze(0).to(self.device)
    
    def act(self, state, training=True):
        """
        Seleciona uma ação (thrust ou não thrust) com base no estado atual.
        
        Args:
            state: Tensor que representa o estado atual
            training: Se o modelo está em modo de treinamento (com exploração) ou não
            
        Returns:
            int: 0 para não fazer thrust, 1 para fazer thrust
        """
        if training and random.random() < self.epsilon:
            # Exploração: escolhe uma ação aleatória
            return random.randint(0, self.action_size - 1)
        else:
            # Exploitation: escolhe a melhor ação de acordo com o modelo
            with torch.no_grad():
                q_values = self.model(state)
                return q_values.max(1)[1].item()
    
    def train(self, batch_size=None):
        """
        Treina o modelo usando experiências passadas da memória de replay.
        
        Args:
            batch_size: Tamanho do lote para treinar (usa o padrão se não especificado)
        """
        if batch_size is None:
            batch_size = self.batch_size
            
        # Verificar se há memória suficiente para treinar
        if len(self.memory) < batch_size:
            return
            
        # Amostrar um batch de experiências
        experiences = self.memory.sample(batch_size)
        
        # Preparar os tensores de batch
        states = torch.cat([exp.state for exp in experiences])
        actions = torch.tensor([exp.action for exp in experiences], 
                              dtype=torch.long, device=self.device).unsqueeze(1)
        next_states = torch.cat([exp.next_state for exp in experiences])
        rewards = torch.tensor([exp.reward for exp in experiences], 
                              dtype=torch.float, device=self.device).unsqueeze(1)
        dones = torch.tensor([exp.done for exp in experiences], 
                             dtype=torch.float, device=self.device).unsqueeze(1)
        
        # Calcular os valores Q para o estado atual usando o modelo principal
        current_q_values = self.model(states).gather(1, actions)
        
        # Calcular os valores Q para o próximo estado usando o modelo alvo
        with torch.no_grad():
            next_q_values = self.target_model(next_states).max(1)[0].unsqueeze(1)
            target_q_values = rewards + (self.gamma * next_q_values * (1 - dones))
            
        # Calcular a perda e atualizar o modelo
        loss = F.smooth_l1_loss(current_q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        # Clipping gradients para estabilidade
        for param in self.model.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()
        
        # Registrar a perda
        self.losses.append(loss.item())
        
        # Atualizar o modelo alvo periodicamente
        self.update_counter += 1
        if self.update_counter % self.target_update_freq == 0:
            self.update_target_model()
            
        # Decair epsilon para reduzir a exploração com o tempo
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def remember(self, state, action, next_state, reward, done):
        """
        Armazena uma transição na memória de replay.
        
        Args:
            state: Estado atual
            action: Ação tomada
            next_state: Próximo estado
            reward: Recompensa recebida
            done: Se o episódio terminou
        """
        self.memory.push(state, action, next_state, reward, done)
        
    def toggle(self):
        """
        Ativa ou desativa o modo autopilot.
        """
        self.active = not self.active
        return self.active
    
    def calculate_reward(self, game, prev_score):
        """
        Calcula a recompensa com base nos eventos do jogo.
        
        Args:
            game: Objeto do jogo
            prev_score: Pontuação anterior para comparação
            
        Returns:
            float: Recompensa calculada
        """
        import src.config as config  # Importa o módulo de configuração diretamente
        
        reward = 0.0
        
        # Recompensa por sobrevivência
        reward += 0.1
        
        # Recompensa por ganhar pontos
        if game.score > prev_score:
            reward += 10.0 * (game.score - prev_score)
            
        # Penalidade por se aproximar muito do chão ou teto
        near_floor = game.spacecraft.y > (config.SCREEN_HEIGHT - config.FLOOR_HEIGHT - 50)
        near_ceiling = game.spacecraft.y < 30
        if near_floor or near_ceiling:
            reward -= 2.0
            
        # Grande penalidade por colidir
        collision = False
        for obstacle in game.obstacles:
            if (game.spacecraft.x < obstacle.x + obstacle.WIDTH and
                game.spacecraft.x + game.spacecraft.HITBOX_WIDTH > obstacle.x):
                # Verificar colisão vertical
                if (game.spacecraft.y < obstacle.gap_y - obstacle.GAP // 2 or
                    game.spacecraft.y + game.spacecraft.HITBOX_HEIGHT > obstacle.gap_y + obstacle.GAP // 2):
                    collision = True
                    break
                    
        if collision:
            reward -= 100.0
            
        # Recompensa por passar pelo meio de um obstáculo
        for obstacle in game.obstacles:
            if (not obstacle.scored and 
                game.spacecraft.x > obstacle.x + obstacle.WIDTH):
                # Cálculo da distância ao centro do vão
                distance_to_center = abs(game.spacecraft.y - obstacle.gap_y)
                position_factor = 1.0 - min(1.0, distance_to_center / (obstacle.GAP / 2))
                
                # Recompensa maior por passar pelo centro do vão
                reward += 5.0 * position_factor
                
        return reward
    
    def save_model(self, score):
        """
        Salva o modelo atual com o nome do planeta e a pontuação.
        
        Args:
            score: Pontuação atual para nomear o arquivo
        """
        planet_name = self.planet_name.lower()
        model_path = os.path.join(self.model_dir, f"{planet_name}_dqn_{int(score)}.pth")
        
        # Salva apenas o estado do dicionário, não o modelo inteiro
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'planet': planet_name,
            'score': score
        }, model_path)
        
        print(f"Modelo salvo em: {model_path}")
    
    def load_model(self, path=None):
        """
        Carrega um modelo salvo.
        
        Args:
            path: Caminho para o arquivo do modelo. Se não for especificado,
                 carrega o melhor modelo para o planeta atual.
        """
        if path is None:
            # Procura pelo melhor modelo para este planeta
            planet_name = self.planet_name.lower()
            model_files = [f for f in os.listdir(self.model_dir) 
                           if f.startswith(f"{planet_name}_dqn_")]
            
            if not model_files:
                print(f"Nenhum modelo encontrado para {self.planet_name}")
                return False
                
            # Ordena por pontuação (parte do nome do arquivo)
            model_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]), reverse=True)
            path = os.path.join(self.model_dir, model_files[0])
        
        # Verifica se o arquivo existe
        if not os.path.exists(path):
            print(f"Arquivo de modelo não encontrado: {path}")
            return False
        
        try:
            # Carrega o modelo
            checkpoint = torch.load(path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.epsilon = checkpoint['epsilon']
            
            # Atualiza o modelo alvo para corresponder ao modelo principal
            self.update_target_model()
            
            print(f"Modelo carregado de: {path}")
            return True
        except Exception as e:
            print(f"Erro ao carregar o modelo: {e}")
            return False
            
    def update_planet(self, planet_name):
        """
        Atualiza o planeta atual e carrega o modelo apropriado se disponível.
        
        Args:
            planet_name: Nome do novo planeta
        """
        if self.planet_name != planet_name:
            self.planet_name = planet_name
            
            # Tenta carregar um modelo para o novo planeta
            loaded = self.load_model()
            
            # Se não conseguir carregar um modelo, reinicia com parâmetros padrão
            if not loaded:
                print(f"Iniciando novo modelo para {planet_name}")
                self.epsilon = 1.0  # Reinicia a exploração
                
                # Reinicia os modelos
                self.model = DQN(self.state_size, self.action_size).to(self.device)
                self.target_model = DQN(self.state_size, self.action_size).to(self.device)
                self.update_target_model()
                
                # Reinicia o otimizador
                self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

# Classe para gerenciar o treinamento acelerado
class AcceleratedTraining:
    """
    Implementa um modo de treinamento acelerado para a IA da espaçonave.
    """
    def __init__(self, game, ai, iterations=1000, render_frequency=100):
        self.game = game
        self.ai = ai
        self.iterations = iterations
        self.render_frequency = render_frequency
        self.current_iteration = 0
        self.scores = []
        self.best_score = 0
        
    def start(self):
        """
        Inicia o treinamento acelerado.
        """
        print(f"Iniciando treinamento acelerado para {self.ai.planet_name}...")
        
        # Ativa o modo de treinamento
        self.ai.active = True
        orig_speed = self.game.obstacle_speed
        
        # Aumenta a velocidade para treinamento mais rápido
        self.game.obstacle_speed *= 1.5
        
        try:
            for i in range(self.iterations):
                self.current_iteration = i
                done = self.train_episode()
                
                # Registra a pontuação
                score = self.game.score
                self.scores.append(score)
                
                # Salva o modelo se for o melhor até agora
                if score > self.best_score:
                    self.best_score = score
                    self.ai.save_model(score)
                
                # Exibe o progresso periodicamente
                if i % 20 == 0 or done:
                    avg_score = sum(self.scores[-20:]) / min(20, len(self.scores))
                    print(f"Iteração {i}/{self.iterations} | "
                          f"Pontuação: {score} | Média: {avg_score:.2f} | "
                          f"Epsilon: {self.ai.epsilon:.4f}")
                
                # Reinicia o jogo para o próximo episódio
                self.game.reset()
                
        finally:
            # Restaura a velocidade original
            self.game.obstacle_speed = orig_speed
            
            # Desativa o modo de treinamento
            self.ai.active = False
            print("Treinamento acelerado concluído.")
            
    def train_episode(self):
        """
        Treina um único episódio até uma colisão ou pontuação alta.
        
        Returns:
            bool: True se o episódio terminou por colisão, False se terminou por pontuação
        """
        import src.config as config  # Importa o módulo de configuração diretamente
        
        # Reinicia o estado
        state = self.ai.get_state(self.game)
        prev_score = 0
        render = (self.current_iteration % self.render_frequency == 0)
        
        # Executa o episódio por até 2000 passos
        for step in range(2000):
            # Escolhe e executa uma ação
            action = self.ai.act(state, training=True)
            
            if action == 1:  # Thrust
                self.game.spacecraft.thrust()
            
            # Atualiza o jogo
            self.game.update()
            
            # Captura o próximo estado
            next_state = self.ai.get_state(self.game)
            
            # Calcular recompensa
            reward = self.ai.calculate_reward(self.game, prev_score)
            
            # Verifica se o episódio terminou
            done = False
            if self.game.state == config.GAME_OVER:
                done = True
                reward = -100  # Penalidade adicional por perder
            
            # Armazena a experiência
            self.ai.remember(state, action, next_state, reward, done)
            
            # Treina o modelo
            self.ai.train()
            
            # Renderiza o jogo periodicamente se solicitado
            if render and step % 5 == 0:
                self.game.draw()
                pygame.display.flip()
                pygame.time.delay(10)  # Pequeno atraso para visualização
            
            # Atualiza o estado para o próximo passo
            state = next_state
            prev_score = self.game.score
            
            # Encerra o episódio se terminou
            if done:
                return True
                
            # Encerra o episódio se atingiu uma pontuação suficiente
            if self.game.score >= 25:  # Pontuação limite para episódio
                return False
                
        return False  # Tempo limite atingido