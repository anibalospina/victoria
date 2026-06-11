# Implementation Plan: Advanced Weighted Prediction Engine

**Branch**: `002-advanced-prediction-engine` | **Date**: 2026-06-10 | **Spec**: [spec.md](file:///Users/anibalospina/development/victoria/specs/002-advanced-prediction-engine/spec.md)

**Input**: Feature specification from `/specs/002-advanced-prediction-engine/spec.md`

## Summary

The Advanced Weighted Prediction Engine improves prediction accuracy and eliminates regional competition bias by implementing a 30% Head-to-Head (H2H) and 70% recent form hybrid weight model, limiting team form to the last 24 months with a 1-year half-life temporal decay, and calibrating rating comparisons using a dynamically computed Federation Strength Index (FSI) derived from inter-confederation World Cup matches.

## Technical Context

**Language/Version**: Python 3.11

**Primary Dependencies**: `polars`, `numpy`, `scipy`, `streamlit`

**Storage**: Flat CSV file (`results.csv`) read using Polars

**Testing**: `pytest`

**Target Platform**: Streamlit Community Cloud (Linux)

**Project Type**: Web application

**Performance Goals**: Computation and prediction UI rendering completed in < 3 seconds

**Constraints**: < 1GB memory limit, strict no-Pandas requirement, Lazy Polars computation

**Scale/Scope**: 1-on-1 match simulator (Team A vs Team B)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. One-on-One Match Focus (Strict Scope)**: ✅ Compliant. No tournament simulation or multi-match features are added.
- **II. Memory-Efficient Polars & No Pandas**: ✅ Compliant. The project exclusively uses `polars` LazyFrames and avoids `pandas` entirely.
- **III. Poisson Distribution with Temporal Decay**: ✅ Compliant. Expected goals calculations use a Poisson distribution with temporal decay and Federation Strength Index scaling.
- **IV. Separation of Concerns**: ✅ Compliant. Data, Analytics, and Presentation remain separated across `src/utils.py`, `src/predictor.py`, and `app.py`.
- **V. Rigorous Quality & Type Hinting**: ✅ Compliant. Full Python type signatures and `pytest` test suites.

## Project Structure

### Documentation (this feature)

```text
specs/002-advanced-prediction-engine/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── predictor.md     # Analytics layer API contract
└── tasks.md             # Phase 2 output (/speckit-tasks command)
```

### Source Code (repository root)

```text
src/
├── predictor.py         # Analytics layer (Poisson calculation, FSI scaling)
└── utils.py             # Data layer (dataset loading, confederation mapping, FSI calculations)

tests/
└── test_predictor.py    # Unit tests for prediction logic and FSI

app.py                   # Presentation layer (Streamlit UI)
```

**Structure Decision**: Single-project structure (Option 1) matching the existing repository layout, keeping core mathematical computations separate from UI.

## Complexity Tracking

*No violations of the Constitution identified.*
