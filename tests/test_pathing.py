"""module for testing the move logic."""
import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.player import Player
from chessGame.enums import ChessColor, MoveType
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

    def test_get_necessary_move_type(self):
        start_row, start_col = 4, 4
        start = Square(start_row, start_col)

        test_cases = [
            (Square(start_row + 1, start_col), MoveType.UP),
            (Square(start_row + 4, start_col), MoveType.UP),
            (Square(start_row - 1, start_col), MoveType.DOWN),
            (Square(start_row - 2, start_col), MoveType.DOWN),
            (Square(start_row, start_col + 1), MoveType.RIGHT),
            (Square(start_row, start_col + 5), MoveType.RIGHT),
            (Square(start_row, start_col - 1), MoveType.LEFT),
            (Square(start_row, start_col - 3), MoveType.LEFT),
            (Square(start_row + 1, start_col + 1), MoveType.UP_RIGHT),
            (Square(start_row + 6, start_col + 6), MoveType.UP_RIGHT),
            (Square(start_row + 1, start_col - 1), MoveType.UP_LEFT),
            (Square(start_row + 3, start_col - 3), MoveType.UP_LEFT),
            (Square(start_row - 1, start_col + 1), MoveType.DOWN_RIGHT),
            (Square(start_row - 2, start_col + 2), MoveType.DOWN_RIGHT),
            (Square(start_row - 1, start_col - 1), MoveType.DOWN_LEFT),
            (Square(start_row - 4, start_col - 4), MoveType.DOWN_LEFT),
        ]
        for dest, result in test_cases:
            self.assertEqual(pathing.get_necessary_move_type(start, dest), result)


    def test_get_next_square_indexes(self):
        squares = self.board.squares
        start_row, start_col = 2, 2
        start = squares[start_row][start_col]

        test_cases = [
            (MoveType.UP, (start_row + 1, start_col)),
            (MoveType.DOWN, (start_row - 1, start_col)),
            (MoveType.RIGHT, (start_row, start_col + 1)),
            (MoveType.LEFT, (start_row, start_col - 1)),
            (MoveType.UP_RIGHT, (start_row + 1, start_col + 1)),
            (MoveType.UP_LEFT, (start_row + 1, start_col - 1)),
            (MoveType.DOWN_RIGHT, (start_row - 1, start_col + 1)),
            (MoveType.DOWN_LEFT, (start_row - 1, start_col - 1))
        ]

        for move_type, result in test_cases:
            self.assertEqual(pathing.get_next_square_indexes(start, move_type), result)

if __name__ == '__main__':
    unittest.main()
