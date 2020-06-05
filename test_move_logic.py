'''module for testing the move logic for chess.'''
import unittest
from unittest.mock import patch
from square import Square
from player import Player
from standardBoard import StandardBoard
import move_logic as ml
import custom_exceptions as ce

class TestMoveLogic(unittest.TestCase):
    '''Class for testing the move logic for chess.'''
    @classmethod
    def setUpClass(cls):
        # TODO: use base Board class
        cls.board = StandardBoard()
        cls.player = Player()

    def test_square_is_in_bounds(self):
        # squares cannot be constructed with negative bounds, so just test if row/col length exceeded
        num_rows = self.board.NUM_ROWS
        num_cols = self.board.NUM_COLS
        bad_row_square = Square(num_rows, 0)
        bad_col_square = Square(0, num_cols)
        good_square = Square(1, 1)

        self.assertFalse(ml.square_is_in_bounds(bad_row_square, self.board))
        self.assertFalse(ml.square_is_in_bounds(bad_col_square, self.board))
        self.assertTrue(ml.square_is_in_bounds(good_square, self.board))

    @patch.object(ml, 'square_is_in_bounds')
    def test_move_piece(self, siib_mock):
        '''test main logic for if a move is legal.'''
        # should raise error if start square not in bounds
        start_square = Square(0, 0)
        end_square = Square(0, 0)

        siib_mock.return_value = False
        with self.assertRaises(ce.InvalidMoveException):
            ml.move_piece(start_square, end_square, self.board, self.player)

        siib_mock.return_value = True

if __name__ == '__main__':
    unittest.main()
