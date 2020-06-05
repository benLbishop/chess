"""Module for the Square class."""

class Square:
    """Class representing a square on the board."""

    def __init__(self, color, row_idx, col_idx):
        self.color = color
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.piece = None

    def is_occupied(self):
        return self.piece is not None

    def clear(self):
        self.piece = None