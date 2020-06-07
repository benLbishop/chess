"""module for testing the move logic."""
import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.player import Player
from chessGame.piece import Piece
from chessGame.enums import ChessColor, PieceType, MoveType
from chessGame.board import Board
from chessGame import constants
import chessGame.move_logic as ml
import chessGame.custom_exceptions as ce

class TestMoveLogic(unittest.TestCase):
    """tests for the move logic."""

    @classmethod
    def setUpClass(cls):
        cls.board = Board(constants.STD_BOARD_CONFIG)
        cls.player = Player({'color': ChessColor.WHITE, 'name': 'Travis'})
        cls.opponent = Player({'color': ChessColor.BLACK, 'name': 'Justin'})

    def tearDown(self):
        self.board.clear()
        self.player.active_pieces = []
        self.opponent.active_pieces = []

    def test_square_is_in_bounds(self):
        # squares can't be constructed with negative bounds, so just test if row/col length exceeded
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
        pawn = Piece(PieceType.PAWN, ChessColor.WHITE, 0, 0)
        knight = Piece(PieceType.KNIGHT, ChessColor.WHITE, 0, 0)
        bishop = Piece(PieceType.BISHOP, ChessColor.WHITE, 0, 0)
        rook = Piece(PieceType.ROOK, ChessColor.WHITE, 0, 0)
        queen = Piece(PieceType.QUEEN, ChessColor.WHITE, 0, 0)
        king = Piece(PieceType.KING, ChessColor.WHITE, 0, 0)

        start = Square(0, 0)
        end = Square(1, 1)

        # TODO: this needs to actually test that the piece type results in the proper method call
        ml.is_valid_destination(pawn, start, end)
        ml.is_valid_destination(knight, start, end)
        ml.is_valid_destination(bishop, start, end)
        ml.is_valid_destination(rook, start, end)
        ml.is_valid_destination(queen, start, end)
        ml.is_valid_destination(king, start, end)

        pawn_mock.assert_called_once()
        knight_mock.assert_called_once()
        bishop_mock.assert_called_once()
        rook_mock.assert_called_once()
        queen_mock.assert_called_once()
        king_mock.assert_called_once()

    @patch.object(ml, 'is_valid_destination')
    @patch.object(ml, 'square_is_in_bounds')
    def test_validate_move(self, siib_mock, valid_dest_mock):
        """test main logic for if a move is legal."""
        white_piece = Piece(PieceType.QUEEN, ChessColor.WHITE, 0, 0)
        start = Square(0, 0)
        start.piece = white_piece
        black_piece = Piece(PieceType.QUEEN, ChessColor.BLACK, 0, 0)
        end = Square(0, 1)
        end.piece = black_piece
        # should raise error if start square not in bounds
        siib_mock.side_effect = [False, True]
        with self.assertRaises(ce.InvalidMoveException):
            ml.validate_move(start, end, self.board, self.player)

        # should raise error if end square not in bounds
        siib_mock.side_effect = [True, False]
        with self.assertRaises(ce.InvalidMoveException):
            ml.validate_move(start, end, self.board, self.player)
        # reset siib_mock
        siib_mock.side_effect = None
        siib_mock.return_value = True

        # should raise if squares are equal
        with self.assertRaises(ce.InvalidMoveException):
            ml.validate_move(start, start, self.board, self.player)

        # raise if no piece in start square
        with self.assertRaises(ce.InvalidMoveException):
            empty_start = Square(0, 0)
            ml.validate_move(empty_start, end, self.board, self.player)

        # raise if moving piece color is not player's color
        with self.assertRaises(ce.InvalidMoveException):
            ml.validate_move(end, start, self.board, self.player)

        valid_dest_mock.return_value = False
        # raise if is_valid_destination is False
        with self.assertRaises(ce.InvalidMoveException):
            ml.validate_move(start, end, self.board, self.player)

        valid_dest_mock.return_value = True
        # should successfully complete otherwise
        self.assertIsNone(ml.validate_move(start, end, self.board, self.player))

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

    def test_get_pawn_path_to_destination(self):
        squares = self.board.squares
        r, c = 1, 1
        # should handle pawns appropriately
        start = squares[r][c]
        # TODO: test ends for if moving pawn is black
        straight_end1 = squares[r + 1][c]
        straight_end2 = squares[r + 2][c]
        diag_end1 = squares[r + 1][c + 1]
        diag_end2 = squares[r + 1][c - 1]

        pawn = Piece(PieceType.PAWN, ChessColor.WHITE, r, c)
        start.piece = pawn

        white_piece = Piece(PieceType.BISHOP, ChessColor.WHITE, 0, 0) # coords don't really matter
        black_piece = Piece(PieceType.BISHOP, ChessColor.BLACK, 0, 0) # coords don't really matter

        # should raise if straight move attempted and ANY piece in way
        straight_end1.piece = white_piece
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_pawn_path_to_destination(start, straight_end1, self.board, pawn)

        straight_end1.piece = black_piece
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_pawn_path_to_destination(start, straight_end1, self.board, pawn)

        # should raise if moving 2 squares and pawn has moved
        straight_end1.clear()
        straight_end2.clear()
        pawn.has_moved = True
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_pawn_path_to_destination(start, straight_end2, self.board, pawn)

        pawn.has_moved = False

        # should raise if moving 2 is squares is valid, but blocking piece
        straight_end1.piece = black_piece
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_pawn_path_to_destination(start, straight_end2, self.board, pawn)

        straight_end1.clear()
        straight_end2.piece = black_piece
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_pawn_path_to_destination(start, straight_end2, self.board, pawn)

        straight_end2.clear()

        # should get the proper path for 2 otherwise
        res = ml.get_pawn_path_to_destination(start, straight_end2, self.board, pawn)
        self.assertEqual(res, [straight_end1, straight_end2])

        # should raise if diagonal move attempted and no piece on end
        # and not performing En-Passant
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_path_to_destination(start, diag_end1, self.board, pawn)
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_path_to_destination(start, diag_end2, self.board, pawn)

    def test_get_knight_path_to_destination(self):
        squares = self.board.squares
        end = squares[2][1]
        knight = Piece(PieceType.KNIGHT, ChessColor.WHITE, 0, 0)

        # should raise if player's piece is on end_square
        end_pawn = Piece(PieceType.PAWN, ChessColor.WHITE, 2, 1)
        end.piece = end_pawn
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_knight_path_to_destination(end, knight)

        # should return path if opponent's piece is on end_square
        end_pawn.color = ChessColor.BLACK
        res = ml.get_knight_path_to_destination(end, knight)
        self.assertEqual(res, [end])

        # should return path if no piece on end_square
        self.board.clear()
        res = ml.get_knight_path_to_destination(end, knight)
        self.assertEqual(res, [end])

    @patch.object(ml, 'get_next_square_indexes')
    @patch.object(ml, 'get_necessary_move_type')
    def test_get_others_path_to_destination(self, gnmt_mock, get_next_square_mock):
        squares = self.board.squares
        start = squares[0][0]
        gnmt_mock.return_value = MoveType.RIGHT

        self.board.clear()
        rook = Piece(PieceType.ROOK, ChessColor.WHITE, 0, 0)
        start.piece = rook
        white_pawn = Piece(PieceType.PAWN, ChessColor.WHITE, 0, 0)
        black_pawn = Piece(PieceType.PAWN, ChessColor.BLACK, 0, 0)
        squares[0][2].piece = white_pawn
        end2 = squares[0][3]
        # should raise if we come across a piece on square that's not destination
        get_next_square_mock.side_effect = [(0, 1), (0, 2)]
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_others_path_to_destination(start, end2, self.board, rook)

        # should raise if piece on destination is same color
        end3 = squares[0][2]
        get_next_square_mock.side_effect = [(0, 1), (0, 2)]
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_others_path_to_destination(start, end3, self.board, rook)

        # should return safely if piece on destination is opponent's
        squares[0][2].piece = black_pawn
        get_next_square_mock.side_effect = [(0, 1), (0, 2)]
        res = ml.get_others_path_to_destination(start, end3, self.board, rook)
        self.assertEqual(res, [squares[0][1], squares[0][2]])

        # should return safely if no piece in path
        self.board.clear()
        get_next_square_mock.side_effect = [(0, 1), (0, 2), (0, 3)]
        res = ml.get_others_path_to_destination(start, end2, self.board, rook)
        self.assertEqual(res, [squares[0][1], squares[0][2], squares[0][3]])

        # TODO: many more tests
    
    @patch.object(ml, 'get_others_path_to_destination')
    @patch.object(ml, 'get_knight_path_to_destination')
    @patch.object(ml, 'get_pawn_path_to_destination')
    def test_get_path_to_destination(self, pptd_mock, kptd_mock, optd_mock):
        # TODO: break up/clean up this test
        squares = self.board.squares
        start = squares[0][0]

        pawn_return_val = ['pawn', 'path']
        pptd_mock.return_value = pawn_return_val

        knight_return_val = ['knight', 'path']
        kptd_mock.return_value = knight_return_val

        # should call pawn function if appropriate
        # should raise if pawn function raises
        pawn = Piece(PieceType.PAWN, ChessColor.WHITE, 0, 0)
        pawn_end = squares[1][0]
        pptd_mock.side_effect = ce.InvalidMoveException('dummy exception')
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_path_to_destination(start, pawn_end, self.board, pawn)

        # should return the pawn's function response otherwise
        pptd_mock.side_effect = None
        res = ml.get_path_to_destination(start, pawn_end, self.board, pawn)
        self.assertEqual(res, pawn_return_val)

        # should handle knights appropriately
        # should raise if knight function raises
        knight = Piece(PieceType.KNIGHT, ChessColor.WHITE, 0, 0)
        knight_end = squares[2][1]
        kptd_mock.side_effect = ce.InvalidMoveException('dummy exception')
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_path_to_destination(start, knight_end, self.board, knight)

        # should return the knights's function response otherwise
        kptd_mock.side_effect = None
        res = ml.get_path_to_destination(start, knight_end, self.board, knight)
        self.assertEqual(res, knight_return_val)

        # should handle other piece types properly
        other_pieces = [
            Piece(PieceType.ROOK, ChessColor.WHITE, 0, 0),
            Piece(PieceType.BISHOP, ChessColor.WHITE, 0, 0),
            Piece(PieceType.QUEEN, ChessColor.WHITE, 0, 0),
            Piece(PieceType.KING, ChessColor.WHITE, 0, 0)
        ]
        optd_mock.side_effect = ce.InvalidMoveException('dummy exception')
        for piece in other_pieces:
            with self.assertRaises(ce.InvalidMoveException):
                ml.get_path_to_destination(start, knight_end, self.board, piece)

        optd_mock.side_effect = None
        dummy_path = ['other', 'dummy', 'path']
        optd_mock.return_value = dummy_path
        for piece in other_pieces:
            res = ml.get_path_to_destination(start, knight_end, self.board, piece)
            self.assertEqual(res, dummy_path)

    @patch.object(ml, 'get_path_to_destination')
    @patch.object(ml, 'validate_move')
    def test_get_move_path(self, validate_move_mock, move_mock):
        start = Square(0, 0)
        end = Square(1, 1)
        pawn = Piece(PieceType.PAWN, ChessColor.WHITE, 0, 0)

        # raise if validation fails
        validate_move_mock.side_effect = ce.InvalidMoveException('dummy exception')
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_move_path(pawn, start, end, self.board, self.player)

        validate_move_mock.side_effect = None

        # raise if get_path_to_destination throws
        move_mock.side_effect = ce.InvalidMoveException('mock exception')
        with self.assertRaises(ce.InvalidMoveException):
            ml.get_move_path(pawn, start, end, self.board, self.player)

        move_mock.side_effect = None
        dummy_path = ['dummy', 'path']
        move_mock.return_value = dummy_path
        # should successfully complete otherwise
        res = ml.get_move_path(pawn, start, end, self.board, self.player)
        self.assertEqual(res, dummy_path)

    @patch.object(ml, 'validate_move')
    def test_get_checking_pieces(self, validate_mock):
        # not check situations
        black_king = Piece(PieceType.KING, ChessColor.BLACK, 7, 0)
        white_king = Piece(PieceType.KING, ChessColor.WHITE, 0, 0)
        # TODO: since I'm mocking validate_move, probably don't need to assign to board
        self.board.squares[7][0] = black_king
        self.board.squares[0][0] = white_king
        self.player.active_pieces = [white_king]
        self.opponent.active_pieces = [black_king]

        validate_mock.side_effect = [ce.InvalidMoveException('dummy exception')]
        self.assertEqual(ml.get_checking_pieces(self.board, self.player, self.opponent), [])
        # TODO: more testing. A lot more

if __name__ == '__main__':
    unittest.main()
