import pygame

def draw_curious_expression(surface, width, height):
    """
    Draws a curious face with one raised eyebrow and questioning expression
    
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
    
    # Draw eyes
    # White part of eyes (right eye slightly smaller - squint)
    pygame.draw.circle(surface, white, (left_eye_x, eye_y_pos), eye_radius)
    pygame.draw.circle(surface, white, (right_eye_x, eye_y_pos), eye_radius * 0.8)
    
    # Pupils (right eye looks to the side)
    pupil_radius = eye_radius // 2
    pygame.draw.circle(surface, black, (left_eye_x, eye_y_pos), pupil_radius)
    pygame.draw.circle(surface, black, (right_eye_x + pupil_radius//2, eye_y_pos), pupil_radius * 0.8)
    
    # Draw subtle highlights in eyes
    highlight_radius = pupil_radius // 3
    highlight_offset_x = pupil_radius // 3
    highlight_offset_y = pupil_radius // 3
    pygame.draw.circle(surface, white, 
                      (left_eye_x - highlight_offset_x, eye_y_pos - highlight_offset_y), 
                      highlight_radius)
    pygame.draw.circle(surface, white, 
                      (right_eye_x - highlight_offset_x, eye_y_pos - highlight_offset_y), 
                      highlight_radius)
    
    # Draw eyebrows (left raised with curiosity, right normal/slight frown)
    eyebrow_length = eye_radius * 2
    eyebrow_thickness = max(2, height // 40)
    
    # Left eyebrow (dramatically raised - questioning)
    left_eyebrow_y = eye_y_pos - eye_radius - eyebrow_thickness * 3
    pygame.draw.line(surface, black, 
                    (left_eye_x - eyebrow_length//2, left_eyebrow_y + eyebrow_thickness * 2),
                    (left_eye_x + eyebrow_length//2, left_eyebrow_y - eyebrow_thickness),
                    eyebrow_thickness)
    
    # Right eyebrow (slightly furrowed)
    right_eyebrow_y = eye_y_pos - eye_radius - eyebrow_thickness
    pygame.draw.line(surface, black, 
                    (right_eye_x - eyebrow_length//2, right_eyebrow_y),
                    (right_eye_x + eyebrow_length//2, right_eyebrow_y + eyebrow_thickness),
                    eyebrow_thickness)
    
    # Draw mouth (slightly open, as if asking a question)
    mouth_width = width // 4
    mouth_height = height // 8
    mouth_rect = pygame.Rect(
        center_x - mouth_width//2,
        center_y + height//8,
        mouth_width,
        mouth_height
    )
    
    # Draw small oval for questioning mouth
    pygame.draw.ellipse(surface, black, mouth_rect, max(2, height // 40))
    
    return surface