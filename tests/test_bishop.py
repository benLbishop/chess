"""Module for testing the Bishop class."""
import unittest

from chess_game.square import Square
from chess_game.enums import ChessColor
from chess_game.pieces.bishop import Bishop
from chess_game import constants

class BishopTest(unittest.TestCase):
    """class for testing the Bishop class."""
    @classmethod
    def setUpClass(cls):
        cls.bishop = Bishop(ChessColor.BLACK)

    def test_init(self):
        """Tests for the class constructor."""
        bishop = self.bishop
        self.assertEqual(bishop.char, constants.PIECE_CHARS['Bishop'])
        self.assertEqual(bishop._value, constants.PIECE_VALUES['Bishop'])
        self.assertEqual(bishop._offsets, constants.PIECE_OFFSETS['Bishop'])

    def test_can_reach_square(self):
        """Tests the can_reach_square method."""
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
            self.assertTrue(self.bishop.can_reach_square(start, dest))

        invalid_dests = [
            Square(start_row, start_col + 1),
            Square(start_row + 3, start_col),
            Square(start_row + 2, start_col + 4),
            Square(start_row - 5, start_col + 4),
            Square(start_row - 3, start_col + 6),
        ]
        for dest in invalid_dests:
            self.assertFalse(self.bishop.can_reach_square(start, dest))
