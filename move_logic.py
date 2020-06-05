'''module containing functions for moving chess pieces.'''
from custom_exceptions import InvalidMoveException
from pieceType import PieceType

def square_is_in_bounds(sqr, brd):
    return sqr.row_idx < brd.NUM_ROWS and sqr.col_idx < brd.NUM_COLS

def is_valid_pawn_destination(piece, start_square, end_square):
    pass

def is_valid_knight_destination(piece, start_square, end_square):
    pass

def is_valid_bishop_destination(piece, start_square, end_square):
    pass

def is_valid_rook_destination(piece, start_square, end_square):
    pass

def is_valid_queen_destination(piece, start_square, end_square):
    pass

def is_valid_king_destination(piece, start_square, end_square):
    pass

# TODO: this feels gross. There has to be a better way to do this
def is_valid_destination(piece, start_square, end_square):
    if (piece.name is PieceType.KING):
        return is_valid_king_destination(piece, start_square, end_square)
    elif (piece.name is PieceType.QUEEN):
        return is_valid_queen_destination(piece, start_square, end_square)
    elif (piece.name is PieceType.ROOK):
        return is_valid_rook_destination(piece, start_square, end_square)
    elif (piece.name is PieceType.BISHOP):
        return is_valid_bishop_destination(piece, start_square, end_square)
    elif (piece.name is PieceType.KNIGHT):
        return is_valid_knight_destination(piece, start_square, end_square)
    else:
        #pawn
        return is_valid_pawn_destination(piece, start_square, end_square)

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
