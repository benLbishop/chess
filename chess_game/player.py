"""module containing the Player class."""
from .enums import ChessColor

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
        for piece, cur_square in player_mapping:
            if piece.has_valid_move(cur_square, board):
                player_has_move = True
                break
        return not player_has_move

    @staticmethod
    def can_block_checking_piece(checking_path, board, player_piece_mapping):
        """Checks if any of the pieces provided in player_piece_mapping
            can capture or block the given checking piece.
        """
        # probably don't need to check the last square in path because it's king square
        path_coords = [square.coords for square in checking_path]
        can_block = False
        for piece, square in player_piece_mapping:
            if piece.has_valid_move_in_list(square.coords, path_coords, board):
                can_block = True
                break
        return can_block

    def is_checkmated(self, board):
        """Does what it sounds like, a.k.a. returns whether or not the player is checkmated.
        """
        checking_pieces = board.get_checking_pieces(self.color)
        if len(checking_pieces) == 0:
            return False
        white_mapping, black_mapping = board.get_active_pieces()
        player_mapping = white_mapping if self.color is ChessColor.WHITE else black_mapping

        king, king_square = player_mapping[0]
        if king.has_valid_move(king_square, board):
            return False
        if len(checking_pieces) > 1:
            # more than one checking piece, and king can't move to get out of check. Checkmate
            return True
        # only 1 checking piece. Might be able to block/capture it
        checking_path = checking_pieces[0].path
        # Already check player's king, so just check remaining pieces
        other_player_pieces = player_mapping[1:]
        return not self.can_block_checking_piece(checking_path, board, other_player_pieces)
