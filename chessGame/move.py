"""Module for the Move class."""
from dataclasses import dataclass

from .pieces.piece import Piece
from .square import Square
from .enums import MoveSideEffect

@dataclass
class Move:
    """Dataclass defining a chess move."""
    start: Square
    end: Square
    captured_piece: Piece = None
    captured_square: Square = None
    side_effect: MoveSideEffect = None
