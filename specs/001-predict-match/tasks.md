# Tasks: Predict Match

**Input**: Design documents from `/specs/001-predict-match/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Analytical engine calculations require unit tests via `pytest` to guarantee correctness and predictability.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- Paths assume single project: `src/`, `tests/` at repository root.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment setup

- [X] T001 Create project directories src/ and tests/
- [X] T002 Create project dependencies file requirements.txt
- [X] T003 [P] Configure local pytest settings in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ingestion of matches and regional confederation data using Polars LazyFrames

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create src/utils.py to load and preprocess historical match dataset results.csv using Polars LazyFrames and @st.cache_data
- [X] T005 Implement regional confederation mapping and base fallback data in src/utils.py
- [X] T006 Initialize unit test file tests/test_predictor.py with mock match data fixtures

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Match Selection & Outcome View (Priority: P1) 🎯 MVP

**Goal**: Select two international teams and view winner predictions and exact scorelines within 3 seconds.

**Independent Test**: Run Streamlit and select Brazil vs Argentina. Click Calculate Prediction and verify winner and score are displayed within 3 seconds. Repeat with Japan vs Senegal (no direct head-to-head records) and check fallback.

### Tests for User Story 1 (TDD Approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T007 [P] [US1] Implement unit tests in tests/test_predictor.py for Poisson prediction, temporal decay, host advantage, and match weights
- [X] T008 [P] [US1] Implement unit tests in tests/test_predictor.py for regional averages fallback logic

### Implementation for User Story 1

- [X] T009 [US1] Implement pure analytical prediction engine in src/predictor.py with type hinting, calculating team strength with temporal decay and match weights
- [X] T010 [US1] Implement regional averages fallback calculation in src/predictor.py when head-to-head records are empty
- [X] T011 [US1] Create app.py Streamlit user interface featuring team selection dropdowns and host country checkboxes
- [X] T012 [US1] Integrate app.py with src/predictor.py to trigger prediction and display suggested winner and exact scoreline
- [X] T013 [US1] Implement team identity validation and error warnings in app.py to prevent self-match calculation

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Alternative Scores Distribution Matrix (Priority: P2)

**Goal**: Display alternative score probability distribution matrix.

**Independent Test**: Verify matrix grid renders next to standard prediction outputs, illustrating probability values for scorelines up to 4-4.

### Tests for User Story 2 ⚠️

- [X] T014 [P] [US2] Implement unit tests in tests/test_predictor.py for score matrix calculations

### Implementation for User Story 2

- [X] T015 [US2] Implement the score matrix probability calculation function in src/predictor.py
- [X] T016 [US2] Update app.py to render the alternative scorelines probability matrix as a visual grid

**Checkpoint**: User Stories 1 AND 2 should both work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Optimizations, verification, and code quality

- [X] T017 Validate memory constraints and profile Polars LazyFrame query plans for optimal efficiency
- [X] T018 Run type checks and enforce strict separation of concerns across src/predictor.py, src/utils.py, and app.py
- [X] T019 Execute complete pytest test suite in tests/test_predictor.py and ensure 100% pass rate
- [X] T020 Run end-to-end user validations as outlined in specs/001-predict-match/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion. Blocks User Stories.
- **User Stories (Phases 3-4)**: Depend on Foundational completion. US2 can run after US1 or in parallel for modular tasks.
- **Polish (Phase 5)**: Depends on all user stories being complete.

### Parallel Opportunities

- All Setup tasks (T001-T003) can be initialized together.
- Test-writing tasks (T007, T008, T014) can be prepared in parallel once base structures are established.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (blocking prerequisite)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Verify prediction and fallback operations.
5. Add Phase 4 (Alternative score matrix) as a feature increment.
