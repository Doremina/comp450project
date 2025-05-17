import pygame
import graphics
import maze_util
import copy
from maze_util import maze_after_pacman_move

# Constants
CELL_SIZE = 24
WALL_COLOR = (100, 100, 100)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
FOOD_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)

input_agent = "keyboard"

# Initialize Pygame
def draw_maze(maze, pacman_direction= "East", input_type="keyboard"):
    pygame.init()
    rows, cols = len(maze), len(maze[0])
    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))
    pygame.display.set_caption("Pacman Maze")
    clock = pygame.time.Clock()

    # Game Score Calculation
    food_score = 0


    running = True

    while running:
        screen.fill(BG_COLOR)

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                if cell == 'W':
                    pygame.draw.rect(screen, WALL_COLOR, rect)
                elif cell == 'P':
                    cx, cy = rect.center
                    r = CELL_SIZE // 2 - 2
                    graphics.draw_pacman_directional(screen, (cx, cy), r, PACMAN_COLOR, pacman_direction)

                elif cell == 'G':
                    #TODO probably need to draw different ghosts as different agents too
                    # Scale and offset the shape to the cell center
                    cx, cy = rect.center
                    graphics.draw_ghost(screen, (cx, cy), GHOST_COLOR)

                elif cell == '.':
                    pygame.draw.circle(screen, FOOD_COLOR, rect.center, 4)

        pygame.display.flip()

        # Exit on window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        input = getinput(where=input_type)
        if input:
            pacman_direction = input
            #TODO

            # update maze
            old_maze = copy.deepcopy(maze)
            maze = maze_after_pacman_move(old_maze, pacman_direction)

            # check if pacman died
            game_over = maze_util.did_pacman_die(old_maze, maze)
            if game_over:
                break

            # check if game won (no food left)
            pacman_win = maze_util.did_pacman_win(maze)
            if pacman_win:
                break

            # check if pacman ate
            if maze_util.did_pacman_eat(old_maze, maze):
                food_score += 1



            # maze = update_maze(maze, "pacman", input)

        clock.tick(10)

    #TODO show score etc.
    # game_over, pacman_win
    print(f"food score: {food_score}")
    pygame.quit()

def getinput(where="keyboard"):
    if where == "keyboard":
        input = pygame.key.get_pressed()
        if input[pygame.K_LEFT]:
            out_direction = "West"
        elif input[pygame.K_RIGHT]:
            out_direction = "East"
        elif input[pygame.K_UP]:
            out_direction = "North"
        elif input[pygame.K_DOWN]:
            out_direction = "South"
        else: return None

    #else: out_direction = "South" #TODO agent

    return out_direction





if __name__ == "__main__":
    maze_path = "./mazes/smallMaze.txt"
    maze = maze_util.load_maze(maze_path)
    draw_maze(maze, input_type=input_agent)
