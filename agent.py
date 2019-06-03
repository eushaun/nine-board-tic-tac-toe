#!/usr/bin/python3

# Agent that plays 9 board tic-tac-toe
# by Eu Shaun Lim(z5156345) and Malay Mukesh Raghuwanshi(z5217107) 
# modified from the starter bot provided by Zac Partridge

# Each tic-tac-toe board is represented by an array, while 
# the nine board tic-tac-toe is represented by a 2d-array 
# consisting of 9 tic-tac-toe boards.

# The minimax tree is represented by a Tree class containing a copy of
# the full board, the current board we are in, the current move/next board to play in,
# the heuristic value of the board and a list of children

# The minimax tree is built using a recursive function that initially 
# gets a list of possible moves available to the current board and
# creates a list of children for the current board and keeps track of
# what the next board should be.

# For each of our AI's turn, we generate a new tree with the current board
# state as the root node. Once we have the minimax tree, we use alpha beta pruning to speed up
# the computation.

# The search depth varies as the game progresses. It will start at depth 3, slowly incrementing
# to depths 4, 5 and 6.

# The heuristic function is defined as the probability that player wins - probability opponent 
# wins for each board.
# Eg: in board 1, if a row/column/diagonal only one X and no O, then Pr(X wins) += 1.
# We then sum up the probability for each of the boards.

import socket
import sys
import numpy as np
from copy import deepcopy

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
s = [".","X","O"]
curr = 0 # this is the current board to play in

class Tree:
    def __init__(self, full_board, board_num, move, heuristic):
        self.full_board = full_board
        self.curr_board = board_num
        self.board = full_board[board_num]
        self.move = move
        self.children = []
        self.heuristic = heuristic  

    def addChildren(self, children):
        self.children.extend(children)

##########################
####  TREE FUNCTIONS  ####
##########################

def buildTree(tree, depth):
    """build a minimax tree from the current board we are in"""
    player = True

    ## get list of children of tree
    list_of_children = getChildren(tree, tree.curr_board, player)
    tree.addChildren(list_of_children)

    # print(tree.board)
    # print("Current board: ", curr)
    # for i in range(len(tree.children)):
    #     print("Children: ", tree.children[i].board)

    for child in tree.children:
        updateHeuristic(child, child.curr_board, player)
        buildTreeRecursive(child, depth, not player, curr)
    return tree

def buildTreeRecursive(tree, depth, player, curr_board):
    """recursively builds the tree"""
    if depth == 0:
        return tree
    list_of_children = getChildren(tree, tree.move, player)
    tree.addChildren(list_of_children)
    for child in tree.children:
        # update heuristic value of current board
        updateHeuristic(child, child.curr_board, player)
        # print_board(tree.children[i].full_board)
        buildTreeRecursive(child, depth-1, not player, tree.move)

def getChildren(parent, board_num, player):
    """given parent tree, return children trees from possible_moves"""
    if not(player):
        player = 2  # the opponent is 'O'
    else:
        player = 1  # we always play 'X'

    possible_moves = np.where(parent.full_board[board_num] == 0)[0]
    children = []
    for i in range(1, len(possible_moves)):
        new_board = deepcopy(parent.full_board)                 # maintain separate copy of board
        new_heuristic = deepcopy(parent.heuristic)
        new_board[board_num][possible_moves[i]] = player        # mark new move
        new_tree = Tree(new_board, board_num, possible_moves[i], new_heuristic)
        children.append(new_tree)

    return children

###############################
####  HEURISTIC FUNCTIONS  ####
###############################

def updateHeuristic(tree, board_num, me):
    """build a list of heuristic values for all 9 boards"""
    for i in range(1,10):
        tree.heuristic[i] *= -1     # flip the sign of the heuristics
    tree.heuristic[board_num] = getHeuristic(tree.full_board[board_num], me)

def sumHeuristic(tree):
    sum = 0
    for i in range(1,10):
        sum += tree.heuristic[i]
    return sum*-1

def getHeuristic(board, me):
    """calculate heuristic using probability player win - probability opponent win"""
    # initialize value
    X_win = O_win = 0

    # set of vertical, horizontal and diagonal indices of the board to check
    indices = [[1,2,3], [4,5,6], [7,8,9], [1,5,9], [3,5,7], [1,4,7], [2,5,8], [3,6,9]]
    for i in range(len(indices)):
        board_row = [board[indices[i][0]], board[indices[i][1]], board[indices[i][2]]]
        if board_row.count(1) == 1 and board_row.count(2) == 0:
            X_win += 1
        elif board_row.count(1) == 2 and board_row.count(2) == 0:
            X_win += 100
        elif board_row.count(1) == 3 and board_row.count(2) == 0:
            X_win += 100000      # from X's perspective, we want to end up here
        elif board_row.count(2) == 1 and board_row.count(1) == 0:
            O_win += 1
        elif board_row.count(2) == 2 and board_row.count(1) == 0:
            O_win += 100
        elif board_row.count(2) == 3 and board_row.count(1) == 0:
            O_win += 100000      # from X's perspective, we want to absolutely avoid this 
    if me:
        return X_win - O_win
    else:
        return O_win - X_win

