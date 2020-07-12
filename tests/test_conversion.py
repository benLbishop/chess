"""module for testing the methods in conversion.py."""
import unittest
from unittest.mock import patch
from chessGame.enums import ChessColor
from chessGame import conversion as conv
from chessGame.pieces import (
    king,
    queen,
    rook,
    bishop,
    knight,
    pawn
)

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
            ('k', king.King),
            ('K', king.King),
            ('q', queen.Queen),
            ('Q', queen.Queen),
            ('r', rook.Rook),
            ('R', rook.Rook),
            ('b', bishop.Bishop),
            ('B', bishop.Bishop),
            ('n', knight.Knight),
            ('N', knight.Knight)
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
        dummy_file = 123
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
            self.assertTupleEqual(res, (dummy_file, dummy_rank))

            rank_mock.assert_called_with(rank_input)
            file_mock.assert_called_with(file_input)
        # TODO: invalid tests

    @patch.object(conv, 'parse_piece_location_string')
    @patch.object(conv, 'parse_piece_type_char')
    @patch.object(conv, 'parse_piece_color_char')
    def test_parse_std_notation_string(self, parse_color_mock, parse_type_mock, parse_loc_mock):
        dummy_color = ChessColor.WHITE
        parse_color_mock.return_value = dummy_color
        parse_type_mock.return_value = 'dummy_type'
        dummy_loc = ('dummy_rank', 'dummy_file')
        parse_loc_mock.return_value = dummy_loc
        pawn_tests = [
            ('w a4', 'w', 'a4'),
            ('b b3 ', 'b', 'b3'),
            ('w h8   ', 'w', 'h8')
        ]
        for test_str, color_input, loc_input in pawn_tests:
            res = conv.parse_std_notation_string(test_str)
            p = res[0]
            self.assertTrue(isinstance(p, pawn.Pawn))
            self.assertEqual(p.color, dummy_color)
            parse_type_mock.assert_not_called()
            parse_color_mock.assert_called_with(color_input)
            parse_loc_mock.assert_called_with(loc_input)

        # TODO: more tests


    def test_parse_piece_string(self):
        white_tests = [
            ('w', pawn.Pawn, ChessColor.WHITE),
            ('w N', knight.Knight, ChessColor.WHITE),
            ('w B', bishop.Bishop, ChessColor.WHITE),
            ('w R', rook.Rook, ChessColor.WHITE),
            ('w Q', queen.Queen, ChessColor.WHITE),
            ('w K', king.King, ChessColor.WHITE)
        ]

        black_tests = [
            ('b', pawn.Pawn, ChessColor.BLACK),
            ('b N', knight.Knight, ChessColor.BLACK),
            ('b B', bishop.Bishop, ChessColor.BLACK),
            ('b R', rook.Rook, ChessColor.BLACK),
            ('b Q', queen.Queen, ChessColor.BLACK),
            ('b K', king.King, ChessColor.BLACK)
        ]

        for s, expected_class, expected_color in white_tests:
            res = conv.parse_piece_string(s)
            self.assertTrue(isinstance(res, expected_class))
            self.assertEqual(res.color, expected_color)

        for s, expected_class, expected_color in black_tests:
            res = conv.parse_piece_string(s)
            self.assertTrue(isinstance(res, expected_class))
            self.assertEqual(res.color, expected_color)
