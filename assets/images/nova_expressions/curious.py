import pygame

def draw_curious_expression(surface, width, height):
    """
    Empty expression - no face drawn

    Args:
        surface: The pygame surface to draw onto
        width: Width of the surface
        height: Height of the surface
    """
    # Clear the surface - draw nothing
    surface.fill((0, 0, 0, 0))  # Transparent

    return surface