##############################
####  ALPHA BETA PRUNING  ####
##############################

def evaluate(tree):
    best_board = None
    best_heuristic = -9999999
    multiple_best_moves = []        # in case there are multiple moves with max heuristic
    for child in tree.children:
        child_value = -negamax(child, -999999, 999999, False)
        # print("Best heuristic for ", child.move, ": ", child_value)
        if child_value > best_heuristic:
            best_heuristic = child_value
            best_board = child
            multiple_best_moves = [child]           # reset list if new max value
        elif child_value == best_heuristic:
            multiple_best_moves.append(child)       # append other moves with max value

    # randomly pick from list of best moves
    if len(multiple_best_moves) > 1:
        # print("Randomly picking a move...")
        n = np.random.randint(0,len(multiple_best_moves))
        best_board = multiple_best_moves[n]

    # print("Best Overall Heuristic: ", best_heuristic)
    # print("Best Move is: ", best_board.move)
    return best_board.move

def negamax(tree, alpha, beta, me):
    """negamax algorithm"""
    if not tree.children:
        return sumHeuristic(tree)
    for child in tree.children:
        alpha = max(alpha, -negamax(child, -beta, -alpha, not me))
        if alpha >= beta:
            return alpha
    return alpha

###########################
####  PRINT FUNCTIONS  ####
###########################

# recursively print the tree
def printTree(tree):
    print("Root node: ")
    print("Heuristic: ", tree.heuristic)
    print_board(tree.full_board)
    for i in range(len(tree.children)):
        print("Parent node: ")
        print("Heuristic: ", tree.children[i].heuristic)
        print_board(tree.children[i].full_board)
        printTreeRecursive(tree.children[i], 1, False)

def printTreeRecursive(tree, depth, me):
        if not tree.children:
            return
        for i in range(len(tree.children)):
            print_board(tree.children[i].full_board)
            print("Depth: ", depth)
            print("Heuristic: ", tree.children[i].heuristic, "\n")
            printTreeRecursive(tree.children[i], depth+1, not me)

# print a row
# This is just ported from game.c
def print_board_row(board, a, b, c, i, j, k):
    print(" "+s[board[a][i]]+" "+s[board[a][j]]+" "+s[board[a][k]]+" | " \
             +s[board[b][i]]+" "+s[board[b][j]]+" "+s[board[b][k]]+" | " \
             +s[board[c][i]]+" "+s[board[c][j]]+" "+s[board[c][k]])

# Print the entire board
# This is just ported from game.c
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()

########################
####  SERVER STUFF  ####
########################

# choose a move to play
def play(depth):
    # print("Depth: ", depth)
    # print_board(boards)
    boards_copy = deepcopy(boards)

    # calculate heuristic values of all the sub-boards at root node
    heuristic = [0]
    for i in range(1,10):
        value = getHeuristic(boards_copy[i], False)
        heuristic.append(value)

    # create new tree
    root_node = Tree(boards_copy, curr, 0, heuristic)

    # build tree with specified depth
    tree = buildTree(root_node, depth)
    # printTree(tree)

    # find optimal move using negamax
    move = evaluate(tree)
    # print("playing", move)
    place(curr, move, 1)
    return move

# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# only parses the strings that are necessary
def parse(string, num_moves):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []
    if command == "second_move":
        place(int(args[0]), int(args[1]), 2)
        # print("opponent played: ", int(args[1]))
        return play(3)
    elif command == "third_move":
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        # print("opponent played: ", int(args[2]))
        return play(3)
    elif command == "next_move":
        place(curr, int(args[0]), 2)
        # increment depth as game progresses deeper
        # print("Move: ", num_moves)
        if num_moves <= 8:
            depth = 3
        elif num_moves <= 17:
            depth = 4
        elif num_moves <= 30:
            depth = 5
        else:
            depth = 6
        # print("opponent played: ", int(args[0]))
        return play(depth)
    elif command == "win":
        print("Yay!! We win!! :)")
        # print_board(boards)
        return -1
    elif command == "loss":
        print("We lost :(")
        # print_board(boards)
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    num_moves = 0
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        num_moves += 1
        for line in text.split("\n"):
            response = parse(line, num_moves)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
