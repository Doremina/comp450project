import maze_util

class LayerAvoidWalls:
    def get_actions(self, maze, legal_actions=None):
        # setting legals = None will allow this layer to be the first and not the first layer

        # if first (maze.legalactions() already implemented wall avoidance)
        if not legal_actions: return maze.legalactions()

        # if second etc.
        else:
            actions = legal_actions.copy()
            for action in actions:
                # if given actions do not satisfy avoiding walls, remove them
                if not action in maze.legalactions():
                    actions.remove(action)
            return actions


class LayerAvoidGhosts:
    def get_actions(self, maze, given_actions=None):
        if not given_actions: given_actions = ["Stop", "North", "South", "East", "West"]

        actions = given_actions.copy()
        for i in range(len(actions), -1, -1):
            ry, rx = maze.action_result_location(actions[i])
            if maze.get_front_maze()[ry][rx].isdigit(): # is ghost
                del actions[i]
        return actions

class LayerExploreRandomly:
    def get_actions(self, maze, given_actions=None):
        if not given_actions: given_actions = ["Stop", "North", "South", "East", "West"]

        actions = given_actions.copy()
        actions.remove("Stop")
        return actions

class LayerMoveTowardCloseFood:
    def get_actions(self, maze, given_actions=None):
        if not given_actions: given_actions = ["Stop", "North", "South", "East", "West"]
        best_results = []
        for action in given_actions:
            score = 0
            cy1, cx1 = maze.action_result_location(action)
            cy2, cx2 = maze.action_result_location(action, (cy1, cx1))
            if maze.get_front_maze()[cy1][cx1] == '.':
                score += 1
            if maze.get_front_maze()[cy2][cx2] == '.':
                score += 1
            best_results.append((score, action))

        top_score = 0
        for result in best_results:
            if result > top_score:
                top_score = result

        actions = [item[1] for item in best_results if item[0] == top_score]

        for i in range(len(actions), -1, -1):
            if actions[i] not in given_actions:
                del actions[i]

        return actions

#TODO eğer layer'ın seçtiği aksiyonların hiçbiri given actions'ta yoksa direkt given actions'ı döndürmesi gerekir
# (layer override edilmiş olur)

class LayerRandomlySelect:
    def get_actions(self, maze, given_actions=None):

