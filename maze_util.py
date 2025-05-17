import copy

from sympy import false


def load_maze(path):
    # Maze is an array,
    # P denotes Pacman
    # . denoted food
    # W denotes wall
    # G denotes ghost
    with open(path, 'r') as f:
        maze = [list(line.replace(' ', '.').strip('\n')) for line in f.readlines()]
    return maze

def getpacmanlocation(maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'P':
                pacman_location = (y, x)
                return pacman_location
    return None


def legalactions(maze, agent="pacman", location=None):
    # if location is given, work based on location
    # if location is not given. work based on agent
    legals = ["Stop"]
    if location:
        cy, cx = location # (y,x)
        if cy-1 >= 0 and maze[cy-1][cx] != 'W': # if going one left is in bounds and not wall
            legals.append("North")
        if cy+1 <= len(maze)-1 and maze[cy+1][cx] != 'W': # if going one right is in bounds and not wall
            legals.append("South")
        if cx+1 <= len(maze[0])-1 and maze[cy][cx+1] != 'W': # if going one up is in bounds and not wall
            legals.append("East")
        if cx-1 >= 0 and maze[cy][cx-1] != 'W':
            legals.append("West")
        return legals

    elif agent == "pacman":
        pacman_location = getpacmanlocation(maze)
        return legalactions(maze, location=pacman_location)

    elif agent == "ghost":
        #TODO to be implemented after ghost agents
        # location =
        # return legalactions(maze, location=location)
        return None

def maze_after_pacman_move(maze, input):

    new_maze = copy.deepcopy(maze)
    pacman_direction = input
    legals = legalactions(maze, agent="pacman")

    # if the only legal action is to stop, stop
    if len(legals) == 1 and legals[0] == 'Stop':
        return new_maze

    y, x = getpacmanlocation(maze)
    if input in legals:
        # update the old location
        new_maze[y][x] = ' '

        # update the new location
        if input == "North":
            new_maze[y-1][x] = 'P'
        elif input == "South":
            new_maze[y+1][x] = 'P'
        elif input == "East":
            new_maze[y][x+1] = 'P'
        elif input == "West":
            new_maze[y][x-1] = 'P'

        return new_maze

    else:
        return new_maze


def did_pacman_eat(old_maze, new_maze):
    # get the old maze and new maze to see if pacman ate
    y, x = getpacmanlocation(new_maze)
    if old_maze[y][x] == '.': return True
    else: return False

def did_pacman_die(old_maze, new_maze):
    # get the old maze and new maze to see if pacman died
    y,x = getpacmanlocation(new_maze)
    if old_maze[y][x] == 'G':
        return True
    else:
        return False

def did_pacman_win(new_maze):
    for line in new_maze:
        for column in line:
            if column == '.':
                return False
    return True


#TODO
# def update_maze_after_moves(maze, moves) # moves = [(agent, move), (agent,move), (agent,move)]

