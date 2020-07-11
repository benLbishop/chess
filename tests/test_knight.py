import unittest
from chessGame.square import Square
from chessGame.enums import ChessColor
from chessGame.pieces.knight import Knight
from chessGame.pieces.pawn import Pawn
from chessGame.board import Board
from chessGame import constants, custom_exceptions

class KnightTest(unittest.TestCase):
    """class for testing the Knight class."""
    @classmethod
    def setUpClass(cls):
        cls.knight = Knight(ChessColor.WHITE)
        cls.board = Board(constants.STD_BOARD_CONFIG)

    def tearDown(self):
        self.board.clear()

    def test_can_reach_square(self):
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

    def test_get_path_to_square(self):
        squares = self.board.squares
        start = squares[0][0]
        end = squares[2][1]

        # should return path if no piece on end_square
        res = self.knight.get_path_to_square(start, end, self.board)
        self.assertEqual(res, [end])

        # should raise if player's piece is on end_square
        end_pawn = Pawn(ChessColor.WHITE)
        end.add_piece(end_pawn)
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            self.knight.get_path_to_square(start, end, self.board)

        # should return path if opponent's piece is on end_square
        end_pawn.color = ChessColor.BLACK
        res = self.knight.get_path_to_square(start, end, self.board)
        self.assertEqual(res, [end])