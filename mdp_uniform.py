import numpy as np

def boardInitialize():
    board = np.ones(shape=(3,3), dtype=int)*(-1)
    return board

def row_count(board, char, row):
    count = 0
    for col in range(3):
        if board[row][col] == char:
            count += 1
    return count

def col_count(board, char, col):
    count = 0
    for row in range(3):
        if board[row][col] == char:
            count += 1
    return count

def diag_count(board, char, diagonal):
    count = 0
    if diagonal == 0:
        for index in range(3):
            if board[index][index] == char:
                count += 1
    else:
        for index in range(3):
            if board[index][2 - index] == char:
                count += 1
    return count

def player1_wins(board):
    return ((row_count(board, 1, 0) == 3) or (row_count(board, 1, 1) == 3) or (row_count(board, 1, 2) == 3) or
        (col_count(board, 1, 0) == 3) or (col_count(board, 1, 1) == 3) or (col_count(board, 1, 2) == 3) or
        (diag_count(board, 1, 0) == 3) or (diag_count(board, 1, 1) == 3))

def player2_wins(board):
    return ((row_count(board, 0, 0) == 3) or (row_count(board, 0, 1) == 3) or (row_count(board, 0, 2) == 3) or
        (col_count(board, 0, 0) == 3) or (col_count(board, 0, 1) == 3) or (col_count(board, 0, 2) == 3) or
        (diag_count(board, 0, 0) == 3) or (diag_count(board, 0, 1) == 3))
    
def draw(board):
    for i in range(9):
        if board[i // 3][i % 3] == -1:
            return False
    return not (player1_wins(board) or player2_wins(board))

def isTerminalState(board):
    return player1_wins(board) or player2_wins(board) or draw(board)
    
def state_encoding(board):
    s = 0
    a = 1
    for i in range(9):
        c = i % 3
        r = i // 3
        s += (a*(board[r][c] + 1))
        a *= 3
    return s    
    
def state_decoding(s):
    i = 8
    a = 3**i
    board = boardInitialize()
    while(i >= 0):
        c = i % 3
        r = i // 3
        board[r][c] = (s // a) - 1
        s %= a
        a //= 3
        i -= 1
    return board

def getReward(board, agent):
    if player1_wins(board):
        return 1 if agent == 1 else -1
    elif player2_wins(board):
        return 1 if agent == 0 else -1
    return 0
        
def computeNextActions(board):
    actions = []
    for i in range(9):
        if board[i // 3][i % 3] == -1:
            actions.append(i)
    return actions

def num_0s_and_1s(board):
    count_0, count_1 = 0, 0
    for i in range(9):
        if board[i // 3][i % 3] == 1:
            count_1 += 1
        elif board[i // 3][i % 3] == 0:
            count_0 += 1
    return [count_0, count_1]

def saveMDP(filename, num_states, num_actions, T, R, discount_factor):
    print(f"Writing to the file {filename}...\n")
    with open(filename, "w") as f: 
        f.write(f"num_states: {num_states}\n")
        f.write(f"num_actions: {num_actions}\n")
        for s in range(num_states):
            for a in range(num_actions):
                for s_prime in range(num_states):
                    if T[s][a][s_prime] > 0:
                        f.write(f"{s} {a} {s_prime} {T[s][a][s_prime]} {R[s][a][s_prime]}\n")
        f.write(f"discount_factor: {discount_factor}\n")
    print("Done...")

def validStates():
    num_states = 3**9
    states = {}
    new_index = 0
    for s in range(num_states):
        board = state_decoding(s)
        num_0s, num_1s = num_0s_and_1s(board)
        diff = num_1s - num_0s
        if diff == 1 or diff == 0:
            states[s] = new_index
            new_index += 1
    return states

def canMakeMove(board, player):
    num_0s, num_1s = num_0s_and_1s(board)
    diff = num_1s - num_0s
    return (player == 1 and diff == 0) or (player == 0 and diff == 1)
    
def create_MDP(agentPlayingAs):
    states = validStates(agentPlayingAs)
    num_states = len(states)
    num_actions = 9
    discount_factor = 1.0
    T = np.zeros((num_states, num_actions, num_states))
    R = np.zeros((num_states, num_actions, num_states))
    
    for s in states:
        board = state_decoding(s)
        validActions = computeNextActions(board)
        if isTerminalState(board) or not(canMakeMove(board, agentPlayingAs)):
            continue
        for a in validActions:
            new_board = board.copy()
            new_board[a // 3][a % 3] = agentPlayingAs
            if isTerminalState(new_board):
                s_prime = state_encoding(new_board)
                T[states[s]][a][states[s_prime]] = 1.0
                R[states[s]][a][states[s_prime]] = getReward(new_board, agentPlayingAs)
                continue
            opponent = 0 if agentPlayingAs == 1 else 1
            next_actions = computeNextActions(new_board)
            for a_prime in next_actions:
                temp_board = new_board.copy()
                temp_board[a_prime // 3][a_prime % 3] = opponent
                s_prime = state_encoding(temp_board)
                T[states[s]][a][states[s_prime]] = 1 / len(next_actions)
                R[states[s]][a][states[s_prime]] = getReward(temp_board, agentPlayingAs)
    
    filename = f'mdp_file{agentPlayingAs}.txt'
    saveMDP(filename, num_states, num_actions, T, R, discount_factor)

create_MDP(0)