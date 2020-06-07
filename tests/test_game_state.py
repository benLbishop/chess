"""module for testing the game state logic."""
import unittest
from unittest.mock import patch
from chessGame.move_logic import pathing, game_state as gs
from chessGame.piece import Piece
from chessGame.enums import PieceType, ChessColor, MoveType
from chessGame.board import Board
from chessGame.player import Player
from chessGame import constants
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.conversion import convert_strings_to_pieces

class GameStateTest(unittest.TestCase):
    """tests for the game state logic."""
    @classmethod
    def setUpClass(cls):
        cls.board = Board(constants.STD_BOARD_CONFIG)
        cls.player = Player({'color': ChessColor.WHITE, 'name': 'Travis'})
        cls.opponent = Player({'color': ChessColor.BLACK, 'name': 'Justin'})

    def tearDown(self):
        self.board.clear()
        self.player.active_pieces = []
        self.opponent.active_pieces = []

    @patch.object(pathing, 'get_move_path')
    def test_get_checking_pieces(self, move_mock):
        # not check situations
        black_king = Piece(PieceType.KING, ChessColor.BLACK, 7, 0)
        white_king = Piece(PieceType.KING, ChessColor.WHITE, 0, 0)
        # TODO: since I'm mocking get_move_path, probably don't need to assign to board
        self.board.squares[7][0] = black_king
        self.board.squares[0][0] = white_king
        self.player.active_pieces = [white_king]
        self.opponent.active_pieces = [black_king]

        move_mock.side_effect = [InvalidMoveException('dummy exception')]
        self.assertEqual(gs.get_checking_pieces(self.board, self.player, self.opponent), [])
        # TODO: more testing. A lot more

    # TODO: move
    def test_get_move_options(self):
        row_idx, col_idx = 3, 3
        white_pawn = Piece(PieceType.PAWN, ChessColor.WHITE, row_idx, col_idx)
        black_pawn = Piece(PieceType.PAWN, ChessColor.BLACK, row_idx, col_idx)
        knight = Piece(PieceType.KNIGHT, ChessColor.WHITE, row_idx, col_idx)
        bishop = Piece(PieceType.BISHOP, ChessColor.WHITE, row_idx, col_idx)
        rook = Piece(PieceType.ROOK, ChessColor.WHITE, row_idx, col_idx)
        queen = Piece(PieceType.QUEEN, ChessColor.WHITE, row_idx, col_idx)
        king = Piece(PieceType.KING, ChessColor.WHITE, row_idx, col_idx)
        test_cases = [
            (white_pawn, constants.PAWN_WHITE_MOVES),
            (black_pawn, constants.PAWN_BLACK_MOVES),
            (knight, []), # TODO uhhhh
            (bishop, constants.BISHOP_MOVES),
            (rook, constants.ROOK_MOVES),
            (queen, constants.QUEEN_MOVES),
            (king, constants.KING_MOVES)
        ]
        for piece, expected_res in test_cases:
            res = gs.get_move_options(piece)
            self.assertEqual(res, expected_res)

    def test_piece_has_valid_move(self):
        valid_move_tests = [
            (['w a2'], ['b a3'], False)
        ]
        for player_list, opp_list, expected_res in valid_move_tests:
            player_pieces = convert_strings_to_pieces(player_list)
            opp_pieces = convert_strings_to_pieces(opp_list)
            self.player.active_pieces = player_pieces
            self.opponent.active_pieces = opp_pieces
            self.board.populate(player_pieces + opp_pieces)

            res = gs.piece_has_valid_move(player_pieces[0], self.board, self.player)
            self.assertEqual(res, expected_res)
            self.tearDown()
        # check every possible square the piece could move to in 1 unit.
        # if blocked, return false
        # if move results in player being in check, return false

