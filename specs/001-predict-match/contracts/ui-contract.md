# Interface Contract: Predict Match UI

## User Inputs
The presentation layer (Streamlit App) collects:

- **Team A (`team_a`)**: Dropdown/autocomplete selection of a unique country name from the historical dataset.
- **Team B (`team_b`)**: Dropdown/autocomplete selection of a unique country name from the historical dataset (excluding `team_a`).
- **Team A Host Checkbox (`team_a_host`)**: Boolean toggle indicating whether Team A is the tournament host country.
- **Team B Host Checkbox (`team_b_host`)**: Boolean toggle indicating whether Team B is the tournament host country.

## Calculation Trigger
- Clicking the **"Calculate Prediction"** button.
- Calculation is disabled if `team_a == team_b`.

## Outputs Presented to the User
The UI must immediately render:

1. **Overall Match Outcome**: Displays one of:
   - `[Team A] Wins` (e.g., "Brazil Wins")
   - `Draw`
   - `[Team B] Wins` (e.g., "Argentina Wins")
2. **Most Probable Exact Final Scoreline**: Formatted as `Team A Score - Team B Score` (e.g., "2 - 1").
3. **Score Distribution Matrix**: A heatmap or grid visualizing score probabilities from 0-0 up to 4-4, highlighting the most likely outcome.
