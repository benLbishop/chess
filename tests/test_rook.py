"""Module for testing the Rook class."""
import unittest

from chessGame.square import Square
from chessGame.pieces.rook import Rook
from chessGame.enums import ChessColor
from chessGame import constants

class RookTest(unittest.TestCase):
    """class for testing the Rook class."""

    @classmethod
    def setUpClass(cls):
        cls.rook = Rook(ChessColor.BLACK)

    def test_init(self):
        """Tests for the class constructor."""
        rook = self.rook
        self.assertEqual(rook.char, constants.PIECE_CHARS['Rook'])
        self.assertEqual(rook._value, constants.PIECE_VALUES['Rook'])
        self.assertEqual(rook._offsets, constants.PIECE_OFFSETS['Rook'])

    def test_can_reach_square(self):
        """Tests the overwritten can_reach_square method."""
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
            self.assertTrue(self.rook.can_reach_square(start, dest))

        invalid_dests = [
            Square(start_row + 1, start_col + 1),
            Square(start_row + 3, start_col+ 1),
            Square(start_row - 2, start_col + 4),
            Square(start_row - 5, start_col + 1),
            Square(start_row - 3, start_col + 6),
        ]
        for dest in invalid_dests:
            self.assertFalse(self.rook.can_reach_square(start, dest))
