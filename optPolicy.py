import numpy as np
import sys

def readMDP(mdp_file):
    with open(mdp_file, 'r') as f:
        lines = f.readlines()
    num_states = int(lines[0].split(":")[1].strip())
    num_actions = int(lines[1].split(":")[1].strip())
    T = np.zeros((num_states, num_actions, num_states))
    R = np.zeros((num_states, num_actions, num_states)) 
    for line in lines[2:]:
        if line.startswith("discount_factor"):
            gamma = float(line.split(":")[1].strip())
            break
        s, a, s_prime, t_val, r_val = line.strip().split()
        s, a, s_prime = int(s), int(a), int(s_prime)
        t_val, r_val = float(t_val), float(r_val)
        T[s][a][s_prime] = t_val
        R[s][a][s_prime] = r_val

    return T, R, gamma

def state_decoding(s):
    i = 8
    a = 3**i
    board = np.zeros((3, 3), dtype=int)
    while(i >= 0):
        c = i % 3
        r = i // 3
        board[r][c] = (s // a) - 1
        s %= a
        a //= 3
        i -= 1
    return board

def validActions(s):
    board = state_decoding(s)
    actions = []
    for i in range(9):
        if board[i // 3][i % 3] == -1:
            actions.append(i)
    return actions

def computeQ_value(s, a, V, T, R, gamma):
    Q = 0
    num_states, num_actions = T.shape[0], T.shape[1]
    for s_prime in range(num_states):
        Q += (T[s][a][s_prime] * (R[s][a][s_prime] + gamma*V[s_prime]))
    return Q

def computeBellmanOptimalityEquations(V, T, R, gamma):
    num_states, num_actions = T.shape[0], T.shape[1]
    new_V = np.zeros(num_states)
    for s in range(num_states):
        action_values = []
        for a in range(num_actions):
            val = 0
            for s_prime in range(num_states):
                val += (T[s][a][s_prime] * (R[s][a][s_prime] + gamma* V[s_prime]))
            action_values.append(val)
        new_V[s] = np.max(action_values)
    return new_V

def valueIteration(T, R, gamma, tol=1e-2):
    num_states= T.shape[0]
    V = np.zeros(num_states)
    while True:
        newV = computeBellmanOptimalityEquations(V, T, R, gamma)
        if np.allclose(newV, V, atol=tol):
            V = newV
            break
        V = newV     
    return V


def computeOptimalPolicy(mdp_file):
    T, R, gamma = readMDP(mdp_file)
    num_states, num_actions = T.shape[0], T.shape[1]
    optimal_policy = np.zeros(num_states, dtype=int)
    V = valueIteration(T, R, gamma)
    for s in range(num_states):
        Q_global = float('-inf')
        valid_actions = validActions(s)
        for a in valid_actions:
            Q_local = computeQ_value(s, a, V, T, R, gamma)
            if Q_local > Q_global:
                optimal_policy[s] = a
                Q_global = Q_local
    return optimal_policy

def savePolicy(policy, filename):
    print(f"Saving to file {filename} ...")
    with open(filename, 'w') as f:
        for action in policy:
            f.write(f"{action}\n") 
    print("Done ...")
  
def main():
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} --agentPlayingAs --mdp_file")
        exit(1)
    
    agentPlayingAs = int(sys.argv[1])
    mdp_file = sys.argv[2]
    optimalPolicy = computeOptimalPolicy(mdp_file)
    filename = f'policy_file{agentPlayingAs}.txt'
    savePolicy(optimalPolicy, filename)

if __name__ == '__main__':
    main()