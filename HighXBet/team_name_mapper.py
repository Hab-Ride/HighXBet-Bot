import pandas as pd
import requests
import json
from datetime import datetime

# Team name mapping between different data sources
TEAM_NAME_MAP = {
    # Premier League
    'Manchester United': 'Man United', 'Man Utd': 'Man United',
    'Manchester City': 'Man City', 
    'Tottenham Hotspur': 'Tottenham', 'Spurs': 'Tottenham',
    'Newcastle United': 'Newcastle',
    'Brighton and Hove Albion': 'Brighton',
    'Wolverhampton Wanderers': 'Wolves',
    'Nottingham Forest': 'Nottm Forest',
    'Sheffield United': 'Sheffield United',
    
    # La Liga
    'Atletico Madrid': 'Ath Madrid', 'Atlético Madrid': 'Ath Madrid',
    'Athletic Bilbao': 'Ath Bilbao',
    'Real Sociedad': 'Sociedad',
    'Celta Vigo': 'Celta',
    
    # Serie A
    'Inter Milan': 'Inter', 'Internazionale': 'Inter',
    'AC Milan': 'Milan',
    'AS Roma': 'Roma',
    'SS Lazio': 'Lazio',
    
    # Bundesliga
    'Bayern Munich': 'Bayern Munich', 'FC Bayern Munich': 'Bayern Munich',
    'Borussia Dortmund': 'Dortmund',
    'RB Leipzig': 'RB Leipzig',
    'Bayer Leverkusen': 'Leverkusen',
    'Borussia Monchengladbach': "M'gladbach",
}

def normalize_team_name(team_name):
    """Convert team names to standard format"""
    if not team_name:
        return None
    
    # Remove extra whitespace and convert to title case
    team_name = str(team_name).strip().title()
    
    # Check if we have a direct mapping
    if team_name in TEAM_NAME_MAP:
        return TEAM_NAME_MAP[team_name]
    
    # Try partial matches
    for api_name, our_name in TEAM_NAME_MAP.items():
        if api_name in team_name or team_name in api_name:
            return our_name
    
    return team_name

def test_mapping():
    """Test the team name mapping"""
    test_names = [
        'Manchester United', 'Man City', 'Tottenham Hotspur',
        'Atletico Madrid', 'Inter Milan', 'Bayern Munich'
    ]
    
    print("🧪 TESTING TEAM NAME MAPPING")
    print("=" * 40)
    for name in test_names:
        mapped = normalize_team_name(name)
        print(f"{name:25} → {mapped}")
    print("=" * 40)

if __name__ == "__main__":
    test_mapping()