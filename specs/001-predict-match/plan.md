# Implementation Plan: Predict Match

**Branch**: `001-predict-match` | **Date**: 2026-06-06 | **Spec**: [spec.md](file:///Users/anibalospina/development/victoria/specs/001-predict-match/spec.md)

**Input**: Feature specification from `specs/001-predict-match/spec.md`

## Summary
The Football Pool Prediction Assistant is an interactive Streamlit application designed to predict the outcome and exact scoreline of a one-on-one match between two selected international teams. The backend implements a Poisson Distribution model using Scipy, combined with an exponential temporal decay function and match-type weighting (penalizing friendlies, prioritizing tournament matches). High-performance data processing is built using Polars LazyFrames, isolated and cached using `@st.cache_data` to ensure low memory footprint on Streamlit Community Cloud.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Streamlit, Polars, Scipy, Pytest

**Storage**: Local CSV match dataset (`results.csv`)

**Testing**: Pytest

**Target Platform**: Streamlit Community Cloud

**Project Type**: Streamlit Web Application

**Performance Goals**: Suggested winner and exact scoreline rendered on the UI within 3 seconds of triggering calculation.

**Constraints**: Memory footprint under 1GB (Streamlit free tier threshold) via Polars LazyFrames and caching.

**Scale/Scope**: ~45,000+ historical international match records.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (One-on-One Match Focus)**: Passed. The scope is strictly limited to one-on-one match setup; no bulk uploads or league calculators.
- **Principle II (Memory-Efficient Polars & No Pandas)**: Passed. Only Polars (LazyFrames) is utilized for data ingestion; Pandas is not used.
- **Principle III (Poisson Distribution with Temporal Decay)**: Passed. Modeling uses Poisson with exponential temporal decay (1-year half-life).
- **Principle IV (Separation of Concerns)**: Passed. Split into `utils.py` (Data), `predictor.py` (Analytics/Poisson), and `app.py` (Presentation).
- **Principle V (Rigorous Quality & Type Hinting)**: Passed. Full type hinting, pure analytical functions, and unit tests via `pytest` are enforced.

## Project Structure

### Documentation (this feature)

```text
specs/001-predict-match/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── ui-contract.md   # UI interface contract
└── checklists/
    └── requirements.md  # Quality checklist
```

### Source Code (repository root)

```text
src/
├── predictor.py        # Analytics layer (pure Poisson calculations)
└── utils.py            # Data layer (Polars data loading, caching)

tests/
└── test_predictor.py   # Unit tests for the prediction engine

app.py                  # Streamlit application entry point
requirements.txt        # Project dependencies
```

**Structure Decision**: Single project layout. Streamlit app entry point is `app.py` at the root, with pure analytical logic and helper scripts placed in the `src/` directory.

## Complexity Tracking

*No violations identified. Code adheres strictly to all constitutional principles.*
