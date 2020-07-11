import unittest

from chessGame.square import Square
from chessGame.pieces.pawn import Pawn
from chessGame.enums import ChessColor

class PawnTest(unittest.TestCase):
    """class for testing the Pawn class."""
    @classmethod
    def setUpClass(cls):
        cls.white_pawn = Pawn(ChessColor.WHITE)
        cls.black_pawn = Pawn(ChessColor.BLACK)

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