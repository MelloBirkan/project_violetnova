import pygame

def draw_happy_expression(surface, width, height):
    """
    Draws a very happy face with crescent-shaped eyes and wide smile
    
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
    
    # Draw crescent eyes (common in anime-style happy faces)
    eye_width = width // 5
    eye_height = height // 15
    eye_y_pos = center_y - height // 8
    left_eye_x = center_x - width // 4
    right_eye_x = center_x + width // 4
    
    # Left eye crescent
    left_eye_rect = pygame.Rect(
        left_eye_x - eye_width//2,
        eye_y_pos - eye_height//2,
        eye_width,
        eye_height
    )
    
    # Right eye crescent
    right_eye_rect = pygame.Rect(
        right_eye_x - eye_width//2,
        eye_y_pos - eye_height//2,
        eye_width,
        eye_height
    )
    
    # Draw the crescents (bottom half of ellipses, filled)
    pygame.draw.arc(surface, black, left_eye_rect, 3.14, 6.28, max(2, height // 30))
    pygame.draw.arc(surface, black, right_eye_rect, 3.14, 6.28, max(2, height // 30))
    
    # Add slight lines below crescents to complete the shape
    pygame.draw.line(surface, black,
                    (left_eye_x - eye_width//2, eye_y_pos),
                    (left_eye_x + eye_width//2, eye_y_pos),
                    max(2, height // 30))
    
    pygame.draw.line(surface, black,
                    (right_eye_x - eye_width//2, eye_y_pos),
                    (right_eye_x + eye_width//2, eye_y_pos),
                    max(2, height // 30))
    
    # Draw wide smile with rosy cheeks
    smile_width = width // 2
    smile_height = height // 3
    
    smile_rect = pygame.Rect(
        center_x - smile_width//2,
        center_y - smile_height//6,
        smile_width,
        smile_height
    )
    
    # Draw the wide smile (top half of an ellipse)
    pygame.draw.arc(surface, black, smile_rect, 0, 3.14, max(2, height // 30))
    
    # Draw rosy cheeks
    cheek_radius = width // 10
    cheek_y = center_y
    left_cheek_x = center_x - width // 3
    right_cheek_x = center_x + width // 3
    
    # Draw with slight transparency for subtle effect
    cheek_color = (255, 150, 150, 100)  # Light pink with transparency
    
    cheek_surface = pygame.Surface((cheek_radius*2, cheek_radius*2), pygame.SRCALPHA)
    pygame.draw.circle(cheek_surface, cheek_color, (cheek_radius, cheek_radius), cheek_radius)
    
    # Blit the cheeks onto the main surface
    surface.blit(cheek_surface, (left_cheek_x - cheek_radius, cheek_y - cheek_radius))
    surface.blit(cheek_surface, (right_cheek_x - cheek_radius, cheek_y - cheek_radius))
    
    return surface