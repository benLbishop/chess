"""Module for testing the Queen class."""
import unittest

from chess_game.square import Square
from chess_game.enums import ChessColor
from chess_game.pieces.queen import Queen
from chess_game import constants

class QueenTest(unittest.TestCase):
    """class for testing the Queen class."""
    @classmethod
    def setUpClass(cls):
        cls.queen = Queen(ChessColor.BLACK)

    def test_init(self):
        """Tests for the class constructor."""
        queen = self.queen
        self.assertEqual(queen.char, constants.PIECE_CHARS['Queen'])
        self.assertEqual(queen._value, constants.PIECE_VALUES['Queen'])
        self.assertEqual(queen._offsets, constants.PIECE_OFFSETS['Queen'])

    def test_can_reach_square(self):
        """Tests the overwritten can_reach_square method."""
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
