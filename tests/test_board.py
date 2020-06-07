"""module containing tests for the Board class."""
import unittest
from unittest.mock import patch
from chessGame.board import Board, StandardBoard
from chessGame.piece import Piece
from chessGame import constants
from chessGame.enums import ChessColor, PieceType
from chessGame.custom_exceptions import PiecePlacementException

class BoardTest(unittest.TestCase):
    """tests for the Board class."""
    @patch.object(Board, '_create_squares')
    def test_init(self, _create_squares_mock):
        """Test the constructor."""
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        board_config = {'num_rows': num_rows, 'num_cols': num_cols}

        test_board = Board(board_config)
        # if dimensions become customizable, make sure they're > 0
        self.assertEqual(test_board.NUM_ROWS, constants.STD_BOARD_WIDTH)
        self.assertEqual(test_board.NUM_COLS, constants.STD_BOARD_HEIGHT)
        _create_squares_mock.assert_called_once()

    def test_create_squares(self):
        """Tests the creation of the squares attribute for the board."""
        #raise exception if board is too small
        with self.assertRaises(ValueError):
            test_board = Board({'num_rows': 1, 'num_cols': 10})

        with self.assertRaises(ValueError):
            test_board = Board({'num_rows': 10, 'num_cols': 1})

        config_list = [
            {'num_rows': constants.STD_BOARD_WIDTH, 'num_cols': constants.STD_BOARD_HEIGHT},
            {'num_rows': 3, 'num_cols': 5},
            {'num_rows': 10, 'num_cols': 7}
        ]
        for config in config_list:
            test_board = Board(config)
            self.assertEqual(len(test_board.squares), config['num_rows'])
            for row in test_board.squares:
                self.assertEqual(len(row), config['num_cols'])

    def test_clear(self):
        """Test the clearing function."""
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        test_board = Board({'num_rows': num_rows, 'num_cols': num_cols})

        # TODO: decouple testing for this from Square logic
        # test clearing when board is already empty
        test_board.clear()
        for row in test_board.squares:
            for square in row:
                self.assertFalse(square.is_occupied())

        # test clearing when board has pieces
        # TODO

    def test_populate(self):
        """test the initial placing of pieces on the board."""
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        test_board = Board({'num_rows': num_rows, 'num_cols': num_cols})
        # raise if piece's indexes are out of bounds
        test_pieces_with_oob = [
            Piece(PieceType.PAWN, ChessColor.WHITE, num_rows, 0),
            Piece(PieceType.PAWN, ChessColor.WHITE, 0, num_cols)
        ]
        for test_piece in test_pieces_with_oob:
            with self.assertRaises(PiecePlacementException):
                test_board.populate([test_piece])
        # raise if two pieces are populated to same square
        test_pieces_with_dup = [
            Piece(PieceType.KING, ChessColor.WHITE, 1, 1),
            Piece(PieceType.QUEEN, ChessColor.WHITE, 1, 1)
        ]
        with self.assertRaises(PiecePlacementException):
            test_board.populate(test_pieces_with_dup)

        # board not cleared if populate fails.
        test_board.clear()
        good_test_pieces = [
            Piece(PieceType.KING, ChessColor.WHITE, 1, 3),
            Piece(PieceType.QUEEN, ChessColor.WHITE, 3, 1),
            Piece(PieceType.PAWN, ChessColor.BLACK, 7, 7),
            Piece(PieceType.ROOK, ChessColor.BLACK, 4, 7),
        ]
        test_board.populate(good_test_pieces)
        for test_piece in good_test_pieces:
            row_idx = test_piece.row_idx
            col_idx = test_piece.col_idx
            self.assertEqual(test_board.squares[row_idx][col_idx].piece, test_piece)

class StandardBoardTest(unittest.TestCase):
    """tests for the derived Board class StandardBoard."""

    def test_init(self):
        """tests for the constructor."""
        # should create an 8x8 board
        std_board = StandardBoard()
        self.assertEqual(std_board.NUM_ROWS, 8)
        self.assertEqual(std_board.NUM_COLS, 8)

if __name__ == '__main__':
    unittest.main()
