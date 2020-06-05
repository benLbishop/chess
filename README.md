# Chess

## Design Decisions

I'm using this project to work on a few things: strengthening my general python knowledge, writing a program using test-driven development, and getting back into thinking about object-oriented design.

To start out, I tried to figure out how I wanted to lay out the board and the pieces. I've started out with a design of having a Board class which contains a 2D list of Square objects. These square objects store their row index and column index, as well as a Piece object (optionally).

I went with this structure because the main actions I can see happening are a user choosing to move a piece from one square to another; in the code, I can represent this as attempting to take a piece from one square object and move it to a destination square object. One alternative would be to have a mapping of pieces to locations for each player. My current thinking is this would be a good deal slower when I'm trying to validate a move. At some point, I'll need to iterate through intermediate squares (for example, if a bishop tries to move three squares, I'll need to check the first and second squares in the diagonal and make sure they're unoccupied). If the squares hold the pieces, I simply need to check the attribute of the object. If I store a mapping of pieces to locations in a dict, I'll have to search each piece to see if it's in that location. I could have a dict of locations to pieces, but that's essentially the same solution as storing the piece in the Square object.