"""Module for the Square class."""

class Square:
    """Class representing a square on the board."""

    def __init__(self, color):
        self.color = color
        self.piece = None

    def is_occupied(self):
        return self.piece is not None

    def clear(self):
        self.piece = None