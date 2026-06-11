# Feature Specification: Advanced Weighted Prediction Engine

**Feature Branch**: `002-advanced-prediction-engine`

**Created**: 2026-06-10

**Status**: Draft

**Input**: User description: "Develop the Advanced Weighted Prediction Engine feature for the Football Pool Prediction Assistant to improve prediction accuracy and eliminate regional competition bias. When a user simulates a match between Team A and Team B, the application must compute a final probability score where exactly 30% of the weight is driven by the historical Head-to-Head (H2H) match records between those two specific teams, and 70% of the weight is driven by each team's recent performance form within the last 12 to 24 months. To prevent statistical distortion when comparing teams from isolated competitive ecosystems—such as Colombia in CONMEBOL vs. Spain in UEFA—the engine must automatically map every country to its official football confederation. The system will dynamically calibrate each team's calculated offensive and defensive power ratings using a Federation Strength Index derived from historical inter-confederation World Cup matches, ensuring that goals scored in highly competitive regions are properly scaled against lower-tier regions. In the user interface, this advanced calculation must run seamlessly behind the scenes upon clicking the simulation button, maintaining the clean single-match layout and delivering the final 1X2 recommendation, exact score, and probability breakdown within three seconds without adding any configuration complexity for the user."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Advanced Hybrid Prediction (Priority: P1)

Users want to simulate a match and receive a prediction that incorporates both direct head-to-head records and recent form in a 30/70 split, ensuring a balanced prediction that doesn't rely solely on outdated matchups.

**Why this priority**: This represents the core mathematical model change, directly improving prediction accuracy for all matchups.

**Independent Test**: Simulate Argentina vs. Iceland (who have a single, old H2H match). Verify that the predicted outcome and score are driven primarily by their recent overall performance (70%) rather than only the 2018 H2H draw (30%).

**Acceptance Scenarios**:

1. **Given** a user simulates a match between two teams with H2H history,
   **When** the prediction is triggered,
   **Then** the expected goals are calculated as a weighted sum of 30% H2H average and 70% recent general form.
2. **Given** a user simulates a match between two teams with no H2H history,
   **When** the prediction is triggered,
   **Then** the expected goals are calculated using 100% of the general form/regional fallback.

---

### User Story 2 - Federation Strength Calibration (Priority: P2)

Users want to simulate inter-confederation matches (e.g., Colombia in CONMEBOL vs. Spain in UEFA) and get a calibrated result that accounts for the relative strength difference between their federations.

**Why this priority**: Eliminates regional bias and ensures that high-scoring performances in less competitive regions are scaled down when facing highly competitive regions.

**Independent Test**: Select a highly rated team from a less competitive confederation and a team from a highly competitive confederation. Verify that the Federation Strength Index scales their relative offensive/defensive ratings.

**Acceptance Scenarios**:

1. **Given** a match between Colombia (CONMEBOL) and Spain (UEFA),
   **When** the simulation button is clicked,
   **Then** the system dynamically scales Colombia's and Spain's ratings using the calculated Federation Strength Index.
2. **Given** a match between two teams from the same confederation (e.g., Brazil vs. Argentina),
   **When** the simulation is run,
   **Then** no federation strength scaling is applied (scaling factor is 1.0).

---

### Edge Cases

- **No World Cup Matches for a Confederation**: A confederation (e.g., OFC) has very few or no inter-confederation World Cup matches in the dataset.
  - *Resolution*: The system must fall back to a baseline Federation Strength Index of 1.0 for that confederation to prevent math division errors.
- **Teams have only 1 H2H Match from 20 years ago**: The decay weight makes the H2H contribution extremely small.
  - *Resolution*: The 30% H2H weight is multiplied by the temporal decay, and the remaining unallocated weight is shifted to the general form to prevent old matches from distorting the prediction.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST calculate expected goals using a hybrid formula: 30% weight from historical Head-to-Head (H2H) match records and 70% weight from recent general performance form.
- **FR-002**: Recent performance form MUST be calculated using match records from the last 24 months, applying the exponential temporal decay function with a 1-year half-life.
- **FR-003**: The system MUST map every country to its official confederation (UEFA, CONMEBOL, CAF, AFC, CONCACAF, OFC).
- **FR-004**: The system MUST dynamically compute a Federation Strength Index (FSI) for each confederation using all historical World Cup matches played between teams of different confederations.
- **FR-005**: The FSI for a confederation MUST be calculated as the ratio of average points earned (3 for win, 1 for draw) in inter-confederation World Cup matches, normalized relative to the global average.
- **FR-006**: In inter-confederation matches, the system MUST multiply each team's expected goals ($\lambda$) by the ratio of their respective Federation Strength Indices: $\text{scale\_factor}_A = \text{FSI}_A / \text{FSI}_B$.
- **FR-007**: The FSI scaling factor MUST be 1.0 if both teams belong to the same confederation.
- **FR-008**: The UI MUST remain clean and run this advanced calculation seamlessly behind the scenes without adding any configuration controls for the user.
- **FR-009**: The UI MUST display the final 1X2 recommendation ("Gana Local", "Empate", "Gana Visitante"), the exact scoreline, and the probability breakdown within 3 seconds of clicking the button.

### Key Entities

- **Federation Strength Index**: The dynamically computed relative strength metric of a confederation based on World Cup history.
- **Hybrid Match Prediction**: The output of the prediction engine incorporating H2H weight, recent form weight, and FSI scaling.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The 1X2 recommendation, exact score, and probability breakdown MUST be visible on the UI within 3 seconds of clicking the button.
- **SC-002**: 100% of inter-confederation simulations MUST successfully resolve using FSI scaling without causing overflow or division-by-zero errors.
- **SC-003**: The predicted win probabilities and scores MUST reflect the 30/70 hybrid weighting and the FSI scaling.

## Assumptions

- The historical match dataset contains a `tournament` column where World Cup matches are identified by `"FIFA World Cup"`.
- The confederation mapping is defined statically for major teams and dynamically inferred for others.
- The FSI calculations are cached using Streamlit's `@st.cache_data` to ensure low memory footprint (under 1GB).
