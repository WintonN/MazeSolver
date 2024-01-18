# Maze Solver

This is the code for the Maze Solver.

**maze_env.py**

This file contains a class representing a typical maze environment, storing the dimensions of the environment, initial 
player position, exit position, optimal path cost, the tile type of each grid position, and a list of all available 
actions.

~~~~~
__init__(filename)
~~~~~
Constructs a new instance based on the given input filename.


~~~~~
get_init_state()
~~~~~
Returns a MazeState object (see below) representing the initial state of the level.


~~~~~
perform_action(state, action)
~~~~~
Simulates the outcome of performing the given 'action' starting from the given 'state', where 'action' is an element of
MazeEnv.ACTIONS and 'state' is a MazeState object. Returns a tuple (success, next_state), where success is True (if the
action is valid and does not collide) or False (if the action is invalid or collides), and next_state is a MazeState
object.


~~~~~
is_solved(state)
~~~~~
Checks whether the given 'state' (a MazeState object) is solved (i.e. player at exit). Returns True (solved) or False 
(not solved).


~~~~~
render(state, path)
~~~~~
Prints a graphical representation of the given 'state' (a MazeState object) to the terminal and the path taken to 
reach that state (if included, a list of MazeState objects).


**maze_state.py**

This file contains a class representing a maze state, storing the position of the player.

~~~~~
__init__(row, col, gem_status)
~~~~~
Constructs a new GameState instance, where row and column are integers between 0 and n_rows, n_cols respectively.


**search.py**

This file contains two classes: 
    ContainerEntry - used to store relevent node information in the frontier during the search (i.e. current state, 
                     cost to reach this state, action performed to reach this state, number of actions performed since 
                     the start to reach this state, the parent node, and the maze environment)
    Search - contains the various search algorithms that can be performed (i.e. BFS, DFS, IDDFS, UCS, Greedy, and 
             A start), as well as the heuristic algorithm used (euclidean distance) for informed search algorithms
    
/!\/!\ ContainerEntry /!\/!\

~~~~~
__init__(state, cost, action, num_actions, parent, maze_env)
~~~~~
Constructs a new ContainerEntry object with all the relevant information necessary.


~~~~~
get_successors()
~~~~~
Returns a list of ContainerEntry objects that contain the possible states that can be reached from the current state 
in the ContainerEntry and all other relevant information (e.g. state is the new state, cost is the cost to reach the 
current state and the cost of the action to reach the new state, ...)


/!\/!\ Search /!\/!\

~~~~~
__init__(maze_env)
~~~~~
Initialise a search class for a given maze environment.


~~~~~
search_bfs()
~~~~~
Search for a solution in the given maze environment using Breadth First Search (BFS). This search method always 
returns the optimal solution and is an uninformed search method.


~~~~~
search_dfs()
~~~~~
Search for a solution in the given maze environment using Depth First Search (DFS). This search method does not always 
returns the optimal solution and is an uninformed search method.


~~~~~
search_iddfs()
~~~~~
Search for a solution in the given maze environment using Iterative Deepening Depth First Search (IDDFS). This search 
method always returns the optimal solution and is an uninformed search method.


~~~~~
search_ucs()
~~~~~
Search for a solution in the given maze environment using Uniform Cost Search (UCS). This search method always returns 
the optimal solution and is an uninformed search method.


~~~~~
search_greedy()
~~~~~
Search for a solution in the given maze environment using Greedy Best First Search (Greedy). This search method always 
returns the optimal solution.


~~~~~
search_a_star()
~~~~~
Search for a solution in the given maze environment using A Star (A*). This search method always returns the optimal 
solution.


~~~~~
compute_heuristic(state)
~~~~~
Computes the heuristic used for informed search methods (greedy and a_star). The heuristic used is eclidean distance.


**maze_solver.py**

This file contains a script to find a solution for the maze and evaluate the solution.

The script takes up to 3 command line arguments:
- search_type, which should be "bfs" or "dfs" "iddfs" or "ucs" or "greedy" or "a_star"
- maze_filename, which must be a valid testcase file (e.g. one of the provided files in the mazes directory)
- (optional) "-v" to enable visualisation of the resulting trajectory


**mazes**

A directory containing sample maze input files.

The format of a maze file is:
~~~~~
num_rows, num_cols
optimal path cost
grid_data (row 1)
...
grid_data (row num_rows)
~~~~~

Maze files can contain comments, starting with '#', which are ignored by the input file parser.