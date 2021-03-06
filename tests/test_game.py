"""module for testing the Game class."""
import unittest
from unittest.mock import patch

from chess_game.game import Game
from chess_game.board import Board, StandardBoard
from chess_game.player import Player
from chess_game import conversion as conv
from chess_game.custom_exceptions import (
    InvalidMoveException,
    PiecePlacementException,
    PawnPromotionException
)
from chess_game.enums import ChessColor, MoveSideEffect
from chess_game.move import Move

class GameTest(unittest.TestCase):
    """tests for the Game class."""
    @classmethod
    def setUpClass(cls):
        white_config = {'name': 'Bob', 'color': ChessColor.WHITE}
        black_config = {'name': 'Allie', 'color': ChessColor.BLACK}
        cls.white_player = Player(white_config)
        cls.black_player = Player(black_config)

    @patch.object(Game, '_validate_initial_game_state')
    @patch.object(Game, '_set_up_pieces')
    def test_init(self, set_up_pieces_mock, validate_mock):
        """tests for the constructor."""
        

        # test behavior when board_config is none
        test_game = Game(self.white_player, self.black_player)
        self.assertIsInstance(test_game.board, StandardBoard)
        self.assertEqual(test_game.white_player, self.white_player)
        self.assertEqual(test_game.black_player, self.black_player)

        self.assertEqual(test_game.is_complete, False)
        self.assertEqual(test_game.is_white_turn, True)

        # make sure populate board is called
        set_up_pieces_mock.assert_called_once()
        validate_mock.assert_called_once()

        # TODO: make sure optional init params work

    @patch.object(Board, 'get_active_pieces')
    def test_validate_initial_game_state(self, active_pieces_mock):
        """Tests for the private _validate_initial_game_state method."""
        # TODO: find a better way to test this. it's goofing up things like test_make_move
        # since it calls other functions that might be mocked
        active_pieces_mock.return_value = ([], [])

        # should raise if board was not populated
        with self.assertRaises(PiecePlacementException):
            test_game = Game(self.white_player, self.black_player)
        
        # TODO
        # should raise if either player has 0 or 2+ kings

        # should raise if either player is in checkmate or stalemate


    @patch.object(Board, 'populate')
    @patch.object(conv, 'parse_std_notation_string')
    def test_set_up_pieces(self, parse_mock, populate_mock):
        """Tests the private _set_up_pieces method."""
        # TODO: test conversion failure, populate failure, if piece_strings is empty, use std piece list

    @patch.object(Game, '_validate_initial_game_state')
    @patch.object(Game, '_check_for_end_of_game')
    @patch.object(Board, 'move_piece')
    def test_make_move(self, move_mock, end_mock, validate_mock):
        """tests function that processes an attempted move of a piece."""
        test_game = Game(self.white_player, self.black_player)
        start_coords, end_coords = ((1, 1), (2, 1))
        start_square = test_game.board.squares[1][1]
        end_square = test_game.board.squares[2][1]
        move_mock.return_value = Move(start_square, end_square)

        # TODO: test adding captured piece to player

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

        # should raise if a pawn promotion is occuring
        move_mock.return_value = Move(start_square, end_square, None, None, MoveSideEffect.PAWN_PROMOTION)
        with self.assertRaises(PawnPromotionException):
            test_game.make_move(start_coords, end_coords)
        move_mock.return_value = Move(start_square, end_square)

        # should call end of game method and switch turns
        end_mock.reset_mock()
        test_game.make_move(start_coords, end_coords)
        end_mock.assert_called_once()
        test_game.is_white_turn = False

    @patch.object(Player, 'is_stalemated')
    @patch.object(Player, 'is_checkmated')
    @patch.object(Board, 'get_checking_pieces')
    def test_check_for_end_of_game(self, check_mock, checkmate_mock, stalemate_mock):
        """Tests for the private _check_for_end_of_game method."""
        # TODO: move this to setUpClass (same with most other tests.)
        checkmate_mock.return_value = False
        stalemate_mock.return_value = False
        test_game = Game(self.white_player, self.black_player)

        check_mock.return_value = ['something']

        # make sure game doesn't end if not in checkmate
        test_game._check_for_end_of_game()
        self.assertEqual(test_game.is_complete, False)

        # make sure game ends if in checkmate
        checkmate_mock.return_value = True
        test_game._check_for_end_of_game()
        self.assertEqual(test_game.is_complete, True)

        test_game.is_complete = False
        check_mock.return_value = []

        # make sure game doesn't end if not in stalemate
        test_game._check_for_end_of_game()
        self.assertEqual(test_game.is_complete, False)

        # make sure game ends if in stalemate
        stalemate_mock.return_value = True
        test_game._check_for_end_of_game()
        self.assertEqual(test_game.is_complete, True)
 