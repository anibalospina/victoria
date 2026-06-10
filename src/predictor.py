import polars as pl
import numpy as np
from scipy.stats import poisson
from datetime import datetime
from typing import Dict, Tuple, List, Any

def get_team_stats(team: str, df_lazy: pl.LazyFrame, ref_date: datetime) -> Tuple[float, float, float]:
    """
    Compute overall weighted average goals scored and conceded by a team.
    """
    matches = df_lazy.filter((pl.col("home_team") == team) | (pl.col("away_team") == team))
    
    days_ago = (ref_date - pl.col("date")).dt.total_days()
    decay_weight = (-0.0019 * days_ago).exp()
    
    importance_weight = pl.when(pl.col("tournament").str.to_lowercase() == "friendly") \
        .then(0.5) \
        .when(pl.col("tournament").str.to_lowercase().str.contains("cup|qualif|championship|nations league|copa|euro")) \
        .then(1.5) \
        .otherwise(1.0)
        
    weight = decay_weight * importance_weight
    
    processed = matches.with_columns([
        pl.when(pl.col("home_team") == team).then(pl.col("home_score")).otherwise(pl.col("away_score")).alias("goals_scored"),
        pl.when(pl.col("home_team") == team).then(pl.col("away_score")).otherwise(pl.col("home_score")).alias("goals_conceded"),
        weight.alias("weight")
    ]).collect()
    
    total_w = processed["weight"].sum()
    if total_w > 1e-5:
        avg_scored = (processed["goals_scored"] * processed["weight"]).sum() / total_w
        avg_conceded = (processed["goals_conceded"] * processed["weight"]).sum() / total_w
        return float(avg_scored), float(avg_conceded), float(total_w)
    else:
        return 1.0, 1.0, 0.0

def get_confederation_stats(conf: str, df_lazy: pl.LazyFrame, conf_map: Dict[str, str], ref_date: datetime) -> Tuple[float, float]:
    """
    Compute average weighted goals scored and conceded by all teams of a confederation.
    """
    conf_teams = [t for t, c in conf_map.items() if c == conf]
    if not conf_teams:
        return 1.2, 1.2
        
    matches = df_lazy.filter(pl.col("home_team").is_in(conf_teams) | pl.col("away_team").is_in(conf_teams))
    
    days_ago = (ref_date - pl.col("date")).dt.total_days()
    decay_weight = (-0.0019 * days_ago).exp()
    
    importance_weight = pl.when(pl.col("tournament").str.to_lowercase() == "friendly") \
        .then(0.5) \
        .when(pl.col("tournament").str.to_lowercase().str.contains("cup|qualif|championship|nations league|copa|euro")) \
        .then(1.5) \
        .otherwise(1.0)
        
    weight = decay_weight * importance_weight
    
    home_matches = matches.filter(pl.col("home_team").is_in(conf_teams)).select([
        pl.col("home_score").alias("goals_scored"),
        pl.col("away_score").alias("goals_conceded"),
        weight.alias("weight")
    ])
    away_matches = matches.filter(pl.col("away_team").is_in(conf_teams)).select([
        pl.col("away_score").alias("goals_scored"),
        pl.col("home_score").alias("goals_conceded"),
        weight.alias("weight")
    ])
    
    union_df = pl.concat([home_matches, away_matches]).collect()
    
    total_w = union_df["weight"].sum()
    if total_w > 1e-5:
        avg_scored = (union_df["goals_scored"] * union_df["weight"]).sum() / total_w
        avg_conceded = (union_df["goals_conceded"] * union_df["weight"]).sum() / total_w
        return float(avg_scored), float(avg_conceded)
    else:
        return 1.2, 1.2

