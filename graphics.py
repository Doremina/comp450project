import pygame
import math
import maze_util
import util
import copy

# Constants
CELL_SIZE = 24
WALL_COLOR = (100, 100, 100)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
FOOD_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)

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

def draw_maze(maze: maze_util.Maze, pacman_direction="East", input_type="keyboard"):
    pygame.init()

    len_y, len_x = len(maze.back_maze), len(maze.back_maze[0])
    screen = pygame.display.set_mode((len_x * CELL_SIZE, len_y * CELL_SIZE))
    pygame.display.set_caption("Pacman Game")
    clock = pygame.time.Clock()
    running = True
    turn = "pacman"

    while running:
        screen.fill(BG_COLOR)
        for y in range(len_y):
            for x in range(len_x):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                current_cell = maze.get_back_maze()[y][x]
                if current_cell == 'W':
                    pygame.draw.rect(screen, WALL_COLOR, rect)

                elif current_cell == '.':
                    pygame.draw.circle(screen, FOOD_COLOR, rect.center, 4)

                current_cell = maze.get_front_maze()[y][x]
                if current_cell == 'P':
                    cx, cy = rect.center
                    r = CELL_SIZE // 2 - 2
                    draw_pacman_directional(screen, (cx, cy), r, PACMAN_COLOR, maze.pacman_direction)

                elif current_cell == 'G':
                    # TODO probably need to draw different ghosts as different agents too

                    # Scale and offset the shape to the cell center
                    cx, cy = rect.center
                    draw_ghost(screen, (cx, cy), GHOST_COLOR)



        pygame.display.flip()

        # Exit on window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # TODO this is where agents will send their inputs
        input_pacman = util.getinput(where=input_type)
        if input_pacman:
            maze.pacman_direction = input_pacman

            # update maze
            maze.update_after_pacman_move(input_pacman)
            maze.check_game_end()

        clock.tick(10)

    maze.check_game_end()
    pygame.quit()