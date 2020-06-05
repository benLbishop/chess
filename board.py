"""module containing the Board class."""
from chessColor import ChessColor
from square import Square

class Board:
    """class representing a chess board of any size."""
    def __init__(self, width, height):
        self.NUM_ROWS = width
        self.NUM_COLS = height
        self._create_squares()

    def _create_squares(self):
        init_squares = []
        for row_idx in range(self.NUM_ROWS):
            square_row = []
            for col_idx in range(self.NUM_COLS):
                cur_color = ChessColor.BLACK if (row_idx + col_idx) % 2 == 0 else ChessColor.WHITE
                cur_square = Square(cur_color, row_idx, col_idx)
                square_row.append(cur_square)

            init_squares.append(square_row)

        self.squares = init_squares

    def clear(self):
        """empties all squares on the board."""
        for row in self.squares:
            for square in row:
                square.piece = None

    def populate(self):
        pass
