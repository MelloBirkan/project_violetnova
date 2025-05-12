import pygame

# Screen configuration
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FLOOR_HEIGHT = 100

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
TRANSITION = 3
QUIZ = 4
QUIZ_FAILURE = 5

# Control modes
CONTROL_MODE_FLAPPY = 0  # Tap for thrust, Flappy Bird style
CONTROL_MODE_HOLD = 1    # Hold space for continuous thrust

# Font settings - these will be initialized later
GAME_FONT = None
SMALL_FONT = None
COUNTDOWN_FONT = None

# Font sizes
GAME_FONT_SIZE = 36
SMALL_FONT_SIZE = 24
COUNTDOWN_FONT_SIZE = 180

# Translation dictionaries
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

# Game parameters
DEFAULT_SOUND_VOLUME = 0.5
SOUND_FADEOUT_TIME = 500  # ms

# Spacecraft parameters
SPACECRAFT_MAX_LIVES = 3
SPACECRAFT_INVULNERABILITY_TIME = 90  # frames (1.5s at 60fps)
SPACECRAFT_KNOCKBACK = -3.5

# Level progression thresholds - points needed to advance to next planet
LEVEL_PROGRESSION_THRESHOLDS = {
    "Earth": 6,
    "Mercury": 2,
    "Venus": 4,
    "Moon": 2,
    "Mars": 3,
    "Jupiter": 20,
    "Saturn": 15,
    "Uranus": 12,
    "Neptune": 11,
    "Pluto": 1,
}

# Obstacle and collectible timing
DEFAULT_OBSTACLE_SPAWN_RATE = 2500  # ms
DEFAULT_COLLECTIBLE_SPAWN_RATE = 3000  # ms

# Transition duration
TRANSITION_DURATION = 180  # frames (3s at 60fps)

# Weapon duration
WEAPON_DURATION = 600  # frames (10s at 60fps)