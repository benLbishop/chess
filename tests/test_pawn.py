"""Module for testing the Pawn class."""
import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.pieces.pawn import Pawn
from chessGame.pieces.piece import Piece
from chessGame.enums import ChessColor
from chessGame.board import Board
from chessGame import constants
from chessGame.custom_exceptions import InvalidMoveException

class PawnTest(unittest.TestCase):
    """class for testing the Pawn class."""
    @classmethod
    def setUpClass(cls):
        cls.white_pawn = Pawn(ChessColor.WHITE)
        cls.black_pawn = Pawn(ChessColor.BLACK)
        cls.board = Board(constants.STD_BOARD_CONFIG)

    def tearDown(self):
        self.board.clear()
        self.white_pawn.move_count = 0
        self.black_pawn.move_count = 0

    @patch.object(Piece, 'has_valid_move_in_list')
    def test_has_valid_move(self, valid_move_mock):
        """Tests the overwritten has_valid_move method."""
        white_pawn = Pawn(ChessColor.WHITE)
        black_pawn = Pawn(ChessColor.BLACK)
        cur_square = self.board.squares[0][0]

        # should call has_valid_move_in_list with the proper coordinates
        white_pawn.has_valid_move(cur_square, self.board)
        valid_move_mock.assert_called_with((0, 0), constants.WHITE_PAWN_OFFSETS, self.board)
        valid_move_mock.reset_mock()

        black_pawn.has_valid_move(cur_square, self.board)
        valid_move_mock.assert_called_with((0, 0), constants.BLACK_PAWN_OFFSETS, self.board)
        valid_move_mock.reset_mock()

        # should return what has_valid_move_in_list returns
        valid_move_mock.return_value = False
        res = white_pawn.has_valid_move(cur_square, self.board)
        self.assertFalse(res)
        res = black_pawn.has_valid_move(cur_square, self.board)
        self.assertFalse(res)

        valid_move_mock.return_value = True
        res = white_pawn.has_valid_move(cur_square, self.board)
        self.assertTrue(res)
        res = black_pawn.has_valid_move(cur_square, self.board)
        self.assertTrue(res)

    def test_can_reach_square(self):
        """Tests the overwritten can_reach_square method."""
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
            self.assertTrue(self.white_pawn.can_reach_square(start, dest))

        for dest in valid_black_dests:
            self.assertTrue(self.black_pawn.can_reach_square(start, dest))

        # test invalid cases
        # wrong color test
        for dest in valid_white_dests:
            self.assertFalse(self.black_pawn.can_reach_square(start, dest))

        for dest in valid_black_dests:
            self.assertFalse(self.white_pawn.can_reach_square(start, dest))

        # bad distance tests
        invalid_dests = [
            Square(start_row, start_col + 1),
            Square(start_row + 2, start_col + 1),
            Square(start_row - 2, start_col + 1),
            Square(start_row + 4, start_col + 4)
        ]
        for dest in invalid_dests:
            self.assertFalse(self.white_pawn.can_reach_square(start, dest))
            self.assertFalse(self.black_pawn.can_reach_square(start, dest))

    def test_can_capture_en_passant(self):
        """Tests for the can_capture_en_passant method."""
        b = self.board
        wp = self.white_pawn
        bp = self.black_pawn
        # should not work if piece not in correct location
        white_start = b.squares[4][4]
        black_start = b.squares[3][4]

        self.assertFalse(wp.can_capture_en_passant(b.squares[4][4], b.squares[5][5], b))

        # Should raise InvalidMoveException if board has no move_history

        # TODO

    @patch.object(Pawn, 'can_capture_en_passant')
    def test_get_one_move_path(self, passant_mock):
        """Tests for the get_one_move_path method."""
        passant_mock.return_value = None
        squares = self.board.squares
        row, col = 1, 1
        start = squares[row][col]
        straight1 = squares[row + 1][col]
        right_diag = squares[row + 1][col + 1]
        left_diag = squares[row + 1][col - 1]

        white_piece = Piece(ChessColor.WHITE)
        black_piece = Piece(ChessColor.BLACK)
        # should raise if straight move attempted and ANY piece in way
        straight1.add_piece(white_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_one_move_path(start, straight1, self.board)
        straight1.clear()

        straight1.add_piece(black_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_one_move_path(start, straight1, self.board)
        straight1.clear()

        # should raise if diagonal move attempted and no piece on end
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_one_move_path(start, right_diag, self.board)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_one_move_path(start, left_diag, self.board)

        # should raise if diagonal move attempted and player piece on end
        right_diag.add_piece(white_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_one_move_path(start, right_diag, self.board)
        right_diag.clear()

        left_diag.add_piece(white_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_one_move_path(start, left_diag, self.board)
        left_diag.clear()

        # should not raise if en passant is possible
        passant_return = 'dummy passant'
        passant_mock.return_value = passant_return
        res = self.white_pawn.get_one_move_path(start, left_diag, self.board)
        self.assertEqual(res, [start, left_diag])

        # should work otherwise TODO

    def test_get_two_move_path(self):
        """Tests for the get_two_move_path method."""
        squares = self.board.squares
        row, col = 1, 1
        start = squares[row][col]
        mid = squares[row + 1][col]
        end = squares[row + 2][col]

        black_piece = Piece(ChessColor.BLACK)
        # should raise if moving 2 squares and pawn has moved
        self.white_pawn.move_count = 1
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_two_move_path(start, end, self.board)

        self.white_pawn.move_count = 0

        # should raise if moving 2 is squares is valid, but blocking piece
        mid.add_piece(black_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_two_move_path(start, end, self.board)
        mid.clear()

        end.add_piece(black_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_two_move_path(start, end, self.board)
        end.clear()

        # should get the proper path for 2 otherwise
        res = self.white_pawn.get_two_move_path(start, end, self.board)
        self.assertEqual(res, [start, mid, end])

    @patch.object(Pawn, 'get_two_move_path')
    @patch.object(Pawn, 'get_one_move_path')
    @patch.object(Pawn, 'can_reach_square')
    def test_get_path_to_square(self, valid_move_mock, one_move_mock, two_move_mock):
        """Tests the overwritten get_path_to_square method."""
        one_move_return = 'one move return'
        two_move_return = 'two move return'
        valid_move_mock.return_value = True
        one_move_mock.return_value = one_move_return
        two_move_mock.return_value = two_move_return

        squares = self.board.squares
        row, col = 1, 1
        start = squares[row][col]
        straight1 = squares[row + 1][col]
        straight2 = squares[row + 2][col]
        right_diag = squares[row + 1][col + 1]
        left_diag = squares[row + 1][col - 1]

        valid_move_mock.return_value = False
        # should raise if piece cannot reach end square
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight1, self.board)
        valid_move_mock.return_value = True

        # should properly call two move and one move functions
        one_ends = [straight1, left_diag, right_diag]
        for end in one_ends:
            res = self.white_pawn.get_path_to_square(start, end, self.board)
            self.assertEqual(res, one_move_return)

        two_res = self.white_pawn.get_path_to_square(start, straight2, self.board)
        self.assertEqual(two_res, two_move_return)

        # should raise if moving one square fails
        one_move_mock.side_effect = InvalidMoveException('dummy exception')
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight1, self.board)
        one_move_mock.side_effect = None

        # should raise if moving two squares fails
        two_move_mock.side_effect = InvalidMoveException('dummy exception')
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight2, self.board)
        two_move_mock.side_effect = None

    def test_get_move_params(self):
        """Tests the overwritten get_move_params method."""
        # TODO
