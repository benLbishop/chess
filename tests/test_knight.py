"""Module for testing the Knight class."""
import unittest
from unittest.mock import patch

from chess_game.square import Square
from chess_game.enums import ChessColor
from chess_game.pieces.knight import Knight
from chess_game.pieces.piece import Piece
from chess_game.board import Board
from chess_game import constants, custom_exceptions

class KnightTest(unittest.TestCase):
    """class for testing the Knight class."""
    @classmethod
    def setUpClass(cls):
        cls.knight = Knight(ChessColor.WHITE)
        cls.board = Board(constants.STD_BOARD_CONFIG)

    def tearDown(self):
        self.board.clear()

    def test_init(self):
        """Tests for the class constructor."""
        knight = self.knight
        self.assertEqual(knight.char, constants.PIECE_CHARS['Knight'])
        self.assertEqual(knight._value, constants.PIECE_VALUES['Knight'])
        self.assertEqual(knight._offsets, constants.PIECE_OFFSETS['Knight'])

    def test_can_reach_square(self):
        """Tests the overwritten can_reach_square method."""
        start_row = 3
        start_col = 3
        start = Square(start_row, start_col)

        valid_dests = [
            Square(start_row + 1, start_col + 2),
            Square(start_row + 1, start_col - 2),
            Square(start_row - 1, start_col + 2),
            Square(start_row - 1, start_col - 2),
            Square(start_row + 2, start_col + 1),
            Square(start_row + 2, start_col - 1),
            Square(start_row - 2, start_col + 1),
            Square(start_row - 2, start_col - 1)
        ]
        for dest in valid_dests:
            self.assertTrue(self.knight.can_reach_square(start, dest))

        invalid_dests = [
            Square(start_row, start_col + 3),
            Square(start_row + 3, start_col),
            Square(start_row - 1, start_col + 1),
            Square(start_row + 4, start_col - 3)
        ]
        for dest in invalid_dests:
            self.assertFalse(self.knight.can_reach_square(start, dest))

    @patch.object(Knight, 'can_reach_square')
    def test_get_path_to_square(self, reach_mock):
        """Tests the overwritten get_path_to_square method."""
        squares = self.board.squares
        start = squares[0][0]
        end = squares[2][1]

        reach_mock.return_value = False
        # should raise if piece cannot reach end square
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            self.knight.get_path_to_square(start, end, self.board)
        reach_mock.return_value = True

        # should return path if no piece on end_square
        res = self.knight.get_path_to_square(start, end, self.board)
        self.assertEqual(res, ([start, end], None))

        # should raise if player's piece is on end_square
        end_piece = Piece(ChessColor.WHITE)
        end.piece = end_piece
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            self.knight.get_path_to_square(start, end, self.board)

        # should return path if opponent's piece is on end_square
        end_piece.color = ChessColor.BLACK
        res = self.knight.get_path_to_square(start, end, self.board)
        self.assertEqual(res, [start, end])
