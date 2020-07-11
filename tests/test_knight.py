import unittest
from chessGame.square import Square
from chessGame.enums import ChessColor
from chessGame.pieces.knight import Knight

class KnightTest(unittest.TestCase):
    """class for testing the Knight class."""
    @classmethod
    def setUpClass(cls):
        cls.knight = Knight(ChessColor.BLACK)

    def test_can_reach_square(self):
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
            self.assertTrue(self.knight.can_reach_square(start, dest))

        invalid_dests = [
            Square(start_row, start_col + 3),
            Square(start_row + 3, start_col),
            Square(start_row - 1, start_col + 1),
            Square(start_row + 4, start_col - 3)
        ]
        for dest in invalid_dests:
            self.assertFalse(self.knight.can_reach_square(start, dest))