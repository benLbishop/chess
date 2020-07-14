"""module for testing for the Player class."""
import unittest
from unittest.mock import patch

from chessGame.player import Player
from chessGame.enums import ChessColor
from chessGame.pieces.piece import Piece
from chessGame.pieces.king import King
from chessGame.board import Board, StandardBoard
from chessGame.move_logic import game_state

class TestPlayer(unittest.TestCase):
    """tests for the Player class."""
    @classmethod
    def setUpClass(cls):
        cls.board = StandardBoard()

    def tearDown(self):
        self.board.clear()

    def test_init(self):
        """tests the constructorr."""
        white_config = {'color': ChessColor.WHITE, 'name': 'Griffin'}
        white_player = Player(white_config)
        black_config = {'color': ChessColor.BLACK, 'name': 'Justin'}
        black_player = Player(black_config)

        self.assertEqual(white_player.color, ChessColor.WHITE)
        self.assertEqual(white_player.name, white_config['name'])
        self.assertEqual(white_player.captured_pieces, [])
        self.assertEqual(black_player.color, ChessColor.BLACK)
        self.assertEqual(black_player.name, black_config['name'])
        self.assertEqual(black_player.captured_pieces, [])

        # TODO: test which names are allowed? Is empty string ok?

    @patch.object(game_state, 'can_block_checking_piece')
    @patch.object(Piece, 'has_valid_move')
    @patch.object(Board, 'get_active_pieces')
    def test_is_checkmated(self, active_pieces_mock, valid_move_mock, block_mock):
        """Tests for the player_is_checkmated method."""
        white_config = {'color': ChessColor.WHITE, 'name': 'Griffin'}
        white_player = Player(white_config)

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
        res = white_player.is_checkmated(self.board, [])
        self.assertFalse(res)

        # should return false if king can move
        valid_move_mock.return_value = True
        res = white_player.is_checkmated(self.board, checking_pieces)
        self.assertFalse(res)
        valid_move_mock.return_value = False

        # should use the correct piece mapping
        # TODO

        # should handle case with > 2 checking pieces
        multi_check_pieces = ['more', 'than', 'one']
        res = white_player.is_checkmated(self.board, multi_check_pieces)
        self.assertTrue(res)
        block_mock.assert_not_called()

        # if king cannot move and 1 checking piece, should call can_block
        block_mock.reset_mock()
        block_mock.return_value = False
        res = white_player.is_checkmated(self.board, checking_pieces)
        self.assertTrue(res)
        block_mock.assert_called_once()

        block_mock.return_value = True
        res = white_player.is_checkmated(self.board, checking_pieces)
        self.assertFalse(res)

    @patch.object(Piece, 'has_valid_move')
    @patch.object(Board, 'get_active_pieces')
    def test_is_stalemated(self, active_pieces_mock, valid_move_mock):
        """Tests for the player_is_stalemated method."""
        white_config = {'color': ChessColor.WHITE, 'name': 'Griffin'}
        white_player = Player(white_config)

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
        res = white_player.is_stalemated(self.board)
        self.assertFalse(res)
        valid_move_mock.side_effect = None

        # should return false otherwise
        valid_move_mock.return_value = False
        res = white_player.is_stalemated(self.board)
        self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()
