# Data Model: Advanced Weighted Prediction Engine

This document defines the key entities, fields, relationships, and validation rules for the prediction engine.

## Entities & Schemas

### 1. Confederation Map
Maps team names to their official football confederation.

| Field | Type | Description |
|---|---|---|
| `team` | `str` | Name of the team (Unique ID) |
| `confederation` | `str` | One of: `UEFA`, `CONMEBOL`, `CAF`, `AFC`, `CONCACAF`, `OFC` |

*Validation Rules*:
* Every team in the simulation must have a confederation.
* Defaults to `UEFA` if unclassifiable.

### 2. Federation Strength Index (FSI)
The calculated index of a confederation's competitive strength based on World Cup history.

| Field | Type | Description |
|---|---|---|
| `confederation` | `str` | One of the 6 official confederations |
| `matches_played` | `int` | Total inter-confederation World Cup matches played by teams in this confederation |
| `points_earned` | `float` | Sum of points: 3 for win, 1 for draw, 0 for loss |
| `average_points` | `float` | `points_earned / matches_played` |
| `fsi` | `float` | Normalized strength index: `average_points / global_average_points` |

*Validation Rules*:
* If `matches_played == 0`, `fsi` defaults to `1.0`.
* `fsi` must be positive.

### 3. Prediction Result
The final output returned by the analytics layer.

| Field | Type | Description |
|---|---|---|
| `team_a` | `str` | Local team |
| `team_b` | `str` | Visitor team |
| `expected_goals_a` | `float` | Predicted expected goals for team A after form decay, hybrid H2H, FSI scaling, and host multiplier |
| `expected_goals_b` | `float` | Predicted expected goals for team B after form decay, hybrid H2H, FSI scaling, and host multiplier |
| `prob_a_win` | `float` | Poisson probability of Team A winning |
| `prob_draw` | `float` | Poisson probability of a draw |
| `prob_b_win` | `float` | Poisson probability of Team B winning |
| `exact_score` | `Tuple[int, int]` | Most probable exact scoreline $(G_A, G_B)$ |
| `score_matrix` | `List[List[float]]` | $5 \times 5$ probability matrix for scorelines up to 4-4 |
| `fallback_used` | `bool` | `True` if no direct H2H matches whatsoever were found |

---

## State Transitions & Workflows

1. **Initalization**:
   - Matches loaded from `results.csv`.
   - Confederation map constructed for all unique teams.
   - Federation Strength Indices dynamically computed using the historical matches and cached.

2. **Simulation Workflow**:
   - User selects `team_a` and `team_b`.
   - Analytics layer retrieves `FSI_A` and `FSI_B`.
   - Calculate H2H expected goals $\lambda_{A, \text{H2H}}$, $\lambda_{B, \text{H2H}}$ and maximum decay weight $D$ from all historical H2H matches.
   - Calculate recent form expected goals $\lambda_{A, \text{gen}}$, $\lambda_{B, \text{gen}}$ using matches from only the last 24 months.
   - Combine H2H and general form using the recency-weighted hybrid formula.
   - Apply Federation Strength Index scaling factor `FSI_A / FSI_B`.
   - Apply host advantage multiplier if applicable.
   - Calculate Poisson outcome probabilities.
