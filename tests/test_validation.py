"""module for testing the move logic."""
import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.player import Player
from chessGame.piece import Piece
from chessGame.enums import ChessColor, PieceType
from chessGame.board import Board
from chessGame import constants
from chessGame.move_logic import validation
import chessGame.custom_exceptions as ce

class TestMoveLogic(unittest.TestCase):
    """tests for the move logic."""

    @classmethod
    def setUpClass(cls):
        cls.board = Board(constants.STD_BOARD_CONFIG)
        cls.player = Player({'color': ChessColor.WHITE, 'name': 'Travis'})
        cls.opponent = Player({'color': ChessColor.BLACK, 'name': 'Justin'})

    def tearDown(self):
        self.board.clear()
        self.player.active_pieces = []
        self.opponent.active_pieces = []

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

    def test_is_valid_pawn_destination(self):
        start_row = 3
        start_col = 3
        start = Square(start_row, start_col)
        # test white pawns
        valid_white_dests = [
            Square(start_row + 1, start_col),
            Square(start_row + 1, start_col + 1),
            Square(start_row + 1, start_col - 1),
            Square(start_row + 2, start_col),
        ]
        valid_black_dests = [
            Square(start_row - 1, start_col),
            Square(start_row - 1, start_col + 1),
            Square(start_row - 1, start_col - 1),
            Square(start_row - 2, start_col),
        ]
        # test valid cases
        for dest in valid_white_dests:
            self.assertTrue(validation.is_valid_pawn_destination(start, dest, ChessColor.WHITE))

        for dest in valid_black_dests:
            self.assertTrue(validation.is_valid_pawn_destination(start, dest, ChessColor.BLACK))

        # test invalid cases
        # wrong color test
        for dest in valid_white_dests:
            self.assertFalse(validation.is_valid_pawn_destination(start, dest, ChessColor.BLACK))

        for dest in valid_black_dests:
            self.assertFalse(validation.is_valid_pawn_destination(start, dest, ChessColor.WHITE))

        # bad distance tests
        invalid_dests = [
            Square(start_row, start_col + 1),
            Square(start_row + 2, start_col + 1),
            Square(start_row - 2, start_col + 1),
            Square(start_row + 4, start_col + 4)
        ]
        for dest in invalid_dests:
            self.assertFalse(validation.is_valid_pawn_destination(start, dest, ChessColor.WHITE))
            self.assertFalse(validation.is_valid_pawn_destination(start, dest, ChessColor.BLACK))



    def test_is_valid_knight_destination(self):
        start_row = 3
        start_col = 3
        start = Square(start_row, start_col)

        valid_dests = [
            Square(start_row + 1, start_col + 2),
            Square(start_row + 1, start_col - 2),
            Square(start_row - 1, start_col + 2),
            Square(start_row - 1, start_col - 2),
            Square(start_row + 2, start_col + 1),
            Square(start_row + 2, start_col - 1),
            Square(start_row - 2, start_col + 1),
            Square(start_row - 2, start_col - 1)
        ]
        for dest in valid_dests:
            self.assertTrue(validation.is_valid_knight_destination(start, dest))

        invalid_dests = [
            Square(start_row, start_col + 3),
            Square(start_row + 3, start_col),
            Square(start_row - 1, start_col + 1),
            Square(start_row + 4, start_col - 3)
        ]
        for dest in invalid_dests:
            self.assertFalse(validation.is_valid_knight_destination(start, dest))

    def test_is_valid_bishop_destination(self):
        start_row = 5
        start_col = 5
        start = Square(start_row, start_col)

        valid_dests = [
            Square(start_row + 1, start_col + 1),
            Square(start_row + 1, start_col - 1),
            Square(start_row - 1, start_col + 1),
            Square(start_row - 1, start_col - 1),
            Square(start_row + 4, start_col + 4),
            Square(start_row + 3, start_col - 3),
            Square(start_row - 3, start_col + 3),
            Square(start_row - 2, start_col - 2)
        ]
        for dest in valid_dests:
            self.assertTrue(validation.is_valid_bishop_destination(start, dest))

        invalid_dests = [
            Square(start_row, start_col + 1),
            Square(start_row + 3, start_col),
            Square(start_row + 2, start_col + 4),
            Square(start_row - 5, start_col + 4),
            Square(start_row - 3, start_col + 6),
        ]
        for dest in invalid_dests:
            self.assertFalse(validation.is_valid_bishop_destination(start, dest))

    def test_is_valid_rook_destination(self):
        start_row = 5
        start_col = 5
        start = Square(start_row, start_col)

        valid_dests = [
            Square(start_row, start_col + 1),
            Square(start_row, start_col + 4),
            Square(start_row, start_col - 2),
            Square(start_row, start_col + 3),
            Square(start_row + 2, start_col),
            Square(start_row + 8, start_col),
            Square(start_row - 1, start_col),
            Square(start_row - 3, start_col),
        ]
        for dest in valid_dests:
            self.assertTrue(validation.is_valid_rook_destination(start, dest))

        invalid_dests = [
            Square(start_row + 1, start_col + 1),
            Square(start_row + 3, start_col+ 1),
            Square(start_row - 2, start_col + 4),
            Square(start_row - 5, start_col + 1),
            Square(start_row - 3, start_col + 6),
        ]
        for dest in invalid_dests:
            self.assertFalse(validation.is_valid_rook_destination(start, dest))

    @patch.object(validation, 'is_valid_rook_destination')
    @patch.object(validation, 'is_valid_bishop_destination')
    def test_is_valid_queen_destination(self, bishop_mock, rook_mock):
        # just test bishop/knight functions, since queen is combo of those
        dummy_start = Square(0, 0)
        dummy_end = Square(1, 1)
        # can't have bishop and rook values both true, so don't need to test that case
        bishop_mock.return_value = True
        rook_mock.return_value = False
        self.assertTrue(validation.is_valid_queen_destination(dummy_start, dummy_end))

        bishop_mock.return_value = False
        rook_mock.return_value = True
        self.assertTrue(validation.is_valid_queen_destination(dummy_start, dummy_end))

        bishop_mock.return_value = False
        rook_mock.return_value = False
        self.assertFalse(validation.is_valid_queen_destination(dummy_start, dummy_end))

    def test_is_valid_king_destination(self):
        start_row = 3
        start_col = 3
        start = Square(start_row, start_col)

        valid_dests = [
            Square(start_row, start_col + 1),
            Square(start_row, start_col - 1),
            Square(start_row + 1, start_col),
            Square(start_row + 1, start_col + 1),
            Square(start_row + 1, start_col - 1),
            Square(start_row - 1, start_col),
            Square(start_row - 1, start_col + 1),
            Square(start_row - 1, start_col - 1)
        ]
        for dest in valid_dests:
            self.assertTrue(validation.is_valid_king_destination(start, dest))

        invalid_dests = [
            Square(start_row, start_col + 2),
            Square(start_row + 2, start_col),
            Square(start_row - 1, start_col + 2),
            Square(start_row + 4, start_col - 3)
        ]
        for dest in invalid_dests:
            self.assertFalse(validation.is_valid_king_destination(start, dest))

    @patch.object(validation, 'is_valid_king_destination')
    @patch.object(validation, 'is_valid_queen_destination')
    @patch.object(validation, 'is_valid_rook_destination')
    @patch.object(validation, 'is_valid_bishop_destination')
    @patch.object(validation, 'is_valid_knight_destination')
    @patch.object(validation, 'is_valid_pawn_destination')
    def test_is_valid_destination(
            self,
            pawn_mock,
            knight_mock,
            bishop_mock,
            rook_mock,
            queen_mock,
            king_mock
        ):
        # should call the appropriate fn based on the piece type
        pawn = Piece(PieceType.PAWN, ChessColor.WHITE, 0, 0)
        knight = Piece(PieceType.KNIGHT, ChessColor.WHITE, 0, 0)
        bishop = Piece(PieceType.BISHOP, ChessColor.WHITE, 0, 0)
        rook = Piece(PieceType.ROOK, ChessColor.WHITE, 0, 0)
        queen = Piece(PieceType.QUEEN, ChessColor.WHITE, 0, 0)
        king = Piece(PieceType.KING, ChessColor.WHITE, 0, 0)

        start = Square(0, 0)
        end = Square(1, 1)

        # TODO: this needs to actually test that the piece type results in the proper method call
        validation.is_valid_destination(pawn, start, end)
        validation.is_valid_destination(knight, start, end)
        validation.is_valid_destination(bishop, start, end)
        validation.is_valid_destination(rook, start, end)
        validation.is_valid_destination(queen, start, end)
        validation.is_valid_destination(king, start, end)

        pawn_mock.assert_called_once()
        knight_mock.assert_called_once()
        bishop_mock.assert_called_once()
        rook_mock.assert_called_once()
        queen_mock.assert_called_once()
        king_mock.assert_called_once()

    @patch.object(validation, 'is_valid_destination')
    @patch.object(validation, 'square_is_in_bounds')
    def test_validate_move(self, siib_mock, valid_dest_mock):
        """test main logic for if a move is legal."""
        white_piece = Piece(PieceType.QUEEN, ChessColor.WHITE, 0, 0)
        start = Square(0, 0)
        start.piece = white_piece
        black_piece = Piece(PieceType.QUEEN, ChessColor.BLACK, 0, 0)
        end = Square(0, 1)
        end.piece = black_piece
        # should raise error if start square not in bounds
        siib_mock.side_effect = [False, True]
        with self.assertRaises(ce.InvalidMoveException):
            validation.validate_move(start, end, self.board, self.player)

        # should raise error if end square not in bounds
        siib_mock.side_effect = [True, False]
        with self.assertRaises(ce.InvalidMoveException):
            validation.validate_move(start, end, self.board, self.player)
        # reset siib_mock
        siib_mock.side_effect = None
        siib_mock.return_value = True

        # should raise if squares are equal
        with self.assertRaises(ce.InvalidMoveException):
            validation.validate_move(start, start, self.board, self.player)

        # raise if no piece in start square
        with self.assertRaises(ce.InvalidMoveException):
            empty_start = Square(0, 0)
            validation.validate_move(empty_start, end, self.board, self.player)

        # raise if moving piece color is not player's color
        with self.assertRaises(ce.InvalidMoveException):
            validation.validate_move(end, start, self.board, self.player)

        valid_dest_mock.return_value = False
        # raise if is_valid_destination is False
        with self.assertRaises(ce.InvalidMoveException):
            validation.validate_move(start, end, self.board, self.player)

        valid_dest_mock.return_value = True
        # should successfully complete otherwise
        self.assertIsNone(validation.validate_move(start, end, self.board, self.player))
