# Feature Specification: Predict Match

**Feature Branch**: `001-predict-match`

**Created**: 2026-06-06

**Status**: Draft

**Input**: User description: "Develop the Football Pool Prediction Assistant, an interactive web application designed to help users determine match outcomes for their football pools. It should allow users to select two international teams, Team A and Team B, from an interactive dropdown or autocomplete list populated by all valid unique countries in the historical dataset. In this initial phase, let's call it "Predict Match," the user interface will focus strictly on a single, one-on-one match setup. There will be no bulk uploading or complex configuration screens. When the user selects the two teams and triggers the calculation, the main view must immediately present the prediction. It will display the most likely overall outcome as Team A Wins, Draw, or Team B Wins, alongside the single most probable exact final scoreline. To maintain transparency, the interface will also show a visual distribution matrix of alternative scores so the user can see the underlying confidence of the prediction. The backend logic will process the historical match records by giving exponentially higher statistical weight to games played in the last 12 to 24 months, ensuring recent form drives the outcome. It will also penalize friendly matches and give high priority to official tournament matches. Unless one of the selected teams is the actual tournament host country, the system will simulate the match under neutral ground rules, eliminating standard home-field advantages. If the two selected teams have no direct head-to-head history, the system will automatically fall back to regional competitive averages to ensure the simulation completes successfully without errors or blank states."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Match Selection & Outcome View (Priority: P1)

Users want to select two international football teams and instantly view predictions for the overall winner and the most probable exact scoreline, ensuring quick decisions for their football pools.

**Why this priority**: This represents the core MVP loop of the application, delivering the basic user value of predicting a match outcome.

**Independent Test**: Select two teams with direct historical data, run the simulation, and verify that the predicted outcome and exact score are rendered on screen within 3 seconds.

**Acceptance Scenarios**:

1. **Given** the user is on the main prediction screen,
   **When** the user selects "Brazil" as Team A and "Argentina" as Team B, and triggers the prediction,
   **Then** the screen displays the suggested winner and the exact scoreline within 3 seconds.
2. **Given** the user selects two teams with no direct head-to-head history (e.g., "Japan" and "Senegal"),
   **When** the user triggers the prediction,
   **Then** the screen displays a prediction using regional competitive averages instead of failing or displaying a blank state.

---

### User Story 2 - Confidence Visualisation via Alternative Scores Matrix (Priority: P2)

Users want to view a visual matrix of alternative score probabilities to understand the distribution of risk and prediction confidence.

**Why this priority**: Adds transparency to the prediction, helping users make informed pool choices based on the confidence margin.

**Independent Test**: Trigger a match prediction and check that a visual probability matrix of alternative scorelines is rendered.

**Acceptance Scenarios**:

1. **Given** a prediction has been calculated for "Brazil" vs "Argentina",
   **When** the results are rendered,
   **Then** the interface displays a visual grid showing the relative probability distribution of alternative scorelines (e.g., from 0-0 up to at least 4-4).

---

### Edge Cases

- **Selected Teams are Identical**: What happens if the user selects the same country for both Team A and Team B?
  - *Resolution*: The system must disable the calculation trigger button or show a validation warning to prevent a team from playing against itself.
- **No Direct Head-to-Head History**: What happens if the two selected teams have never played each other?
  - *Resolution*: The system must automatically fall back to regional competitive averages to compute the simulation without raising an error.
- **Neutral Ground Rules vs Host Country**: How does the system handle home-field advantage?
  - *Resolution*: The system simulates the match under neutral ground rules (home advantage set to 0), unless one of the selected teams is verified as the actual tournament host country.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow the user to select two distinct international teams from an interactive dropdown or autocomplete list.
- **FR-002**: The country list MUST be dynamically populated from the unique set of countries present in the historical dataset.
- **FR-003**: The UI MUST prevent the calculation if Team A and Team B are identical, showing a descriptive validation message.
- **FR-004**: The system MUST calculate the overall match outcome (Team A Win, Draw, or Team B Win) and the single most probable exact scoreline using a Poisson Distribution model.
- **FR-005**: The backend logic MUST apply an exponential temporal decay function to historical matches, assigning exponentially higher weight to games played in the last 12 to 24 months.
- **FR-006**: The model calculations MUST apply match-type weighting, penalizing friendly matches and prioritizing official tournament matches.
- **FR-007**: The system MUST simulate matches under neutral ground rules (no home-field advantage) by default.
- **FR-008**: The system MUST bypass neutral ground rules if one of the selected teams is identified as the actual tournament host country.
- **FR-009**: If the two selected teams have no direct head-to-head match history, the system MUST automatically fall back to regional competitive averages to complete the prediction.
- **FR-010**: The system MUST show a visual distribution matrix of alternative score probabilities.
- **FR-011**: All analytics calculation functions MUST be implemented as pure functions with full type hinting.

### Key Entities

- **Country / Team**: Represents an international football team with confederation/region attributes.
- **Historical Match**: Represents a historical match record (date, home team, away team, home score, away score, tournament type, neutral venue flag).
- **Match Prediction**: Represents the simulation result containing outcome probabilities, the most probable exact scoreline, and the probability matrix.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The suggested winner and exact score prediction MUST be visible and comprehensible on the UI within 3 seconds of the user triggering the calculation.
- **SC-002**: 100% of prediction queries for valid teams MUST resolve successfully without blank states, using the regional fallback method if head-to-head records are absent.
- **SC-003**: The UI layout MUST adapt and render cleanly across desktop and mobile screens, focusing strictly on the one-on-one match setup.
- **SC-004**: The system memory footprint during simulation execution MUST remain under the free tier threshold of the Streamlit Community Cloud (typically ~1GB), achieved via Polars LazyFrames and caching.

## Assumptions

- The historical match dataset is available locally (e.g., as a CSV or parquet file) and contains required fields: date, teams, scores, tournament, and neutral venue flag.
- The country dropdown list is derived dynamically from the unique set of home/away teams in the dataset.
- Regional averages fallback can map each country to its respective continental confederation (e.g., UEFA, CONMEBOL, CAF, AFC, CONCACAF, OFC) using a static mapping or metadata in the dataset.
- Streamlit's `@st.cache_data` is sufficient to cache the processed historical data LazyFrames, preventing repeated expensive reads.
