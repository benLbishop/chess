"""Module containing the Knight class."""
from chessGame.custom_exceptions import InvalidMoveException
from .piece import Piece

class Knight(Piece):
    """class for the knight Piece."""
    def can_reach_square(self, start, end):
        """checks to see if movement from start to end is possible
            for a knight, pretending that no other pieces exist on the board.

            Returns a boolean.
        """
        row_dist = abs(start.row_idx - end.row_idx)
        col_dist = abs(start.col_idx - end.col_idx)
        return (row_dist == 2 and col_dist == 1) or (row_dist == 1 and col_dist == 2)

    def get_path_to_square(self, start, end, board):
        """Attempts to get the path for knights.
        Raises an InvalidMoveException if the move is illegal for some reason.
        """
        if not self.can_reach_square(start, end):
            raise InvalidMoveException('destination not reachable with piece')

        path = [start, end]
        if not end.is_occupied():
            return path, None
        # some piece on destination. Check color
        if end.piece.color is self.color:
            raise InvalidMoveException('cannot move into square occupied by player piece')
        # capturing opponent piece
        return path