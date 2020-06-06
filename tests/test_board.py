"""module containing tests for the Board class."""
import unittest
from unittest.mock import patch
from chessGame import constants, board

class BoardTest(unittest.TestCase):
    """tests for the Board class."""
    @patch.object(board.Board, '_create_squares')
    def test_init(self, _create_squares_mock):
        """Test the constructor."""
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT

        test_board = board.Board(num_rows, num_cols)
        # if dimensions become customizable, make sure they're > 0
        self.assertEqual(test_board.NUM_ROWS, constants.STD_BOARD_WIDTH)
        self.assertEqual(test_board.NUM_COLS, constants.STD_BOARD_HEIGHT)
        _create_squares_mock.assert_called_once()

    def test_create_squares(self):
        """Tests the creation of the squares attribute for the board."""
        #raise exception if board is too small
        with self.assertRaises(ValueError):
            test_board = board.Board(1, 10)

        with self.assertRaises(ValueError):
            test_board = board.Board(10, 1)

        dimen_list = [
            (constants.STD_BOARD_WIDTH, constants.STD_BOARD_HEIGHT),
            (3, 5),
            (10, 7)
        ]
        for num_rows, num_cols in dimen_list:
            test_board = board.Board(num_rows, num_cols)
            self.assertEqual(len(test_board.squares), num_rows)
            for row in test_board.squares:
                self.assertEqual(len(row), num_cols)

    def test_clear(self):
        """Test the clearing function."""
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        test_board = board.Board(num_rows, num_cols)

        # TODO: decouple testing for this from Square logic
        # test clearing when board is already empty
        test_board.clear()
        for row in test_board.squares:
            for square in row:
                self.assertFalse(square.is_occupied())

        # test clearing when board has pieces
        # TODO

if __name__ == '__main__':
    unittest.main()
