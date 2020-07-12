"""module containing constants for the application."""
# Game Configuration
STD_BOARD_WIDTH = 8
STD_BOARD_HEIGHT = 8
STD_BOARD_CONFIG = {'num_rows': STD_BOARD_WIDTH, 'num_cols': STD_BOARD_HEIGHT}
MIN_BOARD_ROWS = 2
MIN_BOARD_COLS = 2

# Move options
STRAIGHT_OFFSETS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]
DIAGONAL_OFFSETS = [
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
]
KNIGHT_OFFSETS = [
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2)
]
PIECE_OFFSETS = {
    'King': STRAIGHT_OFFSETS + DIAGONAL_OFFSETS,
    'Queen': STRAIGHT_OFFSETS + DIAGONAL_OFFSETS,
    'Rook': STRAIGHT_OFFSETS,
    'Bishop': DIAGONAL_OFFSETS,
    'Knight': KNIGHT_OFFSETS
}

PIECE_VALUES = {
    'King': 5,
    'Queen': 4,
    'Rook': 3,
    'Bishop': 2,
    'Knight': 1,
    'Pawn': 0
}

PIECE_CHARS = {
    'King': 'K',
    'Queen': 'Q',
    'Rook': 'R',
    'Bishop': 'B',
    'Knight': 'N',
    'Pawn': 'p'
}

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