"""Module containing the Rook class."""
from .piece import Piece

class Rook(Piece):
    """class for the rook Piece."""
    def __str__(self):
        return "{} Rook".format(self.color)

    def can_reach_square(self, start, end):
        """checks to see if movement from start_square to end_square is possible
            for a rook, pretending that no other pieces exist on the board.

            Returns a boolean.
        """
        row_dist = abs(start.row_idx - end.row_idx)
        col_dist = abs(start.col_idx - end.col_idx)
        return row_dist == 0 or col_dist == 0
