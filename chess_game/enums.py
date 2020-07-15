"""module containing enums for the project."""
from enum import Enum

class ChessColor(Enum):
    """Enum for the chess colors."""
    WHITE = 0
    BLACK = 1

class MoveSideEffect(Enum):
    """Chess moves that require extra behavior."""
    CASTLE = 0
    EN_PASSANT = 1
    PAWN_PROMOTION = 2
