import pygame
import os

class Spacecraft:
    WIDTH = 100
    HEIGHT = 40
    HITBOX_WIDTH = 70  # Largura da caixa de colisão
    HITBOX_HEIGHT = 28 # Altura da caixa de colisão
    
    
    def __init__(self, x, y):
        # Posição e física
        self.x = x
        self.y = y
        self.velocity = 0
        self.angle = 0
        # Cores da chama substituídas: gradiente do exterior para o interior (exterior estático, interior dinâmico)
        self.flame_colors = [
            (178, 34, 34),    # Vermelho escuro (exterior)
            (255, 69, 0),     # Vermelho-laranja
            (255, 165, 0),    # Laranja
            (255, 255, 0),    # Amarelo
            (255, 200, 0)   # Branco (ponta interna dinâmica)
        ]
        # Controle de empuxo
        self.thrusting = False
        self.thrust_power = 3.0
        self.thrust_multiplier = 1.0
        # Tempo de exibição do empuxo e extensão da chama (ms & px)
        self.last_thrust_time = 0
        self.thrust_display_time = 400  # ms para exibir a chama do empuxo
        # Largura da extensão da chama para uma chama de motor mais proeminente (mais larga para maior efeito)
        self.flame_extent = 40
        # Variáveis de animação da chama
        self.animation_frames = 10
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_counter = 0
        # Carrega o sprite da espaçonave
        self.sprite_path = os.path.join("assets", "images", "nova_2x.png")
        self.sprite = pygame.image.load(self.sprite_path)
        # Dimensiona o sprite para a LARGURA e ALTURA visuais
        self.sprite = pygame.transform.scale(self.sprite, (self.WIDTH, self.HEIGHT))
        # Cria a base da espaçonave e os quadros de empuxo
        self.create_animation_frames()
    
    def update(self, gravity, screen_height=720, floor_height=100):
        # Aplica a gravidade e atualiza a posição
        self.velocity += gravity

        # Adapta a potência do empuxo com base na gravidade do planeta
        self.thrust_multiplier = max(1.0, gravity * 4)

        # Aplica o impulso de empuxo
        if self.thrusting:
            self.velocity -= self.thrust_power * self.thrust_multiplier
            self.thrusting = False

        # Calcula nova posição
        new_y = self.y + self.velocity

        # Impede que a nave ultrapasse o limite superior da tela
        if new_y < 0:
            new_y = 0
            self.velocity = 0  # Zera a velocidade para evitar oscilação

        # Impede que a nave ultrapasse o chão, mas permite que colida com ele
        ground_limit = screen_height - floor_height - self.HITBOX_HEIGHT
        if new_y > ground_limit:
            new_y = ground_limit
            # Mantém a verificação de colisão no método check_collision,
            # mas impede que a nave vá abaixo do chão visualmente

        # Aplica a nova posição
        self.y = new_y

        # Atualiza o ângulo da espaçonave com base na velocidade
        self.angle = min(max(-30, -self.velocity * 2), 60)

        # Anima os quadros da chama de empuxo (sempre ciclando)
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % self.animation_frames
    
    def thrust(self):
        # Aplica empuxo
        self.thrusting = True
        # Velocidade imediata para responsividade
        self.velocity -= 0.5 * self.thrust_multiplier
        # Registra o tempo para mostrar a chama de empuxo
        self.last_thrust_time = pygame.time.get_ticks()
    
    def create_animation_frames(self):
        """Cria todos os quadros para a animação da espaçonave com gradiente de chama triangular contínuo e ponta animada."""
        fe = self.flame_extent  # Extensão da Chama (comprimento máximo)
        total_w = self.WIDTH + fe
        base = pygame.Surface((total_w, self.HEIGHT), pygame.SRCALPHA)
        base.fill((0, 0, 0, 0))
        # Sprite posicionado deixando espaço para a chama à esquerda
        sprite_rect = pygame.Rect(fe, 0, self.WIDTH, self.HEIGHT)
        base.blit(self.sprite, sprite_rect)

        # Posicionamento da chama
        flame_origin_x = fe  # Coordenada X onde a chama começa (lado direito da área da chama)
        # Aumenta o deslocamento para mover a chama para baixo
        lower_offset = int(self.HEIGHT * 0.25) # Origem ligeiramente mais baixa para a base da chama
        center_y = self.HEIGHT // 2 + lower_offset
        # Meia-altura máxima da chama em sua base (bico)
        max_flame_base_half_height = max(3, int(self.HEIGHT * 0.15))

        engine_colors = self.flame_colors

        # Comprimentos de cintilação para animação dinâmica
        # Comprimentos ajustados para um efeito de cintilação potencialmente mais visível
        flicker_tip_lengths = [int(fe * 0.8), int(fe * 1.0), int(fe * 0.9)]
        # Parâmetros de animação da ponta (variação de tamanho para o elemento brilhante da ponta)
        tip_animation_sizes = [3, 5, 4] # Tamanhos de exemplo para o elemento brilhante da ponta

        num_anim_frames = len(flicker_tip_lengths)
        if len(tip_animation_sizes) != num_anim_frames:
             # Garante que a lista de tamanhos de animação corresponda à contagem de quadros
             tip_animation_sizes = (tip_animation_sizes * (num_anim_frames // len(tip_animation_sizes) + 1))[:num_anim_frames]

        thrust_images = []
        for idx, current_flame_length in enumerate(flicker_tip_lengths):
            img = base.copy()

            # --- Desenha a Chama Gradiente usando Triângulos Aninhados ---
            num_colors = len(engine_colors)
            for i in range(num_colors):
                 color = engine_colors[i]
                 # Fração de comprimento para esta camada de cor (camadas externas são mais longas, internas mais curtas)
                 # Camada i=0 é a mais externa, i=num_colors-1 é a mais interna
                 length_fraction = 1.0 - (i / num_colors)
                 layer_length = current_flame_length * length_fraction

                 # Coordenada X da ponta para esta camada (estende-se para a esquerda a partir da origem)
                 layer_tip_x = flame_origin_x - layer_length

                 # Meia-altura na base para esta camada (afunila linearmente com o comprimento)
                 layer_base_half_height = max_flame_base_half_height * length_fraction

                 # Pontos para o triângulo desta camada de cor
                 p_tip = (int(layer_tip_x), center_y)
                 p_base1 = (flame_origin_x, int(center_y - layer_base_half_height))
                 p_base2 = (flame_origin_x, int(center_y + layer_base_half_height))

                 # Garante que os pontos formem um triângulo válido antes de desenhar
                 if p_tip[0] < p_base1[0] and p_base1[1] < p_base2[1]:
                     pygame.draw.polygon(img, color, [p_tip, p_base1, p_base2])


            # --- Adiciona Elemento de Ponta Animado ---
            # Posiciona o elemento da ponta no final da chama do quadro atual
            tip_center_x = flame_origin_x - current_flame_length
            tip_center_y = center_y
            tip_size = tip_animation_sizes[idx] # Obtém o tamanho para este quadro
            tip_color = (255, 255, 220) # Ponta branco-amarelada brilhante

            # Desenha um pequeno círculo na ponta para animação
            pygame.draw.circle(img, tip_color, (int(tip_center_x), int(tip_center_y)), tip_size)

            thrust_images.append(img)

        self.base_image = base # Armazena a imagem base sem nenhuma chama
        self.thrust_images = thrust_images
        # Atualiza o número de quadros de animação com base nas imagens geradas
        self.animation_frames = len(self.thrust_images)
        # Redefine o índice do quadro por precaução
    
    def update_image(self):
        """Atualiza todos os quadros de animação"""
        self.create_animation_frames()
    
    def draw(self, screen, invulnerable=False):
        """Desenha a espaçonave, mostrando a chama de empuxo se o empuxo foi acionado recentemente"""
        # Determina se devemos exibir a chama de empuxo
        now = pygame.time.get_ticks()
        if now - self.last_thrust_time < self.thrust_display_time:
            # Imagem de empuxo animada
            current = self.thrust_images[self.current_frame]
        else:
            # Imagem base sem exaustão
            current = self.base_image

        # Efeito de piscar quando invulnerável
        if invulnerable:
            # Faz a nave piscar a cada 200ms
            if (now // 200) % 2 == 0:
                # Cria uma cópia da imagem para modificar
                current = current.copy()
                # Adiciona uma sobreposição azulada semitransparente
                overlay = pygame.Surface(current.get_size(), pygame.SRCALPHA)
                overlay.fill((100, 100, 255, 100))  # Azul translúcido
                current.blit(overlay, (0, 0))

        # Rotaciona a imagem do quadro atual (ângulo positivo inclina o nariz para cima)
        rotated = pygame.transform.rotate(current, self.angle)
        # Calcula a posição central considerando a extensão da chama
        cx = self.x + self.WIDTH // 2 + self.flame_extent // 2
        cy = self.y + self.HEIGHT // 2
        rect = rotated.get_rect(center=(cx, cy))
        screen.blit(rotated, rect.topleft)