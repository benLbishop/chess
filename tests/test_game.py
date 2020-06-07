"""module for testing the Game class."""
import unittest
from unittest.mock import patch
from chessGame.game import Game
from chessGame.board import StandardBoard
from chessGame.player import Player

class GameTest(unittest.TestCase):
    """tests for the Game class."""

    @patch.object(Game, '_populate_board')
    def test_init(self, _populate_board_mock):
        """tests for the constructor."""
        white_config = {'name': 'Bob'}
        black_config = {'name': 'Allie'}

        # test behavior when board_config is none
        test_game = Game(None, white_config, black_config)
        self.assertIsInstance(test_game.board, StandardBoard)
        self.assertIsInstance(test_game.white_player, Player)
        self.assertIsInstance(test_game.black_player, Player)

        self.assertEqual(test_game.is_complete, False)
        self.assertEqual(test_game.is_white_turn, True)

        # make sure populate board is called
        _populate_board_mock.assert_called_once()

    def test_attempt_move(self):
        """tests function that processes an attempted move of a piece."""
        # TODO: should be in Board class?
        # should raise if piece can't be moved
        # update squares of move
        # update which player's turn it is
        # update check/checkmate/stalemate status
        # end the game if appropriate