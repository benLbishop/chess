'''module for testing for the player class.'''
import unittest
from player import Player
from chessColor import ChessColor

class TestPlayer(unittest.TestCase):

    def test_init(self):
        white_p = Player(ChessColor.WHITE)
        black_p = Player(ChessColor.BLACK)

        self.assertEqual(white_p.color, ChessColor.WHITE)
        self.assertEqual(black_p.color, ChessColor.BLACK)

if __name__ == '__main__':
    unittest.main()
