"""module for testing the game state logic."""
import unittest
from unittest.mock import patch
from chessGame.move_logic import pathing, game_state as gs
from chessGame.piece import Piece
from chessGame.enums import PieceType, ChessColor, MoveType
from chessGame.board import Board
from chessGame.player import Player
from chessGame import constants, conversion
from chessGame.custom_exceptions import InvalidMoveException
from . import board_lists

psns = conversion.parse_std_notation_string
pfs = Piece.from_string

class GameStateTest(unittest.TestCase):
    """tests for the game state logic."""
    @classmethod
    def setUpClass(cls):
        cls.board = Board(constants.STD_BOARD_CONFIG)
        cls.white_player = Player({'color': ChessColor.WHITE, 'name': 'Travis'})
        cls.black_player = Player({'color': ChessColor.BLACK, 'name': 'Justin'})

    def tearDown(self):
        self.board.clear()

    # def test_player_is_checkmated(self):
    #     # if len(checking_pieces) > 1, only need to check if king can move and no longer be in check
    #     # otherwise...
    #     #   1. check if king can move and no longer be in check (so just do this first regardless)
    #     #   2. for checking piece's path to king, see if any of player's pieces can intercede path
    #     #       or capture checking piece without opening up another check situation
    #     # test checkmate results
    #     for test_board in board_lists.checkmate_list:
    #         piece_strings, mated_color = test_board
    #         piece_list = [Piece.from_string(s) for s in piece_strings]
    #         white_pieces, black_pieces = separate_pieces(piece_list)
    #         self.board.populate(white_pieces + black_pieces)
    #         self.white_player.active_pieces = white_pieces
    #         self.black_player.active_pieces = black_pieces
    #         # TODO: how do I get the checking pieces?
    #         if mated_color is ChessColor.WHITE:
    #             checking_pieces = gs.get_checking_pieces(self.board, self.white_player, self.black_player)
    #             res = gs.player_is_checkmated(self.board, self.white_player, self.black_player, checking_pieces)
    #         else:
    #             checking_pieces = gs.get_checking_pieces(self.board, self.black_player, self.white_player)
    #             res = gs.player_is_checkmated(self.board, self.black_player, self.white_player, checking_pieces)
    #         self.assertEqual(res, True)
    #         self.tearDown()
    #     # TODO: test non-checkmates

            

    def test_player_is_stalemated(self):
        pass
        # for each piece in player.active_pieces...
        #   try to move piece one increment. If possible and player isn't in check from the resulting move, return False
        # return true if can't find a valid move for any piece

    @patch.object(pathing, 'get_move_path')
    def test_get_checking_pieces(self, move_mock):
        # not check situations
        black_king_params, black_coords = psns('b Ka8')
        white_king_params, white_coords = psns('w Ka1')
        black_king = Piece(*black_king_params)
        white_king = Piece(*white_king_params)
        # TODO: since I'm mocking get_move_path, probably don't need to assign to board
        self.board.squares[black_coords[0]][black_coords[1]].piece = black_king
        self.board.squares[white_coords[0]][white_coords[1]].piece = white_king

        move_mock.side_effect = [InvalidMoveException('dummy exception')]
        self.assertEqual(gs.get_checking_pieces(self.board, self.white_player, self.black_player), [])
        # TODO: more testing. A lot more

    # TODO: move
    def test_get_move_options(self):
        row_idx, col_idx = 3, 3
        white_pawn = pfs('w')
        black_pawn = pfs('b')
        knight = pfs('w N')
        bishop = pfs('w B')
        rook = pfs('w R')
        queen = pfs('w Q')
        king = pfs('w K')
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
            pass # TODO

