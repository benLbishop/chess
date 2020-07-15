# Chess

## Design Decisions

I'm using this project to work on a few things: strengthening my general python knowledge, writing a program using test-driven development, and getting back into thinking about object-oriented design.

To start out, I tried to figure out how I wanted to lay out the board and the pieces. I've started out with a design of having a Board class which contains a 2D list of Square objects. These square objects store their row index and column index, as well as a Piece object (optionally).

I went with this structure because the main actions I can see happening are a user choosing to move a piece from one square to another; in the code, I can represent this as attempting to take a piece from one square object and move it to a destination square object. One alternative would be to have a mapping of pieces to locations for each player. My current thinking is this would be a good deal slower when I'm trying to validate a move. At some point, I'll need to iterate through intermediate squares (for example, if a bishop tries to move three squares, I'll need to check the first and second squares in the diagonal and make sure they're unoccupied). If the squares hold the pieces, I simply need to check the attribute of the object. If I store a mapping of pieces to locations in a dict, I'll have to search each piece to see if it's in that location. I could have a dict of locations to pieces, but that's essentially the same solution as storing the piece in the Square object.

I'm trying to think about how I want to deal with the issue of a player making a move that would resultingly put themselves in check, which is illegal. The brute force solution would be to look through the opponent's every piece and see if it would now be able to attack the king. I should only have to look at a subset of these pieces, however. With the exception of castling, only one piece is moving at a time. If the piece moving is the king, I think I'll need to check all of the opponent's pieces to see if I'm in check. If it was material, however, the only way it could now be check is if there was a piece that was blocked from attacking the king by the piece that just moved. I think I can track this state of "blocked from attacking the king by Piece p," but I'm not exactly sure how useful it would be.

Right now I'm giving pieces row_idx and col_idx attributes. I'm not sure if this will be my long term solution, since I think there's a risk of a piece getting assigned to a square, and having the square and piece's row/col indexes not line up. For loading the game and tracking where the pieces are for check tests, however, the indices are useful.

I've made a number of changes to the game, the primary one being that pieces no longer have row/column indices. Pieces belong to squares and nothing else.

TODO:
    Test all of the new things
        Go through current TODOs
        Make tester_script its own test suite
        experiment with test suites and sub tests
    Actually make game playable
        Implement ChessPlayer class

Possible Improvements:
    I have a lot of cases where I'll move a piece and then undo the move in my stalemate/checkmate functions. These actions use the actual game board; I might want to use a copy of the board and check on that, but I'm not sure about the efficiency of doing so.
    My end of game check gets the list of checking pieces, and then in my player.is_in_checkmate function, I get the checking pieces again. I could pass the checking pieces to the checkmate function, but that feels clunky.
    I check for checkmate and stalemate every turn. There are probably some cases where I can avoid doing so, but it feels risky to start trying to cut corners like that.

Endgame changes:
    Need to set player's turn
    Need to set piece's move_count
