import requests
from datetime import datetime

print("🤖 HIGHXBET SIMPLE ANALYZER")
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
        "soccer_uefa_champions_league" # Champions League
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

def create_analysis_message(events):
    """Create analysis message for Telegram"""
    message = "🎯 <b>HIGHXBET SPORTS ANALYSIS</b> 🎯\n\n"
    message += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    if not events:
        message += "❌ No live events found currently.\n"
        message += "💡 Try again later when matches are scheduled.\n\n"
        return message
    
    # Count by sport type
    football_matches = [e for e in events if 'soccer' in e.get('sport_key', '')]
    basketball_matches = [e for e in events if 'basketball' in e.get('sport_key', '')]
    
    message += f"📊 <b>EVENTS FOUND:</b>\n"
    message += f"⚽ Football: {len(football_matches)} matches\n"
    message += f"🏀 Basketball: {len(basketball_matches)} games\n\n"
    
    # Show top events
    message += "<b>TOP EVENTS TODAY:</b>\n"
    
    for i, event in enumerate(events[:8], 1):  # Show first 8 events
        home_team = event.get('home_team', 'Home Team')
        away_team = event.get('away_team', 'Away Team')
        sport = "⚽ Football" if 'soccer' in event.get('sport_key', '') else "🏀 Basketball"
        
        message += f"{i}. <b>{home_team} vs {away_team}</b>\n"
        message += f"   {sport}\n"
        message += f"   🕒 Commences: {event.get('commence_time', 'Today')[:10]}\n\n"
    
    message += "🔍 <i>Live sports data from The Odds API</i>\n"
    message += "📈 <i>Analysis ready for today's matches</i>"
    
    return message

def main():
    """Main function"""
    print("🚀 Starting HighXBet Analysis...")
    
    # Get sports events
    events = get_sports_events()
    
    # Create analysis message
    message = create_analysis_message(events)
    
    # Print to console
    print("\n" + "=" * 40)
    print("ANALYSIS RESULTS:")
    print("=" * 40)
    print(message.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', ''))
    print("=" * 40)
    
    # Send to Telegram
    print("\n📱 Sending to Telegram...")
    if send_telegram_message(message):
        print("✅ Telegram message sent successfully!")
        print("📱 Check your phone for the analysis!")
    else:
        print("❌ Failed to send Telegram message")
    
    print(f"\n🎯 ANALYSIS COMPLETED!")
    print(f"📊 Total events found: {len(events)}")
    print("🤖 Bot finished successfully!")

# Run the bot
if __name__ == "__main__":
    main()
