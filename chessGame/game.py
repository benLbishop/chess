"""module containing the Game class."""
from .board import Board, StandardBoard
from .player import Player
from .enums import ChessColor
from .custom_exceptions import PiecePlacementException, InvalidMoveException
from . import constants, conversion
from .move_logic import pathing

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
            raise err
        except ValueError as err:
            raise err

        white_pieces, black_pieces = separate_pieces(piece_list)
        self.white_player.active_pieces = white_pieces
        self.black_player.active_pieces = black_pieces

    def _validate_initial_game_state(self):
        # both players have exactly 1 king (maybe at least 1 in the future)
        # neither player is starting in checkmate/stalemate
        # TODO: test
        pass

    
    def _move_piece(self, start_square, end_square):
        """tries to move a piece from start_square to end_square."""
        if self.is_white_turn:
            cur_player = self.white_player
            cur_opponent = self.black_player
        else:
            cur_player = self.black_player
            cur_opponent = self.white_player
        try:
            move_path = pathing.get_move_path(start_square, end_square, self.board, cur_player)
        except InvalidMoveException as err:
            raise err
        # TODO
        # simulate moving piece, see if player put themselves in check, raise if so
        # update pieces, perform captures (update piece.has_moved)
        # log move w/ notation


    def make_move(self, start_square, end_square):
        """Given the user's input, tries to move a piece to a new square."""
        try:
            self._move_piece(start_square, end_square)
        except InvalidMoveException as err:
            raise err
        # see if opponent is now in check/checkmate/stalemate
        # switch turns

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

    sorted_white = sorted(white_pieces, key=lambda piece: piece.name.value)
    sorted_black = sorted(black_pieces, key=lambda piece: piece.name.value)
    return (sorted_white, sorted_black)
