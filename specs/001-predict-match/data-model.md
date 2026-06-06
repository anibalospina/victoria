# Data Model: Predict Match

## Entities

### 1. Country (Team)
Represents an international football team.

| Field | Type | Description | Validation Rules |
| :--- | :--- | :--- | :--- |
| `name` | String | Unique name of the country (e.g., "Brazil") | Must be non-empty, unique in the dataset. |
| `confederation` | String | Regional confederation (e.g., "UEFA", "CONMEBOL") | Must map to one of: UEFA, CONMEBOL, CAF, AFC, CONCACAF, OFC. |

### 2. HistoricalMatch
Represents a historic international football match record.

| Field | Type | Description | Validation Rules |
| :--- | :--- | :--- | :--- |
| `date` | Date | Date when the match was played | ISO Format YYYY-MM-DD. |
| `home_team` | String | Name of the home country | Must match a valid Country. |
| `away_team` | String | Name of the away country | Must match a valid Country, cannot be equal to `home_team`. |
| `home_score` | Integer | Goals scored by home team | Non-negative integer. |
| `away_score` | Integer | Goals scored by away team | Non-negative integer. |
| `tournament` | String | Tournament classification (e.g., "FIFA World Cup", "Friendly") | Non-empty. |
| `neutral` | Boolean | True if played on neutral ground | Default is False. |

### 3. MatchPrediction
The calculated output representing simulated match statistics.

| Field | Type | Description |
| :--- | :--- | :--- |
| `team_a` | String | Name of Team A |
| `team_b` | String | Name of Team B |
| `prob_a_win` | Float | Probability of Team A winning (0.0 to 1.0) |
| `prob_draw` | Float | Probability of a draw (0.0 to 1.0) |
| `prob_b_win` | Float | Probability of Team B winning (0.0 to 1.0) |
| `exact_score` | Tuple[Int, Int] | Most likely exact scoreline (e.g., `(2, 1)`) |
| `score_matrix` | List[List[Float]] | Probability distribution matrix for scores up to 4-4 |
