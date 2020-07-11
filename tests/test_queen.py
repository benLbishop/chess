import unittest

from chessGame.square import Square
from chessGame.enums import ChessColor
from chessGame.pieces.queen import Queen

class QueenTest(unittest.TestCase):
    """class for testing the Queen class."""
    @classmethod
    def setUpClass(cls):
        cls.queen = Queen(ChessColor.BLACK)

    def test_can_reach_square(self):
        start = Square(2, 2)
        
        good_ends = [
            Square(2, 1),
            Square(0, 2),
            Square(5, 5),
            Square(7, 2)
        ]

        bad_ends = [
            Square(3, 4),
            Square(7, 6),
            Square(0, 1)
        ]

        for end in good_ends:
            self.assertTrue(self.queen.can_reach_square(start, end))

        for end in bad_ends:
            self.assertFalse(self.queen.can_reach_square(start, end))