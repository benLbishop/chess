"""module containing the Game class."""
from .board import Board, StandardBoard
from .player import Player
from .enums import ChessColor
from .custom_exceptions import PiecePlacementException, InvalidMoveException
from . import constants, conversion
from .move_logic import pathing, game_state

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
            white_pieces, black_pieces = conversion.convert_strings_to_pieces(piece_strings)
            self.board.populate(white_pieces + black_pieces)
        except PiecePlacementException as err:
            raise err
        except ValueError as err:
            raise err

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

        # update pieces
        moving_piece = start_square.piece
        captured_piece = end_square.piece # could be None
        end_square.piece = moving_piece
        moving_piece.row_idx = end_square.row_idx
        moving_piece.col_idx = end_square.col_idx
        start_square.piece = None
        # if piece was captured, update player piece lists
        if captured_piece is not None:
            cur_opponent.active_pieces.remove(captured_piece)

        # see if player put themselves in check
        checking_pieces = game_state.get_checking_pieces(self.board, cur_player, cur_opponent)
        if len(checking_pieces) > 0:
            # cur_player put themselves in check, not allowed. Reset moved pieces
            start_square.piece = moving_piece
            moving_piece.row_idx = start_square.row_idx
            moving_piece.col_idx = start_square.col_idx
            end_square.piece = captured_piece
            cur_player.captured_pieces.append(captured_piece) # TODO: resort
            raise InvalidMoveException('player tried to put themselves in check')
            

        # TODO: log move w/ notation


    def make_move(self, start_square, end_square):
        """Given the user's input, tries to move a piece to a new square."""
        try:
            self._move_piece(start_square, end_square)
        except InvalidMoveException as err:
            raise err
        # TODO: don't duplicate with _move_piece
        if self.is_white_turn:
            cur_player = self.white_player
            cur_opponent = self.black_player
        else:
            cur_player = self.black_player
            cur_opponent = self.white_player
        # see if opponent is now in check/checkmate/stalemate
        opp_check_pieces = game_state.get_checking_pieces(self.board, cur_opponent, cur_player)
        if len(opp_check_pieces) > 0:
            # check for checkmate
            is_checkmate = game_state.player_is_checkmated(self.board, cur_opponent, cur_player, opp_check_pieces)
            if is_checkmate:
                self.is_complete = True
                # TODO: end game somehow
        else:
            # check for stalemate.
            # TODO: do I need to do this every time?
            is_stalemate = game_state.player_is_stalemated(self.board, cur_opponent, cur_player)
            if is_stalemate:
                self.is_complete = True
                # TODO: end game somehow
        # game not over. switch turns
        self.is_white_turn = not self.is_white_turn
