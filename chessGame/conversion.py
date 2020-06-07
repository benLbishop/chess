"""module for converting string representations of pieces/games to useable objects."""
from .enums import ChessColor, PieceType
from .piece import Piece

def parse_piece_color_string(color_str):
    color_str = color_str.lower().strip()
    if color_str == 'w':
        return ChessColor.WHITE
    elif color_str == 'b':
        return ChessColor.BLACK
    raise ValueError('color string not recognized.')

def parse_piece_type_char(type_char):
    type_char = type_char.lower()
    if type_char == 'k':
        return PieceType.KING
    if type_char == 'q':
        return PieceType.QUEEN
    if type_char == 'r':
        return PieceType.ROOK
    if type_char == 'b':
        return PieceType.BISHOP
    if type_char == 'n':
        return PieceType.KNIGHT
    raise ValueError('invalid piece type character')

def parse_rank_char(rank_char):
    min_rank_val = ord('a')
    rank_val = ord(rank_char)
    val_diff = rank_val - min_rank_val
    if val_diff >= 8: #TODO: don't hardcode
        raise ValueError('invalid rank provided for piece, not in range')
    return val_diff


def parse_file_char(file_char):
    """Takes in a character and returns the 0-indexed file for the piece.
        This expects to take in a string of length one representing a 1-indexed file.
    """
    if not file_char.isdigit():
        raise ValueError('invalid file provided for piece, not an integer')
    readable_file = int(file_char, 10)
    # readable file is 1-indexed, we want 0-indexed
    actual_file = readable_file - 1
    if actual_file >= 8: # TODO: don't hardcode
        raise ValueError('invalid file provided for piece, not in range')
    return actual_file

# TODO: rename
def parse_piece_location_string(loc_str):
    loc_str = loc_str.strip()
    if len(loc_str) < 2:
        raise ValueError('piece location too short.')

    chars = [char for char in loc_str]
    try:
        if len(chars) == 2:
            # pawn, should only be constructing location
            piece_type = PieceType.PAWN
            rank = parse_rank_char(chars[0])
            actual_file = parse_file_char(chars[1])
        else:
            piece_type = parse_piece_type_char(chars[0])
            rank = parse_rank_char(chars[1])
            actual_file = parse_file_char(chars[2])
    except ValueError as err:
        raise err

    return (piece_type, rank, actual_file)
    

def parse_piece_string(piece_str):
    """attempts to parse a string into a Piece.

    Raises a ValueError if anything cannot be parsed.
    """
    split = " ".join(piece_str.split()).split()
    if len(split) < 2:
        raise ValueError('too few fields to define piece.')
    
    color_str = split[0]
    loc_str = split[1]
    try:
        color = parse_piece_color_string(color_str)
        piece_type, rank, actual_file = parse_piece_location_string(loc_str)
    except ValueError as err:
        raise err

    return Piece(piece_type, color, rank, actual_file)
    

def convert_strings_to_pieces(strings):
    try:
        piece_list = [parse_piece_string(piece_str) for piece_str in strings]
        return piece_list
    except ValueError as err:
        raise err
