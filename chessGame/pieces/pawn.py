"""Module containing the Pawn class."""
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.enums import ChessColor, MoveSideEffect
from chessGame import constants
from .piece import Piece

class Pawn(Piece):
    """class for the pawn Piece."""
    def has_valid_move(self, cur_square, board):
        offsets = []
        if self.color == ChessColor.WHITE:
            offsets = constants.WHITE_PAWN_OFFSETS
        else:
            offsets = constants.BLACK_PAWN_OFFSETS
        neighbor_list = [tuple(map(sum, zip(cur_square.coords, offset))) for offset in offsets]
        return self.has_valid_move_in_list(cur_square.coords, neighbor_list, board)

    def can_reach_square(self, start, end):
        """checks to see if movement from start to end is possible
            for a pawn, pretending that no other pieces exist on the board.

            Returns a boolean.
        """
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

    def can_capture_en_passant(self, start, end, board):
        """Checks if an en passant capture is possible."""
        # 1) The move must be diagonal. Should be true based on when this is called.
        # 2) There must be a pawn on the side of the diagonal move, but on the same row.
        passant_row_idx = start.row_idx
        passant_col_idx = end.col_idx
        passant_square = board.squares[passant_row_idx][passant_col_idx]
        passant_piece = passant_square.piece
        if not passant_piece:
            return False
        # 3) The piece must be an opposing player's pawn.
        if not isinstance(passant_piece, Pawn) or passant_piece.color is self.color:
            return False
        # 4) The pawn must have moved as the game's last move, and moved two squares.
        last_move = board.move_history[-1]
        last_start = last_move.start
        last_end = last_move.end
        if last_end is not passant_square:
            return False
        last_row_offset = abs(last_start.row_idx - last_end.row_idx)
        # since it's an opponent's pawn moving, don't need to check col_offset,
        # since the row offset will only be 2 if we move straight ahead
        if last_row_offset != 2:
            return False
        return True

    def get_two_move_path(self, start, end, board):
        """Attempts to get a path for a pawn moving two squares.
            Should be called after the destination is valid.
        """
        if self.has_moved:
            raise InvalidMoveException('Tried to move pawn two pieces after it had already moved.')
        start_row_idx = start.row_idx
        mid_row_idx = start_row_idx + 1 if self.color is ChessColor.WHITE else start_row_idx - 1
        mid = board.squares[mid_row_idx][start.col_idx]
        if mid.is_occupied() or end.is_occupied():
            raise InvalidMoveException('Pawn blocked from moving forward.')
        return [start, mid, end]

    def get_one_move_path(self, start, end, board):
        """Attempts to get a path for a pawn moving one square."""
        path = [start, end]
        col_offset = end.col_idx - start.col_idx
        if col_offset == 0:
            if end.is_occupied():
                raise InvalidMoveException('Pawn blocked from moving forward.')
            return path
        # abs(col_offset) is 1, moving diagonally
        if end.is_occupied():
            # attempting capture. Make sure color is correct
            if end.piece.color is self.color:
                raise InvalidMoveException('Pawn cannot capture piece of same color.')
            return path
        # no piece in diagonal move. only possible with en passant
        if not self.can_capture_en_passant(start, end, board):
            raise InvalidMoveException('Pawn cannot move diagonally without capturing.')
        return path

    def get_path_to_square(self, start, end, board):
        """Attempts to get the path from start to end given the piece is a pawn.

        Raises an InvalidMoveException if the move is illegal for some reason.
        """
        if not self.can_reach_square(start, end):
            raise InvalidMoveException('destination not reachable with piece')

        row_offset = end.row_idx - start.row_idx
        if row_offset == 2:
            return self.get_two_move_path(start, end, board)
        # row_offset of 1
        return self.get_one_move_path(start, end, board)

    def get_move_params(self, start, end, board):
        try:
            self.get_path_to_square(start, end, board)
        except InvalidMoveException as err:
            raise err

        captured_piece, captured_square, side_effect = (None, None, None)
        start_row, start_col = start.coords
        end_row, end_col = end.coords
        col_offset = abs(end_col - start_col)
        if end.is_occupied():
            # moved diagonally and captured.
            captured_piece = end.piece
            captured_square = end
        else:
            if col_offset != 0:
                # moved diagonally without capturing on that square. Performed en passant
                captured_square = board.squares[start_row][end_col]
                captured_piece = captured_square.piece
                side_effect = MoveSideEffect.EN_PASSANT
            # moved straight. check for pawn promotion
            if self.color is ChessColor.WHITE and end_row == board.max_row:
                side_effect = MoveSideEffect.PAWN_PROMOTION
            if self.color is ChessColor.BLACK and end_row == 0:
                side_effect = MoveSideEffect.PAWN_PROMOTION
        return (start, end, captured_piece, captured_square, side_effect)
