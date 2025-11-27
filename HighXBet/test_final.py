import requests
import json

def test_final_setup():
    print("🎯 FINAL SETUP TEST")
    print("=" * 50)
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    bot_token = config['api']['telegram_bot_token']
    chat_id = config['api']['telegram_chat_id']
    
    print("🤖 Testing Telegram connection...")
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        bot_info = response.json()
        print(f"✅ Bot: {bot_info['result']['first_name']}")
    else:
        print("❌ Bot connection failed")
        return
    
    print("📱 Sending welcome message...")
    message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': '🚀 <b>HIGHXBET PRO BOT ACTIVATED!</b>\n\nYour professional betting assistant is now ready!\n\n✅ Real odds from bookmakers\n✅ AI-powered predictions\n✅ Value bet alerts\n✅ Multi-league coverage\n\nGet ready for profitable opportunities! 💎',
        'parse_mode': 'HTML'
    }
    
    msg_response = requests.post(message_url, json=payload)
    if msg_response.status_code == 200:
        print("✅ Welcome message sent to your phone!")
        print("📱 Check Telegram now!")
    else:
        print(f"❌ Failed to send: {msg_response.status_code}")
    
    print("=" * 50)
    print("🎉 SETUP COMPLETE! You're ready to make money! 💰")

if __name__ == "__main__":
    test_final_setup()
    input("\nPress Enter to run the master bot...")