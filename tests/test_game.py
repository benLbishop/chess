"""module for testing the Game class."""
import unittest
from unittest.mock import patch
from chessGame.game import Game
from chessGame.board import Board, StandardBoard
from chessGame.player import Player
import chessGame.conversion as conv
from chessGame import constants
from chessGame.move_logic import pathing, game_state
from chessGame.piece import Piece
from chessGame.enums import PieceType, ChessColor
from chessGame.custom_exceptions import InvalidMoveException

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

    @patch.object(game_state, 'get_checking_pieces')
    @patch.object(pathing, 'get_move_path')
    def test_move_piece(self, move_mock, check_mock):
        """tests function that actually moves pieces in the game."""
        white_config = {'name': 'Bob'}
        black_config = {'name': 'Allie'}
        test_game = Game(None, white_config, black_config, [])
        start = test_game.board.squares[1][1]
        end = test_game.board.squares[2][1]
        king = Piece(PieceType.KING, ChessColor.WHITE, 1, 1)
        rook = Piece(PieceType.ROOK, ChessColor.BLACK, 2, 1)

        move_mock.return_value = []
        # should raise if no move path found
        move_mock.side_effect = InvalidMoveException('dummy exception')
        with self.assertRaises(InvalidMoveException):
            test_game._move_piece(start, end)

        move_mock.side_effect = None
        # should use the proper players as cur_player/opponent
        test_game._move_piece(start, end)
        move_mock.assert_called_with(start, end, test_game.board, test_game.white_player)
        # test black player
        test_game.is_white_turn = False
        test_game._move_piece(start, end)
        move_mock.assert_called_with(start, end, test_game.board, test_game.black_player)

        test_game.board.clear()
        start.piece = king
        test_game.is_white_turn = True
        # should raise if move puts player in check
        check_mock.return_value = ['something']
        with self.assertRaises(InvalidMoveException):
            test_game._move_piece(start, end)
        # make sure piece location wasn't updated permanently
        self.assertIsNone(end.piece)
        self.assertEqual(start.piece, king)

        # test again with a piece on destination square
        end.piece = rook
        with self.assertRaises(InvalidMoveException):
            test_game._move_piece(start, end)
        self.assertEqual(end.piece, rook)
        self.assertEqual(start.piece, king)

            # should properly update capture list, if something like that occurs
        check_mock.return_value = []
        
        test_game.board.clear()
        start.piece = king
        test_game.black_player.active_pieces = [rook]
        test_game._move_piece(start, end)
        self.assertEqual(test_game.black_player.active_pieces, [rook])
        self.assertEqual(test_game.white_player.captured_pieces, [])

        test_game.board.clear()
        start.piece = king
        end.piece = rook
        test_game._move_piece(start, end)
        self.assertEqual(test_game.black_player.active_pieces, [])
        self.assertEqual(test_game.white_player.captured_pieces, [rook])

        # TODO: test this with same piece type but different locations, i.e. two pawns.
        # want to make sure the correct pawn is removed from player list
        
    @patch.object(game_state, 'player_is_stalemated')
    @patch.object(game_state, 'player_is_checkmated')
    @patch.object(game_state, 'get_checking_pieces')
    @patch.object(Game, '_move_piece')
    def test_make_move(self, move_mock, check_mock, checkmate_mock, stalemate_mock):
        """tests function that processes an attempted move of a piece."""
        # TODO: should be in Board class?
        white_config = {'name': 'Bob'}
        black_config = {'name': 'Allie'}
        test_game = Game(None, white_config, black_config, [])
        start = test_game.board.squares[1][1]
        end = test_game.board.squares[2][1]
        # should raise if piece can't be moved
        move_mock.side_effect = InvalidMoveException('dummy exception')
        with self.assertRaises(InvalidMoveException):
            test_game.make_move(start, end)

        move_mock.side_effect = None
        # update check/checkmate/stalemate status. end the game if appropriate
        # update current player if game not over
        check_mock.return_value = ['something']
        checkmate_mock.return_value = False
        test_game.make_move(start, end)
        self.assertEqual(test_game.is_complete, False)
        self.assertEqual(test_game.is_white_turn, False)


        checkmate_mock.return_value = True
        test_game.make_move(start, end)
        self.assertEqual(test_game.is_complete, True)

        test_game.is_white_turn = True # TODO: put this in teardown or something

        test_game.is_complete = False
        check_mock.return_value = []
        stalemate_mock.return_value = False
        test_game.make_move(start, end)
        self.assertEqual(test_game.is_complete, False)
        self.assertEqual(test_game.is_white_turn, False)

        stalemate_mock.return_value = True
        test_game.make_move(start, end)
        self.assertEqual(test_game.is_complete, True)

    