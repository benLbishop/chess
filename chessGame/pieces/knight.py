"""Module containing the Knight class."""
from .piece import Piece

class Knight(Piece):
    """class for the knight Piece."""
    def __str__(self):
        return "{} Knight".format(self.color)

    def can_reach_square(self, start, end):
        """checks to see if movement from start_square to end_square is possible
            for a knight, pretending that no other pieces exist on the board.

            Returns a boolean.
        """
        row_dist = abs(start.row_idx - end.row_idx)
        col_dist = abs(start.col_idx - end.col_idx)
        return (row_dist == 2 and col_dist == 1) or (row_dist == 1 and col_dist == 2)
