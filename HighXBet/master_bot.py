import pandas as pd
import requests
import json
import os
from datetime import datetime
import time

print("🤖 HIGHXBET PRO BOT - OPTIMIZED")
print("=" * 60)

# Team name mapping
TEAM_NAME_MAP = {
    'Manchester United': 'Man United', 'Manchester City': 'Man City',
    'Tottenham Hotspur': 'Tottenham', 'Newcastle United': 'Newcastle',
    'Brighton and Hove Albion': 'Brighton', 'Wolverhampton Wanderers': 'Wolves',
    'Nottingham Forest': 'Nottm Forest', 'West Ham United': 'West Ham',
    'Atletico Madrid': 'Ath Madrid', 'Athletic Bilbao': 'Ath Bilbao',
    'Real Sociedad': 'Sociedad', 'Celta Vigo': 'Celta',
    'Inter Milan': 'Inter', 'AC Milan': 'Milan', 'AS Roma': 'Roma',
    'Bayern Munich': 'Bayern Munich', 'Borussia Dortmund': 'Dortmund',
}

def normalize_team_name(team_name):
    """Convert team names to standard format"""
    if not team_name:
        return None
    
    team_name = str(team_name).strip().title()
    
    if team_name in TEAM_NAME_MAP:
        return TEAM_NAME_MAP[team_name]
    
    for api_name, our_name in TEAM_NAME_MAP.items():
        if api_name in team_name or team_name in api_name:
            return our_name
    
    return team_name

