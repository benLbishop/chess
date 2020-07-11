"""Module containing the Bishop class."""
from .piece import Piece

class Bishop(Piece):
    """class for the bishop Piece."""
    def can_reach_square(self, start, end):
        """checks to see if movement from start_square to end_square is possible
            for a bishop, pretending that no other pieces exist on the board.

            Returns a boolean.
        """
        row_dist = abs(start.row_idx - end.row_idx)
        col_dist = abs(start.col_idx - end.col_idx)
        return row_dist == col_dist
