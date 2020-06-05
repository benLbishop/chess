"""Testing module for the Board class."""

import unittest
import board
import constants

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.test_board = board.Board()

    def tearDown(self):
        pass

    def test_init(self):
        '''Test the constructor.'''
        self.assertEqual(self.test_board.width, constants.STD_BOARD_WIDTH)
        self.assertEqual(self.test_board.height, constants.STD_BOARD_HEIGHT)

    def test_create_squares(self):
        pass



if __name__ == '__main__':
    unittest.main()
