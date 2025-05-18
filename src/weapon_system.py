import pygame
from src.planet_data import LEVEL_PROGRESSION_THRESHOLDS, PLANET_NAME_PT
import src.config as config

class WeaponSystem:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.timer = 0
        
    def update(self):
        """Atualiza o estado da arma"""
        if self.active:
            self.timer -= 1
            self.game.weapon_timer = self.timer
            if self.timer <= 0:
                self.deactivate()
                
    def activate(self, duration=600):
        """Ativa a arma por um tempo determinado (padrão 10s a 60fps)"""
        self.active = True
        self.timer = duration
        self.game.weapon_active = True
        self.game.weapon_timer = duration
        self.game.nova.show_message("Sistemas defensivos ativados! Pressione W para usar.", "excited")
        
    def deactivate(self):
        """Desativa a arma"""
        self.active = False
        self.timer = 0
        self.game.weapon_active = False
        self.game.weapon_timer = 0
        self.game.nova.show_message("Sistemas defensivos offline", "normal")
        
    def use(self):
        """Usa a arma para destruir obstáculos"""
        if not self.active:
            return

        # Encontra o obstáculo mais próximo à frente da nave
        target_obstacle = None
        min_distance = float('inf')

        # Define a posição x do corpo da nave
        spacecraft_body_x = self.game.spacecraft.x + self.game.spacecraft.flame_extent

        for obstacle in self.game.obstacles:
            # Considera apenas obstáculos à frente do corpo da nave
            if obstacle.x > spacecraft_body_x:
                distance = obstacle.x - spacecraft_body_x
                if distance < min_distance:
                    min_distance = distance
                    target_obstacle = obstacle

        if target_obstacle:
            # Remove o obstáculo e concede pontos
            self.game.obstacles.remove(target_obstacle)
            self.game.score += 2
            self.game.nova.show_message("Obstáculo destruído!", "alert")
            
            # Verifica progressão para o próximo planeta com a nova pontuação
            current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
                self.game.current_planet.name,
                10  # Limite padrão para planetas não especificados
            )
            if (self.game.score >= current_threshold and 
                self.game.current_planet_index < len(self.game.planets) - 1):
                next_planet_en = self.game.planets[self.game.current_planet_index + 1].name
                next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
                self.game.nova.show_message(f"Navegação automática engajada! Indo para {next_planet_pt}!", "excited")
                
                # Atualiza o planeta mais distante alcançado na memória
                next_planet = self.game.planets[self.game.current_planet_index + 1].name.lower()
                self.game.furthest_planet_index = max(self.game.furthest_planet_index, self.game.current_planet_index + 1)
                
                # Salva o planeta atual e atualiza o mais distante conforme a dificuldade
                self.game.planet_tracker.save(
                    next_planet,
                    update_furthest=True,
                    allow_save=config.DIFFICULTY_SETTINGS[self.game.difficulty]["save_checkpoint"],
                )
                
                # Inicia o quiz para avanço de planeta
                self.game.state_manager.start_quiz()