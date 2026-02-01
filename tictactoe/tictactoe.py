"""
Tic Tac Toe Player
"""

import math
import copy

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
    NoX=0
    NoO=0
    if board==initial_state():
        return X
    for i in range(3):
        for j in range(3):
            if board[i][j]==X:
                NoX +=1
            elif board[i][j]==O:
                NoO +=1
    if NoX>NoO:
        return O
    else:
        return X

    
    raise NotImplemenedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions=set()
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                actions.add((i,j))
    return actions
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    turn=player(board)
    result=copy.deepcopy(board)
    if result[action[0]][action[1]]==EMPTY:
        result[action[0]][action[1]]=turn
    else:
        print("Invalid Move")
        return board
    return result

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(3):
        if(board[i][0] == X and board[i][1]==X and board[i][2]==X):
            return X
        if(board[i][0] == O and board[i][1]==O and board[i][2]==O):
            return O
    for j in range(3):
        if(board[0][j] == X and board[1][j]==X and board[2][j]==X):
            return X
        if(board[0][j] == O and board[1][j]==O and board[2][j]==O):
            return O
    if board[0][0]==board[1][1]==board[2][2]!= EMPTY:
        return board[1][1]
    if board[0][2]==board[1][1]==board[2][0]:
        return board[1][1]
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                return False
    return True
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return 1
    if winner(board)==O:
        return -1
    else:
        return 0
    raise NotImplementedError


def minimax(board):
    if terminal(board):
        return None

    turn = player(board)
    best_move = None

    if turn == X:
        max_score = float("-inf")
        for move in actions(board):
            val = min_value(result(board, move))
            if val > max_score:
                max_score = val
                best_move = move
    else:
        min_score = float("inf")
        for move in actions(board):
            val = max_value(result(board, move))
            if val < min_score:
                min_score = val
                best_move = move

    return best_move


def min_value(board):
        v=100
        if terminal(board):
            return utility(board)
        for move in actions(board):
            v=min(v, max_value(result(board,move)))
        return v
def max_value(board):
        v=-100
        if terminal(board):
            return utility(board)
        for move in actions(board):
            v=max(v, min_value(result(board,move)))
        return v
