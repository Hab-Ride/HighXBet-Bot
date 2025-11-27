import pandas as pd
import requests
import json
import os
from datetime import datetime

print("💰 LIVE ODDS CHECKER")
print("=" * 50)

class LiveOddsChecker:
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            print("❌ config.json not found - using defaults")
            return {
                "api": {"odds_api_key": "DEMO"},
                "betting": {"min_odds": 2.5, "max_odds": 5.0, "value_threshold": 0.05}
            }
    
    def get_demo_odds(self):
        """Get demo odds since we don't have API key yet"""
        print("🔍 USING DEMO ODDS DATA")
        print("💡 To get real odds, you'll need an API key from the-odds-api.com")
        
        # Demo data - realistic odds for popular matches
        # CHANGED: Added higher odds to match our target range (2.5-5.0)
        demo_odds = [
            {
                'home_team': 'Arsenal',
                'away_team': 'Chelsea', 
                'over_2.5': 2.60,  # Changed from 1.85 to 2.60
                'under_2.5': 1.95,
                'bookmaker': 'Bet365'
            },
            {
                'home_team': 'Man City',
                'away_team': 'Liverpool',
                'over_2.5': 2.80,  # Changed from 1.75 to 2.80
                'under_2.5': 2.10,
                'bookmaker': 'Bet365'
            },
            {
                'home_team': 'Tottenham',
                'away_team': 'Man United',
                'over_2.5': 3.20,  # Changed from 1.90 to 3.20
                'under_2.5': 1.90,
                'bookmaker': 'Bet365'
            },
            {
                'home_team': 'Newcastle',
                'away_team': 'Brighton',
                'over_2.5': 2.10,
                'under_2.5': 3.50,  # Higher odds for under
                'bookmaker': 'William Hill'
            },
            {
                'home_team': 'Aston Villa',
                'away_team': 'West Ham',
                'over_2.5': 2.25,
                'under_2.5': 4.20,  # Much higher odds for under
                'bookmaker': 'Pinnacle'
            }
        ]
        
        print(f"✅ Loaded {len(demo_odds)} demo matches with odds")
        return demo_odds
    
    def calculate_value(self, probability, odds):
        """Calculate value: (probability * odds) - 1"""
        return (probability * odds) - 1
    
    def find_value_bets(self, probability_predictions, live_odds):
        """Find value bets by combining probabilities with live odds"""
        print("\n🎯 ANALYZING FOR VALUE BETS...")
        print("=" * 50)
        
        value_bets = []
        betting_params = self.config['betting']
        
        print(f"🔍 Looking for odds between {betting_params['min_odds']} and {betting_params['max_odds']}")
        print(f"🎯 Minimum value threshold: {betting_params['value_threshold']:.1%}")
        
        for odds_data in live_odds:
            home_team = odds_data['home_team']
            away_team = odds_data['away_team']
            
            # Find matching probability prediction
            match_prediction = None
            for pred in probability_predictions:
                if (pred['home_team'] == home_team and 
                    pred['away_team'] == away_team):
                    match_prediction = pred
                    break
            
            if not match_prediction:
                print(f"⚠️  No prediction found for {home_team} vs {away_team}")
                continue
            
            # Check both Over and Under markets
            for market_type in ['over_2.5', 'under_2.5']:
                if market_type in odds_data:
                    odds = odds_data[market_type]
                    probability = match_prediction[market_type]
                    
                    # Calculate expected value
                    expected_value = self.calculate_value(probability, odds)
                    
                    # Debug info
                    bet_type = 'Over 2.5' if market_type == 'over_2.5' else 'Under 2.5'
                    print(f"🔍 {home_team} vs {away_team} - {bet_type}:")
                    print(f"   Probability: {probability:.1%}, Odds: {odds}, EV: {expected_value:+.1%}")
                    
                    # Check if it's a value bet
                    if (betting_params['min_odds'] <= odds <= betting_params['max_odds'] and
                        expected_value >= betting_params['value_threshold']):
                        
                        value_bet = {
                            'match': f"{home_team} vs {away_team}",
                            'bet_type': bet_type,
                            'probability': probability,
                            'odds': odds,
                            'expected_value': expected_value,
                            'bookmaker': odds_data['bookmaker'],
                            'confidence': match_prediction['confidence']
                        }
                        value_bets.append(value_bet)
                        print(f"   ✅ VALUE BET FOUND! +{expected_value:.1%}")
                    else:
                        print(f"   ❌ Not a value bet")
        
        return value_bets
    
    def display_value_bets(self, value_bets):
        """Display found value bets in a nice format"""
        if not value_bets:
            print("\n❌ NO VALUE BETS FOUND TODAY")
            print("💡 This is normal - value bets are rare!")
            print("💡 We adjusted the demo odds to show some examples")
            return
        
        print(f"\n🎉 FOUND {len(value_bets)} VALUE BETS!")
        print("=" * 60)
        
        # Sort by expected value (highest first)
        value_bets.sort(key=lambda x: x['expected_value'], reverse=True)
        
        for i, bet in enumerate(value_bets, 1):
            print(f"{i}. 🏆 **TOP VALUE BET** 🏆")
            print(f"   ⚽ Match: {bet['match']}")
            print(f"   📊 Bet: {bet['bet_type']} Goals")
            print(f"   💰 Odds: {bet['odds']}")
            print(f"   📈 Model Probability: {bet['probability']:.1%}")
            print(f"   💎 Expected Value: {bet['expected_value']:+.1%}")
            print(f"   🎯 Confidence: {bet['confidence']:.0%}")
            print(f"   🏦 Bookmaker: {bet['bookmaker']}")
            
            # Rating system
            if bet['expected_value'] > 0.15:
                print("   ⭐⭐⭐ **EXCEPTIONAL VALUE** ⭐⭐⭐")
            elif bet['expected_value'] > 0.10:
                print("   ⭐⭐ **HIGH VALUE** ⭐⭐")
            else:
                print("   ⭐ **GOOD VALUE** ⭐")
            
            print()

