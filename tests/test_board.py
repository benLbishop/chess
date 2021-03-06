"""module containing tests for the Board class."""
import unittest
from unittest.mock import patch

from chess_game.board import Board, StandardBoard, CheckingReturnType
from chess_game.pieces.piece import Piece
from chess_game import constants, conversion as conv
from chess_game.enums import ChessColor, MoveSideEffect
from chess_game.custom_exceptions import PiecePlacementException, InvalidMoveException
from chess_game.move import Move

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
        self.assertEqual(test_board._num_rows, constants.STD_BOARD_WIDTH)
        self.assertEqual(test_board._num_cols, constants.STD_BOARD_HEIGHT)
        self.assertEqual(test_board.move_history, [])
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
        squares = test_board.squares
        # test clearing when board is already empty
        test_board.clear()
        for row in squares:
            for square in row:
                self.assertFalse(square.is_occupied())

        # test clearing when board has pieces
        squares[0][0].piece = Piece(ChessColor.WHITE)
        squares[2][2].piece = Piece(ChessColor.BLACK)
        squares[5][1].piece = Piece(ChessColor.WHITE)
        squares[4][3].piece = Piece(ChessColor.BLACK)
        squares[1][6].piece = Piece(ChessColor.WHITE)
        squares[7][7].piece = Piece(ChessColor.BLACK)
        test_board.clear()
        for row in squares:
            for square in row:
                self.assertFalse(square.is_occupied())

        # should reset move history
        move = Move(squares[0][0], squares[1][0])
        test_board.move_history = [move]
        test_board.clear()
        self.assertEqual(test_board.move_history, [])

    @patch.object(Board, 'clear')
    def test_populate(self, clear_mock):
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
        clear_mock.assert_called()

        clear_mock.reset_mock()
        # raise if two pieces are populated to same square
        dup_piece_strings = [
            'w Kb2',
            'w Qb2'
        ]
        dup_piece_list = [psns(s) for s in dup_piece_strings]
        with self.assertRaises(PiecePlacementException):
            test_board.populate(dup_piece_list)
        clear_mock.assert_called()
        
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

    def test_get_castling_rook_squares(self):
        """Tests for the private _get_castling_rook_squares method."""
        # TODO

    def test_handle_castle_side_effect(self):
        """Tests for the private _handle_castle_side_effect method."""
        # TODO

    def test_handle_en_passant_side_effect(self):
        """Tests for the private _handle_en_passant_side_effect method."""
        # TODO

    @patch.object(Board, '_handle_en_passant_side_effect')
    @patch.object(Board, '_handle_castle_side_effect')
    def test_handle_move_side_effect(self, castle_mock, passant_mock):
        """Tests for the private _handle_move_side_effect method."""
        # TODO

    @patch.object(Board, 'undo_move')
    @patch.object(Board, '_handle_move_side_effect')
    @patch.object(Board, 'get_checking_pieces')
    @patch.object(Piece, 'get_move_params')
    def test_move_piece(self, move_mock, check_mock, side_effect_mock, undo_mock):
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

        start_square.piece = test_piece
        # should raise if active_color is not equal to the piece being moved
        with self.assertRaises(InvalidMoveException):
            test_board.move_piece(start_coords, end_coords, ChessColor.BLACK)

        # should raise if piece.get_move throws
        move_mock.side_effect = InvalidMoveException('mock exception')
        with self.assertRaises(InvalidMoveException):
            test_board.move_piece(start_coords, end_coords, ChessColor.WHITE)
        move_mock.side_effect = None

        # should successfully move the piece otherwise
        basic_move_params = (start_square, end_square)
        basic_move = Move(*basic_move_params)
        move_mock.return_value = basic_move_params

        res = test_board.move_piece(start_coords, end_coords, ChessColor.WHITE)
        self.assertEqual(res, basic_move)
        self.assertFalse(start_square.is_occupied())
        self.assertEqual(test_piece, end_square.piece)
        self.assertEqual(test_board.move_history, [basic_move])
        self.assertTrue(test_piece.has_moved)

        test_piece.move_count = 0
        end_square.piece = None
        start_square.piece = test_piece

        # should call the side effect function if appropriate
        side_effect_move_params = (start_square, end_square, None, None, 'some effect')
        side_effect_move = Move(*side_effect_move_params)
        move_mock.return_value = side_effect_move_params

        res = test_board.move_piece(start_coords, end_coords, ChessColor.WHITE)
        self.assertEqual(res, side_effect_move)
        side_effect_mock.assert_called_with(side_effect_move)

        test_piece.move_count = 0
        end_square.piece = None
        start_square.piece = test_piece

        # should raise if player puts themselves in check and call undo_move
        check_mock.return_value = ['something']
        with self.assertRaises(InvalidMoveException):
            test_board.move_piece(start_coords, end_coords, ChessColor.WHITE)
            undo_mock.assert_called_once()
        check_mock.return_value = []

    @patch.object(Board, '_undo_castle_side_effect')
    def test_undo_move(self, undo_castle_mock):
        """Tests the undo_move method."""
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
        test_board.move_history = [Move(last_start, last_end)]
        last_end.piece = test_piece
        self.assertIsNone(last_start.piece)
        test_board.undo_move()
        self.assertEqual(last_start.piece, test_piece)
        self.assertIsNone(last_end.piece)

        # should decrement piece's move count
        self.assertEqual(test_piece.move_count, -1)

        last_start.piece = None
        last_end.piece = None
        # should replace piece if it was captured
        test_piece2 = Piece(ChessColor.WHITE)
        test_board.move_history = [Move(last_start, last_end, test_piece2, last_end)]
        last_end.piece = test_piece
        self.assertIsNone(last_start.piece)
        test_board.undo_move()
        self.assertEqual(last_start.piece, test_piece)
        self.assertEqual(last_end.piece, test_piece2)

        last_start.piece = None
        last_end.piece = None

        # should undo the castling properly
        test_board.move_history = [Move(last_start, last_end, None, None, MoveSideEffect.CASTLE)]
        last_end.piece = test_piece
        test_board.undo_move()
        undo_castle_mock.assert_called_once()

    def test_undo_castle_side_effect(self):
        """Tests for the private _undo_castle_side_effect method."""
        # TODO

    @patch.object(Piece, 'get_path_to_square')
    @patch.object(Board, 'get_active_pieces')
    def test_get_checking_pieces(self, active_pieces_mock, path_mock):
        """Tests for the get_checking_pieces method."""
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        test_board = Board({'num_rows': num_rows, 'num_cols': num_cols})

        white_dummy_king = Piece(ChessColor.WHITE)
        white_mapping = [
            (white_dummy_king, test_board.squares[1][1]),
            (Piece(ChessColor.WHITE), test_board.squares[1][2]),
            (Piece(ChessColor.WHITE), test_board.squares[1][3])
        ]
        black_dummy_king = Piece(ChessColor.BLACK)
        black_mapping = [
            (black_dummy_king, test_board.squares[7][1]),
            (Piece(ChessColor.BLACK), test_board.squares[7][2]),
            (Piece(ChessColor.BLACK), test_board.squares[7][3])
        ]
        active_pieces_mock.return_value = (white_mapping, black_mapping)
        # should use the correct piece mapping
        # TODO

        # should return any pieces checking king
        path_mock.side_effect = ['path1', InvalidMoveException('path exception'), 'path2']
        expected_res = [CheckingReturnType(black_mapping[0][0], 'path1'), CheckingReturnType(black_mapping[2][0], 'path2')]
        res = test_board.get_checking_pieces(ChessColor.WHITE)
        self.assertEqual(res, expected_res)

        # TODO: more tests

    def test_get_active_pieces(self):
        """Tests the get_active_pieces method."""
        num_rows = constants.STD_BOARD_WIDTH
        num_cols = constants.STD_BOARD_HEIGHT
        test_board = Board({'num_rows': num_rows, 'num_cols': num_cols})

        # test with empty piece list
        res = test_board.get_active_pieces()
        self.assertTupleEqual(res, ([], []))

        white_strings = [
            'w Kd2',
            'w Qb4'
        ]
        black_strings = [
            'b h8',
            'b h5'
        ]
        white_coord_map = [psns(s) for s in white_strings]
        black_coord_map = [psns(s) for s in black_strings]
        test_board.populate(white_coord_map + black_coord_map)

        white_mapping = [(p, test_board.squares[row][col]) for p, (row, col) in white_coord_map]
        black_mapping = [(p, test_board.squares[row][col]) for p, (row, col) in black_coord_map]

        res = test_board.get_active_pieces()
        self.assertTupleEqual(res, (white_mapping, black_mapping))

        # TODO: more tests

    def test_promote_pawn(self):
        """Tests for the promote_pawn method."""
        # TODO

class StandardBoardTest(unittest.TestCase):
    """tests for the derived Board class StandardBoard."""

    def test_init(self):
        """tests for the constructor."""
        # should create an 8x8 board
        std_board = StandardBoard()
        self.assertEqual(std_board._num_rows, 8)
        self.assertEqual(std_board._num_cols, 8)

if __name__ == '__main__':
    unittest.main()
