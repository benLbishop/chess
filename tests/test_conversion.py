"""module for testing the methods in conversion.py."""
import unittest
from unittest.mock import patch
from chessGame.enums import ChessColor, PieceType
import chessGame.conversion as conv

class ConversionTest(unittest.TestCase):
    """tests for methods in conversion.py."""

    def test_parse_piece_color_char(self):
        white = ChessColor.WHITE
        black = ChessColor.BLACK
        valid_tests = [
            ('w', white),
            ('b', black),
            ('W', white),
            ('B', black),
            ('  w', white),
            ('b  ', black),
            (' B ', black)
        ]
        for s, result in valid_tests:
            self.assertEqual(conv.parse_piece_color_char(s), result)

        # TODO: invalid tests

    def test_parse_piece_type_char(self):
        valid_tests = [
            ('k', PieceType.KING),
            ('K', PieceType.KING),
            ('q', PieceType.QUEEN),
            ('Q', PieceType.QUEEN),
            ('r', PieceType.ROOK),
            ('R', PieceType.ROOK),
            ('b', PieceType.BISHOP),
            ('B', PieceType.BISHOP),
            ('n', PieceType.KNIGHT),
            ('N', PieceType.KNIGHT)
        ]

        for char, result in valid_tests:
            self.assertEqual(conv.parse_piece_type_char(char), result)

        # TODO: invalid tests

    def test_parse_rank_char(self):
        valid_tests = [
            ('a', 0),
            ('b', 1),
            ('c', 2),
            ('d', 3),
            ('e', 4),
            ('f', 5),
            ('g', 6),
            ('h', 7)
        ]

        for char, result in valid_tests:
            self.assertEqual(conv.parse_rank_char(char), result)

        # TODO: invalid tests

    def test_parse_file_char(self):
        valid_tests = [
            ('1', 0),
            ('2', 1),
            ('3', 2),
            ('4', 3),
            ('5', 4),
            ('6', 5),
            ('7', 6),
            ('8', 7)
        ]

        for char, result in valid_tests:
            self.assertEqual(conv.parse_file_char(char), result)

        # TODO: invalid tests

    @patch.object(conv, 'parse_file_char')
    @patch.object(conv, 'parse_rank_char')
    def test_parse_piece_location_string(self, rank_mock, file_mock):
        dummy_rank = 999
        dummy_file = 999
        dummy_res = (dummy_rank, dummy_file)
        rank_mock.return_value = dummy_rank
        file_mock.return_value = dummy_file

        # raise if the stripped string has len < 2
        short_strs = [
            '',
            'a',
            'a ',
            'a    '
        ]
        for s in short_strs:
            with self.assertRaises(ValueError):
                conv.parse_piece_location_string(s)

        pawn_tests = [
            ('a4', 'a', '4'),
            ('b3 ', 'b', '3'),
            ('h8   ', 'h', '8')
        ]
        for test_str, rank_input, file_input in pawn_tests:
            res = conv.parse_piece_location_string(test_str)
            self.assertTupleEqual(res, (dummy_rank, dummy_file))

            rank_mock.assert_called_with(rank_input)
            file_mock.assert_called_with(file_input)
        # TODO: invalid tests

    @patch.object(conv, 'parse_piece_location_string')
    @patch.object(conv, 'parse_piece_type_char')
    @patch.object(conv, 'parse_piece_color_char')
    def test_parse_std_notation_string(self, parse_color_mock, parse_type_mock, parse_loc_mock):
        parse_color_mock.return_value = 'dummy_color'
        parse_type_mock.return_value = 'dummy_type'
        dummy_loc = ('dummy_rank', 'dummy_file')
        parse_loc_mock.return_value = dummy_loc
        expected_res = (('dummy_type', 'dummy_color'), dummy_loc)
        pawn_tests = [
            ('w a4', 'w', 'a4'),
            ('b b3 ', 'b', 'b3'),
            ('w h8   ', 'w', 'h8')
        ]
        pawn_res = ((PieceType.PAWN, 'dummy_color'), dummy_loc)
        for test_str, color_input, loc_input in pawn_tests:
            res = conv.parse_std_notation_string(test_str)
            self.assertEqual(res, pawn_res)
            parse_type_mock.assert_not_called()
            parse_color_mock.assert_called_with(color_input)
            parse_loc_mock.assert_called_with(loc_input)

        # TODO: more tests


    def test_parse_piece_string(self):
        white_tests = [
            ('w', (PieceType.PAWN, ChessColor.WHITE)),
            ('w N', (PieceType.KNIGHT, ChessColor.WHITE)),
            ('w B', (PieceType.BISHOP, ChessColor.WHITE)),
            ('w R', (PieceType.ROOK, ChessColor.WHITE)),
            ('w Q', (PieceType.QUEEN, ChessColor.WHITE)),
            ('w K', (PieceType.KING, ChessColor.WHITE)),
        ]

        black_tests = [
            ('b', (PieceType.PAWN, ChessColor.BLACK)),
            ('b N', (PieceType.KNIGHT, ChessColor.BLACK)),
            ('b B', (PieceType.BISHOP, ChessColor.BLACK)),
            ('b R', (PieceType.ROOK, ChessColor.BLACK)),
            ('b Q', (PieceType.QUEEN, ChessColor.BLACK)),
            ('b K', (PieceType.KING, ChessColor.BLACK))
        ]

        for s, expected_res in white_tests:
            res = conv.parse_piece_string(s)
            self.assertEqual(res, expected_res)

        for s, expected_res in black_tests:
            res = conv.parse_piece_string(s)
            self.assertEqual(res, expected_res)
