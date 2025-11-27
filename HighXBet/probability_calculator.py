import pandas as pd
import numpy as np
import os

print("🎯 PROBABILITY CALCULATOR")
print("=" * 50)

def load_data():
    """Load the cleaned data we downloaded"""
    try:
        df = pd.read_csv('data/processed/cleaned_data.csv')
        print(f"✅ Data loaded: {len(df)} matches")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def calculate_team_stats(df, team_name, matches=10):
    """Calculate statistics for a specific team"""
    # Get team's recent matches
    team_matches = df[
        (df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)
    ].tail(matches)
    
    if len(team_matches) == 0:
        return None
    
    goals_scored = []
    goals_conceded = []
    over_25_count = 0
    
    for _, match in team_matches.iterrows():
        if match['HomeTeam'] == team_name:
            goals_scored.append(match['FTHG'])
            goals_conceded.append(match['FTAG'])
        else:
            goals_scored.append(match['FTAG'])
            goals_conceded.append(match['FTHG'])
        
        if match['TotalGoals'] > 2.5:
            over_25_count += 1
    
    stats = {
        'matches_analyzed': len(team_matches),
        'avg_goals_scored': np.mean(goals_scored),
        'avg_goals_conceded': np.mean(goals_conceded),
        'over_25_rate': over_25_count / len(team_matches),
        'attack_strength': np.mean(goals_scored),
        'defense_weakness': np.mean(goals_conceded)
    }
    
    return stats

def predict_match_probability(df, home_team, away_team):
    """Predict probability for Over/Under 2.5 goals"""
    print(f"\n🔮 PREDICTING: {home_team} vs {away_team}")
    print("-" * 40)
    
    # Get team stats
    home_stats = calculate_team_stats(df, home_team)
    away_stats = calculate_team_stats(df, away_team)
    
    if not home_stats or not away_stats:
        print("❌ Not enough data for these teams")
        return None
    
    # Display team stats
    print(f"🏠 {home_team}:")
    print(f"   Avg goals scored: {home_stats['avg_goals_scored']:.2f}")
    print(f"   Avg goals conceded: {home_stats['avg_goals_conceded']:.2f}")
    print(f"   Over 2.5 rate: {home_stats['over_25_rate']:.1%}")
    
    print(f"✈️  {away_team}:")
    print(f"   Avg goals scored: {away_stats['avg_goals_scored']:.2f}")
    print(f"   Avg goals conceded: {away_stats['avg_goals_conceded']:.2f}")
    print(f"   Over 2.5 rate: {away_stats['over_25_rate']:.1%}")
    
    # Simple probability calculation
    home_attack = home_stats['avg_goals_scored']
    away_defense = away_stats['avg_goals_conceded']
    away_attack = away_stats['avg_goals_scored']
    home_defense = home_stats['avg_goals_conceded']
    
    # Expected goals (simple model)
    expected_home_goals = (home_attack + away_defense) / 2
    expected_away_goals = (away_attack + home_defense) / 2
    
    # Apply home advantage
    expected_home_goals *= 1.1
    
    total_expected_goals = expected_home_goals + expected_away_goals
    
    # Simple probability based on expected goals
    if total_expected_goals > 3.0:
        over_prob = 0.70
    elif total_expected_goals > 2.5:
        over_prob = 0.60
    elif total_expected_goals > 2.0:
        over_prob = 0.45
    else:
        over_prob = 0.30
    
    # Blend with historical rates
    historical_over = (home_stats['over_25_rate'] + away_stats['over_25_rate']) / 2
    final_over_prob = (over_prob * 0.6) + (historical_over * 0.4)
    
    # Ensure probabilities are reasonable
    final_over_prob = max(0.15, min(0.85, final_over_prob))
    final_under_prob = 1 - final_over_prob
    
    print(f"\n📊 PREDICTION RESULTS:")
    print(f"   Expected total goals: {total_expected_goals:.2f}")
    print(f"   Over 2.5 probability: {final_over_prob:.1%}")
    print(f"   Under 2.5 probability: {final_under_prob:.1%}")
    
    # Confidence rating
    min_matches = min(home_stats['matches_analyzed'], away_stats['matches_analyzed'])
    confidence = min(1.0, min_matches / 10)
    
    print(f"   Confidence: {confidence:.0%}")
    
    return {
        'over_2.5': final_over_prob,
        'under_2.5': final_under_prob,
        'expected_goals': total_expected_goals,
        'confidence': confidence
    }

def analyze_multiple_matches(df):
    """Analyze some example matches"""
    print("\n🎯 ANALYZING POPULAR MATCHES...")
    print("=" * 50)
    
    # Get list of teams from the data
    teams = pd.unique(df['HomeTeam'])
    
    # Analyze some example matches (you can change these)
    matches_to_analyze = [
        ("Arsenal", "Chelsea"),
        ("Man City", "Liverpool"),
        ("Tottenham", "Man United")
    ]
    
    all_predictions = []
    
    for home_team, away_team in matches_to_analyze:
        # Check if both teams exist in our data
        if home_team in teams and away_team in teams:
            prediction = predict_match_probability(df, home_team, away_team)
            if prediction:
                all_predictions.append({
                    'match': f"{home_team} vs {away_team}",
                    **prediction
                })
        else:
            print(f"\n⚠️  Skipping {home_team} vs {away_team} - not in current data")
    
    return all_predictions

def show_value_opportunities(predictions):
    """Show potential value bets based on probabilities"""
    print("\n💰 VALUE BET OPPORTUNITIES")
    print("=" * 50)
    print("Looking for high probability predictions...")
    print("(Assuming odds of 2.5 for Over 2.5 goals)")
    print("-" * 50)
    
    value_bets = []
    
    for pred in predictions:
        # If Over 2.5 probability is high enough, it might be valuable
        if pred['over_2.5'] > 0.65 and pred['confidence'] > 0.7:
            value_bets.append({
                'match': pred['match'],
                'bet': 'Over 2.5 Goals',
                'probability': pred['over_2.5'],
                'confidence': pred['confidence']
            })
        
        # If Under 2.5 probability is high enough
        if pred['under_2.5'] > 0.65 and pred['confidence'] > 0.7:
            value_bets.append({
                'match': pred['match'],
                'bet': 'Under 2.5 Goals', 
                'probability': pred['under_2.5'],
                'confidence': pred['confidence']
            })
    
    if value_bets:
        for i, bet in enumerate(value_bets, 1):
            print(f"{i}. {bet['match']}")
            print(f"   📊 Bet: {bet['bet']}")
            print(f"   🎯 Probability: {bet['probability']:.1%}")
            print(f"   ✅ Confidence: {bet['confidence']:.0%}")
            print()
    else:
        print("❌ No high-confidence value opportunities found")
        print("💡 Try analyzing different matches")

# Main execution
if __name__ == "__main__":
    print("🚀 BETTING BOT - PROBABILITY CALCULATOR")
    print("This analyzes team data and predicts match outcomes")
    print("=" * 50)
    
    # Load the data
    data = load_data()
    if data is None:
        print("❌ Please run download_data.py first!")
        exit()
    
    # Analyze some matches
    predictions = analyze_multiple_matches(data)
    
    # Show value opportunities
    show_value_opportunities(predictions)
    
    print("\n🎯 NEXT STEP: We'll add live odds checking!")
    print("💡 You can modify the teams in 'matches_to_analyze' to test different matches")
    
    input("\nPress Enter to exit...")