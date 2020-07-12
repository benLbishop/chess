"""module for testing the move logic."""
import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.player import Player
from chessGame.enums import ChessColor
from chessGame.board import Board
from chessGame import constants, conversion
from chessGame.move_logic import pathing
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.pieces.piece import Piece

pps = conversion.parse_piece_string
class TestMoveLogic(unittest.TestCase):
    """tests for the move logic."""

    @classmethod
    def setUpClass(cls):
        cls.board = Board(constants.STD_BOARD_CONFIG)
        cls.player = Player({'color': ChessColor.WHITE, 'name': 'Travis'})
        cls.opponent = Player({'color': ChessColor.BLACK, 'name': 'Justin'})

    def tearDown(self):
        self.board.clear()

    def test_get_necessary_offset(self):
        start_row, start_col = 4, 4
        start = Square(start_row, start_col)

        test_cases = [
            (Square(start_row + 1, start_col), (1, 0)),
            (Square(start_row + 4, start_col), (1, 0)),
            (Square(start_row - 1, start_col), (-1, 0)),
            (Square(start_row - 2, start_col), (-1, 0)),
            (Square(start_row, start_col + 1), (0, 1)),
            (Square(start_row, start_col + 5), (0, 1)),
            (Square(start_row, start_col - 1), (0, -1)),
            (Square(start_row, start_col - 3), (0, -1)),
            (Square(start_row + 1, start_col + 1), (1, 1)),
            (Square(start_row + 6, start_col + 6), (1, 1)),
            (Square(start_row + 1, start_col - 1), (1, -1)),
            (Square(start_row + 3, start_col - 3), (1, -1)),
            (Square(start_row - 1, start_col + 1), (-1, 1)),
            (Square(start_row - 2, start_col + 2), (-1, 1)),
            (Square(start_row - 1, start_col - 1), (-1, -1)),
            (Square(start_row - 4, start_col - 4), (-1, -1)),
        ]
        for dest, result in test_cases:
            self.assertEqual(pathing.get_necessary_offset(start, dest), result)


if __name__ == '__main__':
    unittest.main()
