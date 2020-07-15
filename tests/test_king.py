"""Module for testing the King class."""
import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.enums import ChessColor, MoveSideEffect
from chessGame.pieces.king import King
from chessGame.pieces.rook import Rook
from chessGame.pieces.piece import Piece
from chessGame.board import Board, StandardBoard
from chessGame.custom_exceptions import InvalidMoveException
from chessGame import constants

class KingTest(unittest.TestCase):
    """class for testing the King class."""
    @classmethod
    def setUpClass(cls):
        cls.king = King(ChessColor.WHITE)
        cls.board = StandardBoard()

    def tearDown(self):
        self.board.clear()
        self.king.move_count = 0

    def test_init(self):
        """Tests for the class constructor."""
        king = self.king
        self.assertEqual(king.char, constants.PIECE_CHARS['King'])
        self.assertEqual(king._value, constants.PIECE_VALUES['King'])
        self.assertEqual(king._offsets, constants.PIECE_OFFSETS['King'])

    def test_can_reach_square(self):
        """Tests the can_reach_square method."""
        start_row = 3
        start_col = 3
        start = Square(start_row, start_col)

        valid_dests = [
            Square(start_row, start_col + 1),
            Square(start_row, start_col - 1),
            Square(start_row + 1, start_col),
            Square(start_row + 1, start_col + 1),
            Square(start_row + 1, start_col - 1),
            Square(start_row - 1, start_col),
            Square(start_row - 1, start_col + 1),
            Square(start_row - 1, start_col - 1)
        ]
        for dest in valid_dests:
            self.assertTrue(self.king.can_reach_square(start, dest))

        invalid_dests = [
            Square(start_row, start_col + 2),
            Square(start_row + 2, start_col),
            Square(start_row - 1, start_col + 2),
            Square(start_row + 4, start_col - 3)
        ]
        for dest in invalid_dests:
            self.assertFalse(self.king.can_reach_square(start, dest))

    @patch.object(Board, 'undo_move')
    @patch.object(Board, 'move_piece')
    @patch.object(Board, 'get_checking_pieces')
    def test_get_castle_params(self, check_mock, move_mock, undo_mock):
        """tests the get_castle_params method."""
        check_mock.return_value = []

        king = self.king
        board = self.board
        left_rook = Rook(ChessColor.WHITE)
        right_rook = Rook(ChessColor.WHITE)
        left_square = board.squares[0][0]
        right_square = board.squares[0][7]

        king_square = board.squares[0][4]
        king_square.piece = self.king
        left_target = board.squares[0][2]
        right_target = board.squares[0][6]

        # TODO: queenside castle tests, black king tests
        # should raise if king has moved
        king.move_count = 1
        with self.assertRaises(InvalidMoveException):
            king.get_castle_params(king_square, right_target, board)
        king.move_count = 0

        # should raise if no rook on end
        with self.assertRaises(InvalidMoveException):
            king.get_castle_params(king_square, right_target, board)
        right_square.piece = right_rook
        # should raise if targeted rook is opponent's
        right_rook.color = ChessColor.BLACK
        with self.assertRaises(InvalidMoveException):
            king.get_castle_params(king_square, right_target, board)
        right_rook.color = ChessColor.WHITE

        # should raise if piece in between rook and king
        other_piece = Piece(ChessColor.WHITE)
        board.squares[0][5].piece = other_piece
        with self.assertRaises(InvalidMoveException):
            king.get_castle_params(king_square, right_target, board)
        board.squares[0][5].piece = None

        # should raise if king is in check when move starts
        check_mock.return_value = ['something']
        with self.assertRaises(InvalidMoveException):
            king.get_castle_params(king_square, right_target, board)
        check_mock.return_value = []

        # should raise if king attempts to move through check
        move_mock.side_effect = InvalidMoveException('move exception')
        with self.assertRaises(InvalidMoveException):
            king.get_castle_params(king_square, right_target, board)
        move_mock.side_effect = None

        # should return the value otherwise
        expected_res = (king_square, right_target, None, None, MoveSideEffect.CASTLE)
        res = king.get_castle_params(king_square, right_target, board)
        self.assertEqual(res, expected_res)

    @patch.object(Piece, 'get_move_params')
    @patch.object(King, 'get_castle_params')
    def test_get_move_params(self, castle_mock, move_mock):
        """Tests the overwritten get_move_params method."""
        castle_return = 'castling'
        std_return = 'std'
        castle_mock.return_value = castle_return
        move_mock.return_value = std_return
        # should call the appropriate methods
        castle_calls = [
            ((0, 4), (0, 2)),
            ((0, 4), (0, 6)),
            ((7, 4), (7, 2)),
            ((7, 4), (7, 6)),
            ((0, 0), (0, 2))
        ]
        for start_coords, end_coords in castle_calls:
            start = self.board.squares[start_coords[0]][start_coords[1]]
            end = self.board.squares[end_coords[0]][end_coords[1]]
            res = self.king.get_move_params(start, end, self.board)
            self.assertEqual(res, castle_return)

        std_calls = [
            ((0, 4), (0, 3)),
            ((0, 4), (1, 2)),
            ((7, 4), (7, 1)),
            ((7, 4), (6, 5))
        ]
        for start_coords, end_coords in std_calls:
            start = self.board.squares[start_coords[0]][start_coords[1]]
            end = self.board.squares[end_coords[0]][end_coords[1]]
            res = self.king.get_move_params(start, end, self.board)
            self.assertEqual(res, std_return)
