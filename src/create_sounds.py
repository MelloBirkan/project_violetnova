import os
import pygame

def create_sound_directory():
    os.makedirs("assets/sounds", exist_ok=True)

def create_dummy_sound_file(filename):
    """Create an empty sound file that Pygame can load without errors"""
    sound_path = os.path.join("assets/sounds", filename)
    # Create a minimal valid .wav file (44 bytes header + 1 sample of silence)
    with open(sound_path, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write((36).to_bytes(4, byteorder='little'))  # File size - 8
        f.write(b'WAVE')
        
        # Format chunk
        f.write(b'fmt ')
        f.write((16).to_bytes(4, byteorder='little'))  # Chunk size
        f.write((1).to_bytes(2, byteorder='little'))   # PCM format
        f.write((1).to_bytes(2, byteorder='little'))   # Mono
        f.write((44100).to_bytes(4, byteorder='little'))  # Sample rate
        f.write((44100).to_bytes(4, byteorder='little'))  # Byte rate
        f.write((1).to_bytes(2, byteorder='little'))   # Block align
        f.write((8).to_bytes(2, byteorder='little'))   # Bits per sample
        
        # Data chunk
        f.write(b'data')
        f.write((1).to_bytes(4, byteorder='little'))   # Chunk size
        f.write((0).to_bytes(1, byteorder='little'))   # One sample of silence
    
    print(f"Created {filename}")

def main():
    """Create dummy sound files for the game"""
    create_sound_directory()
    
    # Generate simple sound files
    create_dummy_sound_file("flap.wav")
    create_dummy_sound_file("score.wav")
    create_dummy_sound_file("hit.wav")
    
    print("All sound files created successfully!")
    print("NOTE: These are silent placeholders. Replace with real sounds for a better experience.")

if __name__ == "__main__":
    main()