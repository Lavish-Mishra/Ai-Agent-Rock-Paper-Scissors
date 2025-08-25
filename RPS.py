import random
from collections import defaultdict, deque

moves = ["R", "P", "S"]
beats = {"R": "P", "P": "S", "S": "R"}
loses_to = {"R": "S", "P": "R", "S": "P"}

# History
opp_history = []
my_history = []

# Candidate strategies and their scores
strategy_scores = defaultdict(int)

# Trigram Model
N = 3
transition_table = defaultdict(lambda: defaultdict(int))
opp_window = deque(maxlen=N)

def update_trigram_model(prev):
    if len(opp_window) == N:
        transition_table[tuple(opp_window)][prev] += 1
    opp_window.append(prev)

def trigram_strategy():
    if len(opp_window) < N:
        return random.choice(moves)
    next_probs = transition_table[tuple(opp_window)]
    if not next_probs:
        return random.choice(moves)
    prediction = max(next_probs, key=next_probs.get)
    return beats[prediction]  # we counter their likely next move

def mirror_strategy():
    if not opp_history:
        return random.choice(moves)
    return beats[opp_history[-1]]

def anti_mirror_strategy():
    if not opp_history:
        return random.choice(moves)
    return beats[beats[opp_history[-1]]]

def random_strategy():
    return random.choice(moves)

# All strategy functions
strategies = {
    "trigram": trigram_strategy,
    "mirror": mirror_strategy,
    "anti_mirror": anti_mirror_strategy,
    "random": random_strategy
}

# Track simulated strategies' past moves
simulated_moves = {name: [] for name in strategies}

def player(prev_play):
    if prev_play:
        opp_history.append(prev_play)
        update_trigram_model(prev_play)

        # Score each strategy by comparing its last simulated move to the actual opponent move
        for name, moves_list in simulated_moves.items():
            if moves_list:
                predicted_move = moves_list[-1]
                if beats[predicted_move] == prev_play:
                    strategy_scores[name] += 1
                elif predicted_move == prev_play:
                    strategy_scores[name] += 0.3  # small bonus for draw
                else:
                    strategy_scores[name] -= 0.5  # penalty for wrong prediction

    # Simulate all strategies for next round
    for name, strat_func in strategies.items():
        simulated_moves[name].append(strat_func())

    # Choose the current best-performing strategy
    best_strategy = max(strategy_scores, key=strategy_scores.get, default="random")
    move = simulated_moves[best_strategy][-1]

    my_history.append(move)
    return move
