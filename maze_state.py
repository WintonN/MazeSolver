"""
maze_state.py

This file contains a class representing a maze state.
"""


class MazeState:
    """
    Instance of a maze state. row and col represent the current player 
    position.
    """

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        if not isinstance(other, MazeState):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash(self.row + self.col)

    def __repr__(self):
        return f'row: {self.row},\t\t col: {self.col}'

    def deepcopy(self):
        return MazeState(self.row, self.col)