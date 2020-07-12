"""module for testing the Piece class."""
import unittest
from unittest.mock import patch

from chessGame import constants, custom_exceptions
from chessGame.enums import ChessColor
from chessGame.move_logic import pathing
from chessGame.board import Board
from chessGame.pieces.piece import Piece

class PieceTest(unittest.TestCase):
    """Testing for the Piece class."""
    @classmethod
    def setUpClass(cls):
        cls.board = Board(constants.STD_BOARD_CONFIG)

    def tearDown(self):
        self.board.clear()

    def test_init(self):
        """tests the constructor."""
        black_p = Piece(ChessColor.BLACK)
        white_p = Piece(ChessColor.WHITE)
        self.assertEqual(black_p.color, ChessColor.BLACK)
        self.assertEqual(black_p._value, -1)
        self.assertEqual(black_p.has_moved, False)
        self.assertEqual(white_p.color, ChessColor.WHITE)
        self.assertEqual(white_p._value, -1)
        self.assertEqual(white_p.has_moved, False)

    def test_can_reach_square(self):
        p = Piece(ChessColor.BLACK)
        with self.assertRaises(NotImplementedError):
            p.can_reach_square(None, None)

    @patch.object(pathing, 'get_necessary_offset')
    def test_get_path_to_square(self, offset_mock):
        squares = self.board.squares
        start = squares[0][0]
        offset_mock.return_value = (0, 1)

        self.board.clear()
        moving_white_piece = Piece(ChessColor.WHITE)
        start.add_piece(moving_white_piece)
        white_piece = Piece(ChessColor.WHITE)
        black_piece = Piece(ChessColor.BLACK)
        squares[0][2].add_piece(white_piece)
        end2 = squares[0][3]
        # should raise if we come across a piece on square that's not destination
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            moving_white_piece.get_path_to_square(start, end2, self.board)

        # should raise if piece on destination is same color
        end3 = squares[0][2]
        with self.assertRaises(custom_exceptions.InvalidMoveException):
            moving_white_piece.get_path_to_square(start, end3, self.board)

        # should return safely if piece on destination is opponent's
        squares[0][2].add_piece(black_piece)
        res = moving_white_piece.get_path_to_square(start, end3, self.board)
        self.assertEqual(res, [squares[0][0], squares[0][1], squares[0][2]])

        # should return safely if no piece in path
        self.board.clear()
        res = moving_white_piece.get_path_to_square(start, end2, self.board)
        self.assertEqual(res, [squares[0][0], squares[0][1], squares[0][2], squares[0][3]])

        # TODO: many more tests

if __name__ == '__main__':
    unittest.main()
