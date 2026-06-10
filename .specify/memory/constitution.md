<!--
[SYNC IMPACT REPORT]
Version change: None (Initial Template) -> 1.0.0
Modified principles:
  - [PRINCIPLE_1_NAME] -> I. One-on-One Match Focus (Strict Scope)
  - [PRINCIPLE_2_NAME] -> II. Memory-Efficient Polars & No Pandas
  - [PRINCIPLE_3_NAME] -> III. Poisson Distribution with Temporal Decay
  - [PRINCIPLE_4_NAME] -> IV. Separation of Concerns
  - [PRINCIPLE_5_NAME] -> V. Rigorous Quality & Type Hinting
Added sections:
  - Performance & UI Efficiency (replacing [SECTION_2_NAME])
  - Change Management and Compliance (replacing [SECTION_3_NAME])
Removed sections:
  - None
Templates requiring updates:
  - .specify/templates/plan-template.md (✅ aligned, no changes required)
  - .specify/templates/spec-template.md (✅ aligned, no changes required)
  - .specify/templates/tasks-template.md (✅ aligned, no changes required)
Follow-up TODOs:
  - None
-->
# Victoria Constitution

## Core Principles

### I. One-on-One Match Focus (Strict Scope)
Victoria is strictly designed and optimized for one-on-one match analysis (Team A vs Team B). No out-of-scope features (e.g., tournament simulation, league table generators, multi-match accumulator advice) may be introduced without a prior specification update.
*Rationale: Restricting the scope keeps the code focused and ensures the UI can deliver predictions quickly and cleanly.*

### II. Memory-Efficient Polars & No Pandas
The project mandates Python `polars` for all data handling and manipulation, leveraging LazyFrames and lazy evaluation wherever possible. The use of Pandas is strictly forbidden. To ensure the application runs within the memory constraints of the free Streamlit Community Cloud tier, all data loading and preprocessing must be optimized.
*Rationale: Streamlit Community Cloud offers limited memory resources. Polars LazyFrames optimize query execution plans and minimize memory footprint, avoiding out-of-memory crashes.*

### III. Poisson Distribution with Temporal Decay
All prediction calculations must utilize a Poisson Distribution model combined with an exponential temporal decay function to weight recent match results higher than older ones.
*Rationale: The Poisson Distribution is a proven, statistically sound model for discrete goal scoring, and temporal decay ensures predictions reflect current team form.*

### IV. Separation of Concerns
Development must maintain a strict separation of concerns among the following three architectural layers:
1. **Data Layer**: Responsible for data ingestion, cleaning, and preprocessing using Polars.
2. **Analytics Layer**: Contains the statistical calculations and Poisson modeling. All analytical functions must be pure functions.
3. **Presentation Layer**: Streamlit-based UI and user interactions.
*Rationale: Separation of concerns guarantees that mathematical code can be tested independently of Streamlit's runtime, improving testability and modularity.*

### V. Rigorous Quality & Type Hinting
Full Python type hinting is required for all function signatures across all layers. All analytical computations must be implemented as pure functions without side effects. Unit testing via `pytest` must cover all data processing and prediction logic.
*Rationale: Type hinting and pure functions ensure code correctness and readability, while unit tests prevent regressions in prediction calculations.*

## Performance & UI Efficiency
To support smooth, responsive operation on the Streamlit Community Cloud:
- The application must leverage Streamlit's `@st.cache_data` to cache processed data, minimizing expensive disk reads and recalculations.
- The UI must be highly optimized, enabling a user to comprehend the suggested winner and exact score prediction within three seconds of interaction.
*Rationale: Caching and minimal rendering overhead ensure a premium user experience and avoid unnecessary resource utilization.*

## Change Management and Compliance
Any code introduced that violates memory constraints, imports unauthorized libraries (such as Pandas), or implements features outside of the one-on-one match scope without a prior specification update must be rejected.
- All code changes must be validated against unit tests before merge/deployment.
- Dependencies must be kept minimal and strictly conform to the approved Python stack.
*Rationale: Strict gates preserve application performance and stability on the free hosting tier.*

## Governance
This Constitution is the supreme authority governing all technical decisions, architecture, and libraries in the Victoria project.
- **Amendments**: Any change or amendment to these principles requires a formal update to this document, including a version increment.
- **Versioning Policy**: We use semantic versioning (MAJOR.MINOR.PATCH) for the Constitution version.
  - MAJOR: Removal or weakening of a core constraint or principle.
  - MINOR: Addition of a new principle or constraint, or material expansion of existing guidelines.
  - PATCH: Clarifications, formatting fixes, or non-semantic refinements.
- **Compliance Review**: All proposed code changes must be checked against the active principles in this Constitution.
- **Guidance File**: Developer guidelines are tracked in the coding agent context [AGENTS.md](file:///Users/anibalospina/development/victoria/AGENTS.md).

**Version**: 1.0.0 | **Ratified**: 2026-06-06 | **Last Amended**: 2026-06-06
