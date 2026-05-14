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
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # O jogador X sempre começa. Se houver mais X do que O, é a vez do O.
    if x_count > o_count:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    
    # Verifica se a ação é válida (dentro dos limites e em uma célula vazia)
    if i < 0 or i > 2 or j < 0 or j > 2 or board[i][j] != EMPTY:
        raise ValueError("Ação inválida: A célula já está ocupada ou fora do tabuleiro.")
    
    # Faz uma cópia profunda (deepcopy) do tabuleiro para não modificar o original
    new_board = copy.deepcopy(board)
    
    # Aplica a jogada do jogador atual no novo tabuleiro
    new_board[i][j] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Verifica linhas
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
            
    # Verifica colunas
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return board[0][j]
            
    # Verifica diagonais
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # O jogo acaba se alguém vencer
    if winner(board) is not None:
        return True
        
    # O jogo acaba se não houver mais espaços vazios (empate)
    for row in board:
        if EMPTY in row:
            return False
            
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)

    # Se for o X, ele quer MAXIMIZAR o placar
    if current_player == X:
        best_val = -math.inf
        best_action = None
        for action in actions(board):
            # O X avalia o valor mínimo que o O vai permitir
            val = min_value(result(board, action))
            if val > best_val:
                best_val = val
                best_action = action
        return best_action

    # Se for o O, ele quer MINIMIZAR o placar
    else:
        best_val = math.inf
        best_action = None
        for action in actions(board):
            # O O avalia o valor máximo que o X vai permitir
            val = max_value(result(board, action))
            if val < best_val:
                best_val = val
                best_action = action
        return best_action


def max_value(board):
    """
    Função auxiliar para o algoritmo Minimax.
    Retorna o valor máximo possível a partir deste estado do tabuleiro.
    """
    if terminal(board):
        return utility(board)
        
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    """
    Função auxiliar para o algoritmo Minimax.
    Retorna o valor mínimo possível a partir deste estado do tabuleiro.
    """
    if terminal(board):
        return utility(board)
        
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v