"""module for the PieceType enum."""
from enum import Enum

class PieceType(Enum):
    """Enum for the different types of chess pieces."""
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5
