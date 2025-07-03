import random

random.seed(40)

class Ghost:

    def __init__(self, g_id: str):
        self.g_id = g_id
        self.past_move = "Stop"

#TODO can be a bit smarter (follow pacman when it's in sight)
    def move_direction(self, maze):
        current_y, current_x = maze.getghostlocation(self.g_id)
        legals = maze.legalactions(agent=self.g_id)

        # check if pacman is one step ahead of ghost
        for legal in legals:
            ry, rx = maze.action_result_location(legal, location=(current_y, current_x))
            if maze.getpacmanlocation() == (ry, rx):
                return legal

        # check if ghost can see pacman
        for legal in legals:
            ry, rx = maze.action_result_location(legal, location=(current_y, current_x))
            ry2, rx2 = maze.action_result_location(legal, location=(ry, rx))
            ry3, rx3 = maze.action_result_location(legal, location=(ry2, rx2))

            front_maze = maze.get_front_maze()
            front_maze = maze.get_front_maze()

            py, px = maze.getpacmanlocation()
            if (ry2, rx2) == (py, px):
                return legal
            elif (ry3, rx3) == (py, px):
                return legal

        if self.past_move in legals:
            return self.past_move

        index = random.randint(0, len(legals) - 1)
        self.past_move = legals[index]
        return legals[index]

