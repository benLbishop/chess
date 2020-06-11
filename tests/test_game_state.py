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

from . import board_lists

class GameStateTest(unittest.TestCase):
    """tests for the game state logic."""
    @classmethod
    def setUpClass(cls):
        cls.board = Board(constants.STD_BOARD_CONFIG)
        cls.white_player = Player({'color': ChessColor.WHITE, 'name': 'Travis'})
        cls.black_player = Player({'color': ChessColor.BLACK, 'name': 'Justin'})

    def tearDown(self):
        self.board.clear()
        self.white_player.active_pieces = []
        self.black_player.active_pieces = []

    def test_player_is_checkmated(self):
        # if len(checking_pieces) > 1, only need to check if king can move and no longer be in check
        # otherwise...
        #   1. check if king can move and no longer be in check (so just do this first regardless)
        #   2. for checking piece's path to king, see if any of player's pieces can intercede path
        #       or capture checking piece without opening up another check situation
        # test checkmate results
        for test_board in board_lists.checkmate_list:
            piece_strings, mated_color = test_board
            white_pieces, black_pieces = convert_strings_to_pieces(piece_strings)
            self.board.populate(white_pieces + black_pieces)
            self.white_player.active_pieces = white_pieces
            self.black_player.active_pieces = black_pieces
            # TODO: how do I get the checking pieces?
            if mated_color is ChessColor.WHITE:
                checking_pieces = gs.get_checking_pieces(self.board, self.white_player, self.black_player)
                res = gs.player_is_checkmated(self.board, self.white_player, self.black_player, checking_pieces)
            else:
                checking_pieces = gs.get_checking_pieces(self.board, self.black_player, self.white_player)
                res = gs.player_is_checkmated(self.board, self.black_player, self.white_player, checking_pieces)
            self.assertEqual(res, True)
            self.tearDown()
        # TODO: test non-checkmates

            

    def test_player_is_stalemated(self):
        pass
        # for each piece in player.active_pieces...
        #   try to move piece one increment. If possible and player isn't in check from the resulting move, return False
        # return true if can't find a valid move for any piece

    @patch.object(pathing, 'get_move_path')
    def test_get_checking_pieces(self, move_mock):
        # not check situations
        black_king = Piece(PieceType.KING, ChessColor.BLACK, 7, 0)
        white_king = Piece(PieceType.KING, ChessColor.WHITE, 0, 0)
        # TODO: since I'm mocking get_move_path, probably don't need to assign to board
        self.board.squares[7][0] = black_king
        self.board.squares[0][0] = white_king
        self.white_player.active_pieces = [white_king]
        self.black_player.active_pieces = [black_king]

        move_mock.side_effect = [InvalidMoveException('dummy exception')]
        self.assertEqual(gs.get_checking_pieces(self.board, self.white_player, self.black_player), [])
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

    def test_get_valid_adjacent_squares(self):
        valid_move_tests = [
            (['w a2', 'b a3'], [])
        ]
        for piece_strings, expected_res in valid_move_tests:
            white_pieces, black_pieces = convert_strings_to_pieces(piece_strings)
            self.white_player.active_pieces = white_pieces
            self.black_player.active_pieces = black_pieces
            self.board.populate(white_pieces + black_pieces)

            res = gs.get_valid_adjacent_squares(white_pieces[0], self.board, self.black_player)
            self.assertEqual(res, expected_res)
            self.tearDown()
        # check every possible square the piece could move to in 1 unit.
        # if blocked, return false
        # if move results in player being in check, return false

