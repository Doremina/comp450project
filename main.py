import pygame
import graphics
import maze_util
import copy
from maze_util import Maze
import subsumption
from subsumption import SubsumptionAgent

# Constants
CELL_SIZE = 24
WALL_COLOR = (100, 100, 100)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
FOOD_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)

input_agent = "keyboard"
random_seed = 42


if __name__ == "__main__":
    maze_path = "./mazes/bigMaze.txt"
    basic_agent = SubsumptionAgent(["avoid_walls", "avoid_ghosts", "explore_random", "move_toward_food", "random_choice"])

    maze = Maze(maze_path)
    graphics.draw_maze(maze, input_type="agent", agent=basic_agent)

