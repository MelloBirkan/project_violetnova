import pygame

# Configuração da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FLOOR_HEIGHT = 100

# Estados do jogo
MENU = 0
PLAYING = 1
GAME_OVER = 2
TRANSITION = 3
QUIZ = 4
QUIZ_FAILURE = 5

# Modos de controle
CONTROL_MODE_FLAPPY = 0  # Toque para empuxo, estilo Flappy Bird
CONTROL_MODE_HOLD = 1    # Segure o espaço para empuxo contínuo

# Configurações de fonte - serão inicializadas depois
GAME_FONT = None
SMALL_FONT = None
COUNTDOWN_FONT = None

# Tamanhos de fonte
GAME_FONT_SIZE = 36
SMALL_FONT_SIZE = 24
COUNTDOWN_FONT_SIZE = 180

# Dicionários de tradução
COLOR_NAME_PT = {
    "silver": "Prateado",
    "gold": "Dourado",
    "blue": "Azul",
    "red": "Vermelho"
}

PLANET_NAME_PT = {
    "Earth": "Terra",
    "Mercury": "Mercúrio",
    "Venus": "Vênus",
    "Moon": "Lua",
    "Mars": "Marte",
    "Jupiter": "Júpiter",
    "Saturn": "Saturno",
    "Uranus": "Urano",
    "Neptune": "Netuno",
    "Pluto": "Plutão"
}

# Parâmetros do jogo
DEFAULT_SOUND_VOLUME = 0.5
SOUND_FADEOUT_TIME = 500  # ms

# Parâmetros da espaçonave
SPACECRAFT_MAX_LIVES = 3
SPACECRAFT_INVULNERABILITY_TIME = 90  # quadros (1.5s a 60fps)
SPACECRAFT_KNOCKBACK = -3.5

# Limiares de progressão de nível - pontos necessários para avançar para o próximo planeta
# Movido para src.planet_data

# Temporização de obstáculos e colecionáveis
DEFAULT_OBSTACLE_SPAWN_RATE = 2500  # ms
DEFAULT_COLLECTIBLE_SPAWN_RATE = 3000  # ms

# Duração da transição
TRANSITION_DURATION = 180  # quadros (3s a 60fps)

# Duração da arma
WEAPON_DURATION = 600  # quadros (10s a 60fps)