# ChessMinimax
A Chess-playing program using the Minimax algorithm and alpha-beta pruning, where the program plays against the user. It has a complete graphical interface that uses Tkinter. It is quite slow though.

Chess.py is the first version of the program, which uses Python matrixes to represent the chess board. Chess_improved uses strings instead, which speeds up the program by 30-40%. It can even be built using Nuitka for another speedup.

The graphical interface is inspired from the one used on lichess.com.

The evaluation function used by the Minimax algorithm is based on 3 things :
- the value of the player pieces(pawn=1.0, knight=3.2, bishop=3.33, rook=5.1, queen=8.8)
- the mobility of the pieces
- the structure of the pawns

The coefficients used to evaluate the board from those 3 things are in coeffs.txt.

Of course, if the program can checkmate its opponent it does and if it's about to get checkmated it tries everything to avoid that.
