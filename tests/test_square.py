"""module for testing the Square class."""
import unittest
from chessGame.enums import ChessColor
from chessGame.square import Square
from chessGame.pieces.piece import Piece

class TestSquare(unittest.TestCase):
    """tests for the Square class."""

    def setUp(self):
        self.test_square = Square(0, 0)

    def tearDown(self):
        self.test_square.piece = None

    def test_init(self):
        """Test the constructor."""
        with self.assertRaises(ValueError):
            Square(-1, 0)
        with self.assertRaises(ValueError):
            Square(0, -1)
        white_squares = [Square(0, 1), Square(3, 0), Square(8, 5), Square(3, 2)]
        black_squares = [Square(0, 0), Square(2, 0), Square(4, 6), Square(7, 1)]

        for w_s in white_squares:
            self.assertEqual(w_s.color, ChessColor.WHITE)
        for b_s in black_squares:
            self.assertEqual(b_s.color, ChessColor.BLACK)

    def test_is_occupied(self):
        """tests the is_occupied method."""
        self.assertFalse(self.test_square.is_occupied())

        self.test_square.piece = Piece(ChessColor.BLACK)
        self.assertTrue(self.test_square.is_occupied())

    def test_clear(self):
        """tests the clear method."""
        self.assertIsNone(self.test_square.piece)

        # test clear when no piece
        self.test_square.clear()
        self.assertIsNone(self.test_square.piece)

        self.test_square.piece = Piece(ChessColor.BLACK)
        self.test_square.clear()
        self.assertIsNone(self.test_square.piece)

    def test_add_piece(self):
        """tests the add_piece method."""
        p = Piece(ChessColor.BLACK)
        self.test_square.add_piece(p)
        self.assertEqual(self.test_square.piece, p)

if __name__ == '__main__':
    unittest.main()
