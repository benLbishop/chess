"""module for the Piece class."""
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.move_logic import pathing
from chessGame import constants
class Piece:
    """Class representing a chess piece."""
    def __init__(self, color):
        self.color = color
        self._value = constants.PIECE_VALUES.get(type(self).__name__, -1) # TODO: test for subclasses
        self.has_moved = False # TODO: works for initial game state, but what about endgames?

    def __str__(self):
        # TODO: format color to be readable
        return "{} {}".format(self.color, type(self).__name__)

    def __eq__(self, other):
        return (self._value, self.color) == (other._value, other.color)

    def __lt__(self, other):
        return (self._value, self.color) < (other._value, other.color)

    def __le__(self, other):
        return (self._value, self.color) <= (other._value, other.color)

    def can_reach_square(self, start, end):
        """Abstract method for validating if a piece can move from one square to another.
            Must be implemented by subclasses.
        """
        raise NotImplementedError

    def get_path_to_square(self, start, end, board):
        """Attempts to get the path for standard pieces (bishops, rooks, and queens).
        Raises an InvalidMoveException if the move is illegal for some reason.
        """
        # get the movement necessary to reach destination
        move_type = pathing.get_necessary_move_type(start, end)

        cur_square = start
        path = []
        while cur_square is not end:
            next_row_idx, next_col_idx = pathing.get_next_square_indexes(cur_square, move_type)
            cur_square = board.squares[next_row_idx][next_col_idx]
            path.append(cur_square)
            if cur_square.is_occupied():
                break
        if cur_square is not end:
            # reached a block on the path. raise
            raise InvalidMoveException('destination not reachable due to block')
        # on end square. Check to see if occupied
        if cur_square.is_occupied():
            # raise if moving piece color is same as end square piece color
            if cur_square.piece.color is self.color:
                raise InvalidMoveException('cannot move into square occupied by player piece')
        # found a valid path
        return path
