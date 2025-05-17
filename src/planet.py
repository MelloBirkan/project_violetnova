import pygame
import os

class Planet:
    def __init__(self, name, gravity_factor, background_color, obstacle_count, quiz_questions, quiz_hints=None):
        self.name = name
        self.gravity_factor = gravity_factor  # Porcentagem da gravidade da Terra
        self.background_color = background_color
        self.obstacle_count = obstacle_count  # Número de obstáculos baseado no tamanho do planeta
        self.quiz_questions = quiz_questions  # Lista de dict com 'question', 'options', e 'answer'
        self.quiz_hints = quiz_hints or []  # Lista de dicas de quiz
        self.completed = False
        self.background_image = None  # Armazenará a imagem de fundo se disponível

        # Calcula o valor real da gravidade (gravidade da Terra * fator)
        self.gravity = 0.25 * (self.gravity_factor / 100.0) 

        # Cria assets específicos do planeta
        self.create_assets()

    def create_assets(self):
        """Cria assets visuais específicos do planeta"""
        # Tamanho base da superfície para textura do solo
        self.ground_texture = pygame.Surface((800, 100))
        
        # Tradução de nomes de planetas para caminhos de arquivo
        planet_folder_names = {
            "Earth": "terra",
            "Mercury": "mercurio",
            "Venus": "venus",
            "Mars": "marte",
            "Jupiter": "jupiter",
            "Saturn": "saturno",
            "Moon": "lua",
            "Uranus": "urano",
            "Neptune": "netuno"
        }
        
        # Obtém o nome da pasta para o planeta atual
        folder_name = planet_folder_names.get(self.name, "terra")
        
        # Tenta carregar imagem de fundo específica do planeta
        bg_path = os.path.join("assets", "images", "planets_sprites", folder_name, f"ceu_{folder_name}.png")
        try:
            self.background_image = pygame.image.load(bg_path).convert_alpha()
        except pygame.error:
            print(f"Falha ao carregar imagem de fundo de {self.name}, usando fallback")
            self.background_image = None
            
        # Tenta carregar imagem de textura do solo específica do planeta
        img_path = os.path.join("assets", "images", "planets_sprites", folder_name, f"chao_{folder_name}.png")
        try:
            tile_img = pygame.image.load(img_path).convert_alpha()
            tile_w, tile_h = tile_img.get_size()
            # Cria uma nova superfície para a textura do solo com altura adequada
            self.ground_texture = pygame.Surface((800, tile_h), pygame.SRCALPHA)
            # Ladrilha a imagem horizontalmente
            for x in range(0, 800, tile_w):
                self.ground_texture.blit(tile_img, (x, 0))
        except pygame.error:
            print(f"Falha ao carregar textura do solo de {self.name}, usando fallback")
            
            # Fallbacks específicos por planeta
            if self.name == "Earth":
                self.ground_texture.fill((34, 139, 34))  # Verde floresta
                # Adiciona detalhes de grama
                for i in range(0, 800, 20):
                    pygame.draw.rect(self.ground_texture, (0, 100, 0), (i, 0, 10, 20))
            elif self.name == "Moon":
                self.ground_texture.fill((169, 169, 169))  # Cinza escuro
                # Adiciona alguns detalhes de cratera
                for i in range(0, 800, 50):
                    pygame.draw.circle(self.ground_texture, (120, 120, 120), (i, 20), 10)
            elif self.name == "Mercury":
                self.ground_texture.fill((160, 82, 45))  # Marrom siena
                # Adiciona alguns detalhes de cratera
                for i in range(0, 800, 40):
                    pygame.draw.circle(self.ground_texture, (139, 69, 19), (i, 20), 8)
            elif self.name == "Venus":
                self.ground_texture.fill((218, 165, 32))  # Dourado
                # Adiciona alguns detalhes de rocha
                for i in range(0, 800, 30):
                    pygame.draw.rect(self.ground_texture, (184, 134, 11), (i, 0, 15, 15))
            elif self.name == "Mars":
                self.ground_texture.fill((205, 92, 92))  # Vermelho indiano
                # Adiciona alguns detalhes de rocha
                for i in range(0, 800, 35):
                    pygame.draw.rect(self.ground_texture, (178, 34, 34), (i, 0, 12, 12))
            elif self.name == "Jupiter":
                # Júpiter não tem superfície sólida, então cria um padrão semelhante a gás
                self.ground_texture.fill((244, 164, 96))  # Marrom arenoso
                for i in range(0, 800, 25):
                    pygame.draw.rect(self.ground_texture, (210, 105, 30), (i, 10, 15, 80))
            elif self.name == "Saturn":
                # Saturno não tem superfície sólida, então cria um padrão semelhante a gás
                self.ground_texture.fill((245, 222, 179))  # Cor de trigo
                for i in range(0, 800, 20):
                    pygame.draw.rect(self.ground_texture, (222, 184, 135), (i, 5, 10, 90))
            elif self.name == "Uranus":
                # Urano não tem superfície sólida, então cria um padrão semelhante a gás
                self.ground_texture.fill((175, 238, 238))  # Turquesa pálido
                for i in range(0, 800, 30):
                    pygame.draw.rect(self.ground_texture, (127, 255, 212), (i, 0, 20, 100))
            elif self.name == "Neptune":
                # Netuno não tem superfície sólida, então cria um padrão semelhante a gás
                self.ground_texture.fill((65, 105, 225))  # Azul royal
                for i in range(0, 800, 22):
                    pygame.draw.rect(self.ground_texture, (0, 0, 205), (i, 0, 11, 100))
            elif self.name == "Pluto":
                # Superfície gelada de Plutão
                self.ground_texture.fill((220, 220, 230))  # Cinza-azulado muito claro
                # Adiciona alguns detalhes de crateras de gelo
                for i in range(0, 800, 60):
                    pygame.draw.circle(self.ground_texture, (200, 200, 210), (i, 25), 12)
                    pygame.draw.circle(self.ground_texture, (190, 190, 200), (i+30, 15), 8)
            else:
                # Fallback genérico para outros planetas
                self.ground_texture.fill((120, 120, 120))  # Cinza neutro

    def get_info_text(self):
        """Retorna informações sobre o planeta para a tela de transição"""
        info_texts = {
            "Terra": "Planeta natal com 100% de gravidade (g = 1,0). Nosso planeta azul é o único corpo celeste conhecido a abrigar vida.",
            "Mercúrio": "Planeta mais próximo do Sol com 40% de gravidade (g = 0,4). Mercúrio praticamente não tem atmosfera.",
            "Vênus": "Segundo planeta a partir do Sol com 90% de gravidade (g = 0,9). Vênus tem uma atmosfera espessa e tóxica cheia de dióxido de carbono.",
            "Lua": "Satélite da Terra com 16% de gravidade (g = 0,16). A Lua tem cerca de 1/4 do diâmetro da Terra.",
            "Marte": "O Planeta Vermelho com 40% de gravidade (g = 0,4). Marte tem as maiores tempestades de poeira do sistema solar.",
            "Júpiter": "Maior planeta com 240% de gravidade (g = 2,4). Júpiter é um gigante gasoso e tem a Grande Mancha Vermelha, uma tempestade que dura há centenas de anos.",
            "Saturno": "Conhecido por seus anéis com 110% de gravidade (g = 1,1). Saturno é um gigante gasoso composto principalmente de hidrogênio e hélio.",
            "Urano": "Gigante de gelo com 90% de gravidade (g = 0,9). Urano gira de lado com uma inclinação axial de cerca de 98 graus.",
            "Netuno": "Planeta mais distante com 110% de gravidade (g = 1,1). Netuno tem os ventos mais fortes do Sistema Solar, atingindo até 2.100 km/h.",
            "Plutão": "Planeta anão com 6% de gravidade (g = 0,06). Plutão faz parte do Cinturão de Kuiper, uma região de corpos gelados além de Netuno."
        }
        return info_texts.get(self.name, "Planeta desconhecido")

    def draw_ground(self, screen, x, screen_height):
        """Desenha o solo para este planeta"""
        # Calcula a posição para desenhar o solo
        ground_y = screen_height - 100

        # Obtém a largura da tela para determinar quantas cópias precisamos
        screen_width = screen.get_width()

        # Calcula quantas cópias da textura do solo precisamos para cobrir a tela
        # Adiciona 2 cópias extras para garantir rolagem suave nas bordas
        num_copies = (screen_width // 800) + 3

        # Desenha múltiplas cópias da textura do solo para preencher a largura da tela
        for i in range(-1, num_copies):
            screen.blit(self.ground_texture, ((x % 800) + (i * 800), ground_y))
