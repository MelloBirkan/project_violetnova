import pygame
import sys
import argparse
from src.game import Game
from src.config import *
from src.autopilot import QLearningAutopilot

def main():
    # Configura argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Projeto Violeta Nova: Explorador do Sistema Solar")
    parser.add_argument('--autopilot', action='store_true', help='Habilita piloto automático com aprendizado de máquina')
    parser.add_argument('--load-model', type=str, default=None, help='Carrega um modelo de piloto automático salvo')
    parser.add_argument('--save-model', type=str, default=None, help='Salva o modelo de piloto automático ao final')
    args = parser.parse_args()

    # Inicializa o pygame
    pygame.init()
    pygame.mixer.init()

    # Configura a tela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Projeto Violeta Nova: Explorador do Sistema Solar")

    # Inicializa as fontes após o pygame
    # Quiz e outros componentes dependem dessas fontes na criação
    import src.config as config
    config.GAME_FONT = pygame.font.Font(None, config.GAME_FONT_SIZE)
    config.SMALL_FONT = pygame.font.Font(None, config.SMALL_FONT_SIZE)
    config.COUNTDOWN_FONT = pygame.font.Font(None, config.COUNTDOWN_FONT_SIZE)
    
    # Cria a instância do jogo
    game = Game()
    
    # Inicializa o piloto automático se solicitado
    autopilot = None
    if args.autopilot:
        autopilot = QLearningAutopilot(game)
        if args.load_model:
            autopilot.load_model(args.load_model)

    # Loop principal do jogo
    clock = pygame.time.Clock()
    running = True
    
    try:
        while running:
            # Lista para armazenar eventos antes de processá-los
            events = pygame.event.get()
            
            # Verifique eventos de saída e tecla 'a' para controle do autopilot
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                # Permite que o usuário desative/ative o piloto automático com a tecla 'a'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_a and autopilot:
                    args.autopilot = not args.autopilot
                    message = "Piloto automático " + ("ativado" if args.autopilot else "desativado")
                    game.nova.show_message(message, "info")
            
            # Processa eventos manualmente se o autopilot estiver desativado
            if not args.autopilot:
                for event in events:
                    try:
                        game.input_handler.handle_event(event)
                    except Exception as e:
                        print(f"Erro ao processar evento: {e}")
            # Atualiza o piloto automático
            elif autopilot:
                try:
                    autopilot.update()
                except Exception as e:
                    print(f"Erro no piloto automático: {e}")
                    # Desativa o piloto automático em caso de erro contínuo
                    error_count = getattr(autopilot, 'error_count', 0) + 1
                    autopilot.error_count = error_count
                    if error_count > 10:
                        print("Desativando piloto automático devido a erros contínuos")
                        args.autopilot = False
                
            # Atualiza estado do jogo
            try:
                game.update()
            except Exception as e:
                print(f"Erro ao atualizar jogo: {e}")
            
            # Renderiza o jogo
            game.draw()
            
            # Atualiza a tela
            pygame.display.flip()
            clock.tick(60)
    
    except KeyboardInterrupt:
        print("Jogo interrompido pelo usuário")
    
    finally:
        # Salva o modelo de piloto automático se solicitado
        if args.autopilot and autopilot and args.save_model:
            autopilot.save_model(args.save_model)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
