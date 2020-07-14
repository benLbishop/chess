"""module for testing the game state logic."""
import unittest
from unittest.mock import patch
from chessGame.enums import ChessColor
from chessGame.board import Board, StandardBoard
from chessGame.player import Player
from chessGame.move_logic import game_state
from chessGame.pieces.piece import Piece
from chessGame.pieces.king import King
from chessGame.custom_exceptions import InvalidMoveException

class GameStateTest(unittest.TestCase):
    """tests for the game state logic."""
    @classmethod
    def setUpClass(cls):
        cls.board = StandardBoard()
        cls.white_player = Player({'color': ChessColor.WHITE, 'name': 'Travis'})
        cls.black_player = Player({'color': ChessColor.BLACK, 'name': 'Justin'})

    def tearDown(self):
        self.board.clear()

    @patch.object(Piece, 'can_reach_squares')
    def test_can_block_checking_piece(self, reach_mock):
        """Tests for the can_block_checking_piece method."""
        board = self.board
        checking_path_coords = [(0, 0), (1, 0), (2, 0)]
        checking_path = [board.squares[row][col] for row, col in checking_path_coords]
        p1 = Piece(ChessColor.BLACK)
        p2 = Piece(ChessColor.BLACK)
        p3 = Piece(ChessColor.BLACK)
        piece_mapping = [
            (p1, (1, 1)),
            (p2, (1, 2)),
            (p3, (1, 3))
        ]

        # should return false if no square on path can be reached
        reach_mock.return_value = False
        res = game_state.can_block_checking_piece(checking_path, board, piece_mapping)
        self.assertFalse(res)

        # should return true if any piece can reach any square on the path
        reach_mock.side_effect = [False, False, True]
        res = game_state.can_block_checking_piece(checking_path, board, piece_mapping)
        self.assertTrue(res)

    @patch.object(game_state, 'can_block_checking_piece')
    @patch.object(Piece, 'has_valid_move')
    @patch.object(Board, 'get_active_pieces')
    def test_player_is_checkmated(self, active_pieces_mock, valid_move_mock, block_mock):
        """Tests for the player_is_checkmated method."""
        check_path = ['check path']
        checking_pieces = [(Piece(ChessColor.BLACK), check_path)]
        white_king = King(ChessColor.WHITE)
        white_mapping = [
            (white_king, (1, 1)),
            (Piece(ChessColor.WHITE), (1, 2)),
            (Piece(ChessColor.WHITE), (1, 3))
        ]
        black_king = King(ChessColor.BLACK)
        black_mapping = [
            (black_king, (7, 1)),
            (Piece(ChessColor.BLACK), (7, 2)),
            (Piece(ChessColor.BLACK), (7, 3))
        ]
        active_pieces_mock.return_value = (white_mapping, black_mapping)

        # return false if no checking pieces
        res = game_state.player_is_checkmated(self.board, ChessColor.WHITE, [])
        self.assertFalse(res)

        # should return false if king can move
        valid_move_mock.return_value = True
        res = game_state.player_is_checkmated(self.board, ChessColor.WHITE, checking_pieces)
        self.assertFalse(res)
        valid_move_mock.return_value = False

        # should use the correct piece mapping
        # TODO

        # should handle case with > 2 checking pieces
        multi_check_pieces = ['more', 'than', 'one']
        res = game_state.player_is_checkmated(self.board, ChessColor.WHITE, multi_check_pieces)
        self.assertTrue(res)
        block_mock.assert_not_called()

        # if king cannot move and 1 checking piece, should call can_block
        block_mock.reset_mock()
        block_mock.return_value = False
        res = game_state.player_is_checkmated(self.board, ChessColor.WHITE, checking_pieces)
        self.assertTrue(res)
        block_mock.assert_called_once()

        block_mock.return_value = True
        res = game_state.player_is_checkmated(self.board, ChessColor.WHITE, checking_pieces)
        self.assertFalse(res)

    @patch.object(Piece, 'has_valid_move')
    @patch.object(Board, 'get_active_pieces')
    def test_player_is_stalemated(self, active_pieces_mock, valid_move_mock):
        """Tests for the player_is_stalemated method."""
        white_king = King(ChessColor.WHITE)
        white_mapping = [
            (white_king, (1, 1)),
            (Piece(ChessColor.WHITE), (1, 2)),
            (Piece(ChessColor.WHITE), (1, 3))
        ]
        black_king = King(ChessColor.BLACK)
        black_mapping = [
            (black_king, (7, 1)),
            (Piece(ChessColor.BLACK), (7, 2)),
            (Piece(ChessColor.BLACK), (7, 3))
        ]
        active_pieces_mock.return_value = (white_mapping, black_mapping)
        # should use the correct piece mapping
        # TODO

        # should return false if any piece has a valid move
        valid_move_mock.side_effect = [False, True]
        res = game_state.player_is_stalemated(self.board, ChessColor.WHITE)
        self.assertFalse(res)
        valid_move_mock.side_effect = None

        # should return false otherwise
        valid_move_mock.return_value = False
        res = game_state.player_is_stalemated(self.board, ChessColor.WHITE)
        self.assertTrue(res)

    @patch.object(Piece, 'get_path_to_square')
    @patch.object(Board, 'get_active_pieces')
    def test_get_checking_pieces(self, active_pieces_mock, path_mock):
        """Tests for the get_checking_pieces method."""
        white_king = King(ChessColor.WHITE)
        white_mapping = [
            (white_king, (1, 1)),
            (Piece(ChessColor.WHITE), (1, 2)),
            (Piece(ChessColor.WHITE), (1, 3))
        ]
        black_king = King(ChessColor.BLACK)
        black_mapping = [
            (black_king, (7, 1)),
            (Piece(ChessColor.BLACK), (7, 2)),
            (Piece(ChessColor.BLACK), (7, 3))
        ]
        active_pieces_mock.return_value = (white_mapping, black_mapping)
        # should use the correct piece mapping
        # TODO

        # should return any pieces checking king
        path_mock.side_effect = ['path1', InvalidMoveException('path exception'), 'path2']
        expected_res = [(black_mapping[0][0], 'path1'), (black_mapping[2][0], 'path2')]
        res = game_state.get_checking_pieces(self.board, ChessColor.WHITE)
        self.assertEqual(res, expected_res)

        # TODO: more tests
