"""Module containing the King class."""
from chess_game.custom_exceptions import InvalidMoveException
from chess_game.enums import MoveSideEffect
from .piece import Piece

class King(Piece):
    """class for the king Piece."""
    def can_reach_square(self, start, end):
        """checks to see if movement from start_square to end_square is possible
            for a king, pretending that no other pieces exist on the board.

            Returns a boolean.
        """
        row_dist = abs(start.row_idx - end.row_idx)
        col_dist = abs(start.col_idx - end.col_idx)
        return row_dist < 2 and col_dist < 2

    def get_castle_params(self, start, end, board):
        """Attempts to get move parameters for castling.
            Should only be called if the king is moving horizontally 2 squares.
        """
        # 1) king has not moved
        if self.has_moved:
            raise InvalidMoveException('cannot castle if king has moved.')
        # 2) targeted rook has not moved (targeted rook must be player's piece)
        row_idx = start.row_idx
        rook_col_idx = board.max_col if end.col_idx > start.col_idx else 0
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
        # see if king starts in check
        start_checking_pieces = board.get_checking_pieces(self.color)
        if start_checking_pieces:
            raise InvalidMoveException('cannot castle while in check.')
        # see if king moves through check
        try:
            mid_coords = (row_idx, start.col_idx + i)
            board.move_piece(start.coords, mid_coords, self.color)
            board.undo_move()
        except (InvalidMoveException, ValueError):
            raise InvalidMoveException('cannot castle through check.')

        # can successfully castle
        return (start, end, None, None, MoveSideEffect.CASTLE)

    def get_move_params(self, start, end, board):
        # Overwritten to handle castling
        start_row, start_col = start.coords
        end_row, end_col = end.coords

        row_offset = abs(start_row - end_row)
        col_offset = abs(start_col - end_col)
        if row_offset == 0 and col_offset == 2:
            return self.get_castle_params(start, end, board)
        # king moves in a standard way otherwise
        return super().get_move_params(start, end, board)
