# Project Blue Nova: Solar System Explorer

A space-themed game where players navigate a spacecraft through our solar system, experiencing different gravity levels, collecting items, and learning about planets.

## Game Features

- **Solar System Exploration**: Visit all planets in our solar system - Earth, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, and Neptune
- **Variable Gravity**: Experience realistic gravity differences on each celestial body
- **Space Obstacles**: Navigate through asteroid fields, space debris, and solar storms
- **Collectible Items**: Gather data modules for points, fuel cells for extended gameplay, and weapons to destroy obstacles
- **NOVA AI Assistant**: Get scientific facts and alerts from your AI companion
- **Educational Quiz System**: Test your knowledge about planets to progress through the solar system
- **Dynamic Level Progression**: Travel through portals from one planet to the next

## Controls

- **SPACE**: Thrust (counteracts gravity)
- **W**: Use weapon (when available)
- **C**: Change spacecraft color (in menu)
- **ESC**: Quit the game

## Planet Progression

The game follows a realistic solar system order:

1. Earth (100% gravity)
2. Moon (16.6% gravity)
3. Mercury (38% gravity)
4. Venus (90% gravity)
5. Mars (38% gravity)
6. Jupiter (240% gravity)
7. Saturn (110% gravity)
8. Uranus (90% gravity)
9. Neptune (110% gravity)

## Educational Value

This game combines fun gameplay with educational content about our solar system:
- Learn about each planet's characteristics through the NOVA AI
- Test your knowledge with planet-specific quizzes to progress
- Experience different gravity levels as a teaching tool

## Requirements

- Python 3.x
- Pygame

## Installation and Running

1. Clone this repository
2. Install required packages: `pip install -r requirements.txt`
3. Run the game: `python main.py`

The main script will automatically check for dependencies and generate sound files if needed.

## Game Mechanics

- Your spacecraft constantly falls due to each planet's gravity
- Press SPACE or click to thrust upward
- Navigate through the gaps in the space obstacles
- Collect items for points and special abilities
- Each obstacle you pass awards one point
- Score enough points to unlock the portal to the next planet
- Answer a quiz question correctly to proceed to the next planet
- Game ends when your spacecraft hits an obstacle, the ground, or the ceiling

## Credits

Developed as an educational game project based on the Flappy Bird mechanics, but extensively enhanced with space exploration, educational elements, and variable physics.