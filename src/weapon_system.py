import pygame
from src.planet_data import LEVEL_PROGRESSION_THRESHOLDS, PLANET_NAME_PT
import src.config as config
from src.projectile import Projetil

class WeaponSystem:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.timer = 0
        self.projectiles = []
        
    def update(self):
        """Atualiza o estado da arma"""
        if self.active:
            self.timer -= 1
            self.game.weapon_timer = self.timer
            if self.timer <= 0:
                self.deactivate()

        # Atualiza projéteis existentes
        for proj in list(self.projectiles):
            proj.atualizar()

            # Verifica colisão com obstáculos
            for obst in list(self.game.obstacles):
                if proj.colide_com(obst):
                    self.game.obstacles.remove(obst)
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    self.game.score += 2
                    self.game.nova.show_message("Obstáculo destruído!", "alert")

                    # Verifica progressão de planeta
                    current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
                        self.game.current_planet.name,
                        10,
                    )
                    if (
                        self.game.score >= current_threshold
                        and self.game.current_planet_index < len(self.game.planets) - 1
                    ):
                        next_planet_en = self.game.planets[self.game.current_planet_index + 1].name
                        next_planet_pt = PLANET_NAME_PT.get(next_planet_en, next_planet_en)
                        self.game.nova.show_message(
                            f"Navegação automática engajada! Indo para {next_planet_pt}!",
                            "excited",
                        )

                        next_planet = self.game.planets[self.game.current_planet_index + 1].name.lower()
                        self.game.furthest_planet_index = max(
                            self.game.furthest_planet_index, self.game.current_planet_index + 1
                        )

                        self.game.planet_tracker.save(
                            next_planet,
                            update_furthest=True,
                            allow_save=config.DIFFICULTY_SETTINGS[self.game.difficulty][
                                "save_checkpoint"
                            ],
                        )

                        self.game.state_manager.start_quiz()
                    break

            if proj.fora_da_tela() and proj in self.projectiles:
                self.projectiles.remove(proj)
                
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
        """Dispara um projétil a partir da nave"""
        if not self.active:
            return

        inicio_x = (
            self.game.spacecraft.x
            + self.game.spacecraft.flame_extent
            + self.game.spacecraft.WIDTH
        )
        inicio_y = (
            self.game.spacecraft.y
            + self.game.spacecraft.HEIGHT // 2
            - Projetil.ALTURA // 2
        )

        self.projectiles.append(Projetil(inicio_x, inicio_y))
