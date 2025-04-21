import pygame
import sys
import random
import math
from src.spacecraft import Spacecraft
from src.obstacle import Obstacle
from src.collectible import Collectible
from src.planet import Planet
from src.highscore import HighScore
from src.nova_ai import NovaAI
from src.quiz import Quiz

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FLOOR_HEIGHT = 100
GAME_FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)
COUNTDOWN_FONT = pygame.font.Font(None, 180)  # Larger font for countdown

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
TRANSITION = 3
QUIZ = 4
QUIZ_FAILURE = 5  # New state for quiz failure delay

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Project Blue Nova: Solar System Explorer")
clock = pygame.time.Clock()

# Load assets
try:
    # Load sounds
    thrust_sound = pygame.mixer.Sound("assets/sounds/flap.wav")
    score_sound = pygame.mixer.Sound("assets/sounds/score.wav")
    hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
    
except pygame.error as e:
    print(f"Could not load asset: {e}")
    pygame.quit()
    sys.exit()

# Define planet progression and quiz questions
def create_planet_data():
    """Create data for all planets in the game"""
    planet_data = [
        {
            "name": "Earth",
            "gravity_factor": 100,  # Base gravity (g = 1.0)
            "background_color": (25, 25, 112),  # Midnight blue
            "obstacle_count": 6,  # Updated from 4 to 6
            "quiz_questions": [
                {
                    "question": "What percentage of Earth is covered by water?",
                    "options": ["51%", "61%", "71%", "81%"],
                    "answer": 2  # 71% (0-based index)
                },
                {
                    "question": "Earth's atmosphere is mostly composed of which gas?",
                    "options": ["Oxygen", "Carbon Dioxide", "Hydrogen", "Nitrogen"],
                    "answer": 3  # Nitrogen
                },
                {
                    "question": "How long does it take for Earth to rotate once on its axis?",
                    "options": ["12 hours", "24 hours", "365 days", "28 days"],
                    "answer": 1  # 24 hours
                }
            ]
        },
        {
            "name": "Mercury",
            "gravity_factor": 40,  # Updated from 38 to 40 (g = 0.4)
            "background_color": (70, 50, 40),  # Brown
            "obstacle_count": 2,  # Updated from 5 to 2
            "quiz_questions": [
                {
                    "question": "Mercury is the _____ planet from the Sun.",
                    "options": ["First", "Second", "Third", "Fourth"],
                    "answer": 0  # First
                },
                {
                    "question": "One day on Mercury is equivalent to about how many Earth days?",
                    "options": ["29 days", "59 days", "88 days", "176 days"],
                    "answer": 1  # 59 days
                },
                {
                    "question": "Mercury's surface temperature can reach up to:",
                    "options": ["100°C", "230°C", "430°C", "530°C"],
                    "answer": 2  # 430°C
                }
            ]
        },
        {
            "name": "Venus",
            "gravity_factor": 90,  # Unchanged (g = 0.9)
            "background_color": (140, 90, 40),  # Amber
            "obstacle_count": 4,  # Updated from 6 to 4
            "quiz_questions": [
                {
                    "question": "Venus rotates in which direction?",
                    "options": ["Same as Earth", "Opposite to Earth", "It doesn't rotate", "Randomly changes"],
                    "answer": 1  # Opposite to Earth (retrograde)
                },
                {
                    "question": "Venus's atmosphere is primarily composed of:",
                    "options": ["Nitrogen", "Carbon Dioxide", "Sulfuric Acid", "Methane"],
                    "answer": 1  # Carbon Dioxide
                },
                {
                    "question": "Venus is often called Earth's sister planet because:",
                    "options": ["It has oceans", "Similar size and mass", "It has life", "Same orbit time"],
                    "answer": 1  # Similar size and mass
                }
            ]
        },
        {
            "name": "Moon",
            "gravity_factor": 16,  # Updated from 16.6 to 16 (g = 0.16)
            "background_color": (20, 20, 20),  # Very dark gray
            "obstacle_count": 2,  # Updated from 3 to 2
            "quiz_questions": [
                {
                    "question": "How far is the Moon from Earth on average?",
                    "options": ["184,000 km", "238,000 km", "384,000 km", "584,000 km"],
                    "answer": 2  # 384,000 km
                },
                {
                    "question": "The first human to walk on the Moon was:",
                    "options": ["Buzz Aldrin", "Neil Armstrong", "Yuri Gagarin", "Alan Shepard"],
                    "answer": 1  # Neil Armstrong
                },
                {
                    "question": "What causes the Moon's phases?",
                    "options": ["Earth's shadow", "The Sun's position", "Moon's rotation", "Clouds on the Moon"],
                    "answer": 1  # The Sun's position
                }
            ]
        },
        {
            "name": "Mars",
            "gravity_factor": 40,  # Updated from 38 to 40 (g = 0.4)
            "background_color": (150, 70, 40),  # Rust red
            "obstacle_count": 3,  # Updated from 5 to 3
            "quiz_questions": [
                {
                    "question": "What gives Mars its distinctive red color?",
                    "options": ["Plant life", "Iron oxide (rust)", "Carbon dioxide", "Reflected sunlight"],
                    "answer": 1  # Iron oxide
                },
                {
                    "question": "How many moons does Mars have?",
                    "options": ["None", "One", "Two", "Three"],
                    "answer": 2  # Two (Phobos and Deimos)
                },
                {
                    "question": "What is the name of the largest volcano on Mars?",
                    "options": ["Mauna Loa", "Olympus Mons", "Mount Everest", "Mons Huygens"],
                    "answer": 1  # Olympus Mons
                }
            ]
        },
        {
            "name": "Jupiter",
            "gravity_factor": 240,  # Unchanged (g = 2.4)
            "background_color": (210, 140, 70),  # Tan
            "obstacle_count": 20,  # Updated from 8 to 20
            "quiz_questions": [
                {
                    "question": "What is Jupiter primarily made of?",
                    "options": ["Rock and metal", "Water and ice", "Hydrogen and helium", "Carbon dioxide"],
                    "answer": 2  # Hydrogen and helium
                },
                {
                    "question": "What is the Great Red Spot on Jupiter?",
                    "options": ["A volcano", "A dust storm", "A hurricane-like storm", "An impact crater"],
                    "answer": 2  # A hurricane-like storm
                },
                {
                    "question": "Jupiter has the shortest day of any planet. How long is it?",
                    "options": ["6 hours", "10 hours", "14 hours", "18 hours"],
                    "answer": 1  # ~10 hours
                }
            ]
        },
        {
            "name": "Saturn",
            "gravity_factor": 110,  # Unchanged (g = 1.1)
            "background_color": (180, 150, 100),  # Light tan
            "obstacle_count": 15,  # Updated from 7 to 15
            "quiz_questions": [
                {
                    "question": "What are Saturn's rings primarily made of?",
                    "options": ["Gas", "Dust", "Rock and metal", "Ice particles"],
                    "answer": 3  # Ice particles
                },
                {
                    "question": "How many major rings does Saturn have?",
                    "options": ["3", "5", "7", "9"],
                    "answer": 2  # 7 major rings
                },
                {
                    "question": "Saturn is the only planet that could float in water because:",
                    "options": ["It's hollow", "It's very small", "Its density is less than water", "It has helium"],
                    "answer": 2  # Low density
                }
            ]
        },
        {
            "name": "Uranus",
            "gravity_factor": 90,  # Unchanged (g = 0.9)
            "background_color": (140, 210, 210),  # Cyan
            "obstacle_count": 12,  # Updated from 6 to 12
            "quiz_questions": [
                {
                    "question": "Uranus rotates on its side with an axial tilt of about:",
                    "options": ["23 degrees", "45 degrees", "72 degrees", "98 degrees"],
                    "answer": 3  # 98 degrees
                },
                {
                    "question": "What gives Uranus its blue-green color?",
                    "options": ["Water", "Methane", "Ammonia", "Nitrogen"],
                    "answer": 1  # Methane
                },
                {
                    "question": "Uranus was the first planet discovered using a:",
                    "options": ["Naked eye", "Telescope", "Space probe", "Radio telescope"],
                    "answer": 1  # Telescope
                }
            ]
        },
        {
            "name": "Neptune",
            "gravity_factor": 110,  # Unchanged (g = 1.1)
            "background_color": (30, 50, 180),  # Deep blue
            "obstacle_count": 11,  # Updated from 7 to 11
            "quiz_questions": [
                {
                    "question": "Neptune was discovered based on mathematical predictions in:",
                    "options": ["1646", "1746", "1846", "1946"],
                    "answer": 2  # 1846
                },
                {
                    "question": "What is the Great Dark Spot on Neptune?",
                    "options": ["An ocean", "A storm system", "A crater", "A shadow"],
                    "answer": 1  # A storm system
                },
                {
                    "question": "Neptune's largest moon is:",
                    "options": ["Triton", "Nereid", "Proteus", "Larissa"],
                    "answer": 0  # Triton
                }
            ]
        },
        {
            "name": "Pluto",
            "gravity_factor": 6,  # g = 0.06
            "background_color": (50, 50, 80),  # Dark slate blue
            "obstacle_count": 1,  # Terminal level with 1 obstacle
            "quiz_questions": [
                {
                    "question": "In what year was Pluto reclassified as a dwarf planet?",
                    "options": ["2000", "2006", "2010", "2015"],
                    "answer": 1  # 2006
                },
                {
                    "question": "What NASA spacecraft provided the first close-up images of Pluto?",
                    "options": ["Voyager", "New Horizons", "Cassini", "Juno"],
                    "answer": 1  # New Horizons
                },
                {
                    "question": "Pluto's largest moon is called:",
                    "options": ["Hydra", "Nix", "Charon", "Kerberos"],
                    "answer": 2  # Charon
                }
            ]
        }
    ]
    
    return planet_data

