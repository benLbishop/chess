"""module containing functions for determing paths pieces can take."""
from chessGame.enums import MoveType
from chessGame.custom_exceptions import InvalidMoveException

def get_necessary_move_type(start_square, end_square):
    """Returns the MoveType required to properly get to end_square from start_square.
        Assumes that movement from start_square to end_square is possible in a legal chess move.

        Returns a boolean.
    """
    row_diff = end_square.row_idx - start_square.row_idx
    col_diff = end_square.col_idx - start_square.col_idx
    if col_diff == 0:
        return MoveType.UP if row_diff > 0 else MoveType.DOWN
    if row_diff == 0:
        return MoveType.RIGHT if col_diff > 0 else MoveType.LEFT
    if row_diff > 0:
        # moved up and diagonal
        return MoveType.UP_RIGHT if col_diff > 0 else MoveType.UP_LEFT
    # moved down and diagonal
    return MoveType.DOWN_RIGHT if col_diff > 0 else MoveType.DOWN_LEFT

def get_next_square_indexes(cur_square, move_type):
    """Returns a tuple containing the square from moving from cur_square using move_type.
    """
    r_idx = cur_square.row_idx
    c_idx = cur_square.col_idx
    if move_type is MoveType.UP:
        return (r_idx + 1, c_idx)
    if move_type is MoveType.DOWN:
        return (r_idx - 1, c_idx)
    if move_type is MoveType.LEFT:
        return (r_idx, c_idx - 1)
    if move_type is MoveType.RIGHT:
        return (r_idx, c_idx + 1)
    if move_type is MoveType.UP_LEFT:
        return (r_idx + 1, c_idx - 1)
    if move_type is MoveType.UP_RIGHT:
        return (r_idx + 1, c_idx + 1)
    if move_type is MoveType.DOWN_LEFT:
        return (r_idx - 1, c_idx - 1)
    # MoveType.DOWN_RIGHT:
    return (r_idx - 1, c_idx + 1)
