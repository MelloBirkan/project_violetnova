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
DEFAULT_SOUND_VOLUME = 0.7
THRUST_SOUND_VOLUME = 0.1  # Volume reduzido para o som do propulsor
SOUND_FADEOUT_TIME = 500  # ms

# Parâmetros da espaçonave
SPACECRAFT_MAX_LIVES = 3
SPACECRAFT_INVULNERABILITY_TIME = 90  # quadros (1.5s a 60fps)

# Configurações do menu
MENU_OPTIONS = ["Jogar", "Dificuldade", "Configurações", "Créditos", "Sair"]
MENU_OPTION_SPACING = 50
MENU_START_Y = 280
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

# Durações do quiz
QUIZ_DURATION = 600  # quadros (10s a 60fps)
QUIZ_RESULT_DURATION = 120  # quadros (2s a 60fps)

# ================================
# Configurações de dificuldade
# ================================

# Níveis de dificuldade
DIFFICULTY_EASY = 0
DIFFICULTY_MEDIUM = 1
DIFFICULTY_HARD = 2

# Dificuldade padrão
DEFAULT_DIFFICULTY = DIFFICULTY_EASY  # Alterado para modo fácil

# Configurações específicas de cada dificuldade
DIFFICULTY_SETTINGS = {
    DIFFICULTY_EASY: {
        "lives": 3,
        "max_lives": 5,  # Permite acumular até 5 vidas
        "life_collectible_chance": 0.15,
        "weapon_collectible_chance": 0.05,
        "obstacle_distance_multiplier": 2.0,
        "save_checkpoint": True
    },
    DIFFICULTY_MEDIUM: {
        "lives": 1,
        "life_collectible_chance": 0.10,
        "weapon_collectible_chance": 0.05,
        "obstacle_distance_multiplier": 1.0,
        "save_checkpoint": False,
        "max_lives": 3
    },
    DIFFICULTY_HARD: {
        "lives": 1,
        "life_collectible_chance": 0.0,
        "weapon_collectible_chance": 0.01,
        "obstacle_distance_multiplier": 0.6,
        "save_checkpoint": False
    },
}

# Nomes exibidos para cada dificuldade
DIFFICULTY_NAMES = {
    DIFFICULTY_EASY: "Fácil",
    DIFFICULTY_MEDIUM: "Médio",
    DIFFICULTY_HARD: "Difícil",
}
