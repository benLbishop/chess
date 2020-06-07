"module for checking the state of the game (check, checkmate, etc)"
from chessGame.custom_exceptions import InvalidMoveException
from . import pathing

def get_checking_pieces(board, player, opponent):
    """Finds any pieces that have the player's king in check.
        If none found, returns an empty list.
    """
    # king should always be first piece in array
    player_king = player.active_pieces[0]
    king_square = board.squares[player_king.row_idx][player_king.col_idx]

    checking_pieces = []
    for piece in opponent.active_pieces:
        piece_square = board.squares[piece.row_idx][piece.col_idx]
        try:
            pathing.get_move_path(piece, piece_square, king_square, board, opponent)
        except InvalidMoveException:
            continue
        # move from piece to king is valid, so we have check
        checking_pieces.append(piece)
    return checking_pieces
