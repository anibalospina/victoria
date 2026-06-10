import polars as pl
import streamlit as st
from typing import Dict, List

# Static mapping for major countries to speed up and handle edge cases
STATIC_CONFEDERATIONS = {
    # UEFA
    "Albania": "UEFA", "Andorra": "UEFA", "Armenia": "UEFA", "Austria": "UEFA", "Azerbaijan": "UEFA",
    "Belarus": "UEFA", "Belgium": "UEFA", "Bosnia and Herzegovina": "UEFA", "Bulgaria": "UEFA",
    "Croatia": "UEFA", "Cyprus": "UEFA", "Czech Republic": "UEFA", "Czechoslovakia": "UEFA", "Denmark": "UEFA",
    "England": "UEFA", "Estonia": "UEFA", "Faroe Islands": "UEFA", "Finland": "UEFA", "France": "UEFA",
    "Georgia": "UEFA", "Germany": "UEFA", "Gibraltar": "UEFA", "Greece": "UEFA", "Hungary": "UEFA",
    "Iceland": "UEFA", "Israel": "UEFA", "Italy": "UEFA", "Kazakhstan": "UEFA", "Kosovo": "UEFA",
    "Latvia": "UEFA", "Liechtenstein": "UEFA", "Lithuania": "UEFA", "Luxembourg": "UEFA", "Malta": "UEFA",
    "Moldova": "UEFA", "Montenegro": "UEFA", "Netherlands": "UEFA", "North Macedonia": "UEFA", "Northern Ireland": "UEFA",
    "Norway": "UEFA", "Poland": "UEFA", "Portugal": "UEFA", "Republic of Ireland": "UEFA", "Romania": "UEFA",
    "Russia": "UEFA", "San Marino": "UEFA", "Scotland": "UEFA", "Serbia": "UEFA", "Slovakia": "UEFA",
    "Slovenia": "UEFA", "Spain": "UEFA", "Sweden": "UEFA", "Switzerland": "UEFA", "Turkey": "UEFA",
    "Ukraine": "UEFA", "Wales": "UEFA", "Yugoslavia": "UEFA", "Soviet Union": "UEFA", "German DR": "UEFA",
    "Russia": "UEFA",
    # CONMEBOL
    "Argentina": "CONMEBOL", "Bolivia": "CONMEBOL", "Brazil": "CONMEBOL", "Chile": "CONMEBOL",
    "Colombia": "CONMEBOL", "Ecuador": "CONMEBOL", "Paraguay": "CONMEBOL", "Peru": "CONMEBOL",
    "Uruguay": "CONMEBOL", "Venezuela": "CONMEBOL",
    # CONCACAF
    "Anguilla": "CONCACAF", "Antigua and Barbuda": "CONCACAF", "Aruba": "CONCACAF", "Bahamas": "CONCACAF",
    "Barbados": "CONCACAF", "Belize": "CONCACAF", "Bermuda": "CONCACAF", "British Virgin Islands": "CONCACAF",
    "Canada": "CONCACAF", "Cayman Islands": "CONCACAF", "Costa Rica": "CONCACAF", "Cuba": "CONCACAF",
    "Curaçao": "CONCACAF", "Dominica": "CONCACAF", "Dominican Republic": "CONCACAF", "El Salvador": "CONCACAF",
    "Grenada": "CONCACAF", "Guadeloupe": "CONCACAF", "Guatemala": "CONCACAF", "Guyana": "CONCACAF",
    "Haiti": "CONCACAF", "Honduras": "CONCACAF", "Jamaica": "CONCACAF", "Martinique": "CONCACAF",
    "Mexico": "CONCACAF", "Montserrat": "CONCACAF", "Nicaragua": "CONCACAF", "Panama": "CONCACAF",
    "Puerto Rico": "CONCACAF", "Saint Kitts and Nevis": "CONCACAF", "Saint Lucia": "CONCACAF",
    "Saint Vincent and the Grenadines": "CONCACAF", "Suriname": "CONCACAF", "Trinidad and Tobago": "CONCACAF",
    "Turks and Caicos Islands": "CONCACAF", "United States": "CONCACAF", "US Virgin Islands": "CONCACAF",
    # CAF
    "Algeria": "CAF", "Angola": "CAF", "Benin": "CAF", "Botswana": "CAF", "Burkina Faso": "CAF",
    "Burundi": "CAF", "Cameroon": "CAF", "Cape Verde": "CAF", "Central African Republic": "CAF", "Chad": "CAF",
    "Comoros": "CAF", "Congo": "CAF", "DR Congo": "CAF", "Djibouti": "CAF", "Egypt": "CAF",
    "Equatorial Guinea": "CAF", "Eritrea": "CAF", "Eswatini": "CAF", "Ethiopia": "CAF", "Gabon": "CAF",
    "Gambia": "CAF", "Ghana": "CAF", "Guinea": "CAF", "Guinea-Bissau": "CAF", "Ivory Coast": "CAF",
    "Kenya": "CAF", "Lesotho": "CAF", "Liberia": "CAF", "Libya": "CAF", "Madagascar": "CAF",
    "Malawi": "CAF", "Mali": "CAF", "Mauritania": "CAF", "Mauritius": "CAF", "Morocco": "CAF",
    "Mozambique": "CAF", "Namibia": "CAF", "Niger": "CAF", "Nigeria": "CAF", "Rwanda": "CAF",
    "São Tomé and Príncipe": "CAF", "Senegal": "CAF", "Seychelles": "CAF", "Sierra Leone": "CAF",
    "Somalia": "CAF", "South Africa": "CAF", "South Sudan": "CAF", "Sudan": "CAF", "Tanzania": "CAF",
    "Togo": "CAF", "Tunisia": "CAF", "Uganda": "CAF", "Zambia": "CAF", "Zimbabwe": "CAF",
    # AFC
    "Afghanistan": "AFC", "Australia": "AFC", "Bahrain": "AFC", "Bangladesh": "AFC", "Bhutan": "AFC",
    "Brunei": "AFC", "Cambodia": "AFC", "China PR": "AFC", "Guam": "AFC", "Hong Kong": "AFC",
    "India": "AFC", "Indonesia": "AFC", "Iran": "AFC", "Iraq": "AFC", "Japan": "AFC",
    "Jordan": "AFC", "Kuwait": "AFC", "Kyrgyzstan": "AFC", "Laos": "AFC", "Lebanon": "AFC",
    "Macau": "AFC", "Malaysia": "AFC", "Maldives": "AFC", "Mongolia": "AFC", "Myanmar": "AFC",
    "Nepal": "AFC", "North Korea": "AFC", "Oman": "AFC", "Pakistan": "AFC", "Palestine": "AFC",
    "Philippines": "AFC", "Qatar": "AFC", "Saudi Arabia": "AFC", "Singapore": "AFC", "South Korea": "AFC",
    "Sri Lanka": "AFC", "Syria": "AFC", "Taiwan": "AFC", "Tajikistan": "AFC", "Thailand": "AFC",
    "East Timor": "AFC", "Turkmenistan": "AFC", "United Arab Emirates": "AFC", "Uzbekistan": "AFC",
    "Vietnam": "AFC", "Yemen": "AFC",
    # OFC
    "American Samoa": "OFC", "Cook Islands": "OFC", "Fiji": "OFC", "New Caledonia": "OFC",
    "New Zealand": "OFC", "Papua New Guinea": "OFC", "Samoa": "OFC", "Solomon Islands": "OFC",
    "Tahiti": "OFC", "Tonga": "OFC", "Tuvalu": "OFC", "Vanuatu": "OFC"
}

