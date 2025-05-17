import pygame
import math

def draw_pacman_directional(surface, center, radius, color, pacman_direction):
    # Draw Pacman with respect to its direction

    if pacman_direction == "East": start_deg, end_deg = 30, 330
    elif pacman_direction == "West": start_deg, end_deg = 210, 150
    elif pacman_direction == "North": start_deg, end_deg = 300, 240
    elif pacman_direction == "South": start_deg, end_deg = 120, 60
    else : start_deg, end_deg = 30, 330

    # Normalize angle sweep
    if end_deg < start_deg:
        end_deg += 360

    steps = 12
    angle_step = (end_deg - start_deg) / steps

    points = [center]
    for i in range(steps + 1):
        angle_deg = start_deg + i * angle_step
        angle_rad = math.radians(angle_deg)
        x = center[0] + math.cos(angle_rad) * radius
        y = center[1] + math.sin(angle_rad) * radius
        points.append((x, y))

    pygame.draw.polygon(surface, color, points)

def draw_ghost(surface, center, color):
    # Adjustable
    scale = 10

    cx, cy = center

    # Define ghost shape in relative coordinates centered at (0, 0)
    ghost_shape = [
        (0, -0.5), (0.25, -0.75), (0.5, -0.5), (0.75, -0.75),
        (0.75, 0.5), (0.5, 0.75), (-0.5, 0.75),
        (-0.75, 0.5), (-0.75, -0.75), (-0.5, -0.5), (-0.25, -0.75)
    ]

    ghost_points = [(x * scale + cx, -y * scale + cy) for x, y in ghost_shape]

    # Draw the polygon
    pygame.draw.polygon(surface, color, ghost_points)