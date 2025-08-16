################################### Description ################################
| This project implements a Tic-Tac-Toe-playing agent using classic            |
| reinforcement learning techniques based on the Markov Decision Process.      |
| It models all valid game states, computes transitions and rewards, and       |
| derives an optimal policy using the Value Iteration algorithm. The trained   |
| agent can then simulate games against a random opponent. No neural networks  |
| or external ML libraries are used — it's a pure implementation of dynamic    |
| programming principles for decision making in a finite state environment.    |
################################################################################

################################################################################
| MDP (S, A, T, R, γ) formulation for Tic-Tac-Toe.                             |
################################################################################

#################################### States #################################### 
| states = all valid board configurations                                      |
| s = a0v0 + a1v1 + a2v2 + a3v3 + a4v4 + a5v5 + a6v6 + a7v7 + a8v8             |
| vi <-- [-1, 0, 1] <--> [0, 1, 2]                                             |
| ai <-- [3^i]                                                                 |
| states <-- [0, (3^9 - 1)] = 19683 = 3^9 ~ 10^5 number of states              |
################################################################################

#################################### Actions ###################################
| Number of possible/feasible cells to place the char 0/1                      |
################################################################################

#################################### Transitions ###############################
| Uniform probability distribution on opponent's next states                   |
################################################################################

#################################### Rewards ###################################
| WIN --> +1                                                                   |
| LOOSE --> -1                                                                 |
| DRAW --> 0                                                                   |
| Otherwise --> 0                                                              |
################################################################################

################################# Discount_Factor ##############################
| 1 (episodic task)                                                            |
################################################################################

#################################### Players ###################################
| Player 1 --> 1/X                                                             |
| Player 2 --> 0/O                                                             |
################################################################################

################################ Tic-Tac-Toe Board #############################
|                                   +---+---+---+                              |
|                                   |   |   |   |                              |
|                                   +---+---+---+                              |
|                                   |   |   |   |                              |
|                                   +---+---+---+                              |
|                                   |   |   |   |                              |
|                                   +---+---+---+                              |
################################################################################
