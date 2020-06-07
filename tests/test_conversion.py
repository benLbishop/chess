"""module for testing the methods in conversion.py."""
import unittest
from unittest.mock import patch
from chessGame.piece import Piece
from chessGame.enums import ChessColor, PieceType
import chessGame.conversion as conv

class ConversionTest(unittest.TestCase):
    """tests for methods in conversion.py."""

    def test_parse_piece_color_string(self):
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
            self.assertEqual(conv.parse_piece_color_string(s), result)

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
    @patch.object(conv, 'parse_piece_type_char')
    def test_parse_piece_location_string(self, piece_type_mock, rank_mock, file_mock):
        dummy_type = 'dummy type'
        dummy_rank = 'dummy rank'
        dummy_file = 'dummy file'
        dummy_res = (dummy_type, dummy_rank, dummy_file)
        piece_type_mock.return_value = dummy_type
        rank_mock.return_value = dummy_rank
        file_mock.return_value = dummy_file

        # raise if the stripped string has len < 2
        short_strs = [
            '',
            'a',
            '   a ',
            'a    '
        ]
        for s in short_strs:
            with self.assertRaises(ValueError):
                conv.parse_piece_location_string(s)

        # len == 2 tests
        pawn_tests = [
            ('a4', 'a', '4'),
            ('    b3', 'b', '3'),
            ('  h8 ', 'h', '8')
        ]
        for test_str, rank_input, file_input in pawn_tests:
            res = conv.parse_piece_location_string(test_str)
            self.assertTupleEqual(res, (PieceType.PAWN, dummy_rank, dummy_file))

            piece_type_mock.assert_not_called()
            rank_mock.assert_called_with(rank_input)
            file_mock.assert_called_with(file_input)

        # len > 2 tests
        other_type_tests = [
            ('Na4', 'N', 'a', '4'),
            ('    Bb3', 'B', 'b', '3'),
            ('  Kh8 ', 'K', 'h', '8')
        ]
        for test_str, type_input, rank_input, file_input in other_type_tests:
            res = conv.parse_piece_location_string(test_str)
            self.assertTupleEqual(res, dummy_res)

            piece_type_mock.assert_called_with(type_input)
            rank_mock.assert_called_with(rank_input)
            file_mock.assert_called_with(file_input)
        # TODO: invalid tests

    def test_parse_piece_string(self):
        # should handle white space
        # test_cases = [
        #     ('w a4', Piece(PieceType.PAWN, ChessColor.WHITE)),
        #     ('b Ka4', Piece(PieceType.KNIGHT, ChessColor.BLACK)),
        # ]
        # for piece_str, result in test_cases:
        #     self.assertEqual(conv.parse_piece_string(piece_str), result)

        # TODO
        pass

    @patch.object(conv, 'parse_piece_string')
    def test_convert_strings_to_pieces(self, parse_string_mock):
        # raise if any of the strings can't be parsed
        test_strs = [
            '',
            '',
            '',
            ''
        ]
        parse_string_mock.side_effect = ['res1', 'res2', ValueError('dummy error')]

        with self.assertRaises(ValueError):
            conv.convert_strings_to_pieces(test_strs)

        # TODO: more tests
