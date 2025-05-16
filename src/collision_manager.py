import src.config as config
from src.planet_data import LEVEL_PROGRESSION_THRESHOLDS, PLANET_NAME_PT

class CollisionManager:
    def __init__(self, game):
        self.game = game
        
    def check_collisions(self):
        """Método principal de detecção de colisões"""
        # Pula a detecção de colisão se a nave estiver invulnerável
        if self.game.invulnerable:
            return False
        
        # Verifica colisões com os limites (teto e chão)
        if self._check_boundary_collision():
            return True
        
        # Verifica colisões com obstáculos
        return self._check_obstacle_collisions()
    
    def _check_boundary_collision(self):
        """Verifica se a nave colidiu com os limites da tela"""
        spacecraft = self.game.spacecraft
        
        # Verifica se a nave atingiu o teto ou o chão
        if (spacecraft.y <= 0 or 
            spacecraft.y + spacecraft.HITBOX_HEIGHT >= config.SCREEN_HEIGHT - config.FLOOR_HEIGHT):
            
            return self.handle_collision("boundary")
        
        return False
    
    def _check_obstacle_collisions(self):
        """Verifica se a nave colidiu com algum obstáculo"""
        spacecraft = self.game.spacecraft
        
        # Calcula a posição da hitbox da nave
        spacecraft_body_x = spacecraft.x + spacecraft.flame_extent + (spacecraft.WIDTH - spacecraft.HITBOX_WIDTH) / 2
        spacecraft_body_y = spacecraft.y + (spacecraft.HEIGHT - spacecraft.HITBOX_HEIGHT) / 2
        
        # Verifica cada obstáculo para colisão
        for obstacle in self.game.obstacles:
            # Determina se está usando sprites e obtém a largura
            using_sprites = hasattr(obstacle, 'using_sprites') and obstacle.using_sprites
            obstacle_width = obstacle.top_width if using_sprites else obstacle.WIDTH
            
            # Verifica sobreposição horizontal
            horizontal_overlap = (
                spacecraft_body_x + spacecraft.HITBOX_WIDTH > obstacle.x and
                spacecraft_body_x < obstacle.x + obstacle_width
            )
            
            if horizontal_overlap:
                # Calcula os limites do gap
                upper_gap_limit = obstacle.gap_y - obstacle.GAP // 2
                lower_gap_limit = obstacle.gap_y + obstacle.GAP // 2
                
                # Verifica colisão com o obstáculo superior
                if spacecraft_body_y < upper_gap_limit:
                    return self.handle_collision("obstacle", obstacle, "upper")
                
                # Verifica colisão com o obstáculo inferior
                if spacecraft_body_y + spacecraft.HITBOX_HEIGHT > lower_gap_limit:
                    return self.handle_collision("obstacle", obstacle, "lower")
        
        return False
    
    def handle_collision(self, collision_type, obstacle=None, obstacle_part=None):
        """Lida com os efeitos e consequências da colisão"""
        # Reduz vidas e verifica se o jogo acabou
        has_lives_left = self.game.lose_life()
        
        # Aplica o knockback apropriado com base no tipo de colisão
        if collision_type == "boundary":
            self._handle_boundary_collision()
        else:
            self._handle_obstacle_collision(obstacle, obstacle_part)
        
        # Define invulnerabilidade
        self.game.invulnerable = True
        self.game.invulnerable_timer = config.SPACECRAFT_INVULNERABILITY_TIME
        
        # Efeitos visuais
        self.game.screen_shake = 18
        self.game.flash_effect = 5
        
        # Notificação da IA NOVA
        self.game.nova.show_message("Integridade do casco comprometida!", "alerta")
        
        # Retorna se ainda tem vidas
        return has_lives_left
    
    def _handle_boundary_collision(self):
        """Lida com a colisão com os limites da tela"""
        spacecraft = self.game.spacecraft
        
        # Se colidir com o chão
        if spacecraft.y + spacecraft.HITBOX_HEIGHT >= config.SCREEN_HEIGHT - config.FLOOR_HEIGHT:
            # Aplica knockback para cima
            spacecraft.velocity = config.SPACECRAFT_KNOCKBACK * 0.8
            # Garante que a nave não vá abaixo do chão
            spacecraft.y = config.SCREEN_HEIGHT - config.FLOOR_HEIGHT - spacecraft.HITBOX_HEIGHT
        else:
            # Se colidir com o teto, aplica knockback para baixo
            spacecraft.velocity = abs(config.SPACECRAFT_KNOCKBACK) * 0.8
            # Garante que a nave não vá acima do teto
            spacecraft.y = 0
    
    def _handle_obstacle_collision(self, obstacle, obstacle_part):
        """Lida com a colisão com obstáculos"""
        spacecraft = self.game.spacecraft
        
        # Knockback padrão
        spacecraft.velocity = config.SPACECRAFT_KNOCKBACK
        
        # Adiciona movimento horizontal para se afastar do obstáculo
        if obstacle:
            # Knockback horizontal
            if spacecraft.x > obstacle.x:
                spacecraft.x += 15  # Empurra para a direita
            else:
                spacecraft.x -= 15  # Empurra para a esquerda
            
            # Knockback vertical com base na parte que foi atingida
            if obstacle_part == "upper":
                # Atingiu o obstáculo superior, empurra para baixo
                spacecraft.velocity = abs(config.SPACECRAFT_KNOCKBACK) * 0.8
            elif obstacle_part == "lower":
                # Atingiu o obstáculo inferior, empurra para cima
                spacecraft.velocity = config.SPACECRAFT_KNOCKBACK * 0.8
    
    def check_collectible_collisions(self):
        """Verifica e lida com colisões com coletáveis"""
        spacecraft = self.game.spacecraft
        
        for collectible in list(self.game.collectibles):
            # Verifica colisão
            if collectible.check_collision(spacecraft):
                self._handle_collectible_effect(collectible)
                
                # Remove o item coletado
                self.game.collectibles.remove(collectible)
    
    def _handle_collectible_effect(self, collectible):
        """Aplica o efeito de um item coletado"""
        effect = collectible.get_effect()
        
        if effect["effect"] == "info":
            # Mostra informações do planeta
            self.game.nova.give_random_fact(self.game.current_planet.name)
            self.game.score += effect["value"]
            self._check_level_progression()
            
        elif effect["effect"] == "time":
            # Estende o tempo de jogo (adiciona pontuação)
            self.game.score += effect["value"]
            self.game.nova.react_to_discovery("fuel")
            self._check_level_progression()
            
        elif effect["effect"] == "attack":
            # Habilita a arma temporariamente através do sistema de armas
            self.game.weapon_system.activate()
            self.game.nova.react_to_discovery("weapon")
            
        elif effect["effect"] == "life":
            # Adiciona uma vida extra
            self.game.add_life()
    
    def _check_level_progression(self):
        """Verifica se a pontuação atingiu o limite para progressão de planeta"""
        # Level progression thresholds imported at the top
        
        # Obtém o limite para o planeta atual
        current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
            self.game.current_planet.name,
            10  # Limite padrão
        )
        
        # Verifica se a pontuação excede o limite e se há mais planetas disponíveis
        if (self.game.score >= current_threshold and 
            self.game.current_planet_index < len(self.game.planets) - 1):
            
            # Obtém o nome do próximo planeta
            next_planet_en = self.game.planets[self.game.current_planet_index + 1].name
            next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
            
            # Mostra mensagem de navegação
            self.game.nova.show_message(
                f"Navegação automática engajada! Indo para {next_planet_pt}!", 
                "excited"
            )
            
            # Inicia o quiz para avanço de planeta
            self.game.state_manager.start_quiz()
            return True
        
        return False