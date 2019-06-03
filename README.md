# nine-board-tic-tac-toe
http://www.cse.unsw.edu.au/~cs3411/19t1/hw3/

### Introduction
In this project you will be writing an agent to play the game of Nine-Board Tic-Tac-Toe.
This game is played on a 3 x 3 array of 3 x 3 Tic-Tac-Toe boards. The first move is made by placing an X in a randomly chosen cell of a randomly chosen board. After that, the two players take turns placing an O or X alternately into an empty cell of the board corresponding to the cell of the previous move. (For example, if the previous move was into the upper right corner of a board, the next move must be made into the upper right board.)

The game is won by getting three-in-a row either horizontally, vertically or diagonally in one of the nine boards. If a player is unable to make their move (because the relevant board is already full) the game ends in a draw.

### Getting Started
Original files are in src folder.

    cd src
    make all    
In the terminal, type

    ./servt -x -o
You should then see something like this:  
 
    . . . | . . . | . . .  
    . . . | . . . | . . .  
    . . . | . . . | . . .  
    ------+-------+------  
    . . . | . . . | . . .  
    . . . | . . . | . . .  
    . . . | . . x | . . .   
    ------+-------+------  
    . . . | . . . | . . .  
    . . . | . . . | . . .  
    . . . | . . . | . . .  

    next move for O ?  

You can now play Nine-Board Tic-Tac-Toe against yourself, by typing a number for each move. 
The cells in each board are numbered 1, 2, 3, 4, 5, 6, 7, 8, 9 as follows:

    +-----+
    |1 2 3|
    |4 5 6|
    |7 8 9|
    +-----+
To play against a computer player, you need to open another terminal window (and cd to the src directory).

Type this into the first window:

    ./servt -p 12345 -x
This tells the server to use port 12345 for communication, and that the moves for X will be chosen by you, the human, typing at the keyboard. (If port 12345 is busy, choose another 5-digit number.)
You should then type this into the second window (using the same port number):

    ./randt -p 12345
The program `randt` simply chooses each move randomly among the available legal moves.
You can play against a slightly more sophisticated player by typing this into the second window:

    ./lookt -p 12345
(If you are using a Mac, type ./lookt.mac instead of ./lookt)
To play two computer programs against each other, you may need to open three windows. For example, to play agent against `lookt` using port 54321, type as follows:

    window 1:	./servt -p 54321
    window 2:	./agent.py -p 54321
    window 3:	./lookt -p 54321
(Whichever program connects first will play X; the other program will play O.)
Alternatively, you can launch all three programs from a single window by typing

    ./servt -p 54321 &
    ./agent.py -p 54321 &
    ./lookt -p 54321
or, using a shell script:

    ./playpy.sh lookt 54321
The strength of `lookt` can be adjusted by specifying a maximum search depth (default value is 9; reasonable range is 1 to 18), e.g.

    ./lookt -p 12345 -d 6
or

    ./playpy.sh "lookt -d 16" 54321

### How it works
Each tic-tac-toe board is represented by an array, while the nine board tic-tac-toe is represented by a 2d-array consisting of 9 tic-tac-toe boards.

The minimax tree is represented by a Tree class containing a copy of the full board, the current board we are in, the current move/next board to play in, the heuristic value of the board and a list of children

The minimax tree is built using a recursive function that initially gets a list of possible moves available to the current board and creates a list of children for the current board and keeps track of what the next board should be.

For each of our AI's turn, we generate a new tree with the current board state as the root node. Once we have the minimax tree, we use alpha beta pruning to speed up the computation.

The search depth varies as the game progresses. It will start at depth 3, slowly incrementing to depths 4, 5 and 6.

The heuristic function is defined as the probability that player wins - probability opponent wins for each board. For each consecutive X's without any O's in any row/column/diagonal, X's score increases depending on how many X's are in that row/column/diag.  
Eg: in board 1, if a row/column/diagonal has only one X and no O, then Pr(X wins) += 1. But if there's two X, then Pr(X wins) += 10, and Pr(X wins) += 100 if three X as we want the agent to either move towards that board or completely avoid it if it is the opponent's score. We then sum up the probability for each of the boards.

### To-do
1. Use python dictionaries to store heuristic values of each node at the start of the game.
2. Think of better heuristic, current one is kinda simplistic.
