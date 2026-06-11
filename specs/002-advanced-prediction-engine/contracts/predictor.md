# Analytics Layer Contracts

This document defines the Python API contracts for the analytics layer functions in `src/predictor.py` and `src/utils.py`.

## Data Preprocessing Contract

### `compute_federation_strength_indices`
Computes the Federation Strength Index (FSI) for all confederations using historical inter-confederation World Cup matches.

* **Signature**:
  ```python
  def compute_federation_strength_indices(
      df_cached: pl.DataFrame,
      conf_map: Dict[str, str]
  ) -> Dict[str, float]:
  ```
* **Inputs**:
  * `df_cached`: Loaded historical matches DataFrame.
  * `conf_map`: Mapping of teams to confederations.
* **Returns**:
  * `Dict[str, float]`: Keys are confederation names (`UEFA`, `CONMEBOL`, etc.), values are the computed FSI floats.
* **Exceptions**:
  * None. If a confederation has no matches, it defaults to `1.0`.

---

## Prediction Calculation Contract

### `calculate_prediction`
Performs the hybrid expected goals calculations, FSI scaling, and Poisson simulations.

* **Signature**:
  ```python
  def calculate_prediction(
      team_a: str,
      team_b: str,
      team_a_host: bool,
      team_b_host: bool,
      df_cached: pl.DataFrame,
      conf_map: Dict[str, str],
      fsi_map: Dict[str, float]
  ) -> Dict[str, Any]:
  ```
* **Inputs**:
  * `team_a`: String name of local team.
  * `team_b`: String name of visitor team.
  * `team_a_host`: True if Team A has home advantage.
  * `team_b_host`: True if Team B has home advantage.
  * `df_cached`: Loaded matches DataFrame.
  * `conf_map`: Confederation map dict.
  * `fsi_map`: Precomputed FSI values.
* **Returns**:
  * `Dict[str, Any]` containing:
    * `"team_a"`: `str`
    * `"team_b"`: `str`
    * `"prob_a_win"`: `float` (range $[0, 1]$)
    * `"prob_draw"`: `float` (range $[0, 1]$)
    * `"prob_b_win"`: `float` (range $[0, 1]$)
    * `"exact_score"`: `Tuple[int, int]`
    * `"score_matrix"`: `List[List[float]]` ($5 \times 5$ matrix)
    * `"fallback_used"`: `bool`
    * `"expected_goals_a"`: `float`
    * `"expected_goals_b"`: `float`
