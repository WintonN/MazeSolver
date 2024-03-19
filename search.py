from maze_env import MazeEnv
from maze_state import MazeState
from queue import PriorityQueue
import math


"""
solver.py

This file contains the methods and algorithms used to solve the maze 
(i.e. bfs, dfs, iddfs, ucs, greedy, a_star).
"""

class ContainerEntry:
    """
    Container used for the various search algorithms containing all pertinent 
    information to correctly sort them and determine the path used.
    """
    def __init__(self, state, cost, action, num_actions, parent, maze_env):
        self.state = state
        self.cost = cost
        self.action = action
        self.num_actions = num_actions
        self.parent = parent
        self.maze_env = maze_env

    def get_successors(self):
        """
        Return the successors (states that can be reached from the current 
        state) of a state collected from the container.
        """
        successors = []
        for action in self.maze_env.ACTIONS:
            successful, newState = self.maze_env.perform_action(self.state, 
                                                                action)
            if successful:
                successors.append(ContainerEntry(newState, self.cost 
                                                 + self.maze_env.
                                                 ACTION_COST[action], 
                                                 action, self.num_actions + 1, 
                                                 self, self.maze_env))
        return successors
    
    def __eq__(self, obj):
        """
        Determine if two container instances are equal
        """
        return self.state == obj.state and self.cost == obj.cost

    def __lt__(self, other):
        """
        Determine which container instance is less than another based on their 
        cost incurred
        """
        return self.cost < other.cost
    
    def __hash__(self):
        return hash((self.state))

