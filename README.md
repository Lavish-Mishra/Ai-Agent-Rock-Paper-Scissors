# Rock–Paper–Scissors AI (Adaptive Meta‑Strategy)

An adaptive Rock–Paper–Scissors (RPS) bot that predicts opponents using a mix of strategies
(trigram Markov model, mirror/anti‑mirror, and randomness), then **meta‑selects**
the best performing strategy on the fly. Includes several built‑in opponent bots and unit tests.

## Features

- **Adaptive player bot** (`RPS.player`) combining:
  - Trigram Markov prediction over opponent move history
  - Mirror and anti‑mirror heuristics
  - Random fallback
  - Online scoring system to pick the current best strategy
- **Opponent bots** (in `RPS_game.py`):
  - `abbey`: 2‑step Markov predictor + counter
  - `quincy`: periodic sequence bot
  - `kris`: counters your previous move
  - `mrugesh`: counters your most frequent recent move
  - `random_player`: pure RNG
  - `human`: play interactively from stdin
- **Simple game engine**: `play(player1, player2, num_games, verbose=False)`
- **Unit tests** to verify the bot consistently beats each built‑in opponent.

## Project Structure

```
.
├── main.py           # Entry point with sample matchups and (optional) tests
├── RPS.py            # Your adaptive player strategy
├── RPS_game.py       # Game loop + built-in opponent bots
└── test_module.py    # unittest suite
```

## Requirements

- Python 3.8+ (standard library only; no external deps)

## Installation

```bash
git clone <your-repo-url>
cd <your-repo-folder>
# (optional) create venv
python -m venv .venv && source .venv/bin/activate   # on Windows: .venv\Scripts\activate
```

## Usage

### 1) Quick start (run sample matchups)
`main.py` is wired to pit your bot against all built‑in opponents:

```bash
python main.py
```

By default, it runs:
```py
play(player, abbey, 1000)
play(player, quincy, 1000)
play(player, kris, 1000)
play(player, mrugesh, 1000)
```
and prints each series’ final results and win rate.

### 2) Play interactively against a bot
Uncomment the interactive line in `main.py` to play as a human:

```py
# play(human, abbey, 20, verbose=True)
```
Then run:
```bash
python main.py
```
You’ll be prompted each round: `[R]ock, [P]aper, [S]cissors?`

### 3) Toggle verbosity / different opponents
You can pass `verbose=True` to `play(...)` to see per‑round output, and switch
any `playerX` / `playerY` function to try different matchups, e.g.:

```py
play(player, random_player, 100, verbose=True)
```

### 4) Run tests
```bash
python -m unittest test_module.py
```
Each test asserts your bot wins **≥ 60%** over 1000 rounds vs each opponent.

## API Reference

### `play(player1, player2, num_games, verbose=False) -> float`
Runs `num_games` rounds. Each `player` is a function `prev_opponent_play -> "R"|"P"|"S"`.
Returns **Player 1 win rate (0–100)** and prints a summary:

- `player1`: function generating your move given the opponent’s previous move
- `player2`: opponent bot (same signature)
- `verbose`: print round‑by‑round plays and outcomes

### Opponent Bots
- **`abbey(prev)`** — Tracks 2‑step patterns (`XY`) in your history and counters the most likely next move.
- **`quincy(prev)`** — Cycles through a fixed sequence.
- **`kris(prev)`** — Counters your last move.
- **`mrugesh(prev)`** — Looks at your last ten moves, counters the most frequent.
- **`random_player(prev)`** — Uniform random move.
- **`human(prev)`** — Prompts for input; validates `"R"|"P"|"S"`.

## How the Adaptive Player Works (`RPS.player`)

1. **Track histories** of both players.
2. **Update a trigram (N=3) Markov table** on the opponent’s sequence to predict their next move.
3. **Simulate all candidate strategies** (trigram, mirror, anti‑mirror, random) to get a proposed next move from each.
4. **Score strategies online** based on how their *previous* proposals would have fared against the opponent’s *actual* last move:
   - +1 for a would‑be win, +0.3 for draw, −0.5 for loss
5. **Pick the best‑scoring strategy right now** and play its latest proposed move.

This meta‑strategy lets the bot shift rapidly if the opponent switches patterns.

## Extending

- **Add a new candidate strategy** inside `RPS.py` and register it in the `strategies` dict.
- **Add a new opponent** by writing a function with the `prev_opponent_play` signature and plugging it into `main.py` or tests.
- **Tune**: weights in the scoring function, trigram `N`, or add/replace heuristics.

## Example Output (abridged)

```
Final results: {'p1': 678, 'p2': 269, 'tie': 53}
Player 1 win rate: 71.6%
```

_Actual numbers vary since several components are stochastic._

## Tips

- Keep functions pure (derive next move only from `prev_opponent_play` / stored state).
- When experimenting, set a fixed `random.seed(...)` for reproducibility.
- For manual play, keep `verbose=True` small (e.g., 20–50 rounds).
