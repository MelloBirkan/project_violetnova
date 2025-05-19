import random
import pygame
from src.obstacle import Obstacle
from src.collectible import Collectible
import src.config as config
from src.planet_data import LEVEL_PROGRESSION_THRESHOLDS, PLANET_NAME_PT

class GameMechanics:
    def __init__(self, game):
        self.game = game
        
    def update(self):
        """Atualiza as mecânicas do jogo, obstáculos e colecionáveis"""
        if self.game.state != config.PLAYING:
            return
            
        # Atualiza a nave com a gravidade do planeta e limites de tela
        self.game.spacecraft.update(self.game.current_planet.gravity, config.SCREEN_HEIGHT, config.FLOOR_HEIGHT)
        
        # Impulso contínuo quando espaço é mantido pressionado
        if self.game.control_mode == config.CONTROL_MODE_HOLD and self.game.space_held:
            # Aplica pequeno impulso contínuo (20% da força)
            cont = self.game.spacecraft.thrust_power * self.game.spacecraft.thrust_multiplier * 0.2
            self.game.spacecraft.velocity -= cont
            # Mantém o efeito da chama
            self.game.spacecraft.last_thrust_time = pygame.time.get_ticks()
            # Garante que o som do motor continue tocando
            if not pygame.mixer.get_busy() or not self.game.sound_manager.engine_thrust_sound.get_num_channels():
                self.game.sound_manager.play_thrust()
                
        # Gerencia a música de fundo com base na pontuação
        if self.game.sound_manager.music_active and self.game.score >= 2:
            self.game.sound_manager.increase_music_volume_on_progress(self.game.score)
                
        # Gera obstáculos
        current_time = pygame.time.get_ticks()
        if current_time - self.game.last_obstacle_time > self.game.obstacle_spawn_rate:
            self.generate_obstacle()
            self.game.last_obstacle_time = current_time
            
        # Gera colecionáveis
        current_time = pygame.time.get_ticks()
        if current_time - self.game.last_collectible_time > self.game.collectible_spawn_rate:
            self.generate_collectible()
            self.game.last_collectible_time = current_time
            
        # Atualiza obstáculos e verifica pontuação
        for obstacle in self.game.obstacles:
            obstacle.update()
            
            # Pontua ao passar por um obstáculo
            if not obstacle.scored and obstacle.x + obstacle.WIDTH < self.game.spacecraft.x:
                self.game.score += 1
                obstacle.scored = True
                
                # Verifica progressão
                self.check_progression()
                
        # Verifica colisões com colecionáveis
        self.game.collision_manager.check_collectible_collisions()
        
        # Atualiza colecionáveis
        for collectible in list(self.game.collectibles):
            collectible.update()
            collectible.x -= self.game.obstacle_speed  # Move na mesma velocidade dos obstáculos
            
        # Remove obstáculos e itens fora da tela
        self.game.obstacles = [obs for obs in self.game.obstacles if obs.x > -obs.WIDTH]
        self.game.collectibles = [col for col in self.game.collectibles if col.x > -col.WIDTH]
        
        # Verifica colisões
        collision_result = self.game.collision_manager.check_collisions()
        if collision_result is not False:
            # Reproduz som de colisão
            self.game.sound_manager.play_collision()
            
        # Move the floor
        self.game.floor_x = (self.game.floor_x - self.game.obstacle_speed) % 800
            
    def generate_obstacle(self):
        """Gera um novo obstáculo"""
        # Define o espaçamento fixo entre obstáculos
        gap_size = Obstacle.GAP
        
        # Calcula valores mínimo e máximo para o centro do vão
        min_gap_center_y = gap_size // 2
        max_gap_center_y = config.SCREEN_HEIGHT - config.FLOOR_HEIGHT - (gap_size // 2)
        
        # Trata casos extremos com valores extremos
        if min_gap_center_y > max_gap_center_y:
            target_y = ((gap_size // 2) + (config.SCREEN_HEIGHT - config.FLOOR_HEIGHT - (gap_size // 2))) // 2
            
            # Define limites absolutos para correção
            abs_min_y = gap_size // 2
            abs_max_y = config.SCREEN_HEIGHT - config.FLOOR_HEIGHT - (gap_size // 2)
            
            if abs_min_y > abs_max_y:  # Ex.: gap_size > altura jogável
                # Usa o meio da área jogável
                target_y = (config.SCREEN_HEIGHT - config.FLOOR_HEIGHT) // 2
            else:
                # Corrige target_y para um valor fisicamente possível
                target_y = max(abs_min_y, min(target_y, abs_max_y))
                
            min_gap_center_y = target_y
            max_gap_center_y = target_y
            
        # Gera posição aleatória para o centro do vão
        gap_y = random.randint(min_gap_center_y, max_gap_center_y)
        
        # Seleciona aleatoriamente o tipo de obstáculo
        obstacle_type = random.choice(list(Obstacle.TYPES.keys()))
        
        # Obtém o nome do planeta atual
        current_planet_name = self.game.current_planet.name
        
        # Cria novo obstáculo com o nome do planeta
        new_obstacle = Obstacle(
            config.SCREEN_WIDTH, 
            gap_y, 
            self.game.obstacle_speed, 
            obstacle_type, 
            config.SCREEN_HEIGHT,
            current_planet_name
        )
        self.game.obstacles.append(new_obstacle)
        
        # Ocasionalmente a NOVA pode alertar sobre obstáculos
        if random.random() < 0.3:  # 30% de chance
            pass  # Placeholder para alertas futuros da NOVA
            
    def generate_collectible(self):
        """Gera um novo colecionável"""
        settings = config.DIFFICULTY_SETTINGS[self.game.difficulty]

        # Se não houver colecionáveis nesta dificuldade, sai
        if settings["life_collectible_chance"] == 0 and settings["weapon_collectible_chance"] == 0:
            return

        x = config.SCREEN_WIDTH
        y = random.randint(100, config.SCREEN_HEIGHT - config.FLOOR_HEIGHT - 50)

        rand_val = random.random()
        collectible_type = "data"
        life_chance = settings["life_collectible_chance"]
        weapon_chance = settings["weapon_collectible_chance"]

        if rand_val < life_chance:
            collectible_type = "life"
        elif rand_val < life_chance + weapon_chance and not self.game.weapon_active:
            collectible_type = "weapon"
            
        quiz_idx = None
        if collectible_type == "data":
            quiz_idx = random.randrange(len(self.game.current_planet.quiz_questions))

        self.game.collectibles.append(Collectible(x, y, collectible_type, quiz_idx))
        
    def check_progression(self):
        """Verifica se o jogador cumpriu os requisitos para avançar"""
        # Obtém o limite para o planeta atual
        current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
            self.game.current_planet.name,
            10  # Limite padrão
        )
        
        # Verifica se a pontuação atingiu o limite para avançar automaticamente
        if (self.game.score >= current_threshold and 
            self.game.current_planet_index < len(self.game.planets) - 1):
            
            # NOVA anuncia a progressão automática
            next_planet_en = self.game.planets[self.game.current_planet_index + 1].name
            next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
            self.game.nova.show_message(f"Navegação automática engajada! Indo para {next_planet_pt}!", "excited")
            
            # Atualiza o planeta mais distante alcançado
            next_planet = self.game.planets[self.game.current_planet_index + 1].name.lower()
            current_planet = self.game.current_planet.name.lower()
            self.game.furthest_planet_index = max(self.game.furthest_planet_index, self.game.current_planet_index + 1)
            
            # Salva o planeta atual e atualiza o mais distante, respeitando checkpoints
            self.game.planet_tracker.save(
                current_planet,  # Salva o planeta ATUAL, não o próximo
                update_furthest=True,
                allow_save=config.DIFFICULTY_SETTINGS[self.game.difficulty]["save_checkpoint"],
            )
            
            # Fade out da música antes de mudar de planeta
            self.game.sound_manager.stop_music(1000)
            
            # Inicia o quiz antes de incrementar o índice de planeta
            self.game.state_manager.start_quiz()
            
    def handle_collectible_effect(self, collectible):
        """Aplica o efeito de um item coletado"""
        if collectible.type == "data":
            self.game.score += 1
            self.game.nova.show_message("Dados coletados! +1 ponto", "normal")
            
        elif collectible.type == "life":
            if self.game.add_life():
                self.game.nova.show_message("Vida extra obtida!", "excited")
            else:
                self.game.nova.show_message("Já está com o máximo de vidas!", "normal")
                self.game.score += 2  # Pontos extras em vez de vida
                
        elif collectible.type == "weapon":
            self.game.weapon_system.activate()