import pygame

def draw_normal_expression(surface, width, height):
    """
    Draws a simple happy face with gentle smile and neutral eyebrows
    
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
    
    eye_radius = width // 10
    eye_y_pos = center_y - height // 6
    left_eye_x = center_x - width // 4
    right_eye_x = center_x + width // 4
    
    # Draw eyes (slightly larger with pupil)
    # White part of eyes
    pygame.draw.circle(surface, white, (left_eye_x, eye_y_pos), eye_radius)
    pygame.draw.circle(surface, white, (right_eye_x, eye_y_pos), eye_radius)
    
    # Pupils
    pupil_radius = eye_radius // 2
    pygame.draw.circle(surface, black, (left_eye_x, eye_y_pos), pupil_radius)
    pygame.draw.circle(surface, black, (right_eye_x, eye_y_pos), pupil_radius)
    
    # Draw subtle highlight in eyes
    highlight_radius = pupil_radius // 3
    highlight_offset_x = pupil_radius // 3
    highlight_offset_y = pupil_radius // 3
    pygame.draw.circle(surface, white, 
                      (left_eye_x - highlight_offset_x, eye_y_pos - highlight_offset_y), 
                      highlight_radius)
    pygame.draw.circle(surface, white, 
                      (right_eye_x - highlight_offset_x, eye_y_pos - highlight_offset_y), 
                      highlight_radius)
    
    # Draw eyebrows (subtle, neutral position)
    eyebrow_length = eye_radius * 2
    eyebrow_thickness = max(2, height // 40)
    eyebrow_y = eye_y_pos - eye_radius - eyebrow_thickness
    
    # Left eyebrow
    pygame.draw.line(surface, black, 
                    (left_eye_x - eyebrow_length//2, eyebrow_y),
                    (left_eye_x + eyebrow_length//2, eyebrow_y),
                    eyebrow_thickness)
    
    # Right eyebrow
    pygame.draw.line(surface, black, 
                    (right_eye_x - eyebrow_length//2, eyebrow_y),
                    (right_eye_x + eyebrow_length//2, eyebrow_y),
                    eyebrow_thickness)
    
    # Draw smile (gentle curve)
    smile_rect = pygame.Rect(
        center_x - width//4,
        center_y,
        width//2,
        height//4
    )
    
    # Only draw bottom half of ellipse for smile
    pygame.draw.arc(surface, black, smile_rect, 0, 3.14, max(2, height // 30))
    
    return surface