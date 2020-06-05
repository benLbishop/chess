import unittest
from piece import Piece
from pieceType import PieceType
from chessColor import ChessColor

class PieceTest(unittest.TestCase):
    """Testing for the Piece class."""

    def test_init(self):
        pawn = Piece(PieceType.PAWN, ChessColor.BLACK)
        self.assertEqual(pawn.name, PieceType.PAWN)
        self.assertEqual(pawn.color, ChessColor.BLACK)

if __name__ == '__main__':
    unittest.main()
