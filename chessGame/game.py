"""module containing the Game class."""
from .board import Board, StandardBoard
from .custom_exceptions import PiecePlacementException, InvalidMoveException
from . import constants, conversion
from .pieces.king import King

class Game:
    """class representing an instance of a game of chess."""

    def __init__(
            self,
            white_player,
            black_player,
            board_config=None,
            piece_strings=None
        ):
        self.white_player = white_player
        self.black_player = black_player

        self.board = Board(board_config) if board_config is not None else StandardBoard()
        self._set_up_pieces(piece_strings)

        self._validate_initial_game_state()

        self.is_complete = False
        self.is_white_turn = True

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
        white_mapping, black_mapping = self.board.get_active_pieces()
        mapping_pairs = [
            (self.white_player, white_mapping),
            (self.black_player, black_mapping)
        ]
        for player, mapping in mapping_pairs:
            color_str = player.color.name
            if not mapping:
                raise PiecePlacementException('no {} pieces on board.'.format(color_str))
            expected_king = mapping[0][0]
            if not isinstance(expected_king, King):
                raise PiecePlacementException('no {} king on board.'.format(color_str))
            if len(mapping) > 1:
                # check if more than 1 king
                second_piece = mapping[1][0]
                if isinstance(second_piece, King):
                    raise PiecePlacementException('more than 1 {} king on board.'.format(color_str))

            # check if player is starting in checkmate/stalemate
            if player.is_checkmated(self.board):
                raise PiecePlacementException('{} player starting in checkmate.'.format(color_str))

            if player.is_stalemated(self.board):
                raise PiecePlacementException('{} player starting in stalemate.'.format(color_str))

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

        # switch turns
        self.is_white_turn = not self.is_white_turn

        # check to see if end state was reached
        self._check_for_end_of_game()

    def _check_for_end_of_game(self):
        """checks to see if the game has been completed (i.e. reached a checkmate or stalemate)"""
        cur_player = self.white_player if self.is_white_turn else self.black_player
        checking_pieces = self.board.get_checking_pieces(cur_player.color)
        if len(checking_pieces) > 0:
            # check for checkmate
            if cur_player.is_checkmated(self.board):
                self.is_complete = True
        # check for stalemate
        elif cur_player.is_stalemated(self.board):
            self.is_complete = True