def get_conf_vs_conf_avg_goals(conf_a: str, conf_b: str, df_lazy: pl.LazyFrame, conf_map: Dict[str, str], ref_date: datetime) -> float:
    """
    Compute average weighted goals scored by teams of conf_a against teams of conf_b.
    """
    teams_a = [t for t, c in conf_map.items() if c == conf_a]
    teams_b = [t for t, c in conf_map.items() if c == conf_b]
    
    if not teams_a or not teams_b:
        return 1.35
        
    matches = df_lazy.filter(
        ((pl.col("home_team").is_in(teams_a)) & (pl.col("away_team").is_in(teams_b))) |
        ((pl.col("home_team").is_in(teams_b)) & (pl.col("away_team").is_in(teams_a)))
    )
    
    days_ago = (ref_date - pl.col("date")).dt.total_days()
    decay_weight = (-0.0019 * days_ago).exp()
    
    importance_weight = pl.when(pl.col("tournament").str.to_lowercase() == "friendly") \
        .then(0.5) \
        .when(pl.col("tournament").str.to_lowercase().str.contains("cup|qualif|championship|nations league|copa|euro")) \
        .then(1.5) \
        .otherwise(1.0)
        
    weight = decay_weight * importance_weight
    
    processed = matches.with_columns([
        pl.when(pl.col("home_team").is_in(teams_a)).then(pl.col("home_score")).otherwise(pl.col("away_score")).alias("goals_a"),
        weight.alias("weight")
    ]).collect()
    
    total_w = processed["weight"].sum()
    if total_w > 1e-5:
        avg_goals = (processed["goals_a"] * processed["weight"]).sum() / total_w
        return float(avg_goals)
    else:
        return 1.35

def get_poisson_probabilities(lambda_a: float, lambda_b: float) -> Tuple[float, float, float, Tuple[int, int], List[List[float]]]:
    """
    Calculate Poisson probabilities for win/draw/loss and return the score distribution matrix.
    """
    max_goals = 10
    prob_matrix = np.zeros((max_goals + 1, max_goals + 1))
    
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob_matrix[i, j] = poisson.pmf(i, lambda_a) * poisson.pmf(j, lambda_b)
            
    # Calculate outcomes
    a_win_sum = 0.0
    draw_sum = 0.0
    b_win_sum = 0.0
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            if i > j:
                a_win_sum += prob_matrix[i, j]
            elif i == j:
                draw_sum += prob_matrix[i, j]
            else:
                b_win_sum += prob_matrix[i, j]
                
    total_outcome_prob = a_win_sum + draw_sum + b_win_sum
    if total_outcome_prob > 0:
        prob_a_win = a_win_sum / total_outcome_prob
        prob_draw = draw_sum / total_outcome_prob
        prob_b_win = b_win_sum / total_outcome_prob
    else:
        prob_a_win, prob_draw, prob_b_win = 0.333, 0.333, 0.333
        
    # Find most probable exact scoreline
    max_idx = np.unravel_index(np.argmax(prob_matrix), prob_matrix.shape)
    exact_score = (int(max_idx[0]), int(max_idx[1]))
    
    # Alternative scoreline matrix up to 4-4
    matrix_limit = 5
    score_matrix = []
    for i in range(matrix_limit):
        row = []
        for j in range(matrix_limit):
            row.append(float(prob_matrix[i, j]))
        score_matrix.append(row)
        
    return prob_a_win, prob_draw, prob_b_win, exact_score, score_matrix

