import requests
import json
from datetime import datetime

print("🎯 HIGHXBET MATCH ANALYZER")
print("=" * 50)

class SimpleAnalyzer:
    def __init__(self):
        self.config = self.load_config()
        
    def load_config(self):
        """Simple config loader"""
        return {
            "api": {
                "odds_api_key": "d2f5b0c0c61c47bb246e0b5484f7b2a3",
                "telegram_bot_token": "8534136877:AAFyD4a2jNR3MTZlpI3WEoS1oFTMWD7b2a3",
                "telegram_chat_id": "645815915"
            }
        }
    
    def send_telegram_message(self, message):
        """Send message via Telegram"""
        try:
            bot_token = self.config['api']['telegram_bot_token']
            chat_id = self.config['api']['telegram_chat_id']
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_current_matches(self):
        """Get today's matches"""
        api_key = self.config['api']['odds_api_key']
        
        print("🌐 Fetching current matches...")
        
        sports = ["soccer_epl", "basketball_nba"]
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
                    sport_name = "Football" if "soccer" in sport else "Basketball"
                    print(f"✅ {sport_name}: {len(matches)} matches")
                else:
                    print(f"⚠️ {sport}: API error")
                    
            except Exception as e:
                print(f"⚠️ {sport}: Error")
        
        return all_matches
    
    def analyze_matches(self, matches):
        """Simple match analysis"""
        predictions = []
        
        for match in matches[:6]:  # Analyze first 6 matches
            try:
                home_team = match.get('home_team', 'Home')
                away_team = match.get('away_team', 'Away')
                sport = "Basketball" if "basketball" in match.get('sport_key', '') else "Football"
                
                # Simple analysis (replace with real models later)
                if sport == "Football":
                    prediction = f"{home_team} vs {away_team}\n"
                    prediction += f"   📊 Home: 45% | Draw: 30% | Away: 25%\n"
                    prediction += f"   ⚽ Over 2.5: 65% | BTTS: 58%\n"
                    prediction += f"   🎯 Predicted: 2-1\n"
                else:
                    prediction = f"{home_team} vs {away_team}\n"
                    prediction += f"   📊 Home: 55% | Away: 45%\n"
                    prediction += f"   🏀 Over Total: 62%\n"
                    prediction += f"   🎯 Predicted: 108-102\n"
                
                predictions.append(prediction)
                print(f"✅ Analyzed: {home_team} vs {away_team}")
                
            except Exception as e:
                continue
        
        return predictions
    
    def run_analysis(self):
        """Run complete analysis"""
        print("🚀 Starting analysis...")
        
        # Get current matches
        matches = self.get_current_matches()
        
        if not matches:
            message = "❌ No current matches found for analysis."
            print(message)
            self.send_telegram_message(message)
            return
        
        # Analyze matches
        predictions = self.analyze_matches(matches)
        
        # Format Telegram message
        message = "🎯 <b>HIGHXBET DAILY ANALYSIS</b>\n\n"
        message += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        message += f"📊 Found {len(matches)} live matches\n\n"
        
        if predictions:
            message += "<b>TOP PREDICTIONS:</b>\n"
            for i, pred in enumerate(predictions[:4], 1):
                message += f"{i}. {pred}\n"
        else:
            message += "❌ No matches analyzed\n"
        
        message += "\n⚡ <i>Live match analysis completed</i>"
        
        # Send to Telegram
        print("📱 Sending to Telegram...")
        if self.send_telegram_message(message):
            print("✅ Telegram alert sent!")
        else:
            print("❌ Failed to send Telegram")
        
        print(f"\n🎯 ANALYSIS COMPLETE!")
        print(f"📊 Matches analyzed: {len(predictions)}")
        print("📱 Check your Telegram!")

# Run the analysis
if __name__ == "__main__":
    analyzer = SimpleAnalyzer()
    analyzer.run_analysis()
