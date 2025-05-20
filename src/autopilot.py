import random
import src.config as config

class Autopilot:
    """Controlador de autopiloto usando Q-learning simples"""

    def __init__(self, game):
        self.game = game
        self.enabled = False
        self.learning_rate = 0.7
        self.discount = 0.95
        self.epsilon = 0.1
        self.q_table = {}
        self.last_state = None
        self.last_action = 0
        self.prev_score = 0
        self.prev_lives = game.lives

    def toggle(self):
        """Ativa ou desativa o autopiloto"""
        self.enabled = not self.enabled
        if self.enabled:
            self.game.nova.show_message("Autopiloto ativado!", "excited")
        else:
            self.game.nova.show_message("Autopiloto desativado.", "normal")

    def _discretize(self, value, bins, min_value, max_value):
        """Converte valores contínuos para índices discretos"""
        if value < min_value:
            value = min_value
        if value > max_value:
            value = max_value
        scaled = (value - min_value) / (max_value - min_value)
        return int(scaled * (bins - 1))

    def _get_state(self):
        """Extrai o estado atual em forma discretizada"""
        ship = self.game.spacecraft
        obstacles = self.game.obstacles

        if obstacles:
            next_obstacle = min(obstacles, key=lambda o: o.x)
            gap_y = next_obstacle.gap_y
            dist = next_obstacle.x - ship.x
        else:
            gap_y = config.SCREEN_HEIGHT / 2
            dist = config.SCREEN_WIDTH

        y_bin = self._discretize(ship.y, 10, 0, config.SCREEN_HEIGHT)
        vel_bin = self._discretize(ship.velocity, 10, -10, 10)
        dist_bin = self._discretize(dist, 10, -config.SCREEN_WIDTH, config.SCREEN_WIDTH)
        gap_bin = self._discretize(gap_y - ship.y, 10, -config.SCREEN_HEIGHT, config.SCREEN_HEIGHT)

        return (y_bin, vel_bin, dist_bin, gap_bin)

    def _q_values(self, state):
        """Obtém os valores Q para um estado"""
        return self.q_table.setdefault(state, [0.0, 0.0])

    def choose_action(self, state):
        """Escolhe a ação baseado em exploração ou na melhor estimativa"""
        if random.random() < self.epsilon:
            return random.randint(0, 1)
        q = self._q_values(state)
        return 1 if q[1] >= q[0] else 0

    def update_q(self, reward, new_state):
        """Atualiza a Q-table"""
        prev_q = self._q_values(self.last_state)
        next_q = self._q_values(new_state)
        best_next = max(next_q)
        prev_q[self.last_action] += self.learning_rate * (
            reward + self.discount * best_next - prev_q[self.last_action]
        )

    def step(self):
        """Executa uma etapa de decisão e aprendizagem"""
        state = self._get_state()
        if self.last_state is None:
            self.last_state = state

        action = self.choose_action(state)
        self.last_action = action
        if action == 1:
            self.game.spacecraft.thrust()
            self.game.sound_manager.play_thrust()

        reward = 0.1
        if self.game.score > self.prev_score:
            reward += 1.0
            self.prev_score = self.game.score
        if self.game.lives < self.prev_lives:
            reward -= 5.0
            self.prev_lives = self.game.lives

        new_state = self._get_state()
        self.update_q(reward, new_state)
        self.last_state = new_state
