"""module for testing the move logic."""
import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.player import Player
from chessGame.enums import ChessColor
from chessGame.board import Board
from chessGame import constants, custom_exceptions
from chessGame.move_logic import validation
from chessGame.pieces.piece import Piece

class TestMoveLogic(unittest.TestCase):
    """tests for the move logic."""

    @classmethod
    def setUpClass(cls):
        cls.board = Board(constants.STD_BOARD_CONFIG)
        cls.player = Player({'color': ChessColor.WHITE, 'name': 'Travis'})
        cls.opponent = Player({'color': ChessColor.BLACK, 'name': 'Justin'})

    def tearDown(self):
        self.board.clear()

    def test_square_is_in_bounds(self):
        # squares can't be constructed with negative bounds, so just test if row/col length exceeded
        num_rows = self.board.NUM_ROWS
        num_cols = self.board.NUM_COLS
        bad_row_square = Square(num_rows, 0)
        bad_col_square = Square(0, num_cols)
        good_square = Square(1, 1)

        self.assertFalse(validation.square_is_in_bounds(bad_row_square, self.board))
        self.assertFalse(validation.square_is_in_bounds(bad_col_square, self.board))
        self.assertTrue(validation.square_is_in_bounds(good_square, self.board))

    @patch.object(Piece, 'can_reach_square')
    @patch.object(validation, 'square_is_in_bounds')
    def test_validate_move(self, siib_mock, piece_mock):
        """test main logic for if a move is legal."""
        white_piece = Piece(ChessColor.WHITE)
        start = Square(0, 0)
        start.piece = white_piece
        black_piece = Piece(ChessColor.BLACK)
        end = Square(0, 1)
        end.piece = black_piece
        # should raise error if start square not in bounds
        siib_mock.side_effect = [False, True]
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            validation.validate_move(start, end, self.board, self.player)

        # should raise error if end square not in bounds
        siib_mock.side_effect = [True, False]
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            validation.validate_move(start, end, self.board, self.player)
        # reset siib_mock
        siib_mock.side_effect = None
        siib_mock.return_value = True

        # should raise if squares are equal
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            validation.validate_move(start, start, self.board, self.player)

        # raise if no piece in start square
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            empty_start = Square(0, 0)
            validation.validate_move(empty_start, end, self.board, self.player)

        # raise if moving piece color is not player's color
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            validation.validate_move(end, start, self.board, self.player)

        piece_mock.return_value = False
        # raise if is_valid_destination is False
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            validation.validate_move(start, end, self.board, self.player)

        piece_mock.return_value = True
        # should successfully complete otherwise
        self.assertIsNone(validation.validate_move(start, end, self.board, self.player))
