'''module containing functions for moving chess pieces.'''
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.pieceType import PieceType
from chessGame.chessColor import ChessColor
from chessGame.chessEnums import MoveType

def square_is_in_bounds(sqr, brd):
    return sqr.row_idx < brd.NUM_ROWS and sqr.col_idx < brd.NUM_COLS

def is_valid_pawn_destination(start_square, end_square, color):
    # TODO: check special conditions. std capture, en-passant, first move
    row_offset = end_square.row_idx - start_square.row_idx
    col_offset = end_square.col_idx - start_square.col_idx
    # pawn can't move side to side or more than 2 rows
    if row_offset == 0 or abs(row_offset) > 2:
        return False

    if color == ChessColor.WHITE:
        if row_offset < 0:
            # white pawns can't move down in rows
            return False
        if row_offset == 2:
            # Only valid if column did not change.
            return col_offset == 0
    else:
        # ChessColor.BLACK
        if row_offset > 0:
            # black pawns can't move up in rows
            return False
        if row_offset == -2:
            # Only valid if column did not change.
            return col_offset == 0
    # abs(row_offset) should be 1 if we get here.
    # valid only if we move 0 or 1 columns
    return abs(col_offset < 2)

def is_valid_knight_destination(start_square, end_square):
    row_dist = abs(start_square.row_idx - end_square.row_idx)
    col_dist = abs(start_square.col_idx - end_square.col_idx)
    return (row_dist == 2 and col_dist == 1) or (row_dist == 1 and col_dist == 2)

def is_valid_bishop_destination(start_square, end_square):
    row_dist = abs(start_square.row_idx - end_square.row_idx)
    col_dist = abs(start_square.col_idx - end_square.col_idx)
    return row_dist == col_dist

def is_valid_rook_destination(start_square, end_square):
    row_dist = abs(start_square.row_idx - end_square.row_idx)
    col_dist = abs(start_square.col_idx - end_square.col_idx)
    return row_dist == 0 or col_dist == 0

def is_valid_queen_destination(start_square, end_square):
    valid_bishop_move = is_valid_bishop_destination(start_square, end_square)
    valid_rook_move = is_valid_rook_destination(start_square, end_square)
    return valid_bishop_move or valid_rook_move

def is_valid_king_destination(start_square, end_square):
    # TODO: castling
    row_dist = abs(start_square.row_idx - end_square.row_idx)
    col_dist = abs(start_square.col_idx - end_square.col_idx)
    return row_dist < 2 and col_dist < 2

# TODO: this feels gross. There has to be a better way to do this
def is_valid_destination(piece, start_square, end_square):
    if piece.name is PieceType.KING:
        return is_valid_king_destination(start_square, end_square)
    if piece.name is PieceType.QUEEN:
        return is_valid_queen_destination(start_square, end_square)
    if piece.name is PieceType.ROOK:
        return is_valid_rook_destination(start_square, end_square)
    if piece.name is PieceType.BISHOP:
        return is_valid_bishop_destination(start_square, end_square)
    if piece.name is PieceType.KNIGHT:
        return is_valid_knight_destination(start_square, end_square)
    #pawn
    return is_valid_pawn_destination(start_square, end_square, piece.color)

def validate_move(start_square, end_square, board, player):
    '''Attempts to move a piece from one square to another.

        Raises an InvalidMoveException if the move is illegal for some reason.
    '''
    if not square_is_in_bounds(start_square, board):
        raise InvalidMoveException('starting square OOB')

    if not square_is_in_bounds(end_square, board):
        raise InvalidMoveException('ending square OOB')

    if start_square == end_square:
        raise InvalidMoveException('start and end squares are equal')

    start_piece = start_square.piece
    if start_piece is None:
        raise InvalidMoveException('no piece in start square')

    if start_piece.color is not player.color:
        raise InvalidMoveException('piece is not controlled by player')

    try:
        attempt_move(start_piece, start_square, end_square, board)
    except InvalidMoveException as e:
        raise e

def get_necessary_move_type(start_square, end_square):
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
    r = cur_square.row_idx
    c = cur_square.col_idx
    if move_type is MoveType.UP:
        return (r + 1, c)
    if move_type is MoveType.DOWN:
        return (r - 1, c)
    if move_type is MoveType.LEFT:
        return (r, c - 1)
    if move_type is MoveType.RIGHT:
        return (r, c + 1)
    if move_type is MoveType.UP_LEFT:
        return (r + 1, c - 1)
    if move_type is MoveType.UP_RIGHT:
        return (r + 1, c + 1)
    if move_type is MoveType.DOWN_LEFT:
        return (r - 1, c - 1)
    if move_type is MoveType.DOWN_RIGHT:
        return (r - 1, c + 1)

def move_to_destination(start_square, end_square, board, move_type, piece_color):
    cur_square = start_square
    while True:
        next_row_idx, next_col_idx = get_next_square_indexes(cur_square, move_type)
        cur_square = board.squares[next_row_idx][next_col_idx]
        # TODO: clean up this logic, a bit confusing
        if cur_square is end_square:
            if not cur_square.is_occupied():
                return
            # raise if moving piece color is same as end square piece color
            if cur_square.piece.color is piece_color:
                raise InvalidMoveException('cannot move into square occupied by player piece')
            return
        # raise if piece cannot move due to a blocking piece
        if cur_square.is_occupied():
            raise InvalidMoveException('destination not reachable due to block')

def attempt_move(piece, start_square, end_square, board):
    # check if we can reach destination given the piece's moveset
    if not is_valid_destination(piece, start_square, end_square):
        raise InvalidMoveException('destination not reachable with piece')
    # get the movement necessary to reach destination
    move_type = get_necessary_move_type(start_square, end_square)
    # move one square at a time
    try:
        move_to_destination(start_square, end_square, board, move_type, piece.color)
    except InvalidMoveException as e:
        raise e
