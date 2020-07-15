"""module containing the Board class."""
from collections import namedtuple

from .square import Square
from . import constants
from .custom_exceptions import PiecePlacementException, InvalidMoveException
from .enums import ChessColor, MoveSideEffect
from .move import Move

CheckingReturnType = namedtuple('CheckingReturnType', ['piece', 'path'])
class Board:
    """class representing a chess board of any size."""
    def __init__(self, board_config):
        self._num_rows = board_config['num_rows']
        self._num_cols = board_config['num_cols']
        self.move_history = []
        self._create_squares()

    def __str__(self):
        board_str = ''
        for row in self.squares:
            row_str = ''
            for square in row:
                if not square.is_occupied():
                    row_str = row_str + '. '
                else:
                    row_str = row_str + square.piece.char + ' '
            # adding from bottom up
            board_str = row_str + '\n' + board_str
        return board_str

    @property
    def max_row(self):
        """Returns the largest row index."""
        return self._num_rows - 1

    @property
    def max_col(self):
        """Returns the largest column index."""
        return self._num_cols - 1

    def _create_squares(self):
        min_rows = constants.MIN_BOARD_ROWS
        min_cols = constants.MIN_BOARD_COLS
        if self._num_rows < min_rows or self._num_cols < min_cols:
            raise ValueError('Board dimensions must be {}x{} or larger'.format(min_rows, min_cols))

        self.squares = ([
            [Square(row_idx, col_idx) for col_idx in range(self._num_cols)]
            for row_idx in range(self._num_rows)
        ])

    def clear(self):
        """resets the board."""
        for row in self.squares:
            for square in row:
                square.piece = None
        self.move_history = []

    def populate(self, piece_list):
        """places the given pieces on the board."""
        for piece, coordinate in piece_list:
            row_idx, col_idx = coordinate
            if row_idx > self.max_row or col_idx > self.max_col:
                self.clear()
                raise PiecePlacementException('piece out of bounds')
            square = self.squares[row_idx][col_idx]
            if square.is_occupied():
                self.clear()
                raise PiecePlacementException('tried to place piece on occupied square')
            square.piece = piece

    def _get_castling_rook_squares(self, move):
        row_idx, start_col_idx = move.start.coords
        _, end_col_idx = move.end.coords

        is_right_castle = end_col_idx > start_col_idx
        rook_start_col_idx = self.max_col if is_right_castle else 0
        rook_end_col_idx = start_col_idx + 1 if is_right_castle else start_col_idx - 1
        rook_start = self.squares[row_idx][rook_start_col_idx]
        rook_end = self.squares[row_idx][rook_end_col_idx]
        return (rook_start, rook_end)


    def _handle_castle_side_effect(self, move):
        """Method in charge of moving the rook that's part of a castle move."""
        rook_start, rook_end = self._get_castling_rook_squares(move)
        rook_end.piece = rook_start.piece
        rook_start.piece = None

    def _handle_en_passant_side_effect(self, move):
        """Method in charge of removing the piece captured via en passant."""
        row_idx, col_idx = move.captured_square.coords
        captured_square = self.squares[row_idx][col_idx]
        captured_square.piece = None

    def _handle_move_side_effect(self, move):
        side_effect = move.side_effect
        if side_effect is MoveSideEffect.CASTLE:
            self._handle_castle_side_effect(move)
        elif side_effect is MoveSideEffect.EN_PASSANT:
            self._handle_en_passant_side_effect(move)
        elif side_effect is MoveSideEffect.PAWN_PROMOTION:
            # NOTE: pawn promotion requires more input from the user, so it's not handled here.
            pass
        else:
            raise NotImplementedError

    def move_piece(self, start_coords, end_coords, active_color):
        """Attempts to move a piece (if it exists) from the start to the end."""
        start_row, start_col = start_coords
        end_row, end_col = end_coords

        if start_row < 0 or start_row > self.max_row:
            raise ValueError('start row {} out of bounds.'.format(start_row))
        if start_col < 0 or start_col > self.max_col:
            raise ValueError('start column {} out of bounds.'.format(start_col))
        if end_row < 0 or end_row > self.max_row:
            raise ValueError('end row {} out of bounds.'.format(end_row))
        if end_col < 0 or end_col > self.max_col:
            raise ValueError('end column {} out of bounds.'.format(end_col))

        if start_coords == end_coords:
            raise InvalidMoveException('cannot move to the same square.')

        start_square = self.squares[start_row][start_col]
        end_square = self.squares[end_row][end_col]

        moving_piece = start_square.piece
        if not moving_piece:
            raise InvalidMoveException('no piece on starting square.')
        if moving_piece.color is not active_color:
            raise InvalidMoveException('tried to move piece with different color.')

        move = None
        try:
            move_params = moving_piece.get_move_params(start_square, end_square, self)
            move = Move(*move_params)
        except InvalidMoveException as err:
            raise err

        # actually move piece
        end_square.piece = moving_piece
        start_square.piece = None
        moving_piece.move_count += 1

        # NOTE: this is expected to be called after the piece is moved to the end square.
        # Things such as pawn promotion will break if this is done before moving the piece.
        if move.side_effect:
            self._handle_move_side_effect(move)

        self.move_history.append(move)

        checking_pieces = self.get_checking_pieces(active_color)
        if len(checking_pieces) > 0:
            # cur_player put themselves in check, not allowed. Reset move
            self.undo_move()
            raise InvalidMoveException('player tried to put themselves in check')

        return move

    def _undo_castle_side_effect(self, move):
        """Undoes the side effect of castling, aka moving the rook."""
        rook_start, rook_end = self._get_castling_rook_squares(move)
        rook_start.piece = rook_end.piece
        rook_end.piece = None

    def undo_move(self):
        """Reverts the last move made on the board."""
        if not self.move_history:
            raise InvalidMoveException('no move to undo.')
        move = self.move_history.pop()

        last_start = move.start
        last_end = move.end
        moved_piece = last_end.piece

        moved_piece.move_count -= 1
        last_start.piece = moved_piece
        last_end.piece = None

        if move.captured_piece:
            captured_square = move.captured_square
            captured_square.piece = move.captured_piece

        # Pawn promotion and En Passant have been undone at this point. Castling has not
        if move.side_effect and move.side_effect is MoveSideEffect.CASTLE:
            self._undo_castle_side_effect(move)

    def get_checking_pieces(self, active_color):
        """Finds any pieces that have the player's king in check.
            If none found, returns an empty list.
        """
        white_mapping, black_mapping = self.get_active_pieces()
        player_piece_mapping = white_mapping
        opponent_piece_mapping = black_mapping
        if active_color is not ChessColor.WHITE:
            player_piece_mapping = black_mapping
            opponent_piece_mapping = white_mapping
        # king should always be first piece in array
        _, king_square = player_piece_mapping[0]

        checking_pieces = []
        for piece, piece_square in opponent_piece_mapping:
            try:
                path = piece.get_path_to_square(piece_square, king_square, self)
                # move from piece to king is valid, so it is checking king
                checking_pieces.append(CheckingReturnType(piece, path))
            except InvalidMoveException:
                continue
        return checking_pieces

    def get_active_pieces(self):
        """gets the list of white and black pieces on the board."""
        white_pieces = []
        black_pieces = []
        for row in self.squares:
            for square in row:
                if square.is_occupied():
                    piece = square.piece
                    if piece.color == ChessColor.WHITE:
                        white_pieces.append((piece, square))
                    else:
                        black_pieces.append((piece, square))
        # return the pieces from highest value (should be king) to lowest
        return sorted(white_pieces, reverse=True), sorted(black_pieces, reverse=True)

    @staticmethod
    def promote_pawn(pawn_square, new_piece):
        """Method in charge of promoting pawns."""
        color = pawn_square.piece.color
        pawn_square.piece = new_piece(color)

class StandardBoard(Board):
    """class representing a chess board of the standard 8x8 size."""
    def __init__(self):
        super().__init__(constants.STD_BOARD_CONFIG)
