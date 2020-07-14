"module for checking the state of the game (check, checkmate, etc)"
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.enums import ChessColor

# TODO: these should both be moved to the player class
def can_block_checking_piece(checking_path, board, player_piece_mapping):
    """Checks if any of the pieces provided in player_piece_mapping
        can capture or block the given checking piece.
    """
    # probably don't need to check the last square in path because it's king square
    path_coords = [(path_square.row_idx, path_square.col_idx) for path_square in checking_path]
    can_block = False
    for player_piece, player_piece_coords in player_piece_mapping:
        if player_piece.can_reach_squares(player_piece_coords, path_coords, board):
            can_block = True
            break
    return can_block

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
        try:
            check_path = piece.get_path_to_square(piece_square, king_square, board)
            # move from piece to king is valid, so it is checking king
            checking_pieces.append((piece, check_path)) # TODO: maybe make this a namedtuple
        except InvalidMoveException:
            continue
    return checking_pieces
