"""Module for processing input to load the board."""
# TODO: rename this module
from chessGame.conversion import parse_std_notation_string
from chessGame.piece import Piece

def std_strings_to_piece_mapping(string_list):
    """Takes in a list of strings in standard chess notation
        And converts them to a mapping from pieces to their board coordinates.
        Return type is a tuple of the form (Piece, (row_idx, col_idx))
    """
    def map_std_notation_str(s):
        """function used to map the standard notation string."""
        piece_params, coordinates = parse_std_notation_string(s)
        return Piece(*piece_params), coordinates

    return list(map(map_std_notation_str, string_list))
