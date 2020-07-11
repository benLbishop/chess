"""module for converting string representations of pieces/games to useable objects."""
from .enums import ChessColor
from .pieces import (
    king,
    queen,
    rook,
    bishop,
    knight,
    pawn
)

def parse_piece_color_char(char):
    """Converts a char to a ChessColor."""
    char = char.lower().strip()
    if char == 'w':
        return ChessColor.WHITE
    if char == 'b':
        return ChessColor.BLACK
    raise ValueError('color string not recognized.')

def parse_piece_type_char(char):
    """Converts a char to its corresponding piece class."""
    char = char.lower()
    if char == 'k':
        return king.King
    if char == 'q':
        return queen.Queen
    if char == 'r':
        return rook.Rook
    if char == 'b':
        return bishop.Bishop
    if char == 'n':
        return knight.Knight
    raise ValueError('invalid piece type character')

def parse_rank_char(rank_char):
    """Takes in a character and returns the 0-indexed rank for the piece.
        This expects to take in a string of length one representing a 1-indexed rank
        (normally a char in the range 1-8).
    """
    min_rank_val = ord('a')
    rank_val = ord(rank_char)
    val_diff = rank_val - min_rank_val
    if val_diff >= 8: #TODO: don't hardcode
        raise ValueError('invalid rank provided for piece, not in range')
    return val_diff


def parse_file_char(file_char):
    """Takes in a character and returns the 0-indexed file for the piece.
        This expects to take in a string of length one representing a 1-indexed file
        (normally a char in the range a-h).
    """
    if not file_char.isdigit():
        raise ValueError('invalid file provided for piece, not an integer')
    readable_file = int(file_char, 10)
    # readable file is 1-indexed, we want 0-indexed
    actual_file = readable_file - 1
    if actual_file >= 8: # TODO: don't hardcode
        raise ValueError('invalid file provided for piece, not in range')
    return actual_file

def parse_piece_location_string(loc_str):
    """attempts to take the std. notation location and convert it to row, column coordinates."""
    loc_str = loc_str.strip()
    if len(loc_str) < 2:
        raise ValueError('piece location too short.')

    try:
        rank = parse_rank_char(loc_str[0])
        actual_file = parse_file_char(loc_str[1])
        return (rank, actual_file)
    except ValueError as err:
        raise err

def parse_std_notation_string(piece_str):
    """attempts to parse a string into a Piece.

    Raises a ValueError if anything cannot be parsed.
    """
    split = " ".join(piece_str.split()).split()
    if len(split) < 2:
        raise ValueError('too few fields to define piece.')

    color_str = split[0]
    loc_str = split[1]
    if len(color_str) == 0:
        raise ValueError('color string too short.')
    if len(loc_str) == 0:
        raise ValueError('type/location string too short.')
    try:
        color = parse_piece_color_char(color_str)
        piece_class = None
        coordinate = None
        if len(loc_str) == 2:
            # trying to parse pawn.
            piece_class = pawn.Pawn
            coordinate = parse_piece_location_string(loc_str)
        else:
            piece_class = parse_piece_type_char(loc_str[0])
            coordinate = parse_piece_location_string(loc_str[1:])
        return piece_class(color), coordinate
    except ValueError as err:
        raise err

def parse_piece_string(piece_str):
    """attempts to parse a string into a Piece.

    Raises a ValueError if anything cannot be parsed.
    """
    piece_str = piece_str.lower().strip()
    if len(piece_str) == 0:
        raise ValueError('too few fields to define piece.')

    try:
        color = parse_piece_color_char(piece_str[0])
        piece_class = None
        if len(piece_str) == 1:
            piece_class = pawn.Pawn
        else:
            piece_class = parse_piece_type_char(piece_str[-1])
        return piece_class(color)
    except ValueError as err:
        raise err