def calculate_prediction(
    team_a: str,
    team_b: str,
    team_a_host: bool,
    team_b_host: bool,
    df_cached: pl.DataFrame,
    conf_map: Dict[str, str]
) -> Dict[str, Any]:
    """
    Predict the outcome of a match between team_a and team_b.
    Uses Poisson Distribution with temporal decay and match weights.
    Falls back to regional averages if there is no direct head-to-head history.
    """
    df_lazy = df_cached.lazy()
    
    # Use max date in dataset as reference date for temporal decay
    ref_date = df_cached["date"].max()
    
    # Calculate temporal decay and importance weights
    days_ago = (ref_date - pl.col("date")).dt.total_days()
    decay_weight = (-0.0019 * days_ago).exp()
    importance_weight = pl.when(pl.col("tournament").str.to_lowercase() == "friendly") \
        .then(0.5) \
        .when(pl.col("tournament").str.to_lowercase().str.contains("cup|qualif|championship|nations league|copa|euro")) \
        .then(1.5) \
        .otherwise(1.0)
    weight = decay_weight * importance_weight
    
    # 1. Look for direct head-to-head matches
    h2h = df_lazy.filter(
        ((pl.col("home_team") == team_a) & (pl.col("away_team") == team_b)) |
        ((pl.col("home_team") == team_b) & (pl.col("away_team") == team_a))
    )
    
    h2h_processed = h2h.with_columns([
        pl.when(pl.col("home_team") == team_a).then(pl.col("home_score")).otherwise(pl.col("away_score")).alias("goals_a"),
        pl.when(pl.col("home_team") == team_a).then(pl.col("away_score")).otherwise(pl.col("home_score")).alias("goals_b"),
        weight.alias("weight")
    ]).collect()
    
    total_weight = h2h_processed["weight"].sum()
    
    # Calculate general baseline stats for both teams
    avg_scored_a, avg_conceded_a, _ = get_team_stats(team_a, df_lazy, ref_date)
    avg_scored_b, avg_conceded_b, _ = get_team_stats(team_b, df_lazy, ref_date)
    
    # Global average goals in the dataset to act as scaling baseline
    global_avg_goals = max(float((df_cached["home_score"].mean() + df_cached["away_score"].mean()) / 2.0), 1.0)
    
    # General baseline expected goals (overall recent performance form)
    lambda_a_gen = avg_scored_a * (avg_conceded_b / global_avg_goals)
    lambda_b_gen = avg_scored_b * (avg_conceded_a / global_avg_goals)
    
    # If direct head-to-head exists
    if total_weight > 1e-3:
        lambda_a_h2h = (h2h_processed["goals_a"] * h2h_processed["weight"]).sum() / total_weight
        lambda_b_h2h = (h2h_processed["goals_b"] * h2h_processed["weight"]).sum() / total_weight
        
        # Hybrid model: 30% H2H, 70% overall recent performance
        lambda_a = 0.3 * lambda_a_h2h + 0.7 * lambda_a_gen
        lambda_b = 0.3 * lambda_b_h2h + 0.7 * lambda_b_gen
        fallback_used = False
    else:
        # 2. Regional averages fallback
        conf_a = conf_map.get(team_a, "UEFA")
        conf_b = conf_map.get(team_b, "UEFA")
        
        # Get confederation stats
        conf_scored_a, conf_conceded_a = get_confederation_stats(conf_a, df_lazy, conf_map, ref_date)
        conf_scored_b, conf_conceded_b = get_confederation_stats(conf_b, df_lazy, conf_map, ref_date)
        
        # Calculate strengths relative to confederation
        attack_strength_a = avg_scored_a / max(conf_scored_a, 1e-3)
        defense_strength_a = avg_conceded_a / max(conf_conceded_a, 1e-3)
        
        attack_strength_b = avg_scored_b / max(conf_scored_b, 1e-3)
        defense_strength_b = avg_conceded_b / max(conf_conceded_b, 1e-3)
        
        # Average goals scored by conf_a against conf_b
        mu_a_to_b = get_conf_vs_conf_avg_goals(conf_a, conf_b, df_lazy, conf_map, ref_date)
        mu_b_to_a = get_conf_vs_conf_avg_goals(conf_b, conf_a, df_lazy, conf_map, ref_date)
        
        lambda_a = attack_strength_a * defense_strength_b * mu_a_to_b
        lambda_b = attack_strength_b * defense_strength_a * mu_b_to_a
        fallback_used = True
        
    # Ensure expected goals are non-negative and not excessively small/large
    lambda_a = max(float(lambda_a), 0.05)
    lambda_b = max(float(lambda_b), 0.05)
    
    # 3. Apply host advantage multiplier (1.2x)
    if team_a_host:
        lambda_a *= 1.2
    if team_b_host:
        lambda_b *= 1.2
        
    # Calculate Poisson outcome probabilities
    prob_a_win, prob_draw, prob_b_win, exact_score, score_matrix = get_poisson_probabilities(lambda_a, lambda_b)
    
    return {
        "team_a": team_a,
        "team_b": team_b,
        "prob_a_win": prob_a_win,
        "prob_draw": prob_draw,
        "prob_b_win": prob_b_win,
        "exact_score": exact_score,
        "score_matrix": score_matrix,
        "fallback_used": fallback_used,
        "expected_goals_a": lambda_a,
        "expected_goals_b": lambda_b
    }
