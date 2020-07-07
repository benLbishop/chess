"""module for testing the Square class."""
import unittest
from chessGame.enums import ChessColor
from chessGame.square import Square
from chessGame.piece import Piece

class TestSquare(unittest.TestCase):
    """tests for the Square class."""

    def setUp(self):
        self.test_square = Square(0, 0)

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

    def test_eq(self):
        """Test the equality magic function."""
        sq1 = Square(2, 5)
        sq2 = Square(2, 5)
        sq3 = Square(5, 2)
        sq4 = Square(0, 0)
        sq5 = Square(5, 2)

        self.assertEqual(sq1, sq2)
        self.assertEqual(sq3, sq5)
        self.assertNotEqual(sq1, sq3)
        self.assertNotEqual(sq1, sq4)
        self.assertNotEqual(sq2, sq5)


    def test_is_occupied(self):
        """tests the is_occupied method."""
        self.assertFalse(self.test_square.is_occupied())

        self.test_square.piece = Piece.from_string('b')
        self.assertTrue(self.test_square.is_occupied())

    def test_clear(self):
        """tests the clear method."""
        self.assertIsNone(self.test_square.piece)

        # test clear when no piece
        self.test_square.clear()
        self.assertIsNone(self.test_square.piece)

        self.test_square.piece = Piece.from_string('b')
        self.test_square.clear()
        self.assertIsNone(self.test_square.piece)


if __name__ == '__main__':
    unittest.main()
