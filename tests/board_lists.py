"""module containing board configurations for tests."""
from chess_game.enums import ChessColor

b = ChessColor.BLACK
w = ChessColor.WHITE

# list of tuples containing pieces and player in checkmate
# (piece_list, color_in_checkmate)
checkmate_list = [
    (['w Qe7', 'w Nd5', 'b Ke8'], b),
    (['w Kg1', 'b Qg2', 'b Bd5'], w),
    (['w Qf8', 'b Kh8', 'b h7'], b)
]
