import pytest
import polars as pl
from datetime import datetime, timedelta
from src.utils import build_confederation_map
from src.predictor import (
    get_poisson_probabilities,
    calculate_prediction,
    get_team_stats,
    get_confederation_stats,
    get_conf_vs_conf_avg_goals
)

@pytest.fixture
def mock_dataset():
    """
    Generate a simple mock dataset of international matches for testing.
    """
    ref_date = datetime(2026, 6, 1)
    
    # Create matches
    matches = [
        # Direct Head-to-Head: Brazil vs Argentina
        {"date": ref_date - timedelta(days=30), "home_team": "Brazil", "away_team": "Argentina", "home_score": 2, "away_score": 1, "tournament": "FIFA World Cup", "neutral": False},
        {"date": ref_date - timedelta(days=400), "home_team": "Argentina", "away_team": "Brazil", "home_score": 1, "away_score": 0, "tournament": "Friendly", "neutral": False},
        
        # Brazil vs other teams
        {"date": ref_date - timedelta(days=60), "home_team": "Brazil", "away_team": "Uruguay", "home_score": 3, "away_score": 0, "tournament": "Copa América", "neutral": False},
        
        # Argentina vs other teams
        {"date": ref_date - timedelta(days=90), "home_team": "Argentina", "away_team": "Chile", "home_score": 2, "away_score": 0, "tournament": "Copa América", "neutral": False},
        
        # Japan vs Senegal (No Head-to-Head)
        {"date": ref_date - timedelta(days=100), "home_team": "Japan", "away_team": "South Korea", "home_score": 1, "away_score": 0, "tournament": "AFC Asian Cup", "neutral": False},
        {"date": ref_date - timedelta(days=120), "home_team": "Senegal", "away_team": "Cameroon", "home_score": 2, "away_score": 0, "tournament": "African Cup of Nations", "neutral": False},
    ]
    
    df = pl.DataFrame(matches)
    df = df.with_columns(pl.col("date").cast(pl.Date))
    return df

@pytest.fixture
def mock_conf_map():
    return {
        "Brazil": "CONMEBOL",
        "Argentina": "CONMEBOL",
        "Uruguay": "CONMEBOL",
        "Chile": "CONMEBOL",
        "Japan": "AFC",
        "South Korea": "AFC",
        "Senegal": "CAF",
        "Cameroon": "CAF"
    }

def test_poisson_probabilities():
    """
    Test Poisson calculations for probabilities and score matrix.
    """
    prob_a, prob_draw, prob_b, score, matrix = get_poisson_probabilities(1.5, 1.0)
    
    # Probabilities should sum to approximately 1.0
    assert abs(prob_a + prob_draw + prob_b - 1.0) < 1e-4
    # Expected outcome for higher lambda should be higher win probability
    assert prob_a > prob_b
    # Matrix dimensions should be 5x5 (up to 4-4)
    assert len(matrix) == 5
    assert len(matrix[0]) == 5
    
    # Verify values inside matrix are valid probabilities
    for row in matrix:
        for val in row:
            assert 0.0 <= val <= 1.0

def test_host_advantage(mock_dataset, mock_conf_map):
    """
    Test that host country advantage increases expected goals.
    """
    # Without host advantage
    pred_neutral = calculate_prediction(
        "Brazil", "Argentina", False, False, mock_dataset, mock_conf_map
    )
    
    # With Brazil as host
    pred_host = calculate_prediction(
        "Brazil", "Argentina", True, False, mock_dataset, mock_conf_map
    )
    
    assert pred_host["expected_goals_a"] > pred_neutral["expected_goals_a"]
    assert pred_host["prob_a_win"] > pred_neutral["prob_a_win"]

def test_fallback_logic(mock_dataset, mock_conf_map):
    """
    Test that fallback logic is triggered for teams with no H2H history.
    """
    # Japan vs Senegal have no H2H matches in mock_dataset
    pred = calculate_prediction(
        "Japan", "Senegal", False, False, mock_dataset, mock_conf_map
    )
    
    assert pred["fallback_used"] is True
    # Should resolve without errors
    assert pred["expected_goals_a"] > 0
    assert pred["expected_goals_b"] > 0
    assert abs(pred["prob_a_win"] + pred["prob_draw"] + pred["prob_b_win"] - 1.0) < 1e-4

def test_temporal_decay_and_weights(mock_dataset, mock_conf_map):
    """
    Test that temporal decay and match type weights are applied correctly.
    """
    ref_date = mock_dataset["date"].max()
    
    # Test that get_team_stats correctly returns stats
    avg_s, avg_c, w = get_team_stats("Brazil", mock_dataset.lazy(), ref_date)
    assert avg_s > 0
    assert avg_c >= 0
    assert w > 0

    # Test that get_confederation_stats returns valid metrics
    avg_s_conf, avg_c_conf = get_confederation_stats("CONMEBOL", mock_dataset.lazy(), mock_conf_map, ref_date)
    assert avg_s_conf > 0
    assert avg_c_conf > 0
