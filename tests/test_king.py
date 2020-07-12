import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.enums import ChessColor
from chessGame.pieces.king import King
from chessGame.pieces.rook import Rook
from chessGame.pieces.piece import Piece
from chessGame.board import StandardBoard
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.move_logic import game_state

class KingTest(unittest.TestCase):
    """class for testing the King class."""
    @classmethod
    def setUpClass(cls):
        cls.king = King(ChessColor.WHITE)

    def tearDown(self):
        self.king.has_moved = False

    def test_can_reach_square(self):
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

    @patch.object(game_state, 'get_checking_pieces')
    def test_attempt_castle(self, check_mock):
        check_mock.return_value = []

        king = self.king
        board = StandardBoard()
        left_rook = Rook(ChessColor.WHITE)
        right_rook = Rook(ChessColor.WHITE)
        left_square = board.squares[0][0]
        right_square = board.squares[0][7]

        king_square = board.squares[0][4]
        king_square.add_piece(self.king)
        left_target = board.squares[0][2]
        right_target = board.squares[0][6]

        # TODO: queenside castle tests, black king tests
        # should raise if king has moved
        king.has_moved = True
        with self.assertRaises(InvalidMoveException):
            king.attempt_castle(king_square, right_target, board)
        king.has_moved = False

        # should raise if no rook on end
        with self.assertRaises(InvalidMoveException):
            king.attempt_castle(king_square, right_target, board)
        right_square.add_piece(right_rook)
        # should raise if targeted rook is opponent's
        right_rook.color = ChessColor.BLACK
        with self.assertRaises(InvalidMoveException):
            king.attempt_castle(king_square, right_target, board)
        right_rook.color = ChessColor.WHITE

        # should raise if piece in between rook and king
        other_piece = Piece(ChessColor.WHITE)
        board.squares[0][5].add_piece(other_piece)
        with self.assertRaises(InvalidMoveException):
            king.attempt_castle(king_square, right_target, board)
        board.squares[0][5].clear()

        # should raise if king is in check when move starts
        check_mock.return_value = ['something']
        with self.assertRaises(InvalidMoveException):
            king.attempt_castle(king_square, right_target, board)
        check_mock.return_value = []
        # should raise if king attempts to move through check
        check_mock.side_effect = [[], ['something']]
        with self.assertRaises(InvalidMoveException):
            king.attempt_castle(king_square, right_target, board)
