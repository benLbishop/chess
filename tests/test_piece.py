import unittest
from chessGame.piece import Piece
from chessGame.chessEnums import ChessColor, PieceType

class PieceTest(unittest.TestCase):
    """Testing for the Piece class."""

    def test_init(self):
        pawn = Piece(PieceType.PAWN, ChessColor.BLACK)
        self.assertEqual(pawn.name, PieceType.PAWN)
        self.assertEqual(pawn.color, ChessColor.BLACK)

if __name__ == '__main__':
    unittest.main()
