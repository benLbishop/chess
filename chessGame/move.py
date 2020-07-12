"""Module for the Move class."""
from dataclasses import dataclass

@dataclass
class Move:
    """Dataclass defining a chess move."""
    start_coords: tuple
    end_coords: tuple
    captured_piece: str = None # TODO: how to give type without circular import
    captured_piece_coords: tuple = None
    side_effect: str = None # TODO
