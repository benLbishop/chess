"""module for testing the move logic."""
import unittest
from unittest.mock import patch
from chessGame.square import Square
from chessGame.player import Player
from chessGame.piece import Piece
from chessGame.enums import ChessColor, PieceType, MoveType
from chessGame.board import Board
from chessGame import constants, input
from chessGame.move_logic import pathing, validation
import chessGame.custom_exceptions as ce

pfs = Piece.from_string
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

        pawn = pfs('w')
        start.piece = pawn

        white_piece = pfs('w B')
        black_piece = pfs('b B')

        # should raise if straight move attempted and ANY piece in way
        straight_end1.piece = white_piece
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_pawn_path_to_destination(start, straight_end1, self.board, pawn)

        straight_end1.piece = black_piece
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_pawn_path_to_destination(start, straight_end1, self.board, pawn)

        # should raise if moving 2 squares and pawn has moved
        straight_end1.clear()
        straight_end2.clear()
        pawn.has_moved = True
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_pawn_path_to_destination(start, straight_end2, self.board, pawn)

        pawn.has_moved = False

        # should raise if moving 2 is squares is valid, but blocking piece
        straight_end1.piece = black_piece
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_pawn_path_to_destination(start, straight_end2, self.board, pawn)

        straight_end1.clear()
        straight_end2.piece = black_piece
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_pawn_path_to_destination(start, straight_end2, self.board, pawn)

        straight_end2.clear()

        # should get the proper path for 2 otherwise
        res = pathing.get_pawn_path_to_destination(start, straight_end2, self.board, pawn)
        self.assertEqual(res, [straight_end1, straight_end2])

        # should raise if diagonal move attempted and no piece on end
        # and not performing En-Passant
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_path_to_destination(start, diag_end1, self.board, pawn)
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_path_to_destination(start, diag_end2, self.board, pawn)

    def test_get_knight_path_to_destination(self):
        squares = self.board.squares
        end = squares[2][1]
        knight = pfs('w N')

        # should raise if player's piece is on end_square
        end_pawn = pfs('w')
        end.piece = end_pawn
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_knight_path_to_destination(end, knight)

        # should return path if opponent's piece is on end_square
        end_pawn.color = ChessColor.BLACK
        res = pathing.get_knight_path_to_destination(end, knight)
        self.assertEqual(res, [end])

        # should return path if no piece on end_square
        self.board.clear()
        res = pathing.get_knight_path_to_destination(end, knight)
        self.assertEqual(res, [end])

    @patch.object(pathing, 'get_next_square_indexes')
    @patch.object(pathing, 'get_necessary_move_type')
    def test_get_others_path_to_destination(self, gnmt_mock, get_next_square_mock):
        squares = self.board.squares
        start = squares[0][0]
        gnmt_mock.return_value = MoveType.RIGHT

        self.board.clear()
        rook = pfs('w R')
        start.piece = rook
        white_pawn = pfs('w')
        black_pawn = pfs('b')
        squares[0][2].piece = white_pawn
        end2 = squares[0][3]
        # should raise if we come across a piece on square that's not destination
        get_next_square_mock.side_effect = [(0, 1), (0, 2)]
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_others_path_to_destination(start, end2, self.board, rook)

        # should raise if piece on destination is same color
        end3 = squares[0][2]
        get_next_square_mock.side_effect = [(0, 1), (0, 2)]
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_others_path_to_destination(start, end3, self.board, rook)

        # should return safely if piece on destination is opponent's
        squares[0][2].piece = black_pawn
        get_next_square_mock.side_effect = [(0, 1), (0, 2)]
        res = pathing.get_others_path_to_destination(start, end3, self.board, rook)
        self.assertEqual(res, [squares[0][1], squares[0][2]])

        # should return safely if no piece in path
        self.board.clear()
        get_next_square_mock.side_effect = [(0, 1), (0, 2), (0, 3)]
        res = pathing.get_others_path_to_destination(start, end2, self.board, rook)
        self.assertEqual(res, [squares[0][1], squares[0][2], squares[0][3]])

        # TODO: many more tests
    
    @patch.object(pathing, 'get_others_path_to_destination')
    @patch.object(pathing, 'get_knight_path_to_destination')
    @patch.object(pathing, 'get_pawn_path_to_destination')
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
        pawn = pfs('w')
        pawn_end = squares[1][0]
        pptd_mock.side_effect = ce.InvalidMoveException('dummy exception')
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_path_to_destination(start, pawn_end, self.board, pawn)

        # should return the pawn's function response otherwise
        pptd_mock.side_effect = None
        res = pathing.get_path_to_destination(start, pawn_end, self.board, pawn)
        self.assertEqual(res, pawn_return_val)

        # should handle knights appropriately
        # should raise if knight function raises
        knight = pfs('w N')
        knight_end = squares[2][1]
        kptd_mock.side_effect = ce.InvalidMoveException('dummy exception')
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_path_to_destination(start, knight_end, self.board, knight)

        # should return the knights's function response otherwise
        kptd_mock.side_effect = None
        res = pathing.get_path_to_destination(start, knight_end, self.board, knight)
        self.assertEqual(res, knight_return_val)

        # should handle other piece types properly
        other_pieces = [
            pfs('w R'),
            pfs('w B'),
            pfs('w Q'),
            pfs('w K')
        ]
        optd_mock.side_effect = ce.InvalidMoveException('dummy exception')
        for piece in other_pieces:
            with self.assertRaises(ce.InvalidMoveException):
                pathing.get_path_to_destination(start, knight_end, self.board, piece)

        optd_mock.side_effect = None
        dummy_path = ['other', 'dummy', 'path']
        optd_mock.return_value = dummy_path
        for piece in other_pieces:
            res = pathing.get_path_to_destination(start, knight_end, self.board, piece)
            self.assertEqual(res, dummy_path)

    @patch.object(pathing, 'get_path_to_destination')
    @patch.object(validation, 'validate_move')
    def test_get_move_path(self, validate_move_mock, move_mock):
        start = Square(0, 0)
        end = Square(1, 1)

        # raise if validate_move fails
        validate_move_mock.side_effect = ce.InvalidMoveException('dummy exception')
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_move_path(start, end, self.board, self.player)

        validate_move_mock.side_effect = None

        # raise if get_path_to_destination throws
        move_mock.side_effect = ce.InvalidMoveException('mock exception')
        with self.assertRaises(ce.InvalidMoveException):
            pathing.get_move_path(start, end, self.board, self.player)

        move_mock.side_effect = None
        dummy_path = ['dummy', 'path']
        move_mock.return_value = dummy_path
        # should successfully complete otherwise
        res = pathing.get_move_path(start, end, self.board, self.player)
        self.assertEqual(res, dummy_path)

if __name__ == '__main__':
    unittest.main()
