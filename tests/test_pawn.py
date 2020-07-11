import unittest

from chessGame.square import Square
from chessGame.pieces.pawn import Pawn
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

    def test_get_path_to_square(self):
        squares = self.board.squares
        r, c = 1, 1
        # should handle pawns appropriately
        start = squares[r][c]
        # TODO: test ends for if moving pawn is black
        straight_end1 = squares[r + 1][c]
        straight_end2 = squares[r + 2][c]
        diag_end1 = squares[r + 1][c + 1]
        diag_end2 = squares[r + 1][c - 1]

        pawn = self.white_pawn
        start.add_piece(pawn)

        white_piece = Pawn(ChessColor.WHITE)
        black_piece = Pawn(ChessColor.BLACK)

        # should raise if straight move attempted and ANY piece in way
        straight_end1.add_piece(white_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight_end1, self.board)

        straight_end1.add_piece(black_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight_end1, self.board)

        # should raise if moving 2 squares and pawn has moved
        straight_end1.clear()
        straight_end2.clear()
        pawn.has_moved = True
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight_end2, self.board)

        pawn.has_moved = False

        # should raise if moving 2 is squares is valid, but blocking piece
        straight_end1.add_piece(black_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight_end2, self.board)

        straight_end1.clear()
        straight_end2.add_piece(black_piece)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, straight_end2, self.board)

        straight_end2.clear()

        # should get the proper path for 2 otherwise
        res = self.white_pawn.get_path_to_square(start, straight_end2, self.board)
        self.assertEqual(res, [straight_end1, straight_end2])

        # should raise if diagonal move attempted and no piece on end
        # and not performing En-Passant
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, diag_end1, self.board)
        with self.assertRaises(InvalidMoveException):
            self.white_pawn.get_path_to_square(start, diag_end2, self.board)