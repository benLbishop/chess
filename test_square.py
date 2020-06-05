import unittest
from chessColor import ChessColor
from square import Square

class TestSquare(unittest.TestCase):

    def setUp(self):
        self.test_square = Square(0, 0)

    def test_init(self):
        '''Test the initial state after construction.'''
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
        self.assertFalse(self.test_square.is_occupied())

        # TODO: should I use a real piece?
        self.test_square.piece = 'dummy_piece'
        self.assertTrue(self.test_square.is_occupied())

    def test_clear(self):
        self.assertIsNone(self.test_square.piece)

        # test clear when no piece
        self.test_square.clear()
        self.assertIsNone(self.test_square.piece)

        # TODO: should I use a real piece?
        self.test_square.piece = 'dummy_piece'
        self.test_square.clear()
        self.assertIsNone(self.test_square.piece)


if __name__ == '__main__':
    unittest.main()
