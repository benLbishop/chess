"""module for the Piece class."""
from chessGame.custom_exceptions import InvalidMoveException
from chessGame import constants
class Piece:
    """Abstract class representing a chess piece."""
    def __init__(self, color):
        self.color = color
        self.move_count = 0
        # TODO: test this way of setting data for subclasses
        class_name = type(self).__name__
        self.char = constants.PIECE_CHARS.get(class_name, '?')
        self._value = constants.PIECE_VALUES.get(class_name, -1)
        self._offsets = constants.PIECE_OFFSETS.get(class_name, [])

    def __str__(self):
        return "{} {}".format(self.color.name.capitalize(), type(self).__name__)

    def __eq__(self, other):
        return (self._value, self.color) == (other._value, other.color)

    def __lt__(self, other):
        return (self._value, self.color) < (other._value, other.color)

    def __le__(self, other):
        return (self._value, self.color) <= (other._value, other.color)

    @property
    def has_moved(self):
        """Property determining whether or not a piece has moved."""
        return self.move_count > 0

    def has_valid_move_in_list(self, cur_coords, target_list, board):
        """Checks to see if the piece can reach any of the squares in target_list
            (target_list is a list of coordinates for squares.)
        """
        has_move = False
        for target_coords in target_list:
            try:
                board.move_piece(cur_coords, target_coords, self.color)
                board.undo_move()
                has_move = True
                break
            except InvalidMoveException:
                continue
            except ValueError:
                continue
        return has_move


    def has_valid_move(self, cur_square, board):
        """Checks to see if the piece has any valid moves to neighboring squares."""
        coords = cur_square.coords
        neighbor_list = [tuple(map(sum, zip(coords, offset))) for offset in self._offsets]
        return self.has_valid_move_in_list(coords, neighbor_list, board)

    def can_reach_square(self, start, end):
        """Abstract method for validating if a piece can move from one square to another.
            Must be implemented by subclasses.
        """
        raise NotImplementedError

    @staticmethod
    def _get_necessary_offset(start_square, end_square):
        """Returns the offset required to properly get to end_square from start_square.
            Assumes that movement from start_square to end_square is possible in a legal chess move.

            Returns a boolean.
        """
        row_diff = end_square.row_idx - start_square.row_idx
        col_diff = end_square.col_idx - start_square.col_idx
        if col_diff == 0:
            return (1, 0) if row_diff > 0 else (-1, 0)
        if row_diff == 0:
            return (0, 1) if col_diff > 0 else (0, -1)
        if row_diff > 0:
            # moved up and diagonal
            return (1, 1) if col_diff > 0 else (1, -1)
        # moved down and diagonal
        return (-1, 1) if col_diff > 0 else (-1, -1)

    def get_path_to_square(self, start, end, board):
        """Attempts to get the path for standard pieces (bishops, rooks, and queens).
        Raises an InvalidMoveException if the move is illegal for some reason.
        """
        # check if we can reach destination given the piece's moveset
        if not self.can_reach_square(start, end):
            raise InvalidMoveException('destination not reachable with piece')
        # get the movement necessary to reach destination
        offset = self._get_necessary_offset(start, end)

        cur_square = start
        path = [start]
        while cur_square is not end:
            next_row_idx, next_col_idx = tuple(map(sum, zip(cur_square.coords, offset)))
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

    def get_move_params(self, start, end, board):
        """Attempts to get the move parameters using the piece for the provided coordinates."""
        # NOTE: Move not returned because importing the Move class would cause a circular import.
        try:
            self.get_path_to_square(start, end, board)
        except InvalidMoveException as err:
            raise err
        captured_piece, captured_square = (None, None)
        if end.is_occupied():
            captured_piece = end.piece
            captured_square = end
        return (start, end, captured_piece, captured_square)
