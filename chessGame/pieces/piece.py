"""module for the Piece class."""
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.move_logic import pathing, game_state
from chessGame import constants
class Piece:
    """Abstract class representing a chess piece."""
    def __init__(self, color):
        self.color = color
        self.has_moved = False # TODO: works for initial game state, but what about endgames?
        # TODO: test this way of setting data for subclasses
        class_name = type(self).__name__
        self._value = constants.PIECE_VALUES.get(class_name, -1)
        self._offsets = constants.PIECE_OFFSETS.get(class_name, [])

    def __str__(self):
        # TODO: format color to be readable
        return "{} {}".format(self.color, type(self).__name__)

    def __eq__(self, other):
        return (self._value, self.color) == (other._value, other.color)

    def __lt__(self, other):
        return (self._value, self.color) < (other._value, other.color)

    def __le__(self, other):
        return (self._value, self.color) <= (other._value, other.color)

    def has_valid_move(self, cur_square, board):
        """Checks to see if the piece has any valid moves to neighboring squares."""
        # TODO: test
        # TODO: what about castling?
        cur_coords = (cur_square.row_idx, cur_square.col_idx)
        has_move = False
        for offset in self._offsets:
            neighbor_coords = tuple(map(sum, zip(cur_coords, offset)))
            try:
                board.move_piece(cur_coords, neighbor_coords, self.color)
                checking_pieces = game_state.get_checking_pieces(board, self.color)
                board.undo_move()
                if len(checking_pieces) == 0:
                    has_move = True
                    break
            except InvalidMoveException:
                continue
            except ValueError:
                continue
        return has_move

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
        offset = pathing.get_necessary_offset(start, end)

        cur_square = start
        path = [start]
        while cur_square is not end:
            cur_coords = (cur_square.row_idx, cur_square.col_idx)
            next_row_idx, next_col_idx = tuple(map(sum, zip(cur_coords, offset)))
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
