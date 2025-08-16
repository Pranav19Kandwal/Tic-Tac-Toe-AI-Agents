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

def isTerminalState(board):
    return player1_wins(board) or player2_wins(board) or draw(board)

def num_0s_and_1s(board):
    count_0, count_1 = 0, 0
    for i in range(9):
        if board[i // 3][i % 3] == 1:
            count_1 += 1
        elif board[i // 3][i % 3] == 0:
            count_0 += 1
    return [count_0, count_1]

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

def isGameEnd(board, agent):
    if player1_wins(board):
        if agent == 1:
            print("RL Agent WON!!!")
        else:
            print("Congrats, You WON!!!")
        return True
    elif player2_wins(board):
        if agent == 0:
            print("RL Agent WON!!!")
        else:
            print("Congrats, You WON!!!")
        return True
    elif draw(board):
        print("Draw!!!")
        return True
    return False
    
def getNextState(board):
    candidateList = []
    for i in range(9):
        if board[i // 3][i % 3] == -1:
            candidateList.append(i)
    return candidateList[np.random.randint(len(candidateList))]

def reconstructBoard(board):
    Board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(9):
        col = i % 3
        row = i // 3
        if board[row][col] == 1:
            Board[row][col] = 'X'
        elif board[row][col] == 0:
            Board[row][col] = 'O'
        else:
            Board[row][col] = ' '
    return Board

def printBoard(board):
    Board = reconstructBoard(board)
    print("+---+---+---+")
    print(f"| {Board[0][0]} | {Board[0][1]} | {Board[0][2]} |")
    print("+---+---+---+")
    print(f"| {Board[1][0]} | {Board[1][1]} | {Board[1][2]} |")
    print("+---+---+---+")
    print(f"| {Board[2][0]} | {Board[2][1]} | {Board[2][2]} |")
    print("+---+---+---+")
    print("\n\n")

def simulateGame(agent, policy, states):
    print(f"\n********** Agent is playing as Player {agent} **********\n")
    board = boardInitialize()
    printBoard(board)
    playerTurn = [1, 0]
    i = 0
    while True:
        if playerTurn[i] == agent:
            s = state_encoding(board)
            a = policy[states[s]]
            board[a // 3][a % 3] = playerTurn[i]
            printBoard(board)
        
        else:
            nextState = getNextState(board)
            board[nextState // 3][nextState % 3] = playerTurn[i]
            printBoard(board)

        i = (i+1)%2
        if isGameEnd(board, agent):
            break
    return

def readPolicy(policyFile):
    with open(policyFile, 'r') as f:
        lines = f.readlines()
    return [int(line.strip()) for line in lines]

def main():
    # agentPlayingAs = np.random.randint(0, 2)
    agentPlayingAs = 1
    policyFile = f"policy_file{agentPlayingAs}.txt"
    policy = readPolicy(policyFile)
    states = validStates()
    simulateGame(agentPlayingAs, policy, states)

if __name__ == '__main__':
    main()