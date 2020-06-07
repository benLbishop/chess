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

if __name__ == '__main__':
    unittest.main()
