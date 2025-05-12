import pygame

def draw_warning_expression(surface, width, height):
    """
    Draws a warning face with alert eyes and concerned expression
    
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
    warning_yellow = (255, 200, 0)
    
    # Calculate positions
    center_x = width // 2
    center_y = height // 2
    
    # Draw warning triangle background
    triangle_size = width // 1.5
    triangle_half = triangle_size // 2
    triangle_height = int(triangle_size * 0.866)  # sqrt(3)/2 * size
    
    triangle_points = [
        (center_x, center_y - triangle_height//2),  # Top
        (center_x - triangle_half, center_y + triangle_height//2),  # Bottom left
        (center_x + triangle_half, center_y + triangle_height//2)   # Bottom right
    ]
    
    # Draw triangle with black outline
    pygame.draw.polygon(surface, warning_yellow, triangle_points)
    pygame.draw.polygon(surface, black, triangle_points, max(2, width // 40))
    
    # Draw exclamation mark
    # Vertical line
    line_top = center_y - triangle_height//4
    line_bottom = center_y + triangle_height//8
    line_width = max(3, width // 20)
    
    pygame.draw.line(surface, black,
                    (center_x, line_top),
                    (center_x, line_bottom),
                    line_width)
    
    # Bottom dot
    dot_radius = line_width // 2
    dot_y = line_bottom + dot_radius * 2
    
    pygame.draw.circle(surface, black, (center_x, dot_y), dot_radius)
    
    return surface