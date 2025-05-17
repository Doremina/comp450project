# Read maze from file
def load_maze(path):
    # Maze is an array,
    # P denotes Pacman
    # . denoted food
    # W denotes wall
    # G denotes ghost
    with open(path, 'r') as f:
        maze = [list(line.replace(' ', '.').strip('\n')) for line in f.readlines()]
    return maze

