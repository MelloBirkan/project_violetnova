import pygame
import sys
from src.game import Game
from src.config import *

def main():
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()
    
    # Setup screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Projeto Violeta Nova: Explorador do Sistema Solar")
    
    # Initialize fonts after pygame is initialized
    import src.config as config
    config.GAME_FONT = pygame.font.Font(None, config.GAME_FONT_SIZE)
    config.SMALL_FONT = pygame.font.Font(None, config.SMALL_FONT_SIZE)
    config.COUNTDOWN_FONT = pygame.font.Font(None, config.COUNTDOWN_FONT_SIZE)
    
    # Create game instance
    game = Game()
    
    # Game loop
    clock = pygame.time.Clock()
    while True:
        game.input_handler.handle_events()
        game.update()
        game.draw()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()