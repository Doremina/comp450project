import copy
import pygame

class Maze:
    def __init__(self, maze_txt_path):
        self.front_maze, self.back_maze = self.load_maze(maze_txt_path)
        self.pacman_score = 0
        self.pacman_steps = 0
        self.pacman_die = False
        self.pacman_win = False
        self.pacman_direction = "East"

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
                        front[y][x] = ' '
                    elif lines[y][x] == "P" or lines[y][x] == "G":
                        back[y][x] = ' '
                        front[y][x] = lines[y][x]

        return front, back

    def getpacmanlocation(self):
        maze = self.front_maze
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 'P':
                    pacman_location = (y, x)
                    return pacman_location

    def legalactions(self, agent="pacman", location=None):
        # if location is given, work based on location
        # if location is not given. work based on agent
        maze = self.back_maze

        legals = ["Stop"]
        if location:
            cy, cx = location  # (y,x)
            if cy - 1 >= 0 and maze[cy - 1][cx] != 'W':  # if going one left is in bounds and not wall
                legals.append("North")
            if cy + 1 <= len(maze) - 1 and maze[cy + 1][cx] != 'W':  # if going one right is in bounds and not wall
                legals.append("South")
            if cx + 1 <= len(maze[0]) - 1 and maze[cy][cx + 1] != 'W':  # if going one up is in bounds and not wall
                legals.append("East")
            if cx - 1 >= 0 and maze[cy][cx - 1] != 'W':
                legals.append("West")
            return legals

        elif agent == "pacman":
            pacman_location = self.getpacmanlocation()
            return self.legalactions(location=pacman_location)

        elif agent == "ghost":
            # TODO to be implemented after ghost agents
            # location =
            # return legalactions(maze, location=location)
            return None

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
            if self.front_maze[new_pacman_location[0]][new_pacman_location[1]] == 'G':
                self.pacman_die = True #TODO

            #3 if new location has food
            if self.back_maze[new_pacman_location[0]][new_pacman_location[1]] == '.':
                self.pacman_score += 1  # increase score
                new_back_maze[new_pacman_location[0]][new_pacman_location[1]] = ' '  # remove the food
                if not self.food_left(): self.pacman_win = True # if there's no food left after removal, win

            #4 update pacman's position
            new_front_maze[new_pacman_location[0]][new_pacman_location[1]] = 'P'

            #5 remove pacman's old position
            new_front_maze[y][x] = ' '

            self.back_maze = new_back_maze
            self.front_maze = new_front_maze
            self.pacman_steps += 1

    def food_left(self):
        for y in range(len(self.back_maze)):
            for x in range(len(self.back_maze[0])):
                if self.back_maze[y][x] == '.':
                    return True
        return False

    def check_game_end(self):
        if self.pacman_die:
            print(f"Pacman died at {self.pacman_steps} steps and ate {self.pacman_score} pieces of food.")

        if self.pacman_win:
            print(f"Pacman won by eating {self.pacman_score} pieces of food in {self.pacman_steps} steps.")

    def get_back_maze(self):
        return self.back_maze

    def get_front_maze(self):
        return self.front_maze

    def did_pacman_die(self):
        return self.pacman_die

    def did_pacman_win(self):
        return self.pacman_die

    def update_after_ghost_move(self, agent, direction_input):
        #TODO
        pass




