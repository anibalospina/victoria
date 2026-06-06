# Technical Research: Predict Match

## Decisions & Rationale

### 1. Poisson Distribution Modeling for Match Predictions
- **Decision**: Use `scipy.stats.poisson` to calculate the discrete probability distribution of goals scored by Team A and Team B.
- **Rationale**: Football goals are discrete, independent events well-modeled by a Poisson process. It provides mathematically sound and easily computable probabilities for exact scorelines.
- **Alternatives Considered**: 
  - *Machine Learning (Random Forest/XGBoost)*: Rejected due to high memory footprint and potential overfitting on international match features in Streamlit's free tier.
  - *Simple Historical Average*: Rejected as it fails to capture the probability distribution of exact scores.

### 2. Exponential Temporal Decay
- **Decision**: Apply an exponential decay factor $W = e^{-\alpha \cdot t}$ where $t$ is the age of the match in days and $\alpha$ is a decay constant set to yield a 1-year (365-day) half-life.
- **Rationale**: Form fluctuates over time; matches played in the last 12-24 months are vastly more representative of current strength than matches from 10 years ago.
- **Alternatives Considered**: 
  - *Hard Date Cutoffs (e.g., only matches from last 2 years)*: Rejected as it introduces artificial boundary effects where a game 731 days ago has 0 weight and 730 days has full weight.

### 3. Match Importance Weighting
- **Decision**: Weight match contributions by importance: official tournament games (World Cup, Qualifiers) receive a multiplier of $1.5$, whereas friendly matches are penalized with a multiplier of $0.5$.
- **Rationale**: Teams often play sub-optimal lineups or test tactics in friendlies, making friendlies less predictive of competitive strength.

### 4. Zero Head-to-Head Fallback (Regional Averages)
- **Decision**: If Team A and Team B have no direct historical match records, compute their expected goals ($\lambda$) by substituting their individual historic team strengths relative to their confederation's average performance against the opponent's confederation.
- **Rationale**: Ensures the simulation always completes successfully without raising errors or returning blank states.

### 5. High-Performance Data Processing via Polars
- **Decision**: Use `polars` instead of `pandas` and strictly operate on LazyFrames using `.lazy()` and vectorized expressions.
- **Rationale**: Polars provides memory-efficient, multi-threaded execution and query planning optimization, which is crucial for remaining under the ~1GB memory limit of Streamlit Community Cloud.
