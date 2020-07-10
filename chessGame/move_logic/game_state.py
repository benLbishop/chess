"module for checking the state of the game (check, checkmate, etc)"
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.enums import PieceType, ChessColor
from chessGame import constants
from . import pathing

def player_is_checkmated(board, player, opponent, checking_pieces):
    """Does what it sounds like, a.k.a. returns whether or not the player is checkmated.

    This should only after it's confirmed that the player is in check.
    """
    # TODO

def player_is_stalemated(board, player, opponent):
    """Does what it sounds like, a.k.a. returns whether or not the game has reached a stalemate.

    This should only after it's confirmed that the player is not in check.
    """
    # TODO
    return False

def get_checking_pieces(board, player, opponent):
    """Finds any pieces that have the player's king in check.
        If none found, returns an empty list.
    """
    # king should always be first piece in array
    white_pieces, black_pieces = board.get_active_pieces()
    player_king = white_pieces[0] if player.color == ChessColor.WHITE else black_pieces[0]
    king_square = board.squares[player_king.row_idx][player_king.col_idx]

    checking_pieces = []
    for piece in opponent.active_pieces:
        piece_square = board.squares[piece.row_idx][piece.col_idx]
        try:
            pathing.get_move_path(piece_square, king_square, board, opponent)
        except InvalidMoveException:
            continue
        # move from piece to king is valid, so we have check
        checking_pieces.append(piece)
    return checking_pieces

# TODO: move
def get_move_options(piece):
    # TODO: I'd like to just pass in piece_type, but pawn is color-dependent.
    # maybe find a way to put this in Piece class and make a Pawn subclass.
    """takes a piece and returns all of the possible incremental moves."""
    if piece.name == PieceType.PAWN:
        if piece.color == ChessColor.WHITE:
            return constants.PAWN_WHITE_MOVES
        else:
            return constants.PAWN_BLACK_MOVES
    if piece.name == PieceType.BISHOP:
        return constants.BISHOP_MOVES
    if piece.name == PieceType.ROOK:
        return constants.ROOK_MOVES
    if piece.name == PieceType.QUEEN:
        return constants.QUEEN_MOVES
    if piece.name == PieceType.KING:
        return constants.KING_MOVES
    # Knight
    return [] # TODO: wat

def get_valid_adjacent_squares(piece, board, player):
    """Determines if the given piece has any valid move."""
    start_row_idx = piece.row_idx
    start_col_idx = piece.col_idx
    start_square = board.squares[start_row_idx][start_col_idx]
    move_list = get_move_options(piece)

    valid_squares = []
    for move in move_list:
        next_row_idx, next_col_idx = pathing.get_next_square_indexes(start_square, move)
        if next_row_idx >= board.NUM_ROWS or next_col_idx >= board.NUM_COLS:
            # out of bounds
            continue
        next_square = board.squares[next_row_idx][next_col_idx]
        try:
            pathing.get_move_path(start_square, next_square, board, player)
            valid_squares.append(next_square)
        except InvalidMoveException:
            continue
    return valid_squares