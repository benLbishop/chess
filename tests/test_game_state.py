"""module for testing the game state logic."""
import unittest
from unittest.mock import patch
from chessGame.move_logic import pathing, game_state as gs
from chessGame.piece import Piece
from chessGame.enums import PieceType, ChessColor
from chessGame.board import Board
from chessGame.player import Player
from chessGame import constants
from chessGame.custom_exceptions import InvalidMoveException

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
