"""Module containing the Pawn class."""
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.enums import ChessColor, MoveSideEffect
from chessGame.move_logic import game_state
from .piece import Piece

class Pawn(Piece):
    """class for the pawn Piece."""
    def has_valid_move(self, cur_square, board):
        # TODO: test
        cur_coords = (cur_square.row_idx, cur_square.col_idx)
        offsets = []
        if self.color == ChessColor.WHITE:
            offsets = [(1, 0), (1, 1), (1, -1)]
        else:
            offsets = [(-1, 0), (-1, 1), (-1, -1)]
        # TODO: this logic is duplicated in the Piece class. just need different way to get move options
        has_move = False
        for offset in offsets:
            neighbor_coords = tuple(map(sum, zip(cur_coords, offset)))
            try:
                board.move_piece(cur_coords, neighbor_coords, self.color)
                checking_pieces = game_state.get_checking_pieces(board, self.color)
                board.undo_move()
                if len(checking_pieces) == 0:
                    has_move = True
                    break
            except InvalidMoveException:
                continue
            except ValueError:
                continue
        return has_move

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

    def attempt_en_passant_capture(self, start, end, board):
        # 1) The move must be diagonal. Should be true based on when this is called.
        # 2) There must be a pawn on the side of the diagonal move, but on the same row.
        passant_row_idx = start.row_idx
        passant_col_idx = end.col_idx
        passant_square = board.squares[passant_row_idx][passant_col_idx]
        passant_piece = passant_square.piece
        if not passant_piece:
            return None
        # 3) The piece must be an opposing player's pawn.
        if not isinstance(passant_piece, Pawn) or passant_piece.color is self.color:
            return None
        # 4) The pawn must have moved as the game's last move, and moved two squares.
        last_start_row, last_start_col = board.last_move.start_coords
        last_end_row, last_end_col = board.last_move.end_coords
        last_start = board.squares[last_start_row][last_start_col]
        last_end = board.squares[last_end_row][last_end_col]
        if last_end is not passant_square:
            return None
        last_row_offset = abs(last_start.row_idx - last_end.row_idx)
        # since it's an opponent's pawn moving, don't need to check col_offset,
        # since the row offset will only be 2 if we move straight ahead
        if last_row_offset != 2:
            return None
        return passant_piece

    def get_two_move_path(self, start, end, board):
        if self.has_moved:
            raise InvalidMoveException('Tried to move pawn two pieces after it had already moved.')
        start_row_idx = start.row_idx
        mid_row_idx = start_row_idx + 1 if self.color is ChessColor.WHITE else start_row_idx - 1
        mid = board.squares[mid_row_idx][start.col_idx]
        if mid.is_occupied() or end.is_occupied():
            raise InvalidMoveException('Pawn blocked from moving forward.')
        return [start, mid, end]

    def get_one_move_path(self, start, end, board):
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
        captured_piece = self.attempt_en_passant_capture(start, end, board)
        if not captured_piece:
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

    def get_move_params(self, start_coords, end_coords, board):
        # NOTE: A move is not returned because importing the Move class would cause a circular import.
        # TODO: test
        default_res = super().get_move_params(start_coords, end_coords, board)
        start_row, start_col = start_coords
        end_row, end_col = end_coords
        col_offset = abs(end_col - start_col)
        if col_offset != 0 and default_res[2] is None:
            # moved diagonally without capturing on that square. Performed en passant
            captured_coords = (start_row, end_col)
            captured_square = board.squares[captured_coords[0]][captured_coords[1]]
            captured_piece = captured_square.piece
            return (default_res[0], default_res[1], captured_piece, captured_coords, MoveSideEffect.EN_PASSANT)
        # TODO: this is omega clunky
        if self.color is ChessColor.WHITE and end_row == board.NUM_ROWS - 1:
            return (default_res[0], default_res[1], default_res[2], default_res[3], MoveSideEffect.PAWN_PROMOTION)
        if self.color is ChessColor.BLACK and end_row == 0:
            return (default_res[0], default_res[1], default_res[2], default_res[3], MoveSideEffect.PAWN_PROMOTION)
        return default_res
