"""module containing tests for the Board class."""
import unittest
from unittest.mock import patch
from chessGame.board import Board, StandardBoard
from chessGame.pieces.piece import Piece
from chessGame import constants, conversion as conv
from chessGame.enums import ChessColor
from chessGame.custom_exceptions import PiecePlacementException, InvalidMoveException
from chessGame.move import Move

psns = conv.parse_std_notation_string
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
        self.assertIsNone(test_board.last_move)
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
        # TODO: actually populate board first
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
            (Piece(ChessColor.WHITE), (num_rows, 0)),
            (Piece(ChessColor.WHITE), (0, num_cols))
        ]
        for pair in test_pieces_with_oob:
            with self.assertRaises(PiecePlacementException):
                test_board.populate([pair])
        # raise if two pieces are populated to same square
        dup_piece_strings = [
            'w Kb2',
            'w Qb2'
        ]
        dup_piece_list = [psns(s) for s in dup_piece_strings]
        with self.assertRaises(PiecePlacementException):
            test_board.populate(dup_piece_list)

        # board not cleared if populate fails.
        test_board.clear()
        good_test_strings = [
            'w Kd2',
            'w Qb4',
            'b h8',
            'b h5'
        ]
        good_test_list = [psns(s) for s in good_test_strings]
        test_board.populate(good_test_list)
        for test_piece, coordinates in good_test_list:
            row_idx = coordinates[0]
            col_idx = coordinates[1]
            self.assertEqual(test_board.squares[row_idx][col_idx].piece, test_piece)

    @patch.object(Board, '_handle_move_side_effect')
    @patch.object(Piece, 'get_move_params')
    def test_move_piece(self, move_mock, side_effect_mock):
        """tests function that actually moves pieces in the game."""
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        test_board = Board({'num_rows': num_rows, 'num_cols': num_cols})
        test_piece = Piece(ChessColor.WHITE)

        # should raise if coordinates are out of bounds
        oob_cases = [
            ((num_rows, 0), (0, 0)),
            ((0, 0), (num_rows, 0)),
            ((0, num_cols), (0, 0)),
            ((0, 0), (0, num_cols)),
            ((-1, 0), (0, 0)),
            ((0, 0), (-1, 0)),
            ((0, -1), (0, 0)),
            ((0, 0), (0, -1)),
        ]
        for oob_start, oob_end in oob_cases:
            with self.assertRaises(ValueError):
                test_board.move_piece(oob_start, oob_end, ChessColor.WHITE)

        start_coords, end_coords = ((0, 0), (1, 0))
        start_square = test_board.squares[start_coords[0]][start_coords[1]]
        end_square = test_board.squares[end_coords[0]][end_coords[1]]
        # should throw if start and end coords are equal
        with self.assertRaises(InvalidMoveException):
            test_board.move_piece(start_coords, start_coords, ChessColor.WHITE)

        # should raise if no piece lies on starting square
        with self.assertRaises(InvalidMoveException):
            test_board.move_piece(start_coords, end_coords, ChessColor.WHITE)

        start_square.add_piece(test_piece)
        # should raise if active_color is not equal to the piece being moved
        with self.assertRaises(InvalidMoveException):
            test_board.move_piece(start_coords, end_coords, ChessColor.BLACK)

        # should raise if piece.get_move throws
        move_mock.side_effect = InvalidMoveException('mock exception')
        with self.assertRaises(InvalidMoveException):
            test_board.move_piece(start_coords, end_coords, ChessColor.WHITE)

        # should successfully move the piece otherwise
        move_mock.side_effect = None
        basic_move_params = ((0, 0), (0, 0))
        basic_move = Move(*basic_move_params)
        move_mock.return_value = basic_move_params

        res = test_board.move_piece(start_coords, end_coords, ChessColor.WHITE)
        self.assertEqual(res, basic_move)
        self.assertFalse(start_square.is_occupied())
        self.assertEqual(test_piece, end_square.piece)
        self.assertEqual(test_board.last_move, basic_move)
        self.assertTrue(test_piece.has_moved)

        test_piece.has_moved = False

        # should call the side effect function if appropriate
        end_square.clear()
        start_square.add_piece(test_piece)
        side_effect_move_params = ((0, 0), (0, 0), None, None, 'some effect')
        side_effect_move = Move(*side_effect_move_params)
        move_mock.return_value = side_effect_move_params

        res = test_board.move_piece(start_coords, end_coords, ChessColor.WHITE)
        self.assertEqual(res, side_effect_move)
        side_effect_mock.assert_called_with(side_effect_move)

        # TODO: test this with same piece type but different locations, i.e. two pawns.
        # want to make sure the correct pawn is removed from player list

    def test_undo_move(self):
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        test_board = Board({'num_rows': num_rows, 'num_cols': num_cols})
        test_piece = Piece(ChessColor.BLACK)
        last_start = test_board.squares[0][0]
        last_end = test_board.squares[2][2]

        # should raise if no last move
        with self.assertRaises(InvalidMoveException):
            test_board.undo_move()

        # should move piece from last end to last start
        test_board.last_move = Move((0, 0), (2, 2))
        last_end.add_piece(test_piece)
        self.assertIsNone(last_start.piece)
        test_board.undo_move()
        self.assertEqual(last_start.piece, test_piece)
        self.assertIsNone(last_end.piece)

        last_start.clear()
        last_end.clear()
        # should replace piece if it was captured
        test_piece2 = Piece(ChessColor.WHITE)
        test_board.last_move = Move((0, 0), (2, 2), test_piece2, (2, 2))
        last_end.add_piece(test_piece)
        self.assertIsNone(last_start.piece)
        test_board.undo_move()
        self.assertEqual(last_start.piece, test_piece)
        self.assertEqual(last_end.piece, test_piece2)
    
    def test_get_active_pieces(self):
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        test_board = Board({'num_rows': num_rows, 'num_cols': num_cols})

        # test with empty piece list
        res = test_board.get_active_pieces()
        self.assertTupleEqual(res, ([], []))

        test1 = [
            'w Kd2',
            'w Qb4',
            'b h8',
            'b h5'
        ]
        test1_mapping = [psns(s) for s in test1]
        test_board.populate(test1_mapping)

        white_mapping = test1_mapping[0:2]
        black_mapping = test1_mapping[2:]

        res = test_board.get_active_pieces()
        self.assertTupleEqual(res, (white_mapping, black_mapping))

        # TODO: more tests

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
