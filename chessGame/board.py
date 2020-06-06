"""module containing the Board class."""
from .square import Square
from . import constants

class Board:
    """class representing a chess board of any size."""
    def __init__(self, rows, cols):
        self.NUM_ROWS = rows
        self.NUM_COLS = cols
        self._create_squares()

    def _create_squares(self):
        min_rows = constants.MIN_BOARD_ROWS
        min_cols = constants.MIN_BOARD_COLS
        if self.NUM_ROWS < min_rows or self.NUM_COLS < min_cols:
            raise ValueError('Board dimensions too small, must be {0}x{1} or larger'.format(min_rows, min_cols))

        self.squares = [[Square(row_idx, col_idx) for col_idx in range(self.NUM_COLS)] for row_idx in range(self.NUM_ROWS)]

    def clear(self):
        """empties all squares on the board."""
        for row in self.squares:
            for square in row:
                square.piece = None

    def populate(self, piece_mapping):
        """places the given pieces on the board."""
        # TODO
