'''module containing functions for moving chess pieces.'''
from custom_exceptions import InvalidMoveException
from pieceType import PieceType

def square_is_in_bounds(sqr, brd):
    return sqr.row_idx < brd.NUM_ROWS and sqr.col_idx < brd.NUM_COLS

def is_valid_pawn_destination(start_square, end_square):
    # TODO: En-passant
    pass

def is_valid_knight_destination(start_square, end_square):
    row_dist = abs(start_square.row_idx - end_square.row_idx)
    col_dist = abs(start_square.col_idx - end_square.col_idx)
    return (row_dist == 2 and col_dist == 1) or (row_dist == 1 and col_dist == 2)

def is_valid_bishop_destination(start_square, end_square):
    row_dist = abs(start_square.row_idx - end_square.row_idx)
    col_dist = abs(start_square.col_idx - end_square.col_idx)
    return row_dist == col_dist

def is_valid_rook_destination(start_square, end_square):
    # TODO: castling
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
    return is_valid_pawn_destination(start_square, end_square)

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
