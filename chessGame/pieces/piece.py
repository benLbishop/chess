"""module for the Piece class."""
from chessGame.custom_exceptions import InvalidMoveException
from chessGame.move_logic import pathing, game_state
from chessGame import constants
class Piece:
    """Abstract class representing a chess piece."""
    def __init__(self, color):
        self.color = color
        # TODO: works for initial game state, but what about endgames?
        self.move_count = 0
        # TODO: test this way of setting data for subclasses
        class_name = type(self).__name__
        self.char = constants.PIECE_CHARS.get(class_name, '?')
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

    @property
    def has_moved(self):
        """Property determining whether or not a piece has moved."""
        return self.move_count > 0

    def can_reach_squares(self, cur_coords, target_list, board):
        """Checks to see if the piece can reach any of the squares in target_list
            (target_list is actually a list of coordinates for squares.)
        """
        has_move = False
        for target_coords in target_list:
            try:
                board.move_piece(cur_coords, target_coords, self.color)
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


    def has_valid_move(self, cur_square, board):
        """Checks to see if the piece has any valid moves to neighboring squares."""
        cur_coords = (cur_square.row_idx, cur_square.col_idx)
        neighbor_list = [tuple(map(sum, zip(cur_coords, offset))) for offset in self._offsets]
        return self.can_reach_squares(cur_coords, neighbor_list, board)

    # TODO: rename
    def can_reach_square(self, start, end):
        """Abstract method for validating if a piece can move from one square to another.
            Must be implemented by subclasses.
        """
        raise NotImplementedError

    def get_path_to_square(self, start, end, board):
        """Attempts to get the path for standard pieces (bishops, rooks, and queens).
        Raises an InvalidMoveException if the move is illegal for some reason.
        """
        # check if we can reach destination given the piece's moveset
        if not self.can_reach_square(start, end):
            raise InvalidMoveException('destination not reachable with piece')
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

    def get_move_params(self, start_coords, end_coords, board):
        """Attempts to get the move parameters using the piece for the provided coordinates."""
        # NOTE: Move not returned because importing the Move class would cause a circular import.
        start_row, start_col = start_coords
        end_row, end_col = end_coords
        start = board.squares[start_row][start_col]
        end = board.squares[end_row][end_col]
        try:
            self.get_path_to_square(start, end, board)
        except InvalidMoveException as err:
            raise err
        captured_piece, captured_piece_coords = (None, None)
        if end.is_occupied():
            captured_piece = end.piece
            captured_piece_coords = (end.row_idx, end.col_idx)
        return (start_coords, end_coords, captured_piece, captured_piece_coords)
