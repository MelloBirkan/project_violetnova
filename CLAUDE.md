# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Project Violetnova is an educational space-themed arcade game that teaches players about astronomy, space physics, and the gravitational differences between celestial bodies in our solar system. Players control a spacecraft navigating through obstacles while adapting to the unique gravity of each planet, from Mercury to Neptune.

## Commands

### Setup and Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Development

The main development files are located in the `/src` directory. There are no specific lint or test commands defined in the project.

## Code Architecture

### Core Game Loop

- `main.py`: Entry point that checks dependencies and starts the game
- `src/main.py`: Contains the main game loop initialization
- `src/game.py`: Contains the `Game` class that manages game states, game mechanics, and rendering

### Game States

The game uses a state-based architecture with these primary states:
- `SPLASH`: Initial splash screen
- `MENU`: Title screen
- `PLAYING`: Active gameplay
- `GAME_OVER`: End screen showing score
- `TRANSITION`: Screen when moving between planets
- `QUIZ`: Educational quizzes about each planet
- `QUIZ_FAILURE`: Cooldown period when player fails a quiz
- `DIALOGUE`: Character dialogue sequences

### Key Components

1. **Player Character**
   - `spacecraft.py`: Implements the player-controlled spacecraft with physics, visualization, and animation
   - `violet.py`: The main character (a cat astronaut)

2. **Level Elements**
   - `obstacle.py`: Implements game obstacles with different themes (asteroid, debris, storm)
   - `collectible.py`: Items that give power-ups, points, or educational facts
   - `planet.py`: Defines planets with unique gravity, visuals, and educational content
   - `planet_data.py`: Contains planet data constants and progression thresholds

3. **Educational Elements**
   - `quiz.py`: Interactive quiz system about space facts
   - `nova_ai.py`: AI assistant character that provides educational information
   - `dialogue_manager.py`: Handles character interactions and educational dialogue

4. **Game Management**
   - `game.py`: Core game state management and orchestration
   - `state_manager.py`: Handles game state transitions and state-specific logic
   - `input_handler.py`: Processes user input for different game states
   - `ui_manager.py`: Handles UI drawing responsibilities
   - `game_mechanics.py`: Manages obstacles, collectibles, and game physics
   - `weapon_system.py`: Handles weapon functionality and targeting

5. **Support Systems**
   - `highscore.py`: Manages game score persistence
   - `sound_manager.py`: Handles audio playback
   - `visual_effects.py`: Manages visual effects and animations
   - `collision_manager.py`: Manages collision detection and handling
   - `portal.py`: Handles transitions between planets

### Physics and Mechanics

The game implements a simplified physics system where:
- Each planet has a different gravity factor (relative to Earth's 1.0g)
- The spacecraft has thrust capabilities to counteract gravity
- Collision detection uses hitboxes for more accurate interactions
- Obstacle movement creates the game challenge
- Weapons can be used to destroy obstacles when power-ups are collected

### Progression System

Players progress through the solar system by:
1. Achieving a score threshold specific to each planet
2. Successfully answering quiz questions about astronomy
3. Moving to planets with increasingly complex gravitational and obstacle patterns

## File Structure

- `/assets`: Contains images and sounds
  - `/images`: Game sprites and visual assets
    - `/nova_expressions`: Expression images for NOVA AI assistant
    - `/planets_sprites`: Planet-specific background and obstacle sprites
  - `/musics`: Background music for different planets
  - `/sounds`: Sound effects and welcome messages
- `/src`: Main game code
  - Core gameplay files (main.py, game.py, spacecraft.py, obstacle.py)
  - Educational content (planet.py, planet_data.py, quiz.py, nova_ai.py)
  - Game managers (state_manager.py, input_handler.py, ui_manager.py, game_mechanics.py, weapon_system.py)
  - Support systems (highscore.py, sound_manager.py, visual_effects.py, collision_manager.py)
  - Configuration (config.py)

## Game Controls

- **SPACE**: Thrust spacecraft upward
- **W**: Use weapon (when available)
- **C**: Change spacecraft color (in menu) or control mode (during gameplay)
- **ESC**: Exit game

## Control Modes

The game supports two control modes:
- **HOLD**: Hold the SPACE key for continuous thrust (default mode)
- **FLAPPY**: Tap the SPACE key for burst thrust (similar to Flappy Bird mechanics)

## Translation Support

The game supports Brazilian Portuguese with translation dictionaries for planet names and other text elements. Translation mappings are defined in `src/planet_data.py` and `src/config.py`, and passed to various components.

## Development Directives

- UI and comments in the code should be maintained in Brazilian Portuguese
- New educational content should be scientifically accurate
- Accessibility considerations should be maintained for color choices and text presentation

## Planet Configuration

Each planet in the game has:
- Unique gravity factor (relative to Earth's 1.0g)
- Custom background and obstacle sprites
- Educational quiz questions and facts (with explanations)
- Specific progression thresholds

## Game Difficulty Settings

The game has three difficulty levels (Easy, Medium, Hard) defined in `src/config.py`:
- Easy: 3 lives (max 5), checkpoints enabled, slower obstacles, higher chance of power-ups
- Medium: 1 life (max 3), no checkpoints, standard obstacle speed, moderate power-up chance
- Hard: 1 life, no checkpoints, no power-ups, faster obstacles

## Save System

The game uses a simple JSON-based save system to track:
- Last played planet (for resuming)
- Furthest planet reached (for progression)
- Checkpoints (when enabled in easy mode)

The save file is located at `planet_progress.json` in the root directory.

## Development Environment

- Python 3.8+ is required
- Pygame is the only external dependency
- The game is designed to run on Windows, macOS, and Linux

## Recent Development History

Recent work has focused on:
- Adding explanations to quiz questions to enhance educational value
- Translating UI elements and comments to Brazilian Portuguese
- Refining graphics and animations for improved visual appeal
- Implementing the complete solar system progression system
- Adding weapon system functionality for destroying obstacles
- Enhancing the difficulty settings and planet progression mechanics
- Implementing character dialogue for educational storytelling