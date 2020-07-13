"""module for testing the game state logic."""
import unittest
from chessGame.enums import ChessColor
from chessGame.board import Board
from chessGame.player import Player
from chessGame import constants

class GameStateTest(unittest.TestCase):
    """tests for the game state logic."""
    @classmethod
    def setUpClass(cls):
        cls.board = Board(constants.STD_BOARD_CONFIG)
        cls.white_player = Player({'color': ChessColor.WHITE, 'name': 'Travis'})
        cls.black_player = Player({'color': ChessColor.BLACK, 'name': 'Justin'})

    def tearDown(self):
        self.board.clear()

    def test_can_block_checking_piece(self):
        """Tests for the can_block_checking_piece method."""
        # TODO

    def test_player_is_checkmated(self):
        """Tests for the player_is_checkmated method."""
        # TODO


    def test_player_is_stalemated(self):
        """Tests for the player_is_stalemated method."""
        # TODO

    def test_get_checking_pieces(self):
        """Tests for the get_checking_pieces method."""
        # TODO