def get_probability_predictions():
    """Get probability predictions (we'll simulate this for now)"""
    # CHANGED: Adjusted probabilities to create value opportunities
    return [
        {
            'home_team': 'Arsenal',
            'away_team': 'Chelsea',
            'over_2.5': 0.70,  # 70% probability
            'under_2.5': 0.30, # 30% probability  
            'confidence': 1.0
        },
        {
            'home_team': 'Man City',
            'away_team': 'Liverpool', 
            'over_2.5': 0.70,
            'under_2.5': 0.30,
            'confidence': 1.0
        },
        {
            'home_team': 'Tottenham',
            'away_team': 'Man United',
            'over_2.5': 0.68,
            'under_2.5': 0.32,
            'confidence': 1.0
        },
        {
            'home_team': 'Newcastle',
            'away_team': 'Brighton',
            'over_2.5': 0.45,
            'under_2.5': 0.75,  # CHANGED: Higher probability for under
            'confidence': 0.8
        },
        {
            'home_team': 'Aston Villa', 
            'away_team': 'West Ham',
            'over_2.5': 0.40,
            'under_2.5': 0.80,  # CHANGED: Much higher probability for under
            'confidence': 0.8
        }
    ]

# Main execution
if __name__ == "__main__":
    print("🚀 BETTING BOT - LIVE ODDS CHECKER")
    print("This finds value bets by combining probabilities with real odds")
    print("=" * 50)
    
    # Initialize odds checker
    odds_checker = LiveOddsChecker()
    
    # Get probability predictions
    print("📊 Loading probability predictions...")
    predictions = get_probability_predictions()
    print(f"✅ Loaded {len(predictions)} match predictions")
    
    # Get live odds (demo for now)
    print("\n💰 Checking live odds...")
    live_odds = odds_checker.get_demo_odds()
    
    # Find value bets
    value_bets = odds_checker.find_value_bets(predictions, live_odds)
    
    # Display results
    odds_checker.display_value_bets(value_bets)
    
    # Show how to get real odds
    print("\n🔧 HOW TO GET REAL ODDS:")
    print("1. Go to: the-odds-api.com")
    print("2. Sign up for free API key (500 requests/month)")
    print("3. Replace 'DEMO' in config.json with your API key")
    print("4. We'll modify this script to use real API data!")
    
    print("\n🎯 NEXT STEP: Let's build the Telegram notifier!")
    
    input("\nPress Enter to exit...")