"""module containing the Board class."""
from .square import Square
from . import constants
from .custom_exceptions import PiecePlacementException

class Board:
    """class representing a chess board of any size."""
    def __init__(self, board_config):
        self.NUM_ROWS = board_config['num_rows']
        self.NUM_COLS = board_config['num_cols']
        self._create_squares()

    def __str__(self):
        # TODO: test
        board_str = ''
        for row in self.squares:
            row_str = ''
            for square in row:
                if not square.is_occupied():
                    row_str = row_str + '. '
                else:
                    # TODO: get actual piece
                    row_str = row_str + 'p '
            # adding from bottom up
            board_str = row_str + '\n' + board_str
        return board_str


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

    def populate(self, piece_list):
        """places the given pieces on the board."""
        # TODO: clear board on failure?
        for piece in piece_list:
            row_idx = piece.row_idx
            col_idx = piece.col_idx
            if row_idx >= self.NUM_ROWS or col_idx >= self.NUM_COLS:
                raise PiecePlacementException('piece out of bounds')
            if self.squares[row_idx][col_idx].is_occupied():
                raise PiecePlacementException('tried to place piece on occupied square')
            # TODO: might want an add_piece fn for squares to validate piece/square idxs
            self.squares[row_idx][col_idx].piece = piece

class StandardBoard(Board):
    """class representing a chess board of the standard 8x8 size."""
    def __init__(self):
        super().__init__(constants.STD_BOARD_CONFIG)
