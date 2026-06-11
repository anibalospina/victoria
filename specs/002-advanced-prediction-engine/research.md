# Research: Advanced Weighted Prediction Engine

This document outlines the findings, math models, and structural decisions made for the Advanced Weighted Prediction Engine.

## Findings & Data Analysis

An investigation of the `results.csv` dataset yielded the following facts:
1. **World Cup Matches**: There are exactly 964 matches where `tournament == "FIFA World Cup"`.
2. **Inter-Confederation Matches**: Out of the 964 World Cup matches, 664 are played between countries from different confederations (e.g. UEFA vs CONMEBOL).
3. **Confederation Mapping**: Static confederation mapping covers major countries, while other countries can be dynamically mapped by checking the tournaments they have played in.

### Federation Strength Index (FSI) Calculations

The FSI for a confederation is calculated as:
$$\text{FSI}_C = \frac{\text{Average Points Earned by } C \text{ in inter-confederation WC matches}}{\text{Global Average Points Earned per team-match in inter-confederation WC matches}}$$

Using the entire historical dataset, the computed FSI values are:
* **CONMEBOL**: 1.2158 (336 matches, 566 points)
* **UEFA**: 1.2011 (533 matches, 887 points)
* **CAF**: 0.6772 (162 matches, 152 points)
* **CONCACAF**: 0.6207 (150 matches, 129 points)
* **AFC**: 0.5272 (141 matches, 103 points)
* **OFC**: 0.3609 (6 matches, 3 points)

*Edge Case Fallback*: If a confederation has 0 matches (e.g., in mock test datasets), FSI defaults to `1.0` to avoid division by zero.

---

## Prediction Mathematical Model

### 1. Temporal Decay & Weighting
Matches are weighted using an exponential decay function:
$$w_m = e^{-0.0019 \times \text{days\_ago}(m)}$$
This corresponds to a 1-year half-life ($t_{1/2} = 365$ days).

* **Recent Performance Form**: Calculated using match records from the last 24 months (730 days) from the reference date (max date in dataset).
* **H2H Records**: Includes all historical head-to-head matches, but weights them using the decay function.

### 2. Hybrid H2H / General Form Model
To prevent old H2H matches from distorting predictions, the H2H weight is scaled by the temporal decay of the most recent H2H match:
$$D = \max_{m \in M_{\text{H2H}}} (w_m) \quad (\text{or } 0.0 \text{ if } M_{\text{H2H}} \text{ is empty})$$

The final hybrid expected goals (before FSI scaling and host advantage) are:
$$\lambda_A = (0.3 \times D) \times \lambda_{A, \text{H2H}} + (1.0 - 0.3 \times D) \times \lambda_{A, \text{gen}}$$
$$\lambda_B = (0.3 \times D) \times \lambda_{B, \text{H2H}} + (1.0 - 0.3 \times D) \times \lambda_{B, \text{gen}}$$

Where:
* $\lambda_{i, \text{H2H}}$ is the decay-weighted average goals scored by team $i$ in H2H matches.
* $\lambda_{i, \text{gen}}$ is the expected goals based on overall form: $\lambda_{A, \text{gen}} = \text{avg\_scored}_A \times (\text{avg\_conceded}_B / \text{global\_avg})$.

### 3. Federation Strength Calibration
For inter-confederation matches, the expected goals are scaled:
$$\lambda'_A = \lambda_A \times \frac{\text{FSI}_A}{\text{FSI}_B}$$
$$\lambda'_B = \lambda_B \times \frac{\text{FSI}_B}{\text{FSI}_A}$$

If both teams are in the same confederation, scaling factor is `1.0`.

---

## Decisions & Alternatives

1. **Caching of FSI**:
   * *Decision*: Compute the FSI values dynamically upon loading matches, but cache the result using Streamlit's `@st.cache_data`.
   * *Rationale*: Avoids recompilation on every simulation click, ensuring page performance stays under the 3-second limit.
2. **Date Constraint for General Form**:
   * *Decision*: Restrict matches for recent performance form calculation to the last 24 months.
   * *Rationale*: Matches requirements for "recent performance form" while keeping memory usage extremely low (only filters rows).
