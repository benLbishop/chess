import unittest
from chessColor import ChessColor
from square import Square

class TestSquare(unittest.TestCase):

    def setUp(self):
        self.test_square = Square(ChessColor.WHITE)

    def test_init(self):
        '''Test the initial state after construction.'''
        white_square = Square(ChessColor.WHITE)
        black_square = Square(ChessColor.BLACK)

        self.assertEqual(white_square.color, ChessColor.WHITE)
        self.assertEqual(black_square.color, ChessColor.BLACK)

        # no piece to begin
        self.assertIsNone(white_square.piece)

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
