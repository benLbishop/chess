"""module for testing the move logic."""
import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.player import Player
from chessGame.enums import ChessColor, MoveType
from chessGame.board import Board
from chessGame import constants, conversion
from chessGame.move_logic import pathing, validation
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

    @patch.object(Piece, 'get_path_to_square')
    @patch.object(validation, 'validate_move')
    def test_get_move_path(self, validate_move_mock, piece_mock):
        start = Square(0, 0)
        start.piece = Piece(ChessColor.BLACK)
        end = Square(1, 1)

        # raise if validate_move fails
        validate_move_mock.side_effect = InvalidMoveException('dummy exception')
        with self.assertRaises(InvalidMoveException):
            pathing.get_move_path(start, end, self.board, self.player)

        validate_move_mock.side_effect = None

        # raise if pieget_path_to_square throws
        piece_mock.side_effect = InvalidMoveException('mock exception')
        with self.assertRaises(InvalidMoveException):
            pathing.get_move_path(start, end, self.board, self.player)

        piece_mock.side_effect = None
        dummy_path = ['dummy', 'path']
        piece_mock.return_value = dummy_path
        # should successfully complete otherwise
        res = pathing.get_move_path(start, end, self.board, self.player)
        self.assertEqual(res, dummy_path)

if __name__ == '__main__':
    unittest.main()
