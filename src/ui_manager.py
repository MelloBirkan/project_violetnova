import pygame
import math
import src.config as config
from src.planet_data import PLANET_NAME_PT, LEVEL_PROGRESSION_THRESHOLDS

class UIManager:
    def __init__(self, game):
        self.game = game
        
    def draw(self, screen):
        """Draws the game UI based on current state"""
        # Draw the background
        self.game.visual_effects.draw_background(screen, self.game.current_planet)
        
        # Draw content based on game state
        if self.game.state == config.PLAYING or self.game.state == config.MENU or self.game.state == config.GAME_OVER or self.game.state == config.QUIZ_FAILURE:
            self._draw_game_elements(screen)
            
            # Draw specific UI screens based on state
            if self.game.state == config.MENU:
                self.draw_menu_screen(screen)
            elif self.game.state == config.GAME_OVER:
                self.draw_game_over_screen(screen)
            elif self.game.state == config.QUIZ_FAILURE and self.game.state_manager.quiz_failure_timer > 0:
                countdown = math.ceil(self.game.state_manager.quiz_failure_timer / 60)
                self.game.visual_effects.draw_countdown(screen, countdown)
                
        elif self.game.state == config.TRANSITION:
            self.draw_transition_screen(screen)
        elif self.game.state == config.QUIZ:
            # Draw the quiz
            self.game.quiz.draw(screen)
        elif self.game.state == config.QUIZ_FAILURE:
            self.draw_quiz_failure_screen(screen)
            
        # Always draw the NOVA AI assistant on top
        self.game.nova.draw(screen)
            
    def _draw_game_elements(self, screen):
        """Draws the common game elements (obstacles, collectibles, spacecraft, etc.)"""
        # Draw obstacles
        for obstacle in self.game.obstacles:
            obstacle.draw(screen)
            
        # Draw collectibles
        for collectible in self.game.collectibles:
            collectible.draw(screen)
            
        # Draw the ground/floor
        self.game.current_planet.draw_ground(screen, self.game.floor_x, config.SCREEN_HEIGHT)
        
        # Draw the spacecraft (with invulnerability effect if applicable)
        self.game.spacecraft.draw(screen, self.game.invulnerable)
        
        # Draw game info if not in menu state
        if self.game.state != config.MENU:
            self._draw_game_info(screen)
            
    def _draw_game_info(self, screen):
        """Draws game information (score, lives, etc.)"""
        # Left side information
        display_name = PLANET_NAME_PT.get(self.game.current_planet.name, self.game.current_planet.name)
        planet_text = config.SMALL_FONT.render(f"Planeta: {display_name}", True, (255, 255, 255))
        screen.blit(planet_text, (20, 20))
        
        # Show furthest planet reached
        furthest_planet = self.game.planets[self.game.furthest_planet_index].name
        furthest_planet_pt = PLANET_NAME_PT.get(furthest_planet, furthest_planet)
        furthest_text = config.SMALL_FONT.render(f"Mais distante: {furthest_planet_pt}", True, (255, 215, 0))
        screen.blit(furthest_text, (20, 50))
        
        # Get threshold for current planet
        current_threshold = LEVEL_PROGRESSION_THRESHOLDS.get(
            self.game.current_planet.name,
            10  # Default limit
        )
        
        score_text = config.SMALL_FONT.render(f"Pontuação: {self.game.score}/{current_threshold}", True, (255, 255, 255))
        screen.blit(score_text, (20, 80))
        
        # Draw lives indicator
        lives_text = config.SMALL_FONT.render(f"Vidas:", True, (255, 255, 255))
        screen.blit(lives_text, (20, 110))
        
        # Draw life icons
        self.game.visual_effects.draw_life_icons(screen, self.game.lives, self.game.max_lives)
        
        # Draw weapon status at top center if active
        if self.game.weapon_active:
            weapon_time = self.game.weapon_timer // 60  # Convert to seconds
            weapon_text = config.SMALL_FONT.render(f"Arma Ativa: {weapon_time}s", True, (255, 100, 100))
            screen.blit(weapon_text, (config.SCREEN_WIDTH // 2 - weapon_text.get_width() // 2, 20))
            
    def draw_menu_screen(self, screen):
        """Draws the menu screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        title_text = config.GAME_FONT.render("PROJETO VIOLETA NOVA", True, (255, 255, 255))
        subtitle_text = config.SMALL_FONT.render("Explorador do Sistema Solar", True, (200, 200, 255))

        screen.blit(title_text, (config.SCREEN_WIDTH // 2 - title_text.get_width() // 2, 180))
        screen.blit(subtitle_text, (config.SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 220))

        if self.game.in_difficulty_menu:
            self.draw_difficulty_menu(screen)
            return
        
        # Draw menu options
        for i, option in enumerate(config.MENU_OPTIONS):
            y_pos = config.MENU_START_Y + (i * config.MENU_OPTION_SPACING)
            
            # Highlight selected option
            if i == self.game.selected_menu_option:
                # Draw selection box
                box_padding = 20
                box_width = 400
                box_height = 40
                box_x = config.SCREEN_WIDTH // 2 - box_width // 2
                box_y = y_pos - 10
                
                # Draw glowing effect for selected option
                glow_surface = pygame.Surface((box_width + 40, box_height + 40), pygame.SRCALPHA)
                for offset in range(3):
                    alpha = 50 - (offset * 15)
                    pygame.draw.rect(glow_surface, (100, 100, 255, alpha), 
                                   (20 - offset * 4, 20 - offset * 4, 
                                    box_width + offset * 8, box_height + offset * 8), 
                                   2, border_radius=10)
                screen.blit(glow_surface, (box_x - 20, box_y - 20))
                
                # Draw the box
                pygame.draw.rect(screen, (50, 50, 150), (box_x, box_y, box_width, box_height), 
                               border_radius=10)
                pygame.draw.rect(screen, (100, 100, 255), (box_x, box_y, box_width, box_height), 
                               2, border_radius=10)
                
                option_text = config.GAME_FONT.render(option, True, (255, 255, 255))
            else:
                option_text = config.GAME_FONT.render(option, True, (180, 180, 180))
            
            screen.blit(option_text, (config.SCREEN_WIDTH // 2 - option_text.get_width() // 2, y_pos))
        
        # Show current difficulty
        diff_name = config.DIFFICULTY_NAMES.get(self.game.difficulty, "")
        diff_text = config.SMALL_FONT.render(
            f"Dificuldade: {diff_name}", True, (255, 255, 255)
        )
        screen.blit(diff_text, (config.SCREEN_WIDTH // 2 - diff_text.get_width() // 2, config.MENU_START_Y - 40))

        # Show controls
        controls_title = config.SMALL_FONT.render("Controles do Menu:", True, (255, 255, 255))
        controls_nav = config.SMALL_FONT.render("SETA PARA CIMA/BAIXO - Navegar | ENTER/ESPAÇO - Selecionar", True, (200, 200, 200))
        
        controls_y = config.SCREEN_HEIGHT - 150
        screen.blit(controls_title, (config.SCREEN_WIDTH // 2 - controls_title.get_width() // 2, controls_y))
        screen.blit(controls_nav, (config.SCREEN_WIDTH // 2 - controls_nav.get_width() // 2, controls_y + 30))
        
        # Show game controls
        game_controls_title = config.SMALL_FONT.render("Controles do Jogo:", True, (255, 255, 255))
        controls_space = config.SMALL_FONT.render("ESPAÇO - Impulsionar | W - Usar Arma", True, (200, 200, 200))
        
        screen.blit(game_controls_title, (config.SCREEN_WIDTH // 2 - game_controls_title.get_width() // 2, controls_y + 60))
        screen.blit(controls_space, (config.SCREEN_WIDTH // 2 - controls_space.get_width() // 2, controls_y + 90))
        
    def draw_game_over_screen(self, screen):
        """Draws the game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        game_over_text = config.GAME_FONT.render("MISSÃO CONCLUÍDA", True, (255, 215, 0))
        score_text = config.GAME_FONT.render(f"Pontuação Final: {self.game.score}", True, (255, 255, 255))
        
        # Mensagem personalizada baseada no checkpoint
        difficulty_settings = config.DIFFICULTY_SETTINGS[self.game.difficulty]
        if difficulty_settings["save_checkpoint"]:
            restart_text = config.GAME_FONT.render("Pressione ESPAÇO para continuar a missão", True, (255, 255, 255))
        else:
            restart_text = config.GAME_FONT.render("Pressione ESPAÇO para nova missão desde a Terra", True, (255, 255, 255))
        
        # Calculate furthest planet reached
        furthest_planet = self.game.planets[min(self.game.current_planet_index, len(self.game.planets) - 1)].name
        furthest_planet_pt = PLANET_NAME_PT.get(furthest_planet, furthest_planet)
        planet_text = config.GAME_FONT.render(f"Planeta mais distante: {furthest_planet_pt}", True, (255, 255, 255))
        
        screen.blit(game_over_text, (config.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
        screen.blit(score_text, (config.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 220))
        screen.blit(planet_text, (config.SCREEN_WIDTH // 2 - planet_text.get_width() // 2, 320))
        screen.blit(restart_text, (config.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))
        
    def draw_transition_screen(self, screen):
        """Draws the transition screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Darker overlay for text readability
        screen.blit(overlay, (0, 0))
        
        # Draw destination planet name
        display_name = PLANET_NAME_PT.get(self.game.current_planet.name, self.game.current_planet.name)
        planet_title = config.GAME_FONT.render(f"Bem-vindo a {display_name}", True, (255, 255, 255))
        screen.blit(planet_title, (config.SCREEN_WIDTH // 2 - planet_title.get_width() // 2, 100))
        
        # Draw gravity information
        gravity_text = config.GAME_FONT.render(f"Gravidade: {self.game.current_planet.gravity_factor}% da Terra", True, (255, 255, 255))
        screen.blit(gravity_text, (config.SCREEN_WIDTH // 2 - gravity_text.get_width() // 2, 150))
        
        # Draw planet info text
        info_text = self.game.current_planet.get_info_text()
        # Wrap text to fit screen
        wrapped_lines = []
        words = info_text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            test_surface = config.SMALL_FONT.render(test_line, True, (255, 255, 255))
            if test_surface.get_width() < config.SCREEN_WIDTH - 100:
                line = test_line
            else:
                wrapped_lines.append(line)
                line = word + " "
        wrapped_lines.append(line)  # Add last line
        
        # Draw wrapped text
        for i, line in enumerate(wrapped_lines):
            line_surface = config.SMALL_FONT.render(line, True, (200, 200, 255))
            screen.blit(line_surface, (config.SCREEN_WIDTH // 2 - line_surface.get_width() // 2, 220 + i * 30))
            
        # Draw progress indicator
        progress_text = config.SMALL_FONT.render(f"Planeta {self.game.current_planet_index + 1} de {len(self.game.planets)}", True, (180, 180, 180))
        screen.blit(progress_text, (config.SCREEN_WIDTH // 2 - progress_text.get_width() // 2, 350))
        
        # Draw continue prompt
        if self.game.state_manager.transition_time > 60:  # Only show after 1 second
            continue_text = config.SMALL_FONT.render("Pressione ESPAÇO para continuar", True, (255, 255, 255))
            # Pulsating effect
            alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
            continue_text.set_alpha(alpha)
            screen.blit(continue_text, (config.SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 450))
            
    def draw_quiz_failure_screen(self, screen):
        """Draws the quiz failure screen with countdown"""
        # Add semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # More visible semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Calculate countdown number
        countdown_number = self.game.state_manager.quiz_failure_timer // 60 + 1
        
        # Draw large countdown number
        self.game.visual_effects.draw_countdown(screen, countdown_number)
        
        # Draw "Returning..." text with pulsing effect
        self.game.visual_effects.draw_pulsing_text(
            screen,
            "Retornando à órbita...",
            pygame.font.Font(None, 42),  # Create temporary font for pulsing text
            (255, 255, 255),
            (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 100)
        )

    def draw_difficulty_menu(self, screen):
        """Desenha o submenu de seleção de dificuldade"""
        # Criar um overlay escuro para melhor visibilidade
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Título principal
        title = config.GAME_FONT.render("Selecione a Dificuldade", True, (255, 255, 255))
        screen.blit(title, (config.SCREEN_WIDTH // 2 - title.get_width() // 2, 60))
        
        # Descrições e cores para cada dificuldade
        difficulty_data = {
            config.DIFFICULTY_EASY: {
                "name": "Fácil",
                "color": (50, 255, 50),  # Verde
                "description": "Para novos exploradores espaciais",
                "details": [
                    "• 3 vidas desde o início",
                    "• Obstáculos mais espaçados",
                    "• Salvamento de progresso"
                ],
                "stars": 1
            },
            config.DIFFICULTY_MEDIUM: {
                "name": "Médio",
                "color": (255, 255, 50),  # Amarelo
                "description": "Desafio equilibrado",
                "details": [
                    "• Até 3 vidas totais",
                    "• Obstáculos normais",
                    "• Sem salvamento automático"
                ],
                "stars": 2
            },
            config.DIFFICULTY_HARD: {
                "name": "Difícil",
                "color": (255, 50, 50),  # Vermelho
                "description": "Para pilotos experientes",
                "details": [
                    "• 1 vida apenas",
                    "• Obstáculos mais frequentes",
                    "• Sem salvamento automático"
                ],
                "stars": 3
            }
        }
        
        difficulties = [config.DIFFICULTY_EASY, config.DIFFICULTY_MEDIUM, config.DIFFICULTY_HARD]
        
        for i, diff in enumerate(difficulties):
            y_base = 130 + i * 180  # Espaçamento ainda maior entre opções
            
            data = difficulty_data[diff]
            
            # Box de seleção
            box_width = 620
            box_height = 100
            box_x = config.SCREEN_WIDTH // 2 - box_width // 2
            box_y = y_base
            
            # Destacar opção selecionada
            if i == self.game.selected_difficulty:
                # Efeito de brilho
                glow_surf = pygame.Surface((box_width + 40, box_height + 40), pygame.SRCALPHA)
                for offset in range(3):
                    alpha = 50 - (offset * 15)
                    color_with_alpha = (*data["color"], alpha)
                    pygame.draw.rect(glow_surf, color_with_alpha, 
                                   (20 - offset * 4, 20 - offset * 4, 
                                    box_width + offset * 8, box_height + offset * 8), 
                                   3, border_radius=15)
                screen.blit(glow_surf, (box_x - 20, box_y - 20))
                
                # Box principal
                box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
                pygame.draw.rect(box_surf, (*data["color"], 30), 
                               (0, 0, box_width, box_height), 
                               border_radius=10)
                pygame.draw.rect(box_surf, data["color"], 
                               (0, 0, box_width, box_height), 
                               3, border_radius=10)
                screen.blit(box_surf, (box_x, box_y))
                
                # Indicador de seleção
                arrow = config.GAME_FONT.render("►", True, data["color"])
                screen.blit(arrow, (box_x - 40, box_y + box_height//2 - arrow.get_height()//2))
            else:
                # Box não selecionado
                box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
                pygame.draw.rect(box_surf, (50, 50, 50, 100), 
                               (0, 0, box_width, box_height), 
                               border_radius=10)
                pygame.draw.rect(box_surf, (100, 100, 100), 
                               (0, 0, box_width, box_height), 
                               2, border_radius=10)
                screen.blit(box_surf, (box_x, box_y))
            
            # Nome da dificuldade
            name_text = config.GAME_FONT.render(data["name"], True, data["color"])
            screen.blit(name_text, (box_x + 20, box_y + 10))
            
            # Descrição
            desc_text = config.SMALL_FONT.render(data["description"], True, (200, 200, 200))
            screen.blit(desc_text, (box_x + 20, box_y + 40))
            
            # Detalhes
            for j, detail in enumerate(data["details"]):
                detail_text = config.SMALL_FONT.render(detail, True, (180, 180, 180))
                screen.blit(detail_text, (box_x + 300, box_y + 15 + j * 22))
            
            # Desenhar estrelas para indicar dificuldade - canto superior direito
            star_base_x = box_x + box_width - 100  # Posicionar no canto direito
            star_y = box_y + 20  # Mais para cima
            star_size = 8  # Estrelas menores
            for star_idx in range(data["stars"]):
                star_x = star_base_x + star_idx * 20  # Menor espaçamento
                # Desenhar estrela
                points = []
                for point in range(10):
                    if point % 2 == 0:
                        # Pontas externas
                        angle = math.pi * 2 * point / 10 - math.pi / 2
                        x = star_x + star_size * math.cos(angle)
                        y = star_y + star_size * math.sin(angle)
                    else:
                        # Pontas internas
                        angle = math.pi * 2 * point / 10 - math.pi / 2
                        x = star_x + star_size // 2 * math.cos(angle)
                        y = star_y + star_size // 2 * math.sin(angle)
                    points.append((x, y))
                pygame.draw.polygon(screen, data["color"], points)
            
            # Indicador de dificuldade atual
            if self.game.difficulty == diff:
                current_text = config.SMALL_FONT.render("(Atual)", True, data["color"])
                screen.blit(current_text, (box_x + name_text.get_width() + 30, box_y + 12))
        
        # Instruções
        info_text = config.SMALL_FONT.render(
            "SETA PARA CIMA/BAIXO - Escolher | ENTER - Confirmar | ESC - Voltar",
            True,
            (200, 200, 200),
        )
        screen.blit(
            info_text,
            (config.SCREEN_WIDTH // 2 - info_text.get_width() // 2, config.SCREEN_HEIGHT - 80),
        )
