"""module containing the Game class."""
from .board import Board, StandardBoard
from .player import Player
from .enums import ChessColor
from .custom_exceptions import PiecePlacementException
from . import constants, conversion

class Game:
    """class representing an instance of a game of chess."""

    def __init__(self, board_config, white_player_config, black_player_config, piece_strings):
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
        if len(piece_strings) == 0:
            piece_strings = constants.STD_PIECE_STRINGS

        try:
            piece_list = conversion.convert_strings_to_pieces(piece_strings)
            self.board.populate(piece_list)
        except PiecePlacementException as err:
            pass
        except ValueError as err:
            pass

        white_pieces, black_pieces = separate_pieces(piece_list)
        self.white_player.active_pieces = white_pieces
        self.black_player.active_pieces = black_pieces

    def _validate_initial_game_state(self):
        # both players have exactly 1 king (maybe at least 1 in the future)
        # neither player is starting in checkmate/stalemate
        pass

    def attempt_move(self, start_square, end_square):
        """Given the user's input, tries to move a piece to a new square."""

# TODO: move
def separate_pieces(piece_list):
    """takes a list of pieces of mixed color and separates them into white and black.

    Describing colors in chess should never be taken out of context.
    """
    white_pieces, black_pieces = [], []
    for piece in piece_list:
        if piece.color == ChessColor.WHITE:
            white_pieces.append(piece)
        else:
            black_pieces.append(piece)

    return (white_pieces, black_pieces)
