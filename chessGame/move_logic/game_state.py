"module for checking the state of the game (check, checkmate, etc)"
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.enums import ChessColor

def can_block_checking_piece(checking_piece_data, board, player_piece_mapping):
    _, checking_path = checking_piece_data
    can_block = False
    for path_square in checking_path:
        path_coords = (path_square.row_idx, path_square.col_idx)
        for player_piece, player_piece_coords in player_piece_mapping:
            # TODO: duplicate logic with piece.has_valid_move. Might be able to
            # move this logic into the piece classes
            try:
                board.move_piece(player_piece_coords, path_coords, player_piece.color)
                checking_pieces = get_checking_pieces(board, player_piece.color)
                board.undo_move()
                if len(checking_pieces) == 0:
                    can_block = True
                    break
            except InvalidMoveException:
                continue
        if can_block:
            break
    return can_block

def player_is_checkmated(board, active_player_color, checking_pieces):
    """Does what it sounds like, a.k.a. returns whether or not the player is checkmated.

    This should only after it's confirmed that the player is in check.
    """
    white_mapping, black_mapping = board.get_active_pieces()
    player_piece_mapping = white_mapping if active_player_color is ChessColor.WHITE else black_mapping

    king, (king_row_idx, king_col_idx) = player_piece_mapping[0]
    king_square = board.squares[king_row_idx][king_col_idx]
    if king.has_valid_move(king_square, board):
        return False
    if len(checking_pieces) > 1:
        # more than one checking piece, and king can't move to get out of check. Checkmate
        return True
    # only 1 checking piece. Might be able to block/capture it
    return not can_block_checking_piece(checking_pieces[0], board, player_piece_mapping)

def player_is_stalemated(board, active_player_color):
    """Does what it sounds like, a.k.a. returns whether or not the game has reached a stalemate.

    This should only after it's confirmed that the player is not in check.
    """
    white_mapping, black_mapping = board.get_active_pieces()
    player_piece_mapping = white_mapping if active_player_color is ChessColor.WHITE else black_mapping

    player_has_move = False
    for piece, _ in player_piece_mapping:
        if piece.has_valid_move():
            player_has_move = True
            break
    return not player_has_move

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