class Game:
    def __init__(self):
        self.state = MENU
        self.score = 0
        self.high_score_manager = HighScore()
        self.high_score = self.high_score_manager.get()
        
        # Create planet data
        self.planet_data = create_planet_data()
        self.planets = [Planet(data["name"], 
                              data["gravity_factor"], 
                              data["background_color"], 
                              data["obstacle_count"], 
                              data["quiz_questions"]) 
                       for data in self.planet_data]
        
        # Start at Earth
        self.current_planet_index = 0
        self.current_planet = self.planets[self.current_planet_index]
        
        # Spacecraft setup
        self.spacecraft_color = "silver"  # Default color
        self.spacecraft = Spacecraft(100, SCREEN_HEIGHT // 2, self.spacecraft_color)
        self.available_colors = list(Spacecraft.COLORS.keys())
        self.current_color_index = 0
        
        # Game elements
        self.obstacles = []
        self.collectibles = []
        self.last_obstacle_time = pygame.time.get_ticks()
        self.last_collectible_time = pygame.time.get_ticks()
        self.floor_x = 0
        
        # Obstacle and collectible timing
        self.obstacle_spawn_rate = 2000  # milliseconds
        self.collectible_spawn_rate = 3000  # milliseconds
        
        # Game progression
        self.obstacle_speed = 3
        self.weapon_active = False
        self.weapon_timer = 0
        
        # Score thresholds for automatic level progression
        self.level_progression_thresholds = {
            "Earth": 6,   # 6 points needed for Earth (matching the obstacle count)
            "Mercury": 2, # 2 points needed for Mercury
            "Venus": 4,   # 4 points needed for Venus
            "Moon": 2,    # 2 points needed for Moon
            "Mars": 3,    # 3 points needed for Mars
            "Jupiter": 20, # 20 points needed for Jupiter
            "Saturn": 15,  # 15 points needed for Saturn
            "Uranus": 12,  # 12 points needed for Uranus
            "Neptune": 11, # 11 points needed for Neptune
            "Pluto": 1,    # 1 point needed for Pluto (terminal level)
        }
        
        # NOVA AI assistant
        self.nova = NovaAI(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Quiz system
        self.quiz = Quiz(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Transition screen
        self.transition_time = 0
        self.transition_duration = 180  # 3 seconds at 60fps
        
        # Difficulty progression
        self.difficulty_multiplier = 1.0
        
        # Enhanced visuals
        self.stars = self._generate_stars(100)
        
        self.quiz_failure_timer = 0  # Timer for quiz failure delay
        self.last_countdown_number = 0  # Last displayed countdown number
        
    def _generate_stars(self, count):
        """Generate stars for the background"""
        stars = []
        for _ in range(count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT - FLOOR_HEIGHT)
            size = random.uniform(0.5, 2.0)
            brightness = random.randint(150, 255)
            twinkle_speed = random.uniform(0.02, 0.1)
            phase = random.uniform(0, 2 * math.pi)
            stars.append({
                "x": x,
                "y": y,
                "size": size,
                "brightness": brightness,
                "base_brightness": brightness,
                "twinkle_speed": twinkle_speed,
                "phase": phase
            })
        return stars
        
    def reset(self, new_planet=False):
        """Reset the game, optionally switching to a new planet"""
        self.state = PLAYING
        self.weapon_active = False
        self.weapon_timer = 0
        
        if new_planet:
            # Remember the score for progression
            previous_score = self.score
            # Reset score for the new planet
            self.score = 0
            # Update difficulty based on planet index
            self.difficulty_multiplier = 1.0 + (self.current_planet_index * 0.1)
        else:
            # Fresh start
            self.score = 0
            self.current_planet_index = 0
            self.current_planet = self.planets[self.current_planet_index]
            self.difficulty_multiplier = 1.0
            
        # Reset spacecraft position
        self.spacecraft = Spacecraft(100, SCREEN_HEIGHT // 2, self.spacecraft_color)
        
        # Clear all obstacles and collectibles
        self.obstacles = []
        self.collectibles = []
        self.last_obstacle_time = pygame.time.get_ticks()
        self.last_collectible_time = pygame.time.get_ticks()
        
        # Base difficulty adjusted by planet and progression
        self.obstacle_speed = 3 * self.difficulty_multiplier
        self.obstacle_spawn_rate = int(2000 / self.difficulty_multiplier)
        self.collectible_spawn_rate = int(3000 / self.difficulty_multiplier)
        
        # NOVA AI should alert about gravity
        if new_planet:
            self.nova.alert_gravity_change(
                self.current_planet.name, 
                self.current_planet.gravity_factor
            )
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if self.state == QUIZ or self.state == QUIZ_FAILURE:
                    # Pass events to quiz system only if in QUIZ state (not in QUIZ_FAILURE)
                    if self.state == QUIZ:
                        self.quiz.handle_event(event)
                else:
                    if event.key == pygame.K_SPACE:
                        if self.state == MENU:
                            self.reset()
                        elif self.state == PLAYING:
                            self.spacecraft.thrust()
                            thrust_sound.play()
                        elif self.state == GAME_OVER:
                            self.reset()
                        elif self.state == TRANSITION:
                            # Skip transition and force start game on new planet
                            self.reset(new_planet=True)
                    
                    # Change spacecraft color with C key in menu
                    if event.key == pygame.K_c and self.state == MENU:
                        self.current_color_index = (self.current_color_index + 1) % len(self.available_colors)
                        self.spacecraft_color = self.available_colors[self.current_color_index]
                        self.spacecraft.change_color(self.spacecraft_color)
                    
                    # Activate weapon with W key if available
                    if event.key == pygame.K_w and self.state == PLAYING and self.weapon_active:
                        self._use_weapon()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.state == QUIZ or self.state == QUIZ_FAILURE:
                        # Pass events to quiz system only if in QUIZ state (not in QUIZ_FAILURE)
                        if self.state == QUIZ:
                            self.quiz.handle_event(event)
                    else:
                        if self.state == MENU:
                            self.reset()
                        elif self.state == PLAYING:
                            self.spacecraft.thrust()
                            thrust_sound.play()
                        elif self.state == GAME_OVER:
                            self.reset()
                        elif self.state == TRANSITION:
                            # Skip transition and force start game on new planet
                            self.reset(new_planet=True)
    
    def _use_weapon(self):
        """Use weapon to destroy obstacles"""
        if not self.weapon_active:
            return
            
        # Find the obstacle closest to the spacecraft that's in front of it
        target_obstacle = None
        min_distance = float('inf')
        
        for obstacle in self.obstacles:
            # Only target obstacles in front of the spacecraft
            if obstacle.x > self.spacecraft.x:
                distance = obstacle.x - self.spacecraft.x
                if distance < min_distance:
                    min_distance = distance
                    target_obstacle = obstacle
        
        if target_obstacle:
            # Remove the obstacle and award points
            self.obstacles.remove(target_obstacle)
            self.score += 2
            self.nova.show_message("Obstacle destroyed!", "alert")
            # Check for progression to next planet based on new score
            current_threshold = self.level_progression_thresholds.get(
                self.current_planet.name,
                10  # Default threshold for planets not specified
            )
            if self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                next_planet = self.planets[self.current_planet_index + 1]
                self.nova.show_message(f"Auto-navigation engaged! Heading to {next_planet.name}!", "excited")
                # Begin quiz for planet advancement
                self._start_quiz()
    
    def update(self):
        # Update stars (twinkle effect)
        for star in self.stars:
            star["phase"] += star["twinkle_speed"]
            twinkle_factor = 0.5 + 0.5 * math.sin(star["phase"])
            star["brightness"] = int(star["base_brightness"] * twinkle_factor)
        
        # Update NOVA AI
        self.nova.update()
        
        if self.state == PLAYING:
            # Update spacecraft with current planet's gravity
            self.spacecraft.update(self.current_planet.gravity)
            
            # Generate obstacles
            current_time = pygame.time.get_ticks()
            if current_time - self.last_obstacle_time > self.obstacle_spawn_rate:
                gap_y = random.randint(200, SCREEN_HEIGHT - FLOOR_HEIGHT - 150)
                obstacle_type = random.choice(list(Obstacle.TYPES.keys()))
                
                # Create a new obstacle
                new_obstacle = Obstacle(SCREEN_WIDTH, gap_y, self.obstacle_speed, obstacle_type)
                self.obstacles.append(new_obstacle)
                self.last_obstacle_time = current_time
                
                # Occasionally have NOVA warn about obstacles
                if random.random() < 0.3:  # 30% chance
                    self.nova.react_to_obstacle(obstacle_type)
            
            # Generate collectibles (data or weapon)
            if current_time - self.last_collectible_time > self.collectible_spawn_rate:
                # Place collectible in a safe location
                x = SCREEN_WIDTH
                y = random.randint(100, SCREEN_HEIGHT - FLOOR_HEIGHT - 50)
                # Determine collectible type (90% data, 10% weapon)
                if self.weapon_active or random.random() < 0.9:
                    collectible_type = "data"
                else:
                    collectible_type = "weapon"
                self.collectibles.append(Collectible(x, y, collectible_type))
                self.last_collectible_time = current_time
            
            # Update obstacles and check for score
            for obstacle in self.obstacles:
                obstacle.update()
                
                # Score when passing obstacle
                if not obstacle.scored and obstacle.x + obstacle.WIDTH < self.spacecraft.x:
                    self.score += 1
                    obstacle.scored = True
                    score_sound.play()
                    
                    # Get the threshold for the current planet or use default
                    current_threshold = self.level_progression_thresholds.get(
                        self.current_planet.name, 
                        10  # Default threshold for planets not specified
                    )
                    
                    # Check if we've hit or exceeded the score threshold to automatically progress
                    if self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                        # NOVA announces automatic progression
                        next_planet = self.planets[self.current_planet_index + 1]
                        self.nova.show_message(f"Auto-navigation engaged! Heading to {next_planet.name}!", "excited")
                        
                        # Start quiz without incrementing planet index yet - let the quiz handle progression
                        self._start_quiz()
            
            # Update collectibles
            for collectible in list(self.collectibles):
                collectible.update()
                collectible.x -= self.obstacle_speed  # Move at same speed as obstacles
                
                # Check collision with spacecraft
                if collectible.check_collision(self.spacecraft):
                    # Apply collectible effect
                    effect = collectible.get_effect()
                    
                    if effect["effect"] == "info":
                        # Show planet info
                        self.nova.give_random_fact(self.current_planet.name)
                        self.score += effect["value"]
                        
                        # Check if adding points triggered level progression
                        current_threshold = self.level_progression_thresholds.get(
                            self.current_planet.name, 
                            10  # Default threshold for planets not specified
                        )
                        
                        # Check for automatic progression after collecting points
                        if self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                            # NOVA announces automatic progression
                            next_planet = self.planets[self.current_planet_index + 1]
                            self.nova.show_message(f"Auto-navigation engaged! Heading to {next_planet.name}!", "excited")
                            
                            # Start quiz without incrementing planet index yet - let the quiz handle progression
                            self._start_quiz()
                            break  # Exit the loop to avoid processing more collectibles
                    elif effect["effect"] == "time":
                        # Extend play time (add score)
                        self.score += effect["value"]
                        self.nova.react_to_discovery("fuel")
                        
                        # Check if adding points triggered level progression
                        current_threshold = self.level_progression_thresholds.get(
                            self.current_planet.name, 
                            10  # Default threshold for planets not specified
                        )
                        
                        # Check for automatic progression after collecting points
                        if self.score >= current_threshold and self.current_planet_index < len(self.planets) - 1:
                            # NOVA announces automatic progression
                            next_planet = self.planets[self.current_planet_index + 1]
                            self.nova.show_message(f"Auto-navigation engaged! Heading to {next_planet.name}!", "excited")
                            
                            # Start quiz without incrementing planet index yet - let the quiz handle progression
                            self._start_quiz()
                            break  # Exit the loop to avoid processing more collectibles
                    elif effect["effect"] == "attack":
                        # Enable weapon temporarily
                        self.weapon_active = True
                        self.weapon_timer = 600  # 10 seconds at 60fps
                        self.nova.react_to_discovery("weapon")
                    
                    # Remove collected item
                    self.collectibles.remove(collectible)
            
            # Update weapon timer
            if self.weapon_active:
                self.weapon_timer -= 1
                if self.weapon_timer <= 0:
                    self.weapon_active = False
                    self.nova.show_message("Defensive systems offline", "normal")
            
            # Remove off-screen obstacles and collectibles
            self.obstacles = [obs for obs in self.obstacles if obs.x > -obs.WIDTH]
            self.collectibles = [col for col in self.collectibles if col.x > -col.WIDTH]
            
            # Check for collisions
            if self.check_collision():
                hit_sound.play()
                self.state = GAME_OVER
                if self.score > self.high_score_manager.get():
                    self.high_score = self.score
                    self.high_score_manager.save(self.score)
            
            # Move floor
            self.floor_x = (self.floor_x - self.obstacle_speed) % SCREEN_WIDTH
            
        elif self.state == TRANSITION:
            # Update transition screen
            self.transition_time += 1
            if self.transition_time >= self.transition_duration:
                # Transition complete, start game on new planet
                self.reset(new_planet=True)
                
        elif self.state == QUIZ:
            # Update quiz
            self.quiz.update()
            
            # Check if quiz is complete
            if self.quiz.is_complete():
                if self.quiz.is_correct():
                    # Proceed to next planet
                    self._start_transition()
                else:
                    # Failed quiz, set 3-second delay before returning to gameplay
                    self.state = QUIZ_FAILURE
                    self.quiz_failure_timer = 180  # 3 seconds at 60fps
                    self.last_countdown_number = 3  # Start countdown from 3
                    # Add a message from NOVA about the quiz failure
                    self.nova.show_message("Quiz failed! Returning to orbit in...", "alert")
        
        elif self.state == QUIZ_FAILURE:
            # Update quiz failure delay timer
            self.quiz_failure_timer -= 1
            
            # Check current countdown number
            # Convert remaining frames to seconds (ceil)
            current_countdown = math.ceil(self.quiz_failure_timer / 60)
            
            # If countdown number changed, play a sound effect
            if current_countdown < self.last_countdown_number and current_countdown >= 0:
                self.last_countdown_number = current_countdown
                score_sound.play()  # Reuse the score sound for countdown
                
                # Add a message from NOVA about the countdown
                if current_countdown > 0:
                    self.nova.show_message(f"Returning to orbit in {current_countdown}...", "alert")
            
            if self.quiz_failure_timer <= 0:
                # Delay complete, return to gameplay
                self.state = PLAYING
                self.nova.show_message("Back to orbital flight! Continue exploring.", "info")
                self.last_countdown_number = 0  # Reset for next time
    
    def _start_quiz(self):
        """Start a quiz for the current planet"""
        self.state = QUIZ
        
        # Reset countdown number tracker
        self.last_countdown_number = 2
        
        # Select a random quiz question for this planet
        question_data = random.choice(self.current_planet.quiz_questions)
        
        # Start the quiz
        self.quiz.start_quiz(
            question_data["question"],
            question_data["options"],
            question_data["answer"]
        )
    
    def _start_transition(self):
        """Start transition to next planet"""
        self.state = TRANSITION
        self.transition_time = 0
        
        # Increment planet index to advance to the next planet (only happens after passing a quiz)
        self.current_planet_index += 1
        
        # Ensure current_planet_index is valid
        if self.current_planet_index >= len(self.planets):
            # Player reached the end of all planets, show game over
            self.state = GAME_OVER
            if self.score > self.high_score_manager.get():
                self.high_score = self.score
                self.high_score_manager.save(self.score)
            return
        
        # Make sure we're using the correct planet after the quiz
        self.current_planet = self.planets[self.current_planet_index]
        
        # NOVA shows excitement about new planet
        self.nova.show_message(f"Entering {self.current_planet.name} orbit!", "excited")
    
    def check_collision(self):
        # Check floor and ceiling collision
        if self.spacecraft.y <= 0 or self.spacecraft.y + self.spacecraft.HEIGHT >= SCREEN_HEIGHT - FLOOR_HEIGHT:
            return True
        
        # Check obstacle collision
        for obstacle in self.obstacles:
            # Top obstacle collision
            if (self.spacecraft.x + self.spacecraft.WIDTH > obstacle.x and 
                self.spacecraft.x < obstacle.x + obstacle.WIDTH and 
                self.spacecraft.y < obstacle.gap_y - obstacle.GAP // 2):
                return True
            
            # Bottom obstacle collision
            if (self.spacecraft.x + self.spacecraft.WIDTH > obstacle.x and 
                self.spacecraft.x < obstacle.x + obstacle.WIDTH and 
                self.spacecraft.y + self.spacecraft.HEIGHT > obstacle.gap_y + obstacle.GAP // 2):
                return True
        
        return False
    
    def draw(self):
        # Create a base dark background for space
        screen.fill((0, 0, 20))
        
        # Draw stars based on current planet (foreground stars)
        for star in self.stars:
            # Draw star with current brightness
            color = (star["brightness"], star["brightness"], star["brightness"])
            pygame.draw.circle(screen, color, (int(star["x"]), int(star["y"])), star["size"])
        
        # Apply planet's background color as a transparent overlay
        bg_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        bg_color = (*self.current_planet.background_color, 100)  # Add alpha
        bg_overlay.fill(bg_color)
        screen.blit(bg_overlay, (0, 0))
        
        # Draw different screens based on game state
        if self.state == PLAYING or self.state == MENU or self.state == GAME_OVER or self.state == QUIZ_FAILURE:
            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(screen)
            
            # Draw collectibles
            for collectible in self.collectibles:
                collectible.draw(screen)
            
            # Draw floor/ground
            self.current_planet.draw_ground(screen, self.floor_x, SCREEN_HEIGHT)
            
            # Draw spacecraft
            self.spacecraft.draw(screen)
            
            # Draw the current planet name and player score
            if self.state != MENU:
                # Left-side information (unchanged)
                planet_text = SMALL_FONT.render(f"Planet: {self.current_planet.name}", True, (255, 255, 255))
                screen.blit(planet_text, (20, 20))
                
                # Get threshold for current planet
                current_threshold = self.level_progression_thresholds.get(
                    self.current_planet.name, 
                    10  # Default threshold
                )
                
                score_text = SMALL_FONT.render(f"Score: {self.score}/{current_threshold}", True, (255, 255, 255))
                screen.blit(score_text, (20, 50))
                
                high_score_text = SMALL_FONT.render(f"High Score: {self.high_score_manager.get()}", True, (255, 255, 255))
                screen.blit(high_score_text, (20, 80))
                
                # Draw weapon status at top-center if active (moved from right side)
                if self.weapon_active:
                    weapon_time = self.weapon_timer // 60  # Convert to seconds
                    weapon_text = SMALL_FONT.render(f"Weapon Active: {weapon_time}s", True, (255, 100, 100))
                    screen.blit(weapon_text, (SCREEN_WIDTH // 2 - weapon_text.get_width() // 2, 20))
            
            # Draw NOVA AI assistant (blue circle)
            self.nova.draw(screen)
            # If quiz failed, overlay large countdown before resuming
            if self.state == QUIZ_FAILURE and self.quiz_failure_timer > 0:
                # Calculate countdown seconds
                countdown = math.ceil(self.quiz_failure_timer / 60)
                # Render large countdown number
                text_surf = COUNTDOWN_FONT.render(str(countdown), True, (255, 255, 255))
                # Center on screen
                screen.blit(
                    text_surf,
                    (
                        SCREEN_WIDTH // 2 - text_surf.get_width() // 2,
                        SCREEN_HEIGHT // 2 - text_surf.get_height() // 2
                    )
                )
            
            # Draw menu screen
            if self.state == MENU:
                # Semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                
                title_text = GAME_FONT.render("PROJECT BLUE NOVA", True, (255, 255, 255))
                subtitle_text = SMALL_FONT.render("Solar System Explorer", True, (200, 200, 255))
                instruction_text = GAME_FONT.render("Press SPACE to Start", True, (255, 255, 255))
                color_text = GAME_FONT.render(f"Spacecraft: {self.spacecraft_color.capitalize()}", True, (255, 255, 255))
                color_instruction = SMALL_FONT.render("Press C to change color", True, (255, 255, 255))
                
                screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 180))
                screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 220))
                screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 280))
                screen.blit(color_text, (SCREEN_WIDTH // 2 - color_text.get_width() // 2, 330))
                screen.blit(color_instruction, (SCREEN_WIDTH // 2 - color_instruction.get_width() // 2, 370))
                
                # Display controls
                controls_title = SMALL_FONT.render("Controls:", True, (255, 255, 255))
                controls_space = SMALL_FONT.render("SPACE - Thrust", True, (200, 200, 200))
                controls_w = SMALL_FONT.render("W - Use Weapon (when available)", True, (200, 200, 200))
                
                controls_y = SCREEN_HEIGHT - 120
                screen.blit(controls_title, (SCREEN_WIDTH // 2 - controls_title.get_width() // 2, controls_y))
                screen.blit(controls_space, (SCREEN_WIDTH // 2 - controls_space.get_width() // 2, controls_y + 30))
                screen.blit(controls_w, (SCREEN_WIDTH // 2 - controls_w.get_width() // 2, controls_y + 60))
            
            # Draw game over screen
            if self.state == GAME_OVER:
                # Semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                
                game_over_text = GAME_FONT.render("MISSION COMPLETE", True, (255, 215, 0))
                score_text = GAME_FONT.render(f"Final Score: {self.score}", True, (255, 255, 255))
                high_score_text = GAME_FONT.render(f"High Score: {self.high_score_manager.get()}", True, (255, 255, 255))
                restart_text = GAME_FONT.render("Press SPACE to Start New Mission", True, (255, 255, 255))
                
                # Calculate the furthest planet reached
                furthest_planet = self.planets[min(self.current_planet_index, len(self.planets) - 1)].name
                planet_text = GAME_FONT.render(f"Furthest Planet: {furthest_planet}", True, (255, 255, 255))
                
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
                screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 220))
                screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 270))
                screen.blit(planet_text, (SCREEN_WIDTH // 2 - planet_text.get_width() // 2, 320))
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))
        
        elif self.state == TRANSITION:
            # Draw transition screen
            
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))  # Darker overlay for text readability
            screen.blit(overlay, (0, 0))
            
            # Draw destination planet name
            planet_title = GAME_FONT.render(f"Welcome to {self.current_planet.name}", True, (255, 255, 255))
            screen.blit(planet_title, (SCREEN_WIDTH // 2 - planet_title.get_width() // 2, 100))
            
            # Draw gravity info
            gravity_text = GAME_FONT.render(f"Gravity: {self.current_planet.gravity_factor}% of Earth", True, (255, 255, 255))
            screen.blit(gravity_text, (SCREEN_WIDTH // 2 - gravity_text.get_width() // 2, 150))
            
            # Draw planet info text
            info_text = self.current_planet.get_info_text()
            # Wrap text to fit screen
            wrapped_lines = []
            words = info_text.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                test_surface = SMALL_FONT.render(test_line, True, (255, 255, 255))
                if test_surface.get_width() < SCREEN_WIDTH - 100:
                    line = test_line
                else:
                    wrapped_lines.append(line)
                    line = word + " "
            wrapped_lines.append(line)  # Add the last line
            
            # Draw wrapped text
            for i, line in enumerate(wrapped_lines):
                line_surface = SMALL_FONT.render(line, True, (200, 200, 255))
                screen.blit(line_surface, (SCREEN_WIDTH // 2 - line_surface.get_width() // 2, 220 + i * 30))
            
            # Draw progress indicator
            progress_text = SMALL_FONT.render(f"Planet {self.current_planet_index + 1} of {len(self.planets)}", True, (180, 180, 180))
            screen.blit(progress_text, (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, 350))
            
            # Draw continue prompt
            if self.transition_time > 60:  # Only show after 1 second
                continue_text = SMALL_FONT.render("Press SPACE to continue", True, (255, 255, 255))
                # Make it pulse
                alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
                continue_text.set_alpha(alpha)
                screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 450))
        
        elif self.state == QUIZ:
            # Draw quiz
            self.quiz.draw(screen)
        
        elif self.state == QUIZ_FAILURE:
            # Add a semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # More visible semi-transparent black
            screen.blit(overlay, (0, 0))
            
            # Calculate countdown number (2, 1)
            countdown_number = self.quiz_failure_timer // 60 + 1
            
            # Draw large countdown number
            if countdown_number > 0:
                # Add pulse effect - size oscillates slightly based on ticks
                pulse_factor = 1.0 + 0.15 * math.sin(pygame.time.get_ticks() * 0.01)
                pulse_size = int(180 * pulse_factor)
                
                # Use the global countdown font with the pulse effect
                countdown_font = pygame.font.Font(None, pulse_size)
                
                # Color also pulses slightly - more pronounced effect
                color_pulse = int(255 * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.015)))
                countdown_text = countdown_font.render(str(countdown_number), True, (255, color_pulse, color_pulse))
                countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                
                # Draw with enhanced glow effect
                glow_size = 12
                for offset_x in range(-glow_size, glow_size + 1, 3):
                    for offset_y in range(-glow_size, glow_size + 1, 3):
                        if offset_x == 0 and offset_y == 0:
                            continue
                        # Calculate distance for glow fade effect
                        distance = math.sqrt(offset_x**2 + offset_y**2)
                        alpha = int(120 * (1 - distance/glow_size))
                        if alpha <= 0:
                            continue
                            
                        glow_rect = countdown_rect.move(offset_x, offset_y)
                        glow_text = countdown_font.render(str(countdown_number), True, (80, 80, 220, alpha))
                        screen.blit(glow_text, glow_rect)
                
                # Draw main text
                screen.blit(countdown_text, countdown_rect)
                
                # Draw "Resuming..." text with pulsing effect
                resume_font = pygame.font.Font(None, 42)
                alpha_pulse = int(255 * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.008)))
                resume_text = resume_font.render("Returning to orbit...", True, (255, 255, 255))
                resume_text.set_alpha(alpha_pulse)
                resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
                screen.blit(resume_text, resume_rect)
        
        # Always draw NOVA AI assistant on top
        self.nova.draw(screen)

def main():
    # Create and start the game
    game = Game()
    
    # Game loop
    while True:
        game.handle_events()
        game.update()
        game.draw()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()