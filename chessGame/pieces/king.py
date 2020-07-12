"""Module containing the King class."""
from .piece import Piece

# TODO: override get_move to return castling side effect
class King(Piece):
    """class for the king Piece."""
    def can_reach_square(self, start, end):
        """checks to see if movement from start_square to end_square is possible
            for a king, pretending that no other pieces exist on the board.

            Returns a boolean.
        """
        # TODO: castling
        row_dist = abs(start.row_idx - end.row_idx)
        col_dist = abs(start.col_idx - end.col_idx)
        return row_dist < 2 and col_dist < 2
