"""module containing tests for the Board class."""
import unittest
from unittest.mock import patch
from chessGame.board import Board, StandardBoard
from chessGame import constants

class BoardTest(unittest.TestCase):
    """tests for the Board class."""
    @patch.object(Board, '_create_squares')
    def test_init(self, _create_squares_mock):
        """Test the constructor."""
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        boardConfig = {'num_rows': num_rows, 'num_cols': num_cols}

        test_board = Board(boardConfig)
        # if dimensions become customizable, make sure they're > 0
        self.assertEqual(test_board.NUM_ROWS, constants.STD_BOARD_WIDTH)
        self.assertEqual(test_board.NUM_COLS, constants.STD_BOARD_HEIGHT)
        _create_squares_mock.assert_called_once()

    def test_create_squares(self):
        """Tests the creation of the squares attribute for the board."""
        #raise exception if board is too small
        with self.assertRaises(ValueError):
            test_board = Board({'num_rows': 1, 'num_cols': 10})

        with self.assertRaises(ValueError):
            test_board = Board({'num_rows': 10, 'num_cols': 1})

        config_list = [
            {'num_rows': constants.STD_BOARD_WIDTH, 'num_cols': constants.STD_BOARD_HEIGHT},
            {'num_rows': 3, 'num_cols': 5},
            {'num_rows': 10, 'num_cols': 7}
        ]
        for config in config_list:
            test_board = Board(config)
            self.assertEqual(len(test_board.squares), config['num_rows'])
            for row in test_board.squares:
                self.assertEqual(len(row), config['num_cols'])

    def test_clear(self):
        """Test the clearing function."""
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        test_board = Board({'num_rows': num_rows, 'num_cols': num_cols})

        # TODO: decouple testing for this from Square logic
        # test clearing when board is already empty
        test_board.clear()
        for row in test_board.squares:
            for square in row:
                self.assertFalse(square.is_occupied())

        # test clearing when board has pieces
        # TODO

class StandardBoardTest(unittest.TestCase):
    """tests for the derived Board class StandardBoard."""

    def test_init(self):
        """tests for the constructor."""
        # should create an 8x8 board
        std_board = StandardBoard()
        self.assertEqual(std_board.NUM_ROWS, 8)
        self.assertEqual(std_board.NUM_COLS, 8)

if __name__ == '__main__':
    unittest.main()
