import pygame

def draw_alert_expression(surface, width, height):
    """
    Draws an alert face with alarm symbols and urgent expression
    
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
    alert_red = (220, 20, 60)  # Crimson red
    
    # Calculate positions
    center_x = width // 2
    center_y = height // 2
    
    # Draw alert symbol background (circle with exclamation)
    circle_radius = width // 2.5
    
    # Red circle background
    pygame.draw.circle(surface, alert_red, (center_x, center_y), circle_radius)
    pygame.draw.circle(surface, black, (center_x, center_y), circle_radius, max(2, width // 40))
    
    # Exclamation mark (white)
    line_height = circle_radius * 1.2
    line_width = max(4, width // 15)
    
    # Vertical line
    pygame.draw.line(surface, white,
                    (center_x, center_y - line_height//2),
                    (center_x, center_y + line_height//6),
                    line_width)
    
    # Bottom dot
    dot_radius = line_width // 1.5
    dot_y = center_y + line_height//3
    
    pygame.draw.circle(surface, white, (center_x, dot_y), dot_radius)
    
    # Add flashing effect with alternating rings
    ring_spacing = width // 20
    num_rings = 3
    
    for i in range(num_rings):
        ring_radius = circle_radius + ring_spacing * (i + 1)
        # Alternate colors between red and white
        ring_color = white if i % 2 == 0 else alert_red
        pygame.draw.circle(surface, ring_color, (center_x, center_y), ring_radius, max(2, width // 60))
    
    return surface