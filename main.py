#!/usr/bin/env python3
"""
Project Blue Nova: Solar System Explorer - Main Entry Point
-----------------------------------
This script launches the Solar System exploration game.
"""

import os
import sys
import subprocess

def main():
    """Main entry point for the game"""
    print("Starting Project Blue Nova: Solar System Explorer...")
    
    # Check if requirements are installed
    try:
        import pygame
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if sound files exist
    sound_files = ["flap.wav", "score.wav", "hit.wav"]
    sound_dir = os.path.join("assets", "sounds")
    
    missing_sounds = [f for f in sound_files if not os.path.exists(os.path.join(sound_dir, f))]
    
    # If sound files are missing, generate them
    if missing_sounds:
        print("Generating sound files...")
        try:
            import src.create_sounds
            src.create_sounds.main()
        except Exception as e:
            print(f"Error generating sound files: {e}")
            print("You can manually generate sound files: python src/create_sounds.py")
    
    # Launch the game
    from src.main import main
    main()

if __name__ == "__main__":
    main()