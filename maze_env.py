from maze_state import MazeState

"""
maze_env.py

This file contains a class representation of the maze environment.
"""


class MazeEnv:
    """
    Instance of a maze environment. Stores the dimensions of the environment, 
    initial player position, exit position, optimal path cost, the tile type of
      each grid position, and a list of all available actions.

    The grid is indexed top to bottom, left to right (i.e. the top left corner 
    has coordinates (0, 0) and the bottomright corner has coordinates 
    (n_rows-1, n_cols-1)).
    """

    # Input  maze file symbols
    SOLID_TILE = 'X'
    AIR_TILE = ' '
    EXIT_TILE = 'E'
    PLAYER_TILE = 'P'
    VALID_TILES = {SOLID_TILE, AIR_TILE, EXIT_TILE, PLAYER_TILE}

    # Action symbols (i.e. output file symbols)
    LEFT = 'l'
    RIGHT = 'r'
    DOWN = 'd'
    UP = 'u'
    ACTIONS = [LEFT, RIGHT, DOWN, UP]
    ACTION_COST = {LEFT: 1.0, RIGHT: 1.0, DOWN: 1.0, UP: 1.0}

    def __init__(self, filename):
        """
        Process the given input file and create a new maze environment 
        instance based on the input file.
        :param filename: name of input file
        """

        try: # Try to open the maze input file
            f = open(filename, 'r')
        except FileNotFoundError:
            assert False, '/!\\ ERROR: Testcase file not found'

        grid_data = []
        i = 0

        for line in f: # Read the maze input file
            if line.strip()[0] == '#': # Skip commented lines in the file
                continue

            if i == 0: 
                try:
                    self.n_rows, self.n_cols = \
                        tuple([int(x) for x in line.strip().split(',')])
                except ValueError:
                    assert False, f'/!\\ ERROR: Invalid input file - n_rows \
                        and n_cols (line {i})'
            elif i == 1:
                try:
                    self.optimal_cost = int(line.strip())
                except ValueError:
                    assert False, f'/!\\ ERROR: Invalid input file - optimal \
                        path cost (line {i})'

            elif len(line.strip()) > 0:
                grid_data.append(list(line.strip()))
                assert len(grid_data[-1]) == self.n_cols,\
                    f'/!\\ ERROR: Invalid input file - incorrect map row \
                        length (line {i})'

            i += 1

        # Find initial and exit positions for the maze
        self.init_row, self.init_col = None, None
        self.exit_row, self.exit_col = None, None
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                if grid_data[r][c] == self.PLAYER_TILE:
                    assert self.init_row is None and self.init_col is None, \
                        '/!\\ ERROR: Invalid input file - more than one \
                            initial player position'
                    self.init_row, self.init_col = r, c
                    grid_data[r][c] = self.AIR_TILE
                elif grid_data[r][c] == 'E':
                    assert self.exit_row is None and self.exit_col is None, \
                        '/!\\ ERROR: Invalid input file - more than one exit \
                            position'
                    self.exit_row, self.exit_col = r, c
                    grid_data[r][c] = self.AIR_TILE
                elif grid_data[r][c] not in MazeEnv.VALID_TILES:
                    assert grid_data[r][c] in MazeEnv.VALID_TILES, \
                        '/!\\ ERROR: Invalid input file - invalid tile option'
                    
        assert self.init_row is not None and self.init_col is not None, \
            '/!\\ ERROR: Invalid input file - No player initial position'
        assert self.exit_row is not None and self.exit_col is not None, \
            '/!\\ ERROR: Invalid input file - No exit position'

        assert len(grid_data) == self.n_rows, f'/!\\ ERROR: Invalid input \
            file - incorrect number of map rows'

        self.grid_data = grid_data

    def get_init_state(self):
        """
        Get a state representation instance for the initial state.
        :return: initial state
        """
        return MazeState(self.init_row, self.init_col)

    def perform_action(self, state, action):
        """
        Perform the given action on the given state, and return whether the 
        action was successful (i.e. valid and collision free) and the 
        resulting new state.
        :param state: current MazeState
        :param action: an element of self.ACTIONS
        :return: (successful [True/False], next_state [MazeState])
        """
        # get coordinates for next state and clear zone states

        if action == self.LEFT:
            next_row, next_col = (state.row, state.col - 1)         # left 1

        elif action == self.RIGHT:
            next_row, next_col = (state.row, state.col + 1)         # right 1
        
        elif action == self.DOWN:
            next_row, next_col = (state.row + 1, state.col)         # down 1

        elif action == self.UP:
            next_row, next_col = (state.row - 1, state.col)         # up 1

        else:
            assert False, '/!\\ ERROR: Invalid action given to \
                perform_action()'

        # check that next_state is within bounds
        if not (0 <= next_row < self.n_rows and 0 <= next_col < self.n_cols):
            # next state is out of bounds
            return False, state.deepcopy()

        # check for a collision (with either next state or a clear zone state)
        if self.grid_data[next_row][next_col] == self.SOLID_TILE:
            # next state results in collision
            return False, state.deepcopy()
        

        return True, MazeState(next_row, next_col)

    def is_solved(self, state):
        """
        Check if the maze has been solved (i.e. player at exit)
        :param state: current MazeState
        :return: True if solved, False otherwise
        """
        return state.row == self.exit_row and state.col == self.exit_col  

    def render(self, state, path=None):
        """
        Render the maze's current state to terminal
        """
        for r in range(self.n_rows):
            line = ''
            for c in range(self.n_cols):
                # If the cell is part of the path to the solution
                if not path and (r, c) in path:
                    line += self.grid_data[r][c] + '0' + self.grid_data[r][c]
                # If the cell is the player
                elif state.row == r and state.col == c: 
                    line += self.grid_data[r][c] + 'P' + self.grid_data[r][c]
                # If the cell is the exit
                elif self.exit_row == r and self.exit_col == c: 
                    line += self.grid_data[r][c] + 'E' + self.grid_data[r][c]
                else:
                    line += self.grid_data[r][c] * 3
            print(line)
        print('\n')
