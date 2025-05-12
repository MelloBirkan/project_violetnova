import pygame

def draw_excited_expression(surface, width, height):
    """
    Draws an excited face with wide eyes and big smile
    
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
    
    eye_radius = width // 8
    eye_y_pos = center_y - height // 6
    left_eye_x = center_x - width // 4
    right_eye_x = center_x + width // 4
    
    # Draw eyes (wide with excitement)
    # White part of eyes (slightly larger for excited look)
    pygame.draw.circle(surface, white, (left_eye_x, eye_y_pos), eye_radius * 1.2)
    pygame.draw.circle(surface, white, (right_eye_x, eye_y_pos), eye_radius * 1.2)
    
    # Pupils (smaller to show excitement)
    pupil_radius = eye_radius // 2
    pygame.draw.circle(surface, black, (left_eye_x, eye_y_pos), pupil_radius)
    pygame.draw.circle(surface, black, (right_eye_x, eye_y_pos), pupil_radius)
    
    # Draw bright highlight in eyes
    highlight_radius = pupil_radius // 2
    highlight_offset_x = pupil_radius // 2
    highlight_offset_y = pupil_radius // 2
    pygame.draw.circle(surface, white, 
                      (left_eye_x - highlight_offset_x, eye_y_pos - highlight_offset_y), 
                      highlight_radius)
    pygame.draw.circle(surface, white, 
                      (right_eye_x - highlight_offset_x, eye_y_pos - highlight_offset_y), 
                      highlight_radius)
    
    # Draw eyebrows (raised with excitement)
    eyebrow_length = eye_radius * 2
    eyebrow_thickness = max(2, height // 40)
    eyebrow_y = eye_y_pos - eye_radius * 1.8  # Higher position for excitement
    
    # Left eyebrow (raised at outer edge)
    pygame.draw.line(surface, black, 
                    (left_eye_x - eyebrow_length//2, eyebrow_y + eyebrow_thickness),
                    (left_eye_x + eyebrow_length//2, eyebrow_y - eyebrow_thickness),
                    eyebrow_thickness)
    
    # Right eyebrow (raised at inner edge)
    pygame.draw.line(surface, black, 
                    (right_eye_x - eyebrow_length//2, eyebrow_y - eyebrow_thickness),
                    (right_eye_x + eyebrow_length//2, eyebrow_y + eyebrow_thickness),
                    eyebrow_thickness)
    
    # Draw big smile with teeth
    smile_rect = pygame.Rect(
        center_x - width//3,
        center_y - height//10,
        width//1.5,
        height//3
    )
    
    # Draw full smile outline
    pygame.draw.arc(surface, black, smile_rect, 0, 3.14, max(2, height // 30))
    
    # Add smile bottom line
    pygame.draw.line(surface, black,
                    (center_x - width//3, center_y + height//10),
                    (center_x + width//3, center_y + height//10),
                    max(2, height // 30))
    
    # Add simple teeth lines (3 vertical lines)
    teeth_width = width//10
    teeth_top = center_y
    teeth_bottom = center_y + height//10
    
    # Center tooth
    pygame.draw.line(surface, black,
                    (center_x, teeth_top),
                    (center_x, teeth_bottom),
                    max(1, height // 60))
    
    # Left tooth
    pygame.draw.line(surface, black,
                    (center_x - teeth_width, teeth_top),
                    (center_x - teeth_width, teeth_bottom),
                    max(1, height // 60))
    
    # Right tooth
    pygame.draw.line(surface, black,
                    (center_x + teeth_width, teeth_top),
                    (center_x + teeth_width, teeth_bottom),
                    max(1, height // 60))
    
    return surface