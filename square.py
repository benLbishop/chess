"""Module for the Square class."""
from chessColor import ChessColor

class Square:
    """Class representing a square on the board."""

    def __init__(self, row_idx, col_idx):
        if row_idx < 0:
            raise ValueError('row_idx for square cannot be negative')
        if col_idx < 0:
            raise ValueError('col_idx for square cannot be negative')
        self.color = ChessColor.BLACK if (row_idx + col_idx) % 2 == 0 else ChessColor.WHITE
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.piece = None

    def __eq__(self, other):
        if not isinstance(other, Square):
            # don't attempt to compare against unrelated types
            return NotImplemented
        # TODO: What if one square has a piece and the other doesn't? Can that happen?
        return self.row_idx == other.row_idx and self.col_idx == other.col_idx

    def is_occupied(self):
        return self.piece is not None

    def clear(self):
        self.piece = None