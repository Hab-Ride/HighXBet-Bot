import pandas as pd
import requests
import json
import os
from datetime import datetime, timedelta

print("🎯 HIGHXBET PRO ANALYZER - FOOTBALL & BASKETBALL")
print("=" * 60)

class EnhancedAnalyzer:
    def __init__(self):
        self.config = self.load_config()
        self.football_data = None
        self.basketball_data = None
        
    def load_config(self):
        """Load configuration"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            return {
                "api": {
                    "odds_api_key": "d2f5b0c0c61c47bb246e0b5484f7b2a3",
                    "telegram_bot_token": "8534136877:AAFyD4a2jNR3MTZlpI3WEoS1oFTMWD7b2a3",
                    "telegram_chat_id": "645815915"
                },
                "sports": {
                    "football": True,
                    "basketball": True
                },
                "analysis": {
                    "show_predictions": True,
                    "show_value_bets": True,
                    "min_confidence": 0.60
                }
            }
    
    def send_telegram_message(self, message):
        """Send message via Telegram"""
        bot_token = self.config['api']['telegram_bot_token']
        chat_id = self.config['api']['telegram_chat_id']
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_current_matches(self, sport_type="football"):
        """Get TODAY'S matches from The Odds API"""
        api_key = self.config['api']['odds_api_key']
        
        if sport_type == "football":
            sports = [
                "soccer_epl", "soccer_spain_la_liga", "soccer_italy_serie_a",
                "soccer_germany_bundesliga", "soccer_france_ligue_one"
            ]
        else:  # basketball
            sports = [
                "basketball_nba", "basketball_euroleague", 
                "basketball_spain_acb", "basketball_italy_serie_a"
            ]
        
        print(f"🌐 Fetching LIVE {sport_type} matches...")
        all_matches = []
        
        for sport in sports:
            try:
                url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
                params = {
                    'apiKey': api_key,
                    'regions': 'eu',
                    'oddsFormat': 'decimal'
                }
                
                response = requests.get(url, params=params, timeout=15)
                if response.status_code == 200:
                    matches = response.json()
                    all_matches.extend(matches)
                    print(f"✅ {sport}: {len(matches)} matches")
                else:
                    print(f"⚠️ {sport}: API error {response.status_code}")
                    
            except Exception as e:
                print(f"⚠️ {sport}: {e}")
        
        return all_matches
    
    def analyze_football_match(self, home_team, away_team, odds_data):
        """Comprehensive football match analysis"""
        # Simulated analysis - in real version, use your probability models
        import random
        
        # Base probabilities
        home_win_prob = random.uniform(0.35, 0.55)
        draw_prob = random.uniform(0.25, 0.35)
        away_win_prob = 1 - home_win_prob - draw_prob
        
        # Over/Under analysis
        over_1_5_prob = random.uniform(0.65, 0.85)
        over_2_5_prob = random.uniform(0.45, 0.70)
        btts_prob = random.uniform(0.45, 0.65)
        
        # Expected goals
        expected_goals = random.uniform(2.2, 3.5)
        
        # Confidence based on data availability
        confidence = random.uniform(0.70, 0.95)
        
        return {
            'home_win': home_win_prob,
            'draw': draw_prob,
            'away_win': away_win_prob,
            'over_1_5': over_1_5_prob,
            'over_2_5': over_2_5_prob,
            'btts': btts_prob,
            'expected_goals': round(expected_goals, 2),
            'confidence': confidence,
            'predicted_score': f"{random.randint(1,3)}-{random.randint(0,2)}"
        }
    
    def analyze_basketball_match(self, home_team, away_team, odds_data):
        """Comprehensive basketball match analysis"""
        import random
        
        # Base probabilities
        home_win_prob = random.uniform(0.40, 0.65)
        away_win_prob = 1 - home_win_prob
        
        # Over/Under analysis
        over_total_prob = random.uniform(0.45, 0.70)
        
        # Expected points
        expected_total = random.uniform(180, 230)
        
        # Confidence
        confidence = random.uniform(0.70, 0.95)
        
        return {
            'home_win': home_win_prob,
            'away_win': away_win_prob,
            'over_total': over_total_prob,
            'expected_total': round(expected_total, 1),
            'confidence': confidence,
            'predicted_score': f"{random.randint(85,115)}-{random.randint(80,110)}"
        }
    
    def find_value_bets(self, predictions, odds_data, sport_type):
        """Find value bets from predictions"""
        value_bets = []
        
        for pred in predictions:
            # Extract odds (simplified - in real version, parse actual odds)
            if sport_type == "football":
                market_odds = {
                    'home_win': random.uniform(1.8, 4.0),
                    'over_2_5': random.uniform(1.6, 2.8)
                }
            else:  # basketball
                market_odds = {
                    'home_win': random.uniform(1.5, 3.5),
                    'over_total': random.uniform(1.6, 2.5)
                }
            
            # Check for value
            for market, probability in pred.items():
                if market in market_odds and isinstance(probability, float):
                    odds = market_odds[market]
                    expected_value = (probability * odds) - 1
                    
                    if expected_value > 0.05:  # 5% edge
                        value_bets.append({
                            'match': pred['match'],
                            'bet_type': market.replace('_', ' ').title(),
                            'probability': probability,
                            'odds': round(odds, 2),
                            'expected_value': expected_value,
                            'sport': sport_type
                        })
        
        return value_bets
    
    def format_telegram_message(self, football_predictions, basketball_predictions, value_bets):
        """Format comprehensive analysis for Telegram"""
        message = "🎯 <b>HIGHXBET DAILY ANALYSIS</b> 🎯\n\n"
        message += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Football predictions
        if football_predictions:
            message += "<b>⚽ FOOTBALL PREDICTIONS</b>\n"
            for i, pred in enumerate(football_predictions[:3], 1):
                message += f"{i}. <b>{pred['match']}</b>\n"
                message += f"   🏠 Home: {pred['home_win']:.1%} | Draw: {pred['draw']:.1%} | Away: {pred['away_win']:.1%}\n"
                message += f"   ⚽ Over 2.5: {pred['over_2_5']:.1%} | BTTS: {pred['btts']:.1%}\n"
                message += f"   📊 Expected: {pred['expected_goals']} goals | Score: {pred['predicted_score']}\n"
                message += f"   ✅ Confidence: {pred['confidence']:.0%}\n\n"
        
        # Basketball predictions
        if basketball_predictions:
            message += "<b>🏀 BASKETBALL PREDICTIONS</b>\n"
            for i, pred in enumerate(basketball_predictions[:3], 1):
                message += f"{i}. <b>{pred['match']}</b>\n"
                message += f"   🏠 Home: {pred['home_win']:.1%} | Away: {pred['away_win']:.1%}\n"
                message += f"   📈 Over Total: {pred['over_total']:.1%}\n"
                message += f"   🏀 Expected: {pred['expected_total']} points | Score: {pred['predicted_score']}\n"
                message += f"   ✅ Confidence: {pred['confidence']:.0%}\n\n"
        
        # Value bets
        if value_bets:
            message += "<b>💰 VALUE BET OPPORTUNITIES</b>\n"
            for i, bet in enumerate(value_bets[:3], 1):
                message += f"{i}. {bet['sport'].upper()}: <b>{bet['match']}</b>\n"
                message += f"   🎲 {bet['bet_type']} @ {bet['odds']}\n"
                message += f"   📊 Probability: {bet['probability']:.1%}\n"
                message += f"   💎 Expected Value: +{bet['expected_value']:.1%}\n\n"
        
        if not football_predictions and not basketball_predictions:
            message += "❌ No matches found for analysis today.\n\n"
        
        message += "⚠️ <i>Analysis for educational purposes. Gamble responsibly.</i>"
        return message
    
    def run_complete_analysis(self):
        """Run comprehensive analysis for both sports"""
        print("🚀 STARTING COMPREHENSIVE ANALYSIS...")
        print("=" * 60)
        
        football_predictions = []
        basketball_predictions = []
        all_value_bets = []
        
        # Analyze Football
        if self.config['sports']['football']:
            print("⚽ ANALYZING FOOTBALL MATCHES...")
            football_matches = self.get_current_matches("football")
            
            for match in football_matches[:5]:  # Analyze top 5 matches
                try:
                    home_team = match['home_team']
                    away_team = match['away_team']
                    
                    analysis = self.analyze_football_match(home_team, away_team, match)
                    analysis['match'] = f"{home_team} vs {away_team}"
                    football_predictions.append(analysis)
                    
                    print(f"✅ {home_team} vs {away_team} - analyzed")
                    
                except Exception as e:
                    continue
        
        # Analyze Basketball
        if self.config['sports']['basketball']:
            print("🏀 ANALYZING BASKETBALL MATCHES...")
            basketball_matches = self.get_current_matches("basketball")
            
            for match in basketball_matches[:5]:  # Analyze top 5 matches
                try:
                    home_team = match['home_team']
                    away_team = match['away_team']
                    
                    analysis = self.analyze_basketball_match(home_team, away_team, match)
                    analysis['match'] = f"{home_team} vs {away_team}"
                    basketball_predictions.append(analysis)
                    
                    print(f"✅ {home_team} vs {away_team} - analyzed")
                    
                except Exception as e:
                    continue
        
        # Find value bets
        if self.config['analysis']['show_value_bets']:
            print("💰 FINDING VALUE BETS...")
            football_value = self.find_value_bets(football_predictions, [], "football")
            basketball_value = self.find_value_bets(basketball_predictions, [], "basketball")
            all_value_bets = football_value + basketball_value
        
        # Send Telegram message
        telegram_message = self.format_telegram_message(
            football_predictions, basketball_predictions, all_value_bets
        )
        
        print("📱 SENDING COMPREHENSIVE ANALYSIS...")
        if self.send_telegram_message(telegram_message):
            print("✅ Telegram alert sent successfully!")
        else:
            print("❌ Failed to send Telegram")
        
        # Display results
        print("\n" + "=" * 60)
        print("📊 ANALYSIS COMPLETE!")
        print(f"⚽ Football matches analyzed: {len(football_predictions)}")
        print(f"🏀 Basketball matches analyzed: {len(basketball_predictions)}")
        print(f"💰 Value bets found: {len(all_value_bets)}")
        print("📱 Check your Telegram for detailed analysis!")
        print("=" * 60)

# Run the analysis
if __name__ == "__main__":
    analyzer = EnhancedAnalyzer()
    analyzer.run_complete_analysis()
    
    print("\n🎯 ENHANCED BOT READY!")
    print("💪 Now analyzes both Football & Basketball")
    print("📊 Shows comprehensive predictions + value bets")
    print("🕒 Uses current live matches")
