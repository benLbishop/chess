"""module containing the Game class."""
from .board import Board, StandardBoard
from .player import Player
from .enums import ChessColor
from .custom_exceptions import PiecePlacementException, InvalidMoveException
from . import constants, conversion
from .move_logic import game_state

class Game:
    """class representing an instance of a game of chess."""

    def __init__(
            self,
            white_player_config,
            black_player_config,
            board_config=None,
            piece_strings=None
        ):
        white_player_config['color'] = ChessColor.WHITE
        self.white_player = Player(white_player_config)

        black_player_config['color'] = ChessColor.BLACK
        self.black_player = Player(black_player_config)

        self.board = Board(board_config) if board_config is not None else StandardBoard()
        self._set_up_pieces(piece_strings)

        self.is_complete = False
        self.is_white_turn = True # TODO: If loading end game, this should be constructor param

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
        """Checks to make sure the game is starting in a valid state."""
        # both players have exactly 1 king (maybe at least 1 in the future)
        # neither player is starting in checkmate/stalemate
        # TODO

    def make_move(self, start_coords, end_coords):
        """Given the user's input, tries to move a piece to a new square."""
        cur_player = self.white_player if self.is_white_turn else self.black_player
        # move piece
        move = None
        try:
            move = self.board.move_piece(start_coords, end_coords, cur_player.color)
        except InvalidMoveException as err:
            raise err
        except ValueError as err:
            raise err

        # update captured piece list if move was successful
        if move.captured_piece is not None:
            cur_player.captured_pieces.append(move.captured_piece)

        # TODO: log move w/ notation

        self.check_for_end_of_game()

        # switch turns
        self.is_white_turn = not self.is_white_turn

    def check_for_end_of_game(self):
        """checks to see if the game has been completed (i.e. reached a checkmate or stalemate)"""
        cur_player = self.white_player if self.is_white_turn else self.black_player
        checking_pieces = game_state.get_checking_pieces(self.board, cur_player.color)
        if len(checking_pieces) > 0:
            # check for checkmate
            if game_state.player_is_checkmated(self.board, cur_player.color, checking_pieces):
                self.is_complete = True
                # TODO: end game somehow
        elif game_state.player_is_stalemated(self.board, cur_player.color):
            # check for stalemate.
            # TODO: do I need to do this every time?
            self.is_complete = True
            # TODO: end game somehow
