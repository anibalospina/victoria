# Quickstart Validation Guide: Advanced Weighted Prediction Engine

This guide details how to validate that the new weighted prediction engine and FSI scaling work correctly.

## Prerequisites

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Running Tests

Verify the math and logic by running the test suite:
```bash
pytest tests/
```

## Running the App

Start the Streamlit application:
```bash
streamlit run app.py
```

---

## Validation Scenarios

### Scenario 1: Argentina vs Iceland (Hybrid H2H & Recent Form Decay)
* **Goal**: Validate that old H2H matches don't distort prediction outcomes.
* **Setup**: Simulate Argentina vs Iceland.
* **Execution**: Click "Calcular Predicción".
* **Expected Outcome**:
  * The single 2018 H2H draw (1-1) has its weight decayed significantly (weight $\approx e^{-0.0019 \times 3000} \approx 0.003$).
  * The remaining $99.7\%$ of the H2H weight shifts to Argentina's and Iceland's recent general forms.
  * Argentina is predicted to win with a high probability (approx. $65\%+$) rather than a draw.

### Scenario 2: Colombia vs Spain (Inter-Confederation FSI Calibration)
* **Goal**: Validate that FSI scales ratings for teams from different confederations.
* **Setup**: Simulate Colombia (CONMEBOL) vs Spain (UEFA).
* **Execution**: Click "Calcular Predicción".
* **Expected Outcome**:
  * Colombia belongs to CONMEBOL ($\text{FSI} \approx 1.216$).
  * Spain belongs to UEFA ($\text{FSI} \approx 1.201$).
  * Expected goals for Colombia are multiplied by $1.216 / 1.201 \approx 1.012$.
  * Expected goals for Spain are multiplied by $1.201 / 1.216 \approx 0.988$.

### Scenario 3: Brazil vs Argentina (Intra-Confederation Match)
* **Goal**: Validate that FSI scaling does not apply within the same confederation.
* **Setup**: Simulate Brazil (CONMEBOL) vs Argentina (CONMEBOL).
* **Execution**: Click "Calcular Predicción".
* **Expected Outcome**:
  * Both teams are from CONMEBOL.
  * The FSI scaling factor is exactly `1.0`.
