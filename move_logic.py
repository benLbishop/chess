'''module containing functions for moving chess pieces.'''
from custom_exceptions import InvalidMoveException

def square_is_in_bounds(sqr, brd):
    return sqr.row_idx < brd.NUM_ROWS and sqr.col_idx < brd.NUM_COLS

def move_piece(start_square, end_square, board, player):
    '''Attempts to move a piece from one square to another.

        Raises an InvalidMoveException if the move is illegal for some reason.
    '''
    if not square_is_in_bounds(start_square, board):
        raise InvalidMoveException('starting square OOB')
