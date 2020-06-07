"""module for testing the Game class."""
import unittest
from unittest.mock import patch
from chessGame.game import Game
from chessGame.board import Board, StandardBoard
from chessGame.player import Player
import chessGame.conversion as conv
from chessGame import constants

class GameTest(unittest.TestCase):
    """tests for the Game class."""

    @patch.object(Game, '_set_up_pieces')
    def test_init(self, _set_up_pieces_mock):
        """tests for the constructor."""
        white_config = {'name': 'Bob'}
        black_config = {'name': 'Allie'}

        # test behavior when board_config is none
        test_game = Game(None, white_config, black_config, [])
        self.assertIsInstance(test_game.board, StandardBoard)
        self.assertIsInstance(test_game.white_player, Player)
        self.assertIsInstance(test_game.black_player, Player)

        self.assertEqual(test_game.is_complete, False)
        self.assertEqual(test_game.is_white_turn, True)

        # make sure populate board is called
        _set_up_pieces_mock.assert_called_once()

    @patch.object(conv, 'convert_strings_to_pieces')
    def test_set_up_pieces(self, convert_strings_mock):
        # if piece_strings is empty, use std piece list
        white_config = {'name': 'Bob'}
        black_config = {'name': 'Allie'}
        test_game = Game(None, white_config, black_config, [])

        convert_strings_mock.assert_called_with(constants.STD_PIECE_STRINGS)
        # raise if piece_strings cannot be converted
        # TODO test conversion failure, populate failure, player piece assignment, sorting player pieces

    def test_attempt_move(self):
        """tests function that processes an attempted move of a piece."""
        # TODO: should be in Board class?
        # should raise if piece can't be moved
        # update squares of move
        # update which player's turn it is
        # update check/checkmate/stalemate status
        # end the game if appropriate