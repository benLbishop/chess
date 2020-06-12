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
        row_idx, col_idx = 3, 4
        pawn = pfs('b e4')
        self.assertEqual(pawn.name, PieceType.PAWN)
        self.assertEqual(pawn.color, ChessColor.BLACK)
        self.assertEqual(pawn.row_idx, row_idx)
        self.assertEqual(pawn.col_idx, col_idx)
        self.assertEqual(pawn.has_moved, False)

    def test_eq(self):
        """test the __eq__ classmethod."""
        pawn = pfs('b e4')
        pawn2 = pfs('b e4')
        pawn3 = pfs('w e4')
        pawn4 = pfs('b e1')
        pawn5 = pfs('b a4')
        rook = pfs('b Re4')

        self.assertEqual(pawn, pawn2)
        self.assertNotEqual(pawn, pawn3)
        self.assertNotEqual(pawn, pawn4)
        self.assertNotEqual(pawn, pawn5)
        self.assertNotEqual(pawn, rook)

    @patch.object(conv, 'get_piece_params')
    def test_from_string(self, get_params_mock):
        """tests the constructor class method that makes pieces from strings."""
        # should raise if string cannot be parsed
        get_params_mock.side_effect = ValueError('dummy error')

        with self.assertRaises(ValueError):
            Piece.from_string('')

if __name__ == '__main__':
    unittest.main()
