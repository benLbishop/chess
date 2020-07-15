import unittest
from chess_game.enums import ChessColor
from chess_game.board import StandardBoard
from chess_game.pieces.king import King
from chess_game.pieces.rook import Rook
from chess_game.pieces.pawn import Pawn
from chess_game.move import Move
from chess_game.conversion import parse_std_notation_string as psns
from chess_game.player import Player
from chess_game.game import Game
from tests import board_lists, test_game

def main():
    # unittest.main(module=test_game)
    pawn_promotion_test()

def pawn_promotion_test():
    white_config = {'color': ChessColor.WHITE, 'name': 'Griffin'}
    white_player = Player(white_config)
    black_config = {'color': ChessColor.BLACK, 'name': 'Justin'}
    black_player = Player(black_config)
    piece_strings = ['w Kd2', 'w a7', 'b Kd7', 'b a2']
    g = Game(white_player, black_player, piece_strings)
    print(g.board)
    g.make_move((6, 0), (7, 0))
    g.make_move((1, 0), (0, 0))
    print(g.board)

def en_passant_test():
    b = StandardBoard()
    wp = Pawn(ChessColor.WHITE)
    bp = Pawn(ChessColor.BLACK)
    b.squares[4][2].piece = wp
    b.squares[4][3].piece = bp
    b.move_history = [Move(b.squares[6][3], b.squares[4][3])]
    print(b)
    b.move_piece((4, 2), (5, 3), ChessColor.WHITE)
    print(b)

def castle_test():
    b = StandardBoard()
    k = King(ChessColor.WHITE)
    lr = Rook(ChessColor.WHITE)
    rr = Rook(ChessColor.WHITE)
    b.squares[0][0].piece = lr
    b.squares[0][7].piece = rr
    b.squares[0][4].piece = k
    print(b)
    print('Castling...')
    b.move_piece((0, 4), (0, 6), ChessColor.WHITE)
    print(b)
    print('Undoing castling...')
    b.undo_move()
    print(b)

def check_tests():
    board = StandardBoard()
    for test_board in board_lists.checkmate_list:
        piece_strings, mated_color = test_board
        config = {'color': mated_color, 'name': 'Griffin'}
        player = Player(config)
        piece_mapping = [psns(s) for s in piece_strings]
        board.populate(piece_mapping)

        res = player.is_checkmated(board)
        assert res is True
        board.clear()
    print('all checkmates passed')


if __name__ == "__main__":
    main()
