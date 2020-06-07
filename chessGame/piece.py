"""module for the Piece class."""

class Piece:
    """Class representing a chess piece."""
    def __init__(self, name, color, row_idx, col_idx):
        self.name = name
        self.color = color
        self.row_idx = row_idx
        self.col_idx = col_idx

    def __str__(self):
        # TODO: test
        return "{} {}".format(self.color, self.name)