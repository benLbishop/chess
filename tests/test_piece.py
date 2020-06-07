"""module for testing the Piece class."""
import unittest
from chessGame.piece import Piece
from chessGame.enums import ChessColor, PieceType

class PieceTest(unittest.TestCase):
    """Testing for the Piece class."""

    def test_init(self):
        """tests the constructor."""
        row_idx, col_idx = 3, 4
        pawn = Piece(PieceType.PAWN, ChessColor.BLACK, row_idx, col_idx)
        self.assertEqual(pawn.name, PieceType.PAWN)
        self.assertEqual(pawn.color, ChessColor.BLACK)
        self.assertEqual(pawn.row_idx, row_idx)
        self.assertEqual(pawn.col_idx, col_idx)
        self.assertEqual(pawn.has_moved, False)

    def test_eq(self):
        """test the __eq__ classmethod."""
        p = Piece(PieceType.PAWN, ChessColor.BLACK, 3, 4)
        p2 = Piece(PieceType.PAWN, ChessColor.BLACK, 3, 4)
        p3 = Piece(PieceType.PAWN, ChessColor.WHITE, 3, 4)
        p4 = Piece(PieceType.PAWN, ChessColor.BLACK, 0, 4)
        p5 = Piece(PieceType.PAWN, ChessColor.BLACK, 3, 0)
        rook = Piece(PieceType.ROOK, ChessColor.BLACK, 3, 4)

        self.assertEqual(p, p2)
        self.assertNotEqual(p, p3)
        self.assertNotEqual(p, p4)
        self.assertNotEqual(p, p5)
        self.assertNotEqual(p, rook)

if __name__ == '__main__':
    unittest.main()
