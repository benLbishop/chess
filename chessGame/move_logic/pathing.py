"""module containing functions for determing paths pieces can take."""
from chessGame.enums import PieceType, MoveType
from chessGame.custom_exceptions import InvalidMoveException
from . import validation

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

def get_pawn_path_to_destination(start_square, end_square, board, pawn):
    """Attempts to get the path from start_square to end_square given the piece is a pawn.

    Raises an InvalidMoveException if the move is illegal for some reason.
    """
    row_offset = end_square.row_idx - start_square.row_idx
    col_offset = end_square.col_idx - start_square.col_idx
    if abs(row_offset) == 2:
        if pawn.has_moved:
            raise InvalidMoveException('pawn tried moving 2 squares, but has already moved')
        # destination has been validated, so col_offset == 0
        if end_square.is_occupied():
            raise InvalidMoveException('pawn blocked straight ahead')
        start_row_idx = start_square.row_idx
        intermediate_row_idx = start_row_idx + 1 if row_offset > 0 else start_row_idx - 1
        intermediate_square = board.squares[intermediate_row_idx][start_square.col_idx]
        if intermediate_square.is_occupied():
            raise InvalidMoveException('pawn blocked straight ahead')
        return [intermediate_square, end_square]
    # row offset must be 1
    path = [end_square]
    if col_offset == 0:
        if end_square.is_occupied():
            raise InvalidMoveException('pawn blocked straight ahead')
        return path
    # abs(col_offset) must be 1
    # end_square must have a piece # TODO: En-passant
    if not end_square.is_occupied():
        raise InvalidMoveException('pawn cannot move diagonally without capturing')
    if end_square.piece.color is pawn.color:
        raise InvalidMoveException('cannot move into square occupied by player piece')
    return path

def get_knight_path_to_destination(end_square, piece):
    """Attempts to get the path for knights.

    Raises an InvalidMoveException if the move is illegal for some reason.
    """
    path = [end_square]
    if not end_square.is_occupied():
        return path
    if end_square.piece.color is piece.color:
        raise InvalidMoveException('cannot move into square occupied by player piece')
    # capturing opponent piece
    return path

# TODO: rename
def get_others_path_to_destination(start_square, end_square, board, piece):
    """Attempts to get the path for bishops, rooks, queens, and kings.

    Raises an InvalidMoveException if the move is illegal for some reason.
    """
    # get the movement necessary to reach destination
    move_type = get_necessary_move_type(start_square, end_square)

    cur_square = start_square
    path = []
    while True:
        next_row_idx, next_col_idx = get_next_square_indexes(cur_square, move_type)
        cur_square = board.squares[next_row_idx][next_col_idx]
        # TODO: clean up this logic, a bit confusing
        if cur_square is end_square:
            if not cur_square.is_occupied():
                path.append(cur_square)
                return path
            # raise if moving piece color is same as end square piece color
            if cur_square.piece.color is piece.color:
                raise InvalidMoveException('cannot move into square occupied by player piece')
            path.append(cur_square)
            return path
        # raise if piece cannot move due to a blocking piece
        if cur_square.is_occupied():
            raise InvalidMoveException('destination not reachable due to block')
        path.append(cur_square)

def get_path_to_destination(start_square, end_square, board, piece):
    """Attempts to get the path from start_square to end_square.

    Raises an InvalidMoveException if the move is illegal for some reason.
    """
    # TODO: how do castle
    try:
        if piece.name is PieceType.PAWN:
            return get_pawn_path_to_destination(start_square, end_square, board, piece)
        if piece.name is PieceType.KNIGHT:
            return get_knight_path_to_destination(end_square, piece)
        # bishop, rook, queen, or king
        return get_others_path_to_destination(start_square, end_square, board, piece)
    except InvalidMoveException as err:
        raise err

def get_move_path(piece, start_square, end_square, board, player):
    """Tries to get the path for the given move.

    Raises an InvalidMoveException if the path cannot be found.
    """
    try:
        validation.validate_move(start_square, end_square, board, player)
    except InvalidMoveException as err:
        raise err
    # get the path
    try:
        return get_path_to_destination(start_square, end_square, board, piece)
    except InvalidMoveException as err:
        raise err
