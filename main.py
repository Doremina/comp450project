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
    maze_name = "smallMaze"
    maze_path = "./mazes/"+ maze_name + ".txt"
    maze = Maze(maze_path)

    basic_agent = SubsumptionAgent(["avoid_walls", "avoid_ghosts", "move_toward_food","explore_random", "random_choice"], agent_name = "basic_agent_for_empty_maze")
    agent_with_small_memory = SubsumptionAgent(["avoid_walls", "avoid_ghosts", "move_toward_food","explore_random_memory"], agent_name = "agent_with_small_memory")

    graphics.draw_maze(maze, input_type="agent", agent=agent_with_small_memory, maze_name = maze_name)

