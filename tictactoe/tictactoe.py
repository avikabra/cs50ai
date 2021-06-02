"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    numX = 0
    numO = 0
    for row in board:
        for square in row:
            if (square == X):
                numX += 1
            if (square == O):
                numO += 1
    if numX > numO:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != X and board[i][j] != O:
                actions.add((i, j))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try:
        moveType = player(board)
        board[action[0]][action[1]] = moveType
        return board
    except:
        print("invalid action")
        return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #check rows
    for i in range(len(board)):
        if board[i][0] == board[i][1] and board[i][0] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]

    #check cols
    for i in range(len(board)):
        if board[0][i] == board[1][i] and board[0][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    #check major diagonals:
        if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != EMPTY:
            return board[0][0]
        if board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] != EMPTY:
            return board[0][2]

    return EMPTY


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #check for tie
    numEmpty = 0
    for row in board:
        for square in row:
            if square is None:
                numEmpty += 1
    if numEmpty == 0:
        return True

    if winner(board) != EMPTY:
        return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    elif win is None:
        return 0

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -1000000
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = 1000000
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        maxVal = -1000000
        for action in actions(board):
            curr = min_value(result(board, action))
            if (curr > maxVal):
                maxVal = curr
                optAct = action
    else:
        minVal = 1000000
        for action in actions(board):
            curr = max_value(result(board, action))
            if (curr < minVal):
                minVal = curr
                optAct = action

    print(optAct)
    return optAct
