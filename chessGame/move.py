"""Module for the Move class."""
from dataclasses import dataclass
from chessGame.pieces.piece import Piece

@dataclass
class Move:
    """Dataclass defining a chess move."""
    start_coords: tuple
    end_coords: tuple
    captured_piece: Piece = None
    captured_piece_coords: tuple = None
    side_effect: str = None # TODO
