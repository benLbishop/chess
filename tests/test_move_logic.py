'''module for testing the move logic for chess.'''
import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.player import Player
from chessGame.piece import Piece
from chessGame.pieceType import PieceType
from chessGame.chessColor import ChessColor
from chessGame.chessEnums import MoveType
from chessGame.standardBoard import StandardBoard
import chessGame.move_logic as ml
import chessGame.custom_exceptions as ce

class TestMoveLogic(unittest.TestCase):
    '''Class for testing the move logic for chess.'''
    @classmethod
    def setUpClass(cls):
        # TODO: use base Board class
        cls.board = StandardBoard()
        cls.player = Player(ChessColor.WHITE)

    def tearDown(self):
        self.board.clear()

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

    def test_is_valid_pawn_destination(self):
        start_row = 3
        start_col = 3
        start = Square(start_row, start_col)
        # test white pawns
        valid_white_dests = [
            Square(start_row + 1, start_col),
            Square(start_row + 1, start_col + 1),
            Square(start_row + 1, start_col - 1),
            Square(start_row + 2, start_col),
        ]
        valid_black_dests = [
            Square(start_row - 1, start_col),
            Square(start_row - 1, start_col + 1),
            Square(start_row - 1, start_col - 1),
            Square(start_row - 2, start_col),
        ]
        # test valid cases
        for dest in valid_white_dests:
            self.assertTrue(ml.is_valid_pawn_destination(start, dest, ChessColor.WHITE))

        for dest in valid_black_dests:
            self.assertTrue(ml.is_valid_pawn_destination(start, dest, ChessColor.BLACK))

        # test invalid cases
        # wrong color test
        for dest in valid_white_dests:
            self.assertFalse(ml.is_valid_pawn_destination(start, dest, ChessColor.BLACK))

        for dest in valid_black_dests:
            self.assertFalse(ml.is_valid_pawn_destination(start, dest, ChessColor.WHITE))
        
        # bad distance tests
        invalid_dests = [
            Square(start_row, start_col + 1),
            Square(start_row + 2, start_col + 1),
            Square(start_row - 2, start_col + 1),
            Square(start_row + 4, start_col + 4)
        ]
        for dest in invalid_dests:
            self.assertFalse(ml.is_valid_pawn_destination(start, dest, ChessColor.WHITE))
            self.assertFalse(ml.is_valid_pawn_destination(start, dest, ChessColor.BLACK))



    def test_is_valid_knight_destination(self):
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
            self.assertTrue(ml.is_valid_knight_destination(start, dest))

        invalid_dests = [
            Square(start_row, start_col + 3),
            Square(start_row + 3, start_col),
            Square(start_row - 1, start_col + 1),
            Square(start_row + 4, start_col - 3)
        ]
        for dest in invalid_dests:
            self.assertFalse(ml.is_valid_knight_destination(start, dest))

    def test_is_valid_bishop_destination(self):
        start_row = 5
        start_col = 5
        start = Square(start_row, start_col)

        valid_dests = [
            Square(start_row + 1, start_col + 1),
            Square(start_row + 1, start_col - 1),
            Square(start_row - 1, start_col + 1),
            Square(start_row - 1, start_col - 1),
            Square(start_row + 4, start_col + 4),
            Square(start_row + 3, start_col - 3),
            Square(start_row - 3, start_col + 3),
            Square(start_row - 2, start_col - 2)
        ]
        for dest in valid_dests:
            self.assertTrue(ml.is_valid_bishop_destination(start, dest))

        invalid_dests = [
            Square(start_row, start_col + 1),
            Square(start_row + 3, start_col),
            Square(start_row + 2, start_col + 4),
            Square(start_row - 5, start_col + 4),
            Square(start_row - 3, start_col + 6),
        ]
        for dest in invalid_dests:
            self.assertFalse(ml.is_valid_bishop_destination(start, dest))

    def test_is_valid_rook_destination(self):
        start_row = 5
        start_col = 5
        start = Square(start_row, start_col)

        valid_dests = [
            Square(start_row, start_col + 1),
            Square(start_row, start_col + 4),
            Square(start_row, start_col - 2),
            Square(start_row, start_col + 3),
            Square(start_row + 2, start_col),
            Square(start_row + 8, start_col),
            Square(start_row - 1, start_col),
            Square(start_row - 3, start_col),
        ]
        for dest in valid_dests:
            self.assertTrue(ml.is_valid_rook_destination(start, dest))

        invalid_dests = [
            Square(start_row + 1, start_col + 1),
            Square(start_row + 3, start_col+ 1),
            Square(start_row - 2, start_col + 4),
            Square(start_row - 5, start_col + 1),
            Square(start_row - 3, start_col + 6),
        ]
        for dest in invalid_dests:
            self.assertFalse(ml.is_valid_rook_destination(start, dest))

    @patch.object(ml, 'is_valid_rook_destination')
    @patch.object(ml, 'is_valid_bishop_destination')
    def test_is_valid_queen_destination(self, bishop_mock, rook_mock):
        # just test bishop/knight functions, since queen is combo of those
        dummy_start = Square(0, 0)
        dummy_end = Square(1, 1)
        # can't have bishop and rook values both true, so don't need to test that case
        bishop_mock.return_value = True
        rook_mock.return_value = False
        self.assertTrue(ml.is_valid_queen_destination(dummy_start, dummy_end))

        bishop_mock.return_value = False
        rook_mock.return_value = True
        self.assertTrue(ml.is_valid_queen_destination(dummy_start, dummy_end))

        bishop_mock.return_value = False
        rook_mock.return_value = False
        self.assertFalse(ml.is_valid_queen_destination(dummy_start, dummy_end))

    def test_is_valid_king_destination(self):
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
            self.assertTrue(ml.is_valid_king_destination(start, dest))

        invalid_dests = [
            Square(start_row, start_col + 2),
            Square(start_row + 2, start_col),
            Square(start_row - 1, start_col + 2),
            Square(start_row + 4, start_col - 3)
        ]
        for dest in invalid_dests:
            self.assertFalse(ml.is_valid_king_destination(start, dest))

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

        # TODO: this needs to actually test that the piece type results in the proper method call
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

    @patch.object(ml, 'attempt_move')
    @patch.object(ml, 'square_is_in_bounds')
    def test_validate_move(self, siib_mock, attempt_move_mock):
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

        attempt_move_mock.side_effect = ce.InvalidMoveException('mocked exception')
        # raise if attempt_move fails
        with self.assertRaises(ce.InvalidMoveException):
            ml.validate_move(s1, s2, self.board, self.player)

        attempt_move_mock.side_effect = None

        
        
        # TODO: raise if move puts player into check

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
            self.assertEqual(ml.get_necessary_move_type(start, dest), result)


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
            self.assertEqual(ml.get_next_square_indexes(start, move_type), result)

    @patch.object(ml, 'get_next_square_indexes')
    def test_move_to_destination(self, get_next_square_mock):
        # should handle knights appropriately
        squares = self.board.squares
        start = squares[0][0]
        rook = Piece(PieceType.ROOK, ChessColor.WHITE)
        start.piece = rook
        white_pawn = Piece(PieceType.PAWN, ChessColor.WHITE)
        black_pawn = Piece(PieceType.PAWN, ChessColor.BLACK)
        squares[0][2].piece = white_pawn

        e1 = squares[0][3]
        # should raise if we come across a piece on square that's not destination
        get_next_square_mock.side_effect = [(0, 1), (0, 2)]
        with self.assertRaises(ce.InvalidMoveException):
            ml.move_to_destination(start, e1, self.board, MoveType.RIGHT, ChessColor.WHITE)
        
        # should raise if piece on destination is same color
        e2 = squares[0][2]
        get_next_square_mock.side_effect = [(0, 1), (0, 2)]
        with self.assertRaises(ce.InvalidMoveException):
            ml.move_to_destination(start, e2, self.board, MoveType.RIGHT, ChessColor.WHITE)

        # should return safely if piece on destination is opponent's
        squares[0][2].piece = black_pawn
        get_next_square_mock.side_effect = [(0, 1), (0, 2)]
        self.assertIsNone(ml.move_to_destination(start, e2, self.board, MoveType.RIGHT, ChessColor.WHITE))

        # should return safely if no piece in path
        self.board.clear()
        get_next_square_mock.side_effect = [(0, 1), (0, 2), (0, 3)]
        self.assertIsNone(ml.move_to_destination(start, e1, self.board, MoveType.RIGHT, ChessColor.WHITE))

        # TODO: many more tests. pawns, castling, etc

    @patch.object(ml, 'move_to_destination')
    @patch.object(ml, 'get_necessary_move_type')
    @patch.object(ml, 'is_valid_destination')
    def test_attempt_move(
            self,
            valid_dest_mock,
            gnmt_mock,
            move_mock
        ):
        start = Square(0, 0)
        end = Square(1, 1)
        pawn = Piece(PieceType.PAWN, ChessColor.WHITE)

        # raise if destination is not reachable
        valid_dest_mock.return_value = False
        with self.assertRaises(ce.InvalidMoveException):
            ml.attempt_move(pawn, start, end, self.board)

        valid_dest_mock.return_value = True

        # raise if move_to_destination throws
        move_mock.side_effect = ce.InvalidMoveException('mock exception')
        with self.assertRaises(ce.InvalidMoveException):
            ml.attempt_move(pawn, start, end, self.board)

        move_mock.side_effect = None
        # should successfully complete otherwise
        self.assertIsNone(ml.attempt_move(pawn, start, end, self.board))
if __name__ == '__main__':
    unittest.main()
