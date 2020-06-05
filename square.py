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

    def is_occupied(self):
        return self.piece is not None

    def clear(self):
        self.piece = None