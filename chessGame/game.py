"""module containing the Game class."""
from .board import Board, StandardBoard
from .player import Player
from .enums import ChessColor
from .custom_exceptions import PiecePlacementException

class Game:
    """class representing an instance of a game of chess."""

    def __init__(self, board_config, white_player_config, black_player_config):
        white_player_config['color'] = ChessColor.WHITE
        self.white_player = Player(white_player_config)

        black_player_config['color'] = ChessColor.BLACK
        self.black_player = Player(black_player_config)

        self.board = Board(board_config) if board_config is not None else StandardBoard()
        # TODO: where should I get the piece list from?
        self._populate_board([])

        self.is_complete = False
        self.is_white_turn = True

    def _populate_board(self, piece_list):
        """takes a list of pieces and attempts to place them on the board.

        Raises a PiecePlacementException if the board cannot be populated.
        """
        try:
            self.board.populate(piece_list)
        except PiecePlacementException as err:
            pass

    def attempt_move(self, start_square, end_square):
        """Given the user's input, tries to move a piece to a new square."""
