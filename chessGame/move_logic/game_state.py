"module for checking the state of the game (check, checkmate, etc)"
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.enums import ChessColor
from chessGame import constants
from . import pathing

def player_is_checkmated(board, active_player_color, checking_pieces):
    """Does what it sounds like, a.k.a. returns whether or not the player is checkmated.

    This should only after it's confirmed that the player is in check.
    """
    # TODO

def player_is_stalemated(board, active_player_color):
    """Does what it sounds like, a.k.a. returns whether or not the game has reached a stalemate.

    This should only after it's confirmed that the player is not in check.
    """
    # TODO

def get_checking_pieces(board, active_player_color):
    """Finds any pieces that have the player's king in check.
        If none found, returns an empty list.
    """
    white_mapping, black_mapping = board.get_active_pieces()
    player_piece_mapping = white_mapping
    opponent_piece_mapping = black_mapping
    if active_player_color is not ChessColor.WHITE:
        player_piece_mapping = black_mapping
        opponent_piece_mapping = white_mapping
    # king should always be first piece in array
    _, (king_row_idx, king_col_idx) = player_piece_mapping[0]
    king_square = board.squares[king_row_idx][king_col_idx]

    checking_pieces = []
    for piece, (row_idx, col_idx) in opponent_piece_mapping:
        piece_square = board.squares[row_idx][col_idx]
        if not piece.can_reach_square(piece_square, king_square):
            continue
        try:
            check_path = piece.get_path_to_square(piece_square, king_square, board)
            # move from piece to king is valid, so it is checking king
            checking_pieces.append((piece, check_path))
        except InvalidMoveException:
            continue
    return checking_pieces
