"""module for testing the Piece class."""
import unittest
from chessGame.pieces.piece import Piece
from chessGame.enums import ChessColor

class PieceTest(unittest.TestCase):
    """Testing for the Piece class."""

    def test_init(self):
        """tests the constructor."""
        black_p = Piece(ChessColor.BLACK)
        white_p = Piece(ChessColor.WHITE)
        self.assertEqual(black_p.color, ChessColor.BLACK)
        self.assertEqual(black_p.has_moved, False)
        self.assertEqual(white_p.color, ChessColor.WHITE)
        self.assertEqual(white_p.has_moved, False)

    def test_can_reach_square(self):
        p = Piece(ChessColor.BLACK)
        with self.assertRaises(NotImplementedError):
            p.can_reach_square(None, None)

if __name__ == '__main__':
    unittest.main()
