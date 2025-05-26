import copy
import pygame
from ghost import Ghost
import util

class Maze:
    def __init__(self, maze_txt_path):

        self.pacman_score = 0
        self.pacman_steps = 0
        self.pacman_die = False
        self.pacman_win = False
        self.pacman_direction = "East"

        self.ghosts = []

        self.front_maze, self.back_maze = self.load_maze(maze_txt_path)


    def load_maze(self, path):
        # Maze is an array,
        # P denotes Pacman
        # . denoted food
        # W denotes wall
        # G denotes ghost

        with open(path, 'r') as f:

            lines = f.readlines()
            lines = [list(line.replace(' ', '.').strip('\n')) for line in lines]

            len_y = len(lines)
            len_x = len(lines[0])

            front = [[' ' for _ in row] for row in lines]
            back = [[' ' for _ in row] for row in lines]

            for y in range(len_y):
                for x in range(len_x):
                    if lines[y][x] == "." or lines[y][x] == "W":
                        back[y][x] = lines[y][x]
                    elif lines[y][x] == "P":
                        back[y][x] = ' '
                        front[y][x] = lines[y][x]
                    elif lines[y][x].isdigit():
                        back[y][x] = '.' # ghost has food in background at start by default
                        front[y][x] = lines[y][x]
                        self.ghosts.append(Ghost(lines[y][x]))

        # sort ghosts by their ids
        self.ghosts.sort(key=lambda g: g.g_id)
        return front, back

    def getpacmanlocation(self):
        maze = self.front_maze
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 'P':
                    pacman_location = (y, x)
                    return pacman_location

    def getghostlocation(self, g_id):
        maze = self.front_maze
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == g_id:
                    ghost_location = (y, x)
                    return ghost_location

    def legalactions(self, agent="pacman"):
        # if location is given, work based on location
        # if location is not given. work based on agent


        legals = []

        if agent == "pacman":
            maze = self.back_maze # for avoiding walls
            cy, cx = self.getpacmanlocation()
            legals.append("Stop")

            if cy - 1 >= 0 and maze[cy - 1][cx] != 'W':  # if going one left is in bounds and not wall
                legals.append("North")
            if cy + 1 <= len(maze) - 1 and maze[cy + 1][cx] != 'W':  # if going one right is in bounds and not wall
                legals.append("South")
            if cx + 1 <= len(maze[0]) - 1 and maze[cy][cx + 1] != 'W':  # if going one up is in bounds and not wall
                legals.append("East")
            if cx - 1 >= 0 and maze[cy][cx - 1] != 'W':
                legals.append("West")
            return legals

        elif agent.isdigit(): # agent is ghost
            cy, cx = self.getghostlocation(agent)
            back_maze = self.get_back_maze()
            front_maze = self.get_front_maze()

            if cy - 1 >= 0 and back_maze[cy - 1][cx] != 'W':  # if going one left is in bounds and not wall
                if not front_maze[cy-1][cx].isdigit(): legals.append("North") # and not a ghost

            if cy + 1 < len(back_maze) - 1 and back_maze[cy + 1][cx] != 'W':  # if going one right is in bounds and not wall
                if not front_maze[cy+1][cx].isdigit(): legals.append("South") # and not a ghost

            if cx + 1 < len(back_maze[0]) - 1 and back_maze[cy][cx + 1] != 'W':  # if going one up is in bounds and not wall
                if not front_maze[cy][cx+1].isdigit(): legals.append("East")  # and not a ghost

            if cx - 1 >= 0 and back_maze[cy][cx - 1] != 'W': # if going one down is in bounds and not wall
                if not front_maze[cy][cx-1].isdigit(): legals.append("West")  # and not a ghost

            return legals

    def update_after_pacman_move(self, direction_input):

        new_front_maze = copy.deepcopy(self.front_maze)
        new_back_maze = copy.deepcopy(self.back_maze)
        pacman_direction = direction_input
        legals = self.legalactions(agent="pacman")

        # if the only legal action is to stop, stop
        if len(legals) == 1 and legals[0] == 'Stop':
            return

        # old location of pacman is (y, x)
        y, x = self.getpacmanlocation()

        if direction_input in legals:

            #1 find new location of pacman
            new_pacman_location = None
            if direction_input == "North":
                #new_front_maze[y - 1][x] = 'P'
                new_pacman_location = (y - 1, x)
            elif direction_input == "South":
                new_pacman_location = (y + 1, x)
            elif direction_input == "East":
                new_pacman_location = (y, x + 1)
            elif direction_input == "West":
                new_pacman_location = (y, x - 1)

            #2 if new location has ghost, die
            if self.front_maze[new_pacman_location[0]][new_pacman_location[1]].isdigit():
                self.pacman_die = True

            #3 if new location has food
            if self.back_maze[new_pacman_location[0]][new_pacman_location[1]] == '.':
                self.pacman_score += 1  # increase score
                new_back_maze[new_pacman_location[0]][new_pacman_location[1]] = ' '  # remove the food


            #4 update pacman's position
            new_front_maze[new_pacman_location[0]][new_pacman_location[1]] = 'P'

            #5 remove pacman's old position
            new_front_maze[y][x] = ' '

            self.back_maze = new_back_maze
            self.front_maze = new_front_maze
            self.pacman_steps += 1
            if not self.food_left(): self.pacman_win = True  # if there's no food left after removal, win

    def update_after_ghost_move(self, g_id, direction_input):

        new_front_maze = copy.deepcopy(self.front_maze)
        ghost_direction = direction_input
        legals = self.legalactions(agent=g_id)

        # if the only legal action is to stop, stop
        if len(legals) == 1 and legals[0] == 'Stop':
            return

        # old location of pacman is (y, x)
        y, x = self.getghostlocation(g_id)

        if direction_input in legals:

            #1 find new location of ghost
            new_ghost_location = None
            if direction_input == "North":
                new_ghost_location = (y - 1, x)
            elif direction_input == "South":
                new_ghost_location = (y + 1, x)
            elif direction_input == "East":
                new_ghost_location = (y, x + 1)
            elif direction_input == "West":
                new_ghost_location = (y, x - 1)

            #1 check if ghost ate pacman
            if self.front_maze[new_ghost_location[0]][new_ghost_location[1]] == 'P':
                self.pacman_die = True

            #2 update ghost's position
            new_front_maze[new_ghost_location[0]][new_ghost_location[1]] = g_id

            #3 remove ghost's old position
            new_front_maze[y][x] = ' '

            self.front_maze = new_front_maze

    def move_ghosts(self):
        # ghost_moves = [(agent_id, direction), (agent_id, direction)...]
        for ghost in self.ghosts:
            direction = ghost.move_direction(self)
            g_id = ghost.g_id
            self.update_after_ghost_move(g_id, direction)

    def food_left(self):
        for y in range(len(self.back_maze)):
            for x in range(len(self.back_maze[0])):
                if self.back_maze[y][x] == '.':
                    return True
        return False

    def check_game_end(self):
        if self.pacman_die:
            return "Lose", self.pacman_steps, self.pacman_score

        if self.pacman_win:
            return "Win", self.pacman_steps, self.pacman_score


    def get_back_maze(self):
        return self.back_maze

    def get_front_maze(self):
        return self.front_maze

    def did_pacman_die(self):
        return self.pacman_die

    def did_pacman_win(self):
        return self.pacman_die

    #TODO debug this
    def action_result_location(self, action, location=None):
        # returns where pacman will end up after action

        if location is None: cy, cx = self.getpacmanlocation()
        else : cy, cx = location
        maze = self.back_maze
        if action == "Stop":
            return cy, cx
        elif action == "North":
            if cy - 1 >= 0 and maze[cy - 1][cx] != 'W':
                return cy-1, cx
        elif action == "South":
            if cy + 1 <= len(maze) - 1 and maze[cy + 1][cx] != 'W':
                return cy+1, cx
        elif action == "East":
            if cx + 1 <= len(maze[0]) - 1 and maze[cy][cx + 1] != 'W':
                return cy, cx + 1
        elif action == "West":
            if cx - 1 >= 0 and maze[cy][cx - 1] != 'W':
                return cy, cx - 1
        return cy, cx

    def closest_foods(self, dist="manhattan"):
        cy, cx = self.getpacmanlocation()
        maze = self.back_maze
        distances = []
        for y in range(len(maze)):
            for x in range(len(self.back_maze[0])):
                if self.back_maze[y][x] == '.':
                    distances.append([util.manhattanDistance((cy, cx), (y, x)), (y,x)])

        # Step 1: Find the minimum distance
        min_dist = min(distances, key=lambda x: x[0])[0]

        # Step 2: Filter all items with that minimum distance
        result = [item for item in distances if item[0] == min_dist]

        return distances







