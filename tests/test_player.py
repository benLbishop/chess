"""module for testing for the Player class."""
import unittest
from chessGame.player import Player
from chessGame.enums import ChessColor

class TestPlayer(unittest.TestCase):
    """tests for the Player class."""

    def test_init(self):
        """tests the constructorr."""
        white_config = {'color': ChessColor.WHITE, 'name': 'Griffin'}
        white_p = Player(white_config)
        black_config = {'color': ChessColor.BLACK, 'name': 'Justin'}
        black_p = Player(black_config)

        self.assertEqual(white_p.color, ChessColor.WHITE)
        self.assertEqual(white_p.name, white_config['name'])
        self.assertEqual(white_p.captured_pieces, [])
        self.assertEqual(black_p.color, ChessColor.BLACK)
        self.assertEqual(black_p.name, black_config['name'])
        self.assertEqual(black_p.captured_pieces, [])

        # TODO: test which names are allowed? Is empty string ok?

if __name__ == '__main__':
    unittest.main()
