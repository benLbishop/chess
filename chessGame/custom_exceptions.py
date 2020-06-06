"""module containing custom exception classes."""

class InvalidMoveException(Exception):
    """Exception for when an illegal move is attempted."""
    def __init__(self, *args):
        super().__init__(args)
