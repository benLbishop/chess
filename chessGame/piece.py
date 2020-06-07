"""module for the Piece class."""

class Piece:
    """Class representing a chess piece."""
    def __init__(self, name, color, row_idx, col_idx):
        self.name = name
        self.color = color
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.has_moved = False # TODO: works for initial game state, but what about endgames?

    def __str__(self):
        # TODO: test
        return "{} {} at {}, {}".format(self.color, self.name, self.row_idx, self.col_idx)

    def __eq__(self, other):
        if self.name is not other.name:
            return False
        if self.color is not other.color:
            return False
        if self.row_idx != other.row_idx:
            return False
        if self.col_idx != other.col_idx:
            return False
        return True
