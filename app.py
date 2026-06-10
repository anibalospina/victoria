import streamlit as st
import polars as pl
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any
from src.utils import load_historical_matches, get_unique_teams, build_confederation_map
from src.predictor import calculate_prediction, get_poisson_probabilities

# Page configuration
st.set_page_config(
    page_title="Football Pool Prediction Assistant",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom premium styling using Outfit and Inter fonts
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global style overrides */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700;
    }
    
    /* Center columns vertically */
    .stSelectbox label {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: #E2E8F0 !important;
    }
    
    .stCheckbox label {
        font-size: 0.9rem !important;
        color: #CBD5E0 !important;
    }

    /* Container for forms */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    }
    
    /* Result styling */
    .result-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 20px;
        padding: 32px;
        margin-top: 16px;
        text-align: center;
        box-shadow: 0 12px 40px 0 rgba(0, 240, 255, 0.05);
    }
    
    .outcome-title {
        font-size: 2.2rem;
        background: linear-gradient(90deg, #00F0FF, #0072FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 8px;
    }
    
    .score-display {
        font-size: 4.5rem;
        font-weight: 800;
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
        letter-spacing: 2px;
        margin: 16px 0;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #A0AEC0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* Stacked probability bar */
    .prob-bar-container {
        display: flex;
        width: 100%;
        height: 24px;
        border-radius: 12px;
        overflow: hidden;
        margin: 20px 0;
        background-color: #2D3748;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .prob-segment-a {
        height: 100%;
        background: linear-gradient(90deg, #38A169, #48BB78);
        transition: width 0.5s ease-in-out;
    }
    
    .prob-segment-draw {
        height: 100%;
        background: #718096;
        transition: width 0.5s ease-in-out;
    }
    
    .prob-segment-b {
        height: 100%;
        background: linear-gradient(90deg, #ED8936, #ED8936);
        transition: width 0.5s ease-in-out;
    }
    
    .prob-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.95rem;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# App Title & Description
st.markdown("""
<div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
    <h1 style="font-size: 3rem; background: linear-gradient(90deg, #FF4B4B, #FF8F8F); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 8px;">⚽ Football Pool Predictor</h1>
    <p style="color: #A0AEC0; font-size: 1.1rem; font-weight: 400; max-width: 650px; margin: 0 auto;">Simulate international match outcomes using a statistical Poisson engine with form decay, match importance weighting, and regional averages fallback.</p>
</div>
""", unsafe_allow_html=True)

# Ensure results.csv exists in the root path
DATASET_PATH = "results.csv"

if not os.path.exists(DATASET_PATH):
    st.error(f"⚠️ Error: Historical matches dataset (`{DATASET_PATH}`) not found in the project root directory. Please download it first.")
    st.stop()

# Initialize data and cached maps
try:
    df_cached = load_historical_matches(DATASET_PATH)
    teams = get_unique_teams(df_cached)
    conf_map = build_confederation_map(df_cached)
except Exception as e:
    st.error(f"⚠️ Error parsing or loading dataset: {e}")
    st.stop()

# Form Container
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<h3 style="margin-top: 0; color: #FFFFFF; font-size: 1.3rem; margin-bottom: 1rem;">Setup Match</h3>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Set default to Brazil if present, else first team
    default_a_idx = teams.index("Brazil") if "Brazil" in teams else 0
    team_a = st.selectbox("Team A", teams, index=default_a_idx)
    team_a_host = st.checkbox("Host Country", value=False, key="host_a")

with col2:
    # Set default to Argentina if present, else second team
    default_b_idx = teams.index("Argentina") if "Argentina" in teams else (1 if len(teams) > 1 else 0)
    team_b = st.selectbox("Team B", teams, index=default_b_idx)
    team_b_host = st.checkbox("Host Country", value=False, key="host_b")

st.markdown('</div>', unsafe_allow_html=True)

# Validation check
teams_are_identical = (team_a == team_b)

if teams_are_identical:
    st.warning("⚠️ Team A and Team B must be different countries. A team cannot play against itself.")
    calculate_disabled = True
else:
    calculate_disabled = False

# Predict Button
st.markdown('<div style="text-align: center; margin-bottom: 2rem;">', unsafe_allow_html=True)
predict_clicked = st.button("Calculate Prediction", disabled=calculate_disabled, type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

def render_matrix_html(matrix: List[List[float]], exact_score: Tuple[int, int], team_b: str) -> str:
    """
    Renders the 5x5 alternative score matrix as a beautiful HTML heat table.
    """
    max_prob = max(max(row) for row in matrix)
    
    html = """<style>
.matrix-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 6px;
    font-family: 'Inter', sans-serif;
    margin-top: 1rem;
}
.matrix-header {
    text-align: center;
    font-weight: 600;
    color: #A0AEC0;
    font-size: 0.85rem;
    padding: 8px;
}
.matrix-row-label {
    font-weight: 600;
    color: #A0AEC0;
    font-size: 0.85rem;
    text-align: right;
    padding-right: 12px;
    width: 80px;
}
.matrix-cell {
    text-align: center;
    border-radius: 8px;
    padding: 10px 4px;
    font-size: 0.9rem;
    font-weight: 600;
    color: #FFFFFF;
    transition: all 0.2s ease;
    position: relative;
}
.matrix-cell:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    z-index: 10;
}
.highlight-cell {
    border: 2px solid #00F0FF !important;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
}
</style>
<table class="matrix-table">
<tr>
    <th></th>
    <th colspan="5" class="matrix-header" style="border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;">Away Team Goals ({team_b})</th>
</tr>
<tr>
    <th class="matrix-header" style="text-align: right; padding-right: 12px; font-size: 0.75rem;">Home \\ Away</th>
    <th class="matrix-header">0</th>
    <th class="matrix-header">1</th>
    <th class="matrix-header">2</th>
    <th class="matrix-header">3</th>
    <th class="matrix-header">4</th>
</tr>"""
    html = html.replace("{team_b}", team_b)
    for i in range(5):
        html += f"<tr><td class='matrix-row-label'>{i}</td>"
        for j in range(5):
            prob = matrix[i][j]
            intensity = prob / max_prob if max_prob > 0 else 0
            
            # Map to dark gradient blue/purple
            r = int(25 + intensity * 90)   # 25 to 115
            g = int(35 + intensity * 40)   # 35 to 75
            b = int(60 + intensity * 160)  # 60 to 220
            bg_color = f"rgb({r}, {g}, {b})"
            
            is_best = (i == exact_score[0] and j == exact_score[1])
            cell_class = "matrix-cell highlight-cell" if is_best else "matrix-cell"
            
            prob_percent = f"{prob*100:.1f}%"
            html += f"""<td class="{cell_class}" style="background-color: {bg_color}; border: 1px solid rgba(255,255,255,0.04); cursor: default;" title="Score {i}-{j}: {prob_percent}">
<div style="font-size: 0.85rem; font-weight: 700;">{i} - {j}</div>
<div style="font-size: 0.75rem; opacity: 0.8; margin-top: 1px;">{prob_percent}</div>
</td>"""
        html += "</tr>"
    html += "</table>"
    return html

# Result Display
if predict_clicked and not calculate_disabled:
    # Run simulation
    with st.spinner("Simulating match using Poisson Distribution..."):
        import time
        start_time = time.time()
        
        # Calculate prediction parameters
        res = calculate_prediction(
            team_a, team_b, team_a_host, team_b_host, df_cached, conf_map
        )
        
        duration = time.time() - start_time
        
    # Extract prediction outputs
    prob_a = res["prob_a_win"]
    prob_draw = res["prob_draw"]
    prob_b = res["prob_b_win"]
    score_a, score_b = res["exact_score"]
    
    # Determine the suggested outcome string
    if prob_a > prob_b and prob_a > prob_draw:
        winner_text = f"{team_a} Wins"
    elif prob_b > prob_a and prob_b > prob_draw:
        winner_text = f"{team_b} Wins"
    else:
        winner_text = "Draw"
        
    # Stacked bar calculations
    w_a = max(10.0, prob_a * 100)
    w_d = max(10.0, prob_draw * 100)
    w_b = max(10.0, prob_b * 100)
    # Re-normalize to fit 100% exactly
    total_w = w_a + w_d + w_b
    w_a = (w_a / total_w) * 100
    w_d = (w_d / total_w) * 100
    w_b = (w_b / total_w) * 100

    # Display main prediction card
    st.markdown(f"""
<div class="result-card">
    <div class="stat-label">Suggested Winner</div>
    <div class="outcome-title">{winner_text}</div>
    <div class="stat-label" style="margin-top: 16px;">Most Probable Final Scoreline</div>
    <div class="score-display">{score_a} - {score_b}</div>
    <div style="margin-top: 24px;">
        <div class="prob-labels">
            <span>🟢 {team_a}: {prob_a*100:.1f}%</span>
            <span>⚪ Draw: {prob_draw*100:.1f}%</span>
            <span>🟠 {team_b}: {prob_b*100:.1f}%</span>
        </div>
        <div class="prob-bar-container">
            <div class="prob-segment-a" style="width: {w_a}%;" title="{team_a} Win: {prob_a*100:.1f}%"></div>
            <div class="prob-segment-draw" style="width: {w_d}%;" title="Draw: {prob_draw*100:.1f}%"></div>
            <div class="prob-segment-b" style="width: {w_b}%;" title="{team_b} Win: {prob_b*100:.1f}%"></div>
        </div>
    </div>
    <div style="display: flex; justify-content: space-around; margin-top: 16px; font-size: 0.85rem; color: #718096; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 12px;">
        <span>Calculation time: {duration:.3f}s</span>
        <span>Fallback used: {"Yes (Regional Averages)" if res["fallback_used"] else "No (Head-to-Head)"}</span>
    </div>
</div>
""", unsafe_allow_html=True)
    
    # Render Alternative Scores Matrix Section
    st.markdown("<h3 style='margin-top: 2rem; color: #FFFFFF; font-size: 1.3rem; margin-bottom: 0.5rem;'>Alternative Score Probability Matrix</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #A0AEC0; font-size: 0.9rem; margin-bottom: 1.5rem;'>The heat map below visualizes the probability distribution of alternative scorelines up to 4-4. The neon cyan highlighted cell indicates the most likely scoreline.</p>", unsafe_allow_html=True)
    
    matrix_html = render_matrix_html(res["score_matrix"], res["exact_score"], team_b)
    st.markdown(matrix_html, unsafe_allow_html=True)

    # Expected goals breakdown
    st.markdown(f"""
<div style="margin-top: 1.5rem; padding: 12px 16px; background: rgba(255,255,255,0.02); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); font-size: 0.85rem; color: #718096; text-align: center;">
    📊 <strong>Expected Goals (Lambda):</strong> {team_a}: {res["expected_goals_a"]:.2f} goals &nbsp;|&nbsp; {team_b}: {res["expected_goals_b"]:.2f} goals
</div>
""", unsafe_allow_html=True)
