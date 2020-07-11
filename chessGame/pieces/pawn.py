"""Module containing the Pawn class."""
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.enums import ChessColor
from .piece import Piece

class Pawn(Piece):
    """class for the pawn Piece."""
    def __str__(self):
        return "{} Pawn".format(self.color)

    def can_reach_square(self, start, end):
        """checks to see if movement from start to end is possible
            for a pawn, pretending that no other pieces exist on the board.

            Returns a boolean.
        """
        # TODO: incorporate en-passant
        row_offset = end.row_idx - start.row_idx
        col_offset = end.col_idx - start.col_idx
        # pawn can't move side to side or more than 2 rows
        if row_offset == 0 or abs(row_offset) > 2:
            return False

        if self.color == ChessColor.WHITE:
            if row_offset < 0:
                # white pawns can't move down in rows
                return False
            if row_offset == 2:
                # Only valid if column did not change.
                return col_offset == 0
        else:
            # ChessColor.BLACK
            if row_offset > 0:
                # black pawns can't move up in rows
                return False
            if row_offset == -2:
                # Only valid if column did not change.
                return col_offset == 0
        # abs(row_offset) should be 1 if we get here.
        # valid only if we move 0 or 1 columns
        return abs(col_offset) < 2

    def get_path_to_square(self, start, end, board):
        """Attempts to get the path from start to end given the piece is a pawn.

        Raises an InvalidMoveException if the move is illegal for some reason.
        """
        row_offset = end.row_idx - start.row_idx
        col_offset = end.col_idx - start.col_idx
        if abs(row_offset) == 2:
            if self.has_moved:
                raise InvalidMoveException('pawn tried moving 2 squares, but has already moved')
            # destination has been validated, so col_offset == 0
            if end.is_occupied():
                raise InvalidMoveException('pawn blocked straight ahead')
            start_row_idx = start.row_idx
            intermediate_row_idx = start_row_idx + 1 if row_offset > 0 else start_row_idx - 1
            intermediate_square = board.squares[intermediate_row_idx][start.col_idx]
            if intermediate_square.is_occupied():
                raise InvalidMoveException('pawn blocked straight ahead')
            return [intermediate_square, end]
        # row offset must be 1
        path = [end]
        if col_offset == 0:
            if end.is_occupied():
                raise InvalidMoveException('pawn blocked straight ahead')
            return path
        # abs(col_offset) must be 1
        # end must have a piece # TODO: En-passant
        if not end.is_occupied():
            raise InvalidMoveException('pawn cannot move diagonally without capturing')
        if end.piece.color is self.color:
            raise InvalidMoveException('cannot move into square occupied by player piece')
        return path        