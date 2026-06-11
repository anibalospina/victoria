# Tasks: Advanced Weighted Prediction Engine

**Input**: Design documents from `/specs/002-advanced-prediction-engine/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Unit tests are included to validate the new prediction model and Federation Strength Index (FSI) calculations.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths assume single project: `src/utils.py`, `src/predictor.py`, `tests/test_predictor.py`, `app.py` at repository root.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic verification

- [X] T001 Verify existing dependencies and project state by running pytest in tests/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Implement compute_federation_strength_indices function in src/utils.py
- [X] T003 Write unit tests for FSI calculation in tests/test_predictor.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Advanced Hybrid Prediction (Priority: P1) 🎯 MVP

**Goal**: Implement the 30/70 hybrid prediction model with 24-month recent form and H2H decay-weight shifting.

**Independent Test**: Simulate Argentina vs. Iceland. Verify that the predicted outcome is driven by recent form rather than the 2018 draw.

### Tests for User Story 1
> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T004 [P] [US1] Write unit tests for 24-month recent form and H2H decay weight shifting in tests/test_predictor.py

### Implementation for User Story 1

- [X] T005 [US1] Update calculate_prediction and get_team_stats in src/predictor.py to support 24-month recent form filtering
- [X] T006 [US1] Implement H2H decay weight shifting in calculate_prediction in src/predictor.py
- [X] T007 [US1] Update existing test calls in tests/test_predictor.py to conform to updated signatures

**Checkpoint**: User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - Federation Strength Calibration (Priority: P2)

**Goal**: Implement Federation Strength Index scaling for inter-confederation matches.

**Independent Test**: Simulate Colombia vs. Spain. Verify FSI scaling applies. Simulate Brazil vs. Argentina. Verify FSI scaling is 1.0.

### Tests for User Story 2

- [X] T008 [P] [US2] Write unit tests for FSI scaling in tests/test_predictor.py

### Implementation for User Story 2

- [X] T009 [US2] Update calculate_prediction in src/predictor.py to apply FSI scaling
- [X] T010 [US2] Update app.py to compute, cache, and pass the FSI map to calculate_prediction
- [X] T011 [US2] Verify Colombia vs Spain and Argentina vs Iceland simulation flows in app.py

**Checkpoint**: User Story 2 is fully functional and testable.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T012 Run the entire pytest test suite in tests/test_predictor.py
- [X] T013 Verify that computation and rendering takes less than 3 seconds in app.py
- [X] T014 Run the validation scenarios listed in specs/002-advanced-prediction-engine/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - User Story 1 (P1) must be implemented before User Story 2 (P2) to establish the base predictor parameters.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (US1)**: Can start after Foundational (Phase 2).
- **User Story 2 (US2)**: Can start after US1 is completed, as FSI scaling integrates with the hybrid predictor.

---

## Parallel Opportunities

- T004 [US1] and T008 [US2] (unit tests) can be written in parallel with other test files if separated.
- T005 and T006 can be implemented in parallel since they address different parts of the predictor formula.

---

## Parallel Example: User Story 1

```bash
# Developer A writes unit tests:
Task: "Write unit tests for 24-month recent form and H2H decay weight shifting in tests/test_predictor.py"

# Developer B implements recent form filtering:
Task: "Update calculate_prediction and get_team_stats in src/predictor.py to support 24-month recent form filtering"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (blocks all stories).
3. Complete Phase 3: User Story 1.
4. **STOP and VALIDATE**: Test User Story 1 (Argentina vs Iceland simulation).

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready.
2. Add User Story 1 -> Test independently -> Deploy/Demo (MVP!).
3. Add User Story 2 -> Test independently -> Deploy/Demo.
4. Complete Polish phase -> Verification complete.
