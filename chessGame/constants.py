"""module containing constants for the application."""
from .enums import MoveType

# Game Configuration
STD_BOARD_WIDTH = 8
STD_BOARD_HEIGHT = 8
STD_BOARD_CONFIG = {'num_rows': STD_BOARD_WIDTH, 'num_cols': STD_BOARD_HEIGHT}
MIN_BOARD_ROWS = 2
MIN_BOARD_COLS = 2

# Move options
PAWN_WHITE_MOVES = [MoveType.UP, MoveType.UP_LEFT, MoveType.UP_RIGHT]
PAWN_BLACK_MOVES = [MoveType.DOWN, MoveType.DOWN_LEFT, MoveType.DOWN_RIGHT]
BISHOP_MOVES = [MoveType.UP_LEFT, MoveType.UP_RIGHT, MoveType.DOWN_LEFT, MoveType.DOWN_RIGHT]
ROOK_MOVES = [MoveType.UP, MoveType.DOWN, MoveType.LEFT, MoveType.RIGHT]
QUEEN_MOVES = [move for move in MoveType]
KING_MOVES = [move for move in MoveType]

# board configurations
STD_PIECE_STRINGS = [
    'w a2',
    'w b2',
    'w c2',
    'w d2',
    'w e2',
    'w f2',
    'w g2',
    'w h2',
    'w Ra1',
    'w Nb1',
    'w Bc1',
    'w Qd1',
    'w Ke1',
    'w Bf1',
    'w Ng1',
    'w Rh1',
    'b a7',
    'b b7',
    'b c7',
    'b d7',
    'b e7',
    'b f7',
    'b g7',
    'b h7',
    'b Ra8',
    'b Nb8',
    'b Bc8',
    'b Qd8',
    'b Ke8',
    'b Bf8',
    'b Ng8',
    'b Rh8'
]