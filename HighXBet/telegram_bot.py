import requests
import json
import time
from datetime import datetime

print("🤖 TELEGRAM BOT NOTIFIER")
print("=" * 50)

class TelegramNotifier:
    def __init__(self):
        self.config = self.load_config()
        self.bot_token = self.config['api']['telegram_bot_token']
        self.chat_id = self.config['api']['telegram_chat_id']
    
    def load_config(self):
        """Load configuration"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            print("❌ config.json not found")
            return {"api": {"telegram_bot_token": "YOUR_BOT_TOKEN", "telegram_chat_id": "YOUR_CHAT_ID"}}
    
    def send_message(self, message):
        """Send message via Telegram bot"""
        if self.bot_token == "YOUR_BOT_TOKEN" or self.chat_id == "YOUR_CHAT_ID":
            print("❌ Please set up Telegram credentials in config.json")
            print("💡 Check the setup guide below")
            return False
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print("✅ Telegram message sent successfully!")
                return True
            else:
                print(f"❌ Failed to send Telegram message: {response.status_code}")
                print("💡 Check if your bot token and chat ID are correct")
                return False
        except Exception as e:
            print(f"⚠️ Error sending Telegram message: {e}")
            return False
    
    def format_value_bet_message(self, value_bets):
        """Format value bets for Telegram message"""
        if not value_bets:
            return "❌ No value bets found today. Check back later!"
        
        message = "🎯 <b>VALUE BETS ALERT!</b> 🎯\n\n"
        message += f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        message += f"Found <b>{len(value_bets)}</b> high-value opportunities:\n\n"
        
        for i, bet in enumerate(value_bets, 1):
            # Use different emojis for top 3 bets
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
            message += f"   🏦 Bookmaker: {bet['bookmaker']}\n"
            
            # Add excitement based on value
            if bet['expected_value'] > 1.00:
                message += "   🚀 <b>MEGA VALUE OPPORTUNITY!</b> 🚀\n"
            elif bet['expected_value'] > 0.50:
                message += "   ⭐⭐⭐ <b>EXCEPTIONAL VALUE</b> ⭐⭐⭐\n"
            elif bet['expected_value'] > 0.20:
                message += "   ⭐⭐ <b>HIGH VALUE</b> ⭐⭐\n"
            else:
                message += "   ⭐ <b>GOOD VALUE</b> ⭐\n"
            
            message += "\n"
        
        message += "⚠️ <i>Always gamble responsibly. Do your own research.</i>"
        return message
    
    def test_connection(self):
        """Test Telegram connection"""
        print("🔍 Testing Telegram connection...")
        
        if self.bot_token == "YOUR_BOT_TOKEN":
            print("❌ Please set your Telegram Bot Token in config.json")
            return False
        
        # Simple test by getting bot info
        url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                bot_info = response.json()
                print(f"✅ Bot connected: {bot_info['result']['first_name']} (@{bot_info['result']['username']})")
                return True
            else:
                print(f"❌ Bot connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"⚠️ Connection error: {e}")
            return False

def setup_telegram_guide():
    """Guide for setting up Telegram"""
    print("\n📱 HOW TO SET UP TELEGRAM BOT:")
    print("=" * 60)
    print("1. Open Telegram and search for '@BotFather'")
    print("2. Send '/newbot' to create a new bot")
    print("3. Choose a name for your bot (e.g., 'ValueBetAlerts')")
    print("4. Choose a username ending with 'bot' (e.g., 'MyValueBetBot')")
    print("5. Copy the bot token (looks like: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)")
    print("6. Open config.json and replace 'YOUR_BOT_TOKEN' with this token")
    print("")
    print("🔍 HOW TO GET YOUR CHAT ID:")
    print("1. Start a chat with your new bot")
    print("2. Send any message to the bot (e.g., 'Hello')")
    print("3. Visit this URL in your browser (replace YOUR_BOT_TOKEN):")
    print("   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates")
    print("4. Look for 'chat': {'id': 123456789} in the response")
    print("5. Copy that number and replace 'YOUR_CHAT_ID' in config.json")
    print("=" * 60)

def get_demo_value_bets():
    """Create demo value bets like the ones we found"""
    return [
        {
            'match': 'Aston Villa vs West Ham',
            'bet_type': 'Under 2.5 Goals',
            'probability': 0.80,
            'odds': 4.2,
            'expected_value': 2.36,
            'bookmaker': 'Pinnacle',
            'confidence': 0.8
        },
        {
            'match': 'Newcastle vs Brighton',
            'bet_type': 'Under 2.5 Goals', 
            'probability': 0.75,
            'odds': 3.5,
            'expected_value': 1.625,
            'bookmaker': 'William Hill',
            'confidence': 0.8
        },
        {
            'match': 'Tottenham vs Man United',
            'bet_type': 'Over 2.5 Goals',
            'probability': 0.68,
            'odds': 3.2,
            'expected_value': 1.176,
            'bookmaker': 'Bet365', 
            'confidence': 1.0
        },
        {
            'match': 'Man City vs Liverpool',
            'bet_type': 'Over 2.5 Goals',
            'probability': 0.70,
            'odds': 2.8,
            'expected_value': 0.96,
            'bookmaker': 'Bet365',
            'confidence': 1.0
        },
        {
            'match': 'Arsenal vs Chelsea',
            'bet_type': 'Over 2.5 Goals',
            'probability': 0.70,
            'odds': 2.6,
            'expected_value': 0.82,
            'bookmaker': 'Bet365',
            'confidence': 1.0
        }
    ]

# Main execution
if __name__ == "__main__":
    print("🚀 BETTING BOT - TELEGRAM NOTIFIER")
    print("This sends value bet alerts to your phone!")
    print("=" * 50)
    
    # Initialize notifier
    notifier = TelegramNotifier()
    
    # Test connection
    connection_ok = notifier.test_connection()
    
    # Show setup guide if not configured
    if not connection_ok:
        setup_telegram_guide()
    
    # Create demo message with the value bets we found
    print("\n📨 CREATING DEMO ALERT...")
    demo_bets = get_demo_value_bets()
    message = notifier.format_value_bet_message(demo_bets)
    
    # Show what would be sent
    print("\n" + "=" * 60)
    print("📱 DEMO TELEGRAM MESSAGE (What you'll see on your phone):")
    print("=" * 60)
    # Remove HTML tags for console display
    clean_message = message.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
    print(clean_message)
    print("=" * 60)
    
    # Ask if user wants to send (if configured)
    if connection_ok:
        send = input("\n🤔 Do you want to send this to Telegram? (y/n): ").lower().strip()
        if send == 'y':
            notifier.send_message(message)
        else:
            print("💡 Message ready to send when you run the full bot!")
    else:
        print("\n💡 Set up your Telegram credentials to get real alerts!")
    
    print("\n🎯 NEXT: Let's combine everything into one master bot!")
    print("💡 You'll get these value bets sent to your phone automatically")
    
    input("\nPress Enter to exit...")