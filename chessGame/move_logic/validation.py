"""module containing functions for moving chess pieces."""
from chessGame.custom_exceptions import InvalidMoveException

def square_is_in_bounds(sqr, brd):
    """determine if a square is on the board.

    Returns a boolean.
    """
    return sqr.row_idx < brd.NUM_ROWS and sqr.col_idx < brd.NUM_COLS

def validate_move(start_square, end_square, board, player):
    """Runs the attempted move through a series of preliminary checks.

        Raises an InvalidMoveException if the move is illegal for some reason.
    """
    if not square_is_in_bounds(start_square, board):
        raise InvalidMoveException('starting square OOB')

    if not square_is_in_bounds(end_square, board):
        raise InvalidMoveException('ending square OOB')

    if start_square == end_square:
        raise InvalidMoveException('start and end squares are equal')

    start_piece = start_square.piece
    if not start_piece:
        raise InvalidMoveException('no piece in start square')

    if start_piece.color is not player.color:
        raise InvalidMoveException('piece is not controlled by player')

    # check if we can reach destination given the piece's moveset
    if not start_piece.can_reach_square(start_square, end_square):
        raise InvalidMoveException('destination not reachable with piece')
