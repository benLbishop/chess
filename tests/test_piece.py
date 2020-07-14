"""module for testing the Piece class."""
import unittest
from unittest.mock import patch

from chessGame import constants
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.enums import ChessColor
from chessGame.square import Square
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
        self.assertEqual(black_p.move_count, 0)
        self.assertEqual(white_p.color, ChessColor.WHITE)
        self.assertEqual(white_p._value, -1)
        self.assertEqual(white_p.move_count, 0)

    @patch.object(Board, 'undo_move')
    @patch.object(Board, 'move_piece')
    def test_has_valid_move_in_list(self, move_mock, undo_mock):
        """Tests for the has_valid_move_in_list method."""
        moving_piece = Piece(ChessColor.WHITE)
        coords = (0, 0)
        target_list = [(1, 0), (2, 0)]

        # should return false if target square list is empty
        res = moving_piece.has_valid_move_in_list(coords, [], self.board)
        self.assertFalse(res)

        # should return false if piece cannot move to any square
        move_mock.side_effect = InvalidMoveException('move exception')
        res = moving_piece.has_valid_move_in_list(coords, target_list, self.board)
        self.assertFalse(res)
        move_mock.side_effect = None

        # should return true if any move is valid
        move_mock.side_effect = [[], ['something']]
        res = moving_piece.has_valid_move_in_list(coords, target_list, self.board)
        self.assertTrue(res)

        move_mock.side_effect = [['something'], []]
        res = moving_piece.has_valid_move_in_list(coords, target_list, self.board)
        self.assertTrue(res)

    @patch.object(Piece, 'has_valid_move_in_list')
    def test_has_valid_move(self, valid_move_mock):
        """Tests for the has_valid_move method."""
        p = Piece(ChessColor.WHITE)
        test_offsets = [(3, 4), (-98, 1), (400, -3)]
        p._offsets = test_offsets
        cur_square = self.board.squares[0][0]

        # should call has_valid_move_in_list with the proper coordinates
        p.has_valid_move(cur_square, self.board)
        valid_move_mock.assert_called_with((0, 0), test_offsets, self.board)

        # should return what has_valid_move_in_list returns
        valid_move_mock.return_value = False
        res = p.has_valid_move(cur_square, self.board)
        self.assertFalse(res)

        valid_move_mock.return_value = True
        res = p.has_valid_move(cur_square, self.board)
        self.assertTrue(res)

    def test_can_reach_square(self):
        """Makes sure can_reach_square is not implemented."""
        p = Piece(ChessColor.BLACK)
        with self.assertRaises(NotImplementedError):
            p.can_reach_square(None, None)

    def test_get_necessary_offset(self):
        """Tests the get_necessary_offset method."""
        start_row, start_col = 4, 4
        start = Square(start_row, start_col)
        p = Piece(ChessColor.BLACK)

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
            self.assertEqual(p.get_necessary_offset(start, dest), result)

    @patch.object(Piece, 'get_necessary_offset')
    @patch.object(Piece, 'can_reach_square')
    def test_get_path_to_square(self, reach_mock, offset_mock):
        """Tests for the get_path_to_square method."""
        offset_mock.return_value = (0, 1)

        squares = self.board.squares
        start = squares[0][0]
        end2 = squares[0][2]
        end3 = squares[0][3]
        short_path = [squares[0][0], squares[0][1], squares[0][2]]
        long_path = short_path[:] + [squares[0][3]]

        moving_white_piece = Piece(ChessColor.WHITE)
        white_piece = Piece(ChessColor.WHITE)
        black_piece = Piece(ChessColor.BLACK)
        start.add_piece(moving_white_piece)

        reach_mock.return_value = False
        # should raise if piece cannot reach end square
        with self.assertRaises(InvalidMoveException):
            moving_white_piece.get_path_to_square(start, end3, self.board)
        reach_mock.return_value = True

        # should raise if we come across a piece on square that's not destination
        end2.add_piece(white_piece)
        with self.assertRaises(InvalidMoveException):
            moving_white_piece.get_path_to_square(start, end3, self.board)

        # should raise if piece on destination is same color
        with self.assertRaises(InvalidMoveException):
            moving_white_piece.get_path_to_square(start, end2, self.board)
        end2.clear()
        # should return safely if piece on destination is opponent's
        end2.add_piece(black_piece)
        res = moving_white_piece.get_path_to_square(start, end2, self.board)
        self.assertEqual(res, short_path)

        # should return safely if no piece in path
        self.board.clear()
        res = moving_white_piece.get_path_to_square(start, end3, self.board)
        self.assertEqual(res, long_path)

        # TODO: many more tests

    @patch.object(Piece, 'get_path_to_square')
    def test_get_move_params(self, path_mock):
        """Tests for the get_move_params method."""
        start = self.board.squares[0][0]
        end = self.board.squares[1][0]
        moving_piece = Piece(ChessColor.WHITE)

        # should raise if path cannot be found
        path_mock.side_effect = InvalidMoveException('dummy exception')
        with self.assertRaises(InvalidMoveException):
            moving_piece.get_move_params(start, end, self.board)
        path_mock.side_effect = None

        # should return captured piece/coords if it occurs
        other_piece = Piece(ChessColor.BLACK)
        end.add_piece(other_piece)
        res = moving_piece.get_move_params(start, end, self.board)
        expected_res = (start, end, other_piece, end)
        self.assertEqual(res, expected_res)
        end.clear()

        # should return just the coordinates otherwise
        res = moving_piece.get_move_params(start, end, self.board)
        expected_res = (start, end, None, None)
        self.assertEqual(res, expected_res)

if __name__ == '__main__':
    unittest.main()
