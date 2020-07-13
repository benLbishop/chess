"""module containing functions for determing paths pieces can take."""

def get_necessary_offset(start_square, end_square):
    """Returns the offset required to properly get to end_square from start_square.
        Assumes that movement from start_square to end_square is possible in a legal chess move.

        Returns a boolean.
    """
    # TODO: move somewhere else? Only used by Piece class currently,
    # but doesn't feel like it fits there
    row_diff = end_square.row_idx - start_square.row_idx
    col_diff = end_square.col_idx - start_square.col_idx
    if col_diff == 0:
        return (1, 0) if row_diff > 0 else (-1, 0)
    if row_diff == 0:
        return (0, 1) if col_diff > 0 else (0, -1)
    if row_diff > 0:
        # moved up and diagonal
        return (1, 1) if col_diff > 0 else (1, -1)
    # moved down and diagonal
    return (-1, 1) if col_diff > 0 else (-1, -1)
