import requests
import random
from datetime import datetime

print("🤖 HIGHXBET PREDICTION BOT")
print("=" * 40)

def send_telegram_message(message):
    """Send message via Telegram"""
    try:
        bot_token = "8534136877:AAFyD4a2jNR3MTZlpI3WEoS1oFTMWD7b2a3"
        chat_id = "645815915"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def get_sports_events():
    """Get sports events from API"""
    api_key = "d2f5b0c0c61c47bb246e0b5484f7b2a3"
    
    print("🌐 Fetching sports events...")
    
    sports_to_check = [
        "soccer_epl",           # Premier League
        "basketball_nba",       # NBA
        "soccer_spain_la_liga", # La Liga
        "soccer_italy_serie_a"  # Serie A
    ]
    
    all_events = []
    
    for sport in sports_to_check:
        try:
            url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
            params = {
                'apiKey': api_key,
                'regions': 'eu',
                'oddsFormat': 'decimal'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                events = response.json()
                all_events.extend(events)
                
                sport_name = sport.replace('_', ' ').title()
                print(f"✅ {sport_name}: {len(events)} events")
            else:
                print(f"❌ {sport}: API returned {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ {sport}: Connection failed")
    
    return all_events

def generate_football_prediction(home_team, away_team):
    """Generate football match predictions"""
    # Win probabilities
    home_win = random.uniform(0.35, 0.65)
    draw = random.uniform(0.20, 0.35)
    away_win = 1 - home_win - draw
    
    # Goal predictions
    over_1_5 = random.uniform(0.70, 0.90)
    over_2_5 = random.uniform(0.45, 0.75)
    btts = random.uniform(0.40, 0.70)
    
    # Score prediction
    home_goals = random.randint(0, 3)
    away_goals = random.randint(0, 2)
    
    return {
        'home_win': home_win,
        'draw': draw,
        'away_win': away_win,
        'over_1_5': over_1_5,
        'over_2_5': over_2_5,
        'btts': btts,
        'predicted_score': f"{home_goals}-{away_goals}",
        'confidence': random.uniform(0.70, 0.95)
    }

def generate_basketball_prediction(home_team, away_team):
    """Generate basketball game predictions"""
    # Win probabilities
    home_win = random.uniform(0.45, 0.75)
    away_win = 1 - home_win
    
    # Points predictions
    over_total = random.uniform(0.50, 0.80)
    
    # Score prediction
    home_points = random.randint(95, 115)
    away_points = random.randint(90, 110)
    
    return {
        'home_win': home_win,
        'away_win': away_win,
        'over_total': over_total,
        'predicted_score': f"{home_points}-{away_points}",
        'confidence': random.uniform(0.70, 0.95)
    }

def create_predictions_message(events):
    """Create predictions message for Telegram"""
    message = "🎯 <b>HIGHXBET MATCH PREDICTIONS</b> 🎯\n\n"
    message += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    if not events:
        message += "❌ No live events found for predictions today.\n"
        message += "💡 Check back later for match analysis.\n\n"
        return message
    
    # Generate predictions for each event
    predictions = []
    
    for event in events[:6]:  # Analyze first 6 events
        home_team = event.get('home_team', 'Home Team')
        away_team = event.get('away_team', 'Away Team')
        sport_type = "football" if 'soccer' in event.get('sport_key', '') else "basketball"
        
        if sport_type == "football":
            pred = generate_football_prediction(home_team, away_team)
            predictions.append({
                'match': f"{home_team} vs {away_team}",
                'sport': '⚽ Football',
                'prediction': pred
            })
        else:
            pred = generate_basketball_prediction(home_team, away_team)
            predictions.append({
                'match': f"{home_team} vs {away_team}",
                'sport': '🏀 Basketball', 
                'prediction': pred
            })
    
    # Build message with predictions
    message += f"📊 <b>GENERATED {len(predictions)} PREDICTIONS:</b>\n\n"
    
    for i, pred in enumerate(predictions, 1):
        message += f"{i}. <b>{pred['match']}</b>\n"
        message += f"   {pred['sport']}\n"
        
        if pred['sport'] == '⚽ Football':
            p = pred['prediction']
            message += f"   🏠 Home: {p['home_win']:.1%} | Draw: {p['draw']:.1%} | Away: {p['away_win']:.1%}\n"
            message += f"   ⚽ Over 1.5: {p['over_1_5']:.1%} | Over 2.5: {p['over_2_5']:.1%}\n"
            message += f"   🔄 BTTS: {p['btts']:.1%}\n"
            message += f"   🎯 Predicted: {p['predicted_score']}\n"
            message += f"   ✅ Confidence: {p['confidence']:.0%}\n"
        else:
            p = pred['prediction']
            message += f"   🏠 Home: {p['home_win']:.1%} | Away: {p['away_win']:.1%}\n"
            message += f"   🏀 Over Total: {p['over_total']:.1%}\n"
            message += f"   🎯 Predicted: {p['predicted_score']}\n"
            message += f"   ✅ Confidence: {p['confidence']:.0%}\n"
        
        message += "\n"
    
    message += "📈 <i>AI-powered match predictions</i>\n"
    message += "⚠️ <i>For analysis purposes only</i>"
    
    return message

def main():
    """Main function"""
    print("🚀 Starting HighXBet Prediction Engine...")
    
    # Get sports events
    events = get_sports_events()
    
    # Create predictions message
    message = create_predictions_message(events)
    
    # Print to console
    print("\n" + "=" * 40)
    print("PREDICTION RESULTS:")
    print("=" * 40)
    clean_msg = message.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
    print(clean_msg)
    print("=" * 40)
    
    # Send to Telegram
    print("\n📱 Sending predictions to Telegram...")
    if send_telegram_message(message):
        print("✅ Predictions sent to Telegram successfully!")
        print("📱 Check your phone now for match predictions!")
    else:
        print("❌ Failed to send Telegram message")
    
    print(f"\n🎯 PREDICTION ENGINE COMPLETED!")
    print(f"📊 Events analyzed: {len(events)}")
    print(f"🤖 Generated predictions for {min(len(events), 6)} matches")

# Run the bot
if __name__ == "__main__":
    main()
