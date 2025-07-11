import maze_util
import random
import os

# LAYERS
class LayerAvoidWalls:
    name = "Avoid Walls"
    def get_actions(self, maze, given_actions=None):
        # setting legals = None will allow this layer to be the first and not the first layer

        # if first (maze.legalactions() already implemented wall avoidance)
        if given_actions is None: return maze.legalactions()

        # if second etc.
        else:
            actions_temp = given_actions.copy()
            for action in actions_temp:
                # if given actions do not satisfy avoiding walls, remove them
                if not action in maze.legalactions():
                    actions_temp.remove(action)

            # since legal_actions will be sent from low level (higher priority) layer,
            # if none of this layer's action choices matches with the low level layer's actions,
            # ignore this current layer and continue with the low level layer's actions
            # by this, lower layers can OVERRIDE the outer layers.
            if actions_temp: return actions_temp
            else: return given_actions.copy()

#TODO: create another ghost avoid layer which can sense 2 steps ahead (a better sensor)
#TODO: this layer is buggy i couldn't fix yet
class LayerAvoidGhosts:
    name = "Avoid Ghosts"
    def get_actions(self, maze, given_actions=None):
        if given_actions is None: given_actions = ["Stop", "North", "South", "East", "West"]

        """
        actions = given_actions.copy()
        len_actions = len(actions)
        for i in range(len_actions-1, -1, -1):
            ry, rx = maze.action_result_location(actions[i])
            if maze.get_front_maze()[ry][rx].isdigit(): # is ghost
                del actions[i]
        """

        safe_actions_1 = []
        for action in given_actions:
            ry, rx = maze.action_result_location(action)
            cell = maze.get_front_maze()[ry][rx]
            if not str(cell).isdigit():  # is ghost
                safe_actions_1.append(action)

        safe_actions_2 = []
        for action in safe_actions_1:
            ry, rx = maze.action_result_location(action)
            for action2 in ["East", "North", "South", "West"]:
                ry, rx = maze.action_result_location(action2)
                if not maze.get_front_maze()[ry][rx].isdigit():
                    safe_actions_2.append(action)




        # lower layer override
        if safe_actions_2: return safe_actions_2
        elif safe_actions_1: return safe_actions_1
        else: return given_actions.copy()

class LayerExploreRandomly:
    name = "Explore Randomly"
    def get_actions(self, maze, given_actions=None):
        if given_actions is None: given_actions = ["Stop", "North", "South", "East", "West"]

        actions = given_actions.copy()
        if "Stop" in actions: actions.remove("Stop")

        # lower layer override
        if actions: return actions
        else: return given_actions.copy()

# This layer only works if it is the last one
class LayerExploreRandomlyMemory:
    name = "Explore Randomly With Memory"
    def __init__(self):
        self.last_actions = [] # index 0 holds the oldest, index 2 holds the newest

    def add_action(self, action):
        if len(self.last_actions) < 3:
            self.last_actions.append(action)
        else:
            self.last_actions.pop(0)
            self.last_actions.append(action)

    def get_actions(self, maze, given_actions):
        actions = given_actions.copy()
        if "Stop" in actions: actions.remove("Stop")

        preferred_action = None
        if self.last_actions:
            for action in actions:
                if action == self.last_actions[-1]:
                    preferred_action = action
                    break

        if preferred_action is not None:
            self.add_action(preferred_action)
            return [preferred_action]
        else:
            action = random.choice(actions)
            self.add_action(action)
            return [action]


class LayerMoveTowardCloseFood:
    name = "Move Toward Close Food"
    def get_actions(self, maze, given_actions=None):
        if given_actions is None: given_actions = ["Stop", "North", "South", "East", "West"]
        best_results = []
        for action in given_actions:
            score = 0
            cy1, cx1 = maze.action_result_location(action)
            cy2, cx2 = maze.action_result_location(action, (cy1, cx1))
            if maze.get_back_maze()[cy1][cx1] == '.':
                score += 1
            if maze.get_back_maze()[cy2][cx2] == '.':
                score += 1
            best_results.append((score, action))

        top_score = 0
        for result in best_results:
            if result[0] > top_score:
                top_score = result[0]

        actions = [item[1] for item in best_results if item[0] == top_score]

        for i in range(len(actions)-1, -1, -1):
            if actions[i] not in given_actions:
                del actions[i]

        # lower layer override
        if actions: return actions
        else: return given_actions.copy()

class LayerRandomlySelect:
    name = "Randomly Select"
    def get_actions(self, maze, given_actions=None):
        if given_actions is None:
            given_actions = ["Stop", "North", "South", "East", "West"]

        # if given_actions is empty
        elif not given_actions: return None

        rand_index = random.randint(0, len(given_actions) - 1)
        return [given_actions[rand_index]]

LAYERS_DICT = {
    "avoid_walls": LayerAvoidWalls,
    "avoid_ghosts": LayerAvoidGhosts,
    "explore_random": LayerExploreRandomly,
    "explore_random_memory": LayerExploreRandomlyMemory,
    "move_toward_food": LayerMoveTowardCloseFood,
    "random_choice": LayerRandomlySelect,
}

# AGENTS
class SubsumptionAgent:
    agent_num = 0
    def __init__(self, layer_names, agent_name ="unnamed", log_dir = "logs"):
        #init id
        self.agent_num = SubsumptionAgent.agent_num
        SubsumptionAgent.agent_num += 1

        self.agent_name = agent_name

        # init layers
        self.layers = []
        self.initialize_layers(layer_names)

        # init action count for score calculation later
        self.action_count = 0

        # init eaten food amount for score calculation later
        self.food = 0 #TODO increase in game

        # Create log directory
        os.makedirs(log_dir, exist_ok=True)

        # Define log file path
        self.log_path = os.path.join(log_dir, f"{self.agent_num}{self.agent_name}.txt")
        self.log_file = open(self.log_path, "w")

        # Initial log message
        self.log(f"Initialized agent#{self.agent_num} with layers: {', '.join(layer_names)}")

    def initialize_layers(self, layers):
        for layer_name in layers:
            self.layers.append(LAYERS_DICT[layer_name]())

    def log(self, message):
        self.log_file.write(message + "\n")
        self.log_file.flush()

    def eat_food(self):
        self.food += 1

    def game_end(self, winlose:str, steps: int, score:int):
        self.log(f"Game ended with {winlose}.\nSteps Taken: {steps}, Score: {score}.")

    def act(self, maze):

        self.log(f"\nAction #{self.action_count}:")
        chosen_actions = None
        for layer in self.layers:
            chosen_actions = layer.get_actions(maze, given_actions=chosen_actions)
            self.log(f"Layer: {layer.name}, Chosen actions: {chosen_actions}")

        self.log(f"Chosen actions after layer loop: {chosen_actions}")

        if len(chosen_actions) != 1:
            if len(chosen_actions) > 1: raise ValueError("Agent chose more than one action.")
        elif len(chosen_actions) == 0: raise ValueError("Agent chose none of the actions.")
        else:
            self.action_count += 1
            return chosen_actions[0]
