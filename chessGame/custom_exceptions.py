"""module containing custom exception classes."""

class InvalidMoveException(Exception):
    """Exception for when an illegal move is attempted."""
    def __init__(self, *args):
        super().__init__(args)

class PiecePlacementException(Exception):
    """Exception for when an attempt is made to place a piece off of the board."""
    def __init__(self, *args):
        super().__init__(args)
