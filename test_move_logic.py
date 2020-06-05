'''module for testing the move logic for chess.'''
import unittest
from unittest.mock import patch
from square import Square
from player import Player
from piece import Piece
from pieceType import PieceType
from chessColor import ChessColor
from standardBoard import StandardBoard
import move_logic as ml
import custom_exceptions as ce

class TestMoveLogic(unittest.TestCase):
    '''Class for testing the move logic for chess.'''
    @classmethod
    def setUpClass(cls):
        # TODO: use base Board class
        cls.board = StandardBoard()
        cls.player = Player(ChessColor.WHITE)

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

    @patch.object(ml, 'is_valid_king_destination')
    @patch.object(ml, 'is_valid_queen_destination')
    @patch.object(ml, 'is_valid_rook_destination')
    @patch.object(ml, 'is_valid_bishop_destination')
    @patch.object(ml, 'is_valid_knight_destination')
    @patch.object(ml, 'is_valid_pawn_destination')
    def test_is_valid_destination(
        self,
        pawn_mock,
        knight_mock,
        bishop_mock,
        rook_mock,
        queen_mock,
        king_mock
    ):
        # should call the appropriate fn based on the piece type
        pawn = Piece(PieceType.PAWN, ChessColor.WHITE)
        knight = Piece(PieceType.KNIGHT, ChessColor.WHITE)
        bishop = Piece(PieceType.BISHOP, ChessColor.WHITE)
        rook = Piece(PieceType.ROOK, ChessColor.WHITE)
        queen = Piece(PieceType.QUEEN, ChessColor.WHITE)
        king = Piece(PieceType.KING, ChessColor.WHITE)

        s1 = Square(0, 0)
        s2 = Square(1, 1)

        ml.is_valid_destination(pawn, s1, s2)
        ml.is_valid_destination(knight, s1, s2)
        ml.is_valid_destination(bishop, s1, s2)
        ml.is_valid_destination(rook, s1, s2)
        ml.is_valid_destination(queen, s1, s2)
        ml.is_valid_destination(king, s1, s2)

        pawn_mock.assert_called_once()
        knight_mock.assert_called_once()
        bishop_mock.assert_called_once()
        rook_mock.assert_called_once()
        queen_mock.assert_called_once()
        king_mock.assert_called_once()

        pawn_mock.assert_called_with(pawn, s1, s2)
        knight_mock.assert_called_with(knight, s1, s2)
        bishop_mock.assert_called_with(bishop, s1, s2)
        rook_mock.assert_called_with(rook, s1, s2)
        queen_mock.assert_called_with(queen, s1, s2)
        king_mock.assert_called_with(king, s1, s2)

    @patch.object(ml, 'square_is_in_bounds')
    def test_validate_move(self, siib_mock):
        '''test main logic for if a move is legal.'''
        white_piece = Piece(PieceType.QUEEN, ChessColor.WHITE)
        s1 = Square(0, 0)
        s1.piece = white_piece
        black_piece = Piece(PieceType.QUEEN, ChessColor.BLACK)
        s2 = Square(0, 1)
        s2.piece = black_piece
        # should raise error if start square not in bounds
        siib_mock.side_effect = [False, True]
        with self.assertRaises(ce.InvalidMoveException):
            ml.validate_move(s1, s2, self.board, self.player)

        # should raise error if end square not in bounds
        siib_mock.side_effect = [True, False]
        with self.assertRaises(ce.InvalidMoveException):
            ml.validate_move(s1, s2, self.board, self.player)
        # reset siib_mock
        siib_mock.side_effect = None
        siib_mock.return_value = True

        # should raise if squares are equal
        with self.assertRaises(ce.InvalidMoveException):
            ml.validate_move(s1, s1, self.board, self.player)

        # raise if no piece in start square
        with self.assertRaises(ce.InvalidMoveException):
            empty_start = Square(0, 0)
            ml.validate_move(empty_start, s2, self.board, self.player)
        
        # raise if moving piece color is not player's color
        with self.assertRaises(ce.InvalidMoveException):
            ml.validate_move(s2, s1, self.board, self.player)
        # raise if piece cannot move to end square because of its design
        # raise if piece cannot move due to a blocking piece
        # raise if move puts player into check
        # raise if moving piece color is same as end square piece color

if __name__ == '__main__':
    unittest.main()
