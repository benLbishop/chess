"""Module containing the Queen class."""
from .piece import Piece

class Queen(Piece):
    """class for the queen Piece."""
    def can_reach_square(self, start, end):
        """checks to see if movement from start_square to end_square is possible
            for a queen, pretending that no other pieces exist on the board.

            Returns a boolean.
        """
        # TODO: maybe reuse logic from Bishop/Rook classes?
        row_dist = abs(start.row_idx - end.row_idx)
        col_dist = abs(start.col_idx - end.col_idx)
        is_valid_bishop_move = row_dist == col_dist
        is_valid_rook_move = row_dist == 0 or col_dist == 0
        return is_valid_bishop_move or is_valid_rook_move
