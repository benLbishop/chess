"""Module containing the King class."""
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.move_logic import game_state
from chessGame.enums import MoveSideEffect
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

    def attempt_castle(self, start, end, board):
        # 1) king has not moved
        if self.has_moved:
            raise InvalidMoveException('cannot castle if king has moved.')
        # 2) targeted rook has not moved (targeted rook must be player's piece)
        row_idx = start.row_idx
        rook_col_idx = board.NUM_COLS - 1 if end.col_idx > start.col_idx else 0
        rook_square = board.squares[row_idx][rook_col_idx]
        rook = rook_square.piece
        if not rook:
            raise InvalidMoveException('no rook found for castling')
        if rook.color is not self.color:
            raise InvalidMoveException('cannot castle with opponent rook')
        # 3) no pieces in between king and rook
        i = 1 if rook_col_idx > start.col_idx else -1
        cur_col_idx = start.col_idx + i
        while cur_col_idx != rook_col_idx:
            cur_square = board.squares[row_idx][cur_col_idx]
            if cur_square.is_occupied():
                raise InvalidMoveException('cannot castle with piece in between rook and king')
            cur_col_idx += i
        # 4) make sure king isn't in check or moves through check
        # (don't need to check if moves into check since that happens for every piece)
        start_checking_pieces = game_state.get_checking_pieces(board, self.color)
        if len(start_checking_pieces) > 0:
            raise InvalidMoveException('cannot castle while in check.')
        # TODO: pretty jank (aka very very jank)
        mid = board.squares[row_idx][start.col_idx + i]
        mid.add_piece(self)
        start.clear()
        mid_checking_pieces = game_state.get_checking_pieces(board, self.color)
        if len(mid_checking_pieces) > 0:
            raise InvalidMoveException('cannot castle while in check.')
        start.add_piece(self)
        mid.clear()

        # can successfully castle
        start_coords = (start.row_idx, start.col_idx)
        end_coords = (end.row_idx, end.col_idx)
        return (start_coords, end_coords, None, None, MoveSideEffect.CASTLE)

    def get_move_params(self, start_coords, end_coords, board):
        start_row, start_col = start_coords
        end_row, end_col = end_coords
        start = board.squares[start_row][start_col]
        end = board.squares[end_row][end_col]

        row_offset = abs(start_row - end_row)
        col_offset = abs(start_col - end_col)
        if row_offset == 0 and col_offset == 2:
            return self.attempt_castle(start, end, board)
        return super().get_move_params(start_coords, end_coords, board)
