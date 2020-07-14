"""module containing the Player class."""
from .enums import ChessColor
from .move_logic import game_state

class Player:
    """Class representing a user."""
    def __init__(self, player_config):
        self.color = player_config['color']
        self.name = player_config['name']
        self.captured_pieces = []

    def is_stalemated(self, board):
        """Does what it sounds like, a.k.a. returns whether or not the Player is in stalemate.
            This should only after it's confirmed that the player is not in check.
        """
        white_mapping, black_mapping = board.get_active_pieces()
        player_mapping = white_mapping if self.color is ChessColor.WHITE else black_mapping

        player_has_move = False
        for piece, (row_idx, col_idx) in player_mapping:
            cur_square = board.squares[row_idx][col_idx]
            if piece.has_valid_move(cur_square, board):
                player_has_move = True
                break
        return not player_has_move

    def is_checkmated(self, board, checking_pieces):
        """Does what it sounds like, a.k.a. returns whether or not the player is checkmated.
        """
        if len(checking_pieces) == 0:
            return False
        white_mapping, black_mapping = board.get_active_pieces()
        player_mapping = white_mapping if self.color is ChessColor.WHITE else black_mapping

        king, (king_row_idx, king_col_idx) = player_mapping[0]
        king_square = board.squares[king_row_idx][king_col_idx]
        if king.has_valid_move(king_square, board):
            return False
        if len(checking_pieces) > 1:
            # more than one checking piece, and king can't move to get out of check. Checkmate
            return True
        # only 1 checking piece. Might be able to block/capture it
        # TODO: shouldn't call this with player's king in piece_mapping, unecessary
        checking_path = checking_pieces[0][1]
        return not game_state.can_block_checking_piece(checking_path, board, player_mapping)
