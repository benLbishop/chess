"""module for the Piece class."""
class Piece:
    """Class representing a chess piece."""
    def __init__(self, color):
        self.color = color
        self.has_moved = False # TODO: works for initial game state, but what about endgames?

    def __str__(self):
        raise NotImplementedError
