"""module for testing the Piece class."""
import unittest
from unittest.mock import patch
from chessGame.piece import Piece
from chessGame.enums import ChessColor, PieceType
import chessGame.conversion as conv

pfs = Piece.from_string
class PieceTest(unittest.TestCase):
    """Testing for the Piece class."""

    def test_init(self):
        """tests the constructor."""
        pawn = Piece(PieceType.PAWN, ChessColor.BLACK)
        self.assertEqual(pawn.name, PieceType.PAWN)
        self.assertEqual(pawn.color, ChessColor.BLACK)
        self.assertEqual(pawn.has_moved, False)

    def test_eq(self):
        """test the __eq__ classmethod."""
        pawn = pfs('b')
        pawn2 = pfs('b')
        rook = pfs('b R')

        self.assertEqual(pawn, pawn2)
        self.assertNotEqual(pawn, rook)

    @patch.object(conv, 'parse_piece_string')
    def test_from_string(self, get_params_mock):
        """tests the constructor class method that makes pieces from strings."""
        # should raise if string cannot be parsed
        get_params_mock.side_effect = ValueError('dummy error')

        with self.assertRaises(ValueError):
            Piece.from_string('')

if __name__ == '__main__':
    unittest.main()
