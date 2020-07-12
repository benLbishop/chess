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
        self.white_pawn.has_moved = False
        self.black_pawn.has_moved = False

    def test_can_reach_square(self):
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

    def test_attempt_en_passant_capture(self):
        b = self.board
        wp = self.white_pawn
        bp = self.black_pawn
        # should not work if piece not in correct location
        white_start = b.squares[4][4]
        black_start = b.squares[3][4]

        self.assertIsNone(wp.attempt_en_passant_capture(b.squares[4][4], b.squares[5][5], b))

    @patch.object(Pawn, 'attempt_en_passant_capture')
    def test_get_one_move_path(self, passant_mock):
        passant_mock.return_value = None
        squares = self.board.squares
        r, c = 1, 1
        start = squares[r][c]
        straight1 = squares[r + 1][c]
        right_diag = squares[r + 1][c + 1]
        left_diag = squares[r + 1][c - 1]

        white_piece = Piece(ChessColor.WHITE)
        black_piece = Piece(ChessColor.BLACK)
        # should raise if straight move attempted and ANY piece in way
        straight1.add_piece(white_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight1, self.board)
        straight1.clear()

        straight1.add_piece(black_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight1, self.board)
        straight1.clear()

        # should raise if diagonal move attempted and no piece on end
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, right_diag, self.board)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, left_diag, self.board)

        # should raise if diagonal move attempted and player piece on end
        right_diag.add_piece(white_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, right_diag, self.board)
        right_diag.clear()

        left_diag.add_piece(white_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, left_diag, self.board)
        left_diag.clear()

        # should not raise if en passant is possible
        passant_return = 'dummy passant'
        passant_mock.return_value = passant_return
        res = self.white_pawn.get_path_to_square(start, left_diag, self.board)
        self.assertEqual(res, ([start, left_diag], passant_return))

        # should work otherwise TODO

    def test_get_two_move_path(self):
        squares = self.board.squares
        r, c = 1, 1
        start = squares[r][c]
        mid = squares[r + 1][c]
        end = squares[r + 2][c]

        black_piece = Piece(ChessColor.BLACK)
        # should raise if moving 2 squares and pawn has moved
        self.white_pawn.has_moved = True
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, end, self.board)

        self.white_pawn.has_moved = False

        # should raise if moving 2 is squares is valid, but blocking piece
        mid.add_piece(black_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, end, self.board)
        mid.clear()

        end.add_piece(black_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, end, self.board)
        end.clear()

        # should get the proper path for 2 otherwise
        res = self.white_pawn.get_path_to_square(start, end, self.board)
        self.assertEqual(res, ([start, mid, end], None))

    @patch.object(Pawn, 'get_two_move_path')
    @patch.object(Pawn, 'get_one_move_path')
    @patch.object(Pawn, 'can_reach_square')
    def test_get_path_to_square(self, reach_mock, one_move_mock, two_move_mock):
        one_move_return = 'one move return'
        two_move_return = 'two move return'
        reach_mock.return_value = True
        one_move_mock.return_value = one_move_return
        two_move_mock.return_value = two_move_return

        squares = self.board.squares
        r, c = 1, 1
        start = squares[r][c]
        straight1 = squares[r + 1][c]
        straight2 = squares[r + 2][c]
        right_diag = squares[r + 1][c + 1]
        left_diag = squares[r + 1][c - 1]

        reach_mock.return_value = False
        # should raise if piece cannot reach end square
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight1, self.board)
        reach_mock.return_value = True

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
