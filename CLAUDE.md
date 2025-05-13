# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Project Violetnova is an educational space-themed arcade game that teaches players about astronomy, space physics, and the gravitational differences between celestial bodies in our solar system. Players control a spacecraft navigating through obstacles while adapting to the unique gravity of each planet, from Mercury to Neptune.

## Commands

### Setup and Installation

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the game
python3 main.py
```

### Development

The main development files are located in the `/src` directory. There are no specific lint or test commands defined in the project.

## Code Architecture

### Core Game Loop

- `main.py`: Entry point that checks dependencies and starts the game
- `src/main.py`: Contains the main game loop and the `Game` class that manages game states, game mechanics, and rendering

### Game States

The game uses a state-based architecture with these primary states:
- `MENU`: Title screen
- `PLAYING`: Active gameplay
- `GAME_OVER`: End screen showing score
- `TRANSITION`: Screen when moving between planets
- `QUIZ`: Educational quizzes about each planet
- `QUIZ_FAILURE`: Cooldown period when player fails a quiz

### Key Components

1. **Player Character**
   - `spacecraft.py`: Implements the player-controlled spacecraft with physics, visualization, and animation

2. **Level Elements**
   - `obstacle.py`: Implements game obstacles with different themes (asteroid, debris, storm)
   - `collectible.py`: Items that give power-ups, points, or educational facts
   - `planet.py`: Defines planets with unique gravity, visuals, and educational content

3. **Educational Elements**
   - `quiz.py`: Interactive quiz system about space facts
   - `nova_ai.py`: AI assistant character that provides educational information

4. **Support Systems**
   - `highscore.py`: Manages game score persistence
   - `create_sounds.py`: Generates placeholder sound files

### Physics and Mechanics

The game implements a simplified physics system where:
- Each planet has a different gravity factor (relative to Earth's 1.0g)
- The spacecraft has thrust capabilities to counteract gravity
- Collision detection uses hitboxes for more accurate interactions
- Obstacle movement creates the game challenge

### Progression System

Players progress through the solar system by:
1. Achieving a score threshold specific to each planet
2. Successfully answering quiz questions about astronomy
3. Moving to planets with increasingly complex gravitational and obstacle patterns

## File Structure

- `/assets`: Contains images and sounds
- `/src`: Main game code
  - Core gameplay files (main.py, spacecraft.py, obstacle.py)
  - Educational content (planet.py, quiz.py, nova_ai.py)
  - Support systems (highscore.py, create_sounds.py)

## Game Controls

- **SPACE**: Thrust spacecraft upward
- **W**: Use weapon (when available)
- **C**: Change spacecraft color (in menu) or control mode (during gameplay)
- **ESC**: Exit game

## Translation Support

The game supports Brazilian Portuguese with translation dictionaries for planet names and other text elements. Translation mappings are defined in `src/main.py` and passed to various components.

## Development Directives

- Leave all the UI and comments in the code in Brazilian Portuguese.

## Memory Tracking

- Please ask the user  to run the game so I can test the changes I made.