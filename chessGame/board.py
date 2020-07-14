"""module containing the Board class."""
from chessGame.pieces.queen import Queen
from .square import Square
from . import constants
from .custom_exceptions import PiecePlacementException, InvalidMoveException
from .enums import ChessColor, MoveSideEffect
from .move import Move
from .move_logic import game_state

class Board:
    """class representing a chess board of any size."""
    def __init__(self, board_config):
        self.NUM_ROWS = board_config['num_rows']
        self.NUM_COLS = board_config['num_cols']
        # TODO: have move_history. Should this be in Game class?
        self.last_move = None
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


    def _create_squares(self):
        min_rows = constants.MIN_BOARD_ROWS
        min_cols = constants.MIN_BOARD_COLS
        if self.NUM_ROWS < min_rows or self.NUM_COLS < min_cols:
            raise ValueError('Board dimensions must be {}x{} or larger'.format(min_rows, min_cols))

        self.squares = ([
            [Square(row_idx, col_idx) for col_idx in range(self.NUM_COLS)]
            for row_idx in range(self.NUM_ROWS)
        ])

    def clear(self):
        """empties all squares on the board."""
        for row in self.squares:
            for square in row:
                square.clear()

    def populate(self, piece_list):
        """places the given pieces on the board."""
        # TODO: clear board on failure?
        for piece, coordinate in piece_list:
            row_idx, col_idx = coordinate
            if row_idx >= self.NUM_ROWS or col_idx >= self.NUM_COLS:
                raise PiecePlacementException('piece out of bounds')
            square = self.squares[row_idx][col_idx]
            if square.is_occupied():
                raise PiecePlacementException('tried to place piece on occupied square')
            square.add_piece(piece)

    def _handle_castle_side_effect(self, move):
        """Method in charge of moving the rook that's part of a castle move."""
        row_idx, start_col_idx = move.start_coords
        _, end_col_idx = move.end_coords

        is_right_castle = end_col_idx > start_col_idx
        rook_start_col_idx = self.NUM_COLS - 1 if is_right_castle else 0
        rook_end_col_idx = start_col_idx + 1 if is_right_castle else start_col_idx - 1
        rook_start = self.squares[row_idx][rook_start_col_idx]
        rook_end = self.squares[row_idx][rook_end_col_idx]
        rook_end.add_piece(rook_start.piece)
        rook_start.clear()

    def _handle_en_passant_side_effect(self, move):
        """Method in charge of removing the piece captured via en passant."""
        row_idx, col_idx = move.captured_piece_coords
        captured_square = self.squares[row_idx][col_idx]
        captured_square.clear()

    def _handle_pawn_promotion_side_effect(self, move):
        """Method in charge of promoting pawns."""
        # TODO: this should actually ask the player what they want to promote the piece to.
        # For now, I'm just going to make it a queen
        row_idx, col_idx = move.end_coords
        end_square = self.squares[row_idx][col_idx]
        color = end_square.piece.color
        end_square.clear()
        end_square.add_piece(Queen(color))

    def _handle_move_side_effect(self, move):
        side_effect = move.side_effect
        if side_effect is MoveSideEffect.CASTLE:
            self._handle_castle_side_effect(move)
        elif side_effect is MoveSideEffect.EN_PASSANT:
            self._handle_en_passant_side_effect(move)
        elif side_effect is MoveSideEffect.PAWN_PROMOTION:
            self._handle_pawn_promotion_side_effect(move)
        else:
            raise NotImplementedError

    def move_piece(self, start_coords, end_coords, active_color):
        """Attempts to move a piece (if it exists) from the start to the end."""
        # TODO: split apart
        start_row, start_col = start_coords
        end_row, end_col = end_coords

        if start_row < 0 or start_row >= self.NUM_ROWS:
            raise ValueError('start row {} out of bounds.'.format(start_row))
        if start_col < 0 or start_col >= self.NUM_COLS:
            raise ValueError('start column {} out of bounds.'.format(start_col))
        if end_row < 0 or end_row >= self.NUM_ROWS:
            raise ValueError('end row {} out of bounds.'.format(end_row))
        if end_col < 0 or end_col >= self.NUM_COLS:
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
            move_params = moving_piece.get_move_params(start_coords, end_coords, self)
            move = Move(*move_params)
        except InvalidMoveException as err:
            raise err

        # actually move piece
        end_square.add_piece(moving_piece)
        start_square.clear()
        moving_piece.move_count += 1

        # NOTE: this is expected to be called after the piece is moved to the end square.
        # Things such as pawn promotion will break if this is done before moving the piece.
        if move.side_effect:
            self._handle_move_side_effect(move)

        self.last_move = move

        checking_pieces = game_state.get_checking_pieces(self, active_color)
        if len(checking_pieces) > 0:
            # cur_player put themselves in check, not allowed. Reset move
            self.undo_move()
            raise InvalidMoveException('player tried to put themselves in check')

        return move

    def undo_move(self):
        """Reverts the last move made on the board."""
        # TODO: Undo MoveSideEffects
        if not self.last_move:
            raise InvalidMoveException('no move to undo.')

        # TODO: maybe make Move have squares instead of coords
        start_row, start_col = self.last_move.start_coords
        end_row, end_col = self.last_move.end_coords
        last_start = self.squares[start_row][start_col]
        last_end = self.squares[end_row][end_col]
        moved_piece = last_end.piece

        moved_piece.move_count -= 1
        last_start.add_piece(moved_piece)
        last_end.clear()

        if self.last_move.captured_piece:
            captured_row, captured_col = self.last_move.captured_piece_coords
            captured_square = self.squares[captured_row][captured_col]
            captured_square.add_piece(self.last_move.captured_piece)

    def get_active_pieces(self):
        """gets the list of white and black pieces on the board."""
        white_pieces = []
        black_pieces = []
        for row_idx, row in enumerate(self.squares):
            for col_idx, square in enumerate(row):
                coordinate = (row_idx, col_idx)
                if square.is_occupied():
                    piece = square.piece
                    if piece.color == ChessColor.WHITE:
                        white_pieces.append((piece, coordinate))
                    else:
                        black_pieces.append((piece, coordinate))
        # return the pieces from highest value (should be king) to lowest
        return sorted(white_pieces, reverse=True), sorted(black_pieces, reverse=True)

class StandardBoard(Board):
    """class representing a chess board of the standard 8x8 size."""
    def __init__(self):
        super().__init__(constants.STD_BOARD_CONFIG)
