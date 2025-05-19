import pygame
import graphics
import maze_util
import copy
from maze_util import Maze

# Constants
CELL_SIZE = 24
WALL_COLOR = (100, 100, 100)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
FOOD_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)

input_agent = "keyboard"


if __name__ == "__main__":
    maze_path = "./mazes/smallMaze.txt"
    maze = Maze(maze_path)
    print(f"Maze: {maze}, type: {type(maze)}")
    graphics.draw_maze(maze, input_type=input_agent)
