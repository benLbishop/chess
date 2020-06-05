"""Module for the Square class."""
from chessColor import ChessColor

class Square:
    """Class representing a square on the board."""

    def __init__(self, row_idx, col_idx):
        self.color = ChessColor.BLACK if (row_idx + col_idx) % 2 == 0 else ChessColor.WHITE
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.piece = None

    def is_occupied(self):
        return self.piece is not None

    def clear(self):
        self.piece = None