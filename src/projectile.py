import pygame
import src.config as config

class Projetil:
    """Representa um projétil disparado pela espaçonave"""

    LARGURA = 12
    ALTURA = 4
    COR_PRINCIPAL = (255, 215, 0)  # Amarelo dourado
    COR_ALTERNATIVA = (255, 255, 255)

    def __init__(self, x, y, velocidade=12):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.contador_animacao = 0

    def atualizar(self):
        """Move o projétil para a direita e atualiza a animação"""
        self.x += self.velocidade
        self.contador_animacao += 0.2

    def fora_da_tela(self):
        return self.x > config.SCREEN_WIDTH

    def desenhar(self, tela):
        """Desenha o projétil com simples animação de cintilação"""
        cor = self.COR_PRINCIPAL if int(self.contador_animacao) % 2 == 0 else self.COR_ALTERNATIVA
        pygame.draw.rect(tela, cor, (self.x, self.y, self.LARGURA, self.ALTURA))

    def colide_com(self, obstaculo):
        """Verifica colisão simples com um obstáculo"""
        largura_obstaculo = getattr(obstaculo, 'top_width', obstaculo.WIDTH)
        altura_superior = (obstaculo.gap_y - obstaculo.GAP // 2)
        altura_inferior = (obstaculo.gap_y + obstaculo.GAP // 2)

        # Retângulo do projétil
        ret_proj = pygame.Rect(self.x, self.y, self.LARGURA, self.ALTURA)

        # Retângulo do obstáculo superior
        ret_sup = pygame.Rect(obstaculo.x, 0, largura_obstaculo, altura_superior)
        # Retângulo do obstáculo inferior
        ret_inf = pygame.Rect(obstaculo.x, altura_inferior, largura_obstaculo, config.SCREEN_HEIGHT - altura_inferior)

        return ret_proj.colliderect(ret_sup) or ret_proj.colliderect(ret_inf)