class Search:
    """
    Class containing all the algorithms to solve the maze using various search 
    methods (bfs, dfs, iddfs, ucs, greedy, and a_star) and the heuristics used 
    for the informed search methods.
    """

    def __init__(self, maze_env):
        self.maze_env = maze_env
        self.distances = {}
        self.end_position = (self.maze_env.exit_row, self.maze_env.exit_col)


    # === Breadth First Search ================================================
    def search_bfs(self):
        """
        Find a path which solves the environment using Breadth First Search 
        (BFS).
        :return: path (list of actions, where each action is an element of 
                 MazeEnv.ACTIONS)
        """

        start = ContainerEntry(self.maze_env.get_init_state(), 0, None, 0, 
                               None, self.maze_env)
        container = [start]
        visited = set([start.state])

        while (len(container) > 0):
            node = container.pop(0)
            if (self.maze_env.is_solved(node.state)):
                actions = []
                while (node.action is not None):
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                return actions
            else:
                successors = node.get_successors()
                for successor in successors:
                    if successor.state not in visited:
                        visited.add(successor.state)
                        container.append(successor)

        return []
    
    # === Depth First Search ==================================================
    def search_dfs(self):
        """
        Find a path which solves the environment using Depth First Search
        (DFS).
        :return: path (list of actions, where each action is an element of 
                 MazeEnv.ACTIONS)
        """

        start = ContainerEntry(self.maze_env.get_init_state(), 0, None, 0, 
                               None, self.maze_env)
        container = [start]
        visited = set([start.state])

        while (len(container) > 0):
            node = container.pop(-1)
            if (self.maze_env.is_solved(node.state)):
                actions = []
                while (node.action is not None):
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                return actions
            else:
                successors = node.get_successors()
                for successor in successors:
                    if successor.state not in visited:
                        visited.add(successor.state)
                        container.append(successor)

        return []
    
    # === Iterative Deepening Depth First Search ==============================
    def search_iddfs(self):
        """
        Find a path which solves the environment using Iterative Deepening 
        Depth First Search (IDDFS).
        :return: path (list of actions, where each action is an element of 
                 MazeEnv.ACTIONS)
        """

        start = ContainerEntry(self.maze_env.get_init_state(), 0, None, 0,
                               None, self.maze_env)

        for depth in range(1, 1000):
            container = [start]
            visited = {start.state: 0}
            while (len(container) > 0):
                node = container.pop(-1)
                if node.num_actions > depth:
                    continue
                elif (self.maze_env.is_solved(node.state)):
                    actions = []
                    while (node.action is not None):
                        actions.append(node.action)
                        node = node.parent
                    actions.reverse()
                    return actions
                else:
                    successors = node.get_successors()
                    for successor in successors:
                        if successor.state not in visited.keys() or \
                           successor.cost < visited[successor.state]:
                            visited[successor.state] = successor.cost
                            container.append(successor)

        return []

    # === Uniform Cost Search =================================================
    def search_ucs(self):
        """
        Find a path which solves the environment using Uniform Cost Search 
        (UCS).
        :return: path (list of actions, where each action is an element of 
                 MazeEnv.ACTIONS)
        """

        start = ContainerEntry(self.maze_env.get_init_state(), 0, None, 0, 
                               None, self.maze_env)
        container = PriorityQueue()
        container.put((0, start))
        visited = {start.state: 0}

        while (container.qsize() > 0):
            node = container.get()[1]
            if (self.maze_env.is_solved(node.state)):
                actions = []
                while (node.action is not None):
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                return actions
            else:
                successors = node.get_successors()
                for successor in successors:
                    if successor.state not in visited.keys() or successor.cost\
                       < visited[successor.state]:
                        visited[successor.state] = successor.cost
                        container.put((successor.cost, successor))

        return []
    
    # === Greedy Best First Search ============================================
    def search_greedy(self):
        """
        Find a path which solves the environment using Greedy Best First 
        Search (Greedy). 
        :return: path (list of actions, where each action is an element of 
                 MazeEnv.ACTIONS)
        """

        start = ContainerEntry(self.maze_env.get_init_state(), 0, None, 0, 
                               None, self.maze_env)
        container = PriorityQueue()
        container.put((0, start))
        visited = {start.state: 0}
        
        while (container.qsize() > 0):
            node = container.get()[1]
            if (self.maze_env.is_solved(node.state)):
                actions = []
                while (node.action is not None):
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                return actions
            else:
                successors = node.get_successors()
                for successor in successors:
                    if successor.state not in visited.keys() or successor.cost\
                       < visited[successor.state]:
                        visited[successor.state] = successor.cost
                        container.put((self.compute_heuristic(successor.state),
                                       successor))

        return []

    # === A* Search ===========================================================
    def search_a_star(self):
        """
        Find a path which solves the environment using A* Search.
        :return: path (list of actions, where each action is an element of 
                 MazeEnv.ACTIONS)
        """

        start = ContainerEntry(self.maze_env.get_init_state(), 0, None, 0, 
                               None, self.maze_env)
        container = PriorityQueue()
        container.put((0, start))
        visited = {start.state: 0}
        
        while (container.qsize() > 0):
            node = container.get()[1]
            if (self.maze_env.is_solved(node.state)):
                actions = []
                while (node.action is not None):
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                return actions
            else:
                successors = node.get_successors()
                for successor in successors:
                    if successor.state not in visited.keys() or successor.cost\
                       < visited[successor.state]:
                        visited[successor.state] = successor.cost
                        container.put((self.compute_heuristic(successor.state) 
                                       + successor.cost, successor))

        return []
    
    # === Informed Search Heuristic ===========================================
    def compute_heuristic(self, state):
        """
        Compute a heuristic value h(n) for the given state.
        The heurisitcis is the eclidean distance between two points.
        :param state: given state (MazeState object)
        :return: a real number h(n)
        """

        currentPosition = (state.row, state.col)
        # Calculate the vertical and horizontal differences between two points
        vertical = abs(self.end_position[0] - currentPosition[0])
        horizontal = abs(self.end_position[1] - currentPosition[1])

        # If the distance between the two points has not been calculated before
        if (vertical, horizontal) not in self.distances.keys():
            self.distances[(vertical, horizontal)] = math.sqrt((vertical ** 2) 
                                                                + (horizontal 
                                                                   ** 2))
        return self.distances[(vertical, horizontal)]