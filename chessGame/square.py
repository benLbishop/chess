"""module containing the Square class."""
from .enums import ChessColor

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
        return (self.row_idx, self.col_idx) == (other.row_idx, other.col_idx)

    def __lt__(self, other):
        return (self.row_idx, self.col_idx) < (other.row_idx, other.col_idx)

    def __le__(self, other):
        return (self.row_idx, self.col_idx) <= (other.row_idx, other.col_idx)

    @property
    def coords(self):
        """Get the coordinates for the square."""
        return (self.row_idx, self.col_idx)

    def is_occupied(self):
        """ returns a boolean indicating whether or not a piece is on this square. """
        return self.piece is not None
