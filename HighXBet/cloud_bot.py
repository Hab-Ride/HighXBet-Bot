import pandas as pd
import requests
import json
from datetime import datetime
import os

print("🤖 HIGHXBET CLOUD BOT - RUNNING IN CLOUD")

def run_cloud_analysis():
    # Your existing bot code here (same as master_bot.py)
    # But optimized for cloud running
    print("🌐 Running in cloud environment...")
    
    # Add cloud-specific error handling
    try:
        # Your bot logic here
        print("✅ Cloud analysis completed!")
        
        # Send success message
        send_telegram_message("🤖 Cloud bot completed daily analysis!")
        
    except Exception as e:
        print(f"❌ Cloud error: {e}")
        send_telegram_message(f"❌ Bot error: {e}")

def send_telegram_message(message):
    """Send status to Telegram"""
    try:
        bot_token = "8534136877:AAFyD4a2jNR3MTZlpI3WEoS1oFTMWD7bzaQ"
        chat_id = "645815915"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        requests.post(url, json=payload, timeout=10)
    except:
        pass

if __name__ == "__main__":
    run_cloud_analysis()