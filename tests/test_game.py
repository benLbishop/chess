"""module for testing the Game class."""
import unittest
from unittest.mock import patch
from chessGame.game import Game
from chessGame.board import Board, StandardBoard
from chessGame.player import Player
from chessGame import conversion as conv
from chessGame.move_logic import game_state
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.enums import ChessColor
from chessGame.move import Move

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

    @patch.object(Board, 'populate')
    @patch.object(conv, 'parse_std_notation_string')
    def test_set_up_pieces(self, parse_mock, populate_mock):
        # if piece_strings is empty, use std piece list
        white_config = {'name': 'Bob'}
        black_config = {'name': 'Allie'}
        parse_mock.return_value = ('dummy', 'vals')
        test_game = Game(None, white_config, black_config)

        # TODO test conversion failure, populate failure, player piece assignment, sorting player pieces
    
    @patch.object(Game, 'check_for_end_of_game')
    @patch.object(game_state, 'get_checking_pieces')
    @patch.object(Board, 'undo_move')
    @patch.object(Board, 'move_piece')
    def test_make_move(self, move_mock, undo_move_mock, check_mock, end_mock):
        """tests function that processes an attempted move of a piece."""
        # TODO: should be in Board class?
        white_config = {'name': 'Bob'}
        black_config = {'name': 'Allie'}
        test_game = Game(None, white_config, black_config, [])
        start_coords, end_coords = ((1, 1), (2, 1))

        move_mock.return_value = Move((0, 0), (1, 0)) # TODO: test adding captured piece to player

        # should use the proper players as cur_player/opponent
        test_game.make_move(start_coords, end_coords)
        move_mock.assert_called_with(start_coords, end_coords, ChessColor.WHITE)

        test_game.is_white_turn = False
        test_game.make_move(start_coords, end_coords)
        move_mock.assert_called_with(start_coords, end_coords, ChessColor.BLACK)

        test_game.is_white_turn = True
        # should raise if piece can't be moved
        move_mock.side_effect = InvalidMoveException('dummy exception')
        with self.assertRaises(InvalidMoveException):
            test_game.make_move(start_coords, end_coords)

        move_mock.side_effect = None

        # should raise if player puts themselves in check
        check_mock.return_value = ['something']
        with self.assertRaises(InvalidMoveException):
            test_game.make_move(start_coords, end_coords)
            undo_move_mock.assert_called_once()
            self.assertEqual(test_game.is_white_turn, False)

        check_mock.return_value = []

        # should call end of game method
        # TODO

    @patch.object(game_state, 'player_is_stalemated')
    @patch.object(game_state, 'player_is_checkmated')
    @patch.object(game_state, 'get_checking_pieces')
    def test_check_for_end_of_game(self, check_mock, checkmate_mock, stalemate_mock):
        white_config = {'name': 'Bob'}
        black_config = {'name': 'Allie'}
        test_game = Game(None, white_config, black_config, [])

        check_mock.return_value = ['something']
        checkmate_mock.return_value = False
        stalemate_mock.return_value = False

        # make sure game doesn't end if not in checkmate
        test_game.check_for_end_of_game()
        self.assertEqual(test_game.is_complete, False)

        # make sure game ends if in checkmate
        checkmate_mock.return_value = True
        test_game.check_for_end_of_game()
        self.assertEqual(test_game.is_complete, True)

        test_game.is_complete = False
        check_mock.return_value = []

        # make sure game doesn't end if not in stalemate
        test_game.check_for_end_of_game()
        self.assertEqual(test_game.is_complete, False)

        # make sure game ends if in stalemate
        stalemate_mock.return_value = True
        test_game.check_for_end_of_game()
        self.assertEqual(test_game.is_complete, True)
 