"""module for testing for the Player class."""
import unittest
from chessGame.player import Player
from chessGame.enums import ChessColor

class TestPlayer(unittest.TestCase):
    """tests for the Player class."""

    def test_init(self):
        """tests the constructorr."""
        white_p = Player(ChessColor.WHITE)
        black_p = Player(ChessColor.BLACK)

        self.assertEqual(white_p.color, ChessColor.WHITE)
        self.assertEqual(black_p.color, ChessColor.BLACK)

if __name__ == '__main__':
    unittest.main()
