import pygame
import math
import maze_util
import util
import glob
import os

# Constants
CELL_SIZE = 24
WALL_COLOR = (100, 100, 100)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLORS = [
    (255, 0, 0),       # Red
    (0, 255, 255),     # Cyan
    (255, 105, 180),   # Hot Pink
    (0, 255, 0),       # Lime Green
    (255, 165, 0),     # Orange
    (138, 43, 226),    # Blue Violet
    (255, 255, 0),     # Yellow
    (0, 0, 255),       # Blue
    (139, 69, 19),     # Saddle Brown
]
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


def clear_screenshots(path):
    folder = path
    files = glob.glob(os.path.join(folder, "*"))

    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

def draw_maze(maze: maze_util.Maze, pacman_direction="East", input_type="keyboard", agent=None, maze_name="unnamed_maze"):
    pygame.init()

    len_y, len_x = len(maze.back_maze), len(maze.back_maze[0])
    screen = pygame.display.set_mode((len_x * CELL_SIZE, len_y * CELL_SIZE))
    pygame.display.set_caption("Pacman Game")
    clock = pygame.time.Clock()
    running = True
    turn = "pacman"

    screenshot_folder = f"./logs/screenshots/{agent.agent_name}-{maze_name}/"
    os.makedirs(screenshot_folder, exist_ok=True)
    frame_count = 0
    clear_screenshots(screenshot_folder)

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

                elif current_cell.isdigit():
                    # Scale and offset the shape to the cell center
                    cx, cy = rect.center
                    color = GHOST_COLORS[int(current_cell)]
                    draw_ghost(screen, (cx, cy), color)

        pygame.display.flip()

        # Exit on window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # this is where agents will send their inputs
        if turn == "pacman":
            if input_type == "keyboard":
                input_pacman = util.getinput(where=input_type)
                if input_pacman is not None:
                    maze.pacman_direction = input_pacman

                    # update maze
                    maze.update_after_pacman_move(input_pacman)


            elif input_type == "agent":
                if agent is None: raise ValueError("Agent is not defined. Make sure to pass agent to draw_maze if input_type is agent.")
                else:
                    action_pacman = agent.act(maze)
                    if action_pacman is None: raise ValueError("Agent's act() returned None in draw_maze.")

                    # update pacman direction
                    maze.pacman_direction = action_pacman

                    # update maze
                    maze.update_after_pacman_move(action_pacman)

            if maze.check_game_end() is not None:
                if input_type == "agent":
                    winlose, steps, score = maze.check_game_end()
                    agent.game_end(winlose, steps, score)
                elif input_type == "keyboard":
                    print(f"Game ended with {maze.check_game_end()[0]}.\nSteps Taken: {maze.check_game_end()[1]}, Score: {maze.check_game_end()[2]}.")
                running = False

            turn = "ghost"

        elif turn == "ghost":
            maze.move_ghosts()

            if maze.check_game_end() is not None:
                if input_type == "agent":
                    winlose, steps, score = maze.check_game_end()
                    agent.game_end(winlose, steps, score)
                elif input_type == "keyboard":
                    print(f"Game ended with {maze.check_game_end()[0]}.\nSteps Taken: {maze.check_game_end()[1]}, Score: {maze.check_game_end()[2]}.")

                running = False

            turn = "pacman"


        image_dir = screenshot_folder + f"{frame_count}.png"
        pygame.image.save(screen, image_dir)
        frame_count += 1
        clock.tick(30)

    print(f"Game ended when turn: {turn}")
    pygame.quit()