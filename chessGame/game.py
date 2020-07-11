"""module containing the Game class."""
from .board import Board, StandardBoard
from .player import Player
from .enums import ChessColor
from .custom_exceptions import PiecePlacementException, InvalidMoveException
from . import constants, conversion
from .move_logic import game_state

class Game:
    """class representing an instance of a game of chess."""

    def __init__(self, board_config, white_player_config, black_player_config, piece_strings = None):
        white_player_config['color'] = ChessColor.WHITE
        self.white_player = Player(white_player_config)

        black_player_config['color'] = ChessColor.BLACK
        self.black_player = Player(black_player_config)

        self.board = Board(board_config) if board_config is not None else StandardBoard()
        self._set_up_pieces(piece_strings)

        self.is_complete = False
        self.is_white_turn = True # TODO: eventually, this should be configurable

    def _set_up_pieces(self, piece_strings):
        """takes a list of strings, attempts to convert them to pieces,
            and places the pieces in the necessary structures.
        """
        if piece_strings is None:
            piece_strings = constants.STD_PIECE_STRINGS

        try:
            piece_mapping = [conversion.parse_std_notation_string(s) for s in piece_strings]
            self.board.populate(piece_mapping)
        except PiecePlacementException as err:
            raise err
        except ValueError as err:
            raise err

    def _validate_initial_game_state(self):
        # both players have exactly 1 king (maybe at least 1 in the future)
        # neither player is starting in checkmate/stalemate
        # TODO
        pass

    def make_move(self, start_coords, end_coords):
        """Given the user's input, tries to move a piece to a new square."""
        cur_player = self.white_player if self.is_white_turn else self.black_player
        # move piece
        try:
            move_path, captured_piece = self.board.move_piece(start_coords, end_coords, cur_player.color)
        except InvalidMoveException as err:
            raise err

        # see if player put themselves in check
        checking_pieces = game_state.get_checking_pieces(self.board, cur_player.color)
        if len(checking_pieces) > 0:
            # cur_player put themselves in check, not allowed. Reset moved pieces
            self.board.undo_move()
            raise InvalidMoveException('player tried to put themselves in check')

        # update captured piece list if move was successful
        if captured_piece is not None:
            cur_player.captured_pieces.append(captured_piece)
            
        # TODO: log move w/ notation

        # switch turns
        self.is_white_turn = not self.is_white_turn

        self.check_for_end_of_game()

    def check_for_end_of_game(self):
        """checks to see if the game has been completed (i.e. reached a checkmate or stalemate)"""
        cur_player = self.white_player if self.is_white_turn else self.black_player
        checking_pieces = game_state.get_checking_pieces(self.board, cur_player.color)
        if len(checking_pieces) > 0:
            # check for checkmate
            is_checkmate = game_state.player_is_checkmated(self.board, cur_player.color, checking_pieces)
            if is_checkmate:
                self.is_complete = True
                # TODO: end game somehow
        else:
            # check for stalemate.
            # TODO: do I need to do this every time?
            is_stalemate = game_state.player_is_stalemated(self.board, cur_player.color)
            if is_stalemate:
                self.is_complete = True
                # TODO: end game somehow
