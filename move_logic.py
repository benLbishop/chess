'''module containing functions for moving chess pieces.'''
from custom_exceptions import InvalidMoveException
from pieceType import PieceType
from chessColor import ChessColor

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

def attempt_move():
    pass
