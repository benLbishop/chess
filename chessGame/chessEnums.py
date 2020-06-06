"""module containing enums for the project."""
from enum import Enum

class ChessColor(Enum):
    """Enum for the chess colors."""
    WHITE = 0
    BLACK = 1

class PieceType(Enum):
    """Enum for the different types of chess pieces."""
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

class MoveType(Enum):
    """Enum for the types of movements pieces can make to adjacent squares."""
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP_RIGHT = 4
    UP_LEFT = 5
    DOWN_RIGHT = 6
    DOWN_LEFT = 7
