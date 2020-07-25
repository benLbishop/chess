"""Module for the playing chess using the command line."""
import sys
import os

# hack in the path to get access to sibling chess_game TODO: yucky
sys.path.insert(0, os.path.abspath('./'))

from chess_game.game import Game
from chess_game.player import Player
from chess_game.enums import ChessColor
from chess_game.conversion import parse_piece_location_string, parse_piece_type_char
from chess_game.custom_exceptions import PawnPromotionException

def test_input():
    white = Player({'name': 'John', 'color': ChessColor.WHITE})
    black = Player({'name': 'Bob', 'color': ChessColor.BLACK})
    piece_strings = ['w Kf7', 'b Kh8', 'w Qg1']
    game = Game(white, black, piece_strings)
    print(game.board)

    while True:
        cur_color = 'White' if game.is_white_turn else 'Black'
        print("{0}'s turn to move: ".format(cur_color))

        start_coords = None
        end_coords = None
        try:
            start_str = input('piece location: ')
            start_coords = parse_piece_location_string(start_str)
            end_str = input('piece destination: ')
            end_coords = parse_piece_location_string(end_str)
        except ValueError as err:
            print('ERROR: ' + str(err))
            continue
        except KeyboardInterrupt:
            print('\nGame stopped.')
            break
        try:
            game.make_move(start_coords, end_coords)
        except PawnPromotionException:
            piece_str = input('Promote pawn to which piece? ')
            piece_class = parse_piece_type_char(piece_str)
            game.promote_pawn(end_coords, piece_class)
        except Exception as bleh:
            print(bleh)
            continue

        if game.is_complete:
            print('{0} won!!'.format(cur_color))
            break

        print(game.board)


if __name__ == "__main__":
    test_input()
