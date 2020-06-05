"""module containing the StandardBoard class."""
from board import Board
import constants

class StandardBoard(Board):
    """class representing a chess board of the standard 8x8 size."""
    def __init__(self):
        super().__init__(constants.STD_BOARD_WIDTH, constants.STD_BOARD_HEIGHT)
