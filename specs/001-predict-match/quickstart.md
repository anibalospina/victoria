# Quickstart & Validation Guide: Predict Match (Victoria)

This guide outlines how to run and validate Victoria locally.

## Prerequisites
- Python 3.11+
- Git
- Internet connection (to download the Kaggle historical football dataset if not already present)

## Setup Commands

1. **Install dependencies**:
   ```bash
   pip install streamlit polars scipy pytest
   ```

2. **Verify Dataset**:
   Ensure your historical matches dataset is placed in the project root as `results.csv`.

## Run the Application
Start the Streamlit application:
```bash
streamlit run app.py
```

## Validation Scenarios

### Scenario 1: Standard Prediction (Direct History)
- **Action**: Open the app, select `Brazil` as Team A and `Argentina` as Team B. Ensure both host country checkboxes are unchecked. Click **Calculate Prediction**.
- **Expected Outcome**: 
  - Prediction results are displayed within 3 seconds.
  - The winner outcome (Team A Win, Draw, or Team B Win) and the exact scoreline are visible.
  - The alternative scores grid is displayed below the main prediction.

### Scenario 2: Host Advantage Check
- **Action**: Select `Brazil` and `Argentina`. Toggle "Host Country" next to `Brazil`. Click **Calculate Prediction**.
- **Expected Outcome**: 
  - The predicted goals/win probability for Brazil increases relative to Scenario 1 due to the host advantage multiplier.

### Scenario 3: Regional Fallback (No Head-to-Head)
- **Action**: Select two teams with no head-to-head match history in the dataset. Click **Calculate Prediction**.
- **Expected Outcome**:
  - The app calculates and renders the prediction successfully using regional competitive averages without raising a blank screen or calculation errors.

## Running Unit Tests
To run unit tests and verify model correctness:
```bash
pytest tests/
```
