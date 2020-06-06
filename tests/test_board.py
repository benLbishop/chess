"""Testing module for the Board class."""

import unittest
from chessGame import constants, board

class TestBoard(unittest.TestCase):
    def test_init(self):
        '''Test the constructor.'''
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT

        tb = board.Board(num_rows, num_cols)
        # if dimensions become customizable, make sure they're > 0
        self.assertEqual(tb.NUM_ROWS, constants.STD_BOARD_WIDTH)
        self.assertEqual(tb.NUM_COLS, constants.STD_BOARD_HEIGHT)
        # TODO: test if _create_squares is called? test _create_squares here?

    def test_create_squares(self):
        #raise exception if board is too small
        with self.assertRaises(ValueError):
            tb = board.Board(1, 10)

        with self.assertRaises(ValueError):
            tb = board.Board(10, 1)

        dimen_list = [
            (constants.STD_BOARD_WIDTH, constants.STD_BOARD_HEIGHT),
            (3, 5),
            (10, 7)
        ]
        for num_rows, num_cols in dimen_list:
            tb = board.Board(num_rows, num_cols)
            self.assertEqual(len(tb.squares), num_rows)
            for row in tb.squares:
                self.assertEqual(len(row), num_cols)

    def test_clear(self):
        '''Test the clearing function.'''
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        tb = board.Board(num_rows, num_cols)

        # TODO: decouple testing for this from Square logic
        # test clearing when board is already empty
        tb.clear()
        for row in tb.squares:
            for square in row:
                self.assertFalse(square.is_occupied())

        # test clearing when board has pieces
        # TODO



if __name__ == '__main__':
    unittest.main()
