"""Testing module for the Board class."""

import unittest
import board
import constants
from chessColor import ChessColor

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.test_board = board.Board(constants.STD_BOARD_WIDTH, constants.STD_BOARD_HEIGHT)

    def tearDown(self):
        pass

    def test_init(self):
        '''Test the constructor.'''
        tb = self.test_board
        # if dimensions become customizable, make sure they're > 0
        self.assertEqual(tb.NUM_ROWS, constants.STD_BOARD_WIDTH)
        self.assertEqual(tb.NUM_COLS, constants.STD_BOARD_HEIGHT)

        squares = tb.squares
        self.assertEqual(squares[0][0].color, ChessColor.BLACK)
        self.assertEqual(squares[self.test_board.NUM_ROWS - 1][self.test_board.NUM_COLS - 1].color, ChessColor.BLACK)
        self.assertEqual(squares[0][self.test_board.NUM_COLS - 1].color, ChessColor.WHITE)
        self.assertEqual(squares[self.test_board.NUM_ROWS - 1][0].color, ChessColor.WHITE)

    def test_clear(self):
        '''Test the clearing function.'''
        tb = self.test_board

        # TODO: decouple testing for this from Square logic
        # test clearing when board is already empty
        tb.clear()
        for row in self.test_board.squares:
            for square in row:
                self.assertFalse(square.is_occupied())

        # test clearing when board has pieces
        # TODO



if __name__ == '__main__':
    unittest.main()
