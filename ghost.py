import random

random.seed(42)

class Ghost:

    def __init__(self, g_id: str):
        self.g_id = g_id
        self.past_move = "Stop"

#TODO can be a bit smarter (follow pacman when it's in sight)
    def move_direction(self, maze):
        current_y, current_x = maze.getghostlocation(self.g_id)
        legals = maze.legalactions(agent=self.g_id)
        if self.past_move in legals:
            return self.past_move
        index = random.randint(0, len(legals) - 1)
        self.past_move = legals[index]
        return legals[index]