class OptimizedMasterBot:
    def __init__(self):
        self.config = self.load_config()
        self.data = None
        
    def load_config(self):
        """Load configuration"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            return {
                "api": {
                    "odds_api_key": "d2f5b0c0c61c47bb246e0b5484f7b2a3",
                    "telegram_bot_token": "8534136877:AAFyD4a2jNR3MTZlpI3WEoS1oFTMWD7bzaQ",
                    "telegram_chat_id": "645815915"
                },
                "betting": {
                    "min_odds": 2.0,  # Lowered to find more opportunities
                    "max_odds": 6.0,  # Increased range
                    "value_threshold": 0.02,  # Lower threshold
                    "max_bets_per_day": 8,
                    "min_confidence": 0.55  # Lower confidence requirement
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
    
    def get_real_odds(self):
        """Get REAL odds from The Odds API"""
        api_key = self.config['api']['odds_api_key']
        
        print("🌐 FETCHING REAL LIVE ODDS...")
        all_matches = []
        active_leagues = [league for league in self.config['leagues'] if league.get('active', True)]
        
        for league in active_leagues:
            try:
                url = f"https://api.the-odds-api.com/v4/sports/{league['code']}/odds"
                params = {
                    'apiKey': api_key,
                    'regions': 'eu',
                    'markets': 'totals',
                    'oddsFormat': 'decimal'
                }
                
                print(f"📡 {league['name']}...")
                response = requests.get(url, params=params, timeout=15)
                
                if response.status_code == 200:
                    odds_data = response.json()
                    all_matches.extend(odds_data)
                    print(f"✅ {league['name']}: {len(odds_data)} matches")
                else:
                    print(f"⚠️ {league['name']}: API error {response.status_code}")
                    
            except Exception as e:
                print(f"⚠️ {league['name']}: {e}")
        
        if all_matches:
            print(f"🎯 Total live matches: {len(all_matches)}")
            return all_matches
        else:
            print("❌ No real odds data")
            return []
    
    def extract_over_under_odds(self, match_data):
        """Extract Over/Under 2.5 odds from real match data"""
        try:
            best_over = None
            best_under = None
            best_bookmaker = None
            
            for bookmaker in match_data.get('bookmakers', []):
                for market in bookmaker.get('markets', []):
                    if market['key'] == 'totals':
                        over_odds = under_odds = None
                        
                        for outcome in market['outcomes']:
                            if outcome['name'] == 'Over' and outcome['point'] == 2.5:
                                over_odds = outcome['price']
                            elif outcome['name'] == 'Under' and outcome['point'] == 2.5:
                                under_odds = outcome['price']
                        
                        if over_odds and (best_over is None or over_odds > best_over):
                            best_over = over_odds
                            best_bookmaker = bookmaker['title']
                        if under_odds and (best_under is None or under_odds > best_under):
                            best_under = under_odds
                            best_bookmaker = bookmaker['title']
            
            if best_over and best_under:
                return {
                    'over_2.5': best_over,
                    'under_2.5': best_under,
                    'bookmaker': best_bookmaker
                }
            return None
        except:
            return None
    
    def download_data(self):
        """Download comprehensive football data"""
        print("📥 DOWNLOADING HISTORICAL DATA...")
        
        leagues = ['E0', 'E1', 'SP1', 'I1', 'D1', 'F1']
        all_data = []
        
        for league in leagues:
            try:
                url = f"https://www.football-data.co.uk/mmz4281/2324/{league}.csv"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    df = pd.read_csv(requests.compat.StringIO(response.text))
                    df['League'] = league
                    all_data.append(df)
                    print(f"✅ {league}: {len(df)} matches")
            except Exception as e:
                print(f"⚠️ {league}: {e}")
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce')
            essential_cols = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'League']
            available_cols = [col for col in essential_cols if col in combined_df.columns]
            self.data = combined_df[available_cols].dropna()
            
            self.data['TotalGoals'] = self.data['FTHG'] + self.data['FTAG']
            self.data['Over2.5'] = (self.data['TotalGoals'] > 2.5).astype(int)
            
            print(f"✅ Data ready: {len(self.data)} matches")
            return True
        return False
    
    def calculate_team_stats(self, team_name, matches=8):
        """Calculate team statistics"""
        if not team_name:
            return None
            
        team_matches = self.data[
            (self.data['HomeTeam'] == team_name) | (self.data['AwayTeam'] == team_name)
        ].tail(matches)
        
        if len(team_matches) < 3:  # Require minimum matches
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
        
        return {
            'matches': len(team_matches),
            'avg_scored': sum(goals_scored) / len(goals_scored),
            'avg_conceded': sum(goals_conceded) / len(goals_conceded),
            'over_25_rate': over_25_count / len(team_matches)
        }
    
    def predict_match(self, home_team, away_team):
        """Predict match probabilities with team name normalization"""
        # Normalize team names
        home_team = normalize_team_name(home_team)
        away_team = normalize_team_name(away_team)
        
        if not home_team or not away_team:
            return None
            
        home_stats = self.calculate_team_stats(home_team)
        away_stats = self.calculate_team_stats(away_team)
        
        if not home_stats or not away_stats:
            return None
        
        # Enhanced prediction model
        home_expected = (home_stats['avg_scored'] + away_stats['avg_conceded']) / 2 * 1.1
        away_expected = (away_stats['avg_scored'] + home_stats['avg_conceded']) / 2
        total_expected = home_expected + away_expected
        
        # Dynamic probability based on expected goals
        if total_expected > 3.5:
            over_prob = 0.75
        elif total_expected > 3.0:
            over_prob = 0.65
        elif total_expected > 2.5:
            over_prob = 0.55
        elif total_expected > 2.0:
            over_prob = 0.45
        else:
            over_prob = 0.35
        
        # Blend with historical performance
        historical_over = (home_stats['over_25_rate'] + away_stats['over_25_rate']) / 2
        final_over_prob = (over_prob * 0.6) + (historical_over * 0.4)
        final_over_prob = max(0.20, min(0.80, final_over_prob))
        
        confidence = min(home_stats['matches'], away_stats['matches']) / 8
        
        return {
            'over_2.5': final_over_prob,
            'under_2.5': 1 - final_over_prob,
            'expected_goals': round(total_expected, 2),
            'confidence': confidence,
            'home_team': home_team,
            'away_team': away_team
        }
    
    def find_value_bets(self):
        """Find value bets using real odds and predictions"""
        print("🔍 ANALYZING FOR VALUE BETS...")
        
        real_odds_data = self.get_real_odds()
        value_bets = []
        analyzed_count = 0
        value_count = 0
        
        for match_data in real_odds_data:
            try:
                home_team = match_data['home_team']
                away_team = match_data['away_team']
                
                # Get odds for this match
                odds_info = self.extract_over_under_odds(match_data)
                if not odds_info:
                    continue
                
                # Get prediction
                prediction = self.predict_match(home_team, away_team)
                if not prediction:
                    continue
                
                analyzed_count += 1
                
                # Check both markets
                for market in ['over_2.5', 'under_2.5']:
                    odds_value = odds_info[market]
                    probability = prediction[market]
                    expected_value = (probability * odds_value) - 1
                    
                    betting_params = self.config['betting']
                    if (betting_params['min_odds'] <= odds_value <= betting_params['max_odds'] and
                        expected_value >= betting_params['value_threshold'] and
                        prediction['confidence'] >= betting_params['min_confidence']):
                        
                        value_count += 1
                        value_bets.append({
                            'match': f"{home_team} vs {away_team}",
                            'bet_type': 'Over 2.5' if market == 'over_2.5' else 'Under 2.5',
                            'probability': probability,
                            'odds': odds_value,
                            'expected_value': expected_value,
                            'bookmaker': odds_info['bookmaker'],
                            'confidence': prediction['confidence'],
                            'expected_goals': prediction['expected_goals']
                        })
                        
            except Exception as e:
                continue
        
        print(f"✅ Analyzed {analyzed_count} matches, found {value_count} value bets")
        return value_bets
    
    def format_telegram_message(self, value_bets):
        """Format professional Telegram message"""
        if not value_bets:
            return "❌ No value bets found in today's analysis.\n\n💡 This means the market is efficient today. Check back later!"
        
        message = "🎯 <b>HIGHXBET VALUE ALERTS</b> 🎯\n\n"
        message += f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        message += f"📊 Found <b>{len(value_bets)}</b> value opportunities\n\n"
        
        # Sort by expected value
        value_bets.sort(key=lambda x: x['expected_value'], reverse=True)
        
        for i, bet in enumerate(value_bets[:6], 1):
            if i == 1:
                message += "🥇 "
            elif i == 2:
                message += "🥈 "
            elif i == 3:
                message += "🥉 "
            else:
                message += "🔹 "
                
            message += f"<b>{bet['match']}</b>\n"
            message += f"   🎲 <b>{bet['bet_type']}</b>\n"
            message += f"   💰 Odds: <b>{bet['odds']}</b>\n"
            message += f"   📊 Probability: <b>{bet['probability']:.1%}</b>\n"
            message += f"   💎 Expected Value: <b>+{bet['expected_value']:.1%}</b>\n"
            message += f"   ⚽ Expected Goals: {bet['expected_goals']}\n"
            message += f"   🏦 {bet['bookmaker']}\n\n"
        
        message += "⚠️ <i>Professional tool - Gamble responsibly</i>\n"
        message += "🤖 <i>Powered by HighXBet AI</i>"
        
        return message
    
    def run_complete_analysis(self):
        """Run complete professional analysis"""
        print("🚀 HIGHXBET PRO ANALYSIS STARTED")
        print("=" * 60)
        
        if not self.download_data():
            return
        
        value_bets = self.find_value_bets()
        
        print("\n" + "=" * 60)
        print("📊 PROFESSIONAL RESULTS")
        print("=" * 60)
        
        if value_bets:
            print(f"🎉 FOUND {len(value_bets)} VALUE BETS!")
            print("\n" + "=" * 60)
            
            value_bets.sort(key=lambda x: x['expected_value'], reverse=True)
            
            for i, bet in enumerate(value_bets, 1):
                print(f"{i}. {bet['match']}")
                print(f"   📊 {bet['bet_type']} @ {bet['odds']}")
                print(f"   📈 Probability: {bet['probability']:.1%}")
                print(f"   💎 Expected Value: +{bet['expected_value']:.1%}")
                print(f"   ⚽ Expected Goals: {bet['expected_goals']}")
                print(f"   🏦 {bet['bookmaker']}")
                print()
            
            telegram_message = self.format_telegram_message(value_bets)
            print("📱 SENDING TELEGRAM ALERT...")
            
            if self.send_telegram_message(telegram_message):
                print("✅ Telegram alert sent successfully!")
                print("📱 Check your phone for real value bets!")
            else:
                print("❌ Failed to send Telegram")
        else:
            print("❌ No value bets found today.")
            print("💡 The betting market appears efficient today.")
            print("💡 Try again later when more matches are available.")
        
        print("=" * 60)
        print("✅ ANALYSIS COMPLETE!")

if __name__ == "__main__":
    bot = OptimizedMasterBot()
    bot.run_complete_analysis()
    
    print("\n🎯 YOUR PRO BOT IS LIVE!")
    print("💪 Features:")
    print("   ✅ Real odds from 80+ matches")
    print("   ✅ Team name mapping")
    print("   ✅ Optimized value detection")
    print("   ✅ Telegram alerts to your phone")
    
    input("\nPress Enter to exit...")