@st.cache_data
def load_historical_matches(filepath: str) -> pl.DataFrame:
    """
    Load results.csv into a Polars DataFrame, parsing the date column,
    treating "NA" as null values, and dropping rows with null scores.
    """
    df = pl.read_csv(filepath, null_values=["NA"])
    df = df.filter(pl.col("home_score").is_not_null() & pl.col("away_score").is_not_null())
    df = df.with_columns([
        pl.col("date").str.to_date("%Y-%m-%d"),
        pl.col("home_score").cast(pl.Int64),
        pl.col("away_score").cast(pl.Int64)
    ])
    return df

@st.cache_data
def get_unique_teams(df_cached: pl.DataFrame) -> List[str]:
    """
    Get sorted list of unique team names present in the dataset.
    """
    # Combine home_team and away_team unique values
    home_teams = df_cached["home_team"].unique().to_list()
    away_teams = df_cached["away_team"].unique().to_list()
    all_teams = set(home_teams + away_teams)
    return sorted(list(all_teams))

@st.cache_data
def build_confederation_map(df_cached: pl.DataFrame) -> Dict[str, str]:
    """
    Build confederation mapping for all unique teams in the dataset.
    Uses a static map for major teams and infers others from the tournaments they played.
    """
    teams = get_unique_teams(df_cached)
    conf_map = {}
    
    # Pre-filter tournaments by team to optimize dynamic lookups
    for team in teams:
        if team in STATIC_CONFEDERATIONS:
            conf_map[team] = STATIC_CONFEDERATIONS[team]
        else:
            # Dynamic inference based on tournaments
            team_df = df_cached.filter((pl.col("home_team") == team) | (pl.col("away_team") == team))
            tournaments = team_df["tournament"].unique().to_list()
            
            conf = None
            for tour in tournaments:
                tour_lower = tour.lower()
                if "uefa" in tour_lower or "euro" in tour_lower:
                    conf = "UEFA"
                    break
                elif "copa américa" in tour_lower or "copa america" in tour_lower or "conmebol" in tour_lower:
                    conf = "CONMEBOL"
                    break
                elif "african cup" in tour_lower or "caf" in tour_lower:
                    conf = "CAF"
                    break
                elif "afc" in tour_lower or "asian cup" in tour_lower:
                    conf = "AFC"
                    break
                elif "concacaf" in tour_lower or "gold cup" in tour_lower:
                    conf = "CONCACAF"
                    break
                elif "ofc" in tour_lower or "oceania" in tour_lower:
                    conf = "OFC"
                    break
            
            if not conf:
                # Default fallback
                conf = "UEFA"
            conf_map[team] = conf
            
    return conf_map
