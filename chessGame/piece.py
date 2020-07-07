"""module for the Piece class."""
from . import conversion
class Piece:
    """Class representing a chess piece."""
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.has_moved = False # TODO: works for initial game state, but what about endgames?

    def __str__(self):
        return "{} {}".format(self.color, self.name)

    def __eq__(self, other):
        if self.name is not other.name:
            return False
        if self.color is not other.color:
            return False
        return True

    @classmethod
    def from_string(cls, piece_string):
        """creates a piece from a string."""
        params = conversion.parse_piece_string(piece_string)
        return cls(*params)
