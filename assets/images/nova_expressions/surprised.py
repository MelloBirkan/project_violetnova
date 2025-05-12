import pygame

def draw_surprised_expression(surface, width, height):
    """
    Draws a surprised face with wide eyes and O-shaped mouth
    
    Args:
        surface: The pygame surface to draw onto
        width: Width of the surface
        height: Height of the surface
    """
    # Clear the surface
    surface.fill((0, 0, 0, 0))  # Transparent
    
    # Define colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    
    # Calculate positions
    center_x = width // 2
    center_y = height // 2
    
    # Draw very wide eyes
    eye_radius = width // 8
    eye_y_pos = center_y - height // 6
    left_eye_x = center_x - width // 4
    right_eye_x = center_x + width // 4
    
    # White part of eyes (extra large for surprise)
    pygame.draw.circle(surface, white, (left_eye_x, eye_y_pos), eye_radius * 1.3)
    pygame.draw.circle(surface, white, (right_eye_x, eye_y_pos), eye_radius * 1.3)
    
    # Pupils (centered and small with surprise)
    pupil_radius = eye_radius // 2
    pygame.draw.circle(surface, black, (left_eye_x, eye_y_pos), pupil_radius)
    pygame.draw.circle(surface, black, (right_eye_x, eye_y_pos), pupil_radius)
    
    # Draw bright highlight in eyes
    highlight_radius = pupil_radius // 2
    highlight_offset_x = pupil_radius // 3
    highlight_offset_y = pupil_radius // 3
    pygame.draw.circle(surface, white, 
                      (left_eye_x - highlight_offset_x, eye_y_pos - highlight_offset_y), 
                      highlight_radius)
    pygame.draw.circle(surface, white, 
                      (right_eye_x - highlight_offset_x, eye_y_pos - highlight_offset_y), 
                      highlight_radius)
    
    # Draw high eyebrows (raised with surprise)
    eyebrow_length = eye_radius * 2
    eyebrow_thickness = max(2, height // 40)
    eyebrow_y = eye_y_pos - eye_radius * 2  # Very high position for surprise
    
    # Left eyebrow (highly raised)
    pygame.draw.line(surface, black, 
                    (left_eye_x - eyebrow_length//2, eyebrow_y),
                    (left_eye_x + eyebrow_length//2, eyebrow_y),
                    eyebrow_thickness)
    
    # Right eyebrow (highly raised)
    pygame.draw.line(surface, black, 
                    (right_eye_x - eyebrow_length//2, eyebrow_y),
                    (right_eye_x + eyebrow_length//2, eyebrow_y),
                    eyebrow_thickness)
    
    # Draw O-shaped mouth for surprise
    mouth_radius = width // 6
    mouth_y = center_y + height // 6
    
    # Outer circle
    pygame.draw.circle(surface, black, (center_x, mouth_y), mouth_radius, max(2, height // 30))
    
    # Inner white circle (slightly smaller)
    pygame.draw.circle(surface, white, (center_x, mouth_y), mouth_radius - max(2, height // 30))
    
    return surface